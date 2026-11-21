# -*- coding: utf-8 -*-
"""
India Class 8 Maths, Ganita Prakash Part 1, Chapter 4: Quadrilaterals
  python3 tools/gen_in_maths_c8_quadrilaterals.py
The angle sum of a quadrilateral, properties of parallelograms, rectangles, rhombuses, squares, kites and trapeziums
(sides, angles and diagonals), classifying quadrilaterals, and problems with diagonals. Reuses the US Geometry and AU
Year 8 makers with figures.
Wrong answers come from real mistakes: adjacent angles of a parallelogram taken as equal, the angle sum taken as 180°,
and a rhombus assumed to have equal diagonals.
"""
import random
from in_common import unit, T, adopt, gb
import gen_us_math_ge_polygons_and_quadrilaterals as usq
import gen_au_maths_y8_properties_of_quadrilaterals as auq
import gen_uk_maths_y7_angles as uka
import gen_in_maths_c9_quadrilaterals as c9

R = random.Random(908004)
for m in (usq, auq, uka):
    adopt(m, R)

PROPS = [
    ("Which quadrilateral has exactly one pair of parallel sides?", "Trapezium", ["Parallelogram", "Rhombus", "Rectangle"]),
    ("Which quadrilateral has two pairs of equal adjacent sides but is not a rhombus?", "Kite", ["Trapezium", "Rectangle", "Parallelogram"]),
    ("In which quadrilateral are the diagonals equal and perpendicular bisectors of each other?", "Square", ["Rhombus", "Rectangle", "Kite"]),
    ("In which quadrilateral are the diagonals equal but not always perpendicular?", "Rectangle", ["Rhombus", "Kite", "Square"]),
    ("In which quadrilateral do the diagonals bisect each other at right angles, but are not always equal?", "Rhombus", ["Rectangle", "Square", "Trapezium"]),
    ("Every square is also a ___.", "rhombus", ["kite that is not a parallelogram", "trapezium with one pair of parallel sides", "triangle"]),
    ("Which statement is always true?", "Every rectangle is a parallelogram", ["Every parallelogram is a rectangle", "Every rhombus is a square", "Every kite is a rhombus"]),
    ("Which statement is always true?", "Every square is a rectangle", ["Every rectangle is a square", "Every rhombus is a rectangle", "Every trapezium is a parallelogram"]),
    ("Opposite angles of a parallelogram are", "equal", ["supplementary", "complementary", "always 90°"]),
    ("Adjacent angles of a parallelogram are", "supplementary", ["equal", "complementary", "always 90°"]),
    ("The diagonals of a parallelogram", "bisect each other", ["are always equal", "are always perpendicular", "never meet"]),
    ("A parallelogram with one right angle must be a", "rectangle", ["rhombus", "kite", "trapezium"]),
    ("A parallelogram with two adjacent sides equal must be a", "rhombus", ["rectangle", "kite", "trapezium"]),
    ("In a kite, the diagonals", "are perpendicular", ["are equal", "bisect each other", "are parallel"]),
    ("What is the sum of the angles of any quadrilateral?", "360°", ["180°", "540°", "720°"]),
    ("How many diagonals does a quadrilateral have?", "2", ["4", "1", "3"]),
]


def one_prop(r):
    q, a, w = r.choice(PROPS)
    return T(q if q.endswith("?") or "___" in q else q + " ___.", a, w, "<b>%s</b>." % a)


def main():
    unit(8, 1, 4, "quadrilaterals", 4, "G", "Quadrilaterals: Properties of Quadrilaterals", "quadrilaterals",
         "Angle sum of a quadrilateral; properties of parallelograms, rectangles, rhombuses, squares, kites and trapeziums; relationships between quadrilaterals (summary of NCERT Ganita Prakash Class 8)",
         "Class 8 Quadrilaterals worksheet (Ganita Prakash Part 1, Chapter 4): angle sum, parallelograms, rectangles, rhombuses, squares, kites and trapeziums. 100 questions with answers.",
         "The angles of a quadrilateral add up to 360°", "In a parallelogram, opposite angles are equal and adjacent angles add up to 180°.",
         "<p>A quadrilateral splits into two triangles, so its angles add up to <b>360°</b>.</p>"
         "<p><b>Parallelogram</b>: opposite sides parallel and equal, opposite angles equal, diagonals bisect each other. A <b>rectangle</b> also has equal diagonals; a <b>rhombus</b> has perpendicular diagonals; a <b>square</b> has both.</p>"
         "<p>A <b>kite</b> has two pairs of equal adjacent sides; a <b>trapezium</b> has one pair of parallel sides.</p>",
         [("Three angles of a quadrilateral are 80°, 95° and 110°. Find the fourth.", ["360° − (80° + 95° + 110°)"], "75°"),
          ("In parallelogram ABCD, ∠A = 65°. Find ∠B.", ["Adjacent angles add up to 180°"], "115°")],
         ["Using 180° as the angle sum of a quadrilateral.", "Taking adjacent angles of a parallelogram as equal.", "Thinking a rhombus always has equal diagonals. Only a square does."],
         [("What is the angle sum of a quadrilateral?", "360°, because a diagonal splits it into two triangles."),
          ("What are the properties of a parallelogram?", "Opposite sides are parallel and equal, opposite angles are equal, adjacent angles add up to 180° and the diagonals bisect each other."),
          ("Is a square a rhombus?", "Yes. A square has four equal sides, so it is a rhombus; it is also a rectangle.")],
         [("Angle sum of a quadrilateral", [(gb(uka.one_quad), 10), (c9.one_ang, 10)]),
          ("Types of quadrilaterals", [(one_prop, 14), (c9.one_fact, 6)]),
          ("Parallelograms", [(gb(usq.one_pg), 12), (gb(auq.one_angle), 8)]),
          ("Rectangles, rhombuses and squares", [(gb(usq.one_spec), 14), (gb(auq.one_diag), 6)]),
          ("Problems", [(gb(auq.one_angle), 6), (gb(auq.one_diag), 6), (gb(usq.one_pg), 8)])], R)


if __name__ == "__main__":
    main()
