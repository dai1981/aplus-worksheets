# -*- coding: utf-8 -*-
"""
US Grade 2 Math: Shapes and Their Attributes (2.G.A.1)
  python tools/gen_us_math_g2_shapes.py
HTML attributes use single quotes (no backslashes in the JSON).

Words used everywhere (as in the lesson):
  side      one straight line of a flat shape
  corner    where 2 sides meet (also called a vertex); every corner makes an angle
  triangle 3 sides, quadrilateral 4, pentagon 5, hexagon 6 (octagon 8 only as a bonus)
  face      a flat surface of a solid; edge: where 2 faces meet; vertex: a corner where edges meet
  cube      6 faces that are all the same square, 12 edges, 8 vertices
Every drawing is checked in code: each flat shape has exactly the number of sides its name says,
no two sides cross, every corner is clearly a corner (not almost straight), shapes called regular
really have equal sides, and shapes called irregular clearly do not. Solids are drawn in an
oblique view with exactly 3 hidden edges dashed.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
TOP = "#e6f2e9"
SIDE = "#a9d3b6"
RED = "#c0392b"
REDFILL = "#f2b8ae"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
NAMES = {3: "triangle", 4: "quadrilateral", 5: "pentagon", 6: "hexagon", 8: "octagon"}
FOUR = ["triangle", "quadrilateral", "pentagon", "hexagon"]


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
    """Choices keep their order (A B C D, the four shape names)."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fixed": True}


def balance(sets, rnd):
    """Exactly 5 correct answers in each position A-D in every set. Fixed-order questions keep
    their place; the others fill the gaps."""
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
    """Angle between the two sides at each corner, 0..180 (a reflex corner gives its outside angle)."""
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


def regular(n, r=60, start=-90):
    return [(r * math.cos(math.radians(start + 360.0 * i / n)), r * math.sin(math.radians(start + 360.0 * i / n)))
            for i in range(n)]


def S(pts, reg=False):
    pts = [(float(x), float(y)) for x, y in pts]
    n = len(pts)
    sh = {"pts": pts, "n": n, "kind": NAMES[n], "reg": reg}
    # simple polygon: no two sides cross
    for i in range(n):
        for j in range(i + 2, n):
            if (j + 1) % n == i:
                continue
            assert not segs_cross(pts[i], pts[(i + 1) % n], pts[j], pts[(j + 1) % n]), ("sides cross", pts)
    A, L = corner_angles(pts), side_lens(pts)
    assert all(25 <= a <= 160 for a in A), ("corner too flat or too sharp", A)      # every corner is easy to see
    assert min(L) >= 0.2 * max(L), ("side too short to see", L)
    if reg:
        assert max(L) - min(L) < 1e-6 * max(L) and max(A) - min(A) < 1e-6, ("not regular", L, A)
    else:
        assert max(L) / min(L) > 1.15 or max(A) - min(A) > 12, ("looks regular", L, A)
    return sh


CIRCLE = {"pts": [], "n": 0, "kind": "circle", "reg": True}

# triangles
TRI_EQ = S(regular(3), True)
TRI_RIGHT = S([(0, 0), (0, 90), (120, 90)])
TRI_WIDE = S([(0, 60), (150, 80), (40, 0)])
TRI_TALL = S([(0, 130), (60, 130), (30, 0)])
# quadrilaterals
SQUARE = S([(0, 0), (100, 0), (100, 100), (0, 100)], True)
RECT = S([(0, 0), (150, 0), (150, 70), (0, 70)])
TRAP = S([(0, 80), (150, 80), (105, 0), (35, 0)])
QUAD = S([(0, 15), (140, 0), (125, 70), (40, 125)])
KITE = S([(0, 0), (50, 35), (0, 155), (-50, 35)])
RHOMB = S([(0, 0), (100, 0), (150, 80), (50, 80)])
# pentagons
PENT_REG = S(regular(5), True)
HOUSE = S([(0, 45), (55, 0), (110, 45), (110, 120), (0, 120)])
PENT_IR = S([(0, 30), (80, 0), (150, 40), (120, 110), (20, 100)])
PENT_SLANT = S([(0, 0), (130, 0), (150, 60), (60, 110), (0, 80)])
# hexagons
HEX_REG = S(regular(6, start=0), True)
HEX_LONG = S([(30, 0), (130, 0), (165, 45), (130, 90), (30, 90), (0, 45)])
HEX_L = S([(0, 0), (50, 0), (50, 70), (120, 70), (120, 120), (0, 120)])
HEX_IR = S([(0, 30), (50, 0), (130, 10), (150, 70), (90, 115), (20, 90)])
HEX_ARROW = S([(0, 0), (60, 0), (100, 50), (60, 100), (0, 100), (40, 50)])
# bonus
OCT = S(regular(8, start=-90 + 22.5), True)


def rot_pt(p, deg):
    t = math.radians(deg)
    return (p[0] * math.cos(t) - p[1] * math.sin(t), p[0] * math.sin(t) + p[1] * math.cos(t))


def placed(sh, rot, bw, bh, cx, cy):
    """Rotate, scale to fit a bw x bh box (same scale both ways, so regular stays regular), center at (cx, cy)."""
    pts = [rot_pt(p, rot) for p in sh["pts"]]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    k = min(bw / (max(xs) - min(xs)), bh / (max(ys) - min(ys)))
    mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    return [(cx + (p[0] - mx) * k, cy + (p[1] - my) * k) for p in pts]


def shape_elems(sh, rot, bw, bh, cx, cy, sw=3, fill=FILL):
    """SVG elements for one flat shape and the box around everything drawn."""
    if sh["kind"] == "circle":
        r = min(bw, bh) / 2.0
        el = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='%g'/>" % (cx, cy, r, fill, GREEN, sw)]
        pad = r + sw / 2.0 + 1
        return el, (cx - pad, cy - pad, cx + pad, cy + pad)
    pts = placed(sh, rot, bw, bh, cx, cy)
    assert len(pts) == sh["n"]
    el = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>" % (P(pts), fill, GREEN, sw)]
    pad = sw / 2.0 + 1
    return el, (min(p[0] for p in pts) - pad, min(p[1] for p in pts) - pad,
                max(p[0] for p in pts) + pad, max(p[1] for p in pts) + pad)


