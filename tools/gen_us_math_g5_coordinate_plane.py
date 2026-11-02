# -*- coding: utf-8 -*-
"""
US Grade 5 Math: The Coordinate Plane (5.G.A.1-2)
  python tools/gen_us_math_g5_coordinate_plane.py
HTML attributes use single quotes (no backslashes in the JSON).

First quadrant only, whole-number coordinates 0-10.
Every grid is drawn exactly: a point (x, y) sits on the intersection x grid spaces right of the
origin and y grid spaces up. Each letter label sits in the middle of a grid square next to its own
point, never in a square that touches another point, never on a grid line and never on another label
or note (checked in Grid.render).
Wrong answers come from real mistakes: switching x and y, counting grid lines from 1 instead of 0,
reading the next grid line, thinking (0, 5) is on the x-axis, adding the coordinates, counting points
instead of spaces when finding a distance.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
GRID = "#c9d3cc"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


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
    """Choices keep their order (A B C D, numbers from small to large, axis words)."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fixed": True}


def mcq_num(q, correct, cands, e, fmt="%d"):
    ch = []
    for c in cands:
        if c >= 0 and c != correct and c not in ch:
            ch.append(c)
    ch = sorted([correct] + ch[:3])
    assert len(ch) == 4, (q, ch)
    return mcq_fixed(q, [fmt % c for c in ch], fmt % correct, e)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label.replace("'", "’"), FONT, body))


def tw(t, fs, bold=False):
    """Approximate text width in px (Arial)."""
    return len(str(t)) * fs * (0.62 if bold else 0.58)


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK, extra=""):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, extra, t))


def pair(x, y):
    return "(%d, %d)" % (x, y)


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


# ------------------------------------------------------------ coordinate grid
def overlap(a, b, m=1.0):
    return not (a[2] + m <= b[0] or b[2] + m <= a[0] or a[3] + m <= b[1] or b[3] + m <= a[1])


class Grid:
    """First-quadrant grid from 0 to nx across and 0 to ny up. Grid space = u px.
    sx, sy: what one grid space counts by on each axis (the numbers written on the axes)."""

    def __init__(self, nx, ny, u=22, sx=1, sy=1, xt=None, yt=None, title=None):
        assert 1 <= nx <= 10 and 1 <= ny <= 10
        self.nx, self.ny, self.u, self.sx, self.sy = nx, ny, u, sx, sy
        self.xt, self.yt, self.title = xt, yt, title
        left = tw(ny * sy, 14) + 15 + (24 if yt else 0)
        top = 30 + (24 if title else 0)
        self.ox, self.oy = left, top + ny * u
        self.W = int(math.ceil(self.ox + nx * u + 28))
        self.H = int(math.ceil(self.oy + 26 + (22 if xt else 0)))
        if title:
            self.W = max(self.W, int(tw(title, 15, True) + 16))
        if xt:
            assert tw(xt, 14, True) < self.W
        if yt:
            assert tw(yt, 14, True) < ny * u + 20, yt
        self.pts, self.segs, self.arrows, self.notes = [], [], [], []

    def P(self, x, y):
        return (self.ox + x * self.u, self.oy - y * self.u)

    def point(self, x, y, name, col=GREEN, where=None):
        assert x == int(x) and y == int(y) and 0 <= x <= self.nx and 0 <= y <= self.ny, (x, y)
        assert all((p[0], p[1]) != (x, y) for p in self.pts), ("two points at the same spot", x, y)
        self.pts.append((x, y, name, col, where))
        return self

    def data_point(self, xv, yv, name, col=GREEN, where=None):
        assert xv % self.sx == 0 and yv % self.sy == 0, (xv, yv)
        return self.point(xv // self.sx, yv // self.sy, name, col, where)

    def seg(self, a, b, col=GREEN, w=3):
        assert a[0] == b[0] or a[1] == b[1], "only grid-line segments"
        self.segs.append((a, b, col, w))
        return self

    def arrow(self, a, b, col=RED):
        assert a[0] == b[0] or a[1] == b[1]
        self.arrows.append((a, b, col))
        return self

    def note(self, gx, gy, t, anchor="middle", col=RED, fs=14):
        """A short note at grid position (gx, gy) (the middle of the text)."""
        self.notes.append((gx, gy, t, anchor, col, fs))
        return self

    def _label_cell(self, x, y, used, others, boxes, where):
        dirs = [where] if where else [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dx, dy in dirs:
            cx, cy = x + dx, y + dy
            if not (0 <= cx <= self.nx and 0 <= cy <= self.ny):
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
            # segments and arrows lie on grid lines, so they never cross the middle of a square
            used.add(cell)
            return c, box
        raise AssertionError(("no room for label", x, y))

    def render(self):
        u, ox, oy, nx, ny = self.u, self.ox, self.oy, self.nx, self.ny
        s = []
        if self.title:
            s.append(text(self.W / 2.0, 18, self.title, 15, bold=True))
        for k in range(nx + 1):
            x = ox + k * u
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (x, oy, x, oy - ny * u, GRID))
        for k in range(ny + 1):
            y = oy - k * u
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (ox, y, ox + nx * u, y, GRID))
        # axes with arrows
        xe, ye = ox + nx * u + 12, oy - ny * u - 12
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (ox, oy, xe - 4, oy, INK))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (ox, oy, ox, ye + 4, INK))
        s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (xe, oy, xe - 9, oy - 4.5, xe - 9, oy + 4.5, INK))
        s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (ox, ye, ox - 4.5, ye + 9, ox + 4.5, ye + 9, INK))
        s.append(text(xe + 4, oy + 5, "x", 15, anchor="start", bold=True, extra=" font-style='italic'"))
        s.append(text(ox, ye - 6, "y", 15, bold=True, extra=" font-style='italic'"))
        for k in range(1, nx + 1):
            s.append(text(ox + k * u, oy + 18, k * self.sx, 14))
        for k in range(1, ny + 1):
            s.append(text(ox - 9, oy - k * u + 5, k * self.sy, 14, anchor="end"))
        s.append(text(ox - 9, oy + 18, 0, 14, anchor="end"))
        if self.xt:
            s.append(text(ox + nx * u / 2.0, oy + 40, self.xt, 14, bold=True))
        if self.yt:
            my = oy - ny * u / 2.0
            s.append(text(13, my, self.yt, 14, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % my))
        for a, b, col, w in self.segs:
            p, q = self.P(*a), self.P(*b)
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g' stroke-linecap='round'/>"
                     % (p[0], p[1], q[0], q[1], col, w))
        for a, b, col in self.arrows:
            p, q = self.P(*a), self.P(*b)
            L = math.hypot(q[0] - p[0], q[1] - p[1])
            d = ((q[0] - p[0]) / L, (q[1] - p[1]) / L)
            e = (q[0] - d[0] * 10, q[1] - d[1] * 10)
            n = (-d[1], d[0])
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (p[0], p[1], e[0] + d[0] * 2, e[1] + d[1] * 2, col))
            s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>"
                     % (q[0], q[1], e[0] + n[0] * 5.5, e[1] + n[1] * 5.5, e[0] - n[0] * 5.5, e[1] - n[1] * 5.5, col))
        # notes first: their boxes must stay clear of points and labels
        boxes = []
        for gx, gy, t, anchor, col, fs in self.notes:
            c = self.P(gx, gy)
            w = tw(t, fs, True)
            x0 = c[0] - w / 2 if anchor == "middle" else c[0] if anchor == "start" else c[0] - w
            box = (x0, c[1] - fs * 0.4, x0 + w, c[1] + fs * 0.4)
            assert box[0] >= 0 and box[2] <= self.W, t
            for b in boxes:
                assert not overlap(box, b), ("notes overlap", t)
            boxes.append(box)
            s.append(text(c[0], c[1] + fs * 0.36, t, fs, anchor=anchor, bold=True, col=col,
                          extra=" stroke='#ffffff' stroke-width='4' paint-order='stroke'"))
        allpts = {(p[0], p[1]) for p in self.pts}
        for x, y, name, col, where in self.pts:
            c = self.P(x, y)
            dot = (c[0] - 4.5, c[1] - 4.5, c[0] + 4.5, c[1] + 4.5)
            for b in boxes:
                assert not overlap(dot, b), ("note on a point", x, y)
        used = set()
        for x, y, name, col, where in self.pts:
            c = self.P(x, y)
            s.append("<circle cx='%.1f' cy='%.1f' r='4.5' fill='%s'/>" % (c[0], c[1], col))
            if name:
                lc, box = self._label_cell(x, y, used, allpts - {(x, y)}, boxes, where)
                boxes.append(box)
                s.append(text(lc[0], lc[1] + 5.8, name, 16, bold=True))
        return "".join(s)

    def svg(self, label="coordinate grid"):
        return svg_wrap(self.W, self.H, self.render(), label)


