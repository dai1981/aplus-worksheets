# -*- coding: utf-8 -*-
"""
Australia Year 4 Maths: Shapes and composite objects (Australian Curriculum v9.0, AC9M4SP01)
  python3 tools/gen_au_maths_y4_composite_shapes.py
HTML attributes use single quotes (no backslashes in the JSON). Australian English.

Year 4 students represent and approximate composite shapes and objects in the environment, using
combinations of familiar shapes (triangles, quadrilaterals incl. squares, rectangles and trapeziums,
pentagons, hexagons, octagons, circles) and objects (cubes, prisms, pyramids, cylinders, cones, spheres).

Pictures (checked in code):
  2-D shapes   every shape is named from its own corners (sides after joining straight runs, right angles,
               parallel sides), so a picture can never show a different shape from its label; right angles
               are counted from the interior angles (an inside corner of 270 degrees is not a right angle)
  composites   the parts must fill the outline exactly (areas add up) and every part is named from its corners
  hidden shapes triangles and rectangles in line drawings are counted by brute force from the segments
  3-D objects  drawn from 3-D vertices and faces (back faces hidden); composite objects share one view;
               cones and cylinders use ellipses with the cone sides drawn as true tangents
  cube stacks  only the 3 outside faces you can see are drawn; the cubes you can see are a·b·c − (a−1)(b−1)(c−1)
Wrong answers come from real student mistakes: a square is not called a rectangle, adding the sides of the
parts to get the sides of the outline, naming a 2-D shape for a 3-D object, prism vs pyramid, cone vs pyramid,
forgetting the big shape made of small ones, counting only the cubes or faces you can see, forgetting
faces that are glued together.
"""
import itertools, json, math, os, random, re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL, BASE, SIDE, TOP3 = "#cfe6d6", "#f6dcb4", "#a9d3b6", "#e6f2e9"
YEL = "#f3d27a"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]

CUBE, RP, TP, SP = "cube", "rectangular prism", "triangular prism", "square-based pyramid"
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


# ------------------------------------------------------------ 2-D shape facts (screen coordinates, y down)
def area(pts):
    n = len(pts)
    return sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n)) / 2.0


def simplify(pts):
    """Join straight runs: a corner of 180 degrees is not a corner."""
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
    """Interior angles in degrees (works for shapes with an inside corner)."""
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
            return "trapezium"
        return "quadrilateral"
    return {5: "pentagon", 6: "hexagon", 8: "octagon"}[n]


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


TRI = [(0, 90), (120, 90), (40, 0)]
SQ = R(0, 0, 85, 85)
RECT = R(0, 0, 150, 70)
TRAP = [(0, 80), (150, 80), (110, 0), (30, 0)]
RTRAP = [(0, 80), (150, 80), (80, 0), (0, 0)]
PENT = regular(5, 55, -90)
HOUSE5 = [(0, 45), (45, 0), (90, 45), (90, 110), (0, 110)]
HEX = regular(6, 55, 0)
HEX_L = [(0, 0), (45, 0), (45, 70), (110, 70), (110, 115), (0, 115)]
OCT = regular(8, 55, 22.5)
KITE = [(50, 0), (100, 40), (50, 130), (0, 40)]
NAMES = [(TRI, "triangle"), (SQ, "square"), (RECT, "rectangle"), (TRAP, "trapezium"), (RTRAP, "trapezium"),
         (PENT, "pentagon"), (HOUSE5, "pentagon"), (HEX, "hexagon"), (HEX_L, "hexagon"), (OCT, "octagon"),
         (KITE, "quadrilateral")]
for _p, _k in NAMES:
    assert classify(_p) == _k, (_k, classify(_p))
assert right_angles(HOUSE5) == 3 and right_angles(RTRAP) == 2 and right_angles(HEX_L) == 5 and right_angles(RECT) == 4


# ------------------------------------------------------------ composite 2-D shapes
def composite(parts, outline, label=None):
    """parts: list of (pts, kind). The parts must fill the outline exactly."""
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


PART_FILL = {"triangle": BASE, "square": FILL, "rectangle": SIDE, "trapezium": TOP3}


def comp_cv(c, k=1.0):
    cv = Canvas()
    for pts, kind in c["parts"]:
        cv.poly(scaled(pts, k), PART_FILL[kind])
    return cv


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
C_HEX2 = composite([(_hx[0:4], "trapezium"), (_hx[3:6] + [_hx[0]], "trapezium")], _hx)
C_TRAP3 = composite([([(0, _h), (_s, _h), (_s / 2, 0)], "triangle"), ([(_s / 2, 0), (_s, _h), (1.5 * _s, 0)], "triangle"),
                     ([(_s, _h), (2 * _s, _h), (1.5 * _s, 0)], "triangle")],
                    [(0, _h), (2 * _s, _h), (1.5 * _s, 0), (_s / 2, 0)])
C_BIGTRI = composite([([(_s / 2, _h), (1.5 * _s, _h), (_s, 0)], "triangle"),
                      ([(0, 2 * _h), (2 * _s, 2 * _h), (1.5 * _s, _h), (_s / 2, _h)], "trapezium")],
                     [(0, 2 * _h), (2 * _s, 2 * _h), (_s, 0)])
C_2SQ = composite([(R(0, 0, 60, 60), "square"), (R(60, 0, 120, 60), "square")], R(0, 0, 120, 60))
C_SQDIAG = composite([([(0, 0), (90, 0), (90, 90)], "triangle"), ([(0, 0), (90, 90), (0, 90)], "triangle")], R(0, 0, 90, 90))
C_L = composite([(R(0, 0, 40, 110), "rectangle"), (R(40, 70, 110, 110), "rectangle")],
                [(0, 0), (40, 0), (40, 70), (110, 70), (110, 110), (0, 110)])
C_BOAT = composite([([(0, 70), (140, 70), (115, 100), (25, 100)], "trapezium"), ([(70, 0), (70, 70), (125, 70)], "triangle")],
                   [(0, 70), (70, 70), (70, 0), (125, 70), (140, 70), (115, 100), (25, 100)])
C_ROCKET = composite([(R(30, 40, 70, 140), "rectangle"), ([(30, 40), (70, 40), (50, 0)], "triangle"),
                      ([(30, 105), (30, 140), (10, 140)], "triangle"), ([(70, 105), (90, 140), (70, 140)], "triangle")],
                     [(50, 0), (70, 40), (70, 105), (90, 140), (10, 140), (30, 105), (30, 40)])
C_LONGHEX = composite([(R(40, 0, 140, 60), "rectangle"), ([(40, 0), (40, 60), (0, 30)], "triangle"),
                       ([(140, 0), (180, 30), (140, 60)], "triangle")],
                      [(0, 30), (40, 0), (140, 0), (180, 30), (140, 60), (40, 60)])
C_RTRAP = composite([(R(0, 40, 100, 100), "rectangle"), ([(0, 0), (100, 40), (0, 40)], "triangle")],
                    [(0, 0), (100, 40), (100, 100), (0, 100)])
