# -*- coding: utf-8 -*-
"""
BC Grade 6 Math: Triangles (BC Mathematics Curriculum, Grade 6: Geometry and measurement, "triangles")
  python3 tools/gen_cabc_math_g6_triangles.py
Classifying triangles by their sides (equilateral, isosceles, scalene) and by their angles (acute, right, obtuse),
the angles of a triangle add to 180°, finding missing angles (isosceles, right, decimals, ratios, one-step
equations), and British Columbia word problems.

Names used everywhere:
  equilateral  3 equal sides           isosceles  exactly 2 equal sides in every drawing and question here
  scalene      no equal sides          (an equilateral triangle is never offered next to "isosceles")
  acute / right / obtuse: 3 acute angles / 1 right angle / 1 obtuse angle
Every drawing is drawn to its data and checked in code: side lengths and angles shown are the real ones,
tick marks and right-angle marks are computed from the coordinates, and every answer about a drawing is the
computed one.
Wrong answers come from real student mistakes: a right triangle has 2 right angles, an isosceles triangle must
point up, naming an obtuse triangle "acute" because 2 angles are acute, subtracting from 360° or 90°,
subtracting only one known angle, forgetting the right angle, not halving for the base angles, using one
ratio part as the answer, and thinking a big triangle has more than 180°.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-6")
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



# ------------------------------------------------------------ set 3: the angles add to 180°
def set_sum(rnd):
    its = []
    its.append(mcq("The 3 angles of any triangle add up to what?", "180°", ["360°", "90°", "270°"],
                   "The angles of every triangle add to 180°. (360° is the total for a square or any four-sided shape.)", rnd))
    pick = [
        ("Which three angles could be the angles of a triangle?", (50, 60, 70), [(50, 60, 80), (90, 45, 55), (100, 50, 40)]),
        ("Which set of angles can make a triangle?", (30, 60, 90), [(30, 60, 100), (45, 45, 45), (120, 30, 40)]),
        ("Which three angles could be the angles of a right triangle?", (25, 65, 90), [(25, 75, 90), (30, 50, 90), (45, 45, 100)]),
        ("Which three angles could be the angles of an isosceles triangle?", (110, 35, 35), [(110, 40, 40), (100, 35, 35), (70, 70, 50)]),
    ]
    for q, good, bad in pick:
        assert sum(good) == 180
        for b in bad:
            assert sum(b) != 180
        f = lambda t: "%d°, %d°, %d°" % t
        wrong = ", ".join("%s adds to %d°" % (f(b), sum(b)) for b in bad)
        its.append(mcq(q, f(good), [f(b) for b in bad],
                       "%d + %d + %d = 180, so these angles work. The others do not add to 180°: %s." % (good + (wrong,)), rnd))
    two = [((35, 55), "right"), ((25, 40), "obtuse"), ((50, 60), "acute"), ((44, 46), "right"), ((65, 70), "acute")]
    for (a, b), ang in two:
        c = 180 - a - b
        k = "right" if c == 90 else "obtuse" if c > 90 else "acute"
        assert k == ang and max(a, b) < 90
        why = {"right": "%d° is a right angle, so it is a right triangle." % c,
               "obtuse": "%d° is more than 90°, so it is obtuse." % c,
               "acute": "All 3 angles (%d°, %d° and %d°) are less than 90°, so it is acute." % (a, b, c)}[ang]
        e = "First find the third angle: 180° − %d° − %d° = %d°. %s" % (a, b, c, why)
        if ang != "acute":
            e += " Both given angles are acute, but the third one decides."
        its.append(mcq("Two angles of a triangle are %d° and %d°. Classify the triangle by its angles." % (a, b),
                       ang, [x for x in ("acute", "right", "obtuse", "Cannot tell") if x != ang], e, rnd))
    facts = [
        ("One angle of a triangle is 120°. What are the other two angles like?", "Both are acute",
         ["One is right", "One is obtuse", "Both are obtuse"],
         "180° − 120° = 60° is left for the other two angles. Each one is less than 60°, so both are acute."),
        ("Two angles of a triangle add to less than 90°. What kind of triangle is it?", "obtuse",
         ["acute", "right", "Cannot tell"],
         "The third angle is 180° minus a number less than 90°, so it is more than 90°. The triangle is obtuse."),
        ("Two angles of a triangle add to 90°. What is the third angle?", "90°", ["270°", "180°", "45°"],
         "180° − 90° = 90°. The third angle is a right angle."),
        ("Ryan draws a big triangle and a small triangle. He says the angles of the big one add to more than 180°. Is he right?",
         "No, both add to 180°", ["Yes, its angles are bigger", "Yes, they add to 360°", "No, it is less than 180°"],
         "The angles of every triangle add to 180°, big or small. A bigger triangle has longer sides, not bigger angles in total."),
        ("Mei measures two angles of a triangle: 95° and 85°. Is this possible?", "No, nothing is left",
         ["Yes, 95° is obtuse", "Yes, any sizes work", "No, 95° is too small"],
         "95° + 85° = 180°, which leaves 0° for the third angle. A triangle needs 3 angles, so this is not possible."),
        ("The two acute angles of a right triangle add up to what?", "90°", ["180°", "270°", "45°"],
         "All 3 angles add to 180°, and the right angle uses 90°. 180° − 90° = 90° is left for the other two."),
        ("What is the size of each angle in an equilateral triangle?", "60°", ["90°", "120°", "180°"],
         "The 3 angles are equal and add to 180°: 180° ÷ 3 = 60°. (120° comes from dividing 360° by 3.)"),
        ("One angle of a triangle is 100°. What do the other two angles add up to?", "80°", ["260°", "100°", "40°"],
         "180° − 100° = 80°. (260° subtracts from 360°, and 40° is half of 80°: that is only one angle if they are equal.)"),
        ("Ji-woo measures the angles of a triangle as 62°, 58° and 70°. What can you say?", "A measurement is off",
         ["They are all correct", "It is a right triangle", "It is an obtuse triangle"],
         "62 + 58 + 70 = 190. The angles of a triangle must add to exactly 180°, so at least one measurement is wrong."),
        ("Chloe tears off the 3 corners of a paper triangle and puts them together, point to point. What do they make?",
         "A straight angle, 180°", ["A right angle, 90°", "A full turn, 360°", "An acute angle"],
         "The 3 angles of a triangle add to 180°, so the corners fit together to make a straight line."),
    ]
    for q, ans, wrong, e in facts:
        its.append(mcq(q, ans, wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "The angles of a triangle add to 180°", "items": its}


# ------------------------------------------------------------ set 4: find the missing angle
def set_missing(rnd):
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
        ((62, 70), 0, ["?", T(70), T(48)], False, 62, ["118°", "242°", "132°"],
         "70° + 48° = 118°, and 180° − 118° = 62°. (132° subtracts only the 48° angle.)"),
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
         "47° + 68° = 115°. 180° − 115° = 65°. (133° subtracts only the 47° angle.)"),
        ("A right triangle has one angle of 25°. What is the third angle?", "65°", ["155°", "25°", "245°"],
         "The right angle is 90°. 180° − 90° − 25° = 65°. (155° forgets the right angle.)"),
        ("An isosceles triangle has two equal angles of 35°. What is the third angle?", "110°", ["145°", "35°", "70°"],
         "35° + 35° = 70°. 180° − 70° = 110°. (145° uses only one of the 35° angles.)"),
        ("The top angle of an isosceles triangle is 40°. The other 2 angles are equal. How big is each one?", "70°",
         ["140°", "40°", "20°"], "180° − 40° = 140° is shared by 2 equal angles: 140° ÷ 2 = 70°. (140° forgets to halve.)"),
        ("A right triangle has two equal angles. How big is each equal angle?", "45°", ["90°", "60°", "30°"],
         "The right angle is 90°, so the other two add to 180° − 90° = 90°. 90° ÷ 2 = 45°."),
        ("An obtuse isosceles triangle has a 120° angle. The other 2 angles are equal. How big is each one?", "30°",
         ["60°", "120°", "45°"],
         "180° − 120° = 60°, shared by 2 equal angles: 60° ÷ 2 = 30°. (60° forgets to halve; 120° subtracts from 360°.)"),
        ("Two angles of a triangle are 52.5° and 74.5°. What is the third angle?", "53°", ["127°", "63°", "233°"],
         "52.5° + 74.5° = 127°. 180° − 127° = 53°. (63° is a subtraction slip, and 127° is the sum, not the answer.)"),
        ("An isosceles triangle has two equal angles of 72.5°. What is the third angle?", "35°", ["107.5°", "72.5°", "145°"],
         "72.5° + 72.5° = 145°. 180° − 145° = 35°. (107.5° subtracts only one of the equal angles.)"),
        ("Nadia writes the equation a + 115 = 180 to find a missing angle a. What is a?", "65°", ["295°", "115°", "75°"],
         "Subtract to undo the addition: a = 180 − 115 = 65. So a = 65°. (295° adds instead of subtracting.)"),
        ("In triangle PQR, angle P is 38°. Angle Q is 2 times angle P. What is angle R?", "66°", ["142°", "104°", "76°"],
         "Angle Q = 2 × 38° = 76°. Angle R = 180° − 38° − 76° = 66°. (76° is angle Q, not angle R.)"),
        ("A right triangle has two acute angles. One is 2 times the other. What are the two acute angles?",
         "30° and 60°", ["45° and 45°", "60° and 120°", "30° and 90°"],
         "The acute angles add to 90°. Split 90° into 3 equal parts: 90° ÷ 3 = 30°. So the angles are 30° and 2 × 30° = 60°."),
        ("The angles of a triangle are in the ratio 1 : 2 : 3. What is the largest angle?", "90°", ["60°", "30°", "120°"],
         "There are 1 + 2 + 3 = 6 parts. 180° ÷ 6 = 30° per part. The largest angle is 3 × 30° = 90°. (30° is one part only.)"),
    ]
    # check the arithmetic in the word problems
    assert 180 - 47 - 68 == 65 and 180 - 90 - 25 == 65 and 180 - 35 - 35 == 110 and (180 - 40) / 2 == 70
    assert (180 - 120) / 2 == 30 and 180 - 52.5 - 74.5 == 53 and 180 - 2 * 72.5 == 35 and 180 - 38 - 76 == 66
    for q, ans, wrong, e in words:
        its.append(mcq(q, ans, wrong, e, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Find the missing angle", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_words(rnd):
    its = []
    world = [
        ("A yield sign is an equilateral triangle that points down. One yield sign has sides of 75 cm. What is its perimeter?",
         "225 cm", ["150 cm", "75 cm", "300 cm"], "All 3 sides are 75 cm: 3 × 75 = 225 cm. (150 cm counts only 2 sides.)"),
        ("Liam’s lacrosse team makes a pennant shaped like an isosceles triangle. The pointed end has a 30° angle. "
         "The other 2 angles are equal. How big is each one?", "75°", ["150°", "30°", "60°"],
         "180° − 30° = 150°, shared by 2 equal angles: 150° ÷ 2 = 75°."),
        ("The roof of a cabin in Whistler makes an isosceles triangle. The two bottom angles are 35° each. "
         "What is the angle at the top?", "110°", ["145°", "35°", "55°"],
         "35° + 35° = 70°. 180° − 70° = 110°. That angle is more than 90°, so the roof triangle is obtuse."),
        ("A ladder leans against a wall. The wall meets the ground at a right angle, and the ladder makes a 70° angle with the ground. "
         "What angle does the ladder make with the wall?", "20°", ["110°", "70°", "290°"],
         "The ladder, wall and ground make a right triangle. 180° − 90° − 70° = 20°."),
        ("A ramp at the school entrance makes a right triangle with the ground. The ramp makes a 5° angle with the ground. "
         "What is the third angle?", "85°", ["175°", "95°", "5°"], "180° − 90° − 5° = 85°. (175° forgets the right angle.)"),
        ("Emma cuts a square Nanaimo bar from corner to corner. What kind of triangles does she get?", "right isosceles",
         ["acute isosceles", "right scalene", "obtuse scalene"],
         "Each piece has a square corner (90°) and 2 equal sides (two sides of the square), so it is a right isosceles triangle."),
        ("Simran has straws that are 3 cm, 4 cm and 9 cm long. Can she join their ends to make a triangle?",
         "No, 3 + 4 is less than 9", ["Yes, any 3 straws work", "Yes, a scalene one", "No, it needs equal sides"],
         "The two short straws together are only 7 cm. They cannot reach across the 9 cm straw, so no triangle is made."),
        ("Kai draws a 6 cm line. At each end he draws a 60° angle, and the two new lines meet. What kind of triangle is it?",
         "equilateral", ["right", "scalene", "obtuse"],
         "The third angle is 180° − 60° − 60° = 60°. All 3 angles are equal, so all 3 sides are equal (6 cm each)."),
        ("Zara draws an 8 cm line. She draws a 90° angle at one end and a 45° angle at the other. What is the third angle?",
         "45°", ["90°", "135°", "225°"],
         "180° − 90° − 45° = 45°. Two equal angles mean two equal sides, so Zara drew a right isosceles triangle."),
        ("On a camping trip in the Okanagan, the front of a tent is an isosceles triangle with sides of 1.5 m, 1.5 m and 2 m. "
         "What is its perimeter?", "5 m", ["3.5 m", "4.5 m", "6 m"], "1.5 + 1.5 + 2 = 5 m. (3.5 m forgets one of the 1.5 m sides.)"),
        ("Jasleen sews 12 triangle patches for a quilt. Each patch has sides of 6 cm, 8 cm and 10 cm. "
         "How much trim does she need to go around all 12 patches?", "288 cm", ["24 cm", "120 cm", "240 cm"],
         "One patch: 6 + 8 + 10 = 24 cm. For 12 patches: 12 × 24 = 288 cm. (24 cm is only one patch, and 120 cm is 12 × 10.)"),
        ("A sailboat on English Bay has a triangular sail with a right angle at the bottom. One other angle is 52°. "
         "What is the third angle?", "38°", ["128°", "52°", "218°"],
         "180° − 90° − 52° = 38°. (128° forgets the right angle.)"),
        ("Students make triangle flags for the Terry Fox Run. Each flag has angles of 40°, 70° and 70°. "
         "What is the full name of the triangle?", "acute isosceles", ["obtuse isosceles", "acute scalene", "right isosceles"],
         "All angles are less than 90° (acute), and 2 equal angles mean 2 equal sides (isosceles)."),
        ("A bike frame has a triangle with angles of 60° and 70°. What is the third angle?", "50°",
         ["130°", "230°", "120°"], "60° + 70° = 130°. 180° − 130° = 50°."),
        ("Ava says a triangle can have one right angle and one obtuse angle. Is she right?", "No, that is over 180°",
         ["Yes, if it is big", "Yes, if it is scalene", "Yes, if it is isosceles"],
         "90° plus an angle bigger than 90° is already more than 180°, but all 3 angles must add to 180°."),
        ("The two equal legs of a sign at a farmers’ market in Kelowna meet at the top at 50°. "
         "What angle does each leg make with the ground?", "65°", ["130°", "50°", "25°"],
         "The legs and the ground make an isosceles triangle. 180° − 50° = 130°, and 130° ÷ 2 = 65°."),
        ("A ferry route in BC makes a triangle between three islands. Two of its angles are 40° and 65°. "
         "What is the third angle?", "75°", ["105°", "115°", "255°"],
         "40° + 65° = 105°. 180° − 105° = 75°. (115° subtracts only the 65° angle.)"),
        ("A garden bed in Surrey is a triangle with sides of 3 m, 4 m and 5 m. Edging costs $8 per metre. "
         "How much does edging for the whole bed cost?", "$96", ["$40", "$12", "$480"],
         "Perimeter: 3 + 4 + 5 = 12 m. Cost: 12 × $8 = $96. (12 is the length in metres, not the cost, and $40 is the longest side only.)"),
        ("Owen’s class builds a triangular kite frame with angles in the ratio 2 : 3 : 4. What is the smallest angle?", "40°",
         ["20°", "60°", "80°"],
         "There are 2 + 3 + 4 = 9 parts. 180° ÷ 9 = 20° per part. The smallest angle is 2 × 20° = 40°. (20° is one part only.)"),
        ("Hana cuts a rectangular sheet of paper from corner to corner. One angle in each piece is 35°. "
         "What are the other two angles?", "90° and 55°", ["90° and 35°", "55° and 55°", "145° and 0°"],
         "Cutting a rectangle corner to corner keeps a square corner, so one angle is 90°. 180° − 90° − 35° = 55°."),
    ]
    assert 3 * 75 == 225 and (180 - 30) / 2 == 75 and 180 - 70 == 110 and 180 - 90 - 70 == 20 and 180 - 95 == 85
    assert 12 * 24 == 288 and 180 - 90 - 52 == 38 and 180 - 130 == 50 and (180 - 50) / 2 == 65 and 180 - 105 == 75
    assert 12 * 8 == 96 and 180 // 9 * 2 == 40 and 180 - 90 - 35 == 55
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
    iso, _ = tri_svg(tri_ang(70, 70), 0, bw=150, bh=150, label="isosceles triangle with a top angle of 40°",
                     ticks=True, ang_lab=["?", "?", "40°"])
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
        "<p>The 3 angles of every triangle add to 180°, big or small. Tear off the 3 corners of a paper triangle and they make a straight line.</p>"
        "<p>To find a missing angle, add the two you know and subtract from 180°.</p>"
        "<figure class='sn-fig'>" + summ +
        "<figcaption>50° + 60° = 110°, and 180° − 110° = 70°.</figcaption></figure>" +
        ex("Example 2", "Two angles of a triangle are 52.5° and 74.5°. Find the third angle.",
           "52.5° + 74.5° = 127°. 180° − 127° = 53°.", "53°") +
        "<h2>Isosceles and right triangles</h2>"
        "<p>In an isosceles triangle, the 2 angles next to the third side are equal. In a right triangle, the other 2 angles add to 90°.</p>"
        "<figure class='sn-fig'>" + iso +
        "<figcaption>180° − 40° = 140°, and 140° ÷ 2 = 70° for each equal angle.</figcaption></figure>" +
        ex("Example 3", "The angles of a triangle are in the ratio 1 : 2 : 3. Find the angles.",
           "1 + 2 + 3 = 6 parts. 180° ÷ 6 = 30° per part. The angles are 30°, 60° and 90°.", "30°, 60° and 90° (a right triangle)") +
        "<p><b>Construct a triangle.</b> Draw one side with a ruler. Use a protractor to draw the angle at each end. "
        "The two new lines meet at the third corner. A 6 cm side with 60° at both ends makes an equilateral triangle.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["A right triangle has 2 right angles", "It has exactly 1. The other 2 angles are acute and add to 90°"],
            ["An isosceles triangle must point up", "Count the equal sides. It can point any way"],
            ["A triangle with 2 acute angles is acute", "Every triangle has 2 acute angles. Look at the largest one"],
            ["Subtracting from 360° or 90°", "The angles of a triangle add to 180°"],
            ["Subtracting only one known angle", "Subtract both known angles from 180°"],
            ["Forgetting to halve for 2 equal angles", "Subtract the top angle from 180°, then divide by 2"],
            ["A bigger triangle has bigger angles in total", "Every triangle’s angles add to 180°"],
        ])
    )


FAQ = [
    {"q": "What do Grade 6 students learn about triangles in the BC math curriculum?",
     "a": "In Geometry and measurement, Grade 6 students classify triangles by their sides and by their angles, learn that the 3 angles add to 180°, and use this to find missing angles and construct triangles."},
    {"q": "Do the angles of a triangle always add up to 180°?",
     "a": "Yes. In every triangle the 3 angles add to 180°, no matter how big it is. To find a missing angle, add the two known angles and subtract from 180°."},
    {"q": "Can a triangle have two right angles?",
     "a": "No. Two right angles already make 180°, so nothing is left for the third angle. A right triangle has exactly 1 right angle and 2 acute angles."},
    {"q": "How do you find the missing angles of an isosceles triangle?",
     "a": "The 2 base angles are equal. If you know the top angle, subtract it from 180° and divide by 2. If you know one base angle, double it and subtract from 180°."},
]


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    rnd = random.Random(56814)
    spots = Spots(rnd)
    sets = [set_sides(rnd, spots), set_angles(rnd, spots), set_sum(rnd), set_missing(rnd), set_words(rnd)]
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
            k = plain(it["q"])
            if "<svg" not in it["q"]:
                assert k not in seen, it["q"]
            seen.add(k + "|" + "|".join(sorted(it["c"])))
            seen.add(k)
    return {
        "country": "ca-bc", "subject": "math", "grade": "grade-6", "slug": "triangles", "sort": 14,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 6 Triangles: Classify by Sides and Angles, Angle Sum and Missing Angles",
        "seo_title": "Grade 6 Triangles Worksheets: Classify Triangles and Find Missing Angles (Free Math, Answer Key, BC Curriculum)",
        "short_title": "Triangles",
        "domain": "Geometry and measurement",
        "standard_code": "Grade 6: Geometry and measurement",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/6/core",
        "standard_text": "Triangles",
        "meta_desc": "Free Grade 6 math worksheets on triangles for the BC curriculum: classify triangles as equilateral, isosceles or scalene and as acute, right or obtuse, use the 180° angle sum, find missing angles in isosceles and right triangles, and solve word problems about yield signs, roofs and sails. 100 questions with an answer key.",
        "key_big": "Name a triangle by its sides and by its largest angle. Its 3 angles always add to 180°.",
        "key_sub": "Equilateral, isosceles, scalene: count the equal sides. Acute, right, obtuse: look at the largest angle. Missing angle: subtract the two known angles from 180°. A right triangle has only 1 right angle.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "four triangles labelled A to D")
    os.makedirs(OUT, exist_ok=True)
    path_ = os.path.join(OUT, u["slug"] + ".json")
    with open(path_, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path_)
