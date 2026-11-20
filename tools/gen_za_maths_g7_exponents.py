# -*- coding: utf-8 -*-
"""
South Africa Grade 7 Maths (CAPS): Exponents: Squares, Cubes, Square Roots and Cube Roots (Grade 7: 1.2 Exponents)
  python3 tools/gen_za_maths_g7_exponents.py
Squares and cubes, square roots and cube roots, index notation, estimating roots and calculations with exponents (UK
Year 7 and Australia Year 7 makers).
Wrong answers come from real mistakes: multiplying the base by the exponent, halving instead of finding a square root,
and forgetting the order of operations with powers.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y7_powers_and_roots as ukp
adopt(ukp)
if isinstance(getattr(ukp, 'R', None), random.Random): ukp.R = random.Random(807060)
import gen_au_maths_y7_square_numbers_and_square_roots as aus
adopt(aus)
if isinstance(getattr(aus, 'R', None), random.Random): aus.R = random.Random(807061)
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
        ("Squares and cubes", [("collect", ukp.one_sqcube, 10), ("collect", aus.one_square, 10)]),
        ("Square roots and cube roots", [("collect", ukp.one_root, 10), ("collect", aus.one_root, 10)]),
        ("Index notation", [("collect", ukp.one_index, 20)]),
        ("Estimate roots", [("collect", aus.one_est, 20)]),
        ("Calculate with exponents", [("collect", ukp.one_mix, 10), ("collect", aus.one_calc, 10)]),
    ], 80706)
    finish(sets, R)
    body = lesson('<ul><li>5² = 5 × 5 = 25 (5 squared). 4³ = 4 × 4 × 4 = 64 (4 cubed).</li><li>√49 = 7 because 7² = 49. ∛27 = 3 because 3³ = 27.</li><li>In 2⁵, 2 is the base and 5 is the exponent.</li><li>Powers come before × and ÷ in the order of operations.</li></ul>',
        [example("3² + 2³", ["9 + 8"], "17")],
        [['Base × exponent', '5² = 25, not 10.'], ['Halving', '√64 = 8, not 32.'], ['Order of operations', 'Work out the powers first.']])
    faq = [('What does CAPS Grade 7 say about exponents?', 'Represent and compare whole numbers in exponential form, calculate squares, cubes, square roots and cube roots, and use them in calculations.'), ('What is 10³?', '1 000.'), ('Is √50 a whole number?', 'No, it is between 7 and 8.'), ('What is a perfect square?', 'A number like 36 that is a whole number squared.')]
    make('exponents', 6, 'Numbers, Operations and Relationships', 'Grade 7: 1.2 Exponents',
         'Compare and represent whole numbers in exponential form: a^b; recognise and use the appropriate laws of operations with numbers involving exponents and square and cube roots; calculate squares, cubes, square roots and cube roots.',
         'Exponents: Squares, Cubes, Square Roots and Cube Roots', 'Exponents',
         'Free CAPS Grade 7 exponents worksheets: squares, cubes, square roots, cube roots, index notation and estimating roots. 100 questions with memos.',
         '5² = 5 × 5, not 5 × 2.', '√49 = 7 because 7² = 49.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
