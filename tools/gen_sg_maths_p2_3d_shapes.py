# -*- coding: utf-8 -*-
"""
Singapore Primary 2 Maths: 3D shapes
(MOE 2021 Primary Mathematics Syllabus, Standard, Primary 2: Geometry —
 identifying, naming, describing and classifying 3D shapes: cube, cuboid, cone, cylinder, sphere)
  python3 tools/gen_sg_maths_p2_3d_shapes.py
Name the five 3D shapes from drawings in different positions, match real objects (a die, a box of tissues, an ice
cream cone, a tin of milk, a ball), count flat and curved faces, decide which shapes can roll, stack or slide, and
sort shapes, with simple word problems and bar models. Short sentences for 7-8 year olds.

Pictures (checked in code):
  cube, cuboid  drawn from 3D corners and faces, turned and seen from a little above; the flat faces counted in a
                picture come from the same data (3 seen, 6 in all)
  curved shapes cylinder, cone and sphere drawn with ellipses; the hidden half of a rim is dashed
  objects       the same drawings with a die's dots, a tissue box's slot, a tin's label, a ball's stripes
Wrong answers come from real mistakes: cube vs cuboid (a long box with square ends is still a cuboid), circle vs
sphere and square vs cube (2D names for 3D shapes), cylinder vs cone, triangle for a cone, counting only the faces
you can see, "a cylinder cannot roll because it has flat faces", forgetting that a cone rolls, renaming mistakes
in the bar model sums (46 − 28 = 22, 35 + 27 = 512).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-2")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL, SIDE, TOP3 = "#cfe6d6", "#a9d3b6", "#e6f2e9"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Kumar", "Arjun", "Ethan", "Ryan"]

CUBE, CUBOID, CYL, CONE, SPH = "cube", "cuboid", "cylinder", "cone", "sphere"
# flat faces, curved faces, can roll, can stack, can slide
FACTS = {CUBE: (6, 0, False, True, True), CUBOID: (6, 0, False, True, True), CYL: (2, 1, True, True, True),
         CONE: (1, 1, True, False, True), SPH: (0, 1, True, False, False)}


# ------------------------------------------------------------ question helpers
def mcq(q, correct, wrong, e):
    correct = str(correct)
    wrong = [str(x) for x in wrong]
    assert len(wrong) == 3, (q, wrong)
    ch = [correct] + wrong
    assert len(set(re.sub(r"<[^>]+>", "", x) for x in ch)) == 4, (q, ch)
    return {"q": q, "c": ch, "a": 0, "e": e}


def mcq_n(q, correct, wrong, e):
    assert isinstance(correct, int) and correct >= 0, (q, correct)
    assert len(wrong) == 3 and correct not in wrong and len(set(wrong)) == 3, (q, correct, wrong)
    return mcq(q, correct, wrong, e)


def mcq_fixed(q, choices, correct, e):
    """Choices keep their order (A B C D)."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fixed": True}


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=15, anchor="middle", bold=True, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def art(n):
    return "an" if n[0] in "aeiou" else "a"


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
    return (len(t) - t.count(" ") * 0.3 - t.count(",") * 0.3) * fs * 0.6


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
        self.el.append(("p", list(pts), fill, sw, col))
        for x, y in pts:
            self.grow(x - sw, y - sw, x + sw, y + sw)

    def circle(self, c, r, fill=FILL, sw=2.4, col=GREEN):
        self.el.append(("c", c, r, fill, sw, col))
        self.grow(c[0] - r - sw, c[1] - r - sw, c[0] + r + sw, c[1] + r + sw)

    def pline(self, pts, dashed=False, sw=2.4, col=GREEN):
        self.el.append(("pl", list(pts), dashed, sw, col))
        for x, y in pts:
            self.grow(x - sw, y - sw, x + sw, y + sw)

    def add(self, other, dx, dy):
        """Copy another canvas into this one, moved by (dx, dy)."""
        mv = lambda pts: [(x + dx, y + dy) for x, y in pts]
        for e in other.el:
            if e[0] == "p":
                self.poly(mv(e[1]), e[2], e[3], e[4])
            elif e[0] == "c":
                self.circle((e[1][0] + dx, e[1][1] + dy), e[2], e[3], e[4], e[5])
            else:
                self.pline(mv(e[1]), e[2], e[3], e[4])

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
            parts.append(text(x + cw / 2, H + 8 + fs * 0.86, cap, fs, col=col))
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
    return svg_wrap(W + 1, H, "".join(s), label)


# ------------------------------------------------------------ cubes and cuboids
class Solid:
    def __init__(self, verts, faces):
        self.v, self.f = verts, faces

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

    def faces2d(self, k, yaw, pitch):
        """Visible faces: (index, screen corners, normal)."""
        pts, vis, nrm = self.view(yaw, pitch)
        P = lambda p: (p[0] * k, -p[1] * k)
        return [(fi, [P(pts[i]) for i in fc], nrm[fi]) for fi, fc in enumerate(self.f) if vis[fi]]

    def hidden_edges(self, k, yaw, pitch):
        pts, vis, _ = self.view(yaw, pitch)
        P = lambda p: (p[0] * k, -p[1] * k)
        edges = {}
        for fi, fc in enumerate(self.f):
            for i in range(len(fc)):
                edges.setdefault(tuple(sorted((fc[i], fc[(i + 1) % len(fc)]))), []).append(fi)
        return [(P(pts[a]), P(pts[b])) for (a, b), fs in edges.items() if not any(vis[f] for f in fs)]

    def cv(self, k, yaw=30, pitch=20, cols=(TOP3, SIDE, FILL), dashed=True):
        cv = Canvas()
        for fi, q, n in self.faces2d(k, yaw, pitch):
            cv.poly(q, cols[0] if n[1] > 0.5 else cols[1] if n[0] > 0.3 else cols[2], 2.4)
        if dashed:
            for a, b in self.hidden_edges(k, yaw, pitch):
                cv.pline([a, b], dashed=True, sw=1.6)
        return cv


def box(L, H, W):
    v = [(x, y, z) for x in (0, L) for y in (0, H) for z in (0, W)]
    idx = {p: i for i, p in enumerate(v)}
    g = lambda *ps: [idx[p] for p in ps]
    f = [g((0, 0, 0), (L, 0, 0), (L, H, 0), (0, H, 0)), g((0, 0, W), (L, 0, W), (L, H, W), (0, H, W)),
         g((0, 0, 0), (0, 0, W), (0, H, W), (0, H, 0)), g((L, 0, 0), (L, 0, W), (L, H, W), (L, H, 0)),
         g((0, 0, 0), (L, 0, 0), (L, 0, W), (0, 0, W)), g((0, H, 0), (L, H, 0), (L, H, W), (0, H, W))]
    return Solid(v, f)


VIEWS = {
    "cube": ((1.1, 1.1, 1.1), 30, 22),
    "cube_turned": ((1.1, 1.1, 1.1), 50, 30),
    "cuboid": ((1.9, 0.8, 1.0), 25, 22),
    "cuboid_tall": ((0.8, 1.8, 0.7), 35, 18),
    "cuboid_turned": ((1.6, 1.0, 0.8), -35, 24),
    "cuboid_sq": ((1.9, 0.75, 0.75), 25, 22),
}
for _k, (_d, _y, _p) in VIEWS.items():
    assert len(box(*_d).faces2d(1, _y, _p)) == 3, _k          # every picture shows 3 of the 6 faces


