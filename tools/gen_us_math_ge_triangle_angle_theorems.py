# -*- coding: utf-8 -*-
"""
US Geometry: Triangle Angle Theorems (Common Core G-CO.C.10)
  python3 tools/gen_us_math_ge_triangle_angle_theorems.py
The Triangle Angle Sum Theorem, the Exterior Angle Theorem, solving for x, isosceles and equilateral
triangles, and classifying triangles with word problems.
Wrong answers come from real mistakes: subtracting from 360° instead of 180°, adding the adjacent interior
angle to the exterior angle, treating the vertex angle as a base angle, and stopping at x.
"""
import math
import random
from us_hs import B, S, make, lesson, collect, T, fig, num, MINUS, People
from us_geo import Canvas, RED, GREEN, BLUE, INK

R = random.Random(92901)


def lin(a, b):
    s = ("" if a == 1 else num(a)) + "<i>x</i>"
    if b > 0:
        s += " + %s" % num(b)
    elif b < 0:
        s += " %s %s" % (MINUS, num(-b))
    return s


def tri_pts(a, b, base=280):
    """base angles a (left) and b (right) in degrees, drawn with a horizontal base"""
    a_, b_ = max(a, 30), max(b, 30)
    A = (40.0, 190.0)
    Bp = (40.0 + base, 190.0)
    ta, tb = math.tan(math.radians(a_)), math.tan(math.radians(b_))
    x = base * tb / (ta + tb)
    h = x * ta
    if h > 170:
        k = 170 / h
        Bp = (40 + base * k, 190.0)
        x, h = x * k, 170
    C = (40 + x, 190 - h)
    return A, Bp, C


def tri_fig(angs, labels, names=("A", "B", "C"), ext=False, ticks=None):
    """angs = (left, right) base angles for the drawing; labels = texts for left, right, top (None to skip)"""
    A, Bp, C = tri_pts(*angs)
    c = Canvas()
    c.poly([A, Bp, C])
    if ext:
        E = (Bp[0] + 70, Bp[1])
        c.seg(Bp, E)
        c.dot(E, 3)
    c.vlabels([A, Bp, C], names)
    for v, p, q, t in ((A, Bp, C, labels[0]), (Bp, C, A, labels[1]), (C, A, Bp, labels[2])):
        if t:
            c.angle(v, p, q, "", r=20)
            th = abs(math.atan2(p[1] - v[1], p[0] - v[0]) - math.atan2(q[1] - v[1], q[0] - v[0]))
            th = min(th, 2 * math.pi - th)
            w = 7.2 * len(t.replace("<i>", "").replace("</i>", ""))
            rr = max(36, (w / 2 + 4) / math.tan(th / 2) * 0.55 + 18)
            side = min(math.hypot(p[0] - v[0], p[1] - v[1]), math.hypot(q[0] - v[0], q[1] - v[1]))
            c.angle_text(v, p, q, t, r=min(rr, side * 0.55), fs=13)
    if ext and len(labels) > 3 and labels[3]:
        E = (Bp[0] + 70, Bp[1])
        c.angle(Bp, E, C, "", r=18, col=RED)
        c.angle_text(Bp, E, C, labels[3], r=44 if len(labels[3]) > 4 else 36, fs=13, col=RED)
    if ticks:
        for (p, q) in ticks:
            c.ticks((A, Bp, C)[p], (A, Bp, C)[q], 1)
    return c.svg("triangle, not drawn to scale")


def opts(ans, wr, unit="°"):
    return ["%s%s" % (num(w), unit) for w in dict.fromkeys(wr) if w != ans and w > 0][:3]


# ------------------------------------------------------------ set 1: angle sum
def one_sum(r):
    a, b = r.randint(25, 95), r.randint(25, 80)
    c_ = 180 - a - b
    if c_ < 15:
        return None
    order = r.choice([0, 1, 2])
    vals = [a, b, c_]
    labs = ["%d°" % v for v in vals]
    labs[order] = "<i>x</i>°"
    svg = tri_fig((a, b), labs)
    ans = vals[order]
    known = [v for i, v in enumerate(vals) if i != order]
    q = "Find <i>x</i>.%s" % fig(svg)
    e = "The angles of a triangle add to 180°: <i>x</i> = 180 %s %d %s %d = <b>%d</b>." % (MINUS, known[0], MINUS, known[1], ans)
    wr = [360 - known[0] - known[1], known[0] + known[1], 90 - known[1] if known[1] < 90 else ans + 10, ans + 10]
    return T(q, num(ans), [num(w) for w in dict.fromkeys(wr) if w != ans and w > 0][:3], e)


