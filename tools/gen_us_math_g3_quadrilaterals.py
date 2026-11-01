# -*- coding: utf-8 -*-
"""
US Grade 3 Math: Quadrilaterals (3.G.A.1)
  python tools/gen_us_math_g3_quadrilaterals.py
HTML attributes use single quotes (no backslashes in the JSON).

Definitions used everywhere (inclusive, as in the lesson):
  quadrilateral  closed flat shape with 4 straight sides
  rectangle      4 right angles
  rhombus        4 equal sides
  square         4 equal sides and 4 right angles (so it is also a rectangle and a rhombus)
  parallelogram  2 pairs of parallel sides
  trapezoid      only shapes with exactly one pair of parallel sides are called trapezoids here,
                 so both common definitions agree. "Trapezoid" is never a wrong choice for a shape
                 in the parallelogram family.
Every drawing is checked: the shape's real geometry must match its name, and the marks
(tick marks, right-angle squares, parallel arrows) are computed from the real geometry.
"""
import json, re, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-3")
UPDATED = "2026-11-01"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#c9c2b8"


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, rnd):
    seen = {correct}
    pick = []
    for c in cands:
        if c in seen or not c:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def mcq_fixed(q, choices, correct, e):
    """Choices keep their order (A B C D, Always Sometimes Never, numbers)."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e}


def mcq_num(q, correct, cands, e):
    ch = sorted(set([correct] + [c for c in cands if c >= 0 and c != correct][:3]))
    assert len(ch) == 4, (q, ch)
    return {"q": q, "c": [str(c) for c in ch], "a": ch.index(correct), "e": e}


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'>%s</svg>" % (w, h, w, h, label, body))


# ------------------------------------------------------------ geometry
def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def norm(v):
    L = math.hypot(v[0], v[1])
    return (v[0] / L, v[1] / L)


def side_lens(pts):
    n = len(pts)
    return [math.hypot(*sub(pts[(i + 1) % n], pts[i])) for i in range(n)]


def angles(pts):
    """Interior angle at each vertex in degrees (convex shapes)."""
    n = len(pts)
    out = []
    for i in range(n):
        u = norm(sub(pts[i - 1], pts[i]))
        v = norm(sub(pts[(i + 1) % n], pts[i]))
        out.append(math.degrees(math.acos(max(-1, min(1, u[0] * v[0] + u[1] * v[1])))))
    return out


def side_angle_diff(pts, i, j):
    """Angle (0..90) between the directions of side i and side j."""
    n = len(pts)
    a = sub(pts[(i + 1) % n], pts[i])
    b = sub(pts[(j + 1) % n], pts[j])
    t = abs(math.degrees(math.atan2(a[1], a[0]) - math.atan2(b[1], b[0]))) % 180
    return min(t, 180 - t)


def facts(pts):
    L = side_lens(pts)
    A = angles(pts)
    eq = max(L) - min(L) < 1e-6 * max(L)
    rights = [i for i, a in enumerate(A) if abs(a - 90) < 1e-6]
    par = [p for p in [(0, 2), (1, 3)] if side_angle_diff(pts, *p) < 1e-6]
    return {"lens": L, "angles": A, "equal": eq, "rights": rights, "par": par}


def quad_name(pts):
    f = facts(pts)
    if f["equal"] and len(f["rights"]) == 4:
        return "square"
    if len(f["rights"]) == 4:
        return "rectangle"
    if f["equal"]:
        return "rhombus"
    if len(f["par"]) == 2:
        return "parallelogram"
    if len(f["par"]) == 1:
        return "trapezoid"
    return "quadrilateral"


# ------------------------------------------------------------ shapes (y goes down, like SVG)
def S(pts, kind, closed=True, curve=None):
    return {"pts": [(float(x), float(y)) for x, y in pts], "kind": kind, "closed": closed, "curve": curve}


def square(s=100):
    return S([(0, 0), (s, 0), (s, s), (0, s)], "square")


def rect(a, b):
    return S([(0, 0), (a, 0), (a, b), (0, b)], "rectangle")


def rhombus(deg, s=100):
    t = math.radians(deg)
    return S([(0, 0), (s, 0), (s + s * math.cos(t), s * math.sin(t)), (s * math.cos(t), s * math.sin(t))], "rhombus")


def para(a, b, deg):
    t = math.radians(deg)
    return S([(0, 0), (a, 0), (a + b * math.cos(t), b * math.sin(t)), (b * math.cos(t), b * math.sin(t))], "parallelogram")


def trap(bottom, top, h, off):
    return S([(0, h), (bottom, h), (off + top, 0), (off, 0)], "trapezoid")


def rtrap(bottom, top, h):
    return S([(0, h), (bottom, h), (top, 0), (0, 0)], "trapezoid")


def kite(w, a, b):
    return S([(0, 0), (w, a), (0, a + b), (-w, a)], "quadrilateral")


def quad(pts):
    return S(pts, "quadrilateral")


def dart():
    return S([(0, 0), (70, 100), (0, 62), (-70, 100)], "dart")


def tri(pts):
    return S(pts, "triangle")


def poly(pts, kind):
    return S(pts, kind)


def regular(n, r=60, start=-90):
    return [(r * math.cos(math.radians(start + 360 * i / n)), r * math.sin(math.radians(start + 360 * i / n)))
            for i in range(n)]


def open_shape():
    return S([(40, 0), (140, 0), (150, 90), (0, 90), (8, 34)], "open", closed=False)


def curved():
    # 3 straight sides and one curved side (from the last point back to the first)
    return S([(0, 100), (150, 100), (150, 0), (40, 0)], "curved", curve=(-35, 50))


TRI1 = tri([(0, 90), (130, 90), (40, 0)])
TRI2 = tri([(0, 0), (120, 30), (30, 100)])
PENT1 = poly([(60, 0), (130, 45), (105, 120), (15, 120), (0, 45)], "pentagon")
PENT2 = poly([(0, 30), (80, 0), (150, 40), (120, 110), (20, 100)], "pentagon")
HEX1 = poly(regular(6), "hexagon")
HEX2 = poly([(30, 0), (110, 0), (150, 50), (110, 100), (30, 100), (0, 50)], "hexagon")
GEN1 = quad([(0, 15), (140, 0), (125, 70), (40, 125)])
ONE_RIGHT = quad([(0, 0), (120, 0), (120, 70), (50, 130)])
KITE1 = kite(70, 25, 100)
KITE2 = kite(50, 35, 120)


def rot_pt(p, deg):
    t = math.radians(deg)
    return (p[0] * math.cos(t) - p[1] * math.sin(t), p[0] * math.sin(t) + p[1] * math.cos(t))


def bez(p0, c, p1, t):
    return ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p1[0],
            (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p1[1])


def placed(sh, rot, bw, bh, cx, cy):
    """Rotate the shape, scale it to fit a bw x bh box and center it at (cx, cy)."""
    pts = [rot_pt(p, rot) for p in sh["pts"]]
    ctl = rot_pt(sh["curve"], rot) if sh["curve"] else None
    outline = pts[:]
    if ctl:
        outline += [bez(pts[-1], ctl, pts[0], t / 10.0) for t in range(11)]
    xs, ys = [p[0] for p in outline], [p[1] for p in outline]
    k = min(bw / (max(xs) - min(xs)), bh / (max(ys) - min(ys)))
    mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2

    def T(p):
        return (cx + (p[0] - mx) * k, cy + (p[1] - my) * k)
    return [T(p) for p in pts], (T(ctl) if ctl else None)


def shape_elems(sh, rot, bw, bh, cx, cy, marks=("ticks", "rights"), sw=3):
    """SVG elements for one shape plus its marks, and the box around everything drawn."""
    pts, ctl = placed(sh, rot, bw, bh, cx, cy)
    n = len(pts)
    el, box = [], list(pts)
    P = lambda ps: " ".join("%.1f,%.1f" % p for p in ps)
    if not sh["closed"]:
        el.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='%g' stroke-linecap='round' "
                  "stroke-linejoin='round'/>" % (P(pts), GREEN, sw))
    elif ctl:
        d = "M" + " L".join("%.1f,%.1f" % p for p in pts) + " Q%.1f,%.1f %.1f,%.1f Z" % (ctl + pts[0])
        el.append("<path d='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>" % (d, FILL, GREEN, sw))
        box += [bez(pts[-1], ctl, pts[0], t / 10.0) for t in range(11)]
    else:
        el.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>"
                  % (P(pts), FILL, GREEN, sw))
    if marks and sh["closed"] and not ctl and n == 4:
        f = facts(pts)
        mk = "stroke='%s' stroke-width='2' fill='none' stroke-linecap='round'" % INK
        # every angle that is not marked must look clearly different from a right angle
        for i, a in enumerate(f["angles"]):
            assert i in f["rights"] or abs(a - 90) >= 10, (sh["kind"], f["angles"])
        tick_at = set()
        if "ticks" in marks:
            groups = []
            for i, L in enumerate(f["lens"]):
                for g in groups:
                    if abs(f["lens"][g[0]] - L) < 1e-6 * L:
                        g.append(i)
                        break
                else:
                    groups.append([i])
            # sides that look equal but are not would be confusing
            for g1 in groups:
                for g2 in groups:
                    if g1 is not g2:
                        a, b = f["lens"][g1[0]], f["lens"][g2[0]]
                        assert abs(a - b) / max(a, b) > 0.12, (sh["kind"], f["lens"])
            cnt = 0
            for g in groups:
                if len(g) < 2:
                    continue
                cnt += 1
                for i in g:
                    a, b = pts[i], pts[(i + 1) % n]
                    d = norm(sub(b, a))
                    nr = (-d[1], d[0])
                    m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
                    tick_at.add(i)
                    for j in range(cnt):
                        o = (j - (cnt - 1) / 2.0) * 5
                        c = (m[0] + d[0] * o, m[1] + d[1] * o)
                        p1, p2 = (c[0] - nr[0] * 6, c[1] - nr[1] * 6), (c[0] + nr[0] * 6, c[1] + nr[1] * 6)
                        el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' %s/>" % (p1 + p2 + (mk,)))
                        box += [p1, p2]
        if "rights" in marks:
            for i in f["rights"]:
                v = pts[i]
                u1, u2 = norm(sub(pts[i - 1], v)), norm(sub(pts[(i + 1) % n], v))
                k = min(10, 0.2 * min(f["lens"][i - 1], f["lens"][i]))
                q1 = (v[0] + u1[0] * k, v[1] + u1[1] * k)
                q2 = (q1[0] + u2[0] * k, q1[1] + u2[1] * k)
                q3 = (v[0] + u2[0] * k, v[1] + u2[1] * k)
                el.append("<polyline points='%s' %s/>" % (P([q1, q2, q3]), mk.replace("stroke-width='2'", "stroke-width='1.6'")))
        if "arrows" in marks:
            for i, j in [(0, 2), (1, 3)]:
                if (i, j) not in f["par"]:
                    assert side_angle_diff(pts, i, j) >= 8, (sh["kind"], "almost parallel")
            for c, (i, j) in enumerate(f["par"]):
                d = norm(sub(pts[i + 1], pts[i]))
                nr = (-d[1], d[0])
                for s_ in (i, j):
                    a, b = pts[s_], pts[(s_ + 1) % n]
                    m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
                    shift = 13 if s_ in tick_at else 0
                    for r in range(c + 1):
                        o = shift + r * 5 - c * 2.5
                        tip = (m[0] + d[0] * (o + 4), m[1] + d[1] * (o + 4))
                        w1 = (tip[0] - d[0] * 7 + nr[0] * 5, tip[1] - d[1] * 7 + nr[1] * 5)
                        w2 = (tip[0] - d[0] * 7 - nr[0] * 5, tip[1] - d[1] * 7 - nr[1] * 5)
                        el.append("<polyline points='%s' %s/>" % (P([w1, tip, w2]), mk))
                        box += [w1, w2, tip]
    if sh["kind"] in ("square", "rectangle", "rhombus", "parallelogram", "trapezoid", "quadrilateral"):
        assert quad_name(pts) == sh["kind"], (sh["kind"], quad_name(pts))
    pad = sw / 2.0 + 1
    bb = (min(p[0] for p in box) - pad, min(p[1] for p in box) - pad,
          max(p[0] for p in box) + pad, max(p[1] for p in box) + pad)
    return el, bb


def shape_svg(sh, rot=0, bw=140, bh=95, marks=("ticks", "rights"), label="quadrilateral"):
    _, bb = shape_elems(sh, rot, bw, bh, 0, 0, marks)
    pad = 6
    W, H = int(math.ceil(bb[2] - bb[0] + 2 * pad)), int(math.ceil(bb[3] - bb[1] + 2 * pad))
    if W == H:
        W += 1                                       # keep figures out of the larger 'square' print size
    el, bb2 = shape_elems(sh, rot, bw, bh, pad - bb[0] + (W - (bb[2] - bb[0] + 2 * pad)) / 2,
                          pad - bb[1] + (H - (bb[3] - bb[1] + 2 * pad)) / 2, marks)
    assert bb2[0] >= 0 and bb2[1] >= 0 and bb2[2] <= W and bb2[3] <= H
    return svg_wrap(W, H, "".join(el), label)


CELL = 118


def grid_svg(items, marks=("ticks", "rights"), label="four shapes labeled A to D"):
    """2 x 2 grid of shapes labeled A-D. items: list of (shape, rot). Square picture."""
    el = []
    W = H = 2 * CELL
    el.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, CELL, H - 4, GRAY))
    el.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, W - 4, CELL, GRAY))
    for k, (sh, rot) in enumerate(items):
        x0, y0 = (k % 2) * CELL, (k // 2) * CELL
        e, bb = shape_elems(sh, rot, 78, 78, x0 + 66, y0 + 65, marks, sw=2.6)
        assert bb[0] >= x0 + 18 and bb[1] >= y0 + 6 and bb[2] <= x0 + CELL - 3 and bb[3] <= y0 + CELL - 3, (sh["kind"], bb)
        el += e
        el.append("<text x='%d' y='%d' font-size='18' font-weight='700' fill='%s'>%s</text>" % (x0 + 6, y0 + 22, INK, "ABCD"[k]))
    return svg_wrap(W, H, "".join(el), label)


def pair_svg(a, b, marks=("ticks", "rights"), label="shape A and shape B"):
    el = []
    W, H = 2 * CELL, CELL
    el.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, CELL, H - 4, GRAY))
    for k, (sh, rot) in enumerate([a, b]):
        x0 = k * CELL
        e, bb = shape_elems(sh, rot, 78, 78, x0 + 66, 62, marks, sw=2.6)
        assert bb[0] >= x0 + 18 and bb[1] >= 3 and bb[2] <= x0 + CELL - 3 and bb[3] <= H - 3, (sh["kind"], bb)
        el += e
        el.append("<text x='%d' y='22' font-size='18' font-weight='700' fill='%s'>%s</text>" % (x0 + 6, INK, "AB"[k]))
    return svg_wrap(W, H, "".join(el), label)


def strip_svg(items, marks=("ticks", "rights", "arrows"), label="shapes"):
    """Lesson figure: a row of shapes with a caption under each. items: (shape, rot, caption).
    Parallel arrows are drawn on trapezoids only (as in the questions)."""
    cw, top = 132, 112
    el = []
    for k, (sh, rot, cap) in enumerate(items):
        mk = marks if (sh["kind"] == "trapezoid" or not marks) else tuple(m for m in marks if m != "arrows")
        e, bb = shape_elems(sh, rot, 92, 84, k * cw + cw / 2, 56, mk, sw=2.8)
        assert bb[0] >= k * cw + 2 and bb[2] <= (k + 1) * cw - 2 and bb[1] >= 2 and bb[3] <= top - 2, (cap, bb)
        el += e
        el.append("<text x='%d' y='%d' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                  % (k * cw + cw / 2, top + 16, INK, cap))
    return svg_wrap(cw * len(items), top + 24, "".join(el), label)


# ------------------------------------------------------------ set 1: is it a quadrilateral?
def set_is_quad(rnd):
    its = []
    Y, N3, N5, N6, OPEN, CURVE = "Yes, 4 sides", "No, 3 sides", "No, 5 sides", "No, 6 sides", "No, it is open", "No, it has a curve"
    plan = [
        (square(), 45, Y, ["No, it is a diamond", N3, N5],
         "It is closed and has 4 straight sides, so it is a quadrilateral. Turning a shape does not change how many sides it has."),
        (dart(), 0, Y, ["No, it caves in", N3, N5],
         "Count the sides: 4 straight sides, and the shape is closed. A quadrilateral can have a corner that points in."),
        (GEN1, 25, Y, ["No, uneven sides", N3, N5],
         "It has 4 straight sides and is closed. The sides do not have to be the same length."),
        (TRI1, 0, N3, [Y, N5, OPEN],
         "It has only 3 sides and 3 vertices. A quadrilateral needs 4 sides."),
        (PENT2, 15, N5, [Y, N6, N3],
         "Count carefully: it has 5 sides, so it is a pentagon, not a quadrilateral."),
        (open_shape(), 0, OPEN, [Y, N5, N3],
         "The two ends do not meet, so the shape is not closed. A quadrilateral must be a closed shape."),
        (curved(), 0, CURVE, [Y, N3, N5],
         "One side is curved. A quadrilateral has 4 <b>straight</b> sides, so this shape is not one."),
        (HEX2, 0, N6, [Y, N5, "No, 8 sides"],
         "It has 6 sides, so it is a hexagon, not a quadrilateral."),
    ]
    for sh, rot, ans, wrong, e in plan:
        its.append(mcq(fig(shape_svg(sh, rot, marks=(), label=sh["kind"] + " shape")) +
                       "Is this shape a quadrilateral?", ans, wrong, e, rnd))
    # count sides / vertices / angles
    its.append(mcq_num(fig(shape_svg(PENT1, -10, marks=(), label="pentagon")) + "How many sides does this shape have?",
                       5, [4, 6, 3], "Touch each side as you count: 5 sides. It is a pentagon."))
    its.append(mcq_num(fig(shape_svg(KITE2, 15, marks=(), label="kite shape")) + "How many vertices (corners) does this shape have?",
                       4, [3, 5, 2], "A vertex is a corner where two sides meet. This shape has 4 vertices."))
    its.append(mcq_num(fig(shape_svg(HEX1, 0, marks=(), label="hexagon")) + "How many angles does this shape have?",
                       6, [4, 5, 8], "There is one angle at each vertex. 6 vertices means 6 angles."))
    its.append(mcq_num(fig(shape_svg(TRI2, 0, marks=(), label="triangle")) + "How many sides does this shape have?",
                       3, [4, 2, 5], "It has 3 sides, so it is a triangle, not a quadrilateral."))
    # pick from 4 pictures
    grids = [
        ("Which shape is a quadrilateral?", [(trap(130, 70, 70, 25), 0), (TRI1, 20), (PENT1, 0), (curved(), 0)], 0,
         "has 4 straight sides and is closed. The others have 3 sides, 5 sides or a curved side."),
        ("Which shape is a quadrilateral?", [(HEX1, 0), (open_shape(), 0), (rect(150, 80), -30), (TRI2, 0)], 2,
         "has 4 straight sides and is closed, even though it is turned. The others have 6 sides, an open gap or 3 sides."),
        ("Which shape is NOT a quadrilateral?", [(square(), 45), (KITE2, 0), (PENT2, 0), (rhombus(60), 0)], 2,
         "has 5 sides. The other three shapes all have 4 straight sides, so they are quadrilaterals."),
        ("Which shape is NOT a quadrilateral?", [(dart(), 0), (trap(140, 60, 80, 20), 180), (curved(), 90), (rect(140, 90), 0)], 2,
         "has a curved side. The other three shapes have 4 straight sides, so they are quadrilaterals."),
    ]
    for q, items, ans, why in grids:
        order = list(range(4))
        rnd.shuffle(order)
        cells = [items[i] for i in order]
        pos = order.index(ans)
        its.append(mcq_fixed(fig(grid_svg(cells, marks=())) + q, ["A", "B", "C", "D"], "ABCD"[pos],
                             "Shape %s %s" % ("ABCD"[pos], why)))
    # words only
    its.append(mcq_num("How many sides does every quadrilateral have?", 4, [3, 5, 6],
                       "<b>Quad</b> means 4. Every quadrilateral has 4 straight sides, 4 vertices and 4 angles."))
    its.append(mcq("Which of these is NOT a quadrilateral?", "triangle", ["square", "rhombus", "trapezoid"],
                   "A triangle has 3 sides. Squares, rhombuses and trapezoids all have 4 sides.", rnd))
    its.append(mcq("Kai drew a closed shape with 4 straight sides. All 4 sides are different lengths. Is it a quadrilateral?",
                   "Yes", ["No, sides must match", "Only if it is a square", "Only with right angles"],
                   "Any closed shape with 4 straight sides is a quadrilateral. The sides can be different lengths and the angles can be any size.", rnd))
    its.append(mcq_num("How many angles does a quadrilateral have?", 4, [2, 3, 8],
                       "A quadrilateral has 4 vertices, and there is an angle at each one: 4 angles."))
    assert len(its) == 20
    rnd.shuffle(its)
    return {"title": "Is it a quadrilateral?", "items": its}


# ------------------------------------------------------------ set 2: name the shape
NAMES5 = ["square", "rectangle", "rhombus", "parallelogram", "trapezoid"]
WHY = {
    "square": "The tick marks show 4 equal sides, and the small squares show 4 right angles. That makes it a square. "
              "It is also a rectangle and a rhombus, but square is the best name because it tells the most.",
    "rectangle": "The small squares show 4 right angles, so it is a rectangle. The tick marks show that only opposite sides "
                 "are equal, so it is not a square.",
    "rhombus": "The tick marks show 4 equal sides, so it is a rhombus. There are no right-angle marks, so it is not a square.",
    "parallelogram": "Opposite sides are equal (and parallel), but there are no right angles and the sides are not all equal. "
                     "It is a parallelogram, not a rectangle or a rhombus.",
    "trapezoid": "The arrows show exactly one pair of parallel sides. The other two sides are not parallel, so it is a trapezoid.",
}
WRONG = {
    "square": ["rhombus", "rectangle", "parallelogram"],
    "rectangle": ["square", "rhombus", "parallelogram"],
    "rhombus": ["square", "rectangle", "parallelogram"],
    "parallelogram": ["rectangle", "rhombus", "square"],
    "trapezoid": ["parallelogram", "rectangle", "rhombus"],
}


def name_q(sh, rot, rnd, size=(140, 95)):
    marks = ("ticks", "rights", "arrows") if sh["kind"] == "trapezoid" else ("ticks", "rights")
    e = WHY[sh["kind"]]
    if rot % 90:
        e += " Turning a shape does not change its name."
    return mcq(fig(shape_svg(sh, rot, size[0], size[1], marks, label=sh["kind"] + " with marks")) +
               "What is the best name for this shape? Use the marks.", sh["kind"], WRONG[sh["kind"]], e, rnd)


def set_name(rnd):
    its = []
    plan = [(square(), 0, (90, 70)), (square(), 45, (120, 110)), (square(), 20, (110, 90)),
            (rect(150, 80), 0, (150, 90)), (rect(150, 70), 90, (90, 110)), (rect(140, 80), -30, (150, 100)),
            (rhombus(60), 60, (110, 100)), (rhombus(70), 0, (150, 95)), (rhombus(55), 30, (150, 90)),
            (para(150, 80, 55), 0, (150, 85)), (para(130, 90, 60), -20, (150, 95)),
            (trap(150, 70, 80, 40), 0, (150, 85)), (rtrap(150, 70, 90), 0, (150, 85)), (trap(150, 60, 75, 20), 20, (150, 95))]
    for sh, rot, size in plan:
        its.append(name_q(sh, rot, rnd, size))
    words = [
        ("A quadrilateral has 4 equal sides and 4 right angles. What is its best name?", "square", ["rhombus", "rectangle", "parallelogram"],
         "4 equal sides and 4 right angles: that is a square. (It is also a rectangle and a rhombus, but square tells the most.)"),
        ("A quadrilateral has 4 right angles. Its opposite sides are equal, but its sides are not all the same length. What is its best name?",
         "rectangle", ["square", "rhombus", "parallelogram"],
         "4 right angles make it a rectangle. The sides are not all equal, so it is not a square."),
        ("A quadrilateral has 4 equal sides but no right angles. What is its best name?", "rhombus", ["square", "rectangle", "parallelogram"],
         "4 equal sides make it a rhombus. With no right angles, it is not a square."),
        ("A quadrilateral has exactly one pair of parallel sides. What is it called?", "trapezoid", ["parallelogram", "rectangle", "rhombus"],
         "Exactly one pair of parallel sides: that is a trapezoid. Parallelograms, rectangles and rhombuses have 2 pairs."),
    ]
    for q, ans, wrong, e in words:
        its.append(mcq(q, ans, wrong, e, rnd))
    its.append(mcq("On a drawing, what does a small square in a corner show?", "a right angle",
                   ["equal sides", "parallel sides", "a vertex to count"],
                   "A small square in a corner marks a right angle, a square corner like the corner of a book."
                   " Tick marks show equal sides, and arrows show parallel sides.", rnd))
    its.append(mcq("On a drawing, what do matching tick marks on two sides show?", "same length",
                   ["right angles", "parallel sides", "different lengths"],
                   "Sides with the same number of tick marks are the same length.", rnd))
    assert len(its) == 20
    rnd.shuffle(its)
    return {"title": "Name the quadrilateral", "items": its}


# ------------------------------------------------------------ set 3: attributes
def set_attr(rnd):
    its = []
    counts = [(rtrap(150, 70, 90), 180, 2, [0, 1, 4], "The marks show right angles at 2 corners only. The other 2 angles are not right angles."),
              (ONE_RIGHT, 15, 1, [0, 2, 4], "Only one corner has the right-angle mark. The other 3 angles are bigger or smaller than a right angle."),
              (rhombus(60), 60, 0, [1, 2, 4], "There are no right-angle marks. A rhombus has 4 equal sides, but its angles are not right angles unless it is a square."),
              (rect(150, 90), 30, 4, [0, 1, 2], "All 4 corners have the right-angle mark. Every rectangle has 4 right angles, even when it is turned.")]
    for sh, rot, n, wrong, e in counts:
        its.append(mcq_num(fig(shape_svg(sh, rot, 140, 95, ("ticks", "rights"), label="quadrilateral with right-angle marks")) +
                           "How many right angles does this shape have?", n, wrong, e))
    grids = [
        ("Which shape has 4 right angles?", [(rect(150, 90), 25), (rhombus(65), 0), (rtrap(150, 70, 90), 0), (para(150, 80, 60), 0)],
         ("ticks", "rights"), "has a right-angle mark in all 4 corners. One shape has only 2 right angles, and the others have none."),
        ("Which shape has 4 equal sides?", [(rhombus(60), 60), (KITE2, 0), (rect(150, 90), 0), (para(150, 80, 60), 0)],
         ("ticks", "rights"), "has the same tick mark on all 4 sides. The others have 2 pairs of equal sides, not 4 equal sides."),
        ("Which shape has exactly one pair of parallel sides?", [(trap(150, 70, 80, 25), 0), (para(150, 80, 60), 0), (rect(150, 90), 0), (rhombus(65), 0)],
         ("arrows",), "has arrows on only one pair of sides. The others have arrows on 2 pairs of sides."),
    ]
    for q, items, marks, why in grids:
        order = list(range(4))
        rnd.shuffle(order)
        cells = [items[i] for i in order]
        pos = order.index(0)
        its.append(mcq_fixed(fig(grid_svg(cells, marks=marks)) + q, ["A", "B", "C", "D"], "ABCD"[pos],
                             "Shape %s %s" % ("ABCD"[pos], why)))
    pairs = [
        ((square(), 45), (rhombus(60), 0), "4 equal sides", ["4 right angles", "No right angles", "Only 2 equal sides"],
         "Both shapes have the same tick mark on all 4 sides. Only the square has right angles."),
        ((square(), 0), (rect(150, 80), 20), "4 right angles", ["4 equal sides", "No right angles", "Only 2 right angles"],
         "Both shapes have right-angle marks in all 4 corners. Only the square has 4 equal sides."),
        ((rhombus(60), 0), (rect(150, 90), 0), "4 sides", ["4 right angles", "4 equal sides", "No equal sides"],
         "Both are quadrilaterals with 4 sides. Only the rectangle has right angles, and only the rhombus has 4 equal sides."),
    ]
    for a, b, ans, wrong, e in pairs:
        its.append(mcq(fig(pair_svg(a, b)) + "What do shape A and shape B both have?", ans, wrong, e, rnd))
    words = [
        ("How many right angles does every rectangle have?", "4", ["2", "1", "0"],
         "A rectangle is a quadrilateral with 4 right angles. That is what makes it a rectangle."),
        ("How many sides of a rhombus are the same length?", "all 4", ["only 2", "only 3", "none"],
         "A rhombus is a quadrilateral with 4 equal sides."),
        ("Which attribute do a square and a rhombus always share?", "4 equal sides", ["4 right angles", "No parallel sides", "Only 2 equal sides"],
         "Both have 4 equal sides. A square also has 4 right angles, but most rhombuses do not."),
        ("Which attribute do a square and a rectangle always share?", "4 right angles", ["4 equal sides", "No right angles", "Only 2 right angles"],
         "Both have 4 right angles. A square also has 4 equal sides, but most rectangles do not."),
        ("Which attribute does every quadrilateral have?", "4 sides", ["4 right angles", "4 equal sides", "2 pairs of parallel sides"],
         "Every quadrilateral has 4 sides. Right angles, equal sides and parallel sides belong only to some quadrilaterals."),
        ("How many pairs of parallel sides does a parallelogram have?", "2", ["1", "0", "4"],
         "A parallelogram has 2 pairs of parallel sides: top and bottom, and left and right. (4 is the number of sides, not pairs.)"),
        ("What does every rectangle have that not every parallelogram has?", "4 right angles",
         ["4 equal sides", "2 pairs of parallel sides", "4 vertices"],
         "All parallelograms have 2 pairs of parallel sides and 4 vertices. A rectangle is the kind with 4 right angles."),
        ("What does every square have that not every rhombus has?", "4 right angles",
         ["4 equal sides", "2 pairs of parallel sides", "4 sides"],
         "Every rhombus already has 4 equal sides. A square is a rhombus that also has 4 right angles."),
        ("What does every square have that not every rectangle has?", "4 equal sides",
         ["4 right angles", "2 pairs of parallel sides", "4 vertices"],
         "Every rectangle already has 4 right angles. A square is a rectangle that also has 4 equal sides."),
        ("A closed shape has 4 straight sides, and all 4 sides are the same length. Which name must fit it?", "rhombus",
         ["square", "rectangle", "none of these"],
         "4 equal sides is all a rhombus needs. It is a square only if it also has 4 right angles, and we do not know that."),
    ]
    for q, ans, wrong, e in words:
        if ans.isdigit():
            its.append(mcq_num(q, int(ans), [int(w) for w in wrong], e))
        else:
            its.append(mcq(q, ans, wrong, e, rnd))
    assert len(its) == 20
    rnd.shuffle(its)
    return {"title": "Sides and angles: shared attributes", "items": its}


# ------------------------------------------------------------ set 4: always, sometimes, never
def set_asn(rnd):
    its = []
    ASN = [
        ("A square is a rectangle.", "Always", "Only when it is flat",
         "A rectangle needs 4 right angles. Every square has 4 right angles, so every square is a rectangle, even when it is turned."),
        ("A square is a rhombus.", "Always", "Only when it is turned",
         "A rhombus needs 4 equal sides. Every square has 4 equal sides, so every square is a rhombus. Turning does not matter."),
        ("A rectangle is a square.", "Sometimes", "Only when it is turned",
         "Only a rectangle with 4 equal sides is a square. A rectangle 6 cm by 3 cm is not a square."),
        ("A rhombus is a square.", "Sometimes", "Only when it is flat",
         "Only a rhombus with 4 right angles is a square. Most rhombuses have no right angles."),
        ("A rectangle is a quadrilateral.", "Always", "Only when it is flat",
         "Every rectangle is a closed shape with 4 straight sides, so it is always a quadrilateral."),
        ("A triangle is a quadrilateral.", "Never", "Only when it is turned",
         "A triangle has 3 sides. A quadrilateral has 4 sides, so a triangle is never a quadrilateral."),
        ("A quadrilateral is a rhombus.", "Sometimes", "Only when it is turned",
         "Only a quadrilateral with 4 equal sides is a rhombus. Many quadrilaterals have sides of different lengths."),
        ("A rhombus has 4 right angles.", "Sometimes", "Only when it is flat",
         "A rhombus has 4 right angles only when it is a square. Most rhombuses have no right angles."),
        ("A rectangle has 4 equal sides.", "Sometimes", "Only when it is turned",
         "Only a rectangle that is a square has 4 equal sides. Most rectangles have 2 long sides and 2 short sides."),
        ("A square has 4 right angles.", "Always", "Only when it is flat",
         "Every square has 4 right angles, even when it is turned to look like a diamond."),
        ("A parallelogram has 4 right angles.", "Sometimes", "Only when it is turned",
         "A parallelogram has 4 right angles only when it is a rectangle. Most parallelograms lean and have no right angles."),
        ("A shape with a curved side is a quadrilateral.", "Never", "Only when it is big",
         "A quadrilateral has 4 straight sides. A shape with a curved side is never a quadrilateral."),
    ]
    for st, ans, fourth, e in ASN:
        its.append(mcq_fixed("Is this true always, sometimes, or never? <b>%s</b>" % st,
                             ["Always", "Sometimes", "Never", fourth], ans, e))
    its.append(mcq("Which names fit every square?", "rectangle and rhombus", ["rectangle only", "rhombus only", "neither"],
                   "A square has 4 right angles, so it is a rectangle. It has 4 equal sides, so it is a rhombus. It is both.", rnd))
    its.append(mcq("Every rhombus is also a ___.", "quadrilateral", ["square", "rectangle", "none of these"],
                   "A rhombus has 4 straight sides, so it is always a quadrilateral. It is a square or a rectangle only when it has 4 right angles.", rnd))
    its.append(mcq("Every rectangle is also a ___.", "parallelogram", ["square", "rhombus", "none of these"],
                   "A rectangle has 2 pairs of parallel sides, so it is always a parallelogram. It is a square or a rhombus only when its sides are all equal.", rnd))
    its.append(mcq(fig(shape_svg(square(), 45, 110, 110, label="square turned on a corner")) +
                   "Kim says this shape is not a square because it is turned. Is she right?", "No, it is a square",
                   ["Yes, it is a diamond", "Yes, it is a rhombus only", "Yes, squares sit flat"],
                   "The marks show 4 equal sides and 4 right angles, so it is a square. Turning a shape never changes its name. "
                   "(It is also a rhombus.)", rnd))
    its.append(mcq("Ben says a square is not a rectangle because a rectangle must have 2 long sides and 2 short sides. Is he right?",
                   "No, a square has 4 right angles", ["Yes, its sides are all equal", "Yes, a square is a rhombus", "Only if it is turned"],
                   "A rectangle only needs 4 right angles. A square has 4 right angles, so it is a rectangle with all sides equal.", rnd))
    its.append(mcq(fig(shape_svg(rhombus(60), 60, 110, 100, label="rhombus standing on a corner")) +
                   "Ava says this shape is a square because all 4 sides are equal. Is she right?", "No, it has no right angles",
                   ["Yes, 4 equal sides is enough", "Yes, it is a turned square", "No, its sides are not equal"],
                   "The tick marks show 4 equal sides, so it is a rhombus. A square also needs 4 right angles, and this shape has none.", rnd))
    its.append(mcq("A rectangle has 4 equal sides. Which is true?", "It is a square",
                   ["It is not a square", "It is not a rhombus", "It is not a quadrilateral"],
                   "4 right angles and 4 equal sides make a square. It is also a rhombus, and it is still a quadrilateral.", rnd))
    its.append(mcq("A rhombus has 4 right angles. Which is true?", "It is a square",
                   ["It cannot be a square", "It is not a rectangle", "It is not a rhombus now"],
                   "4 equal sides and 4 right angles make a square. It is still a rhombus, and it is also a rectangle.", rnd))
    assert len(its) == 20
    rnd.shuffle(its)
    return {"title": "Always, sometimes, never", "items": its}


# ------------------------------------------------------------ set 5: other quadrilaterals and real life
def set_other(rnd):
    its = []
    grids = [
        ([(trap(150, 70, 80, 25), 0), (square(), 45), (rect(150, 80), 0), (rhombus(60), 0)],
         "is a trapezoid. It has no right angles and its sides are not all equal. The others are a square, a rectangle and a rhombus."),
        ([(KITE2, 0), (rhombus(65), 30), (square(), 0), (rect(150, 70), 90)],
         "is a kite shape. Its sides come in 2 pairs of different lengths and it has no right angles. The others are a rhombus, a square and a rectangle."),
        ([(GEN1, 0), (rect(140, 90), 25), (rhombus(60), 60), (square(), 20)],
         "has 4 different side lengths and no right angles. The others are a rectangle, a rhombus and a square."),
    ]
    for items, why in grids:
        order = list(range(4))
        rnd.shuffle(order)
        cells = [items[i] for i in order]
        pos = order.index(0)
        its.append(mcq_fixed(fig(grid_svg(cells)) + "Which quadrilateral is NOT a rectangle, a rhombus, or a square?",
                             ["A", "B", "C", "D"], "ABCD"[pos], "Shape %s %s" % ("ABCD"[pos], why)))
    whys = [
        (para(150, 80, 55), 10, "Why is this shape not a rectangle?", "It has no right angles",
         ["It is turned", "It is too long", "It has no equal sides"],
         "A rectangle needs 4 right angles. This parallelogram has none. Turning or size never decides a shape's name."),
        (rect(150, 80), -20, "Why is this shape not a rhombus?", "Its sides are not all equal",
         ["It has right angles", "It is not tilted", "It has 5 sides"],
         "A rhombus needs 4 equal sides. This rectangle has 2 long sides and 2 short sides. (A rhombus can have right angles: a square does.)"),
        (rhombus(65), 0, "Why is this rhombus not a square?", "It has no right angles",
         ["Its sides are not equal", "It is not turned", "It is too small"],
         "The tick marks show 4 equal sides, but a square also needs 4 right angles. This shape has none."),
        (KITE1, 0, "Why is this kite shape not a rhombus?", "Its sides are not all equal",
         ["It has no right angles", "It stands on a corner", "It has 5 sides"],
         "The tick marks show 2 short equal sides and 2 long equal sides. A rhombus needs all 4 sides equal. A rhombus does not need right angles."),
    ]
    for sh, rot, q, ans, wrong, e in whys:
        its.append(mcq(fig(shape_svg(sh, rot, 140, 95, label="quadrilateral with marks")) + q, ans, wrong, e, rnd))
    its.append(mcq(fig(shape_svg(GEN1, -15, 140, 95, label="quadrilateral with no marks")) +
                   "No sides are equal, no sides are parallel, and there are no right angles. What is the best name for this shape?",
                   "quadrilateral", ["trapezoid", "parallelogram", "rhombus"],
                   "It has 4 straight sides, so it is a quadrilateral. With no parallel sides it is not a trapezoid or a parallelogram, "
                   "and with no equal sides it is not a rhombus.", rnd))
    its.append(mcq("Mia wants to draw a quadrilateral that is not a rectangle, a rhombus, or a square. Which plan works?",
                   "Sides of 3, 4, 5 and 6 cm", ["4 sides of 5 cm each", "4 right angles", "4 equal sides, 4 right angles"],
                   "With 4 different side lengths it cannot be a rhombus or a square. A rectangle needs opposite sides equal, so it is not a rectangle either.", rnd))
    its.append(mcq("Leo draws a quadrilateral with exactly 1 right angle. Which of these names can it have?",
                   "none of these", ["rectangle", "square", "rhombus"],
                   "Rectangles and squares need 4 right angles. If a rhombus has 1 right angle, all 4 of its angles are right angles. "
                   "So a shape with exactly 1 right angle is none of these.", rnd))
    world = [
        ("The bases on a baseball field make a shape with 4 equal sides of 90 feet and 4 right angles. People call it a diamond. "
         "What is its best name?", "square", ["rhombus", "rectangle", "parallelogram"],
         "4 equal sides and 4 right angles make a square. It looks like a diamond only because it is turned."),
        ("A door is 7 feet tall and 3 feet wide. It has 4 right angles. What is its best name?", "rectangle",
         ["square", "rhombus", "parallelogram"],
         "4 right angles make a rectangle. The sides are not all equal, so it is not a square."),
        ("A floor tile has 4 sides, and each side is 8 inches long. Its corners are not right angles. What is its best name?",
         "rhombus", ["square", "rectangle", "parallelogram"],
         "4 equal sides make a rhombus. Without right angles, it is not a square."),
        ("A toy kite has 2 sides that are 30 cm long and 2 sides that are 50 cm long. Is it a rhombus?",
         "No, its sides are not all equal", ["Yes, it looks like a diamond", "Yes, it has 4 sides", "No, it has 3 sides"],
         "A rhombus needs 4 equal sides. This kite has two 30 cm sides and two 50 cm sides. It is a quadrilateral, but not a rhombus."),
        ("A triangle-shaped sign is cut straight across, parallel to its bottom edge. What shape is the bottom piece?",
         "trapezoid", ["triangle", "rectangle", "pentagon"],
         "The bottom piece has 4 sides. The cut and the bottom edge are parallel, but the two slanted sides are not. "
         "Exactly one pair of parallel sides makes a trapezoid."),
        ("A slice of pizza has 2 straight sides and a curved crust. Is it a quadrilateral?",
         "No, it has a curve", ["Yes, it has 4 corners", "Yes, it is closed", "Only if it is big"],
         "A quadrilateral has 4 straight sides. The pizza slice has a curved side, and only 3 sides in all."),
        ("A stop sign has 8 sides. Is it a quadrilateral?", "No, it has 8 sides", ["Yes, it has corners", "Yes, its sides are equal", "No, it has 6 sides"],
         "A quadrilateral has exactly 4 sides. A stop sign has 8 sides, so it is an octagon."),
        ("A picture frame has 4 sides of 10 inches and 4 right angles. Which names fit it?", "square, rectangle and rhombus",
         ["square only", "rectangle only", "rhombus only"],
         "4 right angles make it a rectangle, 4 equal sides make it a rhombus, and both together make it a square. All three names fit."),
        ("A window has 4 right angles. The top and bottom are 4 feet long, and the sides are 2 feet long. Which name does NOT fit?",
         "square", ["rectangle", "quadrilateral", "parallelogram"],
         "It has 4 right angles, so it is a rectangle, a parallelogram and a quadrilateral. Its sides are not all equal, so it is not a square."),
        ("Zoe cuts one corner off a square piece of paper with one straight cut. How many sides does the paper have now?",
         "5", ["4", "3", "6"],
         "The cut takes away 1 corner but adds 1 new side and 2 new corners: 4 + 1 = 5 sides. It is now a pentagon, not a quadrilateral."),
    ]
    for q, ans, wrong, e in world:
        if ans.isdigit():
            its.append(mcq_num(q, int(ans), [int(w) for w in wrong], e))
        else:
            its.append(mcq(q, ans, wrong, e, rnd))
    assert len(its) == 20
    rnd.shuffle(its)
    return {"title": "Other quadrilaterals and real-world shapes", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    yes_no = strip_svg([(GEN1, 10, "4 sides: yes"), (dart(), 0, "4 sides: yes"), (TRI1, 0, "3 sides: no"),
                        (curved(), 0, "curved: no"), (open_shape(), 0, "open: no")], marks=(),
                       label="quadrilaterals and shapes that are not quadrilaterals")
    family = strip_svg([(square(), 0, "square"), (rect(150, 85), 0, "rectangle"), (rhombus(60), 0, "rhombus"),
                        (para(150, 80, 60), 0, "parallelogram"), (trap(150, 70, 80, 25), 0, "trapezoid")],
                       label="square, rectangle, rhombus, parallelogram and trapezoid with marks")
    turned = strip_svg([(square(), 0, "square"), (square(), 45, "still a square"), (rhombus(60), 60, "rhombus")],
                       label="a square, the same square turned, and a rhombus")
    others = strip_svg([(trap(150, 70, 80, 25), 0, "trapezoid"), (KITE2, 0, "kite shape"), (GEN1, 0, "no special name")],
                       label="quadrilaterals that are not rectangles, rhombuses or squares")
    return (
        "<h2>What is a quadrilateral?</h2>"
        "<p>A <b>quadrilateral</b> is a closed flat shape with <b>4 straight sides</b>. It also has 4 vertices (corners) and 4 angles. "
        "<b>Quad</b> means 4. The sides can be any length, and the shape can be turned any way.</p>"
        "<figure class='sn-fig'>" + yes_no +
        "<figcaption>The first two shapes are quadrilaterals. A triangle has only 3 sides, a shape with a curved side does not count, "
        "and an open shape is not closed.</figcaption></figure>"
        "<h2>Read the marks</h2>" +
        table(["Mark", "What it means"], [
            ["Matching tick marks on sides", "Those sides are the same length"],
            ["A small square in a corner", "A right angle (a square corner, like the corner of a book)"],
            ["Matching arrows on sides", "Those sides are <b>parallel</b>: they go the same way and never meet, like train tracks"],
        ]) +
        "<h2>Special quadrilaterals</h2>"
        "<figure class='sn-fig'>" + family +
        "<figcaption>Each shape is named by what it <b>must</b> have.</figcaption></figure>" +
        table(["Shape", "What it must have"], [
            ["Rectangle", "4 right angles"],
            ["Rhombus", "4 equal sides"],
            ["Square", "4 right angles <b>and</b> 4 equal sides"],
            ["Parallelogram", "2 pairs of parallel sides"],
            ["Trapezoid", "exactly 1 pair of parallel sides"],
        ]) +
        table(["Shape", "4 sides", "4 right angles", "4 equal sides", "2 pairs of parallel sides"], [
            ["Square", "Yes", "Yes", "Yes", "Yes"],
            ["Rectangle", "Yes", "Yes", "Sometimes", "Yes"],
            ["Rhombus", "Yes", "Sometimes", "Yes", "Yes"],
            ["Parallelogram", "Yes", "Sometimes", "Sometimes", "Yes"],
            ["Trapezoid", "Yes", "No", "No", "No"],
        ]) +
        "<p>Some books say a trapezoid has <i>at least</i> one pair of parallel sides. Every trapezoid in this unit has exactly one pair, "
        "so both meanings agree.</p>"
        "<h2>One shape, many names</h2>"
        "<p>A square has 4 right angles, so it <b>is</b> a rectangle. It has 4 equal sides, so it <b>is</b> a rhombus. "
        "Shapes in different groups can share attributes. When we ask for the <b>best name</b>, choose the one that tells the most.</p>"
        "<figure class='sn-fig'>" + turned +
        "<figcaption>Turning a shape does not change its name. A turned square still has 4 right angles. "
        "A rhombus with no right angles is not a square.</figcaption></figure>" +
        ex("Example", "A shape has 4 equal sides and 4 right angles. Which names fit?",
           "4 right angles: rectangle. 4 equal sides: rhombus. Both: square. Square is the best name.", "square, rectangle and rhombus") +
        "<h2>Quadrilaterals with no special name</h2>"
        "<p>Many quadrilaterals are not rectangles, rhombuses, or squares. To draw one, give it sides of different lengths and no right angles.</p>"
        "<figure class='sn-fig'>" + others +
        "<figcaption>All three have 4 straight sides, but none has 4 right angles or 4 equal sides.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["A turned square is a diamond, not a square", "Check the marks: 4 equal sides and 4 right angles make a square in any position"],
            ["A square is not a rectangle", "A rectangle needs only 4 right angles. Every square is a rectangle"],
            ["Every rhombus is a square", "A rhombus needs 4 equal sides. It is a square only with 4 right angles"],
            ["Counting a shape with a curved side as a quadrilateral", "All 4 sides must be straight, and the shape must be closed"],
            ["Thinking all 4 sides of a quadrilateral must be equal", "Any closed shape with 4 straight sides counts"],
        ])
    )


FAQ = [
    {"q": "Is a square a rectangle?",
     "a": "Yes. A rectangle is any quadrilateral with 4 right angles, and every square has 4 right angles. A square is a special rectangle whose 4 sides are all equal."},
    {"q": "Is a square a rhombus?",
     "a": "Yes. A rhombus is a quadrilateral with 4 equal sides, and every square has 4 equal sides. A square is a rhombus that also has 4 right angles."},
    {"q": "What is a quadrilateral in 3rd grade math?",
     "a": "A quadrilateral is a closed flat shape with 4 straight sides and 4 angles. Squares, rectangles, rhombuses, parallelograms and trapezoids are all quadrilaterals."},
    {"q": "What quadrilateral is not a rectangle, rhombus, or square?",
     "a": "Any quadrilateral without 4 right angles and without 4 equal sides, such as a trapezoid, a kite shape with two different side lengths, or a shape with 4 different side lengths."},
]


def gen_quadrilaterals():
    rnd = random.Random(42)
    sets = [set_is_quad(rnd), set_name(rnd), set_attr(rnd), set_asn(rnd), set_other(rnd)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
    return {
        "country": "us", "subject": "math", "grade": "grade-3", "slug": "quadrilaterals", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Quadrilaterals: Squares, Rectangles, Rhombuses and More",
        "seo_title": "Grade 3 Quadrilaterals Worksheets: Square, Rectangle, Rhombus, Trapezoid (Shared Attributes)",
        "short_title": "Quadrilaterals",
        "domain": "Geometry",
        "standard_code": "3.G.A.1",
        "standard_url": "https://www.thecorestandards.org/Math/Content/3/G/A/1/",
        "standard_text": "Understand that shapes in different categories (e.g., rhombuses, rectangles, and others) may share attributes (e.g., having four sides), and that the shared attributes can define a larger category (e.g., quadrilaterals). Recognize rhombuses, rectangles, and squares as examples of quadrilaterals, and draw examples of quadrilaterals that do not belong to any of these subcategories.",
        "meta_desc": "Free Grade 3 quadrilaterals worksheets with pictures: what makes a quadrilateral, naming squares, rectangles, rhombuses, parallelograms and trapezoids, shared attributes, always/sometimes/never, and real-world shapes. 100 practice questions with answers.",
        "key_big": "A quadrilateral is a closed shape with 4 straight sides.",
        "key_sub": "Rectangle = 4 right angles. Rhombus = 4 equal sides. A square has both, so a square is also a rectangle and a rhombus. Turning a shape never changes its name.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (graphs, rulers, A-D choices) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_quadrilaterals()
    path = os.path.join(OUT, "quadrilaterals.json")
    with open(path, "w", encoding="utf-8") as f:
        mark_large(u, "(four shapes labeled A to D|shape A and shape B)")
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
