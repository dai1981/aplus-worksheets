# -*- coding: utf-8 -*-
"""
SG Secondary 3 Maths: Linear Inequalities and Simultaneous Inequalities (MOE syllabus N7)
  python3 tools/gen_sg_maths_s3_simultaneous_linear_inequalities.py
Solving linear inequalities with negatives and brackets, unknowns on both sides, simultaneous inequalities in
the form a < px + q ≤ b, pairs of separate inequalities with integer solutions, number lines and word problems.
Sets 1 to 3 reuse the US Algebra 1 question makers.
Wrong answers come from real mistakes: not reversing the sign when dividing by a negative number, dividing
only one part of a simultaneous inequality, and including an end point that is not allowed.
"""
import math
import random
from fractions import Fraction as F
from sg_sec import num, S, make, lesson, collect, T, expr, fr, fig, MINUS, People, sgd, adopt
import gen_us_math_a1_multi_step_and_compound_inequalities as us

R = random.Random(830600)
adopt(us, R)
P = People(R)
X = "<i>x</i>"
LT, LE, GT, GE = "&lt;", "≤", "&gt;", "≥"


def fv(v):
    v = F(v)
    return num(v) if v.denominator == 1 else (MINUS if v < 0 else "") + fr(abs(v.numerator), v.denominator)


def band(r):
    a = r.randint(-4, 1)
    return us.one_nl_band(r, a, a + r.randint(2, 5))


def one_and(r):
    return band(r) if r.random() < 0.3 else us.one_and(r)


# ------------------------------------------------------------ set 4: two separate inequalities and integers
def one_pair(r):
    # lower bound from a1 x + b1 > c1 (or ≥), upper bound from a2 x + b2 < c2 (or ≤)
    lo = r.randint(-6, 4)
    hi = lo + r.randint(2, 6)
    s1, s2 = r.choice([GT, GE]), r.choice([LT, LE])
    a1, a2 = r.choice([1, 2, 3, 4, -2, -3]), r.choice([1, 2, 3, 5, -2])
    b1, b2 = r.randint(-7, 7), r.randint(-7, 7)
    # write each inequality so that its solution is x s1 lo and x s2 hi
    def ineq(a, b, sgn, bound):
        val = a * bound + b
        if a < 0:
            sgn = {GT: LT, GE: LE, LT: GT, LE: GE}[sgn]
        return "%s %s %s" % (expr([(a, X), (b, "")]), sgn, num(val))
    i1, i2 = ineq(a1, b1, s1, lo), ineq(a2, b2, s2, hi)
    ints = [n for n in range(lo, hi + 1) if (n > lo or s1 == GE) and (n < hi or s2 == LE)]
    if len(ints) < 2:
        return None
    kind = r.choice(["range", "ints", "ints", "great", "small"])
    qs = "%s satisfies both %s and %s." % (X, i1, i2)
    rng = "%s %s %s %s %s" % (num(lo), {GT: LT, GE: LE}[s1], X, s2, num(hi))
    e0 = "Solve each one: %s %s %s and %s %s %s, so %s." % (X, s1, num(lo), X, s2, num(hi), rng)
    if kind == "range":
        flip = {LT: LE, LE: LT}
        wr = ["%s %s %s %s %s" % (num(lo), flip[{GT: LT, GE: LE}[s1]], X, flip[s2], num(hi)),
              "%s %s %s %s %s" % (num(-hi), {GT: LT, GE: LE}[s1], X, s2, num(-lo)) if lo != -hi else "%s %s %s %s %s" % (num(lo - 1), LE, X, LE, num(hi + 1)),
              "%s %s %s or %s %s %s" % (X, {GT: LT, GE: LE}[s1], num(lo), X, {LT: GT, LE: GE}[s2], num(hi))]
        return T(qs + " Find the range of values of %s." % X, rng, wr, e0 + " <b>%s</b>." % rng)
    if kind == "ints":
        right = ", ".join(num(n) for n in ints)
        allint = list(range(lo, hi + 1))
        w1 = ", ".join(num(n) for n in allint) if allint != ints else ", ".join(num(n) for n in range(lo - 1, hi + 1))
        w2 = ", ".join(num(n) for n in ints[1:]) if len(ints) > 2 else ", ".join(num(n) for n in ints + [hi + 1])
        w3 = ", ".join(num(n) for n in range(lo + 1, hi)) if list(range(lo + 1, hi)) != ints and range(lo + 1, hi) else ", ".join(num(n) for n in ints[:-1] + [hi + 1])
        if len({right, w1, w2, w3}) < 4:
            return None
        return T(qs + " List the integer values of %s." % X, right, [w1, w2, w3], e0 + " The integers are <b>%s</b>." % right)
    if kind == "great":
        return T(qs + " Find the greatest integer value of %s." % X, num(ints[-1]), [num(hi + 1), num(ints[-1] - 1), num(lo)] if ints[-1] == hi else [num(hi), num(ints[-1] - 1), num(lo)],
                 e0 + " The greatest integer is <b>%s</b>%s." % (num(ints[-1]), "" if ints[-1] == hi else " (%s itself is not allowed)" % num(hi)))
    return T(qs + " Find the smallest integer value of %s." % X, num(ints[0]), [num(lo - 1), num(ints[0] + 1), num(hi)] if ints[0] == lo else [num(lo), num(ints[0] + 1), num(hi)],
             e0 + " The smallest integer is <b>%s</b>%s." % (num(ints[0]), "" if ints[0] == lo else " (%s itself is not allowed)" % num(lo)))


