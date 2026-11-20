# -*- coding: utf-8 -*-
"""
South Africa Grade 4 Maths (CAPS): Rounding Off to the Nearest 10, 100 and 1 000 (Grade 4: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g4_rounding.py
Rounding off to the nearest 10, 100 and 1 000 with number lines, mixed rounding and problems (UK Year 4 makers with
South African names and numbers).
Wrong answers come from real mistakes: rounding 5 down, looking at the wrong digit, and changing the digits after the
rounding place to the wrong number.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y4_rounding as ukr
adopt(ukr)
if hasattr(ukr, 'R'): ukr.R = random.Random(804020)
import gen_cabc_math_g4_numbers as cbn
adopt(cbn)
if hasattr(cbn, 'R'): cbn.R = random.Random(804021)
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


RW = [("A stadium in Durban had %s fans at a soccer match.", "fans"), ("The Gautrain carried %s passengers on Monday morning.", "passengers"),
      ("A school in Soweto collected %s cans for recycling.", "cans"), ("A farmer in the Free State harvested %s kg of mielies.", "kg"),
      ("Table Mountain is %s m high.", "m"), ("A family drove %s km from Johannesburg to Cape Town and back.", "km"),
      ("A library has %s books.", "books"), ("Kruger National Park had %s visitors in one week.", "visitors")]


def one_rw(r):
    t, u = r.choice(RW)
    n = r.randint(1001, 9999) if u not in ("m",) else 1085
    to = r.choice([10, 100, 1000])
    if n % to == 0:
        raise AssertionError
    if u == "m" and to == 10:
        raise AssertionError
    rt = (n + to // 2) // to * to
    other = rt - to if rt > n else rt + to
    unit_ = (" " + u) if u in ("kg", "m", "km") else ""
    q = (t % comma(n)) + " Round the number to the nearest %s." % comma(to)
    wr = [other, n // to * to * 10 if n // to * to * 10 <= 99999 else rt + 2 * to, (n + to) // to * to if (n + to) // to * to not in (rt, other) else rt + 2 * to]
    return mcq(q, comma(rt) + unit_, [comma(x) + unit_ for x in wr if x != rt],
               "%s is between %s and %s. Look at the digit to the right of the %s place: %s, so round %s. <b>%s%s</b>." % (comma(n), comma(n // to * to), comma(n // to * to + to), {10: "tens", 100: "hundreds", 1000: "thousands"}[to], str(n)[-len(str(to)) + 1], "up" if rt > n else "down", comma(rt), unit_))


def build():
    sets, R = build_sets([
        ("Round to the nearest 10", [("run", ukr.set_ten, ("rnd", ukr.Picker), 20, le10000)]),
        ("Round to the nearest 100", [("run", ukr.set_hundred, ("rnd", ukr.Picker), 20, le10000)]),
        ("Round to the nearest 1 000", [("run", ukr.set_thousand, ("rnd", ukr.Picker), 20, le10000)]),
        ("Mixed rounding", [("run", ukr.set_mixed, ("rnd", ukr.Picker), 12, le10000), ("run", cbn.set_round, ("rnd",), 8, le10000)]),
        ("Rounding problems", [("run", ukr.set_words, ("rnd", ukr.People), 5, le10000), ("collect", uniq(one_rw), 15)]),
    ], 80402)
    finish(sets, R)
    body = lesson('<ul><li>To round off, find the two multiples the number is between, then see which one is nearer.</li><li>Look at the digit just to the right of the place you round to. 5 or more: round up. Less than 5: round down.</li><li>4 536 to the nearest 10 is 4 540; to the nearest 100 is 4 500; to the nearest 1 000 is 5 000.</li><li>We round off to estimate answers and check if an answer makes sense.</li></ul>',
        [example("Round 3 650 to the nearest 100", ["between 3 600 and 3 700", "tens digit 5: round up"], "3 700")],
        [['Rounding 5 down', '5 or more rounds up.'], ['The wrong digit', 'Look one place to the right.'], ['Wrong zeros', 'After rounding, the digits to the right become 0.']])
    faq = [('What does CAPS Grade 4 say about rounding?', 'Round off to the nearest 10, 100 and 1 000.'), ('Why round off?', 'To estimate quickly and check answers.'), ('What is 9 950 rounded to the nearest 100?', '10 000.'), ('Is rounding the same as rounding down?', 'No. You round to the nearest multiple.')]
    make('rounding-off-to-10-100-and-1000', 2, 'Numbers, Operations and Relationships', 'Grade 4: 1.1 Whole numbers',
         'Round off to the nearest 10, 100, 1 000.',
         'Rounding Off to the Nearest 10, 100 and 1 000', 'Rounding Off',
         'Free CAPS Grade 4 rounding off worksheets: round to the nearest 10, 100 and 1 000 with number lines and word problems. 100 questions with memos.',
         '5 or more: round up. Less than 5: round down.', 'Look at the digit to the right of the rounding place.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
