# -*- coding: utf-8 -*-
"""
US Geometry: Slopes of Parallel and Perpendicular Lines (Common Core G-GPE.B.5)
  python3 tools/gen_us_math_ge_slopes_of_parallel_and_perpendicular_lines.py
Parallel and perpendicular slopes, classifying pairs of lines, writing equations of parallel and
perpendicular lines through a point, and using slopes to prove right angles, parallelograms and
perpendicular bisectors.
Wrong answers come from real mistakes: taking only the reciprocal or only the opposite, reading the slope
from standard form without solving for y, and calling lines with the same slope and intercept parallel.
"""
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, fig, num, MINUS, fr, expr
from g8_common import grid_svg
from us_geo import RED, GREEN, BLUE

R = random.Random(92701)
X, Y = "<i>x</i>", "<i>y</i>"
SLOPES = [2, 3, 4, 5, -2, -3, -4, F(1, 2), F(1, 3), F(2, 3), F(3, 4), F(-1, 2), F(-2, 3), F(-3, 4), F(5, 2), F(-4, 5), F(3, 2), -1, 1]


def sf(v):
    v = F(v)
    if v.denominator == 1:
        return num(v)
    s = fr(abs(v.numerator), v.denominator)
    return (MINUS + s) if v < 0 else s


def si(m, b):
    m, b = F(m), F(b)
    if m == 0:
        return "%s = %s" % (Y, sf(b))
    t = X if m == 1 else (MINUS + X if m == -1 else sf(m) + X)
    if b == 0:
        return "%s = %s" % (Y, t)
    return "%s = %s %s %s" % (Y, t, "+" if b > 0 else MINUS, sf(abs(b)))


def pt(x, y):
    return "(%s, %s)" % (num(x), num(y))


def std(a, b, c):
    return "%s = %s" % (expr([(a, X), (b, Y)]), num(c))


def slope(p, q):
    return F(q[1] - p[1], q[0] - p[0])


# ------------------------------------------------------------ set 1: parallel and perpendicular slopes
def one_sl(r):
    m = F(r.choice(SLOPES))
    kind = r.choice(["par", "perp", "perp", "pts"])
    if kind == "pts":
        x1, y1 = r.randint(-6, 6), r.randint(-6, 6)
        dx = r.choice([1, 2, 3, 4, -2, -3])
        dy = m * dx
        if dy.denominator != 1:
            return None
        x2, y2 = x1 + dx, y1 + int(dy)
        want = r.choice(["parallel", "perpendicular"])
        ans = m if want == "parallel" else -1 / m
        q = "A line passes through %s and %s. What is the slope of a line %s to it?" % (B(pt(x1, y1)), B(pt(x2, y2)), want)
        wr = [sf(-1 / m) if want == "parallel" else sf(m), sf(-m), sf(1 / m), sf(F(dx, int(dy)) if dy else 0)]
        e = "Slope = (%s %s %s) ÷ (%s %s %s) = %s. %s" % (
            num(y2), MINUS, "(%s)" % num(y1) if y1 < 0 else num(y1), num(x2), MINUS, "(%s)" % num(x1) if x1 < 0 else num(x1), sf(m),
            "Parallel lines have the same slope: <b>%s</b>." % sf(ans) if want == "parallel" else "Perpendicular slopes are negative reciprocals: <b>%s</b>." % sf(ans))
        return T(q, sf(ans), [w for w in dict.fromkeys(wr) if w != sf(ans)][:3], e)
    b = r.randint(-8, 8)
    if kind == "par":
        q = "What is the slope of a line parallel to %s?" % B(si(m, b))
        ans = m
        wr = [sf(-1 / m), sf(-m), sf(1 / m), num(b) if b else "0"]
        e = "Parallel lines have <b>the same slope</b>: %s." % sf(m)
    else:
        q = "What is the slope of a line perpendicular to %s?" % B(si(m, b))
        ans = -1 / m
        wr = [sf(m), sf(-m), sf(1 / m)]
        e = "Perpendicular slopes are negative reciprocals: flip %s and change the sign. <b>%s</b>. Check: %s × %s = %s1." % (
            sf(m), sf(ans), sf(m), "(%s)" % sf(ans) if ans < 0 else sf(ans), MINUS)
    return T(q, sf(ans), [w for w in dict.fromkeys(wr) if w != sf(ans)][:3], e)


