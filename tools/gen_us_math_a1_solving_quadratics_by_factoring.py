# -*- coding: utf-8 -*-
"""
US Algebra 1: Solving Quadratic Equations by Factoring and Square Roots (Common Core A-REI.B.4b, A-SSE.B.3a)
  python3 tools/gen_us_math_a1_solving_quadratics_by_factoring.py
The zero product property, solving x² + bx + c = 0 and ax² + bx + c = 0 by factoring, setting an equation
equal to zero first, solving by taking square roots, and quadratic word problems (area, projectiles,
consecutive integers, zeros of a function).
Wrong answers come from real mistakes: keeping the sign from the factor (x − 3 = 0 gives 3, not −3), dividing
by x and losing the solution x = 0, factoring before moving every term to one side, and forgetting the
negative square root.
"""
import random
from fractions import Fraction as F
from math import gcd, isqrt
from us_hs import num, B, S, make, lesson, collect, T, expr, fr, MINUS

R = random.Random(91601)
X = "<i>x</i>"
X2 = "<i>x</i><sup>2</sup>"


def lin(a, b):
    return expr([(a, X), (b, "")])


def quad(a, b, c):
    return expr([(a, X2), (b, X), (c, "")])


def nz(r, lo, hi):
    while True:
        k = r.randint(lo, hi)
        if k:
            return k


def sv(v):
    v = F(v)
    return num(v) if v.denominator == 1 else (MINUS if v < 0 else "") + fr(abs(v.numerator), v.denominator)


def sols(*vs):
    vs = sorted(set(F(v) for v in vs))
    if len(vs) == 1:
        return "%s = %s" % (X, sv(vs[0]))
    return " or ".join("%s = %s" % (X, sv(v)) for v in vs)


def uniq(right, wr):
    out = [w for w in dict.fromkeys(wr) if w != right]
    return out[:3] if len(out) >= 3 else None


# ------------------------------------------------------------ set 1: zero product property
def one_zp(r):
    a1, a2 = r.choice([1, 1, 1, 2, 3]), r.choice([1, 1, 2, 5])
    b1, b2 = nz(r, -9, 9), nz(r, -9, 9)
    if F(-b1, a1) == F(-b2, a2):
        return None
    q = "Solve %s." % B("(%s)(%s) = 0" % (lin(a1, b1), lin(a2, b2)))
    right = sols(F(-b1, a1), F(-b2, a2))
    wr = uniq(right, [sols(F(b1, a1), F(b2, a2)), sols(b1, b2) if (a1, a2) != (1, 1) else sols(F(-b1, a1), F(b2, a2)), sols(F(-a1, b1), F(-a2, b2))])
    if not wr:
        return None
    e = "If a product is 0, one of the factors is 0: %s = 0 or %s = 0. So <b>%s</b>." % (lin(a1, b1), lin(a2, b2), right)
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 2: x² + bx + c = 0
def one_simple(r):
    p, q_ = nz(r, -9, 9), nz(r, -9, 9)
    if p == q_ or p + q_ == 0:
        return None
    b, c = -(p + q_), p * q_
    q = "Solve %s by factoring." % B("%s = 0" % quad(1, b, c))
    right = sols(p, q_)
    wr = uniq(right, [sols(-p, -q_), sols(p, -q_), sols(c, 1) if c not in (p, q_) else sols(-c, 1)])
    if not wr:
        return None
    e = "Factor: (%s)(%s) = 0. Set each factor equal to 0: <b>%s</b>." % (lin(1, -p), lin(1, -q_), right)
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 3: rearrange, GCF and a ≠ 1
def one_hard(r):
    kind = r.choice(["gcf", "move", "a", "a"])
    if kind == "gcf":
        a, k = r.choice([2, 3, 4, 5]), nz(r, -9, 9)
        q = "Solve %s." % B("%s = 0" % quad(a, -a * k, 0))
        right = sols(0, k)
        wr = uniq(right, [sols(k), sols(-k, 0), sols(0, a * k)])
        e = "Factor out %d%s: %d%s(%s) = 0. So <b>%s</b>. Do not divide by %s; you would lose %s = 0." % (a, X, a, X, lin(1, -k), right, X, X)
    elif kind == "move":
        p, q_ = nz(r, -8, 8), nz(r, -8, 8)
        if p == q_:
            return None
        b, c = -(p + q_), p * q_
        lhs = X2 if True else ""
        q = "Solve %s." % B("%s = %s" % (X2, expr([(-b, X), (-c, "")])))
        right = sols(p, q_)
        wr = uniq(right, [sols(-p, -q_), sols(-c, 1) if -c not in (p, q_) else sols(c), sols(isqrt(abs(c)), -isqrt(abs(c))) if isqrt(abs(c)) ** 2 == abs(c) and isqrt(abs(c)) not in (abs(p), abs(q_)) else sols(p, -q_)])
        e = "Move every term to one side first: %s = 0. Factor: (%s)(%s) = 0. <b>%s</b>." % (quad(1, b, c), lin(1, -p), lin(1, -q_), right)
    else:
        a1, a2 = r.choice([2, 3]), 1
        b1, b2 = nz(r, -7, 7), nz(r, -7, 7)
        if gcd(a1, abs(b1)) != 1:
            return None
        A, Bc, C = a1 * a2, a1 * b2 + a2 * b1, b1 * b2
        if Bc == 0:
            return None
        q = "Solve %s." % B("%s = 0" % quad(A, Bc, C))
        right = sols(F(-b1, a1), -b2)
        wr = uniq(right, [sols(F(b1, a1), b2), sols(-b1, -b2), sols(F(-b2, a1), -b1)])
        e = "Factor: (%s)(%s) = 0. So %s = 0 or %s = 0: <b>%s</b>." % (lin(a1, b1), lin(a2, b2), lin(a1, b1), lin(a2, b2), right)
    if not wr:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 4: square roots
