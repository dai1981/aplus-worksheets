# -*- coding: utf-8 -*-
"""
CA Grade 5 Math: Coordinates and Transformations
(Ontario Mathematics Curriculum 2020, Grade 5: Spatial Sense, E1.4 and E1.5)
  python3 tools/gen_caon_math_g5_transformations.py
HTML attributes use single quotes (no backslashes in the JSON).

First quadrant only, whole-number coordinates 0-10 (Grade 5 does not use negative coordinates).
Canadian English (counterclockwise, centre, colour). Lines of reflection are vertical (x = m) or
horizontal (y = m), drawn as a dashed purple line with their name. Rotations are 90° clockwise,
90° counterclockwise or 180° about a vertex (the centre of rotation), so every image stays in the
first quadrant. Every grid is drawn exactly; letter labels never sit on a line, note or other label
(checked in Grid.render).
Wrong answers come from real Grade 5 mistakes: swapping x and y, counting grid lines instead of
spaces (1 too far), moving the wrong way, changing the wrong coordinate, stopping on the line of
reflection, reflecting across instead of up or down, sliding instead of flipping, turning the wrong
way, mixing up 90° and 180°, swapping the numbers in a turn without changing the direction.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
BLUE = "#1f5fa8"
INK = "#2b2b2b"
GRID = "#c9d3cc"
MIRROR = "#8e44ad"
THIN = "#a8a8a8"
FONT = "Arial, Helvetica, sans-serif"
HALO = " stroke='#ffffff' stroke-width='4' paint-order='stroke'"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]
LETTERS = ["A", "B", "C", "D"]
MOVES = ["a translation", "a reflection", "a rotation", "it changed size"]
ROTS = ["90° clockwise", "90° counterclockwise", "180°", "360°"]
CHECK = ["Yes, it is correct", "No, it is too far from the line", "No, it was slid, not flipped", "No, it is bigger"]


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
    """Choices keep their order (A B C D, numbers from small to large, fixed lists)."""
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


def plist(pts):
    return ", ".join(pair(*p) for p in pts)


def units(n):
    return "%d unit%s" % (n, "" if n == 1 else "s")


def sgn(v):
    return (v > 0) - (v < 0)


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


# ------------------------------------------------------------ first-quadrant grid
def overlap(a, b, m=1.0):
    return not (a[2] + m <= b[0] or b[2] + m <= a[0] or a[3] + m <= b[1] or b[3] + m <= a[1])


def seg_hits(p, q, box, m=1.5):
    """Does the straight line p-q (px) pass through the box (px)?"""
    n = 80
    for i in range(n + 1):
        t = i / float(n)
        x, y = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t
        if box[0] - m <= x <= box[2] + m and box[1] - m <= y <= box[3] + m:
            return True
    return False


class Grid:
    """First-quadrant grid from 0 to nx across and 0 to ny up. One grid space = u px."""

    def __init__(self, nx, ny, u=22):
        assert 1 <= nx <= 10 and 1 <= ny <= 10
        self.nx, self.ny, self.u = nx, ny, u
        self.ox = tw(ny, 14) + 15
        self.oy = 30 + ny * u
        self.W = int(math.ceil(self.ox + nx * u + 28))
        self.H = int(math.ceil(self.oy + 26))
        self.pts, self.segs, self.arrows, self.notes, self.polys, self.mirrors, self.arcs = [], [], [], [], [], [], []

    def P(self, x, y):
        return (self.ox + x * self.u, self.oy - y * self.u)

    def ok(self, p):
        return 0 <= p[0] <= self.nx and 0 <= p[1] <= self.ny

    def point(self, x, y, name, col=GREEN, where=None):
        assert x == int(x) and y == int(y) and self.ok((x, y)), (x, y)
        assert all((p[0], p[1]) != (x, y) for p in self.pts), ("two points at the same spot", x, y)
        self.pts.append((x, y, name, col, where))
        return self

    def poly(self, pts, col=GREEN, name=None, at=None):
        for p in pts:
            assert self.ok(p), p
        self.polys.append((pts, col))
        for i in range(len(pts)):
            self.segs.append((pts[i], pts[(i + 1) % len(pts)], col, 2.5))
        if name:
            if at is None:
                at = (sum(p[0] for p in pts) / float(len(pts)), sum(p[1] for p in pts) / float(len(pts)))
            self.note(at[0], at[1], name, col=col, fs=16)
        return self

    def mirror(self, kind, m):
        """kind 'v': the line x = m; kind 'h': the line y = m."""
        if kind == "v":
            assert 2 <= m <= self.nx, m
        else:
            assert 1 <= m <= self.ny, m
            self.W = max(self.W, int(math.ceil(self.ox + self.nx * self.u + 10 + tw("y = %d" % m, 14, True) + 4)))
        self.mirrors.append((kind, m))
        return self

    def arrow(self, a, b, col=RED):
        assert a[0] == b[0] or a[1] == b[1]
        self.arrows.append((a, b, col))
        return self

    def arc(self, c, a, b, cw, col=RED):
        """Turning arrow about the centre c from point a to point b (same distance from c)."""
        assert (a[0] - c[0]) ** 2 + (a[1] - c[1]) ** 2 == (b[0] - c[0]) ** 2 + (b[1] - c[1]) ** 2
        self.arcs.append((c, a, b, cw, col))
        return self

    def note(self, gx, gy, t, anchor="middle", col=RED, fs=14):
        self.notes.append((gx, gy, t, anchor, col, fs))
        return self

    def _edges(self):
        return [(self.P(*a), self.P(*b)) for a, b, col, w in self.segs] + \
               [(self.P(*a), self.P(*b)) for a, b, col in self.arrows] + \
               [self._mline(k, m) for k, m in self.mirrors]

    def _mline(self, kind, m):
        u, ox, oy = self.u, self.ox, self.oy
        if kind == "v":
            return ((ox + m * u, oy), (ox + m * u, oy - self.ny * u - 6))
        return ((ox, oy - m * u), (ox + self.nx * u + 6, oy - m * u))

    def _label_cell(self, x, y, used, others, boxes, where):
        dirs = [where] if where else [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dx, dy in dirs:
            cx, cy = x + dx, y + dy
            if not self.ok((cx, cy)):
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
            if any(seg_hits(p, q, box) for p, q in self._edges()):
                continue
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
        for pts, col in self.polys:
            s.append("<polygon points='%s' fill='%s' fill-opacity='0.16' stroke='none'/>"
                     % (" ".join("%.1f,%.1f" % self.P(*p) for p in pts), col))
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
        boxes = []
        # lines of reflection: dashed, with their name outside the grid
        for kind, m in self.mirrors:
            p, q = self._mline(kind, m)
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-dasharray='7 5'/>"
                     % (p[0], p[1], q[0], q[1], MIRROR))
            if kind == "v":
                t = "x = %d" % m
                w = tw(t, 14, True)
                cx, base = ox + m * u, oy - ny * u - 10
                box = (cx - w / 2, base - 11, cx + w / 2, base + 1)
                assert box[0] > ox + 6, ("line name on the y label", m)
                assert box[2] <= self.W and box[1] >= 0
                s.append(text(cx, base, t, 14, bold=True, col=MIRROR))
            else:
                t = "y = %d" % m
                w = tw(t, 14, True)
                x0, base = ox + nx * u + 10, oy - m * u + 5
                box = (x0, base - 11, x0 + w, base + 1)
                assert box[2] <= self.W
                s.append(text(x0, base, t, 14, anchor="start", bold=True, col=MIRROR))
            boxes.append(box)
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
        for c, a, b, cw, col in self.arcs:
            cc, p, q = self.P(*c), self.P(*a), self.P(*b)
            r = math.hypot(p[0] - cc[0], p[1] - cc[1])
            d = 1 if cw else -1                       # screen y is down: clockwise = growing angle
            ang2 = math.atan2(q[1] - cc[1], q[0] - cc[0]) - d * 15.0 / r
            ang0 = math.atan2(p[1] - cc[1], p[0] - cc[0]) + d * 7.0 / r
            e = (cc[0] + r * math.cos(ang2), cc[1] + r * math.sin(ang2))
            start = (cc[0] + r * math.cos(ang0), cc[1] + r * math.sin(ang0))
            sweep_ang = (d * (ang2 - ang0)) % (2 * math.pi)
            large = 1 if sweep_ang > math.pi else 0
            s.append("<path d='M%.1f,%.1f A%.1f,%.1f 0 %d %d %.1f,%.1f' fill='none' stroke='%s' stroke-width='2.5'/>"
                     % (start[0], start[1], r, r, large, 1 if cw else 0, e[0], e[1], col))
            v = (e[0] - cc[0], e[1] - cc[1])
            t = (-v[1] / r, v[0] / r) if cw else (v[1] / r, -v[0] / r)
            tip = (e[0] + t[0] * 9, e[1] + t[1] * 9)
            n = (-t[1], t[0])
            s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>"
                     % (tip[0], tip[1], e[0] + n[0] * 5, e[1] + n[1] * 5, e[0] - n[0] * 5, e[1] - n[1] * 5, col))
        edges = self._edges()
        for gx, gy, t, anchor, col, fs in self.notes:
            c = self.P(gx, gy)
            w = tw(t, fs, True)
            x0 = c[0] - w / 2 if anchor == "middle" else c[0] if anchor == "start" else c[0] - w
            box = (x0, c[1] - fs * 0.4, x0 + w, c[1] + fs * 0.4)
            assert box[0] >= 0 and box[2] <= self.W, t
            for b in boxes:
                assert not overlap(box, b), ("notes overlap", t)
            for p, q in edges:
                assert not seg_hits(p, q, box, 0.5), ("note on a line", t)
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
                s.append(text(lc[0], lc[1] + 5.8, name, 16, bold=True, col=RED if col == RED else INK, extra=HALO))
        return "".join(s)

    def svg(self, label="coordinate grid"):
        return svg_wrap(self.W, self.H, self.render(), label)


def grid_for(pts, extra=1, lo=6, mirror=None):
    """Grid just big enough for the points and the line (smaller grids print larger)."""
    xs = [p[0] for p in pts] + ([mirror[1]] if mirror and mirror[0] == "v" else [])
    ys = [p[1] for p in pts] + ([mirror[1]] if mirror and mirror[0] == "h" else [])
    G = Grid(min(10, max(lo, max(xs) + extra)), min(10, max(lo, max(ys) + extra)))
    if mirror:
        G.mirror(*mirror)
    return G


def pts_grid(pts, label, ref=None, lo=6):
    G = grid_for([p[:2] for p in pts], lo=lo)
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


# ------------------------------------------------------------ set 1: read and plot points
def walk(x, y):
    a = "do not move across" if x == 0 else "go right %d" % x
    b = "do not move up" if y == 0 else "go up %d" % y
    return "Start at the origin (0, 0), %s, then %s" % (a, b)


def read_cands(x, y, i=0):
    c = [(y, x), (x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1), (y + 1, x)]
    first, rest = c[:1], c[1:]
    rest = rest[i % 4:] + rest[:i % 4]
    return [pair(*q) for q in first + rest if inside(q) and q != (x, y)]


def set_read(rnd, P):
    its = []
    pos = Pos(rnd)
    reads = [
        [(3, 5, "A")], [(6, 2, "B"), (2, 6, "C")], [(1, 4, "D")], [(5, 7, "E"), (7, 5, "F")],
        [(0, 4, "G")], [(7, 0, "H")], [(8, 3, "K"), (3, 8, "M")], [(4, 9, "N")],
    ]
    for i, pts in enumerate(reads):
        x, y, n = pts[0]
        e = "%s. Point %s is at %s. The x-coordinate (across) is written first." % (walk(x, y), n, pair(x, y))
        if len(pts) > 1:
            e += " %s is point %s: the numbers are swapped." % (pair(y, x), pts[1][2])
        if x == 0:
            e += " A point on the y-axis has x-coordinate 0."
        if y == 0:
            e += " A point on the x-axis has y-coordinate 0."
        its.append(mcq(fig(pts_grid(pts, "coordinate grid with labelled points")) +
                       "What are the coordinates of point %s?" % n, pair(x, y), read_cands(x, y, i), e, rnd))
    its.append(mcq_num(fig(pts_grid([(6, 3, "P")], "coordinate grid with labelled points")) +
                       "What is the x-coordinate of point P?", 6, [3, 7, 5],
                       "Point P is 6 units to the right of the origin, so its x-coordinate is 6. (3 is its y-coordinate.)"))
    its.append(mcq_num(fig(pts_grid([(2, 7, "Q")], "coordinate grid with labelled points")) +
                       "What is the y-coordinate of point Q?", 7, [2, 8, 6],
                       "Point Q is 7 units up from the x-axis, so its y-coordinate is 7. (2 is its x-coordinate.)"))
    for (x, y), others in [
        ((4, 2), [(2, 4), (5, 3), (4, 3)]),
        ((1, 6), [(6, 1), (2, 7), (1, 5)]),
        ((5, 3), [(3, 5), (6, 3), (5, 4)]),
        ((0, 5), [(5, 0), (2, 5), (0, 7)]),
        ((7, 4), [(4, 7), (8, 5), (6, 4)]),
    ]:
        pts, ans = pick_letters((x, y), others, pos)
        where = {(p[0], p[1]): p[2] for p in pts}
        e = "%s: that is point %s. Point %s is at %s: the numbers are swapped." % (walk(x, y), ans, where[(y, x)], pair(y, x))
        its.append(mcq_fixed(fig(pts_grid(pts, "coordinate grid with points A to D")) +
                             "Which point is at %s?" % pair(x, y), LETTERS, ans, e))
    its.append(mcq("To plot the point (6, 3), what do you do first from the origin?", "Go right 6",
                   ["Go up 6", "Go right 3", "Go up 3"],
                   "The first number, 6, is the x-coordinate. It tells you how far to go across, so go right 6. Then go up 3.", rnd))
    n, he, his = P.next()
    H = he.capitalize()
    its.append(mcq("%s plots the point (2, 5). %s starts at the origin, goes up 2, then right 5. What mistake did %s make?" % (n, H, he),
                   "%s swapped x and y" % H,
                   ["%s counted the grid lines, not the spaces" % H, "%s should have gone left" % H, "No mistake. %s is right" % H],
                   "In (2, 5), x = 2 comes first: go right 2, then up 5. %s went up 2 and right 5, so %s plotted (5, 2)." % (n, he), rnd))
    n, he, his = P.next()
    its.append(mcq("%s starts at the origin. %s walks 5 units right and 2 units up. Which coordinates name %s position?" % (n, he.capitalize(), his),
                   pair(5, 2), [pair(2, 5), pair(5, 0), pair(7, 0)],
                   "Right 5 gives x = 5. Up 2 gives y = 2. Write x first: (5, 2).", rnd))
    its.append(mcq("A point is on the x-axis, 8 units to the right of the origin. What are its coordinates?", pair(8, 0),
                   [pair(0, 8), pair(8, 8), pair(8, 1)],
                   "8 units right gives x = 8. The point is on the x-axis, so it does not go up: y = 0. The point is (8, 0).", rnd))
    its.append(mcq_num("On a map of a park, the playground is at (4, 1) and the pond is at (4, 6). How many units apart are they?",
                       5, [6, 10, 3],
                       "The x-coordinates are the same, so the pond is straight up from the playground. Up from 1 to 6 is 6 − 1 = 5 units. "
                       "(6 comes from counting the grid lines.)", fmt="%d units"))
    assert len(its) == 20, len(its)
    return {"title": "Read and plot points in the first quadrant", "items": its}


# ------------------------------------------------------------ translations
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
        parts.append("%s %s" % (units(abs(dx)), "right" if dx > 0 else "left"))
    if dy:
        parts.append("%s %s" % (units(abs(dy)), "up" if dy > 0 else "down"))
    return " and ".join(parts)


def move_cands(p, dx, dy, i=0):
    """Where students land by mistake: wrong way, x and y moves mixed up, only one number changed."""
    x, y = p
    c = [(x - dx, y + dy), (x + dy, y + dx), (x + dx, y), (x, y + dy), (x + dx, y - dy), (x - dx, y - dy)]
    c = c[i % 3:] + c[:i % 3]
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
        s += "Across: %d to %d is %s %s. " % (a[0], b[0], units(abs(dx)), "right" if dx > 0 else "left")
    else:
        s += "The x-coordinate stays %d, so there is no move left or right. " % a[0]
    if dy:
        s += "Up and down: %d to %d is %s %s. " % (a[1], b[1], units(abs(dy)), "up" if dy > 0 else "down")
    else:
        s += "The y-coordinate stays %d, so there is no move up or down. " % a[1]
    return s + "Count the spaces you jump, not the lines you touch."


def move_e(p, dx, dy):
    x, y = p
    q = (x + dx, y + dy)
    parts = []
    if dx:
        parts.append("%s %d changes x: %d %s %d = %d" % (
            "Right" if dx > 0 else "Left", abs(dx), x, "+" if dx > 0 else "−", abs(dx), q[0]))
    else:
        parts.append("x stays %d" % x)
    if dy:
        parts.append("%s %d changes y: %d %s %d = %d" % (
            "Up" if dy > 0 else "Down", abs(dy), y, "+" if dy > 0 else "−", abs(dy), q[1]))
    else:
        parts.append("y stays %d" % y)
    return ". ".join(parts) + ". The new point is %s." % pair(*q)


def shift(pts, dx, dy):
    return [(x + dx, y + dy) for x, y in pts]


# ------------------------------------------------------------ set 2: translations
def set_translate(rnd, P):
    its = []
    pos = Pos(rnd)
    for i, (p, dx, dy) in enumerate([((3, 4), 2, 0), ((6, 7), 0, -4), ((2, 2), 5, 3), ((8, 3), -6, 2),
                                     ((5, 9), -3, -6), ((1, 6), 7, -5)]):
        q = (p[0] + dx, p[1] + dy)
        assert inside(q)
        its.append(mcq("Point A is at %s. It is translated %s. What are its new coordinates?" % (pair(*p), mv_long(dx, dy)),
                       pair(*q), [pair(*c) for c in move_cands(p, dx, dy, i)], move_e(p, dx, dy), rnd))
    for i, (a, b) in enumerate([((2, 3), (5, 1)), ((6, 2), (3, 6)), ((1, 1), (7, 4))]):
        G = grid_for([a, b], lo=7)
        G.point(a[0], a[1], "A", RED).point(b[0], b[1], "B")
        dx, dy = b[0] - a[0], b[1] - a[1]
        its.append(mcq(fig(G.svg("coordinate grid with points A and B")) +
                       "Point A is translated to point B. Describe the translation.",
                       mv(dx, dy), describe_cands(dx, dy, i), describe_e(a, b), rnd))
    for p, dx, dy in [((2, 6), 4, -3), ((7, 2), -5, 4), ((1, 1), 6, 5)]:
        q = (p[0] + dx, p[1] + dy)
        others = [c for c in move_cands(p, dx, dy) if c != q][:3]
        pts, ans = pick_letters(q, others, pos)
        G = grid_for([p] + [c[:2] for c in pts], lo=7)
        G.point(p[0], p[1], "P", RED)
        for c in pts:
            G.point(*c)
        its.append(mcq_fixed(fig(G.svg("coordinate grid with point P and points A to D")) +
                             "Point P is translated %s. Which point shows where it lands?" % mv_long(dx, dy),
                             LETTERS, ans, move_e(p, dx, dy) + " That is point %s." % ans))
    shapes = [
        ([(1, 5), (4, 5), (1, 8)], 5, -4, None),
        ([(6, 5), (9, 5), (9, 6), (7, 6), (7, 8), (6, 8)], -5, -4, (6.5, 5.5)),
    ]
    for i, (A, dx, dy, at) in enumerate(shapes):
        B = shift(A, dx, dy)
        G = Grid(10, 8)
        G.poly(A, GREEN, "A", at).poly(B, BLUE, "B", (at[0] + dx, at[1] + dy) if at else None)
        its.append(mcq(fig(G.svg("coordinate grid with shape A and shape B")) +
                       "Shape A is translated to shape B. Describe the translation.", mv(dx, dy), describe_cands(dx, dy, i + 1),
                       "Follow one vertex. The vertex of A at %s moves to %s in B. That is %s. Every vertex moves the same way."
                       % (pair(*A[0]), pair(*B[0]), mv_long(dx, dy)), rnd))
    for i, (shape, p, dx, dy) in enumerate([
        ("A triangle has vertices at (1, 2), (4, 2) and (1, 6).", (4, 2), 5, 1),
        ("A rectangle has vertices at (3, 5), (8, 5), (8, 9) and (3, 9).", (8, 9), -2, -4),
    ]):
        q = (p[0] + dx, p[1] + dy)
        its.append(mcq("%s It is translated %s. What are the new coordinates of the vertex at %s?" % (shape, mv_long(dx, dy), pair(*p)),
                       pair(*q), [pair(*c) for c in move_cands(p, dx, dy, i + 1)],
                       move_e(p, dx, dy) + " Every vertex moves the same way.", rnd))
    tri = [(2, 1), (5, 1), (2, 3)]
    its.append(mcq("A triangle has vertices at %s. It is translated 3 units right and 4 units up. Which list shows the new vertices?" % plist(tri),
                   plist(shift(tri, 3, 4)),
                   [plist(shift(tri, 3, 0)), plist(shift(tri, 4, 3)), plist([(5, 5), (5, 1), (2, 3)])],
                   "Add 3 to every x-coordinate and 4 to every y-coordinate: %s. Move every vertex, not just one."
                   % ", ".join("%s → %s" % (pair(*a), pair(*b)) for a, b in zip(tri, shift(tri, 3, 4))), rnd))
    its.append(mcq("Point B is translated 4 units right and 3 units up. It lands on (6, 8). Where did it start?", "(2, 5)",
                   ["(10, 11)", "(3, 4)", "(2, 8)"],
                   "Work backwards and undo each move. 4 right is undone by 4 left: 6 − 4 = 2. 3 up is undone by 3 down: 8 − 3 = 5. B started at (2, 5).", rnd))
    n, he, his = P.next()
    its.append(mcq("%s translates (6, 4) 2 units left and gets (8, 4). What mistake did %s make?" % (n, he),
                   "%s moved right, not left" % he.capitalize(),
                   ["%s changed the y-coordinate" % he.capitalize(), "%s swapped x and y" % he.capitalize(), "No mistake. %s is right" % he.capitalize()],
                   "Moving left makes the x-coordinate smaller: 6 − 2 = 4. The correct answer is (4, 4). %s added 2, which is a move to the right." % n, rnd))
    its.append(mcq("A point is translated up or down. Which coordinate changes?", "only the y-coordinate",
                   ["only the x-coordinate", "both coordinates", "neither coordinate"],
                   "Up and down is the y direction. The point does not move across, so the x-coordinate stays the same.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Translations and new coordinates", "items": its}


# ------------------------------------------------------------ reflections
def reflect(p, line):
    k, m = line
    return (2 * m - p[0], p[1]) if k == "v" else (p[0], 2 * m - p[1])


def lname(line):
    return ("x = %d" if line[0] == "v" else "y = %d") % line[1]


def lword(line):
    return ("the vertical line x = %d" if line[0] == "v" else "the horizontal line y = %d") % line[1]


def refl_e(p, line, name="The point"):
    k, m = line
    r = reflect(p, line)
    if r == p:
        return "%s %s is on the line of reflection %s, so it does not move: %s." % (name, pair(*p), lname(line), pair(*r))
    if k == "v":
        d = p[0] - m
        side, other = ("left", "right") if d < 0 else ("right", "left")
        return ("%s %s is %s to the %s of the line %s. The image is %s to the %s of it: %d %s %d = %d. "
                "y stays %d. The image is %s." % (name, pair(*p), units(abs(d)), side, lname(line), units(abs(d)), other,
                                                  m, "+" if d < 0 else "−", abs(d), r[0], p[1], pair(*r)))
    d = p[1] - m
    side, other = ("below", "above") if d < 0 else ("above", "below")
    return ("%s %s is %s %s the line %s. The image is %s %s it: %d %s %d = %d. "
            "x stays %d. The image is %s." % (name, pair(*p), units(abs(d)), side, lname(line), units(abs(d)), other,
                                              m, "+" if d < 0 else "−", abs(d), r[1], p[0], pair(*r)))


def refl_kinds(p, line):
    """Mistakes for reflecting a point: (point, why, key)."""
    k, m = line
    r = reflect(p, line)
    if k == "v":
        s = sgn(r[0] - m)
        far, short, stop = (r[0] + s, r[1]), (r[0] - s, r[1]), (m, p[1])
        wrong = (p[0], 2 * m - p[1])
        why_w = "it was flipped up or down, not across the line"
    else:
        s = sgn(r[1] - m)
        far, short, stop = (r[0], r[1] + s), (r[0], r[1] - s), (p[0], m)
        wrong = (2 * m - p[0], p[1])
        why_w = "it was flipped across, not up or down over the line"
    out = [(far, "it is 1 unit too far (the grid lines were counted, starting with 1 on P’s line)", "far"),
           (stop, "it stops on the line of reflection", "stop"),
           (short, "it is 1 unit too close to the line of reflection", "short"),
           (wrong, why_w, "wrong"),
           ((r[1], r[0]), "x and y are swapped", "swap")]
    return [(q, w, k) for q, w, k in out if inside(q) and q != r and q != p]


# ------------------------------------------------------------ A-D panels (small grids with shapes)
def poly_el(pts, col, cs, ox, oy, rows):
    P = lambda p: (ox + p[0] * cs, oy + (rows - p[1]) * cs)
    return ("<polygon points='%s' fill='%s' fill-opacity='0.35' stroke='%s' stroke-width='2.5' stroke-linejoin='round'/>"
            % (" ".join("%.1f,%.1f" % P(p) for p in pts), col, col))


def panel_el(cols, rows, shape, image, cs, ox, oy, line=None, centre=None):
    el = []
    for c in range(1, cols):
        el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>"
                  % (ox + c * cs, oy, ox + c * cs, oy + rows * cs, THIN))
    for r in range(1, rows):
        el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>"
                  % (ox, oy + r * cs, ox + cols * cs, oy + r * cs, THIN))
    el.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>"
              % (ox, oy, cols * cs, rows * cs, INK))
    el.append(poly_el(shape, GREEN, cs, ox, oy, rows))
    el.append(poly_el(image, BLUE, cs, ox, oy, rows))
    if line:
        o = 6
        if line[0] == "v":
            x = ox + line[1] * cs
            seg = (x, oy - o, x, oy + rows * cs + o)
        else:
            y = oy + (rows - line[1]) * cs
            seg = (ox - o, y, ox + cols * cs + o, y)
        el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-dasharray='7 5'/>"
                  % (seg + (MIRROR,)))
    if centre:
        el.append("<circle cx='%.1f' cy='%.1f' r='5' fill='%s'/>" % (ox + centre[0] * cs, oy + (rows - centre[1]) * cs, RED))
    return el


def panel_svg(cols, rows, shape, images, cs, label, line=None, centre=None):
    LW, gap, pad, o = 22, 16, 8, 7
    gw, gh = cols * cs, rows * cs
    W = 2 * pad + 2 * (LW + gw + 2 * o) + gap
    H = 2 * pad + 2 * (gh + 2 * o) + gap
    el = []
    for k, img in enumerate(images):
        cx, cy = k % 2, k // 2
        x0 = pad + cx * (LW + gw + 2 * o + gap)
        y0 = pad + cy * (gh + 2 * o + gap)
        el += panel_el(cols, rows, shape, img, cs, x0 + LW + o, y0 + o, line, centre)
        el.append(text(x0, y0 + o + 16, "ABCD"[k], 18, anchor="start", bold=True))
    if W == H:
        W += 1
    return svg_wrap(W, H, "".join(el), label)


def same(a, b):
    return set(a) == set(b)


def panel_pick(cands, pos, rnd):
    """cands: {'ok': pts, key: pts, ...}. Returns the keys in A-D order and the answer letter."""
    vals = list(cands.values())
    for i in range(len(vals)):
        for j in range(i + 1, len(vals)):
            assert not same(vals[i], vals[j]), "two pictures are the same"
    p = pos.next()
    w = [k for k in cands if k != "ok"]
    rnd.shuffle(w)
    return w[:p] + ["ok"] + w[p:], "ABCD"[p]


REFL_PANELS = [
    (("v", 4), 8, 6, [(1, 1), (2, 1), (2, 3), (3, 3), (3, 4), (1, 4)], ["slide", "far", "updown"]),
    (("h", 4), 7, 8, [(1, 5), (5, 5), (5, 6), (2, 6), (2, 7), (1, 7)], ["slide", "far", "across"]),
]
REFL_WHY = {"slide": "the shape was slid across, not flipped (it faces the same way)",
            "far": "the image is 1 unit too far from the line",
            "updown": "the shape was flipped upside down, not across the line",
            "across": "the shape was flipped left to right, not over the line"}


def refl_panel_q(line, cols, rows, A, wrongs, pos, rnd):
    ok = [reflect(p, line) for p in A]
    xs, ys = [p[0] for p in A], [p[1] for p in A]
    if line[0] == "v":
        slide = shift(A, min(q[0] for q in ok) - min(xs), 0)
        far = shift(ok, 1, 0)
    else:
        slide = shift(A, 0, min(q[1] for q in ok) - min(ys))
        far = shift(ok, 0, -1)
    cx, cy = (min(q[0] for q in ok) + max(q[0] for q in ok)), (min(q[1] for q in ok) + max(q[1] for q in ok))
    updown = [(q[0], cy - q[1]) for q in ok]          # upside down, in the same place as the image
    across = [(cx - q[0], q[1]) for q in ok]          # left to right, in the same place as the image
    allc = {"ok": ok, "slide": slide, "far": far, "updown": updown, "across": across}
    cands = {k: allc[k] for k in ["ok"] + wrongs}
    for k, v in cands.items():
        assert all(0 <= x <= cols and 0 <= y <= rows for x, y in v), k
    keys, ans = panel_pick(cands, pos, rnd)
    svg = panel_svg(cols, rows, A, [cands[k] for k in keys], 14, "four grid pictures A to D with a dashed line of reflection", line=line)
    others = "; ".join("%s: %s" % ("ABCD"[j], REFL_WHY[k]) for j, k in enumerate(keys) if k != "ok")
    e = ("Each vertex of the image must be the same distance from the line as its partner, on the other side. "
         "Only <b>%s</b> is a true mirror image. Others: %s." % (ans, others))
    return mcq_fixed(fig(svg) + "The green shape is reflected in the dashed line. In which picture is the blue image correct?",
                     LETTERS, ans, e)


# ------------------------------------------------------------ set 3: reflections
def set_reflect(rnd, P):
    its = []
    pos = Pos(rnd)
    for p, line in [((3, 4), ("v", 5)), ((8, 2), ("v", 6)), ((2, 1), ("h", 3)), ((6, 9), ("h", 6)),
                    ((1, 7), ("v", 4)), ((5, 3), ("h", 5))]:
        r = reflect(p, line)
        assert inside(r)
        its.append(mcq("Reflect the point %s in %s. What are the coordinates of the image?" % (pair(*p), lword(line)),
                       pair(*r), [pair(*q) for q, w, k in refl_kinds(p, line)], refl_e(p, line), rnd))
    for p, line, pick in [((2, 3), ("v", 4), ["far", "stop", "wrong"]), ((7, 5), ("v", 5), ["far", "stop", "swap"]),
                          ((3, 1), ("h", 3), ["far", "stop", "swap"]), ((5, 6), ("h", 4), ["far", "stop", "wrong"])]:
        r = reflect(p, line)
        K = {k: (q, w) for q, w, k in refl_kinds(p, line)}
        wrong = [K[j] for j in pick]
        pts, ans = pick_letters(r, [q for q, w in wrong], pos)
        where = {(c[0], c[1]): c[2] for c in pts}
        G = grid_for([p] + [c[:2] for c in pts], lo=7, mirror=line)
        G.point(p[0], p[1], "P", RED)
        for c in pts:
            G.point(*c)
        e = (refl_e(p, line, "P") + " That is point %s. " % ans +
             " ".join("Point %s: %s." % (where[q], w) for q, w in wrong))
        its.append(mcq_fixed(fig(G.svg("coordinate grid with a line of reflection, point P and points A to D")) +
                             "Which point is the reflection of point P in the line %s?" % lname(line), LETTERS, ans, e))
    for line, cols, rows, A, wrongs in REFL_PANELS:
        its.append(refl_panel_q(line, cols, rows, A, wrongs, pos, rnd))
    its.append(mcq("Reflect the point (5, 3) in the vertical line x = 5. What are the coordinates of the image?", "(5, 3)",
                   ["(6, 3)", "(3, 5)", "(0, 3)"],
                   refl_e((5, 3), ("v", 5)) + " A point on the line of reflection is its own image.", rnd))
    its.append(mcq("A point is reflected in a horizontal line. Which coordinate changes?", "only the y-coordinate",
                   ["only the x-coordinate", "both coordinates", "neither coordinate"],
                   "A horizontal line goes across. The point flips up or down over it, so only y changes. x stays the same.", rnd))
    its.append(mcq("Point P is 3 units to the left of a vertical line of reflection. Where is its image?", "3 units to the right of the line",
                   ["6 units to the right of the line", "3 units to the left of the line", "4 units to the right of the line"],
                   "In a reflection the image is the same distance from the line as the point, on the other side.", rnd))
    its.append(mcq_num("The point (4, 2) is reflected in the horizontal line y = 5. How many units apart are the point and its image?",
                       6, [3, 5, 7],
                       "(4, 2) is 3 units below y = 5, so the image (4, 8) is 3 units above it. From the point to the image is 3 + 3 = 6 units. "
                       "(3 is only the distance to the line.)", fmt="%d units"))
    its.append(mcq("The points (2, 6) and (8, 6) are reflections of each other. Where is the line of reflection?", "x = 5",
                   ["x = 6", "x = 4", "y = 6"],
                   "The line is halfway between the points. From 2 to 8 is 6 units, and half of 6 is 3. 2 + 3 = 5, so the line is x = 5. "
                   "(y = 6 goes through both points; it is not between them.)", rnd))
    G = Grid(10, 8)
    G.mirror("h", 4)
    G.poly([(1, 1), (4, 1), (1, 3)], GREEN, "A").poly([(1, 8), (4, 8), (1, 6)], BLUE, "B")
    n = P.next()[0]
    its.append(mcq_fixed(fig(G.svg("coordinate grid with a line of reflection, shape A and shape B")) +
                         "%s wants to reflect shape A in the dashed line. Is shape B correct?" % n, CHECK, CHECK[1],
                         "(1, 1) is 3 units below the line y = 4, so its image should be 3 units above, at (1, 7). "
                         "B has that vertex at (1, 8): 1 unit too far."))
    n, he, his = P.next()
    its.append(mcq("%s reflects a right triangle in a vertical line. %s image points the same way as the triangle. What mistake did %s make?"
                   % (n, his.capitalize(), he),
                   "%s slid it instead of flipping it" % he.capitalize(),
                   ["%s made it bigger" % he.capitalize(), "%s reflected it too far" % he.capitalize(), "No mistake. %s is right" % he.capitalize()],
                   "A reflection is a mirror image, so it faces the other way. If the image points the same way, the shape was slid (translated).", rnd))
    rect = [(1, 2), (3, 2), (3, 5), (1, 5)]
    line = ("v", 4)
    r = reflect((1, 5), line)
    its.append(mcq("A rectangle has vertices at %s. It is reflected in %s. What are the new coordinates of the vertex at (1, 5)?"
                   % (plist(rect), lword(line)), pair(*r), [pair(*q) for q, w, k in refl_kinds((1, 5), line)],
                   refl_e((1, 5), line, "The vertex"), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Reflections in a line", "items": its}


# ------------------------------------------------------------ rotations about a vertex
TURNS = {"cw": "90° clockwise", "ccw": "90° counterclockwise", "half": "180°"}
WAYS = {"cw": "right turns into down, down into left, left into up and up into right",
        "ccw": "right turns into up, up into left, left into down and down into right",
        "half": "right turns into left, left into right, up into down and down into up"}


def rot(p, c, kind):
    dx, dy = p[0] - c[0], p[1] - c[1]
    r = {"cw": (dy, -dx), "ccw": (-dy, dx), "half": (-dx, -dy)}[kind]
    return (c[0] + r[0], c[1] + r[1])


def rel(dx, dy):
    a = "" if dx == 0 else ("%d right" % dx if dx > 0 else "%d left" % -dx)
    b = "" if dy == 0 else ("%d up" % dy if dy > 0 else "%d down" % -dy)
    return " and ".join(t for t in (a, b) if t)


def rot_e(p, c, kind, pn="The point", cn="the centre"):
    r = rot(p, c, kind)
    return ("From %s %s, %s %s is %s. In a %s turn, %s. So from %s, the image is %s: %s."
            % (cn, pair(*c), pn[0].lower() + pn[1:] if pn.startswith(("The", "Vertex")) else pn, pair(*p),
               rel(p[0] - c[0], p[1] - c[1]), TURNS[kind], WAYS[kind], pair(*c), rel(r[0] - c[0], r[1] - c[1]), pair(*r)))


def rot_kinds(p, c, kind):
    """Mistakes for a rotation: (point, why)."""
    dx, dy = p[0] - c[0], p[1] - c[1]
    out = []
    if kind == "half":
        out += [(rot(p, c, "cw"), "a 90° turn clockwise, not 180°"), (rot(p, c, "ccw"), "a 90° turn counterclockwise, not 180°")]
    else:
        other = "ccw" if kind == "cw" else "cw"
        out += [(rot(p, c, other), "turned the wrong way (%s)" % TURNS[other]), (rot(p, c, "half"), "a 180° turn, not 90°")]
    out += [((c[0] + dy, c[1] + dx), "the numbers were swapped, but the directions were not turned"),
            ((c[0] - dx, c[1] + dy), "a flip left to right, not a turn"),
            ((c[0] + dx, c[1] - dy), "a flip upside down, not a turn")]
    r = rot(p, c, kind)
    if dx == 0 or dy == 0:
        out.append(((r[0] + sgn(r[0] - c[0]), r[1] + sgn(r[1] - c[1])), "1 unit too far (the grid lines were counted)"))
    res, seen = [], set()
    for q, w in out:
        if inside(q) and q != r and q != p and q != c and q not in seen:
            seen.add(q)
            res.append((q, w))
    return res


ROT_PANELS = [
    ((4, 4), "cw", 8, 8, [(4, 4), (7, 4), (7, 6)], ["ccw", "half", "flip"]),
    ((4, 4), "ccw", 8, 8, [(4, 4), (6, 4), (6, 5), (5, 5), (5, 7), (4, 7)], ["cw", "half", "flip"]),
    ((4, 4), "half", 8, 8, [(4, 4), (7, 4), (7, 5), (5, 5), (5, 6), (4, 6)], ["cw", "ccw", "flip"]),
    ((4, 4), "cw", 8, 8, [(4, 4), (4, 7), (5, 7), (6, 6), (5, 5), (5, 4)], ["ccw", "half", "flip"]),
]
ROT_WHY = {"cw": "a 90° clockwise turn", "ccw": "a 90° counterclockwise turn", "half": "a 180° turn",
           "flip": "a flip (reflection), not a turn"}


def rot_panel_q(c, kind, cols, rows, A, wrongs, pos, rnd):
    allc = {"cw": [rot(p, c, "cw") for p in A], "ccw": [rot(p, c, "ccw") for p in A],
            "half": [rot(p, c, "half") for p in A], "flip": [(2 * c[0] - p[0], p[1]) for p in A]}
    if kind != "cw" and "flip" in wrongs and same(allc["flip"], allc[kind]):
        raise AssertionError("flip equals the answer")
    cands = {"ok": allc[kind]}
    for k in wrongs:
        cands[k] = allc[k]
    for k, v in cands.items():
        assert all(0 <= x <= cols and 0 <= y <= rows for x, y in v), (k, v)
        assert not same(v, A), k
    keys, ans = panel_pick(cands, pos, rnd)
    svg = panel_svg(cols, rows, A, [cands[k] for k in keys], 14, "four grid pictures A to D with a red centre of rotation", centre=c)
    others = "; ".join("%s: %s" % ("ABCD"[j], ROT_WHY[k]) for j, k in enumerate(keys) if k != "ok")
    long_side = [p for p in A if p != c and (p[0] == c[0] or p[1] == c[1])][0]
    r = rot(long_side, c, kind)
    e = ("The red dot does not move. Follow one side: the side from the red dot going %s turns to go %s in a %s turn. "
         "Only <b>%s</b> shows that. Others: %s." % (
             rel(sgn(long_side[0] - c[0]), sgn(long_side[1] - c[1])).replace("1 ", ""),
             rel(sgn(r[0] - c[0]), sgn(r[1] - c[1])).replace("1 ", ""), TURNS[kind], ans, others))
    return mcq_fixed(fig(svg) + "The green shape is rotated %s about the red dot. In which picture is the blue image correct?" % TURNS[kind],
                     LETTERS, ans, e)


# ------------------------------------------------------------ set 4: rotations
def set_rotate(rnd, P):
    its = []
    pos = Pos(rnd)
    its.append(mcq_num("How many degrees is a quarter turn?", 90, [45, 180, 360],
                       "A full turn is 360°. A quarter turn is one of 4 equal parts: 360° ÷ 4 = 90°. A half turn is 180°.", fmt="%d°"))
    its.append(mcq("Which way do the hands of a clock turn?", "clockwise", ["counterclockwise", "up and down", "left and right"],
                   "Clock hands go from 12 to 3 to 6 to 9: that is clockwise. The other way is counterclockwise.", rnd))
    its.append(mcq("A triangle is rotated about its vertex A. Which point stays in the same place?", "vertex A",
                   ["the vertex farthest from A", "every vertex", "no point"],
                   "The centre of rotation does not move. Here the centre is vertex A; every other point turns around it.", rnd))
    its.append(mcq("A shape is rotated 180° clockwise about a point. A copy of it is rotated 180° counterclockwise about the same point. Where do they land?",
                   "in the same place", ["in different places", "one is a mirror image of the other", "one lands twice as far away"],
                   "A half turn is a half turn, whichever way you go. 180° clockwise and 180° counterclockwise end in the same place.", rnd))
    data = [
        ("Rotate the point B (6, 4) 90° clockwise about the point A (3, 4). Where does B land?", (6, 4), (3, 4), "cw", "B", "A"),
        ("A triangle has vertices A (4, 4), B (4, 7) and C (6, 4). It is rotated 90° clockwise about vertex A. Where does vertex B land?",
         (4, 7), (4, 4), "cw", "Vertex B", "vertex A"),
        ("Rotate the point Q (8, 5) 90° counterclockwise about the point P (5, 5). Where does Q land?", (8, 5), (5, 5), "ccw", "Q", "P"),
        ("A rectangle has vertices K (3, 3), L (5, 3), M (5, 6) and N (3, 6). It is rotated 90° clockwise about vertex K. Where does vertex M land?",
         (5, 6), (3, 3), "cw", "Vertex M", "vertex K"),
        ("A triangle has vertices D (5, 3), E (2, 4) and F (5, 6). It is rotated 90° counterclockwise about vertex D. Where does vertex E land?",
         (2, 4), (5, 3), "ccw", "Vertex E", "vertex D"),
        ("Rotate the point S (8, 5) 180° about the point R (6, 4). Where does S land?", (8, 5), (6, 4), "half", "S", "R"),
        ("A triangle has vertices A (4, 4), B (1, 5) and C (4, 7). It is rotated 180° about vertex A. Where does vertex B land?",
         (1, 5), (4, 4), "half", "Vertex B", "vertex A"),
    ]
    for q, p, c, kind, pn, cn in data:
        r = rot(p, c, kind)
        assert inside(r), (q, r)
        its.append(mcq(q, pair(*r), [pair(*x) for x, w in rot_kinds(p, c, kind)], rot_e(p, c, kind, pn, cn), rnd))
    for c, kind, cols, rows, A, wrongs in ROT_PANELS:
        its.append(rot_panel_q(c, kind, cols, rows, A, wrongs, pos, rnd))
    for p, c, kind in [((7, 5), (4, 3), "cw"), ((3, 7), (5, 4), "half")]:
        r = rot(p, c, kind)
        K = rot_kinds(p, c, kind)[:3]
        pts, ans = pick_letters(r, [q for q, w in K], pos)
        where = {(t[0], t[1]): t[2] for t in pts}
        G = grid_for([p, c] + [t[:2] for t in pts], lo=7)
        G.point(p[0], p[1], "P", RED).point(c[0], c[1], "R", INK)
        for t in pts:
            G.point(*t)
        e = rot_e(p, c, kind, "P", "R") + " That is point %s. " % ans + " ".join("Point %s: %s." % (where[q], w) for q, w in K)
        its.append(mcq_fixed(fig(G.svg("coordinate grid with point P, centre R and points A to D")) +
                             "Point P is rotated %s about point R. Which point is the image?" % TURNS[kind], LETTERS, ans, e))
    for p, c, r in [((6, 4), (4, 4), (4, 2)), ((5, 4), (3, 3), (1, 2))]:
        kind = [k for k in TURNS if rot(p, c, k) == r]
        assert len(kind) == 1
        kind = kind[0]
        its.append(mcq_fixed("A shape is rotated about the vertex %s. Another vertex moves from %s to %s. Describe the rotation."
                             % (pair(*c), pair(*p), pair(*r)), ROTS, TURNS[kind],
                             "%s is %s from the centre. %s is %s from the centre. %s" % (
                                 pair(*p), rel(p[0] - c[0], p[1] - c[1]), pair(*r), rel(r[0] - c[0], r[1] - c[1]),
                                 "Right turned into down: that is a quarter turn clockwise." if kind == "cw" else
                                 "Right turned into left and up turned into down: that is a half turn, 180°.")))
    n, he, his = P.next()
    H = he.capitalize()
    p, c = (7, 3), (4, 3)
    its.append(mcq("%s rotates the point %s 90° clockwise about %s and gets %s. What mistake did %s make?"
                   % (n, pair(*p), pair(*c), pair(*rot(p, c, "ccw")), he),
                   "%s turned it counterclockwise" % H,
                   ["%s turned it 180°" % H, "%s swapped x and y" % H, "No mistake. %s is right" % H],
                   "%s is a quarter turn counterclockwise. %s" % (pair(*rot(p, c, "ccw")), rot_e(p, c, "cw")), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Rotations of 90° and 180° about a vertex", "items": its}


# ------------------------------------------------------------ set 5: which transformation? and word problems
def classify(A, B):
    """Every way (translation, reflection in a vertical or horizontal line, rotation about a grid point) A maps onto B."""
    SB = set(B)
    out = set()
    for dx in range(-10, 11):
        for dy in range(-10, 11):
            if set(shift(A, dx, dy)) == SB:
                out.add("a translation")
    for m2 in range(0, 21):
        if {(m2 - x, y) for x, y in A} == SB or {(x, m2 - y) for x, y in A} == SB:
            out.add("a reflection")
    for cx in range(-10, 21):
        for cy in range(-10, 21):
            for k in TURNS:
                if {rot(p, (cx, cy), k) for p in A} == SB:
                    out.add("a rotation")
    return out


def set_which(rnd, P):
    its = []
    Lr = [(1, 5), (5, 5), (5, 6), (2, 6), (2, 8), (1, 8)]
    Lh = [(1, 1), (5, 1), (5, 2), (2, 2), (2, 4), (1, 4)]
    T = [(2, 5), (6, 5), (2, 7)]
    cases = [
        ([(1, 1), (4, 1), (1, 3)], [(6, 4), (9, 4), (6, 6)], "a translation", None,
         "B faces the same way as A and is the same size. Every vertex moved 5 units right and 3 units up, for example (1, 1) → (6, 4). That is a translation."),
        ([(1, 2), (3, 2), (3, 3), (2, 3), (2, 6), (1, 6)], [reflect(p, ("v", 5)) for p in [(1, 2), (3, 2), (3, 3), (2, 3), (2, 6), (1, 6)]],
         "a reflection", ((1.5, 2.5), (8.5, 2.5)),
         "B is a mirror image of A: the foot of the L points the other way. It is a reflection in the line x = 5. The size has not changed."),
        (Lr, [rot(p, (5, 5), "cw") for p in Lr], "a rotation", ((3, 5.5), (5.5, 6.5)),
         "In A the long arm of the L lies flat along the bottom. In B it stands straight up. A slide or a flip cannot make a flat arm "
         "stand up, but a turn can: B is A turned 90° clockwise about the vertex (5, 5)."),
        (Lh, [rot(p, (5, 2), "half") for p in Lh], "a rotation", ((1.5, 2.5), (8.5, 1.5)),
         "B is A turned upside down and back to front: a half turn (180°) about the vertex (5, 2). A single flip would change only one of these."),
        (T, [reflect(p, ("h", 4)) for p in T], "a reflection", None,
         "In A the right angle is at the bottom left; in B it is at the top left. B is A flipped over the line y = 4: "
         "each vertex is the same distance from the line on the other side, for example (2, 5) → (2, 3). That is a reflection."),
        ([(1, 4), (5, 4), (5, 6), (1, 6)], [(7, 1), (9, 1), (9, 2), (7, 2)], "it changed size", None,
         "A is 4 units by 2 units. B is only 2 units by 1 unit, so B is smaller. A translation, a reflection or a rotation never changes the size."),
    ]
    for A, B, ans, at, e in cases:
        if ans != "it changed size":
            assert classify(A, B) == {ans}, (ans, classify(A, B))
        G = Grid(10, 9 if max(p[1] for p in A + B) > 8 else 8)
        G.poly(A, GREEN, "A", at[0] if at else None).poly(B, BLUE, "B", at[1] if at else None)
        its.append(mcq_fixed(fig(G.svg("coordinate grid with shape A and shape B")) +
                             "What happened to shape A to make shape B?", MOVES, ans, e))
    n, he, his = P.next()
    its.append(mcq("In a coding lesson, %s’s robot starts at (1, 2). The code says: move 4 right, then move 3 up. Where does the robot stop?" % n,
                   "(5, 5)", [pair(*c) for c in move_cands((1, 2), 4, 3, 1)], move_e((1, 2), 4, 3), rnd))
    n, he, his = P.next()
    its.append(mcq("%s’s robot is at (2, 7). %s wants it to stop at (6, 3). Which code works?" % (n, he.capitalize()),
                   "4 right, 4 down", describe_cands(4, -4, 2), describe_e((2, 7), (6, 3), "The start", "the end"), rnd))
    n, he, his = P.next()
    its.append(mcq("In a board game, each turn moves a counter 2 units right. %s’s counter starts at (1, 4). Where is it after 3 turns?" % n,
                   "(7, 4)", ["(3, 4)", "(6, 4)", "(4, 7)"],
                   "3 turns is 3 × 2 = 6 units right. x: 1 + 6 = 7. y stays 4. The counter is at (7, 4).", rnd))
    its.append(mcq("On a map of a campsite, the fire pit is at (3, 5) and the canoe dock is at (8, 1). Describe the translation from the fire pit to the dock.",
                   "5 right, 4 down", describe_cands(5, -4, 1), describe_e((3, 5), (8, 1), "The fire pit", "the dock"), rnd))
    n, he, his = P.next()
    its.append(mcq("On a hockey play diagram, %s skates from (2, 3), 6 units right and 4 units up. Where does %s stop?" % (n, he),
                   "(8, 7)", [pair(*c) for c in move_cands((2, 3), 6, 4, 2)], move_e((2, 3), 6, 4), rnd))
    n, he, his = P.next()
    its.append(mcq("%s makes a paper snowflake design for the class window. The design is symmetrical in the line x = 5. "
                   "One tip is at (2, 6). Where is the matching tip?" % n,
                   "(8, 6)", [pair(*q) for q, w, k in refl_kinds((2, 6), ("v", 5))], refl_e((2, 6), ("v", 5), "The tip"), rnd))
    its.append(mcq("A school crest is symmetrical in the horizontal line y = 5. One corner is at (3, 2). Where is the matching corner?", "(3, 8)",
                   [pair(*q) for q, w, k in refl_kinds((3, 2), ("h", 5))], refl_e((3, 2), ("h", 5), "The corner"), rnd))
    bed = [(1, 2), (3, 2), (3, 4), (1, 4)]
    img = [reflect(p, ("v", 5)) for p in bed]
    its.append(mcq("A garden has a path along the line x = 5. A flower bed with vertices at %s is reflected in the path to make a matching bed. "
                   "Which list shows the vertices of the new bed?" % plist(bed), plist(img),
                   [plist(shift(img, 1, 0)), plist(shift(bed, 5, 0)), plist([reflect(p, ("h", 5)) for p in bed])],
                   "Each vertex goes the same distance on the other side of x = 5: (1, 2) is 4 units left, so its image is 4 units right, at (9, 2). "
                   "(3, 2) is 2 units left, so its image is (7, 2).", rnd))
    n, he, his = P.next()
    p, c = (7, 6), (5, 5)
    its.append(mcq("%s draws a pinwheel for a Terry Fox Run poster. One blade tip is at %s. The next blade is the first one rotated "
                   "90° counterclockwise about the centre %s. Where is the next tip?" % (n, pair(*p), pair(*c)), pair(*rot(p, c, "ccw")),
                   [pair(*x) for x, w in rot_kinds(p, c, "ccw")], rot_e(p, c, "ccw", "The tip", "the centre"), rnd))
    n, he, his = P.next()
    p, c = (8, 7), (6, 6)
    its.append(mcq("%s makes a quilt pattern. A triangle has a vertex at %s. %s rotates the triangle 180° about its vertex %s. "
                   "Where does the vertex at %s go?" % (n, pair(*p), he.capitalize(), pair(*c), pair(*p)), pair(*rot(p, c, "half")),
                   [pair(*x) for x, w in rot_kinds(p, c, "half")], rot_e(p, c, "half", "The vertex", "the centre"), rnd))
    n, he, his = P.next()
    its.append(mcq_fixed("%s turns a puzzle piece about its corner at (4, 4). Another corner moves from (6, 4) to (4, 6). How did %s turn it?" % (n, he),
                         ROTS, "90° counterclockwise",
                         "(6, 4) is 2 right of the centre. (4, 6) is 2 up from the centre. Right turned into up: that is a quarter turn counterclockwise."))
    its.append(mcq("In a game, a counter at (7, 3) is reflected in the horizontal line y = 4, then translated 2 units left. Where does it end?",
                   "(5, 5)", ["(9, 5)", "(5, 3)", "(5, 6)"],
                   "Reflect first: (7, 3) is 1 unit below y = 4, so the image is 1 unit above, at (7, 5). Then left 2: 7 − 2 = 5. It ends at (5, 5).", rnd))
    its.append(mcq("A rug on a floor plan covers 6 squares. It is rotated 90° about one corner. Which sentence is true?",
                   "It still covers 6 squares", ["It now covers 9 squares", "It now covers 3 squares", "It now covers 12 squares"],
                   "A rotation turns the rug but does not stretch it. The side lengths, angles and area stay the same, so it still covers 6 squares.", rnd))
    its.append(mcq("Which move makes a mirror image of a shape?", "a reflection", ["a translation", "a rotation of 180°", "a rotation of 90°"],
                   "A reflection flips the shape over a line, so the image faces the other way like in a mirror. "
                   "A translation slides the shape and a rotation turns it; neither flips it.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Which transformation? Word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    G = Grid(7, 6)
    G.arrow((0, 0), (4, 0)).arrow((4, 0), (4, 3))
    G.note(2, 0.5, "right 4").note(4.2, 1.5, "up 3", anchor="start")
    G.point(4, 3, "A", where=(1, 1))
    plot = G.svg("coordinate grid: from the origin go right 4, then up 3 to point A at (4, 3)")
    G = Grid(10, 7)
    A = [(1, 4), (4, 4), (1, 6)]
    G.poly(A, GREEN, "A").poly(shift(A, 4, -3), BLUE, "B")
    G.arrow((4, 4), (8, 4)).arrow((8, 4), (8, 1))
    G.note(6, 4.5, "4 right").note(8.2, 2.5, "3 down", anchor="start")
    trans = G.svg("triangle A translated 4 units right and 3 units down to triangle B")
    G = Grid(10, 6)
    G.mirror("v", 5)
    T = [(1, 1), (4, 1), (1, 4)]
    G.poly(T, GREEN, "A").poly([reflect(p, ("v", 5)) for p in T], BLUE, "B")
    refl = G.svg("triangle A reflected in the line x = 5 to make triangle B")
    G = Grid(8, 8)
    T = [(2, 5), (5, 5), (5, 7)]
    G.poly(T, GREEN, "A").poly([rot(p, (2, 5), "cw") for p in T], BLUE, "B", (2.6, 2.7))
    G.arc((2, 5), (5, 5), (2, 2), True)
    G.point(2, 5, None, RED)
    rota = G.svg("triangle A rotated 90° clockwise about its vertex (2, 5) to make triangle B")
    return (
        "<h2>Reading and plotting points</h2>"
        "<p>A point on a grid is named by two numbers, called <b>coordinates</b>: (x, y). "
        "Start at the <b>origin</b>, (0, 0). The first number, <b>x</b>, tells you how far to go <b>across</b>. "
        "The second number, <b>y</b>, tells you how far to go <b>up</b>.</p>"
        "<figure class='sn-fig'>" + plot +
        "<figcaption>To plot (4, 3), start at the origin. Go right 4, then up 3. Point A is at (4, 3), not (3, 4).</figcaption></figure>" +
        ex("Example", "A point is 2 units right of the origin and 6 units up. Name it.",
           "Across first: x = 2. Then up: y = 6.", "(2, 6)") +
        "<h2>Translations: slide the shape</h2>"
        "<p>A <b>translation</b> slides a shape left or right and up or down. It does not turn or flip. "
        "Every vertex moves the same number of units in the same direction.</p>"
        "<figure class='sn-fig'>" + trans +
        "<figcaption>Triangle A is translated 4 units right and 3 units down to make B. Follow one vertex: (4, 4) → (8, 1).</figcaption></figure>" +
        table(["Move", "What changes", "Example from (5, 4)"], [
            ["right 2", "x gets bigger", "(7, 4)"],
            ["left 2", "x gets smaller", "(3, 4)"],
            ["up 2", "y gets bigger", "(5, 6)"],
            ["down 2", "y gets smaller", "(5, 2)"],
        ]) +
        ex("Example", "Describe the translation from (2, 7) to (8, 3).",
           "Across: 2 to 8 is 6 units right. Up and down: 7 to 3 is 4 units down.", "6 units right and 4 units down") +
        "<h2>Reflections: flip over a line</h2>"
        "<p>A <b>reflection</b> flips a shape over a <b>line of reflection</b>. The image is a mirror image. "
        "Each vertex ends up the <b>same distance</b> from the line, on the other side.</p>"
        "<p>The line <b>x = 5</b> goes straight up through 5 on the x-axis. "
        "The line <b>y = 4</b> goes straight across through 4 on the y-axis.</p>"
        "<figure class='sn-fig'>" + refl +
        "<figcaption>(1, 4) is 4 units left of x = 5, so its image is 4 units right, at (9, 4). With a vertical line, only x changes.</figcaption></figure>" +
        ex("Example", "Reflect (3, 4) in the line x = 5.",
           "(3, 4) is 2 units left of the line. Go 2 units right of the line: 5 + 2 = 7. y stays 4.", "(7, 4)") +
        "<h2>Rotations: turn about a point</h2>"
        "<p>A <b>rotation</b> turns a shape about a point called the <b>centre of rotation</b>. In Grade 5 the centre is often a vertex of the shape. "
        "The centre does not move. Say how far (90° is a quarter turn, 180° is a half turn) and which way: "
        "<b>clockwise</b> (the way clock hands move) or <b>counterclockwise</b>.</p>"
        "<figure class='sn-fig'>" + rota +
        "<figcaption>Triangle A turns 90° clockwise about the red vertex (2, 5). The side that went 3 right now goes 3 down, so (5, 5) moves to (2, 2).</figcaption></figure>" +
        "<p>To rotate a point, describe it from the centre, then turn each direction.</p>" +
        table(["Turn", "right becomes", "up becomes"], [
            ["90° clockwise", "down", "right"],
            ["90° counterclockwise", "up", "left"],
            ["180° (either way)", "left", "down"],
        ]) +
        ex("Example", "Rotate (6, 4) 90° counterclockwise about (3, 4).",
           "(6, 4) is 3 right of the centre. In a quarter turn counterclockwise, right turns into up. So the image is 3 up from (3, 4).",
           "(3, 7)") +
        "<h2>What stays the same</h2>"
        "<p>After a translation, a reflection or a rotation, the shape is in a new place, but it is the <b>same shape and size</b>. "
        "The side lengths, the angles and the area all stay the same.</p>" +
        table(["", "Translation", "Reflection", "Rotation"], [
            ["What happens", "slides", "flips over a line", "turns about a point"],
            ["Which way it faces", "the same way", "mirror image", "turned"],
            ["Size and angles", "the same", "the same", "the same"],
        ]) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Swapping x and y: plotting (2, 5) at (5, 2)", "Go across first (x), then up (y)"],
            ["Counting grid lines, starting with 1 on the start line", "Count the spaces you jump"],
            ["Adding for “left” or “down”", "Left and down make the number smaller"],
            ["Stopping on the line of reflection, or going past it", "Go the same distance on the other side"],
            ["Turning the wrong way", "Clockwise goes like clock hands: from 12 towards 3"],
            ["Mixing up 90° and 180°", "90° is a quarter turn; 180° is a half turn"],
        ])
    )


FAQ = [
    {"q": "What do Grade 5 students learn about transformations in the Ontario math curriculum?",
     "a": "In Grade 5 (Spatial Sense, E1.4 and E1.5), students plot and read points in the first quadrant, describe translations with coordinates, "
          "and perform reflections and rotations up to 180° on a grid, predicting where each vertex will land."},
    {"q": "How do you remember which coordinate comes first?",
     "a": "The x-coordinate comes first: go across, then up. Many teachers say “walk before you climb”, so (2, 5) is 2 across and 5 up."},
    {"q": "How do you rotate a shape 90° clockwise about a vertex?",
     "a": "Keep that vertex still. Describe each other vertex from it, then turn the directions a quarter turn the way clock hands move: right becomes down and up becomes right."},
    {"q": "What is the difference between a translation, a reflection and a rotation?",
     "a": "A translation slides a shape, a reflection flips it over a line to make a mirror image, and a rotation turns it about a point. "
          "None of them changes the shape’s size or angles."},
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
        assert sum(need) == len(free), (s["title"], cnt, len(free))
        targets = [i for i in range(4) for _ in range(need[i])]
        rnd.shuffle(targets)
        for it, t in zip(free, targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t
        final = [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


def gen_unit():
    rnd = random.Random(45816)
    P = People(rnd)
    sets = [set_read(rnd, P), set_translate(rnd, P), set_reflect(rnd, P), set_rotate(rnd, P), set_which(rnd, P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-5", "slug": "coordinates-and-transformations", "sort": 16,
        "updated": UPDATED, "pdf_url": "",
        "title": "Coordinates and Transformations: Translations, Reflections and Rotations on a Grid",
        "seo_title": "Grade 5 Coordinates and Transformations Worksheets: Translations, Reflections, Rotations (Free, Answer Key)",
        "short_title": "Coordinates and transformations",
        "domain": "Spatial Sense",
        "standard_code": "Grade 5: E1.5",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Describe and perform translations, reflections, and rotations up to 180° on a grid, and predict the results of these transformations",
        "meta_desc": "Free Grade 5 math worksheets on coordinates and transformations for the Ontario curriculum: read and plot points in the first quadrant, translate points and shapes, reflect them in a line and rotate them 90° and 180° about a vertex. 100 questions with an answer key.",
        "key_big": "A translation slides, a reflection flips, a rotation turns. The shape never changes size.",
        "key_sub": "In (x, y), go across first, then up. In a translation every vertex moves the same way. In a reflection each vertex stays the same distance from the line. In a rotation the centre does not move.",
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
        mark_large(u, "(coordinate grid|four grid pictures)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
