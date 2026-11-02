# -*- coding: utf-8 -*-
"""
British Columbia Grade 7 Math: Cartesian coordinates and graphing
(BC Mathematics Curriculum, Grade 7: Geometry and measurement)
  python3 tools/gen_cabc_math_g7_coordinates.py
HTML attributes use single quotes (no backslashes in the JSON).

Canadian English (counterclockwise, metre, centre). Whole-number coordinates from −6 to 6 on every grid;
negative numbers use the real minus sign. Every grid is square and exact: a point (x, y) sits x grid spaces
right (left if x < 0) of the origin and y spaces up (down if y < 0). Axis numbers, notes, dots and letter
labels never overlap (checked in Grid.render).
Wrong answers come from real mistakes: writing (y, x), dropping or flipping a minus sign, numbering the
quadrants clockwise, calling a point on an axis part of a quadrant, counting grid lines instead of spaces
(one too many), subtracting 4 − 3 for the length from −3 to 4 instead of 4 − (−3), giving a length as a
negative number, forgetting to double in a perimeter, mixing up area and perimeter, forgetting the 1/2 in a
triangle's area, reading the wrong column of a table of values, using the clock time as x.
Grade 7 students add and subtract integers, so lengths across an axis are explained as differences.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-7")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
GRID = "#c9d3cc"
QCOL = "#7a8a80"
FILL = "#e8f3ec"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
PEOPLE = [("Liam", "he", "his"), ("Olivia", "she", "her"), ("Ethan", "he", "his"), ("Ava", "she", "her"),
          ("Noah", "he", "his"), ("Chloe", "she", "her"), ("Arjun", "he", "his"), ("Simran", "she", "her"),
          ("Harjot", "he", "his"), ("Jasleen", "she", "her"), ("Wei", "he", "his"), ("Mei", "she", "her"),
          ("Ji-woo", "she", "her"), ("Mateo", "he", "his"), ("Hana", "she", "her"), ("Lucas", "he", "his"),
          ("Sofia", "she", "her"), ("Kai", "he", "his"), ("Emma", "she", "her"), ("Owen", "he", "his"),
          ("Leah", "she", "her"), ("Ryan", "he", "his"), ("Zara", "she", "her"), ("Nadia", "she", "her")]
QUADS = ["Quadrant I", "Quadrant II", "Quadrant III", "Quadrant IV"]


# ------------------------------------------------------------ numbers and pairs
def num(v):
    return (MINUS + str(-v)) if v < 0 else str(v)


def pair(x, y):
    return "(%s, %s)" % (num(x), num(y))


def quad(x, y):
    if x == 0 or y == 0:
        return None
    return {(1, 1): "Quadrant I", (-1, 1): "Quadrant II", (-1, -1): "Quadrant III", (1, -1): "Quadrant IV"}[
        (1 if x > 0 else -1, 1 if y > 0 else -1)]


def sub(a, b):
    """'4 − (−3) = 7' style difference a − b."""
    return "%s − %s = %s" % (num(a), ("(" + num(b) + ")") if b < 0 else num(b), num(a - b))


# ------------------------------------------------------------ question helpers
def mcq(q, correct, cands, e, rnd):
    seen = {correct}
    pick = []
    for c in cands:
        if c in seen or not c:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def mcq_fixed(q, choices, correct, e):
    """Choices keep their order (A B C D, numbers from small to large, quadrant words)."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fixed": True}


def mcq_int(q, correct, cands, e, unit=""):
    """Whole-number answers (negative wrong answers allowed), shown from small to large."""
    ch = []
    for c in cands:
        if c != correct and c not in ch:
            ch.append(c)
    ch = sorted([correct] + ch[:3])
    assert len(ch) == 4, (q, ch)

    def f(v):
        return num(v) + (unit[:-1] if abs(v) == 1 and unit.endswith("s") else unit)
    return mcq_fixed(q, [f(c) for c in ch], f(correct), e)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs, bold=False):
    """Approximate text width in px (Arial)."""
    return len(str(t)) * fs * (0.62 if bold else 0.58)


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK, extra=""):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, extra, t))


HALO = " stroke='#ffffff' stroke-width='4' paint-order='stroke'"


class People:
    def __init__(self, rnd):
        self.pool = list(PEOPLE)
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


class Pos:
    """Positions for picture answers (A-D), spread over the set."""

    def __init__(self, rnd):
        self.rnd, self.q = rnd, []

    def next(self):
        if not self.q:
            self.q = [0, 1, 2, 3]
            self.rnd.shuffle(self.q)
        return self.q.pop()


# ------------------------------------------------------------ four-quadrant grid
def overlap(a, b, m=1.0):
    return not (a[2] + m <= b[0] or b[2] + m <= a[0] or a[3] + m <= b[1] or b[3] + m <= a[1])


