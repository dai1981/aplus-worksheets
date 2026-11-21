# -*- coding: utf-8 -*-
"""
India Class 10 Maths, NCERT Chapter 7: Coordinate Geometry (CBSE Unit III Coordinate Geometry)
  python3 tools/gen_in_maths_c10_coordinate_geometry.py
Distance formula, points equidistant from two points and points on an axis, collinearity and the type of a triangle or
quadrilateral by distances, the section formula (internal division), the mid-point formula, points of trisection and the
ratio in which an axis divides a segment, and problems.
Wrong answers come from real mistakes: forgetting the square root, adding the differences, (mx₁ + nx₂)/(m + n) with
m and n swapped, averaging without halving, and taking the ratio of the x-coordinates.
"""
import random, math
from fractions import Fraction as F
from in_common import num, S, make, lesson, mix, T, fv, People, MINUS

R = random.Random(910007)
P = People(R)
TRIP = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (12, 5, 13), (4, 3, 5), (8, 6, 10), (15, 8, 17)]


def pt(x, y, name=""):
    return "%s(%s, %s)" % (name, fv(x), fv(y))


def sqrt_s(n):
    s = math.isqrt(n)
    if s * s == n:
        return num(s)
    k, m = 1, n
    for f in range(s, 1, -1):
        if n % (f * f) == 0:
            k, m = f, n // (f * f)
            break
    return ("%d√%d" % (k, m)) if k > 1 else "√%d" % n


def pa(v):
    return "(%s)" % fv(v) if v < 0 else fv(v)


def minus_t(v):
    """'− 3' or '+ 3' for writing x − a"""
    return ("+ %s" % fv(-v)) if v < 0 else ("− %s" % fv(v))


def rc(lo=-8, hi=8):
    return R.randint(lo, hi)


# ---------------------------------------------------------------- set 1: distance formula
def one_dist(r):
    kind = r.choice(["trip", "trip", "surd", "origin"])
    x1, y1 = r.randint(-8, 8), r.randint(-8, 8)
    if kind in ("trip", "surd"):
        if kind == "trip":
            a, b, c = r.choice(TRIP)
            dx, dy = a * r.choice([1, -1]), b * r.choice([1, -1])
        else:
            dx, dy = r.randint(-7, 7), r.randint(-7, 7)
            if dx == 0 or dy == 0 or math.isqrt(dx * dx + dy * dy) ** 2 == dx * dx + dy * dy:
                return None
        x2, y2 = x1 + dx, y1 + dy
        d2 = dx * dx + dy * dy
        return T("Find the distance between the points %s and %s." % (pt(x1, y1, "A"), pt(x2, y2, "B")), sqrt_s(d2),
                 [num(abs(dx) + abs(dy)), num(d2), sqrt_s((x1 + x2) ** 2 + (y1 + y2) ** 2) if (x1 + x2) ** 2 + (y1 + y2) ** 2 != d2 and (x1 + x2) ** 2 + (y1 + y2) ** 2 > 0 else num(abs(dx) + abs(dy) + 1)],
                 "AB = √[(%s − %s)² + (%s − %s)²] = √(%d + %d) = <b>%s</b>." % (fv(x2), "(%s)" % fv(x1) if x1 < 0 else fv(x1), fv(y2), "(%s)" % fv(y1) if y1 < 0 else fv(y1), dx * dx, dy * dy, sqrt_s(d2)))
    a, b, c = r.choice(TRIP)
    x, y = a * r.choice([1, -1]), b * r.choice([1, -1])
    return T("How far is the point %s from the origin?" % pt(x, y, "P"), num(c), [num(abs(x) + abs(y)), num(c * c), num(abs(x - y)) if abs(x - y) not in (c, abs(x) + abs(y)) else num(c + 1)],
             "OP = √(%s² + %s²) = √%d = <b>%d</b>." % ("(%s)" % fv(x) if x < 0 else fv(x), "(%s)" % fv(y) if y < 0 else fv(y), c * c, c))