C_GRID = composite([(R(30 * i, 30 * j, 30 * i + 30, 30 * j + 30), "square") for i in range(4) for j in range(2)], R(0, 0, 120, 60))
assert sides(C_HOUSE["outline"]) == 5 and classify(C_HOUSE["outline"]) == "pentagon"
assert classify(C_LONGHEX["outline"]) == "hexagon" and classify(C_RTRAP["outline"]) == "trapezium"
assert classify(C_2SQ["outline"]) == "rectangle" and classify(C_BIGTRI["outline"]) == "triangle"
assert classify(C_TRAP3["outline"]) == "trapezium" and classify(C_HEX2["outline"]) == "hexagon"


def parts_count(c):
    out = {}
    for _, k in c["parts"]:
        out[k] = out.get(k, 0) + 1
    return out


# ------------------------------------------------------------ hidden shapes in line drawings (counted by brute force)
def _on_seg(p, a, b):
    cr = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
    if cr != 0:
        return False
    return min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def _points(segs):
    pts = set()
    for a, b in segs:
        pts.add(a)
        pts.add(b)
    for (a, b), (c, d) in itertools.combinations(segs, 2):
        den = (b[0] - a[0]) * (d[1] - c[1]) - (b[1] - a[1]) * (d[0] - c[0])
        if den == 0:
            continue
        t = Fraction((c[0] - a[0]) * (d[1] - c[1]) - (c[1] - a[1]) * (d[0] - c[0]), den)
        p = (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
        if _on_seg(p, a, b) and _on_seg(p, c, d):
            pts.add(p)
    return [(Fraction(x), Fraction(y)) for x, y in pts]


def _joined(p, q, segs):
    return any(_on_seg(p, a, b) and _on_seg(q, a, b) for a, b in segs)


def count_triangles(segs):
    segs = [((Fraction(a[0]), Fraction(a[1])), (Fraction(b[0]), Fraction(b[1]))) for a, b in segs]
    pts = _points(segs)
    n = 0
    for p, q, r in itertools.combinations(pts, 3):
        if (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0]) == 0:
            continue
        if _joined(p, q, segs) and _joined(q, r, segs) and _joined(p, r, segs):
            n += 1
    return n


def count_rects(segs, squares_only=False):
    """Axis-aligned rectangles (squares included) whose 4 sides are all drawn."""
    segs = [((Fraction(a[0]), Fraction(a[1])), (Fraction(b[0]), Fraction(b[1]))) for a, b in segs]
    pts = _points(segs)
    xs, ys = sorted({p[0] for p in pts}), sorted({p[1] for p in pts})
    n = 0
    for x0, x1 in itertools.combinations(xs, 2):
        for y0, y1 in itertools.combinations(ys, 2):
            c = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
            if all(_joined(c[i], c[(i + 1) % 4], segs) for i in range(4)):
                if not squares_only or x1 - x0 == y1 - y0:
                    n += 1
    return n


def poly_segs(pts):
    return [(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts))]


def segs_cv(segs, outline):
    cv = Canvas()
    cv.poly(outline, FILL)
    for a, b in segs:
        cv.line(a, b, sw=2.4)
    return cv


H1 = {"out": [(0, 100), (120, 100), (60, 0)], "in": [((60, 0), (40, 100))]}
H2 = {"out": [(0, 100), (120, 100), (60, 0)], "in": [((60, 0), (30, 100)), ((60, 0), (84, 100))]}
H4 = {"out": [(0, 104), (120, 104), (60, 0)], "in": [((30, 52), (90, 52)), ((30, 52), (60, 104)), ((90, 52), (60, 104))]}
HX = {"out": R(0, 0, 100, 100), "in": [((0, 0), (100, 100)), ((100, 0), (0, 100))]}
HR2 = {"out": R(0, 0, 120, 60), "in": [((60, 0), (60, 60))]}
HR3 = {"out": R(0, 0, 150, 50), "in": [((50, 0), (50, 50)), ((100, 0), (100, 50))]}
HG = {"out": R(0, 0, 100, 100), "in": [((50, 0), (50, 100)), ((0, 50), (100, 50))]}
for _f in (H1, H2, H4, HX, HR2, HR3, HG):
    _f["segs"] = poly_segs(_f["out"]) + _f["in"]
assert count_triangles(H1["segs"]) == 3 and count_triangles(H2["segs"]) == 6
assert count_triangles(H4["segs"]) == 5 and count_triangles(HX["segs"]) == 8
assert count_rects(HR2["segs"]) == 3 and count_rects(HR3["segs"]) == 6 and count_rects(HG["segs"], True) == 5
assert count_triangles(HR3["segs"]) == 0 and count_rects(HX["segs"]) == 1


def hidden_cv(h):
    return segs_cv(h["in"], h["out"])


# ------------------------------------------------------------ pictures made of shapes (scenes)
def P(pts, kind):
    assert classify(pts) == kind, (kind, classify(pts))
    return ("poly", pts, kind)


def C(c, r):
    return ("circle", c, r, "circle")


SCENE_FILL = {"triangle": BASE, "square": FILL, "rectangle": SIDE, "trapezium": TOP3, "circle": YEL}
ROBOT = [P([(50, 10), (70, 10), (60, -10)], "triangle"), P(R(30, 10, 90, 70), "square"),
         P([(30, 25), (30, 55), (17, 40)], "triangle"), P([(90, 25), (103, 40), (90, 55)], "triangle"),
         C((48, 32), 7), C((72, 32), 7), P(R(45, 50, 75, 59), "rectangle"),
         P(R(20, 76, 100, 150), "rectangle"), C((60, 98), 7), C((60, 124), 7),
         P(R(0, 82, 15, 132), "rectangle"), P(R(105, 82, 120, 132), "rectangle"),
         P(R(32, 155, 52, 200), "rectangle"), P(R(68, 155, 88, 200), "rectangle")]
TRAIN = [P(R(0, 30, 80, 80), "rectangle"), P(R(12, 40, 32, 60), "square"), P(R(48, 40, 68, 60), "square"),
         P(R(80, 66, 90, 72), "rectangle"), P(R(90, 40, 180, 80), "rectangle"), P(R(140, 0, 180, 40), "square"),
         P(R(102, 14, 116, 40), "rectangle"), P([(180, 60), (198, 80), (180, 80)], "triangle"),
         C((20, 88), 10), C((60, 88), 10), C((110, 88), 10), C((138, 88), 10), C((166, 88), 10)]
HOUSE_SCENE = [P(R(20, 60, 100, 140), "square"), P([(10, 60), (60, 15), (110, 60)], "triangle"),
               P(R(52, 100, 68, 140), "rectangle"), P(R(30, 74, 46, 90), "square"), P(R(74, 74, 90, 90), "square"),
               C((160, 28), 16), P([(125, 100), (150, 52), (175, 100)], "triangle"), P(R(144, 100, 156, 140), "rectangle")]
BOAT_SCENE = [P([(76, 4), (100, 11), (76, 18)], "triangle"), P(R(76, 4, 84, 90), "rectangle"),
              P([(70, 22), (70, 85), (22, 85)], "triangle"), P([(90, 26), (138, 85), (90, 85)], "triangle"),
              P([(0, 90), (160, 90), (135, 122), (25, 122)], "trapezium"),
              C((50, 106), 6), C((80, 106), 6), C((110, 106), 6)]


def scene_count(sc):
    out = {}
    for it in sc:
        out[it[-1]] = out.get(it[-1], 0) + 1
    return out


