# -*- coding: utf-8 -*-
"""
SG Secondary 3 Maths: Fractional Equations Reducible to Quadratic Equations (MOE syllabus N7)
  python3 tools/gen_sg_maths_s3_fractional_equations.py
Equations like 6/(x + 4) = 3 + x and 1/(x − 2) + 2/(x − 3) = 5: clearing the denominators, forming the
quadratic, solving by factorisation or the formula (2 decimal places), excluded values, and word problems
(journey times and sharing costs).
Wrong answers come from real mistakes: multiplying only one side by the denominator, forgetting to multiply
every term, sign errors when expanding, and keeping a value that makes a denominator 0 or is not sensible.
"""
import random
from fractions import Fraction as F
from math import isqrt, sqrt
from sg_sec import num, B, S, make, lesson, collect, T, fr, expr, MINUS, People

R = random.Random(830400)
P = People(R)
X = "<i>x</i>"
X2 = X + "<sup>2</sup>"


def lin(a, b):
    return expr([(a, X), (b, "")])


def quad(a, b, c):
    return expr([(a, X2), (b, X), (c, "")])


def fv(v):
    v = F(v)
    if v.denominator == 1:
        return num(v)
    return (MINUS if v < 0 else "") + fr(abs(v.numerator), v.denominator)


def sol(vs):
    vs = sorted(set(F(v) for v in vs))
    return " or ".join("%s = %s" % (X, fv(v)) for v in vs)


def d2(v):
    return ("%.2f" % v).replace("-", MINUS)


def sol2(a, b):
    a, b = sorted([a, b])
    return "%s = %s or %s = %s" % (X, d2(a), X, d2(b))


def rat_roots(a, b, c):
    D = b * b - 4 * a * c
    if D < 0 or isqrt(D) ** 2 != D:
        return None
    s = isqrt(D)
    return sorted({F(-b - s, 2 * a), F(-b + s, 2 * a)})


def nz(r, lo, hi, skip=()):
    return r.choice([v for v in range(lo, hi + 1) if v != 0 and v not in skip])


def clean(a, b, c):
    """divide by a common factor and make a > 0"""
    from math import gcd
    g = gcd(gcd(abs(a), abs(b)), abs(c)) or 1
    a, b, c = a // g, b // g, c // g
    if a < 0:
        a, b, c = -a, -b, -c
    return a, b, c


# ------------------------------------------------------------ set 1: a/(x + p) = x + q
def one_simple(r):
    p, q = nz(r, -5, 5), r.randint(-5, 5)
    r1 = r.randint(-8, 8)
    r2 = -(p + q) - r1
    a = p * q - r1 * r2
    if a == 0 or r1 == r2 or -p in (r1, r2) or abs(a) > 60:
        return None
    qh = "Solve %s = %s." % (fr(num(a), lin(1, p)), lin(1, q) if q else X)
    right = sol([r1, r2])
    wr = [sol([-r1, -r2]), sol([r1, -p]) if -p != r1 else sol([r2, -p]), sol(rat_roots(1, p + q, p * q + a) or [r1 + 1, r2 - 1])]
    if len({right} | set(wr)) < 4:
        return None
    return T(qh, right, wr, "Multiply both sides by (%s): %s = (%s)(%s). So %s = 0, which gives <b>%s</b>." % (
        lin(1, p), num(a), lin(1, p), lin(1, q) if q else X, quad(1, p + q, p * q - a), right))


# ------------------------------------------------------------ set 2: a/(x + p) + b/(x + q) = c
def two_fracs(r, need_rational=True):
    a, b = nz(r, -6, 6), nz(r, -6, 6)
    p, q = r.sample([-4, -3, -2, -1, 0, 1, 2, 3, 4], 2)
    c = nz(r, -4, 5)
    # a(x + q) + b(x + p) = c(x + p)(x + q)
    A = c
    Bc = c * (p + q) - a - b
    Cc = c * p * q - a * q - b * p
    A, Bc, Cc = clean(A, Bc, Cc)
    return a, b, p, q, c, (A, Bc, Cc)


def den(p):
    return X if p == 0 else lin(1, p)


def prod(p, q):
    if p == 0:
        return "%s(%s)" % (X, den(q))
    if q == 0:
        return "%s(%s)" % (X, den(p))
    return "(%s)(%s)" % (den(p), den(q))


