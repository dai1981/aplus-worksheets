# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 3 Math: 2D shapes and 3D objects (Ontario Curriculum 2020, Spatial Sense E1.1, E1.2, E1.3)
  python3 tools/gen_ca_math_g3_shapes.py
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.

Grade 3 students sort and identify cubes, prisms, pyramids, cylinders and cones by comparing their faces,
edges, vertices and angles (E1.1), build and take apart structures and name the 2D shapes and 3D objects
in them (E1.2), and find matching halves: lines of symmetry (E1.3).

Pictures (checked in code):
  objects with flat faces  drawn from 3D vertices and faces, turned (yaw) and seen from a little above (pitch);
              faces you cannot see are left out and their edges are dashed; faces, edges and vertices are counted
              from the same data (V − E + F = 2), and "only counted what you can see" answers come from the picture
  nets        built from exact squares, rectangles, triangles and circles (a cylinder's rectangle is as long as
              the circle is round)
  composites  the parts fill the outline exactly (areas add up) and every part is named from its own corners
  symmetry    a dashed line is a line of symmetry only when reflecting every edge across it gives the same edges;
              lines of symmetry are counted the same way
Wrong answers come from real student mistakes: prism vs pyramid, counting only the faces you can see, edges and
vertices swapped, giving a cylinder vertices, 2D names for 3D objects, adding the sides of the parts, any line that
cuts a shape in two is a line of symmetry, a slide instead of a flip, only looking for up-and-down lines.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL, BASE, SIDE, TOP3 = "#cfe6d6", "#f6dcb4", "#a9d3b6", "#e6f2e9"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
THIN = "#b8b8b8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]

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


# composite objects (E1.2)
def house3d_cv(k=46):
    cv = Canvas()
    box(1.8, 1.0, 1.1).draw(cv, k, 38, 20, dashed=False)
    prism_lying(1.1, 0.8, 1.8, (0, 1.0, 0)).draw(cv, k, 38, 20, dashed=False)
    return cv


def tower_cv(k=46):
    cv = Canvas()
    box(1.1, 1.1, 1.1).draw(cv, k, 30, 20, dashed=False)
    pyramid(1.1, 1.0, (0, 1.1, 0)).draw(cv, k, 30, 20, dashed=False)
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


# ------------------------------------------------------------ nets
def sq(x, y, w, h):
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]


def net_cube(k=34):
    cv = Canvas()
    for c, r in [(0, 1), (1, 1), (2, 1), (3, 1), (1, 0), (1, 2)]:
        cv.poly(sq(c * k, r * k, k, k), FILL)
    return cv


def net_rp(L=60, W=30, H=40):
    cv = Canvas()
    xs = [0, L, L + W, 2 * L + W, 2 * L + 2 * W]
    for i in range(4):
        cv.poly(sq(xs[i], 0, xs[i + 1] - xs[i], H), FILL)
    cv.poly(sq(0, -W, L, W), TOP3)
    cv.poly(sq(0, H, L, W), TOP3)
    return cv


def net_sp(s=46, h=40):
    cv = Canvas()
    cv.poly(sq(0, 0, s, s), FILL)
    cv.poly([(0, 0), (s, 0), (s / 2, -h)], BASE)
    cv.poly([(0, s), (s, s), (s / 2, s + h)], BASE)
    cv.poly([(0, 0), (0, s), (-h, s / 2)], BASE)
    cv.poly([(s, 0), (s, s), (s + h, s / 2)], BASE)
    return cv


def net_tp(w=40, L=62):
    cv = Canvas()
    for i in range(3):
        cv.poly(sq(i * w, 0, w, L), FILL)
    th = w * math.sqrt(3) / 2
    cv.poly([(w, 0), (2 * w, 0), (1.5 * w, -th)], BASE)
    cv.poly([(w, L), (2 * w, L), (1.5 * w, L + th)], BASE)
    return cv


def net_cyl(r=17, h=56):
    cv = Canvas()
    Lr = 2 * math.pi * r                      # the rectangle wraps once round the circle
    cv.poly(sq(0, 0, Lr, h), FILL)
    cv.circle((Lr / 2, -r), r, fill=TOP3)
    cv.circle((Lr / 2, h + r), r, fill=TOP3)
    return cv


# ------------------------------------------------------------ 2D shape facts (screen coordinates, y down)
def area(pts):
    n = len(pts)
    return sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n)) / 2.0


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


def right_angles(pts):
    return sum(1 for a in interior_angles(simplify(pts)) if abs(a - 90) < 1e-6)


def sides(pts):
    return len(simplify(pts))


def classify(pts):
    p = simplify(pts)
    n = len(p)
    if n == 3:
        return "triangle"
    if n == 4:
        L = [math.hypot(p[(i + 1) % 4][0] - p[i][0], p[(i + 1) % 4][1] - p[i][1]) for i in range(4)]
        ra = right_angles(p)
        sv = [(p[(i + 1) % 4][0] - p[i][0], p[(i + 1) % 4][1] - p[i][1]) for i in range(4)]
        par = sum(1 for i, j in [(0, 2), (1, 3)] if abs(sv[i][0] * sv[j][1] - sv[i][1] * sv[j][0]) < 1e-6)
        if ra == 4:
            return "square" if max(L) - min(L) < 1e-6 else "rectangle"
        if par == 1:
            return "trapezoid"
        if par == 2:
            return "parallelogram"
        return "quadrilateral"
    return {5: "pentagon", 6: "hexagon", 7: "heptagon", 8: "octagon"}[n]


def regular(n, r, start):
    return [(r * math.cos(math.radians(start + 360.0 * i / n)), r * math.sin(math.radians(start + 360.0 * i / n))) for i in range(n)]


