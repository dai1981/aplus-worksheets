# -*- coding: utf-8 -*-
"""
Texas Grade 6 Math: Graphing Points in All Four Quadrants (TEKS 6.11A)
  python3 tools/gen_ustx_math_g6_coordinate_plane.py
Reading and plotting points in four quadrants, quadrants and signs, reflections across the axes, distances on the
plane, and polygons and real-world problems (the US Grade 6 makers with Texas names).
Wrong answers come from real mistakes: switching x and y, mixing up the quadrant numbers, and counting grid lines
instead of units.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g6_coordinate_plane as cp
adopt(cp)
tx_common.GRADE = "grade-6"



def build():
    sets, R = build_sets([
        ("Read and plot points", [("run", cp.set_read, ("rnd", cp.People), 20)]),
        ("Quadrants and signs", [("run", cp.set_quadrants, ("rnd", cp.People), 20)]),
        ("Reflections across the axes", [("run", cp.set_reflect, ("rnd", cp.People), 20)]),
        ("Distance between points", [("run", cp.set_distance, ("rnd", cp.People), 20)]),
        ("Polygons and real-world problems", [("run", cp.set_real, ("rnd", cp.People), 20)]),
    ], 66021)
    finish(sets, R)
    body = lesson('<ul><li>An ordered pair (x, y): move <b>x</b> left or right first, then <b>y</b> up or down.</li><li>Quadrants are numbered I to IV counterclockwise, starting at the top right.</li><li>Quadrant signs: I (+, +), II (−, +), III (−, −), IV (+, −).</li><li>For points on the same horizontal or vertical line, the distance is the difference of the coordinates that change.</li></ul>',
        [example("Where is (−3, 4)?", ["3 left", "4 up"], "Quadrant II"), example("Distance from (−2, 5) to (4, 5)", ["Same y", "|−2| + |4|"], "6 units")],
        [['Switching x and y', 'Across first (x), then up or down (y).'], ['Numbering quadrants clockwise', 'Go counterclockwise: I top right, II top left.'], ['Subtracting with mixed signs', 'From −2 to 4 is 2 + 4 = 6 units.']])
    faq = [('What does TEKS 6.11A ask?', 'Graph points in all four quadrants using ordered pairs of rational numbers.'), ('What is the origin?', 'The point (0, 0), where the axes cross.'), ('Which quadrant has (−, −)?', 'Quadrant III, at the bottom left.'), ('Is a point on an axis in a quadrant?', 'No. Points on an axis are not in any quadrant.')]
    make('coordinate-plane', 21, 'Measurement and Data', '6.11A',
         '6.11A graph points in all four quadrants using ordered pairs of rational numbers',
         'Graphing Points in All Four Quadrants', 'Coordinate Plane',
         'Free Grade 6 coordinate plane worksheets for Texas TEKS 6.11A: plot points in all four quadrants, signs, reflections, distances and polygons. 100 questions with answers.',
         '(x, y): across first, then up or down.', 'Quadrants I to IV go counterclockwise. II is (−, +).',
         body, faq, sets, seo_title='Grade 6 Coordinate Plane Worksheets: All Four Quadrants (TEKS 6.11A, STAAR)')


if __name__ == "__main__":
    build()
