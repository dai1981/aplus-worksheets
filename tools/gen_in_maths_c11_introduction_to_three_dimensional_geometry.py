# -*- coding: utf-8 -*-
"""
India Class 11 Maths, NCERT Chapter 11: Introduction to Three Dimensional Geometry (CBSE Unit III Coordinate Geometry)
  python3 tools/gen_in_maths_c11_introduction_to_three_dimensional_geometry.py
Coordinate axes and planes, the octant of a point, points on the axes and in the coordinate planes, the foot of the
perpendicular on a plane or an axis, the distance between two points and from the origin, and using distances to
show points are collinear or form a right or isosceles triangle (own makers).
Wrong answers come from real mistakes: the wrong signs for an octant, a point on the y-axis written as (0, y, z),
forgetting the z-term in the distance formula, and adding the coordinates instead of squaring them.
"""
import random, math
from in_sr import U, T2, rt, X, Y, Z
from in_common import num

R = random.Random(911111)
OCT = {(1, 1, 1): "I", (-1, 1, 1): "II", (-1, -1, 1): "III", (1, -1, 1): "IV", (1, 1, -1): "V", (-1, 1, -1): "VI", (-1, -1, -1): "VII", (1, -1, -1): "VIII"}


def p3(x, y, z):
    return "(%s, %s, %s)" % (num(x), num(y), num(z))


def nz():
    return R.choice([k for k in range(-9, 10) if k])


def one_oct(r):
    x, y, z = [r.choice([k for k in range(-9, 10) if k]) for _ in range(3)]
    s = tuple(1 if v > 0 else -1 for v in (x, y, z))
    right = OCT[s]
    wr = [OCT[(s[0], s[1], -s[2])], OCT[(-s[0], s[1], s[2])], OCT[(s[0], -s[1], s[2])]]
    return T2("In which octant does the point %s lie?" % p3(x, y, z), "Octant " + right, ["Octant " + w for w in wr],
              "The signs of (%s, %s, %s) are (%s, %s, %s), which is <b>octant %s</b>." % (X, Y, Z, *["+" if v > 0 else "−" for v in s], right))


def one_axis(r):
    k = r.choice(["axis", "plane", "foot", "foot_axis"])
    x, y, z = [r.choice([k_ for k_ in range(-9, 10) if k_]) for _ in range(3)]
    if k == "axis":
        ax = r.choice(["x", "y", "z"])
        right = {"x": "(<i>a</i>, 0, 0)", "y": "(0, <i>b</i>, 0)", "z": "(0, 0, <i>c</i>)"}[ax]
        return T2("What is the general form of a point on the %s-axis?" % ax, right, [w for w in ["(<i>a</i>, 0, 0)", "(0, <i>b</i>, 0)", "(0, 0, <i>c</i>)", {"x": "(0, <i>b</i>, <i>c</i>)", "y": "(<i>a</i>, 0, <i>c</i>)", "z": "(<i>a</i>, <i>b</i>, 0)"}[ax]] if w != right],
                      "On the %s-axis the other two coordinates are 0: <b>%s</b>." % (ax, right))
    if k == "plane":
        pl = r.choice(["xy", "yz", "zx"])
        pts = {"xy": p3(x, y, 0), "yz": p3(0, y, z), "zx": p3(x, 0, z)}
        right = pts[pl]
        return T2("Which point lies in the %s-plane?" % pl.upper(), right, [v for kk, v in pts.items() if kk != pl] + [p3(x, y, z)],
                  "In the %s-plane the %s-coordinate is 0: <b>%s</b>." % (pl.upper(), {"xy": "z", "yz": "x", "zx": "y"}[pl], right))
    if k == "foot":
        pl = r.choice(["xy", "yz", "zx"])
        right = {"xy": p3(x, y, 0), "yz": p3(0, y, z), "zx": p3(x, 0, z)}[pl]
        return T2("Find the foot of the perpendicular from %s to the %s-plane." % (p3(x, y, z), pl.upper()), right,
                  [v for kk, v in {"xy": p3(x, y, 0), "yz": p3(0, y, z), "zx": p3(x, 0, z)}.items() if kk != pl] + [p3(-x, -y, -z)],
                  "Dropping straight down to the %s-plane only changes the %s-coordinate to 0: <b>%s</b>." % (pl.upper(), {"xy": "z", "yz": "x", "zx": "y"}[pl], right))
    ax = r.choice(["x", "y", "z"])
    d2 = {"x": y * y + z * z, "y": x * x + z * z, "z": x * x + y * y}[ax]
    return T2("Find the distance of the point %s from the %s-axis." % (p3(x, y, z), ax), rt(d2),
              [rt(x * x + y * y + z * z), rt({"x": x * x, "y": y * y, "z": z * z}[ax]), rt({"x": x * x + y * y, "y": y * y + z * z, "z": z * z + x * x}[ax])],
              "The foot on the %s-axis keeps only the %s-coordinate, so the distance is √(%s) = <b>%s</b>." % (
                  ax, ax, " + ".join("%s²" % ("(" + num(v) + ")" if v < 0 else num(v)) for a_, v in zip("xyz", (x, y, z)) if a_ != ax), rt(d2)))


