# -*- coding: utf-8 -*-
"""
Texas Grade 7 Math: Circumference and Area of Circles (TEKS 7.5B, 7.8C, 7.9B)
  python3 tools/gen_ustx_math_g7_circles.py
Radius, diameter and π, circumference, area, working backward, and word problems (the US Grade 7 makers with a new
seed).
Wrong answers come from real mistakes: using the diameter in A = πr², mixing up circumference and area, and
squaring the diameter.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g7_circles as ci
adopt(ci)
ci.R = random.Random(670120)
tx_common.GRADE = "grade-7"



def build():
    sets, R = build_sets([
        ("Radius, diameter and π", [("run", ci.set_parts, (), 20)]),
        ("Circumference", [("run", ci.set_circumference, (), 20)]),
        ("Area", [("run", ci.set_area, (), 20)]),
        ("Working backward and parts of circles", [("run", ci.set_reverse, (), 20)]),
        ("Word problems", [("run", ci.set_words, (), 20)]),
    ], 67012)
    finish(sets, R)
    body = lesson("<ul><li><b>π</b> is the ratio of a circle's circumference to its diameter, about 3.14 or 22/7.</li><li>Circumference: C = πd = 2πr.</li><li>Area: A = πr². Cut a circle into thin wedges and line them up: they make a shape close to a parallelogram with base πr and height r.</li><li>The diameter is twice the radius.</li></ul>",
        [example("r = 5 cm", ["C = 2 × 3.14 × 5", "A = 3.14 × 5²"], "C = 31.4 cm, A = 78.5 cm²")],
        [['Using the diameter in A = πr²', 'Halve the diameter to get r first.'], ['Mixing up C and A', 'Circumference is a length (cm); area is square units (cm²).'], ['Squaring before halving', 'r = d ÷ 2, then square r.']])
    faq = [('What does TEKS 7.5B ask?', 'Describe π as the ratio of the circumference of a circle to its diameter.'), ('What does TEKS 7.9B ask?', 'Determine the circumference and area of circles.'), ('What does TEKS 7.8C ask?', 'Use models to determine the approximate formulas for the circumference and area of a circle and connect the models to the actual formulas.'), ('Should I use 3.14 or 22/7?', 'Use what the problem says. 22/7 is handy when the radius is a multiple of 7.')]
    make('circumference-and-area-of-circles', 12, 'Expressions, Equations and Relationships', '7.5B, 7.8C, 7.9B',
         '7.5B describe π as the ratio of the circumference of a circle to its diameter; 7.8C use models to determine the approximate formulas for the circumference and area of a circle and connect the models to the actual formulas; 7.9B determine the circumference and area of circles',
         'Circumference and Area of Circles', 'Circumference and Area of Circles',
         'Free Grade 7 circle worksheets for Texas TEKS 7.5B, 7.8C and 7.9B: radius, diameter and π, circumference, area, working backward and word problems. 100 questions with answers.',
         'C = πd = 2πr. A = πr².', 'r = 5 cm: C = 31.4 cm, A = 78.5 cm².',
         body, faq, sets, seo_title='Grade 7 Circumference and Area of Circles Worksheets (TEKS 7.9B, STAAR)')


if __name__ == "__main__":
    build()
