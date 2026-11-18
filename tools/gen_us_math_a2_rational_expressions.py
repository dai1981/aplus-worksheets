# -*- coding: utf-8 -*-
"""
US Algebra 2: Rational Expressions (Common Core A-APR.D.6, A-APR.D.7)
  python3 tools/gen_us_math_a2_rational_expressions.py
Simplifying and excluded values, multiplying and dividing, adding and subtracting with like and unlike
denominators, complex fractions, and word problems.
Wrong answers come from real mistakes: cancelling terms instead of factors, forgetting excluded values
that cancel, not flipping the second fraction when dividing, and adding denominators.
"""
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, num, MINUS, fr, People
from a2_common import X, poly, sf, lin, pmul

R = random.Random(95501)


def fac(roots, c=1):
    if not roots:
        return sf(c)
    s = "" if c == 1 else (MINUS if c == -1 else num(c))
    return s + "".join("(%s)" % lin(z) for z in roots)


def ex(roots, c=1):
    p = [c]
    for z in roots:
        p = pmul(p, [1, -z])
    return poly(p)


def rf(top, bot):
    return fr(top, bot)


def nz(r, k, avoid=()):
    pool = [x for x in range(-7, 8) if x and x not in avoid]
    return r.sample(pool, k)


# ------------------------------------------------------------ set 1: simplify and excluded values
def one_simp(r):
    a, b, c = nz(r, 3)
    kind = r.choice(["simp", "simp", "simp", "excl"])
    top, bot = ex([a, b]), ex([a, c])
    if kind == "excl":
        q = "What values of <i>x</i> are excluded from the domain of %s?" % B(rf(top, bot))
        right = "<i>x</i> = %s and <i>x</i> = %s" % (sf(min(a, c)), sf(max(a, c)))
        wr = ["<i>x</i> = %s only" % sf(c), "<i>x</i> = %s and <i>x</i> = %s" % (sf(min(-a, -c)), sf(max(-a, -c))), "<i>x</i> = %s and <i>x</i> = %s" % (sf(min(a, b)), sf(max(a, b)))]
        return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3],
                 "Factor the denominator: %s. It is 0 at both values, even though (%s) cancels with the numerator. <b>%s</b>." % (fac([a, c]), lin(a), right))
    q = "Simplify %s." % B(rf(top, bot))
    right = rf(lin(b), lin(c))
    pt, pb = [1, -(a + b), a * b], [1, -(a + c), a * c]
    wr = [rf(lin(-b), lin(-c)), rf(poly(pt[1:]), poly(pb[1:])) if pt[1] and pb[1] else rf(lin(-a), lin(-c)), rf(lin(c), lin(b))]
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3],
             "Factor: %s. Cancel the common factor (%s): <b>%s</b>, with <i>x</i> ≠ %s, %s. (You cannot cancel the <i>x</i>² terms.)" % (
                 rf(fac([a, b]), fac([a, c])), lin(a), right, sf(a), sf(c)))


# ------------------------------------------------------------ set 2: multiply and divide
def one_md(r):
    a, b, c, d = nz(r, 4)
    if r.random() < 0.5:
        q = "Simplify %s." % B("%s · %s" % (rf(ex([a, b]), ex([c, d])), rf(lin(c), lin(a))))
        right = rf(lin(b), lin(d))
        wr = [rf(fac([a, b]), fac([d, a])) if False else rf(lin(a), lin(d)), rf(lin(b), lin(c)), rf(lin(d), lin(b))]
        e = "Factor: %s · %s. Cancel (%s) and (%s): <b>%s</b>." % (rf(fac([a, b]), fac([c, d])), rf(lin(c), lin(a)), lin(a), lin(c), right)
    else:
        q = "Simplify %s." % B("%s ÷ %s" % (rf(ex([a, b]), lin(c)), rf(ex([a, d]), lin(c))))
        right = rf(lin(b), lin(d))
        wr = [rf(fac([a, b]) + fac([a, d]), "(%s)²" % lin(c)), rf(lin(d), lin(b)), rf(lin(b), fac([d, c]))]
        e = "Multiply by the reciprocal: %s · %s. Factor and cancel (%s) and (%s): <b>%s</b>." % (rf(fac([a, b]), lin(c)), rf(lin(c), fac([a, d])), lin(a), lin(c), right)
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)


