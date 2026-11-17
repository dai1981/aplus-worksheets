# -*- coding: utf-8 -*-
"""
AU Year 8 Maths: Index laws (Australian Curriculum v9.0: AC9M8N02)
  python3 tools/gen_au_maths_y8_index_laws.py
Multiplying and dividing powers with the same base, a power of a power, the zero exponent, evaluating with
index laws, and finding a missing exponent.
Wrong answers come from real mistakes: multiplying the exponents when multiplying powers, multiplying the
bases (3⁴ × 3² = 9⁶), thinking 5⁰ = 0, and adding exponents for a power of a power.
"""
import random
from fractions import Fraction as F
from au_hs import NBSP, num, mcq, B, S, make, lesson, collect, QN, T, fr, MINUS

R = random.Random(80201)
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
    return r.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])


# ------------------------------------------------------------ set 1: multiplying
def one_mul(r):
    b = base(r)
    m, n = r.randint(2, 9), r.randint(1, 8)
    q = "Simplify %s, giving your answer as a single power." % B("%s × %s" % (pw(b, m), pw(b, n)))
    e = "Same base, so add the exponents: %d + %d = %d. The answer is <b>%s</b>." % (m, n, m + n, pw(b, m + n))
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
    e = "Same base, so subtract the exponents: %d − %d = %d. The answer is <b>%s</b>." % (m, n, m - n, pw(b, m - n))
    wr = [pw(b, m + n), pw(b, F(m, n)) if m % n == 0 else pw(b, n - m), pw(1, m - n) if isinstance(b, int) else pw(b, m * n), pw(b, m - n + 1)]
    return T(q, pw(b, m - n), [w for w in wr if w != pw(b, m - n)][:3], e)


# ------------------------------------------------------------ set 3: power of a power, zero index
def one_pp(r):
    b = base(r)
    kind = r.random()
    if kind < 0.65:
        m, n = r.randint(2, 6), r.randint(2, 5)
        q = "Simplify %s." % B("(%s)<sup>%d</sup>" % (pw(b, m), n))
        e = "A power of a power: multiply the exponents, %d × %d = %d. The answer is <b>%s</b>." % (m, n, m * n, pw(b, m * n))
        return T(q, pw(b, m * n), [pw(b, m + n), pw(b, m ** n) if m ** n < 100 else pw(b, m * n + 1), pw(b, m * n - 1)], e)
    if kind < 0.85:
        b2 = r.choice([5, 9, 12, 100, 3, 47, 2, 1000, 8])
        q = "What is the value of %s?" % B(pw(b2, 0))
        return T(q, "1", ["0", str(b2) if isinstance(b2, int) else b2, "Undefined"], "Any number (except 0) to the power 0 is <b>1</b>.")
    m = r.randint(2, 7)
    q = "Simplify %s." % B("%s ÷ %s" % (pw(b, m), pw(b, m)))
    e = "%d − %d = 0, so the answer is %s = <b>1</b>." % (m, m, pw(b, 0))
    return T(q, "1", ["0", pw(b, 2 * m) if True else "", pw(b, 1)], e)



