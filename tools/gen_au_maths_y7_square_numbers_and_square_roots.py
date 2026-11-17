# -*- coding: utf-8 -*-
"""
AU Year 7 Maths: Square numbers and square roots (Australian Curriculum v9.0: AC9M7N01)
  python3 tools/gen_au_maths_y7_square_numbers_and_square_roots.py
Perfect squares, square roots of perfect squares, squares of decimals and negatives, estimating square roots
between whole numbers, calculations with squares and roots, and problems with square areas.
Wrong answers come from real mistakes: 6² = 12 (multiplying by 2), √36 = 18 (halving), √9 + √16 = √25,
and (−5)² = −25.
"""
import math
import random
from fractions import Fraction as F
from au_hs import num, B, S, make, lesson, collect, QN, T, MINUS, aud, People

R = random.Random(70101)


def sq(b):
    bs = num(b) if F(b) >= 0 else "(%s)" % num(b)
    return "%s<sup>2</sup>" % bs


# ------------------------------------------------------------ set 1: square numbers
def one_square(r):
    kind = r.choice(["w", "w", "w", "big", "dec", "neg"])
    if kind == "w":
        b = r.randint(2, 15)
        v = b * b
        return QN("Work out %s." % B(sq(b)), v, [2 * b, b + 2, v + b],
                  "%s means %d × %d = <b>%d</b>. The small 2 does not mean × 2." % (sq(b), b, b, v))
    if kind == "big":
        b = r.choice([20, 30, 40, 50, 60, 70, 80, 90, 25, 16, 18, 19, 21])
        v = b * b
        return QN("Work out %s." % B(sq(b)), v, [2 * b, v // 10 if v % 10 == 0 else v + 10, v + b],
                  "%d × %d = <b>%s</b>." % (b, b, num(v)))
    if kind == "dec":
        b = F(r.randint(2, 12), 10)
        v = b * b
        return QN("Work out %s." % B(sq(b)), v, [b * 2, v * 10, v * 100],
                  "%s × %s = <b>%s</b>. One decimal place × one decimal place gives two decimal places." % (num(b), num(b), num(v)))
    b = -r.randint(2, 12)
    v = b * b
    return QN("Work out %s." % B(sq(b)), v, [-v, 2 * b, -2 * b],
              "%s × %s = <b>%d</b>. A negative times a negative is positive." % (num(b), num(b), v))


# ------------------------------------------------------------ set 2: square roots of perfect squares
def one_root(r):
    kind = r.choice(["w", "w", "w", "big", "dec", "frac"])
    if kind == "w":
        b = r.randint(2, 15)
        n = b * b
        return QN("Work out %s." % B("√%d" % n), b, [n // 2, b + 1, n - b if n - b != b else b + 2],
                  "%d × %d = %d, so √%d = <b>%d</b>. A square root is not half the number." % (b, b, n, n, b))
    if kind == "big":
        b = r.choice([20, 30, 40, 50, 60, 70, 80, 90, 100])
        n = b * b
        return QN("Work out %s." % B("√%s" % num(n)), b, [n // 2, b * 10, b // 10],
                  "%d × %d = %s, so √%s = <b>%d</b>." % (b, b, num(n), num(n), b))
    if kind == "dec":
        b = F(r.randint(2, 12), 10)
        n = b * b
        return QN("Work out %s." % B("√%s" % num(n)), b, [n / 2, b / 10, b * 10],
                  "%s × %s = %s, so √%s = <b>%s</b>." % (num(b), num(b), num(n), num(n), num(b)))
    a, b = r.randint(1, 9), r.randint(2, 12)
    if math.gcd(a, b) > 1 or a >= b:
        return None
    q = "Work out %s." % B("√<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a * a, b * b))
    fr = lambda x, y: "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (x, y)
    right = fr(a, b)
    return T(q, right, [fr(a * a // 2 if a * a % 2 == 0 else a * a, b * b // 2 if b * b % 2 == 0 else b), fr(a, b * b), fr(a * a, b)],
             "√%d = %d and √%d = %d, so the answer is <b>%s</b>." % (a * a, a, b * b, b, right))


# ------------------------------------------------------------ set 3: estimating square roots
def one_est(r):
    kind = r.choice(["between", "between", "closest", "is_square"])
    if kind == "between":
        n = r.randint(5, 220)
        lo = math.isqrt(n)
        if lo * lo == n:
            return None
        right = "%d and %d" % (lo, lo + 1)
        wr = ["%d and %d" % (lo - 1, lo), "%d and %d" % (lo + 1, lo + 2), "%d and %d" % (n // 2 - 1, n // 2)]
        if right in wr or n // 2 - 1 < 1:
            return None
        return T("Between which two whole numbers is %s?" % B("√%d" % n), right, wr,
                 "%d² = %d and %d² = %d. %d is between them, so √%d is between <b>%s</b>." % (lo, lo * lo, lo + 1, (lo + 1) ** 2, n, n, right))
    if kind == "closest":
        n = r.randint(10, 200)
        lo = math.isqrt(n)
        if lo * lo == n or n - lo * lo == (lo + 1) ** 2 - n:
            return None
        near = lo if n - lo * lo < (lo + 1) ** 2 - n else lo + 1
        far = lo + 1 if near == lo else lo
        return QN("Which whole number is %s closest to?" % B("√%d" % n), near, [far, n // 2, near + 2 if far < near else near - 2],
                  "%d is between %d² = %d and %d² = %d, and closer to %d. So √%d is closest to <b>%d</b>." % (
                      n, lo, lo * lo, lo + 1, (lo + 1) ** 2, near * near, n, near))
    sqs = [k * k for k in range(4, 16)]
    right = r.choice(sqs)
    non = r.sample([x for x in range(15, 230) if x not in sqs and x % 10 != 0], 3)
    return T("Which of these is a perfect square?", str(right), [str(x) for x in non],
             "%d = %d × %d, so <b>%d</b> is a perfect square." % (right, math.isqrt(right), math.isqrt(right), right))


# ------------------------------------------------------------ set 4: calculations with squares and roots
def one_calc(r):
    a, b = r.randint(2, 10), r.randint(2, 10)
    form = r.randint(0, 4)
    if form == 0:
        v = a * a + b * b
        return QN("Work out %s." % B("%s + %s" % (sq(a), sq(b))), v, [(a + b) ** 2, 2 * a + 2 * b, a * a + b],
                  "%d + %d = <b>%d</b>. Square each number first." % (a * a, b * b, v))
    if form == 1:
        if a == b:
            return None
        v = (a + b) ** 2
        return QN("Work out %s." % B("(%d + %d)<sup>2</sup>" % (a, b)), v, [a * a + b * b, 2 * (a + b), (a + b) * 2 + 2],
                  "Brackets first: %d + %d = %d, then %d² = <b>%d</b>." % (a, b, a + b, a + b, v))
    if form == 2:
        n, m = a * a, b * b
        v = a + b
        sm = n + m
        w1 = math.isqrt(sm) if math.isqrt(sm) ** 2 == sm else sm
        return QN("Work out %s." % B("√%d + √%d" % (n, m)), v, [w1, sm // 2, v + 1],
                  "√%d = %d and √%d = %d, so the answer is <b>%d</b>. Do not add the numbers under the roots first." % (n, a, m, b, v))
    if form == 3:
        n = a * a
        v = b * b - a
        if v <= 0:
            return None
        return QN("Work out %s." % B("%s %s √%d" % (sq(b), MINUS, n)), v, [b * b - n, 2 * b - a, b * b - n // 2],
                  "%s = %d and √%d = %d, so %d − %d = <b>%d</b>." % (sq(b), b * b, n, a, b * b, a, v))
    c = r.randint(2, 6)
    n = a * a
    v = c * a
    return QN("Work out %s." % B("%d × √%d" % (c, n)), v, [c * n // 2 if n % 2 == 0 else c * n, c + a, c * n],
              "√%d = %d, then %d × %d = <b>%d</b>." % (n, a, c, a, v))


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    P = People(R)
    for area, what in [(64, "garden bed"), (144, "vegetable patch"), (81, "chessboard"), (225, "courtyard"), (169, "tile")]:
        s = math.isqrt(area)
        u = "m" if what in ("vegetable patch", "courtyard", "garden bed") else "cm"
        its.append(QN("A square %s has an area of %d %s². How long is each side?" % (what, area, u), s, [area // 4, area // 2, s * 2],
                      "Side × side = %d, so each side is √%d = <b>%d %s</b>." % (area, area, s, u), unit=" " + u))
    for side, u in [(7, "m"), (12, "cm"), (2.5, "m")]:
        a = F(str(side)) ** 2
        its.append(QN("A square has sides of %s %s. What is its area?" % (num(F(str(side))), u), a, [F(str(side)) * 4, F(str(side)) * 2, a / 2],
                      "%s × %s = <b>%s %s²</b>. (4 × side gives the perimeter, not the area.)" % (num(F(str(side))), num(F(str(side))), num(a), u), unit=" %s²" % u))
    for per in [36, 48, 28]:
        s = per // 4
        its.append(QN("A square has a perimeter of %d cm. What is its area?" % per, s * s, [per * per // 16 * 2, per, s * 4 + 4 if s * 4 + 4 != s * s else s * s + 4],
                      "Each side is %d ÷ 4 = %d cm, so the area is %d × %d = <b>%d cm²</b>." % (per, s, s, s, s * s), unit=" cm²"))
    data = [
        ("Which number has a square root of 13?", "169", ["26", "39", "156"], "13² = 13 × 13 = <b>169</b>."),
        ("Charlotte says √49 = 24.5. What is the correct answer?", "7", ["24.5", "14", "98"], "7 × 7 = 49, so √49 = <b>7</b>. Charlotte halved the number."),
        ("What is the next square number after 100?", "121", ["110", "102", "200"], "11² = <b>121</b>."),
        ("How many perfect squares are between 1 and 100, not counting 1 and 100?", "8", ["9", "10", "50"],
         "4, 9, 16, 25, 36, 49, 64 and 81: <b>8</b> square numbers."),
        ("A square room has an area of 30 m². Between which two whole numbers is the side length?", "5 m and 6 m", ["4 m and 5 m", "6 m and 7 m", "15 m and 16 m"],
         "5² = 25 and 6² = 36, so the side is between <b>5 m and 6 m</b>."),
        ("Which is larger: √50 or 7?", "√50", ["7", "They are equal", "You cannot tell without a calculator"],
         "7 = √49, and 50 is more than 49, so <b>√50</b> is larger."),
        ("A square tile is 30 cm long. How many square centimetres does it cover?", "900 cm²", ["120 cm²", "60 cm²", "90 cm²"],
         "30 × 30 = <b>900 cm²</b>."),
        ("Mia arranges 196 chairs in a square. How many chairs are in each row?", "14", ["49", "98", "16"],
         "√196 = 14, because 14 × 14 = 196. <b>14</b> chairs in each row."),
        ("What is the difference between 9² and 8²?", "17", ["1", "2", "64"], "81 − 64 = <b>17</b>."),
    ]
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p>A <b>square number</b> (perfect square) comes from multiplying a whole number by itself: 6² = 6 × 6 = 36.</p>"
        "<p>A <b>square root</b> undoes squaring: √36 = 6, because 6 × 6 = 36. "
        "To estimate a square root, find the perfect squares either side: √50 is between √49 = 7 and √64 = 8, and very close to 7.</p>",
        [("Work out 12².", ["12 × 12."], "144"),
         ("Work out √81 + √16.", ["√81 = 9 and √16 = 4.", "9 + 4."], "13"),
         ("Between which two whole numbers is √70?", ["8² = 64 and 9² = 81."], "8 and 9")],
        ["Multiplying by 2: 6² is 36, not 12.",
         "Halving for a square root: √36 is 6, not 18.",
         "Adding under the root: √9 + √16 = 3 + 4 = 7, not √25 = 5.",
         "Writing (−5)² = −25. A negative times a negative is positive, so (−5)² = 25."])


def main():
    sets = [S("Square numbers", collect(one_square, 20, R)),
            S("Square roots of perfect squares", collect(one_root, 20, R)),
            S("Estimating square roots", collect(one_est, 20, R)),
            S("Calculations with squares and roots", collect(one_calc, 20, R)),
            S("Square and square root problems", problems())]
    make(7, "square-numbers-and-square-roots", 1, "AC9M7N01",
         "Square Numbers and Square Roots",
         "Year 7 Square Numbers and Square Roots Worksheets: Perfect Squares and Estimating Roots (Free, Answer Key)",
         "Squares and square roots",
         "describe the relationship between perfect square numbers and square roots, and use squares of numbers and square "
         "roots of perfect square numbers to solve problems",
         "Free Year 7 maths worksheets on square numbers and square roots for the Australian Curriculum (AC9M7N01): perfect "
         "squares, square roots, estimating roots between whole numbers and area problems. 100 questions with an answer key.",
         "6² = 6 × 6 = 36, and √36 = 6.",
         "A square root undoes a square. To estimate √50, use the perfect squares either side: 49 and 64.",
         body(),
         [("What is a perfect square?", "A number made by multiplying a whole number by itself, such as 1, 4, 9, 16, 25, 36, 49, 64, 81 and 100."),
          ("How are squares and square roots related?", "They undo each other. 7² = 49, so √49 = 7."),
          ("How do I estimate a square root?", "Find the perfect squares either side. √50 is between √49 = 7 and √64 = 8, and very close to 7."),
          ("Why is (−5)² positive?", "(−5)² = (−5) × (−5), and a negative times a negative is positive, so it is 25.")],
         sets, R)


if __name__ == "__main__":
    main()
