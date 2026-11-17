# -*- coding: utf-8 -*-
"""
UK Year 8 Maths: Expanding and Factorising (KS3 Algebra)
  python3 tools/gen_uk_maths_y8_expanding_and_factorising.py
Expanding single brackets with algebraic terms outside, expanding and simplifying, expanding a pair of
binomials, factorising with a numerical and algebraic HCF, and problems with areas and identities.
Wrong answers come from real mistakes: multiplying only the first term, sign errors with a negative
outside, missing the middle terms in (x + a)(x + b), and taking out a common factor that is not the highest.
"""
import random
from math import gcd
from uk_ks3 import num, B, S, make, lesson, collect, T, expr, MINUS

R = random.Random(80301)
VS = ["<i>x</i>", "<i>a</i>", "<i>y</i>", "<i>p</i>", "<i>n</i>", "<i>m</i>", "<i>t</i>"]


def sq(v):
    return v + "<sup>2</sup>"


def poly(c2, c1, c0, v):
    return expr([(c2, sq(v)), (c1, v), (c0, "")])


def nz(r, lo, hi):
    while True:
        k = r.randint(lo, hi)
        if k:
            return k


def br(a, b, v):
    """(a v + b) shown as a bracket"""
    return "(%s)" % expr([(a, v), (b, "")])


def mono(c, v, p=1):
    if p == 0:
        return num(c)
    vv = v if p == 1 else sq(v)
    return expr([(c, vv)])


# ------------------------------------------------------------ set 1: single brackets with letters outside
def one_single(r):
    v = r.choice(VS)
    k = r.choice([1, 2, 3, 4, 5, -1, -2, -3])
    a, b = r.randint(1, 5), nz(r, -9, 9)
    outside = mono(k, v)
    q = "Expand %s." % B("%s%s" % (outside, br(a, b, v)))
    right = poly(k * a, k * b, 0, v)
    wr = [poly(k * a, b, 0, v),                         # only first term
          poly(0, k * a + k * b, 0, v) if k * a + k * b else poly(k * a, 0, k * b, v),   # no square
          poly(k * a, -k * b, 0, v),                    # sign slip
          expr([(k * a, sq(v)), (k * b, "")])]          # forgot the letter on second term
    e = "Multiply each term by %s: %s × %s = %s and %s × %s = %s. So <b>%s</b>." % (
        outside, outside, mono(a, v), mono(k * a, v, 2), outside, num(b) if b > 0 else "(%s)" % num(b), mono(k * b, v), right)
    return T(q, right, [w for w in wr if w != right][:3], e)


# ------------------------------------------------------------ set 2: expand and simplify
def one_simplify(r):
    v = r.choice(VS)
    k1, k2 = r.randint(2, 6), r.choice([2, 3, 4, 5, -2, -3, -4])
    a1, b1, a2, b2 = r.randint(1, 4), nz(r, -7, 7), r.randint(1, 4), nz(r, -7, 7)
    X, C = k1 * a1 + k2 * a2, k1 * b1 + k2 * b2
    if X == 0:
        return None
    s2 = (" + %d" % k2) if k2 > 0 else (" %s %d" % (MINUS, -k2))
    q = "Expand and simplify %s." % B("%d%s%s%s" % (k1, br(a1, b1, v), s2, br(a2, b2, v)))
    right = expr([(X, v), (C, "")])
    wr = [expr([(X, v), (k1 * b1 + b2, "")]),                    # second bracket only first term
          expr([(k1 * a1 - k2 * a2 if k2 < 0 else X, v), (k1 * b1 - k2 * b2, "")]) if k2 < 0 else expr([(X, v), (C + 2 * k2 * b2, "")]),
          expr([(X, v), (-C, "")]) if C else expr([(X + 1, v)]),
          expr([(X + C, v)])]
    e = "%s and %s. Collect like terms: <b>%s</b>." % (expr([(k1 * a1, v), (k1 * b1, "")]), expr([(k2 * a2, v), (k2 * b2, "")]), right)
    return T(q, right, [w for w in wr if w != right][:3], e)


