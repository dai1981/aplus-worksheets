# -*- coding: utf-8 -*-
"""
South Africa Grade 7 Maths (CAPS): Functions and Relationships: Flow Diagrams, Tables and Formulae (Grade 7: 2.2 Functions and relationships)
  python3 tools/gen_za_maths_g7_functions.py
Input and output values in flow diagrams (maker from the Grade 4 generator), tables of values and formulae, and
evaluating rules (BC Grade 7, Ontario Grade 7 and UK Year 7 makers).
Wrong answers come from real mistakes: doing the operations in the wrong order, working backwards with the same
operations, and using only one pair of values to find a rule.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_za_maths_g4_numeric_patterns as zn4
adopt(zn4)
if isinstance(getattr(zn4, 'R', None), random.Random): zn4.R = random.Random(807140)
import gen_cabc_math_g7_linear_relations as cbl
adopt(cbl)
if isinstance(getattr(cbl, 'R', None), random.Random): cbl.R = random.Random(807141)
import gen_caon_math_g7_patterns as cap
adopt(cap)
if isinstance(getattr(cap, 'R', None), random.Random): cap.R = random.Random(807142)
import gen_uk_maths_y7_coordinates_and_straight_line_graphs as ukc
adopt(ukc)
if isinstance(getattr(ukc, 'R', None), random.Random): ukc.R = random.Random(807143)
za_common.GRADE = "grade-7"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok7(it):
    """Grade 7: no circles, pi or standard form (they come in Grade 8 and 9)"""
    return not _re.search(r"π|\bpi\b|circumference|radius|diameter|×\s?10<sup>|standard form|scientific notation", _txt(it))


def noneg(it):
    return ok7(it) and not _re.search(r"(?<![\d)] )[−-]\d", _txt(it))



def build():
    sets, R = build_sets([
        ("Flow diagrams", [("collect", zn4.uniq(zn4.one_flow), 20)]),
        ("Tables of values", [("run", cbl.set_tables, (), 10, ok7), ("collect", ukc.one_table, 10)]),
        ("Find the rule", [("run", cap.set_rule, (), 10, ok7), ("run", cbl.set_expressions, (), 10, ok7)]),
        ("Evaluate the rule", [("run", cbl.set_evaluate, (), 20, ok7)]),
        ("Relationship problems", [("run", cbl.set_words, (), 7, ok7), ("run", cap.set_rate, (), 13, ok7)]),
    ], 80714)
    finish(sets, R)
    body = lesson('<ul><li>A function gives exactly one output for each input.</li><li>In a flow diagram, do the operations in order: input 6 → × 3 → + 4 → output 22.</li><li>To find an input, work backwards with the inverse operations.</li><li>A rule like y = 3x + 4 describes every pair in the table.</li></ul>',
        [example("y = 2x − 5, x = 9", ["2 × 9 = 18", "18 − 5"], "y = 13")],
        [['Wrong order', 'Follow the arrows.'], ['Same operations backwards', 'Use the inverse operations.'], ['One pair only', 'Test the rule on every pair.']])
    faq = [('What does CAPS Grade 7 say about functions?', 'Determine input values, output values or rules for patterns and relationships using flow diagrams, tables and formulae.'), ('What is an input?', 'The number you put into the rule.'), ('What is a formula?', 'A rule written with letters, like y = 3x + 4.'), ('How do I find the rule from a table?', 'Look at how the output changes when the input goes up by 1.')]
    make('functions-and-relationships', 14, 'Patterns, Functions and Algebra', 'Grade 7: 2.2 Functions and relationships',
         'Determine input values, output values or rules for patterns and relationships using flow diagrams, tables and formulae; determine, interpret and justify equivalence of different descriptions of the same relationship or rule presented verbally, in flow diagrams, in tables, by formulae and by number sentences.',
         'Functions and Relationships: Flow Diagrams, Tables and Formulae', 'Functions and Relationships',
         'Free CAPS Grade 7 functions worksheets: flow diagrams, input and output values, tables, formulae and rules. 100 questions with memos.',
         'One input, one output.', 'Work backwards with inverse operations.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
