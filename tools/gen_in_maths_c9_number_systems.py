# -*- coding: utf-8 -*-
"""
India Class 9 Maths, NCERT Chapter 1: Number Systems (CBSE Unit I)
  python3 tools/gen_in_maths_c9_number_systems.py
Decimal expansions (terminating, non-terminating recurring) and p/q form of recurring decimals, rational and irrational
numbers (AU Year 8 maker), operations on real numbers with surds, rationalising the denominator, and the laws of
exponents with rational powers (US Algebra 1 maker).
Wrong answers come from real mistakes: 0.̅ 3 = 3/10, √a + √b = √(a + b), (√a + √b)² = a + b, multiplying the
denominator by itself to rationalise, and a⁻ⁿ as a negative number.
"""
import random, math
from fractions import Fraction as F
from in_common import num, S, make, lesson, mix, T, fv, fr, adopt, gb
import gen_au_maths_y8_irrational_numbers_and_recurring_decimals as au
import gen_us_math_a1_rational_exponents as us

R = random.Random(909001)
adopt(au, R)
adopt(us, R)


def ov(s):
    return "<span class='ov'>%s</span>" % s


def frs(v):
    v = F(v)
    return num(v) if v.denominator == 1 else fr(v.numerator, v.denominator)


# ---------------------------------------------------------------- set 1: decimal expansions and p/q
def one_dec(r):
    kind = r.choice(["pq", "pq", "pq", "type", "type"])
    if kind == "pq":
        t = r.choice(["one", "two", "mixed"])
        if t == "one":
            d = r.randint(1, 8)
            w = r.randint(0, 5)
            v = w + F(d, 9)
            s = "%d.%s" % (w, ov(str(d)))
            return T("Express %s in the form p/q." % s, frs(v), [frs(w + F(d, 10)), frs(w + F(d, 99)), frs(w + F(d, 90))],
                     "Let x = %s. Then 10x − x = %d.%d… − %s, so 9x = %d and x = <b>%s</b>." % (s, w * 10 + d, d, s, 9 * w + d, frs(v)))
        if t == "two":
            d = r.randint(10, 98)
            if d % 11 == 0:
                return None
            v = F(d, 99)
            s = "0.%s" % ov("%02d" % d)
            return T("Express %s in the form p/q." % s, frs(v), [frs(F(d, 100)), frs(F(d, 9)) if F(d, 9) != v else frs(F(d, 90)), frs(F(d, 90))],
                     "Two digits repeat, so multiply by 100: 100x − x = %d, x = %d/99 = <b>%s</b>." % (d, d, frs(v)))
        a, d = r.randint(1, 9), r.randint(1, 9)
        if a == d:
            return None
        v = F(9 * a + d, 90)
        s = "0.%d%s" % (a, ov(str(d)))
        return T("Express %s in the form p/q." % s, frs(v), [frs(F(10 * a + d, 99)), frs(F(10 * a + d, 90)), frs(F(10 * a + d, 100))],
                 "x = %s: 100x − 10x = %d%d.… − %d.… = %d, so x = %d/90 = <b>%s</b>." % (s, a, d, a, 9 * a + d, 9 * a + d, frs(v)))
    p = r.randint(1, 30)
    q = r.choice([2, 4, 5, 8, 16, 20, 25, 40, 3, 6, 7, 9, 11, 12, 13, 15])
    if math.gcd(p, q) != 1:
        return None
    qq = q
    for f_ in (2, 5):
        while qq % f_ == 0:
            qq //= f_
    term = qq == 1
    ans = "Terminating" if term else "Non-terminating recurring"
    return T("What kind of decimal expansion does %s have?" % fr(p, q), ans,
             ["Non-terminating recurring" if term else "Terminating", "Non-terminating non-recurring", "It cannot be decided"],
             "The denominator %d %s, so the decimal is <b>%s</b>. (A rational number never gives a non-terminating non-recurring decimal.)" % (q, "has only the prime factors 2 and 5" if term else "has a prime factor other than 2 and 5", ans.lower()))


