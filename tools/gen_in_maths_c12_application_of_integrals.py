# -*- coding: utf-8 -*-
"""
India Class 12 Maths, NCERT Chapter 8: Application of Integrals (CBSE Unit III Calculus)
  python3 tools/gen_in_maths_c12_application_of_integrals.py
Area under a curve as a definite integral: lines, parabolas y = kx² and y² = 4ax, √x, sin x, circles and ellipses
in standard form, areas cut off by a vertical line, and the area between a line and a parabola (own makers).
Wrong answers come from real mistakes: a negative area left as it is, πr for the area of a circle, πa² for an
ellipse, the wrong limits, and forgetting to double for a region symmetric about the x-axis.
"""
import random
from fractions import Fraction as F
from in_sr import U, T2, X, Y, rt
from in_common import num, fv
import in_common

R = random.Random(912108)
SQ = "sq units"


def A(v, extra=""):
    v = F(v)
    return (fv(v) if v != 1 or not extra else "") + extra + " " + SQ


def one_line(r):
    m, c = r.choice([1, 2, 3, 4, -1, -2]), r.randint(0, 6)
    a, b = sorted(r.sample(range(0, 7), 2))
    f = lambda x: F(m) * x + c
    if f(a) < 0 or f(b) < 0:
        return None
    area = (f(a) + f(b)) * (b - a) / 2
    yx = in_common.expr([(m, X), (c, "")])
    return T2("Find the area bounded by the line <i>y</i> = %s, the %s-axis and the lines %s = %d and %s = %d." % (yx, X, X, a, X, b), A(area),
              [A(f(b) * (b - a)), A(area * 2), A(f(b) - f(a)) if f(b) != f(a) else A(area + 1)],
              "Area = ∫<sub>%d</sub><sup>%d</sup> (%s) d%s = <b>%s</b>." % (a, b, yx, X, A(area)))


def one_par(r):
    k = r.choice(["kx2", "y24ax", "sqrt", "x24ay"])
    if k == "kx2":
        c = r.choice([1, 2, 3, 4])
        a, b = sorted(r.sample(range(0, 5), 2))
        v = F(c) * (F(b) ** 3 - F(a) ** 3) / 3
        yx = in_common.expr([(c, X + "²")])
        return T2("Find the area under <i>y</i> = %s between %s = %d and %s = %d (above the %s-axis)." % (yx, X, a, X, b, X), A(v),
                  [A(F(c) * (b * b - a * a) / 2), A(F(c) * (b ** 3 - a ** 3)), A(F(c) * (b - a) ** 3 / 3) if a else A(v + 1)],
                  "∫<sub>%d</sub><sup>%d</sup> %s d%s = [%s<sup>3</sup>/3]: <b>%s</b>." % (a, b, yx, X, ("" if c == 1 else in_common.num(c) if F(c).denominator == 1 else "(1/2)") + X, A(v)))
    if k == "y24ax":
        a = r.randint(1, 6)
        v = F(8, 3) * a * a
        return T2("Find the area of the region bounded by the parabola <i>y</i>² = %d%s and its latus rectum %s = %d." % (4 * a, X, X, a), A(v),
                  [A(F(4, 3) * a * a), A(4 * a * a), A(F(8, 3) * a)],
                  "Area = 2∫<sub>0</sub><sup>%d</sup> 2√(%d%s) d%s = (8/3)a² with a = %d: <b>%s</b>." % (a, a, X, X, a, A(v)))
    if k == "x24ay":
        a = r.randint(1, 5)
        h = r.choice([1, 2, 4]) * a
        v = 2 * F(2, 3) * h * (2 * (a * h) ** F(1, 2)) / 2 if False else None
        b = r.choice([1, 4, 9, 16])
        # area between x² = 4y and y = b: 2∫0^{2√b} (b − x²/4) dx = (8/3) b^{3/2}
        s = int(b ** 0.5)
        v = F(8, 3) * s ** 3
        return T2("Find the area bounded by the parabola %s² = 4<i>y</i> and the line <i>y</i> = %d." % (X, b), A(v), [A(F(4, 3) * s ** 3), A(F(8, 3) * b), A(4 * s ** 3)],
                  "The line meets the parabola at %s = ±%d. Area = 2∫<sub>0</sub><sup>%d</sup> (%d − %s²/4) d%s = <b>%s</b>." % (X, 2 * s, 2 * s, b, X, X, A(v)))
    a = r.choice([1, 4, 9, 16, 25])
    s = int(a ** 0.5)
    v = F(2, 3) * s ** 3
    return T2("Find the area under <i>y</i> = √%s between %s = 0 and %s = %d." % (X, X, X, a), A(v), [A(F(1, 2) * a), A(F(3, 2) * s), A(F(2, 3) * a)],
              "∫<sub>0</sub><sup>%d</sup> %s<sup>1/2</sup> d%s = (2/3)%s<sup>3/2</sup> = (2/3)(%d) = <b>%s</b>." % (a, X, X, X, s ** 3, A(v)))


