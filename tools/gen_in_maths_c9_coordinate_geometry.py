# -*- coding: utf-8 -*-
"""
India Class 9 Maths, NCERT Chapter 3: Coordinate Geometry (CBSE Unit III)
  python3 tools/gen_in_maths_c9_coordinate_geometry.py
The Cartesian plane: axes, origin, quadrants and their signs, abscissa and ordinate, reading and plotting points on a grid,
points on the axes, distances from the axes, and shapes on the plane (missing vertices, lengths along grid lines).
Wrong answers come from real mistakes: swapping x and y, wrong quadrant numbering (clockwise), calling a point on an
axis part of a quadrant, and the distance from the x-axis taken as |x|.
"""
import random
from in_common import num, S, make, lesson, mix, T, MINUS
from g8_common import grid_svg

R = random.Random(909003)


def pt(x, y):
    return "(%s, %s)" % (num(x), num(y))


def quad(x, y):
    if x == 0 or y == 0:
        return None
    return {(1, 1): "I", (-1, 1): "II", (-1, -1): "III", (1, -1): "IV"}[(1 if x > 0 else -1, 1 if y > 0 else -1)]


def nz(lo, hi):
    return [k for k in range(lo, hi + 1) if k]


# ---------------------------------------------------------------- set 1: the plane
FACTS = [
    ("The point where the x-axis and the y-axis meet is called the", "origin", ["abscissa", "ordinate", "quadrant"], "The axes meet at the origin (0, 0)."),
    ("The x-coordinate of a point is also called its", "abscissa", ["ordinate", "origin", "quadrant"], "The x-coordinate is the abscissa."),
    ("The y-coordinate of a point is also called its", "ordinate", ["abscissa", "origin", "axis"], "The y-coordinate is the ordinate."),
    ("The axes divide the plane into four parts called", "quadrants", ["axes", "ordinates", "origins"], "Each of the four parts is a quadrant."),
    ("The coordinates of the origin are", "(0, 0)", ["(1, 1)", "(0, 1)", "(1, 0)"], "The origin is 0 along both axes."),
    ("Every point on the x-axis has", "y-coordinate 0", ["x-coordinate 0", "equal coordinates", "negative coordinates"], "On the x-axis you have not moved up or down, so y = 0."),
    ("Every point on the y-axis has", "x-coordinate 0", ["y-coordinate 0", "equal coordinates", "positive coordinates"], "On the y-axis you have not moved left or right, so x = 0."),
    ("In which quadrant are both coordinates negative?", "Quadrant III", ["Quadrant I", "Quadrant II", "Quadrant IV"], "Left (x &lt; 0) and down (y &lt; 0) is quadrant III."),
    ("In which quadrant is the abscissa negative and the ordinate positive?", "Quadrant II", ["Quadrant I", "Quadrant III", "Quadrant IV"], "Left and up is quadrant II."),
    ("In which quadrant is the abscissa positive and the ordinate negative?", "Quadrant IV", ["Quadrant I", "Quadrant II", "Quadrant III"], "Right and down is quadrant IV."),
    ("The quadrants are numbered", "anticlockwise, starting from the top right", ["clockwise, starting from the top right", "anticlockwise, starting from the bottom left", "clockwise, starting from the top left"],
     "Quadrant I is top right; the numbering goes anticlockwise."),
    ("The signs of the coordinates of a point in quadrant I are", "(+, +)", ["(−, +)", "(−, −)", "(+, −)"], "Quadrant I is right and up."),
]


def one_plane(r):
    if r.random() < 0.5:
        q, a, w, e = r.choice(FACTS)
        return T(q if q.endswith("?") else q + " ___.", a, w, e + " <b>%s</b>." % a)
    x, y = r.choice(nz(-9, 9)), r.choice(nz(-9, 9))
    qd = quad(x, y)
    return T("In which quadrant does the point %s lie?" % pt(x, y), "Quadrant %s" % qd, ["Quadrant %s" % q for q in ("I", "II", "III", "IV") if q != qd],
             "x is %s and y is %s, so the point is in <b>quadrant %s</b>." % ("positive" if x > 0 else "negative", "positive" if y > 0 else "negative", qd))


