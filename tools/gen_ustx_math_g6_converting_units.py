# -*- coding: utf-8 -*-
"""
Texas Grade 6 Math: Converting Units Within a Measurement System (TEKS 6.4H)
  python3 tools/gen_ustx_math_g6_converting_units.py
Conversion ratios, ratio tables and double number lines, conversions with fractions and decimals, customary and
metric conversions, and multi-step word problems (the US Grade 6 makers, plus own conversions).
Wrong answers come from real mistakes: multiplying when you should divide, using the wrong conversion factor, and
forgetting to convert before comparing.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g6_unit_conversions as uc
adopt(uc)
tx_common.GRADE = "grade-6"

CONV = [("ft", "in", 12, "feet", "inches"), ("yd", "ft", 3, "yards", "feet"), ("mi", "ft", 5280, "miles", "feet"), ("gal", "qt", 4, "gallons", "quarts"),
        ("qt", "pt", 2, "quarts", "pints"), ("pt", "c", 2, "pints", "cups"), ("lb", "oz", 16, "pounds", "ounces"), ("T", "lb", 2000, "tons", "pounds"),
        ("m", "cm", 100, "meters", "centimeters"), ("km", "m", 1000, "kilometers", "meters"), ("L", "mL", 1000, "liters", "milliliters"),
        ("kg", "g", 1000, "kilograms", "grams"), ("cm", "mm", 10, "centimeters", "millimeters"), ("h", "min", 60, "hours", "minutes")]


def one_conv(r):
    big, small, k, bn, sn = r.choice(CONV)
    if r.random() < 0.5:
        n = r.randint(2, 12) if k >= 1000 else r.randint(2, 30)
        v = n * k
        return mcq("Convert. %d %s = ? %s" % (n, bn, sn), "%s %s" % (comma(v), sn), ["%s %s" % (comma(n * k * 10) if k >= 100 else comma(n + k), sn), "%d %s" % (n, sn), "%s %s" % (comma(v // 10) if k >= 100 else comma(n * k - k), sn)],
                   "1 %s = %s %s. A bigger unit to a smaller unit: multiply. %d × %s = <b>%s %s</b>." % (bn[:-1] if bn != "feet" else "foot", comma(k), sn, n, comma(k), comma(v), sn))
    n = r.randint(2, 20)
    v = n * k
    return mcq("Convert. %s %s = ? %s" % (comma(v), sn, bn), "%d %s" % (n, bn), ["%s %s" % (comma(v * k), bn), "%s %s" % (comma(v - k), bn), "%d %s" % (n * 10, bn)],
               "A smaller unit to a bigger unit: divide. %s ÷ %s = <b>%d %s</b>." % (comma(v), comma(k), n, bn))


def build():
    sets, R = build_sets([
        ("The conversion ratio: multiply or divide?", [("run", uc.set_ratio, ("rnd",), 20)]),
        ("Customary and metric conversions", [("collect", one_conv, 20)]),
        ("Ratio tables and double number lines", [("run", uc.set_tables, (), 20)]),
        ("Fractions, decimals and mixed units", [("run", uc.set_mixed, (), 20)]),
        ("Multi-step word problems", [("run", uc.set_story, ("rnd",), 20)]),
    ], 66011)
    finish(sets, R)
    body = lesson('<ul><li>A conversion is a <b>ratio</b>: 1 ft : 12 in.</li><li>From a <b>bigger unit to a smaller unit</b>, multiply: 3 ft = 3 × 12 = 36 in.</li><li>From a <b>smaller unit to a bigger unit</b>, divide: 48 oz = 48 ÷ 16 = 3 lb.</li><li>Metric units change by powers of 10: 1 km = 1,000 m, 1 m = 100 cm, 1 L = 1,000 mL.</li></ul>',
        [example("5 gal = ? qt", ["1 gal = 4 qt", "5 × 4"], "20 qt"), example("2,500 g = ? kg", ["1 kg = 1,000 g", "2,500 ÷ 1,000"], "2.5 kg")],
        [['Multiplying when you should divide', 'Smaller to bigger units gives a smaller number: divide.'], ['Using the wrong conversion factor', '1 yd = 3 ft, but 1 ft = 12 in.'], ['Comparing without converting', 'Change both measures to the same unit first.']])
    faq = [('What does TEKS 6.4H ask?', 'Convert units within a measurement system, including the use of proportions and unit rates.'), ('How do I know whether to multiply or divide?', 'More of a small unit fits in a big unit, so going to the smaller unit gives a bigger number: multiply.'), ('Can I use a ratio table?', 'Yes. Start with 1 big unit and its small units, then scale both.'), ('What does within a system mean?', 'Customary to customary (feet to inches) or metric to metric (meters to centimeters).')]
    make('converting-units', 11, 'Proportionality', '6.4H',
         '6.4H convert units within a measurement system, including the use of proportions and unit rates',
         'Converting Units Within a Measurement System', 'Converting Units',
         'Free Grade 6 unit conversion worksheets for Texas TEKS 6.4H: conversion ratios, customary and metric conversions, ratio tables, fractions and decimals, and word problems. 100 questions with answers.',
         'Bigger to smaller unit: multiply. Smaller to bigger unit: divide.', '5 gal = 20 qt. 2,500 g = 2.5 kg.',
         body, faq, sets, seo_title='Grade 6 Converting Units Worksheets: Customary and Metric (TEKS 6.4H, STAAR)')


if __name__ == "__main__":
    build()
