# -*- coding: utf-8 -*-
"""
AU Year 7 Maths: Transformations on the Cartesian plane (Australian Curriculum v9.0: AC9M7SP03)
  python3 tools/gen_au_maths_y7_transformations_on_the_cartesian_plane.py
Reflections in the axes and in vertical or horizontal lines, rotations of 90° and 180° about a given point,
translations described in words, transforming the vertices of shapes, and describing a single transformation
from a diagram.
Wrong answers come from real mistakes: reflecting in the wrong axis, rotating the wrong way, swapping the
horizontal and vertical moves of a translation, and changing the wrong sign.
"""
import random
from fractions import Fraction as F
from au_hs import num, mcq, B, S, make, lesson, collect, T, fig, RED, BLUE, GREEN, svg_wrap, text, line, INK
from gen_uk_maths_y7_coordinates_and_straight_line_graphs import grid

R = random.Random(71801)


def P(x, y):
    return "(%s, %s)" % (num(x), num(y))


def moves(a, b):
    h = "%d unit%s %s" % (abs(a), "" if abs(a) == 1 else "s", "right" if a > 0 else "left") if a else ""
    v = "%d unit%s %s" % (abs(b), "" if abs(b) == 1 else "s", "up" if b > 0 else "down") if b else ""
    return " and ".join(x for x in (h, v) if x)


# ------------------------------------------------------------ set 1: reflections
def reflect(p, kind, c=0):
    x, y = p
    if kind == "x=":
        return (2 * c - x, y)
    if kind == "y=":
        return (x, 2 * c - y)
    if kind == "y=x":
        return (y, x)
    return (-y, -x)


def mirror_name(kind, c):
    return {"x=": "the line <i>x</i> = %s" % num(c), "y=": "the line <i>y</i> = %s" % num(c),
            "y=x": "the line <i>y</i> = <i>x</i>", "y=-x": "the line <i>y</i> = −<i>x</i>"}[kind]


def one_reflect(r):
    kind = r.choice(["x=", "y=", "x=", "y="])
    c = r.choice([0, 0, 0, 1, -1, 2, -2])
    p = (r.randint(-5, 5), r.randint(-5, 5))
    img = reflect(p, kind, c)
    if img == p or max(abs(v) for v in img) > 9:
        return None
    if kind == "x=" and c == 0:
        nm = "the <i>y</i>-axis"
    elif kind == "y=" and c == 0:
        nm = "the <i>x</i>-axis"
    else:
        nm = mirror_name(kind, c)
    q = "The point %s is reflected in %s. What are the coordinates of its image?" % (B(P(*p)), nm)
    other = {"x=": "y=", "y=": "x=", "y=x": "y=-x", "y=-x": "y=x"}[kind]
    wr = [P(*reflect(p, other, c)), P(-p[0], -p[1]), P(p[1], p[0]) if kind != "y=x" else P(-p[1], p[0])]
    e = {"x=": "Reflecting in a vertical line changes the <i>x</i>-coordinate only: the point is as far on the other side.",
         "y=": "Reflecting in a horizontal line changes the <i>y</i>-coordinate only.",
         "y=x": "Reflecting in <i>y</i> = <i>x</i> swaps the coordinates.",
         "y=-x": "Reflecting in <i>y</i> = −<i>x</i> swaps the coordinates and changes both signs."}[kind]
    right = P(*img)
    wr = [w for w in wr if w != right]
    if len(set(wr)) < 3:
        wr.append(P(img[0] + 1, img[1]))
    return T(q, right, list(dict.fromkeys(wr))[:3], e + " Image: <b>%s</b>." % right)


# ------------------------------------------------------------ set 2: rotations
def rot(p, ang, ctr=(0, 0)):
    x, y = p[0] - ctr[0], p[1] - ctr[1]
    if ang == 90:        # anticlockwise
        x, y = -y, x
    elif ang == -90:     # clockwise
        x, y = y, -x
    else:
        x, y = -x, -y
    return (x + ctr[0], y + ctr[1])


