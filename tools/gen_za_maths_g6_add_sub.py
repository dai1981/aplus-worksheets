# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Addition and Subtraction of 6-Digit Numbers (Grade 6: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g6_add_sub.py
Column addition and subtraction of numbers with at least 6 digits, estimating and checking, and word problems (UK
Year 5, BC Grade 5 and Australia Year 6 makers with South African names and numbers).
Wrong answers come from real mistakes: forgetting to carry, borrowing across a 0 wrongly, and misplacing digits in
the columns.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y5_column_add_sub as ukc
adopt(ukc)
if isinstance(getattr(ukc, 'R', None), random.Random): ukc.R = random.Random(806030)
import gen_cabc_math_g5_add_sub as cba
adopt(cba)
if isinstance(getattr(cba, 'R', None), random.Random): cba.R = random.Random(806031)
import gen_au_maths_y6_estimation as aue
adopt(aue)
if isinstance(getattr(aue, 'R', None), random.Random): aue.R = random.Random(806032)
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
        ("Add big numbers", [("run", cba.set_add, ("rnd", "seen"), 20, nine)]),
        ("Subtract big numbers", [("run", cba.set_sub, ("rnd", "seen"), 20, nine)]),
        ("Mental addition and subtraction", [("run", ukc.set_mental, ("rnd",), 20, nine)]),
        ("Estimate and check", [("run", aue.set_round, (), 10, nine), ("run", cba.set_inverse, ("rnd", cba.People), 10, nine)]),
        ("Addition and subtraction problems", [("run", ukc.set_story, ("rnd",), 13, nine), ("run", cba.set_story, (cba.People,), 7, nine)]),
    ], 80603)
    finish(sets, R)
    body = lesson('<ul><li>Write the numbers in columns with the units lined up.</li><li>Carry 1 to the next column when a column adds to 10 or more.</li><li>Borrow from the next column when the top digit is too small. Across a 0, borrow from the next place that is not 0.</li><li>Estimate first, and check subtraction with addition.</li></ul>',
        [example("500 000 − 236 457", ["borrow across the zeros", "check: 263 543 + 236 457 = 500 000"], "263 543")],
        [['Forgetting to carry', 'Write the carried 1 above the next column.'], ['Borrowing across 0', 'Go to the next place that is not 0.'], ['Wrong columns', 'Line up the units.']])
    faq = [('What does CAPS Grade 6 say about addition and subtraction?', 'Add and subtract whole numbers of at least 6 digits, using estimation, rounding off, compensating and inverse operations to check.'), ('How do I check a subtraction?', 'Add the answer to the number you took away.'), ('Why estimate first?', 'To see if the answer is sensible.'), ('What is a column method?', 'Writing the numbers under each other by place value.')]
    make('addition-and-subtraction', 3, 'Numbers, Operations and Relationships', 'Grade 6: 1.1 Whole numbers',
         'Add and subtract whole numbers of at least 6 digits; use a range of techniques to perform and check written and mental calculations, including estimation, adding and subtracting in columns, building up and breaking down numbers, rounding off and compensating, and using addition and subtraction as inverse operations.',
         'Addition and Subtraction of 6-Digit Numbers', 'Addition and Subtraction',
         'Free CAPS Grade 6 addition and subtraction worksheets: 6-digit column addition and subtraction, mental strategies, estimating and word problems. 100 questions with memos.',
         'Line up the units; carry and borrow carefully.', 'Check subtraction with addition.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