def R(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def scaled(pts, k):
    return [(x * k, y * k) for x, y in pts]


def fit(pts, w=86, h=96):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(w / (max(xs) - min(xs)), h / (max(ys) - min(ys)))


def shape_cv(pts, k=1.0, fill=FILL):
    cv = Canvas()
    cv.poly(scaled(pts, k), fill)
    return cv


# ------------------------------------------------------------ composite 2D shapes (E1.2)
def composite(parts, outline):
    tot = 0
    for pts, kind in parts:
        assert classify(pts) == kind, (kind, classify(pts))
        tot += abs(area(pts))
    assert abs(tot - abs(area(outline))) < 1e-6, (tot, area(outline))
    xs, ys = [p[0] for p in outline], [p[1] for p in outline]
    for pts, _ in parts:
        for x, y in pts:
            assert min(xs) - 1e-6 <= x <= max(xs) + 1e-6 and min(ys) - 1e-6 <= y <= max(ys) + 1e-6
    return {"parts": parts, "outline": outline}


PART_FILL = {"triangle": BASE, "square": FILL, "rectangle": SIDE, "trapezoid": TOP3, "hexagon": "#f3d27a"}


def comp_cv(c, k=1.0):
    cv = Canvas()
    for pts, kind in c["parts"]:
        cv.poly(scaled(pts, k), PART_FILL[kind])
    return cv


def parts_count(c):
    out = {}
    for _, k in c["parts"]:
        out[k] = out.get(k, 0) + 1
    return out


_s = 60.0
_h = _s * math.sqrt(3) / 2
C_HOUSE = composite([(R(0, 50, 80, 130), "square"), ([(0, 50), (80, 50), (40, 8)], "triangle")],
                    [(0, 130), (0, 50), (40, 8), (80, 50), (80, 130)])
C_ARROW = composite([(R(0, 30, 90, 60), "rectangle"), ([(90, 0), (140, 45), (90, 90)], "triangle")],
                    [(0, 30), (90, 30), (90, 0), (140, 45), (90, 90), (90, 60), (0, 60)])
C_TREE = composite([([(0, 70), (100, 70), (50, 0)], "triangle"), (R(40, 70, 60, 115), "rectangle")],
                   [(0, 70), (50, 0), (100, 70), (60, 70), (60, 115), (40, 115), (40, 70)])
_hx = regular(6, 60, 0)
C_HEX6 = composite([([(0, 0), _hx[i], _hx[(i + 1) % 6]], "triangle") for i in range(6)], _hx)
C_HEX2 = composite([(_hx[0:4], "trapezoid"), (_hx[3:6] + [_hx[0]], "trapezoid")], _hx)
C_TRAP3 = composite([([(0, _h), (_s, _h), (_s / 2, 0)], "triangle"), ([(_s / 2, 0), (_s, _h), (1.5 * _s, 0)], "triangle"),
                     ([(_s, _h), (2 * _s, _h), (1.5 * _s, 0)], "triangle")],
                    [(0, _h), (2 * _s, _h), (1.5 * _s, 0), (_s / 2, 0)])
C_2SQ = composite([(R(0, 0, 60, 60), "square"), (R(60, 0, 120, 60), "square")], R(0, 0, 120, 60))
C_SQDIAG = composite([([(0, 0), (90, 0), (90, 90)], "triangle"), ([(0, 0), (90, 90), (0, 90)], "triangle")], R(0, 0, 90, 90))
C_L = composite([(R(0, 0, 40, 110), "rectangle"), (R(40, 70, 110, 110), "rectangle")],
                [(0, 0), (40, 0), (40, 70), (110, 70), (110, 110), (0, 110)])
C_ROCKET = composite([(R(30, 40, 70, 140), "rectangle"), ([(30, 40), (70, 40), (50, 0)], "triangle"),
                      ([(30, 105), (30, 140), (10, 140)], "triangle"), ([(70, 105), (90, 140), (70, 140)], "triangle")],
                     [(50, 0), (70, 40), (70, 105), (90, 140), (10, 140), (30, 105), (30, 40)])
C_BOAT = composite([([(0, 70), (140, 70), (115, 100), (25, 100)], "trapezoid"), ([(70, 0), (70, 70), (125, 70)], "triangle")],
                   [(0, 70), (70, 70), (70, 0), (125, 70), (140, 70), (115, 100), (25, 100)])
assert sides(C_HOUSE["outline"]) == 5 and classify(C_HOUSE["outline"]) == "pentagon"
assert classify(C_2SQ["outline"]) == "rectangle" and classify(C_TRAP3["outline"]) == "trapezoid"
assert classify(C_HEX2["outline"]) == "hexagon" and classify(C_HEX6["outline"]) == "hexagon"
assert sides(C_ARROW["outline"]) == 7


# ------------------------------------------------------------ symmetry (E1.3)
def _q(p):
    return (int(round(p[0] * 100)), int(round(p[1] * 100)))


def refl(p, c, a):
    d = (math.cos(math.radians(a)), math.sin(math.radians(a)))
    v = (p[0] - c[0], p[1] - c[1])
    t = v[0] * d[0] + v[1] * d[1]
    return (2 * (c[0] + d[0] * t) - p[0], 2 * (c[1] + d[1] * t) - p[1])


def edge_set(pts):
    n = len(pts)
    return {frozenset((_q(pts[i]), _q(pts[(i + 1) % n]))) for i in range(n)}


def is_axis(pts, c, a):
    """True when reflecting every edge across the line through c at angle a (degrees) gives the same edges."""
    pts = simplify(pts)
    return edge_set([refl(p, c, a) for p in pts]) == edge_set(pts)


def centre(pts):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)