def one_rotate(r):
    ang = r.choice([90, -90, 180])
    ctr = r.choice([(0, 0), (0, 0), (1, 1), (2, 0), (-1, 2)])
    p = (r.randint(-4, 5), r.randint(-4, 5))
    if p == ctr:
        return None
    img = rot(p, ang, ctr)
    words = {90: "90° anticlockwise", -90: "90° clockwise", 180: "180°"}[ang]
    about = "the origin" if ctr == (0, 0) else "the point %s" % P(*ctr)
    q = "The point %s is rotated %s about %s. Where is its image?" % (B(P(*p)), words, about)
    wrong = [P(*rot(p, -ang if ang != 180 else 90, ctr)), P(*rot(p, ang)) if ctr != (0, 0) else P(-p[0], p[1]), P(p[1], p[0])]
    right = P(*img)
    wrong = [w for w in wrong if w != right]
    if len(set(wrong)) < 3:
        wrong.append(P(img[0], -img[1]))
    e = ("Rotating 180° about the origin changes both signs." if ang == 180 and ctr == (0, 0) else
         "Use tracing paper, or turn the position relative to the centre: (%s, %s) from the centre becomes (%s, %s)." % (
             num(p[0] - ctr[0]), num(p[1] - ctr[1]), num(img[0] - ctr[0]), num(img[1] - ctr[1])))
    return T(q, right, list(dict.fromkeys(wrong))[:3], e + " Image: <b>%s</b>." % right)



# ------------------------------------------------------------ set 3: translations
def one_translate(r):
    a, b = r.randint(-6, 6), r.randint(-6, 6)
    if a == 0 or b == 0 or abs(a) == abs(b):
        return None
    p = (r.randint(-5, 5), r.randint(-5, 5))
    img = (p[0] + a, p[1] + b)
    if r.random() < 0.65:
        q = "The point %s is translated %s. Where is its image?" % (B(P(*p)), moves(a, b))
        right = P(*img)
        wr = [P(p[0] + b, p[1] + a), P(p[0] - a, p[1] - b), P(p[0] + a, p[1] - b)]
        e = "Moving %s changes the <i>x</i>-coordinate by %s; moving %s changes the <i>y</i>-coordinate by %s. Image: <b>%s</b>." % (
            "right" if a > 0 else "left", num(a), "up" if b > 0 else "down", num(b), right)
        return T(q, right, [w for w in wr if w != right], e)
    q = "The point %s is translated to %s. Describe the translation." % (B(P(*p)), B(P(*img)))
    right = moves(a, b).capitalize()
    wr = [moves(b, a).capitalize(), moves(-a, -b).capitalize(), moves(a, -b).capitalize()]
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right], "<i>x</i>: %s → %s is %s. <i>y</i>: %s → %s is %s. <b>%s</b>." % (
        num(p[0]), num(img[0]), num(a), num(p[1]), num(img[1]), num(b), right))


# ------------------------------------------------------------ set 4: transforming shapes
def one_shape(r):
    x0, y0 = r.randint(1, 3), r.randint(1, 3)
    A = [(x0, y0), (x0 + r.randint(2, 3), y0), (x0, y0 + r.randint(2, 3))]
    kind = r.choice(["refl_x", "refl_y", "rot180", "rot90", "trans"])
    i = r.randrange(3)
    names = "ABC"
    pt = A[i]
    if kind == "refl_x":
        img, how = (pt[0], -pt[1]), "reflected in the <i>x</i>-axis"
    elif kind == "refl_y":
        img, how = (-pt[0], pt[1]), "reflected in the <i>y</i>-axis"
    elif kind == "rot180":
        img, how = (-pt[0], -pt[1]), "rotated 180° about the origin"
    elif kind == "rot90":
        img, how = (pt[1], -pt[0]), "rotated 90° clockwise about the origin"
    else:
        a, b = r.choice([-6, -5, -4, 2, 3]), r.choice([-5, -4, 2, 3])
        img, how = (pt[0] + a, pt[1] + b), "translated %s" % moves(a, b)
    q = "Triangle ABC has vertices %s. It is %s. What are the coordinates of %s′?" % (
        ", ".join("%s%s" % (names[k], P(*A[k])) for k in range(3)), how, names[i])
    right = P(*img)
    wr = [P(-img[0], img[1]), P(img[0], -img[1]), P(img[1], img[0]), P(*pt)]
    wr = [w for w in dict.fromkeys(wr) if w != right]
    return T(q, right, wr[:3], "%s%s is %s, so %s′ is <b>%s</b>." % (names[i], P(*pt), how, names[i], right))


def tri_pts(base):
    x, y = base
    return [(x, y), (x + 2, y), (x, y + 3)]


def poly_line(pts, col):
    return [(a[0], a[1], b[0], b[1], col, "") for a, b in zip(pts, pts[1:] + pts[:1])]



