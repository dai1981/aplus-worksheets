# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 1 Math: 2D shapes and 3D objects (Ontario Curriculum 2020, Spatial Sense E1.1, E1.2, E1.3)
  python3 tools/gen_caon_math_g1_shapes.py
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.

Grade 1 students sort 3D objects and 2D shapes by one attribute at a time and name the sorting rule (E1.1),
find the 2D shapes in 3D objects: the flat faces you can trace (E1.2), and make and find matching halves (E1.3).
  2D shapes   circle, triangle, square, rectangle, hexagon (a square is a special rectangle)
  3D objects  cube, sphere, cone, cylinder, prism, pyramid, and the same objects around us
              (a ball, a number cube, a soup can, a hockey puck, a pylon, a cereal box, a tent)
Very short sentences, a picture in almost every question.

Rules kept everywhere (so every answer is right for every definition):
  - a square picture never has "rectangle" as a wrong answer; a cube never has "prism" as a wrong answer
  - colour, size and turning never change the name
Pictures are drawn from their corner points (checked: right number of sides, no crossing sides,
squares really square) and 3D objects from 3D vertices and faces (V − E + F = 2), with hidden edges dashed.
Matching halves are checked in code: a dashed line makes matching halves only when reflecting the shape across
it gives the same shape; a "missing half" answer is the exact mirror image of the half shown.
Wrong answers come from real student mistakes: a turned square called a diamond, a rectangle called a square,
circle vs sphere, square vs cube, triangle vs pyramid, cylinder vs cone, miscounting the sides of a hexagon,
sorting by colour when the rule is sides, calling a face that looks like an oval an oval, a slid half instead
of a flipped half, any line that cuts a shape in two makes matching halves.
Drawing helpers adapted from tools/gen_au_maths_y1_shapes.py and tools/gen_caon_math_g3_shapes.py.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-1")
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
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]

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


# ------------------------------------------------------------ matching halves
def refl_x(pts, x0):
    return [(2 * x0 - x, y) for x, y in pts]


def _key(pts):
    return sorted((round(x, 6), round(y, 6)) for x, y in pts)


def halves_match(pts, a, b):
    """True when folding along the line a-b puts the shape exactly on itself (corners and sides)."""
    d = (b[0] - a[0], b[1] - a[1])
    L = math.hypot(*d)
    d = (d[0] / L, d[1] / L)

    def r(p):
        v = (p[0] - a[0], p[1] - a[1])
        t = v[0] * d[0] + v[1] * d[1]
        return (2 * (a[0] + d[0] * t) - p[0], 2 * (a[1] + d[1] * t) - p[1])
    n = len(pts)
    edges = lambda P: {frozenset(((round(P[i][0], 4), round(P[i][1], 4)), (round(P[(i + 1) % n][0], 4), round(P[(i + 1) % n][1], 4))))
                       for i in range(n)}
    return edges([r(p) for p in pts]) == edges(pts)


def cut_cv(pts, a, b, c=0, curved=False, k=1.0):
    """A shape with a dashed red fold line from a to b (a and b just outside the shape). k scales the picture."""
    pts = [(x * k, y * k) for x, y in pts]
    a, b = (a[0] * k, a[1] * k), (b[0] * k, b[1] * k)
    cv = Canvas()
    cv.poly(pts, COLS[c][0], 0 if curved else 3, COLS[c][1])
    if curved:
        cv.poly(pts, "none", 3, COLS[c][1])
    cv.line(a, b, dashed=True, sw=3, col=RED, dash="8 5")
    return cv


def heart_pts(s=1.0):
    """A heart drawn from a smooth curve; it is the same on both sides of x = 0."""
    pts = []
    for i in range(72):
        t = 2 * math.pi * i / 72
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((x * 3.2 * s, y * 3.2 * s))
    assert _key(refl_x(pts, 0)) == _key(pts)
    return pts


def circle_pts(r):
    return ellipse(0, 0, r, r, 0, 360, 72)[:-1]


# shapes for fold-line questions (exact corner points)
H_SQ = [(0, 0), (80, 0), (80, 80), (0, 80)]
H_RECT = [(0, 0), (120, 0), (120, 64), (0, 64)]
H_TRI = [(0, 90), (45, 0), (90, 90)]
H_HEX = reg(6, 46)
H_HOUSE = [(0, 40), (40, 0), (80, 40), (80, 100), (0, 100)]
H_TRI_R = [(0, 0), (0, 80), (100, 80)]            # a right triangle: no up-and-down line works


def vline(pts, x, ext=12):
    ys = [p[1] for p in pts]
    return (x, min(ys) - ext), (x, max(ys) + ext)


def hline(pts, y, ext=12):
    xs = [p[0] for p in pts]
    return (min(xs) - ext, y), (max(xs) + ext, y)


def mid_x(pts):
    xs = [p[0] for p in pts]
    return (min(xs) + max(xs)) / 2


def mid_y(pts):
    ys = [p[1] for p in pts]
    return (min(ys) + max(ys)) / 2


# half shapes for "which half matches" (the half is left of the fold line x = 0)
HALVES = {
    "house": [(0, 0), (-45, 40), (-45, 100), (0, 100)],
    "tree": [(0, 0), (-45, 60), (-12, 60), (-12, 92), (0, 92)],
    "rocket": [(0, 0), (-22, 32), (-22, 88), (-42, 112), (0, 112)],
    "cup": [(0, 0), (-40, 0), (-30, 70), (0, 70)],
}
for _k, _h in HALVES.items():
    _m = refl_x(_h, 0)
    assert _key(_m) != _key([(x + 50, y) for x, y in _h])           # the mirror is not just the half slid over


