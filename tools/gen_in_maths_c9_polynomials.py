# -*- coding: utf-8 -*-
"""
India Class 9 Maths, NCERT Chapter 2: Polynomials (CBSE Unit II Algebra)
  python3 tools/gen_in_maths_c9_polynomials.py
Polynomials in one variable, degree and types, value p(a) and zeroes, the Factor Theorem and finding k, factorising
quadratics by splitting the middle term and cubics with the Factor Theorem, and algebraic identities
((x ± y)², (x + a)(x + b), (x + y + z)², (x ± y)³, x³ + y³ + z³ − 3xyz) used for products and evaluation.
Wrong answers come from real mistakes: counting terms for the degree, calling x^(1/2) a polynomial, p(−a) for the factor
x − a, sign errors when splitting, (x + y)³ = x³ + y³, and forgetting that a + b + c = 0 gives a³ + b³ + c³ = 3abc.
"""
import random
from fractions import Fraction as F
from in_common import num, S, make, lesson, mix, T, expr, fv

R = random.Random(909002)
X = "<i>x</i>"
SUP = {1: "", 2: "²", 3: "³", 4: "⁴", 5: "⁵"}


def poly(cs):
    return expr([(cs[e], (X + SUP[e]) if e else "") for e in sorted(cs, reverse=True)])


def nz(lo, hi):
    return [k for k in range(lo, hi + 1) if k]


def ev(cs, a):
    return sum(F(c) * F(a) ** e for e, c in cs.items())


def lin(a):
    return "%s %s %s" % (X, "−" if a > 0 else "+", num(abs(a))) if a else X


# ---------------------------------------------------------------- set 1: polynomials and degree
def one_deg(r):
    kind = r.choice(["deg", "deg", "is", "is", "type", "coef"])
    if kind == "deg":
        d = r.randint(1, 5)
        cs = {d: r.choice(nz(-5, 7))}
        for e in r.sample(range(d), min(d, r.randint(1, 3))):
            cs[e] = r.choice(nz(-9, 9))
        n = len(cs)
        return T("What is the degree of %s?" % poly(cs), str(d), [str(n) if n != d else str(d + 1), str(d - 1) if d > 1 else "0", str(max(abs(c) for c in cs.values())) if max(abs(c) for c in cs.values()) != d else str(d + 2)],
                 "The degree is the highest power of %s: <b>%d</b>." % (X, d))
    if kind == "is":
        items = [("4" + X + "² − 3" + X + " + 7", True), (X + "² + √2", True), ("3√" + X + " + 1", False), ("y + 2/y", False),
                 (X + "<sup>10</sup> + y³ + t<sup>50</sup>", False), ("√3 " + X + "² − " + X, True), (X + "<sup>−1</sup> + 3", False), ("5", True),
                 (X + "<sup>1/2</sup> − 2", False), ("(1/2)" + X + "³ − 4", True)]
        e, yes = r.choice(items)
        return T("Is %s a polynomial in one variable?" % e, "Yes" if yes else "No",
                 ["No" if yes else "Yes", "Only if %s &gt; 0" % X, "Yes, but only of degree 0"] if yes else ["Yes", "Yes, of degree 1", "Only if %s &gt; 0" % X],
                 ("All powers of the variable are whole numbers, so <b>yes</b>." if yes else "It has a power that is not a whole number (or more than one variable), so <b>no</b>."))
    if kind == "type":
        d = r.choice([1, 2, 3])
        cs = {d: r.choice(nz(-5, 7)), 0: r.choice(nz(-9, 9))}
        names = {1: "linear", 2: "quadratic", 3: "cubic"}
        return T("Classify %s by its degree." % poly(cs), names[d].capitalize(), [names[k].capitalize() for k in names if k != d] + ["Binomial of degree 0"],
                 "Degree %d: <b>%s</b>. (It also has two terms, so it is a binomial.)" % (d, names[d]))
    cs = {3: r.choice(nz(-5, 7)), 2: r.choice(nz(-9, 9)), 1: r.choice(nz(-9, 9)), 0: r.choice(nz(-9, 9))}
    e = r.choice([2, 1])
    return T("What is the coefficient of %s in %s?" % (X + SUP[e], poly(cs)), num(cs[e]), [num(-cs[e]), num(cs[3]) if cs[3] != cs[e] else num(cs[e] + 1), num(cs[0]) if cs[0] not in (cs[e], -cs[e], cs[3]) else num(cs[e] + 2)],
             "The number multiplying %s is <b>%s</b>." % (X + SUP[e], num(cs[e])))


