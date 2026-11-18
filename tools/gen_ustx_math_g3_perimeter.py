# -*- coding: utf-8 -*-
"""
Texas Grade 3 Math: Perimeter (TEKS 3.7B)
  python3 tools/gen_ustx_math_g3_perimeter.py
Adding side lengths, counting units around a shape on a grid, rectangles and squares, missing side lengths when
the perimeter is given, and word problems that mix perimeter and area. The question makers come from the US
Grade 3 perimeter unit, with Texas names and new numbers.
Wrong answers come from real mistakes: adding only the sides that are labeled, multiplying the sides (area),
counting squares inside instead of edges around, and subtracting only one side when a side is missing.
"""
import random
from tx_common import (finish, make, lesson, S, run_many, adopt, example)
import gen_us_math_g3_perimeter as usp

adopt(usp)
R = random.Random(61601)


def build():
    sets = []
    for k, (title, fn) in enumerate([("Add the side lengths", usp.set_add), ("Count the units around", usp.set_grid),
                                     ("Rectangles and squares", usp.set_rect), ("Find the missing side", usp.set_missing),
                                     ("Word problems: perimeter and area", usp.set_story)]):
        sets.append(S(title, run_many(fn, "rnd", seed=171 + k, avoid=sets)))
    finish(sets, R)
    body = lesson(
        "<ul><li><b>Perimeter</b> is the distance around a shape. Add the lengths of all the sides.</li>"
        "<li>A rectangle has 2 pairs of equal sides: perimeter = length + width + length + width. A square has 4 equal sides.</li>"
        "<li>To find a <b>missing side</b>, add the sides you know and subtract from the perimeter.</li>"
        "<li>Perimeter is measured in units (cm, in., ft). Area is measured in square units.</li></ul>",
        [example("A rectangle is 8 ft long and 5 ft wide. What is its perimeter?", ["8 + 5 + 8 + 5", "= 26"], "26 ft"),
         example("A triangle has a perimeter of 30 cm. Two sides are 9 cm and 12 cm. How long is the third side?", ["9 + 12 = 21", "30 − 21 = 9"], "9 cm")],
        [["Adding only the labeled sides of a rectangle", "Opposite sides are equal. Add all 4 sides."],
         ["Multiplying length × width", "That is area. Perimeter adds the sides."],
         ["Counting the squares inside the shape", "Count the unit edges around the outside."]])
    faq = [("What does TEKS 3.7B ask?", "Find the perimeter of a polygon, or a missing side length when the perimeter and the other side lengths are given, in problems."),
           ("How do you find the perimeter of a rectangle?", "Add all four sides: length + width + length + width. For 7 by 3, that is 7 + 3 + 7 + 3 = 20."),
           ("How do you find a missing side?", "Add the known sides, then subtract that sum from the perimeter."),
           ("What is the difference between perimeter and area?", "Perimeter is the distance around (units). Area is the space inside (square units).")]
    make("perimeter", 16, "Geometry and Measurement", "3.7B",
         "3.7B determine the perimeter of a polygon or a missing length when given perimeter and remaining side lengths in problems",
         "Perimeter of Polygons and Missing Side Lengths", "Perimeter",
         "Free Grade 3 perimeter worksheets for Texas TEKS 3.7B: add side lengths, count units around, rectangles and squares, missing side lengths and perimeter and area word problems. 100 STAAR-style questions with answers.",
         "Perimeter is the distance around: add all the sides.", "For a missing side, add the known sides and subtract from the perimeter.",
         body, faq, sets, seo_title="Grade 3 Perimeter Worksheets: Missing Side Lengths (TEKS 3.7B, STAAR)")


if __name__ == "__main__":
    build()
