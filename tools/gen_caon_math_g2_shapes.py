# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 2 Math: 2D shapes and symmetry (Ontario Curriculum 2020, Spatial Sense E1.1, E1.2, E1.3)
  python3 tools/gen_caon_math_g2_shapes.py
HTML attributes use single quotes (no backslashes in the JSON). Canadian English, short sentences for 7–8-year-olds.

Grade 2 students sort and identify 2D shapes by comparing the number of sides, side lengths, angles and the
number of lines of symmetry (E1.1), put shapes together and take them apart, and see that the space a shape
covers stays the same when its parts are moved (E1.2), and find congruent lengths, angles and shapes (E1.3).

Pictures (checked in code):
  shapes      drawn from their corner points; sides and vertices counted from the points, side lengths and
              square corners (right angles) measured from the points, every corner is a real turn, no sides cross
  lengths     a shape labelled in cm is drawn to scale and every label is measured from the picture
  symmetry    a dashed line is a line of symmetry only when reflecting every side across it gives the same sides;
              lines of symmetry are counted the same way
  composites  the parts fill the outline exactly (areas add up) and every part is named from its own corners;
              rearranged parts cover the same space (areas checked in code)
  congruent   two shapes are congruent when their side lengths and angles match in order (turned or flipped)
Wrong answers come from real student mistakes: a turned square called a “diamond”, a side counted twice or
missed, a shape named by a part of it, the sides of the parts added, any line that cuts a shape in two called a
line of symmetry, the slanted lines of a square forgotten, a turned shape called “not congruent”, a bigger copy
called congruent, a rearranged shape said to cover more space.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#f6dcb4"
FILL3 = "#a9d3b6"
FILL4 = "#f3d27a"
RED = "#c0392b"
BLUE = "#1f5fa8"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
THIN = "#b8b8b8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]


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

    def poly(self, pts, fill, sw=2.6, col=GREEN):
        self.el.append(("p", pts, fill, sw, col))
        for x, y in pts:
            self.grow(x - sw, y - sw, x + sw, y + sw)

    def line(self, a, b, dashed=False, sw=2.4, col=GREEN, dash="5 4"):
        self.el.append(("l", a, b, dashed, sw, col, dash))
        self.grow(min(a[0], b[0]) - sw, min(a[1], b[1]) - sw, max(a[0], b[0]) + sw, max(a[1], b[1]) + sw)

    def pline(self, pts, sw=1.8, col=INK):
        self.el.append(("pl", pts, sw, col))
        for x, y in pts:
            self.grow(x - sw, y - sw, x + sw, y + sw)

    def text(self, x, y, t, fs=15, col=INK):
        """Text centred on (x, y)."""
        self.el.append(("t", x, y, t, fs, col))
        w = tw(t, fs)
        self.grow(x - w / 2 - 1, y - fs * 0.62, x + w / 2 + 1, y + fs * 0.42)

    def body(self, ox, oy):
        s = []
        for e in self.el:
            if e[0] == "p":
                s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>"
                         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in e[1]), e[2], e[4], e[3]))
            elif e[0] == "l":
                _, a, b, dashed, sw, col, dash = e
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g'%s/>"
                         % (a[0] - ox, a[1] - oy, b[0] - ox, b[1] - oy, col, sw,
                            " stroke-dasharray='%s'" % dash if dashed else " stroke-linecap='round'"))
            elif e[0] == "pl":
                _, pts, sw, col = e
                s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='%g'/>"
                         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in pts), col, sw))
            else:
                _, x, y, t, fs, col = e
                s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                         % (x - ox, y - oy + fs * 0.35, fs, col, t))
        return "".join(s)

    def size(self):
        return self.x1 - self.x0, self.y1 - self.y0

    def svg(self, label, pad=5):
        ox, oy = self.x0 - pad, self.y0 - pad
        W, H = int(math.ceil(self.x1 - ox + pad)), int(math.ceil(self.y1 - oy + pad))
        if W == H:
            W += 1                                    # keep figures out of the larger 'square' print size
        return svg_wrap(W, H, self.body(ox, oy), label)


def row_svg(cvs, caps, label, gap=24, fs=15, col=INK):
    """Pictures side by side (centred up and down) with a caption under each."""
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
    Wt, Ht = int(math.ceil(W + 2 * pad)), int(math.ceil(H + capH + 2 * pad))
    if Wt == Ht:
        Wt += 1
    return svg_wrap(Wt, Ht, body, label)


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


# ------------------------------------------------------------ shape facts (screen coordinates, y down)
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


def most_equal(pts):
    """The largest number of sides that have the same length."""
    L = lengths(simplify(pts))
    return max(sum(1 for y in L if abs(y - x) < 1e-6) for x in L)


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


# symmetry
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
    """True when reflecting every side across the line through c at angle a (degrees) gives the same sides."""
    pts = simplify(pts)
    return edge_set([refl(p, c, a) for p in pts]) == edge_set(pts)


def count_axes(pts):
    """Lines of symmetry: any line of symmetry passes through the centre of the vertices (tested every 0.5 degrees)."""
    c = (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
    return sum(1 for i in range(360) if is_axis(pts, c, i * 0.5))


# congruence
def _sig(pts):
    L, A = lengths(pts), interior_angles(pts)
    return [(L[i], A[i]) for i in range(len(pts))]


def _same_cyc(a, b, tol=1e-6):
    n = len(a)
    if n != len(b):
        return False
    return any(all(abs(a[i][0] - b[(i + k) % n][0]) < tol and abs(a[i][1] - b[(i + k) % n][1]) < tol for i in range(n))
               for k in range(n))


def _variants(pts):
    m = [(-x, y) for x, y in pts]
    return [pts, pts[::-1], m, m[::-1]]


def congruent(p, q):
    p, q = simplify(p), simplify(q)
    return any(_same_cyc(_sig(p), _sig(v)) for v in _variants(q))


def same_shape(p, q):
    """Same shape, any size (similar)."""
    p, q = simplify(p), simplify(q)
    sp, sq = sum(lengths(p)), sum(lengths(q))
    return any(_same_cyc(_sig(scaled(p, 1 / sp)), _sig(scaled(v, 1 / sq))) for v in _variants(q))


def tpts(pts, deg=0, s=1.0, flip=False):
    """Turn (and flip) a shape about its centre, and scale it."""
    if flip:
        pts = [(-x, y) for x, y in pts][::-1]
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    c, si = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return [(((x - cx) * c - (y - cy) * si) * s, ((x - cx) * si + (y - cy) * c) * s) for x, y in pts]


def scaled(pts, k):
    return [(x * k, y * k) for x, y in pts]


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
    "kite": [(0, -45), (30, -10), (0, 50), (-30, -10)],
    "para": [(30, 0), (110, 0), (80, 55), (0, 55)],
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
        "kite": "quadrilateral", "para": "parallelogram", "pent_reg": "pentagon", "pent_house": "pentagon",
        "pent_odd": "pentagon", "hex_reg": "hexagon", "hex_L": "hexagon", "hex_arrow": "hexagon", "hept_arrow": "heptagon",
        "oct_reg": "octagon", "oct_cut": "octagon"}
AXES = {"tri_eq": 3, "tri_iso": 1, "tri_right": 0, "tri_thin": 0, "square": 4, "rect": 2, "rect_tall": 2, "rhombus": 2,
        "trap": 1, "rtrap": 0, "kite": 1, "para": 0, "pent_reg": 5, "pent_house": 1, "pent_odd": 0, "hex_reg": 6,
        "hex_L": 0, "hex_arrow": 1, "hept_arrow": 1, "oct_reg": 8, "oct_cut": 2}
CORNERS = {"tri_eq": 0, "tri_iso": 0, "tri_right": 1, "tri_thin": 0, "square": 4, "rect": 4, "rect_tall": 4, "rhombus": 0,
           "trap": 0, "rtrap": 2, "kite": 0, "para": 0}
