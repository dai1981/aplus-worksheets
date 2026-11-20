# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): Division of 3-Digit by 2-Digit Numbers (Grade 5: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g5_division.py
Dividing by multiples of 10, dividing 3-digit numbers by 1-digit and 2-digit numbers, remainders and problems (US
Grade 5 and Australia Year 5 makers with South African names).
Wrong answers come from real mistakes: a remainder bigger than the divisor, leaving out a 0 in the answer, and
ignoring the remainder in a story.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_us_math_g5_division as usd
adopt(usd)
if isinstance(getattr(usd, 'R', None), random.Random): usd.R = random.Random(805060)
import gen_au_maths_y5_division as aud
adopt(aud)
if isinstance(getattr(aud, 'R', None), random.Random): aud.R = random.Random(805061)
za_common.GRADE = "grade-5"


import re as _re


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def _nums(it):
    return [int(x.replace(",", "").replace("\u00a0", "")) for x in _re.findall(r"(?<![\d.])\d[\d,\u00a0]*(?![.\d])", _txt(it)) if x.replace(",", "").replace("\u00a0", "").isdigit()]


def six(it):
    """whole numbers to 6 digits, no decimals, no negatives"""
    t = _txt(it)
    return all(n <= 999999 for n in _nums(it)) and not _re.search(r"\d\.\d|−\d", t)


def nodec(it):
    return not _re.search(r"\d\.\d|−\d", _txt(it))


def den12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " " + it["c"][it["a"]])]
    return all(d <= 12 for d in ds) and nodec(it)



def build():
    sets, R = build_sets([
        ("Divide by multiples of 10", [("run", usd.set_tens, ("rnd", "seen"), 20, six)]),
        ("3-digit by 1-digit", [("run", aud.set_small, ("rnd", "seen", aud.People), 20, six)]),
        ("3-digit by 2-digit", [("run", usd.set_two_digit, ("rnd", "seen"), 20, lambda it: six(it) and all(n < 1000 or n > 9999 for n in _nums(it)))]),
        ("Remainders", [("run", aud.set_remainders, ("rnd", "seen", aud.People), 20, six)]),
        ("Division problems", [("run", aud.set_context, ("rnd", "seen", aud.People), 10, six), ("run", aud.set_story, ("rnd", aud.People, "seen"), 10, six)]),
    ], 80506)
    finish(sets, R)
    body = lesson('<ul><li>To divide by a 2-digit number, estimate how many times it fits: 864 ÷ 24 → about 900 ÷ 25 = 36.</li><li>Use multiples of the divisor: 24, 48, 72, 96, 120 …</li><li>The remainder must be smaller than the divisor.</li><li>Check: answer × divisor + remainder = the number you divided.</li></ul>',
        [example("864 ÷ 24", ["24 × 30 = 720", "864 − 720 = 144", "24 × 6 = 144"], "36")],
        [['Big remainder', 'If the remainder ≥ divisor, divide again.'], ['Missing 0', '612 ÷ 6 = 102.'], ['Ignoring the remainder', 'Decide what the story needs.']])
    faq = [('What does CAPS Grade 5 say about division?', 'Divide at least whole 3-digit by 2-digit numbers.'), ('How do I check a division?', 'Multiply the answer by the divisor and add the remainder.'), ('What is a remainder?', 'What is left after making equal groups.'), ('When do I round up the answer?', 'When the extra ones still need a place, like seats in a taxi.')]
    make('division', 6, 'Numbers, Operations and Relationships', 'Grade 5: 1.1 Whole numbers',
         'Divide at least whole 3-digit by 2-digit numbers.',
         'Division of 3-Digit by 2-Digit Numbers', 'Division',
         'Free CAPS Grade 5 division worksheets: dividing by multiples of 10, 3-digit by 1-digit and 2-digit numbers, remainders and problems. 100 questions with memos.',
         'Estimate how many times the divisor fits.', 'The remainder is smaller than the divisor.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
