# -*- coding: utf-8 -*-
"""
US Algebra 1: The Quadratic Formula and Completing the Square (Common Core A-REI.B.4a, A-REI.B.4b)
  python3 tools/gen_us_math_a1_quadratic_formula_and_completing_the_square.py
Identifying a, b and c and using the discriminant, solving with the quadratic formula (rational answers and
simplified radical answers), completing the square (the number to add, vertex form and solving), and
choosing a method in real problems.
Wrong answers come from real mistakes: using b instead of −b, dividing only part of the numerator by 2a,
using b² − 4ac with the wrong sign of c, and adding b/2 instead of (b/2)² when completing the square.
"""
import random
from fractions import Fraction as F
from math import gcd, isqrt, sqrt
from us_hs import num, B, S, make, lesson, collect, T, expr, fr, MINUS

R = random.Random(91701)
X = "<i>x</i>"
X2 = "<i>x</i><sup>2</sup>"


def quad(a, b, c, v=X):
    v2 = v + "<sup>2</sup>"
    return expr([(a, v2), (b, v), (c, "")])


def nz(r, lo, hi):
    while True:
        k = r.randint(lo, hi)
        if k:
            return k


def sv(v):
    v = F(v)
    return num(v) if v.denominator == 1 else (MINUS if v < 0 else "") + fr(abs(v.numerator), v.denominator)


def sq_split(n):
    k = 1
    for t in range(isqrt(n), 1, -1):
        if n % (t * t) == 0:
            k = t
            break
    return k, n // (k * k)


def radical_answer(a, b, c):
    """Simplified x = (−b ± k√m)/(2a) as HTML, assuming D > 0 and not a perfect square."""
    D = b * b - 4 * a * c
    k, m = sq_split(D)
    p, d = -b, 2 * a
    g = gcd(gcd(abs(p), k), abs(d))
    p, k, d = p // g, k // g, d // g
    if d < 0:
        p, d = -p, -d
    rad = ("%s√%d" % ("" if k == 1 else num(k), m))
    top = ("%s ± %s" % (num(p), rad)) if p else ("±" + rad)
    if d == 1:
        return "%s = %s" % (X, top)
    return "%s = %s" % (X, fr(top, num(d)))


def uniq(right, wr):
    out = [w for w in dict.fromkeys(wr) if w != right]
    return out[:3] if len(out) >= 3 else None


# ------------------------------------------------------------ set 1: a, b, c and the discriminant
def one_disc(r):
    a, b, c = nz(r, -4, 5), r.randint(-9, 9), r.randint(-9, 9)
    D = b * b - 4 * a * c
    kind = r.choice(["D", "count", "count"])
    eq = "%s = 0" % quad(a, b, c)
    if kind == "D":
        q = "Find the discriminant of %s." % B(eq)
        right = num(D)
        wr = uniq(right, [num(b * b + 4 * a * c), num(-b * b - 4 * a * c) if b else num(4 * a * c), num(b - 4 * a * c), num(b * b - 2 * a * c)])
        e = "<i>b</i><sup>2</sup> − 4<i>ac</i> = (%s)<sup>2</sup> − 4(%s)(%s) = %s − (%s) = <b>%s</b>." % (num(b), num(a), num(c), num(b * b), num(4 * a * c), num(D))
    else:
        q = "How many real solutions does %s have?" % B(eq)
        right = "Two" if D > 0 else ("One" if D == 0 else "None")
        wr = [w for w in ["Two", "One", "None", "Infinitely many"] if w != right]
        e = "The discriminant is %s, which is %s: <b>%s</b>." % (num(D), "positive" if D > 0 else ("zero" if D == 0 else "negative"),
                                                                 {"Two": "two real solutions", "One": "one real solution", "None": "no real solutions"}[right])
    if not wr:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 2: formula with rational answers