def half_pick_q(pos, q, key, wrong_key, why):
    """Top: the half and the fold line. Bottom: 4 pieces A-D. Only one piece is the mirror image."""
    half = HALVES[key]
    mirror = refl_x(half, 0)
    slid = [(x + 45, y) for x, y in half]                          # same way round: slid, not flipped
    small = [(x * 0.6, y * 0.6) for x, y in mirror]
    other = refl_x(HALVES[wrong_key], 0)
    p = pos.next()
    cands = [slid, small, other]
    cands.insert(p, mirror)
    assert sum(1 for c in cands if _key(c) == _key(mirror)) == 1
    # top part
    top = Canvas()
    top.poly(half, COLS[1][0], 3, COLS[1][1])
    ys = [y for _, y in half]
    top.line((0, min(ys) - 10), (0, max(ys) + 10), dashed=True, sw=3, col=RED, dash="8 5")
    tw_, th = top.size()
    cell = 70
    rowW = 4 * cell
    s = []
    ox = -rowW / 2                                                   # fold line in the middle of the picture
    s.append(top.body(ox, top.y0 - 4))
    yb = th + 14
    for k, c in enumerate(cands):
        cv = Canvas()
        cv.poly(c, COLS[1][0], 2.6, COLS[1][1])
        w, h = cv.size()
        f = min(1.0, (cell - 22) / w, 82 / h)
        tx = k * cell + 20 + (cell - 22 - w * f) / 2
        ty = yb + 4 + (86 - h * f) / 2
        s.append("<g transform='translate(%.1f,%.1f) scale(%.3f)'>%s</g>" % (tx, ty, f, cv.body(cv.x0, cv.y0)))
        s.append("<text x='%d' y='%.0f' font-size='18' font-weight='700' fill='%s'>%s</text>" % (k * cell + 3, yb + 20, INK, "ABCD"[k]))
        if k:
            s.append("<line x1='%d' y1='%.0f' x2='%d' y2='%.0f' stroke='%s' stroke-width='1'/>" % (k * cell, yb, k * cell, yb + 92, GRAY))
    s.append("<line x1='4' y1='%.0f' x2='%d' y2='%.0f' stroke='%s' stroke-width='1'/>" % (yb - 6, rowW - 4, yb - 6, GRAY))
    svg = svg_wrap(rowW, int(yb + 96), "".join(s), "half a shape next to a fold line, and four pieces labelled A to D")
    L = "ABCD"[p]
    return mcq_fixed(fig(svg) + q, list("ABCD"), L, why % L)


def butterfly_cv(dots, s=1.0):
    """A butterfly: the left wings have dots, the right wings are empty. The fold line goes down the body."""
    cv = Canvas()
    for side in (-1, 1):
        cv.poly(ellipse(side * 30 * s, -16 * s, 28 * s, 22 * s, 0, 360, 48)[:-1], "#f6cfd8", 2.4, "#a33b5a")
        cv.poly(ellipse(side * 24 * s, 22 * s, 20 * s, 16 * s, 0, 360, 48)[:-1], "#f6cfd8", 2.4, "#a33b5a")
    cv.poly(ellipse(0, 2 * s, 6 * s, 40 * s, 0, 360, 36)[:-1], "#5b3f8c", 0)
    spots = [(-34, -24), (-22, -8), (-42, -8), (-26, 22), (-38, -32), (-14, 26)]
    for x, y in spots[:dots]:
        cv.circle((x * s, y * s), 5 * s, fill="#5b3f8c", sw=0)
    cv.line((0, -48 * s), (0, 52 * s), dashed=True, sw=2.4, col=RED, dash="8 5")
    return cv


def blocks_cv(cells, u=26):
    """Left half of a block picture: squares at (col, row) left of the fold line; the right side is empty."""
    cv = Canvas()
    rows = max(r for _, r in cells) + 1
    for c, r in cells:
        x = -u * (c + 1)
        y = -u * (r + 1)
        cv.poly([(x, y), (x + u, y), (x + u, y + u), (x, y + u)], COLS[2][0], 2.4, COLS[2][1])
    cv.line((0, -u * rows - 10), (0, 10), dashed=True, sw=3, col=RED, dash="8 5")
    cv.grow(u * 0.2, -u * rows, u * (max(c for c, _ in cells) + 1), 0)       # room on the right for the other half
    return cv


def pieces_cv(polys, c=0):
    cv = Canvas()
    for p in polys:
        cv.poly(p, COLS[c][0], 3, COLS[c][1])
    return cv


