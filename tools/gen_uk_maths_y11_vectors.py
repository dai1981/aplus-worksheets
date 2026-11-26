# -*- coding: utf-8 -*-
"""
UK Year 11 Maths (GCSE, KS4): Vectors: Column Vectors and Magnitude
  python3 tools/gen_uk_maths_y11_vectors.py
Runs the question makers of gen_sg_maths_s4_vectors with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_gcse import port

if __name__ == "__main__":
    port('gen_sg_maths_s4_vectors', 91108, 11, 'vectors', 8, 'G',
         'Describe translations as 2D vectors; apply addition and subtraction of vectors, multiplication of vectors by a scalar, and diagrammatic and column representations of vectors.',
         'Vectors: Column Vectors and Magnitude', 'Vectors',
         meta='Free Year 11 GCSE maths worksheets on column vectors, adding and subtracting vectors, scalar multiples and magnitude. 100 questions with answers.',
         rep=[])
