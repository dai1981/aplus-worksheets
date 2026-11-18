# -*- coding: utf-8 -*-
"""
Texas Grade 8 Math: Lateral and Total Surface Area of Prisms and Cylinders (TEKS 8.7B)
  python3 tools/gen_ustx_math_g8_surface_area.py
Surface area of rectangular prisms (US Grade 7 maker with a new seed), triangular prisms, lateral and total surface
area of cylinders, and word problems (own makers).
Wrong answers come from real mistakes: using the radius instead of the circumference for the lateral area,
counting only one base, and using the diameter as the radius.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g7_area_surface_area_volume as asv
adopt(asv)
asv.R = random.Random(680180)
tx_common.GRADE = "grade-8"

from fractions import Fraction as F
from ws_common import num

INK = "#1f2937"


def g(v):
    s = ("%.2f" % v).rstrip("0").rstrip(".")
    if "." in s:
        a, b = s.split(".")
        return ("−" if v < 0 else "") + comma(abs(int(a))) + "." + b
    return num(int(s))


def pt(p):
    return "(%s, %s)" % (g(p[0]), g(p[1]))


def one_tri(r):
    a, b, c = r.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17)])
    L = r.randint(4, 20)
    base = a * b / 2.0
    lat = (a + b + c) * L
    tot = lat + 2 * base
    if r.random() < 0.5:
        return mcq("A triangular prism has a right-triangle base with sides %d, %d and %d inches. It is %d inches long. What is its lateral surface area?" % (a, b, c, L), "%s in²" % comma(lat), ["%s in²" % g(tot), "%s in²" % g(base * L), "%s in²" % comma((a + b) * L)],
                   "Lateral area = perimeter of the base × length = (%d + %d + %d) × %d = <b>%s in²</b>." % (a, b, c, L, comma(lat)))
    return mcq("A triangular prism has a right-triangle base with sides %d, %d and %d inches. It is %d inches long. What is its total surface area?" % (a, b, c, L), "%s in²" % g(tot), ["%s in²" % comma(lat), "%s in²" % g(lat + base), "%s in²" % g(base * L)],
               "Lateral: %d × %d = %d. Two bases: 2 × ½ × %d × %d = %s. Total = <b>%s in²</b>." % (a + b + c, L, lat, a, b, g(2 * base), g(tot)))


def one_cyl(r):
    rad, h = r.randint(2, 10), r.randint(3, 15)
    lat = 2 * 3.14 * rad * h
    tot = lat + 2 * 3.14 * rad * rad
    kind = r.choice(["lat", "tot", "pi"])
    if kind == "lat":
        return mcq("A cylinder has radius %d cm and height %d cm. What is its lateral surface area? Use 3.14 for π." % (rad, h), "%s cm²" % g(lat), ["%s cm²" % g(tot), "%s cm²" % g(3.14 * rad * h), "%s cm²" % g(3.14 * rad * rad * h)],
                   "Lateral area = 2πrh = 2 × 3.14 × %d × %d = <b>%s cm²</b>." % (rad, h, g(lat)))
    if kind == "tot":
        return mcq("A cylinder has radius %d cm and height %d cm. What is its total surface area? Use 3.14 for π." % (rad, h), "%s cm²" % g(tot), ["%s cm²" % g(lat), "%s cm²" % g(lat + 3.14 * rad * rad), "%s cm²" % g(3.14 * rad * rad * h)],
                   "2πrh + 2πr² = %s + %s = <b>%s cm²</b>." % (g(lat), g(2 * 3.14 * rad * rad), g(tot)))
    d = 2 * rad
    return mcq("A cylinder has a diameter of %d m and a height of %d m. What is its total surface area in terms of π?" % (d, h), "%dπ m²" % (2 * rad * h + 2 * rad * rad), ["%dπ m²" % (2 * d * h + 2 * d * d), "%dπ m²" % (2 * rad * h), "%dπ m²" % (rad * rad * h)],
               "r = %d. 2πrh + 2πr² = %dπ + %dπ = <b>%dπ m²</b>." % (rad, 2 * rad * h, 2 * rad * rad, 2 * rad * h + 2 * rad * rad))


def one_story(r):
    kind = r.choice(["label", "tank", "box", "tent"])
    if kind == "label":
        rad, h = r.choice([3, 4, 5]), r.choice([10, 11, 12, 15])
        lat = 2 * 3.14 * rad * h
        return mcq("A paper label covers the side of a soup can (not the top or bottom). The can has radius %d cm and height %d cm. How much paper is needed? Use 3.14 for π." % (rad, h), "%s cm²" % g(lat),
                   ["%s cm²" % g(lat + 2 * 3.14 * rad * rad), "%s cm²" % g(3.14 * rad * rad * h), "%s cm²" % g(3.14 * rad * h)], "Only the side: 2πrh = <b>%s cm²</b>." % g(lat))
    if kind == "tank":
        rad, h = r.choice([2, 3, 4]), r.choice([5, 6, 8])
        tot = 2 * 3.14 * rad * h + 2 * 3.14 * rad * rad
        return mcq("A closed water tank is a cylinder with radius %d ft and height %d ft. How much metal covers the whole tank? Use 3.14 for π." % (rad, h), "%s ft²" % g(tot), ["%s ft²" % g(2 * 3.14 * rad * h), "%s ft²" % g(3.14 * rad * rad * h), "%s ft²" % g(tot - 3.14 * rad * rad)],
                   "2πrh + 2πr² = <b>%s ft²</b>." % g(tot))
    if kind == "box":
        l, w, h = r.randint(8, 20), r.randint(5, 12), r.randint(3, 10)
        s = 2 * (l * w + l * h + w * h)
        return mcq("A gift box is %d in. by %d in. by %d in. How much wrapping paper covers it exactly?" % (l, w, h), "%s in²" % comma(s), ["%s in²" % comma(l * w * h), "%s in²" % comma(l * w + l * h + w * h), "%s in²" % comma(2 * (l + w) * h)],
                   "2(lw + lh + wh) = 2(%d + %d + %d) = <b>%s in²</b>." % (l * w, l * h, w * h, comma(s)))
    a, b, c = 6, 8, 10
    L = r.choice([7, 8, 9, 10])
    tot = (a + b + c) * L + a * b
    return mcq("A tent is a triangular prism with a right-triangle front (sides 6 ft, 8 ft and 10 ft) and length %d ft. How much fabric covers all of it, including the floor and both ends?" % L, "%s ft²" % comma(tot), ["%s ft²" % comma((a + b + c) * L), "%s ft²" % comma(a * b * L // 2), "%s ft²" % comma((a + b + c) * L + a * b // 2)],
               "Lateral: 24 × %d = %d. Two ends: 2 × 24 = 48. Total = <b>%s ft²</b>." % (L, 24 * L, comma(tot)))


def build():
    sets, R = build_sets([
        ("Surface area of rectangular prisms", [("run", asv.set_surface, (), 20)]),
        ("Triangular prisms", [("collect", one_tri, 20)]),
        ("Cylinders: lateral and total", [("collect", one_cyl, 20)]),
        ("Mixed practice", [("collect", one_cyl, 10), ("collect", one_tri, 10)]),
        ("Word problems", [("collect", one_story, 20)]),
    ], 68018)
    finish(sets, R)
    body = lesson('<ul><li><b>Lateral area</b> of a prism = perimeter of the base × height (the sides only).</li><li><b>Total area</b> = lateral area + 2 × area of the base.</li><li>A cylinder unrolls into a rectangle and two circles: lateral area = 2πrh, total = 2πrh + 2πr².</li><li>Surface area is in square units.</li></ul>',
        [example("Cylinder r = 3 cm, h = 10 cm", ["2 × 3.14 × 3 × 10 = 188.4", "+ 2 × 3.14 × 9 = 56.52"], "244.92 cm²")],
        [['Using πrh for the lateral area', "The rectangle's width is the circumference, 2πr."], ['Counting only one base', 'A closed prism or cylinder has two bases.'], ['Using the diameter as the radius', 'r = d ÷ 2.']])
    faq = [('What does TEKS 8.7B ask?', 'Use previous knowledge of surface area to make connections to the formulas for lateral and total surface area and determine solutions for problems involving rectangular prisms, triangular prisms and cylinders.'), ('Why is the lateral area of a cylinder 2πrh?', 'Unrolled, the side is a rectangle whose length is the circumference 2πr and whose width is h.'), ('When do I use lateral area only?', 'For labels, walls or open tubes without tops or bottoms.'), ('What is the base of a triangular prism?', 'The triangle at each end.')]
    make('surface-area-of-prisms-and-cylinders', 18, 'Expressions, Equations and Relationships', '8.7B',
         '8.7B use previous knowledge of surface area to make connections to the formulas for lateral and total surface area and determine solutions for problems involving rectangular prisms, triangular prisms, and cylinders',
         'Lateral and Total Surface Area of Prisms and Cylinders', 'Surface Area of Prisms and Cylinders',
         'Free Grade 8 surface area worksheets for Texas TEKS 8.7B: lateral and total surface area of rectangular prisms, triangular prisms and cylinders, and word problems. 100 questions with answers.',
         'Lateral = perimeter of base × height. Total = lateral + 2 bases.', 'Cylinder: 2πrh + 2πr².',
         body, faq, sets, seo_title='Grade 8 Surface Area of Prisms and Cylinders Worksheets (TEKS 8.7B, STAAR)')


if __name__ == "__main__":
    build()
