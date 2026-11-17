# -*- coding: utf-8 -*-
"""
US Geometry: Equations of Circles (Common Core G-GPE.A.1)
  python3 tools/gen_us_math_ge_equations_of_circles.py
Writing the equation from the center and radius, reading the center and radius, completing the square,
writing the equation from a point or a diameter, and deciding whether a point is on, inside or outside.
Wrong answers come from real mistakes: keeping the signs of the center inside the parentheses, using r
instead of r², halving instead of taking the square root, and forgetting to add to both sides when
completing the square.
"""
import math
import random
from us_hs import B, S, make, lesson, collect, T, fig, num, MINUS, People
from g8_common import grid_svg
from us_geo import RED, GREEN, BLUE

R = random.Random(94001)
X, Y = "<i>x</i>", "<i>y</i>"


def sg(n):
    return num(n) if n >= 0 else MINUS + num(-n)


def pt(p):
    return "(%s, %s)" % (sg(p[0]), sg(p[1]))


def part(var, h):
    if h == 0:
        return "%s²" % var
    return "(%s %s %s)²" % (var, MINUS if h > 0 else "+", num(abs(h)))


def eq(h, k, r2):
    return "%s + %s = %s" % (part(X, h), part(Y, k), num(r2))


def rad(n):
    a = 1
    for t in range(math.isqrt(n), 1, -1):
        if n % (t * t) == 0:
            a = t
            break
    b = n // (a * a)
    return num(a) if b == 1 else ("" if a == 1 else num(a)) + "√" + num(b)


def circle_svg(h, k, r):
    lo = min(h - r, k - r, -2) - 1
    hi = max(h + r, k + r, 2) + 1
    n = 48
    pts = [(h + r * math.cos(2 * math.pi * i / n), k + r * math.sin(2 * math.pi * i / n)) for i in range(n)]
    return grid_svg(lo, hi, points=[(h, k, "", RED)], polys=[(pts, "#ffffff", BLUE)], unit=max(12, min(20, 280 // (hi - lo))), label="a circle on the coordinate plane")


# ------------------------------------------------------------ set 1: write the equation
def one_write(r):
    h, k = r.randint(-8, 8), r.randint(-8, 8)
    rr = r.randint(1, 12)
    q = "Write the equation of the circle with center %s and radius %d." % (B(pt((h, k))), rr)
    right = eq(h, k, rr * rr)
    wr = [eq(-h, -k, rr * rr), eq(h, k, rr), eq(k, h, rr * rr) if h != k else eq(h, k, 2 * rr)]
    e = "Standard form: (<i>x</i> %s <i>h</i>)² + (<i>y</i> %s <i>k</i>)² = <i>r</i>². With center %s and <i>r</i>² = %d: <b>%s</b>." % (MINUS, MINUS, pt((h, k)), rr * rr, right)
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)


# ------------------------------------------------------------ set 2: read the center and radius
def one_read(r):
    h, k = r.randint(-9, 9), r.randint(-9, 9)
    r2 = r.choice([n * n for n in range(2, 13)] + [8, 12, 18, 20, 27, 50])
    q = "Find the center and radius of %s." % B(eq(h, k, r2))
    rs = rad(r2)
    right = "Center %s, radius %s" % (pt((h, k)), rs)
    wr = ["Center %s, radius %s" % (pt((-h, -k)), rs), "Center %s, radius %s" % (pt((h, k)), num(r2)),
          "Center %s, radius %s" % (pt((h, k)), num(r2 / 2))]
    if h == 0 and k == 0:
        return None
    e = "Change the signs inside the parentheses: center %s. The right side is <i>r</i>² = %d, so <i>r</i> = √%d = <b>%s</b>." % (pt((h, k)), r2, r2, rs)
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)


# ------------------------------------------------------------ set 3: complete the square
def one_cs(r):
    h, k = r.randint(-7, 7), r.randint(-7, 7)
    if h == 0 or k == 0:
        return None
    rr = r.randint(1, 9)
    D, E = -2 * h, -2 * k
    Fc = h * h + k * k - rr * rr
    lhs = "%s² + %s² %s %s %s %s" % (X, Y, ("+ %d%s" % (D, X)) if D > 0 else ("%s %d%s" % (MINUS, -D, X)), "", ("+ %d%s" % (E, Y)) if E > 0 else ("%s %d%s" % (MINUS, -E, Y)), "")
    lhs = "%s² %s %s² %s" % (X, ("+ %d%s" % (D, X)) if D > 0 else ("%s %d%s" % (MINUS, -D, X)), "+ " + Y, ("+ %d%s" % (E, Y)) if E > 0 else ("%s %d%s" % (MINUS, -E, Y)))
    lhs = "%s² %s + %s² %s" % (X, ("+ %d%s" % (D, X)) if D > 0 else ("%s %d%s" % (MINUS, -D, X)), Y, ("+ %d%s" % (E, Y)) if E > 0 else ("%s %d%s" % (MINUS, -E, Y)))
    rhs = -Fc
    if Fc == 0:
        return None
    full = "%s = %s" % (lhs, sg(rhs))
    q = "Find the center and radius of the circle %s." % B(full)
    right = "Center %s, radius %d" % (pt((h, k)), rr)
    bad_r2 = rhs
    wr = ["Center %s, radius %d" % (pt((-h, -k)), rr), "Center %s, radius %s" % (pt((D, E)), num(rr)),
          "Center %s, radius %s" % (pt((h, k)), rad(bad_r2) if bad_r2 > 0 else num(rr + 2))]
    e = ("Complete the square for each variable: add (%s ÷ 2)² = %d and (%s ÷ 2)² = %d to both sides. "
         "(%s)² + (%s)²... becomes %s. <b>%s</b>." % (sg(D), h * h, sg(E), k * k, "", "", eq(h, k, rr * rr), right))
    e = ("Complete the square: add (%s ÷ 2)² = %d and (%s ÷ 2)² = %d to both sides, so the right side becomes %s + %d + %d = %d. "
         "The equation is %s. <b>%s</b>." % (sg(D), h * h, sg(E), k * k, sg(rhs), h * h, k * k, rr * rr, eq(h, k, rr * rr), right))
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)


