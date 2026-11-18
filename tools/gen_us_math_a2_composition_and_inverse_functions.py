# -*- coding: utf-8 -*-
"""
US Algebra 2: Function Operations, Composition, and Inverses (Common Core F-BF.A.1b, F-BF.A.1c, F-BF.B.4)
  python3 tools/gen_us_math_a2_composition_and_inverse_functions.py
Adding, subtracting, multiplying and dividing functions; evaluating compositions; writing f(g(x)); finding
inverses; and checking inverses with tables, composition and the horizontal line test.
Wrong answers come from real mistakes: multiplying instead of composing, doing the inner and outer
functions in the wrong order, writing the reciprocal 1/f(x) as the inverse, and forgetting to undo the
operations in reverse order.
"""
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, num, MINUS, fr, People
from a2_common import X, poly, sf, ps, lin, pmul, peval

R = random.Random(95701)
FX, GX = "<i>f</i>(<i>x</i>)", "<i>g</i>(<i>x</i>)"


def L(m, b, var=X):
    return poly([m, b], var) if m else sf(b)


def sub(p, q):
    """compose polynomial p(q(x)) where p, q are coefficient lists"""
    out = [0]
    for c in p:
        out = pmul(out, q) if len(out) > 1 or out[0] else [0]
        out = add(out, [c])
    return out


def add(p, q):
    n = max(len(p), len(q))
    p = [0] * (n - len(p)) + p
    q = [0] * (n - len(q)) + q
    r = [a + b for a, b in zip(p, q)]
    while len(r) > 1 and r[0] == 0:
        r = r[1:]
    return r


def comp(p, q):
    out = [p[0]]
    for c in p[1:]:
        out = add(pmul(out, q), [c])
    return out


# ------------------------------------------------------------ set 1: operations on functions
def one_ops(r):
    a, b = r.choice([1, 2, 3, -1, -2]), r.randint(-6, 6)
    c, d = r.choice([1, 2, 3, -1]), r.randint(-6, 6)
    f, g = [a, b], [c, d]
    kind = r.choice(["sum", "diff", "prod", "val"])
    defs = "%s = %s and %s = %s." % (FX, L(a, b), GX, L(c, d))
    if kind == "sum":
        if a + c == 0:
            return None
        right = poly(add(f, g))
        q = "%s Find (<i>f</i> + <i>g</i>)(<i>x</i>)." % defs
        wr = [poly(add(f, [-c, -d])), poly(pmul(f, g)), poly(comp(f, g))]
        e = "Add the like terms: (%s) + (%s) = <b>%s</b>." % (L(a, b), L(c, d), right)
    elif kind == "diff":
        right = poly(add(f, [-c, -d]))
        q = "%s Find (<i>f</i> %s <i>g</i>)(<i>x</i>)." % (defs, MINUS)
        wr = [poly(add(f, [-c, d])), poly(add(f, g)), poly(add([-a, -b], g))]
        e = "Subtract every term of <i>g</i>: (%s) %s (%s) = <b>%s</b>." % (L(a, b), MINUS, L(c, d), right)
    elif kind == "prod":
        right = poly(pmul(f, g))
        q = "%s Find (<i>fg</i>)(<i>x</i>)." % defs
        wr = [poly([a * c, b * d]), poly(comp(f, g)), poly(add(f, g))]
        e = "Multiply with FOIL: (%s)(%s) = <b>%s</b>." % (L(a, b), L(c, d), right)
    else:
        k = r.randint(-4, 4)
        fv, gv = a * k + b, c * k + d
        if gv == 0 or F(fv, gv).denominator > 4:
            return None
        ans = F(fv, gv)
        q = "%s Find (<i>f</i>/<i>g</i>)(%s)." % (defs, sf(k))
        return T(q, sf(ans), [sf(w) for w in dict.fromkeys([F(gv, fv) if fv else ans + 1, fv * gv, fv - gv]) if w != ans][:3],
                 "<i>f</i>(%s) = %s and <i>g</i>(%s) = %s, so the quotient is %s ÷ %s = <b>%s</b>." % (sf(k), sf(fv), sf(k), sf(gv), sf(fv), ps(gv), sf(ans)))
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)