EQUAL = {"tri_eq": 3, "tri_iso": 2, "tri_right": 1, "tri_thin": 1, "square": 4, "rect": 2, "rhombus": 4, "trap": 2,
         "rtrap": 1, "para": 2, "pent_reg": 5, "hex_reg": 6, "oct_reg": 8}
for _k, _p in SHAPES.items():
    check_poly(_p)
    assert classify(_p) == NAME[_k], (_k, classify(_p))
    assert count_axes(_p) == AXES[_k], (_k, count_axes(_p))
for _k, _n in CORNERS.items():
    assert square_corners(SHAPES[_k]) == _n, (_k, square_corners(SHAPES[_k]))
for _k, _n in EQUAL.items():
    assert most_equal(SHAPES[_k]) == _n, (_k, most_equal(SHAPES[_k]))


def n_sides(key):
    return len(simplify(SHAPES[key]))


def shape(key, deg=0, s=1.0, fill=FILL, flip=False):
    pts = tpts(SHAPES[key], deg, s, flip)
    check_poly(pts)
    cv = Canvas()
    cv.poly(pts, fill, 3)
    return cv


def poly_cv(pts, fill=FILL):
    check_poly(pts)
    cv = Canvas()
    cv.poly(pts, fill, 3)
    return cv


def labelled(pts, labels, k, fs=15, dist=8):
    """Shape drawn k px per cm, with the length (in cm) beside each side that has a label. Labels are measured."""
    n = len(pts)
    cv = Canvas()
    cv.poly(pts, FILL, 3)
    cx, cy = sum(p[0] for p in pts) / n, sum(p[1] for p in pts) / n
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        if not labels[i]:
            continue
        cm = math.hypot(b[0] - a[0], b[1] - a[1]) / k
        assert abs(cm - labels[i]) < 1e-6, (labels[i], cm)
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        nx, ny = -(b[1] - a[1]), b[0] - a[0]
        L = math.hypot(nx, ny)
        nx, ny = nx / L, ny / L
        if nx * (mx - cx) + ny * (my - cy) < 0:
            nx, ny = -nx, -ny
        t = "%d cm" % labels[i]
        off = dist + abs(nx) * tw(t, fs) / 2 + abs(ny) * fs * 0.55     # the whole text box clears the side
        cv.text(mx + nx * off, my + ny * off, t, fs)
    return cv


def corner_mark(cv, pts, i, s=10):
    """Small square in the corner at pts[i] (for square corners)."""
    n = len(pts)
    b, a, c = pts[i], pts[i - 1], pts[(i + 1) % n]
    u = ((a[0] - b[0]), (a[1] - b[1]))
    v = ((c[0] - b[0]), (c[1] - b[1]))
    lu, lv = math.hypot(*u), math.hypot(*v)
    u, v = (u[0] / lu * s, u[1] / lu * s), (v[0] / lv * s, v[1] / lv * s)
    cv.pline([(b[0] + u[0], b[1] + u[1]), (b[0] + u[0] + v[0], b[1] + u[1] + v[1]), (b[0] + v[0], b[1] + v[1])], sw=1.8, col=INK)


def tick(cv, a, b, n=1, s=7):
    """n short marks across the middle of side a-b: sides with the same marks are the same length."""
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy)
    dx, dy = dx / L, dy / L
    for j in range(n):
        o = (j - (n - 1) / 2) * 5
        px, py = mx + dx * o, my + dy * o
        cv.line((px - dy * s, py + dx * s), (px + dy * s, py - dx * s), sw=2, col=INK)


# ------------------------------------------------------------ symmetry pictures
def centre(pts):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)


def axis_cv(pts, c, a, k=1.0):
    """The shape with a dashed red line through c at angle a, long enough to cross the whole shape."""
    P = scaled(pts, k)
    c = (c[0] * k, c[1] * k)
    d = (math.cos(math.radians(a)), math.sin(math.radians(a)))
    ts = [(x - c[0]) * d[0] + (y - c[1]) * d[1] for x, y in P]
    t0, t1 = min(ts) - 12, max(ts) + 12
    cv = Canvas()
    cv.poly(P, FILL, 3)
    cv.line((c[0] + d[0] * t0, c[1] + d[1] * t0), (c[0] + d[0] * t1, c[1] + d[1] * t1), dashed=True, sw=2.6, col=RED, dash="8 5")
    return cv


S = SHAPES
AX = {
    "house_v": (S["pent_house"], centre(S["pent_house"]), 90),
    "house_h": (S["pent_house"], (40, 55), 0),
    "sq_diag": (S["square"], centre(S["square"]), 45),
    "sq_v": (S["square"], centre(S["square"]), 90),
    "rect_diag": (S["rect"], centre(S["rect"]), math.degrees(math.atan2(50, 100))),
    "rect_h": (S["rect"], centre(S["rect"]), 0),
    "rect_off": (S["rect"], (35, 25), 90),
    "para_v": (S["para"], centre(S["para"]), 90),
    "tri_iso_v": (S["tri_iso"], centre(S["tri_iso"]), 90),
    "tri_right_d": (S["tri_right"], (40, 30), math.degrees(math.atan2(60, 80))),
    "trap_v": (S["trap"], centre(S["trap"]), 90),
    "trap_h": (S["trap"], centre(S["trap"]), 0),
    "rtrap_v": (S["rtrap"], centre(S["rtrap"]), 90),
    "kite_v": (S["kite"], (0, 0), 90),
    "kite_h": (S["kite"], (0, 0), 0),
    "hex_v": (S["hex_reg"], (0, 0), 90),
    "arrow_h": (S["hex_arrow"], (50, 40), 0),
    "L_diag": (S["hex_L"], centre(S["hex_L"]), 45),
}
AXIS_OK = {k: is_axis(*v) for k, v in AX.items()}
assert AXIS_OK == {"house_v": True, "house_h": False, "sq_diag": True, "sq_v": True, "rect_diag": False, "rect_h": True,
                   "rect_off": False, "para_v": False, "tri_iso_v": True, "tri_right_d": False, "trap_v": True,
                   "trap_h": False, "rtrap_v": False, "kite_v": True, "kite_h": False, "hex_v": True, "arrow_h": True,
                   "L_diag": False}, AXIS_OK


def ax_cv(key, k=1.0):
    pts, c, a = AX[key]
    return axis_cv(pts, c, a, k)


def ax_fit(key, w=90, h=106):
    k = 0.8
    while True:
        cv = ax_cv(key, k)
        if cv.size()[0] <= w and cv.size()[1] <= h:
            return cv
        k *= 0.97


def fit_shape(key, w=88, h=104, deg=0, kmax=1.0):
    k = kmax
    while True:
        cv = shape(key, deg, k)
        if cv.size()[0] <= w and cv.size()[1] <= h:
            return cv
        k *= 0.97


def mirror_grid_svg(cols=8, rows=4, line_at=4, dot=(2, 2), cell=26):
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


# ------------------------------------------------------------ composite shapes (E1.2)
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


PART_FILL = {"triangle": FILL4, "square": FILL3, "rectangle": FILL, "trapezoid": FILL2, "rhombus": "#b9d3ee", "hexagon": FILL4}


def comp_cv(c, k=1.0):
    cv = Canvas()
    for pts, kind in c["parts"]:
        cv.poly(scaled(pts, k), PART_FILL[kind], 2.6)
    return cv


def parts_count(c):
    out = {}
    for _, k in c["parts"]:
        out[k] = out.get(k, 0) + 1
    return out


def comp_fit(c, w=88, h=104):
    k = 1.0
    while True:
        cv = comp_cv(c, k)
        if cv.size()[0] <= w and cv.size()[1] <= h:
            return cv
        k *= 0.97