# ------------------------------------------------------------ set 1: name 2D shapes
WRONG2 = {
    "circle": ["oval", "sphere", "square"],
    "triangle": ["pyramid", "square", "rectangle"],
    "square": ["diamond", "triangle", "cube"],          # never "rectangle": a square is a special rectangle
    "rectangle": ["square", "triangle", "prism"],
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
    its.append(grid_q(pos, "Which shape is a hexagon?", flat("hex_flat", 0, 0.95, 0),
                      [flat("pent", 0, 0.95, 2), flat("square", 0, 0.9, 4), flat("tri_eq", 0, 0.95, 3)],
                      "%s has 6 sides. It is a hexagon. One other shape has only 5 sides, so it is not a hexagon."))
    assert len(its) == 20, len(its)
    return {"title": "Name 2D shapes", "items": its}


# ------------------------------------------------------------ set 2: sort by one attribute, find the rule
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
                      "%s is round. It has no straight sides. The others have 6 straight sides. They are hexagons."))
    its.append(rule_q([flat("tri_eq", 0, 0.7, 0), flat("tri_right", 40, 0.55, 3), flat("tri_thin", 0, 0.5, 1), flat("tri_tall", 180, 0.5, 2)],
                      "a row of shapes in one group", "3 sides", ["same colour", "same size", "4 sides"],
                      "The colours and sizes are different. Every shape has 3 sides. The rule is 3 sides."))
    its.append(rule_q([flat("circle", 0, 0.45, 2), flat("circle", 0, 0.8, 4), flat("circle", 0, 0.6, 0), flat("oval", 0, 0.6, 3)],
                      "a row of shapes in one group", "no corners", ["same colour", "same size", "3 corners"],
                      "The colours and sizes are different. No shape has a corner. The rule is no corners."))
    its.append(rule_q([flat("square", 0, 0.6, 1), flat("rect", 0, 0.55, 1), flat("square", 45, 0.55, 4), flat("rect_long", 90, 0.45, 2)],
                      "a row of shapes in one group", "4 sides", ["same colour", "3 sides", "6 sides"],
                      "Some are squares and some are rectangles. Every shape has 4 sides. The rule is 4 sides."))
    its.append(rule_q([flat("circle", 0, 0.55, 2), flat("tri_eq", 0, 0.65, 2), flat("square", 0, 0.65, 2), flat("hex", 0, 0.6, 2)],
                      "a row of shapes in one group", "same colour", ["3 sides", "no corners", "same shape"],
                      "The shapes are all different. They are all yellow. The rule is same colour."))
    its.append(rule_q([sphere_cv(0.55), cylinder_cv(0.5, lying=True), cone_cv(0.5, "side"), ball_cv(0.5)],
                      "a row of 3D objects in one group", "they can roll", ["they have a point", "they are flat", "only flat faces"],
                      "Each one has a curved part. Each one can roll. The rule is they can roll.",
                      ask="These objects are in one group. What is the sorting rule?"))
    its.append(rule_q([pic3d("cube", 0.6), pic3d("rp_flat", 0.5), pic3d("pyr", 0.55), pic3d("tp", 0.5)],
                      "a row of 3D objects in one group", "only flat faces", ["they can roll", "they have a point", "they are spheres"],
                      "None of them has a curved part. Every face is flat. The rule is only flat faces. "
                      "Only the pyramid has a point.",
                      ask="These objects are in one group. What is the sorting rule?"))
    n, he, his = P.next()
    sort_fig = two([flat("tri_eq", 0, 0.7, 0), flat("square", 0, 0.65, 1)], ["3 sides", "4 sides"], "two groups: 3 sides and 4 sides", gap=50)
    its.append(mcq(sort_fig + "%s sorts shapes into 2 groups. Where does a square go?" % n, "4 sides",
                   ["3 sides", "both groups", "neither group"],
                   "A square has 4 sides. It goes in the 4 sides group."))
    n, he, his = P.next()
    its.append(mcq(sort_fig + "%s uses the same 2 groups. Where does a circle go?" % n, "neither group",
                   ["3 sides", "4 sides", "both groups"],
                   "A circle has no straight sides. It does not go in either group."))
    n, he, his = P.next()
    its.append(mcq(two([flat("tri_eq", 0, 0.7, 3), flat("circle", 0, 0.75, 1)], ["straight sides", "curved"],
                       "two groups: straight sides and curved", gap=40)
                   + "%s sorts shapes into 2 groups. Where does a hexagon go?" % n, "straight sides",
                   ["curved", "both groups", "neither group"],
                   "A hexagon has 6 straight sides. It goes in the straight sides group."))
    n, he, his = P.next()
    roll_fig = two([ball_cv(0.6), cereal_cv(34)], ["rolls", "does not roll"], "two groups: rolls and does not roll", gap=40)
    its.append(mcq(roll_fig + "%s sorts objects. Where does a number cube go?" % n, "does not roll",
                   ["rolls", "both groups", "neither group"],
                   "A number cube has only flat faces. It slides. It does not roll."))
    n, he, his = P.next()
    its.append(mcq(roll_fig + "%s uses the same 2 groups. Where does a soup can go?" % n, "rolls",
                   ["does not roll", "both groups", "neither group"],
                   "A soup can has a curved side. Lay it down and it rolls."))
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
    row3 = [flat("hex", 0, 0.55, 4), flat("pent", 0, 0.55, 1), flat("hex_flat", 0, 0.6, 2),
            flat("square", 0, 0.6, 3), flat("hex_wide", 0, 0.5, 0), flat("circle", 0, 0.55, 2)]
    its.append(row_count_q(row3, "hexagons", 3, 6,
                           "Count the sides of each shape. 3 shapes have 6 sides. The shape with 5 sides is not a hexagon."))
    its.append(mcq(two([flat("square", 0, 0.75, 0), flat("square", 45, 0.75, 0)], ["", ""], "two shapes")
                   + "Are these the same shape?", "Yes, both squares", ["No, one is a diamond", "No, one is bigger", "No, one has 3 sides"],
                   "The second one is turned onto a corner. It still has 4 sides the same length. Both are squares."))
    assert len(its) == 20, len(its)
    return {"title": "Sort by one attribute: find the rule", "items": its}


