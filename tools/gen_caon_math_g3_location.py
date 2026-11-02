# -*- coding: utf-8 -*-
"""
CA Grade 3 Math: Location and movement (Ontario Mathematics Curriculum 2020, E1.4)
  python3 tools/gen_ca_math_g3_location.py
HTML attributes use single quotes (no backslashes in the JSON).

Grade 3 students create and interpret simple maps of familiar places (a park, the school, the
neighbourhood), use grid references (letter across, number down: B3), describe where things are
(next to, between, above, below, left of, right of), and give and follow multi-step instructions
with distances (squares) and quarter and half turns, clockwise and counterclockwise.
Every map is a model in code (cells of a grid) and every answer is worked out from that model.
Wrong answers come from real mistakes: column and row swapped (B3 read as C2, written 3B),
left and right mixed up, up and down mixed up, counting the starting square, turning the wrong way
(counterclockwise instead of clockwise), a half turn done as a quarter turn, forgetting a turn,
and left and right taken from the page for a person who faces the bottom of the map.
Canadian English; no compass points (Grade 3 Ontario uses left, right, up, down and turns).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
INK = "#2b2b2b"
GRID = "#b9b3a9"
YELLOW = "#ffe08a"
RED = "#e06666"
BLUE = "#9fc5e8"
BROWN = "#a0692a"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]
COLS = "ABCDEFGH"

VEC = {"up": (0, -1), "right": (1, 0), "down": (0, 1), "left": (-1, 0)}
OPP = {"up": "down", "down": "up", "left": "right", "right": "left"}
HEAD = ["up", "right", "down", "left"]          # clockwise order; heading index 0..3
FACE_TXT = ["up the map", "to the right", "down the map", "to the left"]


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
    return len(str(t)) * fs * (0.62 if bold else 0.56)


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


def shorten(a, b, d):
    L = math.hypot(b[0] - a[0], b[1] - a[1])
    return (b[0] - (b[0] - a[0]) * d / L, b[1] - (b[1] - a[1]) * d / L)


def arrowhead(a, b, back, col, L=12, W=7):
    D = math.hypot(b[0] - a[0], b[1] - a[1])
    u = ((b[0] - a[0]) / D, (b[1] - a[1]) / D)
    tip = (b[0] - u[0] * back, b[1] - u[1] * back)
    base = (tip[0] - u[0] * L, tip[1] - u[1] * L)
    nr = (-u[1], u[0])
    return "<polygon points='%s' fill='%s'/>" % (P([tip, (base[0] + nr[0] * W, base[1] + nr[1] * W), (base[0] - nr[0] * W, base[1] - nr[1] * W)]), col)


def robot(cx, cy, h):
    """A robot seen from above: yellow disc with a green arrow showing the way it faces."""
    u = VEC[HEAD[h]]
    nr = (-u[1], u[0])
    tip = (cx + u[0] * 12, cy + u[1] * 12)
    b = (cx - u[0] * 7, cy - u[1] * 7)
    return ("<circle cx='%.1f' cy='%.1f' r='15' fill='%s' stroke='#b38f00' stroke-width='2'/>" % (cx, cy, YELLOW) +
            "<polygon points='%s' fill='%s'/>" % (P([tip, (b[0] + nr[0] * 9, b[1] + nr[1] * 9), (b[0] - nr[0] * 9, b[1] - nr[1] * 9)]), GREEN))


# ------------------------------------------------------------ grid maps
class Map:
    """A grid map. Columns A, B, C ... go across. Rows 1, 2, 3 ... go down.
    items: (name, col, row, w, h, kind). kind: b building, g grass, w water or ice, o other, r red."""
    FILLS = {"b": ("#f3e3c3", BROWN), "g": (FILL, GREEN), "w": (BLUE, "#3d6f99"), "o": ("#fff1a8", "#b38f00"),
             "r": ("#f8d7d7", "#a33")}

    def __init__(self, cols, rows, items, cw=80, ch=46, refs=True, fs=14):
        self.cols, self.rows, self.cw, self.ch = cols, rows, cw, ch
        self.refs, self.fs = refs, fs
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
            ls = self.lines(name, w)
            assert len(ls) * 15 <= h * ch - 8, ("label too tall", name)
            for ln in ls:
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
        return self.ox + self.cols * self.cw + 4, self.oy + self.rows * self.ch + 4

    def svg(self, label, marks=(), path=None, hi=None):
        """marks: (cell, kind, arg) kind 'letter' (arg = A-D), 'dot' (start), 'robot' (arg = heading).
        path: list of corner cells, drawn as a dashed route with an arrow. hi: cell to highlight."""
        cw, ch, ox, oy = self.cw, self.ch, self.ox, self.oy
        s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff'/>" % (ox, oy, self.cols * cw, self.rows * ch)]
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
            fl, stc = self.FILLS[kind]
            x, y = ox + c * cw + 3, oy + r * ch + 3
            s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='5' fill='%s' stroke='%s' stroke-width='1.6'/>"
                     % (x, y, w * cw - 6, h * ch - 6, fl, stc))
            ls = self.lines(name, w)
            cx, cy = ox + (c + w / 2.0) * cw, oy + (r + h / 2.0) * ch
            for k, ln in enumerate(ls):
                yy = cy + 5 + (k - (len(ls) - 1) / 2.0) * 15
                s.append(text(cx, yy, ln, self.fs, bold=False))
        if hi:
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='4'/>" % (ox + hi[0] * cw, oy + hi[1] * ch, cw, ch, RED))
        if path:
            pts = [self.centre(c) for c in path]
            s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='3' stroke-dasharray='6 4' stroke-linecap='round'/>"
                     % (P(pts[:-1] + [shorten(pts[-2], pts[-1], 12)]), RED))
            s.append(arrowhead(pts[-2], pts[-1], 2, RED))
        for cell, kind, arg in marks:
            assert self.inside(cell), cell
            cx, cy = self.centre(cell)
            if kind == "letter":
                assert cell not in self.cell, ("letter on a place", cell)
                s.append("<circle cx='%.1f' cy='%.1f' r='13' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (cx, cy, GREEN))
                s.append(text(cx, cy + 6, arg, 17))
            elif kind == "dot":
                assert cell not in self.cell, ("dot on a place", cell)
                s.append("<circle cx='%.1f' cy='%.1f' r='11' fill='%s' stroke='#7a1f1f' stroke-width='2'/>" % (cx, cy, RED))
            elif kind == "robot":
                assert cell not in self.cell, ("robot on a place", cell)
                s.append(robot(cx, cy, arg))
        W, H = self.size()
        return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ map facts (computed)
def neighbours(M, name):
    out = []
    for c in M.where[name]:
        for d in HEAD:
            n = M.at(step(c, d))
            if n and n != name and n not in out:
                out.append(n)
    return out


def between_all(M, a, b):
    """Places that lie between a and b on a straight line of squares (row or column), filling the gap."""
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
    """b is ___ a on the map (sharing a row or a column): right of, left of, below, above."""
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


def walk_e(start, moves):
    x = start
    parts = []
    for d, n in moves:
        x = step(x, d, n)
        parts.append("%s %s to %s" % (sq(n), d, ref(x)))
    return "Start at %s. Go %s." % (ref(start), ", then ".join(parts))


def mistake_moves(moves):
    """Moves a student makes by mistake (in order of how common they are)."""
    out = []
    flip = lambda m, axis: [(OPP[d] if d in axis else d, n) for d, n in m]
    if any(d in ("left", "right") for d, n in moves):
        out.append(("lr", flip(moves, ("left", "right"))))
    if any(d in ("up", "down") for d, n in moves):
        out.append(("ud", flip(moves, ("up", "down"))))
    out.append(("start", [(d, n - 1) for d, n in moves]))
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
        for d2 in HEAD:
            if d2 not in (d, OPP[d]):
                out.append(("axis", [(d2, n)]))
    return out


# ------------------------------------------------------------ robot moves with turns
# ops: ("F", n) move n squares forward; ("T", 1, True) quarter turn clockwise;
# ("T", 1, False) quarter turn counterclockwise; ("T", 2, True) half turn.
def run(start, h, ops):
    """Corners of the path and the final heading. None if the robot leaves a 6 x 5 grid."""
    x, pts = start, [start]
    for op in ops:
        if op[0] == "F":
            x = step(x, HEAD[h], op[1])
            if not (0 <= x[0] < 6 and 0 <= x[1] < 5):
                return None, None
            if op[1]:
                pts.append(x)
        else:
            h = (h + (op[1] if op[2] else -op[1])) % 4
    return pts, h


def op_txt(op):
    if op[0] == "F":
        return "move %s forward" % sq(op[1])
    if op[1] == 2:
        return "make a half turn"
    return "make a quarter turn %s" % ("clockwise" if op[2] else "counterclockwise")


def ops_txt(ops):
    t = [op_txt(o) for o in ops]
    return ", ".join(t[:-1]) + ", then " + t[-1]


def ops_short(ops):
    t = []
    for o in ops:
        if o[0] == "F":
            t.append("forward %d" % o[1])
        elif o[1] == 2:
            t.append("half turn")
        else:
            t.append("quarter turn %s" % ("clockwise" if o[2] else "counterclockwise"))
    s = ", ".join(t)
    return s[0].upper() + s[1:]


def ops_e(start, h, ops):
    x = start
    parts = ["Start at %s, facing %s." % (ref(start), FACE_TXT[h])]
    for o in ops:
        if o[0] == "F":
            x = step(x, HEAD[h], o[1])
            parts.append("Move %s forward to %s." % (sq(o[1]), ref(x)))
        else:
            h = (h + (o[1] if o[2] else -o[1])) % 4
            if o[1] == 2:
                parts.append("A half turn makes the robot face the opposite way: %s." % FACE_TXT[h])
            else:
                parts.append("A quarter turn %s makes it face %s." % ("clockwise" if o[2] else "counterclockwise", FACE_TXT[h]))
    return " ".join(parts)


def mistake_ops(ops):
    out = []
    if any(o[0] == "T" and o[1] == 1 for o in ops):
        out.append(("wrongway", [("T", 1, not o[2]) if o[0] == "T" and o[1] == 1 else o for o in ops]))
    if any(o[0] == "T" and o[1] == 2 for o in ops):
        out.append(("halfq", [("T", 1, True) if o[0] == "T" and o[1] == 2 else o for o in ops]))
        out.append(("halfq", [("T", 1, False) if o[0] == "T" and o[1] == 2 else o for o in ops]))
    out.append(("start", [("F", o[1] - 1) if o[0] == "F" else o for o in ops]))
    out.append(("noturn", [o for o in ops if o[0] == "F"]))
    fi = [i for i, o in enumerate(ops) if o[0] == "F"]
    for i in fi:
        out.append(("plus", [("F", o[1] + 1) if j == i else o for j, o in enumerate(ops)]))
    for i in fi:
        if ops[i][1] > 1:
            out.append(("minus", [("F", o[1] - 1) if j == i else o for j, o in enumerate(ops)]))
    return out


TIP = {"wrongway": " Turning the wrong way (%s) takes the robot to %s.",
       "halfq": " Making only a quarter turn instead of a half turn takes it to %s.",
       "start": " Counting the starting square as 1 stops the robot short, on %s.",
       "noturn": " Forgetting to turn takes it to %s.",
       "plus": " Moving one square too far gives %s.", "minus": " Moving one square too few gives %s."}


# ------------------------------------------------------------ the maps
PARK = Map(6, 5, [
    ("washrooms", 0, 0, 1, 1, "b"), ("swings", 2, 0, 1, 1, "o"), ("slide", 3, 0, 1, 1, "o"), ("parking lot", 4, 0, 2, 1, "o"),
    ("pond", 0, 1, 1, 1, "w"), ("bench", 2, 1, 1, 1, "o"), ("splash pad", 4, 1, 1, 1, "w"),
    ("garden", 0, 2, 1, 1, "g"), ("picnic tables", 1, 2, 1, 1, "o"), ("soccer field", 3, 2, 2, 2, "g"), ("fountain", 5, 2, 1, 1, "w"),
    ("sandbox", 1, 3, 1, 1, "o"),
    ("gate", 0, 4, 1, 1, "r"), ("baseball diamond", 1, 4, 2, 1, "g"), ("tree", 3, 4, 1, 1, "g"), ("bike rack", 5, 4, 1, 1, "o"),
], cw=88)
PARK_LABEL = ("grid map of a park with washrooms, swings, a slide, a parking lot, a pond, a bench, a splash pad, a garden, "
              "picnic tables, a soccer field, a fountain, a sandbox, a gate, a baseball diamond, a tree and a bike rack")

SCHOOL = Map(6, 5, [
    ("parking lot", 0, 0, 2, 1, "o"), ("office", 2, 0, 1, 1, "b"), ("front doors", 3, 0, 1, 1, "r"), ("library", 4, 0, 1, 1, "b"),
    ("music room", 5, 0, 1, 1, "b"),
    ("bike rack", 0, 1, 1, 1, "o"), ("gym", 2, 1, 2, 1, "b"), ("art room", 5, 1, 1, 1, "b"),
    ("garden", 0, 2, 1, 1, "g"), ("portable", 4, 2, 1, 1, "b"),
    ("play structure", 0, 3, 1, 1, "o"), ("field", 2, 3, 2, 2, "g"), ("sandbox", 5, 3, 1, 1, "o"),
    ("basketball court", 0, 4, 2, 1, "o"), ("bench", 4, 4, 1, 1, "o"),
], cw=88)
SCHOOL_LABEL = ("map of a school with a parking lot, office, front doors, library, music room, bike rack, gym, art room, "
                "garden, portable, play structure, field, sandbox, basketball court and bench")

TOWN = Map(6, 5, [
    ("library", 0, 0, 1, 1, "b"), ("school", 2, 0, 2, 1, "b"), ("fire station", 5, 0, 1, 1, "r"),
    ("bakery", 3, 1, 1, 1, "b"), ("park", 4, 1, 2, 2, "g"),
    ("skating rink", 0, 2, 1, 1, "w"), ("café", 1, 2, 1, 1, "r"), ("pool", 2, 2, 1, 1, "w"),
    ("grocery store", 1, 3, 1, 1, "b"), ("community centre", 3, 3, 1, 1, "b"), ("post office", 5, 3, 1, 1, "r"),
    ("Liam’s house", 0, 4, 1, 1, "o"), ("bus stop", 2, 4, 1, 1, "o"), ("dentist", 4, 4, 1, 1, "b"),
], cw=88)
TOWN_LABEL = ("map of a neighbourhood with a library, school, fire station, bakery, park, skating rink, café, pool, "
              "grocery store, community centre, post office, Liam’s house, bus stop and dentist")

BLANK = Map(6, 5, [], cw=46, ch=40)


def isare(n):
    return "are" if n.endswith("s") and n not in ("bus", "glass") else "is"


# ------------------------------------------------------------ set 1: grid references on a park map
def set_refs(rnd, P_):
    M = PARK
    pm = fig(M.svg(PARK_LABEL))
    its = []
    # what is in square ...?
    for cell in [(1, 2), (3, 4), (2, 0), (0, 2), (5, 2)]:
        ans = M.at(cell)
        sw = (cell[1], cell[0])
        cands = []
        swn = M.at(sw) if M.inside(sw) else None
        if swn and swn != ans:
            cands.append(swn)
        for d in HEAD:
            x = step(cell, d)
            if M.inside(x) and M.at(x) and M.at(x) != ans and M.at(x) not in cands:
                cands.append(M.at(x))
        cands += ["sandbox", "pond", "slide", "bench"]
        e = "Find column %s along the top, then go down to row %d. Square %s is the %s." % (COLS[cell[0]], cell[1] + 1, ref(cell), ans)
        if swn and swn != ans:
            e += " Mixing up the column and the row (column %s, row %d) gives the %s." % (COLS[sw[0]], sw[1] + 1, swn)
        its.append(mcq(pm + "What is in square <b>%s</b>?" % ref(cell), "the " + ans, ["the " + x for x in cands if x != ans], e, rnd))
    # what is the grid reference of ...?
    for name in ("pond", "bench", "splash pad", "sandbox", "slide", "gate"):
        c = M.single(name)
        good = ref(c)
        swapped = "%s%d" % (COLS[c[1]], c[0] + 1)
        assert c[0] < M.rows and swapped != good
        nb = (c[0], c[1] + 1) if c[1] + 1 < M.rows else (c[0], c[1] - 1)
        wrong = [swapped, "%d%s" % (c[1] + 1, COLS[c[0]]), ref(nb)]
        its.append(mcq(pm + "What is the grid reference of the <b>%s</b>?" % name, good, wrong,
                       "Go across to find the letter, then down to find the number. The %s %s in column %s, row %d: %s. "
                       "Write the letter first." % (name, isare(name), COLS[c[0]], c[1] + 1, good), rnd))
    # places that cover more than one square
    pl = sorted(M.where["parking lot"])
    its.append(mcq(pm + "The parking lot covers two squares. What are they?", "E1 and F1",
                   ["1E and 1F", "A5 and A6", "E2 and F2"],
                   "The parking lot is in row 1, in columns E and F. Letter first: E1 and F1.", rnd))
    assert [ref(c) for c in pl] == ["E1", "F1"]
    bd = sorted(M.where["baseball diamond"])
    assert [ref(c) for c in bd] == ["B5", "C5"]
    its.append(mcq(pm + "Which squares does the baseball diamond cover?", "B5 and C5",
                   ["5B and 5C", "E2 and E3", "B4 and C4"],
                   "The baseball diamond is in the bottom row, row 5, in columns B and C: B5 and C5.", rnd))
    assert sorted(ref(c) for c in M.where["soccer field"]) == ["D3", "D4", "E3", "E4"]
    its.append(mcq_num(pm + "How many squares does the soccer field cover on the map?", 4, [2, 3, 6],
                       "The soccer field is 2 squares across and 2 squares down: D3, E3, D4 and E4. That is 4 squares."))
    # empty squares
    assert M.at((1, 1)) is None and M.at((2, 1)) == "bench" and M.at((1, 2)) == "picnic tables" and M.at((0, 1)) == "pond"
    its.append(mcq(pm + "Which square is <b>empty</b>?", "B2", ["C2", "B3", "A2"],
                   "B2 is in column B, row 2. Nothing is there. C2 is the bench, B3 is the picnic tables and A2 is the pond.", rnd))
    assert M.at((4, 4)) is None and M.at((3, 4)) == "tree" and M.at((5, 4)) == "bike rack" and M.at((4, 3)) == "soccer field"
    its.append(mcq(pm + "Which square in row 5 is empty?", "E5", ["D5", "F5", "A5"],
                   "Look along row 5: A5 is the gate, B5 and C5 are the baseball diamond, D5 is the tree, E5 is empty and F5 is the bike rack.", rnd))
    # columns and rows
    its.append(mcq(pm + "Which column is the bench in?", "column C", ["column 2", "column B", "column D"],
                   "Columns go up and down and are named with letters. The bench is under the letter C. Its row is 2, so its grid reference is C2.", rnd))
    its.append(mcq(pm + "Which row is the fountain in?", "row 3", ["row 6", "row 2", "row 4"],
                   "Rows go across and are named with numbers. The fountain is beside the number 3. It is in column F, the 6th column, but row 3: F3.", rnd))
    its.append(mcq(pm + "Which grid reference is <b>not</b> on this map?", "G2", ["F5", "A1", "C4"],
                   "The columns go from A to F and the rows go from 1 to 5. There is no column G, so G2 is not on the map.", rnd))
    n, he, his, him = P_.next()
    its.append(mcq(pm + "%s says the sandbox is in square <b>D2</b>. What mistake did %s make?" % (n, he),
                   "%s mixed up the column and the row" % he,
                   ["%s counted the starting square" % he, "%s wrote the number first" % he, "%s used the wrong map" % he],
                   "The sandbox is in column B (the 2nd column) and row 4: B4. %s used the 4 as the column (D) and the 2 as the row. "
                   "Always go across to the letter first, then down to the number." % n, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Read a grid map: grid references like B3", "items": its}


# ------------------------------------------------------------ set 2: position words on a school map
WORD = {"right": "to the right of", "left": "to the left of", "down": "below", "up": "above"}


def set_position(rnd, P_):
    M = SCHOOL
    sm = fig(M.svg(SCHOOL_LABEL))
    its = []

    def between_q(a, b, wrong):
        ans = between_all(M, a, b)
        assert len(ans) == 1, (a, b, ans)
        ans = ans.pop()
        its.append(mcq(sm + "What is <b>between</b> the %s and the %s?" % (a, b), "the " + ans, ["the " + w for w in wrong],
                       "Find the %s and the %s. They are in the same %s. The place in the middle of them is the %s."
                       % (a, b, "row" if M.where[a][0][1] == M.where[b][0][1] else "column", ans), rnd))

    between_q("office", "library", ["gym", "music room", "parking lot"])
    between_q("parking lot", "front doors", ["bike rack", "gym", "library"])
    between_q("bike rack", "play structure", ["basketball court", "parking lot", "field"])

    def just_q(name, d, ans, wrong, e):
        x = [step(c, d) for c in M.where[name]]
        got = {M.at(c) for c in x if M.inside(c)} - {None}
        assert ans in got, (name, d, got)
        its.append(mcq(sm + "What is just <b>%s</b> the %s on the map?" % (WORD[d], name), "the " + ans, ["the " + w for w in wrong], e, rnd))

    just_q("office", "down", "gym", ["parking lot", "front doors", "garden"],
           "Look one square down from the office. That square is part of the gym. The parking lot is on the left of the office.")
    just_q("play structure", "up", "garden", ["basketball court", "bike rack", "field"],
           "Look one square up from the play structure. It is the garden. The basketball court is below it, not above.")
    just_q("library", "left", "front doors", ["music room", "office", "portable"],
           "Look one square to the left of the library. It is the front doors. The music room is on its right.")
    just_q("basketball court", "right", "field", ["bench", "play structure", "sandbox"],
           "Look one square to the right of the basketball court. It is part of the field.")
    just_q("art room", "up", "music room", ["sandbox", "library", "portable"],
           "Look one square up from the art room. It is the music room, in the top row.")
    nb = neighbours(M, "bench")
    assert nb == ["field"], nb
    its.append(mcq(sm + "Which place is <b>next to</b> the bench?", "the field", ["the sandbox", "the portable", "the basketball court"],
                   "Next to means touching, side by side. The field is just to the left of the bench. The sandbox and the portable are 2 squares away.", rnd))
    assert sorted(neighbours(M, "garden")) == ["bike rack", "play structure"]
    its.append(mcq(sm + "The garden is next to two places. What are they?", "the bike rack and the play structure",
                   ["the play structure and the basketball court", "the bike rack and the parking lot", "the gym and the field"],
                   "Look at the squares touching the garden: the bike rack is just above it and the play structure is just below it. The square on its right is empty.", rnd))
    assert set(neighbours(M, "gym")) == {"office", "front doors"}
    its.append(mcq(sm + "Which place is next to the gym?", "the front doors", ["the portable", "the library", "the garden"],
                   "The front doors touch the top of the gym. The portable, the library and the garden do not touch it: there is a gap.", rnd))
    assert M.at((5, 0)) == "music room" and M.at((0, 4)) == "basketball court"
    its.append(mcq(sm + "What is in the <b>top right</b> corner of the map?", "the music room",
                   ["the parking lot", "the basketball court", "the art room"],
                   "Top means the top row. Right means the right side. The music room is in the top right corner. The parking lot is in the top left.", rnd))
    its.append(mcq(sm + "What is in the <b>bottom left</b> corner of the map?", "the basketball court",
                   ["the bench", "the parking lot", "the play structure"],
                   "Bottom means the bottom row. Left means the left side. The basketball court is in the bottom left corner. "
                   "The play structure is just above it.", rnd))
    d = {n: dist(M, "front doors", n) for n in ("gym", "portable", "sandbox", "bench")}
    assert d["gym"] == 1 and min(v for k, v in d.items() if k != "gym") > 1, d
    its.append(mcq(sm + "Which of these places is <b>closest</b> to the front doors?", "the gym",
                   ["the portable", "the sandbox", "the bench"],
                   "The gym is right below the front doors, 1 square away. The portable is %s away and the others are further." % sq(d["portable"]), rnd))
    assert dist(M, "front doors", "field") == 3
    its.append(mcq_num(sm + "How many squares do you move from the front doors, straight down the map, to the field?", 3, [4, 2, 5],
                       "From the front doors (D1) go down: D2 is 1, D3 is 2 and the field (D4) is 3. Do not count the square you start on."))
    assert dist(M, "bike rack", "gym") == 2
    its.append(mcq_num(sm + "How many squares do you move from the bike rack, straight to the right, to the gym?", 2, [3, 1, 4],
                       "From the bike rack (A2) go right: B2 is 1 and the gym (C2) is 2. Do not count the bike rack square."))
    assert direction(M, "library", "front doors") == "right"
    its.append(mcq(sm + "The library is ___ the front doors.", "right of", ["left of", "above", "below"],
                   "The library is in the same row as the front doors, one square to the right.", rnd))
    assert direction(M, "field", "gym") == "down"
    its.append(mcq(sm + "The field is ___ the gym.", "below", ["above", "left of", "right of"],
                   "The field and the gym share columns C and D. The field is lower on the map, so it is below the gym.", rnd))
    # left and right for a person
    n, he, his, him = P_.next()
    its.append(mcq(sm + "%s stands in square B3 and faces the <b>top</b> of the map. Is the garden on %s left or %s right?" % (n, his, his),
                   "on %s left" % his, ["on %s right" % his, "in front of %s" % him, "behind %s" % him],
                   "%s faces the top of the map, the same way you look at the page. The garden (A3) is on the left side of B3, so it is on %s left." % (n, his), rnd))
    n, he, his, him = P_.next()
    its.append(mcq(sm + "%s stands in square B3 and faces the <b>bottom</b> of the map. Is the garden on %s left or %s right?" % (n, his, his),
                   "on %s right" % his, ["on %s left" % his, "in front of %s" % him, "behind %s" % him],
                   "%s faces the bottom of the map, the opposite way to you. %s left and right are swapped. "
                   "Turn the page upside down to check: the garden (A3) is on %s right." % (n, his.capitalize(), his), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Position words: next to, between, above, below, left and right", "items": its}


# ------------------------------------------------------------ set 3: follow moves on a grid map
def set_moves(rnd, P_):
    its = []
    pos = Pos(rnd)
    G = BLANK

    def letters_q(start, moves, who):
        n, he, his, him = who
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
        svg = G.svg("grid map with a red dot and squares A to D", marks)
        e = walk_e(start, moves) + " That is square %s." % "ABCD"[p]
        tip = {"lr": " If you mix up left and right you land on %s.", "ud": " If you mix up up and down you land on %s.",
               "start": " If you count the starting square you stop 1 short, on %s.", "swap": " Going %d %s first by mistake gives %s."}
        k0 = why[cells[0]]
        if k0 == "swap":
            e += tip["swap"] % (moves[1][1], moves[0][0], "ABCD"[order.index(cells[0])])
        elif k0 in tip:
            e += tip[k0] % "ABCD"[order.index(cells[0])]
        q = "%s starts on the red dot. %s moves <b>%s</b>. Where does %s finish?" % (n, he.capitalize(), moves_txt(moves), he)
        its.append(mcq_fixed(fig(svg) + q, ["A", "B", "C", "D"], "ABCD"[p], e))

    for start, moves in [((1, 3), [("right", 3)]), ((4, 4), [("up", 3)]), ((4, 1), [("left", 3)]), ((2, 0), [("down", 3)]),
                         ((0, 4), [("right", 3), ("up", 2)]), ((5, 4), [("up", 1), ("left", 3)]),
                         ((1, 0), [("down", 2), ("right", 3)]), ((4, 3), [("left", 2), ("up", 3)])]:
        letters_q(start, moves, P_.next())

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
        e = walk_e(s0, moves) + " The %s %s in %s." % (ans, isare(ans), ref(end))
        its.append(mcq(pm + "Start at the %s. Move <b>%s</b>. What do you reach?" % (frm, moves_txt(moves)), "the " + ans,
                       ["the " + c for c in cands if c != frm], e, rnd))

    land_q("gate", [("up", 2), ("right", 1)], ["sandbox", "pond"])
    land_q("sandbox", [("up", 2), ("right", 1)], ["swings", "pond"])
    land_q("bike rack", [("up", 3), ("left", 1)], ["fountain", "slide"])
    land_q("pond", [("right", 2), ("up", 1)], ["slide", "bench"])
    land_q("fountain", [("down", 2), ("left", 2)], ["baseball diamond", "bike rack"])

    def route_q(a, b):
        A, B = M.single(a), M.single(b)
        dx, dy = B[0] - A[0], B[1] - A[1]
        mv = [("right" if dx > 0 else "left", abs(dx)), ("up" if dy < 0 else "down", abs(dy))]
        assert walk(A, mv) == B and dx and dy
        wrong = [[(OPP[mv[0][0]], mv[0][1]), mv[1]], [mv[0], (OPP[mv[1][0]], mv[1][1])], [(mv[0][0], mv[0][1] + 1), (mv[1][0], mv[1][1] + 1)]]
        if mv[0][1] != mv[1][1]:
            wrong.insert(2, [(mv[0][0], mv[1][1]), (mv[1][0], mv[0][1])])
        for w in wrong:
            assert walk(A, w) != B
        its.append(mcq(pm + "Which moves take you from the %s to the %s?" % (a, b), moves_short(mv),
                       [moves_short(w) for w in wrong],
                       "The %s is in %s and the %s is in %s. Count the squares you move, not the square you start on: %s." % (
                           a, ref(A), b, ref(B), moves_txt(mv)), rnd))

    route_q("gate", "bench")
    route_q("pond", "sandbox")
    route_q("slide", "fountain")
    a, b = M.single("gate"), M.single("tree")
    assert a[1] == b[1]
    k = b[0] - a[0]
    its.append(mcq_num(pm + "How many squares to the right is it from the gate to the tree?", k, [k + 1, k - 1, k + 2],
                       "The gate is in %s and the tree is in %s. Count the moves: %s right. Do not count the gate square." % (ref(a), ref(b), sq(k))))
    a = M.single("swings")
    b = (2, 4)
    assert M.at(b) == "baseball diamond"
    k = b[1] - a[1]
    its.append(mcq_num(pm + "How many squares down is it from the swings to the baseball diamond, going straight down?", k, [k + 1, k - 1, k + 2],
                       "The swings are in %s. Go straight down: C2, C3, C4, C5. The baseball diamond is in C5. That is %s down." % (ref(a), sq(k))))

    def ref_q(frm, moves):
        s0 = M.single(frm)
        end = walk(s0, moves)
        assert M.inside(end)
        cands = []
        for kind, m in mistake_moves(moves):
            c = walk(s0, m)
            if M.inside(c) and c != end and c != s0 and ref(c) not in cands:
                cands.append(ref(c))
        cands.insert(1, "%d%s" % (end[1] + 1, COLS[end[0]]))
        its.append(mcq(pm + "Start in the square with the %s. Move <b>%s</b>. Which square do you land in?" % (frm, moves_txt(moves)),
                       ref(end), cands, walk_e(s0, moves), rnd))

    ref_q("washrooms", [("right", 3), ("down", 2)])
    ref_q("bike rack", [("left", 2), ("up", 3)])
    assert len(its) == 20, len(its)
    return {"title": "Follow moves on a grid: right, left, up and down", "items": its}


# ------------------------------------------------------------ set 4: quarter turns and half turns
def facing_svg(names, face, turn_to=None, cw=True, label=None):
    """A room seen from above with a name on each wall (top, right, bottom, left) and a child in the middle
    with an arrow for the way the child faces. turn_to: draw a curved arrow for the turn."""
    W, H = 350, 180
    cx, cy = W / 2.0, H / 2.0 + 2
    s = ["<rect x='3' y='3' width='%d' height='%d' rx='6' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (W - 6, H - 6, GREEN)]
    for n in names:
        assert tw(n, 15, True) <= 108, n
    s.append(text(cx, 26, names[0], 15))
    s.append(text(W - 12, cy + 5, names[1], 15, anchor="end"))
    s.append(text(cx, H - 13, names[2], 15))
    s.append(text(12, cy + 5, names[3], 15, anchor="start"))
    u = VEC[HEAD[face]]
    if turn_to is not None:
        a0 = math.atan2(u[1], u[0])
        k = (turn_to - face) % 4 if cw else (face - turn_to) % 4
        sg = 1 if cw else -1
        a0 += sg * 0.3
        sweep = math.radians(90 * k) - 0.6
        R = 48
        pts = [(cx + R * math.cos(a0 + sg * sweep * i / 16.0), cy + R * math.sin(a0 + sg * sweep * i / 16.0)) for i in range(17)]
        s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='3'/>" % (P(pts[:-1]), RED))
        s.append(arrowhead(pts[-3], pts[-1], -2, RED, L=11, W=6))
    s.append("<circle cx='%.1f' cy='%.1f' r='12' fill='#f4a6c0' stroke='#a33' stroke-width='2'/>" % (cx, cy))
    p0 = (cx + u[0] * 14, cy + u[1] * 14)
    p1 = (cx + u[0] * 34, cy + u[1] * 34)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3.4'/>" % (p0 + p1 + (INK,)))
    s.append(arrowhead(p0, (cx + u[0] * 44, cy + u[1] * 44), 0, INK, L=11, W=7))
    lab = label or ("room seen from above with the %s at the top, the %s on the right, the %s at the bottom and the %s on the left, "
                    "and a child facing the %s" % (names[0], names[1], names[2], names[3], names[face]))
    return svg_wrap(W, H, "".join(s), lab)


CLASSROOM = ["board", "window", "door", "bookshelf"]
GYM = ["stage", "clock", "doors", "benches"]
RINK = ["scoreboard", "snack bar", "doors", "penalty box"]
KITCHEN = ["fridge", "window", "table", "stove"]
TURN_NAME = {1: "a quarter turn clockwise", 2: "a half turn", 3: "a quarter turn counterclockwise", 0: "a full turn"}


def set_turns(rnd, P_):
    its = []
    pos = Pos(rnd)
    # facing questions
    for names, face, turns in [(CLASSROOM, 0, [(1, True)]), (GYM, 1, [(1, False)]), (RINK, 2, [(2, True)]),
                               (KITCHEN, 3, [(1, True)]), (CLASSROOM, 2, [(1, False)]), (GYM, 0, [(1, True), (1, True)])]:
        n, he, his, him = P_.next()
        h = face
        for q, c in turns:
            h = (h + (q if c else -q)) % 4
        ans = names[h]
        tt = [("a half turn" if q == 2 else "a quarter turn " + ("clockwise" if c else "counterclockwise")) for q, c in turns]
        turn_t = tt[0] if len(tt) == 1 else tt[0] + ", then another " + tt[1][2:]
        wrong = []
        if turns[0][0] == 1:
            ww = (face - sum(q if c else -q for q, c in turns)) % 4
            wrong.append(names[ww])
        else:
            wrong.append(names[(face + 1) % 4])
        wrong += [names[(face + 2) % 4], names[face]] + names
        e = "%s starts facing the %s. " % (n, names[face])
        if turns[0][0] == 2:
            e += "A half turn is two quarter turns, so %s ends up facing the opposite wall: the %s." % (he, ans)
        elif len(turns) == 2:
            e += ("Clockwise goes the same way as the hands of a clock: top, right, bottom, left. One quarter turn clockwise takes %s to the %s, "
                  "and another takes %s to the %s. Two quarter turns make a half turn." % (him, names[(face + 1) % 4], him, ans))
        elif turns[0][1]:
            e += "Clockwise goes the same way as the hands of a clock: top, right, bottom, left. One quarter turn clockwise from the %s is the %s." % (names[face], ans)
        else:
            e += ("Counterclockwise goes the other way: top, left, bottom, right. One quarter turn counterclockwise from the %s is the %s. "
                  "Turning clockwise by mistake would give the %s." % (names[face], ans, wrong[0]))
        its.append(mcq(fig(facing_svg(names, face)) + "%s faces the %s. %s makes <b>%s</b>. What does %s face now?" % (
            n, names[face], he.capitalize(), turn_t, he), "the " + ans, ["the " + w for w in wrong if w != ans], e, rnd))
    # which turn?
    for names, a, b in [(CLASSROOM, 1, 0), (RINK, 3, 0)]:
        n, he, his, him = P_.next()
        k = (b - a) % 4
        ans = TURN_NAME[k]
        its.append(mcq(fig(facing_svg(names, a)) + "%s faces the %s. Which turn makes %s face the %s?" % (n, names[a], him, names[b]),
                       ans, [TURN_NAME[(4 - k) % 4], "a half turn", "a full turn", TURN_NAME[1]],
                       "Clockwise goes top, right, bottom, left. From the %s, one quarter turn %s brings %s to the %s. "
                       "A quarter turn the other way would face the %s." % (
                           names[a], "clockwise" if k == 1 else "counterclockwise", him, names[b], names[(a - (1 if k == 1 else -1)) % 4]), rnd))
    # robot on a grid
    G = BLANK
    for start, h, ops in [((0, 4), 0, [("F", 3), ("T", 1, True), ("F", 2)]),
                          ((5, 4), 3, [("F", 2), ("T", 1, True), ("F", 3)]),
                          ((1, 0), 2, [("F", 2), ("T", 1, False), ("F", 3)]),
                          ((4, 1), 3, [("F", 3), ("T", 1, False), ("F", 2)]),
                          ((0, 2), 1, [("F", 4), ("T", 2, True), ("F", 1)]),
                          ((0, 4), 0, [("F", 2), ("T", 1, True), ("F", 2), ("T", 1, True), ("F", 1)]),
                          ((5, 0), 2, [("F", 3), ("T", 1, True), ("F", 2), ("T", 1, False), ("F", 1)])]:
        pts, _ = run(start, h, ops)
        assert pts
        ans = pts[-1]
        cells, why = [], {}
        for kind, m in mistake_ops(ops):
            p2, _ = run(start, h, m)
            if p2 and p2[-1] not in cells and p2[-1] not in (ans, start):
                cells.append(p2[-1])
                why[p2[-1]] = kind
        assert len(cells) >= 3, (start, ops, cells)
        cells = cells[:3]
        p = pos.next()
        order = cells[:]
        order.insert(p, ans)
        marks = [(start, "robot", h)] + [(c, "letter", "ABCD"[i]) for i, c in enumerate(order)]
        svg = G.svg("grid map with a robot facing %s and squares A to D" % FACE_TXT[h], marks)
        e = ops_e(start, h, ops) + " That is square %s." % "ABCD"[p]
        k0 = why[cells[0]]
        L0 = "ABCD"[order.index(cells[0])]
        if k0 == "wrongway":
            e += TIP[k0] % ("counterclockwise instead of clockwise" if [o for o in ops if o[0] == "T"][0][2] else "clockwise instead of counterclockwise", L0)
        else:
            e += TIP[k0] % L0
        q = "The robot faces the way its arrow points. It follows these steps: <b>%s</b>. Where does it stop?" % ops_txt(ops)
        its.append(mcq_fixed(fig(svg) + q, ["A", "B", "C", "D"], "ABCD"[p], e))
    # describe the path
    for start, h, ops in [((0, 4), 0, [("F", 2), ("T", 1, True), ("F", 3)]),
                          ((5, 1), 3, [("F", 3), ("T", 1, False), ("F", 2)]),
                          ((1, 0), 2, [("F", 1), ("T", 1, False), ("F", 4)]),
                          ((4, 4), 0, [("F", 2), ("T", 1, False), ("F", 2), ("T", 1, True), ("F", 1)])]:
        pts, _ = run(start, h, ops)
        assert pts
        wrong = [[("T", 1, not o[2]) if o[0] == "T" else o for o in ops],
                 [("F", o[1] + 1) if o[0] == "F" else o for o in ops]]
        fs = [o[1] for o in ops if o[0] == "F"]
        if len(fs) == 2 and fs[0] != fs[1]:
            it = iter(fs[::-1])
            wrong.append([("F", next(it)) if o[0] == "F" else o for o in ops])
        wrong.append([("T", 2, True) if o[0] == "T" and i == 1 else o for i, o in enumerate(ops)])
        for w in wrong:
            p2, _ = run(start, h, w)
            assert p2 != pts, w
        svg = G.svg("grid map with a robot facing %s and a dashed path" % FACE_TXT[h], [(start, "robot", h)], path=pts)
        e = ops_e(start, h, ops) + " Count the squares the robot moves, not the square it starts on, and check which way it turns."
        its.append(mcq(fig(svg) + "The robot starts facing the way its arrow points. Which steps make it follow the dashed path?",
                       ops_short(ops), [ops_short(w) for w in wrong], e, rnd))
    its.append(mcq_num("How many quarter turns make a half turn?", 2, [1, 3, 4],
                       "A quarter turn is one of four equal turns that go all the way around. Two quarter turns make a half turn, and a half turn makes you face the opposite way."))
    assert len(its) == 20, len(its)
    return {"title": "Quarter turns and half turns: follow and describe a path", "items": its}


# ------------------------------------------------------------ set 5: word problems in the neighbourhood
def set_words(rnd, P_):
    M = TOWN
    tm = fig(M.svg(TOWN_LABEL))
    its = []
    house = M.single("Liam’s house")
    rink = M.single("skating rink")
    assert walk(house, [("up", 2)]) == rink and M.at(walk(house, [("up", 1)])) is None
    its.append(mcq(tm + "Liam leaves his house and walks 2 squares up the map. What does he reach?", "the skating rink",
                   ["the café", "the library", "the grocery store"],
                   walk_e(house, [("up", 2)]) + " The skating rink is in A3. Counting his house as 1 would stop him in A4, an empty square.", rnd))
    its.append(mcq(tm + "Find the skating rink. What is its grid reference?", "A3", ["3A", "C1", "A4"],
                   "The skating rink is in column A and row 3. Write the letter first: A3. C1 has the column and row mixed up.", rnd))
    assert M.at((1, 3)) == "grocery store" and M.at((3, 1)) == "bakery"
    its.append(mcq(tm + "What is in square <b>B4</b>?", "the grocery store", ["the bakery", "the café", "the bus stop"],
                   "Find column B, then go down to row 4: the grocery store. Mixing up the column and the row (column D, row 2) gives the bakery.", rnd))
    sch = (2, 0)
    assert M.at(sch) == "school" and walk(house, [("right", 2), ("up", 4)]) == sch
    its.append(mcq(tm + "Which moves take Liam from his house to the school?", "2 right, 4 up",
                   ["4 right, 2 up", "2 right, 4 down", "3 right, 5 up"],
                   "The house is in A5 and the school starts in C1. Go 2 squares right (A to C) and 4 squares up (row 5 to row 1). "
                   "Count the moves, not the starting square.", rnd))
    assert dist(M, "library", "school") == 2
    its.append(mcq_num(tm + "Each square on the map stands for 100 m. How far is it from the library, straight to the right, to the school?", 200,
                       [300, 100, 400],
                       "From the library (A1) to the school (C1) is 2 squares. 2 × 100 m = 200 m. Counting the library square too gives 300 m.", " m"))
    assert walk(rink, [("right", 2)]) == M.single("pool")
    its.append(mcq_num(tm + "Each square is 100 m. Liam walks from his house 2 squares up to the skating rink, then 2 squares right to the pool. How far does he walk in all?",
                       400, [200, 600, 300],
                       "Up to the rink is 2 squares and over to the pool is 2 more: 2 + 2 = 4 squares. 4 × 100 m = 400 m.", " m"))
    assert between_all(M, "skating rink", "pool") == {"café"}
    its.append(mcq(tm + "What is between the skating rink and the pool?", "the café", ["the grocery store", "the school", "the bakery"],
                   "The skating rink (A3), the café (B3) and the pool (C3) are in row 3. The café is in the middle.", rnd))
    fs = M.single("fire station")
    assert M.at(walk(fs, [("down", 3)])) == "post office" and M.at(walk(fs, [("down", 2)])) == "park"
    n, he, his, him = P_.next()
    its.append(mcq(tm + "%s is at the fire station. %s walks 3 squares down the map. Where is %s now?" % (n, he.capitalize(), he), "at the post office",
                   ["at the park", "at the dentist", "at the community centre"],
                   walk_e(fs, [("down", 3)]) + " The post office is in F4. Counting the fire station square would stop %s at the park." % him, rnd))
    cc = M.single("community centre")
    assert M.at(walk(cc, [("down", 1), ("right", 1)])) == "dentist" and M.at(walk(cc, [("down", 1), ("left", 1)])) == "bus stop"
    n, he, his, him = P_.next()
    its.append(mcq(tm + "%s leaves the community centre. %s goes 1 square down, then 1 square right. Where is %s?" % (n, he.capitalize(), he),
                   "at the dentist", ["at the bus stop", "at the bakery", "at the park"],
                   walk_e(cc, [("down", 1), ("right", 1)]) + " The dentist is in E5. Going left instead of right gives the bus stop.", rnd))
    bus = M.single("bus stop")
    pts, hh = run(bus, 0, [("F", 1), ("T", 1, False), ("F", 1)])
    assert M.at(pts[-1]) == "grocery store"
    p2, _ = run(bus, 0, [("F", 1), ("T", 1, True), ("F", 1)])
    assert M.at(p2[-1]) == "community centre"
    n, he, his, him = P_.next()
    its.append(mcq(tm + "%s stands at the bus stop, facing up the map. %s walks 1 square forward, makes a quarter turn counterclockwise, then walks 1 square forward. Where is %s?" % (
        n, he.capitalize(), he), "at the grocery store", ["at the community centre", "at the pool", "at the café"],
        "From the bus stop (C5) one square forward is C4. A quarter turn counterclockwise turns %s to face left. One square left is B4: the grocery store. "
        "Turning clockwise by mistake gives the community centre." % him, rnd))
    cafe = M.single("café")
    pts, _ = run(cafe, 0, [("F", 2), ("T", 1, True), ("F", 1)])
    assert M.at(pts[-1]) == "school" and pts[-1] == (2, 0)
    p2, _ = run(cafe, 0, [("F", 2), ("T", 1, False), ("F", 1)])
    assert M.at(p2[-1]) == "library"
    n, he, his, him = P_.next()
    its.append(mcq(tm + "%s leaves the café, facing up the map. %s walks 2 squares forward, makes a quarter turn clockwise, then walks 1 square forward. Where is %s?" % (
        n, he.capitalize(), he), "at the school", ["at the library", "at the bakery", "at the pool"],
        "From the café (B3) two squares forward is B1. A quarter turn clockwise turns %s to face right. One square right is C1: the school. "
        "Turning counterclockwise by mistake gives the library." % him, rnd))
    n, he, his, him = P_.next()
    its.append(mcq(tm + "%s waits at the bus stop, facing the pool (up the map). Then %s makes a half turn. Which way does %s face now?" % (n, he, he),
                   "down the map", ["up the map", "to the left", "to the right"],
                   "A half turn makes you face the opposite way. Up becomes down. A quarter turn would make %s face left or right." % him, rnd))
    assert dist(M, "bus stop", "pool") == 2
    its.append(mcq_num(tm + "Each square is 100 m. How far is it from the bus stop straight up to the pool?", 200, [300, 100, 400],
                       "From the bus stop (C5) up to the pool (C3) is 2 squares. 2 × 100 m = 200 m.", " m"))
    assert walk(sch, [("left", 2), ("down", 2)]) == rink
    its.append(mcq(tm + "The class goes skating on a field trip. Which moves take them from the school (C1) to the skating rink?", "2 left, 2 down",
                   ["2 right, 2 down", "2 left, 2 up", "3 left, 3 down"],
                   "The school is in C1 and the skating rink is in A3. Go 2 squares left (C to A) and 2 squares down (row 1 to row 3).", rnd))
    # text problems
    n, he, his, him = P_.next()
    its.append(mcq("%s faces the board. %s makes a quarter turn clockwise, then another quarter turn clockwise. What turn did %s make in all?" % (n, he.capitalize(), he),
                   "a half turn", ["a quarter turn", "a full turn", "no turn"],
                   "Two quarter turns the same way make a half turn. %s now faces the back of the classroom." % n, rnd))
    n, he, his, him = P_.next()
    its.append(mcq("In gym class, the teacher says: “Make a quarter turn to your right.” Which way does %s turn?" % n, "clockwise",
                   ["counterclockwise", "a half turn around", "%s does not turn" % he],
                   "Turning to your right goes the same way as the hands of a clock, so it is a quarter turn clockwise. Turning to your left is counterclockwise.", rnd))
    n, he, his, him = P_.next()
    its.append(mcq("%s writes that the swings on a park map are in square <b>3B</b>. Which grid reference should %s write?" % (n, he), "B3",
                   ["3B", "C2", "2C"],
                   "Write the letter (the column) first, then the number (the row): B3. C2 is a different square.", rnd))
    its.append(mcq_num("On a map, each square stands for 10 m. A bike path is 6 squares long on the map. How long is the real bike path?", 60, [16, 6, 70],
                       "Each square is 10 m, so 6 squares is 6 × 10 m = 60 m. Adding 6 + 10 = 16 does not work.", " m"))
    n, he, his, him = P_.next()
    its.append(mcq("%s walks 3 squares right on a grid, then 3 squares left. Where is %s now?" % (n, he), "back where %s started" % he,
                   ["6 squares right of the start", "3 squares right of the start", "3 squares left of the start"],
                   "Left is the opposite of right. 3 squares left undoes 3 squares right, so %s is back at the start." % n, rnd))
    its.append(mcq_num(tm + "Each square is 100 m. Liam walks from his house to the skating rink and back home again. How far does he walk?", 400,
                       [200, 600, 300],
                       "The house (A5) to the skating rink (A3) is 2 squares, or 200 m. There and back is 200 m + 200 m = 400 m.", " m"))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: find the skating rink and other places", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    park = PARK.svg("park map with square B4 highlighted: the sandbox", hi=(1, 3))
    route = BLANK.svg("grid map with a dashed route from a red dot 3 squares right and 2 squares up",
                      marks=[((0, 4), "dot", None)], path=[(0, 4), (3, 4), (3, 2)])
    assert walk((0, 4), [("right", 3), ("up", 2)]) == (3, 2)
    room = facing_svg(CLASSROOM, 0, turn_to=1, cw=True,
                      label="room seen from above: a child faces the board, and a curved arrow shows a quarter turn clockwise to the window")
    pts, _ = run((0, 4), 0, [("F", 2), ("T", 1, True), ("F", 3)])
    assert pts[-1] == (3, 2)
    rob = BLANK.svg("grid map with a robot facing up and a dashed path 2 squares forward, a quarter turn clockwise, then 3 squares forward",
                    marks=[((0, 4), "robot", 0)], path=pts)
    return (
        "<h2>Grid maps and grid references</h2>"
        "<p>A <b>map</b> shows a place from above. Many maps have a grid. The <b>columns</b> have letters across the top. "
        "The <b>rows</b> have numbers down the side. A <b>grid reference</b> like <b>B4</b> names one square.</p>"
        "<p>Go across to the letter first. Then go down to the number.</p>"
        "<figure class='sn-fig'>" + park +
        "<figcaption>Square B4 is column B, row 4. The sandbox is in B4.</figcaption></figure>" +
        ex("Example", "On the park map, what is in square E2?",
           "Go across to column E. Then go down to row 2.", "the splash pad") +
        "<h2>Position words</h2>"
        "<p>Use words like <b>next to</b>, <b>between</b>, <b>above</b>, <b>below</b>, <b>left of</b> and <b>right of</b>. "
        "On the park map, the slide is between the swings and the parking lot. The pond is above the garden.</p>"
        "<h2>Follow moves on a grid</h2>"
        "<p>Do one move at a time. Count the squares you <b>move</b>. Do not count the square you start on.</p>"
        "<figure class='sn-fig'>" + route +
        "<figcaption>Start at the red dot (A5). Move 3 squares right to D5, then 2 squares up to D3.</figcaption></figure>"
        "<h2>Quarter turns and half turns</h2>"
        "<p>A <b>quarter turn</b> is one of four equal turns that go all the way around. A <b>half turn</b> is two quarter turns: "
        "you face the opposite way. <b>Clockwise</b> turns the same way as the hands of a clock. "
        "<b>Counterclockwise</b> turns the other way.</p>"
        "<figure class='sn-fig'>" + room +
        "<figcaption>Maya faces the board. A quarter turn clockwise makes her face the window. A half turn would make her face the door.</figcaption></figure>"
        "<p>A robot on a grid moves <b>forward</b> the way it faces. When it turns, it stays on the same square.</p>"
        "<figure class='sn-fig'>" + rob +
        "<figcaption>Facing up: move 2 squares forward to A3, make a quarter turn clockwise (now facing right), move 3 squares forward to D3.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Swapping the column and the row (B4 read as D2)", "Letter first, across. Then the number, down."],
            ["Writing the number first (4B)", "Always write the letter first: B4."],
            ["Counting the starting square", "Count the moves, not the square you stand on."],
            ["Turning the wrong way", "Clockwise goes like clock hands: top, right, bottom, left."],
            ["Making a quarter turn for a half turn", "A half turn is two quarter turns. You face the opposite way."],
            ["Using left and right of the page for a person facing the bottom", "Turn the map so you face the same way as the person."],
        ])
    )


FAQ = [
    {"q": "What do Grade 3 students learn about location and movement in Ontario math?",
     "a": "In the Ontario curriculum (Spatial Sense, E1.4), Grade 3 students create and read simple maps of familiar places and give and follow multi-step directions that use distances and quarter and half turns."},
    {"q": "How do you read a grid reference like B3?",
     "a": "Go across to column B first, then down to row 3. The letter always comes first, so B3 is not the same square as C2."},
    {"q": "What is the difference between a quarter turn and a half turn?",
     "a": "A quarter turn is one of four equal turns that go all the way around. A half turn is two quarter turns, so you end up facing the opposite way."},
    {"q": "Are maps and directions on the Grade 3 EQAO math assessment?",
     "a": "The Grade 3 EQAO math assessment is based on the Ontario curriculum, which includes spatial sense, so questions about maps, position and movement can appear. These worksheets are good practice."},
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
    rnd = random.Random(33815)
    P_ = People(rnd)
    sets = [set_refs(rnd, P_), set_position(rnd, P_), set_moves(rnd, P_), set_turns(rnd, P_), set_words(rnd, P_)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-3", "slug": "location-and-movement", "sort": 15,
        "updated": UPDATED, "pdf_url": "",
        "title": "Location and Movement: Grid Maps, Directions and Quarter Turns",
        "seo_title": "Grade 3 Location and Movement Worksheets: Grid Maps and Turns (Free)",
        "short_title": "Location and movement",
        "domain": "Spatial Sense",
        "standard_code": "Grade 3: E1.4",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Create and interpret simple maps of familiar places",
        "meta_desc": "Free Grade 3 math worksheets on location and movement: read grid maps with references like B3, use position words, "
                     "follow moves on a grid and make quarter and half turns, clockwise and counterclockwise. 100 questions with an answer key, "
                     "Ontario curriculum aligned and great EQAO practice.",
        "key_big": "A grid reference gives the letter (across) first, then the number (down): B3.",
        "key_sub": "When you follow moves, count the squares you move, not the square you start on. A quarter turn clockwise goes the same way as the hands of a clock.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (maps, grids, rooms) so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "(map|grid map|room seen)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