def grid_for(pts, extra=1, lo=5):
    """Grid just big enough for the points (smaller grids print larger)."""
    nx = min(10, max(lo, max(p[0] for p in pts) + extra))
    ny = min(10, max(lo, max(p[1] for p in pts) + extra))
    return Grid(nx, ny)


def pts_grid(pts, label="coordinate grid", nx=None, ny=None, ref=None):
    """pts: (x, y, name). ref: name of a point drawn in red (the starting point)."""
    G = grid_for(pts) if nx is None else Grid(nx, ny)
    for x, y, n in pts:
        G.point(x, y, n, RED if n == ref else GREEN)
    return G.svg(label)


# ------------------------------------------------------------ explanations
def walk(x, y):
    if x == 0 and y == 0:
        return "It is the origin: go right 0 and up 0"
    if x == 0:
        return "Start at the origin. Go right 0, then up %d" % y
    if y == 0:
        return "Start at the origin. Go right %d, then up 0" % x
    return "Start at the origin. Go right %d, then up %d" % (x, y)


def read_cands(x, y, i):
    near = [(x, y + 1), (x + 1, y), (x - 1, y), (x, y - 1)]
    near = near[i % 4:] + near[:i % 4]
    out = []
    for c in [(y, x), (x + 1, y + 1)] + near:
        if c != (x, y) and min(c) >= 0 and c not in out:
            out.append(c)
    return [pair(*c) for c in out]


