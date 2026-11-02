# -*- coding: utf-8 -*-
"""
CA Grade 5 Math: Triangles and Congruence (Ontario Mathematics Curriculum 2020, Grade 5: Spatial Sense, E1.1 and E1.2)
  python3 tools/gen_caon_math_g5_triangles.py
Classifying triangles by their sides (equilateral, isosceles, scalene) and by their angles (acute, right, obtuse),
the angles of a triangle add to 180°, constructing triangles from side or angle measurements, and congruent
triangles, rectangles and parallelograms, with Canadian word problems.

Names used everywhere:
  equilateral  3 equal sides           isosceles  exactly 2 equal sides in every drawing and question here
  scalene      no equal sides          (an equilateral triangle is never offered next to "isosceles", so the
                                        inclusive and exclusive meanings of isosceles never clash)
  acute / right / obtuse: 3 acute angles / 1 right angle / 1 obtuse angle
Every drawing is drawn to its data and checked in code: side lengths and angles shown are the real ones,
tick marks and right-angle marks are computed from the coordinates, and every answer about a drawing is the
computed one. Congruent shapes on dot paper are made by turning or flipping the first shape in code, and
every shape that is not congruent is proved different (side lengths or area).
Wrong answers come from real student mistakes: an isosceles triangle must point up, a right triangle has
2 right angles, naming an obtuse triangle "acute" because 2 angles are acute, mixing side names and angle
names, subtracting from 360° or 90°, adding the two angles, not halving for the base angles, thinking a big
triangle has more than 180°, and thinking a flipped or turned shape (or one with equal area, perimeter or
angles) is or is not congruent.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#c9c2b8"
DOT = "#9a9a9a"
BLUE = "#2f6db5"
FS = 15


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


def num(x):
    return ("%.2f" % x).rstrip("0").rstrip(".")


# Arial Bold advance widths (per 1000 units of font size), for laying out text without a browser
AW = dict(zip("abcdefghijklmnopqrstuvwxyz", [556, 611, 556, 611, 556, 333, 611, 611, 278, 278, 556, 278, 889, 611, 611, 611,
                                              611, 389, 556, 333, 611, 556, 778, 556, 556, 500]))
AW.update(dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", [722, 722, 722, 722, 667, 611, 778, 722, 278, 556, 722, 611, 833, 722, 778, 667,
                                                  778, 722, 667, 611, 722, 667, 944, 667, 667, 611])))
AW.update({c: 556 for c in "0123456789"})
AW.update({" ": 278, ".": 278, "°": 400, "?": 611, ",": 278})


def tw(t, fs):
    """Width of bold Arial text, plus 5% for safety."""
    return sum(AW[c] for c in t) * fs / 1000.0 * 1.05


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


def groups_of(L):
    groups = []
    for i, x in enumerate(L):
        for g in groups:
            if close(L[g[0]], x):
                g.append(i)
                break
        else:
            groups.append([i])
    return groups


def tri_name(pts):
    """('acute' | 'right' | 'obtuse', 'equilateral' | 'isosceles' | 'scalene'), computed from the coordinates."""
    L, A = side_lens(pts), angles(pts)
    big = max(len(g) for g in groups_of(L))
    sides = "equilateral" if big == 3 else "isosceles" if big == 2 else "scalene"
    if any(abs(a - 90) < 1e-6 for a in A):
        ang = "right"
    elif max(A) > 90:
        ang = "obtuse"
    else:
        ang = "acute"
    return ang, sides


# ------------------------------------------------------------ triangles (y goes down, like SVG)
# Vertex 0 = left end of the base, vertex 1 = right end of the base, vertex 2 = top.
# Side 0 = base (0-1), side 1 = right side (1-2), side 2 = left side (2-0).
def tri_ang(a, b, base=120.0):
    """Triangle with angle a at vertex 0 and angle b at vertex 1."""
    c = 180 - a - b
    assert c > 0
    side = base * math.sin(math.radians(b)) / math.sin(math.radians(c))
    t = math.radians(a)
    return [(0.0, 0.0), (float(base), 0.0), (side * math.cos(t), -side * math.sin(t))]


def tri_sides(base, right, left):
    """Triangle with the given base, right side (vertex 1 to the top) and left side (vertex 0 to the top)."""
    x = (base ** 2 + left ** 2 - right ** 2) / (2.0 * base)
    y = math.sqrt(left ** 2 - x ** 2)
    return [(0.0, 0.0), (float(base), 0.0), (x, -y)]


def rot_pt(p, d):
    t = math.radians(d)
    return (p[0] * math.cos(t) - p[1] * math.sin(t), p[0] * math.sin(t) + p[1] * math.cos(t))


def placed(model, rot, bw, bh, cx, cy):
    pts = [rot_pt(p, rot) for p in model]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    k = min(bw / (max(xs) - min(xs)), bh / (max(ys) - min(ys)))
    mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    return [(cx + (p[0] - mx) * k, cy + (p[1] - my) * k) for p in pts]


def text_el(x, y, t, fs=FS, color=INK):
    """Text centred on (x, y). Returns the element and its box."""
    w = tw(t, fs)
    el = ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
          % (x, y + 0.36 * fs, fs, color, t))
    return el, (x - w / 2, y - 0.37 * fs - 1, x + w / 2, y + 0.37 * fs + 1)


def box_pts(b):
    x0, y0, x1, y1 = b
    xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
    return [(x0, y0), (x1, y0), (x0, y1), (x1, y1), (xm, y0), (xm, y1), (x0, ym), (x1, ym)]


def boxes_apart(a, b, gap=2):
    return a[2] + gap <= b[0] or b[2] + gap <= a[0] or a[3] + gap <= b[1] or b[3] + gap <= a[1]


def tri_elems(model, rot, bw, bh, cx, cy, ticks=True, side_lab=None, ang_lab=None, sw=3):
    """SVG elements for one triangle with its marks, side labels (outside) and angle labels (inside, with an arc).
    Returns elements, bounding box and the placed points."""
    pts = placed(model, rot, bw, bh, cx, cy)
    L, A = side_lens(pts), angles(pts)
    rights = [i for i, a in enumerate(A) if abs(a - 90) < 1e-6]
    for i, a in enumerate(A):
        assert i in rights or abs(a - 90) >= 10, A          # no angle that looks like a right angle but is not
    G = groups_of(L)
    for g1 in (G if ticks else []):
        for g2 in G:
            if g1 is not g2:
                a, b = L[g1[0]], L[g2[0]]
                assert abs(a - b) / max(a, b) > 0.09, L     # sides that look equal must be equal
    el, box, boxes = [], list(pts), []
    P = lambda ps: " ".join("%.1f,%.1f" % p for p in ps)
    el.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>" % (P(pts), FILL, GREEN, sw))
    mk = "stroke='%s' stroke-width='2' fill='none' stroke-linecap='round'" % INK
    segs = [(pts[i], pts[(i + 1) % 3]) for i in range(3)]
    if ticks:
        cnt = 0
        for g in G:
            if len(g) < 2:
                continue
            cnt += 1
            for i in g:
                a, b = pts[i], pts[(i + 1) % 3]
                d = norm(sub(b, a))
                nr = (-d[1], d[0])
                m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
                p1, p2 = (m[0] - nr[0] * 6, m[1] - nr[1] * 6), (m[0] + nr[0] * 6, m[1] + nr[1] * 6)
                el.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' %s/>" % (p1 + p2 + (mk,)))
                segs.append((p1, p2))
                box += [p1, p2]
    for i in rights:
        v = pts[i]
        u1, u2 = norm(sub(pts[i - 1], v)), norm(sub(pts[(i + 1) % 3], v))
        k = min(11, 0.2 * min(L[i - 1], L[i]))
        q1 = (v[0] + u1[0] * k, v[1] + u1[1] * k)
        q2 = (q1[0] + u2[0] * k, q1[1] + u2[1] * k)
        q3 = (v[0] + u2[0] * k, v[1] + u2[1] * k)
        el.append("<polyline points='%s' %s/>" % (P([q1, q2, q3]), mk.replace("stroke-width='2'", "stroke-width='1.6'")))
        segs += [(q1, q2), (q2, q3)]
    c = (sum(p[0] for p in pts) / 3, sum(p[1] for p in pts) / 3)
    if side_lab:
        for i, t in enumerate(side_lab):
            if not t:
                continue
            a, b = pts[i], pts[(i + 1) % 3]
            m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            d = norm(sub(b, a))
            nr = (-d[1], d[0])
            if (c[0] - m[0]) * nr[0] + (c[1] - m[1]) * nr[1] > 0:
                nr = (-nr[0], -nr[1])                       # point away from the triangle
            w, hh = tw(t, FS) / 2, 0.37 * FS + 1
            off = abs(nr[0]) * w + abs(nr[1]) * hh + 5
            e, bx = text_el(m[0] + nr[0] * off, m[1] + nr[1] * off, t)
            el.append(e)
            boxes.append(bx)
    if ang_lab:
        for i in sorted(range(3), key=lambda j: -A[j]):          # the widest angle has the least room: place it first
            t = ang_lab[i]
            if not t:
                continue
            assert i not in rights
            v = pts[i]
            u1, u2 = norm(sub(pts[i - 1], v)), norm(sub(pts[(i + 1) % 3], v))
            r_arc = 15
            a1, a2 = (v[0] + u1[0] * r_arc, v[1] + u1[1] * r_arc), (v[0] + u2[0] * r_arc, v[1] + u2[1] * r_arc)
            cr = u1[0] * u2[1] - u1[1] * u2[0]
            el.append("<path d='M%.1f,%.1f A%d,%d 0 0 %d %.1f,%.1f' fill='none' stroke='%s' stroke-width='1.8'/>"
                      % (a1[0], a1[1], r_arc, r_arc, 1 if cr > 0 else 0, a2[0], a2[1], RED))
            th1 = math.atan2(u1[1], u1[0])
            dth = math.atan2(cr, u1[0] * u2[0] + u1[1] * u2[1])          # signed angle from u1 to u2
            fracs = sorted([f / 20.0 for f in range(3, 18)], key=lambda f: abs(f - 0.5))
            found = None
            for r in range(18, 170):
                for f in fracs:
                    th = th1 + dth * f
                    p = (v[0] + math.cos(th) * r, v[1] + math.sin(th) * r)
                    e, bx = text_el(p[0], p[1], t, color=RED)
                    probe = box_pts(bx)
                    if not all(inside(q, pts) for q in probe):
                        continue
                    if min(seg_dist(q, s0, s1) for q in probe for s0, s1 in segs) < 3:
                        continue
                    if min(dist(q, v) for q in probe) < r_arc + 3:
                        continue
                    if not all(boxes_apart(bx, o, 4) for o in boxes):
                        continue
                    found = (e, bx)
                    break
                if found:
                    break
            assert found, ("no room for angle label", t, A)
            e, bx = found
            el.append(e)
            boxes.append(bx)
    for bx in boxes:
        box += [(bx[0], bx[1]), (bx[2], bx[3])]
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            assert boxes_apart(boxes[i], boxes[j]), (side_lab, ang_lab)
    pad = sw / 2.0 + 1
    bb = (min(p[0] for p in box) - pad, min(p[1] for p in box) - pad,
          max(p[0] for p in box) + pad, max(p[1] for p in box) + pad)
    return el, bb, pts


def tri_svg(model, rot=0, bw=130, bh=90, label="triangle", **kw):
    for grow in (1.0, 1.12, 1.25, 1.4):              # a flat triangle may need a little more room for its angle labels
        try:
            _, bb, _ = tri_elems(model, rot, bw * grow, bh * grow, 0, 0, **kw)
            break
        except AssertionError as err:
            if "no room" not in str(err) or grow == 1.4:
                raise
    bw, bh = bw * grow, bh * grow
    pad = 5
    W, H = int(math.ceil(bb[2] - bb[0] + 2 * pad)), int(math.ceil(bb[3] - bb[1] + 2 * pad))
    if W == H:
        W += 1                                       # keep figures out of the larger 'square' print size
    el, bb2, pts = tri_elems(model, rot, bw, bh, pad - bb[0] + (W - (bb[2] - bb[0] + 2 * pad)) / 2,
                             pad - bb[1] + (H - (bb[3] - bb[1] + 2 * pad)) / 2, **kw)
    assert bb2[0] >= 0 and bb2[1] >= 0 and bb2[2] <= W and bb2[3] <= H
    return svg_wrap(W, H, "".join(el), label), pts


def check_kind(model, rot, ang, sides):
    pts = placed(model, rot, 100, 100, 0, 0)
    assert tri_name(pts) == (ang, sides), (tri_name(pts), ang, sides)


CELL = 118


def grid_svg(items, label="four triangles labelled A to D"):
    """2 x 2 grid of triangles labelled A-D. items: list of (model, rot). Square picture (printed large)."""
    el = []
    W = H = 2 * CELL
    el.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, CELL, H - 4, GRAY))
    el.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, W - 4, CELL, GRAY))
    for k, (model, rot) in enumerate(items):
        x0, y0 = (k % 2) * CELL, (k // 2) * CELL
        e, bb, _ = tri_elems(model, rot, 78, 78, x0 + 67, y0 + 62, sw=2.6)
        assert bb[0] >= x0 + 20 and bb[1] >= y0 + 4 and bb[2] <= x0 + CELL - 3 and bb[3] <= y0 + CELL - 3, bb
        el += e
        el.append("<text x='%d' y='%d' font-size='18' font-weight='700' fill='%s'>%s</text>" % (x0 + 6, y0 + 22, INK, "ABCD"[k]))
    return svg_wrap(W, H, "".join(el), label)


def strip_svg(items, label, cw=140, top=118):
    """Lesson figure: a row of triangles with a caption under each. items: (model, rot, caption, options)."""
    el = []
    for k, (model, rot, cap, opt) in enumerate(items):
        e, bb, _ = tri_elems(model, rot, opt.get("bw", 100), opt.get("bh", 80), k * cw + cw / 2.0, top / 2.0, sw=2.8,
                             ticks=opt.get("ticks", True), side_lab=opt.get("side_lab"), ang_lab=opt.get("ang_lab"))
        assert bb[0] >= k * cw + 2 and bb[2] <= (k + 1) * cw - 2 and bb[1] >= 2 and bb[3] <= top - 2, (cap, bb)
        assert tw(cap, 15) <= cw - 4, cap
        el += e
        el.append("<text x='%.1f' y='%d' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                  % (k * cw + cw / 2.0, top + 16, INK, cap))
    return svg_wrap(int(cw * len(items)), top + 24, "".join(el), label)


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


# ------------------------------------------------------------ triangles used in pictures
EQUI = tri_ang(60, 60)
ISO_AC = tri_ang(70, 70)
ISO_AC2 = tri_ang(65, 65)
ISO_RT = tri_ang(45, 45)
ISO_OB = tri_ang(30, 30)
ISO_OB2 = tri_ang(25, 25)
SCA_AC = tri_ang(50, 72)
SCA_AC2 = tri_ang(40, 62)
SCA_RT = tri_ang(90, 35)
SCA_OB = tri_ang(25, 42)
SCA_OB2 = tri_ang(20, 45)

SIDE_E = {
    "equilateral": "All 3 sides are equal, so it is an equilateral triangle.",
    "isosceles": "Exactly 2 sides are equal, so it is an isosceles triangle.",
    "scalene": "No two sides are equal, so it is a scalene triangle.",
}
ANG_E = {
    "acute": "All 3 angles are less than 90°, so it is an acute triangle.",
    "right": "One angle is exactly 90°, so it is a right triangle.",
    "obtuse": "One angle is more than 90°, so it is an obtuse triangle.",
}


# ------------------------------------------------------------ set 1: classify by sides
def set_sides(rnd, spots):
    its = []
    q = "Classify this triangle by its sides. Use the tick marks."
    pics = [
        (EQUI, 180, "acute", "equilateral", ["scalene", "right", "obtuse"],
         "The tick marks show 3 equal sides. Pointing down does not change the name."),
        (ISO_AC, 0, "acute", "isosceles", ["equilateral", "scalene", "obtuse"],
         "The 2 slanted sides have tick marks, and the base has none."),
        (ISO_AC2, 180, "acute", "isosceles", ["equilateral", "scalene", "right"],
         "An isosceles triangle can point down. Turning a triangle never changes its name."),
        (ISO_OB, 90, "obtuse", "isosceles", ["scalene", "equilateral", "acute"],
         "It lies on its side, but 2 sides still have tick marks. An isosceles triangle can point in any direction."),
        (SCA_AC, 20, "acute", "scalene", ["isosceles", "equilateral", "right"],
         "There are no tick marks, so no two sides are equal."),
        (ISO_RT, 135, "right", "isosceles", ["scalene", "equilateral", "obtuse"],
         "The 2 sides next to the right angle have tick marks. Turned or not, it is isosceles."),
        (SCA_OB2, 0, "obtuse", "scalene", ["isosceles", "equilateral", "acute"],
         "There are no tick marks, so all 3 sides are different lengths."),
    ]
    for model, rot, ang, sides, wrong, extra in pics:
        check_kind(model, rot, ang, sides)
        svg, _ = tri_svg(model, rot, label=sides + " triangle with tick marks")
        its.append(mcq(fig(svg) + q, sides, wrong, SIDE_E[sides] + " " + extra, rnd))
    # side lengths written on the picture (drawn to scale)
    lens = [
        ((6, 6, 4), 0, "isosceles", ["scalene", "equilateral", "obtuse"],
         "Two sides are 6 cm, so exactly 2 sides are equal. The equal sides do not have to be the slanted ones."),
        ((9, 6, 5), 0, "scalene", ["isosceles", "equilateral", "right"],
         "The sides are 9 cm, 6 cm and 5 cm. All 3 are different."),
        ((8, 8, 8), 15, "equilateral", ["scalene", "right", "obtuse"],
         "All 3 sides are 8 cm."),
        ((5, 7.5, 7.5), 180, "isosceles", ["scalene", "equilateral", "right"],
         "Two sides are 7.5 cm. It points down, but it is still isosceles."),
        ((4, 3, 5), 0, "scalene", ["isosceles", "equilateral", "obtuse"],
         "The sides are 4 cm, 3 cm and 5 cm, all different. (It is also a right triangle, but that is a name by angles.)"),
    ]
    for (b, r, l), rot, sides, wrong, extra in lens:
        model = tri_sides(b, r, l)
        assert tri_name(model)[1] == sides
        L = side_lens(model)
        assert all(close(L[i] / L[0], [b, r, l][i] / float(b)) for i in range(3))
        svg, _ = tri_svg(model, rot, bw=120, bh=80, label=sides + " triangle with side lengths", ticks=False,
                         side_lab=[num(b) + " cm", num(r) + " cm", num(l) + " cm"])
        its.append(mcq(fig(svg) + "Classify this triangle by its sides.", sides, wrong, SIDE_E[sides] + " " + extra, rnd))
    # A-D pictures
    grids = [
        ("Which triangle is isosceles?", (ISO_AC, 200), [(SCA_AC2, 0), (SCA_RT, 0), (SCA_OB, 0)], "isosceles",
         "has tick marks on 2 sides, so it is isosceles, even though it points down. The other triangles have no equal sides."),
        ("Which triangle is scalene?", (SCA_AC, 0), [(EQUI, 0), (ISO_OB, 0), (ISO_RT, 0)], "scalene",
         "has no tick marks, so no two sides are equal. The others have 2 or 3 equal sides."),
        ("Which triangle is equilateral?", (EQUI, 90), [(ISO_AC2, 0), (ISO_OB2, 0), (SCA_RT, 0)], "equilateral",
         "has tick marks on all 3 sides. The upright triangle has only 2 equal sides, so it is isosceles."),
    ]
    for q2, good, others, sides, why in grids:
        assert tri_name(good[0])[1] == sides
        for m, _ in others:
            assert tri_name(m)[1] != sides
        p = spots.next()
        cells = others[:]
        rnd.shuffle(cells)
        cells.insert(p, good)
        its.append(mcq_fixed(fig(grid_svg(cells)) + q2, ["A", "B", "C", "D"], "ABCD"[p], "Triangle %s %s" % ("ABCD"[p], why)))
    words = [
        ("A triangle has sides of 5 cm, 5 cm and 8 cm. Classify it by its sides.", "isosceles",
         ["scalene", "equilateral", "obtuse"], "Two sides are 5 cm, so exactly 2 sides are equal: isosceles."),
        ("A triangle has sides of 4.5 cm, 6 cm and 7.5 cm. Classify it by its sides.", "scalene",
         ["isosceles", "equilateral", "acute"], "4.5 cm, 6 cm and 7.5 cm are all different, so the triangle is scalene."),
        ("An equilateral triangle has a perimeter of 36 cm. How long is each side?", "12 cm",
         ["18 cm", "9 cm", "33 cm"], "All 3 sides are equal: 36 ÷ 3 = 12 cm. (18 cm is 36 ÷ 2 and 9 cm is 36 ÷ 4.)"),
        ("An isosceles triangle has two sides of 7 cm and one side of 4 cm. What is its perimeter?", "18 cm",
         ["11 cm", "21 cm", "14 cm"], "Add all 3 sides: 7 + 7 + 4 = 18 cm. (11 cm forgets one of the 7 cm sides.)"),
        ("Owen says a triangle can only be isosceles if it points up. Is he right?", "No, it can point any way",
         ["Yes, it must point up", "Yes, or it is scalene", "No, it must point down"],
         "The name depends only on the sides. Turning an isosceles triangle does not change its 2 equal sides."),
    ]
    for q2, ans, wrong, e in words:
        its.append(mcq(q2, ans, wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Classify triangles by their sides", "items": its}


# ------------------------------------------------------------ set 2: classify by angles
def set_angles(rnd, spots):
    its = []
    q = "Classify this triangle by its angles."
    labelled = [
        ((35, 45), 0, "obtuse", ["acute", "right", "Cannot tell"],
         "100° is more than 90°. It has 2 acute angles too, but a triangle is named by its largest angle."),
        ((60, 50), 0, "acute", ["right", "obtuse", "Cannot tell"],
         "60°, 50° and 70° are all less than 90°."),
        ((90, 40), 0, "right", ["acute", "obtuse", "Cannot tell"],
         "The small square shows a 90° angle. The other two angles, 40° and 50°, are acute."),
        ((35, 35), 180, "obtuse", ["acute", "right", "Cannot tell"],
         "110° is more than 90°. Pointing down does not change the name."),
        ((75, 60), -10, "acute", ["right", "obtuse", "Cannot tell"],
         "75°, 60° and 45° are all less than 90°."),
        ((30, 90), 200, "right", ["acute", "obtuse", "Cannot tell"],
         "The small square shows a 90° angle. The triangle is turned, but it is still a right triangle."),
    ]
    for (a, b), rot, ang, wrong, extra in labelled:
        model = tri_ang(a, b)
        A = [a, b, 180 - a - b]
        assert tri_name(model)[0] == ang
        lab = [None if x == 90 else "%d°" % x for x in A]
        svg, _ = tri_svg(model, rot, bw=150, bh=100, label=ang + " triangle with angle sizes", ticks=False, ang_lab=lab)
        its.append(mcq(fig(svg) + q, ang, wrong, ANG_E[ang] + " " + extra, rnd))
    grids = [
        ("Which triangle is a right triangle?", (SCA_RT, 120), [(SCA_AC, 0), (SCA_OB, 0), (ISO_AC2, 0)], "right",
         "has a small square in one corner, so one angle is 90°. It is turned, but it is still a right triangle."),
        ("Which triangle is obtuse?", (ISO_OB, 0), [(SCA_AC2, 0), (ISO_RT, 0), (EQUI, 0)], "obtuse",
         "has one wide angle, more than 90°. The right triangle has a 90° angle, and the other two have only acute angles."),
    ]
    for q2, good, others, ang, why in grids:
        assert tri_name(good[0])[0] == ang
        for m, _ in others:
            assert tri_name(m)[0] != ang
        p = spots.next()
        cells = others[:]
        rnd.shuffle(cells)
        cells.insert(p, good)
        its.append(mcq_fixed(fig(grid_svg(cells)) + q2, ["A", "B", "C", "D"], "ABCD"[p], "Triangle %s %s" % ("ABCD"[p], why)))
    words = [
        ((90, 45, 45), "right", ["acute", "obtuse", "Cannot tell"], "One angle is exactly 90°, so it is a right triangle."),
        ((100, 40, 40), "obtuse", ["acute", "right", "Cannot tell"],
         "100° is more than 90°, so it is obtuse. Two acute angles do not make it acute: every triangle has at least 2."),
        ((60, 60, 60), "acute", ["right", "obtuse", "Cannot tell"],
         "All 3 angles are 60°, less than 90°, so it is acute. (It is also equilateral, but that is a name by sides.)"),
        ((88, 47, 45), "acute", ["right", "obtuse", "Cannot tell"],
         "88° is close to 90°, but it is still less than 90°. All 3 angles are acute."),
    ]
    for A, ang, wrong, e in words:
        assert sum(A) == 180
        k = "right" if 90 in A else "obtuse" if max(A) > 90 else "acute"
        assert k == ang
        its.append(mcq("A triangle has angles of %d°, %d° and %d°. Classify it by its angles." % A, ang, wrong, e, rnd))
    facts = [
        ("What is the greatest number of right angles a triangle can have?", "1", ["2", "3", "4"],
         "Two right angles already make 90° + 90° = 180°, and that leaves 0° for the third angle. So a triangle has at most 1 right angle."),
        ("Every triangle has at least how many acute angles?", "2", ["1", "3", "0"],
         "A triangle can have at most 1 angle that is 90° or more. So at least 2 of its 3 angles are acute."),
        ("Can a triangle have 2 obtuse angles?", "No, they add to over 180°",
         ["Yes, if it is large", "Yes, if it is isosceles", "No, only right ones"],
         "Two obtuse angles are each more than 90°, so together they are more than 180°. The 3 angles of a triangle add to only 180°."),
        ("Emma draws a right triangle. She says it has 2 right angles, at the bottom corners. Is she right?",
         "No, it has only 1",
         ["Yes, a square has 2", "Yes, one at each end", "No, it has 3"],
         "A right triangle has exactly 1 right angle. The other 2 angles are acute and add up to 90°."),
    ]
    for q2, ans, wrong, e in facts:
        its.append(mcq(q2, ans, wrong, e, rnd))
    full = [
        (ISO_RT, 45, "right isosceles", ["right scalene", "acute isosceles", "obtuse isosceles"]),
        (SCA_OB, 0, "obtuse scalene", ["obtuse isosceles", "acute scalene", "right scalene"]),
        (ISO_AC2, 180, "acute isosceles", ["acute scalene", "obtuse isosceles", "right isosceles"]),
        (ISO_OB2, 0, "obtuse isosceles", ["acute isosceles", "obtuse scalene", "right isosceles"]),
    ]
    for model, rot, name, wrong in full:
        ang, sides = name.split()
        check_kind(model, rot, ang, sides)
        svg, _ = tri_svg(model, rot, label=name + " triangle with marks")
        e = ANG_E[ang] + " " + SIDE_E[sides] + " Its full name is %s triangle." % name
        if ang == "obtuse":
            e = "One angle is wider than a right angle, so it is obtuse. " + SIDE_E[sides] + " Its full name is %s triangle." % name
        if ang == "acute":
            e = "No angle is 90° or wider, so it is acute. " + SIDE_E[sides] + " Its full name is %s triangle." % name
        its.append(mcq(fig(svg) + "Name this triangle by its angles and its sides.", name, wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Classify triangles by their angles", "items": its}


# ------------------------------------------------------------ set 3: angles add to 180°
def set_sum(rnd):
    its = []
    T = lambda x: "%d°" % x
    pics = [
        # (a, b, rot, angle labels by vertex, tick marks, answer, wrong answers, explanation)
        ((50, 60), 0, [T(50), T(60), "?"], False, 70, ["110°", "250°", "130°"],
         "The angles of a triangle add to 180°. 50° + 60° = 110°, and 180° − 110° = 70°."),
        ((35, 75), 0, [T(35), "?", T(70)], False, 75, ["105°", "255°", "145°"],
         "35° + 70° = 105°, and 180° − 105° = 75°."),
        ((90, 38), 0, [None, T(38), "?"], False, 52, ["142°", "38°", "232°"],
         "The small square is 90°. 180° − 90° − 38° = 52°. (142° forgets the right angle.)"),
        ((40, 25), 0, ["?", T(25), T(115)], False, 40, ["140°", "220°", "155°"],
         "25° + 115° = 140°, and 180° − 140° = 40°."),
        ((70, 70), 0, [T(70), None, "?"], True, 40, ["110°", "70°", "220°"],
         "The tick marks show an isosceles triangle, so the 2 bottom angles are equal: both are 70°. "
         "180° − 70° − 70° = 40°."),
        ((65, 65), 180, ["?", None, T(50)], True, 65, ["130°", "50°", "25°"],
         "The tick marks show an isosceles triangle, so the 2 angles next to the unmarked side are equal. "
         "180° − 50° = 130°, and 130° ÷ 2 = 65°."),
        ((60, 60), 0, [None, "?", None], True, 60, ["90°", "120°", "180°"],
         "The tick marks show 3 equal sides, so all 3 angles are equal: 180° ÷ 3 = 60°."),
        ((45, 105), 160, [T(45), T(105), "?"], False, 30, ["150°", "210°", "135°"],
         "45° + 105° = 150°, and 180° − 150° = 30°. Turning the triangle does not change its angles."),
    ]
    for (a, b), rot, lab, ticks, ans, wrong, e in pics:
        A = [a, b, 180 - a - b]
        model = tri_ang(a, b)
        assert A[lab.index("?")] == ans and sum(A) == 180
        for i, t in enumerate(lab):
            assert t in (None, "?") or t == T(A[i])
        if ticks:
            assert tri_name(model)[1] in ("isosceles", "equilateral")
        svg, _ = tri_svg(model, rot, bw=150, bh=100, label="triangle with a missing angle", ticks=ticks, ang_lab=lab)
        its.append(mcq(fig(svg) + "Find the size of the angle marked “?”.", T(ans), wrong, e, rnd))
    words = [
        ("Two angles of a triangle are 47° and 68°. What is the third angle?", "65°", ["115°", "245°", "133°"],
         "47° + 68° = 115°. 180° − 115° = 65°."),
        ("A right triangle has one angle of 25°. What is the third angle?", "65°", ["155°", "25°", "245°"],
         "The right angle is 90°. 180° − 90° − 25° = 65°. (155° forgets the right angle.)"),
        ("An isosceles triangle has two equal angles of 35°. What is the third angle?", "110°", ["145°", "35°", "70°"],
         "35° + 35° = 70°. 180° − 70° = 110°."),
        ("The top angle of an isosceles triangle is 40°. The other 2 angles are equal. How big is each one?", "70°",
         ["140°", "40°", "20°"], "180° − 40° = 140° is shared by 2 equal angles: 140° ÷ 2 = 70°."),
        ("Two angles of a triangle are 35° and 55°. Classify the triangle by its angles.", "right",
         ["acute", "obtuse", "Cannot tell"],
         "The third angle is 180° − 35° − 55° = 90°, so it is a right triangle. Both given angles are acute, but you must find the third one."),
        ("Two angles of a triangle are 25° and 40°. Classify the triangle by its angles.", "obtuse",
         ["acute", "right", "Cannot tell"], "The third angle is 180° − 25° − 40° = 115°, more than 90°, so it is obtuse."),
        ("Which three angles could be the angles of a triangle?", "50°, 60°, 70°",
         ["50°, 60°, 80°", "90°, 45°, 55°", "100°, 50°, 40°"],
         "50 + 60 + 70 = 180. The other sets add to 190°, so they cannot be the angles of a triangle."),
        ("Jayden draws a big triangle and a small triangle. He says the angles of the big one add to more than 180°. Is he right?",
         "No, both add to 180°", ["Yes, its angles are bigger", "Yes, they add to 360°", "No, it is less than 180°"],
         "The angles of every triangle add to 180°, big or small. A bigger triangle has longer sides, not bigger angles in total."),
        ("Can a triangle have angles of 90°, 60° and 40°?", "No, they add to 190°",
         ["Yes, it is a right triangle", "Yes, any 3 angles work", "No, it needs a 45° angle"],
         "90 + 60 + 40 = 190. The angles of a triangle must add to exactly 180°."),
        ("A right triangle has two equal angles. How big is each equal angle?", "45°", ["90°", "60°", "30°"],
         "The right angle is 90°, so the other two add to 180° − 90° = 90°. 90° ÷ 2 = 45°."),
        ("Mei measures two angles of a triangle: 95° and 85°. Is this possible?", "No, nothing is left",
         ["Yes, 95° is obtuse", "Yes, any sizes work", "No, 95° is too small"],
         "95° + 85° = 180°, which leaves 0° for the third angle. A triangle needs 3 angles, so this is not possible."),
        ("The two acute angles of a right triangle add up to what?", "90°", ["180°", "270°", "45°"],
         "All 3 angles add to 180°, and the right angle uses 90°. 180° − 90° = 90° is left for the other two."),
    ]
    for q2, ans, wrong, e in words:
        its.append(mcq(q2, ans, wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "The angles of a triangle add to 180°", "items": its}


# ------------------------------------------------------------ set 4: congruent shapes
def set_congruent(rnd, spots):
    its = []
    puzzles = [
        ([(0, 0), (3, 0), (0, 2)], "turn90",
         [[(0, 0), (3, 0), (0, 3)], [(0, 0), (4, 0), (0, 2)], [(0, 0), (2, 0), (0, 2)]],
         "is triangle P turned a quarter turn. Its sides are still 3 units and 2 units. The others have a side that is longer or shorter."),
        ([(0, 0), (3, 0), (3, 2), (0, 2)], "turn90",
         [[(0, 0), (3, 0), (3, 3), (0, 3)], [(0, 0), (4, 0), (4, 1), (0, 1)], [(0, 2), (3, 2), (4, 0), (1, 0)]],
         "is the 3 by 2 rectangle P turned a quarter turn. The 4 by 1 rectangle has the same perimeter and the slanted shape has the same area, "
         "but neither is the same size and shape."),
        ([(0, 2), (2, 2), (3, 0), (1, 0)], "flipx",
         [[(0, 0), (2, 0), (2, 2), (0, 2)], [(0, 2), (3, 2), (4, 0), (1, 0)], [(0, 2), (2, 2), (4, 0), (2, 0)]],
         "is parallelogram P flipped (a mirror image). A flipped shape is still congruent. The square has the same area, "
         "and the other parallelograms have a longer or more slanted side."),
        ([(0, 0), (3, 0), (4, 2)], "turn180",
         [[(0, 0), (3, 0), (3, 2)], [(0, 0), (3, 0), (1, 2)], [(0, 0), (2, 0), (4, 2)]],
         "is triangle P turned upside down (a half turn). One other triangle has the same area, but its sides are different."),
        ([(0, 2), (4, 2), (2, 0)], "turn90",
         [[(0, 2), (4, 2), (2, 1)], [(0, 3), (4, 3), (2, 0)], [(0, 2), (3, 2), (1, 0)]],
         "is the isosceles triangle P turned on its side. It points sideways, but it is the same size and shape. "
         "The others are flatter, taller or scalene."),
    ]
    for P, tf, others, why in puzzles:
        good = g_tf(P, tf)
        assert congruent(P, good)
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
        ([(0, 0), (3, 0), (1, 2)], lambda p: g_tf(p, "turn90"), SAME,
         "Q is P turned a quarter turn. Turning moves a shape but does not change its size or shape, so they are congruent."),
        ([(0, 0), (3, 0), (4, 2), (1, 2)], lambda p: g_tf(p, "flipx"), SAME,
         "Q is the mirror image of P. Flipping does not change side lengths or angles, so the shapes are congruent."),
        ([(0, 0), (2, 0), (0, 1)], lambda p: [(2 * x, 2 * y) for x, y in p], BIG,
         "Q has the same shape as P, but every side is twice as long. Congruent shapes must be the same size too."),
    ]
    for P, make, ans, e in pairs:
        Q = make(P)
        assert congruent(P, Q) == (ans == SAME)
        its.append(mcq(fig(pair_dot_svg(P, Q)) + "Are shapes P and Q congruent?", ans,
                       [x for x in (SAME, TURNED, FLIPPED, BIG) if x != ans], e, rnd))
    lead = "Triangle ABC is congruent to triangle DEF. A matches D, B matches E and C matches F. "
    parts = [
        ("AB = 6 cm. How long is DE?", "6 cm", ["12 cm", "3 cm", "Cannot tell"],
         "Matching sides of congruent shapes are equal. AB matches DE, so DE = 6 cm."),
        ("Angle C is 50°. What is angle F?", "50°", ["130°", "40°", "Cannot tell"],
         "Matching angles of congruent shapes are equal. Angle C matches angle F, so angle F = 50°."),
        ("The perimeter of triangle ABC is 21 cm. What is the perimeter of triangle DEF?", "21 cm",
         ["42 cm", "7 cm", "Cannot tell"], "All 3 matching sides are equal, so the perimeters are equal: 21 cm."),
        ("BC = 8 cm. Which side of triangle DEF is also 8 cm?", "EF", ["DE", "DF", "None of them"],
         "B matches E and C matches F, so side BC matches side EF."),
    ]
    for q, ans, wrong, e in parts:
        its.append(mcq(lead + q, ans, wrong, e, rnd))
    words = [
        ("Hana wants to draw a rectangle congruent to one that is 7 cm by 3 cm. Which rectangle should she draw?",
         "7 cm by 3 cm", ["14 cm by 6 cm", "5 cm by 5 cm", "21 cm by 1 cm"],
         "A congruent copy has the same side lengths and angles: 7 cm by 3 cm. 14 by 6 is twice as big, 5 by 5 has the same perimeter "
         "and 21 by 1 has the same area, but none of them is the same size and shape."),
        ("Two triangles both have angles of 50°, 60° and 70°. Are they always congruent?", "No, sizes can differ",
         ["Yes, angles match", "Yes, all triangles are", "No, angles must differ"],
         "Triangles with the same angles have the same shape, but one can be bigger. Congruent shapes need equal sides too."),
        ("Two equilateral triangles both have sides of 4 cm. Are they congruent?", "Yes, always",
         ["No, never", "Only if both point up", "Not always"],
         "Both have three 4 cm sides and three 60° angles, so they are the same size and shape, whichever way they point."),
        ("Two parallelograms both have sides of 5 cm and 3 cm. Are they always congruent?", "No, angles can differ",
         ["Yes, all sides match", "Yes, they are alike", "No, sides must differ"],
         "A parallelogram with 5 cm and 3 cm sides can be a rectangle or a slanted shape. Same sides but different angles means not congruent."),
        ("Two rectangles both have an area of 24 cm². Are they always congruent?", "No, e.g. 6 × 4 and 8 × 3",
         ["Yes, same area", "Yes, both are rectangles", "No, rectangles never are"],
         "6 cm × 4 cm and 8 cm × 3 cm both have an area of 24 cm², but their sides are different. Same area does not mean congruent."),
        ("Leah traces triangle P on tracing paper. How can she check if triangle Q is congruent to P?",
         "See if the tracing fits on Q", ["Count the corners", "Compare their areas", "Check that both point up"],
         "Congruent shapes fit exactly on top of each other. She may slide, turn or flip the tracing to make it fit."),
        ("Kai flips a triangle over to make its mirror image. Which is true?", "The image is congruent",
         ["The image is bigger", "The angles change", "It is a new kind"],
         "A flip keeps every side length and every angle the same, so the image is congruent to the triangle."),
        ("Maya cuts out two congruent parallelograms. One has angles of 65° and 115°. What angles does the other have?",
         "65° and 115°", ["25° and 155°", "90° and 90°", "115° and 245°"],
         "Matching angles of congruent shapes are equal, so the other parallelogram also has angles of 65° and 115°."),
    ]
    for q, ans, wrong, e in words:
        its.append(mcq(q, ans, wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Congruent triangles, rectangles and parallelograms", "items": its}


# ------------------------------------------------------------ set 5: word problems and constructions
def set_words(rnd):
    its = []
    world = [
        ("A yield sign is an equilateral triangle that points down. One yield sign has sides of 75 cm. What is its perimeter?",
         "225 cm", ["150 cm", "75 cm", "300 cm"], "All 3 sides are 75 cm: 3 × 75 = 225 cm."),
        ("A yield sign is an equilateral triangle. What is the size of each of its angles?", "60°", ["90°", "45°", "180°"],
         "The 3 angles are equal and add to 180°: 180° ÷ 3 = 60°."),
        ("Liam’s hockey team makes a pennant shaped like an isosceles triangle. The pointed end has a 30° angle. "
         "The other 2 angles are equal. How big is each one?", "75°", ["150°", "30°", "60°"],
         "180° − 30° = 150°, shared by 2 equal angles: 150° ÷ 2 = 75°."),
        ("The roof of a cottage makes an isosceles triangle. The two bottom angles are 35° each. "
         "What is the angle at the top?", "110°", ["145°", "35°", "55°"],
         "35° + 35° = 70°. 180° − 70° = 110°. That angle is more than 90°, so the roof triangle is obtuse."),
        ("A ladder leans against a wall. The wall meets the ground at a right angle, and the ladder makes a 70° angle with the ground. "
         "What angle does the ladder make with the wall?", "20°", ["110°", "70°", "290°"],
         "The ladder, wall and ground make a right triangle. 180° − 90° − 70° = 20°."),
        ("A ramp at the school entrance makes a right triangle with the ground. The ramp makes a 5° angle with the ground. "
         "What is the third angle?", "85°", ["175°", "95°", "5°"], "180° − 90° − 5° = 85°."),
        ("Emma cuts a square Nanaimo bar from corner to corner. What kind of triangles does she get?", "right isosceles",
         ["acute isosceles", "right scalene", "obtuse scalene"],
         "Each piece has a square corner (90°) and 2 equal sides (two sides of the square), so it is a right isosceles triangle."),
        ("Owen cuts a rectangular sandwich, 12 cm by 8 cm, from corner to corner. Are the two pieces congruent?",
         "Yes, they match exactly", ["No, one is bigger", "No, they are not triangles", "Only if it is square"],
         "Each piece is a right triangle with sides 12 cm and 8 cm and the cut. A half turn puts one exactly on the other."),
        ("Maya has straws that are 3 cm, 4 cm and 9 cm long. Can she join their ends to make a triangle?",
         "No, 3 + 4 is less than 9", ["Yes, any 3 straws work", "Yes, a scalene one", "No, it needs equal sides"],
         "The two short straws together are only 7 cm. They cannot reach across the 9 cm straw, so no triangle is made."),
        ("Noah joins three 5 cm straws to make a triangle. What kind of triangle does he make?", "equilateral",
         ["obtuse", "scalene", "right"], "All 3 sides are 5 cm, so the triangle is equilateral (and each angle is 60°)."),
        ("Kai draws a 6 cm line. At each end he draws a 60° angle, and the two new lines meet. What kind of triangle is it?",
         "equilateral", ["right", "scalene", "obtuse"],
         "The third angle is 180° − 60° − 60° = 60°. All 3 angles are equal, so all 3 sides are equal (6 cm each)."),
        ("Zoe draws an 8 cm line. She draws a 90° angle at one end and a 45° angle at the other. What is the third angle?",
         "45°", ["90°", "135°", "225°"],
         "180° − 90° − 45° = 45°. Two equal angles mean two equal sides, so Zoe drew a right isosceles triangle."),
        ("The front of a tent is an isosceles triangle with sides of 1.5 m, 1.5 m and 2 m. What is its perimeter?", "5 m",
         ["3.5 m", "4.5 m", "6 m"], "1.5 + 1.5 + 2 = 5 m. (3.5 m forgets one of the 1.5 m sides.)"),
        ("Priya sews 12 congruent triangle patches for a quilt. Each patch has sides of 6 cm, 8 cm and 10 cm. "
         "How much trim does she need to go around all 12 patches?", "288 cm", ["24 cm", "120 cm", "240 cm"],
         "One patch: 6 + 8 + 10 = 24 cm. The patches are congruent, so 12 × 24 = 288 cm."),
        ("On a map, Toronto, Ottawa and Montréal make a triangle. Its sides are about 350 km, 170 km and 500 km. "
         "Classify it by its sides.", "scalene", ["isosceles", "equilateral", "right"],
         "350 km, 170 km and 500 km are all different, so the triangle is scalene."),
        ("A bike frame has a triangle with angles of 60° and 70°. What is the third angle?", "50°",
         ["130°", "230°", "120°"], "60° + 70° = 130°. 180° − 130° = 50°."),
        ("Students make triangle flags for the Terry Fox Run. Each flag has angles of 40°, 70° and 70°. "
         "What is the full name of the triangle?", "acute isosceles", ["obtuse isosceles", "acute scalene", "right isosceles"],
         "All angles are less than 90° (acute), and 2 equal angles mean 2 equal sides (isosceles)."),
        ("Mateo cuts two congruent triangle shelves for his bedroom. One shelf has angles of 90°, 30° and 60°. "
         "What are the angles of the other shelf?", "90°, 30° and 60°", ["90°, 45° and 45°", "60°, 60° and 60°", "90°, 60° and 60°"],
         "Congruent shapes have matching angles that are equal, so the second shelf has the same angles."),
        ("Ava says a triangle can have one right angle and one obtuse angle. Is she right?", "No, that is over 180°",
         ["Yes, if it is big", "Yes, if it is scalene", "Yes, if it is isosceles"],
         "90° plus an angle bigger than 90° is already more than 180°, but all 3 angles must add to 180°."),
        ("Ethan draws a triangle with sides of 7 cm, 7 cm and 7 cm, and Sofia draws one with sides of 7 cm, 7 cm and 4 cm. "
         "Are the triangles congruent?", "No, one side differs", ["Yes, two sides match", "Yes, both have 7 cm", "Only if turned"],
         "Congruent triangles need all 3 matching sides equal. 7 cm and 4 cm are different, so the triangles are not congruent."),
    ]
    for q, ans, wrong, e in world:
        its.append(mcq(q, ans, wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Triangle word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    sides = strip_svg([(EQUI, 0, "equilateral", {}), (ISO_AC, 180, "isosceles", {}), (ISO_OB, 90, "isosceles", {"bw": 70, "bh": 90}),
                       (SCA_AC2, 0, "scalene", {})], "equilateral, isosceles and scalene triangles with tick marks")
    angs = strip_svg([(tri_ang(70, 50), 0, "acute", {"ticks": False, "bw": 112, "bh": 86, "ang_lab": ["70°", "50°", "60°"]}),
                      (tri_ang(90, 35), 0, "right", {"ticks": False, "bw": 112, "bh": 86, "ang_lab": [None, "35°", "55°"]}),
                      (tri_ang(30, 40), 0, "obtuse", {"ticks": False, "bw": 160, "bh": 80, "ang_lab": ["30°", "40°", "110°"]})],
                     "acute, right and obtuse triangles with their angles", cw=172, top=112)
    for m, a in [(tri_ang(70, 50), "acute"), (tri_ang(90, 35), "right"), (tri_ang(30, 40), "obtuse")]:
        assert tri_name(m)[0] == a
    summ, _ = tri_svg(tri_ang(50, 60), 0, bw=150, bh=100, label="triangle with angles 50°, 60° and a missing angle",
                      ticks=False, ang_lab=["50°", "60°", "?"])
    P = [(0, 0), (3, 0), (1, 2)]
    cong = pair_dot_svg(P, g_tf(P, "flipx"), label="triangle P and its mirror image Q on dot paper")
    assert congruent(P, g_tf(P, "flipx"))
    return (
        "<h2>Name a triangle by its sides</h2>"
        "<p>Look at the sides. Tick marks show sides that are equal.</p>" +
        table(["Name", "Sides"], [
            ["Equilateral", "all 3 sides equal"],
            ["Isosceles", "2 sides equal"],
            ["Scalene", "no sides equal"],
        ]) +
        "<figure class='sn-fig'>" + sides +
        "<figcaption>An isosceles triangle can point up, down or sideways. Turning a triangle never changes its name.</figcaption></figure>"
        "<h2>Name a triangle by its angles</h2>"
        "<p>Look at the largest angle. A right angle is exactly 90°. A small square marks it.</p>" +
        table(["Name", "Angles"], [
            ["Acute", "all 3 angles less than 90°"],
            ["Right", "one angle exactly 90°"],
            ["Obtuse", "one angle more than 90°"],
        ]) +
        "<figure class='sn-fig'>" + angs +
        "<figcaption>Every triangle has at least 2 acute angles. Name it by its largest angle.</figcaption></figure>" +
        "<p>A triangle can have both names. A triangle with a right angle and 2 equal sides is a <b>right isosceles</b> triangle.</p>" +
        ex("Example 1", "A triangle has sides of 6 cm, 6 cm and 4 cm, and angles of 70°, 70° and 40°. Name it.",
           "Two sides are equal: isosceles. All angles are less than 90°: acute.", "an acute isosceles triangle") +
        "<h2>The angles add to 180°</h2>"
        "<p>The 3 angles of every triangle add to 180°, big or small. To find a missing angle, add the two you know and subtract from 180°.</p>"
        "<figure class='sn-fig'>" + summ +
        "<figcaption>50° + 60° = 110°, and 180° − 110° = 70°.</figcaption></figure>" +
        ex("Example 2", "An isosceles triangle has a top angle of 40°. The other 2 angles are equal. How big is each one?",
           "180° − 40° = 140°. The 2 equal angles share it: 140° ÷ 2 = 70°.", "70°") +
        "<p><b>Construct a triangle.</b> Draw one side with a ruler. Use a protractor to draw the angle at each end. "
        "The two new lines meet at the third corner. A 6 cm side with 60° at both ends makes an equilateral triangle.</p>"
        "<h2>Congruent shapes</h2>"
        "<p>Shapes are <b>congruent</b> when they are exactly the same size and shape. One fits exactly on top of the other after a slide, "
        "a turn or a flip. Matching sides are equal and matching angles are equal. This works for triangles, rectangles and parallelograms.</p>"
        "<figure class='sn-fig'>" + cong +
        "<figcaption>Q is P flipped over. Every side and angle matches, so P and Q are congruent.</figcaption></figure>" +
        ex("Example 3", "Rectangle A is 6 cm by 4 cm. Rectangle B is 8 cm by 3 cm. Are they congruent?",
           "Both have an area of 24 cm², but the sides are different. Congruent shapes need matching sides.", "No") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["An isosceles triangle must point up", "Count the equal sides. It can point any way"],
            ["A right triangle has 2 right angles", "It has exactly 1. The other 2 angles are acute"],
            ["A triangle with 2 acute angles is acute", "Every triangle has 2 acute angles. Look at the largest one"],
            ["Subtracting from 360° or 90°", "The angles of a triangle add to 180°"],
            ["Forgetting to halve for 2 equal angles", "Subtract the top angle from 180°, then divide by 2"],
            ["A flipped or turned shape is not congruent", "Slides, turns and flips keep the size and shape"],
            ["Same area, perimeter or angles means congruent", "Check that every side and every angle matches"],
        ])
    )


FAQ = [
    {"q": "What do Grade 5 students learn about triangles in the Ontario math curriculum?",
     "a": "In Grade 5 Spatial Sense, students identify the properties of triangles, classify them by sides and by angles, and construct triangles from side or angle measurements (E1.1). They also identify congruent triangles, rectangles and parallelograms (E1.2)."},
    {"q": "Do the angles of a triangle always add up to 180°?",
     "a": "Yes. In every triangle the 3 angles add to 180°, no matter how big it is. To find a missing angle, add the two known angles and subtract from 180°."},
    {"q": "Can a triangle have two right angles?",
     "a": "No. Two right angles already make 180°, so nothing is left for the third angle. A right triangle has exactly 1 right angle and 2 acute angles."},
    {"q": "What does congruent mean in Grade 5 math?",
     "a": "Congruent shapes are exactly the same size and shape, so one fits on the other after a slide, turn or flip. Matching sides and matching angles are equal."},
]


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    rnd = random.Random(45815)
    spots = Spots(rnd)
    sets = [set_sides(rnd, spots), set_angles(rnd, spots), set_sum(rnd), set_congruent(rnd, spots), set_words(rnd)]
    for s in sets:
        rnd.shuffle(s["items"])
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
        "country": "ca-on", "subject": "math", "grade": "grade-5", "slug": "triangles-and-congruence", "sort": 15,
        "updated": UPDATED, "pdf_url": "",
        "title": "Triangles and Congruence: Classify by Sides and Angles, Angle Sum and Congruent Shapes",
        "seo_title": "Grade 5 Triangles Worksheets: Classify Triangles, Angles Add to 180° and Congruent Shapes (Free, Answer Key)",
        "short_title": "Triangles and Congruence",
        "domain": "Spatial Sense",
        "standard_code": "Grade 5: E1.1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Identify geometric properties of triangles, and construct different types of triangles when given side or angle measurements",
        "meta_desc": "Free Grade 5 math worksheets on triangles for the Ontario curriculum: classify triangles as equilateral, isosceles or scalene and as acute, right or obtuse, find a missing angle using the 180° rule, construct triangles and spot congruent triangles, rectangles and parallelograms. 100 questions with an answer key.",
        "key_big": "Name a triangle by its sides and by its largest angle. Its 3 angles always add to 180°.",
        "key_sub": "Equilateral, isosceles, scalene: count the equal sides. Acute, right, obtuse: look at the largest angle. Congruent shapes match exactly after a slide, turn or flip.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "(four triangles labelled A to D|shape P and)")
    os.makedirs(OUT, exist_ok=True)
    path_ = os.path.join(OUT, u["slug"] + ".json")
    with open(path_, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path_)
