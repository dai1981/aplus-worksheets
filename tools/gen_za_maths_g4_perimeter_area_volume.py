# -*- coding: utf-8 -*-
"""
South Africa Grade 4 Maths (CAPS): Perimeter, Area and Volume (Grade 4: 4.6 Perimeter, area and volume)
  python3 tools/gen_za_maths_g4_perimeter_area_volume.py
Perimeter by adding the sides, perimeter of shapes on a grid, area by counting squares, estimating area (Australia
Year 4 makers) and volume by counting cubes (US Grade 5 maker).
Wrong answers come from real mistakes: counting squares for the perimeter, adding only two sides of a rectangle, and
counting only the cubes you can see.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y4_perimeter_area as aup
adopt(aup)
if hasattr(aup, 'R'): aup.R = random.Random(804260)
import gen_us_math_g5_volume as usv
adopt(usv)
if hasattr(usv, 'R'): usv.R = random.Random(804261)
za_common.GRADE = "grade-4"



def build():
    sets, R = build_sets([
        ("Perimeter: add the sides", [("run", aup.set_add_sides, ("rnd",), 20)]),
        ("Perimeter on a grid", [("run", aup.set_rectilinear, ("rnd",), 20)]),
        ("Area by counting squares", [("run", aup.set_area, ("rnd",), 20)]),
        ("Estimate the area", [("run", aup.set_estimate, ("rnd", [0, 1, 2]), 10), ("run", aup.set_story, ("rnd", aup.People), 10)]),
        ("Volume by counting cubes", [("run", usv.set_count, ("rnd",), 20)]),
    ], 80426)
    finish(sets, R)
    body = lesson('<ul><li><b>Perimeter</b> is the distance all the way around a shape. Add the lengths of all the sides.</li><li><b>Area</b> is the space inside a shape. Count the squares that cover it (square units).</li><li><b>Volume</b> is the space a 3-D object takes up. Count the cubes that fill it (cubic units).</li><li>Count hidden cubes too: a layer of 3 × 2 cubes, 2 layers high, has 12 cubes.</li></ul>',
        [example("Rectangle 6 cm by 4 cm", ["perimeter 6 + 4 + 6 + 4 = 20 cm", "area 6 × 4 = 24 squares"], "20 cm and 24 cm²")],
        [['Squares for perimeter', 'Perimeter counts edges, not squares.'], ['Only two sides', 'A rectangle has 4 sides.'], ['Visible cubes only', 'Count the hidden cubes in each layer.']])
    faq = [('What does CAPS Grade 4 say about perimeter, area and volume?', 'Measure perimeter using rulers or measuring tapes, find areas of regular and irregular shapes by counting squares on grids, and find volume of objects by packing or filling them.'), ('What is a square unit?', 'A square used to measure area, like 1 cm².'), ('Do learners use area formulas in Grade 4?', 'No, they count squares.'), ('Can two shapes have the same area but different perimeters?', 'Yes.')]
    make('perimeter-area-and-volume', 26, 'Measurement', 'Grade 4: 4.6 Perimeter, area and volume',
         'Measure perimeter using rulers or measuring tapes; find areas of regular and irregular 2-D shapes by counting squares on grids; find volume/capacity of objects by packing or filling them.',
         'Perimeter, Area and Volume', 'Perimeter, Area and Volume',
         'Free CAPS Grade 4 perimeter, area and volume worksheets: adding sides, perimeter on grids, area by counting squares, estimating area and volume by counting cubes. 100 questions with memos.',
         'Perimeter: around. Area: inside. Volume: space filled.', 'Count squares for area and cubes for volume.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
