# -*- coding: utf-8 -*-
"""
Texas Grade 8 Math: Writing Linear Equations y = mx + b (TEKS 8.5I)
  python3 tools/gen_ustx_math_g8_linear_equations_y_mx_b.py
Writing y = mx + b from tables and words, from graphs and from two points, what m and b mean, and describing
graphs (the US Grade 8 makers with a new seed).
Wrong answers come from real mistakes: switching m and b, using a point instead of the y-intercept for b, and
getting the sign of the slope wrong.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g8_linear_functions as lf
adopt(lf)
lf.R = random.Random(680080)
tx_common.GRADE = "grade-8"



def build():
    sets, R = build_sets([
        ("Equations from tables and words", [("run", lf.set_tables, (), 20)]),
        ("Write the equation from a graph", [("run", lf.set_graph, (), 20)]),
        ("Write the equation from two points", [("run", lf.set_points, (), 20)]),
        ("What m and b mean", [("run", lf.set_meaning, (), 20)]),
        ("Describe graphs of situations", [("run", lf.set_story, (), 20)]),
    ], 68008)
    finish(sets, R)
    body = lesson('<ul><li>In <b>y = mx + b</b>, m is the slope (rate of change) and b is the y-intercept (starting value).</li><li>From a table, find m from the change in y ÷ change in x, and b from the row where x = 0.</li><li>From two points, find m first, then substitute one point to find b.</li><li>In a story, the rate is m and the fixed starting amount is b.</li></ul>',
        [example("(0, 3) and (2, 7)", ["m = (7 − 3) ÷ 2 = 2", "b = 3"], "y = 2x + 3"), example("$25 fee plus $10 per hour", ["m = 10, b = 25"], "y = 10x + 25")],
        [['Switching m and b', 'm multiplies x; b is the constant.'], ["Using any point's y for b", 'b is the y-value when x = 0.'], ['Getting the sign of m wrong', 'A line that goes down has negative m.']])
    faq = [('What does TEKS 8.5I ask?', 'Write an equation in the form y = mx + b to model a linear relationship between two quantities using verbal, numerical, tabular and graphical representations.'), ('How do I find b from two points?', 'Substitute one point and the slope into y = mx + b and solve for b.'), ('What if b = 0?', 'Then the relationship is proportional: y = mx.'), ('Can m be a fraction?', 'Yes, for example y = ½x + 4.')]
    make('writing-linear-equations', 8, 'Proportionality', '8.5I',
         '8.5I write an equation in the form y = mx + b to model a linear relationship between two quantities using verbal, numerical, tabular, and graphical representations',
         'Writing Linear Equations y = mx + b', 'Writing Linear Equations',
         'Free Grade 8 worksheets for Texas TEKS 8.5I: write y = mx + b from tables, words, graphs and two points, and interpret slope and y-intercept. 100 questions with answers.',
         'y = mx + b: m is the rate, b is the start.', '(0, 3) and (2, 7) → y = 2x + 3.',
         body, faq, sets, seo_title='Grade 8 Writing Linear Equations y = mx + b Worksheets (TEKS 8.5I, STAAR)')


if __name__ == "__main__":
    build()
