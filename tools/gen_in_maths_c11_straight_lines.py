# -*- coding: utf-8 -*-
"""
India Class 11 Maths, NCERT Chapter 9: Straight Lines (CBSE Unit III Coordinate Geometry)
  python3 tools/gen_in_maths_c11_straight_lines.py
Slope from two points and from the inclination, parallel and perpendicular lines, the angle between two lines,
collinear points, the point-slope, two-point, slope-intercept and intercept forms, and the distance of a point from
a line and between parallel lines (own makers).
Wrong answers come from real mistakes: (x₂ − x₁)/(y₂ − y₁), tan of the wrong angle, m₁m₂ = 1 for perpendicular
lines, forgetting the modulus or the square root in the distance formula, and mixing up the intercepts.
"""
import random
from fractions import Fraction as F
from in_sr import U, T2, X, Y, rt, frs
from in_common import num, fv, expr

R = random.Random(911109)


def pt(x, y):
    return "(%s, %s)" % (num(x), num(y))


def gen(a, b, c):
    """a x + b y + c = 0, integers with a > 0"""
    if a < 0 or (a == 0 and b < 0):
        a, b, c = -a, -b, -c
    return expr([(a, X), (b, Y), (c, "")]) + " = 0"


def norm(a, b, c):
    from math import gcd
    g = gcd(gcd(abs(a), abs(b)), abs(c)) or 1
    return a // g, b // g, c // g


TAN = {30: "1/√3", 45: "1", 60: "√3", 120: "−√3", 135: "−1", 150: "−1/√3", 0: "0"}


def one_slope(r):
    k = r.choice(["two", "two", "incl", "back"])
    if k == "two":
        x1, y1 = r.randint(-6, 6), r.randint(-6, 6)
        dx, dy = r.choice([k for k in range(-6, 7) if k]), r.randint(-8, 8)
        x2, y2 = x1 + dx, y1 + dy
        m = F(dy, dx)
        return T2("Find the slope of the line through %s and %s." % (pt(x1, y1), pt(x2, y2)), fv(m),
                  [fv(F(dx, dy)) if dy else "not defined", fv(-m) if m else "1", fv(F(y2 + y1, x2 + x1)) if x2 + x1 and F(y2 + y1, x2 + x1) not in (m, -m) else fv(m + 1)],
                  "m = (y<sub>2</sub> − y<sub>1</sub>) ÷ (x<sub>2</sub> − x<sub>1</sub>) = %s ÷ %s = <b>%s</b>." % (num(dy), num(dx), fv(m)))
    th = r.choice([30, 45, 60, 120, 135, 150])
    if k == "incl":
        return T2("A line makes an angle of %d° with the positive direction of the %s-axis. What is its slope?" % (th, X), TAN[th],
                  [TAN[{30: 60, 60: 30, 45: 135, 135: 45, 120: 150, 150: 120}[th]], TAN[180 - th], "%d" % th if th % 45 else "0"],
                  "m = tan θ = tan %d° = <b>%s</b>." % (th, TAN[th]))
    return T2("The slope of a line is %s. What angle does it make with the positive %s-axis?" % (TAN[th], X), "%d°" % th,
              ["%d°" % (180 - th), "%d°" % (90 - th if th < 90 else th - 90), "%d°" % ({30: 60, 60: 30, 45: 135, 135: 45, 120: 150, 150: 120}[th])],
              "tan θ = %s with 0° ≤ θ &lt; 180° gives <b>θ = %d°</b>." % (TAN[th], th))


def one_pp(r):
    k = r.choice(["perp", "par", "angle", "coll"])
    if k in ("perp", "par"):
        m = F(r.choice([k for k in range(-5, 6) if k]), r.choice([1, 2, 3]))
        mm = m if k == "par" else -1 / m
        return T2("A line has slope %s. What is the slope of a line %s to it?" % (fv(m), "parallel" if k == "par" else "perpendicular"), fv(mm),
                  [fv(-1 / m if k == "par" else m), fv(1 / m), fv(-m)],
                  "%s: <b>%s</b>." % ("Parallel lines have equal slopes" if k == "par" else "Perpendicular lines have m<sub>1</sub>m<sub>2</sub> = −1, so m<sub>2</sub> = −1 ÷ m<sub>1</sub>", fv(mm)))
    if k == "angle":
        m1 = F(r.choice([k for k in range(-4, 5) if k not in (0, 1, -1)]), r.choice([1, 2, 3]))
        if m1 in (1, -1):
            return None
        m2 = (1 + m1) / (1 - m1)
        if abs(m2.denominator) > 9 or abs(m2.numerator) > 20:
            return None
        return T2("Find the acute angle between lines with slopes %s and %s." % (fv(m1), fv(m2)), "45°", ["30°", "60°", "90°"],
                  "tan θ = |(m<sub>2</sub> − m<sub>1</sub>) ÷ (1 + m<sub>1</sub>m<sub>2</sub>)| = |%s ÷ %s| = 1, so <b>θ = 45°</b>." % (fv(m2 - m1), fv(1 + m1 * m2)))
    x1, y1 = r.randint(-5, 5), r.randint(-5, 5)
    dx, dy = r.choice([1, 2, 3, -1, -2]), r.randint(-4, 4)
    t = r.choice([2, 3, -1, -2])
    kk = y1 + t * dy
    return T2("Find k if the points %s, %s and %s are collinear." % (pt(x1, y1), pt(x1 + dx, y1 + dy), "(%s, k)" % num(x1 + t * dx)), num(kk),
              [num(kk + dy), num(-kk) if kk else "1", num(y1 + dy)],
              "Collinear points give equal slopes: %s = (k − %s) ÷ %s, so <b>k = %s</b>." % (fv(F(dy, dx)), num(y1), num(t * dx), num(kk)))


