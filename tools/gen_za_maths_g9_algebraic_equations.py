# -*- coding: utf-8 -*-
"""
South Africa Grade 9 Maths (CAPS): Algebraic Equations: Linear Equations, Equations by Factorisation and Exponential Equations (Grade 9: 2.4 Algebraic equations)
  python3 tools/gen_za_maths_g9_algebraic_equations.py
Linear equations with brackets and fractions, equations solved by factorisation, exponential equations, and changing
the subject of a formula (UK Year 8, Singapore Secondary 2 and Secondary 3 makers).
Wrong answers come from real mistakes: dividing by x and losing a solution, giving only one solution of a factorised
equation, and multiplying only one side by the denominator.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y8_equations_with_unknowns_on_both_sides as uke
adopt(uke)
if isinstance(getattr(uke, 'R', None), random.Random): uke.R = random.Random(809090)
import gen_sg_maths_s2_quadratic_equations as sgq
adopt(sgq)
if isinstance(getattr(sgq, 'R', None), random.Random): sgq.R = random.Random(809091)
import gen_sg_maths_s3_indices as sgi
adopt(sgi)
if isinstance(getattr(sgi, 'R', None), random.Random): sgi.R = random.Random(809092)
import gen_sg_maths_s2_changing_the_subject_of_a_formula as sgc
adopt(sgc)
if isinstance(getattr(sgc, 'R', None), random.Random): sgc.R = random.Random(809093)
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
        ("Linear equations", [("collect", uke.one_br, 10), ("collect", uke.one_frac, 10)]),
        ("Equations by factorisation", [("collect", sgq.one_zero, 10), ("collect", sgq.one_monic, 10)]),
        ("More factorisation equations", [("collect", sgq.one_special, 10), ("collect", sgq.one_monic, 10)]),
        ("Exponential equations", [("collect", sgi.one_eq, 20)]),
        ("Formulae and problems", [("collect", sgc.one_step, 10), ("run", uke.problems, (), 10, ok9)]),
    ], 80909)
    finish(sets, R)
    body = lesson('<ul><li>Linear equations: expand, collect like terms, then solve.</li><li>Equations by factorisation: make one side 0, factorise, then each factor = 0.</li><li>x² − 5x + 6 = 0 → (x − 2)(x − 3) = 0 → x = 2 or x = 3.</li><li>Exponential equations: write both sides with the same base. 3ˣ = 81 = 3⁴, so x = 4.</li></ul>',
        [example("x² = 7x", ["x² − 7x = 0", "x(x − 7) = 0"], "x = 0 or x = 7")],
        [['Dividing by x', 'You lose the solution x = 0.'], ['One solution only', 'Each factor gives a solution.'], ['One side only', 'Multiply both sides by the denominator.']])
    faq = [('What does CAPS Grade 9 say about equations?', 'Solve equations by inspection, trial and improvement or algebraic processes, including factorisation, and solve equations using laws of exponents.'), ('Why make one side 0?', 'If a product is 0, one of the factors is 0.'), ('How many solutions can x² = 9 have?', 'Two: 3 and −3.'), ('What is 2ˣ = 1?', 'x = 0.')]
    make('algebraic-equations', 9, 'Patterns, Functions and Algebra', 'Grade 9: 2.4 Algebraic equations',
         'Solve equations by inspection, trial and improvement or algebraic processes (additive and multiplicative inverses, and factorisation); solve equations of the form: a product of factors = 0; solve equations using laws of exponents; use substitution in equations to generate tables of ordered pairs.',
         'Algebraic Equations: Linear Equations, Equations by Factorisation and Exponential Equations', 'Algebraic Equations',
         'Free CAPS Grade 9 algebraic equations worksheets: linear equations, equations by factorisation, exponential equations and formulae. 100 questions with memos.',
         'Make one side 0, factorise, each factor = 0.', 'Same base: equate the exponents.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
