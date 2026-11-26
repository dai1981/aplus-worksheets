# -*- coding: utf-8 -*-
"""
UK Year 11 Maths (GCSE, KS4): Exponential Growth and Decay
  python3 tools/gen_uk_maths_y11_exponential_growth_and_decay.py
Runs the question makers of gen_us_math_a1_exponential_growth_and_decay with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_gcse import port

if __name__ == "__main__":
    port('gen_us_math_a1_exponential_growth_and_decay', 91104, 11, 'exponential-growth-and-decay', 4, 'R',
         'Set up, solve and interpret the answers in growth and decay problems, including compound interest, and work with general iterative processes.',
         'Exponential Growth and Decay', 'Exponential growth and decay',
         meta='Free Year 11 GCSE maths worksheets on exponential growth and decay, multipliers, half-life and doubling. 100 questions with answers.',
         rep=[('1¢', '1p'), (' ft', ' m'), (' feet', ' m'), ('3 gallons', '3 litres'), ('per mile', 'per km')])
