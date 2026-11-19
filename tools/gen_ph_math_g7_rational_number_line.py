# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Ordering Rational Numbers on a Number Line (Grade 7: Number and Algebra)
  python3 tools/gen_ph_math_g7_rational_number_line.py
Rational numbers on the number line, comparing and ordering positive and negative fractions and decimals (Ontario
Grade 7, Australia Year 7 and UK Year 7 makers).
Wrong answers come from real mistakes: thinking −3/4 is greater than −1/2, counting tick marks instead of spaces,
and ordering negative numbers like positive ones.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_caon_math_g7_compare as cac
adopt(cac)
if hasattr(cac, 'R'): cac.R = random.Random(707090)
import gen_au_maths_y7_fractions_decimals_and_percentages as auf
adopt(auf)
if hasattr(auf, 'R'): auf.R = random.Random(707091)
import gen_uk_maths_y7_place_value_and_ordering as ukp
adopt(ukp)
if hasattr(ukp, 'R'): ukp.R = random.Random(707092)
ph_common.GRADE = "grade-7"



def build():
    sets, R = build_sets([
        ("Rational numbers on the number line", [("run", cac.set_numberline, ("rnd",), 20)]),
        ("Points on the number line", [("collect", auf.one_nl, 20)]),
        ("Compare rational numbers", [("run", cac.set_compare, ("rnd",), 20)]),
        ("Order negative numbers", [("collect", ukp.one_neg_order, 20)]),
        ("Order and compare", [("collect", ukp.one_ineq, 10), ("run", cac.set_between_round, ("rnd",), 10)]),
    ], 70709)
    finish(sets, R)
    body = lesson("<ul><li>On a number line, numbers increase from left to right. Any number is greater than every number to its left.</li><li>Negative numbers are to the left of 0. −0.5 is greater than −0.75, because it is closer to 0 on the right.</li><li>To place a fraction, split each unit into the denominator's number of equal parts and count the spaces.</li><li>To order, change to decimals, then put them on a number line.</li></ul>",
        [example("Order −0.4, <span class='fr'><span class='fn'>1</span><span class='fd'>4</span></span>, −<span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>, 0.3", ["−0.4, 0.25, −0.5, 0.3"], "−1/2, −0.4, 1/4, 0.3")],
        [['−3/4 &gt; −1/2', '−3/4 is farther left, so it is smaller.'], ['Counting tick marks', 'Count the spaces between them.'], ['Negatives like positives', 'For negatives, the bigger digits mean smaller numbers.']])
    faq = [('What does MATATAG Math 7 ask about the number line?', 'Order rational numbers on a number line.'), ('Is −2.5 less than −2?', 'Yes. It is farther left.'), ('Where is 7/4 on a number line?', 'Between 1 and 2, at 1.75.'), ('Can two different fractions be at the same point?', 'Yes, if they are equivalent, like 1/2 and 2/4.')]
    make('ordering-rational-numbers-on-a-number-line', 9, 'Number and Algebra', 'Grade 7: Number and Algebra',
         'Order rational numbers on a number line.',
         'Ordering Rational Numbers on a Number Line', 'Rational Numbers on a Number Line',
         'Free Grade 7 worksheets on rational numbers on the number line for the DepEd MATATAG curriculum: plotting, comparing and ordering positive and negative fractions and decimals. 100 questions with answers.',
         'On a number line, numbers increase to the right.', '−0.5 &gt; −0.75: closer to 0 is greater.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
