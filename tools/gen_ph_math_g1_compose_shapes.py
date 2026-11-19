# -*- coding: utf-8 -*-
"""
Philippines Grade 1 Math (MATATAG): Putting Shapes Together and Taking Them Apart (Grade 1: Measurement and Geometry)
  python3 tools/gen_ph_math_g1_compose_shapes.py
Making new shapes from triangles, squares and rectangles, finding the shapes in a figure, cutting shapes into
halves, and shapes on a dot grid (US Grade 1 and Singapore Primary 1 makers).
Wrong answers come from real mistakes: counting only the small shapes, thinking color or size changes the shape,
and cutting into parts that are not the same.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g1_shapes as uss
adopt(uss)
if hasattr(uss, 'R'): uss.R = random.Random(701020)
import gen_sg_maths_p1_2d_shapes as sgs
adopt(sgs)
if hasattr(sgs, 'R'): sgs.R = random.Random(701021)
ph_common.GRADE = "grade-1"



def build():
    sets, R = build_sets([
        ("Put shapes together", [("run", uss.set_compose, ("rnd", uss.People), 20)]),
        ("Shapes in a figure", [("run", sgs.set_figures, ("rnd", sgs.Pos, sgs.People), 20)]),
        ("Cut a shape into two", [("run", sgs.set_halves, ("rnd", sgs.Pos, sgs.People), 20)]),
        ("Shapes on a dot grid", [("run", sgs.set_dotgrid, ("rnd", sgs.Pos, sgs.People), 20)]),
        ("What makes a shape?", [("run", uss.set_matters, ("rnd", uss.People), 20)]),
    ], 70102)
    finish(sets, R)
    body = lesson('<ul><li>Two triangles can make a square or a rectangle.</li><li>Two squares side by side make a rectangle.</li><li>A rectangle can be cut into 2 squares or 2 triangles.</li><li>Color and size do not change the name of a shape. Sides and corners do.</li></ul>',
        [example("Two triangles", ["put the long sides together"], "a square")],
        [['Only the small shapes', 'Look for big shapes too.'], ['Color changes the shape', 'A red square is still a square.'], ['Parts that are not the same', 'Halves must match.']])
    faq = [('What does MATATAG Math 1 ask about composing shapes?', 'Compose and decompose triangles, squares, and rectangles.'), ('What shapes make a square?', 'Two triangles, or four small squares.'), ('Can I make a triangle from two triangles?', 'Yes, if they are the right shape.'), ('Why play with tangram pieces?', 'They help children see shapes inside shapes.')]
    make('composing-and-decomposing-shapes', 2, 'Measurement and Geometry', 'Grade 1: Measurement and Geometry',
         'Compose and decompose triangles, squares, and rectangles.',
         'Putting Shapes Together and Taking Them Apart', 'Composing Shapes',
         'Free Grade 1 worksheets on composing and decomposing shapes for the DepEd MATATAG curriculum: put triangles, squares and rectangles together and take them apart. 100 questions with pictures and answers.',
         'Two triangles can make a square.', "Color and size do not change a shape's name.",
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
