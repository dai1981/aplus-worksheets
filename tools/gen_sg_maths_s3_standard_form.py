# -*- coding: utf-8 -*-
"""
SG Secondary 3 Maths: Standard Form (Sec 3 Number)
  python3 tools/gen_sg_maths_s3_standard_form.py
Writing large and small numbers in standard form, converting back to ordinary numbers, ordering,
multiplying and dividing in standard form, and real-world problems.
Wrong answers come from real mistakes: counting the zeros instead of the places moved, a sign error for
small numbers, leaving the front number outside 1 ≤ A < 10, and adding the powers when dividing.
"""
import random
from fractions import Fraction as F
from sg_sec import num, mcq, B, S, make, lesson, collect, T, MINUS

R = random.Random(830200)


def sf(a, n):
    return "%s × 10<sup>%s</sup>" % (num(a), num(n))


def mant(r, dp=None):
    d = r.choice([0, 1, 1, 2, 2]) if dp is None else dp
    a = F(r.randint(10 ** d, 10 ** (d + 1) - 1), 10 ** d)
    return a


def ordinary(a, n):
    return F(a) * F(10) ** n


def norm(v):
    """value -> (a, n) with 1 <= a < 10"""
    v = F(v)
    n = 0
    while v >= 10:
        v /= 10; n += 1
    while v < 1:
        v *= 10; n -= 1
    return v, n


# ------------------------------------------------------------ set 1: large numbers
def one_big(r):
    a = mant(r)
    n = r.randint(3, 9)
    v = ordinary(a, n)
    if v.denominator != 1:
        return None
    q = "Write %s in standard form." % B(num(v))
    zeros = len(str(int(v))) - len(str(int(v)).rstrip("0"))
    wr = [sf(a, n + 1), sf(a * 10, n - 1), sf(a, zeros) if zeros != n else sf(a, n - 1), sf(a, -n)]
    e = "Put the decimal point after the first digit: %s. The point has moved %d places, so it is × 10<sup>%d</sup>: <b>%s</b>." % (num(a), n, n, sf(a, n))
    return T(q, sf(a, n), [w for w in wr if w != sf(a, n)][:3], e)


# ------------------------------------------------------------ set 2: small numbers
def one_small(r):
    a = mant(r)
    n = -r.randint(1, 7)
    v = ordinary(a, n)
    q = "Write %s in standard form." % B(num(v))
    zeros = len(num(v).replace(".", "")) - len(num(v).replace(".", "").lstrip("0"))
    wr = [sf(a, -n), sf(a, n - 1), sf(a, -zeros) if -zeros != n else sf(a, n + 1), sf(a / 10, n + 1)]
    e = "The first non-zero digit is %s. The point moves %d place%s to the right, so the power is negative: <b>%s</b>." % (
        num(int(a)), -n, "" if n == -1 else "s", sf(a, n))
    return T(q, sf(a, n), [w for w in wr if w != sf(a, n)][:3], e)


# ------------------------------------------------------------ set 3: back to ordinary numbers
def one_back(r):
    a = mant(r)
    n = r.choice([r.randint(2, 8), -r.randint(1, 6)])
    v = ordinary(a, n)
    q = "Write %s as an ordinary number." % B(sf(a, n))
    wr = [ordinary(a, n + 1), ordinary(a, n - 1), ordinary(a, -n)]
    if n > 0:
        wr.append(F(int(str(a).replace("/", "").split(".")[0]) if a.denominator == 1 else 0) * 0 + int(num(a).replace(".", "")) * 10 ** n)
    e = "%s 10<sup>%s</sup> moves the digits %d place%s to the %s: <b>%s</b>." % (
        "Multiplying by" if n > 0 else "Multiplying by", num(n), abs(n), "" if abs(n) == 1 else "s", "left" if n > 0 else "right", num(v))
    return mcq(q, (num(v), v), [(num(w), w) for w in wr if w != v], e)


