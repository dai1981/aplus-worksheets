# -*- coding: utf-8 -*-
"""
US Geometry: Distance and Midpoint Formulas (Common Core G-GPE.B.7, G-GPE.B.6)
  python3 tools/gen_us_math_ge_distance_and_midpoint_formulas.py
The distance formula with whole-number and radical answers, the midpoint formula, finding a missing
endpoint, partitioning a segment in a ratio, and perimeter and area of figures on the coordinate plane.
Wrong answers come from real mistakes: adding the differences instead of squaring them, forgetting the
square root, subtracting the coordinates in the midpoint formula, and using the midpoint as the endpoint.
"""
import random
from math import isqrt, gcd
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, fig, num, MINUS, People
from g8_common import grid_svg
from us_geo import RED, BLUE, GREEN

R = random.Random(92301)
TRIPLES = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (12, 16, 20), (7, 24, 25)]


def sg(n):
    n = F(n)
    return num(n) if n >= 0 else MINUS + num(-n)


def pt(x, y):
    return "(%s, %s)" % (sg(x), sg(y))


def rad(n):
    a = 1
    for k in range(isqrt(n), 1, -1):
        if n % (k * k) == 0:
            a = k
            break
    b = n // (a * a)
    if b == 1:
        return num(a)
    return ("" if a == 1 else num(a)) + "√" + num(b)


def p_(v):
    return "(%s)" % sg(v) if v < 0 else sg(v)


def dist_steps(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    return "d = √((%s %s %s)² + (%s %s %s)²) = √(%s² + %s²) = √(%d + %d) = √%d" % (
        sg(x2), MINUS, p_(x1), sg(y2), MINUS, p_(y1), p_(dx), p_(dy), dx * dx, dy * dy, dx * dx + dy * dy)


# ------------------------------------------------------------ set 1: whole-number distances
def one_dist(r):
    a, b, c = r.choice(TRIPLES)
    if r.random() < 0.5:
        a, b = b, a
    x1, y1 = r.randint(-9, 6), r.randint(-9, 6)
    x2, y2 = x1 + a * r.choice([1, -1]), y1 + b * r.choice([1, -1])
    if max(abs(x2), abs(y2)) > 20:
        return None
    q = "Find the distance between %s and %s." % (B(pt(x1, y1)), B(pt(x2, y2)))
    e = dist_steps(x1, y1, x2, y2) + " = <b>%d</b>." % c
    wr = [a + b, c * c, abs(x1 + x2) + abs(y1 + y2), c + 1]
    return T(q, num(c), [num(w) for w in dict.fromkeys(wr) if w != c][:3], e)


# ------------------------------------------------------------ set 2: radical distances
def one_rad(r):
    dx, dy = r.randint(1, 9), r.randint(1, 9)
    n = dx * dx + dy * dy
    if isqrt(n) ** 2 == n:
        return None
    x1, y1 = r.randint(-8, 5), r.randint(-8, 5)
    x2, y2 = x1 + dx * r.choice([1, -1]), y1 + dy * r.choice([1, -1])
    q = "Find the distance between %s and %s. Give an exact answer in simplest radical form." % (B(pt(x1, y1)), B(pt(x2, y2)))
    right = rad(n)
    wr = [num(dx + dy), "√" + num(dx + dy) if isqrt(dx + dy) ** 2 != dx + dy else num(n), num(n)]
    if right != "√" + num(n):
        wr.insert(0, "√" + num(n) + " ")  # placeholder never used: unsimplified is equal in value
        wr.pop(0)
    e = dist_steps(x1, y1, x2, y2) + ("" if right == "√" + num(n) else " = <b>%s</b>" % right) + "."
    if right == "√" + num(n):
        e = e[:-1] + ". %d has no perfect square factor, so the answer is <b>%s</b>." % (n, right)
    wr = [w for w in dict.fromkeys(wr) if w != right]
    if len(wr) < 3:
        wr.append("√" + num(abs(dx * dx - dy * dy)) if dx != dy else num(2 * dx))
    return T(q, right, wr[:3], e)


# ------------------------------------------------------------ set 3: midpoint formula
def one_mid(r):
    x1, y1 = r.randint(-10, 10), r.randint(-10, 10)
    x2, y2 = r.randint(-10, 10), r.randint(-10, 10)
    if x1 == x2 or y1 == y2:
        return None
    half = r.random() < 0.25
    if not half and ((x1 + x2) % 2 or (y1 + y2) % 2):
        return None
    mx, my = F(x1 + x2, 2), F(y1 + y2, 2)
    q = "Find the midpoint of the segment with endpoints %s and %s." % (B(pt(x1, y1)), B(pt(x2, y2)))
    right = pt(mx, my)
    wr = [pt(F(x2 - x1, 2), F(y2 - y1, 2)), pt(x1 + x2, y1 + y2), pt(my, mx), pt(F(x1 - x2, 2), F(y1 - y2, 2))]
    e = "Average the <i>x</i>-coordinates and the <i>y</i>-coordinates: ((%s + %s) ÷ 2, (%s + %s) ÷ 2) = <b>%s</b>." % (
        sg(x1), p_(x2), sg(y1), p_(y2), right)
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)


