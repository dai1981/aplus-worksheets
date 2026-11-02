# -*- coding: utf-8 -*-
"""
Canada (British Columbia) Grade 1 Math: 2D shapes and 3D objects
(BC Mathematics Curriculum, Geometry and measurement: comparison of 2D shapes and 3D objects)
  python3 tools/gen_cabc_math_g1_shapes.py
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.

Grade 1 students name and describe 2D shapes (circle, triangle, square, rectangle, hexagon), sort them by
sides and corners, name 3D objects (cube, sphere, cone, cylinder) and the same objects around us,
tell flat (2D) from solid (3D), and trace the flat faces of 3D objects.
Very short sentences, a picture in almost every question.

Rules kept everywhere (so every answer is right for every definition):
  - a square picture never has "rectangle" as a wrong answer
  - colour, size and turning never change the name
Pictures are drawn from their corner points (checked: right number of sides, no crossing sides,
squares really square) and 3D objects from 3D vertices and faces (V − E + F = 2), with hidden edges dashed.
Wrong answers come from real student mistakes: a turned square called a diamond, a rectangle called a square,
circle vs sphere, square vs cube, triangle vs cone, cylinder vs cone, a cylinder seen from the side called a
rectangle, miscounting the sides of a hexagon, sorting by colour when the rule is sides, calling a face that
looks like an oval an oval, thinking a sphere has a flat face to trace.
Drawing helpers copied from tools/gen_caon_math_g1_shapes.py.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL, SIDE, TOP3 = "#cfe6d6", "#a9d3b6", "#e6f2e9"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
RED = "#d62828"
YEL = "#ffd84d"
FONT = "Arial, Helvetica, sans-serif"
# (fill, line) pairs for flat shapes: colour must never change the name
COLS = [("#cfe6d6", "#006633"), ("#cfe0f3", "#1f5f99"), ("#fbe7a6", "#8a6100"),
        ("#f6cfd8", "#a33b5a"), ("#e2d6f0", "#5b3f8c")]
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]

CUBE, PRISM, PYR, CYL, CONE, SPH = "cube", "prism", "pyramid", "cylinder", "cone", "sphere"


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


class Canvas:
    """Collects shapes (screen coordinates, y down), tracks the bounding box, then writes a tight SVG."""

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

    def line(self, a, b, dashed=False, sw=2.4, col=GREEN, dash="5 4"):
        self.el.append(("l", a, b, dashed, sw, col, dash))
        self.grow(min(a[0], b[0]) - sw, min(a[1], b[1]) - sw, max(a[0], b[0]) + sw, max(a[1], b[1]) + sw)

    def pline(self, pts, dashed=False, sw=2.4, col=GREEN):
        self.el.append(("pl", pts, dashed, sw, col))
        for x, y in pts:
            self.grow(x - sw, y - sw, x + sw, y + sw)

    def text(self, x, y, t, fs=18, col=INK):
        self.el.append(("t", x, y, t, fs, col))
        w = tw(t, fs)
        self.grow(x - w / 2, y - fs * 0.8, x + w / 2, y + fs * 0.25)

    def body(self, ox, oy):
        s = []
        for e in self.el:
            if e[0] == "p":
                _, pts, fill, sw, col, dashed = e
                st = (" stroke='%s' stroke-width='%g' stroke-linejoin='round'%s" % (col, sw, " stroke-dasharray='6 4'" if dashed else "")) if sw else ""
                s.append("<polygon points='%s' fill='%s'%s/>"
                         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in pts), fill, st))
            elif e[0] == "c":
                _, c, r, fill, sw, col = e
                st = " stroke='%s' stroke-width='%g'" % (col, sw) if sw else ""
                s.append("<circle cx='%.1f' cy='%.1f' r='%g' fill='%s'%s/>" % (c[0] - ox, c[1] - oy, r, fill, st))
            elif e[0] == "l":
                _, a, b, dashed, sw, col, dash = e
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g'%s/>"
                         % (a[0] - ox, a[1] - oy, b[0] - ox, b[1] - oy, col, sw,
                            " stroke-dasharray='%s'" % dash if dashed else " stroke-linecap='round'"))
            elif e[0] == "t":
                _, x, y, t, fs, col = e
                s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                         % (x - ox, y - oy, fs, col, t))
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
    """Pictures side by side (centred on one middle line), a caption under each."""
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
        f = min(1.0, aw / w, ah / h)                  # shrink a picture a little if it is too big for its cell
        assert f > 0.8, ("too big for the grid", w, h)
        tx = x0 + 21 + (aw - w * f) / 2
        ty = y0 + 5 + (ah - h * f) / 2
        s.append("<g transform='translate(%.1f,%.1f) scale(%.3f)'>%s</g>" % (tx, ty, f, cv.body(cv.x0, cv.y0)))
        s.append("<text x='%d' y='%d' font-size='18' font-weight='700' fill='%s'>%s</text>" % (x0 + 5, y0 + 22, INK, "ABCD"[k]))
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ 2D shapes
def reg(n, r, start=-90):
    return [(r * math.cos(math.radians(start + 360 * i / n)), r * math.sin(math.radians(start + 360 * i / n))) for i in range(n)]


def tpts(pts, deg=0, s=1.0):
    """Turn the points about their middle and scale them."""
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
    "tri_eq": reg(3, 46),
    "tri_right": [(0, 0), (0, 70), (90, 70)],
    "tri_thin": [(0, 0), (120, 25), (25, 58)],
    "tri_tall": [(0, 90), (30, 0), (60, 90)],
    "square": [(0, 0), (70, 0), (70, 70), (0, 70)],
    "rect": [(0, 0), (110, 0), (110, 55), (0, 55)],
    "rect_long": [(0, 0), (130, 0), (130, 40), (0, 40)],
    "hex": reg(6, 44),
    "hex_flat": reg(6, 44, 0),
    "hex_wide": [(0, 30), (30, 0), (90, 0), (120, 30), (90, 60), (30, 60)],
    "pent": reg(5, 44),
}
KIND2D = {"tri_eq": "triangle", "tri_right": "triangle", "tri_thin": "triangle", "tri_tall": "triangle",
          "square": "square", "rect": "rectangle", "rect_long": "rectangle",
          "hex": "hexagon", "hex_flat": "hexagon", "hex_wide": "hexagon", "pent": "pentagon"}
NSIDES = {"triangle": 3, "square": 4, "rectangle": 4, "hexagon": 6, "pentagon": 5}
for _k, _p in SHAPES2D.items():
    check_poly(_p)
    assert len(_p) == NSIDES[KIND2D[_k]]
    if KIND2D[_k] in ("square", "rectangle"):
        _L = [math.hypot(_p[i][0] - _p[i - 1][0], _p[i][1] - _p[i - 1][1]) for i in range(4)]
        for _i in range(4):                        # right angles
            a, b, c = _p[_i - 1], _p[_i], _p[(_i + 1) % 4]
            assert abs((b[0] - a[0]) * (c[0] - b[0]) + (b[1] - a[1]) * (c[1] - b[1])) < 1e-9
        if KIND2D[_k] == "square":
            assert max(_L) - min(_L) < 1e-9
        else:
            assert max(_L) / min(_L) >= 2              # clearly not a square


def shape2d(key, deg=0, s=1.0, c=0):
    pts = tpts(SHAPES2D[key], deg, s)
    check_poly(pts)
    cv = Canvas()
    cv.poly(pts, COLS[c][0], 3, COLS[c][1])
    return cv


def circle_cv(r=40, c=0):
    cv = Canvas()
    cv.circle((0, 0), r, fill=COLS[c][0], sw=3, col=COLS[c][1])
    return cv


def ellipse(cx, cy, rx, ry, a0, a1, n=40):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def oval_cv(rx=48, ry=28, c=0):
    cv = Canvas()
    cv.poly(ellipse(0, 0, rx, ry, 0, 360, 72)[:-1], COLS[c][0], 3, COLS[c][1])
    return cv


def flat(key, deg=0, s=1.0, c=0):
    """Any flat shape by key: a SHAPES2D key, 'circle' or 'oval'. s scales it."""
    if key == "circle":
        return circle_cv(38 * s, c)
    if key == "oval":
        return oval_cv(48 * s, 28 * s, c)
    return shape2d(key, deg, s, c)


# ------------------------------------------------------------ 3D objects
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

    def view(self, yaw, pitch):
        """Turn by yaw about the up axis, then tip towards the viewer by pitch (viewer at -z)."""
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

    def cv(self, k, yaw=30, pitch=20, cols=None, hi=None, dashed=True, sw=2.4, line=GREEN):
        """cols: (top, side, front) fills. hi: face index painted yellow."""
        top, side, front = cols or (TOP3, SIDE, FILL)
        pts, vis, nrm = self.view(yaw, pitch)
        P = lambda p: (p[0] * k, -p[1] * k)
        cv = Canvas()
        for fi, fc in enumerate(self.f):
            if vis[fi]:
                n = nrm[fi]
                col = YEL if fi == hi else top if n[1] > 0.5 else side if n[0] > 0.3 else front
                cv.poly([P(pts[i]) for i in fc], col, sw, line)
        if dashed:
            for (a, b), fs in self.edges.items():
                if not any(vis[f] for f in fs):
                    cv.line(P(pts[a]), P(pts[b]), dashed=True, sw=1.6, col=line)
        cv.P, cv.pts, cv.vis, cv.nrm = P, pts, vis, nrm
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


def prism_lying(w=1.2, h=0.95, D=1.8):
    """Triangular prism lying on a rectangle face: triangle ends at x=0 and x=D."""
    tri = [(0, 0), (w, 0), (w / 2, h)]          # (z, y)
    v = [(0, y, z) for z, y in tri] + [(D, y, z) for z, y in tri]
    f = [[0, 1, 2], [3, 4, 5]] + [[i, (i + 1) % 3, 3 + (i + 1) % 3, 3 + i] for i in range(3)]
    return Solid(v, f)


VIEWS = {
    "cube": (lambda: box(1.1, 1.1, 1.1), 30, 22),
    "cube_turned": (lambda: box(1.1, 1.1, 1.1), 50, 30),
    "cube_small": (lambda: box(0.7, 0.7, 0.7), -25, 22),
    "rp_flat": (lambda: box(1.9, 0.8, 1.0), 25, 22),
    "rp_tall": (lambda: box(0.8, 1.8, 0.7), 35, 18),
    "tp": (lambda: prism_lying(), -50, 16),
    "tp_turned": (lambda: prism_lying(1.1, 0.9, 1.6), 55, 18),
    "pyr": (lambda: pyramid(), 25, 18),
    "pyr_turned": (lambda: pyramid(1.2, 1.5), -30, 25),
}
VIEW_KIND = {"cube": CUBE, "cube_turned": CUBE, "cube_small": CUBE, "rp_flat": PRISM, "rp_tall": PRISM,
             "tp": PRISM, "tp_turned": PRISM, "pyr": PYR, "pyr_turned": PYR}


def solid_cv(view, k=50, hi=None):
    f, yaw, pitch = VIEWS[view]
    return f().cv(k, yaw, pitch, hi=hi)


def hi_face(view, want):
    """Index of the visible face to paint yellow: want = 'front' (faces us most), 'tri' or 'quad'."""
    f, yaw, pitch = VIEWS[view]
    S = f()
    pts, vis, nrm = S.view(yaw, pitch)
    ok = [i for i in range(len(S.f)) if vis[i] and (want == "front" or len(S.f[i]) == (3 if want == "tri" else 4))
          and nrm[i][1] < 0.5]                       # never the top face (seen very flat)
    assert ok, (view, want)
    return min(ok, key=lambda i: nrm[i][2])


def _rot90(pts, on):
    return [(-y, x) for x, y in pts] if on else pts


def cylinder_cv(s=1.0, lying=False, body=FILL, top=TOP3, line=GREEN, dashed=True, band=None, hf=1.0):
    rx, ry, h = 36 * s, 11 * s, 72 * s * hf
    R = lambda p: _rot90(p, lying)
    cv = Canvas()
    cv.poly(R(ellipse(0, 0, rx, ry, 180, 360) + ellipse(0, h, rx, ry, 0, 180)), body, 0)
    if band:                                          # a paper label round the side (soup can)
        y1, y2, col = h * 0.25, h * 0.75, band
        cv.poly(R(ellipse(0, y1, rx, ry, 0, 180) + ellipse(0, y2, rx, ry, 180, 0)), col, 0)
    cv.poly(R(ellipse(0, 0, rx, ry, 0, 360)[:-1]), top, 2.4, line)
    cv.pline(R([(-rx, 0), (-rx, h)]), col=line)
    cv.pline(R([(rx, 0), (rx, h)]), col=line)
    cv.pline(R(ellipse(0, h, rx, ry, 0, 180)), col=line)
    if dashed:
        cv.pline(R(ellipse(0, h, rx, ry, 180, 360)), dashed=True, sw=1.6, col=line)
    return cv


def cone_cv(s=1.0, how="up", body=FILL, line=GREEN, dashed=True, dots=None, top=TOP3, stripe=None):
    """how: 'up' (point at the top), 'down' (point at the bottom), 'side' (lying down)."""
    rx, ry, h = 38 * s, 11 * s, 80 * s
    cv = Canvas()
    if how == "down":
        cv.poly([(0, h)] + ellipse(0, 0, rx, ry, 0, 180), body, 0)
        cv.pline([(-rx, 0), (0, h), (rx, 0)], col=line)
        cv.poly(ellipse(0, 0, rx, ry, 0, 360)[:-1], top, 2.4, line)
        return cv
    R = lambda p: _rot90(p, how == "side")
    cv.poly(R([(0, 0)] + ellipse(0, h, rx, ry, 180, 0)), body, 0)
    cv.poly(R([(0, 0)] + ellipse(0, h, rx, ry, 0, 180)), body, 0)
    if stripe:                                        # a white band round a pylon
        t1, t2 = 0.42, 0.6
        cv.poly(R([(-rx * t1, h * t1), (rx * t1, h * t1), (rx * t2, h * t2), (-rx * t2, h * t2)]), stripe, 0)
    if dots:                                          # spots on a party hat, inside the cone
        for t, f in [(0.38, 0), (0.6, -0.42), (0.66, 0.4), (0.86, -0.05)]:
            y = h * t
            x = f * rx * t
            assert abs(x) + 5 * s < rx * t
            cv.circle(R([(x, y)])[0], 5 * s, fill=dots, sw=0)
    cv.pline(R([(-rx, h), (0, 0), (rx, h)]), col=line)
    cv.pline(R(ellipse(0, h, rx, ry, 0, 180)), col=line)
    if dashed:
        cv.pline(R(ellipse(0, h, rx, ry, 180, 360)), dashed=True, sw=1.6, col=line)
    return cv


def sphere_cv(s=1.0):
    r = 40 * s
    cv = Canvas()
    cv.circle((0, 0), r, fill=FILL, sw=2.4)
    cv.pline(ellipse(0, 0, r, r * 0.3, 0, 180), sw=1.6)
    cv.pline(ellipse(0, 0, r, r * 0.3, 180, 360), dashed=True, sw=1.2)
    cv.poly(ellipse(-r * 0.4, -r * 0.45, r * 0.2, r * 0.12, 0, 360, 24)[:-1], "#ffffff", 0)
    return cv


def pic3d(key, s=1.0, hi=None):
    """Any 3D picture by key. s scales it (1.0 = full size for one picture)."""
    if key in VIEWS:
        return solid_cv(key, 50 * s, hi)
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


# ------------------------------------------------------------ real objects (drawn from the same shapes)
def ball_cv(s=1.0):
    """A beach ball: a sphere with stripes."""
    r = 40 * s
    cv = Canvas()
    cv.circle((0, 0), r, fill="#e74c3c", sw=0)
    cv.poly(ellipse(0, 0, r * 0.55, r, 0, 360, 60)[:-1], "#ffffff", 1.2, "#7a2318")
    cv.poly(ellipse(0, 0, r * 0.2, r, 0, 360, 60)[:-1], "#3d7cc9", 1.2, "#1f4f88")
    cv.circle((0, 0), r, fill="none", sw=2.4, col="#7a2318")
    return cv


def orange_cv(s=1.0):
    r = 36 * s
    cv = Canvas()
    cv.circle((0, 0), r, fill="#f5a623", sw=2.4, col="#b5650d")
    for x, y in [(-12, 6), (10, -10), (14, 14), (-6, -18), (-18, -4), (2, 20)]:
        cv.circle((x * s, y * s), 1.4 * s, fill="#c97a12", sw=0)
    cv.poly([(2 * s, -r), (16 * s, -r - 12 * s), (24 * s, -r - 6 * s), (10 * s, -r + 2 * s)], "#4a9a3a", 1.5, "#2e6b22")
    return cv


def dice_cv(k=48):
    """A number cube."""
    f, yaw, pitch = VIEWS["cube"]
    S = f()
    cv = S.cv(k, yaw, pitch, cols=("#ffffff", "#e8e8e8", "#f6f6f6"), dashed=False, line="#555555")
    pips = {1: [(0.5, 0.5)], 2: [(0.27, 0.27), (0.73, 0.73)], 3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)]}
    shown = [fi for fi, v in enumerate(cv.vis) if v]
    assert len(shown) == 3
    for n, fi in zip((1, 2, 3), shown):
        a, b, d = (cv.P(cv.pts[i]) for i in (S.f[fi][0], S.f[fi][1], S.f[fi][3]))
        for u, v in pips[n]:
            cv.circle((a[0] + u * (b[0] - a[0]) + v * (d[0] - a[0]), a[1] + u * (b[1] - a[1]) + v * (d[1] - a[1])),
                      4.2 if n == 1 else 3.6, fill="#222222", sw=0)
    return cv


def cereal_cv(k=46):
    """A tall cereal box with a band across the front."""
    S = box(1.2, 1.7, 0.5)
    cv = S.cv(k, 25, 18, cols=("#fff3c4", "#e0b23c", "#f6cf4a"), dashed=False, line="#8a6100")
    assert cv.vis[0]                                  # face 0 (the big L x H face) is the front
    a, b, d = (cv.P(cv.pts[i]) for i in (S.f[0][0], S.f[0][1], S.f[0][3]))
    Q = lambda u, v: (a[0] + u * (b[0] - a[0]) + v * (d[0] - a[0]), a[1] + u * (b[1] - a[1]) + v * (d[1] - a[1]))
    cv.poly([Q(0, 0.55), Q(1, 0.55), Q(1, 0.8), Q(0, 0.8)], "#c0392b", 0)
    cv.circle(Q(0.5, 0.3), 0.18 * k, fill="#ffffff", sw=1.5, col="#8a6100")
    return cv


def can_cv(s=1.0):
    """A soup can: a cylinder with a red paper label."""
    return cylinder_cv(s, body="#c9ced6", top="#e4e7ec", line="#4a5260", dashed=False, band="#c0392b")


def puck_cv(s=1.0):
    """A hockey puck: a short, wide cylinder."""
    return cylinder_cv(s, body="#262626", top="#5a5a5a", line="#000000", dashed=False, hf=0.36)


def pylon_cv(s=1.0):
    return cone_cv(s, body="#f57c00", line="#8a3f00", dashed=False, stripe="#ffffff")


def hat_cv(s=1.0):
    return cone_cv(s, body="#b39ddb", line="#5b3f8c", dashed=False, dots="#ffd84d")


def tent_cv(k=50):
    """A tent: a triangular prism with a door on the front end."""
    S = prism_lying(1.3, 1.0, 1.8)
    cv = S.cv(k, -50, 14, cols=("#f5b041", "#e67e22", "#f39c12"), dashed=False, line="#8a4b08")
    end = [fi for fi in (0, 1) if cv.vis[fi]]
    assert len(end) == 1
    i, j, top = S.f[end[0]]
    A, B, T = cv.P(cv.pts[i]), cv.P(cv.pts[j]), cv.P(cv.pts[top])
    m = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
    L = lambda p, q, t: (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
    cv.poly([L(m, A, 0.32), L(m, B, 0.32), L(m, T, 0.55)], "#7a3e06", 0)
    return cv


def icecream_cv(s=1.0):
    """An empty ice-cream cone: a cone with its point down."""
    rx, ry, h = 34 * s, 10 * s, 84 * s
    body, line = "#e3b26a", "#8a5a1a"
    cv = Canvas()
    cv.poly([(0, h)] + ellipse(0, 0, rx, ry, 0, 180), body, 0)
    for t in (0.3, 0.55, 0.8):                         # waffle lines across the cone
        y = h * t
        half = rx * (1 - t)
        cv.line((-half + 2, y - 4 * s), (half - 2, y + 4 * s), sw=1.2, col=line)
    cv.pline([(-rx, 0), (0, h), (rx, 0)], col=line)
    cv.poly(ellipse(0, 0, rx, ry, 0, 360)[:-1], "#f3dca8", 2.4, line)
    return cv


def grid_q(pos, q, right, others, why, label="four shapes labelled A to D"):
    """A-D picture question. why has %s for the letter."""
    p = pos.next()
    cells = list(others)
    cells.insert(p, right)
    L = "ABCD"[p]
    return mcq_fixed(fig(grid_svg(cells, label)) + q, list("ABCD"), L, why % L)


def two(cvs, caps, label, gap=36):
    return fig(row_svg(cvs, caps, label, gap=gap, fs=15))



def log_cv(s=1.0):
    """A cedar log lying down: a cylinder with tree rings on the end we see."""
    cv = cylinder_cv(s, lying=True, body="#a0522d", top="#e0b07a", line="#5a2d0c", dashed=False)
    rx, ry = 36 * s, 11 * s
    for f in (0.6, 0.3):                              # rings on the end face (the end face is turned by _rot90)
        cv.poly(_rot90(ellipse(0, 0, rx * f, ry * f, 0, 360, 36)[:-1], True), "none", 1.2, "#8a5a2b")
    return cv


def salmon_cv(s=1.0):
    """A can of salmon: a short cylinder with a pink label."""
    return cylinder_cv(s, body="#c9ced6", top="#e4e7ec", line="#4a5260", dashed=False, band="#f08080", hf=0.6)


# ------------------------------------------------------------ set 1: name 2D shapes
WRONG2 = {
    "circle": ["oval", "sphere", "square"],
    "triangle": ["cone", "square", "rectangle"],
    "square": ["diamond", "triangle", "cube"],          # never "rectangle": a square is a special rectangle
    "rectangle": ["square", "triangle", "oval"],
    "hexagon": ["pentagon", "octagon", "circle"],
}
E2 = {
    "circle": "It is flat and round. It has no corners. It is a circle.",
    "triangle": "It has 3 straight sides and 3 corners. It is a triangle.",
    "square": "It has 4 sides. They are all the same length. It is a square.",
    "rectangle": "It has 4 sides and 4 square corners. 2 sides are long. 2 are short. It is a rectangle.",
    "hexagon": "Count the sides: 1, 2, 3, 4, 5, 6. A shape with 6 sides is a hexagon.",
}


def set_name2d(rnd, pos):
    its = []
    asks = ["What shape is this?", "Name this shape.", "What is this shape called?"]
    plan = [  # key, turn, scale, colour, note
        ("circle", 0, 1.0, 1, ""),
        ("circle", 0, 0.5, 2, " It is small. It is still a circle."),
        ("circle", 0, 0.8, 4, " Colour does not change the name."),
        ("tri_eq", 0, 1.0, 0, ""),
        ("tri_eq", 180, 0.8, 3, " It is upside down. It is still a triangle."),
        ("tri_thin", 0, 0.9, 2, " A long, thin triangle is still a triangle."),
        ("square", 0, 1.0, 3, ""),
        ("square", 45, 0.9, 4, " It stands on a corner. Some people say “diamond”. It is still a square."),
        ("square", 20, 0.6, 0, " It is small and turned. It is still a square."),
        ("rect", 0, 1.0, 2, ""),
        ("rect", 90, 0.9, 1, " It is standing up. It is still a rectangle."),
        ("rect_long", 25, 0.9, 3, " It is tilted. It is still a rectangle."),
        ("hex", 0, 1.0, 2, ""),
        ("hex_flat", 0, 0.7, 0, " It is small. It is still a hexagon."),
        ("hex", 15, 0.9, 4, " It is turned. It is still a hexagon."),
        ("hex_wide", 0, 0.9, 1, " Its sides are not all the same. It still has 6 sides, so it is a hexagon."),
    ]
    for i, (key, deg, s, c, note) in enumerate(plan):
        kind = "circle" if key == "circle" else KIND2D[key]
        its.append(mcq(fig(flat(key, deg, s, c).svg("a flat shape")) + asks[i % 3], kind, WRONG2[kind], E2[kind] + note))
    its.append(grid_q(pos, "Which shape is a triangle?", flat("tri_tall", 180, 0.9, 1),
                      [flat("square", 0, 0.9, 2), flat("rect", 90, 0.8, 0), flat("hex", 0, 0.95, 4)],
                      "%s has 3 straight sides. It points down. It is still a triangle."))
    its.append(grid_q(pos, "Which shape is a circle?", flat("circle", 0, 1.0, 2),
                      [flat("oval", 0, 0.85, 1), flat("hex", 0, 0.95, 3), flat("square", 45, 0.9, 0)],
                      "%s is round all the way. The oval is stretched. The hexagon has 6 straight sides."))
    its.append(grid_q(pos, "Which shape is a square?", flat("square", 45, 0.85, 3),
                      [flat("rect", 0, 0.75, 2), flat("tri_eq", 0, 0.9, 1), flat("circle", 0, 0.9, 0)],
                      "%s has 4 sides the same length. It stands on a corner. It is still a square."))
    its.append(grid_q(pos, "Which shape is a rectangle?", flat("rect_long", 0, 0.65, 1),
                      [flat("hex_wide", 0, 0.75, 0), flat("tri_right", 0, 0.9, 2), flat("oval", 0, 0.85, 4)],
                      "%s has 4 sides and 4 square corners. 2 sides are long. 2 are short. It is a rectangle."))
    assert len(its) == 20, len(its)
    return {"title": "Name 2D shapes", "items": its}


# ------------------------------------------------------------ set 2: sort by sides and corners
def row_count_q(cells, kind_word, n, total, e):
    q = fig(row_svg(cells, [""] * len(cells), "a row of shapes", gap=14)) + "How many %s can you see?" % kind_word
    return mcq(q, n, [n - 1, n + 1, total], e)


def rule_q(cells, label, right, wrong, e, ask="These are in one group. What is the sorting rule?"):
    return mcq(fig(row_svg(cells, [""] * len(cells), label, gap=18)) + ask, right, wrong, e)


def set_sort(rnd, pos, P):
    its = []
    its.append(grid_q(pos, "Which shape is the odd one out?", flat("square", 0, 0.9, 2),
                      [flat("tri_eq", 180, 0.8, 0), flat("tri_thin", 20, 0.65, 3), flat("tri_right", 0, 0.5, 1)],
                      "%s has 4 sides. It is a square. The others have 3 sides. They are all triangles."))
    its.append(grid_q(pos, "Which shape is NOT a triangle?", flat("rect", 90, 0.8, 4),
                      [flat("tri_tall", 0, 0.9, 1), flat("tri_eq", 90, 0.85, 2), flat("tri_right", 135, 0.7, 0)],
                      "%s has 4 sides. It is a rectangle. Every triangle has 3 sides, any way it points."))
    its.append(grid_q(pos, "Which shape is NOT a square?", flat("rect", 0, 0.75, 1),
                      [flat("square", 45, 0.85, 3), flat("square", 0, 0.5, 0), flat("square", 15, 0.95, 4)],
                      "%s has 2 long sides and 2 short sides. It is a rectangle. The squares are turned, but all their sides are the same."))
    its.append(grid_q(pos, "Which shape is the odd one out?", flat("circle", 0, 0.9, 3),
                      [flat("hex", 0, 0.9, 1), flat("hex_flat", 0, 0.7, 2), flat("hex_wide", 0, 0.75, 0)],
                      "%s is round. It has no corners. The others have 6 corners. They are hexagons."))
    # what shape has this many sides / corners
    for key, deg, s, c, q, n, wrong, e in [
            ("tri_eq", 0, 0.9, 1, "How many sides does this shape have?", 3, [2, 4, 6],
             "Count the straight sides: 1, 2, 3. A triangle has 3 sides."),
            ("hex", 0, 0.9, 3, "How many sides does this shape have?", 6, [5, 7, 4],
             "Touch each side and count: 1, 2, 3, 4, 5, 6. It has 6 sides."),
            ("rect_long", 25, 0.8, 2, "How many corners does this shape have?", 4, [2, 3, 5],
             "Count the corners: 1, 2, 3, 4. A rectangle has 4 corners, even when it is tilted."),
            ("circle", 0, 0.8, 0, "How many corners does a circle have?", 0, [1, 2, 4],
             "A circle is round all the way. It has no corners: 0."),
    ]:
        its.append(mcq(fig(flat(key, deg, s, c).svg("a flat shape")) + q, n, wrong, e))
    its.append(rule_q([flat("tri_eq", 0, 0.7, 0), flat("tri_right", 40, 0.55, 3), flat("tri_thin", 0, 0.5, 1), flat("tri_tall", 180, 0.5, 2)],
                      "a row of shapes in one group", "3 sides", ["same colour", "same size", "4 sides"],
                      "The colours and sizes are different. Every shape has 3 sides. The rule is 3 sides."))
    its.append(rule_q([flat("circle", 0, 0.45, 2), flat("circle", 0, 0.8, 4), flat("circle", 0, 0.6, 0), flat("oval", 0, 0.6, 3)],
                      "a row of shapes in one group", "no corners", ["same colour", "same size", "3 corners"],
                      "The colours and sizes are different. No shape has a corner. The rule is no corners."))
    its.append(rule_q([flat("square", 0, 0.6, 1), flat("rect", 0, 0.55, 1), flat("square", 45, 0.55, 4), flat("rect_long", 90, 0.45, 2)],
                      "a row of shapes in one group", "4 corners", ["same colour", "3 corners", "6 corners"],
                      "Some are squares and some are rectangles. Every shape has 4 corners. The rule is 4 corners."))
    its.append(rule_q([flat("hex", 0, 0.55, 2), flat("hex_flat", 0, 0.5, 0), flat("hex_wide", 0, 0.5, 4), flat("hex", 15, 0.4, 1)],
                      "a row of shapes in one group", "6 sides", ["5 sides", "same size", "no corners"],
                      "The sizes and colours are different. Count the sides of each one: 6. The rule is 6 sides."))
    n, he, his = P.next()
    sort_fig = two([flat("tri_eq", 0, 0.7, 0), flat("square", 0, 0.65, 1)], ["3 sides", "4 sides"], "two groups: 3 sides and 4 sides", gap=50)
    its.append(mcq(sort_fig + "%s sorts shapes into 2 groups. Where does a rectangle go?" % n, "4 sides",
                   ["3 sides", "both groups", "neither group"],
                   "A rectangle has 4 sides. It goes in the 4 sides group."))
    n, he, his = P.next()
    its.append(mcq(sort_fig + "%s uses the same 2 groups. Where does a circle go?" % n, "neither group",
                   ["3 sides", "4 sides", "both groups"],
                   "A circle has no straight sides. It does not go in either group."))
    n, he, his = P.next()
    cor_fig = two([flat("circle", 0, 0.7, 3), flat("tri_eq", 0, 0.75, 1)], ["no corners", "corners"],
                  "two groups: no corners and corners", gap=40)
    its.append(mcq(cor_fig + "%s sorts shapes into 2 groups. Where does a hexagon go?" % n, "corners",
                   ["no corners", "both groups", "neither group"],
                   "A hexagon has 6 corners. It goes in the corners group."))
    n, he, his = P.next()
    its.append(grid_q(pos, "%s’s group has only shapes with 4 corners. Which shape can go in?" % n,
                      flat("rect", 90, 0.75, 3), [flat("tri_eq", 0, 0.9, 1), flat("circle", 0, 0.9, 0), flat("hex", 0, 0.9, 2)],
                      "%s is a rectangle. It has 4 corners. The triangle has 3. The circle has none. The hexagon has 6."))
    row1 = [flat("tri_eq", 0, 0.6, 0), flat("square", 0, 0.6, 1), flat("tri_right", 160, 0.55, 2),
            flat("circle", 0, 0.6, 3), flat("tri_thin", 40, 0.45, 4), flat("hex", 0, 0.55, 2)]
    its.append(row_count_q(row1, "triangles", 3, 6,
                           "Look for 3 sides. There are 3 triangles. The turned one and the thin one count too."))
    row2 = [flat("square", 45, 0.6, 2), flat("rect", 0, 0.55, 0), flat("square", 0, 0.45, 4),
            flat("tri_eq", 0, 0.6, 1), flat("square", 20, 0.65, 3), flat("circle", 0, 0.55, 0), flat("square", 0, 0.7, 1)]
    its.append(row_count_q(row2, "squares", 4, 7,
                           "Look for 4 sides the same length. There are 4 squares. The squares on a corner count too. The long one is a rectangle."))
    row3 = [flat("circle", 0, 0.55, 4), flat("pent", 0, 0.55, 1), flat("oval", 0, 0.55, 2),
            flat("square", 0, 0.6, 3), flat("circle", 0, 0.4, 0), flat("tri_eq", 0, 0.55, 2)]
    its.append(row_count_q(row3, "shapes with no corners", 3, 6,
                           "The 2 circles and the oval are round. They have no corners. That is 3 shapes."))
    its.append(mcq(two([flat("square", 0, 0.75, 0), flat("square", 45, 0.75, 0)], ["", ""], "two shapes")
                   + "Are these the same shape?", "Yes, both squares", ["No, one is a diamond", "No, one is bigger", "No, one has 3 sides"],
                   "The second one is turned onto a corner. It still has 4 sides the same length. Both are squares."))
    assert len(its) == 20, len(its)
    return {"title": "Sort shapes by sides and corners", "items": its}


# ------------------------------------------------------------ set 3: name 3D objects
WRONG3 = {CUBE: ["square", SPH, CYL],
          CYL: ["circle", CONE, "rectangle"],
          CONE: [CYL, "triangle", SPH],
          SPH: ["circle", CYL, CONE]}
E3 = {
    CUBE: "It is solid. All its faces are squares of the same size. It is a cube. A square is flat.",
    CYL: "It has a flat circle at each end and a curved side. It is a cylinder.",
    CONE: "It has 1 flat circle and a point. It is a cone. A triangle is flat.",
    SPH: "It is round all over, like a ball. It is a sphere. A circle is flat.",
}
TURN3 = {"cube_turned": " It is turned. It is still a cube.",
         "cube_small": " It is small. It is still a cube.",
         "cyl_lying": " It is lying on its side. It is still a cylinder.",
         "cone_down": " It is upside down. It is still a cone.",
         "cone_side": " It is lying on its side. It is still a cone."}


def set_objects(rnd, pos):
    its = []
    asks = ["What 3D object is this?", "Name this 3D object.", "What is this 3D object called?"]
    plan = ["cube", "cube_turned", "cube_small", "cyl", "cyl_lying", "cone", "cone_down", "cone_side", "sphere"]
    for i, k in enumerate(plan):
        kind = KIND[k]
        its.append(mcq(fig(pic3d(k).svg("a 3D object")) + asks[i % 3], kind, WRONG3[kind], E3[kind] + TURN3.get(k, "")))
    lab = "four objects labelled A to D"
    its.append(grid_q(pos, "Which one is a sphere?", sphere_cv(0.95),
                      [flat("circle", 0, 1.0, 0), pic3d("cyl_lying", 0.6), pic3d("cube", 0.75)],
                      "%s is round all over, like a ball. It is a sphere. The circle is flat, so it is not a sphere.", lab))
    its.append(grid_q(pos, "Which one is a cylinder?", pic3d("cyl", 0.8),
                      [pic3d("cone", 0.8), flat("rect", 90, 0.75, 1), sphere_cv(0.9)],
                      "%s has a flat circle at each end and a curved side. It is a cylinder. The rectangle is flat.", lab))
    its.append(grid_q(pos, "Which one is a cone?", pic3d("cone_down", 0.8),
                      [flat("tri_eq", 0, 0.95, 2), pic3d("cyl", 0.8), pic3d("cube", 0.75)],
                      "%s has 1 flat circle and a point. It is a cone. It is upside down. The triangle is flat.", lab))
    for cv, name, kind, e in [
            (ball_cv(), "a beach ball", SPH, "A ball is round all over. It is a sphere. A circle is flat."),
            (orange_cv(), "an orange", SPH, "An orange is round all over, like a ball. It is a sphere."),
            (dice_cv(), "a number cube", CUBE, "It has 6 square faces, all the same size. It is a cube. A square is just one flat face."),
            (salmon_cv(), "a can of salmon", CYL, "The can has a flat circle at the top and the bottom. Its side is curved. It is a cylinder."),
            (puck_cv(1.2), "a hockey puck", CYL, "A hockey puck has a flat circle on the top and the bottom. Its side is curved. "
                                                 "It is a short cylinder."),
            (log_cv(), "a cedar log", CYL, "The log has a flat circle at each end. Its side is curved. It is a cylinder lying down."),
            (pylon_cv(), "a pylon", CONE, "A pylon has a round bottom and a point at the top. It is a cone."),
            (icecream_cv(), "an ice-cream cone", CONE, "It has a circle at the top and a point at the bottom. It is a cone."),
    ]:
        its.append(mcq(fig(cv.svg(name)) + "This is %s. What 3D object is it?" % name, kind, WRONG3[kind], e))
    assert len(its) == 20, len(its)
    return {"title": "Name 3D objects around us", "items": its}


# ------------------------------------------------------------ set 4: flat (2D) or solid (3D)
def fs_q(cv, label, right, wrong, e):
    return mcq(fig(cv.svg(label)) + "Is it flat or solid? What is it?", right, wrong, e)


def set_compare(rnd, pos, P):
    its = []
    its.append(fs_q(flat("circle", 0, 0.9, 1), "a flat shape", "flat: a circle", ["solid: a sphere", "flat: a sphere", "solid: a circle"],
                    "It is flat, like a drawing. It is round. It is a circle, a 2D shape."))
    its.append(fs_q(sphere_cv(0.95), "a 3D object", "solid: a sphere", ["flat: a circle", "solid: a circle", "solid: a cylinder"],
                    "It is round all over. You can hold it. It is a sphere, a 3D object."))
    its.append(fs_q(flat("square", 0, 0.9, 2), "a flat shape", "flat: a square", ["solid: a cube", "flat: a cube", "solid: a square"],
                    "It is flat. It has 4 sides the same length. It is a square, a 2D shape."))
    its.append(fs_q(pic3d("cube", 0.95), "a 3D object", "solid: a cube", ["flat: a square", "solid: a square", "flat: a cube"],
                    "It is solid. It has 6 square faces. It is a cube, a 3D object."))
    its.append(fs_q(flat("tri_eq", 0, 0.9, 3), "a flat shape", "flat: a triangle", ["solid: a cone", "flat: a cone", "solid: a triangle"],
                    "It is flat. It has 3 sides. It is a triangle, a 2D shape."))
    its.append(fs_q(pic3d("cone", 0.95), "a 3D object", "solid: a cone", ["flat: a triangle", "solid: a triangle", "solid: a cylinder"],
                    "It is solid. It has a round bottom and a point. It is a cone, a 3D object."))
    lab = "four pictures labelled A to D"
    its.append(grid_q(pos, "Which one is flat?", flat("circle", 0, 0.95, 3),
                      [sphere_cv(0.9), pic3d("cyl", 0.8), pic3d("cone", 0.8)],
                      "%s is a circle. It is flat, a 2D shape. The others are solid 3D objects.", lab))
    its.append(grid_q(pos, "Which one is solid?", pic3d("cube", 0.75),
                      [flat("square", 0, 0.9, 0), flat("tri_eq", 0, 0.95, 1), flat("circle", 0, 0.95, 2)],
                      "%s is a cube. It is solid, a 3D object. The others are flat 2D shapes.", lab))
    its.append(grid_q(pos, "Which one is a 2D shape?", flat("square", 45, 0.85, 4),
                      [pic3d("cube_turned", 0.75), sphere_cv(0.9), pic3d("cyl_lying", 0.6)],
                      "%s is a square on its corner. It is flat, so it is 2D. The others are 3D objects.", lab))
    its.append(grid_q(pos, "Which one is a 3D object?", pic3d("cyl_lying", 0.6),
                      [flat("rect", 0, 0.75, 1), flat("circle", 0, 0.95, 4), flat("hex", 0, 0.95, 2)],
                      "%s is a cylinder. It is solid, so it is 3D. The others are flat shapes.", lab))
    its.append(mcq(two([flat("circle", 0, 0.75, 1), sphere_cv(0.75)], ["circle", "sphere"], "a circle and a sphere")
                   + "How is a circle different from a sphere?", "A circle is flat.",
                   ["A circle is bigger.", "A circle can roll.", "A circle has corners."],
                   "A circle is flat, like a drawing. A sphere is solid. You can hold a sphere."))
    its.append(mcq(two([flat("square", 0, 0.7, 2), pic3d("cube", 0.7)], ["square", "cube"], "a square and a cube")
                   + "How is a cube different from a square?", "A cube is solid.",
                   ["A cube is round.", "A cube has 3 sides.", "A cube is flat."],
                   "A square is flat. A cube is solid. Each face of a cube is a square."))
    its.append(mcq(two([flat("tri_eq", 0, 0.8, 0), pic3d("cone", 0.8)], ["triangle", "cone"], "a triangle and a cone")
                   + "How is a cone different from a triangle?", "A cone is solid.",
                   ["A cone is flat.", "A cone has 3 corners.", "A cone has 4 sides."],
                   "A triangle is flat, with 3 corners. A cone is solid. It has a round bottom and 1 point."))
    row = [flat("circle", 0, 0.5, 1), pic3d("cube", 0.5), sphere_cv(0.5), flat("tri_eq", 0, 0.55, 3),
           pic3d("cyl", 0.5), flat("square", 0, 0.55, 2)]
    its.append(mcq(fig(row_svg(row, [""] * 6, "a row of 2D shapes and 3D objects", gap=16)) + "How many are 3D objects?",
                   3, [2, 4, 6], "The cube, the sphere and the cylinder are solid. That is 3. The other 3 are flat."))
    row = [pic3d("cone", 0.5), flat("rect", 0, 0.5, 0), flat("hex", 0, 0.5, 4), sphere_cv(0.5),
           flat("circle", 0, 0.5, 2), flat("tri_eq", 0, 0.5, 1), pic3d("cube", 0.45)]
    its.append(mcq(fig(row_svg(row, [""] * 7, "a row of 2D shapes and 3D objects", gap=16)) + "How many are flat 2D shapes?",
                   4, [3, 5, 7], "The rectangle, hexagon, circle and triangle are flat. That is 4."))
    lab2 = "four pictures labelled A to D"
    its.append(grid_q(pos, "Which one can roll?", sphere_cv(0.9),
                      [pic3d("cube", 0.75), flat("circle", 0, 0.95, 1), flat("square", 0, 0.9, 2)],
                      "%s is a sphere. It is curved all over, so it rolls. A cube slides. Flat shapes do not roll.", lab2))
    its.append(grid_q(pos, "Which one can roll and stack?", pic3d("cyl", 0.8),
                      [sphere_cv(0.9), pic3d("cube", 0.75), ball_cv(0.85)],
                      "%s is a cylinder. It rolls on its curved side. It stacks on its flat ends. "
                      "A sphere and a ball roll, but they cannot stack. A cube stacks, but it cannot roll.", lab2))
    n, he, his = P.next()
    its.append(mcq(fig(ball_cv(0.9).svg("a beach ball")) + "%s holds a beach ball. Is it 2D or 3D?" % n,
                   "3D: a sphere", ["2D: a circle", "2D: a sphere", "3D: a cylinder"],
                   "You can hold it. It is round all over. It is a 3D sphere."))
    n, he, his = P.next()
    its.append(mcq(fig(dice_cv(44).svg("a number cube")) + "%s rolls a number cube. Is it 2D or 3D?" % n,
                   "3D: a cube", ["2D: a square", "2D: a cube", "3D: a sphere"],
                   "You can hold it. It has 6 square faces. It is a 3D cube."))
    n, he, his = P.next()
    its.append(mcq(fig(flat("rect", 0, 0.9, 4).svg("a flat rectangle")) + "%s draws this on paper. Is it 2D or 3D?" % n,
                   "2D: a rectangle", ["3D: a rectangle", "2D: a square", "3D: a cylinder"],
                   "A drawing on paper is flat. It has 2 long sides and 2 short sides. It is a 2D rectangle."))
    assert len(its) == 20, len(its)
    return {"title": "Flat or solid: compare 2D and 3D", "items": its}


# ------------------------------------------------------------ set 5: faces you can trace (word problems)
def set_faces(rnd, pos, P):
    its = []
    ask = "What shape is the yellow face?"
    hi = hi_face("cube", "front")
    its.append(mcq(fig(pic3d("cube", 1.0, hi=hi).svg("a cube with one face in yellow")) + ask, "square",
                   ["cube", "triangle", "circle"],
                   "The yellow face has 4 sides the same length. It is a square. The whole object is a cube."))
    its.append(mcq(fig(cylinder_cv(1.0, top=YEL).svg("a cylinder with its top face in yellow")) + ask, "circle",
                   ["oval", "cylinder", "sphere"],
                   "We see the top from the side, so it looks stretched. Trace it and you get a circle."))
    its.append(mcq(fig(cone_cv(1.0, "down", top=YEL).svg("a cone with its flat face in yellow")) + ask, "circle",
                   ["oval", "cone", "triangle"],
                   "The flat face of a cone is round. Trace it and you get a circle."))
    for cv, label, q, right, wrong, e in [
            (salmon_cv(0.9), "a can of salmon", "%s traces the bottom of a can of salmon. What shape does %s draw?", "a circle",
             ["a cylinder", "a square", "an oval"], "The bottom of the can is a flat circle. %s draws a circle."),
            (dice_cv(42), "a number cube", "%s traces one face of a number cube. What shape does %s draw?", "a square",
             ["a cube", "a circle", "a triangle"], "A number cube is a cube. Each face is a flat square. %s draws a square."),
            (puck_cv(1.1), "a hockey puck", "%s plays hockey in Kamloops. %s traces a puck. What shape does %s draw?", "a circle",
             ["a cylinder", "a rectangle", "an oval"], "The top of a puck is a flat circle. %s draws a circle."),
    ]:
        n, he, his = P.next()
        args = (n, he.capitalize(), he) if q.count("%s") == 3 else (n, he)
        its.append(mcq(fig(cv.svg(label)) + q % args, right, wrong, e % n))
    its.append(mcq(fig(pic3d("cyl", 0.9).svg("a cylinder")) + "How many flat faces does a cylinder have?", 2, [1, 0, 3],
                   "There is a flat circle on the top. There is one on the bottom. 1 + 1 = 2. The side is curved."))
    its.append(mcq(fig(pic3d("cone", 0.9).svg("a cone")) + "How many flat faces does a cone have?", 1, [0, 2, 3],
                   "A cone has 1 flat circle at the bottom. The rest is curved."))
    its.append(mcq(fig(pic3d("sphere", 0.9).svg("a sphere")) + "How many flat faces does a sphere have?", 0, [1, 2, 3],
                   "A sphere is curved all over. It has no flat faces: 0."))
    its.append(mcq(fig(pic3d("cube", 0.9).svg("a cube")) + "How many faces does a cube have?", 6, [3, 4, 8],
                   "You can see 3 faces. 3 more are at the back, on the side and under it. 3 + 3 = 6."))
    lab = "four objects labelled A to D"
    its.append(grid_q(pos, "Which object has a square face?", pic3d("cube_small", 1.0),
                      [pic3d("cyl", 0.8), pic3d("cone", 0.8), sphere_cv(0.9)],
                      "%s is a cube. Its faces are squares. The cylinder and the cone have circle faces.", lab))
    its.append(grid_q(pos, "Which object has no flat faces?", sphere_cv(0.9),
                      [pic3d("cyl_lying", 0.6), pic3d("cone", 0.8), pic3d("cube_small", 1.0)],
                      "%s is a sphere. It is curved all over. The others have at least 1 flat face.", lab))
    its.append(grid_q(pos, "Which object has 1 circle face and a point?", pic3d("cone_down", 0.8),
                      [pic3d("cyl", 0.8), pic3d("cube", 0.75), sphere_cv(0.9)],
                      "%s is a cone. It has 1 flat circle and a point. The cylinder has 2 circles and no point.", lab))
    n, he, his = P.next()
    its.append(mcq(fig(flat("square", 0, 0.8, 4).svg("a square print")) + "%s dips a block in paint. "
                   "%s stamps this shape. Which block did %s use?" % (n, he.capitalize(), he),
                   "a cube", ["a cylinder", "a cone", "a sphere"],
                   "The print is a square. A cube has square faces. A cylinder and a cone make circles."))
    n, he, his = P.next()
    its.append(mcq(fig(flat("circle", 0, 0.8, 1).svg("a circle print")) + "%s dips a block in paint. "
                   "%s stamps this shape. Which block did %s use?" % (n, he.capitalize(), he),
                   "a cylinder", ["a cube", "a sphere", "a square"],
                   "The print is a circle. The end of a cylinder is a flat circle. A sphere has no flat face to stamp."))
    n, he, his = P.next()
    its.append(mcq(fig(log_cv(0.9).svg("a cedar log")) + "%s finds a cedar log. %s traces both ends. How many circles?" % (n, he.capitalize()),
                   2, [1, 3, 4], "A log is a cylinder. It has a flat circle at each end. 1 + 1 = 2 circles."))
    n, he, his = P.next()
    its.append(mcq(fig(dice_cv(42).svg("a number cube")) + "%s traces every face of a number cube. How many squares?" % n,
                   6, [3, 4, 8], "A cube has 6 faces. Each one is a square. %s draws 6 squares." % n))
    n, he, his = P.next()
    its.append(mcq(fig(ball_cv(0.85).svg("a beach ball")) + "%s wants to trace a beach ball. What happens?" % n,
                   "No flat face to trace", ["%s draws a circle." % n, "%s draws a square." % n, "%s draws an oval." % n],
                   "A ball is a sphere. It is curved all over. It has no flat face to trace."))
    n, he, his = P.next()
    its.append(mcq(fig(salmon_cv(0.8).svg("a can of salmon")) + "%s stacks 3 cans of salmon. Which faces touch?" % n,
                   "the flat circles", ["the curved sides", "the points", "the squares"],
                   "Cans stack on their flat ends. The flat circle faces touch."))
    n, he, his = P.next()
    its.append(mcq(fig(pic3d("cone", 0.85).svg("a cone")) + "%s stamps a cone, flat side down. What print does %s get?" % (n, he),
                   "a circle", ["a triangle", "an oval", "a square"],
                   "The flat side of a cone is a circle. The print is a circle. A triangle is what we see from the side."))
    assert len(its) == 20, len(its)
    return {"title": "Faces you can trace: word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    flat5 = row_svg([flat("circle", 0, 0.8, 1), flat("tri_eq", 0, 0.8, 0), flat("square", 0, 0.8, 2), flat("rect", 0, 0.7, 3),
                     flat("hex", 0, 0.8, 4)],
                    ["circle", "triangle", "square", "rectangle", "hexagon"], "circle, triangle, square, rectangle and hexagon",
                    gap=20, fs=15)
    turned = row_svg([flat("square", 0, 0.8, 2), flat("square", 45, 0.75, 4), flat("tri_eq", 0, 0.8, 0), flat("tri_eq", 180, 0.5, 1)],
                     ["square", "still a square", "triangle", "still a triangle"],
                     "a square and the same square turned; a big triangle and a small upside-down triangle", gap=26, fs=15)
    sortf = row_svg([flat("square", 0, 0.55, 1), flat("rect", 0, 0.5, 3), flat("square", 45, 0.5, 4),
                     flat("rect_long", 90, 0.42, 2)], ["", "", "", ""], "squares and rectangles of different colours and sizes", gap=18)
    solids = row_svg([pic3d("cube", 0.7), sphere_cv(0.75), pic3d("cone", 0.7), pic3d("cyl", 0.7)],
                     ["cube", "sphere", "cone", "cylinder"], "cube, sphere, cone and cylinder", gap=26, fs=15)
    objs = row_svg([dice_cv(36), ball_cv(0.7), pylon_cv(0.7), salmon_cv(0.75)], ["number cube", "ball", "pylon", "can"],
                   "a number cube, a ball, a pylon and a can", gap=24, fs=15)
    pairs = row_svg([flat("circle", 0, 0.8, 0), sphere_cv(0.8), flat("square", 0, 0.75, 0), pic3d("cube", 0.75)],
                    ["circle (2D)", "sphere (3D)", "square (2D)", "cube (3D)"],
                    "a flat circle next to a sphere, and a flat square next to a cube", gap=22, fs=15)
    trace = row_svg([salmon_cv(0.7), flat("circle", 0, 0.7, 3), dice_cv(36), flat("square", 0, 0.65, 2)],
                    ["can", "trace: circle", "number cube", "trace: square"],
                    "a can and the circle it traces; a number cube and the square it traces", gap=22, fs=15)
    return (
        "<h2>2D shapes are flat</h2>"
        "<p>A 2D shape is <b>flat</b>, like a drawing on paper. Count the <b>sides</b> and <b>corners</b> to name it.</p>"
        "<figure class='sn-fig'>" + flat5 + "</figure>" +
        table(["Shape", "Sides", "Corners", "Look for"], [
            ["Circle", "0", "0", "Round all the way."],
            ["Triangle", "3", "3", "3 straight sides."],
            ["Square", "4", "4", "4 sides, all the same length."],
            ["Rectangle", "4", "4", "2 long sides and 2 short sides."],
            ["Hexagon", "6", "6", "6 straight sides."]]) +
        "<p>Size, colour and turning do not change the name.</p>"
        "<figure class='sn-fig'>" + turned +
        "<figcaption>A square on its corner is still a square, not a “diamond”.</figcaption></figure>" +
        ex("Example 1", "A shape has 6 straight sides. What is it?",
           "Count the sides: 1, 2, 3, 4, 5, 6. Six sides make a hexagon.", "a hexagon") +
        "<h2>Sort by sides and corners</h2>"
        "<p>To sort, look at <b>one thing</b> at a time: the number of sides, the number of corners, or no corners. "
        "The <b>sorting rule</b> tells what is the same in a group.</p>"
        "<figure class='sn-fig'>" + sortf +
        "<figcaption>The colours and sizes are different. All have 4 corners. The rule is “4 corners”.</figcaption></figure>" +
        ex("Example 2", "A group has 2 circles and an oval. What is the rule?",
           "They are all round. None of them has a corner.", "no corners") +
        "<h2>3D objects are solid</h2>"
        "<p>A 3D object is <b>solid</b>. You can pick it up and hold it. Dashed lines show the back.</p>"
        "<figure class='sn-fig'>" + solids + "</figure>" +
        table(["Object", "Look for"], [
            ["Cube", "6 flat square faces, all the same size."],
            ["Sphere", "Round all over, like a ball."],
            ["Cone", "1 flat circle and a point."],
            ["Cylinder", "A flat circle at each end and a curved side."]]) +
        "<figure class='sn-fig'>" + objs +
        "<figcaption>A number cube is a cube. A ball is a sphere. A pylon is a cone. A can is a cylinder.</figcaption></figure>"
        "<h2>Flat or solid?</h2>"
        "<p>Every 3D object has a 2D shape that looks like it. The 2D shape is flat. The 3D object is solid.</p>"
        "<figure class='sn-fig'>" + pairs + "</figure>" +
        ex("Example 3", "Is a beach ball a circle or a sphere?",
           "You can hold it. It is round all over, so it is solid.", "a sphere") +
        "<h2>Faces you can trace</h2>"
        "<p>A <b>face</b> is a flat part of a 3D object. Trace around a face and you get a 2D shape.</p>"
        "<figure class='sn-fig'>" + trace + "</figure>" +
        ex("Example 4", "What shape do you get when you trace the bottom of a can?",
           "The bottom of the can is flat and round.", "a circle") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Calling a turned square a “diamond”", "Count the sides. 4 sides the same length make a square, any way up."],
            ["Calling a ball a circle", "A circle is flat. A ball is round all over: it is a sphere."],
            ["Calling a number cube a square", "A square is flat. A number cube is solid: it is a cube."],
            ["Calling a cone a triangle", "A triangle is flat. A cone is solid, with a round bottom and a point."],
            ["Saying the top of a can is an oval", "It only looks stretched from the side. Trace it: it is a circle."],
            ["Sorting by colour when the rule is sides", "Look at one thing at a time. Check that every shape follows the rule."],
        ])
    )


FAQ = [
    {"q": "What shapes do Grade 1 students learn in BC math?",
     "a": "In Geometry and measurement, Grade 1 students compare 2D shapes and 3D objects. They name circles, triangles, squares, "
          "rectangles and hexagons, sort shapes by sides and corners, and name cubes, spheres, cones and cylinders."},
    {"q": "What is the difference between a 2D shape and a 3D object?",
     "a": "A 2D shape is flat, like a drawing on paper. A 3D object is solid and you can hold it, like a ball (a sphere) or a can (a cylinder)."},
    {"q": "Is a square turned on its corner still a square?",
     "a": "Yes. It still has 4 sides of the same length, so it is a square. Many children call it a “diamond”, "
          "but turning a shape never changes its name."},
    {"q": "How can I help my Grade 1 child learn shapes at home?",
     "a": "Go on a shape hunt: find a ball (sphere), a can (cylinder), a number cube (cube) and an ice-cream cone (cone). "
          "Trace their flat faces on paper and sort the drawings by sides and corners."},
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
    """Tag pictures that must print larger (A-D choices, rows) so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(51808)
    P = People(rnd)
    sets = [set_name2d(rnd, Pos(rnd)), set_sort(rnd, Pos(rnd), P), set_objects(rnd, Pos(rnd)),
            set_compare(rnd, Pos(rnd), P), set_faces(rnd, Pos(rnd), P)]
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
            right = it["c"][it["a"]]
            if right in ("square", "a square"):           # a square is a special rectangle
                assert not any(c in ("rectangle", "a rectangle") for c in it["c"]), it["q"][-80:]
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-1", "slug": "2d-shapes-and-3d-objects", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "2D Shapes and 3D Objects: Name, Sort and Compare",
        "seo_title": "Grade 1 Math 2D Shapes and 3D Objects Worksheets (BC Curriculum, Free, Answer Key)",
        "short_title": "2D shapes and 3D objects",
        "domain": "Geometry and measurement",
        "standard_code": "Grade 1: Geometry and measurement",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/1/core",
        "standard_text": "Comparison of 2D shapes and 3D objects",
        "meta_desc": "Free Grade 1 math worksheets on 2D shapes and 3D objects for the BC curriculum: name circles, triangles, "
                     "squares, rectangles and hexagons, sort shapes by sides and corners, name cubes, spheres, cones and cylinders, "
                     "tell flat from solid and trace flat faces. 100 questions with an answer key.",
        "key_big": "2D shapes are flat. 3D objects are solid. Turning a shape never changes its name.",
        "key_sub": "Count sides and corners to name a 2D shape. A square on its corner is still a square. "
                   "A ball is a sphere, not a circle. Trace a flat face of a 3D object to get a 2D shape.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(four (shapes|objects|pictures)|a row of|two |a (circle|square|triangle) and a)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
