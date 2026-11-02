# -*- coding: utf-8 -*-
"""
CA (Ontario) Grade 2 Math: Maps and directions (Ontario Mathematics Curriculum 2020, E1.4 and E1.5)
  python3 tools/gen_caon_math_g2_maps.py
HTML attributes use single quotes (no backslashes in the JSON).

Grade 2 students create and read simple maps of familiar places (the classroom, the schoolyard, a park,
the neighbourhood), describe the relative positions of objects (left of, right of, between, above, below,
next to) and the movements needed to get from one object to another (3 squares right, then 2 up).
Left and right on a map are the left and right of the page. No compass points and no turns of a robot.
Every map is a model in code (cells of a grid). Every answer is worked out from that model.
Wrong answers come from real mistakes: left and right mixed up, up and down mixed up, counting the start
square, the two moves swapped, one square too far, choosing the path that looks shorter, a side view
instead of a view from above. Canadian English.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
INK = "#2b2b2b"
GRID = "#b9b3a9"
YELLOW = "#f2c94c"
RED = "#e06666"
BLUE = "#9fc5e8"
DBLUE = "#2f6ea3"
ORANGE = "#f6a04d"
PINK = "#f4a6c0"
BROWN = "#a0692a"
STONE = "#b7b2aa"
WOOD = "#d9b382"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Noah", "Aiden", "Lucas", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]

DIRS = ["up", "right", "down", "left"]          # clockwise order on the page
DV = [(0, -1), (1, 0), (0, 1), (-1, 0)]
VEC = dict(zip(DIRS, DV))
OPP = {"up": "down", "down": "up", "left": "right", "right": "left"}


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
    assert len(pick) == 3, (re.sub("<svg.*?</svg>", "[svg]", q), correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def mcq_fixed(q, choices, correct, e):
    """Choices keep their order (A B C D pictures, numbers from small to large)."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fixed": True}


def mcq_num(q, correct, cands, e):
    ch = []
    for c in cands:
        if c > 0 and c != correct and c not in ch:
            ch.append(c)
    ch = sorted([correct] + ch[:3])
    assert len(ch) == 4, (q, ch)
    return mcq_fixed(q, [str(c) for c in ch], str(correct), e)


def num_cands(n, p):
    """Wrong counts for a count of n so that the answer sits in place p (0-3) once sorted.
    n + 1 (the start square counted) and n − 1 (one square short) come first."""
    return {0: [n + 1, n + 2, n + 3], 1: [n - 1, n + 1, n + 2], 2: [n - 2, n - 1, n + 1], 3: [n - 3, n - 2, n - 1]}[p]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs, bold=False):
    """Approximate text width in px (Arial)."""
    return len(str(t)) * fs * (0.6 if bold else 0.55)


def text(x, y, t, fs=14, anchor="middle", bold=True, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def P(pts):
    return " ".join("%.1f,%.1f" % p for p in pts)


def add(a, b, k=1.0):
    return (a[0] + b[0] * k, a[1] + b[1] * k)


def sq(n):
    return "%d square%s" % (n, "" if n == 1 else "s")


def step(cell, d, n=1):
    v = VEC[d]
    return (cell[0] + v[0] * n, cell[1] + v[1] * n)


def walk(start, moves):
    x = start
    for d, n in moves:
        x = step(x, d, n)
    return x


def moves_txt(moves):
    return ", then ".join("%s %s" % (sq(n), d) for d, n in moves)


def moves_short(moves):
    return ", ".join("%d %s" % (n, d) for d, n in moves)


def mistake_moves(moves):
    """Moves a student makes by mistake (most common first)."""
    out = []
    flip = lambda m, ax: [(OPP[d] if d in ax else d, n) for d, n in m]
    if any(d in ("left", "right") for d, n in moves):
        out.append(("lr", flip(moves, ("left", "right"))))
    if any(d in ("up", "down") for d, n in moves):
        out.append(("ud", flip(moves, ("up", "down"))))
    out.append(("start", [(d, n - 1) for d, n in moves]))           # counted the start square each time
    if len(moves) == 2 and moves[0][1] != moves[1][1]:
        out.append(("swap", [(moves[0][0], moves[1][1]), (moves[1][0], moves[0][1])]))
    for i in range(len(moves)):
        out.append(("plus", [(d, n + 1 if j == i else n) for j, (d, n) in enumerate(moves)]))
    for i in range(len(moves)):
        if moves[i][1] > 1:
            out.append(("minus", [(d, n - 1 if j == i else n) for j, (d, n) in enumerate(moves)]))
    out.append(("both", flip(moves, ("left", "right", "up", "down"))))
    if len(moves) == 1:
        d, n = moves[0]
        for d2 in DIRS:
            if d2 not in (d, OPP[d]):
                out.append(("axis", [(d2, n)]))
    return out


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her", "her") for n in GIRLS] + [(n, "he", "his", "him") for n in BOYS]
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


# ------------------------------------------------------------ small pictures
def star_pts(cx, cy, s, n=5):
    out = []
    for i in range(2 * n):
        r = s if i % 2 == 0 else s * 0.45
        t = math.radians(90 + 180.0 * i / n)
        out.append((cx + r * math.cos(t), cy - r * math.sin(t)))
    return out


def icon(kind, cx, cy, s=14):
    k = s / 18.0
    st = "stroke='%s' stroke-width='2' stroke-linejoin='round'" % GREEN
    if kind == "tree":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s'/>" % (cx - 3 * k, cy + 2 * k, 6 * k, 15 * k, BROWN) +
                "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#7cc48a' %s/>" % (cx, cy - 4 * k, 12 * k, st))
    if kind == "flag":
        return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5' stroke-linecap='round'/>"
                % (cx - 8 * k, cy - 16 * k, cx - 8 * k, cy + 16 * k, INK) +
                "<polygon points='%s' fill='%s' stroke='#a33' stroke-width='1.5' stroke-linejoin='round'/>"
                % (P([(cx - 7 * k, cy - 15 * k), (cx + 14 * k, cy - 8 * k), (cx - 7 * k, cy - 1 * k)]), RED))
    if kind == "star":
        return "<polygon points='%s' fill='%s' stroke='%s' stroke-width='2' stroke-linejoin='round'/>" % (
            P(star_pts(cx, cy + 1.5 * k, 17 * k)), YELLOW, BROWN)
    if kind == "house":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#f3e3c3' stroke='%s' stroke-width='2'/>"
                % (cx - 12 * k, cy - 2 * k, 24 * k, 18 * k, BROWN) +
                "<polygon points='%s' fill='%s' stroke='%s' stroke-width='2' stroke-linejoin='round'/>"
                % (P([(cx - 16 * k, cy - 1 * k), (cx, cy - 16 * k), (cx + 16 * k, cy - 1 * k)]), RED, "#a33") +
                "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s'/>" % (cx - 3.5 * k, cy + 6 * k, 7 * k, 10 * k, BROWN))
    if kind == "bench":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='1.5' fill='%s' stroke='#6b4316' stroke-width='1.8'/>"
                % (cx - 17 * k, cy - 2 * k, 34 * k, 5 * k, WOOD) +
                "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='1.5' fill='%s' stroke='#6b4316' stroke-width='1.8'/>"
                % (cx - 17 * k, cy - 12 * k, 34 * k, 5 * k, WOOD) +
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#6b4316' stroke-width='2.4'/>" % (cx - 13 * k, cy + 3 * k, cx - 13 * k, cy + 15 * k) +
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#6b4316' stroke-width='2.4'/>" % (cx + 13 * k, cy + 3 * k, cx + 13 * k, cy + 15 * k))
    if kind == "bed":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='2' fill='#b9d4ee' stroke='#3d6f99' stroke-width='1.8'/>"
                % (cx - 12 * k, cy - 16 * k, 24 * k, 32 * k) +
                "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='2' fill='#ffffff' stroke='#3d6f99' stroke-width='1.5'/>"
                % (cx - 8 * k, cy - 13 * k, 16 * k, 7 * k))
    if kind == "desk":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='1.5' fill='%s' stroke='#6b4316' stroke-width='1.8'/>"
                % (cx - 16 * k, cy - 10 * k, 32 * k, 20 * k, WOOD))
    if kind == "door":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#f3e3c3' stroke='#6b4316' stroke-width='1.8'/>"
                % (cx - 9 * k, cy - 16 * k, 18 * k, 32 * k) +
                "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx + 4.5 * k, cy + 1 * k, 2 * k, INK))
    if kind == "ball":
        r = 14 * k
        return ("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='#3d6f99' stroke-width='2'/>" % (cx, cy, r, BLUE) +
                "<path d='M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f' fill='none' stroke='#3d6f99' stroke-width='2'/>"
                % (cx - r, cy, cx, cy - 12 * k, cx + r, cy) +
                "<path d='M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f' fill='none' stroke='#3d6f99' stroke-width='2'/>"
                % (cx - r, cy, cx, cy + 12 * k, cx + r, cy))
    raise KeyError(kind)


def robot(cx, cy, d, col=GREEN, r=12):
    """A round robot (or a person seen from above) with a white arrow showing the way it faces."""
    u = DV[d]
    nr = (-u[1], u[0])
    tip = (cx + u[0] * r * 0.75, cy + u[1] * r * 0.75)
    b = (cx - u[0] * r * 0.35, cy - u[1] * r * 0.35)
    return ("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s'/>" % (cx, cy, r, col) +
            "<polygon points='%s' fill='#ffffff'/>" % P([tip, add(b, nr, r * 0.55), add(b, nr, -r * 0.55)]))