# ------------------------------------------------------------ set 4: missing endpoint and partitions
def one_end(r):
    if r.random() < 0.6:
        x1, y1 = r.randint(-9, 9), r.randint(-9, 9)
        mx, my = r.randint(-8, 8), r.randint(-8, 8)
        if (mx, my) == (x1, y1) or mx == x1 or my == y1:
            return None
        x2, y2 = 2 * mx - x1, 2 * my - y1
        q = "M%s is the midpoint of %s. One endpoint is A%s. Find the other endpoint B." % (
            pt(mx, my), "<span class='ov'>AB</span>", pt(x1, y1))
        right = pt(x2, y2)
        wr = [pt(F(x1 + mx, 2), F(y1 + my, 2)), pt(mx - x1, my - y1), pt(x1 - mx, y1 - my), pt(2 * x1 - mx, 2 * y1 - my)]
        e = ("Go from A to M, then the same step again. Step: (%s, %s). B = M + step = <b>%s</b>. Or solve (%s + <i>x</i>) ÷ 2 = %s." % (
            sg(mx - x1), sg(my - y1), right, sg(x1), sg(mx)))
        return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)
    a, b = r.choice([(1, 2), (2, 1), (1, 3), (3, 1), (1, 4), (3, 2), (2, 3)])
    n = a + b
    dx, dy = n * r.randint(-3, 3), n * r.randint(-3, 3)
    if dx == 0 or dy == 0:
        return None
    x1, y1 = r.randint(-8, 4), r.randint(-8, 4)
    x2, y2 = x1 + dx, y1 + dy
    px, py = x1 + dx * a // n, y1 + dy * a // n
    q = "Find the point P on %s, from A%s to B%s, that partitions the segment in the ratio %d : %d." % (
        "<span class='ov'>AB</span>", pt(x1, y1), pt(x2, y2), a, b)
    right = pt(px, py)
    wr = [pt(x1 + dx * b // n, y1 + dy * b // n), pt(F(x1 + x2, 2), F(y1 + y2, 2)), pt(x1 + F(dx * a, b), y1 + F(dy * a, b)), pt(px + 1, py)]
    e = ("AP is %d/%d of AB. Change from A to B: (%s, %s). P = A + %d/%d of that = (%s + %s, %s + %s) = <b>%s</b>." % (
        a, n, sg(dx), sg(dy), a, n, sg(x1), p_(dx * a // n), sg(y1), p_(dy * a // n), right))
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right and "None" not in w][:3], e)


# ------------------------------------------------------------ set 5: perimeter and area on the plane
def one_poly(r):
    kind = r.choice(["rect", "tri", "right", "map", "map"])
    if kind == "rect":
        x1, y1 = r.randint(-6, 1), r.randint(-6, 1)
        w, h = r.randint(2, 7), r.randint(2, 6)
        if w == h:
            return None
        P = [(x1, y1), (x1 + w, y1), (x1 + w, y1 + h), (x1, y1 + h)]
        ask = r.choice(["perimeter", "area"])
        names = "ABCD"
        svg = grid_svg(-7, 7, points=[(x, y, n, RED) for (x, y), n in zip(P, names)], polys=[(P, "#cfe6d6", GREEN)], unit=18, label="rectangle ABCD")
        q = "Rectangle ABCD has vertices %s. Find its %s.%s" % (", ".join("%s%s" % (n, pt(*p)) for n, p in zip(names, P)), ask, fig(svg))
        ans = 2 * (w + h) if ask == "perimeter" else w * h
        wr = [w * h, w + h, 2 * w * h] if ask == "perimeter" else [2 * (w + h), w * h // 2 if w * h % 2 == 0 else w * h + 1, w + h]
        e = "AB = %d and BC = %d (count or subtract coordinates). %s" % (
            w, h, "Perimeter = 2(%d + %d) = <b>%d units</b>." % (w, h, ans) if ask == "perimeter" else "Area = %d × %d = <b>%d square units</b>." % (w, h, ans))
        u = " units" if ask == "perimeter" else " square units"
        return T(q, num(ans) + u, [num(x) + u for x in dict.fromkeys(wr) if x != ans][:3], e)
    if kind == "right":
        a, b, c = r.choice(TRIPLES[:5])
        x1, y1 = r.randint(-6, 0), r.randint(-6, 0)
        if x1 + a > 7 or y1 + b > 7:
            return None
        P = [(x1, y1), (x1 + a, y1), (x1, y1 + b)]
        ask = r.choice(["perimeter", "area"])
        svg = grid_svg(-7, 7, points=[(x, y, n, RED) for (x, y), n in zip(P, "ABC")], polys=[(P, "#cfe6d6", GREEN)], unit=18, label="triangle ABC")
        q = "Triangle ABC has vertices A%s, B%s and C%s. Find its %s.%s" % (pt(*P[0]), pt(*P[1]), pt(*P[2]), ask, fig(svg))
        if ask == "perimeter":
            ans, wr = a + b + c, [a + b, a + b + a + b, a + b + c * c]
            e = "AB = %d, AC = %d. BC = √(%d² + %d²) = %d by the distance formula. Perimeter = %d + %d + %d = <b>%d units</b>." % (a, b, a, b, c, a, b, c, ans)
            u = " units"
        else:
            ans, wr = F(a * b, 2), [a * b, F(a * c, 2), a + b]
            e = "The legs are AB = %d and AC = %d, and they are perpendicular. Area = ½ × %d × %d = <b>%s square units</b>." % (a, b, a, b, num(ans))
            u = " square units"
        return T(q, num(ans) + u, [num(x) + u for x in dict.fromkeys(wr) if x != ans][:3], e)
    if kind == "tri":
        x1, y1 = r.randint(-6, -1), r.randint(-5, 0)
        base = r.randint(3, 8)
        h = r.randint(2, 7)
        tx = x1 + r.randint(0, base)
        if x1 + base > 7 or y1 + h > 7:
            return None
        P = [(x1, y1), (x1 + base, y1), (tx, y1 + h)]
        svg = grid_svg(-7, 7, points=[(x, y, n, RED) for (x, y), n in zip(P, "PQR")], polys=[(P, "#cfe6d6", GREEN)], unit=18, label="triangle PQR")
        q = "Find the area of triangle PQR with P%s, Q%s and R%s.%s" % (pt(*P[0]), pt(*P[1]), pt(*P[2]), fig(svg))
        ans = F(base * h, 2)
        wr = [base * h, base + h, F((base + 1) * h, 2)]
        e = "Base PQ is horizontal: %d units. Height is the vertical distance from R to the base: %d units. Area = ½ × %d × %d = <b>%s square units</b>." % (
            base, h, base, h, num(ans))
        return T(q, num(ans) + " square units", [num(x) + " square units" for x in dict.fromkeys(wr) if x != ans][:3], e)
    pp = People(r)
    nm, he, his = pp.next()
    a, b, c = r.choice(TRIPLES)
    k = r.choice([1, 2]) if c <= 13 else 1
    place = r.choice([("home", "school"), ("the library", "the park"), ("the gym", "the mall"), ("the bus station", "the museum")])
    x1, y1 = r.randint(-4, 3), r.randint(-4, 3)
    x2, y2 = x1 + a, y1 + b
    q = ("On a town map, each unit is %s mile. %s is at %s and %s is at %s. What is the straight-line distance between them?" % (
        "1" if k == 1 else "0.5", place[0].capitalize(), pt(x1, y1), place[1], pt(x2, y2)))
    d = F(c, k)
    unit = " miles" if d != 1 else " mile"
    wr = [F(a + b, k), F(c * c, k), F(c, 1) if k == 2 else F(2 * c)]
    e = "Distance on the map: √(%d² + %d²) = %d units. Each unit is %s mile, so the distance is <b>%s miles</b>." % (
        a, b, c, "1" if k == 1 else "0.5", num(d))
    return T(q, num(d) + unit, [num(x) + " miles" for x in dict.fromkeys(wr) if x != d][:3], e)


def build():
    sets = [S("Distance formula", collect(one_dist, 20, R)),
            S("Distances in radical form", collect(one_rad, 20, R)),
            S("Midpoint formula", collect(one_mid, 20, R)),
            S("Missing endpoints and partitions", collect(one_end, 20, R)),
            S("Perimeter and area on the coordinate plane", collect(one_poly, 20, R))]
    body = lesson(
        "<p>The <b>distance formula</b> is the Pythagorean theorem on the coordinate plane. The horizontal change and the vertical change are the legs "
        "of a right triangle, and the distance is the hypotenuse:</p>"
        "<p><b>d = √((<i>x</i>₂ %s <i>x</i>₁)² + (<i>y</i>₂ %s <i>y</i>₁)²)</b></p>"
        "<p>The <b>midpoint formula</b> averages the coordinates: M = ((<i>x</i>₁ + <i>x</i>₂) ÷ 2, (<i>y</i>₁ + <i>y</i>₂) ÷ 2).</p>"
        "<p>To find a point that is a fraction of the way from A to B, add that fraction of the change to A.</p>" % (MINUS, MINUS),
        [("Find the distance between (%s2, 3) and (4, %s5)." % (MINUS, MINUS),
          ["Changes: 4 %s (%s2) = 6 and %s5 %s 3 = %s8" % (MINUS, MINUS, MINUS, MINUS, MINUS), "d = √(36 + 64) = √100"], "10"),
         ("M(1, 4) is the midpoint of AB, and A is (%s3, 7). Find B." % MINUS,
          ["From A to M: +4 across, %s3 down" % MINUS, "Take the same step again from M: (1 + 4, 4 %s 3)" % MINUS], "B(5, 1)")],
        ["Adding the changes: √(6² + 8²) is 10, not 6 + 8 = 14.",
         "Forgetting the square root. 100 is d², not d.",
         "Subtracting in the midpoint formula. The midpoint is an average, so add, then divide by 2.",
         "Giving the midpoint when the question asks for the other endpoint."])
    faq = [("What is the distance formula?",
            "d = √((x₂ − x₁)² + (y₂ − y₁)²). It comes from the Pythagorean theorem, with the horizontal and vertical changes as the legs."),
           ("What is the midpoint formula?", "M = ((x₁ + x₂)/2, (y₁ + y₂)/2). Average the x-coordinates and average the y-coordinates."),
           ("How do you find an endpoint from the midpoint?", "Double the midpoint and subtract the known endpoint: B = 2M − A, for each coordinate."),
           ("How do you partition a segment in a ratio a : b?",
            "The point is a/(a + b) of the way from A to B. Multiply the change in each coordinate by a/(a + b) and add it to A.")]
    make("distance-and-midpoint-formulas", 3, "G-GPE.B.7",
         "Distance and Midpoint Formulas",
         "Distance and Midpoint Formula Worksheet (Geometry, G-GPE.B.7) | 100 Questions with Answers",
         "Distance and Midpoint",
         "Use coordinates to compute perimeters of polygons and areas of triangles and rectangles, e.g., using the distance formula.",
         "Free Geometry worksheet on the distance and midpoint formulas: radical answers, missing endpoints, partitioning a segment, and perimeter and area. 100 questions with answers.",
         "d = √((x₂ − x₁)² + (y₂ − y₁)²)",
         "The midpoint averages the coordinates: ((x₁ + x₂)/2, (y₁ + y₂)/2).",
         body, faq, sets, R, domain="Foundations of Geometry", grade="geometry")


if __name__ == "__main__":
    build()