def scene_cv(sc):
    cv = Canvas()
    for it in sc:
        if it[0] == "poly":
            cv.poly(it[1], SCENE_FILL[it[2]], sw=2)
        else:
            cv.circle(it[1], it[2], fill=SCENE_FILL["circle"], sw=2)
    return cv


assert scene_count(ROBOT) == {"triangle": 3, "square": 1, "circle": 4, "rectangle": 6}
assert scene_count(TRAIN) == {"rectangle": 4, "square": 3, "triangle": 1, "circle": 5}
assert scene_count(HOUSE_SCENE) == {"square": 3, "triangle": 2, "rectangle": 2, "circle": 1}
assert scene_count(BOAT_SCENE) == {"triangle": 3, "rectangle": 1, "trapezium": 1, "circle": 3}


# ------------------------------------------------------------ 3-D objects
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

    def seen_faces(self, yaw, pitch):
        return sum(self.view(yaw, pitch)[1])

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


def box(L, H, W, o=(0, 0, 0)):
    v = [(x, y, z) for x in (0, L) for y in (0, H) for z in (0, W)]
    idx = {p: i for i, p in enumerate(v)}
    g = lambda *ps: [idx[p] for p in ps]
    f = [g((0, 0, 0), (L, 0, 0), (L, H, 0), (0, H, 0)), g((0, 0, W), (L, 0, W), (L, H, W), (0, H, W)),
         g((0, 0, 0), (0, 0, W), (0, H, W), (0, H, 0)), g((L, 0, 0), (L, 0, W), (L, H, W), (L, H, 0)),
         g((0, 0, 0), (L, 0, 0), (L, 0, W), (0, 0, W)), g((0, H, 0), (L, H, 0), (L, H, W), (0, H, W))]
    return Solid([(x + o[0], y + o[1], z + o[2]) for x, y, z in v], f)


def prism_lying(w, h, D, o=(0, 0, 0)):
    """Triangular prism lying on a rectangle face: triangle ends in the y-z plane, length D along x."""
    tri = [(0, 0), (w, 0), (w / 2, h)]          # (z, y)
    v = [(0, y, z) for z, y in tri] + [(D, y, z) for z, y in tri]
    f = [[0, 1, 2], [3, 4, 5]] + [[i, (i + 1) % 3, 3 + (i + 1) % 3, 3 + i] for i in range(3)]
    return Solid([(x + o[0], y + o[1], z + o[2]) for x, y, z in v], f)


def pyramid(s, h, o=(0, 0, 0)):
    v = [(0, 0, 0), (s, 0, 0), (s, 0, s), (0, 0, s), (s / 2, h, s / 2)]
    f = [[0, 1, 2, 3]] + [[i, (i + 1) % 4, 4] for i in range(4)]
    return Solid([(x + o[0], y + o[1], z + o[2]) for x, y, z in v], f)


assert tuple(box(1, 1, 1).count.values()) == (6, 12, 8)
assert tuple(prism_lying(1, 1, 2).count.values()) == (5, 9, 6)
assert tuple(pyramid(1, 1).count.values()) == (5, 8, 5)

TENT = (lambda: prism_lying(1.3, 1.0, 1.9), 30, 20)
TENT_SEEN = TENT[0]().seen_faces(TENT[1], TENT[2])
assert TENT_SEEN == 2, TENT_SEEN


def tent_cv(k=50):
    f, y, p = TENT
    return f().draw(Canvas(), k, y, p)


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


def ellipse(cx, cy, rx, ry, a0, a1, n=40):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def _rot90(pts, on):
    return [(-y, x) for x, y in pts] if on else pts


def cyl_cone_cv(rx=30, ry=9, h=70, hc=48, lying=False, s=1.0):
    """A cylinder with a cone on top (a silo, a rocket, a crayon). The cone sides are true tangents to the rim."""
    rx, ry, h, hc = rx * s, ry * s, h * s, hc * s
    Rt = lambda p: _rot90(p, lying)
    cv = Canvas()
    cv.poly(Rt(ellipse(0, 0, rx, ry, 180, 360) + ellipse(0, h, rx, ry, 0, 180)), FILL, 0.0)
    cv.pline(Rt([(-rx, 0), (-rx, h)]))
    cv.pline(Rt([(rx, 0), (rx, h)]))
    cv.pline(Rt(ellipse(0, h, rx, ry, 0, 180)))
    cv.pline(Rt(ellipse(0, h, rx, ry, 180, 360)), dashed=True, sw=1.6)
    d = math.degrees(math.asin(ry / hc))           # tangent points from the tip (0, -hc)
    arc = ellipse(0, 0, rx, ry, -d, 180 + d, 60)
    cv.poly(Rt([(0, -hc)] + arc), BASE, 0.0)
    cv.pline(Rt([arc[-1], (0, -hc), arc[0]]))
    cv.pline(Rt(arc))
    return cv


def icecream_cv(rx=32, ry=9, h=78, r=33, s=1.0):
    rx, ry, h, r = rx * s, ry * s, h * s, r * s
    cv = Canvas()
    d = math.degrees(math.asin(ry / h))            # tangent points from the tip (0, h)
    arc = ellipse(0, 0, rx, ry, d, 180 - d, 40)
    cv.poly([(0, h)] + arc[::-1], BASE, 0.0)
    cv.pline([arc[0], (0, h), arc[-1]])
    cv.poly(ellipse(0, 0, rx, ry, 0, 360)[:-1], TOP3, 2.4)
    cv.circle((0, -r * 0.55), r, fill="#f4c7c3", sw=2.4)
    return cv


def cube_stack(a, b, c, k=26, yaw=32, pitch=24):
    """Solid block of a x c x b unit cubes (a long, c high, b deep). Only the outside faces you can see are drawn."""
    cv = Canvas()
    Pj = lambda p: (rot_view(p, yaw, pitch)[0] * k, -rot_view(p, yaw, pitch)[1] * k)
    faces = []        # (normal, list of unit squares)
    dims = (a, c, b)
    for ax in range(3):
        for side in (0, 1):
            nrm = [0, 0, 0]
            nrm[ax] = 1 if side else -1
            if rot_view(nrm, yaw, pitch)[2] >= -1e-6:
                continue
            o1, o2 = [i for i in range(3) if i != ax]
            for i in range(dims[o1]):
                for j in range(dims[o2]):
                    sq = []
                    for di, dj in [(0, 0), (1, 0), (1, 1), (0, 1)]:
                        p = [0, 0, 0]
                        p[ax] = dims[ax] if side else 0
                        p[o1], p[o2] = i + di, j + dj
                        sq.append(Pj(p))
                    faces.append((ax, sq))
    assert len({f[0] for f in faces}) == 3
    for ax, sq in faces:
        cv.poly(sq, [SIDE, TOP3, FILL][ax], 2)
    return cv


def stack_seen(a, b, c):
    return a * b * c - (a - 1) * (b - 1) * (c - 1)


# ------------------------------------------------------------ set 1: name 2-D shapes
WRONG_NAME = {"triangle": ["pyramid", "trapezium", "pentagon"], "square": ["cube", "trapezium", "pentagon"],
              "rectangle": ["square", "rectangular prism", "trapezium"], "trapezium": ["rectangle", "pentagon", "triangle"],
              "pentagon": ["hexagon", "octagon", "square"], "hexagon": ["octagon", "pentagon", "rectangle"],
              "octagon": ["hexagon", "pentagon", "circle"]}


