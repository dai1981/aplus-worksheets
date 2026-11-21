# -*- coding: utf-8 -*-
"""India Class 1 Maths, Joyful Mathematics Chapter 2: What is Long? What is Round? (Shapes)
Flat and solid shapes, rolling and sliding, sides and corners, shapes around us (UK Year 1, AU Year 1 and US Grade 1 set makers)."""
from in_prim import unit, mod, rn
uk = mod("gen_uk_maths_y1_shapes", 601021)
au = mod("gen_au_maths_y1_shapes", 601022)
us = mod("gen_us_math_g1_shapes", 601023)
unit(1, "what-is-long-what-is-round", 2, "G", 2, "What is Long? What is Round?", "2D and 3D Shapes", "shapes",
     "Shapes: observing and describing objects that are long, round, flat or curved; solid shapes that roll or slide; circles, triangles, squares and rectangles (summary of NCERT Joyful Mathematics Class 1)",
     "Class 1 What is Long? What is Round? worksheet (Joyful Mathematics Chapter 2): flat and solid shapes, roll or slide, sides and corners, shapes around us. 100 picture questions with answers.",
     "A ball is round and rolls; a box is flat-faced and slides.", "Count the sides and corners of a flat shape.",
     "<ul><li>Solid shapes: a <b>ball</b> (sphere) rolls, a <b>box</b> (cuboid) slides, a <b>can</b> (cylinder) rolls and slides.</li><li>Flat shapes: <b>circle</b>, <b>triangle</b> (3 sides), <b>square</b> and <b>rectangle</b> (4 sides).</li></ul>",
     [("How many sides does a triangle have?", ["Count the straight sides"], "3")],
     [["Calling a long rectangle a square", "A square has all 4 sides the same length."], ["Thinking a box can roll", "Flat faces slide; round shapes roll."]],
     [("What is the difference between flat and solid shapes?", "Flat shapes (circle, square) are drawn on paper; solid shapes (ball, box) can be held."), ("Which shapes roll?", "Round shapes such as a ball or the side of a can.")],
     [("Name the flat shape", [rn(uk, "set_name2d", 10), rn(au, "set_name2d", 10)]),
      ("Sides and corners", [rn(au, "set_sides", 20)]),
      ("Solid shapes", [rn(uk, "set_name3d", 12), rn(us, "set_solids", 8)]),
      ("Flat or solid?", [rn(uk, "set_flat_solid", 20)]),
      ("Shapes around us", [rn(uk, "set_world", 10), rn(au, "set_world", 10)])], 60102)
