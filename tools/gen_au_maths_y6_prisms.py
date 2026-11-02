# -*- coding: utf-8 -*-
"""
Australia Year 6 Maths: Prisms and cross-sections (Australian Curriculum v9.0, AC9M6SP01)
  python3 tools/gen_au_maths_y6_prisms.py
HTML attributes use single quotes (no backslashes in the JSON). Australian English.

Year 6 students Compare the parallel cross-sections of objects and recognise their relationships
to right prisms: a right prism has the same cross-section all along its length (its two ends), and
it is named after that shape. Pyramids and cones have cross-sections that shrink towards the apex;
a cylinder keeps the same circle but is not a prism (its ends are circles and it has a curved surface).

Pictures (checked in code):
  objects   drawn from 3-D vertices and faces; a face is drawn when it faces the viewer, edges of
            hidden faces only are dashed; faces, edges and vertices come from the same data
            (V − E + F = 2) and are asserted against n + 2, 3n, 2n for every prism used
  cuts      the object is really cut at a height: the lower piece keeps its base and gets the cut
            face (red), the upper piece is lifted off. Prisms: the cut face is the base polygon;
            pyramids: the base scaled towards the apex; cylinders/cones: circles (same / smaller)
Wrong answers come from real student mistakes: naming a prism by its number of faces, calling a
pyramid a prism, calling a cylinder a “circular prism”, saying a cone’s cross-section is a triangle,
counting only the faces you can see, forgetting the long edges (2n edges), mixing edges and vertices,
using the pyramid rule (n + 1 faces).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL, SIDE, TOP3 = "#cfe6d6", "#a9d3b6", "#e6f2e9"
CUTF = "#f3b9b0"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]
DZX, DZY = 0.55, 0.40

POLY = {3: "triangle", 4: "rectangle", 5: "pentagon", 6: "hexagon", 7: "heptagon", 8: "octagon", 9: "nonagon", 10: "decagon"}
ADJ = {3: "triangular", 4: "rectangular", 5: "pentagonal", 6: "hexagonal", 7: "heptagonal", 8: "octagonal", 9: "nonagonal", 10: "decagonal"}


def pname(n):
    return ADJ[n] + " prism"


def an(w):
    """a / an + word"""
    return ("an " if w[0] in "aeiou" else "a ") + w


def fev(n):
    """faces, edges, vertices of a prism whose cross-section has n sides"""
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
        self.x0 = self.y0 = 1e9
        self.x1 = self.y1 = -1e9

    def grow(self, x0, y0, x1, y1):
        self.x0, self.y0 = min(self.x0, x0), min(self.y0, y0)
        self.x1, self.y1 = max(self.x1, x1), max(self.y1, y1)

    def poly(self, pts, fill, sw=2.4, col=GREEN, dashed=False):
        self.el.append(("p", pts, fill, sw, col, dashed))
        for x, y in pts:
            self.grow(x - sw, y - sw, x + sw, y + sw)

    def circle(self, c, r, fill=FILL, sw=2.4, col=GREEN):
        self.el.append(("c", c, r, fill, sw, col))
        self.grow(c[0] - r - sw, c[1] - r - sw, c[0] + r + sw, c[1] + r + sw)

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
            elif e[0] == "c":
                _, c, r, fill, sw, col = e
                s.append("<circle cx='%.1f' cy='%.1f' r='%g' fill='%s' stroke='%s' stroke-width='%g'/>"
                         % (c[0] - ox, c[1] - oy, r, fill, col, sw))
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


def row_svg(cvs, caps, label, gap=24, fs=17, col=INK):
    """Pictures side by side with a caption (A, B, C, D or a word) under each."""
    H = max(cv.size()[1] for cv in cvs)
    parts, x = [], 0
    for cv, cap in zip(cvs, caps):
        w, h = cv.size()
        cw = max(w, tw(cap, fs) + 4)
        ox = cv.x0 - (x + (cw - w) / 2)
        oy = cv.y0 - (H - h)                                  # objects stand on one line
        parts.append(cv.body(ox, oy))
        parts.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                     % (x + cw / 2, H + 8 + fs * 0.86, fs, col, cap))
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

    def draw(self, cv, k, red=(), lift=0.0):
        view = (DZX, DZY, -1)
        vis = [sum(n[i] * view[i] for i in range(3)) > 1e-9 for n in self.normals]
        P = lambda p: ((p[0] + p[2] * DZX) * k, -(p[1] + lift + p[2] * DZY) * k)
        for fi, fc in enumerate(self.f):
            if vis[fi]:
                n = self.normals[fi]
                L = math.sqrt(sum(x * x for x in n))
                if fi in red:
                    cv.poly([P(self.v[i]) for i in fc], CUTF, 2.6, RED)
                    continue
                col = TOP3 if n[1] / L > 0.6 else SIDE if n[0] / L > 0.6 else FILL
                cv.poly([P(self.v[i]) for i in fc], col, 2.4)
        for (a, b), fs in self.edges.items():
            if not any(vis[f] for f in fs):
                cv.line(P(self.v[a]), P(self.v[b]), dashed=True, sw=1.6)
        return cv

    def cv(self, k):
        return self.draw(Canvas(), k)


def prism_lying(base, D):
    """base: polygon in the x-y plane (the front end), pushed back by D."""
    n = len(base)
    v = [(x, y, 0) for x, y in base] + [(x, y, D) for x, y in base]
    f = [list(range(n)), list(range(n, 2 * n))]
    f += [[i, (i + 1) % n, n + (i + 1) % n, n + i] for i in range(n)]
    return Solid(v, f)


def loft(bot, top, y0, y1):
    """bottom polygon (x, z) at height y0 and top polygon at y1 (same number of corners). Face 1 is the top."""
    n = len(bot)
    v = [(x, y0, z) for x, z in bot] + [(x, y1, z) for x, z in top]
    f = [list(range(n)), list(range(n, 2 * n))]
    f += [[i, (i + 1) % n, n + (i + 1) % n, n + i] for i in range(n)]
    return Solid(v, f)


def apex_solid(base, y0, apex):
    """pyramid: base polygon (x, z) at height y0, apex (x, y, z)."""
    n = len(base)
    v = [(x, y0, z) for x, z in base] + [apex]
    f = [list(range(n))] + [[i, (i + 1) % n, n] for i in range(n)]
    return Solid(v, f)


def reg(n, r, start):
    return [(r * math.cos(math.radians(start + 360 * i / n)), r * math.sin(math.radians(start + 360 * i / n))) for i in range(n)]


def flat_bottom(n, r):
    """regular polygon in the x-y plane standing on one side"""
    return reg(n, r, -90 + 180.0 / n)


HOUSE = [(0, 0), (1.3, 0), (1.3, 0.75), (0.65, 1.25), (0, 0.75)]
RIGHT_TRI = [(0, 0), (1.2, 0), (1.2, 0.9)]

LYING = {  # key: (n, solid)
    "tri": (3, lambda: prism_lying([(0, 0), (1.3, 0), (0.65, 1.05)], 1.5)),
    "rtri": (3, lambda: prism_lying(RIGHT_TRI, 1.6)),
    "rect": (4, lambda: prism_lying([(0, 0), (1.5, 0), (1.5, 0.8), (0, 0.8)], 1.1)),
    "sqend": (4, lambda: prism_lying([(0, 0), (0.75, 0), (0.75, 0.75), (0, 0.75)], 1.9)),
    "pent": (5, lambda: prism_lying(flat_bottom(5, 0.7), 1.3)),
    "house": (5, lambda: prism_lying(HOUSE, 1.4)),
    "hex": (6, lambda: prism_lying(flat_bottom(6, 0.7), 1.3)),
    "oct": (8, lambda: prism_lying(flat_bottom(8, 0.68), 1.2)),
}
UP_BASE = {  # bases in the x-z plane for upright objects
    3: [(0, 0), (1.5, 0), (0.35, 1.4)],
    4: [(0, 0), (1.4, 0), (1.4, 0.8), (0, 0.8)],
    5: reg(5, 0.72, -100),
    6: reg(6, 0.72, -15),
    8: reg(8, 0.7, -10),
}
for _key, (_n, _f) in LYING.items():
    assert _f().count == fev(_n), _key
for _n, _b in UP_BASE.items():
    assert loft(_b, _b, 0, 1).count == fev(_n), _n
    assert apex_solid(_b, 0, (0.5, 1, 0.4)).count == pyr_fev(_n), _n


PYR_BASE = dict(UP_BASE)
PYR_BASE[4] = [(0, 0), (1.2, 0), (1.2, 1.2), (0, 1.2)]      # a square base
PYR_BASE[3] = [(0, 0), (1.4, 0), (1.05, 1.2)]      # turned so that two side faces show
for _n, _b in PYR_BASE.items():
    assert apex_solid(_b, 0, (0.5, 1, 0.4)).count == pyr_fev(_n), _n


def centre(b):
    return (sum(p[0] for p in b) / len(b), sum(p[1] for p in b) / len(b))


def up_prism(n, H=1.4):
    b = UP_BASE[n]
    return loft(b, b, 0, H)


def up_pyramid(n, H=1.45):
    b = PYR_BASE[n]
    cx, cz = centre(b)
    return apex_solid(b, 0, (cx, H, cz))


def cube():
    s = [(0, 0), (1.1, 0), (1.1, 1.1), (0, 1.1)]
    return loft(s, s, 0, 1.1)


def ellipse(cx, cy, rx, ry, a0, a1, n=40):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def cyl_piece(cv, rx, ry, yt, yb, top_red=False):
    """upright cylinder between screen heights yt (top) and yb (bottom)"""
    cv.poly(ellipse(0, yt, rx, ry, 180, 360) + ellipse(0, yb, rx, ry, 0, 180), FILL, 0.01)
    cv.line((-rx, yt), (-rx, yb))
    cv.line((rx, yt), (rx, yb))
    cv.pline(ellipse(0, yb, rx, ry, 0, 180))
    cv.pline(ellipse(0, yb, rx, ry, 180, 360), dashed=True, sw=1.6)
    if top_red:
        cv.poly(ellipse(0, yt, rx, ry, 0, 360)[:-1], CUTF, 2.6, RED)
    else:
        cv.poly(ellipse(0, yt, rx, ry, 0, 360)[:-1], TOP3, 2.4)


def cylinder_cv(rx=36, ry=11, h=76):
    cv = Canvas()
    cyl_piece(cv, rx, ry, 0, h)
    return cv


def cone_cv(rx=38, ry=11, h=82):
    cv = Canvas()
    cv.poly([(0, 0)] + ellipse(0, h, rx, ry, 180, 0), FILL, 0.01)
    cv.poly([(0, 0)] + ellipse(0, h, rx, ry, 0, 180), FILL, 0.01)
    cv.pline([(-rx, h), (0, 0), (rx, h)])
    cv.pline(ellipse(0, h, rx, ry, 0, 180))
    cv.pline(ellipse(0, h, rx, ry, 180, 360), dashed=True, sw=1.6)
    return cv


def sphere_cv(r=40):
    cv = Canvas()
    cv.circle((0, 0), r)
    cv.pline(ellipse(0, 0, r, r * 0.3, 0, 180), sw=1.6)
    cv.pline(ellipse(0, 0, r, r * 0.3, 180, 360), dashed=True, sw=1.2)
    return cv


# ------------------------------------------------------------ cut pictures (cut parallel to the base)
def gap_for(base):
    depth = max(p[1] for p in base) - min(p[1] for p in base)
    return depth * DZY + 0.35


def cut_prism_cv(n, k=55, H=1.4, t=0.55):
    """Upright prism cut at height t·H: the top piece is lifted off, the cut face (red) is the base shape."""
    b = UP_BASE[n]
    h = H * t
    cv = Canvas()
    loft(b, b, h, H).draw(cv, k, lift=gap_for(b))
    low = loft(b, b, 0, h)
    low.draw(cv, k, red=(1,))
    return cv


def cut_pyramid_cv(n, k=55, H=1.45, t=0.45):
    b = PYR_BASE[n]
    cx, cz = centre(b)
    h = H * t
    mid = [(x + (cx - x) * t, z + (cz - z) * t) for x, z in b]       # the base scaled towards the apex
    cv = Canvas()
    apex_solid(mid, h, (cx, H, cz)).draw(cv, k, lift=gap_for(b))
    loft(b, mid, 0, h).draw(cv, k, red=(1,))
    return cv


def cut_cylinder_cv(rx=36, ry=11, h=80, t=0.5, gap=34):
    cv = Canvas()
    yc = h * (1 - t)
    cyl_piece(cv, rx, ry, -gap, yc - gap)
    cyl_piece(cv, rx, ry, yc, h, top_red=True)
    return cv


def cut_cone_cv(rx=40, ry=12, h=86, t=0.45, gap=30):
    """cut at height t·h above the base: the cut circle has radius (1 − t)·rx"""
    cv = Canvas()
    yc = h * (1 - t)                       # screen y of the cut (apex at 0, base at h)
    r2, ry2 = rx * (1 - t), ry * (1 - t)
    cv.poly([(0, -gap)] + ellipse(0, yc - gap, r2, ry2, 180, 0), FILL, 0.01)
    cv.poly([(0, -gap)] + ellipse(0, yc - gap, r2, ry2, 0, 180), FILL, 0.01)
    cv.pline([(-r2, yc - gap), (0, -gap), (r2, yc - gap)])
    cv.pline(ellipse(0, yc - gap, r2, ry2, 0, 180))
    cv.pline(ellipse(0, yc - gap, r2, ry2, 180, 360), dashed=True, sw=1.6)
    cv.poly(ellipse(0, yc, r2, ry2, 180, 360) + ellipse(0, h, rx, ry, 0, 180), FILL, 0.01)
    cv.line((-r2, yc), (-rx, h))
    cv.line((r2, yc), (rx, h))
    cv.pline(ellipse(0, h, rx, ry, 0, 180))
    cv.pline(ellipse(0, h, rx, ry, 180, 360), dashed=True, sw=1.6)
    cv.poly(ellipse(0, yc, r2, ry2, 0, 360)[:-1], CUTF, 2.6, RED)
    return cv


def obj_cv(key, k=55):
    """any object by key"""
    if key in LYING:
        return LYING[key][1]().cv(k)
    if key.startswith("up"):
        return up_prism(int(key[2:])).cv(k)
    if key.startswith("pyr"):
        return up_pyramid(int(key[3:])).cv(k)
    if key == "cube":
        return cube().cv(k)
    if key == "cyl":
        return cylinder_cv()
    if key == "cone":
        return cone_cv()
    if key == "sphere":
        return sphere_cv()
    raise KeyError(key)


def obj_svg(key, label):
    return obj_cv(key).svg(label)


def four(keys, label, k=40):
    cvs = []
    for key in keys:
        if key in ("cyl", "cone", "sphere"):
            cvs.append({"cyl": lambda: cylinder_cv(26, 8, 56), "cone": lambda: cone_cv(28, 8, 60), "sphere": lambda: sphere_cv(29)}[key]())
        else:
            cvs.append(obj_cv(key, k))
    return row_svg(cvs, list("ABCD"), label, gap=26)


# ------------------------------------------------------------ set 1: name the prism
NAME_E = "A prism is named after its cross-section, the shape of its two matching ends. "


def set_name(rnd, pos):
    its = []
    ASK = ["Name this prism.", "What is the name of this prism?", "This object is a prism. What is its name?"]
    rows = [  # picture key, answer, wrong, explanation
        ("tri", pname(3), ["triangular pyramid", pname(5), pname(4)],
         "The two ends are triangles, so it is a triangular prism. Do not name it by its 5 faces: that would give “pentagonal”."),
        ("rtri", pname(3), [pname(4), "triangular pyramid", "square-based pyramid"],
         "The ends are right-angled triangles. They are still triangles, so it is a triangular prism."),
        ("rect", pname(4), ["cube", "hexagonal prism", "rectangular pyramid"],
         "The ends are rectangles, so it is a rectangular prism. It has 6 faces, but “hexagonal” would mean the ends are hexagons."),
        ("sqend", pname(4), ["cube", "square-based pyramid", pname(8)],
         "The ends are squares and the long faces are rectangles, so it is a rectangular prism (also called a square prism). "
         "It is not a cube, because not all its faces are squares."),
        ("pent", pname(5), [pname(7), pname(6), "pentagonal pyramid"],
         "Count the sides of an end: 5 sides, so it is a pentagonal prism. 7 is its number of faces."),
        ("house", pname(5), [pname(3), pname(4), "pentagonal pyramid"],
         "The end looks like a house: a square with a triangle on top. Count its sides: 5. So it is a pentagonal prism, not a triangular prism."),
        ("hex", pname(6), [pname(8), pname(5), "hexagonal pyramid"],
         "Each end has 6 sides, so it is a hexagonal prism. 8 is its number of faces."),
        ("oct", pname(8), [pname(10), pname(6), "octagonal pyramid"],
         "Each end has 8 sides, so it is an octagonal prism. 10 is its number of faces."),
        ("up3", pname(3), [pname(5), "triangular pyramid", pname(4)],
         "This prism stands on one of its ends. The top and bottom are triangles, so it is a triangular prism."),
        ("up6", pname(6), ["hexagonal pyramid", pname(8), pname(4)],
         "The top and bottom are matching hexagons joined by rectangles, so it is a hexagonal prism."),
    ]
    for i, (key, ans, wrong, e) in enumerate(rows):
        its.append(mcq(fig(obj_svg(key, "a prism")) + ASK[i % 3], ans, wrong, NAME_E + e))
    for n, wrong in [(5, ["rectangle", "hexagon", "triangle"]), (3, ["rectangle", "pentagon", "square"]),
                     (8, ["rectangle", "hexagon", "decagon"])]:
        its.append(mcq("What shape is the cross-section of %s?" % an(pname(n)), POLY[n], wrong,
                       NAME_E + "%s has %s ends, so every cross-section parallel to the ends is %s. "
                       "The side faces are rectangles, but they do not give the prism its name." % (an(pname(n)).capitalize(), POLY[n], an(POLY[n]))))
    its.append(mcq("A prism has a cross-section that is a hexagon. What is its name?", pname(6),
                   ["hexagonal pyramid", pname(8), pname(5)], NAME_E + "A hexagon cross-section gives a hexagonal prism."))
    its.append(mcq("A prism has a cross-section with 7 sides (a heptagon). What is its name?", pname(7),
                   ["heptagonal pyramid", pname(9), pname(6)],
                   NAME_E + "7 sides make a heptagon, so it is a heptagonal prism. 9 would be its number of faces."))
    its.append(mcq("A prism is named after the shape of its …", "cross-section (its two ends)",
                   ["biggest face", "number of faces", "side faces"],
                   "Every slice of a prism parallel to its ends is the same shape. That shape names the prism: triangle → triangular prism."))
    its.append(mcq("In a right prism, what shape are the faces that join the two ends?", "rectangles",
                   ["triangles", "the same shape as the ends", "circles"],
                   "In a right prism the ends are joined by rectangles. Triangles that meet at a point belong to a pyramid."))
    its.append(mcq("A cube is a prism. What shape is its cross-section?", "square", ["hexagon", "octagon", "triangle"],
                   "Any slice of a cube parallel to a face is a square. (Hexagon would come from its 6 faces, octagon from its 8 vertices.)"))
    p = pos.next()
    keys = ["pent", "pyr6", "oct"]
    keys.insert(p, "hex")
    its.append(mcq_fixed(fig(four(keys, "four objects labelled A to D")) + "Which object is a hexagonal prism?", list("ABCD"), "ABCD"[p],
                         "%s has two matching hexagon ends (6 sides) joined by rectangles. The others are a pentagonal prism, "
                         "a hexagonal pyramid and an octagonal prism." % "ABCD"[p]))
    p = pos.next()
    keys = ["pyr3", "pyr4", "rect"]
    keys.insert(p, "tri")
    its.append(mcq_fixed(fig(four(keys, "four objects labelled A to D")) + "Which object is a triangular prism?", list("ABCD"), "ABCD"[p],
                         "%s has two matching triangle ends joined by rectangles. The pyramids have triangles that meet at a point." % "ABCD"[p]))
    assert len(its) == 20, len(its)
    return {"title": "Name the prism by its cross-section", "items": its}


# ------------------------------------------------------------ set 2: prism or not?
def set_which(rnd, pos, P):
    its = []
    Q = "Is this object a prism?"
    rows = [
        ("pyr4", "No, it is a square-based pyramid", ["Yes, it is a square prism", "Yes, it is a triangular prism", "No, it is a cone"],
         "It has 1 square base and 4 triangles that meet at a point. Its cross-sections get smaller towards the top, so it is a pyramid, not a prism."),
        ("pyr3", "No, it is a triangular pyramid", ["Yes, it is a triangular prism", "Yes, it is a rectangular prism", "No, it is a cone"],
         "All 4 faces are triangles and 3 of them meet at a point. A triangular prism has 2 triangles joined by 3 rectangles."),
        ("cyl", "No, its ends are circles and it has a curved surface", ["Yes, it is a circular prism", "No, it is a cone", "Yes, it is a rectangular prism"],
         "Every slice of a cylinder parallel to its ends is the same circle, but a prism has only flat faces and its ends are polygons. So a cylinder is not a prism."),
        ("cone", "No, it is a cone", ["Yes, it is a triangular prism", "Yes, it is a circular prism", "No, it is a cylinder"],
         "A cone has 1 circle base and a curved surface that comes to a point. It only looks like a triangle from the side."),
        ("up6", "Yes, it is a hexagonal prism", ["No, it is a hexagonal pyramid", "Yes, it is an octagonal prism", "No, prisms must lie down"],
         "It has two matching hexagons joined by rectangles. A prism is still a prism when it stands on its end."),
        ("sphere", "No, it has no flat faces", ["Yes, it is a circular prism", "No, it is a cylinder", "Yes, every slice is a circle"],
         "A sphere has one curved surface and no flat faces. Its slices are circles of different sizes, so it is not a prism."),
        ("pyr6", "No, it is a hexagonal pyramid", ["Yes, it is a hexagonal prism", "Yes, it is a heptagonal prism", "No, it is a cone"],
         "It has 1 hexagon base and 6 triangles that meet at a point, so it is a hexagonal pyramid. (7 faces does not make it heptagonal.)"),
        ("house", "Yes, it is a pentagonal prism", ["No, it has a triangle on top", "Yes, it is a triangular prism", "No, it is a pyramid"],
         "Its two ends are matching pentagons (a square with a triangle on top has 5 sides), joined by rectangles. So it is a pentagonal prism."),
        ("cube", "Yes, it is a prism with a square cross-section", ["No, a cube is not a prism", "No, it is a pyramid", "Yes, it is a hexagonal prism"],
         "A cube has two matching square ends joined by squares (special rectangles). Every slice parallel to a face is the same square, so a cube is a prism."),
    ]
    for key, ans, wrong, e in rows:
        its.append(mcq(fig(obj_svg(key, "an object")) + Q, ans, wrong, e))
    its.append(mcq("Which object is NOT a prism?", "square-based pyramid", [pname(3), "cube", pname(6)],
                   "A square-based pyramid has 1 base and triangles that meet at a point. The others have two matching ends joined by rectangles."))
    its.append(mcq("Which object is a prism?", pname(5), ["pentagonal pyramid", "cone", "cylinder"],
                   "A pentagonal prism has two matching pentagon ends joined by 5 rectangles. A cylinder has a curved surface, so it is not a prism."))
    its.append(mcq("Why is a square-based pyramid not a prism?", "Its cross-sections get smaller towards the top",
                   ["It has a square face", "It has 5 faces", "It has triangle faces"],
                   "A prism has the same cross-section all the way along. A pyramid’s slices shrink to a point. "
                   "A triangular prism also has triangle faces and 5 faces, so those are not the reason."))
    its.append(mcq("Why is a cylinder not a prism?", "Its ends are circles and it has a curved surface",
                   ["Its cross-sections change size", "It has no flat faces", "It has only 1 flat face"],
                   "A cylinder keeps the same circle all the way along, but a prism must have polygon ends and only flat faces. "
                   "A cylinder has 2 flat circle faces and 1 curved surface."))
    its.append(mcq("Which is true about every prism?", "It has two matching, parallel ends joined by rectangles",
                   ["It has one base and triangles that meet at a point", "It has a curved surface", "It has 6 faces"],
                   "That is what makes a right prism. One base with triangles meeting at a point describes a pyramid."))
    its.append(mcq("Which is true about every pyramid?", "It has one base and triangles that meet at a point",
                   ["It has two matching ends", "Its cross-sections are all the same size", "Its base is always a square"],
                   "A pyramid has one base (any polygon) and triangle faces that meet at the apex. Its base can be a triangle, square, pentagon and so on."))
    n, he, his = P.next()
    its.append(mcq("%s says, “This object has triangle faces, so it is a triangular prism.” The object has 1 square face and 4 triangle faces. "
                   "Is %s right?" % (n, he), "No, it is a square-based pyramid",
                   ["Yes, it is a triangular prism", "No, it is a cube", "No, it is a rectangular prism"],
                   "4 triangles that meet at a point on a square base make a square-based pyramid. A triangular prism has 2 triangles and 3 rectangles."))
    its.append(mcq("How many of these objects are prisms? cube, cone, triangular prism, cylinder, square-based pyramid, hexagonal prism", 3,
                   [4, 2, 5],
                   "The prisms are the cube, the triangular prism and the hexagonal prism: 3. "
                   "The cone and the pyramid get smaller to a point, and the cylinder has a curved surface."))
    its.append(mcq("Which object has the same cross-section all along its length but is NOT a prism?", "cylinder",
                   ["cone", "cube", "hexagonal pyramid"],
                   "Every slice of a cylinder is the same circle, but it is not a prism because it has a curved surface and circle ends. A cube is a prism."))
    p = pos.next()
    keys = ["pyr4", "cone", "cyl"]
    keys.insert(p, "pent")
    its.append(mcq_fixed(fig(four(keys, "four objects labelled A to D")) + "Which object is a prism?", list("ABCD"), "ABCD"[p],
                         "%s has two matching pentagon ends joined by rectangles, so it is a pentagonal prism. "
                         "The pyramid and the cone come to a point, and the cylinder has a curved surface." % "ABCD"[p]))
    p = pos.next()
    keys = ["up3", "cube", "hex"]
    keys.insert(p, "pyr6")
    its.append(mcq_fixed(fig(four(keys, "four objects labelled A to D")) + "Which object is NOT a prism?", list("ABCD"), "ABCD"[p],
                         "%s is a hexagonal pyramid: its triangles meet at a point. The others are a triangular prism, a cube and a hexagonal prism." % "ABCD"[p]))
    assert len(its) == 20, len(its)
    return {"title": "Prism or not a prism?", "items": its}


# ------------------------------------------------------------ set 3: cross-sections parallel to the base
CUTQ = "This object is cut parallel to its base. The red face shows the cut. "


def set_cut(rnd, pos, P):
    its = []
    for n, wrong, extra in [(3, ["rectangle", "square", "pentagon"], ""),
                            (4, ["triangle", "trapezium", "hexagon"], ""),
                            (6, ["rectangle", "octagon", "pentagon"], ""),
                            (5, ["rectangle", "hexagon", "triangle"], "")]:
        its.append(mcq(fig(cut_prism_cv(n).svg("a prism cut parallel to its base")) + CUTQ + "What shape is the cross-section?",
                       POLY[n], wrong,
                       "The object is a %s. Every cut parallel to its base is the same shape as the base: a %s.%s" % (pname(n), POLY[n], extra)))
    its.append(mcq(fig(cut_pyramid_cv(4).svg("a pyramid cut parallel to its base")) + CUTQ + "What is the cross-section?",
                   "a square, smaller than the base",
                   ["a triangle", "a square the same size as the base", "a pentagon"],
                   "A cut parallel to the base of a square-based pyramid is a square. The cut is nearer the apex, so the square is smaller than the base. "
                   "The triangles are the side faces, not the cross-section."))
    its.append(mcq(fig(cut_pyramid_cv(3).svg("a pyramid cut parallel to its base")) + CUTQ + "What is the cross-section?",
                   "a triangle, smaller than the base",
                   ["a triangle the same size as the base", "a square", "a rectangle"],
                   "The base is a triangle, so a cut parallel to the base is also a triangle. In a pyramid it gets smaller the closer you cut to the apex."))
    its.append(mcq(fig(cut_cone_cv().svg("a cone cut parallel to its base")) + CUTQ + "What is the cross-section?",
                   "a circle, smaller than the base",
                   ["a triangle", "a circle the same size as the base", "a square"],
                   "A cut parallel to the base of a cone is a circle. It is smaller than the base because the cone narrows to a point. "
                   "A triangle comes from cutting straight down through the point, not parallel to the base."))
    its.append(mcq(fig(cut_cylinder_cv().svg("a cylinder cut parallel to its base")) + CUTQ + "What is the cross-section?",
                   "a circle the same size as the ends",
                   ["a rectangle", "a smaller circle", "an oval"],
                   "Every cut of a cylinder parallel to its ends is the same circle. It looks like an oval only because we see it at an angle."))
    its.append(mcq("Which object has every cross-section parallel to its base the same shape and size?", pname(3),
                   ["square-based pyramid", "cone", "sphere"],
                   "A prism has the same cross-section all the way along. Pyramids and cones get smaller towards the point, and a sphere’s circles change size."))
    its.append(mcq("When you cut a pyramid parallel to its base, the cross-sections …",
                   "are the same shape as the base but get smaller towards the apex",
                   ["are all the same size as the base", "are always triangles", "get bigger towards the apex"],
                   "Each slice is a smaller copy of the base. At the apex it shrinks to a point."))
    its.append(mcq("When you cut a prism parallel to its ends, every cross-section is …", "the same shape and size as the ends",
                   ["smaller than the ends", "a rectangle", "a triangle"],
                   "That is what makes a prism: it has the same cross-section all along its length."))
    its.append(mcq("Every cut parallel to the base of an object is the same hexagon. What is the object?", pname(6),
                   ["hexagonal pyramid", "cylinder", pname(8)],
                   "The same hexagon all the way along means a hexagonal prism. In a hexagonal pyramid the hexagons get smaller."))
    its.append(mcq("Every cut parallel to the base of an object is a circle of the same size. What is the object?", "cylinder",
                   ["cone", "sphere", pname(6)],
                   "A cylinder has the same circle all the way along. A cone’s circles get smaller, and a sphere’s circles grow and then shrink."))
    its.append(mcq("Cuts parallel to the base of an object are squares that get smaller and smaller until they reach a point. What is the object?",
                   "square-based pyramid", [pname(4), pname(3), "cone"],
                   "Squares that shrink to a point make a square-based pyramid. If the squares stayed the same size it would be a prism."))
    n, he, his = P.next()
    its.append(mcq("A loaf of sandwich bread is shaped like a rectangular prism with square ends. %s cuts it into slices parallel to the ends. "
                   "What shape is each slice?" % n, "a square, the same size as the ends",
                   ["a rectangle as long as the loaf", "a smaller square each time", "a triangle"],
                   "Cuts parallel to the ends of a prism are the same as the ends: every slice is the same square."))
    n, he, his = P.next()
    its.append(mcq("%s saws an unsharpened pencil (a hexagonal prism) in half, straight across, parallel to its end. "
                   "What shape is the outline of the cut face?" % n, "hexagon", ["circle", "rectangle", "octagon"],
                   "The pencil is a hexagonal prism, so a cut parallel to the end is a hexagon. (The lead in the middle is a small circle, but the outline of the cut is a hexagon.)"))
    n, he, his = P.next()
    its.append(mcq("A long chocolate box has two triangle ends joined by 3 rectangles. %s cuts the box parallel to an end. "
                   "What shape is the cut?" % n, "triangle", ["rectangle", "pentagon", "square"],
                   "The box is a triangular prism. Cuts parallel to its ends are triangles, the same as the ends."))
    its.append(mcq("A prism is cut parallel to its ends. The cross-section is a pentagon. How many faces does the prism have?", 7,
                   [5, 6, 10],
                   "It is a pentagonal prism: 2 pentagon ends + 5 rectangles = 7 faces. 6 would be a pentagonal pyramid."))
    n, he, his = P.next()
    its.append(mcq("%s cuts a cone parallel to its base and says the cut face is a triangle. What did %s mix up?" % (n, he),
                   "A cut straight down through the point gives a triangle; a cut parallel to the base gives a circle",
                   ["Nothing: the cut face is a triangle", "The cut face is a square", "The cut face is a rectangle"],
                   "A cone looks like a triangle from the side, but a cut parallel to its base is always a circle."))
    p = pos.next()
    keys = ["cone", "pyr4", "pyr3"]
    keys.insert(p, "cube")
    its.append(mcq_fixed(fig(four(keys, "four objects labelled A to D")) +
                         "Each object is cut parallel to its base, halfway up. Which cross-section is the same size as the base?",
                         list("ABCD"), "ABCD"[p],
                         "%s is a cube, a prism, so every cut parallel to the base is the same square. "
                         "The cone and the pyramids get smaller towards the point, so their cuts are smaller than the base." % "ABCD"[p]))
    assert len(its) == 20, len(its)
    return {"title": "Cross-sections parallel to the base", "items": its}


# ------------------------------------------------------------ set 4: faces, edges and vertices
def fev_e(n):
    F, E, V = fev(n)
    return ("%s has %d faces (2 %ss + %d rectangles), %d edges (%d + %d + %d) and %d vertices (%d + %d)."
            % (an(pname(n)).capitalize(), F, POLY[n], n, E, n, n, n, V, n, n))


def set_fev(rnd):
    its = []
    D = " Dashed lines show edges at the back that you cannot see."
    rows = [  # n, what, wrong, picture key
        (3, "faces", [3, 6, 4], "tri", " You can see only 3 faces, but the bottom and the back end count too."),
        (3, "edges", [6, 5, 12], "up3", " 3 edges round each end and 3 joining the ends."),
        (3, "vertices", [3, 9, 5], None, ""),
        (4, "edges", [8, 6, 4], "rect", D),
        (5, "faces", [5, 10, 6], "pent", D),
        (5, "edges", [10, 7, 5], None, " Do not forget the 5 edges that join the two ends."),
        (5, "vertices", [5, 15, 6], "house", ""),
        (6, "faces", [6, 7, 12], "hex", " Do not forget the 2 hexagon ends."),
        (6, "edges", [12, 8, 6], None, " Edges round both ends (6 + 6) plus 6 joining them."),
        (6, "vertices", [6, 18, 7], "up6", ""),
        (8, "faces", [8, 9, 16], None, ""),
        (8, "edges", [16, 10, 8], None, ""),
        (7, "vertices", [7, 21, 8], None, ""),
    ]
    for n, what, wrong, key, extra in rows:
        ans = dict(zip(("faces", "edges", "vertices"), fev(n)))[what]
        if key:
            q = fig(obj_svg(key, an(pname(n)))) + "This is %s. How many %s does it have?" % (an(pname(n)), what)
        else:
            q = "How many %s does %s have?" % (what, an(pname(n)))
        its.append(mcq(q, ans, wrong, fev_e(n) + extra))
    its.append(mcq("A prism has 8 faces. What shape is its cross-section?", "hexagon", ["octagon", "heptagon", "rectangle"],
                   "Faces = 2 ends + the number of sides. 8 − 2 = 6 sides, so the ends are hexagons. (Heptagon uses the pyramid rule: 8 − 1.)"))
    its.append(mcq("A prism has 18 edges. What shape is its cross-section?", "hexagon", ["nonagon", "octagon", "triangle"],
                   "A prism has 3 edges for every side of its end (round the front, round the back, and joining them). 18 ÷ 3 = 6, so the ends are hexagons."))
    its.append(mcq("A prism has 10 vertices. What is its name?", pname(5), ["decagonal prism", pname(8), pname(6)],
                   "Half the vertices are on each end: 10 ÷ 2 = 5, so the ends are pentagons."))
    F1, E1, V1 = fev(6)
    F2, E2, V2 = pyr_fev(6)
    its.append(mcq("How many more vertices does a hexagonal prism have than a hexagonal pyramid?", V1 - V2, [6, 1, 12],
                   "Prism: 6 + 6 = 12 vertices. Pyramid: 6 on the base + 1 apex = 7. 12 − 7 = 5."))
    F1, E1, V1 = fev(5)
    F2, E2, V2 = pyr_fev(5)
    its.append(mcq("Which has more edges, a pentagonal prism or a pentagonal pyramid, and by how many?", "the prism, by %d" % (E1 - E2),
                   ["the pyramid, by 5", "the prism, by 10", "they have the same number"],
                   "Prism: 5 + 5 + 5 = 15 edges. Pyramid: 5 round the base + 5 up to the apex = 10. 15 − 10 = 5."))
    its.append(mcq("A prism’s cross-section has n sides. Which rule gives its number of faces?", "n + 2", ["n + 1", "2 × n", "3 × n"],
                   "There are n rectangles plus the 2 ends: n + 2. (n + 1 is the rule for a pyramid, 2 × n gives the vertices and 3 × n gives the edges.)"))
    its.append(mcq("A triangular prism and a square-based pyramid both have 5 faces. How else are they different?",
                   "The prism has 6 vertices and the pyramid has 5", ["They have the same number of edges", "The pyramid has more edges",
                                                                       "The prism has 5 vertices and the pyramid has 6"],
                   "Triangular prism: 9 edges, 6 vertices. Square-based pyramid: 8 edges, 5 vertices."))
    assert fev(3)[1:] == (9, 6) and pyr_fev(4)[1:] == (8, 5)
    assert len(its) == 20, len(its)
    return {"title": "Faces, edges and vertices of prisms", "items": its}


# ------------------------------------------------------------ set 5: prisms in real life
def set_real(rnd, P):
    its = []
    n, he, his = P.next()
    its.append(mcq("%s’s family tent has two triangle ends, two sloping sides and a floor. What object is the tent shaped like?" % n,
                   pname(3), ["triangular pyramid", pname(4), pname(5)],
                   "Two triangle ends joined by rectangles (2 sides and the floor) make a triangular prism. Do not use the 5 faces to name it."))
    n, he, his = P.next()
    its.append(mcq("A chocolate bar comes in a long box with two triangle ends. %s flattens the box for recycling. How many faces of cardboard are there?" % n,
                   5, [3, 6, 9],
                   "The box is a triangular prism: 2 triangles + 3 rectangles = 5 faces. 9 is the number of edges."))
    n, he, his = P.next()
    its.append(mcq("%s’s pencil is a hexagonal prism. How many long flat faces run down its side (not counting the ends)?" % n,
                   6, [8, 3, 12],
                   "A hexagon has 6 sides, so there are 6 rectangles along the pencil. 8 counts the 2 ends as well, and 3 is how many you can see at once."))
    n, he, his = P.next()
    its.append(mcq("%s makes the frame of a hexagonal prism from straws, one straw for each edge. How many straws does %s need?" % (n, he),
                   18, [12, 8, 6], "Edges: 6 round each end + 6 joining them = 18. 12 is the number of vertices and 8 the number of faces."))
    n, he, his = P.next()
    its.append(mcq("%s uses balls of modelling clay to join straws at the corners of a pentagonal prism. How many balls of clay does %s need?" % (n, he),
                   10, [15, 7, 5], "One ball for each vertex: 5 on each pentagon end, 5 + 5 = 10. 15 is the number of edges."))
    n, he, his = P.next()
    its.append(mcq("%s paints each face of a wooden triangular prism a different colour. How many colours does %s use?" % (n, he),
                   5, [3, 6, 9], "A triangular prism has 2 triangles + 3 rectangles = 5 faces."))
    n, he, his = P.next()
    its.append(mcq("%s stacks 10 identical hexagon tiles exactly on top of each other. What object does the stack look like?" % n,
                   pname(6), ["hexagonal pyramid", "cylinder", "hexagon"],
                   "Every layer is the same hexagon, so the stack has the same cross-section all the way up: a hexagonal prism."))
    n, he, his = P.next()
    its.append(mcq("%s stacks square tiles, each one smaller than the one below, with their centres in a line. Which object is the stack most like?" % n,
                   "square-based pyramid", [pname(4), "cube", "cone"],
                   "The square cross-sections get smaller towards the top, like a square-based pyramid. In a prism they would all be the same size."))
    n, he, his = P.next()
    its.append(mcq("%s’s birdhouse has a front and a back shaped like a house (a square with a triangle roof), joined by rectangles. What object is it?" % n,
                   pname(5), [pname(3), pname(4), "pentagonal pyramid"],
                   "The house shape has 5 sides, so the birdhouse is a pentagonal prism."))
    n, he, his = P.next()
    its.append(mcq("%s says the Great Pyramid of Giza is a prism. Why is %s wrong?" % (n, he),
                   "Its cross-sections get smaller towards the top",
                   ["It has a square base", "It is too big to be a prism", "It has 5 faces"],
                   "The Great Pyramid is a square-based pyramid: its square slices shrink to a point. A prism keeps the same cross-section all the way up."))
    n, he, his = P.next()
    its.append(mcq("%s cuts a party hat (a cone) parallel to its rim, partway up. What shape is the cut?" % n,
                   "a circle, smaller than the rim", ["a triangle", "a circle the same size as the rim", "an oval with a point"],
                   "A cut parallel to the base of a cone is a circle. It is smaller than the rim because the cone narrows to a point."))
    its.append(mcq("At the sausage sizzle, every slice of a long round salami is the same circle. Is the salami shaped like a prism?",
                   "No, it is shaped like a cylinder", ["Yes, a circular prism", "No, it is shaped like a cone", "Yes, a rectangular prism"],
                   "The same circle all along is a cylinder. It has a curved surface, so it is not a prism."))
    n, he, his = P.next()
    its.append(mcq("%s slices a carrot from the thick end to the thin end. The slices are circles that get smaller. Which object is the carrot most like?" % n,
                   "cone", ["cylinder", pname(6), "sphere"],
                   "Circles that get smaller towards a point match a cone. A cylinder would give circles that are all the same size."))
    n, he, his = P.next()
    its.append(mcq("A block of cheese has two triangle ends joined by rectangles. %s cuts it parallel to a triangle end. What shape is the cut face?" % n,
                   "triangle", ["rectangle", "square", "smaller triangle each time"],
                   "The cheese is a triangular prism, so every cut parallel to the ends is the same triangle."))
    its.append(mcq("At the swimming carnival, the pool is deeper at one end. From the side, the water is a trapezium, and it is the same all the way across the pool. "
                   "What object is the water shaped like?", "a prism with a trapezium cross-section",
                   [pname(4), "a square-based pyramid", pname(3)],
                   "The water has the same trapezium cross-section from one side of the pool to the other, so it is a prism with trapezium ends."))
    n, he, his = P.next()
    its.append(mcq("%s tapes every edge of a cube-shaped gift box. Each edge is 20 cm long. How much tape does %s use?" % (n, he),
                   "240 cm", ["120 cm", "160 cm", "80 cm"],
                   "A cube has 12 edges: 12 × 20 = 240 cm. 120 cm uses the 6 faces, 160 cm the 8 vertices and 80 cm only 4 edges."))
    n, he, his = P.next()
    s, L = 4, 20
    tot = 6 * s + 3 * L
    assert tot == 84
    its.append(mcq("A chocolate box is a triangular prism. Each triangle end has sides of %d cm, and the box is %d cm long. "
                   "%s runs ribbon along every edge. How much ribbon is that?" % (s, L, n),
                   "%d cm" % tot, ["%d cm" % (3 * s + 3 * L), "%d cm" % (6 * s + L), "%d cm" % (6 * s + 2 * L)],
                   "Edges round the two ends: 6 × %d = %d cm. Three long edges: 3 × %d = %d cm. Total: %d + %d = %d cm."
                   % (s, 6 * s, L, 3 * L, 6 * s, 3 * L, tot)))
    n, he, his = P.next()
    a = fev(5)[1] + pyr_fev(5)[1]
    assert a == 25
    its.append(mcq("%s makes the frames of a pentagonal prism and a pentagonal pyramid from straws, one straw for each edge. How many straws altogether?" % n,
                   a, [30, 20, 16],
                   "Prism: 15 edges. Pyramid: 5 round the base + 5 up to the apex = 10. 15 + 10 = 25. (30 counts the prism twice; 16 adds the vertices, 10 + 6.)"))
    n, he, his = P.next()
    its.append(mcq("%s sands every face of a wooden block shaped like an octagonal prism. How many faces does %s sand?" % (n, he),
                   10, [8, 9, 16], "2 octagon ends + 8 rectangles = 10 faces. 9 would be an octagonal pyramid and 16 is the number of vertices."))
    n, he, his = P.next()
    its.append(mcq("%s cuts a wooden beam with a square end into 4 shorter pieces, with cuts parallel to the end. What is each piece?" % n,
                   "a prism with a square cross-section", ["a square-based pyramid", "a square", "a cube every time"],
                   "Cuts parallel to the end keep the same square cross-section, so each piece is still a prism (a rectangular prism with square ends). "
                   "It is only a cube if the piece is exactly as long as the square is wide."))
    assert len(its) == 20, len(its)
    return {"title": "Prisms in real life: tents, pencils, boxes and more", "items": its}


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
    cuts = row_svg([cut_prism_cv(3, 42), cut_pyramid_cv(4, 42), cut_cylinder_cv(28, 9, 64, gap=28), cut_cone_cv(30, 9, 66, gap=24)],
                   ["prism: same", "pyramid: smaller", "cylinder: same", "cone: smaller"],
                   "a prism, a pyramid, a cylinder and a cone, each cut parallel to its base", gap=22, fs=14)
    return (
        "<h2>What is a prism?</h2>"
        "<p>A <b>right prism</b> has two matching ends that are parallel, joined by <b>rectangles</b>. "
        "If you cut it anywhere parallel to its ends, the cut face (the <b>cross-section</b>) is the same shape and size every time.</p>"
        "<p>A prism is <b>named after its cross-section</b>: triangle ends make a triangular prism, hexagon ends make a hexagonal prism.</p>"
        "<figure class='sn-fig'>" + prisms + "</figure>" +
        ex("Example 1", "A prism has ends with 5 sides. What is it called?",
           "Count the sides of an end, not the faces. 5 sides make a pentagon.", "a pentagonal prism") +
        "<h2>Compare the cross-sections</h2>"
        "<p>Cut each object parallel to its base and look at the red face.</p>"
        "<figure class='sn-fig'>" + cuts +
        "<figcaption>A prism and a cylinder keep the same cross-section all the way up. A pyramid and a cone get smaller towards the point.</figcaption></figure>" +
        table(["Object", "Cut parallel to the base", "A prism?"], [
            ["Triangular prism", "the same triangle every time", "Yes"],
            ["Cube", "the same square every time", "Yes"],
            ["Square-based pyramid", "squares that get smaller", "No"],
            ["Cylinder", "the same circle every time", "No: circle ends and a curved surface"],
            ["Cone", "circles that get smaller", "No"],
        ]) +
        ex("Example 2", "A loaf of sandwich bread has square ends. It is sliced parallel to the ends. What shape is each slice?",
           "The loaf is a prism, so every slice is the same as the end.", "the same square") +
        "<h2>Faces, edges and vertices</h2>"
        "<p>If the end of a prism has <b>n</b> sides, the prism has <b>n + 2</b> faces, <b>3 × n</b> edges and <b>2 × n</b> vertices.</p>" +
        table(["Prism", "Faces", "Edges", "Vertices"],
              [[pname(n).capitalize()] + [str(x) for x in fev(n)] for n in (3, 4, 5, 6, 8)]) +
        ex("Example 3", "How many edges does a pentagonal prism have?",
           "5 round the front end, 5 round the back end and 5 joining them: 5 + 5 + 5.", "15 edges") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Naming a prism by its number of faces (a triangular prism has 5 faces, but it is not “pentagonal”)", "Name it by the shape of its ends"],
            ["Calling a pyramid a prism because it has triangles", "A pyramid has one base and triangles that meet at a point; its cross-sections shrink"],
            ["Saying a cone’s cross-section is a triangle", "Cut parallel to the base: a cone gives a circle (smaller than the base)"],
            ["Calling a cylinder a “circular prism”", "A cylinder has a curved surface, so it is not a prism"],
            ["Counting only the faces you can see", "Count the hidden ends and the bottom too"],
            ["Forgetting the edges that join the two ends", "Edges = round the front + round the back + joining them"],
        ])
    )


FAQ = [
    {"q": "What do Year 6 students learn about prisms in the Australian Curriculum?",
     "a": "In Year 6 (AC9M6SP01) students Compare the parallel cross-sections of objects and recognise that a right prism has the same cross-section all along its length, and is named after that shape."},
    {"q": "What is a cross-section of a prism?",
     "a": "It is the flat face you get when you cut the prism parallel to its ends. For a prism it is always the same shape and size as the ends, for example a triangle for a triangular prism."},
    {"q": "Is a cylinder a prism?",
     "a": "No. A cylinder has the same circle cross-section all the way along, but its ends are circles and it has a curved surface, while a prism has polygon ends and only flat faces."},
    {"q": "What is the difference between a prism and a pyramid?",
     "a": "A prism has two matching ends joined by rectangles, so its cross-sections stay the same. A pyramid has one base and triangles that meet at a point, so its cross-sections get smaller towards the apex."},
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
    rnd = random.Random(6816)
    P = People(rnd)
    pos = Pos(rnd)
    sets = [set_name(rnd, pos), set_which(rnd, pos, P), set_cut(rnd, pos, P), set_fev(rnd), set_real(rnd, P)]
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
        "country": "au", "subject": "maths", "grade": "year-6", "slug": "prisms-and-cross-sections", "sort": 16,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 6 Prisms and Cross-Sections",
        "seo_title": "Year 6 Prisms and Cross-Sections Worksheets: Name Prisms, Compare Cross-Sections (Free, with Answers)",
        "short_title": "Prisms and cross-sections",
        "domain": "Space",
        "standard_code": "AC9M6SP01",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Compare the parallel cross-sections of objects and recognise their relationships to right prisms",
        "meta_desc": "Free Year 6 maths worksheets on prisms and cross-sections for the Australian Curriculum: name prisms by their cross-section, tell prisms from pyramids, cylinders and cones, compare cuts parallel to the base, and count faces, edges and vertices. 100 questions with an answer key, ready for Year 7.",
        "key_big": "A prism has the same cross-section all along its length, and it is named after that shape.",
        "key_sub": "Cut a prism parallel to its ends and you always get the same shape: a triangle for a triangular prism, a hexagon for a hexagonal prism. Pyramids and cones get smaller towards the point, so they are not prisms; a cylinder has a curved surface, so it is not a prism either.",
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
