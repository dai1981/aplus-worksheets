# -*- coding: utf-8 -*-
"""
US Algebra 1: Exponent Rules and Rational Exponents (Common Core N-RN.A.1, N-RN.A.2)
  python3 tools/gen_us_math_a1_rational_exponents.py
Exponent rules with variables and coefficients (product, quotient, power, zero and negative exponents),
writing radicals as rational exponents and back, evaluating numbers with rational exponents, simplifying
expressions with rational exponents, and reasoning about common errors.
Wrong answers come from real mistakes: multiplying exponents instead of adding, not raising the coefficient
to the power, reading a negative exponent as a negative number, and swapping the root and the power in
x^(m/n).
"""
import random
from fractions import Fraction as F
from us_hs import num, B, S, make, lesson, collect, T, QN, fr, MINUS

R = random.Random(91001)


def pw(base, e):
    """base^e as HTML; e may be a Fraction."""
    e = F(e)
    if e == 1:
        return base
    es = num(e) if e.denominator == 1 else ("%s%d/%d" % (MINUS if e < 0 else "", abs(e.numerator), e.denominator))
    return "%s<sup>%s</sup>" % (base, es)


def mono(c, exps):
    """c·x^a·y^b with positive exponents only (negative ones go to the denominator)."""
    c = F(c)
    num_ = "".join(pw("<i>%s</i>" % v, e) for v, e in exps if e > 0)
    den = "".join(pw("<i>%s</i>" % v, -e) for v, e in exps if e < 0)
    top = (num(c.numerator) if (c.numerator not in (1, -1) or not num_) else ("" if c.numerator == 1 else MINUS)) + num_
    if c.numerator == -1 and not num_:
        top = MINUS + "1"
    bottom = (num(c.denominator) if c.denominator != 1 else "") + den
    if not bottom:
        return top
    if top.startswith(MINUS):
        return MINUS + fr(top[1:] or "1", bottom)
    return fr(top or "1", bottom)


# ------------------------------------------------------------ set 1: exponent rules with variables
def one_rules(r):
    kind = r.choice(["prod", "quot", "pow", "mix"])
    a, b = r.randint(1, 6), r.randint(1, 5)
    if kind == "prod":
        c1, c2 = r.randint(2, 6), r.randint(2, 5)
        p1, p2, q1, q2 = r.randint(1, 5), r.randint(1, 5), r.randint(1, 4), r.randint(0, 4)
        q = "Simplify %s." % B("(%s)(%s)" % (mono(c1, [("x", p1), ("y", q1)]), mono(c2, [("x", p2), ("y", q2)])))
        right = mono(c1 * c2, [("x", p1 + p2), ("y", q1 + q2)])
        wr = [mono(c1 * c2, [("x", p1 * p2), ("y", q1 * q2 if q2 else q1)]), mono(c1 + c2, [("x", p1 + p2), ("y", q1 + q2)]), mono(c1 * c2, [("x", p1 + p2 + 1), ("y", q1 + q2)])]
        e = "Multiply the numbers (%d × %d = %d) and <b>add</b> the exponents of each variable: <b>%s</b>." % (c1, c2, c1 * c2, right)
    elif kind == "quot":
        c2 = r.randint(2, 5)
        c1 = c2 * r.randint(2, 6)
        p1, p2, q1, q2 = r.randint(4, 9), r.randint(1, 3), r.randint(1, 3), r.randint(2, 6)
        q = "Simplify %s." % B(fr(mono(c1, [("x", p1), ("y", q1)]), mono(c2, [("x", p2), ("y", q2)])))
        right = mono(F(c1, c2), [("x", p1 - p2), ("y", q1 - q2)])
        wr = [mono(F(c1, c2), [("x", p1 - p2), ("y", q2 - q1)]), mono(c1 - c2, [("x", p1 - p2), ("y", q1 - q2)]), mono(F(c1, c2), [("x", F(p1, p2)) if p1 % p2 == 0 else ("x", p1 + p2), ("y", q1 - q2)])]
        e = "Divide the numbers and <b>subtract</b> the exponents: <i>x</i><sup>%d−%d</sup> and <i>y</i><sup>%d−%d</sup>. A negative exponent moves to the denominator: <b>%s</b>." % (p1, p2, q1, q2, right)
    elif kind == "pow":
        c = r.choice([2, 3, -2, 5])
        n = r.choice([2, 3])
        p1, q1 = r.randint(1, 4), r.randint(1, 4)
        q = "Simplify %s." % B("(%s)<sup>%d</sup>" % (mono(c, [("x", p1), ("y", q1)]), n))
        right = mono(c ** n, [("x", p1 * n), ("y", q1 * n)])
        wr = [mono(c, [("x", p1 * n), ("y", q1 * n)]), mono(c * n, [("x", p1 * n), ("y", q1 * n)]), mono(c ** n, [("x", p1 + n), ("y", q1 + n)])]
        e = "Raise every factor to the power %d: %s<sup>%d</sup> = %s, and <b>multiply</b> the exponents: <b>%s</b>." % (n, "(%s)" % num(c) if c < 0 else num(c), n, num(c ** n), right)
    else:
        p1, p2 = r.randint(2, 6), r.randint(1, 5)
        k = r.choice([-1, -2, -3])
        q = "Simplify %s and write with positive exponents." % B("%s · %s" % (pw("<i>x</i>", p1), pw("<i>x</i>", k - p1)))
        right = mono(1, [("x", k)])
        wr = [mono(1, [("x", -k)]), mono(-1, [("x", -k)]) if k != -1 else MINUS + "<i>x</i>", mono(1, [("x", p1 * (k - p1))])]
        e = "Add the exponents: %d + (%d) = %d. Then <i>x</i><sup>%d</sup> = <b>%s</b>." % (p1, k - p1, k, k, right)
    wr = [w for w in dict.fromkeys(wr) if w != right]
    if len(wr) < 3:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 2: radicals and rational exponents
