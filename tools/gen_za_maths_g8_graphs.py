# -*- coding: utf-8 -*-
"""
South Africa Grade 8 Maths (CAPS): Graphs: Global Graphs and Straight-Line Graphs (Grade 8: 2.5 Graphs)
  python3 tools/gen_za_maths_g8_graphs.py
Interpreting global graphs and fare graphs (makers from the Grade 7 generator), distance-time graphs (UK Year 9 maker)
and straight-line graphs: gradient and y-intercept (UK Year 8 and Australia Year 8 makers).
Wrong answers come from real mistakes: reading the wrong axis, mixing up the gradient and the y-intercept, and
counting the gradient the wrong way.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_za_maths_g7_graphs as zg7
adopt(zg7)
if isinstance(getattr(zg7, 'R', None), random.Random): zg7.R = random.Random(808120)
import gen_uk_maths_y9_real_life_graphs as ukg
adopt(ukg)
if isinstance(getattr(ukg, 'R', None), random.Random): ukg.R = random.Random(808121)
import gen_uk_maths_y8_linear_graphs as ukl
adopt(ukl)
if isinstance(getattr(ukl, 'R', None), random.Random): ukl.R = random.Random(808122)
import gen_au_maths_y8_graphing_linear_relations as aug
adopt(aug)
if isinstance(getattr(aug, 'R', None), random.Random): aug.R = random.Random(808123)
za_common.GRADE = "grade-8"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok8(it):
    """Grade 8: no trigonometry, quadratic formula or surds beyond square roots"""
    return not _re.search(r"\b(sin|cos|tan)\b|quadratic|discriminant|imperial|\bmiles?\b", _txt(it))



def build():
    sets, R = build_sets([
        ("Global graphs", [("collect", zg7.uniq(zg7.one_global), 20)]),
        ("Distance-time graphs", [("collect", ukg.one_dt, 10), ("collect", zg7.uniq(zg7.one_fare), 10)]),
        ("Gradient and y-intercept", [("collect", ukl.one_mc, 10), ("collect", aug.one_mc, 10)]),
        ("Gradient from a graph", [("collect", ukl.one_grad, 10), ("collect", ukl.one_from_graph, 10)]),
        ("Lines and their equations", [("collect", aug.one_from_graph, 10), ("collect", aug.one_line_text, 10)]),
    ], 80812)
    finish(sets, R)
    body = lesson('<ul><li>Read the axes and the scale first.</li><li>A global graph shows trends: increasing, decreasing, constant, maximum and minimum.</li><li>In y = mx + c, m is the gradient (steepness) and c is the y-intercept.</li><li>Gradient = change in y ÷ change in x.</li></ul>',
        [example("A line through (0; 2) and (3; 8)", ["gradient (8 − 2) ÷ 3 = 2", "y-intercept 2"], "y = 2x + 2")],
        [['The wrong axis', 'Read the labels first.'], ['m or c?', 'c is where the line crosses the y-axis.'], ['Upside down', 'Change in y over change in x.']])
    faq = [('What does CAPS Grade 8 say about graphs?', 'Analyse and interpret global graphs, draw global graphs, and plot points on the Cartesian plane to draw straight-line graphs.'), ('What does a negative gradient show?', 'The line goes down from left to right.'), ('What is the y-intercept of y = 4x − 3?', '−3.'), ('What is a global graph?', 'A graph that shows the overall trend of a situation.')]
    make('graphs', 12, 'Patterns, Functions and Algebra', 'Grade 8: 2.5 Graphs',
         'Analyse and interpret global graphs of problem situations, with special focus on trends and features: linear or non-linear, constant, increasing or decreasing, maximum or minimum, discrete or continuous; draw global graphs from given descriptions; use tables of ordered pairs to plot points and draw graphs on the Cartesian plane.',
         'Graphs: Global Graphs and Straight-Line Graphs', 'Graphs',
         'Free CAPS Grade 8 graphs worksheets: global graphs, distance-time graphs, gradient, y-intercept and straight-line equations. 100 questions with memos.',
         'y = mx + c: m is the gradient, c the y-intercept.', 'Read the axes first.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
