# -*- coding: utf-8 -*-
"""
UK Year 10 Maths (GCSE, KS4): Equations with Algebraic Fractions
  python3 tools/gen_uk_maths_y10_equations_with_algebraic_fractions.py
Runs the question makers of gen_sg_maths_s3_fractional_equations with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_gcse import port

if __name__ == "__main__":
    port('gen_sg_maths_s3_fractional_equations', 91007, 10, 'equations-with-algebraic-fractions', 7, 'A',
         'Solve equations involving algebraic fractions, including those that lead to quadratic equations.',
         'Equations with Algebraic Fractions', 'Equations with fractions',
         meta='Free Year 10 GCSE maths worksheets on solving equations with algebraic fractions that lead to linear and quadratic equations. 100 questions with answers.',
         rep=[])
