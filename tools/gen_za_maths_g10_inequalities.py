# -*- coding: utf-8 -*-
"""
South Africa Grade 10 Maths (CAPS): Linear Inequalities (Grade 10: Equations and inequalities)
  python3 tools/gen_za_maths_g10_inequalities.py
Solving linear inequalities, multiplying and dividing by negatives, compound inequalities and number lines (US Algebra
1 and Singapore Secondary 2 and Secondary 3 makers).
Wrong answers come from real mistakes: not reversing the sign when dividing by a negative, reading the number line
the wrong way, and solving only one part of a compound inequality.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_us_math_a1_multi_step_and_compound_inequalities as usi
adopt(usi)
if isinstance(getattr(usi, 'R', None), random.Random): usi.R = random.Random(810090)
import gen_sg_maths_s2_linear_inequalities as sgi
adopt(sgi)
if isinstance(getattr(sgi, 'R', None), random.Random): sgi.R = random.Random(810091)
import gen_sg_maths_s3_simultaneous_linear_inequalities as sgs
adopt(sgs)
if isinstance(getattr(sgs, 'R', None), random.Random): sgs.R = random.Random(810092)
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
        ("Solve inequalities", [("collect", sgi.one_solve, 10), ("collect", usi.one_hard, 10)]),
        ("Unknowns on both sides", [("collect", usi.one_both, 10), ("collect", sgi.one_hard, 10)]),
        ("Number lines", [("collect", sgi.one_nl, 10), ("collect", usi.one_graph, 10)]),
        ("Compound inequalities", [("collect", usi.one_and, 10), ("collect", sgs.one_and, 10)]),
        ("Integer solutions", [("collect", sgi.one_list, 10), ("collect", sgs.one_pair, 10)]),
    ], 81009)
    finish(sets, R)
    body = lesson('<ul><li>Solve like an equation.</li><li>When you multiply or divide by a negative number, reverse the inequality sign.</li><li>On a number line, an open dot means &lt; or &gt;; a closed dot means ≤ or ≥.</li><li>A compound inequality like −2 &lt; 3x + 1 ≤ 7 is solved in all three parts.</li></ul>',
        [example("−3x + 5 &lt; 14", ["−3x &lt; 9", "÷ (−3): reverse"], "x &gt; −3")],
        [['Not reversing', 'Dividing by a negative flips the sign.'], ['The number line', 'Open dot: not included.'], ['One part only', 'Do the same to all three parts.']])
    faq = [('What does CAPS Grade 10 say about inequalities?', 'Solve linear inequalities and show the solution graphically and in interval notation.'), ('What is interval notation?', 'Writing x &gt; 2 as (2; ∞).'), ('Is −5 &lt; −2?', 'Yes.'), ('Why reverse the sign?', 'Multiplying by a negative swaps the order of numbers.')]
    make('linear-inequalities', 9, 'Algebra and Number Patterns', 'Grade 10: Equations and inequalities',
         'Solve linear inequalities (and show solution graphically); interval notation must be known.',
         'Linear Inequalities', 'Linear Inequalities',
         'Free CAPS Grade 10 linear inequalities worksheets: solving inequalities, negative coefficients, number lines and compound inequalities. 100 questions with memos.',
         'Divide by a negative: reverse the sign.', 'Open dot: not included.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
