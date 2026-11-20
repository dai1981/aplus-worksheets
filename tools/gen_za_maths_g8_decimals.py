# -*- coding: utf-8 -*-
"""
South Africa Grade 8 Maths (CAPS): Decimal Fractions: Recurring Decimals, Rounding and Calculations (Grade 8: 1.5 Decimal fractions)
  python3 tools/gen_za_maths_g8_decimals.py
Terminating and recurring decimals, changing between fractions and decimals, rounding, and calculating with decimals
(Australia Year 8, UK Year 7 and Ontario Grade 7 makers) in decimal comma form.
Wrong answers come from real mistakes: writing 1/3 as 0,3, putting the comma in the wrong place in a product, and
rounding the wrong digit.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y8_irrational_numbers_and_recurring_decimals as aui
adopt(aui)
if isinstance(getattr(aui, 'R', None), random.Random): aui.R = random.Random(808070)
import gen_uk_maths_y7_rounding_and_estimation as ukr
adopt(ukr)
if isinstance(getattr(ukr, 'R', None), random.Random): ukr.R = random.Random(808071)
import gen_caon_math_g7_decimals as cad
adopt(cad)
if isinstance(getattr(cad, 'R', None), random.Random): cad.R = random.Random(808072)
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
        ("Terminating or recurring?", [("collect", aui.one_tr, 20)]),
        ("Fractions to decimals", [("collect", aui.one_f2d, 20)]),
        ("Decimals to fractions", [("collect", aui.one_d2f, 20)]),
        ("Round off", [("collect", ukr.one_dp, 10), ("collect", ukr.one_sf, 10)]),
        ("Calculate with decimals", [("run", cad.set_multiply, (), 10, ok8), ("run", cad.set_div_dec, (), 10, ok8)]),
    ], 80807)
    finish(sets, R)
    body = lesson("<ul><li>Some fractions give terminating decimals: <span class='fr'><span class='fn'>3</span><span class='fd'>8</span></span> = 0,375.</li><li>Others give recurring decimals: <span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span> = 0,333… = 0,3̇.</li><li>A fraction in simplest form terminates only if its denominator has no prime factors other than 2 and 5.</li><li>Multiply decimals as whole numbers, then count the decimal places.</li></ul>",
        [example("<span class='fr'><span class='fn'>5</span><span class='fd'>11</span></span>", ["5 ÷ 11 = 0,4545…"], "0,45 recurring")],
        [['1/3 = 0,3', '0,3 = 3/10; 1/3 = 0,333…'], ['The comma', 'Count the decimal places.'], ['The wrong digit', 'Look one place to the right.']])
    faq = [('What does CAPS Grade 8 say about decimals?', 'Count, order and compare decimals, use recurring decimals, and calculate with decimal fractions, including squares and roots.'), ('Is 2/7 a recurring decimal?', 'Yes.'), ('What is 0,25 as a fraction?', '1/4.'), ('How do I show a recurring digit?', 'With a dot or a bar over it.')]
    make('decimal-fractions', 7, 'Numbers, Operations and Relationships', 'Grade 8: 1.5 Decimal fractions',
         'Count forwards and backwards in decimal fractions; compare and order decimal fractions; recognise and use equivalent forms of common fractions, decimal fractions and percentages, including recurring decimals; multiply and divide decimal fractions; calculate squares, cubes, square roots and cube roots of decimal fractions.',
         'Decimal Fractions: Recurring Decimals, Rounding and Calculations', 'Decimal Fractions',
         'Free CAPS Grade 8 decimal fractions worksheets: terminating and recurring decimals, fractions and decimals, rounding and calculations. 100 questions with memos.',
         'Denominator with only 2s and 5s: terminating.', 'Count the decimal places in a product.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
