# -*- coding: utf-8 -*-
"""
Texas Grade 4 Math: Place Value to a Billion and Decimals to Hundredths (TEKS 4.2A, 4.2B)
  python3 tools/gen_ustx_math_g4_place_value.py
Reading and writing whole numbers through 1,000,000,000, the value of a digit, expanded notation, each place as 10
times the place to its right and one tenth of the place to its left (including tenths and hundredths). Sets 2 and 3
use the US Grade 4 place value makers with Texas names.
Wrong answers come from real mistakes: dropping a zero placeholder, reading the digit instead of its value, and
thinking a place is 10 times the place to its left.
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


def one_read(r):
    n = rbig(r, 7, 10)
    kind = r.choice(["words", "num"])
    s = str(n)
    i = s.find("0", 1)
    drop = int(s[:i] + s[i + 1:]) if i > 0 else n + 10 ** (len(s) - 2)
    if kind == "words":
        return mcq("How do you write %s in words?" % comma(n), bigwords(n), [bigwords(drop), bigwords(n * 10) if n * 10 < 10 ** 10 else bigwords(n // 10), bigwords(n + 10 ** (len(s) - 3))],
                   "Read each period: billions, millions, thousands, then the rest. <b>%s</b>." % bigwords(n))
    return mcq("Which number is %s?" % bigwords(n), comma(n), [comma(drop), comma(n // 10) if n // 10 > 10 ** 5 else comma(n * 10), comma(n + 10 ** (len(s) - 2))],
               "Write each period with 3 digits and use 0 for empty places: <b>%s</b>." % comma(n))


def one_tenth(r):
    kind = r.choice(["tenth", "tenth", "dec", "dec2"])
    if kind == "tenth":
        d = r.randint(2, 9)
        p = r.randint(1, 8)
        a = d * 10 ** p
        return mcq("The value of %d in %s is what part of the value of %d in %s?" % (d, comma(a), d, comma(a * 10)), "one tenth", ["10 times", "one hundredth", "the same"],
                   "%s is %s ÷ 10, so it is <b>one tenth</b> of the value." % (comma(a), comma(a * 10)))
    if kind == "dec":
        d = r.randint(1, 9)
        opts = [("%d" % d, "%d.%d" % (0, d), "tenths"), ("0.%d" % d, "0.0%d" % d, "hundredths")]
        a, b, name = r.choice(opts)
        return mcq("What is one tenth of %s?" % a, b, ["%d0" % d if "." not in a else "%d" % d, "0.00%d" % d, a + "0" if "." in a else "%d00" % d],
                   "Dividing by 10 moves each digit one place to the right: one tenth of %s is <b>%s</b>." % (a, b))
    d = r.randint(1, 9)
    return mcq("The %d in %d.0 is how many times the value of the %d in 0.%d?" % (d, d, d, d), "10 times", ["one tenth", "100 times", "the same"],
               "%d ones is 10 times %d tenths: <b>10 times</b>." % (d, d))


def one_expand(r):
    n = rbig(r, 7, 10)
    s = str(n)
    parts = [(int(c), len(s) - 1 - i) for i, c in enumerate(s) if c != "0"]
    right = " + ".join("(%d × %s)" % (c, comma(10 ** p)) for c, p in parts)
    wrong = [" + ".join("(%d × %s)" % (c, comma(10 ** (p - 1 if p else 0))) for c, p in parts),
             " + ".join(comma(c * 10 ** p) for c, p in parts),
             " + ".join("(%d × %s)" % (c, comma(10 ** p)) for c, p in parts[:-1])]
    return mcq("Which is %s in expanded notation?" % comma(n), right, wrong, "Each nonzero digit times its place value: <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Read and write numbers to a billion", [("collect", one_read, 20)]),
        ("Value of a digit and place names", [("run", usp.set_value, ("rnd", "seen"), 20)]),
        ("Each place is 10 times the place to its right", [("run", usp.set_ten_times, ("rnd", "seen"), 20)]),
        ("One tenth of the place to its left", [("collect", one_tenth, 20)]),
        ("Expanded notation", [("collect", one_expand, 20)]),
    ], 64001)
    finish(sets, R)
    body = lesson('<ul><li>Large numbers are read in groups of 3 digits (periods): billions, millions, thousands, ones. 2,045,300,016 is two billion, forty-five million, three hundred thousand, sixteen.</li><li>Each place is <b>10 times</b> the place to its right and <b>one tenth</b> of the place to its left. This works for decimals too: 0.3 is 10 times 0.03.</li><li><b>Expanded notation</b> writes each digit times its place value: (4 × 1,000,000) + (7 × 1,000) + (2 × 1).</li></ul>',
        [example("Write 30,506,000 in words.", ["30 million", "506 thousand"], "thirty million, five hundred six thousand"), example("What is one tenth of 0.6?", ["Move each digit one place right."], "0.06")],
        [['Dropping a zero: 30,506,000 as 3,506,000', 'Each period after the first has exactly 3 digits.'], ['Reading the digit, not its value', 'The 7 in 7,000,000 is worth 7 million.'], ['Thinking each place is 10 times the place to its left', 'Moving left multiplies by 10; moving right divides by 10.']])
    faq = [('What does TEKS 4.2A ask?', 'Interpret the value of each place as 10 times the position to the right and one tenth of the position to the left, including numbers through billions and decimals to hundredths.'), ('What does TEKS 4.2B ask?', 'Represent the value of a digit in whole numbers through 1,000,000,000 and decimals to hundredths with expanded notation and numerals.'), ('What is a period?', 'A group of 3 places: ones, thousands, millions, billions. Commas separate the periods.'), ('How do place values work for decimals?', 'Tenths are one tenth of ones, and hundredths are one tenth of tenths.')]
    make('place-value-to-billions', 1, 'Number and Operations', '4.2A, 4.2B',
         '4.2A interpret the value of each place-value position as 10 times the position to the right and as one-tenth of the value of the place to its left; 4.2B represent the value of the digit in whole numbers through 1,000,000,000 and decimals to the hundredths using expanded notation and numerals',
         'Place Value to a Billion and Decimals to Hundredths', 'Place Value to a Billion',
         'Free Grade 4 place value worksheets for Texas TEKS 4.2A and 4.2B: read and write numbers to a billion, value of a digit, 10 times and one tenth relationships with decimals, and expanded notation. 100 questions with answers.',
         'Each place is 10 times the place to its right.', 'Read big numbers by periods: billions, millions, thousands, ones. Each place is also one tenth of the place to its left.',
         body, faq, sets, seo_title='Grade 4 Place Value to a Billion Worksheets: Expanded Notation (TEKS 4.2A, 4.2B, STAAR)')


if __name__ == "__main__":
    build()
