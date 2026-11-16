# -*- coding: utf-8 -*-
"""
US Grade 8 Math: Transformations on the Coordinate Plane (8.G.A.1, 8.G.A.3)
  python3 tools/gen_us_math_g8_transformations.py
Translations, reflections over the axes, rotations of 90° and 180° about the origin and dilations
from the origin: find the image of a point, name the rule, and know which moves keep size and shape.
Wrong answers come from the rule for a different move: reflecting over the wrong axis, rotating the
wrong way, and adding the scale factor instead of multiplying.
"""
import random
from fractions import Fraction as F
from ws_common import num, mcq, balance, B, table, example, write_unit, fig, RED, BLUE
from g8_common import grid_svg

R = random.Random(81101)
UPDATED = "2026-11-16"
X, Y = "<i>x</i>", "<i>y</i>"


def pt(p):
    f = lambda v: num(v) if num(v) is not None else num(v, "f")
    return "(%s, %s)" % (f(p[0]), f(p[1]))


MOVES = {
    "x-axis": lambda p: (p[0], -p[1]), "y-axis": lambda p: (-p[0], p[1]),
    "90ccw": lambda p: (-p[1], p[0]), "90cw": lambda p: (p[1], -p[0]), "180": lambda p: (-p[0], -p[1]),
}
NAMES = {"x-axis": "a reflection over the x-axis", "y-axis": "a reflection over the y-axis",
         "90ccw": "a rotation of 90° counterclockwise about the origin", "90cw": "a rotation of 90° clockwise about the origin",
         "180": "a rotation of 180° about the origin"}
DESC = {"x-axis": "Only y changes sign, so the point flips over the x-axis.",
        "y-axis": "Only x changes sign, so the point flips over the y-axis.",
        "90ccw": "x and y swap and the new x changes sign: a quarter turn counterclockwise.",
        "90cw": "x and y swap and the new y changes sign: a quarter turn clockwise.",
        "180": "Both signs change: a half turn about the origin."}
RULES = {"x-axis": "(x, y) → (x, −y)", "y-axis": "(x, y) → (−x, y)", "90ccw": "(x, y) → (−y, x)",
         "90cw": "(x, y) → (y, −x)", "180": "(x, y) → (−x, −y)"}


def pchoices(p, ans, extra=()):
    cands = [MOVES[k](p) for k in MOVES] + [(p[1], p[0]), (-p[1], -p[0])] + list(extra)
    out = []
    for c in cands:
        if c != ans:
            out.append((pt(c), c))
    return out


def shape_pic(pts, img, lo=-7, hi=7):
    return grid_svg(lo, hi, polys=[(pts, "#c0392b", RED), (img, "#1f5fa8", BLUE)], unit=17)


