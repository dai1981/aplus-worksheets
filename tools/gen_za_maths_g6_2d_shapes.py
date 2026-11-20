# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): 2-D Shapes: Polygons, Triangles, Quadrilaterals and Circles (Grade 6: 3.1 Properties of 2-D shapes)
  python3 tools/gen_za_maths_g6_2d_shapes.py
Polygons, kinds of triangles, quadrilaterals and their diagonals, and parts of a circle (BC Grade 6, Ontario Grade 6
and UK Year 6 makers, and the circle maker from the Grade 5 generator).
Wrong answers come from real mistakes: thinking a square is not a rectangle, naming a triangle by only its sides,
and mixing up the radius and the diameter.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_cabc_math_g6_triangles as cbt
adopt(cbt)
if isinstance(getattr(cbt, 'R', None), random.Random): cbt.R = random.Random(806200)
import gen_caon_math_g6_quadrilaterals as caq
adopt(caq)
if isinstance(getattr(caq, 'R', None), random.Random): caq.R = random.Random(806201)
import gen_uk_maths_y6_circles_nets as ukc
adopt(ukc)
if isinstance(getattr(ukc, 'R', None), random.Random): ukc.R = random.Random(806202)
import gen_za_maths_g5_2d_shapes as zs5
adopt(zs5)
if isinstance(getattr(zs5, 'R', None), random.Random): zs5.R = random.Random(806203)
za_common.GRADE = "grade-6"


import re as _re


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def _nums(it):
    return [int(x.replace(",", "").replace("\u00a0", "")) for x in _re.findall(r"(?<![\d.])\d[\d,\u00a0]*(?![.\d])", _txt(it)) if x.replace(",", "").replace("\u00a0", "").isdigit()]


def noneg(it):
    return not _re.search(r"(?<![\d)] )[−-]\d", _txt(it)) and "negative" not in _txt(it).lower()


def nine(it):
    """whole numbers to 9 digits, no negatives"""
    return all(n <= 999999999 for n in _nums(it)) and noneg(it)


def dec3(it):
    """decimals with at most 3 places, no negatives"""
    return noneg(it) and not _re.search(r"\d\.\d{4}", _txt(it))


def nodec(it):
    return noneg(it) and not _re.search(r"\d\.\d", _txt(it))


def flat(it):
    """first quadrant only: no negative numbers in the text or the picture"""
    return nodec(it) and "−" not in it["q"] and "-1" not in it["q"]


def nomean(it):
    return dec3(it) and not _re.search(r"\bmean\b", _txt(it))


def den12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " " + it["c"][it["a"]])]
    return all(d <= 12 or d in (20, 25, 50, 100) for d in ds) and nodec(it)



def build():
    sets, R = build_sets([
        ("Kinds of triangles", [("run", cbt.set_sides, ("rnd", cbt.Spots), 10, nodec), ("run", cbt.set_angles, ("rnd", cbt.Spots), 10, nodec)]),
        ("Quadrilaterals", [("run", caq.set_name, ("rnd",), 20, nodec)]),
        ("Diagonals and sides", [("run", caq.set_diagonals, ("rnd",), 10, nodec), ("run", caq.set_words, ("rnd",), 10, nodec)]),
        ("Circles", [("run", ukc.set_parts, ("rnd", ukc.Pos), 10, nodec), ("collect", zs5.uniq(zs5.one_circle), 10)]),
        ("Radius and diameter", [("run", ukc.set_radius, ("rnd",), 20, dec3)]),
    ], 80620)
    finish(sets, R)
    body = lesson('<ul><li>Triangles by sides: equilateral, isosceles, scalene. By angles: acute-angled, right-angled, obtuse-angled.</li><li>Quadrilaterals: square, rectangle, rhombus, parallelogram, kite and trapezium. A square is a special rectangle and a special rhombus.</li><li>A diagonal joins two corners that are not next to each other.</li><li>Circle: diameter = 2 × radius.</li></ul>',
        [example("4 equal sides, no right angles", ["opposite sides parallel"], "a rhombus")],
        [['A square is a rectangle', 'It has 4 right angles.'], ['Sides only', 'Look at the angles too.'], ['Radius or diameter?', 'The diameter goes all the way across.']])
    faq = [('What does CAPS Grade 6 say about 2-D shapes?', 'Recognise, visualise and name 2-D shapes, including similarities and differences between quadrilaterals, triangles by sides and angles, and parts of a circle.'), ('Is a square a parallelogram?', 'Yes.'), ('What is a kite?', 'A quadrilateral with two pairs of equal sides next to each other.'), ('How many diagonals does a hexagon have?', '9.')]
    make('2d-shapes', 20, 'Space and Shape (Geometry)', 'Grade 6: 3.1 Properties of 2-D shapes',
         'Recognise, visualise and name 2-D shapes in the environment and geometric settings, focusing on regular and irregular polygons (triangles, squares, rectangles, parallelograms, other quadrilaterals, pentagons, hexagons, heptagons, octagons) and circles; similarities and differences between squares, rectangles, parallelograms, rhombuses, trapeziums and kites; describe, sort and compare 2-D shapes in terms of the length of sides, the number of sides and the size of angles.',
         '2-D Shapes: Polygons, Triangles, Quadrilaterals and Circles', '2-D Shapes',
         'Free CAPS Grade 6 2-D shapes worksheets: triangles by sides and angles, quadrilaterals, diagonals and parts of a circle. 100 questions with memos.',
         'Name shapes by their sides and angles.', 'A square is a special rectangle and rhombus.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
