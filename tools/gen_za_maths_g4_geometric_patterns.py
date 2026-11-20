# -*- coding: utf-8 -*-
"""
South Africa Grade 4 Maths (CAPS): Geometric Patterns: Growing Shape Patterns (Grade 4: 2.2 Geometric patterns)
  python3 tools/gen_za_maths_g4_geometric_patterns.py
Growing shape patterns made of squares, matches and dots, the next figure, the number of objects in a later figure,
and the rule (US Grade 4, BC Grade 4 and Ontario Grade 4 makers).
Wrong answers come from real mistakes: counting the objects in the figure before, multiplying the figure number by
the wrong amount, and forgetting the starting part.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_us_math_g4_patterns as usp
adopt(usp)
if hasattr(usp, 'R'): usp.R = random.Random(804130)
import gen_cabc_math_g4_patterns as cbp
adopt(cbp)
if hasattr(cbp, 'R'): cbp.R = random.Random(804131)
import gen_caon_math_g4_patterns as cap
adopt(cap)
if hasattr(cap, 'R'): cap.R = random.Random(804132)
za_common.GRADE = "grade-4"


import re as _re


def _nums(it):
    t = _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"]
    t = _re.sub(r"<[^>]+>", " ", t)
    return [int(x.replace(",", "").replace("\u00a0", "")) for x in _re.findall(r"(?<![\d.])\d[\d,\u00a0]*(?![.\d])", t) if x.replace(",", "").replace("\u00a0", "").isdigit()]


def le10000(it):
    return all(n <= 10000 for n in _nums(it))


def nodec(it):
    t = _re.sub(r"<[^>]+>", " ", it["q"] + " " + " ".join(it["c"]))
    return not _re.search(r"\d\.\d", t)



def build():
    sets, R = build_sets([
        ("Growing shape patterns", [("run", usp.set_shapes, ("rnd",), 20)]),
        ("Shape pattern rules", [("run", cbp.set_shapes, (), 20)]),
        ("Growing patterns", [("run", cap.set_growing, (), 14, nodec), ("run", usp.set_extend, ("rnd",), 6, le10000)]),
        ("Repeating and growing", [("run", cap.set_repeating, (), 10, nodec), ("run", cap.set_rules, (), 10, nodec)]),
        ("Pattern problems", [("run", cap.set_predict, (cap.People,), 10, nodec), ("run", usp.set_features, ("rnd", usp.People), 10)]),
    ], 80413)
    finish(sets, R)
    body = lesson('<ul><li>In a growing pattern, each figure adds the same number of objects.</li><li>Make a table: figure number and number of objects. Then find the rule.</li><li>Figure 1: 4 matches, figure 2: 7, figure 3: 10. Each figure adds 3 matches.</li><li>Use the rule to find a later figure without drawing them all.</li></ul>',
        [example("Squares: 3, 5, 7, … tiles", ["+ 2 each figure"], "figure 6 has 13 tiles")],
        [['The figure before', 'Count the figure the question asks for.'], ['Wrong multiplier', 'Use the number added each time.'], ['Forgetting the start', 'Add the starting part too.']])
    faq = [('What does CAPS Grade 4 say about geometric patterns?', 'Investigate and extend geometric patterns looking for relationships or rules, represented in physical or diagram form, and determine input and output values using tables.'), ('What is a geometric pattern?', 'A pattern of shapes or objects that changes by a rule.'), ('Why make a table?', 'It makes the rule easy to see.'), ('Can patterns shrink?', 'Yes, some patterns take away objects.')]
    make('geometric-patterns', 13, 'Patterns, Functions and Algebra', 'Grade 4: 2.2 Geometric patterns',
         'Investigate and extend geometric patterns looking for relationships or rules of patterns represented in physical or diagram form: sequences involving a constant difference or ratio; describe the general rules for the observed relationships; determine input values, output values and rules for the patterns and relationships using flow diagrams and tables.',
         'Geometric Patterns: Growing Shape Patterns', 'Geometric Patterns',
         'Free CAPS Grade 4 geometric patterns worksheets: growing shape patterns, the next figure, rules and pattern tables. 100 questions with memos.',
         'Find what each figure adds.', 'Make a table: figure number and number of objects.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