# ------------------------------------------------------------ set 4: from a point or a diameter
def one_pt(r):
    if r.random() < 0.5:
        h, k = r.randint(-6, 6), r.randint(-6, 6)
        dx, dy = r.randint(-6, 6), r.randint(-6, 6)
        if dx == 0 and dy == 0:
            return None
        P = (h + dx, k + dy)
        r2 = dx * dx + dy * dy
        q = "A circle has center %s and passes through %s. Write its equation." % (B(pt((h, k))), B(pt(P)))
        right = eq(h, k, r2)
        wr = [eq(h, k, abs(dx) + abs(dy)), eq(-h, -k, r2), eq(h, k, int(math.sqrt(r2)) if math.isqrt(r2) ** 2 == r2 else r2 * 2)]
        e = "The radius is the distance from the center to the point: <i>r</i>² = %s² + %s² = %d. <b>%s</b>." % (
            "(%s)" % sg(dx) if dx < 0 else sg(dx), "(%s)" % sg(dy) if dy < 0 else sg(dy), r2, right)
        return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)
    h, k = r.randint(-6, 6), r.randint(-6, 6)
    dx, dy = r.randint(-5, 5), r.randint(-5, 5)
    if dx == 0 and dy == 0:
        return None
    A, Bp = (h - dx, k - dy), (h + dx, k + dy)
    r2 = dx * dx + dy * dy
    q = "The endpoints of a diameter are %s and %s. Write the equation of the circle." % (B(pt(A)), B(pt(Bp)))
    right = eq(h, k, r2)
    wr = [eq(h, k, 4 * r2), eq(-h, -k, r2), eq(A[0], A[1], 4 * r2)]
    e = "The center is the midpoint: %s. The radius is half the diameter, so <i>r</i>² = %s² + %s² = %d. <b>%s</b>." % (
        pt((h, k)), "(%s)" % sg(dx) if dx < 0 else sg(dx), "(%s)" % sg(dy) if dy < 0 else sg(dy), r2, right)
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)


# ------------------------------------------------------------ set 5: graphs, points and problems
def one_mix(r):
    kind = r.choice(["graph", "graph", "where", "where", "word"])
    if kind == "graph":
        h, k = r.randint(-4, 4), r.randint(-4, 4)
        rr = r.randint(2, 4)
        q = "Which equation matches the circle?%s" % fig(circle_svg(h, k, rr))
        right = eq(h, k, rr * rr)
        wr = [eq(-h, -k, rr * rr), eq(h, k, rr), eq(k, h, rr * rr) if h != k else eq(h, k, (rr + 1) ** 2)]
        if h == 0 and k == 0:
            return None
        return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3],
                 "The center is %s and the radius is %d, so <i>r</i>² = %d: <b>%s</b>." % (pt((h, k)), rr, rr * rr, right))
    if kind == "where":
        h, k = r.randint(-5, 5), r.randint(-5, 5)
        rr = r.choice([5, 10, 13])
        trip = {5: [(3, 4), (4, 3), (5, 0)], 10: [(6, 8), (8, 6), (10, 0)], 13: [(5, 12), (12, 5), (13, 0)]}[rr]
        where = r.choice(["on", "inside", "outside"])
        dx, dy = r.choice(trip)
        if where == "inside":
            dx, dy = dx - 1 if dx > 1 else dx, dy - 1 if dy > 1 else dy
        elif where == "outside":
            dx, dy = dx + 1, dy + 1
        dx *= r.choice([1, -1])
        dy *= r.choice([1, -1])
        P = (h + dx, k + dy)
        d2 = dx * dx + dy * dy
        q = "Is the point %s on, inside, or outside the circle %s?" % (B(pt(P)), B(eq(h, k, rr * rr)))
        right = {"on": "On the circle", "inside": "Inside the circle", "outside": "Outside the circle"}[where]
        cmp = "=" if d2 == rr * rr else ("&lt;" if d2 < rr * rr else "&gt;")
        e = "Substitute the point: %s² + %s² = %d, and %d %s %d. <b>%s</b>." % (
            "(%s)" % sg(dx) if dx < 0 else sg(dx), "(%s)" % sg(dy) if dy < 0 else sg(dy), d2, d2, cmp, rr * rr, right)
        return T(q, right, [x for x in ["On the circle", "Inside the circle", "Outside the circle", "It cannot be decided"] if x != right], e)
    items = []
    h, k = r.randint(-8, 8), r.randint(-8, 8)
    rr = r.choice([5, 8, 10, 12, 15, 20])
    obj = r.choice([("A cell tower", "covers a circular area with a radius of %d miles" % rr, "miles"),
                    ("A lawn sprinkler", "waters a circle with a radius of %d feet" % rr, "feet"),
                    ("A radio station", "reaches listeners up to %d miles away" % rr, "miles")])
    q = "%s at %s on a map grid %s. Which inequality describes the points it reaches?" % (obj[0], pt((h, k)), obj[1])
    right = eq(h, k, rr * rr).replace(" = ", " ≤ ")
    wr = [eq(h, k, rr).replace(" = ", " ≤ "), eq(h, k, rr * rr).replace(" = ", " ≥ "), eq(-h, -k, rr * rr).replace(" = ", " ≤ ")]
    if h == 0 and k == 0:
        return None
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3],
             "Points within %d %s of %s have a distance squared of at most %d: <b>%s</b>." % (rr, obj[2], pt((h, k)), rr * rr, right))