def fit_svg(make, label, pad=6):
    """make(cx, cy) -> (elements, bbox). Draw once to measure, then again centered in a tight viewBox."""
    _, bb = make(0, 0)
    W, H = int(math.ceil(bb[2] - bb[0] + 2 * pad)), int(math.ceil(bb[3] - bb[1] + 2 * pad))
    if W == H:
        W += 1                                       # keep figures out of the larger 'square' print size
    cx = pad - bb[0] + (W - (bb[2] - bb[0] + 2 * pad)) / 2
    cy = pad - bb[1] + (H - (bb[3] - bb[1] + 2 * pad)) / 2
    el, bb2 = make(cx, cy)
    assert bb2[0] >= 0 and bb2[1] >= 0 and bb2[2] <= W and bb2[3] <= H, (label, bb2, W, H)
    return svg_wrap(W, H, "".join(el), label)


def shape_svg(sh, rot=0, bw=110, bh=80, label=None):
    return fit_svg(lambda cx, cy: shape_elems(sh, rot, bw, bh, cx, cy), label or "a flat shape")


def octagon_sign_svg():
    return fit_svg(lambda cx, cy: shape_elems(OCT, 0, 80, 80, cx, cy, sw=4, fill=REDFILL), "sign shaped like an octagon")


CELL = 118


def grid_svg(cells, label):
    """2 x 2 grid labeled A-D. cells: list of functions f(cx, cy, size) -> (elements, bbox)."""
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


def flat(sh, rot=0, size=80):
    return lambda cx, cy: shape_elems(sh, rot, size, size, cx, cy, sw=2.6)


def pair_svg(a, b, label="shape A and shape B"):
    """Two flat shapes side by side. a, b: (shape, rot, size)."""
    W, H = 2 * CELL, CELL
    el = ["<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, CELL, H - 4, GRAY)]
    for k, (sh, rot, size) in enumerate([a, b]):
        x0 = k * CELL
        e, bb = shape_elems(sh, rot, size, size, x0 + 66, 64, sw=2.6)
        assert bb[0] >= x0 + 20 and bb[1] >= 3 and bb[2] <= x0 + CELL - 3 and bb[3] <= H - 3, (label, bb)
        el += e
        el.append(text(x0 + 7, 22, "AB"[k], 18, "start"))
    return svg_wrap(W, H, "".join(el), label)


# ------------------------------------------------------------ solids (oblique view, depth goes up and to the side)
def box_geom(w, h, d, left=False, ang=38):
    """Corners of a box: front face f (top-left, top-right, bottom-right, bottom-left) and back face b.
    Returns points, the 12 edges (i, j, hidden) and the 3 visible faces."""
    dx, dy = d * math.cos(math.radians(ang)), d * math.sin(math.radians(ang))
    assert dx < w and dy < h                       # the hidden corner sits behind the front face
    sg = -1 if left else 1
    f = [(0, 0), (w, 0), (w, h), (0, h)]
    b = [(x + sg * dx, y - dy) for x, y in f]
    pts = f + b                                    # 0-3 front, 4-7 back
    hid = 7 if not left else 6                     # back-bottom-left (or back-bottom-right) is hidden
    edges = []
    for i in range(4):
        edges += [(i, (i + 1) % 4), (4 + i, 4 + (i + 1) % 4), (i, 4 + i)]
    edges = [(i, j, hid in (i, j)) for i, j in edges]
    side = [1, 5, 6, 2] if not left else [0, 4, 7, 3]
    faces = [([0, 1, 2, 3], FILL), ([0, 1, 5, 4], TOP), (side, SIDE)]
    assert len(edges) == 12 and sum(1 for e in edges if e[2]) == 3
    return pts, edges, faces


def pyramid_geom(w, d, H, ang=38):
    dx, dy = d * math.cos(math.radians(ang)), d * math.sin(math.radians(ang))
    pts = [(0, 0), (w, 0), (w + dx, -dy), (dx, -dy), ((w + dx) / 2, -dy / 2 - H)]
    edges = [(0, 1, False), (1, 2, False), (2, 3, True), (3, 0, True),
             (0, 4, False), (1, 4, False), (2, 4, False), (3, 4, True)]
    faces = [([0, 1, 4], FILL), ([1, 2, 4], SIDE)]
    return pts, edges, faces


def solid_elems(geom, bw, bh, cx, cy, hl=None, sw=2.6):
    """hl: ('face', i) shades visible face i red, ('edge', (i, j)) colors a visible edge red,
    ('vertex', i) puts a red dot on a corner."""
    pts, edges, faces = geom
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    k = min(bw / (max(xs) - min(xs)), bh / (max(ys) - min(ys)))
    mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    T = [(cx + (p[0] - mx) * k, cy + (p[1] - my) * k) for p in pts]
    el = []
    for fi, (idx, col) in enumerate(faces):
        if hl and hl[0] == "face" and hl[1] == fi:
            col = REDFILL
        el.append("<polygon points='%s' fill='%s' stroke='none'/>" % (P([T[i] for i in idx]), col))
    for i, j, hidden in edges:
        if hidden:
            el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.8' "
                      "stroke-dasharray='6 5'/>" % (T[i] + T[j] + (GREEN,)))
    for i, j, hidden in edges:
        if not hidden:
            red = hl and hl[0] == "edge" and set(hl[1]) == {i, j}
            el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%g' stroke-linecap='round'/>"
                      % (T[i] + T[j] + (RED if red else GREEN, 5 if red else sw)))
    if hl and hl[0] == "edge":
        assert any(set(hl[1]) == {i, j} and not h for i, j, h in edges)
    r = 0
    if hl and hl[0] == "vertex":
        r = 6.5
        el.append("<circle cx='%.1f' cy='%.1f' r='%g' fill='%s'/>" % (T[hl[1]] + (r, RED)))
    pad = max(sw / 2.0 + 1, r + 1)
    return el, (min(p[0] for p in T) - pad, min(p[1] for p in T) - pad, max(p[0] for p in T) + pad, max(p[1] for p in T) + pad)


