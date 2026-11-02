# -*- coding: utf-8 -*-
"""
AU Year 1 Maths: Shapes and objects (Australian Curriculum v9.0, AC9M1SP01)
  python3 tools/gen_au_maths_y1_shapes.py
HTML attributes use single quotes (no backslashes in the JSON). Australian English.

Year 1 makes, compares and classifies familiar shapes and objects:
  2-D shapes   circle, triangle, square, rectangle (a square is a special rectangle)
  3-D objects  cube, sphere, cylinder, cone, and the same objects in the environment
               (a ball, a dice, a tin, an ice-cream cone, a party hat)
Sides and corners, sorting (odd one out), same and different.
Very short sentences, a picture in almost every question.

Rules kept everywhere (so every answer is right for every definition):
  - a square picture never has "rectangle" as a wrong answer; a square is never the odd one out among rectangles
  - colour, size and turning never change the name
Pictures are drawn from their corner points (checked: right number of sides, no crossing sides,
squares really square) and 3-D objects from 3-D vertices and faces (V − E + F = 2), with hidden edges dashed.
Wrong answers come from real student mistakes: a turned square called a diamond, a rectangle called a square,
circle vs sphere, square vs cube, triangle vs cone, cylinder vs cone, counting a side or corner twice or missing one.
Drawing helpers adapted from tools/gen_uk_maths_y1_shapes.py.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL, SIDE, TOP3 = "#cfe6d6", "#a9d3b6", "#e6f2e9"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
FONT = "Arial, Helvetica, sans-serif"
# (fill, line) pairs for flat shapes: colour must never matter
COLS = [("#cfe6d6", "#006633"), ("#cfe0f3", "#1f5f99"), ("#fbe7a6", "#8a6100"),
        ("#f6cfd8", "#a33b5a"), ("#e2d6f0", "#5b3f8c")]
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]

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



# ------------------------------------------------------------ extra pictures for this unit
RED = "#d62828"


def marked(key, deg=0, s=1.0, c=0, side=None, corner=None):
    """A flat shape with one side drawn thick red, or one corner marked with a red dot."""
    pts = tpts(SHAPES2D[key], deg, s)
    check_poly(pts)
    cv = Canvas()
    cv.poly(pts, COLS[c][0], 3, COLS[c][1])
    if side is not None:
        cv.line(pts[side], pts[(side + 1) % len(pts)], sw=7, col=RED)
    if corner is not None:
        cv.circle(pts[corner], 8, fill=RED, sw=0)
    return cv


def cricket_ball_cv(s=1.0):
    r = 36 * s
    cv = Canvas()
    cv.circle((0, 0), r, fill="#b3261e", sw=2.4, col="#6e1410")
    for dx in (-4 * s, 4 * s):
        cv.pline(ellipse(dx, 0, r * 0.25, r * 0.97, -80, 80, 30), sw=1.6, col="#f4e9d8")
    cv.poly(ellipse(-r * 0.45, -r * 0.45, r * 0.16, r * 0.1, 0, 360, 24)[:-1], "#e8796f", 0)
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


def sandwich_cv():
    cv = Canvas()
    cv.poly([(0, 0), (80, 0), (80, 80), (0, 80)], "#f6e3b4", 6, "#b07a2a")
    cv.line((4, 4), (76, 76), dashed=True, sw=2.4, col=INK)
    return cv


def door_cv():
    cv = Canvas()
    cv.poly([(0, 0), (52, 0), (52, 104), (0, 104)], "#c58b52", 3, "#6b4423")
    cv.poly([(8, 8), (44, 8), (44, 44), (8, 44)], "#d9a571", 1.5, "#6b4423")
    cv.circle((43, 60), 4, fill="#f1c40f", sw=1, col="#6b4423")
    return cv


def mcq2(figure, q, correct, cands, e):
    return mcq(figure + q, correct, cands, e)


def two(cvs, caps, label, gap=36):
    return fig(row_svg(cvs, caps, label, gap=gap, fs=15))


# ------------------------------------------------------------ set 1: name 2-D shapes
WRONG2 = {
    "circle": ["oval", "sphere", "square"],
    "triangle": ["cone", "square", "rectangle"],
    "square": ["diamond", "triangle", "cube"],          # never "rectangle": a square is a special rectangle
    "rectangle": ["square", "triangle", "oval"],
}
E2 = {
    "circle": "It is flat and round. It has no corners. It is a circle.",
    "triangle": "It has 3 straight sides and 3 corners. It is a triangle.",
    "square": "It has 4 sides. They are all the same length. It is a square.",
    "rectangle": "It has 4 sides and 4 square corners. 2 sides are long. 2 are short. It is a rectangle.",
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
        ("tri_right", 30, 1.0, 4, " It is turned. It is still a triangle."),
        ("tri_thin", 0, 0.9, 2, " A long, thin triangle is still a triangle."),
        ("tri_tall", 90, 0.8, 1, " It points to the side. It is still a triangle."),
        ("square", 0, 1.0, 3, ""),
        ("square", 0, 0.5, 1, " It is small. It is still a square."),
        ("square", 45, 0.9, 4, " It stands on a corner. Some people say “diamond”. It is still a square."),
        ("square", 20, 1.0, 0, " It is turned. It is still a square."),
        ("rect", 0, 1.0, 2, ""),
        ("rect", 90, 0.9, 1, " It is standing up. It is still a rectangle."),
        ("rect_long", 25, 0.9, 3, " It is tilted. It is still a rectangle."),
        ("rect", 0, 0.5, 4, " It is small. It is not a square, because 2 sides are longer."),
    ]
    for i, (key, deg, s, c, note) in enumerate(plan):
        kind = "circle" if key == "circle" else KIND2D[key]
        its.append(mcq(fig(flat(key, deg, s, c).svg("a flat shape")) + asks[i % 3], kind, WRONG2[kind], E2[kind] + note))
    its.append(grid_q(pos, "Which shape is a triangle?", flat("tri_tall", 180, 0.9, 1),
                      [flat("square", 0, 0.9, 2), flat("rect", 90, 0.8, 0), flat("circle", 0, 0.95, 4)],
                      "%s has 3 straight sides. It points down. It is still a triangle."))
    its.append(grid_q(pos, "Which shape is a circle?", flat("circle", 0, 1.0, 2),
                      [flat("oval", 0, 0.85, 1), flat("tri_eq", 0, 0.9, 3), flat("square", 45, 0.9, 0)],
                      "%s is round all the way. The oval is stretched, so it is not a circle."))
    its.append(grid_q(pos, "Which shape is a square?", flat("square", 45, 0.85, 3),
                      [flat("rect", 0, 0.75, 2), flat("tri_eq", 0, 0.9, 1), flat("circle", 0, 0.9, 0)],
                      "%s has 4 sides the same length. It stands on a corner. It is still a square."))
    its.append(grid_q(pos, "Which shape is a rectangle?", flat("rect_long", 0, 0.75, 4),
                      [flat("tri_right", 0, 0.9, 2), flat("oval", 0, 0.85, 3), flat("circle", 0, 0.8, 1)],
                      "%s has 4 sides and 4 square corners. 2 sides are long. It is a rectangle."))
    assert len(its) == 20, len(its)
    return {"title": "Name 2-D shapes", "items": its}


# ------------------------------------------------------------ set 2: sides and corners
def set_sides(rnd, pos, P):
    its = []
    def cnt(key, deg, s, c, what, n, wrong, e):
        name = "a flat shape"
        q = fig(flat(key, deg, s, c).svg(name)) + "How many %s does this shape have?" % what
        its.append(mcq(q, n, wrong, e))
    cnt("tri_eq", 0, 1.0, 0, "sides", 3, [2, 4, 6],
        "Touch each side once. 1, 2, 3. A triangle has 3 sides.")
    cnt("tri_right", 200, 0.9, 1, "corners", 3, [2, 4, 1],
        "Touch each corner once. 1, 2, 3. A triangle has 3 corners.")
    cnt("square", 0, 0.9, 3, "sides", 4, [3, 5, 8],
        "Count each side once. 1, 2, 3, 4. A square has 4 sides.")
    cnt("square", 45, 0.85, 2, "corners", 4, [3, 2, 5],
        "It stands on a corner. Count all the corners, top and bottom. There are 4.")
    cnt("rect", 0, 0.9, 4, "sides", 4, [2, 3, 6],
        "Count the long sides and the short sides. 2 + 2 = 4 sides.")
    cnt("rect_long", 90, 0.7, 0, "corners", 4, [2, 3, 5],
        "Count each corner once. Do not forget the bottom corners. There are 4.")
    cnt("circle", 0, 0.9, 3, "corners", 0, [1, 2, 4],
        "A circle is round all the way. It has no corners: 0.")
    cnt("tri_thin", 15, 0.85, 4, "sides", 3, [2, 4, 5],
        "It is long and thin. Count the sides: 1, 2, 3. It is a triangle.")
    cnt("tri_tall", 180, 0.8, 2, "corners", 3, [2, 4, 1],
        "It points down. Count the corners: 1, 2, 3.")
    cnt("square", 20, 0.6, 1, "sides", 4, [3, 5, 2],
        "It is small and turned. It still has 4 sides.")
    # what is a side, what is a corner
    its.append(mcq(fig(marked("square", 0, 0.9, 1, side=0).svg("a square with one side in red")) + "What is the red part?",
                   "a side", ["a corner", "the inside", "a circle"],
                   "A side is a straight line on the edge of a shape. The red line is a side."))
    its.append(mcq(fig(marked("tri_eq", 0, 0.95, 0, corner=0).svg("a triangle with one corner marked red")) + "What is the red dot on?",
                   "a corner", ["a side", "the inside", "the middle"],
                   "A corner is where 2 sides meet. The red dot is on a corner."))
    its.append(grid_q(pos, "Which shape has 3 corners?", flat("tri_right", 110, 0.85, 2),
                      [flat("square", 0, 0.85, 1), flat("circle", 0, 0.95, 3), flat("rect", 0, 0.75, 0)],
                      "%s is a triangle. It has 3 corners. The square and the rectangle have 4. The circle has 0."))
    its.append(grid_q(pos, "Which shape has no corners?", flat("circle", 0, 0.95, 4),
                      [flat("tri_eq", 0, 0.9, 0), flat("square", 45, 0.85, 2), flat("rect", 90, 0.75, 1)],
                      "%s is a circle. It is round, so it has no corners."))
    its.append(grid_q(pos, "Which shape has 4 sides all the same length?", flat("square", 0, 0.9, 0),
                      [flat("rect", 0, 0.75, 3), flat("rect_long", 90, 0.7, 1), flat("tri_eq", 0, 0.9, 4)],
                      "%s is a square. All 4 sides are the same. The rectangles have 2 long and 2 short sides."))
    its.append(grid_q(pos, "Which shape has 4 corners?", flat("rect", 0, 0.75, 1),
                      [flat("tri_eq", 180, 0.85, 0), flat("circle", 0, 0.9, 2), flat("oval", 0, 0.85, 4)],
                      "%s is a rectangle. It has 4 corners. The triangle has 3. The circle and oval have none."))
    its.append(mcq(fig(flat("tri_eq", 0, 0.85, 4).svg("a flat shape")) + "I have 3 sides and 3 corners. What am I?",
                   "a triangle", ["a square", "a rectangle", "a circle"],
                   "3 sides and 3 corners make a triangle."))
    its.append(mcq(fig(flat("rect", 90, 0.8, 2).svg("a flat shape")) + "I have 4 sides. 2 are long. 2 are short. What am I?",
                   "a rectangle", ["a square", "a triangle", "a circle"],
                   "4 sides with 2 long and 2 short: a rectangle. A square has 4 sides the same."))
    its.append(mcq(fig(row_svg([flat("square", 0, 0.75, 3), flat("tri_eq", 0, 0.8, 1)], ["square", "triangle"],
                               "a square and a triangle", gap=40, fs=15))
                   + "Which has more corners?", "the square", ["the triangle", "they are the same", "neither"],
                   "The square has 4 corners. The triangle has 3. 4 is more than 3."))
    its.append(mcq(fig(row_svg([flat("rect", 0, 0.6, 0), flat("square", 0, 0.75, 4)], ["rectangle", "square"],
                               "a rectangle and a square", gap=40, fs=15))
                   + "How many corners do they have?", "4 each", ["4 and 3", "2 each", "8 each"],
                   "Count each one. The rectangle has 4 corners. The square has 4 corners."))
    assert len(its) == 20, len(its)
    return {"title": "Sides and corners", "items": its}


# ------------------------------------------------------------ set 3: sort shapes, odd one out
def row_count_q(cells, kind_word, n, total, e):
    q = fig(row_svg(cells, [""] * len(cells), "a row of shapes", gap=14)) + "How many %s can you see?" % kind_word
    return mcq(q, n, [n - 1, n + 1, total], e)


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
    its.append(grid_q(pos, "Which shape is NOT a circle?", flat("oval", 0, 0.85, 3),
                      [flat("circle", 0, 0.6, 1), flat("circle", 0, 1.1, 0), flat("circle", 0, 0.85, 4)],
                      "%s is stretched. It is an oval. A circle is round all the way, big or small."))
    its.append(grid_q(pos, "Which shape is the odd one out?", flat("tri_eq", 0, 0.9, 2),
                      [flat("rect", 0, 0.75, 2), flat("rect_long", 90, 0.7, 0), flat("rect", 30, 0.7, 3)],
                      "%s has 3 sides. The others have 4 sides and 4 square corners. They are rectangles."))
    its.append(grid_q(pos, "Which shape is the odd one out?", flat("rect", 0, 0.75, 0),
                      [flat("square", 0, 0.85, 0), flat("square", 30, 0.8, 1), flat("square", 0, 0.6, 3)],
                      "%s has 2 long sides. It is a rectangle. The other 3 are squares. Colour does not matter."))
    # count one kind in a row
    row1 = [flat("tri_eq", 0, 0.6, 0), flat("square", 0, 0.6, 1), flat("tri_right", 160, 0.55, 2),
            flat("circle", 0, 0.6, 3), flat("tri_thin", 40, 0.45, 4), flat("rect", 0, 0.55, 2)]
    its.append(row_count_q(row1, "triangles", 3, 6,
                           "Look for 3 sides. There are 3 triangles. The turned one and the thin one count too."))
    row2 = [flat("square", 45, 0.6, 2), flat("rect", 0, 0.55, 0), flat("square", 0, 0.45, 4),
            flat("tri_eq", 0, 0.6, 1), flat("square", 20, 0.65, 3), flat("circle", 0, 0.55, 0), flat("square", 0, 0.7, 1)]
    its.append(row_count_q(row2, "squares", 4, 7,
                           "Look for 4 sides the same length. There are 4 squares. The squares on a corner count too. The long one is a rectangle."))
    row3 = [flat("circle", 0, 0.45, 4), flat("oval", 0, 0.6, 1), flat("circle", 0, 0.75, 2),
            flat("square", 0, 0.6, 3), flat("circle", 0, 0.55, 0), flat("tri_eq", 180, 0.6, 2)]
    its.append(row_count_q(row3, "circles", 3, 6,
                           "Look for shapes that are round all the way. There are 3 circles. The stretched one is an oval."))
    row4 = [flat("rect", 0, 0.55, 3), flat("tri_eq", 0, 0.6, 0), flat("rect_long", 90, 0.5, 1),
            flat("circle", 0, 0.55, 4), flat("rect", 30, 0.5, 2), flat("tri_right", 0, 0.55, 3)]
    its.append(row_count_q(row4, "rectangles", 3, 6,
                           "Look for 4 sides and 4 square corners. There are 3 rectangles: flat, standing up and tilted."))
    # what is the sorting rule?
    g1 = [flat("tri_eq", 0, 0.7, 0), flat("tri_right", 40, 0.55, 3), flat("tri_thin", 0, 0.5, 1), flat("tri_tall", 180, 0.5, 2)]
    its.append(mcq(fig(row_svg(g1, [""] * 4, "a row of shapes in one group", gap=18)) + "These shapes are in one group. What is the rule?",
                   "3 sides", ["same colour", "same size", "4 sides"],
                   "The colours and sizes are different. Every shape has 3 sides. The rule is 3 sides."))
    g2 = [flat("circle", 0, 0.45, 2), flat("circle", 0, 0.8, 4), flat("circle", 0, 0.6, 0), flat("oval", 0, 0.6, 3)]
    its.append(mcq(fig(row_svg(g2, [""] * 4, "a row of shapes in one group", gap=18)) + "These shapes are in one group. What is the rule?",
                   "no corners", ["same colour", "same size", "3 corners"],
                   "The colours and sizes are different. No shape has a corner. The rule is no corners."))
    g3 = [flat("square", 0, 0.6, 1), flat("rect", 0, 0.55, 1), flat("square", 45, 0.55, 4), flat("rect_long", 90, 0.45, 2)]
    its.append(mcq(fig(row_svg(g3, [""] * 4, "a row of shapes in one group", gap=18)) + "These shapes are in one group. What is the rule?",
                   "4 sides", ["same colour", "3 sides", "all squares"],
                   "Some are squares and some are rectangles. Every shape has 4 sides. The rule is 4 sides."))
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
    its.append(grid_q(pos, "%s’s group has only shapes with 4 corners. Which shape can go in?" % n,
                      flat("rect", 90, 0.75, 3), [flat("tri_eq", 0, 0.9, 1), flat("circle", 0, 0.9, 0), flat("oval", 0, 0.85, 2)],
                      "%s is a rectangle. It has 4 corners. The others have 3 corners or none."))
    # same and different
    its.append(mcq2(two([flat("tri_eq", 0, 1.0, 1), flat("tri_eq", 0, 0.55, 2)], ["", ""], "two shapes"),
                   "How are these shapes the same?", "both have 3 sides", ["same size", "same colour", "both have 4 sides"],
                   "One is big and one is small. The colours are different. Both have 3 sides. Both are triangles."))
    its.append(mcq2(two([flat("square", 0, 0.8, 3), flat("rect", 0, 0.75, 3)], ["", ""], "two shapes"),
                   "How are these shapes different?", "side lengths", ["number of sides", "number of corners", "colour"],
                   "Both have 4 sides and 4 corners. Both are the same colour. The rectangle has 2 longer sides."))
    its.append(mcq2(two([flat("square", 0, 0.75, 0), flat("square", 45, 0.75, 0)], ["", ""], "two shapes"),
                   "Are these the same shape?", "Yes, both squares", ["No, one is a diamond", "No, one is bigger", "No, one has 3 sides"],
                   "The second one is turned onto a corner. It still has 4 sides the same length. Both are squares."))
    its.append(mcq2(two([flat("tri_eq", 0, 0.8, 4), flat("tri_eq", 180, 0.8, 4)], ["", ""], "two shapes"),
                   "What is different about these triangles?", "the way they point", ["the colour", "the size", "the number of sides"],
                   "They are the same size and colour. Both have 3 sides. One points up and one points down."))
    assert len(its) == 20, len(its)
    return {"title": "Sort shapes: odd one out", "items": its}


# ------------------------------------------------------------ set 4: 3-D objects around us
WRONG3 = {CUBE: ["square", SPH, CYL],
          CYL: [CONE, "rectangle", SPH],
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
    asks = ["What 3-D object is this?", "Name this 3-D object.", "What is this 3-D object called?"]
    plan = [("cube", 1.0), ("cube_turned", 1.0), ("cube_small", 1.0), ("cyl", 1.0), ("cyl_lying", 1.0),
            ("cone", 1.0), ("cone_down", 1.0), ("cone_side", 1.0), ("sphere", 1.0), ("sphere", 0.6)]
    for i, (k, s) in enumerate(plan):
        kind = KIND[k]
        note = " It is small. It is still a sphere." if (k == "sphere" and s < 1) else TURN3.get(k, "")
        its.append(mcq(fig(pic3d(k, s).svg("a 3-D object")) + asks[i % 3], kind, WRONG3[kind], E3[kind] + note))
    lab = "four objects labelled A to D"
    its.append(grid_q(pos, "Which one is a sphere?", sphere_cv(0.95),
                      [flat("circle", 0, 1.0, 0), pic3d("cyl_lying", 0.6), pic3d("cube", 0.75)],
                      "%s is round all over, like a ball. It is a sphere. The circle is flat, so it is not a sphere.", lab))
    its.append(grid_q(pos, "Which one is a cube?", pic3d("cube_turned", 0.7),
                      [flat("square", 0, 0.9, 0), pic3d("cyl", 0.8), pic3d("cone", 0.8)],
                      "%s is solid with square faces. It is a cube. The square is flat.", lab))
    its.append(grid_q(pos, "Which one is a cylinder?", pic3d("cyl_lying", 0.6),
                      [pic3d("cone_side", 0.6), pic3d("sphere", 0.9), pic3d("cube_small", 1.0)],
                      "%s has 2 flat circles and a curved side. It is a cylinder lying down. The cone has only 1 circle.", lab))
    its.append(grid_q(pos, "Which one is a cone?", pic3d("cone_down", 0.85),
                      [pic3d("cyl", 0.8), flat("tri_tall", 0, 0.9, 0), pic3d("sphere", 0.9)],
                      "%s has 1 flat circle and a point. It is a cone, upside down. The triangle is flat.", lab))
    for cv, name, kind, e in [
            (ball_cv(), "a beach ball", SPH, "A ball is round all over. It is a sphere. A circle is flat."),
            (orange_cv(), "an orange", SPH, "An orange is round all over, like a ball. It is a sphere."),
            (dice_cv(), "a dice", CUBE, "A dice has 6 square faces, all the same size. It is a cube. A square is just one flat face."),
            (tin_cv(), "a tin of baked beans", CYL, "A tin has a flat circle at the top and the bottom. Its side is curved. It is a cylinder."),
            (icecream_cv(), "an ice-cream cone", CONE, "It has a circle at the top and a point at the bottom. It is a cone."),
            (hat_cv(), "a party hat", CONE, "A party hat has a round bottom and a point at the top. It is a cone."),
    ]:
        its.append(mcq(fig(cv.svg(name)) + "This is %s. What 3-D object is it?" % name, kind, WRONG3[kind], e))
    assert len(its) == 20, len(its)
    return {"title": "3-D objects around us", "items": its}


# ------------------------------------------------------------ set 5: same and different, word problems
def set_world(rnd, pos, P):
    its = []
    n, he, his = P.next()
    its.append(mcq(fig(ball_cv(0.8).svg("a beach ball")) + "%s says a ball is a circle. Is %s right?" % (n, he),
                   "No, it is a sphere", ["Yes, it is a circle", "No, it is a cube", "No, it is a cone"],
                   "A circle is flat. A ball is round all over. It is a sphere."))
    its.append(mcq2(two([flat("circle", 0, 0.85, 0), sphere_cv(0.85)], ["circle", "sphere"], "a circle and a sphere"),
                   "What is different?", "the sphere is solid", ["the circle is solid", "the colour", "nothing"],
                   "Both are round. The circle is flat. The sphere is solid, like a ball."))
    its.append(mcq2(two([flat("square", 0, 0.8, 0), pic3d("cube", 0.8)], ["square", "cube"], "a square and a cube"),
                   "What is different?", "the cube is solid", ["the square is solid", "the cube is round", "nothing"],
                   "The square is flat. The cube is solid. Each face of the cube is a square."))
    its.append(mcq2(two([pic3d("cyl", 0.8), pic3d("cone", 0.8)], ["cylinder", "cone"], "a cylinder and a cone"),
                   "How are they the same?", "both have a circle face", ["both have a point", "both have 2 circles", "both are flat"],
                   "The cylinder has 2 flat circles. The cone has 1. Both have a circle face. Only the cone has a point."))
    its.append(mcq2(two([pic3d("cyl", 0.8), pic3d("cone", 0.8)], ["cylinder", "cone"], "a cylinder and a cone"),
                   "What is different?", "only the cone has a point", ["only the cylinder rolls", "only the cone is solid", "nothing"],
                   "Both are solid and both can roll. The cone comes to a point. The cylinder does not."))
    n, he, his = P.next()
    its.append(mcq2(two([ball_cv(0.7), dice_cv(36)], ["ball", "dice"], "a ball and a dice"),
                   "%s pushes a ball and a dice. Which one rolls?" % n, "the ball", ["the dice", "both", "neither"],
                   "The ball is a sphere. It is curved all over, so it rolls. The dice has flat faces. It slides."))
    n, he, his = P.next()
    its.append(mcq(fig(row_svg([pic3d("cube", 0.55), sphere_cv(0.6), pic3d("cone", 0.55)], ["cube", "sphere", "cone"],
                               "a row of 3-D objects", gap=26, fs=15))
                   + "%s builds a tower at recess. Which object stacks best?" % n, "the cube", ["the sphere", "the cone", "none of them"],
                   "A cube has a flat top and a flat bottom. Cubes stack well. A sphere rolls off. A cone has a point."))
    n, he, his = P.next()
    its.append(mcq(fig(tin_cv(0.8).svg("a tin")) + "%s draws round the bottom of a tin. What shape does %s draw?" % (n, he),
                   "a circle", ["a cylinder", "a square", "a sphere"],
                   "The bottom of a tin is a flat circle. %s draws a circle." % n))
    n, he, his = P.next()
    its.append(mcq(fig(dice_cv(44).svg("a dice")) + "%s draws round one face of a dice. What shape does %s draw?" % (n, he),
                   "a square", ["a cube", "a circle", "a triangle"],
                   "A dice is a cube. Each face is a flat square."))
    n, he, his = P.next()
    its.append(mcq(fig(sandwich_cv().svg("a square sandwich with a cut from corner to corner"))
                   + "%s cuts %s square sandwich on the line. What shape is each piece?" % (n, his),
                   "a triangle", ["a square", "a rectangle", "a circle"],
                   "The cut goes from corner to corner. Each piece has 3 sides. Each piece is a triangle."))
    n, he, his = P.next()
    its.append(mcq(fig(door_cv().svg("a classroom door")) + "%s looks at the classroom door. What shape is it?" % n,
                   "a rectangle", ["a square", "a triangle", "a cube"],
                   "The door has 4 sides and 4 square corners. 2 sides are long. 2 are short. It is a rectangle."))
    n, he, his = P.next()
    its.append(mcq(fig(cricket_ball_cv(0.9).svg("a cricket ball")) + "%s holds a cricket ball. What 3-D object is it?" % n,
                   SPH, ["circle", CYL, CONE],
                   "A cricket ball is round all over. It is a sphere."))
    n, he, his = P.next()
    its.append(mcq2(two([tin_cv(0.7), ball_cv(0.7)], ["tin", "ball"], "a tin and a ball"),
                   "%s wants an object that can roll and stack. Which one?" % n, "the tin", ["the ball", "both", "neither"],
                   "A tin has a curved side, so it rolls. It has flat ends, so it stacks. A ball rolls but does not stack."))
    n, he, his = P.next()
    its.append(mcq2(two([flat("tri_eq", 0, 0.75, 1), flat("tri_right", 0, 0.7, 2)], ["", ""], "two triangles"),
                   "%s draws 2 triangles. How many sides in total?" % n, 6, [3, 5, 4],
                   "Each triangle has 3 sides. 3 + 3 = 6 sides."))
    n, he, his = P.next()
    its.append(mcq2(two([flat("square", 0, 0.7, 3), flat("tri_eq", 0, 0.75, 0)], ["", ""], "a square and a triangle"),
                   "%s draws a square and a triangle. How many corners in total?" % n, 7, [6, 8, 4],
                   "A square has 4 corners. A triangle has 3 corners. 4 + 3 = 7."))
    n, he, his = P.next()
    its.append(mcq(fig(row_svg([flat("square", 0, 0.6, 1), flat("square", 0, 0.6, 2), flat("square", 0, 0.6, 4)], ["", "", ""],
                               "a row of 3 squares", gap=18))
                   + "%s makes 3 squares with sticks. 1 stick is 1 side. How many sticks?" % n, 12, [4, 8, 7],
                   "Each square has 4 sides. 4 + 4 + 4 = 12 sticks."))
    n, he, his = P.next()
    its.append(mcq2(two([flat("circle", 0, 0.75, 4), flat("tri_eq", 0, 0.75, 2)], ["", ""], "a circle and a triangle"),
                   "%s draws a circle and a triangle. How many corners in total?" % n, 3, [4, 1, 6],
                   "A circle has 0 corners. A triangle has 3. 0 + 3 = 3 corners."))
    n, he, his = P.next()
    its.append(mcq(fig(row_svg([flat("tri_eq", 0, 0.6, 0), flat("square", 0, 0.6, 1), flat("circle", 0, 0.6, 3), flat("rect", 0, 0.5, 4)],
                               ["", "", "", ""], "a row of shapes", gap=16))
                   + "%s sorts these shapes. How many have 4 corners?" % n, 2, [3, 4, 1],
                   "The square and the rectangle have 4 corners: 2 shapes. The triangle has 3. The circle has none."))
    n, he, his = P.next()
    its.append(mcq(fig(row_svg([orange_cv(0.6), tin_cv(0.55), dice_cv(30)], ["orange", "tin", "dice"], "a row of objects", gap=24, fs=15))
                   + "%s puts these in a bag. How many have a flat face?" % n, 2, [3, 1, 0],
                   "The tin has 2 flat circles. The dice has flat squares. The orange is round all over. So 2 have a flat face."))
    n, he, his = P.next()
    its.append(mcq(fig(flat("square", 45, 0.85, 2).svg("a flat shape")) + "%s calls this shape a diamond. What is it really?" % n,
                   "a square", ["a triangle", "a circle", "a cube"],
                   "It has 4 sides the same length. It is just turned. It is a square."))
    assert len(its) == 20, len(its)
    return {"title": "Same and different: word problems", "items": its}
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
    parts = row_svg([marked("tri_eq", 0, 1.0, 1, side=1), marked("tri_eq", 0, 1.0, 1, corner=0)], ["a side", "a corner"],
                    "a triangle with a side in red and a triangle with a corner marked red", gap=40, fs=15)
    turned = row_svg([flat("square", 0, 0.8, 2), flat("square", 45, 0.75, 4), flat("tri_eq", 0, 0.8, 0), flat("tri_eq", 180, 0.5, 1)],
                     ["square", "still a square", "triangle", "still a triangle"],
                     "a square and the same square turned; a big triangle and a small upside-down triangle", gap=26, fs=15)
    solids = row_svg([pic3d("cube", 0.8), sphere_cv(0.85), cylinder_cv(0.8), cone_cv(0.8)], ["cube", "sphere", "cylinder", "cone"],
                     "cube, sphere, cylinder and cone", gap=30, fs=15)
    pairs = row_svg([flat("circle", 0, 0.85, 0), sphere_cv(0.85), flat("square", 0, 0.8, 0), pic3d("cube", 0.8)],
                    ["circle (2-D)", "sphere (3-D)", "square (2-D)", "cube (3-D)"],
                    "a flat circle next to a sphere, and a flat square next to a cube", gap=22, fs=15)
    objs = row_svg([ball_cv(0.8), dice_cv(40), tin_cv(0.8), icecream_cv(0.8)],
                   ["ball", "dice", "tin", "ice-cream cone"],
                   "a ball, a dice, a tin and an ice-cream cone", gap=24, fs=15)
    return (
        "<h2>2-D shapes are flat</h2>"
        "<p>A 2-D shape is <b>flat</b>, like a drawing on paper. Count the <b>sides</b> and <b>corners</b> to name it.</p>"
        "<figure class='sn-fig'>" + flat4 + "</figure>" +
        table(["Shape", "Sides", "Corners", "Look for"], [
            ["Circle", "0", "0", "Round all the way."],
            ["Triangle", "3", "3", "3 straight sides."],
            ["Square", "4", "4", "4 sides, all the same length."],
            ["Rectangle", "4", "4", "2 long sides and 2 short sides."]]) +
        "<p>A side is a straight edge. A corner is where 2 sides meet.</p>"
        "<figure class='sn-fig'>" + parts + "</figure>"
        "<p>Size, colour and turning do not change the name.</p>"
        "<figure class='sn-fig'>" + turned +
        "<figcaption>A square on its corner is still a square, not a “diamond”.</figcaption></figure>" +
        ex("Example 1", "A shape has 3 straight sides. It points down. What is it?",
           "Count the sides: 3. It does not matter which way it points.", "a triangle") +
        "<h2>Sort and compare</h2>"
        "<p>To sort shapes, look at the sides and corners, not the colour or size. "
        "The odd one out is the shape that does not follow the rule.</p>" +
        ex("Example 2", "A triangle, a square and a rectangle. Which is the odd one out?",
           "The square and the rectangle have 4 sides. The triangle has 3.", "the triangle") +
        "<h2>3-D objects are solid</h2>"
        "<p>A 3-D object is <b>solid</b>. You can pick it up and hold it. Dashed lines show the back.</p>"
        "<figure class='sn-fig'>" + solids + "</figure>" +
        table(["Object", "Look for"], [
            ["Cube", "6 flat square faces, all the same size."],
            ["Sphere", "Round all over, like a ball."],
            ["Cylinder", "A flat circle at each end and a curved side."],
            ["Cone", "1 flat circle and a point."]]) +
        "<h2>Shapes and objects around us</h2>"
        "<figure class='sn-fig'>" + objs +
        "<figcaption>A ball is a sphere. A dice is a cube. A tin is a cylinder. An ice-cream cone is a cone.</figcaption></figure>" +
        ex("Example 3", "Which one rolls: a ball or a dice?",
           "A ball is a sphere. It is curved all over. A dice has only flat faces.", "the ball") +
        "<h2>Common mistakes</h2>"
        "<figure class='sn-fig'>" + pairs + "</figure>" +
        table(["Mistake", "What to do instead"], [
            ["Calling a turned square a “diamond”", "Count the sides. 4 sides the same length make a square, any way up."],
            ["Calling a ball a circle", "A circle is flat. A ball is round all over: it is a sphere."],
            ["Calling a dice a square", "A square is flat. A dice is solid: it is a cube."],
            ["Calling a rectangle a square", "Check the sides. If 2 sides are longer, it is a rectangle."],
            ["Mixing up a cylinder and a cone", "A cylinder has 2 flat circles. A cone has 1 circle and a point."],
            ["Sorting by colour", "Colour and size do not change a shape. Sort by sides and corners."],
        ])
    )


FAQ = [
    {"q": "What shapes and objects do Year 1 students learn in the Australian Curriculum?",
     "a": "Year 1 students make, compare and sort familiar shapes and objects (AC9M1SP01). They name circles, triangles, squares and rectangles, and objects such as cubes, spheres, cylinders and cones, and find them in the world around them."},
    {"q": "What is the difference between a 2-D shape and a 3-D object?",
     "a": "A 2-D shape is flat, like a drawing on paper. A 3-D object is solid and you can hold it, like a ball (a sphere) or a dice (a cube)."},
    {"q": "Is a square on its corner a diamond?",
     "a": "No. It is still a square, because it has 4 sides of the same length. Turning a shape never changes its name."},
    {"q": "How can I help my Year 1 child learn shapes at home?",
     "a": "Go on a shape hunt around the house or the park: find a ball (sphere), a tin (cylinder), a dice (cube) and an ice-cream cone (cone). Draw around their flat faces to see circles and squares."},
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
    rnd = random.Random(1810)
    P = People(rnd)
    sets = [set_name2d(rnd, Pos(rnd)), set_sides(rnd, Pos(rnd), P), set_sort(rnd, Pos(rnd), P),
            set_objects(rnd, Pos(rnd)), set_world(rnd, Pos(rnd), P)]
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
        "country": "au", "subject": "maths", "grade": "year-1", "slug": "shapes-and-objects", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Shapes and Objects: Name, Sort and Compare",
        "seo_title": "Year 1 Shapes and Objects Worksheets: 2-D Shapes and 3-D Objects (Free, with Answers)",
        "short_title": "Shapes and objects",
        "domain": "Space",
        "standard_code": "AC9M1SP01",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Make, compare and classify familiar shapes; recognise familiar shapes and objects in the environment, "
                         "identifying the similarities and differences between them",
        "meta_desc": "Free Year 1 maths worksheets on shapes and objects, matched to the Australian Curriculum (AC9M1SP01): "
                     "name circles, triangles, squares and rectangles, count sides and corners, find the odd one out, "
                     "and spot cubes, spheres, cylinders and cones in everyday things. 100 questions with an answer key.",
        "key_big": "Count the sides and corners. Flat shapes are 2-D; solid objects are 3-D.",
        "key_sub": "Size, colour and turning never change the name: a square on its corner is still a square. "
                   "A ball is a sphere, not a circle, and a dice is a cube, not a square.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(four (shapes|objects) labelled A to D|a row of|two |a (circle|square|rectangle|cylinder|ball|tin) and a)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
