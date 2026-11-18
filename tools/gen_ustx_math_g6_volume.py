# -*- coding: utf-8 -*-
"""
Texas Grade 6 Math: Volume of Rectangular Prisms with Fractional Edges (TEKS 6.8C, 6.8D)
  python3 tools/gen_ustx_math_g6_volume.py
Packing a prism with fractional cubes, V = l × w × h and V = B × h with fractions, decimals and missing edges, and
word problems (the US Grade 6 makers with Texas names).
Wrong answers come from real mistakes: adding the edges, multiplying only two edges, and forgetting to convert
mixed numbers.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g6_volume as vo
adopt(vo)
tx_common.GRADE = "grade-6"



def build():
    sets, R = build_sets([
        ("Pack a box with small cubes", [("run", vo.set_pack, ("rnd",), 20)]),
        ("Use V = l × w × h with fractions", [("run", vo.set_formula, ("rnd", "seen"), 20)]),
        ("Use V = B × h", [("run", vo.set_base, ("rnd",), 20)]),
        ("Decimals and missing edges", [("run", vo.set_missing, ("rnd",), 20)]),
        ("Volume word problems", [("run", vo.set_story, ("rnd", vo.People), 20)]),
    ], 66018)
    finish(sets, R)
    body = lesson('<ul><li>Volume of a rectangular prism: <b>V = l × w × h</b>, or <b>V = B × h</b> where B is the area of the base.</li><li>With fractions, change mixed numbers to improper fractions and multiply.</li><li>To find a missing edge, divide the volume by the product of the other two edges.</li><li>Volume is measured in cubic units, such as in³ or cm³.</li></ul>',
        [example("4 1/2 cm × 2/3 cm × 6 cm", ["9/2 × 2/3 × 6", "= 18"], "18 cm³")],
        [['Adding the edges', 'Volume multiplies: l × w × h.'], ['Multiplying only two edges', 'That gives the area of the base, B.'], ['Using mixed numbers without converting', 'Change 4 1/2 to 9/2 first.']])
    faq = [('What does TEKS 6.8C ask?', 'Write equations that represent problems related to the area of rectangles, parallelograms, trapezoids and triangles and volume of right rectangular prisms where dimensions are positive rational numbers.'), ('What is B in V = B × h?', 'B is the area of the base: l × w for a rectangular prism.'), ('How do small cubes help?', 'A cube with 1/2-unit edges has volume 1/8 cubic unit, so count the cubes and multiply.'), ('How do I find a missing edge?', 'Divide the volume by the area of the base.')]
    make('volume-of-rectangular-prisms', 18, 'Geometry and Measurement', '6.8C, 6.8D',
         '6.8C write equations that represent problems related to the area of rectangles, parallelograms, trapezoids, and triangles and volume of right rectangular prisms where dimensions are positive rational numbers; 6.8D determine solutions for problems involving the area of rectangles, parallelograms, trapezoids, and triangles and volume of right rectangular prisms where dimensions are positive rational numbers',
         'Volume of Rectangular Prisms with Fractional Edges', 'Volume of Rectangular Prisms',
         'Free Grade 6 volume worksheets for Texas TEKS 6.8C and 6.8D: volume of rectangular prisms with fractional and decimal edges, V = B × h, missing edges and word problems. 100 questions with answers.',
         'V = l × w × h = B × h.', '9/2 × 2/3 × 6 = 18 cubic units. Missing edge = V ÷ (product of the other two).',
         body, faq, sets, seo_title='Grade 6 Volume of Rectangular Prisms with Fractions Worksheets (TEKS 6.8C, 6.8D, STAAR)')


if __name__ == "__main__":
    build()
