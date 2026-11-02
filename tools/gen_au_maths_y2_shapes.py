# -*- coding: utf-8 -*-
"""
AU Year 2 Maths: 2-D shapes (Australian Curriculum v9.0, AC9M2SP01)
  python3 tools/gen_au_maths_y2_shapes.py
HTML attributes use single quotes (no backslashes in the JSON). Australian English, short sentences for 7–8 year olds.

Year 2 recognises, compares and classifies 2-D shapes by the number of sides, and uses the words
“opposite”, “parallel”, “curved” and “straight”.

Pictures (checked in code):
  straight shapes  drawn from their corner points; sides = number of points; every corner is a real turn
  curved shapes    built from edges (a straight edge is 2 points, a curved edge many); straight and curved
                   sides are counted from the edges, corners from the turn where two edges meet
  parallel         every pair of sides is tested in code (cross product 0); red sides and line pairs too
Wrong answers come from real student mistakes: a turned square called a “diamond”, sides miscounted (one
missed or counted twice), an oval called a circle, only the points of a star counted, straight sides
counted as curved, every side counted as a pair of parallel sides, the other side’s length given.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
BLUE = "#1f5fa8"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]


# ------------------------------------------------------------ question helpers
def mcq(q, correct, cands, e):
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-"):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def mcq_fixed(q, choices, correct, e):
    """Choices keep their order (A B C D)."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fixed": True}


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


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


# ------------------------------------------------------------ drawing
def tw(t, fs):
    t = str(t)
    return (len(t) - t.count(" ") * 0.3 - t.count("-") * 0.3) * fs * 0.6


class Canvas:
    """Collects shapes (screen coordinates, y down), tracks the bounding box, then writes a tight SVG."""

    def __init__(self):
        self.el = []
        self.x0 = self.y0 = 1e9
        self.x1 = self.y1 = -1e9

    def grow(self, x0, y0, x1, y1):
        self.x0, self.y0 = min(self.x0, x0), min(self.y0, y0)
        self.x1, self.y1 = max(self.x1, x1), max(self.y1, y1)

    def poly(self, pts, fill, sw=2.4, col=GREEN):
        self.el.append(("p", pts, fill, sw, col))
        for x, y in pts:
            self.grow(x - sw, y - sw, x + sw, y + sw)

    def line(self, a, b, sw=2.4, col=GREEN):
        self.el.append(("l", a, b, sw, col))
        self.grow(min(a[0], b[0]) - sw, min(a[1], b[1]) - sw, max(a[0], b[0]) + sw, max(a[1], b[1]) + sw)

    def text(self, x, y, t, fs=16, col=INK):
        """Text centred on (x, y)."""
        self.el.append(("t", x, y, t, fs, col))
        w = tw(t, fs)
        self.grow(x - w / 2 - 1, y - fs * 0.62, x + w / 2 + 1, y + fs * 0.42)

    def body(self, ox, oy):
        s = []
        for e in self.el:
            if e[0] == "p":
                s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>"
                         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in e[1]), e[2], e[4], e[3]))
            elif e[0] == "l":
                _, a, b, sw, col = e
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g' stroke-linecap='round'/>"
                         % (a[0] - ox, a[1] - oy, b[0] - ox, b[1] - oy, col, sw))
            else:
                _, x, y, t, fs, col = e
                s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                         % (x - ox, y - oy + fs * 0.35, fs, col, t))
        return "".join(s)

    def size(self):
        return self.x1 - self.x0, self.y1 - self.y0

    def svg(self, label, pad=5):
        ox, oy = self.x0 - pad, self.y0 - pad
        W, H = int(math.ceil(self.x1 - ox + pad)), int(math.ceil(self.y1 - oy + pad))
        if W == H:
            W += 1                                    # keep figures out of the larger 'square' print size
        return svg_wrap(W, H, self.body(ox, oy), label)


def row_svg(cvs, caps, label, gap=24, fs=16, col=INK):
    """Pictures side by side with a caption under each."""
    H = max(cv.size()[1] for cv in cvs)
    parts, x = [], 0
    for cv, cap in zip(cvs, caps):
        w, h = cv.size()
        cw = max(w, tw(cap, fs) + 4)
        ox = cv.x0 - (x + (cw - w) / 2)
        oy = cv.y0 - (H - h) / 2
        parts.append(cv.body(ox, oy))
        if cap:
            parts.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                         % (x + cw / 2, H + 8 + fs * 0.86, fs, col, cap))
        x += cw + gap
    W = x - gap
    pad = 5
    capH = 8 + fs * 1.1 if any(caps) else 0
    body = "<g transform='translate(%d,%d)'>%s</g>" % (pad, pad, "".join(parts))
    return svg_wrap(int(math.ceil(W + 2 * pad)), int(math.ceil(H + capH + 2 * pad)), body, label)