# ---------------------------------------------------------------- set 2: reading points from a grid
def one_read(r):
    pts = []
    names = r.sample("ABCDEFPQRS", 4)
    while len(pts) < 4:
        p = (r.randint(-5, 5), r.randint(-5, 5))
        if p not in pts and p != (0, 0):
            pts.append(p)
    pic = grid_svg(-6, 6, points=[(x, y, n, "#c0392b") for (x, y), n in zip(pts, names)], unit=22, label="points on a coordinate grid")
    i = r.randrange(4)
    x, y = pts[i]
    want = r.choice(["coords", "coords", "abs", "ord"])
    if want == "coords":
        w = [pt(y, x) if x != y else pt(x, -y), pt(-x, y) if x else pt(x + 1, y), pt(x, -y) if y else pt(x, y + 1), pt(-x, -y)]
        w = [t for t in dict.fromkeys(w) if t != pt(x, y)]
        return T("What are the coordinates of the point %s?" % names[i] + pic, pt(x, y), w[:3],
                 "Go across first (x = %s), then up or down (y = %s): <b>%s</b>." % (num(x), num(y), pt(x, y)))
    if want == "abs":
        return T("What is the abscissa of the point %s?" % names[i] + pic, num(x), [num(y) if y != x else num(x + 1), num(-x) if x else "1", num(x + y) if x + y not in (x, y, -x) else num(x - 1)],
                 "The abscissa is the x-coordinate of %s %s: <b>%s</b>." % (names[i], pt(x, y), num(x)))
    return T("What is the ordinate of the point %s?" % names[i] + pic, num(y), [num(x) if x != y else num(y + 1), num(-y) if y else "1", num(x + y) if x + y not in (x, y, -y) else num(y - 1)],
             "The ordinate is the y-coordinate of %s %s: <b>%s</b>." % (names[i], pt(x, y), num(y)))


# ---------------------------------------------------------------- set 3: points on the axes and signs
def one_axes(r):
    kind = r.choice(["which", "which", "where", "dist", "dist"])
    if kind == "which":
        ax = r.choice(["x", "y"])
        k = r.choice(nz(-8, 8))
        good = pt(k, 0) if ax == "x" else pt(0, k)
        w = [pt(0, k) if ax == "x" else pt(k, 0), pt(k, k), pt(k, 1) if ax == "x" else pt(1, k)]
        return T("Which point lies on the %s-axis?" % ax, good, w, "On the %s-axis the %s-coordinate is 0: <b>%s</b>." % (ax, "y" if ax == "x" else "x", good))
    if kind == "where":
        k = r.choice(nz(-9, 9))
        t = r.choice(["x", "y"])
        p = pt(k, 0) if t == "x" else pt(0, k)
        ans = "On the %s-axis" % t
        return T("Where does the point %s lie?" % p, ans, ["On the %s-axis" % ("y" if t == "x" else "x"), "In quadrant I" if k > 0 else "In quadrant III", "In quadrant II" if k > 0 else "In quadrant IV"],
                 "A point with %s-coordinate 0 lies on an axis, not in a quadrant: <b>%s</b>." % ("y" if t == "x" else "x", ans.lower()))
    x, y = r.choice(nz(-9, 9)), r.choice(nz(-9, 9))
    if abs(x) == abs(y):
        return None
    t = r.choice(["x", "y"])
    v = abs(y) if t == "x" else abs(x)
    return T("How far is the point %s from the %s-axis?" % (pt(x, y), t), "%d units" % v, ["%d units" % (abs(x) if t == "x" else abs(y)), "%d units" % (abs(x) + abs(y)), "%d units" % abs(x - y) if abs(x - y) not in (v, abs(x) + abs(y), abs(x) if t == "x" else abs(y)) else "%d units" % (v + 1)],
             "The distance from the %s-axis is the size of the %s-coordinate: <b>%d units</b>." % (t, "y" if t == "x" else "x", v))


