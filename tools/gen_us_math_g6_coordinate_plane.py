# -*- coding: utf-8 -*-
"""
US Grade 6 Math: The Coordinate Plane in Four Quadrants (6.NS.C.8, with 6.NS.C.6b and 6.G.A.3)
  python tools/gen_us_math_g6_coordinate_plane.py
HTML attributes use single quotes (no backslashes in the JSON).

All four quadrants, whole-number coordinates from -7 to 7. Negative numbers use the real minus sign.
Every grid is drawn exactly and is square: a point (x, y) sits x grid spaces right (left if x < 0)
of the origin and y grid spaces up (down if y < 0). The numbers on the axes, the quadrant names,
the notes, the dots and the letter labels never overlap (checked in Grid.render).
Wrong answers come from real mistakes: switching x and y, dropping a minus sign, numbering the
quadrants clockwise, reflecting across the wrong axis, subtracting absolute values when the points
are on opposite sides of an axis (4 - 3 = 1 instead of 4 + 3 = 7), adding them when the points are
on the same side, counting grid dots instead of spaces, giving a negative distance.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
GRID = "#c9d3cc"
QCOL = "#7a8a80"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
QUADS = ["Quadrant I", "Quadrant II", "Quadrant III", "Quadrant IV"]
AXES = ["the x-axis", "the y-axis", "both axes", "neither axis"]


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


def dist(a, b):
    assert a[0] == b[0] or a[1] == b[1]
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


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
    """Choices keep their order (A B C D, numbers from small to large, quadrant and axis words)."""
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
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
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

    def __init__(self, R, u=22, quads=False):
        assert 3 <= R <= 7
        self.R, self.u, self.quads = R, u, quads
        side = 2 * R * u
        self.ox = 24 + R * u
        self.oy = 34 + R * u
        self.W = self.H = int(math.ceil(24 + side + 34))
        self.pts, self.segs, self.arrows, self.notes = [], [], [], []

    def P(self, x, y):
        return (self.ox + x * self.u, self.oy - y * self.u)

    def point(self, x, y, name, col=GREEN, where=None):
        assert x == int(x) and y == int(y) and abs(x) <= self.R and abs(y) <= self.R, (x, y)
        assert all((p[0], p[1]) != (x, y) for p in self.pts), ("two points at the same spot", x, y)
        self.pts.append((x, y, name, col, where))
        return self

    def seg(self, a, b, col=GREEN, w=3, dash=False):
        assert a[0] == b[0] or a[1] == b[1], "only grid-line segments"
        self.segs.append((a, b, col, w, dash))
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


def grid_for(pts, quads=False, lo=4):
    R = max(lo, max(max(abs(p[0]), abs(p[1])) for p in pts) + 1)
    return Grid(min(R, 7), quads=quads)


def pts_grid(pts, label="coordinate grid", ref=None, quads=False):
    """pts: (x, y, name). ref: name of a point drawn in red (the starting point)."""
    G = grid_for(pts, quads)
    for x, y, n in pts:
        G.point(x, y, n, RED if n == ref else GREEN)
    return G.svg(label)


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


# ------------------------------------------------------------ set 1: read and plot points
def set_read(rnd, P):
    its = []
    pos = Pos(rnd)
    reads = [
        [(-3, 4, "A")], [(5, -2, "B")], [(-4, -5, "C"), (-5, -4, "D")], [(2, -6, "E")],
        [(3, -5, "G"), (-5, 3, "H")], [(-6, 2, "K")], [(0, -4, "M"), (3, 2, "N")], [(-5, 0, "R")],
    ]
    for pts in reads:
        x, y, n = pts[0]
        e = "%s. Point %s is at %s. The x-coordinate comes first; a minus sign means left or down." % (walk(x, y), n, pair(x, y))
        if (y, x) in [(p[0], p[1]) for p in pts[1:]]:
            e += " %s is point %s: the numbers are switched." % (pair(y, x), pts[1][2])
        its.append(mcq(fig(pts_grid(pts, "coordinate grid with labeled points")) +
                       "What are the coordinates of point %s?" % n, pair(x, y), read_cands(x, y), e, rnd))
    its.append(mcq_int(fig(pts_grid([(-4, 2, "P")], "coordinate grid with labeled points")) +
                       "What is the x-coordinate of point P?", -4, [4, 2, -2],
                       "Point P is 4 units to the left of the origin, so x = " + num(-4) + ". Left means negative. (2 is its y-coordinate.)"))
    its.append(mcq_int(fig(pts_grid([(3, -6, "Q")], "coordinate grid with labeled points")) +
                       "What is the y-coordinate of point Q?", -6, [6, 3, -3],
                       "Point Q is 6 units below the x-axis, so y = " + num(-6) + ". Down means negative. (3 is its x-coordinate.)"))
    for (x, y), others in [
        ((-3, 4), [(4, -3), (3, 4), (-3, -4)]),
        ((2, -5), [(-5, 2), (-2, -5), (2, 5)]),
        ((-4, -2), [(-2, -4), (4, -2), (-4, 2)]),
        ((-5, 3), [(3, -5), (5, 3), (-5, -3)]),
        ((0, -3), [(-3, 0), (0, 3), (3, -3)]),
        ((-2, 5), [(5, -2), (2, 5), (-2, -5)]),
    ]:
        pts, ans = pick_letters((x, y), others, pos)
        where = {(p[0], p[1]): p[2] for p in pts}
        e = "%s: that is point %s." % (walk(x, y), ans)
        if (y, x) in where:
            e += " Point %s is at %s: the numbers are switched." % (where[(y, x)], pair(y, x))
        elif (-x, y) in where and x != 0:
            e += " Point %s is at %s: the sign of x is wrong." % (where[(-x, y)], pair(-x, y))
        its.append(mcq_fixed(fig(pts_grid(pts, "coordinate grid with points A to D")) +
                             "Which point is at %s?" % pair(x, y), ["A", "B", "C", "D"], ans, e))
    its.append(mcq("To plot %s, what do you do first from the origin?" % pair(-5, 2), "Go left 5",
                   ["Go right 5", "Go down 5", "Go left 2"],
                   "The first number, " + num(-5) + ", is the x-coordinate. It is negative, so go left 5. Then go up 2.", rnd))
    its.append(mcq("What does a negative y-coordinate tell you to do?", "Go down", ["Go up", "Go left", "Go right"],
                   "The y-coordinate tells you how far to move up or down. Positive means up, and negative means down.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s starts at the origin. %s goes left 4, then down 3. Which ordered pair names %s point?" % (n, he.capitalize(), his),
                   pair(-4, -3), [pair(-3, -4), pair(4, 3), pair(4, -3)],
                   "Left 4 gives x = %s. Down 3 gives y = %s. Write x first: %s." % (num(-4), num(-3), pair(-4, -3)), rnd))
    its.append(mcq("A point is 6 units to the right of the y-axis and 2 units below the x-axis. What are its coordinates?",
                   pair(6, -2), [pair(-2, 6), pair(6, 2), pair(-6, -2)],
                   "Right of the y-axis means x is positive: x = 6. Below the x-axis means y is negative: y = %s. The point is %s."
                   % (num(-2), pair(6, -2)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Read and plot points in all four quadrants", "items": its}


# ------------------------------------------------------------ set 2: quadrants and signs
SIGN_WORD = {1: "positive", -1: "negative"}


def quad_e(x, y):
    sx = "positive (right)" if x > 0 else "negative (left)"
    sy = "positive (up)" if y > 0 else "negative (down)"
    return "x is %s and y is %s, so %s is in %s. The quadrants are numbered counterclockwise, starting at the top right." % (
        sx, sy, pair(x, y), quad(x, y))


def set_quadrants(rnd, P):
    its = []
    pos = Pos(rnd)
    for x, y in [(-2, -5), (4, -7), (-3, 8), (6, 1), (-9, -1), (1, -4), (-7, 2), (5, 5)]:
        its.append(mcq_fixed("Which quadrant is the point %s in?" % pair(x, y), QUADS, quad(x, y), quad_e(x, y)))
    its.append(mcq_fixed("Where is the point %s?" % pair(0, -4), ["Quadrant III", "Quadrant IV", "on the x-axis", "on the y-axis"],
                         "on the y-axis",
                         "x = 0, so the point does not move left or right. It goes down 4 along the y-axis. A point on an axis is not in any quadrant."))
    its.append(mcq_fixed("Where is the point %s?" % pair(-6, 0), ["Quadrant II", "Quadrant III", "on the x-axis", "on the y-axis"],
                         "on the x-axis",
                         "y = 0, so the point does not move up or down. It goes left 6 along the x-axis. It is not in any quadrant."))
    its.append(mcq_fixed("Where is the point (0, 0)?", ["Quadrant I", "the origin", "on the x-axis only", "on the y-axis only"],
                         "the origin", "(0, 0) is the origin, where the two axes cross. It is on both axes and in no quadrant."))
    its.append(mcq_fixed("In which quadrant are both coordinates negative?", QUADS, "Quadrant III",
                         "Negative x means left and negative y means down. Left and down is the bottom-left part: Quadrant III."))
    its.append(mcq_fixed("A point has a positive x-coordinate and a negative y-coordinate. Which quadrant is it in?", QUADS, "Quadrant IV",
                         "Positive x means right and negative y means down. Right and down is the bottom-right part: Quadrant IV."))
    its.append(mcq("What are the signs of the coordinates of a point in Quadrant II?", "(" + MINUS + ", +)",
                   ["(+, " + MINUS + ")", "(" + MINUS + ", " + MINUS + ")", "(+, +)"],
                   "Quadrant II is the top-left part. Left means x is negative and up means y is positive: (" + MINUS + ", +).", rnd))
    its.append(mcq("The point (a, b) is in Quadrant IV. Which is true?", "a &gt; 0 and b &lt; 0",
                   ["a &lt; 0 and b &gt; 0", "a &lt; 0 and b &lt; 0", "a &gt; 0 and b &gt; 0"],
                   "Quadrant IV is the bottom-right part: x is positive (a &gt; 0) and y is negative (b &lt; 0).", rnd))
    its.append(mcq("Which point is in Quadrant II?", pair(-5, 7), [pair(5, -7), pair(-5, -7), pair(5, 7)],
                   "Quadrant II is the top-left part: x negative, y positive. %s is left 5 and up 7. (%s is in Quadrant IV: "
                   "that is where Quadrant II would be if you counted clockwise.)" % (pair(-5, 7), pair(5, -7)), rnd))
    for target, others, qn in [
        ((-3, -4), [(3, 4), (4, -2), (-4, 3)], "Quadrant III"),
        ((5, -3), [(-3, 5), (2, 4), (-4, -2)], "Quadrant IV"),
    ]:
        pts, ans = pick_letters(target, others, pos)
        where = {(p[0], p[1]): p[2] for p in pts}
        e = "Point %s is at %s. %s" % (ans, pair(*target), quad_e(*target))
        if qn == "Quadrant IV":
            e += " Point %s is in Quadrant II: counting clockwise by mistake would call it IV." % where[(-3, 5)]
        its.append(mcq_fixed(fig(pts_grid(pts, "coordinate grid with points A to D")) +
                             "Which point is in %s?" % qn, ["A", "B", "C", "D"], ans, e))
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq("%s says %s is in Quadrant IV. What mistake did %s make?" % (n, pair(-3, 5), he),
                   "%s numbered the quadrants clockwise" % H,
                   ["%s switched x and y" % H, "%s ignored the minus sign" % H, "No mistake. %s is right" % H],
                   "%s is left and up: Quadrant II. The quadrants go counterclockwise: I top right, II top left, III bottom left, IV bottom right." % pair(-3, 5), rnd))
    n, he, his = P.next()
    its.append(mcq("%s says %s is in Quadrant IV. Is %s right?" % (n, pair(0, -4), he),
                   "No, it is on the y-axis, not in a quadrant",
                   ["Yes, y is negative", "No, it is in Quadrant III", "No, it is on the x-axis"],
                   "x = 0, so the point sits on the y-axis, 4 units below the origin. Points on an axis are not in any quadrant.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Quadrants and signs of coordinates", "items": its}


# ------------------------------------------------------------ set 3: reflections across the axes
def reflect(p, axis):
    return (p[0], -p[1]) if axis == "x" else (-p[0], p[1])


def refl_e(p, axis):
    r = reflect(p, axis)
    if r == p:
        return ("%s is on the %s-axis, the mirror line itself, so its reflection is the same point: %s."
                % (pair(*p), axis, pair(*r)))
    if axis == "x":
        return ("Across the x-axis, the point flips up and down: x stays %s and y changes sign, %s → %s. The image is %s."
                % (num(p[0]), num(p[1]), num(-p[1]), pair(*r)))
    return ("Across the y-axis, the point flips left and right: y stays %s and x changes sign, %s → %s. The image is %s."
            % (num(p[1]), num(p[0]), num(-p[0]), pair(*r)))


def set_reflect(rnd, P):
    its = []
    pos = Pos(rnd)
    for p, axis in [((3, -2), "y"), ((-4, 5), "x"), ((6, 1), "y"), ((-2, -7), "x"), ((5, 4), "x"), ((-8, -3), "y")]:
        r = reflect(p, axis)
        other = reflect(p, "y" if axis == "x" else "x")
        both = (-p[0], -p[1])
        its.append(mcq("Reflect %s across the %s-axis. What are the coordinates of the image?" % (pair(*p), axis),
                       pair(*r), [pair(*other), pair(*both), pair(r[1], r[0])], refl_e(p, axis), rnd))
    its.append(mcq("Reflect %s across the y-axis. What are the coordinates of the image?" % pair(0, 6), pair(0, 6),
                   [pair(0, -6), pair(6, 0), pair(-6, 0)], refl_e((0, 6), "y"), rnd))
    its.append(mcq("Reflect %s across the x-axis. What are the coordinates of the image?" % pair(-5, 0), pair(-5, 0),
                   [pair(5, 0), pair(0, -5), pair(0, 5)], refl_e((-5, 0), "x"), rnd))
    for p, axis, extra in [((-3, 2), "x", (-3, 0)), ((4, -3), "y", (0, -3)), ((-2, -4), "x", (-2, 0)), ((5, 2), "y", (2, 5))]:
        r = reflect(p, axis)
        others = [reflect(p, "y" if axis == "x" else "x"), (-p[0], -p[1]), extra]
        pts, ans = pick_letters(r, others, pos)
        where = {(q[0], q[1]): q[2] for q in pts}
        G = grid_for([p] + [q[:2] for q in pts])
        G.point(p[0], p[1], "P", RED)
        for q in pts:
            G.point(*q)
        wa = where[others[0]]
        e = "P is at %s. %s That is point %s. Point %s is the reflection across the %s-axis instead." % (
            pair(*p), refl_e(p, axis), ans, wa, "y" if axis == "x" else "x")
        its.append(mcq_fixed(fig(G.svg("coordinate grid with point P and points A to D")) +
                             "Which point is the reflection of point P across the %s-axis?" % axis, ["A", "B", "C", "D"], ans, e))
    its.append(mcq_fixed("The points %s and %s are reflections of each other across which axis?" % (pair(4, 1), pair(-4, 1)), AXES,
                         "the y-axis", "Only the x-coordinate changes sign (4 → %s), so the points flip left and right. The mirror line is the y-axis." % num(-4)))
    its.append(mcq_fixed("The points %s and %s are reflections of each other across which axis?" % (pair(-3, 5), pair(-3, -5)), AXES,
                         "the x-axis", "Only the y-coordinate changes sign (5 → %s), so the points flip up and down. The mirror line is the x-axis." % num(-5)))
    its.append(mcq_fixed("%s is reflected across one axis and then the other. Which point does it land on?" % pair(2, -6),
                         [pair(-2, -6), pair(2, 6), pair(-2, 6), pair(-6, 2)], pair(-2, 6),
                         "Across the x-axis: %s → %s. Then across the y-axis: %s → %s. Both signs change." % (
                             pair(2, -6), pair(2, 6), pair(2, 6), pair(-2, 6))))
    its.append(mcq_fixed("Are %s and %s reflections of each other across an axis?" % (pair(3, 4), pair(4, 3)),
                         ["Yes, across the x-axis", "Yes, across the y-axis", "Yes, across both axes", "No, neither axis"],
                         "No, neither axis",
                         "A reflection across an axis keeps the same numbers and changes a sign. Here the numbers are switched, and no sign changes."))
    its.append(mcq("When you reflect a point across the x-axis, what changes?", "the sign of the y-coordinate",
                   ["the sign of the x-coordinate", "the signs of both coordinates", "the order of the numbers"],
                   "The x-axis is a mirror lying across. The point flips up or down, so only y changes sign. Example: %s → %s."
                   % (pair(2, 3), pair(2, -3)), rnd))
    its.append(mcq("Point (a, b) is reflected across the y-axis. Which ordered pair names the image?", "(" + MINUS + "a, b)",
                   ["(a, " + MINUS + "b)", "(" + MINUS + "a, " + MINUS + "b)", "(b, a)"],
                   "The y-axis is a mirror standing up and down. The point flips left or right, so only x changes sign: (" + MINUS + "a, b).", rnd))
    its.append(mcq_fixed("Point %s is reflected across the y-axis. Which quadrant is the image in?" % pair(-6, 2), QUADS, "Quadrant I",
                         "The image is %s. Both coordinates are positive, so it is in Quadrant I." % pair(6, 2)))
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq("%s reflects %s across the x-axis and gets %s. What mistake did %s make?" % (n, pair(2, 5), pair(-2, 5), he),
                   "%s reflected across the y-axis" % H,
                   ["%s switched x and y" % H, "%s changed both signs" % H, "No mistake. %s is right" % H],
                   "%s changed the sign of x, which is a reflection across the y-axis. Across the x-axis, y changes sign: %s." % (H, pair(2, -5)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Reflections across the x-axis and y-axis", "items": its}


# ------------------------------------------------------------ set 4: distance with absolute value
def dist_e(a, b):
    """Explanation for the distance between two points on the same grid line."""
    if a[0] == b[0]:
        k, v, w, ax, line = "x", a[1], b[1], "x-axis", "up-and-down"
    else:
        k, v, w, ax, line = "y", a[0], b[0], "y-axis", "across"
    d = abs(v - w)
    same = "Both points have %s = %s, so they are on the same %s line. " % (k, num(a[0] if k == "x" else a[1]), line)
    if v == 0 or w == 0:
        t = v if w == 0 else w
        return same + "One point is on the %s, so the distance is |%s| = %d units." % (ax, num(t), d), d
    if (v > 0) != (w > 0):
        return same + ("They are on opposite sides of the %s, so add the absolute values: |%s| + |%s| = %d + %d = %d units."
                       % (ax, num(v), num(w), abs(v), abs(w), d)), d
    hi, lo = max(abs(v), abs(w)), min(abs(v), abs(w))
    big, small = (v, w) if abs(v) > abs(w) else (w, v)
    return same + ("They are on the same side of the %s, so subtract the absolute values: |%s| − |%s| = %d − %d = %d units."
                   % (ax, num(big), num(small), hi, lo, d)), d


def set_distance(rnd, P):
    its = []
    for a, b, na, nb, wrong in [
        ((2, -4), (2, 3), "A", "B", [1, -1, -7]),
        ((-5, 2), (3, 2), "C", "D", [2, 9, -8]),
        ((-3, -1), (-3, -6), "E", "F", [7, 6, -5]),
        ((-6, 4), (-2, 4), "G", "H", [8, 5, 6]),
        ((4, -5), (4, 1), "J", "K", [4, 7, -6]),
        ((-4, -2), (3, -2), "M", "N", [1, -1, 4]),
    ]:
        e, d = dist_e(a, b)
        G = grid_for([a, b])
        G.seg(a, b)
        G.point(a[0], a[1], na).point(b[0], b[1], nb)
        its.append(mcq_int(fig(G.svg("coordinate grid with a line segment")) +
                           "How many units long is line segment %s%s?" % (na, nb), d, wrong, e))
    for a, b, wrong in [
        ((-3, 5), (6, 5), [3, -3, -9]),
        ((1, -8), (1, -2), [10, 7, 8]),
        ((-7, -4), (-2, -4), [9, 6, 7]),
        ((0, -6), (0, 5), [1, -1, -11]),
        ((-6, 2), (6, 2), [0, 13, 6]),
        ((5, -2), (5, -7), [9, 6, 7]),
    ]:
        e, d = dist_e(a, b)
        its.append(mcq_int("What is the distance between %s and %s?" % (pair(*a), pair(*b)), d, wrong, e, " units"))
    its.append(mcq_int("How far is the point %s from the y-axis?" % pair(-7, 3), 7, [3, -7, 10],
                       "The distance from the y-axis is how far left or right the point is: |%s| = 7 units. A distance is never negative." % num(-7),
                       " units"))
    its.append(mcq_int("How far is the point %s from the x-axis?" % pair(4, -5), 5, [4, -5, 1],
                       "The distance from the x-axis is how far up or down the point is: |%s| = 5 units." % num(-5), " units"))
    n, he, his = P.next()
    its.append(mcq("%s finds the distance from %s to %s by doing 4 − 3 = 1. What should %s do?" % (n, pair(-4, 2), pair(3, 2), he),
                   "Add: 4 + 3 = 7",
                   ["Subtract: 3 − 4 = " + num(-1), "Count the dots: 8", "Nothing. 1 unit is right"],
                   "The points are on opposite sides of the y-axis: 4 units left and 3 units right. Add the absolute values: 4 + 3 = 7 units.", rnd))
    its.append(mcq("Which shows how to find the distance from %s to %s?" % (pair(5, -3), pair(5, 6)),
                   "|" + num(-3) + "| + |6| = 9", ["|6| − |" + num(-3) + "| = 3", "5 + 6 = 11", "6 − 5 = 1"],
                   "Same x, so look at the y-coordinates, " + num(-3) + " and 6. They are on opposite sides of the x-axis, so add: 3 + 6 = 9 units.", rnd))
    its.append(mcq("Point A is at %s. Point B is 5 units below A. What are the coordinates of B?" % pair(-2, 3), pair(-2, -2),
                   [pair(-2, 8), pair(-7, 3), pair(-2, -5)],
                   "Below means y gets smaller: 3 − 5 = %s. x stays %s. B is at %s." % (num(-2), num(-2), pair(-2, -2)), rnd))
    its.append(mcq("Point C is at %s. Point D is 6 units to the left of C. What are the coordinates of D?" % pair(4, -1), pair(-2, -1),
                   [pair(10, -1), pair(4, -7), pair(-6, -1)],
                   "Left means x gets smaller: 4 − 6 = %s. y stays %s. D is at %s." % (num(-2), num(-1), pair(-2, -1)), rnd))
    its.append(mcq_int("Point E is at %s. Point F is 9 units straight above E. What is the y-coordinate of F?" % pair(3, -4), 5,
                       [9, 13, -13],
                       "Above means y gets bigger: %s + 9 = 5. F is at %s. Check: 4 units up to the x-axis, then 5 more: 4 + 5 = 9."
                       % (num(-4), pair(3, 5))))
    its.append(mcq("Which point is 6 units from %s?" % pair(-2, 1), pair(4, 1),
                   [pair(6, 1), pair(-2, 6), pair(-4, 1)],
                   "%s and %s have the same y. They are on opposite sides of the y-axis: 2 + 4 = 6 units. (%s is 8 units away and %s is only 2.)"
                   % (pair(-2, 1), pair(4, 1), pair(6, 1), pair(-4, 1)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Distance between points using absolute value", "items": its}


# ------------------------------------------------------------ set 5: polygons and real-world problems
def town_grid():
    G = Grid(6)
    for x, y, n in [(-4, 3, "L"), (3, 3, "S"), (3, -5, "P"), (-4, -2, "M")]:
        G.point(x, y, n)
    return fig(G.svg("coordinate grid map of a town"))


def set_real(rnd, P):
    its = []
    for A, B, C, D, wrong in [
        ((-4, 3), (2, 3), (2, -2), (-4, -2), [(4, -2), (-2, -4), (-4, 2)]),
        ((-3, -4), (-3, 2), (5, 2), (5, -4), [(-4, 5), (5, 4), (-5, -4)]),
        ((2, 2), (-3, 2), (-3, -3), (2, -3), [(-3, 2), (-2, -3), (3, -2)]),
    ]:
        G = grid_for([A, B, C, D])
        G.seg(A, B).seg(B, C)
        G.point(A[0], A[1], "A").point(B[0], B[1], "B").point(C[0], C[1], "C")
        same_x = "A" if D[0] == A[0] else "C"
        same_y = "C" if same_x == "A" else "A"
        kind = "square" if dist(A, B) == dist(B, C) else "rectangle"
        e = ("D is in line with %s up and down, so x = %s. It is in line with %s across, so y = %s. D is at %s."
             % (same_x, num(D[0]), same_y, num(D[1]), pair(*D)))
        its.append(mcq(fig(G.svg("coordinate grid with three vertices of a " + kind)) +
                       "A, B and C are 3 vertices of a %s. What are the coordinates of the 4th vertex, D?" % kind,
                       pair(*D), [pair(*w) for w in wrong if w != D], e, rnd))
    its.append(mcq("A rectangle has vertices at %s, %s and %s. What is the 4th vertex?" % (pair(-2, 5), pair(4, 5), pair(4, -3)),
                   pair(-2, -3), [pair(-3, -2), pair(2, -3), pair(-2, 3)],
                   "The 4th vertex is below %s, so x = %s, and across from %s, so y = %s: %s." % (
                       pair(-2, 5), num(-2), pair(4, -3), num(-3), pair(-2, -3)), rnd))
    its.append(mcq_int("A rectangle has vertices at %s, %s, %s and %s. What is its perimeter?" % (pair(-3, 2), pair(4, 2), pair(4, -1), pair(-3, -1)),
                       20, [8, 10, 21],
                       "Length: from x = %s to x = 4 is 3 + 4 = 7 units. Width: from y = %s to y = 2 is 1 + 2 = 3 units. "
                       "Perimeter = 7 + 3 + 7 + 3 = 20 units." % (num(-3), num(-1)), " units"))
    its.append(mcq_int("A rectangle has vertices at %s, %s, %s and %s. What is its area?" % (pair(-5, 3), pair(2, 3), pair(2, -2), pair(-5, -2)),
                       35, [3, 12, 24],
                       "Length: 5 + 2 = 7 units (opposite sides of the y-axis). Width: 3 + 2 = 5 units (opposite sides of the x-axis). "
                       "Area = 7 × 5 = 35 square units.", " square units"))
    its.append(mcq_int("A triangle has vertices at %s, %s and %s. How long is the side from %s to %s?" % (
        pair(-6, -3), pair(-2, -3), pair(-2, 4), pair(-6, -3), pair(-2, -3)), 4, [8, 5, 6],
        "Both points have y = %s. Both x-coordinates are negative, so the points are on the same side of the y-axis: "
        "|%s| − |%s| = 6 − 2 = 4 units." % (num(-3), num(-6), num(-2)), " units"))
    its.append(mcq_int("A square has vertices at %s, %s, %s and %s. What is its perimeter?" % (pair(-3, -3), pair(3, -3), pair(3, 3), pair(-3, 3)),
                       24, [0, 28, 36],
                       "Each side goes from %s to 3: 3 + 3 = 6 units. Perimeter = 4 × 6 = 24 units. (3 − 3 = 0 comes from subtracting instead of adding.)" % num(-3),
                       " units"))
    town = town_grid()
    n, he, his = P.next()
    key = ("The map shows %s’s town. The town hall is at the origin. L = library, S = school, P = park, M = market. "
           "Each unit is 1 block. " % n)
    its.append(mcq(town + key + "What are the coordinates of the park?", pair(3, -5), [pair(-5, 3), pair(3, 5), pair(-3, -5)],
                   "Start at the town hall (the origin), go right 3, then down 5. The park is at %s." % pair(3, -5), rnd))
    its.append(mcq_int(town + key + "How many blocks is it from the library straight across to the school?", 7, [1, 8, 6],
                       "The library is at %s and the school is at %s. Same y, opposite sides of the y-axis: 4 + 3 = 7 blocks."
                       % (pair(-4, 3), pair(3, 3)), " blocks"))
    its.append(mcq_int(town + key + "%s walks from the school straight down to the park. How many blocks does %s walk?" % (n, he), 8,
                       [2, -2, 5],
                       "The school is at %s and the park is at %s. Same x, opposite sides of the x-axis: 3 + 5 = 8 blocks."
                       % (pair(3, 3), pair(3, -5)), " blocks"))
    its.append(mcq_int(town + key + "What is the shortest walk from the market to the school along the streets (the grid lines)?", 12,
                       [2, 5, 7],
                       "The market is at %s and the school is at %s. Across: 4 + 3 = 7 blocks. Up: 2 + 3 = 5 blocks. 7 + 5 = 12 blocks."
                       % (pair(-4, -2), pair(3, 3)), " blocks"))
    its.append(mcq(town + key + "Which place is in Quadrant II?", "the library", ["the school", "the park", "the market"],
                   "Quadrant II is the top-left part (x negative, y positive). The library is at %s." % pair(-4, 3), rnd))
    its.append(mcq("On a treasure map, east is the positive x-direction and north is the positive y-direction. "
                   "The treasure is 3 units west and 5 units south of the origin. Where is it?", pair(-3, -5),
                   [pair(3, 5), pair(-5, -3), pair(3, -5)],
                   "West is left, so x = %s. South is down, so y = %s. The treasure is at %s." % (num(-3), num(-5), pair(-3, -5)), rnd))
    its.append(mcq("A boat is at %s on a map. It sails 8 units east (in the positive x-direction). Where is it now?" % pair(-6, 2),
                   pair(2, 2), [pair(-14, 2), pair(-6, 10), pair(8, 2)],
                   "East changes only x: %s + 8 = 2. y stays 2. The boat is at %s." % (num(-6), pair(2, 2)), rnd))
    n, he, his = P.next()
    its.append(mcq_int("On a city map, %s’s house is at %s and the pool is at %s. Each unit is 1 block. How many blocks apart are they?"
                       % (n, pair(-5, -2), pair(-5, 4)), 6, [2, 7, 9],
                       "Same x, so look at y: %s and 4 are on opposite sides of the x-axis. 2 + 4 = 6 blocks." % num(-2), " blocks"))
    its.append(mcq_int("A garden is a rectangle with corners at %s, %s, %s and %s. Each unit is 1 meter. How many meters of fence go around it?"
                       % (pair(-6, 1), pair(2, 1), pair(2, -4), pair(-6, -4)), 26, [14, 13, 40],
                       "Length: 6 + 2 = 8 m. Width: 1 + 4 = 5 m. Perimeter = 8 + 5 + 8 + 5 = 26 m.", " m"))
    its.append(mcq_int("On a map where each unit is 10 meters, a drone flies straight from %s to %s. How many meters does it fly?"
                       % (pair(4, -3), pair(4, 5)), 80, [8, 20, 90],
                       "Same x. %s and 5 are on opposite sides of the x-axis: 3 + 5 = 8 units. 8 × 10 = 80 meters." % num(-3), " m"))
    n, he, his = P.next()
    its.append(mcq_int("%s walks from %s to %s, then from %s to %s. Each unit is 1 block. How many blocks does %s walk in all?"
                       % (n, pair(-3, 4), pair(5, 4), pair(5, 4), pair(5, -2), he), 14, [4, 8, 6],
                       "First part: 3 + 5 = 8 blocks. Second part: 4 + 2 = 6 blocks. In all: 8 + 6 = 14 blocks.", " blocks"))
    its.append(mcq_int("The museum is at %s on a map. The zoo is at the reflection of the museum across the x-axis. "
                       "Each unit is 1 block. How many blocks apart are they?" % pair(-2, 6), 12, [0, 6, 13],
                       "The zoo is at %s. Same x: 6 + 6 = 12 blocks. A point and its reflection are the same distance from the mirror line."
                       % pair(-2, -6), " blocks"))
    assert len(its) == 20, len(its)
    return {"title": "Polygons and real-world problems", "items": its}


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
    plot = G.svg("four-quadrant grid: from the origin go left 3, then up 4 to point A at (−3, 4)")
    G = Grid(5)
    G.seg((3, 2), (-3, 2), RED, 2, dash=True).seg((3, 2), (3, -2), RED, 2, dash=True)
    G.point(3, 2, "P", RED).point(-3, 2, "Q").point(3, -2, "R")
    refl = G.svg("point P (3, 2), its reflection Q (−3, 2) across the y-axis and R (3, −2) across the x-axis")
    G = Grid(5)
    G.seg((-4, 2), (3, 2)).point(-4, 2, "A").point(3, 2, "B")
    G.note(-2, 2.5, "4").note(1.5, 2.5, "3")
    distf = G.svg("line segment from A (−4, 2) to B (3, 2): 4 units to the y-axis plus 3 units = 7 units")
    return (
        "<h2>Four quadrants</h2>"
        "<p>The x-axis and the y-axis are number lines with negative numbers too. They cross at the <b>origin</b>, (0, 0), "
        "and cut the plane into four <b>quadrants</b>. The quadrants are numbered I, II, III, IV <b>counterclockwise</b>, "
        "starting at the top right.</p>"
        "<p>In an ordered pair (x, y), the sign tells the direction. Positive x: right. Negative x: left. "
        "Positive y: up. Negative y: down.</p>"
        "<figure class='sn-fig'>" + plot +
        "<figcaption>To plot (−3, 4), start at the origin. Go left 3, then up 4. Point A is in Quadrant II.</figcaption></figure>" +
        table(["Quadrant", "Where", "Signs (x, y)", "Example"], [
            ["I", "top right", "(+, +)", "(2, 5)"],
            ["II", "top left", "(−, +)", "(−3, 4)"],
            ["III", "bottom left", "(−, −)", "(−6, −1)"],
            ["IV", "bottom right", "(+, −)", "(4, −2)"],
        ]) +
        "<p>A point on an axis, like (0, −4) or (5, 0), is not in any quadrant.</p>" +
        ex("Example", "Which quadrant is (−2, −5) in?", "x is negative (left) and y is negative (down). Left and down is the bottom left.",
           "Quadrant III") +
        "<h2>Reflections across the axes</h2>"
        "<p>An axis works like a mirror. Reflecting across the <b>x-axis</b> changes the sign of <b>y</b>. "
        "Reflecting across the <b>y-axis</b> changes the sign of <b>x</b>.</p>"
        "<figure class='sn-fig'>" + refl +
        "<figcaption>P (3, 2) reflected across the y-axis is Q (−3, 2). Reflected across the x-axis, it is R (3, −2).</figcaption></figure>" +
        ex("Example", "Reflect (−4, 5) across the x-axis.", "The x-axis is the mirror, so the point flips down. x stays −4. y changes sign: 5 → −5.",
           "(−4, −5)") +
        "<h2>Distance with absolute value</h2>"
        "<p>When two points have the same x-coordinate (or the same y-coordinate), use the absolute values of the other coordinates. "
        "Absolute value is the distance from 0, so |−4| = 4.</p>"
        "<ul><li><b>Opposite sides</b> of the axis (signs are different): <b>add</b> the absolute values.</li>"
        "<li><b>Same side</b> (signs are the same): <b>subtract</b> the absolute values.</li></ul>"
        "<figure class='sn-fig'>" + distf +
        "<figcaption>A (−4, 2) and B (3, 2) are on opposite sides of the y-axis. |−4| + |3| = 4 + 3 = 7 units.</figcaption></figure>" +
        ex("Example", "How far is it from (−5, 2) to (−1, 2)?",
           "Same y. Both x-coordinates are negative, so the points are on the same side: |−5| − |−1| = 5 − 1 = 4.", "4 units") +
        ex("Example", "A rectangle has vertices (−3, 2), (4, 2), (4, −1) and (−3, −1). Find its perimeter.",
           "Length: 3 + 4 = 7 units. Width: 2 + 1 = 3 units. Perimeter = 7 + 3 + 7 + 3.", "20 units") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Switching the numbers: plotting (−3, 4) at (4, −3)", "Move across first (x), then up or down (y)"],
            ["Dropping the minus sign", "Negative x means left; negative y means down"],
            ["Numbering the quadrants clockwise", "Go counterclockwise: I top right, II top left, III bottom left, IV bottom right"],
            ["Reflecting across the wrong axis", "Across the x-axis, y changes sign. Across the y-axis, x changes sign"],
            ["Finding the distance from (−4, 2) to (3, 2) as 4 − 3 = 1", "Opposite sides of the axis: add, 4 + 3 = 7"],
            ["Counting grid dots instead of spaces", "Count the spaces, or use absolute values"],
        ])
    )


FAQ = [
    {"q": "What are the four quadrants of the coordinate plane?",
     "a": "The x-axis and y-axis split the plane into four parts, numbered counterclockwise: Quadrant I (top right, +, +), II (top left, −, +), III (bottom left, −, −) and IV (bottom right, +, −)."},
    {"q": "Is a point on an axis in a quadrant?",
     "a": "No. A point with a 0 coordinate, like (0, −4) or (6, 0), lies on an axis and is not in any quadrant."},
    {"q": "How do you find the distance between two points with the same x-coordinate?",
     "a": "Look at the y-coordinates. If their signs are different, add their absolute values; if the signs are the same, subtract them. For (2, −4) and (2, 3), the distance is 4 + 3 = 7 units."},
    {"q": "What happens to the coordinates when you reflect a point across the x-axis?",
     "a": "The x-coordinate stays the same and the y-coordinate changes sign, so (2, 5) becomes (2, −5). Across the y-axis, the x-coordinate changes sign instead."},
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
        while sum(need) > len(free):
            need[need.index(max(need))] -= 1
        while sum(need) < len(free):
            i = min(range(4), key=lambda j: cnt[j] + need[j])
            need[i] += 1
        targets = [i for i in range(4) for _ in range(need[i])]
        rnd.shuffle(targets)
        for it, t in zip(free, targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t
        final = [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


def gen_unit():
    rnd = random.Random(614)
    P = People(rnd)
    sets = [set_read(rnd, P), set_quadrants(rnd, P), set_reflect(rnd, P), set_distance(rnd, P), set_real(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
            plain = re.sub(r"<[^>]+>", "", it["q"]) + " ".join(it["c"]) + it["e"]
            assert not re.search(r"(?<![\w(|])-\d", plain), plain   # use the real minus sign
    return {
        "country": "us", "subject": "math", "grade": "grade-6", "slug": "coordinate-plane-four-quadrants", "sort": 14,
        "updated": UPDATED, "pdf_url": "",
        "title": "The Coordinate Plane: Four Quadrants, Reflections and Distance",
        "seo_title": "Grade 6 Coordinate Plane Worksheets: Four Quadrants, Reflections and Distance (6.NS.C.8)",
        "short_title": "Coordinate plane (4 quadrants)",
        "domain": "The Number System",
        "standard_code": "6.NS.C.8",
        "standard_url": "https://www.thecorestandards.org/Math/Content/6/NS/C/8/",
        "standard_text": "Solve real-world and mathematical problems by graphing points in all four quadrants of the coordinate plane. Include use of coordinates and absolute value to find distances between points with the same first coordinate or the same second coordinate.",
        "meta_desc": "Free Grade 6 coordinate plane worksheets: plot points in all four quadrants, name the quadrant from the signs, reflect points across the x-axis and y-axis, find distances with absolute value, and solve polygon and map problems. 100 practice questions with an answer key.",
        "key_big": "The signs of (x, y) tell the direction: negative x goes left, negative y goes down.",
        "key_sub": "Quadrants are numbered I to IV counterclockwise from the top right. Reflecting across the x-axis changes the sign of y; across the y-axis, the sign of x. For points on the same grid line, add the absolute values if they are on opposite sides of an axis and subtract if they are on the same side.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (every grid) so their numbers stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "coordinate grid")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