CUBE = box_geom(70, 70, 40)
CUBE_L = box_geom(70, 70, 40, left=True)
PRISM = box_geom(120, 55, 45)
PRISM_TALL = box_geom(60, 110, 40)
PYRAMID = pyramid_geom(100, 50, 120)
# a cube's faces must all be the same square: front w = h, and the depth is drawn shorter on purpose (oblique view)


def solid_svg(geom, label, bw=95, bh=88, hl=None):
    return fit_svg(lambda cx, cy: solid_elems(geom, bw, bh, cx, cy, hl), label)


def solid(geom, size=78):
    return lambda cx, cy: solid_elems(geom, size, size, cx, cy, sw=2.3)


def flat_square(size=62):
    return lambda cx, cy: shape_elems(SQUARE, 0, size, size, cx, cy, sw=2.6)


# ------------------------------------------------------------ explanation pieces
def count_e(sh, what):
    n = sh["n"]
    w = {"sides": "side", "corners": "corner", "angles": "angle"}[what]
    s = "Put your finger on one corner and go around the shape. "
    if what == "sides":
        s += "Count each side once: <b>%d</b> sides." % n
    elif what == "corners":
        s += "Count each corner once, and stop when you are back at the start: <b>%d</b> corners." % n
    else:
        s += "There is 1 angle at each corner. %d corners make <b>%d</b> angles." % (n, n)
    s += " It is a %s." % sh["kind"]
    return s


def grid_q(rnd, q, items, ans, why, target, label="four shapes labeled A to D", word="Shape"):
    """items[ans] is the right picture. It is placed at position target; the others fill the rest."""
    rest = [f for i, f in enumerate(items) if i != ans]
    rnd.shuffle(rest)
    cells = rest[:target] + [items[ans]] + rest[target:]
    L = "ABCD"[target]
    return mcq_fixed(fig(grid_svg(cells, label)) + q, ["A", "B", "C", "D"], L, "%s %s %s" % (word, L, why))


# ============================================================ set 1: count sides and corners
def set_count(rnd, PP):
    its = []
    plan = [
        (TRI_EQ, 0, "sides"), (TRI_RIGHT, 30, "corners"), (SQUARE, 0, "sides"), (SQUARE, 45, "corners"),
        (RECT, 0, "sides"), (PENT_REG, 0, "sides"), (HOUSE, 0, "corners"), (HEX_REG, 0, "sides"),
        (HEX_LONG, 20, "corners"), (TRAP, 0, "corners"), (PENT_IR, 160, "sides"), (RHOMB, 0, "angles"),
        (HEX_REG, 30, "angles"),
    ]
    for sh, rot, what in plan:
        n = sh["n"]
        e = count_e(sh, what)
        if rot % 90:
            e += " Turning a shape does not change how many %s it has." % what
        if sh is SQUARE and rot == 45:
            e = e.replace("It is a quadrilateral.", "It is a square, turned. A square is a quadrilateral.")
        cands = [n + 1, n - 1, 2 * n] if what != "angles" else [n - 1, n + 1, 2 * n]
        its.append(mcq(fig(shape_svg(sh, rot, label=sh["kind"])) + "How many %s does this shape have?" % what, n, cands, e))
    # sides and corners together
    for sh, rot in [(TRI_WIDE, 0), (PENT_SLANT, 0)]:
        n = sh["n"]
        right = "%d sides, %d corners" % (n, n)
        wrong = ["%d sides, %d corners" % (n, n + 1), "%d sides, %d corners" % (n + 1, n), "%d sides, %d corners" % (n - 1, n - 1)]
        its.append(mcq(fig(shape_svg(sh, rot, label=sh["kind"])) + "How many sides and corners does this shape have?",
                       right, wrong,
                       "Count the sides: %d. Count the corners: %d. A flat shape with straight sides always has the same number of sides and corners. "
                       "If you get %d corners, you counted the first corner again." % (n, n, n + 1)))
    # circle
    its.append(mcq(fig(shape_svg(CIRCLE, 0, 70, 70, label="circle")) + "How many corners does a circle have?", 0, [1, 2, 4],
                   "A circle is round all the way around. It has no straight sides, so there are no corners: <b>0</b>."))
    # big and small
    its.append(mcq(fig(pair_svg((TRI_RIGHT, 0, 86), (TRI_EQ, 180, 38))) + "Shape A is big. Shape B is small. Which has more sides?",
                   "They are the same", ["A, it is bigger", "B, it is smaller", "You cannot tell"],
                   "Both are triangles with 3 sides. Size does not change the number of sides."))
    its.append(mcq("A corner is where 2 ___ meet.", "sides", ["corners", "circles", "shapes"],
                   "A side is one straight line of a shape. A corner (vertex) is the point where 2 sides meet."))
    its.append(mcq("A shape has 4 sides. How many corners does it have?", 4, [3, 5, 8],
                   "Each side ends at a corner, and each corner joins 2 sides. A flat shape has the same number of corners as sides: <b>4</b>."))
    nm, he, his = PP.next()
    its.append(mcq("%s draws a shape with 6 corners. How many angles does it have?" % nm, 6, [5, 12, 3],
                   "There is 1 angle at every corner. 6 corners make <b>6</b> angles. Do not add corners and angles together."))
    assert len(its) == 20, len(its)
    return {"title": "Count sides and corners", "items": its}


