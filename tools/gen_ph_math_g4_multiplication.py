# -*- coding: utf-8 -*-
"""
Philippines Grade 4 Math (MATATAG): Multiplying 3- to 4-Digit by 1-Digit and 2- to 3-Digit by 2-Digit Numbers (Grade 4: Number and Algebra)
  python3 tools/gen_ph_math_g4_multiplication.py
Multiplying by a 1-digit number, area models, 2-digit by 2-digit and 3-digit by 2-digit numbers (US Grade 4 and
Singapore Primary 4 makers), and estimating products.
Wrong answers come from real mistakes: forgetting to add the regrouped digit, leaving out the zero in the second
partial product, and adding the partial products wrong.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g4_multiplication as usm
adopt(usm)
if hasattr(usm, 'R'): usm.R = random.Random(704070)
import gen_sg_maths_p4_multiplication as sgm
adopt(sgm)
if hasattr(sgm, 'R'): sgm.R = random.Random(704071)
ph_common.GRADE = "grade-4"



def build():
    sets, R = build_sets([
        ("Multiply by a 1-digit number", [("run", usm.set_std1, ("rnd", "seen"), 20)]),
        ("Area models", [("run", usm.set_area2, ("rnd", "seen"), 20)]),
        ("Multiply 2-digit by 2-digit numbers", [("run", usm.set_std2, ("rnd", "seen"), 20)]),
        ("Multiply 3-digit by 2-digit numbers", [("run", sgm.set_3x2, ("rnd", "seen", sgm.People), 20)]),
        ("Estimate products", [("run", sgm.set_estimate, ("rnd", sgm.People), 20)]),
    ], 70407)
    finish(sets, R)
    body = lesson('<ul><li>Multiply the ones first, then the tens, hundreds and so on. Add any regrouped digit.</li><li>For a 2-digit multiplier, find two partial products: one for the ones digit and one for the tens digit (start that row with a 0).</li><li>Add the partial products.</li><li>Estimate by rounding each factor: 387 × 42 is about 400 × 40 = 16,000.</li></ul>',
        [example("236 × 47", ["236 × 7 = 1,652", "236 × 40 = 9,440", "1,652 + 9,440"], "11,092")],
        [['Forgetting the regrouped digit', 'Add it after you multiply the next place.'], ['No zero in the second row', 'The tens digit makes tens: start with 0.'], ['Adding partial products wrong', 'Line up the places.']])
    faq = [('What does MATATAG Math 4 ask about multiplication?', 'Multiply 3- to 4-digit numbers by a 1-digit number and 2- to 3-digit numbers by 2-digit numbers, with and without regrouping, with products up to 1 000 000, and estimate the result of multiplying two numbers.'), ('What is a partial product?', 'The product of one factor and one place of the other factor.'), ('How do I estimate a product?', 'Round each factor, then multiply.'), ('Does the order of factors matter?', 'No. 47 × 236 = 236 × 47.')]
    make('multiplying-whole-numbers', 7, 'Number and Algebra', 'Grade 4: Number and Algebra',
         'Multiply two numbers with and without regrouping: 3- to 4-digit numbers by a 1-digit number, and 2- to 3-digit numbers by 2-digit numbers, with products up to 1 000 000; estimate the result of multiplying two numbers where the product is less than 1 000 000.',
         'Multiplying 3- to 4-Digit by 1-Digit and 2- to 3-Digit by 2-Digit Numbers', 'Multiplication',
         'Free Grade 4 multiplication worksheets for the DepEd MATATAG curriculum: multiply by 1-digit and 2-digit numbers, area models and estimating products. 100 questions with answers.',
         'Find partial products, then add them.', 'Estimate by rounding each factor.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