def count_axes(pts):
    """Lines of symmetry: any line of symmetry passes through the centre of the vertices (tested every 0.5 degrees)."""
    c = (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
    return sum(1 for i in range(360) if is_axis(pts, c, i * 0.5))


def axis_cv(pts, c, a, k=1.0):
    """The shape with a dashed red line through c at angle a, long enough to cross the whole shape."""
    P = scaled(pts, k)
    c = (c[0] * k, c[1] * k)
    d = (math.cos(math.radians(a)), math.sin(math.radians(a)))
    ts = [(x - c[0]) * d[0] + (y - c[1]) * d[1] for x, y in P]
    t0, t1 = min(ts) - 12, max(ts) + 12
    cv = Canvas()
    cv.poly(P, FILL)
    cv.line((c[0] + d[0] * t0, c[1] + d[1] * t0), (c[0] + d[0] * t1, c[1] + d[1] * t1), dashed=True, sw=2.6, col=RED, dash="8 5")
    return cv


S_RECT = R(0, 0, 140, 80)
S_SQ = R(0, 0, 90, 90)
S_HOUSE = [(0, 45), (45, 0), (90, 45), (90, 110), (0, 110)]
S_PARA = [(30, 0), (150, 0), (120, 80), (0, 80)]
S_ARROW = C_ARROW["outline"]
S_RTRAP = [(0, 80), (150, 80), (80, 0), (0, 0)]
S_KITE = [(50, 0), (100, 40), (50, 130), (0, 40)]
S_LSHAPE = [(0, 0), (45, 0), (45, 70), (110, 70), (110, 115), (0, 115)]
S_TRI3 = regular(3, 55, -90)
assert count_axes(S_SQ) == 4 and count_axes(S_RECT) == 2 and count_axes(S_TRI3) == 3
assert count_axes(S_PARA) == 0 and count_axes(S_LSHAPE) == 0 and count_axes(S_KITE) == 1


def diag_angle(pts):
    return math.degrees(math.atan2(pts[2][1] - pts[0][1], pts[2][0] - pts[0][0]))


# every dashed line used: (shape, centre, angle)
AX = {
    "rect_diag": (S_RECT, centre(S_RECT), diag_angle(S_RECT)),
    "rect_h": (S_RECT, centre(S_RECT), 0),
    "rect_off": (S_RECT, (50, 40), 90),
    "sq_diag": (S_SQ, centre(S_SQ), 45),
    "house_v": (S_HOUSE, centre(S_HOUSE), 90),
    "para_v": (S_PARA, centre(S_PARA), 90),
    "arrow_h": (S_ARROW, (70, 45), 0),
    "rtrap_h": (S_RTRAP, centre(S_RTRAP), 0),
    "rtrap_v": (S_RTRAP, centre(S_RTRAP), 90),
    "kite_h": (S_KITE, (50, 65), 0),
    "l_diag": (S_LSHAPE, centre(S_LSHAPE), 45),
}
AXIS_OK = {k: is_axis(*v) for k, v in AX.items()}
assert AXIS_OK == {"rect_diag": False, "rect_h": True, "rect_off": False, "sq_diag": True, "house_v": True,
                   "para_v": False, "arrow_h": True, "rtrap_h": False, "rtrap_v": False, "kite_h": False, "l_diag": False}, AXIS_OK


def ax_cv(key, k=1.0):
    pts, c, a = AX[key]
    return axis_cv(pts, c, a, k)


def ax_fit(key, w=90, h=106):
    """The largest picture (scale at most 0.6) that fits one cell of the A-D grid."""
    k = 0.6
    while True:
        cv = ax_cv(key, k)
        if cv.size()[0] <= w and cv.size()[1] <= h:
            return cv
        k *= 0.97


def mirror_grid_svg(cols=8, rows=5, line_at=4, dot=(1, 2), cell=26):
    """Square grid with a dashed mirror line on a grid line and one dot on a grid point."""
    pad = 12
    W, H = cols * cell + 2 * pad, rows * cell + 2 * pad + 8
    s = []
    for i in range(cols + 1):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                 % (pad + i * cell, pad, pad + i * cell, pad + rows * cell, THIN))
    for j in range(rows + 1):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                 % (pad, pad + j * cell, pad + cols * cell, pad + j * cell, THIN))
    x = pad + line_at * cell
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3' stroke-dasharray='8 5'/>"
             % (x, pad - 6, x, pad + rows * cell + 6, RED))
    s.append("<circle cx='%d' cy='%d' r='7' fill='%s' stroke='%s' stroke-width='2'/>"
             % (pad + dot[0] * cell, pad + dot[1] * cell, FILL, GREEN))
    return svg_wrap(W, H, "".join(s), "a square grid with a dashed mirror line and a dot")


# ------------------------------------------------------------ set 1: name 3D objects
WRONG3 = {CUBE: ["square", SP, TP], RP: [CUBE, "rectangle", TP], TP: [TBP, RP, "triangle"],
          SP: [TP, CONE, "square"], TBP: [TP, SP, "triangle"], CYL: ["circle", CONE, RP], CONE: [CYL, "triangle", SP]}
E3 = {
    CUBE: "It has 6 faces and they are all squares of the same size, so it is a cube.",
    RP: "It has 6 rectangle faces and they are not all squares, so it is a rectangular prism.",
    TP: "It has the same triangle at each end, joined by 3 rectangles, so it is a triangular prism. A prism does not come to a point.",
    SP: "It has a square base and 4 triangle faces that meet at a point, so it is a square-based pyramid.",
    TBP: "It has 4 triangle faces. It sits on a triangle base and the other 3 triangles meet at a point, so it is a triangle-based pyramid.",
    CYL: "It has 2 flat circle faces and a curved surface, so it is a cylinder. A circle is only a flat 2D shape.",
    CONE: "It has 1 flat circle face and a curved surface that comes to a point, so it is a cone.",
}
TURN3 = {"cube_turned": " It is turned, but it is still a cube.",
         "rp_tall": " It is standing on its end, but it is still a rectangular prism.",
         "rp_turned": " It is turned, but it is still a rectangular prism.",
         "tp_end": " It is turned so you see a triangle end at the front.",
         "tp_standing": " It is standing on a triangle face, but it is still a triangular prism.",
         "sp_turned": " It is turned, but it is still a square-based pyramid.",
         "tbp_turned": " It is turned, but it is still a triangle-based pyramid.",
         "cyl_lying": " It is lying on its side, but it is still a cylinder.",
         "cone_down": " It is upside down, but it is still a cone.",
         "cone_side": " It is lying on its side, but it is still a cone."}


