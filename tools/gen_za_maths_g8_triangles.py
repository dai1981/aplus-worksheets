# -*- coding: utf-8 -*-
"""
South Africa Grade 8 Maths (CAPS): Triangles: Angle Properties, Congruence and Similarity (Grade 8: 3.2 Geometry of 2D shapes)
  python3 tools/gen_za_maths_g8_triangles.py
Angles in a triangle and exterior angles, conditions for congruence, similar triangles and scale factors (UK Year 7 and
Year 9 and Australia Year 7 and Year 8 makers).
Wrong answers come from real mistakes: using 360° in a triangle, thinking AAA proves congruence, and adding instead of
multiplying with a scale factor.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y7_angles as uka
adopt(uka)
if isinstance(getattr(uka, 'R', None), random.Random): uka.R = random.Random(808140)
import gen_au_maths_y7_angle_sum_of_triangles_and_polygons as aua
adopt(aua)
if isinstance(getattr(aua, 'R', None), random.Random): aua.R = random.Random(808141)
import gen_au_maths_y8_congruent_and_similar_triangles as auc
adopt(auc)
if isinstance(getattr(auc, 'R', None), random.Random): auc.R = random.Random(808142)
import gen_uk_maths_y9_similarity_and_congruence as uks
adopt(uks)
if isinstance(getattr(uks, 'R', None), random.Random): uks.R = random.Random(808143)
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
        ("Angles in a triangle", [("collect", uka.one_tri, 10), ("collect", aua.one_tri, 10)]),
        ("Exterior angles", [("collect", aua.one_ext, 20)]),
        ("Congruent triangles", [("collect", auc.one_congruence, 10), ("collect", uks.one_sf, 10)]),
        ("Similar triangles", [("collect", auc.one_sf, 10), ("collect", auc.one_tri, 10)]),
        ("Is it congruent or similar?", [("collect", auc.one_check, 10), ("collect", uks.one_check, 10)]),
    ], 80814)
    finish(sets, R)
    body = lesson('<ul><li>The angles of a triangle add up to 180°. An exterior angle equals the sum of the two opposite interior angles.</li><li>Congruent triangles are identical: SSS, SAS, AAS or RHS.</li><li>Similar triangles have equal angles and sides in the same ratio.</li><li>Find the scale factor by dividing a side by its matching side.</li></ul>',
        [example("Similar triangles: 4 cm ↔ 10 cm, 6 cm ↔ ?", ["scale factor 10 ÷ 4 = 2,5"], "6 × 2,5 = 15 cm")],
        [['360° in a triangle', 'A triangle is 180°.'], ['AAA for congruence', 'Equal angles only prove similarity.'], ['Adding the scale factor', 'Multiply by it.']])
    faq = [('What does CAPS Grade 8 say about triangles?', 'Classify triangles, use the angle sum and exterior angle, and identify and describe the properties of congruent and similar triangles.'), ('What does RHS mean?', 'Right angle, hypotenuse, side.'), ('Are congruent triangles similar?', 'Yes, with scale factor 1.'), ('What is an exterior angle?', 'The angle between one side and the extension of the next side.')]
    make('triangles-congruence-and-similarity', 14, 'Space and Shape (Geometry)', 'Grade 8: 3.2 Geometry of 2D shapes',
         'Revise properties and definitions of triangles in terms of their sides and angles; identify and write clear definitions of congruent and similar triangles; solve geometric problems involving unknown sides and angles in triangles using known properties and definitions, including the exterior angle of a triangle.',
         'Triangles: Angle Properties, Congruence and Similarity', 'Triangles',
         'Free CAPS Grade 8 triangles worksheets: angle sums, exterior angles, congruent triangles, similar triangles and scale factors. 100 questions with memos.',
         'Exterior angle = sum of the two opposite interior angles.', 'Similar: equal angles, sides in ratio.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
