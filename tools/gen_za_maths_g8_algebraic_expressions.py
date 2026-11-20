# -*- coding: utf-8 -*-
"""
South Africa Grade 8 Maths (CAPS): Algebraic Expressions: Simplifying, Expanding and Factorising (Grade 8: 2.3 Algebraic expressions)
  python3 tools/gen_za_maths_g8_algebraic_expressions.py
Like terms, multiplying and dividing monomials, expanding brackets, expanding two binomials and taking out a common
factor (UK Year 8 and Australia Year 8 makers).
Wrong answers come from real mistakes: adding unlike terms, multiplying only the first term in the bracket, and
getting the sign wrong with a negative outside the bracket.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y8_expanding_and_factorising as uke
adopt(uke)
if isinstance(getattr(uke, 'R', None), random.Random): uke.R = random.Random(808100)
import gen_au_maths_y8_expanding_and_factorising as aue
adopt(aue)
if isinstance(getattr(aue, 'R', None), random.Random): aue.R = random.Random(808101)
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
        ("Like terms", [("collect", aue.one_like2, 10), ("collect", uke.one_simplify, 10)]),
        ("Multiply and divide terms", [("collect", aue.one_muldiv, 20)]),
        ("Expand brackets", [("collect", uke.one_single, 10), ("collect", aue.one_expand, 10)]),
        ("Expand two binomials", [("collect", uke.one_double, 20)]),
        ("Common factors", [("collect", uke.one_factor, 10), ("collect", aue.one_factorise, 10)]),
    ], 80810)
    finish(sets, R)
    body = lesson('<ul><li>Only like terms can be added: 3x² + 5x − x² = 2x² + 5x.</li><li>Multiply terms: multiply the numbers and add the exponents. 3a² × 4a = 12a³.</li><li>Expand: multiply every term in the bracket. −2(x − 5) = −2x + 10.</li><li>Two binomials: (x + 3)(x + 4) = x² + 4x + 3x + 12 = x² + 7x + 12.</li></ul>',
        [example("(2x − 1)(x + 5)", ["2x² + 10x − x − 5"], "2x² + 9x − 5")],
        [['Unlike terms', 'x² and x are not like terms.'], ['The first term only', 'Multiply every term in the bracket.'], ['Signs', '−2 × −5 = +10.']])
    faq = [('What does CAPS Grade 8 say about expressions?', 'Add, subtract, multiply and divide algebraic terms, expand products of a monomial and a binomial and of two binomials, and simplify expressions.'), ('What is a binomial?', 'An expression with two terms, like x + 3.'), ('What is 6x²y ÷ 2x?', '3xy.'), ('What is factorising?', 'Writing an expression as a product, like 4x + 8 = 4(x + 2).')]
    make('algebraic-expressions', 10, 'Patterns, Functions and Algebra', 'Grade 8: 2.3 Algebraic expressions',
         'Recognise and differentiate between monomials, binomials and trinomials; add and subtract like terms in algebraic expressions; multiply integers and monomials by monomials, binomials and trinomials; divide monomials, binomials and trinomials by integers or monomials; determine the product of two binomials; determine the squares, cubes, square roots and cube roots of single algebraic terms.',
         'Algebraic Expressions: Simplifying, Expanding and Factorising', 'Algebraic Expressions',
         'Free CAPS Grade 8 algebraic expressions worksheets: like terms, multiplying and dividing terms, expanding brackets, binomials and common factors. 100 questions with memos.',
         'Multiply every term in the bracket.', 'Add only like terms.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
