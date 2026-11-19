# -*- coding: utf-8 -*-
"""
Philippines Grade 4 Math (MATATAG): Decimals on the Number Line: Comparing, Ordering and Rounding (Grade 4: Number and Algebra)
  python3 tools/gen_ph_math_g4_compare_round_decimals.py
Decimals on the number line (US Grade 4 maker), comparing and ordering decimals to hundredths, rounding to the nearest
whole number and to the nearest tenth, and word problems with kilograms, meters and pesos (own makers).
Wrong answers come from real mistakes: thinking the decimal with more digits is bigger, comparing 0.8 and 0.75 as 8
and 75, and rounding down when the next digit is 5.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g4_decimals as usd
adopt(usd)
if hasattr(usd, 'R'): usd.R = random.Random(704220)
ph_common.GRADE = "grade-4"

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


def d2(h):
    """hundredths (int) -> decimal string: 347 -> 3.47, 30 -> 0.3, 5 -> 0.05"""
    w, f = divmod(h, 100)
    s = "%d.%02d" % (w, f)
    s = s.rstrip("0").rstrip(".") if f % 10 == 0 else s
    return comma(int(s)) if "." not in s else comma(w) + s[s.index("."):]


def d2k(h):
    """keep two places: 3.40"""
    w, f = divmod(h, 100)
    return "%s.%02d" % (comma(w), f)


ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen",
        "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def say(n):
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else "")
    return ONES[n // 100] + " hundred" + (" " + say(n % 100) if n % 100 else "")


def pair_vals(r):
    for _ in range(50):
        w = r.choice([0, 0, r.randint(1, 20)])
        a = w * 100 + r.randint(1, 99)
        kind = r.choice(["len", "close", "near"])
        if kind == "len":
            b = w * 100 + r.randint(1, 9) * 10
        elif kind == "close":
            b = a + r.choice([-9, -1, 1, 9, 10, -10])
        else:
            b = (a // 10) * 10 + r.choice([0, 10]) if a % 10 else a + r.randint(1, 9)
        if b > 0 and a != b and abs(a - b) < 100:
            return a, b
    raise AssertionError


def one_cmp(r):
    a, b = pair_vals(r)
    A, B = d2(a), d2(b)
    true = "%s %s %s" % (A, "&lt;" if a < b else "&gt;", B)
    opts = ["%s &lt; %s" % (A, B), "%s &gt; %s" % (A, B), "%s = %s" % (A, B), "%s %s %s" % (B, "&gt;" if a < b else "&lt;", A)]
    return mcq("Compare <b>%s</b> and <b>%s</b>. Which statement is true?" % (A, B), true, [o for o in opts if o != true],
               "Write both with hundredths: %s and %s. Compare place by place: <b>%s</b>." % (d2k(a), d2k(b), true))


def one_ord(r):
    w = r.choice([0, r.randint(1, 9)])
    vals = set()
    while len(vals) < 4:
        x = w * 100 + r.choice([r.randint(1, 9) * 10, r.randint(1, 99)])
        vals.add(x)
    vals = list(vals)
    up = r.random() < 0.5
    srt = sorted(vals, reverse=not up)
    show = lambda v: ", ".join(d2(x) for x in v)
    right = show(srt)
    by_len = sorted(vals, key=lambda x: (len(d2(x)), x), reverse=not up)
    by_digits = sorted(vals, key=lambda x: int(d2(x).split(".")[1]) if "." in d2(x) else 0, reverse=not up)
    wr = [show(by_len), show(by_digits), show(list(reversed(srt))), show([srt[1], srt[0]] + srt[2:])]
    r.shuffle(vals)
    return mcq("Order from %s: %s" % ("least to greatest" if up else "greatest to least", ", ".join(d2(x) for x in vals)), right, [x for x in wr if x != right],
               "Write them all with hundredths: %s. Then compare: <b>%s</b>." % (", ".join(d2k(x) for x in vals), right))


def one_round(r):
    to = r.choice(["whole", "tenth"])
    w = r.randint(0, 30)
    if to == "whole":
        t = r.randint(1, 9)
        h = w * 100 + t * 10 + r.choice([0, r.randint(1, 9)])
        right = w + (1 if h % 100 >= 50 else 0)
        wr = [w if right != w else w + 1, h // 10, w + 2 if right == w + 1 else w - 1 if w else w + 2]
        e = "Look at the tenths digit, %d. %s, so %s rounds to <b>%s</b>." % (t, "5 or more: round up" if t >= 5 else "Less than 5: round down", d2(h), comma(right))
        return mcq("Round <b>%s</b> to the nearest whole number." % d2(h), comma(right), [comma(x) for x in wr if x >= 0], e)
    f = r.randint(1, 99)
    if f % 10 == 0:
        raise AssertionError
    h = w * 100 + f
    up = f % 10 >= 5
    rt = (h // 10 + (1 if up else 0)) * 10
    right = d2(rt) if rt % 100 else d2(rt) + ".0"
    wr = [d2((h // 10 + (0 if up else 1)) * 10), comma(round(h / 100)), d2(h // 10 + (1 if up else 0))]
    wr = [x if "." in x or x == comma(round(h / 100)) else x + ".0" for x in wr]
    e = "Look at the hundredths digit, %d. %s, so %s rounds to <b>%s</b>." % (f % 10, "5 or more: round up" if up else "Less than 5: round down", d2(h), right)
    return mcq("Round <b>%s</b> to the nearest tenth." % d2(h), right, wr, e)


CTX = [("%s and %s run 100 meters. %s's time is %s seconds and %s's time is %s seconds. Who is faster?", "time"),
       ("%s's watermelon weighs %s kg. %s's watermelon weighs %s kg. Whose watermelon is heavier?", "mass"),
       ("In the long jump, %s jumps %s m and %s jumps %s m. Who jumps farther?", "jump")]


def one_word(r):
    p = Kid(r)
    a, b = p.next(), p.next()
    kind = r.choice(["cmp", "cmp", "round"])
    if kind == "round":
        h = r.randint(1001, 9999)
        if h % 10 == 0 or h % 100 // 10 == 9:
            raise AssertionError
        item = r.choice(["a bag of rice", "a box of mangoes", "a sack of onions"])
        q = "%s weighs %s kg. What is its mass to the nearest kilogram?" % (item.capitalize(), d2(h))
        right = round(h / 100 + 1e-9) if h % 100 != 50 else h // 100 + 1
        return mcq(q, "%s kg" % comma(right), ["%s kg" % comma(x) for x in (h // 100 if right != h // 100 else right + 1, h // 10, right - 1 if right - 1 != h // 100 else right + 2)],
                   "The tenths digit is %d, so round %s. %s kg ≈ <b>%s kg</b>." % (h // 10 % 10, "up" if h % 100 >= 50 else "down", d2(h), comma(right)))
    t, what = r.choice(CTX)
    if what == "time":
        x, y = 1200 + r.randint(0, 600), 0
        y = x + r.choice([-1, 1]) * r.choice([3, 7, 10, 20, 30])
        if x // 10 == y // 10 or x % 10 == 0 or y % 10 == 0:
            pass
        q = t % (a["n"], b["n"], a["n"], d2(x), b["n"], d2(y))
        right = a["n"] if x < y else b["n"]
        return mcq(q, right, [b["n"] if right == a["n"] else a["n"], "They are equally fast", "You can’t tell"],
                   "The faster runner has the <b>smaller</b> time. %s &lt; %s, so <b>%s</b> is faster." % (d2(min(x, y)), d2(max(x, y)), right))
    x, y = pair_vals(r)
    x, y = x + (200 if what == "mass" else 100), y + (200 if what == "mass" else 100)
    q = t % (a["n"], d2(x), b["n"], d2(y)) if what == "mass" else t % (a["n"], d2(x), b["n"], d2(y))
    right = a["n"] if x > y else b["n"]
    return mcq(q, right, [b["n"] if right == a["n"] else a["n"], "They are the same", "You can’t tell"],
               "Write both with hundredths: %s and %s. %s is greater, so <b>%s</b>." % (d2k(x), d2k(y), d2(max(x, y)), right))


def build():
    sets, R = build_sets([
        ("Decimals on the number line", [("run", usd.set_lines, ("rnd",), 20)]),
        ("Compare decimals", [("collect", uniq(one_cmp), 20)]),
        ("Order decimals", [("collect", uniq(one_ord), 20)]),
        ("Round decimals", [("collect", uniq(one_round), 20)]),
        ("Decimal word problems", [("collect", uniq(one_word), 20)]),
    ], 70422)
    finish(sets, R)
    body = lesson('<ul><li>On a number line from 0 to 1 split into 10 equal parts, each part is 0.1.</li><li>To compare decimals, line up the decimal points. Compare the ones, then the tenths, then the hundredths. Write 0.8 as 0.80 to compare with 0.75.</li><li>A decimal with more digits is <b>not</b> always bigger: 0.8 &gt; 0.75.</li><li>To round to the nearest whole number, look at the tenths digit. To round to the nearest tenth, look at the hundredths digit. 5 or more: round up. Less than 5: round down.</li></ul>',
        [example("Compare 0.8 and 0.75", ["0.80 and 0.75", "8 tenths &gt; 7 tenths"], "0.8 &gt; 0.75"), example("Round 4.65 to the nearest tenth", ["hundredths digit 5"], "4.7")],
        [['More digits means bigger', '0.75 &lt; 0.8.'], ['Comparing 8 and 75', 'Write 0.8 as 0.80 first.'], ['Rounding 5 down', '5 or more rounds up.']])
    faq = [('What does MATATAG Math 4 ask about comparing decimals?', 'Plot decimal numbers with tenth decimal parts on the number line, compare and order decimal numbers with decimal parts to hundredths, and round decimal numbers to the nearest whole number and to the nearest tenth.'), ('Is 0.50 bigger than 0.5?', 'No. They are equal.'), ('How do I round 3.96 to the nearest tenth?', 'The hundredths digit is 6, so round up: 3.96 ≈ 4.0.'), ('Why round decimals?', 'To estimate, like saying a 2.45-kg bag is about 2 kg.')]
    make('comparing-ordering-and-rounding-decimals', 22, 'Number and Algebra', 'Grade 4: Number and Algebra',
         'Plot decimal numbers with tenth decimal part on the number line; compare and order decimal numbers with decimal parts to hundredths; round decimal numbers to the nearest whole number and to the nearest tenth.',
         'Decimals on the Number Line: Comparing, Ordering and Rounding', 'Comparing and Rounding Decimals',
         'Free Grade 4 worksheets on comparing, ordering and rounding decimals for the DepEd MATATAG curriculum: number lines, comparing, ordering, rounding and word problems. 100 questions with answers.',
         'Line up the decimal points, then compare place by place.', 'Round: 5 or more, round up.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
