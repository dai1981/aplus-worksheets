# -*- coding: utf-8 -*-
"""
CA Grade 6 Math: Cartesian Plane and Transformations
(Ontario Mathematics Curriculum 2020, Grade 6: Spatial Sense, E1)
  python3 tools/gen_ca_math_g6_cartesian.py
HTML attributes use single quotes (no backslashes in the JSON).

Canadian English (counterclockwise, metres, centre). Whole-number coordinates from −6 to 6 on every
grid; negative numbers use the real minus sign. Every grid is square and exact: a point (x, y) sits
x grid spaces right (left if x < 0) of the origin and y spaces up (down if y < 0). Axis numbers,
quadrant names, notes, dots and letter labels never overlap (checked in Grid.render).
Wrong answers come from real mistakes: writing (y, x), dropping or flipping a minus sign, numbering
the quadrants clockwise, moving the wrong way or changing the wrong coordinate in a translation,
counting grid lines instead of spaces (one too many), subtracting when a move crosses an axis
(−2 to 3 is 5, not 1), reflecting in the wrong axis, rotating the wrong way, swapping the numbers
in a rotation without changing a sign, mixing up 90° and 180°.
Grade 6 in Ontario does not add or subtract integers yet (Grade 7), so moves are explained by
counting spaces on the grid, not by integer sums.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
GRID = "#c9d3cc"
QCOL = "#7a8a80"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]
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
        self.pts, self.segs, self.arrows, self.notes, self.arcs = [], [], [], [], []

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

    def arc(self, a, b, cw, col=RED):
        """Turning arrow about the origin from point a to point b (same distance from the origin)."""
        assert a[0] ** 2 + a[1] ** 2 == b[0] ** 2 + b[1] ** 2
        self.arcs.append((a, b, cw, col))
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
        for a, b, cw, col in self.arcs:
            p, q = self.P(*a), self.P(*b)
            r = math.hypot(a[0], a[1]) * u
            # stop short of the end dot so the arrowhead sits just before it
            d = 1 if cw else -1                       # screen y is down: clockwise = growing angle
            ang2 = math.atan2(q[1] - oy, q[0] - ox) - d * 15.0 / r
            ang0 = math.atan2(p[1] - oy, p[0] - ox) + d * 7.0 / r
            e = (ox + r * math.cos(ang2), oy + r * math.sin(ang2))
            start = (ox + r * math.cos(ang0), oy + r * math.sin(ang0))
            sweep_ang = (d * (ang2 - ang0)) % (2 * math.pi)
            large = 1 if sweep_ang > math.pi else 0
            s.append("<path d='M%.1f,%.1f A%.1f,%.1f 0 %d %d %.1f,%.1f' fill='none' stroke='%s' stroke-width='2.5'/>"
                     % (start[0], start[1], r, r, large, 1 if cw else 0, e[0], e[1], col))
            v = (e[0] - ox, e[1] - oy)
            t = (-v[1] / r, v[0] / r) if cw else (v[1] / r, -v[0] / r)
            tip = (e[0] + t[0] * 9, e[1] + t[1] * 9)
            n = (-t[1], t[0])
            s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>"
                     % (tip[0], tip[1], e[0] + n[0] * 5, e[1] + n[1] * 5, e[0] - n[0] * 5, e[1] - n[1] * 5, col))
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


def grid_for(pts, quads=False):
    """Every question grid runs from −6 to 6."""
    assert all(max(abs(p[0]), abs(p[1])) <= 6 for p in pts), pts
    return Grid(6, quads=quads)


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
            e += " %s is point %s: the numbers are swapped." % (pair(y, x), pts[1][2])
        its.append(mcq(fig(pts_grid(pts, "coordinate grid with labelled points")) +
                       "What are the coordinates of point %s?" % n, pair(x, y), read_cands(x, y), e, rnd))
    its.append(mcq_int(fig(pts_grid([(-4, 2, "P")], "coordinate grid with labelled points")) +
                       "What is the x-coordinate of point P?", -4, [4, 2, -2],
                       "Point P is 4 units to the left of the origin, so x = " + num(-4) + ". Left means negative. (2 is its y-coordinate.)"))
    its.append(mcq_int(fig(pts_grid([(3, -6, "Q")], "coordinate grid with labelled points")) +
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
            e += " Point %s is at %s: the numbers are swapped." % (where[(y, x)], pair(y, x))
        elif (-x, y) in where and x != 0:
            e += " Point %s is at %s: the sign of x is wrong." % (where[(-x, y)], pair(-x, y))
        its.append(mcq_fixed(fig(pts_grid(pts, "coordinate grid with points A to D")) +
                             "Which point is at %s?" % pair(x, y), ["A", "B", "C", "D"], ans, e))
    its.append(mcq("To plot %s, what do you do first from the origin?" % pair(-5, 2), "Go left 5",
                   ["Go right 5", "Go down 5", "Go left 2"],
                   "The first number, " + num(-5) + ", is the x-coordinate. It is negative, so go left 5. Then go up 2.", rnd))
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq("A point is 3 units left of the origin and 4 units up. %s writes its coordinates as %s. What mistake did %s make?"
                   % (n, pair(4, -3), he),
                   "%s wrote the y-coordinate first" % H,
                   ["%s counted the grid lines, not the spaces" % H, "%s should have used (3, 4)" % H, "No mistake. %s is right" % H],
                   "The point is %s: left 3 gives x = %s, up 4 gives y = 4. %s put the numbers in the wrong order. "
                   "Always write x (across) first." % (pair(-3, 4), num(-3), n), rnd))
    n, he, his = P.next()
    its.append(mcq("%s starts at the origin. %s goes left 4, then down 3. Which coordinates name %s point?" % (n, he.capitalize(), his),
                   pair(-4, -3), [pair(-3, -4), pair(4, 3), pair(4, -3)],
                   "Left 4 gives x = %s. Down 3 gives y = %s. Write x first: %s." % (num(-4), num(-3), pair(-4, -3)), rnd))
    its.append(mcq("A point is 6 units to the right of the y-axis and 2 units below the x-axis. What are its coordinates?",
                   pair(6, -2), [pair(-2, 6), pair(6, 2), pair(-6, -2)],
                   "Right of the y-axis means x is positive: x = 6. Below the x-axis means y is negative: y = %s. The point is %s."
                   % (num(-2), pair(6, -2)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Read and plot points in all four quadrants", "items": its}


# ------------------------------------------------------------ set 2: quadrants and signs
def quad_e(x, y):
    sx = "positive (right)" if x > 0 else "negative (left)"
    sy = "positive (up)" if y > 0 else "negative (down)"
    return "x is %s and y is %s, so %s is in %s. The quadrants are numbered counterclockwise, starting at the top right." % (
        sx, sy, pair(x, y), quad(x, y))


def set_quadrants(rnd, P):
    its = []
    pos = Pos(rnd)
    for x, y in [(-2, -5), (4, -6), (-3, 6), (6, 1), (-6, -1), (1, -4), (-5, 2), (5, 5)]:
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
    its.append(mcq("Which point could be in Quadrant IV?", pair(4, -2), [pair(-4, 2), pair(-4, -2), pair(4, 2)],
                   "Quadrant IV is the bottom-right part: x positive (right), y negative (down). %s is right 4 and down 2." % pair(4, -2), rnd))
    its.append(mcq("Which point is in Quadrant II?", pair(-5, 6), [pair(5, -6), pair(-5, -6), pair(5, 6)],
                   "Quadrant II is the top-left part: x negative, y positive. %s is left 5 and up 6. (%s is in Quadrant IV: "
                   "that is where Quadrant II would be if you counted clockwise.)" % (pair(-5, 6), pair(5, -6)), rnd))
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
                   ["%s swapped x and y" % H, "%s ignored the minus sign" % H, "No mistake. %s is right" % H],
                   "%s is left and up: Quadrant II. The quadrants go counterclockwise: I top right, II top left, III bottom left, IV bottom right." % pair(-3, 5), rnd))
    n, he, his = P.next()
    its.append(mcq("%s says %s is in Quadrant IV. Is %s right?" % (n, pair(0, -4), he),
                   "No, it is on the y-axis, not in a quadrant",
                   ["Yes, y is negative", "No, it is in Quadrant III", "No, it is on the x-axis"],
                   "x = 0, so the point sits on the y-axis, 4 units below the origin. Points on an axis are not in any quadrant.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Quadrants and the signs of coordinates", "items": its}


# ------------------------------------------------------------ set 3: translations
DIRS = {"left": (-1, 0), "right": (1, 0), "up": (0, 1), "down": (0, -1)}
OPP = {"left": "right", "right": "left", "up": "down", "down": "up"}


def move(p, d, k):
    v = DIRS[d]
    return (p[0] + v[0] * k, p[1] + v[1] * k)


def change_e(p, d, k):
    """'x: 3 left from −2 is −5' style step for one move (counted on the grid)."""
    i = 0 if d in ("left", "right") else 1
    nm = "x" if i == 0 else "y"
    r = move(p, d, k)
    return "%s: %d %s from %s is %s" % (nm, k, d, num(p[i]), num(r[i]))


def trans_cands(p, moves):
    """Wrong answers for a translation: the opposite way, the amounts swapped, the wrong sign."""
    right = p
    for d, k in moves:
        right = move(right, d, k)
    opp = p
    for d, k in moves:
        opp = move(opp, OPP[d], k)
    out = [opp]
    if len(moves) == 1:
        d, k = moves[0]
        i = 0 if d in ("left", "right") else 1
        other = {"left": "down", "right": "up", "up": "right", "down": "left"}[d]
        out.append(move(p, other, k))                       # changed the wrong coordinate
        flip = list(right)
        flip[i] = -flip[i]
        out.append(tuple(flip))                             # sign error
    else:
        (d1, k1), (d2, k2) = moves
        out.append(move(move(p, d1, k2), d2, k1))          # amounts swapped
        out.append(move(move(p, d1, k1), OPP[d2], k2))     # wrong way up/down
        out.append((right[1], right[0]))
    return right, [pair(*c) for c in out if c != right]


def move_words(moves):
    return " and ".join("%d %s %s" % (k, "unit" if k == 1 else "units", d) for d, k in moves)


def set_translate(rnd, P):
    its = []
    pos = Pos(rnd)
    for p, d, k in [((-2, 3), "left", 3), ((4, -1), "down", 4), ((-5, -2), "right", 6),
                    ((3, 4), "down", 6), ((-1, -4), "up", 5), ((2, 5), "left", 6)]:
        r, cands = trans_cands(p, [(d, k)])
        axis_word = "Only x changes" if d in ("left", "right") else "Only y changes"
        e = "%s. %s. The new point is %s." % (axis_word, change_e(p, d, k), pair(*r))
        its.append(mcq("Point %s is translated %s. What are its new coordinates?" % (pair(*p), move_words([(d, k)])),
                       pair(*r), cands, e, rnd))
    for p, moves in [((-3, 2), [("right", 5), ("down", 4)]), ((4, -1), [("left", 6), ("up", 3)])]:
        r, cands = trans_cands(p, moves)
        q = move(p, *moves[0])
        e = "%s, then %s. The new point is %s." % (change_e(p, *moves[0]), change_e(q, *moves[1]), pair(*r))
        its.append(mcq("Point %s is translated %s. What are its new coordinates?" % (pair(*p), move_words(moves)),
                       pair(*r), cands, e, rnd))
    # describe the translation
    its.append(mcq("A point moves from %s to %s. Describe the translation." % (pair(-3, 2), pair(2, 2)),
                   "5 units right", ["1 unit right", "6 units right", "5 units left"],
                   "Only x changes, from %s to 2. Count the spaces: 3 to the y-axis, then 2 more, so 3 + 2 = 5 units right. "
                   "(6 comes from counting the grid lines.)" % num(-3), rnd))
    its.append(mcq("A point moves from %s to %s. Describe the translation." % (pair(4, -3), pair(4, 3)),
                   "6 units up", ["3 units up", "7 units up", "6 units down"],
                   "Only y changes, from %s to 3. That is 3 up to the x-axis and 3 more: 3 + 3 = 6 units up." % num(-3), rnd))
    its.append(mcq("A point moves from %s to %s. Describe the translation." % (pair(1, 4), pair(-4, 1)),
                   "5 units left and 3 units down",
                   ["5 units right and 3 units down", "3 units left and 5 units down", "6 units left and 4 units down"],
                   "x goes from 1 to %s: 1 to the y-axis and 4 more, so 5 units left. y goes from 4 to 1: 3 units down." % num(-4), rnd))
    its.append(mcq("A point moves from %s to %s. Describe the translation." % (pair(-5, -3), pair(2, 1)),
                   "7 units right and 4 units up",
                   ["3 units right and 2 units up", "8 units right and 5 units up", "4 units right and 7 units up"],
                   "x goes from %s to 2: 5 + 2 = 7 units right. y goes from %s to 1: 3 + 1 = 4 units up. "
                   "The moves cross an axis, so add; do not subtract 5 − 2." % (num(-5), num(-3)), rnd))
    its.append(mcq("Point (x, y) is translated 3 units left. Which shows its new coordinates?", "(x − 3, y)",
                   ["(x + 3, y)", "(x, y − 3)", "(x − 3, y − 3)"],
                   "Left and right moves change only x. Left makes x smaller, so subtract 3: (x − 3, y). y stays the same.", rnd))
    its.append(mcq("A point moves from (x, y) to (x, y − 2). How did it move?", "2 units down",
                   ["2 units up", "2 units left", "2 units right"],
                   "Only y changed, so the point moved up or down. y got 2 smaller, so the point moved 2 units down.", rnd))
    # grid: which point is P after the translation?
    for p, moves in [((-4, 4), [("right", 6), ("down", 2)]), ((3, 1), [("left", 6), ("down", 3)]),
                     ((-3, -1), [("right", 4), ("up", 3)])]:
        r, _ = trans_cands(p, moves)
        (d1, k1), (d2, k2) = moves
        swapped = move(move(p, d1, k2), d2, k1)
        wrongway = move(move(p, d1, k1), OPP[d2], k2)
        lines = move(move(p, d1, k1 + 1), d2, k2 + 1)
        others = [o for o in [swapped, wrongway, lines] if max(abs(o[0]), abs(o[1])) <= 6]
        assert len(others) == 3, (p, others)
        pts, ans = pick_letters(r, others, pos)
        G = Grid(6)
        G.point(p[0], p[1], "P", RED)
        for t in pts:
            G.point(*t)
        where = {(t[0], t[1]): t[2] for t in pts}
        q = move(p, d1, k1)
        e = ("P is at %s. %s, then %s. The image is %s: point %s. Point %s comes from counting grid lines instead of spaces."
             % (pair(*p), change_e(p, d1, k1), change_e(q, d2, k2), pair(*r), ans, where[lines]))
        its.append(mcq_fixed(fig(G.svg("coordinate grid with point P and points A to D")) +
                             "Point P is translated %s. Which point shows where it lands?" % move_words(moves),
                             ["A", "B", "C", "D"], ans, e))
    # grid with arrows: describe the move
    G = Grid(6)
    G.arrow((-5, 3), (2, 3)).arrow((2, 3), (2, -2))
    G.point(-5, 3, "P", RED, where=(-1, -1)).point(2, -2, "Q", where=(1, -1))
    its.append(mcq(fig(G.svg("coordinate grid with arrows from P to Q")) + "Describe the translation from P to Q.",
                   "7 units right and 5 units down",
                   ["8 units right and 6 units down", "3 units right and 1 unit down", "5 units right and 7 units down"],
                   "P is at %s and Q is at %s. x: %s to 2 is 5 + 2 = 7 units right. y: 3 to %s is 3 + 2 = 5 units down. "
                   "Both moves cross an axis, so add. Count the spaces between the lines, not the lines." % (pair(-5, 3), pair(2, -2), num(-5), num(-2)), rnd))
    its.append(mcq("Triangle ABC has vertices A %s, B %s and C %s. It is translated 5 units right and 6 units down. "
                   "Where does C land?" % (pair(-4, 1), pair(-1, 1), pair(-1, 4)),
                   pair(4, -2), [pair(4, 10), pair(5, -1), pair(-6, -2)],
                   "Every vertex moves the same way. C is at %s. x: 5 right from %s is 4. y: 6 down from 4 is %s "
                   "(4 down to the x-axis, then 2 more). C lands on %s." % (pair(-1, 4), num(-1), num(-2), pair(4, -2)), rnd))
    n, he, his = P.next()
    its.append(mcq("In a board game, %s’s counter is on %s. %s moves it 6 units right and 5 units up. Where is it now?"
                   % (n, pair(-2, -3), he.capitalize()),
                   pair(4, 2), [pair(-8, 2), pair(3, 3), pair(4, -8)],
                   "x: 6 right from %s is 4 (2 to the y-axis, then 4 more). y: 5 up from %s is 2 (3 to the x-axis, then 2 more). "
                   "The counter is on %s." % (num(-2), num(-3), pair(4, 2)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Translations: how the coordinates change", "items": its}


# ------------------------------------------------------------ set 4: reflections in the axes
def reflect(p, axis):
    return (p[0], -p[1]) if axis == "x" else (-p[0], p[1])


def refl_e(p, axis):
    r = reflect(p, axis)
    if r == p:
        return ("%s is on the %s-axis, the mirror line itself, so its reflection is the same point: %s."
                % (pair(*p), axis, pair(*r)))
    if axis == "x":
        return ("In the x-axis, the point flips up or down: x stays %s and y changes sign, %s → %s. The image is %s."
                % (num(p[0]), num(p[1]), num(-p[1]), pair(*r)))
    return ("In the y-axis, the point flips left or right: y stays %s and x changes sign, %s → %s. The image is %s."
            % (num(p[1]), num(p[0]), num(-p[0]), pair(*r)))


def set_reflect(rnd, P):
    its = []
    pos = Pos(rnd)
    for p, axis in [((3, -2), "y"), ((-4, 5), "x"), ((6, 1), "y"), ((-2, -6), "x"), ((5, 4), "x"), ((-6, -3), "y")]:
        r = reflect(p, axis)
        other = reflect(p, "y" if axis == "x" else "x")
        both = (-p[0], -p[1])
        its.append(mcq("Reflect %s in the %s-axis. What are the coordinates of the image?" % (pair(*p), axis),
                       pair(*r), [pair(*other), pair(*both), pair(r[1], r[0])], refl_e(p, axis), rnd))
    its.append(mcq("Reflect %s in the y-axis. What are the coordinates of the image?" % pair(0, 6), pair(0, 6),
                   [pair(0, -6), pair(6, 0), pair(-6, 0)], refl_e((0, 6), "y"), rnd))
    its.append(mcq("Reflect %s in the x-axis. What are the coordinates of the image?" % pair(-5, 0), pair(-5, 0),
                   [pair(5, 0), pair(0, -5), pair(0, 5)], refl_e((-5, 0), "x"), rnd))
    for p, axis, extra in [((-3, 2), "x", (-3, 0)), ((4, -3), "y", (0, -3)), ((-2, -4), "x", (-2, 0)), ((5, 2), "y", (2, 5))]:
        r = reflect(p, axis)
        others = [reflect(p, "y" if axis == "x" else "x"), (-p[0], -p[1]), extra]
        pts, ans = pick_letters(r, others, pos)
        where = {(q[0], q[1]): q[2] for q in pts}
        G = Grid(6)
        G.point(p[0], p[1], "P", RED)
        for q in pts:
            G.point(*q)
        wa = where[others[0]]
        e = "P is at %s. %s That is point %s. Point %s is the reflection in the %s-axis instead." % (
            pair(*p), refl_e(p, axis), ans, wa, "y" if axis == "x" else "x")
        its.append(mcq_fixed(fig(G.svg("coordinate grid with point P and points A to D")) +
                             "Which point is the reflection of point P in the %s-axis?" % axis, ["A", "B", "C", "D"], ans, e))
    its.append(mcq_fixed("The points %s and %s are reflections of each other in which axis?" % (pair(4, 1), pair(-4, 1)), AXES,
                         "the y-axis", "Only the x-coordinate changes sign (4 → %s), so the points flip left and right. The mirror line is the y-axis." % num(-4)))
    its.append(mcq_fixed("The points %s and %s are reflections of each other in which axis?" % (pair(-3, 5), pair(-3, -5)), AXES,
                         "the x-axis", "Only the y-coordinate changes sign (5 → %s), so the points flip up and down. The mirror line is the x-axis." % num(-5)))
    its.append(mcq_fixed("%s is reflected in one axis and then in the other. Where does it land?" % pair(2, -6),
                         [pair(-2, -6), pair(2, 6), pair(-2, 6), pair(-6, 2)], pair(-2, 6),
                         "In the x-axis: %s → %s. Then in the y-axis: %s → %s. Both signs change." % (
                             pair(2, -6), pair(2, 6), pair(2, 6), pair(-2, 6))))
    its.append(mcq_fixed("Are %s and %s reflections of each other in an axis?" % (pair(3, 4), pair(4, 3)),
                         ["Yes, in the x-axis", "Yes, in the y-axis", "Yes, in both axes", "No, in neither axis"],
                         "No, in neither axis",
                         "A reflection in an axis keeps the same numbers and changes one sign. Here the numbers are swapped, and no sign changes."))
    its.append(mcq("When you reflect a point in the x-axis, what changes?", "the sign of the y-coordinate",
                   ["the sign of the x-coordinate", "the signs of both coordinates", "the order of the numbers"],
                   "The x-axis is a mirror lying flat. The point flips up or down, so only y changes sign. Example: %s → %s."
                   % (pair(2, 3), pair(2, -3)), rnd))
    its.append(mcq("Point Q is the reflection of point P in the y-axis. Q is at %s. Where is P?" % pair(-3, 4), pair(3, 4),
                   [pair(-3, -4), pair(3, -4), pair(4, -3)],
                   "Reflecting in the y-axis changes only the sign of x, and reflecting back does the same. %s → %s."
                   % (pair(-3, 4), pair(3, 4)), rnd))
    its.append(mcq_fixed("Point %s is reflected in the y-axis. Which quadrant is the image in?" % pair(-6, 2), QUADS, "Quadrant I",
                         "The image is %s. Both coordinates are positive, so it is in Quadrant I." % pair(6, 2)))
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq("%s reflects %s in the x-axis and gets %s. What mistake did %s make?" % (n, pair(2, 5), pair(-2, 5), he),
                   "%s reflected in the y-axis" % H,
                   ["%s swapped x and y" % H, "%s changed both signs" % H, "No mistake. %s is right" % H],
                   "%s changed the sign of x, which is a reflection in the y-axis. In the x-axis, y changes sign: %s." % (H, pair(2, -5)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Reflections in the x-axis and y-axis", "items": its}


# ------------------------------------------------------------ set 5: rotations about the origin and combinations
TURNS = {"cw": "90° clockwise", "ccw": "90° counterclockwise", "half": "180°"}


def rot(p, kind):
    x, y = p
    if kind == "cw":
        return (y, -x)
    if kind == "ccw":
        return (-y, x)
    return (-x, -y)


def mv(x, y):
    """'3 right and 1 up' (x first, then y)."""
    a = "" if x == 0 else ("%d right" % x if x > 0 else "%d left" % -x)
    b = "" if y == 0 else ("%d up" % y if y > 0 else "%d down" % -y)
    return " and ".join(t for t in (a, b) if t) or "at the origin"


WAYS = {"cw": "right turns into down, down into left, left into up and up into right",
        "ccw": "right turns into up, up into left, left into down and down into right",
        "half": "right turns into left, left into right, up into down and down into up"}


def rot_e(p, kind, name=None):
    r = rot(p, kind)
    nm = (name + " " + pair(*p)) if name else pair(*p)
    return ("%s is %s from the origin. In a %s turn, %s. So the image is %s from the origin: %s."
            % (nm, mv(*p), TURNS[kind], WAYS[kind], mv(*r), pair(*r)))


def rot_cands(p, kind):
    """Rotating the wrong way, swapping the numbers without a sign change, mixing up 90° and 180°."""
    if kind == "half":
        out = [(-p[0], p[1]), (p[0], -p[1]), (p[1], p[0]), (-p[1], -p[0])]
    else:
        other = "ccw" if kind == "cw" else "cw"
        out = [rot(p, other), (p[1], p[0]), rot(p, "half")]
    return [pair(*c) for c in out if c != rot(p, kind)]


def set_rotate(rnd, P):
    its = []
    pos = Pos(rnd)
    for p, kind in [((3, 1), "cw"), ((-2, 4), "cw"), ((-5, -3), "cw"),
                    ((4, 2), "ccw"), ((-1, 5), "ccw"), ((6, -3), "ccw"),
                    ((2, -5), "half"), ((-4, 3), "half")]:
        r = rot(p, kind)
        its.append(mcq("Rotate %s %s about the origin. What are the coordinates of the image?" % (pair(*p), TURNS[kind]),
                       pair(*r), rot_cands(p, kind), rot_e(p, kind), rnd))
    # grid: which point is the image of P?
    for p, kind, others in [((4, 1), "ccw", [(1, -4), (-4, -1), (1, 4)]),
                            ((-3, 2), "cw", [(-2, -3), (3, -2), (3, 2)]),
                            ((-5, -2), "half", [(5, -2), (-5, 2), (-2, 5)])]:
        r = rot(p, kind)
        pts, ans = pick_letters(r, others, pos)
        where = {(t[0], t[1]): t[2] for t in pts}
        G = Grid(6)
        G.point(p[0], p[1], "P", RED)
        for t in pts:
            G.point(*t)
        e = rot_e(p, kind, "P") + " That is point %s." % ans
        if kind != "half":
            e += " Point %s is a %s turn: the wrong way." % (where[others[0]], TURNS["ccw" if kind == "cw" else "cw"])
        else:
            e += " Points %s and %s are reflections in one axis, where only one sign changes." % (where[others[0]], where[others[1]])
        its.append(mcq_fixed(fig(G.svg("coordinate grid with point P and points A to D")) +
                             "Point P is rotated %s about the origin. Which point is the image?" % TURNS[kind],
                             ["A", "B", "C", "D"], ans, e))
    its.append(mcq_fixed("Point %s is rotated 90° clockwise about the origin. Which quadrant is the image in?" % pair(-4, 3),
                         QUADS, "Quadrant I",
                         "%s is in Quadrant II. A quarter turn clockwise moves it to the next quadrant clockwise: from the top left to the top right. "
                         "The image is %s, in Quadrant I." % (pair(-4, 3), pair(3, 4))))
    its.append(mcq_fixed("Point %s is rotated about the origin and lands on %s. Describe the rotation." % (pair(2, 5), pair(-5, 2)),
                         ["90° clockwise", "90° counterclockwise", "180°", "360°"], "90° counterclockwise",
                         "%s is 2 right and 5 up. %s is 5 left and 2 up. Right turned into up and up turned into left: "
                         "that is a quarter turn counterclockwise. (90° clockwise would give %s.)" % (pair(2, 5), pair(-5, 2), pair(5, -2))))
    its.append(mcq("Point %s is rotated 270° counterclockwise about the origin. Where does it land?" % pair(2, 5),
                   pair(5, -2), [pair(-5, 2), pair(-2, -5), pair(2, -5)],
                   "270° counterclockwise is 3 quarter turns counterclockwise. That ends in the same place as 1 quarter turn clockwise "
                   "(360° − 270° = 90°). " + rot_e((2, 5), "cw"), rnd))
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq("%s rotates %s 90° clockwise about the origin and gets %s. What mistake did %s make?" % (n, pair(4, 1), pair(-1, 4), he),
                   "%s turned it counterclockwise" % H,
                   ["%s swapped the numbers and changed no sign" % H, "%s turned it 180°" % H, "No mistake. %s is right" % H],
                   "%s is a quarter turn counterclockwise. %s Check: %s is in Quadrant I, and a clockwise turn takes it to Quadrant IV."
                   % (pair(-1, 4), rot_e((4, 1), "cw"), pair(4, 1)), rnd))
    # combinations and word problems
    n, he, his = P.next()
    its.append(mcq("%s makes a snowflake design for the class window. One tip is at %s. %s rotates the design 360° about the origin. "
                   "Where is that tip now?" % (n, pair(-3, 5), he.capitalize()), pair(-3, 5),
                   [pair(3, -5), pair(5, 3), pair(-5, -3)],
                   "360° is a full turn, so every point comes back to where it started. The tip is still at %s." % pair(-3, 5), rnd))
    n, he, his = P.next()
    its.append(mcq_fixed("%s draws a point at %s for a quilt pattern. %s reflects it in the x-axis, then reflects the image in the y-axis. "
                         "Which single move gives the same result?" % (n, pair(1, 4), he.capitalize()),
                         ["a rotation of 90° clockwise", "a rotation of 90° counterclockwise", "a rotation of 180°", "a reflection in the x-axis"],
                         "a rotation of 180°",
                         "In the x-axis: %s → %s. Then in the y-axis: %s → %s. Both signs changed, and that is what a 180° rotation "
                         "about the origin does." % (pair(1, 4), pair(1, -4), pair(1, -4), pair(-1, -4))))
    n, he, his = P.next()
    its.append(mcq("In a video game, %s’s spaceship is at %s. The screen is a grid with the origin in the centre. The ship is rotated "
                   "90° clockwise about the origin. Where is it now?" % (n, pair(-2, 6)), pair(6, 2),
                   [pair(-6, -2), pair(2, -6), pair(6, -2)], rot_e((-2, 6), "cw"), rnd))
    n, he, his = P.next()
    its.append(mcq("In a coding app, %s’s sprite is at %s. %s translates it 6 units right, then rotates it 180° about the origin. "
                   "Where does it end up?" % (n, pair(-4, -3), he.capitalize()), pair(-2, 3),
                   [pair(2, -3), pair(-2, -3), pair(2, 3)],
                   "Do the moves in order. 6 right from %s: x goes from %s to 2, so the sprite is at %s. "
                   "A 180° rotation changes both signs: %s → %s." % (pair(-4, -3), num(-4), pair(2, -3), pair(2, -3), pair(-2, 3)), rnd))
    n, he, his = P.next()
    its.append(mcq("%s designs a pinwheel for a Terry Fox Run poster. One blade tip is at %s. The next blade is the first one rotated "
                   "90° counterclockwise about the origin. Where is the next tip?" % (n, pair(1, 5)), pair(-5, 1),
                   [pair(5, -1), pair(5, 1), pair(-1, -5)], rot_e((1, 5), "ccw"), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Rotations about the origin and combinations of moves", "items": its}


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
    G.arrow((-4, -2), (1, -2)).arrow((1, -2), (1, 2))
    G.note(-2.5, -1.5, "right 5").note(1.2, 0.5, "up 4", anchor="start")
    G.point(-4, -2, "P", RED, where=(-1, 1)).point(1, 2, "Q", where=(1, 1))
    trans = G.svg("translation of P (−4, −2) 5 units right and 4 units up to Q (1, 2)")
    G = Grid(5)
    G.seg((3, 2), (-3, 2), RED, 2, dash=True).seg((3, 2), (3, -2), RED, 2, dash=True)
    G.point(3, 2, "P", RED).point(-3, 2, "Q").point(3, -2, "R")
    refl = G.svg("point P (3, 2), its reflection Q (−3, 2) in the y-axis and R (3, −2) in the x-axis")
    G = Grid(5)
    G.arc((4, 2), (2, -4), True).arc((4, 2), (-4, -2), False, GREEN)
    G.point(4, 2, "P", RED, where=(1, 1)).point(2, -4, "Q", where=(1, -1)).point(-4, -2, "R", where=(-1, -1))
    rota = G.svg("point P (4, 2) rotated 90° clockwise about the origin to Q (2, −4), and 180° to R (−4, −2)")
    return (
        "<h2>The four quadrants</h2>"
        "<p>On the Cartesian plane, the x-axis and the y-axis are number lines that include negative numbers. They cross at the "
        "<b>origin</b>, (0, 0), and cut the plane into four <b>quadrants</b>. The quadrants are numbered I, II, III, IV "
        "<b>counterclockwise</b>, starting at the top right.</p>"
        "<p>In (x, y), x always comes first. The sign tells the direction. Positive x: right. Negative x: left. "
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
        "<h2>Translations: sliding a point</h2>"
        "<p>A move left or right changes only <b>x</b>. A move up or down changes only <b>y</b>.</p>" +
        table(["Move", "What happens", "Example from (2, 1)"], [
            ["3 units right", "x + 3", "(5, 1)"],
            ["3 units left", "x − 3", "(−1, 1)"],
            ["3 units up", "y + 3", "(2, 4)"],
            ["3 units down", "y − 3", "(2, −2)"],
        ]) +
        "<figure class='sn-fig'>" + trans +
        "<figcaption>P (−4, −2) moves 5 units right and 4 units up. x: 5 right from −4 is 1. y: 4 up from −2 is 2. It lands on Q (1, 2).</figcaption></figure>" +
        ex("Example", "Describe the translation from (−3, 2) to (2, 2).",
           "Only x changes. From −3 to the y-axis is 3 spaces, then 2 more: 3 + 2 = 5.", "5 units right") +
        "<h2>Reflections in the axes</h2>"
        "<p>An axis works like a mirror. Reflecting in the <b>x-axis</b> changes the sign of <b>y</b>. "
        "Reflecting in the <b>y-axis</b> changes the sign of <b>x</b>.</p>"
        "<figure class='sn-fig'>" + refl +
        "<figcaption>P (3, 2) reflected in the y-axis is Q (−3, 2). Reflected in the x-axis, it is R (3, −2).</figcaption></figure>" +
        ex("Example", "Reflect (−4, 5) in the x-axis.", "The x-axis is the mirror, so the point flips down. x stays −4. y changes sign: 5 → −5.",
           "(−4, −5)") +
        "<h2>Rotations about the origin</h2>"
        "<p>A rotation turns a point around the origin. It stays the same distance from the origin. "
        "Say how far (90°, 180°, 270° or 360°) and which way (clockwise or counterclockwise).</p>"
        "<p>To rotate, describe the point from the origin, then turn each direction. "
        "A quarter turn (90°) clockwise turns right into down and up into right. "
        "A half turn (180°) turns right into left and up into down, so <b>both signs change</b>. "
        "A full turn (360°) brings the point back where it started.</p>"
        "<figure class='sn-fig'>" + rota +
        "<figcaption>P (4, 2) is 4 right and 2 up. A 90° clockwise turn makes it 2 right and 4 down: Q (2, −4). "
        "A 180° turn makes it 4 left and 2 down: R (−4, −2).</figcaption></figure>" +
        table(["Rotation about the origin", "Pattern", "Example from (4, 2)"], [
            ["90° clockwise", "(x, y) → (y, opposite of x)", "(2, −4)"],
            ["90° counterclockwise", "(x, y) → (opposite of y, x)", "(−2, 4)"],
            ["180°", "both signs change", "(−4, −2)"],
            ["360°", "no change", "(4, 2)"],
        ]) +
        ex("Example", "Rotate (−3, 5) 90° counterclockwise about the origin.",
           "(−3, 5) is 3 left and 5 up. A quarter turn counterclockwise turns left into down and up into left. "
           "So the image is 5 left and 3 down.", "(−5, −3)") +
        ex("Combination", "Reflect (1, 4) in the x-axis, then reflect the image in the y-axis.",
           "(1, 4) → (1, −4) → (−1, −4). Both signs changed, so the two reflections give the same result as a 180° rotation.", "(−1, −4)") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Swapping the numbers: plotting (−3, 4) at (4, −3)", "Move across first (x), then up or down (y)"],
            ["Dropping the minus sign", "Negative x means left; negative y means down"],
            ["Numbering the quadrants clockwise", "Go counterclockwise: I top right, II top left, III bottom left, IV bottom right"],
            ["Counting grid lines instead of spaces", "Count the jumps between lines; the starting line is 0"],
            ["From −3 to 2 doing 3 − 2 = 1", "The move crosses an axis, so add: 3 + 2 = 5"],
            ["Reflecting in the wrong axis", "In the x-axis, y changes sign. In the y-axis, x changes sign"],
            ["Rotating the wrong way", "Clockwise goes the way clock hands move: from the top to the right"],
            ["Only swapping the numbers in a 90° turn: (4, 2) → (2, 4)", "Swap and change one sign: (2, −4) clockwise, (−2, 4) counterclockwise"],
        ])
    )


FAQ = [
    {"q": "What do Grade 6 students learn about the Cartesian plane in the Ontario math curriculum?",
     "a": "In Grade 6 (Spatial Sense, E1), students plot and read points in all four quadrants, describe translations from one point to another, and perform and predict combinations of translations, reflections and rotations up to 360°."},
    {"q": "How are the four quadrants numbered?",
     "a": "Counterclockwise from the top right: Quadrant I (+, +), II (−, +), III (−, −) and IV (+, −). A point on an axis, like (0, −4), is not in any quadrant."},
    {"q": "How do you rotate a point 90° about the origin?",
     "a": "Describe the point from the origin, then turn each direction. For 90° clockwise, right becomes down and up becomes right, so (4, 2) goes to (2, −4); a 180° turn changes both signs."},
    {"q": "Is the Cartesian plane on the Grade 6 EQAO math test?",
     "a": "The Grade 6 EQAO math assessment is based on the Ontario curriculum, which includes the spatial sense expectations on coordinates and transformations. Practising these questions helps students get ready for it."},
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
    rnd = random.Random(36814)
    P = People(rnd)
    sets = [set_read(rnd, P), set_quadrants(rnd, P), set_translate(rnd, P), set_reflect(rnd, P), set_rotate(rnd, P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-6", "slug": "cartesian-plane-and-transformations", "sort": 14,
        "updated": UPDATED, "pdf_url": "",
        "title": "The Cartesian Plane: Four Quadrants, Translations, Reflections and Rotations",
        "seo_title": "Grade 6 Cartesian Plane and Transformations Worksheets: Four Quadrants (Free, Answer Key)",
        "short_title": "Cartesian plane and transformations",
        "domain": "Spatial Sense",
        "standard_code": "Grade 6: Spatial Sense, E1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Plot and read coordinates in all four quadrants of a Cartesian plane, and describe the translations that move a point from one coordinate to another; describe and perform combinations of translations, reflections, and rotations up to 360° on a grid, and predict the results",
        "meta_desc": "Free Grade 6 math worksheets on the Cartesian plane for the Ontario curriculum: plot points in all four quadrants, name quadrants from the signs, translate points, reflect them in the axes and rotate them 90° and 180° about the origin. 100 questions with an answer key, good EQAO practice.",
        "key_big": "In (x, y), x tells you left or right and y tells you up or down. A minus sign means left or down.",
        "key_sub": "Quadrants I to IV go counterclockwise from the top right. A translation changes x (left or right) or y (up or down). A reflection in the x-axis changes the sign of y; in the y-axis, the sign of x. A 180° rotation about the origin changes both signs.",
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