# ============================================================ set 2: name the shape
def name_e(sh, rot):
    n = sh["n"]
    s = "Count the sides: %d. A shape with %d sides is a <b>%s</b>." % (n, n, sh["kind"])
    if sh is HEX_L or sh is HEX_ARROW:
        s += " Count the corner that points in, too."
    elif sh is SQUARE and rot % 90:
        s = "Count the sides: 4. It is a square that is turned, and every square is a <b>quadrilateral</b>."
    elif not sh["reg"]:
        s += " The sides do not have to be the same length."
    if rot % 90 and sh is not SQUARE:
        s += " Turning a shape does not change its name."
    return s


def set_name(rnd, PP):
    its = []
    plan = [(TRI_WIDE, 0), (TRI_RIGHT, 200), (TRI_TALL, 15),
            (QUAD, 0), (TRAP, 180), (SQUARE, 45), (KITE, 0),
            (PENT_IR, 0), (HOUSE, 180), (PENT_REG, 36),
            (HEX_L, 0), (HEX_LONG, 0), (HEX_IR, 0), (HEX_ARROW, 0)]
    for sh, rot in plan:
        its.append(mcq_fixed(fig(shape_svg(sh, rot, label=sh["kind"])) + "What is the name of this shape?",
                             FOUR, sh["kind"], name_e(sh, rot)))
    nm, he, his = PP.next()
    its.append(mcq(fig(shape_svg(HEX_IR, 0, label="hexagon with sides of different lengths")) +
                   "%s says this is not a hexagon because the sides are not the same length. Is %s right?" % (nm, he),
                   "No, it has 6 sides", ["Yes, sides must match", "Yes, it is a pentagon", "No, it is an octagon"],
                   "Count the sides: 6. Any closed shape with 6 straight sides is a hexagon. The sides can be different lengths."))
    nm, he, his = PP.next()
    its.append(mcq(fig(shape_svg(SQUARE, 45, 90, 90, label="square turned on a corner")) +
                   "%s says this shape is a diamond, not a quadrilateral. Is %s right?" % (nm, he),
                   "No, it has 4 sides", ["Yes, it is a diamond", "Yes, it is turned", "No, it has 5 sides"],
                   "It has 4 straight sides, so it is a quadrilateral. It is a square standing on a corner. Turning does not change its name."))
    its.append(mcq("A shape has 5 sides. What is it called?", "pentagon", ["hexagon", "quadrilateral", "octagon"],
                   "<b>Penta</b> means 5. A shape with 5 sides is a pentagon. A hexagon has 6 sides."))
    its.append(mcq("How many sides does a hexagon have?", 6, [5, 8, 4],
                   "<b>Hexa</b> means 6. A hexagon has 6 sides and 6 corners. (A pentagon has 5 and an octagon has 8.)"))
    its.append(mcq("A shape has 3 corners. What is it?", "triangle", ["quadrilateral", "hexagon", "pentagon"],
                   "3 corners means 3 sides. <b>Tri</b> means 3, so it is a triangle."))
    its.append(mcq("What does <b>quad</b> in <b>quadrilateral</b> tell you?", "4 sides", ["3 sides", "5 sides", "equal sides"],
                   "Quad means 4. A quadrilateral has 4 sides. The sides do not have to be equal."))
    assert len(its) == 20, len(its)
    return {"title": "Name the shape", "items": its}


# ============================================================ set 3: which shape has ...?
def set_which(rnd, PP):
    its = []
    T = [0, 1, 2, 3] * 3
    rnd.shuffle(T)
    G = [
        ("Which shape has exactly 5 corners?", [flat(PENT_IR), flat(HEX_IR), flat(QUAD), flat(TRI_WIDE)], 0,
         "is a pentagon with 5 corners. The others have 6, 4 and 3 corners."),
        ("Which shape has more sides than a square?", [flat(HEX_LONG), flat(SQUARE, 45, 70), flat(TRI_EQ), flat(TRAP)], 0,
         "is a hexagon with 6 sides. A square has 4. The others have 4, 3 and 4 sides, so they do not have more."),
        ("Which shape has 3 sides?", [flat(TRI_RIGHT, 160), flat(QUAD), flat(PENT_REG), flat(CIRCLE, 0, 66)], 0,
         "has 3 sides, so it is a triangle, even though it is turned. A circle has no sides."),
        ("Which shape is a hexagon?", [flat(HEX_L), flat(PENT_REG), flat(HOUSE), flat(RECT)], 0,
         "has 6 sides, so it is a hexagon. It does not look like a honeycomb, but count the sides: 6. The others have 5, 5 and 4 sides."),
        ("Which shape is NOT a quadrilateral?", [flat(HOUSE), flat(SQUARE, 45, 70), flat(TRAP), flat(QUAD)], 0,
         "has 5 sides, so it is a pentagon. The other three have 4 sides, so they are quadrilaterals."),
        ("Which shape has fewer corners than a square?", [flat(TRI_TALL), flat(PENT_REG), flat(HEX_REG), flat(RHOMB)], 0,
         "is a triangle with 3 corners. A square has 4. The others have 5, 6 and 4 corners."),
        ("Which shape has no corners?", [flat(CIRCLE, 0, 66), flat(TRI_EQ), flat(SQUARE, 0, 66), flat(HEX_REG)], 0,
         "is a circle. It is round, with no straight sides and no corners."),
        ("Which shape has 6 angles?", [flat(HEX_REG, 30), flat(PENT_SLANT), flat(KITE), flat(TRI_WIDE)], 0,
         "is a hexagon. It has 6 corners, and each corner has an angle: 6 angles."),
        ("Which shape is a quadrilateral?", [flat(QUAD, 20), flat(PENT_IR), flat(TRI_RIGHT), flat(HEX_IR)], 0,
         "has 4 sides, so it is a quadrilateral. The sides are not equal, and that is fine."),
        ("Which shape has 1 more side than a square?", [flat(PENT_SLANT), flat(HEX_LONG), flat(RECT), flat(TRI_EQ)], 0,
         "has 5 sides: 1 more than the 4 sides of a square. It is a pentagon."),
        ("Which shape has the most sides?", [flat(HEX_REG, 0, 44), flat(PENT_REG, 0, 64), flat(SQUARE, 0, 74), flat(TRI_RIGHT, 0, 84)], 0,
         "is the smallest shape, but it has the most sides: 6. Count the sides. Do not look at the size."),
        ("Which shape has 2 more sides than a quadrilateral?", [flat(HEX_ARROW), flat(HOUSE), flat(SQUARE, 20, 66), flat(OCT, 0, 72)], 0,
         "has 6 sides. A quadrilateral has 4, and 4 + 2 = 6. It is a hexagon. (The 8-sided shape is an octagon.)"),
    ]
    for (q, items, ans, why), t in zip(G, T):
        its.append(grid_q(rnd, q, items, ans, why, t))
    its.append(mcq("Which has more corners, a triangle or a hexagon?", "a hexagon", ["a triangle", "They are the same", "You cannot tell"],
                   "A triangle has 3 corners. A hexagon has 6 corners. 6 is more than 3."))
    its.append(mcq("How many more sides does a hexagon have than a triangle?", 3, [6, 9, 2],
                   "A hexagon has 6 sides and a triangle has 3. 6 − 3 = <b>3</b> more sides."))
    its.append(mcq("How many more corners does a pentagon have than a quadrilateral?", 1, [9, 5, 2],
                   "A pentagon has 5 corners and a quadrilateral has 4. 5 − 4 = <b>1</b> more corner."))
    its.append(mcq("A shape has more than 4 sides but fewer than 6 sides. What is it?", "pentagon",
                   ["hexagon", "quadrilateral", "octagon"],
                   "More than 4 and fewer than 6 is 5. A shape with 5 sides is a pentagon."))
    its.append(mcq("Does a flat shape with straight sides always have the same number of sides and corners?",
                   "Yes, always", ["No, never", "Only triangles", "Only squares"],
                   "Every side ends at a corner, and every corner joins 2 sides. So a triangle has 3 and 3, a hexagon has 6 and 6."))
    its.append(mcq("How many corners do a square and a triangle have in all?", 7, [6, 8, 1],
                   "A square has 4 corners and a triangle has 3. 4 + 3 = <b>7</b> corners."))
    its.append(mcq("Which has fewer sides, a pentagon or a quadrilateral?", "a quadrilateral",
                   ["a pentagon", "They are the same", "You cannot tell"],
                   "A quadrilateral has 4 sides and a pentagon has 5. 4 is fewer than 5."))
    its.append(mcq("What is the fewest straight sides a closed shape can have?", 3, [2, 1, 4],
                   "2 straight sides cannot close up. With 3 sides you can make a closed shape: a triangle."))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Which shape has ...?", "items": its}