# ---------------------------------------------------------------- set 3: operations with surds
def one_ops(r):
    kind = r.choice(["sq", "sq", "diff", "mul", "add"])
    a, b = r.sample([2, 3, 5, 6, 7, 10, 11], 2)
    if kind == "sq":
        sgn = r.choice(["+", "−"])
        p = 2 * a * b
        k = math.isqrt(a * b)
        rt = ("%d" % (2 * k)) if k * k == a * b else "2√%d" % (a * b)
        ans = "%d %s %s" % (a + b, sgn, rt)
        return T("Simplify (√%d %s √%d)²." % (a, sgn, b), ans, ["%d" % (a + b), "%d %s √%d" % (a + b, sgn, a * b), "%d %s %s" % (a * b, sgn, rt)],
                 "(√a %s √b)² = a + b %s 2√(ab) = <b>%s</b>." % (sgn, sgn, ans))
    if kind == "diff":
        if a < b:
            a, b = b, a
        return T("Simplify (√%d + √%d)(√%d − √%d)." % (a, b, a, b), str(a - b), [str(a + b), "%d − 2√%d" % (a - b, a * b), "√%d" % (a - b)],
                 "(√a + √b)(√a − √b) = a − b = %d − %d = <b>%d</b>." % (a, b, a - b))
    if kind == "mul":
        c, d = r.randint(2, 6), r.randint(2, 6)
        p = r.choice([2, 3, 5])
        return T("Simplify (%d + √%d)(%d − √%d)." % (c, p, d, p) if c != d else "Simplify (%d + √%d)(%d − √%d)." % (c, p, c, p),
                 _mul(c, d, p),
                 [_mul(c, d, -p), "%d" % (c * d - p), "%d + %d√%d" % (c * d, c + d, p)],
                 "Expand: %d·%d − %d√%d + %d√%d − %d = <b>%s</b>." % (c, d, c, p, d, p, p, _mul(c, d, p)))
    k = r.choice([2, 3, 5])
    m1, m2 = r.randint(1, 4), r.randint(1, 4)
    s1, s2 = m1 * m1 * k, m2 * m2 * k
    if s1 == s2:
        return None
    return T("Simplify √%d + √%d." % (s1, s2), "%d√%d" % (m1 + m2, k), ["√%d" % (s1 + s2), "%d√%d" % (m1 * m2, k), "%d√%d" % (m1 + m2, 2 * k)],
             "√%d = %s, √%d = %s. Add like surds: <b>%d√%d</b>. (√a + √b is not √(a + b).)" % (s1, ("%d√%d" % (m1, k)) if m1 > 1 else "√%d" % k, s2, ("%d√%d" % (m2, k)) if m2 > 1 else "√%d" % k, m1 + m2, k))


def _mul(c, d, p):
    """(c + √p)(d − √p) = cd − p + (d − c)√p  (p may be negative to make a wrong answer with the sign flipped)"""
    sgn = 1 if p > 0 else -1
    p = abs(p)
    const = c * d - sgn * p
    coef = (d - c) * sgn
    if coef == 0:
        return "%d" % const
    t = "√%d" % p if abs(coef) == 1 else "%d√%d" % (abs(coef), p)
    return "%d %s %s" % (const, "+" if coef > 0 else "−", t)


