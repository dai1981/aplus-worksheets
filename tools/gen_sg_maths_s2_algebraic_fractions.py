# -*- coding: utf-8 -*-
"""
SG Secondary 2 Maths: Algebraic Fractions (MOE syllabus N5 Algebraic Expressions and Formulae)
  python3 tools/gen_sg_maths_s2_algebraic_fractions.py
Simplifying by cancelling common factors, multiplying and dividing simple algebraic fractions, adding and
subtracting with number denominators, adding and subtracting with linear denominators, and mixed problems.
Wrong answers come from real mistakes: cancelling terms instead of factors, adding numerators and
denominators straight across, forgetting to multiply every term by the other denominator, and losing the
minus sign in front of a bracket.
"""
import math
import random
from fractions import Fraction as F
from sg_sec import num, B, S, make, lesson, collect, T, fr, expr, MINUS, People

R = random.Random(820200)
P = People(R)
X = "<i>x</i>"


def lin(a, b, var=X):
    return expr([(a, var), (b, "")])


def br(a, b):
    return "(%s)" % lin(a, b)


def fx(top, bottom):
    return fr(top, bottom)


def mono(c, p):
    """c x^p"""
    v = "" if p == 0 else (X if p == 1 else X + {2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶"}[p])
    if c == 1 and v:
        return v
    if c == -1 and v:
        return MINUS + v
    return num(c) + v


def frac_mono(c, p):
    """c x^p written as a fraction when c is a fraction or p < 0"""
    c = F(c)
    sign = MINUS if c < 0 else ""
    c = abs(c)
    top_p, bot_p = (p, 0) if p >= 0 else (0, -p)
    top = mono(c.numerator, top_p) if (c.numerator != 1 or top_p == 0) else mono(1, top_p)
    if c.denominator == 1 and bot_p == 0:
        return sign + top
    bot = mono(c.denominator, bot_p) if (c.denominator != 1 or bot_p == 0) else mono(1, bot_p)
    return sign + fx(top, bot)


# ------------------------------------------------------------ set 1: simplify
def one_simp(r):
    kind = r.choice(["mono", "mono", "common", "dos", "trin"])
    if kind == "mono":
        a, b = r.randint(2, 12), r.randint(2, 12)
        p, q = r.randint(1, 3), r.randint(1, 3)
        if a == b and p == q:
            return None
        res = frac_mono(F(a, b), p - q)
        qh = "Simplify %s." % fx(mono(a, p), mono(b, q))
        wr = [frac_mono(F(a, b), p + q), frac_mono(F(a - b if a != b else a + 1, 1), p - q), frac_mono(F(b, a), q - p)]
        return T(qh, res, wr, "Divide the numbers by their HCF and subtract the powers of %s: <b>%s</b>." % (X, res))
    if kind == "common":
        k, b = r.randint(2, 6), r.choice([1, 2, 3, 4, 5, -1, -2, -3])
        m = r.choice([1, 2, 3, 5, 7])
        if math.gcd(k, m) != 1:
            return None
        qh = "Simplify %s." % fx(lin(k, k * b), lin(m, m * b))
        res = fx(str(k), str(m)) if m != 1 else str(k)
        wr = [fx(lin(k, 1), lin(m, 1)), frac_mono(F(k, m), 1), fx(lin(1, k * b), lin(1, m * b)) if m != 1 else lin(1, k * b)]
        return T(qh, res, wr, "Factorise: %s ÷ %s. The bracket (%s) cancels, leaving <b>%s</b>." % (
            "%d%s" % (k, br(1, b)), ("%d%s" % (m, br(1, b))) if m != 1 else br(1, b), lin(1, b), res))
    if kind == "dos":
        b = r.randint(1, 9)
        s = r.choice([1, -1])
        qh = "Simplify %s." % fx(expr([(1, X + "²"), (-b * b, "")]), lin(1, s * b))
        res = lin(1, -s * b)
        return T(qh, res, [lin(1, s * b), lin(1, -b * b) if b > 1 else lin(1, -s * 2), expr([(1, X), (-b * b, "")]) + " ÷ " + lin(1, s * b) if False else lin(-1, s * b)],
                 "%s² − %d = (%s)(%s). Cancel the common factor: <b>%s</b>." % (X, b * b, lin(1, b), lin(1, -b), res))
    p, q = r.sample([1, 2, 3, 4, 5, -1, -2, -3, -4], 2)
    qh = "Simplify %s." % fx(expr([(1, X + "²"), (p + q, X), (p * q, "")]), lin(1, p))
    res = lin(1, q)
    return T(qh, res, [lin(1, p), lin(1, p + q), lin(1, p * q) if p * q not in (q, p, p + q) else lin(1, -q)],
             "Factorise the top: (%s)(%s). Cancel (%s): <b>%s</b>." % (lin(1, p), lin(1, q), lin(1, p), res))


# ------------------------------------------------------------ set 2: multiply and divide
def one_md(r):
    a, b, c, d = [r.randint(2, 9) for _ in range(4)]
    p, q = r.randint(1, 3), r.randint(1, 3)
    if math.gcd(a, b) != 1 or math.gcd(c, d) != 1:
        return None
    if r.random() < 0.5:
        qh = "Simplify %s × %s." % (fx(mono(a, p), str(b)), fx(str(c), mono(d, q)))
        coef = F(a * c, b * d)
        res = frac_mono(coef, p - q)
        wr = [frac_mono(F(a * d, b * c), p + q), frac_mono(F(a + c, b + d), p - q), frac_mono(coef, p + q)]
        e = "Multiply tops and bottoms, then cancel: %s. <b>%s</b>." % (fx(mono(a * c, p), mono(b * d, q)), res)
    else:
        qh = "Simplify %s ÷ %s." % (fx(mono(a, p), str(b)), fx(mono(c, q), str(d)))
        coef = F(a * d, b * c)
        res = frac_mono(coef, p - q)
        wr = [frac_mono(F(a * c, b * d), p + q), frac_mono(F(b * c, a * d), q - p), frac_mono(coef, p + q)]
        e = "Dividing is multiplying by the reciprocal: %s × %s = <b>%s</b>." % (fx(mono(a, p), str(b)), fx(str(d), mono(c, q)), res)
    if len({res} | set(wr)) < 4:
        return None
    return T(qh, res, wr, e)


# ------------------------------------------------------------ set 3: number denominators
def one_num(r):
    m, n = r.sample([2, 3, 4, 5, 6], 2)
    a, b = r.randint(-5, 6), r.randint(-5, 6)
    sgn = r.choice([1, -1])
    L = m * n // math.gcd(m, n)
    k1, k2 = L // m, L // n
    # (x + a)/m ± (x + b)/n
    cx = k1 + sgn * k2
    c0 = k1 * a + sgn * k2 * b
    if cx == 0:
        return None
    qh = "Simplify %s %s %s." % (fx(lin(1, a), str(m)), "+" if sgn > 0 else MINUS, fx(lin(1, b), str(n)))
    res = fx(lin(cx, c0), str(L))
    if math.gcd(math.gcd(abs(cx), abs(c0)), L) > 1:
        return None
    w1 = fx(lin(2, a + b), str(m + n)) if sgn > 0 else fx(num(a - b), str(m + n))
    w2 = fx(lin(cx, k1 * a + k2 * b), str(L)) if sgn < 0 else fx(lin(cx, a + k2 * b), str(L))
    w3 = fx(lin(cx, k1 * a + sgn * b), str(L))
    wr = [w1, w2, w3]
    if len({res} | set(wr)) < 4:
        return None
    e = "Use the common denominator %d: %s %s %s = <b>%s</b>." % (
        L, fx("%s%s" % (k1 if k1 != 1 else "", br(1, a)), str(L)), "+" if sgn > 0 else MINUS, fx("%s%s" % (k2 if k2 != 1 else "", br(1, b)), str(L)), res)
    return T(qh, res, wr, e + (" Multiply every term in the second bracket by −1." if sgn < 0 else ""))


# ------------------------------------------------------------ set 4: linear denominators
def one_lin(r):
    a, b = r.randint(1, 5), r.randint(1, 5)
    p, q = r.sample([0, 1, 2, 3, -1, -2, -3], 2)
    sgn = r.choice([1, -1])
    cx = a + sgn * b
    c0 = a * q + sgn * b * p
    if cx == 0 and c0 == 0:
        return None
    if p == 0:
        den = "%s(%s)" % (X, lin(1, q))
    elif q == 0:
        den = "%s(%s)" % (X, lin(1, p))
    else:
        den = "(%s)(%s)" % (lin(1, p), lin(1, q))
    qh = "Simplify %s %s %s." % (fx(str(a), lin(1, p)), "+" if sgn > 0 else MINUS, fx(str(b), lin(1, q)))
    top = lin(cx, c0) if cx else num(c0)
    res = fx(top, den)
    w1 = fx(num(a + sgn * b), lin(2, p + q))
    w2 = fx(lin(cx, a * q + b * p) if (a * q + b * p) != c0 and cx else (lin(cx, c0 + 1) if cx else num(c0 + 1)), den)
    w3 = fx(num(a + sgn * b) if a + sgn * b else num(c0 + 2), den)
    if len({res, w1, w2, w3}) < 4:
        return None
    e = "Common denominator %s: %s %s %s = <b>%s</b>." % (den, fx("%d%s" % (a, "(%s)" % lin(1, q) if q else X), den), "+" if sgn > 0 else MINUS,
                                                       fx("%d%s" % (b, "(%s)" % lin(1, p) if p else X), den), res)
    return T(qh, res, [w1, w2, w3], e)


# ------------------------------------------------------------ set 5: mixed problems
def one_mix(r):
    kind = r.choice(["dos", "fmul", "fmul", "time", "time", "time", "check"])
    if kind == "dos":
        b = r.randint(1, 9)
        qh = "Simplify %s + %s." % (fx(X, expr([(1, X + "²"), (-b * b, "")])), fx("1", lin(1, b)))
        D = "(%s)(%s)" % (lin(1, b), lin(1, -b))
        res = fx(lin(2, -b), D)
        wr = [fx(lin(1, 1), expr([(1, X + "²"), (1, X), (-b * b + b, "")])), fx(lin(2, b), D), fx(lin(1, -b), D)]
        return T(qh, res, wr, "%s² − %d = %s. Write the second fraction as %s. Add the tops: %s + %s = <b>%s</b> over the common denominator." % (
            X, b * b, D, fx(lin(1, -b), D), X, lin(1, -b), lin(2, -b)))
    if kind == "fmul":
        b = r.randint(1, 6)
        c = r.choice([v for v in range(-5, 7) if v not in (0, b, -b)])
        k = r.randint(2, 5)
        # (x² − b²)/(k x + k c) × (x + c)/(x − b) = (x + b)/k
        qh = "Simplify %s × %s." % (fx(expr([(1, X + "²"), (-b * b, "")]), lin(k, k * c)), fx(lin(1, c), lin(1, -b)))
        res = fx(lin(1, b), str(k))
        wr = [fx(lin(1, -b), str(k)), lin(1, b), fx(lin(1, b), lin(k, k * c))]
        return T(qh, res, wr, "Factorise: %s = (%s)(%s) and %s = %d(%s). Cancel (%s) and (%s): <b>%s</b>." % (
            expr([(1, X + "²"), (-b * b, "")]), lin(1, b), lin(1, -b), lin(k, k * c), k, lin(1, c), lin(1, -b), lin(1, c), res))
    if kind == "time":
        d1, d2 = r.sample([20, 30, 40, 60, 90, 120], 2)
        k = r.choice([5, 10, 15, 20])
        how = "cycles" if max(d1, d2) <= 40 else "drives"
        nm, he, his = P.next()
        qh = ("%s %s %d km at <i>x</i> km/h and then %d km at (<i>x</i> + %d) km/h. Which expression gives the total time in hours?" % (nm, how, d1, d2, k))
        D = "%s(%s)" % (X, lin(1, k))
        res = fx(lin(d1 + d2, d1 * k), D)
        wr = [fx(str(d1 + d2), lin(2, k)), fx(lin(d1 + d2, d2 * k), D), fx(lin(d1 + d2, k), D)]
        return T(qh, res, wr, "Time = distance ÷ speed: %s + %s = %s = <b>%s</b>." % (
            fx(str(d1), X), fx(str(d2), lin(1, k)), fx("%d(%s) + %d%s" % (d1, lin(1, k), d2, X), D), res))
    a = r.randint(2, 9)
    m = r.choice([2, 3])
    qh = "A student writes %s = %s. What is the mistake?" % (fx(lin(1, a), lin(1, m * a)), fx("1", str(m)))
    right = "%s and %d are terms, not factors, so they cannot be cancelled" % (X, a)
    return T(qh, right, ["There is no mistake", "The answer should be %s" % fx(str(a), str(m * a)), "The answer should be %d" % m],
             "Only common <b>factors</b> cancel. %s and %s have no common factor, so the fraction cannot be simplified. <b>%s</b>." % (lin(1, a), lin(1, m * a), right))


def build():
    sets = [S("Simplifying algebraic fractions", collect(one_simp, 20, R)),
            S("Multiplying and dividing", collect(one_md, 20, R)),
            S("Adding and subtracting: number denominators", collect(one_num, 20, R)),
            S("Adding and subtracting: algebraic denominators", collect(one_lin, 20, R)),
            S("Mixed problems", collect(one_mix, 20, R))]
    body = lesson(
        "<ul><li>Algebraic fractions follow the same rules as number fractions.</li>"
        "<li>To <b>simplify</b>, factorise the top and bottom, then cancel common <b>factors</b> (never single terms).</li>"
        "<li>To <b>multiply</b>, multiply tops and bottoms and cancel. To <b>divide</b>, multiply by the reciprocal of the second fraction.</li>"
        "<li>To <b>add or subtract</b>, use a common denominator, multiply each top to match, then combine. Put brackets round each top so a minus sign changes every term.</li></ul>",
        [("Simplify " + fx("x² − 9", "x + 3") + ".", ["x² − 9 = (x + 3)(x − 3)", "Cancel (x + 3)"], "x − 3"),
         ("Simplify " + fx("x + 1", "2") + " − " + fx("x − 3", "5") + ".", ["Common denominator 10", fx("5(x + 1) − 2(x − 3)", "10") + " = " + fx("5x + 5 − 2x + 6", "10")], fx("3x + 11", "10")),
         ("Simplify " + fx("2", "x") + " + " + fx("3", "x + 1") + ".", [fx("2(x + 1) + 3x", "x(x + 1)")], fx("5x + 2", "x(x + 1)"))],
        ["Cancelling terms: " + fx("x + 6", "x + 2") + " is not 3.",
         "Adding straight across: " + fx("1", "x") + " + " + fx("1", "y") + " is not " + fx("2", "x + y") + ".",
         "Forgetting to multiply every term in the bracket when making a common denominator.",
         "Losing the minus sign: −2(x − 3) = −2x + 6."])
    faq = [("How do you simplify an algebraic fraction?", "Factorise the numerator and the denominator fully, then cancel any common factors. Only whole factors can be cancelled, not single terms."),
           ("How do you add algebraic fractions?", "Find a common denominator, rewrite each fraction over it, then add the numerators. Simplify the answer if possible."),
           ("How do you divide algebraic fractions?", "Multiply the first fraction by the reciprocal of the second, then cancel common factors."),
           ("Why can't I cancel the x in (x + 6)/(x + 2)?", "Because x is a term added to 6, not a factor of the whole numerator. Cancelling only works when the same factor multiplies the whole top and bottom.")]
    make(2, "algebraic-fractions", 2, "N5",
         "Algebraic Fractions: Simplify, Multiply, Divide, Add and Subtract",
         "", "Algebraic fractions", "",
         "Free Secondary 2 maths worksheets on algebraic fractions: simplifying by factorising, multiplying and dividing, and adding and subtracting with number and linear denominators. 100 questions with answers.",
         "Factorise first, then cancel common factors, never single terms.",
         "To add or subtract, use a common denominator and put brackets round each numerator.",
         body, faq, sets, R)


if __name__ == "__main__":
    build()
