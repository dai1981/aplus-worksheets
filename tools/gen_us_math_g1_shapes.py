# -*- coding: utf-8 -*-
"""
US Grade 1 Math: Shapes and Their Attributes (1.G.A.1, with 1.G.A.2)
  python tools/gen_us_math_g1_shapes.py
HTML attributes use single quotes (no backslashes in the JSON).

Words used everywhere (as in the lesson):
  side       one straight line of a flat shape
  corner     where 2 sides meet (also called a vertex; two or more are vertices)
  closed     the sides meet all the way around, with no gap
  square corner  a corner like the corner of a page
  shapes     circle, triangle, square, rectangle, trapezoid, hexagon (flat)
             cube, rectangular prism, cone, cylinder (solid; names only)
Defining attributes: closed, straight sides, number of sides and corners (and square corners
for squares and rectangles). Non-defining: color, size, turning.
To stay correct for every definition, a square is never offered as a wrong answer for
"rectangle", and "rectangle" or "trapezoid" is never a wrong answer for a square.
Every drawing is checked in code: side count, simple polygon, real square corners, equal sides
for squares, exactly one pair of parallel sides for trapezoids, and every piece of a composed
shape fits the outline with no gap or overlap (areas add up).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-1")
UPDATED = "2026-11-02"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
FONT = "Arial, Helvetica, sans-serif"
# (fill, line) pairs: color must never matter
COLS = [("#cfe6d6", "#006633"), ("#cfe0f3", "#1f5f99"), ("#fbe7a6", "#8a6100"),
        ("#f6cfd8", "#a33b5a"), ("#e2d6f0", "#5b3f8c")]
GREEN = COLS[0][1]
FILL, TOP, SIDE = "#cfe6d6", "#e6f2e9", "#a9d3b6"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ question helpers
def mcq(q, correct, cands, e):
    """correct + the first 3 unique distractors. Positions are set later by balance()."""
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
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fixed": True}


def balance(sets, rnd):
    """Exactly 5 correct answers in each position A-D in every set."""
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
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def cap(s):
    return s[0].upper() + s[1:]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def P(ps):
    return " ".join("%.1f,%.1f" % p for p in ps)


# ------------------------------------------------------------ geometry
def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def segs_cross(p1, p2, p3, p4):
    d1, d2 = cross(sub(p4, p3), sub(p1, p3)), cross(sub(p4, p3), sub(p2, p3))
    d3, d4 = cross(sub(p2, p1), sub(p3, p1)), cross(sub(p2, p1), sub(p4, p1))
    return d1 * d2 < 0 and d3 * d4 < 0


def corner_angles(pts):
    n = len(pts)
    out = []
    for i in range(n):
        u, v = sub(pts[i - 1], pts[i]), sub(pts[(i + 1) % n], pts[i])
        c = (u[0] * v[0] + u[1] * v[1]) / (math.hypot(*u) * math.hypot(*v))
        out.append(math.degrees(math.acos(max(-1, min(1, c)))))
    return out


def side_lens(pts):
    n = len(pts)
    return [math.hypot(*sub(pts[(i + 1) % n], pts[i])) for i in range(n)]


def area(pts):
    n = len(pts)
    return abs(sum(cross(pts[i], pts[(i + 1) % n]) for i in range(n))) / 2.0


def parallel(a, b, c, d):
    return abs(cross(sub(b, a), sub(d, c))) < 1e-6 * math.hypot(*sub(b, a)) * math.hypot(*sub(d, c))


def regular(n, r=60, start=-90):
    return [(r * math.cos(math.radians(start + 360.0 * i / n)), r * math.sin(math.radians(start + 360.0 * i / n)))
            for i in range(n)]


SIDES = {"triangle": 3, "square": 4, "rectangle": 4, "trapezoid": 4, "hexagon": 6, "slanted": 4}


def S(pts, kind):
    pts = [(float(x), float(y)) for x, y in pts]
    n = len(pts)
    assert SIDES[kind] == n, (kind, n)
    for i in range(n):
        for j in range(i + 2, n):
            if (j + 1) % n == i:
                continue
            assert not segs_cross(pts[i], pts[(i + 1) % n], pts[j], pts[(j + 1) % n]), ("sides cross", pts)
    A, L = corner_angles(pts), side_lens(pts)
    assert all(25 <= a <= 160 for a in A), ("corner too flat or too sharp", A)
    assert min(L) >= 0.2 * max(L), ("side too short", L)
    right = all(abs(a - 90) < 1e-6 for a in A)
    if kind == "square":
        assert right and max(L) - min(L) < 1e-6
    if kind == "rectangle":
        assert right and max(L) / min(L) > 1.4
    if kind == "trapezoid":
        pairs = [parallel(pts[0], pts[1], pts[2], pts[3]), parallel(pts[1], pts[2], pts[3], pts[0])]
        assert sum(pairs) == 1, ("trapezoid needs exactly 1 pair of parallel sides", pts)
    if kind == "slanted":                          # parallelogram with no square corners
        assert not right and min(abs(a - 90) for a in A) > 20
    return {"pts": pts, "n": n, "kind": kind}


CIRCLE = {"pts": [], "n": 0, "kind": "circle"}
TRI_EQ = S(regular(3), "triangle")
TRI_RIGHT = S([(0, 0), (0, 90), (120, 90)], "triangle")
TRI_WIDE = S([(0, 60), (150, 80), (40, 0)], "triangle")
TRI_TALL = S([(0, 130), (60, 130), (30, 0)], "triangle")
SQUARE = S([(0, 0), (100, 0), (100, 100), (0, 100)], "square")
RECT = S([(0, 0), (150, 0), (150, 70), (0, 70)], "rectangle")
RECT2 = S([(0, 0), (140, 0), (140, 70), (0, 70)], "rectangle")      # exactly 2 squares side by side
TRAP = S([(0, 80), (150, 80), (105, 0), (35, 0)], "trapezoid")
TRAP_R = S([(0, 0), (90, 0), (140, 80), (0, 80)], "trapezoid")
HEX_REG = S(regular(6, start=0), "hexagon")
HEX_LONG = S([(30, 0), (130, 0), (165, 45), (130, 90), (30, 90), (0, 45)], "hexagon")
PARA = S([(0, 70), (110, 70), (150, 0), (40, 0)], "slanted")


def rot_pt(p, deg):
    t = math.radians(deg)
    return (p[0] * math.cos(t) - p[1] * math.sin(t), p[0] * math.sin(t) + p[1] * math.cos(t))


def fit(pts, rot, bw, bh, cx, cy):
    """Rotate, scale (same both ways) to fit a bw x bh box, center at (cx, cy)."""
    pts = [rot_pt(p, rot) for p in pts]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    k = min(bw / (max(xs) - min(xs)), bh / (max(ys) - min(ys)))
    mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    return [(cx + (p[0] - mx) * k, cy + (p[1] - my) * k) for p in pts]


def bbox(pts, pad):
    return (min(p[0] for p in pts) - pad, min(p[1] for p in pts) - pad,
            max(p[0] for p in pts) + pad, max(p[1] for p in pts) + pad)


def shape_elems(sh, rot, bw, bh, cx, cy, sw=3, col=0):
    fill, line = COLS[col]
    if sh["kind"] == "circle":
        r = min(bw, bh) / 2.0
        el = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='%g'/>" % (cx, cy, r, fill, line, sw)]
        pad = r + sw / 2.0 + 1
        return el, (cx - pad, cy - pad, cx + pad, cy + pad)
    pts = fit(sh["pts"], rot, bw, bh, cx, cy)
    el = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>" % (P(pts), fill, line, sw)]
    return el, bbox(pts, sw / 2.0 + 1)


def open_elems(sh, rot, bw, bh, cx, cy, sw=3, col=0):
    """The sides drawn one after another, but the last side stops short: a clear gap at the first corner."""
    fill, line = COLS[col]
    pts = fit(sh["pts"], rot, bw, bh, cx, cy)
    a, b = pts[-1], pts[0]
    end = (a[0] + (b[0] - a[0]) * 0.55, a[1] + (b[1] - a[1]) * 0.55)
    gap = math.hypot(*sub(b, end))
    assert gap >= 18, gap
    el = ["<polyline points='%s' fill='none' stroke='%s' stroke-width='%g' stroke-linejoin='round' stroke-linecap='round'/>"
          % (P(pts + [end]), line, sw)]
    return el, bbox(pts, sw / 2.0 + 1)


def curved_elems(sh, rot, bw, bh, cx, cy, sw=3, col=0, bulge=0.22):
    """A triangle whose last side (corner 3 back to corner 1) is a curve bending out."""
    fill, line = COLS[col]
    p = sh["pts"]
    a, b = p[-1], p[0]
    m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    gx, gy = sum(q[0] for q in p) / len(p), sum(q[1] for q in p) / len(p)
    d = sub(m, (gx, gy))
    L = math.hypot(*sub(b, a))
    dl = math.hypot(*d)
    ctrl = (m[0] + d[0] / dl * L * bulge * 2, m[1] + d[1] / dl * L * bulge * 2)
    peak = (m[0] + d[0] / dl * L * bulge, m[1] + d[1] / dl * L * bulge)   # a quadratic curve reaches half way
    allp = fit(p + [ctrl, peak], rot, bw, bh, cx, cy)
    pts, c, pk = allp[:-2], allp[-2], allp[-1]
    path = "M%.1f,%.1f " % pts[0] + " ".join("L%.1f,%.1f" % q for q in pts[1:]) + " Q%.1f,%.1f %.1f,%.1f Z" % (c + pts[0])
    el = ["<path d='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>" % (path, fill, line, sw)]
    return el, bbox(pts + [pk], sw / 2.0 + 1)


def fit_svg(make, label, pad=6):
    _, bb = make(0, 0)
    W, H = int(math.ceil(bb[2] - bb[0] + 2 * pad)), int(math.ceil(bb[3] - bb[1] + 2 * pad))
    if W == H:
        W += 1                                       # keep figures out of the larger 'square' print size
    cx = pad - bb[0] + (W - (bb[2] - bb[0] + 2 * pad)) / 2
    cy = pad - bb[1] + (H - (bb[3] - bb[1] + 2 * pad)) / 2
    el, bb2 = make(cx, cy)
    assert bb2[0] >= 0 and bb2[1] >= 0 and bb2[2] <= W and bb2[3] <= H, (label, bb2, W, H)
    return svg_wrap(W, H, "".join(el), label)


def shape_svg(sh, rot=0, bw=110, bh=80, col=0, label=None):
    return fit_svg(lambda cx, cy: shape_elems(sh, rot, bw, bh, cx, cy, col=col), label or "a " + sh["kind"])


CELL = 118


def grid_svg(cells, label):
    W = H = 2 * CELL
    el = ["<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, CELL, H - 4, GRAY),
          "<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, W - 4, CELL, GRAY)]
    for k, f in enumerate(cells):
        x0, y0 = (k % 2) * CELL, (k // 2) * CELL
        e, bb = f(x0 + 66, y0 + 65)
        assert bb[0] >= x0 + 20 and bb[1] >= y0 + 5 and bb[2] <= x0 + CELL - 3 and bb[3] <= y0 + CELL - 3, (label, k, bb)
        el += e
        el.append(text(x0 + 7, y0 + 22, "ABCD"[k], 18, "start"))
    return svg_wrap(W, H, "".join(el), label)


def flat(sh, rot=0, size=80, col=0, how=None):
    f = {None: shape_elems, "open": open_elems, "curved": curved_elems}[how]
    size = min(size, 84)                             # fits a grid cell next to its letter
    return lambda cx, cy: f(sh, rot, size, size, cx, cy, sw=2.6, col=col)


def pair_svg(a, b, label="shape A and shape B"):
    """Two flat shapes side by side. a, b: draw functions f(cx, cy)."""
    W, H = 2 * CELL, CELL
    el = ["<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, CELL, H - 4, GRAY)]
    for k, f in enumerate([a, b]):
        x0 = k * CELL
        e, bb = f(x0 + 66, 64)
        assert bb[0] >= x0 + 20 and bb[1] >= 3 and bb[2] <= x0 + CELL - 3 and bb[3] <= H - 3, (label, bb)
        el += e
        el.append(text(x0 + 7, 22, "AB"[k], 18, "start"))
    return svg_wrap(W, H, "".join(el), label)


def grid_q(rnd, q, items, ans, why, target, label="four shapes labeled A to D", word="Shape"):
    rest = [f for i, f in enumerate(items) if i != ans]
    rnd.shuffle(rest)
    cells = rest[:target] + [items[ans]] + rest[target:]
    L = "ABCD"[target]
    return mcq_fixed(fig(grid_svg(cells, label)) + q, ["A", "B", "C", "D"], L, "%s %s %s" % (word, L, why))


# ------------------------------------------------------------ composed shapes (pieces shown with dashed lines)
H3 = math.sqrt(3) / 2


def C(outline, pieces, cuts, label, circle=False):
    """outline: polygon; pieces: polygons that must exactly fill it; cuts: dashed inside lines."""
    if not circle:
        tot = area(outline)
        assert abs(sum(area(p) for p in pieces) - tot) < 1e-6 * tot, label
        # every piece corner lies inside or on the outline (no piece sticks out)
        xs, ys = [p[0] for p in outline], [p[1] for p in outline]
        for pc in pieces:
            for q in pc:
                assert min(xs) - 1e-9 <= q[0] <= max(xs) + 1e-9 and min(ys) - 1e-9 <= q[1] <= max(ys) + 1e-9
        # every cut runs along a side of some piece
        for a, b in cuts:
            ok = False
            for pc in pieces:
                n = len(pc)
                for i in range(n):
                    u, v = pc[i], pc[(i + 1) % n]
                    on = abs(cross(sub(v, u), sub(a, u))) < 1e-9 and abs(cross(sub(v, u), sub(b, u))) < 1e-9
                    if on:
                        ok = True
            assert ok, (label, a, b)
    return {"outline": outline, "pieces": pieces, "cuts": cuts, "label": label, "circle": circle}


def comp_elems(cp, bw, bh, cx, cy, col=0, sw=3):
    fill, line = COLS[col]
    if cp["circle"]:
        r = min(bw, bh) / 2.0
        el = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='%g'/>" % (cx, cy, r, fill, line, sw),
              "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.2' stroke-dasharray='6 5'/>"
              % (cx - r, cy, cx + r, cy, line)]
        pad = r + sw / 2.0 + 1
        return el, (cx - pad, cy - pad, cx + pad, cy + pad)
    allp = list(cp["outline"]) + [q for ab in cp["cuts"] for q in ab]
    T = fit(allp, 0, bw, bh, cx, cy)
    n = len(cp["outline"])
    out = T[:n]
    el = ["<polygon points='%s' fill='%s' stroke='none'/>" % (P(out), fill)]
    for i in range(len(cp["cuts"])):
        a, b = T[n + 2 * i], T[n + 2 * i + 1]
        el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.2' stroke-dasharray='6 5'/>"
                  % (a + b + (line,)))
    el.append("<polygon points='%s' fill='none' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>" % (P(out), line, sw))
    return el, bbox(out, sw / 2.0 + 1)


def comp_svg(cp, bw=120, bh=80, col=0):
    return fit_svg(lambda cx, cy: comp_elems(cp, bw, bh, cx, cy, col), cp["label"])


def comp(cp, size=80, col=0):
    return lambda cx, cy: comp_elems(cp, size, size, cx, cy, col, sw=2.6)


def hexv(i):
    """Corners of a hexagon with a flat top: i = 0 right, then going clockwise on the screen."""
    a = math.radians(60 * i)
    return (round(math.cos(a), 12), round(math.sin(a), 12))


HV = [hexv(i) for i in range(6)]        # 0 right, 1 bottom-right, 2 bottom-left, 3 left, 4 top-left, 5 top-right
O = (0.0, 0.0)
SQ = [(0, 0), (1, 0), (1, 1), (0, 1)]
C_RECT2SQ = C([(0, 0), (2, 0), (2, 1), (0, 1)], [SQ, [(1, 0), (2, 0), (2, 1), (1, 1)]], [((1, 0), (1, 1))],
              "rectangle made of 2 squares")
C_SQ2TRI = C(SQ, [[(0, 1), (1, 0), (1, 1)], [(0, 0), (1, 0), (0, 1)]], [((0, 1), (1, 0))], "square made of 2 triangles")
C_RECT2TRI = C([(0, 0), (2, 0), (2, 1), (0, 1)], [[(0, 0), (2, 0), (0, 1)], [(2, 0), (2, 1), (0, 1)]],
               [((0, 1), (2, 0))], "rectangle made of 2 triangles")
C_HEX6 = C(HV, [[O, HV[i], HV[(i + 1) % 6]] for i in range(6)], [(HV[i], HV[i + 3]) for i in range(3)],
           "hexagon made of triangles")
C_HEX2TRAP = C(HV, [[HV[0], HV[1], HV[2], HV[3]], [HV[3], HV[4], HV[5], HV[0]]], [(HV[3], HV[0])],
               "hexagon made of 2 trapezoids")
C_TRAP3 = C([(0, H3), (2, H3), (1.5, 0), (0.5, 0)],
            [[(0, H3), (1, H3), (0.5, 0)], [(0.5, 0), (1, H3), (1.5, 0)], [(1, H3), (2, H3), (1.5, 0)]],
            [((0.5, 0), (1, H3)), ((1, H3), (1.5, 0))], "trapezoid made of triangles")
C_HEXMIX = C(HV, [[HV[0], HV[1], HV[2], HV[3]], [O, HV[3], HV[4]], [O, HV[4], HV[5]], [O, HV[5], HV[0]]],
             [(HV[3], HV[0]), (O, HV[4]), (O, HV[5])], "hexagon made of a trapezoid and triangles")
C_SQ4 = C([(0, 0), (2, 0), (2, 2), (0, 2)],
          [[(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)] for x in (0, 1) for y in (0, 1)],
          [((1, 0), (1, 2)), ((0, 1), (2, 1))], "big square made of small squares")
C_RECT3SQ = C([(0, 0), (3, 0), (3, 1), (0, 1)], [[(x, 0), (x + 1, 0), (x + 1, 1), (x, 1)] for x in range(3)],
              [((1, 0), (1, 1)), ((2, 0), (2, 1))], "rectangle made of squares")
C_HOUSE = C([(0, 0.6), (0.5, 0), (1, 0.6), (1, 1.6), (0, 1.6)],
            [[(0, 0.6), (0.5, 0), (1, 0.6)], [(0, 0.6), (1, 0.6), (1, 1.6), (0, 1.6)]], [((0, 0.6), (1, 0.6))],
            "house made of 2 shapes")
M1, M2, M3 = (0.5, 0), (1.5, 0), (1, H3)
C_TRI4 = C([(0, H3 * 2), (2, H3 * 2), (1, 0)],
           [[(1, 0), (0.5, H3), (1.5, H3)], [(0.5, H3), (0, 2 * H3), (1, 2 * H3)], [(1.5, H3), (1, 2 * H3), (2, 2 * H3)],
            [(0.5, H3), (1.5, H3), (1, 2 * H3)]],
           [((0.5, H3), (1.5, H3)), ((0.5, H3), (1, 2 * H3)), ((1.5, H3), (1, 2 * H3))], "big triangle made of small triangles")
C_HALVES = C([], [], [], "circle made of 2 halves", circle=True)
C_TRAPSQ = C([(0, 1), (3, 1), (2, 0), (1, 0)],
             [[(0, 1), (1, 1), (1, 0)], [(1, 0), (2, 0), (2, 1), (1, 1)], [(2, 0), (3, 1), (2, 1)]],
             [((1, 0), (1, 1)), ((2, 0), (2, 1))], "trapezoid made of 3 shapes")
C_SQVERT = C(SQ, [[(0, 0), (0.5, 0), (0.5, 1), (0, 1)], [(0.5, 0), (1, 0), (1, 1), (0.5, 1)]], [((0.5, 0), (0.5, 1))],
             "square made of 2 rectangles")
C_TRIHALF = C([(0, 1), (1, 1), (0.5, 0)], [[(0, 1), (0.5, 1), (0.5, 0)], [(0.5, 1), (1, 1), (0.5, 0)]],
              [((0.5, 0), (0.5, 1))], "triangle made of 2 triangles")


def hexgap_elems(bw, bh, cx, cy, col=0, sw=2.6, have=4):
    """A hexagon outline (dashed) with only some of its 6 triangles put in."""
    fill, line = COLS[col]
    T = fit(HV + [O], 0, bw, bh, cx, cy)
    hv, c = T[:6], T[6]
    el = ["<polygon points='%s' fill='#ffffff' stroke='%s' stroke-width='2' stroke-dasharray='6 5'/>" % (P(hv), line)]
    for i in range(6):                               # dashed lines show where each missing triangle goes
        el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2' stroke-dasharray='6 5'/>"
                  % (c + hv[i] + (line,)))
    for i in range(have):
        el.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>"
                  % (P([c, hv[(i + 2) % 6], hv[(i + 3) % 6]]), fill, line, sw))
    return el, bbox(hv, sw / 2.0 + 1)


# ------------------------------------------------------------ solids
def box_geom(w, h, d, ang=38):
    dx, dy = d * math.cos(math.radians(ang)), d * math.sin(math.radians(ang))
    assert dx < w and dy < h
    f = [(0, 0), (w, 0), (w, h), (0, h)]
    b = [(x + dx, y - dy) for x, y in f]
    pts = f + b
    edges = []
    for i in range(4):
        edges += [(i, (i + 1) % 4), (4 + i, 4 + (i + 1) % 4), (i, 4 + i)]
    edges = [(i, j, 7 in (i, j)) for i, j in edges]
    faces = [([0, 1, 2, 3], FILL), ([0, 1, 5, 4], TOP), ([1, 5, 6, 2], SIDE)]
    assert len(edges) == 12 and sum(1 for e in edges if e[2]) == 3
    return pts, edges, faces


def box_elems(geom, bw, bh, cx, cy, sw=2.6):
    pts, edges, faces = geom
    T = fit(pts, 0, bw, bh, cx, cy)
    el = []
    for idx, colr in faces:
        el.append("<polygon points='%s' fill='%s' stroke='none'/>" % (P([T[i] for i in idx]), colr))
    for i, j, hidden in edges:
        if hidden:
            el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.8' stroke-dasharray='6 5'/>"
                      % (T[i] + T[j] + (GREEN,)))
    for i, j, hidden in edges:
        if not hidden:
            el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g' stroke-linecap='round'/>"
                      % (T[i] + T[j] + (GREEN, sw)))
    return el, bbox(T, sw / 2.0 + 1)


CUBE = box_geom(70, 70, 40)
PRISM = box_geom(120, 55, 45)


def round_solid(kind, bw, bh, cx, cy, sw=2.6):
    """Cylinder or cone, seen a little from above. The back half of the bottom circle is dashed."""
    rx, ry, h = 40.0, 13.0, 84.0
    k = min(bw / (2 * rx), bh / (h + 2 * ry))
    rx, ry, h = rx * k, ry * k, h * k
    top, bot = cy - h / 2, cy + h / 2
    L, R = cx - rx, cx + rx
    front = "M%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f" % (L, bot, rx, ry, R, bot)
    back = "M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f" % (L, bot, rx, ry, R, bot)
    el = []
    if kind == "cylinder":
        el.append("<path d='M%.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f L%.1f,%.1f Z' fill='%s' stroke='none'/>"
                  % (L, top, L, bot, rx, ry, R, bot, R, top, SIDE))
        el.append("<path d='%s' fill='none' stroke='%s' stroke-width='1.8' stroke-dasharray='6 5'/>" % (back, GREEN))
        el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g'/>" % (L, top, L, bot, GREEN, sw))
        el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g'/>" % (R, top, R, bot, GREEN, sw))
        el.append("<path d='%s' fill='none' stroke='%s' stroke-width='%g'/>" % (front, GREEN, sw))
        el.append("<ellipse cx='%.1f' cy='%.1f' rx='%.1f' ry='%.1f' fill='%s' stroke='%s' stroke-width='%g'/>"
                  % (cx, top, rx, ry, TOP, GREEN, sw))
        yt = top - ry
    else:
        ax, ay = cx, top - ry                       # the point
        el.append("<path d='M%.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f Z' fill='%s' stroke='none'/>"
                  % (ax, ay, L, bot, rx, ry, R, bot, SIDE))
        el.append("<path d='%s' fill='none' stroke='%s' stroke-width='1.8' stroke-dasharray='6 5'/>" % (back, GREEN))
        el.append("<path d='M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f' fill='none' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>"
                  % (L, bot, ax, ay, R, bot, GREEN, sw))
        el.append("<path d='%s' fill='none' stroke='%s' stroke-width='%g'/>" % (front, GREEN, sw))
        yt = ay
    pad = sw / 2.0 + 1
    return el, (L - pad, yt - pad, R + pad, bot + ry + pad)


def solid(kind, size=80):
    if kind == "cube":
        return lambda cx, cy: box_elems(CUBE, size, size, cx, cy, sw=2.3)
    if kind == "prism":
        return lambda cx, cy: box_elems(PRISM, size, size, cx, cy, sw=2.3)
    return lambda cx, cy: round_solid(kind, size, size, cx, cy, sw=2.3)


def solid_svg(kind, label, bw=95, bh=88):
    f = {"cube": lambda cx, cy: box_elems(CUBE, bw, bh, cx, cy), "prism": lambda cx, cy: box_elems(PRISM, bw, bh, cx, cy),
         "cylinder": lambda cx, cy: round_solid("cylinder", bw, bh, cx, cy),
         "cone": lambda cx, cy: round_solid("cone", bw, bh, cx, cy)}[kind]
    return fit_svg(f, label)


# ============================================================ set 1: name the shape
NAME_WRONG = {
    "circle": ["square", "triangle", "hexagon"],
    "triangle": ["trapezoid", "square", "rectangle"],
    "square": ["triangle", "hexagon", "circle"],          # never "rectangle" or "trapezoid": a square is both
    "rectangle": ["square", "triangle", "hexagon"],
    "hexagon": ["trapezoid", "circle", "triangle"],
    "trapezoid": ["triangle", "rectangle", "hexagon"],
}
RULE = {
    "circle": "It is round and has no sides and no corners. It is a <b>circle</b>.",
    "triangle": "It has 3 straight sides and 3 corners. It is a <b>triangle</b>.",
    "square": "It has 4 sides that are all the same length and 4 square corners. It is a <b>square</b>.",
    "rectangle": "It has 4 sides and 4 square corners. 2 sides are long and 2 are short. It is a <b>rectangle</b>.",
    "hexagon": "Count the sides: 6. A shape with 6 sides is a <b>hexagon</b>.",
    "trapezoid": "It has 4 sides. 2 sides go the same way, like train tracks, and one of them is longer. It is a <b>trapezoid</b>.",
}


def set_name(rnd, PP):
    its = []
    plan = [  # shape, turn, box w, box h, color, note
        (CIRCLE, 0, 76, 76, 1, ""), (TRI_EQ, 0, 100, 80, 0, ""), (SQUARE, 0, 76, 76, 2, ""), (RECT, 0, 120, 70, 3, ""),
        (HEX_REG, 0, 100, 80, 4, ""), (TRAP, 0, 120, 70, 1, ""), (CIRCLE, 0, 34, 34, 2, " Small or big, it is still a circle."),
        (TRI_RIGHT, 200, 100, 80, 3, " It is turned, but it is still a triangle."),
        (SQUARE, 45, 86, 86, 0, " It is standing on a corner. Some people call it a diamond, but turning does not change the shape."),
        (RECT, 90, 100, 90, 4, " It is standing up, but it is still a rectangle."),
        (TRAP, 180, 120, 70, 2, " It is upside down, but it is still a trapezoid."),
        (HEX_LONG, 0, 120, 70, 3, " The sides are not all the same length. It is still a hexagon."),
        (TRI_TALL, 180, 70, 90, 1, " It points down, but it is still a triangle."),
        (TRAP_R, 0, 110, 70, 0, " It does not have to look the same on both sides."),
        (RECT, 25, 110, 80, 1, " It is tilted, but it is still a rectangle."),
        (SQUARE, 0, 36, 36, 4, " It is small, but it is still a square."),
    ]
    for sh, rot, bw, bh, col, note in plan:
        k = sh["kind"]
        its.append(mcq(fig(shape_svg(sh, rot, bw, bh, col, "a " + k)) + "What is the name of this shape?",
                       k, NAME_WRONG[k], RULE[k] + note))
    its.append(grid_q(rnd, "Which shape is a rectangle?",
                      [flat(RECT, 90, 80, 3), flat(PARA, 0, 84, 1), flat(TRAP, 0, 84, 2), flat(TRI_WIDE, 0, 84, 4)], 0,
                      "has 4 sides and 4 square corners. It is standing up, and that is fine. "
                      "The slanted shape has 4 sides, but its corners are not square corners.", 1))
    its.append(grid_q(rnd, "Which shape is a hexagon?",
                      [flat(HEX_REG, 30, 74, 0), flat(TRAP, 0, 84, 3), flat(CIRCLE, 0, 70, 1), flat(SQUARE, 0, 66, 2)], 0,
                      "has 6 sides. A trapezoid is like half of a hexagon, but it has only 4 sides.", 3))
    its.append(mcq("I have 6 sides. I have 6 corners. What shape am I?", "hexagon", ["trapezoid", "triangle", "rectangle"],
                   "A shape with 6 sides and 6 corners is a <b>hexagon</b>."))
    its.append(mcq("I am round. I have no sides and no corners. What shape am I?", "circle", ["square", "triangle", "hexagon"],
                   "A round shape with no sides and no corners is a <b>circle</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Name the shape", "items": its}


# ============================================================ set 2: count sides and corners
def set_count(rnd, PP):
    its = []
    plan = [
        (TRI_EQ, 0, 1, "sides", [2, 4, 6]), (SQUARE, 0, 2, "corners", [3, 5, 8]), (RECT, 0, 3, "sides", [2, 5, 3]),
        (TRI_RIGHT, 60, 4, "corners", [4, 2, 6]), (HEX_REG, 0, 0, "sides", [5, 7, 8]), (TRAP, 0, 1, "corners", [3, 5, 6]),
        (HEX_LONG, 20, 2, "corners", [5, 7, 4]), (TRAP_R, 0, 3, "sides", [3, 5, 2]), (SQUARE, 45, 4, "sides", [3, 5, 8]),
    ]
    for sh, rot, col, what, wrong in plan:
        n = sh["n"]
        w = "side" if what == "sides" else "corner"
        e = "Put your finger on one %s. Go around and count each %s once: <b>%d</b> %ss." % ("corner", w, n, w)
        if rot:
            e += " Turning a shape does not change how many %s it has." % what
        if sh["kind"] == "hexagon" and what == "sides":
            e += " If you get 5 or 7, you missed a side or counted one twice."
        if sh["kind"] == "rectangle":
            e += " Count the short sides too."
        its.append(mcq(fig(shape_svg(sh, rot, 110, 80, col, "a " + sh["kind"])) + "How many %s does this shape have?" % what,
                       n, wrong, e))
    its.append(mcq(fig(shape_svg(CIRCLE, 0, 70, 70, 1, "a circle")) + "How many corners does a circle have?", 0, [1, 2, 4],
                   "A circle is round all the way around. It has no straight sides, so it has <b>0</b> corners."))
    for sh, rot, col in [(HEX_REG, 30, 3), (TRI_WIDE, 0, 0)]:
        n = sh["n"]
        right = "%d sides, %d corners" % (n, n)
        wrong = ["%d sides, %d corners" % (n, n + 1), "%d sides, %d corners" % (n - 1, n - 1), "%d sides, %d corners" % (n + 1, n + 1)]
        its.append(mcq(fig(shape_svg(sh, rot, 110, 80, col, "a " + sh["kind"])) + "How many sides and corners does it have?",
                       right, wrong,
                       "Count the sides: %d. Count the corners: %d. A flat shape with straight sides has the same number of each. "
                       "If you get %d corners, you counted the first corner again." % (n, n, n + 1)))
    its.append(mcq(fig(pair_svg(flat(TRI_RIGHT, 0, 84, 3), flat(TRI_EQ, 180, 40, 1))) +
                   "Shape A is big. Shape B is small. Which one has more corners?",
                   "They are the same", ["A, it is bigger", "B, it is smaller", "You cannot tell"],
                   "Both are triangles. Each one has 3 corners. Size does not change the number of corners."))
    T = [0, 2, 1]
    its.append(grid_q(rnd, "Which shape has 6 sides?",
                      [flat(HEX_LONG, 0, 86, 2), flat(TRAP, 0, 86, 0), flat(SQUARE, 0, 66, 4), flat(TRI_EQ, 0, 80, 3)], 0,
                      "has 6 sides. It is a hexagon. The others have 4, 4 and 3 sides.", T[0]))
    its.append(grid_q(rnd, "Which shape has 3 corners?",
                      [flat(TRI_TALL, 150, 84, 4), flat(SQUARE, 30, 66, 1), flat(TRAP_R, 0, 84, 0), flat(CIRCLE, 0, 66, 2)], 0,
                      "has 3 corners, so it is a triangle, even though it is turned. A circle has no corners.", T[1]))
    its.append(grid_q(rnd, "Which shape has the most sides?",
                      [flat(HEX_REG, 0, 44, 1), flat(TRAP, 0, 88, 2), flat(TRI_RIGHT, 0, 86, 0), flat(RECT, 0, 88, 3)], 0,
                      "is the smallest shape, but it has the most sides: 6. Count the sides. Do not look at the size.", T[2]))
    its.append(mcq("A shape has 4 sides. How many corners does it have?", 4, [3, 5, 8],
                   "Each side ends at a corner. A flat shape has the same number of corners as sides: <b>4</b>."))
    its.append(mcq("A hexagon has 6 sides. A triangle has 3 sides. How many more sides does the hexagon have?", 3, [6, 9, 2],
                   "6 − 3 = <b>3</b>. The hexagon has 3 more sides."))
    its.append(mcq("How many corners do 2 triangles have in all?", 6, [3, 5, 4],
                   "Each triangle has 3 corners. 3 + 3 = <b>6</b> corners."))
    its.append(mcq("How many sides do a square and a triangle have in all?", 7, [6, 8, 1],
                   "A square has 4 sides. A triangle has 3 sides. 4 + 3 = <b>7</b> sides."))
    assert len(its) == 20, len(its)
    return {"title": "Count sides and corners", "items": its}


# ============================================================ set 3: what matters (defining attributes)
def set_matters(rnd, PP):
    its = []
    tri_q = "Is this a triangle?"
    its.append(mcq(fig(shape_svg(TRI_EQ, 0, 110, 96, 3, "a big triangle")) + tri_q, "Yes, 3 sides",
                   ["No, it is too big", "No, it has 4 sides", "No, it is open"],
                   "It is closed and has 3 straight sides. It is a triangle. Its size and color do not matter."))
    its.append(mcq(fig(fit_svg(lambda cx, cy: open_elems(TRI_EQ, 0, 100, 86, cx, cy, col=1), "three lines with a gap")) + tri_q,
                   "No, it is open", ["Yes, 3 sides", "No, it is small", "No, it has 4 sides"],
                   "Look at the corner with the gap. The sides do not meet, so the shape is open. A triangle must be closed."))
    its.append(mcq(fig(fit_svg(lambda cx, cy: curved_elems(TRI_EQ, 0, 100, 90, cx, cy, col=2), "shape with one curved side")) + tri_q,
                   "No, a side curves", ["Yes, 3 corners", "No, it is open", "No, it has 4 sides"],
                   "One side is curved. A triangle has 3 <b>straight</b> sides, so this is not a triangle."))
    its.append(mcq(fig(shape_svg(TRI_TALL, 180, 70, 90, 4, "a triangle pointing down")) + tri_q, "Yes, just turned",
                   ["No, it is upside down", "No, it is open", "No, it has 2 sides"],
                   "It has 3 straight sides and it is closed. It points down, but turning does not change the shape."))
    its.append(mcq(fig(shape_svg(TRI_WIDE, 0, 44, 30, 0, "a small triangle")) + tri_q, "Yes, 3 sides",
                   ["No, it is too small", "No, it is open", "No, it is a square"],
                   "It is small, but it is closed and has 3 straight sides. Small triangles are still triangles."))
    its.append(mcq(fig(shape_svg(TRAP, 0, 110, 70, 3, "a trapezoid")) + tri_q, "No, it has 4 sides",
                   ["Yes, it is closed", "Yes, 3 corners", "No, it is open"],
                   "Count the sides: 4. A triangle has only 3 sides. This shape is a trapezoid."))
    its.append(grid_q(rnd, "Which one is a triangle?",
                      [flat(TRI_RIGHT, 160, 80, 4), flat(TRI_EQ, 0, 80, 1, "open"), flat(TRI_EQ, 0, 84, 2, "curved"),
                       flat(TRAP, 0, 84, 0)], 0,
                      "is closed and has 3 straight sides. One shape is open, one has a curved side and one has 4 sides.", 2))
    its.append(grid_q(rnd, "Which one is NOT a triangle?",
                      [flat(TRI_TALL, 0, 84, 0, "open"), flat(TRI_EQ, 0, 84, 3), flat(TRI_RIGHT, 100, 46, 1), flat(TRI_WIDE, 0, 84, 4)], 0,
                      "is open: 2 sides do not meet. The other three are closed with 3 straight sides. "
                      "Their colors, sizes and turns do not matter.", 0))
    its.append(mcq(fig(pair_svg(flat(TRI_EQ, 0, 88, 3), flat(TRI_EQ, 180, 44, 1))) +
                   "Both shapes are triangles. What is different?", "color, size, turn",
                   ["number of sides", "number of corners", "one is open"],
                   "Both have 3 sides and 3 corners. Only the color, the size and the turn are different. These do not change the shape."))
    its.append(mcq(fig(shape_svg(SQUARE, 45, 86, 86, 2, "a square standing on a corner")) + "Is this a square?",
                   "Yes, just turned", ["No, it is a diamond", "No, it is tilted", "No, it is open"],
                   "It has 4 sides that are the same length and 4 square corners. It is a square standing on a corner."))
    its.append(mcq(fig(shape_svg(PARA, 0, 120, 70, 4, "a slanted shape with 4 sides")) + "Is this a rectangle?",
                   "No, no square corners", ["Yes, it has 4 sides", "Yes, it is long", "No, it is open"],
                   "It has 4 sides, but it leans over. Its corners are not square corners. A rectangle needs 4 square corners."))
    its.append(mcq(fig(fit_svg(lambda cx, cy: open_elems(SQUARE, 0, 76, 76, cx, cy, col=0), "four lines with a gap")) + "Is this a square?",
                   "No, it is open", ["Yes, 4 sides", "No, it is too big", "No, it is a triangle"],
                   "There is a gap at one corner. The sides do not all meet, so it is open. A square must be closed."))
    its.append(mcq(fig(pair_svg(flat(HEX_REG, 0, 86, 2), flat(HEX_LONG, 30, 56, 1))) + "Are shape A and shape B both hexagons?",
                   "Yes, 6 sides each", ["No, B is smaller", "No, B is longer", "No, not the same color"],
                   "Count the sides: A has 6 and B has 6. Both are hexagons. Size, color and side lengths do not matter."))
    its.append(mcq("Which one can change the name of a shape?", "the number of sides", ["its color", "its size", "turning it"],
                   "The name comes from the sides and corners. Color, size and turning never change the name."))
    nm, he, his = PP.next()
    its.append(mcq("%s colors a triangle blue. What shape is it now?" % nm, "still a triangle",
                   ["a new shape", "a blue square", "not a triangle"],
                   "Color does not change a shape. It still has 3 sides, so it is still a triangle."))
    a, b = PP.next(), PP.next()
    its.append(mcq("%s draws a big square. %s draws a small square. Are they both squares?" % (a[0], b[0]), "Yes, both",
                   ["Only the big one", "Only the small one", "You cannot tell"],
                   "Both have 4 same sides and 4 square corners. Size does not matter."))
    its.append(mcq("What does every triangle have?", "3 straight sides", ["a point on top", "3 same sides", "a flat bottom"],
                   "Every triangle is closed and has 3 straight sides. It can point any way, and its sides can be different lengths."))
    nm, he, his = PP.next()
    its.append(mcq("%s draws 3 straight lines. The ends do not all meet. Is it a triangle?" % nm, "No, it is open",
                   ["Yes, 3 lines", "Yes, if it is big", "No, it needs 4 lines"],
                   "The lines must meet at every corner to make a closed shape. With a gap, it is not a triangle."))
    nm, he, his = PP.next()
    its.append(mcq("%s turns a square on its corner. %s says it is a diamond now. Is %s right?" % (nm, cap(he), he),
                   "No, still a square", ["Yes, a diamond", "Yes, it turned", "No, a triangle"],
                   "Turning does not change a shape. It still has 4 same sides and 4 square corners. It is a square."))
    its.append(mcq("What does every rectangle have?", "4 square corners",
                   ["2 long sides", "a flat bottom", "the color green"],
                   "Every rectangle is closed with 4 sides and 4 square corners. It can stand up, lie down or be any color."))
    assert len(its) == 20, len(its)
    return {"title": "Is it a triangle? What matters", "items": its}


# ============================================================ set 4: put shapes together
def set_compose(rnd, PP):
    its = []
    cs = lambda cp, col, bw=120, bh=80: fig(comp_svg(cp, bw, bh, col))
    its.append(mcq(cs(C_RECT2SQ, 1) + "This rectangle is made of 2 of which shape?", "squares",
                   ["triangles", "circles", "hexagons"],
                   "Look at the dashed line. Each part has 4 same sides and 4 square corners. 2 <b>squares</b> make the rectangle."))
    its.append(mcq(cs(C_SQ2TRI, 2, 80, 80) + "This square is made of 2 of which shape?", "triangles",
                   ["squares", "rectangles", "trapezoids"],
                   "The dashed line goes from corner to corner. Each part has 3 sides. 2 <b>triangles</b> make the square."))
    its.append(mcq(cs(C_RECT2TRI, 3) + "Which 2 shapes make this rectangle?", "2 triangles",
                   ["2 squares", "2 rectangles", "2 circles"],
                   "The dashed line goes from corner to corner. Each part has 3 sides: <b>2 triangles</b>."))
    its.append(mcq(cs(C_HEX6, 4, 100, 90) + "How many triangles make this hexagon?", 6, [5, 7, 3],
                   "Count the triangles around the middle: <b>6</b>. (3 is the number of dashed lines, not triangles.)"))
    its.append(mcq(cs(C_HEX2TRAP, 0, 100, 90) + "This hexagon is made of 2 of which shape?", "trapezoids",
                   ["triangles", "squares", "rectangles"],
                   "Each half has 4 sides, and the long side is on the dashed line. 2 <b>trapezoids</b> make a hexagon."))
    its.append(mcq(cs(C_TRAP3, 1) + "How many triangles make this trapezoid?", 3, [2, 4, 1],
                   "Count the triangles: one points down in the middle, and one is on each side. That is <b>3</b>."))
    its.append(mcq(cs(C_HEXMIX, 2, 100, 90) + "Which shapes make this hexagon?", "1 trapezoid, 3 triangles",
                   ["2 trapezoids", "6 triangles", "4 triangles"],
                   "The bottom half has no lines inside: it is 1 trapezoid. The top half has 3 triangles."))
    its.append(mcq(cs(C_SQ4, 3, 80, 80) + "How many small squares make this big square?", 4, [2, 3, 6],
                   "There are 2 small squares on top and 2 on the bottom. 2 + 2 = <b>4</b>."))
    its.append(mcq(fig(shape_svg(RECT2, 0, 120, 60, 4, "a long rectangle")) + "Which 2 shapes can make this rectangle?",
                   "2 squares", ["2 circles", "2 hexagons", "1 square"],
                   "Put 2 squares side by side and you get a long rectangle. Circles and hexagons do not fit together this way."))
    its.append(grid_q(rnd, "Which picture shows 2 triangles that make a square?",
                      [comp(C_SQ2TRI, 70, 0), comp(C_SQVERT, 70, 2), comp(C_RECT2TRI, 86, 1), comp(C_TRIHALF, 80, 3)], 0,
                      "is a square cut from corner to corner, so it is 2 triangles. Another square is cut into 2 rectangles. "
                      "One picture is a rectangle, and one is a triangle.", 3, label="four pictures labeled A to D", word="Picture"))
    its.append(grid_q(rnd, "Put 2 squares side by side. Which shape do you get?",
                      [flat(RECT2, 0, 88, 1), flat(SQUARE, 0, 62, 3), flat(TRI_EQ, 0, 80, 0), flat(HEX_REG, 0, 80, 4)], 0,
                      "is a rectangle that is 2 times as long as it is tall. That is what 2 squares side by side make.", 1))
    its.append(mcq("You put 2 triangles together. Which shape can you make?", "a square",
                   ["a circle", "a hexagon", "a cube"],
                   "Put 2 same triangles together along the long side and you can make a <b>square</b>. "
                   "A hexagon needs more pieces, and a circle has no straight sides."))
    its.append(mcq(cs(C_RECT3SQ, 0, 130, 60) + "How many squares make this rectangle?", 3, [2, 4, 6],
                   "Count the parts between the dashed lines: <b>3</b> squares. There are 2 dashed lines, but 3 squares."))
    nm, he, his = PP.next()
    its.append(mcq("%s has 2 trapezoids. %s puts the long sides together. What shape does %s make?" % (nm, cap(he), he),
                   "a hexagon", ["a rectangle", "a triangle", "a circle"],
                   "2 trapezoids with the long sides together make a <b>hexagon</b>, like pattern blocks."))
    nm, he, his = PP.next()
    its.append(mcq("%s makes hexagons. Each hexagon uses 2 trapezoids. %s has 4 trapezoids. How many hexagons can %s make?"
                   % (nm, cap(he), he), 2, [4, 8, 1],
                   "2 trapezoids make 1 hexagon. 2 more make another one. 2 + 2 = 4, so %s can make <b>2</b> hexagons." % nm))
    its.append(mcq(cs(C_HOUSE, 3, 80, 100) + "Which 2 shapes make this house?", "square, triangle",
                   ["2 triangles", "2 squares", "square, circle"],
                   "The bottom has 4 same sides and square corners: a square. The roof has 3 sides: a triangle."))
    its.append(mcq(cs(C_TRI4, 4, 110, 90) + "How many small triangles make this big triangle?", 4, [3, 5, 2],
                   "There is 1 at the top, 2 at the bottom corners and 1 in the middle that points down. 1 + 2 + 1 = <b>4</b>."))
    its.append(mcq(cs(C_HALVES, 1, 80, 80) + "This circle is made of 2 of which shape?", "half circles",
                   ["triangles", "squares", "circles"],
                   "The dashed line cuts the circle into 2 same parts. Each part is a <b>half circle</b>."))
    its.append(mcq(fig(fit_svg(lambda cx, cy: hexgap_elems(100, 90, cx, cy, col=2), "hexagon with some triangles missing")) +
                   "How many more triangles do you need to finish the hexagon?", 2, [4, 6, 3],
                   "A hexagon needs 6 triangles. There are 4. 6 − 4 = <b>2</b> more."))
    its.append(mcq(cs(C_TRAPSQ, 0, 130, 60) + "Which shapes make this trapezoid?", "1 square, 2 triangles",
                   ["3 triangles", "3 squares", "2 squares, 1 triangle"],
                   "The middle part has 4 same sides and square corners: 1 square. Each end has 3 sides: 2 triangles."))
    assert len(its) == 20, len(its)
    return {"title": "Put shapes together", "items": its}


# ============================================================ set 5: 3-D shapes in real life
def set_solids(rnd, PP):
    its = []
    q = "What is the name of this solid shape?"
    its.append(mcq(fig(solid_svg("cube", "a cube")) + q, "cube", ["square", "cylinder", "cone"],
                   "It is a solid, not flat. All its faces are the same square. It is a <b>cube</b>. A square is a flat shape."))
    its.append(mcq(fig(solid_svg("cylinder", "a cylinder", 80, 96)) + q, "cylinder", ["cone", "circle", "cube"],
                   "It has a flat circle on the top and one on the bottom, with a round side. It is a <b>cylinder</b>."))
    its.append(mcq(fig(solid_svg("cone", "a cone", 80, 96)) + q, "cone", ["cylinder", "triangle", "cube"],
                   "It has 1 flat circle at the bottom and a point at the top. It is a <b>cone</b>. A triangle is flat."))
    its.append(mcq(fig(solid_svg("prism", "a box shape", 120, 80)) + q, "rectangular prism", ["cube", "rectangle", "cylinder"],
                   "It is shaped like a box. Some faces are long rectangles, so it is not a cube. It is a <b>rectangular prism</b>."))
    its.append(grid_q(rnd, "Which one is a cylinder?",
                      [solid("cylinder", 80), solid("cone", 80), solid("cube", 76), solid("prism", 82)], 0,
                      "has a flat circle on the top and on the bottom. The cone has only 1 circle and a point.", 2,
                      label="four solids labeled A to D", word="Solid"))
    its.append(grid_q(rnd, "Which one is a cone?",
                      [solid("cone", 80), solid("cylinder", 80), solid("prism", 82), flat(TRI_EQ, 0, 76, 0)], 0,
                      "has a point at the top and a circle at the bottom. One picture is a flat triangle, not a solid.", 0,
                      label="four pictures labeled A to D", word="Picture"))
    its.append(mcq("A can of soup is shaped like a ___.", "cylinder", ["cone", "circle", "cube"],
                   "A can has a flat circle on the top and the bottom. It is a <b>cylinder</b>."))
    its.append(mcq("An ice cream cone is shaped like a ___.", "cone", ["cylinder", "triangle", "cube"],
                   "It has a point at the bottom and a circle at the top. It is a <b>cone</b>. A triangle is flat."))
    its.append(mcq("A game die is shaped like a ___.", "cube", ["square", "cone", "cylinder"],
                   "A die has 6 faces that are all the same square. It is a <b>cube</b>. A square is only one flat face."))
    its.append(mcq("A cereal box is shaped like a ___.", "rectangular prism", ["cube", "rectangle", "cylinder"],
                   "A cereal box has big faces and thin faces, so it is not a cube. It is a <b>rectangular prism</b>."))
    its.append(mcq("A party hat is shaped like a ___.", "cone", ["triangle", "cylinder", "cube"],
                   "A party hat is round at the bottom and has a point at the top. It is a <b>cone</b>."))
    its.append(mcq("A paper towel roll is shaped like a ___.", "cylinder", ["cone", "circle", "rectangle"],
                   "It is long and round, with a circle at each end. It is a <b>cylinder</b>."))
    its.append(mcq("Which one is a flat shape?", "a circle", ["a cube", "a cone", "a cylinder"],
                   "A circle is flat, like a drawing on paper. A cube, a cone and a cylinder are solid. You can hold them."))
    its.append(mcq("Which solid has a flat circle on the top and on the bottom?", "cylinder",
                   ["cone", "cube", "rectangular prism"],
                   "A <b>cylinder</b> has 2 flat circles. A cone has only 1 circle and a point."))
    its.append(mcq("Which solid has a point at the top and a circle at the bottom?", "cone",
                   ["cylinder", "cube", "rectangular prism"],
                   "A <b>cone</b> has 1 circle and a point. A cylinder has 2 circles and no point."))
    nm, he, his = PP.next()
    its.append(mcq("%s traces around the bottom of a can. What flat shape does %s draw?" % (nm, he), "a circle",
                   ["a cylinder", "a square", "a triangle"],
                   "The bottom of a can is a flat circle, so %s draws a <b>circle</b>. The can itself is a cylinder." % nm))
    nm, he, his = PP.next()
    its.append(mcq("%s traces one face of a die. What flat shape does %s draw?" % (nm, he), "a square",
                   ["a cube", "a circle", "a triangle"],
                   "Each face of a die is a flat square, so %s draws a <b>square</b>. The die itself is a cube." % nm))
    nm, he, his = PP.next()
    its.append(mcq("%s puts 1 cube on top of another cube. What shape is the stack?" % nm, "rectangular prism",
                   ["cube", "cylinder", "cone"],
                   "The stack is 2 times as tall as it is wide, so it is not a cube. It is a <b>rectangular prism</b>, like a box."))
    nm, he, his = PP.next()
    its.append(mcq("%s has a can, a box, a die and a party hat. Which one is a cone?" % nm, "the party hat",
                   ["the can", "the box", "the die"],
                   "The party hat has a point and a circle: a cone. The can is a cylinder, the box is a rectangular prism and the die is a cube."))
    nm, he, his = PP.next()
    its.append(mcq("%s wants something that rolls smoothly across the floor. Which one should %s pick?" % (nm, he), "a can",
                   ["a box", "a toy block", "a book"],
                   "A can is a cylinder. Its side is round, so it rolls smoothly. A box, a block and a book have flat faces and corners, so they do not roll smoothly."))
    assert len(its) == 20, len(its)
    return {"title": "3-D shapes in real life", "items": its}


# ============================================================ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def counting_svg():
    """A hexagon with its corners numbered 1-6 outside the shape."""
    sh = HEX_LONG
    W, H = 250, 170
    pts = fit(sh["pts"], 0, 160, 100, W / 2, H / 2)
    el = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='3' stroke-linejoin='round'/>" % (P(pts), FILL, GREEN)]
    mx, my = sum(p[0] for p in pts) / 6, sum(p[1] for p in pts) / 6
    boxes = []
    for i, p in enumerate(pts):
        el.append("<circle cx='%.1f' cy='%.1f' r='5' fill='%s'/>" % (p[0], p[1], "#c0392b"))
        d = (p[0] - mx, p[1] - my)
        L = math.hypot(*d)
        c = (p[0] + d[0] / L * 20, p[1] + d[1] / L * 20)
        el.append(text(c[0], c[1] + 6, str(i + 1), 17, col="#c0392b"))
        boxes.append((c[0] - 7, c[1] - 7, c[0] + 7, c[1] + 7))
    for b in boxes:
        for i in range(6):
            a, q = pts[i], pts[(i + 1) % 6]
            for t in range(21):
                x, y = a[0] + (q[0] - a[0]) * t / 20.0, a[1] + (q[1] - a[1]) * t / 20.0
                assert not (b[0] - 3 < x < b[2] + 3 and b[1] - 3 < y < b[3] + 3), "number touches a side"
        assert b[0] > 0 and b[1] > 0 and b[2] < W and b[3] < H
    return svg_wrap(W, H, "".join(el), "hexagon with its 6 corners numbered")


def mini(f):
    e, bb = f(32, 26)
    assert bb[0] >= 0 and bb[1] >= 0 and bb[2] <= 64 and bb[3] <= 52, bb
    return svg_wrap(64, 52, "".join(e), "small picture")


def strip_svg(items, label, cw=132, top=104):
    el = []
    for k, (f, capt) in enumerate(items):
        e, bb = f(k * cw + cw / 2, top / 2)
        assert bb[0] >= k * cw + 4 and bb[2] <= (k + 1) * cw - 4 and bb[1] >= 2 and bb[3] <= top - 2, (capt, bb)
        assert len(capt) * 8.6 < cw - 6, capt
        el += e
        el.append(text(k * cw + cw / 2, top + 18, capt, 15))
    return svg_wrap(cw * len(items), top + 26, "".join(el), label)


def mshape(sh, rot=0, col=0, w=50, h=40, how=None):
    f = {None: shape_elems, "open": open_elems, "curved": curved_elems}[how]
    return lambda cx, cy: f(sh, rot, w, h, cx, cy, sw=2.4, col=col)


def body_html():
    yes = strip_svg([(mshape(TRI_EQ, 0, 3, 86, 80), "big"), (mshape(TRI_EQ, 0, 1, 40, 36), "small"),
                     (mshape(TRI_TALL, 180, 4, 70, 86), "turned"), (mshape(TRI_WIDE, 0, 2, 100, 70), "long")],
                    "four triangles: big, small, turned and long")
    no = strip_svg([(mshape(TRI_EQ, 0, 1, 86, 80, "open"), "open"), (mshape(TRI_EQ, 0, 2, 90, 80, "curved"), "curved side"),
                    (mshape(TRAP, 0, 0, 100, 60), "4 sides")],
                   "three shapes that are not triangles: open, curved side and 4 sides")
    together = strip_svg([(lambda cx, cy: comp_elems(C_SQ2TRI, 76, 76, cx, cy, 2), "2 triangles"),
                          (lambda cx, cy: comp_elems(C_RECT2SQ, 110, 60, cx, cy, 1), "2 squares"),
                          (lambda cx, cy: comp_elems(C_HEX6, 90, 80, cx, cy, 4), "6 triangles")],
                         "2 triangles make a square, 2 squares make a rectangle, 6 triangles make a hexagon")
    solids = strip_svg([(lambda cx, cy: box_elems(CUBE, 84, 84, cx, cy), "cube"),
                        (lambda cx, cy: box_elems(PRISM, 120, 80, cx, cy), "rect. prism"),
                        (lambda cx, cy: round_solid("cone", 80, 92, cx, cy), "cone"),
                        (lambda cx, cy: round_solid("cylinder", 80, 92, cx, cy), "cylinder")],
                       "a cube, a rectangular prism, a cone and a cylinder", cw=140)
    return (
        "<h2>Know a shape by its sides and corners</h2>"
        "<p>A <b>side</b> is a straight line of a shape. A <b>corner</b> is where 2 sides meet. "
        "A corner is also called a <b>vertex</b>. Two or more are <b>vertices</b>.</p>"
        "<p>To count, put your finger on one corner. Go around the shape. Count each corner once. Stop when you are back at the start.</p>"
        "<figure class='sn-fig'>" + counting_svg() +
        "<figcaption>Start at 1 and go around: 6 corners. There are 6 sides too. It is a hexagon.</figcaption></figure>" +
        table(["Shape", "Name", "Sides", "Corners", "Rule"], [
            [mini(mshape(CIRCLE, 0, 1, 40, 40)), "circle", "0", "0", "round"],
            [mini(mshape(TRI_EQ, 0, 3)), "triangle", "3", "3", "3 straight sides"],
            [mini(mshape(SQUARE, 0, 2, 40, 40)), "square", "4", "4", "4 same sides, 4 square corners"],
            [mini(mshape(RECT, 0, 4, 56, 30)), "rectangle", "4", "4", "4 square corners"],
            [mini(mshape(TRAP, 0, 0, 56, 34)), "trapezoid", "4", "4", "2 sides go the same way"],
            [mini(mshape(HEX_REG, 0, 1, 50, 44)), "hexagon", "6", "6", "6 straight sides"],
        ]) +
        ex("Example", "A shape has 4 sides that are all the same length and 4 square corners. What is it?",
           "4 same sides and 4 square corners make a square.", "a square") +
        "<h2>What matters and what does not</h2>"
        "<p>A shape must be <b>closed</b>: the sides meet all the way around. The sides must be <b>straight</b>. "
        "The number of sides and corners gives the name.</p>"
        "<p><b>Color</b>, <b>size</b> and <b>turning</b> do not matter. A turned square is still a square.</p>"
        "<figure class='sn-fig'>" + yes + "<figcaption>All of these are triangles. Each one is closed and has 3 straight sides.</figcaption></figure>"
        "<figure class='sn-fig'>" + no + "<figcaption>None of these are triangles. One is open, one has a curved side, and one has 4 sides.</figcaption></figure>" +
        ex("Example", "Is a small, blue, upside-down triangle still a triangle?",
           "It is closed and has 3 straight sides. Size, color and turning do not matter.", "yes") +
        "<h2>Put shapes together</h2>"
        "<p>You can put flat shapes together to make a new shape. The dashed lines show the parts.</p>"
        "<figure class='sn-fig'>" + together +
        "<figcaption>2 triangles make a square. 2 squares make a rectangle. 6 triangles make a hexagon.</figcaption></figure>" +
        ex("Example", "2 trapezoids are put together along the long sides. What shape do they make?",
           "Each trapezoid is half of a hexagon. 2 halves make a whole.", "a hexagon") +
        "<h2>Solid shapes</h2>"
        "<p>Some shapes are not flat. You can hold them. These are <b>solid shapes</b> (3-D shapes).</p>"
        "<figure class='sn-fig'>" + solids +
        "<figcaption>Dashed lines show the parts at the back that you cannot see.</figcaption></figure>" +
        table(["Solid shape", "Things shaped like it"], [
            ["cube", "a game die, an ice cube, a toy block"],
            ["rectangular prism", "a cereal box, a shoe box, a book"],
            ["cone", "an ice cream cone, a party hat"],
            ["cylinder", "a can of soup, a paper towel roll"],
        ]) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Calling a turned square a diamond", "Turning does not change a shape. It is still a square"],
            ["Calling 3 lines with a gap a triangle", "A triangle must be closed"],
            ["Thinking color or size changes the shape", "Count the sides and corners. That gives the name"],
            ["Counting 5 or 7 sides on a hexagon", "Start at one corner and stop when you are back there"],
            ["Mixing up a cylinder and a cone", "A cylinder has 2 circles. A cone has 1 circle and a point"],
            ["Calling a cube a square", "A square is flat. A cube is a solid with square faces"],
        ])
    )


FAQ = [
    {"q": "What are defining attributes of shapes in 1st grade?",
     "a": "Defining attributes are what make a shape that shape: being closed, having straight sides, and the number of sides and corners. Color, size and turning are not defining attributes (Common Core 1.G.A.1)."},
    {"q": "Is a square turned on its corner a diamond?",
     "a": "It is still a square. It has 4 same sides and 4 square corners, and turning a shape never changes what it is."},
    {"q": "What 3-D shapes do 1st graders learn?",
     "a": "Grade 1 students learn cubes, rectangular prisms, cones and cylinders. They name them and find them in real things, like a can (cylinder) or a die (cube)."},
    {"q": "What shapes can you make with two triangles?",
     "a": "Two same triangles can make a square or a rectangle when you put their long sides together. Six triangles can make a hexagon (Common Core 1.G.A.2)."},
]


def gen():
    rnd = random.Random(115)
    PP = People(rnd)
    sets = [set_name(rnd, PP), set_count(rnd, PP), set_matters(rnd, PP), set_compose(rnd, PP), set_solids(rnd, PP)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
            assert "\\" not in it["q"] + it["e"] + "".join(it["c"])
    return {
        "country": "us", "subject": "math", "grade": "grade-1", "slug": "shapes-and-attributes", "sort": 15,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 1 Shapes: Sides, Corners and What Makes a Shape",
        "seo_title": "Grade 1 Shapes Worksheets: Defining Attributes, Composing Shapes and 3-D Shapes (1.G.A.1)",
        "short_title": "Shapes and attributes",
        "domain": "Geometry",
        "standard_code": "1.G.A.1",
        "standard_url": "https://www.thecorestandards.org/Math/Content/1/G/A/1/",
        "standard_text": "Distinguish between defining attributes (e.g., triangles are closed and three-sided) versus non-defining attributes (e.g., color, orientation, overall size); build and draw shapes to possess defining attributes.",
        "meta_desc": "Free Grade 1 shapes worksheets with pictures: name circles, triangles, squares, rectangles, trapezoids and hexagons, count sides and corners, learn what matters (closed, straight sides) and what does not (color, size, turning), put shapes together, and find cubes, cones and cylinders in real life. 100 questions with answer key.",
        "key_big": "Sides and corners give a shape its name. Color, size and turning do not.",
        "key_sub": "A triangle is closed and has 3 straight sides. A turned square is still a square. Shapes can be put together: 2 triangles make a square, 2 squares make a rectangle.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (A-D choices, pairs) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "(four [a-z]+ labeled A to D|shape A and shape B)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