# ---------------------------------------------------------------- set 2: using the distance formula
def one_use(r):
    kind = r.choice(["axis", "axis", "find", "coll", "type"])
    if kind == "axis":
        ax = r.choice(["x", "y"])
        x1, y1, x2, y2 = rc(), rc(), rc(), rc()
        if ax == "x":
            if x1 == x2:
                return None
            v = F((x2 * x2 + y2 * y2) - (x1 * x1 + y1 * y1), 2 * (x2 - x1))
            ans = pt(v, 0)
            w = [pt(0, v), pt(-v, 0) if v else pt(1, 0), pt(F(x1 + x2, 2), 0) if F(x1 + x2, 2) != v else pt(v + 1, 0)]
        else:
            if y1 == y2:
                return None
            v = F((x2 * x2 + y2 * y2) - (x1 * x1 + y1 * y1), 2 * (y2 - y1))
            ans = pt(0, v)
            w = [pt(v, 0), pt(0, -v) if v else pt(0, 1), pt(0, F(y1 + y2, 2)) if F(y1 + y2, 2) != v else pt(0, v + 1)]
        if v.denominator > 4:
            return None
        return T("Find the point on the %s-axis which is equidistant from %s and %s." % (ax, pt(x1, y1, "A"), pt(x2, y2, "B")), ans, w,
                 "Let the point be %s. Set PA² = PB² and solve: <b>%s</b>." % ("(x, 0)" if ax == "x" else "(0, y)", ans))
    if kind == "find":
        a, b, c = r.choice(TRIP)
        x1, y1 = rc(-5, 5), rc(-5, 5)
        y2 = y1 + b
        x2a, x2b = x1 + a, x1 - a
        return T("The distance between P(%s, %s) and Q(x, %s) is %d. Find the possible values of x." % (fv(x1), fv(y1), fv(y2), c),
                 "x = %s or x = %s" % (fv(min(x2a, x2b)), fv(max(x2a, x2b))), ["x = %s only" % fv(x2a), "x = %s or x = %s" % (fv(x1 + c), fv(x1 - c)), "x = %s or x = %s" % (fv(-x2a), fv(-x2b)) if {-x2a, -x2b} != {x2a, x2b} else "x = %s or x = %s" % (fv(x2a + 1), fv(x2b - 1))],
                 "(x %s)² + %d² = %d², so (x %s)² = %d and x %s = ±%d: <b>x = %s or x = %s</b>." % (minus_t(x1), b, c, minus_t(x1), a * a, minus_t(x1), a, fv(min(x2a, x2b)), fv(max(x2a, x2b))))
    if kind == "coll":
        x1, y1 = rc(-4, 4), rc(-4, 4)
        dx, dy = r.choice([(1, 2), (2, 1), (1, 3), (3, 4), (2, 3), (1, -2), (3, -1)])
        k1, k2 = r.randint(1, 3), r.randint(1, 3)
        col = r.random() < 0.5
        P2 = (x1 + k1 * dx, y1 + k1 * dy)
        P3 = (x1 + (k1 + k2) * dx, y1 + (k1 + k2) * dy + (0 if col else r.choice([1, -1, 2])))
        return T("Are the points A%s, B%s and C%s collinear?" % (pt(x1, y1), pt(*P2), pt(*P3)), "Yes, because AB + BC = AC" if col else "No, because AB + BC ≠ AC",
                 ["No, because AB + BC ≠ AC" if col else "Yes, because AB + BC = AC", "Yes, because they all have integer coordinates", "No, because AB ≠ BC" if col else "Yes, because AB = BC"],
                 "Find AB, BC and AC with the distance formula. %s" % ("AB + BC = AC, so they lie on one line: <b>yes</b>." if col else "AB + BC is not equal to AC: <b>no</b>."))
    s = r.randint(2, 6)
    x, y = rc(-4, 4), rc(-4, 4)
    t = r.choice(["square", "rhombus", "isos"])
    if t == "square":
        pts = [(x, y), (x + s, y), (x + s, y + s), (x, y + s)]
        name = "a square (four equal sides and equal diagonals)"
    elif t == "rhombus":
        a = r.randint(2, 4)
        b = r.randint(a + 1, 6)
        pts = [(x, y), (x + a, y + b), (x + 2 * a, y), (x + a, y - b)]
        name = "a rhombus (four equal sides, unequal diagonals)"
    else:
        a, b = r.randint(2, 5), r.randint(2, 6)
        pts = [(x - a, y), (x + a, y), (x, y + b)]
        name = "an isosceles triangle"
    lst = ", ".join(pt(*p) for p in pts)
    shape = "quadrilateral" if len(pts) == 4 else "triangle"
    opts_ = ["a square (four equal sides and equal diagonals)", "a rhombus (four equal sides, unequal diagonals)", "a rectangle (unequal sides, equal diagonals)", "a parallelogram (unequal sides and diagonals)"] if len(pts) == 4 else \
        ["an isosceles triangle", "an equilateral triangle", "a scalene triangle", "a right-angled isosceles triangle"]
    if t == "isos" and a == b:
        return None
    return T("The points %s are joined in order. What kind of %s do they form?" % (lst, shape), name.capitalize(), [o.capitalize() for o in opts_ if o != name][:3],
             "Find all the side lengths (and diagonals) with the distance formula: it is <b>%s</b>." % name)


