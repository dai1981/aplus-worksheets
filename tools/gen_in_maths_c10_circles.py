# -*- coding: utf-8 -*-
"""
India Class 10 Maths, NCERT Chapter 10: Circles — Tangents (CBSE Unit IV Geometry)
  python3 tools/gen_in_maths_c10_circles.py
Tangent and secant, number of tangents from a point, the tangent is perpendicular to the radius (tangent length with
Pythagoras), tangents from an external point are equal (angles between tangents, SG Secondary 3 makers with figures),
quadrilaterals and triangles circumscribing a circle, concentric circles and problems.
Wrong answers come from real mistakes: OT − r for the tangent length, ∠AOB = ∠ATB, one tangent from an external point,
AB + BC = CD + DA (wrong pairs), and the chord of the larger circle as twice the radius difference.
"""
import random, math
from in_common import num, S, make, lesson, mix, T, QN, People, adopt
import gen_sg_maths_s3_symmetry_properties_of_circles as sgs

R = random.Random(910010)
P = People(R)
adopt(sgs, R)
TRIP = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15), (12, 16, 20), (20, 21, 29), (9, 40, 41), (12, 5, 13), (4, 3, 5), (15, 8, 17)]


# ---------------------------------------------------------------- set 1: tangents and secants
BASICS = [
    ("How many tangents can a circle have?", "Infinitely many", ["One", "Two", "Four"], "A tangent can be drawn at every point of the circle."),
    ("How many tangents can be drawn to a circle from a point outside it?", "Two", ["One", "None", "Infinitely many"], "From an external point there are exactly two tangents."),
    ("How many tangents can be drawn to a circle from a point on the circle?", "One", ["Two", "None", "Infinitely many"], "At a point on the circle there is exactly one tangent."),
    ("How many tangents can be drawn to a circle from a point inside it?", "None", ["One", "Two", "Infinitely many"], "Every line through an inside point cuts the circle twice, so there is no tangent."),
    ("A line that meets a circle at exactly one point is called a", "tangent", ["secant", "chord", "diameter"], "A tangent touches the circle at one point (the point of contact)."),
    ("A line that meets a circle at two points is called a", "secant", ["tangent", "radius", "normal"], "A secant cuts the circle at two points."),
    ("How many parallel tangents can a circle have at most?", "Two", ["One", "Three", "Infinitely many"], "Parallel tangents are drawn at the two ends of a diameter."),
    ("The tangent at any point of a circle is ___ to the radius through the point of contact.", "perpendicular", ["parallel", "equal", "half of"], "Theorem 10.1: the tangent is perpendicular to the radius."),
    ("The lengths of the tangents drawn from an external point to a circle are", "equal", ["unequal", "equal to the radius", "equal to the diameter"], "Theorem 10.2: tangents from an external point are equal."),
    ("The tangents drawn at the ends of a diameter of a circle are", "parallel", ["perpendicular", "equal to the diameter", "intersecting at the centre"], "Both are perpendicular to the same diameter, so they are parallel."),
    ("The point where a tangent touches a circle is called the", "point of contact", ["centre", "external point", "point of secancy"], "It is the only common point of the tangent and the circle."),
    ("The line through the point of contact perpendicular to the tangent passes through the", "centre", ["external point", "end of a chord", "midpoint of the tangent"], "That line contains the radius, so it passes through the centre."),
]


def one_basic(r):
    if r.random() < 0.45:
        q, a, w, e = r.choice(BASICS)
        return T(q if q.endswith("?") or "___" in q else q + " ___.", a, w, e + " <b>%s</b>." % a)
    a, b, h = r.choice(TRIP)
    kind = r.choice(["len", "rad"])
    if kind == "len":
        return QN("A tangent PQ is drawn at the point P of a circle with centre O and radius %d cm. A point Q on the tangent is %d cm from O. Find PQ." % (a, h), b,
                  [h - a, int(round(math.hypot(a, h))), h + a], "OP ⟂ PQ, so PQ = √(OQ² − OP²) = √(%d² − %d²) = <b>%d cm</b>." % (h, a, b), unit=" cm")
    return QN("From a point Q, the length of the tangent to a circle is %d cm and the distance of Q from the centre is %d cm. Find the radius of the circle." % (b, h), a,
              [h - b, int(round(math.hypot(b, h))), b], "The radius is perpendicular to the tangent: r = √(%d² − %d²) = <b>%d cm</b>." % (h, b, a), unit=" cm")


