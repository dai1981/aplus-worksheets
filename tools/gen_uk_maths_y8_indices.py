# -*- coding: utf-8 -*-
"""
UK Year 8 Maths: Laws of Indices (KS3 Number / Algebra)
  python3 tools/gen_uk_maths_y8_indices.py
Multiplying and dividing powers with the same base, raising a power to a power, the zero index,
negative indices, and simplifying algebraic terms such as 3x² × 4x⁵.
Wrong answers come from real mistakes: multiplying the indices when multiplying powers, multiplying the
bases, thinking a⁰ = 0, reading a negative index as a negative number, and forgetting to square the
number in (2a³)².
"""
import random
from fractions import Fraction as F
from uk_ks3 import num, mcq, B, S, make, lesson, collect, QN, T, fr, MINUS

R = random.Random(80101)
LET = ["<i>a</i>", "<i>x</i>", "<i>y</i>", "<i>m</i>", "<i>n</i>", "<i>p</i>", "<i>t</i>"]


def pw(b, e):
    bs = str(b) if not isinstance(b, int) or b >= 0 else "(%s%d)" % (MINUS, -b)
    if e == 1:
        return bs
    return "%s<sup>%s</sup>" % (bs, num(e))


def term(c, b, e):
    """coefficient × base^e, e.g. 12x⁵"""
    if e == 0:
        return num(c)
    return ("" if c == 1 else num(c)) + pw(b, e)


def base(r):
    return r.choice([2, 3, 5, 7, 10] + LET + LET)


# ------------------------------------------------------------ set 1: multiplying
def one_mul(r):
    b = base(r)
    m, n = r.randint(2, 9), r.randint(1, 8)
    q = "Simplify %s, giving your answer as a single power." % B("%s × %s" % (pw(b, m), pw(b, n)))
    e = "Same base, so add the indices: %d + %d = %d. The answer is <b>%s</b>." % (m, n, m + n, pw(b, m + n))
    wr = [pw(b, m * n), pw(b, m - n) if m != n else pw(b, 0), pw(b * b, m + n) if isinstance(b, int) else "2" + pw(b, m + n), pw(b, m + n + 1)]
    return T(q, pw(b, m + n), [w for w in wr if w != pw(b, m + n)][:3], e)


# ------------------------------------------------------------ set 2: dividing
def one_div(r):
    b = base(r)
    n = r.randint(1, 6)
    m = n + r.randint(1, 8)
    if m % n == 0 and m // n == m - n:
        return None
    q = "Simplify %s, giving your answer as a single power." % B("%s ÷ %s" % (pw(b, m), pw(b, n)))
    e = "Same base, so subtract the indices: %d − %d = %d. The answer is <b>%s</b>." % (m, n, m - n, pw(b, m - n))
    wr = [pw(b, m + n), pw(b, F(m, n)) if m % n == 0 else pw(b, n - m), pw(1, m - n) if isinstance(b, int) else pw(b, m * n), pw(b, m - n + 1)]
    return T(q, pw(b, m - n), [w for w in wr if w != pw(b, m - n)][:3], e)


# ------------------------------------------------------------ set 3: power of a power, zero index
def one_pp(r):
    b = base(r)
    kind = r.random()
    if kind < 0.65:
        m, n = r.randint(2, 6), r.randint(2, 5)
        q = "Simplify %s." % B("(%s)<sup>%d</sup>" % (pw(b, m), n))
        e = "A power of a power: multiply the indices, %d × %d = %d. The answer is <b>%s</b>." % (m, n, m * n, pw(b, m * n))
        return T(q, pw(b, m * n), [pw(b, m + n), pw(b, m ** n) if m ** n < 100 else pw(b, m * n + 1), pw(b, m * n - 1)], e)
    if kind < 0.85:
        b2 = r.choice([5, 9, 12, 100, 3] + LET)
        q = "What is the value of %s?" % B(pw(b2, 0))
        return T(q, "1", ["0", str(b2) if isinstance(b2, int) else b2, "Undefined"], "Any number (except 0) to the power 0 is <b>1</b>.")
    m = r.randint(2, 7)
    q = "Simplify %s." % B("%s ÷ %s" % (pw(b, m), pw(b, m)))
    e = "%d − %d = 0, so the answer is %s = <b>1</b>." % (m, m, pw(b, 0))
    return T(q, "1", ["0", pw(b, 2 * m) if True else "", pw(b, 1)], e)


