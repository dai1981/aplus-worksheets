# -*- coding: utf-8 -*-
"""
South Africa Grade 8 Maths (CAPS): The Theorem of Pythagoras (Grade 8: 4.3 The theorem of Pythagoras)
  python3 tools/gen_za_maths_g8_pythagoras.py
Finding the hypotenuse, finding a shorter side, rounding answers, testing for a right angle, and problems (UK Year 9
and Australia Year 8 makers).
Wrong answers come from real mistakes: adding the squares when finding a shorter side, forgetting the square root,
and using a side that is not the hypotenuse as c.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y9_pythagoras_theorem as ukp
adopt(ukp)
if isinstance(getattr(ukp, 'R', None), random.Random): ukp.R = random.Random(808200)
import gen_au_maths_y8_pythagoras_theorem as aup
adopt(aup)
if isinstance(getattr(aup, 'R', None), random.Random): aup.R = random.Random(808201)
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
        ("Find the hypotenuse", [("collect", ukp.one_hyp, 10), ("collect", aup.one_hyp, 10)]),
        ("Round the answer", [("collect", ukp.one_hyp_dp, 10), ("collect", aup.one_hyp_dp, 10)]),
        ("Find a shorter side", [("collect", ukp.one_short, 10), ("collect", aup.one_short, 10)]),
        ("Is it right-angled?", [("collect", ukp.one_test, 10), ("collect", aup.one_test, 10)]),
        ("Pythagoras problems", [("run", ukp.problems, (), 10, ok8), ("run", aup.problems, (), 10, ok8)]),
    ], 80820)
    finish(sets, R)
    body = lesson('<ul><li>In a right-angled triangle, the hypotenuse c is the longest side, opposite the right angle.</li><li>Theorem of Pythagoras: c² = a² + b².</li><li>For a shorter side: a² = c² − b².</li><li>If c² = a² + b², the triangle has a right angle.</li></ul>',
        [example("Sides 9 cm and 12 cm", ["c² = 81 + 144 = 225"], "c = 15 cm")],
        [['Adding for a short side', 'Subtract: a² = c² − b².'], ['No square root', 'c² = 225 means c = 15.'], ['The wrong c', 'c is the longest side.']])
    faq = [('What does CAPS Grade 8 say about Pythagoras?', 'Investigate the relationship between the lengths of the sides of a right-angled triangle, and use the theorem to calculate a missing length.'), ('Is 5, 12, 13 a right-angled triangle?', 'Yes: 25 + 144 = 169.'), ('What is a Pythagorean triple?', 'Three whole numbers that fit c² = a² + b².'), ('Does it work for every triangle?', 'Only for right-angled triangles.')]
    make('theorem-of-pythagoras', 20, 'Measurement', 'Grade 8: 4.3 The theorem of Pythagoras',
         'Investigate the relationship between the lengths of the sides of a right-angled triangle to develop the Theorem of Pythagoras; determine whether a triangle is a right-angled triangle or not if the length of the three sides of the triangle are known; use the Theorem of Pythagoras to calculate a missing length in a right-angled triangle, leaving irrational answers in surd form.',
         'The Theorem of Pythagoras', 'Theorem of Pythagoras',
         'Free CAPS Grade 8 Pythagoras worksheets: finding the hypotenuse and shorter sides, testing for right angles and problems. 100 questions with memos.',
         'c² = a² + b².', 'c is the longest side.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