# ------------------------------------------------------------ set 3: add and subtract
def one_add(r):
    kind = r.choice(["like", "unlike", "unlike", "unlike"])
    if kind == "like":
        a = nz(r, 1)[0]
        m, n = r.randint(1, 9), r.randint(1, 9)
        op = r.choice(["+", MINUS])
        top = m + n if op == "+" else m - n
        if top == 0:
            return None
        cx_ = lambda k: (sf(k) if abs(k) != 1 else (MINUS if k < 0 else "")) + X
        q = "Simplify %s." % B("%s %s %s" % (rf(cx_(m), lin(a)), op, rf(cx_(n), lin(a))))
        right = rf(cx_(top), lin(a))
        wr = [rf(cx_(m + n), "2(%s)" % lin(a)), rf(cx_(m - n if op == "+" else m + n) if (m - n if op == "+" else m + n) else "0", lin(a)), rf(cx_(m * n), lin(a))]
        return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3],
                 "The denominators match, so combine the numerators and keep the denominator: <b>%s</b>. Never add the denominators." % right)
    a, b = nz(r, 2)
    m, n = r.randint(1, 6), r.randint(1, 6)
    op = r.choice(["+", MINUS])
    s = 1 if op == "+" else -1
    # m/(x-a) ± n/(x-b) = (m(x-b) ± n(x-a)) / ((x-a)(x-b))
    top = [m + s * n, -m * b - s * n * a]
    if top[0] == 0 and top[1] == 0:
        return None
    q = "Simplify %s." % B("%s %s %s" % (rf(num(m), lin(a)), op, rf(num(n), lin(b))))
    right = rf(poly(top) if top[0] else sf(top[1]), fac([a, b]))
    bad_top = [m + s * n, -m * a - s * n * b]
    wr = [rf(num(m + s * n) if m + s * n else "0", "%s %s %s" % (poly([2, -(a + b)]), "", "").strip()) if False else rf(sf(m + s * n), poly([2, -a - b])),
          rf(poly(bad_top) if bad_top[0] else sf(bad_top[1]), fac([a, b])),
          rf(poly([m - s * n, -m * b + s * n * a]) if m - s * n else sf(-m * b + s * n * a), fac([a, b]))]
    e = "LCD = %s. Rewrite: %s %s %s. Combine the numerators: %s(%s) %s %s(%s) = %s. <b>%s</b>." % (
        fac([a, b]), rf("%d(%s)" % (m, lin(b)), fac([a, b])), op, rf("%d(%s)" % (n, lin(a)), fac([a, b])), num(m), lin(b), op, num(n), lin(a),
        poly(top) if top[0] else sf(top[1]), right)
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)


