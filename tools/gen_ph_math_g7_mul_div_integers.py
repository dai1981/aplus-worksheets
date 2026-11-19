# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Multiplying and Dividing Integers (Grade 7: Number and Algebra)
  python3 tools/gen_ph_math_g7_mul_div_integers.py
Multiplication as repeated addition, the sign rules, division as the inverse of multiplication, mixed problems and
word problems (BC Grade 7 makers with Filipino names).
Wrong answers come from real mistakes: thinking two negatives make a negative, getting the sign of a quotient wrong,
and counting negative signs incorrectly.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_cabc_math_g7_mult_div_integers as cbm
adopt(cbm)
if hasattr(cbm, 'R'): cbm.R = random.Random(707230)
ph_common.GRADE = "grade-7"



def build():
    sets, R = build_sets([
        ("Repeated addition", [("run", cbm.set_repeated, ("rnd", cbm.People), 20)]),
        ("Sign rules", [("run", cbm.set_signs, ("rnd", cbm.People), 20)]),
        ("Division as the inverse", [("run", cbm.set_inverse, ("rnd", cbm.People), 20)]),
        ("Mixed problems", [("run", cbm.set_mixed, ("rnd", cbm.People), 20)]),
        ("Word problems", [("run", cbm.set_words, ("rnd", cbm.People), 20)]),
    ], 70723)
    finish(sets, R)
    body = lesson('<ul><li>Same signs: the product or quotient is <b>positive</b>. (−6) × (−4) = 24.</li><li>Different signs: the product or quotient is <b>negative</b>. 18 ÷ (−3) = −6.</li><li>With many factors, count the negative signs: an even number gives a positive answer, an odd number a negative answer.</li><li>Check a division with multiplication: (−6) × (−3) = 18.</li></ul>',
        [example("(−2) × 3 × (−5)", ["two negatives: positive"], "30")],
        [['Two negatives make a negative', '(−3) × (−4) = 12.'], ['Sign of a quotient', '−20 ÷ 4 = −5.'], ['Counting signs', 'Three negative factors give a negative product.']])
    faq = [('What does MATATAG Math 7 ask about multiplying integers?', 'Multiply and divide integers.'), ('Why is a negative times a negative positive?', 'Taking away negative groups is like adding positive ones.'), ('What is −24 ÷ (−6)?', '4.'), ('Can I divide by 0?', 'No. Division by 0 is undefined.')]
    make('multiplying-and-dividing-integers', 23, 'Number and Algebra', 'Grade 7: Number and Algebra',
         'Multiply and divide integers.',
         'Multiplying and Dividing Integers', 'Multiplying and Dividing Integers',
         'Free Grade 7 multiplying and dividing integers worksheets for the DepEd MATATAG curriculum: sign rules, repeated addition, inverse operations and word problems. 100 questions with answers.',
         'Same signs: positive. Different signs: negative.', 'Count the negative signs: even is positive, odd is negative.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
