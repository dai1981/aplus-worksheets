# -*- coding: utf-8 -*-
"""
South Africa Grade 8 Maths (CAPS): Geometry of Straight Lines: Parallel Lines and Transversals (Grade 8: 3.1 Geometry of straight lines)
  python3 tools/gen_za_maths_g8_straight_lines.py
Angles on a line and around a point, vertically opposite angles, corresponding, alternate and co-interior angles on
parallel lines, and angle problems (UK Year 7 and Year 8 and Australia Year 7 makers).
Wrong answers come from real mistakes: mixing up alternate and corresponding angles, thinking co-interior angles are
equal, and using 360° on a straight line.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y7_angles as uka
adopt(uka)
if isinstance(getattr(uka, 'R', None), random.Random): uka.R = random.Random(808130)
import gen_uk_maths_y8_angles_in_parallel_lines_and_polygons as ukp
adopt(ukp)
if isinstance(getattr(ukp, 'R', None), random.Random): ukp.R = random.Random(808131)
import gen_au_maths_y7_angles_and_parallel_lines as aup
adopt(aup)
if isinstance(getattr(aup, 'R', None), random.Random): aup.R = random.Random(808132)
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
        ("Angles on a line and at a point", [("collect", uka.one_line, 10), ("collect", uka.one_point, 10)]),
        ("Vertically opposite angles", [("collect", uka.one_vopp2, 20)]),
        ("Name the angle pair", [("collect", ukp.one_name, 10), ("collect", aup.one_name, 10)]),
        ("Parallel lines", [("collect", ukp.one_parallel, 10), ("collect", aup.one_parallel, 10)]),
        ("Angle problems", [("collect", aup.one_parallel2, 10), ("collect", aup.one_alg, 10)]),
    ], 80813)
    finish(sets, R)
    body = lesson('<ul><li>Angles on a line add to 180°; around a point to 360°; vertically opposite angles are equal.</li><li>When a transversal cuts parallel lines, <b>corresponding</b> angles are equal (F shape).</li><li><b>Alternate</b> angles are equal (Z shape).</li><li><b>Co-interior</b> angles add up to 180° (C shape).</li></ul>',
        [example("Co-interior angles 3x and 2x + 30°", ["5x + 30 = 180"], "x = 30°")],
        [['Alternate or corresponding?', 'Z is alternate; F is corresponding.'], ['Co-interior are equal', 'They add up to 180°.'], ['360° on a line', 'A straight line is 180°.']])
    faq = [('What does CAPS Grade 8 say about straight lines?', 'Recognise and describe pairs of angles formed by perpendicular lines, intersecting lines, and parallel lines cut by a transversal, and solve geometric problems using these relationships.'), ('What is a transversal?', 'A line that crosses two or more lines.'), ('Are alternate angles always equal?', 'Only when the lines are parallel.'), ('How can I prove lines are parallel?', 'Show that corresponding or alternate angles are equal.')]
    make('geometry-of-straight-lines', 13, 'Space and Shape (Geometry)', 'Grade 8: 3.1 Geometry of straight lines',
         'Recognise and describe pairs of angles formed by perpendicular lines, intersecting lines and parallel lines cut by a transversal; solve geometric problems using the relationships between pairs of angles described above.',
         'Geometry of Straight Lines: Parallel Lines and Transversals', 'Geometry of Straight Lines',
         'Free CAPS Grade 8 geometry worksheets: angles on a line, vertically opposite angles, corresponding, alternate and co-interior angles. 100 questions with memos.',
         'Z: alternate. F: corresponding. C: co-interior = 180°.', 'Only for parallel lines.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