# ============================================================ set 1: translations
def set_translate():
    its = []
    for p, (a, b) in [((2, 3), (4, 1)), ((-1, 5), (3, -2)), ((4, -2), (-5, 0)), ((0, 0), (-3, 4)), ((-4, -1), (2, 6)), ((6, 2), (-2, -5)),
                      ((-3, 4), (0, -7)), ((5, -5), (-6, 3)), ((1, -6), (4, 4)), ((-2, -2), (-3, -3))]:
        img = (p[0] + a, p[1] + b)
        rule = "(x, y) → (x %s %d, y %s %d)" % ("+" if a >= 0 else "−", abs(a), "+" if b >= 0 else "−", abs(b))
        q = "Point %s is moved by the rule %s. Where does it land?" % (B(pt(p)), B(rule))
        e = "Add to each part: %s + %s = %s and %s + %s = %s. The image is <b>%s</b>." % (
            num(p[0]), "(%s)" % num(a) if a < 0 else num(a), num(img[0]), num(p[1]), "(%s)" % num(b) if b < 0 else num(b), num(img[1]), pt(img))
        its.append(mcq(q, (pt(img), img), [(pt((p[0] + b, p[1] + a)), (p[0] + b, p[1] + a)), (pt((p[0] - a, p[1] - b)), (p[0] - a, p[1] - b)),
                                           (pt((a, b)), (a, b)), (pt((p[0] + a, p[1] - b)), (p[0] + a, p[1] - b))], e))
    for tri, (a, b) in [([(1, 1), (3, 1), (1, 4)], (3, 2)), ([(-5, 2), (-2, 2), (-4, 5)], (4, -4)), ([(0, -1), (2, -4), (-2, -4)], (-3, 5)),
                        ([(-6, -3), (-3, -2), (-5, 0)], (6, 1)), ([(2, 4), (5, 5), (4, 2)], (-6, -5))]:
        img = [(x + a, y + b) for x, y in tri]
        q = fig(shape_pic(tri, img)) + "The red triangle moves to the blue triangle. What is the rule?"
        rule = "(x, y) → (x %s %d, y %s %d)" % ("+" if a >= 0 else "−", abs(a), "+" if b >= 0 else "−", abs(b))
        e = "Each point moves %d %s and %d %s. The rule is <b>%s</b>." % (abs(a), "right" if a >= 0 else "left", abs(b),
                                                                      "up" if b >= 0 else "down", rule)
        wr = ["(x, y) → (x %s %d, y %s %d)" % ("+" if b >= 0 else "−", abs(b), "+" if a >= 0 else "−", abs(a)),
              "(x, y) → (x %s %d, y %s %d)" % ("−" if a >= 0 else "+", abs(a), "−" if b >= 0 else "+", abs(b)),
              "(x, y) → (x %s %d, y %s %d)" % ("+" if a >= 0 else "−", abs(a), "−" if b >= 0 else "+", abs(b)),
              "(x, y) → (x %s %d, y %s %d)" % ("−" if a >= 0 else "+", abs(a), "+" if b >= 0 else "−", abs(b))]
        its.append(mcq(q, (rule, rule), [(w, w) for w in wr], e))
    for q, ans, wr, e in [
        ("A shape slides 5 units left and 2 units up. Which rule is it?", "(x, y) → (x − 5, y + 2)",
         ["(x, y) → (x + 5, y − 2)", "(x, y) → (x + 2, y − 5)", "(x, y) → (x − 2, y + 5)"], "Left is −x, up is +y: <b>(x, y) → (x − 5, y + 2)</b>."),
        ("After a translation, A(1, 2) lands on A′(4, −1). Where does B(3, 5) land?", "(6, 2)", ["(0, 8)", "(6, 8)", "(4, 4)"],
         "The move is 3 right and 3 down. B′ = (3 + 3, 5 − 3) = <b>(6, 2)</b>."),
        ("A′(2, 7) is the image of A after the rule (x, y) → (x + 3, y − 4). Where was A?", "(−1, 11)", ["(5, 3)", "(−1, 3)", "(5, 11)"],
         "Undo the move: (2 − 3, 7 + 4) = <b>(−1, 11)</b>."),
        ("What does a translation change?", "Only the position", ["The size", "The shape", "The angles"],
         "A translation slides a figure: <b>only the position</b> changes."),
        ("Which point stays the same after (x, y) → (x + 0, y + 0)?", "Every point", ["Only (0, 0)", "No point", "Only points on the x-axis"],
         "Adding 0 does not move anything: <b>every point</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[1], o[15], o[2], o[10], o[3], o[16], o[4], o[11], o[5], o[18], o[6], o[12], o[7], o[17], o[8], o[13],
             o[9], o[14], o[19]]
    return {"title": "Translations", "items": order}


# ============================================================ set 2: reflections
def set_reflect():
    its = []
    for p, ax in [((3, 4), "x-axis"), ((3, 4), "y-axis"), ((-2, 5), "x-axis"), ((-2, 5), "y-axis"), ((6, -1), "x-axis"),
                  ((-4, -3), "y-axis"), ((0, 6), "x-axis"), ((5, 0), "y-axis"), ((-7, 2), "x-axis"), ((1, -6), "y-axis"),
                  ((4, 4), "x-axis"), ((-5, -5), "y-axis")]:
        img = MOVES[ax](p)
        q = "Reflect %s over the %s. What is the image?" % (B(pt(p)), ax)
        keep = "x" if ax == "x-axis" else "y"
        e = "Over the %s, keep %s and change the sign of the other: %s. The image is <b>%s</b>." % (ax, keep, RULES[ax], pt(img))
        its.append(mcq(q, (pt(img), img), pchoices(p, img), e))
    for tri, ax in [([(1, 2), (4, 2), (2, 5)], "x-axis"), ([(1, 1), (4, 3), (2, 5)], "y-axis"), ([(-5, -1), (-2, -2), (-4, -5)], "y-axis"),
                    ([(-3, 1), (-1, 5), (-5, 4)], "x-axis")]:
        img = [MOVES[ax](p) for p in tri]
        q = fig(shape_pic(tri, img)) + "Which move takes the red triangle to the blue triangle?"
        ans = NAMES[ax]
        other = "y-axis" if ax == "x-axis" else "x-axis"
        e = "The figure flips across the %s like a mirror. The answer is <b>%s</b>." % (ax, ans)
        its.append(mcq(q, (ans, ans), [(NAMES[other], 1), (NAMES["180"], 2), ("a translation", 3)], e))
    for q, ans, wr, e in [
        ("Which rule is a reflection over the y-axis?", RULES["y-axis"], [RULES["x-axis"], RULES["180"], "(x, y) → (y, x)"],
         "Over the y-axis, x changes sign: <b>%s</b>." % RULES["y-axis"]),
        ("Which point does not move when reflected over the x-axis?", "(5, 0)", ["(0, 5)", "(5, 5)", "(−5, 5)"],
         "Points on the x-axis stay put: <b>(5, 0)</b>."),
        ("Does a reflection change the size of a figure?", "No, only its position and which way it faces", ["Yes, it gets bigger", "Yes, it gets smaller", "It changes the angles"],
         "A reflection is a flip: <b>no, only its position and which way it faces</b>."),
        ("A point and its image after a reflection over the x-axis are (2, 6) and (2, −6). How far apart are they?", "12 units",
         ["6 units", "0 units", "4 units"], "From y = 6 to y = −6 is <b>12 units</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[1], o[12], o[2], o[3], o[16], o[13], o[4], o[5], o[17], o[14], o[6], o[7], o[18], o[15], o[8], o[9],
             o[19], o[10], o[11]]
    return {"title": "Reflections", "items": order}


# ============================================================ set 3: rotations
def set_rotate():
    its = []
    for p, k in [((3, 1), "90ccw"), ((3, 1), "90cw"), ((3, 1), "180"), ((-2, 4), "90ccw"), ((-2, 4), "180"), ((5, -3), "90cw"),
                 ((-1, -6), "90ccw"), ((4, 0), "90ccw"), ((0, 5), "90cw"), ((-3, -2), "180"), ((6, 2), "90cw"), ((-4, 5), "90cw"),
                 ((2, -5), "180"), ((-6, 1), "90ccw")]:
        img = MOVES[k](p)
        txt = {"90ccw": "90° counterclockwise", "90cw": "90° clockwise", "180": "180°"}[k]
        q = "Rotate %s %s about the origin. What is the image?" % (B(pt(p)), txt)
        e = "The rule for %s is %s. The image is <b>%s</b>." % (txt, RULES[k], pt(img))
        its.append(mcq(q, (pt(img), img), pchoices(p, img), e))
    for tri, k in [([(1, 1), (4, 1), (1, 3)], "180"), ([(1, 1), (4, 1), (1, 3)], "90ccw"), ([(2, 1), (5, 2), (3, 4)], "90cw")]:
        img = [MOVES[k](p) for p in tri]
        q = fig(shape_pic(tri, img)) + "Which move takes the red triangle to the blue triangle?"
        ans = NAMES[k]
        wr = [NAMES[o] for o in ["90ccw", "90cw", "180", "x-axis", "y-axis"] if o != k][:3]
        e = "Check one corner with each rule: %s gives the blue corner. The answer is <b>%s</b>." % (RULES[k], ans)
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    for q, ans, wr, e in [
        ("A rotation of 90° clockwise is the same as a rotation of …", "270° counterclockwise", ["90° counterclockwise", "180°", "360°"],
         "Going 90° one way ends in the same place as 270° the other way: <b>270° counterclockwise</b>."),
        ("After a 360° rotation, where is a point?", "Where it started", ["On the other side of the origin", "On the x-axis", "At the origin"],
         "A full turn brings it back <b>where it started</b>."),
        ("Which rule is a rotation of 180° about the origin?", RULES["180"], [RULES["x-axis"], RULES["90ccw"], "(x, y) → (y, x)"],
         "Both signs change: <b>%s</b>." % RULES["180"]),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[2], o[0], o[1], o[14], o[3], o[4], o[17], o[5], o[15], o[6], o[7], o[19], o[8], o[16], o[9], o[10], o[18],
             o[11], o[12], o[13]]
    return {"title": "Rotations about the origin", "items": order}


# ============================================================ set 4: dilations
def set_dilate():
    its = []
    for p, k in [((2, 3), 2), ((4, -1), 3), ((6, 8), F(1, 2)), ((-3, 5), 2), ((9, -6), F(1, 3)), ((1, 4), 4), ((-2, -2), 3),
                 ((10, 0), F(1, 5)), ((-4, 6), F(3, 2)), ((5, -2), 2), ((-8, -4), F(1, 4)), ((3, 7), 0)][:11]:
        img = (k * p[0], k * p[1])
        ks = num(F(k), "f") if F(k).denominator > 1 else num(k)
        q = "Dilate %s by a scale factor of %s with center at the origin. What is the image?" % (B(pt(p)), ks)
        e = "Multiply both coordinates by %s: (%s × %s, %s × %s). The image is <b>%s</b>." % (ks, num(p[0]), ks, num(p[1]), ks, pt(img))
        wr = [(p[0] + k, p[1] + k), (k * p[0], p[1]), (p[0] / F(k), p[1] / F(k)) if k else (0, 0), (p[1] * k, p[0] * k)]
        its.append(mcq(q, (pt(img), img), [(pt(w), w) for w in wr], e))
    for q, ans, wr, e in [
        ("A dilation has scale factor 3. A side is 4 cm long. How long is the side in the image?", "12 cm", ["7 cm", "4 cm", "1⅓ cm"],
         "Multiply by 3: 4 × 3 = <b>12 cm</b>."),
        ("A dilation has scale factor 1/2. What happens to the figure?", "It gets smaller", ["It gets bigger", "It stays the same size", "It flips"],
         "A scale factor between 0 and 1 shrinks it: <b>it gets smaller</b>."),
        ("A(2, 5) is dilated to A′(6, 15). What is the scale factor?", "3", ["4", "10", "1/3"], "6 ÷ 2 = 3 and 15 ÷ 5 = 3: <b>3</b>."),
        ("A(8, 4) is dilated to A′(2, 1). What is the scale factor?", "1/4", ["4", "−6", "1/2"], "2 ÷ 8 = 1/4 and 1 ÷ 4 = 1/4: <b>1/4</b>."),
        ("Which move can change the size of a figure?", "A dilation", ["A translation", "A reflection", "A rotation"],
         "Only <b>a dilation</b> changes the size."),
        ("After a dilation, which stays the same?", "The angle measures", ["The side lengths", "The area", "The perimeter"],
         "A dilation keeps the shape, so <b>the angle measures</b> stay the same."),
        ("A square with side 5 is dilated by 2. What is the new perimeter?", "40", ["20", "14", "100"],
         "New side = 10, perimeter = 4 × 10 = <b>40</b>."),
        ("Which rule is a dilation with scale factor 4 from the origin?", "(x, y) → (4x, 4y)", ["(x, y) → (x + 4, y + 4)", "(x, y) → (4x, y)", "(x, y) → (x/4, y/4)"],
         "Multiply both coordinates by 4: <b>(x, y) → (4x, 4y)</b>."),
        ("A dilation with scale factor 1 does what?", "Nothing: the figure stays the same", ["Doubles the figure", "Makes it disappear", "Flips it"],
         "Multiplying by 1 changes nothing: <b>the figure stays the same</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[11], o[1], o[12], o[2], o[15], o[3], o[13], o[4], o[16], o[5], o[14], o[6], o[17], o[7], o[18], o[8],
             o[19], o[9], o[10]]
    return {"title": "Dilations", "items": order}


# ============================================================ set 5: name the move
def set_name():
    its = []
    ALL = ["a translation", NAMES["x-axis"], NAMES["y-axis"], NAMES["90ccw"], NAMES["90cw"], NAMES["180"], "a dilation"]
    for rule, ans in [("(x, y) → (x + 2, y − 3)", "a translation"), ("(x, y) → (−x, y)", NAMES["y-axis"]), ("(x, y) → (x, −y)", NAMES["x-axis"]),
                      ("(x, y) → (−x, −y)", NAMES["180"]), ("(x, y) → (−y, x)", NAMES["90ccw"]), ("(x, y) → (y, −x)", NAMES["90cw"]),
                      ("(x, y) → (3x, 3y)", "a dilation"), ("(x, y) → (x − 6, y)", "a translation"), ("(x, y) → (0.5x, 0.5y)", "a dilation"),
                      ("(x, y) → (x, y + 4)", "a translation")]:
        q = "Which move does the rule %s describe?" % B(rule)
        wr = [a for a in ALL if a != ans]
        R.shuffle(wr)
        why = {"a translation": "Numbers are added to x and y, so every point slides the same way.",
               "a dilation": "Both coordinates are multiplied by the same number."}.get(ans, DESC[[k for k in NAMES if NAMES[k] == ans][0]] if ans in NAMES.values() else "")
        e = why + " The answer is <b>%s</b>." % ans
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    for p, img, ans in [((4, 2), (4, -2), NAMES["x-axis"]), ((4, 2), (-4, 2), NAMES["y-axis"]), ((4, 2), (-4, -2), NAMES["180"]),
                        ((4, 2), (-2, 4), NAMES["90ccw"]), ((4, 2), (8, 4), "a dilation"), ((4, 2), (7, 0), "a translation")]:
        q = "%s moves to %s. Which move could it be?" % (B(pt(p)), B(pt(img)))
        wr = [a for a in ALL if a != ans]
        R.shuffle(wr)
        why = ("The point moved %s." % ("by adding numbers" if ans == "a translation" else "by multiplying both coordinates by 2")) \
            if ans in ("a translation", "a dilation") else DESC[[k for k in NAMES if NAMES[k] == ans][0]]
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], why + " The answer is <b>%s</b>." % ans))
    for q, ans, wr, e in [
        ("Which moves keep the size and shape of a figure (rigid motions)?", "Translations, reflections and rotations",
         ["Only dilations", "Only translations", "All moves, including dilations"], "These slide, flip or turn a figure without stretching it: <b>translations, reflections and rotations</b>."),
        ("After a rotation, a segment is 5 cm long. How long was it before?", "5 cm", ["10 cm", "2.5 cm", "We cannot tell"],
         "Rotations keep lengths the same: <b>5 cm</b>."),
        ("Lines that are parallel before a reflection are … after it.", "still parallel", ["perpendicular", "the same line", "no longer lines"],
         "Rigid motions keep parallel lines <b>still parallel</b>."),
        ("A figure is reflected over the x-axis, then over the y-axis. What single move gives the same result?", NAMES["180"],
         [NAMES["90ccw"], "a translation", "a dilation"], "(x, y) → (x, −y) → (−x, −y), which is <b>%s</b>." % NAMES["180"]),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[10], o[1], o[11], o[2], o[16], o[3], o[12], o[4], o[17], o[5], o[13], o[6], o[14], o[7], o[18], o[8],
             o[15], o[9], o[19]]
    return {"title": "Name the move", "items": order}


