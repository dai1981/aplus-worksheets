# -*- coding: utf-8 -*-
"""India Class 3 Maths, Maths Mela Chapter 5: Fun with Shapes (2D Shapes, Sides, Corners and Lines)
Flat shapes: names, sides and corners, quadrilaterals, straight and parallel lines (UK Year 3, US Grade 3 and SG Primary 3 set makers)."""
from in_prim import unit, mod, rn, co, le

uk = mod("gen_uk_maths_y3_shapes", 603050)
qu = mod("gen_us_math_g3_quadrilaterals", 603051)
ln = mod("gen_sg_maths_p3_lines", 603052)
unit(3, "fun-with-shapes", 5, "G", 5, "Fun with Shapes", "2D Shapes, Sides, Corners and Lines", "2D shapes",
     "2D shapes: identifying and describing triangles, squares, rectangles, circles and other shapes by their sides and corners; making shapes; straight lines (summary of NCERT Maths Mela Class 3)",
     "Class 3 Fun with Shapes worksheet (Maths Mela Chapter 5): triangles, squares, rectangles and other shapes, sides, corners and lines. 100 questions with answers.",
     "Name a shape by counting its sides.", "A quadrilateral has 4 sides.",
     "<ul><li>3 sides: triangle. 4 sides: quadrilateral (square, rectangle …). 5 sides: pentagon. 6 sides: hexagon.</li><li>A square has 4 equal sides and 4 right angles.</li></ul>",
     [('A shape has 6 straight sides. What is it?', ['6 sides'], 'A hexagon')],
     [['Thinking a turned square is not a square', 'Turning a shape does not change it.'], ['Counting a curved edge as a side', 'Sides are straight.']],
     [('What is a quadrilateral?', 'Any flat shape with 4 straight sides.'), ('Is a square a rectangle?', 'Yes: it has 4 right angles, and its sides are all equal.')],
     [('Name the shape', [rn(uk, "set_2d", 20)]),
      ('Quadrilaterals', [rn(qu, "set_is_quad", 10), rn(qu, "set_name", 10)]),
      ('Sides and corners', [rn(qu, "set_attr", 20)]),
      ('Lines in shapes', [rn(ln, "set_shapes", 10), rn(ln, "set_par", 10)]),
      ('Shape problems', [rn(uk, "set_problems", 20)])], 60305)