# ---------------------------------------------------------------- set 2: values and zeroes
def one_val(r):
    kind = r.choice(["val", "val", "zero", "zero", "check"])
    if kind == "val":
        cs = {2: r.choice(nz(-4, 5)), 1: r.choice(nz(-7, 7)), 0: r.choice(nz(-9, 9))}
        if r.random() < 0.4:
            cs = {3: r.choice(nz(-3, 3)), 1: r.choice(nz(-5, 5)), 0: r.choice(nz(-9, 9))}
        a = r.choice(nz(-3, 3))
        v = ev(cs, a)
        return T("Find p(%s) for p(%s) = %s." % (num(a), X, poly(cs)), num(v), [num(ev(cs, -a)), num(sum(cs.values())), num(v + 2 * a) if 2 * a else num(v + 1)],
                 "Substitute %s = %s: <b>%s</b>." % (X, num(a), num(v)))
    if kind == "zero":
        a, b = r.choice(nz(-6, 7)), r.choice(nz(-12, 12))
        z = F(-b, a)
        return T("Find the zero of p(%s) = %s." % (X, expr([(a, X), (b, "")])), fv(z), [fv(-z), fv(F(-a, b)) if F(-a, b) not in (z, -z) else fv(z + 1), num(b) if F(b) not in (z, -z) else fv(z - 1)],
                 "%s = 0 gives %s = <b>%s</b>." % (expr([(a, X), (b, "")]), X, fv(z)))
    p_, q_ = r.sample(nz(-5, 5), 2)
    cs = {2: 1, 1: -(p_ + q_), 0: p_ * q_}
    t = r.choice([p_, -p_])
    ok = ev(cs, t) == 0
    return T("Is %s a zero of p(%s) = %s?" % (num(t), X, poly(cs)), "Yes, because p(%s) = 0" % num(t) if ok else "No, because p(%s) = %s" % (num(t), num(ev(cs, t))),
             ["No, because p(%s) = %s" % (num(t), num(ev(cs, t) + 5)) if ok else "Yes, because p(%s) = 0" % num(t), "Yes, because the constant term is %s" % num(p_ * q_), "No, because %s is negative" % num(t) if t < 0 else "No, zeroes must be negative"],
             "p(%s) = %s, so %s." % (num(t), num(ev(cs, t)), "<b>yes</b>" if ok else "<b>no</b>"))


