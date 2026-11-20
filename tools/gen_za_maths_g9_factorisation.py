# -*- coding: utf-8 -*-
"""
South Africa Grade 9 Maths (CAPS): Factorisation: Common Factors, Difference of Two Squares and Trinomials (Grade 9: 2.3 Algebraic expressions)
  python3 tools/gen_za_maths_g9_factorisation.py
Taking out common factors, the difference of two squares, and factorising trinomials (Singapore Secondary 1 and
Secondary 2, UK Year 8 and Year 9 makers).
Wrong answers come from real mistakes: taking out only part of the common factor, writing a² − b² as (a − b)², and
getting the signs wrong in a trinomial.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_sg_maths_s1_simplifying_linear_expressions as sgl
adopt(sgl)
if isinstance(getattr(sgl, 'R', None), random.Random): sgl.R = random.Random(809080)
import gen_uk_maths_y8_expanding_and_factorising as uke
adopt(uke)
if isinstance(getattr(uke, 'R', None), random.Random): uke.R = random.Random(809081)
import gen_sg_maths_s2_expansion_and_factorisation as sge
adopt(sge)
if isinstance(getattr(sge, 'R', None), random.Random): sge.R = random.Random(809082)
import gen_uk_maths_y9_expanding_and_factorising_quadratics as ukq
adopt(ukq)
if isinstance(getattr(ukq, 'R', None), random.Random): ukq.R = random.Random(809083)
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
        ("Common factors", [("collect", sgl.one_factorise, 10), ("collect", uke.one_factor, 10)]),
        ("Trinomials with positive terms", [("collect", sge.one_fact_pos, 10), ("collect", ukq.one_fact_pos, 10)]),
        ("Trinomials with negative terms", [("collect", sge.one_fact_neg, 10), ("collect", ukq.one_fact_neg, 10)]),
        ("Factorisation practice", [("collect", ukq.one_fact_pos, 10), ("collect", sge.one_fact_neg, 10)]),
        ("Factorisation problems", [("run", sge.problems, (), 10, ok9), ("run", ukq.problems, (), 10, ok9)]),
    ], 80908)
    finish(sets, R)
    body = lesson('<ul><li>Always take out the highest common factor first: 6x² + 9x = 3x(2x + 3).</li><li>Difference of two squares: a² − b² = (a + b)(a − b).</li><li>Trinomial x² + bx + c: find two numbers that multiply to c and add to b.</li><li>Check by expanding.</li></ul>',
        [example("x² − x − 12", ["−4 × 3 = −12", "−4 + 3 = −1"], "(x − 4)(x + 3)")],
        [['Part of the factor', 'Take out the highest common factor.'], ['a² − b² = (a − b)²', 'It is (a + b)(a − b).'], ['Signs', 'Check by expanding.']])
    faq = [('What does CAPS Grade 9 say about factorisation?', 'Factorise algebraic expressions that involve common factors, the difference of two squares and trinomials of the form x² + bx + c and ax² + bx + c where a is a common factor.'), ('Is x² + 9 a difference of two squares?', 'No, it is a sum.'), ('How do I check?', 'Expand the brackets.'), ('What is 49 − y²?', '(7 + y)(7 − y).')]
    make('factorisation', 8, 'Patterns, Functions and Algebra', 'Grade 9: 2.3 Algebraic expressions',
         'Factorise algebraic expressions that involve: common factors, difference of two squares, trinomials of the form x² + bx + c and ax² + bx + c where a is a common factor.',
         'Factorisation: Common Factors, Difference of Two Squares and Trinomials', 'Factorisation',
         'Free CAPS Grade 9 factorisation worksheets: common factors, difference of two squares and factorising trinomials. 100 questions with memos.',
         'a² − b² = (a + b)(a − b).', 'Take out the HCF first.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
