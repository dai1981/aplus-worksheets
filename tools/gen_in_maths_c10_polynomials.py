# -*- coding: utf-8 -*-
"""
India Class 10 Maths, NCERT Chapter 2: Polynomials (CBSE Unit II Algebra)
  python3 tools/gen_in_maths_c10_polynomials.py
Degree and zeroes, number of zeroes from a graph, zeroes of a quadratic polynomial by factorisation, relationship between
zeroes and coefficients (α + β = −b/a, αβ = c/a), forming a quadratic polynomial from the sum and product of its zeroes,
expressions in α and β, finding k, and the cubic relationships.
Wrong answers come from real mistakes: α + β = b/a (sign lost), αβ = −c/a, counting turning points as zeroes,
x² − (product)x + (sum), and α² + β² = (α + β)².
"""
import random
from fractions import Fraction as F
from in_common import num, S, make, lesson, mix, T, expr, fv, MINUS
from pc_common import curve_svg

R = random.Random(910002)
X = "<i>x</i>"
X2 = X + "²"
X3 = X + "³"
AL, BE, GA = "α", "β", "γ"


def quad(a, b, c, v=X):
    return expr([(a, v + "²"), (b, v), (c, "")])


def nz(lo=-9, hi=9):
    return [k for k in range(lo, hi + 1) if k != 0]


def zs(vals):
    vals = sorted(set(F(t) for t in vals))
    return " and ".join(fv(t) for t in vals)


# ---------------------------------------------------------------- set 1: degree and zeroes from a graph
def one_graph(r):
    kind = r.choice(["graph", "graph", "graph", "deg", "max"])
    if kind == "graph":
        n = r.choice([0, 1, 2, 3, 2, 3])
        if n == 0:
            a, k = r.choice([1, -1]), r.choice([1, 2, 3])
            fn = lambda x: a * (x * x / 2 + k)
            tp = "quadratic"
        elif n == 1:
            p = r.choice([-2, -1, 1, 2])
            if r.random() < 0.5:
                fn = lambda x: 0.5 * (x - p) ** 2
                tp = "quadratic (touches the x-axis)"
            else:
                fn = lambda x: 0.15 * (x - p) ** 3
                tp = "cubic"
        elif n == 2:
            p, q = sorted(r.sample([-4, -3, -2, -1, 1, 2, 3, 4], 2))
            s = r.choice([1, -1])
            fn = lambda x: s * 0.4 * (x - p) * (x - q)
            tp = "quadratic"
        else:
            p, q, t = sorted(r.sample([-4, -3, -2, -1, 0, 1, 2, 3, 4], 3))
            s = r.choice([1, -1])
            fn = lambda x: s * 0.12 * (x - p) * (x - q) * (x - t)
            tp = "cubic"
        pic = curve_svg(fn, -5, 5, -5, 5, unit=24, label="graph of y = p(x)")
        wr = [str(k) for k in (0, 1, 2, 3, 4) if k != n]
        r.shuffle(wr)
        return T(pic + "The graph of y = p(%s) is shown. How many zeroes does p(%s) have?" % (X, X), str(n), wr[:3],
                 "The zeroes are the %s-coordinates of the points where the graph meets the %s-axis. It meets it at <b>%d</b> point%s." % (X, X, n, "" if n == 1 else "s"))
    if kind == "deg":
        d = r.choice([1, 2, 3, 4])
        terms = [(r.choice([2, 3, -1, 5, -4]), "")]
        if d >= 1:
            terms.insert(0, (r.choice([3, -2, 7, 1]), X))
        if d >= 2:
            terms.insert(0, (r.choice([1, -5, 4, 2]), X2))
        if d >= 3:
            terms.insert(0, (r.choice([2, -1, 6]), X3))
        if d == 4:
            terms.insert(0, (r.choice([1, -3]), X + "⁴"))
        names = {1: "linear", 2: "quadratic", 3: "cubic", 4: "biquadratic"}
        return T("What is the degree of p(%s) = %s?" % (X, expr(terms)), "%d (%s)" % (d, names[d]),
                 ["%d (%s)" % (k, names[k]) for k in names if k != d][:3],
                 "The degree is the highest power of %s: <b>%d</b>." % (X, d))
    d = r.choice([1, 2, 3])
    return T("A polynomial of degree %d can have at most how many zeroes?" % d, str(d), [str(d + 1), str(d - 1) if d > 1 else "infinitely many", str(2 * d)],
             "A polynomial of degree n has at most n zeroes: <b>%d</b>." % d)


