# -*- coding: utf-8 -*-
"""
Texas Grade 2 Math: Place Value to 1,200: Thousands, Hundreds, Tens and Ones (TEKS 2.2A, 2.2B)
  python3 tools/gen_ustx_math_g2_place_value.py
Base-ten blocks, hundreds-tens-ones charts, expanded form, number names (the US Grade 2 makers with Texas names),
and numbers from 1,000 to 1,200 with a thousand block (own maker).
Wrong answers come from real mistakes: reading the digits in the wrong order, writing 1,000 + 100 + 4 as 11004, and
skipping a zero.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g2_place_value as pv
adopt(pv)
import random
pv.P = pv.People(random.Random(69201))
tx_common.GRADE = "grade-2"

WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen",
         "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def name99(n):
    if n < 20:
        return WORDS[n]
    return TENS[n // 10] + ("-" + WORDS[n % 10] if n % 10 else "")


def name(n):
    parts = []
    if n >= 1000:
        parts.append("one thousand")
        n -= 1000
    if n >= 100:
        parts.append(WORDS[n // 100] + " hundred")
        n %= 100
    if n:
        parts.append(name99(n))
    return " ".join(parts)


def one_thousand(r):
    n = r.randint(1001, 1200)
    h, t, o = (n - 1000) // 100, (n % 100) // 10, n % 10
    kind = r.choice(["expanded", "parts", "word", "digit"])
    if kind == "expanded":
        e = " + ".join(str(x) for x in (1000, h * 100, t * 10, o) if x)
        return mcq("What number is %s?" % e, str(n), [str(1000 + h * 100 + o * 10 + t) if t != o else str(n + 10), "1%d%d%d" % (h, t, o) if len(set(str(n))) > 1 else str(n + 1), str(100 + h * 100 + t * 10 + o)],
                   "%s = <b>%s</b>." % (e, n))
    if kind == "parts":
        return mcq("1 thousand, %d hundred%s, %d ten%s and %d one%s. What is the number?" % (h, "" if h == 1 else "s", t, "" if t == 1 else "s", o, "" if o == 1 else "s"), str(n),
                   [str(1000 + t * 100 + h * 10 + o) if t != h else str(n + 100), str(100 * h + 10 * t + o), str(1000 + h * 100 + t * 10 + o + 10)],
                   "1,000 + %d + %d + %d = <b>%s</b>." % (h * 100, t * 10, o, n))
    if kind == "word":
        return mcq("Which number is <b>%s</b>?" % name(n), str(n), [str(n + 100) if n + 100 <= 1200 else str(n - 100), str(n - 1000), str(1000 + (n % 100) * 10 // 10 + h * 10) if h else str(n + 10)],
                   "%s = <b>%s</b>." % (name(n), n))
    d = r.choice(["thousands", "hundreds", "tens", "ones"])
    v = {"thousands": 1, "hundreds": h, "tens": t, "ones": o}[d]
    others = [x for x in dict.fromkeys([1, h, t, o, 0, 9, 5]) if x != v][:3]
    return mcq("What digit is in the <b>%s</b> place in %s?" % (d, n), str(v), [str(x) for x in others],
               "In %s the %s digit is <b>%d</b>." % (n, d, v))


def build():
    sets, R = build_sets([
        ("Base-ten blocks", [("run", pv.set_blocks, ("rnd", "seen"), 20)]),
        ("Hundreds, tens and ones", [("run", pv.set_hto, ("rnd", "seen"), 20)]),
        ("Expanded form", [("run", pv.set_expanded, ("rnd", "seen"), 20)]),
        ("Number names", [("run", pv.set_names, ("rnd", "seen"), 20)]),
        ("Numbers from 1,000 to 1,200", [("collect", one_thousand, 20)]),
    ], 69201)
    finish(sets, R)
    body = lesson('<ul><li>Each place is 10 times the place to its right: ones, tens, hundreds, thousands.</li><li>1,153 = 1 thousand, 1 hundred, 5 tens, 3 ones.</li><li><b>Expanded form</b> adds the value of each digit: 1,000 + 100 + 50 + 3.</li><li>If there are no tens, write a 0 in the tens place: 1,107.</li></ul>',
        [example("4 hundreds, 0 tens, 6 ones", ["400 + 0 + 6"], "406"), example("1,000 + 100 + 20 + 9", ["1 thousand, 1 hundred, 2 tens, 9 ones"], "1,129")],
        [['Reading the digits in the wrong order', 'Start with the biggest place on the left.'], ['Writing 1,000 + 100 + 4 as 11,004', 'Each digit goes in its own place: 1,104.'], ['Skipping a zero', 'No tens? Write 0 in the tens place.']])
    faq = [('What does TEKS 2.2A ask?', 'Use concrete and pictorial models to compose and decompose numbers up to 1,200 in more than one way as a sum of so many thousands, hundreds, tens and ones.'), ('What does TEKS 2.2B ask?', 'Use standard, word and expanded forms to represent numbers up to 1,200.'), ('How many tens are in 100?', '10 tens make 1 hundred.'), ('Can a number be shown in more than one way?', 'Yes. 125 is 1 hundred, 2 tens, 5 ones, or 12 tens and 5 ones.')]
    make('place-value-to-1200', 1, 'Number and Operations', '2.2A, 2.2B',
         '2.2A use concrete and pictorial models to compose and decompose numbers up to 1,200 in more than one way as a sum of so many thousands, hundreds, tens, and ones; 2.2B use standard, word, and expanded forms to represent numbers up to 1,200',
         'Place Value to 1,200: Thousands, Hundreds, Tens and Ones', 'Place Value to 1,200',
         'Free Grade 2 place value worksheets for Texas TEKS 2.2A and 2.2B: base-ten blocks, hundreds, tens and ones, expanded form, number names and numbers to 1,200. 100 questions with answers.',
         'Each digit has a place: thousands, hundreds, tens, ones.', '1,153 = 1,000 + 100 + 50 + 3.',
         body, faq, sets, seo_title='Grade 2 Place Value to 1,200 Worksheets (TEKS 2.2A, 2.2B)')


if __name__ == "__main__":
    build()
