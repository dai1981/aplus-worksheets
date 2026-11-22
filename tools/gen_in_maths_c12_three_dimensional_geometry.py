# -*- coding: utf-8 -*-
"""
India Class 12 Maths, NCERT Chapter 11: Three Dimensional Geometry (CBSE Unit IV Vectors and Three-Dimensional Geometry)
  python3 tools/gen_in_maths_c12_three_dimensional_geometry.py
Direction cosines and direction ratios of a line, the line through two points, Cartesian and vector equations of a
line, the angle between two lines, perpendicular and parallel lines, skew lines and the shortest distance between
two lines (own makers).
Wrong answers come from real mistakes: direction cosines that do not satisfy l² + m² + n² = 1, the point and the
direction mixed up in the equation, forgetting the modulus for an acute angle, and |b₁ × b₂| left out of the
shortest distance formula.
"""
import random, math
from fractions import Fraction as F
from in_sr import U, T2, rt, surd, I_, J_, K_, X, Y, Z
from in_common import num, fv

R = random.Random(912111)
QUAD = [(1, 2, 2, 3), (2, 3, 6, 7), (1, 4, 8, 9), (4, 4, 7, 9), (2, 6, 9, 11), (6, 6, 7, 11), (3, 4, 12, 13), (2, 10, 11, 15), (1, 12, 12, 17)]


def vec(a, b, c):
    out = ""
    for v, u in ((a, I_), (b, J_), (c, K_)):
        if v == 0:
            continue
        mag = "" if abs(v) == 1 else num(abs(v))
        out += ((" %s " % ("−" if v < 0 else "+")) if out else ("−" if v < 0 else "")) + mag + u
    return out or "<b>0</b>"


def p3(v):
    return "(%s, %s, %s)" % tuple(num(t) for t in v)


def qv(r):
    a, b, c, d = r.choice(QUAD)
    xs = [a, b, c]
    r.shuffle(xs)
    return [x * r.choice([1, -1]) for x in xs], d


def cart(P, d):
    parts = []
    for v, t, q in zip((X, Y, Z), P, d):
        top = v if t == 0 else "(%s %s %s)" % (v, "−" if t > 0 else "+", num(abs(t)))
        parts.append("%s/%s" % (top, num(q) if q > 0 else "(%s)" % num(q)))
    return " = ".join(parts)


def one_dc(r):
    v, d = qv(r)
    P = [r.randint(-5, 5) for _ in range(3)]
    Q = [p + x for p, x in zip(P, v)]
    k = r.choice(["two", "dr", "valid"])
    if k == "two":
        right = ", ".join(fv(F(x, d)) for x in v)
        return T2("Find the direction cosines of the line through %s and %s (from the first point to the second)." % (p3(P), p3(Q)), right,
                  [", ".join(num(x) for x in v), ", ".join(fv(F(-x, d)) for x in v), ", ".join(fv(F(x, d * d)) for x in v)],
                  "Direction ratios %s; divide by √(%s) = %d: <b>%s</b>." % (", ".join(num(x) for x in v), " + ".join("%d²" % abs(x) for x in v), d, right))
    if k == "dr":
        t = r.choice([2, 3, -2])
        dr = [x * t for x in v]
        right = ", ".join(fv(F(x, d)) for x in v) if t > 0 else ", ".join(fv(F(-x, d)) for x in v)
        right = "±(%s)" % ", ".join(fv(F(x, d)) for x in v)
        return T2("A line has direction ratios %s. Find its direction cosines." % ", ".join(num(x) for x in dr), right,
                  ["±(%s)" % ", ".join(fv(F(x, abs(t) * d)) for x in dr), "±(%s)" % ", ".join(fv(F(x, d)) for x in dr), "±(%s)" % ", ".join(fv(F(x, d * d)) for x in v)],
                  "Divide the ratios by √(sum of squares) = %d: <b>%s</b> (either direction)." % (abs(t) * d, right))
    good = ", ".join(fv(F(x, d)) for x in v)
    bad = [", ".join(fv(F(x, d + 1)) for x in v), ", ".join(fv(F(x, sum(abs(y) for y in v))) for x in v), "1, 1, 1"]
    return T2("Which set can be the direction cosines of a line?", good, bad,
              "Direction cosines satisfy l² + m² + n² = 1. Only <b>%s</b> does: (%s) = 1." % (good, " + ".join("%d/%d" % (x * x, d * d) for x in v)))