# ---------------------------------------------------------------- set 2: zeroes by factorisation
def one_zero(r):
    kind = r.choice(["monic", "monic", "nonmonic", "common", "dos"])
    v = r.choice([X, "<i>t</i>", "<i>u</i>", "<i>s</i>", X])
    if kind == "monic":
        p, q = r.sample(nz(), 2)
        poly = quad(1, -(p + q), p * q, v)
        return T("Find the zeroes of %s." % poly, zs([p, q]), [zs([-p, -q]), zs([p, -q]) if p != q else zs([p + 1]), zs([p + q, p * q]) if {p + q, p * q} != {p, q} else zs([p - 1, q + 1])],
                 "Find two numbers with product %s and sum %s: (%s)(%s). Zeroes: <b>%s</b>." % (num(p * q), num(-(p + q)), expr([(1, v), (-p, "")]), expr([(1, v), (-q, "")]), zs([p, q])))
    if kind == "nonmonic":
        a = r.choice([2, 3, 4, 5, 6])
        p = F(r.choice(nz(-5, 5)), a)
        q = r.choice(nz(-6, 6))
        if p.denominator == 1:
            return None
        b = -(a * p + a * q)
        c = a * p * q
        if b.denominator != 1 or c.denominator != 1:
            return None
        poly = quad(a, b, c, v)
        return T("Find the zeroes of %s." % poly, zs([p, q]), [zs([-p, -q]), zs([1 / p, q]), zs([p * a, q])],
                 "Split the middle term and factorise: the zeroes are <b>%s</b>. Check: sum = %s = −(%s)/%d, product = %s = %s/%d." % (
                     zs([p, q]), fv(p + q), num(b), a, fv(p * q), num(c), a))
    if kind == "common":
        a = r.choice([2, 3, 4, 5])
        k = r.choice(nz(-8, 8))
        poly = expr([(a, v + "²"), (-a * k, v)])
        return T("Find the zeroes of %s." % poly, zs([0, k]), [zs([k]), zs([0, -k]), zs([-k])],
                 "Take out the common factor: %s%s(%s) = 0, so <b>%s</b>. Do not lose the zero 0." % (num(a), v, expr([(1, v), (-k, "")]), zs([0, k])))
    a = r.choice([1, 4, 9, 1, 25])
    m = r.choice([1, 2, 3, 4, 5, 6])
    c = m * m
    s = int(a ** 0.5)
    poly = expr([(a, v + "²"), (-c, "")])
    z = F(m, s)
    return T("Find the zeroes of %s." % poly, zs([z, -z]), [zs([z]), zs([F(c, a)]) if F(c, a) != z else zs([z * 2]), "no real zeroes"],
             "Difference of squares: (%s)(%s) = 0, so <b>%s</b>." % (expr([(s, v), (-m, "")]), expr([(s, v), (m, "")]), zs([z, -z])))


# ---------------------------------------------------------------- set 3: sum and product of zeroes
def one_rel(r):
    a = r.choice([1, 1, 2, 3, 4, 5, -1, -2])
    b = r.choice(nz(-12, 12))
    c = r.choice(nz(-15, 15))
    if b * b - 4 * a * c < 0:
        return None
    poly = quad(a, b, c)
    kind = r.choice(["sum", "prod", "both"])
    if kind == "sum":
        return T("If α and β are the zeroes of %s, find α + β." % poly, fv(F(-b, a)), [fv(F(b, a)), fv(F(c, a)) if F(c, a) not in (F(-b, a), F(b, a)) else fv(F(-b, a) + 1), fv(F(-a, b)) if F(-a, b) not in (F(-b, a), F(b, a)) else fv(F(-b, a) - 1)],
                 "α + β = −(coefficient of %s)/(coefficient of %s²) = −(%s)/%s = <b>%s</b>." % (X, X, num(b), num(a) if a > 0 else "(%s)" % num(a), fv(F(-b, a))))
    if kind == "prod":
        return T("If α and β are the zeroes of %s, find αβ." % poly, fv(F(c, a)), [fv(F(-c, a)), fv(F(-b, a)) if F(-b, a) not in (F(c, a), F(-c, a)) else fv(F(c, a) + 1), fv(F(a, c)) if F(a, c) not in (F(c, a), F(-c, a)) else fv(F(c, a) - 1)],
                 "αβ = constant term / coefficient of %s² = %s/%s = <b>%s</b>." % (X, num(c), num(a) if a > 0 else "(%s)" % num(a), fv(F(c, a))))
    sm, pr = F(-b, a), F(c, a)
    return T("For %s, which is correct?" % poly, "α + β = %s, αβ = %s" % (fv(sm), fv(pr)),
             ["α + β = %s, αβ = %s" % (fv(-sm), fv(pr)), "α + β = %s, αβ = %s" % (fv(sm), fv(-pr)), "α + β = %s, αβ = %s" % (fv(pr), fv(sm)) if pr != sm else "α + β = %s, αβ = %s" % (fv(-sm), fv(-pr))],
             "α + β = −b/a = <b>%s</b>, αβ = c/a = <b>%s</b>." % (fv(sm), fv(pr)))


