# -*- coding: utf-8 -*-
"""
South Africa Grade 9 Maths (CAPS): Quadrilaterals and Polygons: Properties, Diagonals and Angle Sums (Grade 9: 3.1 Geometry of 2D shapes)
  python3 tools/gen_za_maths_g9_quadrilaterals.py
Angles in quadrilaterals, properties and diagonals of quadrilaterals, angle sums of polygons and regular polygons
(Singapore Secondary 1, Australia Year 8 and Year 7 and Ontario Grade 6 makers).
Wrong answers come from real mistakes: using 180° for a quadrilateral, thinking every parallelogram has equal
diagonals, and using n × 180° for a polygon.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_sg_maths_s1_angles_triangles_and_quadrilaterals as sga
adopt(sga)
if isinstance(getattr(sga, 'R', None), random.Random): sga.R = random.Random(809130)
import gen_au_maths_y8_properties_of_quadrilaterals as auq
adopt(auq)
if isinstance(getattr(auq, 'R', None), random.Random): auq.R = random.Random(809131)
import gen_sg_maths_s1_parallel_lines_and_polygons as sgp
adopt(sgp)
if isinstance(getattr(sgp, 'R', None), random.Random): sgp.R = random.Random(809132)
import gen_au_maths_y7_angle_sum_of_triangles_and_polygons as aua
adopt(aua)
if isinstance(getattr(aua, 'R', None), random.Random): aua.R = random.Random(809133)
import gen_caon_math_g6_quadrilaterals as caq
adopt(caq)
if isinstance(getattr(caq, 'R', None), random.Random): caq.R = random.Random(809134)
za_common.GRADE = "grade-9"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok9(it):
    """Grade 9: no trigonometry, quadratic formula, simultaneous equations or cones and spheres (Grade 10+)"""
    return not _re.search(r"\b(sin|cos|tan)\b|quadratic formula|discriminant|simultaneous|\bcone|\bsphere|imperial|\bmiles?\b", _txt(it))



def build():
    sets, R = build_sets([
        ("Angles in quadrilaterals", [("collect", sga.one_quad, 10), ("collect", auq.one_angle, 10)]),
        ("Diagonals", [("collect", auq.one_diag, 10), ("run", caq.set_diagonals, ("rnd",), 10, ok9)]),
        ("Angle sums of polygons", [("collect", sgp.one_sum, 20)]),
        ("Regular polygons", [("collect", sgp.one_regular, 10), ("collect", aua.one_regular, 10)]),
        ("Polygon problems", [("collect", sgp.one_sides, 10), ("run", caq.set_words, ("rnd",), 10, ok9)]),
    ], 80913)
    finish(sets, R)
    body = lesson('<ul><li>The angles of a quadrilateral add up to 360°.</li><li>Parallelogram: opposite sides parallel and equal, diagonals bisect each other. Rhombus: diagonals perpendicular. Rectangle: diagonals equal.</li><li>Angle sum of an n-sided polygon: (n − 2) × 180°.</li><li>Exterior angles of any polygon add up to 360°.</li></ul>',
        [example("A regular polygon with exterior angle 30°", ["360 ÷ 30"], "12 sides")],
        [['180° for a quadrilateral', 'It is 360°.'], ['All diagonals equal', 'Only in rectangles and squares.'], ['n × 180°', 'Use (n − 2) × 180°.']])
    faq = [('What does CAPS Grade 9 say about quadrilaterals?', 'Use the properties of the sides, angles and diagonals of special quadrilaterals to solve problems.'), ("Do a kite's diagonals bisect each other?", 'Only one diagonal is bisected.'), ('What is each angle of a regular octagon?', '135°.'), ('Is a rectangle a parallelogram?', 'Yes.')]
    make('quadrilaterals-and-polygons', 13, 'Space and Shape (Geometry)', 'Grade 9: 3.1 Geometry of 2D shapes',
         'Investigate and describe the properties of the sides, angles and diagonals of quadrilaterals; solve geometric problems involving unknown sides and angles in quadrilaterals using known properties.',
         'Quadrilaterals and Polygons: Properties, Diagonals and Angle Sums', 'Quadrilaterals and Polygons',
         'Free CAPS Grade 9 quadrilaterals worksheets: angles, properties and diagonals of quadrilaterals and angle sums of polygons. 100 questions with memos.',
         'Polygon: (n − 2) × 180°.', 'Exterior angles add to 360°.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