def bterm(b, p):
    return "%s %s(%s)" % ("+" if b > 0 else MINUS, num(abs(b)), den(p))


def one_two(r):
    a, b, p, q, c, (A, Bc, Cc) = two_fracs(r)
    rs = rat_roots(A, Bc, Cc)
    if not rs or len(rs) < 2 or any(v in (-p, -q) for v in rs) or any(abs(v.denominator) > 5 or abs(v) > 12 for v in rs):
        return None
    kind = r.choice(["solve", "solve", "form"])
    lhs = "%s %s %s" % (fr(num(a), den(p)), "+" if b > 0 else MINUS, fr(num(abs(b)), den(q)))
    qh = "Solve %s = %s." % (lhs, num(c))
    if kind == "form":
        right = "%s = 0" % quad(A, Bc, Cc)
        w = [clean(A, -Bc, Cc), clean(A, Bc, -Cc), clean(c, c * (p + q) + a + b, c * p * q + a * q + b * p)]
        wr = ["%s = 0" % quad(*t) for t in w]
        if len({right} | set(wr)) < 4:
            return None
        return T("When %s = %s is written as a quadratic equation, which is correct?" % (lhs, num(c)), right, wr,
                 "Multiply every term by %s: %s(%s) %s = %s%s. Collect terms: <b>%s</b>." % (
                     prod(p, q), num(a), den(q), bterm(b, p), num(c), prod(p, q), right))
    right = sol(rs)
    wr = [sol([-v for v in rs]), sol([rs[0], -p if -p != rs[0] else -q]), sol(rat_roots(A, -Bc, Cc) or [rs[0] + 1, rs[1] + 1]) if rat_roots(A, -Bc, Cc) != rs else sol([rs[0] + 1, rs[1] + 1])]
    if len({right} | set(wr)) < 4:
        return None
    return T(qh, right, wr, "Multiply every term by %s and collect terms: %s = 0. Solve it: <b>%s</b>. Neither value makes a denominator 0." % (
        prod(p, q), quad(A, Bc, Cc), right))


# ------------------------------------------------------------ set 3: excluded values and checking
def one_excl(r):
    kind = r.choice(["excl", "excl", "check", "x_over"])
    if kind == "excl":
        p, q = r.sample([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5], 2)
        a, b = r.randint(1, 6), r.randint(1, 6)
        qh = "Which values of %s are not allowed in %s + %s = 3?" % (X, fr(num(a), lin(1, p)), fr(num(b), lin(1, q)))
        right = "%s = %s and %s = %s" % (X, num(min(-p, -q)), X, num(max(-p, -q)))
        return T(qh, right, ["%s = %s and %s = %s" % (X, num(min(p, q)), X, num(max(p, q))), "%s = 0" % X, "%s = 3" % X],
                 "A denominator cannot be 0. %s = 0 gives %s = %s, and %s = 0 gives %s = %s: <b>%s</b>." % (lin(1, p), X, num(-p), lin(1, q), X, num(-q), right))
    if kind == "check":
        # x/(x − k) = something with a root at x = k from cancelling: x/(x − 2) = 2/(x − 2) + 1 style
        k = r.randint(1, 6)
        m = r.choice([v for v in range(1, 8) if v != k])
        # x²/(x − k) = (k x ... ) simpler: (x² − m x)/(x − k) = ...  use  x/(x − k) − k/(x − k) = 1 has every x except k? avoid; use:
        # (x² + 2)/(x − k) = (k² + 2)/(x − k) + ... keep it simple:
        qh = "A student solves %s = %s and gets %s = %s or %s = %d. Which answer must be rejected?" % (
            fr(X2, lin(1, -k)), fr(num(k * k), lin(1, -k)), X, num(-k), X, k)
        return T(qh, "%s = %d, because it makes the denominator 0" % (X, k),
                 ["%s = %s, because it is negative" % (X, num(-k)), "Neither: both are correct", "Both must be rejected"],
                 "%s = %d makes %s = 0, and you cannot divide by 0. The solution is %s = %s only. <b>Reject %s = %d</b>." % (X, k, lin(1, -k), X, num(-k), X, k))
    a = r.randint(2, 6)
    r1, r2 = r.sample([v for v in range(-6, 8) if v not in (0, a)], 2)
    # x + c/(x) ... use  x = (s x − t)/x  ->  x² = s x − t
    s, t = r1 + r2, r1 * r2
    if t == 0:
        return None
    qh = "Solve %s = %s." % (X, fr(lin(s, -t), X))
    right = sol([r1, r2])
    return T(qh, right, [sol([-r1, -r2]), sol([0, s]), sol([s, -t]) if {s, -t} != {r1, r2} and s != -t else sol([r1 + 1, r2 + 1])],
             "Multiply both sides by %s: %s = %s, so %s = 0 and <b>%s</b>." % (X, X2, lin(s, -t), quad(1, -s, t), right))


