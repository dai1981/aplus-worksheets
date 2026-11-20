# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Length: Converting mm, cm, m and km with Decimals (Grade 6: 4.1 Length)
  python3 tools/gen_za_maths_g6_length.py
Choosing units, converting between mm, cm, m and km including decimals, comparing and ordering lengths, and length
problems (UK Year 6, Australia Year 6 and Ontario Grade 6 makers, and makers from the Grade 4 and Grade 5
generators), in South African decimal comma form.
Wrong answers come from real mistakes: using 100 instead of 1 000 for km and m, moving the comma the wrong way, and
subtracting before changing to the same unit.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y6_converting_units as ukc
adopt(ukc)
if isinstance(getattr(ukc, 'R', None), random.Random): ukc.R = random.Random(806260)
import gen_au_maths_y6_converting_units as auc
adopt(auc)
if isinstance(getattr(auc, 'R', None), random.Random): auc.R = random.Random(806261)
import gen_caon_math_g6_metric_time as cam
adopt(cam)
if isinstance(getattr(cam, 'R', None), random.Random): cam.R = random.Random(806262)
import gen_za_maths_g5_length as zl5
adopt(zl5)
if isinstance(getattr(zl5, 'R', None), random.Random): zl5.R = random.Random(806263)
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
        ("Choose the unit", [("run", auc.set_sensible, ("rnd",), 7, lambda it: len_only(it) and dec3(it)), ("collect", zl5.unit_maker("len"), 13)]),
        ("Convert whole units", [("collect", conv_maker([("m", "cm", 100), ("km", "m", 1000), ("cm", "mm", 10)]), 20)]),
        ("Convert with decimals", [("run", ukc.set_length, ("rnd",), 10, dec3), ("run", auc.set_length, ("rnd",), 10, dec3)]),
        ("Compare and order lengths", [("collect", zl5.order_maker("len"), 13), ("run", auc.set_compare, ("rnd",), 7, lambda it: len_only(it) and dec3(it))]),
        ("Length problems", [("collect", zl5.uniq(zl5.one_lstory), 16), ("run", cam.set_length, ("rnd",), 4, dec3)]),
    ], 80626)
    finish(sets, R)
    body = lesson('<ul><li>10 mm = 1 cm, 100 cm = 1 m, 1 000 m = 1 km.</li><li>To change to a smaller unit, multiply: 2,5 m = 250 cm.</li><li>To change to a bigger unit, divide: 1 750 m = 1,75 km.</li><li>Change to the same unit before you compare, add or subtract.</li></ul>',
        [example("3,2 km − 850 m", ["3,2 km = 3 200 m", "3 200 − 850"], "2 350 m")],
        [['100 m in a km', '1 km = 1 000 m.'], ['The comma the wrong way', 'A bigger unit gives a smaller number.'], ['Different units', 'Change to the same unit first.']])
    faq = [('What does CAPS Grade 6 say about length?', 'Estimate, measure, compare and order lengths, use mm, cm, m and km, solve problems and convert between units, including with decimal fractions to 2 decimal places.'), ('What is 0,5 km in metres?', '500 m.'), ('How many mm are in 1 m?', '1 000.'), ('Which unit for a road trip?', 'Kilometres.')]
    make('length', 26, 'Measurement', 'Grade 6: 4.1 Length',
         'Estimate, measure, record, compare and order lengths using appropriate measuring instruments; use millimetres (mm), centimetres (cm), metres (m) and kilometres (km); calculate and solve problems involving length, including problems with decimal fractions to 2 decimal places; convert between mm, cm, m and km, including conversions with decimal fractions.',
         'Length: Converting mm, cm, m and km with Decimals', 'Length',
         'Free CAPS Grade 6 length worksheets: choosing units, converting mm, cm, m and km with decimals, comparing lengths and problems. 100 questions with memos.',
         'Smaller unit: multiply. Bigger unit: divide.', 'Same unit before comparing.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
