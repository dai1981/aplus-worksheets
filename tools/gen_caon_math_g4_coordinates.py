# -*- coding: utf-8 -*-
"""
CA Grade 4 Math: Coordinates and Transformations
(Ontario Mathematics Curriculum 2020, Grade 4: Spatial Sense, E1.2 and E1.3)
  python3 tools/gen_caon_math_g4_coordinates.py
HTML attributes use single quotes (no backslashes in the JSON).

First quadrant only, whole-number coordinates 0-10. Canadian English. Moves are in "units"
(1 unit = one square on the grid). Every grid is drawn exactly: a point (x, y) sits on the crossing
x units right of the origin and y units up. Each letter label sits in the middle of a grid square next
to its own point, never in a square that touches another point and never on another label or note
(checked in Grid.render). Mirror lines run along grid lines (dashed blue).
Wrong answers come from real Grade 4 mistakes: swapping x and y, counting the start line as 1
(answers 1 too big), counting the start square as a move (1 short), moving the wrong way, changing
only one coordinate, stopping on the mirror line, changing the wrong coordinate in a reflection.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
BLUE = "#1f5fa8"
INK = "#2b2b2b"
GRID = "#c9d3cc"
FONT = "Arial, Helvetica, sans-serif"
HALO = " stroke='#ffffff' stroke-width='4' paint-order='stroke'"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]
LETTERS = ["A", "B", "C", "D"]
TRF = ["a translation", "a reflection in a vertical line", "a reflection in a horizontal line", "none of these"]


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
    """Choices keep their order (A B C D, names of moves)."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fixed": True}


def mcq_num(q, correct, cands, e):
    ch = []
    for c in cands:
        if c >= 0 and c != correct and c not in ch:
            ch.append(c)
    ch = sorted([correct] + ch[:3])
    assert len(ch) == 4, (q, ch)
    return mcq_fixed(q, ["%d" % c for c in ch], "%d" % correct, e)


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


def un(n):
    return "%d unit%s" % (n, "" if n == 1 else "s")


def inside(p):
    return 0 <= p[0] <= 10 and 0 <= p[1] <= 10


def sgn(v):
    return (v > 0) - (v < 0)


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

    def __init__(self, nx, ny, u=22):
        assert 1 <= nx <= 10 and 1 <= ny <= 10
        self.nx, self.ny, self.u = nx, ny, u
        left = tw(ny, 14) + 15
        top = 30
        self.ox, self.oy = left, top + ny * u
        self.W = int(math.ceil(self.ox + nx * u + 28))
        self.H = int(math.ceil(self.oy + 26))
        self.pts, self.segs, self.arrows, self.notes, self.mirrors = [], [], [], [], []

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

    def poly(self, corners, col=GREEN):
        for i in range(len(corners)):
            self.seg(corners[i], corners[(i + 1) % len(corners)], col)
        return self

    def mirror(self, kind, m):
        """Dashed mirror line along a grid line: kind 'v' (through m on the x-axis) or 'h' (through m on the y-axis)."""
        assert kind in "vh" and 0 < m < (self.nx if kind == "v" else self.ny)
        self.mirrors.append((kind, m))
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
            # segments, arrows and mirror lines lie on grid lines, so they never cross the middle of a square
            used.add(cell)
            return c, box
        raise AssertionError(("no room for label", x, y))

    def render(self):
        u, ox, oy, nx, ny = self.u, self.ox, self.oy, self.nx, self.ny
        s = []
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
        for kind, m in self.mirrors:
            if kind == "v":
                p, q = self.P(m, 0), self.P(m, ny)
            else:
                p, q = self.P(0, m), self.P(nx, m)
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5' stroke-dasharray='7 5'/>"
                     % (p[0], p[1], q[0], q[1], BLUE))
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
            s.append(text(c[0], c[1] + fs * 0.36, t, fs, anchor=anchor, bold=True, col=col, extra=HALO))
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
        return "It is the origin: 0 across and 0 up"
    return "Start at (0, 0). Go across %d, then up %d" % (x, y)


def read_cands(x, y, i):
    """Swapped, counted the start line as 1 (+1 each), then the next grid line."""
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
        parts.append("%s %s" % (un(abs(dx)), "right" if dx > 0 else "left"))
    if dy:
        parts.append("%s %s" % (un(abs(dy)), "up" if dy > 0 else "down"))
    return " and ".join(parts)


def move_cands(p, dx, dy, i=0):
    """Where students land by mistake: wrong way, x/y mixed up, only one number changed."""
    x, y = p
    c = [(x - dx, y + dy), (x + dy, y + dx), (x + dx, y), (x, y + dy), (x + dx, y - dy), (x - dx, y - dy)]
    c = c[i % 3:] + c[:i % 3]
    # backups: counted the start square as a move (1 short), 1 too far, answer written the wrong way round
    c += [(x + dx - sgn(dx), y + dy - sgn(dy)), (x + dx + sgn(dx), y + dy + sgn(dy)), (y + dy, x + dx)]
    return [q for q in c if inside(q) and q != (x + dx, y + dy) and q != (x, y)]


def describe_cands(dx, dy, i=0):
    """Wrong descriptions: numbers swapped, wrong direction, counted the start line (1 too many)."""
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
        s += "Across: %d to %d is %s %s. " % (a[0], b[0], un(abs(dx)), "right" if dx > 0 else "left")
    else:
        s += "The x-coordinate stays %d, so there is no move left or right. " % a[0]
    if dy:
        s += "Up and down: %d to %d is %s %s. " % (a[1], b[1], un(abs(dy)), "up" if dy > 0 else "down")
    else:
        s += "The y-coordinate stays %d, so there is no move up or down. " % a[1]
    return s + "Count the jumps, not the start."


