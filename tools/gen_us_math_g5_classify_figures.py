# -*- coding: utf-8 -*-
"""
US Grade 5 Math: Classify Two-Dimensional Figures (5.G.B.3-4)
  python tools/gen_us_math_g5_classify_figures.py
HTML attributes use single quotes (no backslashes in the JSON).

Definitions used everywhere (inclusive, as in the lesson):
  equilateral triangle  3 equal sides
  isosceles triangle    at least 2 equal sides (so every equilateral triangle is isosceles)
  scalene triangle      no equal sides
  acute / right / obtuse triangle: 3 acute angles / 1 right angle / 1 obtuse angle
  parallelogram  2 pairs of parallel sides
  rectangle      parallelogram with 4 right angles
  rhombus        parallelogram with 4 equal sides
  square         4 right angles and 4 equal sides (so it is a rectangle and a rhombus)
  kite           2 pairs of equal sides next to each other (only kites that are not rhombuses are drawn,
                 and "kite" is never a wrong choice for a rhombus or a square)
  trapezoid      only shapes with EXACTLY one pair of parallel sides are called trapezoids, so both common
                 definitions agree. We never ask whether a parallelogram is a trapezoid.
Every drawing is checked: the real geometry must match the shape's name, and the marks
(tick marks, right-angle squares, parallel arrows) are computed from the real geometry.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#f3f7f2"
FILL3 = "#e4efe6"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
FONT = "Arial, Helvetica, sans-serif"


# ------------------------------------------------------------ question helpers
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
    """Choices keep their order (A B C D, always/sometimes/never, region numbers)."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fixed": True}


def mcq_num(q, correct, cands, e):
    ch = sorted(set([correct] + [c for c in cands if c >= 0 and c != correct][:3]))
    assert len(ch) == 4, (q, ch)
    return mcq_fixed(q, [str(c) for c in ch], str(correct), e)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


class Pos:
    """Positions for picture answers (A-D), spread over the set."""

    def __init__(self, rnd):
        self.rnd, self.q = rnd, []

    def next(self):
        if not self.q:
            self.q = [0, 1, 2, 3]
            self.rnd.shuffle(self.q)
        return self.q.pop()


# ------------------------------------------------------------ geometry
def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def norm(v):
    L = math.hypot(v[0], v[1])
    return (v[0] / L, v[1] / L)


def dirv(deg):
    t = math.radians(deg)
    return (math.cos(t), -math.sin(t))


def side_lens(pts):
    n = len(pts)
    return [math.hypot(*sub(pts[(i + 1) % n], pts[i])) for i in range(n)]


def angles(pts):
    n = len(pts)
    out = []
    for i in range(n):
        u = norm(sub(pts[i - 1], pts[i]))
        v = norm(sub(pts[(i + 1) % n], pts[i]))
        out.append(math.degrees(math.acos(max(-1, min(1, u[0] * v[0] + u[1] * v[1])))))
    assert abs(sum(out) - 180 * (n - 2)) < 1e-6, "shape must be convex"
    return out


def side_angle_diff(pts, i, j):
    n = len(pts)
    a = sub(pts[(i + 1) % n], pts[i])
    b = sub(pts[(j + 1) % n], pts[j])
    t = abs(math.degrees(math.atan2(a[1], a[0]) - math.atan2(b[1], b[0]))) % 180
    return min(t, 180 - t)


def eq(a, b):
    return abs(a - b) < 1e-6 * max(a, b)


def facts(pts):
    L = side_lens(pts)
    A = angles(pts)
    n = len(pts)
    rights = [i for i, a in enumerate(A) if abs(a - 90) < 1e-6]
    par = [p for p in [(0, 2), (1, 3)] if n == 4 and side_angle_diff(pts, *p) < 1e-6]
    groups = []
    for i, x in enumerate(L):
        for g in groups:
            if eq(L[g[0]], x):
                g.append(i)
                break
        else:
            groups.append([i])
    return {"lens": L, "angles": A, "rights": rights, "par": par, "groups": groups}


def tri_name(pts):
    f = facts(pts)
    big = max(len(g) for g in f["groups"])
    sides = "equilateral" if big == 3 else "isosceles" if big == 2 else "scalene"
    if f["rights"]:
        ang = "right"
    elif max(f["angles"]) > 90:
        assert max(f["angles"]) >= 110, f["angles"]
        ang = "obtuse"
    else:
        assert max(f["angles"]) <= 78.5, f["angles"]
        ang = "acute"
    return ang + " " + sides


def quad_name(pts):
    f = facts(pts)
    L = f["lens"]
    all_eq = len(f["groups"]) == 1
    if all_eq and len(f["rights"]) == 4:
        return "square"
    if len(f["rights"]) == 4:
        return "rectangle"
    if all_eq:
        return "rhombus"
    if len(f["par"]) == 2:
        return "parallelogram"
    if len(f["par"]) == 1:
        return "trapezoid"
    if (eq(L[0], L[1]) and eq(L[2], L[3])) or (eq(L[1], L[2]) and eq(L[3], L[0])):
        return "kite"
    return "quadrilateral"


def shape_name(pts):
    return tri_name(pts) if len(pts) == 3 else quad_name(pts)


# ------------------------------------------------------------ shapes (y goes down, like SVG)
def S(pts, kind):
    return {"pts": [(float(x), float(y)) for x, y in pts], "kind": kind}


def tri_ang(a, b, kind, base=120):
    """Triangle with angle a at the left end of the base and angle b at the right end."""
    c = 180 - a - b
    side = base * math.sin(math.radians(b)) / math.sin(math.radians(c))
    t = math.radians(a)
    return S([(0.0, 0.0), (float(base), 0.0), (side * math.cos(t), -side * math.sin(t))], kind)


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
    return S([(0, 0), (w, a), (0, a + b), (-w, a)], "kite")


EQUI = tri_ang(60, 60, "acute equilateral")
ISO_AC = tri_ang(70, 70, "acute isosceles")
ISO_AC2 = tri_ang(65, 65, "acute isosceles")
ISO_RT = tri_ang(45, 45, "right isosceles")
ISO_OB = tri_ang(30, 30, "obtuse isosceles")
ISO_OB2 = tri_ang(25, 25, "obtuse isosceles")
SCA_AC = tri_ang(40, 62, "acute scalene")
SCA_RT = tri_ang(90, 35, "right scalene")
SCA_RT2 = tri_ang(90, 58, "right scalene")
SCA_OB = tri_ang(25, 40, "obtuse scalene")
SCA_OB2 = tri_ang(20, 45, "obtuse scalene")

SQ = square()
RECT = rect(150, 80)
RECT2 = rect(140, 70)
RHO = rhombus(60)
RHO2 = rhombus(65)
PARA = para(150, 80, 60)
PARA2 = para(140, 75, 115)
TRAP = trap(150, 70, 80, 40)
TRAP2 = trap(150, 90, 70, 20)
RTRAP = rtrap(150, 80, 80)
KITE = kite(50, 35, 120)
KITE2 = kite(35, 50, 110)


def rot_pt(p, deg):
    t = math.radians(deg)
    return (p[0] * math.cos(t) - p[1] * math.sin(t), p[0] * math.sin(t) + p[1] * math.cos(t))


def placed(sh, rot, bw, bh, cx, cy):
    pts = [rot_pt(p, rot) for p in sh["pts"]]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    k = min(bw / (max(xs) - min(xs)), bh / (max(ys) - min(ys)))
    mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    return [(cx + (p[0] - mx) * k, cy + (p[1] - my) * k) for p in pts]


