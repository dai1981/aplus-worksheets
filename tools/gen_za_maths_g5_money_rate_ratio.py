# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): Solving Problems: Money, Rate and Ratio (Grade 5: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g5_money_rate_ratio.py
Rand and cents, shopping and change, rates such as rand per kilogram, and sharing in a ratio (makers from the Grade 4
generator, with new numbers) and money estimation (Australia Year 5 maker).
Wrong answers come from real mistakes: writing R2,50 as 25c, giving the cost instead of the change, and sharing
equally when the story gives a ratio.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_za_maths_g4_money_rate_ratio as zm4
adopt(zm4)
if isinstance(getattr(zm4, 'R', None), random.Random): zm4.R = random.Random(805110)
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
        ("Rand and cents", [("collect", zm4.uniq(zm4.one_rc), 20)]),
        ("Shopping and change", [("collect", zm4.uniq(zm4.one_buy), 20)]),
        ("Rates", [("collect", zm4.uniq(zm4.one_rate), 20)]),
        ("Ratio", [("collect", zm4.uniq(zm4.one_ratio), 20)]),
        ("Mixed problems", [("collect", zm4.uniq(zm4.one_buy), 10), ("collect", zm4.uniq(zm4.one_rate), 10)]),
    ], 80511)
    finish(sets, R)
    body = lesson('<ul><li>R1 = 100c. R45,75 is 45 rand and 75 cents.</li><li>Change = money paid − total cost.</li><li>A <b>rate</b> compares different quantities: R24 per kg; 80 km per hour.</li><li>A <b>ratio</b> compares quantities of the same kind: 2 : 3 means for every 2 of one there are 3 of the other.</li></ul>',
        [example("Share R60 in the ratio 1 : 2", ["3 parts: R60 ÷ 3 = R20"], "R20 and R40")],
        [['R2,50 as 25c', 'R2,50 = 250c.'], ['Cost instead of change', 'Subtract from the money paid.'], ['Sharing equally', 'Use the ratio.']])
    faq = [('What does CAPS Grade 5 say about problem solving?', 'Solve problems in financial and measurement contexts, comparing quantities of the same kind (ratio) and of different kinds (rate), and grouping and equal sharing with remainders.'), ('What is a rate?', 'A comparison of two different quantities, like rand per kilogram.'), ('How do we write rand?', 'R45,75.'), ('Why estimate money?', 'To check you have enough before you pay.')]
    make('money-rate-and-ratio-problems', 11, 'Numbers, Operations and Relationships', 'Grade 5: 1.1 Whole numbers',
         'Solve problems in contexts involving whole numbers, including financial contexts, measurement contexts, comparing two or more quantities of the same kind (ratio), comparing two quantities of different kinds (rate), and grouping and equal sharing with remainders.',
         'Solving Problems: Money, Rate and Ratio', 'Money, Rate and Ratio',
         'Free CAPS Grade 5 money worksheets: rand and cents, shopping and change, rates, ratio and estimating with money. 100 questions with memos.',
         'Change = money paid − cost.', 'Rate: different kinds. Ratio: same kind.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
