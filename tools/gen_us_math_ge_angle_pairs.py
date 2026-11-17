# -*- coding: utf-8 -*-
"""
US Geometry: Angle Pairs and the Angle Addition Postulate (Common Core G-CO.C.9, G-CO.A.1)
  python3 tools/gen_us_math_ge_angle_pairs.py
The Angle Addition Postulate, angle bisectors with algebra, complementary and supplementary angles,
vertical angles and linear pairs, and word problems.
Wrong answers come from real mistakes: mixing up complement (90°) and supplement (180°), setting a linear
pair equal instead of adding to 180°, adding vertical angles to 180°, and giving x instead of the angle.
"""
import random
from us_hs import B, S, make, lesson, collect, T, fig, num, MINUS, People
from us_geo import Canvas, pol, RED, GREEN, BLUE

R = random.Random(92401)
ANG = "∠"
TRIOS = [("A", "B", "C", "D"), ("P", "Q", "R", "S"), ("J", "K", "L", "M"), ("X", "Y", "Z", "W"), ("D", "E", "F", "G"), ("R", "S", "T", "U")]


def dg(v):
    return "%s°" % num(v)


def lin(a, b):
    s = ("" if a == 1 else num(a)) + "<i>x</i>"
    if b > 0:
        s += " + %s" % num(b)
    elif b < 0:
        s += " %s %s" % (MINUS, num(-b))
    return s


def m(n):
    return "m%s%s" % (ANG, n)


def split_fig(A, Bv, C, D, t1, t2, tot=None, deg_total=110, k=0.45):
    c = Canvas()
    V = (40, 170)
    deg_total = max(50, min(150, deg_total))
    k = max(0.25, min(0.75, k))
    pa, pc = pol(V[0], V[1], 190, deg_total), pol(V[0], V[1], 190, 0)
    pd = pol(V[0], V[1], 190, deg_total * k)
    for p in (pa, pc, pd):
        c.ray(V, p, 10)
    c.dot(V)
    c.text((V[0] - 6, V[1] + 20), Bv, 16)
    c.text(pol(V[0], V[1], 215, deg_total), A, 16)
    c.text(pol(V[0], V[1], 215, 0), C, 16)
    c.text(pol(V[0], V[1], 215, deg_total * k), D, 16)
    c.angle(V, pc, pd, t1, r=50, tr=95)
    c.angle(V, pd, pa, t2, r=58, col=BLUE, tr=105)
    if tot:
        c.text((V[0] + 40, V[1] + 26), tot, 14, RED, anchor="start")
    return c.svg("angle %s%s%s with ray %s%s inside, not drawn to scale" % (A, Bv, C, Bv, D))


def x_fig(a1, labels):
    """two lines crossing; a1 = acute angle in degrees; labels for the angles 1..4 (right, top, left, bottom)"""
    c = Canvas()
    O = (150, 110)
    p1, p2 = pol(O[0], O[1], 120, a1), pol(O[0], O[1], 120, 180 + a1)
    q1, q2 = pol(O[0], O[1], 120, 0), pol(O[0], O[1], 120, 180)
    c.fullline(p2, p1, 10)
    c.fullline(q2, q1, 10)
    mids = [a1 / 2, 90 + a1 / 2, 180 + a1 / 2, 270 + a1 / 2]
    for t, mid in zip(labels, mids):
        if t:
            rr = 46 if mid % 180 < 90 else 40
            c.text(pol(O[0], O[1], rr, mid), t, 14, INKC if not t.isdigit() else GREEN)
    return c.svg("two intersecting lines, not drawn to scale")


INKC = "#2b2b2b"


