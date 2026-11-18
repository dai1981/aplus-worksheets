# -*- coding: utf-8 -*-
"""
SG Secondary 3 Maths: Indices (MOE syllabus N1: positive, negative, zero and fractional indices; laws of indices)
  python3 tools/gen_sg_maths_s3_indices.py
Laws of indices, zero and negative indices, fractional indices, simplifying algebraic terms and solving
equations such as 4^x = 8. Sets 1, 2 and part of 4 reuse the UK Year 8 question makers.
Wrong answers come from real mistakes: multiplying indices when multiplying powers, reading a negative index
as a negative number, taking the n-th root as dividing by n, and forgetting to apply the index to the number.
"""
import random
from fractions import Fraction as F
from sg_sec import num, B, S, make, lesson, collect, T, QN, fr, MINUS, adopt
import gen_uk_maths_y8_indices as uk

R = random.Random(830100)
adopt(uk, R)
pw, term = uk.pw, uk.term
X = "<i>x</i>"


def sup(b, p, q=1):
    """b^(p/q) with an inline fractional index"""
    e = num(p) if q == 1 else "%s%d/%d" % (MINUS if p < 0 else "", abs(p), q)
    return "%s<sup>%s</sup>" % (b, e)


def pws(b, e):
    return "%s<sup>%s</sup>" % (b, e)


def fv(v):
    v = F(v)
    if v.denominator == 1:
        return num(v)
    return (MINUS if v < 0 else "") + fr(abs(v.numerator), v.denominator)


ROOTS = [(4, 2), (9, 2), (16, 2), (25, 2), (36, 2), (49, 2), (64, 2), (81, 2), (100, 2), (8, 3), (27, 3), (64, 3), (125, 3), (1000, 3), (16, 4), (81, 4), (32, 5)]


# ------------------------------------------------------------ set 3: fractional indices
def one_frac(r):
    a, n = r.choice(ROOTS)
    b = round(a ** (1 / n))
    kind = r.choice(["root", "mn", "mn", "neg"])
    if kind == "root":
        q = "Work out %s." % B(sup(a, 1, n))
        return T(q, num(b), [fv(F(a, n)), num(a * n) if a * n < 10000 else num(a - n), fv(F(1, b))],
                 "An index of 1/%d means the %s root: %s = %s%s = <b>%s</b>." % (
                     n, {2: "square", 3: "cube", 4: "fourth", 5: "fifth"}[n], sup(a, 1, n), "√" if n == 2 else "<sup>%d</sup>√" % n, num(a), num(b)))
    if kind == "mn":
        m = r.choice([2, 3] if n != 2 else [3, 5])
        if b ** m > 100000:
            return None
        q = "Work out %s." % B(sup(a, m, n))
        return T(q, num(b ** m), [fv(F(a * m, n)), num(b * m), fv(F(1, b ** m))],
                 "Take the root first, then the power: %s = (%s)<sup>%d</sup> = %d<sup>%d</sup> = <b>%s</b>." % (sup(a, m, n), sup(a, 1, n), m, b, m, num(b ** m)))
    m = r.choice([1, 2] if n > 2 else [1, 3])
    if b ** m > 1000:
        return None
    q = "Work out %s." % B(sup(a, -m, n))
    right = fr(1, b ** m)
    return T(q, right, [MINUS + num(b ** m), fv(F(-a * m, n)), num(b ** m)],
             "The negative sign means “1 over”, the 1/%d means the root: %s = 1 ÷ %s = <b>%s</b>." % (n, sup(a, -m, n), num(b ** m), right))