# ---------------------------------------------------------------- set 4: forming a quadratic polynomial
def one_form(r):
    kind = r.choice(["sp", "sp", "zeroes", "zeroes", "frac"])
    if kind == "sp":
        sm, pr = r.choice(nz(-9, 9)), r.choice(nz(-12, 12))
        ans = quad(1, -sm, pr)
        return T("Find a quadratic polynomial whose zeroes have sum %s and product %s." % (num(sm), num(pr)), ans,
                 [quad(1, sm, pr), quad(1, -pr, sm), quad(1, sm, -pr)],
                 "x² − (sum)x + (product) = <b>%s</b> (or any non-zero multiple of it)." % ans)
    if kind == "zeroes":
        p, q = r.sample(nz(-7, 7), 2)
        ans = quad(1, -(p + q), p * q)
        return T("Find a quadratic polynomial whose zeroes are %s and %s." % (num(p), num(q)), ans,
                 [quad(1, p + q, p * q), quad(1, -(p + q), -p * q) if p * q != 0 else quad(1, p + q, 1), quad(1, -p * q, p + q) if p + q != 0 else quad(1, -p * q, 1)],
                 "Sum = %s, product = %s. Polynomial: <b>%s</b>." % (num(p + q), num(p * q), ans))
    d = r.choice([2, 3, 4])
    sm = F(r.choice(nz(-5, 5)), d)
    pr = F(r.choice(nz(-5, 5)), d)
    if sm.denominator == 1 or pr.denominator == 1:
        return None
    L = d
    ans = quad(L, -sm * L, pr * L)
    return T("Find a quadratic polynomial with integer coefficients whose zeroes have sum %s and product %s." % (fv(sm), fv(pr)), ans,
             [quad(L, sm * L, pr * L), quad(L, -pr * L, sm * L), quad(1, -sm * L, pr * L)],
             "k(x² − (%s)x + (%s)) with k = %d gives <b>%s</b>." % (fv(sm), fv(pr), L, ans))


# ---------------------------------------------------------------- set 5: expressions, finding k and cubics
def one_app(r):
    kind = r.choice(["sq", "inv", "k", "k", "cubic", "cubic"])
    if kind in ("sq", "inv"):
        a = r.choice([1, 1, 2])
        b = r.choice(nz(-9, 9))
        c = r.choice(nz(-9, 9))
        if b * b - 4 * a * c < 0:
            return None
        sm, pr = F(-b, a), F(c, a)
        poly = quad(a, b, c)
        if kind == "sq":
            v_ = sm * sm - 2 * pr
            return T("If α and β are the zeroes of %s, find α² + β²." % poly, fv(v_), [fv(sm * sm), fv(sm * sm + 2 * pr), fv(sm * sm - pr) if sm * sm - pr != v_ else fv(v_ + 1)],
                     "α² + β² = (α + β)² − 2αβ = (%s)² − 2(%s) = <b>%s</b>." % (fv(sm), fv(pr), fv(v_)))
        v_ = sm / pr
        return T("If α and β are the zeroes of %s, find 1/α + 1/β." % poly, fv(v_), [fv(pr / sm), fv(-v_), fv(1 / sm) if 1 / sm not in (v_, -v_, pr / sm) else fv(v_ + 1)],
                 "1/α + 1/β = (α + β)/(αβ) = %s ÷ %s = <b>%s</b>." % (fv(sm), fv(pr), fv(v_)))
    if kind == "k":
        z = r.choice(nz(-5, 5))
        b = r.choice(nz(-8, 8))
        k = -(z * z + b * z)
        if k == 0:
            return None
        poly = "%s + k" % expr([(1, X2), (b, X)])
        return T("If %s is a zero of p(%s) = %s, find k." % (num(z), X, poly), num(k), [num(-k), num(z * z + b * z - z) if z * z + b * z - z not in (k, -k) else num(k + 1), num(z)],
                 "p(%s) = 0: (%s)² + (%s)(%s) + k = 0, so k = <b>%s</b>." % (num(z), num(z), num(b), num(z), num(k)))
    p, q, t = r.sample(nz(-4, 4), 3)
    a = r.choice([1, 1, 2])
    s1, s2, s3 = p + q + t, p * q + q * t + t * p, p * q * t
    poly = expr([(a, X3), (-a * s1, X2), (a * s2, X), (-a * s3, "")])
    which = r.choice(["sum", "prod", "pair"])
    if which == "sum":
        return T("The zeroes of %s are α, β, γ. Find α + β + γ." % poly, fv(s1), [fv(-s1) if s1 else "1", fv(s3) if s3 != s1 else fv(s1 + 2), fv(s2) if s2 not in (s1, -s1, s3) else fv(s1 - 2)],
                 "α + β + γ = −b/a = <b>%s</b>." % fv(s1))
    if which == "prod":
        return T("The zeroes of %s are α, β, γ. Find αβγ." % poly, fv(s3), [fv(-s3), fv(s1) if s1 not in (s3, -s3) else fv(s3 + 2), fv(s2) if s2 not in (s3, -s3, s1) else fv(s3 - 2)],
                 "αβγ = −d/a = <b>%s</b>." % fv(s3))
    return T("The zeroes of %s are α, β, γ. Find αβ + βγ + γα." % poly, fv(s2), [fv(-s2) if s2 else "1", fv(s1) if s1 not in (s2, -s2) else fv(s2 + 3), fv(s3) if s3 not in (s2, -s2, s1) else fv(s2 - 3)],
             "αβ + βγ + γα = c/a = <b>%s</b>." % fv(s2))


