# -*- coding: utf-8 -*-
"""
UK Year 10 Maths (GCSE, KS4): The Sine Rule, the Cosine Rule and Area of a Triangle
  python3 tools/gen_uk_maths_y10_sine_and_cosine_rules.py
Runs the question makers of gen_sg_maths_s3_sine_and_cosine_rules with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_gcse import port

if __name__ == "__main__":
    port('gen_sg_maths_s3_sine_and_cosine_rules', 91015, 10, 'sine-and-cosine-rules', 15, 'G',
         'Know and apply the sine rule and the cosine rule to find unknown lengths and angles; know and apply Area = ½ab sin C.',
         'The Sine Rule, the Cosine Rule and Area of a Triangle', 'Sine and cosine rules',
         meta='Free Year 10 GCSE maths worksheets on the sine rule, the cosine rule and area = ½ab sin C. 100 questions with answers.',
         rep=[])
