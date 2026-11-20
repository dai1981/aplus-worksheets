# -*- coding: utf-8 -*-
"""
South Africa Grade 8 Maths (CAPS): Numeric and Geometric Patterns: General Rules and the nth Term (Grade 8: 2.1 Numeric and geometric patterns)
  python3 tools/gen_za_maths_g8_patterns.py
Continuing sequences, constant ratio sequences, finding and using the general rule, checking whether a number is in a
pattern (Singapore Secondary 1 and UK Year 7 makers) and pattern tables (BC Grade 7 maker).
Wrong answers come from real mistakes: using only the first difference, mixing up the term and its position, and
forgetting the constant in the rule.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_sg_maths_s1_number_patterns as sgp
adopt(sgp)
if isinstance(getattr(sgp, 'R', None), random.Random): sgp.R = random.Random(808080)
import gen_uk_maths_y7_sequences as uks
adopt(uks)
if isinstance(getattr(uks, 'R', None), random.Random): uks.R = random.Random(808081)
import gen_cabc_math_g7_linear_relations as cbl
adopt(cbl)
if isinstance(getattr(cbl, 'R', None), random.Random): cbl.R = random.Random(808082)
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
        ("Continue the pattern", [("collect", sgp.one_next, 20)]),
        ("Constant ratio", [("collect", sgp.one_geo, 10), ("collect", uks.one_geo, 8), ("collect", uks.one_next, 2)]),
        ("The general rule", [("collect", sgp.one_find_nth, 20)]),
        ("Use the rule", [("collect", sgp.one_use, 10), ("collect", sgp.one_in, 10)]),
        ("Pattern tables and problems", [("run", cbl.set_tables, (), 10, ok8), ("run", sgp.problems, (), 10, ok8)]),
    ], 80808)
    finish(sets, R)
    body = lesson('<ul><li>A linear pattern adds the same number each time: Tₙ = 3n + 4 gives 7, 10, 13 …</li><li>A pattern with a constant ratio multiplies by the same number each time.</li><li>To find the rule of a linear pattern: the difference is the coefficient of n; then find the constant.</li><li>To check if a number is a term, solve the rule for n: n must be a whole number.</li></ul>',
        [example("−3, 1, 5, 9, …", ["difference 4", "4n − 7"], "T₂₀ = 73")],
        [['One difference only', 'Check all the differences.'], ['Term or position?', 'n is the position.'], ['Forgetting the constant', '4n − 7, not 4n.']])
    faq = [('What does CAPS Grade 8 say about patterns?', 'Investigate and extend numeric and geometric patterns, describe the general rules in words and algebraic language, and find terms.'), ('What does Tₙ mean?', 'The term in position n.'), ('Is 50 in 4n − 7?', 'No: 4n = 57 gives n = 14,25.'), ('Can a rule use n²?', 'Yes, for some patterns.')]
    make('numeric-and-geometric-patterns', 8, 'Patterns, Functions and Algebra', 'Grade 8: 2.1 Numeric and geometric patterns',
         "Investigate and extend numeric and geometric patterns looking for relationships between numbers, including patterns represented in physical or diagram form, patterns not limited to sequences involving a constant difference or ratio, of learners' own creation, and represented in tables or algebraically; describe and justify the general rules for observed relationships between numbers in own words or in algebraic language.",
         'Numeric and Geometric Patterns: General Rules and the nth Term', 'Numeric and Geometric Patterns',
         'Free CAPS Grade 8 patterns worksheets: continuing sequences, constant ratio, the general rule, Tₙ and pattern problems. 100 questions with memos.',
         'Tₙ = difference × n + constant.', 'Check the rule on every term.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