# ------------------------------------------------------------ labelled grid maps
class Map:
    """A grid map. items: (name, col, row, w, h, kind). kind: b building, g grass, w water, o other, r red."""
    FILLS = {"b": ("#f3e3c3", BROWN), "g": (FILL, GREEN), "w": (BLUE, "#3d6f99"), "o": ("#fff1a8", "#b38f00"),
             "r": ("#f8d7d7", "#a33")}

    def __init__(self, cols, rows, items, cw=70, ch=46, fs=14):
        self.cols, self.rows, self.cw, self.ch, self.fs = cols, rows, cw, ch, fs
        self.items = items
        self.cell = {}
        self.where = {}
        for name, c, r, w, h, kind in items:
            assert name not in self.where, name
            cells = [(c + i, r + j) for i in range(w) for j in range(h)]
            for x in cells:
                assert 0 <= x[0] < cols and 0 <= x[1] < rows, (name, x)
                assert x not in self.cell, ("two things in one square", name, x)
                self.cell[x] = name
            self.where[name] = cells
            for ln in self.lines(name, w):
                assert tw(ln, fs) <= w * cw - 10, ("label too wide", ln)
            assert len(self.lines(name, w)) * 15 <= h * ch - 8, name
        self.ox = self.oy = 4

    def lines(self, name, w):
        if tw(name, self.fs) <= w * self.cw - 10 or " " not in name:
            return [name]
        a, b = name.split(" ", 1)
        return [a, b]

    def at(self, cell):
        return self.cell.get(cell)

    def single(self, name):
        cs = self.where[name]
        assert len(cs) == 1, name
        return cs[0]

    def inside(self, cell):
        return 0 <= cell[0] < self.cols and 0 <= cell[1] < self.rows

    def centre(self, cell):
        return (self.ox + cell[0] * self.cw + self.cw / 2.0, self.oy + cell[1] * self.ch + self.ch / 2.0)

    def size(self):
        return self.ox + self.cols * self.cw + 4, self.oy + self.rows * self.ch + 4

    def svg(self, label, marks=(), path=None):
        """marks: (cell, kind, arg) kind 'letter' (arg = A-D), 'dot', 'person' (arg = facing 0-3), 'icon'.
        path: list of cells, drawn as a dashed route with an arrow."""
        cw, ch, ox, oy = self.cw, self.ch, self.ox, self.oy
        s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff'/>" % (ox, oy, self.cols * cw, self.rows * ch)]
        for i in range(self.cols + 1):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>" % (ox + i * cw, oy, ox + i * cw, oy + self.rows * ch, GRID))
        for j in range(self.rows + 1):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>" % (ox, oy + j * ch, ox + self.cols * cw, oy + j * ch, GRID))
        for name, c, r, w, h, kind in self.items:
            fl, stc = self.FILLS[kind]
            x, y = ox + c * cw + 3, oy + r * ch + 3
            s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='5' fill='%s' stroke='%s' stroke-width='1.6'/>"
                     % (x, y, w * cw - 6, h * ch - 6, fl, stc))
            ls = self.lines(name, w)
            cx, cy = ox + (c + w / 2.0) * cw, oy + (r + h / 2.0) * ch
            for k, ln in enumerate(ls):
                yy = cy + 5 + (k - (len(ls) - 1) / 2.0) * 15
                s.append(text(cx, yy, ln, self.fs, bold=False))
        if path:
            pts = [self.centre(c) for c in path]
            s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='3' stroke-dasharray='6 4' stroke-linecap='round'/>"
                     % (P(pts[:-1] + [shorten(pts[-2], pts[-1], 22)]), RED))
            s.append(arrowhead(pts[-2], pts[-1], 13, RED))
        for cell, kind, arg in marks:
            assert self.inside(cell), cell
            cx, cy = self.centre(cell)
            assert cell not in self.cell, ("mark on a place", cell)
            if kind == "letter":
                s.append("<circle cx='%.1f' cy='%.1f' r='13' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (cx, cy, GREEN))
                s.append(text(cx, cy + 6, arg, 17))
            elif kind == "dot":
                s.append("<circle cx='%.1f' cy='%.1f' r='11' fill='%s' stroke='#7a1f1f' stroke-width='2'/>" % (cx, cy, RED))
            elif kind == "person":
                s.append(robot(cx, cy, arg, RED, 13))
            elif kind == "icon":
                s.append(icon(arg, cx, cy, 14))
        W, H = self.size()
        return svg_wrap(W, H, "".join(s), label)


def shorten(a, b, d):
    L = math.hypot(b[0] - a[0], b[1] - a[1])
    return (b[0] - (b[0] - a[0]) * d / L, b[1] - (b[1] - a[1]) * d / L)


def arrowhead(a, b, back, col):
    L = math.hypot(b[0] - a[0], b[1] - a[1])
    u = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
    tip = (b[0] - u[0] * back, b[1] - u[1] * back)
    base = (tip[0] - u[0] * 12, tip[1] - u[1] * 12)
    nr = (-u[1], u[0])
    return "<polygon points='%s' fill='%s'/>" % (P([tip, (base[0] + nr[0] * 7, base[1] + nr[1] * 7), (base[0] - nr[0] * 7, base[1] - nr[1] * 7)]), col)


def neighbours(M, name):
    out = []
    for c in M.where[name]:
        for d in DIRS:
            n = M.at(step(c, d))
            if n and n != name and n not in out:
                out.append(n)
    return out


def between_all(M, a, b):
    """Places that lie between a and b in one straight row or column, filling every square in the middle."""
    found = set()
    for ca in M.where[a]:
        for cb in M.where[b]:
            if ca[0] == cb[0] or ca[1] == cb[1]:
                dx = (cb[0] > ca[0]) - (cb[0] < ca[0])
                dy = (cb[1] > ca[1]) - (cb[1] < ca[1])
                cells = []
                x = (ca[0] + dx, ca[1] + dy)
                while x != cb:
                    cells.append(x)
                    x = (x[0] + dx, x[1] + dy)
                names = {M.at(x) for x in cells}
                if cells and len(names) == 1 and None not in names and a not in names and b not in names:
                    found |= names
    return found


def beside(M, name, d):
    """The place in the square just next to `name` in page direction d (all squares of name agree)."""
    got = set()
    for c in M.where[name]:
        n = M.at(step(c, d))
        if n != name:
            got.add(n)
    got.discard(None)
    return got


def dist(M, a, b):
    return min(abs(p[0] - q[0]) + abs(p[1] - q[1]) for p in M.where[a] for q in M.where[b])


def the(n):
    return "the " + n


GC, GR, CS = 6, 5, 36


def grid_svg(objs, cols=GC, rows=GR, C=CS, label="grid"):
    """objs: (col, row, kind, arg). kind: 'robot' (arg = facing), 'letter' (arg = A-D) or an icon name."""
    s = ["<rect x='4' y='4' width='%d' height='%d' fill='#ffffff'/>" % (cols * C, rows * C)]
    for i in range(cols + 1):
        s.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1.3'/>" % (4 + i * C, 4 + i * C, 4 + rows * C, GRID))
    for j in range(rows + 1):
        s.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.3'/>" % (4 + j * C, 4 + cols * C, 4 + j * C, GRID))
    taken = set()
    for c, r, kind, arg in objs:
        assert 0 <= c < cols and 0 <= r < rows, (c, r)
        assert (c, r) not in taken, ("two things in one square", c, r)
        taken.add((c, r))
        cx, cy = 4 + c * C + C / 2.0, 4 + r * C + C / 2.0
        if kind == "robot":
            s.append(robot(cx, cy, arg))
        elif kind == "letter":
            s.append(text(cx, cy + 6.5, arg, 18))
        else:
            s.append(icon(kind, cx, cy, 14))
    return svg_wrap(cols * C + 8, rows * C + 8, "".join(s), label)


def direction_page(M, b, a):
    """b is left / right / up / down of a, in the same row or column."""
    A, B = M.where[a], M.where[b]
    ac, ar = {c for c, r in A}, {r for c, r in A}
    bc, br = {c for c, r in B}, {r for c, r in B}
    if ar & br:
        if min(bc) > max(ac):
            return "right"
        if max(bc) < min(ac):
            return "left"
    if ac & bc:
        if min(br) > max(ar):
            return "down"
        if max(br) < min(ar):
            return "up"
    return None


# ------------------------------------------------------------ set 4: which path is shorter?
PC, PR, PS = 7, 5, 34


def path_cells(start, moves):
    cells = [start]
    x = start
    for d, n in moves:
        for _ in range(n):
            x = step(x, d)
            cells.append(x)
    return cells


def two_paths_svg(start, end, A, B, label):
    """Path A: solid red line. Path B: dashed blue line. Each has a letter tag in its middle square."""
    C = PS
    ca, cb = path_cells(start, A), path_cells(start, B)
    assert ca[-1] == end and cb[-1] == end, (ca[-1], cb[-1], end)
    for cs in (ca, cb):
        assert len(set(cs)) == len(cs)
        for x in cs:
            assert 0 <= x[0] < PC and 0 <= x[1] < PR, x
    assert not (set(ca[1:-1]) & set(cb[1:-1])), "paths share squares"
    cen = lambda c: (4 + c[0] * C + C / 2.0, 4 + c[1] * C + C / 2.0)
    s = ["<rect x='4' y='4' width='%d' height='%d' fill='#ffffff'/>" % (PC * C, PR * C)]
    for i in range(PC + 1):
        s.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>" % (4 + i * C, 4 + i * C, 4 + PR * C, GRID))
    for j in range(PR + 1):
        s.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>" % (4 + j * C, 4 + PC * C, 4 + j * C, GRID))
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='4' stroke-linejoin='round' stroke-linecap='round'/>" % (P([cen(c) for c in ca]), RED))
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='4' stroke-dasharray='7 5' stroke-linejoin='round'/>" % (P([cen(c) for c in cb]), DBLUE))
    for cs, L, col in ((ca, "A", RED), (cb, "B", DBLUE)):
        mid = cs[len(cs) // 2]
        x, y = cen(mid)
        s.append("<circle cx='%.1f' cy='%.1f' r='11' fill='#ffffff' stroke='%s' stroke-width='2.5'/>" % (x, y, col))
        s.append(text(x, y + 5.5, L, 15))
    x, y = cen(start)
    s.append(icon("house", x, y, 13))
    x, y = cen(end)
    s.append(icon("flag", x, y, 13))
    return svg_wrap(PC * C + 8, PR * C + 8, "".join(s), label)


def top_view(kind, cx, cy):
    s = []
    if kind == "table":
        for x, y, w, h in [(cx - 8, cy - 27, 16, 10), (cx - 8, cy + 17, 16, 10), (cx - 36, cy - 8, 10, 16), (cx + 26, cy - 8, 10, 16)]:
            s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='2' fill='%s' stroke='%s' stroke-width='1.6'/>" % (x, y, w, h, BLUE, "#3d6f99"))
        s.append("<rect x='%.1f' y='%.1f' width='48' height='30' rx='2' fill='%s' stroke='#6b4316' stroke-width='2'/>" % (cx - 24, cy - 15, WOOD))
    elif kind == "car":
        for x in (cx - 19, cx + 15):
            for y in (cy - 22, cy + 12):
                s.append("<rect x='%.1f' y='%.1f' width='4' height='10' rx='1' fill='%s'/>" % (x, y, INK))
        s.append("<rect x='%.1f' y='%.1f' width='30' height='60' rx='9' fill='%s' stroke='#a33' stroke-width='2'/>" % (cx - 15, cy - 30, RED))
        s.append("<polygon points='%s' fill='#dfeefa' stroke='#3d6f99' stroke-width='1.4'/>" % P([(cx - 11, cy - 12), (cx + 11, cy - 12), (cx + 9, cy - 4), (cx - 9, cy - 4)]))
        s.append("<rect x='%.1f' y='%.1f' width='18' height='16' rx='2' fill='#f2a0a0' stroke='#a33' stroke-width='1.2'/>" % (cx - 9, cy - 3))
        s.append("<polygon points='%s' fill='#dfeefa' stroke='#3d6f99' stroke-width='1.4'/>" % P([(cx - 9, cy + 14), (cx + 9, cy + 14), (cx + 10, cy + 20), (cx - 10, cy + 20)]))
    elif kind == "bed":
        s.append("<rect x='%.1f' y='%.1f' width='40' height='60' rx='3' fill='#ffffff' stroke='#3d6f99' stroke-width='2'/>" % (cx - 20, cy - 30))
        s.append("<rect x='%.1f' y='%.1f' width='28' height='12' rx='4' fill='#ffffff' stroke='#3d6f99' stroke-width='1.6'/>" % (cx - 14, cy - 26))
        s.append("<rect x='%.1f' y='%.1f' width='40' height='40' rx='3' fill='%s' stroke='#3d6f99' stroke-width='2'/>" % (cx - 20, cy - 10, BLUE))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#3d6f99' stroke-width='1.6'/>" % (cx - 20, cy - 3, cx + 20, cy - 3))
    elif kind == "cup":
        s.append("<rect x='%.1f' y='%.1f' width='16' height='8' rx='4' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (cx + 14, cy - 4, BROWN))
        s.append("<circle cx='%.1f' cy='%.1f' r='19' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (cx - 2, cy, BROWN))
        s.append("<circle cx='%.1f' cy='%.1f' r='14' fill='#8a5a2b'/>" % (cx - 2, cy))
    elif kind == "tree":
        for dx, dy in [(-12, -8), (10, -10), (-10, 10), (12, 9), (0, 0), (0, -15), (0, 15), (-16, 2), (16, 0)]:
            s.append("<circle cx='%.1f' cy='%.1f' r='12' fill='#7cc48a' stroke='%s' stroke-width='1.5'/>" % (cx + dx, cy + dy, GREEN))
        s.append("<circle cx='%.1f' cy='%.1f' r='16' fill='#7cc48a'/>" % (cx, cy))
    elif kind == "house":
        x0, y0, x1, y1 = cx - 32, cy - 22, cx + 32, cy + 22
        s.append("<rect x='%.1f' y='%.1f' width='64' height='44' fill='%s' stroke='#a33' stroke-width='2'/>" % (x0, y0, "#e8a0a0"))
        for a, b in [((x0, y0), (cx - 12, cy)), ((x0, y1), (cx - 12, cy)), ((x1, y0), (cx + 12, cy)), ((x1, y1), (cx + 12, cy)), ((cx - 12, cy), (cx + 12, cy))]:
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#a33' stroke-width='1.8'/>" % (a + b))
    else:
        raise KeyError(kind)
    return "".join(s)


def side_view(kind, cx, cy):
    s = []
    ln = lambda a, b, col, w: "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g' stroke-linecap='round'/>" % (a + b + (col, w))
    if kind == "table":
        s.append(ln((cx - 36, cy - 4), (cx - 36, cy + 26), "#3d6f99", 3))
        s.append(ln((cx - 36, cy + 6), (cx - 26, cy + 6), "#3d6f99", 3))
        s.append(ln((cx - 26, cy + 6), (cx - 26, cy + 26), "#3d6f99", 3))
        s.append(ln((cx + 36, cy - 4), (cx + 36, cy + 26), "#3d6f99", 3))
        s.append(ln((cx + 36, cy + 6), (cx + 26, cy + 6), "#3d6f99", 3))
        s.append(ln((cx + 26, cy + 6), (cx + 26, cy + 26), "#3d6f99", 3))
        s.append("<rect x='%.1f' y='%.1f' width='44' height='6' fill='%s' stroke='#6b4316' stroke-width='1.6'/>" % (cx - 22, cy - 8, WOOD))
        s.append(ln((cx - 18, cy - 2), (cx - 18, cy + 26), "#6b4316", 3.2))
        s.append(ln((cx + 18, cy - 2), (cx + 18, cy + 26), "#6b4316", 3.2))
    elif kind == "car":
        s.append("<path d='M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1f Z' fill='%s' stroke='#a33' stroke-width='2' stroke-linejoin='round'/>"
                 % (cx - 36, cy + 12, cx - 36, cy, cx - 20, cy - 2, cx - 10, cy - 16, cx + 16, cy - 16, cx + 36, cy + 2, RED))
        s.append("<polygon points='%s' fill='#dfeefa' stroke='#3d6f99' stroke-width='1.2'/>" % P([(cx - 7, cy - 13), (cx + 14, cy - 13), (cx + 26, cy - 1), (cx - 16, cy - 1)]))
        for x in (cx - 20, cx + 20):
            s.append("<circle cx='%.1f' cy='%.1f' r='8' fill='%s'/><circle cx='%.1f' cy='%.1f' r='3' fill='#cccccc'/>" % (x, cy + 13, INK, x, cy + 13))
    elif kind == "bed":
        s.append("<rect x='%.1f' y='%.1f' width='8' height='34' fill='%s' stroke='#6b4316' stroke-width='1.6'/>" % (cx - 36, cy - 14, WOOD))
        s.append("<rect x='%.1f' y='%.1f' width='64' height='12' rx='2' fill='%s' stroke='#3d6f99' stroke-width='1.6'/>" % (cx - 28, cy + 2, BLUE))
        s.append("<rect x='%.1f' y='%.1f' width='18' height='8' rx='3' fill='#ffffff' stroke='#3d6f99' stroke-width='1.4'/>" % (cx - 26, cy - 6))
        s.append(ln((cx + 33, cy + 14), (cx + 33, cy + 22), "#6b4316", 3))
    elif kind == "cup":
        s.append("<path d='M%.1f,%.1f a10,10 0 1 1 0,18' fill='none' stroke='%s' stroke-width='3'/>" % (cx + 14, cy - 10, BROWN))
        s.append("<polygon points='%s' fill='#ffffff' stroke='%s' stroke-width='2' stroke-linejoin='round'/>" % (P([(cx - 20, cy - 18), (cx + 18, cy - 18), (cx + 14, cy + 20), (cx - 16, cy + 20)]), BROWN))
    elif kind == "tree":
        s.append("<rect x='%.1f' y='%.1f' width='9' height='26' fill='%s'/>" % (cx - 4.5, cy + 2, BROWN))
        s.append("<circle cx='%.1f' cy='%.1f' r='20' fill='#7cc48a' stroke='%s' stroke-width='2'/>" % (cx, cy - 10, GREEN))
    elif kind == "house":
        s.append("<rect x='%.1f' y='%.1f' width='48' height='30' fill='#f3e3c3' stroke='%s' stroke-width='2'/>" % (cx - 24, cy - 2, BROWN))
        s.append("<polygon points='%s' fill='#e8a0a0' stroke='#a33' stroke-width='2' stroke-linejoin='round'/>" % P([(cx - 32, cy - 2), (cx, cy - 28), (cx + 32, cy - 2)]))
        s.append("<rect x='%.1f' y='%.1f' width='11' height='17' fill='%s'/>" % (cx - 5.5, cy + 11, BROWN))
    else:
        raise KeyError(kind)
    return "".join(s)


def views_svg(panels, label, letters=True):
    """panels: list of (view, kind). One row of up to 4 pictures, labelled A-D."""
    s = []
    for i, (view, kind) in enumerate(panels):
        x0 = 4 + i * 96
        s.append("<rect x='%d' y='4' width='90' height='84' rx='6' fill='#ffffff' stroke='%s' stroke-width='1.2'/>" % (x0, GRID))
        s.append((top_view if view == "top" else side_view)(kind, x0 + 45, 46))
        if len(panels) > 1 and letters:
            s.append(text(x0 + 45, 108, "ABCD"[i], 16))
    H = 116 if len(panels) > 1 and letters else 92
    return svg_wrap(96 * len(panels) + 2, H, "".join(s), label)


NOUN = {"table": "table with 4 chairs", "car": "car", "bed": "bed", "cup": "cup of hot chocolate", "tree": "tree", "house": "house"}


def plan_svg(plans, label):
    """plans: list of dicts {cell: icon} on a 3 x 3 grid, drawn side by side as A, B, C, D."""
    C = 34
    s = []
    for i, pl in enumerate(plans):
        x0 = 4 + i * (3 * C + 14)
        s.append("<rect x='%d' y='4' width='%d' height='%d' fill='#ffffff' stroke='%s' stroke-width='1.6'/>" % (x0, 3 * C, 3 * C, INK))
        for k in range(1, 3):
            s.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x0 + k * C, x0 + k * C, 4 + 3 * C, GRID))
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x0, 4 + k * C, x0 + 3 * C, 4 + k * C, GRID))
        for (c, r), ic in pl.items():
            s.append(icon(ic, x0 + c * C + C / 2.0, 4 + r * C + C / 2.0, 13))
        s.append(text(x0 + 1.5 * C, 3 * C + 26, "ABCD"[i], 16))
    W = 4 + len(plans) * (3 * C + 14) - 10
    return svg_wrap(W, 3 * C + 34, "".join(s), label)


