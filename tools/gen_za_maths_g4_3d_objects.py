# -*- coding: utf-8 -*-
"""
South Africa Grade 4 Maths (CAPS): 3-D Objects: Prisms, Pyramids, Spheres and Cylinders (Grade 4: 3.2 Properties of 3-D objects)
  python3 tools/gen_za_maths_g4_3d_objects.py
Naming rectangular prisms, cubes, spheres, cylinders, cones and pyramids, faces, edges and vertices, flat and curved
surfaces, sorting and problems (Australia Year 3 makers with South African names).
Wrong answers come from real mistakes: mixing up a cylinder and a cone, counting hidden faces wrongly, and calling a
curved surface a face.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y3_objects as auo
adopt(auo)
if hasattr(auo, 'R'): auo.R = random.Random(804160)
za_common.GRADE = "grade-4"



def build():
    sets, R = build_sets([
        ("Name the 3-D object", [("run", auo.set_name, ("rnd", auo.Pos), 20)]),
        ("Faces, edges and vertices", [("run", auo.set_fev, ("rnd",), 20)]),
        ("Flat and curved surfaces", [("run", auo.set_surfaces, ("rnd", auo.Pos, auo.People), 20)]),
        ("Sort 3-D objects", [("run", auo.set_classify, ("rnd", auo.Pos), 20)]),
        ("3-D object problems", [("run", auo.set_problems, ("rnd", auo.People), 20)]),
    ], 80416)
    finish(sets, R)
    body = lesson('<ul><li>A <b>rectangular prism</b> (like a box) has 6 flat faces. A <b>cube</b> is a prism with 6 equal square faces.</li><li>A <b>pyramid</b> has a base and triangular faces that meet at a point.</li><li>A <b>sphere</b> (ball) has one curved surface. A <b>cylinder</b> (tin) has 2 flat faces and 1 curved surface.</li><li>Faces meet at <b>edges</b>; edges meet at <b>vertices</b> (corners).</li></ul>',
        [example("A box of cereal", ["6 rectangular faces"], "rectangular prism")],
        [['Cylinder or cone?', 'A cone has 1 flat face and a point.'], ['Hidden faces', 'Count the faces you cannot see too.'], ['Curved surface as a face', 'Faces are flat.']])
    faq = [('What does CAPS Grade 4 say about 3-D objects?', 'Recognise, visualise and name rectangular prisms, spheres, cylinders and pyramids, and describe, sort and compare them by the shape of faces and flat and curved surfaces.'), ('How many faces does a cube have?', '6.'), ('Does a sphere have edges?', 'No.'), ('Where are cylinders found?', 'Tins, pipes and candles.')]
    make('3d-objects', 16, 'Space and Shape (Geometry)', 'Grade 4: 3.2 Properties of 3-D objects',
         'Recognise, visualise and name 3-D objects in the environment and geometric settings: rectangular prisms and other prisms, spheres, cylinders, pyramids; describe, sort and compare 3-D objects in terms of shape of faces and flat and curved surfaces.',
         '3-D Objects: Prisms, Pyramids, Spheres and Cylinders', '3-D Objects',
         'Free CAPS Grade 4 3-D objects worksheets: rectangular prisms, cubes, pyramids, spheres and cylinders, faces, edges and vertices. 100 questions with memos.',
         'Faces are flat; spheres and cylinders have curved surfaces.', 'Faces meet at edges; edges meet at vertices.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
