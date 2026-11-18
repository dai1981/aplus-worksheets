# -*- coding: utf-8 -*-
"""
Texas Grade 1 Math: Counting Forward and Backward to 120 (TEKS 1.5A)
  python3 tools/gen_ustx_math_g1_counting.py
What comes next or before, missing numbers on a 120 chart, counting objects, reading number words, and counting
past 100 (the US Grade 1 makers with Texas names).
Wrong answers come from real mistakes: skipping a decade change (59, 50), writing 100 and 1 as 1001, and counting
the wrong way.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g1_count_120 as cn
adopt(cn)
tx_common.GRADE = "grade-1"



def build():
    sets, R = build_sets([
        ("Count objects", [("run", cn.set_objects, ("rnd", cn.People), 20)]),
        ("What comes next or before", [("run", cn.set_next, ("rnd", cn.People), 20)]),
        ("Read and write numbers", [("run", cn.set_words, ("rnd", cn.People), 20)]),
        ("Missing numbers on a 120 chart", [("run", cn.set_chart, ("rnd", cn.People), 20)]),
        ("Count past 100 and stories", [("run", cn.set_stories, ("rnd", cn.People), 20)]),
    ], 69109)
    finish(sets, R)
    body = lesson('<ul><li>Count <b>forward</b>: each number is 1 more. Count <b>backward</b>: each number is 1 less.</li><li>After 59 comes 60: the ones go back to 0 and the tens go up.</li><li>After 100 comes 101, 102, … 120.</li><li>On a 120 chart, the number to the right is 1 more.</li></ul>',
        [example("98, 99, 100, ☐", ["1 more than 100"], "101")],
        [['Missing the decade change', 'After 59 comes 60.'], ['Writing 101 as 1001', 'One hundred one is 101.'], ['Counting the wrong way', 'Backward means 1 less each time.']])
    faq = [('What does TEKS 1.5A ask?', 'Recite numbers forward and backward from any given number between 1 and 120.'), ('What comes after 109?', '110.'), ('What comes before 100?', '99.'), ('How can a 120 chart help?', 'Move right for 1 more and down for 10 more.')]
    make('counting-to-120', 9, 'Algebraic Reasoning', '1.5A',
         '1.5A recite numbers forward and backward from any given number between 1 and 120',
         'Counting Forward and Backward to 120', 'Counting to 120',
         'Free Grade 1 counting worksheets for Texas TEKS 1.5A: count forward and backward to 120, next and before, number words and 120 chart puzzles. 100 questions with answers.',
         'Forward is 1 more; backward is 1 less.', '59, 60, 61 … 99, 100, 101',
         body, faq, sets, seo_title='Grade 1 Counting to 120 Worksheets (TEKS 1.5A)')


if __name__ == "__main__":
    build()