# ------------------------------------------------------------ set 3: double brackets
def one_double(r):
    v = r.choice(VS)
    a, b = nz(r, -9, 9), nz(r, -9, 9)
    if r.random() < 0.25:
        c = r.choice([2, 3])
        q = "Expand and simplify %s." % B("(%s)(%s)" % (expr([(c, v), (a, "")]), expr([(1, v), (b, "")])))
        right = poly(c, c * b + a, a * b, v)
        wr = [poly(c, 0, a * b, v), poly(c, a + b, a * b, v), poly(c, c * b + a, a + b, v)]
        e = "Multiply every term: %s, %s, %s and %s. Collect: <b>%s</b>." % (
            mono(c, v, 2), mono(c * b, v), mono(a, v), num(a * b), right)
        return T(q, right, [w for w in wr if w != right], e)
    if r.random() < 0.25:
        q = "Expand %s." % B("(%s)<sup>2</sup>" % expr([(1, v), (a, "")]))
        right = poly(1, 2 * a, a * a, v)
        wr = [poly(1, 0, a * a, v), poly(1, a, a * a, v), poly(1, 2 * a, 2 * a, v)]
        e = "(%s)<sup>2</sup> = (%s)(%s) = %s + %s + %s + %s = <b>%s</b>. Do not forget the middle terms." % (
            expr([(1, v), (a, "")]), expr([(1, v), (a, "")]), expr([(1, v), (a, "")]), sq(v), mono(a, v), mono(a, v), num(a * a), right)
        e = e.replace("+ " + MINUS, MINUS + " ")
        return T(q, right, wr, e)
    q = "Expand and simplify %s." % B("(%s)(%s)" % (expr([(1, v), (a, "")]), expr([(1, v), (b, "")])))
    right = poly(1, a + b, a * b, v)
    wr = [poly(1, 0, a * b, v), poly(1, a * b, a + b, v), poly(1, a + b, a + b, v), poly(1, a - b if a != b else 2 * a, a * b, v)]
    e = "Use a grid or FOIL: %s + %s + %s + %s. Collect the middle terms: <b>%s</b>." % (
        sq(v), mono(b, v), mono(a, v), num(a * b), right)
    e = e.replace("+ " + MINUS, MINUS + " ")
    return T(q, right, [w for w in wr if w != right][:3], e)