# ------------------------------------------------------------ set 2: parallel, perpendicular or neither
def as_std(m, b):
    """write y = mx + b as Ax + By = C with integers, A > 0 (or A = 0, B > 0)"""
    d = (F(m).denominator * F(b).denominator) // __import__("math").gcd(F(m).denominator, F(b).denominator)
    A, Bc, C = -m * d, d, b * d
    if A < 0 or (A == 0 and Bc < 0):
        A, Bc, C = -A, -Bc, -C
    return std(int(A), int(Bc), int(C))


def one_cls(r):
    m = F(r.choice(SLOPES))
    b1 = r.randint(-7, 7)
    kind = r.choice(["parallel", "perpendicular", "neither", "parallel", "perpendicular", "neither"])
    if kind == "parallel":
        m2, b2 = m, b1 + r.choice([-5, -3, -2, 2, 3, 4])
    elif kind == "perpendicular":
        m2, b2 = -1 / m, r.randint(-7, 7)
    else:
        m2 = r.choice([1 / m, -m, m + 1]) if m != 1 and m != -1 else m + 2
        b2 = r.randint(-7, 7)
    l1 = si(m, b1)
    l2 = as_std(m2, b2) if r.random() < 0.5 else si(m2, b2)
    q = "Are these lines parallel, perpendicular, or neither? %s and %s" % (B(l1), B(l2))
    e = "Slopes: %s and %s. " % (sf(m), sf(m2))
    if "=" in l2 and not l2.startswith(Y):
        e = "Solve the second equation for <i>y</i>: %s. " % si(m2, b2) + e
    e += {"parallel": "The slopes are equal (and the intercepts differ), so the lines are <b>parallel</b>.",
          "perpendicular": "The slopes multiply to %s1, so the lines are <b>perpendicular</b>." % MINUS,
          "neither": "The slopes are not equal and do not multiply to %s1, so the answer is <b>neither</b>." % MINUS}[kind]
    if kind == "neither" and m2 == 1 / m:
        e += " Reciprocals are not enough; the signs must also be opposite."
    if kind == "neither" and m2 == -m:
        e += " Opposite slopes are not enough; the numbers must also be flipped."
    return T(q, kind.capitalize(), [x.capitalize() for x in ["parallel", "perpendicular", "neither", "the same line"] if x != kind], e)


# ------------------------------------------------------------ set 3: equation of a parallel line
def one_par(r):
    m = F(r.choice(SLOPES))
    b = r.randint(-6, 6)
    x1 = r.choice([-6, -4, -3, -2, 2, 3, 4, 6])
    y1 = r.randint(-6, 6)
    bb = F(y1) - m * x1
    if bb.denominator > 1 or bb == b:
        return None
    given = B(si(m, b)) if r.random() < 0.7 else B(as_std(m, b))
    q = "Write an equation of the line that passes through %s and is <b>parallel</b> to %s." % (B(pt(x1, y1)), given)
    right = si(m, bb)
    wr = [si(m, b), si(-1 / m, F(y1) + 1 / m * x1), si(m, F(y1) + m * x1), si(m, F(x1) - m * y1)]
    e = ("A parallel line has the same slope, %s. Substitute the point: %s = %s(%s) + <i>b</i>, so <i>b</i> = %s. <b>%s</b>." % (
        sf(m), num(y1), sf(m), num(x1), sf(bb), right))
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)


# ------------------------------------------------------------ set 4: equation of a perpendicular line
def one_perp(r):
    m = F(r.choice(SLOPES))
    b = r.randint(-6, 6)
    p = -1 / m
    x1 = r.choice([-6, -4, -3, -2, 2, 3, 4, 6])
    y1 = r.randint(-6, 6)
    bb = F(y1) - p * x1
    if bb.denominator > 1:
        return None
    given = B(si(m, b)) if r.random() < 0.7 else B(as_std(m, b))
    q = "Write an equation of the line that passes through %s and is <b>perpendicular</b> to %s." % (B(pt(x1, y1)), given)
    right = si(p, bb)
    wr = [si(m, F(y1) - m * x1), si(1 / m, F(y1) - x1 / m), si(-m, F(y1) + m * x1), si(p, b)]
    e = ("The given slope is %s, so the perpendicular slope is %s. Substitute the point: %s = %s(%s) + <i>b</i>, so <i>b</i> = %s. <b>%s</b>." % (
        sf(m), sf(p), num(y1), sf(p), num(x1), sf(bb), right))
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)


