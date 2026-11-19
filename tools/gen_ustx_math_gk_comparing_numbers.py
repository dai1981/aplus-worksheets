# -*- coding: utf-8 -*-
"""
Texas Kindergarten Math: Comparing Numbers: More, Fewer, the Same (TEKS K.2E, K.2G, K.2H)
  python3 tools/gen_ustx_math_gk_comparing_numbers.py
More, fewer or the same, the most and the fewest, making the same number, comparing numbers, and stories (the US
Kindergarten makers with Texas names).
Wrong answers come from real mistakes: picking the longer row instead of the larger number, and mixing up more and
fewer.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_gk_comparing_numbers as cm
adopt(cm)
tx_common.GRADE = "kindergarten"



def build():
    sets, R = build_sets([
        ("More, fewer or the same", [("run", cm.set_rows, ("rnd", cm.Kids), 20)]),
        ("The most and the fewest", [("run", cm.set_boxes, ("rnd", cm.Kids), 20)]),
        ("The same number", [("run", cm.set_same, ("rnd", cm.Kids), 20)]),
        ("Which number is greater?", [("run", cm.set_numbers, ("rnd", cm.Kids), 20)]),
        ("Comparing stories", [("run", cm.set_stories, ("rnd", cm.Kids), 20)]),
    ], 69005)
    finish(sets, R)
    body = lesson('<ul><li>Match the things one to one. The group with some left over has <b>more</b>.</li><li>The other group has <b>fewer</b>.</li><li>If nothing is left over, they are <b>the same</b>.</li><li>A number that comes later when you count is <b>greater</b>.</li></ul>',
        [example("7 apples and 5 cups", ["match them: 2 apples left"], "more apples")],
        [['Picking the longer row', 'Big pictures can take more space. Count them.'], ['Mixing up more and fewer', 'Fewer means less.'], ['Counting only one group', 'Count both groups.']])
    faq = [('What does TEKS K.2G ask?', 'Compare sets of objects up to at least 20 in each set using comparative language.'), ('What does TEKS K.2H ask?', 'Use comparative language to describe two numbers up to 20 presented as written numerals.'), ('What does TEKS K.2E ask?', 'Generate a set using concrete and pictorial models that represents a number that is more than, less than, and equal to a given number up to 20.'), ('Which is greater, 9 or 12?', '12.')]
    make('comparing-numbers-to-20', 5, 'Number and Operations', 'K.2E, K.2G, K.2H',
         'K.2E generate a set using concrete and pictorial models that represents a number that is more than, less than, and equal to a given number up to 20; K.2G compare sets of objects up to at least 20 in each set using comparative language; K.2H use comparative language to describe two numbers up to 20 presented as written numerals',
         'Comparing Numbers: More, Fewer, the Same', 'Comparing Numbers',
         'Free kindergarten comparing worksheets for Texas TEKS K.2E, K.2G and K.2H: more, fewer, the same, the most and the fewest, and comparing numbers to 20. 100 questions with answers.',
         'Match one to one; the group with extras has more.', '12 is greater than 9.',
         body, faq, sets, seo_title='Kindergarten Comparing Numbers Worksheets: More, Fewer, the Same (TEKS K.2G)')


if __name__ == "__main__":
    build()