_s = 60.0
_h = _s * math.sqrt(3) / 2
_hx = regular(6, 60, 0)
C_HOUSE = composite([(R(0, 50, 80, 130), "square"), ([(0, 50), (80, 50), (40, 8)], "triangle")],
                    [(0, 130), (0, 50), (40, 8), (80, 50), (80, 130)])
C_HEX6 = composite([([(0, 0), _hx[i], _hx[(i + 1) % 6]], "triangle") for i in range(6)], _hx)
C_HEX2 = composite([(_hx[0:4], "trapezoid"), (_hx[3:6] + [_hx[0]], "trapezoid")], _hx)
C_HEX3R = composite([([(0, 0), _hx[i], _hx[(i + 1) % 6], _hx[(i + 2) % 6]], "rhombus") for i in (0, 2, 4)], _hx)
C_TRAP3 = composite([([(0, _h), (_s, _h), (_s / 2, 0)], "triangle"), ([(_s / 2, 0), (_s, _h), (1.5 * _s, 0)], "triangle"),
                     ([(_s, _h), (2 * _s, _h), (1.5 * _s, 0)], "triangle")],
                    [(0, _h), (2 * _s, _h), (1.5 * _s, 0), (_s / 2, 0)])
C_RHOMB2 = composite([([(0, _h), (_s, _h), (_s / 2, 0)], "triangle"), ([(_s / 2, 0), (_s, _h), (1.5 * _s, 0)], "triangle")],
                     [(0, _h), (_s, _h), (1.5 * _s, 0), (_s / 2, 0)])
C_2SQ = composite([(R(0, 0, 60, 60), "square"), (R(60, 0, 120, 60), "square")], R(0, 0, 120, 60))
C_4SQ = composite([(R(0, 0, 45, 45), "square"), (R(45, 0, 90, 45), "square"), (R(0, 45, 45, 90), "square"),
                   (R(45, 45, 90, 90), "square")], R(0, 0, 90, 90))
C_SQDIAG = composite([([(0, 0), (90, 0), (90, 90)], "triangle"), ([(0, 0), (90, 90), (0, 90)], "triangle")], R(0, 0, 90, 90))
C_RECTDIAG = composite([([(0, 0), (120, 0), (120, 60)], "triangle"), ([(0, 0), (120, 60), (0, 60)], "triangle")], R(0, 0, 120, 60))
C_SQ4TRI = composite([([(0, 0), (90, 0), (45, 45)], "triangle"), ([(90, 0), (90, 90), (45, 45)], "triangle"),
                      ([(90, 90), (0, 90), (45, 45)], "triangle"), ([(0, 90), (0, 0), (45, 45)], "triangle")], R(0, 0, 90, 90))
C_BIGTRI = composite([([(0, 80), (80, 80), (80, 0)], "triangle"), ([(80, 80), (160, 80), (80, 0)], "triangle")],
                     [(0, 80), (160, 80), (80, 0)])
C_HEXTT = composite([(_hx[0:4], "trapezoid")] + [([(0, 0), _hx[i], _hx[(i + 1) % 6]], "triangle") for i in (3, 4, 5)], _hx)
C_ROCKET = composite([(R(30, 40, 70, 140), "rectangle"), ([(30, 40), (70, 40), (50, 0)], "triangle"),
                      ([(30, 105), (30, 140), (10, 140)], "triangle"), ([(70, 105), (90, 140), (70, 140)], "triangle")],
                     [(50, 0), (70, 40), (70, 105), (90, 140), (10, 140), (30, 105), (30, 40)])
assert classify(C_HOUSE["outline"]) == "pentagon" and classify(C_2SQ["outline"]) == "rectangle"
assert classify(C_TRAP3["outline"]) == "trapezoid" and classify(C_RHOMB2["outline"]) == "rhombus"
assert classify(C_SQDIAG["outline"]) == "square" and classify(C_BIGTRI["outline"]) == "triangle"
assert classify(C_HEX2["outline"]) == "hexagon" and classify(C_HEX3R["outline"]) == "hexagon"


def tiles_cv(cells, k=24):
    """Square tiles at grid cells (col, row)."""
    cv = Canvas()
    for c, r in cells:
        cv.poly(R(c * k, r * k, (c + 1) * k, (r + 1) * k), FILL3, 2.4)
    return cv


TILE_A = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1)]           # 2 rows of 3
TILE_B = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (2, 1)]           # a T
TILE_C = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]                    # an L
TILE_D = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)]                    # steps


# ------------------------------------------------------------ set 1: name shapes by sides and vertices
NAME_E = {
    "triangle": "It has 3 straight sides and 3 vertices. It is a triangle.",
    "square": "It has 4 sides that are all the same length and 4 square corners. It is a square.",
    "rectangle": "It has 4 sides and 4 square corners. 2 sides are long and 2 are short. It is a rectangle.",
    "trapezoid": "It has 4 sides. Only the top and the bottom go the same way (they are parallel). It is a trapezoid.",
    "pentagon": "Count the sides: 5 sides and 5 vertices. It is a pentagon.",
    "hexagon": "Count the sides: 6 sides and 6 vertices. It is a hexagon.",
    "heptagon": "Count the sides: 7 sides and 7 vertices. It is a heptagon.",
    "octagon": "Count the sides: 8 sides and 8 vertices. It is an octagon.",
}
TURNED = " Turning a shape does not change its name."
SAME_LEN = " The sides do not have to be the same length."


def set_names(rnd, pos):
    its = []
    asks = ["What is this shape called?", "Name this shape.", "What shape is this?"]
    rows = [
        (shape("tri_eq"), "triangle", ["square", "pentagon", "hexagon"], NAME_E["triangle"]),
        (shape("tri_right", 160, 0.9), "triangle", ["rectangle", "square", "pentagon"], NAME_E["triangle"] + TURNED),
        (shape("square"), "square", ["rectangle", "triangle", "pentagon"], NAME_E["square"]),
        (shape("square", 45), "square", ["diamond", "rectangle", "triangle"],
         NAME_E["square"] + " It is only turned. “Diamond” is not its math name."),
        (shape("rect"), "rectangle", ["square", "pentagon", "trapezoid"], NAME_E["rectangle"]),
        (shape("rect", 90, 0.85), "rectangle", ["square", "triangle", "hexagon"], NAME_E["rectangle"] + TURNED),
        (shape("trap"), "trapezoid", ["triangle", "rectangle", "pentagon"], NAME_E["trapezoid"]),
        (shape("pent_reg"), "pentagon", ["hexagon", "octagon", "square"], NAME_E["pentagon"]),
        (shape("pent_house", 0, 0.8), "pentagon", ["hexagon", "square", "triangle"],
         NAME_E["pentagon"] + SAME_LEN + " It looks like a house, but it is one shape."),
        (shape("hex_reg"), "hexagon", ["octagon", "pentagon", "heptagon"], NAME_E["hexagon"]),
        (shape("hex_L", 90, 0.85), "hexagon", ["rectangle", "octagon", "pentagon"], NAME_E["hexagon"] + SAME_LEN),
        (shape("oct_reg"), "octagon", ["hexagon", "heptagon", "pentagon"], NAME_E["octagon"]),
        (shape("hept_arrow", 0, 0.95), "heptagon", ["hexagon", "octagon", "pentagon"],
         NAME_E["heptagon"] + " Count the corners that point in too."),
    ]
    for i, (cv, ans, wrong, e) in enumerate(rows):
        its.append(mcq(fig(cv.svg("a 2D shape")) + asks[i % 3], ans, wrong, e))
    for key, deg, s, what in [("pent_odd", 200, 0.85, "vertices"), ("oct_cut", 0, 0.8, "vertices"), ("hex_arrow", 0, 0.9, "sides")]:
        n = n_sides(key)
        one = "side" if what == "sides" else "vertex"
        q = fig(shape(key, deg, s).svg("a 2D shape")) + "How many %s does this shape have?" % what
        e = ("Put your finger on one %s and count as you go around. Stop when you get back to the start. "
             "Do not count the first one twice: %d %s." % (one, n, what))
        if key == "oct_cut":
            e += " Count the small corners too."
        if key == "hex_arrow":
            e += " Count the sides that point in too."
        its.append(mcq(q, n, [n + 1, n - 1, n + 2], e))
    its.append(mcq("A shape has 6 sides and 6 vertices. What is it?", "hexagon", ["pentagon", "octagon", "heptagon"],
                   "6 sides make a hexagon. 5 sides make a pentagon, 7 a heptagon and 8 an octagon."))
    grids = [
        ("Which shape is a hexagon?", ("hex_L", 90), [("pent_reg", 0), ("oct_reg", 0), ("hept_arrow", 0)],
         "%s has 6 sides, so it is a hexagon. The others have 5, 8 and 7 sides."),
        ("Which shape is a square?", ("square", 45), [("rhombus", 62.5), ("rect", 0), ("trap", 0)],
         "%s has 4 sides the same length and 4 square corners. It is a square that is turned. "
         "The other shape with 4 equal sides has no square corners."),
        ("Which shape is a trapezoid?", ("trap", 0), [("rect", 0), ("tri_iso", 0), ("pent_reg", 0)],
         "%s has 4 sides, and only the top and bottom go the same way. It is a trapezoid."),
    ]
    for q, (key, deg), others, e in grids:
        p = pos.next()
        cells = [fit_shape(k, deg=d, kmax=0.9) for k, d in others]
        cells.insert(p, fit_shape(key, deg=deg, kmax=0.9))
        its.append(mcq_fixed(fig(grid_svg(cells, "four 2D shapes labelled A to D")) + q, list("ABCD"), "ABCD"[p], e % "ABCD"[p]))
    assert len(its) == 20, len(its)
    return {"title": "Name shapes by their sides and vertices", "items": its}