# ------------------------------------------------------------ set 1: read the coordinates of a point
def set_read(rnd, P):
    its = []
    reads = [
        [(3, 5, "A")], [(6, 2, "B")], [(2, 7, "C"), (5, 4, "D")], [(8, 3, "P"), (3, 8, "Q")],
        [(1, 4, "F"), (4, 1, "E")], [(7, 6, "G")], [(5, 9, "H"), (9, 5, "J")], [(1, 3, "K")],
        [(9, 7, "M"), (4, 2, "N")], [(6, 8, "R")],
    ]
    for i, pts in enumerate(reads):
        x, y, n = pts[0]
        e = "%s. Point %s is at %s. The x-coordinate (across) always comes first." % (walk(x, y), n, pair(x, y))
        if (y, x) in [(p[0], p[1]) for p in pts[1:]]:
            e += " %s is point %s: the numbers are switched." % (pair(y, x), pts[1][2])
        its.append(mcq(fig(pts_grid(pts, "coordinate grid with labeled points")) +
                       "What are the coordinates of point %s?" % n, pair(x, y), read_cands(x, y, i), e, rnd))
    one = [
        ([(7, 4, "S")], "x", 7, [4, 8, 6],
         "The x-coordinate tells how far to go across. Point S is 7 units to the right of the origin, so x = 7. (4 is its y-coordinate.)"),
        ([(3, 6, "T")], "y", 6, [3, 7, 5],
         "The y-coordinate tells how far to go up. Point T is 6 units up from the x-axis, so y = 6. (3 is its x-coordinate.)"),
        ([(5, 2, "U"), (2, 5, "V")], "x", 5, [2, 6, 4],
         "Point U is 5 units to the right of the origin, so its x-coordinate is 5. Point V is the one at (2, 5)."),
        ([(8, 5, "W")], "y", 5, [8, 6, 4],
         "Point W is 5 units up, so its y-coordinate is 5. Its x-coordinate is 8: W is at (8, 5)."),
    ]
    for pts, ax, ans, wrong, e in one:
        its.append(mcq_num(fig(pts_grid(pts, "coordinate grid with labeled points")) +
                           "What is the %s-coordinate of point %s?" % (ax, pts[0][2]), ans, wrong, e))
    its.append(mcq("In an ordered pair, which coordinate comes first?", "the x-coordinate",
                   ["the y-coordinate", "the larger number", "the smaller number"],
                   "An ordered pair is always written (x, y). The x-coordinate (how far across) comes first, then the y-coordinate (how far up).", rnd))
    its.append(mcq("Which axis goes across, from left to right?", "the x-axis", ["the y-axis", "both axes", "neither axis"],
                   "The x-axis goes across. The y-axis goes up. They meet at the origin, (0, 0).", rnd))
    its.append(mcq("In the ordered pair (6, 2), what does the 6 tell you?", "Go right 6 from the origin",
                   ["Go up 6 from the origin", "Go right 2 from the origin", "Go up 2 from the origin"],
                   "The first number is the x-coordinate. It tells how far to go right from the origin: right 6.", rnd))
    its.append(mcq("In the ordered pair (6, 2), what does the 2 tell you?", "Go up 2", ["Go right 2", "Go up 6", "Go right 6"],
                   "The second number is the y-coordinate. It tells how far to go up: up 2.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s starts at the origin. %s goes right 4, then up 9. Which ordered pair names %s point?" % (n, he.capitalize(), his),
                   "(4, 9)", ["(9, 4)", "(5, 10)", "(4, 0)"],
                   "Right 4 gives x = 4, and up 9 gives y = 9. Write x first: (4, 9).", rnd))
    its.append(mcq("To plot the point (5, 3), what do you do first from the origin?", "Go right 5", ["Go up 5", "Go right 3", "Go up 3"],
                   "The first number, 5, is the x-coordinate. Go right 5 along the x-axis first, then up 3.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Read the coordinates of a point", "items": its}


# ------------------------------------------------------------ set 2: find the point for an ordered pair
def decoys(x, y, i):
    """Points students pick by mistake for (x, y): switched, counted from 1, next grid line."""
    near = [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
    near = near[i % 4:] + near[:i % 4]
    out = []
    for c in [(y, x), (x + 1, y + 1)] + near:
        if c != (x, y) and min(c) >= 0 and c not in out:
            out.append(c)
    return out[:3]


def pick_letters(target, others, pos):
    """Returns the 4 points with letters A-D (target at the next position) and the answer letter."""
    p = pos.next()
    cells = list(others)
    cells.insert(p, target)
    return [(c[0], c[1], "ABCD"[k]) for k, c in enumerate(cells)], "ABCD"[p]


def set_plot(rnd, P):
    its = []
    pos = Pos(rnd)
    targets = [(3, 7), (5, 2), (1, 6), (8, 4), (4, 9), (6, 3), (2, 5), (7, 1), (9, 6), (2, 8)]
    for i, (x, y) in enumerate(targets):
        pts, ans = pick_letters((x, y), decoys(x, y, i), pos)
        where = {(p[0], p[1]): p[2] for p in pts}
        e = "%s: that is point %s." % (walk(x, y), ans)
        if (y, x) in where:
            e += " Point %s is at %s: the numbers are switched." % (where[(y, x)], pair(y, x))
        its.append(mcq_fixed(fig(pts_grid(pts, "coordinate grid with points A to D")) +
                             "Which point is at %s?" % pair(x, y), ["A", "B", "C", "D"], ans, e))
    for x, y, ax, others, e in [
        (5, 2, "x", [(2, 5), (6, 5), (4, 3)],
         "The x-coordinate is the first number: how far across. Point {a} is 5 units to the right, at (5, 2). The point at (2, 5) has a y-coordinate of 5, not an x-coordinate of 5."),
        (6, 3, "y", [(3, 6), (3, 1), (5, 4)],
         "The y-coordinate is the second number: how far up. Point {a} is 3 units up, at (6, 3). The point at (3, 6) has an x-coordinate of 3."),
    ]:
        pts, ans = pick_letters((x, y), others, pos)
        its.append(mcq_fixed(fig(pts_grid(pts, "coordinate grid with points A to D")) +
                             "Which point has a%s %s-coordinate of %d?" % ("n" if ax == "x" else "", ax, x if ax == "x" else y),
                             ["A", "B", "C", "D"], ans, e.format(a=ans)))
    n, he, his = P.next()
    its.append(mcq(fig(pts_grid([(3, 6, "B")], "coordinate grid with point B")) +
                   "%s says point B is at (6, 3). What mistake did %s make?" % (n, he),
                   "%s switched x and y" % he.capitalize(),
                   ["%s counted from 1, not 0" % he.capitalize(), "%s read the wrong point" % he.capitalize(), "No mistake. %s is right" % he.capitalize()],
                   "Point B is 3 units right and 6 units up, so it is at (3, 6). %s wrote the up number first." % n, rnd))
    n, he, his = P.next()
    its.append(mcq(fig(pts_grid([(4, 2, "E")], "coordinate grid with point E")) +
                   "%s says point E is at (5, 3). What mistake did %s make?" % (n, he),
                   "%s counted from 1, not 0" % he.capitalize(),
                   ["%s switched x and y" % he.capitalize(), "%s went left, not right" % he.capitalize(), "No mistake. %s is right" % he.capitalize()],
                   "Point E is at (4, 2). %s counted the first grid line as 1, so both numbers came out 1 too big. Count the spaces from the origin, which is 0." % n, rnd))
    its.append(mcq("Are (2, 5) and (5, 2) the same point?", "No, they are different points",
                   ["Yes, they use the same numbers", "Yes, order does not matter", "Only on a small grid"],
                   "(2, 5) is right 2, up 5. (5, 2) is right 5, up 2. The order of the numbers changes where the point is.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s wants to plot (7, 1). %s goes up 7, then right 1. Which point did %s plot by mistake?" % (n, he.capitalize(), he),
                   "(1, 7)", ["(7, 1)", "(8, 2)", "(7, 7)"],
                   "Going right 1 and up 7 lands on (1, 7). To plot (7, 1), go right 7 first, then up 1.", rnd))
    its.append(mcq("Which point is farther to the right: (2, 9) or (6, 1)?", "(6, 1)", ["(2, 9)", "They are the same", "You cannot tell"],
                   "How far right a point is depends on the x-coordinate, the first number. 6 is more than 2, so (6, 1) is farther right.", rnd))
    its.append(mcq("Which point is higher on the grid: (8, 3) or (2, 5)?", "(2, 5)", ["(8, 3)", "They are the same", "You cannot tell"],
                   "How high a point is depends on the y-coordinate, the second number. 5 is more than 3, so (2, 5) is higher.", rnd))
    its.append(mcq("Which point is straight above (4, 2)?", "(4, 6)", ["(6, 2)", "(2, 4)", "(6, 4)"],
                   "Points straight above each other have the same x-coordinate. (4, 6) has x = 4, the same as (4, 2), and a bigger y.", rnd))
    its.append(mcq("Which point is straight to the right of (1, 5)?", "(7, 5)", ["(1, 7)", "(5, 1)", "(7, 1)"],
                   "Points straight across from each other have the same y-coordinate. (7, 5) has y = 5, the same as (1, 5), and a bigger x.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Find the point for an ordered pair", "items": its}


# ------------------------------------------------------------ set 3: points on the axes and the origin
WHERE = ["on the x-axis", "on the y-axis", "at the origin", "on neither axis"]


def set_axes(rnd, P):
    its = []
    pos = Pos(rnd)
    reads = [
        ([(0, 5, "A")], [(5, 0), (1, 5), (0, 6)],
         "Point A is on the y-axis, so it did not move right at all: x = 0. Go up 5: (0, 5)."),
        ([(6, 0, "B"), (2, 4, "C")], [(0, 6), (6, 1), (7, 0)],
         "Point B is on the x-axis. Go right 6 and up 0: (6, 0). A point on the x-axis always has y = 0."),
        ([(0, 0, "M"), (3, 4, "N")], [(1, 1), (0, 1), (1, 0)],
         "Point M is at the origin, where the axes meet. It is 0 right and 0 up: (0, 0)."),
        ([(0, 8, "K"), (3, 2, "J")], [(8, 0), (1, 8), (0, 9)],
         "Point K is on the y-axis, 8 units up. Its x-coordinate is 0: (0, 8). (8, 0) would be on the x-axis."),
        ([(9, 0, "R")], [(0, 9), (9, 1), (10, 0)],
         "Point R is on the x-axis, 9 units right. It does not go up, so y = 0: (9, 0)."),
        ([(0, 2, "T"), (2, 0, "S")], [(2, 0), (1, 2), (0, 3)],
         "Point T is on the y-axis, 2 units up: (0, 2). Point S is at (2, 0), on the x-axis."),
    ]
    for pts, wrong, e in reads:
        x, y, n = pts[0]
        G = Grid(max(5, max(p[0] for p in pts) + 1), max(5, max(p[1] for p in pts) + 1))
        for p in pts:
            G.point(*p)
        its.append(mcq(fig(G.svg("coordinate grid with points on the axes")) + "What are the coordinates of point %s?" % n,
                       pair(x, y), [pair(*w) for w in wrong], e, rnd))
    for (x, y), ans, e in [
        ((0, 7), "on the y-axis", "x = 0 means the point does not move right. It goes straight up the y-axis to 7."),
        ((6, 0), "on the x-axis", "y = 0 means the point does not move up. It stays on the x-axis at 6."),
        ((0, 0), "at the origin", "Both coordinates are 0, so the point does not move at all. It is the origin."),
        ((3, 3), "on neither axis", "Neither coordinate is 0, so the point is inside the grid: right 3 and up 3."),
    ]:
        its.append(mcq_fixed("Where is the point %s?" % pair(x, y), WHERE, ans, e))
    for ax, tgt, others, e in [
        ("y", (0, 4), [(4, 0), (1, 3), (3, 2)],
         "is at (0, 4). Its x-coordinate is 0, so it sits on the y-axis. The point at (4, 0) is on the x-axis, and the point at (1, 3) is 1 unit to the right of the y-axis."),
        ("x", (5, 0), [(0, 5), (4, 1), (2, 3)],
         "is at (5, 0). Its y-coordinate is 0, so it sits on the x-axis. The point at (0, 5) is on the y-axis, and the point at (4, 1) is 1 unit above the x-axis."),
    ]:
        pts, ans = pick_letters(tgt, others, pos)
        its.append(mcq_fixed(fig(pts_grid(pts, "coordinate grid with points A to D")) +
                             "Which point is on the %s-axis?" % ax, ["A", "B", "C", "D"], ans, "Point %s %s" % (ans, e)))
    its.append(mcq("Which point is on the x-axis?", "(4, 0)", ["(0, 4)", "(4, 4)", "(4, 1)"],
                   "Points on the x-axis do not go up, so their y-coordinate (the second number) is 0: (4, 0).", rnd))
    its.append(mcq("Which point is on the y-axis?", "(0, 9)", ["(9, 0)", "(9, 9)", "(1, 9)"],
                   "Points on the y-axis do not go right, so their x-coordinate (the first number) is 0: (0, 9).", rnd))
    its.append(mcq("Every point on the x-axis has the same y-coordinate. What is it?", "0", ["1", "the same as x", "10"],
                   "Points on the x-axis do not go up at all, so y = 0. Examples: (3, 0), (7, 0).", rnd))
    its.append(mcq("Every point on the y-axis has the same x-coordinate. What is it?", "0", ["1", "the same as y", "10"],
                   "Points on the y-axis do not go right at all, so x = 0. Examples: (0, 2), (0, 8).", rnd))
    its.append(mcq("What are the coordinates of the origin?", "(0, 0)", ["(1, 1)", "(0, 1)", "(1, 0)"],
                   "The origin is where the axes meet. It is the 0 on both number lines, so it is (0, 0).", rnd))
    its.append(mcq("What is the point where the x-axis and the y-axis meet called?", "the origin",
                   ["the ordered pair", "the x-coordinate", "the y-axis"],
                   "The axes meet at the origin, (0, 0). Every point is found by starting there.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s says (0, 5) is on the x-axis because it has a 0 first. Is %s right?" % (n, he),
                   "No, it is on the y-axis", ["Yes, x = 0 means the x-axis", "Yes, every 0 is on the x-axis", "No, it is at the origin"],
                   "x = 0 means the point does not move right, so it stays on the y-axis and goes up 5. Points on the x-axis have y = 0.", rnd))
    its.append(mcq("A point starts at the origin and moves up 4. What are its coordinates now?", "(0, 4)", ["(4, 0)", "(4, 4)", "(1, 4)"],
                   "It did not move right, so x = 0. It moved up 4, so y = 4: (0, 4), on the y-axis.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Points on the axes and the origin", "items": its}


# ------------------------------------------------------------ set 4: distance, moves and shapes
def dist_e(a, b):
    if a[0] == b[0]:
        lo, hi = sorted([a[1], b[1]])
        return ("Both points have x = %d, so they are on the same up-and-down line. Subtract the y-coordinates: %d − %d = %d units. "
                "Count spaces, not dots." % (a[0], hi, lo, hi - lo)), hi - lo
    lo, hi = sorted([a[0], b[0]])
    return ("Both points have y = %d, so they are on the same across line. Subtract the x-coordinates: %d − %d = %d units. "
            "Count spaces, not dots." % (a[1], hi, lo, hi - lo)), hi - lo


def set_distance(rnd, P):
    its = []
    pos = Pos(rnd)
    for a, b, na, nb, wrong in [
        ((2, 3), (2, 8), "A", "B", [6, 8, 11]),
        ((1, 4), (7, 4), "A", "B", [7, 4, 8]),
        ((6, 1), (6, 9), "M", "N", [9, 6, 10]),
        ((2, 5), (9, 5), "C", "D", [8, 5, 11]),
    ]:
        e, d = dist_e(a, b)
        G = grid_for([a, b])
        G.seg(a, b)
        G.point(a[0], a[1], na)
        G.point(b[0], b[1], nb)
        its.append(mcq_num(fig(G.svg("coordinate grid with a line segment")) +
                           "How many units long is line segment %s%s?" % (na, nb), d, wrong, e))
    e, d = dist_e((3, 2), (3, 10))
    its.append(mcq_num("How many units is it from (3, 2) to (3, 10)?", d, [9, 12, 10], e))
    e, d = dist_e((1, 6), (8, 6))
    its.append(mcq_num("A line segment goes from (1, 6) to (8, 6). How long is it?", d, [8, 9, 6], e))
    n, he, his = P.next()
    its.append(mcq_num("%s finds the distance from (5, 2) to (5, 9). %s counts the dots on the grid line and gets 8. What is the real distance?"
                       % (n, he.capitalize()), 7, [8, 9, 11],
                       "Distance is the number of spaces between the points: 9 − 2 = 7. Counting dots counts the starting point too, so it gives 1 too many."))
    its.append(mcq("Point A is at (3, 4). It moves 2 units to the right. Where is it now?", "(5, 4)", ["(3, 6)", "(5, 6)", "(1, 4)"],
                   "Moving right changes only x: 3 + 2 = 5. The y-coordinate stays 4: (5, 4).", rnd))
    its.append(mcq("Point B is at (6, 2). It moves 5 units up. Where is it now?", "(6, 7)", ["(11, 2)", "(11, 7)", "(7, 6)"],
                   "Moving up changes only y: 2 + 5 = 7. The x-coordinate stays 6: (6, 7).", rnd))
    its.append(mcq("Point C is at (2, 5). It moves 4 units right and 3 units down. Where is it now?", "(6, 2)",
                   ["(6, 8)", "(5, 1)", "(2, 6)"],
                   "Right 4 changes x: 2 + 4 = 6. Down 3 changes y: 5 − 3 = 2. The new point is (6, 2).", rnd))
    its.append(mcq("Point A is at (4, 7). Point B is 3 units straight to the left of A. What are the coordinates of B?", "(1, 7)",
                   ["(7, 7)", "(4, 4)", "(4, 10)"],
                   "Left means x gets smaller: 4 − 3 = 1. Straight left means y stays 7: (1, 7).", rnd))
    for (p, n_, dx, dy, words, others, e) in [
        ((2, 3), "P", 4, 0, "4 units to the right of", [(2, 7), (7, 3), (6, 7)],
         "is at (6, 3): x grows by 4 (2 + 4 = 6) and y stays 3. The point at (2, 7) is 4 units up, not right."),
        ((5, 6), "P", 0, -3, "3 units below", [(5, 9), (2, 6), (5, 2)],
         "is at (5, 3): y gets smaller by 3 (6 − 3 = 3) and x stays 5. The point at (5, 9) is 3 units above, and (5, 2) is 4 units below."),
    ]:
        tgt = (p[0] + dx, p[1] + dy)
        pts, ans = pick_letters(tgt, others, pos)
        G = grid_for([p] + [q[:2] for q in pts], lo=6)
        G.point(p[0], p[1], n_, RED)
        for q in pts:
            G.point(*q)
        its.append(mcq_fixed(fig(G.svg("coordinate grid with point P and points A to D")) +
                             "Which point is %s point P?" % words, ["A", "B", "C", "D"], ans, "Point %s %s" % (ans, e)))
    for A, B, C, D, wrong in [
        ((1, 2), (6, 2), (6, 5), (1, 5), [(5, 1), (1, 6), (2, 5)]),
        ((2, 1), (2, 7), (5, 7), (5, 1), [(1, 5), (2, 5), (5, 2)]),
        ((3, 2), (7, 2), (7, 6), (3, 6), [(6, 3), (3, 7), (4, 6)]),
    ]:
        G = grid_for([A, B, C, D], lo=6)
        G.seg(A, B).seg(B, C)
        G.point(A[0], A[1], "A").point(B[0], B[1], "B").point(C[0], C[1], "C")
        same_x = "A" if D[0] == A[0] else "C"
        same_y = "C" if same_x == "A" else "A"
        e = ("D is in line with %s up and down, so x = %d. It is in line with %s across, so y = %d. D is at %s."
             % (same_x, D[0], same_y, D[1], pair(*D)))
        kind = "square" if abs(A[0] - B[0]) + abs(A[1] - B[1]) == abs(B[0] - C[0]) + abs(B[1] - C[1]) else "rectangle"
        its.append(mcq(fig(G.svg("coordinate grid with three corners of a " + kind)) +
                       "A, B and C are 3 corners of a %s. What are the coordinates of the 4th corner, D?" % kind,
                       pair(*D), [pair(*w) for w in wrong], e, rnd))
    its.append(mcq_num("A rectangle has corners at (1, 1), (6, 1), (6, 4) and (1, 4). What is its perimeter in units?", 16, [8, 15, 20],
                       "The bottom side goes from x = 1 to x = 6: 5 units. The left side goes from y = 1 to y = 4: 3 units. "
                       "Perimeter = 5 + 3 + 5 + 3 = 16 units."))
    its.append(mcq_num("A rectangle has corners at (2, 1), (7, 1), (7, 5) and (2, 5). What is its area in square units?", 20, [18, 9, 35],
                       "The length is 7 − 2 = 5 units and the width is 5 − 1 = 4 units. Area = 5 × 4 = 20 square units."))
    its.append(mcq("Which point is on the same up-and-down line as (3, 5)?", "(3, 1)", ["(1, 3)", "(5, 3)", "(1, 5)"],
                   "Points on the same up-and-down line have the same x-coordinate. (3, 1) has x = 3. "
                   "(1, 5) is on the same across line instead.", rnd))
    G = Grid(7, 7)
    G.point(1, 2, "A").point(6, 6, "B")
    n, he, his = P.next()
    its.append(mcq_num(fig(G.svg("coordinate grid with points A and B")) +
                       "%s walks only along grid lines from A to B. What is the shortest number of units %s can walk?" % (n, he),
                       9, [5, 4, 6],
                       "A is at (1, 2) and B is at (6, 6). Go right 6 − 1 = 5 units and up 6 − 2 = 4 units. 5 + 4 = 9 units."))
    assert len(its) == 20, len(its)
    return {"title": "Distance, moves and shapes on the grid", "items": its}


# ------------------------------------------------------------ set 5: real-world graphs
def park_grid():
    G = Grid(8, 8)
    for x, y, n in [(4, 0, "G"), (4, 4, "F"), (7, 7, "P"), (2, 7, "S"), (7, 2, "B")]:
        G.point(x, y, n)
    return fig(G.svg("coordinate grid map of a park"))


def town_grid():
    G = Grid(10, 7)
    for x, y, n in [(3, 1, "H"), (3, 6, "S"), (9, 6, "L"), (6, 3, "C")]:
        G.point(x, y, n)
    return fig(G.svg("coordinate grid map of a town"))


def earn_grid():
    G = Grid(6, 5, sy=8, xt="Hours worked", yt="Dollars earned")
    for h in range(1, 5):
        G.data_point(h, 8 * h, None)
    return G


def plant_grid():
    G = Grid(6, 6, sy=2, xt="Week", yt="Height (cm)")
    for w in range(0, 5):
        G.data_point(w, 2 + 2 * w, None)
    return G


def set_real(rnd, P):
    its = []
    park = park_grid()
    key = "The map shows a park. G = gate, F = fountain, P = pond, S = slide, B = bench. "
    its.append(mcq(park + key + "What are the coordinates of the pond?", "(7, 7)", ["(8, 8)", "(7, 6)", "(6, 7)"],
                   "Start at the origin. Go right 7, then up 7. The pond is at (7, 7).", rnd))
    its.append(mcq(park + key + "Which place is at (7, 2)?", "the bench", ["the slide", "the pond", "the fountain"],
                   "Go right 7, then up 2: that is B, the bench. The slide is at (2, 7): the numbers are switched.", rnd))
    n, he, his = P.next()
    its.append(mcq_num(park + key + "%s walks from the gate straight up to the fountain. How many units does %s walk?" % (n, he),
                       4, [5, 3, 8],
                       "The gate is at (4, 0) and the fountain is at (4, 4). Same x, so subtract the y-coordinates: 4 − 0 = 4 units."))
    its.append(mcq_num(park + key + "How many units is it from the slide straight across to the pond?", 5, [6, 7, 9],
                       "The slide is at (2, 7) and the pond is at (7, 7). Same y, so subtract the x-coordinates: 7 − 2 = 5 units."))
    its.append(mcq(park + key + "A picnic table will go 3 units to the right of the fountain. Where will it be?", "(7, 4)",
                   ["(4, 7)", "(7, 7)", "(1, 4)"],
                   "The fountain is at (4, 4). Right 3 changes only x: 4 + 3 = 7. The table will be at (7, 4).", rnd))
    town = town_grid()
    n, he, his = P.next()
    tkey = "The map shows where %s lives. H = home, S = school, L = library, C = café. Each unit is 1 block. " % n
    its.append(mcq(town + tkey + "What are the coordinates of the library?", "(9, 6)", ["(6, 9)", "(10, 7)", "(9, 5)"],
                   "Start at the origin. Go right 9, then up 6. The library is at (9, 6).", rnd))
    its.append(mcq_num(town + tkey + "%s walks from home straight up to school. How many blocks does %s walk?" % (n, he), 5, [6, 3, 7],
                       "Home is at (3, 1) and school is at (3, 6). Same x, so subtract: 6 − 1 = 5 blocks."))
    its.append(mcq_num(town + tkey + "After school, %s walks straight across to the library. How many blocks is that?" % he, 6, [7, 9, 12],
                       "School is at (3, 6) and the library is at (9, 6). Same y, so subtract: 9 − 3 = 6 blocks."))
    its.append(mcq_num(town + tkey + "%s walks from home to the library along the streets (the grid lines). What is the shortest number of blocks?" % n,
                       11, [6, 5, 15],
                       "Home is at (3, 1) and the library is at (9, 6). Go right 9 − 3 = 6 blocks and up 6 − 1 = 5 blocks. 6 + 5 = 11 blocks."))
    earn = fig(earn_grid().svg("graph of hours worked and dollars earned"))
    n, he, his = P.next()
    ek = "%s earns the same amount for each hour %s works. The graph shows (hours worked, dollars earned). " % (n, he)
    its.append(mcq(earn + ek + "What does the point (3, 24) mean?", "%s earns $24 in 3 hours." % he.capitalize(),
                   ["%s earns $3 in 24 hours." % he.capitalize(), "%s earns $24 each hour." % he.capitalize(),
                    "%s works 3 hours and 24 minutes." % he.capitalize()],
                   "The first number is on the x-axis: hours worked. The second number is on the y-axis: dollars earned. So in 3 hours %s earns $24." % he, rnd))
    its.append(mcq_num(earn + ek + "How much does %s earn in 2 hours?" % he, 16, [8, 24, 2],
                       "Find 2 on the x-axis and go up to the point. It is at 16 on the y-axis, which counts by 8: $16. "
                       "(2 is the hours, not the dollars.)", fmt="$%d"))
    its.append(mcq_num(earn + ek + "How much does %s earn for each hour?" % he, 8, [1, 16, 32],
                       "The point (1, 8) shows $8 for 1 hour. Each hour adds $8: 8, 16, 24, 32.", fmt="$%d"))
    its.append(mcq(earn + ek + "If the pattern continues, which point comes next?", "(5, 40)", ["(40, 5)", "(6, 40)", "(5, 32)"],
                   "The hours go up by 1 and the dollars go up by 8. After (4, 32) comes (4 + 1, 32 + 8) = (5, 40).", rnd))
    its.append(mcq(earn + ek + "Working 0 hours earns $0. Which point shows this?", "(0, 0)", ["(1, 0)", "(0, 1)", "(0, 8)"],
                   "0 hours is x = 0 and $0 is y = 0. That point is the origin, (0, 0).", rnd))
    plant = fig(plant_grid().svg("graph of a plant's height each week"))
    pk = "The graph shows the height of a plant each week, as (week, height in cm). "
    its.append(mcq(plant + pk + "What does the point (0, 2) mean?", "At the start, the plant was 2 cm tall.",
                   ["After 2 weeks, the plant was 0 cm tall.", "The plant grew 2 cm each week.", "The plant did not grow."],
                   "Week 0 is the start. The y-coordinate, 2, is the height. So the plant was 2 cm tall when the graph started.", rnd))
    its.append(mcq_num(plant + pk + "How tall was the plant at week 3?", 8, [3, 6, 10],
                       "Find 3 on the x-axis and go up to the point. It is at 8 on the y-axis, which counts by 2: 8 cm.", fmt="%d cm"))
    its.append(mcq_num(plant + pk + "How many centimeters does the plant grow each week?", 2, [4, 1, 6],
                       "Each week the point is 1 grid space higher. On this y-axis 1 space is 2 cm, so the plant grows 2 cm: 2, 4, 6, 8, 10.",
                       fmt="%d cm"))
    its.append(mcq(plant + pk + "If the pattern continues, which point shows week 5?", "(5, 12)", ["(12, 5)", "(5, 10)", "(6, 12)"],
                   "Each week the height goes up 2 cm. At week 4 it is 10 cm, so at week 5 it is 12 cm: (5, 12). The week comes first.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s reads 15 pages each day. %s table shows the total pages read so far: Day 1: 15, Day 2: 30, Day 3: 45. %s plots each row as (day, pages). "
                   "Which point does %s plot for Day 2?" % (n, his.capitalize(), he.capitalize(), he),
                   "(2, 30)", ["(30, 2)", "(2, 15)", "(3, 45)"],
                   "The day comes first and the pages come second. Day 2 has 30 pages: (2, 30).", rnd))
    n, he, his = P.next()
    its.append(mcq("Tickets cost $4 each. %s graphs (number of tickets, total cost). Which point is on %s graph?" % (n, his),
                   "(3, 12)", ["(12, 3)", "(3, 7)", "(4, 12)"],
                   "3 tickets cost 3 × 4 = $12, so the point is (3, 12). The number of tickets comes first. (4 tickets would cost $16.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Real-world maps and graphs", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    G = Grid(7, 7)
    G.arrow((0, 0), (3, 0)).arrow((3, 0), (3, 5))
    G.note(1.5, 0.5, "right 3").note(3.25, 2.5, "up 5", anchor="start")
    G.point(3, 5, "A")
    plot = G.svg("coordinate grid: from the origin go right 3, then up 5 to point A at (3, 5)")
    G = Grid(6, 6)
    G.point(0, 4, "C").point(5, 0, "D").point(0, 0, None, RED)
    G.note(0.4, 0.5, "origin", anchor="start")
    axes = G.svg("coordinate grid with point C on the y-axis and point D on the x-axis")
    G = Grid(6, 9)
    G.seg((2, 3), (2, 8)).point(2, 3, "A").point(2, 8, "B")
    G.note(2.25, 5.5, "5 units", anchor="start")
    dist = G.svg("line segment from A (2, 3) to B (2, 8), 5 units long")
    G = earn_grid()
    G.note(3.35, 3, "(3, 24)", anchor="start")
    earn = G.svg("graph of hours worked and dollars earned")
    return (
        "<h2>What a coordinate grid is</h2>"
        "<p>A coordinate grid is made of two number lines that cross at 0. The <b>x-axis</b> goes across. "
        "The <b>y-axis</b> goes up. They meet at the <b>origin</b>, (0, 0).</p>"
        "<p>An <b>ordered pair</b> (x, y) tells you how to get to a point from the origin: "
        "the first number says how far to go <b>right</b>, the second says how far to go <b>up</b>.</p>"
        "<figure class='sn-fig'>" + plot +
        "<figcaption>To plot (3, 5), start at the origin. Go right 3 along the x-axis, then up 5. Point A is at (3, 5).</figcaption></figure>" +
        ex("Example", "A point is 6 units to the right of the origin and 2 units up. What are its coordinates?",
           "Right 6 is the x-coordinate. Up 2 is the y-coordinate. Write x first.", "(6, 2)") +
        "<p>Order matters. (3, 5) and (5, 3) are different points.</p>"
        "<h2>Points on the axes</h2>"
        "<figure class='sn-fig'>" + axes +
        "<figcaption>The origin is (0, 0). C is at (0, 4): it does not go right, so it is on the y-axis. D is at (5, 0): it does not go up, so it is on the x-axis.</figcaption></figure>" +
        table(["Point", "Where it is", "Why"], [
            ["(0, 4)", "on the y-axis", "x = 0: no move to the right"],
            ["(5, 0)", "on the x-axis", "y = 0: no move up"],
            ["(0, 0)", "the origin", "no move at all"],
        ]) +
        "<h2>Distance along a grid line</h2>"
        "<p>If two points have the same x-coordinate, they are on the same up-and-down line. Subtract the y-coordinates. "
        "If they have the same y-coordinate, subtract the x-coordinates.</p>"
        "<figure class='sn-fig'>" + dist +
        "<figcaption>A (2, 3) and B (2, 8) have the same x. 8 − 3 = 5 units. Count the spaces, not the dots.</figcaption></figure>" +
        ex("Example", "How far is it from (1, 6) to (8, 6)?", "Same y, so subtract the x-coordinates: 8 − 1 = 7.", "7 units") +
        "<h2>Real-world graphs</h2>"
        "<p>Data from a table can be graphed as points. Each row of the table becomes one ordered pair. "
        "The axis titles tell what each number means.</p>" +
        table(["Hours worked (x)", "1", "2", "3", "4"], [["Dollars earned (y)", "8", "16", "24", "32"]]) +
        "<figure class='sn-fig'>" + earn +
        "<figcaption>The y-axis counts by 8. The point (3, 24) means: in 3 hours, $24 is earned.</figcaption></figure>" +
        ex("Example", "If the pattern continues, what point comes after (4, 32)?",
           "The hours go up by 1 and the dollars go up by 8: (4 + 1, 32 + 8).", "(5, 40)") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Switching the numbers: plotting (3, 7) at right 7, up 3", "Go right first (x), then up (y)"],
            ["Counting the first grid line as 1", "The origin is 0. Count the spaces from it"],
            ["Thinking (0, 5) is on the x-axis", "x = 0 means no move right, so it is on the y-axis"],
            ["Counting dots to find a distance", "Subtract the coordinates that change"],
            ["Ignoring the scale on a real-world graph", "Check what each axis counts by"],
        ])
    )


FAQ = [
    {"q": "How do you find the coordinates of a point?",
     "a": "Start at the origin. Count how far right the point is (the x-coordinate), then how far up (the y-coordinate), and write them as (x, y)."},
    {"q": "Which comes first in an ordered pair, x or y?",
     "a": "The x-coordinate always comes first. A helpful rule is “across, then up”: (4, 7) means right 4, up 7."},
    {"q": "What is the origin on a coordinate plane?",
     "a": "The origin is the point where the x-axis and the y-axis cross. Its coordinates are (0, 0), and every point is found by starting there."},
    {"q": "What is the first quadrant?",
     "a": "It is the top-right part of the coordinate plane, where both coordinates are 0 or greater. In Grade 5, students graph points only in the first quadrant."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions. Choices with a fixed order
    (A-D pictures, numbers, axis words) stay as they are; the other questions fill the gaps."""
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


def gen_coordinate_plane():
    rnd = random.Random(508)
    P = People(rnd)
    sets = [set_read(rnd, P), set_plot(rnd, P), set_axes(rnd, P), set_distance(rnd, P), set_real(rnd, P)]
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
    return {
        "country": "us", "subject": "math", "grade": "grade-5", "slug": "coordinate-plane", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "The Coordinate Plane: Ordered Pairs, Plotting Points and Real-World Graphs",
        "seo_title": "Grade 5 Coordinate Plane Worksheets: Ordered Pairs, Plotting Points in the First Quadrant (5.G.A.1-2)",
        "short_title": "Coordinate plane",
        "domain": "Geometry",
        "standard_code": "5.G.A.1–2",
        "standard_url": "https://www.thecorestandards.org/Math/Content/5/G/A/",
        "standard_text": "Use a pair of perpendicular number lines, called axes, to define a coordinate system, with the intersection of the lines (the origin) arranged to coincide with the 0 on each line and a given point in the plane located by using an ordered pair of numbers, called its coordinates. Understand that the first number indicates how far to travel from the origin in the direction of one axis, and the second number indicates how far to travel in the direction of the second axis. Represent real world and mathematical problems by graphing points in the first quadrant of the coordinate plane, and interpret coordinate values of points in the context of the situation.",
        "meta_desc": "Free Grade 5 coordinate plane worksheets: read and plot ordered pairs in the first quadrant, points on the x-axis and y-axis, the origin, distance along a grid line, the 4th corner of a rectangle, and real-world maps and graphs. 100 practice questions with answers.",
        "key_big": "An ordered pair (x, y) is a set of directions from the origin: go right x, then up y.",
        "key_sub": "The x-coordinate always comes first, so (3, 7) and (7, 3) are different points. A point with x = 0 is on the y-axis, and a point with y = 0 is on the x-axis.",
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
    u = gen_coordinate_plane()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "(coordinate grid|graph of)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
