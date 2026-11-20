# -*- coding: utf-8 -*-
"""
South Africa Grade 9 Maths (CAPS): Algebraic Expressions: Products of Binomials and Squares (Grade 9: 2.3 Algebraic expressions)
  python3 tools/gen_za_maths_g9_algebraic_expressions.py
Simplifying, expanding brackets, products of two binomials, squares of binomials and algebraic fractions (Singapore
Secondary 1 and Secondary 2 and UK Year 9 makers).
Wrong answers come from real mistakes: forgetting the middle term in (a + b)², multiplying only some terms, and
getting the signs wrong.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_sg_maths_s1_simplifying_linear_expressions as sgl
adopt(sgl)
if isinstance(getattr(sgl, 'R', None), random.Random): sgl.R = random.Random(809070)
import gen_sg_maths_s2_expansion_and_factorisation as sge
adopt(sge)
if isinstance(getattr(sge, 'R', None), random.Random): sge.R = random.Random(809071)
import gen_uk_maths_y9_expanding_and_factorising_quadratics as ukq
adopt(ukq)
if isinstance(getattr(ukq, 'R', None), random.Random): ukq.R = random.Random(809072)
import gen_sg_maths_s2_algebraic_fractions as sgf
adopt(sgf)
if isinstance(getattr(sgf, 'R', None), random.Random): sgf.R = random.Random(809073)
za_common.GRADE = "grade-9"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok9(it):
    """Grade 9: no trigonometry, quadratic formula, simultaneous equations or cones and spheres (Grade 10+)"""
    return not _re.search(r"\b(sin|cos|tan)\b|quadratic formula|discriminant|simultaneous|\bcone|\bsphere|imperial|\bmiles?\b", _txt(it))



def build():
    sets, R = build_sets([
        ("Simplify", [("collect", sgl.one_like2, 10), ("collect", sgl.one_muldiv, 10)]),
        ("Expand brackets", [("collect", sgl.one_expand, 10), ("collect", sgl.one_expand2, 10)]),
        ("Products of binomials", [("collect", sge.one_expand, 10), ("collect", ukq.one_expand, 10)]),
        ("Squares of binomials", [("collect", sge.one_square, 10), ("collect", ukq.one_square, 10)]),
        ("Algebraic fractions", [("collect", sgf.one_simp, 10), ("collect", sgf.one_md, 10)]),
    ], 80907)
    finish(sets, R)
    body = lesson('<ul><li>Expand: multiply every term in one bracket by every term in the other.</li><li>(x + 3)(x − 5) = x² − 5x + 3x − 15 = x² − 2x − 15.</li><li>(a + b)² = a² + 2ab + b². Do not forget the middle term.</li><li>Simplify algebraic fractions by cancelling common factors.</li></ul>',
        [example("(2x − 3)²", ["(2x)² − 2 × 2x × 3 + 3²"], "4x² − 12x + 9")],
        [['(a + b)² = a² + b²', 'Add the middle term 2ab.'], ['Some terms only', 'Multiply every term.'], ['Signs', '(−3) × (−5) = +15.']])
    faq = [('What does CAPS Grade 9 say about expressions?', 'Simplify expressions, multiply binomials by binomials and trinomials, determine squares of binomials, and simplify algebraic fractions.'), ('What is (x − 4)²?', 'x² − 8x + 16.'), ('What is a trinomial?', 'An expression with three terms.'), ('Can I cancel terms in a fraction?', 'Only common factors, not terms.')]
    make('algebraic-expressions', 7, 'Patterns, Functions and Algebra', 'Grade 9: 2.3 Algebraic expressions',
         'Use commutative, associative and distributive laws for rational numbers and laws of exponents to multiply integers, monomials and binomials by polynomials, divide polynomials by integers or monomials, determine the product of two binomials, and determine the square of a binomial; simplify algebraic expressions involving the above operations.',
         'Algebraic Expressions: Products of Binomials and Squares', 'Algebraic Expressions',
         'Free CAPS Grade 9 algebraic expressions worksheets: simplifying, expanding, products of binomials, squares of binomials and algebraic fractions. 100 questions with memos.',
         '(a + b)² = a² + 2ab + b².', 'Multiply every term by every term.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
