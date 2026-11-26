# -*- coding: utf-8 -*-
"""
UK Year 10 Maths (GCSE, KS4): Algebraic Fractions: Simplifying, Multiplying and Adding
  python3 tools/gen_uk_maths_y10_algebraic_fractions.py
Runs the question makers of gen_sg_maths_s2_algebraic_fractions with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_gcse import port

if __name__ == "__main__":
    port('gen_sg_maths_s2_algebraic_fractions', 91004, 10, 'algebraic-fractions', 4, 'A',
         'Simplify and manipulate algebraic expressions involving algebraic fractions.',
         'Algebraic Fractions: Simplifying, Multiplying and Adding', 'Algebraic fractions',
         meta='Free Year 10 GCSE maths worksheets on simplifying algebraic fractions by factorising and multiplying, dividing, adding and subtracting them. 100 questions with answers.',
         rep=[])
