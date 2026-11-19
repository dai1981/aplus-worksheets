# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Rational Numbers as Fractions, Decimals and Percentages (Grade 7: Number and Algebra)
  python3 tools/gen_ph_math_g7_fdp.py
Changing between fractions, decimals and percentages, ordering them, and equivalent forms (UK Year 7 makers).
Wrong answers come from real mistakes: writing 3/8 as 3.8, writing 0.6 as 6%, and comparing only the digits.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_uk_maths_y7_fractions_decimals_and_percentages as ukf
adopt(ukf)
if hasattr(ukf, 'R'): ukf.R = random.Random(707080)
ph_common.GRADE = "grade-7"



def build():
    sets, R = build_sets([
        ("Fractions to decimals", [("collect", ukf.one_f2d, 20)]),
        ("Decimals to fractions", [("collect", ukf.one_d2f, 20)]),
        ("Percentages", [("collect", ukf.one_2p, 20)]),
        ("Equivalent forms", [("collect", ukf.one_equiv, 20)]),
        ("Order fractions, decimals and percentages", [("collect", ukf.one_order, 20)]),
    ], 70708)
    finish(sets, R)
    body = lesson("<ul><li>A <b>rational number</b> can be written as a fraction <span class='fr'><span class='fn'>a</span><span class='fd'>b</span></span> of integers (b ≠ 0). It can also be written as a decimal or a percentage.</li><li>Fraction → decimal: divide the numerator by the denominator. <span class='fr'><span class='fn'>3</span><span class='fd'>8</span></span> = 3 ÷ 8 = 0.375.</li><li>Decimal → percentage: multiply by 100. 0.375 = 37.5%.</li><li>To order, change all the numbers to decimals.</li></ul>",
        [example("<span class='fr'><span class='fn'>3</span><span class='fd'>5</span></span>", ["3 ÷ 5 = 0.6", "0.6 × 100"], "60%")],
        [['3/8 as 3.8', 'Divide: 3 ÷ 8 = 0.375.'], ['0.6 as 6%', '0.6 = 60%.'], ['Comparing digits', 'Write all as decimals first.']])
    faq = [('What does MATATAG Math 7 ask about rational numbers?', 'Describe given rational numbers as fractions, decimals, or percentages.'), ('Is 0.333… rational?', 'Yes. It equals 1/3.'), ('How do I write 45% as a fraction?', '45/100 = 9/20.'), ('Which is bigger, 5/8 or 0.6?', '5/8 = 0.625, so 5/8.')]
    make('fractions-decimals-and-percentages', 8, 'Number and Algebra', 'Grade 7: Number and Algebra',
         'Describe given rational numbers as fractions, decimals, or percentages.',
         'Rational Numbers as Fractions, Decimals and Percentages', 'Fractions, Decimals and Percentages',
         'Free Grade 7 fractions, decimals and percentages worksheets for the DepEd MATATAG curriculum: converting, equivalent forms and ordering rational numbers. 100 questions with answers.',
         'Fraction → decimal: divide. Decimal → percent: × 100.', 'To order, change all to decimals.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
