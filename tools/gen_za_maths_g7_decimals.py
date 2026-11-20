# -*- coding: utf-8 -*-
"""
South Africa Grade 7 Maths (CAPS): Decimal Fractions: Fractions, Decimals, Percentages and Rounding (Grade 7: 1.5 Decimal fractions)
  python3 tools/gen_za_maths_g7_decimals.py
Changing between common fractions, decimals and percentages, ordering decimals, and rounding off to decimal places
(UK Year 7 and Australia Year 7 makers) in South African decimal comma form.
Wrong answers come from real mistakes: thinking a longer decimal is bigger, writing 3/8 as 3,8, and rounding the wrong
digit.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y7_fractions_decimals_and_percentages as ukf
adopt(ukf)
if isinstance(getattr(ukf, 'R', None), random.Random): ukf.R = random.Random(807110)
import gen_au_maths_y7_fractions_decimals_and_percentages as auf
adopt(auf)
if isinstance(getattr(auf, 'R', None), random.Random): auf.R = random.Random(807111)
import gen_uk_maths_y7_rounding_and_estimation as ukr
adopt(ukr)
if isinstance(getattr(ukr, 'R', None), random.Random): ukr.R = random.Random(807112)
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
        ("Fractions to decimals", [("collect", ukf.one_f2d, 10), ("collect", auf.one_f2d, 10)]),
        ("Decimals to fractions", [("collect", ukf.one_d2f, 10), ("collect", auf.one_d2f, 10)]),
        ("Percentages", [("collect", ukf.one_2p, 10), ("collect", ukf.one_equiv, 10)]),
        ("Order decimals", [("collect", ukf.one_order, 10), ("collect", auf.one_nl, 10)]),
        ("Round off to decimal places", [("collect", ukr.one_dp, 10), ("collect", ukr.one_dp_zero, 10)]),
    ], 80711)
    finish(sets, R)
    body = lesson("<ul><li>Fraction to decimal: divide the numerator by the denominator. <span class='fr'><span class='fn'>3</span><span class='fd'>8</span></span> = 3 ÷ 8 = 0,375.</li><li>Decimal to fraction: use the place value. 0,45 = <span class='fr'><span class='fn'>45</span><span class='fd'>100</span></span> = <span class='fr'><span class='fn'>9</span><span class='fd'>20</span></span>.</li><li>Decimal to percentage: × 100. 0,375 = 37,5%.</li><li>To round to 2 decimal places, look at the third decimal digit.</li></ul>",
        [example("Order 0,7; 0,65; 0,705", ["0,700; 0,650; 0,705"], "0,65; 0,7; 0,705")],
        [['Longer is bigger', '0,65 &lt; 0,7.'], ['3/8 as 3,8', 'Divide: 3 ÷ 8.'], ['The wrong digit', 'Look one place to the right.']])
    faq = [('What does CAPS Grade 7 say about decimals?', 'Count, order and compare decimal fractions to at least 3 decimal places, round off decimals, and convert between common fractions, decimals and percentages.'), ('What is 1/4 as a decimal?', '0,25.'), ('What is 0,8 as a percentage?', '80%.'), ('What is 2,456 to 1 decimal place?', '2,5.')]
    make('decimal-fractions', 11, 'Numbers, Operations and Relationships', 'Grade 7: 1.5 Decimal fractions',
         'Count forwards and backwards in decimal fractions to at least three decimal places; compare and order decimal fractions to at least 3 decimal places; round off decimal fractions to at least 2 decimal places; recognise equivalence between common fraction, decimal fraction and percentage forms of the same number.',
         'Decimal Fractions: Fractions, Decimals, Percentages and Rounding', 'Decimal Fractions',
         'Free CAPS Grade 7 decimal fractions worksheets: fractions, decimals and percentages, ordering decimals and rounding to decimal places. 100 questions with memos.',
         'Fraction → decimal: divide.', 'Line up the commas to compare.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