# ---------------------------------------------------------------- set 4: plotting and comparing
def one_plot(r):
    kind = r.choice(["same", "mirror", "mirror", "move", "move"])
    if kind == "same":
        a, b = r.sample(nz(-7, 7), 2)
        if abs(a) == abs(b):
            return None
        return T("Are the points %s and %s the same point?" % (pt(a, b), pt(b, a)), "No, the order of the coordinates matters",
                 ["Yes, they use the same numbers", "Yes, if both are in the same quadrant", "Only when both are positive"],
                 "%s is %s across and %s up or down; %s is the other way round. <b>They are different points.</b>" % (pt(a, b), num(a), num(b), pt(b, a)))
    x, y = r.choice(nz(-7, 7)), r.choice(nz(-7, 7))
    if kind == "mirror":
        ax = r.choice(["x", "y"])
        ans = pt(x, -y) if ax == "x" else pt(-x, y)
        return T("The point %s is reflected in the %s-axis. What are the coordinates of its image?" % (pt(x, y), ax), ans,
                 [pt(-x, y) if ax == "x" else pt(x, -y), pt(-x, -y), pt(y, x)],
                 "Reflecting in the %s-axis changes the sign of the %s-coordinate only: <b>%s</b>." % (ax, "y" if ax == "x" else "x", ans))
    dx, dy = r.choice(nz(-5, 5)), r.choice(nz(-5, 5))
    ans = pt(x + dx, y + dy)
    desc = "%d units to the %s and %d units %s" % (abs(dx), "right" if dx > 0 else "left", abs(dy), "up" if dy > 0 else "down")
    return T("Start at %s and move %s. Where do you end?" % (pt(x, y), desc), ans, [pt(x + dy, y + dx) if dx != dy else pt(x - dx, y + dy), pt(x - dx, y - dy), pt(x + dx, y - dy)],
             "Add %s to x and %s to y: <b>%s</b>." % (num(dx), num(dy), ans))


# ---------------------------------------------------------------- set 5: shapes on the plane
def one_shape(r):
    kind = r.choice(["rect", "rect", "len", "area", "quad"])
    x1, y1 = r.randint(-6, 2), r.randint(-6, 2)
    w, h = r.randint(2, 6), r.randint(2, 6)
    if kind == "rect":
        A, B, C, D = (x1, y1), (x1 + w, y1), (x1 + w, y1 + h), (x1, y1 + h)
        return T("A(%s, %s), B(%s, %s) and C(%s, %s) are three vertices of rectangle ABCD. What are the coordinates of D?" % (num(A[0]), num(A[1]), num(B[0]), num(B[1]), num(C[0]), num(C[1])),
                 pt(*D), [pt(D[1], D[0]) if D[0] != D[1] else pt(D[0] + 1, D[1]), pt(C[0], A[1] - h), pt(A[0] - w, C[1])],
                 "D has the same x-coordinate as A and the same y-coordinate as C: <b>%s</b>." % pt(*D))
    if kind == "len":
        t = r.choice(["h", "v"])
        if t == "h":
            p, q = (x1, y1), (x1 + w + 3, y1)
        else:
            p, q = (x1, y1), (x1, y1 + h + 3)
        d = abs(q[0] - p[0]) + abs(q[1] - p[1])
        return T("How long is the segment joining %s and %s?" % (pt(*p), pt(*q)), "%d units" % d, ["%d units" % abs(sum(q) + sum(p)), "%d units" % (d + 1), "%d units" % (abs(q[0] + p[0]) if t == "h" else abs(q[1] + p[1])) if (abs(q[0] + p[0]) if t == "h" else abs(q[1] + p[1])) != d else "%d units" % (d + 2)],
                 "Both points have the same %s-coordinate, so count along the grid: %s − (%s) = <b>%d units</b>." % ("y" if t == "h" else "x", num(q[0] if t == "h" else q[1]), num(p[0] if t == "h" else p[1]), d))
    if kind == "area":
        return T("A rectangle has vertices (%s, %s), (%s, %s), (%s, %s) and (%s, %s). What is its area?" % (num(x1), num(y1), num(x1 + w), num(y1), num(x1 + w), num(y1 + h), num(x1), num(y1 + h)),
                 "%d square units" % (w * h), ["%d square units" % (2 * (w + h)), "%d square units" % (w + h), "%d square units" % ((w + 1) * (h + 1))],
                 "Width %d, height %d: area = <b>%d square units</b>." % (w, h, w * h))
    x, y = r.choice(nz(-6, 6)), r.choice(nz(-6, 6))
    pts = [(x, y), (-x, y), (-x, -y), (x, -y)]
    qs = [quad(*p) for p in pts]
    return T("The points %s are plotted. In which quadrants do they lie, in that order?" % ", ".join(pt(*p) for p in pts), ", ".join(qs),
             [", ".join(reversed(qs)), ", ".join(qs[1:] + qs[:1]), ", ".join([qs[0], qs[3], qs[2], qs[1]])],
             "Check the sign of each coordinate: <b>%s</b>." % ", ".join(qs))