# ------------------------------------------------------------ set 2: evaluate compositions
def one_eval(r):
    a, b = r.choice([1, 2, 3, -2]), r.randint(-6, 6)
    sq = r.random() < 0.5
    f = [1, 0, r.randint(-5, 5)] if sq else [a, b]
    g = [r.choice([1, 2, 3, -1]), r.randint(-5, 5)]
    k = r.randint(-3, 4)
    order = r.choice(["fg", "gf"])
    if order == "fg":
        inner, outer = g, f
        name = "<i>f</i>(<i>g</i>(%s))" % sf(k)
    else:
        inner, outer = f, g
        name = "<i>g</i>(<i>f</i>(%s))" % sf(k)
    iv = peval(inner, k)
    ans = peval(outer, iv)
    alt = peval(inner, peval(outer, k))
    q = "%s = %s and %s = %s. Find %s." % (FX, poly(f), GX, poly(g), B(name))
    return T(q, sf(ans), [sf(w) for w in dict.fromkeys([alt, peval(f, k) * peval(g, k), iv, ans + 2]) if w != ans][:3],
             "Work from the inside out: the inner value is %s. Put it into the outer function: <b>%s</b>. (Doing them in the other order gives %s.)" % (sf(iv), sf(ans), sf(alt)))


# ------------------------------------------------------------ set 3: write f(g(x))
def one_comp(r):
    f = r.choice([[1, 0, r.randint(-5, 5)], [r.choice([2, 3, -1, 4]), r.randint(-6, 6)]])
    g = [r.choice([1, 2, 3, -1]), r.randint(-5, 5)]
    if g[1] == 0:
        return None
    order = r.choice(["fg", "gf"])
    if order == "fg":
        right = poly(comp(f, g))
        other = poly(comp(g, f))
        name = "<i>f</i>(<i>g</i>(<i>x</i>))"
    else:
        right = poly(comp(g, f))
        other = poly(comp(f, g))
        name = "<i>g</i>(<i>f</i>(<i>x</i>))"
    q = "%s = %s and %s = %s. Find %s." % (FX, poly(f), GX, poly(g), B(name))
    wr = [other, poly(pmul(f, g)), poly(add(f, g)) if len(f) == 2 else poly([1, 0, g[0] * 0 + f[-1] + g[1]]) if False else poly(add(comp(f, [g[0], 0]), [g[1]]))]
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3],
             "Replace every <i>x</i> in the outer function with the whole inner function, then simplify: <b>%s</b>." % right)


