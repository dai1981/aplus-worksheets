# -*- coding: utf-8 -*-
"""
UK Year 10 Maths (GCSE, KS4): Quadratic Graphs: Roots, Intercepts and Turning Points
  python3 tools/gen_uk_maths_y10_quadratic_graphs_and_turning_points.py
Runs the question makers of gen_sg_maths_s3_sketching_quadratic_graphs with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_gcse import port

if __name__ == "__main__":
    port('gen_sg_maths_s3_sketching_quadratic_graphs', 91010, 10, 'quadratic-graphs-and-turning-points', 10, 'A',
         'Identify and interpret roots, intercepts and turning points of quadratic functions graphically; deduce turning points by completing the square.',
         'Quadratic Graphs: Roots, Intercepts and Turning Points', 'Quadratic graphs',
         meta='Free Year 10 GCSE maths worksheets on sketching quadratic graphs, roots, intercepts, line of symmetry and turning points. 100 questions with answers.',
         rep=[])
