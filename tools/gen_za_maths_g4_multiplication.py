# -*- coding: utf-8 -*-
"""
South Africa Grade 4 Maths (CAPS): Multiplication of 2-Digit by 2-Digit Numbers (Grade 4: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g4_multiplication.py
Multiplying 2-digit and 3-digit numbers by 1-digit numbers, multiplying 2-digit by 2-digit numbers with the grid
method and in columns (UK Year 4 and US Grade 4 makers), and word problems.
Wrong answers come from real mistakes: forgetting the 0 when multiplying by the tens, forgetting to carry, and
multiplying only the units.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y4_short_multiplication as uks
adopt(uks)
if hasattr(uks, 'R'): uks.R = random.Random(804060)
import gen_us_math_g4_multiplication as usm
adopt(usm)
if hasattr(usm, 'R'): usm.R = random.Random(804061)
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
        ("Grid method", [("run", uks.set_grid, ("rnd", "seen"), 20, le10000)]),
        ("2-digit by 1-digit", [("run", uks.set_short2, ("rnd", "seen"), 20, le10000)]),
        ("3-digit by 1-digit", [("run", uks.set_short3, ("rnd", "seen"), 20, le10000)]),
        ("2-digit by 2-digit", [("run", usm.set_area2, ("rnd", "seen"), 10, le10000), ("run", usm.set_std2, ("rnd", "seen"), 10, le10000)]),
        ("Multiplication problems", [("run", uks.set_story, ("rnd", uks.People), 20, le10000)]),
    ], 80406)
    finish(sets, R)
    body = lesson('<ul><li>Break the numbers into tens and units: 34 × 26 = 30 × 26 + 4 × 26.</li><li>In the grid method, multiply each part and add: 600 + 180 + 80 + 24 = 884.</li><li>In columns, multiply by the units first, then by the tens (write a 0 first), then add.</li><li>Estimate first: 34 × 26 is about 30 × 30 = 900.</li></ul>',
        [example("43 × 25", ["40 × 25 = 1 000", "3 × 25 = 75"], "1 075")],
        [['Missing the 0', 'When you multiply by 2 tens, the answer is in tens.'], ['Forgetting to carry', 'Add the carried digit.'], ['Only the units', 'Multiply every part.']])
    faq = [('What does CAPS Grade 4 say about multiplication?', 'Multiply at least whole 2-digit by 2-digit numbers, using properties of operations and techniques such as the grid method, doubling and halving, and breaking down numbers.'), ('What is the grid method?', 'Splitting both numbers into parts in a grid and adding the products.'), ('How do I check a product?', 'Estimate, or divide back.'), ('Is long multiplication in Grade 4?', '2-digit by 2-digit is the target.')]
    make('multiplication', 6, 'Numbers, Operations and Relationships', 'Grade 4: 1.1 Whole numbers',
         'Multiply at least whole 2-digit by 2-digit numbers.',
         'Multiplication of 2-Digit by 2-Digit Numbers', 'Multiplication',
         'Free CAPS Grade 4 multiplication worksheets: grid method, 2-digit and 3-digit by 1-digit, 2-digit by 2-digit and word problems. 100 questions with memos.',
         'Break into tens and units, multiply, then add.', 'Estimate first to check.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
