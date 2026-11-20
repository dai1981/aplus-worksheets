# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): Addition and Subtraction of 5-Digit Numbers (Grade 5: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g5_add_sub.py
Column addition and subtraction of numbers with at least 5 digits, mental strategies, checking and estimating, and
word problems (UK Year 5 and BC Grade 5 makers with South African names and numbers).
Wrong answers come from real mistakes: forgetting to carry, borrowing across a 0 wrongly, and misplacing digits in
the columns.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y5_column_add_sub as ukc
adopt(ukc)
if isinstance(getattr(ukc, 'R', None), random.Random): ukc.R = random.Random(805030)
import gen_cabc_math_g5_add_sub as cba
adopt(cba)
if isinstance(getattr(cba, 'R', None), random.Random): cba.R = random.Random(805031)
za_common.GRADE = "grade-5"


import re as _re


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def _nums(it):
    return [int(x.replace(",", "").replace("\u00a0", "")) for x in _re.findall(r"(?<![\d.])\d[\d,\u00a0]*(?![.\d])", _txt(it)) if x.replace(",", "").replace("\u00a0", "").isdigit()]


def six(it):
    """whole numbers to 6 digits, no decimals, no negatives"""
    t = _txt(it)
    return all(n <= 999999 for n in _nums(it)) and not _re.search(r"\d\.\d|−\d", t)


def nodec(it):
    return not _re.search(r"\d\.\d|−\d", _txt(it))


def den12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " " + it["c"][it["a"]])]
    return all(d <= 12 for d in ds) and nodec(it)



def build():
    sets, R = build_sets([
        ("Add 5-digit numbers", [("run", ukc.set_add, ("rnd", "seen"), 20, six)]),
        ("Subtract 5-digit numbers", [("run", ukc.set_sub, ("rnd", "seen"), 20, six)]),
        ("Mental addition and subtraction", [("run", ukc.set_mental, ("rnd",), 15, six), ("run", cba.set_add, ("rnd", "seen"), 5, six)]),
        ("Estimate and check", [("run", cba.set_estimate, ("rnd", cba.People), 10, six), ("run", ukc.set_check, ("rnd",), 10, six)]),
        ("Addition and subtraction problems", [("run", ukc.set_story, ("rnd",), 20, six)]),
    ], 80503)
    finish(sets, R)
    body = lesson('<ul><li>Write the numbers in columns with the units lined up.</li><li>Carry 1 to the next column when a column adds to 10 or more.</li><li>Borrow from the next column when the top digit is too small. Across a 0, borrow from the next place that is not 0.</li><li>Estimate first, and check subtraction with addition.</li></ul>',
        [example("60 204 − 27 586", ["borrow across the zeros", "check: 32 618 + 27 586 = 60 204"], "32 618")],
        [['Forgetting to carry', 'Write the carried 1 above the next column.'], ['Borrowing across 0', 'Go to the next place that is not 0.'], ['Wrong columns', 'Line up the units.']])
    faq = [('What does CAPS Grade 5 say about addition and subtraction?', 'Add and subtract whole numbers of at least 5 digits, using estimation, building up and breaking down numbers, rounding off and compensating, and inverse operations.'), ('How do I check my answer?', 'Estimate first, and use the inverse operation.'), ('What is borrowing?', 'Exchanging 1 from the next place for 10 in this place.'), ('Why line up the units?', 'So each digit is added to the same place.')]
    make('addition-and-subtraction', 3, 'Numbers, Operations and Relationships', 'Grade 5: 1.1 Whole numbers',
         'Add and subtract whole numbers of at least 5 digits; use techniques such as estimation, building up and breaking down numbers, rounding off and compensating, and addition and subtraction as inverse operations.',
         'Addition and Subtraction of 5-Digit Numbers', 'Addition and Subtraction',
         'Free CAPS Grade 5 addition and subtraction worksheets: 5-digit column addition and subtraction, mental strategies, estimating, checking and word problems. 100 questions with memos.',
         'Line up the units; carry and borrow carefully.', 'Check subtraction with addition.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
