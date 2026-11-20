# -*- coding: utf-8 -*-
"""
South Africa Grade 8 Maths (CAPS): Transformation Geometry: Translations, Reflections, Rotations and Enlargements (Grade 8: 3.3 Transformation geometry)
  python3 tools/gen_za_maths_g8_transformations.py
Translations, reflections, rotations and enlargements on the coordinate plane, with rules for coordinates (UK Year 8,
Australia Year 7 and Ontario Grade 7 makers).
Wrong answers come from real mistakes: reflecting in the wrong axis, rotating the wrong way, and adding the scale
factor instead of multiplying.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y8_transformations as ukt
adopt(ukt)
if isinstance(getattr(ukt, 'R', None), random.Random): ukt.R = random.Random(808160)
import gen_au_maths_y7_transformations_on_the_cartesian_plane as aut
adopt(aut)
if isinstance(getattr(aut, 'R', None), random.Random): aut.R = random.Random(808161)
import gen_caon_math_g7_transformations as cat
adopt(cat)
if isinstance(getattr(cat, 'R', None), random.Random): cat.R = random.Random(808162)
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
        ("Translations", [("collect", ukt.one_translate, 10), ("collect", aut.one_translate, 10)]),
        ("Reflections", [("collect", ukt.one_reflect, 10), ("collect", aut.one_reflect, 10)]),
        ("Rotations", [("collect", ukt.one_rotate, 10), ("collect", aut.one_rotate, 10)]),
        ("Enlargements", [("collect", ukt.one_enlarge, 10), ("run", cat.set_dilate, ("rnd", cat.People), 10, ok8)]),
        ("Which transformation?", [("collect", aut.one_shape, 10), ("run", cat.set_which, ("rnd", cat.People), 10, ok8)]),
    ], 80816)
    finish(sets, R)
    body = lesson('<ul><li>Translation (x; y) → (x + a; y + b).</li><li>Reflection in the x-axis: (x; y) → (x; −y). In the y-axis: (x; y) → (−x; y). In y = x: (x; y) → (y; x).</li><li>Rotation of 180° about the origin: (x; y) → (−x; −y).</li><li>Enlargement by scale factor k from the origin: (x; y) → (kx; ky).</li></ul>',
        [example("Enlarge (−2; 3) by scale factor 3", ["× 3 each coordinate"], "(−6; 9)")],
        [['The wrong axis', 'Reflecting in the x-axis changes y.'], ['The wrong way', 'Check clockwise or anti-clockwise.'], ['Adding the factor', 'Multiply both coordinates.']])
    faq = [('What does CAPS Grade 8 say about transformations?', 'Recognise, describe and perform transformations with points, line segments and figures on a coordinate plane, including enlargements and reductions.'), ('Does an enlargement keep the angles?', 'Yes.'), ('What does a scale factor of ½ do?', 'It halves every length.'), ('What is the image of (4; −1) reflected in the y-axis?', '(−4; −1).')]
    make('transformation-geometry', 16, 'Space and Shape (Geometry)', 'Grade 8: 3.3 Transformation geometry',
         'Recognise, describe and perform transformations with points, line segments and simple geometric figures on a coordinate plane: reflection in the X-axis or Y-axis, translation within and across quadrants, reflection in the line y = x; identify what the transformation of a point is if given the coordinates of its image; use proportion to describe the effect of enlargement or reduction on area and perimeter of geometric figures.',
         'Transformation Geometry: Translations, Reflections, Rotations and Enlargements', 'Transformation Geometry',
         'Free CAPS Grade 8 transformation worksheets: translations, reflections, rotations and enlargements on the coordinate plane. 100 questions with memos.',
         'Enlarge: multiply both coordinates.', 'Reflect in the x-axis: change the sign of y.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