def solid_cv(view, k=50, **kw):
    d, yaw, pitch = VIEWS[view]
    return box(*d).cv(k, yaw, pitch, **kw)


# ------------------------------------------------------------ curved shapes
def ellipse(cx, cy, rx, ry, a0, a1, n=40):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def _rot90(pts, on):
    return [(-y, x) for x, y in pts] if on else pts


def cylinder_cv(s=1.0, lying=False, rx=36, ry=11, h=72, body=FILL, top=TOP3):
    rx, ry, h = rx * s, ry * s, h * s
    R = lambda p: _rot90(p, lying)
    cv = Canvas()
    cv.poly(R(ellipse(0, 0, rx, ry, 180, 360) + ellipse(0, h, rx, ry, 0, 180)), body, 0)
    cv.poly(R(ellipse(0, 0, rx, ry, 0, 360)[:-1]), top, 2.4)
    cv.pline(R([(-rx, 0), (-rx, h)]))
    cv.pline(R([(rx, 0), (rx, h)]))
    cv.pline(R(ellipse(0, h, rx, ry, 0, 180)))
    cv.pline(R(ellipse(0, h, rx, ry, 180, 360)), dashed=True, sw=1.6)
    return cv


def cone_cv(s=1.0, how="up", rx=38, ry=11, h=80, body=FILL):
    """how: 'up' (tip at the top), 'down' (tip at the bottom), 'side' (lying down)."""
    rx, ry, h = rx * s, ry * s, h * s
    cv = Canvas()
    if how == "down":
        cv.poly([(0, h)] + ellipse(0, 0, rx, ry, 0, 180), body, 0)
        cv.pline([(-rx, 0), (0, h), (rx, 0)])
        cv.poly(ellipse(0, 0, rx, ry, 0, 360)[:-1], TOP3, 2.4)
        return cv
    R = lambda p: _rot90(p, how == "side")
    cv.poly(R([(0, 0)] + ellipse(0, h, rx, ry, 180, 0)), body, 0)
    cv.poly(R([(0, 0)] + ellipse(0, h, rx, ry, 0, 180)), body, 0)
    cv.pline(R([(-rx, h), (0, 0), (rx, h)]))
    cv.pline(R(ellipse(0, h, rx, ry, 0, 180)))
    cv.pline(R(ellipse(0, h, rx, ry, 180, 360)), dashed=True, sw=1.6)
    return cv


def sphere_cv(s=1.0, fill=FILL):
    r = 40 * s
    cv = Canvas()
    cv.circle((0, 0), r, fill=fill, sw=2.4)
    cv.pline(ellipse(0, 0, r, r * 0.3, 0, 180), sw=1.6)
    cv.pline(ellipse(0, 0, r, r * 0.3, 180, 360), dashed=True, sw=1.2)
    return cv


# ------------------------------------------------------------ flat 2D shapes (wrong pictures)
def circle2d(s=1.0):
    cv = Canvas()
    cv.circle((0, 0), 40 * s, fill="#ffffff", sw=2.4)
    return cv


def square2d(s=1.0):
    a = 70 * s
    cv = Canvas()
    cv.poly([(0, 0), (a, 0), (a, a), (0, a)], "#ffffff", 2.4)
    return cv


def tri2d(s=1.0):
    cv = Canvas()
    cv.poly([(-38 * s, 80 * s), (38 * s, 80 * s), (0, 0)], "#ffffff", 2.4)
    return cv


# ------------------------------------------------------------ real objects
def bil(q, u, v):
    """Point on a 4-corner face (corners in order) at (u, v), both 0-1."""
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = q
    return ((1 - u) * (1 - v) * x0 + u * (1 - v) * x1 + u * v * x2 + (1 - u) * v * x3,
            (1 - u) * (1 - v) * y0 + u * (1 - v) * y1 + u * v * y2 + (1 - u) * v * y3)


def uv_ellipse(q, cu, cv_, ru, rv, n=24):
    return [bil(q, cu + ru * math.cos(2 * math.pi * i / n), cv_ + rv * math.sin(2 * math.pi * i / n)) for i in range(n)]


PIPS = {1: [(.5, .5)], 2: [(.27, .27), (.73, .73)], 3: [(.25, .25), (.5, .5), (.75, .75)]}


def die_cv(s=1.0):
    d, yaw, pitch = VIEWS["cube"]
    k = 50 * s
    sol = box(*d)
    cv = Canvas()
    faces = sol.faces2d(k, yaw, pitch)
    for n_pips, (fi, q, n) in zip([1, 2, 3], faces):
        cv.poly(q, "#ffffff" if n[1] <= 0.5 else "#f4f4f4", 2.4)
        for u, v in PIPS[n_pips]:
            cv.poly(uv_ellipse(q, u, v, 0.1, 0.1), INK, 0)
    return cv


def tissue_cv(s=1.0):
    d, yaw, pitch = VIEWS["cuboid"]
    k = 50 * s
    sol = box(*d)
    cv = Canvas()
    for fi, q, n in sol.faces2d(k, yaw, pitch):
        cv.poly(q, "#bfe0f2" if n[1] > 0.5 else "#8cc5e6" if n[0] > 0.3 else "#a6d3ee", 2.4)
        if n[1] > 0.5:
            slot = uv_ellipse(q, 0.5, 0.5, 0.3, 0.14)
            cv.poly(slot, "#ffffff", 1.6)
            cx, cy = bil(q, 0.5, 0.5)
            cv.poly([(cx - 16 * s, cy), (cx - 10 * s, cy - 18 * s), (cx - 2 * s, cy - 11 * s), (cx + 7 * s, cy - 24 * s),
                     (cx + 16 * s, cy)], "#ffffff", 1.6, GRAY)
    return cv


def tin_cv(s=1.0):
    rx, ry, h = 32 * s, 10 * s, 66 * s
    cv = cylinder_cv(s, rx=32, ry=10, h=66, body="#e8e8e8", top="#f4f4f4")
    y1, y2 = h * 0.28, h * 0.78
    cv.poly(ellipse(0, y2, rx, ry, 0, 180) + ellipse(0, y1, rx, ry, 180, 0), "#e57373", 0)
    cv.pline(ellipse(0, y1, rx, ry, 0, 180), sw=1.4, col=RED)
    cv.pline(ellipse(0, y2, rx, ry, 0, 180), sw=1.4, col=RED)
    cv.pline([(-rx, 0), (-rx, h)])
    cv.pline([(rx, 0), (rx, h)])
    return cv


def ball_cv(s=1.0):
    r = 38 * s
    cv = Canvas()
    cv.circle((0, 0), r, fill="#fbe3a0", sw=2.4)
    cv.poly(ellipse(0, 0, r * 0.42, r, -90, 90) + ellipse(0, 0, r * 0.42, r, 90, 270)[1:-1], "#e57373", 1.4, RED)
    cv.pline(ellipse(0, 0, r, r * 0.3, 0, 180), sw=1.6)
    cv.circle((0, 0), r, fill="none", sw=2.4)
    return cv


