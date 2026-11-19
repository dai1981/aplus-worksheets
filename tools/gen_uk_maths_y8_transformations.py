# -*- coding: utf-8 -*-
"""
UK Year 8 Maths: Transformations (KS3 Geometry and measures)
  python3 tools/gen_uk_maths_y8_transformations.py
Reflections in x = a, y = b, y = x and y = −x; rotations of 90° and 180° about a point; translations by a
column vector; enlargements with a scale factor and centre; and describing transformations.
Wrong answers come from real mistakes: reflecting in the wrong axis, rotating the wrong way, mixing up the
top and bottom numbers of a vector, and adding instead of multiplying for an enlargement.
"""
import random
from fractions import Fraction as F
from uk_ks3 import num, mcq, B, S, make, lesson, collect, T, fig, RED, BLUE, GREEN, svg_wrap, text, line, INK
from gen_uk_maths_y7_coordinates_and_straight_line_graphs import grid

R = random.Random(81401)


def P(x, y):
    return "(%s, %s)" % (num(x), num(y))


def vec(a, b):
    return ("<span style='display:inline-block;vertical-align:middle;text-align:center;line-height:1.1;"
            "border-left:2px solid;border-right:2px solid;border-radius:9px;padding:1px 7px'>%s<br>%s</span>" % (num(a), num(b)))


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
    kind = r.choice(["x=", "y=", "x=", "y=", "y=x", "y=-x"])
    c = r.choice([0, 0, 1, -1, 2, -2]) if kind in ("x=", "y=") else 0
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
    if a == 0 or b == 0:
        return None
    p = (r.randint(-5, 5), r.randint(-5, 5))
    img = (p[0] + a, p[1] + b)
    if r.random() < 0.6:
        q = "The point %s is translated by the vector %s. Where is its image?" % (B(P(*p)), vec(a, b))
        right = P(*img)
        wr = [P(p[0] + b, p[1] + a), P(p[0] - a, p[1] - b), P(p[0] + a, p[1] - b)]
        e = "The top number moves %s %d; the bottom number moves %s %d. Image: <b>%s</b>." % (
            "right" if a > 0 else "left", abs(a), "up" if b > 0 else "down", abs(b), right)
        return T(q, right, [w for w in wr if w != right], e)
    q = "A shape moves %d %s and %d %s. Which column vector describes this translation?" % (abs(a), "right" if a > 0 else "left", abs(b), "up" if b > 0 else "down")
    right = vec(a, b)
    wr = [vec(b, a), vec(-a, -b), vec(a, -b)]
    return T(q, right, [w for w in wr if w != right], "Top: across (%s), bottom: up/down (%s): <b>%s</b>." % (num(a), num(b), right))


# ------------------------------------------------------------ set 4: enlargement
def one_enlarge(r):
    kind = r.randint(0, 2)
    if kind == 0:
        k = r.choice([2, 3, 4, F(1, 2), F(3, 2), F(5, 2)])
        sides = r.sample(range(2, 10), 2)
        if any((s * k).denominator > 2 for s in [F(x) for x in sides]):
            return None
        q = "A rectangle %d cm by %d cm is enlarged by scale factor %s. What are the new side lengths?" % (sides[0], sides[1], num(k))
        right = "%s cm by %s cm" % (num(sides[0] * k), num(sides[1] * k))
        wr = ["%s cm by %s cm" % (num(sides[0] + k), num(sides[1] + k)), "%s cm by %s cm" % (num(sides[0] * k * k), num(sides[1] * k * k)),
              "%s cm by %s cm" % (num(F(sides[0]) / k) or num(F(sides[0]) / k, "f"), num(F(sides[1]) / k) or num(F(sides[1]) / k, "f"))]
        return T(q, right, [w for w in wr if w != right], "Multiply every length by %s: <b>%s</b>. (A scale factor below 1 makes the shape smaller.)" % (num(k), right))
    if kind == 1:
        k = r.choice([2, 3, F(1, 2)])
        p = (r.randint(-4, 4) * (2 if k == F(1, 2) else 1), r.randint(-4, 4) * (2 if k == F(1, 2) else 1))
        if p == (0, 0):
            return None
        img = (p[0] * k, p[1] * k)
        q = "The point %s is enlarged by scale factor %s with centre the origin. Where is its image?" % (B(P(*p)), num(k))
        right = P(*img)
        wr = [P(p[0] + k, p[1] + k), P(p[0] * k, p[1]), P(img[1], img[0]) if img[0] != img[1] else P(p[0] * k * k, p[1] * k * k)]
        return T(q, right, [w for w in wr if w != right], "From the origin, multiply both coordinates by %s: <b>%s</b>." % (num(k), right))
    small, big = r.choice([(3, 9), (4, 10), (5, 15), (6, 9), (8, 4), (12, 3), (2, 7)])
    k = F(big, small)
    q = "A side of length %d cm becomes %d cm after an enlargement. What is the scale factor?" % (small, big)
    right = num(k)
    wr = [num(F(small, big)), num(big - small), num(big * small)]
    return T(q, right, [w for w in wr if w != right], "Scale factor = new length ÷ old length = %d ÷ %d = <b>%s</b>." % (big, small, right))


