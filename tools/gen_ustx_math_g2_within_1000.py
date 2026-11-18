# -*- coding: utf-8 -*-
"""
Texas Grade 2 Math: Adding and Subtracting Within 1,000 (TEKS 2.4C)
  python3 tools/gen_ustx_math_g2_within_1000.py
Mental math with tens and hundreds, base-ten blocks, adding with regrouping, subtracting with regrouping, and open
number lines (the US Grade 2 makers with Texas names).
Wrong answers come from real mistakes: forgetting to regroup, regrouping across a zero wrongly, and adding the
wrong place.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g2_add_sub_1000 as as3
adopt(as3)
tx_common.GRADE = "grade-2"



def build():
    sets, R = build_sets([
        ("Mental math with tens and hundreds", [("run", as3.set_mental, ("rnd", as3.People), 20)]),
        ("Base-ten blocks", [("run", as3.set_blocks, ("rnd", as3.People, "seen"), 20)]),
        ("Add with regrouping", [("run", as3.set_regroup_add, ("rnd", as3.People, "seen"), 20)]),
        ("Subtract with regrouping", [("run", as3.set_subtract, ("rnd", as3.People, "seen"), 20)]),
        ("Open number lines", [("run", as3.set_lines, ("rnd", as3.People), 20)]),
    ], 69207)
    finish(sets, R)
    body = lesson('<ul><li>Line up the ones, tens and hundreds.</li><li>Add or subtract one place at a time, starting with the ones.</li><li>Regroup when a place has 10 or more (adding) or not enough (subtracting).</li><li>Use an open number line to jump by hundreds, tens and ones.</li></ul>',
        [example("356 + 278", ["6 + 8 = 14: regroup", "5 + 7 + 1 = 13: regroup", "3 + 2 + 1 = 6"], "634"), example("503 − 167", ["Regroup across the 0", "13 − 7, 9 − 6, 4 − 1"], "336")],
        [['Forgetting to regroup', '14 ones = 1 ten and 4 ones.'], ['Regrouping across a zero wrongly', '503 is 4 hundreds, 9 tens, 13 ones.'], ['Adding the wrong places', 'Line up the digits by place value.']])
    faq = [('What does TEKS 2.4C ask?', 'Solve one-step and multi-step word problems involving addition and subtraction within 1,000 using a variety of strategies based on place value, including algorithms.'), ('What is an open number line?', 'A line with no marks where you draw your own jumps.'), ('How can I check my answer?', 'Estimate first, or add back to check a subtraction.'), ('What is mental math?', 'Solving in your head, like 450 + 200 = 650.')]
    make('adding-and-subtracting-within-1000', 7, 'Number and Operations', '2.4C',
         '2.4C solve one-step and multi-step word problems involving addition and subtraction within 1,000 using a variety of strategies based on place value, including algorithms',
         'Adding and Subtracting Within 1,000', 'Adding and Subtracting Within 1,000',
         'Free Grade 2 worksheets for Texas TEKS 2.4C: add and subtract within 1,000 with mental math, base-ten blocks, regrouping and open number lines. 100 questions with answers.',
         'Line up the places and start with the ones.', '356 + 278 = 634. 503 − 167 = 336.',
         body, faq, sets, seo_title='Grade 2 Adding and Subtracting Within 1,000 Worksheets (TEKS 2.4C)')


if __name__ == "__main__":
    build()
