# -*- coding: utf-8 -*-
"""
Texas Grade 4 Math: Comparing, Ordering and Rounding Whole Numbers (TEKS 4.2C, 4.2D)
  python3 tools/gen_ustx_math_g4_compare_round.py
Comparing and ordering whole numbers to 1,000,000,000 with >, < and =, rounding to any place through the hundred
thousands (the US Grade 4 makers with Texas names), and real-world rounding.
Wrong answers come from real mistakes: comparing the last digits, counting digits wrongly when numbers have
different lengths, rounding to the wrong place, and rounding 5 down.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g4_place_value as usp
adopt(usp)
tx_common.GRADE = "grade-4"

ONES = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen",
        "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def w3(m):
    out = []
    if m >= 100:
        out.append(ONES[m // 100] + " hundred")
        m %= 100
    if m >= 20:
        out.append(TENS[m // 10] + ("-" + ONES[m % 10] if m % 10 else ""))
    elif m:
        out.append(ONES[m])
    return " ".join(out)


def bigwords(n):
    parts = []
    for v, name in ((10 ** 9, "billion"), (10 ** 6, "million"), (10 ** 3, "thousand")):
        if n >= v:
            parts.append(w3(n // v) + " " + name)
            n %= v
    if n:
        parts.append(w3(n))
    return ", ".join(parts)


PLACE = ["ones", "tens", "hundreds", "thousands", "ten thousands", "hundred thousands", "millions", "ten millions", "hundred millions", "billions"]


def rbig(r, lo=6, hi=10):
    d = r.randint(lo, hi)
    s = [str(r.randint(1, 9))] + [str(r.choice([0, r.randint(1, 9), r.randint(1, 9)])) for _ in range(d - 1)]
    return int("".join(s))


def rnd_to(n, p):
    return (n + p // 2) // p * p


def one_big_cmp(r):
    n = rbig(r, 7, 10)
    s = list(str(n))
    i = r.randrange(1, len(s))
    s[i] = str((int(s[i]) + r.randint(1, 8)) % 10)
    m = int("".join(s))
    if m == n:
        return None
    sym = "&gt;" if n > m else "&lt;"
    return mcq("Which symbol makes this true? %s ☐ %s" % (comma(n), comma(m)), sym, ["&lt;" if sym == "&gt;" else "&gt;", "=", "+"],
               "Same digits until the %s place. Compare there: %s %s %s." % (PLACE[len(s) - 1 - i], comma(n), sym, comma(m)))


def one_round_big(r):
    p = r.choice([1000, 10000, 100000])
    n = r.randint(100000, 9999999)
    if n % p == p // 2 or n % p == 0:
        return None
    right = rnd_to(n, p)
    lo = n // p * p
    return mcq("Round %s to the nearest %s." % (comma(n), {1000: "thousand", 10000: "ten thousand", 100000: "hundred thousand"}[p]), comma(right),
               [comma(lo if right != lo else lo + p), comma(rnd_to(n, p // 10)), comma(rnd_to(n, p * 10)) if rnd_to(n, p * 10) != right else comma(right + p), comma(right + n % p)],
               "Look at the digit to the right of that place. %s, so round %s: <b>%s</b>." % ("5 or more" if n % p >= p // 2 else "Less than 5", "up" if n % p >= p // 2 else "down", comma(right)))


def one_real(r):
    k = Kid(r).next()
    kind = r.choice(["pop", "miles", "cmp"])
    if kind == "pop":
        n = r.randint(1100000, 9800000)
        p = r.choice([100000, 10000])
        right = rnd_to(n, p)
        if n % p == p // 2:
            return None
        return mcq("About %s people live in a large Texas city area. A news report rounds the number to the nearest %s. What number does it say?" % (comma(n), "hundred thousand" if p == 100000 else "ten thousand"), comma(right),
                   [comma(n // p * p if right != n // p * p else right + p), comma(rnd_to(n, 1000000)) if rnd_to(n, 1000000) != right else comma(right - p), comma(rnd_to(n, p // 10))],
                   "Round %s to the nearest %s: <b>%s</b>." % (comma(n), "hundred thousand" if p == 100000 else "ten thousand", comma(right)))
    if kind == "miles":
        n = r.randint(1001, 9999)
        right = rnd_to(n, 100)
        if n % 100 == 50:
            return None
        return mcq("A truck driver drove %s miles last month. About how many miles is that, to the nearest hundred?" % comma(n), comma(right), [comma(rnd_to(n, 1000)) if rnd_to(n, 1000) != right else comma(right + 100), comma(rnd_to(n, 10)), comma(n // 100 * 100 if right != n // 100 * 100 else right + 100)],
                   "Look at the tens digit to round to hundreds: <b>%s</b>." % comma(right))
    a = rbig(r, 6, 9)
    b = a + r.choice([-1, 1]) * 10 ** r.randint(2, len(str(a)) - 2)
    teams = r.sample(["Houston", "Dallas", "San Antonio", "Austin"], 2)
    win = teams[0] if a > b else teams[1]
    return mcq("Last year %s fans went to games in %s and %s fans went to games in %s. Which city had more fans?" % (comma(a), teams[0], comma(b), teams[1]), win,
               [teams[1] if win == teams[0] else teams[0], "They had the same number", "We cannot tell"], "Compare from the left: <b>%s</b> had more." % win)


def build():
    sets, R = build_sets([
        ("Compare numbers to a billion", [("collect", one_big_cmp, 20)]),
        ("Compare and order multi-digit numbers", [("run", usp.set_compare, ("rnd", "seen", usp.People), 20)]),
        ("Round to the nearest thousand, ten thousand and hundred thousand", [("collect", one_round_big, 20)]),
        ("Round to any place", [("run", usp.set_round, ("rnd", "seen", usp.People), 20)]),
        ("Real-world comparing and rounding", [("collect", one_real, 20)]),
    ], 64002)
    finish(sets, R)
    body = lesson('<ul><li>A number with more digits is greater. With the same number of digits, compare from the <b>left</b>; the first place where the digits differ decides.</li><li>&gt; means greater than, &lt; means less than.</li><li>To <b>round</b>, look at the digit to the right of the rounding place: 5 or more rounds up, 4 or less rounds down. All places to the right become 0.</li></ul>',
        [example("Compare 4,302,118 and 4,320,118.", ["Same millions and hundred thousands.", "Ten thousands: 0 &lt; 2."], "4,302,118 &lt; 4,320,118"), example("Round 6,748,215 to the nearest hundred thousand.", ["Hundred thousands digit: 7.", "The next digit is 4, so round down."], "6,700,000")],
        [['Comparing the last digits first', 'Start from the greatest place.'], ['Rounding to the wrong place', 'Underline the rounding place before you look to its right.'], ['Rounding 5 down', '5 or more rounds up.']])
    faq = [('What does TEKS 4.2C ask?', 'Compare and order whole numbers to 1,000,000,000 and represent comparisons using &gt;, &lt; or =.'), ('What does TEKS 4.2D ask?', 'Round whole numbers to a given place value through the hundred thousands place.'), ('How do you round to the nearest hundred thousand?', 'Look at the ten thousands digit. If it is 5 or more, add 1 to the hundred thousands digit. Then write zeros in all the places to the right.'), ('Why round big numbers?', 'Rounded numbers are easier to understand and compare, like saying a city has about 2,300,000 people.')]
    make('comparing-and-rounding-whole-numbers', 2, 'Number and Operations', '4.2C, 4.2D',
         '4.2C compare and order whole numbers to 1,000,000,000 and represent comparisons using the symbols >, <, or =; 4.2D round whole numbers to a given place value through the hundred thousands place',
         'Comparing, Ordering and Rounding Whole Numbers', 'Comparing and Rounding Whole Numbers',
         'Free Grade 4 worksheets for Texas TEKS 4.2C and 4.2D: compare and order numbers to a billion, round to the nearest thousand, ten thousand and hundred thousand, and real-world problems. 100 questions with answers.',
         'Compare from the left. Round by looking at the digit to the right.', 'The first place with different digits decides which number is greater. 5 or more rounds up.',
         body, faq, sets, seo_title='Grade 4 Comparing and Rounding Whole Numbers Worksheets (TEKS 4.2C, 4.2D, STAAR)')


if __name__ == "__main__":
    build()