def set_name(rnd, pos):
    its = []
    for pts, kind, lead, extra in [
            (TRI, "triangle", "What is the name of this shape?", "It has 3 straight sides and 3 corners, so it is a triangle. A pyramid is a 3-D object."),
            (SQ, "square", "What is the best name for this shape?", "4 equal sides and 4 right angles: a square. A cube is a 3-D object."),
            (RECT, "rectangle", "What is the best name for this shape?", "4 sides and 4 right angles, with 2 long and 2 short sides: a rectangle."),
            (TRAP, "trapezium", "What is the name of this shape?", "4 sides, and only the top and bottom sides are parallel (they go the same way): a trapezium."),
            (PENT, "pentagon", "What is the name of this shape?", "Count the sides: 5. A shape with 5 sides is a pentagon."),
            (HOUSE5, "pentagon", "This shape looks like a house. What is its name?", "Count the sides: 5. Any shape with 5 straight sides is a pentagon, even if the sides are not equal."),
            (HEX, "hexagon", "What is the name of this shape?", "Count the sides: 6. A shape with 6 sides is a hexagon."),
            (HEX_L, "hexagon", "What is the name of this L shape?", "Count the sides: 6. Any shape with 6 straight sides is a hexagon, even an L shape."),
            (OCT, "octagon", "What is the name of this shape?", "Count the sides: 8. A shape with 8 sides is an octagon, like a stop sign."),
    ]:
        assert classify(pts) == kind
        wrong = WRONG_NAME[kind]
        if pts is HEX_L:
            wrong = ["rectangle", "octagon", "pentagon"]
        its.append(mcq(fig(shape_cv(pts).svg("a 2-D shape")) + lead, kind, wrong, extra))
    its.append(mcq("How many sides does an octagon have?", 8, [6, 10, 5],
                   "An octagon has 8 sides and 8 corners. Think of an octopus with 8 arms. A hexagon has 6."))
    its.append(mcq("How many corners does a pentagon have?", 5, [6, 4, 8],
                   "A pentagon has 5 sides and 5 corners. Every shape with straight sides has as many corners as sides."))
    its.append(mcq("A shape has 6 straight sides. What is it?", "a hexagon", ["a pentagon", "an octagon", "a quadrilateral"],
                   "6 sides: a hexagon. 5 sides is a pentagon and 8 sides is an octagon."))
    its.append(mcq("Which shape is a quadrilateral?", "a trapezium", ["a triangle", "a pentagon", "a hexagon"],
                   "A quadrilateral is any shape with 4 straight sides. A trapezium has 4 sides."))
    for pts, ans, wrong, e in [
            (HOUSE5, 3, [2, 5, 4], "The 2 bottom corners are right angles, and so is the corner at the top. The other 2 corners are bigger than a right angle."),
            (RTRAP, 2, [1, 4, 0], "The 2 corners on the left are right angles (square corners). The 2 corners on the right are not."),
            (HEX_L, 5, [6, 4, 1], "5 corners are right angles. The inside corner of the L is bigger than a right angle (3 right angles), so do not count it."),
    ]:
        assert right_angles(pts) == ans
        its.append(mcq(fig(shape_cv(pts).svg("a 2-D shape")) + "How many right angles does this shape have?", ans, wrong, e))
    its.append(mcq("Is a square a rectangle?", "Yes: it has 4 sides and 4 right angles.",
                   ["No: a rectangle must have 2 long and 2 short sides.", "No: a square has no right angles.", "Only when it is turned."],
                   "A rectangle has 4 sides and 4 right angles. A square has these too, so a square is a special rectangle with all sides equal."))
    its.append(mcq("Which shape has no straight sides and no corners?", "a circle", ["an octagon", "a hexagon", "a trapezium"],
                   "A circle is one curved line. An octagon has 8 straight sides and 8 corners."))
    for q, right, others, why in [
            ("Which shape is a trapezium?", TRAP, [RECT, PENT, TRI], "is a trapezium: 4 sides and only 1 pair of parallel sides."),
            ("Which shape is a hexagon?", HEX_L, [HOUSE5, OCT, TRAP], "has 6 sides, so it is a hexagon. A hexagon does not have to look like a honeycomb."),
    ]:
        p = pos.next()
        cells = [shape_cv(s, min(0.62, fit(s))) for s in others]
        cells.insert(p, shape_cv(right, min(0.62, fit(right))))
        its.append(mcq_fixed(fig(grid_svg(cells, "four 2-D shapes labelled A to D")) + q, list("ABCD"), "ABCD"[p],
                             "%s %s" % ("ABCD"[p], why)))
    assert len(its) == 20, len(its)
    return {"title": "Name 2-D shapes: sides, corners and right angles", "items": its}


