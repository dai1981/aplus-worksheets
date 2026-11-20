# -*- coding: utf-8 -*-
"""
South Africa Grade 8 Maths (CAPS): Functions and Relationships: Flow Diagrams, Tables, Formulae and Equations (Grade 8: 2.2 Functions and relationships)
  python3 tools/gen_za_maths_g8_functions.py
Flow diagrams (maker from the Grade 4 generator), tables of values, finding rules, and equations of straight lines
from tables (UK Year 7, Australia Year 8 and BC Grade 7 makers).
Wrong answers come from real mistakes: doing the operations in the wrong order, using one pair of values to find a
rule, and substituting negative inputs carelessly.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_za_maths_g4_numeric_patterns as zn4
adopt(zn4)
if isinstance(getattr(zn4, 'R', None), random.Random): zn4.R = random.Random(808090)
import gen_uk_maths_y7_coordinates_and_straight_line_graphs as ukc
adopt(ukc)
if isinstance(getattr(ukc, 'R', None), random.Random): ukc.R = random.Random(808091)
import gen_au_maths_y8_graphing_linear_relations as aug
adopt(aug)
if isinstance(getattr(aug, 'R', None), random.Random): aug.R = random.Random(808092)
import gen_cabc_math_g7_linear_relations as cbl
adopt(cbl)
if isinstance(getattr(cbl, 'R', None), random.Random): cbl.R = random.Random(808093)
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
        ("Flow diagrams", [("collect", zn4.uniq(zn4.one_flow), 20)]),
        ("Tables of values", [("collect", ukc.one_table, 10), ("collect", aug.one_table, 10)]),
        ("Find the rule", [("run", cbl.set_expressions, (), 10, ok8), ("run", cbl.set_evaluate, (), 10, ok8)]),
        ("Points on the line", [("collect", ukc.one_onl, 10), ("collect", aug.one_onl, 10)]),
        ("Relationship problems", [("run", cbl.set_words, (), 7, ok8), ("run", aug.problems, (), 13, ok8)]),
    ], 80809)
    finish(sets, R)
    body = lesson('<ul><li>A function gives one output (y) for each input (x).</li><li>Substitute each x into the rule to fill a table: y = −2x + 3, x = −1 gives y = 5.</li><li>To find the rule from a table: the change in y for each step of 1 in x is the coefficient of x.</li><li>A point lies on the line if its coordinates make the equation true.</li></ul>',
        [example("x: 0, 1, 2, 3 and y: 4, 7, 10, 13", ["y goes up by 3", "y = 4 when x = 0"], "y = 3x + 4")],
        [['Wrong order', 'Follow the arrows.'], ['One pair only', 'Test the rule on every pair.'], ['Negative inputs', '−2 × (−1) = +2.']])
    faq = [('What does CAPS Grade 8 say about functions?', 'Determine input values, output values or rules using flow diagrams, tables, formulae and equations, and show equivalence of different descriptions of the same relationship.'), ('Is (2; 7) on y = 3x + 1?', 'Yes: 3 × 2 + 1 = 7.'), ('What is an output?', 'The value you get from the rule.'), ('Can a table and a graph show the same rule?', 'Yes.')]
    make('functions-and-relationships', 9, 'Patterns, Functions and Algebra', 'Grade 8: 2.2 Functions and relationships',
         'Determine input values, output values or rules for patterns and relationships using flow diagrams, tables, formulae and equations; determine, interpret and justify equivalence of different descriptions of the same relationship or rule presented verbally, in flow diagrams, in tables, by formulae, by equations and by graphs on a Cartesian plane.',
         'Functions and Relationships: Flow Diagrams, Tables, Formulae and Equations', 'Functions and Relationships',
         'Free CAPS Grade 8 functions worksheets: flow diagrams, tables of values, finding rules and points on a line. 100 questions with memos.',
         'One input, one output.', 'Test the rule on every pair.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