def orange_cv(s=1.0):
    r = 38 * s
    cv = Canvas()
    cv.circle((0, 0), r, fill="#f39c34", sw=2.4, col="#b35f00")
    cv.pline([(0, -r), (2 * s, -r - 7 * s)], sw=2.4, col="#6b4a1e")
    cv.poly([(2 * s, -r - 4 * s), (14 * s, -r - 14 * s), (24 * s, -r - 6 * s), (12 * s, -r)], "#5aa65a", 1.4, GREEN)
    return cv


def icecream_cv(s=1.0):
    rx, ry, h = 30 * s, 9 * s, 70 * s
    cv = Canvas()
    cv.circle((0, -16 * s), 31 * s, fill="#f7c6d0", sw=2.4, col="#c2586e")
    cv.poly([(0, h)] + ellipse(0, 0, rx, ry, 0, 180), "#e8c07a", 2.4, "#a0702a")
    return cv


def hat_cv(s=1.0):
    cv = cone_cv(s, "up", rx=34, ry=10, h=76, body="#f9d56e")
    cv.circle((0, -5 * s), 7 * s, fill=RED, sw=1.2, col="#7a2318")
    return cv


def rocket_cv(s=1.0):
    rx, ry = 26, 8
    cv = Canvas()
    cv.add(cylinder_cv(s, rx=rx, ry=ry, h=64), 0, 46 * s)
    cv.add(cone_cv(s, "up", rx=rx, ry=ry, h=46), 0, 0)
    return cv


PICS = {
    "circle2d": circle2d, "square2d": square2d, "tri2d": tri2d,
    "cyl": lambda s: cylinder_cv(s), "cyl_lying": lambda s: cylinder_cv(s, lying=True),
    "cyl_short": lambda s: cylinder_cv(s, h=26), "cyl_thin": lambda s: cylinder_cv(s, rx=17, ry=6, h=84),
    "cone": lambda s: cone_cv(s), "cone_down": lambda s: cone_cv(s, "down"), "cone_side": lambda s: cone_cv(s, "side"),
    "sphere": lambda s: sphere_cv(s),
    "die": die_cv, "tissue": tissue_cv, "tin": tin_cv, "ball": ball_cv, "orange": orange_cv,
    "icecream": icecream_cv, "hat": hat_cv, "rocket": rocket_cv,
}
KIND = {"cube": CUBE, "cube_turned": CUBE, "cuboid": CUBOID, "cuboid_tall": CUBOID, "cuboid_turned": CUBOID,
        "cuboid_sq": CUBOID, "cyl": CYL, "cyl_lying": CYL, "cyl_short": CYL, "cyl_thin": CYL, "cone": CONE,
        "cone_down": CONE, "cone_side": CONE, "sphere": SPH, "die": CUBE, "tissue": CUBOID, "tin": CYL,
        "ball": SPH, "orange": SPH, "hat": CONE}


def pic(key, s=1.0):
    if key in VIEWS:
        return solid_cv(key, 50 * s)
    return PICS[key](s)


def one(key, label=None, s=1.0):
    return fig(pic(key, s).svg(label or "a 3D shape"))


def grid_q(pos, right, others, q, e, label="four pictures labelled A to D", s=0.62):
    p = pos.next()
    cells = [pic(k, s) for k in others]
    cells.insert(p, pic(right, s))
    L = "ABCD"[p]
    return mcq_fixed(fig(grid_svg(cells, label)) + q, list("ABCD"), L, e % L)


# ------------------------------------------------------------ bar model
def bar_svg(rows, total=None, label="bar model"):
    """Singapore bar model, drawn to scale.
    rows = [(name, [(value, dashed)], [(first seg, last seg, text)], right text (optional))];
    total = text for a brace on the right spanning all the rows."""
    LW, BW, BH = 96, 300, 30
    big = max(sum(v for v, _ in r[1]) for r in rows)
    sc = BW / float(big)
    side = max([len(r[3]) for r in rows if len(r) > 3] or [0])
    W = LW + BW + (70 if total else 14) + (int(side * 9.5) + 16 if side else 0)
    y = 6
    s = []
    tops = []
    for row in rows:
        name, segs, over = row[:3]
        y += 24
        tops.append(y)
        s.append(text(LW - 10, y + BH / 2.0 + 5, name, 14, anchor="end"))
        xs = [LW]
        for v, dashed in segs:
            xs.append(xs[-1] + v * sc)
        for k, (v, dashed) in enumerate(segs):
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='1.6'%s/>"
                     % (xs[k], y, xs[k + 1] - xs[k], BH, "#fff" if dashed else FILL, INK if not dashed else RED,
                        " stroke-dasharray='5 4'" if dashed else ""))
        for a, b, t in over:
            x1, x2 = xs[a] + 1, xs[b + 1] - 1
            assert tw(t, 14) < x2 - x1 + 8, (t, x2 - x1)
            s.append("<path d='M%.1f %d L%.1f %d L%.1f %d L%.1f %d' fill='none' stroke='%s' stroke-width='1.4'/>"
                     % (x1, y - 2, x1, y - 7, x2, y - 7, x2, y - 2, INK))
            s.append(text((x1 + x2) / 2.0, y - 11, t, 14, col=RED if t == "?" else INK))
        if len(row) > 3:
            s.append(text(xs[-1] + 10, y + BH / 2.0 + 6, row[3], 16, anchor="start", col=RED))
        y += BH + 12
    H = y
    if total:
        xb = LW + BW + 10
        y1, y2 = tops[0], tops[-1] + BH
        ym = (y1 + y2) / 2.0
        s.append("<path d='M%d %d q6 0 6 6 L%d %.1f q0 3 4 3 q-4 0 -4 3 L%d %d q0 6 -6 6' fill='none' "
                 "stroke='%s' stroke-width='1.6'/>" % (xb, y1, xb + 6, ym - 3, xb + 6, y2 - 6, INK))
        s.append(text(xb + 16, ym + 5, total, 14, anchor="start", col=RED if total == "?" else INK))
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ set 1: name 3D shapes
WRONG = {CUBE: [CUBOID, "square", CYL], CUBOID: [CUBE, "rectangle", CYL], CYL: [CONE, "circle", "rectangle"],
         CONE: [CYL, "triangle", SPH], SPH: ["circle", CYL, CONE]}
E1 = {
    CUBE: "It has 6 flat faces. They are all squares of the same size. So it is a cube.",
    CUBOID: "It has 6 flat faces. They are rectangles, not all squares. So it is a cuboid, not a cube.",
    CYL: "It has 2 flat faces that are circles and 1 curved face. So it is a cylinder. It has no pointed tip like a cone.",
    CONE: "It has 1 flat face that is a circle, a curved face and a pointed tip. So it is a cone.",
    SPH: "It is round all over, like a ball. So it is a sphere. A circle is flat; a sphere is solid.",
}
TURN = {"cube_turned": " It is turned, but it is still a cube.",
        "cuboid_tall": " It is standing on its end, but it is still a cuboid.",
        "cuboid_turned": " It is turned, but it is still a cuboid.",
        "cuboid_sq": " The 2 end faces are squares, but the other 4 faces are long rectangles. In a cube, all 6 faces are squares.",
        "cyl_lying": " It is lying on its side, but it is still a cylinder.",
        "cyl_short": " It is short, like a coin, but it is still a cylinder.",
        "cyl_thin": " It is tall and thin, but it is still a cylinder.",
        "cone_down": " It is upside down, but it is still a cone.",
        "cone_side": " It is lying on its side, but it is still a cone."}