def one_eq(r):
    k = r.choice(["ps", "two", "int", "si"])
    if k == "ps":
        x1, y1 = r.randint(-5, 5), r.randint(-5, 5)
        p, q = r.choice([k for k in range(-4, 5) if k]), r.choice([1, 2, 3])
        a, b, c = norm(p, -q, q * y1 - p * x1)
        right = gen(a, b, c)
        return T2("Find the equation of the line through %s with slope %s." % (pt(x1, y1), fv(F(p, q))), right,
                  [gen(*norm(p, -q, -(q * y1 - p * x1))), gen(*norm(q, -p, p * y1 - q * x1)), gen(*norm(p, q, -q * y1 - p * x1))],
                  "<i>y</i> − %s = %s(%s − %s), which gives <b>%s</b>." % (num(y1), fv(F(p, q)), X, num(x1), right))
    if k == "two":
        x1, y1 = r.randint(-5, 5), r.randint(-5, 5)
        x2, y2 = x1 + r.choice([1, 2, 3, -2, 4]), y1 + r.randint(-5, 5)
        a, b, c = norm(y2 - y1, -(x2 - x1), (x2 - x1) * y1 - (y2 - y1) * x1)
        right = gen(a, b, c)
        return T2("Find the equation of the line through %s and %s." % (pt(x1, y1), pt(x2, y2)), right,
                  [gen(*norm(x2 - x1, -(y2 - y1), (y2 - y1) * y1 - (x2 - x1) * x1)), gen(*norm(a, b, -c)) if c else gen(a, b, 1), gen(*norm(a, -b, c)) if b else gen(a, 1, c)],
                  "Slope %s, then <i>y</i> − %s = %s(%s − %s): <b>%s</b>." % (fv(F(y2 - y1, x2 - x1)), num(y1), fv(F(y2 - y1, x2 - x1)), X, num(x1), right))
    if k == "int":
        a, b = r.choice([k for k in range(-6, 7) if k]), r.choice([k for k in range(-6, 7) if k])
        if a == b:
            return None
        A, B, Cc = norm(b, a, -a * b)
        right = gen(A, B, Cc)
        return T2("Find the equation of the line with %s-intercept %s and <i>y</i>-intercept %s." % (X, num(a), num(b)), right,
                  [gen(*norm(a, b, -a * b)), gen(*norm(b, a, a * b)), gen(*norm(b, -a, -a * b))],
                  "%s/%s + <i>y</i>/%s = 1, so <b>%s</b>." % (X, num(a), num(b), right))
    a, b, c = r.choice([k for k in range(-6, 7) if k]), r.choice([k for k in range(1, 7)]), r.randint(-12, 12)
    m, ci = F(-a, b), F(-c, b)
    return T2("Find the slope and the <i>y</i>-intercept of %s." % gen(a, b, c), "slope %s, <i>y</i>-intercept %s" % (fv(m), fv(ci)),
              ["slope %s, <i>y</i>-intercept %s" % (fv(-m), fv(-ci)), "slope %s, <i>y</i>-intercept %s" % (fv(F(b, a)), fv(ci)), "slope %s, <i>y</i>-intercept %s" % (fv(m), fv(F(-c, a)))],
              "Write it as <i>y</i> = %s%s %s %s: <b>slope %s, <i>y</i>-intercept %s</b>." % (fv(m), X, "+" if ci >= 0 else "−", fv(abs(ci)), fv(m), fv(ci)))


