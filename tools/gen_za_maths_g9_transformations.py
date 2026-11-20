# -*- coding: utf-8 -*-
"""
South Africa Grade 9 Maths (CAPS): Transformation Geometry: Coordinates, Rules and Enlargements (Grade 9: 3.3 Transformation geometry)
  python3 tools/gen_za_maths_g9_transformations.py
Translations, reflections, rotations and enlargements on the coordinate plane with coordinate rules (UK Year 8,
Australia Year 7 and Ontario Grade 7 makers).
Wrong answers come from real mistakes: reflecting in the wrong axis, rotating the wrong way, and forgetting that an
enlargement multiplies the area by the square of the scale factor.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y8_transformations as ukt
adopt(ukt)
if isinstance(getattr(ukt, 'R', None), random.Random): ukt.R = random.Random(809140)
import gen_au_maths_y7_transformations_on_the_cartesian_plane as aut
adopt(aut)
if isinstance(getattr(aut, 'R', None), random.Random): aut.R = random.Random(809141)
import gen_caon_math_g7_transformations as cat
adopt(cat)
if isinstance(getattr(cat, 'R', None), random.Random): cat.R = random.Random(809142)
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
        ("Translations", [("collect", ukt.one_translate, 10), ("run", cat.set_translate, ("rnd", cat.People), 10, ok9)]),
        ("Reflections", [("collect", ukt.one_reflect, 10), ("run", cat.set_reflect, ("rnd", cat.People), 10, ok9)]),
        ("Rotations", [("collect", ukt.one_rotate, 10), ("run", cat.set_rotate, ("rnd", cat.People), 10, ok9)]),
        ("Enlargements", [("collect", ukt.one_enlarge, 10), ("run", cat.set_dilate, ("rnd", cat.People), 10, ok9)]),
        ("Which transformation?", [("collect", aut.one_shape, 10), ("run", cat.set_which, ("rnd", cat.People), 10, ok9)]),
    ], 80914)
    finish(sets, R)
    body = lesson('<ul><li>Translation: (x; y) → (x + a; y + b).</li><li>Reflection in the y-axis: (x; y) → (−x; y); in y = x: (x; y) → (y; x).</li><li>Rotation of 90° clockwise about the origin: (x; y) → (y; −x).</li><li>Enlargement by k: (x; y) → (kx; ky). Lengths × k, area × k².</li></ul>',
        [example("Enlarge a 3 cm² shape by scale factor 2", ["area × 2²"], "12 cm²")],
        [['The wrong axis', 'Reflect in the y-axis: change x.'], ['The wrong way', 'Check clockwise or anti-clockwise.'], ['Area × k', 'Area changes by k².']])
    faq = [('What does CAPS Grade 9 say about transformations?', 'Recognise, describe and perform transformations with points, line segments and figures on a coordinate plane, and investigate the effect of enlargement on area and perimeter.'), ('What happens to the perimeter in an enlargement by 3?', 'It is 3 times as long.'), ('What is the image of (2; 5) reflected in y = x?', '(5; 2).'), ('Is a reflection a rigid transformation?', 'Yes, it keeps the size and shape.')]
    make('transformation-geometry', 14, 'Space and Shape (Geometry)', 'Grade 9: 3.3 Transformation geometry',
         'Recognise, describe and perform transformations with points, line segments and simple geometric figures on a coordinate plane, including reflection in the line y = x; identify what the transformation of a point is if given the coordinates of its image; use proportion to describe the effect of enlargement or reduction on area and perimeter of geometric figures.',
         'Transformation Geometry: Coordinates, Rules and Enlargements', 'Transformation Geometry',
         'Free CAPS Grade 9 transformation worksheets: translations, reflections, rotations and enlargements with coordinate rules. 100 questions with memos.',
         'Enlarge by k: lengths × k, area × k².', 'Reflect in y = x: swap x and y.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
