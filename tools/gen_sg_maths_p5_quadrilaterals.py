# -*- coding: utf-8 -*-
"""
Singapore Primary 5 Maths: Parallelograms, rhombuses and trapeziums
(MOE 2021 Primary Mathematics Syllabus, Standard, Primary 5: Geometry)
  python3 tools/gen_sg_maths_p5_quadrilaterals.py
Naming the shapes (a rhombus is a parallelogram with 4 equal sides, a square is a rhombus with 4 right
angles, a trapezium has exactly one pair of parallel sides), their properties (opposite sides and
opposite angles of a parallelogram are equal, angles between a pair of parallel sides add up to 180°),
unknown angles in parallelograms, rhombuses and trapeziums, and figures with triangles.

Every angle figure is drawn from real coordinates: each angle written on a figure is measured from
the drawing and must equal the number shown, and every unknown angle ∠x is measured too and must equal
the answer worked out step by step. Shape-naming pictures are checked in code (parallel sides, equal
sides, right angles). Wrong answers come from real mistakes: opposite angles add up to 180°, a trapezium
has 2 pairs of parallel sides, a rhombus is not a square (or a square is not a rhombus), copying the given
angle, 360° − the given angle, 90° − the given angle, and pairing the wrong angles in a trapezium.
Shape helpers adapted from gen_caon_math_g6_quadrilaterals.py. Singapore English.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-5")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
BLUE = "#2f6fb0"
FONT = "Arial, Helvetica, sans-serif"


# ------------------------------------------------------------ helpers
def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def mcq(q, correct, cands, e, rnd):
    correct = str(correct)
    seen = {plain(correct)}
    pick = []
    for c in cands:
        c = str(c)
        if not c or plain(c) in seen:
            continue
        seen.add(plain(c))
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


def mcq_fixed(q, choices, correct, e):
    """Choices keep their order (A B C D). The answer position is not moved later."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fixed": True}


def balance(sets, rnd):
    """Spread the correct answers evenly (5 per position per set). Fixed-order questions stay as they are."""
    for s in sets:
        cnt, free = [0] * 4, []
        for it in s["items"]:
            if it.pop("fixed", False):
                cnt[it["a"]] += 1
            else:
                free.append(it)
        targets = []
        for p in range(4):
            assert cnt[p] <= 5, (s["title"], cnt)
            targets += [p] * (5 - cnt[p])
        assert len(targets) == len(free)
        rnd.shuffle(targets)
        for it, t in zip(free, targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t
        assert [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)] == [5, 5, 5, 5]


class Spots:
    """Answer letters for A-D picture questions: each letter used about equally often."""
    def __init__(self, rnd):
        self.rnd, self.left = rnd, []

    def next(self):
        if not self.left:
            self.left = [0, 1, 2, 3]
            self.rnd.shuffle(self.left)
        return self.left.pop()


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def deg(x):
    assert x == int(x) and 0 < x < 360, x
    return "%d°" % x


def degs(*xs):
    return [deg(x) for x in xs if 0 < x < 360 and x == int(x)]


# ------------------------------------------------------------ geometry
def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def mul(a, k):
    return (a[0] * k, a[1] * k)


def norm(v):
    L = math.hypot(v[0], v[1])
    return (v[0] / L, v[1] / L)


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def ang_at(V, P, Q):
    u, v = norm(sub(P, V)), norm(sub(Q, V))
    return math.degrees(math.acos(max(-1.0, min(1.0, u[0] * v[0] + u[1] * v[1]))))


def side_lens(pts):
    n = len(pts)
    return [dist(pts[(i + 1) % n], pts[i]) for i in range(n)]


def angles(pts):
    n = len(pts)
    return [ang_at(pts[i], pts[i - 1], pts[(i + 1) % n]) for i in range(n)]


def dir_diff(a, b):
    t = abs(math.degrees(math.atan2(a[1], a[0]) - math.atan2(b[1], b[0]))) % 180
    return min(t, 180 - t)


def side_angle_diff(pts, i, j):
    n = len(pts)
    return dir_diff(sub(pts[(i + 1) % n], pts[i]), sub(pts[(j + 1) % n], pts[j]))


def facts(pts):
    L = side_lens(pts)
    A = angles(pts)
    eq = all(close(L[0], x) for x in L)
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
        return "trapezium"
    return "quadrilateral"


def seg_dist(p, a, b):
    ab, ap = sub(b, a), sub(p, a)
    L2 = ab[0] ** 2 + ab[1] ** 2
    t = max(0.0, min(1.0, (ap[0] * ab[0] + ap[1] * ab[1]) / L2)) if L2 else 0.0
    return dist(p, (a[0] + ab[0] * t, a[1] + ab[1] * t))


def inside(p, poly):
    n = len(poly)
    sg = [(poly[(i + 1) % n][0] - poly[i][0]) * (p[1] - poly[i][1]) - (poly[(i + 1) % n][1] - poly[i][1]) * (p[0] - poly[i][0])
          for i in range(n)]
    return all(x > 0 for x in sg) or all(x < 0 for x in sg)


def rot_pt(p, d):
    t = math.radians(d)
    return (p[0] * math.cos(t) - p[1] * math.sin(t), p[0] * math.sin(t) + p[1] * math.cos(t))


# ------------------------------------------------------------ shapes for naming (y goes down, like SVG)
def S(pts, kind):
    return {"pts": [(float(x), float(y)) for x, y in pts], "kind": kind}


def square(s=100):
    return S([(0, 0), (s, 0), (s, s), (0, s)], "square")


def rect(a, b):
    return S([(0, 0), (a, 0), (a, b), (0, b)], "rectangle")


def rhombus(dg, s=100):
    t = math.radians(dg)
    return S([(0, 0), (s, 0), (s + s * math.cos(t), s * math.sin(t)), (s * math.cos(t), s * math.sin(t))], "rhombus")


def para(a, b, dg):
    t = math.radians(dg)
    return S([(0, 0), (a, 0), (a + b * math.cos(t), b * math.sin(t)), (b * math.cos(t), b * math.sin(t))], "parallelogram")


def trap(bottom, top, h, off):
    return S([(0, h), (bottom, h), (off + top, 0), (off, 0)], "trapezium")


def rtrap(bottom, top, h):
    return S([(0, h), (bottom, h), (top, 0), (0, 0)], "trapezium")


SQ = square()
RECT = rect(150, 85)
RHO = rhombus(60)
RHO2 = rhombus(70)
RHO3 = rhombus(48)
PARA = para(150, 80, 60)
PARA2 = para(140, 90, 55)
PARA3 = para(130, 75, 120)
ISO = trap(150, 70, 80, 40)          # trapezium with equal slanted sides
TRAPG = trap(150, 60, 75, 20)        # trapezium with no equal sides
TRAP3 = trap(160, 60, 70, 70)        # no equal sides
RTRAP = rtrap(150, 70, 90)
QUAD = S([(0, 70), (150, 90), (125, 0), (30, 20)], "quadrilateral")   # no parallel sides


def placed(sh, rot, bw, bh, cx, cy):
    pts = [rot_pt(p, rot) for p in sh["pts"]]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    k = min(bw / (max(xs) - min(xs)), bh / (max(ys) - min(ys)))
    mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    return [(cx + (p[0] - mx) * k, cy + (p[1] - my) * k) for p in pts]


def shape_elems(sh, rot, bw, bh, cx, cy, marks=("ticks", "rights", "arrows"), sw=3):
    """SVG elements for one shape plus its marks, and the box around everything drawn.
    marks: ticks (equal sides), rights (right angles), arrows (parallel sides)."""
    pts = placed(sh, rot, bw, bh, cx, cy)
    n = len(pts)
    el, box = [], list(pts)
    P = lambda ps: " ".join("%.1f,%.1f" % p for p in ps)
    el.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>"
              % (P(pts), FILL, GREEN, sw))
    f = facts(pts)
    mk = "stroke='%s' stroke-width='2' fill='none' stroke-linecap='round'" % INK
    for i, a in enumerate(f["angles"]):
        assert i in f["rights"] or abs(a - 90) >= 10, (sh["kind"], f["angles"])
    tick_at = set()
    if "ticks" in marks:
        groups = []
        for i, L in enumerate(f["lens"]):
            for g in groups:
                if close(f["lens"][g[0]], L):
                    g.append(i)
                    break
            else:
                groups.append([i])
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
    if sh["kind"] != "other":
        assert quad_name(pts) == sh["kind"], (sh["kind"], quad_name(pts))
    pad = sw / 2.0 + 1
    bb = (min(p[0] for p in box) - pad, min(p[1] for p in box) - pad,
          max(p[0] for p in box) + pad, max(p[1] for p in box) + pad)
    return el, bb, pts


def shape_svg(sh, rot=0, bw=140, bh=95, marks=("ticks", "rights", "arrows"), label="quadrilateral"):
    _, bb, _ = shape_elems(sh, rot, bw, bh, 0, 0, marks)
    pad = 5
    W, H = int(math.ceil(bb[2] - bb[0] + 2 * pad)), int(math.ceil(bb[3] - bb[1] + 2 * pad))
    if W == H:
        W += 1
    el, bb2, pts = shape_elems(sh, rot, bw, bh, pad - bb[0] + (W - (bb[2] - bb[0] + 2 * pad)) / 2,
                               pad - bb[1] + (H - (bb[3] - bb[1] + 2 * pad)) / 2, marks)
    assert bb2[0] >= 0 and bb2[1] >= 0 and bb2[2] <= W and bb2[3] <= H
    return svg_wrap(W, H, "".join(el), label), pts


CELL = 118


