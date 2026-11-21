# -*- coding: utf-8 -*-
"""
India Class 9 Maths, NCERT Chapter 10: Heron's Formula (CBSE Unit V Mensuration)
  python3 tools/gen_in_maths_c9_herons_formula.py
Semi-perimeter, the area of a triangle by Heron's formula (triangles with whole-number areas), sides from a ratio and
perimeter, equilateral and isosceles triangles, quadrilaterals split into two triangles, and problems (parks, sign
boards, walls, umbrellas, costs in rupees).
Wrong answers come from real mistakes: using the perimeter instead of the semi-perimeter, forgetting the square root,
½ × base × height with a slant side, and adding the sides instead of the areas.
"""
import random, math
from fractions import Fraction as F
from in_common import num, S, make, lesson, mix, T, QN, inr, People

R = random.Random(909010)
P = People(R)
BASE = [(3, 4, 5), (5, 5, 6), (5, 5, 8), (13, 14, 15), (9, 10, 17), (10, 13, 13), (7, 15, 20), (11, 13, 20), (13, 20, 21), (8, 15, 17), (6, 25, 29),
        (10, 17, 21), (13, 13, 24), (17, 25, 28), (20, 21, 29), (12, 35, 37), (25, 29, 36), (16, 17, 17), (3, 25, 26), (9, 12, 15), (15, 15, 18), (13, 37, 40)]


def area(a, b, c):
    s = F(a + b + c, 2)
    v = s * (s - a) * (s - b) * (s - c)
    rt = math.isqrt(int(v))
    return F(rt) if rt * rt == v else None


def R3(fmt, v):
    """v√3 with the unit"""
    v = F(v)
    return fmt % ("√3" if v == 1 else "%s√3" % num(v))


def tri(r, kmax=3):
    a, b, c = r.choice(BASE)
    k = r.choice([1, 1, 2, 3][:kmax + 1])
    return a * k, b * k, c * k


# ---------------------------------------------------------------- set 1: semi-perimeter
def one_s(r):
    a, b, c = tri(r)
    if r.random() < 0.6:
        s = F(a + b + c, 2)
        return QN("Find the semi-perimeter of a triangle with sides %d cm, %d cm and %d cm." % (a, b, c), s, [a + b + c, F(a + b + c, 3), s + 1],
                  "s = (a + b + c)/2 = %d/2 = <b>%s cm</b>." % (a + b + c, num(s)), unit=" cm")
    s = F(a + b + c, 2)
    which = r.choice([a, b, c])
    return QN("A triangle has sides %d cm, %d cm and %d cm. Find s − a for a = %d cm." % (a, b, c, which), s - which, [a + b + c - which, which - s if which > s else s + which, s],
              "s = %s, so s − a = %s − %d = <b>%s cm</b>." % (num(s), num(s), which, num(s - which)), unit=" cm")


# ---------------------------------------------------------------- set 2: area by Heron's formula
def one_area(r):
    a, b, c = tri(r)
    A = area(a, b, c)
    s = F(a + b + c, 2)
    return QN("Find the area of a triangle with sides %d cm, %d cm and %d cm." % (a, b, c), A,
              [s * (s - a) * (s - b) * (s - c), F(a * b, 2), A * 2],
              "s = %s. Area = √[s(s − a)(s − b)(s − c)] = √[%s × %s × %s × %s] = <b>%s cm²</b>." % (num(s), num(s), num(s - a), num(s - b), num(s - c), num(A)), unit=" cm²")


