# -*- coding: utf-8 -*-
"""
South Africa Grade 10 Maths (CAPS): Linear Equations and Literal Equations (Grade 10: Equations and inequalities)
  python3 tools/gen_za_maths_g10_linear_equations.py
Linear equations with brackets, unknowns on both sides and fractions, and changing the subject of a formula (US
Algebra 1 makers).
Wrong answers come from real mistakes: expanding only part of a bracket, multiplying only one side by the
denominator, and dividing only one term when making a letter the subject.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_us_math_a1_multi_step_equations as usm
adopt(usm)
if isinstance(getattr(usm, 'R', None), random.Random): usm.R = random.Random(810060)
import gen_us_math_a1_literal_equations as usl
adopt(usl)
if isinstance(getattr(usl, 'R', None), random.Random): usl.R = random.Random(810061)
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
        ("Brackets", [("collect", usm.one_dist, 20)]),
        ("Unknowns on both sides", [("collect", usm.one_both, 20)]),
        ("Equations with fractions", [("collect", usm.one_frac, 10), ("collect", usm.one_dec, 10)]),
        ("Change the subject", [("collect", usl.one_step, 10), ("collect", usl.one_std, 10)]),
        ("Literal equations", [("collect", usl.one_factor_out, 20)]),
    ], 81006)
    finish(sets, R)
    body = lesson('<ul><li>Expand brackets and remove fractions by multiplying both sides by the LCD.</li><li>Collect the unknown on one side and the numbers on the other.</li><li>Literal equations: treat the other letters like numbers.</li><li>If the subject appears twice, take it out as a common factor.</li></ul>',
        [example("Make r the subject: A = P + Prt", ["A − P = Prt"], "r = (A − P)/(Pt)")],
        [['Part of a bracket', 'Multiply every term.'], ['One side only', 'Multiply both sides by the LCD.'], ['Dividing one term', 'Divide the whole side.']])
    faq = [('What does CAPS Grade 10 say about equations?', 'Solve linear equations and literal equations (changing the subject of a formula).'), ('What is a literal equation?', 'An equation with several letters, like a formula.'), ('How do I check?', 'Substitute the answer into the original equation.'), ('Can a linear equation have no solution?', 'Yes, if the x terms cancel and a false statement is left.')]
    make('linear-and-literal-equations', 6, 'Algebra and Number Patterns', 'Grade 10: Equations and inequalities',
         'Revise the solution of linear equations; solve literal equations (changing the subject of a formula).',
         'Linear Equations and Literal Equations', 'Linear and Literal Equations',
         'Free CAPS Grade 10 worksheets: linear equations with brackets and fractions and changing the subject of a formula. 100 questions with memos.',
         'Do the same to both sides.', 'Subject twice: take it out as a common factor.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
