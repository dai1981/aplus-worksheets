# -*- coding: utf-8 -*-
"""
US Precalculus: The Binomial Theorem (Common Core A-APR.C.5)
  python3 tools/gen_us_math_pc_binomial_theorem.py
Pascal's triangle and binomial coefficients, coefficients in (x + y)ⁿ, a given term of (ax + b)ⁿ, full
expansions, and uses such as coin-flip probabilities, sums of coefficients and approximations.
Wrong answers come from real mistakes: forgetting to raise the coefficient a or b to its power, losing the
negative sign, using C(n, k) with the wrong k, and counting n terms instead of n + 1.
"""
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, num, MINUS, fr
from a2_common import sf, ps, poly, xp
from pc_common import GRADE, C

R = random.Random(98201)
X, Y = "<i>x</i>", "<i>y</i>"


def nck(n, k):
    return "<sub>%d</sub>C<sub>%d</sub>" % (n, k)


def binom_poly(a, b, n):
    """coefficients of (a x + b)^n from x^n down"""
    return [C(n, k) * a ** (n - k) * b ** k for k in range(n + 1)]


def lin2(a, b):
    s = ("" if a == 1 else MINUS if a == -1 else num(a)) + X
    return "(%s %s %s)" % (s, "+" if b > 0 else MINUS, num(abs(b)))


# ------------------------------------------------------------ set 1: binomial coefficients
def one_coef(r):
    n = r.randint(4, 10)
    k = r.randint(1, n - 1)
    kind = r.choice(["nck", "nck", "row"])
    if kind == "nck":
        ans = C(n, k)
        q = "Find %s." % nck(n, k)
        wr = [str(n * k), str(C(n, k - 1)) if C(n, k - 1) != ans else str(C(n, k + 1)), str(C(n - 1, k)) if C(n - 1, k) != ans else str(ans + n)]
        if len(set(wr + [str(ans)])) < 4:
            return None
        return T(q, num(ans), [num(int(w)) for w in wr], "%s = %d! / (%d! · %d!) = <b>%s</b>. It is entry %d in row %d of Pascal's triangle (starting from 0)." % (nck(n, k), n, k, n - k, num(ans), k, n))
    q = "Which list is row %d of Pascal's triangle (the row that starts 1, %d)?" % (n, n)
    right = ", ".join(str(C(n, i)) for i in range(n + 1))
    wr = [", ".join(str(C(n - 1, i)) for i in range(n)), ", ".join(str(C(n + 1, i)) for i in range(n + 2)), ", ".join(str(C(n, i) + (1 if 0 < i < n else 0)) for i in range(n + 1))]
    return T(q, right, wr, "Each entry is <sub>n</sub>C<sub>k</sub>, the sum of the two entries above it. <b>%s</b>." % right)


# ------------------------------------------------------------ set 2: coefficients in (x + y)^n
def one_xy(r):
    n = r.randint(4, 9)
    kind = r.choice(["coef", "coef", "terms", "count"])
    if kind == "terms":
        q = "How many terms are in the expansion of (%s + %s)<sup>%d</sup>?" % (X, Y, n)
        return T(q, str(n + 1), [str(n), str(2 * n), str(2 ** n)], "The powers of %s go from %d down to 0, which is <b>%d</b> terms." % (X, n, n + 1))
    if kind == "count":
        q = "In the expansion of (%s + %s)<sup>%d</sup>, what is the sum of the exponents in each term?" % (X, Y, n)
        return T(q, str(n), [str(n + 1), str(2 * n), "It changes from term to term"], "In each term %s<sup><i>a</i></sup>%s<sup><i>b</i></sup>, <i>a</i> + <i>b</i> = <b>%d</b>." % (X, Y, n))
    k = r.randint(1, n - 1)
    q = "What is the coefficient of %s%s in the expansion of (%s + %s)<sup>%d</sup>?" % (xp(n - k), xp(k, Y), X, Y, n)
    ans = C(n, k)
    wr = [str(n), str(k * (n - k)) if k * (n - k) != ans else str(ans + 1), str(C(n, k - 1)) if C(n, k - 1) != ans else str(C(n, k + 1) if C(n, k + 1) != ans else ans + 2)]
    if len(set(wr + [str(ans)])) < 4:
        wr.append(str(2 ** k))
    return T(q, num(ans), wr, "The term is %s %s%s, and %s = <b>%s</b>." % (nck(n, k), xp(n - k), xp(k, Y), nck(n, k), num(ans)))


