# -*- coding: utf-8 -*-
"""
Texas Grade 7 Math: Adding and Subtracting Rational Numbers (TEKS 7.3A)
  python3 tools/gen_ustx_math_g7_add_subtract_rational.py
Adding and subtracting integers, decimals and fractions with negative signs, mixed practice, and word problems
(the US Grade 7 makers with a new seed, plus own fraction and decimal makers).
Wrong answers come from real mistakes: adding the absolute values when the signs differ, subtracting a negative as
if it were positive, and adding denominators.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g7_add_subtract_integers as asi
adopt(asi)
asi.R = random.Random(670020)
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
    if a is None or b is None or a.denominator == b.denominator == 1:
        return None
    op = r.choice(["+", "−"])
    v = a + b if op == "+" else a - b
    if v == 0 or v.denominator > 40:
        return None
    w = [a - b if op == "+" else a + b, -v, F(a.numerator + b.numerator, a.denominator + b.denominator) if op == "+" else F(a.numerator - b.numerator, a.denominator + b.denominator)]
    w = [sfr(x) for x in dict.fromkeys(w) if x != v]
    return mcq("Find %s %s %s." % (sfr(a), op, psfr(b)), sfr(v), w,
               "%sUse a common denominator: %s." % ("Add the opposite: %s + %s. " % (sfr(a), psfr(-b)) if op == "−" else "", "<b>%s</b>" % sfr(v)))


def one_dec(r):
    a = r.randint(-2000, 2000) / 100.0
    b = r.randint(-2000, 2000) / 100.0
    if abs(a) < 0.5 or abs(b) < 0.5 or round(a, 2) == int(a) and round(b, 2) == int(b):
        return None
    op = r.choice(["+", "−"])
    v = round(a + b if op == "+" else a - b, 2)
    if v == 0:
        return None
    w = [round(a - b if op == "+" else a + b, 2), -v, round(abs(a) + abs(b), 2) if round(abs(a) + abs(b), 2) != abs(v) else -round(abs(a) + abs(b), 2)]
    w = [sdec(x) for x in dict.fromkeys(w) if x != v]
    return mcq("Find %s %s %s." % (sdec(a), op, psdec(b)), sdec(v), w, "%s<b>%s</b>." % ("Add the opposite: %s + %s = " % (sdec(a), psdec(-b)) if op == "−" else "", sdec(v)))


def build():
    sets, R = build_sets([
        ("Warm-up: add integers", [("run", asi.set_add, (), 20)]),
        ("Subtract integers: add the opposite", [("run", asi.set_sub, (), 20)]),
        ("Add and subtract decimals with signs", [("collect", one_dec, 20)]),
        ("Add and subtract fractions with signs", [("run", asi.set_rational, (), 10), ("collect", one_frac, 10)]),
        ("Word problems", [("run", asi.set_words, (), 20)]),
    ], 67002)
    finish(sets, R)
    body = lesson('<ul><li><b>Same signs</b>: add the absolute values and keep the sign.</li><li><b>Different signs</b>: subtract the absolute values and use the sign of the number with the greater absolute value.</li><li>To <b>subtract</b>, add the opposite: −2.5 − (−4) = −2.5 + 4 = 1.5.</li><li>For fractions, use a common denominator first.</li></ul>',
        [example("−3/4 + 1/6", ["−9/12 + 2/12"], "−7/12"), example("−2.5 − (−4)", ["−2.5 + 4"], "1.5")],
        [['Adding absolute values when the signs differ', '−9 + 4 = −5, not −13.'], ['Subtracting a negative as a positive', '3 − (−5) = 3 + 5 = 8.'], ['Adding denominators', 'Use a common denominator: 1/2 + 1/3 = 5/6.']])
    faq = [('What does TEKS 7.3A ask?', 'Add, subtract, multiply and divide rational numbers fluently.'), ('Do the integer rules work for fractions and decimals?', 'Yes. The sign rules are the same for all rational numbers.'), ('How do I subtract a negative fraction?', 'Add its opposite: 1/2 − (−1/4) = 1/2 + 1/4 = 3/4.'), ('How can I check my answer?', "Use a number line, or check that the answer's sign makes sense.")]
    make('adding-and-subtracting-rational-numbers', 2, 'Number and Operations', '7.3A',
         '7.3A add, subtract, multiply, and divide rational numbers fluently',
         'Adding and Subtracting Rational Numbers', 'Adding and Subtracting Rational Numbers',
         'Free Grade 7 worksheets for Texas TEKS 7.3A: add and subtract integers, decimals and fractions with negative signs, mixed practice and word problems. 100 questions with answers.',
         'To subtract, add the opposite.', '−3/4 + 1/6 = −7/12. −2.5 − (−4) = 1.5.',
         body, faq, sets, seo_title='Grade 7 Adding and Subtracting Rational Numbers Worksheets (TEKS 7.3A, STAAR)')


if __name__ == "__main__":
    build()
