# -*- coding: utf-8 -*-
"""
Texas Grade 7 Math: Multiplying and Dividing Rational Numbers (TEKS 7.3A)
  python3 tools/gen_ustx_math_g7_multiply_divide_rational.py
Sign rules with integers, multiplying and dividing decimals and fractions with signs, many factors, and word
problems (the US Grade 7 makers with a new seed, plus own fraction and decimal makers).
Wrong answers come from real mistakes: using the addition sign rules, flipping the wrong fraction, and losing a
negative sign.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g7_multiply_divide_integers as mdi
adopt(mdi)
mdi.R = random.Random(670030)
tx_common.GRADE = "grade-7"

from fractions import Fraction as F
from ws_common import num, par


def sfr(v):
    """Signed fraction or mixed number in HTML."""
    v = F(v)
    s = "−" if v < 0 else ""
    v = abs(v)
    if v.denominator == 1:
        return s + str(v.numerator)
    w, n = divmod(v.numerator, v.denominator)
    return s + (str(w) if w else "") + fr(n, v.denominator)


def psfr(v):
    return "(%s)" % sfr(v) if v < 0 else sfr(v)


def sdec(v):
    t = ("%.2f" % abs(v)).rstrip("0").rstrip(".")
    return ("−" if v < 0 else "") + t


def psdec(v):
    return "(%s)" % sdec(v) if v < 0 else sdec(v)


def rfrac(r):
    b = r.choice([2, 3, 4, 5, 6, 8, 10, 12])
    a = r.randint(1, 2 * b)
    v = F(a, b) * r.choice([1, -1])
    return v if v.denominator > 1 else None


def one_frac(r):
    a, b = rfrac(r), rfrac(r)
    if a is None or b is None:
        return None
    if abs(a) > 3 or abs(b) > 3:
        return None
    op = r.choice(["×", "÷"])
    v = a * b if op == "×" else a / b
    if v.denominator > 24 or abs(v) > 12:
        return None
    w = [-v, a / b if op == "×" else a * b, F(a.numerator * b.denominator, a.denominator * b.numerator) * -1 if op == "×" else 1 / v]
    w = [sfr(x) for x in dict.fromkeys(w) if x != v]
    how = "Multiply the tops and the bottoms" if op == "×" else "Multiply by the reciprocal of %s" % psfr(b)
    return mcq("Find %s %s %s." % (sfr(a), op, psfr(b)), sfr(v), w, "%s. %s, so the answer is <b>%s</b>." % (how, "The signs are the same" if (a > 0) == (b > 0) else "The signs are different", sfr(v)))


def one_dec(r):
    sa, sb = r.choice([1, -1]), r.choice([1, -1])
    if sa == sb == 1:
        sa = -1
    if r.random() < 0.5:
        a = r.randint(2, 99) / 10.0
        b = r.randint(2, 9) / (10.0 if r.random() < 0.3 else 1.0)
        x, y = sa * a, sb * b
        v = round(x * y, 3)
        if round(v, 2) != v:
            return None
        w = [-v, round(x + y, 2), round(v * 10, 2)]
        return mcq("Find %s × %s." % (sdec(x), psdec(y)), sdec(v), [sdec(t) for t in dict.fromkeys(w) if t != v],
                   "%s × %s = %s. %s, so the product is <b>%s</b>." % (sdec(a), sdec(b), sdec(abs(v)), "Same signs" if sa == sb else "Different signs", sdec(v)))
    q = r.randint(2, 40) / 10.0
    d = r.randint(2, 9) / (10.0 if r.random() < 0.4 else 1.0)
    n = round(q * d, 2)
    x, y = sa * n, sb * d
    v = round(x / y, 2)
    w = [-v, round(v * 10, 2), round(v / 10, 3)]
    return mcq("Find %s ÷ %s." % (sdec(x), psdec(y)), sdec(v), [sdec(t) for t in dict.fromkeys(w) if t != v],
               "%s ÷ %s = %s. %s, so the quotient is <b>%s</b>." % (sdec(n), sdec(d), sdec(q), "Same signs" if sa == sb else "Different signs", sdec(v)))


def build():
    sets, R = build_sets([
        ("Warm-up: multiply and divide integers", [("run", mdi.set_multiply, (), 10), ("run", mdi.set_divide, (), 10)]),
        ("Multiply and divide decimals with signs", [("collect", one_dec, 20)]),
        ("Multiply and divide fractions with signs", [("collect", one_frac, 20)]),
        ("Rational numbers and many factors", [("run", mdi.set_rational, (), 10), ("run", mdi.set_many, (), 10)]),
        ("Word problems", [("run", mdi.set_words, (), 20)]),
    ], 67003)
    finish(sets, R)
    body = lesson('<ul><li>Multiply or divide as if there were no signs.</li><li><b>Same signs</b> give a positive answer; <b>different signs</b> give a negative answer.</li><li>To divide by a fraction, multiply by its reciprocal: −2/3 ÷ 4/5 = −2/3 × 5/4 = −5/6.</li><li>With many factors, count the negatives: an even number gives a positive product.</li></ul>',
        [example("−2/3 × (−9/10)", ["2 × 9 = 18, 3 × 10 = 30", "Same signs"], "3/5"), example("−4.8 ÷ 0.6", ["48 ÷ 6 = 8", "Different signs"], "−8")],
        [['Using the addition sign rules', '(−4)(−3) = 12, not −12.'], ['Flipping the first fraction', 'Keep the first fraction; flip the divisor.'], ['Losing a negative sign', 'Decide the sign first, then compute.']])
    faq = [('What does TEKS 7.3A ask?', 'Add, subtract, multiply and divide rational numbers fluently.'), ('What is the reciprocal of −3/4?', '−4/3. A number and its reciprocal multiply to 1.'), ('Is −1/2 × −1/2 positive?', 'Yes, it is 1/4.'), ('How do I place the decimal point?', 'Multiply as whole numbers, then count the decimal places in both factors.')]
    make('multiplying-and-dividing-rational-numbers', 3, 'Number and Operations', '7.3A',
         '7.3A add, subtract, multiply, and divide rational numbers fluently',
         'Multiplying and Dividing Rational Numbers', 'Multiplying and Dividing Rational Numbers',
         'Free Grade 7 worksheets for Texas TEKS 7.3A: multiply and divide integers, decimals and fractions with negative signs, many factors and word problems. 100 questions with answers.',
         'Same signs: positive. Different signs: negative.', '−2/3 × (−9/10) = 3/5. −4.8 ÷ 0.6 = −8.',
         body, faq, sets, seo_title='Grade 7 Multiplying and Dividing Rational Numbers Worksheets (TEKS 7.3A, STAAR)')


if __name__ == "__main__":
    build()