# ------------------------------------------------------------ set 3: a term of (ax + b)^n
def one_term(r):
    a = r.choice([1, 2, 3, -1, -2])
    b = r.choice([1, 2, 3, -1, -2, -3, 4])
    n = r.randint(3, 7)
    p = r.randint(1, n - 1)
    k = n - p
    ans = C(n, k) * a ** p * b ** k
    if abs(ans) > 100000:
        return None
    q = "What is the coefficient of %s in the expansion of %s<sup>%d</sup>?" % (xp(p), lin2(a, b), n)
    wr = [sf(C(n, k) * a * b), sf(C(n, k) * a ** p * abs(b) ** k) if b < 0 and k % 2 else sf(C(n, k)), sf(C(n, k) * a ** k * b ** p) if a ** k * b ** p != a ** p * b ** k else sf(C(n, k) * b ** k)]
    if len(set(wr + [sf(ans)])) < 4:
        wr.append(sf(-ans))
    return T(q, sf(ans), wr, "The term with %s is %s(%s)<sup>%d</sup>(%s)<sup>%d</sup> = %d · %s · %s = <b>%s</b>%s." % (
        xp(p), nck(n, k), ("" if a == 1 else MINUS if a == -1 else num(a)) + X, p, sf(b), k, C(n, k), ps(a ** p), ps(b ** k), sf(ans), xp(p)))


# ------------------------------------------------------------ set 4: full expansions
def one_exp(r):
    a = r.choice([1, 1, 2, 3])
    b = r.choice([1, 2, 3, -1, -2, -3])
    n = r.choice([2, 3, 3, 4])
    if a > 1 and n == 4:
        return None
    cs = binom_poly(a, b, n)
    right = poly(cs)
    w1 = poly([a ** n] + [0] * (n - 1) + [b ** n])
    w2 = poly([C(n, k) * a ** (n - k) * abs(b) ** k for k in range(n + 1)]) if b < 0 else poly([C(n, k) * a * b for k in range(n + 1)][:1] + [C(n, k) * b ** k for k in range(1, n + 1)])
    w3 = poly([a ** (n - k) * b ** k for k in range(n + 1)])
    wr = [w1, w2, w3]
    if len(set(wr + [right])) < 4:
        return None
    return T("Expand %s<sup>%d</sup>." % (lin2(a, b), n), right, wr,
             "Use row %d of Pascal's triangle (%s) with powers of %s going down and powers of %s going up. <b>%s</b>." % (
                 n, ", ".join(str(C(n, i)) for i in range(n + 1)), ("" if a == 1 else num(a)) + X, sf(b), right))


# ------------------------------------------------------------ set 5: applications
def one_app(r):
    kind = r.choice(["coin", "coin", "sum", "approx", "approx"])
    if kind == "coin":
        n = r.choice([4, 5, 6, 8, 10])
        k = r.randint(1, n - 1)
        q = "A fair coin is flipped %d times. What is the probability of exactly %d heads?" % (n, k)
        ans = F(C(n, k), 2 ** n)
        wr = [sf(F(1, 2 ** n)), sf(F(k, n)) if F(k, n) != ans else sf(F(1, n)), sf(F(C(n, k), 2 * n)) if F(C(n, k), 2 * n) != ans else sf(ans * 2)]
        if len(set(wr + [sf(ans)])) < 4:
            return None
        return T(q, sf(ans), wr, "There are %s = %d ways to place the heads among %d equally likely outcomes (2<sup>%d</sup>). %d/%d = <b>%s</b>." % (
            nck(n, k), C(n, k), 2 ** n, n, C(n, k), 2 ** n, sf(ans)))
    if kind == "sum":
        a = r.choice([1, 2, 3])
        b = r.choice([1, -1, 2, -2, -3])
        n = r.randint(3, 6)
        ans = (a + b) ** n
        q = "What is the sum of all the coefficients in the expansion of %s<sup>%d</sup>?" % (lin2(a, b), n)
        wr = [sf(2 ** n) if 2 ** n != ans else sf(ans + 1), sf((a + abs(b)) ** n) if (a + abs(b)) ** n != ans else sf(n + 1), sf(a ** n + b ** n) if a ** n + b ** n != ans else sf(-ans)]
        if len(set(wr + [sf(ans)])) < 4:
            return None
        return T(q, sf(ans), wr, "Put %s = 1: (%s + (%s))<sup>%d</sup> = (%s)<sup>%d</sup> = <b>%s</b>." % (X, a, sf(b), n, sf(a + b), n, sf(ans)))
    base = r.choice([F(101, 100), F(102, 100), F(99, 100), F(98, 100), F(103, 100)])
    n = r.choice([4, 5, 6, 10])
    h = base - 1
    approx = 1 + n * h + C(n, 2) * h * h
    q = "Use the first three terms of the binomial expansion of (1 %s %s)<sup>%d</sup> to estimate (%s)<sup>%d</sup>." % ("+" if h > 0 else MINUS, num(abs(h)), n, num(base), n)
    return T(q, num(approx), [num(1 + n * h), num(1 + h) if 1 + h != approx else num(approx + F(1, 100)), num(1 + n * h + n * h * h)],
             "1 + %d(%s) + %d(%s)² = 1 %s %s + %s = <b>%s</b>." % (n, num(h), C(n, 2), num(h), "+" if h > 0 else MINUS, num(abs(n * h)), num(C(n, 2) * h * h), num(approx)))


