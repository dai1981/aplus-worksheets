# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): Capacity and Volume: Millilitres and Litres (Grade 5: 4.3 Capacity/Volume)
  python3 tools/gen_za_maths_g5_capacity.py
Choosing units, reading measuring jugs, converting between mℓ and ℓ, and capacity problems (Australia Year 5, UK Year
5 and Ontario Grade 5 makers and the conversion and story makers from the Grade 4 generator).
Wrong answers come from real mistakes: using 100 instead of 1 000 for ℓ and mℓ, reading the wrong interval on a jug,
and subtracting before changing to the same unit.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y5_metric_units as aum
adopt(aum)
if isinstance(getattr(aum, 'R', None), random.Random): aum.R = random.Random(805240)
import gen_uk_maths_y5_converting_units as ukc
adopt(ukc)
if isinstance(getattr(ukc, 'R', None), random.Random): ukc.R = random.Random(805241)
import gen_caon_math_g5_metric as cam
adopt(cam)
if isinstance(getattr(cam, 'R', None), random.Random): cam.R = random.Random(805242)
import gen_au_maths_y4_scales as aus
adopt(aus)
if isinstance(getattr(aus, 'R', None), random.Random): aus.R = random.Random(805243)
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
        ("Choose the unit", [("collect", unit_maker("cap"), 20)]),
        ("Read the jug", [("run", aus.set_capacity, ("rnd",), 20, nodec)]),
        ("Convert millilitres and litres", [("collect", conv_maker([("ℓ", "mℓ", 1000)]), 20)]),
        ("Compare and order capacities", [("collect", order_maker("cap"), 20)]),
        ("Capacity problems", [("collect", story_maker(("l", "ladd", "lglass")), 20)]),
    ], 80524)
    finish(sets, R)
    body = lesson('<ul><li>Capacity is how much a container can hold. Volume is how much space something takes up.</li><li>We measure liquids in millilitres (mℓ) and litres (ℓ). 1 ℓ = 1 000 mℓ.</li><li>Use mℓ for a teaspoon or a cup, and ℓ for a bucket or a bath.</li><li>On a measuring jug, find what each mark is worth before you read it.</li></ul>',
        [example("A 2 ℓ bottle fills 250 mℓ glasses", ["2 ℓ = 2 000 mℓ", "2 000 ÷ 250"], "8 glasses")],
        [['100 mℓ in a litre', '1 ℓ = 1 000 mℓ.'], ['The wrong interval', 'Work out each mark first.'], ['Different units', 'Change to mℓ first.']])
    faq = [('What does CAPS Grade 5 say about capacity and volume?', 'Estimate, measure, record, compare and order capacity and volume using measuring spoons, cups and jugs, in mℓ and ℓ, and convert between them.'), ('How much is a teaspoon?', 'About 5 mℓ.'), ('What is ¾ ℓ in mℓ?', '750 mℓ.'), ('Capacity or volume?', 'Capacity is what a container holds; volume is the space taken up.')]
    make('capacity-and-volume', 24, 'Measurement', 'Grade 5: 4.3 Capacity/Volume',
         'Estimate, measure, record, compare and order capacity and volume using measuring instruments such as measuring spoons, measuring cups and measuring jugs; use millilitres (mℓ) and litres (ℓ); calculate and solve problems involving capacity and volume; convert between litres and millilitres.',
         'Capacity and Volume: Millilitres and Litres', 'Capacity and Volume',
         'Free CAPS Grade 5 capacity and volume worksheets: millilitres and litres, reading measuring jugs, converting units and problems. 100 questions with memos.',
         '1 ℓ = 1 000 mℓ.', 'Read what each mark on the jug is worth.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