# ------------------------------------------------------------ set 4: complex fractions
def one_cx(r):
    kind = r.choice(["num", "num", "var", "var"])
    if kind == "num":
        b, d = r.choice([3, 4, 5, 7]), r.choice([3, 4, 5, 6, 8])
        a, c = r.randint(1, b - 1), r.randint(1, d - 1)
        if __import__("math").gcd(a, b) > 1 or __import__("math").gcd(c, d) > 1:
            return None
        top = F(1, 1) + F(a, b)
        bot = F(c, d) - F(1, 2) if F(c, d) != F(1, 2) else None
        if bot is None or bot == 0:
            return None
        ans = top / bot
        q = "Simplify %s." % B(rf("1 + " + fr(a, b), fr(c, d) + " %s %s" % (MINUS, fr(1, 2))))
        return T(q, sf(ans), [sf(w) for w in dict.fromkeys([top * bot, (1 + a) / F(c - 1) if c != 1 else top, -ans, F(a + b, b) / F(c, d)]) if w != ans][:3],
                 "Top: 1 + %s = %s. Bottom: %s %s %s = %s. Divide: %s ÷ %s = <b>%s</b>." % (fr(a, b), sf(top), fr(c, d), MINUS, fr(1, 2), sf(bot), sf(top), sf(bot), sf(ans)))
    a = r.choice([1, 2, 3, 4, 5])
    # (1/x + a/…)  use (1 + a/x) / (1 - a^2/x^2) = x/(x - a)
    q = "Simplify %s." % B(rf("1 + " + fr(num(a), X), "1 %s %s" % (MINUS, fr(num(a * a), X + "²"))))
    right = rf(X, lin(a))
    wr = [rf(X, lin(-a)), rf(lin(-a), lin(a)), rf(X + "²", lin(a))]
    return T(q, right, wr,
             "Multiply the top and bottom by <i>x</i>²: %s. The bottom is a difference of squares: <i>x</i>(<i>x</i> + %d) ÷ ((<i>x</i> + %d)(<i>x</i> %s %d)) = <b>%s</b>." % (
                 rf("<i>x</i>² + %d<i>x</i>" % a, "<i>x</i>² %s %d" % (MINUS, a * a)), a, a, MINUS, a, right))


# ------------------------------------------------------------ set 5: word problems
def one_word(r):
    pp = People(r)
    nm, he, his = pp.next()
    kind = r.choice(["avg", "work", "cost", "time"])
    if kind == "avg":
        d = r.choice([60, 80, 90, 120, 150, 180])
        k = r.choice([5, 10, 15])
        q = ("%s drives %d miles to a city at <i>x</i> mph and returns at <i>x</i> + %d mph. Which expression gives the total driving time in hours?" % (nm, d, k))
        right = rf("%d(2<i>x</i> + %d)" % (d, k), "<i>x</i>(<i>x</i> + %d)" % k)
        return T(q, right, [rf("%d" % (2 * d), "2<i>x</i> + %d" % k), rf("%d" % d, "<i>x</i>(<i>x</i> + %d)" % k), rf("%d(<i>x</i> + %d)" % (d, k), "<i>x</i>")],
                 "Time = distance ÷ rate: %s + %s. Use the LCD <i>x</i>(<i>x</i> + %d): <b>%s</b>." % (rf(num(d), X), rf(num(d), "<i>x</i> + %d" % k), k, right))
    if kind == "work":
        a, b = r.choice([(3, 6), (4, 12), (6, 3), (2, 6), (10, 15), (5, 20)])
        q = "One pump fills a tank in %d hours and another in %d hours. Working together, what fraction of the tank do they fill in one hour?" % (a, b)
        ans = F(1, a) + F(1, b)
        return T(q, sf(ans), [sf(F(1, a + b)), sf(F(2, a + b)), sf(F(a + b, a * b * 2))], "Add the rates: %s + %s = <b>%s</b> of the tank per hour." % (fr(1, a), fr(1, b), sf(ans)))
    if kind == "cost":
        c = r.choice([120, 180, 240, 300])
        q = "A group shares a %s bus rental equally. With <i>x</i> people each pays %s. If 2 more people join, how much less does each person pay?" % ("$" + num(c), rf("$" + num(c), X))
        right = rf(num(2 * c), "<i>x</i>(<i>x</i> + 2)")
        return T(q, right, [rf(num(c), "<i>x</i> + 2"), rf(num(c), "2"), rf("2", "<i>x</i>(<i>x</i> + 2)")],
                 "%s %s %s = %s = <b>%s</b> dollars." % (rf(num(c), X), MINUS, rf(num(c), "<i>x</i> + 2"), rf("%d(<i>x</i> + 2) %s %d<i>x</i>" % (c, MINUS, c), "<i>x</i>(<i>x</i> + 2)"), right))
    w = r.choice([2, 3, 4])
    q = "A rectangle has area %s and width %s. Which expression is its length?" % (B(ex([-w, 3], 1)), B(lin(-w)))
    right = lin(3)
    return T(q, right, [lin(-3), poly([1, w - 3]) if w != 3 else lin(5), ex([-w, 3]) + " ÷ 2"],
             "Length = area ÷ width. Factor the area: %s. Cancel (%s): <b>%s</b>." % (fac([-w, 3]), lin(-w), right))


