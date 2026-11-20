# -*- coding: utf-8 -*-
"""
South Africa Grade 10 Maths (CAPS): Simultaneous Linear Equations (Grade 10: Equations and inequalities)
  python3 tools/gen_za_maths_g10_simultaneous.py
Solving simultaneous linear equations by elimination and substitution, and word problems (US Algebra 1 and UK Year 9
makers).
Wrong answers come from real mistakes: adding when the signs are the same, multiplying only one term of an equation,
and finding only x.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_us_math_a1_systems_of_linear_equations as uss
adopt(uss)
if isinstance(getattr(uss, 'R', None), random.Random): uss.R = random.Random(810080)
import gen_uk_maths_y9_simultaneous_equations as uks
adopt(uks)
if isinstance(getattr(uks, 'R', None), random.Random): uks.R = random.Random(810081)
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
        ("Add to eliminate", [("collect", uss.one_add, 10), ("collect", uks.one_add, 10)]),
        ("Subtract to eliminate", [("collect", uss.one_sub, 10), ("collect", uks.one_sub, 10)]),
        ("Multiply first", [("collect", uss.one_mult, 10), ("collect", uks.one_mult, 10)]),
        ("Substitution", [("collect", uss.one_subst, 10), ("collect", uks.one_subst, 10)]),
        ("Simultaneous equation problems", [("collect", uss.one_both, 10), ("run", uks.problems, (), 10, ok10)]),
    ], 81008)
    finish(sets, R)
    body = lesson('<ul><li>Elimination: add or subtract the equations to remove one unknown.</li><li>Same signs: subtract. Opposite signs: add.</li><li>Multiply a whole equation first if the coefficients do not match.</li><li>Substitution: make one unknown the subject and substitute it into the other equation.</li></ul>',
        [example("2x + y = 7 and x − y = 2", ["add: 3x = 9"], "x = 3, y = 1")],
        [['Wrong operation', 'Same signs: subtract.'], ['One term only', 'Multiply every term.'], ['Only x', 'Substitute back to find y.']])
    faq = [('What does CAPS Grade 10 say about simultaneous equations?', 'Solve simultaneous linear equations in two unknowns.'), ('What does the solution mean on a graph?', 'The point where the two lines cross.'), ('Can there be no solution?', 'Yes, for parallel lines.'), ('Which method is best?', 'Elimination when coefficients match; substitution when one unknown is easy to isolate.')]
    make('simultaneous-equations', 8, 'Algebra and Number Patterns', 'Grade 10: Equations and inequalities',
         'Solve simultaneous linear equations in two unknowns.',
         'Simultaneous Linear Equations', 'Simultaneous Equations',
         'Free CAPS Grade 10 simultaneous equations worksheets: elimination, substitution and word problems. 100 questions with memos.',
         'Eliminate one unknown, solve, then substitute back.', 'Same signs: subtract.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