# ------------------------------------------------------------ set 4: find the inverse
def one_inv(r):
    kind = r.choice(["lin", "lin", "frac", "cube", "rat", "sqrt"])
    if kind == "lin":
        a, b = r.choice([2, 3, 4, 5, -2, -3]), r.choice([x for x in range(-9, 10) if x])
        q = "Find the inverse of %s." % B("%s = %s" % (FX, L(a, b)))
        right = "<i>f</i><sup>%s1</sup>(<i>x</i>) = %s" % (MINUS, fr(lin(b), num(a)) if a > 0 else fr(poly([-1, b]), num(-a)))
        wr = ["<i>f</i><sup>%s1</sup>(<i>x</i>) = %s" % (MINUS, fr("1", L(a, b))), "<i>f</i><sup>%s1</sup>(<i>x</i>) = %s" % (MINUS, fr(lin(-b), num(a)) if a > 0 else fr(poly([-1, -b]), num(-a))),
              "<i>f</i><sup>%s1</sup>(<i>x</i>) = %s" % (MINUS, L(F(1, a), -b) if True else "")]
        wr[2] = "<i>f</i><sup>%s1</sup>(<i>x</i>) = %s%s %s %s" % (MINUS, fr(1, num(abs(a))) if abs(a) != 1 else "", X, MINUS if b > 0 else "+", num(abs(b)))
        if a < 0:
            wr[2] = wr[2].replace("<i>x</i>) = ", "<i>x</i>) = %s" % MINUS, 1)
        return T(q, right, wr, "Swap <i>x</i> and <i>y</i>: <i>x</i> = %s. Solve for <i>y</i>: subtract %s, then divide by %s. <b>%s</b>. (The reciprocal 1/<i>f</i>(<i>x</i>) is not the inverse.)" % (
            L(a, b, "<i>y</i>"), sf(b), sf(a), right))
    if kind == "frac":
        a, b = r.choice([2, 3, 4, 5]), r.choice([x for x in range(-8, 9) if x])
        q = "Find the inverse of %s." % B("%s = %s" % (FX, fr(lin(-b), num(a))))
        right = "<i>f</i><sup>%s1</sup>(<i>x</i>) = %s" % (MINUS, L(a, -b))
        return T(q, right, ["<i>f</i><sup>%s1</sup>(<i>x</i>) = %s" % (MINUS, L(a, b)), "<i>f</i><sup>%s1</sup>(<i>x</i>) = %s" % (MINUS, fr(num(a), lin(-b))),
                            "<i>f</i><sup>%s1</sup>(<i>x</i>) = %s" % (MINUS, L(a, -b * a) if b * a != b else L(a, b + 1))],
                 "Swap: <i>x</i> = %s. Multiply by %d: %d<i>x</i> = %s. Then %s: <b>%s</b>." % (
                     fr(lin(-b, "<i>y</i>"), num(a)), a, a, lin(-b, "<i>y</i>"), ("subtract %d" % b) if b > 0 else ("add %d" % -b), right))
    if kind == "cube":
        b = r.choice([x for x in range(-8, 9) if x])
        a = r.choice([1, 2, 3])
        q = "Find the inverse of %s." % B("%s = %s%s³ %s %d" % (FX, num(a) if a > 1 else "", X, "+" if b > 0 else MINUS, abs(b)))
        inside = lin(b) if a == 1 else fr(lin(b), num(a))
        right = "<i>f</i><sup>%s1</sup>(<i>x</i>) = ∛(%s)" % (MINUS, inside)
        return T(q, right, ["<i>f</i><sup>%s1</sup>(<i>x</i>) = ∛(%s)" % (MINUS, lin(-b) if a == 1 else fr(lin(-b), num(a))), "<i>f</i><sup>%s1</sup>(<i>x</i>) = ∛<i>x</i> %s %d" % (MINUS, MINUS if b > 0 else "+", abs(b)),
                            "<i>f</i><sup>%s1</sup>(<i>x</i>) = (%s)³" % (MINUS, inside)],
                 "Swap <i>x</i> and <i>y</i>, then undo in reverse order: %s, then take the cube root. <b>%s</b>." % (("subtract %d" % b if b > 0 else "add %d" % -b) + ("" if a == 1 else ", divide by %d" % a), right))
    if kind == "sqrt":
        b = r.randint(1, 9)
        q = "Find the inverse of %s, for <i>x</i> ≥ %s." % (B("%s = √(%s)" % (FX, lin(b))), sf(b))
        right = "<i>f</i><sup>%s1</sup>(<i>x</i>) = <i>x</i>² + %d, for <i>x</i> ≥ 0" % (MINUS, b)
        return T(q, right, ["<i>f</i><sup>%s1</sup>(<i>x</i>) = <i>x</i>² %s %d, for <i>x</i> ≥ 0" % (MINUS, MINUS, b), "<i>f</i><sup>%s1</sup>(<i>x</i>) = (<i>x</i> + %d)², for <i>x</i> ≥ 0" % (MINUS, b),
                            "<i>f</i><sup>%s1</sup>(<i>x</i>) = √(<i>x</i> + %d)" % (MINUS, b)],
                 "Swap: <i>x</i> = √(<i>y</i> %s %d). Square: <i>x</i>² = <i>y</i> %s %d, so <i>y</i> = <i>x</i>² + %d. The outputs of <i>f</i> are ≥ 0, so the inverse uses <i>x</i> ≥ 0. <b>%s</b>." % (MINUS, b, MINUS, b, b, right))
    a = r.choice([1, 2, 3, 4, 5])
    q = "Find the inverse of %s." % B("%s = %s" % (FX, fr(num(a), X)))
    right = "<i>f</i><sup>%s1</sup>(<i>x</i>) = %s" % (MINUS, fr(num(a), X))
    return T(q, right, ["<i>f</i><sup>%s1</sup>(<i>x</i>) = %s" % (MINUS, fr(X, num(a))), "<i>f</i><sup>%s1</sup>(<i>x</i>) = %s%s" % (MINUS, num(a) if a > 1 else "", X), "It has no inverse"],
             "Swap: <i>x</i> = %s, so <i>xy</i> = %d and <i>y</i> = %s. This function is its own inverse. <b>%s</b>." % (fr(num(a), "<i>y</i>"), a, fr(num(a), X), right))


