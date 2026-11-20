# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Numeric Patterns: Rules, Tables and Flow Diagrams (Grade 6: 2.1 Numeric patterns)
  python3 tools/gen_za_maths_g6_numeric_patterns.py
Number patterns with a constant difference or ratio, pattern rules, terms far along a pattern, input and output
tables and flow diagrams (Australia Year 6, Ontario Grade 6 and BC Grade 6 makers, and the flow diagram maker from the
Grade 4 generator).
Wrong answers come from real mistakes: adding when the rule multiplies, counting the terms wrongly, and applying the
operations in a flow diagram in the wrong order.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y6_patterns as aup
adopt(aup)
if isinstance(getattr(aup, 'R', None), random.Random): aup.R = random.Random(806170)
import gen_caon_math_g6_patterns as cap
adopt(cap)
if isinstance(getattr(cap, 'R', None), random.Random): cap.R = random.Random(806171)
import gen_cabc_math_g6_patterns as cbp
adopt(cbp)
if isinstance(getattr(cbp, 'R', None), random.Random): cbp.R = random.Random(806172)
import gen_za_maths_g4_numeric_patterns as zn4
adopt(zn4)
if isinstance(getattr(zn4, 'R', None), random.Random): zn4.R = random.Random(806173)
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
        ("Continue the pattern", [("run", aup.set_continue, ("rnd",), 20, nine)]),
        ("Pattern rules", [("run", aup.set_rule, ("rnd",), 10, nine), ("run", cap.set_rule, ("rnd",), 10, nine)]),
        ("Input and output tables", [("run", cbp.set_tables, (), 10, nine), ("collect", zn4.uniq(zn4.one_flow), 10)]),
        ("Terms far along", [("run", aup.set_far, ("rnd",), 10, nine), ("run", cap.set_terms, ("rnd",), 10, nine)]),
        ("Pattern problems", [("run", aup.set_words, ("rnd", aup.People), 10, nine), ("run", cap.set_words, ("rnd",), 10, nine)]),
    ], 80617)
    finish(sets, R)
    body = lesson('<ul><li>A pattern can add or subtract the same number each time (constant difference): 12, 19, 26, 33 …</li><li>Or multiply or divide by the same number each time (constant ratio): 2, 6, 18, 54 …</li><li>A rule can use the term number: term = 7 × term number + 5.</li><li>Use the rule to find a term far along without listing them all.</li></ul>',
        [example("Rule: 7 × n + 5. Term 20?", ["7 × 20 = 140", "140 + 5"], "145")],
        [['Adding instead of multiplying', 'Check the differences.'], ['Counting terms wrongly', 'Term 1 is the first number.'], ['Wrong order', 'Follow the arrows in the flow diagram.']])
    faq = [('What does CAPS Grade 6 say about numeric patterns?', 'Investigate and extend numeric patterns with a constant difference or ratio, describe the rules in words and number sentences, and use flow diagrams and tables.'), ('What is a term?', 'One number in the pattern.'), ('How do I find term 100?', 'Use the rule with the term number.'), ('Can a pattern get smaller?', 'Yes, when it subtracts or divides.')]
    make('numeric-patterns', 17, 'Patterns, Functions and Algebra', 'Grade 6: 2.1 Numeric patterns',
         "Investigate and extend numeric patterns looking for relationships or rules of patterns: sequences involving a constant difference or ratio, and of the learner's own creation; describe the general rules for the observed relationships; determine input values, output values and rules for the patterns and relationships using flow diagrams, tables and number sentences.",
         'Numeric Patterns: Rules, Tables and Flow Diagrams', 'Numeric Patterns',
         'Free CAPS Grade 6 numeric patterns worksheets: constant difference and ratio, pattern rules, terms far along, tables and flow diagrams. 100 questions with memos.',
         'Find the rule, then use the term number.', 'Constant difference: + or −. Constant ratio: × or ÷.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
