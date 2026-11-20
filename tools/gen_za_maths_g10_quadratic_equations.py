# -*- coding: utf-8 -*-
"""
South Africa Grade 10 Maths (CAPS): Quadratic Equations by Factorisation (Grade 10: Equations and inequalities)
  python3 tools/gen_za_maths_g10_quadratic_equations.py
Solving quadratic equations by factorisation, the zero product property, equations with square roots, and word
problems (US Algebra 1 and Singapore Secondary 2 makers).
Wrong answers come from real mistakes: dividing by x and losing a root, not making one side zero, and giving only the
positive square root.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_us_math_a1_solving_quadratics_by_factoring as usq
adopt(usq)
if isinstance(getattr(usq, 'R', None), random.Random): usq.R = random.Random(810070)
import gen_sg_maths_s2_quadratic_equations as sgq
adopt(sgq)
if isinstance(getattr(sgq, 'R', None), random.Random): sgq.R = random.Random(810071)
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
        ("Zero product", [("collect", usq.one_zp, 10), ("collect", sgq.one_zero, 10)]),
        ("Solve by factorising", [("collect", usq.one_simple, 10), ("collect", sgq.one_monic, 10)]),
        ("Harder quadratics", [("collect", usq.one_hard, 10), ("collect", sgq.one_nonmonic, 10)]),
        ("Square roots", [("collect", usq.one_sqrt, 10), ("collect", sgq.one_special, 10)]),
        ("Quadratic problems", [("collect", sgq.one_prob, 10), ("run", usq.problems, (), 10, ok10)]),
    ], 81007)
    finish(sets, R)
    body = lesson('<ul><li>Make one side 0: ax² + bx + c = 0.</li><li>Factorise, then set each factor to 0 (zero product).</li><li>x² = 25 gives x = ±5: remember the negative root.</li><li>Check that the answers make sense in a word problem.</li></ul>',
        [example("2x² − 5x − 3 = 0", ["(2x + 1)(x − 3) = 0"], "x = −½ or x = 3")],
        [['Dividing by x', 'You lose x = 0.'], ['Not zero', 'Make one side 0 first.'], ['Only +', 'x² = 25 gives ±5.']])
    faq = [('What does CAPS Grade 10 say about quadratic equations?', 'Solve quadratic equations by factorisation.'), ('Can a quadratic have one root?', 'Yes, when it is a perfect square.'), ('What if it does not factorise?', 'The quadratic formula comes in Grade 11.'), ('Why reject a root?', 'A length or a time cannot be negative.')]
    make('quadratic-equations', 7, 'Algebra and Number Patterns', 'Grade 10: Equations and inequalities',
         'Solve quadratic equations (by factorisation).',
         'Quadratic Equations by Factorisation', 'Quadratic Equations',
         'Free CAPS Grade 10 quadratic equations worksheets: zero product, solving by factorising, square roots and word problems. 100 questions with memos.',
         'Make one side 0, factorise, each factor = 0.', 'x² = k gives ±√k.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
