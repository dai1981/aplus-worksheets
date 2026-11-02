# -*- coding: utf-8 -*-
"""
BC Grade 5 Math: Prisms and pyramids (BC Mathematics Curriculum, Grade 5, Geometry and measurement:
“Classification of prisms and pyramids”)
  python3 tools/gen_cabc_math_g5_prisms_pyramids.py
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.

A prism has 2 matching, parallel bases joined by rectangles; a pyramid has 1 base and triangles that
meet at a point (the apex). Both are named after the shape of the base.
  prism, n-sided base:   faces n + 2, edges 3 × n, vertices 2 × n
  pyramid, n-sided base: faces n + 1, edges 2 × n, vertices n + 1

Pictures (checked in code):
  objects  drawn from 3-D vertices and faces; a face is drawn when it faces the viewer, edges of hidden
           faces only are dashed; faces, edges and vertices come from the same data (V − E + F = 2)
           and are asserted against the rules above for every object used
  nets     regular polygons built on the edges of the rectangles / triangles, so every edge that is
           taped together has the same length; broken nets (a missing face, both bases on one side)
           are built from the same pieces
Wrong answers come from real student mistakes: calling a triangular prism a pyramid because it has
triangles, naming by the face the object sits on or by a side face (“rectangular”), naming by the number
of faces (a triangular prism has 5 faces, so “pentagonal”), counting only the faces you can see,
using the prism rule for a pyramid (and the other way round), mixing up edges and vertices,
calling a cylinder a “circular prism”.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL, BASE, SIDE, TOP3 = "#cfe6d6", "#f6dcb4", "#a9d3b6", "#e6f2e9"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]
DZX, DZY = 0.55, 0.40

POLY = {3: "triangle", 4: "rectangle", 5: "pentagon", 6: "hexagon", 7: "heptagon", 8: "octagon", 10: "decagon"}
ADJ = {3: "triangular", 4: "rectangular", 5: "pentagonal", 6: "hexagonal", 7: "heptagonal", 8: "octagonal", 10: "decagonal"}


def pname(n):
    return ADJ[n] + " prism"


def yname(n, square=True):
    return "square pyramid" if n == 4 and square else ADJ[n] + " pyramid"


def an(w):
    return ("an " if w[0] in "aeiou" else "a ") + w


def cap(s):
    return s[0].upper() + s[1:]


def fev(n):
    """faces, edges, vertices of a prism whose base has n sides"""
    return n + 2, 3 * n, 2 * n


def pyr_fev(n):
    return n + 1, 2 * n, n + 1


# ------------------------------------------------------------ question helpers
def mcq(q, correct, cands, e):
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c:
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
    assert "'" not in label
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
    return (len(t) - t.count(" ") * 0.3) * fs * 0.6


class Canvas:
    """Shapes (screen coordinates, y down); tracks the bounding box and writes a tight SVG."""

    def __init__(self):
        self.el = []
        self.polys = []
        self.x0 = self.y0 = 1e9
        self.x1 = self.y1 = -1e9

    def grow(self, x0, y0, x1, y1):
        self.x0, self.y0 = min(self.x0, x0), min(self.y0, y0)
        self.x1, self.y1 = max(self.x1, x1), max(self.y1, y1)

    def poly(self, pts, fill, sw=2.4, col=GREEN, dashed=False):
        self.el.append(("p", pts, fill, sw, col, dashed))
        self.polys.append(pts)
        for x, y in pts:
            self.grow(x - sw, y - sw, x + sw, y + sw)

    def line(self, a, b, dashed=False, sw=2.4, col=GREEN):
        self.el.append(("l", a, b, dashed, sw, col))
        self.grow(min(a[0], b[0]) - sw, min(a[1], b[1]) - sw, max(a[0], b[0]) + sw, max(a[1], b[1]) + sw)

    def pline(self, pts, dashed=False, sw=2.4, col=GREEN):
        self.el.append(("pl", pts, dashed, sw, col))
        for x, y in pts:
            self.grow(x - sw, y - sw, x + sw, y + sw)

    def body(self, ox, oy):
        s = []
        for e in self.el:
            if e[0] == "p":
                s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'%s/>"
                         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in e[1]), e[2], e[4], e[3],
                            " stroke-dasharray='6 4'" if e[5] else ""))
            elif e[0] == "l":
                _, a, b, dashed, sw, col = e
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g'%s/>"
                         % (a[0] - ox, a[1] - oy, b[0] - ox, b[1] - oy, col, sw,
                            " stroke-dasharray='5 4'" if dashed else " stroke-linecap='round'"))
            else:
                _, pts, dashed, sw, col = e
                s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='%g' stroke-linejoin='round'%s/>"
                         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in pts), col, sw,
                            " stroke-dasharray='5 4'" if dashed else " stroke-linecap='round'"))
        return "".join(s)

    def size(self):
        return self.x1 - self.x0, self.y1 - self.y0

    def svg(self, label, pad=5):
        ox, oy = self.x0 - pad, self.y0 - pad
        W, H = int(math.ceil(self.x1 - ox + pad)), int(math.ceil(self.y1 - oy + pad))
        if W == H:
            W += 1
        return svg_wrap(W, H, self.body(ox, oy), label)


def row_svg(cvs, caps, label, gap=24, fs=17, col=INK, bottom=True):
    """Pictures side by side with a caption (A, B, C, D or a word) under each."""
    H = max(cv.size()[1] for cv in cvs)
    parts, x = [], 0
    for cv, c in zip(cvs, caps):
        w, h = cv.size()
        cw = max(w, tw(c, fs) + 4)
        ox = cv.x0 - (x + (cw - w) / 2)
        oy = cv.y0 - ((H - h) if bottom else (H - h) / 2)
        parts.append(cv.body(ox, oy))
        parts.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                     % (x + cw / 2, H + 8 + fs * 0.86, fs, col, c))
        x += cw + gap
    W = x - gap
    pad = 5
    body = "<g transform='translate(%d,%d)'>%s</g>" % (pad, pad, "".join(parts))
    return svg_wrap(int(math.ceil(W + 2 * pad)), int(math.ceil(H + 8 + fs * 1.1 + 2 * pad)), body, label)


# ------------------------------------------------------------ 3-D objects
class Solid:
    def __init__(self, verts, faces):
        self.v, self.f = verts, faces
        c = [sum(p[i] for p in verts) / len(verts) for i in range(3)]
        self.normals = []
        for fc in faces:
            a, b, d = (verts[i] for i in fc[:3])
            u = [b[i] - a[i] for i in range(3)]
            w = [d[i] - a[i] for i in range(3)]
            n = [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]]
            if sum(n[i] * (a[i] - c[i]) for i in range(3)) < 0:
                n = [-x for x in n]
            self.normals.append(n)
        edges = {}
        for fi, fc in enumerate(faces):
            for i in range(len(fc)):
                e = tuple(sorted((fc[i], fc[(i + 1) % len(fc)])))
                edges.setdefault(e, []).append(fi)
        assert all(len(x) == 2 for x in edges.values())
        self.edges = edges
        F, E, V = len(faces), len(edges), len(verts)
        assert V - E + F == 2, (V, E, F)
        self.count = (F, E, V)

    def cv(self, k):
        cv = Canvas()
        view = (DZX, DZY, -1)
        vis = [sum(n[i] * view[i] for i in range(3)) > 1e-9 for n in self.normals]
        P = lambda p: ((p[0] + p[2] * DZX) * k, -(p[1] + p[2] * DZY) * k)
        for fi, fc in enumerate(self.f):
            if vis[fi]:
                n = self.normals[fi]
                L = math.sqrt(sum(x * x for x in n))
                col = TOP3 if n[1] / L > 0.6 else SIDE if n[0] / L > 0.6 else FILL
                cv.poly([P(self.v[i]) for i in fc], col, 2.4)
        for (a, b), fs in self.edges.items():
            if not any(vis[f] for f in fs):
                cv.line(P(self.v[a]), P(self.v[b]), dashed=True, sw=1.6)
        return cv


def prism_lying(base, D):
    """base: polygon in the x-y plane (the front end), pushed back by D."""
    n = len(base)
    v = [(x, y, 0) for x, y in base] + [(x, y, D) for x, y in base]
    f = [list(range(n)), list(range(n, 2 * n))]
    f += [[i, (i + 1) % n, n + (i + 1) % n, n + i] for i in range(n)]
    return Solid(v, f)


def loft(bot, top, y0, y1):
    n = len(bot)
    v = [(x, y0, z) for x, z in bot] + [(x, y1, z) for x, z in top]
    f = [list(range(n)), list(range(n, 2 * n))]
    f += [[i, (i + 1) % n, n + (i + 1) % n, n + i] for i in range(n)]
    return Solid(v, f)


def apex_solid(base, y0, apex):
    n = len(base)
    v = [(x, y0, z) for x, z in base] + [apex]
    f = [list(range(n))] + [[i, (i + 1) % n, n] for i in range(n)]
    return Solid(v, f)


def reg(n, r, start):
    return [(r * math.cos(math.radians(start + 360 * i / n)), r * math.sin(math.radians(start + 360 * i / n))) for i in range(n)]


def flat_bottom(n, r):
    return reg(n, r, -90 + 180.0 / n)


HOUSE = [(0, 0), (1.3, 0), (1.3, 0.75), (0.65, 1.25), (0, 0.75)]
LYING = {  # key: (n, solid)
    "tri": (3, lambda: prism_lying([(0, 0), (1.3, 0), (0.65, 1.05)], 1.5)),
    "rect": (4, lambda: prism_lying([(0, 0), (1.5, 0), (1.5, 0.8), (0, 0.8)], 1.1)),
    "pent": (5, lambda: prism_lying(flat_bottom(5, 0.7), 1.3)),
    "house": (5, lambda: prism_lying(HOUSE, 1.4)),
    "hex": (6, lambda: prism_lying(flat_bottom(6, 0.7), 1.3)),
    "oct": (8, lambda: prism_lying(flat_bottom(8, 0.68), 1.2)),
}
UP_BASE = {
    3: [(0, 0), (1.5, 0), (0.35, 1.4)],
    5: reg(5, 0.72, -100),
    6: reg(6, 0.72, -15),
}
PYR_BASE = {
    3: [(0, 0), (1.4, 0), (1.05, 1.2)],
    4: [(0, 0), (1.2, 0), (1.2, 1.2), (0, 1.2)],          # square
    "4r": [(0, 0), (1.7, 0), (1.7, 0.9), (0, 0.9)],       # rectangle, clearly not a square
    5: reg(5, 0.72, -100),
    6: reg(6, 0.72, -15),
}


def centre(b):
    return (sum(p[0] for p in b) / len(b), sum(p[1] for p in b) / len(b))


def up_prism(n, H=1.4):
    b = UP_BASE[n]
    return loft(b, b, 0, H)


def up_pyramid(key, H=1.45):
    b = PYR_BASE[key]
    cx, cz = centre(b)
    return apex_solid(b, 0, (cx, H, cz))


def cube():
    s = [(0, 0), (1.1, 0), (1.1, 1.1), (0, 1.1)]
    return loft(s, s, 0, 1.1)


for _key, (_n, _f) in LYING.items():
    assert _f().count == fev(_n), _key
for _n in UP_BASE:
    assert up_prism(_n).count == fev(_n), _n
for _k in PYR_BASE:
    assert up_pyramid(_k).count == pyr_fev(4 if _k == "4r" else _k), _k
assert cube().count == fev(4)


def ellipse(cx, cy, rx, ry, a0, a1, n=40):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def cylinder_cv(rx=36, ry=11, h=76):
    cv = Canvas()
    cv.poly(ellipse(0, 0, rx, ry, 180, 360) + ellipse(0, h, rx, ry, 0, 180), FILL, 0.01)
    cv.line((-rx, 0), (-rx, h))
    cv.line((rx, 0), (rx, h))
    cv.pline(ellipse(0, h, rx, ry, 0, 180))
    cv.pline(ellipse(0, h, rx, ry, 180, 360), dashed=True, sw=1.6)
    cv.poly(ellipse(0, 0, rx, ry, 0, 360)[:-1], TOP3, 2.4)
    return cv


def cone_cv(rx=38, ry=11, h=82):
    cv = Canvas()
    cv.poly([(0, 0)] + ellipse(0, h, rx, ry, 180, 0), FILL, 0.01)
    cv.poly([(0, 0)] + ellipse(0, h, rx, ry, 0, 180), FILL, 0.01)
    cv.pline([(-rx, h), (0, 0), (rx, h)])
    cv.pline(ellipse(0, h, rx, ry, 0, 180))
    cv.pline(ellipse(0, h, rx, ry, 180, 360), dashed=True, sw=1.6)
    return cv


# picture key -> (kind, n, name)
OBJ = {
    "tri": ("prism", 3, pname(3)), "rect": ("prism", 4, pname(4)), "pent": ("prism", 5, pname(5)),
    "house": ("prism", 5, pname(5)), "hex": ("prism", 6, pname(6)), "oct": ("prism", 8, pname(8)),
    "up3": ("prism", 3, pname(3)), "up5": ("prism", 5, pname(5)), "up6": ("prism", 6, pname(6)),
    "pyr3": ("pyramid", 3, yname(3)), "pyr4": ("pyramid", 4, yname(4)), "pyr4r": ("pyramid", 4, yname(4, False)),
    "pyr5": ("pyramid", 5, yname(5)), "pyr6": ("pyramid", 6, yname(6)),
    "cube": ("prism", 4, "cube"), "cyl": ("other", 0, "cylinder"), "cone": ("other", 0, "cone"),
}


def obj_cv(key, k=55):
    if key in LYING:
        return LYING[key][1]().cv(k)
    if key.startswith("up"):
        return up_prism(int(key[2:])).cv(k)
    if key.startswith("pyr"):
        kk = key[3:]
        return up_pyramid(int(kk) if kk.isdigit() else kk).cv(k)
    if key == "cube":
        return cube().cv(k)
    if key == "cyl":
        return cylinder_cv()
    if key == "cone":
        return cone_cv()
    raise KeyError(key)


def obj_svg(key):
    kind = OBJ[key][0]
    return obj_cv(key).svg("an object" if kind == "other" else "a " + kind)


def four(keys, k=40):
    cvs = []
    for key in keys:
        if key == "cyl":
            cvs.append(cylinder_cv(26, 8, 56))
        elif key == "cone":
            cvs.append(cone_cv(28, 8, 60))
        else:
            cvs.append(obj_cv(key, k))
    return row_svg(cvs, list("ABCD"), "four objects labelled A to D", gap=26)


# ------------------------------------------------------------ nets
def poly_on_edge(p, q, n, d):
    """Regular n-gon with edge p-q, built on the side of the edge that the unit vector d points to."""
    s = math.hypot(q[0] - p[0], q[1] - p[1])
    a = s / (2 * math.tan(math.pi / n))
    c = ((p[0] + q[0]) / 2 + d[0] * a, (p[1] + q[1]) / 2 + d[1] * a)
    r = math.hypot(p[0] - c[0], p[1] - c[1])
    t0 = math.atan2(p[1] - c[1], p[0] - c[0])
    for sg in (1, -1):
        pts = [(c[0] + r * math.cos(t0 + sg * 2 * math.pi * i / n), c[1] + r * math.sin(t0 + sg * 2 * math.pi * i / n)) for i in range(n)]
        if math.hypot(pts[1][0] - q[0], pts[1][1] - q[1]) < 1e-6:
            for i in range(n):                                  # every side the same length
                j = (i + 1) % n
                assert abs(math.hypot(pts[j][0] - pts[i][0], pts[j][1] - pts[i][1]) - s) < 1e-6
            return pts
    raise AssertionError("no polygon")


def prism_net_cv(n, k, L=1.7, rects=None, bases=(("top", 1), ("bot", 1))):
    """n rectangles (1 wide, L tall) side by side; a regular n-gon base on the top or bottom edge of a rectangle."""
    rects = n if rects is None else rects
    cv = Canvas()
    for i in range(rects):
        cv.poly([(i * k, 0), ((i + 1) * k, 0), ((i + 1) * k, L * k), (i * k, L * k)], FILL)
    for side, i in bases:
        assert i < rects
        if side == "top":
            pts = poly_on_edge((i * k, 0), ((i + 1) * k, 0), n, (0, -1))
        else:
            pts = poly_on_edge((i * k, L * k), ((i + 1) * k, L * k), n, (0, 1))
        cv.poly(pts, BASE)
    return cv


def box_net_cv(L, W, H, k):
    """Rectangular prism: strip L, W, L, W wide and H tall, with an L × W face above and below the first face."""
    xs = [0, L, L + W, 2 * L + W, 2 * L + 2 * W]
    cv = Canvas()
    for i in range(4):
        cv.poly([(xs[i] * k, 0), (xs[i + 1] * k, 0), (xs[i + 1] * k, H * k), (xs[i] * k, H * k)], FILL)
    cv.poly([(0, -W * k), (L * k, -W * k), (L * k, 0), (0, 0)], BASE)
    cv.poly([(0, H * k), (L * k, H * k), (L * k, (H + W) * k), (0, (H + W) * k)], BASE)
    return cv


def pyramid_net_cv(n, k, l=None, sides=None, base_col=BASE):
    """Regular n-gon base (side 1) with an isosceles triangle (height l) on each listed side.
    n = 3 with l = √3/2 gives 4 equal triangles (a triangular pyramid)."""
    base = [(x * k, -y * k) for x, y in flat_bottom(n, 0.5 / math.sin(math.pi / n))]
    a = 0.5 / math.tan(math.pi / n)
    l = 1.15 if l is None else l
    assert l > a + 0.05                                         # the triangles can fold up and meet
    cv = Canvas()
    cv.poly(base, base_col)
    cx, cy = centre(base)
    for i in (range(n) if sides is None else sides):
        p, q = base[i], base[(i + 1) % n]
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        d = math.hypot(mx - cx, my - cy)
        apex = (mx + (mx - cx) / d * l * k, my + (my - cy) / d * l * k)
        cv.poly([p, q, apex], FILL)
    return cv


TETRA_L = math.sqrt(3) / 2


def net_any(key, k):
    """Nets by key (the wrong ones are built from the same pieces)."""
    return {
        "tri": lambda: prism_net_cv(3, k, 1.7),
        "tri2": lambda: prism_net_cv(3, k, 1.7, rects=2, bases=(("top", 0), ("bot", 0))),
        "pent": lambda: prism_net_cv(5, k, 1.5, bases=(("top", 2), ("bot", 1))),
        "pent1": lambda: prism_net_cv(5, k, 1.5, bases=(("top", 2),)),
        "hex": lambda: prism_net_cv(6, k, 1.4, bases=(("top", 1), ("bot", 3))),
        "hexsame": lambda: prism_net_cv(6, k, 1.4, bases=(("top", 0), ("top", 3))),
        "box": lambda: box_net_cv(2, 1.2, 1.4, k),
        "pyr3": lambda: pyramid_net_cv(3, k * 1.6, TETRA_L),
        "pyr4": lambda: pyramid_net_cv(4, k, 1.15),
        "pyr4m": lambda: pyramid_net_cv(4, k, 1.15, sides=(0, 1, 2)),
        "pyr5": lambda: pyramid_net_cv(5, k, 1.2),
        "pyr6": lambda: pyramid_net_cv(6, k, 1.25),
    }[key]()


NET_OBJ = {"tri": pname(3), "pent": pname(5), "hex": pname(6), "box": pname(4),
           "pyr3": yname(3), "pyr4": yname(4), "pyr5": yname(5), "pyr6": yname(6)}


def net_svg(key, k=26):
    return net_any(key, k).svg("a net")


def four_nets(keys, k=18):
    return row_svg([net_any(x, k) for x in keys], list("ABCD"), "four nets labelled A to D", gap=24, bottom=False)


# ------------------------------------------------------------ set 1: prism or pyramid?
PRISM_IS = "A prism has 2 matching bases joined by rectangles. "
PYR_IS = "A pyramid has 1 base and triangles that meet at a point (the apex). "


def set_kind(rnd, pos, P):
    its = []
    Q = ["Is this object a prism or a pyramid?", "What kind of object is this?", "Which word describes this object?"]
    W4 = ["prism", "pyramid", "cylinder", "cone"]
    rows = [  # key, answer, explanation
        ("tri", "prism", PRISM_IS + "The 2 triangle ends match, and 3 rectangles join them. Triangle faces do not always mean a pyramid."),
        ("pyr4", "pyramid", PYR_IS + "The square is the base, and 4 triangles meet at the top."),
        ("up6", "prism", PRISM_IS + "The top and bottom are matching hexagons, joined by 6 rectangles."),
        ("pyr3", "pyramid", PYR_IS + "All 4 faces are triangles, and 3 of them meet at the top."),
        ("house", "prism", PRISM_IS + "The front and back are matching shapes with 5 sides, joined by rectangles. "
                           "The pointed roof does not make it a pyramid."),
        ("pyr5", "pyramid", PYR_IS + "The base has 5 sides, and 5 triangles meet at the top."),
        ("rect", "prism", PRISM_IS + "Every face is a rectangle. Any two opposite faces can be the bases."),
        ("cyl", "cylinder", "It has 2 matching circles and a curved surface, so it is a cylinder. "
                            "A prism has only flat faces, so a cylinder is not a prism."),
    ]
    for i, (key, ans, e) in enumerate(rows):
        its.append(mcq(fig(obj_svg(key)) + Q[i % 3], ans, [w for w in W4 if w != ans], e))
    its.append(mcq(fig(obj_svg("pyr6")) + "Why is this object a pyramid?", "It has 1 base and triangles that meet at a point",
                   ["It has triangle faces", "It has 2 matching bases joined by rectangles", "It has 7 faces"],
                   "The hexagon is the base, and 6 triangles meet at the apex. Having triangle faces is not enough: a triangular prism has triangles too."))
    its.append(mcq(fig(obj_svg("up3")) + "Why is this object a prism?", "It has 2 matching bases joined by rectangles",
                   ["It has triangle faces", "It has 1 base and an apex", "It has 5 faces"],
                   "The top and bottom are matching triangles, and 3 rectangles join them. A square pyramid also has 5 faces, so that is not the reason."))
    its.append(mcq("How many bases does a prism have?", 2, [1, 3, 4],
                   PRISM_IS + "1 base belongs to a pyramid."))
    its.append(mcq("How many bases does a square pyramid have?", 1, [2, 4, 5],
                   PYR_IS + "The square is the only base. The 4 triangles are side faces, and 5 is the number of faces in all."))
    its.append(mcq("In a prism, what shape are the faces that join the two bases?", "rectangles",
                   ["triangles", "the same shape as the bases", "circles"],
                   PRISM_IS + "Triangles that meet at a point belong to a pyramid."))
    its.append(mcq("In a pyramid, what shape are the faces that are not the base?", "triangles",
                   ["rectangles", "the same shape as the base", "squares"],
                   PYR_IS + "Rectangles join the bases of a prism."))
    its.append(mcq("The point at the top of a pyramid, where the triangles meet, is called the …", "apex",
                   ["base", "edge", "face"],
                   "The apex is the vertex where all the triangle faces meet. The base is the face opposite the apex."))
    its.append(mcq("Which object has an apex?", "square pyramid", ["cube", pname(3), pname(4)],
                   "Only a pyramid has triangles that meet at one point. The prisms have 2 bases and no apex."))
    n, he, his = P.next()
    its.append(mcq("%s says, “This object has triangle faces, so it must be a pyramid.” The object has 2 matching triangles joined by 3 rectangles. "
                   "Is %s right?" % (n, he), "No, it is a prism",
                   ["Yes, it is a pyramid", "No, it is a cone", "Yes, triangles always make a pyramid"],
                   PRISM_IS + "This object is a triangular prism. A pyramid has only 1 base, and its triangles meet at a point."))
    its.append(mcq("An object has 1 hexagon face and 6 triangle faces that meet at a point. What kind of object is it?", "pyramid",
                   ["prism", "cylinder", "cone"],
                   PYR_IS + "The hexagon is the base, so it is a hexagonal pyramid."))
    p = pos.next()
    keys = ["tri", "rect", "up6"]
    keys.insert(p, "pyr5")
    its.append(mcq_fixed(fig(four(keys)) + "Which object is a pyramid?", list("ABCD"), "ABCD"[p],
                         "%s has 1 base and triangles that meet at a point. The other objects have 2 matching bases joined by rectangles, so they are prisms." % "ABCD"[p]))
    p = pos.next()
    keys = ["pyr4", "cone", "pyr3"]
    keys.insert(p, "up5")
    its.append(mcq_fixed(fig(four(keys)) + "Which object is a prism?", list("ABCD"), "ABCD"[p],
                         "%s has 2 matching pentagon bases joined by rectangles. The others come to a point: two pyramids and a cone." % "ABCD"[p]))
    assert len(its) == 20, len(its)
    return {"title": "Prism or pyramid?", "items": its}


# ------------------------------------------------------------ set 2: name it by its base
NAME_E = "Prisms and pyramids are named after the shape of the base. "


def set_name(rnd, pos):
    its = []
    ASK = ["Name this object.", "What is the name of this object?", "Which name is correct for this object?"]
    rows = [  # key, answer, wrong, explanation
        ("tri", pname(3), [pname(4), yname(3), pname(5)],
         "The 2 matching ends are triangles, so it is a triangular prism. It lies on a rectangle, but that face is not a base. "
         "Do not use its 5 faces: that would give “pentagonal”."),
        ("rect", pname(4), [yname(4, False), pname(6), "cube"],
         "The bases are rectangles, so it is a rectangular prism. It has 6 faces, but “hexagonal” would mean hexagon bases. "
         "It is not a cube, because its faces are not all squares."),
        ("pent", pname(5), [yname(5), pname(7), pname(4)],
         "Count the sides of an end: 5 sides, so it is a pentagonal prism. 7 is its number of faces."),
        ("house", pname(5), [pname(3), pname(4), yname(5)],
         "The end looks like a house: a square with a triangle on top. Count its sides: 5. So it is a pentagonal prism, not a triangular prism."),
        ("hex", pname(6), [yname(6), pname(8), pname(4)],
         "Each end has 6 sides, so it is a hexagonal prism. 8 is its number of faces, and the rectangles are only the side faces."),
        ("up5", pname(5), [yname(5), pname(7), pname(4)],
         "This prism stands on a base. The top and bottom are matching pentagons, so it is a pentagonal prism."),
        ("oct", pname(8), [pname(10), yname(8), pname(4)],
         "Each end has 8 sides, so it is an octagonal prism. 10 is its number of faces."),
        ("pyr3", yname(3), [pname(3), yname(4), yname(4, False)],
         "The base is a triangle, so it is a triangular pyramid. All 4 faces are triangles. "
         "Do not name it by its 4 faces: that would give a 4-sided base."),
        ("pyr4", yname(4), [yname(3), "square prism", yname(5)],
         "The base is a square, so it is a square pyramid. Do not name it by its triangle side faces or by its 5 faces."),
        ("pyr4r", yname(4, False), [yname(3), pname(4), yname(5)],
         "The base is a long rectangle, so it is a rectangular pyramid. The triangles are side faces, so they do not name it."),
        ("pyr5", yname(5), [yname(6), pname(5), yname(3)],
         "The base has 5 sides, so it is a pentagonal pyramid. 6 is its number of faces."),
        ("pyr6", yname(6), [yname(7), pname(6), yname(3)],
         "The base has 6 sides, so it is a hexagonal pyramid. 7 is its number of faces."),
    ]
    for i, (key, ans, wrong, e) in enumerate(rows):
        its.append(mcq(fig(obj_svg(key)) + ASK[i % 3], ans, wrong, NAME_E + e))
    its.append(mcq("Which face do you use to name a prism or a pyramid?", "the base",
                   ["the face it sits on", "a side face", "the biggest face"],
                   NAME_E + "A prism can lie on a rectangle, but its bases are still the 2 matching ends."))
    its.append(mcq("A pyramid has a base with 5 sides. What is its name?", yname(5), [yname(6), pname(5), yname(3)],
                   NAME_E + "5 sides make a pentagon, so it is a pentagonal pyramid."))
    its.append(mcq("The bases of a prism are hexagons. What is its name?", pname(6), [yname(6), pname(8), pname(4)],
                   NAME_E + "Hexagon bases make a hexagonal prism. The side faces are rectangles, but they do not name it."))
    its.append(mcq("What shape is each base of a triangular prism?", "triangle", ["rectangle", "square", "pentagon"],
                   NAME_E + "A triangular prism has 2 triangle bases. Its 3 side faces are rectangles."))
    its.append(mcq("An object has 1 rectangle base and 4 triangles that meet at a point. What is its name?", yname(4, False),
                   [pname(4), yname(3), yname(5)],
                   NAME_E + "1 base and triangles make a pyramid, and the base is a rectangle: a rectangular pyramid."))
    its.append(mcq("A cube is a special kind of which prism?", pname(4), [pname(6), yname(4), pname(3)],
                   "A cube has square bases joined by squares, and a square is a special rectangle. So a cube is a rectangular prism. "
                   "Its 6 faces do not make it “hexagonal”."))
    p = pos.next()
    keys = ["pyr3", "rect", "pyr5"]
    keys.insert(p, "pyr4")
    its.append(mcq_fixed(fig(four(keys)) + "Which object is a square pyramid?", list("ABCD"), "ABCD"[p],
                         "%s has a square base and 4 triangles that meet at a point. The others are a triangular pyramid, "
                         "a rectangular prism and a pentagonal pyramid." % "ABCD"[p]))
    p = pos.next()
    keys = ["hex", "pyr5", "tri"]
    keys.insert(p, "pent")
    its.append(mcq_fixed(fig(four(keys)) + "Which object is a pentagonal prism?", list("ABCD"), "ABCD"[p],
                         "%s has 2 matching pentagon ends joined by rectangles. The others are a hexagonal prism, a pentagonal pyramid "
                         "and a triangular prism." % "ABCD"[p]))
    assert len(its) == 20, len(its)
    return {"title": "Name it by its base", "items": its}


# ------------------------------------------------------------ set 3: faces, edges and vertices
def prism_e(n):
    F, E, V = fev(n)
    return ("%s has %d faces (2 %ss + %d rectangles), %d edges (%d + %d + %d) and %d vertices (%d + %d)."
            % (cap(an(pname(n))), F, POLY[n], n, E, n, n, n, V, n, n))


def pyr_e(n):
    F, E, V = pyr_fev(n)
    nm = yname(n)
    return ("%s has %d faces (1 %s + %d triangles), %d edges (%d round the base + %d up to the apex) and %d vertices (%d + 1 apex)."
            % (cap(an(nm)), F, "square" if n == 4 else POLY[n], n, E, n, n, V, n))


def set_fev(rnd):
    its = []
    D = " Dashed lines show edges at the back that you cannot see."
    rows = [  # kind, n, what, wrong, picture key, extra
        ("prism", 3, "faces", [3, 6, 9], "tri", " You can see only 3 faces, but the bottom and the back end count too."),
        ("prism", 3, "edges", [6, 5, 12], None, " 3 edges round each end and 3 joining the ends."),
        ("prism", 3, "vertices", [3, 5, 9], "up3", ""),
        ("prism", 4, "edges", [8, 6, 4], "rect", D),
        ("prism", 5, "faces", [5, 6, 10], "pent", D),
        ("prism", 5, "vertices", [5, 15, 6], None, ""),
        ("prism", 6, "edges", [12, 8, 6], "hex", " Do not forget the 6 edges that join the two ends."),
        ("prism", 6, "vertices", [6, 7, 18], None, ""),
        ("pyramid", 4, "faces", [4, 6, 8], "pyr4", " Do not forget the square base on the bottom."),
        ("pyramid", 4, "edges", [4, 5, 12], None, ""),
        ("pyramid", 4, "vertices", [4, 8, 6], None, " Do not forget the apex."),
        ("pyramid", 3, "faces", [3, 5, 6], "pyr3", D),
        ("pyramid", 5, "edges", [5, 15, 6], "pyr5", D),
        ("pyramid", 6, "vertices", [6, 12, 8], "pyr6", ""),
        ("pyramid", 6, "faces", [6, 8, 12], None, " 8 would be a hexagonal prism."),
    ]
    for kind, n, what, wrong, key, extra in rows:
        nm = pname(n) if kind == "prism" else yname(n)
        ans = dict(zip(("faces", "edges", "vertices"), fev(n) if kind == "prism" else pyr_fev(n)))[what]
        assert ans not in wrong
        if key:
            q = fig(obj_svg(key)) + "This is %s. How many %s does it have?" % (an(nm), what)
        else:
            q = "How many %s does %s have?" % (what, an(nm))
        its.append(mcq(q, ans, wrong, (prism_e(n) if kind == "prism" else pyr_e(n)) + extra))
    assert pyr_fev(5)[0] == 6
    its.append(mcq("A pyramid has 6 faces. What is its name?", yname(5), [yname(6), yname(4), pname(5)],
                   "Faces of a pyramid = the base + 1 triangle for each side of the base. 6 − 1 = 5 sides, so the base is a pentagon. "
                   "(Square pyramid uses the prism rule, 6 − 2 = 4.)"))
    assert fev(6)[2] == 12
    its.append(mcq("A prism has 12 vertices. What is its name?", pname(6), [pname(10), pname(4), yname(6)],
                   "Half the vertices are on each base: 12 ÷ 2 = 6, so the bases are hexagons. "
                   "(Decagonal uses the faces rule, 12 − 2, and rectangular uses the edges rule, 12 ÷ 3.)"))
    assert fev(3)[1] == 9 and pyr_fev(4)[1] == 8
    its.append(mcq("Which has more edges, a triangular prism or a square pyramid?", "the triangular prism, by 1",
                   ["the square pyramid, by 1", "they have the same number", "the triangular prism, by 3"],
                   "Triangular prism: 3 + 3 + 3 = 9 edges. Square pyramid: 4 round the base + 4 up to the apex = 8 edges. 9 − 8 = 1."))
    assert fev(3)[2] == 6 and pyr_fev(4)[2] == 5
    its.append(mcq("A triangular prism and a square pyramid both have 5 faces. What else is true?",
                   "The prism has 6 vertices and the pyramid has 5",
                   ["They have the same number of vertices", "The prism has 5 vertices and the pyramid has 6", "The pyramid has more edges"],
                   "Triangular prism: 9 edges, 6 vertices. Square pyramid: 8 edges, 5 vertices."))
    its.append(mcq("What is an edge?", "a line where two faces meet",
                   ["a corner where edges meet", "a flat surface", "the face an object sits on"],
                   "An edge is a line segment where two faces meet. A corner is a vertex, and a flat surface is a face."))
    assert len(its) == 20, len(its)
    return {"title": "Faces, edges and vertices", "items": its}


# ------------------------------------------------------------ set 4: nets
NET_ASK = ["Which object does this net fold into?", "This net is folded up. What object does it make?",
           "What object can be made from this net?"]


def set_nets(rnd, pos, P):
    its = []
    rows = [  # net key, k, wrong, explanation
        ("tri", 26, [yname(3), pname(4), pname(5)],
         "There are 2 triangles and 3 rectangles. The triangles are the matching ends, so it folds into a triangular prism."),
        ("pyr4", 28, [yname(3), pname(4), yname(5)],
         "There is 1 square and 4 triangles. The triangles fold up and meet at a point, so it is a square pyramid."),
        ("pent", 24, [yname(5), pname(7), pname(4)],
         "There are 2 pentagons and 5 rectangles. The pentagons are the matching ends, so it is a pentagonal prism."),
        ("pyr6", 22, [pname(6), yname(7), yname(3)],
         "There is 1 hexagon and 6 triangles that meet at a point, so it is a hexagonal pyramid."),
        ("pyr3", 30, [yname(4), pname(3), "it cannot fold into an object"],
         "There are 4 matching triangles. One is the base, and the other 3 fold up and meet at a point: a triangular pyramid."),
        ("box", 24, ["cube", pname(6), yname(4, False)],
         "There are 6 rectangles in 3 matching pairs, so it folds into a rectangular prism. It is not a cube, because the faces are not all squares."),
        ("pyr5", 24, [yname(6), pname(5), yname(3)],
         "There is 1 pentagon and 5 triangles that meet at a point, so it is a pentagonal pyramid. 6 is its number of faces."),
        ("hex", 22, [yname(6), pname(8), pname(4)],
         "There are 2 hexagons and 6 rectangles. The hexagons are the matching ends, so it is a hexagonal prism."),
    ]
    for i, (key, k, wrong, e) in enumerate(rows):
        its.append(mcq(fig(net_svg(key, k)) + NET_ASK[i % 3], NET_OBJ[key], wrong, e))
    its.append(mcq(fig(net_svg("pent1", 24)) + "This net of a pentagonal prism is missing one face. Which shape is missing?", "a pentagon",
                   ["a rectangle", "a triangle", "a square"],
                   "A pentagonal prism has 2 pentagons and 5 rectangles. The net has all 5 rectangles but only 1 pentagon."))
    its.append(mcq(fig(net_svg("pyr4m", 28)) + "This net of a square pyramid is missing one face. Which shape is missing?", "a triangle",
                   ["a square", "a rectangle", "a pentagon"],
                   "A square pyramid has 1 square and 4 triangles. The net has only 3 triangles, so one side of the square has nothing to fold up."))
    its.append(mcq(fig(net_svg("hexsame", 18)) + "Why will this NOT fold into a hexagonal prism?", "Both hexagons fold onto the same end",
                   ["It needs a third hexagon", "It has too many rectangles", "The rectangles should be triangles"],
                   "Both hexagons are on the top edge, so they fold onto the same end and the other end stays open. "
                   "One hexagon must be on the top edge and one on the bottom edge."))
    its.append(mcq("A net has 2 pentagons and 5 rectangles. Which object does it fold into?", pname(5),
                   [yname(5), pname(7), pname(4)],
                   "2 matching pentagons joined by rectangles make a pentagonal prism. 7 is the number of faces."))
    its.append(mcq("A net has 1 hexagon and 6 triangles. Which object does it fold into?", yname(6),
                   [pname(6), yname(7), yname(3)],
                   "1 base and triangles make a pyramid. The base is a hexagon, so it is a hexagonal pyramid."))
    its.append(mcq("How many triangles are in the net of a square pyramid?", 4, [5, 8, 2],
                   "1 square base + 4 triangles, one on each side of the square. 5 is the number of faces in all."))
    its.append(mcq("How many rectangles are in the net of a hexagonal prism?", 6, [8, 2, 12],
                   "1 rectangle for each side of the hexagon: 6. With the 2 hexagons there are 8 faces in all."))
    its.append(mcq("The net of a pyramid has 5 triangles and 1 other shape. What is the other shape?", "pentagon",
                   ["triangle", "hexagon", "rectangle"],
                   "There is 1 triangle for each side of the base, so the base has 5 sides: a pentagon. "
                   "(Hexagon counts all 6 faces.)"))
    n, he, his = P.next()
    its.append(mcq("%s cuts out a net with 2 triangles and 3 rectangles and says it makes a triangular pyramid. What does it really make?" % n,
                   pname(3), [yname(4), pname(5), yname(5)],
                   "2 matching triangles joined by rectangles make a triangular prism. A triangular pyramid’s net has 4 triangles and no rectangles."))
    its.append(mcq("A net has 4 matching triangles and no other shapes. What does it fold into?", yname(3),
                   [yname(4), pname(3), "it cannot fold into an object"],
                   "One triangle is the base and the other 3 fold up and meet at a point, so it makes a triangular pyramid."))
    p = pos.next()
    keys = ["tri", "pyr4m", "pyr5"]
    keys.insert(p, "pyr4")
    its.append(mcq_fixed(fig(four_nets(keys)) + "Which net folds into a square pyramid?", list("ABCD"), "ABCD"[p],
                         "%s has 1 square and 4 triangles. One other net has only 3 triangles, one makes a triangular prism "
                         "and one makes a pentagonal pyramid." % "ABCD"[p]))
    p = pos.next()
    keys = ["pyr3", "tri2", "pyr4"]
    keys.insert(p, "tri")
    its.append(mcq_fixed(fig(four_nets(keys)) + "Which net folds into a triangular prism?", list("ABCD"), "ABCD"[p],
                         "%s has 2 triangles and 3 rectangles. One net has only 2 rectangles, so it cannot close up; "
                         "the others make a triangular pyramid and a square pyramid." % "ABCD"[p]))
    assert len(its) == 20, len(its)
    return {"title": "Nets of prisms and pyramids", "items": its}


# ------------------------------------------------------------ set 5: real objects
def set_real(rnd, P):
    its = []
    n, he, his = P.next()
    its.append(mcq("On a camping trip on Vancouver Island, %s’s tent has 2 triangle ends, 2 sloping sides and a rectangle floor. "
                   "What object is the tent shaped like?" % n, pname(3), [yname(3), pname(4), pname(5)],
                   "2 matching triangle ends joined by 3 rectangles (2 sides and the floor) make a triangular prism. Do not use its 5 faces to name it."))
    n, he, his = P.next()
    its.append(mcq("%s’s family rents an A-frame cabin near Whistler. Its front and back walls are triangles, and the two sloping roof sides go "
                   "down to the ground. Counting the floor, how many faces does the cabin have?" % n, 5, [3, 6, 4],
                   "The cabin is a triangular prism: 2 triangles + 3 rectangles (2 roof sides and the floor) = 5 faces."))
    n, he, his = P.next()
    its.append(mcq("%s’s pencil is a hexagonal prism. How many long flat faces run down its side (not counting the ends)?" % n,
                   6, [8, 3, 12],
                   "A hexagon has 6 sides, so there are 6 rectangles along the pencil. 8 counts the 2 ends as well, and 3 is how many you can see at once."))
    n, he, his = P.next()
    its.append(mcq("A cereal box is a rectangular prism. %s puts a sticker on every corner. How many stickers does %s need?" % (n, he),
                   8, [6, 12, 4],
                   "A rectangular prism has 8 vertices: 4 on the top and 4 on the bottom. 6 is the number of faces and 12 the number of edges."))
    its.append(mcq("A gazebo in a park has a roof shaped like a hexagonal pyramid with no base. How many triangle panels make the roof?",
                   6, [7, 12, 8],
                   "A hexagonal pyramid has 1 triangle for each side of the hexagon: 6 triangles. 7 counts the base too, and 12 is the number of edges."))
    n, he, his = P.next()
    its.append(mcq("%s builds the frame of a square pyramid with straws, one straw for each edge. How many straws does %s need?" % (n, he),
                   8, [5, 4, 12],
                   "4 straws round the square base + 4 up to the apex = 8. 5 is the number of faces (and of vertices)."))
    n, he, his = P.next()
    its.append(mcq("%s joins straws with balls of modelling clay at every corner of a triangular prism. How many balls of clay does %s need?" % (n, he),
                   6, [9, 5, 3],
                   "One ball for each vertex: 3 on each triangle end, 3 + 3 = 6. 9 is the number of edges."))
    n, he, his = P.next()
    its.append(mcq("%s builds a birdhouse. The front and back are shaped like a house (a square with a triangle roof on top) and are joined by rectangles. "
                   "What object is the birdhouse?" % n, pname(5), [pname(3), pname(4), yname(5)],
                   "The house shape has 5 sides, so the birdhouse is a pentagonal prism."))
    its.append(mcq("In science class, a glass prism has 2 triangle ends. How many of its faces are rectangles?", 3, [2, 5, 6],
                   "A triangular prism has 2 triangles and 3 rectangles, one rectangle for each side of the triangle."))
    n, he, his = P.next()
    its.append(mcq("%s’s tea bag is shaped like a pyramid with 4 faces, all triangles. What is its name?" % n, yname(3),
                   [yname(4), pname(3), yname(4, False)],
                   "4 triangle faces: 1 triangle base and 3 triangles that meet at a point. That is a triangular pyramid."))
    its.append(mcq("A hockey puck has 2 matching circle faces. Is it a prism?", "No, it is a cylinder with a curved surface",
                   ["Yes, it is a circular prism", "Yes, it has 2 matching bases", "No, it is a cone"],
                   "A prism has only flat faces and polygon bases. A hockey puck has a curved surface, so it is a cylinder, not a prism."))
    n, he, his = P.next()
    its.append(mcq("%s builds a cedar planter box shaped like a rectangular prism with no top. How many wooden faces does it have?" % n,
                   5, [6, 4, 8],
                   "A rectangular prism has 6 faces. With no top, there are 6 − 1 = 5: the bottom and 4 sides."))
    n, he, his = P.next()
    its.append(mcq("%s polishes every face of a glass paperweight shaped like a square pyramid. How many faces does %s polish?" % (n, he),
                   5, [4, 8, 6],
                   "1 square base + 4 triangles = 5 faces. 4 forgets the base, and 8 is the number of edges."))
    n, he, his = P.next()
    its.append(mcq("%s sands every face of a wooden block shaped like an octagonal prism. How many faces does %s sand?" % (n, he),
                   10, [8, 9, 16],
                   "2 octagon ends + 8 rectangles = 10 faces. 9 would be an octagonal pyramid, and 16 is the number of vertices."))
    n, he, his = P.next()
    assert 12 * 15 == 180
    its.append(mcq("%s puts tape along every edge of a cube-shaped gift box. Each edge is 15 cm long. How much tape does %s use?" % (n, he),
                   "180 cm", ["90 cm", "120 cm", "60 cm"],
                   "A cube has 12 edges: 12 × 15 = 180 cm. 90 cm uses the 6 faces, 120 cm the 8 vertices and 60 cm only 4 edges."))
    n, he, his = P.next()
    s, L = 4, 20
    tot = 6 * s + 3 * L
    assert tot == 84
    its.append(mcq("A chocolate box is a triangular prism. Each triangle end has 3 sides of %d cm, and the box is %d cm long. "
                   "%s glues ribbon along every edge. How much ribbon is that?" % (s, L, n),
                   "%d cm" % tot, ["%d cm" % (3 * s + 3 * L), "%d cm" % (6 * s + L), "%d cm" % (6 * s + 2 * L)],
                   "Edges round the two ends: 6 × %d = %d cm. Three long edges: 3 × %d = %d cm. Total: %d + %d = %d cm."
                   % (s, 6 * s, L, 3 * L, 6 * s, 3 * L, tot)))
    n, he, his = P.next()
    a = fev(5)[1] + pyr_fev(5)[1]
    assert a == 25
    its.append(mcq("%s makes the frames of a pentagonal prism and a pentagonal pyramid from straws, one straw for each edge. How many straws altogether?" % n,
                   a, [30, 20, 16],
                   "Prism: 5 + 5 + 5 = 15 edges. Pyramid: 5 round the base + 5 up to the apex = 10. 15 + 10 = 25. "
                   "(30 counts the prism twice, and 16 adds the vertices, 10 + 6.)"))
    n, he, his = P.next()
    its.append(mcq("%s stacks 10 matching hexagon tiles exactly on top of each other. What object does the stack look like?" % n,
                   pname(6), [yname(6), "hexagon", "cylinder"],
                   "Every layer is the same hexagon, so the top and bottom are matching hexagons joined by rectangles: a hexagonal prism."))
    n, he, his = P.next()
    its.append(mcq("%s’s tent has a square floor and 4 triangle walls that meet at the top of one pole. What object is the tent shaped like?" % n,
                   yname(4), [pname(3), "cube", "cone"],
                   "1 square base and 4 triangles that meet at a point make a square pyramid."))
    n, he, his = P.next()
    a = fev(3)[2] + pyr_fev(4)[2]
    assert a == 11
    its.append(mcq("%s builds a triangular prism and a square pyramid from toothpicks, with a marshmallow at every corner. "
                   "How many marshmallows does %s use in all?" % (n, he), a, [17, 10, 12],
                   "Triangular prism: 6 vertices. Square pyramid: 4 + 1 apex = 5 vertices. 6 + 5 = 11. (17 counts the edges, 9 + 8.)"))
    assert len(its) == 20, len(its)
    return {"title": "Real objects: tents, boxes and more", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    prisms = row_svg([LYING[k][1]().cv(36) for k in ("tri", "rect", "pent", "hex")],
                     [pname(3), pname(4), pname(5), pname(6)], "a triangular, rectangular, pentagonal and hexagonal prism",
                     gap=22, fs=14)
    pyrs = row_svg([up_pyramid(k).cv(40) for k in (3, 4, 5, 6)],
                   [yname(3), yname(4), yname(5), yname(6)], "a triangular, square, pentagonal and hexagonal pyramid",
                   gap=22, fs=14)
    nets = row_svg([net_any("tri", 20), net_any("pyr4", 22), net_any("pent", 17)],
                   ["triangular prism", "square pyramid", "pentagonal prism"],
                   "nets of a triangular prism, a square pyramid and a pentagonal prism", gap=34, fs=14, bottom=False)
    return (
        "<h2>Prism or pyramid?</h2>"
        "<p>A <b>prism</b> has <b>2 matching bases</b> that face each other. Rectangles join them.</p>"
        "<p>A <b>pyramid</b> has <b>1 base</b>. Its other faces are <b>triangles</b> that meet at one point, the <b>apex</b>.</p>"
        "<h2>Name it by its base</h2>"
        "<p>Look at the base and count its sides. That shape gives the name: a triangle base makes a <b>triangular</b> prism or pyramid.</p>"
        "<figure class='sn-fig'>" + prisms +
        "<figcaption>Prisms: the two matching ends are the bases. A prism can lie on a rectangle, but the rectangle is not a base.</figcaption></figure>"
        "<figure class='sn-fig'>" + pyrs +
        "<figcaption>Pyramids: the base is on the bottom, and the triangles meet at the apex.</figcaption></figure>" +
        ex("Example 1", "An object has 2 matching pentagons joined by 5 rectangles. What is it?",
           "2 matching bases joined by rectangles: a prism. The bases have 5 sides: pentagons.", "a pentagonal prism") +
        ex("Example 2", "An object has 1 square and 4 triangles that meet at a point. What is it?",
           "1 base and triangles: a pyramid. The base is a square.", "a square pyramid") +
        "<h2>Faces, edges and vertices</h2>"
        "<p>A <b>face</b> is a flat surface. An <b>edge</b> is where two faces meet. A <b>vertex</b> is a corner.</p>" +
        table(["Object", "Faces", "Edges", "Vertices"],
              [[cap(pname(n))] + [str(x) for x in fev(n)] for n in (3, 4, 5, 6)] +
              [[cap(yname(n))] + [str(x) for x in pyr_fev(n)] for n in (3, 4, 5, 6)]) +
        ex("Example 3", "How many edges does a hexagonal pyramid have?",
           "6 edges round the base + 6 edges up to the apex: 6 + 6.", "12 edges") +
        "<h2>Nets</h2>"
        "<p>A <b>net</b> is a flat pattern that folds up into the object. A prism’s net has 2 bases and a rectangle for each side of the base. "
        "A pyramid’s net has 1 base and a triangle on each side of it.</p>"
        "<figure class='sn-fig'>" + nets + "</figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Calling a triangular prism a pyramid because it has triangles", "Count the bases: 2 matching bases means a prism"],
            ["Naming a prism by the face it sits on or by a side face", "Find the 2 matching ends: they are the bases"],
            ["Naming by the number of faces (a triangular prism has 5 faces, but it is not “pentagonal”)", "Count the sides of the base"],
            ["Counting only the faces you can see", "Count the hidden faces at the back and the bottom too"],
            ["Forgetting the apex when counting a pyramid’s vertices", "Vertices = the corners of the base + 1"],
            ["Calling a cylinder a “circular prism”", "A cylinder has a curved surface, so it is not a prism"],
        ])
    )


FAQ = [
    {"q": "What do Grade 5 students learn about prisms and pyramids in BC?",
     "a": "The BC Grade 5 math curriculum includes the classification of prisms and pyramids. Students tell prisms from pyramids, name them by their base, count faces, edges and vertices, and match them to their nets."},
    {"q": "How do you name a prism or a pyramid?",
     "a": "Use the shape of the base. A prism with triangle bases is a triangular prism, and a pyramid with a square base is a square pyramid. Do not use the side faces or the number of faces."},
    {"q": "What is the difference between a prism and a pyramid?",
     "a": "A prism has 2 matching bases joined by rectangles. A pyramid has 1 base, and its other faces are triangles that meet at a point called the apex."},
    {"q": "How many faces, edges and vertices does a square pyramid have?",
     "a": "A square pyramid has 5 faces (1 square and 4 triangles), 8 edges and 5 vertices. A triangular prism also has 5 faces, but it has 9 edges and 6 vertices."},
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
    rnd = random.Random(55813)
    P = People(rnd)
    pos = Pos(rnd)
    sets = [set_kind(rnd, pos, P), set_name(rnd, pos), set_fev(rnd), set_nets(rnd, pos, P), set_real(rnd, P)]
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
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-5", "slug": "prisms-and-pyramids", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 5 Prisms and Pyramids",
        "seo_title": "Grade 5 Prisms and Pyramids Worksheets: Faces, Edges, Vertices and Nets (Free, BC Curriculum, Answer Key)",
        "short_title": "Prisms and pyramids",
        "domain": "Geometry and measurement",
        "standard_code": "Grade 5: Geometry and measurement",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/5/core",
        "standard_text": "Classification of prisms and pyramids",
        "meta_desc": "Free Grade 5 math worksheets on prisms and pyramids for the BC curriculum: tell a prism from a pyramid, name each one by its base, "
                     "count faces, edges and vertices, match nets, and solve problems with tents, boxes and straw frames. 100 questions with an answer key.",
        "key_big": "A prism has 2 matching bases joined by rectangles. A pyramid has 1 base and triangles that meet at a point.",
        "key_sub": "Name both by the shape of the base: 2 triangle bases make a triangular prism, and a square base with 4 triangles makes a square pyramid. "
                   "Do not name an object by the face it sits on or by its number of faces.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "four [a-z]+ labelled A to D")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
