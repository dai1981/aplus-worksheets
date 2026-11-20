# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): Multiplication of 3-Digit by 2-Digit Numbers (Grade 5: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g5_multiplication.py
Mental multiplication, 2-digit by 2-digit and 3-digit by 2-digit multiplication with the grid method and in columns,
and word problems (UK Year 5, Australia Year 5 and BC Grade 5 makers).
Wrong answers come from real mistakes: forgetting the 0 when multiplying by the tens, forgetting to carry, and adding
the partial products wrongly.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y5_multiplication as ukm
adopt(ukm)
if isinstance(getattr(ukm, 'R', None), random.Random): ukm.R = random.Random(805050)
import gen_au_maths_y5_multiplication as aum
adopt(aum)
if isinstance(getattr(aum, 'R', None), random.Random): aum.R = random.Random(805051)
import gen_cabc_math_g5_multiplication as cbm
adopt(cbm)
if isinstance(getattr(cbm, 'R', None), random.Random): cbm.R = random.Random(805052)
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
        ("Mental multiplication", [("run", ukm.set_mental, ("rnd",), 15, six), ("run", cbm.set_tens, ("rnd",), 5, six)]),
        ("Grid method", [("run", aum.set_area, ("rnd", "seen"), 20, six)]),
        ("2-digit by 2-digit", [("run", ukm.set_2x2, ("rnd", "seen", ukm.People), 20, six)]),
        ("3-digit by 2-digit", [("run", aum.set_long, ("rnd", "seen", aum.People), 20, six)]),
        ("Multiplication problems", [("run", ukm.set_story, ("rnd", ukm.People), 10, six), ("run", cbm.set_story, ("rnd", cbm.People), 10, six)]),
    ], 80505)
    finish(sets, R)
    body = lesson('<ul><li>Break the numbers into hundreds, tens and units: 243 × 36 = 243 × 30 + 243 × 6.</li><li>Grid method: multiply each part and add the partial products.</li><li>In columns, multiply by the units, then by the tens (write a 0 first), then add.</li><li>Estimate: 243 × 36 is about 240 × 40 = 9 600.</li></ul>',
        [example("243 × 36", ["243 × 30 = 7 290", "243 × 6 = 1 458"], "8 748")],
        [['Missing the 0', 'Multiplying by 3 tens gives tens.'], ['Forgetting to carry', 'Add the carried digit.'], ['Adding wrongly', 'Line up the partial products.']])
    faq = [('What does CAPS Grade 5 say about multiplication?', 'Multiply at least whole 3-digit by 2-digit numbers.'), ('What is a partial product?', 'The answer for one part, like 243 × 30.'), ('How do I check?', 'Estimate, or divide back.'), ('Do I need the times tables?', 'Yes, up to 10 × 10 by heart.')]
    make('multiplication', 5, 'Numbers, Operations and Relationships', 'Grade 5: 1.1 Whole numbers',
         'Multiply at least whole 3-digit by 2-digit numbers.',
         'Multiplication of 3-Digit by 2-Digit Numbers', 'Multiplication',
         'Free CAPS Grade 5 multiplication worksheets: mental multiplication, grid method, 2-digit by 2-digit and 3-digit by 2-digit and word problems. 100 questions with memos.',
         'Multiply by the units, then by the tens, then add.', 'Estimate first.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