# ------------------------------------------------------------ set 4: ordering, × and ÷
def one_order(r):
    vals = []
    while len(vals) < 4:
        a = mant(r, 1)
        n = r.choice([r.randint(3, 6), -r.randint(1, 4)])
        if (a, n) not in vals:
            vals.append((a, n))
    big = max(vals, key=lambda t: ordinary(*t))
    if sorted(ordinary(*t) for t in vals)[-2] == ordinary(*big):
        return None
    kind = r.choice(["largest", "smallest"])
    tgt = big if kind == "largest" else min(vals, key=lambda t: ordinary(*t))
    trap = max(vals, key=lambda t: t[0]) if kind == "largest" else min(vals, key=lambda t: t[0])
    if trap == tgt:
        return None
    q = "Which number is the %s?" % B(kind)
    e = "Compare the powers of 10 first, then the front numbers. The %s is <b>%s</b>." % (kind, sf(*tgt))
    return T(q, sf(*tgt), [sf(*t) for t in vals if t != tgt], e)


def one_md(r):
    a, b = mant(r, r.choice([0, 1])), mant(r, 0)
    m, n = r.randint(-4, 8), r.randint(-4, 6)
    if r.random() < 0.55:
        p = a * b
        ra, rn = norm(p * F(10) ** (m + n))
        if (p * 10) % 1:
            return None
        q = "Work out %s. Give your answer in standard form." % B("(%s) × (%s)" % (sf(a, m), sf(b, n)))
        right = sf(ra, rn)
        wr = [sf(p, m + n) if p >= 10 else sf(ra, rn + 1), sf(ra, m * n) if m * n != rn else sf(ra, rn - 1), sf(a + b, m + n) if a + b < 10 else sf(ra, -rn) if rn else sf(ra, rn + 2)]
        e = "Multiply the front numbers: %s × %s = %s. Add the powers: %s + %s = %s. %s<b>%s</b>." % (
            num(a), num(b), num(p), num(m), "(%s)" % num(n) if n < 0 else num(n), num(m + n),
            ("%s is not between 1 and 10, so adjust: " % num(p)) if p >= 10 else "", right)
    else:
        b = r.choice([2, 4, 5, F(5, 2)])
        a = b * r.choice([2, 3, F(3, 2), 4, 1, F(7, 4)])
        if a >= 10 or a < 1:
            return None
        p = a / b
        ra, rn = norm(p * F(10) ** (m - n))
        q = "Work out %s. Give your answer in standard form." % B("(%s) ÷ (%s)" % (sf(a, m), sf(b, n)))
        right = sf(ra, rn)
        wr = [sf(ra, m + n) if m + n != rn else sf(ra, rn + 1), sf(ra, n - m) if n - m != rn else sf(ra, rn - 2), sf(a - b if a > b else b / a, rn) if (a - b if a > b else b / a) != ra else sf(ra, rn + 3)]
        e = "Divide the front numbers: %s ÷ %s = %s. Subtract the powers: %s − %s = %s. %s<b>%s</b>." % (
            num(a), num(b), num(p), num(m), "(%s)" % num(n) if n < 0 else num(n), num(m - n),
            ("%s is less than 1, so adjust: " % num(p)) if p < 1 else "", right)
    wr = [w for w in wr if w != right and "<sup>0.</sup>" not in w]
    if len(set(wr)) < 3 or ra.denominator > 1000:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    data = [
        ("The distance from the Earth to the Sun is about 150 000 000 km. Write this in standard form.", sf(F(3, 2), 8), [sf(15, 7), sf(F(3, 2), 7), sf(F(3, 2), 9)],
         "Move the point 8 places: <b>%s km</b>." % sf(F(3, 2), 8)),
        ("A grain of sand has a mass of about 0.000 06 g. Write this in standard form.".replace("0.000 06", "0.00006"), sf(6, -5), [sf(6, 5), sf(6, -4), sf(F(6, 10), -4)],
         "The 6 is 5 places after the point: <b>%s g</b>." % sf(6, -5)),
        ("The population of Singapore is about 6.0 × 10<sup>6</sup>. Write this as an ordinary number.", "6 000 000", ["600 000", "60 000 000", "6 000 000 000"],
         "Move the digits 6 places to the left: <b>6 000 000</b>."),
        ("A virus is 1.2 × 10<sup>−7</sup> m long. Write this as an ordinary number.", "0.00000012", ["0.0000012", "0.000000012", "12 000 000"],
         "Move the digits 7 places to the right: <b>0.00000012 m</b>."),
        ("Light travels about 3 × 10<sup>5</sup> km every second. How far does it travel in 2 × 10<sup>3</sup> seconds?", sf(6, 8), [sf(6, 15), sf(5, 8), sf(6, 2)],
         "(3 × 2) × 10<sup>5 + 3</sup> = <b>%s km</b>." % sf(6, 8)),
        ("Which number is NOT written in standard form?", "12 × 10<sup>4</sup>", [sf(F(12, 10), 4), sf(9, -3), sf(1, 6)],
         "The front number must be at least 1 and less than 10. 12 is too big, so <b>12 × 10<sup>4</sup></b> is not in standard form."),
        ("Write 45 × 10<sup>6</sup> correctly in standard form.", sf(F(45, 10), 7), [sf(F(45, 10), 6), sf(F(45, 10), 5), sf(45, 6)],
         "45 = 4.5 × 10<sup>1</sup>, so 45 × 10<sup>6</sup> = <b>%s</b>." % sf(F(45, 10), 7)),
        ("Write 0.3 × 10<sup>−2</sup> correctly in standard form.", sf(3, -3), [sf(3, -1), sf(3, -2), sf(3, 3)],
         "0.3 = 3 × 10<sup>−1</sup>, so the answer is 3 × 10<sup>−1 + (−2)</sup> = <b>%s</b>." % sf(3, -3)),
        ("Mars is 2.28 × 10<sup>8</sup> km from the Sun. Jupiter is 7.78 × 10<sup>8</sup> km. How much further is Jupiter?", sf(F(55, 10), 8), [sf(F(55, 10), 0), sf(55, 8), sf(F(1006, 100), 8)],
         "The powers are the same, so subtract the front numbers: 7.78 − 2.28 = 5.5. Answer <b>%s km</b>." % sf(F(55, 10), 8)),
        ("Work out (4 × 10<sup>3</sup>) + (5 × 10<sup>2</sup>). Give your answer in standard form.", sf(F(45, 10), 3), [sf(9, 5), sf(9, 3), sf(9, 2)],
         "4000 + 500 = 4500 = <b>%s</b>." % sf(F(45, 10), 3)),
        ("An atom has a diameter of 1 × 10<sup>−10</sup> m. How many atoms side by side make 1 mm (1 × 10<sup>−3</sup> m)?", sf(1, 7), [sf(1, -7), sf(1, 13), sf(1, 30)],
         "(1 × 10<sup>−3</sup>) ÷ (1 × 10<sup>−10</sup>) = 10<sup>−3 − (−10)</sup> = <b>%s</b>." % sf(1, 7)),
        ("Which is the smallest?", sf(9, -4), [sf(1, -3), sf(F(5, 2), -2), sf(F(11, 10), -1)], "The most negative power of 10 is the smallest: <b>%s</b> = 0.0009." % sf(9, -4)),
        ("A hard drive holds 2 × 10<sup>12</sup> bytes. A photo uses 4 × 10<sup>6</sup> bytes. How many photos fit?", sf(5, 5), [sf(5, 6), sf(2, 6), sf(8, 18)],
         "(2 ÷ 4) × 10<sup>12 − 6</sup> = 0.5 × 10<sup>6</sup> = <b>%s</b>." % sf(5, 5)),
        ("What is 10<sup>5</sup> as an ordinary number?", "100 000", ["50", "10 000", "1 000 000"], "1 followed by 5 zeros: <b>100 000</b>."),
        ("What is 10<sup>−3</sup> as a decimal?", "0.001", ["0.0001", "−1000", "0.01"], "10<sup>−3</sup> = 1 ÷ 1000 = <b>0.001</b>."),
        ("The mass of the Earth is about 5.97 × 10<sup>24</sup> kg. The Moon is about 7.35 × 10<sup>22</sup> kg. Which is heavier?", "The Earth", ["The Moon", "They are the same", "You cannot tell"],
         "10<sup>24</sup> is 100 times 10<sup>22</sup>, so <b>the Earth</b> is much heavier."),
        ("Write 3 070 000 in standard form.", sf(F(307, 100), 6), [sf(F(307, 100), 5), sf(307, 4), sf(F(37, 10), 6)], "Move the point 6 places: <b>%s</b>. Keep the zero between 3 and 7." % sf(F(307, 100), 6)),
        ("Write 0.000405 in standard form.", sf(F(405, 100), -4), [sf(F(405, 100), -3), sf(405, -6), sf(F(45, 10), -4)], "The first non-zero digit is the 4th place after the point: <b>%s</b>." % sf(F(405, 100), -4)),
        ("Work out (6 × 10<sup>5</sup>)<sup>2</sup>. Give your answer in standard form.", sf(F(36, 10), 11), [sf(36, 10), sf(F(36, 10), 25), sf(12, 10)],
         "6<sup>2</sup> = 36 and (10<sup>5</sup>)<sup>2</sup> = 10<sup>10</sup>. 36 × 10<sup>10</sup> = <b>%s</b>." % sf(F(36, 10), 11)),
        ("Work out (8 × 10<sup>4</sup>) − (3 × 10<sup>3</sup>). Give your answer in standard form.", sf(F(77, 10), 4), [sf(5, 1), sf(5, 4), sf(5, 3)],
         "80 000 − 3000 = 77 000 = <b>%s</b>." % sf(F(77, 10), 4)),
    ]
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p>A number in standard form is written as <b><i>A</i> × 10<sup><i>n</i></sup></b>, where 1 ≤ <i>A</i> &lt; 10 "
        "and <i>n</i> is a whole number. Large numbers have a positive power; small numbers (less than 1) have a negative power.</p>"
        "<p>To multiply, multiply the front numbers and add the powers. To divide, divide the front numbers and subtract "
        "the powers. Then adjust if the front number is not between 1 and 10.</p>",
        [("Write 4 700 000 in standard form.", ["4.7, and the point moves 6 places."], "4.7 × 10<sup>6</sup>"),
         ("Write 0.00052 in standard form.", ["5.2, and the point moves 4 places to the right."], "5.2 × 10<sup>−4</sup>"),
         ("Work out (5 × 10<sup>3</sup>) × (4 × 10<sup>6</sup>).", ["5 × 4 = 20 and 3 + 6 = 9.", "20 × 10<sup>9</sup> = 2 × 10<sup>10</sup>."], "2 × 10<sup>10</sup>")],
        ["Counting the zeros instead of the places the point moves: 4 700 000 is 4.7 × 10<sup>6</sup>, not 10<sup>5</sup>.",
         "Using a positive power for a small number: 0.00052 = 5.2 × 10<sup>−4</sup>.",
         "Leaving the front number too big: 20 × 10<sup>9</sup> should be 2 × 10<sup>10</sup>.",
         "Ordering by the front number only: 9 × 10<sup>3</sup> is smaller than 1 × 10<sup>4</sup>."])