# ------------------------------------------------------------ set 4: algebraic terms with all the laws
def one_alg(r):
    kind = r.choice(["uk", "uk", "root", "half", "neg"])
    if kind == "uk":
        return uk.one_alg(r)
    if kind == "root":
        a, n = r.choice([(4, 2), (9, 2), (16, 2), (25, 2), (8, 3), (27, 3), (64, 3), (125, 3)])
        b = round(a ** (1 / n))
        k = r.choice([2, 3, 4])
        q = "Simplify %s." % B("(%s%s)<sup>1/%d</sup>" % (num(a), pw(X, n * k), n))
        right = num(b) + pw(X, k)
        return T(q, right, [num(a) + pw(X, k), num(b) + pw(X, n * k - n), fv(F(a, n)) + pw(X, k)],
                 "Apply the index to the number and to %s: %s<sup>1/%d</sup> = %d and (%s)<sup>1/%d</sup> = %s. <b>%s</b>." % (
                     X, num(a), n, b, pw(X, n * k), n, pw(X, k), right))
    if kind == "half":
        p, q2 = r.choice([(1, 3), (3, 5), (1, 5), (5, 3), (3, 3), (1, 1)])
        tot = F(p + q2, 2)
        q = "Simplify %s × %s." % (sup(X, p, 2) if p != 2 else pw(X, 1), sup(X, q2, 2))
        right = sup(X, tot.numerator, tot.denominator) if tot.denominator != 1 else (pw(X, tot.numerator) if tot != 1 else X)
        wrong1 = sup(X, p * q2, 4)
        return T(q, right, [wrong1, sup(X, p + q2, 4), sup(X, p + q2, 1)],
                 "Same base, so add the indices: %d/2 + %d/2 = %s. <b>%s</b>." % (p, q2, fv(tot), right))
    m = r.randint(2, 6)
    c = r.choice([2, 3, 5])
    q = "Write %s using a negative index." % B(fr(c, pw(X, m)))
    right = num(c) + sup(X, -m)
    return T(q, right, [sup(num(c) + X, -m), num(c) + sup(X, m), MINUS + num(c) + pw(X, m)],
             "1 ÷ %s = %s, so %s = <b>%s</b>. Only %s is in the denominator, so only it gets the negative index." % (pw(X, m), sup(X, -m), fr(c, pw(X, m)), right, X))


# ------------------------------------------------------------ set 5: equations with indices
BASES = {2: [2, 4, 8, 16, 32, 64], 3: [3, 9, 27, 81], 5: [5, 25, 125]}


def one_eq(r):
    p = r.choice([2, 2, 3, 5])
    lhs = r.choice(BASES[p][:-1] if p == 2 else BASES[p])
    k = {v: i + 1 for i, v in enumerate(BASES[p])}[lhs]          # lhs = p^k
    kind = r.choice(["plain", "frac", "shift", "recip"])
    if kind == "plain" or k == 1:
        if k == 1:
            return None
        t = r.choice([v for v in range(2, 7) if p ** v <= 1000 and v != k])
        rhs = p ** t
        ans = F(t, k)
        q = "Solve %s = %s." % (B(pws(lhs, X)), num(rhs))
        e = "Write both sides as powers of %d: %s = %s. So %d%s = %d and %s = <b>%s</b>." % (
            p, pws(p, "%d%s" % (k, X)), pw(p, t), k, X, t, X, fv(ans))
        return T(q, "%s = %s" % (X, fv(ans)), ["%s = %s" % (X, fv(F(rhs, lhs))) if F(rhs, lhs) != ans else "%s = %s" % (X, fv(ans + 1)),
                                               "%s = %s" % (X, fv(t)) if t != ans else "%s = %s" % (X, fv(ans * 2)), "%s = %s" % (X, fv(F(k, t)))], e)
    if kind == "frac":
        t = r.choice([v for v in range(1, 6) if p ** v <= 1000])
        ans = F(-t, k)
        q = "Solve %s = %s." % (B(pws(lhs, X)), fr(1, p ** t))
        e = "%s = %s and %s = %s, so %d%s = %s and %s = <b>%s</b>." % (num(lhs), pw(p, k), fr(1, p ** t), pw(p, -t), k, X, num(-t), X, fv(ans))
        return T(q, "%s = %s" % (X, fv(ans)), ["%s = %s" % (X, fv(-ans)), "%s = %s" % (X, fv(F(1, p ** t))), "%s = %s" % (X, fv(ans - 1))], e)
    if kind == "shift":
        c = r.choice([1, 2, 3, -1])
        t = r.choice([v for v in range(2, 7) if p ** v <= 1000])
        ans = t - c
        if ans == 0:
            return None
        q = "Solve %s = %s." % (B(pws(p, "%s %s %d" % (X, "+" if c > 0 else MINUS, abs(c)))), num(p ** t))
        e = "%s = %s, so %s %s %d = %d and %s = <b>%s</b>." % (num(p ** t), pw(p, t), X, "+" if c > 0 else MINUS, abs(c), t, X, num(ans))
        return T(q, "%s = %s" % (X, num(ans)), ["%s = %s" % (X, num(t + c)), "%s = %s" % (X, num(t)), "%s = %s" % (X, num(-ans))], e)
    # recip: 9^x = 3 style
    if k == 1:
        return None
    q = "Solve %s = %s." % (B(pws(lhs, X)), num(p))
    ans = F(1, k)
    return T(q, "%s = %s" % (X, fv(ans)), ["%s = %s" % (X, num(k)), "%s = %s" % (X, fv(F(p, lhs))), "%s = 1" % X if ans != 1 else "%s = 0" % X],
             "%s = %s, so %d%s = 1 and %s = <b>%s</b>. (%s<sup>1/%d</sup> = %d.)" % (num(lhs), pw(p, k), k, X, X, fv(ans), num(lhs), k, p))


