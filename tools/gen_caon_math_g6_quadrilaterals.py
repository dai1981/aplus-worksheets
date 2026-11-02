# -*- coding: utf-8 -*-
"""
CA Grade 6 Math: Quadrilaterals and Congruence (Ontario Mathematics Curriculum 2020, Grade 6: Spatial Sense, E1)
  python3 tools/gen_ca_math_g6_quadrilaterals.py
Naming quadrilaterals from their properties (square, rectangle, rhombus, parallelogram, trapezoid, kite),
the properties of their diagonals, line and rotational symmetry, congruent shapes, and statements that are
always true, with Canadian word problems.

Definitions used everywhere (inclusive, as in the lesson):
  rectangle      4 right angles                 rhombus     4 equal sides
  square         4 equal sides and 4 right angles (so also a rectangle and a rhombus)
  parallelogram  2 pairs of parallel sides
  trapezoid      every trapezoid drawn or described has exactly one pair of parallel sides,
                 so both common definitions agree
  kite           2 pairs of equal sides that are next to each other; every kite drawn here is not a rhombus
Every drawing is checked in code: its name, its tick marks / right-angle marks / arrows, the facts about
its diagonals (equal, cut each other in half, cross at right angles), its lines of symmetry and its order of
rotational symmetry are all computed from the real coordinates, and every answer about a drawing is the
computed one. Congruent shapes on dot paper are made by turning or flipping the first shape in code, and
every shape that is not congruent is proved different (side lengths or area).
Wrong answers come from real student mistakes: a square is not a rectangle, a rhombus has equal diagonals,
the diagonals of a rectangle are lines of symmetry or cross at right angles, a parallelogram has 2 lines of
symmetry, order 0 for no rotational symmetry, halving or doubling a diagonal, thinking a flipped or turned
shape is not congruent, and thinking equal area or equal perimeter means congruent.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
DOT = "#9a9a9a"
BLUE = "#2f6db5"


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
            "role='img' aria-label='%s'>%s</svg>" % (w, h, w, h, label, body))


def cm(x):
    s = ("%.2f" % x).rstrip("0").rstrip(".")
    return s + " cm"


def deg(x):
    return "%d°" % x


# ------------------------------------------------------------ geometry
def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def norm(v):
    L = math.hypot(v[0], v[1])
    return (v[0] / L, v[1] / L)


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def side_lens(pts):
    n = len(pts)
    return [dist(pts[(i + 1) % n], pts[i]) for i in range(n)]


def angles(pts):
    n = len(pts)
    out = []
    for i in range(n):
        u = norm(sub(pts[i - 1], pts[i]))
        v = norm(sub(pts[(i + 1) % n], pts[i]))
        out.append(math.degrees(math.acos(max(-1, min(1, u[0] * v[0] + u[1] * v[1])))))
    return out


def side_angle_diff(pts, i, j):
    n = len(pts)
    a = sub(pts[(i + 1) % n], pts[i])
    b = sub(pts[(j + 1) % n], pts[j])
    t = abs(math.degrees(math.atan2(a[1], a[0]) - math.atan2(b[1], b[0]))) % 180
    return min(t, 180 - t)


def facts(pts):
    L = side_lens(pts)
    A = angles(pts)
    eq = all(close(L[0], x) for x in L)
    rights = [i for i, a in enumerate(A) if abs(a - 90) < 1e-6]
    par = [p for p in [(0, 2), (1, 3)] if side_angle_diff(pts, *p) < 1e-6]
    return {"lens": L, "angles": A, "equal": eq, "rights": rights, "par": par}


def is_kite(pts):
    L = side_lens(pts)
    return any(close(L[i], L[(i + 1) % 4]) and close(L[(i + 2) % 4], L[(i + 3) % 4]) for i in range(4)) \
        and not all(close(L[0], x) for x in L)


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
    if is_kite(pts):
        return "kite"
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


def inter(p1, p2, p3, p4):
    """Intersection of line p1p2 with line p3p4 (they must cross)."""
    d1, d2 = sub(p2, p1), sub(p4, p3)
    den = d1[0] * d2[1] - d1[1] * d2[0]
    t = ((p3[0] - p1[0]) * d2[1] - (p3[1] - p1[1]) * d2[0]) / den
    return (p1[0] + t * d1[0], p1[1] + t * d1[1])


def diag_facts(pts):
    A, B, C, D = pts
    E = inter(A, C, B, D)
    ac, bd = dist(A, C), dist(B, D)
    u, v = sub(C, A), sub(D, B)
    perp = abs(u[0] * v[0] + u[1] * v[1]) < 1e-6 * ac * bd
    ac_cut = close(dist(A, E), dist(E, C))   # AC is cut in half by BD
    bd_cut = close(dist(B, E), dist(E, D))
    return {"E": E, "equal": close(ac, bd), "perp": perp, "bisect": ac_cut and bd_cut,
            "one": ac_cut != bd_cut, "none": not ac_cut and not bd_cut}


def reflect(p, a, d):
    """Reflect p in the line through a with unit direction d."""
    w = sub(p, a)
    t = w[0] * d[0] + w[1] * d[1]
    f = (a[0] + d[0] * t, a[1] + d[1] * t)
    return (2 * f[0] - p[0], 2 * f[1] - p[1])


def same_set(ps, qs, tol=1e-6):
    used = set()
    for p in ps:
        for k, q in enumerate(qs):
            if k not in used and dist(p, q) < tol * 1000:
                used.add(k)
                break
        else:
            return False
    return True


def sym_lines(pts):
    """All lines of symmetry of a polygon (as (point, unit direction)), found by testing every line
    through two of the vertices and side midpoints."""
    n = len(pts)
    cand = list(pts) + [((pts[i][0] + pts[(i + 1) % n][0]) / 2, (pts[i][1] + pts[(i + 1) % n][1]) / 2) for i in range(n)]
    out = []
    for i in range(len(cand)):
        for j in range(i + 1, len(cand)):
            if dist(cand[i], cand[j]) < 1e-6:
                continue
            a, d = cand[i], norm(sub(cand[j], cand[i]))
            if not same_set([reflect(p, a, d) for p in pts], pts):
                continue
            dup = False
            for a2, d2 in out:
                cr = d[0] * d2[1] - d[1] * d2[0]
                w = sub(a, a2)
                if abs(cr) < 1e-9 and abs(w[0] * d2[1] - w[1] * d2[0]) < 1e-6:
                    dup = True
            if not dup:
                out.append((a, d))
    return out


def rot_order(pts):
    n = len(pts)
    c = (sum(p[0] for p in pts) / n, sum(p[1] for p in pts) / n)
    order = 1
    for k in range(2, n + 1):
        if n % k:
            continue
        t = 2 * math.pi / k
        r = [(c[0] + (p[0] - c[0]) * math.cos(t) - (p[1] - c[1]) * math.sin(t),
              c[1] + (p[0] - c[0]) * math.sin(t) + (p[1] - c[1]) * math.cos(t)) for p in pts]
        if same_set(r, pts):
            order = k
    return order


# ------------------------------------------------------------ shapes (y goes down, like SVG)
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
    return S([(0, h), (bottom, h), (off + top, 0), (off, 0)], "trapezoid")


def rtrap(bottom, top, h):
    return S([(0, h), (bottom, h), (top, 0), (0, 0)], "trapezoid")


def kite(w, a, b):
    """A at the top, B on the right, C at the bottom, D on the left. AC is the line of symmetry."""
    return S([(0, 0), (w, a), (0, a + b), (-w, a)], "kite")


SQ = square()
RECT = rect(150, 85)
RHO = rhombus(60)
RHO2 = rhombus(70)
PARA = para(150, 80, 60)
PARA2 = para(140, 90, 55)
ISO = trap(150, 70, 80, 40)          # trapezoid with equal legs
TRAPG = trap(150, 60, 75, 20)        # trapezoid with no equal sides
RTRAP = rtrap(150, 70, 90)
KITE1 = kite(70, 25, 100)
KITE2 = kite(50, 35, 120)


def rot_pt(p, d):
    t = math.radians(d)
    return (p[0] * math.cos(t) - p[1] * math.sin(t), p[0] * math.sin(t) + p[1] * math.cos(t))


def placed(sh, rot, bw, bh, cx, cy):
    pts = [rot_pt(p, rot) for p in sh["pts"]]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    k = min(bw / (max(xs) - min(xs)), bh / (max(ys) - min(ys)))
    mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    return [(cx + (p[0] - mx) * k, cy + (p[1] - my) * k) for p in pts]


def clip_line(pts, a, d, ext=14):
    """Segment of the line (a, d) that crosses the convex polygon, extended by ext at both ends."""
    n = len(pts)
    ts = []
    for i in range(n):
        p, q = pts[i], pts[(i + 1) % n]
        e = sub(q, p)
        den = d[0] * e[1] - d[1] * e[0]
        if abs(den) < 1e-12:
            continue
        w = sub(p, a)
        t = (w[0] * e[1] - w[1] * e[0]) / den
        s = (w[0] * d[1] - w[1] * d[0]) / den
        if -1e-9 <= s <= 1 + 1e-9:
            ts.append(t)
    t0, t1 = min(ts) - ext, max(ts) + ext
    return (a[0] + d[0] * t0, a[1] + d[1] * t0), (a[0] + d[0] * t1, a[1] + d[1] * t1)


def line_spec(pts, spec):
    """('d', i, j): line through vertices i and j. ('m', i, j): through the midpoints of sides i and j."""
    n = len(pts)
    if spec[0] == "d":
        a, b = pts[spec[1]], pts[spec[2]]
    else:
        m = lambda i: ((pts[i][0] + pts[(i + 1) % n][0]) / 2, (pts[i][1] + pts[(i + 1) % n][1]) / 2)
        a, b = m(spec[1]), m(spec[2])
    return a, norm(sub(b, a))


def is_sym_line(pts, a, d):
    return same_set([reflect(p, a, d) for p in pts], pts)


def shape_elems(sh, rot, bw, bh, cx, cy, marks=("ticks", "rights"), sw=3, lines=(), labels=False, diag_mark=False):
    """SVG elements for one shape plus its marks, and the box around everything drawn.
    marks: ticks (equal sides), rights (right angles), arrows (parallel sides), diags (both diagonals)."""
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
    if "diags" in marks:
        df = diag_facts(pts)
        for i, j in [(0, 2), (1, 3)]:
            el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.8'/>"
                      % (pts[i] + pts[j] + (BLUE,)))
        if diag_mark and df["perp"]:
            E = df["E"]
            u1, u2 = norm(sub(pts[0], E)), norm(sub(pts[1], E))
            k = 8
            q1 = (E[0] + u1[0] * k, E[1] + u1[1] * k)
            q2 = (q1[0] + u2[0] * k, q1[1] + u2[1] * k)
            q3 = (E[0] + u2[0] * k, E[1] + u2[1] * k)
            el.append("<polyline points='%s' %s/>" % (P([q1, q2, q3]), mk.replace("stroke-width='2'", "stroke-width='1.6'")))
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
    for spec in lines:
        a, d = line_spec(pts, spec)
        p1, p2 = clip_line(pts, a, d)
        el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.4' "
                  "stroke-dasharray='7 5'/>" % (p1 + p2 + (RED,)))
        box += [p1, p2]
    if labels:
        c = (sum(p[0] for p in pts) / n, sum(p[1] for p in pts) / n)
        for i, p in enumerate(pts):
            u = norm(sub(p, c))
            t = (p[0] + u[0] * 13, p[1] + u[1] * 13)
            el.append("<text x='%.1f' y='%.1f' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                      % (t[0], t[1] + 5, INK, "ABCD"[i]))
            box += [(t[0] - 6, t[1] - 8), (t[0] + 6, t[1] + 8)]
        if "diags" in marks:
            E = diag_facts(pts)["E"]
            # put E where the letter is farthest from every line drawn (sides, diagonals, tick marks)
            segs = [(pts[i], pts[(i + 1) % n]) for i in range(n)] + [(pts[0], pts[2]), (pts[1], pts[3])]
            segs += [((float(a), float(b)), (float(c), float(d))) for a, b, c, d in
                     [tuple(map(float, m)) for m in re.findall(r"<line x1='([\d.-]+)' y1='([\d.-]+)' x2='([\d.-]+)' y2='([\d.-]+)' stroke='%s' stroke-width='2'" % INK, "".join(el))]]
            best = None
            for k in range(72):
                ang = 2 * math.pi * k / 72
                for r in (13, 16, 20):
                    t = (E[0] + math.cos(ang) * r, E[1] + math.sin(ang) * r)
                    # the letter is about 11 x 14: test its corners and centre
                    probe = [t, (t[0] - 5, t[1] - 6), (t[0] + 5, t[1] - 6), (t[0] - 5, t[1] + 6), (t[0] + 5, t[1] + 6)]
                    if not all(inside(p, pts) for p in probe):
                        continue
                    sc = min(seg_dist(p, a, b) for p in probe for a, b in segs)
                    if best is None or sc > best[0] + 1e-9:
                        best = (sc, t)
            assert best[0] >= 2.5, (sh["kind"], best)
            t = best[1]
            el.append("<text x='%.1f' y='%.1f' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>E</text>"
                      % (t[0], t[1] + 5, INK))
    if sh["kind"] != "other":
        assert quad_name(pts) == sh["kind"], (sh["kind"], quad_name(pts))
    pad = sw / 2.0 + 1
    bb = (min(p[0] for p in box) - pad, min(p[1] for p in box) - pad,
          max(p[0] for p in box) + pad, max(p[1] for p in box) + pad)
    return el, bb, pts


def shape_svg(sh, rot=0, bw=140, bh=95, marks=("ticks", "rights"), label="quadrilateral", lines=(), labels=False):
    _, bb, _ = shape_elems(sh, rot, bw, bh, 0, 0, marks, lines=lines, labels=labels)
    pad = 5
    W, H = int(math.ceil(bb[2] - bb[0] + 2 * pad)), int(math.ceil(bb[3] - bb[1] + 2 * pad))
    if W == H:
        W += 1
    el, bb2, pts = shape_elems(sh, rot, bw, bh, pad - bb[0] + (W - (bb[2] - bb[0] + 2 * pad)) / 2,
                               pad - bb[1] + (H - (bb[3] - bb[1] + 2 * pad)) / 2, marks, lines=lines, labels=labels)
    assert bb2[0] >= 0 and bb2[1] >= 0 and bb2[2] <= W and bb2[3] <= H
    return svg_wrap(W, H, "".join(el), label), pts


CELL = 118


def grid_svg(items, marks=("ticks", "rights"), label="four shapes labelled A to D"):
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
                               opt.get("marks", ("ticks", "rights")), sw=2.8, lines=opt.get("lines", ()),
                               diag_mark=opt.get("diag_mark", False))
        assert bb[0] >= x0 + 2 and bb[2] <= x0 + cw - 2 and bb[1] >= y0 + 2 and bb[3] <= y0 + top - 2, (cap, bb)
        el += e
        el.append("<text x='%d' y='%d' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                  % (x0 + cw / 2, y0 + top + 16, INK, cap))
    return svg_wrap(cw * cols, rh * rows, "".join(el), label)


# ------------------------------------------------------------ dot paper (congruence)
U = 20        # one grid unit


def g_area(p):
    return abs(sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p)))) / 2.0


def g_sides(p):
    n = len(p)
    return sorted((p[i][0] - p[(i + 1) % n][0]) ** 2 + (p[i][1] - p[(i + 1) % n][1]) ** 2 for i in range(n))


def g_norm(p):
    mx, my = min(x for x, y in p), min(y for x, y in p)
    return [(x - mx, y - my) for x, y in p]


TF = {"turn90": lambda x, y: (-y, x), "turn180": lambda x, y: (-x, -y), "turn270": lambda x, y: (y, -x),
      "flipx": lambda x, y: (-x, y), "flipy": lambda x, y: (x, -y), "flipd": lambda x, y: (y, x)}


def g_tf(p, name):
    return g_norm([TF[name](x, y) for x, y in p])


def g_canon(p):
    best = None
    for f in [lambda x, y: (x, y)] + list(TF.values()) + [lambda x, y: (-y, -x)]:
        q = g_norm([f(x, y) for x, y in p])
        n = len(q)
        for seq in (q, q[::-1]):
            for s in range(n):
                t = tuple(seq[s:] + seq[:s])
                if best is None or t < best:
                    best = t
    return best


def congruent(a, b):
    return g_canon(a) == g_canon(b)


def surely_not_congruent(a, b):
    return g_sides(a) != g_sides(b) or g_area(a) != g_area(b)


def dot_cell(p, x0, y0, letter, n=4):
    """A dot-paper cell with the shape and its letter. Grid 0..n, top-left of the grid at (x0 + 22, y0 + 24)."""
    p = g_norm(p)
    w, h = max(x for x, y in p), max(y for x, y in p)
    assert w <= n and h <= n, p
    ox, oy = (n - w) // 2, (n - h) // 2
    gx, gy = x0 + 22, y0 + 24
    el = []
    for i in range(n + 1):
        for j in range(n + 1):
            el.append("<circle cx='%d' cy='%d' r='1.8' fill='%s'/>" % (gx + i * U, gy + j * U, DOT))
    el.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.6' stroke-linejoin='round'/>"
              % (" ".join("%d,%d" % (gx + (x + ox) * U, gy + (y + oy) * U) for x, y in p), FILL, GREEN))
    el.append("<text x='%d' y='%d' font-size='17' font-weight='700' fill='%s'>%s</text>" % (x0 + 5, y0 + 19, INK, letter))
    return el


DC = 110      # dot cell size


def cong_grid_svg(P, items, label="shape P and four shapes labelled A to D"):
    el = []
    W, H = 3 * DC, 2 * DC
    el += dot_cell(P, 0, DC // 2, "P")
    el.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>" % (DC, DC, H - 4, GREEN))
    el.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (2 * DC, 2 * DC, H - 4, GRAY))
    el.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (DC + 4, DC, W - 4, DC, GRAY))
    for k, p in enumerate(items):
        el += dot_cell(p, DC + (k % 2) * DC, (k // 2) * DC, "ABCD"[k])
    return svg_wrap(W, H, "".join(el), label)


def pair_dot_svg(a, b, label="shape P and shape Q on dot paper"):
    el = dot_cell(a, 0, 0, "P") + dot_cell(b, DC, 0, "Q")
    el.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (DC, DC, DC - 4, GRAY))
    return svg_wrap(2 * DC + 1, DC, "".join(el), label)


# ------------------------------------------------------------ set 1: name the quadrilateral
NAMES = ["square", "rectangle", "rhombus", "parallelogram", "trapezoid", "kite"]
WHY = {
    "square": "The tick marks show 4 equal sides and the small squares show 4 right angles, so it is a square. "
              "It is also a rectangle and a rhombus, but square is the best name because it tells the most.",
    "rectangle": "The small squares show 4 right angles, so it is a rectangle. Only opposite sides are equal, so it is not a square.",
    "rhombus": "The tick marks show 4 equal sides, so it is a rhombus. There are no right angles, so it is not a square.",
    "parallelogram": "The arrows show 2 pairs of parallel sides, so it is a parallelogram. There are no right angles and "
                     "the sides are not all equal, so it is not a rectangle or a rhombus.",
    "trapezoid": "The arrows show exactly 1 pair of parallel sides. The other 2 sides are not parallel, so it is a trapezoid.",
    "kite": "The tick marks show 2 pairs of equal sides, and each pair is next to each other (not opposite). "
            "That makes it a kite. Its sides are not all equal, so it is not a rhombus.",
}
WRONG = {
    "square": ["rhombus", "rectangle", "kite"],
    "rectangle": ["square", "parallelogram", "trapezoid"],
    "rhombus": ["square", "kite", "parallelogram"],
    "parallelogram": ["rectangle", "rhombus", "trapezoid"],
    "trapezoid": ["parallelogram", "kite", "rectangle"],
    "kite": ["rhombus", "trapezoid", "parallelogram"],
}


def set_name(rnd):
    its = []
    plan = [(SQ, 30, (110, 90)), (SQ, 0, (90, 70)), (RECT, 0, (150, 90)), (rect(150, 70), 90, (90, 110)),
            (RHO, 60, (110, 100)), (RHO2, 0, (150, 95)), (PARA, 0, (150, 85)), (PARA2, -20, (150, 95)),
            (ISO, 0, (150, 85)), (RTRAP, 0, (150, 85)), (KITE1, 0, (110, 100)), (KITE2, 90, (150, 90))]
    for sh, rot, size in plan:
        k = sh["kind"]
        marks = {"trapezoid": ("ticks", "rights", "arrows"), "parallelogram": ("arrows",)}.get(k, ("ticks", "rights"))
        svg, _ = shape_svg(sh, rot, size[0], size[1], marks, label=k + " with marks")
        e = WHY[k] + (" Turning a shape does not change its name." if rot % 90 else "")
        its.append(mcq(fig(svg) + "What is the best name for this quadrilateral? Use the marks.", k, WRONG[k], e, rnd))
    words = [
        ("A quadrilateral has 4 equal sides and 4 right angles. What is its best name?", "square",
         ["rhombus", "rectangle", "kite"],
         "4 right angles make a rectangle and 4 equal sides make a rhombus. A shape with both is a square, the name that tells the most."),
        ("A quadrilateral has 4 right angles. Its sides, in order, are 8 cm, 5 cm, 8 cm and 5 cm. What is its best name?",
         "rectangle", ["square", "parallelogram", "rhombus"],
         "4 right angles make it a rectangle. The sides are not all equal (8 cm and 5 cm), so it is not a square."),
        ("A quadrilateral has 4 equal sides. Its angles, in order, are 60°, 120°, 60° and 120°. What is its best name?",
         "rhombus", ["square", "kite", "parallelogram"],
         "4 equal sides make it a rhombus. The angles are not 90°, so it is not a square."),
        ("A quadrilateral has sides 7 cm, 4 cm, 7 cm and 4 cm (in order) and angles 70°, 110°, 70° and 110°. What is its best name?",
         "parallelogram", ["rectangle", "rhombus", "kite"],
         "Opposite sides are equal and opposite angles are equal, so it is a parallelogram. "
         "It has no right angles (not a rectangle) and its sides are not all equal (not a rhombus)."),
        ("A quadrilateral has exactly one pair of parallel sides. What is it called?", "trapezoid",
         ["parallelogram", "kite", "rhombus"],
         "Exactly one pair of parallel sides makes a trapezoid. Parallelograms and rhombuses have 2 pairs."),
        ("A quadrilateral has sides 5 cm, 5 cm, 9 cm and 9 cm, in order around the shape. It has no parallel sides. What is its best name?",
         "kite", ["parallelogram", "rectangle", "trapezoid"],
         "The two 5 cm sides are next to each other, and so are the two 9 cm sides. Two pairs of equal sides next to each other make a kite."),
        ("A rectangle has all 4 sides 12 cm long. What is its best name?", "square",
         ["rectangle", "rhombus", "kite"],
         "It has 4 right angles (it is a rectangle) and 4 equal sides. That makes it a square."),
        ("A rhombus has one right angle. What is its best name?", "square",
         ["rhombus", "kite", "trapezoid"],
         "Opposite angles of a rhombus are equal and angles next to each other add to 180°. "
         "One 90° angle makes all 4 angles 90°, so the rhombus is a square."),
    ]
    for q, ans, wrong, e in words:
        its.append(mcq(q, ans, wrong, e, rnd))
    assert len(its) == 20
    rnd.shuffle(its)
    return {"title": "Name the quadrilateral from its properties", "items": its}


# ------------------------------------------------------------ set 2: diagonals
ST = {
    "eq": ("They are equal in length", lambda d: d["equal"]),
    "neq": ("They are not equal in length", lambda d: not d["equal"]),
    "perp": ("They cross at right angles", lambda d: d["perp"]),
    "nperp": ("They do not cross at right angles", lambda d: not d["perp"]),
    "bis": ("They cut each other in half", lambda d: d["bisect"]),
    "nbis": ("Neither one is cut in half", lambda d: d["none"]),
    "one": ("Only one is cut in half", lambda d: d["one"]),
    "eqp": ("Equal, and cross at right angles", lambda d: d["equal"] and d["perp"]),
    "par": ("They are parallel", lambda d: False),
}


def set_diagonals(rnd):
    its = []
    pics = [
        (RECT, 0, "rectangle", "eq", ["perp", "nbis", "par"],
         "The diagonals of a rectangle are equal in length and cut each other in half. They do not cross at right angles "
         "unless the rectangle is a square."),
        (RHO, 0, "rhombus", "perp", ["eq", "nbis", "par"],
         "The diagonals of a rhombus cross at right angles and cut each other in half. They are not equal: one is long and one is short."),
        (SQ, 20, "square", "eqp", ["neq", "nbis", "nperp"],
         "A square is a rectangle (equal diagonals) and a rhombus (diagonals at right angles). Its diagonals also cut each other in half."),
        (PARA, 0, "parallelogram", "bis", ["eq", "perp", "par"],
         "In every parallelogram the diagonals cut each other in half. In this one they are not equal and do not cross at right angles."),
        (KITE1, 0, "kite", "perp", ["eq", "bis", "par"],
         "The diagonals of a kite cross at right angles. The long diagonal cuts the short one in half, but not the other way round."),
        (KITE2, 0, "kite", "one", ["bis", "nperp", "eq"],
         "The line of symmetry AC cuts the other diagonal BD in half, so BE = ED. But AE is much shorter than EC, so only one diagonal is cut in half."),
        (RHO2, 30, "rhombus", "neq", ["eq", "nperp", "nbis"],
         "The diagonals of this rhombus are different lengths. They do cross at right angles and cut each other in half. "
         "Only a square has equal diagonals among rhombuses."),
        (ISO, 0, "trapezoid", "eq", ["bis", "perp", "par"],
         "This trapezoid has 2 equal sides (the slanted sides), so its diagonals are equal in length. "
         "They do not cut each other in half and do not cross at right angles."),
    ]
    for sh, rot, name, ok, wrong, e in pics:
        svg, pts = shape_svg(sh, rot, 140, 95, ("ticks", "rights", "diags"), label=name + " with its diagonals", labels=True)
        df = diag_facts(pts)
        assert ST[ok][1](df), (name, ok)
        for w in wrong:
            assert not ST[w][1](df), (name, w)
        its.append(mcq(fig(svg) + "AC and BD are the diagonals of this %s. Which is true?" % name,
                       ST[ok][0], [ST[w][0] for w in wrong], e, rnd))
    # numbers from a labelled picture
    num = [
        (RECT, 0, "rectangle", "AC = 14 cm. How long is BD?", "14 cm", ["7 cm", "28 cm", "Cannot tell"],
         "The diagonals of a rectangle are equal, so BD = AC = 14 cm.", lambda d, p: d["equal"]),
        (PARA, 0, "parallelogram", "AE = 6 cm. How long is AC?", "12 cm", ["6 cm", "3 cm", "Cannot tell"],
         "The diagonals of a parallelogram cut each other in half, so E is the middle of AC. AC = 6 + 6 = 12 cm.",
         lambda d, p: d["bisect"]),
        (PARA2, 0, "parallelogram", "BD = 9 cm. How long is AC?", "Cannot tell", ["9 cm", "4.5 cm", "18 cm"],
         "The diagonals of a parallelogram are not always equal. Here AC is longer than BD, so knowing BD does not tell you AC.",
         lambda d, p: not d["equal"]),
        (RHO, 0, "rhombus", "What is the size of angle AEB?", "90°", ["60°", "120°", "180°"],
         "The diagonals of a rhombus cross at right angles, so angle AEB = 90°. (60° and 120° are angles of the rhombus itself.)",
         lambda d, p: d["perp"]),
        (SQ, 0, "square", "AC = 12 cm. How long is BE?", "6 cm", ["12 cm", "24 cm", "3 cm"],
         "The diagonals of a square are equal and cut each other in half. BD = 12 cm, so BE = 12 ÷ 2 = 6 cm.",
         lambda d, p: d["equal"] and d["bisect"]),
        (KITE1, 0, "kite", "BD = 10 cm. How long is BE?", "5 cm", ["10 cm", "20 cm", "Cannot tell"],
         "AC is the line of symmetry of the kite, and it cuts BD in half. BE = 10 ÷ 2 = 5 cm.",
         lambda d, p: close(dist(p[1], d["E"]), dist(d["E"], p[3]))),
    ]
    for sh, rot, name, q, ans, wrong, e, test in num:
        svg, pts = shape_svg(sh, rot, 140, 95, ("ticks", "rights", "diags"), label=name + " ABCD with diagonals", labels=True)
        assert test(diag_facts(pts), pts), q
        its.append(mcq(fig(svg) + "ABCD is a %s. Its diagonals meet at E. %s" % (name, q), ans, wrong, e, rnd))
    words = [
        ("Which quadrilateral always has diagonals that are equal, cross at right angles and cut each other in half?",
         "square", ["rectangle", "rhombus", "kite"],
         "Equal diagonals come from being a rectangle, and right angles where they cross come from being a rhombus. Only a square is both."),
        ("The diagonals of a quadrilateral are equal and cut each other in half, but they do not cross at right angles. What is it?",
         "rectangle", ["square", "rhombus", "parallelogram"],
         "Diagonals that cut each other in half make a parallelogram. Equal diagonals make it a rectangle. Not at right angles, so not a square."),
        ("The diagonals of a quadrilateral cross at right angles and cut each other in half, but they are not equal. What is it?",
         "rhombus", ["square", "rectangle", "kite"],
         "Cutting each other in half at right angles gives a rhombus. The diagonals are not equal, so it is not a square."),
        ("The diagonals of a quadrilateral cut each other in half. They are not equal and not at right angles. What is it?",
         "parallelogram", ["rectangle", "rhombus", "kite"],
         "Diagonals that cut each other in half make a parallelogram. Not equal: not a rectangle. Not at right angles: not a rhombus."),
        ("The diagonals of a quadrilateral cross at right angles, but only one of them is cut in half. What is it?",
         "kite", ["rhombus", "square", "parallelogram"],
         "In a kite, the line of symmetry cuts the other diagonal in half at a right angle, but is not cut in half itself."),
        ("Mei says the diagonals of every rhombus are equal in length. Is she right?", "No, only a square’s are",
         ["Yes, its sides are equal", "Yes, it is symmetrical", "No, they never cross"],
         "Equal sides do not mean equal diagonals. A rhombus that is not a square has one long and one short diagonal."),
    ]
    for q, ans, wrong, e in words:
        its.append(mcq(q, ans, wrong, e, rnd))
    assert len(its) == 20
    rnd.shuffle(its)
    return {"title": "Diagonals of quadrilaterals", "items": its}


# ------------------------------------------------------------ set 3: line and rotational symmetry
YES = "Yes, the halves match when folded"
NO = "No, the halves do not match"
AREA = "Yes, both halves have equal area"
TURN = "Only if the shape is turned"


def set_symmetry(rnd, spots):
    its = []
    dashed = [
        (RECT, 0, ("d", 0, 2), "rectangle",
         "Fold a rectangle along a diagonal and the corners do not land on each other. The two halves have the same area, "
         "but equal area is not enough. A rectangle has only 2 lines of symmetry, through the middles of opposite sides."),
        (PARA, 0, ("m", 0, 2), "parallelogram",
         "A parallelogram that is not a rectangle or a rhombus has no lines of symmetry. Fold it on this line and the slanted sides do not match."),
        (KITE1, 0, ("d", 0, 2), "kite",
         "The line through the top and bottom corners of a kite is its line of symmetry. Each half is the mirror image of the other."),
        (RHO, 0, ("d", 1, 3), "rhombus",
         "Each diagonal of a rhombus is a line of symmetry. Folding on it puts each side exactly on the side next to it."),
        (ISO, 0, ("m", 0, 2), "trapezoid",
         "This trapezoid has equal slanted sides, so the line through the middles of the top and bottom is a line of symmetry."),
        (KITE2, 0, ("d", 1, 3), "kite",
         "A kite has only 1 line of symmetry, the one through the top and bottom corners. Folding on the cross line puts the short sides on the long sides."),
    ]
    for sh, rot, spec, name, e in dashed:
        svg, pts = shape_svg(sh, rot, 140, 95, ("ticks", "rights"), label=name + " with a dashed line", lines=[spec])
        a, d = line_spec(pts, spec)
        ans = YES if is_sym_line(pts, a, d) else NO
        its.append(mcq(fig(svg) + "Is the dashed line a line of symmetry of this %s?" % name, ans,
                       [x for x in (YES, NO, AREA, TURN) if x != ans], e, rnd))
    count = [
        (SQ, 45, "square", ["2", "8", "0"],
         "A square has 4 lines of symmetry: 2 diagonals and 2 lines through the middles of opposite sides. Turning it does not change this."),
        (RECT, 0, "rectangle", ["4", "1", "0"],
         "A rectangle has 2 lines of symmetry, through the middles of opposite sides. Its diagonals are not lines of symmetry."),
        (PARA2, 0, "parallelogram", ["2", "4", "1"],
         "This parallelogram has no lines of symmetry. Any fold leaves the slanted corners sticking out. (It does have rotational symmetry.)"),
        (KITE1, 0, "kite", ["2", "0", "4"],
         "A kite has 1 line of symmetry, through the corners where the equal sides meet. The other diagonal is not a line of symmetry."),
        (ISO, 0, "trapezoid", ["2", "0", "4"],
         "This trapezoid has equal slanted sides, so it has 1 line of symmetry, down the middle. The top and bottom are different lengths, so there is no other."),
    ]
    for sh, rot, name, wrong, e in count:
        svg, pts = shape_svg(sh, rot, 140, 95, ("ticks", "rights"), label=name + " with marks")
        n = len(sym_lines(pts))
        its.append(mcq(fig(svg) + "How many lines of symmetry does this %s have?" % name, str(n), wrong, e, rnd))
    order = [
        (SQ, 0, "square", ["order 2", "order 1", "order 0"],
         "A square fits onto itself after a quarter turn (90°), a half turn, a three-quarter turn and a full turn: 4 times in one full turn, so order 4."),
        (PARA, 0, "parallelogram", ["order 1", "order 4", "order 0"],
         "A parallelogram fits onto itself after a half turn (180°) and after a full turn: order 2. It has rotational symmetry even with no lines of symmetry."),
        (RHO2, 30, "rhombus", ["order 4", "order 1", "order 0"],
         "A rhombus fits onto itself after a half turn and a full turn, so the order is 2. A quarter turn does not work unless it is a square."),
        (KITE2, 0, "kite", ["order 2", "order 0", "order 4"],
         "A kite only fits onto itself after a full turn, so its order of rotational symmetry is 1 (no rotational symmetry). Order 0 is not used: every shape matches after a full turn."),
    ]
    for sh, rot, name, wrong, e in order:
        svg, pts = shape_svg(sh, rot, 140, 95, ("ticks", "rights"), label=name + " with marks")
        its.append(mcq(fig(svg) + "What is the order of rotational symmetry of this %s?" % name,
                       "order %d" % rot_order(pts), wrong, e, rnd))
    # A-D: rotational symmetry but no line of symmetry
    items = [(PARA, 0), (RECT, 0), (KITE1, 0), (ISO, 0)]
    pos = spots.next()
    order_ = [1, 2, 3]
    rnd.shuffle(order_)
    cells = order_[:]
    cells.insert(pos, 0)
    cells = [items[i] for i in cells]
    for k, (sh, rot) in enumerate(cells):
        pts = placed(sh, rot, 78, 78, 0, 0)
        good = rot_order(pts) == 2 and not sym_lines(pts)
        assert good == (k == pos), (sh["kind"], k, pos)
    its.append(mcq_fixed(fig(grid_svg(cells, marks=("ticks", "rights"))) +
                         "Which shape has rotational symmetry of order 2 but no lines of symmetry?",
                         ["A", "B", "C", "D"], "ABCD"[pos],
                         "Shape %s is a parallelogram: it fits onto itself after a half turn, but no fold makes the halves match. "
                         "The rectangle has 2 lines of symmetry, and the kite and the trapezoid have 1 line but only order 1." % "ABCD"[pos]))
    words = [
        ("Which quadrilateral has 4 lines of symmetry and rotational symmetry of order 4?", "square",
         ["rectangle", "rhombus", "kite"],
         "Only a square has 4 lines of symmetry and fits onto itself after every quarter turn. A rectangle and a rhombus have 2 lines and order 2."),
        ("A quadrilateral has exactly 2 lines of symmetry, and they are its diagonals. What is it?", "rhombus",
         ["rectangle", "kite", "square"],
         "The diagonals of a rhombus are its lines of symmetry. A rectangle’s lines go through the middles of the sides, and a square has 4 lines."),
        ("What is the smallest turn that fits a rectangle (not a square) exactly onto itself?", "a half turn (180°)",
         ["a quarter turn (90°)", "a full turn (360°)", "a turn of 45°"],
         "After a quarter turn the long sides would stand up, so it does not fit. After a half turn it fits, so the order is 2."),
        ("Owen says a rectangle has 4 lines of symmetry because its diagonals are lines of symmetry too. Is he right?",
         "No, it has 2 lines", ["Yes, it has 4 lines", "No, it has 1 line", "No, it has 0 lines"],
         "Folding a rectangle on a diagonal does not make the halves match. Only the 2 lines through the middles of opposite sides work."),
    ]
    for q, ans, wrong, e in words:
        its.append(mcq(q, ans, wrong, e, rnd))
    assert len(its) == 20
    rnd.shuffle(its)
    return {"title": "Line symmetry and rotational symmetry", "items": its}


# ------------------------------------------------------------ set 4: congruent shapes
def set_congruent(rnd, spots):
    its = []
    puzzles = [
        ([(0, 0), (3, 0), (2, 2), (0, 2)], "turn90",
         [[(0, 0), (4, 0), (3, 2), (0, 2)], [(0, 0), (3, 0), (3, 2), (0, 2)], [(0, 0), (3, 0), (1, 2), (0, 2)]],
         "is shape P turned a quarter turn. Its sides and angles match P exactly. The others are a longer shape, a rectangle and a shape with a shorter top."),
        ([(0, 0), (3, 0), (3, 1), (1, 1), (1, 3), (0, 3)], "flipx",
         [[(0, 0), (3, 0), (3, 1), (1, 1), (1, 2), (0, 2)], [(0, 0), (3, 0), (3, 2), (2, 2), (2, 3), (0, 3)],
          [(0, 0), (4, 0), (4, 1), (1, 1), (1, 3), (0, 3)]],
         "is shape P flipped (a mirror image). A flipped shape is still congruent: same size, same shape. The others have an arm that is shorter, thicker or longer."),
        ([(0, 2), (2, 2), (3, 0), (1, 0)], "turn90",
         [[(0, 0), (2, 0), (2, 2), (0, 2)], [(0, 2), (3, 2), (4, 0), (1, 0)], [(0, 2), (2, 2), (4, 0), (2, 0)]],
         "is shape P turned a quarter turn. The square has the same area as P (4 square units), but equal area does not mean congruent. "
         "The other parallelograms have a longer or more slanted side."),
        ([(1, 0), (2, 1), (1, 4), (0, 1)], "turn270",
         [[(1, 0), (2, 1), (1, 3), (0, 1)], [(1, 0), (2, 2), (1, 4), (0, 2)], [(2, 0), (4, 1), (2, 4), (0, 1)]],
         "is the kite P turned a quarter turn. The others have a shorter tail, sides that are all equal, or a wider body."),
        ([(0, 1), (1, 0), (2, 1), (2, 3), (0, 3)], "turn180",
         [[(0, 1), (1, 0), (2, 1), (2, 4), (0, 4)], [(0, 2), (1, 0), (2, 2), (2, 4), (0, 4)], [(0, 1), (1, 0), (3, 1), (3, 3), (0, 3)]],
         "is shape P turned upside down (a half turn). The others are taller, have a taller roof, or are wider."),
        ([(0, 0), (2, 0), (0, 2)], "turn90",
         [[(0, 0), (4, 0), (0, 4)], [(0, 0), (3, 0), (0, 3)], [(0, 0), (2, 0), (0, 3)]],
         "is the triangle P turned a quarter turn. Its two short sides are still 2 units. The others are larger copies or have a longer side, so they are not the same size."),
    ]
    for P, tf, others, why in puzzles:
        good = g_tf(P, tf)
        assert congruent(P, good) and g_norm(good) != g_norm(P) or tf == "turn180"
        for o in others:
            assert surely_not_congruent(P, o), o
        assert len({g_canon(o) for o in others}) == 3
        pos = spots.next()
        cells = others[:]
        rnd.shuffle(cells)
        cells.insert(pos, good)
        its.append(mcq_fixed(fig(cong_grid_svg(P, cells)) + "Which shape is congruent to shape P?",
                             ["A", "B", "C", "D"], "ABCD"[pos], "Shape %s %s" % ("ABCD"[pos], why)))
    SAME = "Yes, same size and shape"
    TURNED, FLIPPED, BIG = "No, one is turned", "No, one is flipped", "No, different sizes"
    pairs = [
        ([(0, 0), (3, 0), (3, 1), (1, 2), (0, 2)], lambda p: g_tf(p, "turn90"), SAME,
         "Q is P turned a quarter turn. Turning moves a shape but does not change its size or shape, so they are congruent."),
        ([(0, 0), (3, 0), (1, 2), (0, 2)], lambda p: g_tf(p, "flipx"), SAME,
         "Q is the mirror image of P. Flipping does not change side lengths or angles, so the shapes are congruent."),
        ([(0, 0), (2, 0), (2, 1), (0, 2)], lambda p: [(2 * x, 2 * y) for x, y in p], BIG,
         "Q has the same shape as P, but every side is twice as long. Congruent shapes must be the same size too, so they are not congruent."),
    ]
    for P, make, ans, e in pairs:
        Q = make(P)
        assert congruent(P, Q) == (ans == SAME)
        its.append(mcq(fig(pair_dot_svg(P, Q)) + "Are shapes P and Q congruent?", ans,
                       [x for x in (SAME, TURNED, FLIPPED, BIG) if x != ans], e, rnd))
    lead = "Quadrilateral ABCD is congruent to quadrilateral PQRS. A matches P, B matches Q, C matches R and D matches S. "
    parts = [
        ("AB = 7 cm. How long is PQ?", "7 cm", ["14 cm", "3.5 cm", "Cannot tell"],
         "Matching sides of congruent shapes are equal. AB matches PQ, so PQ = 7 cm."),
        ("Angle B is 115°. What is angle Q?", "115°", ["65°", "245°", "90°"],
         "Matching angles of congruent shapes are equal. Angle B matches angle Q, so angle Q = 115°."),
        ("The perimeter of ABCD is 26 cm. What is the perimeter of PQRS?", "26 cm", ["13 cm", "52 cm", "Cannot tell"],
         "All 4 matching sides are equal, so the perimeters are equal: 26 cm."),
        ("CD = 6 cm. Which side of PQRS is also 6 cm?", "RS", ["QR", "PQ", "SP"],
         "C matches R and D matches S, so side CD matches side RS. RS = 6 cm."),
    ]
    for q, ans, wrong, e in parts:
        its.append(mcq(lead + q, ans, wrong, e, rnd))
    words = [
        ("Hana wants to draw a rectangle congruent to one that is 6 cm by 4 cm. Which rectangle should she draw?",
         "6 cm by 4 cm", ["12 cm by 8 cm", "5 cm by 5 cm", "8 cm by 3 cm"],
         "A congruent copy has the same side lengths and angles: 6 cm by 4 cm. 12 by 8 is an enlargement, 5 by 5 has the same perimeter "
         "and 8 by 3 has the same area, but none of them is the same size and shape."),
        ("Two rectangles both have an area of 24 cm². Are they always congruent?", "No, e.g. 6 × 4 and 8 × 3",
         ["Yes, same area", "Yes, both are rectangles", "No, rectangles never are"],
         "6 cm × 4 cm and 8 cm × 3 cm both have an area of 24 cm², but their sides are different. Same area does not mean congruent."),
        ("Two squares both have sides of 5 cm. Are they congruent?", "Yes, always",
         ["No, never", "Only if both sit flat", "Not always"],
         "Every square with 5 cm sides has the same sides (5 cm) and the same angles (90°), so they are always congruent."),
        ("Two rhombuses both have sides of 5 cm. Are they always congruent?", "No, the angles can differ",
         ["Yes, all sides match", "Yes, rhombuses are alike", "No, sides must differ"],
         "A rhombus with 5 cm sides can be a square or a thin, slanted shape. Same sides but different angles means not congruent."),
        ("Which move does NOT always give a congruent image?", "an enlargement",
         ["a translation (slide)", "a reflection (flip)", "a rotation (turn)"],
         "Slides, flips and turns move a shape without changing its size or shape. An enlargement changes the size."),
        ("Leah traces shape P on tracing paper. How can she check if shape Q is congruent to P?",
         "See if the tracing fits on Q", ["Count the vertices", "Compare their areas", "Check that both are turned"],
         "Congruent shapes fit exactly on top of each other. She may slide, turn or flip the tracing to make it fit."),
        ("Kai flips a trapezoid over to make its mirror image. Which is true?", "The image is congruent",
         ["The image is bigger", "The angles change", "It is now a kite"],
         "A reflection keeps every side length and every angle the same, so the image is congruent to the trapezoid."),
    ]
    for q, ans, wrong, e in words:
        its.append(mcq(q, ans, wrong, e, rnd))
    assert len(its) == 20
    rnd.shuffle(its)
    return {"title": "Congruent shapes", "items": its}


# ------------------------------------------------------------ set 5: always true, and word problems
def set_words(rnd):
    its = []
    always = [
        ("Every square is a rectangle", ["Every rectangle is a square", "Every rhombus is a square", "Every parallelogram is a rectangle"],
         "A rectangle only needs 4 right angles, and every square has them. The other statements are only sometimes true."),
        ("A rectangle’s diagonals are equal", ["A rhombus’s diagonals are equal", "A parallelogram’s diagonals cross at right angles",
                                               "A kite’s diagonals are equal"],
         "The diagonals of every rectangle are equal. A rhombus or a parallelogram has equal diagonals only when it is a rectangle or a square."),
        ("Every rhombus is a parallelogram", ["Every trapezoid is a parallelogram", "Every kite is a parallelogram",
                                              "Every parallelogram is a rhombus"],
         "A rhombus has 4 equal sides, and its opposite sides are parallel, so it is always a parallelogram."),
        ("A parallelogram fits onto itself after a half turn",
         ["A parallelogram has 2 lines of symmetry", "A trapezoid has a line of symmetry", "A rectangle has 4 lines of symmetry"],
         "Every parallelogram (including rectangles, rhombuses and squares) matches itself after a half turn. "
         "Most parallelograms have no lines of symmetry, and many trapezoids have none."),
        ("Congruent shapes have equal perimeters", ["Shapes with equal perimeters are congruent", "Shapes with equal areas are congruent",
                                                    "A shape and its enlargement are congruent"],
         "Congruent shapes have matching sides of equal length, so their perimeters are equal. The opposite is not true: "
         "a 5 × 5 square and a 6 × 4 rectangle have the same perimeter but are not congruent."),
        ("A square’s diagonals cross at right angles", ["A rectangle’s diagonals cross at right angles",
                                                        "A trapezoid’s diagonals cut each other in half", "A parallelogram’s diagonals are equal"],
         "A square is a rhombus, so its diagonals cross at right angles. The other statements are true only for some of those shapes."),
    ]
    for ans, wrong, e in always:
        its.append(mcq("Which statement is <b>always</b> true?", ans, wrong, e, rnd))
    world = [
        ("Liam’s dad builds a deck frame. Opposite sides are 4 m and 3 m, so it is a parallelogram. He measures both diagonals: "
         "5 m and 5 m. What does this tell him?", "The corners are right angles",
         ["All sides are equal", "It is a rhombus", "It is a trapezoid"],
         "A parallelogram with equal diagonals is a rectangle, so all 4 corners are right angles. Builders check corners this way."),
        ("Owen builds a kite for a kite festival in Ottawa. The two wooden sticks are the diagonals of the kite. "
         "At what angle do the sticks cross?", "90°", ["45°", "60°", "180°"],
         "The diagonals of a kite cross at right angles, so the sticks meet at 90°."),
        ("The short stick of Owen’s kite is 60 cm long, and the long stick crosses it at its middle. "
         "How far is the crossing point from each end of the short stick?", "30 cm", ["60 cm", "120 cm", "15 cm"],
         "The long diagonal cuts the short one in half: 60 ÷ 2 = 30 cm."),
        ("The flag of Canada is a rectangle with a red maple leaf in the middle. How many lines of symmetry does the whole flag have?",
         "1", ["2", "0", "4"],
         "The red–white–red rectangle has 2 lines of symmetry, but the maple leaf only matches when folded left to right. "
         "Folding top to bottom turns the leaf upside down, so the flag has just 1 line."),
        ("Priya sews 8 congruent rhombus patches for a quilt. Each side of one patch is 6 cm. "
         "How much ribbon does she need to go around all 8 patches?", "192 cm", ["48 cm", "24 cm", "96 cm"],
         "One patch: 4 × 6 = 24 cm. The patches are congruent, so 8 patches need 8 × 24 = 192 cm."),
        ("A square cottage window has sides of 80 cm. Two wooden bars run along its diagonals. Each bar is about 113 cm long. "
         "About how far from a corner do the bars cross?", "56.5 cm", ["113 cm", "80 cm", "40 cm"],
         "The diagonals of a square cut each other in half: 113 ÷ 2 = 56.5 cm. (40 cm is half a side, not half a diagonal.)"),
        ("Zoe paints a sign shaped like a parallelogram. One angle is 70°. What is the size of an angle next to it?", "110°",
         ["70°", "290°", "20°"],
         "Angles next to each other in a parallelogram add up to 180°: 180° − 70° = 110°. The angle opposite the 70° angle is also 70°."),
        ("Mateo makes a stained-glass design from 4 congruent kites placed around a centre point, each one a quarter turn from the next. "
         "What is the order of rotational symmetry of the design?", "4", ["1", "2", "8"],
         "Each quarter turn moves every kite onto the next one, so the design fits onto itself 4 times in a full turn: order 4."),
        ("Ava draws a quadrilateral. All 4 sides are 5 cm. Its diagonals are 6 cm and 8 cm. What is its best name?", "rhombus",
         ["square", "kite", "rectangle"],
         "4 equal sides make a rhombus. The diagonals are different lengths, so it is not a square. (Half-diagonals 3 cm and 4 cm make 5 cm sides.)"),
        ("Ethan measures a quadrilateral’s diagonals. Both are 10 cm, and they cut each other in half at right angles. What is it?",
         "square", ["rectangle", "rhombus", "kite"],
         "Equal diagonals that cut each other in half: rectangle. At right angles too: rhombus. Both: a square."),
        ("Noah’s family builds a garden bed with exactly one pair of parallel sides. The other two sides are equal. "
         "How many lines of symmetry does the garden bed have?", "1", ["0", "2", "4"],
         "A trapezoid with equal slanted sides has 1 line of symmetry, through the middles of the 2 parallel sides."),
        ("Arjun folds a sheet of letter paper (21.6 cm by 27.9 cm) along a diagonal. Do the two halves match exactly?",
         "No, corners stick out", ["Yes, halves match", "Yes, equal areas", "Yes, both are triangles"],
         "A rectangle that is not a square has no diagonal line of symmetry. The two triangles have equal area, but the corners do not line up."),
        ("Sofia covers a bulletin board with congruent parallelogram tiles. One tile has sides of 4 cm and 7 cm. "
         "What is the perimeter of each tile?", "22 cm", ["11 cm", "28 cm", "44 cm"],
         "Opposite sides of a parallelogram are equal: 4 + 7 + 4 + 7 = 22 cm. (28 is 4 × 7, not a perimeter.)"),
        ("Benjamin cuts a rectangular piece of cardboard, 30 cm by 20 cm, along one diagonal. What is true about the two pieces?",
         "They are congruent triangles", ["One is bigger", "They are squares", "They are not triangles"],
         "A diagonal cuts a rectangle into 2 triangles with sides 30 cm, 20 cm and the diagonal. A half turn puts one exactly on the other, so they are congruent."),
    ]
    for q, ans, wrong, e in world:
        its.append(mcq(q, ans, wrong, e, rnd))
    assert len(its) == 20
    rnd.shuffle(its)
    return {"title": "Always true? Quadrilateral word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    A = ("ticks", "rights", "arrows")
    family = strip_svg([(SQ, 0, "square", {}), (RECT, 0, "rectangle", {}), (RHO, 0, "rhombus", {}),
                        (PARA, 0, "parallelogram", {"marks": ("arrows",)}), (TRAPG, 0, "trapezoid", {"marks": A}),
                        (KITE1, 0, "kite", {"bw": 80, "bh": 84})],
                       "square, rectangle, rhombus, parallelogram, trapezoid and kite with marks", cols=3)
    D = ("ticks", "rights", "diags")
    diags = strip_svg([(SQ, 0, "square", {"marks": D, "diag_mark": True}), (RECT, 0, "rectangle", {"marks": D}),
                       (RHO, 0, "rhombus", {"marks": D, "diag_mark": True}), (KITE1, 0, "kite", {"marks": D, "diag_mark": True, "bw": 80, "bh": 84})],
                      "diagonals of a square, rectangle, rhombus and kite", cols=4)
    sym = strip_svg([(RECT, 0, "2 lines, order 2", {"lines": [("m", 0, 2), ("m", 1, 3)], "marks": ("rights",)}),
                     (RHO, 0, "2 lines, order 2", {"lines": [("d", 0, 2), ("d", 1, 3)], "marks": ("rights",)}),
                     (KITE1, 0, "1 line, order 1", {"lines": [("d", 0, 2)], "bw": 80, "bh": 84}),
                     (PARA, 0, "0 lines, order 2", {})],
                    "lines of symmetry of a rectangle, rhombus, kite and parallelogram", cols=4)
    # check the lesson's symmetry captions
    for sh, n, o in [(RECT, 2, 2), (RHO, 2, 2), (KITE1, 1, 1), (PARA, 0, 2), (SQ, 4, 4), (ISO, 1, 1)]:
        assert len(sym_lines(sh["pts"])) == n and rot_order(sh["pts"]) == o, sh["kind"]
    P = [(0, 0), (3, 0), (3, 1), (1, 2), (0, 2)]
    cong = pair_dot_svg(P, g_tf(P, "turn90"), label="shape P and shape Q on dot paper")
    return (
        "<h2>Name a quadrilateral by its properties</h2>"
        "<p>A quadrilateral has 4 straight sides. Its name comes from what it <b>must</b> have: equal sides, right angles "
        "and parallel sides. Tick marks show equal sides, small squares show right angles and arrows show parallel sides.</p>"
        "<figure class='sn-fig'>" + family +
        "<figcaption>Read the marks, not the look. Turning a shape never changes its name.</figcaption></figure>" +
        table(["Shape", "What it must have"], [
            ["Rectangle", "4 right angles"],
            ["Rhombus", "4 equal sides"],
            ["Square", "4 right angles <b>and</b> 4 equal sides (so it is a rectangle and a rhombus)"],
            ["Parallelogram", "2 pairs of parallel sides (opposite sides and opposite angles are equal)"],
            ["Trapezoid", "exactly 1 pair of parallel sides"],
            ["Kite", "2 pairs of equal sides that are next to each other"],
        ]) +
        "<p>Some books say a trapezoid has <i>at least</i> one pair of parallel sides. Every trapezoid in this unit has exactly one pair, "
        "so both meanings agree. Every kite in this unit is a kite that is not a rhombus.</p>" +
        ex("Example 1", "A quadrilateral has sides 5 cm, 5 cm, 9 cm and 9 cm in order, and no parallel sides. What is it?",
           "The equal sides are next to each other, not opposite. Two pairs of equal sides next to each other make a kite.", "a kite") +
        "<h2>Diagonals</h2>"
        "<p>A <b>diagonal</b> joins two corners that are not next to each other. Every quadrilateral has 2 diagonals. Ask three questions: "
        "Are they equal? Do they cut each other in half? Do they cross at right angles?</p>"
        "<figure class='sn-fig'>" + diags +
        "<figcaption>The small square where the diagonals cross shows a right angle. A rectangle’s diagonals are equal but not at right angles.</figcaption></figure>" +
        table(["Shape", "Lines of symmetry", "Rotational symmetry", "Diagonals equal?", "Cut each other in half?", "Cross at right angles?"], [
            ["Square", "4", "order 4", "Yes", "Yes", "Yes"],
            ["Rectangle", "2", "order 2", "Yes", "Yes", "No"],
            ["Rhombus", "2", "order 2", "No", "Yes", "Yes"],
            ["Parallelogram", "0", "order 2", "No", "Yes", "No"],
            ["Kite", "1", "order 1", "No", "Only one is cut in half", "Yes"],
            ["Trapezoid with equal slanted sides", "1", "order 1", "Yes", "No", "No"],
        ]) +
        "<p>The table shows shapes that are not special cases. For example, a rhombus that is also a square has equal diagonals.</p>" +
        ex("Example 2", "ABCD is a parallelogram. Its diagonals meet at E, and AE = 6 cm. How long is AC?",
           "The diagonals of a parallelogram cut each other in half, so EC = AE = 6 cm. AC = 6 + 6.", "12 cm") +
        "<h2>Line symmetry and rotational symmetry</h2>"
        "<p>A <b>line of symmetry</b> folds a shape into two halves that match exactly. The <b>order of rotational symmetry</b> is how many times "
        "a shape fits onto itself in one full turn. A shape that only fits after a full turn has order 1 (no rotational symmetry).</p>"
        "<figure class='sn-fig'>" + sym +
        "<figcaption>A rectangle’s diagonals are not lines of symmetry. A parallelogram has no lines of symmetry, but it fits onto itself after a half turn.</figcaption></figure>"
        "<h2>Congruent shapes</h2>"
        "<p>Shapes are <b>congruent</b> when they are exactly the same size and shape. One fits exactly on top of the other after a slide, "
        "a turn or a flip. Matching sides are equal and matching angles are equal.</p>"
        "<figure class='sn-fig'>" + cong +
        "<figcaption>Q is P turned a quarter turn. Every side and angle matches, so P and Q are congruent.</figcaption></figure>" +
        ex("Example 3", "Rectangle A is 6 cm by 4 cm. Rectangle B is 8 cm by 3 cm. Are they congruent?",
           "Both have an area of 24 cm², but the sides are different. Congruent shapes need matching sides.", "No") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["A square is not a rectangle", "A rectangle needs only 4 right angles. Every square is a rectangle (and a rhombus)"],
            ["The diagonals of a rhombus are equal", "They cross at right angles, but they are equal only in a square"],
            ["A rectangle’s diagonals are lines of symmetry", "Fold to check: only the lines through the middles of opposite sides work"],
            ["A parallelogram has 2 lines of symmetry", "It has none, but it has rotational symmetry of order 2"],
            ["Order 0 for no rotational symmetry", "Every shape fits after a full turn, so the smallest order is 1"],
            ["A flipped or turned shape is not congruent", "Slides, turns and flips keep size and shape the same"],
            ["Equal area or equal perimeter means congruent", "Check that every side and every angle matches"],
        ])
    )


FAQ = [
    {"q": "What do Grade 6 students learn about quadrilaterals in the Ontario math curriculum?",
     "a": "In Grade 6 Spatial Sense, students list the properties of quadrilaterals, including their diagonals, line symmetry and rotational symmetry, and they identify and construct congruent shapes."},
    {"q": "Is a square a rectangle?",
     "a": "Yes. A rectangle is any quadrilateral with 4 right angles, and every square has 4 right angles. A square is also a rhombus because its 4 sides are equal."},
    {"q": "Are the diagonals of a rhombus equal?",
     "a": "Not usually. The diagonals of a rhombus cut each other in half at right angles, but they are equal only when the rhombus is a square."},
    {"q": "What does congruent mean in Grade 6 math?",
     "a": "Congruent shapes are exactly the same size and shape, so one fits exactly on the other after a slide, turn or flip. Matching sides and matching angles are equal."},
]


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    rnd = random.Random(36815)
    spots = Spots(rnd)
    sets = [set_name(rnd), set_diagonals(rnd), set_symmetry(rnd, spots), set_congruent(rnd, spots), set_words(rnd)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-6", "slug": "quadrilaterals-and-congruence", "sort": 15,
        "updated": UPDATED, "pdf_url": "",
        "title": "Quadrilaterals and Congruence: Properties, Diagonals, Symmetry and Congruent Shapes",
        "seo_title": "Grade 6 Quadrilaterals and Congruent Shapes Worksheets: Diagonals and Symmetry (Free, Answer Key)",
        "short_title": "Quadrilaterals and Congruence",
        "domain": "Spatial Sense",
        "standard_code": "Grade 6: Spatial Sense, E1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Create and analyse designs that include translated, rotated, and reflected two-dimensional shapes; list the geometric properties of quadrilaterals, including diagonals, rotational symmetry, and line symmetry, and identify and construct congruent shapes",
        "meta_desc": "Free Grade 6 math worksheets on quadrilaterals for the Ontario curriculum: name squares, rectangles, rhombuses, parallelograms, trapezoids and kites from their properties, diagonals, line and rotational symmetry, and congruent shapes on dot paper. 100 questions with an answer key, good EQAO practice.",
        "key_big": "Name a quadrilateral by what it must have: a square is also a rectangle and a rhombus.",
        "key_sub": "Check the diagonals (equal? cut in half? at right angles?), the lines of symmetry and the order of rotational symmetry. Congruent shapes match exactly after a slide, turn or flip.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "(four shapes labelled A to D|shape P and)")
    os.makedirs(OUT, exist_ok=True)
    path_ = os.path.join(OUT, u["slug"] + ".json")
    with open(path_, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path_)
