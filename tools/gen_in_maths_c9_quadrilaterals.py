# -*- coding: utf-8 -*-
"""
India Class 9 Maths, NCERT Chapter 8: Quadrilaterals (CBSE Unit IV Geometry)
  python3 tools/gen_in_maths_c9_quadrilaterals.py
Angle sum of a quadrilateral, angles of a parallelogram, properties of parallelograms, rectangles, rhombuses and squares
(US Geometry makers with Indian wording), the Mid-point Theorem and its converse (US maker with NCERT names), and problems.
Wrong answers come from real mistakes: adjacent angles of a parallelogram taken as equal, diagonals of every parallelogram
taken as equal or perpendicular, the line joining mid-points taken as equal to the third side, and a sum of 180° for a quadrilateral.
"""
import random, re
from in_common import num, S, make, lesson, mix, T, QN, adopt, gb
import gen_us_math_ge_polygons_and_quadrilaterals as usq
import gen_us_math_ge_midsegments_and_triangle_centers as usm

R = random.Random(909008)
adopt(usq, R)
adopt(usm, R)


def mid(fn):
    g = gb(fn)

    def f(r):
        it = g(r)
        if not it:
            return None
        def fix(t):
            t = t.replace("Triangle Midsegment Theorem", "Mid-point Theorem")
            t = re.sub(r"\bmidsegments\b", "segments joining the mid-points", t)
            t = re.sub(r"\bmidsegment\b", "segment joining the mid-points", t)
            t = re.sub(r"\bmidpoints\b", "mid-points", t)
            return t
        it["q"], it["e"] = fix(it["q"]), fix(it["e"])
        it["c"] = [fix(c) for c in it["c"]]
        return it
    f.__name__ = fn.__name__
    return f


