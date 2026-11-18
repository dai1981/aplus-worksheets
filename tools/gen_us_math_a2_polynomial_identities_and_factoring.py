# -*- coding: utf-8 -*-
"""
US Algebra 2: Polynomial Identities and Factoring (Common Core A-APR.C.4, A-APR.C.5, A-SSE.A.2)
  python3 tools/gen_us_math_a2_polynomial_identities_and_factoring.py
Sum and difference of cubes, factoring by grouping, quadratic form, special products and the Binomial
Theorem, and solving polynomial equations by factoring.
Wrong answers come from real mistakes: the wrong sign in the cube formulas, writing (a + b)³ as a³ + b³,
stopping before factoring completely, and dropping solutions when dividing by x.
"""
import math
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, num, MINUS
from a2_common import X, poly, sf, lin, pmul, xp

R = random.Random(95401)


def mono(c, var):
    """c·var with c = 1 written as var"""
    return (num(c) if c != 1 else "") + var


def sq_t(c, v, e):
    return (num(c) if c != 1 else "") + v + ({1: "", 2: "²", 3: "³"}[e])


# ------------------------------------------------------------ set 1: sum and difference of cubes
def one_cubes(r):
    a = r.choice([1, 2, 3, 4, 5])
    b = r.choice([1, 2, 3, 4, 5, 6])
    sign = r.choice([1, -1])
    var = r.choice([X, X, "<i>y</i>"])
    if a == b or math.gcd(a, b) > 1:
        return None
    A, Bc = a ** 3, b ** 3
    expr_ = "%s%s³ %s %s" % (num(A) if A != 1 else "", var, "+" if sign > 0 else MINUS, num(Bc))
    first = "%s%s" % (num(a) if a != 1 else "", var)
    sq = "%s%s²" % (num(a * a) if a != 1 else "", var)
    mid = "%s%s" % (num(a * b) if a * b != 1 else "", var)
    if sign > 0:
        right = "(%s + %d)(%s %s %s + %d)" % (first, b, sq, MINUS, mid, b * b)
        wr = ["(%s %s %d)(%s + %s + %d)" % (first, MINUS, b, sq, mid, b * b), "(%s + %d)(%s + %s + %d)" % (first, b, sq, mid, b * b), "(%s + %d)³" % (first, b)]
        e = "Sum of cubes: <i>a</i>³ + <i>b</i>³ = (<i>a</i> + <i>b</i>)(<i>a</i>² %s <i>ab</i> + <i>b</i>²) with <i>a</i> = %s and <i>b</i> = %d. <b>%s</b>." % (MINUS, first, b, right)
    else:
        right = "(%s %s %d)(%s + %s + %d)" % (first, MINUS, b, sq, mid, b * b)
        wr = ["(%s + %d)(%s %s %s + %d)" % (first, b, sq, MINUS, mid, b * b), "(%s %s %d)(%s %s %s + %d)" % (first, MINUS, b, sq, MINUS, mid, b * b), "(%s %s %d)³" % (first, MINUS, b)]
        e = "Difference of cubes: <i>a</i>³ %s <i>b</i>³ = (<i>a</i> %s <i>b</i>)(<i>a</i>² + <i>ab</i> + <i>b</i>²) with <i>a</i> = %s and <i>b</i> = %d. <b>%s</b>." % (MINUS, MINUS, first, b, right)
    return T("Factor %s." % B(expr_), right, wr, e + " (SOAP: Same sign, Opposite sign, Always Positive.)")