def body():
    tri = [(1, 1), (4, 1), (1, 3)]
    return ("<h2>Four kinds of moves</h2>"
            + table(["Move", "What it does", "Rule"], [
                ["Translation", "slides", "(x, y) → (x + a, y + b)"],
                ["Reflection over the x-axis", "flips up–down", "(x, y) → (x, −y)"],
                ["Reflection over the y-axis", "flips left–right", "(x, y) → (−x, y)"],
                ["Rotation 90° counterclockwise", "turns", "(x, y) → (−y, x)"],
                ["Rotation 90° clockwise", "turns", "(x, y) → (y, −x)"],
                ["Rotation 180°", "turns halfway", "(x, y) → (−x, −y)"],
                ["Dilation by k", "makes bigger or smaller", "(x, y) → (kx, ky)"]])
            + "<figure class='sn-fig'>" + shape_pic(tri, [MOVES["180"](p) for p in tri]) + "<figcaption>A 180° rotation about the origin.</figcaption></figure>"
            + example("Reflect (3, −5) over the y-axis.", ["Over the y-axis, change the sign of x.", "(3, −5) → (−3, −5)."], "(−3, −5)")
            + "<p>Translations, reflections and rotations keep the size and shape (they are <b>rigid motions</b>). A dilation keeps the shape but changes the size.</p>"
            + "<h2>Common mistakes</h2><ul><li>Reflecting over the wrong axis: over the x-axis, y changes sign.</li>"
            "<li>Turning the wrong way: counterclockwise is the opposite of a clock.</li>"
            "<li>Adding the scale factor in a dilation. Multiply.</li></ul>")


