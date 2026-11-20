# -*- coding: utf-8 -*-
"""
South Africa Grade 8 Maths (CAPS): Surface Area and Volume of Prisms (Grade 8: 4.2 Surface area and volume of 3D objects)
  python3 tools/gen_za_maths_g8_surface_area_volume.py
Volume and surface area of cubes, rectangular prisms and triangular prisms, capacity, and missing lengths (UK Year 8
and Australia Year 7 and Year 8 makers and the surface area maker from the Grade 7 generator).
Wrong answers come from real mistakes: using the length of a slant edge as the height, counting only some faces, and
using 100 instead of 1 000 for cubic units.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y8_volume_and_surface_area_of_prisms as ukv
adopt(ukv)
if isinstance(getattr(ukv, 'R', None), random.Random): ukv.R = random.Random(808190)
import gen_au_maths_y7_volume_of_prisms as auv
adopt(auv)
if isinstance(getattr(auv, 'R', None), random.Random): auv.R = random.Random(808191)
import gen_au_maths_y8_volume_and_capacity as auc
adopt(auc)
if isinstance(getattr(auc, 'R', None), random.Random): auc.R = random.Random(808192)
import gen_za_maths_g7_surface_area_volume as zs7
adopt(zs7)
if isinstance(getattr(zs7, 'R', None), random.Random): zs7.R = random.Random(808193)
za_common.GRADE = "grade-8"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok8(it):
    """Grade 8: no trigonometry, quadratic formula or surds beyond square roots"""
    return not _re.search(r"\b(sin|cos|tan)\b|quadratic|discriminant|imperial|\bmiles?\b", _txt(it))



def build():
    sets, R = build_sets([
        ("Volume of rectangular prisms", [("collect", ukv.one_cuboid, 10), ("collect", auv.one_cuboid, 10)]),
        ("Volume of triangular prisms", [("collect", ukv.one_prism, 10), ("collect", auv.one_tri, 10)]),
        ("Surface area", [("collect", ukv.one_sa, 10), ("collect", zs7.uniq(zs7.one_sa), 10)]),
        ("Volume and capacity", [("collect", auc.one_conv, 10), ("collect", auc.one_cap, 10)]),
        ("Missing lengths", [("collect", auc.one_missing, 10), ("collect", auv.one_missing, 10)]),
    ], 80819)
    finish(sets, R)
    body = lesson('<ul><li>Volume of a prism = area of the cross-section × length.</li><li>Triangular prism: V = ½ × b × h × l.</li><li>Surface area = the total area of all the faces (use a net).</li><li>1 cm³ = 1 mℓ, 1 000 cm³ = 1 ℓ, 1 m³ = 1 000 ℓ.</li></ul>',
        [example("A triangular prism: triangle base 6 cm, height 4 cm, length 10 cm", ["½ × 6 × 4 = 12 cm²"], "V = 120 cm³")],
        [['The slant edge', 'Use the perpendicular height.'], ['Some faces only', 'Add every face.'], ['100 for cubic units', '1 cm³ = 1 000 mm³.']])
    faq = [('What does CAPS Grade 8 say about surface area and volume?', 'Calculate the surface area, volume and capacity of cubes, rectangular prisms and triangular prisms, and convert between units.'), ('What is a cross-section?', 'The shape that stays the same along the length of a prism.'), ('How many litres is 1 m³?', '1 000 ℓ.'), ('Is surface area in cm³?', 'No, in cm².')]
    make('surface-area-and-volume', 19, 'Measurement', 'Grade 8: 4.2 Surface area and volume of 3D objects',
         'Use appropriate formulae to calculate the surface area, volume and capacity of cubes, rectangular prisms and triangular prisms; describe the interrelationship between surface area and volume of the objects mentioned above; use and convert between appropriate SI units.',
         'Surface Area and Volume of Prisms', 'Surface Area and Volume',
         'Free CAPS Grade 8 surface area and volume worksheets: rectangular and triangular prisms, capacity and missing lengths. 100 questions with memos.',
         'Volume = cross-section × length.', 'Surface area: add all the faces.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