# ---------------------------------------------------------------- set 3: section formula
def one_sec(r):
    m, n = r.choice([(1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2), (1, 4), (3, 4), (2, 5)])
    x1, y1 = rc(-6, 6), rc(-6, 6)
    k = m + n
    x2, y2 = x1 + k * r.randint(-2, 2), y1 + k * r.randint(-2, 2)
    if (x1, y1) == (x2, y2):
        return None
    X_ = F(m * x2 + n * x1, k)
    Y_ = F(m * y2 + n * y1, k)
    W = F(n * x2 + m * x1, k), F(n * y2 + m * y1, k)
    return T("Find the point that divides the line segment joining A%s and B%s internally in the ratio %d : %d." % (pt(x1, y1), pt(x2, y2), m, n), pt(X_, Y_),
             [pt(*W), pt(F(x1 + x2, 2), F(y1 + y2, 2)) if (F(x1 + x2, 2), F(y1 + y2, 2)) not in ((X_, Y_), W) else pt(X_ + 1, Y_), pt(m * x2 + n * x1, m * y2 + n * y1)],
             "P = ((m x₂ + n x₁)/(m + n), (m y₂ + n y₁)/(m + n)) = ((%d × %s + %d × %s)/%d, (%d × %s + %d × %s)/%d) = <b>%s</b>." % (
                 m, pa(x2), n, pa(x1), k, m, pa(y2), n, pa(y1), k, pt(X_, Y_)))


# ---------------------------------------------------------------- set 4: mid-point, trisection, ratio
def one_mid(r):
    kind = r.choice(["mid", "mid", "end", "tri", "ratio", "ratio"])
    x1, y1, x2, y2 = rc(), rc(), rc(), rc()
    if (x1, y1) == (x2, y2):
        return None
    if kind == "mid":
        M = (F(x1 + x2, 2), F(y1 + y2, 2))
        return T("Find the mid-point of the segment joining %s and %s." % (pt(x1, y1, "A"), pt(x2, y2, "B")), pt(*M),
                 [pt(x1 + x2, y1 + y2), pt(F(x2 - x1, 2), F(y2 - y1, 2)) if (F(x2 - x1, 2), F(y2 - y1, 2)) != M else pt(M[0] + 1, M[1]), pt(M[1], M[0]) if M[0] != M[1] else pt(M[0], M[1] + 1)],
                 "Mid-point = ((x₁ + x₂)/2, (y₁ + y₂)/2) = <b>%s</b>." % pt(*M))
    if kind == "end":
        mx, my = F(x1 + x2, 2), F(y1 + y2, 2)
        return T("The mid-point of AB is M%s. If A is %s, find B." % (pt(mx, my), pt(x1, y1)), pt(x2, y2),
                 [pt(F(x1 + mx, 2), F(y1 + my, 2)), pt(mx - x1, my - y1) if (mx - x1, my - y1) != (x2, y2) else pt(x2 + 1, y2), pt(-x2, -y2) if (x2, y2) != (0, 0) else pt(1, 1)],
                 "x₂ = 2 × %s − %s = %s and y₂ = 2 × %s − %s = %s: <b>%s</b>." % (pa(mx), pa(x1), fv(x2), pa(my), pa(y1), fv(y2), pt(x2, y2)))
    if kind == "tri":
        x2, y2 = x1 + 3 * r.randint(-3, 3), y1 + 3 * r.randint(-3, 3)
        if (x1, y1) == (x2, y2):
            return None
        P1 = (F(2 * x1 + x2, 3), F(2 * y1 + y2, 3))
        P2 = (F(x1 + 2 * x2, 3), F(y1 + 2 * y2, 3))
        ans = "%s and %s" % (pt(*P1), pt(*P2))
        M = (F(x1 + x2, 2), F(y1 + y2, 2))
        return T("Find the points of trisection of the segment joining A%s and B%s." % (pt(x1, y1), pt(x2, y2)), ans,
                 ["%s and %s" % (pt(*P1), pt(*M)), "%s and %s" % (pt(F(x1 + x2, 3), F(y1 + y2, 3)), pt(F(2 * (x1 + x2), 3), F(2 * (y1 + y2), 3))), "%s and %s" % (pt(P1[0], P2[1]), pt(P2[0], P1[1])) if P1[0] != P2[0] and P1[1] != P2[1] else "%s only" % pt(*M)],
                 "They divide AB in the ratios 1 : 2 and 2 : 1: <b>%s</b>." % ans)
    ax = r.choice(["x", "y"])
    m, n = r.choice([(1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2), (1, 1), (3, 4), (4, 3)])
    if ax == "x":
        y1 = -m * r.randint(1, 3)
        y2 = n * r.randint(1, 3)
        if F(-y1, y2) != F(m, n):
            y2 = F(-y1 * n, m)
            if y2.denominator != 1:
                return None
        ans = "%d : %d" % (m, n)
        return T("In what ratio does the x-axis divide the segment joining A(%s, %s) and B(%s, %s)?" % (fv(x1), fv(y1), fv(x2), fv(y2)), ans,
                 ["%d : %d" % (n, m) if m != n else "1 : 2", "%s : %s" % (fv(abs(x1)) if x1 else "1", fv(abs(x2)) if x2 else "2") if "%s : %s" % (fv(abs(x1)) if x1 else "1", fv(abs(x2)) if x2 else "2") not in (ans, "%d : %d" % (n, m)) else "2 : 3", "1 : 1" if m != n else "2 : 1"],
                 "On the x-axis y = 0: (%sk %s)/(k + 1) = 0 gives k = %s, so the ratio is <b>%s</b>." % (fv(y2), "+ %s" % fv(y1) if y1 >= 0 else "− %s" % fv(-y1), fv(F(m, n)), ans))
    x1 = -m * r.randint(1, 3)
    x2 = F(-x1 * n, m)
    if x2.denominator != 1:
        return None
    ans = "%d : %d" % (m, n)
    return T("In what ratio does the y-axis divide the segment joining A(%s, %s) and B(%s, %s)?" % (fv(x1), fv(y1), fv(x2), fv(y2)), ans,
             ["%d : %d" % (n, m) if m != n else "1 : 2", "2 : 3" if ans != "2 : 3" else "3 : 5", "1 : 1" if m != n else "2 : 1"],
             "On the y-axis x = 0: (%sk %s)/(k + 1) = 0 gives k = %s, so the ratio is <b>%s</b>." % (fv(x2), "+ %s" % fv(x1) if x1 >= 0 else "− %s" % fv(-x1), fv(F(m, n)), ans))