# ---------------------------------------------------------------- set 3: Factor Theorem
def one_fac(r):
    kind = r.choice(["is", "is", "k", "k"])
    if kind == "is":
        rs = r.sample(nz(-4, 4), 3)
        cs = {3: 1, 2: -sum(rs), 1: rs[0] * rs[1] + rs[1] * rs[2] + rs[0] * rs[2], 0: -rs[0] * rs[1] * rs[2]}
        a = r.choice([rs[0], -rs[0]])
        if -rs[0] in rs and a == -rs[0]:
            return None
        ok = a in rs
        return T("Is (%s) a factor of %s?" % (lin(a), poly(cs)), "Yes, because p(%s) = 0" % num(a) if ok else "No, because p(%s) ≠ 0" % num(a),
                 ["No, because p(%s) ≠ 0" % num(a) if ok else "Yes, because p(%s) = 0" % num(a), "Yes, because p(%s) = 0" % num(-a) if not ok else "No, because p(%s) ≠ 0" % num(-a), "Only if the constant term is divisible by %s" % num(abs(a))],
                 "Factor Theorem: %s is a factor when p(%s) = 0. p(%s) = %s, so <b>%s</b>." % (lin(a), num(a), num(a), num(ev(cs, a)), "yes" if ok else "no"))
    a = r.choice(nz(-3, 3))
    c2, c1 = r.choice(nz(-4, 4)), r.choice(nz(-6, 6))
    d = r.choice([2, 3])
    base = {3: 1, 2: c2} if d == 3 else {2: 1, 1: c1}
    v = ev(base, a)
    k = -v
    desc = poly(base) + " + k"
    return T("Find k if (%s) is a factor of p(%s) = %s." % (lin(a), X, desc), "k = %s" % num(k), ["k = %s" % num(-k) if k else "k = 1", "k = %s" % num(ev(base, -a) * -1) if -ev(base, -a) not in (k, -k) else "k = %s" % num(k + 2), "k = %s" % num(a)] if a not in (k, -k) else ["k = %s" % num(-k) if k else "k = 1", "k = %s" % num(k + 2), "k = %s" % num(k - 2)],
             "p(%s) = 0: %s + k = 0, so <b>k = %s</b>." % (num(a), num(v), num(k)))


# ---------------------------------------------------------------- set 4: factorisation
def one_fct(r):
    kind = r.choice(["split", "split", "split", "cubic"])
    if kind == "split":
        a = r.choice([1, 2, 3, 4, 5, 6])
        p, q = r.choice(nz(-5, 5)), r.choice(nz(-6, 6))
        c1 = r.choice([1, 2, 3]) if a > 1 else 1
        if a % c1:
            return None
        c2 = a // c1
        # (c1 x + p)(c2 x + q)
        b = c1 * q + c2 * p
        c = p * q
        if b == 0:
            return None
        f1 = "(%s)" % expr([(c1, X), (p, "")])
        f2 = "(%s)" % expr([(c2, X), (q, "")])
        ans = f1 + f2
        w = ["(%s)(%s)" % (expr([(c1, X), (-p, "")]), expr([(c2, X), (-q, "")])), "(%s)(%s)" % (expr([(c1, X), (q, "")]), expr([(c2, X), (p, "")])), "(%s)(%s)" % (expr([(c1, X), (p, "")]), expr([(c2, X), (-q, "")]))]
        w = [x for x in w if x != ans and x != f2 + f1]
        if len(w) < 3:
            w.append("(%s)(%s)" % (expr([(a, X), (p, "")]), expr([(1, X), (q, "")])))
        return T("Factorise %s." % poly({2: a, 1: b, 0: c}), ans, w[:3],
                 "Split the middle term: find two numbers with product %s × %s = %s and sum %s. Then group: <b>%s</b>." % (num(a), num(c), num(a * c), num(b), ans))
    rs = r.sample(nz(-4, 5), 3)
    cs = {3: 1, 2: -sum(rs), 1: rs[0] * rs[1] + rs[1] * rs[2] + rs[0] * rs[2], 0: -rs[0] * rs[1] * rs[2]}
    rs = sorted(rs)
    ans = "".join("(%s)" % lin(t) for t in rs)
    return T("Factorise %s using the Factor Theorem." % poly(cs), ans, ["".join("(%s)" % lin(-t) for t in rs), "".join("(%s)" % lin(t) for t in (rs[0], rs[1], -rs[2])), "(%s)(%s)" % (lin(rs[0]), poly({2: 1, 1: -(rs[1] + rs[2]), 0: rs[1] * rs[2] + 1}))],
             "Try factors of the constant term: p(%s) = 0, so (%s) is a factor. Divide and factorise the quadratic: <b>%s</b>." % (num(rs[0]), lin(rs[0]), ans))


