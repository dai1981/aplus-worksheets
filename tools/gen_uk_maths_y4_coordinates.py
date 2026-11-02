# -*- coding: utf-8 -*-
"""
UK Year 4 Maths: Coordinates and translations (National Curriculum in England,
Year 4: Geometry - position and direction)
  python3 tools/gen_uk_maths_y4_coordinates.py
HTML attributes use single quotes (no backslashes in the JSON).

First quadrant only, whole-number coordinates 0-10. British English.
Every grid is drawn exactly: a point (x, y) sits on the crossing x squares along from the origin
and y squares up. Each letter label sits in the middle of a grid square next to its own point,
never in a square that touches another point and never on another label or note (checked in Grid.render).
Wrong answers come from real Year 4 mistakes: swapping x and y, counting grid lines including the
start (answers 1 too big), moving the wrong way in a translation (left for right, down for up),
changing only one coordinate, applying the "right" move to the y-coordinate.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
BLUE = "#1f5fa8"
INK = "#2b2b2b"
GRID = "#c9d3cc"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
LETTERS = ["A", "B", "C", "D"]


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
    """Choices keep their order (A B C D, numbers from small to large, shape names)."""
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
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs, bold=False):
    """Approximate text width in px (Arial)."""
    return len(str(t)) * fs * (0.62 if bold else 0.58)


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK, extra=""):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, extra, t))


def pair(x, y):
    return "(%d, %d)" % (x, y)


def sq(n):
    return "%d square%s" % (n, "" if n == 1 else "s")


def inside(p):
    return 0 <= p[0] <= 10 and 0 <= p[1] <= 10


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
    """First-quadrant grid from 0 to nx across and 0 to ny up. One square = u px."""

    def __init__(self, nx, ny, u=22, title=None):
        assert 1 <= nx <= 10 and 1 <= ny <= 10
        self.nx, self.ny, self.u, self.title = nx, ny, u, title
        left = tw(ny, 14) + 15
        top = 30 + (24 if title else 0)
        self.ox, self.oy = left, top + ny * u
        self.W = int(math.ceil(self.ox + nx * u + 28))
        self.H = int(math.ceil(self.oy + 26))
        if title:
            self.W = max(self.W, int(tw(title, 15, True) + 16))
        self.pts, self.segs, self.arrows, self.notes = [], [], [], []

    def P(self, x, y):
        return (self.ox + x * self.u, self.oy - y * self.u)

    def point(self, x, y, name, col=GREEN, where=None):
        assert x == int(x) and y == int(y) and 0 <= x <= self.nx and 0 <= y <= self.ny, (x, y)
        assert all((p[0], p[1]) != (x, y) for p in self.pts), ("two points at the same spot", x, y)
        self.pts.append((x, y, name, col, where))
        return self

    def seg(self, a, b, col=GREEN, w=3):
        assert a[0] == b[0] or a[1] == b[1], "only grid-line segments"
        self.segs.append((a, b, col, w))
        return self

    def rect(self, x0, y0, x1, y1, col=GREEN):
        c = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        for i in range(4):
            self.seg(c[i], c[(i + 1) % 4], col)
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
        xe, ye = ox + nx * u + 12, oy - ny * u - 12
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (ox, oy, xe - 4, oy, INK))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (ox, oy, ox, ye + 4, INK))
        s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (xe, oy, xe - 9, oy - 4.5, xe - 9, oy + 4.5, INK))
        s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (ox, ye, ox - 4.5, ye + 9, ox + 4.5, ye + 9, INK))
        s.append(text(xe + 4, oy + 5, "x", 15, anchor="start", bold=True, extra=" font-style='italic'"))
        s.append(text(ox, ye - 6, "y", 15, bold=True, extra=" font-style='italic'"))
        for k in range(1, nx + 1):
            s.append(text(ox + k * u, oy + 18, k, 14))
        for k in range(1, ny + 1):
            s.append(text(ox - 9, oy - k * u + 5, k, 14, anchor="end"))
        s.append(text(ox - 9, oy + 18, 0, 14, anchor="end"))
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
                s.append(text(lc[0], lc[1] + 5.8, name, 16, bold=True, col=RED if col == RED else INK))
        return "".join(s)

    def svg(self, label="coordinate grid"):
        return svg_wrap(self.W, self.H, self.render(), label)


def grid_for(pts, extra=1, lo=5):
    """Grid just big enough for the points (smaller grids print larger)."""
    nx = min(10, max(lo, max(p[0] for p in pts) + extra))
    ny = min(10, max(lo, max(p[1] for p in pts) + extra))
    return Grid(nx, ny)


def pts_grid(pts, label="coordinate grid", ref=None, lo=5):
    """pts: (x, y, name). ref: name of a point drawn in red (the starting point)."""
    G = grid_for(pts, lo=lo)
    for x, y, n in pts:
        G.point(x, y, n, RED if n == ref else GREEN)
    return G.svg(label)


def pick_letters(target, others, pos):
    """The 4 points with letters A-D (target at the next position) and the answer letter."""
    p = pos.next()
    cells = list(others)
    cells.insert(p, target)
    assert len(set(cells)) == 4 and all(inside(c) for c in cells), cells
    return [(c[0], c[1], LETTERS[k]) for k, c in enumerate(cells)], LETTERS[p]


# ------------------------------------------------------------ explanations and mistakes
def walk(x, y):
    if x == 0 and y == 0:
        return "It is the origin: 0 along and 0 up"
    return "Start at (0, 0). Go along %d, then up %d" % (x, y)


def read_cands(x, y, i):
    """Swapped, counted the lines including the start (+1 each), then the next grid line."""
    near = [(x, y + 1), (x + 1, y), (x - 1, y), (x, y - 1)]
    near = near[i % 4:] + near[:i % 4]
    out = []
    for c in [(y, x), (x + 1, y + 1)] + near:
        if c != (x, y) and min(c) >= 0 and c not in out:
            out.append(c)
    return [pair(*c) for c in out]


def mv(dx, dy):
    parts = []
    if dx:
        parts.append("%d %s" % (abs(dx), "right" if dx > 0 else "left"))
    if dy:
        parts.append("%d %s" % (abs(dy), "up" if dy > 0 else "down"))
    return ", ".join(parts)


def mv_long(dx, dy):
    parts = []
    if dx:
        parts.append("%s %s" % (sq(abs(dx)), "right" if dx > 0 else "left"))
    if dy:
        parts.append("%s %s" % (sq(abs(dy)), "up" if dy > 0 else "down"))
    return " and ".join(parts)


def sgn(v):
    return (v > 0) - (v < 0)


def move_cands(p, dx, dy, i=0):
    """Where pupils land by mistake: wrong way, x/y mixed up, only one number changed."""
    x, y = p
    c = [(x - dx, y + dy), (x + dy, y + dx), (x + dx, y), (x, y + dy), (x + dx, y - dy), (x - dx, y - dy)]
    c = c[i % 3:] + c[:i % 3]
    # backups: counted the lines (1 too far), the answer written the wrong way round
    c += [(x + dx + sgn(dx), y + dy + sgn(dy)), (y + dy, x + dx)]
    return [q for q in c if inside(q) and q != (x + dx, y + dy) and q != (x, y)]


def describe_cands(dx, dy, i=0):
    """Wrong descriptions: numbers swapped, wrong direction, counted the lines (1 too many)."""
    out = []
    if dx and dy:
        out.append("%d %s, %d %s" % (abs(dy), "right" if dx > 0 else "left", abs(dx), "up" if dy > 0 else "down"))
    out += [mv(-dx, dy), mv(dx + sgn(dx), dy + sgn(dy)), mv(dx, -dy), mv(-dx, -dy)]
    if not dx:
        out += [mv(dy, 0), mv(-dy, 0)]
    if not dy:
        out += [mv(0, dx), mv(0, -dx)]
    first, rest = out[:1], out[1:]
    rest = rest[i % 3:] + rest[:i % 3]
    return [c for c in first + rest if c and c != mv(dx, dy)]


def describe_e(a, b, na="A", nb="B"):
    dx, dy = b[0] - a[0], b[1] - a[1]
    s = "%s is at %s and %s is at %s. " % (na, pair(*a), nb, pair(*b))
    if dx:
        s += "Across: %d to %d is %s %s. " % (a[0], b[0], sq(abs(dx)), "right" if dx > 0 else "left")
    else:
        s += "The x-coordinate stays %d, so there is no move left or right. " % a[0]
    if dy:
        s += "Up and down: %d to %d is %s %s. " % (a[1], b[1], sq(abs(dy)), "up" if dy > 0 else "down")
    else:
        s += "The y-coordinate stays %d, so there is no move up or down. " % a[1]
    return s + "Count the squares you jump, not the lines you touch."


def move_e(p, dx, dy):
    x, y = p
    q = (x + dx, y + dy)
    parts = []
    if dx:
        parts.append("%s %d squares changes x: %d %s %d = %d" % (
            "Right" if dx > 0 else "Left", abs(dx), x, "+" if dx > 0 else "−", abs(dx), q[0]))
    else:
        parts.append("x stays %d" % x)
    if dy:
        parts.append("%s %d changes y: %d %s %d = %d" % (
            "up" if dy > 0 else "down", abs(dy), y, "+" if dy > 0 else "−", abs(dy), q[1]))
    else:
        parts.append("y stays %d" % y)
    second = parts[1] if parts[1].startswith("y ") else parts[1][0].upper() + parts[1][1:]
    s = ". ".join([parts[0], second]) + ". The new point is %s." % pair(*q)
    return s.replace("Right 1 squares", "Right 1 square").replace("Left 1 squares", "Left 1 square")


# ------------------------------------------------------------ set 1: read coordinates
def set_read(rnd, P):
    its = []
    reads = [
        [(3, 5, "A")], [(6, 2, "B")], [(2, 7, "C"), (5, 4, "D")], [(8, 3, "P"), (3, 8, "Q")],
        [(1, 4, "F"), (4, 1, "E")], [(7, 6, "G")], [(5, 9, "H"), (9, 5, "J")], [(4, 3, "K")],
        [(9, 7, "M"), (4, 2, "N")], [(6, 8, "R")],
    ]
    for i, pts in enumerate(reads):
        x, y, n = pts[0]
        e = "%s. Point %s is at %s. Along the corridor (x) first, then up the stairs (y)." % (walk(x, y), n, pair(x, y))
        if (y, x) in [(p[0], p[1]) for p in pts[1:]]:
            e += " %s is point %s: the numbers are swapped." % (pair(y, x), pts[1][2])
        its.append(mcq(fig(pts_grid(pts, "coordinate grid with labelled points")) +
                       "What are the coordinates of point %s?" % n, pair(x, y), read_cands(x, y, i), e, rnd))
    for pts, wrong, e in [
        ([(0, 4, "S"), (3, 2, "T")], [(4, 0), (1, 4), (0, 5)],
         "Point S is on the y-axis, so it does not go along at all: x = 0. It goes up 4. S is at (0, 4)."),
        ([(6, 0, "V")], [(0, 6), (6, 1), (7, 0)],
         "Point V is on the x-axis. Go along 6 and up 0: (6, 0). A point on the x-axis always has y = 0."),
    ]:
        x, y, n = pts[0]
        its.append(mcq(fig(pts_grid(pts, "coordinate grid with points on the axes")) +
                       "What are the coordinates of point %s?" % n, pair(x, y), [pair(*w) for w in wrong], e, rnd))
    for pts, ax, ans, wrong, e in [
        ([(7, 4, "W")], "x", 7, [4, 8, 6],
         "The x-coordinate tells you how far along to go. Point W is 7 squares along from the origin, so x = 7. (4 is its y-coordinate.)"),
        ([(3, 6, "U")], "y", 6, [3, 7, 5],
         "The y-coordinate tells you how far up to go. Point U is 6 squares up, so y = 6. (3 is its x-coordinate.)"),
        ([(8, 5, "Z"), (5, 8, "Y")], "x", 8, [5, 9, 7],
         "Point Z is 8 squares along from the origin, so its x-coordinate is 8. Point Y is the one at (5, 8)."),
    ]:
        its.append(mcq_num(fig(pts_grid(pts, "coordinate grid with labelled points")) +
                           "What is the %s-coordinate of point %s?" % (ax, pts[0][2]), ans, wrong, e))
    its.append(mcq("In coordinates such as (4, 7), which number comes first?", "the x-coordinate (along)",
                   ["the y-coordinate (up)", "the larger number", "the smaller number"],
                   "Coordinates are always written (x, y). Along the corridor, then up the stairs: the number for along comes first.", rnd))
    its.append(mcq("“Along the corridor, then up the stairs.” What does this help you remember?", "Read x first, then y",
                   ["Read y first, then x", "Start at the top of the grid", "Count the lines, not the squares"],
                   "You walk along the corridor before you can go up the stairs. Go along the x-axis first, then up: (x, y).", rnd))
    its.append(mcq("In the coordinates (6, 2), what does the 2 tell you?", "Go up 2", ["Go along 2", "Go up 6", "Go along 6"],
                   "The second number is the y-coordinate. It tells you how far to go up: up 2. The 6 tells you to go along 6 first.", rnd))
    its.append(mcq("What are the coordinates of the origin, where the x-axis and y-axis meet?", "(0, 0)", ["(1, 1)", "(0, 1)", "(1, 0)"],
                   "The origin is the 0 on both axes. You have not moved along or up, so it is (0, 0).", rnd))
    n, he, his = P.next()
    its.append(mcq("%s starts at (0, 0). %s goes along 4, then up 9. What are the coordinates of %s point?" % (n, he.capitalize(), his),
                   "(4, 9)", ["(9, 4)", "(5, 10)", "(4, 0)"],
                   "Along 4 gives x = 4 and up 9 gives y = 9. Write the along number first: (4, 9).", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Read coordinates on a grid", "items": its}


# ------------------------------------------------------------ set 2: find and plot points
def decoys(x, y, i):
    """Points pupils pick by mistake for (x, y): swapped, counted the lines, next grid line."""
    near = [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
    near = near[i % 4:] + near[:i % 4]
    out = []
    for c in [(y, x), (x + 1, y + 1)] + near:
        if c != (x, y) and min(c) >= 0 and c not in out:
            out.append(c)
    return out[:3]


def set_plot(rnd, P):
    its = []
    pos = Pos(rnd)
    targets = [(6, 2), (3, 7), (1, 5), (8, 4), (4, 9), (7, 3), (2, 6), (5, 1), (9, 6), (2, 8)]
    for i, (x, y) in enumerate(targets):
        pts, ans = pick_letters((x, y), decoys(x, y, i), pos)
        where = {(p[0], p[1]): p[2] for p in pts}
        e = "%s: that is point %s." % (walk(x, y), ans)
        if (y, x) in where:
            e += " Point %s is at %s: the numbers are swapped." % (where[(y, x)], pair(y, x))
        its.append(mcq_fixed(fig(pts_grid(pts, "coordinate grid with points A to D")) +
                             "Which point is at %s?" % pair(x, y), LETTERS, ans, e))
    for x, y, ax, others, e in [
        (5, 2, "x", [(2, 5), (6, 5), (4, 3)],
         "The x-coordinate is the first number: how far along. Point {a} is 5 squares along, at (5, 2). The point at (2, 5) has a y-coordinate of 5, not an x-coordinate of 5."),
        (6, 3, "y", [(3, 6), (3, 1), (5, 4)],
         "The y-coordinate is the second number: how far up. Point {a} is 3 squares up, at (6, 3). The point at (3, 6) has an x-coordinate of 3."),
    ]:
        pts, ans = pick_letters((x, y), others, pos)
        its.append(mcq_fixed(fig(pts_grid(pts, "coordinate grid with points A to D")) +
                             "Which point has a%s %s-coordinate of %d?" % ("n" if ax == "x" else "", ax, x if ax == "x" else y),
                             LETTERS, ans, e.format(a=ans)))
    n, he, his = P.next()
    its.append(mcq(fig(pts_grid([(3, 6, "B")], "coordinate grid with point B")) +
                   "%s says point B is at (6, 3). What mistake did %s make?" % (n, he),
                   "%s swapped x and y" % he.capitalize(),
                   ["%s counted the lines from 1" % he.capitalize(), "%s read the wrong point" % he.capitalize(), "No mistake: %s is right" % he],
                   "Point B is 3 squares along and 6 squares up, so it is at (3, 6). %s wrote the up number first." % n, rnd))
    n, he, his = P.next()
    its.append(mcq(fig(pts_grid([(4, 2, "E")], "coordinate grid with point E")) +
                   "%s says point E is at (5, 3). What mistake did %s make?" % (n, he),
                   "%s counted the lines from 1" % he.capitalize(),
                   ["%s swapped x and y" % he.capitalize(), "%s went left, not right" % he.capitalize(), "No mistake: %s is right" % he],
                   "Point E is at (4, 2). %s counted the line at 0 as 1, so both numbers came out 1 too big. Count the squares from the origin." % n, rnd))
    its.append(mcq("Are (2, 5) and (5, 2) the same point?", "No, they are different points",
                   ["Yes, they use the same numbers", "Yes, the order does not matter", "Only on a small grid"],
                   "(2, 5) is along 2, up 5. (5, 2) is along 5, up 2. The order of the numbers changes where the point is.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s wants to plot (7, 1). %s goes up 7, then along 1. Which point did %s plot by mistake?" % (n, he.capitalize(), he),
                   "(1, 7)", ["(7, 1)", "(8, 2)", "(7, 7)"],
                   "Going along 1 and up 7 lands on (1, 7). To plot (7, 1), go along 7 first, then up 1.", rnd))
    its.append(mcq("Which point is further to the right: (2, 9) or (6, 1)?", "(6, 1)", ["(2, 9)", "They are the same", "You cannot tell"],
                   "How far right a point is depends on the x-coordinate, the first number. 6 is more than 2, so (6, 1) is further right.", rnd))
    its.append(mcq("Which point is higher on the grid: (8, 3) or (2, 5)?", "(2, 5)", ["(8, 3)", "They are the same", "You cannot tell"],
                   "How high a point is depends on the y-coordinate, the second number. 5 is more than 3, so (2, 5) is higher.", rnd))
    its.append(mcq("Which point is straight above (4, 2)?", "(4, 6)", ["(6, 2)", "(2, 4)", "(6, 4)"],
                   "Points straight above each other have the same x-coordinate. (4, 6) has x = 4, the same as (4, 2), and a bigger y.", rnd))
    its.append(mcq("Which point is straight to the right of (1, 5)?", "(7, 5)", ["(1, 7)", "(5, 1)", "(7, 1)"],
                   "Points straight across from each other have the same y-coordinate. (7, 5) has y = 5, the same as (1, 5), and a bigger x.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Find and plot points", "items": its}


# ------------------------------------------------------------ set 3: translations
def set_translate(rnd, P):
    its = []
    pos = Pos(rnd)
    # point given in words
    for i, (p, dx, dy) in enumerate([((3, 4), 2, 3), ((2, 3), 0, 5), ((7, 5), -4, 0), ((2, 6), 5, -3),
                                     ((8, 3), -3, 4), ((9, 8), -6, -5)]):
        q = (p[0] + dx, p[1] + dy)
        assert inside(q)
        its.append(mcq("Point A is at %s. It is translated %s. What are its new coordinates?" % (pair(*p), mv_long(dx, dy)),
                       pair(*q), [pair(*c) for c in move_cands(p, dx, dy, i)], move_e(p, dx, dy), rnd))
    # point on a grid, choose where it lands
    # decoys: went the wrong way, moves swapped, only one coordinate changed
    for p, dx, dy, others in [((6, 2), -4, 1, [(10, 3), (3, 2), (2, 1)]), ((1, 6), 3, -2, [(4, 6), (1, 4), (4, 8)]),
                              ((2, 1), 2, 4, [(0, 5), (6, 3), (4, 1)]), ((7, 7), -2, -4, [(3, 5), (5, 7), (9, 3)])]:
        q = (p[0] + dx, p[1] + dy)
        pts, ans = pick_letters(q, others, pos)
        G = grid_for([p] + [c[:2] for c in pts], lo=7)
        G.point(p[0], p[1], "P", RED)
        for c in pts:
            G.point(*c)
        its.append(mcq_fixed(fig(G.svg("coordinate grid with point P and points A to D")) +
                             "Point P is translated %s. Which point shows where it lands?" % mv_long(dx, dy),
                             LETTERS, ans, move_e(p, dx, dy) + " That is point %s." % ans))
    # describe the translation from a grid
    for i, (a, b) in enumerate([((2, 3), (5, 5)), ((7, 2), (3, 2)), ((1, 6), (4, 2)), ((6, 7), (2, 4)), ((3, 1), (3, 7))]):
        G = grid_for([a, b], lo=7)
        G.point(a[0], a[1], "A", RED).point(b[0], b[1], "B")
        dx, dy = b[0] - a[0], b[1] - a[1]
        its.append(mcq(fig(G.svg("coordinate grid with points A and B")) +
                       "Point A is translated to point B. Describe the translation.",
                       mv(dx, dy), describe_cands(dx, dy, i), describe_e(a, b), rnd))
    # describe from coordinates only
    for i, (a, b) in enumerate([((2, 7), (8, 3)), ((9, 1), (5, 6))]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        its.append(mcq("A shape’s corner moves from %s to %s. Describe the translation." % (pair(*a), pair(*b)),
                       mv(dx, dy), describe_cands(dx, dy, i + 1), describe_e(a, b, "The start", "the end"), rnd))
    its.append(mcq("Point B is translated 3 squares right and 2 squares up. It lands on (7, 5). Where did it start?", "(4, 3)",
                   ["(10, 7)", "(5, 2)", "(4, 5)"],
                   "Work backwards: undo each move. 3 right is undone by 3 left: 7 − 3 = 4. 2 up is undone by 2 down: 5 − 2 = 3. B started at (4, 3).", rnd))
    n, he, his = P.next()
    its.append(mcq("%s translates (5, 6) 3 squares left and gets (8, 6). What mistake did %s make?" % (n, he),
                   "%s moved right, not left" % he.capitalize(),
                   ["%s changed the y-coordinate" % he.capitalize(), "%s swapped x and y" % he.capitalize(), "No mistake: %s is right" % he],
                   "Moving left makes the x-coordinate smaller: 5 − 3 = 2. The correct answer is (2, 6). %s added 3, which is a move to the right." % n, rnd))
    its.append(mcq("A point is translated up or down. Which coordinate changes?", "only the y-coordinate",
                   ["only the x-coordinate", "both coordinates", "neither coordinate"],
                   "Up and down is the y direction. The point does not move left or right, so the x-coordinate stays the same.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Translations: left, right, up and down", "items": its}


# ------------------------------------------------------------ set 4: complete a polygon
SHAPES = ["square", "rectangle", "triangle", "trapezium"]


def set_polygon(rnd, P):
    its = []
    pos = Pos(rnd)
    # three corners drawn with two sides: give the 4th corner
    for A, B, C, D, wrong in [
        ((1, 2), (6, 2), (6, 5), (1, 5), [(5, 1), (1, 6), (2, 6)]),
        ((2, 1), (2, 5), (6, 5), (6, 1), [(1, 6), (6, 2), (7, 2)]),
        ((3, 2), (7, 2), (7, 6), (3, 6), [(6, 3), (3, 7), (4, 7)]),
        ((1, 1), (1, 7), (4, 7), (4, 1), [(1, 4), (4, 2), (5, 2)]),
    ]:
        G = grid_for([A, B, C, D], lo=6)
        G.seg(A, B).seg(B, C)
        G.point(A[0], A[1], "A").point(B[0], B[1], "B").point(C[0], C[1], "C")
        same_x = "A" if D[0] == A[0] else "C"
        same_y = "C" if same_x == "A" else "A"
        assert (D[0] == A[0] and D[1] == C[1]) or (D[0] == C[0] and D[1] == A[1])
        e = ("D is straight in line with %s up and down, so x = %d. It is straight in line with %s across, so y = %d. D is at %s."
             % (same_x, D[0], same_y, D[1], pair(*D)))
        kind = "square" if abs(A[0] - B[0]) + abs(A[1] - B[1]) == abs(B[0] - C[0]) + abs(B[1] - C[1]) else "rectangle"
        its.append(mcq(fig(G.svg("coordinate grid with three corners of a " + kind)) +
                       "A, B and C are 3 corners of a %s. What are the coordinates of the 4th corner, D?" % kind,
                       pair(*D), [pair(*w) for w in wrong], e, rnd))
    # red corners, which lettered point completes the shape
    for corners, tgt, others, kind in [
        ([(1, 1), (5, 1), (5, 5)], (1, 5), [(1, 7), (3, 5), (2, 6)], "square"),
        ([(2, 2), (2, 5), (8, 5)], (8, 2), [(7, 2), (2, 8), (8, 1)], "rectangle"),
        ([(3, 1), (7, 1), (3, 5)], (7, 5), [(5, 7), (7, 6), (6, 5)], "square"),
    ]:
        pts, ans = pick_letters(tgt, others, pos)
        G = grid_for(corners + [c[:2] for c in pts], lo=7)
        for c in corners:
            G.point(c[0], c[1], None, RED)
        for c in pts:
            G.point(*c)
        xs = sorted({c[0] for c in corners + [tgt]})
        ys = sorted({c[1] for c in corners + [tgt]})
        assert len(xs) == 2 and len(ys) == 2 and set((x, y) for x in xs for y in ys) == set(corners + [tgt])
        if kind == "square":
            assert xs[1] - xs[0] == ys[1] - ys[0]
        its.append(mcq_fixed(fig(G.svg("coordinate grid with three red corners and points A to D")) +
                             "The red dots are 3 corners of a %s. Which point is the 4th corner?" % kind, LETTERS, ans,
                             "The missing corner must line up with the red corners: x = %d (straight above or below one corner) "
                             "and y = %d (straight across from another). That is %s, point %s." % (tgt[0], tgt[1], pair(*tgt), ans)))
    # corners in words only
    for given, D, wrong, kind in [
        ([(1, 2), (6, 2), (6, 5)], (1, 5), [(5, 1), (6, 2), (2, 6)], "rectangle"),
        ([(2, 3), (5, 3), (5, 6)], (2, 6), [(6, 2), (5, 3), (3, 7)], "square"),
        ([(0, 1), (0, 4), (7, 4)], (7, 1), [(1, 7), (7, 4), (8, 2)], "rectangle"),
    ]:
        xs = sorted({c[0] for c in given + [D]})
        ys = sorted({c[1] for c in given + [D]})
        assert set((x, y) for x in xs for y in ys) == set(given + [D])
        wrong = [w for w in wrong if w not in given] + [(D[1], D[0]), (D[0] + 1, D[1] + 1), (D[0], D[1] + 1)]
        its.append(mcq("A %s has 3 corners at %s, %s and %s. What are the coordinates of the 4th corner?"
                       % ((kind,) + tuple(pair(*c) for c in given)), pair(*D), [pair(*w) for w in wrong],
                       "The corners of a %s use just two x-coordinates (%d and %d) and two y-coordinates (%d and %d). "
                       "The pair not used yet is %s." % (kind, xs[0], xs[1], ys[0], ys[1], pair(*D)), rnd))
    # plot and join: name the shape
    for pts, ans, e in [
        ([(1, 1), (4, 1), (4, 4), (1, 4)], "square", "The sides are all 3 squares long and meet at right angles, so it is a square."),
        ([(2, 1), (8, 1), (8, 4), (2, 4)], "rectangle", "The sides are 6, 3, 6 and 3 squares long and meet at right angles, so it is a rectangle."),
        ([(2, 2), (6, 2), (4, 6)], "triangle", "There are only 3 points, so joining them makes 3 sides: a triangle."),
        ([(1, 1), (7, 1), (5, 4), (3, 4)], "trapezium",
         "The bottom side (y = 1) and the top side (y = 4) are parallel, but the other two sides slope. "
         "One pair of parallel sides makes a trapezium."),
    ]:
        its.append(mcq_fixed("Plot these points and join them in order, then join the last point to the first: %s. Which shape do you make?"
                             % ", ".join(pair(*p) for p in pts), SHAPES, ans, e))
    # shapes after a translation
    for (A, B), col in [(((1, 1, 4, 3), (5, 5, 8, 7)), BLUE), (((6, 4, 9, 7), (2, 1, 5, 4)), BLUE)]:
        G = Grid(10, 8)
        G.rect(*A).rect(*B, col=col)
        G.note((A[0] + A[2]) / 2.0, (A[1] + A[3]) / 2.0, "A", col=GREEN, fs=16)
        G.note((B[0] + B[2]) / 2.0, (B[1] + B[3]) / 2.0, "B", col=col, fs=16)
        dx, dy = B[0] - A[0], B[1] - A[1]
        its.append(mcq(fig(G.svg("coordinate grid with shape A and shape B")) +
                       "Shape A is translated to shape B. Describe the translation.", mv(dx, dy), describe_cands(dx, dy),
                       "Pick one corner and follow it. The bottom-left corner of A is at %s. The bottom-left corner of B is at %s. "
                       "That is %s. Every corner moves the same way." % (pair(A[0], A[1]), pair(B[0], B[1]), mv_long(dx, dy)), rnd))
    for i, (shape, p, dx, dy) in enumerate([
        ("A triangle has corners at (1, 2), (4, 2) and (1, 6).", (4, 2), 5, 1),
        ("A rectangle has corners at (3, 5), (8, 5), (8, 9) and (3, 9).", (8, 9), -2, -6),
        ("A square has corners at (6, 1), (9, 1), (9, 4) and (6, 4).", (6, 4), -4, 5),
    ]):
        q = (p[0] + dx, p[1] + dy)
        its.append(mcq("%s It is translated %s. What are the new coordinates of the corner at %s?" % (shape, mv_long(dx, dy), pair(*p)),
                       pair(*q), [pair(*c) for c in move_cands(p, dx, dy, i)], move_e(p, dx, dy) +
                       " Every corner of the shape moves in the same way, so the shape stays the same size.", rnd))
    its.append(mcq_num("A square has corners at (2, 2), (6, 2) and (6, 6). How many squares long is each side?", 4, [5, 6, 2],
                       "From (2, 2) to (6, 2) the y-coordinate stays 2, so subtract the x-coordinates: 6 − 2 = 4. "
                       "Count the squares between the corners, not the lines (that gives 5).", fmt="%d"))
    assert len(its) == 20, len(its)
    return {"title": "Complete and translate shapes", "items": its}


# ------------------------------------------------------------ set 5: real-life grids
TREASURE = [(7, 6, "T"), (2, 5, "P"), (5, 1, "C"), (1, 2, "W"), (8, 2, "B")]
TNAMES = {"T": "the treasure", "P": "the palm tree", "C": "the cave", "W": "the well", "B": "the boat"}
PARK = [(4, 0, "G"), (4, 4, "F"), (7, 7, "P"), (1, 6, "S"), (7, 2, "C")]
CLASS = [(1, 1, "O"), (4, 1, "A"), (1, 3, "M"), (5, 4, "F"), (3, 6, "T")]


def map_fig(pts, nx, ny, label):
    G = Grid(nx, ny)
    for x, y, n in pts:
        G.point(x, y, n)
    return fig(G.svg(label))


def where(pts, k):
    for x, y, n in pts:
        if n == k:
            return (x, y)
    raise KeyError(k)


def set_real(rnd, P):
    its = []
    tm = map_fig(TREASURE, 9, 8, "map of a treasure island on a coordinate grid")
    key = "The map shows a treasure island. T = treasure, P = palm tree, C = cave, W = well, B = boat. Each square is 1 step. "
    T, Pm, C, W, B = (where(TREASURE, k) for k in "TPCWB")
    its.append(mcq(tm + key + "What are the coordinates of the treasure?", pair(*T), ["(6, 7)", "(8, 7)", "(7, 5)"],
                   "Start at (0, 0). Go along 7, then up 6. The treasure is at (7, 6).", rnd))
    its.append(mcq(tm + key + "What is at (2, 5)?", "the palm tree", ["the cave", "the well", "the treasure"],
                   "Go along 2, then up 5: that is P, the palm tree. Always go along first: (5, 2) would be a different place.", rnd))
    n, he, his = P.next()
    its.append(mcq(tm + key + "%s starts at the palm tree. %s walks 5 squares right and 1 square up. Where is %s now?" % (n, he.capitalize(), he),
                   "the treasure", ["the boat", "the cave", "the well"],
                   "The palm tree is at (2, 5). Right 5: 2 + 5 = 7. Up 1: 5 + 1 = 6. (7, 6) is the treasure.", rnd))
    its.append(mcq(tm + key + "Describe the move from the cave to the treasure.", mv(T[0] - C[0], T[1] - C[1]),
                   describe_cands(T[0] - C[0], T[1] - C[1]), describe_e(C, T, "The cave", "the treasure"), rnd))
    its.append(mcq_num(tm + key + "A pirate walks along the grid lines from the well to the boat. What is the shortest number of steps?",
                       7, [9, 8, 6],
                       "The well is at (1, 2) and the boat is at (8, 2). They have the same y-coordinate, so walk straight across: 8 − 1 = 7 steps. "
                       "Count the squares, not the lines."))
    its.append(mcq(tm + key + "A second treasure is buried 3 squares left of the treasure. What are its coordinates?", "(4, 6)",
                   ["(3, 6)", "(7, 3)", "(6, 4)"],
                   "The treasure is at (7, 6). Left 3 changes only x: 7 − 3 = 4. y stays 6: (4, 6).", rnd))
    its.append(mcq(tm + key + "The boat sails 4 squares up. Where does it stop?", "(8, 6)", ["(12, 2)", "(8, 7)", "(6, 8)"],
                   "The boat is at (8, 2). Up 4 changes only y: 2 + 4 = 6. x stays 8: (8, 6).", rnd))
    pm = map_fig(PARK, 8, 8, "map of a park on a coordinate grid")
    pkey = "The map shows a park. G = gate, F = fountain, P = pond, S = slide, C = café. Each square is 1 step. "
    G_, F, Pd, S, Cf = (where(PARK, k) for k in "GFPSC")
    its.append(mcq(pm + pkey + "What are the coordinates of the café?", pair(*Cf), ["(2, 7)", "(8, 3)", "(7, 3)"],
                   "Start at (0, 0). Go along 7, then up 2. The café is at (7, 2).", rnd))
    its.append(mcq(pm + pkey + "Which place is at (1, 6)?", "the slide", ["the pond", "the café", "the fountain"],
                   "Go along 1, then up 6: that is S, the slide.", rnd))
    n, he, his = P.next()
    its.append(mcq_num(pm + pkey + "%s walks from the gate straight up to the fountain. How many steps does %s walk?" % (n, he),
                       4, [5, 3, 8],
                       "The gate is at (4, 0) and the fountain is at (4, 4). Same x, so it is a straight line up: 4 − 0 = 4 steps."))
    its.append(mcq(pm + pkey + "Describe the move from the fountain to the pond.", mv(Pd[0] - F[0], Pd[1] - F[1]),
                   describe_cands(Pd[0] - F[0], Pd[1] - F[1], 1), describe_e(F, Pd, "The fountain", "the pond"), rnd))
    its.append(mcq(pm + pkey + "A bench is put 3 squares right and 1 square down from the slide. Where is the bench?", "(4, 5)",
                   ["(4, 7)", "(2, 9)", "(4, 6)"],
                   "The slide is at (1, 6). Right 3: 1 + 3 = 4. Down 1: 6 − 1 = 5. The bench is at (4, 5).", rnd))
    its.append(mcq_num(pm + pkey + "What is the shortest number of steps from the slide to the pond along the grid lines?", 7, [6, 9, 5],
                       "The slide is at (1, 6) and the pond is at (7, 7). Go 7 − 1 = 6 squares right and 7 − 6 = 1 square up. 6 + 1 = 7 steps."))
    cm = map_fig(CLASS, 6, 7, "seating plan of a classroom on a coordinate grid")
    ckey = "The seating plan shows where some pupils sit. O = Oliver, A = Amelia, M = Mohammed, F = Freya, T = teacher’s desk. "
    O, A, M, Fr, Td = (where(CLASS, k) for k in "OAMFT")
    its.append(mcq(cm + ckey + "What are the coordinates of Freya’s desk?", pair(*Fr), ["(4, 5)", "(6, 5)", "(5, 3)"],
                   "Go along 5, then up 4. Freya sits at (5, 4). (4, 5) has the numbers swapped.", rnd))
    its.append(mcq(cm + ckey + "Who sits at (1, 3)?", "Mohammed", ["Amelia", "Oliver", "Freya"],
                   "Go along 1, then up 3: that is M, Mohammed. Amelia is at (4, 1), and Oliver is at (1, 1).", rnd))
    its.append(mcq(cm + ckey + "Describe the move from Oliver’s desk to Amelia’s desk.", mv(A[0] - O[0], A[1] - O[1]),
                   describe_cands(A[0] - O[0], A[1] - O[1], 2), describe_e(O, A, "Oliver", "Amelia"), rnd))
    its.append(mcq(cm + ckey + "Mohammed moves to a new desk 4 squares right and 2 squares up. Where is his new desk?", "(5, 5)",
                   ["(3, 7)", "(5, 3)", "(1, 5)"],
                   "Mohammed is at (1, 3). Right 4: 1 + 4 = 5. Up 2: 3 + 2 = 5. His new desk is at (5, 5).", rnd))
    its.append(mcq(cm + ckey + "Describe the move from Mohammed’s desk to the teacher’s desk.", mv(Td[0] - M[0], Td[1] - M[1]),
                   describe_cands(Td[0] - M[0], Td[1] - M[1], 0), describe_e(M, Td, "Mohammed", "the teacher’s desk"), rnd))
    its.append(mcq_num(cm + ckey + "How many squares is it from Oliver’s desk straight up to Mohammed’s desk?", 2, [3, 1, 4],
                       "Oliver is at (1, 1) and Mohammed is at (1, 3). The x-coordinate stays 1, so subtract the y-coordinates: 3 − 1 = 2 squares."))
    n, he, his = P.next()
    its.append(mcq("In a computing lesson, %s’s robot starts at (1, 1). It moves 4 squares right, then 3 squares up, then 2 squares left. "
                   "Where does it stop?" % n, "(3, 4)", ["(5, 4)", "(7, 4)", "(4, 3)"],
                   "Follow one move at a time. Right 4: (5, 1). Up 3: (5, 4). Left 2: (3, 4). Left makes x smaller.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Maps and real-life grids", "items": its}


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
    G.note(1.5, 0.5, "along 3").note(3.25, 2.5, "up 5", anchor="start")
    G.point(3, 5, "A")
    plot = G.svg("coordinate grid: from the origin go along 3, then up 5 to point A at (3, 5)")
    G = Grid(8, 7)
    G.arrow((2, 5), (6, 5)).arrow((6, 5), (6, 2))
    G.point(2, 5, "A", RED).point(6, 2, "B", where=(1, -1))
    G.note(4, 5.5, "4 right").note(6.25, 3.5, "3 down", anchor="start")
    trans = G.svg("coordinate grid: point A at (2, 5) is translated 4 right and 3 down to point B at (6, 2)")
    G = Grid(7, 6)
    G.seg((1, 1), (5, 1)).seg((5, 1), (5, 4)).seg((5, 4), (1, 4), BLUE).seg((1, 4), (1, 1), BLUE)
    G.point(1, 1, "A").point(5, 1, "B").point(5, 4, "C").point(1, 4, "D", RED)
    poly = G.svg("coordinate grid: rectangle ABCD with the missing corner D at (1, 4)")
    return (
        "<h2>What coordinates are</h2>"
        "<p>A coordinate grid has two axes. The <b>x-axis</b> goes across. The <b>y-axis</b> goes up. "
        "They meet at the <b>origin</b>, (0, 0).</p>"
        "<p>Coordinates (x, y) tell you how to reach a point from the origin. "
        "Remember: <b>along the corridor, then up the stairs</b>. The first number is how far along. The second is how far up.</p>"
        "<figure class='sn-fig'>" + plot +
        "<figcaption>To plot (3, 5), start at the origin. Go along 3, then up 5. Point A is at (3, 5).</figcaption></figure>" +
        ex("Example", "A point is 6 squares along from the origin and 2 squares up. What are its coordinates?",
           "Along 6 is the x-coordinate. Up 2 is the y-coordinate. Write the along number first.", "(6, 2)") +
        "<p>Order matters. (3, 5) and (5, 3) are different points. A point on the x-axis has y = 0, such as (4, 0). "
        "A point on the y-axis has x = 0, such as (0, 4).</p>"
        "<h2>Translations</h2>"
        "<p>A <b>translation</b> slides a point or shape without turning it. Moving left or right changes only x. "
        "Moving up or down changes only y.</p>"
        "<figure class='sn-fig'>" + trans +
        "<figcaption>A (2, 5) is translated 4 squares right and 3 squares down. x: 2 + 4 = 6. y: 5 − 3 = 2. It lands on B (6, 2).</figcaption></figure>" +
        table(["Move", "What changes", "Example from (5, 4)"], [
            ["right 2", "x gets bigger", "(7, 4)"],
            ["left 2", "x gets smaller", "(3, 4)"],
            ["up 2", "y gets bigger", "(5, 6)"],
            ["down 2", "y gets smaller", "(5, 2)"],
        ]) +
        ex("Example", "Describe the translation from (1, 6) to (4, 2).",
           "Across: 1 to 4 is 3 squares right. Up and down: 6 to 2 is 4 squares down.", "3 squares right and 4 squares down") +
        "<h2>Completing a shape</h2>"
        "<p>To find the missing corner of a square or rectangle, line it up with the other corners. "
        "It shares its x-coordinate with one corner and its y-coordinate with another.</p>"
        "<figure class='sn-fig'>" + poly +
        "<figcaption>A (1, 1), B (5, 1) and C (5, 4) are 3 corners of a rectangle. D is above A, so x = 1, and across from C, so y = 4. D is at (1, 4).</figcaption></figure>" +
        "<p>When a whole shape is translated, every corner moves the same way. Move each corner, then join them up.</p>" +
        ex("Example", "A triangle has corners at (1, 2), (4, 2) and (1, 6). It is translated 5 squares right. What are the new corners?",
           "Add 5 to each x-coordinate. The y-coordinates stay the same.", "(6, 2), (9, 2) and (6, 6)") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Swapping x and y: plotting (3, 7) at along 7, up 3", "Along the corridor first (x), then up the stairs (y)"],
            ["Counting the lines, starting with 1 at the origin", "The origin is 0. Count the squares you jump"],
            ["Moving the wrong way: adding for “left”", "Left and down make the number smaller"],
            ["Changing only one coordinate for a move like “3 right, 2 up”", "Change x for left/right and y for up/down"],
            ["Changing x for an up or down move", "Up and down change only y"],
        ])
    )


FAQ = [
    {"q": "What do children learn about coordinates in Year 4?",
     "a": "In Year 4, children read and plot coordinates in the first quadrant, describe translations such as “3 squares left and 2 squares up”, "
          "and plot points to complete a shape. Reflections come in Year 5, and all four quadrants in Year 6."},
    {"q": "Which comes first in coordinates, x or y?",
     "a": "The x-coordinate always comes first. Many teachers say “along the corridor, then up the stairs”: (4, 7) means along 4, then up 7."},
    {"q": "What is a translation in maths?",
     "a": "A translation slides a point or shape left or right and up or down without turning it or changing its size. "
          "Moving left or right changes the x-coordinate, and moving up or down changes the y-coordinate."},
    {"q": "What is the first quadrant?",
     "a": "It is the part of a coordinate grid to the right of the y-axis and above the x-axis, where both coordinates are 0 or more. "
          "Year 4 pupils work only in the first quadrant."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions. Fixed-order choices stay as they are."""
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
    rnd = random.Random(4416)
    P = People(rnd)
    sets = [set_read(rnd, P), set_plot(rnd, P), set_translate(rnd, P), set_polygon(rnd, P), set_real(rnd, P)]
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
        "country": "uk", "subject": "maths", "grade": "year-4", "slug": "coordinates", "sort": 16,
        "updated": UPDATED, "pdf_url": "",
        "title": "Coordinates and Translations in the First Quadrant",
        "seo_title": "Year 4 Coordinates Worksheets: Plot Points, Translations and Shapes on a Grid",
        "short_title": "Coordinates",
        "domain": "Geometry – position and direction",
        "standard_code": "Year 4: Geometry – position and direction",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Describe positions on a 2-D grid as coordinates in the first quadrant; describe movements between positions as translations of a given unit to the left/right and up/down; plot specified points and draw sides to complete a given polygon.",
        "meta_desc": "Free Year 4 coordinates worksheets: read and plot coordinates in the first quadrant, describe translations left, right, up and down, complete squares and rectangles, and use maps and seating plans. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "Along the corridor, then up the stairs: (x, y) means go along x, then up y.",
        "key_sub": "(3, 7) and (7, 3) are different points. In a translation, left and right change only x, and up and down change only y.",
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
        mark_large(u, "(coordinate grid|map of|seating plan)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
