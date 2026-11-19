# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Angle Pairs: Complementary, Supplementary, Vertical and Adjacent Angles (Grade 7: Measurement and Geometry)
  python3 tools/gen_ph_math_g7_angle_pairs.py
Naming angle pairs, angles on a line and around a point, vertical angles, writing and solving equations for angle
pairs, and problems (US Grade 7 makers).
Wrong answers come from real mistakes: mixing up complementary (90°) and supplementary (180°), thinking vertical
angles add up to 180°, and subtracting from the wrong total.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g7_angle_relationships as uar
adopt(uar)
if hasattr(uar, 'R'): uar.R = random.Random(707020)
ph_common.GRADE = "grade-7"



def build():
    sets, R = build_sets([
        ("Name the angle pair", [("run", uar.set_words, (), 20)]),
        ("Angles on a line", [("run", uar.set_lines, (), 20)]),
        ("Vertical angles", [("run", uar.set_vertical, (), 20)]),
        ("Equations with angle pairs", [("run", uar.set_equations, (), 20)]),
        ("Angle pair problems", [("run", uar.set_problems, (), 20)]),
    ], 70702)
    finish(sets, R)
    body = lesson('<ul><li><b>Complementary</b> angles add up to 90°. <b>Supplementary</b> angles add up to 180°.</li><li><b>Adjacent</b> angles share a vertex and a side. A <b>linear pair</b> is two adjacent angles on a straight line: they are supplementary.</li><li><b>Vertical angles</b> are opposite each other where two lines cross. They are equal.</li><li>For an unknown angle, write an equation: x + 35 = 90.</li></ul>',
        [example("The supplement of 65°", ["180 − 65"], "115°"), example("Vertical angles 3x and 75°", ["3x = 75"], "x = 25")],
        [['Complementary or supplementary?', 'Complementary: 90°. Supplementary: 180°.'], ['Vertical angles add to 180°', 'They are equal; the linear pairs add to 180°.'], ['Wrong total', 'Around a point, the angles add up to 360°.']])
    faq = [('What does MATATAG Math 7 ask about angle pairs?', 'Describe and explain the relationships between angle pairs based on their measures.'), ('Can three angles be complementary?', 'No. Complementary and supplementary describe pairs of angles.'), ('Are vertical angles always equal?', 'Yes.'), ('What is a linear pair?', 'Two adjacent angles that form a straight line.')]
    make('angle-pairs', 2, 'Measurement and Geometry', 'Grade 7: Measurement and Geometry',
         'Describe and explain the relationships between angle pairs based on their measures.',
         'Angle Pairs: Complementary, Supplementary, Vertical and Adjacent Angles', 'Angle Pairs',
         'Free Grade 7 angle pairs worksheets for the DepEd MATATAG curriculum: complementary, supplementary, vertical, adjacent angles and linear pairs, with equations. 100 questions with answers.',
         'Complementary: 90°. Supplementary: 180°.', 'Vertical angles are equal.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