# ---------------------------------------------------------------- set 5: identities
def one_id(r):
    kind = r.choice(["num", "num", "cube", "abc", "abc", "xyz", "exp"])
    if kind == "num":
        b = r.choice([100, 1000, 50, 200])
        d = r.randint(1, 9)
        t = r.choice(["sq+", "sq-", "diff"])
        if t == "sq+":
            return T("Evaluate %d² using an identity." % (b + d), num((b + d) ** 2), [num(b * b + d * d), num((b + d) ** 2 - 2 * b * d), num(b * b + b * d + d * d)],
                     "(%d + %d)² = %s + 2 × %d × %d + %d = <b>%s</b>." % (b, d, num(b * b), b, d, d * d, num((b + d) ** 2)))
        if t == "sq-":
            return T("Evaluate %d² using an identity." % (b - d), num((b - d) ** 2), [num(b * b - d * d), num(b * b + d * d), num((b - d) ** 2 + 2 * b * d)],
                     "(%d − %d)² = %s − 2 × %d × %d + %d = <b>%s</b>." % (b, d, num(b * b), b, d, d * d, num((b - d) ** 2)))
        return T("Evaluate %d × %d using an identity." % (b + d, b - d), num(b * b - d * d), [num(b * b + d * d), num(b * b - 2 * d), num(b * b)],
                 "(a + b)(a − b) = a² − b²: %s − %d = <b>%s</b>." % (num(b * b), d * d, num(b * b - d * d)))
    if kind == "cube":
        a = r.choice([99, 101, 102, 98, 999, 1001])
        b = 100 if a < 500 else 1000
        d = a - b
        return T("Evaluate %d³ using an identity." % a, num(a ** 3), [num(b ** 3 + d ** 3), num(a ** 3 + 3 * b * d), num(b ** 3 + 3 * b * b * d)],
                 "(%d %s %d)³ = %d³ %s 3 × %d² × %d + 3 × %d × %d² %s %d³ = <b>%s</b>." % (b, "+" if d > 0 else "−", abs(d), b, "+" if d > 0 else "−", b, abs(d), b, abs(d), "+" if d > 0 else "−", abs(d), num(a ** 3)))
    if kind == "abc":
        a, b = r.sample(nz(-15, 15), 2)
        c = -(a + b)
        if c == 0:
            return None
        v = 3 * a * b * c
        return T("Find %s³ + %s³ + %s³ without cubing the numbers." % (num(a) if a > 0 else "(%s)" % num(a), num(b) if b > 0 else "(%s)" % num(b), num(c) if c > 0 else "(%s)" % num(c)), num(v),
                 [num(a * b * c), num(-v), "0"],
                 "%s + %s + %s = 0, so a³ + b³ + c³ = 3abc = 3 × %s × %s × %s = <b>%s</b>." % (pr(a), pr(b), pr(c), pr(a), pr(b), pr(c), num(v)))
    if kind == "xyz":
        p, q, s = r.sample([1, 2, 3, 4, -1, -2, -3], 3)
        e = "(%s)²" % expr([(p, X), (q, "<i>y</i>"), (s, "<i>z</i>")])
        cross = 2 * p * q
        return T("In the expansion of %s, what is the coefficient of %s<i>y</i>?" % (e, X), num(cross), [num(p * q), num(p + q), num(2 * p * s) if 2 * p * s != cross else num(cross + 1)],
                 "(x + y + z)² = x² + y² + z² + 2xy + 2yz + 2zx. The %s<i>y</i> term is 2 × (%s) × (%s) = <b>%s</b>." % (X, num(p), num(q), num(cross)))
    a = r.randint(1, 5)
    return T("Expand (%s + %d)³." % (X, a), poly({3: 1, 2: 3 * a, 1: 3 * a * a, 0: a ** 3}),
             [poly({3: 1, 0: a ** 3}), poly({3: 1, 2: a, 1: a * a, 0: a ** 3}), poly({3: 1, 2: 3 * a, 1: 3 * a, 0: a ** 3})],
             "(x + y)³ = x³ + 3x²y + 3xy² + y³, so <b>%s</b>. It is not x³ + y³." % poly({3: 1, 2: 3 * a, 1: 3 * a * a, 0: a ** 3}))


