# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Converting Units within the SI and between Measurement Systems (Grade 7: Measurement and Geometry)
  python3 tools/gen_ph_math_g7_converting_units.py
Converting metric (SI) units of length, mass, capacity and area (UK Year 8 and Australia Year 8 makers), and
converting between metric and English units of length, mass and capacity (Texas Grade 7 makers).
Wrong answers come from real mistakes: multiplying when going to a bigger unit, using 100 for every metric unit, and
using the conversion factor upside down.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_uk_maths_y8_units_and_scale_drawings as uku
adopt(uku)
if hasattr(uku, 'R'): uku.R = random.Random(707150)
import gen_au_maths_y8_volume_and_capacity as auv
adopt(auv)
if hasattr(auv, 'R'): auv.R = random.Random(707151)
import gen_ustx_math_g7_converting_systems as txc
adopt(txc)
if hasattr(txc, 'R'): txc.R = random.Random(707152)
ph_common.ALLOW_IMPERIAL = True
ph_common.GRADE = "grade-7"



def build():
    sets, R = build_sets([
        ("Metric (SI) units", [("collect", uku.one_metric, 10), ("collect", auv.one_conv, 10)]),
        ("Length between systems", [("collect", txc.one_len, 20)]),
        ("Mass between systems", [("collect", txc.one_mass, 20)]),
        ("Capacity between systems", [("collect", txc.one_cap, 20)]),
        ("Conversion problems", [("collect", txc.one_story, 12), ("collect", txc.one_rate, 8)]),
    ], 70715)
    finish(sets, R)
    body = lesson("<ul><li>SI (metric) prefixes: kilo = 1,000, centi = <span class='fr'><span class='fn'>1</span><span class='fd'>100</span></span>, milli = <span class='fr'><span class='fn'>1</span><span class='fd'>1,000</span></span>. 1 km = 1,000 m, 1 m = 100 cm, 1 kg = 1,000 g, 1 L = 1,000 mL.</li><li>Bigger unit to smaller unit: multiply. Smaller to bigger: divide.</li><li>English units still used in the Philippines: 1 inch = 2.54 cm, 1 foot = 12 inches ≈ 30.48 cm, 1 mile ≈ 1.61 km, 1 pound ≈ 0.454 kg, 1 gallon ≈ 3.79 L.</li><li>Write the factor so the old unit cancels: 5 ft × <span class='fr'><span class='fn'>30.48 cm</span><span class='fd'>1 ft</span></span>.</li></ul>",
        [example("A TV screen of 32 inches", ["32 × 2.54"], "81.28 cm"), example("3.5 kg", ["3.5 × 1,000"], "3,500 g")],
        [['Multiplying to a bigger unit', 'cm to m: divide by 100.'], ['100 for every unit', 'Only m–cm uses 100 in length; kilo and milli use 1,000.'], ['Factor upside down', 'The old unit must cancel.']])
    faq = [('What does MATATAG Math 7 ask about units?', 'Convert units of measure within the International System of Units (SI) and across different systems of measure.'), ('Where are inches used in the Philippines?', 'For TV and phone screens, waist sizes and lumber; height is often given in feet and inches.'), ('How many centimeters are in 1 inch?', 'Exactly 2.54 cm.'), ('What is SI?', 'The International System of Units, based on meters, kilograms, seconds and others.')]
    make('converting-units-of-measure', 15, 'Measurement and Geometry', 'Grade 7: Measurement and Geometry',
         'Convert units of measure within the International System of Units (SI) and across different systems of measure.',
         'Converting Units within the SI and between Measurement Systems', 'Converting Units',
         'Free Grade 7 unit conversion worksheets for the DepEd MATATAG curriculum: metric (SI) units and converting between metric and English units of length, mass and capacity. 100 questions with answers.',
         'Bigger to smaller unit: multiply. Smaller to bigger: divide.', '1 inch = 2.54 cm; 1 kg ≈ 2.2 pounds.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
