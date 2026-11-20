# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): Numeric Patterns: Rules, Tables and Flow Diagrams (Grade 5: 2.1 Numeric patterns)
  python3 tools/gen_za_maths_g5_numeric_patterns.py
Number patterns with a constant difference or ratio, pattern rules, input and output tables and flow diagrams (US
Grade 5, BC Grade 5 and Ontario Grade 5 makers, and the flow diagram maker from the Grade 4 generator).
Wrong answers come from real mistakes: adding when the rule multiplies, using only the first two terms, and
applying the operations in a flow diagram in the wrong order.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_us_math_g5_patterns as usp
adopt(usp)
if isinstance(getattr(usp, 'R', None), random.Random): usp.R = random.Random(805120)
import gen_cabc_math_g5_patterns as cbp
adopt(cbp)
if isinstance(getattr(cbp, 'R', None), random.Random): cbp.R = random.Random(805121)
import gen_caon_math_g5_patterns as cap
adopt(cap)
if isinstance(getattr(cap, 'R', None), random.Random): cap.R = random.Random(805122)
import gen_za_maths_g4_numeric_patterns as zn4
adopt(zn4)
if isinstance(getattr(zn4, 'R', None), random.Random): zn4.R = random.Random(805123)
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
        ("Continue the pattern", [("run", usp.set_generate, ("rnd",), 20, six)]),
        ("Pattern rules", [("run", cbp.set_words_rules, ("rnd",), 10, six), ("run", cap.set_rules, ("rnd",), 10, six)]),
        ("Input and output tables", [("run", cbp.set_tables, ("rnd",), 10, six), ("run", cap.set_tables, ("rnd",), 10, six)]),
        ("Flow diagrams", [("collect", zn4.uniq(zn4.one_flow), 20)]),
        ("Pattern problems", [("run", cbp.set_predict, ("rnd",), 10, six), ("run", usp.set_words, ("rnd",), 10, six)]),
    ], 80512)
    finish(sets, R)
    body = lesson('<ul><li>A pattern can add or subtract the same number each time (constant difference): 7, 15, 23, 31 …</li><li>Or multiply by the same number each time (constant ratio): 3, 6, 12, 24 …</li><li>Check the rule with every pair of terms, not just the first two.</li><li>A flow diagram takes an input, does the operations in order, and gives the output.</li></ul>',
        [example("4, 12, 36, 108, …", ["each term × 3"], "324")],
        [['Adding instead of multiplying', 'Check the difference between more terms.'], ['First two terms only', 'Test the rule on all the terms.'], ['Wrong order', 'Follow the arrows.']])
    faq = [('What does CAPS Grade 5 say about numeric patterns?', "Investigate and extend numeric patterns with a constant difference or ratio, or of the learner's own creation, describe the rules, and use flow diagrams and tables."), ('What is a constant ratio?', 'Multiplying by the same number each time.'), ('What is a flow diagram?', 'A diagram with arrows that shows the input, the operations and the output.'), ('How do I find a missing input?', 'Work backwards with the inverse operations.')]
    make('numeric-patterns', 12, 'Patterns, Functions and Algebra', 'Grade 5: 2.1 Numeric patterns',
         "Investigate and extend numeric patterns looking for relationships or rules of patterns: sequences involving a constant difference or ratio, and of the learner's own creation; describe the general rules for the observed relationships; determine input values, output values and rules for the patterns and relationships using flow diagrams and tables.",
         'Numeric Patterns: Rules, Tables and Flow Diagrams', 'Numeric Patterns',
         'Free CAPS Grade 5 numeric patterns worksheets: constant difference and ratio, pattern rules, input and output tables and flow diagrams. 100 questions with memos.',
         'Find the rule and test it on every term.', 'Constant difference: + or −. Constant ratio: × or ÷.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