def move_e(p, dx, dy):
    x, y = p
    q = (x + dx, y + dy)
    parts = []
    if dx:
        parts.append("%s %s changes x: %d %s %d = %d" % (
            "Right" if dx > 0 else "Left", un(abs(dx)), x, "+" if dx > 0 else "−", abs(dx), q[0]))
    else:
        parts.append("x stays %d" % x)
    if dy:
        parts.append("%s %d changes y: %d %s %d = %d" % (
            "up" if dy > 0 else "down", abs(dy), y, "+" if dy > 0 else "−", abs(dy), q[1]))
    else:
        parts.append("y stays %d" % y)
    second = parts[1] if parts[1].startswith("y ") else parts[1][0].upper() + parts[1][1:]
    return ". ".join([parts[0], second]) + ". The new point is %s." % pair(*q)


# ------------------------------------------------------------ reflections
def refl(p, kind, m):
    return (2 * m - p[0], p[1]) if kind == "v" else (p[0], 2 * m - p[1])


def line_words(kind, m):
    return ("the vertical mirror line through %d on the x-axis" % m if kind == "v"
            else "the horizontal mirror line through %d on the y-axis" % m)


def refl_e(p, kind, m, name="P"):
    r = refl(p, kind, m)
    if kind == "v":
        d = m - p[0]
        side, other = ("left", "right") if d > 0 else ("right", "left")
        return ("%s is at %s. The mirror line goes straight up through %d. %s is %s %s of the line, "
                "so the reflection is %s %s of the line: %d %s %d = %d. A vertical mirror line changes only x; y stays %d. "
                "The reflection is %s." % (name, pair(*p), m, name, un(abs(d)), side, un(abs(d)), other,
                                           m, "+" if d > 0 else "−", abs(d), r[0], p[1], pair(*r)))
    d = m - p[1]
    side, other = ("below", "above") if d > 0 else ("above", "below")
    return ("%s is at %s. The mirror line goes straight across through %d. %s is %s %s the line, "
            "so the reflection is %s %s the line: %d %s %d = %d. A horizontal mirror line changes only y; x stays %d. "
            "The reflection is %s." % (name, pair(*p), m, name, un(abs(d)), side, un(abs(d)), other,
                                       m, "+" if d > 0 else "−", abs(d), r[1], p[0], pair(*r)))


def refl_cands(p, kind, m):
    """Stopped on the line, 1 too far (counted the line as a square), 1 short, changed the other coordinate, swapped."""
    x, y = p
    r = refl(p, kind, m)
    if kind == "v":
        d = m - x
        c = [(m, y), (r[0] + sgn(d), y), (r[0] - sgn(d), y), (x, y + 2 * d), (x, y - 2 * d), (y, r[0])]
    else:
        d = m - y
        c = [(x, m), (x, r[1] + sgn(d)), (x, r[1] - sgn(d)), (x + 2 * d, y), (x - 2 * d, y), (r[1], x)]
    return [q for q in c if inside(q) and q != r and q != p]


def far(c, pts):
    return all(max(abs(c[0] - q[0]), abs(c[1] - q[1])) >= 2 for q in pts)


