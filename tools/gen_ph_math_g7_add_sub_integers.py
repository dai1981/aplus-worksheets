# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Adding and Subtracting Integers (Grade 7: Number and Algebra)
  python3 tools/gen_ph_math_g7_add_sub_integers.py
Adding and subtracting integers with integer chips (tiles), number lines and numerals, and word problems (Ontario
Grade 7 makers with Filipino names).
Wrong answers come from real mistakes: adding the absolute values when the signs differ, subtracting a negative as
a negative, and keeping the wrong sign.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_caon_math_g7_integers as cai
adopt(cai)
if hasattr(cai, 'R'): cai.R = random.Random(707220)
ph_common.GRADE = "grade-7"



def build():
    sets, R = build_sets([
        ("Integer chips", [("run", cai.set_tiles, ("rnd", cai.People), 20)]),
        ("Number lines", [("run", cai.set_lines, ("rnd", cai.People), 20)]),
        ("Add integers", [("run", cai.set_adding, ("rnd", cai.People), 20)]),
        ("Subtract integers", [("run", cai.set_subtracting, ("rnd", cai.People), 20)]),
        ("Integer word problems", [("run", cai.set_words, ("rnd", cai.People), 20)]),
    ], 70722)
    finish(sets, R)
    body = lesson('<ul><li>With integer chips, a positive and a negative chip make a <b>zero pair</b>.</li><li>Same signs: add the absolute values and keep the sign. −4 + (−6) = −10.</li><li>Different signs: subtract the absolute values and keep the sign of the one farther from 0. −9 + 5 = −4.</li><li>To subtract, add the opposite: 3 − (−5) = 3 + 5 = 8.</li></ul>',
        [example("−7 − (−10)", ["−7 + 10"], "3")],
        [['Adding when signs differ', '−9 + 5 is −4, not −14.'], ['− (−) as negative', 'Subtracting −5 is adding 5.'], ['Wrong sign', 'Keep the sign of the number farther from 0.']])
    faq = [('What does MATATAG Math 7 ask about adding integers?', 'Add and subtract integers using concrete models (integer chips), pictorial models (bar models, number lines), and with integers written as numerals.'), ('What is a zero pair?', 'One positive and one negative chip, which add to 0.'), ('Is subtraction of integers commutative?', 'No: 3 − 5 ≠ 5 − 3.'), ('How do I check an answer?', 'Add the answer to the number you subtracted.')]
    make('adding-and-subtracting-integers', 22, 'Number and Algebra', 'Grade 7: Number and Algebra',
         'Add and subtract integers; using concrete models (e.g., counters, integer chips), pictorial models (e.g., bar models, number lines), and with integers written as numerals.',
         'Adding and Subtracting Integers', 'Adding and Subtracting Integers',
         'Free Grade 7 adding and subtracting integers worksheets for the DepEd MATATAG curriculum: integer chips, number lines, rules for signs and word problems. 100 questions with answers.',
         'To subtract, add the opposite.', 'Different signs: subtract and keep the sign of the larger absolute value.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
