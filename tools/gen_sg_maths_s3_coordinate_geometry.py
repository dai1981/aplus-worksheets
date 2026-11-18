# -*- coding: utf-8 -*-
"""
SG Secondary 3 Maths: Coordinate Geometry (MOE syllabus G6)
  python3 tools/gen_sg_maths_s3_coordinate_geometry.py
Gradient of a line through two points, length of a line segment, the equation y = mx + c, parallel lines and
intercepts, and geometric problems (unknown coordinates, areas of triangles, right angles, collinear points).
Wrong answers come from real mistakes: run ÷ rise, subtracting the coordinates in different orders, forgetting
to square-root, adding instead of subtracting inside the square, and using the wrong point to find c.
"""
import random
from fractions import Fraction as F
from math import isqrt, sqrt
from sg_sec import num, S, make, lesson, collect, T, expr, fr, fig, MINUS
from g8_common import grid_svg

R = random.Random(830900)
X, Y = "<i>x</i>", "<i>y</i>"


def fv(v):
    v = F(v)
    return num(v) if v.denominator == 1 else (MINUS if v < 0 else "") + fr(abs(v.numerator), v.denominator)


def pt(p):
    return "(%s, %s)" % (num(p[0]), num(p[1]))


def line_eq(m, c):
    m, c = F(m), F(c)
    if m == 0:
        return "%s = %s" % (Y, fv(c))
    mx = (fv(m) if m not in (1, -1) else ("" if m == 1 else MINUS)) + X
    if m.denominator != 1:
        mx = fv(m) + X
    if c == 0:
        return "%s = %s" % (Y, mx)
    return "%s = %s %s %s" % (Y, mx, "+" if c > 0 else MINUS, fv(abs(c)))


def d2(v):
    return ("%.2f" % v).replace("-", MINUS)


def surd(n):
    k = 1
    for t in range(isqrt(n), 1, -1):
        if n % (t * t) == 0:
            k = t
            break
    m = n // (k * k)
    if m == 1:
        return num(k)
    return ("" if k == 1 else num(k)) + "√" + num(m)


def two_pts(r, lo=-8, hi=8):
    while True:
        a = (r.randint(lo, hi), r.randint(lo, hi))
        b = (r.randint(lo, hi), r.randint(lo, hi))
        if a[0] != b[0] and a != b:
            return a, b


def plot(ps, names, lo=-6, hi=6):
    svg = grid_svg(lo, hi, unit=22, label="points on a coordinate grid", ylo=lo, yhi=hi)
    Xp = lambda x: 22 + (x - lo) * 22
    Yp = lambda y: 22 + (hi - y) * 22
    add = ["<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#1f6fd1' stroke-width='2.6'/>" % (Xp(ps[0][0]), Yp(ps[0][1]), Xp(ps[1][0]), Yp(ps[1][1]))]
    for p, n in zip(ps, names):
        add.append("<circle cx='%.1f' cy='%.1f' r='4.5' fill='#c0392b'/><text x='%.1f' y='%.1f' font-size='14' font-weight='700' fill='#c0392b'>%s</text>" % (
            Xp(p[0]), Yp(p[1]), Xp(p[0]) + 6, Yp(p[1]) - 6, n))
    return fig(svg.replace("</g></svg>", "".join(add) + "</g></svg>"))


# ------------------------------------------------------------ set 1: gradient
def one_grad(r):
    kind = r.choice(["calc", "calc", "calc", "graph"])
    if kind == "graph":
        a, b = two_pts(r, -6, 6)
        m = F(b[1] - a[1], b[0] - a[0])
        right = fv(m)
        wr = [fv(1 / m) if m else "1", fv(-m) if m else "−1", fv(F(b[1] - a[1], b[0] + a[0])) if b[0] + a[0] and F(b[1] - a[1], b[0] + a[0]) not in (m, -m) else fv(m + 1)]
        if len({right} | set(wr)) < 4:
            return None
        return T("Find the gradient of the line through A and B.%s" % plot([a, b], ["A", "B"]), right, wr,
                 "A%s and B%s. Gradient = rise ÷ run = (%s − %s) ÷ (%s − %s) = <b>%s</b>." % (pt(a), pt(b), num(b[1]), par(a[1]), num(b[0]), par(a[0]), right))
    a, b = two_pts(r)
    m = F(b[1] - a[1], b[0] - a[0])
    right = fv(m)
    wr = [fv(1 / m) if m else "1", fv(-m) if m else fv(F(1, 2)), fv(F(b[1] + a[1], b[0] + a[0])) if b[0] + a[0] and F(b[1] + a[1], b[0] + a[0]) not in (m, -m, 1 / m if m else None) else fv(m + 2)]
    if len({right} | set(wr)) < 4:
        return None
    return T("Find the gradient of the line joining %s and %s." % (pt(a), pt(b)), right, wr,
             "Gradient = (%s − %s) ÷ (%s − %s) = %s ÷ %s = <b>%s</b>." % (num(b[1]), par(a[1]), num(b[0]), par(a[0]), num(b[1] - a[1]), num(b[0] - a[0]), right))


