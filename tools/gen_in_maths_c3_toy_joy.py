# -*- coding: utf-8 -*-
"""India Class 3 Maths, Maths Mela Chapter 2: Toy Joy (3D Shapes and Nets)
Solid shapes in toys: names, faces, edges and vertices, nets and real objects (BC Grade 3 and UK Year 3 set makers)."""
from in_prim import unit, mod, rn, co, le

bc = mod("gen_cabc_math_g3_3d_objects", 603020)
uk = mod("gen_uk_maths_y3_shapes", 603021)
unit(3, "toy-joy", 2, "G", 2, "Toy Joy", "3D Shapes and Nets", "3D shapes",
     "3D shapes: identifying cubes, cuboids, cylinders, cones and spheres in toys; faces, edges and corners; nets of a cube and cuboid (summary of NCERT Maths Mela Class 3)",
     "Class 3 Toy Joy worksheet (Maths Mela Chapter 2): cubes, cuboids, cylinders, cones and spheres, faces, edges, corners and nets. 100 questions with answers.",
     "Faces, edges and corners describe a solid.", "A cube has 6 faces, 12 edges and 8 corners.",
     "<ul><li>A <b>face</b> is a flat surface, an <b>edge</b> is where two faces meet, a <b>corner</b> (vertex) is where edges meet.</li><li>A <b>net</b> is the flat shape that folds into a solid.</li></ul>",
     [('How many faces does a cuboid have?', ['Top, bottom, front, back, left, right'], '6')],
     [['Counting only the faces you can see', 'Remember the hidden faces at the back and bottom.'], ['Calling a cube a square', 'A square is flat; a cube is solid.']],
     [('What is a net?', 'A flat pattern that can be folded to make a solid shape.'), ('How many corners does a cube have?', '8.')],
     [('Name the solid', [rn(bc, "set_name", 20)]),
      ('Faces, edges and corners', [rn(bc, "set_fev", 12), rn(uk, "set_fev", 8)]),
      ('Nets', [rn(bc, "set_nets", 20)]),
      ('Skeletons', [rn(bc, "set_skeletons", 20)]),
      ('Toys and real things', [rn(bc, "set_real", 12), rn(uk, "set_name3d", 8)])], 60302)
