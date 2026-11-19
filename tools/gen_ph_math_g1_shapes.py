# -*- coding: utf-8 -*-
"""
Philippines Grade 1 Math (MATATAG): 2D Shapes: Triangles, Rectangles and Squares (Grade 1: Measurement and Geometry)
  python3 tools/gen_ph_math_g1_shapes.py
Naming triangles, rectangles, squares and circles of different sizes and in different positions, counting sides and
corners, and sorting shapes (Australia Year 1, Singapore Primary 1 and US Grade 1 makers with Filipino names).
Wrong answers come from real mistakes: thinking a turned square is not a square, counting a corner twice, and
mixing up a square and a rectangle.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_au_maths_y1_shapes as aus
adopt(aus)
if hasattr(aus, 'R'): aus.R = random.Random(701010)
import gen_sg_maths_p1_2d_shapes as sgs
adopt(sgs)
if hasattr(sgs, 'R'): sgs.R = random.Random(701011)
import gen_us_math_g1_shapes as uss
adopt(uss)
if hasattr(uss, 'R'): uss.R = random.Random(701012)
ph_common.GRADE = "grade-1"



def build():
    sets, R = build_sets([
        ("Name the shape", [("run", aus.set_name2d, ("rnd", aus.Pos), 20)]),
        ("Shapes in any size and position", [("run", sgs.set_name, ("rnd", sgs.Pos), 20)]),
        ("Sides and corners", [("run", aus.set_sides, ("rnd", aus.Pos, aus.People), 20)]),
        ("Count the shapes", [("run", uss.set_count, ("rnd", uss.People), 20)]),
        ("Sort the shapes", [("run", aus.set_sort, ("rnd", aus.Pos, aus.People), 20)]),
    ], 70101)
    finish(sets, R)
    body = lesson('<ul><li>A <b>triangle</b> has 3 sides and 3 corners.</li><li>A <b>rectangle</b> has 4 sides and 4 square corners.</li><li>A <b>square</b> is a rectangle with 4 sides of the same length.</li><li>A shape keeps its name when it is big or small, or turned.</li></ul>',
        [example("A shape with 3 sides", ["count the sides: 3", "count the corners: 3"], "triangle")],
        [['A turned square', 'It is still a square.'], ['Counting a corner twice', 'Mark each corner as you count.'], ['Square or rectangle?', 'A square has 4 equal sides.']])
    faq = [('What does MATATAG Math 1 ask about shapes?', 'Identify simple 2-dimensional shapes (triangle, rectangle, square) of different size and in different orientation, and compare and distinguish them by sides and corners.'), ('Is a square a rectangle?', 'Yes. It is a special rectangle.'), ('Does a circle have corners?', 'No.'), ('Where can I find rectangles?', 'Doors, books and the blackboard.')]
    make('2d-shapes', 1, 'Measurement and Geometry', 'Grade 1: Measurement and Geometry',
         'Identify simple 2-dimensional shapes (triangle, rectangle, square) of different size and in different orientation; compare and distinguish 2-dimensional shapes according to features such as sides and corners.',
         '2D Shapes: Triangles, Rectangles and Squares', '2D Shapes',
         'Free Grade 1 shapes worksheets for the DepEd MATATAG curriculum: triangles, rectangles, squares and circles, sides and corners, and sorting shapes. 100 questions with pictures and answers.',
         'Count the sides and the corners.', 'A turned shape keeps its name.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