def set_name(pos):
    its = []
    asks = ["What is the name of this 3D shape?", "Name this 3D shape.", "What is this shape called?"]
    keys = ["cube", "cuboid", "cyl", "cone", "sphere", "cube_turned", "cuboid_tall", "cyl_lying", "cone_down",
            "cuboid_turned", "cyl_short", "cone_side", "cyl_thin", "cuboid_sq"]
    for i, k in enumerate(keys):
        kind = KIND[k]
        its.append(mcq(one(k) + asks[i % 3], kind, WRONG[kind], E1[kind] + TURN.get(k, "")))
    its.append(mcq("Which of these is a flat 2D shape?", "circle", [SPH, CUBE, CONE],
                   "A circle is flat. You can draw it on paper. A sphere, a cube and a cone are solid 3D shapes."))
    its.append(grid_q(pos, "cuboid_turned", ["cube", "cyl", "square2d"], "Which picture shows a cuboid?",
                      "%s is a cuboid. Its flat faces are rectangles. The cube has only square faces, the cylinder has "
                      "a curved face and the square is a flat 2D shape."))
    its.append(grid_q(pos, "sphere", ["circle2d", "cyl", "cone"], "Which picture shows a sphere?",
                      "%s is a sphere. It is round all over, like a ball. The plain circle is a flat 2D shape, not a sphere."))
    its.append(grid_q(pos, "cone", ["tri2d", "cyl", "sphere"], "Which picture shows a cone?",
                      "%s is a cone. It has a flat circle face and a pointed tip. The triangle is a flat 2D shape."))
    its.append(grid_q(pos, "cube_turned", ["cuboid_sq", "square2d", "cuboid_tall"], "Which picture shows a cube?",
                      "%s is a cube. All its faces are squares of the same size. The two long boxes are cuboids. "
                      "The square is a flat 2D shape."))
    q = (fig(row_svg([pic("cyl", 0.8), pic("cyl_lying", 0.8)], ["", ""], "the same 3D shape in two positions", gap=40))
         + "Both pictures show the same shape. What is it?")
    its.append(mcq(q, CYL, WRONG[CYL], E1[CYL] + " Turning a shape does not change its name."))
    assert len(its) == 20, len(its)
    return {"title": "Name 3D shapes", "items": its}


# ------------------------------------------------------------ set 2: 3D shapes in real life
def set_real(pos, P):
    its = []
    E = {
        "die": "A die has 6 flat faces. They are all squares of the same size. So it is a cube.",
        "tissue": "A box of tissues has 6 flat faces. They are rectangles, not all squares. So it is a cuboid.",
        "tin": "A tin has 2 flat circle faces (top and bottom) and a curved face. So it is a cylinder.",
        "ball": "A ball is round all over. So it is a sphere. A circle is flat; a ball is solid.",
    }
    its.append(mcq(one("die", "a die") + "This is a die from a board game. What 3D shape is it?", CUBE,
                   [CUBOID, "square", SPH], E["die"]))
    its.append(mcq(one("tissue", "a box of tissues") + "This is a box of tissues. What 3D shape is it?", CUBOID,
                   [CUBE, "rectangle", CYL], E["tissue"]))
    its.append(mcq(one("tin", "a tin of milk") + "This is a tin of milk. What 3D shape is it?", CYL,
                   [CONE, "circle", CUBOID], E["tin"]))
    its.append(mcq(one("ball", "a ball") + "This is a ball. What 3D shape is it?", SPH, ["circle", CYL, CONE], E["ball"]))
    its.append(mcq(one("icecream", "an ice cream cone") + "This is an ice cream. What 3D shape is the biscuit part under the ice cream?",
                   CONE, [CYL, "triangle", SPH],
                   "It has a round opening at the top and a pointed tip at the bottom. So it is a cone. "
                   "From the side it looks like a triangle, but a triangle is flat."))
    its.append(mcq(one("icecream", "an ice cream cone") + "What 3D shape is the scoop of ice cream most like?",
                   SPH, ["circle", CONE, CYL],
                   "The scoop is round all over, like a ball. So it is most like a sphere."))
    its.append(mcq(one("orange", "a mandarin orange") + "Families give mandarin oranges at Chinese New Year. "
                   "What 3D shape is a mandarin orange most like?", SPH, ["circle", CONE, CYL],
                   "A mandarin orange is round all over, so it is most like a sphere. A circle is a flat 2D shape."))
    its.append(mcq(one("hat", "a party hat") + "This is a party hat. What 3D shape is it?", CONE,
                   [CYL, "triangle", SPH],
                   "It has a round opening at the bottom and a pointed tip at the top. So it is a cone."))
    for obj, kind, e in [
            ("A shoebox", CUBOID, "A shoebox has 6 flat faces that are rectangles. So it is a cuboid."),
            ("A candle", CYL, "A candle has a flat circle face at each end and a curved face. So it is a cylinder."),
            ("A marble", SPH, "A marble is round all over. So it is a sphere."),
            ("A packet drink", CUBOID, "A packet drink has 6 flat faces. They are rectangles, not all squares. So it is a cuboid."),
            ("A brick", CUBOID, "A brick has 6 flat faces. They are rectangles, not all squares. So it is a cuboid."),
            ("A round birthday cake", CYL, "A round cake has a flat circle top, a flat circle bottom and a curved side. So it is a cylinder."),
            ("A toy block with 6 square faces of the same size", CUBE, "6 flat faces that are all the same square: it is a cube, not a cuboid."),
    ]:
        its.append(mcq("%s is shaped like a …" % obj, kind, WRONG[kind], e))
    its.append(grid_q(pos, "tin", ["die", "tissue", "ball"], "Which object is shaped like a cylinder?",
                      "%s is a tin. It has 2 flat circle faces and a curved face, so it is a cylinder. "
                      "The die is a cube, the box is a cuboid and the ball is a sphere.", "four objects labelled A to D"))
    its.append(grid_q(pos, "die", ["tissue", "tin", "hat"], "Which object is shaped like a cube?",
                      "%s is a die. All its faces are squares of the same size, so it is a cube. "
                      "The box of tissues is a cuboid, the tin is a cylinder and the hat is a cone.", "four objects labelled A to D"))
    its.append(grid_q(pos, "orange", ["tin", "hat", "tissue"], "Which object is shaped like a sphere?",
                      "%s is a mandarin orange. It is round all over, so it is most like a sphere. "
                      "The tin is a cylinder, the hat is a cone and the box is a cuboid.", "four objects labelled A to D"))
    n, she, her = P.next_g()
    its.append(mcq("%s says a ball is a circle. Is %s correct?" % (n, she), "No. A ball is a sphere.",
                   ["Yes. A ball is round.", "No. A ball is a cylinder.", "Yes. A circle can roll."],
                   "A circle is flat. You can draw it on paper. A ball is solid and round all over, so it is a sphere."))
    n, he, his = P.next_b()
    its.append(mcq("%s says a box of tissues is a cube. Is %s correct?" % (n, he), "No. It is a cuboid.",
                   ["Yes. It has 6 flat faces.", "Yes. It is a box.", "No. It is a cylinder."],
                   "A cube and a cuboid both have 6 flat faces. In a cube they are all squares of the same size. "
                   "A box of tissues has long rectangle faces, so it is a cuboid."))
    assert len(its) == 20, len(its)
    return {"title": "3D shapes in real life", "items": its}