def par(v):
    return "(%s)" % num(v) if v < 0 else num(v)


# ------------------------------------------------------------ set 2: length of a line segment
TRIP = [(3, 4), (5, 12), (6, 8), (8, 6), (4, 3), (12, 5), (8, 15), (9, 12)]


def one_len(r):
    exact = r.random() < 0.55
    a = (r.randint(-7, 7), r.randint(-7, 7))
    if exact:
        dx, dy = r.choice(TRIP)
        dx *= r.choice([1, -1])
        dy *= r.choice([1, -1])
    else:
        dx, dy = r.randint(-9, 9), r.randint(-9, 9)
        if dx == 0 or dy == 0 or isqrt(dx * dx + dy * dy) ** 2 == dx * dx + dy * dy:
            return None
    b = (a[0] + dx, a[1] + dy)
    L2 = dx * dx + dy * dy
    L = sqrt(L2)
    wrong_add = (b[0] + a[0]) ** 2 + (b[1] + a[1]) ** 2
    if exact:
        right = "%s units" % num(isqrt(L2))
        wr = ["%s units" % num(L2), "%s units" % num(abs(dx) + abs(dy)), "%s units" % d2(sqrt(wrong_add)) if isqrt(wrong_add) ** 2 != wrong_add else "%s units" % num(isqrt(wrong_add))]
    else:
        right = "%s units" % d2(L)
        wr = ["%s units" % num(L2), "%s units" % num(abs(dx) + abs(dy)), "%s units" % d2(sqrt(wrong_add)) if wrong_add else "%s units" % d2(L + 1)]
    if len({right} | set(wr)) < 4:
        return None
    q = "Find the length of the line segment joining %s and %s%s." % (pt(a), pt(b), "" if exact else ", correct to 2 decimal places")
    return T(q, right, wr, "Length = √((%s − %s)<sup>2</sup> + (%s − %s)<sup>2</sup>) = √(%s + %s) = √%s = <b>%s</b>." % (
        num(b[0]), par(a[0]), num(b[1]), par(a[1]), num(dx * dx), num(dy * dy), num(L2), right))


# ------------------------------------------------------------ set 3: the equation y = mx + c
def one_eq(r):
    kind = r.choice(["mc", "point", "two", "two"])
    m = F(r.choice([-3, -2, -1, 1, 2, 3, 4]), r.choice([1, 1, 1, 2]))
    if kind == "mc":
        c = r.randint(-8, 8)
        eqs = [("%s = %s" % (expr([(1, Y)]), line_eq(m, c).split(" = ")[1]), m, c)]
        k = r.choice([2, 3])
        # write as k y = k m x + k c
        if (k * m).denominator != 1:
            return None
        q = "Find the gradient and the %s-intercept of the line %s." % (Y, "%s = %s" % (expr([(k, Y)]), expr([(k * m, X), (k * c, "")])))
        right = "gradient %s, %s-intercept %s" % (fv(m), Y, fv(c))
        wr = ["gradient %s, %s-intercept %s" % (fv(k * m), Y, fv(k * c)), "gradient %s, %s-intercept %s" % (fv(c), Y, fv(m)) if c != m else "gradient %s, %s-intercept %s" % (fv(-m), Y, fv(c)),
              "gradient %s, %s-intercept %s" % (fv(m), Y, fv(k * c)) if c else "gradient %s, %s-intercept %s" % (fv(-m), Y, fv(-c + 1))]
        return T(q, right, wr, "Divide by %d to get %s. The gradient is <b>%s</b> and the %s-intercept is <b>%s</b>." % (k, line_eq(m, c), fv(m), Y, fv(c)))
    if kind == "point":
        x0 = r.randint(-5, 5)
        y0 = r.randint(-8, 8)
        c = y0 - m * x0
        if c.denominator != 1:
            return None
        q = "Find the equation of the line with gradient %s that passes through %s." % (fv(m), pt((x0, y0)))
        right = line_eq(m, c)
        wr = [line_eq(m, y0 + m * x0), line_eq(m, y0), line_eq(-m, c) if c else line_eq(m, c + 1)]
        if len({right} | set(wr)) < 4:
            return None
        return T(q, right, wr, "Substitute %s into %s = %s%s + <i>c</i>: %s = %s × %s + <i>c</i>, so <i>c</i> = %s. <b>%s</b>." % (
            pt((x0, y0)), Y, fv(m), X, num(y0), fv(m), par(x0), fv(c), right))
    a, b = two_pts(r, -6, 6)
    m = F(b[1] - a[1], b[0] - a[0])
    c = a[1] - m * a[0]
    if m == 0 or c.denominator != 1 or m.denominator > 2:
        return None
    right = line_eq(m, c)
    wr = [line_eq(1 / m, a[1] - a[0] / m), line_eq(m, a[1] + m * a[0]), line_eq(-m, c)]
    if len({right} | set(wr)) < 4:
        return None
    return T("Find the equation of the line through %s and %s." % (pt(a), pt(b)), right, wr,
             "Gradient = %s ÷ %s = %s. Substitute %s: %s = %s × %s + <i>c</i>, so <i>c</i> = %s. <b>%s</b>." % (
                 num(b[1] - a[1]), num(b[0] - a[0]), fv(m), pt(a), num(a[1]), fv(m), par(a[0]), fv(c), right))