# ------------------------------------------------------------ set 4: negative indices and evaluating
def one_neg(r):
    b = r.choice([2, 3, 4, 5, 10])
    n = r.randint(1, 4 if b < 5 else 3)
    if b == 10 and n > 3:
        return None
    kind = r.random()
    if kind < 0.6:
        v = F(1, b ** n)
        q = "Work out %s." % B(pw(b, -n))
        e = "A negative index means “1 over”: %s = 1 ÷ %s = <b>%s</b>." % (pw(b, -n), pw(b, n), fr(1, b ** n))
        return T(q, fr(1, b ** n), ["%s%s" % (MINUS, num(b ** n)), "%s%d" % (MINUS, b * n), fr(1, b * n) if b * n != b ** n else fr(1, b ** n + 1)], e)
    m = r.randint(1, 5)
    k = r.randint(m + 1, m + 5)
    q = "Simplify %s, giving your answer as a single power." % B("%s ÷ %s" % (pw(b, m), pw(b, k)))
    e = "Subtract the indices: %d − %d = %s. The answer is <b>%s</b>." % (m, k, num(m - k), pw(b, m - k))
    return T(q, pw(b, m - k), [pw(b, k - m), pw(b, m + k), pw(b, F(m, k)) if False else pw(b, -(m + k))], e)


def one_eval(r):
    a, m, n = r.choice([(2, 3, 2), (3, 2, 2), (2, 5, 3), (10, 4, 2), (5, 3, 1), (2, 7, 4), (3, 5, 3), (4, 3, 1), (10, 6, 3), (2, 4, 4)])
    kind = r.choice(["div", "mul"])
    if kind == "div":
        v = a ** (m - n)
        q = "Work out %s without a calculator." % B("%s ÷ %s" % (pw(a, m), pw(a, n)))
        e = "%s ÷ %s = %s = <b>%s</b>." % (pw(a, m), pw(a, n), pw(a, m - n), num(v))
        return QN(q, v, [a ** (m + n) if a ** (m + n) < 10 ** 7 else None, m - n, a * (m - n)], e)
    v = a ** (m + n - 2) if False else a ** m * a ** (-n) if False else a ** (m + 1)
    q = "Work out %s without a calculator." % B("%s × %s" % (pw(a, m), pw(a, 1)))
    e = "%s × %s = %s = <b>%s</b>." % (pw(a, m), pw(a, 1), pw(a, m + 1), num(v))
    return QN(q, v, [a ** m, (a * a) ** m if (a * a) ** m < 10 ** 7 else None, a * (m + 1), a ** (m + 2)], e)


