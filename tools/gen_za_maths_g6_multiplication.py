# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Multiplication of 4-Digit by 3-Digit Numbers (Grade 6: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g6_multiplication.py
Multiplying by multiples of 10, 3-digit by 2-digit and 4-digit by 2-digit and 3-digit numbers, finding errors, and
word problems (UK Year 6, Australia Year 6 and BC Grade 5 makers).
Wrong answers come from real mistakes: forgetting the zeros when multiplying by tens and hundreds, forgetting to
carry, and adding the partial products wrongly.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y6_long_multiplication as ukm
adopt(ukm)
if isinstance(getattr(ukm, 'R', None), random.Random): ukm.R = random.Random(806050)
import gen_au_maths_y6_multiply_divide as aum
adopt(aum)
if isinstance(getattr(aum, 'R', None), random.Random): aum.R = random.Random(806051)
import gen_cabc_math_g5_multiplication as cbm
adopt(cbm)
if isinstance(getattr(cbm, 'R', None), random.Random): cbm.R = random.Random(806052)
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


def uniq(fn):
    seen = set()
    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


def one_43(r):
    a = r.randint(1000, 9999)
    b = r.randint(102, 999)
    if b % 10 == 0 or a % 10 == 0:
        raise AssertionError
    p = a * b
    h, t, u = b // 100, b // 10 % 10, b % 10
    wr = [a * h * 100 + a * t * 10 + a * u - a * h * 90, a * h + a * t + a * u if a * (h + t + u) != p else p + 10, p + 1000 * r.choice([1, 10]), p - a * u]
    wr = [x for x in wr if x != p and x > 0]
    return mcq("%s × %d = ?" % (comma(a), b), comma(p), [comma(x) for x in wr[:3]],
               "%s × %d = %s; %s × %d = %s; %s × %d = %s. Add: <b>%s</b>." % (comma(a), h * 100, comma(a * h * 100), comma(a), t * 10, comma(a * t * 10), comma(a), u, comma(a * u), comma(p)))


def build():
    sets, R = build_sets([
        ("Multiply by multiples of 10", [("run", cbm.set_tens, ("rnd",), 15, nine), ("run", ukm.set_2x2, ("rnd", "seen"), 5, nine)]),
        ("3-digit by 2-digit", [("run", ukm.set_3x2, ("rnd", "seen"), 20, nine)]),
        ("4-digit by 2-digit", [("run", ukm.set_4x2, ("rnd", "seen"), 20, nine)]),
        ("4-digit by 3-digit", [("collect", uniq(one_43), 20)]),
        ("Multiplication problems", [("run", ukm.set_story, ("rnd", ukm.People), 10, nine), ("run", aum.set_multiply, ("rnd", "seen", aum.People), 10, nine)]),
    ], 80605)
    finish(sets, R)
    body = lesson('<ul><li>Break the second number into hundreds, tens and units: 2 345 × 216 = 2 345 × 200 + 2 345 × 10 + 2 345 × 6.</li><li>In columns, multiply by the units, then by the tens (write one 0), then by the hundreds (write two 0s).</li><li>Add the partial products.</li><li>Estimate first: 2 345 × 216 is about 2 000 × 200 = 400 000.</li></ul>',
        [example("2 345 × 216", ["2 345 × 200 = 469 000", "2 345 × 16 = 37 520"], "506 520")],
        [['Missing zeros', 'Multiplying by hundreds needs two 0s.'], ['Forgetting to carry', 'Add the carried digit.'], ['Adding wrongly', 'Line up the partial products.']])
    faq = [('What does CAPS Grade 6 say about multiplication?', 'Multiply at least whole 4-digit by 3-digit numbers.'), ('How many partial products are there for × 216?', 'Three: × 200, × 10 and × 6.'), ('How do I check?', 'Estimate, or use a calculator to check.'), ('Is 25 × 4 useful?', 'Yes, 25 × 4 = 100 makes many products easy.')]
    make('multiplication', 5, 'Numbers, Operations and Relationships', 'Grade 6: 1.1 Whole numbers',
         'Multiply at least whole 4-digit by 3-digit numbers.',
         'Multiplication of 4-Digit by 3-Digit Numbers', 'Multiplication',
         'Free CAPS Grade 6 multiplication worksheets: multiplying by multiples of 10, 3-digit by 2-digit and 4-digit by 3-digit numbers and word problems. 100 questions with memos.',
         'Units, tens, hundreds, then add the partial products.', 'Estimate first.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