def build():
    sets = [S("Multiplying and dividing powers", collect(uk.one_mul, 10, R) + collect(uk.one_div, 10, R)),
            S("Power of a power, zero and negative indices", collect(uk.one_pp, 10, R) + collect(uk.one_neg, 10, R)),
            S("Fractional indices", collect(one_frac, 20, R)),
            S("Simplifying with the laws of indices", collect(one_alg, 20, R)),
            S("Equations with indices", collect(one_eq, 20, R))]
    body = lesson(
        "<p>For the same base <i>a</i>:</p>"
        "<ul><li><i>a</i><sup>m</sup> × <i>a</i><sup>n</sup> = <i>a</i><sup>m+n</sup> and <i>a</i><sup>m</sup> ÷ <i>a</i><sup>n</sup> = <i>a</i><sup>m−n</sup></li>"
        "<li>(<i>a</i><sup>m</sup>)<sup>n</sup> = <i>a</i><sup>mn</sup> and (<i>ab</i>)<sup>n</sup> = <i>a</i><sup>n</sup><i>b</i><sup>n</sup></li>"
        "<li><i>a</i><sup>0</sup> = 1 and <i>a</i><sup>−n</sup> = 1 ÷ <i>a</i><sup>n</sup></li>"
        "<li><i>a</i><sup>1/n</sup> is the <i>n</i>th root of <i>a</i>, and <i>a</i><sup>m/n</sup> = (<i>a</i><sup>1/n</sup>)<sup>m</sup>. Take the root first.</li></ul>",
        [("Work out 27<sup>2/3</sup>.", ["27<sup>1/3</sup> = 3 (cube root)", "3<sup>2</sup> = 9"], "9"),
         ("Work out 16<sup>−1/2</sup>.", ["16<sup>1/2</sup> = 4", "The negative index gives 1 ÷ 4"], fr(1, 4)),
         ("Solve 4<sup><i>x</i></sup> = 8.", ["4 = 2<sup>2</sup> and 8 = 2<sup>3</sup>", "2<sup>2<i>x</i></sup> = 2<sup>3</sup>, so 2<i>x</i> = 3"], "<i>x</i> = " + fr(3, 2))],
        ["Thinking 2<sup>−3</sup> is negative. It is " + fr(1, 8) + ".",
         "Dividing by the denominator: 64<sup>1/2</sup> is 8, not 32.",
         "Forgetting the number in a bracket: (8<i>x</i><sup>6</sup>)<sup>1/3</sup> = 2<i>x</i><sup>2</sup>, not 8<i>x</i><sup>2</sup>.",
         "Multiplying indices when multiplying powers: <i>a</i><sup>3</sup> × <i>a</i><sup>4</sup> = <i>a</i><sup>7</sup>."])
    faq = [("What does a fractional index mean?", "An index of 1/n means the nth root. For example, 9^(1/2) = √9 = 3 and 8^(1/3) = 2. For m/n, take the root first, then raise to the power m."),
           ("What does a negative index mean?", "It means 1 over the positive power: a^(−n) = 1/a^n. For example, 2^(−3) = 1/8. It does not make the answer negative."),
           ("Why is any number to the power 0 equal to 1?", "Because a^n ÷ a^n = a^(n−n) = a^0, and any non-zero number divided by itself is 1."),
           ("How do you solve an equation like 4^x = 8?", "Write both sides as powers of the same base: 2^(2x) = 2^3. Then the indices are equal, so 2x = 3 and x = 3/2.")]
    make(3, "indices", 1, "N1",
         "Indices: Zero, Negative and Fractional Indices and the Laws of Indices",
         "", "Indices", "",
         "Free Secondary 3 maths worksheets on indices: laws of indices, zero and negative indices, fractional indices, simplifying algebraic terms and solving index equations. 100 questions with answers.",
         "Same base: add indices to multiply, subtract to divide, multiply for a power of a power.",
         "A negative index means 1 over. A fractional index means a root: take the root first.",
         body, faq, sets, R)


if __name__ == "__main__":
    build()
