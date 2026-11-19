# -*- coding: utf-8 -*-
"""
Texas Kindergarten Math: 2D Shapes: Circles, Triangles, Rectangles and Squares (TEKS K.6A, K.6D, K.6E, K.6F)
  python3 tools/gen_ustx_math_gk_shapes_2d.py
Naming flat shapes, sides and corners, shapes around us, shapes inside shapes, and making bigger shapes (the US
Kindergarten makers with Texas names).
Wrong answers come from real mistakes: naming a shape by its color or size, and thinking a turned square is not a square.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_gk_2d_and_3d_shapes as sh
adopt(sh)
import gen_us_math_gk_build_and_compose_shapes as bc
adopt(bc)
tx_common.GRADE = "kindergarten"



def build():
    sets, R = build_sets([
        ("Name the flat shape", [("run", sh.set_flat, ("rnd", sh.Kids), 20)]),
        ("Sides and corners", [("run", sh.set_sides, ("rnd", sh.Kids), 20)]),
        ("Shapes inside shapes", [("run", bc.set_parts, ("rnd", bc.Kids), 20)]),
        ("Shapes around us", [("run", sh.set_around, ("rnd", sh.Kids), 20)]),
        ("Make a bigger shape", [("run", bc.set_big, ("rnd", bc.Kids), 20)]),
    ], 69012)
    finish(sets, R)
    body = lesson("<ul><li><b>Circle</b>: round, no sides, no corners.</li><li><b>Triangle</b>: 3 sides, 3 corners.</li><li><b>Rectangle</b>: 4 sides, 4 square corners. A <b>square</b> is a rectangle with 4 equal sides.</li><li>Size, color and turning do not change a shape's name.</li></ul>",
        [example("3 sides and 3 corners", ["count the sides"], "triangle")],
        [['Naming a shape by color or size', 'A small red triangle is still a triangle.'], ['Thinking a turned square is not a square', 'Turning does not change the shape.'], ['Counting a corner twice', 'Start at one corner and go around.']])
    faq = [('What does TEKS K.6A ask?', 'Identify two-dimensional shapes, including circles, triangles, rectangles, and squares as special rectangles.'), ('What does TEKS K.6D ask?', 'Identify attributes of two-dimensional shapes using informal and formal geometric language interchangeably.'), ('What does TEKS K.6E ask?', 'Classify and sort a variety of regular and irregular two- and three-dimensional figures regardless of orientation or size.'), ('What does TEKS K.6F ask?', 'Create two-dimensional shapes using a variety of materials and drawings.')]
    make('2d-shapes', 12, 'Geometry and Measurement', 'K.6A, K.6D, K.6E, K.6F',
         'K.6A identify two-dimensional shapes, including circles, triangles, rectangles, and squares as special rectangles; K.6D identify attributes of two-dimensional shapes using informal and formal geometric language interchangeably; K.6E classify and sort a variety of regular and irregular two- and three-dimensional figures regardless of orientation or size; K.6F create two-dimensional shapes using a variety of materials and drawings',
         '2D Shapes: Circles, Triangles, Rectangles and Squares', '2D Shapes',
         'Free kindergarten 2D shape worksheets for Texas TEKS K.6A, K.6D, K.6E and K.6F: circles, triangles, rectangles and squares, sides and corners, and making shapes. 100 questions with answers.',
         'Count the sides and corners to name a shape.', 'A square is a special rectangle.',
         body, faq, sets, seo_title='Kindergarten 2D Shapes Worksheets (TEKS K.6A)')


if __name__ == "__main__":
    build()
