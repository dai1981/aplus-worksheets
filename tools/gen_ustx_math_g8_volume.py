# -*- coding: utf-8 -*-
"""
Texas Grade 8 Math: Volume of Cylinders, Cones and Spheres (TEKS 8.6A, 8.6B, 8.7A)
  python3 tools/gen_ustx_math_g8_volume.py
Volume of cylinders, cones and spheres in terms of π, using 3.14 and finding missing sizes, and real-world volume
(the US Grade 8 makers with a new seed).
Wrong answers come from real mistakes: using the diameter as the radius, forgetting the 1/3 for a cone, and cubing
instead of squaring the radius for a cylinder.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g8_volume_of_cylinders_cones_spheres as vcs
adopt(vcs)
vcs.R = random.Random(680170)
tx_common.GRADE = "grade-8"



def build():
    sets, R = build_sets([
        ("Volume of cylinders", [("run", vcs.set_cyl, (), 20)]),
        ("Volume of cones", [("run", vcs.set_cone, (), 20)]),
        ("Volume of spheres", [("run", vcs.set_sph, (), 20)]),
        ("Use π ≈ 3.14 and find missing sizes", [("run", vcs.set_314, (), 20)]),
        ("Real-world volume", [("run", vcs.set_world, (), 20)]),
    ], 68017)
    finish(sets, R)
    body = lesson('<ul><li>Cylinder: <b>V = Bh = πr²h</b>, where B is the area of the circle base.</li><li>Cone: <b>V = ⅓πr²h</b>. A cone holds one third of a cylinder with the same base and height.</li><li>Sphere: <b>V = ⁴⁄₃πr³</b>.</li><li>Use the radius, not the diameter.</li></ul>',
        [example("Cylinder r = 3, h = 10", ["π × 9 × 10"], "90π"), example("Cone r = 3, h = 10", ["⅓ × 90π"], "30π")],
        [['Using the diameter as the radius', 'r = d ÷ 2.'], ['Forgetting the ⅓ for a cone', 'A cone is one third of the cylinder.'], ['Squaring instead of cubing for a sphere', 'V = ⁴⁄₃πr³ uses r³.']])
    faq = [('What does TEKS 8.6A ask?', 'Describe the volume formula V = Bh of a cylinder in terms of its base area and its height.'), ('What does TEKS 8.6B ask?', 'Model the relationship between the volume of a cylinder and a cone having both congruent bases and heights and connect that relationship to the formulas.'), ('What does TEKS 8.7A ask?', 'Solve problems involving the volume of cylinders, cones and spheres.'), ('What does in terms of π mean?', 'Leave π as a symbol, such as 90π, instead of multiplying by 3.14.')]
    make('volume-of-cylinders-cones-and-spheres', 17, 'Expressions, Equations and Relationships', '8.6A, 8.6B, 8.7A',
         '8.6A describe the volume formula V = Bh of a cylinder in terms of its base area and its height; 8.6B model the relationship between the volume of a cylinder and a cone having both congruent bases and heights and connect that relationship to the formulas; 8.7A solve problems involving the volume of cylinders, cones, and spheres',
         'Volume of Cylinders, Cones and Spheres', 'Volume of Cylinders, Cones and Spheres',
         'Free Grade 8 volume worksheets for Texas TEKS 8.6A, 8.6B and 8.7A: volume of cylinders, cones and spheres, in terms of π and with 3.14, and real-world problems. 100 questions with answers.',
         'Cylinder πr²h, cone ⅓πr²h, sphere ⁴⁄₃πr³.', 'A cone is one third of the cylinder with the same base and height.',
         body, faq, sets, seo_title='Grade 8 Volume of Cylinders, Cones and Spheres Worksheets (TEKS 8.7A, STAAR)')


if __name__ == "__main__":
    build()
