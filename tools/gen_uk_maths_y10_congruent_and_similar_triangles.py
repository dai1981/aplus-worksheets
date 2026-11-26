# -*- coding: utf-8 -*-
"""
UK Year 10 Maths (GCSE, KS4): Congruent and Similar Triangles
  python3 tools/gen_uk_maths_y10_congruent_and_similar_triangles.py
Runs the question makers of gen_sg_maths_s3_congruent_and_similar_triangles with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_gcse import port

if __name__ == "__main__":
    port('gen_sg_maths_s3_congruent_and_similar_triangles', 91013, 10, 'congruent-and-similar-triangles', 13, 'G',
         'Use the basic congruence criteria for triangles (SSS, SAS, ASA, RHS); apply the concepts of congruence and similarity, including the relationships between lengths.',
         'Congruent and Similar Triangles', 'Congruent and similar triangles',
         meta='Free Year 10 GCSE maths worksheets on congruence conditions SSS, SAS, AAS and RHS and finding lengths in similar triangles. 100 questions with answers.',
         rep=[])
