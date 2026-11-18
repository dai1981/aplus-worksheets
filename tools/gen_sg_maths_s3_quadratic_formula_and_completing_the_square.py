# -*- coding: utf-8 -*-
"""
SG Secondary 3 Maths: Quadratic Formula and Completing the Square (MOE syllabus N7: solving quadratic
equations by use of formula and by completing the square)
  python3 tools/gen_sg_maths_s3_quadratic_formula_and_completing_the_square.py
Substituting into the formula, rational solutions, answers correct to 2 decimal places (as in O-Level papers),
completing the square, and solving by completing the square. Sets 2 and 4 reuse the US Algebra 1 makers.
Wrong answers come from real mistakes: using b instead of −b, dividing only the square root by 2a, getting
the sign of c wrong in b² − 4ac, and adding b/2 instead of (b/2)².
"""
import random
from math import sqrt
from sg_sec import num, B, S, make, lesson, collect, T, expr, fr, MINUS, adopt
import gen_us_math_a1_quadratic_formula_and_completing_the_square as us

R = random.Random(830300)
adopt(us, R)
X, X2 = us.X, us.X2
quad = us.quad


def d2(v):
    s = "%.2f" % v
    return s.replace("-", MINUS)


def pair(a, b):
    a, b = sorted([a, b])
    return "%s = %s or %s = %s" % (X, d2(a), X, d2(b))


def roots(a, b, c):
    D = b * b - 4 * a * c
    return (-b - sqrt(D)) / (2 * a), (-b + sqrt(D)) / (2 * a)


def ok_irr(a, b, c):
    D = b * b - 4 * a * c
    if D <= 0 or int(sqrt(D)) ** 2 == D:
        return False
    x1, x2 = roots(a, b, c)
    # avoid answers that sit on a rounding boundary
    return all(abs(abs(v) * 100 - int(abs(v) * 100) - 0.5) > 0.02 for v in (x1, x2))


# ------------------------------------------------------------ set 1: substituting into the formula
def one_sub(r):
    a = r.choice([1, 1, 2, 3, 4, 5])
    b = us.nz(r, -9, 9)
    c = us.nz(r, -9, 9)
    D = b * b - 4 * a * c
    if D <= 0:
        return None
    kind = r.choice(["D", "D", "form"])
    if kind == "D":
        q = "For %s, find the value of <i>b</i><sup>2</sup> − 4<i>ac</i>." % B("%s = 0" % quad(a, b, c))
        wr = [num(b * b + 4 * a * c), num(-b * b - 4 * a * c) if -b * b - 4 * a * c != D else num(D + 1), num(b * b - 4 * a * abs(c) if c < 0 else b * b - 2 * a * c)]
        return T(q, num(D), wr, "<i>a</i> = %s, <i>b</i> = %s, <i>c</i> = %s. (%s)<sup>2</sup> − 4(%s)(%s) = %s − (%s) = <b>%s</b>." % (
            num(a), num(b), num(c), num(b), num(a), num(c), num(b * b), num(4 * a * c), num(D)))
    right = "%s = %s" % (X, fr("%s ± √%s" % (num(-b), num(D)), num(2 * a)))
    wr = ["%s = %s" % (X, fr("%s ± √%s" % (num(b), num(D)), num(2 * a))),
          "%s = %s ± %s" % (X, num(-b), fr("√%s" % num(D), num(2 * a))),
          "%s = %s" % (X, fr("%s ± √%s" % (num(-b), num(b * b + 4 * a * c)), num(2 * a))) if b * b + 4 * a * c != D else "%s = %s" % (X, fr("%s ± √%s" % (num(-b), num(D)), num(a)))]
    return T("Which is the correct substitution into the quadratic formula for %s?" % B("%s = 0" % quad(a, b, c)), right, wr,
             "<i>x</i> = (−<i>b</i> ± √(<i>b</i><sup>2</sup> − 4<i>ac</i>)) ÷ 2<i>a</i> with <i>a</i> = %s, <i>b</i> = %s, <i>c</i> = %s gives <b>%s</b>." % (num(a), num(b), num(c), right))