def one_sqrt(r):
    kind = r.choice(["plain", "coef", "shift", "shift", "none", "irr"])
    if kind == "plain":
        k = r.randint(2, 15)
        q = "Solve %s." % B("%s = %s" % (X2, num(k * k)))
        right = sols(-k, k)
        wr = [sols(k), sols(F(k * k, 2)), sols(-k * k, k * k)]
        e = "Take the square root of both sides, and remember the negative root: <b>%s</b>." % right
    elif kind == "coef":
        a, k = r.choice([2, 3, 4, 5]), r.randint(1, 8)
        c = a * k * k
        q = "Solve %s." % B("%s = 0" % quad(a, 0, -c))
        right = sols(-k, k)
        wr = [sols(k), sols(-isqrt(c) if isqrt(c) ** 2 == c else -c, isqrt(c) if isqrt(c) ** 2 == c else c), sols(F(-c, 2 * a) if F(c, 2 * a) != k else -k * 2, F(c, 2 * a) if F(c, 2 * a) != k else k * 2)]
        e = "Add %s and divide by %d: %s = %s. Square root: <b>%s</b>." % (num(c), a, X2, num(k * k), right)
    elif kind == "shift":
        h, k = nz(r, -8, 8), r.randint(1, 9)
        q = "Solve %s." % B("(%s)<sup>2</sup> = %s" % (lin(1, -h), num(k * k)))
        right = sols(h - k, h + k)
        wr = [sols(h + k), sols(-h - k, -h + k), sols(h - k * k, h + k * k)]
        e = "Square root both sides: %s = ±%d. So %s = %s ± %d: <b>%s</b>." % (lin(1, -h), k, X, num(h), k, right)
    elif kind == "none":
        k = r.randint(1, 20)
        q = "Solve %s." % B("%s + %s = 0" % (X2, num(k)))
        right = "No real solution"
        wr = [sols(-k, k) if isqrt(k) ** 2 != k else sols(-isqrt(k), isqrt(k)), sols(-k), sols(0)]
        e = "%s = −%s, but no real number squared is negative: <b>no real solution</b>." % (X2, num(k))
    else:
        n = r.choice([2, 3, 5, 6, 7, 10, 11, 13])
        q = "Solve %s. Give exact answers." % B("%s = %s" % (X2, num(n)))
        right = "%s = −√%d or %s = √%d" % (X, n, X, n)
        wr = ["%s = √%d" % (X, n), sols(F(-n, 2), F(n, 2)), sols(-n * n, n * n)]
        e = "Square root both sides: <b>%s = ±√%d</b>." % (X, n)
    wr = uniq(right, wr)
    if not wr:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 5: problems
