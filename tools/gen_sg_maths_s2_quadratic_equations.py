# -*- coding: utf-8 -*-
"""
SG Secondary 2 Maths: Quadratic Equations by Factorisation (MOE syllabus N7 Equations and Inequalities)
  python3 tools/gen_sg_maths_s2_quadratic_equations.py
Solving (x − a)(x − b) = 0, factorising and solving x² + bx + c = 0, special cases (x² = kx, difference of two
squares, common factor), non-monic quadratics, and word problems.
Wrong answers come from real mistakes: keeping the sign from the bracket, dividing both sides by x and losing
x = 0, giving only the positive root of x² = k, and not rearranging to "= 0" first.
"""
import random
from fractions import Fraction as F
from sg_sec import num, S, make, lesson, collect, T, fr, expr, MINUS, People

R = random.Random(820600)
P = People(R)
X = "<i>x</i>"
X2 = X + "²"


def lin(a, b):
    return expr([(a, X), (b, "")])


def quad(a, b, c):
    return expr([(a, X2), (b, X), (c, "")])


def fv(v):
    v = F(v)
    if v.denominator == 1:
        return num(v.numerator)
    s = MINUS if v < 0 else ""
    return s + fr(str(abs(v.numerator)), str(v.denominator))


def sol(rs):
    rs = sorted(set(F(v) for v in rs))
    if len(rs) == 1:
        return "%s = %s" % (X, fv(rs[0]))
    return " or ".join("%s = %s" % (X, fv(v)) for v in rs)


def nz(lo=-9, hi=9, skip=()):
    return [v for v in range(lo, hi + 1) if v != 0 and v not in skip]


# ------------------------------------------------------------ set 1: (x − a)(x − b) = 0
def one_zero(r):
    kind = r.choice(["two", "two", "two", "xk", "lin"])
    if kind == "two":
        a, b = sorted(r.sample(nz(), 2))
        qh = "Solve (%s)(%s) = 0." % (lin(1, -a), lin(1, -b))
        return T(qh, sol([a, b]), [sol([-a, -b]), sol([a, -b]), sol([a * b])],
                 "If a product is 0, one factor is 0. %s = 0 or %s = 0, so <b>%s</b>." % (lin(1, -a), lin(1, -b), sol([a, b])))
    if kind == "xk":
        a = r.choice(nz())
        qh = "Solve %s(%s) = 0." % (X, lin(1, -a))
        return T(qh, sol([0, a]), [sol([a]), sol([-a]), sol([0, -a])],
                 "%s = 0 or %s = 0, so <b>%s</b>. Do not forget %s = 0." % (X, lin(1, -a), sol([0, a]), X))
    p, q = r.choice([2, 3, 4, 5]), r.choice(nz(-7, 7))
    a = r.choice(nz())
    if q % p == 0:
        return None
    qh = "Solve (%s)(%s) = 0." % (lin(p, -q), lin(1, -a))
    return T(qh, sol([F(q, p), a]), [sol([q, a]), sol([F(-q, p), -a]), sol([F(p, q), a])],
             "%s = 0 gives %s = %s. %s = 0 gives %s = %s. <b>%s</b>." % (lin(p, -q), X, fv(F(q, p)), lin(1, -a), X, num(a), sol([F(q, p), a])))


# ------------------------------------------------------------ set 2: factorise and solve x² + bx + c = 0
def one_monic(r):
    a, b = sorted(r.sample(nz(), 2))
    B, C = -(a + b), a * b
    qh = "Solve %s = 0." % quad(1, B, C)
    f = "(%s)(%s)" % (lin(1, -a), lin(1, -b))
    return T(qh, sol([a, b]), [sol([-a, -b]), sol([a, -b]) if a != b else sol([a + 1, b]), sol([B, C]) if {B, C} != {a, b} else sol([a + 1, b - 1])],
             "Find two numbers that multiply to %s and add to %s: %s and %s. %s = 0, so <b>%s</b>." % (num(C), num(B), num(-a), num(-b), f, sol([a, b])))


