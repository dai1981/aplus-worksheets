# -*- coding: utf-8 -*-
"""
Philippines Grade 4 Math (MATATAG): Properties of Triangles and Quadrilaterals (Grade 4: Measurement and Geometry)
  python3 tools/gen_ph_math_g4_triangles_quadrilaterals.py
Classifying triangles by sides and angles, and naming and telling apart squares, rectangles, rhombuses,
parallelograms, trapezoids and kites by their properties (UK Year 4, US Grade 3 and Grade 5 makers with Filipino names).
Wrong answers come from real mistakes: thinking a square is not a rectangle, mixing up isosceles and equilateral, and
calling every four-sided shape a rectangle.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_uk_maths_y4_angles_shapes as uka
adopt(uka)
if hasattr(uka, 'R'): uka.R = random.Random(704020)
import gen_us_math_g5_classify_figures as us5
adopt(us5)
if hasattr(us5, 'R'): us5.R = random.Random(704021)
import gen_us_math_g3_quadrilaterals as us3
adopt(us3)
if hasattr(us3, 'R'): us3.R = random.Random(704022)
ph_common.GRADE = "grade-4"



def build():
    sets, R = build_sets([
        ("Kinds of triangles", [("run", uka.set_triangles, ("rnd", uka.People), 20)]),
        ("Classify triangles by sides and angles", [("run", us5.set_triangles, ("rnd",), 20)]),
        ("Kinds of quadrilaterals", [("run", uka.set_quads, ("rnd", uka.People), 20)]),
        ("Properties of quadrilaterals", [("run", us3.set_attr, ("rnd",), 20)]),
        ("Tell quadrilaterals apart", [("run", us5.set_quads, ("rnd",), 20)]),
    ], 70402)
    finish(sets, R)
    body = lesson('<ul><li>Triangles by sides: <b>equilateral</b> (3 equal sides), <b>isosceles</b> (2 equal sides), <b>scalene</b> (no equal sides).</li><li>Triangles by angles: <b>right</b> (one 90° angle), <b>acute</b> (all angles less than 90°), <b>obtuse</b> (one angle more than 90°).</li><li>Quadrilaterals have 4 sides. A <b>parallelogram</b> has 2 pairs of parallel sides; a <b>trapezoid</b> has exactly 1 pair.</li><li>A <b>rectangle</b> has 4 right angles, a <b>rhombus</b> has 4 equal sides, and a <b>square</b> has both.</li></ul>',
        [example("Sides 5 cm, 5 cm, 8 cm", ["Two sides are equal"], "Isosceles triangle"), example("4 equal sides, no right angles", ["Opposite sides are parallel"], "Rhombus")],
        [['A square is not a rectangle', 'A square has 4 right angles, so it is a special rectangle.'], ['Mixing up isosceles and equilateral', 'Isosceles: at least 2 equal sides. Equilateral: all 3.'], ['Every 4-sided shape is a rectangle', 'Check the angles and parallel sides.']])
    faq = [('What does MATATAG Math 4 ask about triangles and quadrilaterals?', 'Draw and state the properties of triangles and quadrilaterals, classify triangles and quadrilaterals according to sides and angles, and differentiate different quadrilaterals.'), ('Can a triangle have two right angles?', 'No. The angles add to 180°.'), ('Is a square a rhombus?', 'Yes. It has 4 equal sides.'), ('What is the difference between a trapezoid and a parallelogram?', 'A trapezoid has exactly one pair of parallel sides; a parallelogram has two.')]
    make('triangles-and-quadrilaterals', 2, 'Measurement and Geometry', 'Grade 4: Measurement and Geometry',
         'Draw and state the properties of triangles and quadrilaterals; classify triangles and quadrilaterals according to sides and angles; differentiate different quadrilaterals.',
         'Properties of Triangles and Quadrilaterals', 'Triangles and Quadrilaterals',
         'Free Grade 4 worksheets on triangles and quadrilaterals for the DepEd MATATAG curriculum: classify triangles by sides and angles and tell squares, rectangles, rhombuses, parallelograms and trapezoids apart. 100 questions with answers.',
         'Classify triangles by sides and by angles.', 'A square is a rectangle and a rhombus.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