def one_rational(r):
    a = r.choice([1, 2, 2, 3, 4])
    p, q_ = F(nz(r, -7, 7), r.choice([1, 1, a if a > 1 else 1])), F(nz(r, -7, 7))
    if p == q_:
        return None
    A = a * p.denominator
    b = -A * (p + q_)
    c = A * p * q_
    if b.denominator != 1 or c.denominator != 1:
        return None
    A, b, c = int(A), int(b), int(c)
    if gcd(gcd(A, abs(b)), abs(c)) != 1 or abs(b) > 40:
        return None
    D = b * b - 4 * A * c
    rt = isqrt(D)
    q = "Use the quadratic formula to solve %s." % B("%s = 0" % quad(A, b, c))
    xs = sorted([p, q_])
    right = "%s = %s or %s = %s" % (X, sv(xs[0]), X, sv(xs[1]))
    w1 = sorted([F(b + rt, 2 * A), F(b - rt, 2 * A)])
    w2 = sorted([F(-b, 2 * A) + rt, F(-b, 2 * A) - rt])
    w3 = sorted([F(-b + rt, A), F(-b - rt, A)])
    wr = uniq(right, ["%s = %s or %s = %s" % (X, sv(u), X, sv(v)) for u, v in (w1, w2, w3)])
    if not wr:
        return None
    e = "<i>a</i> = %s, <i>b</i> = %s, <i>c</i> = %s. <i>b</i><sup>2</sup> − 4<i>ac</i> = %s, and √%s = %s. <i>x</i> = (%s ± %s) ÷ %s, so <b>%s</b>." % (
        num(A), num(b), num(c), num(D), num(D), num(rt), num(-b), num(rt), num(2 * A), right)
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 3: formula with radical answers
def one_radical(r):
    a, b, c = r.choice([1, 1, 2, 3]), r.randint(-8, 8), r.randint(-9, 9)
    D = b * b - 4 * a * c
    if D <= 0 or isqrt(D) ** 2 == D:
        return None
    q = "Use the quadratic formula to solve %s. Give exact answers." % B("%s = 0" % quad(a, b, c))
    right = radical_answer(a, b, c)
    wr = uniq(right, [radical_answer(a, -b, c), radical_answer(a, b, -c) if b * b + 4 * a * c > 0 and isqrt(b * b + 4 * a * c) ** 2 != b * b + 4 * a * c else radical_answer(a, -b, -c) if b * b + 4 * a * c > 0 and isqrt(b * b + 4 * a * c) ** 2 != b * b + 4 * a * c else "%s = %s ± √%d" % (X, num(-b), D),
                      "%s = %s ± √%d" % (X, sv(F(-b, 2 * a)), D), "%s = %s" % (X, fr("%s ± √%d" % (num(-b), D), num(a))) if a > 1 else "%s = %s ± √%d" % (X, num(-b), D)])
    if not wr:
        return None
    k, m = sq_split(D)
    raw = "%s = %s" % (X, fr("%s ± √%d" % (num(-b), D), num(2 * a)))
    if raw == right:
        e = "<i>b</i><sup>2</sup> − 4<i>ac</i> = %s, which is not a perfect square, so <b>%s</b>." % (num(D), right)
    else:
        e = "<i>b</i><sup>2</sup> − 4<i>ac</i> = %s%s. <i>x</i> = %s, which simplifies to <b>%s</b>." % (
            num(D), (" and √%d = %s√%d" % (D, num(k), m)) if k > 1 else "", fr("%s ± √%d" % (num(-b), D), num(2 * a)), right)
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 4: completing the square
def one_complete(r):
    kind = r.choice(["add", "vertex", "solve", "solve"])
    h = nz(r, -8, 8)
    b = 2 * h
    if kind == "add":
        q = "What number should be added to %s to make a perfect square trinomial?" % B(expr([(1, X2), (b, X)]))
        right = num(h * h)
        wr = uniq(right, [num(h), num(abs(b)), num(b * b)])
        e = "Take half of %s and square it: (%s)<sup>2</sup> = <b>%s</b>. Then %s = (%s)<sup>2</sup>." % (num(b), num(h), right, quad(1, b, h * h), expr([(1, X), (h, "")]))
    elif kind == "vertex":
        c = r.randint(-9, 12)
        k = c - h * h
        q = "Write %s in the form (<i>x</i> + <i>p</i>)<sup>2</sup> + <i>q</i>." % B(quad(1, b, c))
        right = "(%s)<sup>2</sup> %s %s" % (expr([(1, X), (h, "")]), "+" if k >= 0 else MINUS, num(abs(k)))
        wr = uniq(right, ["(%s)<sup>2</sup> %s %s" % (expr([(1, X), (h, "")]), "+" if c + h * h >= 0 else MINUS, num(abs(c + h * h))),
                          "(%s)<sup>2</sup> %s %s" % (expr([(1, X), (b, "")]), "+" if c - b * b >= 0 else MINUS, num(abs(c - b * b))),
                          "(%s)<sup>2</sup> %s %s" % (expr([(1, X), (-h, "")]), "+" if k >= 0 else MINUS, num(abs(k)))])
        e = "Half of %s is %s. (%s)<sup>2</sup> = %s, so subtract %s to balance: %s − %s = %s. <b>%s</b>." % (
            num(b), num(h), expr([(1, X), (h, "")]), quad(1, b, h * h), num(h * h), num(c), num(h * h), num(k), right)
        if k == 0:
            return None
    else:
        s = r.randint(1, 7)
        c = h * h - s * s
        if c == 0:
            return None
        q = "Solve %s by completing the square." % B("%s = 0" % quad(1, b, c))
        x1, x2 = sorted([-h - s, -h + s])
        right = "%s = %s or %s = %s" % (X, num(x1), X, num(x2))
        wr = uniq(right, ["%s = %s or %s = %s" % (X, num(h - s), X, num(h + s)), "%s = %s or %s = %s" % (X, num(-h - s * s), X, num(-h + s * s)), "%s = %s" % (X, num(x2))])
        e = "Move %s: %s = %s. Add %s to both sides: (%s)<sup>2</sup> = %s. Square root: %s = ±%d, so <b>%s</b>." % (
            num(c), expr([(1, X2), (b, X)]), num(-c), num(h * h), expr([(1, X), (h, "")]), num(s * s), expr([(1, X), (h, "")]), s, right)
    if not wr:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 5: problems