def main():
    sets = [set_translate(), set_reflect(), set_rotate(), set_dilate(), set_name()]
    balance(sets, R)
    unit = {
        "slug": "transformations",
        "title": "Transformations: Translations, Reflections, Rotations and Dilations",
        "seo_title": "Grade 8 Transformations Worksheets: Translate, Reflect, Rotate and Dilate on the Coordinate Plane",
        "short_title": "Transformations",
        "domain": "Geometry",
        "standard_code": "8.G.A.3",
        "standard_url": "https://www.thecorestandards.org/Math/Content/8/G/A/3/",
        "standard_text": "Describe the effect of dilations, translations, rotations, and reflections on two-dimensional figures using coordinates.",
        "meta_desc": "Free Grade 8 transformations worksheets: translate, reflect over the x- and y-axis, rotate 90° and 180° about the origin, and dilate from the origin using coordinate rules. 100 questions with an answer key.",
        "key_big": "Translate: add. Reflect over x: (x, −y). Reflect over y: (−x, y). Rotate 180°: (−x, −y). Dilate: (kx, ky).",
        "key_sub": "Translations, reflections and rotations keep size and shape. Dilations change the size.",
        "body_html": body(),
        "faq": [
            {"q": "What are the four transformations in Grade 8?", "a": "Translations (slides), reflections (flips), rotations (turns) and dilations (resizing)."},
            {"q": "What is the rule for a reflection over the x-axis?", "a": "(x, y) → (x, −y). The x-coordinate stays the same and the y-coordinate changes sign."},
            {"q": "What is the rule for a 90° rotation about the origin?", "a": "Counterclockwise: (x, y) → (−y, x). Clockwise: (x, y) → (y, −x)."},
            {"q": "Which transformations keep a figure the same size?", "a": "Translations, reflections and rotations. A dilation changes the size unless the scale factor is 1."}],
        "sets": sets, "pdf_url": "", "sort": 11, "updated": UPDATED,
    }
    write_unit("us", "math", "grade-8", unit)


if __name__ == "__main__":
    main()
