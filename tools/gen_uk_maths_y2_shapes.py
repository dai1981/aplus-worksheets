# -*- coding: utf-8 -*-
"""
UK Year 2 Maths: 2-D and 3-D shapes (National Curriculum in England, Geometry – properties of shapes)
  python3 tools/gen_uk_maths_y2_shapes.py
HTML attributes use single quotes (no backslashes in the JSON). British English, short sentences for 6–7 year olds.

Year 2 names 2-D shapes (circle, triangle, square, rectangle, pentagon, hexagon, octagon) and counts their
sides and vertices; checks a vertical line of symmetry; names 3-D shapes (cube, cuboid, pyramid, cylinder,
cone, sphere) and counts faces, edges and vertices; finds 2-D shapes on the faces of 3-D shapes; sorts and
compares shapes and everyday objects.

Pictures (checked in code):
  2-D shapes  drawn from their corner points; the number of sides is the number of points
  symmetry    every dashed line is tested in code by reflecting the shape in it (a line of symmetry
              maps the shape onto itself); "not a line" pictures are also checked to cut the shape
  3-D shapes  drawn from 3-D vertices and faces (V − E + F = 2 checked); "only counted what you can see"
              wrong answers are counted from the same picture
Wrong answers come from real pupil mistakes: a turned square called a diamond, sides miscounted, a 3-D shape
given its 2-D name (circle for sphere), cylinder vs cone, cube vs cuboid, hidden faces not counted,
edges and vertices swapped, a diagonal or off-centre line taken as a line of symmetry.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL, SIDE, TOP3 = "#cfe6d6", "#a9d3b6", "#e6f2e9"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]

CUBE, CUBOID, PYR, CYL, CONE, SPH = "cube", "cuboid", "pyramid", "cylinder", "cone", "sphere"


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
                            " stroke-dasharray='6 4'" if dashed else " stroke-linecap='round'"))
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


SHAPES2D = {
    "tri_eq": reg(3, 42),
    "tri_right": [(0, 0), (0, 60), (80, 60)],
    "tri_thin": [(0, 0), (100, 20), (20, 45)],
    "square": [(0, 0), (62, 0), (62, 62), (0, 62)],
    "rect": [(0, 0), (100, 0), (100, 50), (0, 50)],
    "rhombus": [(0, 0), (60, 0), (60 + 60 * math.cos(math.radians(55)), 60 * math.sin(math.radians(55))),
                (60 * math.cos(math.radians(55)), 60 * math.sin(math.radians(55)))],
    "pent_reg": reg(5, 44),
    "pent_house": [(0, 40), (40, 0), (80, 40), (80, 100), (0, 100)],
    "pent_odd": [(0, 0), (90, 0), (110, 45), (50, 80), (0, 55)],
    "hex_reg": reg(6, 44, 0),
    "hex_L": [(0, 0), (40, 0), (40, 55), (90, 55), (90, 95), (0, 95)],
    "hex_arrow": [(0, 20), (60, 20), (60, 0), (100, 40), (60, 80), (60, 60)],
    "oct_reg": reg(8, 44, 22.5),
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


def n_sides(key):
    return len(SHAPES2D[key])


# ------------------------------------------------------------ symmetry (y down; every shape centred on x = 0)
def arcp(cx, cy, rx, ry, a0, a1, n):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def heart(k=2.6, n=64):
    out = []
    for i in range(n):
        t = 2 * math.pi * i / n
        out.append((k * 16 * math.sin(t) ** 3, -k * (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))))
    return out


def star(r1=46, r2=19):
    return [((r1 if i % 2 == 0 else r2) * math.cos(math.radians(-90 + 36 * i)),
             (r1 if i % 2 == 0 else r2) * math.sin(math.radians(-90 + 36 * i))) for i in range(10)]


SYM = {
    # shapes with a vertical line of symmetry down the middle
    "isos": [(0, -48), (36, 42), (-36, 42)],
    "house": [(-36, -6), (0, -46), (36, -6), (36, 44), (-36, 44)],
    "arrow_up": [(0, -48), (40, -8), (16, -8), (16, 44), (-16, 44), (-16, -8), (-40, -8)],
    "heart": heart(),
    "rect": [(-42, -26), (42, -26), (42, 26), (-42, 26)],
    "square": [(-32, -32), (32, -32), (32, 32), (-32, 32)],
    "hex": reg(6, 42, 0),
    "star": star(),
    "dome": arcp(0, 22, 46, 46, 180, 360, 36),
    "pent": reg(5, 44),
    "oct": reg(8, 42, 22.5),
    # shapes with no vertical line of symmetry
    "rtri": [(-36, -44), (-36, 40), (40, 40)],
    "scalene": [(-46, 34), (44, 34), (22, -40)],
    "para": [(-22, -26), (48, -26), (22, 26), (-48, 26)],
    "L": [(-34, -44), (-6, -44), (-6, 16), (34, 16), (34, 44), (-34, 44)],
    "arrow_right": [(-44, -14), (6, -14), (6, -38), (44, 0), (6, 38), (6, 14), (-44, 14)],
    "trap_right": [(-40, 36), (40, 36), (40, -36), (-6, -36)],
    "flag": [(-30, -44), (34, -22), (-30, 0), (-30, 44), (-38, 44), (-38, -44)],
}
CIRCLE = "circle"


def bbox(pts):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def refl(p, c, a):
    d = (math.cos(math.radians(a)), math.sin(math.radians(a)))
    v = (p[0] - c[0], p[1] - c[1])
    t = v[0] * d[0] + v[1] * d[1]
    return (2 * (c[0] + d[0] * t) - p[0], 2 * (c[1] + d[1] * t) - p[1])


def is_axis(key, c, a):
    """True if the line through c at angle a (degrees, 90 = up and down) maps the shape onto itself."""
    if key == CIRCLE:
        r = refl((0, 0), c, a)
        return math.hypot(*r) < 1e-6
    pts = SYM[key]
    for p in pts:
        r = refl(p, c, a)
        if min(math.hypot(r[0] - x, r[1] - y) for x, y in pts) > 0.05:
            return False
    return True


def cuts(key, c, a):
    """The line really goes through the shape (some of it on each side)."""
    pts = SYM[key] if key != CIRCLE else arcp(0, 0, 42, 42, 0, 360, 72)
    nx, ny = -math.sin(math.radians(a)), math.cos(math.radians(a))
    sd = [(x - c[0]) * nx + (y - c[1]) * ny for x, y in pts]
    return min(sd) < -8 and max(sd) > 8


# expected: which shapes have a vertical line of symmetry through the middle
VSYM = {"isos", "house", "arrow_up", "heart", "rect", "square", "hex", "star", "dome", "pent", "oct", CIRCLE}
for _k in list(SYM) + [CIRCLE]:
    assert is_axis(_k, (0, 0), 90) == (_k in VSYM), _k


def line_for(key, kind):
    """A dashed line: 'mid' vertical through the middle, 'off' vertical off-centre, 'diag', 'across'.
    Returns (point, angle)."""
    x0, y0, x1, y1 = bbox(SYM[key]) if key != CIRCLE else (-42, -42, 42, 42)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if key in VSYM:
        assert abs(cx) < 1e-6, key
    w = x1 - x0
    if kind == "mid":
        return (cx, cy), 90
    if kind == "off":
        return (cx + 0.24 * w, cy), 90
    if kind == "diag":
        return (cx, cy), 60
    if kind == "across":
        return (cx, cy), 0
    raise KeyError(kind)


def seg_in_box(c, a, box, m=10):
    """End points of the line through c at angle a inside box grown by m."""
    x0, y0, x1, y1 = box[0] - m, box[1] - m, box[2] + m, box[3] + m
    d = (math.cos(math.radians(a)), math.sin(math.radians(a)))
    ts = []
    if abs(d[0]) > 1e-9:
        for X in (x0, x1):
            t = (X - c[0]) / d[0]
            y = c[1] + t * d[1]
            if y0 - 1e-6 <= y <= y1 + 1e-6:
                ts.append(t)
    if abs(d[1]) > 1e-9:
        for Y in (y0, y1):
            t = (Y - c[1]) / d[1]
            x = c[0] + t * d[0]
            if x0 - 1e-6 <= x <= x1 + 1e-6:
                ts.append(t)
    t0, t1 = min(ts), max(ts)
    return (c[0] + t0 * d[0], c[1] + t0 * d[1]), (c[0] + t1 * d[0], c[1] + t1 * d[1])


def sym_cv(key, kind="mid", k=1.0):
    """Shape with a red dashed line. Returns (canvas, is the line a line of symmetry)."""
    c, a = line_for(key, kind)
    assert cuts(key, c, a), (key, kind)
    yes = is_axis(key, c, a)
    if kind != "mid":
        assert not yes or key in (CIRCLE, "square", "rect", "hex", "oct"), (key, kind)
    box = bbox(SYM[key]) if key != CIRCLE else (-42, -42, 42, 42)
    A, B = seg_in_box(c, a, box)
    S = lambda p: (p[0] * k, p[1] * k)
    cv = Canvas()
    if key == CIRCLE:
        cv.circle((0, 0), 42 * k, sw=3)
    else:
        cv.poly([S(p) for p in SYM[key]], FILL, 3)
    cv.line(S(A), S(B), dashed=True, sw=2.6, col=RED)
    return cv, yes


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


def box(L, H, W):
    v = [(x, y, z) for x in (0, L) for y in (0, H) for z in (0, W)]
    idx = {p: i for i, p in enumerate(v)}
    g = lambda *ps: [idx[p] for p in ps]
    f = [g((0, 0, 0), (L, 0, 0), (L, H, 0), (0, H, 0)), g((0, 0, W), (L, 0, W), (L, H, W), (0, H, W)),
         g((0, 0, 0), (0, 0, W), (0, H, W), (0, H, 0)), g((L, 0, 0), (L, 0, W), (L, H, W), (L, H, 0)),
         g((0, 0, 0), (L, 0, 0), (L, 0, W), (0, 0, W)), g((0, H, 0), (L, H, 0), (L, H, W), (0, H, W))]
    return Solid(v, f)


def pyramid(s=1.3, h=1.3):
    v = [(0, 0, 0), (s, 0, 0), (s, 0, s), (0, 0, s), (s / 2, h, s / 2)]
    f = [[0, 1, 2, 3]] + [[i, (i + 1) % 4, 4] for i in range(4)]
    return Solid(v, f)


COUNTS = {CUBE: (6, 12, 8), CUBOID: (6, 12, 8), PYR: (5, 8, 5)}
VIEWS = {
    "cube": (lambda: box(1.1, 1.1, 1.1), 30, 22),
    "cube_turned": (lambda: box(1.1, 1.1, 1.1), 50, 30),
    "cuboid_flat": (lambda: box(1.9, 0.8, 1.0), 25, 22),
    "cuboid_tall": (lambda: box(0.8, 1.8, 0.6), 35, 18),
    "cuboid_turned": (lambda: box(1.6, 1.0, 0.7), -35, 24),
    "pyr": (lambda: pyramid(), 25, 18),
    "pyr_turned": (lambda: pyramid(1.2, 1.5), -30, 25),
}
VIEW_KIND = {"cube": CUBE, "cube_turned": CUBE, "cuboid_flat": CUBOID, "cuboid_tall": CUBOID, "cuboid_turned": CUBOID,
             "pyr": PYR, "pyr_turned": PYR}
for _v, (_f, _y, _p) in VIEWS.items():
    _s = _f()
    assert tuple(_s.count[x] for x in ("faces", "edges", "vertices")) == COUNTS[VIEW_KIND[_v]], _v
    _seen = _s.seen(_y, _p)
    assert 1 < _seen["faces"] < _s.count["faces"], (_v, _seen)


def solid_cv(view, k=50):
    f, yaw, pitch = VIEWS[view]
    return f().cv(k, yaw, pitch)


def seen(view):
    f, yaw, pitch = VIEWS[view]
    return f().seen(yaw, pitch)


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
    "triangle": "It has 3 straight sides and 3 vertices. It is a triangle.",
    "square": "It has 4 sides that are all the same length, and 4 square corners. It is a square.",
    "rectangle": "It has 4 sides and 4 square corners. 2 sides are long and 2 are short. It is a rectangle.",
    "pentagon": "Count the sides: 5 sides. It is a pentagon.",
    "hexagon": "Count the sides: 6 sides. It is a hexagon.",
    "octagon": "Count the sides: 8 sides. It is an octagon.",
}
TURNED = " Turning a shape does not change its name."


def set_2d(rnd):
    pos = Pos(rnd)
    its = []
    asks = ["What is this shape called?", "Name this shape.", "What shape is this?"]
    rows = [
        (circle_cv(38), "circle", ["sphere", "oval", "semicircle"],
         "It is flat and round, with no corners. It is a circle. A sphere is a 3-D shape, like a ball."),
        (shape2d("tri_eq", 0), "triangle", ["square", "pentagon", "cone"], NAME_E["triangle"]),
        (shape2d("tri_thin", 15), "triangle", ["rectangle", "pentagon", "hexagon"], NAME_E["triangle"] + " A long, thin triangle is still a triangle."),
        (shape2d("square", 0), "square", ["rectangle", "cube", "hexagon"], NAME_E["square"]),
        (shape2d("square", 45), "square", ["diamond", "triangle", "rectangle"],
         NAME_E["square"] + " It is only turned. “Diamond” is not its maths name."),
        (shape2d("rect", 0), "rectangle", ["square", "cuboid", "pentagon"], NAME_E["rectangle"]),
        (shape2d("rect", 90, 0.9), "rectangle", ["square", "triangle", "hexagon"], NAME_E["rectangle"] + TURNED),
        (shape2d("pent_reg", 0), "pentagon", ["hexagon", "octagon", "triangle"], NAME_E["pentagon"]),
        (shape2d("pent_house", 0, 0.85), "pentagon", ["hexagon", "triangle", "square"],
         NAME_E["pentagon"] + " The sides do not have to be the same length."),
        (shape2d("hex_reg", 0), "hexagon", ["octagon", "pentagon", "circle"], NAME_E["hexagon"]),
        (shape2d("hex_L", 0, 0.9), "hexagon", ["rectangle", "octagon", "pentagon"],
         NAME_E["hexagon"] + " The sides do not have to be the same length."),
        (shape2d("oct_reg", 0), "octagon", ["hexagon", "circle", "pentagon"], NAME_E["octagon"]),
    ]
    for i, (cv, ans, wrong, e) in enumerate(rows):
        its.append(mcq(fig(cv.svg("a 2-D shape")) + asks[i % 3], ans, wrong, e))
    for key, deg, s, what in [("hex_arrow", 0, 0.9, "sides"), ("pent_odd", 200, 0.85, "vertices"), ("oct_cut", 0, 0.8, "vertices")]:
        n = n_sides(key)
        q = fig(shape2d(key, deg, s).svg("a 2-D shape")) + "How many %s does this shape have?" % what
        one = "side" if what == "sides" else "vertex"
        e = ("Put your finger on one %s. Count each %s as you go round, until you get back to the start: %d %s."
             % (one, one, n, what))
        if key == "oct_cut":
            e += " Count the small corners too."
        its.append(mcq(q, n, [n - 1, n + 1, n + 2], e))
    its.append(mcq(fig(circle_cv(30).svg("a circle")) + "How many vertices (corners) does a circle have?", 0, [1, 4, 2],
                   "A circle has 1 curved side and no corners. So it has 0 vertices."))
    its.append(mcq("A shape has 6 straight sides. What is it called?", "hexagon", ["pentagon", "octagon", "cube"],
                   "6 sides make a hexagon. 5 sides make a pentagon. 8 sides make an octagon."))
    its.append(mcq("A shape has 4 sides. 2 sides are long and 2 are short. It has 4 square corners. What is it?", "rectangle",
                   ["square", "triangle", "cuboid"],
                   "4 sides and 4 square corners, with 2 long sides and 2 short sides: a rectangle. A square has 4 sides the same length."))
    p = pos.next()
    cells = [shape2d("pent_reg", 0, 0.8), shape2d("oct_reg", 0, 0.8), shape2d("square", 45, 0.85)]
    cells.insert(p, shape2d("hex_L", 90, 0.8))
    its.append(mcq_fixed(fig(grid_svg(cells, "four 2-D shapes labelled A to D")) + "Which shape is a hexagon?",
                         list("ABCD"), "ABCD"[p],
                         "%s has 6 sides, so it is a hexagon. The other shapes have 5, 8 and 4 sides." % "ABCD"[p]))
    p = pos.next()
    cells = [shape2d("rhombus", 62.5, 0.9), shape2d("rect", 0, 0.75), shape2d("tri_eq", 0, 0.9)]
    cells.insert(p, shape2d("square", 45, 0.95))
    its.append(mcq_fixed(fig(grid_svg(cells, "four 2-D shapes labelled A to D")) + "Which shape is a square?",
                         list("ABCD"), "ABCD"[p],
                         "%s has 4 sides that are the same length and 4 square corners. It is a square that is turned. "
                         "The other shape with equal sides has no square corners, so it is not a square." % "ABCD"[p]))
    assert len(its) == 20, len(its)
    return {"title": "2-D shapes: names, sides and vertices", "items": its}


# ------------------------------------------------------------ set 2: vertical line of symmetry
WHY_NO = {
    "off": "The line is not in the middle. One side is bigger than the other.",
    "diag": "The line goes across at a slant. If you fold on it, the two parts do not match.",
    "across": "The line goes across, not up and down. If you fold on it, the top and bottom do not match.",
    "mid": "The line is in the middle, but the two sides are different shapes. They do not match when you fold.",
}


def set_symmetry(rnd):
    pos = Pos(rnd)
    its = []
    S = 0.82
    # (a) which shape has a line of symmetry on the dashed line?
    for right, others in [
            ("isos", [("rtri", "mid"), ("house", "off"), ("para", "mid")]),
            ("heart", [("L", "mid"), ("star", "off"), ("scalene", "mid")]),
            ("house", [("arrow_right", "mid"), ("isos", "off"), ("trap_right", "mid")]),
            ("star", [("flag", "mid"), ("heart", "off"), ("rtri", "mid")]),
            ("arrow_up", [("para", "mid"), ("dome", "off"), ("L", "mid")]),
    ]:
        p = pos.next()
        cells = []
        for k, kind in others:
            cv, yes = sym_cv(k, kind, S)
            assert not yes, (k, kind)
            cells.append(cv)
        cv, yes = sym_cv(right, "mid", S)
        assert yes
        cells.insert(p, cv)
        its.append(mcq_fixed(fig(grid_svg(cells, "four shapes with dashed lines labelled A to D"))
                             + "Which dashed line is a line of symmetry?", list("ABCD"), "ABCD"[p],
                             "Fold %s on the dashed line: the two halves match exactly. In the others, the two sides "
                             "do not match, or the line is not in the middle." % "ABCD"[p]))
    # (b) on which shape is the dashed line NOT a line of symmetry?
    for wrong, others in [
            (("rtri", "mid"), ["rect", "hex", "dome"]),
            (("house", "off"), ["isos", "square", "arrow_up"]),
            (("arrow_right", "mid"), ["heart", "pent", "oct"]),
    ]:
        p = pos.next()
        cells = []
        for k in others:
            cv, yes = sym_cv(k, "mid", S)
            assert yes, k
            cells.append(cv)
        cv, yes = sym_cv(wrong[0], wrong[1], S)
        assert not yes
        cells.insert(p, cv)
        its.append(mcq_fixed(fig(grid_svg(cells, "four shapes with dashed lines labelled A to D"))
                             + "Which dashed line is NOT a line of symmetry?", list("ABCD"), "ABCD"[p],
                             "Look at %s. %s The other lines cut the shapes into two halves that match."
                             % ("ABCD"[p], WHY_NO[wrong[1]])))
    # (c) one shape, four lines
    for key in ["isos", "house", "heart", "arrow_up"]:
        p = pos.next()
        kinds = ["off", "diag", "across"]
        rnd.shuffle(kinds)
        cells = []
        for kind in kinds:
            cv, yes = sym_cv(key, kind, S)
            assert not yes
            cells.append(cv)
        cv, yes = sym_cv(key, "mid", S)
        assert yes
        cells.insert(p, cv)
        its.append(mcq_fixed(fig(grid_svg(cells, "the same shape with four different dashed lines labelled A to D"))
                             + "Which dashed line is a line of symmetry?", list("ABCD"), "ABCD"[p],
                             "%s goes straight down the middle. The two halves match when you fold. "
                             "A slanted line, a line across or a line that is not in the middle does not work here." % "ABCD"[p]))
    # (d) how many of these have a line of symmetry?
    for row in [
            [("isos", "mid"), ("rtri", "mid"), ("square", "mid"), ("L", "mid")],
            [("heart", "mid"), ("star", "mid"), ("para", "mid"), ("dome", "mid")],
            [("house", "off"), ("flag", "mid"), ("arrow_up", "mid"), ("scalene", "mid")],
            [("rect", "mid"), ("arrow_right", "mid"), ("hex", "mid"), (CIRCLE, "mid")],
            [("oct", "mid"), ("pent", "mid"), ("house", "mid"), ("square", "mid")],
    ]:
        cvs, n = [], 0
        for k, kind in row:
            cv, yes = sym_cv(k, kind, 0.72)
            cvs.append(cv)
            n += yes
        q = (fig(row_svg(cvs, [""] * 4, "a row of four shapes, each with a dashed line", gap=26))
             + "How many of the dashed lines are lines of symmetry?")
        its.append(mcq(q, n, [x for x in (n + 1, n - 1, n + 2, n - 2, n - 3) if 0 <= x <= 4],
                       "Fold each shape in your head on the dashed line. Do the two halves match? " +
                       ("Only 1 of them matches, so 1 line is a line of symmetry." if n == 1 else
                        "All 4 match, so all 4 lines are lines of symmetry." if n == 4 else
                        "%d of them match, so %d lines are lines of symmetry." % (n, n))))
    # (e) letters and words
    its.append(mcq("Which capital letter has a line of symmetry going straight down the middle?", "A", ["F", "L", "J"],
                   "A is the same on the left and the right, so a line down the middle is a line of symmetry. F, L and J do not match."))
    its.append(mcq("You fold a shape on a line. The two halves match exactly. What is the line called?",
                   "a line of symmetry", ["an edge", "a vertex", "a side"],
                   "When the two halves match exactly, the fold line is a line of symmetry."))
    its.append(mcq("Which capital letter does NOT have a line of symmetry going straight down the middle?", "S", ["T", "U", "M"],
                   "T, U and M are the same on both sides of a line down the middle. S is not."))
    assert len(its) == 20, len(its)
    return {"title": "Vertical lines of symmetry", "items": its}


# ------------------------------------------------------------ set 3: naming 3-D shapes; faces, edges, vertices
WRONG3 = {CUBE: [CUBOID, "square", PYR], CUBOID: [CUBE, "rectangle", CYL], PYR: [CONE, "triangle", CUBE],
          CYL: [CONE, "circle", CUBOID], CONE: [CYL, "triangle", PYR], SPH: ["circle", CYL, CONE]}
E3 = {
    CUBE: "It has 6 flat faces. They are all squares of the same size. It is a cube.",
    CUBOID: "It has 6 flat faces, and they are not all squares. It is a cuboid.",
    PYR: "It has a square at the bottom. Its triangle faces meet at a point at the top. It is a pyramid.",
    CYL: "It has 2 flat circle faces and a curved surface. It is a cylinder.",
    CONE: "It has 1 flat circle face. Its curved surface comes to a point. It is a cone.",
    SPH: "It is round all over, like a ball. It is a sphere. A circle is a flat 2-D shape.",
}
TURN3 = {"cube_turned": " It is turned, but it is still a cube.",
         "cuboid_tall": " It is standing on its end, but it is still a cuboid.",
         "pyr_turned": " It is turned, but it is still a pyramid.",
         "cyl_lying": " It is lying on its side, but it is still a cylinder.",
         "cone_down": " It is upside down, but it is still a cone."}


def set_3d(rnd):
    its = []
    asks = ["What is the name of this 3-D shape?", "Name this 3-D shape.", "What is this 3-D shape called?"]
    keys = ["cube", "cube_turned", "cuboid_flat", "cuboid_tall", "pyr", "pyr_turned", "cyl", "cyl_lying", "cone", "cone_down", "sphere"]
    for i, k in enumerate(keys):
        kind = KIND[k]
        its.append(mcq(fig(pic3d(k).svg("a 3-D shape")) + asks[i % 3], kind, WRONG3[kind], E3[kind] + TURN3.get(k, "")))
    hidden = {"faces": "Some faces are at the back and underneath. You cannot see them, but you must count them too.",
              "edges": "The dashed lines are edges at the back. Count them too.",
              "vertices": "Some vertices are at the back, where the dashed lines meet. Count them too."}
    for view, what in [("cube", "faces"), ("cube", "edges"), ("cube_turned", "vertices"), ("cuboid_turned", "faces"),
                       ("cuboid_flat", "vertices"), ("pyr", "faces"), ("pyr", "edges"), ("pyr_turned", "vertices")]:
        kind = VIEW_KIND[view]
        F, E, V = COUNTS[kind]
        cnt = {"faces": F, "edges": E, "vertices": V}
        ans = cnt[what]
        vis = seen(view)[what]
        assert vis < ans
        others = [cnt[w] for w in ("faces", "edges", "vertices") if w != what]
        wrong = [vis] + others + [ans + 1, ans - 1]
        if kind == PYR:
            q = fig(solid_cv(view).svg("a pyramid")) + "This pyramid has a square at the bottom. How many %s does it have?" % what
        else:
            q = fig(solid_cv(view).svg("a %s" % kind)) + "This is %s %s. How many %s does it have?" % (art(kind), kind, what)
        e = "%s %s has %d faces, %d edges and %d vertices. %s" % (
            "This pyramid" if kind == PYR else art(kind).capitalize(), "" if kind == PYR else kind, F, E, V, hidden[what])
        e = e.replace("pyramid  has", "pyramid has")
        if kind == PYR and what == "vertices":
            e += " Do not forget the vertex at the top."
        its.append(mcq(q, ans, wrong, e))
    its.append(mcq("A corner of a 3-D shape is called a …", "vertex", ["edge", "face", "side"],
                   "A corner is a vertex. An edge is where two faces meet. A face is a flat surface."))
    assert len(its) == 20, len(its)
    return {"title": "3-D shapes: faces, edges and vertices", "items": its}


# ------------------------------------------------------------ set 4: 2-D shapes on 3-D shapes
def set_faces(rnd, P):
    pos = Pos(rnd)
    its = []
    its.append(mcq(fig(cylinder_cv().svg("a cylinder")) + "What shape are the 2 flat faces of this cylinder?", "circles",
                   ["ovals", "rectangles", "squares"],
                   "Each end of a cylinder is a flat circle. In a picture it looks like an oval, because we see it from the side."))
    its.append(mcq(fig(cone_cv().svg("a cone")) + "What shape is the flat face of this cone?", "a circle",
                   ["a triangle", "an oval", "a square"],
                   "The flat face at the bottom of a cone is a circle. From the side a cone looks like a triangle, but it has no triangle faces."))
    its.append(mcq(fig(solid_cv("cube").svg("a cube")) + "What shape are the faces of this cube?", "squares",
                   ["triangles", "circles", "cubes"],
                   "All 6 faces of a cube are squares. A cube is a 3-D shape. Its faces are flat 2-D shapes."))
    its.append(mcq(fig(solid_cv("cuboid_flat").svg("a cuboid")) + "What shape are the faces of this cuboid?", "rectangles",
                   ["triangles", "circles", "cuboids"],
                   "The faces of this cuboid are rectangles. Each face has 4 sides and 4 square corners."))
    its.append(mcq(fig(solid_cv("pyr").svg("a pyramid")) + "What shape is the face at the bottom of this pyramid?", "a square",
                   ["a triangle", "a circle", "a pentagon"],
                   "This pyramid stands on a square face. The faces going up to the point are triangles."))
    its.append(mcq(fig(solid_cv("pyr_turned").svg("a pyramid")) + "What shape are the faces that meet at the top of this pyramid?",
                   "triangles", ["squares", "circles", "rectangles"],
                   "The faces that meet at the point are triangles. Only the bottom face is a square."))
    for obj, face, ans, wrong, e in [
            ("the end of a cylinder", "", "a circle", ["a rectangle", "a cylinder", "an oval"],
             "The end of a cylinder is a flat circle face. So it prints a circle. A print is always a flat 2-D shape."),
            ("a face of a cube", "", "a square", ["a rectangle", "a cube", "a triangle"],
             "Every face of a cube is a square. So it prints a square."),
            ("a slanted face of a pyramid", "", "a triangle", ["a square", "a pyramid", "a circle"],
             "The slanted faces go up to the point. They are triangles. So it prints a triangle."),
            ("the big flat face of a cereal box", "", "a rectangle", ["a square", "a cuboid", "a circle"],
             "A cereal box is a cuboid. Its big face is a long rectangle, not a square. So it prints a rectangle."),
    ]:
        n, he, his = P.next()
        its.append(mcq("%s dips %s in paint. Then %s presses it on paper. What shape does %s print?" % (n, obj, he, he), ans, wrong, e))
    its.append(mcq("Which 3-D shape has 2 flat circle faces?", CYL, [CONE, SPH, "circle"],
                   "A cylinder has a flat circle at each end: 2 circles. A cone has only 1 circle."))
    its.append(mcq("Which 3-D shape has 6 square faces?", CUBE, [CUBOID, PYR, "square"],
                   "A cube has 6 faces and they are all squares. A cuboid has rectangle faces."))
    its.append(mcq("Which 3-D shape has 1 flat circle face and a point?", CONE, [CYL, SPH, PYR],
                   "A cone has 1 circle face and its curved surface comes to a point. A pyramid has a point too, but its bottom is a square."))
    its.append(mcq("Which 3-D shape has a square face and triangle faces?", PYR, [CUBE, CUBOID, CONE],
                   "A pyramid can have a square at the bottom and triangles going up to the point. "
                   "A cube has only squares. A cone has a circle."))
    its.append(mcq("Which 3-D shape has no flat faces at all?", SPH, [CYL, CONE, CUBE],
                   "A sphere is round all over, like a ball. It has a curved surface and no flat faces."))
    its.append(mcq("How many square faces does a cube have?", 6, [3, 4, 8],
                   "A cube has 6 square faces. You can see 3 in a picture. 3 more are at the back and underneath."))
    its.append(mcq("A pyramid has a square at the bottom. How many triangle faces does it have?", 4, [5, 3, 1],
                   "There is 1 triangle on each side of the square. The square has 4 sides, so there are 4 triangles. 5 counts the square too."))
    its.append(mcq("How many flat circle faces does a cylinder have?", 2, [1, 3, 0],
                   "A cylinder has 1 flat circle at the top and 1 at the bottom: 2 circles."))
    p = pos.next()
    cells = [pic3d(k, 0.62) for k in ["cube", "pyr", "cuboid_flat"]]
    cells.insert(p, pic3d("cyl", 0.62))
    its.append(mcq_fixed(fig(grid_svg(cells, "four 3-D shapes labelled A to D")) + "Which 3-D shape has circle faces?",
                         list("ABCD"), "ABCD"[p],
                         "%s is a cylinder. Its 2 flat faces are circles. The others have squares, rectangles or triangles." % "ABCD"[p]))
    p = pos.next()
    cells = [pic3d(k, 0.62) for k in ["cube", "cyl", "sphere"]]
    cells.insert(p, pic3d("pyr", 0.62))
    its.append(mcq_fixed(fig(grid_svg(cells, "four 3-D shapes labelled A to D")) + "Which 3-D shape has triangle faces?",
                         list("ABCD"), "ABCD"[p],
                         "%s is a pyramid. Its faces that meet at the top are triangles." % "ABCD"[p]))
    assert len(its) == 20, len(its)
    return {"title": "2-D shapes on 3-D shapes", "items": its}


# ------------------------------------------------------------ set 5: sort and compare (word problems)
def set_problems(rnd, P):
    its = []
    for obj, kind, wrong, e in [
            ("a tin of beans", CYL, [CONE, CUBOID, "circle"], "A tin has 2 flat circle ends and a curved side. It is a cylinder."),
            ("a football", SPH, ["circle", CYL, CONE], "A football is round all over. It is a sphere. A circle is flat."),
            ("a dice", CUBE, [CUBOID, "square", PYR], "A dice has 6 square faces, all the same size. It is a cube."),
            ("a cereal box", CUBOID, [CUBE, "rectangle", CYL], "A cereal box has 6 flat faces. They are rectangles, not all squares. It is a cuboid."),
            ("a party hat", CONE, [CYL, "triangle", PYR], "A party hat has a circle at the bottom and a point at the top. It is a cone."),
    ]:
        its.append(mcq("What 3-D shape is %s?" % obj, kind, wrong, e))
    its.append(mcq("Which of these can roll?", "a ball", ["a dice", "a cereal box", "a book"],
                   "A ball is a sphere. It has a curved surface, so it can roll. The others have only flat faces."))
    its.append(mcq("Which of these can roll, and can also stand in a tall stack?", "a tin of beans",
                   ["a football", "a dice", "a party hat"],
                   "A tin is a cylinder. It rolls on its curved side and stacks on its flat circle faces. "
                   "A football rolls but will not stack."))
    n, he, his = P.next()
    its.append(mcq("%s sorts some 3-D shapes. Group 1: cube, cuboid, pyramid. Group 2: sphere, cylinder, cone. "
                   "What do the shapes in group 2 have?" % n,
                   "a curved surface", ["only flat faces", "8 vertices", "square faces"],
                   "A sphere, a cylinder and a cone all have a curved surface. They can roll. The shapes in group 1 have only flat faces."))
    its.append(mcq("Which 3-D shape is the odd one out: cube, cuboid, sphere, pyramid?", SPH, [CUBE, CUBOID, PYR],
                   "The sphere has no flat faces, no edges and no vertices. The other shapes all have flat faces, edges and vertices."))
    its.append(mcq("Which 2-D shape is the odd one out: triangle, square, circle, pentagon?", "circle",
                   ["triangle", "square", "pentagon"],
                   "A circle has a curved side and no corners. The others have straight sides and vertices."))
    n, he, his = P.next()
    its.append(mcq("%s has 2 dice. How many faces do the 2 dice have altogether?" % n, 12, [6, 16, 24],
                   "A dice is a cube with 6 faces. 6 + 6 = 12. 16 counts the vertices (8 + 8)."))
    n, he, his = P.next()
    its.append(mcq("%s puts a sticker on every vertex of a cube. How many stickers does %s use?" % (n, he), 8, [6, 12, 4],
                   "A cube has 8 vertices: 4 at the top and 4 at the bottom. 6 is the number of faces. 12 is the number of edges."))
    n, he, his = P.next()
    its.append(mcq("%s makes a pyramid from straws. Each edge is one straw. The pyramid has a square at the bottom. "
                   "How many straws does %s need?" % (n, he), 8, [5, 4, 12],
                   "The pyramid has 8 edges: 4 round the square and 4 going up to the top. So %s needs 8 straws. 5 is the number of vertices." % he))
    n, he, his = P.next()
    its.append(mcq("%s draws 2 triangles and 1 square. How many sides is that altogether?" % n, 10, [7, 3, 12],
                   "Each triangle has 3 sides and a square has 4. 3 + 3 + 4 = 10. 7 forgets one triangle."))
    its.append(mcq("A 3-D shape has 5 faces. 4 faces are triangles and 1 is a square. What is it?", PYR, [CUBE, CONE, "triangle"],
                   "A pyramid with a square at the bottom has 1 square face and 4 triangle faces: 5 faces."))
    its.append(mcq("A 3-D shape has 6 faces. They are all squares of the same size. What is it?", CUBE, [CUBOID, PYR, "square"],
                   "6 square faces, all the same size: it is a cube. A cuboid has rectangle faces."))
    its.append(mcq("Which object has 1 flat circle face and a point?", "an ice-cream cone",
                   ["a tin of beans", "an orange", "a tissue box"],
                   "An ice-cream cone is a cone. It has 1 circle at the top and a point at the bottom."))
    n, he, his = P.next()
    m, he2, his2 = P.next()
    its.append(mcq("%s counts the square faces on a cube. %s counts the triangle faces on a pyramid. How many more faces does %s count?"
                   % (n, m, n), 2, [10, 6, 4],
                   "A cube has 6 square faces. A pyramid has 4 triangle faces. 6 − 4 = 2 more. 10 adds them instead of finding the difference."))
    its.append(mcq("A STOP road sign is an octagon. How many sides does it have?", 8, [6, 5, 10],
                   "An octagon has 8 sides and 8 vertices."))
    n, he, his = P.next()
    its.append(mcq("%s has a rubber shaped like a cuboid. How many faces does it have?" % n, 6, [12, 3, 8],
                   "A cuboid has 6 faces: top, bottom, front, back, left and right. 3 is only the faces you can see at once. 12 is the edges and 8 is the vertices."))
    assert len(its) == 20, len(its)
    return {"title": "Sort and compare shapes: word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    flat = row_svg([circle_cv(30), shape2d("tri_eq", 0, 0.8), shape2d("square", 0, 0.8), shape2d("rect", 0, 0.7),
                    shape2d("pent_reg", 0, 0.75), shape2d("hex_reg", 0, 0.75), shape2d("oct_reg", 0, 0.75)],
                   ["circle", "triangle", "square", "rectangle", "pentagon", "hexagon", "octagon"],
                   "circle, triangle, square, rectangle, pentagon, hexagon and octagon", gap=16, fs=14)
    turned = row_svg([shape2d("square", 0, 0.9), shape2d("square", 45, 0.9), shape2d("hex_reg", 0, 0.8), shape2d("hex_L", 0, 0.75)],
                     ["square", "still a square", "hexagon", "also a hexagon"],
                     "a square and the same square turned; a hexagon and a hexagon with sides of different lengths", gap=26, fs=14)
    sym = row_svg([sym_cv("isos", "mid")[0], sym_cv("heart", "mid")[0], sym_cv("rtri", "mid")[0], sym_cv("isos", "diag")[0]],
                  ["yes", "yes", "no", "no"],
                  "shapes with dashed lines: two lines of symmetry and two lines that are not", gap=30, fs=16)
    solids = row_svg([solid_cv("cube", 44), solid_cv("cuboid_flat", 44), solid_cv("pyr", 46),
                      cylinder_cv(0.8), cone_cv(0.8), sphere_cv(0.85)],
                     ["cube", "cuboid", "pyramid", "cylinder", "cone", "sphere"],
                     "cube, cuboid, pyramid, cylinder, cone and sphere", gap=20, fs=14)
    return (
        "<h2>2-D shapes</h2>"
        "<p>A 2-D shape is <b>flat</b>. Count its <b>sides</b> to find its name. "
        "A <b>vertex</b> is a corner. Two or more corners are called <b>vertices</b>.</p>"
        "<figure class='sn-fig'>" + flat + "</figure>" +
        table(["Shape", "Sides", "Vertices"], [
            ["Circle", "1 curved side", "0"], ["Triangle", "3", "3"], ["Square", "4 (all the same length)", "4"],
            ["Rectangle", "4 (2 long, 2 short)", "4"], ["Pentagon", "5", "5"], ["Hexagon", "6", "6"], ["Octagon", "8", "8"]]) +
        "<p>Turning a shape does not change its name. The sides do not have to be the same length.</p>"
        "<figure class='sn-fig'>" + turned +
        "<figcaption>A turned square is still a square, not a “diamond”. Any shape with 6 straight sides is a hexagon.</figcaption></figure>" +
        ex("Example 1", "A shape has 5 straight sides. Two sides are longer than the others. What is it?",
           "Count the sides: 5. The lengths do not matter.", "a pentagon") +
        "<h2>Line of symmetry</h2>"
        "<p>Fold a shape on a line. If the two halves match exactly, the line is a <b>line of symmetry</b>. "
        "In Year 2 we look for a line going <b>straight down the middle</b> (a vertical line).</p>"
        "<figure class='sn-fig'>" + sym +
        "<figcaption>The first two lines are lines of symmetry. The third shape does not match when you fold it. "
        "The last line is slanted, so the two parts do not match.</figcaption></figure>" +
        ex("Example 2", "Is a line straight down the middle of a rectangle a line of symmetry?",
           "Fold the rectangle in half from left to right. The two halves are the same size and shape.", "yes") +
        "<h2>3-D shapes</h2>"
        "<p>A 3-D shape is <b>solid</b>, like a box or a ball. "
        "A <b>face</b> is a flat surface. An <b>edge</b> is where two faces meet. A <b>vertex</b> is a corner. "
        "Dashed lines show edges at the back that you cannot see.</p>"
        "<figure class='sn-fig'>" + solids + "</figure>" +
        table(["Shape", "Faces", "Edges", "Vertices", "Like a…"], [
            ["Cube", "6 squares", "12", "8", "dice"],
            ["Cuboid", "6 rectangles", "12", "8", "cereal box"],
            ["Pyramid (square at the bottom)", "1 square, 4 triangles", "8", "5", "Egyptian pyramid"],
            ["Cylinder", "2 flat circles and a curved surface", "2 curved edges", "0", "tin of beans"],
            ["Cone", "1 flat circle and a curved surface", "1 curved edge", "1 (the point)", "party hat"],
            ["Sphere", "a curved surface only", "0", "0", "football"]]) +
        "<p>The flat faces of 3-D shapes are 2-D shapes. A cube has square faces. A cylinder has circle faces. "
        "A pyramid has triangle faces.</p>" +
        ex("Example 3", "How many faces does a cube have?",
           "You can see 3 faces in a picture. There are 3 more at the back, on the other side and underneath. 3 + 3 = 6.", "6 faces") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Calling a turned square a “diamond”", "Check the sides: 4 sides the same length and 4 square corners make a square"],
            ["Counting only the faces you can see", "Remember the faces at the back and underneath"],
            ["Mixing up edges and vertices", "Edges are the lines where faces meet. Vertices are the corners"],
            ["Thinking any line through the middle is a line of symmetry", "Fold it in your head: both halves must match exactly"],
            ["Using a 2-D name for a 3-D shape", "A ball is a sphere, not a circle. A dice is a cube, not a square"],
            ["Mixing up a cylinder and a cone", "A cylinder has 2 circle faces. A cone has 1 circle face and a point"],
        ])
    )


FAQ = [
    {"q": "What 2-D and 3-D shapes should a Year 2 child know?",
     "a": "2-D: circle, triangle, square, rectangle, pentagon, hexagon and octagon. 3-D: cube, cuboid, pyramid, cylinder, cone and sphere."},
    {"q": "What is a vertical line of symmetry?",
     "a": "It is a line straight down the middle of a shape. If you fold the shape on it, the two halves match exactly."},
    {"q": "How many faces, edges and vertices does a cube have?",
     "a": "A cube has 6 square faces, 12 edges and 8 vertices. A cuboid has the same numbers, but its faces are rectangles."},
    {"q": "How can I help my child learn shapes at home?",
     "a": "Look for shapes around the house, such as a tin of beans (cylinder) or a cereal box (cuboid), and count the faces together. Fold paper shapes to find lines of symmetry."},
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
    rnd = random.Random(2211)
    P = People(rnd)
    sets = [set_2d(rnd), set_symmetry(rnd), set_3d(rnd), set_faces(rnd, P), set_problems(rnd, P)]
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
        "country": "uk", "subject": "maths", "grade": "year-2", "slug": "2d-and-3d-shapes", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "2-D and 3-D Shapes: Sides, Symmetry, Faces, Edges and Vertices",
        "seo_title": "Year 2 2-D and 3-D Shapes Worksheets: Sides, Symmetry and Faces (Free, with Answers)",
        "short_title": "2-D and 3-D shapes",
        "domain": "Geometry – properties of shapes",
        "standard_code": "Year 2: Geometry – properties of shapes",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Identify and describe the properties of 2-D shapes, including the number of sides and line symmetry in a vertical line; identify and describe the properties of 3-D shapes, including the number of edges, vertices and faces; identify 2-D shapes on the surface of 3-D shapes; compare and sort common 2-D and 3-D shapes and everyday objects.",
        "meta_desc": "Free Year 2 maths worksheets on 2-D and 3-D shapes: count sides and vertices, find a vertical line of symmetry, count the faces, edges and vertices of cubes, cuboids and pyramids, spot 2-D shapes on 3-D shapes and sort everyday objects. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "Count the sides to name a 2-D shape. Count faces, edges and vertices to describe a 3-D shape.",
        "key_sub": "A shape keeps its name when it is turned. A line of symmetry folds a shape into two halves that match exactly. Remember the faces you cannot see.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(four [a-z0-9 -]+ labelled A to D|the same shape with four|a row of four shapes)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
