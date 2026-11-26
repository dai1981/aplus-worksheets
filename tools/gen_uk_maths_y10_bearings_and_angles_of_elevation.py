# -*- coding: utf-8 -*-
"""
UK Year 10 Maths (GCSE, KS4): Bearings and Angles of Elevation and Depression
  python3 tools/gen_uk_maths_y10_bearings_and_angles_of_elevation.py
Runs the question makers of gen_sg_maths_s3_bearings_and_angles_of_elevation with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_gcse import port

if __name__ == "__main__":
    port('gen_sg_maths_s3_bearings_and_angles_of_elevation', 91016, 10, 'bearings-and-angles-of-elevation', 16, 'G',
         'Use trigonometric ratios in right-angled triangles to solve problems in two dimensions, including bearings and angles of elevation and depression.',
         'Bearings and Angles of Elevation and Depression', 'Bearings and elevation',
         meta='Free Year 10 GCSE maths worksheets on three-figure bearings and angles of elevation and depression. 100 questions with answers.',
         rep=[])
