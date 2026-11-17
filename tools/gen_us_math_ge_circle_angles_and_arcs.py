# -*- coding: utf-8 -*-
"""
US Geometry: Circle Angles, Arcs, and Tangents (Common Core G-C.A.2, G-C.A.3)
  python3 tools/gen_us_math_ge_circle_angles_and_arcs.py
Central angles and arcs, inscribed angles, inscribed quadrilaterals, tangent lines, and angles formed by
chords and secants.
Wrong answers come from real mistakes: giving an inscribed angle the full arc measure, doubling instead of
halving, adding opposite angles of an inscribed quadrilateral to 360°, and adding the arcs for an angle
outside the circle instead of subtracting.
"""
import math
import random
from us_hs import B, S, make, lesson, collect, T, fig, num, MINUS, People
from us_geo import Canvas, pol, RED, GREEN, BLUE

R = random.Random(93801)
O = (130, 130)
RAD = 100


def lin(a, b):
    s = ("" if a == 1 else num(a)) + "<i>x</i>"
    if b > 0:
        s += " + %s" % num(b)
    elif b < 0:
        s += " %s %s" % (MINUS, num(-b))
    return s


def P(d):
    return pol(O[0], O[1], RAD, d)


def arc_text(c, d1, d2, t, col=RED):
    m = (d1 + d2) / 2
    c.text(pol(O[0], O[1], RAD + 20, m), t, 13, col)


def central_fig(arc, lab_ang, lab_arc):
    c = Canvas()
    c.circle(O, RAD)
    a1 = 200
    a2 = a1 + arc
    A, Bp = P(a1), P(a2)
    c.seg(O, A)
    c.seg(O, Bp)
    c.dot(O, 3.5)
    for p, n, d in ((A, "A", a1), (Bp, "B", a2)):
        c.dot(p, 3.5)
        c.text(pol(O[0], O[1], RAD + 16, d), n, 15)
    c.text((O[0], O[1] - 16), "O", 14)
    if lab_ang:
        c.angle(O, A, Bp, "", r=20)
        c.angle_text(O, A, Bp, lab_ang, r=40, fs=13)
    if lab_arc:
        arc_text(c, a1, a2, lab_arc)
    return c.svg("circle O with central angle AOB")


def inscribed_fig(arc, lab_ang, lab_arc, diam=False):
    c = Canvas()
    c.circle(O, RAD)
    a1 = 230
    a2 = a1 + arc
    A, Bp = P(a1), P(a2)
    cpos = a1 - (360 - arc) / 2
    C = P(cpos)
    c.seg(C, A)
    c.seg(C, Bp)
    if diam:
        c.seg(A, Bp, w=1.5)
    c.dot(O, 3)
    for p, n, d in ((A, "A", a1), (Bp, "B", a2), (C, "C", cpos)):
        c.dot(p, 3.5)
        c.text(pol(O[0], O[1], RAD + 16, d), n, 15)
    c.text((O[0] + 8, O[1] - 8), "O", 13)
    if lab_ang:
        c.angle(C, A, Bp, "", r=22)
        c.angle_text(C, A, Bp, lab_ang, r=46, fs=13)
    if lab_arc:
        arc_text(c, a1, a2, lab_arc)
    return c.svg("circle O with inscribed angle ACB")


def quad_fig(labels):
    c = Canvas()
    c.circle(O, RAD)
    ds = [215, 320, 50, 140]
    pts = [P(d) for d in ds]
    c.poly(pts)
    for p, n, d in zip(pts, "ABCD", ds):
        c.text(pol(O[0], O[1], RAD + 16, d), n, 15)
    for i, n in enumerate("ABCD"):
        if labels.get(n):
            v, a, b = pts[i], pts[(i + 1) % 4], pts[(i - 1) % 4]
            c.angle(v, a, b, "", r=20)
            c.angle_text(v, a, b, labels[n], r=46, fs=13)
    return c.svg("quadrilateral ABCD inscribed in a circle")


