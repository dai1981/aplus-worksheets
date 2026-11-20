# -*- coding: utf-8 -*-
"""
South Africa Grade 7 Maths (CAPS): Geometry of Straight Lines: Angles on a Line, at a Point and Vertically Opposite Angles (Grade 7: 3.1 Geometry of straight lines)
  python3 tools/gen_za_maths_g7_straight_lines.py
Angles on a straight line, angles around a point, vertically opposite angles, naming angles and measuring them (UK
Year 7, BC Grade 6 and Ontario Grade 6 makers).
Wrong answers come from real mistakes: using 360° for a straight line, thinking vertically opposite angles add to
180°, and reading the wrong scale on a protractor.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y7_angles as uka
adopt(uka)
if isinstance(getattr(uka, 'R', None), random.Random): uka.R = random.Random(807180)
import gen_cabc_math_g6_angles as cba
adopt(cba)
if isinstance(getattr(cba, 'R', None), random.Random): cba.R = random.Random(807181)
import gen_caon_math_g6_angles as caa
adopt(caa)
if isinstance(getattr(caa, 'R', None), random.Random): caa.R = random.Random(807182)
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
        ("Kinds of angles", [("run", cba.set_classify, ("rnd", cba.People), 10, ok7), ("run", caa.set_names, ("rnd", caa.People), 10, ok7)]),
        ("Angles on a straight line", [("collect", uka.one_line, 20)]),
        ("Angles around a point", [("collect", uka.one_point, 20)]),
        ("Vertically opposite angles", [("collect", uka.one_vopp, 10), ("collect", uka.one_vopp2, 10)]),
        ("Angle problems", [("run", uka.problems, (), 10, ok7), ("run", cba.set_line_point, ("rnd", cba.People), 10, ok7)]),
    ], 80718)
    finish(sets, R)
    body = lesson('<ul><li>Angles on a straight line add up to 180°.</li><li>Angles around a point add up to 360°.</li><li>When two lines cross, the vertically opposite angles are equal.</li><li>Perpendicular lines meet at 90°. Parallel lines never meet.</li></ul>',
        [example("Two angles on a line: 115° and x", ["180 − 115"], "x = 65°")],
        [['360° on a line', 'A straight line is 180°.'], ['Vertically opposite add to 180°', 'They are equal.'], ['The wrong scale', 'Start from 0° on one arm.']])
    faq = [('What does CAPS Grade 7 say about straight lines?', 'Recognise and describe line segments, rays, straight lines, parallel and perpendicular lines, and angles on a line, around a point and vertically opposite angles.'), ('What is a ray?', 'A line with one end point.'), ('What is a reflex angle?', 'Between 180° and 360°.'), ('Are all angles at a point 360° together?', 'Yes.')]
    make('geometry-of-straight-lines', 18, 'Space and Shape (Geometry)', 'Grade 7: 3.1 Geometry of straight lines',
         'Recognise and describe pairs of lines: parallel, perpendicular and intersecting lines; recognise and describe angles on a straight line, angles around a point and vertically opposite angles; classify and measure angles.',
         'Geometry of Straight Lines: Angles on a Line, at a Point and Vertically Opposite Angles', 'Geometry of Straight Lines',
         'Free CAPS Grade 7 geometry worksheets: kinds of angles, angles on a straight line, around a point and vertically opposite angles. 100 questions with memos.',
         'Line: 180°. Point: 360°.', 'Vertically opposite angles are equal.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