# ------------------------------------------------------------ set 5: describing and problems
def tri_pts(base):
    x, y = base
    return [(x, y), (x + 2, y), (x, y + 3)]


def poly_line(pts, col):
    return [(a[0], a[1], b[0], b[1], col, "") for a, b in zip(pts, pts[1:] + pts[:1])]


def problems():
    its = []
    A = tri_pts((1, 1))
    for kind, img, right, wr, e in [
        ("refl_y", [(-x, y) for x, y in A], "A reflection in the <i>y</i>-axis", ["A reflection in the <i>x</i>-axis", "A rotation of 180° about the origin", "A translation 2 left"],
         "B is the mirror image of A across the <i>y</i>-axis: <b>a reflection in the <i>y</i>-axis</b>."),
        ("rot180", [(-x, -y) for x, y in A], "A rotation of 180° about the origin", ["A reflection in the <i>y</i>-axis", "A reflection in the <i>x</i>-axis", "A translation"],
         "B is upside down in the opposite quadrant: <b>a rotation of 180° about the origin</b>."),
        ("trans", [(x - 5, y - 4) for x, y in A], "A translation by the vector " + vec(-5, -4), ["A translation by the vector " + vec(-4, -5), "A rotation of 90° clockwise", "A reflection in <i>y</i> = <i>x</i>"],
         "Every point moves 5 left and 4 down: <b>a translation by %s</b>." % vec(-5, -4)),
        ("refl_x", [(x, -y) for x, y in A], "A reflection in the <i>x</i>-axis", ["A reflection in the <i>y</i>-axis", "A rotation of 90° clockwise about the origin", "An enlargement"],
         "B is the mirror image of A across the <i>x</i>-axis: <b>a reflection in the <i>x</i>-axis</b>."),
    ]:
        g = grid(lines=poly_line(A, BLUE) + poly_line(img, RED))
        ca = (sum(x for x, _ in A) / 3.0, sum(y for _, y in A) / 3.0)
        cb = (sum(x for x, _ in img) / 3.0, sum(y for _, y in img) / 3.0)
        g = g.replace("</g></svg>", text(30 + (ca[0] + 5) * 24, 30 + (5 - ca[1]) * 24 + 5, "A", 14, col=BLUE)
                      + text(30 + (cb[0] + 5) * 24, 30 + (5 - cb[1]) * 24 + 5, "B", 14, col=RED) + "</g></svg>")
        q = "Shape A (blue) is mapped onto shape B (red). Describe the single transformation.%s" % fig(g)
        its.append(T(q, right, wr, e))
    data = [
        ("Which transformation can change the size of a shape?", "Enlargement", ["Reflection", "Rotation", "Translation"], "Only an <b>enlargement</b> changes the size (unless the scale factor is 1)."),
        ("After a reflection, rotation or translation, the image is…", "congruent to the original", ["similar but bigger", "always the same way up", "always in the same place"],
         "These keep every length and angle, so the image is <b>congruent</b>."),
        ("To describe a rotation fully, you must give…", "the angle, the direction and the centre", ["only the angle", "the angle and the direction", "the mirror line"], "A full description needs <b>the angle, the direction and the centre</b>."),
        ("To describe an enlargement fully, you must give…", "the scale factor and the centre", ["only the scale factor", "the vector", "the angle and the centre"], "A full description needs <b>the scale factor and the centre of enlargement</b>."),
        ("A shape is enlarged by scale factor 3. What happens to its angles?", "They stay the same", ["They are multiplied by 3", "They are divided by 3", "They are multiplied by 9"], "Enlargement changes lengths, not angles: <b>they stay the same</b>."),
        ("A triangle with perimeter 12 cm is enlarged by scale factor 2.5. What is the new perimeter?", "30 cm", ["14.5 cm", "75 cm", "4.8 cm"], "Every length × 2.5: 12 × 2.5 = <b>30 cm</b>."),
        ("Point P(3, 1) is translated to P′(−1, 4). What is the translation vector?", vec(-4, 3), [vec(4, -3), vec(3, -4), vec(2, 5)], "<i>x</i>: 3 → −1 is −4; <i>y</i>: 1 → 4 is +3: <b>%s</b>." % vec(-4, 3)),
        ("Which point is unchanged by a reflection in the line <i>y</i> = <i>x</i>?", "(4, 4)", ["(4, −4)", "(4, 0)", "(0, 4)"], "Points on the mirror line do not move. (4, 4) is on <i>y</i> = <i>x</i>: <b>(4, 4)</b>."),
        ("A shape is rotated 90° clockwise and then another 90° clockwise about the same centre. What single rotation is this?", "180° about the same centre", ["90° anticlockwise", "360°", "No rotation"], "90° + 90° = <b>180°</b>."),
        ("Which is the same as a rotation of 270° anticlockwise?", "90° clockwise", ["90° anticlockwise", "180°", "270° clockwise"], "270° one way ends in the same place as <b>90° the other way</b>."),
        ("A rectangle 4 cm by 6 cm is enlarged to 10 cm by 15 cm. What is the scale factor?", "2.5", ["6", "0.4", "1.5"], "10 ÷ 4 = 15 ÷ 6 = <b>2.5</b>."),
        ("A shape is enlarged by scale factor ½. What happens to its lengths?", "They are halved", ["They are doubled", "They stay the same", "They are squared"], "Scale factor ½ makes every length <b>half</b> as long."),
        ("A point (2, −3) is reflected in the line <i>x</i> = 4. Where is its image?", "(6, −3)", ["(2, 11)", "(−6, −3)", "(4, −3)"], "2 is 2 left of the line, so the image is 2 right of it: <b>(6, −3)</b>."),
        ("The point (5, 2) is rotated 90° anticlockwise about the origin. Where is its image?", "(−2, 5)", ["(2, −5)", "(−5, −2)", "(5, −2)"], "(<i>x</i>, <i>y</i>) → (−<i>y</i>, <i>x</i>): <b>(−2, 5)</b>."),
        ("Which transformation could map the letter b onto the letter d?", "A reflection in a vertical line", ["A rotation of 90°", "A translation", "An enlargement"], "b and d are mirror images: <b>a reflection in a vertical line</b>."),
        ("Which transformation could map the letter b onto the letter q?", "A rotation of 180°", ["A reflection in a vertical line", "A translation", "An enlargement"], "Turning b upside down gives q: <b>a rotation of 180°</b>."),
    ]
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<ul><li><b>Reflection</b>: give the mirror line. Each point ends up the same distance on the other side.</li>"
        "<li><b>Rotation</b>: give the angle, the direction (clockwise or anticlockwise) and the centre.</li>"
        "<li><b>Translation</b>: give a column vector — top number across (+ right), bottom number up (+ up).</li>"
        "<li><b>Enlargement</b>: give the scale factor and the centre. Every length is multiplied by the scale factor.</li></ul>"
        "<p>Reflections, rotations and translations give a <b>congruent</b> image. Enlargements give a <b>similar</b> image.</p>",
        [("Reflect (3, −2) in the <i>y</i>-axis.", ["Change the sign of the <i>x</i>-coordinate."], "(−3, −2)"),
         ("Translate (1, 4) by %s." % vec(3, -5), ["1 + 3 = 4 and 4 − 5 = −1."], "(4, −1)"),
         ("Rotate (2, 5) 180° about the origin.", ["Change both signs."], "(−2, −5)")],
        ["Reflecting in the wrong axis: the <i>x</i>-axis is horizontal, so reflecting in it changes the <i>y</i>-coordinate.",
         "Rotating the wrong way: anticlockwise is the opposite way to clock hands.",
         "Swapping the numbers in a column vector: the top number is the horizontal move.",
         "Adding the scale factor instead of multiplying for an enlargement."])


