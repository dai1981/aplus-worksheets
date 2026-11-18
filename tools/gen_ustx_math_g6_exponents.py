# -*- coding: utf-8 -*-
"""
Texas Grade 6 Math: Exponents, Prime Factorization and Order of Operations (TEKS 6.7A)
  python3 tools/gen_ustx_math_g6_exponents.py
Reading and evaluating powers, prime factorization, order of operations with exponents, grouping symbols, and
word problems (the US Grade 6 makers with Texas names).
Wrong answers come from real mistakes: multiplying the base by the exponent, working strictly left to right, and
adding before multiplying.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g6_exponents as ex
import gen_us_math_g6_gcf_lcm as gl
adopt(ex)
adopt(gl)
tx_common.GRADE = "grade-6"



def build():
    sets, R = build_sets([
        ("Read and evaluate powers", [("run", ex.set_read, ("rnd", ex.People), 10), ("run", ex.set_powers, ("rnd", ex.People), 10)]),
        ("Prime factorization", [("run", gl.set_primes, (gl.People,), 20)]),
        ("Order of operations with exponents", [("run", ex.set_order, ("rnd", ex.People), 20)]),
        ("Grouping symbols, fractions and decimals", [("run", ex.set_harder, ("rnd", ex.People), 20)]),
        ("Exponent word problems", [("run", ex.set_story, ("rnd", ex.People), 20)]),
    ], 66013)
    finish(sets, R)
    body = lesson('<ul><li>An <b>exponent</b> tells how many times to use the base as a factor: 2<sup>5</sup> = 2 × 2 × 2 × 2 × 2 = 32.</li><li><b>Prime factorization</b> writes a number as a product of primes, often with exponents: 72 = 2<sup>3</sup> × 3<sup>2</sup>.</li><li>Order of operations: grouping symbols, exponents, multiply and divide (left to right), add and subtract (left to right).</li></ul>',
        [example("8 + 2³ × 5", ["2³ = 8", "8 × 5 = 40", "8 + 40"], "48"), example("Prime factorization of 36", ["36 = 4 × 9 = 2 × 2 × 3 × 3"], "2² × 3²")],
        [['Multiplying the base by the exponent: 2⁵ = 10', '2⁵ = 2 × 2 × 2 × 2 × 2 = 32.'], ['Working strictly left to right', 'Do exponents, then × and ÷, then + and −.'], ['Stopping at a composite factor', 'Keep splitting until every factor is prime.']])
    faq = [('What does TEKS 6.7A ask?', 'Generate equivalent numerical expressions using order of operations, including whole number exponents and prime factorization.'), ('What is 10⁰?', 'Any nonzero number to the power 0 is 1.'), ('Do I multiply before I divide?', 'No. Multiply and divide from left to right in the order they appear.'), ('How do I write a prime factorization?', 'Use a factor tree, then group equal primes with exponents.')]
    make('exponents-and-order-of-operations', 13, 'Expressions, Equations and Relationships', '6.7A',
         '6.7A generate equivalent numerical expressions using order of operations, including whole number exponents and prime factorization',
         'Exponents, Prime Factorization and Order of Operations', 'Exponents and Order of Operations',
         'Free Grade 6 worksheets for Texas TEKS 6.7A: exponents, prime factorization, order of operations with exponents and grouping symbols, and word problems. 100 questions with answers.',
         'Grouping, exponents, × and ÷, then + and −.', '8 + 2³ × 5 = 8 + 40 = 48. 72 = 2³ × 3².',
         body, faq, sets, seo_title='Grade 6 Exponents, Prime Factorization and Order of Operations Worksheets (TEKS 6.7A, STAAR)')


if __name__ == "__main__":
    build()