def rel_ok(pl, x, d, a):
    where = {v: k for k, v in pl.items()}
    X, A = where[x], where[a]
    return (X[0] - A[0], X[1] - A[1]) == DV[DIRS.index(d)]


SIDE_TXT = ["in front of %s", "on %s right", "behind %s", "on %s left"]


def side_for(face, d):
    """A person faces page direction `face` (0-3). Something is in page direction d. Where is it for them? 0 front, 1 right, 2 behind, 3 left."""
    return (d - face) % 4


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)

def balance(sets, rnd):
    """Spread the correct answers exactly 5/5/5/5 over the positions. Choices with a fixed order stay as they are."""
    for s in sets:
        cnt = [0] * 4
        free = []
        for it in s["items"]:
            if it.pop("fixed", False):
                cnt[it["a"]] += 1
            else:
                free.append(it)
        need = [5 - c for c in cnt]
        assert min(need) >= 0 and sum(need) == len(free), (s["title"], cnt)
        targets = [i for i in range(4) for _ in range(need[i])]
        rnd.shuffle(targets)
        for it, t in zip(free, targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t
        final = [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


def mark_large(u, pattern):
    """Tag pictures that must print larger (maps, grids, rows of A-D pictures) so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ the maps
PC, PR, PS = 7, 5, 34

CLASS = Map(5, 4, [
    ("books", 0, 0, 1, 1, "b"), ("whiteboard", 1, 0, 2, 1, "o"), ("window", 3, 0, 1, 1, "w"), ("sink", 4, 0, 1, 1, "w"),
    ("fish tank", 0, 1, 1, 1, "w"), ("teacher’s desk", 2, 1, 1, 1, "b"), ("cubbies", 4, 1, 1, 1, "b"),
    ("carpet", 0, 2, 2, 1, "g"), ("bins", 4, 2, 1, 1, "o"),
    ("door", 0, 3, 1, 1, "r"), ("coat hooks", 1, 3, 1, 1, "o"), ("computers", 2, 3, 1, 1, "o"), ("plants", 4, 3, 1, 1, "g"),
], cw=88, ch=46)
CLASS_LABEL = "map of a classroom with books, a whiteboard, a window, a sink, a fish tank, the teacher’s desk, cubbies, a carpet, bins, the door, coat hooks, computers and plants"

PLAY = Map(6, 5, [
    ("school", 0, 0, 2, 1, "b"), ("gym", 3, 0, 1, 1, "b"), ("portable", 5, 0, 1, 1, "b"),
    ("water fountain", 1, 1, 1, 1, "w"), ("maple tree", 4, 1, 1, 1, "g"),
    ("sandbox", 0, 2, 1, 1, "o"), ("play structure", 2, 2, 2, 1, "o"), ("swings", 5, 2, 1, 1, "o"),
    ("bench", 1, 3, 1, 1, "o"), ("garden", 4, 3, 1, 1, "g"),
    ("gate", 0, 4, 1, 1, "r"), ("hopscotch", 2, 4, 1, 1, "o"), ("bike racks", 5, 4, 1, 1, "o"),
], cw=88, ch=46)
PLAY_LABEL = "map of a schoolyard with the school, the gym, a portable, a water fountain, a maple tree, a sandbox, a play structure, swings, a bench, a garden, the gate, hopscotch and bike racks"

PARK = Map(6, 5, [
    ("washrooms", 0, 0, 1, 1, "b"), ("parking lot", 2, 0, 2, 1, "o"), ("snack bar", 5, 0, 1, 1, "b"),
    ("maple tree", 1, 1, 1, 1, "g"), ("slide", 4, 1, 1, 1, "o"),
    ("BBQ", 0, 2, 1, 1, "r"), ("pond", 2, 2, 1, 1, "w"), ("swings", 5, 2, 1, 1, "o"),
    ("picnic table", 1, 3, 1, 1, "o"), ("sandbox", 3, 3, 1, 1, "o"),
    ("garbage cans", 0, 4, 1, 1, "o"), ("gate", 2, 4, 1, 1, "r"), ("splash pad", 4, 4, 1, 1, "w"),
], cw=88, ch=46)
PARK_LABEL = "map of a park with washrooms, a parking lot, a snack bar, a maple tree, a slide, a BBQ, a pond, swings, a picnic table, a sandbox, garbage cans, the gate and a splash pad"

TOWN = Map(6, 4, [
    ("arena", 0, 0, 2, 1, "b"), ("library", 3, 0, 1, 1, "b"), ("fire hall", 5, 0, 1, 1, "r"),
    ("park", 1, 1, 1, 1, "g"), ("school", 4, 1, 2, 1, "b"),
    ("store", 0, 2, 1, 1, "o"), ("pool", 2, 2, 1, 1, "w"), ("mailbox", 4, 2, 1, 1, "r"),
    ("home", 1, 3, 1, 1, "b"), ("bakery", 3, 3, 1, 1, "o"), ("bus stop", 5, 3, 1, 1, "o"),
], cw=88, ch=46)
TOWN_LABEL = "map of a neighbourhood with an arena, a library, a fire hall, a park, a school, a store, a pool, a mailbox, a home, a bakery and a bus stop"

DWORD = {"up": "up", "down": "down", "left": "left", "right": "right"}
GOWORD = {"up": "up", "down": "down", "left": "to the left", "right": "to the right"}


def isare(n):
    return "are" if n.endswith("s") else "is"


def first_in(M, name, d):
    """The first place you reach going straight from `name` in page direction d (empty squares skipped)."""
    x = step(M.single(name), d)
    while M.inside(x):
        if M.at(x) and M.at(x) != name:
            return M.at(x)
        x = step(x, d)
    return None


def between_loose(M, a, b):
    """Places in the squares between a and b, in one straight row or column (empty squares allowed)."""
    A, B = M.single(a), M.single(b)
    assert A[0] == B[0] or A[1] == B[1], (a, b)
    dx = (B[0] > A[0]) - (B[0] < A[0])
    dy = (B[1] > A[1]) - (B[1] < A[1])
    out = set()
    x = (A[0] + dx, A[1] + dy)
    while x != B:
        if M.at(x):
            out.add(M.at(x))
        x = (x[0] + dx, x[1] + dy)
    return out


def land_on(M, frm, moves, extra):
    """Start at `frm`, follow page moves. Returns (answer, wrong places from real mistakes first)."""
    s0 = M.single(frm)
    end = walk(s0, moves)
    ans = M.at(end)
    assert ans and ans != frm, (frm, moves, end)
    cands, why = [], {}
    for kind, mm in mistake_moves(moves):
        c = walk(s0, mm)
        if M.inside(c) and M.at(c) and M.at(c) not in (ans, frm) and M.at(c) not in cands:
            cands.append(M.at(c))
            why[M.at(c)] = kind
    for x in extra:
        assert x != ans and x in M.where, x
    cands += [x for x in extra if x not in cands]
    return ans, cands, why


def route(M, a, b):
    A, B = M.single(a), M.single(b)
    dx, dy = B[0] - A[0], B[1] - A[1]
    assert dx and dy, (a, b)
    mv = [("right" if dx > 0 else "left", abs(dx)), ("up" if dy < 0 else "down", abs(dy))]
    assert walk(A, mv) == B
    wrong = [[(OPP[mv[0][0]], mv[0][1]), mv[1]], [mv[0], (OPP[mv[1][0]], mv[1][1])], [(mv[0][0], mv[0][1] + 1), (mv[1][0], mv[1][1] + 1)]]
    if mv[0][1] != mv[1][1]:
        wrong.insert(2, [(mv[0][0], mv[1][1]), (mv[1][0], mv[0][1])])
    for w in wrong:
        assert walk(A, w) != B
    return mv, wrong


# ------------------------------------------------------------ set 1: position words on a classroom map
def set_position(rnd, P_):
    M = CLASS
    m = fig(M.svg(CLASS_LABEL))
    its = []

    def between_q(a, b, wrong):
        ans = between_all(M, a, b)
        assert len(ans) == 1, (a, b, ans)
        ans = ans.pop()
        for w in wrong:
            assert w != ans and w in M.where
        line = "row" if M.where[a][0][1] == M.where[b][0][1] else "column"
        its.append(mcq(m + "What is <b>between</b> the %s and the %s?" % (a, b), the(ans), [the(w) for w in wrong],
                       "Find the %s and the %s. They are in the same %s. The %s %s in the middle of them."
                       % (a, b, line, ans, isare(ans)), rnd))

    between_q("door", "computers", ["carpet", "plants", "fish tank"])
    between_q("books", "carpet", ["whiteboard", "door", "teacher’s desk"])
    between_q("sink", "bins", ["window", "plants", "teacher’s desk"])
    between_q("cubbies", "plants", ["sink", "computers", "door"])
    between_q("whiteboard", "sink", ["books", "cubbies", "teacher’s desk"])

    WORD = {"left": "just to the <b>left</b> of", "right": "just to the <b>right</b> of", "up": "just <b>above</b>", "down": "just <b>below</b>"}

    def side_q(name, d, extra):
        ans = beside(M, name, d)
        assert len(ans) == 1, (name, d, ans)
        ans = ans.pop()
        opp = beside(M, name, OPP[d])
        wrong = sorted(opp) + extra
        for w in wrong:
            assert w != ans and w in M.where, w
        e = "Start at the %s. Look one square %s. That square has the %s." % (name, GOWORD[d], ans)
        if opp:
            o = sorted(opp)[0]
            if d in ("left", "right"):
                e += " The %s %s just to the %s. Do not mix up left and right." % (o, isare(o), OPP[d])
            else:
                e += " The %s %s just %s." % (o, isare(o), "below" if d == "up" else "above")
        its.append(mcq(m + "What is %s the %s?" % (WORD[d], name), the(ans), [the(w) for w in wrong], e, rnd))

    side_q("coat hooks", "left", ["carpet", "plants", "fish tank"])
    side_q("computers", "left", ["plants", "teacher’s desk", "door"])
    side_q("sink", "left", ["cubbies", "whiteboard", "books"])
    side_q("books", "right", ["fish tank", "window", "sink"])
    side_q("door", "right", ["computers", "carpet", "plants"])
    side_q("cubbies", "up", ["window", "teacher’s desk", "plants"])
    side_q("door", "up", ["fish tank", "coat hooks", "books"])
    side_q("teacher’s desk", "up", ["computers", "window", "books"])
    side_q("fish tank", "down", ["door", "coat hooks", "teacher’s desk"])
    side_q("sink", "down", ["bins", "window", "plants"])

    nb = neighbours(M, "plants")
    assert nb == ["bins"], nb
    its.append(mcq(m + "Which is <b>next to</b> the plants?", "the bins", ["the computers", "the cubbies", "the door"],
                   "Next to means touching, side by side. The bins are just above the plants. The square to the left of the plants is empty.", rnd))
    assert M.at((0, 0)) == "books" and M.at((4, 3)) == "plants" and M.at((4, 0)) == "sink" and M.at((0, 3)) == "door"
    its.append(mcq(m + "What is in the <b>top left</b> corner of the map?", "the books", ["the sink", "the door", "the plants"],
                   "Top is the top row. Left is the left side of the page. The books are in the top left corner. The sink is in the top right.", rnd))
    its.append(mcq(m + "What is in the <b>bottom right</b> corner of the map?", "the plants", ["the door", "the sink", "the bins"],
                   "Bottom is the bottom row. Right is the right side of the page. The plants are in the bottom right corner.", rnd))
    its.append(mcq(m + "Which of these is <b>not</b> on the map?", "the piano", ["the fish tank", "the sink", "the computers"],
                   "Read every label on the map. There is a fish tank, a sink and computers, but no piano.", rnd))
    bottom = sorted({M.at((c, 3)) for c in range(5)} - {None})
    assert len(bottom) == 4
    its.append(mcq_num(m + "How many things are in the <b>bottom row</b> of the map?", 4, [5, 3, 6],
                       "Look along the bottom row: the door, the coat hooks, the computers and the plants. That is 4 things. One square is empty."))
    assert len(its) == 20, len(its)
    return {"title": "Position words on a classroom map: left of, right of, between, above and below", "items": its}


# ------------------------------------------------------------ set 2: read a map of a park
def set_read(rnd, P_):
    its = []
    pos = Pos(rnd)
    for obj, others in [("table", [("side", "table"), ("top", "bed"), ("side", "cup")]),
                        ("car", [("side", "car"), ("top", "bed"), ("side", "house")]),
                        ("tree", [("side", "tree"), ("top", "cup"), ("side", "house")])]:
        p = pos.next()
        panels = others[:]
        panels.insert(p, ("top", obj))
        lab = "four pictures: " + ", ".join("%s %s view of a %s" % ("ABCD"[i], "top" if v == "top" else "side", k) for i, (v, k) in enumerate(panels))
        side_letter = "ABCD"[panels.index(("side", obj))]
        e = ("A map shows things from above, like a bird flying over them. Picture %s shows the %s from above. "
             "Picture %s shows it from the side." % ("ABCD"[p], NOUN[obj], side_letter))
        its.append(mcq_fixed(fig(views_svg(panels, lab)) + "Which picture shows the <b>%s</b> from above, like on a map?" % NOUN[obj],
                             ["A", "B", "C", "D"], "ABCD"[p], e))
    for obj, wrong, e in [
        ("bed", ["a car", "a table with 4 chairs", "a house"], "You can see a pillow at one end and a blanket. It is a bed seen from above."),
        ("cup", ["a tree", "a car", "a bed"], "A round shape with a handle on one side. It is a cup of hot chocolate seen from above."),
    ]:
        its.append(mcq(fig(views_svg([("top", obj)], "view from above of a " + obj)) + "This picture shows something from above. What is it?",
                       "a " + NOUN[obj], wrong, e, rnd))

    M = PARK
    pk = fig(M.svg(PARK_LABEL))
    assert M.at((5, 0)) == "snack bar" and M.at((0, 0)) == "washrooms" and M.at((0, 4)) == "garbage cans" and M.at((5, 4)) is None
    its.append(mcq(pk + "What is in the <b>top right</b> corner of the park map?", "the snack bar", ["the washrooms", "the splash pad", "the garbage cans"],
                   "Top is the top row. Right is the right side of the page. The snack bar is in the top right corner. The washrooms are in the top left.", rnd))
    its.append(mcq(pk + "What is in the <b>bottom left</b> corner of the park map?", "the garbage cans", ["the washrooms", "the gate", "the snack bar"],
                   "Bottom is the bottom row. Left is the left side of the page. The garbage cans are in the bottom left corner.", rnd))

    def first_q(frm, d, wrong, why):
        ans = first_in(M, frm, d)
        assert ans and ans not in wrong, (frm, d, ans)
        for w in wrong:
            assert w in M.where
        its.append(mcq(pk + "Start at the %s. Go straight <b>%s</b>. What is the first thing you reach?" % (frm, GOWORD[d]),
                       the(ans), [the(w) for w in wrong],
                       "Start at the %s and move %s, one square at a time. Skip the empty squares. The first place is the %s.%s"
                       % (frm, GOWORD[d], ans, why), rnd))

    first_q("BBQ", "right", ["swings", "maple tree", "picnic table"], " The swings are further along the same row.")
    first_q("gate", "up", ["parking lot", "sandbox", "picnic table"], " The parking lot is further up.")
    first_q("slide", "down", ["snack bar", "swings", "sandbox"], "")
    first_q("swings", "left", ["BBQ", "slide", "sandbox"], " The BBQ is at the far end of the row.")

    for a, b, wrong in [("BBQ", "swings", ["slide", "sandbox", "maple tree"]),
                        ("washrooms", "garbage cans", ["maple tree", "picnic table", "gate"])]:
        ans = between_loose(M, a, b)
        assert len(ans) == 1, ans
        ans = ans.pop()
        line = "row" if M.single(a)[1] == M.single(b)[1] else "column"
        its.append(mcq(pk + "What is <b>between</b> the %s and the %s?" % (a, b), the(ans), [the(w) for w in wrong],
                       "The %s and the %s are in the same %s. Look along the %s between them. The %s %s the only thing there."
                       % (a, b, line, line, ans, isare(ans)), rnd))

    d = {x: dist(M, "gate", x) for x in ("picnic table", "slide", "washrooms", "snack bar")}
    assert d["picnic table"] == 2 and min(v for k2, v in d.items() if k2 != "picnic table") > 2, d
    its.append(mcq(pk + "Which of these is <b>closest</b> to the gate?", "the picnic table", ["the slide", "the washrooms", "the snack bar"],
                   "Count the squares from the gate. The picnic table is only 2 squares away (1 left and 1 up). The others are further away.", rnd))

    a, b = M.single("BBQ"), M.single("swings")
    n = b[0] - a[0]
    assert a[1] == b[1] and n == 5
    its.append(mcq_num(pk + "How many squares is it from the BBQ, straight across to the swings?", n, num_cands(n, 1),
                       "Count each move to the right: 1, 2, 3, 4, 5. That is 5 squares. Do not count the BBQ square."))
    a, b = M.single("gate"), M.where["parking lot"]
    assert (2, 0) in b
    n = a[1] - 0
    assert n == 4
    its.append(mcq_num(pk + "How many squares is it from the gate, straight up to the parking lot?", n, num_cands(n, 2),
                       "Count each move up: 1, 2, 3, 4. That is 4 squares. If you count the gate square too, you get 5, which is too many."))

    for b_, a_ in [("swings", "pond"), ("splash pad", "slide")]:
        dd = direction_page(M, b_, a_)
        assert dd
        rel = {"right": "to the right of", "left": "to the left of", "down": "below", "up": "above"}[dd]
        line = "row" if dd in ("left", "right") else "column"
        its.append(mcq(pk + "You walk from the %s straight to the %s. Which way do you go on the map?" % (a_, b_),
                       dd, [x for x in ("up", "down", "left", "right") if x != dd],
                       "The %s %s %s the %s, in the same %s. So you go %s." % (b_, isare(b_), rel, a_, line, dd), rnd))

    top = sorted({M.at((c, 0)) for c in range(6)} - {None})
    assert len(top) == 3
    its.append(mcq_num(pk + "How many places are in the <b>top row</b> of the map?", 3, [4, 2, 5],
                       "The top row has the washrooms, the parking lot and the snack bar. The parking lot takes up 2 squares, but it is 1 place. That is 3 places."))
    its.append(mcq(pk + "Which of these is <b>not</b> on the park map?", "a skating rink", ["a splash pad", "a BBQ", "a pond"],
                   "Read every label. The map has a splash pad, a BBQ and a pond, but no skating rink.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Read a map of a park", "items": its}


# ------------------------------------------------------------ set 3: follow moves
def set_moves(rnd, P_):
    its = []
    M = PLAY
    pm = fig(M.svg(PLAY_LABEL))
    pos = Pos(rnd)

    def land_q(frm, moves, extra):
        ans, cands, why = land_on(M, frm, moves, extra)
        e = "Start at the %s. Go %s. You reach the %s. Do not count the square you start on." % (frm, moves_txt(moves), ans)
        if cands and why.get(cands[0]) == "lr":
            e += " Mixing up left and right takes you to the %s." % cands[0]
        elif cands and why.get(cands[0]) == "ud":
            dv = [d for d, k in moves if d in ("up", "down")][0]
            e += " Going %s instead of %s takes you to the %s." % (OPP[dv], dv, cands[0])
        elif cands and why.get(cands[0]) == "start":
            e += " Counting the start square stops you at the %s." % cands[0]
        its.append(mcq(pm + "Start at the %s. Go <b>%s</b>. What do you reach?" % (frm, moves_txt(moves)), the(ans),
                       [the(c) for c in cands], e, rnd))

    land_q("gate", [("up", 2)], ["bench", "school", "water fountain"])
    land_q("bench", [("right", 3)], ["play structure", "swings", "maple tree"])
    land_q("portable", [("down", 2)], ["maple tree", "bike racks", "gym"])
    land_q("swings", [("left", 4), ("up", 1)], ["sandbox", "school", "play structure"])
    land_q("hopscotch", [("up", 3), ("right", 2)], ["gym", "portable", "play structure"])
    land_q("bike racks", [("up", 1), ("left", 1)], ["swings", "hopscotch", "maple tree"])
    land_q("sandbox", [("down", 1), ("right", 1)], ["gate", "play structure", "water fountain"])
    land_q("gym", [("down", 3), ("left", 2)], ["hopscotch", "play structure", "sandbox"])
    land_q("garden", [("left", 4), ("down", 1)], ["bench", "sandbox", "hopscotch"])

    def letters_q(start, moves, extra=()):
        ans = walk(start, moves)
        assert 0 <= ans[0] < GC and 0 <= ans[1] < GR, (start, moves)
        cells, why = [], {}
        for kind, mm in mistake_moves(moves):
            c = walk(start, mm)
            if 0 <= c[0] < GC and 0 <= c[1] < GR and c not in (ans, start) and c not in cells:
                cells.append(c)
                why[c] = kind
        for c in extra:
            if c not in (ans, start) and c not in cells:
                cells.append(c)
        assert len(cells) >= 3, (start, moves, cells)
        cells = cells[:3]
        p = pos.next()
        order = cells[:]
        order.insert(p, ans)
        objs = [(start[0], start[1], "house", None)] + [(c[0], c[1], "letter", "ABCD"[i]) for i, c in enumerate(order)]
        svg = grid_svg(objs, label="grid with a house and squares A to D")
        e = "Start at the house. Go %s, one square at a time. Do not count the house square. You stop on %s." % (moves_txt(moves), "ABCD"[p])
        k0 = why.get(cells[0])
        if k0 == "start":
            e += " Counting the house square %s stops you on %s." % ("as 1" if len(moves) == 1 else "at each move", "ABCD"[order.index(cells[0])])
        elif k0 == "lr":
            e += " %s is what you get if you mix up left and right." % "ABCD"[order.index(cells[0])]
        its.append(mcq_fixed(fig(svg) + "Start at the house. Go <b>%s</b>. Where do you stop?" % moves_txt(moves),
                             ["A", "B", "C", "D"], "ABCD"[p], e))

    letters_q((0, 4), [("right", 3)])
    letters_q((5, 4), [("up", 3)])
    letters_q((1, 0), [("down", 2)])
    letters_q((5, 2), [("left", 4)], extra=[(1, 1), (1, 3)])
    letters_q((0, 4), [("right", 3), ("up", 2)])
    letters_q((5, 4), [("left", 2), ("up", 3)])
    letters_q((0, 0), [("right", 4), ("down", 2)])
    letters_q((4, 4), [("up", 2), ("left", 3)])

    a, b = M.single("sandbox"), M.single("swings")
    n = b[0] - a[0]
    assert a[1] == b[1] and n == 5
    its.append(mcq_num(pm + "How many squares is it from the sandbox, straight across to the swings?", n, num_cands(n, 2),
                       "Count each move to the right: 1, 2, 3, 4, 5. That is 5 squares. Do not count the sandbox square."))
    a2, b2 = M.single("bike racks"), M.single("portable")
    n = a2[1] - b2[1]
    assert a2[0] == b2[0] and n == 4
    its.append(mcq_num(pm + "How many squares is it from the bike racks, straight up to the portable?", n, num_cands(n, 1),
                       "Count each move up: 1, 2, 3, 4. That is 4 squares. If you count the bike racks square too, you get 5, which is too many."))
    a3, b3 = M.single("water fountain"), M.single("bench")
    n = b3[1] - a3[1]
    assert a3[0] == b3[0] and n == 2
    its.append(mcq_num(pm + "How many squares is it from the water fountain, straight down to the bench?", n, num_cands(n, 0),
                       "Count each move down: 1, 2. That is 2 squares. Do not count the water fountain square."))
    assert len(its) == 20, len(its)
    return {"title": "Follow moves: 3 squares right, 2 squares up", "items": its}


# ------------------------------------------------------------ set 4: describe a path
def set_paths(rnd, P_):
    its = []
    M = PLAY
    pm = fig(M.svg(PLAY_LABEL))
    for a, b in [("gate", "water fountain"), ("sandbox", "garden"), ("portable", "bench"), ("gym", "bike racks"), ("swings", "hopscotch")]:
        mv, wrong = route(M, a, b)
        its.append(mcq(pm + "Which moves take you from the %s to the %s?" % (a, b), moves_short(mv),
                       [moves_short(w) for w in wrong],
                       "From the %s, count the squares across, then the squares up or down: %s. Count the moves, not the square you start on." % (
                           a, moves_txt(mv)), rnd))

    G = Map(6, 4, [], cw=40, ch=40)
    for start, moves, endicon in [((0, 3), [("up", 2), ("right", 3)], "flag"), ((5, 3), [("left", 4), ("up", 1)], "star"),
                                  ((1, 0), [("right", 3), ("down", 2)], "house"), ((4, 0), [("down", 3), ("left", 2)], "tree")]:
        cells = path_cells(start, moves)
        end = cells[-1]
        assert G.inside(end)
        svg = G.svg("grid with a red dot, a %s and a dashed path between them" % endicon,
                    marks=[(start, "dot", None), (end, "icon", endicon)], path=cells)
        wrong = [[(moves[0][0], moves[0][1] + 1), (moves[1][0], moves[1][1] + 1)],
                 [(moves[0][0], moves[1][1]), (moves[1][0], moves[0][1])],
                 [(OPP[moves[0][0]], moves[0][1]), moves[1]] if moves[0][0] in ("left", "right") else [moves[0], (OPP[moves[1][0]], moves[1][1])]]
        assert len({moves_short(w) for w in wrong} | {moves_short(moves)}) == 4
        its.append(mcq(fig(svg) + "Follow the dashed path from the red dot to the %s. Which moves does it show?" % endicon,
                       moves_short(moves), [moves_short(w) for w in wrong],
                       "Count the squares along the path from the dot: %s. Do not count the dot’s own square." % moves_txt(moves), rnd))
        if endicon == "flag":
            n = sum(k for d, k in moves)
            its.append(mcq_num(fig(svg) + "How many squares long is the dashed path from the red dot to the flag?", n, num_cands(n, 3),
                               "Count each move along the path: 2 up + 3 right = 5 squares. Do not count the dot’s square."))

    PAIRS = [
        ((0, 4), (4, 1), [("up", 3), ("right", 4)], [("right", 5), ("up", 3), ("left", 1)]),
        ((0, 0), (5, 3), [("down", 4), ("right", 5), ("up", 1)], [("right", 5), ("down", 3)]),
        ((1, 4), (5, 0), [("up", 2), ("right", 2), ("up", 2), ("right", 2)], [("right", 4), ("up", 4)]),
    ]
    p_cycle = [0, 1, 2, 3]
    rnd.shuffle(p_cycle)
    k = 0
    for i, (st, en, A, B) in enumerate(PAIRS):
        la, lb = sum(n for d, n in A), sum(n for d, n in B)
        svg = fig(two_paths_svg(st, en, A, B, "grid with a house, a flag and two paths: A is a solid red line and B is a dashed blue line"))
        intro = "There are two paths from the house to the flag. "
        for L, ln, mv in (("A", la, A), ("B", lb, B)):
            p = p_cycle[k % 4]
            k += 1
            its.append(mcq_num(svg + intro + "How many squares long is path <b>%s</b>?" % L, ln, num_cands(ln, p),
                               "Count each move along path %s from the house: %s = %d squares. Do not count the house square."
                               % (L, " + ".join(str(n) for d, n in mv), ln)))
        if la == lb:
            ans = "They are the same length."
            wrong = ["Path A, by 1 square", "Path B, by 1 square", "Path A, by 2 squares"]
            e = "Path A is %s. Path B is %s. They are the same length, even though path A has more turns." % (sq(la), sq(lb))
        else:
            sh, lo = ("A", "B") if la < lb else ("B", "A")
            dif = abs(la - lb)
            ans = "Path %s, by %s" % (sh, sq(dif))
            wrong = ["Path %s, by %s" % (lo, sq(dif)), "Path %s, by %s" % (sh, sq(dif + 1)), "They are the same length."]
            e = "Path A is %s. Path B is %s. %d is less than %d, so path %s is shorter. %d − %d = %d." % (
                sq(la), sq(lb), min(la, lb), max(la, lb), sh, max(la, lb), min(la, lb), dif)
        its.append(mcq(svg + intro + "Which path is shorter, and by how much?", ans, wrong, e, rnd))
    st, en = (0, 4), (5, 1)
    n = abs(en[0] - st[0]) + abs(en[1] - st[1])
    svg = grid_svg([(st[0], st[1], "house", None), (en[0], en[1], "flag", None)], cols=PC, rows=PR, C=PS, label="grid with a house and a flag")
    its.append(mcq_num(fig(svg) + "What is the <b>shortest</b> path from the house to the flag? How many squares long is it?", n, num_cands(n, 2),
                       "Go straight across and straight up, with no going back: 5 across + 3 up = 8 squares."))
    assert len(its) == 20, len(its)
    return {"title": "Describe a path from one place to another", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_real(rnd, P_):
    its = []
    pos = Pos(rnd)
    for q, rels, good, wrongs, e in [
        ("Maya draws a map of her bedroom. The <b>desk is to the left of the bed</b>. The <b>door is below the desk</b>. Which map is right?",
         [("desk", "left", "bed"), ("door", "down", "desk")],
         {(0, 1): "desk", (1, 1): "bed", (0, 2): "door"},
         [{(2, 1): "desk", (1, 1): "bed", (2, 2): "door"}, {(0, 1): "desk", (1, 1): "bed", (0, 0): "door"},
          {(1, 0): "desk", (1, 1): "bed", (1, 2): "door"}],
         "Left is the left side of the page. Below means just under. The desk is just left of the bed and the door is just under the desk."),
        ("Lucas draws a map of his backyard. The <b>tree is above the bench</b>. The <b>ball is to the right of the bench</b>. Which map is right?",
         [("tree", "up", "bench"), ("ball", "right", "bench")],
         {(1, 0): "tree", (1, 1): "bench", (2, 1): "ball"},
         [{(1, 0): "tree", (1, 1): "bench", (0, 1): "ball"}, {(1, 2): "tree", (1, 1): "bench", (2, 1): "ball"},
          {(1, 2): "tree", (1, 1): "bench", (0, 1): "ball"}],
         "Above means just over it, toward the top of the page. Right is the right side of the page. The tree is over the bench and the ball is just right of it."),
    ]:
        ok = lambda pl: all(rel_ok(pl, *r) for r in rels)
        assert ok(good) and not any(ok(w) for w in wrongs), q
        p = pos.next()
        plans = wrongs[:]
        plans.insert(p, good)
        its.append(mcq_fixed(fig(plan_svg(plans, "four small maps A to D")) + q, ["A", "B", "C", "D"], "ABCD"[p],
                             e + " That is map %s." % "ABCD"[p]))

    M = PARK
    pk = fig(M.svg(PARK_LABEL))
    key = "The Grade 2 class goes on a field trip to the park. "
    n, he, his, him = P_.next()
    s0 = M.single("gate")
    assert M.at(walk(s0, [("up", 2)])) == "pond" and M.at(walk(s0, [("up", 4)])) == "parking lot"
    its.append(mcq(pk + key + "%s walks from the gate 2 squares up. What does %s reach?" % (n, he), "the pond",
                   ["the parking lot", "the sandbox", "the picnic table"],
                   "From the gate, count the moves up: 1 (an empty square), 2 (the pond). Do not count the gate square.", rnd))
    n, he, his, him = P_.next()
    s0 = M.single("BBQ")
    assert M.at(walk(s0, [("right", 3), ("down", 1)])) == "sandbox" and M.at(walk(s0, [("right", 2)])) == "pond"
    its.append(mcq(pk + key + "%s helps at the BBQ. Then %s walks 3 squares right and 1 square down. Where is %s?" % (n, he, he),
                   "at the sandbox", ["at the pond", "at the splash pad", "at the slide"],
                   "From the BBQ go right 3 squares, then down 1 square. That is the sandbox. Counting the BBQ square as 1 stops you at the pond.", rnd))
    n, he, his, him = P_.next()
    n2, he2, his2, him2 = P_.next()
    a, b = M.single("gate"), M.single("swings")
    assert walk(a, [("right", 3), ("up", 2)]) == b and walk(a, [("up", 2), ("right", 3)]) == b
    its.append(mcq(pk + key + "%s goes from the gate to the swings: 3 right, then 2 up. %s goes 2 up, then 3 right. Who walks farther?" % (n, n2),
                   "They walk the same.", [n, n2, "You cannot tell."],
                   "%s walks 3 + 2 = 5 squares. %s walks 2 + 3 = 5 squares. They walk the same: 5 squares each." % (n, n2), rnd))
    n, he, his, him = P_.next()
    assert M.at(walk(M.single("BBQ"), [("right", 3)])) is None
    its.append(mcq(pk + key + "%s walks 3 squares right from the BBQ, then 3 squares left. Where is %s now?" % (n, he),
                   "back at the BBQ", ["at the swings", "at the sandbox", "at the maple tree"],
                   "3 right, then 3 left takes %s back to where %s started: the BBQ." % (him, he), rnd))
    n, he, his, him = P_.next()
    a, b = M.single("slide"), M.single("swings")
    assert walk(a, [("right", 1), ("down", 1)]) == b
    its.append(mcq(pk + key + "%s is at the slide. Next %s wants a turn on the swings. Which moves take %s there?" % (n, he, him),
                   "1 right, 1 down", ["1 left, 1 down", "1 right, 1 up", "2 right, 2 down"],
                   "The swings are 1 square right of the slide and 1 square down. Mixing up left and right, or up and down, sends %s the wrong way." % him, rnd))
    n, he, his, him = P_.next()
    s0 = M.single("washrooms")
    assert M.at(walk(s0, [("down", 2), ("right", 2)])) == "pond" and M.at(walk(s0, [("down", 1), ("right", 1)])) == "maple tree"
    its.append(mcq(pk + key + "%s leaves the washrooms. %s goes 2 squares down, then 2 squares right. What does %s reach?" % (n, he.capitalize(), he),
                   "the pond", ["the maple tree", "the BBQ", "the picnic table"],
                   "From the washrooms go down 2 squares to the BBQ, then right 2 squares to the pond. Counting the start square each time stops you at the maple tree.", rnd))
    n, he, his, him = P_.next()
    assert dist(M, "gate", "splash pad") == 2 and M.at((3, 4)) is None
    its.append(mcq_num(pk + key + "Each square on the map is 10 big steps. %s walks from the gate straight to the splash pad. How many big steps is that?" % n,
                       20, [30, 10, 40],
                       "The splash pad is 2 squares right of the gate. 2 squares is 10 + 10 = 20 big steps. Counting the gate square too gives 30, which is too many."))
    n, he, his, him = P_.next()
    mv, wrong = route(M, "picnic table", "slide")
    assert mv == [("right", 3), ("up", 2)]
    its.append(mcq(pk + key + "%s eats lunch at the picnic table. Then %s goes to the slide. Which moves take %s there?" % (n, he, him),
                   moves_short(mv), [moves_short(w) for w in wrong],
                   "From the picnic table, count 3 squares right, then 2 squares up. That is the slide.", rnd))

    T = TOWN
    tm = fig(T.svg(TOWN_LABEL))
    tk = "This is a map of Owen’s neighbourhood. Each square is 1 block. "

    def town_land(who, frm, moves, extra, verb="walks"):
        ans, cands, why = land_on(T, frm, moves, extra)
        place = "home" if frm == "home" else "the " + frm
        e = "Start at %s. Go %s. You reach the %s." % (place, moves_txt(moves), ans)
        if cands and why.get(cands[0]) == "lr":
            e += " Mixing up left and right takes you to the %s." % cands[0]
        elif cands and why.get(cands[0]) == "start":
            e += " Counting the start square stops you at the %s." % cands[0]
        else:
            e += " Do not count the square you start on."
        its.append(mcq(tm + tk + "%s %s from %s %s. Where is %s now?" % (who[0], verb, "his home" if frm == "home" else "the " + frm, moves_txt(moves).replace("squares", "blocks").replace("square", "block"), who[1]),
                       "at the " + ans, ["at the " + c for c in cands], e.replace("squares", "blocks").replace("square", "block"), rnd))

    assert T.at((1, 2)) is None
    town_land(("Owen", "he"), "home", [("up", 2)], ["arena", "store", "pool"])
    town_land(("Owen", "he"), "home", [("right", 3), ("up", 2)], ["library", "mailbox", "pool"], verb="rides his bike")
    n, he, his, him = P_.next()
    town_land((n, he), "library", [("down", 3)], ["pool", "mailbox", "home"])
    n, he, his, him = P_.next()
    town_land((n, he), "bus stop", [("up", 1), ("left", 1)], ["school", "bakery", "fire hall"])
    n, he, his, him = P_.next()
    town_land((n, he), "fire hall", [("down", 3)], ["school", "mailbox", "library"])
    n, he, his, him = P_.next()
    town_land((n, he), "bakery", [("left", 2), ("up", 2)], ["store", "arena", "pool"])

    mv, wrong = route(T, "home", "library")
    its.append(mcq(tm + tk + "Owen wants to go from his home to the library. Which moves take him there?", moves_short(mv),
                   [moves_short(w) for w in wrong],
                   "From home, count %s right, then %s up. That is the library." % (sq(mv[0][1]).replace("square", "block"), sq(mv[1][1]).replace("square", "block")), rnd))
    a, b = T.single("store"), T.single("mailbox")
    n_ = b[0] - a[0]
    assert a[1] == b[1] and n_ == 4
    its.append(mcq_num(tm + tk + "How many blocks is it from the store, straight across to the mailbox?", n_, num_cands(n_, 1),
                       "Count each move to the right: 1, 2, 3, 4. That is 4 blocks. Do not count the store square."))
    ans = between_loose(T, "store", "mailbox")
    assert ans == {"pool"}
    its.append(mcq(tm + tk + "Owen walks from the store straight to the mailbox. What does he pass on the way?", "the pool",
                   ["the park", "the bakery", "the arena"],
                   "The store and the mailbox are in the same row. The pool is the only place between them.", rnd))
    n, he, his, him = P_.next()
    p_, po, bk = T.single("park"), T.single("pool"), T.single("bakery")
    l1 = abs(po[0] - p_[0]) + abs(po[1] - p_[1])
    l2 = abs(bk[0] - po[0]) + abs(bk[1] - po[1])
    assert l1 == 2 and l2 == 2
    its.append(mcq_num(tm + tk + "%s walks from the park to the pool. Then %s walks from the pool to the bakery. How many blocks does %s walk in all?" % (n, he, he),
                       4, [2, 3, 6],
                       "Park to pool: 1 right + 1 down = 2 blocks. Pool to bakery: 1 right + 1 down = 2 blocks. 2 + 2 = 4 blocks."))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: field trips and neighbourhood maps", "items": its}


# ------------------------------------------------------------ lesson
def body_html():
    views = views_svg([("side", "table"), ("top", "table")], "a table with 4 chairs from the side and from above", letters=False)
    cls = CLASS.svg(CLASS_LABEL)
    rt = Map(6, 4, [], cw=40, ch=40).svg("grid map with a dashed path from a red dot 2 squares up and 3 squares right to a flag",
                                          marks=[((0, 3), "dot", None), ((3, 1), "icon", "flag")], path=path_cells((0, 3), [("up", 2), ("right", 3)]))
    two = two_paths_svg((0, 4), (4, 1), [("up", 3), ("right", 4)], [("right", 5), ("up", 3), ("left", 1)],
                        "grid with a house, a flag and two paths: A is a solid red line and B is a dashed blue line")
    assert beside(CLASS, "fish tank", "down") == {"carpet"}
    return (
        "<h2>What a map is</h2>"
        "<p>A <b>map</b> shows a place from above, like a bird flying over it. "
        "Each shape on the map stands for a real thing.</p>"
        "<figure class='sn-fig'>" + views +
        "<figcaption>Left: a table with 4 chairs from the side. Right: the same table from above. Maps show things from above.</figcaption></figure>"
        "<h2>Where is it?</h2>"
        "<p>Use <b>position words</b>: next to, between, left of, right of, above, below. "
        "On a map, <b>left</b> and <b>right</b> are the left and right of the page. "
        "<b>Above</b> means toward the top of the page and <b>below</b> means toward the bottom.</p>"
        "<figure class='sn-fig'>" + cls +
        "<figcaption>The coat hooks are between the door and the computers. The sink is just above the cubbies. The whiteboard is to the right of the books.</figcaption></figure>" +
        ex("Example", "What is just below the fish tank?",
           "Find the fish tank. Look one square down.", "the carpet") +
        "<h2>Follow moves</h2>"
        "<p>Count the squares you <b>move</b>. Do not count the square you start on. Do one move at a time.</p>"
        "<figure class='sn-fig'>" + rt +
        "<figcaption>Start at the red dot. Go 2 squares up, then 3 squares right. You reach the flag.</figcaption></figure>" +
        ex("Example", "How do you describe the path to the flag?",
           "Count the squares up: 1, 2. Then count the squares right: 1, 2, 3.", "2 up, then 3 right") +
        "<h2>Which path is shorter?</h2>"
        "<p>Count the squares along each path. The path with fewer squares is shorter. A path with more turns is not always longer.</p>"
        "<figure class='sn-fig'>" + two +
        "<figcaption>Path A: 3 + 4 = 7 squares. Path B: 5 + 3 + 1 = 9 squares. Path A is shorter by 2 squares.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting the start square", "Count the moves, not the square you stand on"],
            ["Mixing up left and right", "Hold up your hands: the left hand makes an L"],
            ["Going down instead of up", "Up is toward the top of the page"],
            ["Swapping the moves (2 right, 3 up instead of 3 right, 2 up)", "Do the moves in order, one at a time"],
            ["Choosing the path that looks shorter", "Count the squares on each path, then compare"],
        ])
    )


FAQ = [
    {"q": "What do Grade 2 students learn about maps in the Ontario math curriculum?",
     "a": "In the Spatial Sense strand, Grade 2 students create and read simple maps of familiar places (E1.4). They describe where objects are and the moves needed to get from one object to another (E1.5)."},
    {"q": "How can I help my child tell left from right?",
     "a": "Hold up both hands with the fingers up and thumbs out: the left hand makes an L. Practise with games like “turn left at the mailbox” on a walk."},
    {"q": "Why does my child get the wrong answer when following moves on a grid?",
     "a": "The most common mistake is counting the starting square as 1. Show that a move goes to the next square, so “3 right” means three jumps, not three squares including the start."},
    {"q": "How can we practise maps at home?",
     "a": "Draw a simple map of the bedroom or backyard from above. Hide a toy and give moves like “3 steps forward, then 2 steps to the left”, then let your child give the directions."},
]


def gen():
    rnd = random.Random(42813)
    P_ = People(rnd)
    sets = [set_position(rnd, P_), set_read(rnd, P_), set_moves(rnd, P_), set_paths(rnd, P_), set_real(rnd, P_)]
    for s in sets:
        rnd.shuffle(s["items"])
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1, it["q"][:80]
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-2", "slug": "maps-and-directions", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Maps and Directions: Position Words, Map Reading and Paths",
        "seo_title": "Grade 2 Maps and Directions Math Worksheets: Free, with Answer Key (Ontario)",
        "short_title": "Maps and directions",
        "domain": "Spatial Sense",
        "standard_code": "Grade 2: E1.5",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Describe the relative positions of several objects and the movements needed to get from one object to another",
        "meta_desc": "Free Grade 2 math worksheets on maps and directions for the Ontario curriculum: position words like left of, between and above, "
                     "reading a simple park map, following moves such as 3 squares right and 2 up, describing paths, and word problems. 100 questions with an answer key.",
        "key_big": "Count the squares you move, not the square you start on.",
        "key_sub": "On a map, left and right are the left and right of the page, and up means toward the top. Do one move at a time: 3 right, then 2 up.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "(map|grid|four pictures|four small maps)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
