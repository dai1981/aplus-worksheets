# -*- coding: utf-8 -*-
"""
South Africa Grade 9 Maths (CAPS): Numeric and Geometric Patterns: Linear and Geometric Sequences (Grade 9: 2.1 Numeric and geometric patterns)
  python3 tools/gen_za_maths_g9_patterns.py
Linear and geometric sequences, the general term, using the rule, and pattern problems (UK Year 9 and Singapore
Secondary 1 makers).
Wrong answers come from real mistakes: mixing up linear and geometric sequences, mixing up the term and its
position, and forgetting the constant.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y9_arithmetic_and_geometric_sequences as uks
adopt(uks)
if isinstance(getattr(uks, 'R', None), random.Random): uks.R = random.Random(809050)
import gen_sg_maths_s1_number_patterns as sgp
adopt(sgp)
if isinstance(getattr(sgp, 'R', None), random.Random): sgp.R = random.Random(809051)
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
        ("Linear or geometric?", [("collect", uks.one_type, 20)]),
        ("The general term", [("collect", uks.one_nth, 10), ("collect", sgp.one_find_nth, 10)]),
        ("Geometric sequences", [("collect", uks.one_geo, 10), ("collect", sgp.one_geo, 10)]),
        ("Use the rule", [("collect", uks.one_use, 10), ("collect", sgp.one_in, 10)]),
        ("Pattern problems", [("run", uks.problems, (), 10, ok9), ("run", sgp.problems, (), 10, ok9)]),
    ], 80905)
    finish(sets, R)
    body = lesson('<ul><li>A linear sequence has a constant difference: Tₙ = dn + c.</li><li>A geometric sequence has a constant ratio: 3, 6, 12, 24 … (× 2).</li><li>To find a far term, substitute n into the rule.</li><li>To check if a number is a term, solve for n.</li></ul>',
        [example("5, 8, 11, 14, …", ["d = 3", "Tₙ = 3n + 2"], "T₅₀ = 152")],
        [['Linear or geometric?', 'Check differences, then ratios.'], ['Term or position?', 'n is the position.'], ['The constant', '3n + 2, not 3n.']])
    faq = [('What does CAPS Grade 9 say about patterns?', 'Investigate and extend numeric and geometric patterns, describe the general rule in algebraic language, and find terms.'), ('What is a geometric sequence?', 'Each term is multiplied by the same number.'), ('What is Tₙ?', 'The term in position n.'), ('Can the ratio be a fraction?', 'Yes: 64, 32, 16 … has ratio ½.')]
    make('numeric-and-geometric-patterns', 5, 'Patterns, Functions and Algebra', 'Grade 9: 2.1 Numeric and geometric patterns',
         'Investigate and extend numeric and geometric patterns looking for relationships between numbers, including patterns represented in physical or diagram form, patterns not limited to sequences involving a constant difference or ratio, represented in tables or algebraically; describe and justify the general rules for observed relationships between numbers in own words or in algebraic language.',
         'Numeric and Geometric Patterns: Linear and Geometric Sequences', 'Numeric and Geometric Patterns',
         'Free CAPS Grade 9 patterns worksheets: linear and geometric sequences, the general term and pattern problems. 100 questions with memos.',
         'Linear: Tₙ = dn + c.', 'Geometric: multiply by the ratio.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
