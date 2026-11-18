# -*- coding: utf-8 -*-
"""
Texas Grade 1 Math: 3D Solids: Spheres, Cones, Cylinders and Prisms (TEKS 1.6B, 1.6E)
  python3 tools/gen_ustx_math_g1_solids_3d.py
Naming solids (the US Grade 1 maker), solid clues and real objects (the Texas Grade 2 makers), cubes and faces of
solids (US Grade 2 and Ontario makers), and what does and does not make a solid (own maker), all with Texas names.
Wrong answers come from real mistakes: mixing up 2D and 3D names, and naming a solid by its color or size.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g1_shapes as sh
adopt(sh)
import gen_us_math_g2_shapes as sh2
adopt(sh2)
import gen_caon_math_g3_shapes as csh
adopt(csh)
import gen_ustx_math_g2_solids_3d as s3
tx_common.GRADE = "grade-1"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


DEF = [("A cube is painted red. Does the color make it a cube?", "No, it has 6 square faces", ["Yes, all cubes are red", "Yes, red makes it a cube", "No, cubes have no faces"], "A cube is a cube because of its <b>6 square faces</b>, not its color."),
       ("A big ball and a small marble are both spheres. Why?", "Both are round all over", ["Both are big", "Both are red", "Both have flat faces"], "Size does not matter. Both are <b>round all over</b>."),
       ("A cone is turned upside down. Is it still a cone?", "Yes", ["No, it is a cylinder", "No, it is a sphere", "Only if it is red"], "Turning a solid does not change its name. It is still a <b>cone</b>."),
       ("Which tells you a solid is a cylinder?", "2 flat circle faces and a curved surface", ["It is blue", "It is tall", "It is made of metal"], "A cylinder has <b>2 flat circle faces</b> and a curved surface."),
       ("Which does NOT matter when you name a solid?", "Its color", ["The shape of its faces", "The number of faces", "If it has a curved surface"], "<b>Color</b> does not change the name of a solid."),
       ("Which tells you a solid is a triangular prism?", "2 triangle faces and 3 rectangle faces", ["It is yellow", "It is small", "It can be held in one hand"], "A triangular prism has <b>2 triangle faces and 3 rectangle faces</b>."),
       ("Which solid has a point at the top and a circle face at the bottom?", "A cone", ["A cylinder", "A cube", "A sphere"], "That is a <b>cone</b>."),
       ("Which solid has 6 faces that are rectangles?", "A rectangular prism", ["A cone", "A sphere", "A cylinder"], "A <b>rectangular prism</b> has 6 rectangle faces.")]


def one_def(r):
    q, a, w, e = r.choice(DEF)
    return mcq(q, a, w, e)


def build():
    sets, R = build_sets([
        ("Name the solid", [("run", sh.set_solids, ("rnd", sh.People), 20)]),
        ("Solids in the world", [("collect", uniq(s3.one_clue), 6), ("collect", uniq(s3.one_real), 14)]),
        ("Cubes: faces, edges and vertices", [("run", sh2.set_cube, ("rnd", sh2.People), 20)]),
        ("Faces of solids", [("run", csh.set_faces, ("rnd", csh.People), 20)]),
        ("What makes a solid that solid?", [("collect", uniq(one_def), 8), ("collect", uniq(s3.one_sort), 7), ("collect", uniq(s3.one_cmp), 5)]),
    ], 69115)
    finish(sets, R)
    body = lesson('<ul><li>3D <b>solids</b>: sphere, cone, cylinder, rectangular prism, cube, triangular prism.</li><li>A <b>face</b> is a flat surface. A sphere has none.</li><li>A <b>cube</b> is a rectangular prism with 6 square faces.</li><li>Color, size and how a solid is turned do <b>not</b> change its name.</li></ul>',
        [example("A can of soup", ["2 circle faces, curved surface"], "cylinder")],
        [['Mixing up 2D and 3D names', 'A circle is flat; a sphere is a ball.'], ['Naming a solid by its color or size', 'A small red cube is still a cube.'], ['Calling a cube a square', 'A square is one face of a cube.']])
    faq = [('What does TEKS 1.6E ask?', 'Identify three-dimensional solids, including spheres, cones, cylinders, rectangular prisms (including cubes), and triangular prisms, and describe their attributes using formal geometric language.'), ('What does TEKS 1.6B ask?', 'Distinguish between attributes that define a two-dimensional or three-dimensional figure and attributes that do not define the shape.'), ('Is a cube a rectangular prism?', 'Yes. It is a special one with square faces.'), ('Which solids can roll?', 'Spheres, cones and cylinders.')]
    make('3d-solids', 15, 'Geometry and Measurement', '1.6B, 1.6E',
         '1.6B distinguish between attributes that define a two-dimensional or three-dimensional figure and attributes that do not define the shape; 1.6E identify three-dimensional solids, including spheres, cones, cylinders, rectangular prisms (including cubes), and triangular prisms, and describe their attributes using formal geometric language',
         '3D Solids: Spheres, Cones, Cylinders and Prisms', '3D Solids',
         'Free Grade 1 3D solid worksheets for Texas TEKS 1.6B and 1.6E: spheres, cones, cylinders, cubes and prisms, faces, and what does and does not make a solid. 100 questions with answers.',
         'Name a solid by its faces, not its color.', 'A cube has 6 square faces.',
         body, faq, sets, seo_title='Grade 1 3D Solids Worksheets (TEKS 1.6E)')


if __name__ == "__main__":
    build()
