# -*- coding: utf-8 -*-
"""
US Kindergarten Math: 2D and 3D Shapes (K.G.A.2, K.G.A.3, K.G.B.4)
  python3 tools/gen_us_math_gk_2d_and_3d_shapes.py
Name flat shapes (circle, square, triangle, rectangle, hexagon) in any size or turn, name solid shapes
(cube, sphere, cone, cylinder), tell flat from solid, count sides and corners, and find shapes around us.
"""
import random
from ws_common import table, write_unit, fig
from k_pics import one_shape_svg, one_solid_svg, lettered_mix_svg
from k_common import Kids, mcq, finish

UPDATED = "2026-11-16"
FLAT = ["circle", "square", "triangle", "rectangle", "hexagon"]
SOLID = ["cube", "sphere", "cone", "cylinder"]
COLORS = ["red", "blue", "yellow", "green"]
SIDES = {"triangle": 3, "square": 4, "rectangle": 4, "hexagon": 6, "circle": 0}
NEAR = {"square": ["rectangle", "cube", "triangle"], "rectangle": ["square", "triangle", "cylinder"],
        "triangle": ["cone", "square", "hexagon"], "circle": ["sphere", "hexagon", "square"],
        "hexagon": ["circle", "triangle", "square"],
        "cube": ["square", "cylinder", "sphere"], "sphere": ["circle", "cone", "cube"],
        "cone": ["triangle", "cylinder", "sphere"], "cylinder": ["rectangle", "cone", "cube"]}
WHY = {"circle": "A circle is round. It has no sides and no corners.",
       "square": "A square has 4 sides that are all the same length and 4 corners.",
       "rectangle": "A rectangle has 4 sides and 4 corners. Two sides are long and two are short.",
       "triangle": "A triangle has 3 sides and 3 corners.",
       "hexagon": "A hexagon has 6 sides and 6 corners.",
       "cube": "A cube is solid. All of its faces are squares, like a number cube.",
       "sphere": "A sphere is solid and round all over, like a ball.",
       "cone": "A cone is solid. It has a round flat bottom and a point on top.",
       "cylinder": "A cylinder is solid. It has two round flat ends, like a can."}


def cap(s):
    return s[0].upper() + s[1:]


# ============================================================ set 1: flat shapes
def set_flat(rnd, K):
    plan = [("circle", 0, 40), ("square", 0, 40), ("triangle", 0, 40), ("rectangle", 0, 36), ("hexagon", 0, 40),
            ("square", 45, 34), ("triangle", 180, 38), ("rectangle", 90, 32), ("circle", 0, 22), ("hexagon", 30, 30),
            ("triangle", 35, 44), ("square", 20, 26), ("rectangle", 30, 38), ("triangle", 90, 30), ("hexagon", 15, 44),
            ("circle", 0, 46), ("square", 70, 42), ("rectangle", 135, 28), ("triangle", 250, 36), ("hexagon", 0, 24)]
    its = []
    for i, (k, rot, r) in enumerate(plan):
        col = COLORS[i % 4]
        q = fig(one_shape_svg(k, col, r=r, rot=rot)) + "What is the name of this flat shape?"
        e = WHY[k] + " This is a <b>%s</b>." % k
        if rot:
            e += " Turning a shape does not change its name."
        its.append(mcq(q, cap(k), [cap(x) for x in NEAR[k]], e))
    return {"title": "Name the flat shape", "items": its}


