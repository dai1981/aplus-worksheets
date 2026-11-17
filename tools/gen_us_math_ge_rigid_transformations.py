# -*- coding: utf-8 -*-
"""
US Geometry: Rigid Transformations (Common Core G-CO.A.5, G-CO.A.2, G-CO.A.3)
  python3 tools/gen_us_math_ge_rigid_transformations.py
Translations with coordinate rules, reflections over the axes and the lines y = x, y = −x, x = k and y = k,
rotations about the origin, identifying and composing transformations, and symmetry and properties.
Wrong answers come from real mistakes: changing the wrong coordinate in a reflection, mixing up 90° and 270°
rotation rules, forgetting to swap the coordinates, and doing a composition in the wrong order.
"""
import random
from us_hs import B, S, make, lesson, collect, T, fig, num, MINUS
from g8_common import grid_svg
from us_geo import RED, GREEN, BLUE

R = random.Random(92801)
X, Y = "<i>x</i>", "<i>y</i>"


def sg(n):
    return num(n) if n >= 0 else MINUS + num(-n)


def pt(p):
    return "(%s, %s)" % (sg(p[0]), sg(p[1]))


def shift(a, var):
    if a == 0:
        return var
    return "%s %s %s" % (var, "+" if a > 0 else MINUS, num(abs(a)))


REFL = {
    "the <i>x</i>-axis": lambda p: (p[0], -p[1]),
    "the <i>y</i>-axis": lambda p: (-p[0], p[1]),
    "the line <i>y</i> = <i>x</i>": lambda p: (p[1], p[0]),
    "the line <i>y</i> = %s<i>x</i>" % MINUS: lambda p: (-p[1], -p[0]),
}
ROT = {
    "90° counterclockwise": lambda p: (-p[1], p[0]),
    "180°": lambda p: (-p[0], -p[1]),
    "270° counterclockwise": lambda p: (p[1], -p[0]),
    "90° clockwise": lambda p: (p[1], -p[0]),
}
RULE = {
    "the <i>x</i>-axis": "(<i>x</i>, <i>y</i>) → (<i>x</i>, %s<i>y</i>)" % MINUS,
    "the <i>y</i>-axis": "(<i>x</i>, <i>y</i>) → (%s<i>x</i>, <i>y</i>)" % MINUS,
    "the line <i>y</i> = <i>x</i>": "(<i>x</i>, <i>y</i>) → (<i>y</i>, <i>x</i>)",
    "the line <i>y</i> = %s<i>x</i>" % MINUS: "(<i>x</i>, <i>y</i>) → (%s<i>y</i>, %s<i>x</i>)" % (MINUS, MINUS),
    "90° counterclockwise": "(<i>x</i>, <i>y</i>) → (%s<i>y</i>, <i>x</i>)" % MINUS,
    "180°": "(<i>x</i>, <i>y</i>) → (%s<i>x</i>, %s<i>y</i>)" % (MINUS, MINUS),
    "270° counterclockwise": "(<i>x</i>, <i>y</i>) → (<i>y</i>, %s<i>x</i>)" % MINUS,
    "90° clockwise": "(<i>x</i>, <i>y</i>) → (<i>y</i>, %s<i>x</i>)" % MINUS,
}


def rp(r, lo=-8, hi=8):
    while True:
        p = (r.randint(lo, hi), r.randint(lo, hi))
        if p[0] and p[1] and abs(p[0]) != abs(p[1]):
            return p