# ------------------------------------------------------------ set 4: evaluating
def one_eval(r):
    a = r.choice([2, 3, 4, 5, 10])
    kind = r.choice(["div", "mul", "pp", "zero"])
    if kind == "div":
        n = r.randint(1, 6)
        m = n + r.randint(1, 4 if a < 5 else 3)
        v = a ** (m - n)
        q = "Work out %s without a calculator." % B("%s ÷ %s" % (pw(a, m), pw(a, n)))
        e = "%s ÷ %s = %s = <b>%s</b>." % (pw(a, m), pw(a, n), pw(a, m - n), num(v)) if m - n > 1 else "%s ÷ %s = %s<sup>1</sup> = <b>%s</b>." % (pw(a, m), pw(a, n), a, num(v))
        return QN(q, v, [a ** (m + n) if a ** (m + n) < 10 ** 7 else None, m - n, a * (m - n)], e)
    if kind == "mul":
        m, n = r.randint(1, 4), r.randint(1, 3)
        if a ** (m + n) > 10 ** 6:
            return None
        v = a ** (m + n)
        q = "Work out %s without a calculator." % B("%s × %s" % (pw(a, m), pw(a, n)))
        e = "%s × %s = %s = <b>%s</b>." % (pw(a, m), pw(a, n), pw(a, m + n), num(v))
        return QN(q, v, [a ** (m * n) if a ** (m * n) < 10 ** 7 and m * n != m + n else a ** (m + n + 1), (a * a) ** (m + n) if (a * a) ** (m + n) < 10 ** 7 else None, a * (m + n)], e)
    if kind == "pp":
        m, n = r.randint(1, 3), r.randint(2, 3)
        if a ** (m * n) > 10 ** 6:
            return None
        v = a ** (m * n)
        q = "Work out %s without a calculator." % B("(%s)<sup>%d</sup>" % (pw(a, m), n))
        e = "(%s)<sup>%d</sup> = %s = <b>%s</b>." % (pw(a, m), n, pw(a, m * n), num(v))
        return QN(q, v, [a ** (m + n) if m * n != m + n else a ** (m * n + 1), a * m * n, (a * n) ** m], e)
    m, k = r.randint(2, 6), r.randint(2, 9)
    q = "Work out %s." % B("%d × %s" % (k, pw(a, 0)))
    return QN(q, k, [0, k * a, k + 1], "%s = 1, so %d × 1 = <b>%d</b>." % (pw(a, 0), k, k))


