# -*- coding: utf-8 -*-
"""
British Columbia Grade 4 Math: Regular and irregular polygons (BC Mathematics Curriculum, Geometry and measurement)
  python3 tools/gen_cabc_math_g4_polygons.py
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.

Every shape is drawn from its own corner points. Sides, angles, "regular", right angles and the name
(triangle ... decagon, square, rectangle, rhombus, trapezoid) are worked out in code from the same points,
and the marks on the pictures (ticks for equal sides, small squares for right angles, arcs for equal angles)
come from those facts too. Venn diagram answers are checked from the same facts.
Wrong answers come from real student mistakes: a shape with a curve or an open shape counted as a polygon,
a star named by its points, a side missed or counted twice, equal sides alone (a rhombus) or equal angles
alone (a rectangle) taken as regular, a turned square called something else.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
BLUE = "#2f6fb5"
ORANGE = "#c96a12"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Ji-woo", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]
NAMES = {3: "triangle", 4: "quadrilateral", 5: "pentagon", 6: "hexagon", 7: "heptagon", 8: "octagon", 10: "decagon"}


# ------------------------------------------------------------ question helpers
def mcq(q, correct, cands, e):
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c:
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


def tw(t, fs):
    """Approximate width of bold Arial text in px."""
    t = str(t)
    return (len(t) - t.count(" ") * 0.3) * fs * 0.62


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


# ------------------------------------------------------------ geometry (screen coordinates, y down)
def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def unit(v):
    L = math.hypot(v[0], v[1])
    return (v[0] / L, v[1] / L)


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
    """Interior angles in degrees; works for shapes that cave in (angles over 180)."""
    s = 1 if area(pts) > 0 else -1
    n = len(pts)
    out = []
    for i in range(n):
        a, b, c = pts[i - 1], pts[i], pts[(i + 1) % n]
        u, v = sub(b, a), sub(c, b)
        turn = math.degrees(math.atan2(u[0] * v[1] - u[1] * v[0], u[0] * v[0] + u[1] * v[1])) * s
        out.append(180 - turn)
    assert abs(sum(out) - 180 * (n - 2)) < 1e-6, out
    return out


def side_lens(pts):
    n = len(pts)
    return [math.hypot(*sub(pts[(i + 1) % n], pts[i])) for i in range(n)]


def segs_cross(p1, p2, p3, p4):
    def o(a, b, c):
        v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        return 0 if abs(v) < 1e-9 else (1 if v > 0 else -1)
    return o(p1, p2, p3) * o(p1, p2, p4) < 0 and o(p3, p4, p1) * o(p3, p4, p2) < 0


def is_simple(pts):
    n = len(pts)
    for i in range(n):
        for j in range(i + 1, n):
            if j == i + 1 or (i == 0 and j == n - 1):
                continue
            if segs_cross(pts[i], pts[(i + 1) % n], pts[j], pts[(j + 1) % n]):
                return False
    return True


def facts(pts):
    p = simplify(pts)
    assert is_simple(p)
    n = len(p)
    L = side_lens(p)
    A = interior_angles(p)
    eqs = max(L) - min(L) < 1e-6 * max(L)
    eqa = max(A) - min(A) < 1e-6
    rights = sum(1 for a in A if abs(a - 90) < 1e-6)
    f = {"n": n, "lens": L, "angles": A, "eqs": eqs, "eqa": eqa, "regular": eqs and eqa, "rights": rights,
         "concave": max(A) > 180 + 1e-6}
    f["name"] = NAMES[n]
    f["quad"] = quad_name(p, f) if n == 4 else None
    return f


def quad_name(p, f):
    sv = [sub(p[(i + 1) % 4], p[i]) for i in range(4)]
    par = sum(1 for i, j in [(0, 2), (1, 3)] if abs(sv[i][0] * sv[j][1] - sv[i][1] * sv[j][0]) < 1e-6 * f["lens"][i] * f["lens"][j])
    if f["rights"] == 4:
        return "square" if f["eqs"] else "rectangle"
    if f["eqs"]:
        return "rhombus"
    if par == 2:
        return "parallelogram"
    if par == 1:
        return "trapezoid"
    return "quadrilateral"


def regular(n, r=60, start=-90):
    return [(r * math.cos(math.radians(start + 360.0 * i / n)), r * math.sin(math.radians(start + 360.0 * i / n)))
            for i in range(n)]


def walk(lens, dirs):
    """A closed shape from side lengths and directions (degrees)."""
    p = [(0.0, 0.0)]
    for L, d in zip(lens, dirs):
        x, y = p[-1]
        p.append((x + L * math.cos(math.radians(d)), y + L * math.sin(math.radians(d))))
    assert math.hypot(*sub(p[-1], p[0])) < 1e-6, p[-1]
    return p[:-1]


def rot_pt(p, deg):
    t = math.radians(deg)
    return (p[0] * math.cos(t) - p[1] * math.sin(t), p[0] * math.sin(t) + p[1] * math.cos(t))


# ------------------------------------------------------------ the shapes
def P(pts, marks=("ticks", "angles")):
    """A polygon."""
    pts = [(float(x), float(y)) for x, y in pts]
    return {"pts": pts, "poly": True, "closed": True, "marks": marks, "f": facts(pts)}


def NP(pts, closed=True, cross=False, why="curve"):
    """Not a polygon: a curve (many points), an open shape, or sides that cross."""
    return {"pts": [(float(x), float(y)) for x, y in pts], "poly": False, "closed": closed, "cross": cross,
            "marks": (), "why": why, "f": None}


def arc_pts(cx, cy, rx, ry, a0, a1, n=36):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def rounded_rect(w, h, r):
    out = []
    for cx, cy, a0 in [(w - r, r, -90), (w - r, h - r, 0), (r, h - r, 90), (r, r, 180)]:
        out += arc_pts(cx, cy, r, r, a0, a0 + 90, 12)
    return out


def star(R=60, r=24):
    return [(rr * math.cos(math.radians(-90 + 36 * i)), rr * math.sin(math.radians(-90 + 36 * i)))
            for i, rr in enumerate([R, r] * 5)]


SQ = P([(0, 0), (100, 0), (100, 100), (0, 100)])
RECT = P([(0, 0), (160, 0), (160, 90), (0, 90)])
RHOM = P(walk([100] * 4, [0, 60, 180, 240]))
PARA = P(walk([140, 80, 140, 80], [0, 60, 180, 240]))
ITRAP = P([(0, 80), (160, 80), (115, 0), (45, 0)])
RTRAP = P([(0, 80), (150, 80), (80, 0), (0, 0)])
KITE = P([(0, 0), (70, 20), (0, 150), (-70, 20)])
QUAD = P([(0, 15), (140, 0), (125, 70), (40, 125)], ())
TRI_S = P([(0, 100), (90, 100), (130, 0)])
TRI_R = P([(0, 0), (0, 90), (120, 90)])
TRI_I = P([(0, 110), (90, 110), (45, 0)])
HOUSE = P([(0, 0), (60, -30), (120, 0), (120, 90), (0, 90)])
PENT_I = P([(60, 0), (130, 45), (105, 120), (15, 120), (0, 45)], ())
HEX_I = P([(30, 0), (110, 0), (150, 50), (110, 100), (30, 100), (0, 50)], ())
L_SH = P([(0, 0), (50, 0), (50, 75), (125, 75), (125, 125), (0, 125)], ("angles",))
ARROW = P([(0, 30), (90, 30), (90, 0), (140, 45), (90, 90), (90, 60), (0, 60)], ())
T_SH = P([(0, 0), (120, 0), (120, 40), (80, 40), (80, 110), (40, 110), (40, 40), (0, 40)], ("angles",))
STAR = P(star(), ())
EQHEX = P(walk([62] * 6, [0, 70, 140, 180, 250, 320]))
ALTHEX = P(walk([90, 40] * 3, [0, 60, 120, 180, 240, 300]))
CUTOCT = P(walk([80, 30] * 4, [0, 45, 90, 135, 180, 225, 270, 315]))
DEC_I = P([(x * 1.6, y) for x, y in regular(10, 55, -90)], ())
REG = {n: P(regular(n, 60, -90 if n % 2 else -90 + 180.0 / n)) for n in (3, 5, 6, 7, 8, 10)}
REG[4] = SQ

CIRCLE = NP(arc_pts(0, 0, 55, 55, 0, 360, 72)[:-1])
OVAL = NP(arc_pts(0, 0, 80, 45, 0, 360, 72)[:-1])
SEMI = NP(arc_pts(0, 0, 70, 70, 180, 360, 36))
RINK = NP(rounded_rect(170, 85, 28))
CURVSIDE = NP([(0, 100), (150, 100), (150, 0), (40, 0)] +
              [((1 - t) ** 2 * 40 + 2 * (1 - t) * t * (-35), (1 - t) ** 2 * 0 + 2 * (1 - t) * t * 50 + t * t * 100)
               for t in [i / 24.0 for i in range(1, 24)]])
_la = math.degrees(math.asin(0.7))
LEAF = NP(arc_pts(0, -70, 100, 100, _la, 180 - _la, 20)[:-1] + arc_pts(0, 70, 100, 100, 180 + _la, 360 - _la, 20)[:-1])
GAPTRI = NP([(80, 120), (130, 120), (65, 0), (0, 120), (50, 120)], closed=False, why="open")
OPEN5 = NP([(40, 0), (140, 0), (150, 90), (0, 90), (8, 34)], closed=False, why="open")
BOWTIE = NP([(0, 0), (130, 90), (130, 0), (0, 90)], cross=True, why="cross")
PENTAGRAM = NP([regular(5, 62)[(2 * i) % 5] for i in range(5)], cross=True, why="cross")
for _s in (CIRCLE, OVAL, SEMI, RINK, CURVSIDE, LEAF):
    assert len(_s["pts"]) > 20
assert not is_simple(BOWTIE["pts"]) and not is_simple(PENTAGRAM["pts"])

# the facts the questions rely on
assert SQ["f"]["regular"] and SQ["f"]["quad"] == "square"
assert RECT["f"]["eqa"] and not RECT["f"]["eqs"] and RECT["f"]["quad"] == "rectangle"
assert RHOM["f"]["eqs"] and not RHOM["f"]["eqa"] and RHOM["f"]["quad"] == "rhombus"
assert PARA["f"]["quad"] == "parallelogram" and PARA["f"]["rights"] == 0
assert ITRAP["f"]["quad"] == "trapezoid" and RTRAP["f"]["quad"] == "trapezoid" and RTRAP["f"]["rights"] == 2
assert KITE["f"]["quad"] == "quadrilateral" and QUAD["f"]["quad"] == "quadrilateral"
assert TRI_R["f"]["rights"] == 1 and not TRI_I["f"]["eqs"] and not TRI_S["f"]["eqs"]
assert HOUSE["f"]["n"] == 5 and HOUSE["f"]["rights"] == 2
assert L_SH["f"]["n"] == 6 and L_SH["f"]["concave"] and L_SH["f"]["rights"] == 5
assert ARROW["f"]["n"] == 7 and T_SH["f"]["n"] == 8 and STAR["f"]["n"] == 10 and DEC_I["f"]["n"] == 10
assert STAR["f"]["eqs"] and not STAR["f"]["eqa"]
assert EQHEX["f"]["eqs"] and not EQHEX["f"]["eqa"]
assert ALTHEX["f"]["eqa"] and not ALTHEX["f"]["eqs"] and CUTOCT["f"]["eqa"] and not CUTOCT["f"]["eqs"]
for _n, _s in REG.items():
    assert _s["f"]["regular"] and _s["f"]["n"] == _n
for _s in (PENT_I, HEX_I, DEC_I, QUAD):
    assert not _s["f"]["eqs"] and not _s["f"]["eqa"]


# ------------------------------------------------------------ drawing
def place(sh, rot, bw, bh, cx, cy):
    """Rotate, scale to fit a bw x bh box and centre at (cx, cy)."""
    pts = [rot_pt(p, rot) for p in sh["pts"]]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    k = min(bw / (max(xs) - min(xs)), bh / (max(ys) - min(ys)))
    mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    return [(cx + (x - mx) * k, cy + (y - my) * k) for x, y in pts]


def groups(vals, tol):
    gs = []
    for i, v in enumerate(vals):
        for g in gs:
            if abs(vals[g[0]] - v) <= tol(v):
                g.append(i)
                break
        else:
            gs.append([i])
    return gs


def shape_elems(sh, rot, bw, bh, cx, cy, sw=2.6, fill=FILL, col=GREEN, marks=None):
    """SVG elements for one shape (and its marks) and the box around everything drawn."""
    pts = place(sh, rot, bw, bh, cx, cy)
    PS = lambda ps: " ".join("%.1f,%.1f" % p for p in ps)
    el, box = [], list(pts)
    marks = sh["marks"] if marks is None else marks
    if not sh["closed"]:
        el.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='%g' stroke-linecap='round' stroke-linejoin='round'/>"
                  % (PS(pts), col, sw))
    else:
        el.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'%s/>"
                  % (PS(pts), fill, col, sw, " fill-rule='evenodd'" if sh.get("cross") else ""))
    if sh["poly"] and marks:
        p = simplify(pts)
        n = len(p)
        L, A = side_lens(p), interior_angles(p)
        mk = "stroke='%s' stroke-width='2' fill='none' stroke-linecap='round'" % INK
        if "ticks" in marks:
            gs = groups(L, lambda v: 1e-6 * v)
            for g1 in gs:                                    # sides that look equal but are not would confuse
                for g2 in gs:
                    if g1 is not g2:
                        a, b = L[g1[0]], L[g2[0]]
                        assert abs(a - b) / max(a, b) > 0.12, ("sides look equal", L)
            cnt = 0
            for g in gs:
                if len(g) < 2:
                    continue
                cnt += 1
                assert cnt <= 3
                for i in g:
                    a, b = p[i], p[(i + 1) % n]
                    d = unit(sub(b, a))
                    nr = (-d[1], d[0])
                    m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
                    for j in range(cnt):
                        o = (j - (cnt - 1) / 2.0) * 5
                        c = (m[0] + d[0] * o, m[1] + d[1] * o)
                        q1, q2 = (c[0] - nr[0] * 6, c[1] - nr[1] * 6), (c[0] + nr[0] * 6, c[1] + nr[1] * 6)
                        el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' %s/>" % (q1 + q2 + (mk,)))
                        box += [q1, q2]
        if "angles" in marks:
            for i, a in enumerate(A):                       # an unmarked angle must not look like a right angle
                assert abs(a - 90) < 1e-6 or abs(a - 90) >= 10, ("almost a right angle", A)
            gs = groups(A, lambda v: 1e-6)
            for g1 in gs:
                for g2 in gs:
                    if g1 is not g2 and len(g1) > 1 and len(g2) > 1:
                        assert abs(A[g1[0]] - A[g2[0]]) >= 10, ("angles look equal", A)
            cnt = 0
            for g in gs:
                a = A[g[0]]
                right = abs(a - 90) < 1e-6
                if not right and (len(g) < 2 or a > 180):
                    continue
                if not right:
                    cnt += 1
                    assert cnt <= 2
                for i in g:
                    v = p[i]
                    u1, u2 = unit(sub(p[i - 1], v)), unit(sub(p[(i + 1) % n], v))
                    short = min(L[i - 1], L[i])
                    if right:
                        k = min(10, 0.2 * short)
                        q1 = (v[0] + u1[0] * k, v[1] + u1[1] * k)
                        q2 = (q1[0] + u2[0] * k, q1[1] + u2[1] * k)
                        q3 = (v[0] + u2[0] * k, v[1] + u2[1] * k)
                        el.append("<polyline points='%s' %s/>" % (PS([q1, q2, q3]), mk.replace("stroke-width='2'", "stroke-width='1.6'")))
                        box += [q1, q2, q3]
                    else:
                        sweep = 1 if u1[0] * u2[1] - u1[1] * u2[0] > 0 else 0
                        for j in range(cnt):
                            r = min(11, 0.26 * short) + 4 * j
                            a1 = (v[0] + u1[0] * r, v[1] + u1[1] * r)
                            a2 = (v[0] + u2[0] * r, v[1] + u2[1] * r)
                            el.append("<path d='M%.1f,%.1f A%.1f,%.1f 0 0 %d %.1f,%.1f' %s/>"
                                      % (a1[0], a1[1], r, r, sweep, a2[0], a2[1], mk.replace("stroke-width='2'", "stroke-width='1.6'")))
    pad = sw / 2.0 + 1
    bb = (min(p[0] for p in box) - pad, min(p[1] for p in box) - pad, max(p[0] for p in box) + pad, max(p[1] for p in box) + pad)
    return el, bb


def shape_svg(sh, rot=0, bw=130, bh=88, label="a shape", marks=None):
    _, bb = shape_elems(sh, rot, bw, bh, 0, 0, marks=marks)
    pad = 6
    W, H = int(math.ceil(bb[2] - bb[0] + 2 * pad)), int(math.ceil(bb[3] - bb[1] + 2 * pad))
    if W == H:
        W += 1                                             # keep figures out of the larger 'square' print size
    el, bb2 = shape_elems(sh, rot, bw, bh, pad - bb[0] + (W - (bb[2] - bb[0] + 2 * pad)) / 2, pad - bb[1], marks=marks)
    assert bb2[0] >= 0 and bb2[1] >= 0 and bb2[2] <= W + 0.01 and bb2[3] <= H + 0.01, (bb2, W, H)
    return svg_wrap(W, H, "".join(el), label)


CELL = 118


def grid_svg(items, label="four shapes labelled A to D", marks=None):
    """2 x 2 grid of shapes labelled A-D. items: list of (shape, rot)."""
    W = H = 2 * CELL
    el = ["<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, CELL, H - 4, GRAY),
          "<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, W - 4, CELL, GRAY)]
    for k, (sh, rot) in enumerate(items):
        x0, y0 = (k % 2) * CELL, (k // 2) * CELL
        e, bb = shape_elems(sh, rot, 74, 74, x0 + 67, y0 + 64, sw=2.4, marks=marks)
        assert bb[0] >= x0 + 18 and bb[1] >= y0 + 4 and bb[2] <= x0 + CELL - 3 and bb[3] <= y0 + CELL - 3, bb
        el += e
        el.append("<text x='%d' y='%d' font-size='18' font-weight='700' fill='%s'>%s</text>" % (x0 + 6, y0 + 22, INK, "ABCD"[k]))
    return svg_wrap(W, H, "".join(el), label)


def strip_svg(items, label, cw=124, bw=88, bh=78, fs=15, marks=None):
    """A row of shapes with a caption under each. items: (shape, rot, caption)."""
    top = bh + 24
    el = []
    for k, (sh, rot, cap) in enumerate(items):
        e, bb = shape_elems(sh, rot, bw, bh, k * cw + cw / 2, top / 2, sw=2.6, marks=marks)
        assert bb[0] >= k * cw + 2 and bb[2] <= (k + 1) * cw - 2 and bb[1] >= 0 and bb[3] <= top, (cap, bb)
        assert tw(cap, fs) <= cw - 4, cap
        el += e
        el.append("<text x='%d' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                  % (k * cw + cw / 2, top + fs + 2, fs, INK, cap))
    return svg_wrap(cw * len(items), top + fs + 8, "".join(el), label)


# ------------------------------------------------------------ Venn diagrams
CRIT = {
    "Regular": lambda f: f["regular"],
    "4 sides": lambda f: f["n"] == 4,
    "Has a right angle": lambda f: f["rights"] > 0,
    "All sides equal": lambda f: f["eqs"],
    "All angles equal": lambda f: f["eqa"],
    "Triangle": lambda f: f["n"] == 3,
    "6 sides": lambda f: f["n"] == 6,
}


def region(l1, l2, f):
    a, b = CRIT[l1](f), CRIT[l2](f)
    return "B" if a and b else "A" if a else "C" if b else "D"


def venn_frame(l1, l2, Wv, r=66, d=76, H=204, fs=15):
    cx1, cx2, cy = Wv / 2.0 - d / 2.0, Wv / 2.0 + d / 2.0, 118
    assert tw(l1, fs) + tw(l2, fs) + 30 <= Wv, (l1, l2)
    assert cy - r > 30 and cy + r < H - 8
    el = ["<rect x='2' y='2' width='%d' height='%d' rx='8' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (Wv - 4, H - 4, INK),
          "<circle cx='%.1f' cy='%d' r='%d' fill='%s' fill-opacity='0.12' stroke='%s' stroke-width='2.4'/>" % (cx1, cy, r, BLUE, BLUE),
          "<circle cx='%.1f' cy='%d' r='%d' fill='%s' fill-opacity='0.12' stroke='%s' stroke-width='2.4'/>" % (cx2, cy, r, ORANGE, ORANGE),
          "<text x='12' y='28' font-size='%d' font-weight='700' fill='%s'>%s</text>" % (fs, BLUE, l1),
          "<text x='%d' y='28' font-size='%d' font-weight='700' fill='%s' text-anchor='end'>%s</text>" % (Wv - 12, fs, ORANGE, l2)]
    # the labels must not run into each other
    assert 12 + tw(l1, fs) < Wv - 12 - tw(l2, fs)
    return el, (cx1, cx2, cy, r, H)


def venn_svg(l1, l2, sh, rot=0):
    """Venn diagram with regions A-D and one shape beside it in a dashed box."""
    Wv = max(286, int(math.ceil(tw(l1, 15) + tw(l2, 15) + 40)))
    el, (cx1, cx2, cy, r, H) = venn_frame(l1, l2, Wv)
    for t, x, y in [("A", cx1 - 36, cy + 7), ("B", (cx1 + cx2) / 2, cy + 7), ("C", cx2 + 36, cy + 7), ("D", 18, H - 14)]:
        el.append("<text x='%.1f' y='%.1f' font-size='20' font-weight='700' fill='%s' text-anchor='middle'>%s</text>" % (x, y, INK, t))
    bx, bw = Wv + 12, 128
    el.append("<rect x='%d' y='2' width='%d' height='%d' rx='8' fill='none' stroke='%s' stroke-width='1.6' stroke-dasharray='6 4'/>"
              % (bx, bw, H - 4, GRAY))
    e, bb = shape_elems(sh, rot, 92, 92, bx + bw / 2.0, H / 2.0, sw=2.6)
    assert bb[0] >= bx + 3 and bb[2] <= bx + bw - 3 and bb[1] >= 4 and bb[3] <= H - 4, bb
    el += e
    return svg_wrap(bx + bw + 2, H, "".join(el), "a Venn diagram with regions A to D and a shape")


def venn_lesson_svg():
    """Venn diagram with shapes inside: all sides equal / all angles equal."""
    Wv = 330
    l1, l2 = "All sides equal", "All angles equal"
    el, (cx1, cx2, cy, r, H) = venn_frame(l1, l2, Wv)
    put = [(RHOM, 30, cx1 - 34, cy, 50), (SQ, 15, (cx1 + cx2) / 2, cy - 21, 27), (REG[3], 0, (cx1 + cx2) / 2, cy + 19, 27),
           (RECT, 0, cx2 + 34, cy, 50), (KITE, 0, Wv - 32, H - 46, 44)]
    for sh, rot, x, y, s in put:
        e, bb = shape_elems(sh, rot, s, s, x, y, sw=2, marks=())
        el += e
    assert region(l1, l2, RHOM["f"]) == "A" and region(l1, l2, SQ["f"]) == "B" and region(l1, l2, REG[3]["f"]) == "B"
    assert region(l1, l2, RECT["f"]) == "C" and region(l1, l2, KITE["f"]) == "D"
    return svg_wrap(Wv, H, "".join(el), "a Venn diagram sorting a rhombus, a square, a triangle, a rectangle and a kite")


# ------------------------------------------------------------ real-life pictures
def poly_el(pts, fill, col, sw):
    return "<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>" % (
        " ".join("%.1f,%.1f" % p for p in pts), fill, col, sw)


def stop_sign_svg():
    o = [(x + 60, y + 60) for x, y in regular(8, 56, -90 + 22.5)]
    i = [(x + 60, y + 60) for x, y in regular(8, 50, -90 + 22.5)]
    body = (poly_el(o, RED, "#7d1d14", 2) + poly_el(i, "none", "#ffffff", 2.4) +
            "<text x='60' y='68' font-size='24' font-weight='700' fill='#ffffff' text-anchor='middle'>STOP</text>")
    return svg_wrap(121, 120, body, "a stop sign")


def yield_svg():
    o = [(10, 8), (130, 8), (70, 112)]
    i = [(32, 21), (108, 21), (70, 87)]
    return svg_wrap(141, 120, poly_el(o, RED, "#7d1d14", 2) + poly_el(i, "#ffffff", "#ffffff", 1), "a yield sign")


def school_sign_svg():
    pts = [(10, 50), (60, 8), (110, 50), (110, 122), (10, 122)]
    return svg_wrap(121, 130, poly_el(pts, "#c6e01a", INK, 2.6), "a school zone sign shaped like a house")


def honeycomb_svg():
    s = 22
    h = s * math.sqrt(3)
    el = []
    for cx, cy in [(0, 0), (1.5 * s, h / 2), (1.5 * s, -h / 2), (0, h), (0, -h), (-1.5 * s, h / 2), (-1.5 * s, -h / 2)]:
        el.append(poly_el([(cx + 80 + x, cy + 62 + y) for x, y in regular(6, s, 0)], "#f3c623", "#9a6b00", 2.2))
    return svg_wrap(161, 124, "".join(el), "honeycomb cells")


def rink_svg():
    pts = [(x + 8, y + 8) for x, y in rounded_rect(170, 85, 28)]
    body = (poly_el(pts, "#ffffff", INK, 2.6) +
            "<line x1='93' y1='8' x2='93' y2='93' stroke='%s' stroke-width='3'/>" % RED +
            "<line x1='66' y1='8' x2='66' y2='93' stroke='%s' stroke-width='3'/>" % BLUE +
            "<line x1='120' y1='8' x2='120' y2='93' stroke='%s' stroke-width='3'/>" % BLUE +
            "<circle cx='93' cy='50.5' r='13' fill='none' stroke='%s' stroke-width='2'/>" % BLUE)
    return svg_wrap(187, 101, body, "a hockey rink")


S_PB = 44
PB = {
    "hexagon": (regular(6, S_PB, 0), "#f3c623"),
    "trapezoid": ([(0, 0), (2 * S_PB, 0), (1.5 * S_PB, -S_PB * math.sqrt(3) / 2), (0.5 * S_PB, -S_PB * math.sqrt(3) / 2)], "#d6453b"),
    "blue": (walk([S_PB] * 4, [0, 300, 180, 120]), "#2f6fb5"),
    "tan": (walk([S_PB] * 4, [0, 330, 180, 150]), "#e3c9a0"),
}
assert facts(PB["hexagon"][0])["regular"] and facts(PB["trapezoid"][0])["quad"] == "trapezoid"
assert facts(PB["blue"][0])["quad"] == "rhombus" and facts(PB["tan"][0])["quad"] == "rhombus"
_tl = side_lens(PB["trapezoid"][0])
assert sorted(round(x, 6) for x in _tl) == [S_PB, S_PB, S_PB, 2 * S_PB]


def pattern_blocks_svg():
    caps = [("hexagon", "yellow"), ("trapezoid", "red"), ("blue", "blue"), ("tan", "tan")]
    cw, top, el = 106, 86, []
    for k, (key, cap) in enumerate(caps):
        pts, colr = PB[key]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        ox = k * cw + cw / 2.0 - (max(xs) + min(xs)) / 2
        oy = top / 2.0 + 2 - (max(ys) + min(ys)) / 2
        assert max(xs) - min(xs) <= cw - 8 and max(ys) - min(ys) <= top - 6
        el.append(poly_el([(x + ox, y + oy) for x, y in pts], colr, INK, 2))
        el.append("<text x='%d' y='%d' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                  % (k * cw + cw / 2, top + 20, INK, cap))
    return svg_wrap(cw * 4, top + 27, "".join(el), "four pattern blocks: yellow, red, blue and tan")


def hex_triangles_svg():
    hx = [(x + 62, y + 56) for x, y in regular(6, 52, 0)]
    el = [poly_el([(62, 56), hx[i], hx[(i + 1) % 6]], "#4fae74", INK, 2) for i in range(6)]
    return svg_wrap(125, 112, "".join(el), "a hexagon covered by green triangles")


# ------------------------------------------------------------ set 1: polygon or not?
Y, C, O, X = "Yes, it is a polygon", "No, it has a curve", "No, it is not closed", "No, two sides cross"
WHY = {"curve": C, "open": O, "cross": X}


def set_polygon(rnd, pos, Pp):
    its = []
    ask = ["Is this shape a polygon?", "Is this a polygon?"]
    yes = [
        (REG[6], 0, "It is closed and it has 6 straight sides that meet only at the corners, so it is a polygon."),
        (SQ, 45, "It is a square that has been turned. It is closed and has 4 straight sides, so it is a polygon. Turning a shape does not change that."),
        (TRI_S, 0, "It is closed and has 3 straight sides. Every triangle is a polygon."),
        (L_SH, 0, "It has 6 straight sides and it is closed. A polygon can have a corner that points in."),
        (STAR, 0, "The outline is 10 straight sides joined end to end. The sides do not cross, so the star is a polygon."),
        (ARROW, 0, "It is closed and every side is straight. The sides meet only at the corners, so it is a polygon."),
        (PENT_I, 0, "It is closed and has 5 straight sides. The sides do not need to be the same length."),
    ]
    for i, (sh, rot, e) in enumerate(yes):
        its.append(mcq(fig(shape_svg(sh, rot, marks=())) + ask[i % 2], Y, [C, O, X], e))
    no = [
        (CIRCLE, "A circle is one curved line. It has no straight sides, so it is not a polygon."),
        (OVAL, "An oval is curved all the way around. A polygon has only straight sides."),
        (SEMI, "The bottom is straight, but the top is curved. A polygon has only straight sides."),
        (RINK, "The corners are curved. Even one curve means it is not a polygon."),
        (CURVSIDE, "Three sides are straight, but the left side is curved. Every side of a polygon must be straight."),
        (GAPTRI, "There is a gap at the bottom, so the shape is not closed. A polygon must be closed."),
        (OPEN5, "The ends do not meet, so the shape is open. A polygon must be closed."),
        (BOWTIE, "Two sides cross in the middle. In a polygon the sides meet only at the corners."),
        (PENTAGRAM, "The lines cross each other inside the shape. In a polygon the sides meet only at the corners and never cross."),
    ]
    for i, (sh, e) in enumerate(no):
        its.append(mcq(fig(shape_svg(sh, 0)) + ask[i % 2], WHY[sh["why"]], [Y] + [w for w in (C, O, X) if w != WHY[sh["why"]]], e))
    p = pos.next()
    cells = [(CIRCLE, 0), (OPEN5, 0), (BOWTIE, 0)]
    cells.insert(p, (HEX_I, 0))
    its.append(mcq_fixed(fig(grid_svg(cells, marks=())) + "Which shape is a polygon?", list("ABCD"), "ABCD"[p],
                         "%s is closed and has 6 straight sides. The others have a curve, are open, or have sides that cross." % "ABCD"[p]))
    p = pos.next()
    cells = [(TRI_I, 0), (L_SH, 0), (HOUSE, 0)]
    cells.insert(p, (LEAF, 0))
    its.append(mcq_fixed(fig(grid_svg(cells, marks=())) + "Which shape is NOT a polygon?", list("ABCD"), "ABCD"[p],
                         "%s is made of two curved lines, so it is not a polygon. The other three are closed and have only straight sides." % "ABCD"[p]))
    its.append(mcq("A polygon is a closed shape made of …", "straight sides only", ["curved sides only", "straight and curved sides", "exactly 4 sides"],
                   "A polygon is closed and all its sides are straight line segments. It can have 3 or more sides."))
    its.append(mcq("What is the smallest number of sides a polygon can have?", 3, [2, 4, 1],
                   "Two straight lines cannot close a shape. With 3 sides you get a triangle, the polygon with the fewest sides."))
    assert len(its) == 20, len(its)
    return {"title": "Polygon or not?", "items": its}


# ------------------------------------------------------------ set 2: name polygons by their sides
def set_name(rnd, pos, Pp):
    its = []
    ask = ["What is the name of this polygon?", "Name this polygon.", "What is this polygon called?"]
    plan = [
        (TRI_S, 200, ["quadrilateral", "pentagon", "hexagon"], "It has 3 sides, so it is a triangle."),
        (QUAD, 15, ["triangle", "pentagon", "hexagon"], "It has 4 sides, so it is a quadrilateral. Its sides are all different, but it still has 4."),
        (REG[5], 0, ["hexagon", "quadrilateral", "octagon"], "It has 5 sides, so it is a pentagon."),
        (HOUSE, 0, ["quadrilateral", "hexagon", "heptagon"],
         "Count the sides around the outside: 2 roof sides, 2 walls and the bottom. That is 5 sides, so it is a pentagon."),
        (REG[6], 0, ["pentagon", "octagon", "heptagon"], "It has 6 sides, so it is a hexagon."),
        (L_SH, 90, ["quadrilateral", "octagon", "pentagon"],
         "Go around the outside and count: 6 sides. It is a hexagon, even though it does not look like a honeycomb cell."),
        (REG[7], 0, ["hexagon", "octagon", "decagon"], "It has 7 sides, so it is a heptagon."),
        (ARROW, 0, ["hexagon", "pentagon", "octagon"],
         "Count every side, including the short ones beside the point: 7 sides. It is a heptagon."),
        (REG[8], 0, ["hexagon", "heptagon", "decagon"], "It has 8 sides, so it is an octagon. Octo means 8, like an octopus with 8 arms."),
        (T_SH, 0, ["hexagon", "heptagon", "quadrilateral"],
         "Mark the corner where you start, then count each side once: 8 sides. It is an octagon."),
        (REG[10], 0, ["octagon", "heptagon", "hexagon"], "It has 10 sides, so it is a decagon. Deca means 10."),
        (STAR, 0, ["pentagon", "octagon", "heptagon"],
         "The star has 5 points, but count the sides: 2 sides for each point, 5 × 2 = 10. It is a decagon."),
    ]
    for i, (sh, rot, wrong, e) in enumerate(plan):
        assert sh["f"]["name"] not in wrong
        its.append(mcq(fig(shape_svg(sh, rot, marks=())) + ask[i % 3], sh["f"]["name"], wrong, e))
    its.append(mcq("A polygon has 8 sides. What is it called?", "an octagon", ["a hexagon", "a heptagon", "a decagon"],
                   "8 sides make an octagon. A stop sign is an octagon."))
    its.append(mcq("How many sides does a heptagon have?", 7, [6, 8, 5],
                   "A heptagon has 7 sides. Hexagon is 6, heptagon is 7, octagon is 8."))
    its.append(mcq("How many sides does a decagon have?", 10, [12, 8, 9], "Deca means 10, so a decagon has 10 sides."))
    its.append(mcq("How many vertices does a hexagon have?", 6, [12, 5, 7],
                   "A polygon has the same number of vertices (corners) as sides. A hexagon has 6 sides and 6 vertices."))
    n, he, his = Pp.next()
    its.append(mcq("%s counts the vertices of a polygon. There are 5. How many sides does it have?" % n, 5, [4, 6, 10],
                   "Each side goes from one vertex to the next, so a polygon has as many sides as vertices: 5."))
    its.append(mcq("Which polygon has the most sides?", "decagon", ["octagon", "heptagon", "hexagon"],
                   "decagon 10, octagon 8, heptagon 7, hexagon 6. The decagon has the most."))
    n, he, his = Pp.next()
    its.append(mcq("%s says, “A pentagon has 6 sides.” What is the mistake?" % n,
                   "A pentagon has 5 sides", ["A pentagon has 4 sides", "A pentagon has 8 sides", "There is no mistake"],
                   "Penta means 5. A pentagon has 5 sides. A shape with 6 sides is a hexagon."))
    p = pos.next()
    cells = [(L_SH, 0), (T_SH, 0), (HOUSE, 0)]
    cells.insert(p, (ARROW, 0))
    its.append(mcq_fixed(fig(grid_svg(cells, marks=())) + "Which shape is a heptagon?", list("ABCD"), "ABCD"[p],
                         "%s has 7 sides. The others have 6, 8 and 5 sides." % "ABCD"[p]))
    assert len(its) == 20, len(its)
    return {"title": "Name polygons by their sides", "items": its}


# ------------------------------------------------------------ set 3: regular or irregular?
RG, IA, IS, IB = "Regular", "Irregular: angles not equal", "Irregular: sides not equal", "Irregular: sides and angles not equal"


def reg_answer(f):
    if f["regular"]:
        return RG
    if f["eqs"]:
        return IA
    if f["eqa"]:
        return IS
    return IB


def set_regular(rnd, pos, Pp):
    its = []
    note = "Same marks mean equal sides or equal angles. "
    asks = ["Is this polygon regular or irregular?", "Regular or irregular?"]
    plan = [
        (SQ, 20, "All 4 sides are equal and all 4 angles are right angles, so the square is a regular quadrilateral."),
        (REG[3], 0, "All 3 sides are equal and all 3 angles are equal, so it is a regular triangle."),
        (REG[5], 0, "All 5 sides are equal and all 5 angles are equal, so it is a regular pentagon."),
        (REG[6], 0, "All 6 sides are equal and all 6 angles are equal, so it is a regular hexagon."),
        (REG[8], 0, "All 8 sides are equal and all 8 angles are equal, so it is a regular octagon."),
        (RHOM, 0, "The 4 sides are equal, but 2 angles are narrow and 2 are wide. Equal sides alone do not make a polygon regular. "
                  "This rhombus is irregular."),
        (EQHEX, 0, "All 6 sides are equal, but the angles are not all the same size, so the hexagon is irregular."),
        (RECT, 0, "All 4 angles are right angles, but the long sides and the short sides are different. The rectangle is irregular."),
        (ALTHEX, 0, "All 6 angles are equal, but 3 sides are long and 3 are short, so the hexagon is irregular."),
        (CUTOCT, 0, "All 8 angles are equal, but 4 sides are long and 4 are short, so the octagon is irregular."),
        (TRI_R, 0, "The 3 sides are different lengths and only one angle is a right angle, so the triangle is irregular."),
        (KITE, 0, "Two sides are short and two are long, and the angles are different sizes, so it is irregular."),
        (HOUSE, 0, "The sides are different lengths, and 2 angles are right angles while the others are wider. It is an irregular pentagon."),
        (ITRAP, 0, "The top and bottom are different lengths, and the angles at the top are wider than at the bottom. The trapezoid is irregular."),
    ]
    for i, (sh, rot, e) in enumerate(plan):
        ans = reg_answer(sh["f"])
        its.append(mcq(fig(shape_svg(sh, rot)) + note + asks[i % 2], ans, [w for w in (RG, IA, IS, IB) if w != ans], e))
    cnt = {}
    for sh, _, _ in plan:
        cnt[reg_answer(sh["f"])] = cnt.get(reg_answer(sh["f"]), 0) + 1
    assert cnt == {RG: 5, IA: 2, IS: 3, IB: 4}, cnt
    its.append(mcq("A regular polygon has …", "all sides equal and all angles equal",
                   ["all sides equal", "all angles equal", "4 equal sides"],
                   "A polygon is regular only when all its sides are equal AND all its angles are equal."))
    its.append(mcq("A rhombus that is not a square has 4 equal sides. Is it regular?", "No, its angles are not all equal",
                   ["Yes, its sides are all equal", "Yes, it has 4 sides", "No, it has a curve"],
                   "Its sides are equal, but 2 angles are wide and 2 are narrow. A regular polygon needs equal angles too."))
    its.append(mcq("A rectangle that is not a square has 4 right angles. Is it regular?", "No, its sides are not all equal",
                   ["Yes, all its angles are equal", "Yes, it has 4 sides", "No, it has no right angles"],
                   "Its angles are equal, but the long sides and short sides are different. A regular polygon needs equal sides too."))
    its.append(mcq("What do we call a regular quadrilateral?", "a square", ["a rhombus", "a rectangle", "a trapezoid"],
                   "A square has 4 equal sides and 4 equal angles (right angles). It is the only regular quadrilateral."))
    p = pos.next()
    cells = [(RHOM, 0), (RECT, 0), (KITE, 0)]
    cells.insert(p, (REG[6], 0))
    its.append(mcq_fixed(fig(grid_svg(cells)) + "Which polygon is regular?", list("ABCD"), "ABCD"[p],
                         "%s has 6 equal sides and 6 equal angles. The rhombus has unequal angles, the rectangle has unequal sides, "
                         "and the kite has neither." % "ABCD"[p]))
    p = pos.next()
    cells = [(REG[5], 0), (SQ, 0), (REG[3], 0)]
    cells.insert(p, (RHOM, 30))
    its.append(mcq_fixed(fig(grid_svg(cells)) + "Which polygon is irregular?", list("ABCD"), "ABCD"[p],
                         "%s is a rhombus. Its sides are equal, but its angles are not. The other three are regular." % "ABCD"[p]))
    assert len(its) == 20, len(its)
    return {"title": "Regular or irregular?", "items": its}


# ------------------------------------------------------------ set 4: sort polygons (Venn diagrams)
def venn_e(l1, l2, sh, letter, what):
    f = sh["f"]
    a, b = CRIT[l1](f), CRIT[l2](f)
    part = {"A": "It fits “%s” but not “%s”, so it goes in A." % (l1, l2),
            "B": "It fits both “%s” and “%s”, so it goes in the middle, B." % (l1, l2),
            "C": "It fits “%s” but not “%s”, so it goes in C." % (l2, l1),
            "D": "It fits neither “%s” nor “%s”, so it goes outside both circles, D." % (l1, l2)}[letter]
    return what + " " + part


def set_sort(rnd, pos, Pp):
    its = []
    plan = [
        ("Regular", "4 sides", SQ, 0, "It is a square: 4 equal sides and 4 equal angles."),
        ("Regular", "4 sides", REG[6], 0, "It is a regular hexagon. It has 6 sides, not 4."),
        ("Regular", "4 sides", RECT, 0, "It is a rectangle: 4 sides, but the sides are not all equal, so it is not regular."),
        ("Regular", "4 sides", TRI_S, 0, "It is a triangle with sides of different lengths: not regular and not 4 sides."),
        ("All sides equal", "All angles equal", RHOM, 30, "It is a rhombus: equal sides, but 2 wide and 2 narrow angles."),
        ("All sides equal", "All angles equal", REG[5], 0, "It is a regular pentagon: equal sides and equal angles."),
        ("All sides equal", "All angles equal", CUTOCT, 0, "Its 8 angles are equal, but it has long sides and short sides."),
        ("All sides equal", "All angles equal", KITE, 0, "It is a kite shape. Its sides are not all equal and its angles are not all equal."),
        ("Has a right angle", "Regular", L_SH, 0, "It has right angles, but its sides are different lengths, so it is not regular."),
        ("Has a right angle", "Regular", SQ, 30, "It is a turned square. It has 4 right angles and it is regular."),
        ("Has a right angle", "Regular", REG[3], 0, "It is a regular triangle. Its angles are equal, and none is a right angle."),
        ("Has a right angle", "Regular", PARA, 0, "It is a parallelogram with no right angles. Its sides and angles are not all equal."),
    ]
    tally = {}
    for l1, l2, sh, rot, what in plan:
        letter = region(l1, l2, sh["f"])
        tally[letter] = tally.get(letter, 0) + 1
        its.append(mcq_fixed(fig(venn_svg(l1, l2, sh, rot)) + "Where does this shape go in the Venn diagram?",
                             list("ABCD"), letter, venn_e(l1, l2, sh, letter, what)))
    assert tally == {"A": 3, "B": 3, "C": 3, "D": 3}, tally
    grid_plan = [
        ("Regular", "4 sides", "B", [RHOM, RECT, REG[5]], SQ,
         "Which shape goes in the middle of a Venn diagram with the circles “Regular” and “4 sides”?",
         "is a square: it has 4 sides and it is regular. The rhombus and the rectangle are irregular, and the pentagon has 5 sides"),
        ("Regular", "Has a right angle", "D", [SQ, REG[6], RECT], PARA,
         "Which shape goes outside both circles of a Venn diagram with “Regular” and “Has a right angle”?",
         "is a parallelogram: it has no right angle and it is not regular. The square is in both circles, the hexagon is regular, and the rectangle has right angles"),
        ("All sides equal", "All angles equal", "A", [SQ, RECT, REG[3]], RHOM,
         "Which shape fits “All sides equal” but NOT “All angles equal”?",
         "is a rhombus. Its sides are equal, but its angles are not"),
        ("Triangle", "Regular", "B", [TRI_R, TRI_I, SQ], REG[3],
         "Which shape goes in the middle of a Venn diagram with “Triangle” and “Regular”?",
         "is a triangle with 3 equal sides and 3 equal angles. The other triangles are irregular, and the square is not a triangle"),
    ]
    for l1, l2, letter, others, right, q, why in grid_plan:
        assert region(l1, l2, right["f"]) == letter and all(region(l1, l2, o["f"]) != letter for o in others)
        p = pos.next()
        cells = [(o, 0) for o in others]
        cells.insert(p, (right, 0))
        its.append(mcq_fixed(fig(grid_svg(cells)) + q, list("ABCD"), "ABCD"[p], "%s %s." % ("ABCD"[p], why)))
    its.append(mcq("A Venn diagram has the circles “All sides equal” and “All angles equal”. What kind of polygons go in the middle?",
                   "regular polygons", ["rhombuses", "rectangles", "irregular polygons"],
                   "In the middle, a polygon has all sides equal AND all angles equal. That is what a regular polygon is."))
    n, he, his = Pp.next()
    its.append(mcq("%s puts these shapes in a group called “Regular”: a square, a regular triangle, a rhombus and a regular hexagon. "
                   "Which shape is in the wrong group?" % n, "the rhombus", ["the square", "the regular triangle", "the regular hexagon"],
                   "A rhombus that is not a square has equal sides but unequal angles, so it is irregular."))
    n, he, his = Pp.next()
    its.append(mcq("%s sorts shapes into “Quadrilaterals” and “Not quadrilaterals”. Which shape is NOT a quadrilateral?" % n,
                   "a hexagon", ["a trapezoid", "a rhombus", "a square"],
                   "A quadrilateral has 4 sides. A trapezoid, a rhombus and a square each have 4 sides. A hexagon has 6."))
    assert region("Has a right angle", "Regular", RECT["f"]) == "A"
    its.append(mcq("A Venn diagram has the circles “Has a right angle” and “Regular”. Where does a rectangle that is not a square go?",
                   "in “Has a right angle” only", ["in the middle", "in “Regular” only", "outside both circles"],
                   "A rectangle has 4 right angles, but its sides are not all equal, so it is not regular. It goes in “Has a right angle” only."))
    assert len(its) == 20, len(its)
    return {"title": "Sort polygons in Venn diagrams", "items": its}


# ------------------------------------------------------------ set 5: polygons in real life
def set_life(rnd, pos, Pp):
    its = []
    its.append(mcq(fig(stop_sign_svg()) + "A stop sign has 8 equal sides and 8 equal angles. What shape is it?",
                   "a regular octagon", ["an irregular octagon", "a regular hexagon", "a regular decagon"],
                   "8 sides make an octagon. The sides and angles are all equal, so it is a regular octagon."))
    its.append(mcq(fig(honeycomb_svg()) + "Bees build honeycomb cells shaped like regular hexagons. How many sides does each cell have?",
                   6, [8, 5, 7], "A hexagon has 6 sides. Each cell is a regular hexagon: 6 equal sides and 6 equal angles."))
    its.append(mcq(fig(yield_svg()) + "A yield sign is a triangle with 3 equal sides and 3 equal angles. Which word describes it?",
                   "regular", ["irregular", "quadrilateral", "open"],
                   "All sides are equal and all angles are equal, so the yield sign is a regular triangle."))
    its.append(mcq(fig(school_sign_svg()) + "A school zone sign in BC has this shape. It has 2 right angles at the bottom. What is it?",
                   "an irregular pentagon", ["a regular pentagon", "an irregular hexagon", "a regular hexagon"],
                   "It has 5 sides, so it is a pentagon. Its angles are not all equal (2 right angles and 3 wider angles), so it is irregular."))
    n, he, his = Pp.next()
    its.append(mcq(fig(rink_svg()) + "%s plays hockey at a rink in Kamloops. The rink has rounded corners. Is the outline of the rink a polygon?" % n,
                   "No, its corners are curved", ["Yes, it is a rectangle", "Yes, it has 4 sides", "No, it is too big"],
                   "A polygon has only straight sides. The rounded corners are curves, so the rink outline is not a polygon."))
    n, he, his = Pp.next()
    its.append(mcq("%s cuts a round pizza into 8 slices. Is one slice a polygon?" % n,
                   "No, the crust edge is curved", ["Yes, it is a triangle", "Yes, it has 3 corners", "No, it has 8 sides"],
                   "A slice has 2 straight cut edges, but the crust edge is curved. A polygon has only straight sides."))
    its.append(mcq(fig(pattern_blocks_svg()) + "Which pattern block is a regular polygon?", "the yellow hexagon",
                   ["the red trapezoid", "the blue rhombus", "the tan rhombus"],
                   "The yellow hexagon has 6 equal sides and 6 equal angles. The trapezoid has a long side, and the two rhombuses have unequal angles."))
    its.append(mcq("The red trapezoid pattern block has 3 short sides of the same length and 1 long side. Is it regular?",
                   "No, its sides are not all equal", ["Yes, 3 sides are equal", "Yes, it has 4 sides", "No, it has a curve"],
                   "One side is longer than the other three, so not all sides are equal. The trapezoid is irregular."))
    its.append(mcq(fig(hex_triangles_svg()) + "How many green triangle blocks cover one yellow hexagon block?", 6, [3, 2, 4],
                   "6 triangles fit around the centre of the hexagon. (3 is the number of blue rhombuses, and 2 is the number of red trapezoids.)"))
    n, he, his = Pp.next()
    its.append(mcq("%s's family builds a garden bed shaped like a regular hexagon in Kelowna. Each side is 2 m long. "
                   "How many metres of edging go all the way around?" % n, "12 m", ["8 m", "10 m", "14 m"],
                   "A regular hexagon has 6 equal sides: 6 × 2 m = 12 m."))
    n, he, his = Pp.next()
    its.append(mcq("%s draws a regular octagon. Each side is 4 cm. What is the distance all the way around?" % n,
                   "32 cm", ["24 cm", "28 cm", "12 cm"],
                   "A regular octagon has 8 equal sides: 8 × 4 cm = 32 cm."))
    n, he, his = Pp.next()
    its.append(mcq("%s flies a kite at Stanley Park. It has 4 straight sides: 2 short sides of 30 cm and 2 long sides of 50 cm. "
                   "Is the kite a regular polygon?" % n, "No, its sides are not all equal",
                   ["Yes, it has 4 sides", "Yes, it has 2 pairs of equal sides", "No, it has a curve"],
                   "A regular polygon has all sides equal. The kite has 30 cm and 50 cm sides, so it is irregular."))
    n, he, his = Pp.next()
    its.append(mcq("A window in %s's house in Victoria is a square. Is the window a regular polygon?" % n,
                   "Yes, 4 equal sides and 4 equal angles", ["No, it has right angles", "No, it has only 4 sides", "No, windows are not polygons"],
                   "A square has 4 equal sides and 4 right angles, which are equal angles. It is a regular polygon."))
    its.append(mcq("The flag of Canada is a rectangle twice as long as it is tall. Is its outline a regular polygon?",
                   "No, its sides are not all equal", ["Yes, all its angles are equal", "Yes, it has 4 sides", "No, it has no right angles"],
                   "The flag has 4 right angles, but the long sides are twice as long as the short sides. Equal angles alone do not make it regular."))
    its.append(mcq("A soccer ball has 12 patches shaped like pentagons. How many sides do the 12 pentagons have in all?",
                   60, [12, 17, 72], "Each pentagon has 5 sides: 12 × 5 = 60. (72 would be 12 × 6, for hexagons.)"))
    n, he, his = Pp.next()
    its.append(mcq("%s finds a metal nut shaped like a regular hexagon. How many equal angles does it have?" % n, 6, [4, 3, 12],
                   "A regular hexagon has 6 vertices, so it has 6 angles, and they are all equal."))
    n, he, his = Pp.next()
    its.append(mcq("%s draws a polygon with 5 sides. Every side is 3 cm, but the angles are not all equal. What did %s draw?" % (n, he),
                   "an irregular pentagon", ["a regular pentagon", "a regular hexagon", "an irregular hexagon"],
                   "5 sides make a pentagon. Equal sides are not enough: the angles must be equal too. It is irregular."))
    n, he, his = Pp.next()
    its.append(mcq("%s says, “A rectangle is regular because all 4 angles are right angles.” Is %s right?" % (n, he),
                   "No, the sides must be equal too", ["Yes, equal angles are enough", "Yes, all rectangles are regular",
                                                       "No, a rectangle has 5 sides"],
                   "A regular polygon needs equal sides AND equal angles. Only a square is a regular rectangle."))
    n, he, his = Pp.next()
    its.append(mcq("%s makes a sign for the Terry Fox Run. %s wants a regular polygon with 3 sides. What should %s cut out?" % (n, he.capitalize(), he),
                   "a triangle with 3 equal sides", ["a triangle with a right angle", "a square", "a triangle with 2 equal sides"],
                   "A regular triangle has 3 equal sides and 3 equal angles. It is also called an equilateral triangle."))
    its.append(mcq("A floor at a Surrey community centre is covered by regular hexagon tiles with no gaps. "
                   "Which other regular polygon can also cover a floor with no gaps?", "a square",
                   ["a regular pentagon", "a regular octagon", "a regular heptagon"],
                   "4 squares fit around a corner with no gaps. Regular pentagons, heptagons and octagons always leave gaps. "
                   "(Regular triangles work too.)"))
    assert len(its) == 20, len(its)
    return {"title": "Polygons in real life: word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    yes_no = strip_svg([(REG[6], 0, "polygon"), (L_SH, 0, "polygon"), (SEMI, 0, "curve"), (GAPTRI, 0, "open"), (BOWTIE, 0, "sides cross")],
                       "polygons and shapes that are not polygons", cw=112, bw=82, bh=72, marks=())
    names = strip_svg([(TRI_S, 0, "triangle 3"), (QUAD, 0, "quadrilateral 4"), (REG[5], 0, "pentagon 5"), (REG[6], 0, "hexagon 6")],
                      "a triangle, a quadrilateral, a pentagon and a hexagon", cw=146, bw=84, bh=72, marks=())
    names2 = strip_svg([(REG[7], 0, "heptagon 7"), (T_SH, 0, "octagon 8"), (REG[10], 0, "decagon 10")],
                       "a heptagon, an octagon and a decagon", cw=146, bw=84, bh=72, marks=())
    reg = strip_svg([(REG[6], 0, "regular"), (SQ, 0, "regular"), (RHOM, 0, "irregular"), (RECT, 0, "irregular")],
                    "a regular hexagon, a square, a rhombus and a rectangle with marks", cw=128, bw=96, bh=78)
    return (
        "<h2>What is a polygon?</h2>"
        "<p>A <b>polygon</b> is a flat, closed shape made of <b>straight sides</b>. The sides meet only at the corners, called "
        "<b>vertices</b>. A polygon can be any size, and it can be turned any way.</p>"
        "<figure class='sn-fig'>" + yes_no +
        "<figcaption>The first two are polygons. A shape with a curve, an open shape, and a shape whose sides cross are not polygons.</figcaption></figure>"
        "<h2>Name a polygon by its sides</h2>"
        "<p>Count the sides. A polygon has the same number of vertices as sides.</p>"
        "<figure class='sn-fig'>" + names + "</figure>"
        "<figure class='sn-fig'>" + names2 +
        "<figcaption>The name depends only on the number of sides, not on the size or the side lengths.</figcaption></figure>" +
        table(["Sides", "Name", "Remember it"], [
            ["3", "triangle", "tri = 3, like a tricycle"],
            ["4", "quadrilateral", "quad = 4"],
            ["5", "pentagon", "penta = 5"],
            ["6", "hexagon", "a honeycomb cell"],
            ["7", "heptagon", "hepta = 7"],
            ["8", "octagon", "octo = 8, like an octopus; a stop sign"],
            ["10", "decagon", "deca = 10"],
        ]) +
        ex("Example 1", "A star has 5 points. What kind of polygon is it?",
           "Do not count the points. Count the sides: each point has 2 sides, so 5 × 2 = 10.", "a decagon") +
        "<h2>Regular or irregular?</h2>"
        "<p>A polygon is <b>regular</b> when <b>all its sides are equal and all its angles are equal</b>. "
        "If even one side or one angle is different, the polygon is <b>irregular</b>.</p>"
        "<p>Marks help you check. Matching ticks show equal sides. A small square shows a right angle. Matching arcs show equal angles.</p>"
        "<figure class='sn-fig'>" + reg +
        "<figcaption>The rhombus has equal sides but unequal angles. The rectangle has equal angles but unequal sides. Both are irregular.</figcaption></figure>" +
        ex("Example 2", "Is a rhombus with 2 wide angles and 2 narrow angles regular?",
           "Its 4 sides are equal. Its angles are not equal. A regular polygon needs both.", "No, it is irregular") +
        "<h2>Sort polygons in a Venn diagram</h2>"
        "<p>A Venn diagram has two circles, each with a rule. A shape that fits both rules goes in the middle, where the circles overlap. "
        "A shape that fits neither rule goes outside both circles.</p>"
        "<figure class='sn-fig'>" + venn_lesson_svg() +
        "<figcaption>The rhombus has equal sides only. The rectangle has equal angles only. The square and the regular triangle fit both, so they are in the middle. "
        "The kite shape fits neither.</figcaption></figure>" +
        ex("Example 3", "The circles are “Regular” and “4 sides”. Where does a regular hexagon go?",
           "It is regular, so it is in the “Regular” circle. It has 6 sides, not 4, so it is not in the other circle.", "in “Regular” only") +
        "<h2>Polygons around you</h2>"
        "<p>A stop sign is a regular octagon. Honeycomb cells are regular hexagons. A yield sign is a regular triangle. "
        "A Canadian flag is a rectangle, so it is irregular. A hockey rink with rounded corners is not a polygon at all.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Calling a shape with a curve a polygon", "Every side must be straight. One curve means it is not a polygon"],
            ["Calling an open shape a polygon", "Check that the shape is closed with no gaps"],
            ["Equal sides means regular", "Check the angles too. A rhombus has equal sides but is not regular"],
            ["Equal angles means regular", "Check the sides too. A rectangle has equal angles but is not regular"],
            ["Missing a side or counting one twice", "Mark the vertex where you start and go around once"],
            ["Naming a star by its points", "Count the sides. A 5-point star has 10 sides"],
        ])
    )


FAQ = [
    {"q": "What is the difference between a regular and an irregular polygon?",
     "a": "A regular polygon has all sides equal and all angles equal, like a square or a stop sign. If any side or angle is different, the polygon is irregular."},
    {"q": "Is a rhombus a regular polygon?",
     "a": "Only when it is a square. A rhombus has 4 equal sides, but its angles are usually not equal, so most rhombuses are irregular."},
    {"q": "What do Grade 4 students learn about polygons in the BC curriculum?",
     "a": "In Geometry and measurement, Grade 4 students learn regular and irregular polygons: they describe, name, compare and sort polygons by their sides and angles."},
    {"q": "How can I help my child practise polygons at home?",
     "a": "Go on a shape hunt for signs, tiles and windows, count the sides together and ask whether all the sides and angles are equal. The 100 questions here also help with FSA numeracy practice."},
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
    rnd = random.Random(34811)
    Pp = People(rnd)
    pos = Pos(rnd)
    sets = [set_polygon(rnd, pos, Pp), set_name(rnd, pos, Pp), set_regular(rnd, pos, Pp), set_sort(rnd, pos, Pp), set_life(rnd, pos, Pp)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-4", "slug": "regular-and-irregular-polygons", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Regular and Irregular Polygons: Name, Compare and Sort",
        "seo_title": "Grade 4 Math Regular and Irregular Polygons Worksheets (BC Curriculum, Free, Answer Key)",
        "short_title": "Regular and irregular polygons",
        "domain": "Geometry and measurement",
        "standard_code": "Grade 4: Geometry and measurement",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/4/core",
        "standard_text": "Regular and irregular polygons",
        "meta_desc": "Free Grade 4 math worksheets on regular and irregular polygons for the BC curriculum: tell polygons from other shapes, "
                     "name them by their sides, check for equal sides and equal angles, sort them in Venn diagrams and find polygons in real life. "
                     "100 questions with an answer key, good for FSA numeracy practice.",
        "key_big": "A regular polygon has all sides equal AND all angles equal. If not, it is irregular.",
        "key_sub": "A polygon is a closed shape with straight sides that do not cross. Name it by counting its sides. "
                   "A rhombus has equal sides and a rectangle has equal angles, but neither is regular unless it is a square.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(four shapes labelled A to D|a Venn diagram|four pattern blocks)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
