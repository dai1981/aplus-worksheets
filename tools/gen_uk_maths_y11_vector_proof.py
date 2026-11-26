# -*- coding: utf-8 -*-
"""
UK Year 11 Maths (GCSE, KS4): Vector Geometry and Proof
  python3 tools/gen_uk_maths_y11_vector_proof.py
Runs the question makers of gen_sg_maths_s4_vector_geometry with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_gcse import port

if __name__ == "__main__":
    port('gen_sg_maths_s4_vector_geometry', 91109, 11, 'vector-proof', 9, 'G',
         'Use vectors to construct geometric arguments and proofs.',
         'Vector Geometry and Proof', 'Vector proof',
         meta='Free Year 11 GCSE maths worksheets on writing vectors in terms of a and b, midpoints, ratios and proving lines are parallel. 100 questions with answers.',
         rep=[])
