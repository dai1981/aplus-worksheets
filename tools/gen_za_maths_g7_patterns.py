# -*- coding: utf-8 -*-
"""
South Africa Grade 7 Maths (CAPS): Numeric and Geometric Patterns: Sequences, Rules and the nth Term (Grade 7: 2.1 Numeric and geometric patterns)
  python3 tools/gen_za_maths_g7_patterns.py
Continuing number sequences, geometric sequences, finding and using the rule for the term number, checking whether a
number is in a pattern, and pattern tables (UK Year 7 makers and Ontario Grade 7 maker).
Wrong answers come from real mistakes: using only the first difference, mixing up the term and the term number, and
forgetting the constant in the rule.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y7_sequences as uks
adopt(uks)
if isinstance(getattr(uks, 'R', None), random.Random): uks.R = random.Random(807130)
import gen_caon_math_g7_patterns as cap
adopt(cap)
if isinstance(getattr(cap, 'R', None), random.Random): cap.R = random.Random(807131)
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
        ("Continue the sequence", [("collect", uks.one_next, 20)]),
        ("Constant ratio", [("collect", uks.one_geo, 18), ("collect", uks.one_next, 2)]),
        ("Find the rule", [("collect", uks.one_find_nth, 20)]),
        ("Use the rule", [("collect", uks.one_use, 10), ("collect", uks.one_in, 10)]),
        ("Pattern tables and problems", [("run", cap.set_tables, (), 10, ok7), ("run", cap.set_words, (), 10, ok7)]),
    ], 80713)
    finish(sets, R)
    body = lesson('<ul><li>A pattern with a constant difference: 5, 9, 13, 17 … (+ 4).</li><li>A pattern with a constant ratio: 3, 6, 12, 24 … (× 2).</li><li>The rule links the term to the term number n: 4n + 1 gives 5, 9, 13 …</li><li>To check if a number is in the pattern, solve the rule for n: it must be a whole number.</li></ul>',
        [example("7, 12, 17, 22, …", ["difference 5", "5n + 2"], "term 50 = 252")],
        [['One difference only', 'Check all the differences.'], ['Term or term number?', 'n is the position.'], ['Forgetting the constant', '5n + 2, not 5n.']])
    faq = [('What does CAPS Grade 7 say about patterns?', 'Investigate and extend numeric and geometric patterns, describe the rules in words and algebraic language, and find terms using the rule.'), ('What is the nth term?', 'A rule for any term using its position n.'), ('Is 100 in 3n + 1?', 'Yes: 3 × 33 + 1 = 100.'), ('Can a pattern decrease?', 'Yes, if the difference is negative.')]
    make('numeric-and-geometric-patterns', 13, 'Patterns, Functions and Algebra', 'Grade 7: 2.1 Numeric and geometric patterns',
         "Investigate and extend numeric and geometric patterns looking for relationships between numbers, including patterns represented in physical or diagram form, not limited to sequences involving a constant difference or ratio, of learners' own creation, and represented in tables; describe and justify the general rules for observed relationships between numbers in own words.",
         'Numeric and Geometric Patterns: Sequences, Rules and the nth Term', 'Numeric and Geometric Patterns',
         'Free CAPS Grade 7 patterns worksheets: number sequences, constant difference and ratio, the rule for the nth term and pattern tables. 100 questions with memos.',
         'Rule: term = difference × n + constant.', 'Check the rule on every term.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