def tangent_fig(lab_r, lab_t, lab_d, two=False):
    c = Canvas()
    Q = (O[0] + 230, O[1])
    c.circle(O, 80)
    ang = math.degrees(math.acos(80 / 230))
    T1 = pol(O[0], O[1], 80, ang)
    T2 = pol(O[0], O[1], 80, -ang)
    c.seg(Q, T1)
    if two:
        c.seg(Q, T2)
    c.seg(O, T1, col=BLUE)
    c.seg(O, Q, dash=True, w=1.8)
    c.right(T1, O, Q)
    c.dot(O, 3.5)
    c.text((O[0] - 14, O[1] + 4), "O", 14)
    c.text((T1[0], T1[1] - 16), "A", 15)
    c.text((Q[0] + 14, Q[1] + 4), "P", 15)
    if two:
        c.text((T2[0], T2[1] + 18), "B", 15)
    if lab_r:
        c.text(((O[0] + T1[0]) / 2 - 12, (O[1] + T1[1]) / 2), lab_r, 13, BLUE, anchor="end")
    if lab_t:
        c.text(((T1[0] + Q[0]) / 2 + 8, (T1[1] + Q[1]) / 2 - 12), lab_t, 13)
    if lab_d:
        c.text(((O[0] + Q[0]) / 2 + 30, O[1] + 16), lab_d, 13)
    return c.svg("circle O with tangent from point P")