# ------------------------------------------------------------ set 2: which shapes make this shape?
def set_make(rnd, pos):
    its = []
    q2 = lambda c, t: fig(comp_cv(c).svg("a composite shape made of smaller shapes")) + t

    def add(c, t, right, wrong, e, want=None):
        if want is not None:
            assert parts_count(c) == want, (parts_count(c), want)
        its.append(mcq(q2(c, t), right, wrong, e))

    add(C_HOUSE, "Which two shapes make this house?", "a square and a triangle",
        ["a pentagon and a triangle", "a square and 2 triangles", "a rectangle and a circle"],
        "The walls are a square (4 equal sides) and the roof is a triangle (3 sides).", {"square": 1, "triangle": 1})
    add(C_HOUSE, "How many sides does the outline of the whole house have?", 5, [7, 6, 4],
        "Go round the outside: 2 walls, the floor and 2 roof sides = 5 sides, so the outline is a pentagon. "
        "Do not add 4 + 3 = 7: the line where the roof meets the walls is inside.")
    add(C_ARROW, "Which two shapes make this arrow?", "a rectangle and a triangle",
        ["2 triangles", "a pentagon and a rectangle", "a square and a circle"],
        "The long part is a rectangle and the point is a triangle.", {"rectangle": 1, "triangle": 1})
    add(C_TREE, "Which two shapes make this tree?", "a triangle and a rectangle",
        ["a triangle and a trapezium", "2 triangles", "a pentagon and a square"],
        "The leaves are a triangle and the trunk is a thin rectangle.", {"triangle": 1, "rectangle": 1})
    add(C_HEX6, "How many triangles make this hexagon?", 6, [3, 4, 8],
        "Count the triangles round the centre: 6. A hexagon has 6 sides, and each side belongs to one triangle.", {"triangle": 6})
    add(C_HEX2, "Which shapes make this hexagon?", "2 trapeziums", ["2 triangles", "2 rectangles", "2 pentagons"],
        "The line cuts the hexagon into 2 pieces. Each piece has 4 sides and 1 pair of parallel sides, so each is a trapezium.",
        {"trapezium": 2})
    add(C_TRAP3, "Which shapes make this trapezium?", "3 triangles", ["2 triangles", "4 triangles", "3 squares"],
        "Count the pieces: 3 triangles. Pattern blocks work like this: 3 triangles make 1 trapezium.", {"triangle": 3})
    add(C_BIGTRI, "Which two shapes make this big triangle?", "a trapezium and a triangle",
        ["2 triangles", "a rectangle and a triangle", "a square and a triangle"],
        "The top piece is a small triangle. The bottom piece has 4 sides and 1 pair of parallel sides: a trapezium.",
        {"triangle": 1, "trapezium": 1})
    add(C_2SQ, "Which shapes make this rectangle?", "2 squares", ["4 squares", "2 triangles", "a square and a triangle"],
        "The line in the middle cuts the rectangle into 2 equal squares.", {"square": 2})
    add(C_SQDIAG, "Which shapes make this square?", "2 triangles", ["2 rectangles", "4 triangles", "2 squares"],
        "The line goes from one corner to the opposite corner. It cuts the square into 2 triangles.", {"triangle": 2})
    add(C_L, "Which shapes make this L shape?", "2 rectangles", ["3 squares", "a rectangle and a triangle", "2 squares"],
        "A tall rectangle and a flat rectangle make the L. Neither piece has 4 equal sides, so they are not squares.",
        {"rectangle": 2})
    add(C_BOAT, "Which two shapes make this boat?", "a trapezium and a triangle",
        ["a rectangle and a triangle", "2 triangles", "a trapezium and a square"],
        "The sail is a triangle. The hull has 4 sides, with the top longer than the bottom: a trapezium.",
        {"trapezium": 1, "triangle": 1})
    add(C_ROCKET, "Which shapes make this rocket?", "1 rectangle and 3 triangles",
        ["1 rectangle and 2 triangles", "1 square and 3 triangles", "2 rectangles and 3 triangles"],
        "The body is a rectangle. The nose is a triangle and there is a triangle fin on each side: 1 + 2 = 3 triangles.",
        {"rectangle": 1, "triangle": 3})
    add(C_LONGHEX, "A rectangle and 2 triangles make this shape. What is the name of the whole outline?", "a hexagon",
        ["a rectangle", "an octagon", "a pentagon"],
        "Go round the outside and count the sides: 6. So the outline is a hexagon.")
    add(C_RTRAP, "A rectangle and a triangle make this shape. What is the name of the whole outline?", "a trapezium",
        ["a pentagon", "a rectangle", "a triangle"],
        "The sloping side of the triangle and the side of the rectangle go round the outside. The outline has 4 sides and 1 pair of parallel sides: a trapezium.")
    add(C_GRID, "This rectangle is made from squares of the same size. How many squares?", 8, [6, 4, 12],
        "There are 2 rows of 4 squares: 4 + 4 = 8. Adding the rows and columns (4 + 2 = 6) does not count the squares.",
        {"square": 8})
    its.append(mcq("You join 2 squares of the same size along one side. Which shape do you make?", "a rectangle",
                   ["a bigger square", "an octagon", "a hexagon"],
                   "2 squares side by side make a rectangle twice as long as it is wide. It has 4 sides, not 4 + 4 = 8."))
    its.append(mcq("Two right-angled triangles are the same. You join them along their longest sides. Which shape can you make?",
                   "a rectangle", ["a pentagon", "a hexagon", "an octagon"],
                   "Put the triangles together like the two halves of a sandwich cut corner to corner: they make a rectangle with 4 right angles."))
    its.append(mcq("Mei cuts a rectangle from one corner to the opposite corner. What two shapes does she get?", "2 triangles",
                   ["2 rectangles", "2 squares", "a triangle and a trapezium"],
                   "A cut from corner to corner makes 2 triangles. A cut across the middle would make 2 rectangles."))
    p = pos.next()
    others = [C_ARROW, C_BOAT, C_SQDIAG]
    cells = [comp_cv(c, min(0.6, fit(c["outline"]))) for c in others]
    cells.insert(p, comp_cv(C_HOUSE, min(0.6, fit(C_HOUSE["outline"]))))
    its.append(mcq_fixed(fig(grid_svg(cells, "four composite shapes labelled A to D")) + "Which shape is made from a square and a triangle?",
                         list("ABCD"), "ABCD"[p],
                         "%s is a square with a triangle on top. The others are a rectangle and a triangle, a trapezium and a triangle, and 2 triangles."
                         % "ABCD"[p]))
    assert len(its) == 20, len(its)
    return {"title": "Which shapes make this composite shape?", "items": its}


# ------------------------------------------------------------ set 3: count shapes in a picture
def set_count(rnd, P_):
    its = []
    sc = lambda s: fig(scene_cv(s).svg("a picture made of shapes"))
    rob, tr, ho, bo = scene_count(ROBOT), scene_count(TRAIN), scene_count(HOUSE_SCENE), scene_count(BOAT_SCENE)
    rect_tip = " (A square is a rectangle too.)"
    its.append(mcq(sc(ROBOT) + "How many circles are in this robot?", rob["circle"], [2, 5, 3],
                   "2 eyes and 2 buttons: 2 + 2 = 4 circles."))
    its.append(mcq(sc(ROBOT) + "How many triangles are in this robot?", rob["triangle"], [1, 2, 4],
                   "1 on top of the head and 1 ear on each side: 1 + 2 = 3 triangles."))
    its.append(mcq(sc(ROBOT) + "How many rectangles are in this robot?" + rect_tip, rob["rectangle"] + rob["square"], [6, 4, 8],
                   "Mouth, body, 2 arms and 2 legs are 6 rectangles. The square head is a rectangle too: 6 + 1 = 7."))
    tot = sum(rob.values())
    its.append(mcq(sc(ROBOT) + "How many shapes are in this robot altogether?", tot, [tot - 5, tot - 1, tot + 1],
                   "Count every shape: 3 triangles + 1 square + 6 rectangles + 4 circles = %d. "
                   "Do not forget the eyes, mouth and buttons drawn on top of other shapes." % tot))
    its.append(mcq(sc(TRAIN) + "How many circles are in this train?", tr["circle"], [3, 2, 6],
                   "2 wheels on the carriage and 3 wheels on the engine: 2 + 3 = 5 circles."))
    its.append(mcq(sc(TRAIN) + "How many squares are in this train?", tr["square"], [2, 1, 4],
                   "2 square windows on the carriage and the square cabin on the engine: 2 + 1 = 3 squares."))
    its.append(mcq(sc(TRAIN) + "How many rectangles are in this train?" + rect_tip, tr["rectangle"] + tr["square"], [4, 3, 8],
                   "4 rectangles (carriage, engine, chimney, the join between them) and 3 squares, which are rectangles too: 4 + 3 = 7."))
    its.append(mcq(sc(HOUSE_SCENE) + "How many squares are in this picture?", ho["square"], [2, 1, 5],
                   "The 2 windows are squares, and so are the walls of the house: 2 + 1 = 3 squares."))
    its.append(mcq(sc(HOUSE_SCENE) + "How many rectangles are in this picture?" + rect_tip, ho["rectangle"] + ho["square"], [2, 3, 8],
                   "The door and the tree trunk are rectangles (2). The 3 squares are rectangles too: 2 + 3 = 5."))
    its.append(mcq(sc(HOUSE_SCENE) + "How many shapes are in this picture altogether?", sum(ho.values()), [7, 6, 9],
                   "3 squares + 2 rectangles + 2 triangles + 1 circle = 8 shapes."))
    its.append(mcq(sc(BOAT_SCENE) + "How many triangles are in this boat?", bo["triangle"], [2, 4, 1],
                   "2 sails and the little flag at the top of the mast: 2 + 1 = 3 triangles."))
    its.append(mcq(sc(BOAT_SCENE) + "What shape is the hull (the bottom part) of this boat?", "a trapezium",
                   ["a rectangle", "a triangle", "a hexagon"],
                   "The hull has 4 sides. The top and bottom are parallel but not the same length, so it is a trapezium."))
    hq = lambda h, t: fig(hidden_cv(h).svg("a shape divided by lines")) + t
    its.append(mcq(hq(H1, "How many triangles can you find in this picture?"), count_triangles(H1["segs"]), [2, 4, 1],
                   "There are 2 small triangles, and together they make 1 big triangle: 2 + 1 = 3."))
    its.append(mcq(hq(H2, "How many triangles can you find in this picture?"), count_triangles(H2["segs"]), [3, 4, 5],
                   "3 small triangles, 2 triangles made of 2 small ones next to each other, and 1 big one: 3 + 2 + 1 = 6."))
    its.append(mcq(hq(H4, "How many triangles can you find in this picture?"), count_triangles(H4["segs"]), [4, 6, 3],
                   "4 small triangles, and the big triangle made of all 4: 4 + 1 = 5."))
    its.append(mcq(hq(HX, "How many triangles can you find in this square?"), count_triangles(HX["segs"]), [4, 6, 2],
                   "4 small triangles meet in the middle. Each diagonal also cuts the square into 2 big triangles: 2 + 2 = 4 more. 4 + 4 = 8."))
    n, he, his = P_.next()
    its.append(mcq(hq(H4, "%s counts the triangles in this picture and gets 4. What did %s forget?" % (n, he)),
                   "the big triangle made by all 4", ["the triangles at the back", "a square in the middle", "nothing: 4 is right"],
                   "There are 4 small triangles, but all 4 together make 1 big triangle too. 4 + 1 = 5."))
    its.append(mcq(hq(HR2, "How many rectangles can you find?" + rect_tip), count_rects(HR2["segs"]), [2, 1, 4],
                   "There are 2 squares, and they make 1 big rectangle together: 2 + 1 = 3."))
    its.append(mcq(hq(HR3, "How many rectangles can you find?" + rect_tip), count_rects(HR3["segs"]), [3, 4, 5],
                   "3 small ones, 2 made of 2 small ones next to each other, and 1 big one: 3 + 2 + 1 = 6."))
    its.append(mcq(hq(HG, "How many squares can you find?"), count_rects(HG["segs"], True), [4, 6, 9],
                   "4 small squares, and the big square around all of them: 4 + 1 = 5."))
    assert len(its) == 20, len(its)
    return {"title": "Count the shapes in a picture", "items": its}