# ------------------------------------------------------------ set 5: problems
def problems():
    data = [
        ("Find <i>n</i> if 2<sup>5</sup> × 2<sup><i>n</i></sup> = 2<sup>12</sup>.", "7", ["17", "2.4", "60"], "5 + <i>n</i> = 12, so <i>n</i> = <b>7</b>."),
        ("Find <i>n</i> if 3<sup>10</sup> ÷ 3<sup><i>n</i></sup> = 3<sup>4</sup>.", "6", ["14", "2.5", "40"], "10 − <i>n</i> = 4, so <i>n</i> = <b>6</b>."),
        ("Find <i>n</i> if (5<sup>3</sup>)<sup><i>n</i></sup> = 5<sup>12</sup>.", "4", ["9", "15", "36"], "3 × <i>n</i> = 12, so <i>n</i> = <b>4</b>."),
        ("Write 8 as a power of 2.", "2<sup>3</sup>", ["2<sup>4</sup>", "2<sup>8</sup>", "8<sup>2</sup>"], "2 × 2 × 2 = 8, so 8 = <b>2<sup>3</sup></b>."),
        ("Write 4<sup>3</sup> as a power of 2.", "2<sup>6</sup>", ["2<sup>5</sup>", "2<sup>7</sup>", "8<sup>3</sup>"], "4 = 2<sup>2</sup>, so 4<sup>3</sup> = (2<sup>2</sup>)<sup>3</sup> = <b>2<sup>6</sup></b>."),
        ("Write 10<sup>4</sup> × 10<sup>3</sup> as an ordinary number.", "10 000 000", ["1 000 000 000 000", "100 000", "1 000 000"], "10<sup>4</sup> × 10<sup>3</sup> = 10<sup>7</sup> = <b>10 000 000</b>."),
        ("Which is larger, 2<sup>10</sup> or 10<sup>3</sup>?", "2<sup>10</sup>", ["10<sup>3</sup>", "They are equal", "You cannot tell"], "2<sup>10</sup> = 1024 and 10<sup>3</sup> = 1000, so <b>2<sup>10</sup></b> is larger."),
        ("Lachlan says 3<sup>4</sup> × 3<sup>2</sup> = 9<sup>6</sup>. What is the correct answer?", "3<sup>6</sup>", ["3<sup>8</sup>", "9<sup>8</sup>", "9<sup>6</sup>"], "Keep the base and add the exponents: <b>3<sup>6</sup></b>. Do not multiply the bases."),
        ("Work out 5<sup>0</sup> + 5<sup>1</sup>.", "6", ["5", "1", "10"], "5<sup>0</sup> = 1 and 5<sup>1</sup> = 5, so <b>6</b>."),
        ("Work out (−2)<sup>5</sup>.", "−32", ["32", "−10", "10"], "An odd number of negatives gives a negative: <b>−32</b>."),
        ("Find <i>n</i> if 2<sup><i>n</i></sup> = 64.", "6", ["32", "8", "5"], "2 × 2 × 2 × 2 × 2 × 2 = 64, so <i>n</i> = <b>6</b>."),
        ("Which of these equals 1?", "7<sup>3</sup> ÷ 7<sup>3</sup>", ["7<sup>1</sup>", "1<sup>0</sup> − 1", "7 × 0"], "7<sup>3</sup> ÷ 7<sup>3</sup> = 7<sup>0</sup> = <b>1</b>."),
        ("Why is 6<sup>0</sup> equal to 1?", "Because 6<sup>3</sup> ÷ 6<sup>3</sup> = 6<sup>0</sup>, and any number divided by itself is 1", ["Because 6 × 0 = 1", "Because the exponent is 0 so the answer is 0", "It is not; 6<sup>0</sup> = 6"],
         "6<sup>3</sup> ÷ 6<sup>3</sup> = 6<sup>3−3</sup> = 6<sup>0</sup>, and it also equals 1. <b>So 6<sup>0</sup> = 1.</b>"),
        ("Simplify 2<sup>3</sup> × 2<sup>4</sup> ÷ 2<sup>5</sup>.", "2<sup>2</sup>", ["2<sup>12</sup>", "2<sup>7</sup>", "2<sup>−2</sup>"], "3 + 4 − 5 = 2: <b>2<sup>2</sup></b> = 4."),
        ("Write 9<sup>4</sup> as a power of 3.", "3<sup>8</sup>", ["3<sup>6</sup>", "3<sup>4</sup>", "27<sup>4</sup>"], "9 = 3<sup>2</sup>, so 9<sup>4</sup> = 3<sup>8</sup>."),
        ("A bacteria colony doubles every hour. It starts with 1 cell. After how many hours are there 2<sup>10</sup> cells?", "10", ["20", "5", "1024"], "Each hour multiplies by 2, so after <b>10</b> hours there are 2<sup>10</sup> cells."),
        ("A bacteria colony doubles every hour. After 4 hours it has 3 × 2<sup>4</sup> cells. How many cells is that?", "48", ["24", "1296", "96"], "2<sup>4</sup> = 16 and 3 × 16 = <b>48</b>."),
        ("Which is the same as 5<sup>2</sup> × 5<sup>2</sup> × 5<sup>2</sup>?", "(5<sup>2</sup>)<sup>3</sup>", ["5<sup>8</sup>", "15<sup>2</sup>", "5<sup>222</sup>"], "Three lots of 5<sup>2</sup> multiplied: (5<sup>2</sup>)<sup>3</sup> = 5<sup>6</sup>."),
        ("Simplify (10<sup>2</sup>)<sup>3</sup> and write it as an ordinary number.", "1 000 000", ["100 000", "10 000", "1000"], "(10<sup>2</sup>)<sup>3</sup> = 10<sup>6</sup> = <b>1 000 000</b>."),
        ("Which calculation gives 3<sup>9</sup>?", "3<sup>4</sup> × 3<sup>5</sup>", ["3<sup>3</sup> × 3<sup>3</sup>", "(3<sup>3</sup>)<sup>6</sup>", "3<sup>18</sup> ÷ 3<sup>2</sup>"], "4 + 5 = 9: <b>3<sup>4</sup> × 3<sup>5</sup></b>."),
    ]
    fix = lambda t: t.replace(" 000", NBSP + "000")
    data = [(q, fix(a_), [fix(w) for w in ws], fix(e)) for q, a_, ws, e in data]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>The <b>exponent</b> (index) tells you how many times the base is multiplied by itself. With the <b>same base</b>:</p>"
        "<ul><li>Multiplying: add the exponents. 2<sup>3</sup> × 2<sup>4</sup> = 2<sup>7</sup></li>"
        "<li>Dividing: subtract the exponents. 5<sup>6</sup> ÷ 5<sup>2</sup> = 5<sup>4</sup></li>"
        "<li>Power of a power: multiply the exponents. (3<sup>2</sup>)<sup>4</sup> = 3<sup>8</sup></li>"
        "<li>Zero exponent: any non-zero number to the power 0 is 1. 7<sup>0</sup> = 1</li></ul>",
        [("Simplify 4<sup>5</sup> × 4<sup>3</sup>.", ["Same base: add 5 + 3."], "4<sup>8</sup>"),
         ("Work out 10<sup>7</sup> ÷ 10<sup>4</sup>.", ["Subtract: 10<sup>3</sup>."], "1000"),
         ("Simplify (2<sup>3</sup>)<sup>2</sup>.", ["Multiply 3 × 2."], "2<sup>6</sup> = 64")],
        ["Multiplying the exponents when you multiply powers: 2<sup>3</sup> × 2<sup>4</sup> = 2<sup>7</sup>, not 2<sup>12</sup>.",
         "Multiplying the bases: 3<sup>4</sup> × 3<sup>2</sup> = 3<sup>6</sup>, not 9<sup>6</sup>.",
         "Thinking 5<sup>0</sup> = 0. It is 1.",
         "Adding the exponents for a power of a power: (3<sup>2</sup>)<sup>4</sup> = 3<sup>8</sup>, not 3<sup>6</sup>."])


