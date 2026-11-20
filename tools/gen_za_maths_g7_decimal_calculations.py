# -*- coding: utf-8 -*-
"""
South Africa Grade 7 Maths (CAPS): Calculating with Decimal Fractions (Grade 7: 1.5 Decimal fractions)
  python3 tools/gen_za_maths_g7_decimal_calculations.py
Adding and subtracting decimals, multiplying decimals by whole numbers and decimals, dividing decimals by whole
numbers, estimating and problems (BC Grade 7, Ontario Grade 7 and UK Year 6 makers) in decimal comma form.
Wrong answers come from real mistakes: lining up the last digits instead of the commas, putting the comma in the wrong
place in a product, and forgetting to fill empty places with 0.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_cabc_math_g7_add_sub_decimals as cba
adopt(cba)
if isinstance(getattr(cba, 'R', None), random.Random): cba.R = random.Random(807120)
import gen_cabc_math_g7_mult_div_decimals as cbm
adopt(cbm)
if isinstance(getattr(cbm, 'R', None), random.Random): cbm.R = random.Random(807121)
import gen_caon_math_g7_decimals as cad
adopt(cad)
if isinstance(getattr(cad, 'R', None), random.Random): cad.R = random.Random(807122)
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
        ("Add and subtract decimals", [("run", cba.set_line_up, (cba.People, "rnd", "seen"), 10, noneg), ("run", cba.set_zeros, (cba.People, "rnd", "seen"), 10, noneg)]),
        ("Multiply decimals", [("run", cbm.set_multiply, (), 10, noneg), ("run", cad.set_multiply, (), 10, noneg)]),
        ("Divide decimals", [("run", cbm.set_div_whole, (), 10, noneg), ("run", cbm.set_div_dec, (), 10, noneg)]),
        ("Estimate", [("run", cbm.set_estimate, (), 10, noneg), ("run", cad.set_estimate, (), 10, noneg)]),
        ("Decimal problems", [("run", cbm.set_words, (), 3, noneg), ("run", cad.set_words, (), 12, noneg), ("run", cba.set_words, (cba.People,), 5, noneg)]),
    ], 80712)
    finish(sets, R)
    body = lesson('<ul><li>To add or subtract, line up the decimal commas and fill empty places with 0.</li><li>To multiply, multiply as whole numbers, then count the decimal places: 0,3 × 0,4 = 0,12.</li><li>To divide by a whole number, divide as usual and keep the comma in line.</li><li>Estimate first to check where the comma goes.</li></ul>',
        [example("2,4 × 1,5", ["24 × 15 = 360", "2 decimal places"], "3,60 = 3,6")],
        [['Lining up the last digits', 'Line up the commas.'], ['The comma in the wrong place', 'Count the decimal places.'], ['An empty place', 'Write 0 in it.']])
    faq = [('What does CAPS Grade 7 say about decimal calculations?', 'Add, subtract and multiply decimal fractions to at least 3 decimal places, and divide decimal fractions by whole numbers.'), ('What is 0,5 × 0,5?', '0,25.'), ('What is 4,8 ÷ 4?', '1,2.'), ('How do I check?', 'Estimate with whole numbers.')]
    make('calculating-with-decimals', 12, 'Numbers, Operations and Relationships', 'Grade 7: 1.5 Decimal fractions',
         'Add and subtract decimal fractions of at least three decimal places; multiply decimal fractions by whole numbers and by decimal fractions; divide decimal fractions by whole numbers; solve problems in context involving decimal fractions.',
         'Calculating with Decimal Fractions', 'Calculating with Decimals',
         'Free CAPS Grade 7 worksheets: adding, subtracting, multiplying and dividing decimals, estimating and decimal problems. 100 questions with memos.',
         'Count the decimal places in a product.', 'Line up the commas to add.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
