# -*- coding: utf-8 -*-
"""
South Africa Grade 8 Maths (CAPS): Quadrilaterals and Polygons: Properties and Angle Sums (Grade 8: 3.2 Geometry of 2D shapes)
  python3 tools/gen_za_maths_g8_quadrilaterals.py
Angles in quadrilaterals, properties of quadrilaterals and their diagonals, angle sums of polygons and regular
polygons (UK Year 7 and Year 8, Australia Year 7 and Year 8 and Ontario Grade 6 makers).
Wrong answers come from real mistakes: using 180° for a quadrilateral, thinking all parallelograms have equal
diagonals, and using n × 180° for the angle sum of a polygon.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y7_angles as uka
adopt(uka)
if isinstance(getattr(uka, 'R', None), random.Random): uka.R = random.Random(808150)
import gen_au_maths_y8_properties_of_quadrilaterals as auq
adopt(auq)
if isinstance(getattr(auq, 'R', None), random.Random): auq.R = random.Random(808151)
import gen_uk_maths_y8_angles_in_parallel_lines_and_polygons as ukp
adopt(ukp)
if isinstance(getattr(ukp, 'R', None), random.Random): ukp.R = random.Random(808152)
import gen_au_maths_y7_angle_sum_of_triangles_and_polygons as aua
adopt(aua)
if isinstance(getattr(aua, 'R', None), random.Random): aua.R = random.Random(808153)
import gen_caon_math_g6_quadrilaterals as caq
adopt(caq)
if isinstance(getattr(caq, 'R', None), random.Random): caq.R = random.Random(808154)
za_common.GRADE = "grade-8"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok8(it):
    """Grade 8: no trigonometry, quadratic formula or surds beyond square roots"""
    return not _re.search(r"\b(sin|cos|tan)\b|quadratic|discriminant|imperial|\bmiles?\b", _txt(it))



def build():
    sets, R = build_sets([
        ("Angles in a quadrilateral", [("collect", uka.one_quad, 10), ("collect", auq.one_angle, 10)]),
        ("Properties and diagonals", [("collect", auq.one_diag, 10), ("run", caq.set_diagonals, ("rnd",), 10, ok8)]),
        ("Angle sum of a polygon", [("collect", ukp.one_sum, 10), ("collect", aua.one_sum, 10)]),
        ("Regular polygons", [("collect", ukp.one_regular, 10), ("collect", aua.one_regular, 10)]),
        ("Polygon problems", [("collect", ukp.one_sides, 10), ("run", caq.set_words, ("rnd",), 10, ok8)]),
    ], 80815)
    finish(sets, R)
    body = lesson('<ul><li>The angles of a quadrilateral add up to 360°.</li><li>A parallelogram has opposite sides and angles equal; a rectangle has equal diagonals; a rhombus has perpendicular diagonals.</li><li>The angles of an n-sided polygon add up to (n − 2) × 180°.</li><li>Each angle of a regular polygon = (n − 2) × 180° ÷ n.</li></ul>',
        [example("A regular hexagon", ["(6 − 2) × 180 = 720"], "each angle 120°")],
        [['180° in a quadrilateral', 'A quadrilateral is 360°.'], ['All diagonals equal', 'Only in rectangles and squares.'], ['n × 180°', 'Use (n − 2) × 180°.']])
    faq = [('What does CAPS Grade 8 say about quadrilaterals?', 'Describe and compare quadrilaterals by sides, angles and diagonals, and solve geometric problems using their properties.'), ('Do the diagonals of a kite cross at 90°?', 'Yes.'), ('What is the angle sum of a pentagon?', '540°.'), ('Is a square a rhombus?', 'Yes.')]
    make('quadrilaterals-and-polygons', 15, 'Space and Shape (Geometry)', 'Grade 8: 3.2 Geometry of 2D shapes',
         'Explore properties of the sides, angles and diagonals of quadrilaterals (parallelogram, rectangle, rhombus, square, trapezium, kite); solve geometric problems involving unknown sides and angles in quadrilaterals using known properties.',
         'Quadrilaterals and Polygons: Properties and Angle Sums', 'Quadrilaterals and Polygons',
         'Free CAPS Grade 8 quadrilaterals worksheets: angles in quadrilaterals, properties and diagonals, polygon angle sums and regular polygons. 100 questions with memos.',
         'Quadrilateral: 360°. Polygon: (n − 2) × 180°.', 'Rhombus diagonals are perpendicular.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