def problems():
    x = X
    data = [
        ("A rectangle is 3 m longer than it is wide. Its area is 40 m². What is its width?", "5 m", ["8 m", "−8 m", "6.3 m"], "<i>w</i>(<i>w</i> + 3) = 40, so <i>w</i><sup>2</sup> + 3<i>w</i> − 40 = 0, (<i>w</i> + 8)(<i>w</i> − 5) = 0. A width cannot be negative: <b>5 m</b>."),
        ("A ball is thrown up. Its height is <i>h</i> = −16<i>t</i><sup>2</sup> + 64<i>t</i>. When does it land?", "After 4 seconds", ["After 2 seconds", "After 16 seconds", "After 64 seconds"], "0 = −16<i>t</i>(<i>t</i> − 4), so <i>t</i> = 0 (thrown) or <b><i>t</i> = 4</b> (lands)."),
        ("The product of two consecutive positive integers is 132. What is the smaller integer?", "11", ["12", "66", "10"], "<i>n</i>(<i>n</i> + 1) = 132, so <i>n</i><sup>2</sup> + <i>n</i> − 132 = 0 and (<i>n</i> + 12)(<i>n</i> − 11) = 0. <b><i>n</i> = 11</b>."),
        ("What are the zeros of <i>f</i>(<i>x</i>) = <i>x</i><sup>2</sup> − 6<i>x</i> + 8?", "2 and 4", ["−2 and −4", "6 and 8", "−4 and 2"], "(<i>x</i> − 2)(<i>x</i> − 4) = 0, so the zeros are <b>2 and 4</b>."),
        ("Where does the graph of <i>y</i> = <i>x</i><sup>2</sup> − <i>x</i> − 12 cross the <i>x</i>-axis?", "(−3, 0) and (4, 0)", ["(3, 0) and (−4, 0)", "(0, −12)", "(−12, 0) and (1, 0)"], "(<i>x</i> − 4)(<i>x</i> + 3) = 0: <b>(−3, 0) and (4, 0)</b>."),
        ("Ethan solves <i>x</i><sup>2</sup> = 5<i>x</i> by dividing both sides by <i>x</i> and gets <i>x</i> = 5. What did he miss?", "<i>x</i> = 0", ["<i>x</i> = −5", "<i>x</i> = 25", "Nothing"], "<i>x</i><sup>2</sup> − 5<i>x</i> = 0 gives <i>x</i>(<i>x</i> − 5) = 0, so <b><i>x</i> = 0</b> is also a solution."),
        ("Maya solves (<i>x</i> − 2)(<i>x</i> + 3) = 6 by writing <i>x</i> − 2 = 6 or <i>x</i> + 3 = 6. Why is this wrong?", "The zero product property only works when the product is 0", ["She should have added 2 and 3", "She forgot the negative root", "It is correct"],
         "Expand and move the 6: <i>x</i><sup>2</sup> + <i>x</i> − 12 = 0, so <i>x</i> = 3 or <i>x</i> = −4. <b>The product must be 0</b>."),
        ("A square garden's area is 81 m². What is its side length?", "9 m", ["−9 m", "40.5 m", "18 m"], "<i>s</i><sup>2</sup> = 81 gives ±9, but a length is positive: <b>9 m</b>."),
        ("A picture with area 48 in.² is 2 in. longer than it is wide. What is its length?", "8 in.", ["6 in.", "−6 in.", "24 in."], "<i>w</i>(<i>w</i> + 2) = 48, so (<i>w</i> + 8)(<i>w</i> − 6) = 0 and <i>w</i> = 6. The length is <b>8 in.</b>"),
        ("Which equation has solutions <i>x</i> = 3 and <i>x</i> = −5?", "(<i>x</i> − 3)(<i>x</i> + 5) = 0", ["(<i>x</i> + 3)(<i>x</i> − 5) = 0", "(<i>x</i> − 3)(<i>x</i> − 5) = 0", "<i>x</i><sup>2</sup> − 15 = 0"], "A solution <i>x</i> = 3 comes from the factor (<i>x</i> − 3): <b>(<i>x</i> − 3)(<i>x</i> + 5) = 0</b>."),
        ("A rock is dropped from 144 ft. Its height is <i>h</i> = 144 − 16<i>t</i><sup>2</sup>. When does it hit the ground?", "After 3 seconds", ["After 9 seconds", "After 12 seconds", "After 4.5 seconds"], "16<i>t</i><sup>2</sup> = 144, so <i>t</i><sup>2</sup> = 9 and <i>t</i> = <b>3</b> (time is positive)."),
        ("How many real solutions does <i>x</i><sup>2</sup> − 10<i>x</i> + 25 = 0 have?", "One", ["Two", "None", "Infinitely many"], "(<i>x</i> − 5)<sup>2</sup> = 0, so <i>x</i> = 5 is the <b>only</b> solution."),
        ("A number squared is 30 more than the number. What are the possible numbers?", "6 or −5", ["−6 or 5", "30 or 1", "5 or 6"], "<i>n</i><sup>2</sup> = <i>n</i> + 30, so (<i>n</i> − 6)(<i>n</i> + 5) = 0: <b>6 or −5</b>."),
        ("A walkway of width <i>x</i> goes around a 10 m by 6 m pool. The total area is 96 m². Which equation fits?", "(10 + 2<i>x</i>)(6 + 2<i>x</i>) = 96", ["(10 + <i>x</i>)(6 + <i>x</i>) = 96", "60 + 2<i>x</i> = 96", "(10 − 2<i>x</i>)(6 − 2<i>x</i>) = 96"],
         "The walkway adds <i>x</i> on each side, so each length grows by 2<i>x</i>: <b>(10 + 2<i>x</i>)(6 + 2<i>x</i>) = 96</b>."),
        ("Solve (10 + 2<i>x</i>)(6 + 2<i>x</i>) = 96 for the walkway width <i>x</i>.", "1 m", ["2 m", "−9 m", "4 m"], "4<i>x</i><sup>2</sup> + 32<i>x</i> + 60 = 96, so <i>x</i><sup>2</sup> + 8<i>x</i> − 9 = 0 and (<i>x</i> + 9)(<i>x</i> − 1) = 0: <b>1 m</b>."),
        ("Solve 2<i>x</i><sup>2</sup> = 50.", "<i>x</i> = −5 or <i>x</i> = 5", ["<i>x</i> = 5", "<i>x</i> = 25", "<i>x</i> = ±√50 only"], "<i>x</i><sup>2</sup> = 25, so <b><i>x</i> = ±5</b>."),
        ("Which method is quickest for (<i>x</i> + 1)<sup>2</sup> = 16?", "Take square roots", ["Factor out the GCF", "Graph only", "Use the zero product property directly"], "Square root both sides: <i>x</i> + 1 = ±4, so <i>x</i> = 3 or <i>x</i> = −5."),
        ("The sum of a number and its square is 56. Which equation fits?", "<i>n</i><sup>2</sup> + <i>n</i> = 56", ["2<i>n</i> = 56", "<i>n</i><sup>2</sup> = 56<i>n</i>", "(<i>n</i> + 1)<sup>2</sup> = 56"], "“A number and its square” gives <b><i>n</i> + <i>n</i><sup>2</sup> = 56</b> (solutions 7 and −8)."),
        ("A ball's height is <i>h</i> = −16<i>t</i><sup>2</sup> + 48<i>t</i>. At what times is it at height 32 ft?", "1 s and 2 s", ["2 s only", "3 s", "0 s and 3 s"], "−16<i>t</i><sup>2</sup> + 48<i>t</i> − 32 = 0 → <i>t</i><sup>2</sup> − 3<i>t</i> + 2 = 0 → (<i>t</i> − 1)(<i>t</i> − 2) = 0: <b>1 s and 2 s</b>."),
        ("What is the first step to solve 3<i>x</i><sup>2</sup> + 6<i>x</i> = 24?", "Subtract 24 so one side is 0", ["Divide both sides by <i>x</i>", "Take the square root", "Factor 3<i>x</i><sup>2</sup> + 6<i>x</i> = 24 into two brackets"],
         "Get 0 on one side first: 3<i>x</i><sup>2</sup> + 6<i>x</i> − 24 = 0, then 3(<i>x</i> + 4)(<i>x</i> − 2) = 0."),
    ]
    return [T(q, a, [w.replace("two brackets", "two binomials") for w in wl], e) for q, a, wl, e in data]


