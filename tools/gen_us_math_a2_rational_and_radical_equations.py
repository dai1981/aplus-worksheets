# -*- coding: utf-8 -*-
"""
US Algebra 2: Rational and Radical Equations (Common Core A-REI.A.2, A-CED.A.1)
  python3 tools/gen_us_math_a2_rational_and_radical_equations.py
Proportions, rational equations with extraneous solutions, radical equations, radical equations with
extraneous solutions and rational exponents, and work and rate problems.
Wrong answers come from real mistakes: keeping a solution that makes a denominator zero, squaring only one
term instead of the whole side, forgetting to check a squared equation, and adding work times instead of
rates.
"""
import math
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, num, MINUS, fr, People
from a2_common import X, poly, sf, lin

R = random.Random(95601)


def hrs(v):
    return "%s hour%s" % (sf(v), "" if F(v) == 1 else "s")


def xs(vals):
    vals = sorted(set(vals))
    return "<i>x</i> = " + ", ".join(sf(v) for v in vals) if vals else "No solution"


# ------------------------------------------------------------ set 1: proportions
def one_prop(r):
    a, b = r.sample([x for x in range(-6, 7) if x], 2)
    x0 = r.choice([x for x in range(-8, 9) if x not in (a, b)])
    m = r.randint(2, 7)
    n = F(m) * (x0 - b) / (x0 - a)
    if n.denominator != 1 or n == 0 or n == m:
        return None
    n = int(n)
    q = "Solve %s." % B("%s = %s" % (fr(num(m), lin(a)), fr(sf(n), lin(b))))
    right = xs([x0])
    # m(x - b) = n(x - a)  ->  (m - n)x = mb - na
    bad = F(m * b + n * a, m - n) if m != n else None
    wr = [xs([bad]) if bad is not None and bad != x0 else xs([x0 + 1]), xs([-x0]), xs([x0 + 2])]
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3],
             "Cross-multiply: %d(%s) = %s(%s). Then %d<i>x</i> %s %d = %s<i>x</i> %s %d, so <i>x</i> = <b>%s</b>. Check: it does not make a denominator 0." % (
                 m, lin(b), sf(n), lin(a), m, MINUS if b > 0 else "+", abs(m * b), sf(n), MINUS if n * a > 0 else "+", abs(n * a), sf(x0)))


# ------------------------------------------------------------ set 2: rational equations, extraneous solutions
def one_ext(r):
    kind = r.choice(["ext", "ext", "two", "lcd"])
    if kind == "ext":
        a = r.choice([x for x in range(-5, 6) if x])
        good = r.choice([x for x in range(-6, 7) if x != a])
        # x/(x-a) - c/(x-a) style producing (x-a)(x-good)=0 after clearing: x^2/(x-a) = ... use x^2 - (a+good)x + a*good = 0
        # equation: x²/(x − a) = ((a + good)x − a·good)/(x − a)
        top2 = poly([a + good, -a * good]) if a + good else sf(-a * good)
        q = "Solve %s." % B("%s = %s" % (fr(X + "²", lin(a)), fr(top2, lin(a))))
        right = xs([good])
        return T(q, right, [xs([a, good]), xs([a]), "No solution"],
                 "Multiply both sides by (%s): <i>x</i>² = %s, so %s(%s) = 0 and <i>x</i> = %s or %s. But <i>x</i> = %s makes the denominator 0, so it is extraneous. <b>%s</b>." % (
                     lin(a), top2, "<i>x</i>" if good == 0 else "(%s)" % lin(good), lin(a), sf(a), sf(good), sf(a), right))
    if kind == "two":
        p, q_ = r.sample([x for x in range(-6, 7) if x], 2)
        # x + c/x = s  -> x^2 - s x + c = 0 with roots p, q
        s, c = p + q_, p * q_
        q = "Solve %s." % B("%s + %s = %s" % (X, fr(sf(c), X), sf(s)) if c > 0 else "%s %s %s = %s" % (X, MINUS, fr(num(-c), X), sf(s)))
        right = xs([p, q_])
        return T(q, right, [xs([-p, -q_]), xs([max(p, q_)]), xs([s])],
                 "Multiply by <i>x</i>: <i>x</i>² %s %s<i>x</i> %s %s = 0, so (<i>x</i> %s %s)(<i>x</i> %s %s) = 0. Neither solution is 0, so both work. <b>%s</b>." % (
                     MINUS if s >= 0 else "+", num(abs(s)) if abs(s) != 1 else "", "+" if c > 0 else MINUS, num(abs(c)), MINUS if p > 0 else "+", num(abs(p)), MINUS if q_ > 0 else "+", num(abs(q_)), right))
    a = r.choice([2, 3, 4, 5, 6])
    b = r.choice([2, 3, 4, 6])
    x0 = r.choice([x for x in range(1, 13)])
    # 1/a + 1/x = 1/b?  -> 1/x = 1/b - 1/a
    if a <= b:
        return None
    inv = F(1, b) - F(1, a)
    x0 = 1 / inv
    if x0.denominator != 1:
        return None
    q = "Solve %s." % B("%s + %s = %s" % (fr(1, a), fr(1, X), fr(1, b)))
    right = xs([x0])
    return T(q, right, [xs([a - b]), xs([a + b]), xs([F(a * b, a + b)])],
             "%s = %s %s %s = %s, so <i>x</i> = <b>%s</b>. (Subtracting denominators, %d %s %d, is a common mistake.)" % (fr(1, X), fr(1, b), MINUS, fr(1, a), sf(inv), sf(x0), a, MINUS, b))


