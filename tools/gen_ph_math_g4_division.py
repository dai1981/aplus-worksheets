# -*- coding: utf-8 -*-
"""
Philippines Grade 4 Math (MATATAG): Dividing 3- to 4-Digit Numbers by 1-Digit and 2- to 3-Digit Numbers by 2-Digit Numbers (Grade 4: Number and Algebra)
  python3 tools/gen_ph_math_g4_division.py
Dividing by 1-digit numbers with and without remainders and zeros in the quotient (US Grade 4 makers), dividing by
2-digit numbers (US Grade 5 maker) with Filipino names, and estimating quotients with multiples of 10 (own maker).
Wrong answers come from real mistakes: leaving out a 0 in the quotient, a remainder bigger than the divisor, and
rounding the divisor but not the dividend.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g4_division as usd
adopt(usd)
if hasattr(usd, 'R'): usd.R = random.Random(704080)
import gen_us_math_g5_division as us5
adopt(us5)
if hasattr(us5, 'R'): us5.R = random.Random(704081)
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


def one_estq(r):
    one = r.random() < 0.4
    if one:
        d = r.randint(3, 9)
        k = r.choice([k for k in range(20, 1000, 10) if d * k < 10000 and d * k >= 100])
        rd, D = d, d * k
        n = D + r.randint(-d * 4, d * 4)
        how = "Change %s to a nearby number that %d divides easily: %s." % (comma(n), d, comma(D))
    else:
        d = r.randint(11, 89)
        rd = (d + 5) // 10 * 10
        if rd == d or rd >= 100:
            raise AssertionError
        k = r.choice([k for k in range(2, 100) if 100 <= rd * k < 10000])
        D = rd * k
        n = D + r.randint(-rd // 3, rd // 3)
        how = "Round %d to %d. Then change %s to a nearby multiple of %d: %s." % (d, rd, comma(n), rd, comma(D))
    if n == D or n < 100:
        raise AssertionError
    est = D // rd
    exact = n // d
    w = [est * 10, est // 10 if est >= 20 and est % 10 == 0 else est + rd, exact if exact != est else exact + 1, D]
    return mcq("Estimate %s ÷ %d using multiples of 10 (compatible numbers)." % (comma(n), d), "about %s" % comma(est), ["about %s" % comma(x) for x in w if x != est],
               how + " %s ÷ %d = <b>%s</b>." % (comma(D), rd, comma(est)))


def build():
    sets, R = build_sets([
        ("Divide 3-digit numbers", [("run", usd.set_no_rem, ("rnd", "seen"), 20)]),
        ("4-digit dividends and zeros in the quotient", [("run", usd.set_four, ("rnd", "seen"), 20)]),
        ("Divide with remainders", [("run", usd.set_rem, ("rnd", "seen", usd.People), 20)]),
        ("Divide by 2-digit numbers", [("run", us5.set_two_digit, ("rnd", "seen"), 20)]),
        ("Estimate quotients", [("collect", uniq(one_estq), 20)]),
    ], 70408)
    finish(sets, R)
    body = lesson('<ul><li>Long division: <b>divide, multiply, subtract, bring down</b>. Repeat for each digit.</li><li>If a place cannot be divided, write <b>0</b> in the quotient.</li><li>The remainder must be less than the divisor. Check: quotient × divisor + remainder = dividend.</li><li>To estimate, round the divisor to a multiple of 10 and change the dividend to a nearby number it divides easily.</li></ul>',
        [example("4,236 ÷ 6", ["42 hundreds ÷ 6 = 7 hundreds", "3 tens ÷ 6 = 0 tens (write 0)", "36 ÷ 6 = 6"], "706"), example("Estimate 738 ÷ 23", ["23 → 20, 738 → 800", "800 ÷ 20"], "about 40")],
        [['Leaving out a 0', 'Write 0 when a place cannot be divided.'], ['A remainder as big as the divisor', 'Then the quotient digit is too small.'], ['Rounding only the divisor', 'Change the dividend to a compatible number too.']])
    faq = [('What does MATATAG Math 4 ask about division?', 'Divide 3- to 4-digit numbers by 1-digit numbers and 2- to 3-digit numbers by 2-digit numbers, with and without regrouping, and estimate the quotient by first estimating the dividends and divisors using multiples of 10.'), ('How do I check a division?', 'Multiply the quotient by the divisor and add the remainder.'), ('What are compatible numbers?', 'Numbers that are close to the real ones and easy to divide in your head.'), ('Can the remainder be 0?', 'Yes. Then the division is exact.')]
    make('dividing-whole-numbers', 8, 'Number and Algebra', 'Grade 4: Number and Algebra',
         'Divide two numbers with and without regrouping: 3- to 4-digit numbers by 1-digit numbers, and 2- to 3-digit numbers by 2-digit numbers; estimate the quotient when dividing 3- to 4-digit dividends by 1- to 2-digit divisors, by first estimating the dividends and divisors using multiples of 10.',
         'Dividing 3- to 4-Digit Numbers by 1-Digit and 2- to 3-Digit Numbers by 2-Digit Numbers', 'Division',
         'Free Grade 4 division worksheets for the DepEd MATATAG curriculum: long division by 1-digit and 2-digit numbers, zeros in the quotient, remainders and estimating quotients. 100 questions with answers.',
         'Divide, multiply, subtract, bring down.', 'The remainder is always less than the divisor.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