# ------------------------------------------------------------ set 1: translations
def one_tr(r):
    a, b = r.randint(-7, 7), r.randint(-7, 7)
    if a == 0 or b == 0:
        return None
    P = rp(r)
    rule = "(<i>x</i>, <i>y</i>) → (%s, %s)" % (shift(a, X), shift(b, Y))
    kind = r.choice(["apply", "apply", "find", "pre"])
    if kind == "apply":
        q = "Point A%s is translated by the rule %s. What are the coordinates of A′?" % (pt(P), B(rule))
        ans = (P[0] + a, P[1] + b)
        wr = [(P[0] + b, P[1] + a), (P[0] - a, P[1] - b), (P[0] + a, P[1] - b), (P[0] * a, P[1] * b)]
        e = "Add %s to <i>x</i> and %s to <i>y</i>: (%s + %s, %s + %s) = <b>%s</b>." % (sg(a), sg(b), sg(P[0]), "(%s)" % sg(a) if a < 0 else sg(a),
                                                                                  sg(P[1]), "(%s)" % sg(b) if b < 0 else sg(b), pt(ans))
        return T(q, pt(ans), [pt(w) for w in dict.fromkeys(wr) if w != ans][:3], e)
    Q = (P[0] + a, P[1] + b)
    if kind == "pre":
        q = "A translation by the rule %s maps point A to A′%s. What are the coordinates of A?" % (B(rule), pt(Q))
        wr = [(Q[0] + a, Q[1] + b), (Q[0] - b, Q[1] - a), (Q[0] + a, Q[1] - b)]
        e = "Undo the translation: subtract %s from <i>x</i> and %s from <i>y</i>. A = <b>%s</b>." % (sg(a), sg(b), pt(P))
        return T(q, pt(P), [pt(w) for w in dict.fromkeys(wr) if w != P][:3], e)
    q = "A translation maps A%s to A′%s. Which rule describes it?" % (pt(P), pt(Q))
    wrong = ["(<i>x</i>, <i>y</i>) → (%s, %s)" % (shift(-a, X), shift(-b, Y)), "(<i>x</i>, <i>y</i>) → (%s, %s)" % (shift(b, X), shift(a, Y)),
             "(<i>x</i>, <i>y</i>) → (%s, %s)" % (shift(a, X), shift(-b, Y))]
    e = "Change in <i>x</i>: %s %s %s = %s. Change in <i>y</i>: %s %s %s = %s. <b>%s</b>." % (
        sg(Q[0]), MINUS, "(%s)" % sg(P[0]) if P[0] < 0 else sg(P[0]), sg(a), sg(Q[1]), MINUS, "(%s)" % sg(P[1]) if P[1] < 0 else sg(P[1]), sg(b), rule)
    return T(q, rule, [w for w in dict.fromkeys(wrong) if w != rule], e)


# ------------------------------------------------------------ set 2: reflections
def one_ref(r):
    P = rp(r)
    if r.random() < 0.72:
        k = r.choice(list(REFL))
        ans = REFL[k](P)
        wr = [f(P) for kk, f in REFL.items() if kk != k] + [(-P[0], -P[1])]
        q = "Reflect A%s over %s. What are the coordinates of A′?" % (pt(P), k)
        e = "Reflection over %s: %s. A′ = <b>%s</b>." % (k, RULE[k], pt(ans))
        return T(q, pt(ans), [pt(w) for w in dict.fromkeys(wr) if w != ans][:3], e)
    c = r.choice([-4, -3, -2, -1, 1, 2, 3, 4])
    if r.random() < 0.5:
        line_ = "the line <i>x</i> = %s" % sg(c)
        ans = (2 * c - P[0], P[1])
        wr = [(-P[0], P[1]), (P[0], 2 * c - P[1]), (c - P[0], P[1]), (2 * c + P[0], P[1])]
        e = "A is %s unit%s %s of <i>x</i> = %s. Go the same distance to the other side: <i>x</i> = %s. The <i>y</i>-coordinate stays. <b>%s</b>." % (
            num(abs(P[0] - c)), "" if abs(P[0] - c) == 1 else "s", "right" if P[0] > c else "left", sg(c), sg(2 * c - P[0]), pt(ans))
    else:
        line_ = "the line <i>y</i> = %s" % sg(c)
        ans = (P[0], 2 * c - P[1])
        wr = [(P[0], -P[1]), (2 * c - P[0], P[1]), (P[0], c - P[1]), (P[0], 2 * c + P[1])]
        e = "A is %s unit%s %s <i>y</i> = %s. Go the same distance to the other side: <i>y</i> = %s. The <i>x</i>-coordinate stays. <b>%s</b>." % (
            num(abs(P[1] - c)), "" if abs(P[1] - c) == 1 else "s", "above" if P[1] > c else "below", sg(c), sg(2 * c - P[1]), pt(ans))
    if ans == P:
        return None
    q = "Reflect A%s over %s. What are the coordinates of A′?" % (pt(P), line_)
    return T(q, pt(ans), [pt(w) for w in dict.fromkeys(wr) if w != ans][:3], e)


