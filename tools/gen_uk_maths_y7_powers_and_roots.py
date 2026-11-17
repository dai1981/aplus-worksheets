# -*- coding: utf-8 -*-
"""
UK Year 7 Maths: Powers and Roots (KS3 Number)
  python3 tools/gen_uk_maths_y7_powers_and_roots.py
Squares, cubes, square and cube roots, index notation, estimating roots, and problems with squares and cubes.
Wrong answers come from real mistakes: multiplying by the power (5² = 10), halving for a square root,
dividing by 3 for a cube root, and squaring a negative to a negative.
"""
import random
from fractions import Fraction as F
from uk_ks3 import num, mcq, B, S, make, lesson, collect, QN, T, MINUS

R = random.Random(70501)


def sup(b, e):
    bs = num(b) if F(b) >= 0 else "(%s)" % num(b)
    return "%s<sup>%d</sup>" % (bs, e)


# ------------------------------------------------------------ set 1: squares and cubes
def one_sqcube(r):
    kind = r.choice(["sq", "sq", "cube", "dec", "neg"])
    if kind == "sq":
        b = r.randint(2, 15); v = b * b
        return QN("Work out %s." % B(sup(b, 2)), v, [2 * b, b + 2, v + b],
                  "%s means %d × %d = <b>%d</b>, not %d × 2." % (sup(b, 2), b, b, v, b))
    if kind == "cube":
        b = r.randint(2, 10); v = b ** 3
        return QN("Work out %s." % B(sup(b, 3)), v, [3 * b, b * b, v + b * b],
                  "%s means %d × %d × %d = <b>%s</b>." % (sup(b, 3), b, b, b, num(v)))
    if kind == "dec":
        b = F(r.randint(2, 9), 10); v = b * b
        return QN("Work out %s." % B(sup(b, 2)), v, [b * 2, v * 10, v * 100],
                  "%s × %s = <b>%s</b>. Two decimal places × one decimal place each gives two decimal places." % (num(b), num(b), num(v)))
    b = -r.randint(2, 9)
    e2 = r.choice([2, 3])
    v = b ** e2
    return QN("Work out %s." % B(sup(b, e2)), v, [-v, b * e2, -b * e2],
              "%s. %s. The answer is <b>%s</b>." % (" × ".join([num(b)] * e2),
              "Two negatives make a positive" if e2 == 2 else "Three negatives make a negative", num(v)))