# ---------------------------------------------------------------- set 5: problems
def one_prob(r):
    kind = r.choice(["para", "para", "garden", "town", "center"])
    if kind == "para":
        ax, ay, bx, by, cx, cy = [rc(-5, 6) for _ in range(6)]
        dx, dy = ax + cx - bx, ay + cy - by
        if len({(ax, ay), (bx, by), (cx, cy)}) < 3 or (bx - ax) * (cy - ay) == (by - ay) * (cx - ax):
            return None
        return T("A%s, B%s and C%s are three vertices of parallelogram ABCD. Find D." % (pt(ax, ay), pt(bx, by), pt(cx, cy)), pt(dx, dy),
                 [pt(bx + cx - ax, by + cy - ay), pt(ax + bx - cx, ay + by - cy), pt(F(ax + cx, 2), F(ay + cy, 2))],
                 "The diagonals of a parallelogram bisect each other: mid-point of AC = mid-point of BD, so D = A + C − B = <b>%s</b>." % pt(dx, dy))
    if kind == "center":
        cx, cy = rc(-5, 5), rc(-5, 5)
        a, b, c = r.choice(TRIP)
        px, py = cx + a, cy + b
        qx, qy = 2 * cx - px, 2 * cy - py
        return T("The centre of a circle is %s and one end of a diameter is %s. Find the other end." % (pt(cx, cy, "O"), pt(px, py, "A")), pt(qx, qy),
                 [pt(F(cx + px, 2), F(cy + py, 2)), pt(px - cx, py - cy), pt(-px, -py)],
                 "O is the mid-point of the diameter: B = 2O − A = <b>%s</b>." % pt(qx, qy))
    name, he, his = P.next()
    if kind == "garden":
        a, b, c = r.choice(TRIP)
        k = r.choice([1, 2, 10, 5])
        x1, y1 = rc(0, 5), rc(0, 5)
        x2, y2 = x1 + a * k, y1 + b * k
        return T("On a map grid (1 unit = 1 m), %s's house is at %s and %s school gate is at %s. How far is it in a straight line?" % (name, pt(x1, y1), his, pt(x2, y2)), "%s m" % num(c * k),
                 ["%s m" % num((a + b) * k), "%s m" % num((c * k) ** 2), "%s m" % num(abs(a - b) * k) if abs(a - b) * k != c * k else "%s m" % num(c * k + 1)],
                 "Distance = √[(%d)² + (%d)²] = <b>%s m</b>." % (a * k, b * k, num(c * k)))
    m, n = r.choice([(1, 2), (2, 1), (1, 3), (3, 1)])
    k = m + n
    x1, y1 = rc(0, 6), rc(0, 6)
    x2, y2 = x1 + k * r.randint(1, 3), y1 + k * r.randint(1, 3)
    Px, Py = F(m * x2 + n * x1, k), F(m * y2 + n * y1, k)
    return T("Two villages are at A%s and B%s on a grid. A well is to be dug on AB so that its distances from A and B are in the ratio %d : %d. Where should it be?" % (pt(x1, y1), pt(x2, y2), m, n),
             pt(Px, Py), [pt(F(n * x2 + m * x1, k), F(n * y2 + m * y1, k)), pt(F(x1 + x2, 2), F(y1 + y2, 2)) if m != n else pt(Px + 1, Py), pt(Px, Py + 1)],
             "Section formula with m : n = %d : %d: <b>%s</b>." % (m, n, pt(Px, Py)))


