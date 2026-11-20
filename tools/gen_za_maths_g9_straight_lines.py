# -*- coding: utf-8 -*-
"""
South Africa Grade 9 Maths (CAPS): Geometry of Straight Lines: Angle Relationships and Parallel Lines (Grade 9: 3.2 Geometry of straight lines)
  python3 tools/gen_za_maths_g9_straight_lines.py
Angles on lines and around points, vertically opposite angles, angles on parallel lines, and solving for unknown
angles with reasons (Singapore Secondary 1, UK Year 8 and Australia Year 7 makers).
Wrong answers come from real mistakes: mixing up alternate and corresponding angles, thinking co-interior angles are
equal, and forgetting to give a reason.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_sg_maths_s1_angles_triangles_and_quadrilaterals as sga
adopt(sga)
if isinstance(getattr(sga, 'R', None), random.Random): sga.R = random.Random(809110)
import gen_sg_maths_s1_parallel_lines_and_polygons as sgp
adopt(sgp)
if isinstance(getattr(sgp, 'R', None), random.Random): sgp.R = random.Random(809111)
import gen_au_maths_y7_angles_and_parallel_lines as aup
adopt(aup)
if isinstance(getattr(aup, 'R', None), random.Random): aup.R = random.Random(809112)
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
        ("Angles on a line and at a point", [("collect", sga.one_line, 10), ("collect", sga.one_point, 10)]),
        ("Vertically opposite angles", [("collect", sga.one_vopp, 10), ("collect", sga.one_vopp2, 10)]),
        ("Name the angle pair", [("collect", sgp.one_name, 20)]),
        ("Parallel lines", [("collect", sgp.one_parallel, 10), ("collect", aup.one_parallel2, 10)]),
        ("Angles with algebra", [("collect", aup.one_alg, 10), ("collect", aup.one_check, 10)]),
    ], 80911)
    finish(sets, R)
    body = lesson('<ul><li>Angles on a straight line add to 180°; around a point to 360°.</li><li>Vertically opposite angles are equal.</li><li>With parallel lines: corresponding angles are equal, alternate angles are equal, co-interior angles add to 180°.</li><li>Give a reason for every step.</li></ul>',
        [example("Alternate angles 4x − 10° and 3x + 15°", ["4x − 10 = 3x + 15"], "x = 25°")],
        [['Alternate or corresponding?', 'Z: alternate. F: corresponding.'], ['Co-interior equal', 'They add up to 180°.'], ['No reason', 'State the angle rule you used.']])
    faq = [('What does CAPS Grade 9 say about straight lines?', 'Solve geometric problems involving unknown angles using the relationships between pairs of angles formed by intersecting and parallel lines, giving reasons.'), ('What makes two lines parallel?', 'Equal corresponding or alternate angles.'), ('Why give reasons?', 'To prove each step.'), ('What are adjacent angles?', 'Angles that share a side and a vertex.')]
    make('geometry-of-straight-lines', 11, 'Space and Shape (Geometry)', 'Grade 9: 3.2 Geometry of straight lines',
         'Recognise and describe pairs of angles formed by perpendicular lines, intersecting lines, and parallel lines cut by a transversal; solve geometric problems using the relationships between pairs of angles, giving reasons.',
         'Geometry of Straight Lines: Angle Relationships and Parallel Lines', 'Geometry of Straight Lines',
         'Free CAPS Grade 9 geometry worksheets: angles on lines, vertically opposite angles, parallel lines and angles with algebra. 100 questions with memos.',
         'Z: equal. F: equal. C: add to 180°.', 'Give a reason for each step.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
