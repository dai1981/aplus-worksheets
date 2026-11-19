# -*- coding: utf-8 -*-
"""
Philippines Grade 4 Math (MATATAG): Adding and Subtracting Numbers up to 1,000,000 (Grade 4: Number and Algebra)
  python3 tools/gen_ph_math_g4_add_subtract.py
Adding and subtracting 4- to 6-digit numbers with and without regrouping, subtracting across zeros, and word problems
(US Grade 4 makers with Filipino names; items with dollars are skipped).
Wrong answers come from real mistakes: forgetting to regroup, subtracting the smaller digit from the bigger one, and
lining up digits from the left.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g4_add_sub as usa
adopt(usa)
if hasattr(usa, 'R'): usa.R = random.Random(704060)
import gen_uk_maths_y4_column_add_sub as uka
adopt(uka)
if hasattr(uka, 'R'): uka.R = random.Random(704061)
ph_common.GRADE = "grade-4"



def build():
    sets, R = build_sets([
        ("Add 4-digit numbers", [("run", usa.set_add4, ("rnd", "seen"), 20)]),
        ("Add 5- and 6-digit numbers", [("run", usa.set_add56, ("rnd", "seen"), 20)]),
        ("Subtract with regrouping", [("run", usa.set_sub4, ("rnd", "seen"), 20)]),
        ("Subtract across zeros", [("run", usa.set_zeros, ("rnd", "seen"), 20)]),
        ("Word problems and checking", [("run", uka.set_check, ("rnd",), 10), ("run", uka.set_story, ("rnd",), 10)]),
    ], 70406)
    finish(sets, R)
    body = lesson('<ul><li>Line up the digits by place value, starting from the ones.</li><li>Add or subtract one column at a time, from right to left.</li><li>Adding: if a column is 10 or more, regroup (carry) 1 to the next column.</li><li>Subtracting: if the top digit is smaller, regroup (borrow) from the next column. Check by adding the answer and the number you subtracted.</li></ul>',
        [example("254,368 + 137,945", ["Add from the ones, regrouping 5 times"], "392,313"), example("500,000 − 128,457", ["Regroup across the zeros"], "371,543")],
        [['Forgetting to regroup', 'Write the carried 1 above the next column.'], ['Subtracting the smaller digit from the bigger', 'Regroup when the top digit is smaller.'], ['Lining up from the left', 'Line up the ones.']])
    faq = [('What does MATATAG Math 4 ask about addition and subtraction?', 'Add numbers with sums up to 1 000 000 and subtract numbers where both numbers are less than 1 000 000, with and without regrouping.'), ('How do I check a subtraction?', 'Add the answer to the number you subtracted. You should get the first number.'), ('What is regrouping?', 'Trading 10 of one place for 1 of the next place.'), ('Should I estimate first?', 'Yes. An estimate shows if your answer is reasonable.')]
    make('adding-and-subtracting-to-1000000', 6, 'Number and Algebra', 'Grade 4: Number and Algebra',
         'Add numbers with sums up to 1 000 000 and subtract numbers where both numbers are less than 1 000 000, with and without regrouping.',
         'Adding and Subtracting Numbers up to 1,000,000', 'Addition and Subtraction',
         'Free Grade 4 addition and subtraction worksheets for the DepEd MATATAG curriculum: add and subtract numbers up to 1,000,000 with regrouping, across zeros and in word problems. 100 questions with answers.',
         'Line up the ones; work from right to left.', 'Check a subtraction by adding.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
