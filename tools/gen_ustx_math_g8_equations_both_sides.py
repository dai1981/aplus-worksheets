# -*- coding: utf-8 -*-
"""
Texas Grade 8 Math: Equations with Variables on Both Sides (TEKS 8.8A, 8.8B, 8.8C)
  python3 tools/gen_ustx_math_g8_equations_both_sides.py
Solving equations with variables on both sides, distributing and combining like terms, fractions and decimals, one,
no or infinitely many solutions, and word problems (the US Grade 8 makers with a new seed).
Wrong answers come from real mistakes: adding the variable terms instead of subtracting, distributing to only the
first term, and stopping at 0 = 0.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g8_linear_equations as le
adopt(le)
le.R = random.Random(680110)
tx_common.GRADE = "grade-8"



def build():
    sets, R = build_sets([
        ("Variables on both sides", [("run", le.set_both, (), 20)]),
        ("Distribute and combine like terms", [("run", le.set_dist, (), 20)]),
        ("Fractions and decimals", [("run", le.set_frac, (), 20)]),
        ("One, none or infinitely many solutions", [("run", le.set_count, (), 20)]),
        ("Word problems", [("run", le.set_words, (), 20)]),
    ], 68011)
    finish(sets, R)
    body = lesson('<ul><li>Get the variable terms on one side: subtract the smaller variable term from both sides.</li><li>Then undo the constants and divide.</li><li>Distribute and combine like terms first if there are parentheses.</li><li>If the variables cancel: a true statement (5 = 5) means infinitely many solutions; a false one (3 = 7) means no solution.</li></ul>',
        [example("5x + 3 = 2x + 15", ["Subtract 2x: 3x + 3 = 15", "3x = 12"], "x = 4"), example("Gym A: 30 + 5v. Gym B: 10 + 9v.", ["30 + 5v = 10 + 9v", "20 = 4v"], "v = 5 visits")],
        [['Adding the variable terms', 'Subtract 2x from both sides, do not add it.'], ['Distributing to only the first term', '3(x + 2) = 3x + 6.'], ['Stopping at 0 = 0', '0 = 0 means every number is a solution.']])
    faq = [('What does TEKS 8.8C ask?', 'Model and solve one-variable equations with variables on both sides of the equal sign that represent mathematical and real-world problems using rational number coefficients and constants.'), ('What does TEKS 8.8A ask?', 'Write one-variable equations or inequalities with variables on both sides that represent problems using rational number coefficients and constants.'), ('How can an equation have no solution?', 'If the variables cancel and leave a false statement, like 4 = 9.'), ('What does TEKS 8.8B ask?', 'Write a corresponding real-world problem when given a one-variable equation or inequality with variables on both sides of the equal sign using rational number coefficients and constants.')]
    make('equations-with-variables-on-both-sides', 11, 'Expressions, Equations and Relationships', '8.8A, 8.8B, 8.8C',
         '8.8A write one-variable equations or inequalities with variables on both sides that represent problems using rational number coefficients and constants; 8.8B write a corresponding real-world problem when given a one-variable equation or inequality with variables on both sides of the equal sign using rational number coefficients and constants; 8.8C model and solve one-variable equations with variables on both sides of the equal sign that represent mathematical and real-world problems using rational number coefficients and constants',
         'Equations with Variables on Both Sides', 'Equations with Variables on Both Sides',
         'Free Grade 8 worksheets for Texas TEKS 8.8: equations with variables on both sides, distributing, fractions and decimals, one, no or infinitely many solutions, and word problems. 100 questions with answers.',
         'Move the variable terms to one side, then solve.', '5x + 3 = 2x + 15 → 3x = 12 → x = 4.',
         body, faq, sets, seo_title='Grade 8 Equations with Variables on Both Sides Worksheets (TEKS 8.8C, STAAR)')


if __name__ == "__main__":
    build()