# ============================================================ set 2: solid shapes
def set_solid(rnd, K):
    its = []
    for i, k in enumerate(SOLID * 3):
        col = COLORS[(i + 1) % 4]
        r = [40, 30, 46][i // 4]
        q = fig(one_solid_svg(k, col, r=r)) + "What is the name of this solid shape?"
        its.append(mcq(q, cap(k), [cap(x) for x in NEAR[k]], WHY[k] + " This is a <b>%s</b>." % k))
    r2 = random.Random(77)
    for k in ["sphere", "cylinder", "cone", "cube", "cylinder", "sphere", "cube", "cone"]:
        order = SOLID[:]
        r2.shuffle(order)
        items = [("solid", x, COLORS[j], 0) for j, x in enumerate(order)]
        ans = "ABCD"[order.index(k)]
        q = fig(lettered_mix_svg(items)) + "Which one is a <b>%s</b>?" % k
        e = WHY[k] + " The answer is <b>%s</b>." % ans
        its.append(mcq(q, ans, [x for x in "ABCD" if x != ans], e))
    o = its
    order = [o[0], o[1], o[2], o[3], o[12], o[4], o[13], o[5], o[14], o[6],
             o[15], o[7], o[16], o[8], o[17], o[9], o[18], o[10], o[19], o[11]]
    return {"title": "Name the solid shape", "items": order}


# ============================================================ set 3: find the shape, flat or solid
def set_find(rnd, K):
    its = []
    for target, items in [
        ("triangle", [("flat", "square", "red", 0), ("flat", "triangle", "blue", 200), ("flat", "circle", "yellow", 0), ("flat", "hexagon", "green", 0)]),
        ("square", [("flat", "rectangle", "green", 0), ("flat", "triangle", "red", 0), ("flat", "square", "yellow", 45), ("flat", "circle", "blue", 0)]),
        ("hexagon", [("flat", "hexagon", "red", 0), ("flat", "circle", "blue", 0), ("flat", "square", "green", 0), ("flat", "triangle", "yellow", 0)]),
        ("rectangle", [("flat", "square", "blue", 0), ("flat", "hexagon", "yellow", 0), ("flat", "triangle", "green", 0), ("flat", "rectangle", "red", 90)]),
        ("circle", [("flat", "hexagon", "green", 0), ("flat", "circle", "red", 0), ("flat", "square", "yellow", 0), ("solid", "sphere", "blue", 0)]),
        ("cube", [("flat", "square", "red", 0), ("solid", "cylinder", "blue", 0), ("solid", "cube", "yellow", 0), ("solid", "cone", "green", 0)]),
        ("sphere", [("flat", "circle", "blue", 0), ("solid", "cone", "red", 0), ("solid", "cube", "green", 0), ("solid", "sphere", "yellow", 0)]),
        ("cone", [("solid", "cone", "blue", 0), ("flat", "triangle", "yellow", 0), ("solid", "cylinder", "red", 0), ("solid", "sphere", "green", 0)]),
        ("cylinder", [("solid", "cube", "green", 0), ("solid", "cylinder", "yellow", 0), ("flat", "rectangle", "blue", 0), ("solid", "cone", "red", 0)]),
        ("triangle", [("solid", "cone", "red", 0), ("flat", "square", "green", 30), ("flat", "hexagon", "blue", 0), ("flat", "triangle", "yellow", 90)]),
    ]:
        idx = [i for i, it in enumerate(items) if it[1] == target][0]
        ans = "ABCD"[idx]
        q = fig(lettered_mix_svg(items)) + "Which one is a <b>%s</b>?" % target
        e = WHY[target] + " The answer is <b>%s</b>." % ans
        its.append(mcq(q, ans, [x for x in "ABCD" if x != ans], e))
    for want, items in [
        ("solid", [("flat", "circle", "red", 0), ("flat", "square", "blue", 0), ("solid", "cube", "green", 0), ("flat", "triangle", "yellow", 0)]),
        ("flat", [("solid", "sphere", "red", 0), ("flat", "hexagon", "blue", 0), ("solid", "cone", "yellow", 0), ("solid", "cylinder", "green", 0)]),
        ("solid", [("solid", "sphere", "blue", 0), ("flat", "rectangle", "green", 0), ("flat", "circle", "yellow", 0), ("flat", "hexagon", "red", 0)]),
        ("flat", [("solid", "cube", "yellow", 0), ("solid", "cone", "blue", 0), ("solid", "sphere", "green", 0), ("flat", "triangle", "red", 0)]),
        ("solid", [("flat", "square", "yellow", 0), ("flat", "triangle", "green", 0), ("solid", "cylinder", "red", 0), ("flat", "circle", "blue", 0)]),
        ("flat", [("flat", "circle", "green", 0), ("solid", "cylinder", "yellow", 0), ("solid", "cube", "blue", 0), ("solid", "cone", "red", 0)]),
        ("solid", [("flat", "hexagon", "green", 0), ("solid", "cone", "red", 0), ("flat", "rectangle", "blue", 0), ("flat", "square", "yellow", 0)]),
        ("flat", [("solid", "sphere", "yellow", 0), ("solid", "cylinder", "green", 0), ("flat", "rectangle", "red", 0), ("solid", "cube", "blue", 0)]),
        ("solid", [("flat", "triangle", "blue", 0), ("flat", "circle", "red", 0), ("flat", "hexagon", "yellow", 0), ("solid", "sphere", "green", 0)]),
        ("flat", [("solid", "cone", "green", 0), ("flat", "square", "red", 0), ("solid", "sphere", "blue", 0), ("solid", "cylinder", "yellow", 0)]),
    ]:
        idx = [i for i, it in enumerate(items) if it[0] == want]
        assert len(idx) == 1
        ans = "ABCD"[idx[0]]
        k = items[idx[0]][1]
        q = fig(lettered_mix_svg(items)) + "Which shape is <b>%s</b>?" % want
        e = ("Flat shapes lie flat on paper. Solid shapes you can hold and they take up space. "
             "The %s is %s, so the answer is <b>%s</b>." % (k, want, ans))
        its.append(mcq(q, ans, [x for x in "ABCD" if x != ans], e))
    o = its
    order = [o[0], o[10], o[1], o[11], o[2], o[12], o[3], o[13], o[4], o[14],
             o[5], o[15], o[6], o[16], o[7], o[17], o[8], o[18], o[9], o[19]]
    return {"title": "Find the shape: flat or solid", "items": order}


# ============================================================ set 4: sides and corners
def set_sides(rnd, K):
    its = []
    plan = [("triangle", "sides", 0), ("square", "sides", 0), ("rectangle", "corners", 0), ("hexagon", "sides", 0),
            ("triangle", "corners", 60), ("circle", "corners", 0), ("square", "corners", 30), ("hexagon", "corners", 20),
            ("rectangle", "sides", 90), ("circle", "sides", 0), ("triangle", "sides", 150), ("hexagon", "sides", 45)]
    for i, (k, what, rot) in enumerate(plan):
        n = SIDES[k]
        q = fig(one_shape_svg(k, COLORS[i % 4], r=40, rot=rot)) + "How many <b>%s</b> does this %s have?" % (what, k)
        if k == "circle":
            e = "A circle is round. It has no straight sides and no corners. The answer is <b>0</b>."
            wr = [1, 2, 4]
        else:
            e = "Touch each %s and count: %s. A %s has <b>%d</b> %s." % (
                what[:-1], ", ".join(str(x) for x in range(1, n + 1)), k, n, what)
            wr = [n + 1, n - 1, n + 2, 2 * n]
        its.append(mcq(q, n, wr, e, allow_zero=True))
    for want, ans, wr in [("3 sides", "Triangle", ["Square", "Circle", "Hexagon"]),
                          ("6 sides", "Hexagon", ["Triangle", "Square", "Rectangle"]),
                          ("no corners", "Circle", ["Square", "Triangle", "Hexagon"]),
                          ("4 sides that are all the same length", "Square", ["Rectangle", "Triangle", "Hexagon"])]:
        q = fig(lettered_mix_svg([("flat", "triangle", "red", 0), ("flat", "square", "blue", 0),
                                  ("flat", "circle", "yellow", 0), ("flat", "hexagon", "green", 0)])) + \
            "Which shape has <b>%s</b>?" % want
        e = WHY[ans.lower()] + " The answer is <b>%s</b>." % ans.lower()
        its.append(mcq(q, ans, wr, e))
    for q, ans, wr, e in [
        ("A square and a rectangle both have 4 sides. How are they different?",
         "All sides of a square are the same length", ["A square has 3 corners", "A rectangle is round", "A square is solid"],
         "Both have 4 sides and 4 corners. <b>All sides of a square are the same length</b>. A rectangle has 2 long and 2 short sides."),
        ("How are a circle and a sphere different?", "A sphere is solid", ["A circle has corners", "A sphere has 4 sides", "They are the same"],
         "A circle is flat. <b>A sphere is solid</b>, like a ball."),
        ("Which solid shape can roll?", "Sphere", ["Cube", "Square", "Triangle"],
         "A <b>sphere</b> is round all over, so it can roll. A cube has flat faces, so it slides."),
        ("Which solid shape can stack well?", "Cube", ["Sphere", "Cone", "Circle"],
         "A <b>cube</b> has flat faces on every side, so cubes stack well."),
    ]:
        pic = lettered_mix_svg([("solid", "cube", "red", 0), ("solid", "sphere", "blue", 0),
                                ("solid", "cone", "yellow", 0), ("solid", "cylinder", "green", 0)]) if "solid" in q else \
            lettered_mix_svg([("flat", "square", "blue", 0), ("flat", "rectangle", "red", 0)]) if "square" in q else \
            lettered_mix_svg([("flat", "circle", "yellow", 0), ("solid", "sphere", "yellow", 0)])
        its.append(mcq(fig(pic) + q, ans, wr, e))
    o = its
    order = [o[0], o[1], o[12], o[2], o[3], o[13], o[4], o[5], o[14], o[6],
             o[16], o[7], o[15], o[8], o[17], o[9], o[18], o[10], o[19], o[11]]
    assert len({id(x) for x in order}) == 20
    return {"title": "Sides and corners", "items": order}


# ============================================================ set 5: shapes around us
def set_around(rnd, K):
    its = []
    flat = [("a door", "rectangle"), ("a slice of pizza", "triangle"), ("a clock face", "circle"),
            ("a window pane", "square"), ("a honeycomb cell", "hexagon"), ("a dollar bill", "rectangle"),
            ("a cookie", "circle"), ("a sandwich cut corner to corner", "triangle"), ("a sticky note", "square"),
            ("a coin", "circle")]
    for thing, k in flat:
        q = "What flat shape is <b>%s</b> like?" % thing
        e = "%s is like a <b>%s</b>. %s" % (cap(thing), k, WHY[k])
        its.append(mcq(fig(one_shape_svg(k, "green", r=34)) + q, cap(k), [cap(x) for x in NEAR[k]], e))
    solid = [("a basketball", "sphere"), ("a soup can", "cylinder"), ("a traffic cone", "cone"),
             ("a toy block", "cube"), ("a globe", "sphere"), ("a paper towel roll", "cylinder"),
             ("a party hat", "cone"), ("an ice cube", "cube"), ("a marble", "sphere"), ("a candle", "cylinder")]
    for thing, k in solid:
        q = "What solid shape is <b>%s</b> like?" % thing
        e = "%s is like a <b>%s</b>. %s" % (cap(thing), k, WHY[k])
        its.append(mcq(fig(one_solid_svg(k, "red", r=32)) + q, cap(k), [cap(x) for x in NEAR[k]], e))
    # the picture shows the answer: make it a hint, not the question, by showing all four solids instead
    for it, (thing, k) in zip(its[10:], solid):
        it["q"] = fig(lettered_mix_svg([("solid", "cube", "red", 0), ("solid", "sphere", "blue", 0),
                                         ("solid", "cone", "yellow", 0), ("solid", "cylinder", "green", 0)])) + \
            "What solid shape is <b>%s</b> like?" % thing
    for it, (thing, k) in zip(its[:10], flat):
        it["q"] = fig(lettered_mix_svg([("flat", "circle", "red", 0), ("flat", "square", "blue", 0),
                                         ("flat", "triangle", "yellow", 0), ("flat", "rectangle", "green", 0)]
                                        if k != "hexagon" else
                                        [("flat", "circle", "red", 0), ("flat", "hexagon", "blue", 0),
                                         ("flat", "triangle", "yellow", 0), ("flat", "square", "green", 0)])) + \
            "What flat shape is <b>%s</b> like?" % thing
    o = its
    order = [o[0], o[10], o[1], o[11], o[2], o[12], o[3], o[13], o[4], o[14],
             o[5], o[15], o[6], o[16], o[7], o[17], o[8], o[18], o[9], o[19]]
    return {"title": "Shapes around us", "items": order}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Flat shapes</h2>"
        "<p>Flat shapes lie flat on paper. Count the <b>sides</b> and <b>corners</b> to name them.</p>"
        + lettered_mix_svg([("flat", "triangle", "red", 0), ("flat", "square", "blue", 0),
                            ("flat", "rectangle", "yellow", 0), ("flat", "hexagon", "green", 0)]) +
        table(["Shape", "Sides", "Corners"], [
            ["Circle", "0", "0"], ["Triangle", "3", "3"], ["Square", "4 (all the same)", "4"],
            ["Rectangle", "4", "4"], ["Hexagon", "6", "6"],
        ]) +
        "<h2>Solid shapes</h2>"
        "<p>Solid shapes take up space. You can hold them.</p>"
        + lettered_mix_svg([("solid", "cube", "red", 0), ("solid", "sphere", "blue", 0),
                            ("solid", "cone", "yellow", 0), ("solid", "cylinder", "green", 0)]) +
        table(["Shape", "Like a…"], [["Cube", "number cube"], ["Sphere", "ball"], ["Cone", "party hat"], ["Cylinder", "can"]]) +
        "<h2>Size and turn do not matter</h2>"
        "<p>A big triangle and a small triangle are both triangles. A turned square is still a square.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do"], [
            ["Calling a turned square a diamond", "Count the sides: 4 equal sides is a square"],
            ["Mixing up circle and sphere", "A circle is flat. A sphere is solid"],
            ["Mixing up square and rectangle", "A square has 4 sides of the same length"],
        ])
    )


