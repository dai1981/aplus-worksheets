# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Formulas: Substituting and Solving for a Variable (Grade 7: Number and Algebra)
  python3 tools/gen_ph_math_g7_formulas.py
Substituting into formulas, finding an unknown in a formula (Australia Year 7 makers), solving a formula for one
variable in terms of the others (UK Year 8 maker), and formula problems (US Grade 6 maker).
Wrong answers come from real mistakes: substituting into the wrong letter, undoing operations in the wrong order,
and dividing only part of one side.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_au_maths_y7_formulas_and_substitution as auf
adopt(auf)
if hasattr(auf, 'R'): auf.R = random.Random(707270)
import gen_uk_maths_y8_changing_the_subject_of_a_formula as ukc
adopt(ukc)
if hasattr(ukc, 'R'): ukc.R = random.Random(707271)
import gen_us_math_g6_expressions as uex
adopt(uex)
if hasattr(uex, 'R'): uex.R = random.Random(707272)
ph_common.GRADE = "grade-7"



def build():
    sets, R = build_sets([
        ("Substitute into a formula", [("collect", auf.one_sub, 20)]),
        ("Formulas with two or more variables", [("collect", auf.one_sub2, 20)]),
        ("Solve for a variable", [("collect", ukc.one_step, 20)]),
        ("Find the unknown", [("collect", auf.one_unknown, 20)]),
        ("Formula problems", [("run", uex.set_formulas, ("rnd", uex.People), 12), ("collect", ukc.one_step, 8)]),
    ], 70727)
    finish(sets, R)
    body = lesson("<ul><li>A <b>formula</b> is an equation that shows how quantities are related, like A = lw or d = rt.</li><li>To use a formula, substitute the known values and calculate.</li><li>To solve a formula for one variable, use the properties of equality as with any equation: from d = rt, divide both sides by t to get r = <span class='fr'><span class='fn'>d</span><span class='fd'>t</span></span>.</li><li>Undo the operations in reverse order, and do the same to the whole of both sides.</li></ul>",
        [example("P = 2l + 2w, solve for l", ["P − 2w = 2l", "divide by 2"], "l = (P − 2w) ÷ 2")],
        [['Wrong letter', 'Match each value to its letter.'], ['Wrong order', 'Undo + and − before × and ÷.'], ['Dividing part of a side', 'Divide the whole side.']])
    faq = [('What does MATATAG Math 7 ask about formulas?', 'Solve one variable in terms of the other variables in a formula, and solve problems involving algebraic expressions and formulas.'), ('What is the subject of a formula?', 'The variable on its own on one side, like A in A = lw.'), ('Why rearrange a formula?', 'To find a different quantity quickly, like time from distance and speed.'), ('Do units matter?', 'Yes. Use the same units throughout.')]
    make('formulas-and-solving-for-a-variable', 27, 'Number and Algebra', 'Grade 7: Number and Algebra',
         'Solve one variable in terms of the other variables in a formula; solve problems involving algebraic expressions and formulas.',
         'Formulas: Substituting and Solving for a Variable', 'Formulas',
         'Free Grade 7 formula worksheets for the DepEd MATATAG curriculum: substituting into formulas, finding unknowns and solving a formula for one variable. 100 questions with answers.',
         'Substitute, then calculate.', 'Solve for a variable: undo the operations on both sides.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
