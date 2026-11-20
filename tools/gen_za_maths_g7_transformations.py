# -*- coding: utf-8 -*-
"""
South Africa Grade 7 Maths (CAPS): Transformation Geometry: Translations, Reflections and Rotations on a Grid (Grade 7: 3.4 Transformation geometry)
  python3 tools/gen_za_maths_g7_transformations.py
Points on the coordinate grid, translations, reflections and rotations of shapes, and naming the transformation
(Australia Year 7 and BC Grade 7 makers).
Wrong answers come from real mistakes: writing the coordinates the wrong way round, reflecting in the wrong axis,
and rotating the wrong way.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y7_transformations_on_the_cartesian_plane as aut
adopt(aut)
if isinstance(getattr(aut, 'R', None), random.Random): aut.R = random.Random(807210)
import gen_cabc_math_g7_transformations as cbt
adopt(cbt)
if isinstance(getattr(cbt, 'R', None), random.Random): cbt.R = random.Random(807211)
import gen_cabc_math_g7_coordinates as cbc
adopt(cbc)
if isinstance(getattr(cbc, 'R', None), random.Random): cbc.R = random.Random(807212)
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
        ("Coordinates", [("run", cbc.set_read, ("rnd", cbc.People), 10, ok7), ("run", cbc.set_quadrants, ("rnd", cbc.People), 10, ok7)]),
        ("Translations", [("collect", aut.one_translate, 10), ("run", cbt.set_translate, ("rnd", cbt.People), 10, ok7)]),
        ("Reflections", [("collect", aut.one_reflect, 10), ("run", cbt.set_reflect, ("rnd", cbt.People), 10, ok7)]),
        ("Rotations", [("collect", aut.one_rotate, 10), ("run", cbt.set_rotate, ("rnd", cbt.People), 10, ok7)]),
        ("Which transformation?", [("collect", aut.one_shape, 10), ("run", cbt.set_which, ("rnd", cbt.People), 10, ok7)]),
    ], 80721)
    finish(sets, R)
    body = lesson('<ul><li>A point is written (x; y) or (x, y): across first, then up or down.</li><li><b>Translation</b>: every point moves the same distance in the same direction.</li><li><b>Reflection</b> in the x-axis changes the sign of y; in the y-axis it changes the sign of x.</li><li><b>Rotation</b> of 180° about the origin changes both signs.</li></ul>',
        [example("Reflect (3, −2) in the y-axis", ["change the sign of x"], "(−3, −2)")],
        [['The wrong way round', 'x first, then y.'], ['The wrong axis', 'Reflecting in the x-axis changes y.'], ['The wrong direction', 'Check clockwise or anti-clockwise.']])
    faq = [('What does CAPS Grade 7 say about transformations?', 'Recognise, describe and perform translations, reflections and rotations with geometric figures and shapes on squared paper, and use the coordinate grid.'), ('Does a transformation change the size?', 'Translations, reflections and rotations do not.'), ('What is the origin?', 'The point (0, 0).'), ('Which quadrant is (−2, 5) in?', 'The second quadrant.')]
    make('transformation-geometry', 21, 'Space and Shape (Geometry)', 'Grade 7: 3.4 Transformation geometry',
         'Recognise, describe and perform transformations with points on a coordinate plane, focusing on reflecting a point in the X-axis or Y-axis, translating a point within and across quadrants; recognise, describe and perform transformations with triangles on squared paper, including translations, reflections and rotations.',
         'Transformation Geometry: Translations, Reflections and Rotations on a Grid', 'Transformation Geometry',
         'Free CAPS Grade 7 transformation geometry worksheets: coordinates, translations, reflections and rotations on a grid. 100 questions with memos.',
         'x first, then y.', 'Reflect in the y-axis: change the sign of x.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
