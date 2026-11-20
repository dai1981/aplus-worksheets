# -*- coding: utf-8 -*-
"""
South Africa Grade 10 Maths (CAPS): Algebraic Fractions: Simplifying, Multiplying and Dividing (Grade 10: Algebraic expressions)
  python3 tools/gen_za_maths_g10_algebraic_fractions.py
Simplifying algebraic fractions, multiplying and dividing, adding and subtracting with numbers and linear
denominators (Singapore Secondary 2 makers) and fractional equations (Singapore Secondary 3 makers).
Wrong answers come from real mistakes: cancelling terms instead of factors, forgetting to flip the second fraction,
and adding the denominators.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_sg_maths_s2_algebraic_fractions as sgf
adopt(sgf)
if isinstance(getattr(sgf, 'R', None), random.Random): sgf.R = random.Random(810030)
import gen_sg_maths_s3_fractional_equations as sge
adopt(sge)
if isinstance(getattr(sge, 'R', None), random.Random): sge.R = random.Random(810031)
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
        ("Simplify", [("collect", sgf.one_simp, 20)]),
        ("Multiply and divide", [("collect", sgf.one_md, 20)]),
        ("Add and subtract", [("collect", sgf.one_num, 10), ("collect", sgf.one_lin, 10)]),
        ("Mixed practice", [("collect", sgf.one_mix, 20)]),
        ("Equations with fractions", [("collect", sge.one_simple, 10), ("collect", sge.one_excl, 10)]),
    ], 81003)
    finish(sets, R)
    body = lesson('<ul><li>Factorise first, then cancel common factors (not terms).</li><li>Multiply: multiply the tops and the bottoms. Divide: multiply by the reciprocal.</li><li>Add or subtract with a common denominator (the LCD).</li><li>State the values that make a denominator 0: they are excluded.</li></ul>',
        [example("(x² − 9)/(x + 3)", ["(x + 3)(x − 3)/(x + 3)"], "x − 3, x ≠ −3")],
        [['Cancelling terms', 'Only cancel factors.'], ['Not flipping', 'Divide: multiply by the reciprocal.'], ['Adding denominators', 'Use a common denominator.']])
    faq = [('What does CAPS Grade 10 say about algebraic fractions?', 'Simplify, add, subtract, multiply and divide algebraic fractions with numerators and denominators limited to the polynomials covered in factorisation.'), ('Why exclude values?', 'Division by 0 is undefined.'), ('Can I cancel x in (x + 2)/x?', 'No, x is not a factor of the whole top.'), ('What is the LCD?', 'The lowest common denominator.')]
    make('algebraic-fractions', 3, 'Algebra and Number Patterns', 'Grade 10: Algebraic expressions',
         'Simplification of algebraic fractions using factorisation with denominators of cubes (limited to sum and difference of cubes); adding, subtracting, multiplying and dividing algebraic fractions.',
         'Algebraic Fractions: Simplifying, Multiplying and Dividing', 'Algebraic Fractions',
         'Free CAPS Grade 10 algebraic fractions worksheets: simplifying, multiplying, dividing, adding and subtracting, and fractional equations. 100 questions with memos.',
         'Factorise first, then cancel factors.', 'State the excluded values.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
