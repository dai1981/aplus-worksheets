# -*- coding: utf-8 -*-
"""
South Africa Grade 10 Maths (CAPS): Number Patterns: Linear Sequences and the General Term (Grade 10: Number patterns)
  python3 tools/gen_za_maths_g10_number_patterns.py
Linear or geometric sequences, the general term Tₙ, finding terms and positions, and pattern problems (US Algebra 1,
UK Year 9 and Singapore Secondary 1 makers).
Wrong answers come from real mistakes: using only the first difference, mixing up n and Tₙ, and forgetting the
constant term.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_us_math_a1_arithmetic_and_geometric_sequences as uss
adopt(uss)
if isinstance(getattr(uss, 'R', None), random.Random): uss.R = random.Random(810050)
import gen_uk_maths_y9_arithmetic_and_geometric_sequences as uks
adopt(uks)
if isinstance(getattr(uks, 'R', None), random.Random): uks.R = random.Random(810051)
import gen_sg_maths_s1_number_patterns as sgp
adopt(sgp)
if isinstance(getattr(sgp, 'R', None), random.Random): sgp.R = random.Random(810052)
za_common.GRADE = "grade-10"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok10(it):
    """Grade 10: no complex numbers, logarithms, radians, sine or cosine rules, or calculus"""
    return not _re.search(r"imaginary|complex|\blog|radian|\bπ/|sine rule|cosine rule|law of (sines|cosines)|derivative|imperial|\bmiles?\b|\bfeet\b|\binch", _txt(it))



def build():
    sets, R = build_sets([
        ("Linear or not?", [("collect", uss.one_type, 10), ("collect", uks.one_type, 10)]),
        ("The general term", [("collect", uss.one_nth, 10), ("collect", uks.one_nth, 10)]),
        ("Find a term", [("collect", uks.one_use, 10), ("collect", sgp.one_use, 10)]),
        ("Which term?", [("collect", sgp.one_in, 10), ("collect", sgp.one_find_nth, 10)]),
        ("Pattern problems", [("run", uss.problems, (), 10, ok10), ("collect", sgp.one_next, 10)]),
    ], 81005)
    finish(sets, R)
    body = lesson('<ul><li>A linear sequence has a constant first difference d.</li><li>General term: Tₙ = dn + c, or Tₙ = a + (n − 1)d.</li><li>To find a term, substitute n. To find a position, solve Tₙ = value for n.</li><li>n must be a natural number.</li></ul>',
        [example("4; 11; 18; 25; …", ["d = 7", "Tₙ = 7n − 3"], "T₄₀ = 277")],
        [['One difference only', 'Check all the differences.'], ['n or Tₙ?', 'n is the position; Tₙ the value.'], ['The constant', '7n − 3, not 7n.']])
    faq = [('What does CAPS Grade 10 say about number patterns?', 'Investigate number patterns leading to those where there is a constant difference between consecutive terms, and the general term is therefore linear.'), ('Is 100 a term of Tₙ = 3n + 2?', 'No: n = 32,67 is not a whole number.'), ('What is d?', 'The common difference.'), ('Can d be negative?', 'Yes, the sequence then decreases.')]
    make('number-patterns', 5, 'Algebra and Number Patterns', 'Grade 10: Number patterns',
         'Investigate number patterns leading to those where there is a constant difference between consecutive terms, and the general term is therefore linear.',
         'Number Patterns: Linear Sequences and the General Term', 'Number Patterns',
         'Free CAPS Grade 10 number patterns worksheets: linear sequences, the general term, finding terms and positions. 100 questions with memos.',
         'Tₙ = dn + c.', 'n must be a natural number.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