TRI = [(3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (6, 8, 10), (8, 6, 10), (8, 15, 17), (1, 1, None), (1, 2, None), (2, 1, None)]


def one_dist(r):
    a, b, h = r.choice(TRI)
    a *= r.choice([1, -1])
    c = r.randint(-20, 20)
    if r.random() < 0.6:
        x1, y1 = r.randint(-5, 5), r.randint(-5, 5)
        v = abs(a * x1 + b * y1 + c)
        right = fv(F(v, h)) if h else (rt(a * a + b * b, 1).replace("√", "") if False else ("%s/√%d" % (num(v), a * a + b * b) if v else "0"))
        if v == 0:
            return None
        wr = [num(v), fv(F(v, a * a + b * b)), fv(F(abs(a * x1 + b * y1 - c), h)) if h and abs(a * x1 + b * y1 - c) != v else num(v + 1)]
        return T2("Find the distance of the point %s from the line %s." % (pt(x1, y1), gen(a, b, c)), right, wr,
                  "d = |a%s<sub>1</sub> + b<i>y</i><sub>1</sub> + c| ÷ √(a² + b²) = |%s| ÷ √%d = <b>%s</b>." % (X, num(a * x1 + b * y1 + c), a * a + b * b, right))
    if not h:
        return None
    c2 = c + h * r.choice([1, 2, 3, -1, -2])
    return T2("Find the distance between the parallel lines %s and %s." % (gen(a, b, c), gen(a, b, c2)), fv(F(abs(c - c2), h)),
              [num(abs(c - c2)), fv(F(abs(c + c2), h)) if c + c2 and abs(c + c2) != abs(c - c2) else num(abs(c - c2) + 1), fv(F(abs(c - c2), h * h))],
              "d = |c<sub>1</sub> − c<sub>2</sub>| ÷ √(a² + b²) = %d ÷ %d = <b>%s</b>." % (abs(c - c2), h, fv(F(abs(c - c2), h))))


U(11, 9, "straight-lines", 9, "III", "Straight Lines: Slope, Forms of the Equation and Distance", "straight lines",
  "Brief recall of two dimensional geometry from earlier classes; slope of a line and angle between two lines; various forms of equations of a line: parallel to axis, point-slope form, slope-intercept form, two-point form and intercept form; distance of a point from a line (summary of the CBSE syllabus)",
  "Class 11 Straight Lines worksheet (NCERT Chapter 9): slope, inclination, parallel and perpendicular lines, angle between lines, collinearity, forms of the equation and distance from a line. 100 questions with answers.",
  "m = (y₂ − y₁)/(x₂ − x₁) = tan θ.", "Distance from (x₁, y₁) to ax + by + c = 0 is |ax₁ + by₁ + c|/√(a² + b²).",
  "<ul><li>Slope m = (y<sub>2</sub> − y<sub>1</sub>) ÷ (x<sub>2</sub> − x<sub>1</sub>) = tan θ, where θ is the inclination.</li>"
  "<li>Parallel lines: m<sub>1</sub> = m<sub>2</sub>. Perpendicular lines: m<sub>1</sub>m<sub>2</sub> = −1. Angle: tan θ = |(m<sub>2</sub> − m<sub>1</sub>) ÷ (1 + m<sub>1</sub>m<sub>2</sub>)|.</li>"
  "<li>Forms: <i>y</i> − <i>y</i><sub>1</sub> = m(<i>x</i> − <i>x</i><sub>1</sub>); <i>y</i> = m<i>x</i> + c; <i>x</i>/a + <i>y</i>/b = 1.</li>"
  "<li>Distance of (<i>x</i><sub>1</sub>, <i>y</i><sub>1</sub>) from A<i>x</i> + B<i>y</i> + C = 0: |A<i>x</i><sub>1</sub> + B<i>y</i><sub>1</sub> + C| ÷ √(A² + B²).</li></ul>",
  [("Find the distance of (3, −5) from 3<i>x</i> − 4<i>y</i> − 26 = 0.", ["|9 + 20 − 26| ÷ √(9 + 16)", "= 3 ÷ 5"], "3/5")],
  ["Using (x₂ − x₁)/(y₂ − y₁) for the slope.", "Saying perpendicular lines have m₁m₂ = 1.", "Leaving out the modulus or the square root in the distance."],
  [("What is the slope of a vertical line?", "It is not defined."), ("What is the slope of ax + by + c = 0?", "−a/b.")],
  [("Slope and inclination", [(one_slope, 20)]),
   ("Parallel, perpendicular and collinear", [(one_pp, 20)]),
   ("Equations of a line", [(one_eq, 20)]),
   ("Distance from a line", [(one_dist, 20)]),
   ("Mixed problems", [(one_eq, 8), (one_pp, 6), (one_dist, 6)])], 911109)
