# -*- coding: utf-8 -*-
"""
South Africa Grade 7 Maths (CAPS): Algebraic Equations: Solving by Inspection and Inverse Operations (Grade 7: 2.4 Algebraic equations)
  python3 tools/gen_za_maths_g7_algebraic_equations.py
One-step and two-step equations, balance models, writing equations for stories, and checking by substitution (UK
Year 7, Australia Year 7, BC Grade 7 and Ontario Grade 7 makers).
Wrong answers come from real mistakes: using the same operation instead of the inverse, undoing the steps in the
wrong order, and changing only one side of the equation.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y7_solving_equations as uke
adopt(uke)
if isinstance(getattr(uke, 'R', None), random.Random): uke.R = random.Random(807160)
import gen_au_maths_y7_solving_linear_equations as aue
adopt(aue)
if isinstance(getattr(aue, 'R', None), random.Random): aue.R = random.Random(807161)
import gen_cabc_math_g7_two_step_equations as cbe
adopt(cbe)
if isinstance(getattr(cbe, 'R', None), random.Random): cbe.R = random.Random(807162)
import gen_caon_math_g7_equations as cae
adopt(cae)
if isinstance(getattr(cae, 'R', None), random.Random): cae.R = random.Random(807163)
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
        ("Solve by inspection", [("collect", uke.one_step, 10), ("collect", aue.one_step, 10)]),
        ("Balance the equation", [("run", cbe.set_balance, (cbe.People,), 20, ok7)]),
        ("Two-step equations", [("run", cbe.set_plus, (cbe.People,), 10, ok7), ("run", cbe.set_minus_div, (cbe.People,), 10, ok7)]),
        ("Write an equation", [("run", cbe.set_write, (cbe.People,), 10, ok7), ("run", cae.set_two_step, (cae.People,), 10, ok7)]),
        ("Equation problems", [("run", cbe.set_words, (cbe.People,), 10, ok7), ("run", cae.set_words, (cae.People,), 10, ok7)]),
    ], 80716)
    finish(sets, R)
    body = lesson('<ul><li>An equation says two expressions are equal: 3x + 5 = 26.</li><li>Do the same to both sides to keep the balance.</li><li>Undo the operations in reverse order: − 5, then ÷ 3. x = 7.</li><li>Check by substitution: 3 × 7 + 5 = 26.</li></ul>',
        [example("x ÷ 4 − 3 = 5", ["+ 3: x ÷ 4 = 8", "× 4"], "x = 32")],
        [['The same operation', 'Use the inverse.'], ['The wrong order', 'Undo + and − first.'], ['One side only', 'Do the same to both sides.']])
    faq = [('What does CAPS Grade 7 say about equations?', 'Write number sentences to describe problem situations, solve equations by inspection, trial and improvement or inverse operations, and check solutions by substitution.'), ('What is a solution?', 'The value that makes the equation true.'), ('How do I check?', 'Substitute the value back in.'), ('What is trial and improvement?', 'Trying values and getting closer each time.')]
    make('algebraic-equations', 16, 'Patterns, Functions and Algebra', 'Grade 7: 2.4 Algebraic equations',
         'Write number sentences to describe problem situations; analyse and interpret number sentences that describe a given situation; solve and complete number sentences by inspection, trial and improvement; identify variables and constants in given formulae or equations; use substitution in equations to generate tables of ordered pairs.',
         'Algebraic Equations: Solving by Inspection and Inverse Operations', 'Algebraic Equations',
         'Free CAPS Grade 7 algebraic equations worksheets: one-step and two-step equations, balances, writing equations and checking solutions. 100 questions with memos.',
         'Do the same to both sides.', 'Undo the steps in reverse order.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