# ============================================================ set 4: cubes and other solids
def set_cube(rnd, PP):
    its = []
    cube_pic = lambda lab="cube with hidden edges dashed", hl=None: fig(solid_svg(CUBE, lab, hl=hl))
    prism_pic = fig(solid_svg(PRISM, "rectangular prism with hidden edges dashed", 120, 80))
    its.append(mcq(cube_pic() + "How many faces does a cube have?", 6, [3, 4, 8],
                   "A face is a flat side. You can see 3 faces, but there are 3 more on the back, the bottom and the left: 3 + 3 = <b>6</b>."))
    its.append(mcq(cube_pic() + "How many edges does a cube have?", 12, [9, 8, 6],
                   "An edge is where 2 faces meet. There are 4 edges on the front, 4 on the back and 4 going from front to back: <b>12</b>. "
                   "The dashed lines are edges you cannot see, so count them too."))
    its.append(mcq(cube_pic() + "How many vertices (corners) does a cube have?", 8, [7, 6, 12],
                   "A vertex is a corner where edges meet. There are 4 on the front and 4 on the back: <b>8</b>. "
                   "One vertex is hidden at the back, where the dashed lines meet."))
    its.append(mcq(cube_pic("cube with one face shaded red", ("face", 0)) + "What is the red part called?",
                   "a face", ["an edge", "a vertex", "a side"],
                   "The red part is a flat surface of the cube. A flat surface of a solid is called a <b>face</b>."))
    its.append(mcq(cube_pic("cube with one edge in red", ("edge", (1, 2))) + "What is the red line called?",
                   "an edge", ["a face", "a vertex", "a corner"],
                   "The red line is where 2 faces meet. That is an <b>edge</b>."))
    its.append(mcq(cube_pic("cube with a red dot on one corner", ("vertex", 5)) + "What is the red dot on?",
                   "a vertex", ["an edge", "a face", "a side"],
                   "The dot is on a corner where 3 edges meet. A corner of a solid is a <b>vertex</b>. (Two or more are vertices.)"))
    its.append(mcq("What shape is each face of a cube?", "square", ["triangle", "circle", "hexagon"],
                   "Every face of a cube is a square, and all 6 squares are the same size."))
    its.append(mcq(cube_pic("cube seen from the front, right and top") + "How many faces of this cube can you see?", 3, [6, 2, 4],
                   "You can see the front, the top and the right side: <b>3</b> faces. The other 3 faces are hidden."))
    its.append(mcq(prism_pic + "How many faces does this box have?", 6, [3, 4, 8],
                   "This solid is a rectangular prism. It has a front and back, a top and bottom, and a left and right side: <b>6</b> faces."))
    its.append(mcq(prism_pic + "How many edges does this box have?", 12, [9, 8, 4],
                   "4 edges on the front, 4 on the back and 4 joining them: <b>12</b>. Count the 3 dashed edges too."))
    its.append(mcq(prism_pic + "How many vertices does this box have?", 8, [7, 4, 6],
                   "4 vertices on the front and 4 on the back: <b>8</b>. One of them is hidden."))
    its.append(mcq(prism_pic + "How is a cube different from this box?", "Its faces all match",
                   ["It has 8 faces", "It has no edges", "It is flat"],
                   "Both have 6 faces, 12 edges and 8 vertices. A cube's 6 faces are all the same square. This box has long and short faces."))
    T = [rnd.randrange(4) for _ in range(2)]
    its.append(grid_q(rnd, "Which solid is a cube?",
                      [solid(CUBE), solid(PRISM), flat_square(), solid(PYRAMID)], 0,
                      "has 6 faces that are all the same square. One shape is a flat square, not a solid. "
                      "The long box has faces that are not all squares, and the pyramid has triangle faces.",
                      T[0], "four solids labeled A to D", "Picture"))
    its.append(grid_q(rnd, "Which solid is NOT a cube?",
                      [solid(PRISM_TALL, 84), solid(CUBE, 80), solid(CUBE, 52), solid(CUBE_L, 70)], 0,
                      "is a tall box. Its front is not a square, so its faces are not all the same. "
                      "The other three are cubes: one is small and one is drawn from the left, but size and turning do not matter.",
                      T[1], "four solids labeled A to D", "Solid"))
    its.append(mcq("How many edges meet at each vertex of a cube?", 3, [2, 4, 6],
                   "At every corner of a cube, 3 edges meet: one going up or down, one going side to side and one going back."))
    its.append(mcq("Which word means a flat surface of a solid?", "face", ["edge", "vertex", "corner"],
                   "A <b>face</b> is a flat surface. An edge is where 2 faces meet. A vertex is a corner."))
    its.append(mcq("A cube has 6 faces. You can see 3 faces. How many faces are hidden?", 3, [6, 9, 2],
                   "6 − 3 = <b>3</b>. The hidden faces are the back, the bottom and one side."))
    its.append(mcq("A cube has 12 edges. In a picture, 9 edges are solid lines. The rest are dashed. How many are dashed?",
                   3, [12, 21, 4],
                   "12 − 9 = <b>3</b>. Dashed lines show the edges you cannot see."))
    its.append(mcq("Is a square the same as a cube?", "No, a square is flat",
                   ["Yes, they match", "Yes, both have 4 sides", "No, a cube has 4 faces"],
                   "A square is a flat shape with 4 sides. A cube is a solid with 6 square faces."))
    its.append(mcq(cube_pic("cube with 3 hidden edges dashed") + "A cube has 8 vertices. You can see 7 in this picture. How many are hidden?",
                   1, [8, 15, 2],
                   "8 − 7 = <b>1</b>. The hidden vertex is at the back, where the 3 dashed edges meet."))
    assert len(its) == 20, len(its)
    return {"title": "Cubes: faces, edges and vertices", "items": its}