# ------------------------------------------------------------ set 4: objects in the environment
def set_objects(rnd, P_):
    its = []
    for cv, name, lead, right, wrong, e in [
            (cyl_cone_cv(), "a silo", "This farm silo is made of two objects. Which two?", "a cylinder and a cone",
             ["a rectangle and a triangle", "a cylinder and a square-based pyramid", "a cone and a sphere"],
             "The tall part has 2 circle ends and a curved side: a cylinder. The roof has a circle base and a point: a cone. "
             "Rectangles and triangles are flat 2-D shapes."),
            (icecream_cv(), "an ice-cream cone", "This ice-cream is made of two objects. Which two?", "a cone and a sphere",
             ["a triangle and a circle", "a cylinder and a sphere", "a square-based pyramid and a sphere"],
             "The scoop is round like a ball: a sphere. The cone comes to a point and has a circle at the top: a cone."),
            (house3d_cv(), "a house", "This model house is made of two objects. Which two?", "a rectangular prism and a triangular prism",
             ["a rectangular prism and a square-based pyramid", "a rectangle and a triangle", "a cube and a cone"],
             "The bottom has 6 rectangle faces: a rectangular prism. The roof has a triangle at each end and does not come to a point: a triangular prism."),
            (tower_cv(), "a tower", "This tower is made of two objects. Which two?", "a cube and a square-based pyramid",
             ["a cube and a triangular prism", "a square and a triangle", "a cube and a cone"],
             "The bottom has 6 square faces: a cube. The top has 4 triangle faces that meet at a point: a square-based pyramid. A cone has a circle base."),
            (cyl_cone_cv(15, 5, 115, 32, lying=True), "a crayon", "This crayon is made of two objects. Which two?", "a cylinder and a cone",
             ["a rectangle and a triangle", "a triangular prism and a cone", "a cylinder and a sphere"],
             "The long part is a cylinder and the tip is a cone. A rectangle and a triangle are only the flat outline."),
    ]:
        its.append(mcq(fig(cv.svg(name)) + lead, right, wrong, e))
    its.append(mcq(fig(tent_cv().svg("a tent")) + "This tent is shaped like which object?", TP, [SP, "triangle", RP],
                   "It has a triangle at each end joined by rectangles, and it does not come to a point: a triangular prism."))
    f, y, p = TENT
    its.append(mcq(fig(tent_cv().svg("a tent")) + "How many faces does this tent have? Count the floor too.", 5, [TENT_SEEN, 6, 4],
                   "You can see only %d faces. A tent has 2 triangle ends and 3 rectangles (2 sloping sides and the floor): 2 + 3 = 5." % TENT_SEEN))
    for a, b, c in [(2, 2, 2), (3, 2, 2), (3, 3, 2)]:
        tot, vis = a * b * c, stack_seen(a, b, c)
        sq = a * b + b * c + a * c
        layer = a * b
        e = ("Each layer has %d × %d = %d cubes and there are %d layers: %s = %d. You can see only %d of them; the other %d %s hidden behind the others."
             % (a, b, layer, c, " + ".join([str(layer)] * c), tot, vis, tot - vis, "is" if tot - vis == 1 else "are"))
        its.append(mcq(fig(cube_stack(a, b, c).svg("a solid stack of cubes")) + "This is a solid stack of cubes with no gaps. How many cubes are in it?",
                       tot, [vis, sq, layer], e))
    for obj, kind, wrong, e in [
            ("a shipping container", RP, ["rectangle", CUBE, TP], "It has 6 rectangle faces and is longer than it is tall: a rectangular prism."),
            ("a basketball", SPH, ["circle", CYL, CONE], "It is round all over: a sphere. A circle is a flat 2-D shape."),
            ("a round rainwater tank on a farm", CYL, ["circle", RP, CONE], "It has a circle at the top and bottom and a curved side: a cylinder."),
            ("a dice", CUBE, ["square", SP, TP], "It has 6 square faces of the same size: a cube."),
            ("a traffic cone", CONE, ["triangle", SP, CYL], "It has a circle base, a curved surface and a point: a cone. A pyramid has flat triangle faces."),
            ("a long chocolate box with a triangle at each end", TP, ["triangle", SP, RP], "2 triangle ends joined by 3 rectangles: a triangular prism."),
            ("a roof made of 4 triangles that meet at a point on a square base", SP, [TP, CONE, "triangle"],
             "A square base and 4 triangle faces that meet at a point: a square-based pyramid."),
    ]:
        its.append(mcq("%s is closest to which object?" % (obj[0].upper() + obj[1:]), kind, wrong, e))
    n, he, his = P_.next()
    its.append(mcq("%s says a tent with a triangle at each end is a pyramid. Why is %s wrong?" % (n, he),
                   "It does not come to a point, so it is a prism.",
                   ["It has no triangle faces.", "It has a curved surface.", "A tent is a 2-D shape."],
                   "A pyramid comes to a point. A tent like this has the same triangle at both ends, so it is a triangular prism."))
    its.append(mcq("A water tower is a sphere on top of a tall cylinder. You draw it flat, as you see it from the front. Which 2-D shapes do you draw?",
                   "a circle and a rectangle", ["a sphere and a cylinder", "a circle and a triangle", "2 circles"],
                   "From the front, a sphere looks like a circle and a standing cylinder looks like a rectangle. "
                   "Sphere and cylinder are the names of the 3-D objects, not the flat drawing."))
    its.append(mcq("Which of these is made of a cylinder with a cone on top?", "a rocket", ["a cricket ball", "a dice", "a tissue box"],
                   "A rocket has a cylinder body and a cone nose. A cricket ball is a sphere, a dice is a cube and a tissue box is a rectangular prism."))
    assert len(its) == 20, len(its)
    return {"title": "3-D objects in the world around us", "items": its}