# ------------------------------------------------------------ set 2: exterior angle theorem
def one_ext(r):
    a, c_ = r.randint(30, 80), r.randint(30, 80)
    b = 180 - a - c_
    if b < 20:
        return None
    ext = a + c_
    kind = r.choice(["ext", "int", "alg"])
    if kind == "ext":
        svg = tri_fig((a, b), ["%d°" % a, None, "%d°" % c_, "<i>x</i>°"], ext=True)
        q = "Find <i>x</i>, the exterior angle.%s" % fig(svg)
        ans = ext
        e = "Exterior Angle Theorem: an exterior angle equals the sum of the two remote interior angles. <i>x</i> = %d + %d = <b>%d</b>." % (a, c_, ans)
        wr = [b, 180 - ext, 360 - ext, ext + 10]
    elif kind == "int":
        svg = tri_fig((a, b), ["<i>x</i>°", None, "%d°" % c_, "%d°" % ext], ext=True)
        q = "Find <i>x</i>.%s" % fig(svg)
        ans = a
        e = "The exterior angle equals the sum of the remote interior angles: %d = <i>x</i> + %d, so <i>x</i> = <b>%d</b>." % (ext, c_, ans)
        wr = [180 - ext, ext + c_, b, 180 - c_]
    else:
        x = r.randint(4, 18)
        k1, k2 = r.randint(1, 4), r.randint(1, 4)
        d1 = a - k1 * x
        d2 = c_ - k2 * x
        k3 = r.choice([k for k in range(1, 9) if k != k1 + k2])
        d3 = ext - k3 * x
        if a <= 0 or abs(d1) > 40 or abs(d2) > 40 or abs(d3) > 60 or d1 == 0 and d2 == 0:
            return None
        svg = tri_fig((a, b), [lin(k1, d1) + "°", None, lin(k2, d2) + "°", lin(k3, d3) + "°"], ext=True)
        ask = r.choice(["x", "ext"])
        q = "Find %s.%s" % ("<i>x</i>" if ask == "x" else "the measure of the exterior angle", fig(svg))
        steps = "Exterior angle = sum of the remote interior angles: %s = (%s) + (%s), so <i>x</i> = %d." % (lin(k3, d3), lin(k1, d1), lin(k2, d2), x)
        if ask == "x":
            bad = (180 - d1 - d2 - d3) / (k1 + k2 + k3)
            wr = [int(bad) if bad == int(bad) and bad > 0 else x + 3, ext, x + 1, x - 2]
            return T(q, num(x), [num(w) for w in dict.fromkeys(wr) if w != x and w > 0][:3], steps.replace("<i>x</i> = %d." % x, "<i>x</i> = <b>%d</b>." % x))
        return T(q, "%d°" % ext, opts(ext, [x, 180 - ext, a, ext + 10]), steps + " The exterior angle is %d(%d) %s %d = <b>%d°</b>." % (
            k3, x, "+" if d3 >= 0 else MINUS, abs(d3), ext))
    return T(q, num(ans), [num(w) for w in dict.fromkeys(wr) if w != ans and w > 0][:3], e)