# ------------------------------------------------------------ set 2: factoring by grouping
def one_group(r):
    a = r.choice([1, 2, 3])
    b = r.choice([x for x in range(-6, 7) if x])
    c = r.choice([1, 2, 3, 4, 5, 6, 7, 9])
    sq = r.random() < 0.5 and math.isqrt(c) ** 2 == c
    s = r.choice([1, -1])
    # (a x + b)(x^2 + s c)
    p = pmul([a, b], [1, 0, s * c])
    q = "Factor %s by grouping%s." % (B(poly(p)), " completely" if sq and s < 0 else "")
    k = math.isqrt(c)
    if s < 0 and k * k == c:
        right = "(%s)(%s)(%s)" % (poly([a, b]), lin(k), lin(-k))
        wr = ["(%s)(%s)" % (poly([a, b]), poly([1, 0, -c])), "(%s)(%s)(%s)" % (poly([a, -b]), lin(k), lin(-k)), "(%s)(%s)²" % (poly([a, b]), lin(k))]
        e = "Group: %s(%s) %s %d(%s) = (%s)(%s). Then %s is a difference of squares: <b>%s</b>." % (
            xp(2), poly([a, b]), MINUS, c, poly([a, b]), poly([a, b]), poly([1, 0, -c]), poly([1, 0, -c]), right)
    else:
        right = "(%s)(%s)" % (poly([a, b]), poly([1, 0, s * c]))
        wr = ["(%s)(%s)" % (poly([a, -b]), poly([1, 0, s * c])), "(%s)(%s)" % (poly([a, b]), poly([1, 0, -s * c])), "(%s)(%s)" % (poly([1, b]), poly([a, 0, s * c])) if a != 1 else "(%s)(%s)" % (poly([1, s * c]), poly([1, 0, b]))]
        e = "Group the first two and last two terms: %s(%s) %s %d(%s). The common factor is (%s): <b>%s</b>." % (
            xp(2), poly([a, b]), "+" if s > 0 else MINUS, c, poly([a, b]), poly([a, b]), right)
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)


# ------------------------------------------------------------ set 3: quadratic form
def one_qform(r):
    m, n = r.sample([1, 2, 3, 4, 5, 6, 7, 9], 2)
    kind = r.choice(["sq", "mix"])
    if kind == "sq":
        m, n = r.sample([1, 4, 9, 16], 2)
    p = [1, 0, -(m + n), 0, m * n]
    q = "Factor %s completely over the integers." % B(poly(p))
    def f2(v):
        k = math.isqrt(v)
        if k * k == v:
            return "(%s)(%s)" % (lin(k), lin(-k))
        return "(%s)" % poly([1, 0, -v])
    lo, hi = sorted([m, n])
    right = f2(lo) + f2(hi)
    wr = ["(%s)(%s)" % (poly([1, 0, -lo]), poly([1, 0, -hi])) if right != "(%s)(%s)" % (poly([1, 0, -lo]), poly([1, 0, -hi])) else "(%s)(%s)" % (poly([1, 0, lo]), poly([1, 0, hi])),
          "(%s)(%s)" % (poly([1, 0, lo]), poly([1, 0, hi])), "(%s)(%s)" % (poly([1, -lo]), poly([1, -hi]))]
    e = "Let <i>u</i> = <i>x</i>². Then <i>u</i>² %s %d<i>u</i> + %d = (<i>u</i> %s %d)(<i>u</i> %s %d). Replace <i>u</i> with <i>x</i>² and factor any difference of squares: <b>%s</b>." % (
        MINUS, m + n, m * n, MINUS, lo, MINUS, hi, right)
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)


