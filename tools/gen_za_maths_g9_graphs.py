# -*- coding: utf-8 -*-
"""
South Africa Grade 9 Maths (CAPS): Linear Graphs: Gradient, Intercepts and y = mx + c (Grade 9: 2.5 Graphs)
  python3 tools/gen_za_maths_g9_graphs.py
Gradient and y-intercept, gradient from a graph or two points, parallel lines, equations of lines, and global graphs
(Singapore Secondary 1, UK Year 8, Australia Year 8 makers and the global graph maker from the Grade 7 generator).
Wrong answers come from real mistakes: mixing up m and c, counting the gradient the wrong way, and thinking parallel
lines have the same intercept.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_sg_maths_s1_linear_graphs_and_gradient as sgl
adopt(sgl)
if isinstance(getattr(sgl, 'R', None), random.Random): sgl.R = random.Random(809100)
import gen_uk_maths_y8_linear_graphs as ukl
adopt(ukl)
if isinstance(getattr(ukl, 'R', None), random.Random): ukl.R = random.Random(809101)
import gen_au_maths_y8_graphing_linear_relations as aug
adopt(aug)
if isinstance(getattr(aug, 'R', None), random.Random): aug.R = random.Random(809102)
import gen_za_maths_g7_graphs as zg7
adopt(zg7)
if isinstance(getattr(zg7, 'R', None), random.Random): zg7.R = random.Random(809103)
za_common.GRADE = "grade-9"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok9(it):
    """Grade 9: no trigonometry, quadratic formula, simultaneous equations or cones and spheres (Grade 10+)"""
    return not _re.search(r"\b(sin|cos|tan)\b|quadratic formula|discriminant|simultaneous|\bcone|\bsphere|imperial|\bmiles?\b", _txt(it))



def build():
    sets, R = build_sets([
        ("Gradient and y-intercept", [("collect", sgl.one_mc, 10), ("collect", ukl.one_mc, 10)]),
        ("Gradient", [("collect", sgl.one_grad, 10), ("collect", ukl.one_grad, 10)]),
        ("Equation from a graph", [("collect", sgl.one_from_graph, 10), ("collect", aug.one_from_graph, 10)]),
        ("Parallel lines", [("collect", sgl.one_parallel, 10), ("collect", ukl.one_parallel, 10)]),
        ("Interpret graphs", [("collect", zg7.uniq(zg7.one_global), 10), ("collect", aug.one_line_text, 10)]),
    ], 80910)
    finish(sets, R)
    body = lesson("<ul><li>In y = mx + c, m is the gradient and c is the y-intercept.</li><li>Gradient = <span class='fr'><span class='fn'>change in y</span><span class='fd'>change in x</span></span>.</li><li>The x-intercept is where y = 0; the y-intercept is where x = 0.</li><li>Parallel lines have the same gradient.</li></ul>",
        [example("Line through (1; 3) and (4; 9)", ["m = 6 ÷ 3 = 2", "3 = 2 + c"], "y = 2x + 1")],
        [['m or c?', 'c is where the line crosses the y-axis.'], ['Upside down', 'Change in y over change in x.'], ['Parallel means same c', 'Parallel means same m.']])
    faq = [('What does CAPS Grade 9 say about graphs?', 'Interpret and draw linear graphs, determine the gradient and intercepts, and find the equation of a straight line.'), ('What is the gradient of y = 5?', '0, a horizontal line.'), ('Where does y = 2x − 6 cut the x-axis?', 'At x = 3.'), ('What does a negative gradient mean?', 'The line goes down from left to right.')]
    make('linear-graphs', 10, 'Patterns, Functions and Algebra', 'Grade 9: 2.5 Graphs',
         'Analyse and interpret global graphs of problem situations; draw linear graphs from given equations; determine equations from given linear graphs; extend the focus on features of graphs to include x-intercept and y-intercept and the gradient of a line.',
         'Linear Graphs: Gradient, Intercepts and y = mx + c', 'Linear Graphs',
         'Free CAPS Grade 9 linear graphs worksheets: gradient, intercepts, y = mx + c, parallel lines and global graphs. 100 questions with memos.',
         'y = mx + c.', 'Parallel lines: same gradient.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