# ------------------------------------------------------------ set 3: algebra with the angle sum
def one_alg(r):
    x = r.randint(5, 25)
    k = [r.randint(1, 5) for _ in range(3)]
    ang = [r.randint(25, 100), r.randint(25, 80)]
    ang.append(180 - sum(ang))
    if ang[2] < 15:
        return None
    d = [ang[i] - k[i] * x for i in range(3)]
    if any(abs(v) > 45 for v in d):
        return None
    if r.random() < 0.3:
        d[0] = 0 if False else d[0]
    labs = [lin(k[i], d[i]) + "°" if d[i] or True else "" for i in range(3)]
    svg = tri_fig((ang[0], ang[1]), labs)
    ask = r.choice(["x", "x", "big", "small"])
    tot_k, tot_d = sum(k), sum(d)
    steps = "Add the angles and set the sum equal to 180: %s = 180, so %d<i>x</i> = %d and <i>x</i> = %d." % (
        lin(tot_k, tot_d), tot_k, 180 - tot_d, x)
    if ask == "x":
        bad = (360 - tot_d) / tot_k
        wr = [int(bad) if bad == int(bad) else x + 2, x + 1, max(ang), x - 1]
        q = "Find <i>x</i>.%s" % fig(svg)
        return T(q, num(x), [num(w) for w in dict.fromkeys(wr) if w != x and w > 0][:3], steps.replace("and <i>x</i> = %d." % x, "and <i>x</i> = <b>%d</b>." % x))
    want = max(ang) if ask == "big" else min(ang)
    if sorted(ang)[1] == want:
        return None
    q = "Find the measure of the %s angle.%s" % ("largest" if ask == "big" else "smallest", fig(svg))
    wr = [x, min(ang) if ask == "big" else max(ang), sorted(ang)[1], want + 10]
    e = steps + " The angles are %d°, %d° and %d°. The %s is <b>%d°</b>." % (ang[0], ang[1], ang[2], "largest" if ask == "big" else "smallest", want)
    return T(q, "%d°" % want, opts(want, wr), e)


