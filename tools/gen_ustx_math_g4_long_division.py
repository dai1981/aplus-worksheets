# -*- coding: utf-8 -*-
"""
Texas Grade 4 Math: Long Division: Dividing up to 4-Digit Numbers by 1-Digit Numbers (TEKS 4.4E, 4.4F)
  python3 tools/gen_ustx_math_g4_long_division.py
Dividing tens and hundreds with basic facts, 2- and 3-digit dividends with area models, 4-digit dividends and zeros
in the quotient, remainders (the US Grade 4 division makers with Texas names), and representing a quotient with an
array, an area model or an equation.
Wrong answers come from real mistakes: forgetting a zero in the quotient, a remainder bigger than the divisor, and
subtracting instead of dividing.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g4_division as usd
adopt(usd)
tx_common.GRADE = "grade-4"

def one_rep(r):
    d = r.randint(2, 9)
    q = r.randint(12, 250)
    t = d * q
    kind = r.choice(["eq", "check", "parts"])
    if kind == "eq":
        return mcq("Which equation shows how to find %s ÷ %d?" % (comma(t), d), "%d × ☐ = %s" % (d, comma(t)), ["%s × %d = ☐" % (comma(t), d), "%s − %d = ☐" % (comma(t), d), "☐ ÷ %d = %s" % (d, comma(t))],
                   "Division asks: %d times what is %s? <b>%d × ☐ = %s</b>, and ☐ = %d." % (d, comma(t), d, comma(t), q))
    if kind == "check":
        return mcq("Which multiplication checks %s ÷ %d = %d?" % (comma(t), d, q), "%d × %d = %s" % (q, d, comma(t)), ["%d + %d = %d" % (q, d, q + d), "%s × %d" % (comma(t), d), "%d × %d = %s" % (q, d + 1, comma(q * (d + 1)))],
                   "Multiply the quotient by the divisor: <b>%d × %d = %s</b>." % (q, d, comma(t)))
    h = q // 10 * 10
    if h == 0 or h == q:
        return None
    return mcq("An area model splits %s ÷ %d into %s ÷ %d and %d ÷ %d. What is the quotient?" % (comma(t), d, comma(d * h), d, d * (q - h), d), q,
               [h, q - h, q + 1, h + d * (q - h)], "%s ÷ %d = %d and %d ÷ %d = %d. %d + %d = <b>%d</b>." % (comma(d * h), d, h, d * (q - h), d, q - h, h, q - h, q))


def build():
    sets, R = build_sets([
        ("Divide tens and hundreds using facts", [("run", usd.set_facts, ("rnd", "seen"), 20)]),
        ("Arrays, area models and equations", [("collect", one_rep, 20)]),
        ("Divide 2- and 3-digit numbers", [("run", usd.set_no_rem, ("rnd", "seen"), 20)]),
        ("4-digit dividends and zeros in the quotient", [("run", usd.set_four, ("rnd", "seen"), 20)]),
        ("Divide with remainders", [("run", usd.set_rem, ("rnd", "seen", usd.People), 20)]),
    ], 64009)
    finish(sets, R)
    body = lesson('<ul><li>Divide from the greatest place: divide, multiply, subtract, bring down. Repeat.</li><li>If a place cannot be divided, write <b>0</b> in the quotient.</li><li>The <b>remainder</b> must be less than the divisor.</li><li>Check: quotient × divisor + remainder = dividend.</li></ul>',
        [example("2,436 ÷ 6", ["24 hundreds ÷ 6 = 4 hundreds.", "3 tens ÷ 6 = 0 tens (write 0).", "36 ones ÷ 6 = 6."], "406"), example("Check 125 ÷ 4 = 31 R1", ["31 × 4 = 124", "124 + 1 = 125"], "correct")],
        [['Leaving out a 0 in the quotient: 2,436 ÷ 6 = 46', 'Write 0 when a place cannot be divided.'], ['A remainder as big as the divisor', 'If the remainder is too big, the quotient digit is too small.'], ['Forgetting to bring down a digit', 'Bring down one digit at a time.']])
    faq = [('What does TEKS 4.4E ask?', 'Represent the quotient of up to a four-digit whole number divided by a one-digit whole number using arrays, area models or equations.'), ('What does TEKS 4.4F ask?', 'Use strategies and algorithms, including the standard algorithm, to divide up to a four-digit dividend by a one-digit divisor.'), ('What is a remainder?', 'The amount left over when a number cannot be divided equally. It is always less than the divisor.'), ('How do I check a division answer?', 'Multiply the quotient by the divisor and add the remainder. You should get the dividend.')]
    make('long-division', 9, 'Number and Operations', '4.4E, 4.4F',
         '4.4E represent the quotient of up to a four-digit whole number divided by a one-digit whole number using arrays, area models, or equations; 4.4F use strategies and algorithms, including the standard algorithm, to divide up to a four-digit dividend by a one-digit divisor',
         'Long Division: Dividing up to 4-Digit Numbers by 1-Digit Numbers', 'Long Division',
         'Free Grade 4 long division worksheets for Texas TEKS 4.4E and 4.4F: divide using facts, area models and equations, 2- to 4-digit dividends, zeros in the quotient and remainders. 100 STAAR-style questions with answers.',
         'Divide, multiply, subtract, bring down.', 'Write 0 in the quotient when a place cannot be divided. The remainder is less than the divisor.',
         body, faq, sets, seo_title='Grade 4 Long Division Worksheets: 4-Digit by 1-Digit (TEKS 4.4E, 4.4F, STAAR)')


if __name__ == "__main__":
    build()