def main():
    sets = [S("Reflections", collect(one_reflect, 20, R)),
            S("Rotations", collect(one_rotate, 20, R)),
            S("Translations and vectors", collect(one_translate, 20, R)),
            S("Enlargements", collect(one_enlarge, 20, R)),
            S("Describing transformations", problems())]
    make(8, "transformations", 14, "G",
         "Transformations: Reflection, Rotation, Translation and Enlargement",
         "Year 8 Transformations Worksheets: Reflections, Rotations, Translations with Vectors and Enlargements",
         "Transformations",
         "Identify properties of, and describe the results of, translations, rotations and reflections applied to given "
         "figures; identify, describe and construct congruent shapes including on coordinate axes; use scale factors and "
         "enlargement.",
         "Free Year 8 transformations worksheets: reflect in x = a, y = b and y = x, rotate 90° and 180°, translate by "
         "column vectors, enlarge with a scale factor and describe transformations. 100 questions with answers.",
         "Reflection: mirror line. Rotation: angle, direction, centre. Translation: column vector. Enlargement: scale factor, centre.",
         "Reflections, rotations and translations keep the shape the same size (congruent).",
         body(),
         [("How do I describe a rotation?", "Give the angle (90°, 180°…), the direction (clockwise or anticlockwise) and the centre of rotation."),
          ("What does a column vector mean?", "The top number is the move across (positive means right) and the bottom number is the move up or down (positive means up)."),
          ("What happens to coordinates when you reflect in y = x?", "The coordinates swap: (3, −1) becomes (−1, 3)."),
          ("What is the difference between congruent and similar?", "Congruent shapes are exactly the same size and shape. Similar shapes are the same shape but can be a different size, as after an enlargement.")],
         sets, R)


if __name__ == "__main__":
    main()
