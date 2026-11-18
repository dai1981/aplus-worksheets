# -*- coding: utf-8 -*-
"""
Texas Grade 1 Math: Numbers to 120: Tens and Ones (TEKS 1.2B, 1.2C)
  python3 tools/gen_ustx_math_g1_numbers_to_120.py
Base-ten blocks, teen numbers, tens and ones in a number, tens with 0 ones and more than 9 ones, and stories
(the US Grade 1 makers with Texas names).
Wrong answers come from real mistakes: swapping the tens and the ones, counting a rod as 1, and writing 40 + 5 as 405.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g1_place_value as pv
adopt(pv)
import random
pv.P = pv.People(random.Random(69101))
tx_common.GRADE = "grade-1"



def build():
    sets, R = build_sets([
        ("Count tens and ones in blocks", [("run", pv.set_blocks, ("rnd", "seen"), 20)]),
        ("Teen numbers: 1 ten and some ones", [("run", pv.set_teens, ("rnd", "seen"), 20)]),
        ("Tens and ones in a number", [("run", pv.set_digits, ("rnd", "seen"), 20)]),
        ("Tens with 0 ones, and more than 9 ones", [("run", pv.set_decades, ("rnd", "seen"), 20)]),
        ("Tens and ones stories", [("run", pv.set_story, ("rnd", "seen"), 20)]),
    ], 69101)
    finish(sets, R)
    body = lesson('<ul><li>A <b>ten</b> is 10 ones put together. A rod shows 1 ten.</li><li>In 47, the 4 means 4 tens (40) and the 7 means 7 ones.</li><li>47 = 40 + 7. This is the <b>expanded form</b>.</li><li>12 ones is the same as 1 ten and 2 ones.</li></ul>',
        [example("3 rods and 6 cubes", ["3 tens = 30", "30 + 6"], "36")],
        [['Swapping tens and ones', 'The tens digit is on the left.'], ['Counting a rod as 1', 'Each rod is 10.'], ['Writing 40 + 5 as 405', '40 + 5 = 45.']])
    faq = [('What does TEKS 1.2B ask?', 'Use concrete and pictorial models to compose and decompose numbers up to 120 in more than one way as so many hundreds, so many tens, and so many ones.'), ('What does TEKS 1.2C ask?', 'Use objects, pictures, and expanded and standard forms to represent numbers up to 120.'), ('Is 1 ten and 14 ones the same as 24?', 'Yes. 10 + 14 = 24.'), ('What is expanded form?', 'A number written as tens plus ones, like 30 + 6.')]
    make('numbers-to-120', 1, 'Number and Operations', '1.2B, 1.2C',
         '1.2B use concrete and pictorial models to compose and decompose numbers up to 120 in more than one way as so many hundreds, so many tens, and so many ones; 1.2C use objects, pictures, and expanded and standard forms to represent numbers up to 120',
         'Numbers to 120: Tens and Ones', 'Numbers to 120',
         'Free Grade 1 place value worksheets for Texas TEKS 1.2B and 1.2C: base-ten blocks, teen numbers, tens and ones and expanded form to 120. 100 questions with answers.',
         'A ten is 10 ones. 47 is 4 tens and 7 ones.', '47 = 40 + 7',
         body, faq, sets, seo_title='Grade 1 Numbers to 120: Tens and Ones Worksheets (TEKS 1.2B)')


if __name__ == "__main__":
    build()