# ------------------------------------------------------------ set 5: algebra with coefficients and problems
def one_alg(r):
    x = r.choice(LET)
    kind = r.randint(0, 3)
    if kind == 0:
        a, b = r.randint(2, 7), r.randint(2, 6)
        m, n = r.randint(1, 6), r.randint(1, 6)
        q = "Simplify %s." % B("%s × %s" % (term(a, x, m), term(b, x, n)))
        right = term(a * b, x, m + n)
        return T(q, right, [term(a + b, x, m + n), term(a * b, x, m * n), term(a * b, x, m + n + 1) if m * n == m + n else term(a * b, x, m * n + 1)],
                 "Multiply the numbers (%d × %d = %d) and add the indices (%d + %d = %d): <b>%s</b>." % (a, b, a * b, m, n, m + n, right))
    if kind == 1:
        b, a = r.randint(2, 6), r.randint(2, 6)
        n = r.randint(1, 5)
        m = n + r.randint(1, 6)
        q = "Simplify %s." % B("%s ÷ %s" % (term(a * b, x, m), term(b, x, n)))
        right = term(a, x, m - n)
        return T(q, right, [term(a * b - b, x, m - n), term(a, x, F(m, n)) if m % n == 0 and m // n != m - n else term(a, x, m + n), term(a * b, x, m - n)],
                 "Divide the numbers (%d ÷ %d = %d) and subtract the indices (%d − %d = %d): <b>%s</b>." % (a * b, b, a, m, n, m - n, right))
    if kind == 2:
        a, m, n = r.randint(2, 5), r.randint(2, 5), r.choice([2, 3])
        q = "Simplify %s." % B("(%s)<sup>%d</sup>" % (term(a, x, m), n))
        right = term(a ** n, x, m * n)
        return T(q, right, [term(a, x, m * n), term(a * n, x, m * n), term(a ** n, x, m + n)],
                 "Raise the number to the power too: %d<sup>%d</sup> = %d, and %d × %d = %d: <b>%s</b>." % (a, n, a ** n, m, n, m * n, right))
    m, n, k = r.randint(2, 6), r.randint(2, 6), r.randint(1, 4)
    q = "Simplify %s." % B("%s × %s ÷ %s" % (pw(x, m), pw(x, n), pw(x, k)))
    right = pw(x, m + n - k)
    return T(q, right, [pw(x, m * n - k), pw(x, m + n + k), pw(x, F(m * n, k)) if (m * n) % k == 0 and F(m * n, k) != m + n - k else pw(x, m - n - k)],
             "%d + %d − %d = %d: <b>%s</b>." % (m, n, k, m + n - k, right))


def problems():
    its = []
    for q, a, w, e in [
        ("Find <i>n</i> if 2<sup>5</sup> × 2<sup><i>n</i></sup> = 2<sup>12</sup>.", "7", ["17", "2.4", "60"], "5 + <i>n</i> = 12, so <i>n</i> = <b>7</b>."),
        ("Find <i>n</i> if 3<sup>10</sup> ÷ 3<sup><i>n</i></sup> = 3<sup>4</sup>.", "6", ["14", "2.5", "40"], "10 − <i>n</i> = 4, so <i>n</i> = <b>6</b>."),
        ("Find <i>n</i> if (5<sup>3</sup>)<sup><i>n</i></sup> = 5<sup>12</sup>.", "4", ["9", "15", "36"], "3 × <i>n</i> = 12, so <i>n</i> = <b>4</b>."),
        ("Write 8 as a power of 2.", "2<sup>3</sup>", ["2<sup>4</sup>", "2<sup>8</sup>", "8<sup>2</sup>"], "2 × 2 × 2 = 8, so 8 = <b>2<sup>3</sup></b>."),
        ("Write 4<sup>3</sup> as a power of 2.", "2<sup>6</sup>", ["2<sup>5</sup>", "2<sup>7</sup>", "8<sup>3</sup>"], "4 = 2<sup>2</sup>, so 4<sup>3</sup> = (2<sup>2</sup>)<sup>3</sup> = <b>2<sup>6</sup></b>."),
        ("Which is the same as 1/9?", "3<sup>−2</sup>", ["−3<sup>2</sup>", "9<sup>−9</sup>", "3<sup>−3</sup>"], "3<sup>−2</sup> = 1 ÷ 3<sup>2</sup> = <b>1/9</b>.".replace("1/9", fr(1, 9))),
        ("Simplify 10<sup>4</sup> × 10<sup>3</sup> and write the answer as an ordinary number.", "10,000,000", ["1,000,000,000,000", "100,000", "1,000,000"], "10<sup>4</sup> × 10<sup>3</sup> = 10<sup>7</sup> = <b>10,000,000</b>."),
        ("Which is larger, 2<sup>10</sup> or 10<sup>3</sup>?", "2<sup>10</sup>", ["10<sup>3</sup>", "They are equal", "You cannot tell"], "2<sup>10</sup> = 1,024 and 10<sup>3</sup> = 1,000, so <b>2<sup>10</sup></b> is larger."),
        ("Leo says 3<sup>4</sup> × 3<sup>2</sup> = 9<sup>6</sup>. What is the correct answer?", "3<sup>6</sup>", ["3<sup>8</sup>", "9<sup>8</sup>", "9<sup>6</sup>"], "Keep the base and add the indices: <b>3<sup>6</sup></b>. Do not multiply the bases."),
        ("Simplify (2<i>a</i><sup>3</sup>)<sup>2</sup> × <i>a</i>.", "4<i>a</i><sup>7</sup>", ["2<i>a</i><sup>7</sup>", "4<i>a</i><sup>6</sup>", "4<i>a</i><sup>10</sup>"], "(2<i>a</i><sup>3</sup>)<sup>2</sup> = 4<i>a</i><sup>6</sup>, then × <i>a</i> = <b>4<i>a</i><sup>7</sup></b>."),
        ("Work out 5<sup>0</sup> + 5<sup>1</sup>.", "6", ["5", "1", "10"], "5<sup>0</sup> = 1 and 5<sup>1</sup> = 5, so <b>6</b>."),
        ("Work out 2<sup>−1</sup> + 2<sup>−2</sup>.", fr(3, 4), [fr(1, 6), "−6", fr(1, 8)], "1/2 + 1/4 = <b>3/4</b>.".replace("3/4", fr(3, 4))),
        ("Simplify <i>x</i><sup>5</sup> × <i>y</i><sup>2</sup> × <i>x</i><sup>3</sup>.", "<i>x</i><sup>8</sup><i>y</i><sup>2</sup>", ["<i>xy</i><sup>10</sup>", "<i>x</i><sup>15</sup><i>y</i><sup>2</sup>", "(<i>xy</i>)<sup>10</sup>"], "Only add indices of the same letter: <i>x</i><sup>5+3</sup><i>y</i><sup>2</sup> = <b><i>x</i><sup>8</sup><i>y</i><sup>2</sup></b>."),
        ("Work out (−2)<sup>5</sup>.", "−32", ["32", "−10", "10"], "An odd number of negatives gives a negative: <b>−32</b>."),
        ("Simplify 12<i>m</i><sup>6</sup><i>n</i><sup>3</sup> ÷ 4<i>m</i><sup>2</sup><i>n</i>.", "3<i>m</i><sup>4</sup><i>n</i><sup>2</sup>", ["8<i>m</i><sup>4</sup><i>n</i><sup>2</sup>", "3<i>m</i><sup>3</sup><i>n</i><sup>3</sup>", "3<i>m</i><sup>4</sup><i>n</i><sup>3</sup>"], "12 ÷ 4 = 3, <i>m</i><sup>6−2</sup> = <i>m</i><sup>4</sup>, <i>n</i><sup>3−1</sup> = <i>n</i><sup>2</sup>: <b>3<i>m</i><sup>4</sup><i>n</i><sup>2</sup></b>."),
        ("Find <i>n</i> if 2<sup><i>n</i></sup> = 64.", "6", ["32", "8", "5"], "2 × 2 × 2 × 2 × 2 × 2 = 64, so <i>n</i> = <b>6</b>."),
        ("Find <i>n</i> if 10<sup><i>n</i></sup> = 0.01.", "−2", ["2", "−1", "−3"], "0.01 = 1/100 = 1/10<sup>2</sup> = 10<sup>−2</sup>, so <i>n</i> = <b>−2</b>."),
        ("Which of these equals 1?", "7<sup>3</sup> ÷ 7<sup>3</sup>", ["7<sup>1</sup>", "1<sup>0</sup> − 1", "7 × 0"], "7<sup>3</sup> ÷ 7<sup>3</sup> = 7<sup>0</sup> = <b>1</b>."),
        ("Simplify (<i>p</i><sup>2</sup>)<sup>3</sup> ÷ <i>p</i><sup>4</sup>.", "<i>p</i><sup>2</sup>", ["<i>p</i>", "<i>p</i><sup>1.25</sup>", "<i>p</i><sup>10</sup>"], "(<i>p</i><sup>2</sup>)<sup>3</sup> = <i>p</i><sup>6</sup>, then 6 − 4 = 2: <b><i>p</i><sup>2</sup></b>."),
        ("Work out 4<sup>3</sup> ÷ 4<sup>5</sup>.", fr(1, 16), ["16", "−16", fr(1, 8)], "4<sup>3−5</sup> = 4<sup>−2</sup> = 1/16.".replace("1/16.", "<b>" + fr(1, 16) + "</b>.")),
    ]:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p>The <b>index</b> (power) tells you how many times the base is multiplied by itself. With the <b>same base</b>:</p>"
        "<ul><li>Multiplying: add the indices. <i>a</i><sup>m</sup> × <i>a</i><sup>n</sup> = <i>a</i><sup>m+n</sup></li>"
        "<li>Dividing: subtract the indices. <i>a</i><sup>m</sup> ÷ <i>a</i><sup>n</sup> = <i>a</i><sup>m−n</sup></li>"
        "<li>Power of a power: multiply the indices. (<i>a</i><sup>m</sup>)<sup>n</sup> = <i>a</i><sup>mn</sup></li>"
        "<li><i>a</i><sup>0</sup> = 1 and <i>a</i><sup>−n</sup> = 1 ÷ <i>a</i><sup>n</sup></li></ul>",
        [("Simplify 3<i>x</i><sup>2</sup> × 4<i>x</i><sup>5</sup>.", ["Multiply the numbers: 3 × 4 = 12.", "Add the indices: 2 + 5 = 7."], "12<i>x</i><sup>7</sup>"),
         ("Simplify (2<i>a</i><sup>3</sup>)<sup>2</sup>.", ["2<sup>2</sup> = 4.", "(<i>a</i><sup>3</sup>)<sup>2</sup> = <i>a</i><sup>6</sup>."], "4<i>a</i><sup>6</sup>"),
         ("Work out 2<sup>−3</sup>.", ["1 ÷ 2<sup>3</sup> = 1 ÷ 8."], fr(1, 8))],
        ["Multiplying the indices when you multiply powers: <i>a</i><sup>3</sup> × <i>a</i><sup>4</sup> = <i>a</i><sup>7</sup>, not <i>a</i><sup>12</sup>.",
         "Multiplying the bases: 3<sup>4</sup> × 3<sup>2</sup> = 3<sup>6</sup>, not 9<sup>6</sup>.",
         "Thinking 5<sup>0</sup> = 0. It is 1.",
         "Thinking 2<sup>−3</sup> is negative. It is 1/8."])