# ------------------------------------------------------------ set 3: answers to 2 decimal places
def one_dp(r):
    a = r.choice([1, 1, 2, 2, 3, 4, 5])
    b = us.nz(r, -9, 9)
    c = us.nz(r, -9, 9)
    if not ok_irr(a, b, c):
        return None
    x1, x2 = roots(a, b, c)
    D = b * b - 4 * a * c
    right = pair(x1, x2)
    wr = [pair(-x1, -x2),
          pair((b - sqrt(D)) / (2 * a) * 1, (b + sqrt(D)) / (2 * a)) if False else pair(-b / (2 * a) - sqrt(D), -b / (2 * a) + sqrt(D)),
          pair((-b - sqrt(b * b + 4 * a * c)) / (2 * a), (-b + sqrt(b * b + 4 * a * c)) / (2 * a)) if b * b + 4 * a * c > 0 else pair(x1 * 2, x2 * 2)]
    if len({right} | set(wr)) < 4:
        return None
    return T("Solve %s, giving your answers correct to 2 decimal places." % B("%s = 0" % quad(a, b, c)), right, wr,
             "<i>x</i> = %s. √%s ≈ %.4f, so <b>%s</b>." % (fr("%s ± √%s" % (num(-b), num(D)), num(2 * a)), num(D), sqrt(D), right))


# ------------------------------------------------------------ set 5: completing the square to 2 d.p. and problems
def one_cs(r):
    kind = r.choice(["cs", "cs", "rect", "rearr", "num"])
    if kind == "cs":
        h = us.nz(r, -6, 6)
        k = r.choice([v for v in range(2, 30) if int(sqrt(v)) ** 2 != v])
        # (x + h)² = k  ->  x² + 2hx + h² − k = 0
        c = h * h - k
        if c == 0:
            return None
        q = "Solve %s by completing the square, giving your answers correct to 2 decimal places." % B("%s = 0" % quad(1, 2 * h, c))
        x1, x2 = -h - sqrt(k), -h + sqrt(k)
        if abs(abs(x1) * 100 % 1 - 0.5) < 0.02 or abs(abs(x2) * 100 % 1 - 0.5) < 0.02:
            return None
        right = pair(x1, x2)
        wr = [pair(h - sqrt(k), h + sqrt(k)), pair(-h - k, -h + k), pair(-h - sqrt(k + 2 * h * h), -h + sqrt(k + 2 * h * h)) if h else pair(x1 - 1, x2 - 1)]
        return T(q, right, wr, "%s = %s. Add %s: (%s)<sup>2</sup> = %s. So %s = ±√%s and <b>%s</b>." % (
            expr([(1, X2), (2 * h, X)]), num(-c), num(h * h), expr([(1, X), (h, "")]), num(k), expr([(1, X), (h, "")]), num(k), right))
    if kind == "rect":
        d = r.randint(1, 6)
        A = r.choice([v for v in range(10, 90) if int(sqrt(d * d + 4 * v)) ** 2 != d * d + 4 * v])
        w = (-d + sqrt(d * d + 4 * A)) / 2
        q = "A rectangle has width <i>x</i> cm and length (%s) cm. Its area is %s cm². Find <i>x</i>, correct to 2 decimal places." % (expr([(1, X), (d, "")]), num(A))
        right = "%s cm" % d2(w)
        wr = ["%s cm" % d2(w + d), "%s cm" % d2((-d - sqrt(d * d + 4 * A)) / 2), "%s cm" % d2(sqrt(A))]
        return T(q, right, wr, "%s = 0. <i>x</i> = %s. A length is positive, so <i>x</i> = <b>%s</b>." % (
            quad(1, d, -A), fr("%s ± √%s" % (num(-d), num(d * d + 4 * A)), "2"), right))
    if kind == "rearr":
        a = r.choice([1, 2, 3])
        b = us.nz(r, -7, 7)
        c = us.nz(r, -7, 7)
        if not ok_irr(a, -b, -c):
            return None
        # a x² = b x + c
        q = "Solve %s = %s, giving your answers correct to 2 decimal places." % (expr([(a, X2)]), expr([(b, X), (c, "")]))
        x1, x2 = roots(a, -b, -c)
        right = pair(x1, x2)
        wr = [pair(*roots(a, b, c)) if ok_irr(a, b, c) else pair(-x1, -x2), pair(-x1, -x2) if ok_irr(a, b, c) else pair(x1 + 1, x2 + 1),
              pair(*roots(a, -b, c)) if ok_irr(a, -b, c) else pair(x1 * 2, x2 * 2)]
        if len({right} | set(wr)) < 4:
            return None
        return T(q, right, wr, "First make one side 0: %s = 0. Then use the formula: <b>%s</b>." % (quad(a, -b, -c), right))
    n = r.randint(3, 12)
    t = r.choice([v for v in range(15, 80) if int(sqrt(1 + 4 * v)) ** 2 != 1 + 4 * v])
    x = (-1 + sqrt(1 + 4 * t)) / 2
    q = "The product of a positive number and 1 more than it is %s. Find the number, correct to 2 decimal places." % num(t)
    return T(q, d2(x), [d2(x + 1), d2((-1 - sqrt(1 + 4 * t)) / 2), d2(sqrt(t))],
             "%s(%s) = %s gives %s = 0. %s = %s, and the positive answer is <b>%s</b>." % (X, expr([(1, X), (1, "")]), num(t), quad(1, 1, -t), X, fr("−1 ± √%s" % num(1 + 4 * t), "2"), d2(x)))


