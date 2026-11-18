# -*- coding: utf-8 -*-
"""
Texas Grade 7 Math: Two-Step Equations (TEKS 7.10A, 7.10C, 7.11A, 7.11B)
  python3 tools/gen_ustx_math_g7_two_step_equations.py
Undoing two steps in reverse order, solving px + q = r, negative numbers, parentheses, decimals and fractions, and
word problems (the US Grade 7 makers with a new seed).
Wrong answers come from real mistakes: dividing before subtracting, changing only one side, and losing a negative
sign.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g7_two_step_equations as te
adopt(te)
te.R = random.Random(670170)
tx_common.GRADE = "grade-7"



def build():
    sets, R = build_sets([
        ("Two steps: undo in reverse order", [("run", te.set_steps, (), 20)]),
        ("Solve px + q = r", [("run", te.set_basic, (), 20)]),
        ("Negative numbers and x ÷ p", [("run", te.set_negative, (), 20)]),
        ("Parentheses, decimals and fractions", [("run", te.set_mixed, (), 20)]),
        ("Word problems: write and solve", [("run", te.set_words, (), 20)]),
    ], 67017)
    finish(sets, R)
    body = lesson('<ul><li>A <b>two-step equation</b> such as 3x + 5 = 20 has two operations on the variable.</li><li>Undo them in <b>reverse order</b>: first undo the + or −, then undo the × or ÷.</li><li>Do the same step to both sides.</li><li>Check by substituting the answer.</li></ul>',
        [example("3x + 5 = 20", ["Subtract 5: 3x = 15", "Divide by 3"], "x = 5"), example("A $15 fee plus $8 per class is $87.", ["15 + 8c = 87", "8c = 72"], "c = 9")],
        [['Dividing before subtracting', 'Undo + or − first: 3x + 5 = 20 → 3x = 15.'], ['Changing only one side', 'Do the same step to both sides.'], ['Losing a negative sign', '−3x = −15 gives x = 5.']])
    faq = [('What does TEKS 7.11A ask?', 'Model and solve one-variable, two-step equations and inequalities.'), ('What does TEKS 7.10C ask?', 'Write a corresponding real-world problem given a one-variable, two-step equation or inequality.'), ('Why undo in reverse order?', 'It is like taking off shoes and socks: the last thing done is undone first.'), ('How do I check?', 'Substitute the answer into the original equation.')]
    make('two-step-equations', 17, 'Expressions, Equations and Relationships', '7.10A, 7.10C, 7.11A, 7.11B',
         '7.10A write one-variable, two-step equations and inequalities to represent constraints or conditions within problems; 7.10C write a corresponding real-world problem given a one-variable, two-step equation or inequality; 7.11A model and solve one-variable, two-step equations and inequalities; 7.11B determine if the given value(s) make(s) one-variable, two-step equations and inequalities true',
         'Two-Step Equations', 'Two-Step Equations',
         'Free Grade 7 two-step equation worksheets for Texas TEKS 7.10 and 7.11: undo in reverse order, px + q = r, negatives, parentheses, fractions and word problems. 100 questions with answers.',
         'Undo + or − first, then × or ÷.', '3x + 5 = 20 → 3x = 15 → x = 5.',
         body, faq, sets, seo_title='Grade 7 Two-Step Equations Worksheets (TEKS 7.11A, STAAR)')


if __name__ == "__main__":
    build()
