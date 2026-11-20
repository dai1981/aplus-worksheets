# -*- coding: utf-8 -*-
"""
South Africa Grade 9 Maths (CAPS): Similar and Congruent Triangles (Grade 9: 3.1 Geometry of 2D shapes)
  python3 tools/gen_za_maths_g9_triangles.py
Angles in triangles, conditions for congruence, similar triangles and scale factors, and deciding whether triangles are
similar or congruent (Singapore Secondary 1 and Secondary 2 and Australia Year 7 makers).
Wrong answers come from real mistakes: thinking AAA proves congruence, matching the wrong sides, and adding instead of
multiplying with a scale factor.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_sg_maths_s1_angles_triangles_and_quadrilaterals as sga
adopt(sga)
if isinstance(getattr(sga, 'R', None), random.Random): sga.R = random.Random(809120)
import gen_au_maths_y7_angle_sum_of_triangles_and_polygons as aua
adopt(aua)
if isinstance(getattr(aua, 'R', None), random.Random): aua.R = random.Random(809121)
import gen_sg_maths_s2_congruence_and_similarity as sgc
adopt(sgc)
if isinstance(getattr(sgc, 'R', None), random.Random): sgc.R = random.Random(809122)
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
        ("Angles in triangles", [("collect", sga.one_tri, 10), ("collect", aua.one_ext, 10)]),
        ("Congruent triangles", [("collect", sgc.one_congruence, 11), ("collect", sga.one_tri, 9)]),
        ("Scale factors", [("collect", sgc.one_sf, 20)]),
        ("Similar triangles", [("collect", sgc.one_tri, 20)]),
        ("Similar or congruent?", [("collect", sgc.one_check, 20)]),
    ], 80912)
    finish(sets, R)
    body = lesson('<ul><li>Congruent triangles are identical: SSS, SAS, AAS or RHS.</li><li>Similar triangles have equal angles and sides in proportion.</li><li>Match corresponding sides by the equal angles.</li><li>Scale factor = a side of one triangle ÷ the matching side of the other.</li></ul>',
        [example("Similar triangles: 6 ↔ 9, 8 ↔ ?", ["scale factor 1,5"], "12")],
        [['AAA for congruence', 'Equal angles prove similarity only.'], ['Wrong sides', 'Match sides opposite equal angles.'], ['Adding the factor', 'Multiply.']])
    faq = [('What does CAPS Grade 9 say about triangles?', 'Establish the minimum conditions for congruent and similar triangles and use them to solve problems.'), ('Is SSA a congruence condition?', 'No, except RHS for right-angled triangles.'), ('What is the scale factor of congruent triangles?', '1.'), ('Are all equilateral triangles similar?', 'Yes.')]
    make('similar-and-congruent-triangles', 12, 'Space and Shape (Geometry)', 'Grade 9: 3.1 Geometry of 2D shapes',
         'Through investigation, establish the minimum conditions for congruent triangles; through investigation, establish the minimum conditions for similar triangles; solve geometric problems involving unknown sides and angles in triangles, using known properties of triangles, as well as definitions of congruence and similarity.',
         'Similar and Congruent Triangles', 'Similar and Congruent Triangles',
         'Free CAPS Grade 9 worksheets: angles in triangles, congruent triangles, similar triangles and scale factors. 100 questions with memos.',
         'Congruent: SSS, SAS, AAS, RHS.', 'Similar: equal angles, sides in proportion.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
