# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): Length: Measuring and Converting mm, cm, m and km (Grade 5: 4.1 Length)
  python3 tools/gen_za_maths_g5_length.py
Choosing units, reading scales, converting between mm, cm, m and km, and length problems (Australia Year 5, UK Year 5
and Ontario Grade 5 makers, the conversion maker from the Grade 4 generator, and own story maker).
Wrong answers come from real mistakes: using 100 instead of 1 000 for km and m, multiplying when changing to a bigger
unit, and subtracting before changing to the same unit.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y5_metric_units as aum
adopt(aum)
if isinstance(getattr(aum, 'R', None), random.Random): aum.R = random.Random(805220)
import gen_uk_maths_y5_converting_units as ukc
adopt(ukc)
if isinstance(getattr(ukc, 'R', None), random.Random): ukc.R = random.Random(805221)
import gen_caon_math_g5_metric as cam
adopt(cam)
if isinstance(getattr(cam, 'R', None), random.Random): cam.R = random.Random(805222)
import gen_au_maths_y4_scales as aus
adopt(aus)
if isinstance(getattr(aus, 'R', None), random.Random): aus.R = random.Random(805223)
from gen_za_maths_g4_length import conv_maker, story_maker, mass_only, cap_only, len_only
za_common.GRADE = "grade-5"

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


OBJ = {"len": [("an ant", 4, "mm"), ("a grain of rice", 6, "mm"), ("a R5 coin", 26, "mm"), ("a pencil", 17, "cm"), ("a school desk", 70, "cm"), ("a maths book", 30, "cm"), ("a classroom", 9, "m"),
               ("a soccer field", 100, "m"), ("a school bus", 12, "m"), ("the road from Cape Town to Stellenbosch", 50, "km"), ("the N1 from Johannesburg to Pretoria", 60, "km"), ("a door", 2, "m"), ("a teaspoon", 13, "cm"), ("a fingernail", 10, "mm")],
       "mass": [("a pencil", 5, "g"), ("an apple", 150, "g"), ("a loaf of bread", 700, "g"), ("a bag of mealie meal", 10, "kg"), ("a Grade 5 learner", 35, "kg"), ("a cow", 500, "kg"), ("a R2 coin", 6, "g"),
                ("a bag of potatoes", 7, "kg"), ("a slice of cheese", 20, "g"), ("a bicycle", 12, "kg"), ("a packet of sweets", 125, "g"), ("a watermelon", 4, "kg")],
       "cap": [("a teaspoon", 5, "mℓ"), ("a cup of tea", 250, "mℓ"), ("a can of cooldrink", 330, "mℓ"), ("a bucket", 10, "ℓ"), ("a bath", 150, "ℓ"), ("a kettle", 2, "ℓ"), ("a bottle of medicine", 100, "mℓ"),
               ("a swimming pool", 50000, "ℓ"), ("a carton of milk", 1, "ℓ"), ("a glass of water", 200, "mℓ"), ("a watering can", 8, "ℓ"), ("a tablespoon", 15, "mℓ")]}
UNITS = {"len": ["mm", "cm", "m", "km"], "mass": ["g", "kg"], "cap": ["mℓ", "ℓ"]}


