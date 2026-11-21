# -*- coding: utf-8 -*-
"""India Class 2 Maths, Joyful Mathematics Chapter 4: Shadow Story (2D Shapes)
Flat shapes as the faces and shadows of solids: names, sides and corners, curved and straight edges (AU Year 2, UK Year 2, Ontario and SG set makers)."""
from in_prim import unit, mod, rn
au = mod("gen_au_maths_y2_shapes", 602041)
uk = mod("gen_uk_maths_y2_shapes", 602042)
ca = mod("gen_caon_math_g2_shapes", 602043)
sg = mod("gen_sg_maths_p2_3d_shapes", 602044)
unit(2, "shadow-story", 4, "G", 4, "Shadow Story", "2D Shapes", "2D shapes",
     "2D shapes: recognising flat shapes such as circles, triangles, squares and rectangles as the faces and shadows of 3D objects; sides, corners and curved edges (summary of NCERT Joyful Mathematics Class 2)",
     "Class 2 Shadow Story worksheet (Joyful Mathematics Chapter 4): circles, triangles, squares and rectangles, sides and corners, faces of solids. 100 picture questions with answers.",
     "The shadow or face of a solid is a flat shape.", "Count sides and corners to name a shape.",
     "<ul><li>The face of a cube is a <b>square</b>; the bottom of a cylinder is a <b>circle</b>.</li><li>A triangle has 3 sides and 3 corners; a rectangle has 4 sides and 4 corners.</li></ul>",
     [("What shape is the bottom of a tin?", ["Trace it on paper"], "Circle")],
     [["Calling every 4-sided shape a square", "A square has 4 equal sides."], ["Counting a curved edge as a side", "Sides are straight."]],
     [("How are 2D and 3D shapes linked?", "The faces of solid shapes are flat 2D shapes."), ("What is a corner?", "A point where two sides meet.")],
     [("Name the shape", [rn(au, "set_names", 10), rn(uk, "set_2d", 10)]),
      ("Sides and corners", [rn(au, "set_count", 20)]),
      ("Curved or straight", [rn(au, "set_curved", 20)]),
      ("Faces of solids", [rn(sg, "set_faces", 10), rn(ca, "set_names", 10)]),
      ("Shape problems", [rn(au, "set_problems", 20)])], 60204)
