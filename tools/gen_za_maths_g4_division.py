# -*- coding: utf-8 -*-
"""
South Africa Grade 4 Maths (CAPS): Division of 3-Digit by 1-Digit Numbers with Remainders (Grade 4: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g4_division.py
Division facts, dividing 2-digit and 3-digit numbers by 1-digit numbers, remainders and grouping and sharing
problems (US Grade 4 and BC Grade 4 makers with South African names).
Wrong answers come from real mistakes: a remainder bigger than the divisor, leaving out a 0 in the answer, and
ignoring the remainder in a story.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_us_math_g4_division as usd
adopt(usd)
if hasattr(usd, 'R'): usd.R = random.Random(804070)
import gen_cabc_math_g4_mult_div as cbd
adopt(cbd)
if hasattr(cbd, 'R'): cbd.R = random.Random(804071)
za_common.GRADE = "grade-4"


import re as _re


def _nums(it):
    t = _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"]
    t = _re.sub(r"<[^>]+>", " ", t)
    return [int(x.replace(",", "").replace("\u00a0", "")) for x in _re.findall(r"(?<![\d.])\d[\d,\u00a0]*(?![.\d])", t) if x.replace(",", "").replace("\u00a0", "").isdigit()]


def le10000(it):
    return all(n <= 10000 for n in _nums(it))


def le100k(it):
    return all(n <= 99999 for n in _nums(it))


def den12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " ".join(it["c"]))]
    return all(d <= 12 for d in ds)


def den8(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " ".join(it["c"]))]
    return all(d <= 8 for d in ds)



def build():
    sets, R = build_sets([
        ("Division facts", [("run", usd.set_facts, ("rnd", "seen"), 20, le10000)]),
        ("3-digit by 1-digit", [("run", usd.set_no_rem, ("rnd", "seen"), 20, le10000)]),
        ("Remainders", [("run", usd.set_rem, ("rnd", "seen", usd.People), 20, le10000)]),
        ("Sharing and grouping", [("run", cbd.set_share, ("rnd", "seen"), 20, le10000)]),
        ("Remainders in stories", [("run", cbd.set_rem, ("rnd", "seen", cbd.People), 20, le10000)]),
    ], 80407)
    finish(sets, R)
    body = lesson('<ul><li>Division shares a number into equal groups or finds how many groups there are.</li><li>Break the number down: 864 ÷ 4 = 800 ÷ 4 + 64 ÷ 4 = 200 + 16 = 216.</li><li>The <b>remainder</b> is what is left over. It must be smaller than the divisor.</li><li>In a story, decide what to do with the remainder: 27 learners in cars of 4 need 7 cars.</li></ul>',
        [example("458 ÷ 3", ["300 ÷ 3 = 100", "150 ÷ 3 = 50", "8 ÷ 3 = 2 r 2"], "152 r 2")],
        [['Big remainder', 'If the remainder ≥ the divisor, divide again.'], ['Missing 0', '612 ÷ 6 = 102, not 12.'], ['Ignoring the remainder', 'Think about what the story needs.']])
    faq = [('What does CAPS Grade 4 say about division?', 'Divide at least whole 3-digit by 1-digit numbers, including grouping and equal sharing with remainders.'), ('What is a remainder?', 'The amount left after equal groups are made.'), ('How do I check a division?', 'Answer × divisor + remainder = the number.'), ('Can I divide by 0?', 'No.')]
    make('division', 7, 'Numbers, Operations and Relationships', 'Grade 4: 1.1 Whole numbers',
         'Divide at least whole 3-digit by 1-digit numbers; solve problems involving grouping and equal sharing with remainders.',
         'Division of 3-Digit by 1-Digit Numbers with Remainders', 'Division',
         'Free CAPS Grade 4 division worksheets: division facts, 3-digit by 1-digit numbers, remainders, sharing and grouping problems. 100 questions with memos.',
         'The remainder is smaller than the divisor.', 'Check: answer × divisor + remainder.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
