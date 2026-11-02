# -*- coding: utf-8 -*-
"""
CA-BC Grade 2 Math: 2D shapes and 3D objects (BC Mathematics Curriculum, Geometry and measurement)
  python3 tools/gen_cabc_math_g2_shapes.py
HTML attributes use single quotes (no backslashes in the JSON). Canadian English, short sentences for 7–8-year-olds.

BC Grade 2 Content: multiple attributes of 2D shapes and 3D objects. Students count the sides and vertices of
2D shapes, sort shapes by two attributes, count the faces, edges and vertices of 3D objects, name the 2D shapes
of their faces, and match 3D objects to real things.

Pictures (checked in code):
  2D shapes   drawn from their corner points; sides and vertices counted from the points, square corners and equal
              sides measured from the points, every corner is a real turn, no sides cross
  3D objects  drawn from 3D vertices and faces (V − E + F = 2); hidden edges are dashed; "only counted what you can
              see" answers come from the picture
Wrong answers come from real student mistakes: counting the first vertex twice, missing a vertex, giving a cylinder
vertices, counting only the faces you can see, edges and vertices swapped, 2D names for 3D objects, a cone said to
have a triangle face, a turned square called a different shape.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL, BASE, SIDE, TOP3 = "#cfe6d6", "#f6dcb4", "#a9d3b6", "#e6f2e9"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
THIN = "#b8b8b8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]

CUBE, RP, TP = "cube", "rectangular prism", "triangular prism"
SP, TBP = "square-based pyramid", "triangle-based pyramid"
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
    """Positions for picture answers (A-D), spread over the unit."""

    def __init__(self, rnd):
        self.rnd, self.q = rnd, []

    def next(self):
        if not self.q:
            self.q = [0, 1, 2, 3]
            self.rnd.shuffle(self.q)
        return self.q.pop()


def art(n):
    return "an" if n[0] in "aeiou" else "a"


# ------------------------------------------------------------ drawing
def tw(t, fs):
    """Approximate width of bold Arial text in px."""
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

    def line(self, a, b, dashed=False, sw=2.4, col=GREEN, dash="5 4"):
        self.el.append(("l", a, b, dashed, sw, col, dash))
        self.grow(min(a[0], b[0]) - sw, min(a[1], b[1]) - sw, max(a[0], b[0]) + sw, max(a[1], b[1]) + sw)

    def pline(self, pts, dashed=False, sw=2.4, col=GREEN):
        self.el.append(("pl", pts, dashed, sw, col))
        for x, y in pts:
            self.grow(x - sw, y - sw, x + sw, y + sw)

    def body(self, ox, oy):
        s = []
        for e in self.el:
            if e[0] == "p":
                st = " stroke='%s' stroke-width='%g' stroke-linejoin='round'" % (e[4], e[3]) if e[3] else ""
                s.append("<polygon points='%s' fill='%s'%s/>"
                         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in e[1]), e[2], st))
            elif e[0] == "c":
                _, c, r, fill, sw, col = e
                st = " stroke='%s' stroke-width='%g'" % (col, sw) if sw else ""
                s.append("<circle cx='%.1f' cy='%.1f' r='%g' fill='%s'%s/>" % (c[0] - ox, c[1] - oy, r, fill, st))
            elif e[0] == "l":
                _, a, b, dashed, sw, col, dash = e
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g'%s/>"
                         % (a[0] - ox, a[1] - oy, b[0] - ox, b[1] - oy, col, sw,
                            " stroke-dasharray='%s'" % dash if dashed else " stroke-linecap='round'"))
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


def row_svg(cvs, caps, label, gap=24, fs=14, col=INK):
    """Pictures side by side (lined up at the bottom) with a caption under each."""
    H = max(cv.size()[1] for cv in cvs)
    parts, x = [], 0
    for cv, cap in zip(cvs, caps):
        w, h = cv.size()
        cw = max(w, tw(cap, fs) + 4)
        ox = cv.x0 - (x + (cw - w) / 2)
        oy = cv.y0 - (H - h)
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


# ------------------------------------------------------------ 3D objects with flat faces
def rot_view(p, yaw, pitch):
    cy_, sy_ = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))
    x, y, z = p
    x1, z1 = x * cy_ + z * sy_, -x * sy_ + z * cy_
    return (x1, y * cp + z1 * sp, -y * sp + z1 * cp)


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
        pts = [rot_view(p, yaw, pitch) for p in self.v]
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

    def draw(self, cv, k, yaw, pitch, dashed=True):
        pts, vis, nrm = self.view(yaw, pitch)
        Pj = lambda p: (p[0] * k, -p[1] * k)
        for fi, fc in enumerate(self.f):
            if vis[fi]:
                n = nrm[fi]
                col = TOP3 if n[1] > 0.5 else SIDE if n[0] > 0.3 else FILL
                cv.poly([Pj(pts[i]) for i in fc], col, 2.4)
        if dashed:
            for (a, b), fs in self.edges.items():
                if not any(vis[f] for f in fs):
                    cv.line(Pj(pts[a]), Pj(pts[b]), dashed=True, sw=1.6)
        return cv


def _shift(v, o):
    return [(x + o[0], y + o[1], z + o[2]) for x, y, z in v]


def box(L, H, W, o=(0, 0, 0)):
    v = [(x, y, z) for x in (0, L) for y in (0, H) for z in (0, W)]
    idx = {p: i for i, p in enumerate(v)}
    g = lambda *ps: [idx[p] for p in ps]
    f = [g((0, 0, 0), (L, 0, 0), (L, H, 0), (0, H, 0)), g((0, 0, W), (L, 0, W), (L, H, W), (0, H, W)),
         g((0, 0, 0), (0, 0, W), (0, H, W), (0, H, 0)), g((L, 0, 0), (L, 0, W), (L, H, W), (L, H, 0)),
         g((0, 0, 0), (L, 0, 0), (L, 0, W), (0, 0, W)), g((0, H, 0), (L, H, 0), (L, H, W), (0, H, W))]
    return Solid(_shift(v, o), f)


def prism_lying(w=1.2, h=0.95, D=1.8, o=(0, 0, 0)):
    """Triangular prism lying on a rectangle face: triangle ends in the y-z plane, length along x."""
    tri = [(0, 0), (w, 0), (w / 2, h)]          # (z, y)
    v = [(0, y, z) for z, y in tri] + [(D, y, z) for z, y in tri]
    f = [[0, 1, 2], [3, 4, 5]] + [[i, (i + 1) % 3, 3 + (i + 1) % 3, 3 + i] for i in range(3)]
    return Solid(_shift(v, o), f)


def prism_standing(w=1.1, d=0.95, H=1.5):
    """Triangular prism standing on a triangle face."""
    tri = [(0, 0), (w, 0), (w / 2, d)]          # (x, z)
    v = [(x, 0, z) for x, z in tri] + [(x, H, z) for x, z in tri]
    f = [[0, 1, 2], [3, 4, 5]] + [[i, (i + 1) % 3, 3 + (i + 1) % 3, 3 + i] for i in range(3)]
    return Solid(v, f)


def pyramid(s=1.3, h=1.3, o=(0, 0, 0)):
    v = [(0, 0, 0), (s, 0, 0), (s, 0, s), (0, 0, s), (s / 2, h, s / 2)]
    f = [[0, 1, 2, 3]] + [[i, (i + 1) % 4, 4] for i in range(4)]
    return Solid(_shift(v, o), f)


def tri_pyramid(s=1.5, h=1.3):
    """Triangle-based pyramid: a triangle base and 3 triangle faces that meet at a point."""
    d = s * math.sqrt(3) / 2
    v = [(0, 0, 0), (s, 0, 0), (s / 2, 0, d), (s / 2, h, d / 3)]
    f = [[0, 1, 2], [0, 1, 3], [1, 2, 3], [2, 0, 3]]
    return Solid(v, f)


COUNTS = {CUBE: (6, 12, 8), RP: (6, 12, 8), TP: (5, 9, 6), SP: (5, 8, 5), TBP: (4, 6, 4)}

VIEWS = {
    "cube": (lambda: box(1.1, 1.1, 1.1), 30, 22),
    "cube_turned": (lambda: box(1.1, 1.1, 1.1), 50, 30),
    "rp_flat": (lambda: box(1.9, 0.8, 1.0), 25, 22),
    "rp_tall": (lambda: box(0.8, 1.8, 0.7), 35, 18),
    "rp_turned": (lambda: box(1.6, 1.0, 0.8), -35, 24),
    "tp_lying": (lambda: prism_lying(), 30, 20),
    "tp_end": (lambda: prism_lying(), 120, 25),
    "tp_standing": (lambda: prism_standing(), 20, 35),
    "sp": (lambda: pyramid(), 25, 18),
    "sp_turned": (lambda: pyramid(1.2, 1.5), -30, 25),
    "tbp": (lambda: tri_pyramid(), -160, 20),
    "tbp_turned": (lambda: tri_pyramid(1.4, 1.6), 45, 22),
}
VIEW_KIND = {"cube": CUBE, "cube_turned": CUBE, "rp_flat": RP, "rp_tall": RP, "rp_turned": RP,
             "tp_lying": TP, "tp_end": TP, "tp_standing": TP, "sp": SP, "sp_turned": SP, "tbp": TBP, "tbp_turned": TBP}
for _v, (_f, _y, _p) in VIEWS.items():
    _s = _f()
    assert tuple(_s.count[x] for x in ("faces", "edges", "vertices")) == COUNTS[VIEW_KIND[_v]], _v
    _seen = _s.seen(_y, _p)
    assert 1 < _seen["faces"] < _s.count["faces"], (_v, _seen)


def solid_cv(view, k=50):
    f, yaw, pitch = VIEWS[view]
    return f().draw(Canvas(), k, yaw, pitch)


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
    R_ = lambda p: _rot90(p, lying)
    cv = Canvas()
    cv.poly(R_(ellipse(0, 0, rx, ry, 180, 360) + ellipse(0, h, rx, ry, 0, 180)), FILL, 0)
    cv.poly(R_(ellipse(0, 0, rx, ry, 0, 360)[:-1]), TOP3, 2.4)
    cv.pline(R_([(-rx, 0), (-rx, h)]))
    cv.pline(R_([(rx, 0), (rx, h)]))
    cv.pline(R_(ellipse(0, h, rx, ry, 0, 180)))
    cv.pline(R_(ellipse(0, h, rx, ry, 180, 360)), dashed=True, sw=1.6)
    return cv


def cone_cv(s=1.0, how="up"):
    """how: 'up' (point at the top), 'down' (point at the bottom), 'side' (lying down)."""
    rx, ry, h = 38 * s, 11 * s, 80 * s
    cv = Canvas()
    if how == "down":
        cv.poly([(0, h)] + ellipse(0, 0, rx, ry, 0, 180), FILL, 0)
        cv.pline([(-rx, 0), (0, h), (rx, 0)])
        cv.poly(ellipse(0, 0, rx, ry, 0, 360)[:-1], TOP3, 2.4)
        return cv
    R_ = lambda p: _rot90(p, how == "side")
    cv.poly(R_([(0, 0)] + ellipse(0, h, rx, ry, 180, 0)), FILL, 0)
    cv.poly(R_([(0, 0)] + ellipse(0, h, rx, ry, 0, 180)), FILL, 0)
    cv.pline(R_([(-rx, h), (0, 0), (rx, h)]))
    cv.pline(R_(ellipse(0, h, rx, ry, 0, 180)))
    cv.pline(R_(ellipse(0, h, rx, ry, 180, 360)), dashed=True, sw=1.6)
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
    raise KeyError(key)


KIND = dict(VIEW_KIND, cyl=CYL, cyl_lying=CYL, cone=CONE, cone_down=CONE, cone_side=CONE)



def sphere_cv(s=1.0):
    r = 40 * s
    cv = Canvas()
    cv.circle((0, 0), r, fill=FILL)
    cv.pline(ellipse(0, 0, r, r * 0.28, 0, 180), sw=1.6)
    cv.pline(ellipse(0, 0, r, r * 0.28, 180, 360), dashed=True, sw=1.4)
    return cv


def pic(key, s=1.0):
    if key == "sph":
        return sphere_cv(s)
    return pic3d(key, s)


KIND["sph"] = SPH


def house3d_cv(k=46):
    cv = Canvas()
    box(1.8, 1.0, 1.1).draw(cv, k, 38, 20, dashed=False)
    prism_lying(1.1, 0.8, 1.8, (0, 1.0, 0)).draw(cv, k, 38, 20, dashed=False)
    return cv


def silo_cv(rx=30, ry=9, h=70, hc=48, s=1.0):
    """A cylinder with a cone on top. The cone sides are true tangents to the rim."""
    rx, ry, h, hc = rx * s, ry * s, h * s, hc * s
    cv = Canvas()
    cv.poly(ellipse(0, 0, rx, ry, 180, 360) + ellipse(0, h, rx, ry, 0, 180), FILL, 0)
    cv.pline([(-rx, 0), (-rx, h)])
    cv.pline([(rx, 0), (rx, h)])
    cv.pline(ellipse(0, h, rx, ry, 0, 180))
    cv.pline(ellipse(0, h, rx, ry, 180, 360), dashed=True, sw=1.6)
    d = math.degrees(math.asin(ry / hc))
    arc = ellipse(0, 0, rx, ry, -d, 180 + d, 60)
    cv.poly([(0, -hc)] + arc, BASE, 0)
    cv.pline([arc[-1], (0, -hc), arc[0]])
    cv.pline(arc)
    return cv


def sq(x, y, w, h):
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]


def net_cube(k=34):
    cv = Canvas()
    for c, r in [(0, 1), (1, 1), (2, 1), (3, 1), (1, 0), (1, 2)]:
        cv.poly(sq(c * k, r * k, k, k), FILL)
    return cv


# ------------------------------------------------------------ 2D shapes (screen coordinates, y down)
def regular(n, r, start=-90):
    return [(r * math.cos(math.radians(start + 360.0 * i / n)), r * math.sin(math.radians(start + 360.0 * i / n))) for i in range(n)]


def R(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def area(pts):
    n = len(pts)
    return sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n)) / 2.0


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


def simplify(pts):
    out = list(pts)
    changed = True
    while changed:
        changed = False
        n = len(out)
        for i in range(n):
            a, b, c = out[i - 1], out[i], out[(i + 1) % n]
            if abs((b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])) < 1e-6:
                del out[i]
                changed = True
                break
    return out


def interior_angles(pts):
    s = 1 if area(pts) > 0 else -1
    n = len(pts)
    out = []
    for i in range(n):
        a, b, c = pts[i - 1], pts[i], pts[(i + 1) % n]
        u = (b[0] - a[0], b[1] - a[1])
        v = (c[0] - b[0], c[1] - b[1])
        turn = math.degrees(math.atan2(u[0] * v[1] - u[1] * v[0], u[0] * v[0] + u[1] * v[1])) * s
        out.append(180 - turn)
    assert abs(sum(out) - 180 * (n - 2)) < 1e-6
    return out


def lengths(pts):
    n = len(pts)
    return [math.hypot(pts[(i + 1) % n][0] - pts[i][0], pts[(i + 1) % n][1] - pts[i][1]) for i in range(n)]


def square_corners(pts):
    return sum(1 for a in interior_angles(simplify(pts)) if abs(a - 90) < 1e-6)


def all_equal(pts):
    L = lengths(simplify(pts))
    return max(L) - min(L) < 1e-6


def classify(pts):
    p = simplify(pts)
    n = len(p)
    if n == 3:
        return "triangle"
    if n == 4:
        L = lengths(p)
        ra = square_corners(p)
        sv = [(p[(i + 1) % 4][0] - p[i][0], p[(i + 1) % 4][1] - p[i][1]) for i in range(4)]
        par = sum(1 for i, j in [(0, 2), (1, 3)] if abs(sv[i][0] * sv[j][1] - sv[i][1] * sv[j][0]) < 1e-6)
        if ra == 4:
            return "square" if max(L) - min(L) < 1e-6 else "rectangle"
        if par == 1:
            return "trapezoid"
        if par == 2:
            return "rhombus" if max(L) - min(L) < 1e-6 else "parallelogram"
        return "quadrilateral"
    return {5: "pentagon", 6: "hexagon", 7: "heptagon", 8: "octagon"}[n]


def tpts(pts, deg=0, s=1.0):
    """Turn a shape about its centre, and scale it."""
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    c, si = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return [(((x - cx) * c - (y - cy) * si) * s, ((x - cx) * si + (y - cy) * c) * s) for x, y in pts]


SHAPES = {
    "tri_eq": regular(3, 42),
    "tri_iso": [(0, 80), (50, 80), (25, 0)],
    "tri_right": [(0, 0), (0, 60), (80, 60)],
    "tri_thin": [(0, 0), (100, 20), (20, 45)],
    "square": R(0, 0, 62, 62),
    "rect": R(0, 0, 100, 50),
    "rect_tall": R(0, 0, 40, 90),
    "rhombus": [(0, 0), (60, 0), (60 + 60 * math.cos(math.radians(55)), 60 * math.sin(math.radians(55))),
                (60 * math.cos(math.radians(55)), 60 * math.sin(math.radians(55)))],
    "trap": [(0, 60), (100, 60), (75, 0), (25, 0)],
    "rtrap": [(0, 0), (50, 0), (90, 60), (0, 60)],
    "pent_reg": regular(5, 44),
    "pent_house": [(0, 40), (40, 0), (80, 40), (80, 100), (0, 100)],
    "pent_odd": [(0, 0), (90, 0), (110, 45), (50, 80), (0, 55)],
    "hex_reg": regular(6, 44, 0),
    "hex_L": [(0, 0), (40, 0), (40, 55), (90, 55), (90, 95), (0, 95)],
    "hex_arrow": [(0, 0), (50, 0), (90, 40), (50, 80), (0, 80), (40, 40)],
    "hept_arrow": [(-44, -14), (6, -14), (6, -38), (44, 0), (6, 38), (6, 14), (-44, 14)],
    "oct_reg": regular(8, 44, 22.5),
    "oct_cut": [(20, 0), (100, 0), (120, 20), (120, 60), (100, 80), (20, 80), (0, 60), (0, 20)],
}
NAME = {"tri_eq": "triangle", "tri_iso": "triangle", "tri_right": "triangle", "tri_thin": "triangle", "square": "square",
        "rect": "rectangle", "rect_tall": "rectangle", "rhombus": "rhombus", "trap": "trapezoid", "rtrap": "trapezoid",
        "pent_reg": "pentagon", "pent_house": "pentagon", "pent_odd": "pentagon", "hex_reg": "hexagon",
        "hex_L": "hexagon", "hex_arrow": "hexagon", "hept_arrow": "heptagon", "oct_reg": "octagon", "oct_cut": "octagon"}
CORNERS = {"tri_eq": 0, "tri_iso": 0, "tri_right": 1, "tri_thin": 0, "square": 4, "rect": 4, "rect_tall": 4, "rhombus": 0,
           "trap": 0, "rtrap": 2, "pent_reg": 0, "pent_house": 3, "hex_reg": 0, "hex_L": 5}
for _k, _p in SHAPES.items():
    check_poly(_p)
    assert classify(_p) == NAME[_k], (_k, classify(_p))
for _k, _n in CORNERS.items():
    assert square_corners(SHAPES[_k]) == _n, (_k, square_corners(SHAPES[_k]))


def n_sides(key):
    return len(simplify(SHAPES[key]))


def shape(key, deg=0, s=1.0, fill=FILL):
    pts = tpts(SHAPES[key], deg, s)
    check_poly(pts)
    cv = Canvas()
    cv.poly(pts, fill, 3)
    return cv


def fit_shape(key, w=88, h=104, deg=0, kmax=0.9):
    k = kmax
    while True:
        cv = shape(key, deg, k)
        if cv.size()[0] <= w and cv.size()[1] <= h:
            return cv
        k *= 0.97


def circle_cv(r=40):
    cv = Canvas()
    cv.circle((0, 0), r, fill=FILL, sw=3)
    return cv


def grid_q(pos, cells_right, cells_other, label, q, e):
    p = pos.next()
    cells = list(cells_other)
    cells.insert(p, cells_right)
    L = "ABCD"[p]
    return mcq_fixed(fig(grid_svg(cells, label)) + q, list("ABCD"), L, e % L)


def plural(n, one, many):
    return "%d %s" % (n, one if n == 1 else many)


# ------------------------------------------------------------ set 1: sides and vertices of 2D shapes
def set_sides(rnd, pos, P):
    its = []
    rows = [("tri_eq", 0, 1.0, "sides"), ("square", 45, 0.9, "vertices"), ("rect", 0, 0.9, "sides"),
            ("pent_reg", 0, 1.0, "vertices"), ("hex_reg", 0, 1.0, "sides"), ("oct_reg", 0, 1.0, "vertices"),
            ("pent_house", 0, 0.8, "sides"), ("hex_L", 90, 0.85, "vertices"), ("tri_right", 160, 0.9, "vertices"),
            ("trap", 0, 0.9, "sides"), ("hept_arrow", 0, 0.95, "sides"), ("oct_cut", 0, 0.8, "vertices"),
            ("hex_arrow", 0, 0.9, "vertices")]
    extra = {"square": " It is turned, but it is still a square.",
             "hex_L": " Count the corner that points in too.",
             "hept_arrow": " Count the short sides near the point too.",
             "oct_cut": " Count the small corners too.",
             "hex_arrow": " Count the corner that points in too.",
             "tri_right": " It is turned, but it still has 3 corners.",
             "pent_house": " It looks like a house, but it is one shape."}
    for key, deg, s, what in rows:
        n = n_sides(key)
        one = "side" if what == "sides" else "vertex"
        q = fig(shape(key, deg, s).svg("a 2D shape")) + "How many %s does this shape have?" % what
        e = ("Put your finger on one %s. Count as you go around. Stop when you get back to the start. "
             "Do not count the first one twice: %d %s." % (one, n, what)) + extra.get(key, "")
        its.append(mcq(q, n, [n + 1, n - 1, n + 2], e))
    its.append(mcq("A shape has 5 sides. How many vertices does it have?", 5, [6, 4, 10],
                   "A 2D shape has the same number of vertices as sides. 5 sides, so 5 vertices."))
    its.append(mcq("A shape has 6 sides and 6 vertices. What is it?", "hexagon", ["pentagon", "octagon", "cube"],
                   "6 sides make a hexagon. A pentagon has 5 sides and an octagon has 8. A cube is a 3D object."))
    its.append(mcq("Which shape has 8 sides?", "octagon", ["hexagon", "pentagon", "square"],
                   "An octagon has 8 sides and 8 vertices, like a stop sign."))
    n, he, his = P.next()
    its.append(mcq("%s counts the vertices of a square: 1, 2, 3, 4, 5. %s counted the first corner again. "
                   "How many vertices does a square have?" % (n, he.capitalize()), 4, [5, 8, 3],
                   "A square has 4 vertices. %s touched the first corner again at the end and counted it twice." % n))
    its.append(grid_q(pos, fit_shape("pent_odd"), [fit_shape("tri_iso"), fit_shape("hex_reg"), fit_shape("square")],
                      "four 2D shapes labelled A to D", "Which shape has 5 vertices?",
                      "%s has 5 vertices. The others have 3, 6 and 4."))
    its.append(grid_q(pos, fit_shape("hex_L"), [fit_shape("pent_house"), fit_shape("oct_reg"), fit_shape("rect")],
                      "four 2D shapes labelled A to D", "Which shape has 6 sides?",
                      "%s has 6 sides, so it is a hexagon. The others have 5, 8 and 4 sides."))
    its.append(grid_q(pos, fit_shape("tri_thin"), [fit_shape("trap"), fit_shape("pent_reg"), fit_shape("rhombus")],
                      "four 2D shapes labelled A to D", "Which shape has 3 vertices?",
                      "%s has 3 vertices, so it is a triangle. The others have 4, 5 and 4."))
    assert len(its) == 20, len(its)
    return {"title": "Sides and vertices of 2D shapes", "items": its}


# ------------------------------------------------------------ set 2: sort by two attributes
BOTH, NEITHER = "both rules", "neither rule"


def rule_q(key, deg, s, r1, r2, t1, t2, says):
    pts = SHAPES[key]
    a, b = t1(pts), t2(pts)
    right = BOTH if a and b else NEITHER if not a and not b else "only “%s”" % (r1 if a else r2)
    q = (fig(shape(key, deg, s).svg("a 2D shape")) +
         "Sort by two rules: “%s” and “%s”. Which rules does this shape follow?" % (r1, r2))
    return mcq(q, right, [BOTH, "only “%s”" % r1, "only “%s”" % r2, NEITHER], says(pts) + " So it follows %s." % right)


def set_sort(rnd, pos, P):
    its = []
    four = lambda p: n_s(p) == 4
    sqc = lambda p: square_corners(p) > 0
    three = lambda p: n_s(p) == 3
    eq = lambda p: all_equal(p)

    def says_a(p):
        n, c = n_s(p), square_corners(p)
        return "It has %s and %s." % (plural(n, "side", "sides"), "no square corners" if c == 0 else plural(c, "square corner", "square corners"))

    def says_b(p):
        n = n_s(p)
        return "It has %s. %s" % (plural(n, "side", "sides"),
                                  "All its sides are the same length." if all_equal(p) else "Its sides are not all the same length.")
    for key, deg, s in [("square", 45, 0.9), ("trap", 0, 0.9), ("tri_right", 0, 1.0), ("hex_reg", 0, 1.0)]:
        its.append(rule_q(key, deg, s, "4 sides", "square corner", four, sqc, says_a))
    for key, deg, s in [("tri_eq", 0, 1.0), ("tri_iso", 0, 1.0), ("pent_reg", 0, 1.0), ("rect", 0, 0.9)]:
        its.append(rule_q(key, deg, s, "3 sides", "sides all the same", three, eq, says_b))
    assert sorted(it["c"][0] for it in its) == sorted([BOTH, "only “4 sides”", "only “square corner”", NEITHER,
                                                      BOTH, "only “3 sides”", "only “sides all the same”", NEITHER])
    L = "four 2D shapes labelled A to D"
    assert n_s(SHAPES["rhombus"]) == 4 and square_corners(SHAPES["rhombus"]) == 0
    its.append(grid_q(pos, fit_shape("rhombus"), [fit_shape("square"), fit_shape("rect"), fit_shape("tri_right")], L,
                      "Which shape has 4 sides and no square corners?",
                      "%s has 4 sides, but none of its corners is a square corner. The square and the rectangle have 4 square corners. "
                      "The triangle has only 3 sides."))
    its.append(grid_q(pos, fit_shape("tri_right"), [fit_shape("tri_eq"), fit_shape("square"), fit_shape("rtrap")], L,
                      "Which shape has 3 sides and a square corner?",
                      "%s has 3 sides and 1 square corner. The other triangle has no square corner. "
                      "The other two shapes have square corners, but 4 sides."))
    assert all_equal(SHAPES["hex_reg"]) and not all_equal(SHAPES["hex_L"])
    its.append(grid_q(pos, fit_shape("hex_reg"), [fit_shape("square"), fit_shape("hex_L"), fit_shape("tri_eq")], L,
                      "Which shape has 6 sides that are all the same length?",
                      "%s has 6 sides and they are all the same length. The other 6-sided shape has long and short sides. "
                      "The square and the triangle have equal sides, but not 6 of them."))
    its.append(grid_q(pos, fit_shape("trap"), [fit_shape("square"), fit_shape("rect"), fit_shape("rect_tall")], L,
                      "The rule is “4 sides and 4 square corners”. Which shape does not follow the rule?",
                      "%s has 4 sides, but its corners are not square corners. The other 3 shapes have 4 square corners."))
    its.append(mcq("Which 3D object can roll and has a vertex?", CONE, [CYL, SPH, CUBE],
                   "A cone rolls on its curved surface and has 1 vertex at its point. A cylinder and a sphere roll but have no vertices. "
                   "A cube has vertices but does not roll."))
    its.append(mcq("Which 3D object can roll and has 2 flat faces?", CYL, [CONE, SPH, CUBE],
                   "A cylinder rolls on its curved surface and has 2 flat circle faces. A cone has 1 flat face, and a sphere has none."))
    its.append(mcq("Which 3D object has only flat faces and a triangle face?", TP, [CUBE, CONE, CYL],
                   "A triangular prism has a triangle face at each end, and all its faces are flat. "
                   "A cone looks like a triangle from the side, but it has a curved surface and no triangle face."))
    its.append(mcq("Which 3D object has 6 faces, and all of them are squares?", CUBE, [RP, SP, TP],
                   "A cube has 6 faces and every face is a square of the same size. A rectangular prism has 6 faces too, "
                   "but they are not all squares."))
    its.append(mcq("Which 3D object has only flat faces and comes to a point?", SP, [CONE, CUBE, TP],
                   "A square-based pyramid has 5 flat faces that come to a point at the top. "
                   "A cone comes to a point too, but it has a curved surface."))
    its.append(mcq("A shape has 4 sides that are all the same length. It has 4 square corners. What is it?", "square",
                   ["rectangle", "trapezoid", "cube"],
                   "4 equal sides and 4 square corners make a square. A rectangle has square corners, but 2 long and 2 short sides."))
    n, he, his = P.next()
    its.append(mcq("%s puts a square and a rectangle in the same group. What could %s rule be?" % (n, his), "4 square corners",
                   ["sides all the same", "3 sides", "curved sides"],
                   "A square and a rectangle both have 4 square corners. Only the square has sides that are all the same length."))
    its.append(mcq("Which 2D shape has no sides and no vertices?", "circle", ["triangle", "square", "hexagon"],
                   "A circle is round. It has no straight sides and no corners. The other shapes have sides and vertices."))
    assert len(its) == 20, len(its)
    return {"title": "Sort shapes by two attributes", "items": its}


def n_s(pts):
    return len(simplify(pts))


# ------------------------------------------------------------ set 3: faces, edges, vertices of 3D objects
def set_fev(rnd, P):
    its = []
    its.append(mcq("A flat surface of a 3D object is called a …", "face", ["edge", "vertex", "side"],
                   "A face is a flat surface. An edge is where two faces meet. A vertex is a corner."))
    its.append(mcq("The line where two faces of an object meet is called an …", "edge", ["vertex", "face", "angle"],
                   "Where two faces meet there is an edge."))
    its.append(mcq("A corner of a 3D object, where edges meet, is called a …", "vertex", ["edge", "face", "side"],
                   "A corner is a vertex. When there is more than one, we say vertices."))
    hidden = {"faces": "Some faces are at the back or underneath. You cannot see them, but count them too.",
              "edges": "The dashed lines show edges at the back. Count them too.",
              "vertices": "Some vertices are at the back, where the dashed lines meet. Count them too. Count each vertex once."}
    for view, what in [("cube", "faces"), ("cube", "edges"), ("cube_turned", "vertices"), ("rp_flat", "faces"),
                       ("rp_turned", "edges"), ("rp_tall", "vertices"), ("tp_lying", "faces"), ("tp_lying", "edges"),
                       ("tp_standing", "vertices"), ("sp", "faces"), ("sp", "edges"), ("sp_turned", "vertices")]:
        kind = VIEW_KIND[view]
        F, E, V = COUNTS[kind]
        cnt = {"faces": F, "edges": E, "vertices": V}
        ans = cnt[what]
        vis = seen(view)[what]
        assert vis < ans, (view, what)
        others = [cnt[w] for w in ("faces", "edges", "vertices") if w != what]
        wrong = [vis] + others + [ans + 1, ans - 1]
        q = fig(solid_cv(view).svg("a %s" % kind)) + "This is %s %s. How many %s does it have?" % (art(kind), kind, what)
        e = "%s %s has %d faces, %d edges and %d vertices. %s" % (art(kind).capitalize(), kind, F, E, V, hidden[what])
        if kind == SP and what == "vertices":
            e += " Do not forget the vertex at the top."
        its.append(mcq(q, ans, wrong, e))
    its.append(mcq(fig(cylinder_cv().svg("a cylinder")) + "How many vertices does a cylinder have?", 0, [2, 4, 1],
                   "A cylinder has no corners, so it has 0 vertices. Its edges are round circles, not corners. "
                   "In a drawing it can look like it has 4 corners, but it does not."))
    its.append(mcq(fig(cone_cv().svg("a cone")) + "How many vertices does a cone have?", 1, [0, 2, 3],
                   "A cone has 1 vertex: the point at the top. Its round edge has no corners."))
    its.append(mcq(fig(sphere_cv().svg("a sphere")) + "How many flat faces does a sphere have?", 0, [1, 2, 6],
                   "A sphere is round all over, like a ball. It has no flat faces, no edges and no vertices."))
    n, she, her = P.next()
    its.append(mcq("%s counts the vertices of a cube and gets 9. What did %s do wrong?" % (n, she),
                   "counted one vertex twice", ["missed one vertex", "counted the edges", "counted the faces"],
                   "A cube has 8 vertices. 9 is 1 too many, so %s counted one vertex twice. "
                   "Touch each corner once, or mark it as you count." % n))
    its.append(mcq("Which has more vertices: a cube or a square-based pyramid?", "the cube",
                   ["the pyramid", "They are the same.", "Neither has vertices."],
                   "A cube has 8 vertices. A square-based pyramid has 4 at the bottom and 1 at the top: 5. 8 is more than 5."))
    assert len(its) == 20, len(its)
    return {"title": "Faces, edges and vertices of 3D objects", "items": its}


# ------------------------------------------------------------ set 4: the 2D faces of 3D objects
def set_faces(rnd, pos, P):
    its = []
    its.append(mcq("What shape is each face of a cube?", "a square", ["a triangle", "a circle", "a cube"],
                   "All 6 faces of a cube are squares of the same size. The cube is 3D; its faces are flat 2D squares."))
    its.append(mcq("Which 2D shapes are the faces of a triangular prism?", "2 triangles and 3 rectangles",
                   ["3 triangles and 2 rectangles", "2 triangles and 2 rectangles", "5 triangles"],
                   "A triangular prism has a triangle at each end: 2 triangles. 3 rectangles join them. That is 5 faces."))
    its.append(mcq("Which 2D shapes are the faces of a square-based pyramid?", "1 square and 4 triangles",
                   ["4 squares and 1 triangle", "1 square and 3 triangles", "5 triangles"],
                   "It has 1 square at the bottom and 4 triangles that meet at the top: 5 faces."))
    its.append(mcq("Which 2D shapes are the faces of a rectangular prism, like a cereal box?", "6 rectangles",
                   ["4 rectangles", "6 triangles", "3 rectangles"],
                   "A box has 6 faces: front and back, top and bottom, and 2 ends. Each one is a rectangle. "
                   "You can only see 3 at a time."))
    its.append(mcq(fig(cylinder_cv().svg("a cylinder")) + "What shape are the 2 flat faces of a cylinder?", "circles",
                   ["rectangles", "triangles", "spheres"],
                   "The flat faces of a cylinder are circles. In a drawing they look squashed because we see them from the side."))
    its.append(mcq(fig(cone_cv().svg("a cone")) + "What shape is the flat face of a cone?", "a circle",
                   ["a triangle", "a square", "a cone"],
                   "A cone has 1 flat face: a circle at the bottom. From the side a cone looks like a triangle, "
                   "but it has no triangle face."))
    n, he, his = P.next()
    its.append(mcq("%s dips one face of a cube in paint and presses it on paper. What shape does %s print?" % (n, he), "a square",
                   ["a cube", "a triangle", "a circle"],
                   "Every face of a cube is a square, so the print is a square. A print is flat (2D), so it cannot be a cube."))
    n, he, his = P.next()
    its.append(mcq("%s traces around the bottom of a can of salmon. What shape does %s draw?" % (n, he), "a circle",
                   ["a rectangle", "a cylinder", "a triangle"],
                   "The can is a cylinder. Its bottom face is a circle, so the tracing is a circle."))
    its.append(mcq("You press each face of an object in paint. Which object can print a triangle?", TP, [CONE, CUBE, CYL],
                   "A triangular prism has a triangle face at each end. A cone has only a circle face, "
                   "even though it looks like a triangle from the side."))
    its.append(mcq("Which object can print a square and a triangle?", SP, [CUBE, CONE, CYL],
                   "A square-based pyramid has 1 square face and 4 triangle faces."))
    its.append(mcq("How many square faces does a square-based pyramid have?", 1, [4, 5, 0],
                   "Only the bottom is a square: 1 square face. The other 4 faces are triangles."))
    its.append(mcq("How many triangle faces does a triangular prism have?", 2, [3, 5, 1],
                   "A triangular prism has 1 triangle at each end: 2 triangles. Its other 3 faces are rectangles."))
    its.append(mcq("Which 3D object has no flat faces at all?", SPH, [CYL, CONE, CUBE],
                   "A sphere is round all over. A cylinder has 2 flat faces and a cone has 1."))
    n, she, her = P.next()
    its.append(mcq("%s traces every face of a number cube. How many squares does %s draw?" % (n, she), 6, [3, 8, 4],
                   "A cube has 6 faces, so %s draws 6 squares. You can see only 3 faces at a time. 8 is the number of vertices." % n))
    n, he, his = P.next()
    its.append(mcq("%s traces every flat face of a cylinder. What does %s draw?" % (n, he), "2 circles",
                   ["1 circle", "2 rectangles", "2 triangles"],
                   "A cylinder has a flat circle face at the top and one at the bottom: 2 circles."))
    its.append(mcq(fig(net_cube().svg("a flat pattern of 6 squares")) + "This flat pattern is folded up. Which 3D object does it make?",
                   CUBE, ["square", RP, SP],
                   "6 squares of the same size fold up into a cube: 1 square for each face."))
    L = "four 3D objects labelled A to D"
    s = 0.62
    its.append(grid_q(pos, pic("cyl", s), [pic("cube", s), pic("sp", s), pic("tp_lying", s)], L,
                      "Which object has a circle face?",
                      "%s is a cylinder. It has 2 circle faces. The others have only flat faces with straight sides."))
    its.append(grid_q(pos, pic("cube_turned", s), [pic("rp_flat", s), pic("sp_turned", s), pic("tp_standing", s)], L,
                      "Which object has only square faces?",
                      "%s is a cube: all 6 faces are squares. The box has long rectangle faces. "
                      "The pyramid and the prism have triangle faces."))
    its.append(grid_q(pos, pic("tp_lying", s), [pic("sp", s), pic("rp_tall", s), pic("cone", s)], L,
                      "Which object has triangle faces and rectangle faces?",
                      "%s is a triangular prism: 2 triangles and 3 rectangles. The pyramid has a square and triangles. "
                      "The box has only rectangles. The cone has a circle."))
    its.append(grid_q(pos, pic("sp_turned", s), [pic("cube", s), pic("cyl", s), pic("rp_turned", s)], L,
                      "Which object has 4 triangle faces?",
                      "%s is a square-based pyramid. It has 4 triangle faces and 1 square face."))
    assert len(its) == 20, len(its)
    return {"title": "Which 2D faces does a 3D object have?", "items": its}


# ------------------------------------------------------------ set 5: real objects and riddles
def set_real(rnd, pos, P):
    its = []
    for q, right, wrong, e in [
            ("A soccer ball is shaped like a …", SPH, ["circle", CYL, CONE],
             "A soccer ball is round all over, like a sphere. A circle is a flat 2D shape."),
            ("A hockey puck is shaped like a …", CYL, ["circle", SPH, CONE],
             "A puck has 2 flat circle faces and a curved side, so it is a short cylinder."),
            ("A cereal box is shaped like a …", RP, ["rectangle", CUBE, TP],
             "A cereal box has 6 rectangle faces. They are not all squares, so it is a rectangular prism, not a cube."),
            ("A number cube in a board game is shaped like a …", CUBE, ["square", RP, SPH],
             "It has 6 square faces of the same size, so it is a cube. A square is only one flat face."),
            ("Ava buys an ice cream at Kits Beach in Vancouver. Her waffle cone is shaped like a …", CONE, ["triangle", SP, CYL],
             "It has 1 round opening at the top and comes to a point, so it is a cone. A triangle is flat."),
            ("A tent at a campsite in the Okanagan has a triangle at the front and at the back. Which object is it like?", TP,
             ["triangle", SP, CONE],
             "A triangle at each end, joined by rectangles, makes a triangular prism. It has no single point at the top."),
    ]:
        its.append(mcq(q, right, wrong, e))
    for q, right, wrong, e in [
            ("I have 6 faces. All of them are squares. What am I?", CUBE, [RP, "square", SP],
             "6 square faces of the same size: a cube."),
            ("I can roll. I have 1 flat face and 1 vertex. What am I?", CONE, [CYL, SPH, SP],
             "A cone has 1 flat circle face and 1 vertex at its point, and it rolls on its curved surface."),
            ("I have 5 faces: 1 square and 4 triangles. What am I?", SP, [TP, CUBE, CONE],
             "A square-based pyramid has a square at the bottom and 4 triangles that meet at the top."),
            ("I can roll. I have 2 flat faces, and they are circles. What am I?", CYL, [CONE, SPH, "circle"],
             "A cylinder has 2 circle faces and a curved side that rolls."),
            ("I have no flat faces, no edges and no vertices. What am I?", SPH, [CYL, CONE, "circle"],
             "A sphere is round all over. A circle is flat (2D), so it is not a 3D object."),
            ("I have 2 triangle faces and 3 rectangle faces. What am I?", TP, [SP, RP, CONE],
             "A triangle at each end and 3 rectangles between them: a triangular prism."),
            ("I have 6 faces, 12 edges and 8 vertices. My faces are not all squares. What am I?", RP, [CUBE, TP, SP],
             "A cube and a rectangular prism both have 6 faces, 12 edges and 8 vertices. "
             "The faces are not all squares, so it is a rectangular prism."),
    ]:
        its.append(mcq(q, right, wrong, e))
    n, she, her = P.next()
    its.append(mcq("%s builds a cube with straws and balls of clay. Each straw is an edge. How many straws does %s need?"
                   % (n, she), 12, [8, 6, 24],
                   "A cube has 12 edges: 4 on the top, 4 on the bottom and 4 going up and down. 4 + 4 + 4 = 12 straws."))
    n, he, his = P.next()
    its.append(mcq("%s builds a cube with straws. A ball of clay holds the straws together at each vertex. How many balls of clay does %s need?"
                   % (n, he), 8, [12, 9, 6],
                   "A cube has 8 vertices: 4 on the top and 4 on the bottom. 4 + 4 = 8 balls of clay. Count each corner once."))
    n, he, his = P.next()
    its.append(mcq("%s is stacking blocks. Which block is hard to stack because it has no flat face?" % n, SPH, [CUBE, CYL, RP],
                   "A sphere has no flat face, so it rolls away. A cube, a cylinder and a rectangular prism all have flat faces to stack on."))
    n, she, her = P.next()
    its.append(mcq("%s wants a block that can roll and can also be stacked on. Which block should %s pick?" % (n, she), CYL,
                   [SPH, CUBE, SP],
                   "A cylinder rolls on its curved side and stacks on its flat circle faces. "
                   "A sphere only rolls. A cube and a pyramid do not roll."))
    n, he, his = P.next()
    its.append(mcq("%s looks at a box of tissues and sees 3 faces. How many faces does the box have?" % n, 6, [3, 4, 8],
                   "A box is a rectangular prism. It has 6 faces. The other 3 are at the back, on the side and underneath."))
    its.append(mcq(fig(silo_cv().svg("a grain bin on a farm")) + "This grain bin on a farm is made of two 3D objects. Which two?",
                   "a cylinder and a cone", ["a rectangle and a triangle", "a cylinder and a pyramid", "a cone and a cube"],
                   "The tall part has 2 circle faces and a curved side: a cylinder. The roof has a circle base and a point: a cone. "
                   "A rectangle and a triangle are flat 2D shapes."))
    n, he, his = P.next()
    L = "four 3D objects labelled A to D"
    s = 0.62
    its.append(grid_q(pos, pic("cone_down", s), [pic("cyl", s), pic("sp", s), pic("sph", s)], L,
                      "%s's riddle: “I have 1 flat face and 1 vertex.” Which picture is %s riddle about?" % (n, his),
                      "%s is a cone. It is upside down, but it still has 1 circle face and 1 vertex."))
    assert len(its) == 20, len(its)
    return {"title": "Real objects and shape riddles", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    flat2d = row_svg([shape("tri_eq", 0, 0.75), shape("square", 0, 0.8), shape("rect", 0, 0.7), shape("pent_reg", 0, 0.75),
                      shape("hex_reg", 0, 0.75), shape("oct_reg", 0, 0.75)],
                     ["triangle", "square", "rectangle", "pentagon", "hexagon", "octagon"],
                     "a triangle, a square, a rectangle, a pentagon, a hexagon and an octagon", gap=14, fs=14)
    solids = row_svg([solid_cv("cube", 40), solid_cv("rp_flat", 38), solid_cv("tp_lying", 40), solid_cv("sp", 40)],
                     ["cube", "rectangular prism", "triangular prism", "square-based pyramid"],
                     "a cube, a rectangular prism, a triangular prism and a square-based pyramid", gap=14, fs=14)
    curved = row_svg([cylinder_cv(0.8), cone_cv(0.8), sphere_cv(0.85)], ["cylinder", "cone", "sphere"],
                     "a cylinder, a cone and a sphere", gap=40, fs=14)
    return (
        "<h2>2D shapes: sides and vertices</h2>"
        "<p>A 2D shape is flat. A <b>side</b> is a straight line. A <b>vertex</b> is a corner where two sides meet. "
        "More than one vertex are called <b>vertices</b>. A 2D shape has the same number of sides and vertices.</p>"
        "<figure class='sn-fig'>" + flat2d +
        "<figcaption>3, 4, 4, 5, 6 and 8 sides. Count the sides to name the shape.</figcaption></figure>" +
        ex("Example 1", "How many vertices does a pentagon have?",
           "Put your finger on one corner. Count as you go around: 1, 2, 3, 4, 5. Stop at the start. Do not count it again.",
           "5 vertices") +
        "<h2>Sort by two rules</h2>"
        "<p>You can sort shapes by more than one thing: the number of sides, square corners, or sides that are all the same length. "
        "A shape can follow both rules, one rule, or neither rule.</p>" +
        table(["Shape", "4 sides?", "Square corner?", "Group"], [
            ["square", "yes", "yes", "both rules"],
            ["trapezoid", "yes", "no", "only “4 sides”"],
            ["triangle with a square corner", "no", "yes", "only “square corner”"],
            ["hexagon", "no", "no", "neither rule"]]) +
        "<h2>3D objects: faces, edges and vertices</h2>"
        "<p>A 3D object is solid, like a box or a ball. A <b>face</b> is a flat surface. An <b>edge</b> is where two faces meet. "
        "A <b>vertex</b> is a corner. Dashed lines show edges at the back.</p>"
        "<figure class='sn-fig'>" + solids +
        "<figcaption>A prism has the same shape at both ends. A pyramid comes to a point.</figcaption></figure>"
        "<figure class='sn-fig'>" + curved +
        "<figcaption>A cylinder, a cone and a sphere have a curved surface, so they can roll.</figcaption></figure>" +
        table(["Object", "Flat faces", "Edges", "Vertices", "Like a …"], [
            ["Cube", "6 squares", "12", "8", "number cube"],
            ["Rectangular prism", "6 rectangles", "12", "8", "cereal box"],
            ["Triangular prism", "2 triangles, 3 rectangles", "9", "6", "tent"],
            ["Square-based pyramid", "1 square, 4 triangles", "8", "5", "pyramid in Egypt"],
            ["Cylinder", "2 circles", "2 round edges", "0", "hockey puck"],
            ["Cone", "1 circle", "1 round edge", "1", "ice cream cone"],
            ["Sphere", "0", "0", "0", "soccer ball"]]) +
        ex("Example 2", "How many faces does a cube have?",
           "In a picture you see 3 faces. There are 3 more at the back, on the side and underneath. 3 + 3 = 6.", "6 faces") +
        "<h2>The faces are 2D shapes</h2>"
        "<p>Each flat face of a 3D object is a 2D shape. Trace around a face or press it in paint to see the shape.</p>" +
        ex("Example 3", "What 2D shapes are the faces of a triangular prism?",
           "There is a triangle at each end. 3 rectangles join the ends.", "2 triangles and 3 rectangles") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting the first vertex twice", "Stop when you get back to the start, or mark each corner as you count"],
            ["Giving a cylinder vertices", "A cylinder has no corners: 0 vertices. Its edges are round"],
            ["Counting only the faces you can see", "Remember the faces at the back and underneath"],
            ["Saying a cone has a triangle face", "A cone has 1 circle face and a curved surface"],
            ["Calling a can a circle", "A can is a cylinder (3D). Its flat faces are circles (2D)"],
        ])
    )


FAQ = [
    {"q": "What do Grade 2 students learn about shapes in the BC curriculum?",
     "a": "In Geometry and measurement, Grade 2 students describe, compare and sort 2D shapes and 3D objects by more than one attribute, such as sides, vertices, faces and whether they roll."},
    {"q": "How many vertices does a cylinder have?",
     "a": "A cylinder has 0 vertices. It has 2 flat circle faces and a curved surface, and its edges are round, so it has no corners."},
    {"q": "What is the difference between a 2D shape and a 3D object?",
     "a": "A 2D shape is flat, like a square drawn on paper. A 3D object is solid, like a box or a ball, and its flat faces are 2D shapes."},
    {"q": "How can I help my child learn 2D shapes and 3D objects at home?",
     "a": "Go on a shape hunt in the kitchen: a can is a cylinder and a cereal box is a rectangular prism. Count the faces, edges and vertices together, and trace the faces on paper."},
]


# ------------------------------------------------------------ build
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
    rnd = random.Random(52809)
    P = People(rnd)
    pos = Pos(rnd)
    sets = [set_sides(rnd, pos, P), set_sort(rnd, pos, P), set_fev(rnd, P), set_faces(rnd, pos, P), set_real(rnd, pos, P)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-2", "slug": "2d-shapes-and-3d-objects", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "2D Shapes and 3D Objects: Sides, Vertices, Faces and Edges",
        "seo_title": "Grade 2 Math 2D Shapes and 3D Objects Worksheets (BC Curriculum, Free, Answer Key)",
        "short_title": "2D shapes and 3D objects",
        "domain": "Geometry and measurement",
        "standard_code": "Grade 2: Geometry and measurement",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/2/core",
        "standard_text": "Multiple attributes of 2D shapes and 3D objects",
        "meta_desc": "Free Grade 2 math worksheets on 2D shapes and 3D objects for the BC curriculum: count sides and vertices, "
                     "sort shapes by two rules, count faces, edges and vertices, name the faces of cubes, prisms, pyramids, "
                     "cylinders and cones, and solve shape riddles. 100 questions with an answer key.",
        "key_big": "Count sides and vertices to name a 2D shape. Count faces, edges and vertices to name a 3D object.",
        "key_sub": "Count each vertex once. Remember the faces at the back. A cylinder has 0 vertices and a cone has 1.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(four 3D objects labelled A to D|four 2D shapes labelled A to D)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