# ------------------------------------------------------------ set 4: special products and the Binomial Theorem
def one_ident(r):
    kind = r.choice(["cube", "cube", "binom", "binom", "id"])
    if kind == "cube":
        b = r.choice([1, 2, 3, 4])
        s = r.choice([1, -1])
        p = [1, 3 * s * b, 3 * b * b, s * b ** 3]
        q = "Expand %s." % B("(%s)³" % lin(-s * b))
        right = poly(p)
        wr = [poly([1, 0, 0, s * b ** 3]), poly([1, s * b, b * b, s * b ** 3]), poly([1, 3 * s * b, 3 * b * b, b ** 3]) if s < 0 else poly([1, 3 * b, 9 * b, b ** 3])]
        return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3],
                 "(<i>a</i> + <i>b</i>)³ = <i>a</i>³ + 3<i>a</i>²<i>b</i> + 3<i>ab</i>² + <i>b</i>³ with <i>b</i> = %s. <b>%s</b>. It is not just <i>a</i>³ + <i>b</i>³." % (sf(s * b), right))
    if kind == "binom":
        n = r.choice([4, 5, 6, 7])
        k = r.randint(1, n - 1)
        c = r.choice([1, 2, 3])
        coef = math.comb(n, k) * c ** k
        q = "What is the coefficient of %s in the expansion of %s?" % (B(xp(n - k)), B("(%s + %d)<sup>%d</sup>" % (X, c, n) if c > 1 else "(%s + 1)<sup>%d</sup>" % (X, n)))
        if c == 1:
            q = "What is the coefficient of %s in the expansion of %s?" % (B(xp(n - k)), B("(%s + <i>y</i>)<sup>%d</sup>" % (X, n)))
            q = q.replace(B(xp(n - k)), B(xp(n - k) + ("<i>y</i>" if k == 1 else "<i>y</i><sup>%d</sup>" % k)))
        wr = [math.comb(n, k), coef * c if c > 1 else math.comb(n, k + 1) if math.comb(n, k + 1) != coef else n, n * c ** k, c ** k]
        return T(q, num(coef), [num(w) for w in dict.fromkeys(wr) if w != coef][:3],
                 "Binomial Theorem: the term is C(%d, %d) · %s<sup>%d</sup> · %d<sup>%d</sup>. C(%d, %d) = %d (row %d of Pascal's triangle), so the coefficient is %d × %d = <b>%s</b>." % (
                     n, k, X, n - k, c, k, n, k, math.comb(n, k), n, math.comb(n, k), c ** k, num(coef)) if c > 1 else
                 "Binomial Theorem: the coefficient is C(%d, %d) = <b>%d</b>, from row %d of Pascal's triangle." % (n, k, coef, n))
    items = [("Which identity is true for all <i>x</i> and <i>y</i>?", "(<i>x</i>² + <i>y</i>²)² = (<i>x</i>² %s <i>y</i>²)² + (2<i>xy</i>)²" % MINUS,
              ["(<i>x</i> + <i>y</i>)² = <i>x</i>² + <i>y</i>²", "(<i>x</i> + <i>y</i>)³ = <i>x</i>³ + <i>y</i>³", "<i>x</i>² + <i>y</i>² = (<i>x</i> + <i>y</i>)(<i>x</i> + <i>y</i>)"],
              "Expand both sides: each equals <i>x</i>⁴ + 2<i>x</i>²<i>y</i>² + <i>y</i>⁴. This identity makes Pythagorean triples."),
             ("Use (<i>x</i>² %s <i>y</i>², 2<i>xy</i>, <i>x</i>² + <i>y</i>²) with <i>x</i> = 3 and <i>y</i> = 2. Which Pythagorean triple do you get?" % MINUS, "5, 12, 13",
              ["3, 4, 5", "5, 6, 13", "6, 8, 10"], "3² %s 2² = 5, 2(3)(2) = 12 and 3² + 2² = 13." % MINUS),
             ("Which product equals <i>a</i>² %s <i>b</i>²?" % MINUS, "(<i>a</i> + <i>b</i>)(<i>a</i> %s <i>b</i>)" % MINUS,
              ["(<i>a</i> %s <i>b</i>)²" % MINUS, "(<i>a</i> + <i>b</i>)²", "(<i>a</i> %s <i>b</i>)(<i>a</i>² + <i>ab</i> + <i>b</i>²)" % MINUS], "The middle terms cancel: <i>a</i>² %s <i>ab</i> + <i>ab</i> %s <i>b</i>²." % (MINUS, MINUS)),
             ("Use the identity <i>a</i>² %s <i>b</i>² = (<i>a</i> + <i>b</i>)(<i>a</i> %s <i>b</i>) to find 53 × 47 mentally." % (MINUS, MINUS), "2,491", ["2,500", "2,509", "2,401"],
              "53 × 47 = (50 + 3)(50 %s 3) = 2,500 %s 9." % (MINUS, MINUS)),
             ("Which is the expansion of (<i>a</i> %s <i>b</i>)²?" % MINUS, "<i>a</i>² %s 2<i>ab</i> + <i>b</i>²" % MINUS,
              ["<i>a</i>² %s <i>b</i>²" % MINUS, "<i>a</i>² + 2<i>ab</i> %s <i>b</i>²" % MINUS, "<i>a</i>² %s <i>ab</i> + <i>b</i>²" % MINUS], "(<i>a</i> %s <i>b</i>)(<i>a</i> %s <i>b</i>) has two middle terms of %s<i>ab</i>." % (MINUS, MINUS, MINUS))]
    q, right, wr, e = r.choice(items)
    return T(q, right, wr, e + " <b>%s</b>." % right)


