# -*- coding: utf-8 -*-
"""
UK Year 7 Maths: Simplifying Expressions (KS3 Algebra)
  python3 tools/gen_uk_maths_y7_simplifying_expressions.py
Collecting like terms, multiplying and dividing terms, expanding a single bracket, expanding and
simplifying, and taking out a common factor. Wrong answers come from real mistakes: combining unlike
terms (3x + 2y = 5xy), losing a minus sign, multiplying only the first term in a bracket, and adding
instead of multiplying powers.
"""
import random
from fractions import Fraction as F
from uk_ks3 import num, par, mcq, B, S, make, lesson, collect, T, expr, MINUS

R = random.Random(71201)
VARS = ["<i>a</i>", "<i>b</i>", "<i>x</i>", "<i>y</i>", "<i>m</i>", "<i>n</i>", "<i>p</i>", "<i>t</i>"]


def nz(r, lo, hi):
    while True:
        k = r.randint(lo, hi)
        if k:
            return k


# ------------------------------------------------------------ set 1: like terms, one letter
def one_like1(r):
    x = r.choice(VARS)
    cs = [r.randint(2, 9), nz(r, -7, 9), nz(r, -6, 8)]
    if r.random() < 0.5:
        cs = cs[:2]
    tot = sum(cs)
    if tot == 0:
        return None
    q = "Simplify %s." % B(expr([(c, x) for c in cs]))
    right = expr([(tot, x)])
    absum = sum(abs(c) for c in cs)
    wr = [expr([(absum, x)]) if absum != tot else expr([(tot + 2, x)]), "%s%s" % (num(tot), x.replace("</i>", "<sup>%d</sup></i>" % len(cs)).replace("<i>", "<i>") if False else x + "<sup>%d</sup>" % len(cs)),
          expr([(-tot, x)]), num(tot)]
    e = "All the terms are %s terms, so add the numbers: %s = %s. The answer is <b>%s</b>." % (
        x, " + ".join("(%s)" % num(c) if c < 0 else num(c) for c in cs), num(tot), right)
    return T(q, right, [w for w in wr if w != right][:3], e)


# ------------------------------------------------------------ set 2: like terms, two letters and numbers
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


# ------------------------------------------------------------ set 3: multiply and divide terms
def one_muldiv(r):
    x, y = sorted(r.sample(VARS, 2))
    a, b = r.randint(2, 9), r.randint(2, 9)
    kind = r.randint(0, 3)
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


# ------------------------------------------------------------ set 4: expanding one bracket
def one_expand(r):
    x = r.choice(VARS)
    k = r.choice([2, 3, 4, 5, 6, 7, 8, -2, -3, -4, -5])
    a = r.choice([1, 1, 2, 3])
    b = nz(r, -9, 9)
    kind = r.random()
    if kind < 0.2 and k > 0:
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


# ------------------------------------------------------------ set 5: expand and simplify, factorise
def one_expand2(r):
    x = r.choice(VARS)
    k1, k2 = r.randint(2, 6), r.choice([2, 3, 4, 5, -2, -3])
    b1, b2 = nz(r, -6, 7), nz(r, -6, 7)
    A = k1 + k2
    C = k1 * b1 + k2 * b2
    if A == 0:
        return None
    s1 = "%d(%s)" % (k1, expr([(1, x), (b1, "")]))
    s2 = (" + %d(%s)" % (k2, expr([(1, x), (b2, "")]))) if k2 > 0 else (" %s %d(%s)" % (MINUS, -k2, expr([(1, x), (b2, "")])))
    right = expr([(A, x), (C, "")])
    wr = [expr([(A, x), (k1 * b1 + b2, "")]), expr([(A, x), (k1 * b1 - k2 * b2, "")]) if k2 < 0 else expr([(A, x), (b1 + b2, "")]),
          expr([(k1 - k2 if k2 < 0 else A + 1, x), (C, "")])]
    wr = [w for w in wr if w != right]
    q = "Expand and simplify %s." % B(s1 + s2)
    e = "%s and %s. Collect like terms: <b>%s</b>." % (
        expr([(k1, x), (k1 * b1, "")]), expr([(k2, x), (k2 * b2, "")]), right)
    return T(q, right, wr[:3], e)