def set_name(rnd, pos):
    its = []
    asks = ["What is the name of this 3D object?", "Name this 3D object.", "What is this object called?"]
    keys = ["cube", "cube_turned", "rp_flat", "rp_tall", "rp_turned", "tp_lying", "tp_standing", "tp_end", "sp", "sp_turned",
            "tbp", "tbp_turned", "cyl", "cyl_lying", "cone", "cone_down", "cone_side"]
    for i, k in enumerate(keys):
        kind = KIND[k]
        its.append(mcq(fig(pic3d(k).svg("a 3D object")) + asks[i % 3], kind, WRONG3[kind], E3[kind] + TURN3.get(k, "")))
    for kind, right, others, why in [
            (TBP, "tbp", ["sp", "tp_lying", "cone"], "it has 4 triangle faces and comes to a point. The others have a square base, no point, or a curved surface"),
            (RP, "rp_tall", ["cube", "tp_lying", "cyl"], "it has 6 rectangle faces that are not all squares. It is standing on its end"),
            (CONE, "cone_side", ["cyl_lying", "sp", "tp_end"], "it has 1 circle face and comes to a point. It is lying on its side"),
    ]:
        p = pos.next()
        cells = [pic3d(k, 0.62) for k in others]
        cells.insert(p, pic3d(right, 0.62))
        its.append(mcq_fixed(fig(grid_svg(cells, "four 3D objects labelled A to D")) + "Which picture shows %s %s?" % (art(kind), kind),
                             list("ABCD"), "ABCD"[p], "%s is %s %s: %s." % ("ABCD"[p], art(kind), kind, why)))
    assert len(its) == 20, len(its)
    return {"title": "Name 3D objects: cubes, prisms, pyramids, cylinders and cones", "items": its}


# ------------------------------------------------------------ set 2: faces, edges, vertices and angles
def set_fev(rnd, P):
    its = []
    its.append(mcq("A flat surface of a 3D object is called a …", "face", ["edge", "vertex", "corner"],
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
                       ("sp", "faces"), ("sp", "edges"), ("sp_turned", "vertices"), ("tbp", "faces")]:
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
                   "A cylinder has no corners, so it has 0 vertices. Its 2 edges are curved circles, not corners. "
                   "In a drawing it can look like it has 4 corners, but it does not."))
    its.append(mcq(fig(cone_cv().svg("a cone")) + "How many vertices does a cone have?", 1, [0, 2, 3],
                   "A cone has 1 vertex: the point at the top. Its circle edge is curved and has no corners."))
    its.append(mcq("Every face of a cube is a square. How many right angles does one face have?", 4, [8, 2, 3],
                   "A square has 4 square corners, so it has 4 right angles. 8 is the number of vertices of the whole cube."))
    its.append(mcq("Which object has right angles at every corner of every face?", RP, [SP, TBP, TP],
                   "All 6 faces of a rectangular prism are rectangles, and every rectangle has 4 right angles. "
                   "Pyramids and triangular prisms have triangle faces, and a triangle can never have a right angle at every corner."))
    n, he, his = P.next()
    its.append(mcq("%s says a cube has 8 edges. %s is wrong. What did %s count?" % (n, he.capitalize(), he), "the vertices",
                   ["the faces", "the edges at the front", "the hidden faces"],
                   "A cube has 8 vertices (corners) and 12 edges. %s counted the vertices." % n))
    assert len(its) == 20, len(its)
    return {"title": "Faces, edges, vertices and angles", "items": its}


# ------------------------------------------------------------ set 3: 2D faces of 3D objects, and nets
def set_faces(rnd, P):
    its = []
    its.append(mcq("What shape is each face of a cube?", "a square", ["a triangle", "a circle", "a cube"],
                   "All 6 faces of a cube are squares of the same size. A cube is the 3D object; its faces are 2D squares."))
    its.append(mcq("Which 2D shapes are the faces of a triangular prism?", "2 triangles and 3 rectangles",
                   ["3 triangles and 2 rectangles", "2 triangles and 2 rectangles", "1 triangle and 4 rectangles"],
                   "A triangular prism has a triangle at each end (2 triangles) and 3 rectangles joining them: 5 faces."))
    its.append(mcq("Which 2D shapes are the faces of a square-based pyramid?", "1 square and 4 triangles",
                   ["4 squares and 1 triangle", "1 square and 3 triangles", "2 squares and 4 triangles"],
                   "A square-based pyramid has 1 square at the bottom and 4 triangles that meet at the top: 5 faces."))
    its.append(mcq("Which 2D shapes are the faces of a triangle-based pyramid?", "4 triangles",
                   ["3 triangles", "1 square and 3 triangles", "3 triangles and 1 rectangle"],
                   "It has 3 triangles that meet at the top and 1 more triangle as the base: 3 + 1 = 4 triangles. Do not forget the base."))
    its.append(mcq("Which 2D shapes are the faces of a rectangular prism like a cereal box?", "6 rectangles",
                   ["4 rectangles", "6 triangles", "4 rectangles and 2 circles"],
                   "A rectangular prism has 6 faces and each one is a rectangle: front and back, top and bottom, and 2 ends."))
    its.append(mcq(fig(cylinder_cv().svg("a cylinder")) + "What shape are the 2 flat faces of a cylinder?", "circles",
                   ["rectangles", "ovals", "spheres"],
                   "The flat faces of a cylinder are circles. In a drawing they look like ovals because we see them from the side."))
    its.append(mcq("What shape is the flat face of a cone?", "a circle", ["a triangle", "a square", "a cone"],
                   "A cone has 1 flat face: a circle. From the side a cone looks like a triangle, but it has no triangle faces."))
    n, he, his = P.next()
    its.append(mcq("%s dips one face of a cube in paint and presses it on paper. What shape does %s print?" % (n, he), "a square",
                   ["a cube", "a triangle", "a circle"],
                   "Every face of a cube is a square, so the print is a square. A print is flat (2D), so it cannot be a cube."))
    n, he, his = P.next()
    its.append(mcq("%s traces around the bottom of a soup can. What shape does %s draw?" % (n, he), "a circle",
                   ["a rectangle", "a cylinder", "a triangle"],
                   "The can is a cylinder and its bottom face is a circle, so the tracing is a circle."))
    its.append(mcq("You press each face of an object in paint. Which object can print a triangle?", TP,
                   [CUBE, CYL, RP],
                   "A triangular prism has a triangle face at each end. A cube, a cylinder and a rectangular prism have no triangle faces."))
    its.append(mcq("Which object can print 1 square and 4 triangles?", SP, [CUBE, CONE, CYL],
                   "A square-based pyramid has 1 square face and 4 triangle faces."))
    its.append(mcq("How many square faces does a square-based pyramid have?", 1, [4, 5, 0],
                   "Only the base is a square: 1 square face. The other 4 faces are triangles."))
    its.append(mcq("How many triangle faces does a triangular prism have?", 2, [3, 5, 1],
                   "A triangular prism has 1 triangle at each end: 2 triangles. Its name says “triangle”, but its other 3 faces are rectangles."))
    its.append(mcq("How many rectangle faces does a triangular prism have?", 3, [2, 5, 4],
                   "The 3 faces that join the 2 triangle ends are rectangles: 3 rectangles."))
    its.append(mcq("A net is a flat shape you can fold to make a 3D object. How many squares are in a net of a cube?", 6, [4, 8, 12],
                   "A cube has 6 faces, so its net has 6 squares, one for each face. 8 is the number of vertices."))
    for cv, name, right, wrong, e in [
            (net_cube(), "a net made of 6 squares", CUBE, ["square", RP, SP],
             "6 squares of the same size fold up into a cube: 1 square for each face."),
            (net_sp(), "a net made of 1 square and 4 triangles", SP, [TP, TBP, "square"],
             "The square is the base. The 4 triangles fold up and meet at a point: a square-based pyramid."),
            (net_tp(), "a net made of 3 rectangles and 2 triangles", TP, [SP, RP, TBP],
             "The 3 rectangles fold into a tube and the 2 triangles close the ends: a triangular prism."),
            (net_rp(), "a net made of 6 rectangles", RP, [CUBE, TP, "rectangle"],
             "6 rectangles that are not all squares fold into a rectangular prism, like a box."),
            (net_cyl(), "a net made of a rectangle and 2 circles", CYL, [CONE, "rectangle", RP],
             "The rectangle rolls into a tube (the curved surface) and the 2 circles close the ends: a cylinder."),
    ]:
        its.append(mcq(fig(cv.svg(name)) + "This net is folded up. Which 3D object does it make?", right, wrong, e))
    assert len(its) == 20, len(its)
    return {"title": "2D faces of 3D objects, and nets", "items": its}


