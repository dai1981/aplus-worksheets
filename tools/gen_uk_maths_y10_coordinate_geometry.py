# -*- coding: utf-8 -*-
"""
UK Year 10 Maths (GCSE, KS4): Coordinate Geometry: Gradient, Length and Midpoint
  python3 tools/gen_uk_maths_y10_coordinate_geometry.py
Runs the question makers of gen_sg_maths_s3_coordinate_geometry with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_gcse import port

if __name__ == "__main__":
    port('gen_sg_maths_s3_coordinate_geometry', 91009, 10, 'coordinate-geometry', 9, 'A',
         'Use the form y = mx + c to identify parallel and perpendicular lines; find the equation of the line through two given points or through one point with a given gradient.',
         'Coordinate Geometry: Gradient, Length and Midpoint', 'Coordinate geometry',
         meta='Free Year 10 GCSE maths worksheets on gradient, length and midpoint of a line segment and the equation of a straight line. 100 questions with answers.',
         rep=[])
