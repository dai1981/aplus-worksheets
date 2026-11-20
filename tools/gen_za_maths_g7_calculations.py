# -*- coding: utf-8 -*-
"""
South Africa Grade 7 Maths (CAPS): Calculating with Whole Numbers: Order of Operations, Long Multiplication and Long Division (Grade 7: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g7_calculations.py
The order of operations with brackets and powers (UK Year 7 makers), long multiplication and long division (UK Year 6
makers), and multi-step problems.
Wrong answers come from real mistakes: working from left to right only, ignoring brackets, and leaving out a 0 in
long division.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y7_order_of_operations as uko
adopt(uko)
if isinstance(getattr(uko, 'R', None), random.Random): uko.R = random.Random(807030)
import gen_uk_maths_y6_long_multiplication as ukm
adopt(ukm)
if isinstance(getattr(ukm, 'R', None), random.Random): ukm.R = random.Random(807031)
import gen_uk_maths_y6_long_division as ukd
adopt(ukd)
if isinstance(getattr(ukd, 'R', None), random.Random): ukd.R = random.Random(807032)
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
        ("× and ÷ before + and −", [("collect", uko.one_md, 20)]),
        ("Brackets and powers", [("collect", uko.one_br, 10), ("collect", uko.one_pow, 10)]),
        ("Long multiplication", [("run", ukm.set_4x2, ("rnd", "seen"), 10, noneg), ("run", ukm.set_3x2, ("rnd", "seen"), 10, noneg)]),
        ("Long division", [("run", ukd.set_long4, ("rnd", "seen", ukd.People), 10, noneg), ("run", ukd.set_long3, ("rnd", "seen", ukd.People), 10, noneg)]),
        ("Multi-step problems", [("run", ukm.set_story, ("rnd", ukm.People), 10, noneg), ("run", ukd.set_story, ("rnd", ukd.People, "seen"), 10, noneg)]),
    ], 80703)
    finish(sets, R)
    body = lesson('<ul><li>Order of operations: brackets, then powers and roots, then × and ÷ from left to right, then + and − from left to right.</li><li>Long multiplication: multiply by each digit, write the zeros, then add.</li><li>Long division: divide, multiply, subtract, bring down.</li><li>Estimate first to check the size of the answer.</li></ul>',
        [example("48 − 3 × (2 + 4)²", ["brackets: 6", "power: 36", "3 × 36 = 108"], "48 − 108 = −60")],
        [['Left to right only', '× and ÷ come first.'], ['Ignoring brackets', 'Work out brackets first.'], ['A missing 0', 'Write 0 when the divisor does not fit.']])
    faq = [('What does CAPS Grade 7 say about calculations?', 'Add, subtract, multiply and divide whole numbers, including long multiplication and long division, and use the order of operations.'), ('What comes first: powers or ×?', 'Powers.'), ('What is 2 + 3²?', '11.'), ('How do I check a long division?', 'Multiply the answer by the divisor.')]
    make('calculating-with-whole-numbers', 3, 'Numbers, Operations and Relationships', 'Grade 7: 1.1 Whole numbers',
         'Perform calculations using all four operations on whole numbers, estimating and using calculators where appropriate; use the order of operations including brackets, squares and cubes; multiply whole numbers by at least 2-digit numbers and divide by at least 2-digit numbers.',
         'Calculating with Whole Numbers: Order of Operations, Long Multiplication and Long Division', 'Calculating with Whole Numbers',
         'Free CAPS Grade 7 worksheets: order of operations with brackets and powers, long multiplication, long division and multi-step problems. 100 questions with memos.',
         'Brackets, powers, × and ÷, + and −.', 'Estimate to check the size of the answer.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