# ------------------------------------------------------------ set 5: checking inverses and problems
def one_check(r):
    kind = r.choice(["table", "table", "comp", "hline", "word"])
    if kind == "table":
        a, b = r.choice([2, 3, 4, -2]), r.randint(-5, 5)
        xs_ = r.sample(range(-4, 6), 4)
        k = r.choice(xs_)
        y = a * k + b
        q = "<i>f</i>(%s) = %s. What is <i>f</i><sup>%s1</sup>(%s)?" % (sf(k), sf(y), MINUS, sf(y))
        return T(q, sf(k), [sf(w) for w in dict.fromkeys([y, F(1, y) if y else k + 1, -k if k else 1, a * y + b]) if w != k][:3],
                 "An inverse swaps inputs and outputs: <i>f</i>(%s) = %s means <i>f</i><sup>%s1</sup>(%s) = <b>%s</b>." % (sf(k), sf(y), MINUS, sf(y), sf(k)))
    if kind == "comp":
        a, b = r.choice([2, 3, 4, 5]), r.choice([x for x in range(-7, 8) if x])
        good = r.random() < 0.5
        gtxt = fr(lin(b), num(a)) if good else fr(lin(-b), num(a))
        q = "Are %s and %s inverses?" % (B("%s = %s" % (FX, L(a, b))), B("%s = %s" % (GX, gtxt)))
        if good:
            right = "Yes, because <i>f</i>(<i>g</i>(<i>x</i>)) = <i>x</i>"
            e = "<i>f</i>(<i>g</i>(<i>x</i>)) = %d · %s %s %d = (%s) %s %d = <i>x</i>. <b>%s</b>." % (a, gtxt, "+" if b > 0 else MINUS, abs(b), lin(b), "+" if b > 0 else MINUS, abs(b), right)
        else:
            right = "No, because <i>f</i>(<i>g</i>(<i>x</i>)) ≠ <i>x</i>"
            e = "<i>f</i>(<i>g</i>(<i>x</i>)) = (%s) %s %d = %s, not <i>x</i>. <b>%s</b>." % (lin(-b), "+" if b > 0 else MINUS, abs(b), poly([1, 2 * b]), right)
        return T(q, right, [x for x in ["Yes, because <i>f</i>(<i>g</i>(<i>x</i>)) = <i>x</i>", "No, because <i>f</i>(<i>g</i>(<i>x</i>)) ≠ <i>x</i>",
                                        "Yes, because <i>f</i>(<i>x</i>) · <i>g</i>(<i>x</i>) = 1", "No, because they have different slopes"] if x != right], e)
    if kind == "hline":
        items = [("Which function has an inverse that is also a function?", "<i>f</i>(<i>x</i>) = <i>x</i>³", ["<i>f</i>(<i>x</i>) = <i>x</i>²", "<i>f</i>(<i>x</i>) = |<i>x</i>|", "<i>f</i>(<i>x</i>) = <i>x</i>⁴ + 1"],
                  "<i>x</i>³ passes the horizontal line test: each output comes from exactly one input."),
                 ("Why does <i>f</i>(<i>x</i>) = <i>x</i>² not have an inverse function on all real numbers?", "Two inputs give the same output, such as <i>f</i>(2) = <i>f</i>(%s2)" % MINUS,
                  ["Its graph is not a straight line", "It has no <i>y</i>-intercept", "Its outputs can be negative"], "A horizontal line meets the parabola twice, so it fails the horizontal line test."),
                 ("The graph of an inverse function is the reflection of the original graph over which line?", "<i>y</i> = <i>x</i>", ["The <i>x</i>-axis", "The <i>y</i>-axis", "<i>y</i> = %s<i>x</i>" % MINUS],
                  "Swapping <i>x</i> and <i>y</i> reflects every point over the line <i>y</i> = <i>x</i>."),
                 ("A point (3, 8) is on the graph of <i>f</i>. Which point must be on the graph of <i>f</i><sup>%s1</sup>?" % MINUS, "(8, 3)", ["(3, 8)", "(%s3, %s8)" % (MINUS, MINUS), "(%s, %s)" % (fr(1, 3), fr(1, 8))],
                  "The inverse swaps the coordinates.")]
        q, right, wr, e = r.choice(items)
        return T(q, right, wr, e + " <b>%s</b>." % right)
    pp = People(r)
    nm, he, his = pp.next()
    rate, fee = r.choice([(15, 20), (12, 30), (25, 10), (18, 25), (40, 15)])
    q = ("A tutor charges %s per hour plus a %s booking fee, so C(<i>h</i>) = %d<i>h</i> + %d. %s paid %s. Use the inverse to find how many hours %s booked." % (
        "$" + num(rate), "$" + num(fee), rate, fee, nm, "$" + num(rate * 3 + fee), he))
    return T(q, "3 hours", ["%s hours" % num(F(rate * 3 + fee, rate)), "%s hours" % num(rate * 3 + fee - fee + 1) if False else "4 hours", "%s hours" % num(F(rate * 3, fee)) if num(F(rate * 3, fee)) else "2 hours"],
             "The inverse is <i>h</i> = (C %s %d) ÷ %d. (%d %s %d) ÷ %d = <b>3 hours</b>." % (MINUS, fee, rate, rate * 3 + fee, MINUS, fee, rate))