# ------------------------------------------------------------ set 3: name 3D objects
WRONG3 = {CUBE: ["square", SPH, CYL],             # never "prism": a cube is a special prism
          PRISM: ["rectangle", PYR, CUBE],
          "tprism": ["triangle", PYR, CONE],
          PYR: ["triangle", PRISM, CONE],
          CYL: ["circle", CONE, SPH],
          CONE: [CYL, "triangle", PYR],
          SPH: ["circle", CYL, CONE]}
E3 = {
    CUBE: "It is solid. All its faces are squares of the same size. It is a cube. A square is flat.",
    PRISM: "It has flat faces. Both ends are the same shape. It is a prism. A rectangle is flat.",
    "tprism": "Both ends are the same triangle. The other faces are rectangles. It is a prism, not a pyramid.",
    PYR: "It has a flat bottom. Its triangle faces meet at a point at the top. It is a pyramid.",
    CYL: "It has a flat circle at each end and a curved side. It is a cylinder.",
    CONE: "It has 1 flat circle and a point. It is a cone. A triangle is flat.",
    SPH: "It is round all over, like a ball. It is a sphere. A circle is flat.",
}
TURN3 = {"cube_turned": " It is turned. It is still a cube.",
         "pyr_turned": " It is turned. It is still a pyramid.",
         "cyl_lying": " It is lying on its side. It is still a cylinder.",
         "cone_down": " It is upside down. It is still a cone."}


def set_objects(rnd, pos):
    its = []
    asks = ["What 3D object is this?", "Name this 3D object.", "What is this 3D object called?"]
    plan = ["cube", "cube_turned", "rp_flat", "tp", "pyr", "pyr_turned", "cyl", "cyl_lying", "cone_down", "sphere"]
    for i, k in enumerate(plan):
        kind = KIND[k]
        wk = "tprism" if k == "tp" else kind
        its.append(mcq(fig(pic3d(k).svg("a 3D object")) + asks[i % 3], kind, WRONG3[wk], E3[wk] + TURN3.get(k, "")))
    lab = "four objects labelled A to D"
    its.append(grid_q(pos, "Which one is a sphere?", sphere_cv(0.95),
                      [flat("circle", 0, 1.0, 0), pic3d("cyl_lying", 0.6), pic3d("cube", 0.75)],
                      "%s is round all over, like a ball. It is a sphere. The circle is flat, so it is not a sphere.", lab))
    its.append(grid_q(pos, "Which one is a pyramid?", pic3d("pyr_turned", 0.8),
                      [pic3d("tp_turned", 0.75), flat("tri_eq", 0, 0.95, 2), pic3d("cone", 0.8)],
                      "%s has triangle faces that meet at a point. It is a pyramid. The prism has a triangle at both ends. "
                      "The triangle is flat. The cone has a curved side.", lab))
    for cv, name, kind, e in [
            (ball_cv(), "a beach ball", SPH, "A ball is round all over. It is a sphere. A circle is flat."),
            (dice_cv(), "a number cube", CUBE, "It has 6 square faces, all the same size. It is a cube. A square is just one flat face."),
            (can_cv(), "a soup can", CYL, "A soup can has a flat circle at the top and the bottom. Its side is curved. It is a cylinder."),
            (puck_cv(1.2), "a hockey puck", CYL, "A hockey puck has a flat circle on the top and the bottom. Its side is curved. "
                                                 "It is a short cylinder."),
            (pylon_cv(), "a pylon", CONE, "A pylon has a round bottom and a point at the top. It is a cone."),
            (icecream_cv(), "an ice-cream cone", CONE, "It has a circle at the top and a point at the bottom. It is a cone."),
            (cereal_cv(), "a cereal box", PRISM, "A cereal box has 6 flat faces. They are rectangles. It is a prism."),
            (tent_cv(), "a tent", PRISM, "Both ends of the tent are the same triangle. It is a prism. A pyramid has only 1 point at the top."),
    ]:
        wk = "tprism" if name == "a tent" else kind
        its.append(mcq(fig(cv.svg(name)) + "This is %s. What 3D object is it?" % name, kind, WRONG3[wk], e))
    assert len(its) == 20, len(its)
    return {"title": "Name 3D objects around us", "items": its}