def root(n, inside):
    return ("√" if n == 2 else "<sup>%d</sup>√" % n) + inside


def one_convert(r):
    n = r.choice([2, 3, 4, 5])
    m = r.choice([1, 2, 3, 4, 5])
    if F(m, n).denominator != n:
        return None
    v = r.choice(["x", "a", "y"])
    if r.random() < 0.5:
        rad = root(n, pw("<i>%s</i>" % v, m) if m > 1 else "<i>%s</i>" % v)
        q = "Write %s using a rational exponent." % B(rad)
        right = pw("<i>%s</i>" % v, F(m, n))
        wr = [pw("<i>%s</i>" % v, F(n, m)) if m > 1 else pw("<i>%s</i>" % v, n), pw("<i>%s</i>" % v, m * n), pw("<i>%s</i>" % v, F(1, n)) if m > 1 else pw("<i>%s</i>" % v, F(1, n + 1))]
        e = "The power goes on top and the root on the bottom: <b>%s</b>." % right
    else:
        q = "Write %s as a radical." % B(pw("<i>%s</i>" % v, F(m, n)))
        right = root(n, pw("<i>%s</i>" % v, m) if m > 1 else "<i>%s</i>" % v)
        wr = [root(m, pw("<i>%s</i>" % v, n)) if m > 1 else pw("<i>%s</i>" % v, n), fr(pw("<i>%s</i>" % v, m), num(n)), root(n, "<i>%s</i>" % v) + ("<sup>%d</sup>" % m if False else "") if m > 1 else root(2 * n, "<i>%s</i>" % v)]
        e = "<i>x</i><sup><i>m</i>/<i>n</i></sup> is the <i>n</i>th root of <i>x</i><sup><i>m</i></sup>: <b>%s</b>." % right
    wr = [w for w in dict.fromkeys(wr) if w != right]
    if len(wr) < 3:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 3: evaluate
BASES = [(4, 2), (9, 2), (16, 2), (25, 2), (36, 2), (49, 2), (64, 2), (100, 2), (8, 3), (27, 3), (64, 3), (125, 3), (16, 4), (81, 4), (32, 5), (1000, 3)]


