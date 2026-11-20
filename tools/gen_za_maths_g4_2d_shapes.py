# -*- coding: utf-8 -*-
"""
South Africa Grade 4 Maths (CAPS): 2-D Shapes: Polygons, Circles and Angles (Grade 4: 3.1 Properties of 2-D shapes)
  python3 tools/gen_za_maths_g4_2d_shapes.py
Naming polygons and circles, regular and irregular polygons, sorting shapes by straight and curved sides (BC Grade
4 makers), and right angles, angles smaller and bigger than a right angle (UK Year 4 and Australia Year 4 makers).
Wrong answers come from real mistakes: thinking a turned shape has a new name, calling a polygon regular when only
its sides are equal, and judging an angle by the length of its arms.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_cabc_math_g4_polygons as cbp
adopt(cbp)
if hasattr(cbp, 'R'): cbp.R = random.Random(804150)
import gen_uk_maths_y4_angles_shapes as uka
adopt(uka)
if hasattr(uka, 'R'): uka.R = random.Random(804151)
import gen_au_maths_y4_angles as aua
adopt(aua)
if hasattr(aua, 'R'): aua.R = random.Random(804152)
za_common.GRADE = "grade-4"



def build():
    sets, R = build_sets([
        ("Is it a polygon?", [("run", cbp.set_polygon, ("rnd", cbp.Pos, cbp.People), 20)]),
        ("Name the polygon", [("run", cbp.set_name, ("rnd", cbp.Pos, cbp.People), 20)]),
        ("Regular and irregular polygons", [("run", cbp.set_regular, ("rnd", cbp.Pos, cbp.People), 20)]),
        ("Right angles", [("run", uka.set_kinds, ("rnd", uka.People), 20)]),
        ("Compare angles", [("run", aua.set_compare, ("rnd", aua.People), 20)]),
    ], 80415)
    finish(sets, R)
    body = lesson('<ul><li>A <b>polygon</b> is a closed 2-D shape with straight sides: triangle (3), quadrilateral (4), pentagon (5), hexagon (6), heptagon (7), octagon (8).</li><li>A <b>circle</b> has one curved side and no corners.</li><li>A <b>regular</b> polygon has equal sides and equal angles.</li><li>Compare angles with a right angle (the corner of a page): smaller than a right angle, a right angle, or bigger than a right angle.</li></ul>',
        [example("A shape with 6 straight sides", ["count the sides: 6"], "hexagon")],
        [['A turned shape', 'Turning does not change the name.'], ['Equal sides only', 'Regular needs equal angles too.'], ['Long arms, big angle', 'The size of an angle is the turn, not the arm length.']])
    faq = [('What does CAPS Grade 4 say about 2-D shapes?', 'Recognise, visualise and name regular and irregular polygons (triangles, squares, rectangles, other quadrilaterals, pentagons, hexagons, heptagons) and circles; describe, sort and compare them by straight and curved sides and number of sides; recognise right angles and angles smaller and greater than a right angle.'), ('Is a circle a polygon?', 'No. It has a curved side.'), ('What is a heptagon?', 'A polygon with 7 sides.'), ('How can learners check a right angle?', 'Use the corner of a page.')]
    make('2d-shapes-and-angles', 15, 'Space and Shape (Geometry)', 'Grade 4: 3.1 Properties of 2-D shapes',
         'Recognise, visualise and name 2-D shapes in the environment and geometric settings: regular and irregular polygons (triangles, squares, rectangles, other quadrilaterals, pentagons, hexagons, heptagons) and circles; describe, sort and compare 2-D shapes in terms of straight and curved sides and number of sides; recognise and describe right angles, and angles bigger or smaller than right angles.',
         '2-D Shapes: Polygons, Circles and Angles', '2-D Shapes and Angles',
         'Free CAPS Grade 4 2-D shapes worksheets: polygons and circles, regular and irregular polygons, right angles and comparing angles. 100 questions with memos.',
         'Count the straight sides to name a polygon.', 'Compare angles with a right angle.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