# ------------------------------------------------------------ set 1: Angle Addition Postulate
def one_add(r):
    A, Bv, C, D = r.choice(TRIOS)
    a1, a2 = r.randint(15, 80), r.randint(15, 80)
    kind = r.choice(["whole", "part", "part"])
    if kind == "whole":
        svg = split_fig(A, Bv, C, D, dg(a1), dg(a2), None, a1 + a2, a1 / (a1 + a2))
        q = "Find %s.%s" % (m(A + Bv + C), fig(svg))
        ans, wr = a1 + a2, [abs(a1 - a2), 180 - a1 - a2 if a1 + a2 < 180 else a1 + a2 + 10, a1 + a2 + 10]
        e = "Angle Addition Postulate: %s + %s = %s. %d° + %d° = <b>%d°</b>." % (m(A + Bv + D), m(D + Bv + C), m(A + Bv + C), a2, a1, ans)
    else:
        tot = a1 + a2
        svg = split_fig(A, Bv, C, D, "?", dg(a2), "%s = %s" % (m(A + Bv + C), dg(tot)), tot, a1 / tot)
        q = "%s = %s. Find %s.%s" % (m(A + Bv + C), dg(tot), m(D + Bv + C), fig(svg))
        ans, wr = a1, [tot + a2, 180 - tot if tot < 180 else a1 + 10, 90 - a2 if a2 < 90 and 90 - a2 != a1 else a1 + 5]
        e = "%s + %s = %s, so %s = %d° %s %d° = <b>%d°</b>." % (m(A + Bv + D), m(D + Bv + C), m(A + Bv + C), m(D + Bv + C), tot, MINUS, a2, ans)
    wr = [w for w in dict.fromkeys(wr) if w != ans and 0 < w < 360] + [ans + 4, ans - 6]
    return T(q, dg(ans), [dg(w) for w in dict.fromkeys(wr) if w != ans][:3], e)


# ------------------------------------------------------------ set 2: algebra and bisectors
def one_alg(r):
    A, Bv, C, D = r.choice(TRIOS)
    x = r.randint(3, 15)
    if r.random() < 0.5:
        a1, b1 = r.randint(2, 6), r.randint(-10, 15)
        a2, b2 = r.randint(1, 5), r.randint(-10, 15)
        v1, v2 = a1 * x + b1, a2 * x + b2
        if v1 < 10 or v2 < 10 or v1 + v2 > 170:
            return None
        tot = v1 + v2
        ask = r.choice(["x", "part"])
        svg = split_fig(A, Bv, C, D, lin(a1, b1) + "°", lin(a2, b2) + "°", "%s = %s" % (m(A + Bv + C), dg(tot)), tot, v1 / tot)
        q = "%s = %s, %s = (%s)° and %s = (%s)°. %s%s" % (
            m(A + Bv + C), dg(tot), m(D + Bv + C), lin(a1, b1), m(A + Bv + D), lin(a2, b2),
            "Find <i>x</i>." if ask == "x" else "Find %s." % m(D + Bv + C), fig(svg))
        steps = "(%s) + (%s) = %d, so %d<i>x</i> = %d and <i>x</i> = %d." % (lin(a1, b1), lin(a2, b2), tot, a1 + a2, tot - b1 - b2, x)
        if ask == "x":
            return T(q, num(x), [num(w) for w in dict.fromkeys([v1, v2, x + 2, x - 1]) if w != x][:3], steps.replace("= %d." % x, "= <b>%d</b>." % x))
        return T(q, dg(v1), [dg(w) for w in dict.fromkeys([x, v2, tot - x, v1 + 10]) if w != v1 and w > 0][:3],
                 steps + " %s = %d(%d) %s = <b>%d°</b>." % (m(D + Bv + C), a1, x, ("+ %d" % b1) if b1 >= 0 else "%s %d" % (MINUS, -b1), v1))
    a1, a2 = r.sample(range(1, 7), 2)
    b1 = r.randint(-10, 20)
    b2 = a1 * x + b1 - a2 * x
    half = a1 * x + b1
    if not (10 <= half <= 85) or abs(b2) > 40:
        return None
    ask = r.choice(["x", "whole"])
    svg = split_fig(A, Bv, C, D, lin(a1, b1) + "°", lin(a2, b2) + "°", None, 2 * half, 0.5)
    q = "%s bisects %s. %s = (%s)° and %s = (%s)°. %s%s" % (
        Bv + D, ANG + A + Bv + C, m(D + Bv + C), lin(a1, b1), m(A + Bv + D), lin(a2, b2),
        "Find <i>x</i>." if ask == "x" else "Find %s." % m(A + Bv + C), fig(svg))
    q = q.replace(Bv + D + " bisects", "Ray %s%s bisects" % (Bv, D), 1)
    steps = "A bisector makes two congruent angles: %s = %s, so %s<i>x</i> = %d and <i>x</i> = %d." % (lin(a1, b1), lin(a2, b2), num(abs(a1 - a2)) if abs(a1 - a2) > 1 else "", abs(b2 - b1), x)
    steps = steps.replace(", so <i>x</i> = %d and <i>x</i> = " % abs(b2 - b1), ", so <i>x</i> = ")
    if ask == "x":
        return T(q, num(x), [num(w) for w in dict.fromkeys([half, 2 * half, x + 1, x + 3]) if w != x][:3], steps.replace("= %d." % x, "= <b>%d</b>." % x))
    return T(q, dg(2 * half), [dg(w) for w in dict.fromkeys([half, x, 2 * half + 10, 180 - 2 * half]) if w != 2 * half and w > 0][:3],
             steps + " Each half is %d°, so %s = 2 × %d° = <b>%d°</b>." % (half, m(A + Bv + C), half, 2 * half))