# ------------------------------------------------------------ set 3: flat faces and curved faces
def set_faces(pos, P):
    its = []
    its.append(mcq_n(one("cube", "a cube") + "How many flat faces does a cube have?", 6, [3, 4, 5],
                     "A cube has 6 flat faces. In the picture you can see only 3. "
                     "The other 3 are at the back and at the bottom: 3 + 3 = 6."))
    its.append(mcq_n(one("cuboid", "a cuboid") + "How many flat faces does a cuboid have?", 6, [3, 4, 2],
                     "A cuboid has 6 flat faces: top and bottom, front and back, and 2 ends. You can see only 3 of them."))
    its.append(mcq_n(one("cyl", "a cylinder") + "How many flat faces does a cylinder have?", 2, [1, 3, 0],
                     "A cylinder has 2 flat faces: a circle at the top and a circle at the bottom. "
                     "The curved face is not flat, so do not count it."))
    its.append(mcq_n(one("cone", "a cone") + "How many flat faces does a cone have?", 1, [0, 2, 3],
                     "A cone has 1 flat face: the circle at the bottom. The rest is a curved face."))
    its.append(mcq_n(one("sphere", "a sphere") + "How many flat faces does a sphere have?", 0, [1, 2, 6],
                     "A sphere is round all over. It has no flat faces, only a curved face."))
    its.append(mcq_n(one("cyl_lying", "a cylinder") + "How many curved faces does a cylinder have?", 1, [2, 0, 3],
                     "A cylinder has 1 curved face that goes all the way round. Its 2 circle faces are flat."))
    its.append(mcq_n(one("sphere", "a sphere") + "How many curved faces does a sphere have?", 1, [0, 2, 3],
                     "A sphere has 1 curved face that goes all the way round. It has no flat faces."))
    its.append(mcq("What shape is each face of a cube?", "a square", ["a rectangle", "a circle", "a cube"],
                   "All 6 faces of a cube are squares of the same size. The cube is 3D; each face is a flat square."))
    its.append(mcq(one("cuboid", "a cuboid") + "What shape are the faces of this cuboid?", "rectangles",
                   ["circles", "triangles", "cuboids"],
                   "The faces of this cuboid are rectangles. A cuboid is a 3D shape; its faces are flat 2D shapes."))
    its.append(mcq(one("cyl", "a cylinder") + "What shape are the 2 flat faces of a cylinder?", "circles",
                   ["rectangles", "squares", "spheres"],
                   "The flat faces of a cylinder are circles. In a picture they look squashed because we see them from the side."))
    its.append(mcq(one("cone_down", "a cone") + "What shape is the flat face of a cone?", "a circle",
                   ["a triangle", "a square", "a sphere"],
                   "The flat face of a cone is a circle. From the side a cone looks like a triangle, "
                   "but it has no triangle face."))
    its.append(mcq("Which shape has only flat faces?", CUBE, [CYL, CONE, SPH],
                   "A cube has 6 flat faces and no curved face. A cylinder and a cone have a curved face too. "
                   "A sphere has only a curved face."))
    its.append(mcq("Which shape has only a curved face?", SPH, [CYL, CONE, CUBE],
                   "A sphere has 1 curved face and no flat faces. A cylinder and a cone also have flat faces."))
    its.append(mcq("Which shape has 1 flat face and 1 curved face?", CONE, [CYL, SPH, CUBE],
                   "A cone has 1 flat circle face and 1 curved face. A cylinder has 2 flat faces."))
    its.append(mcq("Which shape has 2 flat faces and 1 curved face?", CYL, [CONE, CUBE, SPH],
                   "A cylinder has 2 flat circle faces and 1 curved face. A cone has only 1 flat face."))
    n, she, her = P.next_g()
    its.append(mcq("%s draws around the bottom of a tin of milk. What shape does %s draw?" % (n, she), "a circle",
                   ["a cylinder", "a square", "a rectangle"],
                   "The tin is a cylinder. Its bottom face is a flat circle, so %s draws a circle." % n))
    n, he, his = P.next_b()
    its.append(mcq("%s dips one face of a die in paint and presses it on paper. What shape does %s print?" % (n, he),
                   "a square", ["a cube", "a circle", "a rectangle"],
                   "Every face of a die (a cube) is a square, so the print is a square. A print is flat, so it cannot be a cube."))
    n, she, her = P.next_g()
    its.append(mcq("%s counts the flat faces of a cube in a picture and gets 3. What did %s forget?" % (n, she),
                   "the faces at the back", ["the curved faces", "the circle faces", "nothing"],
                   "A picture shows only 3 faces of a cube. There are 3 more at the back and at the bottom. 3 + 3 = 6 flat faces."))
    its.append(grid_q(pos, "cyl", ["cube", "cuboid", "cuboid_sq"], "Which shape has a curved face?",
                      "%s is a cylinder. It has a curved face. The cube and the cuboids have only flat faces."))
    its.append(grid_q(pos, "sphere", ["cyl", "cone", "cube_turned"], "Which shape has no flat faces?",
                      "%s is a sphere. It has only a curved face. The cylinder has 2 flat faces, the cone has 1 "
                      "and the cube has 6."))
    assert len(its) == 20, len(its)
    return {"title": "Flat faces and curved faces", "items": its}


# ------------------------------------------------------------ set 4: roll, stack or slide
def can(kind):
    f, c, roll, stack, slide = FACTS[kind]
    return {"roll": roll, "stack": stack, "slide": slide}


def do_choice(kind):
    c = can(kind)
    key = (c["roll"], c["stack"], c["slide"])
    return {(True, False, False): "roll only", (False, True, True): "stack and slide only",
            (True, True, True): "roll, stack and slide", (True, False, True): "roll and slide only"}[key]


DO = ["roll only", "stack and slide only", "roll, stack and slide", "roll and slide only"]
SLOPE = {("roll", "curved"): "It rolls: it has a curved face.", ("slide", "flat"): "It slides: it has a flat face.",
         ("roll", "flat"): "It rolls: it has flat faces.", ("slide", "curved"): "It slides: it has a curved face."}


