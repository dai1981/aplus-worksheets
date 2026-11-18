# -*- coding: utf-8 -*-
"""
Texas Grade 1 Math: 10 More and 10 Less (TEKS 1.5C)
  python3 tools/gen_ustx_math_g1_ten_more_less.py
10 more and 10 less with base-ten blocks, on a hundred chart, mixed with 1 more and 1 less, and stories (the US
Grade 1 makers with Texas names).
Wrong answers come from real mistakes: changing the ones digit, adding 1 instead of 10, and going the wrong way.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g1_ten_more_less as tm
adopt(tm)
tx_common.GRADE = "grade-1"



def build():
    sets, R = build_sets([
        ("10 more with base-ten blocks", [("run", tm.set_more_blocks, ("rnd",), 20)]),
        ("10 less with base-ten blocks", [("run", tm.set_less_blocks, ("rnd",), 20)]),
        ("Use a hundred chart", [("run", tm.set_chart, ("rnd",), 20)]),
        ("10 more, 10 less, 1 more, 1 less", [("run", tm.set_mixed, ("rnd",), 20)]),
        ("Word problems: 10 more and 10 less", [("run", tm.set_stories, ("rnd", tm.People), 20)]),
    ], 69111)
    finish(sets, R)
    body = lesson('<ul><li><b>10 more</b>: the tens digit goes up by 1. 34 → 44.</li><li><b>10 less</b>: the tens digit goes down by 1. 34 → 24.</li><li>The ones digit stays the same.</li><li>On a hundred chart, 10 more is the number just below.</li></ul>',
        [example("10 more than 38", ["3 tens → 4 tens"], "48")],
        [['Changing the ones digit', 'Only the tens change.'], ['Adding 1 instead of 10', '10 more than 38 is 48, not 39.'], ['Going the wrong way', 'More goes up; less goes down.']])
    faq = [('What does TEKS 1.5C ask?', 'Use relationships to determine the number that is 10 more and 10 less than a given number up to 120.'), ('What is 10 more than 95?', '105.'), ('What is 10 less than 110?', '100.'), ('Why does only the tens digit change?', 'Adding or taking 1 ten does not change the ones.')]
    make('10-more-and-10-less', 11, 'Algebraic Reasoning', '1.5C',
         '1.5C use relationships to determine the number that is 10 more and 10 less than a given number up to 120',
         '10 More and 10 Less', '10 More and 10 Less',
         'Free Grade 1 worksheets for Texas TEKS 1.5C: find 10 more and 10 less with blocks, a hundred chart and stories. 100 questions with answers.',
         'Only the tens digit changes.', '10 more than 38 is 48; 10 less is 28.',
         body, faq, sets, seo_title='Grade 1 10 More and 10 Less Worksheets (TEKS 1.5C)')


if __name__ == "__main__":
    build()