# ------------------------------------------------------------ set 4: answers to 2 decimal places
def one_dp(r):
    a, b, p, q, c, (A, Bc, Cc) = two_fracs(r)
    D = Bc * Bc - 4 * A * Cc
    if D <= 0 or isqrt(D) ** 2 == D or A == 0:
        return None
    x1, x2 = (-Bc - sqrt(D)) / (2 * A), (-Bc + sqrt(D)) / (2 * A)
    if any(abs(abs(v) * 100 % 1 - 0.5) < 0.03 for v in (x1, x2)) or max(abs(x1), abs(x2)) > 30:
        return None
    lhs = "%s %s %s" % (fr(num(a), den(p)), "+" if b > 0 else MINUS, fr(num(abs(b)), den(q)))
    qh = "Solve %s = %s, giving your answers correct to 2 decimal places." % (lhs, num(c))
    right = sol2(x1, x2)
    D2 = Bc * Bc + 4 * A * Cc
    wr = [sol2(-x1, -x2), sol2((-Bc - sqrt(D2)) / (2 * A), (-Bc + sqrt(D2)) / (2 * A)) if D2 > 0 else sol2(x1 + 1, x2 + 1),
          sol2((Bc - sqrt(D)) / (2 * A) * 2, (Bc + sqrt(D)) / (2 * A) * 2)]
    if len({right} | set(wr)) < 4:
        return None
    return T(qh, right, wr, "Multiply every term by %s: %s = 0. <i>x</i> = %s, so <b>%s</b>." % (
        prod(p, q), quad(A, Bc, Cc), fr("%s ± √%s" % (num(-Bc), num(D)), num(2 * A)), right))


