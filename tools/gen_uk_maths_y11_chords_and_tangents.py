# -*- coding: utf-8 -*-
"""
UK Year 11 Maths (GCSE, KS4): Circle Theorems: Chords and Tangents
  python3 tools/gen_uk_maths_y11_chords_and_tangents.py
Runs the question makers of gen_sg_maths_s3_symmetry_properties_of_circles with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_gcse import port

if __name__ == "__main__":
    port('gen_sg_maths_s3_symmetry_properties_of_circles', 91107, 11, 'chords-and-tangents', 7, 'G',
         'Apply the standard circle theorems concerning radii, tangents and chords, and use them to prove related results.',
         'Circle Theorems: Chords and Tangents', 'Chords and tangents',
         meta='Free Year 11 GCSE maths worksheets on perpendicular bisectors of chords, tangents from an external point and radius–tangent angles. 100 questions with answers.',
         rep=[])
