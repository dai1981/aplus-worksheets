# -*- coding: utf-8 -*-
"""
South Africa Grade 4 Maths (CAPS): Whole Numbers to 10 000: Counting, Place Value, Comparing and Ordering (Grade 4: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g4_whole_numbers.py
Counting forwards and backwards in 2s, 3s, 5s, 10s, 25s, 50s and 100s (own maker), place value and expanded
notation of 4-digit numbers (UK Year 4 makers), comparing and ordering (Ontario Grade 4 maker and own maker),
and odd and even numbers (Australia Year 4 maker), with South African number writing (10 000).
Wrong answers come from real mistakes: counting on by 1 instead of the jump, mixing up the value and the digit,
and comparing the last digits first.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y4_place_value as ukp
adopt(ukp)
if hasattr(ukp, 'R'): ukp.R = random.Random(804010)
import gen_caon_math_g4_numbers as can
adopt(can)
if hasattr(can, 'R'): can.R = random.Random(804011)
import gen_au_maths_y4_odd_even as auo
adopt(auo)
if hasattr(auo, 'R'): auo.R = random.Random(804012)
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


def one_count(r):
    st = r.choice([2, 3, 5, 10, 25, 50, 100])
    up = r.random() < 0.6
    a = st * r.randint(2, 9900 // st)
    seq = [a + (st if up else -st) * i for i in range(4)]
    if min(seq) < 0 or max(seq) > 10000:
        raise AssertionError
    k = r.choice([3, 3, 1, 2])
    ans = seq[k]
    show = ", ".join("☐" if i == k else comma(x) for i, x in enumerate(seq))
    return mcq("Count %s in %ds. What number goes in the box? <b>%s</b>" % ("forwards" if up else "backwards", st, show), comma(ans),
               [comma(ans + (st if up else -st)), comma(ans + (1 if up else -1)), comma(ans - (st if up else -st) * 2 if k else ans + 10)],
               "Each jump is %s %d. The missing number is <b>%s</b>." % ("+" if up else "−", st, comma(ans)))


def one_order(r):
    vs = r.sample(range(1000, 10000), 4)
    up = r.random() < 0.5
    s = sorted(vs, reverse=not up)
    show = lambda v: ", ".join(comma(x) for x in v)
    first = sorted(vs, key=lambda x: (str(x)[::-1]), reverse=not up)
    return mcq("Order from %s: <b>%s</b>" % ("smallest to biggest" if up else "biggest to smallest", show(vs)), show(s),
               [show(first) if first != s else show([s[1], s[0]] + s[2:]), show(list(reversed(s))), show([s[0], s[2], s[1], s[3]])],
               "Compare the thousands, then the hundreds, then the tens: <b>%s</b>." % show(s))


def build():
    sets, R = build_sets([
        ("Count forwards and backwards", [("collect", uniq(one_count), 20)]),
        ("Place value", [("run", ukp.set_value, ("rnd", "seen"), 20, le10000)]),
        ("Expanded notation", [("run", ukp.set_partition, ("rnd", "seen"), 20, le10000)]),
        ("Compare and order", [("run", can.set_compare, ("rnd",), 10, le10000), ("collect", uniq(one_order), 10)]),
        ("Odd and even numbers", [("run", auo.set_odd_even, ("rnd",), 10, le10000), ("run", auo.set_rules, ("rnd",), 10, le10000)]),
    ], 80401)
    finish(sets, R)
    body = lesson('<ul><li>A 4-digit number has <b>thousands, hundreds, tens and units</b>. In 4 536 the 4 is worth 4 000.</li><li>Expanded notation: 4 536 = 4 000 + 500 + 30 + 6.</li><li>To compare, start with the thousands. If they are the same, compare the hundreds, then the tens, then the units.</li><li>Even numbers end in 0, 2, 4, 6 or 8. Odd numbers end in 1, 3, 5, 7 or 9.</li><li>When you count in 25s, 50s or 100s, add the same jump each time.</li></ul>',
        [example("7 048", ["7 thousands, 0 hundreds, 4 tens, 8 units"], "7 000 + 40 + 8"), example("Order 3 905, 3 950, 3 059", ["thousands: all 3", "hundreds: 9, 9, 0"], "3 059, 3 905, 3 950")],
        [['Counting on by 1', 'Add the jump (25, 50, 100) each time.'], ['Value or digit?', 'The digit 5 in 4 536 has a value of 500.'], ['Comparing the units first', 'Start with the biggest place.']])
    faq = [('What does CAPS Grade 4 say about whole numbers?', 'Count forwards and backwards in 2s, 3s, 5s, 10s, 25s, 50s and 100s to at least 10 000, order, compare and represent numbers to at least 4-digit numbers, and recognise the place value of digits in whole numbers to at least 4-digit numbers.'), ('Why do we write 10 000 with a space?', 'South Africa uses a space, not a comma, between groups of three digits.'), ('Is 0 even?', 'Yes.'), ('What comes after 9 999?', '10 000.')]
    make('whole-numbers-to-10000', 1, 'Numbers, Operations and Relationships', 'Grade 4: 1.1 Whole numbers',
         'Count forwards and backwards in 2s, 3s, 5s, 10s, 25s, 50s, 100s between 0 and at least 10 000; order, compare and represent numbers to at least 4-digit numbers; represent odd and even numbers to at least 1 000; recognise the place value of digits in whole numbers to at least 4-digit numbers.',
         'Whole Numbers to 10 000: Counting, Place Value, Comparing and Ordering', 'Whole Numbers to 10 000',
         'Free CAPS Grade 4 maths worksheets on whole numbers to 10 000: counting in 25s, 50s and 100s, place value, expanded notation, comparing, ordering and odd and even numbers. 100 questions with memos.',
         'Thousands, hundreds, tens, units.', 'Compare from the biggest place first.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
