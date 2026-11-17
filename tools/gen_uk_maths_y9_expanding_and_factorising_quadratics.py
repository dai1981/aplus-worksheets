# -*- coding: utf-8 -*-
"""
UK Year 9 Maths: Expanding and Factorising Quadratics (KS3 Algebra)
  python3 tools/gen_uk_maths_y9_expanding_and_factorising_quadratics.py
Expanding (x + a)(x + b), squaring a bracket, the difference of two squares, factorising x² + bx + c with
positive and negative numbers, and solving simple quadratics by factorising.
Wrong answers come from real mistakes: missing the middle terms, sign errors when multiplying negatives,
choosing two numbers that multiply correctly but add wrongly, and writing (x + 3)² = x² + 9.
"""
import random
from uk_ks3 import num, mcq, B, S, make, lesson, collect, T, expr, MINUS

R = random.Random(90401)
X = "<i>x</i>"
X2 = "<i>x</i><sup>2</sup>"


def quad(b, c, v=X, v2=X2):
    return expr([(1, v2), (b, v), (c, "")])


def br(a, v=X):
    return "(%s)" % expr([(1, v), (a, "")])


def nz(r, lo, hi):
    while True:
        k = r.randint(lo, hi)
        if k:
            return k


# ------------------------------------------------------------ set 1: expanding (x + a)(x + b)
def one_expand(r):
    a, b = nz(r, -9, 9), nz(r, -9, 9)
    if a == b or a == -b:
        return None
    q = "Expand and simplify %s." % B(br(a) + br(b))
    right = quad(a + b, a * b)
    wr = [expr([(1, X2), (a * b, "")]), quad(a * b, a + b), quad(a + b, -a * b), quad(a - b, a * b)]
    e = "%s + %s + %s + %s. Collect the middle terms: <b>%s</b>." % (X2, expr([(b, X)]), expr([(a, X)]), num(a * b), right)
    e = e.replace("+ " + MINUS, MINUS + " ")
    return T(q, right, [w for w in wr if w != right][:3], e)