# ------------------------------------------------------------ set 2: equal sides and square corners
def set_sides(rnd, pos, P):
    its = []
    k = 16
    # side lengths in cm (drawn to scale)
    r63 = R(0, 0, 6 * k, 3 * k)
    its.append(mcq(fig(labelled(r63, [6, 3, 6, 3], k).svg("a rectangle 6 cm long and 3 cm wide")) +
                   "How many sides of this rectangle are 6 cm long?", 2, [1, 4, 3],
                   "The top and the bottom are 6 cm. The 2 short sides are 3 cm. So 2 sides are 6 cm long."))
    sq = R(0, 0, 5 * k, 5 * k)
    its.append(mcq(fig(labelled(sq, [5, 0, 0, 0], k).svg("a square with one side 5 cm")) +
                   "This is a square. One side is 5 cm. How long is the side on the right?", "5 cm",
                   ["10 cm", "20 cm", "4 cm"],
                   "All 4 sides of a square are the same length. So every side is 5 cm."))
    teq = regular(3, 4 * k / math.sqrt(3))
    its.append(mcq(fig(labelled(teq, [4, 4, 4], k).svg("a triangle with sides 4 cm, 4 cm and 4 cm")) +
                   "How many sides of this triangle are the same length?", 3, [2, 1, 4],
                   "All 3 sides are 4 cm. So all 3 sides are the same length."))
    hh = math.sqrt(25 - 9) * k
    tiso = [(0, hh), (6 * k, hh), (3 * k, 0)]
    its.append(mcq(fig(labelled(tiso, [6, 5, 5], k).svg("a triangle with sides 6 cm, 5 cm and 5 cm")) +
                   "How many sides of this triangle are the same length?", 2, [3, 1, 0],
                   "The two slanted sides are both 5 cm. The bottom is 6 cm. So 2 sides are the same length."))
    t345 = [(0, 0), (0, 3 * k), (4 * k, 3 * k)]
    its.append(mcq(fig(labelled(t345, [3, 4, 5], k).svg("a triangle with sides 3 cm, 4 cm and 5 cm")) +
                   "Which is true about this triangle?", "All sides are different.",
                   ["2 sides are the same.", "All sides are the same.", "It has 4 sides."],
                   "The sides are 3 cm, 4 cm and 5 cm. No two are the same, so all 3 sides are different lengths."))
    r72 = R(0, 0, 7 * k, 2 * k)
    its.append(mcq(fig(labelled(r72, [7, 2, 0, 0], k).svg("a rectangle 7 cm long and 2 cm wide")) +
                   "How long is the bottom side of this rectangle?", "7 cm", ["2 cm", "9 cm", "5 cm"],
                   "The bottom is across from the top. In a rectangle, sides across from each other are the same length: 7 cm."))
    ht = math.sqrt(25 - 4) * k
    trp = [(0, ht), (7 * k, ht), (5 * k, 0), (2 * k, 0)]
    its.append(mcq(fig(labelled(trp, [7, 5, 3, 5], k).svg("a trapezoid with sides 7 cm, 5 cm, 3 cm and 5 cm")) +
                   "Which 2 sides of this trapezoid are the same length?", "the 2 slanted sides",
                   ["the top and bottom", "the top and 1 slanted side", "all 4 sides"],
                   "The 2 slanted sides are both 5 cm. The top is 3 cm and the bottom is 7 cm, so they are different."))
    # square corners
    for key, deg, s, extra in [("rect", 0, 0.9, " They are square corners, like the corner of a book."),
                               ("tri_right", 0, 1.0, " The other 2 corners are pointy, not square."),
                               ("rtrap", 0, 1.0, " The 2 corners on the left are square. The other 2 are not."),
                               ("rhombus", 0, 1.0, " Its corners are pointy or wide. None of them is a square corner."),
                               ("square", 45, 0.9, " Turning a square does not change its corners."),
                               ("tri_eq", 0, 1.0, " All 3 corners are pointy, smaller than a square corner.")]:
        n = CORNERS[key]
        e = "This shape has %d square corner%s.%s" % (n, "" if n == 1 else "s", extra)
        wrong = {4: [2, 0, 8], 1: [3, 0, 2], 2: [4, 1, 0], 0: [4, 2, 3]}[n]
        if key == "tri_eq":
            wrong = [3, 1, 2]
        its.append(mcq(fig(shape(key, deg, s).svg("a 2D shape")) + "How many square corners does this shape have?", n, wrong, e))
    # sorting by sides and corners
    its.append(mcq("Which shape has 4 sides the same length and 4 square corners?", "square",
                   ["rectangle", "trapezoid", "triangle"],
                   "A square has 4 equal sides and 4 square corners. A rectangle has 4 square corners, but 2 long and 2 short sides."))
    its.append(mcq("A square and a rectangle both have 4 square corners. How are they different?",
                   "A square has 4 equal sides.", ["A square has 5 sides.", "A rectangle has 3 sides.", "A square is turned."],
                   "Both have 4 sides and 4 square corners. In a square, all 4 sides are the same length."))
    its.append(mcq("A triangle has 1 square corner. How many of its corners are not square?", 2, [1, 3, 0],
                   "A triangle has 3 corners. 1 is square, so 3 − 1 = 2 corners are not square."))
    n, he, his = P.next()
    its.append(mcq("%s turns a square so it stands on a corner. %s says it is now a diamond. What is it?" % (n, he.capitalize()),
                   "still a square", ["a diamond", "a rectangle", "a triangle"],
                   "Turning a shape does not change its sides or corners. It still has 4 equal sides and 4 square corners, so it is still a square."))
    for q, right, others, e in [
            ("Which shape has 3 sides the same length?", ("tri_eq", 0), [("tri_iso", 0), ("tri_right", 0), ("square", 0)],
             "%s has 3 sides that are all the same length. The other triangles have only 2 equal sides or none."),
            ("Which shape has no square corners?", ("rhombus", 0), [("rect", 0), ("tri_right", 0), ("square", 45)],
             "%s has 2 pointy corners and 2 wide corners. The others each have at least 1 square corner."),
            ("Which shape has 4 equal sides but no square corners?", ("rhombus", 62.5), [("square", 0), ("rect", 0), ("trap", 0)],
             "%s has 4 sides the same length, but its corners are not square. The square has 4 square corners."),
    ]:
        p = pos.next()
        cells = [fit_shape(kk, deg=d, kmax=0.9) for kk, d in others]
        cells.insert(p, fit_shape(right[0], deg=right[1], kmax=0.9))
        its.append(mcq_fixed(fig(grid_svg(cells, "four 2D shapes labelled A to D")) + q, list("ABCD"), "ABCD"[p], e % "ABCD"[p]))
    assert len(its) == 20, len(its)
    return {"title": "Equal sides and square corners", "items": its}