def one_factorise(r):
    x = r.choice(VARS)
    h = r.choice([2, 3, 4, 5, 6])
    a, b = r.randint(1, 5), nz(r, -7, 7)
    from math import gcd
    if gcd(a, abs(b)) != 1:
        return None
    if r.random() < 0.25:
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


def body():
    return lesson(
        "<p><b>Like terms</b> have exactly the same letters and powers. Only like terms can be added or subtracted: "
        "3<i>x</i> + 5<i>x</i> = 8<i>x</i>, but 3<i>x</i> + 2<i>y</i> cannot be simplified. The sign belongs to the term after it.</p>"
        "<p>To <b>expand</b> a bracket, multiply every term inside by the term outside. "
        "To <b>factorise</b>, take out the highest common factor and put the rest in a bracket.</p>",
        [("Simplify 5<i>x</i> + 3<i>y</i> − 2<i>x</i> + <i>y</i>.", ["<i>x</i> terms: 5<i>x</i> − 2<i>x</i> = 3<i>x</i>.", "<i>y</i> terms: 3<i>y</i> + <i>y</i> = 4<i>y</i>."], "3<i>x</i> + 4<i>y</i>"),
         ("Expand and simplify 3(<i>x</i> + 2) − 2(<i>x</i> − 4).", ["3<i>x</i> + 6 − 2<i>x</i> + 8.", "Collect: <i>x</i> + 14."], "<i>x</i> + 14"),
         ("Factorise 12<i>a</i> + 18.", ["The HCF of 12 and 18 is 6.", "12<i>a</i> ÷ 6 = 2<i>a</i> and 18 ÷ 6 = 3."], "6(2<i>a</i> + 3)")],
        ["Combining unlike terms: 3<i>x</i> + 2<i>y</i> is not 5<i>xy</i>.",
         "Multiplying only the first term: 4(<i>x</i> + 3) is 4<i>x</i> + 12, not 4<i>x</i> + 3.",
         "Losing the sign: −2(<i>x</i> − 4) = −2<i>x</i> + 8.",
         "Writing <i>x</i> × <i>x</i> as 2<i>x</i>. It is <i>x</i><sup>2</sup>."])


def main():
    sets = [S("Collecting like terms", collect(one_like1, 20, R)),
            S("Like terms with two letters", collect(one_like2, 20, R)),
            S("Multiplying and dividing terms", collect(one_muldiv, 20, R)),
            S("Expanding brackets", collect(one_expand, 20, R)),
            S("Expanding, simplifying and factorising", collect(one_expand2, 12, R) + collect(one_factorise, 8, R))]
    make(7, "simplifying-expressions", 12, "A",
         "Simplifying Expressions: Like Terms, Expanding Brackets and Factorising",
         "Year 7 Simplifying Expressions Worksheets: Collecting Like Terms, Expanding Brackets and Factorising",
         "Simplifying expressions",
         "Simplify and manipulate algebraic expressions to maintain equivalence by: collecting like terms; multiplying a "
         "single term over a bracket; taking out common factors.",
         "Free Year 7 worksheets on simplifying expressions: collecting like terms, multiplying terms, expanding single "
         "brackets, expanding and simplifying, and factorising. 100 questions with step-by-step answers.",
         "Only like terms can be collected: 3x + 5x = 8x, but 3x + 2y stays as it is.",
         "Expand by multiplying every term in the bracket. Factorise by taking out the highest common factor.",
         body(),
         [("What are like terms?", "Terms with exactly the same letters and powers, such as 3x and −5x. 3x and 3x² are not like terms."),
          ("Can I simplify 3x + 2y?", "No. They are unlike terms, so 3x + 2y is already as simple as it can be."),
          ("How do I expand a bracket with a negative in front?", "Multiply each term by the negative number. −2(x − 4) = −2x + 8, because −2 × −4 = +8."),
          ("What does factorise fully mean?", "Take out the highest common factor, so nothing more can come out of the bracket. 12a + 18 = 6(2a + 3), not 2(6a + 9).")],
         sets, R)


if __name__ == "__main__":
    main()