def grid_svg(cvs, label, cell=118):
    """2 x 2 grid of pictures labelled A-D."""
    W = H = 2 * cell
    s = ["<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (cell, cell, H - 4, GRAY),
         "<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (cell, W - 4, cell, GRAY)]
    for k, cv in enumerate(cvs):
        x0, y0 = (k % 2) * cell, (k // 2) * cell
        aw, ah = cell - 26, cell - 10
        w, h = cv.size()
        assert w <= aw and h <= ah, ("too big for the grid", w, h)
        ox = cv.x0 - (x0 + 21 + (aw - w) / 2)
        oy = cv.y0 - (y0 + 5 + (ah - h) / 2)
        s.append(cv.body(ox, oy))
        s.append("<text x='%d' y='%d' font-size='18' font-weight='700' fill='%s'>%s</text>" % (x0 + 5, y0 + 22, INK, "ABCD"[k]))
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ straight-sided shapes
def reg(n, r, start=-90):
    return [(r * math.cos(math.radians(start + 360 * i / n)), r * math.sin(math.radians(start + 360 * i / n))) for i in range(n)]


def tpts(pts, deg=0, s=1.0):
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    c, si = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return [(((x - cx) * c - (y - cy) * si) * s, ((x - cx) * si + (y - cy) * c) * s) for x, y in pts]


def _cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def check_poly(pts):
    """No two sides cross, every corner is a real corner (turn of at least 25 degrees)."""
    n = len(pts)
    for i in range(n):
        a, b, c = pts[i - 1], pts[i], pts[(i + 1) % n]
        u = (b[0] - a[0], b[1] - a[1])
        v = (c[0] - b[0], c[1] - b[1])
        ang = math.degrees(math.acos(max(-1, min(1, (u[0] * v[0] + u[1] * v[1]) / math.hypot(*u) / math.hypot(*v)))))
        assert ang > 25, ("corner almost straight", pts)
    for i in range(n):
        for j in range(i + 2, n):
            if i == 0 and j == n - 1:
                continue
            p1, p2, p3, p4 = pts[i], pts[(i + 1) % n], pts[j], pts[(j + 1) % n]
            d1, d2 = _cross(p3, p4, p1), _cross(p3, p4, p2)
            d3, d4 = _cross(p1, p2, p3), _cross(p1, p2, p4)
            assert not ((d1 > 0) != (d2 > 0) and (d3 > 0) != (d4 > 0)), ("sides cross", pts)


def star(r1=46, r2=19):
    return [((r1 if i % 2 == 0 else r2) * math.cos(math.radians(-90 + 36 * i)),
             (r1 if i % 2 == 0 else r2) * math.sin(math.radians(-90 + 36 * i))) for i in range(10)]


SHAPES = {
    "tri_eq": reg(3, 42),
    "tri_right": [(0, 0), (0, 60), (80, 60)],
    "tri_thin": [(0, 0), (100, 20), (20, 45)],
    "tri_down": [(-44, -26), (44, -26), (0, 50)],
    "square": [(0, 0), (62, 0), (62, 62), (0, 62)],
    "rect": [(0, 0), (100, 0), (100, 50), (0, 50)],
    "rhombus": [(0, 0), (60, 0), (60 + 60 * math.cos(math.radians(55)), 60 * math.sin(math.radians(55))),
                (60 * math.cos(math.radians(55)), 60 * math.sin(math.radians(55)))],
    "trap": [(0, 60), (100, 60), (75, 0), (25, 0)],
    "kite": [(0, -45), (30, -10), (0, 50), (-30, -10)],
    "pent_reg": reg(5, 44),
    "pent_house": [(0, 40), (40, 0), (80, 40), (80, 100), (0, 100)],
    "pent_odd": [(0, 0), (90, 0), (110, 45), (50, 80), (0, 55)],
    "hex_reg": reg(6, 44, 0),
    "hex_L": [(0, 0), (40, 0), (40, 55), (90, 55), (90, 95), (0, 95)],
    "hex_arrow": [(0, 20), (60, 20), (60, 0), (100, 40), (60, 80), (60, 60)],
    "hept_arrow": [(-44, -14), (6, -14), (6, -38), (44, 0), (6, 38), (6, 14), (-44, 14)],
    "oct_reg": reg(8, 44, 22.5),
    "oct_cut": [(20, 0), (100, 0), (120, 20), (120, 60), (100, 80), (20, 80), (0, 60), (0, 20)],
    "cross": [(-15, -45), (15, -45), (15, -15), (45, -15), (45, 15), (15, 15), (15, 45), (-15, 45), (-15, 15),
              (-45, 15), (-45, -15), (-15, -15)],
    "star": star(),
    "dodec": reg(12, 44, 15),
}
for _p in SHAPES.values():
    check_poly(_p)


def shape(key, deg=0, s=1.0, fill=FILL):
    pts = tpts(SHAPES[key], deg, s)
    check_poly(pts)
    cv = Canvas()
    cv.poly(pts, fill, 3)
    return cv


def n_sides(key):
    return len(SHAPES[key])


def side_dirs(pts):
    n = len(pts)
    return [(pts[(i + 1) % n][0] - pts[i][0], pts[(i + 1) % n][1] - pts[i][1]) for i in range(n)]


def is_par(u, v):
    return abs(u[0] * v[1] - u[1] * v[0]) / (math.hypot(*u) * math.hypot(*v)) < 1e-6


def par_pairs(key):
    d = side_dirs(SHAPES[key])
    return sum(1 for i in range(len(d)) for j in range(i + 1, len(d)) if is_par(d[i], d[j]))


PAR_EXPECT = {"rect": 2, "square": 2, "tri_eq": 0, "hex_reg": 3, "trap": 1, "oct_reg": 4, "pent_reg": 0, "rhombus": 2,
              "kite": 0, "tri_right": 0}
for _k, _n in PAR_EXPECT.items():
    assert par_pairs(_k) == _n, (_k, par_pairs(_k))


def labelled(key, deg=0, s=1.0, labels=None, red=(), dist=13, fs=16):
    """Shape with letters (or lengths) beside its sides and some sides in red."""
    pts = tpts(SHAPES[key], deg, s)
    n = len(pts)
    cv = Canvas()
    cv.poly(pts, FILL, 3)
    cx, cy = sum(p[0] for p in pts) / n, sum(p[1] for p in pts) / n
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        if i in red:
            cv.line(a, b, sw=5, col=RED)
        if labels and labels[i]:
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            nx, ny = -(b[1] - a[1]), b[0] - a[0]
            L = math.hypot(nx, ny)
            nx, ny = nx / L, ny / L
            if nx * (mx - cx) + ny * (my - cy) < 0:
                nx, ny = -nx, -ny
            t = labels[i]
            extra = abs(nx) * tw(t, fs) / 2
            cv.text(mx + nx * (dist + extra), my + ny * dist, t, fs)
    return cv, pts


# ------------------------------------------------------------ shapes with curved sides
def arc(cx, cy, rx, ry, a0, a1, n=40):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


CURVED = {
    # each shape is a list of edges; a straight edge has 2 points, a curved edge more
    "circle": [arc(0, 0, 40, 40, 0, 360, 72)],
    "oval": [arc(0, 0, 52, 30, 0, 360, 72)],
    "semi": [arc(0, 0, 46, 46, 180, 360), [(46, 0), (-46, 0)]],
    "quarter": [[(0, 0), (60, 0)], arc(0, 0, 60, 60, 360, 270, 30), [(0, -60), (0, 0)]],
    "stadium": [[(-30, -25), (30, -25)], arc(30, 0, 25, 25, -90, 90, 30), [(30, 25), (-30, 25)], arc(-30, 0, 25, 25, 90, 270, 30)],
    "arch": [[(-30, 40), (30, 40)], [(30, 40), (30, 0)], arc(0, 0, 30, 30, 360, 180), [(-30, 0), (-30, 40)]],
    "lens": None,
    "fan": None,
}
# lens: two arcs of radius 50 (centres (0, 30) and (0, -30)) that meet at (-40, 0) and (40, 0)
CURVED["lens"] = [arc(0, 30, 50, 50, math.degrees(math.atan2(-30, -40)) + 360, math.degrees(math.atan2(-30, 40)) + 360),
                  arc(0, -30, 50, 50, math.degrees(math.atan2(30, 40)), math.degrees(math.atan2(30, -40)))]
_P = lambda a: (60 * math.cos(math.radians(a)), 50 + 60 * math.sin(math.radians(a)))
CURVED["fan"] = [[(0, 50), _P(240)], arc(0, 50, 60, 60, 240, 300, 20), [_P(300), (0, 50)]]


def _close(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1]) < 1e-6


def curved_info(key):
    """(straight sides, curved sides, corners), worked out from the edges."""
    ed = CURVED[key]
    st = sum(1 for e in ed if len(e) == 2)
    cu = len(ed) - st
    if len(ed) == 1:
        assert _close(ed[0][0], ed[0][-1])
        return st, cu, 0
    corners = 0
    for i in range(len(ed)):
        e, f = ed[i], ed[(i + 1) % len(ed)]
        assert _close(e[-1], f[0]), (key, i)
        u = (e[-1][0] - e[-2][0], e[-1][1] - e[-2][1])
        v = (f[1][0] - f[0][0], f[1][1] - f[0][1])
        ang = math.degrees(math.acos(max(-1, min(1, (u[0] * v[0] + u[1] * v[1]) / math.hypot(*u) / math.hypot(*v)))))
        corners += ang > 15
    return st, cu, corners


CURVED_EXPECT = {"circle": (0, 1, 0), "oval": (0, 1, 0), "semi": (1, 1, 2), "quarter": (2, 1, 3), "stadium": (2, 2, 0),
                 "arch": (3, 1, 2), "lens": (0, 2, 2), "fan": (2, 1, 3)}
for _k, _v in CURVED_EXPECT.items():
    assert curved_info(_k) == _v, (_k, curved_info(_k))


def curved(key, s=1.0, deg=0):
    pts = []
    for e in CURVED[key]:
        pts.extend(e[1:] if pts else e)
    if _close(pts[0], pts[-1]):
        pts = pts[:-1]
    pts = tpts(pts, deg, s)
    cv = Canvas()
    cv.poly(pts, FILL, 3)
    return cv


def circle_cv(r=40):
    cv = Canvas()
    cv.poly(arc(0, 0, r, r, 0, 360, 72)[:-1], FILL, 3)
    return cv


def oval_cv(rx=52, ry=30):
    cv = Canvas()
    cv.poly(arc(0, 0, rx, ry, 0, 360, 72)[:-1], FILL, 3)
    return cv


def pic(key, s=1.0, deg=0):
    if key == "circle":
        return circle_cv(40 * s)
    if key == "oval":
        return oval_cv(52 * s, 30 * s)
    if key in CURVED:
        return curved(key, s, deg)
    return shape(key, deg, s)


def build(key, deg, s):
    return pic(key, s, deg)


# ------------------------------------------------------------ line pairs
PAIRS = {
    "par_h": ([(0, 0), (82, 0)], [(0, 34), (82, 34)]),
    "par_v": ([(0, 0), (0, 84)], [(36, 0), (36, 84)]),
    "par_s": ([(0, 50), (60, 0)], [(24, 74), (84, 24)]),
    "meet": ([(0, 0), (41, 76)], [(82, 0), (41, 76)]),
    "cross": ([(0, 0), (82, 70)], [(0, 70), (82, 0)]),
    "closer": ([(0, 0), (82, 18)], [(0, 60), (82, 36)]),
    "apart": ([(0, 26), (40, 76)], [(40, 26), (80, 0)]),
}
PAR_LINES = {"par_h", "par_v", "par_s"}
for _k, (_a, _b) in PAIRS.items():
    _u = (_a[1][0] - _a[0][0], _a[1][1] - _a[0][1])
    _v = (_b[1][0] - _b[0][0], _b[1][1] - _b[0][1])
    assert is_par(_u, _v) == (_k in PAR_LINES), _k


def pair_cv(key):
    a, b = PAIRS[key]
    cv = Canvas()
    cv.line(*a, sw=3.5, col=BLUE)
    cv.line(*b, sw=3.5, col=BLUE)
    return cv


# ------------------------------------------------------------ set 1: name shapes by their sides
NAME_E = {
    "triangle": "It has 3 straight sides and 3 corners. It is a triangle.",
    "square": "It has 4 straight sides that are all the same length, and 4 square corners. It is a square.",
    "rectangle": "It has 4 straight sides and 4 square corners. 2 sides are long and 2 are short. It is a rectangle.",
    "pentagon": "Count the sides: 5 straight sides. It is a pentagon.",
    "hexagon": "Count the sides: 6 straight sides. It is a hexagon.",
    "octagon": "Count the sides: 8 straight sides. It is an octagon.",
}
TURNED = " Turning a shape does not change its name."
SAME_LEN = " The sides do not have to be the same length."


def set_names(rnd):
    pos = Pos(rnd)
    its = []
    asks = ["What is this shape called?", "Name this shape.", "What shape is this?"]
    rows = [
        (pic("circle", 0.95), "circle", ["oval", "sphere", "semicircle"],
         "It is round and the same width all the way round. It has no corners. It is a circle."),
        (pic("oval"), "oval", ["circle", "rectangle", "semicircle"],
         "It is round with no corners, but it is longer than it is wide. It is an oval, not a circle."),
        (shape("tri_eq"), "triangle", ["square", "pentagon", "hexagon"], NAME_E["triangle"]),
        (shape("tri_right", 160, 0.9), "triangle", ["rectangle", "pentagon", "square"], NAME_E["triangle"] + TURNED),
        (shape("square"), "square", ["rectangle", "hexagon", "triangle"], NAME_E["square"]),
        (shape("square", 45), "square", ["diamond", "rectangle", "triangle"],
         NAME_E["square"] + " It is only turned. “Diamond” is not its maths name."),
        (shape("rect"), "rectangle", ["square", "pentagon", "hexagon"], NAME_E["rectangle"]),
        (shape("rect", 90, 0.85), "rectangle", ["square", "triangle", "octagon"], NAME_E["rectangle"] + TURNED),
        (shape("pent_reg"), "pentagon", ["hexagon", "octagon", "triangle"], NAME_E["pentagon"]),
        (shape("pent_house", 0, 0.8), "pentagon", ["hexagon", "triangle", "square"], NAME_E["pentagon"] + SAME_LEN),
        (shape("hex_reg"), "hexagon", ["octagon", "pentagon", "circle"], NAME_E["hexagon"]),
        (shape("hex_L", 0, 0.85), "hexagon", ["rectangle", "octagon", "pentagon"], NAME_E["hexagon"] + SAME_LEN),
        (shape("oct_reg"), "octagon", ["hexagon", "circle", "pentagon"], NAME_E["octagon"]),
        (shape("oct_cut", 0, 0.75), "octagon", ["rectangle", "hexagon", "pentagon"],
         NAME_E["octagon"] + " Count the short sides at the corners too."),
    ]
    for i, (cv, ans, wrong, e) in enumerate(rows):
        its.append(mcq(fig(cv.svg("a 2-D shape")) + asks[i % 3], ans, wrong, e))
    grids = [
        ("Which shape is a hexagon?", "hex_L", 90, 0.8, [("pent_reg", 0, 0.8), ("oct_reg", 0, 0.8), ("square", 45, 0.85)],
         "%s has 6 straight sides, so it is a hexagon. The other shapes have 5, 8 and 4 sides."),
        ("Which shape is a square?", "square", 45, 0.95, [("rhombus", 62.5, 0.9), ("rect", 0, 0.75), ("tri_eq", 0, 0.9)],
         "%s has 4 sides that are all the same length and 4 square corners. It is a square that is turned. "
         "The other shape with 4 equal sides has no square corners, so it is not a square."),
        ("Which shape is an oval?", "oval", 0, 0.8, [("circle", 0, 0.95), ("semi", 0, 0.9), ("hex_reg", 0, 0.9)],
         "%s is round with no corners, and it is longer than it is wide. That makes it an oval. The circle is the same width all the way round."),
        ("Which shape is a pentagon?", "pent_odd", 30, 0.7, [("hex_arrow", 0, 0.8), ("square", 0, 1.0), ("tri_thin", 0, 0.8)],
         "%s has 5 straight sides, so it is a pentagon. The sides do not have to be the same length."),
    ]
    for q, key, deg, s, others, e in grids:
        p = pos.next()
        cells = [build(*o) for o in others]
        main = build(key, deg, s)
        cells.insert(p, main)
        its.append(mcq_fixed(fig(grid_svg(cells, "four 2-D shapes labelled A to D")) + q, list("ABCD"), "ABCD"[p], e % "ABCD"[p]))
    its.append(mcq("A shape has 6 straight sides. What is it called?", "hexagon", ["pentagon", "octagon", "rectangle"],
                   "6 sides make a hexagon. 5 sides make a pentagon. 8 sides make an octagon."))
    its.append(mcq("A shape has 4 straight sides. 2 sides are long and 2 are short. It has 4 square corners. What is it?",
                   "rectangle", ["square", "pentagon", "triangle"],
                   "4 sides and 4 square corners, with 2 long sides and 2 short sides: a rectangle. A square has 4 sides the same length."))
    assert len(its) == 20, len(its)
    return {"title": "Name shapes by their sides", "items": its}


# ------------------------------------------------------------ set 2: count sides and corners
def set_count(rnd):
    pos = Pos(rnd)
    its = []
    rows = [
        ("hex_arrow", 0, 0.9, "sides", None), ("pent_odd", 200, 0.85, "corners", None), ("oct_cut", 0, 0.8, "corners", None),
        ("hex_L", 180, 0.85, "sides", None), ("tri_thin", 30, 0.9, "corners", None), ("rect", 90, 0.8, "sides", None),
        ("hept_arrow", 0, 1.0, "sides", None), ("pent_house", 0, 0.8, "sides", None), ("square", 45, 0.95, "corners", None),
        ("rhombus", 0, 0.9, "corners", None), ("trap", 0, 0.9, "sides", None),
    ]
    for key, deg, s, what, _ in rows:
        n = n_sides(key)
        one = "side" if what == "sides" else "corner"
        q = fig(shape(key, deg, s).svg("a 2-D shape")) + "How many %s does this shape have?" % what
        e = ("Put your finger on one %s. Count each %s as you go round, until you get back to the start: %d %s."
             % (one, one, n, what))
        if key == "oct_cut":
            e += " Count the small corners too."
        if key in ("hex_L", "hex_arrow", "hept_arrow"):
            e += " Count the corners that point in too."
        its.append(mcq(q, n, [n - 1, n + 1, n + 2], e))
    its.append(mcq(fig(shape("star", 0, 0.95).svg("a star shape")) + "How many corners does this star have?", 10, [5, 9, 11],
                   "There are 5 corners that point out and 5 corners that point in. 5 + 5 = 10 corners. 5 only counts the points."))
    its.append(mcq(fig(shape("cross", 0, 0.9).svg("a cross shape")) + "How many sides does this shape have?", 12, [4, 11, 8],
                   "Each arm of the cross has 3 sides. There are 4 arms. 3 + 3 + 3 + 3 = 12 sides. 4 only counts the arms."))
    its.append(mcq(fig(pic("circle", 0.8).svg("a circle")) + "How many corners does a circle have?", 0, [1, 4, 2],
                   "A circle has 1 curved side and no corners. So it has 0 corners."))
    its.append(mcq(fig(pic("oval", 0.85).svg("an oval")) + "How many corners does an oval have?", 0, [2, 1, 4],
                   "An oval has 1 curved side. The ends are round, not pointed, so there are no corners. 2 counts the ends."))
    its.append(mcq("A shape has 5 corners. How many straight sides does it have?", 5, [4, 6, 10],
                   "A shape with straight sides has the same number of sides as corners. 5 corners means 5 sides."))
    its.append(mcq("How many more sides does an octagon have than a hexagon?", 2, [1, 14, 3],
                   "An octagon has 8 sides. A hexagon has 6 sides. 8 − 6 = 2 more. 14 adds them instead."))
    p = pos.next()
    cells = [shape("pent_reg", 0, 0.8), shape("tri_eq", 0, 0.9), shape("hex_reg", 0, 0.8)]
    cells.insert(p, shape("square", 45, 0.85))
    its.append(mcq_fixed(fig(grid_svg(cells, "four 2-D shapes labelled A to D")) + "Which shape has 4 corners?",
                         list("ABCD"), "ABCD"[p],
                         "%s has 4 corners. It is a square that is turned. The others have 5, 3 and 6 corners." % "ABCD"[p]))
    p = pos.next()
    cells = [shape("hex_reg", 0, 0.8), shape("pent_house", 0, 0.7), shape("rect", 0, 0.8)]
    cells.insert(p, shape("oct_cut", 0, 0.65))
    its.append(mcq_fixed(fig(grid_svg(cells, "four 2-D shapes labelled A to D")) + "Which shape has the most sides?",
                         list("ABCD"), "ABCD"[p],
                         "%s has 8 sides. The others have 6, 5 and 4 sides. 8 is the most." % "ABCD"[p]))
    p = pos.next()
    cells = [shape("pent_odd", 0, 0.7), shape("hept_arrow", 0, 0.85), shape("square", 0, 1.0)]
    cells.insert(p, shape("hex_arrow", 0, 0.8))
    its.append(mcq_fixed(fig(grid_svg(cells, "four 2-D shapes labelled A to D")) + "Which shape has 6 corners?",
                         list("ABCD"), "ABCD"[p],
                         "%s has 6 corners. Count the corners that point in too. The others have 5, 7 and 4 corners." % "ABCD"[p]))
    assert len(its) == 20, len(its)
    return {"title": "Count sides and corners", "items": its}


# ------------------------------------------------------------ set 3: curved and straight sides
def set_curved(rnd):
    pos = Pos(rnd)
    its = []

    def info(k):
        return curved_info(k)

    for key, s, deg, what in [("circle", 0.8, 0, "curved"), ("semi", 0.9, 90, "curved"), ("stadium", 0.95, 0, "curved"),
                              ("lens", 1.2, 0, "curved"), ("arch", 1.0, 0, "curved"), ("semi", 0.9, 0, "straight"),
                              ("quarter", 0.9, 0, "straight"), ("arch", 1.0, 180, "straight"), ("stadium", 0.95, 90, "straight"),
                              ("fan", 0.9, 0, "curved"), ("lens", 1.2, 90, "straight")]:
        st, cu, co = info(key)
        ans = cu if what == "curved" else st
        other = st if what == "curved" else cu
        q = fig(pic(key, s, deg).svg("a 2-D shape with curved or straight sides")) + "How many %s sides does this shape have?" % what
        e = "This shape has %d straight side%s and %d curved side%s. So it has %d %s side%s." % (
            st, "" if st == 1 else "s", cu, "" if cu == 1 else "s", ans, what, "" if ans == 1 else "s")
        if ans == 0:
            e += " Every side bends."
        its.append(mcq(q, ans, [other, st + cu, ans + 1, ans + 2, ans - 1, ans + 3], e))
    for key, s in [("semi", 0.9), ("quarter", 0.9), ("arch", 1.0)]:
        st, cu, co = info(key)
        e = "A corner is where two sides meet at a point. This shape has %d corners." % co
        if key == "arch":
            e += " At the top, the straight sides join the curve smoothly, so there is no corner there."
        if key == "semi":
            e += " They are at the two ends of the straight side."
        its.append(mcq(fig(pic(key, s).svg("a 2-D shape with a curved side")) + "How many corners does this shape have?",
                       co, [co + 1, co - 1, st + cu, 0, co + 2], e))
    for q, right, others, e in [
            ("Which shape has only straight sides?", ("hex_reg", 0.8), [("semi", 0.8), ("oval", 0.8), ("arch", 0.95)],
             "%s is a hexagon. All 6 of its sides are straight. The others have a curved side."),
            ("Which shape has only curved sides?", ("lens", 1.0), [("quarter", 0.8), ("tri_eq", 0.9), ("rect", 0.75)],
             "Both sides of %s bend. The others have straight sides."),
            ("Which shape has curved and straight sides?", ("semi", 0.8), [("circle", 0.85), ("square", 1.0), ("pent_reg", 0.8)],
             "%s has 1 curved side and 1 straight side. The circle has only a curved side. The square and pentagon have only straight sides."),
    ]:
        p = pos.next()
        cells = [pic(k, s) for k, s in others]
        cells.insert(p, pic(*right))
        its.append(mcq_fixed(fig(grid_svg(cells, "four 2-D shapes labelled A to D")) + q, list("ABCD"), "ABCD"[p], e % "ABCD"[p]))
    its.append(mcq("Which shape has 1 curved side and no straight sides?", "a circle", ["a semicircle", "a square", "a triangle"],
                   "A circle has 1 curved side all the way round. A semicircle also has 1 straight side."))
    its.append(mcq("Which shape has only straight sides?", "a triangle", ["a circle", "an oval", "a semicircle"],
                   "A triangle has 3 straight sides. A circle and an oval have a curved side. A semicircle has a curved side and a straight side."))
    its.append(mcq("A semicircle is half a circle. How many sides does it have altogether?", 2, [1, 3, 0],
                   "It has 1 curved side and 1 straight side. 1 + 1 = 2 sides. 1 forgets the straight side."))
    assert len(its) == 20, len(its)
    return {"title": "Curved and straight sides", "items": its}


# ------------------------------------------------------------ set 4: opposite and parallel sides
def set_parallel(rnd):
    pos = Pos(rnd)
    its = []
    for q, right, others, e in [
            ("Which pair of lines is parallel?", "par_h", ["meet", "cross", "closer"],
             "The lines in %s stay the same distance apart. They will never meet, even if you make them longer."),
            ("Which pair of lines is parallel?", "par_s", ["closer", "meet", "apart"],
             "The lines in %s slant the same way and stay the same distance apart. Slanted lines can be parallel too."),
            ("Which pair of lines is parallel?", "par_v", ["cross", "apart", "closer"],
             "The lines in %s go straight up and down and stay the same distance apart. So they are parallel."),
    ]:
        p = pos.next()
        cells = [pair_cv(k) for k in others]
        cells.insert(p, pair_cv(right))
        its.append(mcq_fixed(fig(grid_svg(cells, "four pairs of lines labelled A to D")) + q, list("ABCD"), "ABCD"[p], e % "ABCD"[p]))
    p = pos.next()
    cells = [pair_cv(k) for k in ["par_h", "par_s", "par_v"]]
    cells.insert(p, pair_cv("closer"))
    its.append(mcq_fixed(fig(grid_svg(cells, "four pairs of lines labelled A to D")) + "Which pair of lines is NOT parallel?",
                         list("ABCD"), "ABCD"[p],
                         "In %s the lines get closer together. If you make them longer, they will meet. So they are not parallel." % "ABCD"[p]))
    # red sides
    for q, right, others, e in [
            ("In which shape are the two red sides parallel?", ("rect", 0, 0.75, (0, 2)),
             [("tri_eq", 0, 0.9, (0, 1)), ("trap", 0, 0.8, (1, 3)), ("pent_reg", 0, 0.85, (0, 2))],
             "In %s the red sides are opposite each other and stay the same distance apart. They are parallel. "
             "In the other shapes the red sides would meet if you made them longer."),
            ("In which shape are the two red sides parallel?", ("hex_reg", 0, 0.8, (1, 4)),
             [("kite", 0, 0.85, (0, 2)), ("trap", 0, 0.8, (1, 3)), ("tri_right", 0, 0.9, (0, 1))],
             "In %s the red sides are opposite each other and point the same way. They are parallel. "
             "The red sides in the other shapes slant towards each other."),
    ]:
        p = pos.next()
        built = []
        for k, deg, s, red in others + [right]:
            d = side_dirs(tpts(SHAPES[k], deg, s))
            par = is_par(d[red[0]], d[red[1]])
            assert par == ((k, deg, s, red) == right), (k, red)
            built.append(labelled(k, deg, s, red=red)[0])
        cells = built[:3]
        cells.insert(p, built[3])
        its.append(mcq_fixed(fig(grid_svg(cells, "four 2-D shapes with red sides labelled A to D")) + q,
                             list("ABCD"), "ABCD"[p], e % "ABCD"[p]))
    # opposite sides with letters
    for key, s, ask in [("hex_reg", 1.0, 0), ("hex_reg", 1.0, 2), ("oct_reg", 1.0, 1)]:
        n = n_sides(key)
        letters = [chr(65 + i) for i in range(n)]
        cv, pts = labelled(key, 0, s, labels=letters)
        opp = (ask + n // 2) % n
        d = side_dirs(pts)
        assert is_par(d[ask], d[opp])
        wrong = [letters[(ask + n // 2 - 1) % n], letters[(ask + n // 2 + 1) % n], letters[(ask + 1) % n], letters[(ask - 1) % n]]
        e = ("Side %s is right across the shape from side %s. Opposite sides are across from each other, not next to each other."
             % (letters[opp], letters[ask]))
        if n == 6:
            e += " In this hexagon they are also parallel."
        else:
            e += " In this octagon they are also parallel."
        ch = sorted([letters[opp]] + wrong[:3])
        its.append(mcq_fixed(fig(cv.svg("a hexagon with its sides labelled with letters" if n == 6 else "an octagon with its sides labelled with letters"))
                             + "Which side is opposite side %s?" % letters[ask], ch, letters[opp], e))
    # opposite sides of a rectangle are the same length
    for L, W, which in [(9, 4, "bottom"), (7, 3, "right")]:
        k = 12
        SHAPES["_r"] = [(0, 0), (L * k, 0), (L * k, W * k), (0, W * k)]
        cv, pts = labelled("_r", 0, 1.0, labels=["%d cm" % L, "", "", "%d cm" % W], fs=16)
        del SHAPES["_r"]
        ans = L if which == "bottom" else W
        other = W if which == "bottom" else L
        e = ("The %s side is opposite the %s side. Opposite sides of a rectangle are the same length. So it is %d cm."
             % (which, "top" if which == "bottom" else "left", ans))
        its.append(mcq(fig(cv.svg("a rectangle with two side lengths")) + "This is a rectangle. How long is the %s side?" % which,
                       "%d cm" % ans, ["%d cm" % other, "%d cm" % (L + W), "%d cm" % (L - W), "%d cm" % (2 * ans)], e))
    # pairs of parallel sides
    for key, deg, s, name in [("rect", 0, 0.8, "rectangle"), ("tri_eq", 0, 0.9, "triangle"), ("hex_reg", 0, 0.85, "hexagon"),
                              ("trap", 0, 0.85, "shape"), ("oct_reg", 0, 0.85, "octagon")]:
        n = par_pairs(key)
        ns = n_sides(key)
        wrong = [ns, n + 1, n - 1, n + 2, 2 * n]
        e = {"rect": "The top and bottom are parallel. The left and right sides are parallel. That is 2 pairs. 4 counts every side.",
             "tri_eq": "Every side of a triangle slants towards the other two. If you make the sides longer, they all meet. So there are 0 pairs.",
             "hex_reg": "Each side has an opposite side that is parallel to it. 6 sides make 3 pairs. 6 counts every side.",
             "trap": "Only the top and the bottom are parallel. The two slanted sides would meet if you made them longer. So there is 1 pair.",
             "oct_reg": "Each side has an opposite side that is parallel to it. 8 sides make 4 pairs. 8 counts every side."}[key]
        its.append(mcq(fig(shape(key, deg, s).svg(("an " if name[0] in "aeiou" else "a ") + name)) + "How many pairs of parallel sides does this %s have?" % name,
                       n, wrong, e))
    p = pos.next()
    cells = [shape(k, 0, s) for k, s in [("rect", 0.75), ("hex_reg", 0.8), ("square", 1.0)]]
    cells.insert(p, shape("tri_eq", 0, 0.9))
    its.append(mcq_fixed(fig(grid_svg(cells, "four 2-D shapes labelled A to D")) + "Which shape has no parallel sides?",
                         list("ABCD"), "ABCD"[p],
                         "%s is a triangle. Its sides all slant towards each other, so none are parallel. "
                         "The rectangle, hexagon and square all have opposite sides that are parallel." % "ABCD"[p]))
    sq_cv = labelled("square", 0, 1.0, labels=["A", "B", "C", "D"])[0]
    its.append(mcq(fig(sq_cv.svg("a square with its sides labelled A to D")) +
                   "How many pairs of opposite sides does this square have?", 2, [4, 1, 3],
                   "Side A is opposite side C. Side B is opposite side D. That is 2 pairs. 4 counts every side, not pairs."))
    its.append(mcq("What are parallel lines?", "lines that stay the same distance apart",
                   ["lines that meet at a corner", "lines that cross over", "lines that are curved"],
                   "Parallel lines stay the same distance apart. They never meet, even if you make them longer."))
    its.append(mcq("Which of these has parallel lines?", "the two rails of a train track",
                   ["the hands of a clock at 3 o’clock", "the letter V", "the letter X"],
                   "The two rails of a train track stay the same distance apart, so they are parallel. "
                   "The lines in a V meet, and the lines in an X cross."))
    assert len(its) == 20, len(its)
    return {"title": "Opposite and parallel sides", "items": its}


# ------------------------------------------------------------ set 5: sort and classify; word problems
def set_problems(rnd, P):
    pos = Pos(rnd)
    its = []
    its.append(mcq(fig(labelled("oct_reg", 0, 0.8)[0].svg("a stop sign shape")) +
                   "A STOP sign is this shape. How many sides does it have?", 8, [6, 7, 10],
                   "A STOP sign is an octagon. An octagon has 8 sides and 8 corners."))
    its.append(mcq(fig(shape("tri_down", 0, 0.9).svg("a give way sign shape")) +
                   "A GIVE WAY sign is this shape. What shape is it?", "triangle", ["square", "pentagon", "octagon"],
                   "It has 3 straight sides and 3 corners, so it is a triangle. It points down, but it is still a triangle."))
    its.append(mcq(fig(shape("dodec", 0, 0.9).svg("the shape of a 50c coin")) +
                   "The Australian 50c coin has 12 straight sides. How many corners does it have?", 12, [0, 11, 6],
                   "A shape with straight sides has the same number of corners as sides. 12 sides means 12 corners. "
                   "It is not round, so 0 is wrong."))
    its.append(mcq(fig(pic("oval", 0.9).svg("the shape of a footy ground")) +
                   "Many AFL footy grounds, like the MCG, are this shape. What is it?", "oval",
                   ["circle", "rectangle", "hexagon"],
                   "It is round with no corners, and it is longer than it is wide. It is an oval. That is why we call a footy ground “the oval”."))
    its.append(mcq("A cricket pitch has 2 long sides, 2 short sides and 4 square corners. What shape is it?", "rectangle",
                   ["square", "oval", "hexagon"],
                   "4 straight sides and 4 square corners, with 2 long and 2 short sides: a rectangle. A square has 4 sides the same length."))
    n, he, his = P.next()
    its.append(mcq(fig(shape("hex_reg", 0, 0.85).svg("a hexagon")) +
                   "%s makes a hexagon with paddle-pop sticks. %s uses 1 stick for each side. How many sticks does %s use?"
                   % (n, he.capitalize(), he), 6, [5, 8, 12],
                   "A hexagon has 6 sides. 1 stick for each side means 6 sticks."))
    n, he, his = P.next()
    its.append(mcq("%s makes 2 triangles and 1 square with paddle-pop sticks. Each side is 1 stick. How many sticks does %s use?"
                   % (n, he), 10, [7, 3, 12],
                   "Each triangle has 3 sides and a square has 4. 3 + 3 + 4 = 10 sticks. 7 forgets one triangle."))
    n, he, his = P.next()
    its.append(mcq("%s draws 3 triangles. How many corners is that altogether?" % n, 9, [3, 6, 12],
                   "Each triangle has 3 corners. 3 + 3 + 3 = 9 corners."))
    n, he, his = P.next()
    its.append(mcq("%s sorts shapes. Group 1: square, triangle, hexagon. Group 2: circle, oval. What is the sorting rule?" % n,
                   "straight sides or curved sides", ["big or small", "3 sides or 4 sides", "red or blue"],
                   "Group 1 shapes have only straight sides. Group 2 shapes have a curved side. So the rule is straight or curved."))
    for q, right, others, e in [
            ("Which shape is the odd one out?", ("pent_reg", 0, 0.8), [("square", 45, 0.9), ("rect", 0, 0.75), ("rhombus", 0, 0.75)],
             "%s has 5 sides. The other three shapes all have 4 sides."),
            ("Which shape is the odd one out?", ("semi", 0, 0.8), [("tri_eq", 0, 0.9), ("hex_reg", 0, 0.8), ("square", 0, 1.0)],
             "%s has a curved side. The other three shapes have only straight sides."),
            ("Which shape is the odd one out?", ("tri_right", 0, 0.9), [("rect", 0, 0.75), ("hex_reg", 0, 0.8), ("square", 0, 1.0)],
             "%s is a triangle. It has no parallel sides. The other three shapes all have opposite sides that are parallel."),
    ]:
        p = pos.next()
        cells = [build(*o) for o in others]
        cells.insert(p, build(*right))
        its.append(mcq_fixed(fig(grid_svg(cells, "four 2-D shapes labelled A to D")) + q, list("ABCD"), "ABCD"[p], e % "ABCD"[p]))
    its.append(mcq("Which shape is the odd one out: triangle, square, circle, hexagon?", "circle",
                   ["triangle", "square", "hexagon"],
                   "A circle has a curved side and no corners. The others have straight sides and corners."))
    its.append(mcq("I have 5 straight sides and 5 corners. What shape am I?", "pentagon", ["hexagon", "octagon", "triangle"],
                   "5 sides and 5 corners make a pentagon."))
    its.append(mcq("I have 4 square corners. My opposite sides are parallel. My sides are not all the same length. What am I?",
                   "rectangle", ["square", "triangle", "oval"],
                   "A rectangle has 4 square corners and 2 pairs of parallel sides. A square would have all 4 sides the same length."))
    its.append(mcq("I have no corners. I am longer than I am wide. What shape am I?", "oval", ["circle", "rectangle", "semicircle"],
                   "No corners means only a curved side. Longer than wide means it is an oval. A circle is the same width all the way round."))
    n, he, his = P.next()
    its.append(mcq(fig(shape("oct_cut", 0, 0.7).svg("a square with its corners cut off")) +
                   "%s cuts the 4 corners off a square piece of paper with straight cuts. How many sides does the new shape have?" % n,
                   8, [4, 12, 6],
                   "Each cut makes 1 new short side. The 4 old sides are still there. 4 + 4 = 8 sides. The new shape is an octagon."))
    n, he, his = P.next()
    cv, _ = labelled("rect", 0, 0.75)
    pts = tpts(SHAPES["rect"], 0, 0.75)
    cv.line(pts[0], pts[2], sw=2.6, col=RED)
    its.append(mcq(fig(cv.svg("a rectangle with a line from corner to corner")) +
                   "%s cuts a rectangle along the red line, from corner to corner. What 2 shapes does %s get?" % (n, he),
                   "2 triangles", ["2 rectangles", "2 squares", "a triangle and a square"],
                   "Each piece has 3 straight sides and 3 corners. So %s gets 2 triangles." % he))
    n, he, his = P.next()
    its.append(mcq("%s has 5 triangles, 4 squares and 3 circles. How many of the shapes have only straight sides?" % n, 9,
                   [12, 3, 7],
                   "Triangles and squares have only straight sides. 5 + 4 = 9. Circles have a curved side, so do not count them."))
    n, he, his = P.next()
    its.append(mcq(fig(labelled("hex_reg", 0, 0.85, red=(0, 1))[0].svg("a hexagon with 2 red sides")) +
                   "%s draws a hexagon. %s colours 2 sides red. How many sides are not red?" % (n, he.capitalize()),
                   4, [2, 8, 6],
                   "A hexagon has 6 sides. 6 − 2 = 4 sides are not red. 8 adds instead of taking away."))
    assert len(its) == 20, len(its)
    return {"title": "Sort and classify: word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    flat = row_svg([pic("circle", 0.75), pic("oval", 0.65), shape("tri_eq", 0, 0.8), shape("square", 0, 0.8), shape("rect", 0, 0.65),
                    shape("pent_reg", 0, 0.75), shape("hex_reg", 0, 0.75), shape("oct_reg", 0, 0.75)],
                   ["circle", "oval", "triangle", "square", "rectangle", "pentagon", "hexagon", "octagon"],
                   "circle, oval, triangle, square, rectangle, pentagon, hexagon and octagon", gap=14, fs=14)
    turned = row_svg([shape("square", 0, 0.9), shape("square", 45, 0.9), shape("hex_reg", 0, 0.8), shape("hex_L", 0, 0.75)],
                     ["square", "still a square", "hexagon", "also a hexagon"],
                     "a square and the same square turned; a hexagon and a hexagon with sides of different lengths", gap=26, fs=14)
    curv = row_svg([pic("circle", 0.75), pic("semi", 0.8), pic("quarter", 0.8), pic("arch", 0.9)],
                   ["1 curved", "1 curved, 1 straight", "1 curved, 2 straight", "1 curved, 3 straight"],
                   "shapes with curved and straight sides", gap=18, fs=14)
    par = row_svg([pair_cv("par_h"), pair_cv("par_s"), pair_cv("closer"), pair_cv("cross")],
                  ["parallel", "parallel", "not parallel", "not parallel"],
                  "two pairs of parallel lines and two pairs that are not parallel", gap=26, fs=14)
    rect_cv = labelled("rect", 0, 0.9, labels=["A", "B", "C", "D"], red=(0, 2))[0]
    hex_cv = labelled("hex_reg", 0, 0.9, red=(1, 4))[0]
    tri_cv = labelled("tri_eq", 0, 1.0)[0]
    opp = row_svg([rect_cv, hex_cv, tri_cv], ["2 pairs", "3 pairs", "0 pairs"],
                  "a rectangle and a hexagon with a pair of opposite parallel sides in red, and a triangle with none", gap=30, fs=14)
    return (
        "<h2>Name a shape by its sides</h2>"
        "<p>A 2-D shape is <b>flat</b>. Count its <b>sides</b> to find its name. "
        "A <b>corner</b> is where two sides meet. Corners are also called <b>vertices</b>.</p>"
        "<figure class='sn-fig'>" + flat + "</figure>" +
        table(["Shape", "Sides", "Corners"], [
            ["Circle", "1 curved side (same width all the way round)", "0"], ["Oval", "1 curved side (longer than it is wide)", "0"],
            ["Triangle", "3", "3"], ["Square", "4 (all the same length)", "4"],
            ["Rectangle", "4 (2 long, 2 short)", "4"], ["Pentagon", "5", "5"], ["Hexagon", "6", "6"], ["Octagon", "8", "8"]]) +
        "<p>Turning a shape does not change its name. The sides do not have to be the same length.</p>"
        "<figure class='sn-fig'>" + turned +
        "<figcaption>A turned square is still a square, not a “diamond”. Any shape with 6 straight sides is a hexagon.</figcaption></figure>" +
        ex("Example 1", "A shape has 5 straight sides. Two sides are longer than the others. What is it?",
           "Count the sides: 5. The lengths do not matter.", "a pentagon") +
        "<p>To count sides, put your finger on one side. Count each side as you go round, until you are back where you started. "
        "Count the corners that point in too.</p>"
        "<h2>Curved and straight sides</h2>"
        "<p>A <b>straight</b> side does not bend. A <b>curved</b> side bends. Some shapes have both.</p>"
        "<figure class='sn-fig'>" + curv + "</figure>" +
        ex("Example 2", "A semicircle is half a circle. How many sides does it have?",
           "It has 1 curved side and 1 straight side. 1 + 1 = 2.", "2 sides") +
        "<h2>Opposite and parallel sides</h2>"
        "<p><b>Opposite</b> sides are across the shape from each other, not next to each other. "
        "<b>Parallel</b> lines stay the same distance apart. They never meet, even if you make them longer.</p>"
        "<figure class='sn-fig'>" + par + "</figure>"
        "<figure class='sn-fig'>" + opp +
        "<figcaption>In a rectangle, side A is opposite side C, and they are parallel (red). "
        "A hexagon has 3 pairs of parallel sides. A triangle has none.</figcaption></figure>" +
        ex("Example 3", "The top of a rectangle is 9 cm long. How long is the bottom?",
           "The bottom is opposite the top. Opposite sides of a rectangle are the same length.", "9 cm") +
        "<h2>Sort and classify</h2>"
        "<p>We can sort shapes by the number of sides, by curved or straight sides, or by parallel sides. "
        "To find the odd one out, look for the one thing that three shapes share and the fourth does not.</p>" +
        ex("Example 4", "Which is the odd one out: square, rectangle, triangle, hexagon?",
           "The square, rectangle and hexagon all have parallel sides. The triangle has none.", "triangle") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Calling a turned square a “diamond”", "Check the sides: 4 sides the same length and 4 square corners make a square"],
            ["Calling an oval a circle", "A circle is the same width all the way round. An oval is longer one way"],
            ["Missing a side, or counting one twice", "Start at one side, keep your finger on the shape and stop when you get back"],
            ["Counting only the points of a star", "Count the corners that point in too"],
            ["Thinking parallel lines must go across", "Slanted and up-and-down lines can be parallel too"],
            ["Saying a rectangle has 4 pairs of parallel sides", "A pair is 2 sides. A rectangle has 2 pairs"],
        ])
    )


FAQ = [
    {"q": "What 2-D shapes do Year 2 students learn in Australia?",
     "a": "Year 2 students name circles, ovals, triangles, squares, rectangles, pentagons, hexagons and octagons. They compare and sort them by the number of sides, curved or straight sides, and opposite and parallel sides (Australian Curriculum AC9M2SP01)."},
    {"q": "What does parallel mean in Year 2 maths?",
     "a": "Parallel lines stay the same distance apart and never meet, like the two rails of a train track. A rectangle has 2 pairs of parallel sides."},
    {"q": "Is a turned square called a diamond?",
     "a": "No. A square turned on its corner is still a square, because it still has 4 equal sides and 4 square corners. “Diamond” is an everyday word, not a maths name."},
    {"q": "What is the difference between a circle and an oval?",
     "a": "Both have 1 curved side and no corners. A circle is the same width all the way round; an oval is longer than it is wide, like a footy ground."},
]


def balance(sets, rnd):
    """Spread the correct answers exactly 5/5/5/5 over the positions. A-D picture questions keep their order."""
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
            right = it["c"][it["a"]]
            wrong = [x for i, x in enumerate(it["c"]) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        final = [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(2814)
    P = People(rnd)
    sets = [set_names(rnd), set_count(rnd), set_curved(rnd), set_parallel(rnd), set_problems(rnd, P)]
    for s in sets:
        rnd.shuffle(s["items"])
    balance(sets, rnd)
    seen_q = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1, it["q"][:80]
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen_q, it["q"]
            seen_q.add(k)
    u = {
        "country": "au", "subject": "maths", "grade": "year-2", "slug": "2d-shapes", "sort": 14,
        "updated": UPDATED, "pdf_url": "",
        "title": "2-D Shapes: Sides, Corners, Curved, Opposite and Parallel Sides",
        "seo_title": "Year 2 2-D Shapes Worksheets: Sides, Corners and Parallel Sides (Free, with Answers)",
        "short_title": "2-D shapes",
        "domain": "Space",
        "standard_code": "AC9M2SP01",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Recognise, compare and classify shapes, referencing the number of sides and using spatial terms such as “opposite”, “parallel”, “curved” and “straight”",
        "meta_desc": "Free Year 2 maths worksheets on 2-D shapes: name triangles, squares, rectangles, pentagons, hexagons, octagons, circles and ovals, count sides and corners, spot curved and straight sides, find opposite and parallel sides, and sort shapes. 100 questions with an answer key, following the Australian Curriculum.",
        "key_big": "Count the sides to name a 2-D shape. Turning a shape does not change its name.",
        "key_sub": "Sides can be straight or curved. Opposite sides are across from each other. Parallel sides stay the same distance apart and never meet.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(four [a-z0-9 -]+ labelled A to D)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