# ------------------------------------------------------------ set 4: compose and decompose
def set_compose(rnd, pos, P):
    its = []
    q2 = lambda c, t: fig(comp_cv(c).svg("a shape made of smaller shapes")) + t

    def add(c, t, right, wrong, e, want=None):
        if want is not None:
            assert parts_count(c) == want, (parts_count(c), want)
        its.append(mcq(q2(c, t), right, wrong, e))

    add(C_HOUSE, "Which two shapes make this house?", "a square and a triangle",
        ["a pentagon and a triangle", "a square and 2 triangles", "a rectangle and a circle"],
        "The wall is a square (4 equal sides) and the roof is a triangle (3 sides).", {"square": 1, "triangle": 1})
    add(C_HOUSE, "How many sides does the outline of the whole house have?", 5, [7, 6, 4],
        "Go around the outside: 2 walls, the floor and 2 roof sides = 5 sides, so the outline is a pentagon. "
        "Do not add 4 + 3 = 7: the line where the roof meets the wall is inside.")
    add(C_ARROW, "Which two shapes make this arrow?", "a rectangle and a triangle",
        ["2 triangles", "a pentagon and a rectangle", "a square and a circle"],
        "The long part is a rectangle and the point is a triangle.", {"rectangle": 1, "triangle": 1})
    add(C_TREE, "Which two shapes make this tree?", "a triangle and a rectangle",
        ["a triangle and a trapezoid", "2 triangles", "a pentagon and a square"],
        "The top of the tree is a triangle and the trunk is a thin rectangle.", {"triangle": 1, "rectangle": 1})
    add(C_HEX6, "How many triangles make this hexagon?", 6, [3, 4, 8],
        "Count the triangles around the centre: 6. A hexagon has 6 sides, and each side belongs to one triangle.", {"triangle": 6})
    add(C_HEX2, "Which shapes make this hexagon?", "2 trapezoids", ["2 triangles", "2 rectangles", "2 pentagons"],
        "The line cuts the hexagon into 2 pieces. Each piece has 4 sides and 1 pair of parallel sides, so each is a trapezoid.",
        {"trapezoid": 2})
    add(C_TRAP3, "Which shapes make this trapezoid?", "3 triangles", ["2 triangles", "4 triangles", "3 squares"],
        "Count the pieces: 3 triangles. With pattern blocks, 3 triangle blocks make 1 trapezoid block.", {"triangle": 3})
    add(C_2SQ, "Which shapes make this rectangle?", "2 squares", ["4 squares", "2 triangles", "a square and a triangle"],
        "The line in the middle cuts the rectangle into 2 equal squares.", {"square": 2})
    add(C_SQDIAG, "Which shapes make this square?", "2 triangles", ["2 rectangles", "4 triangles", "2 squares"],
        "The line goes from one corner to the opposite corner. It cuts the square into 2 triangles.", {"triangle": 2})
    add(C_L, "Which shapes make this L shape?", "2 rectangles", ["3 squares", "a rectangle and a triangle", "2 squares"],
        "A tall rectangle and a flat rectangle make the L. Neither piece has 4 equal sides, so they are not squares.",
        {"rectangle": 2})
    add(C_ROCKET, "Which shapes make this rocket?", "1 rectangle and 3 triangles",
        ["1 rectangle and 2 triangles", "1 square and 3 triangles", "2 rectangles and 3 triangles"],
        "The body is a rectangle. The nose is a triangle and there is a triangle fin on each side: 1 + 2 = 3 triangles.",
        {"rectangle": 1, "triangle": 3})
    for cv, name, lead, right, wrong, e in [
            (silo_cv(), "a farm silo", "This farm silo is made of two 3D objects. Which two?", "a cylinder and a cone",
             ["a rectangle and a triangle", "a cylinder and a square-based pyramid", "a cone and a cube"],
             "The tall part has 2 circle faces and a curved side: a cylinder. The roof has a circle base and a point: a cone. "
             "A rectangle and a triangle are flat 2D shapes."),
            (house3d_cv(), "a model house", "This model house is made of two 3D objects. Which two?",
             "a rectangular prism and a triangular prism",
             ["a rectangular prism and a square-based pyramid", "a rectangle and a triangle", "a cube and a cone"],
             "The bottom has 6 rectangle faces: a rectangular prism. The roof has a triangle at each end and does not come to a point: a triangular prism."),
            (tower_cv(), "a tower", "This tower is made of two 3D objects. Which two?", "a cube and a square-based pyramid",
             ["a cube and a triangular prism", "a square and a triangle", "a cube and a cone"],
             "The bottom has 6 square faces: a cube. The top has 4 triangle faces that meet at a point: a square-based pyramid. A cone has a circle base."),
    ]:
        its.append(mcq(fig(cv.svg(name)) + lead, right, wrong, e))
    its.append(mcq("You put 2 squares of the same size side by side. Which shape do you make?", "a rectangle",
                   ["a bigger square", "an octagon", "a hexagon"],
                   "2 squares side by side make a rectangle twice as long as it is wide. It has 4 sides, not 4 + 4 = 8."))
    n, he, his = P.next()
    its.append(mcq("%s cuts a rectangle from one corner to the opposite corner. What two shapes does %s get?" % (n, he), "2 triangles",
                   ["2 rectangles", "2 squares", "a triangle and a trapezoid"],
                   "A cut from corner to corner makes 2 triangles. A cut across the middle would make 2 rectangles."))
    its.append(mcq("You put 2 cubes side by side and glue them together. Which 3D object do you make?", RP,
                   ["a bigger cube", "rectangle", TP],
                   "The new object has 6 faces: 2 squares at the ends and 4 long rectangles. It is a rectangular prism, not a cube."))
    n, he, his = P.next()
    its.append(mcq("%s cuts a cube of cheese straight down the middle into 2 equal halves. What 2 objects does %s get?"
                   % (n, he), "2 rectangular prisms", ["2 cubes", "2 triangular prisms", "2 square-based pyramids"],
                   "Each half has 6 faces: 2 squares and 4 rectangles that are not squares. So each half is a rectangular prism. Half a cube is not a cube."))
    n, he, his = P.next()
    its.append(mcq("%s cuts a cube of cheese straight down, from one corner of the top to the opposite corner. What 2 objects does %s get?"
                   % (n, he), "2 triangular prisms", ["2 rectangular prisms", "2 triangle-based pyramids", "2 cubes"],
                   "The cut makes a triangle at the top and a triangle at the bottom of each piece, joined by rectangles. "
                   "Each piece is a triangular prism. It does not come to a point, so it is not a pyramid."))
    p = pos.next()
    others = [C_ARROW, C_BOAT, C_SQDIAG]
    cells = [comp_cv(c, min(0.6, fit(c["outline"]))) for c in others]
    cells.insert(p, comp_cv(C_HOUSE, min(0.6, fit(C_HOUSE["outline"]))))
    its.append(mcq_fixed(fig(grid_svg(cells, "four shapes made of smaller shapes labelled A to D")) + "Which shape is made from a square and a triangle?",
                         list("ABCD"), "ABCD"[p],
                         "%s is a square with a triangle on top. The others are a rectangle and a triangle, a trapezoid and a triangle, and 2 triangles."
                         % "ABCD"[p]))
    assert len(its) == 20, len(its)
    return {"title": "Build and take apart: shapes and objects", "items": its}