def main():
    sets = [S("Large numbers in standard form", collect(one_big, 20, R)),
            S("Small numbers in standard form", collect(one_small, 20, R)),
            S("Standard form to ordinary numbers", collect(one_back, 20, R)),
            S("Ordering, multiplying and dividing", collect(one_order, 6, R) + collect(one_md, 14, R)),
            S("Problems", problems())]
    make(3, "standard-form", 2, "N1",
         "Standard Form: Writing, Ordering and Calculating",
         "Secondary 3 Standard Form Worksheets: Large and Small Numbers, Converting, Multiplying and Dividing",
         "Standard form",
         "Interpret and compare numbers in standard form A × 10ⁿ, 1 ≤ A < 10, where n is a positive or negative integer or zero.",
         "Free Secondary 3 standard form worksheets: write large and small numbers in standard form, convert back to ordinary "
         "numbers, order numbers, and multiply and divide in standard form. 100 questions with answers.",
         "Standard form is A × 10ⁿ with 1 ≤ A < 10. Big numbers have positive n, small numbers negative n.",
         "To multiply, multiply the front numbers and add the powers. Then adjust so the front number is between 1 and 10.",
         body(),
         [("What is standard form?", "A way of writing very large or very small numbers as A × 10ⁿ, where A is at least 1 and less than 10."),
          ("How do I write a small number in standard form?", "Move the decimal point to after the first non-zero digit. Count the places moved, and use a negative power: 0.00052 = 5.2 × 10⁻⁴."),
          ("How do I multiply numbers in standard form?", "Multiply the front numbers and add the powers of 10. If the front number becomes 10 or more, adjust: 20 × 10⁹ = 2 × 10¹⁰."),
          ("How do I compare numbers in standard form?", "Compare the powers of 10 first. Only if they are the same, compare the front numbers.")],
         sets, R)


if __name__ == "__main__":
    main()
