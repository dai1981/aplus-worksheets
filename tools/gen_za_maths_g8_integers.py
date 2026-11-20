# -*- coding: utf-8 -*-
"""
South Africa Grade 8 Maths (CAPS): Integers: Adding, Subtracting, Multiplying and Dividing (Grade 8: 1.2 Integers)
  python3 tools/gen_za_maths_g8_integers.py
Adding and subtracting integers, multiplying and dividing integers, squares, cubes and roots of integers, and mixed
calculations (UK Year 7 and Australia Year 7 and Year 8 makers).
Wrong answers come from real mistakes: getting the sign wrong when multiplying two negatives, thinking (−3)² is −9,
and subtracting a negative as if it were positive.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y7_negative_numbers as ukn
adopt(ukn)
if isinstance(getattr(ukn, 'R', None), random.Random): ukn.R = random.Random(808030)
import gen_au_maths_y8_integers_and_rational_numbers as aui
adopt(aui)
if isinstance(getattr(aui, 'R', None), random.Random): aui.R = random.Random(808031)
import gen_au_maths_y7_adding_and_subtracting_integers as aua
adopt(aua)
if isinstance(getattr(aua, 'R', None), random.Random): aua.R = random.Random(808032)
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
        ("Add and subtract integers", [("collect", ukn.one_add, 7), ("collect", ukn.one_sub_neg, 7), ("collect", aua.one_mix, 6)]),
        ("Multiply integers", [("collect", ukn.one_mul, 10), ("collect", aui.one_mul, 10)]),
        ("Divide integers", [("collect", ukn.one_div, 10), ("collect", aui.one_div, 10)]),
        ("Squares, cubes and roots", [("collect", ukn.one_sq, 10), ("collect", aui.one_sq, 10)]),
        ("Mixed calculations", [("collect", ukn.one_mixed, 10), ("collect", aui.one_mixed, 10)]),
    ], 80803)
    finish(sets, R)
    body = lesson('<ul><li>Same signs give a positive answer: (−4) × (−5) = 20.</li><li>Different signs give a negative answer: (−24) ÷ 6 = −4.</li><li>(−3)² = 9, but (−2)³ = −8.</li><li>Subtracting a negative is the same as adding: 5 − (−3) = 8.</li></ul>',
        [example("(−6) × 4 − (−18) ÷ 3", ["−24 − (−6)", "−24 + 6"], "−18")],
        [['Two negatives', '(−) × (−) = +.'], ['(−3)² = −9', '(−3) × (−3) = 9.'], ['− (−)', 'Subtracting a negative means add.']])
    faq = [('What does CAPS Grade 8 say about integers?', 'Add, subtract, multiply and divide integers, and calculate squares, cubes, square roots and cube roots of integers.'), ('What is ∛(−27)?', '−3.'), ('Is −5 × 0 negative?', 'No, it is 0.'), ('What is −2²?', '−4, because only 2 is squared.')]
    make('integers', 3, 'Numbers, Operations and Relationships', 'Grade 8: 1.2 Integers',
         'Perform calculations involving all four operations with integers; perform calculations involving all four operations with numbers that involve the squares, cubes, square roots and cube roots of integers; recognise and use commutative, associative and distributive properties, and additive and multiplicative inverses for integers.',
         'Integers: Adding, Subtracting, Multiplying and Dividing', 'Integers',
         'Free CAPS Grade 8 integers worksheets: adding, subtracting, multiplying and dividing integers, squares, cubes and roots. 100 questions with memos.',
         'Same signs: positive. Different signs: negative.', '(−3)² = 9.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
