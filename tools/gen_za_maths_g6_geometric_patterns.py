# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Geometric Patterns: Shape Patterns, Tables and Rules (Grade 6: 2.2 Geometric patterns)
  python3 tools/gen_za_maths_g6_geometric_patterns.py
Growing shape patterns, tables of figure numbers, rules and later figures (Australia Year 6, Ontario Grade 5 and
Grade 6 and US Grade 4 makers).
Wrong answers come from real mistakes: counting the figure before, multiplying the figure number without the
starting part, and continuing the pattern by the wrong amount.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y6_patterns as aup
adopt(aup)
if isinstance(getattr(aup, 'R', None), random.Random): aup.R = random.Random(806180)
import gen_caon_math_g5_patterns as ca5
adopt(ca5)
if isinstance(getattr(ca5, 'R', None), random.Random): ca5.R = random.Random(806181)
import gen_caon_math_g6_patterns as cap
adopt(cap)
if isinstance(getattr(cap, 'R', None), random.Random): cap.R = random.Random(806182)
import gen_us_math_g4_patterns as us4
adopt(us4)
if isinstance(getattr(us4, 'R', None), random.Random): us4.R = random.Random(806183)
import gen_cabc_math_g6_patterns as cbp
adopt(cbp)
if isinstance(getattr(cbp, 'R', None), random.Random): cbp.R = random.Random(806184)
za_common.GRADE = "grade-6"


import re as _re


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def _nums(it):
    return [int(x.replace(",", "").replace("\u00a0", "")) for x in _re.findall(r"(?<![\d.])\d[\d,\u00a0]*(?![.\d])", _txt(it)) if x.replace(",", "").replace("\u00a0", "").isdigit()]


def noneg(it):
    return not _re.search(r"(?<![\d)] )[−-]\d", _txt(it)) and "negative" not in _txt(it).lower()


def nine(it):
    """whole numbers to 9 digits, no negatives"""
    return all(n <= 999999999 for n in _nums(it)) and noneg(it)


def dec3(it):
    """decimals with at most 3 places, no negatives"""
    return noneg(it) and not _re.search(r"\d\.\d{4}", _txt(it))


def nodec(it):
    return noneg(it) and not _re.search(r"\d\.\d", _txt(it))


def flat(it):
    """first quadrant only: no negative numbers in the text or the picture"""
    return nodec(it) and "−" not in it["q"] and "-1" not in it["q"]


def nomean(it):
    return dec3(it) and not _re.search(r"\bmean\b", _txt(it))


def den12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " " + it["c"][it["a"]])]
    return all(d <= 12 or d in (20, 25, 50, 100) for d in ds) and nodec(it)



def build():
    sets, R = build_sets([
        ("Growing shape patterns", [("run", aup.set_growing, ("rnd",), 20, nine)]),
        ("Shape patterns", [("run", us4.set_shapes, ("rnd",), 20, nine)]),
        ("Tables of figures", [("run", ca5.set_tables, ("rnd",), 10, nine), ("run", cbp.set_expressions, (), 10, nine)]),
        ("Rules with figure numbers", [("run", cap.set_patterns, ("rnd",), 10, nine), ("run", cap.set_evaluate, ("rnd",), 10, nine)]),
        ("Pattern problems", [("run", ca5.set_grow, ("rnd",), 16, nine), ("run", cbp.set_words, (), 4, nine)]),
    ], 80618)
    finish(sets, R)
    body = lesson('<ul><li>In a growing shape pattern, each figure adds the same number of objects.</li><li>Make a table: figure number and number of objects.</li><li>Find the rule: figure 1 has 6 tiles, figure 2 has 10, figure 3 has 14. Rule: 4 × figure number + 2.</li><li>Use the rule to find any figure: figure 25 has 4 × 25 + 2 = 102 tiles.</li></ul>',
        [example("Matches: 5, 9, 13, …", ["+ 4 each figure", "rule: 4 × n + 1"], "figure 30 has 121 matches")],
        [['The figure before', 'Use the figure number in the question.'], ['Forgetting the start', '4 × n + 1, not just 4 × n.'], ['Wrong step', 'Find what is added each time.']])
    faq = [('What does CAPS Grade 6 say about geometric patterns?', 'Investigate and extend geometric patterns represented in physical or diagram form, describe the rules, and use flow diagrams, tables and number sentences.'), ('Why use a rule?', 'To find any figure without drawing them all.'), ('What does n stand for?', 'The figure number.'), ('Can I check my rule?', 'Yes, test it on the first figures.')]
    make('geometric-patterns', 18, 'Patterns, Functions and Algebra', 'Grade 6: 2.2 Geometric patterns',
         "Investigate and extend geometric patterns looking for relationships or rules of patterns represented in physical or diagram form: sequences involving a constant difference or ratio, and of the learner's own creation; describe the general rules for the observed relationships; determine input values, output values and rules for the patterns and relationships using flow diagrams, tables and number sentences.",
         'Geometric Patterns: Shape Patterns, Tables and Rules', 'Geometric Patterns',
         'Free CAPS Grade 6 geometric patterns worksheets: growing shape patterns, tables, rules and later figures. 100 questions with memos.',
         'Figure number → rule → number of objects.', 'Test the rule on the first figures.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