def one_eval(r):
    base, n = r.choice(BASES)
    rt = round(base ** (1.0 / n))
    m = r.choice([1, 2, 3, -1, -2])
    if abs(m) >= 3 and rt > 5:
        return None
    if F(m, n).denominator != n:
        return None
    val = F(rt) ** m
    q = "Evaluate %s." % B(pw(num(base), F(m, n)))
    def show(v):
        v = F(v)
        return num(v) if v.denominator == 1 else fr(v.numerator, v.denominator)
    right = show(val)
    wr = [show(F(base * m, n)) if F(base * m, n).denominator == 1 else show(F(base, n)), show(-abs(val)) if val > 0 else show(abs(val)), show(F(rt) ** (-m)), show(F(base) ** abs(m) if base ** abs(m) < 10 ** 6 else rt * abs(m))]
    wr = [w for w in dict.fromkeys(wr) if w != right]
    e = ("Take the root first: %s = %d. Then raise to the power %s: <b>%s</b>." % (root(n, num(base)), rt, num(m), right)) if m != 1 else (
        "The exponent 1/%d means the %s root: %s = <b>%s</b>." % (n, {2: "square", 3: "cube", 4: "fourth", 5: "fifth"}[n], root(n, num(base)), right))
    if m < 0:
        e += " A negative exponent means the reciprocal, not a negative number."
    if len(wr) < 3:
        return None
    return T(q, right, wr[:3], e)


# ------------------------------------------------------------ set 4: simplify with rational exponents
def one_simp(r):
    kind = r.choice(["prod", "pow", "quot", "root"])
    n = r.choice([2, 3, 4])
    if kind == "prod":
        a, b = F(r.randint(1, 5), n), F(r.randint(1, 5), n)
        q = "Simplify %s." % B("%s · %s" % (pw("<i>x</i>", a), pw("<i>x</i>", b)))
        right = pw("<i>x</i>", a + b)
        wr = [pw("<i>x</i>", a * b), pw("<i>x</i>", F(a.numerator + b.numerator, 2 * n)), pw("<i>x</i>", a + b + 1)]
        e = "Add the exponents: %s + %s = %s. So <b>%s</b>." % (fr(a.numerator, a.denominator) if a.denominator > 1 else num(a), fr(b.numerator, b.denominator) if b.denominator > 1 else num(b), fr((a + b).numerator, (a + b).denominator) if (a + b).denominator > 1 else num(a + b), right)
    elif kind == "pow":
        a = F(r.randint(1, 5), n)
        k = r.choice([2, 3, 4, 6])
        q = "Simplify %s." % B("(%s)<sup>%d</sup>" % (pw("<i>x</i>", a), k))
        right = pw("<i>x</i>", a * k)
        wr = [pw("<i>x</i>", a + k), pw("<i>x</i>", F(a.numerator, a.denominator * k)), pw("<i>x</i>", a * k + 1)]
        e = "Multiply the exponents: %s × %d. So <b>%s</b>." % (fr(a.numerator, a.denominator) if a.denominator > 1 else num(a), k, right)
    elif kind == "quot":
        a, b = F(r.randint(3, 9), n), F(r.randint(1, 3), n)
        if a <= b:
            return None
        q = "Simplify %s." % B(fr(pw("<i>x</i>", a), pw("<i>x</i>", b)))
        right = pw("<i>x</i>", a - b)
        wr = [pw("<i>x</i>", a / b), pw("<i>x</i>", a + b), pw("<i>x</i>", b - a)]
        e = "Subtract the exponents. So <b>%s</b>." % right
    else:
        k = r.choice([2, 3])
        m = r.choice([1, 3, 5])
        q = "Write %s as a power of <i>x</i>." % B("√<i>x</i> · " + root(k, pw("<i>x</i>", m) if m > 1 else "<i>x</i>"))
        tot = F(1, 2) + F(m, k)
        right = pw("<i>x</i>", tot)
        wr = [pw("<i>x</i>", F(1, 2) * F(m, k)), pw("<i>x</i>", F(1 + m, 2 + k)), pw("<i>x</i>", F(1, 2) + F(k, m))]
        e = "√<i>x</i> = <i>x</i><sup>1/2</sup> and the second factor is <i>x</i><sup>%d/%d</sup>. Add the exponents: <b>%s</b>." % (m, k, right)
    wr = [w for w in dict.fromkeys(wr) if w != right]
    if len(wr) < 3:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 5: reasoning
