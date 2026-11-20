# -*- coding: utf-8 -*-
"""
South Africa Grade 9 Maths (CAPS): Real Numbers: Rational and Irrational Numbers, Roots and Rounding (Grade 9: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g9_real_numbers.py
Rational and irrational numbers, recurring decimals, estimating roots, and rounding to significant figures (Australia
Year 7 and Year 8, UK Year 9 and Singapore Secondary 1 makers).
Wrong answers come from real mistakes: calling every decimal irrational, thinking √16 is irrational, and counting
leading zeros as significant figures.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y8_irrational_numbers_and_recurring_decimals as aui
adopt(aui)
if isinstance(getattr(aui, 'R', None), random.Random): aui.R = random.Random(809010)
import gen_au_maths_y7_square_numbers_and_square_roots as aus
adopt(aus)
if isinstance(getattr(aus, 'R', None), random.Random): aus.R = random.Random(809011)
import gen_uk_maths_y9_rounding_and_error_intervals as ukr
adopt(ukr)
if isinstance(getattr(ukr, 'R', None), random.Random): ukr.R = random.Random(809012)
import gen_sg_maths_s1_approximation_and_estimation as sga
adopt(sga)
if isinstance(getattr(sga, 'R', None), random.Random): sga.R = random.Random(809013)
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
        ("Rational or irrational?", [("collect", aui.one_ri, 20)]),
        ("Recurring decimals", [("collect", aui.one_tr, 10), ("collect", aui.one_d2f, 10)]),
        ("Estimate roots", [("collect", aus.one_est, 20)]),
        ("Significant figures", [("collect", ukr.one_sf_big, 10), ("collect", ukr.one_small, 10)]),
        ("Estimate and approximate", [("collect", sga.one_est, 10), ("collect", sga.one_mixed, 10)]),
    ], 80901)
    finish(sets, R)
    body = lesson("<ul><li>A <b>rational</b> number can be written as a fraction <span class='fr'><span class='fn'>a</span><span class='fd'>b</span></span>: terminating and recurring decimals are rational.</li><li>An <b>irrational</b> number cannot: √2, √7 and π never end or repeat.</li><li>√50 is between 7 and 8 because 49 &lt; 50 &lt; 64.</li><li>Significant figures start at the first non-zero digit: 0,004 07 has 3 significant figures.</li></ul>",
        [example("Is √0,25 rational?", ["√0,25 = 0,5"], "yes, rational")],
        [['Every decimal is irrational', '0,333… is rational.'], ['√16 irrational', '√16 = 4.'], ['Leading zeros', 'They are not significant.']])
    faq = [('What does CAPS Grade 9 say about real numbers?', 'Describe the real number system by recognising, defining and distinguishing properties of natural numbers, whole numbers, integers, rational and irrational numbers.'), ('Is π rational?', 'No.'), ('Between which integers is √30?', '5 and 6.'), ('Is 0 rational?', 'Yes, 0 = 0/1.')]
    make('real-numbers', 1, 'Numbers, Operations and Relationships', 'Grade 9: 1.1 Whole numbers',
         'Describe the real number system by recognising, defining and distinguishing properties of natural numbers, whole numbers, integers, rational numbers and irrational numbers; recognise and use rounding off and estimation.',
         'Real Numbers: Rational and Irrational Numbers, Roots and Rounding', 'Real Numbers',
         'Free CAPS Grade 9 real numbers worksheets: rational and irrational numbers, recurring decimals, estimating roots and significant figures. 100 questions with memos.',
         'Rational: can be written as a fraction.', '√2 and π are irrational.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
