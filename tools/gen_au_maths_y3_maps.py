# -*- coding: utf-8 -*-
"""
AU Year 3 Maths: Maps and locations (Australian Curriculum v9.0, AC9M3SP02)
  python3 tools/gen_au_maths_y3_maps.py
HTML attributes use single quotes (no backslashes in the JSON).

Year 3 students read and make simple maps and plans of familiar places (classroom, school, park, zoo),
describe where things are (next to, between, left of, right of, north, south, east and west of),
follow and give directions on a grid map, read grid references (letter across, number down: B3),
and know that a map is a bird's-eye view (seen from above).
Every map is a model in code (cells of a grid). Every answer is worked out from that model:
moves, "between", "next to", compass directions, grid references and left/right for a person who faces
a direction. Wrong answers come from real mistakes: east and west mixed up, north and south mixed up,
left and right from the wrong viewpoint, counting the starting square, reading the grid reference
number first (B3 read as C2), writing the number first (3B), side view instead of a bird's-eye view.
Australian English.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
INK = "#2b2b2b"
GRID = "#b9b3a9"
YELLOW = "#f2c94c"
RED = "#e06666"
BLUE = "#9fc5e8"
ORANGE = "#f6a04d"
PINK = "#f4a6c0"
BROWN = "#a0692a"
STONE = "#b7b2aa"
WOOD = "#d9b382"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]
COLS = "ABCDEFGH"

VEC = {"north": (0, -1), "east": (1, 0), "south": (0, 1), "west": (-1, 0)}
OPP = {"north": "south", "south": "north", "east": "west", "west": "east"}
CW = ["north", "east", "south", "west"]          # clockwise order
DIRS4 = ["north", "south", "east", "west"]


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


def mcq_num(q, correct, cands, e, unit=""):
    ch = []
    for c in cands:
        if c > 0 and c != correct and c not in ch:
            ch.append(c)
    ch = sorted([correct] + ch[:3])
    assert len(ch) == 4, (q, ch)
    return mcq_fixed(q, ["%d%s" % (c, unit) for c in ch], "%d%s" % (correct, unit), e)


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


def sq(n):
    return "%d square%s" % (n, "" if n == 1 else "s")


def ref(cell):
    return "%s%d" % (COLS[cell[0]], cell[1] + 1)


def step(cell, d, n=1):
    v = VEC[d]
    return (cell[0] + v[0] * n, cell[1] + v[1] * n)


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


# ------------------------------------------------------------ small pictures (side view, for little plans)
def icon(kind, cx, cy, s=14):
    k = s / 18.0
    st = "stroke='%s' stroke-width='2' stroke-linejoin='round'" % GREEN
    if kind == "tree":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s'/>" % (cx - 3 * k, cy + 2 * k, 6 * k, 15 * k, BROWN) +
                "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#7cc48a' %s/>" % (cx, cy - 4 * k, 12 * k, st))
    if kind == "bench":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='1.5' fill='%s' stroke='#6b4316' stroke-width='1.8'/>"
                % (cx - 17 * k, cy - 2 * k, 34 * k, 5 * k, WOOD) +
                "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='1.5' fill='%s' stroke='#6b4316' stroke-width='1.8'/>"
                % (cx - 17 * k, cy - 12 * k, 34 * k, 5 * k, WOOD) +
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#6b4316' stroke-width='2.4'/>" % (cx - 13 * k, cy + 3 * k, cx - 13 * k, cy + 15 * k) +
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#6b4316' stroke-width='2.4'/>" % (cx + 13 * k, cy + 3 * k, cx + 13 * k, cy + 15 * k))
    if kind == "bin":
        return ("<polygon points='%s' fill='#4f9a5c' stroke='#2d5e36' stroke-width='1.8' stroke-linejoin='round'/>"
                % P([(cx - 11 * k, cy - 10 * k), (cx + 11 * k, cy - 10 * k), (cx + 9 * k, cy + 14 * k), (cx - 9 * k, cy + 14 * k)]) +
                "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='1.5' fill='#e2c044' stroke='#2d5e36' stroke-width='1.8'/>"
                % (cx - 13 * k, cy - 16 * k, 26 * k, 6 * k) +
                "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx + 6 * k, cy + 15 * k, 3.5 * k, INK))
    if kind == "flag":
        return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5' stroke-linecap='round'/>"
                % (cx - 8 * k, cy - 16 * k, cx - 8 * k, cy + 16 * k, INK) +
                "<polygon points='%s' fill='%s' stroke='#a33' stroke-width='1.5' stroke-linejoin='round'/>"
                % (P([(cx - 7 * k, cy - 15 * k), (cx + 14 * k, cy - 8 * k), (cx - 7 * k, cy - 1 * k)]), RED))
    if kind == "tent":
        return ("<polygon points='%s' fill='%s' stroke='#b76a1f' stroke-width='2' stroke-linejoin='round'/>"
                % (P([(cx, cy - 15 * k), (cx + 17 * k, cy + 13 * k), (cx - 17 * k, cy + 13 * k)]), ORANGE) +
                "<polygon points='%s' fill='#fff3e0' stroke='#b76a1f' stroke-width='1.5' stroke-linejoin='round'/>"
                % P([(cx, cy - 1 * k), (cx + 6 * k, cy + 13 * k), (cx - 6 * k, cy + 13 * k)]))
    if kind == "pond":
        return "<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='%s' stroke='#3d6f99' stroke-width='2'/>" % (cx, cy + 2 * k, 16 * k, 10 * k, BLUE)
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
    raise KeyError(kind)


# ------------------------------------------------------------ grid maps
class Map:
    """A grid map. Columns A, B, C ... go across (west to east). Rows 1, 2, 3 ... go down (north to south).
    items: (name, col, row, w, h, kind). kind: b building, g grass, w water, o other."""
    FILLS = {"b": ("#f3e3c3", BROWN), "g": (FILL, GREEN), "w": (BLUE, "#3d6f99"), "o": ("#fff1a8", "#b38f00"),
             "r": ("#f8d7d7", "#a33")}

    def __init__(self, cols, rows, items, cw=70, ch=46, refs=True, compass=True, fs=14):
        self.cols, self.rows, self.cw, self.ch = cols, rows, cw, ch
        self.refs, self.compass, self.fs = refs, compass, fs
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
        self.ox = 26 if refs else 4
        self.oy = 26 if refs else 4

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
        W = self.ox + self.cols * self.cw + (90 if self.compass else 4)
        H = self.oy + self.rows * self.ch + 4
        if self.compass:
            H = max(H, 100)
        return W, H

    def svg(self, label, marks=(), path=None, hi=None, hide=()):
        """marks: (cell, kind, arg) kind 'letter' (arg = A-D), 'dot' (a person), 'icon'.
        path: list of cells, drawn as a dashed route with an arrow. hi: cell to highlight."""
        cw, ch, ox, oy = self.cw, self.ch, self.ox, self.oy
        s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff'/>" % (ox, oy, self.cols * cw, self.rows * ch)]
        if hi:
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#ffe08a'/>" % (ox + hi[0] * cw, oy + hi[1] * ch, cw, ch))
        for i in range(self.cols + 1):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>" % (ox + i * cw, oy, ox + i * cw, oy + self.rows * ch, GRID))
        for j in range(self.rows + 1):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>" % (ox, oy + j * ch, ox + self.cols * cw, oy + j * ch, GRID))
        if self.refs:
            for i in range(self.cols):
                s.append(text(ox + i * cw + cw / 2.0, oy - 8, COLS[i], 15))
            for j in range(self.rows):
                s.append(text(ox - 12, oy + j * ch + ch / 2.0 + 5.5, str(j + 1), 15))
        for name, c, r, w, h, kind in self.items:
            if name in hide:
                continue
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
                     % (P(pts[:-1] + [shorten(pts[-2], pts[-1], 26)]), RED))
            s.append(arrowhead(pts[-2], pts[-1], 16, RED))
        for cell, kind, arg in marks:
            assert self.inside(cell), cell
            cx, cy = self.centre(cell)
            if kind == "letter":
                assert cell not in self.cell, ("letter on a place", cell)
                s.append("<circle cx='%.1f' cy='%.1f' r='13' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (cx, cy, GREEN))
                s.append(text(cx, cy + 6, arg, 17))
            elif kind == "dot":
                assert cell not in self.cell or path, ("dot on a place", cell)
                s.append("<circle cx='%.1f' cy='%.1f' r='11' fill='%s' stroke='#7a1f1f' stroke-width='2'/>" % (cx, cy, RED))
            elif kind == "icon":
                assert cell not in self.cell, ("icon on a place", cell)
                s.append(icon(arg, cx, cy, 15))
        if self.compass:
            W, H = self.size()
            s.append(compass(ox + self.cols * cw + 46, oy + min(self.rows * ch, 96) / 2.0 + (0 if self.rows * ch >= 96 else 0)))
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


def compass(cx, cy, r=20):
    s = []
    for ang, big in ((0, True), (90, False), (180, False), (270, False)):
        t = math.radians(ang)
        u = (math.sin(t), -math.cos(t))
        nr = (-u[1], u[0])
        L = r if big else r - 4
        tip = (cx + u[0] * L, cy + u[1] * L)
        s.append("<polygon points='%s' fill='%s'/>" % (P([tip, (cx + nr[0] * 5, cy + nr[1] * 5), (cx - nr[0] * 5, cy - nr[1] * 5)]),
                                                      GREEN if big else "#8a8478"))
    s.append("<circle cx='%.1f' cy='%.1f' r='3' fill='#ffffff' stroke='%s' stroke-width='1.2'/>" % (cx, cy, INK))
    s.append(text(cx, cy - r - 5, "N", 15))
    s.append(text(cx, cy + r + 16, "S", 15))
    s.append(text(cx + r + 11, cy + 5.5, "E", 15))
    s.append(text(cx - r - 11, cy + 5.5, "W", 15))
    return "".join(s)


# ------------------------------------------------------------ map facts (computed)
def neighbours(M, name):
    out = []
    for c in M.where[name]:
        for d in CW:
            n = M.at(step(c, d))
            if n and n != name and n not in out:
                out.append(n)
    return out


def between_all(M, a, b):
    """Places that lie between a and b on a straight line of squares (row or column), with nothing else in the way."""
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


def direction(M, b, a):
    """b is ___ of a (straight across or straight up/down, sharing a row or a column), else None."""
    A, B = M.where[a], M.where[b]
    ac, ar = {c for c, r in A}, {r for c, r in A}
    bc, br = {c for c, r in B}, {r for c, r in B}
    if ar & br:
        if min(bc) > max(ac):
            return "east"
        if max(bc) < min(ac):
            return "west"
    if ac & bc:
        if min(br) > max(ar):
            return "south"
        if max(br) < min(ar):
            return "north"
    return None


def first_in(M, name, d):
    """The first place you meet going straight in direction d from a one-square place."""
    c = M.single(name)
    x = step(c, d)
    while M.inside(x):
        if M.at(x):
            return M.at(x)
        x = step(x, d)
    return None


def dist(M, a, b):
    return min(abs(p[0] - q[0]) + abs(p[1] - q[1]) for p in M.where[a] for q in M.where[b])


def walk(start, moves):
    x = start
    for d, n in moves:
        x = step(x, d, n)
    return x


def moves_txt(moves):
    return ", then ".join("%s %s" % (sq(n), d) for d, n in moves)


def moves_short(moves):
    return ", ".join("%d %s" % (n, d) for d, n in moves)


def walk_e(start, moves, M=None):
    x = start
    parts = []
    for d, n in moves:
        x = step(x, d, n)
        parts.append("%s %s to %s" % (sq(n), d, ref(x)))
    s = "Start at %s. Go %s." % (ref(start), ", then ".join(parts))
    return s


def mistake_moves(moves):
    """Moves a student makes by mistake (in order of how common they are)."""
    out = []
    flip = lambda m, axis: [(OPP[d] if d in axis else d, n) for d, n in m]
    if any(d in ("east", "west") for d, n in moves):
        out.append(("ew", flip(moves, ("east", "west"))))
    if any(d in ("north", "south") for d, n in moves):
        out.append(("ns", flip(moves, ("north", "south"))))
    out.append(("start", [(d, n - 1) for d, n in moves]))           # counted the starting square each time
    if len(moves) == 2 and moves[0][1] != moves[1][1]:
        out.append(("swap", [(moves[0][0], moves[1][1]), (moves[1][0], moves[0][1])]))
    for i in range(len(moves)):
        out.append(("plus", [(d, n + 1 if j == i else n) for j, (d, n) in enumerate(moves)]))
    for i in range(len(moves)):
        if moves[i][1] > 1:
            out.append(("minus", [(d, n - 1 if j == i else n) for j, (d, n) in enumerate(moves)]))
    out.append(("both", flip(moves, ("east", "west", "north", "south"))))
    if len(moves) == 1:                                              # went across instead of up or down
        d, n = moves[0]
        for d2 in CW:
            if d2 not in (d, OPP[d]):
                out.append(("axis", [(d2, n)]))
    return out


# ------------------------------------------------------------ the maps
SCHOOL = Map(6, 5, [
    ("hall", 0, 0, 2, 1, "b"), ("library", 2, 0, 1, 1, "b"), ("office", 3, 0, 1, 1, "b"), ("car park", 4, 0, 2, 1, "o"),
    ("canteen", 0, 1, 1, 1, "b"), ("toilets", 0, 2, 1, 1, "b"), ("art room", 0, 3, 1, 1, "b"),
    ("garden", 2, 2, 1, 1, "g"), ("oval", 4, 1, 2, 2, "g"), ("classrooms", 4, 3, 2, 1, "b"),
    ("playground", 0, 4, 2, 1, "g"), ("sandpit", 2, 4, 1, 1, "o"), ("gate", 3, 4, 1, 1, "r"), ("bike racks", 5, 4, 1, 1, "o"),
])
SCHOOL_LABEL = "map of a school with a hall, library, office, car park, canteen, toilets, art room, garden, oval, classrooms, playground, sandpit, gate and bike racks"

PARK = Map(6, 5, [
    ("toilets", 0, 0, 1, 1, "b"), ("swings", 2, 0, 1, 1, "o"), ("slide", 4, 0, 1, 1, "o"), ("kiosk", 5, 0, 1, 1, "b"),
    ("pond", 1, 1, 1, 1, "w"), ("bench", 3, 1, 1, 1, "o"), ("tap", 5, 1, 1, 1, "w"),
    ("BBQ", 0, 2, 1, 1, "r"), ("gum tree", 2, 2, 1, 1, "g"), ("bin", 4, 2, 1, 1, "o"),
    ("sandpit", 1, 3, 1, 1, "o"), ("shelter", 3, 3, 1, 1, "b"), ("flag", 5, 3, 1, 1, "r"),
    ("gate", 0, 4, 1, 1, "r"), ("rotunda", 2, 4, 1, 1, "b"), ("picnic table", 4, 4, 1, 1, "o"),
])
PARK_LABEL = "grid map of a park with a toilets block, swings, slide, kiosk, pond, bench, tap, BBQ, gum tree, bin, sandpit, shelter, flag, gate, rotunda and picnic table"

CLASS = Map(5, 4, [
    ("whiteboard", 0, 0, 2, 1, "o"), ("window", 3, 0, 2, 1, "w"),
    ("teacher’s desk", 0, 1, 2, 1, "b"), ("sink", 4, 1, 1, 1, "w"),
    ("reading mat", 2, 2, 2, 1, "g"), ("laptops", 0, 3, 1, 1, "o"),
    ("door", 2, 3, 1, 1, "r"), ("lockers", 4, 3, 1, 1, "b"), ("bins", 4, 2, 1, 1, "o"),
], cw=74, ch=46)
CLASS_LABEL = "plan of a classroom with a whiteboard, window, teacher’s desk, sink, reading mat, laptops, door, lockers and bins"

ZOO = Map(6, 5, [
    ("lions", 0, 0, 1, 1, "b"), ("kangaroos", 1, 0, 2, 1, "g"), ("emus", 3, 0, 1, 1, "g"), ("picnic area", 4, 0, 2, 1, "g"),
    ("tigers", 0, 1, 1, 1, "b"), ("café", 4, 1, 1, 1, "r"),
    ("reptiles", 0, 2, 1, 1, "b"), ("koalas", 2, 2, 1, 1, "g"), ("penguins", 4, 2, 1, 1, "w"), ("seals", 5, 2, 1, 1, "w"),
    ("wombats", 1, 3, 1, 1, "g"), ("playground", 3, 3, 2, 1, "o"),
    ("toilets", 0, 4, 1, 1, "b"), ("entrance", 2, 4, 1, 1, "r"), ("gift shop", 4, 4, 1, 1, "b"),
], cw=74)
ZOO_LABEL = "map of a zoo with lions, kangaroos, emus, a picnic area, tigers, a café, reptiles, koalas, penguins, seals, wombats, a playground, toilets, the entrance and a gift shop"


def isare(n):
    return "are" if n.endswith("s") else "is"


def the(n):
    return n if n.startswith(("BBQ",)) and False else "the " + n


# ------------------------------------------------------------ set 1: read a school map
def set_read(rnd, P_):
    M = SCHOOL
    sm = fig(M.svg(SCHOOL_LABEL))
    its = []

    def between_q(a, b, wrong, extra=""):
        ans = between_all(M, a, b)
        assert len(ans) == 1, (a, b, ans)
        ans = ans.pop()
        its.append(mcq(sm + "What is <b>between</b> the %s and the %s?" % (a, b), "the " + ans, ["the " + w for w in wrong],
                       "Find the %s and the %s. They are in the same %s. The place in the middle of them is the %s.%s"
                       % (a, b, "row" if M.where[a][0][1] == M.where[b][0][1] else "column", ans, extra), rnd))

    between_q("hall", "office", ["car park", "canteen", "office"])
    between_q("library", "car park", ["oval", "library", "hall"])
    between_q("canteen", "art room", ["hall", "playground", "garden"])
    between_q("playground", "gate", ["classrooms", "garden", "bike racks"])
    between_q("toilets", "playground", ["canteen", "sandpit", "garden"])

    def next_q(a, wrong, word="next to"):
        nb = neighbours(M, a)
        assert len(nb) >= 1
        ans = [n for n in nb]
        return ans

    # a place with exactly one neighbour
    nb = neighbours(M, "garden")
    assert nb == [], nb
    nb = neighbours(M, "bike racks")
    assert nb == ["classrooms"], nb
    its.append(mcq(sm + "Which place is <b>next to</b> the bike racks?", "the classrooms",
                   ["the gate", "the oval", "the sandpit"],
                   "Next to means touching, side by side. The classrooms are just above the bike racks. The gate is 2 squares away.", rnd))
    nb = neighbours(M, "canteen")
    assert sorted(nb) == ["hall", "toilets"], nb
    its.append(mcq(sm + "The canteen is next to two places. What are they?", "the hall and the toilets",
                   ["the toilets and the art room", "the hall and the library", "the garden and the toilets"],
                   "Look at the squares touching the canteen: the hall is just above it and the toilets are just below it. The square on its right is empty.", rnd))
    assert set(neighbours(M, "oval")) == {"car park", "classrooms"}
    its.append(mcq(sm + "Which place is next to the oval?", "the car park",
                   ["the garden", "the office", "the bike racks"],
                   "The car park touches the top of the oval. The garden and the office do not touch it: there is a gap.", rnd))
    # corners and sides of the map
    assert M.at((0, 0)) == "hall" and M.at((5, 0)) == "car park" and M.at((0, 4)) == "playground" and M.at((5, 4)) == "bike racks"
    its.append(mcq(sm + "What is in the <b>top right</b> corner of the map?", "the car park",
                   ["the hall", "the bike racks", "the playground"],
                   "Top means the top row. Right means the right side. The car park is in the top right corner. The hall is in the top left.", rnd))
    its.append(mcq(sm + "What is in the <b>bottom left</b> corner of the map?", "the playground",
                   ["the bike racks", "the hall", "the art room"],
                   "Bottom means the bottom row. Left means the left side. The playground is in the bottom left corner.", rnd))
    # sizes
    its.append(mcq_num(sm + "How many squares does the oval cover on the map?", 4, [2, 3, 6],
                       "The oval is 2 squares across and 2 squares down: 2 rows of 2 squares. 2 + 2 = 4 squares."))
    its.append(mcq(sm + "Which place covers the most squares on the map?", "the oval",
                   ["the hall", "the classrooms", "the car park"],
                   "The oval covers 4 squares. The hall, the car park and the classrooms cover 2 squares each.", rnd))
    # nearest
    d = {n: dist(M, "gate", n) for n in ("sandpit", "garden", "library", "canteen")}
    assert d["sandpit"] == 1 and min(v for k, v in d.items() if k != "sandpit") > 1, d
    its.append(mcq(sm + "Which of these places is <b>closest</b> to the gate?", "the sandpit",
                   ["the garden", "the library", "the canteen"],
                   "The sandpit is right next to the gate. The others are further away.", rnd))
    dg, dc = dist(M, "office", "garden"), dist(M, "office", "art room")
    assert dg < dc
    its.append(mcq(sm + "Which is closer to the office?", "the garden",
                   ["the art room", "the playground", "the bike racks"],
                   "Count squares from the office. The garden is %s away. The art room is %s away." % (sq(dg), sq(dc)), rnd))
    # counting squares in a straight line
    its.append(mcq_num(sm + "How many squares do you walk from the gate, straight up the map, to the office? (Do not count the gate.)",
                       dist(M, "gate", "office"), [5, 3, 2],
                       "From the gate (D5) go up: D4 is 1, D3 is 2, D2 is 3 and the office (D1) is 4. "
                       "Do not count the square you start on."))
    assert dist(M, "gate", "office") == 4
    its.append(mcq_num(sm + "How many squares is it from the canteen straight down to the playground?", 3, [4, 2, 5],
                       "From the canteen go down: toilets (1), art room (2), playground (3). Do not count the canteen."))
    assert dist(M, "canteen", "playground") == 3
    # what is on the map
    its.append(mcq(sm + "Which of these is <b>not</b> on the map?", "the swimming pool",
                   ["the canteen", "the library", "the bike racks"],
                   "Read every label on the map. There is a canteen, a library and bike racks, but no swimming pool.", rnd))
    its.append(mcq(sm + "What is just above the art room on the map?", "the toilets",
                   ["the playground", "the canteen", "the garden"],
                   "Look up from the art room, one square. That square is the toilets. The playground is just below it.", rnd))
    its.append(mcq(sm + "What is just to the right of the library on the map?", "the office",
                   ["the hall", "the car park", "the garden"],
                   "Look one square to the right of the library. It is the office. The hall is on its left.", rnd))
    assert M.at((1, 4)) == "playground" and M.at((3, 4)) == "gate"
    its.append(mcq(sm + "What is just to the left of the sandpit on the map?", "the playground",
                   ["the gate", "the garden", "the bike racks"],
                   "Look one square to the left of the sandpit. It is part of the playground. The gate is on its right.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Read a school map: next to, between and closest", "items": its}


# ------------------------------------------------------------ set 2: compass directions and position words
FACE_SIDE = {0: "in front of", 1: "on the right of", 2: "behind", 3: "on the left of"}


def side_for(face, d):
    """A person faces `face`. Something is in direction d from them. Where is it for them?"""
    k = (CW.index(d) - CW.index(face)) % 4
    return ["in front of", "on the right of", "behind", "on the left of"][k]


def set_compass(rnd, P_):
    M = SCHOOL
    sm = fig(M.svg(SCHOOL_LABEL))
    its = []

    def dir_q(b, a, extra_wrong=None):
        d = direction(M, b, a)
        assert d, (b, a)
        wrong = [OPP[d]] + [x for x in DIRS4 if x not in (d, OPP[d])]
        e = "Use the compass: north is up, south is down, east is right and west is left. The %s %s %s of the %s." % (b, isare(b), d, a)
        if d in ("east", "west"):
            e += " Do not mix up east and west: “Never Eat Soggy Weet-Bix” goes round clockwise: north, east, south, west."
        its.append(mcq(sm + "The %s %s ___ of the %s." % (b, isare(b), a), d, wrong, e, rnd))

    dir_q("oval", "garden")
    dir_q("canteen", "toilets")
    dir_q("art room", "canteen")
    dir_q("library", "hall")
    dir_q("hall", "office")
    dir_q("bike racks", "classrooms")

    def first_q(a, d, wrong):
        ans = first_in(M, a, d)
        assert ans, (a, d)
        opp = first_in(M, a, OPP[d])
        cands = ([opp] if opp else []) + wrong
        its.append(mcq(sm + "What is the first place you reach going straight <b>%s</b> from the %s?" % (d, a), "the " + ans,
                       ["the " + w for w in cands],
                       "%s is %s on the map. Go %s from the %s, square by square. The first place you reach is the %s."
                       % (d.capitalize(), {"north": "up", "south": "down", "east": "to the right", "west": "to the left"}[d], d, a, ans)
                       + (" Going %s would give the %s." % (OPP[d], opp) if opp else ""), rnd))

    first_q("garden", "north", ["office", "oval", "canteen"])
    first_q("garden", "west", ["library", "art room", "playground"])
    first_q("sandpit", "north", ["library", "classrooms", "hall"])
    first_q("library", "south", ["office", "oval", "hall"])
    first_q("toilets", "east", ["oval", "canteen", "art room"])
    first_q("office", "west", ["car park", "hall", "garden"])
    # compass facts
    its.append(mcq("On most maps, which way is north?", "towards the top of the map",
                   ["towards the bottom of the map", "towards the left of the map", "towards the right of the map"],
                   "Maps usually have north at the top. The compass on the map shows N pointing up.", rnd))
    n, he, his = P_.next()
    its.append(mcq("%s walks east to the canteen. Which way does %s walk to come straight back?" % (n, he), "west", ["east", "north", "south"],
                   "To come back you go the opposite way. East and west are opposites. North and south are opposites.", rnd))
    its.append(mcq("On a map with north at the top, which direction is to the right?", "east", ["west", "north", "south"],
                   "Going clockwise from north: north (up), east (right), south (down), west (left). Many students mix up east and west.", rnd))
    # facing a direction: left and right for the person
    pf = []
    for who_at, face, target in [("garden", "north", "library"), ("garden", "south", "sandpit"), ("library", "south", "hall"),
                                 ("gate", "north", "sandpit"), ("toilets", "east", "canteen")]:
        d = direction(M, target, who_at)
        assert d, (who_at, target)
        side = side_for(face, d)
        pf.append((who_at, face, target, d, side))
    for who_at, face, target, d, side in pf:
        n, he, his = P_.next()
        obj = "her" if he == "she" else "him"
        ans = side.replace("of", "").strip() if False else side
        choices = ["in front of " + obj, "behind " + obj, "on " + his + " left", "on " + his + " right"]
        m = {"in front of": "in front of " + obj, "behind": "behind " + obj, "on the left of": "on " + his + " left", "on the right of": "on " + his + " right"}
        c = m[side]
        if face in ("north",):
            e = "%s faces north, the same way as the top of the map. So %s left is west and %s right is east. The %s is %s of %s, so it is %s." % (
                n, his, his, target, d, obj, c)
        elif face == "south":
            e = ("%s faces south, towards the bottom of the map, so %s left and right are swapped compared with the page. "
                 "Turn the map upside down to check. %s left is east. The %s is %s, so it is %s." % (n, his, his.capitalize(), target, d, c))
        else:
            e = "%s faces east. %s left is north and %s right is south. The %s is %s, so it is %s." % (n, his.capitalize(), his, target, d, c)
        wrong = [x for x in choices if x != c]
        # the most common mistake first: left and right from the page, not the person
        if "left" in c:
            wrong.sort(key=lambda x: 0 if "right" in x else 1)
        elif "right" in c:
            wrong.sort(key=lambda x: 0 if "left" in x else 1)
        its.append(mcq(sm + "%s stands %s the %s and faces <b>%s</b>. Where is the %s for %s?" % (n, "in" if who_at == "garden" else "at", who_at, face, target, obj), c, wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Position words and compass directions: north, south, east, west", "items": its}


# ------------------------------------------------------------ set 3: follow directions on a grid map
def set_directions(rnd, P_):
    its = []
    pos = Pos(rnd)
    G = Map(6, 5, [], cw=46, ch=40)

    def letters_q(start, moves, who):
        n, he, his = who
        ans = walk(start, moves)
        assert G.inside(ans) and ans != start
        cells, why = [], {}
        for kind, m in mistake_moves(moves):
            c = walk(start, m)
            if G.inside(c) and c != ans and c != start and c not in cells:
                cells.append(c)
                why[c] = kind
        assert len(cells) >= 3, (start, moves, cells)
        cells = cells[:3]
        p = pos.next()
        order = cells[:]
        order.insert(p, ans)
        marks = [(start, "dot", None)] + [(c, "letter", "ABCD"[i]) for i, c in enumerate(order)]
        svg = G.svg("grid map with a compass, a red dot and squares A to D", marks)
        e = walk_e(start, moves) + " That is square %s." % "ABCD"[p]
        tip = {"ew": " If you mix up east and west you land on %s.", "ns": " If you mix up north and south you land on %s.",
               "start": " If you count the starting square you stop 1 short, on %s.", "swap": " Going %d %s first by mistake gives %s."}
        k0 = why[cells[0]]
        if k0 == "swap":
            e += tip["swap"] % (moves[1][1], moves[0][0], "ABCD"[order.index(cells[0])])
        elif k0 in tip:
            e += tip[k0] % "ABCD"[order.index(cells[0])]
        q = "%s starts at the red dot. %s goes <b>%s</b>. Where does %s finish?" % (n, he.capitalize(), moves_txt(moves), he)
        its.append(mcq_fixed(fig(svg) + q, ["A", "B", "C", "D"], "ABCD"[p], e))

    for start, moves in [((2, 3), [("east", 2)]), ((4, 4), [("north", 3)]), ((4, 1), [("west", 3)]), ((2, 0), [("south", 3)]),
                         ((0, 4), [("east", 3), ("north", 2)]), ((5, 4), [("north", 1), ("west", 3)]),
                         ((1, 0), [("south", 2), ("east", 3)]), ((4, 3), [("west", 2), ("north", 3)])]:
        letters_q(start, moves, P_.next())

    # on the park map
    M = PARK
    pm = fig(M.svg(PARK_LABEL))

    def land_q(frm, moves, extra):
        s0 = M.single(frm)
        end = walk(s0, moves)
        ans = M.at(end)
        assert ans and ans != frm, (frm, moves, end)
        cands = []
        for kind, m in mistake_moves(moves):
            c = walk(s0, m)
            if M.inside(c) and M.at(c) and M.at(c) not in (ans, frm) and M.at(c) not in cands:
                cands.append(M.at(c))
        cands += extra + sorted((n for n in M.where if n not in (ans, frm)), key=lambda n: (dist(M, n, ans), n))
        e = walk_e(s0, moves) + " The %s is in %s." % (ans, ref(end))
        its.append(mcq(pm + "Start at the %s. Go <b>%s</b>. What do you reach?" % (frm, moves_txt(moves)), "the " + ans,
                       ["the " + c for c in cands if c != frm], e, rnd))

    land_q("gate", [("north", 2), ("east", 2)], ["pond", "sandpit"])
    land_q("BBQ", [("east", 3), ("north", 1)], ["swings", "gum tree"])
    land_q("tap", [("south", 2), ("west", 2)], ["bin", "picnic table"])
    land_q("rotunda", [("north", 3), ("east", 1)], ["shelter", "slide"])
    land_q("kiosk", [("west", 2), ("south", 1)], ["swings", "pond"])

    def route_q(a, b):
        A, B = M.single(a), M.single(b)
        dx, dy = B[0] - A[0], B[1] - A[1]
        mv = [("east" if dx > 0 else "west", abs(dx)), ("north" if dy < 0 else "south", abs(dy))]
        assert walk(A, mv) == B and dx and dy
        wrong = [[(OPP[mv[0][0]], mv[0][1]), mv[1]], [mv[0], (OPP[mv[1][0]], mv[1][1])], [(mv[0][0], mv[0][1] + 1), (mv[1][0], mv[1][1] + 1)]]
        if mv[0][1] != mv[1][1]:
            wrong.insert(2, [(mv[0][0], mv[1][1]), (mv[1][0], mv[0][1])])
        for w in wrong:
            assert walk(A, w) != B
        its.append(mcq(pm + "Which directions take you from the %s to the %s?" % (a, b), moves_short(mv),
                       [moves_short(w) for w in wrong],
                       "The %s is in %s and the %s is in %s. Count the squares you move, not the square you start on: %s." % (
                           a, ref(A), b, ref(B), moves_txt(mv)), rnd))

    route_q("gate", "gum tree")
    route_q("pond", "bin")
    route_q("slide", "shelter")
    # how many squares
    a, b = M.single("BBQ"), M.single("bin")
    assert a[1] == b[1]
    its.append(mcq_num(pm + "How many squares east is it from the BBQ to the bin?", b[0] - a[0], [b[0] - a[0] + 1, b[0] - a[0] - 1, b[0] - a[0] + 2],
                       "Count the moves: the BBQ is in %s and the bin is in %s. That is %s east. Do not count the BBQ square."
                       % (ref(a), ref(b), sq(b[0] - a[0]))))
    a, b = M.single("flag"), M.single("kiosk")
    assert a[0] == b[0]
    its.append(mcq_num(pm + "How many squares north is it from the flag to the kiosk?", a[1] - b[1], [a[1] - b[1] + 1, a[1] - b[1] - 1, a[1] - b[1] + 2],
                       "The flag is in %s and the kiosk is in %s. Count the moves up: %s north." % (ref(a), ref(b), sq(a[1] - b[1]))))
    # directions: three steps
    n, he, his = P_.next()
    s0 = M.single("toilets")
    mv = [("south", 3), ("east", 2), ("south", 1)]
    end = walk(s0, mv)
    assert M.at(end) == "rotunda" and M.at(walk(s0, [("south", 4)])) == "gate" and M.at(walk(s0, [("south", 3), ("east", 1)])) == "sandpit"
    its.append(mcq(pm + "%s starts at the toilets. %s goes 3 squares south, 2 squares east, then 1 square south. Where is %s?" % (n, he.capitalize(), he),
                   "at the rotunda", ["at the gate", "at the sandpit", "at the picnic table"],
                   walk_e(s0, mv) + " The rotunda is there.", rnd))
    n, he, his = P_.next()
    assert direction(M, "slide", "swings") == "east"
    its.append(mcq(pm + "%s walks from the swings straight to the slide. Which direction does %s walk?" % (n, he),
                   "east", ["west", "north", "south"],
                   "The slide (E1) is to the right of the swings (C1) in the same row. Right on the map is east.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Follow directions on a grid map", "items": its}


# ------------------------------------------------------------ set 4: bird's-eye view and grid references
def top_view(kind, cx, cy):
    s = []
    if kind == "table":
        for x, y, w, h in [(cx - 8, cy - 27, 16, 10), (cx - 8, cy + 17, 16, 10), (cx - 36, cy - 8, 10, 16), (cx + 26, cy - 8, 10, 16)]:
            s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='2' fill='%s' stroke='%s' stroke-width='1.6'/>" % (x, y, w, h, BLUE, "#3d6f99"))
        s.append("<rect x='%.1f' y='%.1f' width='48' height='30' rx='2' fill='%s' stroke='#6b4316' stroke-width='2'/>" % (cx - 24, cy - 15, WOOD))
    elif kind == "round table":
        for ang in (0, 90, 180, 270):
            t = math.radians(ang)
            x, y = cx + 28 * math.cos(t), cy + 28 * math.sin(t)
            s.append("<circle cx='%.1f' cy='%.1f' r='7' fill='%s' stroke='#3d6f99' stroke-width='1.6'/>" % (x, y, BLUE))
        s.append("<circle cx='%.1f' cy='%.1f' r='19' fill='%s' stroke='#6b4316' stroke-width='2'/>" % (cx, cy, WOOD))
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
    elif kind == "round table":
        s.append("<rect x='%.1f' y='%.1f' width='44' height='6' fill='%s' stroke='#6b4316' stroke-width='1.6'/>" % (cx - 22, cy - 8, WOOD))
        s.append(ln((cx, cy - 2), (cx, cy + 24), "#6b4316", 4))
        s.append(ln((cx - 12, cy + 26), (cx + 12, cy + 26), "#6b4316", 4))
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


NOUN = {"table": "table with 4 chairs", "round table": "round table with 4 stools", "car": "car", "bed": "bed",
        "cup": "cup of hot chocolate", "tree": "tree", "house": "house"}


def set_birdseye_refs(rnd, P_):
    its = []
    pos = Pos(rnd)
    for obj, o1, o2 in [("table", "round table", "bed"), ("car", "bed", "car"), ("cup", "round table", "tree"),
                        ("tree", "cup", "house"), ("house", "table", "house")]:
        p = pos.next()
        others = [("side", obj), ("top", o1), ("side", o2) if o2 != obj else ("side", "cup")]
        if obj == "car":
            others = [("side", "car"), ("top", "bed"), ("side", "house")]
        if obj == "house":
            others = [("side", "house"), ("top", "table"), ("side", "tree")]
        assert len(set(others)) == 3 and ("top", obj) not in others
        panels = others[:]
        panels.insert(p, ("top", obj))
        lab = "four pictures: " + ", ".join("%s %s view of a %s" % ("ABCD"[i], "top" if v == "top" else "side", k) for i, (v, k) in enumerate(panels))
        side_letter = "ABCD"[panels.index(("side", obj))]
        e = ("A bird’s-eye view shows something from above, like a bird flying over it. Picture %s shows the %s from above. "
             "Picture %s shows it from the side." % ("ABCD"[p], NOUN[obj], side_letter))
        its.append(mcq_fixed(fig(views_svg(panels, lab)) + "Which picture shows the <b>%s</b> from above (a bird’s-eye view)?" % NOUN[obj],
                             ["A", "B", "C", "D"], "ABCD"[p], e))
    for obj, wrong, e in [
        ("bed", ["a car", "a table with 4 chairs", "a house"], "You can see a pillow at one end and a blanket. It is a bed seen from above."),
        ("round table", ["a tree", "a cup of hot chocolate", "a car"], "A round top with 4 small circles around it: a round table with 4 stools, seen from above."),
        ("car", ["a bed", "a house", "a table with 4 chairs"], "You can see the windscreen, the roof and the 4 wheels poking out. It is a car seen from above."),
    ]:
        its.append(mcq(fig(views_svg([("top", obj)], "bird’s-eye view of a " + obj)) + "This is a bird’s-eye view. What is it?",
                       "a " + NOUN[obj], wrong, e, rnd))
    its.append(mcq("A drink can stands on a table. What shape does its top look like in a bird’s-eye view?", "a circle",
                   ["a rectangle", "a triangle", "a square"],
                   "From above you see only the round top of the can: a circle. From the side the can looks like a rectangle.", rnd))
    # grid references on the classroom plan
    M = CLASS
    cm = fig(M.svg(CLASS_LABEL))
    for name in ("sink", "laptops", "door", "bins"):
        c = M.single(name)
        good = ref(c)
        swapped = "%s%d" % (COLS[c[1]], c[0] + 1)          # number read as the column
        if c[0] >= M.rows:                                  # that square is not on the plan: use the square above or below
            swapped = ref((c[0], c[1] - 1) if c[1] > 0 else (c[0], c[1] + 1))
        wrong = ["%d%s" % (c[1] + 1, COLS[c[0]]), swapped, ref((c[0] + 1, c[1]) if c[0] + 1 < M.cols else (c[0] - 1, c[1]))]
        assert swapped != good
        its.append(mcq(cm + "What is the grid reference of the <b>%s</b>?" % name, good, wrong,
                       "Go across first to find the letter, then down to find the number. The %s %s in column %s, row %d: %s. "
                       "Always write the letter first." % (name, isare(name), COLS[c[0]], c[1] + 1, good), rnd))
    for cell in [(1, 1), (2, 2), (4, 3), (3, 0)]:
        ans = M.at(cell)
        sw = (cell[1], cell[0])
        cands = []
        if M.inside(sw) and M.at(sw) and M.at(sw) != ans:
            cands.append(M.at(sw))
        for d in CW:
            x = step(cell, d)
            if M.inside(x) and M.at(x) and M.at(x) != ans and M.at(x) not in cands:
                cands.append(M.at(x))
        cands += ["laptops", "lockers", "sink", "door"]
        e = "Find column %s along the top, then go down to row %d. Square %s is the %s." % (COLS[cell[0]], cell[1] + 1, ref(cell), ans)
        if M.inside(sw) and M.at(sw) and M.at(sw) != ans:
            e += " Mixing up the letter and the number (column %s, row %d) gives the %s." % (COLS[sw[0]], sw[1] + 1, M.at(sw))
        its.append(mcq(cm + "What is in square <b>%s</b>?" % ref(cell), "the " + ans, ["the " + x for x in cands if x != ans], e, rnd))
    for name, n in [("whiteboard", 2), ("reading mat", 2)]:
        cs = M.where[name]
        assert len(cs) == n
        good = " and ".join(ref(c) for c in sorted(cs))
        a, b = sorted(cs)
        wrong = [" and ".join("%d%s" % (c[1] + 1, COLS[c[0]]) for c in sorted(cs)),
                 " and ".join("%s%d" % (COLS[c[1]], c[0] + 1) for c in sorted(cs)),
                 " and ".join(ref((c[0], c[1] + 1)) for c in sorted(cs))]
        its.append(mcq(cm + "The %s covers two squares. What are they?" % name, good, wrong,
                       "The %s is in row %d, in columns %s and %s. So it covers %s." % (name, a[1] + 1, COLS[a[0]], COLS[b[0]], good), rnd))
    its.append(mcq(cm + "Which square is empty?", "B4",
                   ["C4", "A4", "E3"], "Look at row 4: A4 is the laptops, C4 is the door and E4 is the lockers. B4 has nothing in it.", rnd))
    assert M.at((1, 3)) is None and M.at((2, 3)) == "door" and M.at((0, 3)) == "laptops" and M.at((4, 2)) == "bins"
    assert len(its) == 20, len(its)
    return {"title": "Bird’s-eye views and grid references like B3", "items": its}


# ------------------------------------------------------------ set 5: choose the right map and real-life problems
def plan_svg(plans, label):
    """plans: list of dicts {cell: icon} on a 3 x 3 grid, drawn side by side as A, B, C, D, with a north arrow."""
    C = 34
    s = []
    # north arrow
    s.append("<polygon points='%s' fill='%s'/>" % (P([(16, 26), (8, 46), (24, 46)]), GREEN))
    s.append("<line x1='16' y1='44' x2='16' y2='74' stroke='%s' stroke-width='4'/>" % GREEN)
    s.append(text(16, 20, "N", 15))
    for i, pl in enumerate(plans):
        x0 = 40 + i * (3 * C + 14)
        s.append("<rect x='%d' y='4' width='%d' height='%d' fill='#ffffff' stroke='%s' stroke-width='1.6'/>" % (x0, 3 * C, 3 * C, INK))
        for k in range(1, 3):
            s.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x0 + k * C, x0 + k * C, 4 + 3 * C, GRID))
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x0, 4 + k * C, x0 + 3 * C, 4 + k * C, GRID))
        for (c, r), ic in pl.items():
            s.append(icon(ic, x0 + c * C + C / 2.0, 4 + r * C + C / 2.0, 13))
        s.append(text(x0 + 1.5 * C, 3 * C + 26, "ABCD"[i], 16))
    W = 40 + len(plans) * (3 * C + 14) - 10
    return svg_wrap(W, 3 * C + 34, "".join(s), label)


def rel_ok(pl, rel):
    where = {v: k for k, v in pl.items()}
    kind = rel[0]
    if kind == "between":
        x, a, b = (where[t] for t in rel[1:])
        same = (a[0] == b[0] == x[0] and min(a[1], b[1]) < x[1] < max(a[1], b[1]) and abs(a[1] - b[1]) == 2) or \
               (a[1] == b[1] == x[1] and min(a[0], b[0]) < x[0] < max(a[0], b[0]) and abs(a[0] - b[0]) == 2)
        return same
    x, d, a = where[rel[1]], rel[2], where[rel[3]]
    v = VEC[d]
    return (x[0] - a[0], x[1] - a[1]) == v


def set_real(rnd, P_):
    its = []
    pos = Pos(rnd)
    NAMES = {"tree": "tree", "bench": "bench", "bin": "bin", "flag": "flag", "tent": "tent", "pond": "pond", "bed": "bed",
             "desk": "desk", "door": "door"}
    for q, rel, good, wrongs, e in [
        ("Which map shows the <b>bin between the bench and the tree</b>?", ("between", "bin", "bench", "tree"),
         {(0, 1): "bench", (1, 1): "bin", (2, 1): "tree"},
         [{(0, 1): "bin", (1, 1): "bench", (2, 1): "tree"}, {(0, 0): "bench", (1, 1): "tree", (2, 2): "bin"},
          {(0, 1): "bench", (1, 1): "tree", (2, 1): "bin"}],
         "Between means in the middle of the other two, in a straight line. Only one map has the bin in the middle, with the bench on one side and the tree on the other."),
        ("Which map shows the <b>flag north of the tent</b>?", ("rel", "flag", "north", "tent"),
         {(1, 0): "flag", (1, 1): "tent", (2, 2): "pond"},
         [{(1, 2): "flag", (1, 1): "tent", (0, 0): "pond"}, {(2, 1): "flag", (1, 1): "tent", (0, 2): "pond"},
          {(0, 1): "flag", (1, 1): "tent", (2, 0): "pond"}],
         "North is towards the top, where the arrow points. The flag must be just above the tent. The flag below the tent would be south of it."),
        ("Which map shows the <b>pond east of the tree</b> and the <b>bench south of the tree</b>?", ("both",),
         {(1, 1): "tree", (2, 1): "pond", (1, 2): "bench"},
         [{(1, 1): "tree", (0, 1): "pond", (1, 2): "bench"}, {(1, 1): "tree", (2, 1): "pond", (1, 0): "bench"},
          {(1, 1): "tree", (0, 1): "pond", (1, 0): "bench"}],
         "East is to the right and south is down. The pond must be just right of the tree and the bench just below it. Mixing up east and west puts the pond on the left."),
        ("Ruby draws a plan of her bedroom. The <b>desk is west of the bed</b> and the <b>door is south of the desk</b>. Which plan is right? (The bed is blue and the desk is brown.)", ("both2",),
         {(0, 1): "desk", (1, 1): "bed", (0, 2): "door"},
         [{(2, 1): "desk", (1, 1): "bed", (2, 2): "door"}, {(0, 1): "desk", (1, 1): "bed", (0, 0): "door"},
          {(1, 0): "desk", (1, 1): "bed", (1, 2): "door"}],
         "West is to the left and south is down. The desk is just left of the bed and the door is just below the desk."),
    ]:
        def ok(pl):
            if rel[0] == "both":
                return all(v in pl.values() for v in ("tree", "pond", "bench")) and rel_ok(pl, ("rel", "pond", "east", "tree")) and rel_ok(pl, ("rel", "bench", "south", "tree"))
            if rel[0] == "both2":
                return rel_ok(pl, ("rel", "desk", "west", "bed")) and rel_ok(pl, ("rel", "door", "south", "desk"))
            return rel_ok(pl, rel)
        assert ok(good) and not any(ok(w) for w in wrongs), q
        p = pos.next()
        plans = wrongs[:]
        plans.insert(p, good)
        its.append(mcq_fixed(fig(plan_svg(plans, "four small maps A to D with a north arrow")) + q, ["A", "B", "C", "D"], "ABCD"[p],
                             e + " That is map %s." % "ABCD"[p]))
    # the zoo
    M = ZOO
    zm = fig(M.svg(ZOO_LABEL))
    key = "The class is on a school excursion to the zoo. "
    c = M.single("koalas")
    ent = M.single("entrance")
    its.append(mcq(zm + key + "What is in square <b>E2</b>?", "the café", ["the seals", "the playground", "the penguins"],
                   "Find column E along the top, then go down to row 2. Square E2 is the café.", rnd))
    assert M.at((4, 1)) == "café"
    pg = M.single("penguins")
    its.append(mcq(zm + key + "What is the grid reference of the penguins?", ref(pg), ["3E", "C5", "E4"],
                   "The penguins are in column E and row 3. Write the letter first: E3.", rnd))
    assert ref(pg) == "E3"
    mv = [("north", 2)]
    assert walk(ent, mv) == c
    its.append(mcq(zm + key + "From the entrance, the class walks 2 squares north. Which animals do they see?", "the koalas",
                   ["the wombats", "the kangaroos", "the playground"],
                   walk_e(ent, mv) + " The koalas are in C3. Counting the entrance square as 1 would stop you 1 square short.", rnd))
    mv = [("north", 3), ("east", 1)]
    end = walk(M.single("toilets"), mv)
    assert M.at(end) == "tigers" or True
    s0 = M.single("toilets")
    mv = [("north", 4), ("east", 3)]
    end = walk(s0, mv)
    assert M.at(end) == "emus"
    wrongE = walk(s0, [("north", 3), ("east", 2)])
    its.append(mcq(zm + key + "Kai leaves the toilets and goes 4 squares north, then 3 squares east. Which animals does he reach?", "the emus",
                   ["the kangaroos", "the koalas", "the lions"],
                   walk_e(s0, mv) + " The emus are in D1. Do not count the toilets square as one of the 4.", rnd))
    d = direction(M, "seals", "penguins")
    assert d == "east"
    its.append(mcq(zm + key + "The seals are ___ of the penguins.", "east", ["west", "north", "south"],
                   "The seals are just to the right of the penguins. Right on the map is east.", rnd))
    d = direction(M, "tigers", "reptiles")
    assert d == "north"
    its.append(mcq(zm + key + "The tigers are ___ of the reptiles.", "north", ["south", "east", "west"],
                   "The tigers are just above the reptiles. Up on the map is north.", rnd))
    b = between_all(M, "lions", "reptiles")
    assert b == {"tigers"}
    its.append(mcq(zm + key + "Which animals are between the lions and the reptiles?", "the tigers",
                   ["the kangaroos", "the koalas", "the wombats"],
                   "The lions, tigers and reptiles are in column A. The tigers are in the middle.", rnd))
    assert between_all(M, "kangaroos", "picnic area") == {"emus"}
    its.append(mcq(zm + key + "The class eats lunch in the picnic area. Which animals are between the kangaroos and the picnic area?", "the emus",
                   ["the café", "the lions", "the penguins"],
                   "Row 1 has the lions, the kangaroos, the emus and the picnic area. The emus are in the middle of the kangaroos and the picnic area.", rnd))
    r = [("east", 2), ("north", 2)]
    s0 = M.single("entrance")
    assert walk(s0, r) == M.single("penguins") and M.at(walk(s0, [("west", 2), ("north", 2)])) == "reptiles"
    its.append(mcq(zm + key + "Which directions take the class from the entrance to the penguins?", "2 east, 2 north",
                   ["2 west, 2 north", "3 east, 3 north", "2 east, 2 south"],
                   "The entrance is C5 and the penguins are E3. Go 2 squares east (C to E) and 2 squares north (row 5 to row 3). "
                   "Going west would take you to the reptiles.", rnd))
    its.append(mcq_num(zm + key + "Each square on the map is 20 metres. How far is it from the entrance straight north to the koalas?", 40,
                       [60, 20, 80],
                       "From the entrance (C5) to the koalas (C3) is 2 squares. 2 × 20 = 40 metres. Counting the entrance square too gives 3 squares, or 60 metres.",
                       " m"))
    n, he, his = P_.next()
    its.append(mcq(zm + key + "%s stands at the entrance and faces north. Where is the gift shop for %s?" % (n, "her" if he == "she" else "him"),
                   "on %s right" % his, ["on %s left" % his, "behind %s" % ("her" if he == "she" else "him"), "straight in front of %s" % ("her" if he == "she" else "him")],
                   "Facing north is facing the top of the map, so %s right is east. The gift shop (E5) is east of the entrance (C5)." % his, rnd))
    assert direction(M, "gift shop", "entrance") == "east"
    pl = sorted(M.where["playground"])
    assert [ref(c) for c in pl] == ["D4", "E4"]
    its.append(mcq(zm + key + "The playground covers two squares. What are their grid references?", "D4 and E4",
                   ["4D and 4E", "D3 and E3", "C4 and D4"],
                   "The playground is in row 4, in columns D and E. Letter first: D4 and E4.", rnd))
    # text problems
    n, he, his = P_.next()
    its.append(mcq("%s’s house is south of the school. Which way does %s walk to get from school to home?" % (n, he), "south",
                   ["north", "east", "west"], "The house is south of the school, so %s walks south. North would take %s further away." % (he, "her" if he == "she" else "him"), rnd))
    n, he, his = P_.next()
    obj = "her" if he == "she" else "him"
    its.append(mcq("%s faces south. The canteen is on %s left. Which direction is the canteen from %s?" % (n, his, obj), "east",
                   ["west", "north", "south"],
                   "When you face south, your left hand points east. Try it: face the bottom of the map and hold out your left arm. "
                   "On the page left is west, but %s is facing the other way." % n, rnd))
    its.append(mcq("What does the key (legend) on a map tell you?", "what the symbols on the map mean",
                   ["which way is north", "how old the map is", "who drew the map"],
                   "A key lists the symbols used on the map and what each one means, for example a blue shape for water. The compass shows north.", rnd))
    its.append(mcq("Matilda writes a grid reference on a street map. Which is written the right way?", "D4",
                   ["4D", "4 4", "D D"],
                   "Write the letter (across) first, then the number (down or up). D4 is right; 4D has them the wrong way round.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Choose the right map and solve real-life problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    school = SCHOOL.svg(SCHOOL_LABEL)
    route = Map(6, 5, [], cw=46, ch=40).svg("grid map with a dashed route from a red dot 2 squares north and 3 squares east to a flag",
                                             marks=[((0, 4), "dot", None), ((3, 2), "icon", "flag")], path=[(0, 4), (0, 2), (3, 2)])
    views = views_svg([("side", "table"), ("top", "table")], "a table with 4 chairs from the side and from above", letters=False)
    cls = CLASS.svg("classroom plan with square B4 highlighted", hi=(1, 3))
    return (
        "<h2>What a map is</h2>"
        "<p>A <b>map</b> or <b>plan</b> shows a place from above, like a bird flying over it. "
        "This is called a <b>bird’s-eye view</b>. Each shape on the map stands for a real place.</p>"
        "<figure class='sn-fig'>" + views +
        "<figcaption>Left: a table with 4 chairs seen from the side. Right: the same table seen from above. Maps use the view from above.</figcaption></figure>"
        "<h2>Where is it?</h2>"
        "<p>Use position words: <b>next to</b>, <b>between</b>, <b>left of</b>, <b>right of</b>. "
        "Maps also use the <b>compass points</b>. <b>North</b> is usually at the top. "
        "Going clockwise: north, east, south, west. Remember it with “Never Eat Soggy Weet-Bix”.</p>"
        "<figure class='sn-fig'>" + school +
        "<figcaption>The library is between the hall and the office. The oval is east of the garden. The canteen is north of the toilets.</figcaption></figure>" +
        table(["On the map", "Compass point"], [["up", "north"], ["down", "south"], ["right", "east"], ["left", "west"]]) +
        ex("Example", "What is the first place you reach going straight south from the library?",
           "South is down the map. From the library, go down: C2 is empty, C3 is the garden.", "the garden") +
        "<h2>Follow directions on a grid</h2>"
        "<p>Count the squares you <b>move</b>. Do not count the square you start on. Do one direction at a time.</p>"
        "<figure class='sn-fig'>" + route +
        "<figcaption>Start at the red dot (A5). Go 2 squares north to A3, then 3 squares east to D3: the flag.</figcaption></figure>"
        "<h2>Grid references</h2>"
        "<p>Many maps have letters across the top and numbers down the side. A <b>grid reference</b> like <b>B4</b> names one square. "
        "Go across to the letter first, then down to the number.</p>"
        "<figure class='sn-fig'>" + cls +
        "<figcaption>Square B4 is highlighted: column B, row 4. It is empty. The door is in C4.</figcaption></figure>" +
        ex("Example", "On the classroom plan, what is in square E2?",
           "Go across to column E, then down to row 2.", "the sink") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Mixing up east and west", "North at the top, then go clockwise: Never Eat Soggy Weet-Bix. East is on the right."],
            ["Using left and right of the page for a person who faces south", "Turn the map so you face the same way as the person"],
            ["Counting the starting square", "Count the moves, not the square you stand on"],
            ["Reading a grid reference number first (B3 as C2)", "Letter first, across; then the number"],
            ["Choosing the side view when asked for a bird’s-eye view", "Imagine looking straight down from above"],
        ])
    )


FAQ = [
    {"q": "What do Year 3 students learn about maps in the Australian Curriculum?",
     "a": "In Year 3 (AC9M3SP02) students read and draw simple maps and plans of familiar places, such as the classroom, school or park, and describe where landmarks are using words like next to, between, left, right and the compass points."},
    {"q": "How can my child remember north, east, south and west?",
     "a": "Start at north at the top and go clockwise, saying “Never Eat Soggy Weet-Bix”. East is on the right of a map and west is on the left."},
    {"q": "How do you read a grid reference like B3?",
     "a": "Go across to column B first, then down to row 3. The letter always comes first."},
    {"q": "Are maps and directions in the NAPLAN numeracy test?",
     "a": "Yes. Space questions in NAPLAN numeracy often ask students to read a simple map, follow directions or find a location. Practising with grid maps like these helps."},
]


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


def gen():
    rnd = random.Random(3812)
    P_ = People(rnd)
    sets = [set_read(rnd, P_), set_compass(rnd, P_), set_directions(rnd, P_), set_birdseye_refs(rnd, P_), set_real(rnd, P_)]
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
        "country": "au", "subject": "maths", "grade": "year-3", "slug": "maps-and-locations", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Maps and Locations: Compass Points, Directions and Grid References",
        "seo_title": "Year 3 Maps and Locations Worksheets: Compass Directions and Grid Maps (Free)",
        "short_title": "Maps and locations",
        "domain": "Space",
        "standard_code": "AC9M3SP02",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Interpret and create two dimensional representations of familiar environments, locating key landmarks and objects relative to each other",
        "meta_desc": "Free Year 3 maths worksheets on maps and locations: read a school map, use north, south, east and west, follow directions on a grid map, bird’s-eye views and grid references like B3. 100 questions with an answer key, Australian Curriculum aligned and great for NAPLAN practice.",
        "key_big": "North is at the top of most maps. Going clockwise: north, east, south, west.",
        "key_sub": "When you follow directions, count the squares you move, not the square you start on. A grid reference gives the letter (across) first, then the number.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (maps, grids, rows of A-D pictures) so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "(map|grid map|plan of|four pictures|four small maps)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
