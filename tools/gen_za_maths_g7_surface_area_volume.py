# -*- coding: utf-8 -*-
"""
South Africa Grade 7 Maths (CAPS): Surface Area and Volume of Cubes and Rectangular Prisms (Grade 7: 4.2 Surface area and volume of 3D objects)
  python3 tools/gen_za_maths_g7_surface_area_volume.py
Volume of cubes and rectangular prisms, missing lengths, surface area, and converting cubic units and capacity (UK Year
8, Australia Year 7 and BC Grade 7 makers and own maker).
Wrong answers come from real mistakes: adding the lengths instead of multiplying, counting only three faces for the
surface area, and using 100 instead of 1 000 for cubic units.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y7_volume_of_prisms as auv
adopt(auv)
if isinstance(getattr(auv, 'R', None), random.Random): auv.R = random.Random(807230)
import gen_uk_maths_y8_volume_and_surface_area_of_prisms as ukv
adopt(ukv)
if isinstance(getattr(ukv, 'R', None), random.Random): ukv.R = random.Random(807231)
import gen_cabc_math_g7_volume as cbv
adopt(cbv)
if isinstance(getattr(cbv, 'R', None), random.Random): cbv.R = random.Random(807232)
za_common.GRADE = "grade-7"

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
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok7(it):
    """Grade 7: no circles, pi or standard form (they come in Grade 8 and 9)"""
    return not _re.search(r"π|\bpi\b|circumference|radius|diameter|×\s?10<sup>|standard form|scientific notation", _txt(it))


def noneg(it):
    return ok7(it) and not _re.search(r"(?<![\d)] )[−-]\d", _txt(it))


def one_sa(r):
    k = r.choice(["cube", "box", "box", "units"])
    if k == "cube":
        a = r.randint(2, 15)
        return mcq("A cube has edges of %d cm. What is its surface area?" % a, "%s cm²" % comma(6 * a * a), ["%s cm²" % comma(x) for x in (a * a * a, 4 * a * a, a * a)],
                   "6 faces × %d × %d = <b>%s cm²</b>." % (a, a, comma(6 * a * a)))
    if k == "box":
        l, b, h = r.randint(3, 15), r.randint(2, 12), r.randint(2, 10)
        if len({l, b, h}) < 3:
            raise AssertionError
        sa = 2 * (l * b + l * h + b * h)
        return mcq("A rectangular prism is %d cm long, %d cm wide and %d cm high. What is its surface area?" % (l, b, h), "%s cm²" % comma(sa),
                   ["%s cm²" % comma(x) for x in (l * b * h, l * b + l * h + b * h, 2 * (l * b + l * h))],
                   "2 × (%d × %d + %d × %d + %d × %d) = 2 × (%d + %d + %d) = <b>%s cm²</b>." % (l, b, l, h, b, h, l * b, l * h, b * h, comma(sa)))
    v = r.choice([(2, "m³", "cm³", 1000000), (5, "cm³", "mm³", 1000), (3, "ℓ", "cm³", 1000), (4, "m³", "ℓ", 1000)])
    n, big, small, f = v
    return mcq("Convert %d %s to %s." % (n, big, small), "%s %s" % (comma(n * f), small), ["%s %s" % (comma(n * f // 10), small), "%s %s" % (comma(n * (100 if f >= 1000 else 10)), small), "%s %s" % (comma(n * f * 10), small)],
               "1 %s = %s %s, so %d %s = <b>%s %s</b>." % (big, comma(f), small, n, big, comma(n * f), small))


def build():
    sets, R = build_sets([
        ("Volume of cubes and rectangular prisms", [("collect", auv.one_cuboid, 10), ("collect", ukv.one_cuboid, 10)]),
        ("Missing lengths", [("collect", auv.one_missing, 20)]),
        ("Surface area", [("collect", uniq(one_sa), 20)]),
        ("Volume by layers", [("run", cbv.set_count, ("rnd",), 10, ok7), ("run", cbv.set_rect, ("rnd",), 10, ok7)]),
        ("Volume problems", [("run", cbv.set_story, (), 10, ok7), ("run", auv.problems, (), 10, ok7)]),
    ], 80723)
    finish(sets, R)
    body = lesson('<ul><li>Volume of a rectangular prism = length × breadth × height. Cube: V = l³.</li><li>Surface area = the total area of all the faces. Rectangular prism: 2(lb + lh + bh). Cube: 6l².</li><li>1 cm³ = 1 mℓ; 1 000 cm³ = 1 ℓ; 1 m³ = 1 000 ℓ.</li><li>Volume is in cubic units (cm³); surface area is in square units (cm²).</li></ul>',
        [example("A box 10 cm × 6 cm × 4 cm", ["V = 10 × 6 × 4", "SA = 2(60 + 40 + 24)"], "240 cm³ and 248 cm²")],
        [['Adding the lengths', 'Multiply length, breadth and height.'], ['Three faces only', 'A prism has 6 faces.'], ['100 for cubic units', '1 cm³ = 1 000 mm³.']])
    faq = [('What does CAPS Grade 7 say about surface area and volume?', 'Calculate the surface area, volume and capacity of cubes and rectangular prisms, and convert between cubic units and capacity units.'), ('What is 1 m³ in litres?', '1 000 ℓ.'), ('What does a net show?', 'All the faces you add for the surface area.'), ('Is volume the same as capacity?', 'Capacity is how much a container holds; it is measured in ℓ.')]
    make('surface-area-and-volume', 23, 'Measurement', 'Grade 7: 4.2 Surface area and volume of 3D objects',
         'Use appropriate formulae to calculate the surface area, volume and capacity of cubes and rectangular prisms; describe the interrelationship between surface area and volume; solve problems involving surface area, volume and capacity; use and convert between appropriate SI units, including mm³, cm³ and m³, and mℓ, ℓ and kℓ.',
         'Surface Area and Volume of Cubes and Rectangular Prisms', 'Surface Area and Volume',
         'Free CAPS Grade 7 surface area and volume worksheets: volume and surface area of cubes and rectangular prisms, missing lengths and unit conversions. 100 questions with memos.',
         'Volume = l × b × h.', 'Surface area: add all six faces.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