# ------------------------------------------------------------ set 3: lines of symmetry
YES = "Yes, the halves match."
NO = "No, they do not match."
CUTS = "Yes, it cuts it in 2."
UPDOWN = "No, it must go up and down."


def set_symmetry(rnd, pos, P):
    its = []
    for key, name, why in [
            ("house_v", "a pentagon", "Fold along the line: the left half lands exactly on the right half."),
            ("sq_diag", "a square", "Fold the square from corner to corner: the 2 halves match. A line of symmetry can be slanted."),
            ("rect_h", "a rectangle", "Fold along the line: the top half lands exactly on the bottom half. "
                                      "A line of symmetry can go side to side."),
            ("tri_iso_v", "a triangle", "Fold along the line: the 2 slanted sides are the same length, so the halves match."),
            ("rect_diag", "a rectangle", "Fold a rectangle from corner to corner and the corners stick out. "
                                         "The 2 triangles are the same size, but they do not match when you fold."),
            ("para_v", "a slanted shape", "Fold along the line: the slanted sides go opposite ways, so the halves do not match."),
            ("trap_h", "a trapezoid", "The top half is narrower than the bottom half, so the halves do not match when you fold."),
            ("kite_v", "a kite shape", "Fold along the line: the left half lands exactly on the right half."),
    ]:
        ok = AXIS_OK[key]
        right = YES if ok else NO
        wrong = [NO if ok else YES, CUTS, UPDOWN]
        if key in ("house_v", "tri_iso_v", "kite_v"):
            wrong = [NO, CUTS, "No, it must go across."]
        q = fig(ax_cv(key).svg("%s with a dashed line" % name)) + "Is the dashed line a line of symmetry?"
        its.append(mcq(q, right, wrong, why))
    for key, wrong, e in [
            ("square", [2, 8, 1], "A square has 4 lines of symmetry: up and down, side to side and 2 from corner to corner. "
                                  "Do not forget the 2 slanted lines."),
            ("rect", [4, 1, 0], "Fold it top to bottom or side to side: 2 lines. A fold from corner to corner does not match."),
            ("tri_eq", [1, 6, 0], "This triangle has 3 equal sides. A line goes from each corner to the middle of the side across: 3 lines."),
            ("trap", [2, 0, 4], "Only the up-and-down line in the middle makes halves that match. The top is shorter than the bottom, "
                                "so a side-to-side fold does not match."),
            ("para", [2, 1, 4], "No fold makes the halves match, because the sides slant. It has 0 lines of symmetry."),
            ("hex_reg", [3, 12, 2], "This hexagon has 6 equal sides. 3 lines go through opposite corners and 3 through the middles "
                                    "of opposite sides: 6 lines."),
    ]:
        n = AXES[key]
        its.append(mcq(fig(shape(key, 0, 0.9).svg("a 2D shape")) + "How many lines of symmetry does this shape have?", n, wrong, e))
    for q, right, others, e in [
            ("Which picture shows a line of symmetry?", "sq_v", ["rect_diag", "trap_h", "L_diag"],
             "%s shows a line of symmetry: the 2 halves match when you fold. The other lines cut the shape in two, but the halves do not match."),
            ("Which picture shows a line of symmetry?", "arrow_h", ["house_h", "rect_off", "rtrap_v"],
             "%s shows a line of symmetry: the top half of the shape matches the bottom half. The other halves do not match."),
    ]:
        p = pos.next()
        cells = [ax_fit(k) for k in others]
        cells.insert(p, ax_fit(right))
        assert AXIS_OK[right] and not any(AXIS_OK[k] for k in others)
        its.append(mcq_fixed(fig(grid_svg(cells, "four shapes with dashed lines labelled A to D")) + q,
                             list("ABCD"), "ABCD"[p], e % "ABCD"[p]))
    p = pos.next()
    others = ["square", "tri_iso", "rect"]
    cells = [fit_shape(k, kmax=0.9) for k in others]
    cells.insert(p, fit_shape("para", kmax=0.9))
    assert AXES["para"] == 0 and all(AXES[k] > 0 for k in others)
    its.append(mcq_fixed(fig(grid_svg(cells, "four 2D shapes labelled A to D")) + "Which shape has no lines of symmetry?",
                         list("ABCD"), "ABCD"[p],
                         "%s has slanted sides that go the same way, so no fold makes matching halves. "
                         "The square, the triangle and the rectangle each have at least 1 line of symmetry." % "ABCD"[p]))
    its.append(mcq(fig(mirror_grid_svg()) + "The dashed line is a mirror line. The dot is 2 squares to the left of it. "
                   "Where is the matching dot?", "2 squares to the right", ["4 squares to the right", "2 squares to the left",
                                                                           "2 squares down"],
                   "A matching dot is the same distance from the mirror line, on the other side: 2 squares to the right. "
                   "4 counts the distance between the dots."))
    its.append(mcq("Think of the flag of Canada. How many lines of symmetry does it have?", 1, [2, 4, 0],
                   "Fold the flag down the middle: the red bands and the two halves of the maple leaf match. "
                   "Fold it across and the leaf does not match upside down. So there is only 1 line."))
    n, he, his = P.next()
    its.append(mcq("%s folds a paper in half and cuts half a heart along the fold. Where is the line of symmetry of the heart?" % n,
                   "along the fold", ["along the cut edge", "across the middle", "there is none"],
                   "When %s opens the paper, the fold is the line of symmetry. Both halves were cut together, so they match." % n))
    assert len(its) == 20, len(its)
    return {"title": "Lines of symmetry", "items": its}