# ------------------------------------------------------------ set 4: flat faces you can trace
def set_faces(rnd, pos, P):
    its = []
    ask = "What shape is the yellow face?"
    for view, want, right, wrong, e in [
            ("cube", "front", "square", ["cube", "triangle", "circle"],
             "The yellow face has 4 sides the same length. It is a square. The whole object is a cube."),
            ("rp_flat", "front", "rectangle", ["prism", "square", "triangle"],
             "The yellow face has 2 long sides and 2 short sides. It is a rectangle."),
            ("pyr", "tri", "triangle", ["pyramid", "square", "circle"],
             "The yellow face has 3 sides. It is a triangle. The whole object is a pyramid."),
            ("tp", "tri", "triangle", ["prism", "rectangle", "circle"],
             "The yellow face at the end has 3 sides. It is a triangle."),
            ("tp", "quad", "rectangle", ["triangle", "prism", "circle"],
             "The yellow face has 4 sides and 4 square corners. It is a rectangle."),
    ]:
        hi = hi_face(view, want)
        its.append(mcq(fig(pic3d(view, 1.0, hi=hi).svg("a 3D object with one face in yellow")) + ask, right, wrong, e))
    its.append(mcq(fig(cylinder_cv(1.0, top=YEL).svg("a cylinder with its top face in yellow")) + ask, "circle",
                   ["oval", "cylinder", "sphere"],
                   "We see the top from the side, so it looks stretched. Trace it and you get a circle."))
    its.append(mcq(fig(cone_cv(1.0, "down", top=YEL).svg("a cone with its flat face in yellow")) + ask, "circle",
                   ["oval", "cone", "triangle"],
                   "The flat face of a cone is round. Trace it and you get a circle."))
    for cv, label, q, right, wrong, e in [
            (can_cv(0.8), "a soup can", "%s traces the bottom of a soup can. What shape does %s draw?", "a circle",
             ["a cylinder", "a square", "a sphere"], "The bottom of a soup can is a flat circle. %s draws a circle."),
            (dice_cv(42), "a number cube", "%s traces one face of a number cube. What shape does %s draw?", "a square",
             ["a cube", "a circle", "a triangle"], "A number cube is a cube. Each face is a flat square. %s draws a square."),
            (cereal_cv(40), "a cereal box", "%s traces the front of a cereal box. What shape does %s draw?", "a rectangle",
             ["a square", "a prism", "a triangle"], "The front has 2 long sides and 2 short sides. %s draws a rectangle."),
            (tent_cv(42), "a tent", "%s traces the front end of a tent. What shape does %s draw?", "a triangle",
             ["a rectangle", "a pyramid", "a square"], "The front end of the tent has 3 sides. %s draws a triangle."),
    ]:
        n, he, his = P.next()
        its.append(mcq(fig(cv.svg(label)) + q % (n, he), right, wrong, e % n))
    its.append(mcq(fig(pic3d("cyl", 0.9).svg("a cylinder")) + "How many flat faces does a cylinder have?", 2, [1, 0, 3],
                   "There is a flat circle on the top. There is one on the bottom. 1 + 1 = 2. The side is curved."))
    its.append(mcq(fig(pic3d("cone", 0.9).svg("a cone")) + "How many flat faces does a cone have?", 1, [0, 2, 3],
                   "A cone has 1 flat circle at the bottom. The rest is curved."))
    its.append(mcq(fig(pic3d("sphere", 0.9).svg("a sphere")) + "How many flat faces does a sphere have?", 0, [1, 2, 3],
                   "A sphere is curved all over. It has no flat faces: 0."))
    its.append(mcq(fig(pic3d("cube", 0.9).svg("a cube")) + "How many faces does a cube have?", 6, [3, 4, 8],
                   "You can see 3 faces. 3 more are at the back, on the side and under it. 3 + 3 = 6."))
    lab = "four objects labelled A to D"
    its.append(grid_q(pos, "Which object has a triangle face?", pic3d("pyr", 0.8),
                      [pic3d("cube", 0.75), pic3d("cyl", 0.8), pic3d("sphere", 0.9)],
                      "%s is a pyramid. Its side faces are triangles. The cube has squares. The cylinder has circles.", lab))
    its.append(grid_q(pos, "Which object has no flat faces?", pic3d("sphere", 0.9),
                      [pic3d("cyl_lying", 0.6), pic3d("cone", 0.8), pic3d("cube_small", 1.0)],
                      "%s is a sphere. It is curved all over. The others have at least 1 flat face.", lab))
    its.append(grid_q(pos, "Which object has 1 circle face and a point?", pic3d("cone_down", 0.8),
                      [pic3d("cyl", 0.8), pic3d("pyr", 0.8), pic3d("sphere", 0.9)],
                      "%s is a cone. It has 1 flat circle and a point. The cylinder has 2 circles and no point.", lab))
    n, he, his = P.next()
    its.append(mcq(fig(flat("tri_eq", 0, 0.8, 4).svg("a triangle print")) + "%s dips one face of a block in paint. "
                   "%s stamps this shape. Which block did %s use?" % (n, he.capitalize(), he),
                   "a pyramid", ["a cube", "a cylinder", "a sphere"],
                   "The print is a triangle. A pyramid has triangle faces. A cube makes squares. A cylinder makes circles."))
    n, he, his = P.next()
    its.append(mcq(fig(flat("circle", 0, 0.8, 1).svg("a circle print")) + "%s dips one face of a block in paint. "
                   "%s stamps this shape. Which block did %s use?" % (n, he.capitalize(), he),
                   "a cylinder", ["a cube", "a pyramid", "a sphere"],
                   "The print is a circle. The end of a cylinder is a flat circle. A sphere has no flat face to stamp."))
    assert len(its) == 20, len(its)
    return {"title": "Flat faces you can trace", "items": its}


# ------------------------------------------------------------ set 5: matching halves
YES = "Yes, they match"
NO_BIG = "No, one half is bigger"
ANY = "Yes, any line makes halves"
NONE = "No, it has no halves"


