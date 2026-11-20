# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Capacity and Volume: Millilitres, Litres and Cubic Centimetres (Grade 6: 4.3 Capacity/Volume)
  python3 tools/gen_za_maths_g6_capacity.py
Choosing units, converting between mℓ and ℓ including decimals, comparing capacities, the link between cm³ and mℓ,
and capacity problems (UK Year 6, Australia Year 6 and BC Grade 6 makers, and makers from the Grade 4 and Grade 5
generators).
Wrong answers come from real mistakes: using 100 instead of 1 000 for ℓ and mℓ, moving the comma the wrong way, and
mixing up capacity and volume.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y6_converting_units as ukc
adopt(ukc)
if isinstance(getattr(ukc, 'R', None), random.Random): ukc.R = random.Random(806280)
import gen_au_maths_y6_converting_units as auc
adopt(auc)
if isinstance(getattr(auc, 'R', None), random.Random): auc.R = random.Random(806281)
import gen_cabc_math_g6_volume as cbv
adopt(cbv)
if isinstance(getattr(cbv, 'R', None), random.Random): cbv.R = random.Random(806282)
import gen_za_maths_g5_capacity as zc5
adopt(zc5)
if isinstance(getattr(zc5, 'R', None), random.Random): zc5.R = random.Random(806283)
from gen_za_maths_g4_length import conv_maker, story_maker, mass_only, cap_only, len_only
za_common.GRADE = "grade-6"


import re as _re


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def _nums(it):
    return [int(x.replace(",", "").replace("\u00a0", "")) for x in _re.findall(r"(?<![\d.])\d[\d,\u00a0]*(?![.\d])", _txt(it)) if x.replace(",", "").replace("\u00a0", "").isdigit()]


def noneg(it):
    return not _re.search(r"(?<![\d)] )[−-]\d", _txt(it)) and "negative" not in _txt(it).lower()


def nine(it):
    """whole numbers to 9 digits, no negatives"""
    return all(n <= 999999999 for n in _nums(it)) and noneg(it)


def dec3(it):
    """decimals with at most 3 places, no negatives"""
    return noneg(it) and not _re.search(r"\d\.\d{4}", _txt(it))


def nodec(it):
    return noneg(it) and not _re.search(r"\d\.\d", _txt(it))


def flat(it):
    """first quadrant only: no negative numbers in the text or the picture"""
    return nodec(it) and "−" not in it["q"] and "-1" not in it["q"]


def nomean(it):
    return dec3(it) and not _re.search(r"\bmean\b", _txt(it))


def den12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " " + it["c"][it["a"]])]
    return all(d <= 12 or d in (20, 25, 50, 100) for d in ds) and nodec(it)



def build():
    sets, R = build_sets([
        ("Choose the unit", [("collect", zc5.unit_maker("cap"), 20)]),
        ("Convert millilitres and litres", [("collect", conv_maker([("ℓ", "mℓ", 1000)]), 20)]),
        ("Convert with decimals", [("run", ukc.set_mass_cap, ("rnd",), 5, lambda it: cap_only(it) and dec3(it)), ("run", auc.set_mass_cap, ("rnd",), 5, lambda it: cap_only(it) and dec3(it)), ("collect", conv_maker([("ℓ", "mℓ", 1000)]), 10)]),
        ("Capacity and volume", [("run", cbv.set_capacity, (), 10, dec3), ("run", cbv.set_link, (), 10, dec3)]),
        ("Capacity problems", [("collect", story_maker(("l", "ladd", "lglass")), 20)]),
    ], 80628)
    finish(sets, R)
    body = lesson('<ul><li>1 ℓ = 1 000 mℓ.</li><li>To change ℓ to mℓ, multiply by 1 000: 1,5 ℓ = 1 500 mℓ. To change mℓ to ℓ, divide by 1 000.</li><li>Capacity is how much a container can hold. Volume is the space an object takes up.</li><li>1 cm³ holds 1 mℓ, so a 1 000 cm³ box holds 1 ℓ.</li></ul>',
        [example("A 2 ℓ jug fills cups of 250 mℓ", ["2 ℓ = 2 000 mℓ", "2 000 ÷ 250"], "8 cups")],
        [['100 mℓ in a litre', '1 ℓ = 1 000 mℓ.'], ['The comma the wrong way', 'ℓ is bigger, so the number is smaller.'], ['Capacity or volume?', 'Capacity: what it holds. Volume: space it takes up.']])
    faq = [('What does CAPS Grade 6 say about capacity and volume?', 'Estimate, measure, compare and order capacity and volume in mℓ and ℓ, solve problems and convert between units, including with decimal fractions.'), ('How many mℓ is 0,75 ℓ?', '750 mℓ.'), ('What is 1 cm³?', 'A cube with 1 cm sides; it holds 1 mℓ.'), ('Which unit for a bath?', 'Litres.')]
    make('capacity-and-volume', 28, 'Measurement', 'Grade 6: 4.3 Capacity/Volume',
         'Estimate, measure, record, compare and order capacity and volume using appropriate measuring instruments; use millilitres (mℓ) and litres (ℓ); calculate and solve problems involving capacity and volume, including problems with decimal fractions to 2 decimal places; convert between litres and millilitres, including conversions with decimal fractions.',
         'Capacity and Volume: Millilitres, Litres and Cubic Centimetres', 'Capacity and Volume',
         'Free CAPS Grade 6 capacity and volume worksheets: millilitres and litres, converting with decimals, cm³ and problems. 100 questions with memos.',
         '1 ℓ = 1 000 mℓ.', '1 cm³ holds 1 mℓ.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