def set_roll(pos, P):
    its = []
    E = {CUBE: "A cube has only flat faces. It can stack and slide on its flat faces. It has no curved face, so it cannot roll.",
         CUBOID: "A cuboid has only flat faces. It can stack and slide. It has no curved face, so it cannot roll.",
         CYL: "A cylinder rolls on its curved face. It stacks and slides on its 2 flat faces. So it can do all three.",
         CONE: "A cone rolls on its curved face and slides on its flat face. It has a pointed tip, so you cannot stack a shape on it.",
         SPH: "A sphere has only a curved face. It rolls, but it cannot stack or slide."}
    for k in ["sphere", "cube", "cyl", "cone", "cuboid_turned"]:
        kind = KIND[k]
        right = do_choice(kind)
        its.append(mcq(one(k) + "What can this shape do?", right, [x for x in DO if x != right], E[kind]))
    its.append(mcq("Which shape can roll and can also be stacked?", CYL, [SPH, CONE, CUBE],
                   "A cylinder rolls on its curved face and stacks on its flat faces. A sphere and a cone roll, "
                   "but you cannot stack on them. A cube stacks, but it cannot roll."))
    its.append(mcq("Which shape can roll but cannot slide?", SPH, [CYL, CONE, CUBOID],
                   "A sphere has no flat face to slide on, so it always rolls. A cylinder and a cone can slide on a flat face."))
    its.append(mcq("Which shape can slide but cannot roll?", CUBOID, [CYL, CONE, SPH],
                   "A cuboid has only flat faces, so it slides but cannot roll. The other shapes have a curved face, so they can roll."))
    its.append(mcq("Why can a sphere roll?", "It has a curved face.",
                   ["It has flat faces.", "It has a pointed tip.", "It is a circle."],
                   "Shapes roll on a curved face. A sphere is curved all over, so it rolls easily."))
    its.append(mcq("Why can you not put a box on top of a cone?", "The cone has a pointed tip.",
                   ["The cone has a flat face.", "The cone can slide.", "The cone has no faces."],
                   "The top of a cone is a pointed tip, not a flat face. A box on top would fall off."))
    for k, how, move, face, e in [
            ("cyl_lying", "lying on its curved face", "roll", "curved",
             "The cylinder is lying on its curved face, so it rolls down the slope."),
            ("cyl", "standing on a flat face", "slide", "flat",
             "The cylinder is standing on a flat circle face. A flat face does not roll, so it slides down."),
            ("cube_turned", "on one of its flat faces", "slide", "flat",
             "A cube has only flat faces, so it cannot roll. It slides down the slope."),
            ("sphere", "", "roll", "curved",
             "A sphere has only a curved face, so it rolls down the slope."),
    ]:
        kind = KIND[k]
        right = SLOPE[(move, face)]
        q = (one(k, "a %s" % kind) + "Mr Tan puts this %s on a slope%s. It moves down the slope. What does it do?"
             % (kind, ", " + how if how else ""))
        its.append(mcq(q, right, [x for x in SLOPE.values() if x != right], e))
    n, he, his = P.next_b()
    its.append(mcq("%s builds a tower of shapes. Which shape can only go at the very top?" % n, CONE, [CUBE, CUBOID, CYL],
                   "A cone has a flat face at the bottom, so it can sit on the tower. Its pointed tip means nothing can go on it. "
                   "Cubes, cuboids and cylinders can go anywhere in the tower."))
    its.append(mcq("A cone lies on its curved face. You push it. How does it roll?", "round in a circle",
                   ["in a straight line", "it cannot roll", "on its flat face"],
                   "A cone rolls round and round its pointed tip, so it moves in a circle. A cylinder rolls in a straight line."))
    its.append(mcq("Which shape can roll in every direction?", SPH, [CYL, CONE, CUBE],
                   "A sphere is curved all over, so it can roll any way. A cylinder rolls only forwards or backwards. "
                   "A cone rolls in a circle. A cube cannot roll."))
    its.append(grid_q(pos, "cyl_lying", ["cube", "cuboid", "cuboid_sq"], "Which shape can roll?",
                      "%s is a cylinder. It rolls on its curved face. The cube and the cuboids have only flat faces, so they cannot roll."))
    its.append(grid_q(pos, "cuboid_turned", ["cyl", "cone", "sphere"], "Which shape can NOT roll?",
                      "%s is a cuboid. It has only flat faces, so it cannot roll. The cylinder, the cone and the sphere "
                      "all have a curved face, so they can roll."))
    n, she, her = P.next_g()
    its.append(mcq("%s says a cylinder cannot roll because it has flat faces. Is %s correct?" % (n, she),
                   "No. It rolls on its curved face.",
                   ["Yes. Flat faces cannot roll.", "Yes. Only a sphere can roll.", "No. It rolls on its flat faces."],
                   "A cylinder has 2 flat faces and 1 curved face. Lying on its curved face, it rolls. "
                   "Standing on a flat face, it can stack or slide."))
    assert len(its) == 20, len(its)
    return {"title": "Roll, stack or slide?", "items": its}


# ------------------------------------------------------------ set 5: sort 3D shapes and word problems
def group_q(keys, ask, right, wrong, e):
    cvs = [pic(k, 0.5) for k in keys]
    svg = row_svg(cvs, [""] * len(cvs), "a group of 3D shapes", gap=14)
    return mcq_n(fig(svg) + ask, right, wrong, e)


