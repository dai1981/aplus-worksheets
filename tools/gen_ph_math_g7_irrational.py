# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Irrational Numbers and Their Locations on the Number Line (Grade 7: Number and Algebra)
  python3 tools/gen_ph_math_g7_irrational.py
Rational or irrational, estimating square roots and cube roots between whole numbers, locating them on the number
line, and ordering (US Grade 8 and Texas Grade 8 makers).
Wrong answers come from real mistakes: calling every square root irrational, placing √20 near 10, and thinking π
equals 3.14 exactly.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g8_rational_and_irrational_numbers as uri
adopt(uri)
if hasattr(uri, 'R'): uri.R = random.Random(707120)
import gen_us_math_g8_square_and_cube_roots as usr
adopt(usr)
if hasattr(usr, 'R'): usr.R = random.Random(707121)
import gen_ustx_math_g8_approximating_irrationals as txi
adopt(txi)
if hasattr(txi, 'R'): txi.R = random.Random(707122)
ph_common.GRADE = "grade-7"



def build():
    sets, R = build_sets([
        ("Rational or irrational?", [("run", uri.set_classify, (), 20)]),
        ("Between which two whole numbers?", [("run", usr.set_estimate, (), 20)]),
        ("Locate on the number line", [("collect", txi.one_locate, 20)]),
        ("Estimate irrational numbers", [("run", uri.set_estimate, (), 20)]),
        ("Order real numbers", [("run", uri.set_order, (), 20)]),
    ], 70712)
    finish(sets, R)
    body = lesson('<ul><li>An <b>irrational number</b> cannot be written as a fraction of integers. Its decimal never ends and never repeats.</li><li>√2, √5, ∛10 and π are irrational. √49 = 7 and ∛8 = 2 are rational, because 49 and 8 are perfect powers.</li><li>To locate √30, find the perfect squares around it: 25 &lt; 30 &lt; 36, so 5 &lt; √30 &lt; 6, closer to 5.</li><li>π ≈ 3.14 is only an approximation.</li></ul>',
        [example("√40", ["36 &lt; 40 &lt; 49", "6 &lt; √40 &lt; 7"], "about 6.3")],
        [['Every root is irrational', '√36 = 6 is rational.'], ['√20 near 10', '√20 is between 4 and 5.'], ['π = 3.14', '3.14 is only close to π.']])
    faq = [('What does MATATAG Math 7 ask about irrational numbers?', 'Identify irrational numbers involving square roots and cube roots, and their locations on the number line.'), ('Is 0.121212… irrational?', 'No. It repeats, so it is rational.'), ('Is √2 between 1 and 2?', 'Yes, about 1.41.'), ('Why is π irrational?', 'Its decimal never ends and never repeats.')]
    make('irrational-numbers-on-the-number-line', 12, 'Number and Algebra', 'Grade 7: Number and Algebra',
         'Identify irrational numbers involving square roots and cube roots, and their locations on the number line.',
         'Irrational Numbers and Their Locations on the Number Line', 'Irrational Numbers',
         'Free Grade 7 irrational numbers worksheets for the DepEd MATATAG curriculum: rational or irrational, estimating square and cube roots, and locating them on the number line. 100 questions with answers.',
         'Irrational: the decimal never ends and never repeats.', '25 &lt; 30 &lt; 36, so 5 &lt; √30 &lt; 6.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