def main():
    seen = set()
    sets = [
        S("Distance formula", mix(R, [(one_dist, 20)], seen)),
        S("Using the distance formula", mix(R, [(one_use, 20)], seen)),
        S("Section formula", mix(R, [(one_sec, 20)], seen)),
        S("Mid-point, trisection and ratios", mix(R, [(one_mid, 20)], seen)),
        S("Problems", mix(R, [(one_prob, 20)], seen)),
    ]
    body = lesson(
        "<p><b>Distance formula</b>: the distance between P(x₁, y₁) and Q(x₂, y₂) is √[(x₂ − x₁)² + (y₂ − y₁)²]. From the origin: √(x² + y²).</p>"
        "<p><b>Section formula</b>: the point dividing PQ internally in the ratio m : n is ((mx₂ + nx₁)/(m + n), (my₂ + ny₁)/(m + n)).</p>"
        "<p><b>Mid-point</b> (ratio 1 : 1): ((x₁ + x₂)/2, (y₁ + y₂)/2).</p>",
        [("Find the distance between (2, 3) and (4, 1).", ["√[(4 − 2)² + (1 − 3)²]", "√8"], "2√2"),
         ("Find the point dividing A(4, −3) and B(8, 5) in the ratio 3 : 1.", ["x = (3 × 8 + 1 × 4)/4 = 7", "y = (3 × 5 + 1 × (−3))/4 = 3"], "(7, 3)")],
        ["Forgetting the square root in the distance formula.",
         "Swapping m and n: m goes with the second point (x₂, y₂).",
         "Adding the coordinates for the mid-point without dividing by 2."])
    faq = [
        ("What is the distance formula?", "The distance between (x₁, y₁) and (x₂, y₂) is √[(x₂ − x₁)² + (y₂ − y₁)²]. It comes from Pythagoras theorem."),
        ("What is the section formula?", "The point dividing the join of (x₁, y₁) and (x₂, y₂) internally in the ratio m : n is ((mx₂ + nx₁)/(m + n), (my₂ + ny₁)/(m + n))."),
        ("How do I check whether three points are collinear using distances?", "Find the three distances. If the two shorter ones add up to the longest, the points are collinear."),
        ("How do I find the ratio in which the x-axis divides a segment?", "Take the ratio as k : 1 and set the y-coordinate from the section formula equal to 0, then solve for k."),
    ]
    make(10, "coordinate-geometry", 7, "III", 7, "Coordinate Geometry: Distance and Section Formulae", "coordinate geometry",
         "Concepts of coordinate geometry, graphs of linear equations; distance formula; section formula (internal division) (summary of the CBSE syllabus)",
         "Class 10 Coordinate Geometry worksheet (NCERT Chapter 7): distance formula, equidistant points, collinearity, section formula, mid-points and trisection. 100 questions with answers.",
         "d = √[(x₂ − x₁)² + (y₂ − y₁)²]", "Section formula: ((mx₂ + nx₁)/(m + n), (my₂ + ny₁)/(m + n)).",
         body, faq, sets, R)


if __name__ == "__main__":
    main()
