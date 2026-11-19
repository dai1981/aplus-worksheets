# -*- coding: utf-8 -*-
"""
Philippines Grade 4 Math (MATATAG): Rounding Numbers and Estimating Sums and Differences (Grade 4: Number and Algebra)
  python3 tools/gen_ph_math_g4_rounding_estimating.py
Rounding to the nearest thousand and other places (Singapore Primary 4 and US Grade 4 makers), rounding to the
nearest hundred thousand, and estimating sums and differences of 5- and 6-digit numbers by rounding (own makers).
Wrong answers come from real mistakes: rounding down when the next digit is 5, changing digits to the left, and
adding first and rounding later.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g4_place_value as usp
adopt(usp)
if hasattr(usp, 'R'): usp.R = random.Random(704050)
import gen_sg_maths_p4_rounding as sgr
adopt(sgr)
if hasattr(sgr, 'R'): sgr.R = random.Random(704051)
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


def rnd_to(n, p):
    return (n + p // 2) // p * p


def one_r100k(r):
    n = r.randint(100001, 999999)
    if r.random() < 0.3:
        n = n // 100000 * 100000 + 50000 + r.randint(0, 999)
    right = rnd_to(n, 100000)
    down = n // 100000 * 100000
    w = [down if right != down else down + 100000, rnd_to(n, 10000), rnd_to(n, 1000)]
    w = [x for x in w if x != right] + [right + 100000 if right < 1000000 else right - 100000]
    d = (n // 10000) % 10
    return mcq("Round %s to the nearest hundred thousand." % comma(n), right, w,
               "Look at the ten thousands digit: %d. %s, so the answer is <b>%s</b>." % (d, "5 or more: round up" if d >= 5 else "Less than 5: keep the hundred thousands digit", comma(right)))


def one_est(r):
    big = r.random() < 0.5
    a = r.randint(100000, 899999) if big else r.randint(10000, 89999)
    b = r.randint(10000, a - 1000) if r.random() < 0.5 else r.randint(10000, 99999)
    p = 100000 if big and b >= 100000 else 10000
    if p == 10000 and a >= 100000:
        p = 10000
    sub = r.random() < 0.5 and a > b
    ra, rb = rnd_to(a, p), rnd_to(b, p)
    est = ra - rb if sub else ra + rb
    if est <= 0:
        raise AssertionError
    exact = a - b if sub else a + b
    w = [exact, rnd_to(exact, p * 10), (a // p * p) - (b // p * p) if sub else (a // p * p) + (b // p * p)]
    w = [x for x in w if x != est] + [est + p]
    nm = "ten thousand" if p == 10000 else "hundred thousand"
    return mcq("Estimate %s %s %s by rounding each number to the nearest %s." % (comma(a), "−" if sub else "+", comma(b), nm), est, w,
               "%s → %s and %s → %s. %s %s %s = <b>%s</b>." % (comma(a), comma(ra), comma(b), comma(rb), comma(ra), "−" if sub else "+", comma(rb), comma(est)))


CTX = [("A town had %s people last year and %s people this year.", "How many people is that altogether, about?", "add"),
       ("A farm harvested %s kilograms of rice in the first season and %s kilograms in the second season.", "About how many kilograms is that in all?", "add"),
       ("A school raised %s pesos and %s pesos in two fund drives.", "About how many pesos did it raise in all?", "add"),
       ("A stadium has %s seats. %s seats were filled at a basketball game.", "About how many seats were empty?", "sub"),
       ("A city had %s trees. %s trees were cut after a typhoon.", "About how many trees were left?", "sub"),
       ("A website had %s visits in May and %s visits in June.", "About how many more visits were there in May?", "sub")]


def one_word(r):
    t, ask, op = r.choice(CTX)
    a = r.randint(120000, 950000)
    b = r.randint(15000, a - 20000) if op == "sub" else r.randint(15000, 990000 - a)
    if b < 10000:
        raise AssertionError
    p = 10000
    ra, rb = rnd_to(a, p), rnd_to(b, p)
    est = ra + rb if op == "add" else ra - rb
    exact = a + b if op == "add" else a - b
    w = [exact, ra - rb if op == "add" else ra + rb, est + 10000]
    return mcq((t % (comma(a), comma(b))) + " " + ask + " Round each number to the nearest ten thousand.", est, w,
               "%s → %s, %s → %s. %s %s %s = <b>%s</b>." % (comma(a), comma(ra), comma(b), comma(rb), comma(ra), "+" if op == "add" else "−", comma(rb), comma(est)))


def build():
    sets, R = build_sets([
        ("Round to the nearest thousand", [("run", sgr.set_thousand, (sgr.Picker,), 20)]),
        ("Round to different places", [("run", usp.set_round, ("rnd", "seen", usp.People), 12), ("run", sgr.set_hundred, (sgr.Picker,), 8)]),
        ("Round to the nearest hundred thousand", [("collect", uniq(one_r100k), 20)]),
        ("Estimate sums and differences", [("collect", uniq(one_est), 20)]),
        ("Estimate in word problems", [("collect", uniq(one_word), 20)]),
    ], 70405)
    finish(sets, R)
    body = lesson('<ul><li>To round, find the place you are rounding to and look at the digit just to its right.</li><li>If that digit is 5 or more, round up. If it is 4 or less, keep the digit. All the digits to the right become 0.</li><li>To <b>estimate</b> a sum or difference, round each number first, then add or subtract.</li><li>An estimate tells you if an exact answer is reasonable.</li></ul>',
        [example("Round 648,215 to the nearest hundred thousand", ["Ten thousands digit: 4"], "600,000"), example("Estimate 48,710 + 31,260", ["50,000 + 30,000"], "80,000")],
        [['Rounding down at 5', '5 or more rounds up.'], ['Changing digits to the left', 'Only the rounding place can change (and carry).'], ['Adding first, rounding later', 'For an estimate, round each number first.']])
    faq = [('What does MATATAG Math 4 ask about rounding?', 'Round numbers to the nearest hundred thousand, and estimate the sum and difference of two 5- to 6-digit numbers by rounding the addends to the nearest large place value of the numbers.'), ('Why estimate?', 'To check that an answer makes sense and to calculate quickly.'), ('What is 750,000 rounded to the nearest hundred thousand?', '800,000, because the ten thousands digit is 5.'), ('Can an estimate be wrong?', 'It is not exact, but it should be close.')]
    make('rounding-and-estimating', 5, 'Number and Algebra', 'Grade 4: Number and Algebra',
         'Round numbers to the nearest hundred thousand; estimate the sum and difference of two 5- to 6-digit numbers by rounding the addends to the nearest large place value of the numbers.',
         'Rounding Numbers and Estimating Sums and Differences', 'Rounding and Estimating',
         'Free Grade 4 rounding and estimating worksheets for the DepEd MATATAG curriculum: round to the nearest thousand and hundred thousand, and estimate sums and differences. 100 questions with answers.',
         'Look at the digit to the right: 5 or more rounds up.', 'Estimate: round first, then add or subtract.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