# ---------------------------------------------------------------- set 2: tangent length (with figures)
def one_len(r):
    a, b, h = r.choice(TRIP)
    k = r.choice([1, 1, 2])
    a, b, h = a * k, b * k, h * k
    t = 2 * math.degrees(math.asin(a / h))
    kind = r.choice(["len", "dist", "rad"])
    if kind == "len":
        pic = sgs.tangent_fig(t, {"OA": "%d" % a})
        return QN("TA and TB are tangents to the circle with centre O. The radius is %d cm and OT = %d cm. Find TA.%s" % (a, h, pic), b, [h - a, int(round(math.hypot(a, h))), h + a],
                  "∠OAT = 90° (tangent ⟂ radius). TA = √(%d² − %d²) = <b>%d cm</b>." % (h, a, b), unit=" cm")
    if kind == "dist":
        pic = sgs.tangent_fig(t, {"OA": "%d" % a, "TA": "%d" % b})
        return QN("TA is a tangent to the circle with centre O. OA = %d cm and TA = %d cm. Find OT.%s" % (a, b, pic), h, [a + b, int(round(math.sqrt(abs(b * b - a * a)))) if b != a else b, b],
                  "∠OAT = 90°, so OT = √(%d² + %d²) = <b>%d cm</b>." % (a, b, h), unit=" cm")
    pic = sgs.tangent_fig(t, {"TA": "%d" % b})
    return QN("TA is a tangent to the circle with centre O. TA = %d cm and OT = %d cm. Find the radius.%s" % (b, h, pic), a, [h - b, int(round(math.hypot(b, h))), b],
              "∠OAT = 90°, so OA = √(%d² − %d²) = <b>%d cm</b>." % (h, b, a), unit=" cm")


