# -*- coding: utf-8 -*-
"""
India Class 8 Maths, Ganita Prakash Part 2, Chapter 7: Area
  python3 tools/gen_in_maths_c8_area.py
Area of triangles and parallelograms, a missing base or height, trapeziums, rhombuses and kites (half the product of the
diagonals), and composite shapes made of rectangles and triangles. Reuses the AU Year 7 and Year 8 makers with figures.
Wrong answers come from real mistakes: using the slant side instead of the perpendicular height, forgetting ½ for a
triangle, and adding the parallel sides without halving for a trapezium.
"""
import random
from in_common import unit, QN, adopt, gb
import gen_au_maths_y7_area_of_triangles_and_parallelograms as a7
import gen_au_maths_y8_area_and_perimeter_of_composite_shapes as a8

R = random.Random(908014)
adopt(a7, R)
adopt(a8, R)


def one_rhombus(r):
    d1, d2 = r.choice([6, 8, 10, 12, 14, 16, 18, 20, 24]), r.choice([5, 7, 9, 11, 13, 15, 21])
    kind = r.choice(["area", "area", "back"])
    if kind == "area":
        return QN("The diagonals of a rhombus are %d cm and %d cm. Find its area." % (d1, d2), d1 * d2 // 2 if d1 * d2 % 2 == 0 else None, [d1 * d2, d1 + d2, 2 * (d1 + d2)],
                  "Area = ½ × %d × %d = <b>%d cm²</b>." % (d1, d2, d1 * d2 // 2), unit=" cm²")
    a = d1 * d2 // 2
    return QN("A rhombus has area %d cm² and one diagonal of %d cm. Find the other diagonal." % (a, d1), d2, [a // d1 if a % d1 == 0 and a // d1 != d2 else d2 + 2, a - d1, 2 * a],
              "½ × %d × d = %d, so d = 2 × %d ÷ %d = <b>%d cm</b>." % (d1, a, a, d1, d2), unit=" cm")


def main():
    unit(8, 2, 7, "area", 14, "M", "Area: Triangles, Quadrilaterals and Composite Shapes", "area",
         "Area of triangles, parallelograms, trapeziums, rhombuses and kites, and of shapes made from them (summary of NCERT Ganita Prakash Class 8)",
         "Class 8 Area worksheet (Ganita Prakash Part 2, Chapter 7): area of triangles, parallelograms, trapeziums, rhombuses, kites and composite shapes. 100 questions with answers.",
         "Triangle ½bh, parallelogram bh, trapezium ½(a + b)h", "Rhombus and kite: ½ × product of the diagonals.",
         "<p><b>Parallelogram</b>: base × perpendicular height. <b>Triangle</b>: ½ × base × height.</p>"
         "<p><b>Trapezium</b>: ½ × (sum of the parallel sides) × height. <b>Rhombus</b> and <b>kite</b>: ½ × d<sub>1</sub> × d<sub>2</sub>.</p>"
         "<p>For a composite shape, split it into rectangles and triangles and add (or subtract a hole).</p>",
         [("Find the area of a trapezium with parallel sides 8 cm and 12 cm and height 5 cm.", ["½ × (8 + 12) × 5"], "50 cm²"),
          ("The diagonals of a kite are 10 cm and 7 cm. Find its area.", ["½ × 10 × 7"], "35 cm²")],
         ["Using the slant side instead of the perpendicular height.", "Forgetting the ½ for a triangle.", "Multiplying the diagonals of a rhombus without halving."],
         [("How do you find the area of a trapezium?", "Half the sum of the parallel sides times the perpendicular distance between them."),
          ("How do you find the area of a rhombus?", "Half the product of its diagonals, because the diagonals cut it into four right triangles."),
          ("Why is the area of a triangle half of base × height?", "Two copies of the triangle make a parallelogram with the same base and height.")],
         [("Area of triangles", [(gb(a7.one_tri), 20)]),
          ("Area of parallelograms", [(gb(a7.one_para), 12), (gb(a7.one_missing), 8)]),
          ("Trapeziums", [(gb(a8.one_trap), 20)]),
          ("Rhombuses and kites", [(one_rhombus, 12), (gb(a8.one_kite), 8)]),
          ("Composite shapes", [(gb(a8.one_comp), 12), (gb(a7.one_house), 8)])], R)


if __name__ == "__main__":
    main()
