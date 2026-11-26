# -*- coding: utf-8 -*-
"""
UK Year 10 Maths (GCSE, KS4): Area and Volume of Similar Shapes
  python3 tools/gen_uk_maths_y10_area_and_volume_of_similar_shapes.py
Runs the question makers of gen_sg_maths_s3_area_and_volume_of_similar_figures with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_gcse import port

if __name__ == "__main__":
    port('gen_sg_maths_s3_area_and_volume_of_similar_figures', 91014, 10, 'area-and-volume-of-similar-shapes', 14, 'G',
         'Understand the relationship between lengths, areas and volumes in similar figures.',
         'Area and Volume of Similar Shapes', 'Area and volume of similar shapes',
         meta='Free Year 10 GCSE maths worksheets on length, area and volume scale factors of similar shapes and solids. 100 questions with answers.',
         rep=[])