# ------------------------------------------------------------ set 1: central angles and arcs
def one_central(r):
    a = r.choice(range(40, 165, 5))
    kind = r.choice(["arc", "major", "ang", "semi", "alg"])
    if kind == "arc":
        q = "m∠AOB = %d°. Find the measure of minor arc AB.%s" % (a, fig(central_fig(a, "%d°" % a, "?")))
        return T(q, "%d°" % a, ["%d°" % w for w in [a // 2 if a % 2 == 0 else a + 5, 2 * a if 2 * a < 360 else a + 10, 360 - a]],
                 "A minor arc has the same measure as its central angle: <b>%d°</b>." % a)
    if kind == "major":
        q = "m∠AOB = %d°. Find the measure of the major arc from A to B (the long way around).%s" % (a, fig(central_fig(a, "%d°" % a, "")))
        return T(q, "%d°" % (360 - a), ["%d°" % w for w in [a, 180 - a, 2 * a if 2 * a != 360 - a else a + 20]],
                 "A whole circle is 360°. Major arc = 360° %s %d° = <b>%d°</b>." % (MINUS, a, 360 - a))
    if kind == "ang":
        q = "Minor arc AB measures %d°. Find m∠AOB.%s" % (a, fig(central_fig(a, "?", "%d°" % a)))
        return T(q, "%d°" % a, ["%d°" % w for w in [a // 2 if a % 2 == 0 else a + 5, 360 - a, 180 - a]],
                 "A central angle has the same measure as its arc: <b>%d°</b>." % a)
    if kind == "semi":
        b = r.choice(range(30, 150, 5))
        q = "<span class='ov'>AB</span> is a diameter, and point C is on the circle with arc AC = %d°. Find arc CB (the part of the semicircle from C to B)." % b
        return T(q, "%d°" % (180 - b), ["%d°" % w for w in [360 - b, b, 90 - b if b < 90 else b - 90]],
                 "A diameter cuts the circle into two semicircles of 180°. 180° %s %d° = <b>%d°</b>." % (MINUS, b, 180 - b))
    x = r.randint(5, 25)
    k, d = r.randint(2, 6), r.randint(-10, 20)
    v = k * x + d
    if not (30 <= v <= 170):
        return None
    q = "m∠AOB = (%s)° and minor arc AB = %d°. Find <i>x</i>.%s" % (lin(k, d), v, fig(central_fig(v, lin(k, d) + "°", "%d°" % v)))
    bad = (2 * v - d) / k
    return T(q, num(x), [num(w) for w in dict.fromkeys([int(bad) if bad == int(bad) else x + 2, v, x + 1, (360 - v - d) // k if (360 - v - d) % k == 0 else x - 1]) if w != x and w > 0][:3],
             "The central angle equals its arc: %s = %d, so %d<i>x</i> = %d and <i>x</i> = <b>%d</b>." % (lin(k, d), v, k, v - d, x))


# ------------------------------------------------------------ set 2: inscribed angles
def one_insc(r):
    arc = r.choice(range(40, 172, 4))
    kind = r.choice(["ang", "ang", "arc", "semi", "alg"])
    if kind == "ang":
        q = "Find m∠ACB.%s" % fig(inscribed_fig(arc, "?", "%d°" % arc))
        return T(q, "%d°" % (arc // 2), ["%d°" % w for w in [arc, 2 * arc if 2 * arc < 360 else arc + 20, 180 - arc // 2]],
                 "An inscribed angle is half its intercepted arc: %d° ÷ 2 = <b>%d°</b>." % (arc, arc // 2))
    if kind == "arc":
        q = "m∠ACB = %d°. Find the measure of arc AB.%s" % (arc // 2, fig(inscribed_fig(arc, "%d°" % (arc // 2), "?")))
        return T(q, "%d°" % arc, ["%d°" % w for w in [arc // 2, arc // 4 if arc % 4 == 0 else arc + 6, 180 - arc // 2]],
                 "The intercepted arc is twice the inscribed angle: 2 × %d° = <b>%d°</b>." % (arc // 2, arc))
    if kind == "semi":
        q = "<span class='ov'>AB</span> is a diameter of the circle. Find m∠ACB.%s" % fig(inscribed_fig(180, "?", "", diam=True))
        return T(q, "90°", ["180°", "45°", "60°"], "An angle inscribed in a semicircle intercepts a 180° arc, so it is 180° ÷ 2 = <b>90°</b>.")
    x = r.randint(4, 20)
    k, d = r.randint(2, 6), r.randint(-10, 20)
    ang = k * x + d
    if not (20 <= ang <= 85):
        return None
    q = "m∠ACB = (%s)° and arc AB = %d°. Find <i>x</i>.%s" % (lin(k, d), 2 * ang, fig(inscribed_fig(2 * ang, lin(k, d) + "°", "%d°" % (2 * ang))))
    bad = (2 * ang - d) / k
    return T(q, num(x), [num(w) for w in dict.fromkeys([int(bad) if bad == int(bad) else x + 2, ang, x + 1, 2 * x]) if w != x and w > 0][:3],
             "The inscribed angle is half the arc: %s = %d ÷ 2 = %d, so %d<i>x</i> = %d and <i>x</i> = <b>%d</b>." % (lin(k, d), 2 * ang, ang, k, ang - d, x))


# ------------------------------------------------------------ set 3: inscribed quadrilaterals
def one_quad(r):
    a, b = r.randint(60, 120), r.randint(60, 120)
    if a == 90 or b == 90:
        return None
    kind = r.choice(["opp", "opp", "alg", "alg"])
    if kind == "opp":
        v = r.choice("ABCD")
        opp = {"A": "C", "B": "D", "C": "A", "D": "B"}[v]
        q = "Quadrilateral ABCD is inscribed in the circle. Find m∠%s.%s" % (opp, fig(quad_fig({v: "%d°" % a, opp: "?"})))
        return T(q, "%d°" % (180 - a), ["%d°" % w for w in [a, 360 - a, 90 - a if a < 90 else a - 90]],
                 "Opposite angles of an inscribed quadrilateral are supplementary: 180° %s %d° = <b>%d°</b>." % (MINUS, a, 180 - a))
    x = r.randint(5, 20)
    k1, k2 = r.randint(2, 6), r.randint(1, 5)
    d1 = a - k1 * x
    d2 = 180 - a - k2 * x
    if abs(d1) > 40 or abs(d2) > 40:
        return None
    ask = r.choice(["x", "ang"])
    q = "Quadrilateral ABCD is inscribed in the circle. m∠A = (%s)° and m∠C = (%s)°. %s%s" % (
        lin(k1, d1), lin(k2, d2), "Find <i>x</i>." if ask == "x" else "Find m∠A.", fig(quad_fig({"A": lin(k1, d1) + "°", "C": lin(k2, d2) + "°"})))
    steps = "∠A and ∠C are opposite, so they add to 180°: (%s) + (%s) = 180, %d<i>x</i> = %d, <i>x</i> = %d." % (lin(k1, d1), lin(k2, d2), k1 + k2, 180 - d1 - d2, x)
    if ask == "x":
        bad = (d2 - d1) / (k1 - k2) if k1 != k2 else None
        return T(q, num(x), [num(w) for w in dict.fromkeys([int(bad) if bad and bad == int(bad) and bad > 0 else x + 2, a, x + 1, (360 - d1 - d2) // (k1 + k2)]) if w != x and w > 0][:3],
                 steps.replace("<i>x</i> = %d." % x, "<i>x</i> = <b>%d</b>." % x))
    return T(q, "%d°" % a, ["%d°" % w for w in dict.fromkeys([180 - a, x, a + 10]) if w != a][:3], steps + " m∠A = %d(%d) %s %d = <b>%d°</b>." % (k1, x, "+" if d1 >= 0 else MINUS, abs(d1), a))


# ------------------------------------------------------------ set 4: tangents
def one_tan(r):
    kind = r.choice(["len", "len", "dist", "two", "two_alg"])
    a, b, c_ = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10), (9, 12, 15), (7, 24, 25), (12, 16, 20), (20, 21, 29)])
    if kind == "len":
        q = "<span class='ov'>PA</span> is tangent to circle O at A. OA = %d and OP = %d. Find PA.%s" % (a, c_, fig(tangent_fig(num(a), "?", num(c_))))
        return T(q, num(b), [num(c_ - a), num(c_ + a), num(round(math.sqrt(a * a + c_ * c_), 1)) if False else "√%d" % (a * a + c_ * c_)],
                 "A tangent is perpendicular to the radius at the point of tangency, so △OAP is a right triangle with hypotenuse OP. PA = √(%d² %s %d²) = <b>%d</b>." % (c_, MINUS, a, b))
    if kind == "dist":
        q = "<span class='ov'>PA</span> is tangent to circle O at A. OA = %d and PA = %d. Find OP.%s" % (a, b, fig(tangent_fig(num(a), num(b), "?")))
        return T(q, num(c_), [num(a + b), num(b - a) if b > a else num(a - b + 2), "√%d" % (b * b - a * a) if b > a else num(c_ + 2)],
                 "OA ⟂ PA, so OP is the hypotenuse: √(%d² + %d²) = <b>%d</b>." % (a, b, c_))
    if kind == "two":
        t = r.randint(5, 25)
        q = "<span class='ov'>PA</span> and <span class='ov'>PB</span> are tangent to circle O. PA = %d. Find PB.%s" % (t, fig(tangent_fig("", num(t), "", two=True)))
        return T(q, num(t), [num(2 * t), num(t // 2) if t % 2 == 0 else num(t + 1), num(t + 5)],
                 "Two tangent segments from the same outside point are congruent: PB = PA = <b>%d</b>." % t)
    x = r.randint(2, 12)
    k1, k2 = r.sample(range(1, 7), 2)
    d1 = r.randint(-5, 12)
    v = k1 * x + d1
    d2 = v - k2 * x
    if v < 4 or abs(d2) > 30:
        return None
    diff = abs(k1 - k2)
    q = "<span class='ov'>PA</span> and <span class='ov'>PB</span> are tangent to circle O. PA = %s and PB = %s. Find PA." % (lin(k1, d1), lin(k2, d2))
    e = "Tangent segments from one point are congruent: %s = %s, so %s<i>x</i> = %d and <i>x</i> = %d. PA = <b>%d</b>." % (lin(k1, d1), lin(k2, d2), num(diff) if diff > 1 else "", abs(d2 - d1), x, v)
    e = e.replace(", so <i>x</i> = %d and <i>x</i> = " % abs(d2 - d1), ", so <i>x</i> = ")
    return T(q, num(v), [num(w) for w in dict.fromkeys([x, 2 * v, v + diff]) if w != v][:3] + ([num(v + 3)] if len({x, 2 * v, v + diff} - {v}) < 3 else []), e)


# ------------------------------------------------------------ set 5: chords and secants
def one_sec(r):
    kind = r.choice(["in", "in", "out", "out", "tf"])
    a, b = r.choice(range(30, 150, 2)), r.choice(range(20, 130, 2))
    if kind == "in":
        if a + b >= 360:
            return None
        q = "Two chords intersect inside a circle. The arcs intercepted by the angle and its vertical angle measure %d° and %d°. Find the angle." % (a, b)
        ans = (a + b) // 2
        return T(q, "%d°" % ans, ["%d°" % w for w in dict.fromkeys([a + b, abs(a - b) // 2, 180 - ans]) if w != ans][:3],
                 "An angle formed by two chords is half the sum of the intercepted arcs: (%d° + %d°) ÷ 2 = <b>%d°</b>." % (a, b, ans))
    if kind == "out":
        big, small = max(a, b) + 40, min(a, b)
        if big + small >= 360 or big == small:
            return None
        q = "Two secants meet outside a circle. The far arc is %d° and the near arc is %d°. Find the angle between the secants." % (big, small)
        ans = (big - small) // 2
        return T(q, "%d°" % ans, ["%d°" % w for w in dict.fromkeys([(big + small) // 2, big - small, big // 2]) if w != ans][:3],
                 "An angle outside the circle is half the difference of the intercepted arcs: (%d° %s %d°) ÷ 2 = <b>%d°</b>." % (big, MINUS, small, ans))
    items = [("A tangent and a radius meet at the point of tangency. What angle do they form?", "90°", ["45°", "180°", "It depends on the circle"],
              "A tangent line is always perpendicular to the radius drawn to the point of tangency."),
             ("Two inscribed angles intercept the same arc. How are they related?", "They are congruent", ["They are supplementary", "One is twice the other", "They are complementary"],
              "Each is half of the same arc, so they are equal."),
             ("A triangle is inscribed in a circle, and one side is a diameter. What kind of triangle is it?", "A right triangle", ["An equilateral triangle", "An obtuse triangle", "An isosceles triangle"],
              "The angle opposite the diameter is inscribed in a semicircle, so it is 90°."),
             ("Which quadrilateral can always be inscribed in a circle?", "A rectangle", ["A rhombus", "A parallelogram", "A kite"],
              "A quadrilateral can be inscribed when opposite angles are supplementary. A rectangle has 90° + 90° = 180°."),
             ("A central angle and an inscribed angle intercept the same arc. The central angle is 110°. What is the inscribed angle?", "55°", ["110°", "220°", "70°"],
              "The arc is 110°, and the inscribed angle is half of it."),
             ("How many tangent lines can be drawn to a circle from a point outside it?", "Two", ["One", "None", "Infinitely many"],
              "From an outside point there are exactly two tangent lines, and the two tangent segments are congruent.")]
    q, right, wr, e = r.choice(items)
    return T(q, right, wr, e + " <b>%s</b>." % right)


def build():
    sets = [S("Central angles and arcs", collect(one_central, 20, R)),
            S("Inscribed angles", collect(one_insc, 20, R)),
            S("Inscribed quadrilaterals", collect(one_quad, 20, R)),
            S("Tangent lines", collect(one_tan, 20, R)),
            S("Chords, secants and reasoning", collect(one_sec, 20, R))]
    body = lesson(
        "<ul><li>A <b>central angle</b> (vertex at the center) equals its arc. A circle is 360°, and a semicircle is 180°.</li>"
        "<li>An <b>inscribed angle</b> (vertex on the circle) is <b>half</b> its intercepted arc. An angle inscribed in a semicircle is 90°.</li>"
        "<li>Opposite angles of an <b>inscribed quadrilateral</b> are supplementary.</li>"
        "<li>A <b>tangent</b> is perpendicular to the radius at the point of tangency. Two tangent segments from the same outside point are congruent.</li>"
        "<li>Two chords crossing inside: angle = ½(sum of arcs). Secants or tangents meeting outside: angle = ½(difference of arcs).</li></ul>",
        [("An inscribed angle intercepts a 124° arc. Find the angle.", ["Half of 124°"], "62°"),
         ("PA is tangent to circle O at A, OA = 6 and OP = 10. Find PA.", ["∠OAP = 90°", "PA = √(100 %s 36)" % MINUS], "8")],
        ["Giving an inscribed angle the same measure as its arc. Halve the arc.",
         "Halving a central angle. Only inscribed angles are half the arc.",
         "Adding opposite angles of an inscribed quadrilateral to 360°. They add to 180°.",
         "Adding the arcs for an angle outside the circle. Subtract them, then halve."])
    faq = [("What is the inscribed angle theorem?", "An inscribed angle is half the measure of its intercepted arc."),
           ("What is the difference between a central angle and an inscribed angle?",
            "A central angle has its vertex at the center and equals its arc. An inscribed angle has its vertex on the circle and is half its arc."),
           ("Why is a tangent perpendicular to the radius?", "The radius to the point of tangency is the shortest distance from the center to the tangent line, and the shortest segment to a line is perpendicular."),
           ("What are the angles of a quadrilateral inscribed in a circle?", "Opposite angles are supplementary: they add to 180 degrees.")]
    make("circle-angles-and-arcs", 18, "G-C.A.2",
         "Circle Angles, Arcs, and Tangents",
         "Circle Angles Worksheet: Central, Inscribed Angles and Tangents (Geometry, G-C.A.2) | 100 Questions",
         "Circle Angles and Arcs",
         "Identify and describe relationships among inscribed angles, radii, and chords. Include the relationship between central, inscribed, and circumscribed angles; inscribed angles on a diameter are right angles; the radius of a circle is perpendicular to the tangent where the radius intersects the circle.",
         "Free Geometry worksheet on circle angles: central and inscribed angles, arcs, inscribed quadrilaterals, tangents, chords and secants. 100 questions with answers.",
         "An inscribed angle is half its arc. A central angle equals its arc.",
         "A tangent is perpendicular to the radius. Opposite angles of an inscribed quadrilateral add to 180°.",
         body, faq, sets, R, domain="Circles", grade="geometry")


if __name__ == "__main__":
    build()
