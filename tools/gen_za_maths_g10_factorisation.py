# -*- coding: utf-8 -*-
"""
South Africa Grade 10 Maths (CAPS): Products and Factorisation (Grade 10: Algebraic expressions)
  python3 tools/gen_za_maths_g10_factorisation.py
Multiplying polynomials, special products, common factors, trinomials, the difference of two squares, the sum and
difference of cubes, and grouping (US Algebra 1 and Algebra 2 makers with South African terms).
Wrong answers come from real mistakes: forgetting the middle term, getting the signs wrong in a trinomial, and using
the wrong signs in the sum or difference of cubes.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_us_math_a1_polynomial_operations as usp
adopt(usp)
if isinstance(getattr(usp, 'R', None), random.Random): usp.R = random.Random(810020)
import gen_us_math_a1_factoring_polynomials as usf
adopt(usf)
if isinstance(getattr(usf, 'R', None), random.Random): usf.R = random.Random(810021)
import gen_us_math_a2_polynomial_identities_and_factoring as usi
adopt(usi)
if isinstance(getattr(usi, 'R', None), random.Random): usi.R = random.Random(810022)
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
        ("Products", [("collect", usp.one_mul, 10), ("collect", usp.one_special, 10)]),
        ("Common factors and grouping", [("collect", usf.one_gcf, 10), ("collect", usi.one_group, 10)]),
        ("Trinomials", [("collect", usf.one_simple, 10), ("collect", usf.one_ac, 10)]),
        ("Difference of two squares", [("collect", usf.one_special, 10), ("collect", usf.one_complete, 10)]),
        ("Sum and difference of cubes", [("collect", usi.one_cubes, 20)]),
    ], 81002)
    finish(sets, R)
    body = lesson('<ul><li>Take out the highest common factor first.</li><li>Trinomial ax² + bx + c: find factors of ac that add up to b.</li><li>Difference of two squares: a² − b² = (a + b)(a − b).</li><li>Cubes: a³ + b³ = (a + b)(a² − ab + b²) and a³ − b³ = (a − b)(a² + ab + b²).</li></ul>',
        [example("8x³ − 27", ["(2x)³ − 3³"], "(2x − 3)(4x² + 6x + 9)")],
        [['The middle term', '(a + b)² = a² + 2ab + b².'], ['Signs', 'Check by expanding.'], ['Cube signs', 'The middle sign in the trinomial is the opposite.']])
    faq = [('What does CAPS Grade 10 say about factorisation?', 'Multiply a binomial by a trinomial, and factorise trinomials, by grouping in pairs, and the sum and difference of two cubes.'), ('Can x² + 4 be factorised?', 'Not over the real numbers.'), ('How do I check?', 'Expand the factors.'), ('What is grouping?', 'Pairing terms that share a factor.')]
    make('products-and-factorisation', 2, 'Algebra and Number Patterns', 'Grade 10: Algebraic expressions',
         'Products: multiplication of a binomial by a trinomial; factorisation: revise common factors (Grade 9), factorisation of trinomials, factorisation by grouping in pairs, sums and differences of two cubes.',
         'Products and Factorisation', 'Products and Factorisation',
         'Free CAPS Grade 10 worksheets: products of polynomials, common factors, trinomials, difference of two squares, sum and difference of cubes and grouping. 100 questions with memos.',
         'a³ − b³ = (a − b)(a² + ab + b²).', 'Take out the HCF first.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