def problems():
    data = [
        ("Why does 9<sup>1/2</sup> equal 3?", "Because (9<sup>1/2</sup>)<sup>2</sup> = 9<sup>1</sup> = 9, so 9<sup>1/2</sup> is the square root", ["Because half of 9 is about 3", "Because 9 ÷ 3 = 3", "Because 9 − 6 = 3"],
         "Using the power rule, (9<sup>1/2</sup>)<sup>2</sup> = 9, so 9<sup>1/2</sup> is a number whose square is 9: <b>√9 = 3</b>."),
        ("Which is equal to 2<sup>−3</sup>?", fr(1, 8), ["−8", "−6", fr(1, 6)], "A negative exponent means the reciprocal: 1 ÷ 2<sup>3</sup> = <b>⅛</b>."),
        ("Which is equal to 5<sup>0</sup>?", "1", ["0", "5", "−5"], "Any nonzero number to the power 0 is <b>1</b>."),
        ("Which is equal to (−2)<sup>4</sup>?", "16", ["−16", "−8", "8"], "(−2)(−2)(−2)(−2) = <b>16</b>."),
        ("Which is equal to −2<sup>4</sup>?", "−16", ["16", "−8", "8"], "Only the 2 is raised to the power: −(2<sup>4</sup>) = <b>−16</b>."),
        ("Noah says 3<i>x</i><sup>0</sup> = 1. What is the correct value (with <i>x</i> ≠ 0)?", "3", ["1", "0", "3<i>x</i>"], "Only <i>x</i> has the exponent 0: 3 × 1 = <b>3</b>."),
        ("Simplify (2<i>x</i><sup>3</sup>)<sup>2</sup> · 3<i>x</i>.", "12<i>x</i><sup>7</sup>", ["6<i>x</i><sup>6</sup>", "12<i>x</i><sup>6</sup>", "36<i>x</i><sup>7</sup>"], "(2<i>x</i><sup>3</sup>)<sup>2</sup> = 4<i>x</i><sup>6</sup>, then × 3<i>x</i> = <b>12<i>x</i><sup>7</sup></b>."),
        ("Which is larger: 8<sup>2/3</sup> or 4<sup>3/2</sup>?", "4<sup>3/2</sup>", ["8<sup>2/3</sup>", "They are equal", "You cannot tell"], "8<sup>2/3</sup> = 2<sup>2</sup> = 4 and 4<sup>3/2</sup> = 2<sup>3</sup> = 8: <b>4<sup>3/2</sup></b>."),
        ("Solve 2<sup><i>x</i></sup> = 32.", "<i>x</i> = 5", ["<i>x</i> = 16", "<i>x</i> = 6", "<i>x</i> = 4"], "2<sup>5</sup> = 32, so <b><i>x</i> = 5</b>."),
        ("Solve 9<sup><i>x</i></sup> = 3.", "<i>x</i> = " + fr(1, 2), ["<i>x</i> = 3", "<i>x</i> = 2", "<i>x</i> = " + fr(1, 3)], "9<sup>1/2</sup> = 3, so <b><i>x</i> = ½</b>."),
        ("Write 1/<i>x</i><sup>4</sup> with a negative exponent.", "<i>x</i><sup>−4</sup>", ["−<i>x</i><sup>4</sup>", "<i>x</i><sup>1/4</sup>", "4<sup>−<i>x</i></sup>"], "1/<i>x</i><sup>4</sup> = <b><i>x</i><sup>−4</sup></b>."),
        ("The area of a square is 49<i>x</i><sup>6</sup> cm². What is its side length?", "7<i>x</i><sup>3</sup> cm", ["7<i>x</i><sup>6</sup> cm", "24.5<i>x</i><sup>3</sup> cm", "49<i>x</i><sup>3</sup> cm"], "√(49<i>x</i><sup>6</sup>) = (49<i>x</i><sup>6</sup>)<sup>1/2</sup> = <b>7<i>x</i><sup>3</sup></b>."),
        ("A cube has volume 8<i>a</i><sup>9</sup>. What is its edge length?", "2<i>a</i><sup>3</sup>", ["2<i>a</i><sup>6</sup>", "8<i>a</i><sup>3</sup>", "4<i>a</i><sup>3</sup>"], "(8<i>a</i><sup>9</sup>)<sup>1/3</sup> = <b>2<i>a</i><sup>3</sup></b>."),
        ("Simplify 16<sup>−1/2</sup>.", fr(1, 4), ["−4", "−8", "8"], "16<sup>1/2</sup> = 4, and the negative exponent gives the reciprocal: <b>¼</b>."),
        ("Which expression is NOT equal to <i>x</i><sup>6</sup>?", "<i>x</i><sup>2</sup> · <i>x</i><sup>3</sup>", ["(<i>x</i><sup>2</sup>)<sup>3</sup>", "<i>x</i><sup>8</sup> ÷ <i>x</i><sup>2</sup>", "<i>x</i><sup>4</sup> · <i>x</i><sup>2</sup>"], "<i>x</i><sup>2</sup> · <i>x</i><sup>3</sup> = <b><i>x</i><sup>5</sup></b>, not <i>x</i><sup>6</sup>."),
        ("Simplify (<i>x</i><sup>4</sup><i>y</i><sup>−2</sup>)<sup>−1</sup>.", fr("<i>y</i><sup>2</sup>", "<i>x</i><sup>4</sup>"), [fr("<i>x</i><sup>4</sup>", "<i>y</i><sup>2</sup>"), "−<i>x</i><sup>4</sup><i>y</i><sup>2</sup>", "<i>x</i><sup>3</sup><i>y</i><sup>−3</sup>"],
         "Multiply each exponent by −1: <i>x</i><sup>−4</sup><i>y</i><sup>2</sup> = <b><i>y</i><sup>2</sup>/<i>x</i><sup>4</sup></b>."),
        ("What is 27<sup>2/3</sup>?", "9", ["18", "6", "81"], "<sup>3</sup>√27 = 3, then 3<sup>2</sup> = <b>9</b>."),
        ("Bacteria double every hour. Which expression gives the number after <i>t</i> hours, starting with 100?", "100 · 2<sup><i>t</i></sup>", ["100 · <i>t</i><sup>2</sup>", "100 + 2<i>t</i>", "200<sup><i>t</i></sup>"], "Doubling each hour multiplies by 2 again and again: <b>100 · 2<sup><i>t</i></sup></b>."),
        ("Using 100 · 2<sup><i>t</i></sup>, how many bacteria are there after 1.5 hours (to the nearest whole number)?", "283", ["300", "250", "400"], "2<sup>1.5</sup> = 2√2 ≈ 2.828, and 100 × 2.828 ≈ <b>283</b>."),
        ("Which is equal to (<i>a</i><sup>1/3</sup>)<sup>6</sup>?", "<i>a</i><sup>2</sup>", ["<i>a</i><sup>18</sup>", "<i>a</i><sup>1/18</sup>", "<i>a</i><sup>6⅓</sup>"], "Multiply the exponents: ⅓ × 6 = 2, so <b><i>a</i><sup>2</sup></b>."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<ul><li>Product: <i>x</i><sup><i>a</i></sup> · <i>x</i><sup><i>b</i></sup> = <i>x</i><sup><i>a</i>+<i>b</i></sup></li>"
        "<li>Quotient: <i>x</i><sup><i>a</i></sup> ÷ <i>x</i><sup><i>b</i></sup> = <i>x</i><sup><i>a</i>−<i>b</i></sup></li>"
        "<li>Power: (<i>x</i><sup><i>a</i></sup>)<sup><i>b</i></sup> = <i>x</i><sup><i>ab</i></sup>, and (<i>xy</i>)<sup><i>n</i></sup> = <i>x</i><sup><i>n</i></sup><i>y</i><sup><i>n</i></sup></li>"
        "<li>Zero and negative: <i>x</i><sup>0</sup> = 1 and <i>x</i><sup>−<i>n</i></sup> = 1/<i>x</i><sup><i>n</i></sup></li></ul>"
        "<p>A <b>rational exponent</b> is a root: <i>x</i><sup>1/<i>n</i></sup> = <sup><i>n</i></sup>√<i>x</i> and "
        "<i>x</i><sup><i>m</i>/<i>n</i></sup> = (<sup><i>n</i></sup>√<i>x</i>)<sup><i>m</i></sup>. The bottom number is the root and the top number is the power. "
        "All the same rules apply.</p>",
        [("Simplify (3<i>x</i><sup>2</sup><i>y</i>)<sup>3</sup>.", ["Cube every factor: 27<i>x</i><sup>6</sup><i>y</i><sup>3</sup>."], "27<i>x</i><sup>6</sup><i>y</i><sup>3</sup>"),
         ("Evaluate 8<sup>2/3</sup>.", ["Cube root of 8 is 2.", "2<sup>2</sup> = 4."], "4"),
         ("Simplify <i>x</i><sup>1/2</sup> · <i>x</i><sup>3/2</sup>.", ["½ + 3/2 = 2."], "<i>x</i><sup>2</sup>")],
        ["Multiplying exponents when you multiply powers: <i>x</i><sup>2</sup> · <i>x</i><sup>3</sup> = <i>x</i><sup>5</sup>, not <i>x</i><sup>6</sup>.",
         "Forgetting the coefficient: (2<i>x</i>)<sup>3</sup> = 8<i>x</i><sup>3</sup>, not 2<i>x</i><sup>3</sup>.",
         "Reading a negative exponent as a negative number: 2<sup>−3</sup> = ⅛, not −8.",
         "Swapping root and power: 8<sup>2/3</sup> is the cube root of 8 squared, not the square root of 8 cubed."])


def main():
    sets = [S("Exponent rules with variables", collect(one_rules, 20, R)),
            S("Radicals and rational exponents", collect(one_convert, 20, R)),
            S("Evaluate rational exponents", collect(one_eval, 20, R)),
            S("Simplify with rational exponents", collect(one_simp, 20, R)),
            S("Reasoning with exponents", problems())]
    make("rational-exponents", 10, "N-RN.A.2",
         "Exponent Rules and Rational Exponents",
         "Algebra 1 Rational Exponents Worksheets: Exponent Rules, Radicals and Negative Exponents (Free, Answer Key)",
         "Rational exponents",
         "Rewrite expressions involving radicals and rational exponents using the properties of exponents.",
         "Free Algebra 1 rational exponents worksheets (N-RN.A.1, N-RN.A.2): exponent rules with variables, zero and negative exponents, "
         "writing radicals as rational exponents, evaluating numbers like 8^(2/3) and simplifying. 100 questions with an answer key.",
         "x^(m/n) is the nth root of x, raised to the power m.",
         "Multiply powers: add exponents. Power of a power: multiply exponents. Negative exponent: reciprocal.",
         body(),
         [("What is a rational exponent?", "An exponent that is a fraction. x^(1/n) is the nth root of x, and x^(m/n) is the nth root of x raised to the power m."),
          ("How do you evaluate 16^(3/4)?", "Take the 4th root first (2), then raise it to the 3rd power: 2³ = 8."),
          ("What does a negative exponent mean?", "The reciprocal: x^(−n) = 1/xⁿ. It does not make the number negative."),
          ("Do exponent rules work with fractional exponents?", "Yes. Add exponents when multiplying, subtract when dividing and multiply for a power of a power, just like with whole numbers.")],
         sets, R, domain="Exponents & Exponential Functions")


if __name__ == "__main__":
    main()