# ------------------------------------------------------------ set 5: describing transformations
def problems():
    its = []
    A = tri_pts((1, 1))
    for img, right, wr, e in [
        ([(-x, y) for x, y in A], "A reflection in the <i>y</i>-axis", ["A reflection in the <i>x</i>-axis", "A rotation of 180° about the origin", "A translation 2 units left"],
         "B is the mirror image of A across the <i>y</i>-axis: <b>a reflection in the <i>y</i>-axis</b>."),
        ([(-x, -y) for x, y in A], "A rotation of 180° about the origin", ["A reflection in the <i>y</i>-axis", "A reflection in the <i>x</i>-axis", "A translation"],
         "B is upside down in the opposite quadrant: <b>a rotation of 180° about the origin</b>."),
        ([(x - 5, y - 4) for x, y in A], "A translation 5 units left and 4 units down", ["A translation 4 units left and 5 units down", "A rotation of 90° clockwise", "A reflection in the <i>y</i>-axis"],
         "Every point moves 5 left and 4 down: <b>a translation 5 units left and 4 units down</b>."),
        ([(x, -y) for x, y in A], "A reflection in the <i>x</i>-axis", ["A reflection in the <i>y</i>-axis", "A rotation of 90° clockwise about the origin", "A translation 4 units down"],
         "B is the mirror image of A across the <i>x</i>-axis: <b>a reflection in the <i>x</i>-axis</b>."),
        ([(y, -x) for x, y in A], "A rotation of 90° clockwise about the origin", ["A rotation of 90° anticlockwise about the origin", "A reflection in the <i>x</i>-axis", "A rotation of 180° about the origin"],
         "Each point (<i>x</i>, <i>y</i>) goes to (<i>y</i>, −<i>x</i>): <b>a rotation of 90° clockwise about the origin</b>."),
    ]:
        g = grid(lines=poly_line(A, BLUE) + poly_line(img, RED))
        ca = (sum(x for x, _ in A) / 3.0, sum(y for _, y in A) / 3.0)
        cb = (sum(x for x, _ in img) / 3.0, sum(y for _, y in img) / 3.0)
        g = g.replace("</g></svg>", text(30 + (ca[0] + 5) * 24, 30 + (5 - ca[1]) * 24 + 5, "A", 14, col=BLUE)
                      + text(30 + (cb[0] + 5) * 24, 30 + (5 - cb[1]) * 24 + 5, "B", 14, col=RED) + "</g></svg>")
        its.append(T("Shape A (blue) is mapped onto shape B (red). Describe the single transformation.%s" % fig(g), right, wr, e))
    data = [
        ("After a reflection, rotation or translation, the image is…", "congruent to the original", ["bigger than the original", "always the same way up", "always in the same place"],
         "These keep every length and angle, so the image is <b>congruent</b>."),
        ("To describe a rotation fully, you must give…", "the angle, the direction and the centre", ["only the angle", "the angle and the direction", "the mirror line"], "A full description needs <b>the angle, the direction and the centre</b>."),
        ("Which point does not move when it is reflected in the <i>x</i>-axis?", "(4, 0)", ["(0, 4)", "(4, 4)", "(−4, 4)"], "Points on the mirror line stay where they are: <b>(4, 0)</b>."),
        ("A shape is rotated 90° clockwise and then another 90° clockwise about the same centre. What single rotation is this?", "180° about the same centre", ["90° anticlockwise", "360°", "No rotation"], "90° + 90° = <b>180°</b>."),
        ("Which is the same as a rotation of 270° anticlockwise?", "90° clockwise", ["90° anticlockwise", "180°", "270° clockwise"], "270° one way ends in the same place as <b>90° the other way</b>."),
        ("The point (5, 2) is rotated 90° anticlockwise about the origin. Where is its image?", "(−2, 5)", ["(2, −5)", "(−5, −2)", "(5, −2)"], "(<i>x</i>, <i>y</i>) → (−<i>y</i>, <i>x</i>): <b>(−2, 5)</b>."),
        ("A point (2, −3) is reflected in the line <i>x</i> = 4. Where is its image?", "(6, −3)", ["(2, 11)", "(−6, −3)", "(4, −3)"], "2 is 2 left of the line, so the image is 2 right of it: <b>(6, −3)</b>."),
        ("Which transformation could map the letter b onto the letter d?", "A reflection in a vertical line", ["A rotation of 90°", "A translation", "A rotation of 180°"], "b and d are mirror images: <b>a reflection in a vertical line</b>."),
        ("Which transformation could map the letter b onto the letter q?", "A rotation of 180°", ["A reflection in a vertical line", "A translation", "A rotation of 90° clockwise"], "Turning b upside down gives q: <b>a rotation of 180°</b>."),
        ("A translation moves (1, 1) to (4, −2). Where does the same translation move (0, 5)?", "(3, 2)", ["(−3, 8)", "(3, 8)", "(4, 3)"], "The move is 3 right and 3 down: (0 + 3, 5 − 3) = <b>(3, 2)</b>."),
        ("Reflecting in the <i>y</i>-axis changes…", "the sign of the <i>x</i>-coordinate", ["the sign of the <i>y</i>-coordinate", "both signs", "nothing"], "The <i>y</i>-axis is vertical, so points move left or right: <b>the sign of the <i>x</i>-coordinate</b> changes."),
        ("Rotating 180° about the origin changes…", "the signs of both coordinates", ["only the <i>x</i>-coordinate", "only the <i>y</i>-coordinate", "nothing"], "(<i>x</i>, <i>y</i>) → (−<i>x</i>, −<i>y</i>): <b>both signs change</b>."),
        ("A shape is reflected in the <i>x</i>-axis and then reflected again in the <i>x</i>-axis. Where does it end up?", "Back where it started", ["In the opposite quadrant", "Rotated 90°", "Translated down"], "Two reflections in the same line undo each other: <b>back where it started</b>."),
        ("Which coordinates show a square's corner (3, 1) after a translation 4 units left?", "(−1, 1)", ["(7, 1)", "(3, −3)", "(−4, 1)"], "Left changes <i>x</i>: 3 − 4 = −1. <b>(−1, 1)</b>."),
        ("A game character at (−2, 3) moves 5 right and 6 down. Where is it now?", "(3, −3)", ["(−7, 9)", "(4, −2)", "(3, 9)"], "(−2 + 5, 3 − 6) = <b>(3, −3)</b>."),
    ]
    its += [T(q, a[0].upper() + a[1:] if a[0].islower() else a, [w[0].upper() + w[1:] if w[0].islower() else w for w in ws], e) for q, a, ws, e in data]
    return its


