# -*- coding: utf-8 -*-
"""
Texas Kindergarten Math: Adding and Subtracting: Show Your Thinking (TEKS K.3C)
  python3 tools/gen_ustx_math_gk_strategies.py
Adding and subtracting within 5, missing numbers, mixed facts, and stories (the US Kindergarten makers with Texas
names).
Wrong answers come from real mistakes: mixing up + and −, and giving a number from the problem.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_gk_add_and_subtract_within_5 as a5
adopt(a5)
tx_common.GRADE = "kindergarten"



def build():
    sets, R = build_sets([
        ("Add within 5", [("run", a5.set_add, ("rnd", a5.Kids), 20)]),
        ("Subtract within 5", [("run", a5.set_sub, ("rnd", a5.Kids), 20)]),
        ("Missing numbers", [("run", a5.set_missing, ("rnd", a5.Kids), 20)]),
        ("Mixed facts", [("run", a5.set_mixed, ("rnd", a5.Kids), 20)]),
        ("Stories: add or subtract?", [("run", a5.set_stories, ("rnd", a5.Kids), 20)]),
    ], 69009)
    finish(sets, R)
    body = lesson('<ul><li>Use fingers, pictures or objects to show the problem.</li><li>Joining: add. Taking away: subtract.</li><li>Say how you solved it: “I counted on from 3.”</li><li>Know the small facts fast: 2 + 2 = 4, 5 − 1 = 4.</li></ul>',
        [example("3 + ☐ = 5", ["3, 4, 5: 2 more"], "2")],
        [['Mixing up + and −', 'Read the sign first.'], ['Giving a number from the problem', 'Find the missing number.'], ['Not checking', 'Use fingers to check.']])
    faq = [('What does TEKS K.3C ask?', 'Explain the strategies used to solve problems involving adding and subtracting within 10 using spoken words, concrete and pictorial models, and number sentences.'), ('Why learn facts to 5?', 'They help with bigger facts later.'), ('What is a strategy?', 'A way to solve, like counting on.'), ('How can my child explain?', 'Ask them to show it with fingers or blocks.')]
    make('addition-and-subtraction-strategies', 9, 'Number and Operations', 'K.3C',
         'K.3C explain the strategies used to solve problems involving adding and subtracting within 10 using spoken words, concrete and pictorial models, and number sentences',
         'Adding and Subtracting: Show Your Thinking', 'Addition and Subtraction Strategies',
         'Free kindergarten worksheets for Texas TEKS K.3C: add and subtract within 5, missing numbers, mixed facts and stories with pictures. 100 questions with answers.',
         'Show it, solve it, say how.', '3 + 2 = 5 and 5 − 2 = 3',
         body, faq, sets, seo_title='Kindergarten Addition and Subtraction Strategies Worksheets (TEKS K.3C)')


if __name__ == "__main__":
    build()