def main():
    seen = set()
    sets = [
        S("The Cartesian plane", mix(R, [(one_plane, 20)], seen)),
        S("Reading points on a grid", mix(R, [(one_read, 20)], seen)),
        S("Points on the axes and distances", mix(R, [(one_axes, 20)], seen)),
        S("Plotting and moving points", mix(R, [(one_plot, 20)], seen)),
        S("Shapes on the plane", mix(R, [(one_shape, 20)], seen)),
    ]
    body = lesson(
        "<p>Two perpendicular number lines, the <b>x-axis</b> and the <b>y-axis</b>, meet at the <b>origin</b> O(0, 0) and divide the plane into four <b>quadrants</b> (I to IV, anticlockwise from the top right).</p>"
        "<p>A point is written (x, y): the <b>abscissa</b> x first, then the <b>ordinate</b> y. Signs: I (+, +), II (−, +), III (−, −), IV (+, −). Points on an axis are in no quadrant.</p>",
        [("Where is (−4, 3)?", ["x negative, y positive"], "Quadrant II"),
         ("How far is (5, −2) from the x-axis?", ["The distance from the x-axis is |y|"], "2 units")],
        ["Swapping the coordinates: (2, 5) and (5, 2) are different points.",
         "Numbering the quadrants clockwise. They go anticlockwise.",
         "Saying a point like (0, 4) is in quadrant I. It lies on the y-axis."])
    faq = [
        ("What is the abscissa and the ordinate?", "For the point (x, y), the abscissa is the x-coordinate and the ordinate is the y-coordinate."),
        ("How are the quadrants numbered?", "Anticlockwise from the top right: I (+, +), II (−, +), III (−, −), IV (+, −)."),
        ("Which quadrant does a point on an axis belong to?", "None. A point on an axis is not in any quadrant."),
        ("How far is a point (x, y) from the axes?", "Its distance from the x-axis is |y| and from the y-axis is |x|."),
    ]
    make(9, "coordinate-geometry", 3, "III", 3, "Coordinate Geometry: The Cartesian Plane", "coordinate geometry",
         "The Cartesian plane, coordinates of a point, names and terms associated with the coordinate plane, notations (summary of the CBSE syllabus)",
         "Class 9 Coordinate Geometry worksheet (NCERT Chapter 3): axes, quadrants, abscissa and ordinate, reading and plotting points, and shapes on the plane. 100 questions with answers.",
         "(x, y): across first, then up or down", "Quadrants I to IV go anticlockwise from the top right.",
         body, faq, sets, R)


if __name__ == "__main__":
    main()