def main():
    sets = [S("Multiplying powers", collect(one_mul, 20, R)),
            S("Dividing powers", collect(one_div, 20, R)),
            S("Power of a power and the zero exponent", collect(one_pp, 20, R)),
            S("Evaluating with index laws", collect(one_eval, 20, R)),
            S("Index law problems", problems())]
    make(8, "index-laws", 2, "AC9M8N02",
         "Index Laws: Multiplying, Dividing, Power of a Power and the Zero Exponent",
         "Year 8 Index Laws Worksheets: Multiplying and Dividing Powers and the Zero Exponent (Free, Answer Key)",
         "Index laws",
         "establish and apply the exponent laws with positive integer exponents and the zero-exponent, using exponent notation with numbers",
         "Free Year 8 maths worksheets on index laws for the Australian Curriculum (AC9M8N02): multiplying and dividing powers, "
         "power of a power, the zero exponent, evaluating and finding missing exponents. 100 questions with an answer key.",
         "Same base: multiply → add the exponents, divide → subtract, power of a power → multiply.",
         "Any non-zero number to the power 0 is 1.",
         body(),
         [("What are the index laws?", "With the same base, add exponents when multiplying, subtract when dividing, and multiply when raising a power to a power. Any non-zero number to the power 0 is 1."),
          ("Why is any number to the power 0 equal to 1?", "Because aⁿ ÷ aⁿ = a⁰, and any number divided by itself is 1."),
          ("Can I use index laws with different bases?", "Not directly. 2³ × 3² cannot be written as one power, but 4³ can be rewritten as 2⁶ first."),
          ("What is the difference between 2³ × 2⁴ and (2³)⁴?", "2³ × 2⁴ = 2⁷ (add the exponents), but (2³)⁴ = 2¹² (multiply the exponents).")],
         sets, R)


if __name__ == "__main__":
    main()