def one_circle(r):
    k = r.choice(["full", "quad", "ell", "ellq"])
    a = r.randint(2, 8)
    if k == "full":
        return T2("Find the area enclosed by the circle %s² + <i>y</i>² = %d." % (X, a * a), A(a * a, "π"), [A(2 * a, "π"), A(a, "π"), A(a * a * 4, "")],
                  "Area = 4∫<sub>0</sub><sup>%d</sup> √(%d − %s²) d%s = πr² = <b>%dπ sq units</b>." % (a, a * a, X, X, a * a))
    if k == "quad":
        v = F(a * a, 4)
        return T2("Find the area of the region in the first quadrant enclosed by the %s-axis, the line %s = <i>y</i> and the circle %s² + <i>y</i>² = %d." % (X, X, X, a * a) if False else
                  "Find the area of the part of the circle %s² + <i>y</i>² = %d that lies in the first quadrant." % (X, a * a), A(v, "π"), [A(a * a, "π"), A(F(a * a, 2), "π"), A(F(a, 2), "π")],
                  "It is a quarter of the circle: πr²/4 = <b>%s sq units</b>." % (fv(v) + "π"))
    b = r.choice([k_ for k_ in range(2, 9) if k_ != a])
    if k == "ell":
        return T2("Find the area enclosed by the ellipse %s²/%d + <i>y</i>²/%d = 1." % (X, a * a, b * b), A(a * b, "π"), [A(a * a * b * b, "π"), A(max(a, b) ** 2, "π"), A(2 * a * b, "π")],
                  "Area = 4∫<sub>0</sub><sup>%d</sup> (%d/%d)√(%d − %s²) d%s = πab = π × %d × %d = <b>%dπ sq units</b>." % (a, b, a, a * a, X, X, a, b, a * b))
    return T2("Find the area of the part of the ellipse %s²/%d + <i>y</i>²/%d = 1 in the first quadrant." % (X, a * a, b * b), A(F(a * b, 4), "π"), [A(a * b, "π"), A(F(a * b, 2), "π"), A(F(a * a, 4), "π")],
              "A quarter of πab: <b>%s sq units</b>." % (fv(F(a * b, 4)) + "π"))


