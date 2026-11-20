# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Mass: Converting Grams and Kilograms with Decimals (Grade 6: 4.2 Mass)
  python3 tools/gen_za_maths_g6_mass.py
Choosing units, converting between g and kg including decimals, comparing and ordering masses, and mass problems
(UK Year 6, Australia Year 6 and Ontario Grade 6 makers, and makers from the Grade 4 and Grade 5 generators).
Wrong answers come from real mistakes: using 100 instead of 1 000 for kg and g, moving the comma the wrong way, and
subtracting before changing to the same unit.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y6_converting_units as ukc
adopt(ukc)
if isinstance(getattr(ukc, 'R', None), random.Random): ukc.R = random.Random(806270)
import gen_au_maths_y6_converting_units as auc
adopt(auc)
if isinstance(getattr(auc, 'R', None), random.Random): auc.R = random.Random(806271)
import gen_caon_math_g6_metric_time as cam
adopt(cam)
if isinstance(getattr(cam, 'R', None), random.Random): cam.R = random.Random(806272)
import gen_za_maths_g5_mass as zm5
adopt(zm5)
if isinstance(getattr(zm5, 'R', None), random.Random): zm5.R = random.Random(806273)
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
        ("Choose the unit", [("run", auc.set_sensible, ("rnd",), 6, lambda it: mass_only(it) and dec3(it)), ("collect", zm5.unit_maker("mass"), 14)]),
        ("Convert grams and kilograms", [("collect", conv_maker([("kg", "g", 1000)]), 20)]),
        ("Convert with decimals", [("run", ukc.set_mass_cap, ("rnd",), 10, lambda it: mass_only(it) and dec3(it)), ("run", auc.set_mass_cap, ("rnd",), 7, lambda it: mass_only(it) and dec3(it)), ("collect", conv_maker([("kg", "g", 1000)]), 3)]),
        ("Compare and order masses", [("collect", zm5.order_maker("mass"), 20)]),
        ("Mass problems", [("collect", story_maker(("kg", "kgadd")), 20)]),
    ], 80627)
    finish(sets, R)
    body = lesson('<ul><li>1 kg = 1 000 g.</li><li>To change kg to g, multiply by 1 000: 2,35 kg = 2 350 g.</li><li>To change g to kg, divide by 1 000: 750 g = 0,75 kg.</li><li>Change to the same unit before you compare, add or subtract.</li></ul>',
        [example("1,2 kg + 650 g", ["1,2 kg = 1 200 g", "1 200 + 650"], "1 850 g")],
        [['100 g in a kg', '1 kg = 1 000 g.'], ['The comma the wrong way', 'kg is bigger, so the number is smaller.'], ['Different units', 'Change to grams first.']])
    faq = [('What does CAPS Grade 6 say about mass?', 'Estimate, measure, compare and order masses in g and kg, solve problems and convert between units, including with decimal fractions.'), ('What is 0,25 kg in grams?', '250 g.'), ('Which is heavier, 1,5 kg or 1 450 g?', '1,5 kg = 1 500 g, so 1,5 kg.'), ('Which scale measures mass?', 'A kitchen scale or a bathroom scale.')]
    make('mass', 27, 'Measurement', 'Grade 6: 4.2 Mass',
         'Estimate, measure, record, compare and order objects using measuring instruments; use grams (g) and kilograms (kg); calculate and solve problems involving mass, including problems with decimal fractions to 2 decimal places; convert between grams and kilograms, including conversions with decimal fractions.',
         'Mass: Converting Grams and Kilograms with Decimals', 'Mass',
         'Free CAPS Grade 6 mass worksheets: grams and kilograms, converting with decimals, comparing masses and problems. 100 questions with memos.',
         '1 kg = 1 000 g.', 'Same unit before comparing.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
