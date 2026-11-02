# -*- coding: utf-8 -*-
"""
UK Year 3 Maths: 2-D and 3-D shapes (National Curriculum in England, Geometry – properties of shapes)
  python3 tools/gen_uk_maths_y3_shapes.py
HTML attributes use single quotes (no backslashes in the JSON). British English.

Year 3 names 2-D shapes (triangle, square, rectangle, pentagon, hexagon, octagon, circle, semicircle)
and 3-D shapes (cube, cuboid, cylinder, cone, sphere, square-based pyramid, triangular prism),
recognises them turned round or lying down, and counts faces, edges and vertices.

Pictures (checked in code):
  2-D shapes  drawn from their corner points, turned and in different sizes; the number of sides is the
              number of points, no two sides cross and every corner really is a corner (not almost straight)
  3-D shapes  drawn from 3-D vertices and faces, turned (yaw) and seen from a little above (pitch);
              a face is shown when it faces the viewer, edges of hidden faces only are dashed;
              faces, edges and vertices are counted from the same data (V − E + F = 2), and the
              "only counted what you can see" wrong answers are counted from the same picture
  models      straw-and-clay models: one straw for each edge, one clay ball for each vertex
Wrong answers come from real pupil mistakes: a turned square called a diamond, a side miscounted
(pentagon/hexagon/octagon mixed up), a 3-D shape given its 2-D name (circle for sphere), cylinder vs cone
vs prism, prism vs pyramid, cube vs cuboid, hidden faces not counted, edges and vertices swapped.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL, BASE, SIDE, TOP3 = "#cfe6d6", "#f6dcb4", "#a9d3b6", "#e6f2e9"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
STRAW = "#d99a2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]

CUBE, CUBOID, TP, SP = "cube", "cuboid", "triangular prism", "square-based pyramid"
CYL, CONE, SPH = "cylinder", "cone", "sphere"


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
    """Approximate width of bold Arial text in px."""
    t = str(t)
    return (len(t) - t.count(" ") * 0.3 - t.count("-") * 0.3) * fs * 0.6


def circle_pts(c, r, n=72):
    return [(c[0] + r * math.cos(2 * math.pi * i / n), c[1] + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


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
                s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>"
                         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in e[1]), e[2], e[4], e[3]))
            elif e[0] == "c":
                _, c, r, fill, sw, col = e
                st = " stroke='%s' stroke-width='%g'" % (col, sw) if sw else ""
                s.append("<circle cx='%.1f' cy='%.1f' r='%g' fill='%s'%s/>" % (c[0] - ox, c[1] - oy, r, fill, st))
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


# ------------------------------------------------------------ 2-D shapes
def reg(n, r, start=-90):
    return [(r * math.cos(math.radians(start + 360 * i / n)), r * math.sin(math.radians(start + 360 * i / n))) for i in range(n)]


def turn(pts, deg, s=1.0):
    """Turn the points about their middle and scale them."""
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    c, si = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return [((x - cx) * c - (y - cy) * si) * s for x, y in pts], [((x - cx) * si + (y - cy) * c) * s for x, y in pts]


def tpts(pts, deg=0, s=1.0):
    xs, ys = turn(pts, deg, s)
    return list(zip(xs, ys))


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


NAME2D = {3: "triangle", 4: "quadrilateral", 5: "pentagon", 6: "hexagon", 8: "octagon"}
SHAPES2D = {
    "tri_eq": reg(3, 40),
    "tri_right": [(0, 0), (0, 60), (80, 60)],
    "tri_thin": [(0, 0), (110, 20), (20, 45)],
    "square": [(0, 0), (60, 0), (60, 60), (0, 60)],
    "rect": [(0, 0), (100, 0), (100, 50), (0, 50)],
    "rhombus": [(0, 0), (60, 0), (60 + 60 * math.cos(math.radians(55)), 60 * math.sin(math.radians(55))),
                (60 * math.cos(math.radians(55)), 60 * math.sin(math.radians(55)))],
    "trapezium": [(0, 60), (100, 60), (75, 0), (25, 0)],
    "pent_reg": reg(5, 42),
    "pent_house": [(0, 40), (40, 0), (80, 40), (80, 100), (0, 100)],
    "pent_odd": [(0, 0), (90, 0), (110, 45), (50, 80), (0, 55)],
    "hex_reg": reg(6, 42, 0),
    "hex_L": [(0, 0), (40, 0), (40, 55), (90, 55), (90, 95), (0, 95)],
    "hex_arrow": [(0, 20), (60, 20), (60, 0), (100, 40), (60, 80), (60, 60)],
    "oct_reg": reg(8, 42, 22.5),
    "oct_cut": [(20, 0), (100, 0), (120, 20), (120, 60), (100, 80), (20, 80), (0, 60), (0, 20)],
}
for _p in SHAPES2D.values():
    check_poly(_p)


def shape2d(key, deg=0, s=1.0, fill=FILL):
    pts = tpts(SHAPES2D[key], deg, s)
    check_poly(pts)
    cv = Canvas()
    cv.poly(pts, fill, 3)
    return cv


def circle_cv(r=40):
    cv = Canvas()
    cv.circle((0, 0), r, sw=3)
    return cv


def semi_cv(r=45, deg=0):
    """Semicircle: the curved side and 1 straight side. deg turns it."""
    pts = [(r * math.cos(math.radians(a)), -r * math.sin(math.radians(a))) for a in range(0, 181, 5)]
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    pts = [(x * c - y * s, x * s + y * c) for x, y in pts]
    cv = Canvas()
    cv.poly(pts, FILL, 3)
    return cv


def n_sides(key):
    return len(SHAPES2D[key])


# ------------------------------------------------------------ 3-D shapes
class Solid:
    def __init__(self, verts, faces):
        self.v, self.f = verts, faces
        edges = {}
        for fi, fc in enumerate(faces):
            for i in range(len(fc)):
                e = tuple(sorted((fc[i], fc[(i + 1) % len(fc)])))
                edges.setdefault(e, []).append(fi)
        assert all(len(x) == 2 for x in edges.values())
        self.edges = edges
        F, E, V = len(faces), len(edges), len(verts)
        assert V - E + F == 2, (V, E, F)
        self.count = {"faces": F, "edges": E, "vertices": V}

    def view(self, yaw, pitch):
        """Turn the solid by yaw about the up axis, then tip it towards the viewer by pitch.
        Returns the points in view space and which faces the viewer can see (viewer at -z)."""
        cy_, sy_ = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
        cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))
        pts = []
        for x, y, z in self.v:
            x1, z1 = x * cy_ + z * sy_, -x * sy_ + z * cy_
            y2, z2 = y * cp + z1 * sp, -y * sp + z1 * cp
            pts.append((x1, y2, z2))
        c = [sum(p[i] for p in pts) / len(pts) for i in range(3)]
        vis, nrm = [], []
        for fc in self.f:
            a, b, d = (pts[i] for i in fc[:3])
            u = [b[i] - a[i] for i in range(3)]
            w = [d[i] - a[i] for i in range(3)]
            n = [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]]
            m = [sum(pts[i][j] for i in fc) / len(fc) for j in range(3)]
            if sum(n[i] * (m[i] - c[i]) for i in range(3)) < 0:
                n = [-x for x in n]
            L = math.sqrt(sum(x * x for x in n))
            n = [x / L for x in n]
            nrm.append(n)
            vis.append(n[2] < -1e-6)
        return pts, vis, nrm

    def seen(self, yaw, pitch):
        """How many faces, edges and vertices can be seen in this picture."""
        _, vis, _ = self.view(yaw, pitch)
        F = sum(vis)
        E = sum(1 for fs in self.edges.values() if any(vis[f] for f in fs))
        V = len({i for fi, fc in enumerate(self.f) if vis[fi] for i in fc})
        return {"faces": F, "edges": E, "vertices": V}

    def cv(self, k, yaw=30, pitch=20):
        pts, vis, nrm = self.view(yaw, pitch)
        P = lambda p: (p[0] * k, -p[1] * k)
        cv = Canvas()
        for fi, fc in enumerate(self.f):
            if vis[fi]:
                n = nrm[fi]
                col = TOP3 if n[1] > 0.5 else SIDE if n[0] > 0.3 else FILL
                cv.poly([P(pts[i]) for i in fc], col, 2.4)
        for (a, b), fs in self.edges.items():
            if not any(vis[f] for f in fs):
                cv.line(P(pts[a]), P(pts[b]), dashed=True, sw=1.6)
        return cv

    def model_cv(self, k, yaw=30, pitch=20):
        """Straw-and-clay model: every edge is a straw, every vertex a ball of clay."""
        pts, vis, _ = self.view(yaw, pitch)
        P = lambda p: (p[0] * k, -p[1] * k)
        cv = Canvas()
        back = [e for e, fs in self.edges.items() if not any(vis[f] for f in fs)]
        front = [e for e in self.edges if e not in back]
        for a, b in back:
            cv.line(P(pts[a]), P(pts[b]), sw=3.5, col="#e9c27a")
        for a, b in front:
            cv.line(P(pts[a]), P(pts[b]), sw=4, col=STRAW)
        for i in sorted(range(len(pts)), key=lambda i: -pts[i][2]):
            cv.circle(P(pts[i]), 6, fill=RED, sw=1.2, col="#7a2318")
        return cv


def box(L, H, W):
    v = [(x, y, z) for x in (0, L) for y in (0, H) for z in (0, W)]
    idx = {p: i for i, p in enumerate(v)}
    g = lambda *ps: [idx[p] for p in ps]
    f = [g((0, 0, 0), (L, 0, 0), (L, H, 0), (0, H, 0)), g((0, 0, W), (L, 0, W), (L, H, W), (0, H, W)),
         g((0, 0, 0), (0, 0, W), (0, H, W), (0, H, 0)), g((L, 0, 0), (L, 0, W), (L, H, W), (L, H, 0)),
         g((0, 0, 0), (L, 0, 0), (L, 0, W), (0, 0, W)), g((0, H, 0), (L, H, 0), (L, H, W), (0, H, W))]
    return Solid(v, f)


def prism_lying(w=1.2, h=0.95, D=1.8):
    """Triangular prism lying on a rectangle face: triangle ends in the y-z plane, length along x."""
    tri = [(0, 0), (w, 0), (w / 2, h)]          # (z, y)
    v = [(0, y, z) for z, y in tri] + [(D, y, z) for z, y in tri]
    f = [[0, 1, 2], [3, 4, 5]] + [[i, (i + 1) % 3, 3 + (i + 1) % 3, 3 + i] for i in range(3)]
    return Solid(v, f)


def prism_standing(w=1.1, d=0.95, H=1.5):
    """Triangular prism standing on a triangle face."""
    tri = [(0, 0), (w, 0), (w / 2, d)]          # (x, z)
    v = [(x, 0, z) for x, z in tri] + [(x, H, z) for x, z in tri]
    f = [[0, 1, 2], [3, 4, 5]] + [[i, (i + 1) % 3, 3 + (i + 1) % 3, 3 + i] for i in range(3)]
    return Solid(v, f)


def pyramid(s=1.3, h=1.3):
    v = [(0, 0, 0), (s, 0, 0), (s, 0, s), (0, 0, s), (s / 2, h, s / 2)]
    f = [[0, 1, 2, 3]] + [[i, (i + 1) % 4, 4] for i in range(4)]
    return Solid(v, f)


COUNTS = {CUBE: (6, 12, 8), CUBOID: (6, 12, 8), TP: (5, 9, 6), SP: (5, 8, 5)}
for _s, _k in [(box(1, 1, 1), CUBE), (box(1.8, 1, 0.9), CUBOID), (prism_lying(), TP), (prism_standing(), TP), (pyramid(), SP)]:
    assert tuple(_s.count[x] for x in ("faces", "edges", "vertices")) == COUNTS[_k], _k

# every picture used: (solid, yaw, pitch)
VIEWS = {
    "cube": (lambda: box(1.1, 1.1, 1.1), 30, 22),
    "cube_turned": (lambda: box(1.1, 1.1, 1.1), 50, 30),
    "cuboid_flat": (lambda: box(1.9, 0.8, 1.0), 25, 22),
    "cuboid_tall": (lambda: box(0.8, 1.8, 0.7), 35, 18),
    "cuboid_turned": (lambda: box(1.6, 1.0, 0.8), -35, 24),
    "tp_lying": (lambda: prism_lying(), 30, 20),
    "tp_end": (lambda: prism_lying(), 120, 25),
    "tp_standing": (lambda: prism_standing(), 20, 35),
    "sp": (lambda: pyramid(), 25, 18),
    "sp_turned": (lambda: pyramid(1.2, 1.5), -30, 25),
}
VIEW_KIND = {"cube": CUBE, "cube_turned": CUBE, "cuboid_flat": CUBOID, "cuboid_tall": CUBOID, "cuboid_turned": CUBOID,
             "tp_lying": TP, "tp_end": TP, "tp_standing": TP, "sp": SP, "sp_turned": SP}
for _v, (_f, _y, _p) in VIEWS.items():
    _s = _f()
    assert tuple(_s.count[x] for x in ("faces", "edges", "vertices")) == COUNTS[VIEW_KIND[_v]], _v
    _seen = _s.seen(_y, _p)
    assert 1 < _seen["faces"] < _s.count["faces"], (_v, _seen)


def solid_cv(view, k=50):
    f, yaw, pitch = VIEWS[view]
    return f().cv(k, yaw, pitch)


def model_cv(view, k=55):
    f, yaw, pitch = VIEWS[view]
    return f().model_cv(k, yaw, pitch)


def seen(view):
    f, yaw, pitch = VIEWS[view]
    return f().seen(yaw, pitch)


# ------------------------------------------------------------ curved 3-D shapes (drawn flat, then turned)
def ellipse(cx, cy, rx, ry, a0, a1, n=40):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def _rot90(pts, on):
    return [(-y, x) for x, y in pts] if on else pts


def cylinder_cv(s=1.0, lying=False):
    rx, ry, h = 36 * s, 11 * s, 72 * s
    R = lambda p: _rot90(p, lying)
    cv = Canvas()
    cv.poly(R(ellipse(0, 0, rx, ry, 180, 360) + ellipse(0, h, rx, ry, 0, 180)), FILL, 0.01)
    cv.poly(R(ellipse(0, 0, rx, ry, 0, 360)[:-1]), TOP3, 2.4)
    cv.pline(R([(-rx, 0), (-rx, h)]))
    cv.pline(R([(rx, 0), (rx, h)]))
    cv.pline(R(ellipse(0, h, rx, ry, 0, 180)))
    cv.pline(R(ellipse(0, h, rx, ry, 180, 360)), dashed=True, sw=1.6)
    return cv


def cone_cv(s=1.0, how="up"):
    """how: 'up' (point at the top), 'down' (point at the bottom, like an ice-cream cone), 'side' (lying down)."""
    rx, ry, h = 38 * s, 11 * s, 80 * s
    cv = Canvas()
    if how == "down":
        cv.poly([(0, h)] + ellipse(0, 0, rx, ry, 0, 180), FILL, 0.01)
        cv.pline([(-rx, 0), (0, h), (rx, 0)])
        cv.poly(ellipse(0, 0, rx, ry, 0, 360)[:-1], TOP3, 2.4)
        return cv
    R = lambda p: _rot90(p, how == "side")
    cv.poly(R([(0, 0)] + ellipse(0, h, rx, ry, 180, 0)), FILL, 0.01)
    cv.poly(R([(0, 0)] + ellipse(0, h, rx, ry, 0, 180)), FILL, 0.01)
    cv.pline(R([(-rx, h), (0, 0), (rx, h)]))
    cv.pline(R(ellipse(0, h, rx, ry, 0, 180)))
    cv.pline(R(ellipse(0, h, rx, ry, 180, 360)), dashed=True, sw=1.6)
    return cv


def sphere_cv(s=1.0):
    r = 40 * s
    cv = Canvas()
    cv.circle((0, 0), r, fill=FILL, sw=2.4)
    cv.pline(ellipse(0, 0, r, r * 0.3, 0, 180), sw=1.6)
    cv.pline(ellipse(0, 0, r, r * 0.3, 180, 360), dashed=True, sw=1.2)
    return cv


def pic3d(key, s=1.0):
    """Any 3-D picture by key. s scales it (1.0 = full size for one picture)."""
    if key in VIEWS:
        return solid_cv(key, 50 * s)
    if key == "cyl":
        return cylinder_cv(s)
    if key == "cyl_lying":
        return cylinder_cv(s, lying=True)
    if key.startswith("cone"):
        return cone_cv(s, {"cone": "up", "cone_down": "down", "cone_side": "side"}[key])
    if key == "sphere":
        return sphere_cv(s)
    raise KeyError(key)


KIND = dict(VIEW_KIND, cyl=CYL, cyl_lying=CYL, cone=CONE, cone_down=CONE, cone_side=CONE, sphere=SPH)


def art(n):
    return "an" if n[0] in "aeiou" else "a"


# ------------------------------------------------------------ set 1: 2-D shapes
NAME_E = {
    "triangle": "It has 3 straight sides and 3 vertices, so it is a triangle.",
    "square": "It has 4 equal sides and 4 right angles, so it is a square.",
    "rectangle": "It has 4 sides and 4 right angles. The long sides are longer than the short sides, so it is a rectangle, not a square.",
    "pentagon": "Count the sides: 5 straight sides make a pentagon.",
    "hexagon": "Count the sides: 6 straight sides make a hexagon.",
    "octagon": "Count the sides: 8 straight sides make an octagon.",
}
TURNED = " Turning a shape or making it bigger or smaller does not change its name."


def set_2d(rnd, pos):
    its = []
    asks = ["What is the name of this shape?", "Name this 2-D shape.", "What is this shape called?"]
    a = iter(asks * 6)
    rows = [
        (shape2d("square", 45), "square", ["diamond", "triangle", "hexagon"],
         "It has 4 equal sides and 4 right angles, so it is a square. It is only turned. “Diamond” is not the maths name."),
        (shape2d("rect", 30), "rectangle", ["square", "triangle", "pentagon"], NAME_E["rectangle"] + TURNED),
        (shape2d("tri_eq", 180), "triangle", ["square", "pentagon", "semicircle"], NAME_E["triangle"] + " It is upside down, but it is still a triangle."),
        (shape2d("tri_thin", 15), "triangle", ["rectangle", "pentagon", "hexagon"], NAME_E["triangle"] + " A long, thin triangle is still a triangle."),
        (shape2d("pent_reg", 36, 0.9), "pentagon", ["hexagon", "octagon", "square"], NAME_E["pentagon"]),
        (shape2d("pent_house", 180, 0.8), "pentagon", ["hexagon", "triangle", "square"], NAME_E["pentagon"] + " The sides do not have to be equal."),
        (shape2d("hex_reg", 15), "hexagon", ["octagon", "pentagon", "circle"], NAME_E["hexagon"]),
        (shape2d("hex_L", 0, 0.9), "hexagon", ["rectangle", "octagon", "pentagon"], NAME_E["hexagon"] + " The sides do not have to be equal."),
        (shape2d("oct_reg", 0, 0.85), "octagon", ["hexagon", "circle", "pentagon"], NAME_E["octagon"]),
        (shape2d("oct_cut", 90, 0.8), "octagon", ["rectangle", "hexagon", "pentagon"], NAME_E["octagon"] + " Count the short sides at the corners too."),
        (semi_cv(45, 90), "semicircle", ["circle", "oval", "triangle"],
         "It is half of a circle: 1 curved side and 1 straight side. It is a semicircle."),
        (circle_cv(38), "circle", ["sphere", "oval", "semicircle"],
         "It is flat and perfectly round, so it is a circle. A sphere is a 3-D shape, like a ball."),
    ]
    for cv, ans, wrong, e in rows:
        its.append(mcq(fig(cv.svg("a 2-D shape")) + next(a), ans, wrong, e))
    # counting sides and vertices from pictures (counted from the points)
    for key, deg, s, what in [("hex_arrow", 30, 0.9, "sides"), ("pent_odd", 200, 0.85, "vertices"), ("oct_reg", 22.5, 0.85, "vertices")]:
        n = n_sides(key)
        q = fig(shape2d(key, deg, s).svg("a 2-D shape")) + "How many %s does this shape have?" % what
        e = ("Count each %s once. Put a finger on one %s and go round until you are back where you started: %d %s. "
             "The shape has the same number of sides and vertices." % (what[:-1] if what == "sides" else "vertex",
                                                                         what[:-1] if what == "sides" else "vertex", n, what))
        its.append(mcq(q, n, [n + 1, n - 1, n + 2], e))
    its.append(mcq("A 2-D shape has 6 straight sides. What is it called?", "hexagon", ["pentagon", "octagon", "cube"],
                   "6 sides: hexagon. 5 sides: pentagon. 8 sides: octagon."))
    its.append(mcq("How many vertices does a pentagon have?", 5, [6, 4, 10],
                   "A pentagon has 5 sides and 5 vertices (corners). A shape with straight sides has the same number of sides and vertices."))
    its.append(mcq(fig(semi_cv(45, 0).svg("a semicircle")) + "How many straight sides does a semicircle have?", 1, [2, 0, 3],
                   "A semicircle has 1 straight side (along the bottom) and 1 curved side."))
    # A-D pictures
    p = pos.next()
    cells = [shape2d("pent_reg", 0, 0.8), shape2d("oct_reg", 0, 0.8), shape2d("square", 45, 0.8)]
    cells.insert(p, shape2d("hex_L", 90, 0.8))
    its.append(mcq_fixed(fig(grid_svg(cells, "four 2-D shapes labelled A to D")) + "Which shape is a hexagon?",
                         list("ABCD"), "ABCD"[p],
                         "%s has 6 sides, so it is a hexagon. The others have 5, 8 and 4 sides. A hexagon does not need equal sides." % "ABCD"[p]))
    p = pos.next()
    cells = [shape2d("rhombus", 62.5, 0.9), shape2d("rect", 0, 0.75), shape2d("trapezium", 0, 0.8)]
    cells.insert(p, shape2d("square", 45, 0.95))
    its.append(mcq_fixed(fig(grid_svg(cells, "four 2-D shapes labelled A to D")) + "Which shape is a square?",
                         list("ABCD"), "ABCD"[p],
                         "%s has 4 equal sides and 4 right angles. It is a square that has been turned. "
                         "The other diamond shape has equal sides but no right angles, so it is not a square." % "ABCD"[p]))
    assert len(its) == 20, len(its)
    return {"title": "2-D shapes: names, sides and vertices", "items": its}


# ------------------------------------------------------------ set 2: naming 3-D shapes
WRONG3 = {CUBE: [CUBOID, "square", SP], CUBOID: [CUBE, "rectangle", TP], TP: [SP, CUBOID, "triangle"],
          SP: [TP, CONE, "square"], CYL: [CONE, TP, "circle"], CONE: [CYL, "triangle", SP], SPH: ["circle", CYL, CONE]}
E3 = {
    CUBE: "It has 6 faces and they are all squares of the same size, so it is a cube.",
    CUBOID: "It has 6 rectangle faces and they are not all squares, so it is a cuboid.",
    TP: "It has 2 triangle faces at the ends, joined by 3 rectangles, so it is a triangular prism.",
    SP: "It has a square face at the bottom and 4 triangle faces that meet at a point, so it is a square-based pyramid.",
    CYL: "It has 2 circle faces at the ends and a curved surface, so it is a cylinder.",
    CONE: "It has 1 circle face and a curved surface that comes to a point, so it is a cone.",
    SPH: "It is round all over, like a ball, so it is a sphere. A circle is a flat 2-D shape.",
}
TURN3 = {"cube_turned": " It is turned, but it is still a cube.",
         "cuboid_tall": " It is standing on its end, but it is still a cuboid.",
         "cuboid_turned": " It is turned, but it is still a cuboid.",
         "tp_end": " It is turned so you see a triangle end at the front.",
         "tp_standing": " It is standing on a triangle face, but it is still a triangular prism.",
         "sp_turned": " It is turned, but it is still a square-based pyramid.",
         "cyl_lying": " It is lying on its side, but it is still a cylinder.",
         "cone_down": " It is upside down, but it is still a cone.",
         "cone_side": " It is lying on its side, but it is still a cone."}


def set_name3d(rnd, pos):
    its = []
    asks = ["What is the name of this 3-D shape?", "Name this 3-D shape.", "What is this 3-D shape called?"]
    keys = ["cube", "cube_turned", "cuboid_flat", "cuboid_tall", "tp_lying", "tp_standing", "tp_end", "sp", "sp_turned",
            "cyl", "cyl_lying", "cone", "cone_down", "cone_side", "sphere"]
    for i, k in enumerate(keys):
        kind = KIND[k]
        e = E3[kind] + TURN3.get(k, "")
        if k in ("tp_lying", "tp_standing", "tp_end"):
            e += " A pyramid comes to a point; a prism does not."
        its.append(mcq(fig(pic3d(k).svg("a 3-D shape")) + asks[i % 3], kind, WRONG3[kind], e))
    for a, b in [("tp_lying", "tp_standing"), ("cyl", "cyl_lying")]:
        kind = KIND[a]
        q = (fig(row_svg([pic3d(a, 0.8), pic3d(b, 0.8)], ["", ""], "the same 3-D shape in two positions", gap=40))
             + "Both pictures show the same 3-D shape in different positions. What is it?")
        its.append(mcq(q, kind, WRONG3[kind], E3[kind] + " Turning a shape does not change its name."))
    for kind, right, others, why in [
            (CONE, "cone_side", ["cyl_lying", "sp", "tp_end"], "it has 1 circle face and comes to a point. It is lying on its side"),
            (CUBOID, "cuboid_tall", ["cube", "tp_lying", "cyl"], "it has 6 rectangle faces that are not all squares. It is standing on its end"),
            (TP, "tp_standing", ["sp_turned", "cuboid_flat", "cone"], "it has 2 triangle faces joined by rectangles. It is standing on a triangle"),
    ]:
        p = pos.next()
        cells = [pic3d(k, 0.62) for k in others]
        cells.insert(p, pic3d(right, 0.62))
        its.append(mcq_fixed(fig(grid_svg(cells, "four 3-D shapes labelled A to D")) + "Which picture shows %s %s?" % (art(kind), kind),
                             list("ABCD"), "ABCD"[p], "%s is %s %s: %s." % ("ABCD"[p], art(kind), kind, why)))
    assert len(its) == 20, len(its)
    return {"title": "Name 3-D shapes in different positions", "items": its}


# ------------------------------------------------------------ set 3: faces, edges and vertices
def set_fev(rnd):
    its = []
    its.append(mcq("A flat surface of a 3-D shape is called a …", "face", ["edge", "vertex", "side"],
                   "A face is a flat surface. An edge is where two faces meet. A vertex is a corner."))
    its.append(mcq("The line where two faces of a 3-D shape meet is called an …", "edge", ["vertex", "face", "angle"],
                   "Where two faces meet there is an edge."))
    its.append(mcq("A corner of a 3-D shape, where edges meet, is called a …", "vertex", ["edge", "face", "side"],
                   "A corner is a vertex. More than one vertex are called vertices."))
    hidden = {"faces": "Some faces are at the back. You cannot see them, but you must count them too.",
              "edges": "The dashed lines show edges at the back. Count them too.",
              "vertices": "Some vertices are at the back, where the dashed lines meet. Count them too."}
    for view, what in [("cube", "faces"), ("cube", "edges"), ("cube_turned", "vertices"), ("cuboid_flat", "faces"),
                       ("tp_lying", "faces"), ("tp_lying", "edges"), ("tp_standing", "vertices"),
                       ("sp", "faces"), ("sp", "edges"), ("sp_turned", "vertices")]:
        kind = VIEW_KIND[view]
        F, E, V = COUNTS[kind]
        cnt = {"faces": F, "edges": E, "vertices": V}
        ans = cnt[what]
        vis = seen(view)[what]
        assert vis < ans
        others = [cnt[w] for w in ("faces", "edges", "vertices") if w != what]
        wrong = [vis] + others + [ans + 1, ans - 1]
        q = fig(solid_cv(view).svg("a %s" % kind)) + "This is %s %s. How many %s does it have?" % (art(kind), kind, what)
        e = "%s %s has %d faces, %d edges and %d vertices. %s" % (art(kind).capitalize(), kind, F, E, V, hidden[what])
        if kind == SP and what == "vertices":
            e += " Do not forget the vertex at the top."
        its.append(mcq(q, ans, wrong, e))
    its.append(mcq("How many vertices does a cuboid have?", 8, [12, 6, 4],
                   "A cuboid has 8 vertices: 4 at the top and 4 at the bottom. 12 is the number of edges."))
    its.append(mcq("Which 3-D shape has 5 vertices?", SP, [TP, CUBE, CONE],
                   "A square-based pyramid has 4 vertices round the square and 1 at the top: 4 + 1 = 5."))
    its.append(mcq("Which 3-D shape has no flat faces, no edges and no vertices?", SPH, [CYL, CONE, CUBE],
                   "A sphere is round all over, like a ball. It has only one curved surface."))
    its.append(mcq("How many flat faces does a cylinder have?", 2, [1, 3, 0],
                   "A cylinder has 2 flat circle faces, one at each end, and a curved surface."))
    its.append(mcq("How many flat faces does a cone have?", 1, [2, 0, 3],
                   "A cone has 1 flat circle face. The rest is a curved surface that comes to a point."))
    n1, n2 = "Leo", "Zara"
    its.append(mcq("%s says a cube has 8 edges. He is wrong. What did he count?" % n1, "the vertices",
                   ["the faces", "the edges at the front", "the hidden faces"],
                   "A cube has 8 vertices (corners) and 12 edges. %s counted the vertices." % n1))
    its.append(mcq("%s counts 12 on a cuboid. She counted correctly. What did she count?" % n2, "the edges",
                   ["the faces", "the vertices", "the faces you can see"],
                   "A cuboid has 6 faces, 12 edges and 8 vertices. So 12 is the number of edges."))
    assert len(its) == 20, len(its)
    return {"title": "Faces, edges and vertices", "items": its}


# ------------------------------------------------------------ set 4: faces and models
def set_models(rnd, P):
    its = []
    its.append(mcq(fig(cylinder_cv().svg("a cylinder")) + "What shape are the 2 flat faces of this cylinder?", "circles",
                   ["rectangles", "ovals", "spheres"],
                   "Each end of a cylinder is a flat circle. It looks like an oval in the picture because we see it from the side."))
    its.append(mcq(fig(cone_cv().svg("a cone")) + "What shape is the flat face of this cone?", "a circle",
                   ["a triangle", "a square", "a semicircle"],
                   "The flat face at the bottom of a cone is a circle. The cone looks like a triangle from the side, but it has no triangle faces."))
    its.append(mcq(fig(solid_cv("cube").svg("a cube")) + "How many square faces does a cube have?", 6, [3, 4, 8],
                   "A cube has 6 square faces. You can see 3 of them; 3 more are at the back and underneath."))
    its.append(mcq("Which 2-D shapes are the faces of a triangular prism?", "2 triangles and 3 rectangles",
                   ["3 triangles and 2 rectangles", "2 triangles and 2 rectangles", "1 triangle and 4 rectangles"],
                   "A triangular prism has a triangle at each end (2 triangles) and 3 rectangles joining them: 5 faces."))
    its.append(mcq("Which 2-D shapes are the faces of a square-based pyramid?", "1 square and 4 triangles",
                   ["4 squares and 1 triangle", "1 square and 3 triangles", "2 squares and 4 triangles"],
                   "A square-based pyramid has 1 square at the bottom and 4 triangles that meet at the top: 5 faces."))
    n, he, his = P.next()
    its.append(mcq("%s dips the end of a cylinder in paint. Then %s presses it on paper. What shape does %s print?" % (n, he, he),
                   "a circle", ["a rectangle", "a cylinder", "a triangle"],
                   "The end of a cylinder is a flat circle face, so it prints a circle. A print is always a flat 2-D shape."))
    n, he, his = P.next()
    its.append(mcq("%s prints with the bottom face of a square-based pyramid. What shape does %s print?" % (n, he),
                   "a square", ["a triangle", "a pyramid", "a circle"],
                   "The base of a square-based pyramid is a square, so it prints a square. The other faces would print triangles."))
    its.append(mcq("Which 3-D shape has 2 circle faces and a curved surface?", CYL, [CONE, SPH, "circle"],
                   "A cylinder has 2 circle faces (one at each end) and a curved surface. A cone has only 1 circle face."))
    its.append(mcq("Which 3-D shape has 1 circle face and comes to a point?", CONE, [CYL, SPH, SP],
                   "A cone has 1 circle face and a curved surface that comes to a point. A pyramid also has a point, but its base is a square."))
    its.append(mcq("Which 3-D shape has some triangle faces?", SP, [CUBE, CYL, CUBOID],
                   "A square-based pyramid has 4 triangle faces. Cubes and cuboids have squares and rectangles, and a cylinder has circles."))
    its.append(mcq("Which 3-D shape can roll?", CYL, [CUBE, CUBOID, SP],
                   "A cylinder has a curved surface, so it can roll. Shapes with only flat faces slide but do not roll."))
    # straw-and-clay models
    for view, kind in [("cube", CUBE), ("tp_lying", TP), ("sp", SP)]:
        F, E, V = COUNTS[kind]
        q = (fig(model_cv(view).svg("a model made from straws and balls of clay"))
             + "This model is made from straws and balls of clay. Which 3-D shape is it?")
        e = ("It has %d straws (edges) and %d balls of clay (vertices). %s"
             % (E, V, {CUBE: "All the edges are the same length, so it is a cube.",
                       TP: "It has 2 triangles at the ends joined by 3 straws, so it is a triangular prism.",
                       SP: "It has a square at the bottom and 4 straws going up to one point, so it is a square-based pyramid."}[kind]))
        its.append(mcq(q, kind, {CUBE: [CUBOID, SP, TP], TP: [SP, CUBOID, CUBE], SP: [TP, CONE, CUBE]}[kind], e))
    rule = " Each straw makes an edge and each ball of clay makes a vertex."
    its.append(mcq("You make a cube from straws and balls of clay. How many straws do you need?", 12, [8, 6, 24],
                   "A cube has 12 edges, so you need 12 straws. 8 is the number of vertices (balls of clay)." + rule))
    its.append(mcq("You make a cube from straws and balls of clay. How many balls of clay do you need?", 8, [12, 6, 4],
                   "A cube has 8 vertices, so you need 8 balls of clay: 4 at the top and 4 at the bottom." + rule))
    its.append(mcq("You make a triangular prism from straws and balls of clay. What do you need?", "9 straws and 6 balls",
                   ["6 straws and 9 balls", "9 straws and 5 balls", "6 straws and 5 balls"],
                   "A triangular prism has 9 edges (3 on each triangle and 3 joining them) and 6 vertices." + rule))
    its.append(mcq("How many straws do you need to make a square-based pyramid?", 8, [5, 4, 12],
                   "A square-based pyramid has 8 edges: 4 round the square and 4 going up to the top." + rule))
    its.append(mcq("Which 3-D shape can you NOT make from straight straws and balls of clay?", SPH, [CUBE, TP, SP],
                   "A sphere is curved all over and has no edges or vertices, so straight straws cannot make it."))
    n, he, his = P.next()
    its.append(mcq("%s has 6 balls of clay and 9 straws. %s uses them all to make one 3-D shape. Which shape?" % (n, he.capitalize()),
                   TP, [SP, CUBE, CUBOID],
                   "6 vertices and 9 edges: that is a triangular prism. A square-based pyramid has 5 vertices and 8 edges."))
    assert len(its) == 20, len(its)
    return {"title": "Faces of 3-D shapes and making models", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_problems(rnd, P):
    its = []
    for obj, kind, wrong, e in [
            ("a tin of beans", CYL, [CONE, CUBOID, "circle"], "A tin has 2 circle ends and a curved side, so it is a cylinder."),
            ("a dice", CUBE, [CUBOID, "square", SP], "A dice has 6 square faces that are all the same size, so it is a cube."),
            ("a football", SPH, ["circle", CYL, CONE], "A football is round all over, so it is a sphere. A circle is flat."),
            ("a long chocolate box with a triangle at each end", TP, [SP, CUBOID, CONE],
             "2 triangle ends joined by 3 rectangles make a triangular prism."),
            ("an ice-cream cone", CONE, [CYL, "triangle", SP], "It has a circle at the top, a curved side and a point at the bottom, so it is a cone."),
            ("a cereal box", CUBOID, [CUBE, "rectangle", TP], "A cereal box has 6 rectangle faces that are not all squares, so it is a cuboid."),
            ("an Egyptian pyramid with a square base", SP, [TP, CONE, CUBE],
             "It has a square base and 4 triangle faces that meet at the top, so it is a square-based pyramid."),
    ]:
        its.append(mcq("What 3-D shape is %s?" % obj, kind, wrong, e))
    n, he, his = P.next()
    its.append(mcq("%s uses 6 lolly sticks to make a closed 2-D shape. Each stick is one side. What shape does %s make?" % (n, he),
                   "a hexagon", ["a pentagon", "an octagon", "a cube"], "6 sides make a hexagon."))
    n, he, his = P.next()
    its.append(mcq("%s cuts a circle in half with one straight cut through the middle. What shape is each piece?" % n,
                   "a semicircle", ["a triangle", "a circle", "an oval"], "Half of a circle is a semicircle. It has 1 curved side and 1 straight side."))
    n, he, his = P.next()
    its.append(mcq("%s draws a 2-D shape with 8 straight sides. What is it called?" % n, "an octagon",
                   ["a hexagon", "a pentagon", "a cuboid"], "8 sides make an octagon. 6 sides make a hexagon."))
    its.append(mcq("A STOP road sign is an octagon. How many vertices does it have?", 8, [6, 7, 9],
                   "An octagon has 8 sides and 8 vertices."))
    n, he, his = P.next()
    its.append(mcq("%s makes 2 cubes from straws. How many straws does %s use?" % (n, he), 24, [12, 16, 20],
                   "1 cube needs 12 straws (12 edges). 2 cubes: 12 + 12 = 24 straws. 16 uses the vertices (8 + 8)."))
    n, he, his = P.next()
    its.append(mcq("%s has 20 straws. %s makes one cube. How many straws are left?" % (n, he.capitalize()), 8, [12, 14, 32],
                   "A cube uses 12 straws (12 edges). 20 − 12 = 8 straws left. 14 comes from taking away 6 faces instead of 12 edges."))
    n, he, his = P.next()
    its.append(mcq("%s makes a triangular prism and a square-based pyramid. %s puts a ball of clay at every vertex. How many balls does %s use?"
                   % (n, he.capitalize(), he), 11, [17, 10, 12],
                   "A triangular prism has 6 vertices and a square-based pyramid has 5. 6 + 5 = 11. 17 adds the edges (9 + 8)."))
    n, he, his = P.next()
    its.append(mcq("%s puts a sticker on every face of 3 dice. How many stickers does %s use?" % (n, he), 18, [24, 36, 9],
                   "A dice is a cube with 6 faces. 3 dice: 6 + 6 + 6 = 18 stickers. 24 uses the vertices and 36 uses the edges."))
    n, he, his = P.next()
    its.append(mcq("%s counts all the vertices on 2 square-based pyramids. How many vertices are there?" % n, 10, [8, 16, 5],
                   "Each pyramid has 5 vertices: 4 round the square and 1 at the top. 5 + 5 = 10. 8 forgets the top vertices."))
    n, he, his = P.next()
    its.append(mcq("%s has a cube, a cylinder, a sphere, a cone and a cuboid. How many of them have a curved surface?" % n,
                   3, [2, 4, 5], "The cylinder, the sphere and the cone have curved surfaces: 3 shapes. The cube and cuboid have only flat faces."))
    n, he, his = P.next()
    its.append(mcq("%s cuts out 3 triangles and 2 squares from card. How many vertices do they have altogether?" % n, 17, [5, 20, 13],
                   "3 triangles: 3 + 3 + 3 = 9. 2 squares: 4 + 4 = 8. 9 + 8 = 17 vertices. 5 counts the shapes, not the vertices."))
    its.append(mcq("A tin of beans has a paper label all the way round. Which part of the tin does the label cover?",
                   "the curved surface", ["a flat face", "an edge", "the vertices"],
                   "The label goes round the side of the tin. That is the curved surface of the cylinder. The 2 flat faces are the top and bottom."))
    n, he, his = P.next()
    its.append(mcq("%s holds a 3-D shape with 6 faces, 12 edges and 8 vertices. Not all of its faces are squares. What shape is it?" % n,
                   CUBOID, [CUBE, TP, SP],
                   "Cubes and cuboids both have 6 faces, 12 edges and 8 vertices. All the faces of a cube are squares, so this is a cuboid."))
    assert len(its) == 20, len(its)
    return {"title": "Shapes all around us: word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    flat = row_svg([shape2d("tri_eq", 0, 0.8), shape2d("square", 0, 0.8), shape2d("rect", 0, 0.7), shape2d("pent_reg", 0, 0.8),
                    shape2d("hex_reg", 0, 0.8), shape2d("oct_reg", 0, 0.8), circle_cv(32), semi_cv(36)],
                   ["triangle", "square", "rectangle", "pentagon", "hexagon", "octagon", "circle", "semicircle"],
                   "triangle, square, rectangle, pentagon, hexagon, octagon, circle and semicircle", gap=16, fs=14)
    turned = row_svg([shape2d("square", 0, 0.9), shape2d("square", 45, 0.9), shape2d("hex_reg", 0, 0.8), shape2d("hex_L", 0, 0.75)],
                     ["square", "still a square", "hexagon", "also a hexagon"],
                     "a square and the same square turned; a regular hexagon and a hexagon with unequal sides", gap=26, fs=14)
    solids = row_svg([solid_cv("cube", 44), solid_cv("cuboid_flat", 44), solid_cv("tp_lying", 46), solid_cv("sp", 46)],
                     ["cube", "cuboid", "triangular prism", "square-based pyramid"],
                     "cube, cuboid, triangular prism and square-based pyramid", gap=22, fs=14)
    curved = row_svg([cylinder_cv(0.85), cone_cv(0.85), sphere_cv(0.9)], ["cylinder", "cone", "sphere"],
                     "cylinder, cone and sphere", gap=40, fs=14)
    positions = row_svg([solid_cv("tp_lying", 44), solid_cv("tp_standing", 44), cone_cv(0.8), cone_cv(0.8, "down")],
                        ["lying down", "standing up", "point up", "point down"],
                        "a triangular prism and a cone in different positions", gap=26, fs=14)
    model = row_svg([solid_cv("cube", 52), model_cv("cube", 52)], ["cube", "straw-and-clay model"],
                    "a cube and a model of a cube made from straws and balls of clay", gap=40, fs=14)
    return (
        "<h2>2-D shapes</h2>"
        "<p>A 2-D shape is <b>flat</b>. Count its straight <b>sides</b> to find its name. "
        "A <b>vertex</b> is a corner where two sides meet. Two or more are called <b>vertices</b>.</p>"
        "<figure class='sn-fig'>" + flat + "</figure>" +
        table(["Shape", "Sides", "Vertices"], [
            ["Triangle", "3", "3"], ["Square, rectangle", "4", "4"], ["Pentagon", "5", "5"],
            ["Hexagon", "6", "6"], ["Octagon", "8", "8"], ["Circle", "1 curved side", "0"],
            ["Semicircle", "1 straight side, 1 curved side", "2"]]) +
        "<p>Turning a shape does not change its name. The sides do not have to be equal.</p>"
        "<figure class='sn-fig'>" + turned +
        "<figcaption>A turned square is still a square, not a “diamond”. Any shape with 6 straight sides is a hexagon.</figcaption></figure>" +
        ex("Example 1", "A shape has 5 straight sides. Two of them are longer than the others. What is it called?",
           "Count the sides: 5. The lengths do not matter.", "a pentagon") +
        "<h2>3-D shapes</h2>"
        "<p>A 3-D shape is <b>solid</b>, like a box or a ball. "
        "A <b>face</b> is a flat surface. An <b>edge</b> is where two faces meet. A <b>vertex</b> is a corner where edges meet. "
        "Dashed lines show edges at the back that you cannot see.</p>"
        "<figure class='sn-fig'>" + solids + "</figure>"
        "<figure class='sn-fig'>" + curved +
        "<figcaption>A cylinder, a cone and a sphere have a curved surface, so they can roll.</figcaption></figure>" +
        table(["Shape", "Faces", "Edges", "Vertices", "Example"], [
            ["Cube", "6 (all squares)", "12", "8", "a dice"],
            ["Cuboid", "6 (rectangles)", "12", "8", "a cereal box"],
            ["Triangular prism", "5 (2 triangles, 3 rectangles)", "9", "6", "a tent"],
            ["Square-based pyramid", "5 (1 square, 4 triangles)", "8", "5", "an Egyptian pyramid"],
            ["Cylinder", "2 flat circles and a curved surface", "2 curved", "0", "a tin of beans"],
            ["Cone", "1 flat circle and a curved surface", "1 curved", "1 (the point)", "an ice-cream cone"],
            ["Sphere", "1 curved surface", "0", "0", "a football"]]) +
        "<p>A 3-D shape keeps its name when it is turned, lying down or upside down.</p>"
        "<figure class='sn-fig'>" + positions + "</figure>" +
        ex("Example 2", "How many faces does a cube have?",
           "You can see 3 faces in a picture. There are 3 more at the back, on the left and underneath. 3 + 3 = 6.", "6 faces") +
        "<h2>Making 3-D shapes</h2>"
        "<p>You can make a model of a 3-D shape with straws and balls of modelling clay. "
        "Each <b>straw</b> is an <b>edge</b>. Each <b>ball of clay</b> is a <b>vertex</b>.</p>"
        "<figure class='sn-fig'>" + model +
        "<figcaption>A cube needs 12 straws (12 edges) and 8 balls of clay (8 vertices).</figcaption></figure>" +
        ex("Example 3", "How many straws and balls of clay do you need for a square-based pyramid?",
           "Edges: 4 round the square and 4 up to the top = 8. Vertices: 4 round the square and 1 at the top = 5.",
           "8 straws and 5 balls of clay") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Calling a turned square a “diamond”", "Check the sides and angles: 4 equal sides and 4 right angles make a square"],
            ["Thinking a hexagon must have equal sides", "Any shape with 6 straight sides is a hexagon"],
            ["Counting only the faces you can see", "Remember the faces at the back and underneath"],
            ["Mixing up edges and vertices", "Edges are the lines (straws); vertices are the corners (clay balls)"],
            ["Mixing up a cylinder and a cone", "A cylinder has 2 circle faces; a cone has 1 circle face and a point"],
            ["Mixing up a prism and a pyramid", "A pyramid comes to a point; a prism has the same shape at both ends"],
            ["Using a 2-D name for a 3-D shape", "A ball is a sphere, not a circle; a dice is a cube, not a square"],
        ])
    )


FAQ = [
    {"q": "What 2-D and 3-D shapes should a Year 3 child know?",
     "a": "2-D: triangle, square, rectangle, pentagon, hexagon, octagon, circle and semicircle. 3-D: cube, cuboid, cylinder, cone, sphere, square-based pyramid and triangular prism."},
    {"q": "What is the difference between a face, an edge and a vertex?",
     "a": "A face is a flat surface, an edge is where two faces meet, and a vertex is a corner where edges meet. A cube has 6 faces, 12 edges and 8 vertices."},
    {"q": "Is a diamond a square?",
     "a": "“Diamond” is not a maths name. A square turned on its corner is still a square. A shape with 4 equal sides but no right angles is a rhombus."},
    {"q": "How can I help my child learn 3-D shapes at home?",
     "a": "Look for shapes around the house, such as a tin of beans (cylinder) or a cereal box (cuboid), and count the faces, edges and vertices together. Making shapes with straws and modelling clay helps too."},
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
    """Tag pictures that must print larger (A-D choices, pairs) so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(3313)
    P = People(rnd)
    pos = Pos(rnd)
    sets = [set_2d(rnd, pos), set_name3d(rnd, pos), set_fev(rnd), set_models(rnd, P), set_problems(rnd, P)]
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
        "country": "uk", "subject": "maths", "grade": "year-3", "slug": "2d-and-3d-shapes", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "2-D and 3-D Shapes: Names, Faces, Edges and Vertices",
        "seo_title": "Year 3 2-D and 3-D Shapes Worksheets: Sides, Faces, Edges and Vertices (Free, with Answers)",
        "short_title": "2-D and 3-D shapes",
        "domain": "Geometry – properties of shapes",
        "standard_code": "Year 3: Geometry – properties of shapes",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Draw 2-D shapes and make 3-D shapes using modelling materials; recognise 3-D shapes in different orientations and describe them.",
        "meta_desc": "Free Year 3 maths worksheets on 2-D and 3-D shapes: name triangles, pentagons, hexagons and octagons, recognise cubes, cuboids, cylinders, cones, spheres, pyramids and prisms in any position, count faces, edges and vertices, and make shapes with straws and clay. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "Count the sides to name a 2-D shape. Faces, edges and vertices describe a 3-D shape.",
        "key_sub": "A shape keeps its name when it is turned. A face is a flat surface, an edge is where two faces meet, and a vertex is a corner. Remember the faces you cannot see.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(four [a-z0-9-]+ shapes labelled A to D|the same 3-D shape in two positions)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
