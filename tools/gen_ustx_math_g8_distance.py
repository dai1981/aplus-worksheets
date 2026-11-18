# -*- coding: utf-8 -*-
"""
Texas Grade 8 Math: Distance Between Two Points (TEKS 8.7D)
  python3 tools/gen_ustx_math_g8_distance.py
Distance straight across or up and down, drawing a right triangle, using the coordinates, shapes and comparisons,
and maps (the US Grade 8 makers with a new seed).
Wrong answers come from real mistakes: adding the changes in x and y, forgetting the square root, and subtracting
coordinates with mixed signs.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g8_distance_on_coordinate_plane as dcp
adopt(dcp)
dcp.R = random.Random(680160)
tx_common.GRADE = "grade-8"



def build():
    sets, R = build_sets([
        ("Straight across or up and down", [("run", dcp.set_straight, (), 20)]),
        ("Draw a right triangle", [("run", dcp.set_picture, (), 20)]),
        ("Use the coordinates", [("run", dcp.set_formula, (), 20)]),
        ("Shapes and comparisons", [("run", dcp.set_shapes, (), 20)]),
        ("Maps and real-world distance", [("run", dcp.set_maps, (), 20)]),
    ], 68016)
    finish(sets, R)
    body = lesson('<ul><li>For points on the same horizontal or vertical line, the distance is the difference of the coordinates that change.</li><li>Otherwise, draw a <b>right triangle</b>: the legs are the change in x and the change in y.</li><li>Use the Pythagorean theorem: d = √((change in x)² + (change in y)²).</li><li>With negative coordinates, count the units across 0.</li></ul>',
        [example("(1, 2) and (4, 6)", ["Across 3, up 4", "√(9 + 16)"], "5")],
        [['Adding the changes: 3 + 4 = 7', 'The distance is the hypotenuse: √(9 + 16) = 5.'], ['Forgetting the square root', 'd² = 25 means d = 5.'], ['Subtracting with mixed signs', 'From −2 to 4 is 6 units.']])
    faq = [('What does TEKS 8.7D ask?', 'Determine the distance between two points on a coordinate plane using the Pythagorean Theorem.'), ('Do I need the distance formula?', 'No. Drawing a right triangle and using a² + b² = c² works every time.'), ('Can a distance be negative?', 'No. Distance is always positive or zero.'), ('What if the answer is not a whole number?', 'Leave it as a square root or round it, such as √20 ≈ 4.5.')]
    make('distance-on-the-coordinate-plane', 16, 'Expressions, Equations and Relationships', '8.7D',
         '8.7D determine the distance between two points on a coordinate plane using the Pythagorean Theorem',
         'Distance Between Two Points', 'Distance on the Coordinate Plane',
         'Free Grade 8 worksheets for Texas TEKS 8.7D: distance between two points on the coordinate plane with right triangles and the Pythagorean theorem, shapes and maps. 100 questions with answers.',
         'Draw a right triangle and use a² + b² = c².', '(1, 2) to (4, 6): √(3² + 4²) = 5.',
         body, faq, sets, seo_title='Grade 8 Distance on the Coordinate Plane Worksheets (TEKS 8.7D, STAAR)')


if __name__ == "__main__":
    build()