# ------------------------------------------------------------ set 2: squares and difference of two squares
def one_square(r):
    a = nz(r, -9, 9)
    if r.random() < 0.6:
        q = "Expand %s." % B(br(a) + "<sup>2</sup>")
        right = quad(2 * a, a * a)
        wr = [expr([(1, X2), (a * a, "")]), quad(a, a * a), quad(2 * a, 2 * a), quad(-2 * a, a * a)]
        e = "%s<sup>2</sup> = %s%s = %s + %s + %s + %d = <b>%s</b>." % (br(a), br(a), br(a), X2, expr([(a, X)]), expr([(a, X)]), a * a, right)
        e = e.replace("+ " + MINUS, MINUS + " ")
        return T(q, right, [w for w in wr if w != right][:3], e)
    a = abs(a)
    q = "Expand %s." % B("(%s + %d)(%s − %d)" % (X, a, X, a))
    right = expr([(1, X2), (-a * a, "")])
    wr = [quad(0, a * a), quad(2 * a, -a * a), quad(-2 * a, -a * a)]
    e = "%s − %d%s + %d%s − %d. The middle terms cancel: <b>%s</b> (difference of two squares)." % (X2, a, X, a, X, a * a, right)
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 3: factorising, positive c
def one_fact_pos(r):
    p, q_ = r.randint(1, 9), r.randint(1, 9)
    sign = r.choice([1, -1])
    p, q_ = p * sign, q_ * sign
    if p == q_ and r.random() < 0.6:
        return None
    b, c = p + q_, p * q_
    qn = "Factorise %s." % B(quad(b, c))
    right = br(min(p, q_)) + br(max(p, q_))
    pairs = [(d, c // d) for d in range(1, abs(c) + 1) if c % d == 0]
    wrong_pair = None
    for d, e2 in pairs:
        if d + e2 != b and {d, e2} != {abs(p), abs(q_)}:
            wrong_pair = (d * sign, e2 * sign)
            break
    wr = [br(-p) + br(-q_)]
    if wrong_pair:
        wr.append(br(min(wrong_pair)) + br(max(wrong_pair)))
    wr.append(br(b) + br(c) if b != c else br(b) + br(1))
    wr.append(br(min(p, q_)) + br(-max(p, q_)) if p != -q_ else br(p + 1) + br(q_))
    e = "Find two numbers that multiply to %s and add to %s: %s and %s. So <b>%s</b>." % (num(c), num(b), num(p), num(q_), right)
    wr = [w for w in wr if w != right and w != br(max(p, q_)) + br(min(p, q_))]
    return T(qn, right, list(dict.fromkeys(wr))[:3], e)


# ------------------------------------------------------------ set 4: factorising, negative c and difference of two squares
def one_fact_neg(r):
    if r.random() < 0.3:
        a = r.randint(2, 12)
        qn = "Factorise %s." % B(expr([(1, X2), (-a * a, "")]))
        right = "(%s + %d)(%s − %d)" % (X, a, X, a)
        wr = ["(%s − %d)<sup>2</sup>" % (X, a), "(%s + %d)<sup>2</sup>" % (X, a), "(%s − %d)(%s − %d)" % (X, a * a, X, 1)]
        return T(qn, right, wr, "%s − %d = %s<sup>2</sup> − %d<sup>2</sup>, the difference of two squares: <b>%s</b>." % (X2, a * a, X, a, right))
    p, q_ = r.randint(1, 9), -r.randint(1, 9)
    if p == -q_:
        return None
    b, c = p + q_, p * q_
    qn = "Factorise %s." % B(quad(b, c))
    right = br(min(p, q_)) + br(max(p, q_))
    wr = [br(-p) + br(-q_), br(abs(p)) + br(abs(q_)), br(min(-p, -q_)) + br(max(-p, -q_)) if False else br(-abs(p)) + br(-abs(q_))]
    e = "Two numbers that multiply to %s (so one is negative) and add to %s: %s and %s. So <b>%s</b>." % (num(c), num(b), num(p), num(q_), right)
    wr = [w for w in wr if w != right and w != br(max(p, q_)) + br(min(p, q_))]
    if len(set(wr)) < 3:
        wr.append(br(c) + br(1))
    return T(qn, right, list(dict.fromkeys(wr))[:3], e)


# ------------------------------------------------------------ set 5: solving and problems
def problems():
    its = []
    data = [
        ("Solve %s." % B("(%s − 3)(%s + 5) = 0" % (X, X)), "%s = 3 or %s = −5" % (X, X), ["%s = −3 or %s = 5" % (X, X), "%s = 3 or %s = 5" % (X, X), "%s = −15" % X], "One bracket must be zero: %s − 3 = 0 or %s + 5 = 0. <b>%s = 3 or %s = −5</b>." % (X, X, X, X)),
        ("Solve %s." % B(quad(7, 12) + " = 0"), "%s = −3 or %s = −4" % (X, X), ["%s = 3 or %s = 4" % (X, X), "%s = −2 or %s = −6" % (X, X), "%s = 12" % X], "(%s + 3)(%s + 4) = 0, so <b>%s = −3 or %s = −4</b>." % (X, X, X, X)),
        ("Solve %s." % B(quad(-2, -15) + " = 0"), "%s = 5 or %s = −3" % (X, X), ["%s = −5 or %s = 3" % (X, X), "%s = 15 or %s = −1" % (X, X), "%s = 2" % X], "(%s − 5)(%s + 3) = 0, so <b>%s = 5 or %s = −3</b>." % (X, X, X, X)),
        ("Solve %s." % B(expr([(1, X2), (-49, "")]) + " = 0"), "%s = 7 or %s = −7" % (X, X), ["%s = 7 only" % X, "%s = 49" % X, "%s = 24.5" % X], "(%s + 7)(%s − 7) = 0, so <b>%s = ±7</b>." % (X, X, X)),
        ("Solve %s." % B(expr([(1, X2), (-6, X)]) + " = 0"), "%s = 0 or %s = 6" % (X, X), ["%s = 6 only" % X, "%s = −6 or %s = 0" % (X, X), "%s = 3" % X], "%s(%s − 6) = 0, so <b>%s = 0 or %s = 6</b>." % (X, X, X, X)),
        ("A rectangle has sides (%s + 2) cm and (%s + 5) cm. Which expression gives its area?" % (X, X), quad(7, 10), [quad(0, 10), expr([(2, X), (7, "")]), quad(7, 7)], "(%s + 2)(%s + 5) = <b>%s</b>." % (X, X, quad(7, 10))),
        ("A square has side (%s − 4) cm. Which expression gives its area?" % X, quad(-8, 16), [quad(0, -16), quad(0, 16), quad(-4, 16)], "(%s − 4)<sup>2</sup> = <b>%s</b>." % (X, quad(-8, 16))),
        ("Which pair of numbers multiplies to −12 and adds to 4?", "6 and −2", ["−6 and 2", "3 and −4", "12 and −1"], "6 × (−2) = −12 and 6 + (−2) = 4: <b>6 and −2</b>."),
        ("Leo says (%s + 6)<sup>2</sup> = %s + 36. What is the correct expansion?" % (X, X2), quad(12, 36), [quad(6, 36), expr([(1, X2), (36, "")]), quad(12, 12)], "(%s + 6)(%s + 6) = <b>%s</b>. Leo missed the middle terms." % (X, X, quad(12, 36))),
        ("Use the difference of two squares to work out 51<sup>2</sup> − 49<sup>2</sup>.", "200", ["4", "2", "10,000"], "(51 + 49)(51 − 49) = 100 × 2 = <b>200</b>."),
        ("Factorise fully %s." % B(expr([(2, X2), (10, X), (12, "")])), "2(%s + 2)(%s + 3)" % (X, X), ["(2%s + 4)(%s + 3)" % (X, X), "2(%s + 5)(%s + 1)" % (X, X), "(%s + 2)(%s + 3)" % (X, X)],
         "Take out 2: 2(%s). Then factorise: <b>2(%s + 2)(%s + 3)</b>." % (quad(5, 6), X, X)),
        ("Which expression is equivalent to %s?" % B(quad(-1, -20)), "(%s − 5)(%s + 4)" % (X, X), ["(%s + 5)(%s − 4)" % (X, X), "(%s − 10)(%s + 2)" % (X, X), "(%s − 20)(%s + 1)" % (X, X)],
         "−5 × 4 = −20 and −5 + 4 = −1: <b>(%s − 5)(%s + 4)</b>." % (X, X)),
        ("Expand %s." % B("(2%s + 1)(%s + 3)" % (X, X)), expr([(2, X2), (7, X), (3, "")]), [expr([(2, X2), (3, "")]), expr([(2, X2), (4, X), (3, "")]), expr([(3, X2), (7, X), (3, "")])],
         "2%s + 6%s + %s + 3 = <b>%s</b>." % (X2, X, X, expr([(2, X2), (7, X), (3, "")]))),
        ("What is the missing number? (%s + 4)(%s + ☐) = %s + 9%s + 20" % (X, X, X2, X), "5", ["16", "−5", "4"], "4 + ☐ = 9 and 4 × ☐ = 20, so ☐ = <b>5</b>."),
        ("The area of a rectangle is %s cm². One side is (%s + 3) cm. What is the other side?" % (quad(8, 15), X), "(%s + 5) cm" % X, ["(%s + 12) cm" % X, "(%s + 2) cm" % X, "(%s − 5) cm" % X], "%s = (%s + 3)(%s + 5), so the other side is <b>(%s + 5) cm</b>." % (quad(8, 15), X, X, X)),
        ("For which value of <i>k</i> can %s + 6%s + <i>k</i> be written as a perfect square (%s + <i>a</i>)<sup>2</sup>?" % (X2, X, X), "9", ["36", "6", "3"], "(%s + 3)<sup>2</sup> = %s + 6%s + 9, so <i>k</i> = <b>9</b>." % (X, X2, X)),
        ("Solve %s." % B(quad(-8, 16) + " = 0"), "%s = 4" % X, ["%s = 4 or %s = −4" % (X, X), "%s = −4" % X, "%s = 16" % X], "(%s − 4)<sup>2</sup> = 0, so <b>%s = 4</b> (a repeated root)." % (X, X)),
        ("Which of these cannot be factorised into two brackets with whole numbers?", quad(3, 5), [quad(5, 6), quad(-1, -6), expr([(1, X2), (-25, "")])], "No two whole numbers multiply to 5 and add to 3, so <b>%s</b> cannot." % quad(3, 5)),
        ("A rectangle has length %s + 3 and width %s − 3. Its area is 40. Find %s." % (X, X, X), "7", ["−7", "6.3", "43"], "(%s + 3)(%s − 3) = %s − 9 = 40, so %s = 49 and %s = 7 (a length must be positive). <b>7</b>." % (X, X, X2, X2, X)),
        ("What are the solutions of %s(%s + 8) = 0?" % (X, X), "%s = 0 or %s = −8" % (X, X), ["%s = 8" % X, "%s = −8 only" % X, "%s = 0 or %s = 8" % (X, X)], "Either %s = 0 or %s + 8 = 0. <b>%s = 0 or %s = −8</b>." % (X, X, X, X)),
    ]
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p>To <b>expand</b> two brackets, multiply each term in the first by each term in the second, then collect the "
        "middle terms: (<i>x</i> + <i>a</i>)(<i>x</i> + <i>b</i>) = <i>x</i>² + (<i>a</i> + <i>b</i>)<i>x</i> + <i>ab</i>.</p>"
        "<p>To <b>factorise</b> <i>x</i>² + <i>bx</i> + <i>c</i>, find two numbers that <b>multiply to <i>c</i></b> and <b>add to <i>b</i></b>. "
        "The <b>difference of two squares</b>: <i>x</i>² − <i>a</i>² = (<i>x</i> + <i>a</i>)(<i>x</i> − <i>a</i>).</p>",
        [("Expand (<i>x</i> + 3)(<i>x</i> − 7).", ["<i>x</i>² − 7<i>x</i> + 3<i>x</i> − 21."], "<i>x</i>² − 4<i>x</i> − 21"),
         ("Factorise <i>x</i>² + 2<i>x</i> − 15.", ["Multiply to −15, add to 2: 5 and −3."], "(<i>x</i> + 5)(<i>x</i> − 3)"),
         ("Solve <i>x</i>² − 5<i>x</i> + 6 = 0.", ["(<i>x</i> − 2)(<i>x</i> − 3) = 0."], "<i>x</i> = 2 or <i>x</i> = 3")],
        ["Missing the middle terms: (<i>x</i> + 3)² is <i>x</i>² + 6<i>x</i> + 9, not <i>x</i>² + 9.",
         "Sign errors: (−3) × (−7) = +21, but (−3) × 7 = −21.",
         "Finding numbers that multiply to <i>c</i> but do not add to <i>b</i>.",
         "Giving only the positive solution of <i>x</i>² = 49. There are two: 7 and −7."])


def main():
    sets = [S("Expanding double brackets", collect(one_expand, 20, R)),
            S("Squares and the difference of two squares", collect(one_square, 20, R)),
            S("Factorising with a positive constant", collect(one_fact_pos, 20, R)),
            S("Factorising with a negative constant", collect(one_fact_neg, 20, R)),
            S("Solving and problems", problems())]
    make(9, "expanding-and-factorising-quadratics", 4, "A",
         "Expanding and Factorising Quadratics",
         "Year 9 Quadratics Worksheets: Expanding Double Brackets, Factorising x² + bx + c and Difference of Two Squares",
         "Quadratics",
         "Simplify and manipulate algebraic expressions to maintain equivalence by: expanding products of two or more "
         "binomials; factorising quadratic expressions of the form x² + bx + c, including the difference of two squares.",
         "Free Year 9 quadratics worksheets: expand double brackets and squares, the difference of two squares, factorise "
         "x² + bx + c with positive and negative numbers, and solve by factorising. 100 questions with answers.",
         "To factorise x² + bx + c, find two numbers that multiply to c and add to b.",
         "(x + a)² = x² + 2ax + a², and x² − a² = (x + a)(x − a).",
         body(),
         [("How do I factorise a quadratic?", "For x² + bx + c, find two numbers that multiply to c and add to b. If they are p and q, the answer is (x + p)(x + q)."),
          ("What is the difference of two squares?", "x² − a² = (x + a)(x − a). For example x² − 49 = (x + 7)(x − 7)."),
          ("Why is (x + 3)² not x² + 9?", "Because (x + 3)² = (x + 3)(x + 3), which has two middle terms of 3x. So it is x² + 6x + 9."),
          ("How do I solve a quadratic by factorising?", "Factorise so the equation is (x − p)(x − q) = 0. One of the brackets must be zero, so x = p or x = q.")],
         sets, R)


if __name__ == "__main__":
    main()
