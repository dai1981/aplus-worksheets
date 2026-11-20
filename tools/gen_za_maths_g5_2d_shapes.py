# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): 2-D Shapes: Polygons, Triangles, Quadrilaterals and Circles (Grade 5: 3.1 Properties of 2-D shapes)
  python3 tools/gen_za_maths_g5_2d_shapes.py
Regular and irregular polygons, triangles, quadrilaterals and their properties (BC Grade 4, Ontario Grade 5 and US
Grade 5 makers), and parts of a circle (own maker).
Wrong answers come from real mistakes: counting corners as sides, thinking a square is not a rectangle, and mixing
up the radius and the diameter.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_cabc_math_g4_polygons as cbp
adopt(cbp)
if isinstance(getattr(cbp, 'R', None), random.Random): cbp.R = random.Random(805150)
import gen_caon_math_g5_triangles as cat
adopt(cat)
if isinstance(getattr(cat, 'R', None), random.Random): cat.R = random.Random(805151)
import gen_us_math_g5_classify_figures as usc
adopt(usc)
if isinstance(getattr(usc, 'R', None), random.Random): usc.R = random.Random(805152)
za_common.GRADE = "grade-5"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


import re as _re


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def _nums(it):
    return [int(x.replace(",", "").replace("\u00a0", "")) for x in _re.findall(r"(?<![\d.])\d[\d,\u00a0]*(?![.\d])", _txt(it)) if x.replace(",", "").replace("\u00a0", "").isdigit()]


def six(it):
    """whole numbers to 6 digits, no decimals, no negatives"""
    t = _txt(it)
    return all(n <= 999999 for n in _nums(it)) and not _re.search(r"\d\.\d|−\d", t)


def nodec(it):
    return not _re.search(r"\d\.\d|−\d", _txt(it))


def den12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " " + it["c"][it["a"]])]
    return all(d <= 12 for d in ds) and nodec(it)


def circle_svg(show):
    s = "<svg viewBox='0 0 160 140' width='160' height='140' role='img' aria-label='circle'>"
    s += "<circle cx='80' cy='70' r='55' fill='none' stroke='#333' stroke-width='2'/><circle cx='80' cy='70' r='3' fill='#333'/>"
    if show == "radius":
        s += "<line x1='80' y1='70' x2='135' y2='70' stroke='#c0392b' stroke-width='3'/>"
    elif show == "diameter":
        s += "<line x1='25' y1='70' x2='135' y2='70' stroke='#c0392b' stroke-width='3'/>"
    elif show == "centre":
        s += "<circle cx='80' cy='70' r='6' fill='none' stroke='#c0392b' stroke-width='3'/>"
    elif show == "circumference":
        s += "<circle cx='80' cy='70' r='55' fill='none' stroke='#c0392b' stroke-width='4'/>"
    return s + "</svg>"


PARTS = ["centre", "radius", "diameter", "circumference"]


def one_circle(r):
    k = r.choice(["name", "name", "r2d", "d2r"])
    if k == "name":
        p = r.choice(PARTS)
        expl = {"centre": "The centre is the point in the middle of the circle.", "radius": "A radius goes from the centre to the edge.",
                "diameter": "A diameter goes across the circle through the centre.", "circumference": "The circumference is the distance all the way round the circle."}
        q = fig(circle_svg(p)) + "What is the part marked in red called?"
        return mcq(q, "the " + p, ["the " + x for x in PARTS if x != p], expl[p] + " Answer: <b>the %s</b>." % p)
    rad = r.randint(2, 40)
    unit = r.choice(["cm", "mm", "m"])
    if k == "r2d":
        return mcq("A circle has a radius of %d %s. What is its diameter?" % (rad, unit), "%d %s" % (2 * rad, unit), ["%d %s" % (x, unit) for x in (rad, rad + 2, 4 * rad)],
                   "The diameter is 2 radii: 2 × %d = <b>%d %s</b>." % (rad, 2 * rad, unit))
    return mcq("A circle has a diameter of %d %s. What is its radius?" % (2 * rad, unit), "%d %s" % (rad, unit), ["%d %s" % (x, unit) for x in (2 * rad, 4 * rad, rad + 2)],
               "The radius is half the diameter: %d ÷ 2 = <b>%d %s</b>." % (2 * rad, rad, unit))


def build():
    sets, R = build_sets([
        ("Polygons", [("run", cbp.set_name, ("rnd", cbp.Pos, cbp.People), 10, six), ("run", cbp.set_regular, ("rnd", cbp.Pos, cbp.People), 10, six)]),
        ("Triangles", [("run", cat.set_sides, ("rnd", cat.Spots), 10, six), ("run", usc.set_triangles, ("rnd",), 10, six)]),
        ("Quadrilaterals", [("run", usc.set_quads, ("rnd",), 20, six)]),
        ("Circles", [("collect", uniq(one_circle), 20)]),
        ("Shape properties", [("run", usc.set_hierarchy, ("rnd",), 10, six), ("run", usc.set_reason, ("rnd",), 10, six)]),
    ], 80515)
    finish(sets, R)
    body = lesson('<ul><li>A <b>polygon</b> is a closed shape with straight sides. A <b>regular</b> polygon has all sides and all angles equal.</li><li>Triangles: equilateral (3 equal sides), isosceles (2 equal sides), scalene (no equal sides). A right-angled triangle has one right angle.</li><li>Quadrilaterals have 4 sides: square, rectangle, rhombus, parallelogram, kite, trapezium.</li><li>Circle: the <b>radius</b> goes from the centre to the edge; the <b>diameter</b> is 2 radii.</li></ul>',
        [example("4 equal sides, 4 right angles", ["a quadrilateral", "also a rectangle and a rhombus"], "a square")],
        [['Corners as sides', 'Count the straight sides.'], ['A square is a rectangle', 'It has 4 right angles.'], ['Radius or diameter?', 'The diameter goes all the way across.']])
    faq = [('What does CAPS Grade 5 say about 2-D shapes?', 'Recognise, visualise and name regular and irregular polygons, triangles, quadrilaterals, circles and others, and describe their sides and angles.'), ('Is a square a rhombus?', 'Yes. It has 4 equal sides.'), ('What is a trapezium?', 'A quadrilateral with at least one pair of parallel sides.'), ('What is the centre of a circle?', 'The point in the middle, the same distance from every point on the edge.')]
    make('2d-shapes', 15, 'Space and Shape (Geometry)', 'Grade 5: 3.1 Properties of 2-D shapes',
         'Recognise, visualise and name 2-D shapes in the environment and geometric settings, focusing on regular and irregular polygons (triangles, squares, rectangles, other quadrilaterals, pentagons, hexagons, heptagons) and circles; similarities and differences between rectangles and squares; describe, sort and compare 2-D shapes in terms of straight and curved sides, number of sides and angles (right angles and angles smaller or bigger than a right angle).',
         '2-D Shapes: Polygons, Triangles, Quadrilaterals and Circles', '2-D Shapes',
         'Free CAPS Grade 5 2-D shapes worksheets: regular and irregular polygons, triangles, quadrilaterals and parts of a circle. 100 questions with memos.',
         'Name shapes by their sides and angles.', 'A regular polygon has equal sides and equal angles.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