def build():
    sets = [S("Operations on functions", collect(one_ops, 20, R)),
            S("Evaluate compositions", collect(one_eval, 20, R)),
            S("Write a composition", collect(one_comp, 20, R)),
            S("Find the inverse", collect(one_inv, 20, R)),
            S("Check inverses and problems", collect(one_check, 20, R))]
    body = lesson(
        "<p>Functions can be added, subtracted, multiplied and divided like expressions: (<i>f</i> + <i>g</i>)(<i>x</i>) = <i>f</i>(<i>x</i>) + <i>g</i>(<i>x</i>).</p>"
        "<p>A <b>composition</b> <i>f</i>(<i>g</i>(<i>x</i>)) puts the output of <i>g</i> into <i>f</i>. Work from the inside out. Usually <i>f</i>(<i>g</i>(<i>x</i>)) ≠ <i>g</i>(<i>f</i>(<i>x</i>)).</p>"
        "<p>An <b>inverse</b> <i>f</i><sup>%s1</sup> undoes <i>f</i>. To find it, swap <i>x</i> and <i>y</i> and solve for <i>y</i>. "
        "Two functions are inverses when <i>f</i>(<i>g</i>(<i>x</i>)) = <i>x</i> and <i>g</i>(<i>f</i>(<i>x</i>)) = <i>x</i>. "
        "A function has an inverse function only if it passes the <b>horizontal line test</b>.</p>" % MINUS,
        [("<i>f</i>(<i>x</i>) = <i>x</i>² + 1 and <i>g</i>(<i>x</i>) = 2<i>x</i> %s 3. Find <i>f</i>(<i>g</i>(2))." % MINUS, ["<i>g</i>(2) = 1", "<i>f</i>(1) = 2"], "2"),
         ("Find the inverse of <i>f</i>(<i>x</i>) = 4<i>x</i> + 7.", ["<i>x</i> = 4<i>y</i> + 7", "<i>y</i> = (<i>x</i> %s 7)/4" % MINUS], "<i>f</i><sup>%s1</sup>(<i>x</i>) = (<i>x</i> %s 7)/4" % (MINUS, MINUS))],
        ["Multiplying <i>f</i>(<i>x</i>) · <i>g</i>(<i>x</i>) when the question asks for <i>f</i>(<i>g</i>(<i>x</i>)).",
         "Evaluating the outer function first. Start with the inside.",
         "Writing <i>f</i><sup>%s1</sup>(<i>x</i>) as 1/<i>f</i>(<i>x</i>). The %s1 is not an exponent here." % (MINUS, MINUS),
         "Undoing the steps in the same order. Undo them in reverse order."])
    faq = [("How do you find f(g(x))?", "Replace every x in f with the whole expression g(x), then simplify."),
           ("How do you find the inverse of a function?", "Write y = f(x), swap x and y, and solve for y. The result is the inverse function."),
           ("How can you tell if two functions are inverses?", "Compose them both ways. If f(g(x)) = x and g(f(x)) = x, they are inverses."),
           ("What is the horizontal line test?", "If any horizontal line crosses a graph more than once, the function is not one-to-one, so its inverse is not a function.")]
    make("composition-and-inverse-functions", 7, "F-BF.B.4",
         "Function Composition and Inverse Functions",
         "Composition and Inverse Functions Worksheet: f(g(x)), Finding Inverses (Algebra 2) | 100 Questions",
         "Composition and Inverses",
         "Find inverse functions. Solve an equation of the form f(x) = c for a simple function f that has an inverse and write an expression for the inverse.",
         "Free Algebra 2 worksheet on function operations, composition f(g(x)), finding inverses, verifying inverses and the horizontal line test. 100 questions with answers.",
         "f(g(x)): work from the inside out. To find an inverse, swap x and y and solve.",
         "f and g are inverses when f(g(x)) = x.",
         body, faq, sets, R, domain="Functions", grade="algebra-2")


if __name__ == "__main__":
    build()
