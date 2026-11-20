# -*- coding: utf-8 -*-
"""
South Africa Grade 8 Maths (CAPS): Algebraic Equations: Linear Equations with Unknowns on Both Sides (Grade 8: 2.4 Algebraic equations)
  python3 tools/gen_za_maths_g8_algebraic_equations.py
Linear equations, negative solutions, equations with brackets and fractions, and changing the subject of a formula
(UK Year 8 and Australia Year 8 makers).
Wrong answers come from real mistakes: moving a term without changing its sign, expanding only part of a bracket,
and multiplying only one side by the denominator.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y8_equations_with_unknowns_on_both_sides as uke
adopt(uke)
if isinstance(getattr(uke, 'R', None), random.Random): uke.R = random.Random(808110)
import gen_au_maths_y8_linear_equations as aue
adopt(aue)
if isinstance(getattr(aue, 'R', None), random.Random): aue.R = random.Random(808111)
import gen_uk_maths_y8_changing_the_subject_of_a_formula as ukc
adopt(ukc)
if isinstance(getattr(ukc, 'R', None), random.Random): ukc.R = random.Random(808112)
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
        ("Solve linear equations", [("collect", uke.one_basic, 10), ("collect", aue.one_basic, 10)]),
        ("Negative solutions", [("collect", uke.one_neg, 10), ("collect", aue.one_neg, 10)]),
        ("Equations with brackets", [("collect", uke.one_br, 10), ("collect", aue.one_br, 10)]),
        ("Equations with fractions", [("collect", uke.one_frac, 10), ("collect", aue.one_frac, 10)]),
        ("Formulae and problems", [("collect", ukc.one_step, 10), ("run", uke.problems, (), 10, ok8)]),
    ], 80811)
    finish(sets, R)
    body = lesson('<ul><li>Do the same to both sides to keep the equation balanced.</li><li>Collect the x terms on one side and the numbers on the other: 5x − 3 = 2x + 9 → 3x = 12 → x = 4.</li><li>Expand brackets first. With fractions, multiply both sides by the denominator.</li><li>Check by substituting the answer.</li></ul>',
        [example("3(x − 2) = x + 8", ["3x − 6 = x + 8", "2x = 14"], "x = 7")],
        [['The sign when moving', 'Subtract 2x from both sides; the sign changes.'], ['Part of a bracket', 'Multiply every term.'], ['One side only', 'Multiply both sides by the denominator.']])
    faq = [('What does CAPS Grade 8 say about equations?', 'Solve equations by inspection, trial and improvement or algebraic processes (additive and multiplicative inverses), including equations using laws of exponents.'), ('Can the answer be negative?', 'Yes.'), ('How do I check?', 'Substitute the answer into both sides.'), ('What is changing the subject?', 'Rearranging a formula to make another letter the subject.')]
    make('algebraic-equations', 11, 'Patterns, Functions and Algebra', 'Grade 8: 2.4 Algebraic equations',
         'Solve equations by inspection, trial and improvement or algebraic processes (additive and multiplicative inverses, and factorisation); use substitution in equations to generate tables of ordered pairs; solve equations that use laws of exponents.',
         'Algebraic Equations: Linear Equations with Unknowns on Both Sides', 'Algebraic Equations',
         'Free CAPS Grade 8 algebraic equations worksheets: linear equations, negative solutions, brackets, fractions and changing the subject. 100 questions with memos.',
         'Do the same to both sides.', 'Expand brackets first.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