# ============================================================ set 5: real-world shapes and riddles
def set_world(rnd, PP):
    its = []
    its.append(mcq(fig(octagon_sign_svg()) + "A stop sign has 8 sides. What shape is it?", "octagon",
                   ["hexagon", "pentagon", "circle"],
                   "<b>Octa</b> means 8, like the 8 legs of an octopus. A shape with 8 sides is an octagon. A hexagon has only 6."))
    its.append(mcq("A slice of pizza has 2 straight sides and 1 curved crust. Which shape does it look most like?", "triangle",
                   ["circle", "square", "pentagon"],
                   "It has 3 corners and 3 sides, so it looks most like a triangle. It is not a true triangle, because the crust is curved. "
                   "The whole pizza is a circle."))
    its.append(mcq("I have 6 sides and 6 corners. What shape am I?", "hexagon", ["pentagon", "octagon", "cube"],
                   "6 sides make a hexagon. A cube has 6 faces, not 6 sides, and it is a solid."))
    its.append(mcq("I have 3 sides and 3 corners. What shape am I?", "triangle", ["hexagon", "quadrilateral", "pentagon"],
                   "3 sides make a triangle. Do not add the sides and the corners: it has 3 sides, not 6."))
    its.append(mcq("I am a solid with 6 faces. Every face is the same square. What am I?", "cube", ["square", "hexagon", "triangle"],
                   "A solid with 6 faces that are all the same square is a cube. A square is flat, and a hexagon is flat."))
    its.append(mcq("A yield sign has 3 sides. What shape is it?", "triangle", ["quadrilateral", "hexagon", "octagon"],
                   "3 sides make a triangle."))
    its.append(mcq("Home plate on a baseball field has 5 sides. What shape is it?", "pentagon",
                   ["hexagon", "quadrilateral", "octagon"],
                   "5 sides make a pentagon. Home plate looks like a house drawn upside down."))
    its.append(mcq("Each cell in a honeycomb has 6 sides. What shape is each cell?", "hexagon", ["pentagon", "octagon", "cube"],
                   "6 sides make a hexagon."))
    its.append(mcq("A door is a rectangle. Which shape group does a rectangle belong to?", "quadrilateral",
                   ["triangle", "pentagon", "hexagon"],
                   "A rectangle has 4 sides, so it is a quadrilateral."))
    its.append(mcq("A die is a number cube. Each face has a different number of dots. How many faces have dots?", 6, [3, 4, 8],
                   "A die is a cube, and a cube has <b>6</b> faces. That is why a die shows 1 to 6."))
    its.append(mcq("A cereal box has 6 faces. Some faces are big and some are small. Is it a cube?",
                   "No, faces differ", ["Yes, it has 6 faces", "Yes, it is a box", "No, it has 8 faces"],
                   "A cube needs 6 faces that are all the same square. The cereal box has faces of different sizes, so it is not a cube."))
    nm, he, his = PP.next()
    its.append(mcq("%s draws a house: a square with a triangle roof that fits the top. %s traces only the outside line. How many sides does the outline have?"
                   % (nm, cap(he)), 5, [7, 6, 4],
                   "The square gives 3 outside sides (left, bottom, right). The roof gives 2. The line between them is inside. "
                   "3 + 2 = <b>5</b> sides: a pentagon."))
    nm, he, his = PP.next()
    its.append(mcq("%s cuts a square from one corner to the opposite corner. What 2 shapes does %s get?" % (nm, he),
                   "2 triangles", ["2 squares", "2 rectangles", "1 triangle"],
                   "The cut goes corner to corner. Each piece has 3 sides, so you get <b>2 triangles</b>."))
    nm, he, his = PP.next()
    its.append(mcq("%s cuts one corner off a square with one straight cut. How many sides does the paper have now?" % nm,
                   5, [4, 3, 6],
                   "The cut takes away 1 corner and makes 2 new corners: 4 − 1 + 2 = 5 corners. 5 corners means <b>5</b> sides. It is a pentagon now."))
    a, b = PP.next(), PP.next()
    its.append(mcq("%s draws a shape with 4 sides. %s draws a shape with 1 more side. What shape did %s draw?" % (a[0], b[0], b[0]),
                   "pentagon", ["quadrilateral", "hexagon", "triangle"],
                   "4 + 1 = 5 sides. A shape with 5 sides is a pentagon."))
    nm, he, his = PP.next()
    its.append(mcq("%s says every hexagon looks like a honeycomb cell. Is %s right?" % (nm, he),
                   "No, any 6 sides", ["Yes, sides must match", "Yes, or it is a pentagon", "No, it has 8 sides"],
                   "Any closed shape with 6 straight sides is a hexagon. The sides can be different lengths, and it can look long or bent."))
    its.append(mcq("How many corners do 2 triangles have in all?", 6, [3, 5, 4],
                   "Each triangle has 3 corners. 3 + 3 = <b>6</b> corners."))
    nm, he, his = PP.next()
    its.append(mcq("%s uses 1 straw for each side. %s makes a pentagon. How many straws does %s use?" % (nm, cap(he), he), 5, [4, 6, 10],
                   "A pentagon has 5 sides, so %s needs <b>5</b> straws." % nm))
    nm, he, his = PP.next()
    its.append(mcq("%s builds a cube. %s uses a stick for each edge. How many sticks does %s need?" % (nm, cap(he), he), 12, [8, 6, 9],
                   "A cube has <b>12</b> edges, so %s needs 12 sticks. (8 is the number of corners, and 9 is how many edges you can see.)" % nm))
    its.append(mcq("Then %s puts a ball of clay on each corner of the cube. How many clay balls does %s need?" % (nm, he), 8, [12, 6, 4],
                   "A cube has <b>8</b> vertices (corners): 4 on the top and 4 on the bottom."))
    assert len(its) == 20, len(its)
    return {"title": "Real-world shapes and riddles", "items": its}


