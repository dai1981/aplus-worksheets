# -*- coding: utf-8 -*-
"""
UK Year 10 Maths (GCSE, KS4): Solving Quadratic Equations: Completing the Square and the Quadratic Formula
  python3 tools/gen_uk_maths_y10_solving_quadratic_equations.py
Runs the question makers of gen_sg_maths_s3_quadratic_formula_and_completing_the_square with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_gcse import port

if __name__ == "__main__":
    port('gen_sg_maths_s3_quadratic_formula_and_completing_the_square', 91005, 10, 'solving-quadratic-equations', 5, 'A',
         'Solve quadratic equations algebraically by factorising, by completing the square and by using the quadratic formula; find approximate solutions using a graph.',
         'Solving Quadratic Equations: Completing the Square and the Quadratic Formula', 'Solving quadratic equations',
         meta='Free Year 10 GCSE maths worksheets on completing the square, the quadratic formula and the discriminant. 100 questions with answers.',
         rep=[])
