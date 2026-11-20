# -*- coding: utf-8 -*-
"""
South Africa Grade 7 Maths (CAPS): Whole Numbers: Place Value, Ordering, Rounding and Estimating (Grade 7: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g7_whole_numbers.py
Place value, multiplying and dividing by powers of 10, ordering, inequality signs and rounding and estimating (UK
Year 7 and Australia Year 7 makers) with South African number writing.
Wrong answers come from real mistakes: mixing up the value and the digit, comparing from the right, and rounding
the wrong digit.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y7_place_value_and_ordering as ukp
adopt(ukp)
if isinstance(getattr(ukp, 'R', None), random.Random): ukp.R = random.Random(807010)
import gen_uk_maths_y7_rounding_and_estimation as ukr
adopt(ukr)
if isinstance(getattr(ukr, 'R', None), random.Random): ukr.R = random.Random(807011)
import gen_au_maths_y7_rounding_and_estimation as aur
adopt(aur)
if isinstance(getattr(aur, 'R', None), random.Random): aur.R = random.Random(807012)
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
        ("Place value", [("collect", ukp.one_digit, 20)]),
        ("× and ÷ by 10, 100 and 1 000", [("collect", ukp.one_scale, 20)]),
        ("Order and compare", [("collect", ukp.one_order, 10), ("collect", ukp.one_order_list, 5), ("collect", ukp.one_ineq, 5)]),
        ("Round off", [("collect", ukr.one_sf, 10), ("collect", aur.one_ctx, 10)]),
        ("Estimate", [("collect", ukr.one_est, 10), ("collect", aur.one_est, 10)]),
    ], 80701)
    finish(sets, R)
    body = lesson('<ul><li>Each place is worth 10 times the place to its right.</li><li>× 10 moves every digit one place to the left; ÷ 10 moves every digit one place to the right.</li><li>To compare, count the digits, then compare from the left. Use &lt; and &gt;.</li><li>Round off to estimate: 4 872 × 31 is about 5 000 × 30 = 150 000.</li></ul>',
        [example("Round 6 482 517 to the nearest 100 000", ["ten thousands digit 8"], "6 500 000")],
        [['Value or digit?', 'The 4 in 6 482 517 is worth 400 000.'], ['Comparing from the right', 'Compare from the left.'], ['The wrong digit', 'Look one place to the right.']])
    faq = [('What does CAPS Grade 7 say about whole numbers?', 'Revise and use the properties of whole numbers, order and compare them, round off and estimate, and calculate with all four operations.'), ('What does &lt; mean?', 'Is less than.'), ('What is 340 ÷ 100?', '3,4.'), ('Why estimate?', 'To check that an answer is sensible.')]
    make('whole-numbers', 1, 'Numbers, Operations and Relationships', 'Grade 7: 1.1 Whole numbers',
         'Order, compare and represent whole numbers; recognise and use the place value of digits; round off and estimate; use the properties of whole numbers and calculation techniques including multiplying and dividing by powers of 10.',
         'Whole Numbers: Place Value, Ordering, Rounding and Estimating', 'Whole Numbers',
         'Free CAPS Grade 7 whole numbers worksheets: place value, multiplying and dividing by powers of 10, ordering, rounding and estimating. 100 questions with memos.',
         'Compare from the left; round to estimate.', '× 10: digits move left.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
