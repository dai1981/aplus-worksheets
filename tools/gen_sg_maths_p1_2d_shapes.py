# -*- coding: utf-8 -*-
"""
Singapore Primary 1 Maths: 2D Shapes
(MOE 2021 Primary Mathematics Syllabus, Standard. Primary 1: Geometry)
  python3 tools/gen_sg_maths_p1_2d_shapes.py
Identifying, naming, describing and classifying rectangle, square, triangle, circle, half circle and
quarter circle; forming figures with shapes; copying and completing figures on a dot grid.
HTML attributes use single quotes (no backslashes in the JSON). Singapore English. 6-7-year-olds:
very short sentences and a picture in almost every question.

Rules kept everywhere (so every answer is right for every definition):
  - a square picture never has "rectangle" as a wrong answer, and no question asks "how many rectangles"
    in a figure that has a square
  - colour, size and turning never change the name
  - curved shapes are counted by "straight sides"; corners: half circle 2, quarter circle 3
Pictures are drawn from their corner points and checked in code (number of sides, square corners,
squares really square). Figures made of shapes are built from pieces, and every count is taken from
the pieces. Dot-grid copies are checked in code: the right copy is the figure moved, and every wrong
copy is NOT the same shape and size even when turned or flipped.
Wrong answers come from real mistakes: a turned square called a diamond, half circle vs quarter circle,
a quarter circle called a triangle (3 corners), a circle cut into unequal parts called half circles,
missing the upside-down triangle in the middle, a side one dot too long or too short on a dot grid.
Drawing helpers adapted from tools/gen_cabc_math_g1_shapes.py.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-1")
UPDATED = "2026-11-03"
GREEN = "#006633"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
DOT = "#8a8378"
FONT = "Arial, Helvetica, sans-serif"
# (fill, line) pairs for flat shapes: colour must never change the name
COLS = [("#cfe6d6", "#006633"), ("#cfe0f3", "#1f5f99"), ("#fbe7a6", "#8a6100"),
        ("#f6cfd8", "#a33b5a"), ("#e2d6f0", "#5b3f8c")]
GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Kumar", "Arjun", "Ethan", "Ryan"]

TRI, SQ, REC, CIR, HALF, QUAR = "triangle", "square", "rectangle", "circle", "half circle", "quarter circle"


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


def txt(x, y, t, fs=16, col=INK, anchor="middle"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


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

    def circle(self, c, r, fill=COLS[0][0], sw=2.4, col=GREEN):
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

    def rect(self, x0, y0, x1, y1, col=GRAY, sw=1.5):
        self.el.append(("r", x0, y0, x1, y1, col, sw))
        self.grow(x0 - sw, y0 - sw, x1 + sw, y1 + sw)

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
                s.append(txt(x - ox, y - oy, t, fs, col))
            elif e[0] == "r":
                _, x0, y0, x1, y1, col, sw = e
                s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='6' fill='none' stroke='%s' stroke-width='%g'/>"
                         % (x0 - ox, y0 - oy, x1 - x0, y1 - y0, col, sw))
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
            parts.append(txt(x + cw / 2, H + 8 + fs * 0.86, cap, fs, col))
        x += cw + gap
    W = x - gap
    pad = 5
    capH = 8 + fs * 1.1 if any(caps) else 0
    body = "<g transform='translate(%d,%d)'>%s</g>" % (pad, pad, "".join(parts))
    return svg_wrap(int(math.ceil(W + 2 * pad)), int(math.ceil(H + capH + 2 * pad)), body, label)


def grid_cells(cvs, x0=0, cell=118, ch=None):
    """2 x 2 cells of pictures labelled A-D (SVG parts), starting at x0."""
    ch = ch or cell
    s = ["<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x0 + cell, x0 + cell, 2 * ch - 4, GRAY),
         "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x0 + 4, ch, x0 + 2 * cell - 4, ch, GRAY)]
    for k, cv in enumerate(cvs):
        cx, cy = x0 + (k % 2) * cell, (k // 2) * ch
        aw, ah = cell - 26, ch - 10
        w, h = cv.size()
        f = min(1.0, aw / w, ah / h)                  # shrink a picture if it is too big for its cell
        assert f > 0.55, ("too big for the grid", w, h)
        tx = cx + 21 + (aw - w * f) / 2
        ty = cy + 5 + (ah - h * f) / 2
        s.append("<g transform='translate(%.1f,%.1f) scale(%.3f)'>%s</g>" % (tx, ty, f, cv.body(cv.x0, cv.y0)))
        s.append(txt(cx + 5, cy + 22, "ABCD"[k], 18, INK, "start"))
    return "".join(s)


def grid_svg(cvs, label, cell=118):
    return svg_wrap(2 * cell, 2 * cell, grid_cells(cvs, 0, cell), label)


def grid_q(pos, q, right, others, why, label="four shapes labelled A to D", maker=grid_svg):
    """A-D picture question. why has %s for the letter."""
    p = pos.next()
    cells = list(others)
    cells.insert(p, right)
    L = "ABCD"[p]
    return mcq_fixed(fig(maker(cells, label)) + q, list("ABCD"), L, why % L)


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


def classify(pts):
    """Name of a polygon from its corner points: triangle, square, rectangle or 'other'."""
    check_poly(pts)
    n = len(pts)
    if n == 3:
        return TRI
    if n == 4:
        L = [math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]) for i in range(4)]
        right = all(abs((pts[i][0] - pts[i - 1][0]) * (pts[(i + 1) % 4][0] - pts[i][0])
                        + (pts[i][1] - pts[i - 1][1]) * (pts[(i + 1) % 4][1] - pts[i][1])) < 1e-6 * max(L) ** 2
                    for i in range(4))
        if right:
            return SQ if max(L) - min(L) < 1e-6 * max(L) else REC
    return "other"


SHAPES2D = {
    "tri_eq": reg(3, 46),
    "tri_right": [(0, 0), (0, 70), (90, 70)],
    "tri_thin": [(0, 0), (120, 25), (25, 58)],
    "tri_tall": [(0, 90), (30, 0), (60, 90)],
    "square": [(0, 0), (70, 0), (70, 70), (0, 70)],
    "rect": [(0, 0), (110, 0), (110, 55), (0, 55)],
    "rect_long": [(0, 0), (130, 0), (130, 40), (0, 40)],
    "diamond": [(0, -50), (28, 0), (0, 50), (-28, 0)],      # thin rhombus: NOT a square
}
for _k, _p in SHAPES2D.items():
    _kind = classify(_p)
    assert _kind == {"tri": TRI, "squ": SQ, "rec": REC, "dia": "other"}[_k[:3]], (_k, _kind)
    if _kind == REC:
        _L = [math.hypot(_p[i][0] - _p[i - 1][0], _p[i][1] - _p[i - 1][1]) for i in range(4)]
        assert max(_L) / min(_L) >= 2                  # clearly not a square


def arc(cx, cy, r, a0, a1, n=40):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def half_pts(cx, cy, r, a0):
    """Half circle: the arc from a0 to a0 + 180 (screen angles, y down) and the straight side back."""
    return arc(cx, cy, r, a0, a0 + 180)


def quarter_pts(cx, cy, r, a0):
    """Quarter circle: the square corner at the centre, the arc from a0 to a0 + 90."""
    return [(cx, cy)] + arc(cx, cy, r, a0, a0 + 90, 24)


def flat(key, deg=0, s=1.0, c=0):
    """Any flat shape by key. s scales it. Half circle 'half' + a0, quarter circle 'quarter' + a0."""
    cv = Canvas()
    if key == "circle":
        cv.circle((0, 0), 38 * s, fill=COLS[c][0], sw=3, col=COLS[c][1])
    elif key == "oval":
        cv.poly([(48 * s * math.cos(math.radians(a)), 28 * s * math.sin(math.radians(a))) for a in range(0, 360, 5)],
                COLS[c][0], 3, COLS[c][1])
    elif key == "half":
        cv.poly(half_pts(0, 0, 50 * s, 180 + deg), COLS[c][0], 3, COLS[c][1])
    elif key == "quarter":
        cv.poly(quarter_pts(0, 0, 62 * s, 270 + deg), COLS[c][0], 3, COLS[c][1])
    else:
        pts = tpts(SHAPES2D[key], deg, s)
        check_poly(pts)
        cv.poly(pts, COLS[c][0], 3, COLS[c][1])
    return cv


def kind_of(key):
    return {"circle": CIR, "oval": "oval", "half": HALF, "quarter": QUAR}.get(key) or classify(SHAPES2D[key])


def cut_circle(mode, r=40, c=1, fill=None, line=None):
    """A circle with cut lines. mode: half, chord_v, chord_h, quarters, cross_off, thirds."""
    fill, line = fill or COLS[c][0], line or COLS[c][1]
    cv = Canvas()
    cv.circle((0, 0), r, fill=fill, sw=3, col=line)
    seg = lambda a, b: cv.line(a, b, sw=2.6, col=INK)
    if mode == "half":
        seg((0, -r), (0, r))
    elif mode == "half_h":
        seg((-r, 0), (r, 0))
    elif mode in ("chord_v", "chord_h"):
        d = 0.45 * r
        h = math.sqrt(r * r - d * d)
        seg((d, -h), (d, h)) if mode == "chord_v" else seg((-h, -d), (h, -d))
    elif mode == "quarters":
        seg((0, -r), (0, r))
        seg((-r, 0), (r, 0))
    elif mode == "cross_off":
        dx, dy = 0.4 * r, 0.35 * r
        hy = math.sqrt(r * r - dx * dx)
        hx = math.sqrt(r * r - dy * dy)
        seg((dx, -hy), (dx, hy))
        seg((-hx, dy), (hx, dy))
    elif mode == "thirds":
        for a in (-90, 30, 150):
            seg((0, 0), (r * math.cos(math.radians(a)), r * math.sin(math.radians(a))))
    else:
        raise KeyError(mode)
    return cv


# ------------------------------------------------------------ figures made of shapes
def Pc(pts, c):
    return {"k": classify(pts), "t": "p", "pts": pts, "c": c}


def Cc(cx, cy, r, c):
    return {"k": CIR, "t": "c", "cxy": (cx, cy), "r": r, "c": c}


def Hc(cx, cy, r, a0, c):
    return {"k": HALF, "t": "p", "pts": half_pts(cx, cy, r, a0), "c": c}


def Qc(cx, cy, r, a0, c):
    return {"k": QUAR, "t": "p", "pts": quarter_pts(cx, cy, r, a0), "c": c}


def rect_pts(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def comp_cv(pieces, s=1.0):
    cv = Canvas()
    for p in pieces:
        f, l = COLS[p["c"]]
        if p["t"] == "c":
            cv.circle((p["cxy"][0] * s, p["cxy"][1] * s), p["r"] * s, fill=f, sw=2.4, col=l)
        else:
            cv.poly([(x * s, y * s) for x, y in p["pts"]], f, 2.4, l)
    return cv


def count(pieces, kind):
    return sum(1 for p in pieces if p["k"] == kind)


def kinds(pieces):
    return sorted(set(p["k"] for p in pieces))


def F_house():
    return [Pc(rect_pts(0, 40, 60, 100), 1), Pc([(-8, 40), (68, 40), (30, 0)], 3)]


def F_rocket():
    return [Pc(rect_pts(20, 30, 50, 110), 1), Pc([(20, 30), (50, 30), (35, 0)], 3),
            Pc([(20, 80), (20, 110), (0, 110)], 2), Pc([(50, 80), (70, 110), (50, 110)], 2)]


def F_sun(n=6):
    ps = [Cc(0, 0, 28, 2)]
    for k in range(n):
        t = -90 + 360 * k / n
        P = lambda rr, a: (rr * math.cos(math.radians(a)), rr * math.sin(math.radians(a)))
        ps.append(Pc([P(34, t - 15), P(56, t), P(34, t + 15)], 2))
    return ps


def F_train():
    return [Pc(rect_pts(0, 35, 60, 75), 1), Pc(rect_pts(60, 25, 110, 75), 3)] + \
           [Cc(x, 86, 11, 4) for x in (15, 45, 72, 98)]


def F_robot():
    return [Pc(rect_pts(25, 0, 55, 30), 2), Pc(rect_pts(15, 30, 65, 100), 1),
            Pc(rect_pts(0, 35, 15, 80), 3), Pc(rect_pts(65, 35, 80, 80), 3),
            Pc(rect_pts(22, 100, 37, 135), 4), Pc(rect_pts(43, 100, 58, 135), 4)]


def F_boat():
    return [Hc(50, 60, 45, 0, 1), Pc(rect_pts(47, 0, 53, 60), 2), Pc([(53, 6), (90, 54), (53, 54)], 3)]


def F_icecream():
    return [Pc([(0, 40), (50, 40), (25, 112)], 2), Hc(25, 40, 25, 180, 3)]


def F_kite():
    V = [(0, -48), (40, 0), (0, 48), (-40, 0)]
    V = [(0, -45), (45, 0), (0, 45), (-45, 0)]
    return [Pc([(0, 0), V[i], V[(i + 1) % 4]], i % 2 + 1) for i in range(4)]


def F_bigtri():
    A, B, C = (0, 90), (104, 90), (52, 0)
    ab, bc, ca = (52, 90), (78, 45), (26, 45)
    return [Pc([A, ab, ca], 0), Pc([ab, B, bc], 0), Pc([ca, bc, C], 0), Pc([ca, ab, bc], 2)]


def F_rectcut():
    return [Pc([(0, 0), (110, 0), (110, 55)], 1), Pc([(0, 0), (110, 55), (0, 55)], 2)]


def F_flower():
    return [Pc(rect_pts(0, 0, 40, 40), 2), Hc(20, 0, 20, 180, 3), Hc(20, 40, 20, 0, 3),
            Hc(0, 20, 20, 90, 3), Hc(40, 20, 20, 270, 3)]


def F_caterpillar():
    return [Cc(28 * i, 0, 14, i % 2) for i in range(5)]


def F_tree():
    return [Pc([(0, 70), (80, 70), (40, 0)], 0), Pc(rect_pts(32, 70, 48, 106), 2)]


def F_umbrella():
    return [Hc(50, 50, 50, 180, 4), Pc(rect_pts(47, 50, 53, 102), 2)]


def F_two_tri_square():
    return [Pc([(0, 0), (70, 0), (0, 70)], 1), Pc([(70, 0), (70, 70), (0, 70)], 3)]


def F_two_squares():
    return [Pc(rect_pts(0, 0, 55, 55), 2), Pc(rect_pts(55, 0, 110, 55), 4)]


def F_nine_squares():
    return [Pc(rect_pts(30 * i, 30 * j, 30 * i + 30, 30 * j + 30), (i + j) % 2 + 1) for i in range(3) for j in range(3)]


def union_kind(pieces):
    """Outline of pieces that fill a rectangle exactly: square or rectangle (checked by area)."""
    xs = [x for p in pieces for x, _ in p["pts"]]
    ys = [y for p in pieces for _, y in p["pts"]]
    box = rect_pts(min(xs), min(ys), max(xs), max(ys))

    def area(pts):
        return abs(sum(pts[i - 1][0] * pts[i][1] - pts[i][0] * pts[i - 1][1] for i in range(len(pts)))) / 2
    assert abs(sum(area(p["pts"]) for p in pieces) - area(box)) < 1e-6
    return classify(box)


# ------------------------------------------------------------ dot grids
S_DOT = 16


def dot_cv(cols, rows, S=S_DOT, polys=(), plines=(), c=1, segs=()):
    """A dot grid (cols x rows dots). polys are lists of grid points (filled shapes)."""
    cv = Canvas()
    for i in range(cols):
        for j in range(rows):
            cv.circle((i * S, j * S), 2.2, fill=DOT, sw=0)
    P = lambda p: (p[0] * S, p[1] * S)
    for pts in polys:
        for x, y in pts:
            assert 0 <= x < cols and 0 <= y < rows, ("off the grid", pts)
        cv.poly([P(p) for p in pts], COLS[c][0], 2.6, COLS[c][1])
    for a, b in segs:
        cv.line(P(a), P(b), sw=2.2, col=COLS[c][1])
    for pts in plines:
        cv.pline([P(p) for p in pts], sw=3, col=COLS[c][1])
    return cv


def canon(pts):
    """Edges of a grid polygon after moving it to the corner (to compare copies)."""
    mx, my = min(p[0] for p in pts), min(p[1] for p in pts)
    q = [(x - mx, y - my) for x, y in pts]
    return frozenset(frozenset((q[i - 1], q[i])) for i in range(len(q)))


def symmetries(pts):
    out = []
    for flip in (False, True):
        for t in range(4):
            q = [(-x, y) if flip else (x, y) for x, y in pts]
            for _ in range(t):
                q = [(-y, x) for x, y in q]
            out.append(canon(q))
    return out


def fit_shift(pts, cols, rows, rnd):
    """Move a grid figure to a random place that fits on the grid."""
    mx, my = min(p[0] for p in pts), min(p[1] for p in pts)
    w, h = max(p[0] for p in pts) - mx, max(p[1] for p in pts) - my
    assert w < cols and h < rows, pts
    dx = rnd.randint(0, cols - 1 - w) - mx
    dy = rnd.randint(0, rows - 1 - h) - my
    return [(x + dx, y + dy) for x, y in pts]


def copy_svg(orig_cv, cvs, label, cell=112, ch=96):
    """The figure in a box on the left, four copies labelled A-D on the right."""
    ow, oh = orig_cv.size()
    left = ow + 34
    H = 2 * ch
    bx0, by0 = 8, (H - oh) / 2 - 12
    s = ["<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='6' fill='none' stroke='%s' stroke-width='2'/>"
         % (bx0, by0, ow + 18, oh + 24, INK)]
    s.append("<g transform='translate(%.1f,%.1f)'>%s</g>" % (bx0 + 9, by0 + 12, orig_cv.body(orig_cv.x0, orig_cv.y0)))
    s.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>" % (left, left, H - 4, INK))
    s.append(grid_cells(cvs, left + 4, cell, ch))
    return svg_wrap(int(left + 4 + 2 * cell), H, "".join(s), label)


# ------------------------------------------------------------ set 1: name the shape
WRONG1 = {
    CIR: ["oval", HALF, SQ],
    TRI: [QUAR, SQ, REC],
    SQ: ["diamond", TRI, CIR],                  # never "rectangle": a square is a special rectangle
    REC: [SQ, TRI, HALF],
    HALF: [QUAR, CIR, TRI],
    QUAR: [HALF, TRI, CIR],
}
E1 = {
    CIR: "It is round. It has no corners. It is a circle.",
    TRI: "It has 3 straight sides and 3 corners. It is a triangle.",
    SQ: "It has 4 straight sides. All 4 sides are the same length. It is a square.",
    REC: "It has 4 straight sides and 4 square corners. 2 sides are long. 2 sides are short. It is a rectangle.",
    HALF: "It is half of a circle. It has 1 straight side and 1 curved side. It is a half circle.",
    QUAR: "It is a quarter of a circle. It has 2 straight sides and 1 curved side. It is a quarter circle.",
}


def set_name(rnd, pos):
    its = []
    asks = ["What shape is this?", "Name this shape.", "What is this shape called?"]
    plan = [  # key, turn, scale, colour, note
        ("circle", 0, 1.0, 1, ""),
        ("circle", 0, 0.55, 3, " It is small. It is still a circle."),
        ("tri_eq", 0, 1.0, 0, ""),
        ("tri_eq", 180, 0.8, 3, " It is upside down. It is still a triangle."),
        ("tri_right", 0, 0.9, 2, " It has a square corner. It is still a triangle."),
        ("square", 0, 1.0, 3, ""),
        ("square", 45, 0.9, 4, " It stands on a corner. Some children say “diamond”. It is still a square."),
        ("square", 20, 0.6, 0, " It is small and turned. It is still a square."),
        ("rect", 0, 1.0, 2, ""),
        ("rect", 90, 0.85, 1, " It is standing up. It is still a rectangle."),
        ("rect_long", 25, 0.85, 4, " It is tilted. It is still a rectangle."),
        ("half", 0, 1.0, 0, ""),
        ("half", 180, 0.8, 2, " It is upside down. It is still a half circle."),
        ("half", 90, 0.85, 4, " It is turned. It is still a half circle."),
        ("quarter", 0, 1.0, 1, ""),
        ("quarter", 180, 0.8, 3, " It is turned. It is still a quarter circle."),
    ]
    for i, (key, deg, s, c, note) in enumerate(plan):
        kind = kind_of(key)
        its.append(mcq(fig(flat(key, deg, s, c).svg("a flat shape")) + asks[i % 3], kind, WRONG1[kind], E1[kind] + note))
    its.append(grid_q(pos, "Which shape is a half circle?", flat("half", 270, 0.8, 1),
                      [flat("quarter", 90, 0.85, 2), flat("circle", 0, 0.9, 0), flat("tri_eq", 0, 0.85, 4)],
                      "%s is half of a circle. It has 1 straight side. The quarter circle has 2 straight sides."))
    its.append(grid_q(pos, "Which shape is a quarter circle?", flat("quarter", 90, 0.9, 4),
                      [flat("half", 0, 0.8, 3), flat("tri_right", 0, 0.85, 1), flat("circle", 0, 0.9, 2)],
                      "%s has 2 straight sides and 1 curved side. It is a quarter circle. The triangle has no curved side."))
    its.append(grid_q(pos, "Which shape is a square?", flat("square", 45, 0.85, 3),
                      [flat("rect", 0, 0.75, 2), flat("diamond", 0, 0.9, 1), flat("tri_eq", 0, 0.9, 0)],
                      "%s has 4 sides the same length and 4 square corners. It stands on a corner. It is still a square."))
    its.append(grid_q(pos, "Which shape is a triangle?", flat("tri_tall", 180, 0.9, 1),
                      [flat("square", 0, 0.9, 2), flat("quarter", 0, 0.9, 0), flat("rect", 90, 0.8, 4)],
                      "%s has 3 straight sides. It points down. It is still a triangle. The quarter circle has a curved side."))
    assert len(its) == 20, len(its)
    return {"title": "Name the shape", "items": its}


# ------------------------------------------------------------ set 2: sides and corners
ORDER = [REC, SQ, TRI, CIR, HALF, QUAR]
SIDES = {CIR: 0, TRI: 3, SQ: 4, REC: 4, HALF: 1, QUAR: 2}         # straight sides
CORNERS = {CIR: 0, TRI: 3, SQ: 4, REC: 4, HALF: 2, QUAR: 3}


def rule_q(cells, right, wrong, e, ask="These shapes are in one group. What is the same?"):
    return mcq(fig(row_svg(cells, [""] * len(cells), "a row of shapes in one group", gap=18)) + ask, right, wrong, e)


def set_sides(rnd, pos, P):
    its = []
    for key, deg, s, c, q, n, wrong, e in [
            ("tri_eq", 0, 0.9, 1, "How many straight sides does this shape have?", 3, [2, 4, 6],
             "Count the sides: 1, 2, 3. A triangle has 3 straight sides."),
            ("square", 45, 0.75, 2, "How many corners does this square have?", 4, [2, 3, 5],
             "Count the corners: 1, 2, 3, 4. A square has 4 corners, even when it is turned."),
            ("rect_long", 25, 0.8, 3, "How many corners does this shape have?", 4, [2, 3, 5],
             "Count the corners: 1, 2, 3, 4. A rectangle has 4 corners, even when it is tilted."),
            ("circle", 0, 0.8, 0, "How many corners does a circle have?", 0, [1, 2, 4],
             "A circle is round all the way. It has no corners: 0."),
            ("half", 0, 0.9, 4, "How many straight sides does a half circle have?", 1, [0, 2, 3],
             "A half circle has 1 straight side. The other side is curved."),
            ("half", 180, 0.8, 1, "How many corners does a half circle have?", 2, [0, 1, 3],
             "The corners are where the straight side meets the curved side. There are 2 corners."),
            ("quarter", 0, 0.9, 2, "How many straight sides does a quarter circle have?", 2, [1, 3, 4],
             "A quarter circle has 2 straight sides and 1 curved side."),
            ("quarter", 90, 0.85, 3, "How many corners does a quarter circle have?", 3, [2, 4, 1],
             "There is 1 square corner and 2 corners at the ends of the curved side. 1 + 2 = 3 corners."),
    ]:
        kind = kind_of(key)
        assert n == (SIDES[kind] if "sides" in q else CORNERS[kind]), q
        its.append(mcq(fig(flat(key, deg, s, c).svg("a flat shape")) + q, n, wrong, e))
    # riddles
    for q, right, wrong, e in [
            ("I have 3 straight sides and 3 corners. What am I?", "a triangle", ["a quarter circle", "a square", "a rectangle"],
             "A triangle has 3 straight sides. A quarter circle has only 2 straight sides."),
            ("I have 4 straight sides. 2 are long and 2 are short. What am I?", "a rectangle", ["a square", "a triangle", "a half circle"],
             "A rectangle has 2 long sides and 2 short sides. A square has 4 sides the same length."),
            ("I am round. I have no corners. What am I?", "a circle", ["a half circle", "a quarter circle", "a square"],
             "A circle is round all the way. A half circle has 2 corners."),
            ("I have 1 straight side and 1 curved side. What am I?", "a half circle", ["a quarter circle", "a circle", "a triangle"],
             "A half circle has 1 straight side and 1 curved side. A quarter circle has 2 straight sides."),
            ("I have 2 straight sides and 1 curved side. What am I?", "a quarter circle", ["a half circle", "a triangle", "a circle"],
             "A quarter circle has 2 straight sides and 1 curved side."),
    ]:
        k = right[2:]
        pic = {TRI: ("tri_eq", 0, 0.6, 0), SQ: ("square", 0, 0.6, 1), REC: ("rect", 0, 0.5, 3), CIR: ("circle", 0, 0.6, 4),
               HALF: ("half", 0, 0.6, 2), QUAR: ("quarter", 0, 0.6, 1)}
        names = sorted([right] + wrong, key=lambda x: ORDER.index(x[2:]))
        row = row_svg([flat(*pic[x[2:]]) for x in names], [x[2:] for x in names], "a row of shapes with their names", gap=16, fs=14)
        its.append(mcq(fig(row) + q, right, wrong, e))
        if "straight side" in q:
            assert ("%d straight" % SIDES[k]) in q, q
    its.append(grid_q(pos, "Which shape is the odd one out?", flat("square", 0, 0.8, 2),
                      [flat("tri_eq", 180, 0.8, 0), flat("tri_thin", 20, 0.65, 3), flat("tri_right", 0, 0.75, 1)],
                      "%s has 4 sides. It is a square. The others have 3 sides. They are triangles."))
    its.append(grid_q(pos, "Which shape has no corners?", flat("circle", 0, 0.9, 1),
                      [flat("half", 0, 0.8, 3), flat("quarter", 0, 0.85, 4), flat("tri_eq", 0, 0.85, 2)],
                      "%s is a circle. It has no corners. The half circle has 2 corners."))
    its.append(grid_q(pos, "Which shape has a curved side and 3 corners?", flat("quarter", 180, 0.85, 0),
                      [flat("half", 90, 0.8, 2), flat("tri_eq", 0, 0.85, 3), flat("circle", 0, 0.9, 4)],
                      "%s is a quarter circle. It has a curved side and 3 corners. The triangle has no curved side."))
    its.append(grid_q(pos, "Which shape is NOT a square?", flat("rect", 0, 0.75, 1),
                      [flat("square", 45, 0.85, 3), flat("square", 0, 0.55, 0), flat("square", 15, 0.95, 4)],
                      "%s has 2 long sides and 2 short sides. It is a rectangle. The squares are turned, but all their sides are the same."))
    its.append(rule_q([flat("square", 0, 0.6, 1), flat("rect", 0, 0.55, 3), flat("square", 45, 0.55, 4), flat("rect_long", 90, 0.45, 2)],
                      "4 corners", ["same colour", "3 corners", "same size"],
                      "Some are squares. Some are rectangles. The colours and sizes are different. All of them have 4 corners."))
    its.append(rule_q([flat("circle", 0, 0.5, 2), flat("half", 0, 0.6, 0), flat("quarter", 90, 0.6, 4), flat("half", 180, 0.5, 1)],
                      "a curved side", ["4 corners", "same colour", "no corners"],
                      "A circle, half circles and a quarter circle. Each one has a curved side."))
    n, he, his = P.next()
    row = [flat("tri_eq", 0, 0.6, 0), flat("quarter", 0, 0.6, 1), flat("tri_right", 160, 0.55, 2),
           flat("circle", 0, 0.55, 3), flat("tri_thin", 40, 0.45, 4), flat("half", 0, 0.55, 2)]
    ks = [TRI, QUAR, TRI, CIR, TRI, HALF]
    m = sum(1 for k in ks if k == TRI)
    its.append(mcq(fig(row_svg(row, [""] * 6, "a row of shapes", gap=14)) + "%s draws these shapes. How many triangles are there?" % n,
                   m, [m + 1, m - 1, 6],
                   "Look for 3 straight sides. There are %d triangles. The quarter circle has a curved side, so it is not a triangle." % m))
    assert len(its) == 20, len(its)
    return {"title": "Sides and corners", "items": its}


# ------------------------------------------------------------ set 3: half circles and quarter circles
def apart(pieces, s=1.0):
    return comp_cv(pieces, s)


def pizza_cv():
    cv = cut_circle("quarters", 42, fill="#f3c26b", line="#b5651d")
    for x, y in [(-20, -16), (18, -22), (22, 16), (-16, 20), (-28, 6), (8, 30), (-6, -32), (30, -4)]:
        if abs(x) > 6 and abs(y) > 6:
            cv.circle((x, y), 4.5, fill="#c0392b", sw=0)
    return cv


def set_halves(rnd, pos, P):
    its = []
    its.append(mcq(fig(cut_circle("half", 42, 1).svg("a circle cut into 2 equal parts")) +
                   "This circle is cut into 2 equal parts. What is each part?", HALF, [QUAR, CIR, TRI],
                   "2 equal parts of a circle are 2 half circles."))
    its.append(mcq(fig(cut_circle("quarters", 42, 2).svg("a circle cut into 4 equal parts")) +
                   "This circle is cut into 4 equal parts. What is each part?", QUAR, [HALF, TRI, CIR],
                   "4 equal parts of a circle are 4 quarter circles. A quarter circle has a curved side, so it is not a triangle."))
    two_h = [Hc(0, -6, 40, 180, 1), Hc(0, 6, 40, 0, 3)]
    its.append(mcq(fig(apart(two_h).svg("two half circles")) + "How many half circles make a circle?", 2, [1, 3, 4],
                   "1 half circle + 1 half circle = 1 circle. 2 half circles make a circle."))
    four_q = [Qc(-5, -5, 40, 180, 1), Qc(5, -5, 40, 270, 2), Qc(5, 5, 40, 0, 3), Qc(-5, 5, 40, 90, 4)]
    its.append(mcq(fig(apart(four_q).svg("four quarter circles")) + "How many quarter circles make a circle?", 4, [2, 3, 5],
                   "4 quarter circles fit together to make 1 circle."))
    two_q = [Qc(-5, 0, 46, 180, 2), Qc(5, 0, 46, 270, 4)]
    its.append(mcq(fig(apart(two_q).svg("two quarter circles")) + "How many quarter circles make a half circle?", 2, [4, 1, 3],
                   "A half circle is 2 quarters of a circle. 2 quarter circles make a half circle."))
    j2q = [Qc(0, 0, 50, 180, 2), Qc(0, 0, 50, 270, 4)]
    its.append(mcq(fig(comp_cv(j2q).svg("two quarter circles joined")) + "2 quarter circles are put together. What shape do they make?",
                   "a half circle", ["a circle", "a quarter circle", "a triangle"],
                   "The 2 straight sides meet. The new shape has 1 straight side and 1 curved side. It is a half circle."))
    j2h = [Hc(0, 0, 40, 180, 1), Hc(0, 0, 40, 0, 0)]
    its.append(mcq(fig(comp_cv(j2h).svg("two half circles joined")) + "2 half circles are put together. What shape do they make?",
                   "a circle", ["a half circle", "a quarter circle", "an oval"],
                   "The 2 straight sides meet in the middle. The new shape is round all the way. It is a circle."))
    n, he, his = P.next()
    its.append(mcq(fig(flat("half", 0, 0.8, 3).svg("a half circle")) +
                   "%s has 1 half circle. How many more half circles does %s need to make a circle?" % (n, he), 1, [2, 3, 4],
                   "A circle is 2 half circles. %s has 1. 2 − 1 = 1 more." % n))
    lab = "four shapes labelled A to D"
    its.append(grid_q(pos, "Which shape is a half circle?", flat("half", 90, 0.8, 2),
                      [flat("quarter", 0, 0.85, 1), flat("quarter", 180, 0.85, 4), flat("circle", 0, 0.85, 3)],
                      "%s has 1 straight side. It is a half circle. Each quarter circle has 2 straight sides.", lab))
    its.append(grid_q(pos, "Which shape is a half circle?", flat("half", 180, 0.75, 4),
                      [flat("quarter", 90, 0.9, 0), flat("tri_eq", 180, 0.85, 2), flat("oval", 0, 0.8, 1)],
                      "%s is half of a circle, upside down. It has 1 straight side and 1 curved side.", lab))
    its.append(grid_q(pos, "Which shape is a quarter circle?", flat("quarter", 270, 0.9, 3),
                      [flat("half", 270, 0.8, 1), flat("half", 0, 0.8, 2), flat("tri_right", 90, 0.8, 0)],
                      "%s has 2 straight sides and 1 curved side. It is a quarter circle. The half circles have only 1 straight side.", lab))
    its.append(grid_q(pos, "Which shape is a quarter circle?", flat("quarter", 0, 0.75, 0),
                      [flat("tri_right", 0, 0.8, 3), flat("half", 90, 0.75, 4), flat("circle", 0, 0.75, 1)],
                      "%s has a square corner and a curved side. It is a quarter circle. The triangle has 3 straight sides.", lab))
    lab2 = "four circles labelled A to D"
    its.append(grid_q(pos, "Which circle is cut into 2 half circles?", cut_circle("half", 38, 1),
                      [cut_circle("chord_v", 38, 1), cut_circle("chord_h", 38, 1), cut_circle("quarters", 38, 1)],
                      "In %s the line goes through the middle. The 2 parts are equal. The other cuts make parts that are not equal, or 4 parts.", lab2))
    its.append(grid_q(pos, "Which circle is cut into 4 quarter circles?", cut_circle("quarters", 38, 3),
                      [cut_circle("cross_off", 38, 3), cut_circle("half_h", 38, 3), cut_circle("thirds", 38, 3)],
                      "In %s both lines go through the middle. The 4 parts are equal. They are quarter circles.", lab2))
    n, he, his = P.next()
    its.append(mcq(fig(pizza_cv().svg("a round pizza cut into 4 equal slices")) +
                   "%s cuts a round pizza into 4 equal slices. What shape is each slice?" % n,
                   QUAR, [HALF, TRI, CIR],
                   "A circle cut into 4 equal parts gives 4 quarter circles. Each slice is a quarter circle."))
    n, he, his = P.next()
    its.append(mcq(fig(cut_circle("half_h", 42, fill="#e8b86b", line="#8a5a1a").svg("a round pancake cut into 2 equal parts")) +
                   "%s cuts a round pancake into 2 equal parts. What shape is each part?" % n,
                   HALF, [QUAR, CIR, "oval"],
                   "A circle cut into 2 equal parts gives 2 half circles."))
    n, he, his = P.next()
    cv = flat("half", 0, 0.9, 1)
    cv.line((0, 0), (0, -45), dashed=True, sw=2, col=INK)
    its.append(mcq(fig(cv.svg("a paper half circle with a fold line")) +
                   "%s folds a paper circle in half. Then %s folds it along the dashed line. What shape is it now?" % (n, he),
                   QUAR, [HALF, TRI, CIR],
                   "Half of a half circle is a quarter circle."))
    n, he, his = P.next()
    its.append(mcq(fig(cut_circle("chord_v", 42, 4).svg("a circle cut into 2 parts that are not equal")) +
                   "%s cuts a circle like this. Are the 2 parts half circles?" % n,
                   "No, the parts are not equal", ["Yes, there are 2 parts", "Yes, they are round", "No, there are 3 parts"],
                   "Half circles are 2 equal parts. The line does not go through the middle. One part is bigger."))
    row = [flat("half", 0, 0.5, 0), flat("quarter", 0, 0.55, 2), flat("half", 180, 0.45, 3), flat("circle", 0, 0.5, 1),
           flat("quarter", 180, 0.5, 4), flat("half", 90, 0.5, 2), flat("quarter", 90, 0.45, 0)]
    ks = [HALF, QUAR, HALF, CIR, QUAR, HALF, QUAR]
    h, q = ks.count(HALF), ks.count(QUAR)
    its.append(mcq(fig(row_svg(row, [""] * 7, "a row of shapes", gap=12)) + "How many half circles can you see?", h, [h + q, q + 1, h - 1],
                   "A half circle has 1 straight side. There are %d half circles. The others are quarter circles and a circle." % h))
    its.append(mcq(fig(row_svg(row[::-1], [""] * 7, "a row of shapes", gap=12)) + "How many quarter circles can you see?", q, [h + q, q + 1, q - 1],
                   "A quarter circle has 2 straight sides and a square corner. There are %d quarter circles." % q))
    assert h == q == 3
    assert len(its) == 20, len(its)
    return {"title": "Half circles and quarter circles", "items": its}


# ------------------------------------------------------------ set 4: shapes that make up a figure
NAME_A = {TRI: "a triangle", SQ: "a square", REC: "a rectangle", CIR: "a circle", HALF: "a half circle", QUAR: "a quarter circle"}
PLURAL = {TRI: "triangles", SQ: "squares", REC: "rectangles", CIR: "circles", HALF: "half circles", QUAR: "quarter circles"}


def count_q(pieces, label, ask, kind, wrong, e, s=1.0):
    n = count(pieces, kind)
    if kind == REC:
        assert count(pieces, SQ) == 0               # a square is also a rectangle: never ask then
    return mcq(fig(comp_cv(pieces, s).svg(label)) + ask, n, wrong(n, len(pieces)) + [n + 2, n - 2], e % {"n": n, "all": len(pieces)})


def two_shapes_q(pieces, label, ask, right, wrong, e):
    ks = kinds(pieces)
    assert len(ks) == 2 and right == "%s and %s" % (NAME_A[ks[0]], NAME_A[ks[1]]) or \
        right == "%s and %s" % (NAME_A[ks[1]], NAME_A[ks[0]]), (ks, right)
    return mcq(fig(comp_cv(pieces).svg(label)) + ask, right, wrong, e)


def set_figures(rnd, pos, P):
    its = []
    n, he, his = P.next()
    its.append(two_shapes_q(F_house(), "a house made of shapes", "%s makes a house. Which 2 shapes does %s use?" % (n, he),
                            "a square and a triangle", ["a square and a circle", "2 triangles", "a circle and a triangle"],
                            "The wall has 4 sides the same length. It is a square. The roof has 3 sides. It is a triangle."))
    n, he, his = P.next()
    its.append(count_q(F_rocket(), "a rocket made of shapes", "%s makes a rocket with shapes. How many triangles are there?" % n, TRI,
                       lambda k, a: [k - 1, k + 1, a],
                       "The tip is 1 triangle. There are 2 more at the bottom. 1 + 2 = %(n)d triangles."))
    its.append(count_q(F_sun(), "a sun made of shapes", "How many triangles are in this sun?", TRI,
                       lambda k, a: [k - 1, k + 1, a],
                       "Count the points around the circle. Each one is a triangle. There are %(n)d triangles."))
    n, he, his = P.next()
    its.append(count_q(F_train(), "a train made of shapes", "%s makes a train. How many circles does %s use?" % (n, he), CIR,
                       lambda k, a: [k - 1, k + 2, a],
                       "The wheels are circles. Count them: %(n)d circles."))
    n, he, his = P.next()
    rob = F_robot()
    its.append(mcq(fig(comp_cv(rob, 0.9).svg("a robot made of shapes")) +
                  "%s makes a robot with shapes. How many shapes are there in all?" % n, len(rob), [len(rob) - 1, len(rob) + 1, len(rob) - 2],
                  "Head 1, body 1, arms 2, legs 2. 1 + 1 + 2 + 2 = %d shapes." % len(rob)))
    assert len(rob) == 6
    boat = F_boat()
    assert CIR not in kinds(boat) and {HALF, REC, TRI} == set(kinds(boat))
    its.append(mcq(fig(comp_cv(boat).svg("a boat made of shapes")) + "Which shape is NOT used in this boat?", "a circle",
                   ["a half circle", "a triangle", "a rectangle"],
                   "The boat is a half circle, the pole is a thin rectangle and the sail is a triangle. There is no circle."))
    n, he, his = P.next()
    its.append(two_shapes_q(F_icecream(), "an ice cream made of shapes", "%s draws an ice cream. Which 2 shapes does %s use?" % (n, he),
                            "a triangle and a half circle", ["a triangle and a circle", "a triangle and a quarter circle", "a square and a half circle"],
                            "The cone has 3 straight sides. It is a triangle. The top has 1 straight side and 1 curved side. It is a half circle."))
    its.append(count_q(F_kite(), "a kite made of 4 triangles", "How many small triangles make this kite?", TRI,
                       lambda k, a: [2, 3, 5],
                       "The 2 lines cross in the middle. They make %(n)d small triangles."))
    its.append(count_q(F_bigtri(), "a big triangle made of small triangles", "How many small triangles make this big triangle?", TRI,
                       lambda k, a: [3, 5, 2],
                       "There are 3 small triangles pointing up. Do not miss the one in the middle. It points down. 3 + 1 = %(n)d."))
    n, he, his = P.next()
    its.append(count_q(F_rectcut(), "a rectangle cut along a line", "%s cuts a rectangle along the line. How many triangles does %s get?" % (n, he), TRI,
                       lambda k, a: [1, 3, 4],
                       "The line goes from corner to corner. It makes %(n)d triangles."))
    n, he, his = P.next()
    its.append(count_q(F_flower(), "a flower made of shapes", "%s makes a flower. How many half circles does %s use?" % (n, he), HALF,
                       lambda k, a: [k - 1, k + 1, a],
                       "There is 1 half circle on each side of the square. There are %(n)d half circles."))
    its.append(count_q(F_caterpillar(), "a caterpillar made of shapes", "How many circles make this caterpillar?", CIR,
                       lambda k, a: [k - 1, k + 1, a],
                       "Count the round parts: 1, 2, 3, 4, 5. There are %(n)d circles."))
    tt = F_two_tri_square()
    assert count(tt, TRI) == 2 and union_kind(tt) == SQ
    its.append(mcq(fig(comp_cv(tt).svg("two triangles put together")) + "What shape do these 2 triangles make?", "a square",
                   ["a triangle", "a circle", "a half circle"],
                   "Together they have 4 sides the same length and 4 square corners. They make a square."))
    t2 = F_two_squares()
    assert count(t2, SQ) == 2 and union_kind(t2) == REC
    n, he, his = P.next()
    its.append(mcq(fig(comp_cv(t2).svg("two squares put together")) + "%s puts 2 squares side by side. What shape does %s make?" % (n, he),
                   "a rectangle", ["a square", "a triangle", "a half circle"],
                   "The new shape has 2 long sides and 2 short sides. It is a rectangle, not a square."))
    t9 = F_nine_squares()
    assert count(t9, SQ) == 9 and union_kind(t9) == SQ
    its.append(mcq(fig(comp_cv(t9).svg("a big square made of small squares")) + "How many small squares make this big square?", 9,
                   [8, 6, 12],
                   "There are 3 rows. Each row has 3 squares. 3 + 3 + 3 = 9. Do not miss the one in the middle."))
    n, he, his = P.next()
    its.append(two_shapes_q(F_tree(), "a tree made of shapes", "%s draws a tree. Which 2 shapes does %s use?" % (n, he),
                            "a triangle and a rectangle", ["a triangle and a square", "2 triangles", "a circle and a rectangle"],
                            "The top has 3 straight sides. It is a triangle. The trunk has 2 long sides and 2 short sides. It is a rectangle."))
    its.append(two_shapes_q(F_umbrella(), "an umbrella made of shapes", "Which 2 shapes make this umbrella?",
                            "a half circle and a rectangle", ["a circle and a rectangle", "a quarter circle and a rectangle", "a half circle and a triangle"],
                            "The top has 1 straight side and 1 curved side. It is a half circle. The handle is a thin rectangle."))
    lab = "four figures labelled A to D"
    figs3 = {"rocket": F_rocket(), "house": F_house(), "kite": F_kite(), "cut": F_rectcut(), "ice": F_icecream(),
             "tree": F_tree(), "umb": F_umbrella(), "sun": F_sun(), "boat": F_boat(), "flower": F_flower()}
    assert [count(figs3[k], TRI) for k in ("rocket", "house", "kite", "cut")] == [3, 1, 4, 2]
    its.append(grid_q(pos, "Which figure uses 3 triangles?", comp_cv(figs3["rocket"], 0.8),
                      [comp_cv(figs3["house"], 0.8), comp_cv(figs3["kite"], 0.9), comp_cv(figs3["cut"], 0.75)],
                      "%s is the rocket. It has 1 triangle at the top and 2 at the bottom. That is 3 triangles.", lab))
    assert set(kinds(figs3["ice"])) == {TRI, HALF}
    assert all(set(kinds(figs3[k])) != {TRI, HALF} for k in ("house", "tree", "umb"))
    its.append(grid_q(pos, "Which figure is made of a triangle and a half circle?", comp_cv(figs3["ice"], 0.85),
                      [comp_cv(figs3["house"], 0.85), comp_cv(figs3["tree"], 0.8), comp_cv(figs3["umb"], 0.75)],
                      "%s is the ice cream. The cone is a triangle and the top is a half circle.", lab))
    assert CIR in kinds(figs3["sun"]) and all(CIR not in kinds(figs3[k]) for k in ("boat", "ice", "flower"))
    its.append(grid_q(pos, "Which figure uses a circle?", comp_cv(figs3["sun"], 0.8),
                      [comp_cv(figs3["boat"], 0.8), comp_cv(figs3["ice"], 0.85), comp_cv(figs3["flower"], 0.85)],
                      "%s is the sun. Its middle is a circle. The boat, the ice cream and the flower use half circles, not circles.", lab))
    assert len(its) == 20, len(its)
    return {"title": "Shapes that make a figure", "items": its}


# ------------------------------------------------------------ set 5: copy and complete figures on a dot grid
GC, GR = 6, 5                     # dots across and down in each small grid
COPY = [   # name, figure, wrong copies (each a real copying slip)
    ("L", [(0, 0), (1, 0), (1, 2), (3, 2), (3, 3), (0, 3)],
     [[(0, 0), (1, 0), (1, 2), (4, 2), (4, 3), (0, 3)], [(0, 1), (1, 1), (1, 2), (3, 2), (3, 3), (0, 3)],
      [(0, 0), (2, 0), (2, 2), (3, 2), (3, 3), (0, 3)]],
     "In %s every side is as long as in the figure. In the others one side is too long or too short."),
    ("rect", [(0, 0), (3, 0), (3, 2), (0, 2)],
     [[(0, 0), (4, 0), (4, 2), (0, 2)], [(0, 0), (3, 0), (3, 3), (0, 3)], [(0, 0), (2, 0), (2, 1), (0, 1)]],
     "The figure is 3 spaces long and 2 spaces tall. Only %s is the same. Count the spaces, not the dots."),
    ("tri", [(0, 0), (0, 3), (2, 3)],
     [[(0, 0), (0, 3), (3, 3)], [(0, 1), (0, 3), (2, 3)], [(0, 0), (0, 2), (2, 3)]],
     "The figure goes 3 spaces down and 2 spaces across. Only %s matches."),
    ("T", [(0, 0), (3, 0), (3, 1), (2, 1), (2, 3), (1, 3), (1, 1), (0, 1)],
     [[(0, 0), (3, 0), (3, 1), (2, 1), (2, 4), (1, 4), (1, 1), (0, 1)],
      [(0, 0), (5, 0), (5, 1), (3, 1), (3, 3), (2, 3), (2, 1), (0, 1)],
      [(0, 0), (3, 0), (3, 1), (1, 1), (1, 3), (0, 3)]],
     "%s has the same top and the same middle part as the figure. Check each side, one at a time."),
    ("house", [(0, 1), (1, 0), (2, 1), (2, 3), (0, 3)],
     [[(0, 1), (1, 0), (2, 1), (2, 4), (0, 4)], [(0, 2), (2, 0), (4, 2), (4, 4), (0, 4)],
      [(0, 1), (2, 1), (2, 3), (0, 3)]],
     "%s has the same roof and the same walls. One wrong copy has no roof, and others are too tall or too big."),
    ("steps", [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2), (3, 3), (0, 3)],
     [[(0, 0), (1, 0), (1, 2), (3, 2), (3, 3), (0, 3)],
      [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2), (3, 3), (4, 3), (4, 4), (0, 4)],
      [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (4, 2), (4, 3), (0, 3)]],
     "The figure has 3 steps, each 1 space. Only %s is the same."),
    ("peak", [(0, 3), (2, 0), (4, 3)],
     [[(0, 3), (2, 1), (4, 3)], [(0, 3), (3, 0), (4, 3)], [(0, 3), (2, 0), (3, 3)]],
     "The top of the figure is right above the middle of the bottom. The bottom is 4 spaces long. Only %s matches."),
]


def check_copy(orig, wrongs):
    base = canon(orig)
    for w in wrongs:
        check_poly(w)
        assert base not in symmetries(w), ("a wrong copy is the same figure", orig, w)
    assert len({canon(w) for w in wrongs}) == 3


def copy_q(pos, rnd, P, name, orig, wrongs, why):
    check_poly(orig)
    check_copy(orig, wrongs)
    p = pos.next()
    cells = [fit_shift(w, GC, GR, rnd) for w in wrongs]
    right = fit_shift(orig, GC, GR, rnd)
    assert canon(right) == canon(orig)
    cells.insert(p, right)
    cvs = [dot_cv(GC, GR, polys=[c], c=1) for c in cells]
    ocv = dot_cv(GC, GR, polys=[fit_shift(orig, GC, GR, rnd)], c=3)
    n, he, his = P.next()
    L = "ABCD"[p]
    q = fig(copy_svg(ocv, cvs, "a figure in a box and four copies labelled A to D")) + \
        "%s copies the figure in the box. Which copy is correct?" % n
    return mcq_fixed(q, list("ABCD"), L, why % L)


S_FIN = 28


def finish_q(pos, rnd, P, drawn, cands_wrong, want):
    """2 sides drawn (P0-P1-P2). Which labelled dot finishes the square or rectangle?"""
    P0, P1, P2 = drawn
    right = (P0[0] + P2[0] - P1[0], P0[1] + P2[1] - P1[1])
    assert classify([P0, P1, P2, right]) == want
    for w in cands_wrong:
        assert w != right and w not in drawn
        try:
            k = classify([P0, P1, P2, w])
        except AssertionError:
            k = "other"
        assert k != want, (drawn, w)
    p = pos.next()
    cands = list(cands_wrong)
    cands.insert(p, right)
    cols, rows = 8, 6
    cv = Canvas()
    for i in range(cols):
        for j in range(rows):
            cv.circle((i * S_FIN, j * S_FIN), 2.4, fill=DOT, sw=0)
    Pp = lambda q: (q[0] * S_FIN, q[1] * S_FIN)
    cv.pline([Pp(P0), Pp(P1), Pp(P2)], sw=3.2, col=COLS[1][1])
    segs = [(Pp(P0), Pp(P1)), (Pp(P1), Pp(P2))]
    used = []
    for k, c in enumerate(cands):
        assert 0 <= c[0] < cols and 0 <= c[1] < rows
        x, y = Pp(c)
        cv.circle((x, y), 5.5, fill=COLS[3][1], sw=0)
        # put the letter in a free spot next to its dot: away from the lines, the other big dots and letters
        best = None
        for dx, dy in [(11, -8), (-11, -8), (11, 16), (-11, 16)]:
            lx, ly = x + dx, y + dy
            cx, cy = lx, ly - 5
            d = min([seg_dist((cx, cy), a, b) for a, b in segs] +
                    [math.hypot(cx - Pp(o)[0], cy - Pp(o)[1]) for o in cands if o != c] +
                    [math.hypot(cx - u[0], cy - u[1]) for u in used])
            if best is None or d > best[0]:
                best = (d, lx, ly)
        assert best[0] >= 9, ("letter too close", drawn, c, best)
        used.append((best[1], best[2] - 5))
        cv.text(best[1], best[2], "ABCD"[k], 15, COLS[3][1])
    L = "ABCD"[p]
    n, he, his = P.next()
    q = fig(cv.svg("a dot grid with 2 sides of a %s and four dots labelled A to D" % want)) + \
        "%s draws 2 sides of a %s. Which dot finishes the %s?" % (n, want, want)
    return mcq_fixed(q, list("ABCD"), L,
                     "Join both ends to dot %s. All 4 corners are square corners%s." % (L, " and all 4 sides are the same length" if want == SQ else ""))


def seg_dist(p, a, b):
    ax, ay = b[0] - a[0], b[1] - a[1]
    t = max(0, min(1, ((p[0] - a[0]) * ax + (p[1] - a[1]) * ay) / (ax * ax + ay * ay)))
    return math.hypot(p[0] - a[0] - t * ax, p[1] - a[1] - t * ay)


def set_dotgrid(rnd, pos, P):
    its = []
    for name, orig, wrongs, why in COPY:
        its.append(copy_q(pos, rnd, P, name, orig, wrongs, why))
    for drawn, wrong, want in [
            ([(2, 1), (4, 1), (4, 3)], [(0, 3), (2, 5), (0, 5)], SQ),
            ([(1, 1), (6, 1), (6, 3)], [(3, 3), (1, 5), (3, 5)], REC),
            ([(3, 0), (5, 2), (3, 4)], [(1, 0), (1, 4), (2, 5)], SQ),
            ([(6, 0), (6, 4), (3, 4)], [(1, 0), (3, 2), (1, 2)], REC),
            ([(1, 5), (1, 2), (4, 2)], [(6, 5), (4, 3), (6, 3)], SQ),
    ]:
        its.append(finish_q(pos, rnd, P, drawn, wrong, want))
    lab = "four shapes on dot grids labelled A to D"
    which = [
        ("square", [(1, 0), (4, 0), (4, 3), (1, 3)], [[(0, 0), (4, 0), (4, 3), (0, 3)], [(0, 1), (3, 1), (3, 3), (0, 3)], [(0, 0), (0, 3), (3, 3)]],
         "%s has 4 sides that are each 3 spaces long. It is a square. The shape 4 spaces long and 3 spaces tall is a rectangle."),
        ("square", [(2, 0), (4, 2), (2, 4), (0, 2)], [[(2, 0), (3, 2), (2, 4), (1, 2)], [(0, 1), (4, 1), (4, 3), (0, 3)], [(0, 4), (2, 0), (4, 4)]],
         "%s stands on a corner. Its 4 sides are the same length and its corners are square corners. It is a square. The thin one is not."),
        ("rectangle", [(0, 1), (5, 1), (5, 3), (0, 3)], [[(0, 0), (1, 0), (1, 2), (3, 2), (3, 3), (0, 3)], [(0, 4), (2, 0), (4, 4)], [(0, 1), (1, 0), (2, 1), (2, 3), (0, 3)]],
         "%s has 4 straight sides and 4 square corners. 2 sides are long and 2 are short. It is a rectangle."),
        ("triangle", [(1, 0), (4, 3), (0, 4)], [[(0, 0), (2, 0), (2, 2), (0, 2)], [(0, 1), (1, 0), (2, 1), (2, 3), (0, 3)], [(0, 0), (3, 0), (3, 4), (0, 4)]],
         "%s has 3 straight sides and 3 corners. It is a triangle, even when it is turned."),
    ]
    for want, right, others, why in which:
        assert classify(right) == want
        for o in others:
            assert classify(o) != want
        n, he, his = P.next()
        its.append(grid_q(pos, "%s draws 4 shapes on dot paper. Which one is a %s?" % (n, want),
                          dot_cv(GC, GR, polys=[right], c=2), [dot_cv(GC, GR, polys=[o], c=2) for o in others], why, lab))
    # name the shape on the dot grid
    sq_turn = [(1, 1), (3, 0), (4, 2), (2, 3)]
    assert classify(sq_turn) == SQ
    n, he, his = P.next()
    its.append(mcq(fig(dot_cv(GC, GR, polys=[sq_turn], c=4).svg("a shape on a dot grid")) +
                   "%s draws this shape on dot paper. What shape is it?" % n, SQ, ["diamond", TRI, "half circle"],
                   "Each side goes 2 across and 1 up or down, so all 4 sides are the same length. The corners are square corners. It is a square."))
    tri_r = [(0, 0), (0, 3), (4, 3)]
    assert classify(tri_r) == TRI
    n, he, his = P.next()
    its.append(mcq(fig(dot_cv(GC, GR, polys=[tri_r], c=0).svg("a shape on a dot grid")) +
                   "%s draws this shape on dot paper. What shape is it?" % n, TRI, [QUAR, SQ, REC],
                   "It has 3 straight sides and 3 corners. It is a triangle. A quarter circle has a curved side."))
    rect_t = [(1, 0), (3, 0), (3, 4), (1, 4)]
    assert classify(rect_t) == REC
    n, he, his = P.next()
    its.append(mcq(fig(dot_cv(GC, GR, polys=[rect_t], c=2).svg("a shape on a dot grid")) +
                   "%s draws this shape on dot paper. What shape is it?" % n, REC, [SQ, TRI, HALF],
                   "It is 2 spaces across and 4 spaces down. 2 sides are long and 2 are short. It is a rectangle."))
    house = [(1, 2), (3, 2), (3, 4), (1, 4)]
    roof = [(1, 2), (2, 0), (3, 2)]
    assert classify(house) == SQ and classify(roof) == TRI
    n, he, his = P.next()
    its.append(mcq(fig(dot_cv(GC, GR, polys=[house, roof], c=1).svg("a figure on a dot grid")) +
                   "%s draws a house on dot paper. Which 2 shapes make it?" % n, "a square and a triangle",
                   ["2 triangles", "a square and a half circle", "a circle and a triangle"],
                   "The bottom is 2 spaces each way. It is a square. The roof has 3 straight sides. It is a triangle."))
    assert len(its) == 20, len(its)
    return {"title": "Copy and complete figures on a dot grid", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    six = row_svg([flat("rect", 0, 0.6, 2), flat("square", 0, 0.7, 3), flat("tri_eq", 0, 0.75, 0), flat("circle", 0, 0.75, 1),
                   flat("half", 0, 0.7, 4), flat("quarter", 0, 0.75, 2)],
                  ["rectangle", "square", "triangle", "circle", "half circle", "quarter circle"],
                  "a rectangle, a square, a triangle, a circle, a half circle and a quarter circle", gap=16, fs=14)
    turned = row_svg([flat("square", 0, 0.75, 2), flat("square", 45, 0.7, 4), flat("half", 0, 0.7, 0), flat("half", 180, 0.6, 1)],
                     ["square", "still a square", "half circle", "still a half circle"],
                     "a square and the same square turned; a half circle and an upside-down half circle", gap=24, fs=15)
    cuts = row_svg([cut_circle("half", 34, 1), flat("half", 0, 0.68, 1), cut_circle("quarters", 34, 3), flat("quarter", 0, 0.62, 3)],
                   ["2 equal parts", "half circle", "4 equal parts", "quarter circle"],
                   "a circle cut into 2 equal parts gives half circles; cut into 4 equal parts gives quarter circles", gap=22, fs=15)
    figs = row_svg([comp_cv(F_house(), 0.8), comp_cv(F_rocket(), 0.75), comp_cv(F_icecream(), 0.8)],
                   ["square + triangle", "rectangle + 3 triangles", "triangle + half circle"],
                   "a house, a rocket and an ice cream made of shapes", gap=24, fs=15)
    orig = [(0, 0), (1, 0), (1, 2), (3, 2), (3, 3), (0, 3)]
    copy = row_svg([dot_cv(GC, GR, polys=[orig], c=3), dot_cv(GC, GR, polys=[[(x + 1, y + 1) for x, y in orig]], c=1)],
                   ["figure", "copy"], "a figure on a dot grid and its copy", gap=40, fs=15)
    return (
        "<h2>Six shapes to know</h2>"
        "<p>Look at the <b>sides</b> and the <b>corners</b>. A side can be <b>straight</b> or <b>curved</b>.</p>"
        "<figure class='sn-fig'>" + six + "</figure>" +
        table(["Shape", "Straight sides", "Curved sides", "Corners"], [
            ["Rectangle", "4 (2 long, 2 short)", "0", "4"],
            ["Square", "4 (all the same length)", "0", "4"],
            ["Triangle", "3", "0", "3"],
            ["Circle", "0", "1", "0"],
            ["Half circle", "1", "1", "2"],
            ["Quarter circle", "2", "1", "3"]]) +
        "<p>Size, colour and turning do not change the name.</p>"
        "<figure class='sn-fig'>" + turned +
        "<figcaption>A square on its corner is still a square, not a “diamond”.</figcaption></figure>" +
        ex("Example 1", "A shape has 2 straight sides and 1 curved side. What is it?",
           "A half circle has only 1 straight side. 2 straight sides and 1 curved side make a quarter circle.", "a quarter circle") +
        "<h2>Half circles and quarter circles</h2>"
        "<p>Cut a circle into <b>2 equal parts</b>. Each part is a <b>half circle</b>. "
        "Cut it into <b>4 equal parts</b>. Each part is a <b>quarter circle</b>. The cuts must go through the middle.</p>"
        "<figure class='sn-fig'>" + cuts + "</figure>" +
        ex("Example 2", "How many quarter circles make a half circle?",
           "2 quarter circles fit together to make a half circle.", "2") +
        "<h2>Shapes make figures</h2>"
        "<p>We can put shapes together to make a figure. Count each kind of shape. Point to each one as you count.</p>"
        "<figure class='sn-fig'>" + figs + "</figure>" +
        ex("Example 3", "2 squares are put side by side. What shape do they make?",
           "The new shape has 2 long sides and 2 short sides.", "a rectangle") +
        "<h2>Copy a figure on a dot grid</h2>"
        "<p>Start at one corner. Count the <b>spaces</b> between dots along each side. Draw the same number of spaces in your copy.</p>"
        "<figure class='sn-fig'>" + copy +
        "<figcaption>The copy is in a new place. Every side has the same number of spaces.</figcaption></figure>" +
        ex("Example 4", "A side of the figure joins 4 dots in a row. How many spaces long is it?",
           "4 dots in a row have 3 spaces between them.", "3 spaces") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Calling a turned square a “diamond”", "Check the sides. 4 sides the same length and 4 square corners make a square, any way up."],
            ["Mixing up a half circle and a quarter circle", "Count the straight sides. A half circle has 1. A quarter circle has 2."],
            ["Calling a quarter circle a triangle", "A triangle has 3 straight sides. A quarter circle has a curved side."],
            ["Calling any 2 parts of a circle half circles", "Half circles are 2 equal parts. The cut goes through the middle."],
            ["Missing a shape in a figure", "Point to each shape as you count. Look in the middle too."],
            ["Counting dots instead of spaces", "On a dot grid, count the spaces between the dots."],
        ])
    )


FAQ = [
    {"q": "What 2D shapes are taught in Primary 1 maths?",
     "a": "Primary 1 students in Singapore learn the rectangle, square, triangle, circle, half circle and quarter circle. "
          "They name and describe the shapes, use them to make figures, and copy figures on a dot grid."},
    {"q": "What is the difference between a half circle and a quarter circle?",
     "a": "A half circle is 1 of 2 equal parts of a circle and has 1 straight side. "
          "A quarter circle is 1 of 4 equal parts and has 2 straight sides that meet at a square corner."},
    {"q": "Is a square turned on its corner still a square?",
     "a": "Yes. It still has 4 sides of the same length and 4 square corners. Many children call it a “diamond”, "
          "but turning a shape never changes its name."},
    {"q": "How can I help my child copy figures on a dot grid?",
     "a": "Ask your child to start at one corner and count the spaces between the dots along each side. "
          "Then check the copy side by side with the figure, one side at a time."},
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
    """Tag pictures that must print larger (A-D choices, rows, dot grids) so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(61810)
    P = People(rnd)
    sets = [set_name(rnd, Pos(rnd)), set_sides(rnd, Pos(rnd), P), set_halves(rnd, Pos(rnd), P),
            set_figures(rnd, Pos(rnd), P), set_dotgrid(rnd, Pos(rnd), P)]
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
        "country": "sg", "subject": "maths", "grade": "primary-1", "slug": "2d-shapes", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 1 2D Shapes",
        "seo_title": "P1 2D Shapes Worksheets: Free Primary 1 Maths with Answers (MOE Syllabus)",
        "short_title": "2D shapes",
        "domain": "Measurement and Geometry",
        "standard_code": "Primary 1: Geometry",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Identifying, naming, describing and classifying 2D shapes (rectangle, square, triangle, circle, "
                         "half circle, quarter circle); forming figures; copying figures on grids",
        "meta_desc": "Free P1 maths practice: name 2D shapes, count sides and corners, half and quarter circles, "
                     "make figures and copy them on a dot grid. 100 questions with answers.",
        "key_big": "Count the straight sides and the corners to name a shape. Turning a shape never changes its name.",
        "key_sub": "A half circle has 1 straight side. A quarter circle has 2. A square on its corner is still a square.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(four |a row of|a dot grid|a figure in a box)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