# ------------------------------------------------------------ set 5: problems
def one_prob(r):
    nm, he, his = P.next()
    kind = r.choice(["taxi", "load", "mean", "phone", "prime", "frac"])
    if kind == "taxi":
        flag = r.choice([F(39, 10), F(41, 10), F(43, 10), F(45, 10)])
        per = r.choice([F(1, 4), F(3, 10), F(2, 5), F(1, 2)])
        budget = r.choice([15, 20, 25, 30])
        m = (budget - flag) / per
        mx = math.floor(m)
        if m == mx:
            return None
        qh = "A taxi charges %s plus %s for every 400 m. %s has %s. What is the greatest number of 400 m stages %s can pay for?" % (sgd(flag), sgd(per), nm, sgd(budget), he)
        return T(qh, num(mx), [num(mx + 1), num(math.floor(budget / per)), num(math.ceil(m) + 1)],
                 "%s + %s<i>n</i> ≤ %s gives <i>n</i> ≤ %s. The greatest whole number is <b>%s</b>." % (sgd(flag), sgd(per), sgd(budget), ("%.2f" % m), num(mx)))
    if kind == "load":
        lim = r.choice([500, 600, 750, 800, 1000])
        drv = r.choice([60, 65, 70, 75])
        box = r.choice([22, 24, 25, 28, 32, 35])
        n = (lim - drv) // box
        if (lim - drv) % box == 0:
            return None
        qh = "A lift can carry at most %s kg. A worker of mass %d kg rides with boxes of %d kg each. What is the greatest number of boxes?" % (num(lim), drv, box)
        return T(qh, num(n), [num(n + 1), num(lim // box), num(n - 1)],
                 "%d + %d<i>n</i> ≤ %s, so <i>n</i> ≤ %s. The greatest whole number is <b>%d</b>." % (drv, box, num(lim), "%.2f" % ((lim - drv) / box), n))
    if kind == "mean":
        sc = r.sample(range(55, 90), 3)
        tgt = r.choice([70, 72, 75, 78, 80])
        need = 4 * tgt - sum(sc)
        if need > 100 or need < 40:
            return None
        qh = "%s scored %s, %s and %s in three tests. What is the lowest mark on the fourth test that gives a mean of at least %d?" % (nm, sc[0], sc[1], sc[2], tgt)
        return T(qh, num(need), [num(need - 1), num(tgt), num(need + 1)],
                 "(%d + <i>m</i>) ÷ 4 ≥ %d, so <i>m</i> ≥ %d − %d = <b>%d</b>." % (sum(sc), tgt, 4 * tgt, sum(sc), need))
    if kind == "phone":
        a_fix, a_rate = r.choice([(10, F(1, 5)), (15, F(1, 10)), (20, F(1, 20))])
        b_fix, b_rate = r.choice([(5, F(3, 10)), (8, F(1, 4)), (4, F(2, 5))])
        if b_rate <= a_rate:
            return None
        m = F(a_fix - b_fix) / (b_rate - a_rate)
        if m <= 0:
            return None
        qh = ("Plan A costs %s a month plus %s per minute. Plan B costs %s a month plus %s per minute. For how many minutes <i>t</i> is Plan A cheaper?" % (
            sgd(a_fix), sgd(a_rate), sgd(b_fix), sgd(b_rate)))
        right = "<i>t</i> &gt; %s" % fv(m)
        return T(qh, right, ["<i>t</i> &lt; %s" % fv(m), "<i>t</i> &gt; %s" % fv(F(a_fix, 1) / b_rate), "<i>t</i> ≥ %s" % fv(m + 1)],
                 "%s + %s<i>t</i> &lt; %s + %s<i>t</i>. Collect terms: %s<i>t</i> &gt; %s, so <b>%s</b>." % (num(a_fix), "%g" % float(a_rate), num(b_fix), "%g" % float(b_rate), "%g" % float(b_rate - a_rate), num(a_fix - b_fix), right))
    if kind == "prime":
        lo = r.randint(1, 10)
        hi = lo + r.randint(5, 12)
        a = r.choice([2, 3])
        b = r.randint(1, 6)
        primes = [n for n in range(lo + 1, hi + 1) if n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))]
        if not primes:
            return None
        qh = "Find the prime numbers that satisfy %s &lt; %s ≤ %s." % (num(a * lo + b), expr([(a, X), (b, "")]), num(a * hi + b))
        right = ", ".join(map(str, primes))
        allp = [n for n in range(lo, hi + 2) if n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))]
        w1 = ", ".join(map(str, allp)) if allp != primes else ", ".join(map(str, primes + [hi + 1]))
        w2 = ", ".join(map(str, primes[:-1])) if len(primes) > 1 else ", ".join(map(str, [lo]))
        w3 = ", ".join(map(str, range(lo + 1, hi + 1)))
        if len({right, w1, w2, w3}) < 4:
            return None
        return T(qh, right, [w1, w2, w3], "Subtract %d and divide by %d: %d &lt; %s ≤ %d. The primes in this range are <b>%s</b>." % (b, a, lo, X, hi, right))
    a = r.choice([2, 3, 4, 5])
    c = r.choice([2, 3, 4, 6])
    k = r.randint(-5, 6)
    # x/a − 1 < (x − c)/... keep simple: (x + k)/a ≤ c  ->  x ≤ a c − k
    qh = "Solve %s ≤ %s." % (fr(expr([(1, X), (k, "")]), num(a)), num(c))
    right = "%s ≤ %s" % (X, num(a * c - k))
    return T(qh, right, ["%s ≤ %s" % (X, num(c - k)), "%s ≥ %s" % (X, num(a * c - k)), "%s ≤ %s" % (X, fv(F(c - k, a)))],
             "Multiply both sides by %d (positive, so the sign stays): %s ≤ %d. So <b>%s</b>." % (a, expr([(1, X), (k, "")]), a * c, right))