def build():
    sets = [S("Substituting into the formula", collect(one_sub, 20, R)),
            S("Quadratic formula: exact solutions", collect(us.one_rational, 20, R)),
            S("Quadratic formula: answers to 2 decimal places", collect(one_dp, 20, R)),
            S("Completing the square", collect(us.one_complete, 20, R)),
            S("Completing the square and problems", collect(one_cs, 20, R))]
    for s in sets:
        for it in s["items"]:
            for k in ("q", "e"):
                it[k] = it[k].replace("perfect square trinomial", "perfect square")
    body = lesson(
        "<p>For <i>ax</i><sup>2</sup> + <i>bx</i> + <i>c</i> = 0, the <b>quadratic formula</b> is "
        "<i>x</i> = (−<i>b</i> ± √(<i>b</i><sup>2</sup> − 4<i>ac</i>)) ÷ 2<i>a</i>. It works when the quadratic does not factorise.</p>"
        "<p>To <b>complete the square</b> for <i>x</i><sup>2</sup> + <i>px</i>, add (<i>p</i>/2)<sup>2</sup>: <i>x</i><sup>2</sup> + 6<i>x</i> + 9 = (<i>x</i> + 3)<sup>2</sup>.</p>"
        "<p>Make one side 0 first. Give answers correct to 2 decimal places unless the question says otherwise.</p>",
        [("Solve <i>x</i><sup>2</sup> − 4<i>x</i> − 1 = 0, correct to 2 decimal places.", ["<i>a</i> = 1, <i>b</i> = −4, <i>c</i> = −1, so <i>b</i><sup>2</sup> − 4<i>ac</i> = 20", "<i>x</i> = (4 ± √20) ÷ 2"], "<i>x</i> = −0.24 or <i>x</i> = 4.24"),
         ("Solve <i>x</i><sup>2</sup> + 6<i>x</i> − 2 = 0 by completing the square.", ["<i>x</i><sup>2</sup> + 6<i>x</i> = 2", "Add 9: (<i>x</i> + 3)<sup>2</sup> = 11", "<i>x</i> + 3 = ±√11"], "<i>x</i> = −6.32 or <i>x</i> = 0.32")],
        ["Using <i>b</i> instead of −<i>b</i> at the start of the formula.",
         "Dividing only the square root by 2<i>a</i>. The whole top is divided.",
         "Getting the sign of <i>c</i> wrong: for <i>c</i> = −3, −4<i>ac</i> is positive.",
         "Adding <i>p</i>/2 instead of (<i>p</i>/2)<sup>2</sup> when completing the square."])
    faq = [("When should I use the quadratic formula?", "Use it when the quadratic does not factorise easily, or when the question asks for answers correct to 2 decimal places or 3 significant figures."),
           ("What is completing the square?", "Writing x² + px + q as (x + p/2)² − (p/2)² + q. Then you can solve by taking square roots of both sides."),
           ("Why do I get two answers?", "Because a number and its negative have the same square, so ± gives two values of x. In a word problem, reject any answer that does not make sense, such as a negative length."),
           ("What if b² − 4ac is negative?", "Then the equation has no real solutions, and the graph does not cut the x-axis.")]
    make(3, "quadratic-formula-and-completing-the-square", 3, "N7",
         "Quadratic Equations: The Formula and Completing the Square",
         "", "Quadratic formula and completing the square", "",
         "Free Secondary 3 maths worksheets on solving quadratic equations with the quadratic formula and by completing the square, with answers correct to 2 decimal places. 100 questions with answers.",
         "x = (−b ± √(b² − 4ac)) ÷ 2a works for every quadratic equation.",
         "Make one side 0 first. To complete the square, add (half the coefficient of x)².",
         body, faq, sets, R)


if __name__ == "__main__":
    build()
