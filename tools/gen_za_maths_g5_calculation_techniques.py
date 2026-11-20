# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): Calculation Techniques: Estimating, Compensating, Doubling and Halving and Inverse Operations (Grade 5: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g5_calculation_techniques.py
Rounding off and compensating, doubling and halving (makers from the Grade 4 generator), estimating and judging
answers (Australia Year 5 makers), and inverse operations (BC Grade 5 maker).
Wrong answers come from real mistakes: compensating the wrong way, doubling only part of a number, and undoing an
operation with the same operation.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_za_maths_g4_calculation_techniques as zc4
adopt(zc4)
if isinstance(getattr(zc4, 'R', None), random.Random): zc4.R = random.Random(805040)
import gen_au_maths_y5_estimation_money as aue
adopt(aue)
if isinstance(getattr(aue, 'R', None), random.Random): aue.R = random.Random(805041)
import gen_cabc_math_g5_add_sub as cba
adopt(cba)
if isinstance(getattr(cba, 'R', None), random.Random): cba.R = random.Random(805042)
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
        ("Rounding off and compensating", [("collect", zc4.uniq(zc4.one_comp), 20)]),
        ("Doubling and halving", [("collect", zc4.uniq(zc4.one_dh), 20)]),
        ("Estimate by rounding", [("run", aue.set_round, (), 20, six)]),
        ("Is the answer reasonable?", [("run", aue.set_reasonable, (aue.People,), 20, six)]),
        ("Inverse operations", [("run", cba.set_inverse, ("rnd", cba.People), 20, six)]),
    ], 80504)
    finish(sets, R)
    body = lesson('<ul><li>Round off and compensate: 3 456 + 198 = 3 456 + 200 − 2.</li><li>Double and halve: 25 × 64 = 50 × 32 = 100 × 16 = 1 600.</li><li>Estimate before you calculate, so you can spot a wrong answer.</li><li>Use inverse operations to check: + and − undo each other, × and ÷ undo each other.</li></ul>',
        [example("8 405 − 997", ["8 405 − 1 000 = 7 405", "add back 3"], "7 408")],
        [['Compensating the wrong way', 'You took away 3 too many, so add 3 back.'], ['Doubling part', 'Double the whole number.'], ['Same operation to undo', 'Undo − with +.']])
    faq = [('What does CAPS Grade 5 say about calculation techniques?', 'Use estimation, building up and breaking down numbers, rounding off and compensating, doubling and halving, a number line, and addition, subtraction, multiplication and division as inverse operations.'), ('Why estimate?', 'To check that an answer is sensible.'), ('Which technique is fastest?', 'It depends on the numbers.'), ('Is mental maths daily?', 'CAPS asks for mental maths every day.')]
    make('calculation-techniques', 4, 'Numbers, Operations and Relationships', 'Grade 5: 1.1 Whole numbers',
         'Use a range of techniques to perform and check written and mental calculations of whole numbers, including estimation, building up and breaking down numbers, rounding off and compensating, doubling and halving, using a number line, and using addition and subtraction as well as multiplication and division as inverse operations.',
         'Calculation Techniques: Estimating, Compensating, Doubling and Halving and Inverse Operations', 'Calculation Techniques',
         'Free CAPS Grade 5 mental maths worksheets: rounding off and compensating, doubling and halving, estimating and inverse operations. 100 questions with memos.',
         'Round off, calculate, then compensate.', 'Estimate first; check with the inverse.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
