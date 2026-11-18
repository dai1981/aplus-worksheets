# -*- coding: utf-8 -*-
"""
Texas Grade 7 Math: Converting Between Customary and Metric Units (TEKS 7.4E)
  python3 tools/gen_ustx_math_g7_converting_systems.py
Converting length, mass and weight, and capacity between customary and metric units with given conversion factors,
using proportions and unit rates, and word problems.
Wrong answers come from real mistakes: multiplying when you should divide, using the wrong factor, and rounding too
early.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)

tx_common.GRADE = "grade-7"

LEN = [("inches", "centimeters", 2.54, "1 inch = 2.54 centimeters"), ("miles", "kilometers", 1.6, "1 mile ≈ 1.6 kilometers"), ("meters", "feet", 3.28, "1 meter ≈ 3.28 feet"),
       ("yards", "meters", 0.91, "1 yard ≈ 0.91 meter"), ("feet", "centimeters", 30.48, "1 foot = 30.48 centimeters")]
MASS = [("kilograms", "pounds", 2.2, "1 kilogram ≈ 2.2 pounds"), ("ounces", "grams", 28.35, "1 ounce ≈ 28.35 grams"), ("pounds", "grams", 454, "1 pound ≈ 454 grams")]
CAP = [("liters", "quarts", 1.06, "1 liter ≈ 1.06 quarts"), ("gallons", "liters", 3.79, "1 gallon ≈ 3.79 liters"), ("cups", "milliliters", 237, "1 cup ≈ 237 milliliters")]


def g(v):
    s = ("%.2f" % v).rstrip("0").rstrip(".")
    return comma(int(s)) if "." not in s else comma(int(s.split(".")[0])) + "." + s.split(".")[1]


def conv(r, table):
    a, b, k, note = r.choice(table)
    n = r.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25])
    if r.random() < 0.55:
        v = round(n * k, 2)
        return mcq("Use %s. Convert %d %s to %s." % (note, n, a, b), "%s %s" % (g(v), b), ["%s %s" % (g(round(n / k, 2)), b), "%s %s" % (g(n + k), b), "%s %s" % (g(round(v * 10, 2)), b)],
                   "Multiply by the conversion factor: %d × %s = <b>%s %s</b>." % (n, g(k), g(v), b))
    v = round(n * k, 2)
    return mcq("Use %s. Convert %s %s to %s." % (note, g(v), b, a), "%d %s" % (n, a), ["%s %s" % (g(round(v * k, 2)), a), "%s %s" % (g(round(v - k, 2)), a), "%d %s" % (n * 10, a)],
               "Divide by the conversion factor: %s ÷ %s = <b>%d %s</b>." % (g(v), g(k), n, a))


def one_len(r):
    return conv(r, LEN)


def one_mass(r):
    return conv(r, MASS)


def one_cap(r):
    return conv(r, CAP)


def one_rate(r):
    kind = r.choice(["speed", "price", "gas"])
    if kind == "speed":
        kmh = r.choice([32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112])
        mph = kmh / 1.6
        return mcq("A speed limit in Mexico is %d km/h. Use 1 mile ≈ 1.6 kilometers. About how many miles per hour is that?" % kmh, "%s mi/h" % g(mph), ["%s mi/h" % g(kmh * 1.6), "%s mi/h" % g(kmh - 1.6), "%s mi/h" % g(mph * 10)],
                       "%d ÷ 1.6 = <b>%s mi/h</b>." % (kmh, g(mph)))
    if kind == "price":
        p = r.choice([1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 11])
        m = lambda v: "$%.2f" % v
        return mcq("Pecans cost %s per pound. Use 1 kilogram ≈ 2.2 pounds. About how much do they cost per kilogram?" % m(p), m(p * 2.2), [m(p / 2.2), m(p + 2.2), m(p)],
                   "1 kg ≈ 2.2 lb, so multiply: %s × 2.2 = <b>%s</b> per kilogram." % (m(p), m(p * 2.2)))
    l = 3.79 * r.randint(2, 9)
    n = int(round(l / 3.79))
    return mcq("A water jug holds %s liters. Use 1 gallon ≈ 3.79 liters. How many gallons does it hold?" % g(l), "%d gallons" % n, ["%s gallons" % g(round(l * 3.79, 2)), "%d gallons" % (n * 4), "%s gallons" % g(round(l - 3.79, 2))],
               "%s ÷ 3.79 = <b>%d gallons</b>." % (g(l), n))


def one_story(r):
    k = Kid(r).next()
    kind = r.choice(["race", "luggage", "board", "soda", "height"])
    if kind == "race":
        km = r.choice([5, 10, 15, 20, 25])
        return mcq("%s runs a %d-kilometer race in Austin. Use 1 mile ≈ 1.6 kilometers. About how many miles is the race?" % (k["n"], km), "%s miles" % g(km / 1.6), ["%s miles" % g(km * 1.6), "%s miles" % g(km - 1.6), "%d miles" % km],
                   "%d ÷ 1.6 = <b>%s miles</b>." % (km, g(km / 1.6)))
    if kind == "luggage":
        kg = r.choice([20, 23, 25, 30])
        return mcq("An airline allows a %d-kilogram suitcase. Use 1 kilogram ≈ 2.2 pounds. About how many pounds is that?" % kg, "%s pounds" % g(kg * 2.2), ["%s pounds" % g(kg / 2.2), "%s pounds" % g(kg + 2.2), "%d pounds" % (kg * 2)],
                   "%d × 2.2 = <b>%s pounds</b>." % (kg, g(kg * 2.2)))
    if kind == "board":
        inch = r.choice([12, 18, 24, 30, 36])
        return mcq("A shelf is %d inches long. Use 1 inch = 2.54 centimeters. How long is it in centimeters?" % inch, "%s cm" % g(inch * 2.54), ["%s cm" % g(inch / 2.54), "%s cm" % g(inch + 2.54), "%s cm" % g(inch * 25.4)],
                   "%d × 2.54 = <b>%s cm</b>." % (inch, g(inch * 2.54)))
    if kind == "soda":
        lt = r.choice([2, 3])
        n = r.choice([2, 3, 4, 5])
        return mcq("%s buys %d bottles of soda. Each holds %d liters. Use 1 liter ≈ 1.06 quarts. About how many quarts is that in all?" % (k["n"], n, lt), "%s quarts" % g(n * lt * 1.06), ["%s quarts" % g(n * lt / 1.06), "%d quarts" % (n * lt), "%s quarts" % g(lt * 1.06)],
                   "%d × %d = %d liters. %d × 1.06 = <b>%s quarts</b>." % (n, lt, n * lt, n * lt, g(n * lt * 1.06)))
    cm = r.choice([150, 155, 160, 165, 170])
    return mcq("%s is %d centimeters tall. Use 1 inch = 2.54 centimeters. About how tall is %s in inches? Round to the nearest inch." % (k["n"], cm, k["he"]), "%d inches" % round(cm / 2.54), ["%d inches" % round(cm * 2.54), "%d inches" % (cm - 3), "%d inches" % round(cm / 2.54 / 12)],
               "%d ÷ 2.54 ≈ %s, so about <b>%d inches</b>." % (cm, g(round(cm / 2.54, 2)), round(cm / 2.54)))


def build():
    sets, R = build_sets([
        ("Length: inches, feet, miles and metric units", [("collect", one_len, 20)]),
        ("Mass and weight: pounds, ounces, kilograms and grams", [("collect", one_mass, 20)]),
        ("Capacity: quarts, gallons, cups and liters", [("collect", one_cap, 20)]),
        ("Rates and unit prices in other units", [("collect", one_rate, 20)]),
        ("Word problems", [("collect", one_story, 20)]),
    ], 67009)
    finish(sets, R)
    body = lesson('<ul><li>A conversion factor is a ratio, such as 1 inch : 2.54 cm.</li><li>To change to the unit with more pieces (inches to centimeters), <b>multiply</b> by the factor.</li><li>To change back, <b>divide</b> by the factor.</li><li>You can also set up a proportion: 1/2.54 = x/30.</li></ul>',
        [example("12 in. to centimeters (1 in. = 2.54 cm)", ["12 × 2.54"], "30.48 cm"), example("10 km to miles (1 mi ≈ 1.6 km)", ["10 ÷ 1.6"], "6.25 mi")],
        [['Multiplying when you should divide', 'Kilometers to miles: there are fewer miles, so divide by 1.6.'], ['Using the wrong factor', 'Read which unit the factor starts from.'], ['Rounding too early', 'Round only the final answer.']])
    faq = [('What does TEKS 7.4E ask?', 'Convert between measurement systems, including the use of proportions and the use of unit rates.'), ('Do I need to memorize the factors?', 'No. Problems and the STAAR reference materials give the conversion factors.'), ('Why are some conversions approximate?', 'Many factors, like 1 mile ≈ 1.6 km, are rounded.'), ('How can a proportion help?', 'Write the factor as a ratio and match units: 1 kg/2.2 lb = x kg/11 lb.')]
    make('converting-between-measurement-systems', 9, 'Proportionality', '7.4E',
         '7.4E convert between measurement systems, including the use of proportions and the use of unit rates',
         'Converting Between Customary and Metric Units', 'Converting Between Measurement Systems',
         'Free Grade 7 worksheets for Texas TEKS 7.4E: convert length, mass, weight and capacity between customary and metric units with proportions and unit rates. 100 questions with answers.',
         'To the unit with more pieces, multiply; back again, divide.', '12 in. × 2.54 = 30.48 cm. 10 km ÷ 1.6 = 6.25 mi.',
         body, faq, sets, seo_title='Grade 7 Converting Between Customary and Metric Units Worksheets (TEKS 7.4E, STAAR)')


if __name__ == "__main__":
    build()