# ------------------------------------------------------------ set 1: read coordinates
def set_read(rnd, P):
    its = []
    reads = [
        [(4, 6, "A")], [(5, 3, "B")], [(2, 6, "C"), (6, 2, "D")], [(7, 4, "E"), (4, 7, "F")],
        [(1, 3, "G"), (3, 1, "H")], [(8, 5, "J")], [(6, 9, "K"), (9, 6, "L")], [(3, 2, "M")],
        [(9, 8, "N"), (5, 2, "P")], [(7, 7, "Q")],
    ]
    for i, pts in enumerate(reads):
        x, y, n = pts[0]
        e = "%s. Point %s is at %s. Go across first (x), then up (y)." % (walk(x, y), n, pair(x, y))
        if (y, x) in [(p[0], p[1]) for p in pts[1:]]:
            e += " %s is point %s: the numbers are swapped." % (pair(y, x), pts[1][2])
        its.append(mcq(fig(pts_grid(pts, "coordinate grid with labelled points")) +
                       "What are the coordinates of point %s?" % n, pair(x, y), read_cands(x, y, i), e, rnd))
    for pts, wrong, e in [
        ([(0, 5, "S"), (4, 2, "T")], [(5, 0), (1, 5), (0, 6)],
         "Point S is on the y-axis, so it does not go across at all: x = 0. It goes up 5. S is at (0, 5)."),
        ([(7, 0, "V")], [(0, 7), (7, 1), (8, 0)],
         "Point V is on the x-axis. Go across 7 and up 0: (7, 0). A point on the x-axis always has y = 0."),
    ]:
        x, y, n = pts[0]
        its.append(mcq(fig(pts_grid(pts, "coordinate grid with points on the axes")) +
                       "What are the coordinates of point %s?" % n, pair(x, y), [pair(*w) for w in wrong], e, rnd))
    for pts, ax, ans, wrong, e in [
        ([(6, 3, "W")], "x", 6, [3, 7, 5],
         "The x-coordinate tells you how far across to go. Point W is 6 units across from the origin, so x = 6. (3 is its y-coordinate.)"),
        ([(2, 5, "U")], "y", 5, [2, 6, 4],
         "The y-coordinate tells you how far up to go. Point U is 5 units up, so y = 5. (2 is its x-coordinate.)"),
        ([(8, 4, "Z"), (4, 8, "Y")], "x", 8, [4, 9, 7],
         "Point Z is 8 units across from the origin, so its x-coordinate is 8. Point Y is the one at (4, 8)."),
    ]:
        its.append(mcq_num(fig(pts_grid(pts, "coordinate grid with labelled points")) +
                           "What is the %s-coordinate of point %s?" % (ax, pts[0][2]), ans, wrong, e))
    its.append(mcq("In the ordered pair (5, 8), which number comes first?", "the x-coordinate (across)",
                   ["the y-coordinate (up)", "the larger number", "the smaller number"],
                   "An ordered pair is always written (x, y). The number for across comes first, then the number for up.", rnd))
    its.append(mcq("Which tip helps you plot a point such as (3, 6)?", "Go across first, then up",
                   ["Go up first, then across", "Start at the top of the grid", "Count the lines, starting with 1"],
                   "Think of walking to an elevator before you ride it up. Go across the x-axis first, then up: (x, y).", rnd))
    its.append(mcq("In the ordered pair (7, 3), what does the 3 tell you?", "Go up 3", ["Go across 3", "Go up 7", "Go across 7"],
                   "The second number is the y-coordinate. It tells you how far to go up: up 3. The 7 tells you to go across 7 first.", rnd))
    its.append(mcq("What are the coordinates of the origin, where the x-axis and the y-axis meet?", "(0, 0)", ["(1, 1)", "(0, 1)", "(1, 0)"],
                   "The origin is 0 on both axes. You have not moved across or up, so it is (0, 0).", rnd))
    n, he, his = P.next()
    its.append(mcq("%s starts at (0, 0). %s goes across 3, then up 8. What are the coordinates of %s point?" % (n, he.capitalize(), his),
                   "(3, 8)", ["(8, 3)", "(4, 9)", "(3, 0)"],
                   "Across 3 gives x = 3 and up 8 gives y = 8. Write the across number first: (3, 8).", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Read points on a grid", "items": its}


# ------------------------------------------------------------ set 2: plot points
def decoys(x, y, i):
    """Points students pick by mistake for (x, y): swapped, counted the start line, next grid line."""
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
    targets = [(5, 2), (2, 7), (1, 4), (7, 3), (3, 8), (6, 4), (2, 5), (4, 1), (8, 6), (3, 9)]
    for i, (x, y) in enumerate(targets):
        pts, ans = pick_letters((x, y), decoys(x, y, i), pos)
        where = {(p[0], p[1]): p[2] for p in pts}
        e = "%s: that is point %s." % (walk(x, y), ans)
        if (y, x) in where:
            e += " Point %s is at %s: the numbers are swapped." % (where[(y, x)], pair(y, x))
        its.append(mcq_fixed(fig(pts_grid(pts, "coordinate grid with points A to D")) +
                             "Which point is at %s?" % pair(x, y), LETTERS, ans, e))
    for x, y, ax, others, e in [
        (6, 2, "x", [(2, 6), (5, 6), (4, 3)],
         "The x-coordinate is the first number: how far across. Point {a} is 6 units across, at (6, 2). The point at (2, 6) has a y-coordinate of 6, not an x-coordinate of 6."),
        (5, 4, "y", [(4, 5), (2, 1), (6, 2)],
         "The y-coordinate is the second number: how far up. Point {a} is 4 units up, at (5, 4). The point at (4, 5) has an x-coordinate of 4."),
    ]:
        pts, ans = pick_letters((x, y), others, pos)
        its.append(mcq_fixed(fig(pts_grid(pts, "coordinate grid with points A to D")) +
                             "Which point has a%s %s-coordinate of %d?" % ("n" if ax == "x" else "", ax, x if ax == "x" else y),
                             LETTERS, ans, e.format(a=ans)))
    n, he, his = P.next()
    its.append(mcq(fig(pts_grid([(2, 5, "B")], "coordinate grid with point B")) +
                   "%s says point B is at (5, 2). What mistake did %s make?" % (n, he),
                   "%s swapped x and y" % he.capitalize(),
                   ["%s counted the start line as 1" % he.capitalize(), "%s read the wrong point" % he.capitalize(), "No mistake: %s is right" % he],
                   "Point B is 2 units across and 5 units up, so it is at (2, 5). %s wrote the up number first." % n, rnd))
    n, he, his = P.next()
    its.append(mcq(fig(pts_grid([(3, 4, "E")], "coordinate grid with point E")) +
                   "%s says point E is at (4, 5). What mistake did %s make?" % (n, he),
                   "%s counted the start line as 1" % he.capitalize(),
                   ["%s swapped x and y" % he.capitalize(), "%s went left, not right" % he.capitalize(), "No mistake: %s is right" % he],
                   "Point E is at (3, 4). %s counted the line at 0 as 1, so both numbers came out 1 too big. The origin is 0: count the jumps." % n, rnd))
    its.append(mcq("Are (3, 6) and (6, 3) the same point?", "No, they are different points",
                   ["Yes, they use the same numbers", "Yes, the order does not matter", "Only on a small grid"],
                   "(3, 6) is across 3, up 6. (6, 3) is across 6, up 3. The order of the numbers changes where the point is.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s wants to plot (8, 2). %s goes up 8, then across 2. Which point did %s plot by mistake?" % (n, he.capitalize(), he),
                   "(2, 8)", ["(8, 2)", "(9, 3)", "(8, 8)"],
                   "Going across 2 and up 8 lands on (2, 8). To plot (8, 2), go across 8 first, then up 2.", rnd))
    its.append(mcq("Which point is farther to the right: (3, 9) or (7, 2)?", "(7, 2)", ["(3, 9)", "They are the same", "You cannot tell"],
                   "How far right a point is depends on the x-coordinate, the first number. 7 is more than 3, so (7, 2) is farther right.", rnd))
    its.append(mcq("Which point is higher on the grid: (9, 2) or (1, 6)?", "(1, 6)", ["(9, 2)", "They are the same", "You cannot tell"],
                   "How high a point is depends on the y-coordinate, the second number. 6 is more than 2, so (1, 6) is higher.", rnd))
    its.append(mcq("Which point is straight above (5, 1)?", "(5, 7)", ["(7, 1)", "(1, 5)", "(7, 5)"],
                   "Points straight above each other have the same x-coordinate. (5, 7) has x = 5, the same as (5, 1), and a bigger y.", rnd))
    its.append(mcq("Which point is straight to the right of (2, 4)?", "(8, 4)", ["(2, 8)", "(4, 2)", "(8, 2)"],
                   "Points straight across from each other have the same y-coordinate. (8, 4) has y = 4, the same as (2, 4), and a bigger x.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Plot points (A to D)", "items": its}


# ------------------------------------------------------------ set 3: translations
def set_translate(rnd, P):
    its = []
    pos = Pos(rnd)
    # point given in words
    for i, (p, dx, dy) in enumerate([((2, 4), 3, 2), ((3, 2), 0, 6), ((8, 5), -5, 0), ((1, 7), 4, -3),
                                     ((7, 2), -2, 5), ((9, 9), -4, -6)]):
        q = (p[0] + dx, p[1] + dy)
        assert inside(q)
        its.append(mcq("Point A is at %s. It is translated %s. What are its new coordinates?" % (pair(*p), mv_long(dx, dy)),
                       pair(*q), [pair(*c) for c in move_cands(p, dx, dy, i)], move_e(p, dx, dy), rnd))
    # point on a grid, choose where it lands
    # decoys: went the wrong way, moves swapped, only one coordinate changed
    for p, dx, dy, others in [((5, 1), 3, 2, [(2, 3), (7, 4), (8, 1)]), ((2, 7), 4, -3, [(6, 7), (2, 4), (6, 10)]),
                              ((7, 2), -3, 4, [(10, 6), (7, 6), (3, 2)]), ((8, 8), -5, -2, [(3, 10), (6, 3), (8, 6)])]:
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
    for i, (a, b) in enumerate([((1, 2), (4, 4)), ((6, 3), (2, 3)), ((2, 6), (5, 1)), ((7, 6), (3, 2)), ((4, 1), (4, 6))]):
        G = grid_for([a, b], lo=7)
        G.point(a[0], a[1], "A", RED).point(b[0], b[1], "B")
        dx, dy = b[0] - a[0], b[1] - a[1]
        its.append(mcq(fig(G.svg("coordinate grid with points A and B")) +
                       "Point A is translated to point B. Describe the translation.",
                       mv(dx, dy), describe_cands(dx, dy, i), describe_e(a, b), rnd))
    # describe from coordinates only
    for i, (a, b) in enumerate([((3, 8), (9, 4)), ((8, 2), (1, 7))]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        its.append(mcq("A point moves from %s to %s. Describe the translation." % (pair(*a), pair(*b)),
                       mv(dx, dy), describe_cands(dx, dy, i + 1), describe_e(a, b, "The start", "the end"), rnd))
    its.append(mcq("Point B is translated 3 units right and 2 units up. It lands on (8, 6). Where did it start?", "(5, 4)",
                   ["(11, 8)", "(6, 3)", "(5, 6)"],
                   "Work backwards: undo each move. 3 right is undone by 3 left: 8 − 3 = 5. 2 up is undone by 2 down: 6 − 2 = 4. B started at (5, 4).", rnd))
    n, he, his = P.next()
    its.append(mcq("%s translates (6, 5) 4 units left and gets (10, 5). What mistake did %s make?" % (n, he),
                   "%s moved right, not left" % he.capitalize(),
                   ["%s changed the y-coordinate" % he.capitalize(), "%s swapped x and y" % he.capitalize(), "No mistake: %s is right" % he],
                   "Moving left makes the x-coordinate smaller: 6 − 4 = 2. The correct answer is (2, 5). %s added 4, which is a move to the right." % n, rnd))
    its.append(mcq("A point is translated left or right. Which coordinate changes?", "only the x-coordinate",
                   ["only the y-coordinate", "both coordinates", "neither coordinate"],
                   "Left and right is the x direction. The point does not move up or down, so the y-coordinate stays the same.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Translations: slide a point", "items": its}


# ------------------------------------------------------------ set 4: reflections
def L_shape(x0, y0, fx=False, fy=False):
    """An L-shaped hexagon in a 3 by 3 box at (x0, y0). fx / fy flip it left-right / up-down.
    Returns the corners and the middle of the foot square (where its letter goes)."""
    base = [(0, 0), (3, 0), (3, 1), (1, 1), (1, 3), (0, 3)]
    f = lambda p: (x0 + (3 - p[0] if fx else p[0]), y0 + (3 - p[1] if fy else p[1]))
    c = (0.5, 0.5)
    lab = (x0 + (3 - c[0] if fx else c[0]), y0 + (3 - c[1] if fy else c[1]))
    return [f(p) for p in base], lab


def set_reflect(rnd, P):
    its = []
    pos = Pos(rnd)
    # coordinates of the reflection of P (grid with P and the mirror line)
    for p, kind, m in [((2, 3), "v", 4), ((7, 2), "v", 5), ((3, 1), "h", 3), ((5, 6), "h", 4), ((1, 5), "v", 4), ((4, 7), "h", 5)]:
        r = refl(p, kind, m)
        G = grid_for([p, r, (m, m)], lo=7)
        G.mirror(kind, m).point(p[0], p[1], "P", RED)
        its.append(mcq(fig(G.svg("coordinate grid with point P and a dashed mirror line")) +
                       "The blue dashed line is a mirror line. Point P is reflected in it. What are the coordinates of the reflection?",
                       pair(*r), [pair(*c) for c in refl_cands(p, kind, m)], refl_e(p, kind, m), rnd))
    # which lettered point is the reflection
    for p, kind, m in [((3, 4), "v", 5), ((6, 2), "h", 4), ((8, 5), "v", 6), ((1, 7), "h", 5)]:
        r = refl(p, kind, m)
        others = []
        for c in refl_cands(p, kind, m):
            if far(c, [p, r] + others):
                others.append(c)
        assert len(others) >= 3, (p, others)
        others = others[:3]
        pts, ans = pick_letters(r, others, pos)
        G = grid_for([p] + [c[:2] for c in pts], lo=7)
        G.mirror(kind, m).point(p[0], p[1], "P", RED)
        for c in pts:
            G.point(*c)
        where = {(c[0], c[1]): c[2] for c in pts}
        e = refl_e(p, kind, m) + " That is point %s." % ans
        on = (m, p[1]) if kind == "v" else (p[0], m)
        if on in where:
            e += " Point %s is on the mirror line: the reflection goes past the line, not onto it." % where[on]
        its.append(mcq_fixed(fig(G.svg("coordinate grid with point P, a dashed mirror line and points A to D")) +
                             "Point P is reflected in the blue dashed mirror line. Which point shows the reflection?",
                             LETTERS, ans, e))
    # a corner of a rectangle after a reflection
    for (x0, y0, x1, y1), kind, m, corner, other in [((1, 2, 3, 5), "v", 5, (3, 5), (1, 5)),
                                                    ((2, 1, 6, 3), "h", 4, (6, 3), (6, 1)),
                                                    ((6, 6, 8, 8), "v", 5, (6, 8), (8, 8))]:
        cs = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        r = refl(corner, kind, m)
        G = grid_for(cs + [refl(c, kind, m) for c in cs], lo=7)
        G.mirror(kind, m).poly(cs)
        G.point(corner[0], corner[1], None, RED)
        e = (refl_e(corner, kind, m, "The red corner") + " %s is where the corner at %s goes, so it belongs to a different corner."
             % (pair(*refl(other, kind, m)), pair(*other)))
        its.append(mcq(fig(G.svg("coordinate grid with a rectangle and a dashed mirror line")) +
                       "The rectangle has corners at %s. It is reflected in the blue dashed mirror line. "
                       "Where does the red corner at %s go?" % (", ".join(pair(*c) for c in cs[:3]) + " and " + pair(*cs[3]), pair(*corner)),
                       pair(*r), [pair(*refl(other, kind, m))] + [pair(*c) for c in refl_cands(corner, kind, m)], e, rnd))
    # translation or reflection?
    for a, b, ans, e in [
        ((1, 1, False, False), (6, 4, False, False), TRF[0],
         "Shape B points the same way as shape A. It has only slid 5 units right and 3 units up, so it is a translation."),
        ((1, 2, False, False), (6, 2, True, False), TRF[1],
         "Shape B is flipped left to right: its foot points the other way. The two shapes are the same distance from a vertical line through 5, so it is a reflection in a vertical line."),
        ((2, 1, False, False), (2, 6, False, True), TRF[2],
         "Shape B is flipped upside down: its foot is now at the top. The shapes are the same distance from a horizontal line through 5, so it is a reflection in a horizontal line."),
    ]:
        ca, la = L_shape(*a)
        cb, lb = L_shape(*b)
        G = grid_for(ca + cb, lo=7)
        G.poly(ca).poly(cb, BLUE)
        G.note(la[0], la[1], "A", col=GREEN, fs=16).note(lb[0], lb[1], "B", col=BLUE, fs=16)
        its.append(mcq_fixed(fig(G.svg("coordinate grid with shape A and shape B")) +
                             "Shape A is moved to shape B. Which move is it?", TRF, ans, e))
    its.append(mcq("A point is reflected in a vertical mirror line. Which coordinate changes?", "only the x-coordinate",
                   ["only the y-coordinate", "both coordinates", "neither coordinate"],
                   "A vertical mirror line flips the point across, to the left or right. The point does not go up or down, so y stays the same.", rnd))
    its.append(mcq("Point P is 3 units to the left of a vertical mirror line. Where is its reflection?", "3 units to the right of the line",
                   ["3 units to the left of the line", "on the mirror line", "6 units to the right of the line"],
                   "A reflection is the same distance from the mirror line, on the other side. 3 units left becomes 3 units right.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s reflects (2, 5) in %s and gets (4, 5). What mistake did %s make?" % (n, line_words("v", 4), he),
                   "%s stopped on the mirror line" % he.capitalize(),
                   ["%s changed the y-coordinate" % he.capitalize(), "%s swapped x and y" % he.capitalize(), "No mistake: %s is right" % he],
                   "(2, 5) is 2 units left of the line through 4. The reflection is 2 units right of the line: 4 + 2 = 6. "
                   "The answer is (6, 5). %s only moved to the line." % n, rnd))
    its.append(mcq("A point is right on the mirror line. Where is its reflection?", "at the same point",
                   ["1 unit past the line", "at the origin", "on the x-axis"],
                   "The point is 0 units from the mirror line, so its reflection is also 0 units away: it does not move.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Reflections in a mirror line", "items": its}


# ------------------------------------------------------------ set 5: maps and word problems
TOWN = [(1, 2, "S"), (6, 7, "R"), (8, 3, "L"), (2, 6, "F"), (5, 4, "G")]
LAKE = [(1, 1, "D"), (1, 4, "C"), (5, 4, "I"), (6, 6, "N"), (7, 1, "B")]
CLASS = [(1, 1, "L"), (4, 1, "M"), (1, 4, "A"), (5, 3, "Z"), (3, 6, "T")]


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
    tm = map_fig(TOWN, 9, 8, "map of a town on a coordinate grid")
    key = "The map shows a town. S = school, R = skating rink, L = library, F = fire station, G = grocery store. Each unit is 1 block. "
    S, R, L, F, G = (where(TOWN, k) for k in "SRLFG")
    its.append(mcq(tm + key + "What are the coordinates of the skating rink?", pair(*R), ["(7, 6)", "(7, 8)", "(6, 6)"],
                   "Start at (0, 0). Go across 6, then up 7. The rink is at (6, 7). (7, 6) has the numbers swapped.", rnd))
    its.append(mcq(tm + key + "What is at (8, 3)?", "the library", ["the school", "the grocery store", "the fire station"],
                   "Go across 8, then up 3: that is L, the library.", rnd))
    n, he, his = P.next()
    its.append(mcq(tm + key + "%s leaves the school. %s walks 4 blocks right and 2 blocks up. Where is %s now?" % (n, he.capitalize(), he),
                   "the grocery store", ["the skating rink", "the library", "the fire station"],
                   "The school is at (1, 2). Right 4: 1 + 4 = 5. Up 2: 2 + 2 = 4. (5, 4) is the grocery store.", rnd))
    its.append(mcq(tm + key + "Describe the move from the library to the skating rink.", mv(R[0] - L[0], R[1] - L[1]),
                   describe_cands(R[0] - L[0], R[1] - L[1]), describe_e(L, R, "The library", "the rink"), rnd))
    its.append(mcq_num(tm + key + "A fire truck drives along the streets (the grid lines) from the fire station to the library. "
                       "What is the shortest number of blocks?", 9, [10, 6, 3],
                       "The fire station is at (2, 6) and the library is at (8, 3). Go 8 − 2 = 6 blocks right and 6 − 3 = 3 blocks down. "
                       "6 + 3 = 9 blocks."))
    its.append(mcq(tm + key + "A new park is built 3 blocks left of the library. What are its coordinates?", "(5, 3)",
                   ["(11, 3)", "(8, 0)", "(3, 5)"],
                   "The library is at (8, 3). Left 3 changes only x: 8 − 3 = 5. y stays 3: (5, 3).", rnd))
    lm = map_fig(LAKE, 8, 7, "map of a lake at a cottage on a coordinate grid")
    lkey = "The map shows a lake at the cottage. D = dock, C = cottage, I = island, N = loon nest, B = beach. Each unit is 100 m. "
    D, C, I, N, B = (where(LAKE, k) for k in "DCINB")
    its.append(mcq(lm + lkey + "What are the coordinates of the island?", pair(*I), ["(4, 5)", "(6, 5)", "(5, 5)"],
                   "Go across 5, then up 4. The island is at (5, 4).", rnd))
    n, he, his = P.next()
    its.append(mcq(lm + lkey + "%s paddles a canoe from the dock 4 units right and 3 units up. Where does %s land?" % (n, he),
                   "the island", ["the loon nest", "the cottage", "the beach"],
                   "The dock is at (1, 1). Right 4: 1 + 4 = 5. Up 3: 1 + 3 = 4. (5, 4) is the island.", rnd))
    its.append(mcq(lm + lkey + "Describe the move from the island to the loon nest.", mv(N[0] - I[0], N[1] - I[1]),
                   describe_cands(N[0] - I[0], N[1] - I[1], 1), describe_e(I, N, "The island", "the loon nest"), rnd))
    its.append(mcq_num(lm + lkey + "How many units is it from the dock straight up to the cottage?", 3, [4, 2, 5],
                       "The dock is at (1, 1) and the cottage is at (1, 4). The x-coordinate stays 1, so subtract the y-coordinates: 4 − 1 = 3 units."))
    n, he, his = P.next()
    its.append(mcq(lm + lkey + "%s paddles from the island 2 units left and 3 units down. What are the coordinates of the spot where %s stops?" % (n, he),
                   "(3, 1)", ["(7, 1)", "(3, 7)", "(2, 1)"],
                   "The island is at (5, 4). Left 2: 5 − 2 = 3. Down 3: 4 − 3 = 1. %s stops at (3, 1)." % n, rnd))
    cm = map_fig(CLASS, 6, 7, "seating plan of a classroom on a coordinate grid")
    ckey = "The seating plan shows where some students sit. L = Liam, M = Maya, A = Arjun, Z = Zoe, T = teacher’s desk. "
    Li, Ma, Ar, Zo, Td = (where(CLASS, k) for k in "LMAZT")
    its.append(mcq(cm + ckey + "What are the coordinates of Zoe’s desk?", pair(*Zo), ["(3, 5)", "(6, 4)", "(5, 4)"],
                   "Go across 5, then up 3. Zoe sits at (5, 3). (3, 5) has the numbers swapped.", rnd))
    its.append(mcq(cm + ckey + "Who sits at (1, 4)?", "Arjun", ["Maya", "Liam", "Zoe"],
                   "Go across 1, then up 4: that is A, Arjun. Maya is at (4, 1), with the numbers the other way round.", rnd))
    its.append(mcq(cm + ckey + "Describe the move from Liam’s desk to Zoe’s desk.", mv(Zo[0] - Li[0], Zo[1] - Li[1]),
                   describe_cands(Zo[0] - Li[0], Zo[1] - Li[1], 2), describe_e(Li, Zo, "Liam", "Zoe"), rnd))
    n, he, his = P.next()
    its.append(mcq("In a coding lesson, %s’s robot starts at (2, 1). The code says: move 3 right, move 4 up, move 1 left. "
                   "Where does the robot stop?" % n, "(4, 5)", ["(6, 5)", "(5, 5)", "(5, 4)"],
                   "Follow one move at a time. 3 right: (5, 1). 4 up: (5, 5). 1 left: (4, 5). Left makes x smaller.", rnd))
    its.append(mcq("A robot is at (1, 2). Which line of code moves it to (6, 2)?", "move 5 right",
                   ["move 6 right", "move 5 up", "move 5 left"],
                   "The y-coordinate stays 2, so the robot only moves across. 6 − 1 = 5, and x gets bigger, so it moves 5 right. "
                   "Count the jumps, not the start.", rnd))
    n, he, his = P.next()
    its.append(mcq("%s is making a symmetrical design on grid paper for art class. The mirror line is the vertical line through 5 on the x-axis. "
                   "%s draws a dot at (3, 6). Where should the matching dot go?" % (n, he.capitalize()), "(7, 6)",
                   [pair(*c) for c in refl_cands((3, 6), "v", 5)], refl_e((3, 6), "v", 5, "The dot"), rnd))
    n, he, his = P.next()
    its.append(mcq("%s draws half of a butterfly. The body is a vertical mirror line through 6 on the x-axis. "
                   "The tip of the left wing is at (2, 7). Where is the tip of the right wing?" % n, "(10, 7)",
                   [pair(*c) for c in refl_cands((2, 7), "v", 6)], refl_e((2, 7), "v", 6, "The left wing tip"), rnd))
    n, he, his = P.next()
    its.append(mcq("%s folds grid paper along the horizontal line through 4 on the y-axis. A paint dot at (5, 1) is printed on the other side of the fold. "
                   "Where is the new dot?" % n, "(5, 7)",
                   [pair(*c) for c in refl_cands((5, 1), "h", 4)],
                   refl_e((5, 1), "h", 4, "The paint dot") + " Folding paper makes a reflection.", rnd))
    its.append(mcq("On a plan of the schoolyard, a soccer net is a rectangle with corners at (1, 5), (3, 5), (3, 6) and (1, 6). "
                   "The net is moved 4 units right and 2 units down. What are the new coordinates of the corner at (3, 6)?", "(7, 4)",
                   [pair(*c) for c in move_cands((3, 6), 4, -2)], move_e((3, 6), 4, -2) +
                   " Every corner moves the same way, so the net stays the same size.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Maps, robots and designs", "items": its}


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
    G.arrow((0, 0), (4, 0)).arrow((4, 0), (4, 5))
    G.note(2, 0.5, "across 4").note(4.25, 2.5, "up 5", anchor="start")
    G.point(4, 5, "A")
    plot = G.svg("coordinate grid: from the origin go across 4, then up 5 to point A at (4, 5)")
    G = Grid(8, 7)
    G.arrow((1, 2), (5, 2)).arrow((5, 2), (5, 4))
    G.point(1, 2, "A", RED, where=(-1, 1)).point(5, 4, "B")
    G.note(3, 1.5, "4 right").note(5.25, 3, "2 up", anchor="start")
    trans = G.svg("coordinate grid: point A at (1, 2) is translated 4 right and 2 up to point B at (5, 4)")
    G = Grid(8, 6)
    G.mirror("v", 4)
    G.arrow((2, 3), (4, 3)).arrow((4, 3), (6, 3), GREEN)
    G.point(2, 3, "P", RED, where=(-1, 1)).point(6, 3, "Q", where=(1, 1))
    G.note(3, 4.5, "2").note(5, 4.5, "2", col=GREEN)
    refl_svg = G.svg("coordinate grid: point P at (2, 3) is 2 units left of the mirror line through 4, so its reflection Q is at (6, 3)")
    ca, la = L_shape(1, 1)
    cb, lb = L_shape(6, 1, fx=True)
    G = Grid(10, 5)
    G.mirror("v", 5).poly(ca).poly(cb, BLUE)
    G.note(la[0], la[1], "A", col=GREEN, fs=16).note(lb[0], lb[1], "B", col=BLUE, fs=16)
    shapes = G.svg("coordinate grid: L-shape A and its reflection B in the vertical mirror line through 5")
    return (
        "<h2>Reading and plotting points</h2>"
        "<p>A coordinate grid has two number lines. The <b>x-axis</b> goes across. The <b>y-axis</b> goes up. "
        "They meet at the <b>origin</b>, (0, 0).</p>"
        "<p>An ordered pair (x, y) tells you how to reach a point from the origin. "
        "<b>Go across first, then up.</b> The first number is how far across. The second number is how far up.</p>"
        "<figure class='sn-fig'>" + plot +
        "<figcaption>To plot (4, 5), start at the origin. Go across 4, then up 5. Point A is at (4, 5).</figcaption></figure>" +
        ex("Example", "A point is 6 units across from the origin and 2 units up. What are its coordinates?",
           "Across 6 is the x-coordinate. Up 2 is the y-coordinate. Write the across number first.", "(6, 2)") +
        "<p>Order matters. (4, 5) and (5, 4) are different points. A point on the x-axis has y = 0, such as (3, 0). "
        "A point on the y-axis has x = 0, such as (0, 3).</p>"
        "<h2>Translations: slide</h2>"
        "<p>A <b>translation</b> slides a point or shape without turning or flipping it. One square on the grid is 1 unit. "
        "Moving right or left changes only x. Moving up or down changes only y.</p>"
        "<figure class='sn-fig'>" + trans +
        "<figcaption>A (1, 2) is translated 4 units right and 2 units up. x: 1 + 4 = 5. y: 2 + 2 = 4. It lands on B (5, 4).</figcaption></figure>" +
        table(["Move", "What changes", "Example from (5, 4)"], [
            ["2 right", "x gets bigger", "(7, 4)"],
            ["2 left", "x gets smaller", "(3, 4)"],
            ["2 up", "y gets bigger", "(5, 6)"],
            ["2 down", "y gets smaller", "(5, 2)"],
        ]) +
        ex("Example", "Describe the translation from (1, 6) to (4, 2).",
           "Across: 1 to 4 is 3 units right. Up and down: 6 to 2 is 4 units down.", "3 units right and 4 units down") +
        "<h2>Reflections: flip</h2>"
        "<p>A <b>reflection</b> flips a point or shape over a <b>mirror line</b>. "
        "The reflection is the same distance from the line, on the other side.</p>"
        "<figure class='sn-fig'>" + refl_svg +
        "<figcaption>P (2, 3) is 2 units left of the mirror line through 4. Its reflection is 2 units right of the line: 4 + 2 = 6. Q is at (6, 3).</figcaption></figure>" +
        "<p>A vertical mirror line (straight up and down) changes only x. A horizontal mirror line (straight across) changes only y.</p>" +
        ex("Example", "Reflect (5, 1) in the horizontal mirror line through 3 on the y-axis.",
           "(5, 1) is 2 units below the line. The reflection is 2 units above it: 3 + 2 = 5. x stays 5.", "(5, 5)") +
        "<figure class='sn-fig'>" + shapes +
        "<figcaption>Shape B is a reflection of shape A. It is flipped, so its foot points the other way. A translation would keep the foot pointing the same way.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Swapping x and y: plotting (3, 7) at across 7, up 3", "Go across first (x), then up (y)"],
            ["Counting the start line as 1", "The origin is 0. Count the jumps between lines"],
            ["Counting the start square as a move", "Start counting with your first jump"],
            ["Moving the wrong way: adding for “left”", "Left and down make the number smaller"],
            ["Stopping on the mirror line", "Go the same distance past the line"],
            ["Changing y for a vertical mirror line", "A vertical line changes x; a horizontal line changes y"],
        ])
    )


FAQ = [
    {"q": "What do Grade 4 students learn about coordinates in the Ontario math curriculum?",
     "a": "In Grade 4 (Spatial Sense, E1.2 and E1.3), students plot and read points in the first quadrant, describe the translation that moves one point to another, and perform translations and reflections on a grid."},
    {"q": "Which comes first in an ordered pair, x or y?",
     "a": "The x-coordinate always comes first. (3, 7) means go across 3, then up 7. A simple tip is “across first, then up.”"},
    {"q": "How do you reflect a point on a grid?",
     "a": "Count how many units the point is from the mirror line, then count the same number of units on the other side. A vertical mirror line changes only x, and a horizontal mirror line changes only y."},
    {"q": "What is the difference between a translation and a reflection?",
     "a": "A translation slides a shape left, right, up or down, so it still faces the same way. A reflection flips the shape over a mirror line, so it faces the opposite way, like your image in a mirror."},
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
    rnd = random.Random(44814)
    P = People(rnd)
    sets = [set_read(rnd, P), set_plot(rnd, P), set_translate(rnd, P), set_reflect(rnd, P), set_real(rnd, P)]
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
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-4", "slug": "coordinates-and-transformations", "sort": 14,
        "updated": UPDATED, "pdf_url": "",
        "title": "Coordinates, Translations and Reflections on a Grid",
        "seo_title": "Grade 4 Coordinates Worksheets: Plot Points, Translations and Reflections (Free, Answer Key)",
        "short_title": "Coordinates and transformations",
        "domain": "Spatial Sense",
        "standard_code": "Grade 4: E1.2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Plot and read coordinates in the first quadrant of a Cartesian plane, and describe the translations that move a point from one coordinate to another",
        "meta_desc": "Free Grade 4 math worksheets on coordinates for the Ontario curriculum: read and plot points in the first quadrant, describe translations, reflect points and shapes in a mirror line, and solve map and coding problems. 100 questions with an answer key.",
        "key_big": "In (x, y), go across x first, then up y.",
        "key_sub": "(2, 6) and (6, 2) are different points. A translation slides: right and left change x, up and down change y. A reflection flips a point over a mirror line to the same distance on the other side.",
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
