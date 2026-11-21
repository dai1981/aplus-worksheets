# -*- coding: utf-8 -*-
"""
India Class 9 Maths, NCERT Chapter 9: Circles (CBSE Unit IV Geometry)
  python3 tools/gen_in_maths_c9_circles.py
Chords: the perpendicular from the centre bisects a chord, distances of chords from the centre, equal chords are equidistant
and subtend equal angles; angles: the angle at the centre is double the angle at the circumference, angles in the same
segment and in a semicircle, cyclic quadrilaterals. Uses SG Secondary 3 makers (with figures); tangent questions are left
out (they are in Class 10).
Wrong answers come from real mistakes: taking the half chord as the whole chord, the angle at the circumference taken as
double the angle at the centre, opposite angles of a cyclic quadrilateral taken as equal, and adding the radius and distance.
"""
import random
from in_common import S, make, lesson, mix, T, adopt, gb
import gen_sg_maths_s3_symmetry_properties_of_circles as sym
import gen_sg_maths_s3_angle_properties_of_circles as ang

R = random.Random(909009)
adopt(sym, R)



def notan(fn):
    g = gb(fn)

    def f(r):
        for _ in range(30):
            it = g(r)
            if it and "tangent" not in (it["q"] + it["e"] + " ".join(it["c"])).lower():
                return it
        return None
    f.__name__ = fn.__name__
    return f


FACTS = [
    ("Equal chords of a circle subtend ___ angles at the centre.", "equal", ["supplementary", "complementary", "right"]),
    ("The perpendicular from the centre of a circle to a chord ___ the chord.", "bisects", ["is equal to", "is parallel to", "doubles"]),
    ("The line drawn through the centre of a circle to bisect a chord is ___ to the chord.", "perpendicular", ["parallel", "equal", "tangent"]),
    ("There is one and only one circle passing through ___ given non-collinear points.", "three", ["two", "four", "any number of"]),
    ("Equal chords of a circle are ___ from the centre.", "equidistant", ["at different distances", "always 1 cm", "parallel"]),
    ("The angle subtended by an arc at the centre is ___ the angle subtended by it at any point on the remaining part of the circle.", "double", ["half", "equal to", "supplementary to"]),
    ("Angles in the same segment of a circle are", "equal", ["supplementary", "complementary", "always 90°"]),
    ("The sum of either pair of opposite angles of a cyclic quadrilateral is", "180°", ["90°", "360°", "equal to the other pair"]),
    ("The angle in a semicircle is", "a right angle", ["an acute angle", "an obtuse angle", "a straight angle"]),
    ("A quadrilateral whose four vertices lie on a circle is called", "a cyclic quadrilateral", ["a kite", "a trapezium", "a rhombus"]),
    ("The longest chord of a circle is", "a diameter", ["a radius", "an arc", "a segment"]),
    ("Through two given points, how many circles can be drawn?", "Infinitely many", ["Exactly one", "Exactly two", "None"]),
    ("If two chords of a circle are equidistant from the centre, they are", "equal", ["parallel", "perpendicular", "diameters"]),
    ("If the angles subtended by two chords at the centre are equal, the chords are", "equal", ["parallel", "perpendicular", "unequal"]),
]


def one_fact(r):
    q, a, w = r.choice(FACTS)
    q = q if ("___" in q or q.endswith("?")) else q + " ___."
    return T(q, a, w, "<b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        S("Chords and the perpendicular from the centre", mix(R, [(gb(sym.one_chord), 12), (gb(sym.one_dist), 8)], seen)),
        S("Equal chords and circle facts", mix(R, [(notan(sym.one_equal), 10), (one_fact, 10)], seen)),
        S("Angle at the centre", mix(R, [(gb(ang.one_centre), 20)], seen)),
        S("Angles in the same segment and in a semicircle", mix(R, [(gb(ang.one_same), 12), (notan(ang.one_semi), 8)], seen)),
        S("Cyclic quadrilaterals and problems", mix(R, [(gb(ang.one_cyc), 14), (notan(ang.one_mix), 6)], seen)),
    ]
    body = lesson(
        "<p><b>Chords</b>: the perpendicular from the centre to a chord bisects it, so half chord² + distance² = radius². Equal chords are equidistant from the centre and subtend equal angles at the centre.</p>"
        "<p><b>Angles</b>: the angle subtended by an arc at the centre is double the angle it subtends at any point on the rest of the circle. Angles in the same segment are equal; the angle in a semicircle is 90°.</p>"
        "<p>In a <b>cyclic quadrilateral</b> each pair of opposite angles adds up to 180°.</p>",
        [("A chord is 8 cm from the centre of a circle of radius 10 cm. Find its length.", ["Half chord = √(10² − 8²) = 6"], "12 cm"),
         ("ABCD is cyclic and ∠A = 75°. Find ∠C.", ["Opposite angles add up to 180°"], "105°")],
        ["Forgetting to double the half chord found by Pythagoras.",
         "Making the angle at the circumference double the angle at the centre. It is half.",
         "Taking the opposite angles of a cyclic quadrilateral as equal. They add up to 180°."])
    faq = [
        ("What is the perpendicular bisector property of a chord?", "The perpendicular from the centre to a chord bisects the chord, and the line from the centre to the mid-point of a chord is perpendicular to it."),
        ("What is the relation between the angle at the centre and at the circumference?", "The angle at the centre is double the angle subtended by the same arc at any point on the remaining part of the circle."),
        ("What is a cyclic quadrilateral?", "A quadrilateral whose vertices all lie on a circle. Its opposite angles add up to 180°."),
        ("How many circles pass through three non-collinear points?", "Exactly one."),
    ]
    make(9, "circles", 9, "IV", 9, "Circles: Chords and Angles", "circles",
         "Equal chords of a circle subtend equal angles at the centre and conversely; the perpendicular from the centre to a chord bisects the chord and conversely; equal chords are equidistant from the centre and conversely; the angle subtended by an arc at the centre is double the angle at any point on the remaining part of the circle; angles in the same segment are equal; the sum of either pair of opposite angles of a cyclic quadrilateral is 180° and its converse (summary of the CBSE syllabus)",
         "Class 9 Circles worksheet (NCERT Chapter 9): chords and distances from the centre, equal chords, angle at the centre, angles in the same segment and cyclic quadrilaterals. 100 questions with answers.",
         "Angle at the centre = 2 × angle at the circumference", "Cyclic quadrilateral: opposite angles add up to 180°.",
         body, faq, sets, R)


if __name__ == "__main__":
    main()