def build():
    sets = [S("Simplify and excluded values", collect(one_simp, 20, R)),
            S("Multiply and divide", collect(one_md, 20, R)),
            S("Add and subtract", collect(one_add, 20, R)),
            S("Complex fractions", collect(one_cx, 20, R)),
            S("Word problems", collect(one_word, 20, R))]
    body = lesson(
        "<p>A <b>rational expression</b> is a fraction with polynomials on the top and bottom. Work with them like number fractions, but <b>factor first</b>.</p>"
        "<ul><li><b>Simplify</b>: factor the top and bottom, then cancel common <b>factors</b> (never single terms). The excluded values make the original denominator 0.</li>"
        "<li><b>Multiply</b>: factor, cancel, multiply across. <b>Divide</b>: multiply by the reciprocal.</li>"
        "<li><b>Add or subtract</b>: find the LCD, rewrite each fraction over it, then combine the numerators.</li>"
        "<li><b>Complex fractions</b>: multiply the top and bottom by the LCD of all the small fractions.</li></ul>",
        [("Simplify (<i>x</i>² %s 9) ÷ (<i>x</i>² + 5<i>x</i> + 6)." % MINUS, ["(<i>x</i> + 3)(<i>x</i> %s 3) ÷ ((<i>x</i> + 2)(<i>x</i> + 3))" % MINUS], "(<i>x</i> %s 3)/(<i>x</i> + 2), <i>x</i> ≠ %s3, %s2" % (MINUS, MINUS, MINUS)),
         ("Add 2/(<i>x</i> %s 1) + 3/(<i>x</i> + 2)." % MINUS, ["LCD (<i>x</i> %s 1)(<i>x</i> + 2)" % MINUS, "2(<i>x</i> + 2) + 3(<i>x</i> %s 1) = 5<i>x</i> + 1" % MINUS], "(5<i>x</i> + 1)/((<i>x</i> %s 1)(<i>x</i> + 2))" % MINUS)],
        ["Cancelling terms: (<i>x</i> + 3)/(<i>x</i> + 5) is not 3/5.",
         "Forgetting an excluded value because its factor cancelled.",
         "Adding the denominators. Rewrite over the LCD instead.",
         "Not distributing the minus sign to every term of the second numerator."])
    faq = [("How do you simplify a rational expression?", "Factor the numerator and denominator completely, then cancel common factors. State the values that make the original denominator zero."),
           ("How do you add rational expressions?", "Find the least common denominator, rewrite each fraction with it, add the numerators, and simplify."),
           ("How do you divide rational expressions?", "Multiply the first expression by the reciprocal of the second, then factor and cancel."),
           ("What is an excluded value?", "A value of x that makes a denominator equal to zero. It is not allowed, even if the factor cancels later.")]
    make("rational-expressions", 5, "A-APR.D.7",
         "Rational Expressions: Simplify, Multiply, Divide, Add, and Subtract",
         "Rational Expressions Worksheet: Simplifying, Adding, Multiplying (Algebra 2) | 100 Questions",
         "Rational Expressions",
         "Understand that rational expressions form a system analogous to the rational numbers, closed under addition, subtraction, multiplication, and division by a nonzero rational expression; add, subtract, multiply, and divide rational expressions.",
         "Free Algebra 2 worksheet on rational expressions: simplifying and excluded values, multiplying, dividing, adding with an LCD and complex fractions. 100 questions with answers.",
         "Factor first, then cancel common factors, never single terms.",
         "To add, use the LCD. To divide, multiply by the reciprocal.",
         body, faq, sets, R, domain="Rational Expressions and Equations", grade="algebra-2")


if __name__ == "__main__":
    build()
