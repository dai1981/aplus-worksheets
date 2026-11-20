# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): Geometric Patterns: Shape Patterns, Tables and Rules (Grade 5: 2.2 Geometric patterns)
  python3 tools/gen_za_maths_g5_geometric_patterns.py
Growing shape patterns, symbol patterns, the number of objects in a later figure and the rule (Ontario Grade 5 and
BC Grade 5 makers).
Wrong answers come from real mistakes: counting the figure before, multiplying the figure number without the
starting part, and continuing the pattern by the wrong amount.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_caon_math_g5_patterns as cap
adopt(cap)
if isinstance(getattr(cap, 'R', None), random.Random): cap.R = random.Random(805130)
import gen_cabc_math_g5_patterns as cbp
adopt(cbp)
if isinstance(getattr(cbp, 'R', None), random.Random): cbp.R = random.Random(805131)
import gen_us_math_g5_patterns as usp
adopt(usp)
if isinstance(getattr(usp, 'R', None), random.Random): usp.R = random.Random(805132)
import gen_us_math_g4_patterns as us4
adopt(us4)
if isinstance(getattr(us4, 'R', None), random.Random): us4.R = random.Random(805133)
za_common.GRADE = "grade-5"


import re as _re


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def _nums(it):
    return [int(x.replace(",", "").replace("\u00a0", "")) for x in _re.findall(r"(?<![\d.])\d[\d,\u00a0]*(?![.\d])", _txt(it)) if x.replace(",", "").replace("\u00a0", "").isdigit()]


def six(it):
    """whole numbers to 6 digits, no decimals, no negatives"""
    t = _txt(it)
    return all(n <= 999999 for n in _nums(it)) and not _re.search(r"\d\.\d|−\d", t)


def nodec(it):
    return not _re.search(r"\d\.\d|−\d", _txt(it))


def den12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " " + it["c"][it["a"]])]
    return all(d <= 12 for d in ds) and nodec(it)



def build():
    sets, R = build_sets([
        ("Growing patterns", [("run", cap.set_grow, ("rnd",), 20, six)]),
        ("Patterns with symbols", [("run", cbp.set_symbols, ("rnd",), 20, six)]),
        ("Patterns with letters", [("run", cbp.set_variables, ("rnd",), 20, six)]),
        ("Two patterns", [("run", usp.set_relationship, ("rnd",), 10, six), ("run", usp.set_pairs, ("rnd",), 10, six)]),
        ("Pattern problems", [("run", cap.set_words, ("rnd",), 7, six), ("run", us4.set_shapes, ("rnd",), 13, six)]),
    ], 80513)
    finish(sets, R)
    body = lesson('<ul><li>In a growing shape pattern, each figure adds the same number of objects.</li><li>Make a table of the figure number and the number of objects.</li><li>Find the rule: figure 1 has 5, figure 2 has 8, figure 3 has 11. The rule is figure number × 3 + 2.</li><li>Use the rule to find figure 20 without drawing it: 20 × 3 + 2 = 62.</li></ul>',
        [example("Matches: 4, 7, 10, …", ["+ 3 each figure", "rule: × 3 + 1"], "figure 10 has 31 matches")],
        [['The figure before', 'Use the figure number in the question.'], ['Forgetting the start', '× 3 + 1, not just × 3.'], ['Wrong step', 'Find what is added each time.']])
    faq = [('What does CAPS Grade 5 say about geometric patterns?', 'Investigate and extend geometric patterns represented in physical or diagram form, with a constant difference or ratio, describe the rules, and use flow diagrams and tables.'), ('Why find a rule?', 'So you can find any figure without drawing them all.'), ('Can a pattern use letters?', 'Yes, n can stand for the figure number.'), ('What is a constant difference?', 'The same number added each time.')]
    make('geometric-patterns', 13, 'Patterns, Functions and Algebra', 'Grade 5: 2.2 Geometric patterns',
         "Investigate and extend geometric patterns looking for relationships or rules of patterns represented in physical or diagram form: sequences involving a constant difference or ratio, and of the learner's own creation; describe the general rules for the observed relationships; determine input values, output values and rules for the patterns and relationships using flow diagrams and tables.",
         'Geometric Patterns: Shape Patterns, Tables and Rules', 'Geometric Patterns',
         'Free CAPS Grade 5 geometric patterns worksheets: growing shape patterns, pattern tables, rules and later figures. 100 questions with memos.',
         'Figure number → rule → number of objects.', 'Test the rule on the first figures.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
