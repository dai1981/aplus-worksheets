# -*- coding: utf-8 -*-
"""
UK Year 11 Maths (GCSE, KS4): Circle Theorems: Angles in Circles
  python3 tools/gen_uk_maths_y11_circle_theorems.py
Runs the question makers of gen_sg_maths_s3_angle_properties_of_circles with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_gcse import port

if __name__ == "__main__":
    port('gen_sg_maths_s3_angle_properties_of_circles', 91106, 11, 'circle-theorems', 6, 'G',
         'Apply and prove the standard circle theorems concerning angles, radii, tangents and chords.',
         'Circle Theorems: Angles in Circles', 'Circle theorems',
         meta='Free Year 11 GCSE maths worksheets on angle at the centre, angles in the same segment, angle in a semicircle and cyclic quadrilaterals. 100 questions with answers.',
         rep=[])
