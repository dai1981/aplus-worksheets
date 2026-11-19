# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Volume of Cylinders (Grade 7: Measurement and Geometry)
  python3 tools/gen_ph_math_g7_cylinders.py
The volume of a cylinder as base area × height, with π, diameters and missing dimensions, and problems (Singapore
Secondary 2, UK Year 8 and BC Grade 7 makers, and own real-life problems).
Wrong answers come from real mistakes: using the diameter as the radius, forgetting to square the radius, and
using 2πr (the circumference) instead of πr².
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_sg_maths_s2_volume_of_cones_and_spheres as sgc
adopt(sgc)
if hasattr(sgc, 'R'): sgc.R = random.Random(707160)
import gen_uk_maths_y8_volume_and_surface_area_of_prisms as ukv
adopt(ukv)
if hasattr(ukv, 'R'): ukv.R = random.Random(707161)
import gen_cabc_math_g7_volume as cbv
adopt(cbv)
if hasattr(cbv, 'R'): cbv.R = random.Random(707162)
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


CYL = [("A water drum", "cm", (25, 30, 35, 40), (80, 90, 100), "liters"), ("A can of sardines", "cm", (3, 4), (3, 4, 5), "mL"),
       ("A water tank on a roof", "m", (0.5, 0.6, 0.7), (1, 1.2, 1.5), "liters"), ("A glass", "cm", (3, 3.5, 4), (10, 12, 14), "mL"),
       ("A rain barrel", "cm", (20, 25, 30), (60, 70, 80), "liters")]


def one_cylh(r):
    rad, h = r.randint(2, 10), r.randint(3, 20)
    V = rad * rad * h
    if r.random() < 0.5:
        q = "A cylinder has a volume of %sπ cm³ and a radius of %d cm. What is its height?" % (comma(V), rad)
        return mcq(q, "%d cm" % h, ["%d cm" % x for x in (V // rad if V % rad == 0 and V // rad != h else h + 2, h * 2, V // (2 * rad) if V % (2 * rad) == 0 and V // (2 * rad) != h else h + 1)],
                   "V = πr²h, so %sπ = π × %d × h. h = %s ÷ %d = <b>%d cm</b>." % (comma(V), rad * rad, comma(V), rad * rad, h))
    q = "A cylinder has a volume of %sπ cm³ and a height of %d cm. What is its radius?" % (comma(V), h)
    return mcq(q, "%d cm" % rad, ["%d cm" % x for x in (rad * rad, rad * 2, rad + 1)],
               "πr² × %d = %sπ, so r² = %s ÷ %d = %d and r = √%d = <b>%d cm</b>." % (h, comma(V), comma(V), h, rad * rad, rad * rad, rad))


def one_cylp(r):
    name, u, rs, hs, cap = r.choice(CYL)
    rad, h = r.choice(rs), r.choice(hs)
    V = 3.14 * rad * rad * h
    if u == "cm":
        val = V / 1000 if cap == "liters" else V
    else:
        val = V * 1000
    val = round(val, 1)
    sv = lambda x: "%s %s" % (comma(int(x)) if x == int(x) else ("%s" % comma(int(x))) + ("%.1f" % (x - int(x)))[1:], cap)
    q = "%s is a cylinder with radius %s %s and height %s %s. About how many %s does it hold? (Use π ≈ 3.14 and 1,000 cm³ = 1 L.)" % (name, rad, u, h, u, cap)
    if u == "m":
        q = q.replace("1,000 cm³ = 1 L", "1 m³ = 1,000 L")
    wrong = [round(val * 2, 1), round(3.14 * 2 * rad * h * (val / V), 1), round(val / 10, 1) if val >= 10 else round(val * 10, 1)]
    return mcq(q, sv(val), [sv(x) for x in wrong if x != val], "V = πr²h ≈ 3.14 × %s² × %s = %s %s³. That is about <b>%s</b>." % (rad, h, ("%.2f" % V).rstrip("0").rstrip("."), u, sv(val)))


def build():
    sets, R = build_sets([
        ("Volume = base area × height", [("run", cbv.set_cyl, ("rnd",), 20)]),
        ("Find the volume", [("collect", sgc.one_cyl, 20)]),
        ("Radius or diameter?", [("collect", ukv.one_cyl, 20)]),
        ("Missing radius or height", [("collect", uniq(one_cylh), 20)]),
        ("Cylinder problems", [("collect", uniq(one_cylp), 20)]),
    ], 70716)
    finish(sets, R)
    body = lesson('<ul><li>A cylinder is like a stack of equal circles. Its volume is <b>base area × height</b>.</li><li>The base is a circle with area πr², so <b>V = πr²h</b>.</li><li>If you know the diameter, halve it to get the radius first.</li><li>Volume is in cubic units: cm³ or m³. 1,000 cm³ = 1 L.</li></ul>',
        [example("r = 5 cm, h = 10 cm", ["π × 5² × 10 = 250π"], "≈ 785 cm³")],
        [['Diameter as radius', 'Halve the diameter first.'], ['Not squaring', 'r² means r × r.'], ['Using 2πr', '2πr is the circumference, not the base area.']])
    faq = [('What does MATATAG Math 7 ask about cylinders?', 'Explain inductively the volume of a cylinder using the area of a circle, find the volume of a cylinder, and solve problems involving the volumes of cylinders.'), ('Which value of π should I use?', 'Use 3.14, 22/7 or the π key, as the question says.'), ('How many liters does a 1,000 cm³ can hold?', '1 liter.'), ('Why is the formula πr²h?', 'The base area πr² is stacked h units high.')]
    make('volume-of-cylinders', 16, 'Measurement and Geometry', 'Grade 7: Measurement and Geometry',
         'Explain inductively the volume of a cylinder using the area of a circle, leading to the identification of the formula; find the volume of a cylinder; solve problems involving the volumes of cylinders.',
         'Volume of Cylinders', 'Volume of Cylinders',
         'Free Grade 7 volume of cylinders worksheets for the DepEd MATATAG curriculum: V = πr²h, radius and diameter, missing dimensions and real-life problems. 100 questions with answers.',
         'V = πr²h (base area × height).', 'Halve the diameter to get the radius.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