# ------------------------------------------------------------ set 4: parallel lines and intercepts
def one_par(r):
    kind = r.choice(["par", "par", "xint", "meet", "which"])
    m = F(r.choice([-3, -2, -1, 2, 3, 4, F(1, 2), F(-1, 2)]))
    if kind == "par":
        c = r.randint(-6, 6)
        x0, y0 = r.randint(-4, 4), r.randint(-6, 6)
        c2 = y0 - m * x0
        if c2.denominator != 1 or c2 == c:
            return None
        q = "Find the equation of the line parallel to %s that passes through %s." % (line_eq(m, c), pt((x0, y0)))
        right = line_eq(m, c2)
        wr = [line_eq(m, c), line_eq(-1 / m, y0 + x0 / m) if (y0 + x0 / m).denominator == 1 else line_eq(-m, c2), line_eq(m, y0)]
        if len({right} | set(wr)) < 4:
            return None
        return T(q, right, wr, "Parallel lines have the same gradient, %s. %s = %s × %s + <i>c</i> gives <i>c</i> = %s: <b>%s</b>." % (fv(m), num(y0), fv(m), par(x0), fv(c2), right))
    if kind == "xint":
        c = r.randint(-8, 8)
        if c == 0:
            return None
        x = -F(c) / m
        q = "Where does the line %s cross the %s-axis?" % (line_eq(m, c), X)
        right = "(%s, 0)" % fv(x)
        return T(q, right, ["(0, %s)" % fv(c), "(%s, 0)" % fv(-x), "(%s, 0)" % fv(F(c) / m * m * m) if F(c) * m not in (x, -x) else "(%s, 0)" % fv(x + 1)],
                 "On the %s-axis, %s = 0: 0 = %s%s %s %s, so %s = <b>%s</b>. The point is <b>%s</b>." % (X, Y, fv(m), X, "+" if c > 0 else MINUS, num(abs(c)), X, fv(x), right))
    if kind == "meet":
        x0, y0 = r.randint(-4, 4), r.randint(-5, 5)
        m2 = r.choice([v for v in [-2, -1, 1, 2, 3] if v != m])
        c1, c2 = y0 - m * x0, y0 - m2 * x0
        if F(c1).denominator != 1 or F(c2).denominator != 1:
            return None
        q = "Find the point where the lines %s and %s meet." % (line_eq(m, c1), line_eq(m2, c2))
        right = pt((x0, y0))
        return T(q, right, [pt((y0, x0)) if x0 != y0 else pt((x0, -y0)), pt((-x0, y0)) if x0 else pt((x0, y0 + 1)), pt((x0, int(m * x0 + c2 * 0 + c1) + 1))],
                 "Set the right-hand sides equal: %s = %s, so %s = %s. Then %s = %s. <b>%s</b>." % (
                     line_eq(m, c1).split(" = ", 1)[1], line_eq(m2, c2).split(" = ", 1)[1], X, num(x0), Y, num(y0), right))
    c = r.randint(-5, 5)
    q = "Which line is parallel to %s?" % line_eq(m, c)
    k = r.choice([2, 3])
    right = "%s = %s" % (expr([(k, Y)]), expr([(k * m, X), (r.randint(-9, 9), "")])) if (k * m).denominator == 1 else line_eq(m, c + 3)
    wr = [line_eq(-m, c), line_eq(1 / m, c), "%s = %s" % (expr([(k, Y)]), expr([(m, X), (c, "")])) if m.denominator == 1 else line_eq(m * 2, c)]
    if len({right} | set(wr)) < 4:
        return None
    return T(q, right, wr, "Parallel lines have the same gradient, %s. Divide %s by the number in front of %s to check: <b>%s</b>." % (fv(m), right, Y, right))