# ------------------------------------------------------------ set 5: approximate real things (word problems)
def set_problems(rnd, P_):
    its = []
    its.append(mcq("A stop sign is closest to which shape?", "an octagon", ["a hexagon", "a circle", "a pentagon"],
                   "A stop sign has 8 straight sides, so it is an octagon. Count carefully: 6 sides would be a hexagon."))
    its.append(mcq("A give way sign in Australia is closest to which shape?", "a triangle", ["a square", "a trapezium", "a pentagon"],
                   "A give way sign has 3 sides (it points down), so it is a triangle."))
    its.append(mcq("The Australian 50c coin has 12 straight sides. How many corners does it have?", 12, [6, 24, 11],
                   "A shape with straight sides has the same number of corners as sides: 12 sides, 12 corners."))
    its.append(mcq("A slice cut from the centre of a round pizza is closest to which shape?", "a triangle",
                   ["a square", "a rectangle", "a circle"],
                   "The slice has 2 straight sides that meet at a point in the middle and a slightly curved crust: close to a triangle."))
    its.append(mcq("A bucket is wider at the top than at the bottom. From the side, it looks closest to which shape?", "a trapezium",
                   ["a rectangle", "a triangle", "a square"],
                   "From the side you see 4 sides: the top and bottom are parallel but the top is longer. That is a trapezium."))
    its.append(mcq("A netball court is closest to which shape?", "a rectangle", ["a square", "a circle", "a triangle"],
                   "A netball court has 4 straight sides and 4 right angles, and it is longer than it is wide: a rectangle."))
    its.append(mcq("A tennis ball tube is closest to which object?", CYL, ["circle", RP, CONE],
                   "It has a circle at each end and a curved side: a cylinder."))
    its.append(mcq("A lighthouse with a pointed roof can be modelled with which two objects?", "a cylinder and a cone",
                   ["a rectangle and a triangle", "a cube and a sphere", "a cylinder and a triangular prism"],
                   "The tall round tower is a cylinder and the pointed roof with a circle base is a cone."))
    n, he, his = P_.next()
    its.append(mcq("%s glues a square-based pyramid on top of a cube to make a tower. How many faces are on the outside of the tower?" % n,
                   9, [11, 10, 8],
                   "Cube 6 + pyramid 5 = 11 faces, but the top of the cube and the bottom of the pyramid are glued together and hidden. "
                   "11 − 2 = 9."))
    n, he, his = P_.next()
    its.append(mcq("%s glues one cube on top of another. How many square faces are on the outside now?" % n, 10, [12, 11, 8],
                   "2 cubes have 6 + 6 = 12 faces. The 2 faces glued together are hidden: 12 − 2 = 10."))
    its.append(mcq("A silo is a cylinder with a cone roof. How many flat faces does the whole silo have?", 1, [3, 2, 0],
                   "A cylinder has 2 flat circle faces and a cone has 1. The cone sits on the top circle of the cylinder, so both of those are hidden. "
                   "Only the circle on the ground is left: 1."))
    n, he, his = P_.next()
    its.append(mcq("%s makes a model pine tree: a cone on top of a thin cylinder trunk. How many curved surfaces does the model have?" % n,
                   2, [1, 3, 4],
                   "A cone has 1 curved surface and a cylinder has 1 curved surface: 1 + 1 = 2."))
    n, he, his = P_.next()
    its.append(mcq("%s draws houses. Each house is a square with a triangle roof, a rectangle door and 2 square windows. "
                   "%s draws 3 houses. How many squares does %s draw?" % (n, he.capitalize(), he), 9, [3, 6, 12],
                   "Each house has 1 square wall + 2 square windows = 3 squares. 3 houses: 3 × 3 = 9."))
    n, he, his = P_.next()
    its.append(mcq("%s uses triangle pattern blocks. 6 triangles make 1 hexagon. How many triangles does %s need for 3 hexagons?" % (n, he),
                   18, [9, 6, 12], "Each hexagon needs 6 triangles: 3 × 6 = 18."))
    n, he, his = P_.next()
    its.append(mcq("1 trapezium pattern block covers the same space as 3 triangle blocks. A hexagon is 6 triangle blocks. "
                   "How many trapezium blocks cover a hexagon?", 2, [3, 6, 1],
                   "6 triangles ÷ 3 triangles in each trapezium = 2 trapeziums. You can see this in a hexagon cut in half."))
    n, he, his = P_.next()
    assert stack_seen(4, 2, 3) == 18
    its.append(mcq("%s builds a solid block of cubes 4 long, 2 wide and 3 high. How many cubes does %s use?" % (n, he), 24, [18, 9, 8],
                   "Each layer is 4 × 2 = 8 cubes. 3 layers: 8 + 8 + 8 = 24. From one corner you can see only 18; 6 are hidden behind the others. "
                   "Adding 4 + 2 + 3 = 9 does not count the cubes."))
    n, he, his = P_.next()
    its.append(mcq("%s puts 3 stop signs in a row for a road safety lesson. Each stop sign is an octagon. How many sides are there altogether?" % n,
                   24, [11, 18, 16],
                   "An octagon has 8 sides. 3 octagons: 3 × 8 = 24 sides. 18 would be 3 hexagons."))
    n, he, his = P_.next()
    its.append(mcq("%s makes a hexagon from 6 triangles. Each side of a triangle is 5 cm. What is the distance around the hexagon?" % n,
                   "30 cm", ["90 cm", "15 cm", "60 cm"],
                   "Only the 6 sides on the outside count: 6 × 5 = 30 cm. The lines inside the hexagon are not part of the outline."))
    its.append(mcq("Which object is closest to the shape of a cricket ball?", SPH, ["circle", CYL, CONE],
                   "A cricket ball is round all over: a sphere."))
    its.append(mcq("A shoebox lid is lying flat on the table. Seen from above, it is closest to which shape?", "a rectangle",
                   ["a rectangular prism", "a square", "a trapezium"],
                   "From above you see only the flat top of the lid: 4 sides and 4 right angles, longer than it is wide. That is a rectangle."))
    assert len(its) == 20, len(its)
    return {"title": "Real-world problems: model things with shapes and objects", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    shapes = row_svg([shape_cv(TRI, 0.5), shape_cv(SQ, 0.5), shape_cv(RECT, 0.42), shape_cv(TRAP, 0.42),
                      shape_cv(PENT, 0.55), shape_cv(HEX, 0.55), shape_cv(OCT, 0.55)],
                     ["triangle", "square", "rectangle", "trapezium", "pentagon", "hexagon", "octagon"],
                     "triangle, square, rectangle, trapezium, pentagon, hexagon and octagon", gap=14, fs=14)
    comps = row_svg([comp_cv(C_HOUSE, 0.8), comp_cv(C_ROCKET, 0.7), comp_cv(C_HEX6, 0.75)],
                    ["square + triangle", "rectangle + 3 triangles", "6 triangles"],
                    "a house, a rocket and a hexagon made of smaller shapes", gap=30, fs=14)
    tri3 = hidden_cv(H1).svg("a triangle cut by one line into 2 smaller triangles")
    objs = row_svg([cyl_cone_cv(s=0.8), icecream_cv(s=0.8), house3d_cv(38), tower_cv(38)],
                   ["cylinder + cone", "cone + sphere", "2 prisms", "cube + pyramid"],
                   "a silo, an ice-cream, a house and a tower made of objects", gap=22, fs=14)
    stack = cube_stack(2, 2, 2).svg("a solid stack of 8 cubes")
    return (
        "<h2>Familiar 2-D shapes</h2>"
        "<p>A 2-D shape is flat. Name a shape by counting its <b>sides</b>. It has the same number of <b>corners</b>. "
        "A shape keeps its name when it is turned, and its sides do not have to be equal.</p>"
        "<figure class='sn-fig'>" + shapes +
        "<figcaption>A square, a rectangle and a trapezium all have 4 sides, so they are quadrilaterals.</figcaption></figure>" +
        table(["Shape", "Sides and corners", "Look for", "In real life"], [
            ["Triangle", "3", "3 straight sides", "a give way sign"],
            ["Square", "4", "4 equal sides, 4 right angles", "a window pane"],
            ["Rectangle", "4", "4 right angles", "a netball court"],
            ["Trapezium", "4", "only 1 pair of parallel sides", "a bucket seen from the side"],
            ["Pentagon", "5", "5 straight sides", "the outline of a house"],
            ["Hexagon", "6", "6 straight sides", "a honeycomb cell"],
            ["Octagon", "8", "8 straight sides", "a stop sign"]]) +
        "<p>A square has 4 right angles, so a square is a special rectangle.</p>"
        "<h2>Composite shapes</h2>"
        "<p>A <b>composite shape</b> is made of smaller familiar shapes. Look for the lines inside to find the parts. "
        "Then count the sides round the outside to name the whole outline.</p>"
        "<figure class='sn-fig'>" + comps + "</figure>" +
        ex("Example 1", "A house is a square with a triangle roof. How many sides does the whole outline have?",
           "Go round the outside: 2 walls, the floor and 2 roof sides. The line between the roof and the walls is inside, so do not count it.",
           "5 sides, so the outline is a pentagon") +
        "<figure class='sn-fig'>" + tri3 + "</figure>" +
        ex("Example 2", "How many triangles are in this picture?",
           "Count the small triangles: 2. Then look for bigger triangles made of smaller ones: the whole shape is 1 more. 2 + 1 = 3.",
           "3 triangles") +
        "<h2>Composite objects</h2>"
        "<p>Things around us are often made of familiar 3-D <b>objects</b>: cubes, prisms, pyramids, cylinders, cones and spheres.</p>"
        "<figure class='sn-fig'>" + objs +
        "<figcaption>A silo, an ice-cream, a house and a tower.</figcaption></figure>" +
        table(["Real thing", "Objects that model it"], [
            ["Farm silo, rocket, crayon", "cylinder + cone"],
            ["Ice-cream", "cone + sphere"],
            ["House with a sloping roof", "rectangular prism + triangular prism"],
            ["Tent", "triangular prism"],
            ["Shipping container, cereal box", "rectangular prism"]]) +
        "<figure class='sn-fig'>" + stack + "</figure>" +
        ex("Example 3", "How many cubes are in this solid stack?",
           "Each layer has 2 × 2 = 4 cubes and there are 2 layers: 4 + 4 = 8. You can see only 7; 1 cube is hidden at the back.",
           "8 cubes") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Saying a square is not a rectangle", "A square has 4 right angles, so it is a special rectangle"],
            ["Adding the sides of the parts (4 + 3 = 7 for a house)", "Count only the sides round the outside"],
            ["Forgetting the big shape made of small ones", "After the small shapes, look for shapes made of 2, 3 or more"],
            ["Calling a tent a pyramid", "A pyramid comes to a point; a prism has the same shape at both ends"],
            ["Counting only the cubes or faces you can see", "Remember the ones at the back, underneath and inside"],
            ["Using 2-D names for objects (a can is a “circle”)", "A can is a cylinder; only its ends are circles"],
        ])
    )