def pr(v):
    return "(%s)" % num(v) if v < 0 else num(v)


def main():
    seen = set()
    sets = [
        S("Polynomials, degree and coefficients", mix(R, [(one_deg, 20)], seen)),
        S("Values and zeroes", mix(R, [(one_val, 20)], seen)),
        S("Factor Theorem", mix(R, [(one_fac, 20)], seen)),
        S("Factorisation", mix(R, [(one_fct, 20)], seen)),
        S("Algebraic identities", mix(R, [(one_id, 20)], seen)),
    ]
    body = lesson(
        "<p>A <b>polynomial</b> in x has only whole-number powers of x. Its <b>degree</b> is the highest power. A <b>zero</b> of p(x) is a value a with p(a) = 0.</p>"
        "<p><b>Factor Theorem</b>: (x − a) is a factor of p(x) exactly when p(a) = 0.</p>"
        "<p>Identities: (x + y)² = x² + 2xy + y², x² − y² = (x + y)(x − y), (x + y)³ = x³ + y³ + 3xy(x + y), x³ + y³ + z³ − 3xyz = (x + y + z)(x² + y² + z² − xy − yz − zx).</p>",
        [("Is (x + 1) a factor of x³ + x² + x + 1?", ["p(−1) = −1 + 1 − 1 + 1 = 0"], "Yes"),
         ("Factorise 6x² + 17x + 5.", ["6 × 5 = 30 = 15 × 2, 15 + 2 = 17", "6x² + 15x + 2x + 5 = 3x(2x + 5) + (2x + 5)"], "(3x + 1)(2x + 5)")],
        ["Finding the degree by counting terms. Use the highest power.",
         "Testing p(a) for the factor (x + a). For x + a, test p(−a).",
         "Writing (x + y)³ = x³ + y³. The middle terms 3x²y + 3xy² are missing."])
    faq = [
        ("What is the Factor Theorem?", "If p(a) = 0 then (x − a) is a factor of p(x), and if (x − a) is a factor then p(a) = 0."),
        ("How do I factorise ax² + bx + c by splitting the middle term?", "Find two numbers whose product is ac and whose sum is b, rewrite bx as the sum of two terms, then factorise in pairs."),
        ("What is the zero of a linear polynomial ax + b?", "x = −b/a."),
        ("If a + b + c = 0, what is a³ + b³ + c³?", "3abc, from the identity a³ + b³ + c³ − 3abc = (a + b + c)(a² + b² + c² − ab − bc − ca)."),
    ]
    make(9, "polynomials", 2, "II", 2, "Polynomials: Zeroes, Factor Theorem and Identities", "polynomials",
         "Definition of a polynomial in one variable, coefficients, terms and zero polynomial; degree; constant, linear, quadratic and cubic polynomials; monomials, binomials, trinomials; factors and multiples; zeros of a polynomial; the Factor Theorem; factorisation of ax² + bx + c and of cubic polynomials using the Factor Theorem; algebraic identities including (x + y + z)², (x ± y)³ and x³ + y³ + z³ − 3xyz (summary of the CBSE syllabus)",
         "Class 9 Polynomials worksheet (NCERT Chapter 2): degree and coefficients, values and zeroes, Factor Theorem, factorisation and algebraic identities. 100 questions with answers.",
         "p(a) = 0 ⇔ (x − a) is a factor", "Factor Theorem: test a value to find a factor.",
         body, faq, sets, R)


if __name__ == "__main__":
    main()