def one_eq(r):
    P = [r.randint(-6, 6) for _ in range(3)]
    d = [r.choice([k for k in range(-5, 6) if k]) for _ in range(3)]
    k = r.choice(["cart", "vec", "pt", "two"])
    if k == "cart":
        right = cart(P, d)
        return T2("Find the Cartesian equation of the line through %s with direction ratios %s." % (p3(P), ", ".join(num(x) for x in d)), right,
                  [cart(d, P) if all(P) else cart([-x for x in P], d), cart([-x for x in P], d) if any(P) else cart(P, [x + 1 for x in d]), cart(P, [x * 2 for x in d]) if False else cart([x + y for x, y in zip(P, d)], P) if all(P) else cart(P, [-x for x in d][:2] + [d[2]])],
                  "(%s − %s<sub>1</sub>)/a = (%s − %s<sub>1</sub>)/b = (%s − %s<sub>1</sub>)/c: <b>%s</b>." % (X, X, Y, Y, Z, Z, right))
    if k == "vec":
        right = "<b><i>r</i></b> = (%s) + λ(%s)" % (vec(*P), vec(*d))
        return T2("Write the line %s in vector form." % cart(P, d), right,
                  ["<b><i>r</i></b> = (%s) + λ(%s)" % (vec(*d), vec(*P)), "<b><i>r</i></b> = (%s) + λ(%s)" % (vec(*[-x for x in P]), vec(*d)) if any(P) else "<b><i>r</i></b> = λ(%s)" % vec(*P), "<b><i>r</i></b> = (%s) + λ(%s)" % (vec(*P), vec(*[-x for x in d][:1] + d[1:]))],
                  "The line passes through %s with direction %s: <b>%s</b>." % (p3(P), vec(*d), right))
    if k == "pt":
        lam = r.choice([1, 2, -1, 3])
        Q = [p + lam * x for p, x in zip(P, d)]
        return T2("Which point lies on the line %s?" % cart(P, d), p3(Q), [p3([-x for x in P]) if any(P) else p3(d), p3(d), p3([q + 1 for q in Q])],
                  "Put each fraction equal to λ = %s: %s, so the point is <b>%s</b>." % (num(lam), ", ".join("%s = %s" % (v, num(q)) for v, q in zip((X, Y, Z), Q)), p3(Q)))
    Q = [p + x for p, x in zip(P, d)]
    right = cart(P, d)
    return T2("Find the Cartesian equation of the line through %s and %s." % (p3(P), p3(Q)), right, [cart(P, Q), cart(Q, P) if all(P) else cart(P, [x + y for x, y in zip(P, Q)]), cart(P, [-x for x in d][:2] + [d[2]])],
              "Direction ratios are Q − P = %s, so the line is <b>%s</b>." % (", ".join(num(x) for x in d), right))


