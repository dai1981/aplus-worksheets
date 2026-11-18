# -*- coding: utf-8 -*-
"""
Texas Grade 4 Math: Measurement Conversions: Customary and Metric Units (TEKS 4.8A, 4.8B)
  python3 tools/gen_ustx_math_g4_conversions.py
Relative sizes of customary and metric units, converting from a larger unit to a smaller unit, mixed units,
conversion tables (the US Grade 4 makers with Texas names), and converting from a smaller unit to a larger unit.
Wrong answers come from real mistakes: dividing when converting to a smaller unit, using 10 for every conversion,
and mixing up feet and yards.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g4_conversions as usc
adopt(usc)
tx_common.GRADE = "grade-4"

BIG = [("feet", "inches", 12), ("yards", "feet", 3), ("gallons", "quarts", 4), ("quarts", "pints", 2), ("pints", "cups", 2),
       ("pounds", "ounces", 16), ("meters", "centimeters", 100), ("kilometers", "meters", 1000), ("liters", "milliliters", 1000),
       ("kilograms", "grams", 1000), ("hours", "minutes", 60), ("minutes", "seconds", 60), ("days", "hours", 24), ("weeks", "days", 7)]


def one_rel(r):
    big, small, f = r.choice(BIG)
    one = big[:-1] if big != "feet" else "foot"
    return mcq("Which is greater: 1 %s or 1 %s?" % (one, small[:-1] if small != "feet" else "foot"), "1 %s" % one, ["1 %s" % (small[:-1] if small != "feet" else "foot"), "They are equal", "We cannot tell"],
               "1 %s = %s %s, so <b>1 %s</b> is greater." % (one, comma(f), small, one))


def one_mixed(r):
    big, small, f = r.choice([b for b in BIG if b[2] <= 60])
    a, b = r.randint(2, 9), r.randint(1, f - 1)
    ab = {"feet": "ft", "inches": "in.", "yards": "yd", "pounds": "lb", "ounces": "oz", "hours": "h", "minutes": "min", "seconds": "s", "days": "d", "weeks": "wk",
          "gallons": "gal", "quarts": "qt", "pints": "pt", "cups": "c"}
    if big not in ab or small not in ab:
        return None
    t = a * f + b
    return mcq("%d %s %d %s = ? %s" % (a, ab[big], b, ab[small], small), t, [a + b, a * f, a * 10 + b, t + f],
               "%d %s = %d × %d = %d %s. Add %d: <b>%d %s</b>." % (a, big, a, f, a * f, small, b, t, small))


def one_up(r):
    big, small, f = r.choice(BIG)
    n = r.randint(2, 12) if f < 100 else r.randint(2, 9)
    q = "How many %s are in %s %s?" % (big, comma(n * f), small)
    return mcq(q, n, [n * f * f if n * f * f < 100000 else n + f, n * f - f, n + 1, f], "1 %s = %s %s. %s ÷ %s = <b>%d %s</b>." % (big[:-1] if big != "feet" else "foot", comma(f), small, comma(n * f), comma(f), n, big))


def build():
    sets, R = build_sets([
        ("How big is each unit?", [("run", usc.set_sizes, ("rnd",), 14), ("collect", one_rel, 6)]),
        ("Change to a smaller unit", [("run", usc.set_convert, ("rnd",), 20)]),
        ("Change to a larger unit", [("collect", one_up, 20)]),
        ("Mixed units and comparing", [("run", usc.set_mixed, ("rnd",), 12), ("collect", one_mixed, 8)]),
        ("Conversion tables", [("run", usc.set_tables, ("rnd",), 20)]),
    ], 64021)
    finish(sets, R)
    body = lesson('<ul><li>Customary: 1 foot = 12 inches, 1 yard = 3 feet, 1 pound = 16 ounces, 1 gallon = 4 quarts, 1 quart = 2 pints, 1 pint = 2 cups.</li><li>Metric: 1 meter = 100 centimeters, 1 kilometer = 1,000 meters, 1 kilogram = 1,000 grams, 1 liter = 1,000 milliliters.</li><li>Larger unit to smaller unit: <b>multiply</b>. Smaller unit to larger unit: <b>divide</b>. A table of equivalent measures helps.</li></ul>',
        [example("5 yards = ? feet", ["1 yard = 3 feet", "5 × 3 = 15"], "15 feet"), example("48 ounces = ? pounds", ["1 pound = 16 ounces", "48 ÷ 16 = 3"], "3 pounds")],
        [['Dividing when changing to a smaller unit', 'Smaller units mean more of them: multiply.'], ['Using 10 for every conversion', 'Check the table: 12 inches in a foot, 16 ounces in a pound.'], ['Mixing up feet and yards', 'A yard is longer: 1 yard = 3 feet.']])
    faq = [('What does TEKS 4.8A ask?', 'Identify the relative sizes of measurement units within the customary and metric systems.'), ('What does TEKS 4.8B ask?', 'Convert measurements within the same system from a smaller unit to a larger unit or a larger unit to a smaller unit, using a table of equivalent measures.'), ('When do I multiply and when do I divide?', 'Multiply to change to a smaller unit (you need more of them). Divide to change to a larger unit.'), ('Do I have to memorize the conversions?', 'On the STAAR Grade 4 test a reference chart is given, but knowing the common ones makes problems faster.')]
    make('measurement-conversions', 21, 'Geometry and Measurement', '4.8A, 4.8B',
         '4.8A identify relative sizes of measurement units within the customary and metric systems; 4.8B convert measurements within the same measurement system, customary or metric, from a smaller unit into a larger unit or a larger unit into a smaller unit when given other equivalent measures represented in a table',
         'Measurement Conversions: Customary and Metric Units', 'Measurement Conversions',
         'Free Grade 4 measurement worksheets for Texas TEKS 4.8A and 4.8B: sizes of customary and metric units, convert to smaller and larger units, mixed units and conversion tables. 100 questions with answers.',
         'To a smaller unit: multiply. To a larger unit: divide.', '1 foot = 12 inches, 1 yard = 3 feet, 1 pound = 16 ounces, 1 kilogram = 1,000 grams, 1 liter = 1,000 milliliters.',
         body, faq, sets, seo_title='Grade 4 Measurement Conversions Worksheets: Customary and Metric (TEKS 4.8A, 4.8B, STAAR)')


if __name__ == "__main__":
    build()
