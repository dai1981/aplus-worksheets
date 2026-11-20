# -*- coding: utf-8 -*-
"""
South Africa Grade 7 Maths (CAPS): Area and Perimeter of Squares, Rectangles and Triangles (Grade 7: 4.1 Area and perimeter of 2D shapes)
  python3 tools/gen_za_maths_g7_area_perimeter.py
Area of rectangles and triangles, perimeter, composite shapes, and area of triangles and parallelograms (UK Year 7 and
Australia Year 7 makers).
Wrong answers come from real mistakes: forgetting to halve for a triangle, using the slant side instead of the
perpendicular height, and mixing up area and perimeter.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y7_perimeter_and_area as ukp
adopt(ukp)
if isinstance(getattr(ukp, 'R', None), random.Random): ukp.R = random.Random(807220)
import gen_au_maths_y7_area_of_triangles_and_parallelograms as aua
adopt(aua)
if isinstance(getattr(aua, 'R', None), random.Random): aua.R = random.Random(807221)
za_common.GRADE = "grade-7"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok7(it):
    """Grade 7: no circles, pi or standard form (they come in Grade 8 and 9)"""
    return not _re.search(r"π|\bpi\b|circumference|radius|diameter|×\s?10<sup>|standard form|scientific notation", _txt(it))


def noneg(it):
    return ok7(it) and not _re.search(r"(?<![\d)] )[−-]\d", _txt(it))



def build():
    sets, R = build_sets([
        ("Area of rectangles", [("collect", ukp.one_rt, 20)]),
        ("Area of triangles", [("collect", ukp.one_pt, 10), ("collect", aua.one_tri, 10)]),
        ("Perimeter", [("collect", ukp.one_per, 20)]),
        ("Composite shapes", [("collect", ukp.one_comp, 10), ("collect", aua.one_house, 10)]),
        ("Missing lengths and problems", [("collect", aua.one_missing, 10), ("run", ukp.problems, (), 10, ok7)]),
    ], 80722)
    finish(sets, R)
    body = lesson("<ul><li>Perimeter is the distance around a shape. Area is the space inside it.</li><li>Rectangle: A = l × b. Square: A = l².</li><li>Triangle: A = <span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span> × base × perpendicular height.</li><li>Split composite shapes into rectangles and triangles.</li></ul>",
        [example("A triangle with base 12 cm and height 7 cm", ["½ × 12 × 7"], "42 cm²")],
        [['Forgetting ½', 'A triangle is half a rectangle.'], ['The slant side', 'Use the perpendicular height.'], ['Area or perimeter?', 'Area is in cm²; perimeter in cm.']])
    faq = [('What does CAPS Grade 7 say about area and perimeter?', 'Calculate the perimeter of regular and irregular polygons and the area of squares, rectangles and triangles using formulae, and convert between mm², cm², m² and km².'), ('How many cm² are in 1 m²?', '10 000.'), ('What is the perpendicular height?', 'The height at right angles to the base.'), ('Can I find area by counting squares?', 'Yes, but formulae are faster.')]
    make('area-and-perimeter', 22, 'Measurement', 'Grade 7: 4.1 Area and perimeter of 2D shapes',
         'Use appropriate formulae to calculate perimeter of polygons and area of squares, rectangles and triangles; describe the interrelationship between perimeter and area; convert between mm², cm² and m².',
         'Area and Perimeter of Squares, Rectangles and Triangles', 'Area and Perimeter',
         'Free CAPS Grade 7 area and perimeter worksheets: area of rectangles and triangles, perimeter, composite shapes and missing lengths. 100 questions with memos.',
         'Triangle: ½ × base × height.', 'Use the perpendicular height.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