# ------------------------------------------------------------ set 3: rotations about the origin
def one_rot(r):
    P = rp(r)
    k = r.choice(list(ROT))
    ans = ROT[k](P)
    if r.random() < 0.75:
        wr = [f(P) for kk, f in ROT.items()] + [(P[1], P[0]), (-P[0], P[1])]
        q = "Rotate A%s %s about the origin. What are the coordinates of A′?" % (pt(P), k)
        e = "Rotation %s: %s. A′ = <b>%s</b>." % (k, RULE[k], pt(ans))
        if k == "90° clockwise":
            e += " (90° clockwise is the same as 270° counterclockwise.)"
        return T(q, pt(ans), [pt(w) for w in dict.fromkeys(wr) if w != ans][:3], e)
    q = "A rotation about the origin maps A%s to A′%s. Which rotation is it?" % (pt(P), pt(ans))
    right = {"90° counterclockwise": "90° counterclockwise", "180°": "180°", "270° counterclockwise": "90° clockwise", "90° clockwise": "90° clockwise"}[k]
    e = "Test the rules: %s gives %s. <b>%s</b>." % (RULE[k], pt(ans), right)
    return T(q, right, [x for x in ["90° counterclockwise", "180°", "90° clockwise", "360°"] if x != right], e)


# ------------------------------------------------------------ set 4: identify and compose
TRI = [(1, 1), (4, 1), (1, 3)]