ARROW_KINDS = ("parallelogram", "trapezoid")


def shape_elems(sh, rot, bw, bh, cx, cy, sw=3):
    """SVG elements for one shape with its marks (computed from the geometry), and its bounding box.
    Tick marks: equal sides (not on plain parallelograms, where the arrows would crowd them).
    Small squares: right angles. Arrows: parallel sides (parallelograms that are not rectangles or
    rhombuses, and trapezoids)."""
    pts = placed(sh, rot, bw, bh, cx, cy)
    n = len(pts)
    assert shape_name(pts) == sh["kind"], (sh["kind"], shape_name(pts))
    f = facts(pts)
    el, box = [], list(pts)
    P = lambda ps: " ".join("%.1f,%.1f" % p for p in ps)
    el.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>" % (P(pts), FILL, GREEN, sw))
    mk = "stroke='%s' stroke-width='2' fill='none' stroke-linecap='round'" % INK
    # every angle that is not marked must look clearly different from a right angle
    for i, a in enumerate(f["angles"]):
        assert i in f["rights"] or abs(a - 90) >= 10, (sh["kind"], f["angles"])
    # sides that look equal but are not would be confusing
    G = f["groups"]
    for g1 in G:
        for g2 in G:
            if g1 is not g2:
                a, b = f["lens"][g1[0]], f["lens"][g2[0]]
                assert abs(a - b) / max(a, b) > 0.09, (sh["kind"], f["lens"])
    tick_at = set()
    cnt = 0
    for g in G:
        if len(g) < 2 or sh["kind"] == "parallelogram":      # parallelograms: arrows only, so the marks do not crowd
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
    for i in f["rights"]:
        v = pts[i]
        u1, u2 = norm(sub(pts[i - 1], v)), norm(sub(pts[(i + 1) % n], v))
        k = min(10, 0.2 * min(f["lens"][i - 1], f["lens"][i]))
        q1 = (v[0] + u1[0] * k, v[1] + u1[1] * k)
        q2 = (q1[0] + u2[0] * k, q1[1] + u2[1] * k)
        q3 = (v[0] + u2[0] * k, v[1] + u2[1] * k)
        el.append("<polyline points='%s' %s/>" % (P([q1, q2, q3]), mk.replace("stroke-width='2'", "stroke-width='1.6'")))
    if n == 4:
        for i, j in [(0, 2), (1, 3)]:
            if (i, j) not in f["par"]:
                assert side_angle_diff(pts, i, j) >= 8, (sh["kind"], "almost parallel")
    if sh["kind"] in ARROW_KINDS:
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
    pad = sw / 2.0 + 1
    bb = (min(p[0] for p in box) - pad, min(p[1] for p in box) - pad,
          max(p[0] for p in box) + pad, max(p[1] for p in box) + pad)
    return el, bb


def shape_svg(sh, rot=0, bw=120, bh=80, label="shape"):
    _, bb = shape_elems(sh, rot, bw, bh, 0, 0)
    pad = 6
    W, H = int(math.ceil(bb[2] - bb[0] + 2 * pad)), int(math.ceil(bb[3] - bb[1] + 2 * pad))
    if W == H:
        W += 1                                       # keep figures out of the larger 'square' print size
    el, bb2 = shape_elems(sh, rot, bw, bh, pad - bb[0] + (W - (bb[2] - bb[0] + 2 * pad)) / 2,
                          pad - bb[1] + (H - (bb[3] - bb[1] + 2 * pad)) / 2)
    assert bb2[0] >= 0 and bb2[1] >= 0 and bb2[2] <= W and bb2[3] <= H
    return svg_wrap(W, H, "".join(el), label)


CELL = 118


def grid_svg(items, label="four shapes labeled A to D"):
    """2 x 2 grid of shapes labeled A-D. items: list of (shape, rot). Square picture (printed large)."""
    el = []
    W = H = 2 * CELL
    el.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, CELL, H - 4, GRAY))
    el.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, W - 4, CELL, GRAY))
    for k, (sh, rot) in enumerate(items):
        x0, y0 = (k % 2) * CELL, (k // 2) * CELL
        e, bb = shape_elems(sh, rot, 76, 76, x0 + 67, y0 + 60, sw=2.6)
        assert bb[0] >= x0 + 20 and bb[1] >= y0 + 4 and bb[2] <= x0 + CELL - 3 and bb[3] <= y0 + CELL - 3, (sh["kind"], bb)
        el += e
        el.append("<text x='%d' y='%d' font-size='18' font-weight='700' fill='%s'>%s</text>" % (x0 + 6, y0 + 22, INK, "ABCD"[k]))
    return svg_wrap(W, H, "".join(el), label)


def strip_svg(items, cw=126, top=96, bw=88, bh=72, label="shapes"):
    """Lesson figure: a row of shapes with a caption under each. items: (shape, rot, caption)."""
    el = []
    for k, (sh, rot, cap) in enumerate(items):
        e, bb = shape_elems(sh, rot, bw, bh, k * cw + cw / 2.0, top / 2.0, sw=2.8)
        assert bb[0] >= k * cw + 2 and bb[2] <= (k + 1) * cw - 2 and bb[1] >= 2 and bb[3] <= top - 2, (cap, bb)
        assert tw(cap, 15) <= cw - 4, cap
        el += e
        el.append("<text x='%.1f' y='%d' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                  % (k * cw + cw / 2.0, top + 16, INK, cap))
    return svg_wrap(int(cw * len(items)), top + 24, "".join(el), label)


# ------------------------------------------------------------ hierarchy diagrams
# Arial Bold advance widths (per 1000 units of font size), for laying out text without a browser
AW = dict(zip("abcdefghijklmnopqrstuvwxyz", [556, 611, 556, 611, 556, 333, 611, 611, 278, 278, 556, 278, 889, 611, 611, 611,
                                              611, 389, 556, 333, 611, 556, 778, 556, 556, 500]))
AW.update(dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", [722, 722, 722, 722, 667, 611, 778, 722, 278, 556, 722, 611, 833, 722, 778, 667,
                                                  778, 722, 667, 611, 722, 667, 944, 667, 667, 611])))
AW.update({" ": 278, "0": 556, "1": 556, "2": 556, "3": 556, "4": 556, "5": 556})


def tw(t, fs):
    """Width of bold Arial text, plus 5% for safety."""
    return sum(AW[c] for c in t) * fs / 1000.0 * 1.05


def inside(b, r, m=3):
    return b[0] >= r[0] + m and b[1] >= r[1] + m and b[2] <= r[2] - m and b[3] <= r[3] - m


def apart(b, r, m=3):
    return b[2] + m <= r[0] or r[2] + m <= b[0] or b[3] + m <= r[1] or r[3] + m <= b[1]


# Nested-box diagram: every group sits inside the group it belongs to.
VW, VH = 400, 178
V_RECTS = {
    "Q": (2, 2, 398, 176),           # quadrilaterals
    "P": (46, 30, 392, 170),         # parallelograms
    "R": (58, 58, 264, 162),         # rectangles
    "H": (166, 58, 380, 162),        # rhombuses
}
V_IN = {1: "Q", 2: "QP", 3: "QPR", 4: "QPH", 5: "QPRH"}       # region number -> the groups it is inside
V_NUM = {1: (24, 104), 2: (366, 44), 3: (112, 128), 4: (322, 128), 5: (215, 128)}


