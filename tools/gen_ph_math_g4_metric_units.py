# -*- coding: utf-8 -*-
"""
Philippines Grade 4 Math (MATATAG): Converting Units of Length, Mass and Capacity (Grade 4: Measurement and Geometry)
  python3 tools/gen_ph_math_g4_metric_units.py
Converting meters and centimeters, kilometers and meters, kilograms and grams, grams and milligrams, and liters and
milliliters (UK Year 4 makers with US spelling and own makers), comparing measurements and word problems.
Wrong answers come from real mistakes: multiplying when going to a bigger unit, using 100 for every unit, and
forgetting to change one of the units before comparing.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_uk_maths_y4_converting_units as ukc
adopt(ukc)
if hasattr(ukc, 'R'): ukc.R = random.Random(704130)
ph_common.GRADE = "grade-4"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


FACT = {("m", "cm"): 100, ("km", "m"): 1000, ("kg", "g"): 1000, ("g", "mg"): 1000, ("L", "mL"): 1000}
NAMES = {"m": "meters", "cm": "centimeters", "km": "kilometers", "kg": "kilograms", "g": "grams", "mg": "milligrams", "L": "liters", "mL": "milliliters"}


def one_conv(r):
    (big, small), f = r.choice(list(FACT.items()))
    if r.random() < 0.5:
        n = r.randint(2, 45)
        right = n * f
        q = "How many %s are in %d %s?" % (NAMES[small], n, big)
        w = [n * f // 10, n * f * 10, n + f]
        e = "1 %s = %s %s, so multiply by %s: %d × %s = <b>%s %s</b>." % (big, comma(f), small, comma(f), n, comma(f), comma(right), small)
        unit_ = small
    else:
        n = r.randint(2, 45)
        right = n
        q = "How many %s are in %s %s?" % (NAMES[big], comma(n * f), small)
        w = [n * 10, n * f * 10, n * f // 10]
        e = "%s %s = 1 %s, so divide by %s: %s ÷ %s = <b>%d %s</b>." % (comma(f), small, big, comma(f), comma(n * f), comma(f), n, big)
        unit_ = big
    return mcq(q, "%s %s" % (comma(right), unit_), ["%s %s" % (comma(x), unit_) for x in w if x != right], e)


def one_mixed(r):
    (big, small), f = r.choice(list(FACT.items()))
    a = r.randint(1, 9)
    b = r.randint(1, f - 1)
    if f == 1000 and r.random() < 0.6:
        b = r.choice([50, 125, 250, 300, 450, 500, 750, 800, 905])
    total = a * f + b
    if r.random() < 0.5:
        q = "%d %s %s %s = ☐ %s" % (a, big, comma(b), small, small)
        right, w = total, [a * 100 + b if f != 100 else a * 1000 + b, a + b, a * f]
        e = "%d %s = %s %s. %s + %s = <b>%s %s</b>." % (a, big, comma(a * f), small, comma(a * f), comma(b), comma(total), small)
        show = lambda v: "%s %s" % (comma(v), small)
    else:
        q = "%s %s = ☐ %s ☐ %s" % (comma(total), small, big, small)
        right = "%d %s %s %s" % (a, big, comma(b), small)
        w = ["%d %s %s %s" % (a * 10 if a * 10 < 100 else a + 1, big, comma(b // 10 if b >= 10 else b + 1), small), "%d %s %s %s" % (a + 1, big, comma(b), small), "%s %s %s %s" % (comma(total // 100), big, comma(total % 100), small) if f == 1000 else "%d %s %s %s" % (total // 10, big, comma(total % 10), small)]
        e = "%s %s = %d %s and %s %s left: <b>%s</b>." % (comma(a * f), small, a, big, comma(b), small, right)
        return mcq("Convert. " + q, right, w, e)
    return mcq("Convert. " + q, show(right), [show(x) for x in w if x != right], e)


CTX = [("A water jug holds %(a)d L. %(n)s pours out %(b)s mL. How many milliliters are left?", "L", "mL"),
       ("A sack has %(a)d kg of rice. %(n)s uses %(b)s g for dinner. How many grams of rice are left?", "kg", "g"),
       ("%(n)s walks %(a)d km %(b)s m to school. How many meters is that?", "km", "m"),
       ("A ribbon is %(a)d m long. %(n)s cuts off %(b)s cm. How many centimeters are left?", "m", "cm"),
       ("A vitamin tablet has %(b)s mg of vitamin C. How many milligrams are in %(a)d tablets?", None, "mg")]


def one_story(r):
    k = Kid(r).next()
    t, big, small = r.choice(CTX)
    a = r.randint(2, 9)
    if small == "mg":
        b = r.choice([100, 250, 500])
        right = a * b
        q = t % {"a": a, "b": comma(b), "n": k["n"]}
        return mcq(q, "%s mg" % comma(right), ["%s mg" % comma(x) for x in (a + b, right * 10, right // 10)], "%d × %s = <b>%s mg</b>." % (a, comma(b), comma(right)))
    f = FACT[(big, small)]
    b = r.randint(f // 20, f - 1) // 5 * 5
    if b == 0:
        raise AssertionError
    q = t % {"a": a, "b": comma(b), "n": k["n"]}
    if "walks" in t:
        right = a * f + b
        w = [a + b, a * 100 + b, a * f]
        e = "%d km = %s m. %s + %s = <b>%s m</b>." % (a, comma(a * f), comma(a * f), comma(b), comma(right))
    else:
        right = a * f - b
        w = [a * f + b, a - b if a > b else a * f, a * 100 - b if a * 100 > b else a * f // 10]
        e = "%d %s = %s %s. %s − %s = <b>%s %s</b>." % (a, big, comma(a * f), small, comma(a * f), comma(b), comma(right), small)
    return mcq(q, "%s %s" % (comma(right), small), ["%s %s" % (comma(x), small) for x in w if x != right and x > 0] + ["%s %s" % (comma(right + 10), small)], e)


def one_cmp(r):
    (big, small), f = r.choice(list(FACT.items()))
    a = r.randint(1, 9)
    b = a * f + r.choice([-1, 1]) * r.randint(1, f // 2)
    sym = ">" if a * f > b else "<"
    return mcq("Which sign makes this true? %d %s ☐ %s %s" % (a, big, comma(b), small), sym, [s for s in ["<", ">", "="] if s != sym] + ["+"],
               "%d %s = %s %s, and %s %s %s. <b>%s</b>." % (a, big, comma(a * f), small, comma(a * f), sym.replace(">", "&gt;").replace("<", "&lt;"), comma(b), sym.replace(">", "&gt;").replace("<", "&lt;")))


def build():
    sets, R = build_sets([
        ("Units of length", [("run", ukc.set_length, ("rnd",), 15), ("run", ukc.set_compare, ("rnd",), 5)]),
        ("Units of mass and capacity", [("run", ukc.set_mass_cap, ("rnd",), 20)]),
        ("Convert big and small units", [("collect", uniq(one_conv), 20)]),
        ("Mixed units and comparing", [("collect", uniq(one_mixed), 12), ("collect", uniq(one_cmp), 8)]),
        ("Measurement word problems", [("collect", uniq(one_story), 20)]),
    ], 70413)
    finish(sets, R)
    body = lesson('<ul><li>1 m = 100 cm, 1 km = 1,000 m, 1 kg = 1,000 g, 1 g = 1,000 mg, 1 L = 1,000 mL.</li><li>From a bigger unit to a smaller unit, <b>multiply</b> (you need more of the small units).</li><li>From a smaller unit to a bigger unit, <b>divide</b>.</li><li>Before you compare or add measurements, write them in the same unit.</li></ul>',
        [example("3 kg 250 g", ["3 kg = 3,000 g", "3,000 + 250"], "3,250 g"), example("4,500 mL", ["4,500 ÷ 1,000"], "4 L 500 mL")],
        [['Multiplying to get a bigger unit', 'cm to m: divide by 100.'], ['Using 100 for every unit', 'Only m and cm use 100; the others use 1,000.'], ['Comparing different units', 'Change to the same unit first.']])
    faq = [('What does MATATAG Math 4 ask about units?', 'Convert common units of measure from larger to smaller units, and vice versa: meter and centimeter, kilometer and meter, kilogram and gram, gram and milligram, and liter and milliliter.'), ('What does milli mean?', 'One thousandth: 1,000 mL make 1 L.'), ('Where are milligrams used?', 'For very light things, like the amount of medicine in a tablet.'), ('How many centimeters are in a kilometer?', '100,000.')]
    make('converting-units-of-length-mass-and-capacity', 13, 'Measurement and Geometry', 'Grade 4: Measurement and Geometry',
         'Convert common units of measure from larger to smaller units, and vice versa: meter and centimeter, kilometer and meter, kilogram and gram, gram and milligram, and liter and milliliter.',
         'Converting Units of Length, Mass and Capacity', 'Converting Metric Units',
         'Free Grade 4 metric conversion worksheets for the DepEd MATATAG curriculum: meters and centimeters, kilometers and meters, kilograms, grams and milligrams, liters and milliliters. 100 questions with answers.',
         'Bigger to smaller unit: multiply. Smaller to bigger: divide.', 'm–cm: 100. km–m, kg–g, g–mg, L–mL: 1,000.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
