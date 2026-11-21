# -*- coding: utf-8 -*-
"""India Class 4 Maths, Maths Mela Chapter 1: Shapes Around Us (2D Shapes, Polygons and Composite Shapes)
Polygons, regular and irregular shapes, sorting shapes and making shapes from other shapes (BC Grade 4 and AU Year 4 set makers)."""
from in_prim import unit, mod, rn, co, le

bc = mod("gen_cabc_math_g4_polygons", 604010)
cs = mod("gen_au_maths_y4_composite_shapes", 604011)
unit(4, "shapes-around-us", 1, "G", 1, "Shapes Around Us", "2D Shapes, Polygons and Composite Shapes", "shapes",
     "Shapes: identifying and describing 2D shapes and polygons, their sides and corners, and making shapes by combining others (summary of NCERT Maths Mela Class 4)",
     "Class 4 Shapes Around Us worksheet (Maths Mela Chapter 1): polygons, sides and corners, regular shapes and composite shapes. 100 questions with answers.",
     "Polygons are named by their number of sides.", "A regular polygon has equal sides and equal angles.",
     "<ul><li>Triangle 3 sides, quadrilateral 4, pentagon 5, hexagon 6, octagon 8.</li><li>A <b>regular</b> polygon has all sides and angles equal.</li><li>Shapes can be joined to make new shapes: two triangles can make a square.</li></ul>",
     [('Name a shape with 8 sides.', ['8 sides'], 'Octagon')],
     [['Calling a circle a polygon', 'A polygon has only straight sides.'], ['Thinking a shape must be upright', 'Turning a shape does not change its name.']],
     [('What is a polygon?', 'A closed flat shape made of straight sides.'), ('What is a regular polygon?', 'A polygon with all sides equal and all angles equal.')],
     [('Is it a polygon?', [rn(bc, "set_polygon", 20)]),
      ('Name the polygon', [rn(bc, "set_name", 20)]),
      ('Regular or irregular', [rn(bc, "set_regular", 20)]),
      ('Making shapes', [rn(cs, "set_make", 10), rn(cs, "set_count", 10)]),
      ('Shapes around us', [rn(bc, "set_life", 10), rn(cs, "set_objects", 10)])], 60401)
