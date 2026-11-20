# -*- coding: utf-8 -*-
"""
South Africa Grade 9 Maths (CAPS): Surface Area and Volume of Prisms and Cylinders (Grade 9: 4.2 Surface area and volume of 3D objects)
  python3 tools/gen_za_maths_g9_surface_area_volume.py
Volume and surface area of rectangular and triangular prisms and cylinders, and capacity (Singapore Secondary 1, UK
Year 8 and BC Grade 8 makers).
Wrong answers come from real mistakes: using the diameter as the radius, leaving out the curved surface, and using 100
instead of 1 000 for cubic units.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_sg_maths_s1_volume_and_surface_area_of_prisms_and_cylinders as sgv
adopt(sgv)
if isinstance(getattr(sgv, 'R', None), random.Random): sgv.R = random.Random(809170)
import gen_uk_maths_y8_volume_and_surface_area_of_prisms as ukv
adopt(ukv)
if isinstance(getattr(ukv, 'R', None), random.Random): ukv.R = random.Random(809171)
import gen_cabc_math_g8_surface_area_volume as cbs
adopt(cbs)
if isinstance(getattr(cbs, 'R', None), random.Random): cbs.R = random.Random(809172)
za_common.GRADE = "grade-9"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok9(it):
    """Grade 9: no trigonometry, quadratic formula, simultaneous equations or cones and spheres (Grade 10+)"""
    return not _re.search(r"\b(sin|cos|tan)\b|quadratic formula|discriminant|simultaneous|\bcone|\bsphere|imperial|\bmiles?\b", _txt(it))



def build():
    sets, R = build_sets([
        ("Volume of prisms", [("collect", sgv.one_cuboid, 10), ("collect", sgv.one_prism, 10)]),
        ("Volume of cylinders", [("collect", sgv.one_cyl, 10), ("collect", ukv.one_cyl, 10)]),
        ("Surface area of prisms", [("collect", sgv.one_sa, 10), ("run", cbs.set_prism_sa, (), 10, ok9)]),
        ("Surface area of cylinders", [("run", cbs.set_cyl_sa, (), 20, ok9)]),
        ("Volume problems", [("run", cbs.set_story, (), 10, ok9), ("run", sgv.problems, (), 10, ok9)]),
    ], 80917)
    finish(sets, R)
    body = lesson('<ul><li>Volume of a prism or cylinder = area of the base × height.</li><li>Cylinder: V = πr²h.</li><li>Surface area of a cylinder = 2πr² + 2πrh (two circles and the curved rectangle).</li><li>1 cm³ = 1 mℓ; 1 000 cm³ = 1 ℓ.</li></ul>',
        [example("A cylinder with r = 5 cm and h = 10 cm", ["V = π × 25 × 10"], "about 785 cm³")],
        [['Diameter as radius', 'r = d ÷ 2.'], ['No curved surface', 'Add 2πrh.'], ['100 for cubic units', '1 cm³ = 1 000 mm³.']])
    faq = [('What does CAPS Grade 9 say about surface area and volume?', 'Calculate the surface area, volume and capacity of cubes, rectangular prisms, triangular prisms and cylinders.'), ('What is the curved surface of a cylinder?', 'A rectangle 2πr by h when unrolled.'), ('How many litres does 1 m³ hold?', '1 000 ℓ.'), ('What happens to the volume if the radius doubles?', 'It becomes 4 times as big.')]
    make('surface-area-and-volume', 17, 'Measurement', 'Grade 9: 4.2 Surface area and volume of 3D objects',
         'Use appropriate formulae to calculate the surface area, volume and capacity of cubes, rectangular prisms, triangular prisms and cylinders; investigate how doubling any or all the dimensions of right prisms and cylinders affects their volume; solve problems involving surface area, volume and capacity.',
         'Surface Area and Volume of Prisms and Cylinders', 'Surface Area and Volume',
         'Free CAPS Grade 9 surface area and volume worksheets: prisms and cylinders, capacity and volume problems. 100 questions with memos.',
         'Cylinder: V = πr²h.', 'SA of a cylinder = 2πr² + 2πrh.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