# ============================================================ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def counting_svg():
    """A pentagon with its corners numbered 1-5 outside the shape."""
    sh = PENT_IR
    cx, cy = 120, 95
    pts = placed(sh, 0, 150, 110, cx, cy)
    el = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='3' stroke-linejoin='round'/>" % (P(pts), FILL, GREEN)]
    mx, my = sum(p[0] for p in pts) / 5, sum(p[1] for p in pts) / 5
    boxes = []
    for i, p in enumerate(pts):
        el.append("<circle cx='%.1f' cy='%.1f' r='5' fill='%s'/>" % (p[0], p[1], RED))
        d = (p[0] - mx, p[1] - my)
        L = math.hypot(*d)
        c = (p[0] + d[0] / L * 20, p[1] + d[1] / L * 20)
        el.append(text(c[0], c[1] + 6, str(i + 1), 17, col=RED))
        boxes.append((c[0] - 7, c[1] - 7, c[0] + 7, c[1] + 7))
    # numbers stay clear of every side and inside the picture
    for b in boxes:
        for i in range(5):
            a, q = pts[i], pts[(i + 1) % 5]
            for t in range(21):
                x, y = a[0] + (q[0] - a[0]) * t / 20.0, a[1] + (q[1] - a[1]) * t / 20.0
                assert not (b[0] - 3 < x < b[2] + 3 and b[1] - 3 < y < b[3] + 3), "number touches a side"
        assert b[0] > 0 and b[1] > 0 and b[2] < 240 and b[3] < 190
    return svg_wrap(240, 190, "".join(el), "pentagon with its 5 corners numbered")


def mini_pair(a, b, rot_a=0, rot_b=0):
    """Two small shapes in one table cell: a regular one and an irregular one."""
    el = []
    for k, (sh, r) in enumerate([(a, rot_a), (b, rot_b)]):
        e, bb = shape_elems(sh, r, 50, 46, 32 + k * 64, 30, sw=2.4)
        assert bb[0] >= 0 and bb[2] <= 128 and bb[1] >= 0 and bb[3] <= 60
        el += e
    return svg_wrap(128, 60, "".join(el), "two %ss" % a["kind"])


def strip_svg(items, label, cw=132, top=104):
    """Row of shapes or solids with a caption under each. items: (draw(cx, cy) -> (el, bb), caption)."""
    el = []
    for k, (f, capt) in enumerate(items):
        e, bb = f(k * cw + cw / 2, top / 2)
        assert bb[0] >= k * cw + 4 and bb[2] <= (k + 1) * cw - 4 and bb[1] >= 2 and bb[3] <= top - 2, (capt, bb)
        assert len(capt) * 8.6 < cw - 6, capt
        el += e
        el.append(text(k * cw + cw / 2, top + 18, capt, 15))
    return svg_wrap(cw * len(items), top + 26, "".join(el), label)


