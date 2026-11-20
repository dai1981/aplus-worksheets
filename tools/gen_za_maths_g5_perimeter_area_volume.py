# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): Perimeter, Area and Volume (Grade 5: 4.6 Perimeter, area and volume)
  python3 tools/gen_za_maths_g5_perimeter_area_volume.py
Perimeter of polygons, area of rectangles and composite shapes by counting squares, and volume of rectangular
prisms by counting cubes (Australia Year 5, UK Year 5, BC Grade 5 and US Grade 5 makers).
Wrong answers come from real mistakes: adding only two sides for the perimeter, mixing up area and perimeter, and
counting only the cubes you can see.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y5_perimeter_area as aup
adopt(aup)
if isinstance(getattr(aup, 'R', None), random.Random): aup.R = random.Random(805270)
import gen_uk_maths_y5_area_perimeter as uka
adopt(uka)
if isinstance(getattr(uka, 'R', None), random.Random): uka.R = random.Random(805271)
import gen_cabc_math_g5_area_perimeter as cba
adopt(cba)
if isinstance(getattr(cba, 'R', None), random.Random): cba.R = random.Random(805272)
import gen_us_math_g5_volume as usv
adopt(usv)
if isinstance(getattr(usv, 'R', None), random.Random): usv.R = random.Random(805273)
za_common.GRADE = "grade-5"


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



def build():
    sets, R = build_sets([
        ("Perimeter", [("run", aup.set_perimeter, ("rnd", "seen"), 10, nodec), ("run", cba.set_perimeter, ("rnd", cba.People), 10, nodec)]),
        ("Area by counting squares", [("run", cba.set_count, ("rnd", cba.People), 20, nodec)]),
        ("Area of rectangles", [("run", aup.set_rect_area, ("rnd",), 10, nodec), ("run", uka.set_composite_area, ("rnd", "seen"), 10, nodec)]),
        ("Volume by counting cubes", [("run", usv.set_count, ("rnd",), 20, nodec)]),
        ("Perimeter or area?", [("run", cba.set_story, ("rnd", cba.People), 20, nodec)]),
    ], 80527)
    finish(sets, R)
    body = lesson('<ul><li><b>Perimeter</b> is the distance around a shape: add all the sides.</li><li><b>Area</b> is the space inside a shape: count the squares. A rectangle has rows × columns squares.</li><li><b>Volume</b> is the space an object takes up: count the cubes, including hidden ones.</li><li>Perimeter is in cm or m; area in square units (cm²); volume in cubic units (cm³).</li></ul>',
        [example("A rectangle 6 cm by 4 cm", ["perimeter: 6 + 4 + 6 + 4", "area: 6 × 4 squares"], "20 cm and 24 cm²")],
        [['Two sides only', 'Add all four sides.'], ['Area or perimeter?', 'Area is inside; perimeter is around.'], ['Visible cubes only', 'Count the hidden cubes too.']])
    faq = [('What does CAPS Grade 5 say about perimeter, area and volume?', 'Measure the perimeter of polygons, find the area of regular and irregular shapes by counting squares on grids, and find the volume of rectangular prisms by counting or packing cubes.'), ('Can two shapes have the same area but different perimeters?', 'Yes.'), ('What is a square centimetre?', 'A square with sides of 1 cm.'), ('How do I count hidden cubes?', 'Count one layer, then multiply by the number of layers.')]
    make('perimeter-area-and-volume', 27, 'Measurement', 'Grade 5: 4.6 Perimeter, area and volume',
         'Measure perimeter using rulers or measuring tapes; find areas of regular and irregular shapes by counting squares on grids in order to develop an understanding of square units; find volume or capacity of objects by packing or filling them, and by counting cubes in order to develop an understanding of cubic units.',
         'Perimeter, Area and Volume', 'Perimeter, Area and Volume',
         'Free CAPS Grade 5 perimeter, area and volume worksheets: perimeter of polygons, area by counting squares and volume by counting cubes. 100 questions with memos.',
         'Perimeter: around. Area: inside. Volume: space taken up.', 'Count hidden cubes too.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
