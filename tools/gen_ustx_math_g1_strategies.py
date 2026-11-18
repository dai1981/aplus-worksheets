# -*- coding: utf-8 -*-
"""
Texas Grade 1 Math: Addition and Subtraction Strategies (TEKS 1.3E)
  python3 tools/gen_ustx_math_g1_strategies.py
Counting on and back, turn-around facts, subtracting by thinking addition, fact families, and choosing a strategy for
word problems (the US Grade 1 makers with Texas names).
Wrong answers come from real mistakes: counting the start number, thinking 9 − 3 = 3 − 9, and mixing up the parts and the whole.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g1_strategies as st
adopt(st)
tx_common.GRADE = "grade-1"



def build():
    sets, R = build_sets([
        ("Count on and count back", [("run", st.set_count, (st.People,), 20)]),
        ("Turn-around facts and make a ten", [("run", st.set_turn_around, (st.People,), 20)]),
        ("Subtract by thinking addition", [("run", st.set_think_add, (st.People,), 20)]),
        ("Fact families", [("run", st.set_families, (st.People,), 20)]),
        ("Word problems: choose a strategy", [("run", st.set_stories, (st.People,), 20)]),
    ], 69106)
    finish(sets, R)
    body = lesson('<ul><li><b>Count on</b> to add small numbers; <b>count back</b> to take away small numbers.</li><li><b>Turn-around facts</b>: 2 + 5 = 5 + 2.</li><li><b>Think addition</b>: 12 − 5 = ? because 5 + 7 = 12.</li><li>A <b>fact family</b> uses the same 3 numbers: 3 + 4 = 7, 4 + 3 = 7, 7 − 3 = 4, 7 − 4 = 3.</li></ul>',
        [example("12 − 5", ["Think: 5 + ? = 12"], "7")],
        [['Counting the start number', 'Count on from the next number.'], ['Turning around a subtraction', '9 − 3 is not 3 − 9.'], ['Mixing up parts and whole', 'The whole is the biggest number in a fact family.']])
    faq = [('What does TEKS 1.3E ask?', 'Explain strategies used to solve addition and subtraction problems up to 20 using spoken words, objects, pictorial models, and number sentences.'), ('What is a fact family?', 'Facts that use the same three numbers.'), ('Does the order matter in addition?', 'No. 2 + 5 and 5 + 2 are both 7.'), ('Does the order matter in subtraction?', 'Yes. Start with the whole.')]
    make('addition-and-subtraction-strategies', 6, 'Number and Operations', '1.3E',
         '1.3E explain strategies used to solve addition and subtraction problems up to 20 using spoken words, objects, pictorial models, and number sentences',
         'Addition and Subtraction Strategies', 'Addition and Subtraction Strategies',
         'Free Grade 1 strategy worksheets for Texas TEKS 1.3E: count on and back, turn-around facts, think addition to subtract and fact families. 100 questions with answers.',
         'Count on, turn it around, or think addition.', '12 − 5 = 7 because 5 + 7 = 12.',
         body, faq, sets, seo_title='Grade 1 Addition and Subtraction Strategies Worksheets (TEKS 1.3E)')


if __name__ == "__main__":
    build()