def body():
    return lesson(
        "<p>The <b>zero product property</b>: if <i>A</i> · <i>B</i> = 0, then <i>A</i> = 0 or <i>B</i> = 0. To solve a quadratic by factoring:</p>"
        "<ol><li>Move every term to one side so the other side is <b>0</b>.</li><li>Factor (take out the GCF first).</li>"
        "<li>Set each factor equal to 0 and solve.</li></ol>"
        "<p>If there is no <i>x</i>-term, take <b>square roots</b>: <i>x</i><sup>2</sup> = 49 gives <i>x</i> = ±7. "
        "In real situations, reject answers that make no sense, such as a negative length.</p>",
        [("Solve <i>x</i><sup>2</sup> + 2<i>x</i> = 15.", ["<i>x</i><sup>2</sup> + 2<i>x</i> − 15 = 0.", "(<i>x</i> + 5)(<i>x</i> − 3) = 0."], "<i>x</i> = −5 or <i>x</i> = 3"),
         ("Solve 3<i>x</i><sup>2</sup> − 12<i>x</i> = 0.", ["3<i>x</i>(<i>x</i> − 4) = 0."], "<i>x</i> = 0 or <i>x</i> = 4"),
         ("Solve (<i>x</i> − 2)<sup>2</sup> = 25.", ["<i>x</i> − 2 = ±5."], "<i>x</i> = 7 or <i>x</i> = −3")],
        ["Keeping the sign from the factor: <i>x</i> − 3 = 0 gives <i>x</i> = 3, not −3.",
         "Dividing by <i>x</i> and losing the solution <i>x</i> = 0.",
         "Factoring before the other side is 0: (<i>x</i> − 2)(<i>x</i> + 3) = 6 does not mean <i>x</i> − 2 = 6.",
         "Forgetting the negative root: <i>x</i><sup>2</sup> = 49 has two solutions, 7 and −7."])


