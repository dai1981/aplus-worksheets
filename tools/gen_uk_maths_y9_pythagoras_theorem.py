# -*- coding: utf-8 -*-
"""
UK Year 9 Maths: Pythagoras' Theorem (KS3 Geometry and measures)
  python3 tools/gen_uk_maths_y9_pythagoras_theorem.py
Finding the hypotenuse, finding a shorter side, answers to 1 decimal place, testing for a right angle,
the distance between two points, and real-life problems.
Wrong answers come from real mistakes: adding the sides without squaring, forgetting the square root,
adding instead of subtracting when finding a shorter side, and using a shorter side as the hypotenuse.
"""
import math
import random
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F
from uk_ks3 import num, mcq, B, S, make, lesson, collect, QN, T, svg_wrap, line, text, fig, INK, RED, GREEN

R = random.Random(90101)
TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15), (12, 16, 20), (20, 21, 29), (9, 40, 41), (10, 24, 26), (15, 20, 25), (12, 35, 37)]


def d1(x):
    return "{:,.1f}".format(float(Decimal(str(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)))


def rtri(a_lab, b_lab, c_lab, a, b):
    """Right angle at bottom-left. a = vertical leg, b = horizontal leg (for proportions)."""
    sc = min(200.0 / b, 120.0 / a)
    W, H = b * sc, a * sc
    x0, y0 = 60, 30 + H
    s = ["<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f Z' fill='#eef6f0' stroke='%s' stroke-width='2.5'/>" % (x0, y0, x0 + W, y0, x0, y0 - H, INK),
         "<path d='M%.1f %.1f l14 0 l0 14' fill='none' stroke='%s' stroke-width='1.8' transform='translate(0,0)'/>" % (x0, y0 - 14, GREEN),
         text(x0 - 8, y0 - H / 2 + 5, a_lab, 15, anchor="end", col=RED if a_lab == "x" else INK, italic=a_lab == "x"),
         text(x0 + W / 2, y0 + 22, b_lab, 15, col=RED if b_lab == "x" else INK, italic=b_lab == "x"),
         text(x0 + W / 2 + 14, y0 - H / 2 - 8, c_lab, 15, anchor="start", col=RED if c_lab == "x" else INK, italic=c_lab == "x")]
    return svg_wrap(int(x0 + W + 90), int(y0 + 34), "".join(s), "right-angled triangle, not drawn accurately")


# ------------------------------------------------------------ set 1: hypotenuse, whole numbers
def one_hyp(r):
    a, b, c = r.choice(TRIPLES)
    k = r.choice([1, 1, 2]) if c < 20 else 1
    a, b, c = a * k, b * k, c * k
    if r.random() < 0.5:
        a, b = b, a
    q = "Find the length of the hypotenuse %s.%s" % (B("<i>x</i>"), fig(rtri("%d cm" % a, "%d cm" % b, "x", a, b)))
    e = "<i>x</i>² = %d² + %d² = %d + %d = %d. <i>x</i> = √%d = <b>%d cm</b>." % (a, b, a * a, b * b, c * c, c * c, c)
    return QN(q, c, [a + b, c * c, int(math.sqrt(abs(b * b - a * a))) if int(math.sqrt(abs(b * b - a * a))) ** 2 == abs(b * b - a * a) else max(a, b) + 1], e, unit=" cm")


# ------------------------------------------------------------ set 2: hypotenuse, 1 decimal place
def one_hyp_dp(r):
    a, b = r.randint(3, 15), r.randint(3, 15)
    c2 = a * a + b * b
    if int(math.isqrt(c2)) ** 2 == c2 or a == b:
        return None
    c = math.sqrt(c2)
    q = "Find %s. Give your answer to 1 decimal place.%s" % (B("<i>x</i>"), fig(rtri("%d cm" % a, "%d cm" % b, "x", a, b)))
    e = "<i>x</i>² = %d² + %d² = %d. <i>x</i> = √%d = %s… = <b>%s cm</b>." % (a, b, c2, c2, "{:.3f}".format(c), d1(c))
    right = d1(c) + " cm"
    wr = [d1(a + b) + " cm", "%d cm" % c2, d1(math.sqrt(abs(a * a - b * b))) + " cm", d1(c + 1) + " cm"]
    return T(q, right, [w for w in wr if w != right][:3], e)


# ------------------------------------------------------------ set 3: shorter side
def one_short(r):
    if r.random() < 0.5:
        a, b, c = r.choice(TRIPLES)
        if r.random() < 0.5:
            a, b = b, a
        q = "Find the length %s.%s" % (B("<i>x</i>"), fig(rtri("x", "%d cm" % b, "%d cm" % c, a, b)))
        e = "The hypotenuse is %d cm, so subtract: <i>x</i>² = %d² − %d² = %d − %d = %d. <i>x</i> = <b>%d cm</b>." % (c, c, b, c * c, b * b, a * a, a)
        add = math.sqrt(c * c + b * b)
        return QN(q, a, [c - b, a * a, F(str(round(add, 1)))], e, unit=" cm")
    b = r.randint(3, 12)
    c = r.randint(b + 2, 20)
    a2 = c * c - b * b
    if int(math.isqrt(a2)) ** 2 == a2:
        return None
    a = math.sqrt(a2)
    q = "Find %s. Give your answer to 1 decimal place.%s" % (B("<i>x</i>"), fig(rtri("x", "%d cm" % b, "%d cm" % c, a, b)))
    e = "<i>x</i>² = %d² − %d² = %d. <i>x</i> = √%d = <b>%s cm</b>." % (c, b, a2, a2, d1(a))
    right = d1(a) + " cm"
    wr = [d1(math.sqrt(c * c + b * b)) + " cm", "%d cm" % (c - b), "%d cm" % a2]
    return T(q, right, [w for w in wr if w != right], e)


# ------------------------------------------------------------ set 4: right angle test, distance between points
def one_test(r):
    if r.random() < 0.5:
        if r.random() < 0.5:
            a, b, c = r.choice(TRIPLES)
            yes = True
        else:
            a, b, c = r.choice(TRIPLES)
            c += r.choice([-1, 1])
            yes = False
        q = "A triangle has sides %d cm, %d cm and %d cm. Is it right-angled?" % (a, b, c)
        right = "Yes, because %d² + %d² = %d²" % (a, b, c) if yes else "No, because %d² + %d² ≠ %d²" % (a, b, c)
        wr = ["No, because %d² + %d² ≠ %d²" % (a, b, c) if yes else "Yes, because %d² + %d² = %d²" % (a, b, c),
              "Yes, because %d + %d &gt; %d" % (a, b, c), "No, because %d is not a square number" % c]
        e = "%d² + %d² = %d and %d² = %d. %s" % (a, b, a * a + b * b, c, c * c, "<b>They are equal, so it is right-angled.</b>" if yes else "<b>They are not equal, so it is not right-angled.</b>")
        return T(q, right, wr, e)
    x1, y1 = r.randint(-5, 5), r.randint(-5, 5)
    a, b, c = r.choice(TRIPLES[:6] + [(3, 4, 5), (6, 8, 10)])
    sx, sy = r.choice([1, -1]), r.choice([1, -1])
    if r.random() < 0.5:
        a, b = b, a
    x2, y2 = x1 + sx * a, y1 + sy * b
    q = "Find the distance between the points (%s, %s) and (%s, %s)." % (num(x1), num(y1), num(x2), num(y2))
    e = "Across %d, up/down %d. Distance = √(%d² + %d²) = √%d = <b>%d units</b>." % (a, b, a, b, c * c, c)
    return QN(q, c, [a + b, c * c, abs((x2 + y2) - (x1 + y1)) if abs((x2 + y2) - (x1 + y1)) != c else c + 2], e, unit=" units")


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    data = [
        ("A ladder 5 m long leans against a wall. Its foot is 1.4 m from the wall. How high up the wall does it reach?", "4.8 m", ["5.2 m", "3.6 m", "6.4 m"], "<i>h</i>² = 5² − 1.4² = 25 − 1.96 = 23.04. <i>h</i> = <b>4.8 m</b>."),
        ("A rectangle is 8 cm by 6 cm. How long is its diagonal?", "10 cm", ["14 cm", "100 cm", "5.3 cm"], "√(8² + 6²) = √100 = <b>10 cm</b>."),
        ("A TV screen is 48 inches wide and 27 inches high. What is the diagonal, to the nearest inch?", "55 inches", ["75 inches", "40 inches", "60 inches"], "√(48² + 27²) = √3,033 = 55.07… ≈ <b>55 inches</b>."),
        ("A ship sails 9 km north and then 12 km east. How far is it from its start?", "15 km", ["21 km", "7.9 km", "225 km"], "√(9² + 12²) = √225 = <b>15 km</b>."),
        ("An isosceles triangle has two sides of 13 cm and a base of 10 cm. What is its height?", "12 cm", ["13 cm", "8 cm", "16.4 cm"], "Half the base is 5 cm. √(13² − 5²) = √144 = <b>12 cm</b>."),
        ("A square has a diagonal of 10 cm. Which is the side length, to 1 decimal place?", "7.1 cm", ["5 cm", "14.1 cm", "10 cm"], "<i>s</i>² + <i>s</i>² = 100, so <i>s</i>² = 50 and <i>s</i> = <b>7.1 cm</b>."),
        ("In a right-angled triangle, which side is the hypotenuse?", "The longest side, opposite the right angle", ["The shortest side", "The side next to the right angle", "The base"],
         "The hypotenuse is <b>the longest side, opposite the right angle</b>."),
        ("Which set of lengths could be the sides of a right-angled triangle?", "7, 24, 25", ["5, 6, 7", "4, 5, 6", "6, 7, 10"], "7² + 24² = 49 + 576 = 625 = 25². So <b>7, 24, 25</b>."),
        ("A kite string is 50 m long. The kite is directly above a point 30 m from the person. How high is the kite?", "40 m", ["58.3 m", "20 m", "80 m"], "√(50² − 30²) = √1,600 = <b>40 m</b>."),
        ("A cuboid box is 12 cm by 9 cm at the base. How long is the diagonal of the base?", "15 cm", ["21 cm", "7.9 cm", "225 cm"], "√(12² + 9²) = √225 = <b>15 cm</b>."),
        ("A ramp rises 1 m over a horizontal distance of 6 m. How long is the ramp, to 1 decimal place?", "6.1 m", ["7 m", "5.9 m", "37 m"], "√(6² + 1²) = √37 = 6.08… ≈ <b>6.1 m</b>."),
        ("Leo says the hypotenuse of a triangle with shorter sides 3 cm and 4 cm is 7 cm. What mistake has he made?", "He added the sides without squaring", ["He forgot to halve", "He used the wrong formula for area", "There is no mistake"],
         "He needs √(3² + 4²) = 5 cm. <b>He added the sides without squaring.</b>"),
        ("A football pitch is 100 m by 64 m. How far is it from corner to opposite corner, to the nearest metre?", "119 m", ["164 m", "77 m", "14,096 m"], "√(100² + 64²) = √14,096 = 118.7… ≈ <b>119 m</b>."),
        ("What is the distance between (1, 2) and (4, 6)?", "5 units", ["7 units", "25 units", "3.6 units"], "Across 3, up 4: √(9 + 16) = <b>5 units</b>."),
        ("An equilateral triangle has sides of 6 cm. What is its height, to 1 decimal place?", "5.2 cm", ["6.7 cm", "3 cm", "4.2 cm"], "√(6² − 3²) = √27 = 5.196… ≈ <b>5.2 cm</b>."),
        ("A 13 m wire runs from the top of a 12 m pole to the ground. How far from the pole does it reach the ground?", "5 m", ["1 m", "17.7 m", "25 m"], "√(13² − 12²) = √25 = <b>5 m</b>."),
        ("The two shorter sides of a right-angled triangle are equal. The hypotenuse is √50 cm. How long is each shorter side?", "5 cm", ["25 cm", "7.1 cm", "√25 cm … no, 10 cm"], "2<i>s</i>² = 50, so <i>s</i>² = 25 and <i>s</i> = <b>5 cm</b>."),
        ("Pythagoras' theorem says that in a right-angled triangle…", "<i>a</i>² + <i>b</i>² = <i>c</i>², where <i>c</i> is the hypotenuse", ["<i>a</i> + <i>b</i> = <i>c</i>", "<i>a</i>² × <i>b</i>² = <i>c</i>²", "<i>a</i>² + <i>b</i>² = <i>c</i>, where <i>c</i> is the hypotenuse"],
         "The squares on the two shorter sides add up to the square on the hypotenuse: <b><i>a</i>² + <i>b</i>² = <i>c</i>²</b>."),
        ("A rectangular gate is 1.2 m wide and 1.6 m high. How long is the diagonal brace?", "2 m", ["2.8 m", "1.4 m", "4 m"], "√(1.2² + 1.6²) = √4 = <b>2 m</b>."),
        ("A cyclist rides 5 km east and 5 km south. How far is she from her start, to 1 decimal place?", "7.1 km", ["10 km", "5 km", "50 km"], "√(25 + 25) = √50 = 7.07… ≈ <b>7.1 km</b>."),
    ]
    for q, a, w, e in data:
        w = [x if "… no" not in x else "10 cm" for x in w]
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p>In a right-angled triangle, the longest side (opposite the right angle) is the <b>hypotenuse</b>, <i>c</i>. "
        "<b>Pythagoras' theorem</b>: <i>a</i>² + <i>b</i>² = <i>c</i>².</p>"
        "<ul><li>To find the hypotenuse: square, <b>add</b>, square root.</li><li>To find a shorter side: square, <b>subtract</b>, square root.</li></ul>"
        + fig(rtri("6 cm", "8 cm", "c", 6, 8)),
        [("Find <i>c</i> in the triangle above.", ["<i>c</i>² = 6² + 8² = 36 + 64 = 100.", "<i>c</i> = √100."], "10 cm"),
         ("The hypotenuse is 13 cm and one side is 5 cm. Find the other side.", ["13² − 5² = 169 − 25 = 144.", "√144 = 12."], "12 cm")],
        ["Adding the sides without squaring: 3, 4 gives 5, not 7.",
         "Forgetting the square root at the end.",
         "Adding when you need a shorter side. Subtract from the hypotenuse squared.",
         "Using a shorter side as the hypotenuse. The hypotenuse is always opposite the right angle."])


