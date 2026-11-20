# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Division of 4-Digit by 3-Digit Numbers (Grade 6: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g6_division.py
Short division, long division of 3-digit and 4-digit numbers by 2-digit and 3-digit numbers, remainders and problems
(UK Year 6 and Australia Year 6 makers, and own maker for 3-digit divisors).
Wrong answers come from real mistakes: a remainder bigger than the divisor, leaving out a 0 in the answer, and
ignoring the remainder in a story.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y6_long_division as ukd
adopt(ukd)
if isinstance(getattr(ukd, 'R', None), random.Random): ukd.R = random.Random(806060)
import gen_au_maths_y6_multiply_divide as aum
adopt(aum)
if isinstance(getattr(aum, 'R', None), random.Random): aum.R = random.Random(806061)
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


def one_d43(r):
    d = r.randint(101, 499)
    q = r.randint(11, 99)
    rem = r.choice([0, 0, r.randint(1, d - 1)])
    n = d * q + rem
    if n > 9999 or n < 1000 or d % 10 == 0:
        raise AssertionError
    def fmt(qq, rr):
        return comma(qq) + (" r %d" % rr if rr else "")
    right = fmt(q, rem)
    wr = [fmt(q - 1, rem + d), fmt(q + 1, 0) if rem else fmt(q + 1, 0), fmt(q // 10, rem) if q >= 20 else fmt(q + 10, rem), fmt(q, rem + 1 if rem + 1 < d else rem - 1) if rem else fmt(q - 1, 0)]
    wr = [w for w in dict.fromkeys(wr) if w != right]
    big = d * (q // 10 * 10)
    e = "%d × %d = %s. %s − %s = %s, and %s ÷ %d = %d%s. Answer: <b>%s</b>." % (d, q // 10 * 10, comma(big), comma(n), comma(big), comma(n - big), comma(n - big), d, q % 10, (" r %d" % rem) if rem else "", right)
    if q // 10 * 10 == q:
        e = "%d × %d = %s%s. Answer: <b>%s</b>." % (d, q, comma(d * q), (", with %d left over" % rem) if rem else "", right)
    return mcq("%s ÷ %d = ?" % (comma(n), d), right, wr[:3], e)


def build():
    sets, R = build_sets([
        ("Short division", [("run", ukd.set_short, ("rnd", "seen", ukd.People), 20, nine)]),
        ("Divide by 2-digit numbers", [("run", ukd.set_long3, ("rnd", "seen", ukd.People), 10, nine), ("run", ukd.set_long4, ("rnd", "seen", ukd.People), 10, nine)]),
        ("Divide by 3-digit numbers", [("collect", uniq(one_d43), 20)]),
        ("Remainders", [("run", ukd.set_remainders, ("rnd", "seen", ukd.People), 10, nine), ("run", aum.set_remainders, ("rnd", "seen", aum.People), 10, nine)]),
        ("Division problems", [("run", ukd.set_story, ("rnd", ukd.People, "seen"), 10, nine), ("run", aum.set_divide, ("rnd", "seen", aum.People), 10, nine)]),
    ], 80606)
    finish(sets, R)
    body = lesson('<ul><li>To divide by a 3-digit number, estimate how many times it fits: 8 064 ÷ 252 → about 8 000 ÷ 250 = 32.</li><li>Use multiples of the divisor: 252 × 30 = 7 560, then 8 064 − 7 560 = 504 = 252 × 2.</li><li>The remainder must be smaller than the divisor.</li><li>Check: answer × divisor + remainder = the number you divided.</li></ul>',
        [example("8 064 ÷ 252", ["252 × 30 = 7 560", "8 064 − 7 560 = 504", "504 = 252 × 2"], "32")],
        [['Big remainder', 'If the remainder ≥ divisor, divide again.'], ['A missing 0', '3 618 ÷ 18 = 201, not 21.'], ['Ignoring the remainder', 'Decide what the story needs.']])
    faq = [('What does CAPS Grade 6 say about division?', 'Divide at least whole 4-digit by 3-digit numbers.'), ('How do I check a division?', 'Multiply the answer by the divisor and add the remainder.'), ('How do I start?', 'Estimate how many times the divisor fits.'), ('When do I round the answer up?', 'When the leftover items still need a place, like taxis for learners.')]
    make('division', 6, 'Numbers, Operations and Relationships', 'Grade 6: 1.1 Whole numbers',
         'Divide at least whole 4-digit by 3-digit numbers.',
         'Division of 4-Digit by 3-Digit Numbers', 'Division',
         'Free CAPS Grade 6 division worksheets: short division, long division by 2-digit and 3-digit numbers, remainders and problems. 100 questions with memos.',
         'Estimate how many times the divisor fits.', 'The remainder is smaller than the divisor.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
