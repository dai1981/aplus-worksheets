# -*- coding: utf-8 -*-
"""
UK Year 10 Maths (GCSE, KS4): Direct and Inverse Proportion
  python3 tools/gen_uk_maths_y10_direct_and_inverse_proportion.py
Runs the question makers of gen_sg_maths_s2_direct_and_inverse_proportion with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_gcse import port

if __name__ == "__main__":
    port('gen_sg_maths_s2_direct_and_inverse_proportion', 91012, 10, 'direct-and-inverse-proportion', 12, 'R',
         'Solve problems involving direct and inverse proportion, including graphical and algebraic representations.',
         'Direct and Inverse Proportion', 'Direct and inverse proportion',
         meta='Free Year 10 GCSE maths worksheets on direct and inverse proportion, y = kx and y = k/x, and proportion problems. 100 questions with answers.',
         rep=[('S$1 = RM3.50. How many ringgit do you get for S$40?', '1 kg of nuts costs £3.50. How much do 40 kg cost?'), ('RM', '£')])
