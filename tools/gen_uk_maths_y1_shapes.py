# -*- coding: utf-8 -*-
"""
UK Year 1 Maths: 2-D and 3-D shapes (National Curriculum in England, Geometry – properties of shapes)
  python3 tools/gen_uk_maths_y1_shapes.py
HTML attributes use single quotes (no backslashes in the JSON). British English.

Year 1 recognises and names common shapes:
  2-D  circle, triangle, square, rectangle (rectangles include squares)
  3-D  cube, cuboid (cuboids include cubes), sphere, cylinder, cone, pyramid
Only light counting of sides and corners. Very short sentences, a picture in almost every question.

Rules kept everywhere (so every answer is right for every definition):
  - a square picture never has "rectangle" as a wrong answer, and a cube never has "cuboid"
  - "Which is NOT a ..." pictures never use rectangles/cuboids with a square/cube as the odd one out
  - colour, size and turning never change the name
Pictures are drawn from their corner points (checked: right number of sides, no crossing sides,
squares really square) and 3-D shapes from 3-D vertices and faces (V − E + F = 2), with hidden edges dashed.
Wrong answers come from real pupil mistakes: a turned square called a diamond, a rectangle called a square,
circle vs sphere, square vs cube, triangle vs pyramid or cone, cube vs cuboid, cylinder vs cone.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL, SIDE, TOP3 = "#cfe6d6", "#a9d3b6", "#e6f2e9"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
FONT = "Arial, Helvetica, sans-serif"
# (fill, line) pairs for flat shapes: colour must never matter
COLS = [("#cfe6d6", "#006633"), ("#cfe0f3", "#1f5f99"), ("#fbe7a6", "#8a6100"),
        ("#f6cfd8", "#a33b5a"), ("#e2d6f0", "#5b3f8c")]
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
                st = " stroke='%s' stroke-width='%g' stroke-linejoin='round'" % (e[4], e[3]) if e[3] else ""
                s.append("<polygon points='%s' fill='%s'%s/>"
                         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in e[1]), e[2], st))
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
    """Pictures side by side (bottoms in line when there are captions, else centred), a caption under each."""
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


# ------------------------------------------------------------ 2-D shapes
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
}
KIND2D = {"tri_eq": "triangle", "tri_right": "triangle", "tri_thin": "triangle", "tri_tall": "triangle",
          "square": "square", "rect": "rectangle", "rect_long": "rectangle"}
for _k, _p in SHAPES2D.items():
    check_poly(_p)
    assert len(_p) == {"triangle": 3, "square": 4, "rectangle": 4}[KIND2D[_k]]
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
                col = "#ffd84d" if fi == hi else top if n[1] > 0.5 else side if n[0] > 0.3 else front
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


VIEWS = {
    "cube": (lambda: box(1.1, 1.1, 1.1), 30, 22),
    "cube_turned": (lambda: box(1.1, 1.1, 1.1), 50, 30),
    "cube_small": (lambda: box(0.7, 0.7, 0.7), -25, 22),
    "cuboid_flat": (lambda: box(1.9, 0.8, 1.0), 25, 22),
    "cuboid_tall": (lambda: box(0.8, 1.8, 0.7), 35, 18),
    "cuboid_turned": (lambda: box(1.6, 1.0, 0.8), -35, 24),
    "pyr": (lambda: pyramid(), 25, 18),
    "pyr_turned": (lambda: pyramid(1.2, 1.5), -30, 25),
}
VIEW_KIND = {"cube": CUBE, "cube_turned": CUBE, "cube_small": CUBE, "cuboid_flat": CUBOID, "cuboid_tall": CUBOID,
             "cuboid_turned": CUBOID, "pyr": PYR, "pyr_turned": PYR}


def solid_cv(view, k=50, hi=None):
    f, yaw, pitch = VIEWS[view]
    return f().cv(k, yaw, pitch, hi=hi)


def _rot90(pts, on):
    return [(-y, x) for x, y in pts] if on else pts


def cylinder_cv(s=1.0, lying=False, body=FILL, top=TOP3, line=GREEN, dashed=True, band=None):
    rx, ry, h = 36 * s, 11 * s, 72 * s
    R = lambda p: _rot90(p, lying)
    cv = Canvas()
    cv.poly(R(ellipse(0, 0, rx, ry, 180, 360) + ellipse(0, h, rx, ry, 0, 180)), body, 0)
    if band:                                          # a paper label round the side (tin)
        y1, y2, col = h * 0.25, h * 0.75, band
        cv.poly(R(ellipse(0, y1, rx, ry, 0, 180) + ellipse(0, y2, rx, ry, 180, 0)), col, 0)
    cv.poly(R(ellipse(0, 0, rx, ry, 0, 360)[:-1]), top, 2.4, line)
    cv.pline(R([(-rx, 0), (-rx, h)]), col=line)
    cv.pline(R([(rx, 0), (rx, h)]), col=line)
    cv.pline(R(ellipse(0, h, rx, ry, 0, 180)), col=line)
    if dashed:
        cv.pline(R(ellipse(0, h, rx, ry, 180, 360)), dashed=True, sw=1.6, col=line)
    return cv


def cone_cv(s=1.0, how="up", body=FILL, line=GREEN, dashed=True, dots=None):
    """how: 'up' (point at the top), 'down' (point at the bottom), 'side' (lying down)."""
    rx, ry, h = 38 * s, 11 * s, 80 * s
    cv = Canvas()
    if how == "down":
        cv.poly([(0, h)] + ellipse(0, 0, rx, ry, 0, 180), body, 0)
        cv.pline([(-rx, 0), (0, h), (rx, 0)], col=line)
        cv.poly(ellipse(0, 0, rx, ry, 0, 360)[:-1], TOP3, 2.4, line)
        return cv
    R = lambda p: _rot90(p, how == "side")
    cv.poly(R([(0, 0)] + ellipse(0, h, rx, ry, 180, 0)), body, 0)
    cv.poly(R([(0, 0)] + ellipse(0, h, rx, ry, 0, 180)), body, 0)
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
    """Any 3-D picture by key. s scales it (1.0 = full size for one picture)."""
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


def tin_cv(s=1.0):
    return cylinder_cv(s, body="#c9ced6", top="#e4e7ec", line="#4a5260", dashed=False, band="#2e86c1")


def tent_cv(k=50):
    S = pyramid(1.5, 1.1)
    cv = S.cv(k, 40, 16, cols=("#f5b041", "#e67e22", "#f39c12"), dashed=False, line="#8a4b08")
    side = [fi for fi in range(1, 5) if cv.vis[fi]]
    fi = min(side, key=lambda f: cv.nrm[f][2])        # the face that looks most at us
    i, j, top = S.f[fi]
    A, B, T = cv.P(cv.pts[i]), cv.P(cv.pts[j]), cv.P(cv.pts[top])
    m = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
    L = lambda p, q, t: (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
    cv.poly([L(m, A, 0.32), L(m, B, 0.32), L(m, T, 0.5)], "#7a3e06", 0)
    return cv


def hat_cv(s=1.0):
    return cone_cv(s, body="#b39ddb", line="#5b3f8c", dashed=False, dots="#ffd84d")


OBJ = {"ball": ball_cv, "orange": orange_cv, "dice": dice_cv, "cereal": cereal_cv, "tin": tin_cv, "tent": tent_cv, "hat": hat_cv}


def art(n):
    return "an" if n[0] in "aeiou" else "a"


def grid_q(pos, q, right, others, why, label="four shapes labelled A to D"):
    """A-D picture question. why has %s for the letter."""
    p = pos.next()
    cells = list(others)
    cells.insert(p, right)
    L = "ABCD"[p]
    return mcq_fixed(fig(grid_svg(cells, label)) + q, list("ABCD"), L, why % L)


# ------------------------------------------------------------ set 1: name 2-D shapes
WRONG2 = {
    "circle": ["oval", "sphere", "square"],
    "triangle": ["pyramid", "square", "rectangle"],
    "square": ["diamond", "triangle", "cube"],          # never "rectangle": a square is a special rectangle
    "rectangle": ["square", "triangle", "cuboid"],
}
E2 = {
    "circle": "It is flat and round. It has no corners. It is a circle.",
    "triangle": "It has 3 straight sides and 3 corners. It is a triangle.",
    "square": "It has 4 sides that are all the same length and 4 square corners. It is a square.",
    "rectangle": "It has 4 sides and 4 square corners. 2 sides are long and 2 are short. It is a rectangle.",
}


def set_name2d(rnd, pos):
    its = []
    asks = ["What is this shape called?", "Name this shape.", "What shape is this?"]
    plan = [  # key, turn, scale, colour, note
        ("circle", 0, 1.0, 1, ""),
        ("circle", 0, 0.5, 2, " It is small, but it is still a circle."),
        ("tri_eq", 0, 1.0, 0, ""),
        ("tri_eq", 180, 0.8, 3, " It is upside down, but it is still a triangle."),
        ("tri_right", 30, 1.0, 4, " It is turned, but it is still a triangle."),
        ("tri_thin", 0, 0.9, 2, " A long, thin triangle is still a triangle."),
        ("square", 0, 1.0, 3, ""),
        ("square", 0, 0.5, 1, " It is small, but it is still a square."),
        ("square", 45, 0.9, 4, " It is standing on a corner. Some people say “diamond”, but it is still a square."),
        ("square", 20, 1.0, 0, " It is turned, but it is still a square."),
        ("rect", 0, 1.0, 2, ""),
        ("rect", 90, 0.9, 1, " It is standing up, but it is still a rectangle."),
        ("rect_long", 25, 0.9, 3, " It is tilted, but it is still a rectangle."),
        ("rect", 0, 0.5, 4, " It is small, but it is still a rectangle. It is not a square: 2 sides are longer."),
    ]
    for i, (key, deg, s, c, note) in enumerate(plan):
        kind = "circle" if key == "circle" else KIND2D[key]
        e = E2[kind] + note
        its.append(mcq(fig(flat(key, deg, s, c).svg("a flat shape")) + asks[i % 3], kind, WRONG2[kind], e))
    # light counting of sides
    its.append(mcq(fig(flat("tri_right", 200, 0.9, 1).svg("a flat shape")) + "How many sides does this shape have?", 3, [2, 4, 6],
                   "Put your finger on one side. Count each side once: 3 sides. It is a triangle."))
    its.append(mcq(fig(flat("square", 45, 0.8, 2).svg("a flat shape")) + "How many sides does this shape have?", 4, [3, 5, 2],
                   "Count each side once: 4 sides. It is a square on its corner."))
    its.append(mcq(fig(flat("rect", 0, 0.9, 0).svg("a flat shape")) + "How many corners does this shape have?", 4, [2, 3, 5],
                   "Count each corner once: 4 corners. Do not forget the corners at the bottom."))
    its.append(mcq(fig(flat("circle", 0, 0.8, 3).svg("a flat shape")) + "How many corners does a circle have?", 0, [1, 2, 4],
                   "A circle is round all the way round. It has no corners at all: 0."))
    its.append(grid_q(pos, "Which shape is a triangle?", flat("tri_tall", 180, 0.9, 1),
                      [flat("square", 0, 0.9, 2), flat("rect", 90, 0.8, 0), flat("circle", 0, 0.95, 4)],
                      "%s has 3 straight sides. It points down, but it is still a triangle."))
    its.append(grid_q(pos, "Which shape is a circle?", flat("circle", 0, 1.0, 2),
                      [flat("oval", 0, 0.85, 1), flat("tri_eq", 0, 0.9, 3), flat("square", 45, 0.9, 0)],
                      "%s is perfectly round. The oval is stretched, so it is not a circle."))
    assert len(its) == 20, len(its)
    return {"title": "Name 2-D shapes", "items": its}


# ------------------------------------------------------------ set 2: same shape, different look
def row_count_q(cells, kind_word, n, total, e, label="a row of shapes"):
    q = fig(row_svg(cells, [""] * len(cells), label, gap=14)) + "How many %s can you see?" % kind_word
    return mcq(q, n, [n - 1, n + 1, total], e)


def set_same(rnd, pos, P):
    its = []
    its.append(grid_q(pos, "Which shape is NOT a triangle?", flat("square", 0, 0.9, 2),
                      [flat("tri_eq", 180, 0.8, 0), flat("tri_thin", 20, 0.65, 3), flat("tri_right", 0, 0.5, 1)],
                      "%s has 4 sides, so it is a square. The others all have 3 sides. They are triangles in different sizes, colours and turns."))
    its.append(grid_q(pos, "Which shape is NOT a triangle?", flat("rect", 90, 0.8, 4),
                      [flat("tri_tall", 0, 0.9, 1), flat("tri_eq", 90, 0.85, 2), flat("tri_right", 135, 0.7, 0)],
                      "%s has 4 sides. It is a rectangle. Every triangle has 3 sides, whichever way it points."))
    its.append(grid_q(pos, "Which shape is NOT a square?", flat("rect", 0, 0.75, 1),
                      [flat("square", 45, 0.85, 3), flat("square", 0, 0.5, 0), flat("square", 15, 0.95, 4)],
                      "%s has 2 long sides and 2 short sides. It is a rectangle, not a square. A square has 4 sides the same length, even when it is turned."))
    its.append(grid_q(pos, "Which shape is NOT a circle?", flat("oval", 0, 0.85, 3),
                      [flat("circle", 0, 0.6, 1), flat("circle", 0, 1.1, 0), flat("circle", 0, 0.85, 4)],
                      "%s is stretched. It is an oval. A circle is perfectly round, big or small."))
    its.append(grid_q(pos, "Which shape is a square?", flat("square", 45, 0.85, 0),
                      [flat("rect", 0, 0.75, 2), flat("tri_eq", 0, 0.9, 1), flat("rect_long", 90, 0.75, 3)],
                      "%s has 4 sides the same length. It is standing on a corner, but it is a square. The other 4-sided shapes have long and short sides."))
    its.append(mcq(fig(flat("square", 45, 0.95, 1).svg("a flat shape")) + "Is this a square?", "Yes, it is just turned",
                   ["No, it is a diamond", "No, it has 3 sides", "No, it is too big"],
                   "It has 4 sides the same length and 4 square corners. Turning a square does not change it. “Diamond” is not its maths name."))
    its.append(mcq(fig(flat("tri_eq", 180, 0.55, 4).svg("a flat shape")) + "Is this a triangle?", "Yes, it has 3 sides",
                   ["No, it is upside down", "No, it is too small", "No, it has 4 sides"],
                   "It has 3 straight sides, so it is a triangle. Small or upside down, it is still a triangle."))
    its.append(mcq(fig(flat("rect", 0, 0.9, 2).svg("a flat shape")) + "Is this a square?", "No, 2 sides are longer",
                   ["Yes, it has 4 sides", "Yes, it has 4 corners", "No, it has 3 sides"],
                   "It has 4 sides, but 2 are long and 2 are short. A square has 4 sides the same length. This is a rectangle."))
    its.append(mcq(fig(row_svg([flat("tri_eq", 0, 1.0, 0), flat("tri_eq", 180, 0.5, 3)], ["", ""], "a big shape and a small shape", gap=40))
                   + "What is different about these 2 triangles?", "size and turn",
                   ["number of sides", "number of corners", "one is not a triangle"],
                   "Both have 3 sides and 3 corners. Only the size and the turn are different. They are both triangles."))
    # count one kind in a row (turned and small ones count too)
    row1 = [flat("tri_eq", 0, 0.6, 0), flat("square", 0, 0.6, 1), flat("tri_right", 160, 0.55, 2),
            flat("circle", 0, 0.6, 3), flat("tri_thin", 40, 0.45, 4), flat("rect", 0, 0.55, 2)]
    its.append(row_count_q(row1, "triangles", 3, 6,
                           "Look for 3 straight sides. There are 3 triangles. The turned and thin ones count too."))
    row2 = [flat("square", 45, 0.6, 2), flat("rect", 0, 0.55, 0), flat("square", 0, 0.45, 4),
            flat("tri_eq", 0, 0.6, 1), flat("square", 20, 0.65, 3), flat("circle", 0, 0.55, 0), flat("square", 0, 0.7, 1)]
    its.append(row_count_q(row2, "squares", 4, 7,
                           "Look for 4 sides the same length. There are 4 squares. The squares on their corners count too. The long shape is a rectangle."))
    row3 = [flat("circle", 0, 0.45, 4), flat("oval", 0, 0.6, 1), flat("circle", 0, 0.75, 2),
            flat("square", 0, 0.6, 3), flat("circle", 0, 0.55, 0), flat("tri_eq", 180, 0.6, 2)]
    its.append(row_count_q(row3, "circles", 3, 6,
                           "Look for shapes that are perfectly round. There are 3 circles. The stretched shape is an oval."))
    row4 = [flat("rect", 0, 0.55, 3), flat("tri_eq", 0, 0.6, 0), flat("rect_long", 90, 0.5, 1),
            flat("circle", 0, 0.55, 4), flat("rect", 30, 0.5, 2), flat("tri_right", 0, 0.55, 3)]
    its.append(row_count_q(row4, "rectangles", 3, 6,
                           "Look for 4 sides and 4 square corners. There are 3 rectangles: one lies flat, one stands up and one is tilted."))
    n, he, his = P.next()
    its.append(mcq("%s colours a triangle red. What shape is it now?" % n, "a triangle",
                   ["a square", "a new shape", "a circle"],
                   "Colour does not change a shape. It still has 3 sides. It is still a triangle."))
    n, he, his = P.next()
    its.append(mcq("%s turns a square onto its corner. What shape is it now?" % n, "a square",
                   ["a diamond", "a triangle", "a circle"],
                   "Turning does not change a shape. It still has 4 sides the same length. It is still a square."))
    a, b = P.next(), P.next()
    its.append(mcq("%s draws a big circle. %s draws a small circle. Are they both circles?" % (a[0], b[0]), "Yes, both",
                   ["Only the big one", "Only the small one", "No, neither"],
                   "Both are flat and perfectly round. Size does not change the name."))
    its.append(mcq("What does every triangle have?", "3 straight sides",
                   ["a point at the top", "3 sides the same", "a flat bottom"],
                   "Every triangle has 3 straight sides and 3 corners. It can point any way. Its sides can be different lengths."))
    its.append(mcq("What does every square have?", "4 sides the same length",
                   ["a flat bottom", "3 corners", "2 long sides"],
                   "A square has 4 sides that are all the same length and 4 square corners. It can be turned any way."))
    its.append(mcq("Which one can change the name of a shape?", "the number of sides",
                   ["its colour", "its size", "turning it"],
                   "The name comes from the sides and corners. Colour, size and turning never change the name."))
    its.append(mcq("A shape has 4 sides. 2 are long and 2 are short. It has 4 square corners. What is it?", "a rectangle",
                   ["a square", "a triangle", "a circle"],
                   "4 sides and 4 square corners with long and short sides: a rectangle. A square has all 4 sides the same."))
    assert len(its) == 20, len(its)
    return {"title": "Same shape, any size, colour or turn", "items": its}


# ------------------------------------------------------------ set 3: name 3-D shapes
WRONG3 = {CUBE: ["square", PYR, CYL],                   # never "cuboid": a cube is a special cuboid
          CUBOID: [CUBE, "rectangle", CYL],
          PYR: ["triangle", CONE, CUBE],
          CYL: [CONE, "circle", CUBOID],
          CONE: [CYL, "triangle", PYR],
          SPH: ["circle", CYL, CONE]}
E3 = {
    CUBE: "It is solid. All its faces are squares of the same size. It is a cube.",
    CUBOID: "It is solid, like a box. Some faces are long rectangles, so it is not a cube. It is a cuboid.",
    PYR: "It has a square at the bottom and triangle faces that meet at a point. It is a pyramid.",
    CYL: "It has a flat circle at each end and a curved side. It is a cylinder.",
    CONE: "It has 1 flat circle and comes to a point. It is a cone.",
    SPH: "It is round all over, like a ball. It is a sphere. A circle is flat.",
}
TURN3 = {"cube_turned": " It is turned, but it is still a cube.",
         "cube_small": " It is small, but it is still a cube.",
         "cuboid_tall": " It is standing on its end, but it is still a cuboid.",
         "cuboid_turned": " It is turned, but it is still a cuboid.",
         "pyr_turned": " It is turned, but it is still a pyramid.",
         "cyl_lying": " It is lying on its side, but it is still a cylinder.",
         "cone_down": " It is upside down, but it is still a cone.",
         "cone_side": " It is lying on its side, but it is still a cone."}


def set_name3d(rnd, pos):
    its = []
    asks = ["What is this 3-D shape called?", "Name this 3-D shape.", "What 3-D shape is this?"]
    keys = ["cube", "cube_turned", "cube_small", "cuboid_flat", "cuboid_tall", "cuboid_turned", "pyr", "pyr_turned",
            "cyl", "cyl_lying", "cone", "cone_down", "cone_side", "sphere"]
    for i, k in enumerate(keys):
        kind = KIND[k]
        its.append(mcq(fig(pic3d(k).svg("a 3-D shape")) + asks[i % 3], kind, WRONG3[kind], E3[kind] + TURN3.get(k, "")))
    its.append(grid_q(pos, "Which one is a sphere?", sphere_cv(0.95),
                      [pic3d("cyl_lying", 0.6), pic3d("cone", 0.8), pic3d("cube", 0.75)],
                      "%s is round all over, like a ball. It is a sphere. The cylinder and cone have flat circle faces.",
                      "four 3-D shapes labelled A to D"))
    its.append(grid_q(pos, "Which one is a cuboid?", pic3d("cuboid_flat", 0.65),
                      [pic3d("cyl", 0.8), pic3d("pyr", 0.75), pic3d("sphere", 0.9)],
                      "%s is shaped like a box with long rectangle faces. It is a cuboid.", "four 3-D shapes labelled A to D"))
    its.append(grid_q(pos, "Which one is a cube?", pic3d("cube_turned", 0.7),
                      [pic3d("cuboid_flat", 0.65), pic3d("cuboid_tall", 0.55), pic3d("pyr", 0.75)],
                      "%s has square faces that are all the same size. It is a cube. The 2 boxes with long faces are cuboids.",
                      "four 3-D shapes labelled A to D"))
    its.append(grid_q(pos, "Which one is a cone?", pic3d("cone_down", 0.85),
                      [pic3d("pyr_turned", 0.65), pic3d("cyl", 0.8), pic3d("cube_small", 1.0)],
                      "%s has 1 flat circle and a point. It is a cone, upside down. The pyramid has a point too, but its bottom is a square.",
                      "four 3-D shapes labelled A to D"))
    its.append(mcq("I am round all over. I can roll any way. What am I?", SPH, ["circle", CYL, CUBE],
                   "A shape that is round all over, like a ball, is a sphere."))
    its.append(mcq("I have 2 flat circles and a curved side. What am I?", CYL, [CONE, SPH, "circle"],
                   "A cylinder has a flat circle at each end and a curved side. A cone has only 1 circle."))
    assert len(its) == 20, len(its)
    return {"title": "Name 3-D shapes", "items": its}


# ------------------------------------------------------------ set 4: 2-D or 3-D?
def set_flat_solid(rnd, pos):
    its = []
    # flat shapes are drawn in the same green as the solids, so colour never gives the answer away
    its.append(grid_q(pos, "Which shape is 3-D (solid)?", pic3d("cube", 0.75),
                      [flat("square", 0, 0.9, 0), flat("circle", 0, 0.95, 0), flat("tri_eq", 0, 0.9, 0)],
                      "%s is a cube. It is solid, so it is 3-D. The others are flat 2-D shapes."))
    its.append(grid_q(pos, "Which shape is 3-D (solid)?", sphere_cv(0.95),
                      [flat("circle", 0, 1.0, 0), flat("rect", 0, 0.75, 0), flat("square", 45, 0.85, 0)],
                      "%s is a sphere. It is round all over, like a ball, so it is 3-D. The circle is flat."))
    its.append(grid_q(pos, "Which shape is 3-D (solid)?", pic3d("pyr", 0.75),
                      [flat("tri_eq", 0, 0.95, 0), flat("tri_right", 0, 0.9, 0), flat("square", 0, 0.9, 0)],
                      "%s is a pyramid. It is solid, so it is 3-D. The triangles and the square are flat."))
    its.append(grid_q(pos, "Which shape is 2-D (flat)?", flat("circle", 0, 1.0, 0),
                      [pic3d("sphere", 0.95), pic3d("cyl", 0.8), pic3d("cone", 0.8)],
                      "%s is a circle. It is flat, so it is 2-D. The others are solid 3-D shapes."))
    its.append(grid_q(pos, "Which shape is 2-D (flat)?", flat("rect", 0, 0.75, 0),
                      [pic3d("cuboid_flat", 0.65), pic3d("cube", 0.75), pic3d("cyl_lying", 0.6)],
                      "%s is a rectangle. It is flat, so it is 2-D. The cuboid looks like a rectangle from the front, but it is solid."))
    its.append(grid_q(pos, "Which shape is 2-D (flat)?", flat("tri_eq", 0, 0.95, 0),
                      [pic3d("pyr", 0.75), pic3d("cone", 0.8), pic3d("cuboid_tall", 0.55)],
                      "%s is a triangle. It is flat, so it is 2-D. The pyramid and the cone are solid."))
    # 2-D name vs 3-D name, side by side
    its.append(grid_q(pos, "Which one is a circle?", flat("circle", 0, 0.95, 0),
                      [pic3d("sphere", 0.95), pic3d("cyl", 0.8), pic3d("cone", 0.8)],
                      "%s is flat and round: a circle. The sphere is round too, but it is solid."))
    its.append(grid_q(pos, "Which one is a sphere?", pic3d("sphere", 0.95),
                      [flat("circle", 0, 1.0, 0), flat("oval", 0, 0.85, 0), pic3d("cyl", 0.8)],
                      "%s is round all over, like a ball: a sphere. The circle is flat, so it is not a sphere."))
    its.append(grid_q(pos, "Which one is a square?", flat("square", 0, 0.9, 0),
                      [pic3d("cube", 0.75), pic3d("pyr", 0.75), flat("tri_eq", 0, 0.9, 0)],
                      "%s is a flat square. The cube has square faces, but it is solid, so it is a cube."))
    its.append(grid_q(pos, "Which one is a cube?", pic3d("cube", 0.75),
                      [flat("square", 0, 0.9, 0), flat("square", 45, 0.85, 0), pic3d("cyl", 0.8)],
                      "%s is solid with square faces: a cube. The squares are flat."))
    its.append(grid_q(pos, "Which one is a triangle?", flat("tri_eq", 0, 0.95, 0),
                      [pic3d("pyr", 0.75), pic3d("cone", 0.8), flat("square", 0, 0.9, 0)],
                      "%s is a flat triangle. The pyramid and the cone are solid 3-D shapes."))
    # count the 3-D shapes in a row
    rowa = [flat("circle", 0, 0.55, 0), pic3d("cube", 0.55), flat("tri_eq", 0, 0.55, 0), pic3d("cyl", 0.6),
            pic3d("sphere", 0.6), flat("square", 0, 0.55, 0)]
    its.append(mcq(fig(row_svg(rowa, [""] * 6, "a row of shapes", gap=14)) + "How many 3-D shapes can you see?", 3, [2, 4, 6],
                   "The cube, the cylinder and the sphere are solid: 3 shapes. The circle, the triangle and the square are flat."))
    rowb = [pic3d("cone", 0.55), flat("rect", 0, 0.5, 0), pic3d("cuboid_flat", 0.45), pic3d("pyr", 0.5),
            flat("circle", 0, 0.5, 0), pic3d("sphere", 0.55)]
    its.append(mcq(fig(row_svg(rowb, [""] * 6, "a row of shapes", gap=14)) + "How many 3-D shapes can you see?", 4, [3, 5, 2],
                   "The cone, the cuboid, the pyramid and the sphere are solid: 4 shapes. The rectangle and the circle are flat."))
    rowc = [pic3d("cube", 0.5), flat("tri_eq", 180, 0.5, 0), pic3d("cyl_lying", 0.45), flat("square", 45, 0.5, 0),
            pic3d("cone_side", 0.45)]
    its.append(mcq(fig(row_svg(rowc, [""] * 5, "a row of shapes", gap=14)) + "How many flat 2-D shapes can you see?", 2, [3, 1, 5],
                   "The triangle and the square are flat: 2 shapes. The cube, the cylinder and the cone are solid."))
    # flat faces of solids: draw round them
    its.append(mcq(fig(pic3d("cube", 1.0, hi=0).svg("a cube with one face coloured")) + "You draw round the yellow face. What shape do you draw?",
                   "a square", ["a cube", "a triangle", "a circle"],
                   "Each face of a cube is a flat square. You draw a square. The cube itself is 3-D."))
    its.append(mcq(fig(pic3d("cuboid_flat", 1.0, hi=0).svg("a cuboid with one face coloured")) + "You draw round the yellow face. What shape do you draw?",
                   "a rectangle", ["a square", "a cuboid", "a triangle"],
                   "The yellow face has 2 long sides and 2 short sides. It is a rectangle."))
    its.append(mcq(fig(cylinder_cv(1.0).svg("a cylinder")) + "You stand this cylinder on paper. You draw round the bottom. What shape do you draw?",
                   "a circle", ["a cylinder", "an oval", "a square"],
                   "The flat ends of a cylinder are circles. You draw a circle. In the picture it looks squashed because we see it from the side."))
    its.append(mcq(fig(pic3d("pyr", 1.0).svg("a pyramid")) + "You stand this pyramid on paper. You draw round the bottom. What shape do you draw?",
                   "a square", ["a triangle", "a pyramid", "a circle"],
                   "The bottom of this pyramid is a flat square. The sides are triangles, but you draw round the bottom."))
    its.append(mcq(fig(cone_cv(1.0).svg("a cone")) + "You stand this cone on paper. You draw round the bottom. What shape do you draw?",
                   "a circle", ["a triangle", "a cone", "a square"],
                   "The bottom of a cone is a flat circle. A cone looks like a triangle from the side, but it has no triangle faces."))
    its.append(mcq("Which one is a flat 2-D shape?", "a circle", ["a sphere", "a cube", "a cone"],
                   "A circle is flat, like a drawing on paper. A sphere, a cube and a cone are solid. You can hold them."))
    assert len(its) == 20, len(its)
    return {"title": "2-D or 3-D? Flat or solid", "items": its}


# ------------------------------------------------------------ set 5: shapes all around us
def set_world(rnd, pos, P):
    its = []
    ask = "What 3-D shape is it?"
    for obj, name, kind, e in [
            ("ball", "a beach ball", SPH, "A ball is round all over. It is a sphere. A circle is flat."),
            ("orange", "an orange", SPH, "An orange is round all over, like a ball. It is a sphere."),
            ("dice", "a dice", CUBE, "A dice has 6 square faces, all the same size. It is a cube. A square is only one flat face."),
            ("tin", "a tin of beans", CYL, "A tin has a flat circle at the top and the bottom and a curved side. It is a cylinder."),
            ("cereal", "a cereal box", CUBOID, "A cereal box has big faces and thin faces. It is not a cube. It is a cuboid."),
            ("tent", "a tent", PYR, "This tent has a square bottom and triangle sides that meet at a point. It is shaped like a pyramid."),
            ("hat", "a party hat", CONE, "A party hat has a round bottom and a point at the top. It is a cone."),
    ]:
        cv = OBJ[obj]()
        its.append(mcq(fig(cv.svg(name)) + "This is %s. %s" % (name, ask), kind, WRONG3[kind], e))
    for name, kind, wrong, e in [
            ("a marble", SPH, ["circle", CYL, CONE], "A marble is round all over. It is a sphere."),
            ("an ice-cream cone", CONE, [CYL, "triangle", PYR], "It has a circle at the top and a point at the bottom. It is a cone."),
            ("a book", CUBOID, [CUBE, "rectangle", CYL], "A book has 6 flat faces. Some are long and some are thin. It is a cuboid."),
    ]:
        its.append(mcq("What 3-D shape is %s?" % name, kind, wrong, e))
    n, he, his = P.next()
    its.append(mcq("%s has a ball, a dice and a tin. Which one is a sphere?" % n, "the ball",
                   ["the dice", "the tin", "none of them"],
                   "The ball is round all over, so it is a sphere. The dice is a cube and the tin is a cylinder."))
    n, he, his = P.next()
    its.append(mcq("%s wants a shape that rolls. Which one should %s pick?" % (n, he), "a tin",
                   ["a dice", "a book", "a cereal box"],
                   "A tin is a cylinder. It has a curved side, so it rolls. The others have only flat faces."))
    n, he, his = P.next()
    its.append(mcq("%s builds a tall tower. Which shape stacks best?" % n, "a cube",
                   ["a sphere", "a cone", "a pyramid"],
                   "A cube has flat faces on the top and bottom, so cubes stack well. A sphere rolls off. A cone and a pyramid have a point."))
    n, he, his = P.next()
    its.append(mcq("%s draws round a coin. What shape does %s draw?" % (n, he), "a circle",
                   ["a sphere", "a cylinder", "a square"],
                   "A coin has a flat round face. Drawing round it makes a flat circle."))
    n, he, his = P.next()
    its.append(mcq("%s cuts a square sandwich from corner to corner. What shape is each piece?" % n, "a triangle",
                   ["a square", "a rectangle", "a circle"],
                   "The cut makes 2 pieces. Each piece has 3 sides. Each piece is a triangle."))
    n, he, his = P.next()
    its.append(mcq("%s looks at a door. It has 2 long sides and 2 short sides. What shape is the front of the door?" % n,
                   "a rectangle", ["a square", "a triangle", "a cube"],
                   "4 sides with 2 long and 2 short, and square corners: a rectangle."))
    n, he, his = P.next()
    its.append(mcq("%s draws 2 triangles. How many sides are there in total?" % n, 6, [3, 5, 4],
                   "Each triangle has 3 sides. 3 + 3 = 6 sides."))
    n, he, his = P.next()
    its.append(mcq("%s draws a square and a triangle. How many corners are there in total?" % n, 7, [6, 8, 2],
                   "A square has 4 corners. A triangle has 3 corners. 4 + 3 = 7 corners."))
    n, he, his = P.next()
    its.append(mcq("%s looks at %s dice. What flat shape is each face?" % (n, his), "a square",
                   ["a cube", "a circle", "a triangle"],
                   "A dice is a cube. Each face of a cube is a flat square."))
    n, he, his = P.next()
    its.append(mcq("%s sees a shape with a square bottom and a point at the top. What is it?" % n, "a pyramid",
                   ["a cone", "a cube", "a triangle"],
                   "A square at the bottom and triangle faces that meet at a point: a pyramid. A cone has a circle at the bottom."))
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
    flat4 = row_svg([flat("circle", 0, 0.9, 1), flat("tri_eq", 0, 0.9, 0), flat("square", 0, 0.9, 2), flat("rect", 0, 0.8, 3)],
                    ["circle", "triangle", "square", "rectangle"], "circle, triangle, square and rectangle", gap=26, fs=15)
    turned = row_svg([flat("square", 0, 0.8, 2), flat("square", 45, 0.75, 4), flat("tri_eq", 0, 0.8, 0), flat("tri_eq", 180, 0.5, 1)],
                     ["square", "still a square", "triangle", "still a triangle"],
                     "a square and the same square turned; a big triangle and a small upside-down triangle", gap=26, fs=15)
    solids1 = row_svg([pic3d("cube", 0.85), pic3d("cuboid_flat", 0.8), pic3d("pyr", 0.85)], ["cube", "cuboid", "pyramid"],
                      "cube, cuboid and pyramid", gap=36, fs=15)
    solids2 = row_svg([sphere_cv(0.9), cylinder_cv(0.85), cone_cv(0.85)], ["sphere", "cylinder", "cone"],
                      "sphere, cylinder and cone", gap=40, fs=15)
    pairs = row_svg([flat("circle", 0, 0.85, 1), sphere_cv(0.85), flat("square", 0, 0.8, 2), pic3d("cube", 0.8)],
                    ["circle (2-D)", "sphere (3-D)", "square (2-D)", "cube (3-D)"],
                    "a flat circle next to a sphere, and a flat square next to a cube", gap=22, fs=15)
    objs = row_svg([ball_cv(0.8), dice_cv(40), tin_cv(0.8), cereal_cv(36), tent_cv(40), hat_cv(0.8)],
                   ["ball", "dice", "tin", "cereal box", "tent", "party hat"],
                   "a ball, a dice, a tin, a cereal box, a tent and a party hat", gap=18, fs=14)
    return (
        "<h2>2-D shapes are flat</h2>"
        "<p>A 2-D shape is <b>flat</b>, like a drawing on paper. Look at the <b>sides</b> and the <b>corners</b> to name it.</p>"
        "<figure class='sn-fig'>" + flat4 + "</figure>" +
        table(["Shape", "What to look for"], [
            ["Circle", "Round. No sides and no corners."],
            ["Triangle", "3 straight sides and 3 corners."],
            ["Square", "4 sides, all the same length. 4 square corners."],
            ["Rectangle", "4 sides: 2 long and 2 short. 4 square corners."]]) +
        "<p>A square is a special rectangle: all its sides are the same length.</p>"
        "<p>Size, colour and turning do not change the name.</p>"
        "<figure class='sn-fig'>" + turned +
        "<figcaption>A square on its corner is still a square, not a “diamond”.</figcaption></figure>" +
        ex("Example 1", "A shape has 3 straight sides. It points down. What is it?",
           "Count the sides: 3. It does not matter which way it points.", "a triangle") +
        "<h2>3-D shapes are solid</h2>"
        "<p>A 3-D shape is <b>solid</b>. You can pick it up and hold it. Dashed lines show the back of the shape.</p>"
        "<figure class='sn-fig'>" + solids1 + "</figure>"
        "<figure class='sn-fig'>" + solids2 + "</figure>" +
        table(["Shape", "What to look for"], [
            ["Cube", "6 square faces, all the same size."],
            ["Cuboid", "Like a box. Some faces are long rectangles."],
            ["Pyramid", "A flat bottom and triangle faces that meet at a point."],
            ["Sphere", "Round all over, like a ball."],
            ["Cylinder", "A flat circle at each end and a curved side."],
            ["Cone", "1 flat circle and a point."]]) +
        "<h2>2-D or 3-D?</h2>"
        "<p>Some 2-D and 3-D shapes look alike in a picture. Ask: is it flat, or can I hold it?</p>"
        "<figure class='sn-fig'>" + pairs + "</figure>" +
        ex("Example 2", "You draw round one face of a dice. What shape do you draw?",
           "A dice is a cube. Each face of a cube is a flat square.", "a square") +
        "<h2>Shapes all around us</h2>"
        "<figure class='sn-fig'>" + objs +
        "<figcaption>A ball is a sphere. A dice is a cube. A tin is a cylinder. A cereal box is a cuboid. "
        "This tent is a pyramid. A party hat is a cone.</figcaption></figure>" +
        ex("Example 3", "Which one rolls: a tin or a cereal box?",
           "A tin is a cylinder with a curved side. A cereal box has only flat faces.", "the tin") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Calling a turned square a “diamond”", "Count the sides. 4 sides the same length make a square, any way up."],
            ["Calling a rectangle a square", "Check the sides. If 2 sides are longer, it is not a square. It is a rectangle."],
            ["Calling a ball a circle", "A circle is flat. A ball is round all over: it is a sphere."],
            ["Calling a dice a square", "A square is flat. A dice is solid: it is a cube."],
            ["Mixing up a cube and a cuboid", "A cube has all faces the same square. A cuboid has some long faces."],
            ["Mixing up a cylinder and a cone", "A cylinder has 2 flat circles. A cone has 1 circle and a point."],
        ])
    )


FAQ = [
    {"q": "What shapes does a Year 1 child need to know?",
     "a": "In Year 1, children recognise and name 2-D shapes (circle, triangle, square and rectangle) and 3-D shapes (cube, cuboid, pyramid, sphere, cylinder and cone)."},
    {"q": "What is the difference between a 2-D and a 3-D shape?",
     "a": "A 2-D shape is flat, like a drawing on paper. A 3-D shape is solid and you can hold it, like a ball or a box."},
    {"q": "Is a square a rectangle?",
     "a": "Yes. A rectangle has 4 sides and 4 square corners, and a square is a special rectangle with all 4 sides the same length. The National Curriculum says “rectangles (including squares)”."},
    {"q": "How can I help my child learn shapes at home?",
     "a": "Go on a shape hunt: find a ball (sphere), a tin (cylinder), a cereal box (cuboid) and a dice (cube). Draw round their flat faces to see the 2-D shapes."},
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
    """Tag pictures that must print larger (A-D choices, rows) so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(1109)
    P = People(rnd)
    sets = []
    for f in (lambda: set_name2d(rnd, Pos(rnd)), lambda: set_same(rnd, Pos(rnd), P), lambda: set_name3d(rnd, Pos(rnd)),
              lambda: set_flat_solid(rnd, Pos(rnd)), lambda: set_world(rnd, Pos(rnd), P)):
        sets.append(f())
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
            # a square / cube picture never has rectangle / cuboid as a wrong answer
            right = it["c"][it["a"]]
            if right in ("square", "a square"):
                assert not any(c in ("rectangle", "a rectangle") for c in it["c"]), it["q"][-80:]
            if right in (CUBE, "a cube"):
                assert not any(c in (CUBOID, "a cuboid") for c in it["c"]), it["q"][-80:]
    u = {
        "country": "uk", "subject": "maths", "grade": "year-1", "slug": "2d-and-3d-shapes", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "2-D and 3-D Shapes: Name and Recognise Shapes",
        "seo_title": "Year 1 2-D and 3-D Shapes Worksheets: Name Flat and Solid Shapes (Free, with Answers)",
        "short_title": "2-D and 3-D shapes",
        "domain": "Geometry – properties of shapes",
        "standard_code": "Year 1: Geometry – properties of shapes",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Recognise and name common 2-D and 3-D shapes, including: 2-D shapes [for example, rectangles (including squares), circles and triangles]; 3-D shapes [for example, cuboids (including cubes), pyramids and spheres].",
        "meta_desc": "Free Year 1 maths worksheets on 2-D and 3-D shapes: name circles, triangles, squares and rectangles in any size, colour or turn, recognise cubes, cuboids, pyramids, spheres, cylinders and cones, tell flat from solid and spot shapes in everyday objects. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "2-D shapes are flat. 3-D shapes are solid.",
        "key_sub": "Count the sides to name a flat shape. Size, colour and turning never change the name: a square on its corner is still a square, and a ball is a sphere, not a circle.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(four (3-D )?shapes labelled A to D|a row of shapes|a big shape and a small shape)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
