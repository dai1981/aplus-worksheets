# -*- coding: utf-8 -*-
"""
Texas Grade 8 Math: Identifying Functions (TEKS 8.5G, 8.5H)
  python3 tools/gen_ustx_math_g8_functions.py
Is it a function (ordered pairs, tables and mappings), graphs and the vertical line test, evaluating functions,
linear or nonlinear, and comparing functions (the US Grade 8 makers with a new seed).
Wrong answers come from real mistakes: thinking repeated y-values break a function, missing a repeated x-value,
and mixing up input and output.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g8_functions as fn
adopt(fn)
fn.R = random.Random(680090)
tx_common.GRADE = "grade-8"



def build():
    sets, R = build_sets([
        ("Is it a function?", [("run", fn.set_relations, (), 20)]),
        ("Graphs and the vertical line test", [("run", fn.set_graphs, (), 20)]),
        ("Evaluate a function", [("run", fn.set_eval, (), 20)]),
        ("Linear or nonlinear?", [("run", fn.set_linear, (), 20)]),
        ("Compare functions", [("run", fn.set_compare, (), 20)]),
    ], 68009)
    finish(sets, R)
    body = lesson('<ul><li>A <b>function</b> gives exactly one output for each input.</li><li>In ordered pairs or a table, no x-value may repeat with a different y-value. Repeated y-values are fine.</li><li><b>Vertical line test</b>: if any vertical line crosses a graph more than once, it is not a function.</li><li>A linear function has a constant rate of change; its graph is a straight line.</li></ul>',
        [example("{(1, 4), (2, 5), (1, 6)}", ["x = 1 has two outputs"], "not a function"), example("f(x) = 3x − 2, f(4)", ["3 × 4 − 2"], "10")],
        [['Thinking repeated y-values break a function', '(1, 5) and (2, 5) is fine: each input has one output.'], ['Missing a repeated x-value', 'Check every input once.'], ['Mixing up input and output', 'x is the input; y = f(x) is the output.']])
    faq = [('What does TEKS 8.5G ask?', 'Identify functions using sets of ordered pairs, tables, mappings and graphs.'), ('What does TEKS 8.5H ask?', 'Identify examples of proportional and non-proportional functions that arise from mathematical and real-world problems.'), ('Is a horizontal line a function?', 'Yes. Every input has the same one output.'), ('Is a circle a function?', 'No. A vertical line can cross it twice.')]
    make('functions', 9, 'Proportionality', '8.5G, 8.5H',
         '8.5G identify functions using sets of ordered pairs, tables, mappings, and graphs; 8.5H identify examples of proportional and non-proportional functions that arise from mathematical and real-world problems',
         'Identifying Functions', 'Functions',
         'Free Grade 8 function worksheets for Texas TEKS 8.5G and 8.5H: ordered pairs, tables, mappings, the vertical line test, evaluating, linear or nonlinear and comparing functions. 100 questions with answers.',
         'A function gives exactly one output for each input.', 'Repeated x with different y: not a function. Vertical line test for graphs.',
         body, faq, sets, seo_title='Grade 8 Identifying Functions Worksheets (TEKS 8.5G, STAAR)')


if __name__ == "__main__":
    build()