FAQ = [
    {"q": "What shapes should a kindergartner know?",
     "a": "Flat shapes: circle, square, triangle, rectangle and hexagon. Solid shapes: cube, sphere, cone and cylinder."},
    {"q": "What is the difference between 2D and 3D shapes?",
     "a": "2D shapes are flat, like a drawing on paper. 3D shapes are solid and take up space, like a ball or a box."},
    {"q": "Is a turned square called a diamond?",
     "a": "It is still a square. Turning a shape does not change its name. Count the sides and check that they are the same length."},
    {"q": "How can I practice shapes at home?",
     "a": "Go on a shape hunt: find circles (plates), rectangles (doors), cylinders (cans) and spheres (balls). Ask how many sides and corners each flat shape has."},
]


def gen():
    rnd = random.Random(2013)
    K = Kids(rnd)
    sets = [set_flat(rnd, K), set_solid(rnd, K), set_find(rnd, K), set_sides(rnd, K), set_around(rnd, K)]
    finish(sets, rnd, max_num=12)
    return {
        "slug": "2d-and-3d-shapes", "sort": 13, "updated": UPDATED, "pdf_url": "",
        "title": "2D and 3D Shapes: Flat and Solid Shapes",
        "seo_title": "Kindergarten Shapes Worksheets: 2D and 3D Shapes, Sides and Corners",
        "short_title": "2D and 3D Shapes",
        "domain": "Geometry",
        "standard_code": "K.G.A.2",
        "standard_url": "https://www.thecorestandards.org/Math/Content/K/G/A/2/",
        "standard_text": "Correctly name shapes regardless of their orientations or overall size.",
        "meta_desc": "Free kindergarten shapes worksheets: name circles, squares, triangles, rectangles and hexagons, "
                     "name cubes, spheres, cones and cylinders, tell flat from solid, count sides and corners, and "
                     "find shapes around us. 100 picture questions with an answer key.",
        "key_big": "Count sides and corners to name a flat shape. Solid shapes take up space.",
        "key_sub": "Size and turn do not change a shape’s name. A ball is a sphere, a can is a cylinder.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    write_unit("us", "math", "kindergarten", gen())
