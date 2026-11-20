# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Perimeter, Area and Volume of Rectangles and Rectangular Prisms (Grade 6: 4.6 Perimeter, area and volume)
  python3 tools/gen_za_maths_g6_perimeter_area_volume.py
Perimeter of rectangles, regular polygons and composite shapes, area of rectangles and composite shapes, and volume
of rectangular prisms (BC Grade 6, Australia Year 6 and UK Year 6 makers).
Wrong answers come from real mistakes: adding only two sides for the perimeter, mixing up area and perimeter, and
adding the lengths for the volume.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_cabc_math_g6_perimeter as cbp
adopt(cbp)
if isinstance(getattr(cbp, 'R', None), random.Random): cbp.R = random.Random(806310)
import gen_au_maths_y6_area_rectangles as aua
adopt(aua)
if isinstance(getattr(aua, 'R', None), random.Random): aua.R = random.Random(806311)
import gen_cabc_math_g6_volume as cbv
adopt(cbv)
if isinstance(getattr(cbv, 'R', None), random.Random): cbv.R = random.Random(806312)
import gen_uk_maths_y6_area_volume as uka
adopt(uka)
if isinstance(getattr(uka, 'R', None), random.Random): uka.R = random.Random(806313)
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
        ("Perimeter", [("run", cbp.set_rect, (), 10, dec3), ("run", cbp.set_regular, (), 10, dec3)]),
        ("Area of rectangles", [("run", aua.set_grids, ("rnd",), 10, dec3), ("run", uka.set_rect, ("rnd",), 10, dec3)]),
        ("Composite shapes", [("run", cbp.set_composite, (), 10, dec3), ("run", aua.set_composite, ("rnd", "seen"), 10, dec3)]),
        ("Volume of rectangular prisms", [("run", cbv.set_count, ("rnd",), 10, dec3), ("run", cbv.set_rect, ("rnd",), 10, dec3)]),
        ("Perimeter, area and volume problems", [("run", aua.set_story, ("rnd", aua.People, "seen"), 10, dec3), ("run", cbv.set_story, (), 10, dec3)]),
    ], 80631)
    finish(sets, R)
    body = lesson('<ul><li><b>Perimeter</b>: add all the sides. Rectangle: 2 × (length + breadth).</li><li><b>Area</b> of a rectangle: length × breadth, in square units (cm², m²).</li><li>For a composite shape, split it into rectangles.</li><li><b>Volume</b> of a rectangular prism: length × breadth × height, in cubic units (cm³).</li></ul>',
        [example("A box 6 cm by 4 cm by 5 cm", ["6 × 4 = 24 cubes in a layer", "5 layers"], "120 cm³")],
        [['Two sides only', 'Add all four sides.'], ['Area or perimeter?', 'Area is inside; perimeter is around.'], ['Adding for volume', 'Multiply length, breadth and height.']])
    faq = [('What does CAPS Grade 6 say about perimeter, area and volume?', 'Measure perimeter, find areas of regular and irregular shapes, and find the volume of rectangular prisms, using square and cubic units.'), ('What is the area of a 7 m by 3 m room?', '21 m².'), ('What does cm³ mean?', 'Cubic centimetres.'), ('How do I find the area of an L-shape?', 'Split it into two rectangles.')]
    make('perimeter-area-and-volume', 31, 'Measurement', 'Grade 6: 4.6 Perimeter, area and volume',
         'Measure perimeter using rulers or measuring tapes; measurement of area: find areas of regular and irregular shapes by counting squares on grids, and investigate the relationship between the area and the lengths of rectangles; measurement of volume: find the volume of rectangular prisms by packing or counting cubes, and investigate the relationship between volume and the length, breadth and height.',
         'Perimeter, Area and Volume of Rectangles and Rectangular Prisms', 'Perimeter, Area and Volume',
         'Free CAPS Grade 6 perimeter, area and volume worksheets: perimeter, area of rectangles and composite shapes and volume of rectangular prisms. 100 questions with memos.',
         'Area = l × b. Volume = l × b × h.', 'Split composite shapes into rectangles.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
