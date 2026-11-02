# -*- coding: utf-8 -*-
"""
AU Year 4 Maths: Grid references and maps (Australian Curriculum v9.0, AC9M4SP02)
  python3 tools/gen_au_maths_y4_grid_references.py
HTML attributes use single quotes (no backslashes in the JSON).

Year 4 students create and interpret grid reference systems: they read and write grid references (B3),
use the eight compass points (N, NE, E, SE, S, SW, W, NW) and numbers of squares to give and follow
directions, and describe pathways between places on a map.
Same grid convention as the Year 3 maps unit: letters go across (west to east), numbers go down
(north to south), so row 1 is the top row.
Every map is a model in code (cells of a grid). Every answer is worked out from that model.
Wrong answers come from real mistakes: writing or reading the number first (3B, B3 read as C2),
mixing up east and west or north and south (north-east for north-west), turning the wrong way,
counting the starting square, and naming in-between directions the wrong way round (east-north).
Australian English.
"""
import json, math, os, random, re
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
INK = "#2b2b2b"
GRID = "#b9b3a9"
RED = "#e06666"
BLUE = "#9fc5e8"
BROWN = "#a0692a"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]
COLS = "ABCDEFGH"

DIR8 = ["north", "north-east", "east", "south-east", "south", "south-west", "west", "north-west"]   # clockwise
VEC = dict(zip(DIR8, [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]))
VDIR = {v: d for d, v in VEC.items()}
ABBR = dict(zip(DIR8, ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]))


def opp(d):
    return DIR8[(DIR8.index(d) + 4) % 8]


def turn(d, k):
    """k eighth turns clockwise (negative: anticlockwise)."""
    return DIR8[(DIR8.index(d) + k) % 8]


def flip_ew(d):
    v = VEC[d]
    return VDIR[(-v[0], v[1])]


def flip_ns(d):
    v = VEC[d]
    return VDIR[(v[0], -v[1])]


def sgn(x):
    return (x > 0) - (x < 0)


