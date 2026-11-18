# -*- coding: utf-8 -*-
"""
Texas Grade 4 Math: Measurement Word Problems: Length, Time, Liquid Volume, Mass and Money (TEKS 4.8C)
  python3 tools/gen_ustx_math_g4_measurement_problems.py
Word problems with measurements and money (the US Grade 4 maker with Texas names), and new problems on length,
elapsed time, liquid volume, mass and money that use addition, subtraction, multiplication or division.
Wrong answers come from real mistakes: mixing units without converting, treating an hour as 100 minutes, and
using the wrong operation.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g4_conversions as usc
adopt(usc)
tx_common.GRADE = "grade-4"

def one_length(r):
    k = Kid(r).next()
    kind = r.choice(["ribbon", "fence", "cut"])
    if kind == "ribbon":
        a, n = r.randint(2, 9), r.randint(3, 8)
        return mcq("%s needs %d pieces of string. Each piece is %d inches long. How many inches of string does %s need?" % (k["n"], n, a * 4, k["he"]), "%d inches" % (n * a * 4),
                   ["%d inches" % (n + a * 4), "%d inches" % (n * a * 4 - a * 4), "%d feet" % (n * a * 4)], "%d × %d = <b>%d inches</b>." % (n, a * 4, n * a * 4))
    if kind == "fence":
        f = r.randint(2, 9)
        i = r.randint(1, 11)
        return mcq("A board is %d feet %d inches long. How many inches long is it?" % (f, i), "%d inches" % (f * 12 + i), ["%d inches" % (f + i), "%d inches" % (f * 10 + i), "%d inches" % (f * 12)],
                   "%d feet = %d × 12 = %d inches. %d + %d = <b>%d inches</b>." % (f, f, f * 12, f * 12, i, f * 12 + i))
    m = r.randint(3, 9)
    c = r.randint(1, 3) * 25
    return mcq("A rope is %d meters long. %s cuts off %d centimeters. How many centimeters are left?" % (m, k["n"], c), "%d centimeters" % (m * 100 - c), ["%d centimeters" % (m - c if m > c else m * 10 - c), "%d centimeters" % (m * 100 + c), "%d centimeters" % (m * 10 - c)],
               "%d m = %d cm. %d − %d = <b>%d centimeters</b>." % (m, m * 100, m * 100, c, m * 100 - c))


def one_time(r):
    k = Kid(r).next()
    kind = r.choice(["elapsed", "total", "week"])
    if kind == "elapsed":
        h, mnt = r.randint(1, 4), r.choice([5, 10, 15, 20, 25, 35, 40, 45, 50])
        d = r.choice([35, 45, 50, 55, 70, 85, 95])
        t = h * 60 + mnt + d
        end = "%d:%02d" % (t // 60, t % 60)
        return mcq("Soccer practice starts at %d:%02d p.m. and lasts %d minutes. When does it end?" % (h, mnt, d), end + " p.m.",
                   ["%d:%02d p.m." % (h, (mnt + d) % 100) if (mnt + d) % 100 < 60 and (mnt + d) % 100 != t % 60 else "%d:%02d p.m." % (h + 1, (t % 60 + 10) % 60), "%d:%02d p.m." % (t // 60 + 1, t % 60), "%d:%02d p.m." % (t // 60, (t % 60 + 5) % 60)],
                   "%d:%02d + %d minutes. Count to the next hour, then add the rest: <b>%s p.m.</b>" % (h, mnt, d, end))
    if kind == "total":
        a, b = r.randint(31, 55), r.randint(31, 55)
        s = a + b
        if s % 60 == 0:
            return None
        return mcq("%s practices piano for %d minutes and reads for %d minutes. How long is that in hours and minutes?" % (k["n"], a, b), "%d hour %d minutes" % (s // 60, s % 60) if s >= 60 else "%d minutes" % s,
                   ["%d minutes" % (s + 40), "%d hours %d minutes" % (s // 60 + 1, s % 60), "%d hour %d minutes" % (s // 100 + 1, s % 100) if s % 100 != s % 60 else "%d hour %d minutes" % (s // 60, s % 60 + 10)],
                   "%d + %d = %d minutes = <b>%s</b>." % (a, b, s, "%d hour %d minutes" % (s // 60, s % 60) if s >= 60 else "%d minutes" % s))
    m = r.choice([15, 20, 25, 30, 35, 40, 45])
    d = r.choice([5, 6, 7])
    return mcq("%s walks the dog for %d minutes each day. How many minutes is that in %d days?" % (k["n"], m, d), "%d minutes" % (m * d), ["%d minutes" % (m + d), "%d minutes" % (m * d - m), "%d minutes" % (m * 7 + 7)],
               "%d × %d = <b>%d minutes</b>." % (d, m, m * d))


def one_volume_mass(r):
    k = Kid(r).next()
    kind = r.choice(["liters", "cups", "grams", "kg_share"])
    if kind == "liters":
        a = r.randint(2, 6)
        ml = r.choice([250, 500, 200])
        n = a * 1000 // ml
        return mcq("A cooler holds %d liters of water. How many %d-milliliter cups can be filled?" % (a, ml), n, [a * ml, n + 1, a * 1000 - ml], "%d L = %s mL. %s ÷ %d = <b>%d</b> cups." % (a, comma(a * 1000), comma(a * 1000), ml, n))
    if kind == "cups":
        q = r.randint(2, 6)
        return mcq("A recipe makes %d quarts of soup. How many 1-cup servings is that? (1 quart = 4 cups)" % q, "%d servings" % (q * 4), ["%d servings" % (q * 2), "%d servings" % (q + 4), "%d servings" % (q * 8)], "%d × 4 = <b>%d servings</b>." % (q, q * 4))
    if kind == "grams":
        a, b = r.randint(150, 650), r.randint(150, 650)
        return mcq("A bag of apples has a mass of %d grams. A bag of pears has a mass of %d grams. What is their total mass?" % (a, b), "%s grams" % comma(a + b), ["%s grams" % comma(abs(a - b)), "%s grams" % comma(a + b + 100), "%d kilograms" % (a + b)], "%d + %d = <b>%s grams</b>." % (a, b, comma(a + b)))
    t, n = r.choice([(12, 4), (15, 5), (18, 6), (24, 8), (20, 4), (36, 9)])
    return mcq("%d kilograms of rice are shared equally among %d families. How many kilograms does each family get?" % (t, n), "%d kilograms" % (t // n), ["%d kilograms" % (t - n), "%d kilograms" % (t * n), "%d grams" % (t // n)], "%d ÷ %d = <b>%d kilograms</b>." % (t, n, t // n))


def one_money(r):
    k = Kid(r).next()
    kind = r.choice(["change", "each", "total"])
    if kind == "change":
        p = r.randint(105, 1895)
        pay = 2000
        return mcq("%s buys a book for $%d.%02d and pays with a $20 bill. How much change does %s get?" % (k["n"], p // 100, p % 100, k["he"]), "$%d.%02d" % ((pay - p) // 100, (pay - p) % 100),
                   ["$%d.%02d" % ((pay - p) // 100 + 1, (pay - p) % 100), "$%d.%02d" % ((pay + p) // 100, (pay + p) % 100), "$%d.%02d" % ((pay - p) // 100, ((pay - p) % 100 + 10) % 100)],
                   "$20.00 − $%d.%02d = <b>$%d.%02d</b>." % (p // 100, p % 100, (pay - p) // 100, (pay - p) % 100))
    if kind == "each":
        n, c = r.randint(3, 8), r.randint(4, 12)
        return mcq("%d tickets to a science museum cost $%d in all. Each ticket costs the same. How much is one ticket?" % (n, n * c), "$%d" % c, ["$%d" % (n * c - n), "$%d" % (c + 1), "$%d" % (n * c * n)], "$%d ÷ %d = <b>$%d</b>." % (n * c, n, c))
    n, c = r.randint(3, 9), r.randint(125, 875)
    return mcq("A notebook costs $%d.%02d. How much do %d notebooks cost?" % (c // 100, c % 100, n), "$%d.%02d" % (n * c // 100, n * c % 100), ["$%d.%02d" % ((n + c) // 100, (n + c) % 100), "$%d.%02d" % ((n * c + 100) // 100, (n * c + 100) % 100), "$%d.%02d" % (n * c // 100, (n * c % 100 + 5) % 100)],
               "%d × $%d.%02d = <b>$%d.%02d</b>." % (n, c // 100, c % 100, n * c // 100, n * c % 100))


def build():
    sets, R = build_sets([
        ("Length problems", [("collect", one_length, 20)]),
        ("Time problems", [("collect", one_time, 20)]),
        ("Liquid volume and mass problems", [("collect", one_volume_mass, 20)]),
        ("Money problems", [("collect", one_money, 20)]),
        ("Mixed measurement word problems", [("run", usc.set_story, ("rnd",), 20)]),
    ], 64022)
    finish(sets, R)
    body = lesson('<ul><li>Read what is measured: length, time, liquid volume, mass or money. Decide whether to add, subtract, multiply or divide.</li><li>Make the units the same before you compute: 2 feet 5 inches = 29 inches; 3 liters = 3,000 milliliters.</li><li>For time, 1 hour = 60 minutes. Count to the next hour, then add the rest.</li></ul>',
        [example("Practice starts at 3:40 p.m. and lasts 55 minutes. When does it end?", ["3:40 + 20 minutes = 4:00", "4:00 + 35 minutes = 4:35"], "4:35 p.m."), example("How many 250 mL cups can be filled from 2 liters?", ["2 L = 2,000 mL", "2,000 ÷ 250 = 8"], "8 cups")],
        [['Computing with different units', 'Convert first so both numbers use the same unit.'], ['Treating an hour as 100 minutes', '1 hour = 60 minutes.'], ['Choosing the wrong operation', 'Ask: are amounts joined, compared, repeated or shared?']])
    faq = [('What does TEKS 4.8C ask?', 'Solve problems that deal with measurements of length, intervals of time, liquid volumes, mass and money using addition, subtraction, multiplication or division as appropriate.'), ('Do I need to convert units?', 'Often, yes. Change to the same unit before you add or subtract.'), ('How do I solve elapsed time problems?', 'Count forward to the next hour, then add the rest of the minutes.'), ('How do I work with money?', 'Line up the decimal points to add or subtract, and remember that $1 = 100 cents.')]
    make('measurement-word-problems', 22, 'Geometry and Measurement', '4.8C',
         '4.8C solve problems that deal with measurements of length, intervals of time, liquid volumes, mass, and money using addition, subtraction, multiplication, or division as appropriate',
         'Measurement Word Problems: Length, Time, Liquid Volume, Mass and Money', 'Measurement Word Problems',
         'Free Grade 4 measurement word problem worksheets for Texas TEKS 4.8C: length, elapsed time, liquid volume, mass and money problems with all four operations. 100 STAAR-style questions with answers.',
         'Use the same unit for every number, then choose the operation.', '1 hour = 60 minutes, 1 foot = 12 inches, 1 liter = 1,000 milliliters.',
         body, faq, sets, seo_title='Grade 4 Measurement Word Problems Worksheets (TEKS 4.8C, STAAR)')


if __name__ == "__main__":
    build()
