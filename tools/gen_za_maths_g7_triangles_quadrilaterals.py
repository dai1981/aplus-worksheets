# -*- coding: utf-8 -*-
"""
South Africa Grade 7 Maths (CAPS): Triangles and Quadrilaterals: Properties and Angle Sums (Grade 7: 3.2 Geometry of 2D shapes)
  python3 tools/gen_za_maths_g7_triangles_quadrilaterals.py
Kinds of triangles by sides and angles, the angle sum of a triangle and a quadrilateral, and properties of
quadrilaterals (BC Grade 6, Ontario Grade 6, UK Year 7 and Australia Year 7 makers).
Wrong answers come from real mistakes: using 360° for a triangle, forgetting that the base angles of an isosceles
triangle are equal, and thinking a square is not a rectangle.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_cabc_math_g6_triangles as cbt
adopt(cbt)
if isinstance(getattr(cbt, 'R', None), random.Random): cbt.R = random.Random(807190)
import gen_caon_math_g6_quadrilaterals as caq
adopt(caq)
if isinstance(getattr(caq, 'R', None), random.Random): caq.R = random.Random(807191)
import gen_uk_maths_y7_angles as uka
adopt(uka)
if isinstance(getattr(uka, 'R', None), random.Random): uka.R = random.Random(807192)
import gen_au_maths_y7_angle_sum_of_triangles_and_polygons as aua
adopt(aua)
if isinstance(getattr(aua, 'R', None), random.Random): aua.R = random.Random(807193)
za_common.GRADE = "grade-7"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok7(it):
    """Grade 7: no circles, pi or standard form (they come in Grade 8 and 9)"""
    return not _re.search(r"π|\bpi\b|circumference|radius|diameter|×\s?10<sup>|standard form|scientific notation", _txt(it))


def noneg(it):
    return ok7(it) and not _re.search(r"(?<![\d)] )[−-]\d", _txt(it))



def build():
    sets, R = build_sets([
        ("Kinds of triangles", [("run", cbt.set_sides, ("rnd", cbt.Spots), 10, ok7), ("run", cbt.set_angles, ("rnd", cbt.Spots), 10, ok7)]),
        ("Angles in a triangle", [("collect", uka.one_tri, 10), ("collect", aua.one_tri, 10)]),
        ("Kinds of quadrilaterals", [("run", caq.set_name, ("rnd",), 10, ok7), ("run", caq.set_diagonals, ("rnd",), 10, ok7)]),
        ("Angles in a quadrilateral", [("collect", uka.one_quad, 10), ("collect", aua.one_quad, 10)]),
        ("Shape problems", [("run", cbt.set_missing, ("rnd",), 10, ok7), ("run", caq.set_words, ("rnd",), 10, ok7)]),
    ], 80719)
    finish(sets, R)
    body = lesson('<ul><li>The angles of a triangle add up to 180°.</li><li>The angles of a quadrilateral add up to 360°.</li><li>An isosceles triangle has two equal sides and two equal base angles. An equilateral triangle has three angles of 60°.</li><li>A square is a special rectangle, rhombus and parallelogram.</li></ul>',
        [example("An isosceles triangle with top angle 40°", ["180 − 40 = 140", "140 ÷ 2"], "base angles 70° each")],
        [['360° in a triangle', 'A triangle is 180°.'], ['Base angles', 'In an isosceles triangle they are equal.'], ['A square is a rectangle', 'It has four right angles.']])
    faq = [('What does CAPS Grade 7 say about 2-D shapes?', 'Describe, sort, define and compare triangles by their sides and angles, and quadrilaterals by their sides, angles, parallel and perpendicular sides.'), ('Can a triangle have two right angles?', 'No: 90 + 90 = 180 leaves 0°.'), ('What is a kite?', 'A quadrilateral with two pairs of equal adjacent sides.'), ('Is every rhombus a parallelogram?', 'Yes.')]
    make('triangles-and-quadrilaterals', 19, 'Space and Shape (Geometry)', 'Grade 7: 3.2 Geometry of 2D shapes',
         'Describe, sort, define and compare triangles in terms of their sides and angles (equilateral, isosceles, right-angled, scalene); describe, sort, define and compare quadrilaterals in terms of length of sides, parallel and perpendicular sides, and size of angles (parallelogram, rectangle, square, rhombus, trapezium, kite); solve geometric problems using the angle sums.',
         'Triangles and Quadrilaterals: Properties and Angle Sums', 'Triangles and Quadrilaterals',
         'Free CAPS Grade 7 worksheets: kinds of triangles and quadrilaterals, angle sums of triangles and quadrilaterals, and shape problems. 100 questions with memos.',
         'Triangle: 180°. Quadrilateral: 360°.', 'A square is a special rectangle.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