class Grid:
    """Square grid from -R to R on both axes. Grid space = u px. Every axis number is written."""

    def __init__(self, R=6, u=22, quads=False):
        assert 3 <= R <= 7
        self.R, self.u, self.quads = R, u, quads
        side = 2 * R * u
        self.ox = 24 + R * u
        self.oy = 34 + R * u
        self.W = self.H = int(math.ceil(24 + side + 34))
        self.pts, self.segs, self.arrows, self.notes, self.fills = [], [], [], [], []

    def P(self, x, y):
        return (self.ox + x * self.u, self.oy - y * self.u)

    def point(self, x, y, name, col=GREEN, where=None):
        assert x == int(x) and y == int(y) and abs(x) <= self.R and abs(y) <= self.R, (x, y)
        assert all((p[0], p[1]) != (x, y) for p in self.pts), ("two points at the same spot", x, y)
        self.pts.append((x, y, name, col, where))
        return self

    def seg(self, a, b, col=GREEN, w=3, dash=False, slant=False):
        assert slant or a[0] == b[0] or a[1] == b[1], "only grid-line segments"
        self.segs.append((a, b, col, w, dash))
        return self

    def poly(self, pts, col=GREEN, w=3, fill=True, dash_last=False, slant=False):
        """Closed shape (sides along grid lines unless slant); dash_last draws the last two sides dashed (missing vertex)."""
        n = len(pts)
        if fill:
            self.fills.append(list(pts))
        for i in range(n):
            if dash_last and i >= n - 2:
                self.seg(pts[i], pts[(i + 1) % n], col, 2, dash=True)
            else:
                self.seg(pts[i], pts[(i + 1) % n], col, w, slant=slant)
        return self

    def arrow(self, a, b, col=RED):
        assert a[0] == b[0] or a[1] == b[1]
        self.arrows.append((a, b, col))
        return self

    def note(self, gx, gy, t, anchor="middle", col=RED, fs=14):
        self.notes.append((gx, gy, t, anchor, col, fs))
        return self

    def _label_cell(self, x, y, used, others, boxes, where):
        dirs = [where] if where else [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dx, dy in dirs:
            cx, cy = x + dx, y + dy
            if not (abs(cx) <= self.R and abs(cy) <= self.R):
                continue
            corners = {(x + dx, y), (x, y + dy), (x + dx, y + dy)}
            if corners & others:                     # the square touches another point: the label could be misread
                continue
            cell = (min(x, cx), min(y, cy))
            if cell in used:
                continue
            c = self.P(x + dx / 2.0, y + dy / 2.0)
            box = (c[0] - 7, c[1] - 7, c[0] + 7, c[1] + 7)
            if any(overlap(box, b) for b in boxes):
                continue
            used.add(cell)
            return c, box
        raise AssertionError(("no room for label", x, y))

    def render(self):
        u, ox, oy, R = self.u, self.ox, self.oy, self.R
        s = []
        for f in self.fills:
            s.append("<polygon points='%s' fill='%s'/>" % (" ".join("%.1f,%.1f" % self.P(*p) for p in f), FILL))
        lo, hi = -R * u, R * u
        for k in range(-R, R + 1):
            if k == 0:
                continue
            x = ox + k * u
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (x, oy - hi, x, oy - lo, GRID))
            y = oy - k * u
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (ox + lo, y, ox + hi, y, GRID))
        # axes with arrows at both ends
        x0, x1 = ox + lo - 14, ox + hi + 14
        y0, y1 = oy - hi - 14, oy - lo + 14
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (x0 + 4, oy, x1 - 4, oy, INK))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (ox, y0 + 4, ox, y1 - 4, INK))
        for (ax, ay, dx, dy) in [(x1, oy, 1, 0), (x0, oy, -1, 0), (ox, y0, 0, -1), (ox, y1, 0, 1)]:
            bx, by = ax - dx * 9, ay - dy * 9
            s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>"
                     % (ax, ay, bx - dy * 4.5, by + dx * 4.5, bx + dy * 4.5, by - dx * 4.5, INK))
        s.append(text(x1 + 3, oy + 5, "x", 15, anchor="start", bold=True, extra=" font-style='italic'"))
        s.append(text(ox + 12, y0 + 8, "y", 15, anchor="start", bold=True, extra=" font-style='italic'"))
        assert x1 + 3 + 10 <= self.W and y0 - 4 >= 0
        boxes, nums = [], []
        # numbers on the axes (white halo; drawn over segments so they stay readable)
        for k in range(-R, R + 1):
            if k == 0:
                continue
            t = num(k)
            w = tw(t, 14)
            cx = ox + k * u
            boxes.append((cx - w / 2, oy + 5, cx + w / 2, oy + 15.5))
            nums.append(text(cx, oy + 15.5, t, 14, extra=HALO))
            cy = oy - k * u
            boxes.append((ox - 6 - w, cy - 5, ox - 6, cy + 5))
            nums.append(text(ox - 6, cy + 5, t, 14, anchor="end", extra=HALO))
        # no "0" at the origin: next to the x-axis "-1" it would read as "-10"
        for a, b, col, w, dash in self.segs:
            p, q = self.P(*a), self.P(*b)
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g' stroke-linecap='round'%s/>"
                     % (p[0], p[1], q[0], q[1], col, w, " stroke-dasharray='6 5'" if dash else ""))
        for a, b, col in self.arrows:
            p, q = self.P(*a), self.P(*b)
            L = math.hypot(q[0] - p[0], q[1] - p[1])
            d = ((q[0] - p[0]) / L, (q[1] - p[1]) / L)
            e = (q[0] - d[0] * 10, q[1] - d[1] * 10)
            n = (-d[1], d[0])
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (p[0], p[1], e[0] + d[0] * 2, e[1] + d[1] * 2, col))
            s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>"
                     % (q[0], q[1], e[0] + n[0] * 5.5, e[1] + n[1] * 5.5, e[0] - n[0] * 5.5, e[1] - n[1] * 5.5, col))
        s.extend(nums)
        notes = list(self.notes)
        if self.quads:
            m = R - 1
            for t, gx, gy in [("I", m, m + 0.5), ("II", -m, m + 0.5), ("III", -m, -m - 0.5), ("IV", m, -m - 0.5)]:
                notes.append((gx, gy, t, "middle", QCOL, 15))
        for gx, gy, t, anchor, col, fs in notes:
            c = self.P(gx, gy)
            w = tw(t, fs, True)
            x0_ = c[0] - w / 2 if anchor == "middle" else c[0] if anchor == "start" else c[0] - w
            box = (x0_, c[1] - fs * 0.4, x0_ + w, c[1] + fs * 0.4)
            assert box[0] >= 0 and box[2] <= self.W, t
            for b in boxes:
                assert not overlap(box, b), ("note overlaps", t)
            boxes.append(box)
            s.append(text(c[0], c[1] + fs * 0.36, t, fs, anchor=anchor, bold=True, col=col, extra=HALO))
        allpts = {(p[0], p[1]) for p in self.pts}
        for x, y, name, col, where in self.pts:
            c = self.P(x, y)
            dot = (c[0] - 4.5, c[1] - 4.5, c[0] + 4.5, c[1] + 4.5)
            for b in boxes:
                assert not overlap(dot, b, 0), ("dot on a number or note", x, y)
        used = set()
        for x, y, name, col, where in self.pts:
            c = self.P(x, y)
            s.append("<circle cx='%.1f' cy='%.1f' r='4.5' fill='%s'/>" % (c[0], c[1], col))
            if name:
                lc, box = self._label_cell(x, y, used, allpts - {(x, y)}, boxes, where)
                boxes.append(box)
                s.append(text(lc[0], lc[1] + 5.8, name, 16, bold=True, col=col if col == RED else INK))
        return "".join(s)

    def svg(self, label="coordinate grid"):
        return svg_wrap(self.W, self.H, self.render(), label)


def pts_grid(pts, label="coordinate grid", ref=None, quads=False):
    """pts: (x, y, name). ref: name of a point drawn in red."""
    assert all(max(abs(p[0]), abs(p[1])) <= 6 for p in pts), pts
    G = Grid(6, quads=quads)
    for x, y, n in pts:
        G.point(x, y, n, RED if n == ref else GREEN)
    return G.svg(label)