def main():
    sets = [S("Multiplying powers", collect(one_mul, 20, R)),
            S("Dividing powers", collect(one_div, 20, R)),
            S("Power of a power and the zero index", collect(one_pp, 20, R)),
            S("Negative indices and evaluating", collect(one_neg, 12, R) + collect(one_eval, 8, R)),
            S("Algebraic terms and problems", collect(one_alg, 10, R) + R.sample(problems(), 10))]
    make(8, "indices", 1, "N",
         "Laws of Indices: Multiplying, Dividing and Powers of Powers",
         "Year 8 Laws of Indices Worksheets: Multiply, Divide, Power of a Power, Zero and Negative Indices",
         "Laws of indices",
         "Use integer powers and associated real roots (square, cube and higher), recognise powers of 2, 3, 4, 5; "
         "simplify and manipulate algebraic expressions to maintain equivalence.",
         "Free Year 8 laws of indices worksheets: multiply and divide powers, power of a power, zero and negative indices, "
         "and simplify algebraic terms like 3x² × 4x⁵. 100 questions with answers.",
         "Same base: multiply → add the indices, divide → subtract, power of a power → multiply.",
         "a⁰ = 1 and a⁻ⁿ = 1 ÷ aⁿ. Multiply or divide the numbers in front as normal.",
         body(),
         [("What are the laws of indices?", "With the same base, add indices when multiplying, subtract when dividing, and multiply when raising a power to a power. a⁰ = 1 and a⁻ⁿ = 1/aⁿ."),
          ("Why is any number to the power 0 equal to 1?", "Because aⁿ ÷ aⁿ = a⁰, and any number divided by itself is 1."),
          ("Does a negative index make a number negative?", "No. It makes a fraction: 2⁻³ = 1/8."),
          ("How do I simplify 3x² × 4x⁵?", "Multiply the numbers (3 × 4 = 12) and add the indices of x (2 + 5 = 7) to get 12x⁷.")],
         sets, R)


if __name__ == "__main__":
    main()