def one_angle(r):
    k = r.choice(["perp", "cos", "kperp"])
    if k == "kperp":
        a = [r.choice([k_ for k_ in range(-5, 6) if k_]) for _ in range(3)]
        b = [r.choice([k_ for k_ in range(-5, 6) if k_]) for _ in range(2)]
        if a[2] == 0:
            return None
        kk = F(-(a[0] * b[0] + a[1] * b[1]), a[2])
        if kk.denominator != 1 or kk == 0:
            return None
        P = [r.randint(-4, 4) for _ in range(3)]
        Q = [r.randint(-4, 4) for _ in range(3)]
        return T2("Find k so that the lines %s and %s are perpendicular." % (cart(P, a), cart(Q, b + ["k"]) if False else cart(Q, b + [1]).rsplit("/", 1)[0] + "/k"), num(kk),
                  [num(-kk), num(a[0] * b[0] + a[1] * b[1]), fv(F(a[2], a[0] * b[0] + a[1] * b[1])) if a[0] * b[0] + a[1] * b[1] and F(a[2], a[0] * b[0] + a[1] * b[1]) not in (kk, -kk) else num(kk + 1)],
                  "Perpendicular lines: a<sub>1</sub>a<sub>2</sub> + b<sub>1</sub>b<sub>2</sub> + c<sub>1</sub>c<sub>2</sub> = 0, so %s + %sk = 0 and <b>k = %s</b>." % (num(a[0] * b[0] + a[1] * b[1]), num(a[2]), num(kk)))
    u, d1 = qv(r)
    w, d2 = qv(r)
    dot = sum(x * y for x, y in zip(u, w))
    if k == "perp":
        return T2("Two lines have direction ratios %s and %s. Are they perpendicular?" % (", ".join(num(x) for x in u), ", ".join(num(x) for x in w)),
                  "Yes" if dot == 0 else "No", ["No" if dot == 0 else "Yes", "Only if they intersect", "It cannot be decided from direction ratios"],
                  "a<sub>1</sub>a<sub>2</sub> + b<sub>1</sub>b<sub>2</sub> + c<sub>1</sub>c<sub>2</sub> = %s, so <b>%s</b>." % (num(dot), "they are perpendicular" if dot == 0 else "they are not perpendicular"))
    c = F(abs(dot), d1 * d2)
    if c == 0 or c == 1:
        return None
    return T2("Find cos θ, where θ is the acute angle between lines with direction ratios %s and %s." % (", ".join(num(x) for x in u), ", ".join(num(x) for x in w)), fv(c),
              [fv(F(abs(dot), d1 * d1 * d2 * d2)), num(abs(dot)), fv(F(abs(dot), d1 + d2))],
              "cos θ = |%s| ÷ (%d × %d) = <b>%s</b>." % (num(dot), d1, d2, fv(c)))


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def one_sd(r):
    a1 = [r.randint(-3, 3) for _ in range(3)]
    a2 = [r.randint(-3, 3) for _ in range(3)]
    b1 = [r.randint(-2, 3) for _ in range(3)]
    b2 = [r.randint(-2, 3) for _ in range(3)]
    c = cross(b1, b2)
    n2 = sum(x * x for x in c)
    if n2 == 0:
        return None
    t = sum((y - x) * z for x, y, z in zip(a1, a2, c))
    L1 = "<b><i>r</i></b> = (%s) + λ(%s)" % (vec(*a1), vec(*b1))
    L2 = "<b><i>r</i></b> = (%s) + μ(%s)" % (vec(*a2), vec(*b2))
    s, q = surd(n2)
    val = F(abs(t), s)

    def sdf(v):
        if q == 1:
            return fv(v)
        return "%d/√%d" % (v.numerator, q) if v.denominator == 1 else "%d/(%d√%d)" % (v.numerator, v.denominator, q)
    right = sdf(val)
    if r.random() < 0.4:
        return T2("Do the lines %s and %s intersect?" % (L1, L2), "Yes, the shortest distance is 0" if t == 0 else "No, they are skew lines",
                  ["No, they are skew lines" if t == 0 else "Yes, the shortest distance is 0", "They are parallel", "They are the same line"],
                  "(<b>a</b><sub>2</sub> − <b>a</b><sub>1</sub>) · (<b>b</b><sub>1</sub> × <b>b</b><sub>2</sub>) = %s, so <b>%s</b>." % (num(t), "they intersect" if t == 0 else "they are skew"))
    if t == 0:
        return None
    return T2("Find the shortest distance between the lines %s and %s." % (L1, L2), right,
              [num(abs(t)), sdf(F(abs(t), s * s)) if q != 1 else fv(F(abs(t), n2)), fv(F(abs(t), n2)) if q != 1 else fv(val * 2)],
              "<b>b</b><sub>1</sub> × <b>b</b><sub>2</sub> = %s with magnitude %s; (<b>a</b><sub>2</sub> − <b>a</b><sub>1</sub>) · (<b>b</b><sub>1</sub> × <b>b</b><sub>2</sub>) = %s. d = |%s| ÷ %s = <b>%s</b>." % (
                  vec(*c), rt(n2), num(t), num(t), rt(n2), right))