# ------------------------------------------------------------ set 3: radical equations
def one_rad(r):
    kind = r.choice(["basic", "basic", "iso", "cube", "exp"])
    if kind == "basic":
        a, b = r.randint(1, 6), r.randint(-8, 8)
        k = r.randint(1, 8)
        x0 = F(k * k - b, a)
        if x0.denominator != 1:
            return None
        q = "Solve %s." % B("√(%s) = %d" % (poly([a, b]), k))
        right = xs([x0])
        return T(q, right, [xs([F(k - b, a)]), xs([F(k * k + b, a)]), xs([-x0]) if x0 else xs([1])],
                 "Square both sides: %s = %d, so <i>x</i> = <b>%s</b>. Check: √(%s) = %d. ✓" % (poly([a, b]), k * k, sf(x0), sf(a * x0 + b), k))
    if kind == "iso":
        c, k = r.randint(1, 9), r.randint(1, 7)
        a = r.randint(1, 4)
        x0 = F(k * k, a)
        if x0.denominator != 1:
            return None
        q = "Solve %s." % B("√(%s) + %d = %d" % (poly([a, 0]), c, k + c))
        return T(q, xs([x0]), [xs([F((k + c) ** 2 - c, a)]), xs([F((k + c) ** 2, a)]), xs([F(k, a)])],
                 "Isolate the radical first: √(%s) = %d. Then square: %s = %d, <i>x</i> = <b>%s</b>." % (poly([a, 0]), k, poly([a, 0]), k * k, sf(x0)))
    if kind == "cube":
        a, b, k = r.randint(1, 4), r.randint(-6, 6), r.choice([-3, -2, 2, 3, 4])
        x0 = F(k ** 3 - b, a)
        if x0.denominator != 1:
            return None
        q = "Solve %s." % B("∛(%s) = %s" % (poly([a, b]), sf(k)))
        return T(q, xs([x0]), [xs([F(k * k - b, a)]), xs([F(3 * k - b, a)]), xs([F(-k ** 3 - b, a)])],
                 "Cube both sides: %s = %s, so <i>x</i> = <b>%s</b>. A cube root can equal a negative number." % (poly([a, b]), sf(k ** 3), sf(x0)))
    b = r.choice([2, 3, 4, 5])
    n = r.choice([2, 3])
    val = b ** n
    q = "Solve %s." % B("%s<sup>%d/%d</sup> = %d" % (X, n, 1 if False else 1, val) if False else "%s<sup>%s</sup> = %d" % (X, "%d/2" % n if n == 3 else "2/3", val if n == 3 else b * b))
    if n == 3:
        x0 = b * b
        e = "Raise both sides to the 2/3 power: <i>x</i> = %d<sup>2/3</sup> = (∛%d)² = %d² = <b>%d</b>." % (val, val, b, x0)
        return T(q, xs([x0]), [xs([val * 3 // 2]) if (val * 3) % 2 == 0 else xs([val]), xs([b]), xs([val ** 2])], e)
    x0s = [b ** 3, -b ** 3]
    e = "Raise both sides to the 3/2 power: (<i>x</i><sup>2/3</sup>)<sup>3/2</sup> = |<i>x</i>|, so <i>x</i> = ±%d<sup>3/2</sup> = ±%d. Both check, because (%s)<sup>2/3</sup> = %d too. <b>%s</b>." % (
        b * b, b ** 3, sf(-b ** 3), b * b, xs(x0s))
    return T(q, xs(x0s), [xs([b ** 3]), xs([b]), xs([b ** 2 * 3 // 2]) if (b * b * 3) % 2 == 0 else xs([b ** 4])], e)


# ------------------------------------------------------------ set 4: radical equations with extraneous solutions
def one_radext(r):
    p_, q_ = r.sample(range(-3, 10), 2)
    lo, hi = sorted([p_, q_])
    # √(x + c) = x - d   with solutions of x - d = s, s >= 0 one positive one negative
    d = r.randint(-3, 6)
    s1, s2 = r.randint(1, 6), -r.randint(1, 6)
    # x - d = s => x = d + s; x + c = s^2 => c = s^2 - x
    xa, xb = d + s1, d + s2
    c = s1 * s1 - xa
    if s2 * s2 - xb != c:
        # need both to satisfy squared eq: s^2 - s - (d + c) = 0 -> s1 + s2 = 1
        s2 = 1 - s1
        xb = d + s2
        if s2 >= 0:
            return None
        if s2 * s2 - xb != c:
            return None
    q = "Solve %s." % B("√(%s) = %s" % (poly([1, c]) if c else X, lin(d) if d else X))
    right = xs([xa])
    return T(q, right, [xs([xa, xb]), xs([xb]), "No solution"],
             "Square both sides: %s = (%s)². This gives <i>x</i> = %s or <i>x</i> = %s. Check: <i>x</i> = %s makes the right side %s, but a square root cannot be negative, so it is extraneous. <b>%s</b>." % (
                 poly([1, c]) if c else X, lin(d) if d else X, sf(xa), sf(xb), sf(xb), sf(s2), right))


# ------------------------------------------------------------ set 5: work and rate problems
def one_word(r):
    pp = People(r)
    n1, he, his = pp.next()
    n2, she, her = pp.next()
    kind = r.choice(["work", "work", "boat", "pipe", "find"])
    if kind == "work":
        a, b = r.choice([(3, 6), (4, 12), (6, 12), (2, 3), (5, 20), (10, 15), (6, 3), (12, 4)])
        t = F(a * b, a + b)
        q = "%s can paint a fence in %d hours, and %s can paint it in %d hours. How long will it take them working together?" % (n1, a, n2, b)
        return T(q, hrs(t) if t != 1 else "1 hour", [hrs(F(a + b, 2)), hrs(a + b), hrs(abs(a - b)) if a != b else "2 hours"],
                 "Add the rates: %s + %s = %s, which is %s of the job per hour. Time = 1 ÷ %s = <b>%s</b>." % (fr(1, a), fr(1, b), fr(1, X), sf(F(a + b, a * b)), sf(F(a + b, a * b)), hrs(t)))
    if kind == "find":
        a, b = r.choice([(6, 3), (12, 4), (10, 6), (20, 5), (15, 10), (12, 6)])
        t = F(a * b, a - b) if a > b else None
        # together time b, one alone a -> other alone t
        tog, alone = b, a
        other = F(alone * tog, alone - tog)
        q = "Two pumps together drain a pool in %d hours. The first pump alone takes %d hours. How long would the second pump take alone?" % (tog, alone)
        return T(q, hrs(other), [hrs(alone - tog), hrs(F(alone + tog, 2)), hrs(alone + tog)],
                 "%s + %s = %s. So %s = %s, and <i>x</i> = <b>%s</b>." % (fr(1, alone), fr(1, X), fr(1, tog), fr(1, X), sf(F(1, tog) - F(1, alone)), hrs(other)))
    if kind == "boat":
        c = r.choice([2, 3, 4, 5])
        v = r.choice([8, 10, 12, 15, 18])
        d1 = r.choice([2, 3, 4, 5]) * (v + c)
        t = F(d1, v + c)
        d2 = t * (v - c)
        q = ("A boat travels %d miles downstream in the same time it travels %s miles upstream. The current is %d mph. What is the boat's speed in still water?" % (d1, sf(d2), c))
        return T(q, "%d mph" % v, ["%d mph" % (v + c), "%d mph" % (v - c), "%s mph" % sf(F(d1 + d2, 2))],
                 "Same time: %s = %s. Cross-multiply and solve: <i>r</i> = <b>%d mph</b>." % (fr(num(d1), "<i>r</i> + %d" % c), fr(sf(d2), "<i>r</i> %s %d" % (MINUS, c)), v))
    a = r.choice([4, 6, 8, 10])
    b = r.choice([2, 3, 4])
    q = "A tank fills in %d hours with the inlet open. The drain alone empties it in %d hours. If both are open, how long does it take to fill the empty tank?" % (b, a)
    if a <= b:
        return None
    t = F(a * b, a - b)
    return T(q, hrs(t), [hrs(F(a * b, a + b)), hrs(a - b), hrs(a + b)],
             "Net rate = %s %s %s = %s per hour. Time = <b>%s</b>." % (fr(1, b), MINUS, fr(1, a), sf(F(1, b) - F(1, a)), hrs(t)))


def build():
    sets = [S("Proportions", collect(one_prop, 20, R)),
            S("Rational equations and extraneous solutions", collect(one_ext, 20, R)),
            S("Radical equations", collect(one_rad, 20, R)),
            S("Radical equations with extraneous solutions", collect(one_radext, 20, R)),
            S("Work and rate problems", collect(one_word, 20, R))]
    body = lesson(
        "<p>To solve a <b>rational equation</b>, multiply every term by the LCD to clear the fractions, solve, and then <b>check</b>: "
        "a solution that makes any denominator 0 is <b>extraneous</b> and must be thrown out.</p>"
        "<p>To solve a <b>radical equation</b>, isolate the radical, then raise both sides to the same power (square for √, cube for ∛). "
        "Squaring can create extraneous solutions, so check every answer in the original equation.</p>"
        "<p>For work problems, add the <b>rates</b> (jobs per hour): 1/<i>a</i> + 1/<i>b</i> = 1/<i>t</i>.</p>",
        [("Solve √(<i>x</i> + 7) = <i>x</i> + 1.", ["Square: <i>x</i> + 7 = <i>x</i>² + 2<i>x</i> + 1", "<i>x</i>² + <i>x</i> %s 6 = 0, so <i>x</i> = 2 or %s3" % (MINUS, MINUS),
          "Check %s3: √4 = 2 but %s3 + 1 = %s2. Extraneous." % (MINUS, MINUS, MINUS)], "<i>x</i> = 2"),
         ("One worker takes 4 hours, another takes 6 hours. How long together?", ["1/4 + 1/6 = 5/12 per hour"], "12/5 = 2.4 hours")],
        ["Keeping a solution that makes a denominator 0.",
         "Squaring term by term: (<i>x</i> + 1)² is <i>x</i>² + 2<i>x</i> + 1, not <i>x</i>² + 1.",
         "Squaring before isolating the radical.",
         "Adding or averaging the times in a work problem instead of adding the rates."])
    faq = [("What is an extraneous solution?", "A value that comes out of the algebra but does not satisfy the original equation, usually because it makes a denominator zero or a square root negative."),
           ("How do you solve a rational equation?", "Multiply both sides by the least common denominator, solve the resulting equation, and check each answer in the original."),
           ("How do you solve a radical equation?", "Isolate the radical, raise both sides to the index (square a square root), solve, and check for extraneous solutions."),
           ("How do you solve a work problem?", "Add the rates. If one person takes a hours and another takes b hours, together they do 1/a + 1/b of the job each hour.")]
    make("rational-and-radical-equations", 6, "A-REI.A.2",
         "Rational and Radical Equations",
         "Rational and Radical Equations Worksheet: Extraneous Solutions (Algebra 2, A-REI.A.2) | 100 Questions",
         "Rational and Radical Equations",
         "Solve simple rational and radical equations in one variable, and give examples showing how extraneous solutions may arise.",
         "Free Algebra 2 worksheet on rational and radical equations: proportions, extraneous solutions, square and cube root equations, rational exponents and work problems. 100 questions.",
         "Clear fractions with the LCD; isolate a radical and raise both sides to its power.",
         "Always check: answers that make a denominator 0 or a root negative are extraneous.",
         body, faq, sets, R, domain="Rational Expressions and Equations", grade="algebra-2")


if __name__ == "__main__":
    build()