def main():
    sets = [S("Finding the hypotenuse", collect(one_hyp, 20, R)),
            S("Hypotenuse to 1 decimal place", collect(one_hyp_dp, 20, R)),
            S("Finding a shorter side", collect(one_short, 20, R)),
            S("Right angles and distances between points", collect(one_test, 20, R)),
            S("Problems", problems())]
    make(9, "pythagoras-theorem", 1, "G",
         "Pythagoras' Theorem: Hypotenuse, Shorter Sides and Problems",
         "Year 9 Pythagoras' Theorem Worksheets: Find the Hypotenuse, Shorter Sides, Distances and Word Problems",
         "Pythagoras' theorem",
         "Use Pythagoras' Theorem and trigonometric ratios in similar triangles to solve problems involving right-angled triangles.",
         "Free Year 9 Pythagoras' theorem worksheets with diagrams: find the hypotenuse, find a shorter side, answers to "
         "1 decimal place, test for a right angle, distance between points and real-life problems. 100 questions with answers.",
         "a² + b² = c², where c is the hypotenuse (the longest side, opposite the right angle).",
         "Hypotenuse: square, add, square root. Shorter side: square, subtract, square root.",
         body(),
         [("What is Pythagoras' theorem?", "In a right-angled triangle, a² + b² = c², where c is the hypotenuse and a and b are the two shorter sides."),
          ("How do I find a shorter side?", "Square the hypotenuse, subtract the square of the known side, then take the square root."),
          ("How do I know which side is the hypotenuse?", "It is the longest side, opposite the right angle."),
          ("How do I check if a triangle is right-angled?", "Square the two shorter sides and add. If the total equals the square of the longest side, it is right-angled.")],
         sets, R)


if __name__ == "__main__":
    main()
