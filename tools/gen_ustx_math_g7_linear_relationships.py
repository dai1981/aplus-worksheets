# -*- coding: utf-8 -*-
"""
Texas Grade 7 Math: Linear Relationships: y = mx + b (TEKS 7.7A)
  python3 tools/gen_ustx_math_g7_linear_relationships.py
Writing y = mx + b from tables and words, from graphs and from two points, what m and b mean, and describing graphs
(the US makers with a new seed).
Wrong answers come from real mistakes: switching m and b, reading the rate from one point only, and thinking every
line starts at 0.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g8_linear_functions as lf
adopt(lf)
lf.R = random.Random(670160)
import gen_us_math_g8_slope as sl
adopt(sl)
sl.R = random.Random(670161)
tx_common.GRADE = "grade-7"



def build():
    sets, R = build_sets([
        ("Rate of change in tables and equations", [("run", sl.set_table_eq, (), 20)]),
        ("Write y = mx + b from tables and words", [("run", lf.set_tables, (), 20)]),
        ("Write the equation from a graph", [("run", lf.set_graph, (), 20)]),
        ("What m and b mean", [("run", lf.set_meaning, (), 20)]),
        ("Describe graphs of situations", [("run", lf.set_story, (), 20)]),
    ], 67016)
    finish(sets, R)
    body = lesson('<ul><li>A <b>linear relationship</b> has a constant rate of change. Its equation is <b>y = mx + b</b>.</li><li><b>m</b> is the rate of change (how much y changes when x goes up by 1).</li><li><b>b</b> is the starting value, where the line crosses the y-axis (x = 0).</li><li>If b = 0, the relationship is proportional: y = mx.</li></ul>',
        [example("x: 0, 1, 2, 3  y: 5, 8, 11, 14", ["y goes up 3 each time: m = 3", "y = 5 when x = 0: b = 5"], "y = 3x + 5")],
        [['Switching m and b', 'm multiplies x; b is added.'], ['Finding m from one point', 'Use the change in y ÷ the change in x.'], ['Thinking every line starts at 0', 'Check the y-value when x = 0.']])
    faq = [('What does TEKS 7.7A ask?', 'Represent linear relationships using verbal descriptions, tables, graphs and equations that simplify to the form y = mx + b.'), ('What does b mean in a story?', 'The starting amount, like a $25 sign-up fee.'), ('How is y = mx + b different from y = kx?', 'y = kx always passes through (0, 0); y = mx + b may not.'), ('What does a negative m mean?', 'y goes down as x goes up.')]
    make('linear-relationships', 16, 'Expressions, Equations and Relationships', '7.7A',
         '7.7A represent linear relationships using verbal descriptions, tables, graphs, and equations that simplify to the form y = mx + b',
         'Linear Relationships: y = mx + b', 'Linear Relationships',
         'Free Grade 7 worksheets for Texas TEKS 7.7A: linear relationships y = mx + b from tables, words and graphs, rate of change, starting value and describing graphs. 100 questions with answers.',
         'y = mx + b: m is the rate, b is the start.', 'x: 0, 1, 2  y: 5, 8, 11 → y = 3x + 5.',
         body, faq, sets, seo_title='Grade 7 Linear Relationships Worksheets: y = mx + b (TEKS 7.7A, STAAR)')


if __name__ == "__main__":
    build()