# ------------------------------------------------------------ set 5: matching halves (line symmetry)
YES = "Yes, the two halves match."
NO = "No, the two halves do not match."
CUTS = "Yes, it cuts the shape into 2 parts."
UPDOWN = "No, a line of symmetry must go up and down."


def set_symmetry(rnd, pos, P):
    its = []
    for key, name, why in [
            ("house_v", "a pentagon", "Fold along the line: the left half lands exactly on the right half."),
            ("sq_diag", "a square", "Fold the square from corner to corner: the 2 triangles match exactly. A line of symmetry can go any way, even on a slant."),
            ("arrow_h", "an arrow", "Fold along the line: the top half lands exactly on the bottom half. Lines of symmetry can go side to side too."),
            ("rect_diag", "a rectangle", "Fold a rectangle from corner to corner and the corners stick out: the halves do not match. "
                                         "The line cuts it into 2 triangles of the same size, but they do not match when you fold."),
            ("para_v", "a parallelogram", "Fold along the line: the slanted sides go opposite ways, so the halves do not match."),
            ("rtrap_h", "a trapezoid", "The top half is narrower than the bottom half, so the halves do not match when you fold."),
    ]:
        ok = AXIS_OK[key]
        right = YES if ok else NO
        wrong = [NO if ok else YES, CUTS, UPDOWN]
        if key == "house_v":
            wrong = [NO, CUTS, "No, a line of symmetry must go side to side."]
        q = fig(ax_cv(key).svg("%s with a dashed line" % name)) + "Is the dashed line a line of symmetry?"
        its.append(mcq(q, right, wrong, why))
    for right, others, why in [
            ("house_v", ["rect_diag", "para_v", "rtrap_v"],
             "shows a line of symmetry: the 2 halves match when you fold. The other lines cut the shape in two, but the halves do not match."),
            ("rect_h", ["kite_h", "rect_off", "l_diag"],
             "shows a line of symmetry: the rectangle is folded exactly in half. The other lines make halves that do not match."),
    ]:
        p = pos.next()
        cells = [ax_fit(k) for k in others]
        cells.insert(p, ax_fit(right))
        assert AXIS_OK[right] and not any(AXIS_OK[k] for k in others)
        its.append(mcq_fixed(fig(grid_svg(cells, "four shapes with dashed lines labelled A to D")) + "Which picture shows a line of symmetry?",
                             list("ABCD"), "ABCD"[p], "%s %s" % ("ABCD"[p], why)))
    its.append(mcq(fig(shape_cv(S_SQ).svg("a square")) + "How many lines of symmetry does a square have?", count_axes(S_SQ), [2, 8, 1],
                   "A square has 4 lines of symmetry: 1 up and down, 1 side to side and 2 from corner to corner. Do not forget the 2 slanted lines."))
    its.append(mcq(fig(shape_cv(S_TRI3).svg("a triangle with 3 equal sides")) + "This triangle has 3 equal sides. How many lines of symmetry does it have?",
                   count_axes(S_TRI3), [1, 6, 0],
                   "Each line goes from a corner to the middle of the opposite side. There are 3 corners, so there are 3 lines of symmetry."))
    its.append(mcq("Which capital letter has matching halves when you fold it down the middle, from top to bottom?", "T",
                   ["F", "G", "J"],
                   "Fold T down the middle: the left half matches the right half. F, G and J do not have matching halves."))
    its.append(mcq("Which capital letter has a line of symmetry going across, from side to side?", "E",
                   ["A", "N", "R"],
                   "Fold E across the middle: the top half matches the bottom half. A has a line going up and down, not across. N and R have none."))
    its.append(mcq(fig(mirror_grid_svg()) + "The dashed line is a mirror line. The dot is 3 squares to the left of the line. "
                   "Where is the matching dot?", "3 squares to the right of the line", ["6 squares to the right of the line",
                   "1 square to the right of the line", "3 squares below the dot"],
                   "A matching point is the same distance from the mirror line, on the other side: 3 squares to the left, so 3 squares to the right. "
                   "1 comes from counting from the edge of the grid."))
    its.append(mcq("Think of the flag of Canada. How many lines of symmetry does it have?", 1, [2, 4, 0],
                   "Fold the flag down the middle: the red bands and the two halves of the maple leaf match. "
                   "Fold it across and the leaf does not match upside down, so there is only 1 line of symmetry."))
    n, he, his = P.next()
    its.append(mcq("%s cuts a paper snowflake with 6 arms that are all the same. How many lines of symmetry does it have?" % n, 6, [3, 2, 12],
                   "A line of symmetry can go through each arm. A snowflake with 6 matching arms has 6 lines of symmetry."))
    its.append(mcq("A stop sign is a shape with 8 equal sides. Forget the words on it. How many lines of symmetry does the shape have?",
                   8, [4, 2, 1],
                   "A shape with 8 equal sides and 8 equal angles has 8 lines of symmetry: 4 through opposite corners and 4 through the middles of opposite sides."))
    its.append(mcq("Look at the lines painted on a soccer field from above. How many lines of symmetry do they have?", 2, [1, 4, 0],
                   "The two halves of the field match across the halfway line, and the left and right sides match along the long middle line: 2 lines."))
    n, he, his = P.next()
    its.append(mcq("%s folds a paper in half and cuts half a heart along the fold. %s opens the paper. Where is the line of symmetry of the heart?"
                   % (n, he.capitalize()), "along the fold", ["along the cut edge", "across the middle, from side to side", "there is none"],
                   "The fold is the line of symmetry. The cut makes the same edge on both halves, so the halves match along the fold."))
    n, he, his = P.next()
    its.append(mcq("%s draws the left half of a maple leaf next to a mirror line. How should the right half look?" % n,
                   "the same shape, flipped like a mirror", ["the same shape, slid over without flipping",
                                                             "the same shape, upside down", "a bigger copy of the left half"],
                   "Matching halves are mirror images. The right half is the left half flipped over the line, not slid across."))
    n, he, his = P.next()
    its.append(mcq("%s has a rectangle card that is not a square. In how many ways can %s fold it so the halves match exactly?" % (n, he),
                   count_axes(S_RECT), [4, 1, 0],
                   "%s can fold it top to bottom or side to side: 2 ways. A fold from corner to corner does not match on a rectangle." % n))
    assert len(its) == 20, len(its)
    return {"title": "Matching halves: line symmetry", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    flat = row_svg([solid_cv("cube", 40), solid_cv("rp_flat", 40), solid_cv("tp_lying", 42), solid_cv("sp", 42), solid_cv("tbp", 42)],
                   ["cube", "rectangular prism", "triangular prism", "square-based pyramid", "triangle-based pyramid"],
                   "cube, rectangular prism, triangular prism, square-based pyramid and triangle-based pyramid", gap=14, fs=14)
    curved = row_svg([cylinder_cv(0.85), cone_cv(0.85)], ["cylinder", "cone"], "a cylinder and a cone", gap=50, fs=14)
    nets = row_svg([net_cube(26), net_sp(36, 30), net_tp(30, 48)], ["cube", "square-based pyramid", "triangular prism"],
                   "nets of a cube, a square-based pyramid and a triangular prism", gap=30, fs=14)
    comps = row_svg([comp_cv(C_HOUSE, 0.75), comp_cv(C_HEX6, 0.7), silo_cv(s=0.75), house3d_cv(36)],
                    ["square + triangle", "6 triangles", "cylinder + cone", "2 prisms"],
                    "shapes and objects made of smaller shapes and objects", gap=22, fs=14)
    sym = row_svg([ax_cv("house_v", 0.8), ax_cv("sq_diag", 0.8), ax_cv("rect_diag", 0.6)],
                  ["matching halves", "matching halves", "not matching"],
                  "two lines of symmetry and one line that is not a line of symmetry", gap=30, fs=14)
    return (
        "<h2>3D objects</h2>"
        "<p>A 3D object is solid, like a box or a can. A <b>face</b> is a flat surface. An <b>edge</b> is where two faces meet. "
        "A <b>vertex</b> is a corner where edges meet. Two or more are called <b>vertices</b>. Dashed lines show edges at the back.</p>"
        "<figure class='sn-fig'>" + flat +
        "<figcaption>A prism has the same shape at both ends. A pyramid comes to a point.</figcaption></figure>"
        "<figure class='sn-fig'>" + curved +
        "<figcaption>A cylinder and a cone have a curved surface, so they can roll.</figcaption></figure>" +
        table(["Object", "Faces", "Edges", "Vertices", "Example"], [
            ["Cube", "6 squares", "12", "8", "a number cube"],
            ["Rectangular prism", "6 rectangles", "12", "8", "a cereal box"],
            ["Triangular prism", "2 triangles, 3 rectangles", "9", "6", "a tent"],
            ["Square-based pyramid", "1 square, 4 triangles", "8", "5", "a pyramid in Egypt"],
            ["Triangle-based pyramid", "4 triangles", "6", "4", "a 4-sided game die"],
            ["Cylinder", "2 circles and 1 curved surface", "2 curved", "0", "a soup can"],
            ["Cone", "1 circle and 1 curved surface", "1 curved", "1 (the point)", "a pylon"]]) +
        "<p>Every face of a cube or a rectangular prism has 4 right angles (square corners). An object keeps its name when it is turned.</p>" +
        ex("Example 1", "How many faces does a cube have?",
           "In a picture you can see 3 faces. There are 3 more at the back, on the side and underneath. 3 + 3 = 6.", "6 faces") +
        "<h2>Faces and nets</h2>"
        "<p>Each face of a 3D object is a 2D shape. A <b>net</b> is a flat pattern of these faces. Fold it up and you get the object.</p>"
        "<figure class='sn-fig'>" + nets + "</figure>" +
        ex("Example 2", "Which 2D shapes are the faces of a triangular prism?",
           "There is a triangle at each end. 3 rectangles join the ends.", "2 triangles and 3 rectangles") +
        "<h2>Build and take apart</h2>"
        "<p>Many shapes and objects are made of smaller ones. Look for the lines inside to find the parts. "
        "To name the whole outline, count only the sides around the outside.</p>"
        "<figure class='sn-fig'>" + comps + "</figure>" +
        ex("Example 3", "A house is a square with a triangle roof. How many sides does the whole outline have?",
           "Go around the outside: 2 walls, the floor and 2 roof sides. The line between the roof and the wall is inside.",
           "5 sides, so the outline is a pentagon") +
        "<h2>Matching halves</h2>"
        "<p>A <b>line of symmetry</b> cuts a shape into 2 matching halves. If you fold along the line, one half lands exactly on the other. "
        "The line can go up and down, side to side or on a slant.</p>"
        "<figure class='sn-fig'>" + sym +
        "<figcaption>Fold a rectangle from corner to corner and the corners stick out, so that line is not a line of symmetry.</figcaption></figure>" +
        ex("Example 4", "How many lines of symmetry does a rectangle (not a square) have?",
           "Fold it top to bottom: the halves match. Fold it side to side: they match. Fold it corner to corner: they do not.",
           "2 lines") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Mixing up a prism and a pyramid", "A pyramid comes to a point; a prism has the same shape at both ends"],
            ["Counting only the faces you can see", "Remember the faces at the back and underneath"],
            ["Giving a cylinder vertices", "A cylinder has no corners: 0 vertices. Its edges are curved"],
            ["Mixing up edges and vertices", "Edges are lines; vertices are corners"],
            ["Calling a can a circle", "A can is a cylinder (3D); its flat faces are circles (2D)"],
            ["Any line that cuts a shape in two is a line of symmetry", "Fold it: the halves must match exactly"],
        ])
    )