def body():
    return lesson(
        "<ul><li><b>Reflection</b> in the <i>x</i>-axis: (<i>x</i>, <i>y</i>) → (<i>x</i>, −<i>y</i>). In the <i>y</i>-axis: (<i>x</i>, <i>y</i>) → (−<i>x</i>, <i>y</i>).</li>"
        "<li><b>Rotation</b>: give the angle, the direction (clockwise or anticlockwise) and the centre. "
        "180° about the origin: (<i>x</i>, <i>y</i>) → (−<i>x</i>, −<i>y</i>).</li>"
        "<li><b>Translation</b>: every point slides the same way, such as 3 units right and 2 units down.</li></ul>"
        "<p>All three keep the shape the same size and shape, so the image is <b>congruent</b>.</p>",
        [("Reflect (3, −2) in the <i>y</i>-axis.", ["Change the sign of the <i>x</i>-coordinate."], "(−3, −2)"),
         ("Translate (1, 4) 3 units right and 5 units down.", ["1 + 3 = 4 and 4 − 5 = −1."], "(4, −1)"),
         ("Rotate (2, 5) 180° about the origin.", ["Change both signs."], "(−2, −5)")],
        ["Reflecting in the wrong axis: the <i>x</i>-axis is horizontal, so reflecting in it changes the <i>y</i>-coordinate.",
         "Rotating the wrong way: anticlockwise is the opposite way to clock hands.",
         "Swapping the moves: right and left change <i>x</i>; up and down change <i>y</i>.",
         "Forgetting the centre of rotation when it is not the origin."])


def main():
    sets = [S("Reflections", collect(one_reflect, 20, R)),
            S("Rotations", collect(one_rotate, 20, R)),
            S("Translations", collect(one_translate, 20, R)),
            S("Transforming shapes", collect(one_shape, 20, R)),
            S("Describing transformations", problems())]
    make(7, "transformations-on-the-cartesian-plane", 18, "AC9M7SP03",
         "Transformations on the Cartesian Plane: Reflections, Rotations and Translations",
         "Year 7 Transformations Worksheets: Reflections, Rotations and Translations on the Cartesian Plane (Free, Answer Key)",
         "Transformations",
         "describe transformations of a set of points using coordinates in the Cartesian plane, translations and reflections on an axis, "
         "and rotations about a given point",
         "Free Year 7 maths worksheets on transformations for the Australian Curriculum (AC9M7SP03): reflections in the axes, "
         "rotations about a point, translations, transforming shapes and describing transformations. 100 questions with an answer key.",
         "Reflection: mirror line. Rotation: angle, direction, centre. Translation: how far across and up or down.",
         "Reflections, rotations and translations keep the shape the same size (congruent).",
         body(),
         [("What happens to coordinates when you reflect in the x-axis?", "The y-coordinate changes sign: (3, 2) becomes (3, −2)."),
          ("How do I describe a rotation?", "Give the angle (such as 90° or 180°), the direction (clockwise or anticlockwise) and the centre of rotation."),
          ("How do I translate a point?", "Add the move across to the x-coordinate and the move up or down to the y-coordinate. Left and down are negative."),
          ("What does congruent mean?", "Exactly the same size and shape. Reflections, rotations and translations always give a congruent image.")],
         sets, R)


if __name__ == "__main__":
    main()
