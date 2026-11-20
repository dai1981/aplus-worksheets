# -*- coding: utf-8 -*-
"""
South Africa Grade 4 Maths (CAPS): Calculation Techniques: Estimating, Compensating, Doubling and Halving, Number Lines and Inverse Operations (Grade 4: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g4_calculation_techniques.py
Estimating sums and differences, rounding off and compensating, doubling and halving (own makers), breaking down
numbers and number lines, and inverse operations (Australia Year 3 and Year 4 makers).
Wrong answers come from real mistakes: compensating in the wrong direction, doubling only part of a number, and
undoing with the same operation.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y4_rounding_estimation as aur
adopt(aur)
if hasattr(aur, 'R'): aur.R = random.Random(804040)
import gen_au_maths_y3_mental as aum
adopt(aum)
if hasattr(aum, 'R'): aum.R = random.Random(804041)
za_common.GRADE = "grade-4"

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


def one_comp(r):
    a = r.randint(120, 4800)
    b = r.choice([x for x in range(19, 999) if x % 100 in (97, 98, 99) or x % 10 in (8, 9)])
    if r.random() < 0.5:
        rb = (b + 5) // 10 * 10 if b % 100 < 90 else (b + 50) // 100 * 100
        d = rb - b
        q = "Use rounding and compensating: <b>%s + %d</b>" % (comma(a), b)
        right = a + b
        e = "%d is close to %d. %s + %d = %s, then take away %d: <b>%s</b>." % (b, rb, comma(a), rb, comma(a + rb), d, comma(right))
        wr = [a + rb, a + rb + d, a + b - 10]
    else:
        if a <= b:
            raise AssertionError
        rb = (b + 5) // 10 * 10 if b % 100 < 90 else (b + 50) // 100 * 100
        d = rb - b
        q = "Use rounding and compensating: <b>%s − %d</b>" % (comma(a), b)
        right = a - b
        e = "%d is close to %d. %s − %d = %s, then add back %d: <b>%s</b>." % (b, rb, comma(a), rb, comma(a - rb), d, comma(right))
        wr = [a - rb, a - rb - d, a - b + 10]
    return mcq(q, comma(right), [comma(x) for x in wr if x != right and x >= 0], e)


def one_dh(r):
    kind = r.choice(["double", "half", "dh"])
    if kind == "double":
        n = r.randint(26, 2499)
        return mcq("Double <b>%s</b>." % comma(n), comma(2 * n), [comma(x) for x in (n + 2, 2 * n + 10, n // 2 if n % 2 == 0 else 2 * n - 10)],
                   "Double the parts: %s. <b>%s</b>." % (" + ".join(comma(2 * p) for p in (n // 100 * 100, n % 100) if p), comma(2 * n)))
    if kind == "half":
        n = 2 * r.randint(26, 4999)
        return mcq("Halve <b>%s</b>." % comma(n), comma(n // 2), [comma(x) for x in (n * 2, n // 2 + 10, n - 2)],
                   "Halve the parts: %s. <b>%s</b>." % (" + ".join(comma(p // 2) for p in (n // 100 * 100, n % 100) if p), comma(n // 2)))
    a = r.choice([5, 25, 50])
    b = r.choice([x for x in range(12, 99, 2)])
    return mcq("Use doubling and halving: <b>%d × %d</b>" % (a, b), comma(a * b), [comma(x) for x in (a * b // 2, a * b + a, a + b)],
               "Double %d to get %d and halve %d to get %d: %d × %d = <b>%s</b>." % (a, 2 * a, b, b // 2, 2 * a, b // 2, comma(a * b)))


def build():
    sets, R = build_sets([
        ("Estimate first", [("run", aur.set_sums, (), 20, le100k)]),
        ("Rounding off and compensating", [("collect", uniq(one_comp), 20)]),
        ("Doubling and halving", [("collect", uniq(one_dh), 20)]),
        ("Breaking down numbers", [("run", aum.set_strategies, (), 20)]),
        ("Inverse operations", [("run", aum.set_inverse, (), 20)]),
    ], 80404)
    finish(sets, R)
    body = lesson('<ul><li><b>Estimate</b> by rounding off first: 3 897 + 2 104 is about 4 000 + 2 000 = 6 000.</li><li><b>Compensate</b>: 2 456 + 198 = 2 456 + 200 − 2 = 2 654.</li><li><b>Double and halve</b>: 25 × 48 = 50 × 24 = 1 200.</li><li><b>Break down</b> numbers: 347 + 225 = 300 + 200 + 40 + 20 + 7 + 5.</li><li>Addition and subtraction are <b>inverse operations</b>; so are multiplication and division.</li></ul>',
        [example("5 342 − 299", ["5 342 − 300 = 5 042", "add back 1"], "5 043")],
        [['Compensating the wrong way', 'You took away 1 too many, so add 1 back.'], ['Doubling only part', 'Double every part of the number.'], ['Same operation to undo', 'Undo + with −, × with ÷.']])
    faq = [('What does CAPS Grade 4 say about calculation techniques?', 'Use a range of techniques: estimation, building up and breaking down numbers, rounding off and compensating, doubling and halving, using a number line, and using addition and subtraction (and multiplication and division) as inverse operations.'), ('Why estimate?', 'To judge if an answer is reasonable.'), ('Which technique is best?', 'The one that makes the numbers easiest for you.'), ('Is mental maths part of CAPS?', 'Yes: 10 minutes of mental maths every day.')]
    make('calculation-techniques', 4, 'Numbers, Operations and Relationships', 'Grade 4: 1.1 Whole numbers',
         'Use a range of techniques to perform and check written and mental calculations of whole numbers, including estimation, building up and breaking down numbers, rounding off and compensating, doubling and halving, using a number line, and using addition and subtraction as well as multiplication and division as inverse operations.',
         'Calculation Techniques: Estimating, Compensating, Doubling and Halving, Number Lines and Inverse Operations', 'Calculation Techniques',
         'Free CAPS Grade 4 mental maths worksheets on calculation techniques: estimation, rounding off and compensating, doubling and halving, breaking down numbers and inverse operations. 100 questions with memos.',
         'Round off, calculate, then compensate.', 'Check with the inverse operation.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
