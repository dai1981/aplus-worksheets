# -*- coding: utf-8 -*-
"""
AU Year 8 Maths: Expanding and Factorising Linear Expressions (Australian Curriculum v9.0: AC9M8A01)
  python3 tools/gen_au_maths_y8_expanding_and_factorising.py
Expanding a bracket (including a negative outside), expanding and simplifying, factorising with the highest
common factor (including a negative factor), simplifying products and like terms, and problems.
Wrong answers come from real mistakes: multiplying only the first term, sign errors with a negative outside,
taking out a common factor that is not the highest, and combining unlike terms.
"""
import random
from math import gcd
from au_hs import num, par, B, S, make, lesson, collect, T, expr, MINUS

R = random.Random(80501)
VARS = ["<i>a</i>", "<i>b</i>", "<i>x</i>", "<i>y</i>", "<i>m</i>", "<i>n</i>", "<i>p</i>", "<i>t</i>"]
VS = VARS


def nz(r, lo, hi):
    while True:
        k = r.randint(lo, hi)
        if k:
            return k


def br(a, b, v):
    return "(%s)" % expr([(a, v), (b, "")])


# ------------------------------------------------------------ set 1: expanding
def one_expand(r):
    x = r.choice(VARS)
    k = r.choice([2, 3, 4, 5, 6, 7, 8, -2, -3, -4, -5])
    a = r.choice([1, 1, 2, 3])
    b = nz(r, -9, 9)
    kind = r.random()
    if False:
        # x(x + b)
        q = "Expand %s." % B("%s(%s)" % (x, expr([(1, x), (b, "")])))
        right = expr([(1, x + "<sup>2</sup>"), (b, x)])
        wr = [expr([(1, x + "<sup>2</sup>"), (b, "")]), expr([(2, x), (b, x)]), expr([(1 + b, x)]) if 1 + b else expr([(b, x + "<sup>2</sup>")])]
        e = "%s × %s = %s<sup>2</sup> and %s × %s = %s. So <b>%s</b>." % (x, x, x, x, num(b), expr([(b, x)]), right)
        return T(q, right, [w for w in wr if w != right], e)
    inner = expr([(a, x), (b, "")])
    shown = ("%d(%s)" % (k, inner)) if k > 0 else ("%s%d(%s)" % (MINUS, -k, inner))
    right = expr([(k * a, x), (k * b, "")])
    wr = [expr([(k * a, x), (b, "")]),                 # only first term
          expr([(k * a, x), (-k * b, "")]),            # sign slip
          expr([(k + a, x), (k + b, "")]) if k + b else expr([(k + a, x)])]
    if k < 0:
        wr.insert(0, expr([(k * a, x), (-k * b, "")]))
    wr = [w for w in wr if w != right]
    q = "Expand %s." % B(shown)
    e = "Multiply %s by each term inside the bracket: %s × %s and %s × %s. The answer is <b>%s</b>." % (
        num(k), num(k), expr([(a, x)]), num(k), par(b), right)
    return T(q, right, wr[:3], e)


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