# ------------------------------------------------------------ set 4: compose and decompose
def set_compose(rnd, pos, P):
    its = []
    q2 = lambda c, t, k=1.0: fig(comp_cv(c, k).svg("a shape made of smaller shapes")) + t

    def add(c, t, right, wrong, e, want=None, k=1.0):
        if want is not None:
            assert parts_count(c) == want, (parts_count(c), want)
        its.append(mcq(q2(c, t, k), right, wrong, e))

    add(C_SQDIAG, "Which shapes make this square?", "2 triangles", ["2 rectangles", "4 triangles", "2 squares"],
        "The line goes from one corner to the opposite corner. It cuts the square into 2 triangles.", {"triangle": 2}, 0.9)
    add(C_2SQ, "Which shapes make this rectangle?", "2 squares", ["4 squares", "2 triangles", "2 rectangles"],
        "The line in the middle cuts the rectangle into 2 squares. Each part has 4 equal sides.", {"square": 2})
    add(C_HEX6, "How many triangles make this hexagon?", 6, [3, 4, 8],
        "Count the triangles around the centre: 6. Each side of the hexagon belongs to 1 triangle.", {"triangle": 6}, 0.8)
    add(C_HEX2, "Which shapes make this hexagon?", "2 trapezoids", ["2 triangles", "2 rectangles", "2 pentagons"],
        "The line cuts the hexagon into 2 parts. Each part has 4 sides and is a trapezoid, like the trapezoid pattern block.",
        {"trapezoid": 2}, 0.8)
    add(C_TRAP3, "How many triangles make this trapezoid?", 3, [2, 4, 6],
        "Count the parts: 3 triangles. 3 triangle pattern blocks cover 1 trapezoid block.", {"triangle": 3})
    add(C_RHOMB2, "Which shapes make this shape?", "2 triangles", ["2 squares", "3 triangles", "a triangle and a square"],
        "The line cuts it into 2 triangles. 2 triangle pattern blocks make 1 rhombus block.", {"triangle": 2})
    add(C_HEX3R, "How many parts make this hexagon?", 3, [6, 2, 4],
        "Count the parts: 3. Each part has 4 equal sides. 3 of these pattern blocks cover a hexagon.", {"rhombus": 3}, 0.8)
    add(C_HOUSE, "Which two shapes make this house?", "a square and a triangle",
        ["a pentagon and a triangle", "2 squares", "a rectangle and a circle"],
        "The wall is a square (4 equal sides) and the roof is a triangle (3 sides).", {"square": 1, "triangle": 1}, 0.9)
    add(C_HOUSE, "How many sides does the outline of the whole house have?", 5, [7, 6, 4],
        "Go around the outside: 2 walls, the floor and 2 roof sides. That is 5 sides, so the outline is a pentagon. "
        "Do not add 4 + 3 = 7: the line between the roof and the wall is inside.", None, 0.9)
    add(C_ROCKET, "Which shapes make this rocket?", "1 rectangle, 3 triangles",
        ["1 rectangle, 2 triangles", "1 square, 3 triangles", "2 rectangles, 3 triangles"],
        "The body is a rectangle. The nose is a triangle and there is a triangle on each side: 1 + 2 = 3 triangles.",
        {"rectangle": 1, "triangle": 3}, 0.8)
    add(C_SQ4TRI, "How many triangles make this square?", 4, [2, 8, 3],
        "The 2 lines cross in the middle. Count the parts: 4 triangles.", {"triangle": 4}, 0.9)
    add(C_HEXTT, "Which shapes make this hexagon?", "1 trapezoid, 3 triangles",
        ["2 trapezoids", "1 trapezoid, 2 triangles", "4 triangles"],
        "The top part is a trapezoid. The bottom half is cut into 3 triangles. 3 triangles cover the same space as 1 trapezoid.",
        {"trapezoid": 1, "triangle": 3}, 0.8)
    # the space a shape covers stays the same
    assert abs(abs(area(C_SQDIAG["outline"])) * (80 / 90) ** 2 - abs(area(C_BIGTRI["outline"]))) < 1e-6
    sqd = comp_cv(C_SQDIAG, 80 / 90)
    its.append(mcq(fig(row_svg([sqd, comp_cv(C_BIGTRI)], ["A", "B"], "a square of 2 triangles and the same 2 triangles moved", gap=36)) +
                   "Shape B is made from the 2 triangles of shape A, moved. Which shape covers more space?",
                   "They cover the same space.", ["A covers more.", "B covers more.", "You cannot tell."],
                   "B uses the same 2 triangles as A. Nothing was added or cut off, so both cover the same space. B is only wider."))
    assert len(TILE_A) == len(TILE_B) == 6
    its.append(mcq(fig(row_svg([tiles_cv(TILE_A), tiles_cv(TILE_B)], ["A", "B"], "two shapes made of square tiles", gap=36)) +
                   "Which shape covers more space?", "They cover the same space.",
                   ["A covers more.", "B covers more.", "You cannot tell."],
                   "Count the tiles. A has 6 squares and B has 6 squares. The same tiles were moved, so they cover the same space. "
                   "B is longer, but it is not bigger."))
    its.append(mcq(fig(tiles_cv(TILE_C).svg("a shape made of square tiles")) +
                   "How many square tiles make this shape?", len(TILE_C), [len(TILE_C) - 1, len(TILE_C) + 1, 3],
                   "Count each tile once: 3 going down and 2 more along the bottom. The corner tile is counted only once: 3 + 2 = 5."))
    n, he, his = P.next()
    its.append(mcq(fig(tiles_cv(TILE_D).svg("a shape made of square tiles")) +
                   "%s moves all these tiles into one long row. How many tiles are in the row?" % n,
                   len(TILE_D), [len(TILE_D) - 1, len(TILE_D) + 1, 3],
                   "Moving tiles does not change how many there are. There are 5 tiles, so the row has 5 tiles. "
                   "3 counts only the steps."))
    its.append(mcq("You put 2 squares of the same size side by side. Which shape do you make?", "a rectangle",
                   ["a bigger square", "an octagon", "a hexagon"],
                   "2 squares side by side make a rectangle. It has 4 sides, not 4 + 4 = 8."))
    n, he, his = P.next()
    its.append(mcq("%s cuts a square from one corner to the opposite corner. What shapes does %s get?" % (n, he), "2 triangles",
                   ["2 rectangles", "2 squares", "4 triangles"],
                   "A cut from corner to corner makes 2 triangles. A cut across the middle would make 2 rectangles."))
    p = pos.next()
    others = [C_HOUSE, C_2SQ, C_HEX2]
    cells = [comp_fit(c) for c in others]
    cells.insert(p, comp_fit(C_SQDIAG))
    its.append(mcq_fixed(fig(grid_svg(cells, "four shapes made of smaller shapes labelled A to D")) +
                         "Which square is made of 2 triangles?", list("ABCD"), "ABCD"[p],
                         "%s is a square cut from corner to corner into 2 triangles. The others are a square and a triangle, "
                         "2 squares, and 2 trapezoids." % "ABCD"[p]))
    p = pos.next()
    others = [C_HEX6, C_SQ4TRI, C_HEX2]
    cells = [comp_fit(c) for c in others]
    cells.insert(p, comp_fit(C_TRAP3))
    its.append(mcq_fixed(fig(grid_svg(cells, "four shapes made of smaller shapes labelled A to D")) +
                         "Which shape is made of exactly 3 triangles?", list("ABCD"), "ABCD"[p],
                         "%s is a trapezoid made of 3 triangles. The others have 6 triangles, 4 triangles and 2 trapezoids." % "ABCD"[p]))
    assert parts_count(C_TRAP3) == {"triangle": 3}
    assert len(its) == 20, len(its)
    return {"title": "Put shapes together and take them apart", "items": its}


# ------------------------------------------------------------ set 5: congruent shapes and shape problems
CY = "Yes, same shape and size"
CN_SIZE = "No, not the same size"
CN_SHAPE = "No, not the same shape"
CN_TURN = "No, one is turned"


def pair_svg(a, b, label):
    return row_svg([poly_cv(a), poly_cv(b, FILL2)], ["", ""], label, gap=40)


