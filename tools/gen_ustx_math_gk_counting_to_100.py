# -*- coding: utf-8 -*-
"""
Texas Kindergarten Math: Counting to 100 by Ones and Tens (TEKS K.5)
  python3 tools/gen_ustx_math_gk_counting_to_100.py
Counting on to 20, counting by 10s, counting on from any number, the hundred chart, and stories (the US Kindergarten
makers with Texas names).
Wrong answers come from real mistakes: missing the decade change (29, 20), and adding 1 when counting by 10s.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_gk_counting_to_100 as c1
adopt(c1)
tx_common.GRADE = "kindergarten"



def build():
    sets, R = build_sets([
        ("Count on to 20", [("run", c1.set_to_20, ("rnd", c1.People), 20)]),
        ("Count by 10s", [("run", c1.set_tens, ("rnd", c1.People), 20)]),
        ("Count on from any number", [("run", c1.set_any, ("rnd", c1.People), 20)]),
        ("Hundred chart", [("run", c1.set_chart, ("rnd", c1.People), 20)]),
        ("Counting stories", [("run", c1.set_stories, ("rnd", c1.People), 20)]),
    ], 69010)
    finish(sets, R)
    body = lesson('<ul><li>Count by <b>ones</b>: 27, 28, 29, 30.</li><li>After 29 comes 30: the ones start again.</li><li>Count by <b>tens</b>: 10, 20, 30 … 100.</li><li>You can start counting from any number.</li></ul>',
        [example("Count on: 38, 39, ☐", ["after 39 comes 40"], "40")],
        [['Missing the decade change', 'After 39 comes 40.'], ['Adding 1 when counting by 10s', '10, 20, 30, not 10, 11.'], ['Starting again at 1', 'Start from the number given.']])
    faq = [('What does TEKS K.5 ask?', 'Recite numbers up to at least 100 by ones and tens beginning with any given number.'), ('What comes after 69?', '70.'), ('How many tens make 100?', '10 tens.'), ('How can a hundred chart help?', 'Each row is the next ten.')]
    make('counting-to-100-by-ones-and-tens', 10, 'Algebraic Reasoning', 'K.5',
         'K.5 recite numbers up to at least 100 by ones and tens beginning with any given number',
         'Counting to 100 by Ones and Tens', 'Counting to 100',
         'Free kindergarten counting worksheets for Texas TEKS K.5: count to 100 by ones and tens from any number, with a hundred chart. 100 questions with answers.',
         'By ones: 38, 39, 40. By tens: 10, 20, 30.', 'After 39 comes 40.',
         body, faq, sets, seo_title='Kindergarten Counting to 100 by Ones and Tens Worksheets (TEKS K.5)')


if __name__ == "__main__":
    build()
