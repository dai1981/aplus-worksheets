# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Rounding Off to the Nearest 5, 10, 100, 1 000, 10 000, 100 000 and 1 000 000 (Grade 6: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g6_rounding.py
Rounding off to the nearest 5 (Grade 5 maker), to the nearest 10, 100 and 1 000 and to bigger places (UK Year 5
and Year 6 and Ontario Grade 6 makers), and rounding problems (maker from the Grade 4 generator).
Wrong answers come from real mistakes: rounding 5 down, looking at the wrong digit, and changing the digits to the
right of the rounding place to anything but 0.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y5_rounding as ukr
adopt(ukr)
if isinstance(getattr(ukr, 'R', None), random.Random): ukr.R = random.Random(806020)
import gen_uk_maths_y6_place_value as ukp
adopt(ukp)
if isinstance(getattr(ukp, 'R', None), random.Random): ukp.R = random.Random(806021)
import gen_caon_math_g6_place_value as cap
adopt(cap)
if isinstance(getattr(cap, 'R', None), random.Random): cap.R = random.Random(806022)
import gen_za_maths_g5_rounding as zr5
adopt(zr5)
if isinstance(getattr(zr5, 'R', None), random.Random): zr5.R = random.Random(806023)
import gen_za_maths_g4_rounding as zr4
adopt(zr4)
if isinstance(getattr(zr4, 'R', None), random.Random): zr4.R = random.Random(806024)
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
        ("Round to the nearest 5 and 10", [("collect", zr5.uniq(zr5.one_r5), 10), ("run", ukr.set_small, ("rnd", ukr.Picker), 10, nine)]),
        ("Round to 100 and 1 000", [("run", ukr.set_tenk, ("rnd", ukr.Picker), 20, nine)]),
        ("Round big numbers", [("run", ukr.set_hundredk, ("rnd", ukr.Picker), 10, nine), ("run", ukp.set_round, ("rnd", ukp.Picker), 10, nine)]),
        ("Mixed rounding", [("run", cap.set_round, ("rnd",), 8, nine), ("run", ukr.set_mixed, ("rnd", ukr.Picker), 12, nine)]),
        ("Rounding problems", [("collect", zr4.uniq(zr4.one_rw), 20)]),
    ], 80602)
    finish(sets, R)
    body = lesson('<ul><li>Find the two multiples the number lies between and choose the nearer one.</li><li>Look at the digit to the right of the rounding place: 5 or more, round up; less than 5, round down.</li><li>All the digits to the right of the rounding place become 0.</li><li>Rounding off helps to estimate answers.</li></ul>',
        [example("Round 4 762 381 to the nearest 100 000", ["between 4 700 000 and 4 800 000", "ten thousands digit 6"], "4 800 000")],
        [['Rounding 5 down', '5 or more rounds up.'], ['The wrong digit', 'Look one place to the right.'], ['Digits left behind', 'Everything to the right becomes 0.']])
    faq = [('What does CAPS Grade 6 say about rounding?', 'Round off to the nearest 5, 10, 100 and 1 000, and use rounding to estimate.'), ('What is 2 649 999 to the nearest million?', '3 000 000.'), ('Why round off?', 'To estimate and check answers quickly.'), ('Does rounding change the value?', 'Yes, a little. It gives a number that is easier to work with.')]
    make('rounding-off', 2, 'Numbers, Operations and Relationships', 'Grade 6: 1.1 Whole numbers',
         'Round off to the nearest 5, 10, 100 and 1 000; use a range of techniques to perform and check written and mental calculations, including estimation and rounding off.',
         'Rounding Off to the Nearest 5, 10, 100, 1 000, 10 000, 100 000 and 1 000 000', 'Rounding Off',
         'Free CAPS Grade 6 rounding off worksheets: round to the nearest 5, 10, 100, 1 000 and bigger places, and rounding problems. 100 questions with memos.',
         '5 or more: round up.', 'Digits to the right become 0.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