QUAD = [(1, 2, 2, 3), (2, 3, 6, 7), (1, 4, 8, 9), (4, 4, 7, 9), (2, 6, 9, 11), (6, 6, 7, 11), (2, 10, 11, 15), (3, 4, 12, 13), (2, 5, 14, 15), (1, 12, 12, 17)]


def one_dist(r):
    if r.random() < 0.7:
        a, b, c, d = r.choice(QUAD)
        dx, dy, dz = [v * r.choice([1, -1]) for v in r.sample([a, b, c], 3)]
        x1, y1, z1 = r.randint(-6, 6), r.randint(-6, 6), r.randint(-6, 6)
        P, Q = p3(x1, y1, z1), p3(x1 + dx, y1 + dy, z1 + dz)
        return T2("Find the distance between %s and %s." % (P, Q), str(d), [rt(dx * dx + dy * dy), str(abs(dx) + abs(dy) + abs(dz)), str(d * d)],
                  "PQ = √(%d² + %d² + %d²) = √%d = <b>%d</b>." % (abs(dx), abs(dy), abs(dz), d * d, d))
    x, y, z = r.randint(-6, 6), r.randint(-6, 6), r.randint(1, 6)
    s = x * x + y * y + z * z
    return T2("Find the distance of %s from the origin." % p3(x, y, z), rt(s), [rt(x * x + y * y) if x * x + y * y else "0", str(abs(x) + abs(y) + abs(z)), str(s)],
              "OP = √(%s² + %s² + %s²) = √%d = <b>%s</b>." % (num(abs(x)), num(abs(y)), num(z), s, rt(s)))


