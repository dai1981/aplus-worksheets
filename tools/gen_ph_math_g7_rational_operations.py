# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Operations on Rational Numbers (Grade 7: Number and Algebra)
  python3 tools/gen_ph_math_g7_rational_operations.py
Adding, subtracting, multiplying and dividing positive and negative fractions and decimals (Texas Grade 7 makers),
and mixed operations (Australia Year 8 makers).
Wrong answers come from real mistakes: adding the denominators, getting the sign wrong, and dividing without using
the reciprocal.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_ustx_math_g7_add_subtract_rational as txa
adopt(txa)
if hasattr(txa, 'R'): txa.R = random.Random(707100)
import gen_ustx_math_g7_multiply_divide_rational as txm
adopt(txm)
if hasattr(txm, 'R'): txm.R = random.Random(707101)
import gen_au_maths_y8_integers_and_rational_numbers as aui
adopt(aui)
if hasattr(aui, 'R'): aui.R = random.Random(707102)
ph_common.GRADE = "grade-7"



def build():
    sets, R = build_sets([
        ("Add and subtract fractions", [("collect", txa.one_frac, 20)]),
        ("Add and subtract decimals", [("collect", txa.one_dec, 20)]),
        ("Multiply and divide fractions", [("collect", txm.one_frac, 20)]),
        ("Multiply and divide decimals", [("collect", txm.one_dec, 20)]),
        ("Mixed operations", [("collect", aui.one_rat, 10), ("collect", aui.one_mixed, 10)]),
    ], 70710)
    finish(sets, R)
    body = lesson('<ul><li>Fractions: add or subtract with a common denominator; multiply numerators and denominators; to divide, multiply by the reciprocal.</li><li>Decimals: line up the decimal points to add or subtract; count decimal places to multiply.</li><li>Signs: same signs multiply or divide to a positive answer; different signs give a negative answer.</li><li>To add numbers with different signs, subtract their absolute values and keep the sign of the larger one.</li></ul>',
        [example("−<span class='fr'><span class='fn'>2</span><span class='fd'>3</span></span> + <span class='fr'><span class='fn'>1</span><span class='fd'>4</span></span>", ["−<span class='fr'><span class='fn'>8</span><span class='fd'>12</span></span> + <span class='fr'><span class='fn'>3</span><span class='fd'>12</span></span>"], "−<span class='fr'><span class='fn'>5</span><span class='fd'>12</span></span>"), example("−1.5 × (−0.4)", ["same signs: positive"], "0.6")],
        [['Adding denominators', 'Use a common denominator.'], ['Wrong sign', 'Different signs give a negative product.'], ['Dividing directly', 'Multiply by the reciprocal.']])
    faq = [('What does MATATAG Math 7 ask about rational numbers?', 'Perform operations on rational numbers.'), ('What is the reciprocal of −2/5?', '−5/2.'), ('Is the product of two negative numbers negative?', 'No, it is positive.'), ('How do I check a division?', 'Multiply the answer by the divisor.')]
    make('operations-on-rational-numbers', 10, 'Number and Algebra', 'Grade 7: Number and Algebra',
         'Perform operations on rational numbers.',
         'Operations on Rational Numbers', 'Operations on Rational Numbers',
         'Free Grade 7 worksheets on operations with rational numbers for the DepEd MATATAG curriculum: positive and negative fractions and decimals and multi-step problems. 100 questions with answers.',
         'Same signs: positive. Different signs: negative.', 'To divide by a fraction, multiply by its reciprocal.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
