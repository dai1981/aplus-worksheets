# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Adding and Subtracting Decimal Fractions (Grade 6: 1.3 Decimal fractions)
  python3 tools/gen_za_maths_g6_add_sub_decimals.py
Adding and subtracting decimals with up to 2 decimal places, lining up the decimal comma, filling empty places with
zeros, estimating and word problems (Australia Year 6, Ontario Grade 6 and US Grade 5 makers), in South African
decimal comma form.
Wrong answers come from real mistakes: lining up the last digits instead of the commas, forgetting to fill an empty
place, and carrying wrongly over the comma.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y6_add_sub_decimals as aua
adopt(aua)
if isinstance(getattr(aua, 'R', None), random.Random): aua.R = random.Random(806130)
import gen_caon_math_g6_add_sub_decimals as caa
adopt(caa)
if isinstance(getattr(caa, 'R', None), random.Random): caa.R = random.Random(806131)
import gen_us_math_g5_add_sub_decimals as usa
adopt(usa)
if isinstance(getattr(usa, 'R', None), random.Random): usa.R = random.Random(806132)
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
        ("Line up the commas", [("run", aua.set_line_up, (aua.People, "rnd", "seen"), 10, dec3), ("run", caa.set_line_up, (caa.People, "rnd", "seen"), 10, dec3)]),
        ("Different decimal places", [("run", aua.set_places, (aua.People, "rnd", "seen"), 10, dec3), ("run", caa.set_places, (caa.People, "rnd", "seen"), 10, dec3)]),
        ("Subtract with zeros", [("run", aua.set_zeros, (aua.People, "rnd", "seen"), 10, dec3), ("run", usa.set_subtract, (usa.People, "rnd", "seen"), 10, dec3)]),
        ("Estimate", [("run", aua.set_estimate, (aua.People,), 10, dec3), ("run", caa.set_estimate, (caa.People,), 10, dec3)]),
        ("Decimal problems", [("run", aua.set_words, (aua.People,), 10, dec3), ("run", caa.set_words, (caa.People,), 10, dec3)]),
    ], 80613)
    finish(sets, R)
    body = lesson('<ul><li>Write the numbers in columns with the decimal commas lined up.</li><li>Fill empty places with 0: 7,4 − 2,35 → 7,40 − 2,35.</li><li>Add or subtract as with whole numbers, and put the comma in the answer under the other commas.</li><li>Estimate first: 7,4 − 2,35 is about 7 − 2 = 5.</li></ul>',
        [example("12,6 + 3,85", ["12,60 + 3,85"], "16,45")],
        [['Lining up the last digits', 'Line up the commas.'], ['An empty place', 'Write 0 in it.'], ['The comma moves', 'Keep it under the other commas.']])
    faq = [('What does CAPS Grade 6 say about adding decimals?', 'Add and subtract decimal fractions with at least 2 decimal places.'), ('Why write 7,40 for 7,4?', 'It makes the columns the same length; the value is the same.'), ('How do I check?', 'Estimate with whole numbers.'), ('Where do we add decimals?', 'With money, lengths and masses.')]
    make('adding-and-subtracting-decimals', 13, 'Numbers, Operations and Relationships', 'Grade 6: 1.3 Decimal fractions',
         'Add and subtract decimal fractions with at least 2 decimal places; solve problems in context involving decimal fractions.',
         'Adding and Subtracting Decimal Fractions', 'Adding and Subtracting Decimals',
         'Free CAPS Grade 6 worksheets: adding and subtracting decimals, lining up the decimal comma, estimating and decimal problems. 100 questions with memos.',
         'Line up the decimal commas.', 'Fill empty places with 0.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