def build():
    sets = [S("Solving linear inequalities", collect(us.one_hard, 20, R)),
            S("Unknowns on both sides", collect(us.one_both, 20, R)),
            S("Simultaneous inequalities in one line", collect(one_and, 20, R)),
            S("Two inequalities and integer solutions", collect(one_pair, 20, R)),
            S("Problems", collect(one_prob, 20, R))]
    body = lesson(
        "<ul><li>Solve an inequality like an equation, but when you <b>multiply or divide by a negative number, reverse the sign</b>.</li>"
        "<li><b>Simultaneous inequalities</b> must both be true. Solve each one, then combine them, for example −2 &lt; <i>x</i> ≤ 5.</li>"
        "<li>For a double inequality such as 3 &lt; 2<i>x</i> + 1 ≤ 9, do the same to all three parts.</li>"
        "<li>On a number line, a filled circle means the end point is included (≤ or ≥); an open circle means it is not (&lt; or &gt;).</li></ul>",
        [("Solve 3 &lt; 2<i>x</i> + 1 ≤ 9.", ["Subtract 1: 2 &lt; 2<i>x</i> ≤ 8", "Divide by 2"], "1 &lt; <i>x</i> ≤ 4"),
         ("Find the integers that satisfy both 3<i>x</i> − 2 ≥ −8 and 5 − <i>x</i> &gt; 1.", ["3<i>x</i> ≥ −6, so <i>x</i> ≥ −2", "−<i>x</i> &gt; −4, so <i>x</i> &lt; 4 (sign reversed)"], "−2, −1, 0, 1, 2, 3")],
        ["Forgetting to reverse the sign when dividing by a negative number.",
         "Dividing only the middle part of a double inequality.",
         "Including an end point that has &lt; or &gt;.",
         "Listing integers outside the range, or missing 0."])
    faq = [("What are simultaneous linear inequalities?", "Two or more inequalities that must all be true at the same time. Solve each one and find the values that satisfy all of them, such as −2 < x ≤ 5."),
           ("When do I reverse the inequality sign?", "Only when you multiply or divide both sides by a negative number. Adding or subtracting never changes the sign."),
           ("How do I find the integer solutions?", "Find the range first, then list the whole numbers inside it. Include an end point only if the sign is ≤ or ≥."),
           ("How do I show the solution on a number line?", "Draw a line between the end points. Use a filled circle for ≤ or ≥ and an open circle for < or >.")]
    make(3, "simultaneous-linear-inequalities", 6, "N7",
         "Linear Inequalities and Simultaneous Inequalities",
         "", "Simultaneous linear inequalities", "",
         "Free Secondary 3 maths worksheets on linear inequalities and simultaneous inequalities: reversing the sign, double inequalities, integer solutions, number lines and word problems. 100 questions with answers.",
         "Reverse the sign when you multiply or divide by a negative number.",
         "Simultaneous inequalities must all be true: solve each, then combine the ranges.",
         body, faq, sets, R)


if __name__ == "__main__":
    build()
