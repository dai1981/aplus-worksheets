# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Whole Numbers to 9 Digits: Place Value, Comparing and Ordering (Grade 6: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g6_whole_numbers.py
Place value of numbers to 9 digits, reading and writing numbers, comparing and ordering (UK Year 6, Ontario Grade 6
and BC Grade 6 makers) and expanded notation (maker from the Grade 5 generator), with South African number writing.
Wrong answers come from real mistakes: mixing up the value and the digit, leaving out a 0 for an empty place, and
comparing numbers with different numbers of digits from the left.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y6_place_value as ukp
adopt(ukp)
if isinstance(getattr(ukp, 'R', None), random.Random): ukp.R = random.Random(806010)
import gen_caon_math_g6_place_value as cap
adopt(cap)
if isinstance(getattr(cap, 'R', None), random.Random): cap.R = random.Random(806011)
import gen_cabc_math_g6_place_value as cbp
adopt(cbp)
if isinstance(getattr(cbp, 'R', None), random.Random): cbp.R = random.Random(806012)
import gen_za_maths_g5_whole_numbers as zw5
adopt(zw5)
if isinstance(getattr(zw5, 'R', None), random.Random): zw5.R = random.Random(806013)
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
        ("Place value", [("run", ukp.set_value, ("rnd", "seen"), 10, nine), ("run", cap.set_whole, ("rnd", "seen"), 10, nine)]),
        ("Read and write numbers", [("run", cbp.set_read, (), 5, nine), ("run", ukp.set_words, ("rnd", ukp.People), 15, nine)]),
        ("Expanded notation", [("run", cbp.set_whole, ("rnd", "seen"), 10, nine), ("collect", zw5.uniq(zw5.one_expand), 10)]),
        ("Compare and order", [("run", ukp.set_compare, ("rnd", "seen"), 10, nine), ("run", cap.set_compare, ("rnd", "seen"), 10, nine)]),
        ("More place value", [("run", cbp.set_compare, (), 10, nine), ("run", cap.set_whole, ("rnd", "seen"), 10, nine)]),
    ], 80601)
    finish(sets, R)
    body = lesson('<ul><li>A 9-digit number has three groups: millions, thousands and units: 345 208 917.</li><li>In 345 208 917 the 4 is worth 40 000 000 (forty million).</li><li>Write 0 for an empty place: three million and five = 3 000 005.</li><li>To compare, count the digits first. With the same number of digits, compare from the left.</li></ul>',
        [example("Twelve million four hundred and six thousand and thirty", ["12 million", "406 thousand", "030"], "12 406 030")],
        [['Value or digit?', 'The digit 4 in 345 208 917 has a value of 40 000 000.'], ['A missing 0', 'Write 0 for every empty place.'], ['Fewer digits, bigger number', 'Count the digits first.']])
    faq = [('What does CAPS Grade 6 say about whole numbers?', 'Count, order, compare and represent numbers to at least 9-digit numbers, and recognise the place value of digits in whole numbers to at least 9 digits.'), ('How many zeros are in one million?', 'Six: 1 000 000.'), ('How do South Africans write big numbers?', 'With a space between groups of three digits: 345 208 917.'), ('What is a billion?', '1 000 million: 1 000 000 000.')]
    make('whole-numbers-to-9-digits', 1, 'Numbers, Operations and Relationships', 'Grade 6: 1.1 Whole numbers',
         'Count forwards and backwards in whole number intervals and fractions; order, compare and represent numbers to at least 9-digit numbers; represent odd and even numbers to at least 1 000 000; recognise the place value of digits in whole numbers to at least 9-digit numbers.',
         'Whole Numbers to 9 Digits: Place Value, Comparing and Ordering', 'Whole Numbers to 9 Digits',
         'Free CAPS Grade 6 whole numbers worksheets: 9-digit place value, reading and writing numbers, expanded notation, comparing and ordering. 100 questions with memos.',
         'Millions, thousands, units: three groups of three digits.', 'Count the digits first, then compare from the left.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