def grid_svg(items, marks=("ticks", "rights", "arrows"), label="four figures labelled A to D"):
    el = []
    W = H = 2 * CELL
    el.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, CELL, H - 4, GRAY))
    el.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, W - 4, CELL, GRAY))
    for k, (sh, rot) in enumerate(items):
        x0, y0 = (k % 2) * CELL, (k // 2) * CELL
        e, bb, _ = shape_elems(sh, rot, 78, 78, x0 + 66, y0 + 65, marks, sw=2.6)
        assert bb[0] >= x0 + 18 and bb[1] >= y0 + 6 and bb[2] <= x0 + CELL - 3 and bb[3] <= y0 + CELL - 3, (sh["kind"], bb)
        el += e
        el.append("<text x='%d' y='%d' font-size='18' font-weight='700' fill='%s'>%s</text>" % (x0 + 6, y0 + 22, INK, "ABCD"[k]))
    return svg_wrap(W, H, "".join(el), label)


def strip_svg(items, label, cols=None):
    """Lesson figure: shapes with a caption under each. items: (shape, rot, caption, options)."""
    cols = cols or len(items)
    cw, top = 132, 112
    rows = (len(items) + cols - 1) // cols
    rh = top + 26
    el = []
    for k, (sh, rot, cap, opt) in enumerate(items):
        x0, y0 = (k % cols) * cw, (k // cols) * rh
        e, bb, _ = shape_elems(sh, rot, opt.get("bw", 92), opt.get("bh", 78), x0 + cw / 2, y0 + 56,
                               opt.get("marks", ("ticks", "rights", "arrows")), sw=2.8)
        assert bb[0] >= x0 + 2 and bb[2] <= x0 + cw - 2 and bb[1] >= y0 + 2 and bb[3] <= y0 + top - 2, (cap, bb)
        el += e
        el.append("<text x='%d' y='%d' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                  % (x0 + cw / 2, y0 + top + 16, INK, cap))
    return svg_wrap(cw * cols, rh * rows, "".join(el), label)


# ------------------------------------------------------------ angle figures (math coords, y goes up)
def para_P(a, w=150, s=85, rot=0, names="ABCD", start=0):
    """Parallelogram: base[0]=(0,0), base[1]=(w,0), angle a at base[0]. base[start] gets names[0]."""
    t = math.radians(a)
    D = (s * math.cos(t), s * math.sin(t))
    base = [(0.0, 0.0), (float(w), 0.0), add((w, 0), D), D]
    base = [rot_pt(p, rot) for p in base]
    return {names[(i - start) % 4]: base[i] for i in range(4)}, list(names)


def trap_P(a, b, w=160, h=80, rot=0, names="ABCD", start=0):
    """Trapezium: base[0]base[1] (bottom, length w) parallel to base[2]base[3] (top).
    Angle a at base[0], angle b at base[1]."""
    x0 = h / math.tan(math.radians(a)) if a != 90 else 0.0
    x1 = h / math.tan(math.radians(b)) if b != 90 else 0.0
    base = [(0.0, 0.0), (float(w), 0.0), (w - x1, float(h)), (x0, float(h))]
    top = (w - x1) - x0
    assert top > 0.3 * w, (a, b, top)
    base = [rot_pt(p, rot) for p in base]
    return {names[(i - start) % 4]: base[i] for i in range(4)}, list(names)


def on_line(P, X, Y, k):
    """Point X + k (Y − X)."""
    return add(P[X], mul(sub(P[Y], P[X]), k))


def ext(P, X, Y, L=55):
    """Point beyond Y on line XY, L units past Y."""
    return add(P[Y], mul(norm(sub(P[Y], P[X])), L))


def measure(P, V, X, Y):
    return ang_at(P[V], P[X], P[Y])


class AFig:
    """An angle figure. P: dict name -> (x, y) in maths coordinates (y up)."""
    def __init__(self, P, poly, size=(190, 100)):
        self.P, self.poly = dict(P), list(poly)
        self.segs, self.angs, self.arrows, self.ticks, self.rights, self.sides = [], [], [], [], [], []
        self.letters = None
        self.size = size

    def seg(self, a, b):
        self.segs.append((a, b))
        return self

    def ang(self, V, X, Y, txt, unknown=False):
        """Label the angle XVY. txt is a number (degrees) or a letter for an unknown."""
        self.angs.append((V, X, Y, txt, unknown))
        return self

    def check(self):
        """Every number on the figure is the real angle."""
        for V, X, Y, txt, unk in self.angs:
            if not unk:
                m = measure(self.P, V, X, Y)
                assert abs(m - txt) < 1e-6, (V, X, Y, txt, m)

    def value(self, V, X, Y):
        m = measure(self.P, V, X, Y)
        assert abs(m - round(m)) < 1e-6, m
        return int(round(m))

    def svg(self, label):
        self.check()
        P = self.P
        xs, ys = [p[0] for p in P.values()], [p[1] for p in P.values()]
        k = min(self.size[0] / (max(xs) - min(xs)), self.size[1] / (max(ys) - min(ys)))
        S_ = {n: ((p[0] - min(xs)) * k, (max(ys) - p[1]) * k) for n, p in P.items()}
        poly = [S_[n] for n in self.poly]
        cen = (sum(p[0] for p in poly) / len(poly), sum(p[1] for p in poly) / len(poly))
        el, obst, boxes, pts_all = [], [], [], list(S_.values())
        F = lambda p: "%.1f,%.1f" % p
        el.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.8' stroke-linejoin='round'/>"
                  % (" ".join(F(p) for p in poly), FILL, GREEN))
        lines = [(self.poly[i], self.poly[(i + 1) % len(self.poly)]) for i in range(len(self.poly))]
        for a, b in self.segs:
            el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.6' stroke-linecap='round'/>"
                      % (S_[a] + S_[b] + (GREEN,)))
        lines += self.segs
        for a, b in lines:
            obst.append((S_[a], S_[b]))
        mk = "stroke='%s' stroke-width='2' fill='none' stroke-linecap='round' stroke-linejoin='round'" % INK
        # equal sides
        for g, grp in enumerate(self.ticks):
            for a, b in grp:
                pa, pb = S_[a], S_[b]
                d = norm(sub(pb, pa))
                nr = (-d[1], d[0])
                m = mul(add(pa, pb), 0.5)
                for j in range(g + 1):
                    o = (j - g / 2.0) * 5
                    c = add(m, mul(d, o))
                    p1, p2 = add(c, mul(nr, -6)), add(c, mul(nr, 6))
                    el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' %s/>" % (p1 + p2 + (mk,)))
                    obst.append((p1, p2))
        # parallel sides
        tick_segs = {frozenset(s) for grp in self.ticks for s in grp}
        for g, grp in enumerate(self.arrows):
            d = norm(sub(S_[grp[0][1]], S_[grp[0][0]]))
            nr = (-d[1], d[0])
            for a, b in grp:
                assert dir_diff(sub(P[b], P[a]), sub(P[grp[0][1]], P[grp[0][0]])) < 1e-6, (a, b)
                m = mul(add(S_[a], S_[b]), 0.5)
                shift = 14 if frozenset((a, b)) in tick_segs else 0
                for r in range(g + 1):
                    o = shift + r * 5 - g * 2.5
                    tip = add(m, mul(d, o + 4))
                    w1 = add(add(tip, mul(d, -7)), mul(nr, 5))
                    w2 = add(add(tip, mul(d, -7)), mul(nr, -5))
                    el.append("<polyline points='%s %s %s' %s/>" % (F(w1), F(tip), F(w2), mk))
                    obst += [(w1, tip), (tip, w2)]
        # right angles
        for V, X, Y in self.rights:
            assert abs(measure(P, V, X, Y) - 90) < 1e-6, (V, X, Y)
            v = S_[V]
            u1, u2 = norm(sub(S_[X], v)), norm(sub(S_[Y], v))
            q1, q3 = add(v, mul(u1, 10)), add(v, mul(u2, 10))
            q2 = add(q1, mul(u2, 10))
            el.append("<polyline points='%s %s %s' %s/>" % (F(q1), F(q2), F(q3), mk.replace("'2'", "'1.6'")))
            obst += [(q1, q2), (q2, q3)]
        # angle arcs
        arcs = []
        for V, X, Y, txt, unk in self.angs:
            v = S_[V]
            u1, u2 = norm(sub(S_[X], v)), norm(sub(S_[Y], v))
            th = ang_at(v, S_[X], S_[Y])
            ra = 13 if th >= 75 else (17 if th >= 50 else 22)
            cr = u1[0] * u2[1] - u1[1] * u2[0]
            p1, p2 = add(v, mul(u1, ra)), add(v, mul(u2, ra))
            col = RED if unk else INK
            el.append("<path d='M%.1f %.1f A%d %d 0 0 %d %.1f %.1f' fill='none' stroke='%s' stroke-width='1.8'/>"
                      % (p1[0], p1[1], ra, ra, 1 if cr > 0 else 0, p2[0], p2[1], col))
            a1 = math.atan2(u1[1], u1[0])
            sgn = 1 if cr > 0 else -1
            prev = p1
            for i in range(1, 9):
                t = a1 + sgn * math.radians(th) * i / 8
                q = add(v, (ra * math.cos(t), ra * math.sin(t)))
                obst.append((prev, q))
                prev = q
            arcs.append((v, u1, u2, th, ra, txt, unk, sgn, a1))
            pts_all += [p1, p2]

        def clear(c, w, h):
            pts = []
            for i in range(9):
                fx = -w / 2 + w * i / 8.0
                pts += [(c[0] + fx, c[1] - h / 2), (c[0] + fx, c[1] + h / 2)]
            for i in range(1, 4):
                fy = -h / 2 + h * i / 4.0
                pts += [(c[0] - w / 2, c[1] + fy), (c[0] + w / 2, c[1] + fy)]
            return min(seg_dist(p, a, b) for p in pts for a, b in obst)

        line_s = [(S_[a], S_[b]) for a, b in lines]

        def crosses(v, c):
            """The path from the vertex to the label crosses a line that does not go through the vertex."""
            for a, b in line_s:
                if seg_dist(v, a, b) < 1e-6:
                    continue
                d1 = (b[0] - a[0]) * (v[1] - a[1]) - (b[1] - a[1]) * (v[0] - a[0])
                d2 = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
                d3 = (c[0] - v[0]) * (a[1] - v[1]) - (c[1] - v[1]) * (a[0] - v[0])
                d4 = (c[0] - v[0]) * (b[1] - v[1]) - (c[1] - v[1]) * (b[0] - v[0])
                if d1 * d2 < 0 and d3 * d4 < 0:
                    return True
            return False

        def free(c, w, h, gap=2):
            for bc, bw, bh in boxes:
                if abs(c[0] - bc[0]) < (w + bw) / 2 + gap and abs(c[1] - bc[1]) < (h + bh) / 2 + gap:
                    return False
            return True

        # angle labels: inside the wedge, as near the vertex as possible
        for v, u1, u2, th, ra, txt, unk, sgn, a1 in arcs:
            s = deg(txt) if not unk else txt
            w, h = (9.0 if unk else 8.4 * len(s) - 2), 14.0
            best = None
            for R in range(ra + 6, 90):
                for off in (0, 0.12, -0.12, 0.24, -0.24, 0.36, -0.36):
                    t = a1 + sgn * math.radians(th) * (0.5 + off)
                    c = add(v, (R * math.cos(t), R * math.sin(t)))
                    corners = [(c[0] + dx, c[1] + dy) for dx in (-w / 2, w / 2) for dy in (-h / 2, h / 2)]
                    okw = True
                    for q in corners:
                        uq = sub(q, v)
                        L = math.hypot(*uq)
                        if L < ra + 2 or ang_at(v, q, add(v, u1)) > th or ang_at(v, q, add(v, u2)) > th:
                            okw = False
                            break
                    if not okw or not free(c, w, h) or crosses(v, c):
                        continue
                    if clear(c, w, h) >= 2.5:
                        best = c
                        break
                if best:
                    break
            assert best, ("no room for angle label", s, label)
            boxes.append((best, w, h))
            if unk:
                el.append("<text x='%.1f' y='%.1f' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>"
                          "<tspan font-style='italic'>%s</tspan></text>" % (best[0], best[1] + 5, RED, s))
            else:
                el.append("<text x='%.1f' y='%.1f' font-size='14' fill='%s' text-anchor='middle'>%s</text>"
                          % (best[0] + 2, best[1] + 5, INK, s))
        # side lengths
        for a, b, s in self.sides:
            pa, pb = S_[a], S_[b]
            m = mul(add(pa, pb), 0.5)
            d = norm(sub(pb, pa))
            nr = (-d[1], d[0])
            if (m[0] + nr[0] - cen[0]) ** 2 + (m[1] + nr[1] - cen[1]) ** 2 < (m[0] - cen[0]) ** 2 + (m[1] - cen[1]) ** 2:
                nr = (-nr[0], -nr[1])
            w, h = 8.2 * len(s), 14.0
            best = None
            for R in range(8, 40):
                for sh in (0, 8, -8, 16, -16):
                    c = add(add(m, mul(nr, R)), mul(d, sh))
                    if free(c, w, h) and clear(c, w, h) >= 3:
                        best = c
                        break
                if best:
                    break
            assert best, ("no room for side label", s)
            boxes.append((best, w, h))
            el.append("<text x='%.1f' y='%.1f' font-size='14' fill='%s' text-anchor='middle'>%s</text>"
                      % (best[0], best[1] + 5, INK, s))
        # vertex letters: outside, away from the middle
        for n in (self.letters if self.letters is not None else sorted(S_)):
            p = S_[n]
            away = sub(p, cen)
            away = norm(away) if math.hypot(*away) > 1e-9 else (0, -1)
            best = None
            for r in (13, 15, 17, 20):
                for i in range(48):
                    t = 2 * math.pi * i / 48
                    dvec = (math.cos(t), math.sin(t))
                    c = add(p, mul(dvec, r))
                    w, h = 11.0, 14.0
                    if not free(c, w, h, 1):
                        continue
                    cl = clear(c, w, h)
                    if cl < 3:
                        continue
                    sc = min(cl, 7) * 0.5 + 3 * (dvec[0] * away[0] + dvec[1] * away[1]) - 0.2 * r
                    if inside(c, poly):
                        sc -= 6
                    if best is None or sc > best[0] + 1e-9:
                        best = (sc, c)
            assert best, ("no room for letter", n, label)
            c = best[1]
            boxes.append((c, 11.0, 14.0))
            el.append("<text x='%.1f' y='%.1f' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                      % (c[0], c[1] + 5.5, INK, n))
        # bounding box of everything
        bx = [p for p in pts_all]
        for c, w, h in boxes:
            bx += [(c[0] - w / 2, c[1] - h / 2), (c[0] + w / 2, c[1] + h / 2)]
        for a, b in obst:
            bx += [a, b]
        pad = 4
        x0, y0 = min(p[0] for p in bx) - pad, min(p[1] for p in bx) - pad
        W, H = int(math.ceil(max(p[0] for p in bx) + pad - x0)), int(math.ceil(max(p[1] for p in bx) + pad - y0))
        if W == H:
            W += 1
        body = "<g transform='translate(%.1f %.1f)'>%s</g>" % (-x0, -y0, "".join(el))
        return svg_wrap(W, H, body, label)


def para_fig(a, w=150, s=85, rot=0, names="ABCD", start=0, rh=False, size=(180, 95)):
    P, poly = para_P(a, w, s, rot, names, start)
    f = AFig(P, poly, size)
    A, B, C, D = poly
    if rh:
        f.ticks = [[(A, B), (B, C), (C, D), (D, A)]]
    else:
        f.arrows = [[(A, B), (D, C)], [(A, D), (B, C)]]
    return f


def trap_fig(a, b, w=160, h=80, rot=0, names="ABCD", start=0, size=(180, 95)):
    P, poly = trap_P(a, b, w, h, rot, names, start)
    f = AFig(P, poly, size)
    # the parallel sides are base[0]base[1] and base[3]base[2]
    nm = lambda i: names[(i - start) % 4]
    f.arrows = [[(nm(0), nm(1)), (nm(3), nm(2))]]
    f.par = (nm(0) + nm(1), nm(3) + nm(2))
    return f


def ANG(V, X, Y):
    return "∠" + X + V + Y


# ------------------------------------------------------------ bar models
def bar_model(rows, total, label):
    """rows: (name, units, extra) with extra = None or (text, length in units); one row has ask=True.
    A bracket on the right joins all rows: total."""
    U, H, gap = 52, 28, 14
    L = 16 + max(10 * len(r[0]) for r in rows)
    el = []
    top = 30 if rows[0][3] else 6
    y = top
    ends = []
    for k, (name, units, extra, ask) in enumerate(rows):
        el.append("<text x='%d' y='%.1f' font-size='15' font-weight='700' fill='%s'>%s</text>" % (4, y + H / 2 + 5, INK, name))
        for i in range(units):
            el.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                      % (L + i * U, y, U, H, FILL, GREEN))
        x = L + units * U
        if extra:
            t, ln = extra
            wx = int(U * ln)
            el.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff' stroke='%s' stroke-width='2' stroke-dasharray='5 3'/>"
                      % (x, y, wx, H, GREEN))
            el.append("<text x='%.1f' y='%.1f' font-size='14' fill='%s' text-anchor='middle'>%s</text>" % (x + wx / 2.0, y + H / 2 + 5, INK, t))
            x += wx
        if ask:
            assert k in (0, len(rows) - 1)
            yb, yt, sg = (y - 4, y - 10, -1) if k == 0 else (y + H + 4, y + H + 10, 1)
            el.append("<path d='M%d %d L%d %d L%d %d L%d %d' fill='none' stroke='%s' stroke-width='2'/>"
                      % (L, yb, L, yt, x, yt, x, yb, RED))
            el.append("<text x='%.1f' y='%.1f' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>?</text>"
                      % (L + (x - L) / 2.0, yt - 4 if k == 0 else yt + 16, RED))
        ends.append(x)
        y += H + gap
    xb = max(ends) + 10
    y1 = top + len(rows) * (H + gap) - gap
    el.append("<path d='M%d %d L%d %d L%d %d L%d %d' fill='none' stroke='%s' stroke-width='2'/>" % (xb - 4, top, xb + 4, top, xb + 4, y1, xb - 4, y1, INK))
    el.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='2'/>" % (xb + 4, (top + y1) / 2.0, xb + 10, (top + y1) / 2.0, INK))
    el.append("<text x='%d' y='%.1f' font-size='15' font-weight='700' fill='%s'>%s</text>" % (xb + 14, (top + y1) / 2.0 + 5, INK, total))
    W = xb + 14 + 9 * len(total) + 6
    Ht = y1 + (30 if rows[-1][3] else 6)
    return svg_wrap(W, Ht, "".join(el), label)