def set_sort(pos, P):
    its = []
    # how many in a group (counted from the same list that draws the picture)
    g1 = ["cube", "cyl", "sphere", "cuboid", "cone", "cyl_lying", "cube_turned"]
    k1 = [KIND[k] for k in g1]
    roll = sum(1 for k in k1 if can(k)["roll"])
    assert roll == 4
    its.append(group_q(g1, "How many of these shapes can roll?", roll,
                       [k1.count(CYL) + k1.count(SPH), k1.count(SPH), len(k1)],
                       "The shapes with a curved face can roll: 2 cylinders, 1 sphere and 1 cone. 2 + 1 + 1 = 4. "
                       "Do not forget the cone."))
    g2 = ["cuboid", "cube", "cuboid_tall", "cone", "cube_turned", "cyl", "cuboid_sq"]
    k2 = [KIND[k] for k in g2]
    assert k2.count(CUBOID) == 3 and k2.count(CUBE) == 2
    its.append(group_q(g2, "How many cuboids are there?", k2.count(CUBOID),
                       [k2.count(CUBOID) + k2.count(CUBE), k2.count(CUBOID) - 1, k2.count(CUBOID) + 1],
                       "There are 3 cuboids. The long shape with square ends is a cuboid too: its other 4 faces are long rectangles. "
                       "The 2 cubes are not cuboids: all their faces are squares of the same size."))
    g3 = ["cyl", "sphere", "cube", "cone", "cuboid", "sphere", "cyl_lying"]
    k3 = [KIND[k] for k in g3]
    only_flat = sum(1 for k in k3 if FACTS[k][1] == 0)
    any_flat = sum(1 for k in k3 if FACTS[k][0] > 0)
    assert (only_flat, any_flat) == (2, 5)
    its.append(group_q(g3, "How many of these shapes have only flat faces?", only_flat, [any_flat, 1, len(k3)],
                       "Only the cube and the cuboid have no curved face: 2 shapes. "
                       "The cylinders and the cone have flat faces, but they have a curved face too."))
    its.append(mcq(one("rocket", "a toy rocket") + "Ahmad makes a toy rocket from two 3D shapes. Which two shapes?",
                   "a cylinder and a cone", ["a cylinder and a triangle", "a cuboid and a cone", "a cone and a sphere"],
                   "The bottom part has 2 flat circle faces and a curved face: a cylinder. "
                   "The top has a pointed tip: a cone. A triangle is flat."))
    n, she, her = P.next_g()
    its.append(mcq("%s sorts shapes into two groups.<br>Group A: cube, cuboid<br>Group B: cylinder, cone, sphere<br>"
                   "What is the rule for Group B?" % n, "They can roll.",
                   ["They have only flat faces.", "They can be stacked.", "They have 2 flat faces."],
                   "A cylinder, a cone and a sphere all have a curved face, so they can roll. "
                   "The cube and the cuboid cannot roll."))
    n, he, his = P.next_b()
    its.append(mcq("%s sorts shapes into two groups.<br>Group A: cube, cuboid, cylinder<br>Group B: cone, sphere<br>"
                   "What is the rule for Group A?" % n, "They can be stacked.",
                   ["They can roll.", "They have only flat faces.", "They have a curved face."],
                   "A cube, a cuboid and a cylinder have flat faces at the top and bottom, so they can be stacked. "
                   "A cylinder has a curved face, so “only flat faces” is not the rule."))
    its.append(grid_q(pos, "cone", ["cube", "cyl", "cuboid"], "Three of these shapes can be stacked. Which one cannot?",
                      "%s is a cone. It has a pointed tip, so you cannot stack a shape on it. "
                      "The cube, the cylinder and the cuboid have flat faces at the top and bottom."))
    for q, right, wrong, e in [
            ("I have 6 flat faces. They are all squares. What am I?", CUBE, [CUBOID, "square", SPH],
             "6 flat faces that are all squares of the same size: a cube."),
            ("I can roll. I have 2 flat faces. What am I?", CYL, [CONE, SPH, "circle"],
             "A cylinder rolls on its curved face and has 2 flat circle faces. A cone has only 1 flat face."),
            ("I have only a curved face. I cannot be stacked. What am I?", SPH, ["circle", CONE, CYL],
             "A sphere has 1 curved face and no flat faces. A circle is flat, not a 3D shape."),
            ("I have 1 flat face and a pointed tip. What am I?", CONE, [CYL, "triangle", SPH],
             "A cone has 1 flat circle face and a pointed tip. A triangle is a flat 2D shape."),
    ]:
        its.append(mcq(q, right, wrong, e))
    n, she, her = P.next_g()
    its.append(mcq_n("%s has 2 tins of milk. How many flat faces do the 2 tins have altogether?" % n, 2 + 2, [2, 6, 3],
                     "Each tin is a cylinder with 2 flat faces. 2 + 2 = 4. (6 also counts the curved faces, which are not flat.)"))
    n, he, his = P.next_b()
    its.append(mcq_n("%s has 4 party hats shaped like cones. He draws around the flat face of each hat. "
                     "How many circles does he draw?" % n, 4, [8, 0, 1],
                     "A cone has 1 flat face, a circle. 4 hats give 4 circles. (8 gives each cone 2 flat faces, like a cylinder.)"))
    n, he, his = P.next_b()
    its.append(mcq_n("%s has 3 dice. He counts all the faces of the 3 dice. How many faces are there?" % n, 6 * 3, [9, 6, 12],
                     "Each die is a cube with 6 faces. 6 + 6 + 6 = 18. (9 counts only the 3 faces you can see on each die.)"))
    n, she, her = P.next_g()
    box_ = {CUBE: 1, CUBOID: 2, CYL: 3, SPH: 2, CONE: 1}
    r = sum(v for k, v in box_.items() if can(k)["roll"])
    assert r == 6
    its.append(mcq_n("%s has 1 cube, 2 cuboids, 3 cylinders, 2 spheres and 1 cone. She puts all the shapes that can roll "
                     "in a box. How many shapes are in the box?" % n, r,
                     [box_[SPH], box_[CYL] + box_[SPH], sum(box_.values())],
                     "Cylinders, spheres and cones can roll. 3 + 2 + 1 = 6. Do not forget the cone."))
    # bar models
    a, b = 46, 28
    its.append(mcq_n(fig(bar_svg([("Cubes", [(a, False)], [(0, 0, str(a))]),
                                  ("Cylinders", [(b, False), (a - b, True)], [(0, 0, str(b))], "?")],
                                 label="bar model: cubes and cylinders"))
                     + "Mrs Lim has %d cubes and %d cylinders. How many more cubes than cylinders does she have?" % (a, b),
                     a - b, [a + b, 22, 28],
                     "Find the difference: %d − %d = %d. Rename 1 ten as 10 ones: 16 − 8 = 8, 3 − 2 = 1. "
                     "(22 comes from 8 − 6 instead of renaming.)" % (a, b, a - b)))
    a, b = 35, 27
    n, he, his = P.next_b()
    its.append(mcq_n(fig(bar_svg([("Shapes", [(a, False), (b, False)], [(0, 0, "%d cuboids" % a), (1, 1, "%d cones" % b)])],
                                 total="?", label="bar model: cuboids and cones"))
                     + "%s uses %d cuboids and %d cones to build a model. How many shapes does he use altogether?" % (n, a, b),
                     a + b, [52, 8, 512],
                     "Add the parts: %d + %d = %d. 5 + 7 = 12 ones: rename 10 ones as 1 ten. "
                     "(52 forgets the new ten; 512 writes 12 next to 5.)" % (a, b, a + b)))
    its.append(mcq_n(fig(bar_svg([("Balls", [(5, False)] * 4, [(i, i, "5") for i in range(4)])], total="?",
                                 label="bar model: 4 boxes of balls"))
                     + "A shop packs 5 balls in each box. How many balls are there in 4 boxes?", 4 * 5, [9, 25, 15],
                     "1 unit = 5 balls. 4 units = 4 × 5 = 20 balls. (9 adds 4 + 5 instead.)"))
    n, she, her = P.next_g()
    its.append(mcq_n(fig(bar_svg([("Marbles", [(8, False)] * 3, [(0, 0, "?")])], total="24",
                                 label="bar model: 24 marbles in 3 bags"))
                     + "%s has 24 marbles. She puts them equally into 3 bags. How many marbles are in each bag?" % n,
                     24 // 3, [21, 27, 72],
                     "3 units = 24. 1 unit = 24 ÷ 3 = 8 marbles. (21 takes away 3 instead of dividing.)"))
    its.append(mcq_n(fig(bar_svg([("Shapes", [(18, False), (32, False)], [(0, 0, "18 cones"), (1, 1, "?")])],
                                 total="50", label="bar model: 50 shapes"))
                     + "There are 50 shapes in a box. 18 are cones. The rest are cylinders. How many cylinders are there?",
                     50 - 18, [68, 48, 42],
                     "Whole − part: 50 − 18 = 32. Rename 1 ten as 10 ones: 10 − 8 = 2, 4 − 1 = 3. "
                     "(48 comes from 8 − 0; 68 adds instead of subtracting.)"))
    assert len(its) == 20, len(its)
    return {"title": "Sort 3D shapes and word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % x for x in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    five = row_svg([pic("cube", 0.8), pic("cuboid", 0.75), pic("cyl", 0.8), pic("cone", 0.8), pic("sphere", 0.8)],
                   ["cube", "cuboid", "cylinder", "cone", "sphere"],
                   "a cube, a cuboid, a cylinder, a cone and a sphere", gap=22)
    real = row_svg([pic("die", 0.8), pic("tissue", 0.75), pic("tin", 0.8), pic("icecream", 0.8), pic("ball", 0.8)],
                   ["die", "tissue box", "tin of milk", "ice cream cone", "ball"],
                   "a die, a box of tissues, a tin of milk, an ice cream cone and a ball", gap=18)
    pair = row_svg([pic("cube", 0.8), pic("cuboid_sq", 0.8), pic("circle2d", 0.8), pic("sphere", 0.8)],
                   ["cube", "cuboid", "circle (2D)", "sphere (3D)"],
                   "a cube next to a cuboid, and a circle next to a sphere", gap=26)
    model = bar_svg([("Cubes", [(15, False)], [(0, 0, "15")]), ("Cones", [(9, False), (6, True)], [(0, 0, "9")], "?")],
                    label="bar model: 15 cubes and 9 cones")
    yes, no = "yes", "no"
    return (
        "<h2>The five 3D shapes</h2>"
        "<p>A 3D shape is solid. You can hold it. A <b>flat face</b> is flat, like a table top. "
        "A <b>curved face</b> is round, like the side of a ball.</p>"
        "<figure class='sn-fig'>" + five +
        "<figcaption>A cube and a cuboid have only flat faces. A cylinder, a cone and a sphere have a curved face.</figcaption></figure>"
        + table(["Shape", "Flat faces", "Curved faces", "Real object"], [
            ["Cube", "6 squares", "0", "a die"],
            ["Cuboid", "6 rectangles", "0", "a box of tissues"],
            ["Cylinder", "2 circles", "1", "a tin of milk"],
            ["Cone", "1 circle", "1", "an ice cream cone"],
            ["Sphere", "0", "1", "a ball"]]) +
        "<figure class='sn-fig'>" + real +
        "<figcaption>Look for these shapes around you: at home, in class and at the hawker centre.</figcaption></figure>" +
        ex("Example 1", "How many flat faces does a cube have?",
           "A picture shows 3 faces. 3 more are at the back and at the bottom. 3 + 3 = 6.", "6 flat faces") +
        "<h2>Roll, stack or slide?</h2>"
        "<p>A shape <b>rolls</b> on a curved face. It <b>slides</b> on a flat face. "
        "You can <b>stack</b> shapes that have flat faces at the top and bottom.</p>" +
        table(["Shape", "Roll?", "Stack?", "Slide?"], [
            ["Cube", no, yes, yes], ["Cuboid", no, yes, yes], ["Cylinder", yes, yes, yes],
            ["Cone", yes, "no (pointed tip)", yes], ["Sphere", yes, no, no]]) +
        ex("Example 2", "Which shape can roll and can also be stacked?",
           "It needs a curved face to roll and flat faces to stack. A cylinder has both.", "a cylinder") +
        "<h2>Sort and solve</h2>"
        "<p>Sort shapes by what they have (flat or curved faces) or what they can do (roll, stack, slide). "
        "Use a bar model for word problems.</p>" +
        "<figure class='sn-fig'>" + model +
        "<figcaption>The bar for the cones is shorter. The dashed part is the difference.</figcaption></figure>" +
        ex("Example 3", "Wei Ming has 15 cubes and 9 cones. How many more cubes than cones does he have?",
           "Look at the bar model. Find the difference: 15 − 9 = 6.", "6 more cubes") +
        "<h2>Common mistakes</h2>"
        "<figure class='sn-fig'>" + pair +
        "<figcaption>A cuboid can have square ends, but its other faces are long. A circle is flat; a sphere is solid.</figcaption></figure>" +
        table(["Mistake", "What to do instead"], [
            ["Calling a long box a cube", "A cube has 6 squares of the same size. Any other box is a cuboid"],
            ["Calling a ball a circle", "A circle is flat (2D). A ball is a sphere (3D)"],
            ["Mixing up a cylinder and a cone", "A cone has 1 flat face and a pointed tip. A cylinder has 2 flat faces"],
            ["Calling a cone a triangle", "A triangle is flat. A cone has a curved face"],
            ["Counting only the faces you can see", "Count the faces at the back and at the bottom too"],
            ["Saying a cylinder cannot roll", "It rolls on its curved face"],
        ])
    )