# ------------------------------------------------------------ set 3: special cases
def one_special(r):
    kind = r.choice(["kx", "kx", "dos", "dos", "cf", "rearr"])
    if kind == "kx":
        k = r.choice(nz(-12, 12))
        qh = "Solve %s = %s." % (X2, expr([(k, X)]))
        return T(qh, sol([0, k]), [sol([k]), sol([0, -k]), sol([k, -k])],
                 "Do not divide by %s. Write %s = 0, so %s(%s) = 0 and <b>%s</b>." % (X, quad(1, -k, 0), X, lin(1, -k), sol([0, k])))
    if kind == "dos":
        a = r.randint(1, 12)
        m = r.choice([1, 1, 2, 3])
        if m == 1:
            qh = "Solve %s = %s." % (X2, num(a * a))
        else:
            qh = "Solve %s = 0." % expr([(m, X2), (-m * a * a, "")])
        return T(qh, sol([a, -a]), [sol([a]), sol([a * a, -a * a]) if m == 1 else sol([m * a, -m * a]), sol([F(a, 2), -F(a, 2)]) if a % 2 == 0 else sol([a + 1, -a - 1])],
                 "%s%s = %s, so %s = ±%s: <b>%s</b>. Remember the negative root." % ("Divide by %d: " % m if m > 1 else "", X2, num(a * a), X, num(a), sol([a, -a])))
    if kind == "cf":
        k = r.choice([2, 3, 4, 5])
        a, b = sorted(r.sample(nz(-6, 6), 2))
        qh = "Solve %s = 0." % quad(k, -k * (a + b), k * a * b)
        return T(qh, sol([a, b]), [sol([-a, -b]), sol([k * a, k * b]), sol([a, b, 0])],
                 "Take out the common factor %d: %d(%s) = 0. Then %d(%s)(%s) = 0, so <b>%s</b>." % (k, k, quad(1, -(a + b), a * b), k, lin(1, -a), lin(1, -b), sol([a, b])))
    a, b = sorted(r.sample(nz(-8, 8), 2))
    B, C = -(a + b), a * b
    if B == 0:
        return None
    qh = "Solve %s = %s." % (expr([(1, X2), (B, X)]), num(-C))
    return T(qh, sol([a, b]), [sol([-a, -b]), sol([-C, -C - B]) if -C not in (a, b) else sol([a + 2, b]), sol([a, -b])],
             "First make one side 0: %s = 0. Factorise: (%s)(%s) = 0, so <b>%s</b>." % (quad(1, B, C), lin(1, -a), lin(1, -b), sol([a, b])))


# ------------------------------------------------------------ set 4: non-monic
def one_nonmonic(r):
    p = r.choice([2, 3, 5])
    q = r.choice([v for v in nz(-7, 7) if v % p != 0])
    b = r.choice(nz(-6, 6))
    # (p x − q)(x − b) = p x² − (p b + q) x + q b
    A, B, C = p, -(p * b + q), q * b
    qh = "Solve %s = 0." % quad(A, B, C)
    right = sol([F(q, p), b])
    wr = [sol([F(-q, p), -b]), sol([q, b]), sol([F(p, q), b]) if abs(q) != 1 else sol([F(q, p), -b])]
    if len({right} | set(wr)) < 4:
        return None
    return T(qh, right, wr, "Factorise: (%s)(%s) = 0. %s = 0 gives %s = %s, and %s = 0 gives %s = %s, so <b>%s</b>." % (
        lin(p, -q), lin(1, -b), lin(p, -q), X, fv(F(q, p)), lin(1, -b), X, num(b), right))