def venn_svg(numbers=True, label="nested diagram of quadrilaterals"):
    s, labels = [], []
    styles = {"Q": (FILL2, GREEN), "P": (FILL3, GREEN), "R": (FILL, GREEN), "H": (FILL, GREEN)}
    box = "<rect x='%d' y='%d' width='%d' height='%d' rx='9' fill='%s' stroke='%s' stroke-width='%g'/>"
    for key in "QPRH":                                   # fills first
        r = V_RECTS[key]
        s.append(box % (r[0], r[1], r[2] - r[0], r[3] - r[1], styles[key][0], "none", 0))
    R, H = V_RECTS["R"], V_RECTS["H"]                    # the overlap (squares) is darker
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (H[0], R[1], R[2] - H[0], R[3] - R[1], "#a9d3b6"))
    for key in "QPRH":                                   # then every outline, so none is hidden
        r = V_RECTS[key]
        s.append(box % (r[0], r[1], r[2] - r[0], r[3] - r[1], "none", styles[key][1], 2.2))

    def text(x, y, t, anchor, groups, fs=15):
        w, h = tw(t, fs), fs * 0.75
        x0 = x if anchor == "start" else x - w if anchor == "end" else x - w / 2
        labels.append(((x0, y - h, x0 + w, y + 2), groups))
        s.append("<text x='%d' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
                 % (x, y, fs, INK, anchor, t))

    text(10, 21, "Quadrilaterals", "start", "Q")
    text(54, 49, "Parallelograms", "start", "QP")
    text(65, 80, "Rectangles", "start", "QPR", 14)
    text(373, 80, "Rhombuses", "end", "QPH", 14)
    text(215, 80, "Squares", "middle", "QPRH", 14)
    if numbers:
        for k, (x, y) in V_NUM.items():
            s.append("<circle cx='%d' cy='%d' r='11' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (x, y, INK))
            s.append("<text x='%d' y='%d' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%d</text>" % (x, y + 5, INK, k))
            labels.append(((x - 11, y - 11, x + 11, y + 11), V_IN[k]))
    for b, groups in labels:
        for key, r in V_RECTS.items():
            if key in groups:
                assert inside(b, r), ("label outside its group", b, key)
            else:
                assert apart(b, r), ("label crosses a group", b, key)
    for i, (b, _) in enumerate(labels):
        for c, _ in labels[i + 1:]:
            assert apart(b, c, 2), ("labels overlap", b, c)
    return svg_wrap(VW, VH, "".join(s), label)


def tree_svg(nodes, edges, W, H, label, fs=15):
    """nodes: key -> (center x, top y, text). Boxes are 30 high. edges: (parent, child)."""
    s, boxes = [], {}
    for k, (cx, y, t) in nodes.items():
        w = tw(t, fs) + 20
        boxes[k] = (cx - w / 2, y, cx + w / 2, y + 30)
        assert boxes[k][0] >= 1 and boxes[k][2] <= W - 1 and y + 30 <= H - 1, (t, boxes[k])
    for a, b in edges:
        A, B = boxes[a], boxes[b]
        x1, y1 = (A[0] + A[2]) / 2, A[3]
        x2, y2 = (B[0] + B[2]) / 2, B[1]
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.4'/>" % (x1, y1, x2, y2, GREEN))
    keys = list(boxes)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            assert apart(boxes[a], boxes[b], 6), (a, b)
    for k, (cx, y, t) in nodes.items():
        b = boxes[k]
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='30' rx='7' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (b[0], y, b[2] - b[0], FILL, GREEN))
        s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (cx, y + 20, fs, INK, t))
    return svg_wrap(W, H, "".join(s), label)


def quad_tree(label="tree diagram of quadrilaterals"):
    nodes = {"Q": (224, 3, "Quadrilaterals"), "P": (140, 51, "Parallelograms"), "O": (318, 51, "Other quadrilaterals"),
             "R": (76, 99, "Rectangles"), "H": (204, 99, "Rhombuses"), "S": (140, 147, "Squares")}
    edges = [("Q", "P"), ("Q", "O"), ("P", "R"), ("P", "H"), ("R", "S"), ("H", "S")]
    return tree_svg(nodes, edges, 412, 180, label)


def tri_tree(label="tree diagram of triangles by sides"):
    nodes = {"T": (150, 3, "Triangles"), "I": (84, 51, "Isosceles"), "C": (226, 51, "Scalene"),
             "E": (84, 99, "Equilateral")}
    edges = [("T", "I"), ("T", "C"), ("I", "E")]
    return tree_svg(nodes, edges, 300, 132, label)


# ------------------------------------------------------------ set 1: triangles
SIDE_E = {
    "equilateral": "The tick marks show that all 3 sides are equal, so it is equilateral.",
    "isosceles": "The tick marks show exactly 2 equal sides, so it is isosceles.",
    "scalene": "There are no tick marks: all 3 sides have different lengths, so it is scalene.",
}
ANG_E = {
    "acute": "All 3 angles are smaller than a right angle, so it is acute.",
    "right": "The small square shows a right angle, so it is a right triangle.",
    "obtuse": "One angle is wider than a right angle, so it is obtuse.",
}


def full_e(kind, extra=""):
    a, s = kind.split()
    return ANG_E[a] + " " + SIDE_E[s] + " Its full name is " + kind + " triangle." + (" " + extra if extra else "")


