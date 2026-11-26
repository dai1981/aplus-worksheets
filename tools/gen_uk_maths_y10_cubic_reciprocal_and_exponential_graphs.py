# -*- coding: utf-8 -*-
"""
UK Year 10 Maths (GCSE, KS4): Cubic, Reciprocal and Exponential Graphs
  python3 tools/gen_uk_maths_y10_cubic_reciprocal_and_exponential_graphs.py
Runs the question makers of gen_sg_maths_s3_power_and_exponential_graphs with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_gcse import port

if __name__ == "__main__":
    port('gen_sg_maths_s3_power_and_exponential_graphs', 91011, 10, 'cubic-reciprocal-and-exponential-graphs', 11, 'A',
         'Recognise, sketch and interpret graphs of linear, quadratic, cubic and reciprocal functions and exponential functions y = kˣ.',
         'Cubic, Reciprocal and Exponential Graphs', 'Cubic, reciprocal and exponential graphs',
         meta='Free Year 10 GCSE maths worksheets on recognising and reading graphs of cubic, reciprocal and exponential functions. 100 questions with answers.',
         rep=[])