def problems():
    data = [
        ("A ball is thrown upward: <i>h</i> = −16<i>t</i><sup>2</sup> + 40<i>t</i> + 5. When does it hit the ground, to the nearest tenth of a second?", "2.6 s", ["0.1 s", "2.5 s", "5.0 s"],
         "<i>t</i> = (−40 − √(1600 + 320)) ÷ (−32) = (40 + 43.8) ÷ 32 ≈ <b>2.6 s</b>. The negative answer makes no sense."),
        ("Which method is best for <i>x</i><sup>2</sup> − 9 = 0?", "Square roots or factoring", ["The quadratic formula only", "Completing the square only", "Graphing only"], "<i>x</i><sup>2</sup> = 9 gives ±3 straight away: <b>square roots</b> (or difference of squares)."),
        ("Which method is best for <i>x</i><sup>2</sup> + 3<i>x</i> − 7 = 0?", "The quadratic formula", ["Factoring with integers", "Taking square roots", "The zero product property directly"], "No two integers multiply to −7 and add to 3, so use <b>the quadratic formula</b>."),
        ("The discriminant of a quadratic is 0. What does its graph look like?", "It touches the x-axis at one point", ["It crosses the x-axis twice", "It does not touch the x-axis", "It is a straight line"], "One real solution means the vertex is on the <i>x</i>-axis: <b>it touches at one point</b>."),
        ("The discriminant of a quadratic is −20. How many times does its graph cross the x-axis?", "0", ["1", "2", "20"], "A negative discriminant means no real solutions: <b>0</b> times."),
        ("A rectangle has length 2 cm more than its width and area 20 cm². What is its width, to the nearest hundredth?", "3.58 cm", ["5.58 cm", "4.47 cm", "10 cm"], "<i>w</i><sup>2</sup> + 2<i>w</i> − 20 = 0, so <i>w</i> = (−2 + √84) ÷ 2 ≈ <b>3.58 cm</b>."),
        ("Liam uses the formula on <i>x</i><sup>2</sup> − 6<i>x</i> + 2 = 0 and writes <i>x</i> = (−6 ± √28)/2. What is his mistake?", "−<i>b</i> should be 6, not −6", ["He should use + 4<i>ac</i>", "He should divide by 4", "There is no mistake"],
         "<i>b</i> = −6, so −<i>b</i> = 6: <b><i>x</i> = (6 ± √28)/2 = 3 ± √7</b>."),
        ("Solve <i>x</i><sup>2</sup> + 6<i>x</i> = 7 by completing the square.", "<i>x</i> = −7 or <i>x</i> = 1", ["<i>x</i> = 7 or <i>x</i> = −1", "<i>x</i> = −3 ± √7", "<i>x</i> = 1"], "Add 9: (<i>x</i> + 3)<sup>2</sup> = 16, so <i>x</i> + 3 = ±4: <b>−7 or 1</b>."),
        ("What is the vertex of <i>y</i> = <i>x</i><sup>2</sup> − 8<i>x</i> + 21? (Complete the square.)", "(4, 5)", ["(−4, 5)", "(4, 21)", "(8, 21)"], "<i>y</i> = (<i>x</i> − 4)<sup>2</sup> + 5, so the vertex is <b>(4, 5)</b>."),
        ("For which value of <i>k</i> does <i>x</i><sup>2</sup> + 10<i>x</i> + <i>k</i> = 0 have exactly one solution?", "25", ["10", "5", "100"], "The discriminant 100 − 4<i>k</i> must be 0, so <b><i>k</i> = 25</b>."),
        ("Solve 2<i>x</i><sup>2</sup> + 4<i>x</i> − 1 = 0 to the nearest tenth.", "<i>x</i> ≈ −2.2 or <i>x</i> ≈ 0.2", ["<i>x</i> ≈ 2.2 or <i>x</i> ≈ −0.2", "<i>x</i> ≈ −4.4 or <i>x</i> ≈ 0.4", "No real solution"], "<i>x</i> = (−4 ± √24) ÷ 4 = (−4 ± 4.9) ÷ 4: <b>−2.2 or 0.2</b>."),
        ("A company's profit is <i>P</i> = −<i>x</i><sup>2</sup> + 14<i>x</i> − 40 (in thousands of dollars) when it sells <i>x</i> thousand items. When does it break even?", "At 4 and 10 thousand items", ["At 14 thousand items", "At 7 thousand items", "Never"],
         "−<i>x</i><sup>2</sup> + 14<i>x</i> − 40 = 0 → <i>x</i><sup>2</sup> − 14<i>x</i> + 40 = 0 → (<i>x</i> − 4)(<i>x</i> − 10) = 0: <b>4 and 10</b>."),
        ("What is the sum of the solutions of <i>x</i><sup>2</sup> − 9<i>x</i> + 14 = 0?", "9", ["−9", "14", "5"], "The solutions are 2 and 7, which add to <b>9</b> (the same as −<i>b</i>/<i>a</i>)."),
        ("Which is the quadratic formula?", "<i>x</i> = (−<i>b</i> ± √(<i>b</i><sup>2</sup> − 4<i>ac</i>)) ÷ 2<i>a</i>", ["<i>x</i> = (<i>b</i> ± √(<i>b</i><sup>2</sup> − 4<i>ac</i>)) ÷ 2<i>a</i>", "<i>x</i> = −<i>b</i> ± √(<i>b</i><sup>2</sup> − 4<i>ac</i>) ÷ 2<i>a</i>", "<i>x</i> = (−<i>b</i> ± √(<i>b</i><sup>2</sup> + 4<i>ac</i>)) ÷ 2<i>a</i>"],
         "The whole numerator −<i>b</i> ± √(<i>b</i><sup>2</sup> − 4<i>ac</i>) is divided by 2<i>a</i>."),
        ("Before using the formula on 3<i>x</i><sup>2</sup> = 5<i>x</i> + 2, what should you do?", "Rewrite it as 3<i>x</i><sup>2</sup> − 5<i>x</i> − 2 = 0", ["Use <i>a</i> = 3, <i>b</i> = 5, <i>c</i> = 2", "Divide by <i>x</i>", "Take the square root of both sides"],
         "The formula needs standard form <i>ax</i><sup>2</sup> + <i>bx</i> + <i>c</i> = 0, so <i>b</i> = −5 and <i>c</i> = −2."),
        ("A garden of area 60 m² is 4 m longer than it is wide. What is its width, to the nearest tenth?", "6.0 m", ["10.0 m", "7.7 m", "15.0 m"], "<i>w</i><sup>2</sup> + 4<i>w</i> − 60 = 0 → (<i>w</i> + 10)(<i>w</i> − 6) = 0: <b>6.0 m</b>."),
        ("Is <i>x</i> = 3 + √2 a solution of <i>x</i><sup>2</sup> − 6<i>x</i> + 7 = 0?", "Yes", ["No", "Only if <i>x</i> is rational", "You cannot check irrational answers"], "<i>x</i> = (6 ± √8) ÷ 2 = 3 ± √2: <b>yes</b>."),
        ("What must be added to both sides to complete the square in <i>x</i><sup>2</sup> − 5<i>x</i> = 3?", fr(25, 4), [fr(5, 2), "25", "−" + fr(25, 4)], "Half of −5 is −5/2, and (−5/2)<sup>2</sup> = <b>25/4</b>."),
        ("A diver's height is <i>h</i> = −5<i>t</i><sup>2</sup> + 10<i>t</i> + 15 meters. When does she reach the water?", "After 3 seconds", ["After 1 second", "After 15 seconds", "After 2 seconds"], "−5(<i>t</i><sup>2</sup> − 2<i>t</i> − 3) = 0 → (<i>t</i> − 3)(<i>t</i> + 1) = 0: <b>3 s</b>."),
        ("Which equation has two irrational solutions?", "<i>x</i><sup>2</sup> − 2<i>x</i> − 4 = 0", ["<i>x</i><sup>2</sup> − 2<i>x</i> − 3 = 0", "<i>x</i><sup>2</sup> − 4 = 0", "<i>x</i><sup>2</sup> + 4 = 0"], "Its discriminant is 4 + 16 = 20, which is positive but not a perfect square: <b><i>x</i><sup>2</sup> − 2<i>x</i> − 4 = 0</b>."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>For <i>ax</i><sup>2</sup> + <i>bx</i> + <i>c</i> = 0, the <b>quadratic formula</b> is "
        "<i>x</i> = (−<i>b</i> ± √(<i>b</i><sup>2</sup> − 4<i>ac</i>)) ÷ 2<i>a</i>. It works for every quadratic.</p>"
        "<p>The <b>discriminant</b> <i>b</i><sup>2</sup> − 4<i>ac</i> tells you how many real solutions there are: positive → two, zero → one, negative → none.</p>"
        "<p>To <b>complete the square</b> for <i>x</i><sup>2</sup> + <i>bx</i>, add (<i>b</i>/2)<sup>2</sup>: <i>x</i><sup>2</sup> + 6<i>x</i> + 9 = (<i>x</i> + 3)<sup>2</sup>. "
        "This also gives vertex form.</p>",
        [("Solve <i>x</i><sup>2</sup> − 4<i>x</i> − 1 = 0.", ["<i>a</i> = 1, <i>b</i> = −4, <i>c</i> = −1. <i>b</i><sup>2</sup> − 4<i>ac</i> = 20.", "<i>x</i> = (4 ± √20) ÷ 2 = (4 ± 2√5) ÷ 2."], "<i>x</i> = 2 ± √5"),
         ("Solve <i>x</i><sup>2</sup> + 8<i>x</i> + 7 = 0 by completing the square.", ["<i>x</i><sup>2</sup> + 8<i>x</i> = −7.", "Add 16: (<i>x</i> + 4)<sup>2</sup> = 9.", "<i>x</i> + 4 = ±3."], "<i>x</i> = −1 or <i>x</i> = −7")],
        ["Using <i>b</i> instead of −<i>b</i> at the start of the formula.",
         "Dividing only the square root by 2<i>a</i>. The whole numerator is divided.",
         "Getting the sign of <i>c</i> wrong in <i>b</i><sup>2</sup> − 4<i>ac</i>.",
         "Adding <i>b</i>/2 instead of (<i>b</i>/2)<sup>2</sup> when completing the square."])


def main():
    sets = [S("The discriminant", collect(one_disc, 20, R)),
            S("Quadratic formula: rational solutions", collect(one_rational, 20, R)),
            S("Quadratic formula: exact radical solutions", collect(one_radical, 20, R)),
            S("Completing the square", collect(one_complete, 20, R)),
            S("Quadratic formula problems", problems())]
    make("quadratic-formula-and-completing-the-square", 17, "A-REI.B.4",
         "The Quadratic Formula and Completing the Square",
         "Algebra 1 Quadratic Formula Worksheets: Discriminant, Exact Answers and Completing the Square (Free, Answer Key)",
         "Quadratic formula and completing the square",
         "Solve quadratic equations in one variable. Use the method of completing the square to transform any quadratic equation in x into an "
         "equation of the form (x − p)² = q that has the same solutions. Derive the quadratic formula from this form.",
         "Free Algebra 1 quadratic formula worksheets (A-REI.B.4): the discriminant, solving with the quadratic formula (rational and exact "
         "radical answers), completing the square, vertex form and word problems. 100 questions with an answer key.",
         "x = (−b ± √(b² − 4ac)) ÷ 2a works for every quadratic.",
         "Discriminant b² − 4ac: positive → two solutions, zero → one, negative → none.",
         body(),
         [("What is the quadratic formula?", "For ax² + bx + c = 0, x = (−b ± √(b² − 4ac)) / (2a)."),
          ("What does the discriminant tell you?", "The value of b² − 4ac. If it is positive there are two real solutions, if it is zero there is one, and if it is negative there are none."),
          ("How do you complete the square?", "For x² + bx, add (b/2)² to make a perfect square: x² + bx + (b/2)² = (x + b/2)². Add the same amount to both sides of an equation."),
          ("When should I use the quadratic formula instead of factoring?", "When the quadratic does not factor easily with integers, or when you need exact or decimal answers.")],
         sets, R, domain="Quadratics")


if __name__ == "__main__":
    main()