def unit_maker(kind):
    seen = set()

    def f(r):
        o, v, u = r.choice(OBJ[kind])
        how = r.choice(["which", "best"])
        if how == "which":
            q = "Which is the best estimate for %s %s?" % ({"len": "the length of", "mass": "the mass of", "cap": "how much is in"}[kind] if not o.startswith("the ") else "the distance of", o)
            if kind == "len" and o.startswith("the "):
                q = "Which is the best estimate for the length of %s?" % o
            right = "%s %s" % (comma(v), u)
            wr = ["%s %s" % (comma(v), x) for x in UNITS[kind] if x != u]
            if len(wr) < 3:
                wr += ["%s %s" % (comma(v * 100), u), "%s %s" % (comma(max(1, v // 10) if v >= 10 else v * 10), u)]
            e = "%s is about <b>%s</b>." % (o[0].upper() + o[1:], right)
        else:
            q = "Which unit would you use to measure %s %s?" % ({"len": "the length of", "mass": "the mass of", "cap": "how much"}[kind], o) + (" holds" if kind == "cap" else "")
            right = u
            wr = [x for x in UNITS[kind] if x != u] + {"len": [], "mass": ["mℓ", "cm"], "cap": ["g", "kg"]}[kind]
            e = "%s is measured in <b>%s</b>." % (o[0].upper() + o[1:], u)
        out = mcq(q, right, wr[:3], e)
        if out["q"] in seen:
            raise AssertionError
        seen.add(out["q"])
        return out
    return f


ORD = {"len": [("m", "cm", 100), ("km", "m", 1000), ("cm", "mm", 10)], "mass": [("kg", "g", 1000)], "cap": [("ℓ", "mℓ", 1000)]}


def order_maker(kind):
    seen = set()

    def f(r):
        big, small, k = r.choice(ORD[kind])
        base = r.randint(1, 5) * k + r.choice([1, 2, 3, 4, 5, 6, 7, 8, 9]) * (k // 10 if k > 10 else 1) * (1 if k > 10 else 0)
        vals = sorted(set([base, base + r.choice([5, 10, 20, 50]) * (k // 100 or 1), base - r.choice([5, 10, 25]) * (k // 100 or 1), base + k // 2 if k > 10 else base + 3]))
        if len(vals) < 4 or min(vals) <= 0:
            raise AssertionError
        def show(x, mode):
            if mode == 0 or x % k == 0 and mode == 1:
                return "%s %s" % (comma(x), small) if mode == 0 else "%d %s" % (x // k, big)
            return "%d %s %s %s" % (x // k, big, comma(x % k), small) if x // k else "%s %s" % (comma(x), small)
        modes = [r.choice([0, 1]) for _ in vals]
        shown = [show(x, m) for x, m in zip(vals, modes)]
        idx = list(range(4))
        r.shuffle(idx)
        mixed = [shown[i] for i in idx]
        if len(set(modes)) < 2:
            raise AssertionError
        right = ", ".join(shown)
        wr = [", ".join(mixed), ", ".join(shown[::-1]), ", ".join(sorted(shown))]
        wr = [w for w in wr if w != right]
        if len(set(wr)) < len(wr) or len(wr) < 2:
            raise AssertionError
        q = "Order from the smallest to the biggest: <b>%s</b>" % "; ".join(mixed)
        out = mcq(q, right.replace(", ", "; "), [w.replace(", ", "; ") for w in wr] + ["; ".join(shown[1:] + shown[:1])], "Change them all to %s: %s. Answer: <b>%s</b>." % (small, ", ".join("%s %s" % (comma(v), small) for v in vals), "; ".join(shown)))
        if out["q"] in seen:
            raise AssertionError
        seen.add(out["q"])
        return out
    return f

LS = [("A rope is %s m long. %s cuts off %s cm. How much rope is left?", "m"),
      ("%s walks %s km to school and then %s m to the shop. How far is that in metres?", "kmadd"),
      ("A roll of ribbon is %s m long. %s uses %s cm for a gift. How much is left?", "m"),
      ("%s runs %s laps of a %s m track. How far is that in kilometres and metres?", "laps")]


def one_lstory(r):
    k = Kid(r).next()
    t, kind = r.choice(LS)
    a = r.randint(2, 9)
    if kind == "m":
        b = r.choice([15, 35, 45, 65, 80, 125, 150, 175])
        if b >= a * 100:
            raise AssertionError
        right = a * 100 - b
        q = t % (a, k["n"], b)
        return mcq(q, "%s cm" % comma(right), ["%s cm" % comma(x) for x in (a * 100 + b, a * 10 - b if a * 10 > b else right + 10, a * 1000 - b)],
                   "%d m = %s cm. %s − %d = <b>%s cm</b>." % (a, comma(a * 100), comma(a * 100), b, comma(right)))
    if kind == "kmadd":
        b = r.choice([150, 250, 300, 450, 600, 750, 850])
        right = a * 1000 + b
        q = t % (k["n"], a, b)
        return mcq(q, "%s m" % comma(right), ["%s m" % comma(x) for x in (a * 100 + b, a + b, a * 1000 - b)],
                   "%d km = %s m. %s + %d = <b>%s m</b>." % (a, comma(a * 1000), comma(a * 1000), b, comma(right)))
    lap = r.choice([200, 400])
    n = r.randint(3, 9)
    tot = n * lap
    if tot < 1000:
        raise AssertionError
    right = "%d km %d m" % (tot // 1000, tot % 1000) if tot % 1000 else "%d km" % (tot // 1000)
    q = t % (k["n"], n, lap)
    return mcq(q, right, ["%s m" % comma(tot // 10), "%d km %d m" % (tot // 100, tot % 100) if tot % 100 else "%d km" % (tot // 100), "%d km %d m" % (tot // 1000 + 1, tot % 1000) if tot % 1000 else "%d km" % (tot // 1000 + 1)],
               "%d × %d m = %s m = <b>%s</b>." % (n, lap, comma(tot), right))


def build():
    sets, R = build_sets([
        ("Choose the unit", [("run", aum.set_units, ("rnd",), 4, lambda it: len_only(it) and nodec(it)), ("collect", unit_maker("len"), 16)]),
        ("Read the scale", [("run", aum.set_read, ("rnd",), 5, lambda it: len_only(it) and nodec(it)), ("run", aus.set_length, ("rnd",), 15, nodec)]),
        ("Convert units of length", [("run", cam.set_length, ("rnd",), 5, nodec), ("collect", conv_maker([("m", "cm", 100), ("km", "m", 1000), ("cm", "mm", 10)]), 15)]),
        ("Compare and order lengths", [("collect", order_maker("len"), 20)]),
        ("Length problems", [("collect", uniq(one_lstory), 20)]),
    ], 80522)
    finish(sets, R)
    body = lesson('<ul><li>10 mm = 1 cm, 100 cm = 1 m, 1 000 m = 1 km.</li><li>Choose a sensible unit: mm for an ant, cm for a book, m for a classroom, km for a road.</li><li>To change to a smaller unit, multiply; to change to a bigger unit, divide.</li><li>Change to the same unit before you add or subtract.</li></ul>',
        [example("3 km − 850 m", ["3 km = 3 000 m", "3 000 − 850"], "2 150 m")],
        [['100 m in a km', '1 km = 1 000 m.'], ['Multiplying to a bigger unit', 'mm to cm: divide by 10.'], ['Different units', 'Change to the same unit first.']])
    faq = [('What does CAPS Grade 5 say about length?', 'Estimate, measure, record, compare and order lengths in mm, cm, m and km, calculate and solve problems, and convert between units.'), ('How many mm are in 1 m?', '1 000.'), ('Which unit for the distance to Durban?', 'Kilometres.'), ('Why change to the same unit?', 'You can only add or subtract like units.')]
    make('length', 22, 'Measurement', 'Grade 5: 4.1 Length',
         'Estimate, measure, record, compare and order 2-D shapes and 3-D objects using measuring instruments such as rulers, metre sticks, tape measures and trundle wheels; use millimetres (mm), centimetres (cm), metres (m) and kilometres (km); calculate and solve problems involving length; convert between mm, cm, m and km.',
         'Length: Measuring and Converting mm, cm, m and km', 'Length',
         'Free CAPS Grade 5 length worksheets: choosing units, reading scales, converting mm, cm, m and km and length problems. 100 questions with memos.',
         '10 mm = 1 cm, 100 cm = 1 m, 1 000 m = 1 km.', 'Same unit before adding or subtracting.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
