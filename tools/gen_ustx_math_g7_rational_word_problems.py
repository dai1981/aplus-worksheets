# -*- coding: utf-8 -*-
"""
Texas Grade 7 Math: Rational Number Word Problems (TEKS 7.3B)
  python3 tools/gen_ustx_math_g7_rational_word_problems.py
Choosing the operation, integer, decimal and fraction word problems, and multi-step problems (the US Grade 7
makers with a new seed).
Wrong answers come from real mistakes: choosing the wrong operation, losing a negative sign, and stopping after one
step.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g7_rational_number_word_problems as rw
adopt(rw)
rw.R = random.Random(670040)
tx_common.GRADE = "grade-7"



def build():
    sets, R = build_sets([
        ("Choose the operation", [("run", rw.set_operation, (), 20)]),
        ("Integer word problems", [("run", rw.set_integers, (), 20)]),
        ("Decimal word problems", [("run", rw.set_decimals, (), 20)]),
        ("Fraction and mixed-number word problems", [("run", rw.set_fractions, (), 20)]),
        ("Multi-step problems", [("run", rw.set_multistep, (), 20)]),
    ], 67004)
    finish(sets, R)
    body = lesson('<ul><li>Read the problem and decide what happens: joining (+), taking away or comparing (−), equal groups (×) or sharing (÷).</li><li>Use negative numbers for losses, drops, debts and below-zero values.</li><li>Estimate first, then compute.</li><li>Check that the answer makes sense in the story.</li></ul>',
        [example("At 6 a.m. it is −8°F. It rises 15 degrees.", ["−8 + 15"], "7°F"), example("Ruby has $50. She buys 3 books at $8.75.", ["3 × 8.75 = 26.25", "50 − 26.25"], "$23.75")],
        [['Choosing the wrong operation', 'Ask what happens in the story: join, take away, groups or share?'], ['Losing a negative sign', 'A drop below zero gives a negative number.'], ['Stopping after one step', 'Read the question again: what does it ask for?']])
    faq = [('What does TEKS 7.3B ask?', 'Apply and extend previous understandings of operations to solve problems using addition, subtraction, multiplication and division of rational numbers.'), ('When do I use a negative number?', 'For values below zero, losses, debts, drops in temperature or depth below sea level.'), ('Should I estimate first?', 'Yes. An estimate tells you if your exact answer is reasonable.'), ('How do I check a multi-step problem?', 'Work backward, or plug your answer into the story.')]
    make('rational-number-word-problems', 4, 'Number and Operations', '7.3B',
         '7.3B apply and extend previous understandings of operations to solve problems using addition, subtraction, multiplication, and division of rational numbers',
         'Rational Number Word Problems', 'Rational Number Word Problems',
         'Free Grade 7 worksheets for Texas TEKS 7.3B: choose the operation, integer, decimal and fraction word problems, and multi-step rational number problems. 100 questions with answers.',
         'Decide what happens in the story, then choose the operation.', 'Use negatives for drops, debts and below zero. Estimate, compute and check.',
         body, faq, sets, seo_title='Grade 7 Rational Number Word Problems Worksheets (TEKS 7.3B, STAAR)')


if __name__ == "__main__":
    build()