# ---------------------------------------------------------------- set 3: special triangles and ratios
def one_spec(r):
    kind = r.choice(["ratio", "ratio", "iso", "iso", "equi"])
    if kind == "ratio":
        a, b, c = r.choice([(3, 4, 5), (5, 12, 13), (13, 14, 15), (5, 5, 6), (8, 15, 17), (9, 10, 17), (12, 17, 25)])
        k = r.choice([2, 3, 4, 5, 10])
        Pm = (a + b + c) * k
        A = area(a * k, b * k, c * k)
        if A is None:
            return None
        return QN("The sides of a triangle are in the ratio %d : %d : %d and its perimeter is %d cm. Find its area." % (a, b, c, Pm), A, [A / k, A / 2, F(a * b * k * k, 1)],
                  "The sides are %d, %d and %d cm (×%d). s = %d. Area = √[s(s − a)(s − b)(s − c)] = <b>%s cm²</b>." % (a * k, b * k, c * k, k, Pm // 2, num(A)), unit=" cm²")
    if kind == "iso":
        a, b = r.choice([(5, 6), (5, 8), (13, 10), (13, 24), (17, 16), (15, 18), (10, 12), (25, 14), (25, 48), (26, 20)])
        A = area(a, a, b)
        if A is None:
            return None
        return QN("An isosceles triangle has equal sides of %d cm and a base of %d cm. Find its area." % (a, b), A, [F(a * b, 2), A * 2, F(a * a, 2)],
                  "s = %s. Area = √[%s × %s × %s × %s] = <b>%s cm²</b>. (Or: height = √(%d² − %d²).)" % (num(F(2 * a + b, 2)), num(F(2 * a + b, 2)), num(F(b, 2)), num(F(b, 2)), num(F(2 * a - b, 2)), num(A), a, b // 2), unit=" cm²")
    a = r.choice([2, 4, 6, 8, 10, 12, 20])
    return T("Find the area of an equilateral triangle of side %d cm, using Heron's formula." % a, R3("%s cm²", F(a * a, 4)),
             ["%s cm²" % num(F(a * a, 2)), R3("%s cm²", F(a * a, 2)), R3("%s cm²", F(3 * a, 2))],
             "s = %s, so area = √[%s × (%s)³] = (√3/4) × %d² = <b>%s</b>." % (num(F(3 * a, 2)), num(F(3 * a, 2)), num(F(a, 2)), a, R3("%s cm²", F(a * a, 4))))


# ---------------------------------------------------------------- set 4: quadrilaterals
def one_quad(r):
    kind = r.choice(["diag", "diag", "right"])
    if kind == "diag":
        for _ in range(50):
            t1 = tri(r, 2)
            t2 = tri(r, 2)
            common = set(t1) & set(t2)
            if common:
                break
        else:
            return None
        d = max(common)
        o1 = [x for x in t1]
        o1.remove(d)
        o2 = [x for x in t2]
        o2.remove(d)
        A1, A2 = area(*t1), area(*t2)
        return QN("A quadrilateral ABCD has AB = %d m, BC = %d m, CD = %d m, DA = %d m and diagonal AC = %d m. Find its area." % (o1[0], o1[1], o2[0], o2[1], d), A1 + A2,
                  [A1, A2 + A1 / 2, (A1 + A2) * 2], "The diagonal splits it into triangles with sides %d, %d, %d and %d, %d, %d. Areas %s + %s = <b>%s m²</b>." % (
                      o1[0], o1[1], d, o2[0], o2[1], d, num(A1), num(A2), num(A1 + A2)), unit=" m²")
    a, b, c = r.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17)])
    others = [t for t in BASE if c in t and t != (a, b, c)]
    if not others:
        return None
    t2 = r.choice(others)
    rest = list(t2)
    rest.remove(c)
    A1 = F(a * b, 2)
    A2 = area(*t2)
    return QN("Quadrilateral ABCD has ∠B = 90°, AB = %d cm, BC = %d cm, CD = %d cm and DA = %d cm. Find its area." % (a, b, rest[0], rest[1]), A1 + A2, [A1, A2, F(a * b, 1) + A2],
              "AC = √(%d² + %d²) = %d cm. Area = ½ × %d × %d + area of the triangle with sides %d, %d, %d = %s + %s = <b>%s cm²</b>." % (a, b, c, a, b, c, rest[0], rest[1], num(A1), num(A2), num(A1 + A2)), unit=" cm²")


# ---------------------------------------------------------------- set 5: problems
def one_prob(r):
    kind = r.choice(["park", "board", "wall", "umbrella", "field"])
    name, he, his = P.next()
    if kind == "park":
        a, b, c = tri(r, 3)
        rate = r.choice([5, 8, 10, 20, 25])
        A = area(a, b, c)
        return T("A triangular park has sides %d m, %d m and %d m. Grass is planted at %s per m². Find the cost." % (a, b, c, inr(rate)), inr(A * rate),
                 [inr(A), inr((a + b + c) * rate), inr(A * rate * 2)], "Area = %s m² (Heron's formula). Cost = %s × %d = <b>%s</b>." % (num(A), num(A), rate, inr(A * rate)))
    if kind == "board":
        a = r.choice([2, 4, 6, 8])
        return T("A traffic signal board is an equilateral triangle with side %d m. Find its area." % a, R3("%s m²", F(a * a, 4)),
                 ["%s m²" % num(F(a * a, 2)), R3("%s m²", F(3 * a, 2)), R3("%s m²", F(a * a, 2))],
                 "Using Heron's formula with s = %s: area = (√3/4) × %d² = <b>%s</b>." % (num(F(3 * a, 2)), a, R3("%s m²", F(a * a, 4))))
    if kind == "wall":
        a, b, c = r.choice([(122, 22, 120), (11, 60, 61), (13, 84, 85), (20, 99, 101)])
        rate = r.choice([5000, 6000, 8000])
        A = area(a, b, c)
        if A is None:
            return None
        return T("The triangular side wall of a flyover has sides %d m, %d m and %d m. Advertisements on it earn %s per m² per year. How much is earned in a year?" % (a, b, c, inr(rate)), inr(A * rate),
                 [inr(A * rate * 2), inr((a + b + c) * rate), inr(A * rate / 12)], "Area = %s m². Earnings = %s × %s = <b>%s</b>." % (num(A), num(A), num(rate), inr(A * rate)))
    if kind == "umbrella":
        n = r.choice([8, 10, 12])
        a, b = r.choice([(50, 20), (13, 10), (25, 14)])
        A = area(a, a, b)
        if A is None:
            return None
        return T("An umbrella is made of %d triangular pieces, each with sides %d cm, %d cm and %d cm. How much cloth is used?" % (n, a, a, b), "%s cm²" % num(A * n),
                 ["%s cm²" % num(A), "%s cm²" % num(F(a * b, 2) * n), "%s cm²" % num(A * n * 2)], "One piece = %s cm². %d pieces = <b>%s cm²</b>." % (num(A), n, num(A * n)))
    a, b, c = tri(r, 2)
    A = area(a, b, c)
    h = r.choice([a, b, c])
    return T("A triangular field has sides %d m, %d m and %d m. Find the length of the altitude to the side of %d m." % (a, b, c, h), "%s m" % num(2 * A / h),
             ["%s m" % num(A / h), "%s m" % num(A), "%s m" % num(2 * A / (a + b + c))], "Area by Heron = %s m². Altitude = 2 × area ÷ base = <b>%s m</b>." % (num(A), num(2 * A / h)))


def main():
    seen = set()
    sets = [
        S("Semi-perimeter", mix(R, [(one_s, 20)], seen)),
        S("Area by Heron's formula", mix(R, [(one_area, 20)], seen)),
        S("Ratios, isosceles and equilateral triangles", mix(R, [(one_spec, 20)], seen)),
        S("Areas of quadrilaterals", mix(R, [(one_quad, 20)], seen)),
        S("Word problems", mix(R, [(one_prob, 20)], seen)),
    ]
    body = lesson(
        "<p><b>Heron's formula</b> gives the area of a triangle from its three sides a, b, c: Area = √[s(s − a)(s − b)(s − c)], where s = (a + b + c)/2 is the <b>semi-perimeter</b>.</p>"
        "<p>It is useful when the height is not known. A quadrilateral can be split by a diagonal into two triangles; add their areas.</p>",
        [("Find the area of a triangle with sides 13 cm, 14 cm and 15 cm.", ["s = 21", "√(21 × 8 × 7 × 6) = √7056"], "84 cm²"),
         ("Find the area of an equilateral triangle of side 10 cm.", ["s = 15", "√(15 × 5 × 5 × 5)"], "25√3 cm²")],
        ["Using the perimeter instead of the semi-perimeter s.",
         "Forgetting the square root at the end.",
         "Using ½ × base × slant side as if the slant side were the height."])
    faq = [
        ("What is Heron's formula?", "The area of a triangle with sides a, b, c is √[s(s − a)(s − b)(s − c)], where s = (a + b + c)/2."),
        ("When should I use Heron's formula?", "When you know all three sides of a triangle but not its height."),
        ("What is the semi-perimeter?", "Half of the perimeter: s = (a + b + c)/2."),
        ("How do I find the area of a quadrilateral using Heron's formula?", "Draw a diagonal to split it into two triangles, find each area with Heron's formula, and add them."),
    ]
    make(9, "herons-formula", 10, "VI", 10, "Heron's Formula: Area of a Triangle", "Heron's formula",
         "Area of a triangle using Heron's formula (without proof) (summary of the CBSE syllabus)",
         "Class 9 Heron's Formula worksheet (NCERT Chapter 10): semi-perimeter, area of a triangle from three sides, isosceles and equilateral triangles, quadrilaterals and word problems. 100 questions with answers.",
         "Area = √[s(s − a)(s − b)(s − c)]", "s = (a + b + c)/2 is the semi-perimeter.",
         body, faq, sets, R)


if __name__ == "__main__":
    main()
