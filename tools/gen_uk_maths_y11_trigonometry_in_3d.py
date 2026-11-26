# -*- coding: utf-8 -*-
"""
UK Year 11 Maths (GCSE, KS4): Pythagoras and Trigonometry in 3D
  python3 tools/gen_uk_maths_y11_trigonometry_in_3d.py
Runs the question makers of gen_sg_maths_s4_problems_in_three_dimensions with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_gcse import port

if __name__ == "__main__":
    port('gen_sg_maths_s4_problems_in_three_dimensions', 91110, 11, 'trigonometry-in-3d', 10, 'G',
         "Apply Pythagoras' theorem and trigonometric ratios to find angles and lengths in right-angled triangles in three-dimensional figures.",
         'Pythagoras and Trigonometry in 3D', 'Trigonometry in 3D',
         meta='Free Year 11 GCSE maths worksheets on lengths of diagonals and angles between lines and planes in cuboids and pyramids. 100 questions with answers.',
         rep=[])