# ------------------------------------------------------------ set 5: proofs with slopes
def one_proof(r):
    kind = r.choice(["right", "right", "pgram", "bis", "trap"])
    if kind == "right":
        A = (r.randint(-5, 0), r.randint(-5, 0))
        u = (r.choice([1, 2, 3, 4]), r.choice([1, 2, 3, -1, -2]))
        k = r.choice([1, 2])
        Bp = (A[0] + u[0] * 2, A[1] + u[1] * 2)
        good = r.random() < 0.6
        v = (-u[1] * k, u[0] * k) if good else (-u[1] * k + 1, u[0] * k)
        C = (A[0] + v[0], A[1] + v[1])
        if max(abs(c) for p in (A, Bp, C) for c in p) > 7 or v[0] == 0 or u[0] == 0:
            return None
        m1, m2 = slope(A, Bp), slope(A, C)
        svg = grid_svg(-7, 7, points=[(A[0], A[1], "A", RED), (Bp[0], Bp[1], "B", RED), (C[0], C[1], "C", RED)],
                       polys=[([A, Bp, C], "#cfe6d6", GREEN)], unit=17, label="triangle ABC")
        q = "Triangle ABC has A%s, B%s and C%s. Is angle A a right angle?%s" % (pt(*A), pt(*Bp), pt(*C), fig(svg))
        if m1 * m2 == -1:
            right = "Yes, because the slopes of AB and AC multiply to %s1" % MINUS
            e = "Slope AB = %s, slope AC = %s. %s × %s = %s1, so AB ⟂ AC. <b>Yes</b>." % (sf(m1), sf(m2), sf(m1), "(%s)" % sf(m2) if m2 < 0 else sf(m2), MINUS)
        else:
            right = "No, because the slopes of AB and AC do not multiply to %s1" % MINUS
            e = "Slope AB = %s, slope AC = %s. Their product is %s, not %s1. <b>No</b>." % (sf(m1), sf(m2), sf(m1 * m2), MINUS)
        wr = ["Yes, because the slopes of AB and AC multiply to %s1" % MINUS, "No, because the slopes of AB and AC do not multiply to %s1" % MINUS,
              "Yes, because AB and AC have the same slope", "No, because AB is longer than AC"]
        return T(q, right, [w for w in wr if w != right], e)
    if kind == "pgram":
        A = (r.randint(-6, -2), r.randint(-6, -2))
        u = (r.randint(3, 6), r.randint(-1, 2))
        v = (r.randint(1, 3), r.randint(3, 5))
        D = (A[0] + v[0], A[1] + v[1])
        Bp = (A[0] + u[0], A[1] + u[1])
        C = (Bp[0] + v[0], Bp[1] + v[1])
        if max(abs(c) for p in (A, Bp, C, D) for c in p) > 7:
            return None
        names = "ABCD"
        svg = grid_svg(-7, 7, points=[(p[0], p[1], n, RED) for p, n in zip((A, Bp, C, D), names)], polys=[([A, Bp, C, D], "#cfe6d6", GREEN)], unit=17, label="quadrilateral ABCD")
        q = "Quadrilateral ABCD has A%s, B%s, C%s and D%s. Which statement uses slopes to show it is a parallelogram?%s" % (pt(*A), pt(*Bp), pt(*C), pt(*D), fig(svg))
        s1, s2 = slope(A, Bp), slope(A, D)
        right = "Slope AB = slope DC = %s and slope AD = slope BC = %s" % (sf(s1), sf(s2))
        wr = ["Slope AB = slope BC = %s" % sf(s1), "Slope AB × slope AD = %s1" % MINUS, "Slope AC = slope BD"]
        e = "A parallelogram has two pairs of parallel sides, and parallel sides have equal slopes. <b>%s</b>." % right
        return T(q, right, wr, e)
    if kind == "trap":
        q = "A quadrilateral has side slopes of %s, %s, %s and %s, in order around the shape. What is the best name for it?" % tuple(
            sf(x) for x in r.choice([(F(1, 2), -2, F(1, 2), -2), (F(2, 3), F(-3, 2), F(2, 3), F(-3, 2)), (3, F(-1, 3), 3, F(-1, 3))]))
        return T(q, "Rectangle", ["Trapezoid", "Rhombus", "Kite"],
                 "Opposite sides have equal slopes (parallel), and neighbors have slopes that multiply to %s1 (perpendicular). Four right angles: <b>rectangle</b>." % MINUS)
    A = (r.randint(-6, 2), r.randint(-6, 2))
    d = (r.choice([2, 4, 6, -2, -4]), r.choice([2, 4, -2, -4, 6]))
    Bp = (A[0] + d[0], A[1] + d[1])
    M = (A[0] + d[0] // 2, A[1] + d[1] // 2)
    m = slope(A, Bp)
    p = -1 / m
    bb = F(M[1]) - p * M[0]
    if bb.denominator > 1:
        return None
    q = "Find the perpendicular bisector of the segment from %s to %s." % (B(pt(*A)), B(pt(*Bp)))
    right = si(p, bb)
    wr = [si(m, F(M[1]) - m * M[0]), si(p, F(A[1]) - p * A[0]), si(-m, F(M[1]) + m * M[0])]
    e = "Midpoint: %s. Slope of the segment: %s, so the perpendicular slope is %s. %s = %s(%s) + <i>b</i>, <i>b</i> = %s. <b>%s</b>." % (
        pt(*M), sf(m), sf(p), num(M[1]), sf(p), num(M[0]), sf(bb), right)
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)