def set_halves(rnd, pos, P):
    its = []
    ask = "Fold on the dashed line. Do the 2 halves match?"
    hp = heart_pts(0.9)
    cases = [
        (H_SQ, vline(H_SQ, mid_x(H_SQ)), 2, "a square", False,
         "The line is in the middle. Fold it and the 2 halves land on each other. They match."),
        (H_TRI, vline(H_TRI, mid_x(H_TRI)), 3, "a triangle", False,
         "The line goes from the top corner to the middle of the bottom. The 2 halves match."),
        (hp, vline(hp, 0), 3, "a heart", True,
         "The line goes down the middle of the heart. The left half and the right half match."),
        (H_RECT, vline(H_RECT, 34), 1, "a rectangle", False,
         "The line is not in the middle. The right part is bigger. The halves do not match."),
        (circle_pts(44), hline(circle_pts(44), 18), 0, "a circle", True,
         "The line is low. The top part is much bigger. The parts do not match."),
        (H_HOUSE, vline(H_HOUSE, 26), 4, "a house shape", False,
         "The line is not under the top point. The right part is bigger. The halves do not match."),
    ]
    for pts, (a, b), c, name, curved, e in cases:
        ok = halves_match(pts, a, b)
        right = YES if ok else NO_BIG
        wrong = [NO_BIG, NONE, "No, the line must go across"] if ok else [YES, ANY, NONE]
        its.append(mcq(fig(cut_cv(pts, a, b, c, curved).svg("%s with a dashed line" % name)) + ask, right, wrong, e))
    assert [halves_match(p, *l) for p, l, *_ in cases] == [True, True, True, False, False, False]
    # which line makes matching halves (A-D)
    n, he, his = P.next()
    sq = H_SQ
    lines = [(vline(sq, 40), True), (vline(sq, 22), False), (hline(sq, 60), False), (vline(sq, 58), False)]
    good = [l for l, ok in lines if ok][0]
    bad = [l for l, ok in lines if not ok]
    assert halves_match(sq, *good) and not any(halves_match(sq, *l) for l in bad)
    its.append(grid_q(pos, "%s cuts a square piece of toast. Which cut makes matching halves?" % n,
                      cut_cv(sq, *good, c=2, k=0.85), [cut_cv(sq, *l, c=2, k=0.85) for l in bad],
                      "%s cuts right down the middle. The 2 pieces are the same. The other cuts make a big piece and a small piece.",
                      "four squares with dashed lines labelled A to D"))
    tri = H_TRI
    good = vline(tri, 45)
    bad = [vline(tri, 25), hline(tri, 50), vline(tri, 66)]
    assert halves_match(tri, *good) and not any(halves_match(tri, *l) for l in bad)
    its.append(grid_q(pos, "Which line makes matching halves?", cut_cv(tri, *good, c=4, k=0.75), [cut_cv(tri, *l, c=4, k=0.75) for l in bad],
                      "%s goes from the top corner straight down the middle. The 2 halves match.",
                      "four triangles with dashed lines labelled A to D"))
    # which shape is cut into matching halves
    hx = H_HEX
    good_hex = vline(hx, 0)
    bad_cells = [(H_RECT, hline(H_RECT, 18)), (H_TRI_R, vline(H_TRI_R, 50)), (H_HOUSE, hline(H_HOUSE, 40))]
    assert halves_match(hx, *good_hex) and not any(halves_match(p, *l) for p, l in bad_cells)
    its.append(grid_q(pos, "Which shape is cut into matching halves?", cut_cv(hx, *good_hex, c=0, k=0.8),
                      [cut_cv(p, *l, c=0, k=0.7) for p, l in bad_cells],
                      "%s is a hexagon cut from corner to corner, down the middle. The 2 halves match.",
                      "four shapes with dashed lines labelled A to D"))
    good_rect = hline(H_RECT, 32)
    bad_cells = [(H_SQ, vline(H_SQ, 20)), (H_TRI, hline(H_TRI, 60)), (circle_pts(40), vline(circle_pts(40), 16))]
    assert halves_match(H_RECT, *good_rect) and not any(halves_match(p, *l) for p, l in bad_cells)
    its.append(grid_q(pos, "Which shape is cut into matching halves?", cut_cv(H_RECT, *good_rect, c=1, k=0.6),
                      [cut_cv(p, *l, c=1, curved=(len(p) > 20), k=0.75) for p, l in bad_cells],
                      "%s is a rectangle cut across the middle. The top half and the bottom half match.",
                      "four shapes with dashed lines labelled A to D"))
    # which half matches
    for key, wk, q, why in [
            ("house", "cup", "%s draws half a house. Which piece makes matching halves?",
             "%s is the same half, flipped over the line. A slid piece faces the wrong way. A smaller piece does not match."),
            ("tree", "rocket", "%s draws half a tree. Which piece makes matching halves?",
             "%s is the same half, flipped like in a mirror. It is the same size. It faces the other way."),
            ("rocket", "tree", "%s draws half a rocket. Which piece makes matching halves?",
             "%s is the same half, flipped over the line. Same size, same shape, facing the other way."),
    ]:
        n, he, his = P.next()
        its.append(half_pick_q(pos, q % n, key, wk, why))
    # put 2 halves together
    n, he, his = P.next()
    semis = pieces_cv([ellipse(0, -5, 40, 40, 180, 360, 36), ellipse(0, 5, 40, 40, 0, 180, 36)], c=3)
    its.append(mcq(fig(semis.svg("two half circles")) + "%s puts these 2 halves together. What shape does %s make?" % (n, he),
                   "a circle", ["an oval", "a sphere", "a triangle"],
                   "Each piece is half of a circle. Push them together. They make a whole circle."))
    n, he, his = P.next()
    trap1 = [(-46, 0), (46, 0), (23, -40), (-23, -40)]
    trap2 = [(-46, 8), (46, 8), (23, 48), (-23, 48)]
    its.append(mcq(fig(pieces_cv([trap1, trap2], c=2).svg("two matching halves of a shape")) +
                   "%s puts these 2 halves together. What shape does %s make?" % (n, he),
                   "a hexagon", ["an octagon", "a rectangle", "a triangle"],
                   "Put the long sides together. Count the sides around the outside: 6. It is a hexagon."))
    n, he, his = P.next()
    t1 = [(0, 0), (70, 0), (70, 70)]
    t2 = [(-8, 8), (-8, 78), (62, 78)]
    its.append(mcq(fig(pieces_cv([t1, t2], c=0).svg("two matching triangles")) +
                   "%s puts these 2 triangles together. What shape does %s make?" % (n, he),
                   "a square", ["a triangle", "a hexagon", "a cube"],
                   "Put the long sides together. The new shape has 4 sides the same length. It is a square."))
    # word problems
    n, he, his = P.next()
    its.append(mcq(fig(butterfly_cv(3).svg("a butterfly with 3 spots on the left wings")) +
                   "%s paints a butterfly with matching halves. How many spots go on the right side?" % n, 3, [6, 2, 4],
                   "Matching halves look the same. The left side has 3 spots. So the right side has 3 spots."))
    n, he, his = P.next()
    its.append(mcq(fig(butterfly_cv(4).svg("a butterfly with 4 spots on the left wings")) +
                   "%s paints 4 spots on one side of a butterfly. Then %s paints the other side to match. How many spots in all?" % (n, he), 8, [4, 6, 9],
                   "The left side has 4 spots. The right side gets 4 too. 4 + 4 = 8."))
    n, he, his = P.next()
    cells = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0, 2)]
    its.append(mcq(fig(blocks_cv(cells).svg("6 blocks on the left of a dashed line")) +
                   "%s builds a block wall with matching halves. This is the left half. How many blocks in all?" % n,
                   12, [6, 8, 10],
                   "The left half has 6 blocks. The right half needs 6 too. 6 + 6 = 12."))
    n, he, his = P.next()
    da, db = (-10, -10), (90, 90)
    assert halves_match(H_SQ, da, db)
    its.append(mcq(fig(cut_cv(H_SQ, da, db, c=2).svg("a square paper with a dashed line from corner to corner")) +
                   "%s folds a square paper on the line. The halves match. What shape is each half?" % n,
                   "a triangle", ["a square", "a rectangle", "a circle"],
                   "The fold goes from corner to corner. Each half has 3 sides. Each half is a triangle."))
    assert len(its) == 20, len(its)
    return {"title": "Matching halves: fold, build and solve", "items": its}


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
    sortf = row_svg([flat("tri_eq", 0, 0.6, 0), flat("tri_right", 30, 0.5, 3), flat("tri_thin", 0, 0.45, 1),
                     flat("tri_tall", 180, 0.45, 2)], ["", "", "", ""], "four triangles of different colours and sizes", gap=18)
    solids1 = row_svg([pic3d("cube", 0.75), pic3d("rp_flat", 0.6), pic3d("pyr", 0.7)], ["cube", "prism", "pyramid"],
                      "cube, prism and pyramid", gap=30, fs=15)
    solids2 = row_svg([pic3d("cyl", 0.75), pic3d("cone", 0.75), sphere_cv(0.8)], ["cylinder", "cone", "sphere"],
                      "cylinder, cone and sphere", gap=30, fs=15)
    objs = row_svg([ball_cv(0.7), dice_cv(36), can_cv(0.7), pylon_cv(0.7)], ["ball", "number cube", "soup can", "pylon"],
                   "a ball, a number cube, a soup can and a pylon", gap=24, fs=15)
    trace = row_svg([can_cv(0.7), flat("circle", 0, 0.7, 3), dice_cv(36), flat("square", 0, 0.65, 2)],
                    ["soup can", "trace: circle", "number cube", "trace: square"],
                    "a soup can and the circle it traces; a number cube and the square it traces", gap=22, fs=15)
    hp = heart_pts(0.8)
    halves = row_svg([cut_cv(hp, *vline(hp, 0), c=3, curved=True), cut_cv(H_SQ, *vline(H_SQ, 40), c=2), cut_cv(H_RECT, *vline(H_RECT, 34), c=1)],
                     ["match", "match", "do not match"],
                     "a heart and a square cut into matching halves; a rectangle cut into halves that do not match", gap=30, fs=15)
    pairs = row_svg([flat("circle", 0, 0.8, 0), sphere_cv(0.8), flat("square", 0, 0.75, 0), pic3d("cube", 0.75)],
                    ["circle (2D)", "sphere (3D)", "square (2D)", "cube (3D)"],
                    "a flat circle next to a sphere, and a flat square next to a cube", gap=22, fs=15)
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
        "<h2>Sort and find the rule</h2>"
        "<p>To sort, look at <b>one thing</b> at a time: the number of sides, corners or no corners, colour, size, "
        "or if an object can roll. The <b>sorting rule</b> tells what is the same in a group.</p>"
        "<figure class='sn-fig'>" + sortf +
        "<figcaption>The colours and sizes are different. All have 3 sides. The rule is “3 sides”.</figcaption></figure>" +
        ex("Example 2", "A group has a ball, a soup can and a cone. What is the rule?",
           "Each one has a curved part. Each one can roll.", "they can roll") +
        "<h2>3D objects are solid</h2>"
        "<p>A 3D object is <b>solid</b>. You can pick it up and hold it. Dashed lines show the back.</p>"
        "<figure class='sn-fig'>" + solids1 + "</figure>"
        "<figure class='sn-fig'>" + solids2 + "</figure>" +
        table(["Object", "Look for"], [
            ["Cube", "6 flat square faces, all the same size."],
            ["Prism", "Flat faces. Both ends are the same shape."],
            ["Pyramid", "Triangle faces that meet at a point."],
            ["Cylinder", "A flat circle at each end and a curved side."],
            ["Cone", "1 flat circle and a point."],
            ["Sphere", "Round all over, like a ball."]]) +
        "<figure class='sn-fig'>" + objs +
        "<figcaption>A ball is a sphere. A number cube is a cube. A soup can is a cylinder. A pylon is a cone.</figcaption></figure>"
        "<h2>Flat faces you can trace</h2>"
        "<p>A <b>face</b> is a flat part of a 3D object. Trace around a face and you get a 2D shape.</p>"
        "<figure class='sn-fig'>" + trace + "</figure>" +
        ex("Example 3", "What shape do you get when you trace the bottom of a soup can?",
           "The bottom of the can is flat and round.", "a circle") +
        "<h2>Matching halves</h2>"
        "<p>Fold a shape on a line. If the 2 halves land exactly on each other, they are <b>matching halves</b>. "
        "A line that is not in the middle makes a big part and a small part.</p>"
        "<figure class='sn-fig'>" + halves + "</figure>" +
        ex("Example 4", "A butterfly has matching halves. The left wing has 3 spots. How many spots are on the right wing?",
           "Matching halves look the same, like in a mirror.", "3 spots") +
        "<h2>Common mistakes</h2>"
        "<figure class='sn-fig'>" + pairs + "</figure>" +
        table(["Mistake", "What to do instead"], [
            ["Calling a turned square a “diamond”", "Count the sides. 4 sides the same length make a square, any way up."],
            ["Calling a ball a circle", "A circle is flat. A ball is round all over: it is a sphere."],
            ["Calling a number cube a square", "A square is flat. A number cube is solid: it is a cube."],
            ["Mixing up a prism and a pyramid", "A pyramid comes to a point. A prism has the same shape at both ends."],
            ["Sorting by colour when the rule is sides", "Look at one thing at a time. Check that every shape follows the rule."],
            ["Thinking any line makes matching halves", "Fold it. The 2 halves must land exactly on each other."],
        ])
    )