# ---------------------------------------------------------------- set 4: circumscribing figures
def one_circ(r):
    kind = r.choice(["quad", "quad", "tri", "tri", "para"])
    if kind == "quad":
        p, q, s, t = [r.randint(2, 9) for _ in range(4)]   # tangent lengths from A, B, C, D
        AB, BC, CD, DA = p + q, q + s, s + t, t + p
        miss = r.choice(["AB", "BC", "CD", "DA"])
        vals = {"AB": AB, "BC": BC, "CD": CD, "DA": DA}
        given = ", ".join("%s = %d cm" % (k, v) for k, v in vals.items() if k != miss)
        ans = vals[miss]
        return QN("A quadrilateral ABCD is drawn to circumscribe a circle. %s. Find %s." % (given, miss), ans,
                  [sum(v for k, v in vals.items() if k != miss) - 2 * ans if sum(v for k, v in vals.items() if k != miss) - 2 * ans > 0 else ans + 3,
                   vals[{"AB": "CD", "BC": "DA", "CD": "AB", "DA": "BC"}[miss]],
                   ans + 2],
                  "Tangents from each vertex are equal, so AB + CD = AD + BC. %s = <b>%d cm</b>." % (miss, ans), unit=" cm")
    if kind == "tri":
        x, y, z = [r.randint(2, 12) for _ in range(3)]   # tangent lengths from A, B, C
        AB, BC, CA = x + y, y + z, z + x
        want = r.choice(["A", "B", "C"])
        v = {"A": x, "B": y, "C": z}[want]
        return QN("A circle is inscribed in △ABC, touching AB, BC and CA. AB = %d cm, BC = %d cm and CA = %d cm. Find the length of the tangent from %s to the circle." % (AB, BC, CA, want), v,
                  [{"A": BC, "B": CA, "C": AB}[want] // 2 if {"A": BC, "B": CA, "C": AB}[want] // 2 != v else v + 1, (AB + BC + CA) // 2, abs({"A": AB - CA, "B": AB - BC, "C": CA - BC}[want]) if abs({"A": AB - CA, "B": AB - BC, "C": CA - BC}[want]) != v else v + 2],
                  "Let the tangent lengths from A, B, C be x, y, z: x + y = %d, y + z = %d, z + x = %d, so x + y + z = %d and the tangent from %s is <b>%d cm</b>." % (AB, BC, CA, (AB + BC + CA) // 2, want, v), unit=" cm")
    return T("A parallelogram circumscribes a circle. What kind of parallelogram must it be?", "A rhombus", ["A rectangle", "Any parallelogram", "A square only"],
             "AB + CD = AD + BC and opposite sides are equal, so 2AB = 2BC: all sides are equal. It is <b>a rhombus</b>.")


# ---------------------------------------------------------------- set 5: problems
def one_prob(r):
    kind = r.choice(["conc", "conc", "conc", "ext", "ang"])
    if kind == "conc":
        a, b, h = r.choice(TRIP)       # inner radius a, half chord b, outer radius h
        k = r.choice([1, 1, 2])
        a, b, h = a * k, b * k, h * k
        return QN("Two concentric circles have radii %d cm and %d cm. Find the length of the chord of the larger circle that touches the smaller circle." % (h, a), 2 * b,
                  [b, 2 * (h - a), h + a], "The chord is a tangent to the smaller circle, so it is perpendicular to the radius and bisected: half chord = √(%d² − %d²) = %d cm. Chord = <b>%d cm</b>." % (h, a, b, 2 * b), unit=" cm")
    if kind == "ang":
        t = r.choice([40, 50, 60, 70, 80, 100, 110, 120])
        return QN("Two tangents PA and PB are drawn to a circle with centre O from an external point P. If ∠AOB = %d°, find ∠APB." % (180 - t), t,
                  [180 - t, (180 - t) // 2, 90 - t // 2], "∠OAP = ∠OBP = 90°, so ∠APB = 360° − 90° − 90° − %d° = <b>%d°</b>." % (180 - t, t), unit="°")
    for _ in range(50):
        it = sgs.one_prob(r)
        if it and "tangent" in it["q"]:
            return it
    return None


def main():
    seen = set()
    sets = [
        S("Tangents and secants", mix(R, [(one_basic, 20)], seen)),
        S("Tangent ⟂ radius", mix(R, [(one_len, 20)], seen)),
        S("Tangents from an external point", mix(R, [(sgs.one_tan, 20)], seen)),
        S("Circles inside polygons", mix(R, [(one_circ, 20)], seen)),
        S("Problems", mix(R, [(one_prob, 20)], seen)),
    ]
    body = lesson(
        "<p>A <b>tangent</b> meets a circle at exactly one point, the point of contact. A secant meets it at two points.</p>"
        "<p>Theorem 10.1: the tangent at any point of a circle is <b>perpendicular to the radius</b> through the point of contact. So tangent length = √(OT² − r²).</p>"
        "<p>Theorem 10.2: the <b>tangents from an external point are equal</b>. The line from the external point to the centre bisects the angle between them, and ∠APB + ∠AOB = 180°.</p>",
        [("From Q, the tangent to a circle is 24 cm and OQ = 25 cm. Find the radius.", ["Radius ⟂ tangent", "r = √(25² − 24²) = √49"], "7 cm"),
         ("ABCD circumscribes a circle. AB = 6, BC = 7, CD = 4. Find AD.", ["AB + CD = AD + BC", "10 = AD + 7"], "AD = 3 cm")],
        ["Taking OT − r as the tangent length. Use Pythagoras: √(OT² − r²).",
         "Writing ∠AOB = ∠APB. They are supplementary: they add up to 180°.",
         "Using AB + BC = CD + DA for a circumscribed quadrilateral. The opposite sides add up: AB + CD = AD + BC."])
    faq = [
        ("What is a tangent to a circle?", "A line that meets the circle at exactly one point. That point is called the point of contact."),
        ("Why is the tangent perpendicular to the radius?", "The point of contact is the only point of the tangent on the circle; every other point is outside, so OP is the shortest distance from O to the line, and the shortest distance is the perpendicular."),
        ("How many tangents can be drawn from a point outside a circle?", "Exactly two, and they are equal in length."),
        ("What is true for a quadrilateral that circumscribes a circle?", "The sums of opposite sides are equal: AB + CD = AD + BC."),
    ]
    make(10, "circles", 10, "IV", 10, "Circles: Tangents to a Circle", "circles",
         "Tangent to a circle at the point of contact; the tangent at any point of a circle is perpendicular to the radius through the point of contact; the lengths of tangents drawn from an external point to a circle are equal (summary of the CBSE syllabus)",
         "Class 10 Circles worksheet (NCERT Chapter 10): tangents and secants, tangent ⟂ radius, equal tangents from an external point, circumscribed quadrilaterals and concentric circles. 100 questions with answers.",
         "Tangent ⟂ radius at the point of contact", "Tangents from an external point are equal.",
         body, faq, sets, R)


if __name__ == "__main__":
    main()
