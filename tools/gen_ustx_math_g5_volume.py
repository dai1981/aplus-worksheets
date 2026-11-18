# -*- coding: utf-8 -*-
"""
Texas Grade 5 Math: Volume of Rectangular Prisms (TEKS 5.4G, 5.6A, 5.6B)
  python3 tools/gen_ustx_math_g5_volume.py
Counting unit cubes, layers times the cubes in the base, V = l × w × h and V = B × h, missing edges, two prisms
put together, and word problems. The question makers come from the US Grade 5 volume unit with Texas names.
Wrong answers come from real mistakes: counting only the cubes you can see, adding the edges, and using square
units for volume.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g5_volume as usv
adopt(usv)
tx_common.GRADE = "grade-5"



def build():
    sets, R = build_sets([
        ("Count unit cubes", [("run", usv.set_count, ("rnd",), 20)]),
        ("Use V = l × w × h and V = B × h", [("run", usv.set_formula, ("rnd", "seen"), 20)]),
        ("Find a missing edge", [("run", usv.set_missing, ("rnd", "seen"), 20)]),
        ("Add the volumes of two prisms", [("run", usv.set_two, ("rnd", usv.People), 20)]),
        ("Volume word problems", [("run", usv.set_story, ("rnd", usv.People), 20)]),
    ], 65016)
    finish(sets, R)
    body = lesson('<ul><li>A <b>unit cube</b> has a volume of 1 cubic unit. Volume is the number of unit cubes that fill a figure with no gaps or overlaps.</li><li>A rectangular prism is <b>layers</b>: the cubes in the base times the number of layers. V = B × h, where B is the area of the base.</li><li>V = l × w × h. For a cube, V = s × s × s.</li><li>Volume is in cubic units: cubic centimeters, cubic feet.</li></ul>',
        [example("A box is 6 cm long, 4 cm wide and 3 cm high.", ["B = 6 × 4 = 24", "V = 24 × 3"], "72 cubic centimeters"), example("A cube has 5-inch edges.", ["5 × 5 × 5"], "125 cubic inches")],
        [['Counting only the cubes you can see', 'Count the cubes in one layer, then multiply by the number of layers.'], ['Adding the edges', 'Volume multiplies: l × w × h.'], ['Writing square units', 'Volume is in cubic units.']])
    faq = [('What does TEKS 5.6A ask?', 'Recognize a unit cube as one cubic unit and the volume of a 3D figure as the number of unit cubes needed to fill it.'), ('What does TEKS 5.6B ask?', 'Find the volume of a rectangular prism as the number of layers times the number of unit cubes in the area of the base.'), ('What does TEKS 5.4G ask?', 'Use models to develop the volume formulas V = l × w × h, V = s × s × s and V = Bh.'), ('What is B in V = Bh?', 'The area of the base. For a rectangular prism, B = l × w.')]
    make('volume-of-rectangular-prisms', 16, 'Geometry and Measurement', '5.4G, 5.6A, 5.6B',
         '5.4G use concrete objects and pictorial models to develop the formulas for the volume of a rectangular prism, including the special form for a cube (V = l x w x h, V = s x s x s, and V = Bh); 5.6A recognize a cube with side length of one unit as a unit cube having one cubic unit of volume and the volume of a three-dimensional figure as the number of unit cubes (n cubic units) needed to fill it with no gaps or overlaps if possible; 5.6B determine the volume of a rectangular prism with whole number side lengths in problems related to the number of layers times the number of unit cubes in the area of the base',
         'Volume of Rectangular Prisms', 'Volume',
         'Free Grade 5 volume worksheets for Texas TEKS 5.4G, 5.6A and 5.6B: count unit cubes, layers, V = l × w × h and V = Bh, missing edges, two prisms and word problems. 100 questions with answers.',
         'V = l × w × h = B × h.', 'Volume counts unit cubes: the cubes in one layer times the number of layers. Use cubic units.',
         body, faq, sets, seo_title='Grade 5 Volume of Rectangular Prisms Worksheets (TEKS 5.6A, 5.6B, STAAR)')


if __name__ == "__main__":
    build()