def build():
    sets = [S("Binomial coefficients and Pascal's triangle", collect(one_coef, 20, R)),
            S("Coefficients in (x + y)ⁿ", collect(one_xy, 20, R)),
            S("Finding a term", collect(one_term, 20, R)),
            S("Full expansions", collect(one_exp, 20, R)),
            S("Applications", collect(one_app, 20, R))]
    body = lesson(
        "<ul><li><b>Binomial theorem</b>: (<i>x</i> + <i>y</i>)<sup><i>n</i></sup> = Σ <sub><i>n</i></sub>C<sub><i>k</i></sub> <i>x</i><sup><i>n</i>−<i>k</i></sup><i>y</i><sup><i>k</i></sup>, for <i>k</i> = 0 to <i>n</i>.</li>"
        "<li><sub><i>n</i></sub>C<sub><i>k</i></sub> = <i>n</i>! / (<i>k</i>!(<i>n</i> − <i>k</i>)!), the numbers in row <i>n</i> of Pascal's triangle.</li>"
        "<li>There are <i>n</i> + 1 terms. In each term, the exponents add to <i>n</i>.</li>"
        "<li>For (<i>ax</i> + <i>b</i>)<sup><i>n</i></sup>, raise the <b>whole</b> first term and the <b>whole</b> second term (with its sign) to their powers.</li></ul>",
        [("Find the coefficient of <i>x</i>³ in (2<i>x</i> − 1)<sup>5</sup>.", ["The term is <sub>5</sub>C<sub>2</sub>(2<i>x</i>)³(−1)²", "= 10 · 8 · 1"], "80"),
         ("Expand (<i>x</i> + 2)³.", ["Row 3: 1, 3, 3, 1", "<i>x</i>³ + 3<i>x</i>²(2) + 3<i>x</i>(4) + 8"], "<i>x</i>³ + 6<i>x</i>² + 12<i>x</i> + 8")],
        ["Forgetting to raise the coefficient: (2<i>x</i>)³ = 8<i>x</i>³, not 2<i>x</i>³.",
         "Losing the sign: (−1)² = 1 but (−1)³ = −1.",
         "Using the wrong row or position in Pascal's triangle.",
         "Counting <i>n</i> terms. (<i>x</i> + <i>y</i>)<sup><i>n</i></sup> has <i>n</i> + 1 terms."])
    faq = [("What is the binomial theorem?", "It expands (x + y)ⁿ as a sum of terms nCk · xⁿ⁻ᵏ · yᵏ for k = 0, 1, …, n."),
           ("How is Pascal's triangle related to the binomial theorem?", "Row n of Pascal's triangle gives the coefficients of (x + y)ⁿ. Each entry is the sum of the two entries above it."),
           ("How do you find one term without expanding everything?", "Choose k so the powers match, then compute nCk times the first term to the power n − k times the second term to the power k."),
           ("How do you find the sum of the coefficients?", "Substitute x = 1 (and y = 1) into the binomial. For (2x − 1)⁵, the sum is (2 − 1)⁵ = 1.")]
    make("binomial-theorem", 12, "A-APR.C.5",
         "The Binomial Theorem",
         "Binomial Theorem Worksheet: Pascal's Triangle and Expansions | 100 Questions with Answers",
         "Binomial Theorem",
         "Know and apply the Binomial Theorem for the expansion of (x + y)ⁿ in powers of x and y for a positive integer n, where x and y are any numbers, with coefficients determined for example by Pascal's Triangle.",
         "Free precalculus worksheet on the binomial theorem: binomial coefficients, Pascal's triangle, finding a term, full expansions and coin-flip probabilities. 100 questions.",
         "(x + y)ⁿ has n + 1 terms with coefficients nCk from Pascal's triangle.",
         "Raise the whole term, sign included, to each power.",
         body, faq, sets, R, domain="Polynomials", grade=GRADE)


if __name__ == "__main__":
    build()