def main():
    seen = set()
    sets = [
        S("Degree and zeroes from a graph", mix(R, [(one_graph, 20)], seen)),
        S("Zeroes of a quadratic polynomial", mix(R, [(one_zero, 20)], seen)),
        S("Sum and product of zeroes", mix(R, [(one_rel, 20)], seen)),
        S("Forming a quadratic polynomial", mix(R, [(one_form, 20)], seen)),
        S("Expressions in α and β, finding k, cubics", mix(R, [(one_app, 20)], seen)),
    ]
    body = lesson(
        "<p>A <b>zero</b> of p(x) is a value of x with p(x) = 0. On the graph of y = p(x), the zeroes are where the graph meets the x-axis.</p>"
        "<p>A polynomial of degree n has at most n zeroes.</p>"
        "<p>For ax² + bx + c with zeroes α and β: <b>α + β = −b/a</b> and <b>αβ = c/a</b>.</p>"
        "<p>A quadratic with given zeroes: x² − (sum of zeroes)x + (product of zeroes).</p>",
        [("Find the zeroes of x² − 2x − 8 and check the relationship.", ["x² − 2x − 8 = (x − 4)(x + 2)", "Zeroes 4 and −2", "Sum 2 = −(−2)/1, product −8 = −8/1"], "4 and −2"),
         ("Find a quadratic polynomial with sum of zeroes 1/4 and product −1.", ["x² − ¼x − 1", "Multiply by 4"], "4x² − x − 4")],
        ["Writing α + β = b/a. The sign changes: α + β = −b/a.",
         "Counting the turning points of a graph instead of the points on the x-axis.",
         "Using α² + β² = (α + β)². It is (α + β)² − 2αβ."])
    faq = [
        ("What are the zeroes of a polynomial?", "The values of x that make p(x) = 0. Geometrically, they are the x-coordinates where the graph of y = p(x) meets the x-axis."),
        ("What is the relationship between the zeroes and coefficients of a quadratic polynomial?", "For ax² + bx + c, sum of zeroes = −b/a and product of zeroes = c/a."),
        ("How do I find a quadratic polynomial from the sum and product of its zeroes?", "Use x² − (sum)x + (product), then multiply by a number to clear fractions if needed."),
        ("How many zeroes can a cubic polynomial have?", "At most 3. Its graph meets the x-axis at 1, 2 or 3 points."),
    ]
    make(10, "polynomials", 2, "II", 2, "Polynomials: Zeroes and Coefficients", "polynomials",
         "Zeros of a polynomial; relationship between zeros and coefficients of quadratic polynomials (summary of the CBSE syllabus)",
         "Class 10 Polynomials worksheet (NCERT Chapter 2): zeroes from graphs, zeroes of quadratics, sum and product of zeroes, forming polynomials and α, β expressions. 100 questions with answers.",
         "α + β = −b/a, αβ = c/a", "For ax² + bx + c with zeroes α and β.",
         body, faq, sets, R)


if __name__ == "__main__":
    main()
