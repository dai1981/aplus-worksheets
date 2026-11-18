# -*- coding: utf-8 -*-
"""
Texas Grade 2 Math: Adding and Subtracting Two-Digit Numbers (TEKS 2.4B)
  python3 tools/gen_ustx_math_g2_two_digit.py
Base-ten blocks, adding two-digit numbers, subtracting two-digit numbers, adding up to four two-digit numbers, and
missing numbers (the US Grade 2 makers with Texas names).
Wrong answers come from real mistakes: forgetting to regroup, subtracting the smaller digit from the bigger one,
and adding the tens as ones.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g2_add_sub_100 as as1
adopt(as1)
tx_common.GRADE = "grade-2"



def build():
    sets, R = build_sets([
        ("Base-ten blocks", [("run", as1.set_blocks, ("rnd", "seen"), 20)]),
        ("Add two-digit numbers", [("run", as1.set_add, ("rnd", as1.People, "seen"), 20)]),
        ("Subtract two-digit numbers", [("run", as1.set_sub, ("rnd", "seen"), 20)]),
        ("Add three or four two-digit numbers", [("run", as1.set_several, ("rnd", as1.People, "seen"), 20)]),
        ("Missing numbers", [("run", as1.set_missing, ("rnd", as1.People, "seen"), 20)]),
    ], 69206)
    finish(sets, R)
    body = lesson('<ul><li>Add the ones, then the tens. If there are 10 or more ones, <b>regroup</b> 10 ones as 1 ten.</li><li>To subtract, if there are not enough ones, regroup 1 ten as 10 ones.</li><li>To add several numbers, look for pairs that make 10 or 100.</li><li>Check subtraction by adding.</li></ul>',
        [example("47 + 38", ["7 + 8 = 15: write 5, regroup 1 ten", "4 + 3 + 1 = 8 tens"], "85"), example("62 − 27", ["Regroup: 5 tens 12 ones", "12 − 7 = 5, 5 − 2 = 3"], "35")],
        [['Forgetting to regroup', '15 ones = 1 ten and 5 ones.'], ['Subtracting the smaller digit from the bigger', '62 − 27: regroup, do not do 7 − 2.'], ['Adding tens as ones', '4 tens + 3 tens = 7 tens = 70.']])
    faq = [('What does TEKS 2.4B ask?', 'Add up to four two-digit numbers and subtract two-digit numbers using mental strategies and algorithms based on knowledge of place value and properties of operations.'), ('What does regroup mean?', 'Trade 10 ones for 1 ten, or 1 ten for 10 ones.'), ('How can I add 4 numbers fast?', 'Make tens first: 26 + 14 = 40.'), ('How do I check subtraction?', 'Add the answer to the number you took away.')]
    make('adding-and-subtracting-two-digit-numbers', 6, 'Number and Operations', '2.4B',
         '2.4B add up to four two-digit numbers and subtract two-digit numbers using mental strategies and algorithms based on knowledge of place value and properties of operations',
         'Adding and Subtracting Two-Digit Numbers', 'Adding and Subtracting Two-Digit Numbers',
         'Free Grade 2 worksheets for Texas TEKS 2.4B: add and subtract two-digit numbers with base-ten blocks and regrouping, add up to four two-digit numbers and missing numbers. 100 questions with answers.',
         'Add or subtract the ones, then the tens. Regroup when you need to.', '47 + 38 = 85. 62 − 27 = 35.',
         body, faq, sets, seo_title='Grade 2 Adding and Subtracting Two-Digit Numbers Worksheets (TEKS 2.4B)')


if __name__ == "__main__":
    build()