def set_congruent(rnd, pos, P):
    its = []
    T = SHAPES
    pairs = [
        (tpts(T["square"], 0, 0.9), tpts(T["square"], 45, 0.9), "A square turned is still the same square. "
         "Same shape and same size, so they are congruent."),
        (tpts(T["tri_iso"], 0, 1.0), tpts(T["tri_iso"], 0, 0.6), "They are the same shape, but one is smaller. "
         "Congruent shapes must be the same size too."),
        (tpts(T["rect"], 0, 0.8), tpts(T["rect"], 90, 0.8), "The rectangle is turned. It has the same sides and corners, "
         "so the two shapes are congruent."),
        (tpts(T["tri_right"], 0, 1.0), tpts(T["tri_right"], 0, 1.0, flip=True), "One triangle is flipped over. "
         "Flipping does not change the sides or corners, so they are congruent."),
        (tpts(T["hex_reg"], 0, 0.9), tpts(T["hex_reg"], 0, 0.65), "Both are hexagons with equal sides, but one is smaller. "
         "So they are not congruent."),
        (tpts(T["rect"], 0, 0.7), tpts(T["square"], 0, 0.95), "One is a rectangle and one is a square. They are not the same shape."),
        (tpts(T["trap"], 0, 0.85), tpts(T["trap"], 180, 0.85), "The trapezoid is turned upside down. It is still the same shape and size."),
        (tpts(T["tri_eq"], 0, 1.0), tpts(T["tri_iso"], 0, 0.9), "Both are triangles, but they are not the same shape. "
         "Only one has 3 equal sides."),
    ]
    for a, b, e in pairs:
        if congruent(a, b):
            right, wrong = CY, [CN_TURN, CN_SIZE, CN_SHAPE]
        elif same_shape(a, b):
            right, wrong = CN_SIZE, [CY, CN_SHAPE, CN_TURN]
        else:
            right, wrong = CN_SHAPE, [CY, CN_SIZE, CN_TURN]
        its.append(mcq(fig(pair_svg(a, b, "two shapes")) + "Are these 2 shapes congruent?", right, wrong, e))
    # one-of-four rows: which shape is congruent to the first?
    for base, opts, e in [
            (tpts(T["tri_right"], 0, 0.8),
             [tpts(T["tri_right"], 0, 1.05), tpts(T["tri_right"], 90, 0.8), tpts(T["tri_iso"], 0, 0.8), tpts(T["tri_thin"], 0, 0.7)],
             "%s is the same triangle, turned. The others are bigger or a different shape."),
            (tpts(T["rect"], 0, 0.6),
             [tpts(T["rect"], 0, 0.85), tpts(T["square"], 0, 0.75), tpts(T["rect"], 90, 0.6), tpts(T["para"], 0, 0.55)],
             "%s is the same rectangle, standing up. The others are a bigger rectangle, a square and a slanted shape."),
    ]:
        p = pos.next()
        right = [o for o in opts if congruent(base, o)]
        assert len(right) == 1, len(right)
        others = [o for o in opts if not congruent(base, o)]
        order = others[:p] + right + others[p:]
        cvs = [poly_cv(base, FILL2)] + [poly_cv(o) for o in order]
        svg = row_svg(cvs, ["this one", "A", "B", "C", "D"], "a shape and four shapes labelled A to D", gap=20)
        its.append(mcq_fixed(fig(svg) + "Which shape is congruent to “this one”?", list("ABCD"), "ABCD"[p], e % "ABCD"[p]))
    # congruent lengths
    its.append(mcq("Which 2 pencils have congruent lengths?", "12 cm and 12 cm", ["12 cm and 21 cm", "10 cm and 12 cm", "6 cm and 12 cm"],
                   "Congruent lengths are exactly the same length. 12 cm and 12 cm are the same."))
    its.append(mcq("Two triangles are congruent. One has sides of 3 cm, 4 cm and 5 cm. What are the sides of the other?",
                   "3 cm, 4 cm and 5 cm", ["6 cm, 8 cm and 10 cm", "3 cm, 3 cm and 3 cm", "4 cm, 4 cm and 5 cm"],
                   "Congruent shapes are the same shape and size, so the sides are the same: 3 cm, 4 cm and 5 cm. "
                   "6, 8 and 10 cm would make a bigger triangle."))
    # word problems
    n, he, his = P.next()
    its.append(mcq("%s sees a yield sign. It is a triangle with 3 equal sides. How many lines of symmetry does the shape have?" % n,
                   AXES["tri_eq"], [1, 0, 6],
                   "A triangle with 3 equal sides has 3 lines of symmetry, one from each corner to the middle of the side across."))
    n, he, his = P.next()
    its.append(mcq("%s cuts a square sandwich from corner to corner. What does %s get?" % (n, he), "2 congruent triangles",
                   ["2 congruent squares", "2 different triangles", "4 triangles"],
                   "A cut from corner to corner makes 2 triangles. They are the same shape and size, so they are congruent."))
    n, he, his = P.next()
    its.append(mcq("%s makes a quilt with congruent squares. One square is 10 cm on each side. How long is a side of another square?" % n,
                   "10 cm", ["20 cm", "40 cm", "5 cm"],
                   "Congruent squares are the same size, so every side of every square is 10 cm."))
    its.append(mcq("A stop sign is an octagon. How many vertices does it have?", 8, [6, 7, 16],
                   "An octagon has 8 sides and 8 vertices. 16 adds the sides and the vertices."))
    n, he, his = P.next()
    its.append(mcq("%s covers 2 hexagon blocks with green triangle blocks. How many triangles does %s use?" % (n, he), 12,
                   [6, 8, 2], "6 triangles cover 1 hexagon. 2 hexagons need 6 + 6 = 12 triangles."))
    n, he, his = P.next()
    its.append(mcq("A window is a square made of 4 congruent small squares, 2 across and 2 down. Each small square is 30 cm "
                   "on each side. How wide is the whole window?", "60 cm", ["30 cm", "120 cm", "90 cm"],
                   "2 small squares go across. 30 cm + 30 cm = 60 cm."))
    n, he, his = P.next()
    its.append(mcq("%s has a picture frame shaped like a rectangle. The top is 25 cm long. How long is the bottom?" % n,
                   "25 cm", ["50 cm", "100 cm", "You cannot tell."],
                   "In a rectangle, the top and the bottom are the same length. So the bottom is 25 cm too."))
    n, he, his = P.next()
    its.append(mcq("%s puts 2 congruent paper triangles together to make a square. How many sides does the square have?" % n,
                   4, [6, 3, 8], "A square has 4 sides. Do not add 3 + 3 = 6: the sides where the triangles touch are inside."))
    assert len(its) == 20, len(its)
    return {"title": "Congruent shapes and shape problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def marked_square_rect():
    """A square with equal-side marks and square-corner marks, and a rectangle with square-corner marks."""
    sq = R(0, 0, 70, 70)
    a = Canvas()
    a.poly(sq, FILL, 3)
    for i in range(4):
        tick(a, sq[i], sq[(i + 1) % 4], 1)
        corner_mark(a, sq, i)
    rc = R(0, 0, 110, 55)
    b = Canvas()
    b.poly(rc, FILL, 3)
    for i in range(4):
        tick(b, rc[i], rc[(i + 1) % 4], 1 if i % 2 == 0 else 2)
        corner_mark(b, rc, i)
    t = tpts(SHAPES["tri_eq"], 0, 1.1)
    c = Canvas()
    c.poly(t, FILL, 3)
    for i in range(3):
        tick(c, t[i], t[(i + 1) % 3], 1)
    return row_svg([a, b, c], ["4 equal sides", "2 long, 2 short", "3 equal sides"],
                   "a square, a rectangle and a triangle with marks on equal sides and square corners", gap=30)


def body_html():
    names = row_svg([shape("tri_eq", 0, 0.75), shape("square", 0, 0.8), shape("rect", 0, 0.65), shape("trap", 0, 0.6),
                     shape("pent_reg", 0, 0.75), shape("hex_reg", 0, 0.75), shape("hept_arrow", 0, 0.75), shape("oct_reg", 0, 0.75)],
                    ["triangle", "square", "rectangle", "trapezoid", "pentagon", "hexagon", "heptagon", "octagon"],
                    "triangle, square, rectangle, trapezoid, pentagon, hexagon, heptagon and octagon", gap=12, fs=14)
    turned = row_svg([shape("square", 0, 0.9), shape("square", 45, 0.9), shape("hex_reg", 0, 0.8), shape("hex_L", 0, 0.75)],
                     ["square", "still a square", "hexagon", "also a hexagon"],
                     "a square and the same square turned; a hexagon and a hexagon with sides of different lengths", gap=26, fs=14)
    sym = row_svg([ax_cv("house_v", 0.8), ax_cv("sq_diag", 0.8), ax_cv("rect_diag", 0.6)],
                  ["matching halves", "matching halves", "not matching"],
                  "two lines of symmetry and one line that is not a line of symmetry", gap=30, fs=14)
    comps = row_svg([comp_cv(C_SQDIAG, 0.7), comp_cv(C_HEX6, 0.6), comp_cv(C_HEX2, 0.6), comp_cv(C_TRAP3, 0.6)],
                    ["2 triangles", "6 triangles", "2 trapezoids", "3 triangles"],
                    "a square made of 2 triangles, a hexagon made of 6 triangles, a hexagon made of 2 trapezoids and a trapezoid made of 3 triangles",
                    gap=22, fs=14)
    same = row_svg([comp_cv(C_SQDIAG, 70 / 90), comp_cv(C_BIGTRI, 70 / 80)], ["square", "same 2 triangles"],
                   "a square made of 2 triangles and the same 2 triangles moved into one big triangle", gap=40, fs=14)
    cong = row_svg([shape("tri_right", 0, 0.8), shape("tri_right", 90, 0.8, fill=FILL2), shape("tri_right", 0, 0.5, fill=FILL2)],
                   ["shape", "congruent", "not congruent"],
                   "a triangle, the same triangle turned, and a smaller copy", gap=30, fs=14)
    return (
        "<h2>Sides and vertices</h2>"
        "<p>A 2D shape is flat. Count its <b>sides</b> to find its name. A <b>vertex</b> is a corner where two sides meet. "
        "Two or more are called <b>vertices</b>. A shape with straight sides has as many vertices as sides.</p>"
        "<figure class='sn-fig'>" + names + "</figure>" +
        table(["Shape", "Sides", "Vertices"], [
            ["Triangle", "3", "3"], ["Square", "4, all the same length", "4"], ["Rectangle", "4, 2 long and 2 short", "4"],
            ["Trapezoid", "4, only 1 pair go the same way", "4"], ["Pentagon", "5", "5"], ["Hexagon", "6", "6"],
            ["Heptagon", "7", "7"], ["Octagon", "8", "8"]]) +
        "<p>Turning a shape does not change its name. The sides do not have to be the same length.</p>"
        "<figure class='sn-fig'>" + turned +
        "<figcaption>A turned square is still a square, not a “diamond”. Any shape with 6 straight sides is a hexagon.</figcaption></figure>" +
        ex("Example 1", "How many vertices does a hexagon have?",
           "A hexagon has 6 sides. A shape with straight sides has the same number of vertices as sides.", "6 vertices") +
        "<h2>Equal sides and square corners</h2>"
        "<p>Compare the <b>side lengths</b>: are they all the same, or are some longer? Look at the <b>corners</b> too. "
        "A <b>square corner</b> (a right angle) looks like the corner of a book. The small marks show sides that are the same length.</p>"
        "<figure class='sn-fig'>" + marked_square_rect() + "</figure>" +
        ex("Example 2", "A square and a rectangle both have 4 square corners. How are they different?",
           "Look at the sides. All 4 sides of a square are the same length. A rectangle has 2 long and 2 short sides.",
           "the side lengths") +
        "<h2>Lines of symmetry</h2>"
        "<p>A <b>line of symmetry</b> cuts a shape into 2 matching halves. Fold along the line: one half lands exactly on the other. "
        "The line can go up and down, side to side or on a slant.</p>"
        "<figure class='sn-fig'>" + sym +
        "<figcaption>Fold a rectangle from corner to corner and the corners stick out, so that line is not a line of symmetry.</figcaption></figure>" +
        ex("Example 3", "How many lines of symmetry does a square have?",
           "Fold it up and down, side to side, and corner to corner both ways. Each fold matches.", "4 lines") +
        "<h2>Put shapes together and take them apart</h2>"
        "<p>Small shapes can make a bigger shape. Big shapes can be cut into smaller ones. Pattern blocks are a good way to try this.</p>"
        "<figure class='sn-fig'>" + comps + "</figure>"
        "<p>If you move the parts to make a new shape, it covers the <b>same space</b>. Nothing was added or taken away.</p>"
        "<figure class='sn-fig'>" + same + "</figure>" +
        ex("Example 4", "6 square tiles make a rectangle. You move them to make a T. How many tiles are in the T?",
           "Moving tiles does not change how many there are.", "6 tiles") +
        "<h2>Congruent shapes</h2>"
        "<p>Shapes are <b>congruent</b> when they are the same shape and the same size. One can be turned or flipped. "
        "Lengths are congruent when they are exactly the same length.</p>"
        "<figure class='sn-fig'>" + cong + "</figure>" +
        ex("Example 5", "Two squares have sides of 4 cm and 6 cm. Are they congruent?",
           "They are the same shape, but not the same size.", "no") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Calling a turned square a “diamond”", "Check the sides and corners: 4 equal sides and 4 square corners make a square"],
            ["Counting a side twice, or missing one", "Keep your finger on the first side and stop when you get back to it"],
            ["Adding the sides of the parts", "Count only the sides around the outside of the whole shape"],
            ["Any line that cuts a shape in two is a line of symmetry", "Fold it: the halves must match exactly"],
            ["Forgetting slanted lines of symmetry", "Try folding from corner to corner too"],
            ["Saying a turned shape is not congruent", "Turning or flipping does not change the size or the shape"],
        ])
    )