# ------------------------------------------------------------ set 1: identify and name
WHY = {
    "rectangle": "The small squares show 4 right angles, so it is a rectangle. Its sides are not all equal, so it is not a square.",
    "rhombus": "The tick marks show 4 equal sides, so it is a rhombus. It has no right angles, so it is not a square.",
    "parallelogram": "The arrows show 2 pairs of parallel sides, so it is a parallelogram. The sides are not all equal "
                     "and there are no right angles, so it is not a rhombus or a rectangle.",
    "trapezium": "The arrows show exactly 1 pair of parallel sides. The other 2 sides are not parallel, so it is a trapezium.",
}
WRONG = {
    "rectangle": ["square", "rhombus", "trapezium"],
    "rhombus": ["square", "trapezium", "rectangle"],
    "parallelogram": ["trapezium", "rhombus", "rectangle"],
    "trapezium": ["parallelogram", "rhombus", "rectangle"],
}


def set_name(rnd, spots):
    its = []
    plan = [(PARA, 0, (150, 85)), (PARA2, -20, (150, 95)),
            (RHO, 60, (110, 100)), (RHO2, 0, (150, 95)),
            (TRAPG, 0, (150, 85)), (RTRAP, 0, (150, 85)), (ISO, 180, (150, 85)), (TRAP3, 90, (90, 130))]
    for sh, rot, size in plan:
        k = sh["kind"]
        marks = {"parallelogram": ("arrows",), "rhombus": ("ticks", "rights")}.get(k, ("ticks", "rights", "arrows"))
        svg, _ = shape_svg(sh, rot, size[0], size[1], marks, label=k + " with marks")
        e = WHY[k] + (" Turning a figure does not change its name." if rot % 360 else "")
        its.append(mcq(fig(svg) + "What is the best name for this figure? Use the marks.", k, WRONG[k], e, rnd))
    # A-D pictures
    grids = [
        ("Which figure is a trapezium?", "trapezium", [(PARA, 0), (RHO2, 0), (RECT, 0)], (TRAPG, 0),
         "Figure %s has exactly 1 pair of parallel sides (one set of arrows), so it is a trapezium. "
         "The other figures have 2 pairs of parallel sides."),
        ("Which figure is a rhombus?", "rhombus", [(PARA2, 0), (RECT, 0), (ISO, 0)], (RHO, 0),
         "Figure %s has 4 equal sides (tick marks on every side), so it is a rhombus. "
         "The parallelogram and the rectangle have only opposite sides equal."),
        ("Which figure is NOT a parallelogram?", "trapezium", [(RHO2, 30), (RECT, 0), (PARA, 0)], (RTRAP, 0),
         "Figure %s has only 1 pair of parallel sides, so it is a trapezium, not a parallelogram. "
         "A rhombus and a rectangle are special parallelograms."),
        ("Which figure has 4 equal sides but no right angles?", "rhombus", [(SQ, 0), (PARA, 0), (TRAPG, 0)], (RHO3, 0),
         "Figure %s is a rhombus: 4 equal sides and no right angles. The square also has 4 equal sides, but it has 4 right angles."),
    ]
    for q, kind, others, good, e in grids:
        marks = ("ticks", "rights") if kind == "rhombus" else ("arrows", "rights")
        pos = spots.next()
        cells = others[:]
        rnd.shuffle(cells)
        cells.insert(pos, good)
        for j, (sh, rot) in enumerate(cells):
            nm = quad_name(placed(sh, rot, 78, 78, 0, 0))
            if kind == "trapezium":
                assert (nm == "trapezium") == (j == pos), (q, nm)
            else:
                assert (nm == "rhombus") == (j == pos), (q, nm)
        its.append(mcq_fixed(fig(grid_svg(cells, marks)) + q, ["A", "B", "C", "D"], "ABCD"[pos], e % "ABCD"[pos]))
    words = [
        ("A rhombus is a parallelogram with ______.", "4 equal sides",
         ["4 right angles", "1 pair of parallel sides", "no equal sides"],
         "A rhombus has 2 pairs of parallel sides like every parallelogram, and all 4 of its sides are equal. "
         "It does not need right angles; that would make it a square."),
        ("How many pairs of parallel sides does a trapezium have?", "exactly 1 pair",
         ["2 pairs", "no pairs", "4 pairs"],
         "A trapezium has exactly 1 pair of parallel sides. A figure with 2 pairs is a parallelogram."),
        ("How many pairs of parallel sides does a parallelogram have?", "2 pairs",
         ["exactly 1 pair", "4 pairs", "no pairs"],
         "Both pairs of opposite sides of a parallelogram are parallel: 2 pairs."),
        ("A quadrilateral has 4 equal sides and 4 right angles. Is it a rhombus?", "Yes, it is a square",
         ["No, it has right angles", "No, it is a trapezium", "Only if it is turned"],
         "It has 4 equal sides, so it is a rhombus. With 4 right angles it is a special rhombus called a square."),
        ("Which statement about a square is true?", "It is a rhombus with 4 right angles",
         ["It is not a rhombus", "It is a trapezium", "It has 1 pair of parallel sides"],
         "A square has 4 equal sides (so it is a rhombus) and 4 right angles. It has 2 pairs of parallel sides."),
        ("A quadrilateral has 2 pairs of parallel sides. Its sides are not all equal and it has no right angles. "
         "What is its best name?", "parallelogram", ["rhombus", "trapezium", "square"],
         "2 pairs of parallel sides make a parallelogram. Its sides are not all equal, so it is not a rhombus or a square."),
        ("Siti says, “A trapezium has 2 pairs of parallel sides.” Is she right?", "No, it has exactly 1 pair",
         ["Yes, like a parallelogram", "No, it has no parallel sides", "Yes, if its sides are equal"],
         "A trapezium has exactly 1 pair of parallel sides. A quadrilateral with 2 pairs is a parallelogram."),
        ("Which of these is always a parallelogram?", "a rhombus",
         ["a trapezium", "any quadrilateral", "a figure with 1 right angle"],
         "A rhombus has 2 pairs of parallel sides, so it is always a parallelogram. A trapezium has only 1 pair."),
    ]
    for q, ans, wrong, e in words:
        its.append(mcq(q, ans, wrong, e, rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Name parallelograms, rhombuses and trapeziums", "items": its}


# ------------------------------------------------------------ angle question helper
def find_x(f, V, X, Y, label, intro, wrong, e, rnd, ask="Find ∠x."):
    f.ang(V, X, Y, "x", True)
    ans = f.value(V, X, Y)
    svg = f.svg(label)
    return mcq(fig(svg) + intro + " " + ask, deg(ans), degs(*wrong), e, rnd), ans


# ------------------------------------------------------------ set 2: properties
def set_properties(rnd):
    its = []
    # sides
    f = para_fig(62, 150, 87.5)
    f.sides = [("A", "B", "12 cm"), ("B", "C", "7 cm")]
    its.append(mcq(fig(f.svg("parallelogram ABCD with AB 12 cm and BC 7 cm")) +
                   "ABCD is a parallelogram. AB = 12 cm and BC = 7 cm. Find the length of CD.", "12 cm",
                   ["7 cm", "19 cm", "24 cm"],
                   "Opposite sides of a parallelogram are equal. CD is opposite AB, so CD = 12 cm.", rnd))
    f = para_fig(70, 153, 85)
    f.sides = [("A", "B", "9 cm"), ("D", "A", "5 cm")]
    its.append(mcq(fig(f.svg("parallelogram ABCD with AB 9 cm and AD 5 cm")) +
                   "ABCD is a parallelogram. AB = 9 cm and AD = 5 cm. Find its perimeter.", "28 cm",
                   ["14 cm", "45 cm", "19 cm"],
                   "Opposite sides are equal, so the sides are 9 cm, 5 cm, 9 cm and 5 cm. Perimeter = 9 + 5 + 9 + 5 = 28 cm.", rnd))
    f = para_fig(55, 110, 110, rh=True)
    f.sides = [("A", "B", "8 cm")]
    its.append(mcq(fig(f.svg("rhombus ABCD with side 8 cm")) +
                   "ABCD is a rhombus. AB = 8 cm. Find its perimeter.", "32 cm", ["16 cm", "64 cm", "24 cm"],
                   "All 4 sides of a rhombus are equal. Perimeter = 4 × 8 = 32 cm.", rnd))
    its.append(mcq("The perimeter of a rhombus is 52 cm. Find the length of one side.", "13 cm",
                   ["26 cm", "208 cm", "48 cm"],
                   "A rhombus has 4 equal sides. One side = 52 ÷ 4 = 13 cm.", rnd))
    its.append(mcq("PQRS is a parallelogram. PQ = 15 cm and its perimeter is 46 cm. Find the length of QR.", "8 cm",
                   ["16 cm", "31 cm", "23 cm"],
                   "PQ + QR is half the perimeter: 46 ÷ 2 = 23 cm. QR = 23 − 15 = 8 cm.", rnd))
    # angles with figures
    f = para_fig(64)
    f.ang("A", "B", "D", 64)
    q, _ = find_x(f, "C", "B", "D", "parallelogram ABCD with angle A 64° and unknown angle x at C",
                  "ABCD is a parallelogram.", [116, 296, 26],
                  "Opposite angles of a parallelogram are equal. ∠x is opposite ∠DAB, so ∠x = 64°.", rnd)
    f = para_fig(62)
    f.ang("B", "C", "A", 118)
    its.append(q)
    q, _ = find_x(f, "D", "A", "C", "parallelogram ABCD with angle B 118° and unknown angle x at D",
                  "ABCD is a parallelogram.", [62, 242, 28],
                  "Opposite angles of a parallelogram are equal. ∠x is opposite ∠ABC, so ∠x = 118°.", rnd)
    its.append(q)
    f = para_fig(72)
    f.ang("A", "B", "D", 72)
    q, _ = find_x(f, "B", "C", "A", "parallelogram ABCD with angle A 72° and unknown angle x at B",
                  "ABCD is a parallelogram.", [72, 288, 18],
                  "∠x and ∠DAB are next to each other, between the parallel sides AD and BC, so they add up to 180°. "
                  "∠x = 180° − 72° = 108°.", rnd)
    its.append(q)
    f = para_fig(56, 110, 110, rh=True)
    f.ang("D", "A", "C", 124)
    q, _ = find_x(f, "A", "B", "D", "rhombus ABCD with angle D 124° and unknown angle x at A",
                  "ABCD is a rhombus.", [124, 236, 34],
                  "A rhombus is a parallelogram, so angles next to each other add up to 180°. ∠x = 180° − 124° = 56°.", rnd)
    its.append(q)
    f = trap_fig(105, 62)
    f.ang("A", "B", "D", 105)
    q, _ = find_x(f, "D", "A", "C", "trapezium ABCD with AB parallel to DC, angle A 105° and unknown angle x at D",
                  "ABCD is a trapezium. AB ∥ DC.", [105, 255, 15],
                  "∠DAB and ∠x lie between the parallel sides AB and DC, on the same side AD, so they add up to 180°. "
                  "∠x = 180° − 105° = 75°.", rnd)
    its.append(q)
    f = trap_fig(65, 48, 170, 80)
    f.ang("B", "C", "A", 48)
    q, _ = find_x(f, "C", "D", "B", "trapezium ABCD with AB parallel to DC, angle B 48° and unknown angle x at C",
                  "ABCD is a trapezium. AB ∥ DC.", [48, 312, 42],
                  "∠ABC and ∠x lie between the parallel sides AB and DC, on the same side BC, so they add up to 180°. "
                  "∠x = 180° − 48° = 132°.", rnd)
    its.append(q)
    # which angles, from a picture
    f = trap_fig(70, 52)
    svg = f.svg("trapezium ABCD with AB parallel to DC")
    assert f.value("A", "B", "D") + f.value("D", "A", "C") == 180
    assert f.value("A", "B", "D") + f.value("B", "C", "A") != 180 and f.value("A", "B", "D") + f.value("C", "D", "B") != 180
    its.append(mcq(fig(svg) + "ABCD is a trapezium. AB ∥ DC. Which two angles must add up to 180°?", "∠A and ∠D",
                   ["∠A and ∠B", "∠A and ∠C", "∠B and ∠D"],
                   "∠A and ∠D are at the two ends of side AD, between the parallel sides AB and DC, so they add up to 180°. "
                   "∠A and ∠B are on the same parallel side, so they do not.", rnd))
    f = para_fig(60, 150, 80)
    svg = f.svg("parallelogram ABCD")
    its.append(mcq(fig(svg) + "ABCD is a parallelogram. Which two angles are equal?", "∠B and ∠D",
                   ["∠A and ∠B", "∠B and ∠C", "∠C and ∠D"],
                   "Opposite angles of a parallelogram are equal. ∠B and ∠D are opposite each other. "
                   "Angles next to each other, such as ∠A and ∠B, add up to 180°.", rnd))
    words = [
        ("What do the 4 angles of any quadrilateral add up to?", "360°", ["180°", "90°", "720°"],
         "A quadrilateral can be cut into 2 triangles along a diagonal. 2 × 180° = 360°."),
        ("Which is true about the opposite angles of a parallelogram?", "They are equal",
         ["They add up to 180°", "They add up to 360°", "They are always 90°"],
         "Opposite angles of a parallelogram are equal. It is the angles next to each other that add up to 180°."),
        ("Which is true about every rhombus?", "All sides equal, opposite angles equal",
         ["All 4 angles are equal", "Only 1 pair of sides is parallel", "Opposite angles add up to 180°"],
         "A rhombus has 4 equal sides and, like every parallelogram, equal opposite angles. "
         "All 4 angles are equal only in a square."),
        ("PQRS is a trapezium. PQ ∥ SR and ∠P = 80°. Which angle must be 100°?", "∠S",
         ["∠Q", "∠R", "None of them"],
         "∠P and ∠S are at the two ends of side PS, between the parallel sides PQ and SR. "
         "They add up to 180°, so ∠S = 180° − 80° = 100°."),
        ("Which property does a rhombus have that a parallelogram does not always have?", "4 equal sides",
         ["Opposite sides parallel", "Opposite angles equal", "Angles add up to 360°"],
         "Every parallelogram has parallel and equal opposite sides and equal opposite angles. "
         "Only a rhombus must have all 4 sides equal."),
        ("Which property does a parallelogram have that a trapezium does not?", "2 pairs of parallel sides",
         ["4 straight sides", "Angles add up to 360°", "1 pair of parallel sides"],
         "A trapezium has exactly 1 pair of parallel sides. A parallelogram has 2 pairs."),
        ("In parallelogram ABCD, ∠A + ∠C = 150°. Find ∠B.", "105°", ["75°", "150°", "30°"],
         "∠A and ∠C are opposite, so they are equal: ∠A = 150° ÷ 2 = 75°. ∠B is next to ∠A, so ∠B = 180° − 75° = 105°."),
    ]
    for q, ans, wrong, e in words:
        its.append(mcq(q, ans, wrong, e, rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Properties: equal sides, equal angles and angles that add up to 180°", "items": its}


# ------------------------------------------------------------ set 3: parallelograms and rhombuses
def set_para_angles(rnd):
    its = []
    # (figure builder, given angle, unknown, label, intro, wrong, explanation)
    f = para_fig(58)
    f.ang("A", "B", "D", 58)
    its.append(find_x(f, "B", "C", "A", "parallelogram ABCD with angle A 58° and unknown angle x at B",
                      "ABCD is a parallelogram.", [58, 302, 32],
                      "∠DAB and ∠x are next to each other, so they add up to 180°. ∠x = 180° − 58° = 122°.", rnd)[0])
    f = para_fig(67, 160, 85, names="PQRS", start=2)
    # base[2] = P, base[3] = Q, base[0] = R, base[1] = S
    f.ang("S", "P", "R", 113)
    its.append(find_x(f, "R", "S", "Q", "parallelogram PQRS with angle S 113° and unknown angle x at R",
                      "PQRS is a parallelogram.", [113, 247, 23],
                      "∠PSR and ∠x are next to each other, on side SR, so they add up to 180°. ∠x = 180° − 113° = 67°.", rnd)[0])
    f = para_fig(46, 110, 110, rh=True)
    f.ang("A", "B", "D", 46)
    its.append(find_x(f, "D", "A", "C", "rhombus ABCD with angle A 46° and unknown angle x at D",
                      "ABCD is a rhombus.", [46, 314, 44],
                      "A rhombus is a parallelogram, so ∠DAB and ∠x add up to 180°. ∠x = 180° − 46° = 134°.", rnd)[0])
    f = para_fig(81, 150, 85)
    f.ang("D", "A", "C", 99)
    its.append(find_x(f, "B", "C", "A", "parallelogram ABCD with angle D 99° and unknown angle x at B",
                      "ABCD is a parallelogram.", [81, 261, 9],
                      "∠x and ∠ADC are opposite angles of the parallelogram, so they are equal. ∠x = 99°.", rnd)[0])
    f = para_fig(76, 100, 100, rot=90, rh=True)
    f.ang("A", "B", "D", 76)
    its.append(find_x(f, "C", "D", "B", "rhombus ABCD standing on its side with angle A 76° and unknown angle x at C",
                      "ABCD is a rhombus.", [104, 284, 14],
                      "Opposite angles of a rhombus are equal. ∠x is opposite ∠DAB, so ∠x = 76°.", rnd)[0])
    f = para_fig(47, 160, 90)
    f.ang("C", "D", "B", 47)
    its.append(find_x(f, "D", "A", "C", "parallelogram ABCD with angle C 47° and unknown angle x at D",
                      "ABCD is a parallelogram.", [47, 313, 43],
                      "∠x and ∠BCD are next to each other, on side DC, so they add up to 180°. ∠x = 180° − 47° = 133°.", rnd)[0])
    f = para_fig(103, 150, 85, rot=-25)
    f.ang("B", "C", "A", 77)
    its.append(find_x(f, "A", "B", "D", "tilted parallelogram ABCD with angle B 77° and unknown angle x at A",
                      "ABCD is a parallelogram.", [77, 283, 13],
                      "∠x and ∠ABC are next to each other, on side AB, so they add up to 180°. ∠x = 180° − 77° = 103°.", rnd)[0])
    # extended sides
    f = para_fig(65, 140, 85)
    f.P["E"] = ext(f.P, "A", "B", 55)
    f.seg("B", "E")
    f.ang("A", "B", "D", 65)
    its.append(find_x(f, "B", "C", "E", "parallelogram ABCD with AB extended to E, angle A 65° and unknown angle x",
                      "ABCD is a parallelogram. ABE is a straight line.", [115, 295, 25],
                      "∠ABC = 180° − 65° = 115° (angles next to each other). ABE is a straight line, so "
                      "∠x = 180° − 115° = 65°.", rnd)[0])
    f = para_fig(70, 140, 85)
    f.P["E"] = ext(f.P, "D", "C", 55)
    f.seg("C", "E")
    f.ang("D", "A", "C", 110)
    its.append(find_x(f, "C", "B", "E", "parallelogram ABCD with DC extended to E, angle D 110° and unknown angle x",
                      "ABCD is a parallelogram. DCE is a straight line.", [70, 250, 20],
                      "∠BCD = 180° − 110° = 70° (angles next to each other). DCE is a straight line, so "
                      "∠x = 180° − 70° = 110°.", rnd)[0])
    f = para_fig(52, 140, 85)
    f.P["E"] = ext(f.P, "A", "B", 60)
    f.seg("B", "E")
    f.ang("B", "C", "E", 52)
    its.append(find_x(f, "D", "A", "C", "parallelogram ABCD with AB extended to E, angle CBE 52° and unknown angle x at D",
                      "ABCD is a parallelogram. ABE is a straight line.", [52, 308, 38],
                      "ABE is a straight line, so ∠ABC = 180° − 52° = 128°. ∠x is opposite ∠ABC, so ∠x = 128°.", rnd)[0])
    f = para_fig(71, 105, 105, rh=True)
    f.P["E"] = ext(f.P, "A", "D", 50)
    f.seg("D", "E")
    f.ang("D", "C", "E", 71)
    its.append(find_x(f, "B", "C", "A", "rhombus ABCD with AD extended to E, angle CDE 71° and unknown angle x at B",
                      "ABCD is a rhombus. ADE is a straight line.", [71, 289, 19],
                      "ADE is a straight line, so ∠ADC = 180° − 71° = 109°. ∠x is opposite ∠ADC, so ∠x = 109°.", rnd)[0])
    # two unknowns
    f = para_fig(106, 150, 85)
    f.ang("B", "C", "A", 74)
    f.ang("A", "B", "D", "x", True)
    f.ang("C", "D", "B", "y", True)
    x, y = f.value("A", "B", "D"), f.value("C", "D", "B")
    assert (x, y) == (106, 106)
    its.append(mcq(fig(f.svg("parallelogram ABCD with angle B 74° and unknown angles x at A and y at C")) +
                   "ABCD is a parallelogram. Find ∠x + ∠y.", deg(x + y), degs(148, 106, 286),
                   "∠x = 180° − 74° = 106° (next to ∠B). ∠y is opposite ∠x, so ∠y = 106°. ∠x + ∠y = 212°.", rnd))
    # bar model
    bm = bar_model([("∠A", 2, None, True), ("∠B", 1, None, False)], "180°", "bar model of angle A as 2 units and angle B as 1 unit")
    its.append(mcq(fig(bm) + "In parallelogram ABCD, ∠A is twice as large as ∠B. Find ∠A.", "120°",
                   ["60°", "90°", "240°"],
                   "∠A and ∠B are next to each other, so they add up to 180°. 3 units = 180°, 1 unit = 60°. "
                   "∠A = 2 units = 120°.", rnd))
    words = [
        ("In parallelogram ABCD, ∠A is 30° more than ∠B. Find ∠A.", "105°", ["75°", "150°", "120°"],
         "∠A + ∠B = 180°. Take away the extra 30°: 180° − 30° = 150°, so ∠B = 150° ÷ 2 = 75°. ∠A = 75° + 30° = 105°."),
        ("In parallelogram ABCD, ∠A + ∠C = 136°. Find ∠D.", "112°", ["68°", "136°", "44°"],
         "∠A and ∠C are opposite, so ∠A = 136° ÷ 2 = 68°. ∠D is next to ∠A: ∠D = 180° − 68° = 112°."),
        ("In rhombus ABCD, ∠A + ∠B + ∠C = 250°. Find ∠D.", "110°", ["70°", "125°", "290°"],
         "The 4 angles add up to 360°, so ∠D = 360° − 250° = 110°. Check: ∠A = ∠C = 70° and ∠B = ∠D = 110°."),
        ("In parallelogram PQRS, ∠P = 57°. Find ∠Q + ∠R.", "180°", ["114°", "246°", "123°"],
         "∠Q = 180° − 57° = 123° and ∠R = ∠P = 57°. ∠Q + ∠R = 123° + 57° = 180°."),
        ("Two angles next to each other in a parallelogram differ by 40°. Find the larger angle.", "110°",
         ["70°", "140°", "130°"],
         "The two angles add up to 180°. 180° − 40° = 140°, so the smaller angle is 140° ÷ 2 = 70°. The larger is 70° + 40° = 110°."),
        ("Three angles of a parallelogram are 71°, 109° and 71°. Find the fourth angle.", "109°", ["71°", "289°", "251°"],
         "The 4 angles add up to 360°: 360° − 71° − 109° − 71° = 109°. It is opposite the other 109° angle."),
        ("One angle of a rhombus is 38°. Find the largest angle of the rhombus.", "142°", ["38°", "322°", "52°"],
         "Angles next to each other add up to 180°: 180° − 38° = 142°. The angles are 38°, 142°, 38° and 142°."),
    ]
    for q, ans, wrong, e in words:
        its.append(mcq(q, ans, wrong, e, rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Unknown angles in parallelograms and rhombuses", "items": its}


# ------------------------------------------------------------ set 4: trapeziums
def set_trap_angles(rnd):
    its = []
    T = "ABCD is a trapezium. AB ∥ DC."
    f = trap_fig(68, 55)
    f.ang("A", "B", "D", 68)
    its.append(find_x(f, "D", "A", "C", "trapezium ABCD with angle A 68° and unknown angle x at D", T, [68, 292, 22],
                      "∠DAB and ∠x lie between the parallel sides AB and DC, on side AD. They add up to 180°: "
                      "∠x = 180° − 68° = 112°.", rnd)[0])
    f = trap_fig(75, 57, 170, 80)
    f.ang("B", "C", "A", 57)
    its.append(find_x(f, "C", "D", "B", "trapezium ABCD with angle B 57° and unknown angle x at C", T, [57, 303, 33],
                      "∠ABC and ∠x lie between the parallel sides, on side BC, so they add up to 180°. ∠x = 180° − 57° = 123°.", rnd)[0])
    # upside down: long side on top
    f = trap_fig(62, 70, 170, 80, rot=180)
    f.ang("D", "A", "C", 118)
    its.append(find_x(f, "A", "B", "D", "upside-down trapezium ABCD with angle D 118° and unknown angle x at A", T,
                      [118, 242, 28],
                      "∠ADC and ∠x lie between the parallel sides AB and DC, on side AD, so they add up to 180°. "
                      "∠x = 180° − 118° = 62°.", rnd)[0])
    # parallel sides standing up
    f = trap_fig(80, 74, 150, 75, rot=90, size=(120, 140))
    f.ang("C", "D", "B", 106)
    its.append(find_x(f, "B", "C", "A", "trapezium ABCD standing up with angle C 106° and unknown angle x at B", T,
                      [106, 286, 16],
                      "AB and DC are the parallel sides, even when they stand up. ∠BCD and ∠x are on side BC, "
                      "so they add up to 180°. ∠x = 180° − 106° = 74°.", rnd)[0])
    # AD parallel to BC
    T2 = "ABCD is a trapezium. AD ∥ BC."
    f = trap_fig(70, 116, 170, 80, names="ABCD", start=1)
    # base[1]=A, base[2]=B, base[3]=C, base[0]=D: AD bottom side, BC top side
    f.ang("A", "B", "D", 116)
    its.append(find_x(f, "B", "C", "A", "trapezium ABCD with AD parallel to BC, angle A 116° and unknown angle x at B", T2,
                      [116, 296, 26],
                      "Here the parallel sides are AD and BC. ∠DAB and ∠x are on side AB, between them, so they add up to 180°. "
                      "∠x = 180° − 116° = 64°.", rnd)[0])
    f = trap_fig(60, 79, 170, 80, names="ABCD", start=1)
    f.ang("C", "D", "B", 120)
    its.append(find_x(f, "D", "A", "C", "trapezium ABCD with AD parallel to BC, angle C 120° and unknown angle x at D", T2,
                      [120, 240, 30],
                      "Here the parallel sides are AD and BC. ∠BCD and ∠x are on side CD, between them, so they add up to 180°. "
                      "∠x = 180° − 120° = 60°.", rnd)[0])
    # right trapeziums
    f = trap_fig(90, 63, 150, 85)
    f.rights = [("A", "B", "D"), ("D", "A", "C")]
    f.ang("B", "C", "A", 63)
    its.append(find_x(f, "C", "D", "B", "right-angled trapezium ABCD with angle B 63° and unknown angle x at C", T,
                      [63, 27, 297],
                      "∠ABC and ∠x lie between the parallel sides, on side BC, so they add up to 180°. ∠x = 180° − 63° = 117°.", rnd)[0])
    f = trap_fig(90, 52, 160, 80)
    f.rights = [("A", "B", "D"), ("D", "A", "C")]
    f.ang("C", "D", "B", 128)
    its.append(find_x(f, "B", "C", "A", "right-angled trapezium ABCD with angle C 128° and unknown angle x at B", T,
                      [128, 38, 232],
                      "∠x and ∠BCD are on side BC, between the parallel sides, so they add up to 180°. ∠x = 180° − 128° = 52°.", rnd)[0])
    # extended sides
    f = trap_fig(72, 66, 150, 75)
    f.P["E"] = ext(f.P, "D", "C", 55)
    f.seg("C", "E")
    f.ang("C", "B", "E", 66)
    its.append(find_x(f, "B", "C", "A", "trapezium ABCD with DC extended to E, angle BCE 66° and unknown angle x at B",
                      T + " DCE is a straight line.", [114, 294, 24],
                      "DCE is a straight line, so ∠BCD = 180° − 66° = 114°. ∠x and ∠BCD lie between the parallel sides, "
                      "so ∠x = 180° − 114° = 66°.", rnd)[0])
    f = trap_fig(108, 60, 150, 75)
    f.P["E"] = ext(f.P, "B", "A", 55)
    f.seg("A", "E")
    f.ang("A", "D", "E", 72)
    its.append(find_x(f, "D", "A", "C", "trapezium ABCD with BA extended to E, angle DAE 72° and unknown angle x at D",
                      T + " BAE is a straight line.", [108, 288, 18],
                      "BAE is a straight line, so ∠DAB = 180° − 72° = 108°. ∠x and ∠DAB lie between the parallel sides, "
                      "so ∠x = 180° − 108° = 72°.", rnd)[0])
    f = trap_fig(70, 131, 150, 75)
    f.P["E"] = ext(f.P, "A", "B", 55)
    f.seg("B", "E")
    f.ang("B", "C", "E", 49)
    its.append(find_x(f, "C", "D", "B", "trapezium ABCD with AB extended to E, angle CBE 49° and unknown angle x at C",
                      T + " ABE is a straight line.", [131, 311, 41],
                      "ABE is a straight line, so ∠ABC = 180° − 49° = 131°. ∠x and ∠ABC lie between the parallel sides, "
                      "so ∠x = 180° − 131° = 49°.", rnd)[0])
    # two unknowns
    f = trap_fig(75, 60, 170, 80)
    f.ang("A", "B", "D", 75)
    f.ang("B", "C", "A", 60)
    f.ang("D", "A", "C", "x", True)
    f.ang("C", "D", "B", "y", True)
    x, y = f.value("D", "A", "C"), f.value("C", "D", "B")
    its.append(mcq(fig(f.svg("trapezium ABCD with angles A 75° and B 60° and unknown angles x at D and y at C")) +
                   T + " Find ∠x + ∠y.", deg(x + y), degs(135, 105, 45),
                   "∠x = 180° − 75° = 105° and ∠y = 180° − 60° = 120°. ∠x + ∠y = 105° + 120° = 225°.", rnd))
    f = trap_fig(70, 85, 170, 80)
    f.ang("D", "A", "C", 110)
    f.ang("C", "D", "B", 95)
    f.ang("A", "B", "D", "x", True)
    f.ang("B", "C", "A", "y", True)
    x, y = f.value("A", "B", "D"), f.value("B", "C", "A")
    its.append(mcq(fig(f.svg("trapezium ABCD with angles D 110° and C 95° and unknown angles x at A and y at B")) +
                   T + " Find ∠x + ∠y.", deg(x + y), degs(205, 70, 85),
                   "∠x = 180° − 110° = 70° and ∠y = 180° − 95° = 85°. ∠x + ∠y = 70° + 85° = 155°.", rnd))
    f = trap_fig(70, 55, 170, 80)
    f.ang("A", "B", "D", 70)
    f.ang("B", "C", "A", 55)
    f.ang("C", "D", "B", 125)
    its.append(find_x(f, "D", "A", "C", "trapezium ABCD with angles A 70°, B 55°, C 125° and unknown angle x at D", T,
                      [70, 125, 55],
                      "∠x and ∠DAB lie between the parallel sides, on side AD: ∠x = 180° − 70° = 110°. "
                      "Check: 70° + 55° + 125° + 110° = 360°.", rnd)[0])
    bm = bar_model([("∠W", 3, None, True), ("∠Z", 1, None, False)], "180°", "bar model of angle W as 3 units and angle Z as 1 unit")
    its.append(mcq(fig(bm) + "WXYZ is a trapezium. WX ∥ ZY. ∠W is 3 times as large as ∠Z. Find ∠W.", "135°",
                   ["45°", "60°", "270°"],
                   "∠W and ∠Z are on side WZ, between the parallel sides, so they add up to 180°. "
                   "4 units = 180°, 1 unit = 45°. ∠W = 3 units = 135°.", rnd))
    words = [
        ("PQRS is a trapezium. PQ ∥ SR and ∠Q = 64°. Which of these must be true?", "∠R = 116°",
         ["∠S = 116°", "∠P = 116°", "∠R = 64°"],
         "∠Q and ∠R are at the two ends of side QR, between the parallel sides, so ∠R = 180° − 64° = 116°. "
         "We cannot find ∠P or ∠S from ∠Q."),
        ("The angles of a trapezium are 72°, 108°, 95° and ∠x. Find ∠x.", "85°", ["95°", "108°", "265°"],
         "The 4 angles add up to 360°: ∠x = 360° − 72° − 108° − 95° = 85°. (95° and 85° add up to 180°.)"),
        ("ABCD is a trapezium. AB ∥ DC. ∠A is 24° more than ∠D. Find ∠A.", "102°", ["78°", "156°", "114°"],
         "∠A + ∠D = 180°. 180° − 24° = 156°, so ∠D = 156° ÷ 2 = 78°. ∠A = 78° + 24° = 102°."),
        ("A trapezium has 2 right angles. One of its other angles is 58°. Find the fourth angle.", "122°",
         ["32°", "58°", "148°"],
         "The 4 angles add up to 360°: 360° − 90° − 90° − 58° = 122°. (58° and 122° add up to 180°.)"),
        ("Can a trapezium have exactly 3 right angles?", "No, the 4th would be 90° too",
         ["Yes, always", "Yes, if one side is longer", "No, it has no right angles"],
         "3 × 90° = 270°, so the 4th angle is 360° − 270° = 90°. With 4 right angles the figure is a rectangle, "
         "which has 2 pairs of parallel sides, so it is not a trapezium."),
    ]
    for q, ans, wrong, e in words:
        its.append(mcq(q, ans, wrong, e, rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Unknown angles in trapeziums", "items": its}


# ------------------------------------------------------------ set 5: figures with triangles, word problems
def set_triangles(rnd):
    its = []
    # parallelogram, E on DC, DA = DE
    f = para_fig(68, 165, 85, size=(210, 110))
    f.P["E"] = on_line(f.P, "D", "C", 85.0 / 165)
    f.seg("A", "E")
    f.ticks = [[("D", "A"), ("D", "E")]]
    f.arrows = []
    f.ang("D", "A", "E", 112)
    its.append(find_x(f, "A", "D", "E", "parallelogram ABCD with E on DC, AD equal to DE, angle ADE 112° and unknown angle x",
                      "ABCD is a parallelogram. E is on DC and AD = DE.", [68, 56, 112],
                      "AD = DE, so triangle ADE is isosceles and ∠x = ∠DEA. ∠x = (180° − 112°) ÷ 2 = 68° ÷ 2 = 34°.", rnd)[0])
    f = para_fig(70, 170, 85, size=(210, 110))
    f.P["E"] = on_line(f.P, "D", "C", 85.0 / 170)
    f.seg("A", "E")
    f.ticks = [[("D", "A"), ("D", "E")]]
    f.arrows = []
    f.ang("A", "B", "D", 70)
    its.append(find_x(f, "E", "A", "C", "parallelogram ABCD with E on DC, AD equal to DE, angle A 70° and unknown angle x at E",
                      "ABCD is a parallelogram. E is on DC and AD = DE.", [35, 110, 70],
                      "∠ADE = 180° − 70° = 110° (next to ∠A). Triangle ADE is isosceles: ∠DEA = (180° − 110°) ÷ 2 = 35°. "
                      "DEC is a straight line, so ∠x = 180° − 35° = 145°.", rnd)[0])
    # rhombus with diagonal BD
    f = para_fig(64, 105, 105, rh=True, size=(210, 110))
    f.seg("B", "D")
    f.ang("A", "B", "D", 64)
    its.append(find_x(f, "B", "A", "D", "rhombus ABCD with diagonal BD, angle A 64° and unknown angle x",
                      "ABCD is a rhombus.", [64, 116, 32],
                      "AB = AD, so triangle ABD is isosceles and ∠x = ∠ADB. ∠x = (180° − 64°) ÷ 2 = 58°.", rnd)[0])
    f = para_fig(110, 105, 105, rh=True, size=(210, 110))
    f.seg("B", "D")
    f.ang("B", "C", "D", 35)
    its.append(find_x(f, "A", "B", "D", "rhombus ABCD with diagonal BD, angle CBD 35° and unknown angle x at A",
                      "ABCD is a rhombus.", [70, 145, 35],
                      "CB = CD, so triangle BCD is isosceles: ∠CDB = 35°. ∠BCD = 180° − 35° − 35° = 110°. "
                      "∠x is opposite ∠BCD, so ∠x = 110°.", rnd)[0])
    # parallelogram with diagonal AC
    # built from the angles: ∠BAC = 42, ∠BCA = 31 -> ∠ABC = 107, ∠DAB = 73
    P = {"A": (0.0, 0.0), "B": (160.0, 0.0)}
    t = math.radians(180 - 107)
    BC = 160 * math.sin(math.radians(42)) / math.sin(math.radians(31))
    P["C"] = add(P["B"], (BC * math.cos(t), BC * math.sin(t)))
    P["D"] = sub(P["C"], P["B"])
    f = AFig(P, "ABCD", (210, 110))
    f.arrows = [[("A", "B"), ("D", "C")], [("A", "D"), ("B", "C")]]
    f.seg("A", "C")
    f.ang("A", "B", "C", 42)
    f.ang("C", "B", "A", 31)
    its.append(find_x(f, "D", "A", "C", "parallelogram ABCD with diagonal AC, angles BAC 42° and BCA 31° and unknown angle x at D",
                      "ABCD is a parallelogram.", [73, 138, 149],
                      "In triangle ABC, ∠ABC = 180° − 42° − 31° = 107°. ∠x is opposite ∠ABC, so ∠x = 107°.", rnd)[0])
    P = {"A": (0.0, 0.0), "B": (150.0, 0.0)}
    t = math.radians(180 - 105)
    BC = 150 * math.sin(math.radians(30)) / math.sin(math.radians(45))
    P["C"] = add(P["B"], (BC * math.cos(t), BC * math.sin(t)))
    P["D"] = sub(P["C"], P["B"])
    f = AFig(P, "ABCD", (210, 110))
    f.arrows = [[("A", "B"), ("D", "C")], [("A", "D"), ("B", "C")]]
    f.seg("A", "C")
    f.ang("A", "B", "C", 30)
    f.ang("B", "C", "A", 105)
    its.append(find_x(f, "A", "C", "D", "parallelogram ABCD with diagonal AC, angle BAC 30°, angle B 105° and unknown angle x",
                      "ABCD is a parallelogram.", [75, 30, 105],
                      "∠DAB = 180° − 105° = 75° (next to ∠B). ∠x = ∠DAB − ∠BAC = 75° − 30° = 45°.", rnd)[0])
    # parallelogram, E on AB, DE drawn
    f = para_fig(72, 170, 90, size=(210, 110))
    a, d = 72, 50          # E on AB with ∠ADE = 50, so ∠AED = 58 (sine rule, AD = 90)
    AE = 90 * math.sin(math.radians(d)) / math.sin(math.radians(180 - a - d))
    f.P["E"] = (AE, 0.0)
    f.seg("D", "E")
    f.ang("A", "B", "D", 72)
    f.ang("D", "A", "E", 50)
    its.append(find_x(f, "D", "E", "C", "parallelogram ABCD with E on AB, angle A 72°, angle ADE 50° and unknown angle x",
                      "ABCD is a parallelogram. E is on AB.", [108, 122, 50],
                      "∠ADC = 180° − 72° = 108° (next to ∠A). ∠x = ∠ADC − ∠ADE = 108° − 50° = 58°.", rnd)[0])
    f = para_fig(66, 170, 100, size=(210, 110))
    a, d = 66, 54
    AE = 100 * math.sin(math.radians(d)) / math.sin(math.radians(180 - a - d))
    f.P["E"] = (AE, 0.0)
    f.seg("D", "E")
    f.ang("A", "B", "D", 66)
    f.ang("D", "A", "E", 54)
    its.append(find_x(f, "E", "D", "B", "parallelogram ABCD with E on AB, angle A 66°, angle ADE 54° and unknown angle x at E",
                      "ABCD is a parallelogram. AEB is a straight line.", [60, 114, 66],
                      "In triangle ADE, ∠AED = 180° − 66° − 54° = 60°. AEB is a straight line, so ∠x = 180° − 60° = 120°.", rnd)[0])
    # trapezium with diagonal BD
    f = trap_fig(76, 62, 170, 85, size=(210, 110))
    f.seg("B", "D")
    # move D so that ∠ABD = 40: keep A, B, the angle at A and the height, fix it by choosing the height
    a, p = 76, 40
    AB = 170.0
    AD = AB * math.sin(math.radians(p)) / math.sin(math.radians(180 - a - p))
    f.P["D"] = (AD * math.cos(math.radians(a)), AD * math.sin(math.radians(a)))
    h = f.P["D"][1]
    f.P["C"] = (AB - h / math.tan(math.radians(62)), h)
    assert f.P["C"][0] - f.P["D"][0] > 40
    f.ang("A", "B", "D", 76)
    f.ang("B", "A", "D", 40)
    its.append(find_x(f, "D", "B", "C", "trapezium ABCD with diagonal BD, angle A 76°, angle ABD 40° and unknown angle x",
                      "ABCD is a trapezium. AB ∥ DC.", [64, 104, 140],
                      "∠ADC = 180° − 76° = 104° (between the parallel sides). In triangle ABD, ∠ADB = 180° − 76° − 40° = 64°. "
                      "∠x = 104° − 64° = 40°.", rnd)[0])
    # trapezium, E on DC, BE = BC
    for c, ask, wrong, e in [
        (70, ("B", "E", "C"), [70, 110, 55],
         "BE = BC, so triangle BCE is isosceles: ∠BEC = ∠BCE = 70°. ∠x = 180° − 70° − 70° = 40°."),
        (65, ("B", "A", "E"), [50, 115, 130],
         "∠ABC = 180° − 65° = 115° (between the parallel sides). Triangle BCE is isosceles, so ∠BEC = 65° and "
         "∠EBC = 180° − 65° − 65° = 50°. ∠x = 115° − 50° = 65°."),
    ]:
        f = trap_fig(72, 180 - c, 175, 95, size=(210, 110))
        P = f.P
        BC = dist(P["B"], P["C"])
        # E: from C go along CD by 2·BC·cos c, so that BE = BC
        CE = 2 * BC * math.cos(math.radians(c))
        P["E"] = (P["C"][0] - CE, P["C"][1])
        assert P["E"][0] - P["D"][0] > 25
        f.seg("B", "E")
        f.ticks = [[("B", "E"), ("B", "C")]]
        f.ang("C", "B", "E", c)
        V = "B"
        q, ans = find_x(f, V, ask[1], ask[2], "trapezium ABCD with E on DC, BE equal to BC, angle C %d° and unknown angle x" % c,
                        "ABCD is a trapezium. AB ∥ DC. E is on DC and BE = BC.", wrong, e, rnd)
        its.append(q)
    # right trapezium with diagonal AC: ∠DCA = 34, ∠B = 70
    h = 80.0
    DC = h / math.tan(math.radians(34))
    AB = DC + h / math.tan(math.radians(70))
    P = {"A": (0.0, 0.0), "B": (AB, 0.0), "C": (DC, h), "D": (0.0, h)}
    f = AFig(P, "ABCD", (210, 110))
    f.arrows = [[("A", "B"), ("D", "C")]]
    f.rights = [("A", "B", "D"), ("D", "A", "C")]
    f.seg("A", "C")
    f.ang("C", "D", "A", 34)
    f.ang("B", "C", "A", 70)
    its.append(find_x(f, "C", "A", "B", "right-angled trapezium ABCD with diagonal AC, angle DCA 34°, angle B 70° and unknown angle x",
                      "ABCD is a trapezium. AB ∥ DC.", [56, 110, 34],
                      "In triangle ACD, ∠DAC = 180° − 90° − 34° = 56°, so ∠BAC = 90° − 56° = 34°. "
                      "In triangle ABC, ∠x = 180° − 70° − 34° = 76°.", rnd)[0])
    bm = bar_model([("small", 1, None, True), ("large", 4, None, False)], "180°", "bar model of the smaller angle as 1 unit and the larger as 4 units")
    its.append(mcq(fig(bm) + "Mr Tan’s plot in the community garden is a parallelogram. One angle is 4 times as large as "
                   "the angle next to it. Find the smaller angle.", "36°", ["45°", "144°", "72°"],
                   "Angles next to each other add up to 180°. 5 units = 180°, 1 unit = 180° ÷ 5 = 36°.", rnd))
    bm = bar_model([("larger", 1, ("50°", 0.9), True), ("smaller", 1, None, False)], "180°",
                   "bar model of the larger angle as 1 unit and 50° and the smaller angle as 1 unit")
    its.append(mcq(fig(bm) + "The top of a study table is a trapezium. Two of its angles are at the ends of a slanted side, "
                   "between the parallel sides. One is 50° more than the other. Find the larger angle.", "115°",
                   ["65°", "130°", "140°"],
                   "The two angles add up to 180°. 2 units = 180° − 50° = 130°, 1 unit = 65°. Larger angle = 65° + 50° = 115°.", rnd))
    world = [
        ("A floor tile at the void deck is a rhombus. One of its angles is 58°. Find the largest angle of the tile.", "122°",
         ["58°", "302°", "32°"],
         "Angles next to each other in a rhombus add up to 180°: 180° − 58° = 122°."),
        ("Ali cuts a rhombus card along the diagonal that joins its two 110° angles. What are the angles of each triangle?",
         "55°, 55°, 70°", ["35°, 35°, 110°", "55°, 55°, 110°", "70°, 70°, 40°"],
         "The cut splits each 110° angle into 55° and 55°. The third angle of each triangle is the other angle of the rhombus: "
         "180° − 110° = 70°. Check: 55° + 55° + 70° = 180°."),
        ("Hui Min bends a 60 cm wire to make a parallelogram. One side is 18 cm. How long is a side next to it?", "12 cm",
         ["42 cm", "24 cm", "21 cm"],
         "Opposite sides are equal: 18 + 18 = 36 cm. The other two sides share 60 − 36 = 24 cm, so each is 12 cm."),
        ("From the side, the roof of a bus shelter is a trapezium with parallel top and bottom. Both bottom angles are 62°. "
         "Find the sum of the two top angles.", "236°", ["124°", "118°", "298°"],
         "Each top angle is 180° − 62° = 118° (between the parallel sides). 118° + 118° = 236°."),
        ("Zhi Hao measures a quadrilateral. Its angles are 75°, 105°, 75° and 105°, and its sides are 6 cm, 4 cm, 6 cm and 4 cm, in order. "
         "What is its best name?", "parallelogram", ["rhombus", "trapezium", "rectangle"],
         "Opposite sides are equal and opposite angles are equal, so it is a parallelogram. "
         "The sides are not all equal (not a rhombus) and there are no right angles (not a rectangle)."),
        ("Raju draws parallelogram PQRS and joins the diagonal PR. ∠SPR = 35° and ∠PRS = 40°. Find ∠PQR.", "105°",
         ["75°", "145°", "140°"],
         "In triangle PRS, ∠PSR = 180° − 35° − 40° = 105°. ∠PQR is opposite ∠PSR, so ∠PQR = 105°."),
    ]
    for q, ans, wrong, e in world:
        its.append(mcq(q, ans, wrong, e, rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Figures with triangles and word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    family = strip_svg([(PARA, 0, "parallelogram", {"marks": ("arrows",)}), (RHO, 0, "rhombus", {"marks": ("ticks", "rights")}),
                        (TRAPG, 0, "trapezium", {})],
                       "parallelogram, rhombus and trapezium with marks", cols=3)
    f1 = para_fig(70, 150, 85)
    f1.ang("A", "B", "D", 70).ang("B", "C", "A", 110).ang("C", "D", "B", 70).ang("D", "A", "C", 110)
    pf = f1.svg("parallelogram ABCD with angles 70°, 110°, 70° and 110°")
    f2 = trap_fig(65, 50, 170, 80)
    f2.ang("A", "B", "D", 65).ang("D", "A", "C", 115).ang("B", "C", "A", 50).ang("C", "D", "B", 130)
    tf = f2.svg("trapezium ABCD with AB parallel to DC and angles 65°, 50°, 130° and 115°")
    f3 = para_fig(64, 105, 105, rh=True)
    f3.seg("B", "D")
    f3.ang("A", "B", "D", 64)
    f3.ang("B", "A", "D", "x", True)
    assert f3.value("B", "A", "D") == 58
    rf = f3.svg("rhombus ABCD with diagonal BD, angle A 64° and unknown angle x")
    bm = bar_model([("∠A", 2, None, True), ("∠B", 1, None, False)], "180°", "bar model of angle A as 2 units and angle B as 1 unit")
    return (
        "<h2>Parallelogram, rhombus and trapezium</h2>"
        "<p>Arrows show parallel sides. Tick marks show equal sides. Name a figure by what it <b>must</b> have.</p>"
        "<figure class='sn-fig'>" + family +
        "<figcaption>A parallelogram has 2 pairs of parallel sides. A rhombus is a parallelogram with 4 equal sides. "
        "A trapezium has exactly 1 pair of parallel sides.</figcaption></figure>" +
        table(["Figure", "Sides", "Angles"], [
            ["Parallelogram", "2 pairs of parallel sides; opposite sides are equal", "Opposite angles are equal"],
            ["Rhombus", "A parallelogram with 4 equal sides", "Opposite angles are equal"],
            ["Square", "A rhombus with 4 right angles", "All 4 angles are 90°"],
            ["Trapezium", "Exactly 1 pair of parallel sides", "The 2 angles on each slanted side add up to 180°"],
        ]) +
        "<h2>Angles in a parallelogram and a rhombus</h2>"
        "<p>Opposite angles are <b>equal</b>. Angles next to each other add up to <b>180°</b>. All 4 angles add up to 360°.</p>"
        "<figure class='sn-fig'>" + pf +
        "<figcaption>70° + 110° = 180°. The 70° angles are opposite each other, and so are the 110° angles.</figcaption></figure>" +
        ex("Example 1", "ABCD is a parallelogram and ∠A = 64°. Find ∠B and ∠C.",
           "∠B is next to ∠A: ∠B = 180° − 64° = 116°. ∠C is opposite ∠A, so ∠C = 64°.", "∠B = 116°, ∠C = 64°") +
        "<figure class='sn-fig'>" + bm +
        "<figcaption>∠A is twice ∠B: 3 units = 180°, 1 unit = 60°, so ∠A = 120°.</figcaption></figure>"
        "<h2>Angles in a trapezium</h2>"
        "<p>Find the parallel sides first. The 2 angles at the ends of each slanted side lie between the parallel sides, "
        "so they add up to 180°. Opposite angles of a trapezium are usually <b>not</b> equal.</p>"
        "<figure class='sn-fig'>" + tf +
        "<figcaption>AB ∥ DC. ∠A + ∠D = 65° + 115° = 180° and ∠B + ∠C = 50° + 130° = 180°.</figcaption></figure>" +
        ex("Example 2", "ABCD is a trapezium with AB ∥ DC. ∠B = 48°. Find ∠C.",
           "∠B and ∠C are at the ends of side BC, between the parallel sides. ∠C = 180° − 48°.", "132°") +
        "<h2>Figures with triangles</h2>"
        "<p>Use the facts one step at a time: the angles of a triangle add up to 180°, angles on a straight line add up to 180°, "
        "and an isosceles triangle has 2 equal angles.</p>"
        "<figure class='sn-fig'>" + rf +
        "<figcaption>AB = AD (a rhombus has 4 equal sides), so triangle ABD is isosceles.</figcaption></figure>" +
        ex("Example 3", "ABCD is a rhombus and ∠A = 64°. Find ∠x = ∠ABD.",
           "Triangle ABD is isosceles, so ∠ABD = ∠ADB. ∠x = (180° − 64°) ÷ 2 = 116° ÷ 2.", "58°") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Opposite angles of a parallelogram add up to 180°", "Opposite angles are equal. Angles next to each other add up to 180°"],
            ["A trapezium has 2 pairs of parallel sides", "A trapezium has exactly 1 pair. 2 pairs make a parallelogram"],
            ["A rhombus must have right angles, like a square", "A rhombus needs only 4 equal sides. A square is a rhombus with right angles"],
            ["In a trapezium, ∠A + ∠B = 180°", "Add the 2 angles on the same slanted side, such as ∠A + ∠D when AB ∥ DC"],
            ["Writing 360° − the given angle", "Use 180° for angles next to each other, and 360° only for all 4 angles"],
        ])
    )


FAQ = [
    {"q": "What is taught about parallelograms, rhombuses and trapeziums in P5?",
     "a": "Primary 5 students learn the properties of a parallelogram, a rhombus and a trapezium, and use them to find unknown angles, "
          "including in figures made with triangles."},
    {"q": "Is a square a rhombus?",
     "a": "Yes. A rhombus is a parallelogram with 4 equal sides, and a square has 4 equal sides, so a square is a rhombus with 4 right angles."},
    {"q": "What is the most common mistake with angles in a parallelogram?",
     "a": "Thinking that opposite angles add up to 180°. Opposite angles are equal; it is the angles next to each other that add up to 180°."},
    {"q": "Is this topic in the MOE syllabus for Primary 5?",
     "a": "Yes. Properties of the parallelogram, rhombus and trapezium and finding unknown angles are Primary 5 Geometry in the MOE 2021 "
          "Primary Mathematics Syllabus, and angle questions like these also appear in the PSLE."},
]


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    rnd = random.Random(65815)
    spots = Spots(rnd)
    sets = [set_name(rnd, spots), set_properties(rnd), set_para_angles(rnd), set_trap_angles(rnd), set_triangles(rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len({plain(c) for c in it["c"]}) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "sg", "subject": "maths", "grade": "primary-5", "slug": "parallelograms-rhombuses-and-trapeziums", "sort": 15,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 5 Parallelograms, Rhombuses and Trapeziums: Properties and Unknown Angles",
        "seo_title": "P5 Parallelogram, Rhombus and Trapezium Worksheets: Free Primary 5 Maths with Answers (MOE Syllabus)",
        "short_title": "Parallelograms, Rhombuses and Trapeziums",
        "domain": "Measurement and Geometry",
        "standard_code": "Primary 5: Geometry",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Properties of parallelogram, rhombus and trapezium; finding unknown angles",
        "meta_desc": "Free P5 practice: name parallelograms, rhombuses and trapeziums, use their properties and find unknown angles. "
                     "100 questions with answers.",
        "key_big": "In a parallelogram, opposite angles are equal and angles next to each other add up to 180°.",
        "key_sub": "∠A = 64°, so ∠B = 180° − 64° = 116° and ∠C = 64°. In a trapezium, the 2 angles on a slanted side add up to 180°.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "(four figures labelled A to D|bar model|.*(with E on|with diagonal|extended to))")
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    os.makedirs(OUT, exist_ok=True)
    path_ = os.path.join(OUT, u["slug"] + ".json")
    with open(path_, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path_)