# ------------------------------------------------------------ set 3: factorising
def one_factorise(r):
    x = r.choice(VARS)
    h = r.choice([2, 3, 4, 5, 6])
    a, b = r.randint(1, 5), nz(r, -7, 7)
    if gcd(a, abs(b)) != 1:
        return None
    if False:
        # x^2 + bx = x(x + b)
        shown = expr([(1, x + "<sup>2</sup>"), (b, x)])
        right = "%s(%s)" % (x, expr([(1, x), (b, "")]))
        wr = ["%s(%s)" % (x, expr([(1, x + "<sup>2</sup>"), (b, "")])), "%s<sup>2</sup>(1 %s %d)" % (x, "+" if b > 0 else MINUS, abs(b)), "%d(%s)" % (abs(b), expr([(1, x + "<sup>2</sup>"), (1 if b > 0 else -1, x)]))]
        e = "Both terms contain %s, so take it out: <b>%s</b>." % (x, right)
        return T("Factorise %s." % B(shown), right, wr, e)
    shown = expr([(h * a, x), (h * b, "")])
    right = "%d(%s)" % (h, expr([(a, x), (b, "")]))
    small = [d for d in range(2, h) if h % d == 0]
    wr = ["%d(%s)" % (small[0], expr([(h * a // small[0], x), (h * b // small[0], "")])) if small else "%d(%s)" % (h, expr([(a, x), (h * b, "")])),
          "%d(%s)" % (h, expr([(a, x), (-b, "")])),
          "%d%s(%s)" % (h, x, expr([(a, ""), (b, "")]))]
    e = "The highest common factor of %d and %d is %d: <b>%s</b>. Check by expanding." % (h * a, abs(h * b), h, right)
    if small:
        e += " Taking out only %d does not factorise fully." % small[0]
    return T("Factorise fully %s." % B(shown), right, wr, e)


def one_factor_neg(r):
    v = r.choice(VS)
    h = r.choice([2, 3, 4, 5, 6])
    a, b = r.randint(1, 6), r.randint(1, 9)
    if gcd(a, b) != 1:
        return None
    q = "Factorise %s by taking out %s." % (B(expr([(-h * a, v), (-h * b, "")])), B(MINUS + str(h)))
    right = "%s%d%s" % (MINUS, h, br(a, b, v))
    wr = ["%s%d%s" % (MINUS, h, br(a, -b, v)), "%d%s" % (h, br(-a, b, v)) if a != 1 or True else "", "%s%d%s" % (MINUS, h, br(-a, -b, v))]
    e = "%s ÷ (%s%d) = %s and %s ÷ (%s%d) = %d. So <b>%s</b>. Check: %s%d × %s = %s." % (
        expr([(-h * a, v)]), MINUS, h, expr([(a, v)]), num(-h * b), MINUS, h, b, right, MINUS, h, expr([(a, v)]), expr([(-h * a, v)]))
    return T(q, right, [w for w in wr if w != right], e)


# ------------------------------------------------------------ set 4: simplifying
def one_muldiv(r):
    x, y = sorted(r.sample(VARS, 2))
    a, b = r.randint(2, 9), r.randint(2, 9)
    kind = r.choice([0, 2, 3])
    if kind == 0:
        q = "Simplify %s." % B("%d%s × %d%s" % (a, x, b, y))
        right = "%d%s%s" % (a * b, x, y)
        wr = ["%d%s%s" % (a + b, x, y), "%d%s + %d%s" % (a, x, b, y) if False else "%d%s%s" % (a * b, x, x), "%d%s" % (a * b, x)]
        wr = ["%d%s%s" % (a + b, x, y), "%d%s<sup>2</sup>" % (a * b, x), "%d%s%s" % (a, x, y)]
        e = "Multiply the numbers (%d × %d = %d) and write the letters together: <b>%s</b>." % (a, b, a * b, right)
    elif kind == 1:
        q = "Simplify %s." % B("%d%s × %d%s" % (a, x, b, x))
        right = "%d%s<sup>2</sup>" % (a * b, x)
        wr = ["%d%s" % (a * b, x), "%d%s<sup>2</sup>" % (a + b, x), "%d%s" % (a + b, x)]
        e = "%d × %d = %d and %s × %s = %s<sup>2</sup>, so <b>%s</b>." % (a, b, a * b, x, x, x, right)
    elif kind == 2:
        q = "Simplify %s." % B("%d%s%s ÷ %d%s" % (a * b, x, y, a, x))
        right = "%d%s" % (b, y)
        wr = ["%d%s%s" % (b, x, y), "%d%s" % (a * b - a, y), "%d" % b]
        e = "%d ÷ %d = %d and the %s cancels: <b>%s</b>." % (a * b, a, b, x, right)
    else:
        q = "Simplify %s." % B("%s × %s × %d" % (x, y, a))
        right = "%d%s%s" % (a, x, y)
        wr = ["%s%s%d" % (x, y, a), "%d + %s%s" % (a, x, y), "%d%s<sup>2</sup>" % (a, x)]
        e = "Write the number first, then the letters in alphabetical order: <b>%s</b>." % right
    return T(q, right, wr, e)


def one_like2(r):
    x, y = sorted(r.sample(VARS, 2))
    a1, b1, a2, b2 = r.randint(1, 9), nz(r, -6, 8), nz(r, -6, 6), nz(r, -6, 7)
    c = nz(r, -9, 9) if r.random() < 0.5 else 0
    terms = [(a1, x), (b1, y), (a2, x), (b2, y)] + ([(c, "")] if c else [])
    r.shuffle(terms)
    A, Bb = a1 + a2, b1 + b2
    if A == 0 or Bb == 0:
        return None
    right = expr([(A, x), (Bb, y), (c, "")])
    wr = [expr([(A + Bb, x + y)] + ([(c, "")] if c else [])),                     # combined unlike terms
          expr([(abs(a1) + abs(a2), x), (abs(b1) + abs(b2), y), (c, "")]),         # ignored signs
          expr([(A, x), (-Bb, y), (c, "")]),
          expr([(A + Bb + c, x + y)])]
    wr = [w for w in wr if w != right]
    q = "Simplify %s." % B(expr(terms))
    e = "Collect the %s terms (%s) and the %s terms (%s)%s. The answer is <b>%s</b>." % (
        x, expr([(A, x)]), y, expr([(Bb, y)]), ", then the number" if c else "", right)
    return T(q, right, wr[:3], e)


# ------------------------------------------------------------ set 5: problems
def problems():
    x, y = "<i>x</i>", "<i>y</i>"
    data = [
        ("A rectangle is (%s + 5) cm long and 3 cm wide. Which expression gives its area?" % x, "3%s + 15" % x, ["3%s + 5" % x, "%s + 15" % x, "2%s + 16" % x], "3(%s + 5) = <b>3%s + 15</b>." % (x, x)),
        ("A rectangle is (%s + 5) cm by (%s + 2) cm. Which expression gives its perimeter?" % (x, x), "4%s + 14" % x, ["2%s + 7" % x, "4%s + 7" % x, "%s + 7" % x], "2(%s + 5) + 2(%s + 2) = <b>4%s + 14</b>." % (x, x, x)),
        ("Which expression is equivalent to 3(2%s − 4)?" % x, "6%s − 12" % x, ["6%s − 4" % x, "5%s − 7" % x, "6%s + 12" % x], "3 × 2%s = 6%s and 3 × (−4) = −12: <b>6%s − 12</b>." % (x, x, x)),
        ("Which is the full factorisation of 12%s + 18?" % x, "6(2%s + 3)" % x, ["3(4%s + 6)" % x, "2(6%s + 9)" % x, "6(2%s + 18)" % x], "The HCF of 12 and 18 is 6: <b>6(2%s + 3)</b>." % x),
        ("Is 2%s + 10 the same as 2(%s + 5)?" % (x, x), "Yes, for every value of " + x, ["No, never", "Only when " + x + " = 0", "Only when " + x + " = 5"],
         "2(%s + 5) = 2%s + 10, so they are equal <b>for every value</b>." % (x, x)),
        ("The area of a rectangle is 6%s + 15 and its width is 3. What is its length?" % x, "2%s + 5" % x, ["6%s + 12" % x, "2%s + 15" % x, "3%s + 5" % x], "6%s + 15 = 3(2%s + 5), so the length is <b>2%s + 5</b>." % (x, x, x)),
        ("Expand %s." % B("−4(3 − 2%s)" % x), "−12 + 8%s" % x, ["−12 − 8%s" % x, "12 − 8%s" % x, "−12 + 2%s" % x], "−4 × 3 = −12 and −4 × (−2%s) = +8%s: <b>−12 + 8%s</b>." % (x, x, x)),
        ("Expand and simplify %s." % B("5(%s + 2) − 2(%s − 3)" % (x, x)), "3%s + 16" % x, ["3%s + 4" % x, "3%s + 13" % x, "7%s + 16" % x], "5%s + 10 − 2%s + 6 = <b>3%s + 16</b>." % (x, x, x)),
        ("Which expression is NOT equivalent to 4%s + 8?" % x, "4(%s + 8)" % x, ["4(%s + 2)" % x, "2(2%s + 4)" % x, "8 + 4%s" % x], "4(%s + 8) = 4%s + 32, so it is <b>not</b> equivalent." % (x, x)),
        ("Movie tickets cost $%s each and popcorn costs $6. Which expression gives the cost for 4 people who each buy a ticket and popcorn?" % x, "4(%s + 6)" % x, ["4%s + 6" % x, "%s + 24" % x, "4 + %s + 6" % x],
         "Each person pays %s + 6, so 4 people pay <b>4(%s + 6)</b> = 4%s + 24." % (x, x, x)),
        ("Which law is shown by 3 × (%s + 4) = 3 × %s + 3 × 4?" % (x, x), "The distributive law", ["The commutative law", "The associative law", "The identity law"], "Multiplying over a bracket uses the <b>distributive law</b>."),
        ("Which law is shown by %s + 7 = 7 + %s?" % (x, x), "The commutative law", ["The distributive law", "The associative law", "The inverse law"], "Changing the order of addition uses the <b>commutative law</b>."),
        ("Which law is shown by (2 × %s) × 5 = 2 × (%s × 5)?" % (x, x), "The associative law", ["The commutative law", "The distributive law", "The identity law"], "Changing which pair is done first uses the <b>associative law</b>."),
        ("Simplify %s." % B("%s + 0" % x), x, ["0", "0%s" % x, "1"], "Adding 0 does not change a number (the identity law): <b>%s</b>." % x),
        ("Simplify %s." % B("5%s − 5%s + 3" % (x, x)), "3", ["10%s + 3" % x, "3%s" % x, "0"], "5%s − 5%s = 0 (the inverse law), leaving <b>3</b>." % (x, x)),
        ("Mia factorises 8%s + 12 as 2(4%s + 6). What should she have written?" % (x, x), "4(2%s + 3)" % x, ["8(%s + 4)" % x, "2(4%s + 6)" % x, "4(2%s + 12)" % x], "The highest common factor of 8 and 12 is 4: <b>4(2%s + 3)</b>." % x),
        ("A triangle has sides %s, %s + 3 and 2%s − 1 cm. Which expression gives its perimeter?" % (x, x, x), "4%s + 2" % x, ["4%s + 4" % x, "3%s + 2" % x, "2%s<sup>2</sup> + 2" % x], "%s + %s + 3 + 2%s − 1 = <b>4%s + 2</b>." % (x, x, x, x)),
        ("Factorise fully %s." % B("15%s + 10%s" % (x, y)), "5(3%s + 2%s)" % (x, y), ["5(3%s + 10%s)" % (x, y), "15(%s + 10%s)" % (x, y), "5%s(3 + 2%s)" % (x, y)], "The HCF of 15 and 10 is 5: <b>5(3%s + 2%s)</b>." % (x, y)),
        ("Rearrange the terms: which expression is equal to 7 − 3%s + 2%s?" % (x, y), "2%s − 3%s + 7" % (y, x), ["3%s − 2%s + 7" % (x, y), "2%s + 3%s + 7" % (y, x), "7%s − 3 + 2%s" % (x, y)], "Each term keeps its sign when it moves: <b>2%s − 3%s + 7</b>." % (y, x)),
        ("A plumber charges a $90 call-out fee plus $%s for each hour. Which expression gives the cost for 3 jobs that each take 2 hours?" % x, "6%s + 270" % x, ["3(%s + 90)" % x, "2%s + 270" % x, "6%s + 90" % x],
         "One job costs 90 + 2%s. Three jobs: 3(90 + 2%s) = <b>6%s + 270</b>." % (x, x, x)),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>To <b>expand</b>, multiply every term inside the bracket by the number outside (the distributive law). "
        "Watch the signs when the number outside is negative.</p>"
        "<p>To <b>factorise</b>, find the highest common factor of the terms and take it outside the bracket. Check by expanding.</p>"
        "<p>The <b>commutative</b> and <b>associative</b> laws let you reorder and regroup terms; the <b>identity</b> laws "
        "(+ 0, × 1) and <b>inverse</b> laws (<i>a</i> − <i>a</i> = 0) help you simplify.</p>",
        [("Expand −3(2<i>x</i> − 5).", ["−3 × 2<i>x</i> = −6<i>x</i>.", "−3 × (−5) = +15."], "−6<i>x</i> + 15"),
         ("Expand and simplify 4(<i>x</i> + 2) + 3(<i>x</i> − 1).", ["4<i>x</i> + 8 + 3<i>x</i> − 3."], "7<i>x</i> + 5"),
         ("Factorise fully 18<i>x</i> − 24.", ["The HCF of 18 and 24 is 6."], "6(3<i>x</i> − 4)")],
        ["Multiplying only the first term: 3(2<i>x</i> − 5) is not 6<i>x</i> − 5.",
         "Losing the sign: −2(<i>x</i> − 3) = −2<i>x</i> + 6, not −2<i>x</i> − 6.",
         "Not factorising fully: 12<i>x</i> + 18 = 6(2<i>x</i> + 3), not 2(6<i>x</i> + 9).",
         "Combining unlike terms: 3<i>x</i> + 2<i>y</i> cannot be simplified to 5<i>xy</i>."])


def main():
    sets = [S("Expanding brackets", collect(one_expand, 20, R)),
            S("Expanding and simplifying", collect(one_simplify, 20, R)),
            S("Factorising", collect(one_factorise, 14, R) + collect(one_factor_neg, 6, R)),
            S("Simplifying expressions", collect(one_muldiv, 8, R) + collect(one_like2, 12, R)),
            S("Linear expressions in problems", problems())]
    make(8, "expanding-and-factorising", 5, "AC9M8A01",
         "Expanding and Factorising Linear Expressions",
         "Year 8 Expanding and Factorising Worksheets: Linear Expressions and the Distributive Law (Free, Answer Key)",
         "Expanding and factorising",
         "create, expand, factorise, rearrange and simplify linear expressions, applying the associative, commutative, identity, distributive and inverse properties",
         "Free Year 8 maths worksheets on expanding and factorising for the Australian Curriculum (AC9M8A01): expanding brackets, "
         "expanding and simplifying, factorising with the highest common factor and the laws of arithmetic. 100 questions with an answer key.",
         "Expand: multiply every term inside the bracket. Factorise: take out the highest common factor.",
         "Expanding and factorising are opposites, so you can check one with the other.",
         body(),
         [("What is the difference between expanding and factorising?", "Expanding removes brackets by multiplying out. Factorising puts brackets back in by taking out a common factor. They are opposites."),
          ("What is the distributive law?", "a(b + c) = ab + ac. The number outside the bracket multiplies every term inside."),
          ("What does factorise fully mean?", "Take out the highest common factor, so nothing more can come out of the bracket."),
          ("How do I expand a bracket with a negative outside?", "Multiply each term by the negative number. A negative times a negative is positive: −2(x − 3) = −2x + 6.")],
         sets, R)


if __name__ == "__main__":
    main()
