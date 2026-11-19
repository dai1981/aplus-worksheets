# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Interior and Exterior Angles of Polygons (Grade 7: Measurement and Geometry)
  python3 tools/gen_ph_math_g7_polygon_angles.py
The angle sum of a polygon, interior angles of regular polygons, exterior angles, the number of sides from an angle
(UK Year 8 and Australia Year 7 makers), and the exterior angle next to an interior angle (own maker).
Wrong answers come from real mistakes: using n × 180 instead of (n − 2) × 180, dividing the angle sum by the wrong
number, and mixing up interior and exterior angles.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_uk_maths_y8_angles_in_parallel_lines_and_polygons as uka
adopt(uka)
if hasattr(uka, 'R'): uka.R = random.Random(707030)
import gen_au_maths_y7_angle_sum_of_triangles_and_polygons as aua
adopt(aua)
if hasattr(aua, 'R'): aua.R = random.Random(707031)
ph_common.GRADE = "grade-7"

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


from ws_common import svg_wrap, text, GREEN, FILL, INK, RED


def one_adj(r):
    ia = r.randint(60, 170)
    kind = r.choice(["ext", "int", "reg"])
    if kind == "ext":
        q = "An interior angle of a polygon is %d°. What is the exterior angle next to it?" % ia
        right = 180 - ia
        e = "An interior angle and the exterior angle next to it make a straight line: 180° − %d° = <b>%d°</b>." % (ia, right)
        return mcq(q, "%d°" % right, ["%d°" % x for x in (360 - ia, 90 - ia if ia < 90 else ia - 90, ia)], e)
    if kind == "int":
        ea = 180 - ia
        q = "An exterior angle of a polygon is %d°. What is the interior angle next to it?" % ea
        e = "180° − %d° = <b>%d°</b>." % (ea, ia)
        return mcq(q, "%d°" % ia, ["%d°" % x for x in (360 - ea, ea, abs(90 - ea) + 90 if abs(90 - ea) + 90 != ia else ia + 10)], e)
    n = r.choice([5, 6, 8, 9, 10, 12, 15, 18, 20])
    ea = 360 // n
    if 360 % n:
        raise AssertionError
    q = "Each exterior angle of a regular polygon is %d°. What is each interior angle?" % ea
    e = "Interior + exterior = 180°: 180° − %d° = <b>%d°</b>. (The polygon has 360 ÷ %d = %d sides.)" % (ea, 180 - ea, ea, n)
    return mcq(q, "%d°" % (180 - ea), ["%d°" % x for x in (360 - ea, ea * 2, n)], e)


def build():
    sets, R = build_sets([
        ("Angle sum of a polygon", [("collect", uka.one_sum, 10), ("collect", aua.one_sum, 10)]),
        ("Interior angles of regular polygons", [("collect", uka.one_regular, 20)]),
        ("Exterior angles", [("collect", aua.one_ext, 20)]),
        ("Interior and exterior angle pairs", [("collect", uniq(one_adj), 20)]),
        ("Find the number of sides", [("collect", uka.one_sides, 20)]),
    ], 70703)
    finish(sets, R)
    body = lesson('<ul><li>A polygon with n sides can be split into n − 2 triangles, so its interior angles add up to <b>(n − 2) × 180°</b>.</li><li>Each interior angle of a <b>regular</b> polygon is (n − 2) × 180° ÷ n.</li><li>An interior angle and the <b>exterior angle</b> next to it add up to 180°.</li><li>The exterior angles of any convex polygon add up to 360°. In a regular polygon each exterior angle is 360° ÷ n.</li></ul>',
        [example("Regular octagon", ["(8 − 2) × 180 = 1,080", "1,080 ÷ 8"], "135° each"), example("Exterior angle 24°", ["360 ÷ 24"], "15 sides")],
        [['n × 180', 'Use (n − 2) × 180.'], ['Dividing by the wrong number', 'Divide the sum by the number of angles, n.'], ['Interior or exterior?', 'Exterior = 180° − interior.']])
    faq = [('What does MATATAG Math 7 ask about polygon angles?', 'Deduce the relationship between the exterior angle and adjacent interior angle of a polygon, and determine the measures of angles and the number of sides of polygons.'), ('What is the angle sum of a hexagon?', '(6 − 2) × 180° = 720°.'), ('Why do exterior angles add to 360°?', 'Walking around the polygon, you make one full turn.'), ('Can a regular polygon have an exterior angle of 50°?', 'No: 360 ÷ 50 is not a whole number.')]
    make('interior-and-exterior-angles-of-polygons', 3, 'Measurement and Geometry', 'Grade 7: Measurement and Geometry',
         'Deduce the relationship between the exterior angle and adjacent interior angle of a polygon; determine the measures of angles and the number of sides of polygons.',
         'Interior and Exterior Angles of Polygons', 'Polygon Angles',
         'Free Grade 7 polygon angles worksheets for the DepEd MATATAG curriculum: angle sums, interior and exterior angles of regular polygons and the number of sides. 100 questions with answers.',
         'Angle sum = (n − 2) × 180°.', 'Interior + exterior = 180°; exterior angles add to 360°.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