def body_html():
    names = strip_svg([(lambda cx, cy: shape_elems(SQUARE, 45, 80, 80, cx, cy, sw=2.8), "quadrilateral"),
                       (lambda cx, cy: shape_elems(HEX_L, 0, 86, 86, cx, cy, sw=2.8), "hexagon"),
                       (lambda cx, cy: shape_elems(PENT_SLANT, 0, 96, 86, cx, cy, sw=2.8), "pentagon"),
                       (lambda cx, cy: shape_elems(HEX_ARROW, 0, 96, 86, cx, cy, sw=2.8), "hexagon")],
                      "a turned square, an L-shaped hexagon, an uneven pentagon and an arrow-shaped hexagon")
    parts = strip_svg([(lambda cx, cy: solid_elems(CUBE, 88, 84, cx, cy, ("face", 0)), "face"),
                       (lambda cx, cy: solid_elems(CUBE, 88, 84, cx, cy, ("edge", (1, 2))), "edge"),
                       (lambda cx, cy: solid_elems(CUBE, 88, 84, cx, cy, ("vertex", 5)), "vertex")],
                      "three cubes showing a face, an edge and a vertex in red", top=108)
    return (
        "<h2>Count sides and corners</h2>"
        "<p>A <b>side</b> is one straight line of a flat shape. A <b>corner</b> is where 2 sides meet. "
        "Another word for corner is <b>vertex</b>. Every corner makes an <b>angle</b>.</p>"
        "<p>To count, put your finger on one corner. Go around the shape and count each side or corner once. "
        "Stop when you are back at the start.</p>"
        "<figure class='sn-fig'>" + counting_svg() +
        "<figcaption>Start at 1 and go around: 5 corners. There are 5 sides too. A flat shape always has the same number of sides and corners.</figcaption></figure>" +
        ex("Example", "A shape has 6 sides. How many corners and angles does it have?",
           "Sides and corners always match: 6 corners. There is 1 angle at each corner: 6 angles.", "6 corners and 6 angles") +
        "<h2>The name comes from the number of sides</h2>" +
        table(["Shapes", "Name", "Sides", "Corners"], [
            [mini_pair(TRI_EQ, TRI_WIDE), "triangle", "3", "3"],
            [mini_pair(SQUARE, QUAD), "quadrilateral", "4", "4"],
            [mini_pair(PENT_REG, HOUSE), "pentagon", "5", "5"],
            [mini_pair(HEX_REG, HEX_L), "hexagon", "6", "6"],
        ]) +
        "<p>A stop sign has 8 sides. A shape with 8 sides is an <b>octagon</b>. A circle has no straight sides and no corners.</p>"
        "<figure class='sn-fig'>" + names +
        "<figcaption>Turning and uneven sides do not change the name. Only the number of sides does.</figcaption></figure>"
        "<h2>Cubes: faces, edges and vertices</h2>"
        "<p>A <b>cube</b> is a solid, like a die. It is not flat.</p>"
        + table(["Word", "What it means", "A cube has"], [
            ["face", "a flat surface", "6 faces, all the same square"],
            ["edge", "where 2 faces meet", "12 edges"],
            ["vertex", "a corner where edges meet", "8 vertices"],
        ]) +
        "<figure class='sn-fig'>" + parts +
        "<figcaption>Dashed lines show the edges at the back that you cannot see.</figcaption></figure>" +
        table(["Solid", "Faces", "Edges", "Vertices"], [
            ["Cube (all faces are the same square)", "6", "12", "8"],
            ["Rectangular prism (a box like a cereal box)", "6", "12", "8"],
        ]) +
        ex("Example", "In a picture of a cube, you can see 3 faces. How many faces does the cube have?",
           "3 faces are on the back, the bottom and one side. You cannot see them. 3 + 3 = 6.", "6 faces") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting the first corner again at the end", "Stop when you get back to the corner where you started"],
            ["Calling a turned square a diamond, not a quadrilateral", "Count the sides: 4. Turning never changes the name"],
            ["Thinking a hexagon must have equal sides", "Any closed shape with 6 straight sides is a hexagon"],
            ["Thinking a bigger shape has more sides", "Size does not matter. Count the sides"],
            ["Saying a cube has 3 faces", "Count the hidden faces too: a cube has 6"],
            ["Mixing up faces, edges and vertices", "Face = flat surface, edge = line where faces meet, vertex = corner"],
        ])
    )


FAQ = [
    {"q": "What shapes should a 2nd grader know?",
     "a": "Grade 2 students should know triangles, quadrilaterals, pentagons, hexagons and cubes (Common Core 2.G.A.1). They name each flat shape by counting its sides and corners."},
    {"q": "How many faces, edges and vertices does a cube have?",
     "a": "A cube has 6 faces, 12 edges and 8 vertices. All 6 faces are squares of the same size."},
    {"q": "Does a hexagon have to have equal sides?",
     "a": "No. Any closed flat shape with 6 straight sides is a hexagon, even if the sides are different lengths. The same rule works for triangles, quadrilaterals and pentagons."},
    {"q": "What is the difference between a side and a vertex?",
     "a": "A side is a straight line of the shape. A vertex is a corner, the point where 2 sides meet."},
]


def gen():
    rnd = random.Random(215)
    PP = People(rnd)
    sets = [set_count(rnd, PP), set_name(rnd, PP), set_which(rnd, PP), set_cube(rnd, PP), set_world(rnd, PP)]
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
        "country": "us", "subject": "math", "grade": "grade-2", "slug": "shapes-and-attributes", "sort": 15,
        "updated": UPDATED, "pdf_url": "",
        "title": "Shapes and Their Attributes: Sides, Corners, Faces and Cubes",
        "seo_title": "Grade 2 Shapes Worksheets: Triangles, Quadrilaterals, Pentagons, Hexagons and Cubes (2.G.A.1)",
        "short_title": "Shapes and attributes",
        "domain": "Geometry",
        "standard_code": "2.G.A.1",
        "standard_url": "https://www.thecorestandards.org/Math/Content/2/G/A/1/",
        "standard_text": "Recognize and draw shapes having specified attributes, such as a given number of angles or a given number of equal faces. Identify triangles, quadrilaterals, pentagons, hexagons, and cubes.",
        "meta_desc": "Free Grade 2 shapes worksheets with pictures: count sides and corners, name triangles, quadrilaterals, pentagons and hexagons, find shapes with given attributes, and count the faces, edges and vertices of a cube. 100 practice questions with answers.",
        "key_big": "Count the sides to name a shape: 3 triangle, 4 quadrilateral, 5 pentagon, 6 hexagon.",
        "key_sub": "A shape has as many corners as sides. Size, turning and uneven sides never change the name. A cube has 6 square faces, 12 edges and 8 vertices.",
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
