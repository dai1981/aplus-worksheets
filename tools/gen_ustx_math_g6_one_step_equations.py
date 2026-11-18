# -*- coding: utf-8 -*-
"""
Texas Grade 6 Math: One-Step Equations (TEKS 6.9A, 6.9C, 6.10A, 6.10B)
  python3 tools/gen_ustx_math_g6_one_step_equations.py
Checking solutions by substituting, tape diagram and balance models, solving x + p = q and px = q, and writing
and solving equations for word problems (the US Grade 6 makers with Texas names).
Wrong answers come from real mistakes: doing the same operation instead of the inverse, and writing the equation
from the wrong relationship.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g6_one_step_equations as ose
adopt(ose)
tx_common.GRADE = "grade-6"



def build():
    sets, R = build_sets([
        ("Is it a solution? Substitute and check", [("run", ose.set_substitute, ("rnd", ose.People), 20)]),
        ("Models and inverse operations", [("run", ose.set_models, ("rnd", ose.People), 20)]),
        ("Solve x + p = q", [("run", ose.set_add, ("rnd", ose.People), 20)]),
        ("Solve px = q", [("run", ose.set_mul, ("rnd", ose.People), 20)]),
        ("Word problems: write an equation and solve", [("run", ose.set_words, ("rnd", ose.People), 20)]),
    ], 66019)
    finish(sets, R)
    body = lesson('<ul><li>An <b>equation</b> says two expressions are equal. A <b>solution</b> makes it true.</li><li>Use the <b>inverse operation</b> to get the variable alone: subtract to undo adding, divide to undo multiplying.</li><li>Do the same thing to both sides to keep the equation balanced.</li><li>Check by substituting your answer back into the equation.</li></ul>',
        [example("x + 8 = 14", ["Subtract 8 from both sides"], "x = 6"), example("3/4 n = 9", ["Divide by 3/4: 9 × 4/3"], "n = 12")],
        [['Doing the same operation instead of the inverse: x + 8 = 14, x = 22', 'Undo adding 8 by subtracting 8.'], ['Changing only one side', 'Do the same step to both sides.'], ['Writing the equation the wrong way', 'Read the relationship: 4 years older means s + 4 = 13.']])
    faq = [('What does TEKS 6.10A ask?', 'Model and solve one-variable, one-step equations and inequalities that represent problems, including geometric concepts.'), ('What does TEKS 6.10B ask?', 'Determine if the given value(s) make(s) one-variable, one-step equations or inequalities true.'), ('What does TEKS 6.9C ask?', 'Write corresponding real-world problems given one-variable, one-step equations or inequalities.'), ('How do I check my answer?', 'Substitute it into the equation. Both sides should be equal.')]
    make('one-step-equations', 19, 'Expressions, Equations and Relationships', '6.9A, 6.9C, 6.10A, 6.10B',
         '6.9A write one-variable, one-step equations and inequalities to represent constraints or conditions within problems; 6.9C write corresponding real-world problems given one-variable, one-step equations or inequalities; 6.10A model and solve one-variable, one-step equations and inequalities that represent problems, including geometric concepts; 6.10B determine if the given value(s) make(s) one-variable, one-step equations or inequalities true',
         'One-Step Equations', 'One-Step Equations',
         'Free Grade 6 one-step equation worksheets for Texas TEKS 6.9 and 6.10: check solutions, tape diagrams and balances, solve x + p = q and px = q, and word problems. 100 questions with answers.',
         'Use the inverse operation on both sides.', 'x + 8 = 14, so x = 6. 9x = 72, so x = 8.',
         body, faq, sets, seo_title='Grade 6 One-Step Equations Worksheets (TEKS 6.9A, 6.10A, STAAR)')


if __name__ == "__main__":
    build()
