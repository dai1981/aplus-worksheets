# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Multiplying and Dividing Decimal Fractions (Grade 6: 1.3 Decimal fractions)
  python3 tools/gen_za_maths_g6_mult_div_decimals.py
Multiplying and dividing decimals by 10, 100 and 1 000, multiplying and dividing decimals by whole numbers, and
problems (Australia Year 6, Ontario Grade 6 and UK Year 6 makers), in South African decimal comma form.
Wrong answers come from real mistakes: adding a 0 instead of moving the digits, putting the comma in the wrong place,
and forgetting the comma in the answer.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y6_powers_of_10 as aup
adopt(aup)
if isinstance(getattr(aup, 'R', None), random.Random): aup.R = random.Random(806140)
import gen_caon_math_g6_mult_div_decimals as cam
adopt(cam)
if isinstance(getattr(cam, 'R', None), random.Random): cam.R = random.Random(806141)
import gen_uk_maths_y6_decimal_calculations as ukd
adopt(ukd)
if isinstance(getattr(ukd, 'R', None), random.Random): ukd.R = random.Random(806142)
import gen_cabc_math_g6_decimals as cbd
adopt(cbd)
if isinstance(getattr(cbd, 'R', None), random.Random): cbd.R = random.Random(806143)
za_common.GRADE = "grade-6"


import re as _re


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def _nums(it):
    return [int(x.replace(",", "").replace("\u00a0", "")) for x in _re.findall(r"(?<![\d.])\d[\d,\u00a0]*(?![.\d])", _txt(it)) if x.replace(",", "").replace("\u00a0", "").isdigit()]


def noneg(it):
    return not _re.search(r"(?<![\d)] )[−-]\d", _txt(it)) and "negative" not in _txt(it).lower()


def nine(it):
    """whole numbers to 9 digits, no negatives"""
    return all(n <= 999999999 for n in _nums(it)) and noneg(it)


def dec3(it):
    """decimals with at most 3 places, no negatives"""
    return noneg(it) and not _re.search(r"\d\.\d{4}", _txt(it))


def nodec(it):
    return noneg(it) and not _re.search(r"\d\.\d", _txt(it))


def flat(it):
    """first quadrant only: no negative numbers in the text or the picture"""
    return nodec(it) and "−" not in it["q"] and "-1" not in it["q"]


def nomean(it):
    return dec3(it) and not _re.search(r"\bmean\b", _txt(it))


def den12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " " + it["c"][it["a"]])]
    return all(d <= 12 or d in (20, 25, 50, 100) for d in ds) and nodec(it)



def build():
    sets, R = build_sets([
        ("× and ÷ by 10, 100 and 1 000", [("run", aup.set_p10, (), 10, dec3), ("run", ukd.set_powers, (), 10, dec3)]),
        ("Multiply decimals by whole numbers", [("run", cam.set_mul_tenths, (), 10, dec3), ("run", ukd.set_multiply, (), 10, dec3)]),
        ("Divide decimals by whole numbers", [("run", cam.set_div_whole, (), 10, dec3), ("run", ukd.set_divide, (), 10, dec3)]),
        ("Estimate", [("run", cbd.set_estimate, (), 10, dec3), ("run", aup.set_estimate, (), 10, dec3)]),
        ("Decimal problems", [("run", cam.set_problems, (), 8, dec3), ("run", cbd.set_problems, (), 6, dec3), ("run", ukd.set_words, (ukd.People,), 6, dec3)]),
    ], 80614)
    finish(sets, R)
    body = lesson('<ul><li>× 10 moves every digit one place to the left; ÷ 10 moves every digit one place to the right.</li><li>3,45 × 100 = 345; 3,45 ÷ 10 = 0,345.</li><li>Decimal × whole number: multiply as whole numbers, then put in the comma. 2,3 × 4: 23 × 4 = 92, so 9,2.</li><li>Estimate to check where the comma goes.</li></ul>',
        [example("4,8 ÷ 6", ["48 ÷ 6 = 8 tenths"], "0,8")],
        [['Adding a 0', '3,45 × 10 = 34,5, not 3,450.'], ['The comma in the wrong place', 'Estimate: 2,3 × 4 is about 8.'], ['No comma', 'Count the decimal places.']])
    faq = [('What does CAPS Grade 6 say about multiplying decimals?', 'Multiply and divide decimal fractions by 10 and 100, and multiply and divide decimal fractions by whole numbers.'), ('What is 0,7 × 100?', '70.'), ('What is 5,6 ÷ 7?', '0,8.'), ('How do I check?', 'Estimate with whole numbers.')]
    make('multiplying-and-dividing-decimals', 14, 'Numbers, Operations and Relationships', 'Grade 6: 1.3 Decimal fractions',
         'Multiply decimal fractions by 10 and 100; divide decimal fractions by 10 and 100; multiply and divide decimal fractions by whole numbers; solve problems in context involving decimal fractions.',
         'Multiplying and Dividing Decimal Fractions', 'Multiplying and Dividing Decimals',
         'Free CAPS Grade 6 worksheets: multiplying and dividing decimals by 10, 100 and 1 000 and by whole numbers, estimating and problems. 100 questions with memos.',
         '× 10: digits move left. ÷ 10: digits move right.', 'Estimate to place the comma.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
