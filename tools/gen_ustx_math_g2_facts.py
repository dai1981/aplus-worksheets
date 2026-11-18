# -*- coding: utf-8 -*-
"""
Texas Grade 2 Math: Addition and Subtraction Facts to 20 (TEKS 2.4A)
  python3 tools/gen_ustx_math_g2_facts.py
Ten frames, doubles and near doubles, making 10, subtraction facts, and fact stories (the US Grade 2 makers with
Texas names).
Wrong answers come from real mistakes: counting one too many or too few, mixing up + and −, and not using a
known fact.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g2_facts as fa
adopt(fa)
tx_common.GRADE = "grade-2"



def build():
    sets, R = build_sets([
        ("Ten frames", [("run", fa.set_ten_frames, (fa.People,), 20)]),
        ("Doubles and near doubles", [("run", fa.set_doubles, (fa.People,), 20)]),
        ("Make a ten", [("run", fa.set_make_ten, (fa.People,), 20)]),
        ("Subtraction facts", [("run", fa.set_subtract, (fa.People,), 20)]),
        ("Fact stories", [("run", fa.set_stories, (fa.People,), 20)]),
    ], 69205)
    finish(sets, R)
    body = lesson('<ul><li>Know the facts to 20 by heart. Use a strategy you know to find the rest.</li><li><b>Doubles</b>: 7 + 7 = 14, so 7 + 8 = 15.</li><li><b>Make a ten</b>: 9 + 5 = 10 + 4 = 14.</li><li>Think addition to subtract: 13 − 5 = ? because 5 + 8 = 13.</li></ul>',
        [example("8 + 6", ["8 + 2 = 10", "10 + 4"], "14"), example("15 − 7", ["7 + 8 = 15"], "8")],
        [['Counting one too many', 'Start counting after the first number.'], ['Mixing up + and −', 'Read the sign before you start.'], ['Not using a known fact', 'Use doubles and tens to help.']])
    faq = [('What does TEKS 2.4A ask?', 'Recall basic facts to add and subtract within 20 with automaticity.'), ('What are doubles?', 'Facts with two of the same number, like 6 + 6.'), ('How can a ten frame help?', 'It shows how many more make 10.'), ('How are + and − related?', 'If 8 + 5 = 13, then 13 − 5 = 8.')]
    make('addition-and-subtraction-facts-to-20', 5, 'Number and Operations', '2.4A',
         '2.4A recall basic facts to add and subtract within 20 with automaticity',
         'Addition and Subtraction Facts to 20', 'Addition and Subtraction Facts',
         'Free Grade 2 addition and subtraction fact worksheets for Texas TEKS 2.4A: ten frames, doubles, make a ten, subtraction facts and fact stories. 100 questions with answers.',
         'Use doubles and make a ten.', '8 + 6 = 10 + 4 = 14. 15 − 7 = 8 because 7 + 8 = 15.',
         body, faq, sets, seo_title='Grade 2 Addition and Subtraction Facts to 20 Worksheets (TEKS 2.4A)')


if __name__ == "__main__":
    build()