def build():
    sets = [S("Parallel and perpendicular slopes", collect(one_sl, 20, R)),
            S("Parallel, perpendicular, or neither", collect(one_cls, 20, R)),
            S("Equations of parallel lines", collect(one_par, 20, R)),
            S("Equations of perpendicular lines", collect(one_perp, 20, R)),
            S("Prove it with slopes", collect(one_proof, 20, R))]
    body = lesson(
        "<p><b>Parallel</b> lines have <b>the same slope</b> (and different <i>y</i>-intercepts).</p>"
        "<p><b>Perpendicular</b> lines have slopes that are <b>negative reciprocals</b>: flip the fraction and change the sign. "
        "Their product is %s1. The perpendicular slope to %s is %s.</p>"
        "<p>To write the equation of a parallel or perpendicular line through a point, find the slope first, then substitute the point "
        "into <i>y</i> = <i>mx</i> + <i>b</i> to find <i>b</i>. If a line is in standard form, solve for <i>y</i> before reading the slope.</p>" % (MINUS, fr(2, 3), MINUS + fr(3, 2)),
        [("Write the line through (4, 1) perpendicular to <i>y</i> = 2<i>x</i> %s 5." % MINUS,
          ["Perpendicular slope: %s" % (MINUS + fr(1, 2)), "1 = %s(4) + <i>b</i>, so <i>b</i> = 3" % (MINUS + fr(1, 2))], "<i>y</i> = %s<i>x</i> + 3" % (MINUS + fr(1, 2))),
         ("Are 3<i>x</i> + 2<i>y</i> = 8 and <i>y</i> = %s<i>x</i> + 1 parallel, perpendicular, or neither?" % fr(2, 3),
          ["Solve for <i>y</i>: <i>y</i> = %s<i>x</i> + 4" % (MINUS + fr(3, 2)), "%s × %s = %s1" % (MINUS + fr(3, 2), fr(2, 3), MINUS)], "Perpendicular")],
        ["Taking only the reciprocal (2 → ½) or only the opposite (2 → %s2). Do both: 2 → %s½." % (MINUS, MINUS),
         "Reading the slope of 3<i>x</i> + 2<i>y</i> = 8 as 3. Solve for <i>y</i> first: the slope is %s." % (MINUS + fr(3, 2)),
         "Using the given line's <i>y</i>-intercept for the new line. Find a new <i>b</i> with the point.",
         "Calling two equations for the same line parallel. Parallel lines never meet."])
    faq = [("How do you know if two lines are perpendicular?", "Their slopes are negative reciprocals, so the product of the slopes is −1. A vertical and a horizontal line are also perpendicular."),
           ("What is the slope of a line parallel to y = 3x + 2?", "3. Parallel lines have the same slope."),
           ("What is the slope of a line perpendicular to y = 3x + 2?", "−1/3, the negative reciprocal of 3."),
           ("How do you write the equation of a perpendicular line through a point?",
            "Find the negative reciprocal of the given slope, then substitute the point into y = mx + b to solve for b.")]
    make("slopes-of-parallel-and-perpendicular-lines", 7, "G-GPE.B.5",
         "Slopes of Parallel and Perpendicular Lines",
         "Parallel and Perpendicular Lines Worksheet: Slopes and Equations (Geometry) | 100 Questions",
         "Parallel and Perpendicular Slopes",
         "Prove the slope criteria for parallel and perpendicular lines and use them to solve geometric problems (e.g., find the equation of a line parallel or perpendicular to a given line that passes through a given point).",
         "Free Geometry worksheet on parallel and perpendicular slopes: negative reciprocals, writing equations through a point, and proofs with slopes. 100 questions with answers.",
         "Parallel lines: same slope. Perpendicular lines: negative reciprocal slopes.",
         "The slopes of perpendicular lines multiply to −1.",
         body, faq, sets, R, domain="Parallel and Perpendicular Lines", grade="geometry")


if __name__ == "__main__":
    build()
