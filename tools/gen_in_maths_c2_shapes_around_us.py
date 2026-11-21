# -*- coding: utf-8 -*-
"""India Class 2 Maths, Joyful Mathematics Chapter 2: Shapes Around Us (3D Shapes)
Names of solid shapes, shapes in real things, faces, roll or slide, sorting (Singapore Primary 2 and UK Year 2 set makers)."""
from in_prim import unit, mod, rn
sg = mod("gen_sg_maths_p2_3d_shapes", 602021)
uk = mod("gen_uk_maths_y2_shapes", 602022)
unit(2, "shapes-around-us", 2, "G", 2, "Shapes Around Us", "3D Shapes", "3D shapes",
     "3D shapes: identifying cubes, cuboids, cylinders, cones and spheres in the surroundings, their faces, and which roll or slide (summary of NCERT Joyful Mathematics Class 2)",
     "Class 2 Shapes Around Us worksheet (Joyful Mathematics Chapter 2): cube, cuboid, cylinder, cone and sphere, real objects, faces, roll or slide. 100 picture questions with answers.",
     "Cube, cuboid, cylinder, cone, sphere.", "Round shapes roll; flat faces slide.",
     "<ul><li>A dice is a <b>cube</b>; a brick is a <b>cuboid</b>; a tin is a <b>cylinder</b>; a party hat is a <b>cone</b>; a ball is a <b>sphere</b>.</li><li>A cube has 6 square faces.</li></ul>",
     [("What shape is a matchbox?", ["It has 6 rectangle faces"], "Cuboid")],
     [["Calling a cube a square", "A square is flat; a cube is solid."], ["Thinking a cone cannot roll", "A cone rolls round in a circle on its curved side."]],
     [("What are 3D shapes?", "Solid shapes with length, width and height, such as a cube or a ball."), ("How many faces does a cube have?", "6 square faces.")],
     [("Name the solid", [rn(sg, "set_name", 20)]),
      ("Shapes in real things", [rn(sg, "set_real", 20)]),
      ("Faces", [rn(sg, "set_faces", 12), rn(uk, "set_faces", 8)]),
      ("Roll or slide?", [rn(sg, "set_roll", 20)]),
      ("Sorting solids", [rn(sg, "set_sort", 10), rn(uk, "set_3d", 10)])], 60202)