# ---------------------------------------------------------------- set 4: rationalising the denominator
def one_rat(r):
    kind = r.choice(["simple", "simple", "conj", "conj", "two"])
    if kind == "simple":
        a = r.randint(1, 9)
        p = r.choice([2, 3, 5, 6, 7, 10])
        g = math.gcd(a, p)
        num_, den = a // g, p // g
        top = "√%d" % p if num_ == 1 else "%d√%d" % (num_, p)
        ans = top if den == 1 else "%s/%d" % (top, den)
        return T("Rationalise the denominator of %d/√%d." % (a, p), ans, ["%d/%d" % (a, p) if F(a, p).denominator != 1 else "%d" % (a // p), ("%d√%d/%d" % (a, p, p * p) if a != 1 else "√%d/%d" % (p, p * p)), "√%d/%d" % (a, p) if a != 1 else "%d√%d" % (p, p)],
                 "Multiply top and bottom by √%d: %s√%d/%d = <b>%s</b>." % (p, "" if a == 1 else a, p, p, ans))
    if kind == "conj":
        a = r.randint(1, 5)
        p = r.choice([2, 3, 5, 6, 7])
        if a * a == p:
            return None
        sg = r.choice([1, -1])
        den = a * a - p
        ans = sx(a, -sg, p, den)
        sgs = "+" if sg > 0 else "−"
        wr = [sx(a, sg, p, den), sx(a, -sg, p, a * a + p), sx(a, -sg, p, 1) if abs(den) != 1 else sx(a, -sg, p, a * a + p + 1), sx(a, sg, p, a * a + p)]
        return T("Rationalise the denominator of 1/(%d %s √%d)." % (a, sgs, p), ans, [w for w in dict.fromkeys(wr) if w != ans][:3],
                 "Multiply top and bottom by the conjugate %d %s √%d: the denominator becomes %d² − %d = %d, so the answer is <b>%s</b>." % (a, "−" if sg > 0 else "+", p, a, p, den, ans))
    a, b = r.sample([2, 3, 5, 6, 7], 2)
    if a < b:
        a, b = b, a
    d = a - b
    ans = "√%d − √%d" % (a, b) if d == 1 else "(√%d − √%d)/%d" % (a, b, d)
    return T("Rationalise the denominator of 1/(√%d + √%d)." % (a, b), ans, ["√%d + √%d" % (a, b) if d == 1 else "(√%d + √%d)/%d" % (a, b, d), "(√%d − √%d)/%d" % (a, b, a + b), "√%d − √%d" % (a, b) if d != 1 else "(√%d − √%d)/2" % (a, b)],
             "Multiply by √%d − √%d: denominator %d − %d = %d, so <b>%s</b>." % (a, b, a, b, d, ans))


def sx(c0, c1, p, d):
    """(c0 + c1√p)/d written neatly"""
    if d < 0:
        c0, c1, d = -c0, -c1, -d
    rt = "√%d" % p if abs(c1) == 1 else "%d√%d" % (abs(c1), p)
    if c0 == 0:
        top = ("−" if c1 < 0 else "") + rt
    elif c0 > 0:
        top = "%d %s %s" % (c0, "+" if c1 > 0 else "−", rt)
    else:
        top = ("%s − %d" % (rt, -c0)) if c1 > 0 else ("−%d − %s" % (-c0, rt))
    return top if d == 1 else "(%s)/%d" % (top, d)


# ---------------------------------------------------------------- set 5: laws of exponents
def one_exp(r):
    kind = r.choice(["law", "law", "frac"])
    if kind == "frac":
        return us.one_eval(r)
    a = r.choice([2, 3, 5, 7, 11, 13])
    p, q = F(r.randint(1, 5), r.choice([2, 3, 4, 5])), F(r.randint(1, 5), r.choice([2, 3, 4, 5]))
    if p.denominator == 1 or q.denominator == 1:
        return None
    law = r.choice(["mul", "div", "pow"])
    sup = lambda v: "" if v == 1 else "<sup>%s</sup>" % ("%d" % v if F(v).denominator == 1 else "%d/%d" % (F(v).numerator, F(v).denominator))
    if law == "mul":
        v = p + q
        return T("Simplify %d%s · %d%s." % (a, sup(p), a, sup(q)), "%d%s" % (a, sup(v)), ["%d%s" % (a, sup(p * q)), "%d%s" % (a * a, sup(v)), "%d%s" % (a, sup(p + q + 1))],
                 "aᵖ · a<sup>q</sup> = a<sup>p + q</sup>: %s + %s = %s, so <b>%d%s</b>." % (frs(p), frs(q), frs(v), a, sup(v)))
    if law == "div":
        if p <= q:
            p, q = q, p
        if p == q:
            return None
        v = p - q
        return T("Simplify %d%s ÷ %d%s." % (a, sup(p), a, sup(q)), "%d%s" % (a, sup(v)), ["%d%s" % (a, sup(p / q)), "%d%s" % (a, sup(p + q)), "1%s" % sup(v)],
                 "aᵖ ÷ a<sup>q</sup> = a<sup>p − q</sup> = <b>%d%s</b>." % (a, sup(v)))
    v = p * q
    return T("Simplify (%d%s)%s." % (a, sup(p), sup(q)), "%d%s" % (a, sup(v)), ["%d%s" % (a, sup(p + q)), "%d%s" % (a, sup(p ** 2)) if p ** 2 != v else "%d%s" % (a, sup(v + 1)), "%d%s" % (a * a, sup(v))],
             "(aᵖ)<sup>q</sup> = a<sup>pq</sup>: %s × %s = %s, so <b>%d%s</b>." % (frs(p), frs(q), frs(v), a, sup(v)))


def main():
    seen = set()
    sets = [
        S("Decimal expansions and p/q form", mix(R, [(one_dec, 20)], seen)),
        S("Rational and irrational numbers", mix(R, [(gb(au.one_ri), 20)], seen)),
        S("Operations on real numbers", mix(R, [(one_ops, 20)], seen)),
        S("Rationalising the denominator", mix(R, [(one_rat, 20)], seen)),
        S("Laws of exponents for real numbers", mix(R, [(one_exp, 20)], seen)),
    ]
    body = lesson(
        "<p>A <b>rational number</b> p/q has a terminating or a non-terminating recurring decimal. An <b>irrational number</b> (√2, √3, π) has a non-terminating non-recurring decimal. Together they make the real numbers.</p>"
        "<p>Identities: (√a + √b)(√a − √b) = a − b, (√a + √b)² = a + b + 2√(ab). To <b>rationalise</b> 1/(a + √b), multiply top and bottom by a − √b.</p>"
        "<p>Laws of exponents: aᵖ · a<sup>q</sup> = a<sup>p + q</sup>, (aᵖ)<sup>q</sup> = a<sup>pq</sup>, a<sup>−n</sup> = 1/aⁿ, a<sup>m/n</sup> = (ⁿ√a)ᵐ.</p>",
        [("Express 0.4" + ov("7") + " in the form p/q.", ["x = 0.4777…", "100x − 10x = 47.7… − 4.7… = 43"], "43/90"),
         ("Rationalise 1/(7 + 3√2).", ["Multiply by 7 − 3√2", "Denominator 49 − 18 = 31"], "(7 − 3√2)/31")],
        ["Writing 0." + ov("3") + " = 3/10. A recurring decimal needs 9s in the denominator: 3/9 = 1/3.",
         "Using √a + √b = √(a + b). Only like surds can be added.",
         "Thinking a<sup>−n</sup> is negative. It is the reciprocal 1/aⁿ."])
    faq = [
        ("How do I convert a recurring decimal to p/q form?", "Let x equal the decimal, multiply by 10, 100, … so the repeating part lines up, subtract, and solve for x."),
        ("What is the difference between rational and irrational numbers?", "Rational numbers can be written as p/q and have terminating or recurring decimals. Irrational numbers cannot, and their decimals never end or repeat."),
        ("What does rationalising the denominator mean?", "Rewriting a fraction so that the denominator has no square root, by multiplying the numerator and denominator by a suitable surd (the conjugate)."),
        ("What is 64^(1/3)?", "The cube root of 64, which is 4. In general a^(1/n) is the nth root of a."),
    ]
    make(9, "number-systems", 1, "I", 1, "Number Systems: Rational and Irrational Numbers", "number systems",
         "Review of representation of natural numbers, integers and rational numbers on the number line; rational numbers as recurring/terminating decimals; operations on real numbers; non-recurring/non-terminating decimals and irrational numbers (√2, √3) on the number line; rationalisation of denominators; laws of exponents with integral and rational powers (summary of the CBSE syllabus)",
         "Class 9 Number Systems worksheet (NCERT Chapter 1): decimal expansions, p/q form, rational and irrational numbers, surds, rationalising denominators and laws of exponents. 100 questions with answers.",
         "Real numbers = rational + irrational", "Rational: terminating or recurring decimals. Irrational: never end, never repeat.",
         body, faq, sets, R)


if __name__ == "__main__":
    main()