def table_svg(heads, top, bot, label):
    """Two-row table of values: heads = (top row name, bottom row name)."""
    CW, RH = 46, 32
    LW = int(max(tw(h, 15) for h in heads) + 20)
    k = len(top)
    W, H = LW + CW * k + 4, RH * 2 + 4
    s = []
    for r, (name, row) in enumerate([(heads[0], top), (heads[1], bot)]):
        y = 2 + r * RH
        s.append("<rect x='2' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (y, LW, RH, FILL, GREEN))
        s.append(text(2 + LW / 2, y + RH / 2 + 5, name, 15))
        for i, v in enumerate(row):
            x = 2 + LW + i * CW
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>" % (x, y, CW, RH, GREEN))
            s.append(text(x + CW / 2, y + RH / 2 + 6, v, 16, col=RED if v == "?" else INK))
    return svg_wrap(W, H, "".join(s), label)


def tbl(heads, xs, ys, missing=None, label="table of values"):
    return table_svg(heads, [num(v) for v in xs], ["?" if i == missing else num(v) for i, v in enumerate(ys)], label)


# ------------------------------------------------------------ explanations
def walk(x, y):
    a = "go 0 left or right" if x == 0 else ("go right %d" % x if x > 0 else "go left %d" % -x)
    b = "0 up or down" if y == 0 else ("up %d" % y if y > 0 else "down %d" % -y)
    return "Start at the origin, %s, then %s" % (a, b)


def read_cands(x, y):
    out = []
    for c in [(y, x), (abs(x), abs(y)), (-x, y), (x, -y), (-x, -y), (-y, -x)]:
        if c != (x, y) and c not in out:
            out.append(c)
    return [pair(*c) for c in out]


def pick_letters(target, others, pos):
    p = pos.next()
    cells = list(others)
    cells.insert(p, target)
    return [(c[0], c[1], "ABCD"[k]) for k, c in enumerate(cells)], "ABCD"[p]


def quad_e(x, y):
    sx = "positive (right)" if x > 0 else "negative (left)"
    sy = "positive (up)" if y > 0 else "negative (down)"
    return "x is %s and y is %s, so %s is in %s. The quadrants go counterclockwise from the top right: I, II, III, IV." % (
        sx, sy, pair(x, y), quad(x, y))


# ------------------------------------------------------------ set 1: the four quadrants and the axes
def set_quadrants(rnd, P):
    its = []
    pos = Pos(rnd)
    for x, y in [(4, 2), (-3, 5), (-1, -6), (5, -4), (-6, 3), (2, -1), (6, 6), (-4, -2)]:
        its.append(mcq_fixed("Which quadrant is the point %s in?" % pair(x, y), QUADS, quad(x, y), quad_e(x, y)))
    its.append(mcq_fixed("Where is the point %s?" % pair(0, 5), ["Quadrant I", "Quadrant II", "on the x-axis", "on the y-axis"],
                         "on the y-axis",
                         "x = 0, so the point does not move left or right. It goes up 5 along the y-axis. "
                         "A point on an axis is not in any quadrant."))
    its.append(mcq_fixed("Where is the point %s?" % pair(3, 0), ["Quadrant I", "Quadrant IV", "on the x-axis", "on the y-axis"],
                         "on the x-axis",
                         "y = 0, so the point does not move up or down. It goes right 3 along the x-axis. It is not in any quadrant."))
    its.append(mcq_fixed("What is the name of the point (0, 0), where the axes cross?",
                         ["the x-axis", "the origin", "Quadrant I", "the y-axis"], "the origin",
                         "The x-axis and the y-axis cross at (0, 0). This point is called the origin. Every point is plotted by starting there."))
    its.append(mcq_fixed("In which quadrant is the x-coordinate negative and the y-coordinate positive?", QUADS, "Quadrant II",
                         "Negative x means left and positive y means up. Left and up is the top-left part: Quadrant II."))
    its.append(mcq_fixed("In which quadrant are both coordinates negative?", QUADS, "Quadrant III",
                         "Negative x means left and negative y means down. Left and down is the bottom-left part: Quadrant III."))
    its.append(mcq("What are the signs of the coordinates of a point in Quadrant IV?", "(+, " + MINUS + ")",
                   ["(" + MINUS + ", +)", "(" + MINUS + ", " + MINUS + ")", "(+, +)"],
                   "Quadrant IV is the bottom-right part. Right means x is positive and down means y is negative: (+, " + MINUS + ").", rnd))
    its.append(mcq("Which point is in Quadrant III?", pair(-2, -5), [pair(2, 5), pair(-2, 5), pair(2, -5)],
                   "Quadrant III is the bottom-left part: x negative (left) and y negative (down). %s is left 2 and down 5." % pair(-2, -5), rnd))
    its.append(mcq("A point is on the x-axis. What must be true?", "Its y-coordinate is 0",
                   ["Its x-coordinate is 0", "Both coordinates are 0", "Its y-coordinate is negative"],
                   "On the x-axis, you do not move up or down from the origin, so y = 0. Examples: %s and (4, 0)." % pair(-5, 0), rnd))
    for target, others, qn in [
        ((-4, -3), [(4, 3), (3, -4), (-3, 4)], "Quadrant III"),
        ((5, -2), [(-2, 5), (2, 5), (-5, -2)], "Quadrant IV"),
    ]:
        pts, ans = pick_letters(target, others, pos)
        where = {(p[0], p[1]): p[2] for p in pts}
        e = "Point %s is at %s. %s" % (ans, pair(*target), quad_e(*target))
        if qn == "Quadrant IV":
            e += " Point %s is in Quadrant II: numbering the quadrants clockwise would wrongly call it IV." % where[(-2, 5)]
        its.append(mcq_fixed(fig(pts_grid(pts, "coordinate grid with points A to D")) +
                             "Which point is in %s?" % qn, ["A", "B", "C", "D"], ans, e))
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq("%s says %s is in Quadrant II. What mistake did %s make?" % (n, pair(4, -1), he),
                   "%s numbered the quadrants clockwise" % H,
                   ["%s swapped x and y" % H, "%s ignored the minus sign" % H, "No mistake. %s is right" % H],
                   "%s is right and down: Quadrant IV. The quadrants go counterclockwise: I top right, II top left, "
                   "III bottom left, IV bottom right." % pair(4, -1), rnd))
    n, he, his = P.next()
    its.append(mcq("%s says %s is in Quadrant III because it has a minus sign. Is %s right?" % (n, pair(-6, 0), he),
                   "No, it is on the x-axis, not in a quadrant",
                   ["Yes, x is negative", "No, it is in Quadrant II", "No, it is on the y-axis"],
                   "y = 0, so the point sits on the x-axis, 6 units left of the origin. Points on an axis are not in any quadrant.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "The four quadrants and the axes", "items": its}


# ------------------------------------------------------------ set 2: read points
def set_read(rnd, P):
    its = []
    pos = Pos(rnd)
    reads = [
        [(3, 5, "A")], [(-4, 2, "B")], [(-2, -6, "C"), (-6, -2, "D")], [(5, -3, "E")],
        [(-5, 4, "F"), (4, -5, "G")], [(6, -1, "H")], [(-3, -3, "J")], [(0, 4, "K"), (4, 0, "L")],
        [(-1, 6, "M")], [(-6, 0, "N")], [(1, -5, "T"), (-5, 1, "U")], [(0, -3, "V")],
    ]
    for pts in reads:
        x, y, n = pts[0]
        e = "%s. Point %s is at %s. Write the x-coordinate first; a minus sign means left or down." % (walk(x, y), n, pair(x, y))
        if (y, x) in [(p[0], p[1]) for p in pts[1:]]:
            e += " %s is point %s: the numbers are swapped." % (pair(y, x), pts[1][2])
        its.append(mcq(fig(pts_grid(pts, "coordinate grid with labelled points")) +
                       "What are the coordinates of point %s?" % n, pair(x, y), read_cands(x, y), e, rnd))
    its.append(mcq_int(fig(pts_grid([(-5, 3, "R")], "coordinate grid with labelled points")) +
                       "What is the x-coordinate of point R?", -5, [5, 3, -3],
                       "Point R is 5 units to the left of the y-axis, so x = " + num(-5) + ". Left means negative. (3 is its y-coordinate.)"))
    its.append(mcq_int(fig(pts_grid([(2, -4, "S")], "coordinate grid with labelled points")) +
                       "What is the y-coordinate of point S?", -4, [4, 2, -2],
                       "Point S is 4 units below the x-axis, so y = " + num(-4) + ". Down means negative. (2 is its x-coordinate.)"))
    # which point has a given coordinate
    for (target, others, ask, e) in [
        ((-3, 4), [(4, -3), (3, 1), (1, -2)], "Which point has an x-coordinate of %s?" % num(-3),
         "x = %s means 3 units left of the y-axis. Only point %%s is there, at %s. Point %%s has y = %s, not x." % (num(-3), pair(-3, 4), num(-3))),
        ((5, -2), [(-2, 5), (-5, 2), (2, 3)], "Which point has a y-coordinate of %s?" % num(-2),
         "y = %s means 2 units below the x-axis. Only point %%s is there, at %s. Point %%s has x = %s, not y." % (num(-2), pair(5, -2), num(-2))),
    ]:
        pts, ans = pick_letters(target, others, pos)
        where = {(p[0], p[1]): p[2] for p in pts}
        its.append(mcq_fixed(fig(pts_grid(pts, "coordinate grid with points A to D")) + ask,
                             ["A", "B", "C", "D"], ans, e % (ans, where[others[0]])))
    pts, ans = pick_letters((-2, -5), [(2, 5), (-5, 2), (5, -2)], pos)
    where = {(p[0], p[1]): p[2] for p in pts}
    its.append(mcq_fixed(fig(pts_grid(pts, "coordinate grid with points A to D")) +
                         "Which point has two negative coordinates?", ["A", "B", "C", "D"], ans,
                         "Both coordinates are negative when the point is left of the y-axis and below the x-axis (Quadrant III). "
                         "Point %s is at %s." % (ans, pair(-2, -5))))
    its.append(mcq(fig(pts_grid([(-4, 1, "P"), (3, 1, "Q"), (3, -5, "T")], "coordinate grid with points P, Q and T")) +
                   "Which two points have the same y-coordinate?", "P and Q", ["Q and T", "P and T", "All three points"],
                   "P is at %s and Q is at %s. Both are 1 unit above the x-axis, so both have y = 1. "
                   "Q and T have the same x-coordinate, 3, not the same y-coordinate." % (pair(-4, 1), pair(3, 1)), rnd))
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq(fig(pts_grid([(-2, 5, "W")], "coordinate grid with point W")) +
                   "%s writes the coordinates of point W as %s. What mistake did %s make?" % (n, pair(5, -2), he),
                   "%s wrote the y-coordinate first" % H,
                   ["%s counted the grid lines, not the spaces" % H, "%s dropped a minus sign" % H, "No mistake. %s is right" % H],
                   "W is left 2 and up 5, so it is at %s. %s put the numbers in the wrong order. "
                   "Always write x (across) first, then y (up or down)." % (pair(-2, 5), n), rnd))
    its.append(mcq("A point is 6 units to the left of the y-axis and 4 units below the x-axis. What are its coordinates?",
                   pair(-6, -4), [pair(-4, -6), pair(6, 4), pair(6, -4)],
                   "Left of the y-axis means x is negative: x = %s. Below the x-axis means y is negative: y = %s. "
                   "The point is %s." % (num(-6), num(-4), pair(-6, -4)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Read the coordinates of points", "items": its}


# ------------------------------------------------------------ set 3: plot points
def set_plot(rnd, P):
    its = []
    pos = Pos(rnd)
    for (x, y), others in [
        ((2, 5), [(5, 2), (-2, 5), (2, -5)]),
        ((-4, 3), [(3, -4), (4, 3), (-4, -3)]),
        ((-5, -2), [(-2, -5), (5, -2), (-5, 2)]),
        ((3, -6), [(-6, 3), (-3, -6), (3, 6)]),
        ((-2, 6), [(6, -2), (2, 6), (-2, -6)]),
        ((6, -4), [(-4, 6), (-6, -4), (6, 4)]),
        ((-6, -5), [(-5, -6), (6, -5), (-6, 5)]),
        ((0, -5), [(-5, 0), (0, 5), (5, -5)]),
        ((4, 0), [(0, 4), (-4, 0), (4, 4)]),
        ((-2, 4), [(4, -2), (2, 4), (-2, -4)]),
    ]:
        pts, ans = pick_letters((x, y), others, pos)
        where = {(p[0], p[1]): p[2] for p in pts}
        e = "%s: that is point %s." % (walk(x, y), ans)
        if (y, x) in where:
            e += " Point %s is at %s: the numbers are swapped." % (where[(y, x)], pair(y, x))
        elif (-x, y) in where and x != 0:
            e += " Point %s is at %s: the sign of x is wrong." % (where[(-x, y)], pair(-x, y))
        its.append(mcq_fixed(fig(pts_grid(pts, "coordinate grid with points A to D")) +
                             "Which point is at %s?" % pair(x, y), ["A", "B", "C", "D"], ans, e))
    its.append(mcq("To plot %s, what do you do first from the origin?" % pair(-3, 6), "Go left 3",
                   ["Go right 3", "Go up 6", "Go left 6"],
                   "The first number, " + num(-3) + ", is the x-coordinate. It is negative, so go left 3. Then go up 6.", rnd))
    its.append(mcq("To plot %s, you go right 4 from the origin. What do you do next?" % pair(4, -2), "Go down 2",
                   ["Go up 2", "Go left 2", "Go right 2"],
                   "The second number, " + num(-2) + ", is the y-coordinate. It is negative, so go down 2.", rnd))
    # plotted wrong
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq(fig(pts_grid([(-1, 5, "X")], "coordinate grid with point X")) +
                   "%s was asked to plot %s. %s plotted point X. What mistake did %s make?" % (n, pair(5, -1), H, he),
                   "%s went up or down first" % H,
                   ["%s dropped the minus sign" % H, "%s counted the grid lines, not the spaces" % H, "No mistake. %s is right" % H],
                   "X is at %s. To plot %s, go right 5 first (x), then down 1 (y). %s used the numbers in the wrong order."
                   % (pair(-1, 5), pair(5, -1), n), rnd))
    plan = [(2, 3, "A"), (-4, 1, "B"), (-3, -2, "C"), (5, -4, "D")]
    k = pos.next()
    drawn = [((p[1], p[0], p[2]) if i == k else p) for i, p in enumerate(plan)]
    lst = ", ".join("%s %s" % (p[2], pair(p[0], p[1])) for p in plan)
    its.append(mcq_fixed(fig(pts_grid(drawn, "coordinate grid with points A to D")) +
                         "Mei wants to plot %s. Which point did she plot in the wrong place?" % lst,
                         ["A", "B", "C", "D"], "ABCD"[k],
                         "Point %s should be at %s, but it is at %s: x and y are swapped. The other points are correct."
                         % ("ABCD"[k], pair(plan[k][0], plan[k][1]), pair(plan[k][1], plan[k][0]))))
    its.append(mcq("You plot %s and %s and join them with a line segment. What kind of segment is it?" % (pair(-4, 3), pair(5, 3)),
                   "horizontal (parallel to the x-axis)",
                   ["vertical (parallel to the y-axis)", "on the x-axis", "slanted"],
                   "Both points have y = 3, so both are 3 units up. The segment runs straight across, parallel to the x-axis.", rnd))
    its.append(mcq("Which point would you plot in the same quadrant as %s?" % pair(-2, -6), pair(-5, -1),
                   [pair(5, 1), pair(-5, 1), pair(5, -1)],
                   "%s is left and down: Quadrant III. %s is also left and down." % (pair(-2, -6), pair(-5, -1)), rnd))
    its.append(mcq("Which point would you plot on the y-axis?", pair(0, -3),
                   [pair(-3, 0), pair(-3, -3), pair(3, 3)],
                   "A point on the y-axis does not move left or right, so x = 0. %s goes down 3 along the y-axis." % pair(0, -3), rnd))
    its.append(mcq("You plot a point 3 units to the right of %s. Where is the new point?" % pair(-5, 2), pair(-2, 2),
                   [pair(-8, 2), pair(-5, 5), pair(2, -2)],
                   "Moving right changes only x. %s + 3 = %s, so the new point is %s. y stays 2." % (num(-5), num(-2), pair(-2, 2)), rnd))
    n, he, his = P.next()
    its.append(mcq("%s plots the point %s. Which moves from the origin are correct?" % (n, pair(-3, -4)),
                   "left 3, then down 4", ["left 4, then down 3", "right 3, then down 4", "left 3, then up 4"],
                   "x = %s: go left 3. y = %s: go down 4. Always do x first." % (num(-3), num(-4)), rnd))
    its.append(mcq("You plot a point 2 units below %s. Where is the new point?" % pair(4, 1), pair(4, -1),
                   [pair(2, 1), pair(4, 3), pair(-1, 4)],
                   "Moving down changes only y. 1 − 2 = %s, so the new point is %s. x stays 4." % (num(-1), pair(4, -1)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Plot points in all four quadrants", "items": its}


# ------------------------------------------------------------ set 4: shapes on the plane
def length_e(a, b):
    """Length of a segment along a grid line, explained with integer subtraction."""
    i = 0 if a[1] == b[1] else 1
    nm = "x" if i == 0 else "y"
    hi, lo = max(a[i], b[i]), min(a[i], b[i])
    return "Only %s changes, from %s to %s. Length = %s units (larger − smaller)." % (nm, num(lo), num(hi), sub(hi, lo))


def set_shapes(rnd, P):
    its = []
    pos = Pos(rnd)
    # missing vertex of a rectangle, with a figure
    for A, B, C in [((-4, 3), (2, 3), (2, -2)), ((-5, -1), (-5, 4), (3, 4))]:
        D = (A[0] + C[0] - B[0], A[1] + C[1] - B[1])
        G = Grid(6)
        G.poly([A, B, C, D], dash_last=True)
        G.point(A[0], A[1], "A").point(B[0], B[1], "B").point(C[0], C[1], "C")
        cands = [pair(D[1], D[0]), pair(-D[0], D[1]), pair(D[0], -D[1]), pair(*B)]
        its.append(mcq(fig(G.svg("coordinate grid with rectangle vertices A, B and C")) +
                       "A, B and C are three vertices of rectangle ABCD. What are the coordinates of D?",
                       pair(*D), cands,
                       "D lines up with A and with C. It has the same %s-coordinate as A (%s) and the same %s-coordinate as C (%s). "
                       "D is %s." % ("x" if A[0] == D[0] else "y", num(A[0] if A[0] == D[0] else A[1]),
                                     "y" if A[0] == D[0] else "x", num(C[1] if A[0] == D[0] else C[0]), pair(*D)), rnd))
    # missing vertex, text only
    for A, B, C in [((-3, -2), (4, -2), (4, 5)), ((1, -6), (-5, -6), (-5, -1))]:
        D = (A[0] + C[0] - B[0], A[1] + C[1] - B[1])
        cands = [pair(D[1], D[0]), pair(-D[0], D[1]), pair(D[0], -D[1]), pair(C[1], A[0])]
        its.append(mcq("A rectangle has vertices at %s, %s and %s. What are the coordinates of the fourth vertex?"
                       % (pair(*A), pair(*B), pair(*C)), pair(*D), cands,
                       "The sides of the rectangle run along grid lines. The fourth vertex is across from %s. "
                       "It takes x from one neighbour and y from the other: %s." % (pair(*B), pair(*D)), rnd))
    # lengths along grid lines
    for a, b in [((-3, 2), (4, 2)), ((5, -4), (5, 1)), ((-6, -1), (-2, -1)), ((-2, -5), (-2, 3))]:
        L = abs(a[0] - b[0]) + abs(a[1] - b[1])
        i = 0 if a[1] == b[1] else 1
        hi, lo = max(a[i], b[i]), min(a[i], b[i])
        cands = [abs(abs(hi) - abs(lo)), abs(hi) + abs(lo), L + 1, lo - hi]
        if lo < 0 < hi:
            e = length_e(a, b) + " The segment crosses an axis: %d units on one side and %d on the other, %d + %d = %d." % (
                -lo, hi, -lo, hi, L)
        else:
            e = length_e(a, b) + " Both ends are on the same side of the axis, so do not add %d and %d." % (abs(lo), abs(hi))
        q = "What is the length of the line segment from %s to %s?" % (pair(*a), pair(*b))
        if a == (5, -4):
            G = Grid(6)
            G.seg(a, b)
            G.point(a[0], a[1], "P").point(b[0], b[1], "Q")
            q = fig(G.svg("coordinate grid with segment PQ")) + "What is the length of segment PQ?"
            e = "P is at %s and Q is at %s. " % (pair(*a), pair(*b)) + e
        its.append(mcq_int(q, L, cands, e, " units"))
    its.append(mcq_int("How far is the point %s from the x-axis?" % pair(-5, 4), 4, [5, 9, 1],
                       "The distance to the x-axis is how far up or down the point is: the y-coordinate, 4 units. "
                       "(5 units is the distance to the y-axis.)", " units"))
    # perimeter and area
    R = [(-4, 3), (2, 3), (2, -1), (-4, -1)]
    G = Grid(6)
    G.poly(R)
    for p, nm in zip(R, "ABCD"):
        G.point(p[0], p[1], nm)
    its.append(mcq_int(fig(G.svg("coordinate grid with rectangle ABCD")) + "What is the perimeter of rectangle ABCD?",
                       20, [10, 24, 28],
                       "Length AB: %s units. Width BC: %s units. Perimeter = 6 + 4 + 6 + 4 = 20 units. "
                       "(24 is the area; 10 adds only two sides.)" % (sub(2, -4), sub(3, -1)), " units"))
    its.append(mcq_int("A rectangle has vertices at %s, %s, %s and %s. What is its area?" % (pair(-3, 4), pair(2, 4), pair(2, -2), pair(-3, -2)),
                       30, [22, 6, 42],
                       "Length: %s units. Width: %s units. Area = 5 × 6 = 30 square units. (22 is the perimeter; "
                       "6 × 7 = 42 comes from counting grid lines.)" % (sub(2, -3), sub(4, -2)), " square units"))
    T = [(-3, -2), (3, -2), (3, 2)]
    G = Grid(6)
    G.poly(T, slant=True)
    G.point(-3, -2, "A", where=(-1, -1)).point(3, -2, "B", where=(1, -1)).point(3, 2, "C", where=(1, 1))
    its.append(mcq_int(fig(G.svg("coordinate grid with right triangle ABC")) + "What is the area of triangle ABC?",
                       12, [24, 10, 20],
                       "Base AB: %s units. Height BC: %s units. Area = base × height ÷ 2 = 6 × 4 ÷ 2 = 12 square units. "
                       "(24 forgets to divide by 2.)" % (sub(3, -3), sub(2, -2)), " square units"))
    its.append(mcq_fixed("The points %s, %s, %s and %s are joined in order. What shape do they make?"
                         % (pair(-3, 1), pair(2, 1), pair(2, -4), pair(-3, -4)),
                         ["a square", "a rectangle that is not a square", "a trapezoid", "a parallelogram with no right angles"],
                         "a square",
                         "The sides run along grid lines, so the angles are right angles. Across: %s. Down: %s. "
                         "All four sides are 5 units, so it is a square." % (sub(2, -3), sub(1, -4))))
    its.append(mcq("Two vertices of a square are %s and %s. The other two vertices are above them. Where are they?"
                   % (pair(-2, 1), pair(2, 1)),
                   "%s and %s" % (pair(-2, 5), pair(2, 5)),
                   ["%s and %s" % (pair(-2, 3), pair(2, 3)), "%s and %s" % (pair(-2, -3), pair(2, -3)),
                    "%s and %s" % (pair(-2, 6), pair(2, 6))],
                   "The side length is %s units. Go up 4 from y = 1: 1 + 4 = 5. The vertices are %s and %s. "
                   "(Using 2 as the side length gives y = 3; counting grid lines gives 5 units and y = 6.)"
                   % (sub(2, -2), pair(-2, 5), pair(2, 5)), rnd))
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq("%s says the segment from %s to %s is 1 unit long. What mistake did %s make?" % (n, pair(-3, 6), pair(4, 6), he),
                   "%s did 4 − 3 instead of 4 − (%s)" % (H, num(-3)),
                   ["%s counted the grid lines, not the spaces" % H, "%s used the y-coordinates" % H, "No mistake. %s is right" % H],
                   "The length is %s units. Subtracting a negative is the same as adding: 4 + 3 = 7." % sub(4, -3), rnd))
    its.append(mcq("The points %s and %s are joined. Which is true?" % (pair(-4, -1), pair(-4, 5)),
                   "It is a vertical segment 6 units long",
                   ["It is a horizontal segment 6 units long", "It is a vertical segment 4 units long",
                    "It is a vertical segment 7 units long"],
                   "Both points have x = %s, so the segment goes straight up and down. Length = %s units." % (num(-4), sub(5, -1)), rnd))
    its.append(mcq_fixed("A rectangle has vertices at %s, %s and %s. In which quadrant is the fourth vertex?"
                         % (pair(-5, 2), pair(3, 2), pair(3, -4)), QUADS, "Quadrant III",
                         "The fourth vertex takes x from %s and y from %s: %s. x is negative and y is negative, "
                         "so it is in Quadrant III." % (pair(-5, 2), pair(3, -4), pair(-5, -4))))
    n, he, his = P.next()
    its.append(mcq("%s draws a map of Stanley Park on a grid where each unit is 10 m. The playground is at %s and the "
                   "washroom is at %s. How far apart are they?" % (n, pair(-3, 4), pair(-3, -2)),
                   "60 m", ["20 m", "70 m", "6 m"],
                   "Only y changes: %s units. Each unit is 10 m, so 6 × 10 = 60 m. "
                   "(4 − 2 = 2 gives 20 m; 6 m forgets the scale.)" % sub(4, -2), rnd))
    n, he, his = P.next()
    its.append(mcq("%s plans a rectangular school garden in Burnaby on a grid map where each unit is 1 m. The corners are at "
                   "%s, %s, %s and %s. How much fencing goes around the garden?"
                   % (n, pair(-4, -3), pair(3, -3), pair(3, 1), pair(-4, 1)),
                   "22 m", ["11 m", "28 m", "26 m"],
                   "Length: %s m. Width: %s m. Perimeter = 7 + 4 + 7 + 4 = 22 m. "
                   "(28 is the area in square metres; 11 goes only halfway around.)" % (sub(3, -4), sub(1, -3)), rnd))
    its.append(mcq("A rectangle is 5 units wide and 3 units tall. Its bottom-left vertex is at %s. "
                   "Where is its top-right vertex?" % pair(-1, -1),
                   pair(4, 2), [pair(2, 4), pair(5, 3), pair(-6, 2)],
                   "Go right 5 for the width: %s + 5 = 4. Go up 3 for the height: %s + 3 = 2. The vertex is %s. "
                   "(5, 3) forgets to start from %s." % (num(-1), num(-1), pair(4, 2), pair(-1, -1)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Shapes on the Cartesian plane: missing vertices and side lengths", "items": its}


# ------------------------------------------------------------ set 5: graph a table of values (BC word problems)
def set_tables(rnd, P):
    its = []
    pos = Pos(rnd)
    # A: Prince George winter morning: x = hours after 6 a.m., y = °C
    xs, ys = [0, 1, 2, 3, 4], [-5, -3, -1, 1, 3]
    T = tbl(("Hours after 6 a.m. (x)", "Temperature, °C (y)"), xs, ys, label="table of values: hours after 6 a.m. and temperature")
    its.append(mcq(fig(T) + "On a winter morning in Prince George, the temperature rises 2 °C each hour. "
                   "Which ordered pair (x, y) shows the temperature at 8 a.m.?", pair(2, -1),
                   [pair(-1, 2), pair(2, 1), pair(8, -1)],
                   "8 a.m. is 2 hours after 6 a.m., so x = 2. The table gives y = %s. Write x first: %s. "
                   "(x is hours after 6 a.m., not the clock time.)" % (num(-1), pair(2, -1)), rnd))
    G = Grid(6)
    for x, y in zip(xs, ys):
        G.point(x, y, None)
    its.append(mcq_fixed(fig(G.svg("graph of the temperature table: points (0, −5) to (4, 3)")) +
                         "This graph shows the Prince George temperatures (x = hours after 6 a.m., y = temperature in °C). "
                         "The points for which hours are in Quadrant IV?",
                         ["hours 0, 1 and 2", "hours 1 and 2", "hours 3 and 4", "hours 2, 3 and 4"], "hours 1 and 2",
                         "Quadrant IV needs x positive and y negative. Hours 1 and 2 have temperatures below 0 °C. "
                         "Hour 0, %s, is on the y-axis, so it is not in a quadrant." % pair(0, -5)))
    its.append(mcq_int("In Prince George it is 3 °C at 10 a.m. (x = 4). The temperature keeps rising 2 °C each hour. "
                       "What is the temperature at 11 a.m.?", 5, [4, 7, 3],
                       "11 a.m. is x = 5, one hour after x = 4. Add 2 °C: 3 + 2 = 5 °C. The point is %s. "
                       "(4 °C adds only 1; 7 °C adds 2 hours.)" % pair(5, 5), " °C"))
    # B: Owen pays back a loan
    n, he, his = ("Owen", "he", "his")
    plan = [(0, -6), (1, -4), (2, -2), (3, 0)]
    k = pos.next()
    drawn = [((p[1], p[0]) if i == k else p) for i, p in enumerate(plan)]
    G = Grid(6)
    for (x, y), nm in zip(drawn, "ABCD"):
        G.point(x, y, nm)
    its.append(mcq_fixed(fig(G.svg("graph of Owen’s balance: points A to D")) +
                         "Owen owes his sister $6, so his balance is %s$6. He pays back $2 each week. He graphs (week, balance) "
                         "for weeks 0 to 3. Which point is plotted in the wrong place?" % MINUS,
                         ["A", "B", "C", "D"], "ABCD"[k],
                         "The pairs are %s. Point %s is at %s: x and y are swapped. It should be at %s."
                         % (", ".join(pair(*p) for p in plan), "ABCD"[k], pair(*drawn[k]), pair(*plan[k]))))
    its.append(mcq_int("Owen’s balance starts at %s$6 and goes up $2 each week. In which week does his graph reach the x-axis "
                       "(balance $0)?" % MINUS, 3, [2, 6, 4],
                       "%s$6 + $2 + $2 + $2 = $0, so it takes 3 weeks. The point is (3, 0), on the x-axis. "
                       "(6 forgets that he pays $2 each week.)" % MINUS))
    its.append(mcq("Owen’s balance starts at %s$6 (week 0) and goes up $2 each week. Which ordered pair (week, balance) "
                   "shows his balance after week 1?" % MINUS, pair(1, -4), [pair(-4, 1), pair(1, 4), pair(1, -2)],
                   "After 1 week: %s6 + 2 = %s. x = 1 and y = %s: %s. (%s is week 2’s balance.)"
                   % (MINUS, num(-4), num(-4), pair(1, -4), num(-2)), rnd))
    # C: diver
    xs, ys = [0, 1, 2, 3], [0, -2, -4, -6]
    its.append(mcq(fig(tbl(("Minutes (x)", "Depth, m (y)"), xs, ys, label="table of values: minutes and depth")) +
                   "Leah is scuba diving off Vancouver Island. She starts at the surface and goes down 2 m each minute. "
                   "Which rule matches the table?", "y = %s2x" % MINUS,
                   ["y = 2x", "y = x %s 2" % MINUS, "y = %sx" % MINUS],
                   "Each minute, y goes down by 2, and y = 0 when x = 0. So y = %s2 × x. Check: x = 3 gives %s2 × 3 = %s."
                   % (MINUS, MINUS, num(-6)), rnd))
    G = Grid(6)
    for x, y in zip(xs, ys):
        G.point(x, y, None)
    its.append(mcq_fixed(fig(G.svg("graph of Leah’s dive: points (0, 0) to (3, −6)")) +
                         "This graph shows Leah’s dive (x = minutes, y = depth in metres). In which quadrant are the points after the start?",
                         QUADS, "Quadrant IV",
                         "After the start, x is positive (time goes on) and y is negative (below the surface). "
                         "Right and down is Quadrant IV. The start, (0, 0), is the origin."))
    # D: rule y = x + 2
    xs, ys = [-3, -2, -1, 0, 1], [-1, 0, 1, 2, 3]
    its.append(mcq_int(fig(tbl(("x", "y = x + 2"), xs, ys, missing=2, label="table of values for y = x + 2 with one value missing")) +
                       "Ji-woo makes a table of values for y = x + 2. What is the missing value?", 1, [3, -3, -1],
                       "x = %s. y = %s + 2 = 1. (3 forgets the minus sign; %s subtracts 2.)" % (num(-1), num(-1), num(-3))))
    G = Grid(6)
    for x, y in zip(xs, ys):
        G.point(x, y, None)
    its.append(mcq(fig(G.svg("graph of five points on a line: (−3, −1) to (1, 3)")) +
                   "Ji-woo graphs the points from the table. Which rule matches the graph?", "y = x + 2",
                   ["y = x %s 2" % MINUS, "y = 2x", "y = 2x + 2"],
                   "Read a point: (0, 2). With y = x + 2, x = 0 gives 2. Check (%s, %s): %s + 2 = %s. "
                   "y = 2x gives 0 at x = 0, so it does not match." % (num(-3), num(-1), num(-3), num(-1)), rnd))
    its.append(mcq("Ji-woo’s table for y = x + 2 has x = %s, %s, %s, 0 and 1. Which of its points is on the y-axis?"
                   % (num(-3), num(-2), num(-1)), pair(0, 2), [pair(2, 0), pair(-2, 0), pair(0, -2)],
                   "A point on the y-axis has x = 0. When x = 0, y = 0 + 2 = 2, so the point is (0, 2). "
                   "(%s is the table’s point on the x-axis.)" % pair(-2, 0), rnd))
    # E: game sprite y = 2x - 1
    n, he, his = P.next()
    its.append(mcq("%s is coding a game. %s sprite moves along these points: %s, %s, %s and %s. "
                   "Which point comes next in the pattern?" % (n, his.capitalize(), pair(-2, -5), pair(-1, -3), pair(0, -1), pair(1, 1)),
                   pair(2, 3), [pair(3, 2), pair(2, 2), pair(2, -3)],
                   "x goes up by 1 each time and y goes up by 2. After %s comes (1 + 1, 1 + 2) = %s." % (pair(1, 1), pair(2, 3)), rnd))
    G = Grid(6)
    for x in [-4, -3, -2, -1, 0]:
        G.point(x, 2 * x + 3, None)
    its.append(mcq(fig(G.svg("graph of points (−4, −5) to (0, 3) on a line")) +
                   "%s changes %s sprite’s path. This graph shows the new path. When x goes up by 1, how does y change?" % (n, his), "y goes up by 2",
                   ["y goes up by 1", "y goes down by 2", "y goes up by 3"],
                   "From %s to %s, x goes up 1 and y goes from %s to %s, up 2. Each point is 1 right and 2 up from the one before."
                   % (pair(-3, -3), pair(-2, -1), num(-3), num(-1)), rnd))
    # F: tide at a dock in Nanaimo
    xs, ys = [0, 1, 2, 3, 4], [3, 2, 1, 0, -1]
    T = tbl(("Hours (x)", "Water level, m (y)"), xs, ys, label="table of values: hours and water level")
    its.append(mcq(fig(T) + "At a dock in Nanaimo, the water level is measured from its average level. The tide goes out, "
                   "so the level drops 1 m each hour. Which ordered pair shows when the water is at its average level (0 m)?",
                   pair(3, 0), [pair(0, 3), pair(4, -1), pair(-3, 0)],
                   "The level is 0 m at hour 3, so x = 3 and y = 0: %s. (0, 3) is the start, when the water is 3 m above average." % pair(3, 0), rnd))
    G = Grid(6)
    for x, y in zip(xs, ys):
        G.point(x, y, None)
    its.append(mcq(fig(G.svg("graph of the water level: points (0, 3) to (4, −1)")) +
                   "This graph shows the tide table. Which statement is true?",
                   "The points go down from left to right",
                   ["The points go up from left to right", "The points are all in Quadrant I", "The points make a horizontal line"],
                   "As x goes up by 1, y goes down by 1, so each point is 1 right and 1 down from the one before. "
                   "The last point, %s, is in Quadrant IV." % pair(4, -1), rnd))
    pts, ans = pick_letters((4, -1), [(-1, 4), (4, 1), (1, -4)], pos)
    its.append(mcq_fixed(fig(pts_grid(pts, "coordinate grid with points A to D")) +
                         "The water level at the Nanaimo dock is 1 m below average after 4 hours. Which point shows this?",
                         ["A", "B", "C", "D"], ans,
                         "x = 4 hours and y = %s m (below average is negative). The point is %s: point %s." % (num(-1), pair(4, -1), ans)))
    # G: Whistler evening temperature
    xs, ys = [0, 1, 2, 3, 4], [6, 3, 0, -3, -6]
    T = tbl(("Hours after 6 p.m. (x)", "Temperature, °C (y)"), xs, ys, label="table of values: hours after 6 p.m. and temperature")
    its.append(mcq(fig(T) + "On a ski day in Whistler, the temperature falls 3 °C each hour after 6 p.m. "
                   "Which ordered pair shows the temperature at 10 p.m.?", pair(4, -6),
                   [pair(-6, 4), pair(4, 6), pair(10, -6)],
                   "10 p.m. is 4 hours after 6 p.m., so x = 4. The table gives y = %s. The ordered pair is %s." % (num(-6), pair(4, -6)), rnd))
    its.append(mcq_int("The Whistler temperature keeps falling 3 °C each hour. Graph the point for 11 p.m. (x = 5). "
                       "What is its y-coordinate?", -9, [-7, -3, 9],
                       "x = 4 has y = %s. One more hour: %s %s 3 = %s. (%s only subtracts 1; 9 drops the minus sign.)"
                       % (num(-6), num(-6), MINUS, num(-9), num(-7)), " °C"))
    # mistakes
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq("A table shows x = 1, 2, 3 and y = %s, %s, %s. %s graphs the points %s, %s and %s. What mistake did %s make?"
                   % (num(-2), num(-4), num(-6), n, pair(-2, 1), pair(-4, 2), pair(-6, 3), he),
                   "%s used y as the first coordinate" % H,
                   ["%s dropped the minus signs" % H, "%s plotted the wrong table" % H, "No mistake. %s is right" % H],
                   "The ordered pairs are (x, y): %s, %s and %s. %s wrote y first." % (pair(1, -2), pair(2, -4), pair(3, -6), n), rnd))
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq("From a table of night temperatures in Kamloops, %s must plot %s. %s plots it in Quadrant I. "
                   "What mistake did %s make?" % (n, pair(2, -3), H, he),
                   "%s dropped the minus sign" % H,
                   ["%s swapped x and y" % H, "%s numbered the quadrants clockwise" % H, "No mistake. %s is right" % H],
                   "y = %s means 3 down, so %s is right 2 and down 3: Quadrant IV. Ignoring the minus sign puts it at (2, 3) in Quadrant I."
                   % (num(-3), pair(2, -3)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Graph a table of values: BC word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    G = Grid(5, quads=True)
    G.arrow((0, 0), (-3, 0)).arrow((-3, 0), (-3, 4))
    G.note(-2, 0.5, "left 3").note(-2.8, 2, "up 4", anchor="start")
    G.point(-3, 4, "A", where=(1, 1))
    plot = G.svg("Cartesian plane: from the origin go left 3, then up 4 to point A at (−3, 4)")
    G = Grid(5)
    R = [(-3, 3), (4, 3), (4, -2), (-3, -2)]
    G.poly(R)
    for p, nm, w in zip(R, "ABCD", [(-1, 1), (1, 1), (1, -1), (-1, -1)]):
        G.point(p[0], p[1], nm, where=w)
    rect = G.svg("rectangle ABCD with A (−3, 3), B (4, 3), C (4, −2) and D (−3, −2)")
    G = Grid(5)
    for x in range(0, 5):
        G.point(x, 2 * x - 4, None)
    graph = G.svg("graph of the table: points (0, −4), (1, −2), (2, 0), (3, 2), (4, 4)")
    return (
        "<h2>The four quadrants</h2>"
        "<p>The Cartesian plane has two number lines. The <b>x-axis</b> goes across and the <b>y-axis</b> goes up and down. "
        "They cross at the <b>origin</b>, (0, 0), and cut the plane into four <b>quadrants</b>. "
        "The quadrants are numbered I, II, III, IV <b>counterclockwise</b>, starting at the top right.</p>"
        "<p>An ordered pair (x, y) always gives x first. The sign tells the direction. "
        "Positive x: right. Negative x: left. Positive y: up. Negative y: down.</p>"
        "<figure class='sn-fig'>" + plot +
        "<figcaption>To plot (−3, 4), start at the origin. Go left 3, then up 4. Point A is in Quadrant II.</figcaption></figure>" +
        table(["Quadrant", "Where", "Signs (x, y)", "Example"], [
            ["I", "top right", "(+, +)", "(4, 2)"],
            ["II", "top left", "(−, +)", "(−3, 4)"],
            ["III", "bottom left", "(−, −)", "(−5, −1)"],
            ["IV", "bottom right", "(+, −)", "(2, −6)"],
        ]) +
        "<p>A point on an axis, like (0, 5) or (−6, 0), is not in any quadrant.</p>" +
        ex("Example", "Which quadrant is (5, −4) in?", "x is positive (right) and y is negative (down). Right and down is the bottom right.",
           "Quadrant IV") +
        "<h2>Shapes on the plane</h2>"
        "<p>When a side runs along a grid line, only one coordinate changes. Its length is the larger value minus the smaller one. "
        "If the side crosses an axis, subtracting a negative number adds: 4 − (−3) = 7.</p>"
        "<figure class='sn-fig'>" + rect +
        "<figcaption>AB goes from x = −3 to x = 4: 4 − (−3) = 7 units. BC goes from y = 3 to y = −2: 3 − (−2) = 5 units.</figcaption></figure>" +
        ex("Example", "Find the perimeter and the area of rectangle ABCD above.",
           "Length 7 units, width 5 units. Perimeter = 7 + 5 + 7 + 5 = 24 units. Area = 7 × 5 = 35 square units.",
           "24 units and 35 square units") +
        ex("Missing vertex", "A rectangle has vertices (−3, 3), (4, 3) and (4, −2). Find the fourth vertex.",
           "The fourth vertex lines up with (−3, 3) and with (4, −2). Take x = −3 from the first and y = −2 from the second.",
           "(−3, −2)") +
        "<h2>Graph a table of values</h2>"
        "<p>Each column of a table of values is one ordered pair (x, y). Plot every pair. "
        "If y changes by the same amount each time x goes up by 1, the points lie on a straight line.</p>" +
        table(["x", "0", "1", "2", "3", "4"], [["y", "−4", "−2", "0", "2", "4"]]) +
        "<figure class='sn-fig'>" + graph +
        "<figcaption>The pairs (0, −4), (1, −2), (2, 0), (3, 2) and (4, 4). Each point is 1 right and 2 up from the one before.</figcaption></figure>" +
        ex("Example", "A diver starts at the surface and goes down 2 m each minute. Write the point for 3 minutes.",
           "x = 3 minutes. Below the surface is negative: y = −2 × 3 = −6.", "(3, −6), in Quadrant IV") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Swapping the numbers: plotting (−3, 4) at (4, −3)", "Move across first (x), then up or down (y)"],
            ["Dropping the minus sign", "Negative x means left; negative y means down"],
            ["Numbering the quadrants clockwise", "Go counterclockwise: I top right, II top left, III bottom left, IV bottom right"],
            ["Saying (0, 5) is in Quadrant I", "A point on an axis is not in any quadrant"],
            ["From −3 to 4 doing 4 − 3 = 1", "Subtract the negative: 4 − (−3) = 7"],
            ["Counting grid lines instead of spaces", "Count the jumps between lines; the starting line is 0"],
            ["Reading a table across the wrong row", "Each column is one pair: top number x, bottom number y"],
        ])
    )


FAQ = [
    {"q": "What do Grade 7 students learn about Cartesian coordinates in BC?",
     "a": "The BC Grade 7 math curriculum includes Cartesian coordinates and graphing. Students plot and read points in all four quadrants, work with shapes on the grid and graph ordered pairs, for example from a table of values."},
    {"q": "How are the four quadrants numbered?",
     "a": "Counterclockwise from the top right: Quadrant I (+, +), II (−, +), III (−, −) and IV (+, −). A point on an axis, like (0, 5), is not in any quadrant."},
    {"q": "How do you find the length of a side on a coordinate grid?",
     "a": "If the side runs along a grid line, subtract the coordinates that change: larger minus smaller. From (−3, 2) to (4, 2), the length is 4 − (−3) = 7 units."},
    {"q": "Are coordinates on the Grade 7 FSA?",
     "a": "The Grade 7 FSA numeracy questions draw on the math students learn in BC, so reading and plotting points and graphing tables of values is useful practice. These worksheets come with an answer key."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions. Choices with a fixed order
    stay as they are; the other questions fill the gaps."""
    for s in sets:
        cnt = [0] * 4
        free = []
        for it in s["items"]:
            if it.pop("fixed", False):
                cnt[it["a"]] += 1
            else:
                free.append(it)
        need = [max(0, 5 - c) for c in cnt]
        assert sum(need) == len(free), (s["title"], cnt)
        targets = [i for i in range(4) for _ in range(need[i])]
        rnd.shuffle(targets)
        for it, t in zip(free, targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t
        final = [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


def gen_unit():
    rnd = random.Random(37812)
    P = People(rnd)
    sets = [set_quadrants(rnd, P), set_read(rnd, P), set_plot(rnd, P), set_shapes(rnd, P), set_tables(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1, it["q"]
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
            plain = re.sub(r"<[^>]+>", "", it["q"]) + " ".join(it["c"]) + it["e"]
            assert not re.search(r"(?<![\w(|])-\d", plain), plain   # use the real minus sign
    return {
        "country": "ca-bc", "subject": "math", "grade": "grade-7", "slug": "cartesian-coordinates-and-graphing", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Cartesian Coordinates and Graphing: Four Quadrants, Shapes and Tables of Values",
        "seo_title": "Grade 7 Cartesian Coordinates and Graphing Worksheets: Free Math with Answer Key (BC Curriculum)",
        "short_title": "Cartesian coordinates and graphing",
        "domain": "Geometry and measurement",
        "standard_code": "Grade 7: Geometry and measurement",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/7/core",
        "standard_text": "Cartesian coordinates and graphing",
        "meta_desc": "Free Grade 7 math worksheets on Cartesian coordinates for the BC curriculum: name the four quadrants, read and plot points, find missing vertices and side lengths of shapes on the grid, and graph tables of values in BC word problems. 100 questions with an answer key, good FSA numeracy practice.",
        "key_big": "In (x, y), x tells you left or right and y tells you up or down. A minus sign means left or down.",
        "key_sub": "Quadrants I to IV go counterclockwise from the top right. A point on an axis is in no quadrant. A side along a grid line is larger minus smaller, so from −3 to 4 is 4 − (−3) = 7. Each column of a table of values is one point to plot.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (every grid) so their numbers stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "coordinate grid|graph of|table of values")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
