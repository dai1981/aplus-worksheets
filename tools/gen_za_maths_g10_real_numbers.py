# -*- coding: utf-8 -*-
"""
South Africa Grade 10 Maths (CAPS): The Number System, Surds and Rounding (Grade 10: Algebraic expressions)
  python3 tools/gen_za_maths_g10_real_numbers.py
Rational and irrational numbers, simplifying, adding and multiplying surds, and estimating and rounding (Australia
Year 8, US Algebra 1 and UK Year 9 makers with South African terms).
Wrong answers come from real mistakes: adding the numbers under the root, simplifying √12 as 2√6, and calling a
recurring decimal irrational.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y8_irrational_numbers_and_recurring_decimals as aui
adopt(aui)
if isinstance(getattr(aui, 'R', None), random.Random): aui.R = random.Random(810010)
import gen_us_math_a1_simplifying_radicals as usr
adopt(usr)
if isinstance(getattr(usr, 'R', None), random.Random): usr.R = random.Random(810011)
import gen_uk_maths_y9_rounding_and_error_intervals as ukr
adopt(ukr)
if isinstance(getattr(ukr, 'R', None), random.Random): ukr.R = random.Random(810012)
import gen_au_maths_y7_square_numbers_and_square_roots as aus
adopt(aus)
if isinstance(getattr(aus, 'R', None), random.Random): aus.R = random.Random(810013)
za_common.GRADE = "grade-10"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok10(it):
    """Grade 10: no complex numbers, logarithms, radians, sine or cosine rules, or calculus"""
    return not _re.search(r"imaginary|complex|\blog|radian|\bπ/|sine rule|cosine rule|law of (sines|cosines)|derivative|imperial|\bmiles?\b|\bfeet\b|\binch", _txt(it))



def build():
    sets, R = build_sets([
        ("Rational or irrational?", [("collect", aui.one_ri, 10), ("collect", aui.one_tr, 10)]),
        ("Simplify surds", [("collect", usr.one_simp, 20)]),
        ("Add and subtract surds", [("collect", usr.one_add, 20)]),
        ("Multiply surds", [("collect", usr.one_mul, 20)]),
        ("Estimate and round", [("collect", aus.one_est, 10), ("collect", ukr.one_sf_big, 10)]),
    ], 81001)
    finish(sets, R)
    body = lesson('<ul><li>Real numbers are rational (can be written as a fraction) or irrational (like √2 and π).</li><li>Simplify a surd by taking out a square factor: √50 = √(25 × 2) = 5√2.</li><li>Add only like surds: 3√2 + 5√2 = 8√2, but √2 + √3 cannot be simplified.</li><li>√a × √b = √(ab).</li></ul>',
        [example("√18 + √8", ["3√2 + 2√2"], "5√2")],
        [['Adding under the root', '√2 + √3 ≠ √5.'], ['Not the biggest square', '√12 = 2√3.'], ['Recurring is irrational', '0,333… = ⅓ is rational.']])
    faq = [('What does CAPS Grade 10 say about the number system?', 'Understand that real numbers can be rational or irrational, establish between which two integers a surd lies, and round real numbers to an appropriate degree of accuracy.'), ('Between which integers is √40?', '6 and 7.'), ('What is a surd?', 'A root that cannot be simplified to a rational number.'), ('Is √49 a surd?', 'No, it equals 7.')]
    make('number-system-and-surds', 1, 'Algebra and Number Patterns', 'Grade 10: Algebraic expressions',
         'Understand that real numbers can be irrational or rational; establish between which two integers a given simple surd lies; round real numbers to an appropriate degree of accuracy (to a given number of decimal digits); simplify, add, subtract and multiply surds.',
         'The Number System, Surds and Rounding', 'Number System and Surds',
         'Free CAPS Grade 10 worksheets: rational and irrational numbers, simplifying, adding and multiplying surds and rounding. 100 questions with memos.',
         '√50 = 5√2.', 'Add only like surds.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
