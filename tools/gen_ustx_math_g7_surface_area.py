# -*- coding: utf-8 -*-
"""
Texas Grade 7 Math: Lateral and Total Surface Area with Nets (TEKS 7.9D)
  python3 tools/gen_ustx_math_g7_surface_area.py
Faces and nets (US Grade 6 maker), surface area of rectangular prisms (US Grade 7 maker), lateral versus total
surface area (own), pyramids and triangular prisms, and word problems (US Grade 6 makers with Texas names).
Wrong answers come from real mistakes: counting each pair of faces once, including the bases in lateral area, and
mixing up area and volume.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g7_area_surface_area_volume as asv
adopt(asv)
asv.R = random.Random(670150)
import gen_us_math_g6_surface_area as sa6
adopt(sa6)
tx_common.GRADE = "grade-7"

INK = "#1f2937"
FILL = "#dbeafe"


def g(v):
    s = ("%.2f" % v).rstrip("0").rstrip(".")
    if "." in s:
        a, b = s.split(".")
        return comma(int(a)) + "." + b
    return comma(int(s))


def txt(x, y, t, anchor="middle", col=INK):
    return "<text x='%.1f' y='%.1f' font-size='13' text-anchor='%s' fill='%s'>%s</text>" % (x, y, anchor, col, t)


def one_lateral(r):
    l, w, h = r.randint(3, 15), r.randint(2, 10), r.randint(2, 12)
    lat = 2 * (l + w) * h
    tot = lat + 2 * l * w
    if r.random() < 0.5:
        return mcq("A rectangular prism is %d cm long, %d cm wide and %d cm tall. What is its <b>lateral</b> surface area (the four side faces)?" % (l, w, h), "%s cm²" % comma(lat), ["%s cm²" % comma(tot), "%s cm²" % comma(l * w * h), "%s cm²" % comma((l + w) * h)],
                   "Lateral area = perimeter of the base × height = 2(%d + %d) × %d = <b>%s cm²</b>." % (l, w, h, comma(lat)))
    return mcq("A rectangular prism is %d cm long, %d cm wide and %d cm tall. Its lateral area is %s cm². What is its <b>total</b> surface area?" % (l, w, h, comma(lat)), "%s cm²" % comma(tot), ["%s cm²" % comma(lat + l * w), "%s cm²" % comma(lat), "%s cm²" % comma(l * w * h)],
               "Total = lateral + 2 bases = %s + 2 × %d × %d = <b>%s cm²</b>." % (comma(lat), l, w, comma(tot)))


def build():
    sets, R = build_sets([
        ("Faces and nets", [("run", sa6.set_faces, ("rnd",), 20)]),
        ("Surface area of rectangular prisms", [("run", asv.set_surface, (), 20)]),
        ("Lateral and total surface area", [("collect", one_lateral, 20)]),
        ("Pyramids and triangular prisms", [("run", sa6.set_pyr_tri, ("rnd",), 20)]),
        ("Word problems", [("run", sa6.set_story, ("rnd", sa6.People), 20)]),
    ], 67015)
    finish(sets, R)
    body = lesson('<ul><li>A <b>net</b> is a flat pattern that folds into a solid. The surface area is the total area of the net.</li><li><b>Lateral</b> surface area is the area of the sides only (no bases). For a prism: perimeter of the base × height.</li><li><b>Total</b> surface area = lateral area + the areas of the bases.</li><li>A rectangular pyramid has 1 rectangle base and 4 triangle faces; a triangular prism has 2 triangle bases and 3 rectangles.</li></ul>',
        [example("Box 5 cm × 3 cm × 4 cm", ["Lateral: 2(5 + 3) × 4 = 64", "Bases: 2 × 15 = 30"], "94 cm²")],
        [['Counting each pair of faces once', 'A box has 6 faces: 3 pairs.'], ['Including the bases in lateral area', 'Lateral area is the sides only.'], ['Mixing up surface area and volume', 'Surface area is in square units; volume is in cubic units.']])
    faq = [('What does TEKS 7.9D ask?', "Solve problems involving the lateral and total surface area of a rectangular prism, rectangular pyramid, triangular prism and triangular pyramid by determining the area of the shape's net."), ('What is the difference between lateral and total surface area?', 'Total surface area includes the bases; lateral does not.'), ('When do I use lateral area?', 'For things with no top or bottom, like the label on a box or the walls of a room.'), ("How do I find the area of a pyramid's net?", 'Add the base and the triangle faces: ½ × base × slant height for each triangle.')]
    make('lateral-and-total-surface-area', 15, 'Expressions, Equations and Relationships', '7.9D',
         "7.9D solve problems involving the lateral and total surface area of a rectangular prism, rectangular pyramid, triangular prism, and triangular pyramid by determining the area of the shape's net",
         'Lateral and Total Surface Area with Nets', 'Lateral and Total Surface Area',
         'Free Grade 7 surface area worksheets for Texas TEKS 7.9D: nets, rectangular prisms, lateral and total surface area, pyramids and triangular prisms, and word problems. 100 questions with answers.',
         'Lateral = sides only. Total = lateral + bases.', 'Box 5 × 3 × 4: lateral 64 cm², total 94 cm².',
         body, faq, sets, seo_title='Grade 7 Lateral and Total Surface Area Worksheets with Nets (TEKS 7.9D, STAAR)')


if __name__ == "__main__":
    build()