# ------------------------------------------------------------ set 2: roots
def one_root(r):
    kind = r.choice(["sq", "sq", "cube", "est"])
    if kind == "sq":
        b = r.randint(2, 15); n = b * b
        return QN("Work out %s." % B("√%d" % n), b, [n // 2, n * n if n < 40 else n - b, b + 1],
                  "%d × %d = %d, so √%d = <b>%d</b>. A square root is not half the number." % (b, b, n, n, b))
    if kind == "cube":
        b = r.randint(2, 10); n = b ** 3
        wr = [n // 3 if n % 3 == 0 else None, b * b, b + 1]
        return QN("Work out %s." % B("∛%s" % num(n)), b, [w for w in wr if w],
                  "%d × %d × %d = %s, so ∛%s = <b>%d</b>." % (b, b, b, num(n), num(n), b))
    n = r.randint(5, 140)
    import math
    lo = int(math.isqrt(n))
    if lo * lo == n:
        return None
    right = "%d and %d" % (lo, lo + 1)
    wr = ["%d and %d" % (lo - 1, lo), "%d and %d" % (lo + 1, lo + 2), "%d and %d" % (n // 2 - 1, n // 2)]
    if right in wr:
        return None
    return T("Between which two whole numbers is %s?" % B("√%d" % n), right, wr,
             "%d² = %d and %d² = %d. %d is between them, so √%d is between <b>%s</b>." % (lo, lo * lo, lo + 1, (lo + 1) ** 2, n, n, right))


# ------------------------------------------------------------ set 3: index notation
def one_index(r):
    kind = r.choice(["write", "eval", "eval", "ten"])
    if kind == "write":
        b, e = r.randint(2, 9), r.randint(3, 6)
        if b == e:
            return None
        q = "Write %s using index notation." % B(" × ".join([str(b)] * e))
        right = sup(b, e)
        return T(q, right, [sup(e, b), "%d × %d" % (b, e), sup(b * e, 1).replace("<sup>1</sup>", "")],
                 "%d is multiplied by itself %d times, so it is <b>%s</b>." % (b, e, right))
    if kind == "eval":
        b, e = r.choice([(2, 4), (2, 5), (2, 6), (2, 7), (3, 4), (5, 3), (4, 3), (3, 3), (2, 8), (6, 3), (10, 3), (1, 7)])
        v = b ** e
        return QN("Work out %s." % B(sup(b, e)), v, [b * e, e ** b if e ** b != v else v + b, v // b],
                  "%s = %s = <b>%s</b>." % (sup(b, e), " × ".join([str(b)] * e), num(v)))
    e = r.randint(3, 7)
    v = 10 ** e
    return QN("Work out %s." % B(sup(10, e)), v, [10 * e, 10 ** (e - 1), 10 ** (e + 1)],
              "%s is 1 followed by %d zeros: <b>%s</b>." % (sup(10, e), e, num(v)))


# ------------------------------------------------------------ set 4: mixed calculations
def one_mix(r):
    a, b = r.randint(2, 9), r.randint(2, 6)
    form = r.randint(0, 4)
    if form == 0:
        v = a * a + b ** 3
        return QN("Work out %s." % B("%s + %s" % (sup(a, 2), sup(b, 3))), v, [2 * a + 3 * b, (a + b) ** 2, a * a + b * b],
                  "%d + %d = <b>%d</b>." % (a * a, b ** 3, v))
    if form == 1:
        n = (a + 2) ** 2
        v = n and (a + 2) * b
        return QN("Work out %s." % B("%d × √%d" % (b, n)), v, [b * n // 2 if n % 2 == 0 else b * n, (a + 2) + b, b * n],
                  "√%d = %d, then %d × %d = <b>%d</b>." % (n, a + 2, b, a + 2, v))
    if form == 2:
        n = a * a
        v = b * b - a if b * b > a else None
        if v is None or v == 0:
            return None
        return QN("Work out %s." % B("%s %s √%d" % (sup(b, 2), MINUS, n)), v, [b * b - n, 2 * b - a, b * b - n // 2],
                  "%s = %d and √%d = %d, so %d − %d = <b>%d</b>." % (sup(b, 2), b * b, n, a, b * b, a, v))
    if form == 3:
        v = (a * b) ** 2
        return QN("Work out %s." % B("(%d × %d)<sup>2</sup>" % (a, b)), v, [a * b * 2, a * a * b, a * b * b],
                  "%d × %d = %d, then %d² = <b>%s</b>." % (a, b, a * b, a * b, num(v)))
    n = a * a
    m = b * b
    v = a + b
    return QN("Work out %s." % B("√%d + √%d" % (n, m)), v, [int((n + m) ** 0.5) if int((n + m) ** 0.5) ** 2 == n + m else n + m, (n + m) // 2, v + 1],
              "√%d = %d and √%d = %d, so the answer is <b>%d</b>. (You cannot add the numbers under the roots first.)" % (n, a, m, b, v))


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    for area in [49, 81, 144, 64, 121]:
        s = int(area ** 0.5)
        its.append(QN("A square has an area of %d cm². What is the length of one side?" % area, s, [area // 4, area // 2, s * 2],
                      "Side × side = %d, so the side is √%d = <b>%d cm</b>." % (area, area, s), unit=" cm"))
    for vol in [27, 125, 64, 1000]:
        s = round(vol ** (1 / 3))
        its.append(QN("A cube has a volume of %s cm³. What is the length of one edge?" % num(vol), s, [vol // 3 if vol % 3 == 0 else vol // 2, s * s, s + 2],
                      "Edge × edge × edge = %s, so the edge is ∛%s = <b>%d cm</b>." % (num(vol), num(vol), s), unit=" cm"))
    for a, b in [((2, 5), (5, 2)), ((3, 4), (4, 3)), ((2, 6), (6, 2)), ((10, 2), (2, 10))]:
        va, vb = a[0] ** a[1], b[0] ** b[1]
        big = sup(*a) if va > vb else sup(*b)
        q = "Which is larger: %s or %s?" % (B(sup(*a)), B(sup(*b)))
        e = "%s = %s and %s = %s, so <b>%s</b> is larger." % (sup(*a), num(va), sup(*b), num(vb), big)
        its.append(T(q, big, ["They are equal", "You cannot tell without a calculator",
                              sup(*b) if big == sup(*a) else sup(*a)], e))
    for n in [36, 100, 64]:
        k = int(n ** 0.5)
        its.append(T("Which number has a square root of %d?" % k, str(n), [str(k * 2), str(k * 3), str(n + 1)],
                     "%d² = %d, so the number is <b>%d</b>." % (k, n, n)))
    data = [
        ("Which of these is a square number and a cube number?", "64", ["16", "27", "100"], "64 = 8² and 64 = 4³, so <b>64</b>."),
        ("Which of these is a cube number?", "125", ["25", "150", "100"], "125 = 5 × 5 × 5 = 5³, so <b>125</b>."),
        ("A square patio has sides of 4.5 m. What is its area?", "20.25 m²", ["9 m²", "18 m²", "20.5 m²"], "4.5 × 4.5 = <b>20.25 m²</b>."),
        ("Which is the value of √0.25?", "0.5", ["0.125", "0.05", "0.0625"], "0.5 × 0.5 = 0.25, so √0.25 = <b>0.5</b>."),
    ]
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p>A power tells you how many times to multiply a number by itself: 5² = 5 × 5 = 25 and 2³ = 2 × 2 × 2 = 8.</p>"
        "<p>A <b>square root</b> undoes squaring: √25 = 5. A <b>cube root</b> undoes cubing: ∛8 = 2.</p>"
        "<p>To estimate √50, find the square numbers either side: 49 = 7² and 64 = 8², so √50 is just over 7.</p>",
        [("Work out 3⁴.", ["3 × 3 × 3 × 3 = 81."], "81"),
         ("Work out √144 + 2³.", ["√144 = 12 and 2³ = 8.", "12 + 8 = 20."], "20"),
         ("Work out (−6)².", ["(−6) × (−6) = 36: two negatives make a positive."], "36")],
        ["Multiplying by the power: 5² is 25, not 10.",
         "Halving for a square root: √36 is 6, not 18.",
         "Adding under the root: √9 + √16 = 3 + 4 = 7, but √25 = 5.",
         "Mixing up 2⁵ and 5²: 2⁵ = 32 and 5² = 25."])


def main():
    sets = [S("Squares and cubes", collect(one_sqcube, 20, R)),
            S("Square roots and cube roots", collect(one_root, 20, R)),
            S("Index notation", collect(one_index, 20, R)),
            S("Calculations with powers and roots", collect(one_mix, 20, R)),
            S("Problems", problems())]
    make(7, "powers-and-roots", 5, "N",
         "Powers and Roots: Squares, Cubes, Square Roots and Cube Roots",
         "Year 7 Powers and Roots Worksheets: Squares, Cubes, Square Roots, Cube Roots and Index Notation",
         "Powers and roots",
         "Use integer powers and associated real roots (square, cube and higher), recognise powers of 2, 3, 4, 5 and "
         "distinguish between exact representations of roots and their decimal approximations.",
         "Free Year 7 powers and roots worksheets: squares and cubes, square roots and cube roots, index notation, "
         "estimating square roots and problems with area and volume. 100 questions with answers.",
         "5² = 5 × 5 = 25, and √25 = 5. A square root undoes a square.",
         "2³ = 2 × 2 × 2 = 8, and ∛8 = 2. To estimate √50, use the squares either side: 49 and 64.",
         body(),
         [("What is the difference between 5² and 5 × 2?", "5² means 5 × 5 = 25. 5 × 2 = 10. The small 2 says how many fives to multiply."),
          ("What are the square numbers up to 225?", "1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196 and 225."),
          ("How do I estimate a square root?", "Find the two square numbers either side. √50 is between √49 = 7 and √64 = 8, and closer to 7."),
          ("Can a square number be negative?", "No. A positive or negative number squared is always positive or zero, for example (−4)² = 16.")],
         sets, R)


if __name__ == "__main__":
    main()