# ------------------------------------------------------------ set 4: isosceles and equilateral
def one_iso(r):
    kind = r.choice(["base", "vertex", "alg", "alg", "equi"])
    if kind == "equi":
        x = r.randint(4, 15)
        k = r.randint(2, 6)
        d = 60 - k * x
        if abs(d) > 40:
            return None
        q = "Triangle ABC is equilateral, and m∠A = (%s)°. Find <i>x</i>." % lin(k, d)
        e = "Every angle of an equilateral triangle is 60°: %s = 60, so %d<i>x</i> = %d and <i>x</i> = <b>%d</b>." % (lin(k, d), k, 60 - d, x)
        bad = (180 - d) / k
        wr = [int(bad) if bad == int(bad) else x + 2, 60, x + 1, x - 1]
        return T(q, num(x), [num(w) for w in dict.fromkeys(wr) if w != x and w > 0][:3], e)
    base = r.randint(25, 80)
    vert = 180 - 2 * base
    if kind == "base":
        svg = tri_fig((base, base), [None, "<i>x</i>°", "%d°" % vert], ticks=[(0, 2), (1, 2)])
        q = "The triangle is isosceles, with the congruent sides marked. Find <i>x</i>.%s" % fig(svg)
        ans = base
        e = "The base angles are congruent. They share 180° %s %d° = %d°, so <i>x</i> = %d ÷ 2 = <b>%d</b>." % (MINUS, vert, 180 - vert, 180 - vert, ans)
        wr = [vert, 180 - vert, (180 - vert) // 3 if False else 90 - vert // 2 if vert % 2 == 0 and 90 - vert // 2 != ans else ans + 5]
    elif kind == "vertex":
        svg = tri_fig((base, base), ["%d°" % base, None, "<i>x</i>°"], ticks=[(0, 2), (1, 2)])
        q = "The triangle is isosceles, with the congruent sides marked. Find <i>x</i>.%s" % fig(svg)
        ans = vert
        e = "The two base angles are both %d°. <i>x</i> = 180 %s 2(%d) = <b>%d</b>." % (base, MINUS, base, ans)
        wr = [180 - base, base, 180 - 3 * base if 180 - 3 * base > 0 else ans + 10]
    else:
        x = r.randint(4, 16)
        k1, k2 = r.sample(range(1, 7), 2)
        d1 = base - k1 * x
        d2 = base - k2 * x
        if abs(d1) > 40 or abs(d2) > 40:
            return None
        svg = tri_fig((base, base), [lin(k1, d1) + "°", lin(k2, d2) + "°", None], ticks=[(0, 2), (1, 2)])
        ask = r.choice(["x", "vertex"])
        q = "The triangle is isosceles, with the congruent sides marked. Find %s.%s" % ("<i>x</i>" if ask == "x" else "the vertex angle (the top angle)", fig(svg))
        diff = abs(k1 - k2)
        steps = "Base angles are congruent: %s = %s, so %s<i>x</i> = %d and <i>x</i> = %d." % (lin(k1, d1), lin(k2, d2), num(diff) if diff > 1 else "", abs(d2 - d1), x)
        steps = steps.replace(", so <i>x</i> = %d and <i>x</i> = " % abs(d2 - d1), ", so <i>x</i> = ")
        if ask == "x":
            bad = (180 - d1 - d2) / (k1 + k2)
            wr = [int(bad) if bad == int(bad) and bad > 0 else x + 2, base, x + 1]
            return T(q, num(x), [num(w) for w in dict.fromkeys(wr) if w != x and w > 0][:3], steps[:steps.rindex("= %d." % x)] + "= <b>%d</b>." % x)
        return T(q, "%d°" % vert, opts(vert, [base, 180 - base, x, vert + 10]),
                 steps + " Each base angle is %d°, so the vertex angle is 180 %s 2(%d) = <b>%d°</b>." % (base, MINUS, base, vert))
    return T(q, num(ans), [num(w) for w in dict.fromkeys(wr) if w != ans and w > 0][:3], e)


# ------------------------------------------------------------ set 5: classify and word problems
def one_word(r):
    pp = People(r)
    nm, he, his = pp.next()
    kind = r.choice(["ratio", "ratio", "right", "classify", "roof", "tf"])
    if kind == "ratio":
        p = sorted(r.sample(range(1, 9), 3))
        if 180 % sum(p) or p[2] * 180 // sum(p) == 90:
            return None
        u = 180 // sum(p)
        angs = [u * x for x in p]
        q = "The angles of a triangle are in the ratio %d : %d : %d. Find the largest angle." % tuple(p)
        ans = angs[2]
        e = "%d + %d + %d = %d parts, and 180° ÷ %d = %d° per part. Largest = %d × %d° = <b>%d°</b>." % (p[0], p[1], p[2], sum(p), sum(p), u, p[2], u, ans)
        return T(q, "%d°" % ans, opts(ans, [angs[0], angs[1], 360 * p[2] // sum(p) if 360 % sum(p) == 0 else ans + 15, ans + 10]), e)
    if kind == "right":
        a = r.randint(15, 75)
        if a == 45:
            return None
        q = "One acute angle of a right triangle measures %d°. What is the other acute angle?" % a
        ans = 90 - a
        e = "The acute angles of a right triangle are complementary (90° + the two acute angles = 180°). 90° %s %d° = <b>%d°</b>." % (MINUS, a, ans)
        return T(q, "%d°" % ans, opts(ans, [180 - a, 90 + a, a]), e)
    if kind == "classify":
        a = r.randint(20, 120)
        b = r.randint(20, 100)
        c_ = 180 - a - b
        if c_ < 10 or len({a, b, c_}) < 3:
            return None
        m = max(a, b, c_)
        right = "Obtuse" if m > 90 else ("Right" if m == 90 else "Acute")
        q = "A triangle has angles of %d° and %d°. Classify it by its angles." % (a, b)
        e = "The third angle is 180 %s %d %s %d = %d°. The largest angle is %d°, so the triangle is <b>%s</b>." % (MINUS, a, MINUS, b, c_, m, right.lower())
        return T(q, right, [x for x in ["Acute", "Right", "Obtuse", "Equiangular"] if x != right], e)
    if kind == "roof":
        v = r.choice([100, 110, 120, 130, 140, 96, 104, 116])
        q = "The two sloping sides of a roof truss are the same length, and the angle at the peak is %d°. What angle does each sloping side make with the horizontal beam?" % v
        ans = (180 - v) // 2
        e = "The truss is an isosceles triangle, so the base angles are equal: (180 %s %d) ÷ 2 = <b>%d°</b>." % (MINUS, v, ans)
        return T(q, "%d°" % ans, opts(ans, [180 - v, v // 2, 90 - v // 2 if 90 - v // 2 > 0 else ans + 10, ans + 5]), e)
    items = [("Can a triangle have two right angles?", "No, because the third angle would be 0°", ["Yes, if it is isosceles", "Yes, if the third angle is acute", "No, because a right triangle has three acute angles"],
              "90° + 90° = 180°, which leaves nothing for the third angle."),
             ("Can a triangle have two obtuse angles?", "No, because their sum is already more than 180°", ["Yes, if the third angle is small", "Yes, in an isosceles triangle", "No, because obtuse angles must be next to each other"],
              "Two angles over 90° add to more than 180°."),
             ("Can an obtuse triangle be isosceles?", "Yes, if the obtuse angle is the vertex angle", ["No, never", "Only if it is also a right triangle", "Yes, if the obtuse angles are the base angles"],
              "For example 120°, 30°, 30°. The base angles must be acute."),
             ("What is the measure of each angle of an equiangular triangle?", "60°", ["90°", "45°", "180°"], "180° ÷ 3 = 60°."),
             ("An exterior angle of a triangle is 90°. What kind of triangle is it?", "A right triangle", ["An acute triangle", "An obtuse triangle", "An equilateral triangle"],
              "The interior angle next to it is 180° %s 90° = 90°." % MINUS),
             ("What is the sum of the three exterior angles of a triangle, one at each vertex?", "360°", ["180°", "540°", "It depends on the triangle"],
              "Each exterior angle is 180° minus its interior angle: 3(180°) %s 180° = 360°." % MINUS)]
    q, right, wr, e = r.choice(items)
    return T(q, right, wr, e + " <b>%s</b>." % right)


def build():
    sets = [S("Triangle Angle Sum Theorem", collect(one_sum, 20, R)),
            S("Exterior Angle Theorem", collect(one_ext, 20, R)),
            S("Solve for x", collect(one_alg, 20, R)),
            S("Isosceles and equilateral triangles", collect(one_iso, 20, R)),
            S("Classify triangles and word problems", collect(one_word, 20, R))]
    body = lesson(
        "<p><b>Triangle Angle Sum Theorem</b>: the three interior angles of a triangle add to 180°.</p>"
        "<p><b>Exterior Angle Theorem</b>: an exterior angle equals the sum of the two <b>remote</b> interior angles (the two that are not next to it).</p>"
        "<p><b>Isosceles Triangle Theorem</b>: if two sides are congruent, the angles opposite them (the base angles) are congruent. "
        "An equilateral triangle has three 60° angles.</p>"
        "<p>The acute angles of a right triangle add to 90°.</p>",
        [("A triangle has angles (2<i>x</i> + 10)°, (3<i>x</i>)° and (<i>x</i> + 20)°. Find the largest angle.",
          ["6<i>x</i> + 30 = 180, so <i>x</i> = 25", "Angles: 60°, 75°, 45°"], "75°"),
         ("An isosceles triangle has a vertex angle of 40°. Find each base angle.", ["180 %s 40 = 140", "140 ÷ 2 = 70"], "70°")],
        ["Using 360° instead of 180° for the angles of a triangle.",
         "Adding the interior angle next to the exterior angle. Use the two remote angles.",
         "Treating the vertex angle as a base angle. The base angles are opposite the congruent sides.",
         "Stopping at <i>x</i> when the question asks for an angle."])
    faq = [("What do the angles of a triangle add up to?", "180 degrees. This is the Triangle Angle Sum Theorem."),
           ("What is the Exterior Angle Theorem?", "An exterior angle of a triangle equals the sum of the two interior angles that are not next to it."),
           ("What are the base angles of an isosceles triangle?", "The two angles opposite the congruent sides. They are always congruent."),
           ("Can a triangle have two right angles?", "No. Two right angles already add to 180 degrees, leaving nothing for the third angle.")]
    make("triangle-angle-theorems", 9, "G-CO.C.10",
         "Triangle Angle Theorems: Angle Sum, Exterior Angles, and Isosceles Triangles",
         "Triangle Angle Sum and Exterior Angle Theorem Worksheet (Geometry) | 100 Questions",
         "Triangle Angle Theorems",
         "Prove theorems about triangles. Theorems include: measures of interior angles of a triangle sum to 180°; base angles of isosceles triangles are congruent; the segment joining midpoints of two sides of a triangle is parallel to the third side and half the length; the medians of a triangle meet at a point.",
         "Free Geometry worksheet on triangle angle theorems: the angle sum, the Exterior Angle Theorem, solving for x, and isosceles and equilateral triangles. 100 questions with answers.",
         "The angles of a triangle add to 180°.",
         "An exterior angle equals the sum of the two remote interior angles. Base angles of an isosceles triangle are congruent.",
         body, faq, sets, R, domain="Triangles", grade="geometry")


if __name__ == "__main__":
    build()