def one_shape(r):
    k = r.choice(["coll", "iso", "right", "find"])
    x1, y1, z1 = r.randint(-4, 4), r.randint(-4, 4), r.randint(-4, 4)
    if k == "coll":
        a, b, c, d = r.choice(QUAD)
        dx, dy, dz = [v * r.choice([1, -1]) for v in (a, b, c)]
        t = r.choice([2, 3])
        A, B, C_ = p3(x1, y1, z1), p3(x1 + dx, y1 + dy, z1 + dz), p3(x1 + t * dx, y1 + t * dy, z1 + t * dz)
        return T2("A = %s, B = %s and C = %s. Which is true?" % (A, B, C_), "AB + BC = AC, so A, B, C are collinear",
                  ["AB = BC, so the triangle is isosceles", "AB² + BC² = AC², so the triangle is right-angled", "A, B, C form a triangle with all sides different"],
                  "AB = %d, BC = %d and AC = %d. Since %d + %d = %d, <b>the points are collinear</b>." % (d, (t - 1) * d, t * d, d, (t - 1) * d, t * d))
    if k == "find":
        a, b, c, d = r.choice(QUAD)
        cand = [z1 + c, z1 - c]
        return T2("The distance between %s and (%s, %s, <i>k</i>) is %d. Find the possible values of <i>k</i>." % (p3(x1, y1, z1), num(x1 + a), num(y1 + b), d),
                  "%s or %s" % (num(min(cand)), num(max(cand))), ["%s only" % num(max(cand)), "%s or %s" % (num(-max(cand)), num(-min(cand))) if cand[0] + cand[1] else "%s or %s" % (num(min(cand) - 1), num(max(cand) + 1)), "%s or %s" % (num(z1 + d), num(z1 - d))],
                  "%d² + %d² + (<i>k</i> − %s)² = %d, so (<i>k</i> − %s)² = %d and <i>k</i> = <b>%s or %s</b>." % (a, b, num(z1), d * d, num(z1), c * c, num(min(cand)), num(max(cand))))
    if k == "iso":
        u = r.randint(1, 5)
        A, B, C_ = p3(x1, y1, z1), p3(x1 + u, y1, z1), p3(x1, y1 + u, z1)
        return T2("What kind of triangle has vertices %s, %s and %s?" % (A, B, C_), "Right-angled and isosceles",
                  ["Equilateral", "Scalene and not right-angled", "The points are collinear"],
                  "AB = AC = %d and BC = %s, and %d + %d = %d = BC², so it is <b>right-angled and isosceles</b>." % (u, rt(2 * u * u), u * u, u * u, 2 * u * u))
    u = r.randint(1, 4)
    A, B, C_ = p3(x1 + u, y1, z1), p3(x1, y1 + u, z1), p3(x1, y1, z1 + u)
    return T2("What kind of triangle has vertices %s, %s and %s?" % (A, B, C_), "Equilateral", ["Right-angled and isosceles", "Scalene", "The points are collinear"],
              "Each side is √(%d + %d) = %s, so the triangle is <b>equilateral</b>." % (u * u, u * u, rt(2 * u * u)))


U(11, 11, "introduction-to-three-dimensional-geometry", 11, "III", "Introduction to Three Dimensional Geometry: Octants and Distance", "3D geometry",
  "Coordinate axes and coordinate planes in three dimensions; coordinates of a point; distance between two points (summary of the CBSE syllabus)",
  "Class 11 Introduction to Three Dimensional Geometry worksheet (NCERT Chapter 11): octants, points on axes and planes, foot of a perpendicular, distance formula and triangle problems in 3D. 100 questions with answers.",
  "PQ = √((x₂ − x₁)² + (y₂ − y₁)² + (z₂ − z₁)²).", "The signs of x, y and z decide the octant.",
  "<ul><li>Three axes meet at the origin O; the XY-, YZ- and ZX-planes divide space into eight <b>octants</b>.</li>"
  "<li>A point on the <i>x</i>-axis is (a, 0, 0); a point in the XY-plane is (a, b, 0).</li>"
  "<li>Distance between P(<i>x</i><sub>1</sub>, <i>y</i><sub>1</sub>, <i>z</i><sub>1</sub>) and Q(<i>x</i><sub>2</sub>, <i>y</i><sub>2</sub>, <i>z</i><sub>2</sub>): √((<i>x</i><sub>2</sub> − <i>x</i><sub>1</sub>)² + (<i>y</i><sub>2</sub> − <i>y</i><sub>1</sub>)² + (<i>z</i><sub>2</sub> − <i>z</i><sub>1</sub>)²).</li></ul>",
  [("Find the distance between (1, −3, 4) and (−4, 1, 2).", ["√((−5)² + 4² + (−2)²)", "= √45"], "3√5")],
  ["Leaving out the z-term in the distance formula.", "Writing a point on the y-axis as (0, y, z).", "Using the wrong signs for an octant."],
  [("How many octants are there?", "Eight."), ("What is the distance of (x, y, z) from the origin?", "√(x² + y² + z²).")],
  [("Octants", [(one_oct, 20)]),
   ("Axes and planes", [(one_axis, 20)]),
   ("Distance formula", [(one_dist, 20)]),
   ("Triangles and collinear points", [(one_shape, 14), (one_dist, 6)]),
   ("Mixed problems", [(one_axis, 8), (one_shape, 6), (one_oct, 6)])], 911111)