# ------------------------------------------------------------ set 5: solve by factoring
def one_solve(r):
    kind = r.choice(["gcf", "gcf", "qform", "group", "cube"])
    if kind == "gcf":
        a, b = r.sample([x for x in range(-6, 7) if x], 2)
        p = pmul([1, 0], pmul([1, -a], [1, -b]))
        q = "Solve %s." % B(poly(p) + " = 0")
        sol = sorted([0, a, b])
        right = "<i>x</i> = " + ", ".join(sf(z) for z in sol)
        wr = ["<i>x</i> = " + ", ".join(sf(z) for z in sorted([a, b])), "<i>x</i> = " + ", ".join(sf(z) for z in sorted([0, -a, -b])), "<i>x</i> = " + ", ".join(sf(z) for z in sorted([-a, -b]))]
        return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3],
                 "Factor out <i>x</i>: <i>x</i>(%s) = 0, then <i>x</i>(%s)(%s) = 0. Do not divide by <i>x</i>, or you lose the solution 0. <b>%s</b>." % (
                     poly(pmul([1, -a], [1, -b])), lin(a), lin(b), right))
    if kind == "qform":
        m, n = r.sample([1, 4, 9, 16, 25], 2)
        p = [1, 0, -(m + n), 0, m * n]
        q = "Solve %s." % B(poly(p) + " = 0")
        rs = sorted([math.isqrt(m), -math.isqrt(m), math.isqrt(n), -math.isqrt(n)])
        right = "<i>x</i> = " + ", ".join(sf(z) for z in rs)
        wr = ["<i>x</i> = %s, %s" % (num(min(m, n)), num(max(m, n))), "<i>x</i> = %s, %s" % (num(math.isqrt(min(m, n))), num(math.isqrt(max(m, n)))), "<i>x</i> = ±%s" % num(math.isqrt(m * n))]
        return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3],
                 "(<i>x</i>² %s %d)(<i>x</i>² %s %d) = 0, so <i>x</i>² = %d or <i>x</i>² = %d. Take ± square roots: <b>%s</b>." % (MINUS, m, MINUS, n, m, n, right))
    if kind == "group":
        a = r.choice([x for x in range(-5, 6) if x])
        k = r.choice([1, 2, 3, 4])
        p = pmul([1, -a], [1, 0, -k * k])
        q = "Solve %s." % B(poly(p) + " = 0")
        rs = sorted({a, k, -k})
        right = "<i>x</i> = " + ", ".join(sf(z) for z in rs)
        wr = ["<i>x</i> = " + ", ".join(sf(z) for z in sorted({-a, k, -k})), "<i>x</i> = %s, %s" % (sf(min(a, k * k)), sf(max(a, k * k))) if a != k * k else "<i>x</i> = %s" % sf(a), "<i>x</i> = %s, %s" % (sf(min(a, k)), sf(max(a, k))) if a != k else "<i>x</i> = %s, %s" % (sf(a), sf(-a - 1))]
        return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3],
                 "Group: <i>x</i>²(%s) %s %d(%s) = (%s)(<i>x</i>² %s %d) = (%s)(%s)(%s). <b>%s</b>." % (lin(a), MINUS, k * k, lin(a), lin(a), MINUS, k * k, lin(a), lin(k), lin(-k), right))
    b = r.choice([1, 2, 3, 4, 5])
    q = "Find the real solution of %s." % B("%s³ %s %d = 0" % (X, MINUS, b ** 3))
    return T(q, "<i>x</i> = %d" % b, ["<i>x</i> = ±%d" % b, "<i>x</i> = %s" % sf(-b), "<i>x</i> = %s" % num(F(b ** 3, 3)) if (b ** 3) % 3 == 0 else "<i>x</i> = %d" % (b * b)],
             "(<i>x</i> %s %d)(<i>x</i>² + %d<i>x</i> + %d) = 0. The quadratic has a negative discriminant, so the only real solution is <b><i>x</i> = %d</b>." % (MINUS, b, b, b * b, b))