U(12, 11, "three-dimensional-geometry", 11, "V3", "Three Dimensional Geometry: Direction Cosines, Lines, Angles and Shortest Distance", "3D geometry",
  "Direction cosines and direction ratios of a line joining two points; Cartesian equation and vector equation of a line, skew lines, shortest distance between two lines; angle between two lines (summary of the CBSE syllabus)",
  "Class 12 Three Dimensional Geometry worksheet (NCERT Chapter 11): direction cosines and ratios, Cartesian and vector equations of a line, angle between lines, perpendicular lines, skew lines and shortest distance. 100 questions with answers.",
  "Direction cosines satisfy l² + m² + n² = 1.", "Shortest distance = |(a₂ − a₁) · (b₁ × b₂)| ÷ |b₁ × b₂|.",
  "<ul><li>The line through (<i>x</i><sub>1</sub>, <i>y</i><sub>1</sub>, <i>z</i><sub>1</sub>) and (<i>x</i><sub>2</sub>, <i>y</i><sub>2</sub>, <i>z</i><sub>2</sub>) has direction ratios <i>x</i><sub>2</sub> − <i>x</i><sub>1</sub>, …; divide by their root-sum-square to get direction cosines.</li>"
  "<li>Line through a point with direction ratios a, b, c: (<i>x</i> − <i>x</i><sub>1</sub>)/a = (<i>y</i> − <i>y</i><sub>1</sub>)/b = (<i>z</i> − <i>z</i><sub>1</sub>)/c, or <b><i>r</i></b> = <b><i>a</i></b> + λ<b><i>b</i></b>.</li>"
  "<li>Angle between lines: cos θ = |a<sub>1</sub>a<sub>2</sub> + b<sub>1</sub>b<sub>2</sub> + c<sub>1</sub>c<sub>2</sub>| ÷ (√(a<sub>1</sub>² + …) √(a<sub>2</sub>² + …)). Perpendicular when the sum is 0.</li>"
  "<li>Skew lines neither meet nor are parallel. Their shortest distance is |(<b><i>a</i></b><sub>2</sub> − <b><i>a</i></b><sub>1</sub>) · (<b><i>b</i></b><sub>1</sub> × <b><i>b</i></b><sub>2</sub>)| ÷ |<b><i>b</i></b><sub>1</sub> × <b><i>b</i></b><sub>2</sub>|.</li></ul>",
  [("Find the direction cosines of the line through (−2, 4, −5) and (1, 2, 3).", ["Direction ratios 3, −2, 8", "√(9 + 4 + 64) = √77"], "3/√77, −2/√77, 8/√77")],
  ["Giving direction ratios when direction cosines are asked.", "Swapping the point and the direction in the equation of a line.", "Leaving out the division by |b₁ × b₂| in the shortest distance."],
  [("What is the difference between direction ratios and direction cosines?", "Direction ratios are any numbers proportional to the direction cosines; direction cosines also satisfy l² + m² + n² = 1."),
   ("What are skew lines?", "Lines in space that are not parallel and do not intersect.")],
  [("Direction cosines and ratios", [(one_dc, 20)]),
   ("Equation of a line", [(one_eq, 20)]),
   ("Angle between two lines", [(one_angle, 20)]),
   ("Skew lines and shortest distance", [(one_sd, 20)]),
   ("Mixed problems", [(one_dc, 6), (one_eq, 7), (one_angle, 7)])], 912111)
