# -*- coding: utf-8 -*-
"""
Texas Grade 4 Math: Area and Perimeter Formulas (TEKS 4.5C, 4.5D)
  python3 tools/gen_ustx_math_g4_area_perimeter_formulas.py
Perimeter and area of rectangles and squares with formulas (P = 2l + 2w, P = 4s, A = l × w), missing sides,
bigger numbers and L-shaped floor plans. The question makers come from the US Grade 4 area and perimeter unit,
with Texas names and new numbers. Wrong answers come from real mistakes: using the area formula for perimeter,
adding only two sides, and writing units instead of square units.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, build_sets, example, figure)
import gen_us_math_g4_area_perimeter as usm
adopt(usm)
tx_common.GRADE = "grade-4"


def build():
    sets, R = build_sets([
        ("Area or perimeter? Squares", [("run", usm.set_decide, ("rnd", usm.People), 20)]),
        ("Use the formulas", [("run", usm.set_formulas, ("rnd", "seen"), 20)]),
        ("Find the unknown side", [("run", usm.set_unknown, ("rnd", "seen"), 20)]),
        ("Bigger numbers and the right formula", [("run", usm.set_big, ("rnd", "seen"), 20)]),
        ("L-shapes and word problems", [("run", usm.set_story, ("rnd", usm.People), 20)]),
    ], 64017)
    finish(sets, R)
    body = lesson('<ul><li><b>Perimeter</b> of a rectangle: P = l + w + l + w, or P = 2l + 2w. For a square, P = 4s.</li><li><b>Area</b> of a rectangle: A = l × w. Area is in square units.</li><li>To find a missing side from the area, divide: w = A ÷ l. From the perimeter, halve it and subtract the length.</li></ul>',
        [example("A rectangle is 12 ft by 7 ft. Find the perimeter and area.", ["P = 2 × 12 + 2 × 7 = 24 + 14 = 38 ft", "A = 12 × 7 = 84 square feet"], "38 ft and 84 square feet"), example("A rectangle has an area of 72 square inches and a length of 9 inches. What is the width?", ["72 ÷ 9 = 8"], "8 inches")],
        [['Using l × w for perimeter', 'Perimeter adds all sides: 2l + 2w.'], ['Adding only l + w', 'That is half the perimeter. Double it.'], ['Writing ft for area', 'Area is in square units: square feet.']])
    faq = [('What does TEKS 4.5C ask?', 'Use models to find the formulas for the perimeter of a rectangle (l + w + l + w or 2l + 2w), the perimeter of a square (4s) and the area of a rectangle (l × w).'), ('What does TEKS 4.5D ask?', 'Solve problems about the perimeter and area of rectangles with whole-number dimensions.'), ('How do you find a missing side?', 'For area, divide the area by the known side. For perimeter, subtract the two known sides from the perimeter and halve what is left.'), ('How can I tell if a problem asks for area or perimeter?', 'Fences, borders and trim go around: perimeter. Carpet, paint and tiles cover: area.')]
    make('area-and-perimeter-formulas', 17, 'Algebraic Reasoning', '4.5C, 4.5D',
         '4.5C use models to determine the formulas for the perimeter of a rectangle (l + w + l + w or 2l + 2w), including the special form for perimeter of a square (4s) and the area of a rectangle (l x w); 4.5D solve problems related to perimeter and area of rectangles where dimensions are whole numbers',
         'Area and Perimeter Formulas', 'Area and Perimeter Formulas',
         'Free Grade 4 area and perimeter worksheets for Texas TEKS 4.5C and 4.5D: perimeter 2l + 2w and 4s, area l × w, missing sides, bigger numbers and L-shaped floor plans. 100 STAAR-style questions with answers.',
         'Perimeter: P = 2l + 2w. Area: A = l × w.', 'A square has P = 4s. Area is in square units. Divide the area by one side to find the other side.',
         body, faq, sets, seo_title='Grade 4 Area and Perimeter Formulas Worksheets (TEKS 4.5C, 4.5D, STAAR)')


if __name__ == "__main__":
    build()
