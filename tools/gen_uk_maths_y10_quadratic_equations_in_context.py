# -*- coding: utf-8 -*-
"""
UK Year 10 Maths (GCSE, KS4): Quadratic Equations in Context: Word Problems
  python3 tools/gen_uk_maths_y10_quadratic_equations_in_context.py
Runs the question makers of gen_sg_maths_s3_quadratic_equation_word_problems with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_gcse import port

if __name__ == "__main__":
    port('gen_sg_maths_s3_quadratic_equation_word_problems', 91006, 10, 'quadratic-equations-in-context', 6, 'A',
         'Translate simple situations or procedures into algebraic expressions or formulae; derive a quadratic equation, solve it and interpret the solution.',
         'Quadratic Equations in Context: Word Problems', 'Quadratic word problems',
         meta='Free Year 10 GCSE maths worksheets on forming and solving quadratic equations from area, number, speed and money problems. 100 questions with answers.',
         rep=[])