FAQ = [
    {"q": "What 2D shapes do Grade 2 students learn in Ontario?",
     "a": "Grade 2 students sort and name triangles, squares, rectangles, trapezoids, pentagons, hexagons, heptagons and octagons. They compare the number of sides, side lengths, angles and lines of symmetry (Spatial Sense, expectation E1.1)."},
    {"q": "Is a diamond a shape in math?",
     "a": "No. A “diamond” is usually a square that is turned, or a shape with 4 equal sides that is not a square. Turning a shape does not change its name, so a turned square is still a square."},
    {"q": "What does congruent mean in Grade 2 math?",
     "a": "Congruent shapes are the same shape and the same size, even if one is turned or flipped. Congruent lengths are exactly the same length (expectation E1.3)."},
    {"q": "How can I help my child learn shapes and symmetry at home?",
     "a": "Cut shapes out of paper and fold them to find matching halves. Use pattern blocks or cut squares into triangles, then move the pieces to make new shapes."},
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
    rnd = random.Random(42812)
    P = People(rnd)
    pos = Pos(rnd)
    sets = [set_names(rnd, pos), set_sides(rnd, pos, P), set_symmetry(rnd, pos, P), set_compose(rnd, pos, P),
            set_congruent(rnd, pos, P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-2", "slug": "2d-shapes-and-symmetry", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "2D Shapes and Symmetry: Sides, Vertices and Congruent Shapes",
        "seo_title": "Grade 2 Math 2D Shapes and Symmetry Worksheets: Sides, Vertices, Congruent Shapes (Free, Answer Key)",
        "short_title": "2D shapes and symmetry",
        "domain": "Spatial Sense",
        "standard_code": "Grade 2: E1.1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Sort and identify two-dimensional shapes by comparing number of sides, side lengths, angles, and number of lines of symmetry",
        "meta_desc": "Free Grade 2 math worksheets on 2D shapes and symmetry for the Ontario curriculum: name shapes from triangles to octagons, compare sides and square corners, find lines of symmetry, put shapes together and take them apart, and spot congruent shapes. 100 questions with an answer key.",
        "key_big": "Count the sides to name a shape. Turning a shape does not change its name.",
        "key_sub": "A turned square is still a square, not a “diamond”. A line of symmetry makes 2 halves that match when you fold. Congruent shapes are the same shape and the same size.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(four 2D shapes labelled A to D|four shapes made of smaller shapes labelled A to D|four shapes with dashed lines labelled A to D|a square grid|a shape and four shapes|a square of 2 triangles|two shapes made of square tiles)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
