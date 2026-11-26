# -*- coding: utf-8 -*-
"""
UK Year 10 Maths (GCSE, KS4): Standard Form: Writing and Calculating
  python3 tools/gen_uk_maths_y10_standard_form.py
Runs the question makers of gen_sg_maths_s3_standard_form with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_gcse import port

if __name__ == "__main__":
    port('gen_sg_maths_s3_standard_form', 91002, 10, 'standard-form', 2, 'N',
         'Calculate with and interpret standard form A × 10ⁿ, where 1 ≤ A < 10 and n is an integer.',
         'Standard Form: Writing and Calculating', 'Standard form',
         meta='Free Year 10 GCSE maths worksheets on writing large and small numbers in standard form and multiplying, dividing, adding and subtracting in standard form. 100 questions with answers.',
         rep=[('Singapore', 'Denmark')])