# ------------------------------------------------------------ set 5: geometric problems
def one_geo(r):
    kind = r.choice(["k", "k", "area", "right", "col"])
    if kind == "k":
        a = (r.randint(-5, 5), r.randint(-5, 5))
        m = r.choice([-3, -2, -1, 1, 2, 3])
        dx = r.choice([-4, -3, -2, 2, 3, 4])
        k = a[1] + m * dx
        q = "The line joining A%s and B(%s, <i>k</i>) has gradient %s. Find <i>k</i>." % (pt(a), num(a[0] + dx), num(m))
        return T(q, num(k), [num(a[1] - m * dx), num(m * dx), num(a[1] + F(dx, m)) if F(dx, m).denominator == 1 else num(k + 1)],
                 "(<i>k</i> − %s) ÷ (%s − %s) = %s, so <i>k</i> − %s = %s and <i>k</i> = <b>%s</b>." % (par(a[1]), num(a[0] + dx), par(a[0]), num(m), par(a[1]), num(m * dx), num(k)))
    if kind == "area":
        x1, x2 = sorted(r.sample(range(-5, 7), 2))
        y0 = r.randint(-4, 2)
        h = r.randint(2, 7)
        xc = r.randint(-5, 6)
        base = x2 - x1
        A = F(base * h, 2)
        q = "Find the area of the triangle with vertices %s, %s and %s." % (pt((x1, y0)), pt((x2, y0)), pt((xc, y0 + h)))
        su = lambda v: "%s square unit%s" % (fv(v), "" if v == 1 else "s")
        w3 = F(base * (y0 + h), 2)
        return T(q, su(A), [su(base * h), su(F(base + h)), su(w3) if y0 and w3 > 0 and w3 != A else su(A + 1)],
                 "The base is on the line %s = %s with length %s − %s = %d. The height is %d. Area = ½ × %d × %d = <b>%s</b> square units." % (Y, num(y0), num(x2), par(x1), base, h, base, h, fv(A)))
    if kind == "right":
        p = (r.randint(-4, 3), r.randint(-4, 3))
        u = r.choice([(1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (1, 1)])
        s = r.choice([1, 2])
        a = (p[0] + u[0] * s, p[1] + u[1] * s)
        b = (p[0] - u[1] * s, p[1] + u[0] * s)
        AB2 = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
        PA2 = (a[0] - p[0]) ** 2 + (a[1] - p[1]) ** 2
        PB2 = (b[0] - p[0]) ** 2 + (b[1] - p[1]) ** 2
        q = "P%s, A%s and B%s are the vertices of a triangle. Which statement is true?" % (pt(p), pt(a), pt(b))
        right = "PA² + PB² = AB², so angle APB = 90°"
        return T(q, right, ["PA = PB = AB, so the triangle is equilateral", "AB² + PA² = PB², so angle PAB = 90°", "No angle is 90°"],
                 "PA² = %d, PB² = %d and AB² = %d. %d + %d = %d, so by the converse of Pythagoras' theorem <b>angle APB = 90°</b>." % (PA2, PB2, AB2, PA2, PB2, AB2))
    a = (r.randint(-5, 2), r.randint(-5, 2))
    d = (r.choice([1, 2, 3]), r.choice([-2, -1, 1, 2, 3]))
    t = r.choice([2, 3])
    b = (a[0] + d[0], a[1] + d[1])
    c_on = (a[0] + t * d[0], a[1] + t * d[1])
    off = r.choice([True, False])
    c = c_on if not off else (c_on[0], c_on[1] + 1)
    m1 = F(d[1], d[0])
    m2 = F(c[1] - a[1], c[0] - a[0])
    q = "Are the points A%s, B%s and C%s on the same straight line?" % (pt(a), pt(b), pt(c))
    if off:
        right = "No: gradient AB = %s but gradient AC = %s" % (fv(m1), fv(m2))
        wr = ["Yes: gradient AB = gradient AC = %s" % fv(m1), "Yes: they all have positive coordinates" if False else "Yes: AB = BC", "No: gradient AB = %s but gradient AC = %s" % (fv(-m1), fv(m2))]
    else:
        right = "Yes: gradient AB = gradient AC = %s" % fv(m1)
        wr = ["No: gradient AB = %s but gradient AC = %s" % (fv(m1), fv(m1 * t)), "No: AB is not equal to BC", "Yes: gradient AB = gradient AC = %s" % fv(1 / m1)]
    if len({right} | set(wr)) < 4:
        return None
    return T(q, right, wr, "Compare gradients from A: AB has gradient %s and AC has gradient %s. %s" % (
        fv(m1), fv(m2), "They are equal, so the points are collinear: <b>yes</b>." if not off else "They are different: <b>no</b>."))


def build():
    sets = [S("Gradient of a line", collect(one_grad, 20, R)),
            S("Length of a line segment", collect(one_len, 20, R)),
            S("The equation y = mx + c", collect(one_eq, 20, R)),
            S("Parallel lines and intercepts", collect(one_par, 20, R)),
            S("Geometric problems", collect(one_geo, 20, R))]
    body = lesson(
        "<ul><li><b>Gradient</b> of the line through (<i>x</i><sub>1</sub>, <i>y</i><sub>1</sub>) and (<i>x</i><sub>2</sub>, <i>y</i><sub>2</sub>) = (<i>y</i><sub>2</sub> − <i>y</i><sub>1</sub>) ÷ (<i>x</i><sub>2</sub> − <i>x</i><sub>1</sub>).</li>"
        "<li><b>Length</b> = √((<i>x</i><sub>2</sub> − <i>x</i><sub>1</sub>)<sup>2</sup> + (<i>y</i><sub>2</sub> − <i>y</i><sub>1</sub>)<sup>2</sup>). This is Pythagoras' theorem on the grid.</li>"
        "<li>In <b><i>y</i> = <i>mx</i> + <i>c</i></b>, <i>m</i> is the gradient and <i>c</i> is the <i>y</i>-intercept. To find <i>c</i>, substitute a point on the line.</li>"
        "<li><b>Parallel lines</b> have equal gradients.</li></ul>",
        [("Find the equation of the line through (1, 2) and (3, 8).", ["Gradient = (8 − 2) ÷ (3 − 1) = 3", "2 = 3 × 1 + c, so c = −1"], "y = 3x − 1"),
         ("Find the length of the line joining (−1, 2) and (5, −6).", ["√(6² + (−8)²) = √(36 + 64) = √100"], "10 units")],
        ["Working out run ÷ rise instead of rise ÷ run.",
         "Subtracting the x-values in one order and the y-values in the other.",
         "Forgetting the square root at the end of the length formula.",
         "Mixing up the gradient and the y-intercept in 2y = 6x + 4. Divide by 2 first: y = 3x + 2."])
    faq = [("How do you find the gradient from two points?", "Divide the change in y by the change in x: (y₂ − y₁) ÷ (x₂ − x₁). Keep the points in the same order on top and bottom."),
           ("How do you find the length of a line segment?", "Use √((x₂ − x₁)² + (y₂ − y₁)²). It is Pythagoras' theorem with the horizontal and vertical distances as the shorter sides."),
           ("How do you find the equation of a straight line?", "Find the gradient m, then substitute one point into y = mx + c to find c."),
           ("How can I tell if two lines are parallel?", "Write both in the form y = mx + c. If the gradients m are equal, the lines are parallel.")]
    make(3, "coordinate-geometry", 9, "G6",
         "Coordinate Geometry: Gradient, Length and Equation of a Line",
         "", "Coordinate geometry", "",
         "Free Secondary 3 maths worksheets on coordinate geometry: gradient from two points, length of a line segment, equations y = mx + c, parallel lines and geometric problems. 100 questions with answers.",
         "Gradient = rise ÷ run; length = √(run² + rise²).",
         "In y = mx + c, m is the gradient and c is the y-intercept. Parallel lines have equal gradients.",
         body, faq, sets, R)


if __name__ == "__main__":
    build()
