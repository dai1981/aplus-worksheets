# -*- coding: utf-8 -*-
"""
South Africa Grade 9 Maths (CAPS): Area and Perimeter: Polygons, Circles and Composite Shapes (Grade 9: 4.1 Area and perimeter of 2D shapes)
  python3 tools/gen_za_maths_g9_area_perimeter.py
Area of trapeziums and kites, circumference and area of circles, composite shapes and shapes with holes (Australia
Year 8 and Singapore Secondary 1 makers).
Wrong answers come from real mistakes: forgetting to halve, using the diameter as the radius, and adding the area of a
hole instead of subtracting it.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y8_area_and_perimeter_of_composite_shapes as aua
adopt(aua)
if isinstance(getattr(aua, 'R', None), random.Random): aua.R = random.Random(809160)
import gen_au_maths_y8_circumference_and_area_of_circles as auc
adopt(auc)
if isinstance(getattr(auc, 'R', None), random.Random): auc.R = random.Random(809161)
import gen_sg_maths_s1_perimeter_and_area as sgp
adopt(sgp)
if isinstance(getattr(sgp, 'R', None), random.Random): sgp.R = random.Random(809162)
za_common.GRADE = "grade-9"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok9(it):
    """Grade 9: no trigonometry, quadratic formula, simultaneous equations or cones and spheres (Grade 10+)"""
    return not _re.search(r"\b(sin|cos|tan)\b|quadratic formula|discriminant|simultaneous|\bcone|\bsphere|imperial|\bmiles?\b", _txt(it))



def build():
    sets, R = build_sets([
        ("Trapeziums and kites", [("collect", aua.one_trap, 10), ("collect", aua.one_kite, 10)]),
        ("Perimeter", [("collect", aua.one_per, 10), ("collect", sgp.one_per, 10)]),
        ("Circles", [("collect", auc.one_circ, 10), ("collect", auc.one_area, 10)]),
        ("Parts of circles", [("collect", auc.one_part, 10), ("collect", auc.one_pi, 10)]),
        ("Composite shapes", [("collect", aua.one_comp, 10), ("collect", aua.one_hole, 10)]),
    ], 80916)
    finish(sets, R)
    body = lesson('<ul><li>Trapezium: A = ½(a + b)h. Kite and rhombus: A = ½ × d₁ × d₂.</li><li>Circle: C = 2πr, A = πr².</li><li>A semicircle has half the area of the circle.</li><li>For a shape with a hole, subtract the area of the hole.</li></ul>',
        [example("A square of side 10 cm with a circular hole of radius 3 cm", ["100 − π × 9"], "about 71,7 cm²")],
        [['Forgetting ½', 'Trapeziums and kites need ½.'], ['Diameter as radius', 'r = d ÷ 2.'], ['Adding the hole', 'Subtract it.']])
    faq = [('What does CAPS Grade 9 say about area?', 'Use formulae to calculate the area and perimeter of polygons and circles, and solve problems including composite shapes.'), ('What is the area of a quarter circle?', '¼πr².'), ('How many cm² are in 1 m²?', '10 000.'), ('What is a composite shape?', 'A shape made of simpler shapes.')]
    make('area-and-perimeter', 16, 'Measurement', 'Grade 9: 4.1 Area and perimeter of 2D shapes',
         'Use appropriate formulae to calculate perimeter and area of polygons and circles; investigate how doubling any or all the dimensions of a 2-D figure affects its perimeter and its area; solve problems involving perimeter and area of polygons and circles.',
         'Area and Perimeter: Polygons, Circles and Composite Shapes', 'Area and Perimeter',
         'Free CAPS Grade 9 area and perimeter worksheets: trapeziums, kites, circles, parts of circles and composite shapes. 100 questions with memos.',
         'A = πr²; trapezium A = ½(a + b)h.', 'Subtract the area of a hole.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
