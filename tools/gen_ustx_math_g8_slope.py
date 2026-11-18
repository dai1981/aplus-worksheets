# -*- coding: utf-8 -*-
"""
Texas Grade 8 Math: Slope and Rate of Change (TEKS 8.4A, 8.4C)
  python3 tools/gen_ustx_math_g8_slope.py
Slope from a graph, from two points, from tables and equations, ideas about slope, and slope triangles on the same
line (the US Grade 8 makers with a new seed, plus an own slope-triangle maker).
Wrong answers come from real mistakes: run over rise, subtracting in different orders, and thinking a steeper line
has a smaller slope.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g8_slope as sl
adopt(sl)
sl.R = random.Random(680060)
from fractions import Fraction as F
from ws_common import num
tx_common.GRADE = "grade-8"

def sfrac(v):
    v = F(v)
    if v.denominator == 1:
        return num(v.numerator)
    return ("−" if v < 0 else "") + fr(abs(v.numerator), v.denominator)


def one_tri(r):
    m = F(r.choice([1, 2, 3, -1, -2, -3, 1, 2]), r.choice([1, 1, 2, 3, 4]))
    b = r.randint(-5, 5)
    xs = sorted(r.sample(range(-6, 9), 4))
    pts = [(x, m * x + b) for x in xs]
    if any(p[1].denominator != 1 for p in pts):
        return None
    (x1, y1), (x2, y2) = pts[0], pts[1]
    (x3, y3), (x4, y4) = pts[2], pts[3]
    q = "The points (%s, %s), (%s, %s), (%s, %s) and (%s, %s) are on the same line. What is the slope?" % (num(x1), num(int(y1)), num(x2), num(int(y2)), num(x3), num(int(y3)), num(x4), num(int(y4)))
    w = [sfrac(1 / m), sfrac(-m), sfrac(m + 1)] if m != 0 else ["1", "−1", "2"]
    return mcq(q, sfrac(m), [x for x in dict.fromkeys(w) if x != sfrac(m)],
               "Any two points give the same slope: (%s − %s) ÷ (%s − %s) = <b>%s</b>, and (%s − %s) ÷ (%s − %s) = %s too." % (num(int(y2)), num(int(y1)), num(x2), num(x1), sfrac(m), num(int(y4)), num(int(y3)), num(x4), num(x3), sfrac(m)))


def build():
    sets, R = build_sets([
        ("Slope from a graph", [("run", sl.set_graph, (), 20)]),
        ("Slope from two points", [("run", sl.set_points, (), 20)]),
        ("The same slope for any two points", [("collect", one_tri, 20)]),
        ("Slope and y-intercept from tables and equations", [("run", sl.set_table_eq, (), 20)]),
        ("Understanding slope", [("run", sl.set_ideas, (), 20)]),
    ], 68006)
    finish(sets, R)
    body = lesson('<ul><li><b>Slope</b> m = change in y ÷ change in x = (y₂ − y₁) ÷ (x₂ − x₁).</li><li>Slope triangles on the same line are <b>similar</b>, so every pair of points gives the same slope.</li><li>Up from left to right: positive slope. Down: negative slope. Horizontal: 0.</li><li>In a table, the <b>y-intercept</b> is the y-value when x = 0.</li></ul>',
        [example("(1, 2) and (3, 8)", ["(8 − 2) ÷ (3 − 1) = 6 ÷ 2"], "m = 3"), example("(−2, 5) and (2, −3)", ["(−3 − 5) ÷ (2 − (−2)) = −8 ÷ 4"], "m = −2")],
        [['Run over rise', 'Slope is rise ÷ run: change in y on top.'], ['Subtracting in different orders', 'Use the same point first in the top and the bottom.'], ['Forgetting the sign', 'A line that falls has a negative slope.']])
    faq = [('What does TEKS 8.4A ask?', 'Use similar right triangles to develop an understanding that slope, m, given as the rate comparing the change in y-values to the change in x-values, is the same for any two points on the same line.'), ('What does TEKS 8.4C ask?', 'Use data from a table or graph to determine the rate of change or slope and y-intercept in mathematical and real-world problems.'), ('What is the slope of a vertical line?', 'It is undefined, because the change in x is 0.'), ('Is slope the same as rate of change?', 'Yes. For a line, the slope is its constant rate of change.')]
    make('slope', 6, 'Proportionality', '8.4A, 8.4C',
         '8.4A use similar right triangles to develop an understanding that slope, m, given as the rate comparing the change in y-values to the change in x-values, (y2 − y1)/(x2 − x1), is the same for any two points (x1, y1) and (x2, y2) on the same line; 8.4C use data from a table or graph to determine the rate of change or slope and y-intercept in mathematical and real-world problems',
         'Slope and Rate of Change', 'Slope',
         'Free Grade 8 slope worksheets for Texas TEKS 8.4A and 8.4C: slope from graphs, two points, tables and equations, slope triangles and y-intercepts. 100 questions with answers.',
         'm = (y₂ − y₁) ÷ (x₂ − x₁).', '(1, 2) and (3, 8): m = 3. Every pair of points on a line gives the same slope.',
         body, faq, sets, seo_title='Grade 8 Slope and Rate of Change Worksheets (TEKS 8.4A, 8.4C, STAAR)')


if __name__ == "__main__":
    build()
