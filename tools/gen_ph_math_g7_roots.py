# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Square Roots of Perfect Squares and Cube Roots of Perfect Cubes (Grade 7: Number and Algebra)
  python3 tools/gen_ph_math_g7_roots.py
Perfect squares and square roots, perfect cubes and cube roots, solving x² = a and x³ = a, and word problems (US
Grade 8 and Australia Year 7 makers).
Wrong answers come from real mistakes: dividing by 2 instead of finding the square root, dividing by 3 for a cube
root, and confusing squaring with doubling.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g8_square_and_cube_roots as usr
adopt(usr)
if hasattr(usr, 'R'): usr.R = random.Random(707110)
import gen_au_maths_y7_square_numbers_and_square_roots as aus
adopt(aus)
if hasattr(aus, 'R'): aus.R = random.Random(707111)
ph_common.GRADE = "grade-7"



def build():
    sets, R = build_sets([
        ("Square roots", [("run", usr.set_sqrt, (), 20)]),
        ("Cube roots", [("run", usr.set_cbrt, (), 20)]),
        ("Perfect squares", [("collect", aus.one_square, 10), ("collect", aus.one_root, 10)]),
        ("Solve x² = a and x³ = a", [("run", usr.set_solve, (), 20)]),
        ("Root word problems", [("run", usr.set_words, (), 14), ("collect", aus.one_calc, 6)]),
    ], 70711)
    finish(sets, R)
    body = lesson('<ul><li>A <b>perfect square</b> is a whole number times itself: 49 = 7 × 7. Its <b>square root</b> is √49 = 7.</li><li>A <b>perfect cube</b> is a number used three times as a factor: 64 = 4 × 4 × 4. Its <b>cube root</b> is ∛64 = 4.</li><li>A square with area 81 cm² has sides of √81 = 9 cm. A cube with volume 125 cm³ has edges of ∛125 = 5 cm.</li><li>∛(−27) = −3, because (−3) × (−3) × (−3) = −27.</li></ul>',
        [example("√144", ["12 × 12 = 144"], "12"), example("∛216", ["6 × 6 × 6 = 216"], "6")],
        [['Dividing by 2', '√64 is 8, not 32.'], ['Dividing by 3', '∛27 is 3, not 9.'], ['Squaring as doubling', '5² = 25, not 10.']])
    faq = [('What does MATATAG Math 7 ask about roots?', 'Determine the square roots of perfect squares and the cube roots of perfect cubes.'), ('Does 49 have two square roots?', 'Yes, 7 and −7; √49 means the positive one, 7.'), ('Can a negative number have a cube root?', 'Yes. ∛(−8) = −2.'), ('Is 50 a perfect square?', 'No. It is between 49 and 64.')]
    make('square-roots-and-cube-roots', 11, 'Number and Algebra', 'Grade 7: Number and Algebra',
         'Determine the square roots of perfect squares and the cube roots of perfect cubes.',
         'Square Roots of Perfect Squares and Cube Roots of Perfect Cubes', 'Square and Cube Roots',
         'Free Grade 7 square roots and cube roots worksheets for the DepEd MATATAG curriculum: perfect squares, perfect cubes, solving x² = a and word problems. 100 questions with answers.',
         '√49 = 7 because 7 × 7 = 49.', '∛64 = 4 because 4 × 4 × 4 = 64.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
