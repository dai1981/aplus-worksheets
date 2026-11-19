# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Scientific Notation: Very Large and Very Small Numbers (Grade 7: Number and Algebra)
  python3 tools/gen_ph_math_g7_scientific_notation.py
Writing very large and very small numbers in scientific notation and back, comparing, and multiplying and dividing
numbers in scientific notation (US Grade 8 makers).
Wrong answers come from real mistakes: a first factor of 10 or more, counting the zeros instead of the places
moved, and using a positive exponent for a small number.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g8_scientific_notation as usn
adopt(usn)
if hasattr(usn, 'R'): usn.R = random.Random(707280)
ph_common.GRADE = "grade-7"



def build():
    sets, R = build_sets([
        ("Large numbers", [("run", usn.set_large, (), 20)]),
        ("Small numbers", [("run", usn.set_small, (), 20)]),
        ("Back to decimal form", [("run", usn.set_standard, (), 20)]),
        ("Compare numbers", [("run", usn.set_compare, (), 20)]),
        ("Operations", [("run", usn.set_ops, (), 20)]),
    ], 70728)
    finish(sets, R)
    body = lesson('<ul><li>A number in <b>scientific notation</b> is written a × 10<sup>n</sup>, where 1 ≤ a &lt; 10 and n is an integer.</li><li>Large numbers have a positive exponent: 93,000,000 = 9.3 × 10<sup>7</sup>.</li><li>Small numbers have a negative exponent: 0.00042 = 4.2 × 10<sup>−4</sup>.</li><li>To multiply, multiply the first factors and add the exponents; to divide, divide the first factors and subtract the exponents. Then adjust so the first factor is between 1 and 10.</li></ul>',
        [example("(3 × 10<sup>5</sup>)(4 × 10<sup>3</sup>)", ["3 × 4 = 12", "10<sup>5 + 3</sup> = 10<sup>8</sup>", "12 × 10<sup>8</sup>"], "1.2 × 10<sup>9</sup>")],
        [['First factor 10 or more', '45 × 10³ should be 4.5 × 10⁴.'], ['Counting zeros', 'Count the places the decimal point moves.'], ['Positive exponent for small numbers', '0.003 = 3 × 10⁻³.']])
    faq = [('What does MATATAG Math 7 ask about scientific notation?', 'Write numbers in scientific notation to represent very large or very small numbers, and vice versa, and perform operations on numbers expressed in scientific notation.'), ('Where is scientific notation used?', 'In science, for distances in space, sizes of cells and populations.'), ('Is 0.5 × 10³ in scientific notation?', 'No. The first factor must be at least 1: 5 × 10².'), ('How many people live in the Philippines in scientific notation?', 'About 1.1 × 10⁸.')]
    make('scientific-notation', 28, 'Number and Algebra', 'Grade 7: Number and Algebra',
         'Write numbers in scientific notation to represent very large or very small numbers, and vice versa; perform operations on numbers expressed in scientific notation.',
         'Scientific Notation: Very Large and Very Small Numbers', 'Scientific Notation',
         'Free Grade 7 scientific notation worksheets for the DepEd MATATAG curriculum: very large and very small numbers, converting, comparing and operations. 100 questions with answers.',
         'a × 10ⁿ with 1 ≤ a &lt; 10.', 'Large numbers: positive exponent. Small numbers: negative exponent.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
