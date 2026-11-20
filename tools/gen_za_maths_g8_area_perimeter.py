# -*- coding: utf-8 -*-
"""
South Africa Grade 8 Maths (CAPS): Area and Perimeter: Polygons and Circles (Grade 8: 4.1 Area and perimeter of 2D shapes)
  python3 tools/gen_za_maths_g8_area_perimeter.py
Area of triangles, trapeziums and kites, composite shapes, circumference and area of circles (Australia Year 7 and
Year 8 and UK Year 8 makers).
Wrong answers come from real mistakes: forgetting to halve, using the diameter as the radius, and mixing up the
circumference and the area.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y8_area_and_perimeter_of_composite_shapes as aua
adopt(aua)
if isinstance(getattr(aua, 'R', None), random.Random): aua.R = random.Random(808180)
import gen_au_maths_y7_area_of_triangles_and_parallelograms as aut
adopt(aut)
if isinstance(getattr(aut, 'R', None), random.Random): aut.R = random.Random(808181)
import gen_au_maths_y8_circumference_and_area_of_circles as auc
adopt(auc)
if isinstance(getattr(auc, 'R', None), random.Random): auc.R = random.Random(808182)
import gen_uk_maths_y8_circles as ukc
adopt(ukc)
if isinstance(getattr(ukc, 'R', None), random.Random): ukc.R = random.Random(808183)
za_common.GRADE = "grade-8"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok8(it):
    """Grade 8: no trigonometry, quadratic formula or surds beyond square roots"""
    return not _re.search(r"\b(sin|cos|tan)\b|quadratic|discriminant|imperial|\bmiles?\b", _txt(it))



def build():
    sets, R = build_sets([
        ("Triangles and parallelograms", [("collect", aut.one_tri, 10), ("collect", aut.one_para, 10)]),
        ("Trapeziums and kites", [("collect", aua.one_trap, 10), ("collect", aua.one_kite, 10)]),
        ("Circumference", [("collect", auc.one_circ, 10), ("collect", ukc.one_circ, 10)]),
        ("Area of circles", [("collect", auc.one_area, 10), ("collect", ukc.one_area, 10)]),
        ("Composite shapes", [("collect", aua.one_comp, 10), ("collect", aua.one_hole, 10)]),
    ], 80818)
    finish(sets, R)
    body = lesson('<ul><li>Triangle: A = ½ × b × h. Parallelogram: A = b × h. Trapezium: A = ½(a + b) × h.</li><li>Circumference: C = πd = 2πr. Area of a circle: A = πr².</li><li>Use π ≈ 3,14 or the π key.</li><li>Split composite shapes; subtract the area of a hole.</li></ul>',
        [example("A circle with diameter 10 cm", ["r = 5 cm", "A = π × 5²"], "about 78,5 cm²")],
        [['Forgetting ½', 'Triangles and trapeziums need ½.'], ['Diameter as radius', 'r = d ÷ 2.'], ['C or A?', 'Area uses r² and is in cm².']])
    faq = [('What does CAPS Grade 8 say about area and perimeter?', 'Use formulae to calculate the perimeter and area of polygons and circles, and convert between square units.'), ('What is π?', 'The ratio of the circumference to the diameter, about 3,14.'), ('What is the area of a semicircle?', '½πr².'), ('How many mm² in 1 cm²?', '100.')]
    make('area-and-perimeter', 18, 'Measurement', 'Grade 8: 4.1 Area and perimeter of 2D shapes',
         'Use appropriate formulae to calculate perimeter and area of squares, rectangles, triangles and circles; calculate areas of polygons, to at least 2 decimal places, by decomposing into rectangles and/or triangles; use and convert between appropriate SI units.',
         'Area and Perimeter: Polygons and Circles', 'Area and Perimeter',
         'Free CAPS Grade 8 area and perimeter worksheets: triangles, trapeziums, kites, circumference and area of circles and composite shapes. 100 questions with memos.',
         'A = πr²; C = 2πr.', 'r = d ÷ 2.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