def dir_between(a, b):
    """Direction and number of squares from cell a to cell b, if b is in one of the 8 directions."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    if (dx, dy) == (0, 0):
        return None
    if dx == 0 or dy == 0 or abs(dx) == abs(dy):
        return VDIR[(sgn(dx), sgn(dy))], max(abs(dx), abs(dy))
    return None


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


def ref_nf(cell):
    """The grid reference written number first (a common mistake)."""
    return "%d%s" % (cell[1] + 1, COLS[cell[0]])


def step(cell, d, n=1):
    v = VEC[d]
    return (cell[0] + v[0] * n, cell[1] + v[1] * n)


def walk(start, moves):
    x = start
    for d, n in moves:
        x = step(x, d, n)
    return x


def cells_on(start, moves):
    """Every square you pass through or stop on (not the start)."""
    out, x = [], start
    for d, n in moves:
        for _ in range(n):
            x = step(x, d)
            out.append(x)
    return out


def moves_txt(moves):
    return ", then ".join("%s %s" % (sq(n), d) for d, n in moves)


def moves_short(moves):
    return ", ".join("%d %s" % (n, d) for d, n in moves)


def walk_e(start, moves):
    x = start
    parts = []
    for d, n in moves:
        x = step(x, d, n)
        parts.append("%s %s to %s" % (sq(n), d, ref(x)))
    return "Start at %s. Go %s." % (ref(start), ", then ".join(parts))


def mistake_moves(moves):
    """Moves a student makes by mistake, most common first."""
    out = []
    if any(VEC[d][0] for d, n in moves):
        out.append(("ew", [(flip_ew(d), n) for d, n in moves]))
    if any(VEC[d][1] for d, n in moves):
        out.append(("ns", [(flip_ns(d), n) for d, n in moves]))
    if all(n > 1 for d, n in moves):
        out.append(("start", [(d, n - 1) for d, n in moves]))
    out.append(("plus", [(d, n + 1) for d, n in moves]))
    if len(moves) == 2 and moves[0][1] != moves[1][1]:
        out.append(("swap", [(moves[0][0], moves[1][1]), (moves[1][0], moves[0][1])]))
    for i in range(len(moves)):
        out.append(("plus1", [(d, n + 1 if j == i else n) for j, (d, n) in enumerate(moves)]))
    for i in range(len(moves)):
        if moves[i][1] > 1:
            out.append(("minus1", [(d, n - 1 if j == i else n) for j, (d, n) in enumerate(moves)]))
    out.append(("both", [(opp(d), n) for d, n in moves]))
    for k in (2, -2):
        out.append(("turn", [(turn(d, k), n) for d, n in moves]))
    return out


TIP = {"ew": "Mixing up east and west gives %s.", "ns": "Mixing up north and south gives %s.",
       "start": "Counting the starting square stops you 1 square short, at %s.",
       "plus": "Going 1 square too far each time gives %s.",
       "swap": "Swapping the two numbers of squares gives %s."}


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her", "her") for n in GIRLS] + [(n, "he", "his", "him") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


# ------------------------------------------------------------ drawing
def compass8(cx, cy):
    """An 8-point compass rose: long arrows for N, E, S, W, short ones for NE, SE, SW, NW."""
    s = []
    for i, d in enumerate(DIR8):
        t = math.radians(45 * i)
        u = (math.sin(t), -math.cos(t))
        nr = (-u[1], u[0])
        L, w = (22, 5) if i % 2 == 0 else (14, 3.5)
        tip = (cx + u[0] * L, cy + u[1] * L)
        col = GREEN if i == 0 else ("#8a8478" if i % 2 == 0 else "#b9b3a9")
        s.append("<polygon points='%s' fill='%s'/>" % (P([tip, (cx + nr[0] * w, cy + nr[1] * w), (cx - nr[0] * w, cy - nr[1] * w)]), col))
    s.append("<circle cx='%.1f' cy='%.1f' r='3' fill='#ffffff' stroke='%s' stroke-width='1.2'/>" % (cx, cy, INK))
    s.append(text(cx, cy - 31, "N", 14))
    s.append(text(cx, cy + 42, "S", 14))
    s.append(text(cx + 34, cy + 5, "E", 14))
    s.append(text(cx - 34, cy + 5, "W", 14))
    s.append(text(cx + 26, cy - 19, "NE", 14))
    s.append(text(cx - 26, cy - 19, "NW", 14))
    s.append(text(cx + 26, cy + 30, "SE", 14))
    s.append(text(cx - 26, cy + 30, "SW", 14))
    return "".join(s)


class Map:
    """A grid map. Columns A, B, C ... go across (west to east). Rows 1, 2, 3 ... go down (north to south).
    items: (name, col, row, w, h, kind). kind: b building, g grass, w water, o other, r red."""
    FILLS = {"b": ("#f3e3c3", BROWN), "g": (FILL, GREEN), "w": (BLUE, "#3d6f99"), "o": ("#fff1a8", "#b38f00"),
             "r": ("#f8d7d7", "#a33")}

    def __init__(self, cols, rows, items, cw=66, ch=46, fs=14):
        self.cols, self.rows, self.cw, self.ch, self.fs = cols, rows, cw, ch, fs
        self.items = items
        self.cell, self.where = {}, {}
        for name, c, r, w, h, kind in items:
            assert name not in self.where, name
            cells = [(c + i, r + j) for i in range(w) for j in range(h)]
            for x in cells:
                assert self.inside(x), (name, x)
                assert x not in self.cell, ("two things in one square", name, x)
                self.cell[x] = name
            self.where[name] = cells
            ls = self.lines(name, w)
            assert len(ls) * 15 <= h * ch - 12, name
            for ln in ls:
                assert tw(ln, fs) <= w * cw - 10, ("label too wide", ln)
        self.ox, self.oy = 26, 26

    def lines(self, name, w):
        if tw(name, self.fs) <= w * self.cw - 10 or " " not in name:
            return [name]
        return name.split(" ", 1)

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
        W = self.ox + self.cols * self.cw + 104
        H = max(self.oy + self.rows * self.ch + 4, self.oy + self.rows * self.ch / 2.0 + 50)
        return W, int(math.ceil(H))

    def svg(self, label, marks=(), path=None, hi=None):
        cw, ch, ox, oy = self.cw, self.ch, self.ox, self.oy
        s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff'/>" % (ox, oy, self.cols * cw, self.rows * ch)]
        if hi:
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#ffe08a'/>" % (ox + hi[0] * cw, oy + hi[1] * ch, cw, ch))
        for i in range(self.cols + 1):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>" % (ox + i * cw, oy, ox + i * cw, oy + self.rows * ch, GRID))
        for j in range(self.rows + 1):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>" % (ox, oy + j * ch, ox + self.cols * cw, oy + j * ch, GRID))
        for i in range(self.cols):
            s.append(text(ox + i * cw + cw / 2.0, oy - 8, COLS[i], 15))
        for j in range(self.rows):
            s.append(text(ox - 12, oy + j * ch + ch / 2.0 + 5.5, str(j + 1), 15))
        for name, c, r, w, h, kind in self.items:
            fl, stc = self.FILLS[kind]
            x, y = ox + c * cw + 3, oy + r * ch + 3
            s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='5' fill='%s' stroke='%s' stroke-width='1.6'/>"
                     % (x, y, w * cw - 6, h * ch - 6, fl, stc))
            ls = self.lines(name, w)
            cx, cy = ox + (c + w / 2.0) * cw, oy + (r + h / 2.0) * ch
            for k, ln in enumerate(ls):
                s.append(text(cx, cy + 5 + (k - (len(ls) - 1) / 2.0) * 15, ln, self.fs, bold=False))
        if path:
            s.append(self.path_svg(path))
        for cell, kind, arg in marks:
            assert self.inside(cell), cell
            cx, cy = self.centre(cell)
            if kind == "dot":
                assert cell not in self.cell, ("dot on a place", cell)
                s.append("<circle cx='%.1f' cy='%.1f' r='11' fill='%s' stroke='#7a1f1f' stroke-width='2'/>" % (cx, cy, RED))
            elif kind == "flag":
                assert cell not in self.cell, ("flag on a place", cell)
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5' stroke-linecap='round'/>"
                         % (cx - 7, cy - 14, cx - 7, cy + 14, INK))
                s.append("<polygon points='%s' fill='%s' stroke='#a33' stroke-width='1.5' stroke-linejoin='round'/>"
                         % (P([(cx - 6, cy - 13), (cx + 12, cy - 7), (cx - 6, cy - 1)]), RED))
        s.append(compass8(ox + self.cols * cw + 54, oy + self.rows * ch / 2.0 - 4))
        W, H = self.size()
        return svg_wrap(W, H, "".join(s), label)

    def edge(self, u):
        """Distance from a cell centre to its edge along unit vector u."""
        t = []
        if abs(u[0]) > 1e-9:
            t.append(self.cw / 2.0 / abs(u[0]))
        if abs(u[1]) > 1e-9:
            t.append(self.ch / 2.0 / abs(u[1]))
        return min(t)

    def path_svg(self, corners):
        """A dashed red route through the centres of the corner cells. It starts at the edge of the first
        cell (if that is a place) and the arrow tip stops at the edge of the last cell (if that is a place)."""
        pts = [self.centre(c) for c in corners]

        def unit(a, b):
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            return ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        u0 = unit(pts[0], pts[1])
        if self.at(corners[0]):
            d0 = self.edge(u0)
            pts[0] = (pts[0][0] + u0[0] * d0, pts[0][1] + u0[1] * d0)
        u1 = unit(pts[-2], pts[-1])
        back = self.edge(u1) + 1 if self.at(corners[-1]) else 8
        tip = (pts[-1][0] - u1[0] * back, pts[-1][1] - u1[1] * back)
        base = (tip[0] - u1[0] * 12, tip[1] - u1[1] * 12)
        nr = (-u1[1], u1[0])
        line = pts[:-1] + [base]
        return ("<polyline points='%s' fill='none' stroke='%s' stroke-width='3' stroke-dasharray='6 4' stroke-linecap='round' stroke-linejoin='round'/>"
                % (P(line), RED) +
                "<polygon points='%s' fill='%s'/>" % (P([tip, (base[0] + nr[0] * 7, base[1] + nr[1] * 7), (base[0] - nr[0] * 7, base[1] - nr[1] * 7)]), RED))


def isare(n):
    return "are" if n.endswith("s") and n not in ("platypus",) else "is"


# ------------------------------------------------------------ the maps
TOWN = Map(6, 5, [
    ("school", 0, 0, 2, 1, "b"), ("library", 2, 0, 1, 1, "b"), ("post office", 4, 0, 1, 1, "b"), ("bakery", 5, 0, 1, 1, "b"),
    ("pool", 0, 1, 1, 1, "w"), ("park", 1, 1, 2, 2, "g"), ("chemist", 4, 1, 1, 1, "b"), ("bank", 5, 1, 1, 1, "b"),
    ("fire station", 0, 2, 1, 1, "r"), ("café", 4, 2, 1, 1, "r"), ("bus stop", 5, 2, 1, 1, "o"),
    ("police station", 1, 3, 1, 1, "r"), ("supermarket", 2, 3, 2, 1, "b"), ("hospital", 5, 3, 1, 2, "b"),
    ("train station", 0, 4, 2, 1, "o"), ("cinema", 2, 4, 1, 1, "b"), ("vet", 4, 4, 1, 1, "b"),
], cw=72)
TOWN_LABEL = ("grid map of a town with columns A to F, rows 1 to 5 and a compass: school, library, post office, bakery, pool, park, chemist, "
              "bank, fire station, café, bus stop, police station, supermarket, hospital, train station, cinema and vet")

ZOO = Map(6, 5, [
    ("koalas", 0, 0, 1, 1, "g"), ("emus", 2, 0, 1, 1, "g"), ("aviary", 4, 0, 1, 1, "o"), ("café", 5, 0, 1, 1, "r"),
    ("wombats", 1, 1, 1, 1, "g"), ("kangaroos", 3, 1, 1, 1, "g"),
    ("reptiles", 0, 2, 1, 1, "b"), ("dingoes", 2, 2, 1, 1, "g"), ("seals", 4, 2, 1, 1, "w"), ("penguins", 5, 2, 1, 1, "w"),
    ("toilets", 1, 3, 1, 1, "b"), ("platypus", 3, 3, 1, 1, "w"), ("play area", 5, 3, 1, 1, "o"),
    ("gift shop", 0, 4, 1, 1, "b"), ("entrance", 2, 4, 1, 1, "r"), ("picnic area", 4, 4, 2, 1, "g"),
], cw=80)
ZOO_LABEL = ("grid map of a wildlife park with columns A to F, rows 1 to 5 and an 8-point compass: koalas, emus, aviary, café, wombats, "
             "kangaroos, reptiles, dingoes, seals, penguins, toilets, platypus, play area, gift shop, entrance and picnic area")

PARK = Map(6, 5, [
    ("gate", 0, 0, 1, 1, "r"), ("slide", 2, 0, 1, 1, "o"), ("swings", 3, 0, 1, 1, "o"), ("kiosk", 5, 0, 1, 1, "b"),
    ("BBQ", 1, 1, 1, 1, "r"), ("gum tree", 4, 1, 1, 1, "g"), ("tap", 5, 1, 1, 1, "w"),
    ("pond", 2, 2, 2, 1, "w"),
    ("toilets", 0, 3, 1, 1, "b"), ("sandpit", 4, 3, 1, 1, "o"),
    ("skate park", 0, 4, 1, 1, "o"), ("rotunda", 2, 4, 1, 1, "b"), ("bench", 3, 4, 1, 1, "o"), ("car park", 5, 4, 1, 1, "o"),
])
PARK_LABEL = ("grid map of a park with columns A to F, rows 1 to 5 and an 8-point compass: gate, slide, swings, kiosk, BBQ, gum tree, "
              "tap, pond, toilets, sandpit, skate park, rotunda, bench and car park")

CAMP = Map(6, 5, [
    ("cabins", 0, 0, 2, 1, "b"), ("office", 3, 0, 1, 1, "b"), ("car park", 5, 0, 1, 1, "o"),
    ("dining hall", 2, 1, 2, 1, "b"), ("flying fox", 5, 1, 1, 1, "o"),
    ("campfire", 0, 2, 1, 1, "r"), ("lake", 3, 2, 2, 2, "w"),
    ("archery", 1, 3, 1, 1, "o"), ("oval", 5, 3, 1, 2, "g"),
    ("toilets", 0, 4, 1, 1, "b"), ("canoes", 3, 4, 1, 1, "w"),
], cw=72)
CAMP_LABEL = ("grid map of a school camp with columns A to F, rows 1 to 5 and an 8-point compass: cabins, office, car park, dining hall, "
              "flying fox, campfire, lake, archery, oval, toilets and canoes")

BLANK = Map(6, 5, [], cw=52, ch=40)


# ------------------------------------------------------------ set 1: read and write grid references
def set_refs(rnd, P_):
    M = TOWN
    tm = fig(M.svg(TOWN_LABEL))
    its = []
    # what is in square X?
    for cell in [(2, 0), (4, 1), (0, 2), (5, 2), (1, 3), (4, 4), (3, 3)]:
        ans = M.at(cell)
        assert ans
        cands, notes = [], []
        sw = (cell[1], cell[0])
        if M.inside(sw) and M.at(sw) and M.at(sw) != ans:
            cands.append(M.at(sw))
            notes.append("Reading the number as the column (column %s, row %d) gives the %s." % (COLS[sw[0]], sw[1] + 1, M.at(sw)))
        for d in ("east", "west", "south", "north") + tuple(DIR8):
            x = step(cell, d)
            if M.inside(x) and M.at(x) and M.at(x) != ans and M.at(x) not in cands:
                cands.append(M.at(x))
        for x in sorted(M.cell, key=lambda x: (abs(x[0] - cell[0]) + abs(x[1] - cell[1]), x)):
            if (x[0] == cell[0] or x[1] == cell[1]) and M.at(x) not in cands + [ans]:
                cands.append(M.at(x))
        e = "Go across to column %s first, then down to row %d. Square %s is the %s." % (COLS[cell[0]], cell[1] + 1, ref(cell), ans)
        if notes:
            e += " " + notes[0]
        its.append(mcq(tm + "What is in square <b>%s</b>?" % ref(cell), "the " + ans, ["the " + c for c in cands], e, rnd))
    # what is the grid reference of X?
    for name in ("bakery", "pool", "café", "cinema", "post office", "bank"):
        c = M.single(name)
        good = ref(c)
        sw = (c[1], c[0])
        swapped = ref(sw) if M.inside(sw) and sw != c else None
        side = ref((c[0] - 1, c[1])) if c[0] > 0 else ref((c[0] + 1, c[1]))
        down = ref((c[0], c[1] + 1)) if c[1] + 1 < M.rows else ref((c[0], c[1] - 1))
        wrong = [ref_nf(c)] + ([swapped] if swapped else []) + [side, down]
        e = ("Go across to find the letter, then down to find the number. The %s %s in column %s, row %d: %s. "
             "Always write the letter first, so not %s." % (name, isare(name), COLS[c[0]], c[1] + 1, good, ref_nf(c)))
        its.append(mcq(tm + "What is the grid reference of the <b>%s</b>?" % name, good, wrong, e, rnd))
    # places that cover more than one square
    for name, wrong in [
        ("park", ["2B, 2C, 3B and 3C", "B1, C1, B2 and C2", "A2, B2, A3 and B3"]),
        ("hospital", ["4F and 5F", "D6 and E6", "F3 and F4"]),
        ("school", ["1A and 1B", "A1 and A2", "B1 and C1"]),
    ]:
        cs = sorted(M.where[name], key=lambda c: (c[1], c[0]))
        rs = [ref(c) for c in cs]
        good = ", ".join(rs[:-1]) + " and " + rs[-1]
        assert good not in wrong
        e = "The %s covers %d squares: %s. Letter first, then number, for each square." % (name, len(cs), good)
        its.append(mcq(tm + "The %s covers more than one square. Which squares?" % name, good, wrong, e, rnd))
    assert M.at((0, 4)) == M.at((1, 4)) == "train station"
    its.append(mcq(tm + "Which place covers squares <b>A5 and B5</b>?", "the train station",
                   ["the police station", "the fire station", "the cinema"],
                   "Row 5 is the bottom row. Squares A5 and B5 are the first two squares in it: the train station.", rnd))
    # an empty square
    empty = [c for c in [(3, 1)] if not M.at(c)]
    assert empty == [(3, 1)] and M.at((2, 1)) == "park" and M.at((4, 1)) == "chemist" and M.at((3, 3)) == "supermarket"
    its.append(mcq(tm + "Which square is <b>empty</b>?", "D2", ["C2", "E2", "D4"],
                   "D2 is in column D, row 2. Nothing is drawn there. C2 is part of the park, E2 is the chemist and D4 is part of the supermarket.", rnd))
    # same row
    assert M.single("pool")[1] == 1 and M.single("chemist")[1] == 1
    its.append(mcq(tm + "Which place is in the <b>same row</b> as the pool?", "the chemist", ["the café", "the library", "the fire station"],
                   "The pool is in A2, so it is in row 2. The chemist is in E2, also row 2. The fire station is in A3: same column, not the same row.", rnd))
    # spot the mistake
    n, he, his, him = P_.next()
    assert ref(M.single("police station")) == "B4"
    its.append(mcq(tm + "%s says the police station is in <b>4B</b>. What should %s write?" % (n, he), "B4", ["4B", "D2", "B3"],
                   "%s has the number first. A grid reference gives the letter first (across), then the number (down): B4." % n, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Read and write grid references like B3", "items": its}


# ------------------------------------------------------------ set 2: the eight compass points
def set_compass(rnd, P_):
    M = ZOO
    zm = fig(M.svg(ZOO_LABEL))
    its = []

    def dir_q(b, a):
        A, B = M.single(a), M.single(b)
        d, n = dir_between(A, B)
        if d in ("north", "south", "east", "west"):
            wrong = [opp(d), turn(d, 1), turn(d, -1)]
        else:
            wrong = [flip_ew(d), flip_ns(d), opp(d)]
        dx, dy = B[0] - A[0], B[1] - A[1]
        parts = []
        if dx:
            parts.append("%s %s" % (sq(abs(dx)), "right (east)" if dx > 0 else "left (west)"))
        if dy:
            parts.append("%s %s" % (sq(abs(dy)), "down (south)" if dy > 0 else "up (north)"))
        e = "The %s %s in %s and the %s %s in %s. From the %s, go %s." % (a, isare(a), ref(A), b, isare(b), ref(B), a, " and ".join(parts))
        if dx and dy:
            e += " The same number each way is a diagonal, so the %s %s %s of the %s." % (b, isare(b), d, a)
        else:
            e += " So the %s %s %s of the %s." % (b, isare(b), d, a)
        if d in ("north-east", "north-west", "south-east", "south-west"):
            e += " Check east (right) and west (left) carefully: %s would be the other way." % flip_ew(d)
        its.append(mcq(zm + "The %s %s ___ of the %s." % (b, isare(b), a), d, wrong, e, rnd))

    for b, a in [("kangaroos", "dingoes"), ("reptiles", "emus"), ("toilets", "entrance"), ("play area", "seals"),
                 ("platypus", "kangaroos"), ("café", "aviary"), ("koalas", "reptiles"), ("reptiles", "dingoes")]:
        dir_q(b, a)

    def first(a, d):
        x = step(M.single(a), d)
        while M.inside(x):
            if M.at(x):
                return M.at(x), x
            x = step(x, d)
        return None, None

    def first_q(a, d, extra):
        ans, cell = first(a, d)
        assert ans, (a, d)
        cands, notes = [], []
        for kind, d2 in (("ew", flip_ew(d)), ("opp", opp(d)), ("ns", flip_ns(d))):
            w, wc = first(a, d2)
            if w and w != ans and w not in cands:
                cands.append(w)
                if not notes:
                    notes.append("Going %s by mistake gives the %s." % (d2, w))
        nxt = step(cell, d)
        while M.inside(nxt) and not M.at(nxt):
            nxt = step(nxt, d)
        if M.inside(nxt) and M.at(nxt) not in cands + [ans]:
            cands.append(M.at(nxt))
        cands += extra
        e = ("%s is %s on the map. From the %s (%s), move one square at a time diagonally: the first place is the %s in %s."
             % (d.capitalize(), {"north-east": "up and to the right", "north-west": "up and to the left",
                                 "south-east": "down and to the right", "south-west": "down and to the left"}[d],
                a, ref(M.single(a)), ans, ref(cell)))
        if notes:
            e += " " + notes[0]
        its.append(mcq(zm + "What is the first place you reach going straight <b>%s</b> from the %s?" % (d, a), "the " + ans,
                       ["the " + c for c in cands], e, rnd))

    first_q("dingoes", "north-west", ["kangaroos"])
    first_q("entrance", "north-east", ["kangaroos"])
    first_q("aviary", "south-west", ["café", "seals"])
    # turning
    for face, k, how in [("north", 2, "a quarter turn clockwise"), ("east", 4, "a half turn"), ("south", -2, "a quarter turn anticlockwise"),
                         ("north-east", 2, "a quarter turn clockwise"), ("north-west", 6, "a three-quarter turn clockwise")]:
        n, he, his, him = P_.next()
        ans = turn(face, k)
        wrong = [turn(face, -k), turn(face, k // 2), opp(face) if opp(face) != ans else turn(face, 1), face]
        if k == 4:
            wrong = [turn(face, 2), turn(face, -2), face]
        steps_ = {2: "two compass points clockwise", -2: "two compass points anticlockwise", 4: "four compass points (to the opposite side)",
                  6: "six compass points clockwise (the same as a quarter turn anticlockwise)"}[k]
        e = "Use the compass rose. A quarter turn moves you 2 points, from one main direction to the next. From %s, move %s: %s." % (face, steps_, ans)
        if k in (2, -2, 6):
            e += " Turning the other way would give %s." % turn(face, -k)
        its.append(mcq("%s faces <b>%s</b>. %s makes %s. Which way does %s face now?" % (n, face, he.capitalize(), how, he), ans, wrong, e, rnd))
    # facts
    its.append(mcq("Which direction is halfway between <b>south</b> and <b>west</b>?", "south-west",
                   ["west-south", "south-east", "north-west"],
                   "The in-between directions always start with north or south: south-west (SW), not west-south. South-east is between south and east.", rnd))
    its.append(mcq("What is the opposite direction to <b>north-east</b>?", "south-west", ["north-west", "south-east", "west"],
                   "Opposite means a half turn. Turn north-east halfway round the compass: south-west. Both parts change: north to south and east to west.", rnd))
    its.append(mcq("Going clockwise: N, NE, E, ___, S. Which compass point is missing?", "SE", ["NW", "SW", "ES"],
                   "After east (E), going clockwise towards south (S), the next point is south-east (SE). Write S first: SE, not ES.", rnd))
    its.append(mcq("What is the short way to write <b>north-west</b>?", "NW", ["WN", "NE", "SW"],
                   "Use the first letter of each word, in order: North-West is NW. North or south always comes first.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "The eight compass points: N, NE, E, SE, S, SW, W, NW", "items": its}


# ------------------------------------------------------------ set 3: follow directions
def set_follow(rnd, P_):
    its = []
    G = BLANK

    def grid_q(start, moves):
        n, he, his, him = P_.next()
        ans = walk(start, moves)
        assert G.inside(ans) and ans != start, (start, moves)
        assert all(G.inside(c) for c in cells_on(start, moves)), (start, moves)
        cands, first_tip = [], None
        for kind, m in mistake_moves(moves):
            c = walk(start, m)
            if G.inside(c) and c != ans and c != start and ref(c) not in cands:
                cands.append(ref(c))
                if first_tip is None and kind in TIP:
                    first_tip = TIP[kind] % ref(c)
        cands = cands[:2] + [ref_nf(ans)] + cands[2:]
        e = walk_e(start, moves)
        if first_tip:
            e += " " + first_tip
        svg = G.svg("empty grid with columns A to F, rows 1 to 5, an 8-point compass and a red dot in %s" % ref(start), [(start, "dot", None)])
        its.append(mcq(fig(svg) + "%s starts at the red dot in %s. %s goes <b>%s</b>. Which square does %s finish in?"
                       % (n, ref(start), he.capitalize(), moves_txt(moves), he), ref(ans), cands, e, rnd))

    for start, moves in [((1, 3), [("east", 3)]), ((4, 4), [("north", 3)]), ((5, 1), [("west", 4)]),
                         ((0, 0), [("south-east", 3)]), ((4, 4), [("north-west", 2), ("north", 1)]),
                         ((1, 4), [("north-east", 2), ("east", 2)]), ((5, 0), [("south-west", 2), ("south", 2)]),
                         ((0, 2), [("east", 3), ("north", 2)])]:
        grid_q(start, moves)

    M = PARK
    pm = fig(M.svg(PARK_LABEL))

    def land_q(frm, moves):
        s0 = M.single(frm)
        end = walk(s0, moves)
        ans = M.at(end)
        assert ans and ans != frm, (frm, moves, end)
        assert all(M.inside(c) for c in cells_on(s0, moves))
        cands, first_tip = [], None
        for kind, m in mistake_moves(moves):
            c = walk(s0, m)
            if M.inside(c) and M.at(c) and M.at(c) not in (ans, frm) and M.at(c) not in cands:
                cands.append(M.at(c))
                if first_tip is None and kind in TIP:
                    first_tip = TIP[kind] % ("the " + M.at(c))
        for c in [step(end, d) for d in DIR8]:
            if M.inside(c) and M.at(c) and M.at(c) not in cands + [ans, frm]:
                cands.append(M.at(c))
        for c in sorted(M.cell, key=lambda x: (abs(x[0] - end[0]) + abs(x[1] - end[1]), x)):
            if M.at(c) not in cands + [ans, frm]:
                cands.append(M.at(c))
        e = walk_e(s0, moves) + " The %s %s in %s." % (ans, isare(ans), ref(end))
        if first_tip:
            e += " " + first_tip
        its.append(mcq(pm + "Start at the %s. Go <b>%s</b>. What do you reach?" % (frm, moves_txt(moves)), "the " + ans,
                       ["the " + c for c in cands], e, rnd))

    land_q("gate", [("south-east", 1), ("east", 3)])
    land_q("car park", [("north", 4), ("west", 2)])
    land_q("toilets", [("north-east", 2), ("north", 1)])
    land_q("rotunda", [("north-east", 1), ("east", 1)])
    land_q("kiosk", [("south", 2), ("west", 2)])
    land_q("skate park", [("north-east", 1), ("north", 2)])
    land_q("tap", [("south-west", 2), ("south", 1)])

    # without a map: letters go across, numbers go down
    G8 = Map(8, 8, [])

    def text_q(start, moves, who):
        n, he, his, him = P_.next()
        ans = walk(start, moves)
        assert G8.inside(ans)
        cands = []
        for kind, m in mistake_moves(moves):
            c = walk(start, m)
            if G8.inside(c) and c != ans and c != start and ref(c) not in cands:
                cands.append(ref(c))
        cands = cands[:2] + [ref_nf(ans)] + cands[2:]
        parts, x = [], start
        for d, k in moves:
            y = step(x, d, k)
            ch = []
            if y[0] != x[0]:
                ch.append("the letter from %s to %s" % (COLS[x[0]], COLS[y[0]]))
            if y[1] != x[1]:
                ch.append("the number from %d to %d" % (x[1] + 1, y[1] + 1))
            parts.append("%s %s changes %s" % (sq(k), d, " and ".join(ch)))
            x = y
        e = "Moving east or west changes the letter. Moving north or south changes the number (south adds, north takes away). "
        e += "; ".join(p[0].upper() + p[1:] for p in parts) + ". The answer is %s." % ref(ans)
        if any(d not in ("north", "south", "east", "west") for d, k in moves):
            e += " A diagonal move changes both the letter and the number."
        its.append(mcq("On a grid map, letters go across (A, B, C and so on) and numbers go down (1, 2, 3 and so on). "
                       "%s %s starts at <b>%s</b> and moves <b>%s</b>. Where is it now?" % (who, "", ref(start), moves_txt(moves)),
                       ref(ans), cands, e, rnd))

    text_q((1, 1), [("east", 3), ("south", 2)], "A toy robot")
    text_q((5, 5), [("west", 2), ("north", 3)], "A toy robot")
    text_q((2, 0), [("south-east", 3)], "A toy robot")
    text_q((6, 6), [("north-west", 2)], "A toy robot")
    text_q((3, 4), [("east", 1), ("north", 4)], "A toy robot")
    for it in its:
        it["q"] = it["q"].replace("robot  starts", "robot starts")
    assert len(its) == 20, len(its)
    return {"title": "Follow directions on a grid map", "items": its}


# ------------------------------------------------------------ set 4: give directions and describe pathways
def legs_of(start, corners):
    """Turn a list of corner cells into moves."""
    out, a = [], start
    for b in corners:
        d, n = dir_between(a, b)
        out.append((d, n))
        a = b
    return out


def bfs(M, a, b, ok):
    A, B = M.single(a), M.single(b)
    q, seen = deque([(A, 0)]), {A}
    while q:
        x, d = q.popleft()
        for dd in ("north", "south", "east", "west"):
            y = step(x, dd)
            if y == B:
                return d + 1
            if M.inside(y) and y not in seen and ok(y):
                seen.add(y)
                q.append((y, d + 1))
    return None


def set_pathways(rnd, P_):
    M = PARK
    pm = fig(M.svg(PARK_LABEL))
    its = []

    def route_q(a, b):
        A, B = M.single(a), M.single(b)
        dx, dy = B[0] - A[0], B[1] - A[1]
        mv = [("east" if dx > 0 else "west", abs(dx)), ("north" if dy < 0 else "south", abs(dy))]
        assert walk(A, mv) == B and dx and dy
        wrong = [[(flip_ew(mv[0][0]), mv[0][1]), mv[1]], [mv[0], (flip_ns(mv[1][0]), mv[1][1])], [(mv[0][0], mv[0][1] + 1), (mv[1][0], mv[1][1] + 1)]]
        if mv[0][1] != mv[1][1]:
            wrong.insert(2, [(mv[0][0], mv[1][1]), (mv[1][0], mv[0][1])])
        for w in wrong:
            assert walk(A, w) != B
        its.append(mcq(pm + "Which directions take you from the %s to the %s?" % (a, b), moves_short(mv),
                       [moves_short(w) for w in wrong],
                       "The %s %s in %s and the %s %s in %s. %s to %s is %s %s. Row %d to row %d is %s %s. "
                       "Count the squares you move, not the square you start on." % (
                           a, isare(a), ref(A), b, isare(b), ref(B), COLS[A[0]], COLS[B[0]], sq(abs(dx)), mv[0][0], A[1] + 1, B[1] + 1, sq(abs(dy)), mv[1][0]), rnd))

    route_q("gate", "sandpit")
    route_q("slide", "toilets")
    route_q("car park", "BBQ")
    route_q("rotunda", "kiosk")
    route_q("tap", "skate park")

    def diag_q(a, b):
        A, B = M.single(a), M.single(b)
        d, n = dir_between(A, B)
        assert d not in ("north", "south", "east", "west")
        good = "%s %s" % (sq(n), d)
        wrong = ["%s %s" % (sq(n), flip_ns(d)), "%s %s" % (sq(n), flip_ew(d)), "%s %s" % (sq(n + 1), d)]
        for w in ([(flip_ns(d), n)], [(flip_ew(d), n)], [(d, n + 1)]):
            assert walk(A, w) != B
        its.append(mcq(pm + "Which <b>one straight line</b> takes you from the %s to the %s?" % (a, b), good, wrong,
                       "The %s %s in %s and the %s %s in %s. That is %s %s and %s %s: the same number each way, so it is a diagonal. Go %s."
                       % (a, isare(a), ref(A), b, isare(b), ref(B), sq(abs(B[0] - A[0])), "east" if B[0] > A[0] else "west",
                          sq(abs(B[1] - A[1])), "south" if B[1] > A[1] else "north", good), rnd))

    diag_q("tap", "rotunda")
    diag_q("toilets", "swings")
    diag_q("car park", "sandpit")

    def drawn_q(a, corners, b):
        A = M.single(a)
        cs = [A] + corners
        assert M.at(cs[-1]) == b
        mv = legs_of(A, corners)
        on = cells_on(A, mv)
        assert all(M.at(c) is None for c in on[:-1]), (a, b, [ref(c) for c in on if M.at(c)])
        svg = M.svg("%s with a dashed red path from the %s to the %s" % (PARK_LABEL.replace("grid map", "grid map"), a, b), path=cs)
        good = moves_short(mv)
        wrong = [[(flip_ew(d) if VEC[d][0] else d, n) for d, n in mv], [(flip_ns(d) if VEC[d][1] else d, n) for d, n in mv],
                 [(d, n + 1) for d, n in mv]]
        if len(mv) == 2 and mv[0][1] != mv[1][1]:
            wrong.insert(2, [(mv[0][0], mv[1][1]), (mv[1][0], mv[0][1])])
        for i in range(len(mv)):
            wrong.append([(d, n + 1 if j == i else n) for j, (d, n) in enumerate(mv)])
        wrong.append(mv[:-1])
        wtxt = []
        for w in wrong:
            if moves_short(w) != good and walk(A, w) != cs[-1]:
                wtxt.append(moves_short(w))
        e = walk_e(A, mv) + " That is the %s." % b
        its.append(mcq(fig(svg) + "Which directions describe the dashed path from the <b>%s</b> to the <b>%s</b>?" % (a, b), good, wtxt, e, rnd))
        return mv, svg

    drawn_q("BBQ", [(3, 1), (3, 0)], "swings")
    mv_gate, svg_gate = drawn_q("gate", [(0, 2), (1, 2), (1, 4), (2, 4)], "rotunda")
    drawn_q("rotunda", [(2, 3), (4, 3)], "sandpit")
    drawn_q("car park", [(5, 2), (4, 2), (4, 1)], "gum tree")
    drawn_q("skate park", [(1, 4), (1, 3), (3, 3), (3, 4)], "bench")
    total = sum(n for d, n in mv_gate)
    assert total == 6
    its.append(mcq_num(fig(svg_gate) + "How many squares long is the dashed path from the gate to the rotunda?", total,
                       [total + 1, len(mv_gate), total - 1],
                       "Add the squares of each part: %s = %d squares. Count the moves, not the gate square you start on."
                       % (" + ".join(str(n) for d, n in mv_gate), total)))

    # fewest squares, only through empty squares
    for who, a, b in [(P_.next(), "gate", "rotunda"), (P_.next(), "bench", "BBQ")]:
        n, he, his, him = who
        d = bfs(M, a, b, lambda c: M.at(c) is None)
        A, B = M.single(a), M.single(b)
        man = abs(A[0] - B[0]) + abs(A[1] - B[1])
        assert d == man, (a, b, d, man)
        its.append(mcq_num(pm + "%s walks from the %s to the %s. %s moves only north, south, east or west, and only through empty squares. "
                           "What is the fewest number of squares %s can move?" % (n, a, b, he.capitalize(), he), d,
                           [d + 1, max(abs(A[0] - B[0]), abs(A[1] - B[1])), d - 1],
                           "The %s is in %s and the %s is in %s: %s across and %s up or down. %d + %d = %d squares, and there is a way round "
                           "through empty squares that is this short. Do not count the starting square."
                           % (a, ref(A), b, ref(B), sq(abs(A[0] - B[0])), sq(abs(A[1] - B[1])), abs(A[0] - B[0]), abs(A[1] - B[1]), d)))

    # keep out of the pond
    pond = set(M.where["pond"])
    for a, b, good, wrongs in [
        ("BBQ", "sandpit", [("south", 2), ("east", 3)], [[("south", 1), ("east", 3), ("south", 1)], [("south", 2), ("west", 3)], [("south", 3), ("east", 3)]]),
        ("swings", "bench", [("east", 1), ("south", 4), ("west", 1)], [[("south", 4)], [("west", 1), ("south", 4), ("east", 1)], [("east", 1), ("south", 3), ("west", 1)]]),
    ]:
        A, B = M.single(a), M.single(b)

        def ok(m):
            return walk(A, m) == B and not (set(cells_on(A, m)) & pond) and all(M.inside(c) for c in cells_on(A, m))
        assert ok(good) and not any(ok(w) for w in wrongs)
        notes = []
        for w in wrongs:
            if walk(A, w) == B:
                notes.append("“%s” walks through the pond." % moves_short(w))
        its.append(mcq(pm + "Which directions take you from the %s to the %s <b>without</b> walking through the pond?" % (a, b),
                       moves_short(good), [moves_short(w) for w in wrongs],
                       walk_e(A, good) + " That is the %s, and the path never enters the pond (C3 and D3). " % b + " ".join(notes), rnd))

    # the way back
    for who, a, corners, b in [(P_.next(), "rotunda", [(2, 3), (4, 3)], "sandpit"), (P_.next(), "car park", [(5, 2), (4, 2), (4, 1)], "gum tree")]:
        n, he, his, him = who
        A = M.single(a)
        mv = legs_of(A, corners)
        back = [(opp(d), k) for d, k in reversed(mv)]
        assert walk(walk(A, mv), back) == A
        wrong = [[(opp(d), k) for d, k in mv], mv, [(d, k) for d, k in reversed(mv)]]
        wrong2 = [w for w in wrong if moves_short(w) != moves_short(back)]
        if len(wrong2) < 3:
            wrong2.append([(opp(back[0][0]), back[0][1])] + back[1:])
        its.append(mcq(pm + "%s walks from the %s: <b>%s</b>. %s reaches the %s. Which directions take %s back the same way?"
                       % (n, a, moves_short(mv), he.capitalize(), b, him), moves_short(back), [moves_short(w) for w in wrong2],
                       "To go back the same way, do the moves in reverse order and turn each direction to its opposite: %s." % moves_short(back), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Give directions and describe pathways", "items": its}


# ------------------------------------------------------------ set 5: real-life problems
def set_real(rnd, P_):
    M = CAMP
    cm = fig(M.svg(CAMP_LABEL))
    key = "Year 4 is on school camp. "
    its = []
    ff = M.single("flying fox")
    assert ref(ff) == "F2"
    its.append(mcq(cm + key + "What is the grid reference of the flying fox?", "F2", ["2F", "E2", "F3"],
                   "Go across to column F, then down to row 2: F2. Letter first, then number.", rnd))
    assert M.at((1, 3)) == "archery" and M.at((3, 1)) == "dining hall"
    its.append(mcq(cm + key + "What is in square <b>B4</b>?", "the archery", ["the dining hall", "the campfire", "the toilets"],
                   "Column B, row 4 is the archery. Reading the number as the column (column D, row 2) gives the dining hall.", rnd))
    lk = sorted(M.where["lake"], key=lambda c: (c[1], c[0]))
    assert [ref(c) for c in lk] == ["D3", "E3", "D4", "E4"]
    its.append(mcq(cm + key + "Which squares does the lake cover?", "D3, E3, D4 and E4",
                   ["3D, 3E, 4D and 4E", "C3, D3, C4 and D4", "D2, E2, D3 and E3"],
                   "The lake is in columns D and E, rows 3 and 4: D3, E3, D4 and E4.", rnd))
    s0 = M.single("campfire")
    mv = [("north-east", 1), ("east", 1)]
    assert M.at(walk(s0, mv)) == "dining hall"
    assert M.at(walk(s0, [("north-west", 1)])) is None
    its.append(mcq(cm + key + "From the campfire, the class walks <b>1 square north-east, then 1 square east</b>. Where are they?", "at the dining hall",
                   ["at the cabins", "at the archery", "at the office"],
                   walk_e(s0, mv) + " C2 is part of the dining hall.", rnd))
    A, B = M.single("toilets"), M.single("office")
    mv = [("east", 3), ("north", 4)]
    assert walk(A, mv) == B
    its.append(mcq(cm + key + "Which directions take you from the toilets to the office?", "3 east, 4 north",
                   ["3 west, 4 north", "3 east, 4 south", "4 east, 3 north"],
                   "The toilets are in A5 and the office is in D1. A to D is 3 squares east. Row 5 to row 1 is 4 squares north.", rnd))
    d, n = dir_between(M.single("campfire"), M.single("archery"))
    assert (d, n) == ("south-east", 1)
    its.append(mcq(cm + key + "The archery is ___ of the campfire.", "south-east", ["north-east", "south-west", "north-west"],
                   "The campfire is in A3 and the archery is in B4: 1 square right (east) and 1 square down (south). That is south-east.", rnd))
    assert dir_between(M.single("campfire"), M.single("toilets")) == ("south", 2)
    its.append(mcq_num(cm + key + "Each square on the map is 50 metres. How far is it from the campfire straight south to the toilets?", 100,
                       [150, 50, 200],
                       "From A3 to A5 is 2 squares. 2 × 50 = 100 metres. Counting the campfire square too gives 3 squares, or 150 metres.", " m"))
    A, B = M.single("archery"), M.single("flying fox")
    mv = [("east", 4), ("north", 2)]
    assert walk(A, mv) == B
    its.append(mcq_num(cm + key + "Each square is 50 metres. Jack walks from the archery 4 squares east, then 2 squares north to the flying fox. How far does he walk?",
                       300, [400, 200, 100],
                       "He walks 4 + 2 = 6 squares. 6 × 50 = 300 metres. Only counting the east part gives 4 × 50 = 200 metres.", " m"))
    n, he, his, him = P_.next()
    s0 = M.single("toilets")
    assert M.at(walk(s0, [("east", 3)])) == "canoes" and M.at(walk(s0, [("north", 2)])) == "campfire"
    its.append(mcq(cm + key + "%s is at the toilets, facing north. %s makes a quarter turn clockwise, then walks 3 squares. What does %s reach?"
                   % (n, he.capitalize(), he), "the canoes", ["the campfire", "the archery", "the lake"],
                   "Facing north, a quarter turn clockwise makes %s face east. 3 squares east of A5 is D5: the canoes." % him, rnd))
    s0 = M.single("archery")
    x = step(s0, "north-east")
    while not M.at(x):
        x = step(x, "north-east")
    assert M.at(x) == "dining hall" and M.at(step(s0, "north-west")) == "campfire" and M.at(step(s0, "south-west")) == "toilets"
    its.append(mcq(cm + key + "What is the first place you reach going straight north-east from the archery?", "the dining hall",
                   ["the campfire", "the toilets", "the office"],
                   "North-east is up and to the right. From B4: C3 is empty, then D2 is the dining hall. North-west would give the campfire.", rnd))
    x = step(ff, "south-west")
    assert M.at(x) == "lake"
    its.append(mcq(cm + key + "What is <b>1 square south-west</b> of the flying fox?", "the lake", ["the oval", "the car park", "the dining hall"],
                   "South-west is down and to the left. From F2, one square down and one square left is E3, part of the lake.", rnd))
    # without a map
    n, he, his, him = P_.next()
    its.append(mcq("%s’s tent is at <b>C4</b> on the campsite map. The toilets are 3 squares east of %s tent. What is the grid reference of the toilets?"
                   % (n, his), "F4", ["E4", "C7", "4F"],
                   "East is across, so the letter changes and the number stays the same. C, then D (1), E (2), F (3): F4. "
                   "Counting C as 1 gives E4.", rnd))
    its.append(mcq("On a street map, the letters go across and the numbers go down. The beach is in <b>B2</b> and the surf club is in <b>B5</b>. "
                   "Which direction is the surf club from the beach?", "south", ["north", "east", "west"],
                   "Both are in column B, so the direction is straight up or down. The number goes from 2 to 5, which is down the map: south.", rnd))
    its.append(mcq("A treasure hunt clue says: “Start at A1. Go 4 squares east, then 3 squares south.” Letters go across and numbers go down. "
                   "Where is the treasure?", "E4", ["D3", "D4", "4E"],
                   "4 squares east changes A to E. 3 squares south changes 1 to 4. The treasure is in E4. Counting the starting square gives D3.", rnd))
    assert walk((0, 0), [("east", 4), ("south", 3)]) == (4, 3)
    n, he, his, him = P_.next()
    its.append(mcq("%s writes the grid reference of the canteen on a school map as <b>3E</b>. What should %s write?" % (n, he), "E3",
                   ["3E", "C5", "D3"],
                   "Write the letter first and then the number. 3E has them the wrong way round; E3 is right. C5 swaps the letter and number positions.", rnd))
    n, he, his, him = P_.next()
    end = walk((0, 0), [("north", 2), ("east", 2)])
    assert dir_between(end, (0, 0)) == ("south-west", 2)
    its.append(mcq("On the oval, %s walks 2 squares north, then 2 squares east. Which <b>one</b> direction takes %s straight back to where %s started?"
                   % (n, him, he), "south-west", ["north-east", "south-east", "north-west"],
                   "%s went north and east, so to come back %s goes the opposite way: south and west. 2 each way is a diagonal: south-west." % (n, he), rnd))
    n, he, his, him = P_.next()
    end = walk((0, 0), [("north-east", 3), ("south-east", 3)])
    assert end == (6, 0)
    its.append(mcq("On a bushwalk map, %s walks 3 squares north-east, then 3 squares south-east. Where is %s now, compared with the start?"
                   % (n, he), "6 squares east", ["6 squares north", "3 squares east", "6 squares west"],
                   "North-east goes up 3 and right 3. South-east goes down 3 and right 3. The ups and downs cancel out, and %s went 3 + 3 = 6 squares right: east." % he, rnd))
    its.append(mcq("On a bushwalk map, the lookout is 3 squares north-west of the car park. Which direction is the car park from the lookout?",
                   "south-east", ["north-west", "south-west", "north-east"],
                   "To go back, turn to the opposite direction. The opposite of north-west is south-east.", rnd))
    its.append(mcq_num("Each square on a map of the town is 100 metres. The pool is 4 squares west of the school, in the same row. How far is the pool from the school?",
                       400, [500, 300, 100],
                       "4 squares × 100 metres = 400 metres. Counting the school square as well gives 5 squares, or 500 metres.", " m"))
    its.append(mcq_num("On a map of a farm, the dam is in <b>C2</b> and the shed is in <b>F2</b>. How many squares east is it from the dam to the shed?",
                       3, [4, 2, 6],
                       "Count the moves from C: D (1), E (2), F (3). That is 3 squares east. Counting C as well gives 4."))
    assert len(its) == 20, len(its)
    return {"title": "Real-life map problems: camps, streets and bushwalks", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def rose_svg():
    return svg_wrap(120, 110, compass8(60, 56), "an 8-point compass rose: N, NE, E, SE, S, SW, W, NW")


def body_html():
    town = TOWN.svg("town map with square E3 highlighted: the café", hi=(4, 2))
    route = BLANK.svg("empty grid with a dashed path from a red dot in A5, 2 squares north-east to C3, then 3 squares east to a flag in F3",
                      marks=[((0, 4), "dot", None), ((5, 2), "flag", None)], path=[(0, 4), (2, 2), (5, 2)])
    path = PARK.svg("park map with a dashed path from the rotunda 1 square north, then 2 squares east to the sandpit",
                    path=[(2, 4), (2, 3), (4, 3)])
    assert walk((0, 4), [("north-east", 2), ("east", 3)]) == (5, 2)
    assert TOWN.at((4, 2)) == "café"
    return (
        "<h2>Grid references</h2>"
        "<p>A grid map has letters across the top and numbers down the side. "
        "A <b>grid reference</b> such as <b>E3</b> names one square. Go across to the letter first, then down to the number.</p>"
        "<figure class='sn-fig'>" + town +
        "<figcaption>Square E3 is highlighted: column E, row 3. It is the café.</figcaption></figure>" +
        ex("Example", "What is the grid reference of the bakery?",
           "Go across to column F, then down to row 1. Write the letter first.", "F1") +
        "<p>Some maps number the rows from the bottom up. Always check where row 1 is.</p>"
        "<h2>The eight compass points</h2>"
        "<p>North is usually at the top of a map. The four main points, going clockwise, are north, east, south and west "
        "(“Never Eat Soggy Weet-Bix”). Halfway between them are <b>north-east</b>, <b>south-east</b>, <b>south-west</b> and <b>north-west</b>. "
        "North or south always comes first: NE, not EN.</p>"
        "<figure class='sn-fig'>" + rose_svg() +
        "<figcaption>An 8-point compass. North-east is halfway between north and east.</figcaption></figure>" +
        table(["On the map", "Direction"], [["up", "north (N)"], ["up and right", "north-east (NE)"], ["right", "east (E)"],
                                            ["down and right", "south-east (SE)"], ["down", "south (S)"], ["down and left", "south-west (SW)"],
                                            ["left", "west (W)"], ["up and left", "north-west (NW)"]]) +
        "<p>A quarter turn moves 2 points round the compass. A half turn takes you to the opposite direction.</p>"
        "<h2>Follow and give directions</h2>"
        "<p>Give the direction and the number of squares (or steps). Count the squares you <b>move</b>, not the square you start on. "
        "One square north-east means one square up and one square right, across the corner.</p>"
        "<figure class='sn-fig'>" + route +
        "<figcaption>Start at the red dot in A5. Go 2 squares north-east to C3, then 3 squares east to the flag in F3.</figcaption></figure>" +
        ex("Example", "On the park map, describe the dashed path from the rotunda to the sandpit.",
           "The rotunda is in C5. Go 1 square north to C4, then 2 squares east to E4.", "1 north, 2 east") +
        "<figure class='sn-fig'>" + path +
        "<figcaption>The path from the rotunda (C5) goes 1 square north, then 2 squares east to the sandpit (E4).</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Writing the number first (3B)", "Letter first, across; then the number: B3"],
            ["Mixing up east and west", "East is on the right of the map, west on the left"],
            ["Naming in-between points the wrong way (east-north)", "North or south comes first: north-east"],
            ["Turning the wrong way", "Clockwise goes the same way as the hands of a clock: N, NE, E, SE and so on"],
            ["Counting the starting square", "Count the moves, not the square you stand on"],
        ])
    )


FAQ = [
    {"q": "What do Year 4 students learn about grid references in the Australian Curriculum?",
     "a": "In Year 4 (AC9M4SP02) students create and read grid reference systems. They use grid references like B3 and directions such as north-east with a number of squares to find places and describe pathways."},
    {"q": "How do you read a grid reference like B3?",
     "a": "Go across to column B first, then down (or up) to row 3. The letter always comes first."},
    {"q": "What are the 8 compass points?",
     "a": "North, north-east, east, south-east, south, south-west, west and north-west, going clockwise. The in-between points always start with north or south."},
    {"q": "Do Year 4 students sit NAPLAN?",
     "a": "No. NAPLAN is for Years 3, 5, 7 and 9. Map and grid reference skills from Year 4 help students prepare for the Year 5 NAPLAN numeracy test."},
]


def balance(sets, rnd):
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
    rnd = random.Random(4816)
    P_ = People(rnd)
    sets = [set_refs(rnd, P_), set_compass(rnd, P_), set_follow(rnd, P_), set_pathways(rnd, P_), set_real(rnd, P_)]
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
        "country": "au", "subject": "maths", "grade": "year-4", "slug": "grid-references-and-maps", "sort": 16,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grid References and Maps: Compass Points, Directions and Pathways",
        "seo_title": "Year 4 Grid References and Maps Worksheets: 8 Compass Points and Directions (Free)",
        "short_title": "Grid references and maps",
        "domain": "Space",
        "standard_code": "AC9M4SP02",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Create and interpret grid reference systems using grid references and directions to locate and describe positions and pathways",
        "meta_desc": "Free Year 4 maths worksheets on grid references and maps: read and write grid references like B3, use the 8 compass points, "
                     "follow directions and describe pathways on grid maps. 100 questions with an answer key, aligned to the Australian Curriculum.",
        "key_big": "A grid reference gives the letter (across) first, then the number: B3.",
        "key_sub": "Give directions as a compass point and a number of squares. Count the squares you move, not the square you start on. "
                   "North-east is halfway between north and east.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "(grid map|empty grid)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
