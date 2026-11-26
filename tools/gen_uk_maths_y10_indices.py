# -*- coding: utf-8 -*-
"""
UK Year 10 Maths (GCSE, KS4): Indices: Negative and Fractional Indices
  python3 tools/gen_uk_maths_y10_indices.py
Runs the question makers of gen_sg_maths_s3_indices with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_gcse import port

if __name__ == "__main__":
    port('gen_sg_maths_s3_indices', 91001, 10, 'indices', 1, 'N',
         'Calculate with roots and with integer and fractional indices; apply the laws of indices.',
         'Indices: Negative and Fractional Indices', 'Indices',
         meta='Free Year 10 GCSE maths worksheets on laws of indices, zero, negative and fractional indices and index equations. 100 questions with answers.',
         rep=[])