# ------------------------------------------------------------ set 4: factorising
def one_factor(r):
    v = r.choice(VS)
    kind = r.random()
    if kind < 0.45:
        h = r.choice([2, 3, 4, 5, 6, 7, 8])
        a, b = r.randint(1, 6), nz(r, -9, 9)
        if gcd(a, abs(b)) != 1:
            return None
        q = "Factorise fully %s." % B(expr([(h * a, v), (h * b, "")]))
        right = "%d%s" % (h, br(a, b, v))
        smaller = [d for d in range(2, h) if h % d == 0]
        wr = ["%d%s" % (smaller[-1], br(h * a // smaller[-1], h * b // smaller[-1], v)) if smaller else "%d%s" % (h, br(a, -b, v)),
              "%d%s" % (h, br(a, -b, v)), "%d%s" % (h, br(a, h * b, v)), "%s%s" % (mono(h, v), br(a, b, ""))]
        e = "The HCF of %d and %d is %d: <b>%s</b>. Check by expanding." % (h * a, abs(h * b), h, right)
        return T(q, right, [w for w in wr if w != right][:3], e)
    h = r.choice([1, 2, 3, 4, 5])
    a, b = r.randint(1, 5), nz(r, -9, 9)
    if gcd(a, abs(b)) != 1:
        return None
    q = "Factorise fully %s." % B(poly(h * a, h * b, 0, v))
    outside = mono(h, v)
    right = "%s%s" % (outside, br(a, b, v))
    wr = ["%s%s" % (v, br(h * a, h * b, v)) if h > 1 else "%s%s" % (v, br(a, b, "")),
          "%d%s" % (h, "(%s)" % expr([(a, sq(v)), (b, v)])) if h > 1 else "%s(%s)" % (sq(v), expr([(a, ""), (b, "")])),
          "%s%s" % (outside, br(a, -b, v)), "%s%s" % (mono(h, v, 2), br(a, b, ""))]
    e = "Both terms contain %s%s. Take out %s: <b>%s</b>." % (num(h) if h > 1 else "", v, outside, right)
    return T(q, right, [w for w in wr if w != right][:3], e)


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    X = "<i>x</i>"
    data = [
        ("A rectangle is (%s + 3) cm long and %s cm wide. Which expression gives its area?" % (X, X), poly(1, 3, 0, X), [poly(0, 1, 3, X), "2%s + 3" % X, poly(0, 4, 6, X)],
         "Area = %s(%s + 3) = <b>%s</b>." % (X, X, poly(1, 3, 0, X))),
        ("A rectangle is (%s + 5) cm by (%s + 2) cm. Which expression gives its area?" % (X, X), poly(1, 7, 10, X), [poly(1, 0, 10, X), poly(0, 4, 14, X), poly(1, 7, 7, X)],
         "(%s + 5)(%s + 2) = %s + 2%s + 5%s + 10 = <b>%s</b>." % (X, X, sq(X), X, X, poly(1, 7, 10, X))),
        ("A rectangle is (%s + 5) cm by (%s + 2) cm. Which expression gives its perimeter?" % (X, X), poly(0, 4, 14, X), [poly(1, 7, 10, X), poly(0, 2, 7, X), poly(0, 4, 7, X)],
         "2(%s + 5) + 2(%s + 2) = <b>%s</b>." % (X, X, poly(0, 4, 14, X))),
        ("Which expression is equivalent to 3(2%s − 4)?" % X, "6%s − 12" % X, ["6%s − 4" % X, "5%s − 7" % X, "6%s + 12" % X], "3 × 2%s = 6%s and 3 × (−4) = −12: <b>6%s − 12</b>." % (X, X, X)),
        ("Ruby expands (%s + 4)<sup>2</sup> and gets %s + 16. What is the correct answer?" % (X, sq(X)), poly(1, 8, 16, X), [poly(1, 4, 16, X), poly(1, 16, 16, X), poly(2, 8, 16, X)],
         "(%s + 4)(%s + 4) = %s + 4%s + 4%s + 16 = <b>%s</b>. Ruby missed the middle terms." % (X, X, sq(X), X, X, poly(1, 8, 16, X))),
        ("Which is the full factorisation of 12%s + 18?" % X, "6(2%s + 3)" % X, ["3(4%s + 6)" % X, "2(6%s + 9)" % X, "6(2%s + 18)" % X], "The HCF of 12 and 18 is 6: <b>6(2%s + 3)</b>." % X),
        ("Factorise fully 8%s − 12%s." % (sq(X), X), "4%s(2%s − 3)" % (X, X), ["4(2%s − 3%s)" % (sq(X), X), "2%s(4%s − 6)" % (X, X), "4%s(2%s − 3)" % (sq(X), X)],
         "The HCF of 8%s and 12%s is 4%s: <b>4%s(2%s − 3)</b>." % (sq(X), X, X, X, X)),
        ("Expand %s." % B("(%s − 3)(%s + 3)" % (X, X)), poly(1, 0, -9, X), [poly(1, -6, -9, X), poly(1, 6, -9, X), poly(1, 0, 9, X)],
         "%s + 3%s − 3%s − 9 = <b>%s</b>. The middle terms cancel." % (sq(X), X, X, poly(1, 0, -9, X))),
        ("Expand %s." % B("(%s − 2)(%s − 5)" % (X, X)), poly(1, -7, 10, X), [poly(1, -7, -10, X), poly(1, 7, 10, X), poly(1, -3, 10, X)],
         "%s − 5%s − 2%s + 10 = <b>%s</b>. (−2) × (−5) = +10." % (sq(X), X, X, poly(1, -7, 10, X))),
        ("Simplify %s." % B("%s(%s + 2) + 3(%s + 2)" % (X, X, X)), poly(1, 5, 6, X), [poly(1, 5, 2, X), poly(0, 4, 8, X), poly(1, 2, 6, X)],
         "%s + 2%s + 3%s + 6 = <b>%s</b>." % (sq(X), X, X, poly(1, 5, 6, X))),
        ("Which pair of brackets expands to %s?" % B(poly(1, 5, 6, X)), "(%s + 2)(%s + 3)" % (X, X), ["(%s + 1)(%s + 6)" % (X, X), "(%s + 5)(%s + 1)" % (X, X), "(%s + 6)(%s − 1)" % (X, X)],
         "We need two numbers that multiply to 6 and add to 5: 2 and 3. So <b>(%s + 2)(%s + 3)</b>." % (X, X)),
        ("Is %s + 10 the same as 2(%s + 5)?" % ("2" + X, X), "Yes, for every value of " + X, ["No, never", "Only when " + X + " = 0", "Only when " + X + " = 5"],
         "2(%s + 5) = 2%s + 10, so they are equal <b>for every value</b>. This is an identity." % (X, X)),
        ("The area of a rectangle is 6%s + 15 and its width is 3. What is its length?" % X, "2%s + 5" % X, ["6%s + 12" % X, "2%s + 15" % X, "3%s + 5" % X], "6%s + 15 = 3(2%s + 5), so the length is <b>2%s + 5</b>." % (X, X, X)),
        ("Expand %s." % B("−4(3 − 2%s)" % X), "−12 + 8%s" % X, ["−12 − 8%s" % X, "12 − 8%s" % X, "−12 + 2%s" % X], "−4 × 3 = −12 and −4 × (−2%s) = +8%s: <b>−12 + 8%s</b>." % (X, X, X)),
        ("Expand and simplify %s." % B("5(%s + 2) − 2(%s − 3)" % (X, X)), "3%s + 16" % X, ["3%s + 4" % X, "3%s + 13" % X, "7%s + 16" % X], "5%s + 10 − 2%s + 6 = <b>3%s + 16</b>." % (X, X, X)),
        ("Factorise %s." % B("%s<i>y</i> + %s" % (X, X)), "%s(<i>y</i> + 1)" % X, ["%s<i>y</i>(1 + 1)" % X, "%s(<i>y</i>)" % X, "<i>y</i>(%s + 1)" % X], "Both terms contain %s. %s = %s × 1, so <b>%s(<i>y</i> + 1)</b>." % (X, X, X, X)),
        ("A square has side (%s + 6) cm. Which expression is its area in cm²?" % X, poly(1, 12, 36, X), [poly(1, 0, 36, X), poly(1, 6, 36, X), poly(0, 4, 24, X)], "(%s + 6)<sup>2</sup> = <b>%s</b>." % (X, poly(1, 12, 36, X))),
        ("Expand %s." % B("(2%s + 1)(%s + 4)" % (X, X)), poly(2, 9, 4, X), [poly(2, 8, 4, X), poly(2, 5, 4, X), poly(3, 9, 4, X)], "2%s + 8%s + %s + 4 = <b>%s</b>." % (sq(X), X, X, poly(2, 9, 4, X))),
        ("Factorise fully %s." % B("15<i>ab</i> + 10<i>a</i>"), "5<i>a</i>(3<i>b</i> + 2)", ["5(3<i>ab</i> + 2<i>a</i>)", "<i>a</i>(15<i>b</i> + 10)", "5<i>b</i>(3<i>a</i> + 2)"],
         "The HCF is 5<i>a</i>: <b>5<i>a</i>(3<i>b</i> + 2)</b>."),
        ("Which expression is NOT equivalent to 4%s + 8?" % X, "4(%s + 8)" % X, ["4(%s + 2)" % X, "2(2%s + 4)" % X, "8 + 4%s" % X], "4(%s + 8) = 4%s + 32, so it is <b>not</b> equivalent." % (X, X)),
    ]
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p>To <b>expand</b>, multiply every term inside the bracket by the term outside. For two brackets, multiply "
        "every term in the first by every term in the second (a grid helps), then collect like terms.</p>"
        "<p>To <b>factorise</b>, find the highest common factor of all the terms, including letters, and take it outside "
        "the bracket. Check by expanding.</p>",
        [("Expand 3<i>x</i>(2<i>x</i> − 5).", ["3<i>x</i> × 2<i>x</i> = 6<i>x</i><sup>2</sup>.", "3<i>x</i> × (−5) = −15<i>x</i>."], "6<i>x</i><sup>2</sup> − 15<i>x</i>"),
         ("Expand and simplify (<i>x</i> + 4)(<i>x</i> − 2).", ["<i>x</i><sup>2</sup> − 2<i>x</i> + 4<i>x</i> − 8."], "<i>x</i><sup>2</sup> + 2<i>x</i> − 8"),
         ("Factorise fully 6<i>x</i><sup>2</sup> + 9<i>x</i>.", ["The HCF of 6<i>x</i><sup>2</sup> and 9<i>x</i> is 3<i>x</i>."], "3<i>x</i>(2<i>x</i> + 3)")],
        ["Multiplying only the first term: 3<i>x</i>(2<i>x</i> − 5) is not 6<i>x</i><sup>2</sup> − 5.",
         "Losing the sign: −2(<i>x</i> − 3) = −2<i>x</i> + 6.",
         "Missing the middle terms: (<i>x</i> + 4)<sup>2</sup> = <i>x</i><sup>2</sup> + 8<i>x</i> + 16, not <i>x</i><sup>2</sup> + 16.",
         "Not factorising fully: 12<i>x</i> + 18 = 6(2<i>x</i> + 3), not 2(6<i>x</i> + 9)."])


def main():
    sets = [S("Expanding single brackets", collect(one_single, 20, R)),
            S("Expanding and simplifying", collect(one_simplify, 20, R)),
            S("Expanding double brackets", collect(one_double, 20, R)),
            S("Factorising", collect(one_factor, 20, R)),
            S("Problems", problems())]
    make(8, "expanding-and-factorising", 3, "A",
         "Expanding and Factorising: Single and Double Brackets",
         "Year 8 Expanding and Factorising Worksheets: Single Brackets, Double Brackets and Common Factors",
         "Expanding and factorising",
         "Simplify and manipulate algebraic expressions to maintain equivalence by: collecting like terms; multiplying a "
         "single term over a bracket; taking out common factors; expanding products of two or more binomials.",
         "Free Year 8 worksheets on expanding and factorising: single brackets with letters outside, expanding and "
         "simplifying, double brackets, factorising with algebraic common factors and area problems. 100 questions with answers.",
         "Expand: multiply every term inside the bracket. Factorise: take out the highest common factor.",
         "For two brackets, multiply each term in the first by each term in the second, then collect like terms.",
         body(),
         [("What is the difference between expanding and factorising?", "Expanding removes brackets by multiplying out. Factorising puts brackets back in by taking out a common factor. They are opposites."),
          ("How do I expand double brackets?", "Multiply each term in the first bracket by each term in the second (four products), then collect like terms. A grid or FOIL helps."),
          ("What does factorise fully mean?", "Take out the highest common factor, including any letters, so nothing more can come out of the bracket."),
          ("How can I check my factorising?", "Expand your answer. You should get back to the expression you started with.")],
         sets, R)


if __name__ == "__main__":
    main()
