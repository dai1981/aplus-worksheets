# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): Rounding Off to the Nearest 5, 10, 100 and 1 000 (Grade 5: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g5_rounding.py
Rounding off to the nearest 5 (own maker), to the nearest 10, 100 and 1 000 and to bigger places (UK Year 5
makers), and rounding problems with South African places (maker from the Grade 4 generator).
Wrong answers come from real mistakes: rounding 5 down, looking at the wrong digit, and rounding to the nearest 10
when asked for the nearest 5.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y5_rounding as ukr
adopt(ukr)
if isinstance(getattr(ukr, 'R', None), random.Random): ukr.R = random.Random(805020)
import gen_za_maths_g4_rounding as zr4
adopt(zr4)
if isinstance(getattr(zr4, 'R', None), random.Random): zr4.R = random.Random(805021)
za_common.GRADE = "grade-5"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


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


def one_r5(r):
    n = r.randint(11, 9999)
    if n % 5 == 0:
        raise AssertionError
    lo5, hi5 = n - n % 5, n - n % 5 + 5
    if n - lo5 == hi5 - n:
        raise AssertionError
    rt = lo5 if n - lo5 < hi5 - n else hi5
    ten = (n + 5) // 10 * 10
    wr = [hi5 if rt == lo5 else lo5, ten if ten not in (lo5, hi5) else rt + 10, rt - 10 if rt > 10 else rt + 15]
    return mcq("Round <b>%s</b> off to the nearest 5." % comma(n), comma(rt), [comma(x) for x in wr],
               "%s is between %s and %s. It is nearer to <b>%s</b>." % (comma(n), comma(lo5), comma(hi5), comma(rt)))


def build():
    sets, R = build_sets([
        ("Round to the nearest 5", [("collect", uniq(one_r5), 20)]),
        ("Round to 10, 100 and 1 000", [("run", ukr.set_small, ("rnd", ukr.Picker), 20, six)]),
        ("Round bigger numbers", [("run", ukr.set_tenk, ("rnd", ukr.Picker), 20, six)]),
        ("Mixed rounding", [("run", ukr.set_mixed, ("rnd", ukr.Picker), 15, six), ("run", ukr.set_hundredk, ("rnd", ukr.Picker), 5, six)]),
        ("Rounding problems", [("collect", zr4.uniq(zr4.one_rw), 20)]),
    ], 80502)
    finish(sets, R)
    body = lesson('<ul><li>To round off, find the two multiples the number lies between and choose the nearer one.</li><li>Nearest 5: 37 is between 35 and 40, nearer to 35.</li><li>Look at the digit to the right of the rounding place: 5 or more, round up; less than 5, round down.</li><li>Round off to estimate quickly.</li></ul>',
        [example("Round 48 362 to the nearest 1 000", ["between 48 000 and 49 000", "hundreds digit 3"], "48 000")],
        [['Rounding 5 down', '5 or more rounds up.'], ['The wrong digit', 'Look one place to the right.'], ['Nearest 10 for nearest 5', 'Multiples of 5 end in 0 or 5.']])
    faq = [('What does CAPS Grade 5 say about rounding?', 'Round off to the nearest 5, 10, 100 and 1 000.'), ('Why round to the nearest 5?', 'It is handy for money and time, like R5 coins and 5-minute marks.'), ('What is 2 497 to the nearest 100?', '2 500.'), ('Is rounding the same as estimating?', 'Rounding is one way to estimate.')]
    make('rounding-off-to-5-10-100-and-1000', 2, 'Numbers, Operations and Relationships', 'Grade 5: 1.1 Whole numbers',
         'Round off to the nearest 5, 10, 100 and 1 000.',
         'Rounding Off to the Nearest 5, 10, 100 and 1 000', 'Rounding Off',
         'Free CAPS Grade 5 rounding off worksheets: round to the nearest 5, 10, 100 and 1 000 and rounding problems. 100 questions with memos.',
         '5 or more: round up.', 'Multiples of 5 end in 0 or 5.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