# ------------------------------------------------------------ set 5: word problems
def one_word(r):
    kind = r.choice(["speed", "speed", "share", "share", "price"])
    nm, he, his = P.next()
    if kind == "speed":
        v = r.choice([40, 45, 50, 60, 72, 75, 80, 90])
        k = r.choice([5, 10, 15, 20])
        t = r.choice([F(1, 2), F(1, 4), F(1, 3), F(1)])
        d = t * v * (v + k) / k
        if d.denominator != 1 or d > 600 or d < 60:
            return None
        tt = {F(1, 2): "30 minutes", F(1, 4): "15 minutes", F(1, 3): "20 minutes", 1: "1 hour"}[t]
        qh = ("%s drives %s km at <i>x</i> km/h. If %s drove %d km/h faster, the journey would take %s less. "
              "Which equation is correct, and what is <i>x</i>?" % (nm, num(d), he, k, tt))
        right = "%s − %s = %s, so <i>x</i> = %d" % (fr(num(d), X), fr(num(d), lin(1, k)), fv(t), v)
        wr = ["%s − %s = %s, so <i>x</i> = %d" % (fr(num(d), lin(1, k)), fr(num(d), X), fv(t), v + k),
              "%s − %s = %s, so <i>x</i> = %d" % (fr(num(d), X), fr(num(d), lin(1, k)), fv(t * 60) if t != 1 else "60", v // 2),
              "%s + %s = %s, so <i>x</i> = %d" % (fr(num(d), X), fr(num(d), lin(1, k)), fv(t), v - k)]
        return T(qh, right, wr, "Time = distance ÷ speed. The slower time minus the faster time is %s h. Clearing denominators gives a quadratic with a positive root <b><i>x</i> = %d</b> (%s ÷ %d − %s ÷ %d = %s)." % (
            fv(t), v, num(d), v, num(d), v + k, fv(t)))
    if kind == "share":
        n = r.randint(5, 14)
        k = r.choice([2, 3])
        c = r.choice([2, 3, 4, 5, 6, 8, 10])
        tot = F(c * n * (n - k), k)
        if tot.denominator != 1 or tot > 2000:
            return None
        qh = ("A group of <i>x</i> friends share the cost of a $%s gift equally. If %d of them drop out, each of the others pays $%d more. "
              "How many friends were there at first?" % (num(tot), k, c))
        return T(qh, num(n), [num(n - k), num(n + k), num(int(tot) // c)],
                 "%s − %s = %d. Multiply by %s(%s) and simplify: %s = 0. The positive answer is <b>%d</b>." % (
                     fr(num(tot), lin(1, -k)), fr(num(tot), X), c, X, lin(1, -k), quad(c, -c * k, -int(tot) * k), n))
    p = r.choice([2, 3, 4, 5, 6, 8])
    n = r.randint(6, 20)
    d = r.choice([1, 2, 4])
    # $T buys x items; if each cost $p less, could buy d more
    Tt = F(p * n * (n + d), d)
    if Tt.denominator != 1 or Tt > 1500:
        return None
    price = Tt / n
    if price.denominator not in (1, 2, 4, 5, 10, 20):
        return None
    qh = ("%s spends $%s on some books at $<i>x</i> each. If each book cost $%d less, %s could buy %d more. "
          "What is the price of one book?" % (nm, num(Tt), p, he, d))
    from sg_sec import sgd
    return T(qh, sgd(price), [sgd(price - p), sgd(n), sgd(price + p)],
             "%s − %s = %d. Clearing denominators gives a quadratic in <i>x</i> whose positive root is <b>%s</b> (%s books at %s, or %s at %s)." % (
                 fr(num(Tt), lin(1, -p)), fr(num(Tt), X), d, sgd(price), num(n), sgd(price), num(n + d), sgd(price - p)))


def build():
    sets = [S("Equations like a/(x + p) = x + q", collect(one_simple, 20, R)),
            S("Two fractions: forming and solving the quadratic", collect(one_two, 20, R)),
            S("Values that are not allowed", collect(one_excl, 20, R)),
            S("Answers to 2 decimal places", collect(one_dp, 20, R)),
            S("Word problems", collect(one_word, 20, R))]
    body = lesson(
        "<ul><li>Multiply <b>every term</b> by the denominators (the lowest common multiple of them) to clear the fractions.</li>"
        "<li>Expand, collect all terms on one side and solve the <b>quadratic</b> by factorising or the formula.</li>"
        "<li>Check each answer: a value that makes a denominator 0 is <b>not allowed</b>. In word problems, also reject answers that do not make sense.</li></ul>",
        [("Solve " + fr("6", "x + 4") + " = 3 + x.", ["Multiply by (x + 4): 6 = (3 + x)(x + 4)", "x² + 7x + 6 = 0, so (x + 1)(x + 6) = 0"], "x = −6 or x = −1"),
         ("Solve " + fr("1", "x") + " + " + fr("2", "x + 1") + " = 1.", ["Multiply by x(x + 1): (x + 1) + 2x = x(x + 1)", "x² − 2x − 1 = 0, so x = 1 ± √2"], "x = −0.41 or x = 2.41")],
        ["Multiplying only the fractions by the denominator and forgetting the whole-number term.",
         "Expanding a minus sign wrongly: −2(x − 3) = −2x + 6.",
         "Keeping an answer that makes a denominator 0.",
         "In speed problems, subtracting the times the wrong way round. The slower journey takes longer."])
    faq = [("What is a fractional equation?", "An equation with the unknown in a denominator, such as 6/(x + 4) = 3 + x. Clearing the fractions often turns it into a quadratic equation."),
           ("How do you clear the fractions?", "Multiply every term on both sides by the product (or LCM) of the denominators, then expand and simplify."),
           ("Why must I check my answers?", "Multiplying by an expression with x can bring in a value that makes a denominator 0. That value is not a solution and must be rejected."),
           ("How do I set up a speed word problem?", "Write each time as distance ÷ speed. The difference between the two times gives the equation, for example 120/x − 120/(x + 10) = 1/2.")]
    make(3, "fractional-equations", 4, "N7",
         "Fractional Equations That Reduce to Quadratic Equations",
         "", "Fractional equations", "",
         "Free Secondary 3 maths worksheets on fractional equations that reduce to quadratic equations: clearing denominators, solving by factorisation or formula, excluded values and word problems. 100 questions with answers.",
         "Multiply every term by the denominators, then solve the quadratic.",
         "Reject any answer that makes a denominator 0 or does not make sense.",
         body, faq, sets, R)


if __name__ == "__main__":
    build()
