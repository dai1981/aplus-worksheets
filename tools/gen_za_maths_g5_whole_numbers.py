# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): Whole Numbers to 6 Digits: Place Value, Comparing and Ordering (Grade 5: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g5_whole_numbers.py
Place value of 6-digit numbers, reading and writing numbers, expanded notation, counting in intervals, and comparing
and ordering (UK Year 5 and BC Grade 5 makers), with South African number writing (245 306).
Wrong answers come from real mistakes: mixing up the value and the digit, leaving out a 0 for an empty place, and
comparing the last digits first.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y5_place_value as ukp
adopt(ukp)
if isinstance(getattr(ukp, 'R', None), random.Random): ukp.R = random.Random(805010)
import gen_cabc_math_g5_numbers as cbn
adopt(cbn)
if isinstance(getattr(cbn, 'R', None), random.Random): cbn.R = random.Random(805011)
import gen_za_maths_g4_whole_numbers as zw4
adopt(zw4)
if isinstance(getattr(zw4, 'R', None), random.Random): zw4.R = random.Random(805012)
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


def one_expand(r):
    ds = [r.randint(1, 9)] + [r.choice([0, 0] + list(range(1, 10))) for _ in range(5)]
    n = int("".join(map(str, ds)))
    parts = [d * 10 ** (5 - i) for i, d in enumerate(ds) if d]
    if len(parts) < 3:
        raise AssertionError
    if r.random() < 0.5:
        q = "Which number is <b>%s</b>?" % " + ".join(comma(x) for x in parts)
        nz = int("".join(str(d) for d in ds if d))
        i = r.choice([i for i in range(1, 6) if ds[i] != ds[i - 1]] or [1])
        sw = ds[:]
        sw[i - 1], sw[i] = sw[i], sw[i - 1]
        wr = [nz, n // 10 if n // 10 >= 1000 else n * 10, int("".join(map(str, sw)))]
        wr = [x for x in wr if x != n]
        wr = [x for x in wr if x != n]
        return mcq(q, comma(n), [comma(x) for x in wr] + [comma(n + 1000)], "Put each digit in its place: <b>%s</b>." % comma(n))
    q = "Write <b>%s</b> in expanded notation." % comma(n)
    right = " + ".join(comma(x) for x in parts)
    wr1 = " + ".join(str(d) for d in ds if d)
    wr2 = " + ".join(comma(x // 10) for x in parts)
    wr3 = " + ".join(comma(x * 10) for x in parts)
    return mcq(q, right, [wr1, wr2, wr3], "Each digit is worth its place value: <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Place value", [("run", ukp.set_value, ("rnd", "seen"), 12, six), ("run", cbn.set_value, (), 8, six)]),
        ("Read and write numbers", [("run", cbn.set_read, (), 9, six), ("run", ukp.set_words, ("rnd", ukp.People), 11, six)]),
        ("Expanded notation", [("run", cbn.set_expand, (), 12, six), ("collect", uniq(one_expand), 8)]),
        ("Count in intervals", [("run", ukp.set_count, ("rnd",), 15, six), ("collect", zw4.uniq(zw4.one_count), 5)]),
        ("Compare and order", [("run", ukp.set_compare, ("rnd", "seen"), 10, six), ("run", cbn.set_compare, (), 10, six)]),
    ], 80501)
    finish(sets, R)
    body = lesson('<ul><li>A 6-digit number has hundred thousands, ten thousands, thousands, hundreds, tens and units: 245 306.</li><li>In 245 306 the 4 is worth 40 000, and the 0 shows that there are no tens.</li><li>Expanded notation: 245 306 = 200 000 + 40 000 + 5 000 + 300 + 6.</li><li>To compare, start from the biggest place.</li></ul>',
        [example("Three hundred and eight thousand and fifty", ["308 thousands", "0 hundreds, 5 tens, 0 units"], "308 050")],
        [['Value or digit?', 'The digit 4 in 245 306 has a value of 40 000.'], ['A missing 0', 'Write 0 for an empty place.'], ['Last digits first', 'Compare from the left.']])
    faq = [('What does CAPS Grade 5 say about whole numbers?', 'Order, compare and represent numbers to at least 6-digit numbers, recognise the place value of digits in whole numbers to at least 6 digits, and count forwards and backwards in whole number intervals up to at least 10 000.'), ('How do South Africans write big numbers?', 'With a space between groups of three digits: 245 306.'), ('What is the biggest 6-digit number?', '999 999.'), ('What comes after 99 999?', '100 000.')]
    make('whole-numbers-to-6-digits', 1, 'Numbers, Operations and Relationships', 'Grade 5: 1.1 Whole numbers',
         'Count forwards and backwards in whole number intervals up to at least 10 000; order, compare and represent numbers to at least 6-digit numbers; recognise the place value of digits in whole numbers to at least 6-digit numbers.',
         'Whole Numbers to 6 Digits: Place Value, Comparing and Ordering', 'Whole Numbers to 6 Digits',
         'Free CAPS Grade 5 whole numbers worksheets: 6-digit place value, reading and writing numbers, expanded notation, counting and comparing. 100 questions with memos.',
         'Hundred thousands, ten thousands, thousands, hundreds, tens, units.', 'Compare from the biggest place.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
