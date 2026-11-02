# -*- coding: utf-8 -*-
"""
CA-BC Grade 3 Math: 3D objects (BC Mathematics Curriculum, Geometry and measurement: construction of 3D objects)
  python3 tools/gen_cabc_math_g3_3d_objects.py
HTML attributes use single quotes (no backslashes in the JSON). Canadian English, short sentences for 8–9-year-olds.

BC Grade 3 students construct 3D objects: they build them from nets and as skeletons (sticks and connectors,
such as toothpicks and modelling clay), name cubes, prisms, pyramids, cylinders, cones and spheres, and describe
their faces, edges and vertices.

Pictures (checked in code):
  objects     drawn from 3D vertices and faces, turned and seen from a little above; faces that face the viewer are
              shown, edges of hidden faces only are dashed; faces, edges and vertices are counted from the same data
              (V − E + F = 2), and the "only counted what you can see" wrong answers come from the same picture
  skeletons   one stick for each edge, one connector for each vertex (sticks at the back are lighter)
  cube nets   a cube is rolled over the squares (fold_cube): a net is good only when the 6 squares land on 6
              different faces; opposite faces come from the same fold
  other nets  rectangular prism, triangular prism and pyramids, with edges that match when folded
Wrong answers come from real student mistakes: counting only the faces you can see, edges and vertices swapped,
prism vs pyramid, a cylinder called a circle, "only the cross shape is a cube net", any 6 squares make a cube,
counting faces instead of edges for sticks.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL, BASE, SIDE, TOP3 = "#cfe6d6", "#f6dcb4", "#a9d3b6", "#e6f2e9"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
STICK = "#b5793a"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]

CUBE, RP, TP = "cube", "rectangular prism", "triangular prism"
SP, TBP = "square-based pyramid", "triangle-based pyramid"
CYL, CONE, SPH = "cylinder", "cone", "sphere"
COUNTS = {CUBE: (6, 12, 8), RP: (6, 12, 8), TP: (5, 9, 6), SP: (5, 8, 5), TBP: (4, 6, 4)}


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


def inside(pt, poly):
    x, y = pt
    n, c = len(poly), False
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            c = not c
    return c


class Canvas:
    """Collects shapes and text (screen coordinates, y down), tracks the bounding box, then writes a tight SVG."""

    def __init__(self):
        self.el, self.boxes, self.polys, self.segs = [], [], [], []
        self.x0 = self.y0 = 1e9
        self.x1 = self.y1 = -1e9

    def grow(self, x0, y0, x1, y1):
        self.x0, self.y0 = min(self.x0, x0), min(self.y0, y0)
        self.x1, self.y1 = max(self.x1, x1), max(self.y1, y1)

    def poly(self, pts, fill, sw=2.4, col=GREEN):
        self.el.append(("p", pts, fill, sw, col))
        self.polys.append(pts)
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

    def text(self, x, y, t, fs=16, col=INK):
        """(x, y) is the middle of the text."""
        w = tw(t, fs)
        box = (x - w / 2, y - fs * 0.5, x + w / 2, y + fs * 0.5)
        for b in self.boxes:
            assert box[2] < b[0] or b[2] < box[0] or box[3] < b[1] or b[3] < box[1], (t, box, b)
        self.boxes.append(box)
        self.el.append(("t", x, y + fs * 0.36, t, fs, col))
        self.grow(*box)

    def check(self):
        """Each label sits inside one face (or outside all faces), never across a face edge."""
        for (x0, y0, x1, y1) in self.boxes:
            pts = [(x0 + (x1 - x0) * i / 6, y0 + (y1 - y0) * j / 3) for i in range(7) for j in range(4)]
            hit = [sum(inside(p, poly) for p in pts) for poly in self.polys]
            hit = [h for h in hit if h]
            assert all(h == len(pts) for h in hit), ("label crosses a face edge", (x0, y0, x1, y1), hit)

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
            elif e[0] == "pl":
                _, pts, dashed, sw, col = e
                s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='%g' stroke-linejoin='round'%s/>"
                         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in pts), col, sw,
                            " stroke-dasharray='5 4'" if dashed else " stroke-linecap='round'"))
            else:
                _, x, y, t, fs, col = e
                s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                         % (x - ox, y - oy, fs, col, t))
        return "".join(s)

    def size(self):
        return self.x1 - self.x0, self.y1 - self.y0

    def svg(self, label, pad=5):
        self.check()
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
        cv.check()
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


def grid_svg(cvs, label, cw=118, ch=118):
    """2 x 2 grid of pictures labelled A-D."""
    W, H = 2 * cw, 2 * ch
    s = ["<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (cw, cw, H - 4, GRAY),
         "<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (ch, W - 4, ch, GRAY)]
    for k, cv in enumerate(cvs):
        cv.check()
        x0, y0 = (k % 2) * cw, (k // 2) * ch
        aw, ah = cw - 26, ch - 10
        w, h = cv.size()
        assert w <= aw and h <= ah, ("too big for the grid", w, h, aw, ah)
        ox = cv.x0 - (x0 + 21 + (aw - w) / 2)
        oy = cv.y0 - (y0 + 5 + (ah - h) / 2)
        s.append(cv.body(ox, oy))
        s.append("<text x='%d' y='%d' font-size='18' font-weight='700' fill='%s'>%s</text>" % (x0 + 5, y0 + 22, INK, "ABCD"[k]))
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ 3D objects with flat faces
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
        """Turn the solid by yaw about the up axis, then tip it towards the viewer by pitch (viewer at -z)."""
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
        """Skeleton: every edge is a stick, every vertex a connector. Sticks at the back are lighter."""
        pts, vis, _ = self.view(yaw, pitch)
        P = lambda p: (p[0] * k, -p[1] * k)
        cv = Canvas()
        back = [e for e, fs in self.edges.items() if not any(vis[f] for f in fs)]
        front = [e for e in self.edges if e not in back]
        for a, b in back:
            cv.line(P(pts[a]), P(pts[b]), sw=3.5, col="#dcb98f")
        for a, b in front:
            cv.line(P(pts[a]), P(pts[b]), sw=4, col=STICK)
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


def tri_pyramid(s=1.5, h=1.3):
    """Triangle-based pyramid: a triangle base and 3 triangle faces that meet at a point."""
    d = s * math.sqrt(3) / 2
    v = [(0, 0, 0), (s, 0, 0), (s / 2, 0, d), (s / 2, h, d / 3)]
    f = [[0, 1, 2], [0, 1, 3], [1, 2, 3], [2, 0, 3]]
    return Solid(v, f)


VIEWS = {
    "cube": (lambda: box(1.1, 1.1, 1.1), 30, 22),
    "cube_turned": (lambda: box(1.1, 1.1, 1.1), 50, 30),
    "rp_flat": (lambda: box(1.9, 0.8, 1.0), 25, 22),
    "rp_tall": (lambda: box(0.8, 1.8, 0.7), 35, 18),
    "rp_turned": (lambda: box(1.6, 1.0, 0.8), -35, 24),
    "rp_sq": (lambda: box(1.8, 0.8, 0.8), 25, 22),
    "tp_lying": (lambda: prism_lying(), 30, 20),
    "tp_end": (lambda: prism_lying(), 120, 25),
    "tp_standing": (lambda: prism_standing(), 20, 35),
    "sp": (lambda: pyramid(), 25, 18),
    "sp_turned": (lambda: pyramid(1.2, 1.5), -30, 25),
    "tbp": (lambda: tri_pyramid(), -160, 20),
}
VIEW_KIND = {"cube": CUBE, "cube_turned": CUBE, "rp_flat": RP, "rp_tall": RP, "rp_turned": RP, "rp_sq": RP,
             "tp_lying": TP, "tp_end": TP, "tp_standing": TP, "sp": SP, "sp_turned": SP, "tbp": TBP}
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


# ------------------------------------------------------------ curved 3D objects
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
    """how: 'up' (point at the top), 'down' (point at the bottom), 'side' (lying down)."""
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


# ------------------------------------------------------------ cube nets (a cube is rolled over the squares)
def rot_y(s):
    return ((0, 0, s), (0, 1, 0), (-s, 0, 0))


def rot_x(s):
    return ((1, 0, 0), (0, 0, -s), (0, s, 0))


def mat(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)) for i in range(3))


def fold_cube(cells):
    """Returns {cell: face} or None when the squares are not 6, or two squares land on the same face."""
    cells = list(cells)
    assert len(set(cells)) == len(cells)
    if len(cells) != 6:
        return None
    I = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    R = {cells[0]: I}
    todo = [cells[0]]
    while todo:
        c = todo.pop(0)
        for (dc, dr), M in [((1, 0), rot_y(1)), ((-1, 0), rot_y(-1)), ((0, 1), rot_x(-1)), ((0, -1), rot_x(1))]:
            n = (c[0] + dc, c[1] + dr)
            if n in cells and n not in R:
                R[n] = mat(M, R[c])
                todo.append(n)
    assert len(R) == 6, "squares are not connected"
    face = {c: tuple(m[2][i] * -1 for i in range(3)) for c, m in R.items()}
    return face if len(set(face.values())) == 6 else None


def opposite(cells, a):
    face = fold_cube(cells)
    return [c for c in cells if face[c] == tuple(-v for v in face[a])][0]


CROSS = [(0, 1), (1, 1), (2, 1), (3, 1), (1, 0), (1, 2)]
GOOD = {
    "cross": CROSS,
    "t": [(0, 1), (1, 1), (2, 1), (3, 1), (0, 0), (0, 2)],
    "z": [(0, 1), (1, 1), (2, 1), (3, 1), (0, 0), (3, 2)],
    "s": [(0, 1), (1, 1), (2, 1), (3, 1), (2, 0), (1, 2)],
    "stairs": [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2)],
    "three": [(0, 0), (1, 0), (2, 0), (2, 1), (3, 1), (4, 1)],
    "two31": [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1), (1, 2)],
}
WHY_SAME = "two squares are on the same side of the row of 4, so they fold onto the same face"
BAD = {
    "same1": ([(0, 1), (1, 1), (2, 1), (3, 1), (0, 0), (3, 0)], WHY_SAME),
    "same2": ([(0, 1), (1, 1), (2, 1), (3, 1), (1, 0), (2, 0)], WHY_SAME),
    "same3": ([(0, 1), (1, 1), (2, 1), (3, 1), (0, 2), (2, 2)], WHY_SAME),
    "row5": ([(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (1, 0)], "5 squares in a row wrap all the way around, so two squares overlap"),
    "block": ([(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1)], "it has a 2 by 2 block of squares, so two squares overlap"),
    "five": ([(0, 1), (1, 1), (2, 1), (3, 1), (1, 0)], "it has only 5 squares, so one face is missing"),
    "seven": ([(0, 1), (1, 1), (2, 1), (3, 1), (1, 0), (1, 2), (2, 0)], "it has 7 squares, but a cube has only 6 faces"),
}
for _n in GOOD.values():
    assert fold_cube(_n), _n
for _n, _w in BAD.values():
    assert fold_cube(_n) is None, _n


def cube_net_cv(cells, k=30, letters=None, fs=18):
    cv = Canvas()
    c0 = min(c for c, r in cells)
    r0 = min(r for c, r in cells)
    for c, r in cells:
        x, y = (c - c0) * k, (r - r0) * k
        cv.poly([(x, y), (x + k, y), (x + k, y + k), (x, y + k)], FILL, 2)
    if letters:
        for (c, r), t in letters.items():
            cv.text((c - c0 + 0.5) * k, (r - r0 + 0.5) * k, t, fs, col=GREEN)
    return cv


# ------------------------------------------------------------ other nets
def box_net_cv(L, W, H, k, top_on=0, bot_on=0):
    """Strip of 4 faces (L, W, L, W wide, H tall) with an L × W face above face top_on and below face bot_on."""
    xs = [0, L, L + W, 2 * L + W, 2 * L + 2 * W]
    cv = Canvas()
    for i in range(4):
        cv.poly([(xs[i] * k, 0), (xs[i + 1] * k, 0), (xs[i + 1] * k, H * k), (xs[i] * k, H * k)], FILL, 2)
    assert top_on in (0, 2) and bot_on in (0, 2)          # the lid sits on a face that is L wide
    cv.poly([(xs[top_on] * k, -W * k), ((xs[top_on] + L) * k, -W * k), ((xs[top_on] + L) * k, 0), (xs[top_on] * k, 0)], FILL, 2)
    cv.poly([(xs[bot_on] * k, H * k), ((xs[bot_on] + L) * k, H * k), ((xs[bot_on] + L) * k, (H + W) * k), (xs[bot_on] * k, (H + W) * k)], FILL, 2)
    return cv


def tri_prism_net_cv(k, s=1.2, L=1.7):
    """3 rectangles (s wide, L tall) side by side, an equilateral triangle (side s) on top of the middle one and
    under the middle one: every triangle side matches a rectangle end."""
    cv = Canvas()
    for i in range(3):
        cv.poly([(i * s * k, 0), ((i + 1) * s * k, 0), ((i + 1) * s * k, L * k), (i * s * k, L * k)], FILL, 2)
    t = s * math.sqrt(3) / 2
    cv.poly([(s * k, 0), (2 * s * k, 0), (1.5 * s * k, -t * k)], BASE, 2)
    cv.poly([(s * k, L * k), (2 * s * k, L * k), (1.5 * s * k, (L + t) * k)], BASE, 2)
    return cv


def pyramid_net_cv(k, s=1.2, l=1.1):
    """Square base with a triangle (base s, height l) on each side."""
    S, Lk = s * k, l * k
    cv = Canvas()
    cv.poly([(0, 0), (S, 0), (S, S), (0, S)], BASE, 2)
    for t in [[(0, 0), (S, 0), (S / 2, -Lk)], [(S, 0), (S, S), (S + Lk, S / 2)],
              [(0, S), (S, S), (S / 2, S + Lk)], [(0, 0), (0, S), (-Lk, S / 2)]]:
        cv.poly(t, FILL, 2)
    return cv


def tetra_net_cv(k):
    """4 equal triangles: a big triangle cut into 4."""
    H = math.sqrt(3)
    P = lambda x, y: (x * k, y * k)
    p0, p1, p2 = P(0, H), P(2, H), P(1, 0)
    m01, m12, m02 = P(1, H), P(1.5, H / 2), P(0.5, H / 2)
    cv = Canvas()
    for t in [[p0, m01, m02], [m01, p1, m12], [m02, m12, p2]]:
        cv.poly(t, FILL, 2)
    cv.poly([m02, m01, m12], BASE, 2)
    return cv


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


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


# ------------------------------------------------------------ set 1: name 3D objects
WRONG1 = {CUBE: [RP, "square", SP], RP: [CUBE, "rectangle", TP], TP: [SP, RP, "triangle"],
          SP: [TP, CONE, "square"], TBP: [TP, SP, "triangle"], CYL: ["circle", CONE, TP], CONE: [CYL, "triangle", SP],
          SPH: ["circle", CYL, CONE]}
E1 = {
    CUBE: "It has 6 faces and they are all squares of the same size, so it is a cube.",
    RP: "It has 6 rectangle faces and they are not all squares, so it is a rectangular prism.",
    TP: "It has 2 triangle faces at the ends, joined by 3 rectangles, so it is a triangular prism. It does not come to a point, so it is not a pyramid.",
    SP: "It has a square face at the bottom and 4 triangle faces that meet at a point, so it is a square-based pyramid.",
    TBP: "It has a triangle at the bottom and 3 triangle faces that meet at a point, so it is a triangle-based pyramid.",
    CYL: "It has 2 flat circle faces at the ends and a curved surface, so it is a cylinder. A circle is only a flat 2D shape.",
    CONE: "It has 1 flat circle face and a curved surface that comes to a point, so it is a cone.",
    SPH: "It is round all over, like a ball, so it is a sphere. A circle is a flat 2D shape.",
}
TURN1 = {"cube_turned": " It is turned, but it is still a cube.",
         "rp_tall": " It is standing on its end, but it is still a rectangular prism.",
         "rp_turned": " It is turned, but it is still a rectangular prism.",
         "tp_end": " It is turned so you see a triangle end at the front.",
         "tp_standing": " It is standing on a triangle face, but it is still a triangular prism.",
         "sp_turned": " It is turned, but it is still a square-based pyramid.",
         "cyl_lying": " It is lying on its side, but it is still a cylinder.",
         "cone_down": " It is upside down, but it is still a cone.",
         "cone_side": " It is lying on its side, but it is still a cone."}


def set_name(rnd, pos):
    its = []
    asks = ["What is the name of this object?", "Name this 3D object.", "What is this object called?"]
    keys = ["cube", "cube_turned", "rp_flat", "rp_tall", "rp_turned", "tp_lying", "tp_standing", "tp_end", "sp", "sp_turned",
            "tbp", "cyl", "cyl_lying", "cone", "cone_down", "sphere"]
    for i, k in enumerate(keys):
        kind = KIND[k]
        its.append(mcq(fig(pic3d(k).svg("a 3D object")) + asks[i % 3], kind, WRONG1[kind], E1[kind] + TURN1.get(k, "")))
    q = (fig(row_svg([pic3d("tp_lying", 0.8), pic3d("tp_standing", 0.8)], ["", ""], "the same 3D object in two positions", gap=40))
         + "Both pictures show the same object in different positions. What is it?")
    its.append(mcq(q, TP, WRONG1[TP], E1[TP] + " Turning an object does not change its name."))
    for kind, right, others, why in [
            (CONE, "cone_side", ["cyl_lying", "sp", "tp_end"], "it has 1 circle face and comes to a point. It is lying on its side"),
            (SP, "sp_turned", ["tp_lying", "tbp", "rp_flat"],
             "it has a square base and 4 triangles that meet at a point. A triangular prism has no point, and a triangle-based pyramid has a triangle base"),
            (CYL, "cyl_lying", ["cone", "sphere", "rp_flat"], "it has 2 circle faces and a curved surface. It is lying on its side"),
    ]:
        p = pos.next()
        cells = [pic3d(k, 0.62) for k in others]
        cells.insert(p, pic3d(right, 0.62))
        its.append(mcq_fixed(fig(grid_svg(cells, "four 3D objects labelled A to D")) + "Which picture shows %s %s?" % (art(kind), kind),
                             list("ABCD"), "ABCD"[p], "%s is %s %s: %s." % ("ABCD"[p], art(kind), kind, why)))
    assert len(its) == 20, len(its)
    return {"title": "Name 3D objects", "items": its}


# ------------------------------------------------------------ set 2: faces, edges and vertices
def set_fev(rnd, P):
    its = []
    its.append(mcq("A flat surface of a 3D object is called a …", "face", ["edge", "vertex", "point"],
                   "A face is a flat surface. An edge is where two faces meet. A vertex is a corner."))
    its.append(mcq("The line where two faces of an object meet is called an …", "edge", ["vertex", "face", "angle"],
                   "Where two faces meet there is an edge."))
    its.append(mcq("A corner of an object, where edges meet, is called a …", "vertex", ["edge", "face", "side"],
                   "A corner is a vertex. More than one vertex are called vertices."))
    hidden = {"faces": "Some faces are at the back or underneath. You cannot see them, but you must count them too.",
              "edges": "The dashed lines show edges at the back. Count them too.",
              "vertices": "Some vertices are at the back, where the dashed lines meet. Count them too."}
    for view, what in [("cube", "faces"), ("cube", "edges"), ("cube_turned", "vertices"), ("rp_flat", "faces"),
                       ("rp_turned", "edges"), ("tp_lying", "faces"), ("tp_lying", "edges"), ("tp_standing", "vertices"),
                       ("sp", "faces"), ("sp", "edges"), ("sp_turned", "vertices"), ("tbp", "edges")]:
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
    its.append(mcq("Which 2D shapes are the faces of a triangular prism?", "2 triangles and 3 rectangles",
                   ["3 triangles and 2 rectangles", "2 triangles and 2 rectangles", "1 triangle and 4 rectangles"],
                   "A triangular prism has a triangle at each end (2 triangles) and 3 rectangles joining them: 5 faces."))
    its.append(mcq("Which 2D shapes are the faces of a square-based pyramid?", "1 square and 4 triangles",
                   ["4 squares and 1 triangle", "1 square and 3 triangles", "2 squares and 4 triangles"],
                   "A square-based pyramid has 1 square at the bottom and 4 triangles that meet at the top: 5 faces."))
    its.append(mcq("Which object has 5 vertices?", SP, [TP, CUBE, CONE],
                   "A square-based pyramid has 4 vertices around the square and 1 at the top: 4 + 1 = 5. A triangular prism has 6."))
    n, he, his = P.next()
    its.append(mcq("%s says a cube has 8 edges. %s is wrong. What did %s count?" % (n, he.capitalize(), he), "the vertices",
                   ["the faces", "the edges at the front", "the hidden faces"],
                   "A cube has 8 vertices (corners) and 12 edges. %s counted the vertices." % n))
    n, he, his = P.next()
    its.append(mcq("%s counts the faces of a cube in a picture and gets 3. What did %s forget?" % (n, he),
                   "the 3 faces at the back", ["the 8 vertices", "the 12 edges", "the faces on the top"],
                   "A picture shows only 3 faces of a cube. There are 3 more at the back and underneath: 3 + 3 = 6 faces."))
    assert len(its) == 20, len(its)
    return {"title": "Faces, edges and vertices", "items": its}


# ------------------------------------------------------------ set 3: build with nets
def letters_for(cells, names="ABCDEF"):
    order = sorted(cells, key=lambda c: (c[1], c[0]))
    return {c: names[i] for i, c in enumerate(order)}


def set_nets(rnd, pos):
    its = []
    its.append(mcq("A net is a flat shape that you can fold to make a 3D object. How many squares are in a net of a cube?",
                   6, [4, 8, 12],
                   "A cube has 6 faces, so its net has 6 squares. 8 is the number of vertices and 12 is the number of edges."))
    # which net makes a cube? (1 good, 3 bad)
    for good, bads in [("cross", ["five", "same1", "block"]), ("stairs", ["row5", "seven", "same2"]),
                       ("t", ["block", "same3", "five"]), ("three", ["same1", "row5", "seven"])]:
        p = pos.next()
        cells = [cube_net_cv(BAD[b][0], 21) for b in bads]
        cells.insert(p, cube_net_cv(GOOD[good], 21))
        why = "; ".join("%s: %s" % ("ABCD"[i], BAD[b][1]) for i, b in zip([i for i in range(4) if i != p], bads))
        its.append(mcq_fixed(fig(grid_svg(cells, "four nets labelled A to D", 150, 96)) + "Which net folds into a cube?",
                             list("ABCD"), "ABCD"[p],
                             "%s has 6 squares and each one folds onto a different face. %s." % ("ABCD"[p], why[0].upper() + why[1:])))
    # which net will NOT make a cube? (3 good, 1 bad)
    for goods, bad in [(["cross", "z", "s"], "same3"), (["two31", "stairs", "t"], "block")]:
        p = pos.next()
        cells = [cube_net_cv(GOOD[g], 21) for g in goods]
        cells.insert(p, cube_net_cv(BAD[bad][0], 21))
        its.append(mcq_fixed(fig(grid_svg(cells, "four nets labelled A to D", 150, 96)) + "Which net will NOT fold into a cube?",
                             list("ABCD"), "ABCD"[p],
                             "%s will not work: %s. The other three nets each make a cube." % ("ABCD"[p], BAD[bad][1])))
    # one net: will it fold into a cube?
    YES = "Yes: each square folds onto a different face."
    its.append(mcq(fig(cube_net_cv(GOOD["stairs"]).svg("a net of 6 squares")) + "Will this net fold into a cube?", YES,
                   ["No: only a cross shape makes a cube.", "No: the squares are not in a straight line.", "No: a cube net needs 8 squares."],
                   "It has 6 squares and none of them overlap when you fold it. There are 11 different nets of a cube, not only the cross."))
    its.append(mcq(fig(cube_net_cv(BAD["same1"][0]).svg("a net of 6 squares")) + "Will this net fold into a cube?",
                   "No: two squares fold onto the same face.",
                   ["Yes: it has 6 squares.", "Yes: it has a row of 4 squares.", "No: a cube net needs 8 squares."],
                   "The 2 squares on top of the row of 4 both fold up onto the top face. The bottom face is left open. Having 6 squares is not enough."))
    its.append(mcq(fig(cube_net_cv(BAD["five"][0]).svg("a net of 5 squares")) + "What happens when you fold this net?",
                   "It makes a box with one face missing.",
                   ["It makes a cube.", "It makes a square-based pyramid.", "It makes a rectangular prism."],
                   "The net has only 5 squares. A cube has 6 faces, so one face is left open, like a box with no lid."))
    # nets of other objects
    for cv, label, kind, wrong, e in [
            (box_net_cv(1.6, 1.0, 1.0, 26), "a net of 2 squares and 4 rectangles", RP, [CUBE, TP, "rectangle"],
             "It has 6 faces: 4 rectangles and 2 squares. The faces are not all squares, so it folds into a rectangular prism, not a cube."),
            (tri_prism_net_cv(30), "a net of 2 triangles and 3 rectangles", TP, [SP, TBP, RP],
             "It has 2 triangles and 3 rectangles. The triangles become the ends, so it is a triangular prism. A pyramid net has triangles that meet at a point."),
            (pyramid_net_cv(30), "a net of 1 square and 4 triangles", SP, [TP, CUBE, TBP],
             "It has 1 square and 4 triangles. The square is the base and the 4 triangles fold up to meet at a point: a square-based pyramid."),
            (tetra_net_cv(36), "a net of 4 triangles", TBP, [TP, SP, "triangle"],
             "It has 4 triangles. One is the base and the other 3 fold up to meet at a point: a triangle-based pyramid."),
    ]:
        its.append(mcq(fig(cv.svg(label)) + "Which 3D object does this net make?", kind, wrong, e))
    NAME4 = {"cube": "a cube", RP: "a rectangular prism", TP: "a triangular prism", SP: "a square-based pyramid"}
    nets4 = [("cube", cube_net_cv(CROSS, 20)), (RP, box_net_cv(1.5, 1.0, 1.0, 20)),
             (TP, tri_prism_net_cv(21)), (SP, pyramid_net_cv(23))]
    for kind, why in [(TP, "it has 2 triangles and 3 rectangles"), (SP, "it has 1 square and 4 triangles that meet at a point")]:
        p = pos.next()
        others = [k for k, cv in nets4 if k != kind]
        rnd.shuffle(others)
        keys = others[:]
        keys.insert(p, kind)
        cells = [dict(nets4)[k] for k in keys]
        rest = ", ".join("%s makes %s" % ("ABCD"[i], NAME4[k]) for i, k in enumerate(keys) if k != kind)
        its.append(mcq_fixed(fig(grid_svg(cells, "four nets labelled A to D", 150, 96)) + "Which net folds into %s %s?" % (art(kind), kind),
                             list("ABCD"), "ABCD"[p], "%s: %s. The others: %s." % ("ABCD"[p], why, rest)))
    its.append(mcq("How many triangles are in the net of a square-based pyramid?", 4, [5, 1, 3],
                   "A square-based pyramid has 1 square and 4 triangles. The net has the same faces: 4 triangles."))
    its.append(mcq("Which shapes do you need for the net of a triangular prism?", "2 triangles and 3 rectangles",
                   ["3 triangles and 2 rectangles", "1 square and 4 triangles", "4 triangles"],
                   "A net has the same faces as the object. A triangular prism has 2 triangle ends and 3 rectangles."))
    # opposite faces
    for cells, start in [(CROSS, (1, 0)), (GOOD["z"], (0, 1))]:
        let = letters_for(cells)
        opp = opposite(cells, start)
        assert (opp[0] == start[0] and abs(opp[1] - start[1]) == 2) or (opp[1] == start[1] and abs(opp[0] - start[0]) == 2)
        face = fold_cube(cells)
        wrong = [let[c] for c in cells if c not in (start, opp)]
        # next-door squares first: the most common wrong answer
        wrong.sort(key=lambda t: [c for c in cells if let[c] == t][0] not in
                   [(start[0] + 1, start[1]), (start[0] - 1, start[1]), (start[0], start[1] + 1), (start[0], start[1] - 1)])
        assert all(face[c] != tuple(-v for v in face[start]) for c in cells if let[c] in wrong)
        q = (fig(cube_net_cv(cells, 34, let).svg("a net of a cube with faces A to F"))
             + "This net is folded into a cube. Which face is opposite face %s?" % let[start])
        its.append(mcq(q, let[opp], wrong,
                       "%s and %s are in the same line with one square between them, so they fold onto opposite faces. "
                       "Squares that touch in the net are next to each other on the cube." % (let[start], let[opp])))
    assert len(its) == 20, len(its)
    return {"title": "Build with nets: which net makes a cube?", "items": its}


# ------------------------------------------------------------ set 4: skeletons
def set_skeletons(rnd, P):
    its = []
    its.append(mcq("You build a skeleton of a 3D object with sticks and connectors. Each stick is …", "an edge",
                   ["a vertex", "a face", "a curved surface"],
                   "A stick is a straight line between two corners, so each stick is an edge."))
    its.append(mcq("In a skeleton, each connector (like a ball of modelling clay) is …", "a vertex",
                   ["an edge", "a face", "a base"],
                   "The connectors join the sticks at the corners, so each connector is a vertex."))
    for view, what in [("cube", "sticks"), ("cube", "connectors"), ("rp_flat", "sticks"), ("tp_lying", "sticks"),
                       ("tp_lying", "connectors"), ("sp", "sticks"), ("tbp", "sticks"), ("tbp", "connectors")]:
        kind = VIEW_KIND[view]
        F, E, V = COUNTS[kind]
        ans = E if what == "sticks" else V
        other = V if what == "sticks" else E
        front = seen(view)["edges"] if what == "sticks" else seen(view)["vertices"]
        wrong = [other, F, front, ans + 1, ans - 1]
        q = (fig(model_cv(view).svg("a skeleton made from sticks and connectors"))
             + "This is a skeleton of %s %s. How many %s does it have?" % (art(kind), kind, what))
        if what == "sticks":
            e = ("%s %s has %d edges, so the skeleton has %d sticks. Count the lighter sticks at the back too." % (art(kind).capitalize(), kind, E, E))
        else:
            e = ("%s %s has %d vertices, so the skeleton has %d connectors. %d is the number of sticks." % (art(kind).capitalize(), kind, V, V, E))
        its.append(mcq(q, ans, wrong, e))
    its.append(mcq(fig(model_cv("tp_lying").svg("a skeleton made from sticks and connectors")) + "Which object is this skeleton?",
                   TP, [SP, RP, TBP],
                   "It has 2 triangles at the ends joined by 3 sticks: 9 sticks and 6 connectors. It does not come to a point, so it is a prism."))
    its.append(mcq(fig(model_cv("sp").svg("a skeleton made from sticks and connectors")) + "Which object is this skeleton?",
                   SP, [TP, CUBE, TBP],
                   "It has a square at the bottom and 4 sticks that meet at a point on top: 8 sticks and 5 connectors. It is a square-based pyramid."))
    its.append(mcq("What do you need to build a skeleton of a cube?", "12 sticks and 8 connectors",
                   ["8 sticks and 12 connectors", "6 sticks and 8 connectors", "12 sticks and 6 connectors"],
                   "A cube has 12 edges (sticks) and 8 vertices (connectors). 6 is the number of faces."))
    its.append(mcq("What do you need to build a skeleton of a square-based pyramid?", "8 sticks and 5 connectors",
                   ["5 sticks and 8 connectors", "8 sticks and 4 connectors", "4 sticks and 5 connectors"],
                   "Edges: 4 around the square and 4 up to the top = 8 sticks. Vertices: 4 around the square and 1 at the top = 5 connectors."))
    n, he, his = P.next()
    its.append(mcq("%s uses 9 sticks and 6 connectors to build one skeleton. Which object is it?" % n, TP, [SP, CUBE, TBP],
                   "9 edges and 6 vertices: that is a triangular prism. A square-based pyramid has 8 edges and 5 vertices."))
    n, he, his = P.next()
    its.append(mcq("%s uses 6 sticks and 4 connectors to build one skeleton. Which object is it?" % n, TBP, [SP, TP, "triangle"],
                   "6 edges and 4 vertices: that is a triangle-based pyramid. A square-based pyramid needs 8 sticks and 5 connectors."))
    n, he, his = P.next()
    its.append(mcq("%s builds a skeleton of a cube. What must be true about the sticks?" % n, "They are all the same length.",
                   ["They are 2 different lengths.", "There are 6 of them.", "There are 8 of them."],
                   "All the faces of a cube are the same square, so all 12 edges are the same length."))
    n, he, his = P.next()
    its.append(mcq("%s has 8 short sticks and 4 long sticks. %s uses all 12 to build a skeleton. Which object is it?"
                   % (n, he.capitalize()), RP, [CUBE, TP, SP],
                   "12 sticks make a box shape with 8 corners. The sticks are not all the same length, so it is a rectangular prism, not a cube."))
    its.append(mcq("Which object can you NOT build as a skeleton with straight sticks?", SPH, [CUBE, TP, SP],
                   "A sphere is curved all over. It has no straight edges and no vertices, so sticks cannot make it."))
    n, he, his = P.next()
    its.append(mcq("%s builds a triangle-based pyramid and a cube. How many sticks does %s use altogether?" % (n, he), 18, [12, 10, 14],
                   "A triangle-based pyramid has 6 edges and a cube has 12. 6 + 12 = 18 sticks. 10 adds the faces (4 + 6) instead."))
    assert len(its) == 20, len(its)
    return {"title": "Skeletons with sticks and connectors: how many sticks?", "items": its}


# ------------------------------------------------------------ set 5: real objects and word problems
def set_real(rnd, P):
    its = []
    for obj, kind, wrong, e in [
            ("a can of soup", CYL, ["circle", CONE, RP], "A can has 2 circle ends and a curved side, so it is a cylinder."),
            ("an ice cream cone", CONE, [CYL, "triangle", SP], "It has a circle at the top, a curved side and a point at the bottom, so it is a cone."),
            ("a box of crackers", RP, [CUBE, "rectangle", TP], "It has 6 rectangle faces that are not all squares, so it is a rectangular prism."),
            ("a soccer ball", SPH, ["circle", CYL, CONE], "A soccer ball is round all over, so it is a sphere. A circle is flat."),
            ("a hockey puck", CYL, ["circle", SPH, CONE], "A puck has 2 flat circle faces and a curved side, so it is a short cylinder."),
            ("a number cube (a die)", CUBE, [RP, "square", SP], "It has 6 square faces that are all the same size, so it is a cube."),
    ]:
        its.append(mcq("%s is shaped like which 3D object?" % (obj[0].upper() + obj[1:]), kind, wrong, e))
    its.append(mcq("A tent at a campsite in the Okanagan has a triangle at each end. Which 3D object is it shaped like?", TP, [SP, RP, CONE],
                   "2 triangle ends joined by rectangles make a triangular prism. It does not come to one point, so it is not a pyramid."))
    its.append(mcq("The attic of a cabin near Whistler has a triangle at each end, two sloping roof sides and a flat floor. "
                   "Which object is it shaped like?", TP, [SP, RP, TBP],
                   "2 triangles at the ends and 3 rectangles (2 roof sides and the floor) make a triangular prism. It has no point, so it is not a pyramid."))
    its.append(mcq("A tea bag is shaped like a pyramid with 4 triangle faces. Which 3D object is it?", TBP, [TP, SP, "triangle"],
                   "4 triangle faces: 1 triangle base and 3 triangles that meet at a point. That is a triangle-based pyramid."))
    n, he, his = P.next()
    its.append(mcq("A tissue box sits on %s’s desk. %s can see 3 of its faces. How many faces can %s NOT see?"
                   % (n, he.capitalize(), he), 3, [0, 6, 2],
                   "A box (rectangular prism) has 6 faces. 6 − 3 = 3 faces are at the back and underneath."))
    n, he, his = P.next()
    its.append(mcq("%s paints a box for a recycling project. %s paints every face except the bottom. How many faces does %s paint?"
                   % (n, he.capitalize(), he), 5, [3, 6, 4],
                   "A box has 6 faces. All but the bottom: 6 − 1 = 5 faces. 3 is only the faces you see from the front."))
    n, he, his = P.next()
    its.append(mcq("%s puts one number cube on top of another to make a tower on the table. "
                   "How many faces of the cubes touch the table or the other cube?" % n, 3, [2, 1, 4],
                   "The bottom cube touches the table with 1 face. The two cubes touch each other with 1 face each: 1 + 1 + 1 = 3."))
    n, he, his = P.next()
    its.append(mcq("%s glues a piece of ribbon along every edge of a cube-shaped gift box. How many pieces of ribbon does %s need?"
                   % (n, he), 12, [8, 6, 9],
                   "A cube has 12 edges, so %s needs 12 pieces. 8 is the number of vertices and 6 is the number of faces." % n))
    n, he, his = P.next()
    its.append(mcq("%s makes 2 cube boxes from paper nets. How many paper squares are there in the 2 nets?" % n, 12, [6, 16, 24],
                   "Each cube net has 6 squares. 6 + 6 = 12 squares. 16 counts the vertices (8 + 8) instead."))
    n, he, his = P.next()
    its.append(mcq("%s’s class builds 3 cube skeletons for a display in the hallway. How many sticks do they use?" % n, 36, [24, 18, 12],
                   "Each cube needs 12 sticks. 12 + 12 + 12 = 36 sticks. 24 uses the 8 vertices (8 × 3) instead."))
    n, he, his = P.next()
    its.append(mcq("There are 4 groups in %s’s class. Each group builds a square-based pyramid skeleton. How many connectors do they use?"
                   % n, 20, [32, 16, 24],
                   "A square-based pyramid has 5 vertices. 5 + 5 + 5 + 5 = 20 connectors. 32 uses the 8 edges (sticks) instead."))
    n, he, his = P.next()
    its.append(mcq("%s has 20 sticks. %s builds one cube skeleton. How many sticks are left?" % (n, he.capitalize()), 8, [12, 14, 32],
                   "A cube uses 12 sticks (12 edges). 20 − 12 = 8 sticks left. 14 comes from taking away 6 faces instead of 12 edges."))
    n, he, his = P.next()
    its.append(mcq("On a camping trip, %s’s family puts up a tent frame shaped like the skeleton of a triangular prism. How many poles does the frame have?"
                   % n, 9, [6, 5, 12],
                   "A triangular prism has 9 edges: 3 on each triangle end (6) and 3 joining the ends. So the frame has 9 poles."))
    its.append(mcq("Why do stores stack boxes shaped like rectangular prisms, not balls?", "Flat faces stack with no gaps.",
                   ["Boxes can roll.", "Boxes come to a point.", "Boxes have a curved surface."],
                   "Rectangular prisms have flat faces, so they sit on top of each other on a shelf. Spheres would roll off."))
    its.append(mcq("A can of juice stands on a shelf in the fridge. Which part of the can touches the shelf?", "a flat circle face",
                   ["the curved surface", "a vertex", "a square face"],
                   "A cylinder stands on one of its flat circle faces. On its curved surface it would roll."))
    assert len(its) == 20, len(its)
    return {"title": "3D objects in real life: word problems", "items": its}


# ------------------------------------------------------------ lesson
def body_html():
    flat = row_svg([solid_cv("cube", 40), solid_cv("rp_flat", 38), solid_cv("tp_lying", 40), solid_cv("sp", 40)],
                   ["cube", "rectangular prism", "triangular prism", "square-based pyramid"],
                   "a cube, a rectangular prism, a triangular prism and a square-based pyramid", gap=14, fs=14)
    curved = row_svg([cylinder_cv(0.8), cone_cv(0.8), sphere_cv(0.85)], ["cylinder", "cone", "sphere"],
                     "a cylinder, a cone and a sphere", gap=40, fs=14)
    nets = row_svg([cube_net_cv(CROSS, 24), cube_net_cv(GOOD["stairs"], 24), cube_net_cv(BAD["same1"][0], 24)],
                   ["makes a cube", "makes a cube", "does not"],
                   "two nets that fold into a cube and one that does not", gap=30, fs=14)
    other_nets = row_svg([box_net_cv(1.5, 1.0, 1.0, 22), tri_prism_net_cv(24), pyramid_net_cv(26)],
                         ["rectangular prism", "triangular prism", "square-based pyramid"],
                         "nets of a rectangular prism, a triangular prism and a square-based pyramid", gap=20, fs=14)
    model = row_svg([solid_cv("cube", 46), model_cv("cube", 46), model_cv("sp", 46)], ["cube", "cube skeleton", "pyramid skeleton"],
                    "a cube, a skeleton of a cube and a skeleton of a square-based pyramid", gap=30, fs=14)
    return (
        "<h2>What is a 3D object?</h2>"
        "<p>A 3D object is <b>solid</b>, like a box or a ball. A <b>face</b> is a flat surface. An <b>edge</b> is where two faces meet. "
        "A <b>vertex</b> is a corner. Two or more are called <b>vertices</b>. Dashed lines show edges at the back.</p>"
        "<figure class='sn-fig'>" + flat +
        "<figcaption>A prism has the same shape at both ends. A pyramid comes to a point.</figcaption></figure>"
        "<figure class='sn-fig'>" + curved +
        "<figcaption>A cylinder, a cone and a sphere have a curved surface.</figcaption></figure>" +
        table(["Object", "Faces", "Edges", "Vertices", "Real object"], [
            ["Cube", "6 squares", "12", "8", "a number cube"],
            ["Rectangular prism", "6 rectangles", "12", "8", "a cereal box"],
            ["Triangular prism", "2 triangles, 3 rectangles", "9", "6", "a tent"],
            ["Square-based pyramid", "1 square, 4 triangles", "8", "5", "a pyramid roof"],
            ["Triangle-based pyramid", "4 triangles", "6", "4", "a pyramid-shaped tea bag"]]) +
        ex("Example 1", "How many faces does a cube have?",
           "A picture shows 3 faces. There are 3 more at the back and underneath. 3 + 3 = 6.", "6 faces") +
        "<h2>Build with nets</h2>"
        "<p>A <b>net</b> is a flat shape that folds up into a 3D object. The net has the same faces as the object. "
        "A cube net has 6 squares, but not every group of 6 squares works. Each square must fold onto a different face.</p>"
        "<figure class='sn-fig'>" + nets +
        "<figcaption>In the last one, the 2 squares above the row both fold onto the top. The bottom stays open.</figcaption></figure>"
        "<figure class='sn-fig'>" + other_nets +
        "<figcaption>Count the shapes in a net: 2 triangles and 3 rectangles make a triangular prism.</figcaption></figure>" +
        ex("Example 2", "A net has 1 square and 4 triangles. What does it make?",
           "The square is the base. The 4 triangles fold up and meet at a point.", "a square-based pyramid") +
        "<h2>Build skeletons</h2>"
        "<p>A <b>skeleton</b> shows only the edges and vertices. Use sticks (like toothpicks or straws) and connectors "
        "(like balls of modelling clay). Each <b>stick</b> is an <b>edge</b>. Each <b>connector</b> is a <b>vertex</b>.</p>"
        "<figure class='sn-fig'>" + model +
        "<figcaption>A cube skeleton needs 12 sticks and 8 connectors. A square-based pyramid needs 8 sticks and 5 connectors.</figcaption></figure>" +
        ex("Example 3", "How many sticks and connectors do you need for a triangular prism?",
           "Edges: 3 on each triangle end and 3 joining them = 9. Vertices: 3 on each end = 6.",
           "9 sticks and 6 connectors") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting only the faces you can see", "Count the faces at the back and underneath too"],
            ["Mixing up a prism and a pyramid", "A pyramid comes to a point. A prism has the same shape at both ends"],
            ["Thinking any 6 squares make a cube", "Check that no two squares fold onto the same face"],
            ["Thinking only the cross is a cube net", "There are 11 different cube nets"],
            ["Using the number of faces for sticks", "Sticks are edges; connectors are vertices"],
        ])
    )


FAQ = [
    {"q": "What do Grade 3 students learn about 3D objects in the BC curriculum?",
     "a": "The Grade 3 content standard is construction of 3D objects. Students build objects from nets and as skeletons, and describe their faces, edges and vertices."},
    {"q": "How many nets of a cube are there?",
     "a": "There are 11 different nets of a cube. Each has 6 squares, and no two squares fold onto the same face."},
    {"q": "What is the difference between a prism and a pyramid?",
     "a": "A prism has the same shape at both ends, joined by rectangles, so it has no point. A pyramid has one base and triangle faces that meet at a point."},
    {"q": "How can I help my child build 3D objects at home?",
     "a": "Cut open an empty cereal box to see its net, then fold it back up. Build skeletons with toothpicks and balls of modelling clay, and count the sticks (edges) and balls (vertices)."},
]


def gen():
    rnd = random.Random(53809)
    P = People(rnd)
    sets = [set_name(rnd, Pos(rnd)), set_fev(rnd, P), set_nets(rnd, Pos(rnd)), set_skeletons(rnd, P), set_real(rnd, P)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-3", "slug": "3d-objects", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "3D Objects: Nets, Skeletons, Faces, Edges and Vertices",
        "seo_title": "Grade 3 Math 3D Objects Worksheets: Nets and Skeletons (BC Curriculum, Free, Answer Key)",
        "short_title": "3D objects",
        "domain": "Geometry and measurement",
        "standard_code": "Grade 3: Geometry and measurement",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/3/core",
        "standard_text": "Construction of 3D objects",
        "meta_desc": "Free Grade 3 math worksheets on 3D objects for the BC curriculum: name cubes, prisms, pyramids, cylinders, cones and spheres, count faces, edges and vertices, find the nets that fold into a cube, count the sticks and connectors in skeletons, and solve real-life word problems. 100 questions with an answer key.",
        "key_big": "A net folds into a 3D object. A skeleton shows its edges (sticks) and vertices (connectors).",
        "key_sub": "A cube has 6 faces, 12 edges and 8 vertices. Count the faces you cannot see too. A cube net has 6 squares that fold onto 6 different faces. A pyramid comes to a point; a prism does not.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(four 3D objects labelled A to D|four nets labelled A to D|the same 3D object in two positions)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