FAQ = [
    {"q": "What is a composite shape in Year 4 maths?",
     "a": "A composite shape is made of two or more familiar shapes, such as a house made of a square and a triangle. In the Australian Curriculum (AC9M4SP01), Year 4 students describe and draw composite shapes and objects using familiar shapes."},
    {"q": "Is a square a rectangle?",
     "a": "Yes. A rectangle is any 4-sided shape with 4 right angles, and a square has these too, so a square is a special rectangle with 4 equal sides."},
    {"q": "What is the difference between a shape and an object?",
     "a": "A shape is flat (2-D), like a triangle or a circle. An object is solid (3-D), like a cone or a cylinder. A silo is an object made of a cylinder and a cone."},
    {"q": "How can my child practise composite shapes at home?",
     "a": "Go on a shape hunt: find the shapes in road signs, buildings and playground equipment, and build houses, towers and rockets from blocks, boxes and tins. Then try the 100 questions on this page and check them with the answer key."},
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
    """Tag pictures that must print larger (A-D choices, wide pictures) so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(4818)
    P_ = People(rnd)
    pos = Pos(rnd)
    sets = [set_name(rnd, pos), set_make(rnd, pos), set_count(rnd, P_), set_objects(rnd, P_), set_problems(rnd, P_)]
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
        "country": "au", "subject": "maths", "grade": "year-4", "slug": "shapes-and-composite-objects", "sort": 18,
        "updated": UPDATED, "pdf_url": "",
        "title": "Shapes and Composite Objects: Name, Combine and Count Shapes and Objects",
        "seo_title": "Year 4 Composite Shapes and Objects Worksheets: 2-D Shapes, Composite Shapes and 3-D Objects (Free, Answer Key)",
        "short_title": "Shapes and composite objects",
        "domain": "Space",
        "standard_code": "AC9M4SP01",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Represent and approximate composite shapes and objects in the environment, using combinations of familiar shapes and objects",
        "meta_desc": "Free Year 4 maths worksheets on shapes and composite objects: name triangles, quadrilaterals, trapeziums, pentagons, hexagons and octagons, find the shapes that make a composite shape, count the shapes in a picture, and model a silo as a cylinder and a cone. 100 questions with an answer key, following the Australian Curriculum.",
        "key_big": "Big shapes and objects are made of smaller familiar ones: a house is a square and a triangle; a silo is a cylinder and a cone.",
        "key_sub": "Name a shape by counting its sides round the outside. A square is a special rectangle. When you count shapes or cubes, look for the big ones and the hidden ones too.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(four 2-D shapes labelled A to D|four composite shapes labelled A to D|a picture made of shapes)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