def build():
    sets = [S("Sum and difference of cubes", collect(one_cubes, 20, R)),
            S("Factoring by grouping", collect(one_group, 20, R)),
            S("Quadratic form", collect(one_qform, 20, R)),
            S("Identities and the Binomial Theorem", collect(one_ident, 20, R)),
            S("Solve by factoring", collect(one_solve, 20, R))]
    body = lesson(
        "<ul><li><b>Sum of cubes</b>: <i>a</i>³ + <i>b</i>³ = (<i>a</i> + <i>b</i>)(<i>a</i>² %s <i>ab</i> + <i>b</i>²).</li>"
        "<li><b>Difference of cubes</b>: <i>a</i>³ %s <i>b</i>³ = (<i>a</i> %s <i>b</i>)(<i>a</i>² + <i>ab</i> + <i>b</i>²).</li>"
        "<li><b>Grouping</b>: with four terms, factor the first pair and the second pair, then take out the common binomial.</li>"
        "<li><b>Quadratic form</b>: <i>x</i>⁴ %s 5<i>x</i>² + 4 is a quadratic in <i>x</i>²: (<i>x</i>² %s 1)(<i>x</i>² %s 4).</li>"
        "<li><b>Binomial Theorem</b>: the coefficients of (<i>a</i> + <i>b</i>)<sup><i>n</i></sup> are row <i>n</i> of Pascal's triangle, C(<i>n</i>, <i>k</i>).</li></ul>"
        "<p>To solve a polynomial equation, move everything to one side, factor completely, and set each factor equal to 0.</p>" % (MINUS, MINUS, MINUS, MINUS, MINUS, MINUS),
        [("Factor 8<i>x</i>³ + 27.", ["<i>a</i> = 2<i>x</i>, <i>b</i> = 3"], "(2<i>x</i> + 3)(4<i>x</i>² %s 6<i>x</i> + 9)" % MINUS),
         ("Solve <i>x</i>³ + 2<i>x</i>² %s 9<i>x</i> %s 18 = 0." % (MINUS, MINUS), ["<i>x</i>²(<i>x</i> + 2) %s 9(<i>x</i> + 2)" % MINUS, "(<i>x</i> + 2)(<i>x</i> %s 3)(<i>x</i> + 3)" % MINUS], "<i>x</i> = %s3, %s2, 3" % (MINUS, MINUS))],
        ["Mixing up the signs in the cube formulas. Same sign, opposite sign, always positive.",
         "Writing (<i>a</i> + <i>b</i>)³ = <i>a</i>³ + <i>b</i>³. The middle terms 3<i>a</i>²<i>b</i> + 3<i>ab</i>² are missing.",
         "Stopping before factoring completely, such as leaving <i>x</i>² %s 9." % MINUS,
         "Dividing both sides by <i>x</i> and losing the solution <i>x</i> = 0."])
    faq = [("How do you factor a sum of cubes?", "a³ + b³ = (a + b)(a² − ab + b²). The second factor does not factor further over the real numbers."),
           ("How do you factor by grouping?", "Split four terms into two pairs, factor the GCF from each pair, and then factor out the common binomial."),
           ("What is quadratic form?", "An expression like x⁴ − 13x² + 36 that is a quadratic in x². Substitute u = x², factor, then substitute back."),
           ("What is the Binomial Theorem?", "(a + b)ⁿ = Σ C(n, k) aⁿ⁻ᵏ bᵏ. The coefficients C(n, k) come from Pascal's triangle.")]
    make("polynomial-identities-and-factoring", 4, "A-APR.C.4",
         "Polynomial Identities and Factoring",
         "Factoring Polynomials Worksheet: Sum and Difference of Cubes, Grouping (Algebra 2) | 100 Questions",
         "Polynomial Identities and Factoring",
         "Prove polynomial identities and use them to describe numerical relationships. For example, the polynomial identity (x² + y²)² = (x² − y²)² + (2xy)² can be used to generate Pythagorean triples.",
         "Free Algebra 2 worksheet on factoring polynomials: sum and difference of cubes, grouping, quadratic form, identities, the Binomial Theorem and solving by factoring. 100 questions.",
         "a³ ± b³ = (a ± b)(a² ∓ ab + b²).",
         "Factor completely, then set each factor equal to 0 to solve.",
         body, faq, sets, R, domain="Polynomials", grade="algebra-2")


if __name__ == "__main__":
    build()
