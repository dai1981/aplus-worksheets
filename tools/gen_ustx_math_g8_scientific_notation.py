# -*- coding: utf-8 -*-
"""
Texas Grade 8 Math: Scientific Notation (TEKS 8.2C)
  python3 tools/gen_ustx_math_g8_scientific_notation.py
Writing large and small numbers in scientific notation, converting to standard form, comparing, and operations in
real-world contexts (the US Grade 8 makers with a new seed).
Wrong answers come from real mistakes: moving the decimal point the wrong way, a first factor that is not between 1
and 10, and adding exponents when comparing.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g8_scientific_notation as sn
adopt(sn)
sn.R = random.Random(680030)
tx_common.GRADE = "grade-8"



def build():
    sets, R = build_sets([
        ("Large numbers", [("run", sn.set_large, (), 20)]),
        ("Small numbers", [("run", sn.set_small, (), 20)]),
        ("Standard form and correct notation", [("run", sn.set_standard, (), 20)]),
        ("Compare and how many times", [("run", sn.set_compare, (), 20)]),
        ("Operations and real life", [("run", sn.set_ops, (), 20)]),
    ], 68003)
    finish(sets, R)
    body = lesson('<ul><li><b>Scientific notation</b> writes a number as a × 10<sup>n</sup>, where 1 ≤ a &lt; 10.</li><li>Large numbers have a positive exponent: 3,500,000 = 3.5 × 10<sup>6</sup>.</li><li>Small numbers have a negative exponent: 0.0042 = 4.2 × 10<sup>−3</sup>.</li><li>To compare, look at the exponents first, then the first factors.</li></ul>',
        [example("Write 72,000,000.", ["Move the point 7 places left"], "7.2 × 10⁷"), example("Write 0.00056.", ["Move the point 4 places right"], "5.6 × 10⁻⁴")],
        [['Moving the decimal point the wrong way', 'Large numbers get positive exponents; small numbers get negative ones.'], ['A first factor not between 1 and 10', '35 × 10⁵ should be 3.5 × 10⁶.'], ['Comparing only the first factors', 'Compare the exponents first: 3 × 10⁸ > 9 × 10⁷.']])
    faq = [('What does TEKS 8.2C ask?', 'Convert between standard decimal notation and scientific notation.'), ('Why use scientific notation?', 'It makes very large and very small numbers easy to read and compare.'), ('Is 12 × 10⁴ in scientific notation?', 'No. The first factor must be at least 1 and less than 10: 1.2 × 10⁵.'), ('What does a negative exponent mean?', 'The number is less than 1.')]
    make('scientific-notation', 3, 'Number and Operations', '8.2C',
         '8.2C convert between standard decimal notation and scientific notation',
         'Scientific Notation', 'Scientific Notation',
         'Free Grade 8 scientific notation worksheets for Texas TEKS 8.2C: write large and small numbers in scientific notation, standard form, compare and operations. 100 questions with answers.',
         'a × 10ⁿ with 1 ≤ a < 10.', '3,500,000 = 3.5 × 10⁶. 0.0042 = 4.2 × 10⁻³.',
         body, faq, sets, seo_title='Grade 8 Scientific Notation Worksheets (TEKS 8.2C, STAAR)')


if __name__ == "__main__":
    build()