FAQ = [
    {"q": "What 3D shapes do P2 students learn?",
     "a": "Primary 2 students learn to name, describe and sort five 3D shapes: cube, cuboid, cylinder, cone and sphere. "
          "They look at flat and curved faces and at which shapes can roll, stack or slide."},
    {"q": "How do I explain the difference between a cube and a cuboid to my child?",
     "a": "A cube has 6 faces that are all squares of the same size, like a die. A cuboid has rectangle faces, "
          "like a box of tissues or a shoebox."},
    {"q": "What is the most common mistake with 3D shapes in P2?",
     "a": "Children often use 2D names for 3D shapes, such as calling a ball a circle or an ice cream cone a triangle. "
          "Let them hold real objects and feel the flat and curved faces."},
    {"q": "Is this topic in the MOE syllabus?",
     "a": "Yes. Identifying, naming, describing and classifying the cube, cuboid, cone, cylinder and sphere is part of "
          "Geometry in the MOE 2021 Primary 2 Mathematics syllabus."},
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
    """Tag pictures that must print larger (A-D choices, rows of shapes, bar models)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


class People2(People):
    """Girls and boys drawn separately, so the pronoun in a question always fits."""

    def __init__(self, rnd):
        self.g = [(n, "she", "her") for n in GIRLS]
        self.b = [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.g)
        rnd.shuffle(self.b)
        self.i = self.j = 0

    def next_g(self):
        p = self.g[self.i % len(self.g)]
        self.i += 1
        return p

    def next_b(self):
        p = self.b[self.j % len(self.b)]
        self.j += 1
        return p


def gen():
    rnd = random.Random(62812)
    P = People2(rnd)
    sets = [set_name(Pos(rnd)), set_real(Pos(rnd), P), set_faces(Pos(rnd), P), set_roll(Pos(rnd), P), set_sort(Pos(rnd), P)]
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
        "country": "sg", "subject": "maths", "grade": "primary-2", "slug": "3d-shapes", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 2 3D Shapes: Cube, Cuboid, Cylinder, Cone and Sphere",
        "seo_title": "P2 3D Shapes Worksheets: Free Primary 2 Maths with Answers (MOE Syllabus)",
        "short_title": "3D shapes",
        "domain": "Measurement and Geometry",
        "standard_code": "Primary 2: Geometry",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Identifying, naming, describing and classifying 3D shapes: cube, cuboid, cone, cylinder, sphere",
        "meta_desc": "Free P2 maths practice: name cubes, cuboids, cylinders, cones and spheres, count flat and curved "
                     "faces, roll, stack or slide. 100 questions with answers.",
        "key_big": "A cube has 6 square faces of the same size; any other box is a cuboid.",
        "key_sub": "A cylinder has 2 flat faces and 1 curved face, so it can roll, stack and slide.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(u, "(four pictures labelled A to D|four objects labelled A to D|the same 3D shape in two positions|"
                         "a group of 3D shapes|bar model)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