# ------------------------------------------------------------ set 5: problems
def one_prob(r):
    kind = r.choice(["rect", "rect", "cons", "square", "prod", "ball"])
    if kind == "rect":
        w = r.randint(3, 12)
        d = r.randint(2, 7)
        A = w * (w + d)
        qh = "A rectangle is %s cm wide and (%s) cm long. Its area is %s cm². Find %s." % (X, lin(1, d), num(A), X)
        other = -(w + d)
        return T(qh, "%s = %s" % (X, num(w)), ["%s = %s" % (X, num(w + d)), sol([w, other]), "%s = %s" % (X, num(A // d) if A % d == 0 and A // d != w else w + 1)],
                 "%s(%s) = %s gives %s = 0, so (%s)(%s) = 0. %s = %s or %s, but a length cannot be negative, so <b>%s = %s</b>." % (
                     X, lin(1, d), num(A), quad(1, d, -A), lin(1, -w), lin(1, w + d), X, num(w), num(other), X, num(w)))
    if kind == "cons":
        n = r.randint(4, 15)
        pr = n * (n + 1)
        qh = "The product of two consecutive positive whole numbers is %s. What is the smaller number?" % num(pr)
        return T(qh, num(n), [num(n + 1), num(pr // 2), num(n - 1)],
                 "Let the numbers be %s and %s + 1. %s = %s gives (%s)(%s) = 0. The positive answer is <b>%s</b>." % (
                     X, X, quad(1, 1, 0).replace(" + " + X, " + " + X), num(pr), lin(1, -n), lin(1, n + 1), num(n)))
    if kind == "square":
        s = r.randint(3, 12)
        k = r.choice([2, 3, 4, 5])
        # x² + k x = s² + k s  -> (x − s)(x + s + k) = 0 ; a square of side x has area x², a strip k cm wide added
        tot = s * s + k * s
        qh = "A square of side %s cm has a strip %d cm wide added along one side, making a rectangle %s cm by (%s) cm. The rectangle's area is %s cm². Find %s." % (X, k, X, lin(1, k), num(tot), X)
        return T(qh, "%s = %s" % (X, num(s)), ["%s = %s" % (X, num(s + k)), sol([s, -(s + k)]), "%s = %s" % (X, num(s - 1))],
                 "%s = %s gives (%s)(%s) = 0. The length must be positive: <b>%s = %s</b>." % (quad(1, k, 0), num(tot), lin(1, -s), lin(1, s + k), X, num(s)))
    if kind == "prod":
        n = r.randint(2, 12)
        k = r.choice([v for v in range(1, 13) if v != n])
        qh = "When a positive number is squared, the result is %d times the number. What is the number?" % k
        return T(qh, num(k), ["0", num(k * k), "%s or 0" % num(k)],
                 "%s = %d%s gives %s(%s) = 0, so %s = 0 or %s = %d. The number is positive: <b>%s</b>." % (X2, k, X, X, lin(1, -k), X, X, k, num(k)))
    t = r.choice([1, 2, 3, 4])
    u = r.choice([v for v in [2, 3, 4, 5, 6] if v > t])
    # h = 5(t − t1)(u − t)... use h = −5t² + 5(t1+t2)t − 5 t1 t2 = 0 at t1, t2
    nm, he, his = P.next()
    B = 5 * (t + u)
    C = 5 * t * u
    qh = "A model rocket's height in metres after <i>t</i> seconds is %s. When is the rocket at a height of %s m? (Solve %s = %s.)" % (
        expr([(B, "<i>t</i>"), (-5, "<i>t</i>²")]), num(C), expr([(B, "<i>t</i>"), (-5, "<i>t</i>²")]), num(C))
    right = "<i>t</i> = %s or <i>t</i> = %s" % (num(t), num(u))
    return T(qh, right, ["<i>t</i> = %s only" % num(u), "<i>t</i> = %s or <i>t</i> = %s" % (num(-t), num(-u)), "<i>t</i> = %s or <i>t</i> = %s" % (num(5 * t), num(5 * u))],
             "Rearrange: 5<i>t</i>² − %s<i>t</i> + %s = 0. Divide by 5: <i>t</i>² − %s<i>t</i> + %s = 0, so (<i>t</i> − %s)(<i>t</i> − %s) = 0. The rocket is at that height going up and coming down: <b>%s</b>." % (
                 num(B), num(C), num(t + u), num(t * u), num(t), num(u), right))


def build():
    sets = [S("Using (x − a)(x − b) = 0", collect(one_zero, 20, R)),
            S("Factorise and solve", collect(one_monic, 20, R)),
            S("Special cases", collect(one_special, 20, R)),
            S("Non-monic quadratics", collect(one_nonmonic, 20, R)),
            S("Word problems", collect(one_prob, 20, R))]
    body = lesson(
        "<ul><li>A <b>quadratic equation</b> has an %s term, for example %s = 0.</li>"
        "<li>Make one side <b>0</b>, factorise the other side, then use: if <i>A</i> × <i>B</i> = 0, then <i>A</i> = 0 or <i>B</i> = 0.</li>"
        "<li>Most quadratic equations have <b>two</b> solutions. Check both in the question: a length or an age cannot be negative.</li></ul>" % (X2, quad(1, -5, 6)),
        [("Solve x² − 5x + 6 = 0.", ["Two numbers that multiply to 6 and add to −5: −2 and −3", "(x − 2)(x − 3) = 0"], "x = 2 or x = 3"),
         ("Solve x² = 7x.", ["x² − 7x = 0", "x(x − 7) = 0"], "x = 0 or x = 7"),
         ("Solve 2x² + x − 3 = 0.", ["(2x + 3)(x − 1) = 0", "2x + 3 = 0 gives x = " + MINUS + fr("3", "2")], "x = " + MINUS + fr("3", "2") + " or x = 1")],
        ["Keeping the sign from the bracket: (x − 4) = 0 gives x = 4, not −4.",
         "Dividing both sides of x² = 7x by x. You lose the answer x = 0.",
         "Giving only x = 5 for x² = 25. The answers are x = 5 or x = −5.",
         "Factorising before making one side 0: x² + 2x = 8 must become x² + 2x − 8 = 0 first."])
    faq = [("How do you solve a quadratic equation by factorisation?", "Rearrange so one side is 0, factorise the quadratic, then set each factor equal to 0 and solve."),
           ("Why does a quadratic equation have two answers?", "Because two different values can make the product of the factors 0. Sometimes both answers are the same, giving one repeated root."),
           ("Can I divide both sides of x² = 3x by x?", "No. That loses the solution x = 0. Write x² − 3x = 0, then x(x − 3) = 0, so x = 0 or x = 3."),
           ("What do I do with a negative answer in a word problem?", "Check whether it makes sense. A length, a time or a number of people cannot be negative, so reject that answer.")]
    make(2, "quadratic-equations", 6, "N7",
         "Quadratic Equations: Solving by Factorisation",
         "", "Quadratic equations", "",
         "Free Secondary 2 maths worksheets on solving quadratic equations by factorisation: (x − a)(x − b) = 0, x² = kx, difference of two squares, non-monic quadratics and word problems. 100 questions with answers.",
         "Make one side 0, factorise, then set each factor equal to 0.",
         "If A × B = 0, then A = 0 or B = 0. Check that each answer makes sense.",
         body, faq, sets, R)


if __name__ == "__main__":
    build()
