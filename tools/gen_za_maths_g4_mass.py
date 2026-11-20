# -*- coding: utf-8 -*-
"""
South Africa Grade 4 Maths (CAPS): Mass: Grams and Kilograms (Grade 4: 4.2 Mass)
  python3 tools/gen_za_maths_g4_mass.py
Reading kitchen and bathroom scales, choosing grams or kilograms, converting between g and kg, comparing masses and
problems (Australia Year 4, UK Year 3 and Year 4, and Ontario Grade 4 makers).
Wrong answers come from real mistakes: reading the wrong marks on the scale, using 100 g in a kilogram, and
comparing numbers with different units.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y4_scales as aus
adopt(aus)
if hasattr(aus, 'R'): aus.R = random.Random(804220)
import gen_uk_maths_y3_measuring as uk3
adopt(uk3)
if hasattr(uk3, 'R'): uk3.R = random.Random(804221)
import gen_uk_maths_y4_converting_units as ukc
adopt(ukc)
if hasattr(ukc, 'R'): ukc.R = random.Random(804222)
import gen_caon_math_g4_metric as cam
adopt(cam)
if hasattr(cam, 'R'): cam.R = random.Random(804223)
import gen_au_maths_y3_measuring as au3
adopt(au3)
if hasattr(au3, 'R'): au3.R = random.Random(804224)
za_common.GRADE = "grade-4"


import re as _re


def nodollar(it):
    return True


def mass_only(it):
    t = _re.sub(r"<[^>]+>", " ", it["q"] + " " + " ".join(it["c"]))
    return bool(_re.search(r"\b(kg|g|kilograms?|grams?|mass|heavy|heavier|lighter|weigh)", t)) and not _re.search(r"\b(ml|mL|l|L|ℓ|litres?|liters?)\b", t)


def cap_only(it):
    t = _re.sub(r"<[^>]+>", " ", it["q"] + " " + " ".join(it["c"]))
    return bool(_re.search(r"(ml|mL|ℓ|\bl\b|\bL\b|litre|liter|capacity|holds)", t)) and not _re.search(r"\b(kg|kilograms?|grams?)\b", t)


def len_only(it):
    t = _re.sub(r"<[^>]+>", " ", it["q"] + " " + " ".join(it["c"]))
    return bool(_re.search(r"\b(mm|cm|m|km|metres?|meters?|centimetres?|centimeters?|long|tall|length|height|distance)\b", t)) and not _re.search(r"\b(kg|g|ml|mL|l|L)\b", t)




def conv_maker(pairs):
    seen = set()

    def f(r):
        big, small, k = r.choice(pairs)
        kind = r.choice(["b2s", "s2b", "mix", "frac"])
        if kind == "b2s":
            n = r.randint(2, 9)
            m = r.choice([0, r.randint(1, k - 1)]) if k > 10 else r.randint(0, k - 1)
            q = "Convert <b>%d %s%s</b> to %s." % (n, big, (" %s %s" % (comma(m), small)) if m else "", small)
            right = n * k + m
            wr = [n * 100 + m if k != 100 else n * 1000 + m, n + m, n * k * 10 + m]
            e = "1 %s = %s %s, so %d %s = %s %s%s. <b>%s %s</b>." % (big, comma(k), small, n, big, comma(n * k), small, (" and %s + %s = %s" % (comma(n * k), comma(m), comma(right))) if m else "", comma(right), small)
            out = mcq(q, "%s %s" % (comma(right), small), ["%s %s" % (comma(x), small) for x in wr if x != right], e)
        elif kind == "s2b":
            n = r.randint(2, 9)
            q = "How many %s are in <b>%s %s</b>?" % ({"kg": "kilograms", "ℓ": "litres", "m": "metres", "cm": "centimetres", "km": "kilometres"}[big], comma(n * k), small)
            out = mcq(q, "%d %s" % (n, big), ["%s %s" % (comma(x), big) for x in (n * 10, n * k * 10, n + 1)], "%s %s = 1 %s, so %s ÷ %s = <b>%d %s</b>." % (comma(k), small, big, comma(n * k), comma(k), n, big))
        elif kind == "mix":
            n = r.randint(1, 9)
            m = r.randint(1, k - 1)
            if k > 10:
                m = m // 5 * 5 or 5
            t = n * k + m
            q = "<b>%s %s</b> = ☐ %s ☐ %s" % (comma(t), small, big, small)
            right = "%d %s %s %s" % (n, big, comma(m), small)
            wr = ["%d %s %s %s" % (n + 1, big, comma(m), small), "%s %s %s %s" % (comma(t // 10), big, comma(t % 10), small), "%d %s %s %s" % (n, big, comma(m * 10 if m * 10 < k else m + 1), small)]
            out = mcq(q, right, wr, "%s %s = %d %s, with %s %s left: <b>%s</b>." % (comma(n * k), small, n, big, comma(m), small, right))
        else:
            if k == 10:
                raise AssertionError
            a, b = r.choice([(1, 2), (1, 4), (3, 4), (1, 5), (1, 10)])
            v = k * a // b
            q = "<b>%s %s</b> = ☐ %s" % (fr(a, b), big, small)
            out = mcq(q, "%s %s" % (comma(v), small), ["%s %s" % (comma(x), small) for x in (k // b, v * 10 if v * 10 != k else v + 50, b * 100 // a if b * 100 // a != v else v // 2)] if a > 1 else ["%s %s" % (comma(x), small) for x in (k * b, v * 10, a * 100 + b)],
                      "%s of %s %s = %s ÷ %d%s = <b>%s %s</b>." % (fr(a, b), comma(k), small, comma(k), b, (" × %d" % a) if a > 1 else "", comma(v), small))
        if out["q"] in seen:
            raise AssertionError
        seen.add(out["q"])
        return out
    return f


MS = [("A bag of mealie meal has a mass of %s kg. %s uses %s g for supper. How much is left?", "kg"),
      ("%s buys %s kg of potatoes and %s g of onions. What is the total mass in grams?", "kgadd"),
      ("A box of apples has a mass of %s kg. %s takes out %s g of apples. How much is left?", "kg"),
      ("A bucket holds %s ℓ of water. %s pours out %s mℓ to water the plants. How much is left?", "l"),
      ("%s mixes %s ℓ of juice with %s mℓ of water. How much cooldrink is there in millilitres?", "ladd"),
      ("A jug holds %s ℓ. %s fills %s glasses of 250 mℓ each from the full jug. How much is left in the jug?", "lglass")]


def story_maker(kinds):
    seen = set()

    def f(r):
        k = Kid(r).next()
        t, kind = r.choice([m for m in MS if m[1] in kinds])
        a = r.randint(2, 9)
        b = r.choice([150, 250, 300, 450, 500, 600, 750, 850])
        if kind in ("kg", "l"):
            u = "g" if kind == "kg" else "mℓ"
            q = t % (a, k["n"], comma(b))
            right = a * 1000 - b
            wr = [a * 1000 + b, a * 100 - b if a * 100 > b else a * 1000 - b + 100, b - a if b > a else right + 10]
            e = "%d %s = %s %s. %s − %s = <b>%s %s</b>." % (a, "kg" if u == "g" else "ℓ", comma(a * 1000), u, comma(a * 1000), comma(b), comma(right), u)
        elif kind in ("kgadd", "ladd"):
            u = "g" if kind == "kgadd" else "mℓ"
            q = t % (k["n"], a, comma(b))
            right = a * 1000 + b
            wr = [a + b, a * 100 + b, a * 1000 - b]
            e = "%d %s = %s %s. %s + %s = <b>%s %s</b>." % (a, "kg" if u == "g" else "ℓ", comma(a * 1000), u, comma(a * 1000), comma(b), comma(right), u)
        else:
            u = "mℓ"
            g = r.randint(2, a * 4 - 1)
            q = t % (a, k["n"], g)
            right = a * 1000 - g * 250
            wr = [g * 250, a * 1000 - g * 25, right + 250]
            e = "%d × 250 mℓ = %s mℓ. %s − %s = <b>%s mℓ</b>." % (g, comma(g * 250), comma(a * 1000), comma(g * 250), comma(right))
        out = mcq(q, "%s %s" % (comma(right), u), ["%s %s" % (comma(x), u) for x in wr if x > 0 and x != right] + ["%s %s" % (comma(right + 1000), u)], e)
        if out["q"] in seen:
            raise AssertionError
        seen.add(out["q"])
        return out
    return f


def pos_temp(it):
    t = _re.sub(r"<[^>]+>", " ", it["q"] + " " + " ".join(it["c"]))
    return "−" not in t and "-" not in _re.sub(r"[A-Za-z]-[A-Za-z]", "", t)



def build():
    sets, R = build_sets([
        ("Read the scale", [("run", aus.set_mass, ("rnd",), 15), ("run", au3.set_mass, ("rnd",), 5, lambda it: "1 kilogram?" not in it["q"])]),
        ("Grams or kilograms?", [("run", cam.set_grams, ("rnd",), 15, mass_only), ("collect", conv_maker([("kg", "g", 1000)]), 5)]),
        ("Convert g and kg", [("run", ukc.set_mass_cap, ("rnd",), 8, mass_only), ("collect", conv_maker([("kg", "g", 1000)]), 12)]),
        ("Compare masses", [("run", uk3.set_mass, ("rnd",), 15), ("collect", story_maker(("kg", "kgadd")), 5)]),
        ("Mass problems", [("run", aus.set_story, ("rnd",), 6, mass_only), ("collect", story_maker(("kg", "kgadd")), 14)]),
    ], 80422)
    finish(sets, R)
    body = lesson('<ul><li>We measure mass in grams (g) and kilograms (kg). 1 000 g = 1 kg.</li><li>Light things like a slice of bread are measured in grams; heavy things like a bag of mealie meal in kilograms.</li><li>Read a scale carefully: find what each small mark stands for.</li><li>Before you compare, change both masses to the same unit.</li></ul>',
        [example("2 kg 350 g", ["2 kg = 2 000 g", "2 000 + 350"], "2 350 g")],
        [['Wrong marks', 'Count what each mark is worth.'], ['100 g in a kilogram', '1 kg = 1 000 g.'], ['Different units', 'Change to the same unit first.']])
    faq = [('What does CAPS Grade 4 say about mass?', 'Estimate, measure, record, compare and order the mass of objects using bathroom scales, kitchen scales and balances, in grams and kilograms, and convert between g and kg.'), ('How heavy is a 1 litre bottle of water?', 'About 1 kg.'), ('Is mass the same as weight?', 'In everyday language we say weight, but in maths we measure mass.'), ('What scale is used for people?', 'A bathroom scale.')]
    make('mass', 22, 'Measurement', 'Grade 4: 4.2 Mass',
         'Estimate, measure, record, compare and order the mass of objects using bathroom scales, kitchen scales and balances; use grams (g) and kilograms (kg); calculate and solve problems involving mass; convert between g and kg (limited to whole numbers and common fractions).',
         'Mass: Grams and Kilograms', 'Mass',
         'Free CAPS Grade 4 mass worksheets: reading scales, grams and kilograms, converting, comparing masses and problems. 100 questions with memos.',
         '1 000 g = 1 kg.', 'Change to the same unit before comparing.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
