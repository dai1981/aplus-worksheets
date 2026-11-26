# -*- coding: utf-8 -*-
"""
UK Year 10 Maths (GCSE, KS4): Surds: Simplifying and Rationalising
  python3 tools/gen_uk_maths_y10_surds.py
Runs the question makers of gen_us_math_a1_simplifying_radicals with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_gcse import port

if __name__ == "__main__":
    port('gen_us_math_a1_simplifying_radicals', 91003, 10, 'surds', 3, 'N',
         'Calculate exactly with surds; simplify surd expressions involving squares and rationalise denominators.',
         'Surds: Simplifying and Rationalising', 'Surds',
         meta='Free Year 10 GCSE maths worksheets on simplifying surds, multiplying and adding surds and rationalising the denominator. 100 questions with answers.',
         rep=[('radicals', 'surds'), ('radical', 'surd'), ('Radicals', 'Surds'), ('Radical', 'Surd')])