def one_between(r):
    k = r.choice(["xx2", "kx", "sin", "horiz", "abs"])
    if k == "horiz":
        c = r.randint(1, 6)
        v = F(4, 3) * c ** 3
        return T2("Find the area enclosed between the parabola <i>y</i> = %s² and the line <i>y</i> = %d." % (X, c * c), A(v), [A(F(2, 3) * c ** 3), A(2 * c ** 3), A(F(4, 3) * c * c)],
                  "They meet at %s = ±%d. Area = ∫<sub>−%d</sub><sup>%d</sup> (%d − %s²) d%s = <b>%s</b>." % (X, c, c, c, c * c, X, X, A(v)))
    if k == "abs":
        c = r.randint(1, 9)
        return T2("Find the area enclosed between <i>y</i> = |%s| and the line <i>y</i> = %d." % (X, c), A(c * c), [A(F(c * c, 2)), A(2 * c * c), A(2 * c)],
                  "The region is a triangle with base %d and height %d: area = ½ × %d × %d = <b>%s</b>." % (2 * c, c, 2 * c, c, A(c * c)))
    if k == "xx2":
        m = r.randint(1, 6)
        v = F(m ** 3, 6)
        return T2("Find the area enclosed between the parabola <i>y</i> = %s² and the line <i>y</i> = %s%s." % (X, "" if m == 1 else m, X), A(v),
                  [A(F(m ** 3, 3)), A(F(m * m, 2)), A(F(m ** 3, 2))],
                  "They meet at %s = 0 and %s = %d. Area = ∫<sub>0</sub><sup>%d</sup> (%s%s − %s²) d%s = %d³/6 = <b>%s</b>." % (X, X, m, m, "" if m == 1 else m, X, X, X, m, A(v)))
    if k == "kx":
        a = r.randint(1, 4)
        # y² = 4ax and y = 2x... area between y = x and y² = 4ax: meet at x = 0, 4a; area = 8a²/3
        v = F(8, 3) * a * a
        return T2("Find the area enclosed between the parabola <i>y</i>² = %d%s and the line <i>y</i> = %s." % (4 * a, X, X), A(v), [A(F(16, 3) * a * a), A(8 * a * a), A(F(4, 3) * a * a)],
                  "They meet at %s = 0 and %s = %d. Area = ∫<sub>0</sub><sup>%d</sup> (2√(%d%s) − %s) d%s = <b>%s</b>." % (X, X, 4 * a, 4 * a, a, X, X, X, A(v)))
    n = r.choice([1, 2])
    return T2("Find the area between <i>y</i> = sin %s and the %s-axis from %s = 0 to %s = %s." % (X, X, X, X, "π" if n == 1 else "2π"), A(2 * n), [A(0), A(n), A(4 * n) if n == 1 else A(2)],
              "Area = %s∫<sub>0</sub><sup>π</sup> sin %s d%s = %s × 2 = <b>%s</b>. (Area is never negative, so the part below the axis counts as positive.)" % ("" if n == 1 else "2", X, X, n, A(2 * n)))


U(12, 8, "application-of-integrals", 8, "Ca", "Application of Integrals: Area under Curves, Circles and Ellipses", "application of integrals",
  "Applications in finding the area under simple curves, especially lines, circles, parabolas and ellipses (in standard form only) (summary of the CBSE syllabus)",
  "Class 12 Application of Integrals worksheet (NCERT Chapter 8): area under lines and parabolas, circles, ellipses, areas cut by a line and areas between curves. 100 questions with answers.",
  "Area = ∫ₐᵇ y dx, taken as positive.", "Circle πr², ellipse πab.",
  "<ul><li>The area between <i>y</i> = f(<i>x</i>), the <i>x</i>-axis and <i>x</i> = a, <i>x</i> = b is ∫<sub>a</sub><sup>b</sup> |f(<i>x</i>)| d<i>x</i>.</li>"
  "<li>Use symmetry: for a circle or ellipse, find the first-quadrant area and multiply by 4.</li>"
  "<li>Circle <i>x</i>² + <i>y</i>² = a²: area πa². Ellipse <i>x</i>²/a² + <i>y</i>²/b² = 1: area πab.</li>"
  "<li>Area between two curves: ∫ (upper − lower) d<i>x</i> between the points where they meet.</li></ul>",
  [("Find the area bounded by <i>y</i>² = 9<i>x</i>, <i>x</i> = 2, <i>x</i> = 4 and the <i>x</i>-axis in the first quadrant.", ["∫<sub>2</sub><sup>4</sup> 3√<i>x</i> d<i>x</i> = 2[<i>x</i><sup>3/2</sup>] from 2 to 4", "= 2(8 − 2√2)"], "16 − 4√2 sq units")],
  ["Leaving an area negative when the curve is below the axis.", "Using πa² for an ellipse instead of πab.", "Forgetting to double the area of a region that is symmetric about the x-axis."],
  [("Can an area be negative?", "No. If the curve is below the axis, take the absolute value of the integral."),
   ("Do I need to draw a sketch?", "Yes; it shows the limits and which curve is on top.")],
  [("Area under a line", [(one_line, 20)]),
   ("Parabolas and √x", [(one_par, 20)]),
   ("Circles and ellipses", [(one_circle, 20)]),
   ("Area between curves", [(one_between, 14), (one_par, 6)]),
   ("Mixed problems", [(one_line, 6), (one_circle, 6), (one_between, 4), (one_par, 4)])], 912108)
