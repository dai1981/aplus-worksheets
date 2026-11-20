# -*- coding: utf-8 -*-
"""
South Africa Grade 9 Maths (CAPS): Functions and Relationships: Tables, Formulae, Direct and Inverse Proportion (Grade 9: 2.2 Functions and relationships)
  python3 tools/gen_za_maths_g9_functions.py
Flow diagrams (maker from the Grade 4 generator), tables of values and points on a line (UK Year 7 and Australia Year 8
makers), and direct and inverse proportion (Singapore Secondary 2 makers).
Wrong answers come from real mistakes: using one pair of values to find a rule, substituting negatives carelessly, and
treating an inverse proportion as direct.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_za_maths_g4_numeric_patterns as zn4
adopt(zn4)
if isinstance(getattr(zn4, 'R', None), random.Random): zn4.R = random.Random(809060)
import gen_uk_maths_y7_coordinates_and_straight_line_graphs as ukc
adopt(ukc)
if isinstance(getattr(ukc, 'R', None), random.Random): ukc.R = random.Random(809061)
import gen_au_maths_y8_graphing_linear_relations as aug
adopt(aug)
if isinstance(getattr(aug, 'R', None), random.Random): aug.R = random.Random(809062)
import gen_sg_maths_s2_direct_and_inverse_proportion as sgd
adopt(sgd)
if isinstance(getattr(sgd, 'R', None), random.Random): sgd.R = random.Random(809063)
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
        ("Flow diagrams", [("collect", zn4.uniq(zn4.one_flow), 20)]),
        ("Tables of values", [("collect", ukc.one_table, 10), ("collect", aug.one_table, 10)]),
        ("Points on the line", [("collect", ukc.one_onl, 10), ("collect", aug.one_onl, 10)]),
        ("Direct and inverse proportion", [("collect", sgd.one_which, 10), ("collect", sgd.one_inverse, 10)]),
        ("Proportion formulae", [("collect", sgd.one_formula, 20)]),
    ], 80906)
    finish(sets, R)
    body = lesson("<ul><li>A function gives one output for each input.</li><li>Substitute the input into the formula to find the output.</li><li>Direct proportion: y = kx (the ratio y ÷ x stays the same).</li><li>Inverse proportion: y = <span class='fr'><span class='fn'>k</span><span class='fd'>x</span></span> (the product xy stays the same).</li></ul>",
        [example("y is inversely proportional to x; y = 6 when x = 4", ["k = 24"], "y = 3 when x = 8")],
        [['One pair only', 'Test the rule on every pair.'], ['Negatives', '−3 × (−2) = 6.'], ['Inverse as direct', 'More workers: less time.']])
    faq = [('What does CAPS Grade 9 say about functions?', 'Determine input values, output values or rules using flow diagrams, tables, formulae and equations, including direct and inverse proportion.'), ('What is k?', 'The constant of proportion.'), ('Is y = 2x + 1 direct proportion?', 'No, the graph does not pass through the origin.'), ('What does an inverse proportion graph look like?', 'A curve that gets closer to the axes.')]
    make('functions-and-relationships', 6, 'Patterns, Functions and Algebra', 'Grade 9: 2.2 Functions and relationships',
         'Determine input values, output values or rules for patterns and relationships using flow diagrams, tables, formulae and equations; determine, interpret and justify equivalence of different descriptions of the same relationship or rule; describe direct and inverse proportion.',
         'Functions and Relationships: Tables, Formulae, Direct and Inverse Proportion', 'Functions and Relationships',
         'Free CAPS Grade 9 functions worksheets: flow diagrams, tables of values, points on a line and direct and inverse proportion. 100 questions with memos.',
         'Direct: y = kx. Inverse: xy = k.', 'Test the rule on every pair.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
