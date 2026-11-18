# -*- coding: utf-8 -*-
"""
Texas Grade 7 Math: Unit Rates with Fractions (TEKS 7.4B)
  python3 tools/gen_ustx_math_g7_unit_rates.py
Unit rates by dividing fractions, complex fractions, comparing rates, mixed numbers and mixed units, and word
problems (the US Grade 7 makers with a new seed).
Wrong answers come from real mistakes: dividing the wrong way, multiplying instead of dividing, and comparing
without a common unit.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g7_unit_rates_fractions as urf
adopt(urf)
urf.R = random.Random(670060)
tx_common.GRADE = "grade-7"



def build():
    sets, R = build_sets([
        ("Dividing by a whole number for a unit rate", [("run", urf.set_whole, (), 20)]),
        ("Complex fractions: fraction ÷ fraction", [("run", urf.set_complex, (), 20)]),
        ("Compare rates and use them", [("run", urf.set_compare, (), 20)]),
        ("Mixed numbers and mixed units", [("run", urf.set_mixed_units, (), 20)]),
        ("Word problems", [("run", urf.set_words, (), 20)]),
    ], 67006)
    finish(sets, R)
    body = lesson('<ul><li>A <b>unit rate</b> is the amount for 1 unit: miles per 1 hour, dollars per 1 pound.</li><li>Divide the first quantity by the second: 1/2 mile in 1/4 hour is 1/2 ÷ 1/4 = 2 miles per hour.</li><li>A <b>complex fraction</b> has a fraction in the top or bottom. Divide to simplify it.</li><li>To compare rates, find each unit rate in the same units.</li></ul>',
        [example("3/4 mile in 1/6 hour", ["3/4 ÷ 1/6 = 3/4 × 6"], "4 1/2 miles per hour"), example("2 1/2 gallons in 1/2 hour", ["5/2 ÷ 1/2 = 5"], "5 gallons per hour")],
        [['Dividing the wrong way', 'Miles per hour: miles ÷ hours.'], ['Multiplying instead of dividing', 'A rate is a quotient: divide.'], ['Comparing different units', 'Change both to the same units first.']])
    faq = [('What does TEKS 7.4B ask?', 'Calculate unit rates from rates in mathematical and real-world problems.'), ('What is a complex fraction?', 'A fraction whose numerator or denominator is a fraction, like (1/2)/(1/4).'), ('How do I compare two rates?', 'Find both unit rates, then compare the numbers.'), ('Why is 1/2 ÷ 1/4 = 2?', 'Two quarters fit in one half.')]
    make('unit-rates-with-fractions', 6, 'Proportionality', '7.4B',
         '7.4B calculate unit rates from rates in mathematical and real-world problems',
         'Unit Rates with Fractions', 'Unit Rates with Fractions',
         'Free Grade 7 unit rate worksheets for Texas TEKS 7.4B: unit rates with fractions, complex fractions, comparing rates, mixed numbers and word problems. 100 questions with answers.',
         'Unit rate = first quantity ÷ second quantity.', '3/4 mile in 1/6 hour = 3/4 ÷ 1/6 = 4 1/2 mph.',
         body, faq, sets, seo_title='Grade 7 Unit Rates with Fractions Worksheets (TEKS 7.4B, STAAR)')


if __name__ == "__main__":
    build()