def set_triangles(rnd):
    its = []
    pos = Pos(rnd)
    q = "What is the full name of this triangle (angles, then sides)?"
    full = [
        (ISO_RT, 135, ["acute isosceles", "right scalene", "obtuse isosceles"],
         "The other 2 angles are acute, but a triangle is named by its largest angle."),
        (SCA_RT, 0, ["right isosceles", "acute scalene", "obtuse scalene"], ""),
        (ISO_OB, 0, ["acute isosceles", "obtuse scalene", "right isosceles"],
         "Having 2 acute angles does not make it acute: look at the largest angle."),
        (SCA_AC, 15, ["acute isosceles", "right scalene", "obtuse scalene"], ""),
        (SCA_OB, 200, ["obtuse isosceles", "acute scalene", "right scalene"], "Turning a triangle does not change its name."),
        (ISO_AC, 180, ["acute equilateral", "obtuse isosceles", "acute scalene"],
         "Only 2 sides have tick marks, so it is not equilateral. Standing on its point does not change its name."),
        (SCA_RT2, 90, ["right isosceles", "obtuse scalene", "acute scalene"], "Turning a triangle does not change its name."),
    ]
    for sh, rot, wrong, extra in full:
        its.append(mcq(fig(shape_svg(sh, rot, label=sh["kind"] + " triangle")) + q, sh["kind"], wrong, full_e(sh["kind"], extra), rnd))
    its.append(mcq(fig(shape_svg(EQUI, 0, 100, 86, label="equilateral triangle")) + "Which names fit this triangle?",
                   "equilateral and isosceles", ["equilateral only", "isosceles only", "scalene"],
                   "The tick marks show 3 equal sides, so it is equilateral. An isosceles triangle has at least 2 equal sides, "
                   "and this one has 3, so it is isosceles too.", rnd))
    its.append(mcq(fig(shape_svg(ISO_AC2, 0, 100, 86, label="isosceles triangle")) + "Classify this triangle by its sides.",
                   "isosceles", ["equilateral", "scalene", "obtuse"],
                   "The tick marks show 2 equal sides, so it is isosceles. The third side has no tick mark, so it is not equilateral. "
                   "(Obtuse describes an angle, and this triangle has no obtuse angle.)", rnd))
    its.append(mcq(fig(shape_svg(SCA_OB2, 0, label="scalene triangle")) + "Classify this triangle by its sides.",
                   "scalene", ["isosceles", "equilateral", "right"],
                   "There are no tick marks and the 3 sides have different lengths, so it is scalene. "
                   "(Right describes an angle, and this triangle has no right angle.)", rnd))
    tgrids = [
        ("Which is a right isosceles triangle?", [(ISO_RT, 180), (SCA_RT, 0), (ISO_AC, 0), (ISO_OB, 0)],
         lambda k: k == "right isosceles",
         "has a right angle (the small square) and 2 equal sides (the tick marks). The other right triangle is scalene, "
         "and the other isosceles triangles are acute and obtuse."),
        ("Which triangle is scalene?", [(SCA_OB, 0), (ISO_AC2, 0), (EQUI, 0), (ISO_RT, 225)],
         lambda k: k.endswith("scalene"),
         "has no equal sides, so it is scalene. The others have tick marks on at least 2 sides, so they are isosceles "
         "(one is also equilateral)."),
    ]
    for q2, items, test, why in tgrids:
        assert [test(sh["kind"]) for sh, _ in items] == [True, False, False, False], q2
        p = pos.next()
        cells = items[1:]
        cells.insert(p, items[0])
        its.append(mcq_fixed(fig(grid_svg(cells, "four triangles labeled A to D")) + q2, ["A", "B", "C", "D"], "ABCD"[p],
                             "Triangle %s %s" % ("ABCD"[p], why)))
    words = [
        ("A triangle has angles of 100°, 40° and 40°. Classify it by its angles.", "obtuse",
         ["acute", "right", "acute and obtuse"],
         "100° is more than 90°, so it is an obtuse triangle. Every triangle has at least 2 acute angles, so name it by its largest angle."),
        ("A triangle has three 60° angles. Classify it by its angles.", "acute",
         ["right", "obtuse", "equilateral"],
         "60° is less than 90°, so all 3 angles are acute: it is an acute triangle. (Equilateral is a name by sides, not by angles.)"),
        ("A triangle has sides of 5 cm, 5 cm and 8 cm. Classify it by its sides.", "isosceles",
         ["scalene", "equilateral", "not a triangle"],
         "2 sides are 5 cm, so it has 2 equal sides. That makes it isosceles."),
        ("A triangle has sides of 6 in, 6 in and 6 in. Which names fit it?", "equilateral and isosceles",
         ["equilateral only", "isosceles only", "scalene"],
         "All 3 sides are equal, so it is equilateral. It has at least 2 equal sides, so it is also isosceles."),
        ("A triangle has sides of 4 m, 7 m and 9 m. Classify it by its sides.", "scalene",
         ["isosceles", "equilateral", "not a triangle"],
         "All 3 sides have different lengths, so it is scalene."),
        ("Can a right triangle also be an obtuse triangle?", "No, only 1 angle can be 90° or more",
         ["Yes, if it is big", "Yes, if it is turned", "Only if it is isosceles"],
         "A right angle and an obtuse angle together are already more than 180°, the total of a triangle's angles. "
         "So a triangle has at most 1 angle that is 90° or more."),
        ("Can a right triangle be isosceles?", "Yes, 2 sides can be equal",
         ["No, it is always scalene", "No, it would be equilateral", "Only if it is obtuse"],
         "A right isosceles triangle has a right angle and 2 equal sides, like half of a square cut corner to corner."),
        ("A roof frame is a triangle. Its two slanted sides are each 12 feet long, and the bottom is 20 feet long. "
         "The top angle is obtuse. What is the full name of the triangle?", "obtuse isosceles",
         ["acute isosceles", "obtuse scalene", "obtuse equilateral"],
         "The top angle is obtuse, so it is an obtuse triangle. The two 12-foot sides are equal, so it is isosceles."),
    ]
    for qq, ans, wrong, e in words:
        its.append(mcq(qq, ans, wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Classify triangles by sides and angles", "items": its}


# ------------------------------------------------------------ set 2: quadrilaterals
BEST = {
    "square": ("square", ["rhombus", "rectangle", "parallelogram"],
               "The tick marks show 4 equal sides and the small squares show 4 right angles, so it is a square. "
               "It is also a rhombus, a rectangle and a parallelogram, but square tells the most."),
    "rectangle": ("rectangle", ["square", "parallelogram", "rhombus"],
                  "The small squares show 4 right angles, so it is a rectangle. Only opposite sides are equal, so it is not a square. "
                  "It is also a parallelogram, but rectangle tells more."),
    "rhombus": ("rhombus", ["square", "rectangle", "trapezoid"],
                "The tick marks show 4 equal sides, so it is a rhombus. It has no right angles, so it is not a square."),
    "parallelogram": ("parallelogram", ["rectangle", "rhombus", "trapezoid"],
                      "The arrows show 2 pairs of parallel sides, so it is a parallelogram. It has no right angles (not a rectangle) "
                      "and its sides are not all equal (not a rhombus)."),
    "trapezoid": ("trapezoid", ["parallelogram", "rectangle", "rhombus"],
                  "The arrows show exactly 1 pair of parallel sides. The other 2 sides are not parallel, so it is a trapezoid, not a parallelogram."),
    "kite": ("kite", ["rhombus", "parallelogram", "trapezoid"],
             "The tick marks show 2 pairs of equal sides next to each other, so it is a kite. Its sides are not all equal, "
             "so it is not a rhombus, and it has no parallel sides."),
}


def set_quads(rnd):
    its = []
    pos = Pos(rnd)
    q = "What is the best name for this quadrilateral?"
    for sh, rot, extra in [(SQ, 45, "Turning it on a corner does not make it a different shape."), (RECT, 0, ""),
                           (RHO, 0, ""), (RHO2, 90, "Standing it on a point does not change its name."), (PARA, 0, ""),
                           (TRAP, 0, ""), (RTRAP, 0, "It has 2 right angles, but a rectangle needs 4."), (KITE, 0, "")]:
        ans, wrong, e = BEST[sh["kind"]]
        if extra:
            e += " " + extra
        its.append(mcq(fig(shape_svg(sh, rot, label=sh["kind"] + " with marks")) + q, ans, wrong, e, rnd))
    nf = [
        (RECT2, 15, "rhombus", ["rectangle", "parallelogram", "quadrilateral"],
         "It has 4 right angles, so it is a rectangle, a parallelogram and a quadrilateral. Its sides are not all equal, so it is not a rhombus."),
        (RHO2, 0, "rectangle", ["rhombus", "parallelogram", "quadrilateral"],
         "It has 4 equal sides, so it is a rhombus, a parallelogram and a quadrilateral. It has no right angles, so it is not a rectangle."),
        (PARA2, 0, "rectangle", ["parallelogram", "quadrilateral", "polygon"],
         "It has 2 pairs of parallel sides, so it is a parallelogram, a quadrilateral and a polygon. It has no right angles, so it is not a rectangle."),
    ]
    for sh, rot, ans, others, e in nf:
        its.append(mcq(fig(shape_svg(sh, rot, label=sh["kind"] + " with marks")) + "Which name does NOT fit this shape?", ans, others, e, rnd))
    its.append(mcq(fig(shape_svg(SQ, 0, 90, 90, label="square with marks")) + "Which names fit this shape?",
                   "square, rectangle and rhombus", ["square only", "square and rhombus only", "square and rectangle only"],
                   "4 right angles make it a rectangle. 4 equal sides make it a rhombus. Both together make it a square, so all three names fit.", rnd))
    grids = [
        ("Which shape is a rhombus but not a square?", [(RHO, 0), (SQ, 45), (SQ, 0), (RECT, 0)],
         "has 4 equal sides but no right angles. The two squares are rhombuses too, but they are squares, and the rectangle is not a rhombus."),
        ("Which shape is a parallelogram but not a rectangle?", [(PARA, 0), (RECT, 0), (SQ, 20), (TRAP2, 0)],
         "has 2 pairs of parallel sides and no right angles. The rectangle and the square have 4 right angles, "
         "and the trapezoid has only 1 pair of parallel sides."),
        ("Which shape has exactly 1 pair of parallel sides?", [(TRAP2, 0), (PARA2, 0), (RHO, 0), (KITE2, 0)],
         "is a trapezoid: only its top and bottom are parallel. The parallelogram and the rhombus have 2 pairs, and the kite has none."),
    ]
    for q2, items, why in grids:
        p = pos.next()
        cells = items[1:]
        cells.insert(p, items[0])
        its.append(mcq_fixed(fig(grid_svg(cells)) + q2, ["A", "B", "C", "D"], "ABCD"[p], "Shape %s %s" % ("ABCD"[p], why)))
    words = [
        ("What must every rhombus have?", "4 equal sides", ["4 right angles", "a point at the top", "1 pair of parallel sides"],
         "A rhombus is a parallelogram with 4 equal sides. It does not need right angles, and it can be turned any way."),
        ("What must every rectangle have?", "4 right angles", ["2 long and 2 short sides", "4 equal sides", "1 pair of parallel sides"],
         "A rectangle is a parallelogram with 4 right angles. Its sides may all be equal: then it is a square."),
        ("A floor tile has 4 equal sides. None of its angles are right angles. What is its best name?", "rhombus",
         ["square", "rectangle", "kite"],
         "4 equal sides make a rhombus. With no right angles, it is not a square."),
        ("A tabletop has 4 right angles. It is 6 feet long and 3 feet wide. What is its best name?", "rectangle",
         ["square", "rhombus", "trapezoid"],
         "4 right angles make a rectangle. The sides are not all equal, so it is not a square."),
    ]
    for qq, ans, wrong, e in words:
        its.append(mcq(qq, ans, wrong, e, rnd))
    its.append(mcq_num("How many pairs of parallel sides does every parallelogram have?", 2, [1, 4, 0],
                       "A parallelogram has 2 pairs of parallel sides: each side is parallel to the side across from it. (4 is the number of sides.)"))
    assert len(its) == 20, len(its)
    return {"title": "Name quadrilaterals by their properties", "items": its}


# ------------------------------------------------------------ set 3: the hierarchy diagram
REG_E = {
    1: "It is a quadrilateral but not a parallelogram, so it goes in region 1, outside the Parallelograms box.",
    2: "It is a parallelogram, but it has no right angles and its sides are not all equal. So it is not a rectangle or a rhombus: region 2.",
    3: "It is a rectangle but not a rhombus (its sides are not all equal), so it goes in region 3.",
    4: "It is a rhombus but not a rectangle (no right angles), so it goes in region 4.",
    5: "It is both a rectangle and a rhombus, so it goes where the two boxes overlap: region 5, the squares.",
}


def region_q(text, ans, wrong, extra="", e=None):
    ch = sorted([ans] + wrong)
    return mcq_fixed(fig(venn_svg(label="nested diagram of quadrilaterals with regions 1 to 5")) + text,
                     ["region %d" % c for c in ch], "region %d" % ans, e or (REG_E[ans] + (" " + extra if extra else "")))


def set_hierarchy(rnd):
    its = []
    rq = "In which region of the diagram does it belong?"
    its.append(region_q("A quadrilateral has 4 equal sides and 4 right angles. " + rq, 5, [3, 4, 2],
                        "A square belongs to every box: rectangles, rhombuses, parallelograms and quadrilaterals."))
    its.append(region_q("A quadrilateral has 4 right angles. Its sides are 8 cm, 3 cm, 8 cm and 3 cm. " + rq, 3, [5, 2, 1]))
    its.append(region_q("A quadrilateral has 4 equal sides and no right angles. " + rq, 4, [5, 2, 1]))
    its.append(region_q("A quadrilateral has 2 pairs of parallel sides, no right angles, and sides of 9 cm, 5 cm, 9 cm and 5 cm. " + rq,
                        2, [3, 4, 1]))
    its.append(region_q("A quadrilateral has exactly 1 pair of parallel sides. " + rq, 1, [2, 3, 4],
                        "With only 1 pair of parallel sides it is a trapezoid, not a parallelogram."))
    its.append(region_q("A square is turned so that it stands on one corner. " + rq, 5, [4, 2, 1],
                        "Turning does not change its sides or angles, so it is still a square."))
    its.append(region_q("A kite has 2 short equal sides, 2 long equal sides, and no parallel sides. " + rq, 1, [2, 4, 5],
                        "A kite like this has no parallel sides at all."))
    its.append(region_q("Which region holds the shapes that are both rectangles and rhombuses?", 5, [2, 3, 4],
                        e="Region 5 is where the Rectangles box and the Rhombuses box overlap. These shapes have 4 right angles "
                          "and 4 equal sides: they are the squares."))
    vf = fig(venn_svg(label="nested diagram of quadrilaterals with regions 1 to 5"))
    its.append(mcq(vf + "Regions 3 and 5 together make up which group?", "rectangles", ["squares", "rhombuses", "parallelograms"],
                   "The Rectangles box covers region 3 and region 5. So every square (region 5) is a rectangle.", rnd))
    its.append(mcq(vf + "Regions 4 and 5 together make up which group?", "rhombuses", ["squares", "rectangles", "quadrilaterals"],
                   "The Rhombuses box covers region 4 and region 5. So every square (region 5) is a rhombus.", rnd))
    its.append(mcq(vf + "Kai draws a shape that belongs in region 5. Which names fit his shape?", "every name in the diagram",
                   ["square only", "square and rhombus only", "square and rectangle only"],
                   "Region 5 is inside all 4 boxes. The shape is a square, a rectangle, a rhombus, a parallelogram and a quadrilateral.", rnd))
    tf = fig(quad_tree())
    its.append(mcq(tf + "Squares are below both Rectangles and Rhombuses in the diagram. What does this show?",
                   "Every square is both", ["Squares are bigger", "Every rectangle is a square", "Squares are neither"],
                   "Each line going down leads to a smaller group inside the group above it. Squares are under both, so every square is a rectangle and every square is a rhombus.", rnd))
    its.append(mcq(tf + "Which group in the diagram contains all the others?", "quadrilaterals",
                   ["squares", "parallelograms", "rectangles"],
                   "Quadrilaterals is at the top. Every shape below it has 4 sides, so every shape in the diagram is a quadrilateral.", rnd))
    its.append(mcq(tf + "Which statement does the diagram show?", "All rhombuses are parallelograms.",
                   ["All parallelograms are rhombuses.", "All rhombuses are squares.", "All rhombuses are rectangles."],
                   "Rhombuses is below Parallelograms, so every rhombus is a parallelogram. The other statements go the wrong way or across.", rnd))
    its.append(mcq(tf + "A shape is in the Rhombuses group. Which groups must it also be in?", "parallelograms and quadrilaterals",
                   ["squares", "rectangles and squares", "none"],
                   "Follow the lines up from Rhombuses: Parallelograms, then Quadrilaterals. A rhombus is a square only if it has 4 right angles.", rnd))
    its.append(mcq(tf + "A shape is in the Parallelograms group. Must it also be in the Rectangles group?",
                   "No, only with 4 right angles", ["Yes, always", "Yes, it has 4 sides", "No, never"],
                   "Properties pass down, not up. A parallelogram is a rectangle only if it has 4 right angles.", rnd))
    tt = fig(tri_tree())
    its.append(mcq(tt + "In this diagram, an isosceles triangle has at least 2 equal sides. Which statement is true?",
                   "All equilateral triangles are isosceles.",
                   ["All isosceles triangles are equilateral.", "Some scalene triangles are isosceles.", "No equilateral triangle is isosceles."],
                   "Equilateral is below Isosceles: 3 equal sides means at least 2 equal sides. Not every isosceles triangle has 3 equal sides.", rnd))
    its.append(mcq(tt + "A triangle has sides of 5 cm, 5 cm and 7 cm. Which groups in the diagram does it belong to?",
                   "triangles and isosceles", ["isosceles only", "triangles, isosceles, equilateral", "triangles and scalene"],
                   "It has exactly 2 equal sides, so it is in Isosceles, and that is inside Triangles. It is not equilateral.", rnd))
    its.append(mcq(tt + "A triangle has 3 sides of 4 cm. Which groups in the diagram does it belong to?",
                   "triangles, isosceles, equilateral", ["equilateral only", "triangles and equilateral", "triangles and scalene"],
                   "It is equilateral. Follow the lines up: equilateral triangles are isosceles, and isosceles triangles are triangles.", rnd))
    its.append(mcq(tt + "Why is there no line between Scalene and Isosceles?", "No triangle is both",
                   ["Scalene triangles are isosceles", "They are the same group", "All triangles are scalene"],
                   "A scalene triangle has no equal sides and an isosceles triangle has at least 2. A triangle cannot be both.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "The hierarchy diagram: where does each shape belong?", "items": its}


# ------------------------------------------------------------ set 4: always, sometimes, never
def set_asn(rnd):
    its = []
    ASN = [
        ("An equilateral triangle is isosceles.", "Always", "Only if it is turned",
         "An isosceles triangle has at least 2 equal sides. An equilateral triangle has 3, so it is always isosceles."),
        ("An isosceles triangle is equilateral.", "Sometimes", "Only if it is big",
         "Only an isosceles triangle whose third side is also equal is equilateral. Sides of 5, 5 and 8 cm make an isosceles triangle that is not equilateral."),
        ("A right triangle is obtuse.", "Never", "Only if it is turned",
         "A triangle has only 1 angle that is 90° or more. A right triangle already has its 90° angle, so it can never also have an obtuse angle."),
        ("A right triangle is isosceles.", "Sometimes", "Only if it is turned",
         "Half of a square cut corner to corner is a right isosceles triangle. A right triangle with sides 3, 4 and 5 is scalene."),
        ("A scalene triangle is isosceles.", "Never", "Only if it is big",
         "A scalene triangle has no equal sides, and an isosceles triangle has at least 2. A triangle cannot be both."),
        ("An equilateral triangle is a right triangle.", "Never", "Only if it is turned",
         "Each angle of an equilateral triangle is 60°, so none of them is a right angle."),
        ("An obtuse triangle is scalene.", "Sometimes", "Only if it is big",
         "Sides of 4, 5 and 8 make an obtuse scalene triangle, but a triangle with 2 equal sides and a wide top angle is obtuse isosceles."),
        ("A rhombus is a parallelogram.", "Always", "Only if it is turned",
         "A rhombus is a parallelogram with 4 equal sides, so every rhombus is a parallelogram."),
        ("A parallelogram is a rectangle.", "Sometimes", "Only if it is big",
         "Only a parallelogram with 4 right angles is a rectangle. Most parallelograms lean and have no right angles."),
        ("A square is a parallelogram.", "Always", "Only if it is turned",
         "A square is a rectangle, and every rectangle is a parallelogram. The property passes down, so a square has 2 pairs of parallel sides too."),
        ("A rectangle is a rhombus.", "Sometimes", "Only if it is turned",
         "Only a rectangle with 4 equal sides (a square) is a rhombus. A 6 cm by 3 cm rectangle is not a rhombus."),
        ("A quadrilateral with exactly 1 pair of parallel sides is a parallelogram.", "Never", "Only if it is big",
         "A parallelogram needs 2 pairs of parallel sides. A shape with exactly 1 pair is a trapezoid, never a parallelogram."),
    ]
    for st, ans, fourth, e in ASN:
        its.append(mcq_fixed("Is this true always, sometimes, or never? <b>%s</b>" % st,
                             ["Always", "Sometimes", "Never", fourth], ans, e))
    TF = ["True", "False: only some are", "False: none are", "True only if turned"]
    allq = [
        ("All squares are rectangles.", "True",
         "A rectangle needs 4 right angles, and every square has 4 right angles."),
        ("All rectangles are squares.", "False: only some are",
         "Only rectangles with 4 equal sides are squares. A 6 cm by 3 cm rectangle is not a square."),
        ("All squares are rhombuses.", "True",
         "A rhombus needs 4 equal sides, and every square has 4 equal sides, even when it sits flat."),
        ("All parallelograms are rhombuses.", "False: only some are",
         "Only parallelograms with 4 equal sides are rhombuses. Properties pass down from parallelograms to rhombuses, not up."),
        ("All right triangles are scalene.", "False: only some are",
         "A right triangle can have 2 equal sides: that is a right isosceles triangle."),
        ("All isosceles triangles are acute.", "False: only some are",
         "An isosceles triangle can have a right angle or an obtuse angle at the top. Only some isosceles triangles are acute."),
    ]
    for st, ans, e in allq:
        its.append(mcq("True or false? <b>%s</b>" % st, ans, [c for c in TF if c != ans], e, rnd))
    its.append(mcq(fig(shape_svg(SQ, 45, 90, 90, label="square standing on a corner")) +
                   "Max says this shape is a rhombus, so it cannot be a square. Is he right?", "No, it is both",
                   ["Yes, it is a diamond", "Yes, a square sits flat", "No, it is only a square"],
                   "The marks show 4 equal sides and 4 right angles. 4 equal sides make it a rhombus, and with 4 right angles it is also a square. "
                   "Turning does not change its name.", rnd))
    its.append(mcq(fig(shape_svg(ISO_RT, 180, 110, 70, label="right isosceles triangle")) +
                   "Lily says a triangle can be right or isosceles, but not both. Is she right?", "No, this one is both",
                   ["Yes, it must be one", "Yes, it is only right", "No, it is equilateral"],
                   "The small square shows a right angle and the tick marks show 2 equal sides. One name is for angles and one is for sides, "
                   "so a triangle can have both: right isosceles.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Always, sometimes, never: true or false?", "items": its}


# ------------------------------------------------------------ set 5: properties pass down, clues, fix the mistake
def set_reason(rnd):
    its = []
    W = [
        ("All rectangles have 4 right angles, and all squares are rectangles. What must be true?",
         "All squares have 4 right angles", ["Some squares have right angles", "All rectangles have equal sides", "Squares have no right angles"],
         "A square is a kind of rectangle, so it gets every property of a rectangle, including 4 right angles."),
        ("All parallelograms have opposite sides that are parallel. Which shapes must have this too?",
         "rectangles, rhombuses and squares", ["only parallelograms", "only rectangles", "trapezoids and kites"],
         "Rectangles, rhombuses and squares are all kinds of parallelograms, so the property passes down to all of them."),
        ("All squares have 4 equal sides. Does that mean all rectangles have 4 equal sides?",
         "No, properties pass down, not up", ["Yes, squares are rectangles", "Yes, all rectangles match", "No, rectangles have 3"],
         "A square is a special rectangle. What is true for every rectangle is true for squares, but not the other way around."),
        ("All rhombuses have 4 equal sides. Which shape must also have 4 equal sides?", "square",
         ["rectangle", "parallelogram", "trapezoid"],
         "Every square is a rhombus, so a square gets the 4 equal sides of a rhombus."),
        ("Opposite sides of every parallelogram are equal in length. Which shape must also have opposite sides equal?", "rectangle",
         ["trapezoid", "kite", "any quadrilateral"],
         "A rectangle is a kind of parallelogram, so it has every property of a parallelogram. Trapezoids and kites are not parallelograms."),
        ("All isosceles triangles have at least 2 equal sides. Which triangle must also have at least 2 equal sides?", "equilateral",
         ["scalene", "right", "obtuse"],
         "Every equilateral triangle is isosceles, so it has at least 2 equal sides (in fact, 3)."),
    ]
    for q, ans, wrong, e in W:
        its.append(mcq(q, ans, wrong, e, rnd))
    clues = [
        ("I have 4 sides and 4 right angles. My sides are not all equal. What is my best name?", "rectangle",
         ["square", "rhombus", "parallelogram"],
         "4 right angles make a rectangle. The sides are not all equal, so it is not a square. Rectangle tells more than parallelogram."),
        ("I have 2 pairs of parallel sides and no right angles. My sides are not all equal. What is my best name?", "parallelogram",
         ["rectangle", "rhombus", "trapezoid"],
         "2 pairs of parallel sides make a parallelogram. No right angles: not a rectangle. Sides not all equal: not a rhombus."),
        ("I have 4 equal sides, and one of my angles is a right angle. What is my best name?", "square",
         ["rhombus", "rectangle", "kite"],
         "4 equal sides make a rhombus. A rhombus is a parallelogram, and when a parallelogram has 1 right angle, all 4 of its angles are right angles. "
         "So it is a square."),
        ("I have 3 sides. Two of my sides are equal, and one of my angles is a right angle. What am I?", "right isosceles triangle",
         ["right scalene triangle", "acute isosceles triangle", "equilateral triangle"],
         "A right angle makes it a right triangle, and 2 equal sides make it isosceles."),
        ("I have 4 sides. Two pairs of my sides are equal, and each pair is next to each other. I have no parallel sides. What am I?", "kite",
         ["rhombus", "parallelogram", "rectangle"],
         "2 pairs of equal sides next to each other make a kite. With no parallel sides it is not a parallelogram, so it is not a rhombus or a rectangle."),
    ]
    for q, ans, wrong, e in clues:
        its.append(mcq(q, ans, wrong, e, rnd))
    fix = [
        ("Ella says, \"All rectangles are squares.\" Which change makes her statement true?", "All squares are rectangles.",
         ["All rectangles are rhombuses.", "No squares are rectangles.", "No rectangles are squares."],
         "A square has 4 right angles, so every square is a rectangle. But most rectangles do not have 4 equal sides."),
        ("Omar says, \"All parallelograms are rhombuses.\" Which change makes his statement true?", "Some parallelograms are rhombuses.",
         ["All parallelograms are squares.", "No rhombus is a parallelogram.", "All rhombuses are squares."],
         "Only parallelograms with 4 equal sides are rhombuses. (Every rhombus is a parallelogram, but not the other way around.)"),
        ("Nora says, \"An equilateral triangle is not isosceles.\" Which change makes her statement true?",
         "An equilateral triangle is isosceles.",
         ["An equilateral triangle is obtuse.", "An equilateral triangle is scalene.", "An equilateral triangle is right."],
         "Isosceles means at least 2 equal sides. An equilateral triangle has 3 equal sides, so it is isosceles too."),
        ("Leo says, \"A rhombus has to stand on a point like a diamond.\" Which statement is correct?",
         "A rhombus can be turned any way.",
         ["A rhombus must stand on a point.", "A rhombus is never a square.", "A rhombus has no equal sides."],
         "A rhombus only needs 4 equal sides. Turning it does not change that. A square sitting flat is a rhombus too."),
    ]
    for q, ans, wrong, e in fix:
        its.append(mcq(q.replace('"', "&quot;"), ans, wrong, e, rnd))
    world = [
        ("A tile maker has two bins: one for rectangles and one for rhombuses. A tile has 4 equal sides and 4 right angles. "
         "Which bin can it go in?", "either bin", ["the rectangle bin only", "the rhombus bin only", "neither bin"],
         "The tile is a square. 4 right angles make it a rectangle, and 4 equal sides make it a rhombus, so it belongs in both groups."),
        ("A garden bed has 4 sides. The front edge and the back edge are parallel, but the two side edges are not. What is its best name?",
         "trapezoid", ["parallelogram", "rectangle", "rhombus"],
         "Exactly 1 pair of parallel sides makes a trapezoid. A parallelogram needs 2 pairs."),
        ("A sail is a triangle. One angle is a right angle, and its sides are 3 m, 4 m and 5 m. What is its full name?",
         "right scalene triangle", ["right isosceles triangle", "acute scalene triangle", "obtuse scalene triangle"],
         "It has a right angle, so it is right. All 3 sides are different, so it is scalene."),
        ("Maya sorts these shapes into the group \"has 4 right angles\": a square, a rhombus with no right angles, a rectangle and a trapezoid. "
         "Which shapes go in the group?", "the square and the rectangle",
         ["the square only", "the rectangle only", "the square and the rhombus"],
         "Every rectangle has 4 right angles, and a square is a rectangle, so both go in. The rhombus and the trapezoid do not have 4 right angles."),
        ("A baseball diamond has 4 sides of 90 feet and 4 right angles. People call it a diamond. Which names fit it?",
         "square, rectangle and rhombus", ["rhombus only", "square only", "kite only"],
         "4 equal sides and 4 right angles make a square, so it is also a rectangle and a rhombus. It only looks like a diamond because it is turned."),
    ]
    for q, ans, wrong, e in world:
        its.append(mcq(q.replace('"', "&quot;"), ans, wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Properties pass down: clues, mistakes and real-world shapes", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    sides = strip_svg([(EQUI, 0, "equilateral"), (ISO_AC, 0, "isosceles"), (SCA_AC, 0, "scalene")],
                      cw=140, label="equilateral, isosceles and scalene triangles")
    angs = strip_svg([(SCA_AC, 0, "acute"), (ISO_RT, 0, "right"), (ISO_OB, 0, "obtuse")],
                     cw=140, bh=70, label="acute, right and obtuse triangles")
    quads = strip_svg([(PARA, 0, "parallelogram"), (RECT, 0, "rectangle"), (RHO, 0, "rhombus"), (SQ, 0, "square"),
                       (TRAP, 0, "trapezoid"), (KITE, 0, "kite")], cw=128, bw=96, bh=74,
                      label="parallelogram, rectangle, rhombus, square, trapezoid and kite with marks")
    return (
        "<h2>The big idea: a smaller group keeps every property</h2>"
        "<p>Shapes are sorted into groups by their <b>properties</b> (sides and angles). A <b>subcategory</b> is a smaller group inside a bigger one. "
        "Every shape in the smaller group has <b>all</b> the properties of the bigger group, plus more.</p>"
        "<p>All rectangles have 4 right angles. Squares are rectangles. So all squares have 4 right angles. "
        "Properties pass <b>down</b> to the smaller group, never <b>up</b>: squares have 4 equal sides, but most rectangles do not.</p>"
        "<h2>Classify triangles</h2>"
        "<p>Name a triangle two ways: by its <b>sides</b> and by its <b>angles</b>. Tick marks show equal sides, and a small square shows a right angle.</p>"
        "<figure class='sn-fig'>" + sides + "<figcaption>By sides</figcaption></figure>"
        "<figure class='sn-fig'>" + angs + "<figcaption>By angles: look at the largest angle</figcaption></figure>" +
        table(["By sides", "Meaning", "By angles", "Meaning"], [
            ["Equilateral", "3 equal sides", "Acute", "3 acute angles"],
            ["Isosceles", "at least 2 equal sides", "Right", "1 right angle"],
            ["Scalene", "no equal sides", "Obtuse", "1 obtuse angle"],
        ]) +
        "<p>An equilateral triangle has 3 equal sides, so it is also <b>isosceles</b>. Use both names for the full name: "
        "a right angle and 2 equal sides make a <b>right isosceles</b> triangle. A triangle can never be right and obtuse at the same time.</p>"
        "<h2>Classify quadrilaterals</h2>"
        "<p>Arrows show parallel sides. Shapes with 2 pairs of arrows are parallelograms; a trapezoid has 1 pair.</p>"
        "<figure class='sn-fig'>" + quads +
        "<figcaption>Each shape is named by what it must have, not by how it is turned.</figcaption></figure>" +
        table(["Shape", "What it must have", "It is also a"], [
            ["Parallelogram", "2 pairs of parallel sides", "quadrilateral"],
            ["Rectangle", "a parallelogram with 4 right angles", "parallelogram"],
            ["Rhombus", "a parallelogram with 4 equal sides", "parallelogram"],
            ["Square", "4 right angles and 4 equal sides", "rectangle, rhombus, parallelogram"],
            ["Trapezoid", "exactly 1 pair of parallel sides (in this unit)", "quadrilateral"],
            ["Kite", "2 pairs of equal sides next to each other", "quadrilateral"],
        ]) +
        "<p>Some books define a trapezoid as a quadrilateral with <i>at least</i> 1 pair of parallel sides, so a parallelogram is a trapezoid there. "
        "Every trapezoid in this unit has exactly 1 pair, so both definitions agree.</p>"
        "<h2>The hierarchy</h2>"
        "<p>A hierarchy diagram shows which groups are inside which. A line going down (or a box inside a box) means "
        "&quot;is a kind of&quot;.</p>"
        "<figure class='sn-fig'>" + quad_tree() +
        "<figcaption>Squares are under both Rectangles and Rhombuses: every square is both.</figcaption></figure>"
        "<figure class='sn-fig'>" + venn_svg(numbers=False, label="nested diagram of quadrilaterals") +
        "<figcaption>The same groups as boxes. Squares sit where Rectangles and Rhombuses overlap.</figcaption></figure>"
        "<figure class='sn-fig'>" + tri_tree() +
        "<figcaption>Every equilateral triangle is isosceles. No triangle is both isosceles and scalene.</figcaption></figure>" +
        ex("Example", "All parallelograms have opposite sides that are equal. Is this true for every rhombus?",
           "A rhombus is a parallelogram, so it gets every property of a parallelogram.", "yes") +
        ex("Example", "A quadrilateral has 4 equal sides and 4 right angles. Which names fit?",
           "4 equal sides: rhombus. 4 right angles: rectangle. Both are parallelograms and quadrilaterals. Square tells the most.",
           "square, rectangle, rhombus, parallelogram, quadrilateral") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["A square is not a rectangle", "A rectangle needs only 4 right angles. Every square is a rectangle"],
            ["A rhombus must look like a diamond", "A rhombus needs only 4 equal sides. A square sitting flat is a rhombus"],
            ["All rectangles are squares", "Only rectangles with 4 equal sides are squares"],
            ["An equilateral triangle is not isosceles", "Isosceles means at least 2 equal sides, and 3 is at least 2"],
            ["A right triangle can also be obtuse", "A triangle has at most 1 angle of 90° or more"],
            ["Properties pass up the hierarchy", "Only down: a square has every property of a rectangle, not the other way"],
        ])
    )


FAQ = [
    {"q": "Is a square a rhombus?",
     "a": "Yes. A rhombus is a parallelogram with 4 equal sides, and every square has 4 equal sides. A square is a rhombus that also has 4 right angles."},
    {"q": "Is every rectangle a parallelogram?",
     "a": "Yes. A rectangle has 2 pairs of parallel sides, so it is a parallelogram with 4 right angles. Not every parallelogram is a rectangle."},
    {"q": "Is an equilateral triangle also isosceles?",
     "a": "Yes, when isosceles means at least 2 equal sides, which is the definition most math programs use. An equilateral triangle has 3 equal sides."},
    {"q": "Is a parallelogram a trapezoid?",
     "a": "It depends on the book. If a trapezoid has exactly 1 pair of parallel sides, a parallelogram is not a trapezoid; "
          "if it has at least 1 pair, every parallelogram is a trapezoid. Check which definition your class uses."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions. Choices with a fixed order
    (A-D pictures, always/sometimes/never, regions, numbers) stay as they are; the others fill the gaps."""
    for s in sets:
        cnt = [0] * 4
        free = []
        for it in s["items"]:
            if it.pop("fixed", False):
                cnt[it["a"]] += 1
            else:
                free.append(it)
        need = [max(0, 5 - c) for c in cnt]
        assert sum(need) == len(free), (s["title"], cnt, len(free))
        targets = [i for i in range(4) for _ in range(need[i])]
        rnd.shuffle(targets)
        for it, t in zip(free, targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t
        final = [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


def gen():
    rnd = random.Random(515)
    sets = [set_triangles(rnd), set_quads(rnd), set_hierarchy(rnd), set_asn(rnd), set_reason(rnd)]
    for s in sets:
        rnd.shuffle(s["items"])
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
    return {
        "country": "us", "subject": "math", "grade": "grade-5", "slug": "classify-two-dimensional-figures", "sort": 15,
        "updated": UPDATED, "pdf_url": "",
        "title": "Classify Two-Dimensional Figures: Triangles, Quadrilaterals and the Hierarchy of Shapes",
        "seo_title": "Grade 5 Classifying 2D Shapes Worksheets: Quadrilateral Hierarchy, Types of Triangles (5.G.B.3-4)",
        "short_title": "Classify 2D figures",
        "domain": "Geometry",
        "standard_code": "5.G.B.3–4",
        "standard_url": "https://www.thecorestandards.org/Math/Content/5/G/B/",
        "standard_text": "Understand that attributes belonging to a category of two-dimensional figures also belong to all subcategories of that category. For example, all rectangles have four right angles and squares are rectangles, so all squares have four right angles. Classify two-dimensional figures in a hierarchy based on properties.",
        "meta_desc": "Free Grade 5 worksheets on classifying 2D figures: equilateral, isosceles and scalene triangles, acute, right and obtuse triangles, parallelograms, rectangles, rhombuses, squares and trapezoids, the quadrilateral hierarchy diagram, and always/sometimes/never. 100 practice questions with answers.",
        "key_big": "A smaller group keeps every property of the bigger group it belongs to.",
        "key_sub": "All rectangles have 4 right angles, and squares are rectangles, so all squares have 4 right angles. Properties pass down the hierarchy, never up: a square is a rectangle and a rhombus, but not every rectangle is a square.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (A-D choices, hierarchy diagrams) so their labels stay readable."""
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
        mark_large(u, "(four [a-z]+ labeled A to D|nested diagram|tree diagram)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