def one_id(r):
    if r.random() < 0.55:
        kind = r.choice(["tr", "rx", "ry", "r180", "r90", "ryx"])
        if kind == "ryx":
            base = r.choice([[(3, 1), (6, 1), (5, 3)], [(4, 1), (6, 2), (3, 2)], [(2, 0), (5, 1), (6, 3)]])
        else:
            base = r.choice([[(1, 1), (4, 1), (1, 3)], [(2, 1), (5, 2), (2, 4)], [(1, 2), (3, 1), (4, 4)], [(2, 2), (6, 2), (3, 5)]])
        if kind == "tr":
            a, b = r.choice([(-6, 1), (-5, -6), (1, -6), (-6, -4), (2, -7)])
            img = [(x + a, y + b) for x, y in base]
            right = "A translation by (<i>x</i>, <i>y</i>) → (%s, %s)" % (shift(a, X), shift(b, Y))
        elif kind == "rx":
            img = [(x, -y) for x, y in base]
            right = "A reflection over the <i>x</i>-axis"
        elif kind == "ry":
            img = [(-x, y) for x, y in base]
            right = "A reflection over the <i>y</i>-axis"
        elif kind == "r180":
            img = [(-x, -y) for x, y in base]
            right = "A rotation of 180° about the origin"
        elif kind == "r90":
            img = [(-y, x) for x, y in base]
            right = "A rotation of 90° counterclockwise about the origin"
        else:
            img = [(y, x) for x, y in base]
            right = "A reflection over the line <i>y</i> = <i>x</i>"
        pts = [(x, y, n, BLUE) for (x, y), n in zip(base, ["A", "B", "C"])] + [(x, y, n, RED) for (x, y), n in zip(img, ["A′", "B′", "C′"])]
        svg = grid_svg(-7, 7, points=pts, polys=[(base, "#cfe6d6", BLUE), (img, "#f6d5d0", RED)], unit=17, label="triangle ABC and its image")
        q = "Which transformation maps triangle ABC to triangle A′B′C′?%s" % fig(svg)
        pool = ["A reflection over the <i>x</i>-axis", "A reflection over the <i>y</i>-axis", "A rotation of 180° about the origin",
                "A rotation of 90° counterclockwise about the origin", "A reflection over the line <i>y</i> = <i>x</i>",
                "A rotation of 90° clockwise about the origin"]
        wr = [p for p in pool if p != right]
        rot = (len(base) + base[0][0] + base[1][1]) % len(wr)
        wr = wr[rot:] + wr[:rot]
        e = "Compare a vertex: A%s goes to A′%s. %s. <b>%s</b>." % (pt(base[0]), pt(img[0]), {
            "tr": "Every point moves the same way and the triangle keeps its orientation",
            "rx": "<i>x</i> stays and <i>y</i> changes sign", "ry": "<i>y</i> stays and <i>x</i> changes sign",
            "r180": "Both coordinates change sign", "r90": "(<i>x</i>, <i>y</i>) → (%s<i>y</i>, <i>x</i>)" % MINUS,
            "ryx": "The coordinates swap"}[kind], right)
        return T(q, right, wr[:3], e)
    P = rp(r, -6, 6)
    a, b = r.randint(-5, 5), r.randint(-5, 5)
    if a == 0 or b == 0:
        return None
    k = r.choice(list(REFL)[:2] + ["180°", "90° counterclockwise"])
    f = REFL.get(k) or ROT.get(k)
    first_tr = r.random() < 0.5
    if first_tr:
        ans = f((P[0] + a, P[1] + b))
        other = (f(P)[0] + a, f(P)[1] + b)
        desc = "translate it by (<i>x</i>, <i>y</i>) → (%s, %s), then %s" % (shift(a, X), shift(b, Y),
                                                                      ("reflect it over " + k) if k in REFL else ("rotate it " + k + " about the origin"))
        mid = (P[0] + a, P[1] + b)
    else:
        ans = (f(P)[0] + a, f(P)[1] + b)
        other = f((P[0] + a, P[1] + b))
        desc = "%s, then translate it by (<i>x</i>, <i>y</i>) → (%s, %s)" % (("reflect it over " + k) if k in REFL else ("rotate it " + k + " about the origin"),
                                                                       shift(a, X), shift(b, Y))
        mid = f(P)
    if ans == other:
        return None
    q = "Start with A%s: %s. Where does A end up?" % (pt(P), desc)
    wr = [other, (ans[0], -ans[1]), (P[0] + a, P[1] + b)]
    e = "Do the steps in order. After the first step: %s. After the second step: <b>%s</b>. The order matters: the other order gives %s." % (pt(mid), pt(ans), pt(other))
    return T(q, pt(ans), [pt(w) for w in dict.fromkeys(wr) if w != ans][:3], e)


# ------------------------------------------------------------ set 5: properties and symmetry
POLY = [("equilateral triangle", 3), ("square", 4), ("regular pentagon", 5), ("regular hexagon", 6), ("regular octagon", 8),
        ("regular decagon", 10), ("regular 12-gon", 12), ("regular nonagon", 9)]