FAQ = [
    {"q": "What shapes do Grade 1 students learn in Ontario math?",
     "a": "In Spatial Sense, Grade 1 students sort 2D shapes and 3D objects by one attribute at a time and name the sorting rule, "
          "find 2D shapes in 3D objects, and make shapes with matching halves. They name circles, triangles, squares, rectangles "
          "and hexagons, and cubes, prisms, pyramids, cylinders, cones and spheres."},
    {"q": "What is the difference between a 2D shape and a 3D object?",
     "a": "A 2D shape is flat, like a drawing on paper. A 3D object is solid and you can hold it, like a ball (a sphere) or a soup can (a cylinder)."},
    {"q": "What does “matching halves” mean in Grade 1?",
     "a": "A shape has matching halves when you fold it on a line and the two halves land exactly on each other, like a heart or a butterfly. "
          "This is the start of learning about symmetry."},
    {"q": "How can I help my Grade 1 child learn shapes at home?",
     "a": "Go on a shape hunt: find a ball (sphere), a soup can (cylinder), a cereal box (prism) and a number cube (cube). "
          "Trace their flat faces, sort the objects by what rolls, and fold paper cut-outs to look for matching halves."},
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
    rnd = random.Random(41811)
    P = People(rnd)
    sets = [set_name2d(rnd, Pos(rnd)), set_sort(rnd, Pos(rnd), P), set_objects(rnd, Pos(rnd)),
            set_faces(rnd, Pos(rnd), P), set_halves(rnd, Pos(rnd), P)]
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
            if right == CUBE:                             # a cube is a special prism
                assert PRISM not in it["c"], it["q"][-80:]
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-1", "slug": "2d-shapes-and-3d-objects", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "2D Shapes and 3D Objects: Name, Sort and Find Matching Halves",
        "seo_title": "Grade 1 Math 2D Shapes and 3D Objects Worksheets: Sorting Rules, Faces and Matching Halves (Free, Answer Key)",
        "short_title": "2D shapes and 3D objects",
        "domain": "Spatial Sense",
        "standard_code": "Grade 1: E1.1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Sort three-dimensional objects and two-dimensional shapes according to one attribute at a time, "
                         "and identify the sorting rule being used",
        "meta_desc": "Free Grade 1 math worksheets on 2D shapes and 3D objects for the Ontario curriculum: name circles, triangles, "
                     "squares, rectangles and hexagons, sort by one attribute and find the rule, name cubes, prisms, pyramids, "
                     "cylinders, cones and spheres, trace flat faces and find matching halves. 100 questions with an answer key.",
        "key_big": "Look at one thing at a time: sides, corners, flat or curved. Turning never changes the name.",
        "key_sub": "A square on its corner is still a square. A ball is a sphere, not a circle. "
                   "Trace a flat face of a 3D object to get a 2D shape. Matching halves land exactly on each other when you fold.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(four (shapes|objects|squares|triangles)|half a shape|a row of|two |a (circle|square|rectangle|cylinder|ball|tin) and a)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