def main():
    sets = [S("Zero product property", collect(one_zp, 20, R)),
            S("Solve x² + bx + c = 0 by factoring", collect(one_simple, 20, R)),
            S("Set to zero, GCF and a ≠ 1", collect(one_hard, 20, R)),
            S("Solve by taking square roots", collect(one_sqrt, 20, R)),
            S("Quadratic equation word problems", problems())]
    make("solving-quadratics-by-factoring", 16, "A-REI.B.4",
         "Solving Quadratic Equations by Factoring and Square Roots",
         "Algebra 1 Solving Quadratics by Factoring Worksheets: Zero Product Property and Square Roots (Free, Answer Key)",
         "Solving quadratics by factoring",
         "Solve quadratic equations by inspection (e.g., for x² = 49), taking square roots, completing the square, the quadratic formula and "
         "factoring, as appropriate to the initial form of the equation.",
         "Free Algebra 1 worksheets on solving quadratic equations (A-REI.B.4b): the zero product property, solving by factoring, setting "
         "the equation to zero, solving by square roots and quadratic word problems. 100 questions with an answer key.",
         "Make one side 0, factor, then set each factor equal to 0.",
         "x² = k has two solutions, ±√k. Reject answers that make no sense in the situation.",
         body(),
         [("What is the zero product property?", "If the product of two factors is 0, at least one of the factors must be 0. So (x − 3)(x + 5) = 0 means x = 3 or x = −5."),
          ("Why must one side be zero before factoring?", "The zero product property only works for a product equal to 0. A product of 6 does not tell you what each factor is."),
          ("When should I solve by square roots?", "When there is no x-term, as in x² = 49 or (x − 2)² = 25. Remember both the positive and negative roots."),
          ("Why do word problems sometimes have only one answer?", "A quadratic often gives two solutions, but one may not make sense, such as a negative length or time.")],
         sets, R, domain="Quadratics")


if __name__ == "__main__":
    main()