# ---------------------------------------------------------------- set 1: angles
def one_ang(r):
    kind = r.choice(["sum", "sum", "pg", "pg", "ratio", "adj"])
    if kind == "sum":
        a, b, c = r.randint(50, 130), r.randint(50, 130), r.randint(50, 130)
        d = 360 - a - b - c
        if not 30 <= d <= 170:
            return None
        return QN("Three angles of a quadrilateral are %d°, %d° and %d°. Find the fourth angle." % (a, b, c), d, [180 - (a + b + c) % 180, 360 - a - b, d + 10],
                  "The angles of a quadrilateral add up to 360°: 360° − %d° − %d° − %d° = <b>%d°</b>." % (a, b, c, d), unit="°")
    if kind == "pg":
        a = r.randint(35, 145)
        if a == 90:
            return None
        want = r.choice(["adj", "opp"])
        if want == "adj":
            return QN("In parallelogram ABCD, ∠A = %d°. Find ∠B." % a, 180 - a, [a, 360 - a, 90 - a if a < 90 else a - 90], "Adjacent angles of a parallelogram add up to 180°: ∠B = 180° − %d° = <b>%d°</b>." % (a, 180 - a), unit="°")
        return QN("In parallelogram PQRS, ∠P = %d°. Find ∠R." % a, a, [180 - a, 360 - a, a // 2], "Opposite angles of a parallelogram are equal: <b>∠R = %d°</b>." % a, unit="°")
    if kind == "ratio":
        p, q, s, t = r.choice([(3, 5, 9, 13), (1, 2, 3, 4), (2, 3, 4, 6), (1, 3, 5, 6), (3, 4, 5, 6), (2, 4, 5, 7), (1, 2, 4, 5)])
        if 360 % (p + q + s + t):
            return None
        k = 360 // (p + q + s + t)
        return T("The angles of a quadrilateral are in the ratio %d : %d : %d : %d. Find the largest angle." % (p, q, s, t), "%d°" % (t * k),
                 ["%d°" % (p * k), "%d°" % (t * 180 // (p + q + s + t)) if 180 % (p + q + s + t) == 0 else "%d°" % (t * k - 10), "%d°" % (t * 10)],
                 "%d parts = 360°, so 1 part = %d° and the largest angle is <b>%d°</b>." % (p + q + s + t, k, t * k))
    d = r.choice([10, 20, 30, 40, 50, 60])
    big = (180 + d) // 2
    return T("Two adjacent angles of a parallelogram differ by %d°. Find the larger one." % d, "%d°" % big, ["%d°" % (180 - big), "%d°" % (big + d), "%d°" % ((360 + d) // 2)],
             "x + (x − %d) = 180, so x = <b>%d°</b>." % (d, big))


# ---------------------------------------------------------------- set 5: problems
def one_prob(r):
    kind = r.choice(["diag", "diag", "perim", "rhom", "midq", "rect"])
    if kind == "diag":
        a, b = r.randint(4, 15), r.randint(4, 15)
        return T("The diagonals of parallelogram ABCD meet at O. AO = %d cm and BO = %d cm. Find AC and BD." % (a, b), "AC = %d cm, BD = %d cm" % (2 * a, 2 * b),
                 ["AC = %d cm, BD = %d cm" % (a, b), "AC = %d cm, BD = %d cm" % (2 * b, 2 * a) if a != b else "AC = %d cm, BD = %d cm" % (a + b, a + b), "AC = BD = %d cm" % (a + b)],
                 "The diagonals of a parallelogram bisect each other: <b>AC = %d cm, BD = %d cm</b>." % (2 * a, 2 * b))
    if kind == "perim":
        a, b = r.randint(3, 20), r.randint(3, 20)
        return QN("Two adjacent sides of a parallelogram are %d cm and %d cm. Find its perimeter." % (a, b), 2 * (a + b), [a + b, a * b, 4 * a], "Opposite sides are equal: 2(%d + %d) = <b>%d cm</b>." % (a, b, 2 * (a + b)), unit=" cm")
    if kind == "rhom":
        tr = r.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (12, 16, 20)])
        return T("The diagonals of a rhombus are %d cm and %d cm. Find its side." % (2 * tr[0], 2 * tr[1]), "%d cm" % tr[2], ["%d cm" % (tr[0] + tr[1]), "%d cm" % (2 * tr[2]), "%d cm" % (tr[1])],
                 "The diagonals of a rhombus bisect each other at right angles: side = √(%d² + %d²) = <b>%d cm</b>." % (tr[0], tr[1], tr[2]))
    if kind == "midq":
        p, q = r.randint(6, 30), r.randint(6, 30)
        return T("The mid-points of the sides of a quadrilateral with diagonals %d cm and %d cm are joined. What is the perimeter of the new quadrilateral?" % (p, q), "%d cm" % (p + q),
                 ["%d cm" % (2 * (p + q)), "%s cm" % num((p + q) / 2), "%d cm" % (p * q // 2) if p * q % 2 == 0 else "%d cm" % (p + q + 2)],
                 "Each side of the new figure is half a diagonal (Mid-point Theorem), and each diagonal is used twice: %d + %d = <b>%d cm</b>. It is a parallelogram." % (p, q, p + q))
    if kind == "rect":
        tr = r.choice([(6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17), (12, 16, 20)])
        return T("A rectangle is %d cm by %d cm. How long is each diagonal, and what is the distance from the point where they meet to a vertex?" % (tr[0], tr[1]), "%d cm; %s cm" % (tr[2], num(tr[2] / 2)),
                 ["%d cm; %d cm" % (tr[2], tr[2]), "%d cm; %s cm" % (tr[0] + tr[1], num((tr[0] + tr[1]) / 2)), "%d cm; %s cm" % (tr[2] * 2, num(tr[2]))],
                 "Diagonal = √(%d² + %d²) = %d cm. The diagonals of a rectangle are equal and bisect each other: <b>%s cm</b> from each vertex." % (tr[0], tr[1], tr[2], num(tr[2] / 2)))
    return None


FACTS = [
    ("A quadrilateral with both pairs of opposite sides parallel is a", "parallelogram", ["trapezium", "kite", "cyclic quadrilateral"]),
    ("The diagonals of a parallelogram", "bisect each other", ["are always equal", "are always perpendicular", "never meet"]),
    ("The diagonals of a rectangle are", "equal and bisect each other", ["perpendicular to each other", "unequal", "parallel"]),
    ("The diagonals of a rhombus", "bisect each other at right angles", ["are equal", "are parallel", "meet at 60°"]),
    ("The diagonals of a square are", "equal and bisect each other at right angles", ["unequal and perpendicular", "equal but not perpendicular", "parallel"]),
    ("A parallelogram with one right angle is a", "rectangle", ["rhombus", "trapezium", "kite"]),
    ("A quadrilateral with exactly one pair of parallel sides is a", "trapezium", ["parallelogram", "rhombus", "rectangle"]),
    ("If a line is drawn through the mid-point of one side of a triangle parallel to another side, it", "bisects the third side", ["is equal to the third side", "is perpendicular to the third side", "passes through the opposite vertex"]),
    ("The line segment joining the mid-points of two sides of a triangle is", "parallel to the third side and half of it", ["equal to the third side", "perpendicular to the third side", "twice the third side"]),
    ("If the diagonals of a quadrilateral bisect each other, it is a", "parallelogram", ["trapezium", "kite", "cyclic quadrilateral only"]),
    ("A diagonal of a parallelogram divides it into", "two congruent triangles", ["two equal squares", "four congruent triangles", "two unequal triangles"]),
    ("The quadrilateral formed by joining the mid-points of the sides of any quadrilateral is a", "parallelogram", ["square", "trapezium", "kite"]),
]


def one_fact(r):
    q, a, w = r.choice(FACTS)
    return T(q + " ___.", a, w, "<b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        S("Angles of quadrilaterals and parallelograms", mix(R, [(one_ang, 20)], seen)),
        S("Properties of parallelograms", mix(R, [(gb(usq.one_pg), 12), (one_fact, 8)], seen)),
        S("Rectangles, rhombuses and squares", mix(R, [(gb(usq.one_spec), 16), (one_fact, 4)], seen)),
        S("The Mid-point Theorem", mix(R, [(mid(usm.one_mid), 20)], seen)),
        S("Problems", mix(R, [(one_prob, 20)], seen)),
    ]
    body = lesson(
        "<p>The angles of a quadrilateral add up to 360°. In a <b>parallelogram</b>, opposite sides are equal, opposite angles are equal, adjacent angles add up to 180°, and the diagonals bisect each other.</p>"
        "<p>Rectangle: equal diagonals. Rhombus: diagonals bisect each other at right angles. Square: both.</p>"
        "<p><b>Mid-point Theorem</b>: the segment joining the mid-points of two sides of a triangle is parallel to the third side and half of it. Converse: a line through the mid-point of one side, parallel to another side, bisects the third side.</p>",
        [("In parallelogram ABCD, ∠A = 70°. Find ∠B, ∠C and ∠D.", ["∠B = 180° − 70°", "Opposite angles are equal"], "110°, 70°, 110°"),
         ("D and E are the mid-points of AB and AC, and BC = 14 cm. Find DE.", ["DE = ½ BC"], "7 cm")],
        ["Taking adjacent angles of a parallelogram as equal. They add up to 180°.",
         "Thinking the diagonals of every parallelogram are equal. That is true only for rectangles (and squares).",
         "Making DE equal to BC. The segment joining the mid-points is half of the third side."])
    faq = [
        ("What are the properties of a parallelogram?", "Opposite sides are equal and parallel, opposite angles are equal, adjacent angles are supplementary, and the diagonals bisect each other."),
        ("What is the Mid-point Theorem?", "The line segment joining the mid-points of two sides of a triangle is parallel to the third side and is half of it."),
        ("How are the diagonals of a rhombus special?", "They bisect each other at right angles (and bisect the angles of the rhombus)."),
        ("What is the sum of the angles of a quadrilateral?", "360°, because a diagonal divides it into two triangles of 180° each."),
    ]
    make(9, "quadrilaterals", 8, "IV", 8, "Quadrilaterals: Parallelograms and the Mid-point Theorem", "quadrilaterals",
         "The diagonal divides a parallelogram into two congruent triangles; in a parallelogram opposite sides are equal and conversely; opposite angles are equal and conversely; a quadrilateral is a parallelogram if a pair of its opposite sides is parallel and equal; the diagonals of a parallelogram bisect each other and conversely; the Mid-point Theorem and its converse (summary of the CBSE syllabus)",
         "Class 9 Quadrilaterals worksheet (NCERT Chapter 8): angle sum, properties of parallelograms, rectangles, rhombuses and squares, and the Mid-point Theorem. 100 questions with answers.",
         "Parallelogram: diagonals bisect each other", "Mid-point Theorem: DE ∥ BC and DE = ½ BC.",
         body, faq, sets, R)


if __name__ == "__main__":
    main()