def one_sym(r):
    kind = r.choice(["rot", "rot", "lines", "prop", "prop", "map"])
    if kind == "rot":
        name, n = r.choice(POLY)
        q = "What is the smallest angle of rotation that maps a %s onto itself?" % B(name)
        ans = 360 // n if 360 % n == 0 else None
        if ans is None:
            return None
        wr = [180 * (n - 2) // n, 180 // n if 180 % n == 0 else ans * 2, 360]
        e = "Rotating by one vertex: 360° ÷ %d = <b>%d°</b>." % (n, ans)
        return T(q, "%d°" % ans, ["%d°" % w for w in dict.fromkeys(wr) if w != ans][:3], e)
    if kind == "lines":
        name, n = r.choice(POLY + [("rectangle (not a square)", 2), ("rhombus (not a square)", 2), ("isosceles triangle (not equilateral)", 1),
                                   ("parallelogram (not a rectangle or rhombus)", 0)])
        q = "How many lines of symmetry does a %s have?" % B(name)
        wr = [n + 2, 2 * n if n else 1, n - 1 if n > 1 else 4, 4]
        e = {0: "No line folds it onto itself, although it has 180° rotational symmetry. <b>0</b>.",
             1: "Only the line through the vertex angle and the midpoint of the base. <b>1</b>.",
             2: "The lines through the midpoints of opposite sides (rectangle) or through opposite vertices (rhombus). <b>2</b>."}.get(
            n, "A regular polygon with %d sides has %d lines of symmetry. <b>%d</b>." % (n, n, n))
        return T(q, num(n), [num(w) for w in dict.fromkeys(wr) if w != n and w >= 0][:3], e)
    if kind == "map":
        items = [("Which transformation maps a rectangle onto itself?", "A rotation of 180° about its center",
                  ["A rotation of 90° about its center", "A reflection over a diagonal", "A translation along a side"],
                  "A rectangle that is not a square only matches itself after a half turn (or a reflection over a line through the midpoints of opposite sides)."),
                 ("Which transformation does NOT map a square onto itself?", "A reflection over a line through one vertex and the midpoint of a side",
                  ["A rotation of 90° about its center", "A reflection over a diagonal", "A rotation of 270° about its center"],
                  "Squares have 4 lines of symmetry: 2 diagonals and 2 lines through midpoints of opposite sides."),
                 ("A figure is reflected over the <i>y</i>-axis and then over the <i>x</i>-axis. Which single transformation has the same result?", "A rotation of 180° about the origin",
                  ["A reflection over the line <i>y</i> = <i>x</i>", "A rotation of 90° about the origin", "A translation"],
                  "(<i>x</i>, <i>y</i>) → (%s<i>x</i>, <i>y</i>) → (%s<i>x</i>, %s<i>y</i>), which is the 180° rotation rule." % (MINUS, MINUS, MINUS)),
                 ("A figure is reflected over two parallel lines. Which single transformation has the same result?", "A translation",
                  ["A rotation", "A reflection", "A dilation"], "Two reflections over parallel lines make a translation, twice the distance between the lines.")]
        q, right, wr, e = r.choice(items)
        return T(q, right, wr, e + " <b>%s</b>." % right)
    items = [("Which is preserved by every rigid transformation?", "Side lengths and angle measures", ["Orientation", "Position on the plane", "The slope of each side"],
              "Rigid motions keep size and shape, so the image is congruent. Orientation can change in a reflection."),
             ("Which transformation changes the orientation of a figure (clockwise order of the vertices)?", "A reflection", ["A translation", "A rotation", "A rotation of 180°"],
              "A reflection flips a figure, so A, B, C clockwise become A′, B′, C′ counterclockwise."),
             ("Triangle ABC is rotated 90° about the origin. AB = 7 and m∠B = 48°. What are A′B′ and m∠B′?", "A′B′ = 7 and m∠B′ = 48°",
              ["A′B′ = 7 and m∠B′ = 138°", "A′B′ = 14 and m∠B′ = 48°", "A′B′ = 7 and m∠B′ = 42°"], "A rotation is rigid, so lengths and angles do not change."),
             ("Which transformation is NOT a rigid transformation?", "A dilation with scale factor 2", ["A translation", "A reflection", "A rotation"],
              "A dilation changes the size, so lengths are not preserved."),
             ("If a rigid transformation maps triangle ABC to triangle DEF, what can you conclude?", "The triangles are congruent",
              ["The triangles are similar but not congruent", "The triangles have the same orientation", "Point A and point D are the same point"],
              "Rigid transformations preserve distance and angle measure, so the figures are congruent."),
             ("Under a translation, a segment and its image are always", "Parallel (or on the same line) and the same length",
              ["Perpendicular", "Different lengths", "Reflected copies"], "A translation slides every point the same distance in the same direction."),
             ("A point is rotated 360° about the origin. Where does it end up?", "At its starting point", ["On the opposite side of the origin", "Reflected over the <i>x</i>-axis", "At the origin"],
              "A full turn brings every point back to where it started.")]
    q, right, wr, e = r.choice(items)
    return T(q, right, wr, e + " <b>%s</b>." % right)


def build():
    sets = [S("Translations", collect(one_tr, 20, R)),
            S("Reflections", collect(one_ref, 20, R)),
            S("Rotations about the origin", collect(one_rot, 20, R)),
            S("Identify and compose transformations", collect(one_id, 20, R)),
            S("Properties and symmetry", collect(one_sym, 20, R))]
    rules = "".join("<li>%s %s: %s</li>" % ("Reflect over" if k in REFL else "Rotate", k, RULE[k]) for k in list(REFL) + ["90° counterclockwise", "180°", "270° counterclockwise"])
    body = lesson(
        "<p>A <b>rigid transformation</b> (isometry) moves a figure without changing its size or shape, so the image is congruent. "
        "Translations, reflections and rotations are rigid. A reflection changes orientation; the others do not.</p>"
        "<ul><li>Translate by (<i>a</i>, <i>b</i>): (<i>x</i>, <i>y</i>) → (<i>x</i> + <i>a</i>, <i>y</i> + <i>b</i>)</li>%s</ul>"
        "<p>Rotations are counterclockwise unless the problem says clockwise. 90° clockwise is the same as 270° counterclockwise. "
        "In a composition, do the first step first; the order can change the result.</p>" % rules,
        [("Rotate A(3, %s5) 90° counterclockwise about the origin." % MINUS, ["Rule: (<i>x</i>, <i>y</i>) → (%s<i>y</i>, <i>x</i>)" % MINUS, "(%s(%s5), 3)" % (MINUS, MINUS)], "A′(5, 3)"),
         ("Reflect A(6, 1) over the line <i>x</i> = 2.", ["A is 4 units right of <i>x</i> = 2", "Go 4 units left of the line: <i>x</i> = %s2" % MINUS], "A′(%s2, 1)" % MINUS)],
        ["Changing the wrong coordinate. Over the <i>x</i>-axis, <i>x</i> stays and <i>y</i> changes sign.",
         "Forgetting to swap the coordinates for a 90° rotation or a reflection over <i>y</i> = <i>x</i>.",
         "Mixing up clockwise and counterclockwise.",
         "Reflecting over <i>x</i> = 2 by changing the sign of <i>x</i>. Measure the distance to the line instead."])
    faq = [("What is the rule for a 90 degree counterclockwise rotation?", "(x, y) → (−y, x). Swap the coordinates and change the sign of the new x-coordinate."),
           ("What is the rule for reflecting over y = x?", "(x, y) → (y, x). Swap the coordinates."),
           ("What is a rigid transformation?", "A transformation that keeps lengths and angle measures the same: a translation, reflection or rotation. The image is congruent to the original."),
           ("Does the order of transformations matter?", "Often, yes. A translation followed by a rotation usually gives a different result than the rotation followed by the translation.")]
    make("rigid-transformations", 8, "G-CO.A.5",
         "Rigid Transformations: Translations, Reflections, and Rotations",
         "Rigid Transformations Worksheet: Translations, Reflections, Rotations (Geometry) | 100 Questions",
         "Rigid Transformations",
         "Given a geometric figure and a rotation, reflection, or translation, draw the transformed figure using, e.g., graph paper, tracing paper, or geometry software. Specify a sequence of transformations that will carry a given figure onto another.",
         "Free Geometry worksheet on rigid transformations: translation rules, reflections over lines, rotations about the origin, compositions and symmetry. 100 questions with answers.",
         "Rigid transformations keep size and shape: the image is congruent.",
         "Rotate 90° counterclockwise: (x, y) → (−y, x). Reflect over y = x: (x, y) → (y, x).",
         body, faq, sets, R, domain="Transformations", grade="geometry")


if __name__ == "__main__":
    build()
