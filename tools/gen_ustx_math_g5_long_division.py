# -*- coding: utf-8 -*-
"""
Texas Grade 5 Math: Dividing by 2-Digit Divisors (TEKS 5.3C)
  python3 tools/gen_ustx_math_g5_long_division.py
Dividing up to 4-digit dividends by 2-digit divisors: multiples of 10 and estimates, one-digit quotients, long
division and area models, zeros in the quotient and checking, and word problems with remainders. The question
makers come from the US Grade 5 division unit with Texas names.
Wrong answers come from real mistakes: an estimate that is too big or too small, forgetting a zero in the quotient,
and a remainder bigger than the divisor.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g5_division as usd
adopt(usd)
tx_common.GRADE = "grade-5"



def build():
    sets, R = build_sets([
        ("Divide with multiples of 10 and estimate", [("run", usd.set_tens, ("rnd", "seen"), 20)]),
        ("One-digit quotients: adjust the estimate", [("run", usd.set_one_digit, ("rnd", "seen", usd.People), 20)]),
        ("Two-digit quotients: long division and area models", [("run", usd.set_two_digit, ("rnd", "seen"), 20)]),
        ("Zeros in the quotient, remainders and checking", [("run", usd.set_zeros, ("rnd", "seen", usd.People), 20)]),
        ("Word problems: what to do with the remainder", [("run", usd.set_story, ("rnd", usd.People, "seen"), 20)]),
    ], 65005)
    finish(sets, R)
    body = lesson('<ul><li>Round the divisor to estimate each digit of the quotient: 3,682 ÷ 25 is about 3,600 ÷ 25.</li><li>Divide, multiply, subtract, compare, bring down. If the difference is as big as the divisor, the estimate was too small.</li><li>Write 0 in the quotient when a place cannot be divided.</li><li>Check: quotient × divisor + remainder = dividend.</li></ul>',
        [example("2,436 ÷ 12", ["24 hundreds ÷ 12 = 2 hundreds", "3 tens ÷ 12 = 0 tens", "36 ÷ 12 = 3"], "203"), example("Check 4,565 ÷ 87 = 52 R41", ["52 × 87 = 4,524", "4,524 + 41 = 4,565"], "correct")],
        [['An estimate that is too big', 'If the product is larger than what you have, try a smaller digit.'], ['Leaving out a 0 in the quotient', 'Every place after the first digit needs a digit.'], ['A remainder as big as the divisor', 'Then the quotient digit is too small.']])
    faq = [('What does TEKS 5.3C ask?', 'Solve with proficiency for quotients of up to a four-digit dividend by a two-digit divisor using strategies and the standard algorithm.'), ('How do you estimate with a 2-digit divisor?', 'Round the divisor to the nearest ten and use a basic fact: 368 ÷ 42 is about 360 ÷ 40 = 9.'), ('What if my estimate is wrong?', 'Adjust it: if the product is too big, try one less; if the difference is too big, try one more.'), ('How do you check a division answer?', 'Multiply the quotient by the divisor and add the remainder.')]
    make('dividing-by-two-digit-divisors', 5, 'Number and Operations', '5.3C',
         '5.3C solve with proficiency for quotients of up to a four-digit dividend by a two-digit divisor using strategies and the standard algorithm',
         'Dividing by 2-Digit Divisors', 'Dividing by 2-Digit Divisors',
         'Free Grade 5 division worksheets for Texas TEKS 5.3C: divide up to 4-digit numbers by 2-digit divisors with estimates, long division, area models, zeros in the quotient, remainders and word problems. 100 questions with answers.',
         'Estimate with a rounded divisor, then divide, multiply, subtract, bring down.', 'Write 0 when a place cannot be divided. Check: quotient × divisor + remainder = dividend.',
         body, faq, sets, seo_title='Grade 5 Dividing by 2-Digit Divisors Worksheets: Long Division (TEKS 5.3C, STAAR)')


if __name__ == "__main__":
    build()
