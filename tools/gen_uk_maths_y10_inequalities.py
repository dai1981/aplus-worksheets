# -*- coding: utf-8 -*-
"""
UK Year 10 Maths (GCSE, KS4): Linear Inequalities and Simultaneous Inequalities
  python3 tools/gen_uk_maths_y10_inequalities.py
Runs the question makers of gen_sg_maths_s3_simultaneous_linear_inequalities with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_gcse import port

if __name__ == "__main__":
    port('gen_sg_maths_s3_simultaneous_linear_inequalities', 91008, 10, 'inequalities', 8, 'A',
         'Solve linear inequalities in one variable; represent the solution set on a number line and using set notation.',
         'Linear Inequalities and Simultaneous Inequalities', 'Inequalities',
         meta='Free Year 10 GCSE maths worksheets on solving linear inequalities, number lines and pairs of inequalities. 100 questions with answers.',
         rep=[])