FAQ = [
    {"q": "What 3D objects do Grade 3 students learn in Ontario?",
     "a": "Cubes, prisms, pyramids, cylinders and cones. Students sort them by comparing their faces, edges, vertices and angles (Spatial Sense, expectation E1.1)."},
    {"q": "How many faces, edges and vertices does a cylinder have?",
     "a": "A cylinder has 2 flat circle faces and 1 curved surface, 2 curved edges and 0 vertices. It has no corners."},
    {"q": "Are shapes and symmetry on the Grade 3 EQAO math test?",
     "a": "The Grade 3 EQAO math assessment is based on the Ontario curriculum, which includes Spatial Sense. Practising 3D objects, nets and matching halves helps students get ready."},
    {"q": "How can I help my child learn 3D objects and symmetry at home?",
     "a": "Hunt for objects in the kitchen, like a soup can (cylinder) or a cereal box (rectangular prism), and count their faces, edges and vertices. Fold paper cut-outs to see if the halves match."},
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
    rnd = random.Random(33814)
    P = People(rnd)
    pos = Pos(rnd)
    sets = [set_name(rnd, pos), set_fev(rnd, P), set_faces(rnd, P), set_compose(rnd, pos, P), set_symmetry(rnd, pos, P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-3", "slug": "2d-shapes-and-3d-objects", "sort": 14,
        "updated": UPDATED, "pdf_url": "",
        "title": "2D Shapes and 3D Objects: Faces, Edges, Vertices and Symmetry",
        "seo_title": "Grade 3 Math 2D Shapes and 3D Objects Worksheets: Prisms, Pyramids, Nets and Symmetry (Free, Answer Key)",
        "short_title": "2D shapes and 3D objects",
        "domain": "Spatial Sense",
        "standard_code": "Grade 3: E1.1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Sort and identify cubes, prisms, pyramids, cylinders, and cones by comparing their faces, edges, vertices, and angles",
        "meta_desc": "Free Grade 3 math worksheets on 2D shapes and 3D objects for the Ontario curriculum: name cubes, prisms, pyramids, cylinders and cones, count faces, edges and vertices, match nets, build and take apart shapes, and find lines of symmetry. 100 questions with an answer key, great for EQAO practice.",
        "key_big": "Count faces, edges and vertices to name an object. A pyramid comes to a point; a prism does not.",
        "key_sub": "Count the faces you cannot see too. A cylinder has 0 vertices. A line of symmetry makes 2 halves that match exactly when you fold.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(four 3D objects labelled A to D|four shapes made of smaller shapes labelled A to D|four shapes with dashed lines labelled A to D|a square grid|a net made of 6 rectangles|a net made of a rectangle)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