def build():
    sets = [S("Write the equation", collect(one_write, 20, R)),
            S("Find the center and radius", collect(one_read, 20, R)),
            S("Complete the square", collect(one_cs, 20, R)),
            S("From a point or a diameter", collect(one_pt, 20, R)),
            S("Graphs, points and problems", collect(one_mix, 20, R))]
    body = lesson(
        "<p>A circle is every point at distance <i>r</i> from its center (<i>h</i>, <i>k</i>). The distance formula gives the <b>standard form</b>:</p>"
        "<p><b>(<i>x</i> %s <i>h</i>)² + (<i>y</i> %s <i>k</i>)² = <i>r</i>²</b></p>"
        "<p>The signs inside the parentheses are the opposite of the center: (<i>x</i> + 3)² means <i>h</i> = %s3. The right side is <i>r</i>², not <i>r</i>.</p>"
        "<p>If the equation is expanded, group the <i>x</i>-terms and the <i>y</i>-terms and <b>complete the square</b> for each, adding the same numbers to both sides.</p>" % (MINUS, MINUS, MINUS),
        [("Find the center and radius of <i>x</i>² + 6<i>x</i> + <i>y</i>² %s 4<i>y</i> = 12." % MINUS,
          ["Add 9 and 4 to both sides", "(<i>x</i> + 3)² + (<i>y</i> %s 2)² = 25" % MINUS], "Center (%s3, 2), radius 5" % MINUS),
         ("Write the circle with center (2, %s1) through (5, 3)." % MINUS, ["<i>r</i>² = 3² + 4² = 25"], "(<i>x</i> %s 2)² + (<i>y</i> + 1)² = 25" % MINUS)],
        ["Keeping the sign: (<i>x</i> %s 4)² has center <i>x</i> = 4, not %s4." % (MINUS, MINUS),
         "Writing <i>r</i> instead of <i>r</i>² on the right side.",
         "Halving the right side to get the radius. Take the square root.",
         "Completing the square on the left but not adding the same numbers to the right."])
    faq = [("What is the standard form of the equation of a circle?", "(x − h)² + (y − k)² = r², where (h, k) is the center and r is the radius."),
           ("How do you find the center and radius from the equation?", "The center is (h, k), using the opposite signs of the numbers in the parentheses. The radius is the square root of the right side."),
           ("How do you complete the square to find a circle's center?", "Group x-terms and y-terms, add (half the x-coefficient)² and (half the y-coefficient)² to both sides, then factor each group as a square."),
           ("How do you write a circle's equation from the endpoints of a diameter?", "The center is the midpoint of the diameter and the radius is half the diameter's length.")]
    make("equations-of-circles", 20, "G-GPE.A.1",
         "Equations of Circles",
         "Equation of a Circle Worksheet: Center, Radius, Completing the Square (Geometry) | 100 Questions",
         "Equations of Circles",
         "Derive the equation of a circle of given center and radius using the Pythagorean Theorem; complete the square to find the center and radius of a circle given by an equation.",
         "Free Geometry worksheet on equations of circles: standard form, center and radius, completing the square, diameters and points inside or outside. 100 questions with answers.",
         "(x − h)² + (y − k)² = r²: center (h, k), radius r.",
         "Change the signs to read the center. Take the square root of the right side for the radius.",
         body, faq, sets, R, domain="Circles", grade="geometry")


if __name__ == "__main__":
    build()