# ------------------------------------------------------------ set 3: complementary and supplementary
def one_comp(r):
    kind = r.choice(["c", "s", "c", "s", "alg", "alg"])
    if kind in ("c", "s"):
        a = r.randint(5, 85) if kind == "c" else r.randint(5, 175)
        if a == 90:
            return None
        tot = 90 if kind == "c" else 180
        word = "complement" if kind == "c" else "supplement"
        q = "Find the %s of %s %s angle." % (B(word), "an" if str(a)[0] == "8" or a in (11, 18) else "a", dg(a))
        ans = tot - a
        other = (180 if kind == "c" else 90) - a
        wr = [other if other > 0 else a + 90, a, 360 - a]
        e = "%s angles add to %d°. %d° %s %d° = <b>%d°</b>." % ("Complementary" if kind == "c" else "Supplementary", tot, tot, MINUS, a, ans)
        return T(q, dg(ans), [dg(w) for w in dict.fromkeys(wr) if w != ans and w > 0][:3], e)
    tot = r.choice([90, 180])
    word = "complement" if tot == 90 else "supplement"
    k, d = r.choice([2, 3, 4, 5]), r.choice([-12, -6, 6, 10, 12, 15, 20, 30])
    # angle = k * other + d, angle + other = tot
    if (tot - d) % (k + 1):
        return None
    other = (tot - d) // (k + 1)
    ang = tot - other
    if other <= 0 or ang <= 0:
        return None
    rel = "%s %d° %s %s times its %s" % ("is", abs(d), "more than" if d > 0 else "less than", {2: "two", 3: "three", 4: "four", 5: "five"}[k], word)
    q = "An angle %s. Find the measure of the angle." % rel
    wr = [other, (180 - d) // (k + 1) if tot == 90 else (90 - d) // (k + 1), ang + d]
    e = ("Let the %s be <i>x</i>. Then the angle is %d<i>x</i> %s %d, and together they make %d°: <i>x</i> + %d<i>x</i> %s %d = %d, "
         "so %d<i>x</i> = %d and <i>x</i> = %d. The angle is %d° %s %d° = <b>%d°</b>." % (
             word, k, "+" if d > 0 else MINUS, abs(d), tot, k, "+" if d > 0 else MINUS, abs(d), tot, k + 1, tot - d, other, tot, MINUS, other, ang))
    return T(q, dg(ang), [dg(w) for w in dict.fromkeys(wr) if w != ang and w > 0][:3], e)


# ------------------------------------------------------------ set 4: vertical angles and linear pairs
def one_vert(r):
    a1 = r.choice([35, 40, 50, 55, 60, 65, 70])
    kind = r.choice(["num", "num", "algv", "algl"])
    if kind == "num":
        a = r.randint(25, 80) if r.random() < 0.5 else r.randint(100, 155)
        known = r.randint(0, 3)
        ask = r.choice([(known + 2) % 4, (known + 1) % 4, (known + 3) % 4])
        meas = [a, 180 - a, a, 180 - a]
        meas = meas[(4 - known) % 4:] + meas[:(4 - known) % 4]
        meas = [a if (i - known) % 2 == 0 else 180 - a for i in range(4)]
        labels = ["" for _ in range(4)]
        labels[known] = dg(a)
        labels[ask] = "<i>x</i>°"
        svg = x_fig(a1 if (a < 90) == (known % 2 == 0) else 180 - a1, labels)
        ans = meas[ask]
        q = "Find <i>x</i>.%s" % fig(svg)
        if (ask - known) % 2 == 0:
            e = "The angles are vertical angles (across from each other), so they are congruent: <i>x</i> = <b>%d</b>." % ans
        else:
            e = "The angles form a linear pair (side by side on a line), so they add to 180°: <i>x</i> = 180 %s %d = <b>%d</b>." % (MINUS, a, ans)
        wr = [180 - ans, 90 - ans if ans < 90 else ans - 90, 360 - ans]
        return T(q, num(ans), [num(w) for w in dict.fromkeys(wr) if w != ans and w > 0][:3], e)
    x = r.randint(4, 20)
    a1c, a2c = r.sample(range(2, 8), 2)
    b1 = r.randint(-15, 25)
    if kind == "algv":
        b2 = a1c * x + b1 - a2c * x
        v = a1c * x + b1
        if not (20 <= v <= 160) or v == 90 or abs(b2) > 60:
            return None
        labels = [lin(a1c, b1) + "°", "", lin(a2c, b2) + "°", ""]
        svg = x_fig(a1 if v < 90 else 180 - a1, labels)
        q = "The two labeled angles are vertical angles. Find <i>x</i>.%s" % fig(svg)
        e = "Vertical angles are congruent: %s = %s, so %s<i>x</i> = %d and <i>x</i> = <b>%d</b>." % (
            lin(a1c, b1), lin(a2c, b2), "" if abs(a1c - a2c) == 1 else num(abs(a1c - a2c)), abs(b2 - b1), x)
        e = e.replace(", so <i>x</i> = %d and <i>x</i> = " % abs(b2 - b1), ", so <i>x</i> = ")
        bad = (180 - b1 - b2) / (a1c + a2c)
        wr = [v, int(bad) if bad == int(bad) and bad > 0 else x + 2, x + 1, x - 2]
        return T(q, num(x), [num(w) for w in dict.fromkeys(wr) if w != x and w > 0][:3], e)
    a2c = r.randint(1, 5)
    v1 = a1c * x + b1
    b2 = 180 - v1 - a2c * x
    v2 = 180 - v1
    if not (20 <= v1 <= 160) or v1 == 90 or abs(b2) > 60:
        return None
    labels = [lin(a1c, b1) + "°", lin(a2c, b2) + "°", "", ""]
    svg = x_fig(a1 if v1 < 90 else 180 - a1, labels)
    ask = r.choice(["x", "ang"])
    q = "The two labeled angles form a linear pair. %s%s" % ("Find <i>x</i>." if ask == "x" else "Find the measure of the angle labeled (%s)°." % lin(a1c, b1), fig(svg))
    e = "A linear pair adds to 180°: (%s) + (%s) = 180, so %d<i>x</i> = %d and <i>x</i> = %d." % (
        lin(a1c, b1), lin(a2c, b2), a1c + a2c, 180 - b1 - b2, x)
    if ask == "x":
        same = (b2 - b1) / (a1c - a2c) if a1c != a2c else None
        wr = [int(same) if same and same == int(same) and same > 0 else x + 3, v1, x + 1]
        return T(q, num(x), [num(w) for w in dict.fromkeys(wr) if w != x and w > 0][:3], e.replace("= %d." % x, "= <b>%d</b>." % x))
    e += " The angle is %d(%d) %s %d = <b>%d°</b>." % (a1c, x, "+" if b1 >= 0 else MINUS, abs(b1), v1)
    return T(q, dg(v1), [dg(w) for w in dict.fromkeys([v2, x, 90 - v1 if v1 < 90 else v1 - 90]) if w != v1 and w > 0][:3], e)


# ------------------------------------------------------------ set 5: word problems and reasoning
def one_word(r):
    pp = People(r)
    nm, he, his = pp.next()
    kind = r.choice(["ramp", "scissors", "fold", "ratio", "ratio", "tf", "tf", "clock"])
    if kind == "ramp":
        a = r.randint(8, 35)
        q = "A wheelchair ramp makes a %s angle with the flat ground. What angle does the ramp make with the ground on its other side, along the same straight line?" % dg(a)
        ans, wr = 180 - a, [90 - a, a, 360 - a]
        e = "The two angles form a linear pair along the ground, so they add to 180°: 180° %s %d° = <b>%d°</b>." % (MINUS, a, ans)
    elif kind == "scissors":
        a = r.randint(20, 70)
        q = "The blades of an open pair of scissors cross like two lines. The angle between the blades is %s. What is the angle between the two handles?" % dg(a)
        ans, wr = a, [180 - a, 90 - a, 2 * a]
        e = "The angle between the handles is across from the angle between the blades. Vertical angles are congruent: <b>%d°</b>." % a
    elif kind == "fold":
        a = r.randint(20, 80) * 2
        q = ("%s folds a paper corner so that the crease bisects an angle of %s. What is the measure of each of the two angles formed?" % (nm, dg(a)))
        ans, wr = a // 2, [a, 180 - a, 90 - a // 2]
        e = "A bisector splits the angle into two equal angles: %d° ÷ 2 = <b>%d°</b>." % (a, ans)
    elif kind == "ratio":
        p, s_ = r.choice([(1, 2), (2, 3), (1, 4), (4, 5), (1, 5), (2, 7), (3, 7), (7, 11), (1, 3), (5, 13)])
        tot = r.choice([90, 180])
        if tot % (p + s_):
            return None
        u = tot // (p + s_)
        word = "complementary" if tot == 90 else "supplementary"
        q = "Two angles are %s, and their measures are in the ratio %d : %d. Find the measure of the larger angle." % (word, p, s_)
        ans = s_ * u
        other = 180 if tot == 90 else 90
        wr = [p * u, s_ * other // (p + s_) if other % (p + s_) == 0 else ans + 10, ans - u]
        e = "%s angles add to %d°. Split %d° into %d parts: %d ÷ %d = %d° per part. Larger angle = %d × %d° = <b>%d°</b>." % (
            word.capitalize(), tot, tot, p + s_, tot, p + s_, u, s_, u, ans)
    elif kind == "clock":
        h = r.choice([1, 2, 4, 5])
        a = 30 * h
        q = "At %d:00, the hands of a clock form an angle of %s. What is the supplement of this angle?" % (h, dg(a))
        ans, wr = 180 - a, [90 - a if a < 90 else a - 90, 360 - a, a]
        e = "Supplementary angles add to 180°: 180° %s %d° = <b>%d°</b>." % (MINUS, a, ans)
    else:
        items = [("Vertical angles are always congruent.", "Always true", "Vertical angles are formed by two crossing lines and always have equal measures."),
                 ("A linear pair of angles is complementary.", "Never true", "A linear pair adds to 180°, not 90°. It is supplementary."),
                 ("Two acute angles are complementary.", "Sometimes true", "Only if they add to 90°, like 30° and 60°. 30° and 40° are not."),
                 ("Two supplementary angles form a linear pair.", "Sometimes true", "They also need to be adjacent (side by side). Two separate angles can add to 180°."),
                 ("The supplement of an acute angle is obtuse.", "Always true", "180° minus an angle less than 90° is more than 90°."),
                 ("Two right angles are supplementary.", "Always true", "90° + 90° = 180°."),
                 ("An obtuse angle has a complement.", "Never true", "An obtuse angle is more than 90°, so nothing positive adds to it to make 90°.")]
        s, right, why = r.choice(items)
        return T("Is this statement always, sometimes, or never true? %s" % B(s), right,
                 [x for x in ["Always true", "Sometimes true", "Never true", "Only for right angles"] if x != right], why + " <b>%s</b>." % right)
    wr = [w for w in dict.fromkeys(wr) if w != ans and w > 0] + [ans + 10, ans - 5]
    return T(q, dg(ans), [dg(w) for w in dict.fromkeys(wr) if w != ans and w > 0][:3], e)


def build():
    sets = [S("Angle Addition Postulate", collect(one_add, 20, R)),
            S("Angle addition and bisectors with algebra", collect(one_alg, 20, R)),
            S("Complementary and supplementary angles", collect(one_comp, 20, R)),
            S("Vertical angles and linear pairs", collect(one_vert, 20, R)),
            S("Word problems and reasoning", collect(one_word, 20, R))]
    body = lesson(
        "<p><b>Angle Addition Postulate</b>: if D is inside %sABC, then m%sABD + m%sDBC = m%sABC. "
        "An <b>angle bisector</b> splits an angle into two congruent angles.</p>"
        "<ul><li><b>Complementary</b> angles add to 90°. <b>Supplementary</b> angles add to 180°.</li>"
        "<li>A <b>linear pair</b> is two adjacent angles on a straight line. They are supplementary.</li>"
        "<li><b>Vertical angles</b> are across from each other where two lines cross. They are congruent.</li></ul>" % (ANG, ANG, ANG, ANG),
        [("Two angles form a linear pair. One is (3<i>x</i> + 20)° and the other is (2<i>x</i> + 10)°. Find both angles.",
          ["A linear pair adds to 180: 5<i>x</i> + 30 = 180", "<i>x</i> = 30", "3(30) + 20 = 110 and 2(30) + 10 = 70"], "110° and 70°"),
         ("An angle is 10° more than its complement. Find the angle.",
          ["Complement = <i>x</i>, angle = <i>x</i> + 10", "<i>x</i> + <i>x</i> + 10 = 90, so <i>x</i> = 40"], "50°")],
        ["Mixing up the totals. Complementary is 90° (C comes before S, 90 before 180).",
         "Setting a linear pair equal. Linear pairs add to 180°; only vertical angles are equal.",
         "Stopping at <i>x</i> when the question asks for an angle measure.",
         "Thinking any two angles that add to 180° form a linear pair. They must also be adjacent."])
    faq = [("What is the difference between complementary and supplementary angles?",
            "Complementary angles add to 90 degrees. Supplementary angles add to 180 degrees."),
           ("Are vertical angles always congruent?", "Yes. When two lines intersect, the angles across from each other always have equal measures."),
           ("What is a linear pair?", "Two adjacent angles whose outer sides form a straight line. A linear pair always adds to 180 degrees."),
           ("What is the Angle Addition Postulate?",
            "If a point D is in the interior of angle ABC, then the measure of angle ABD plus the measure of angle DBC equals the measure of angle ABC.")]
    make("angle-pairs", 4, "G-CO.C.9",
         "Angle Pairs: Complementary, Supplementary, and Vertical Angles",
         "Angle Pairs Worksheet: Complementary, Supplementary, Vertical Angles (Geometry) | 100 Questions",
         "Angle Pairs",
         "Prove theorems about lines and angles. Theorems include: vertical angles are congruent; when a transversal crosses parallel lines, alternate interior angles are congruent and corresponding angles are congruent; points on a perpendicular bisector of a line segment are exactly those equidistant from the segment's endpoints.",
         "Free Geometry worksheet on angle pairs: the Angle Addition Postulate, bisectors, complementary and supplementary angles, vertical angles and linear pairs. 100 questions with answers.",
         "Complementary angles add to 90°. Supplementary angles add to 180°.",
         "Vertical angles are congruent. A linear pair adds to 180°.",
         body, faq, sets, R, domain="Foundations of Geometry", grade="geometry")


if __name__ == "__main__":
    build()
