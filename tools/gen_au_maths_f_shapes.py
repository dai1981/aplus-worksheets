# -*- coding: utf-8 -*-
"""
AU Foundation Maths: Familiar Shapes (Australian Curriculum v9.0, AC9MFSP01)
  python3 tools/gen_au_maths_f_shapes.py
Name circles, triangles, squares and rectangles (any size, colour or turn), count sides and corners, find
and sort shapes, count shapes in a picture, and find shapes in everyday objects, giving reasons.
Wrong answers come from real mistakes: calling a turned square a diamond or a different shape, calling a
long rectangle a square, saying a circle has corners, and judging a shape by its colour or size.
"""
import random
from k_pics import one_shape_svg, lettered_shapes_svg, shapes_mix_svg
from f_common import Kids, mcq, finish, make, fig, figure, mistakes

R = random.Random(100001)
SHAPES = ["circle", "triangle", "square", "rectangle"]
COLS = ["red", "blue", "yellow", "green"]
SIDES = {"circle": 0, "triangle": 3, "square": 4, "rectangle": 4}
WHY = {"circle": "It is perfectly round, with no straight sides and no corners",
       "triangle": "It has 3 straight sides and 3 corners",
       "square": "It has 4 straight sides that are all the same length, and 4 square corners",
       "rectangle": "It has 4 straight sides and 4 square corners, with 2 long sides and 2 short sides"}


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ set 1: name the shape
def set_name(rnd):
    its = []
    plan = [("circle", "red", 0), ("triangle", "blue", 0), ("square", "yellow", 0), ("rectangle", "green", 0), ("triangle", "red", 180),
            ("square", "blue", 45), ("rectangle", "yellow", 90), ("circle", "green", 0), ("triangle", "green", 30), ("rectangle", "red", 20),
            ("square", "green", 15), ("circle", "blue", 0), ("triangle", "yellow", 90), ("rectangle", "blue", 0), ("square", "red", 0),
            ("triangle", "blue", 200), ("rectangle", "green", 135), ("square", "yellow", 30), ("circle", "yellow", 0), ("triangle", "red", 60)]
    for i, (k, c, rot) in enumerate(plan):
        r = [40, 28, 46, 34][i % 4]
        q = fig(one_shape_svg(k, c, r, rot)) + "What is the name of this shape?"
        wr = [s.capitalize() for s in SHAPES if s != k] + ["Diamond"]
        if k == "square":
            wr = ["Diamond", "Triangle", "Circle"]   # a square is also a rectangle, so never offer that as wrong
        e = "%s, so it is a <b>%s</b>.%s" % (WHY[k], k, " Turning a shape does not change its name." if rot else "")
        its.append(mcq(q, k.capitalize(), wr, e))
    return {"title": "Name the shape", "items": its}


# ------------------------------------------------------------ set 2: sides and corners
def set_sides(rnd):
    its = []
    plan = [("triangle", "sides"), ("square", "corners"), ("rectangle", "sides"), ("circle", "corners"), ("triangle", "corners"),
            ("rectangle", "corners"), ("square", "sides"), ("circle", "sides"), ("rectangle", "sides"), ("square", "corners")]
    for i, (k, what) in enumerate(plan):
        c = COLS[i % 4]
        q = fig(one_shape_svg(k, c, 36, [0, 30, 90, 0, 180][i % 5])) + "How many %s does this shape have?" % ("straight sides" if what == "sides" else what)
        n = SIDES[k]
        if k == "circle":
            e = "A circle is round. It has <b>0</b> %s." % ("straight sides" if what == "sides" else "corners")
            its.append(mcq(q, 0, [1, 2, 4], e, allow_zero=True))
        else:
            e = "Touch and count each %s: %s. A %s has <b>%d</b>." % (what[:-1], ", ".join(str(j) for j in range(1, n + 1)), k, n)
            its.append(mcq(q, n, [n - 1, n + 1, 2, 5], e))
    facts = [("Which shape has 3 sides?", "Triangle", ["Square", "Circle", "Rectangle"], "A <b>triangle</b> has 3 sides. Tri means three."),
             ("Which shape has no corners?", "Circle", ["Triangle", "Square", "Rectangle"], "A <b>circle</b> is round, so it has no corners."),
             ("Which shape has 4 sides that are all the same length?", "Square", ["Rectangle", "Triangle", "Circle"], "All 4 sides of a <b>square</b> are the same length."),
             ("Which shape has 2 long sides and 2 short sides?", "Rectangle", ["Square", "Triangle", "Circle"], "A <b>rectangle</b> has 2 long sides and 2 short sides."),
             ("Which shape is round?", "Circle", ["Square", "Triangle", "Rectangle"], "A <b>circle</b> is round all the way around."),
             ("How many corners does a triangle have?", "3", ["4", "2", "0"], "A triangle has 3 sides and <b>3</b> corners."),
             ("A shape has 4 corners. Which shape could it be?", "A square", ["A triangle", "A circle", "A heart"], "Squares and rectangles have 4 corners. <b>A square</b> is in the list."),
             ("How many sides do a square and a triangle have altogether?", "7", ["6", "8", "4"], "A square has 4 and a triangle has 3: 4 and 3 make <b>7</b>."),
             ("Which shape can roll?", "Circle", ["Square", "Triangle", "Rectangle"], "A <b>circle</b> has no corners to stop it rolling."),
             ("Which two shapes both have 4 square corners?", "Square and rectangle", ["Square and triangle", "Circle and rectangle", "Triangle and circle"], "Both a <b>square and a rectangle</b> have 4 square corners.")]
    for q, a, wr, e in facts:
        its.append(mcq(q, a, wr, e, allow_zero=True))
    o = its
    return {"title": "Sides and corners", "items": [x for pair in zip(o[:10], o[10:]) for x in pair]}


# ------------------------------------------------------------ set 3: find and sort
def set_find(rnd):
    its = []
    seen = set()
    while len(its) < 20:
        target = SHAPES[len(its) % 4]
        others = [s for s in SHAPES if s != target and not (target == "rectangle" and s == "square")] + (["circle"] if target == "rectangle" else [])
        rnd.shuffle(others)
        kinds = others[:3] + [target]
        rnd.shuffle(kinds)
        cols = [rnd.choice(COLS) for _ in range(4)]
        key = (tuple(kinds), tuple(cols))
        if key in seen:
            continue
        seen.add(key)
        letter = "ABCD"[kinds.index(target)]
        if len(its) < 12:
            q = fig(lettered_shapes_svg(list(zip(kinds, cols)))) + "Which one is a <b>%s</b>?" % target
            e = "%s. That is shape <b>%s</b>." % (WHY[target], letter)
            its.append(mcq(q, letter, [x for x in "ABCD" if x != letter], e))
        else:
            odd = target
            same = rnd.choice([s for s in SHAPES if s != odd and {s, odd} != {"square", "rectangle"}])
            kinds = [same] * 4
            pos = rnd.randrange(4)
            kinds[pos] = odd
            cols = [rnd.choice(COLS) for _ in range(4)]
            key = ("odd", tuple(kinds), tuple(cols))
            if key in seen:
                continue
            seen.add(key)
            letter = "ABCD"[pos]
            q = fig(lettered_shapes_svg(list(zip(kinds, cols)))) + "Which shape does <b>not</b> belong?"
            e = "Three are %ss. Shape <b>%s</b> is a %s. Colour does not matter, only the shape." % (same, letter, odd)
            its.append(mcq(q, letter, [x for x in "ABCD" if x != letter], e))
    return {"title": "Find and sort shapes", "items": its}


# ------------------------------------------------------------ set 4: count shapes in a picture
def set_count(rnd):
    its = []
    seen = set()
    while len(its) < 20:
        target = SHAPES[len(its) % 4]
        n = rnd.randint(2, 6)
        rest = [s for s in SHAPES if s != target and not (target == "rectangle" and s == "square")]
        items = [(target, rnd.choice(COLS)) for _ in range(n)] + [(rnd.choice(rest), rnd.choice(COLS)) for _ in range(rnd.randint(3, 6))]
        key = (target, n, len(items))
        if key in seen:
            continue
        seen.add(key)
        q = fig(shapes_mix_svg(items, 7000 + len(its))) + "How many <b>%ss</b> are in the picture?" % target
        its.append(mcq(q, n, [n + 1, n - 1, len(items), n + 2], "Find every %s, whatever its colour, and count each one once: <b>%d</b>." % (target, n)))
    return {"title": "Count the shapes", "items": its}


# ------------------------------------------------------------ set 5: shapes around us
ENV = [("a dinner plate", "circle"), ("a door", "rectangle"), ("a slice of sandwich cut corner to corner", "triangle"), ("a window with 4 equal sides", "square"),
       ("a coin", "circle"), ("a book cover", "rectangle"), ("a road sign that says GIVE WAY", "triangle"), ("a cracker with 4 equal sides", "square"),
       ("the face of a clock", "circle"), ("a phone screen", "rectangle"), ("the sail on a small boat", "triangle"), ("a square sticky note", "square"),
       ("a car wheel", "circle"), ("a whiteboard", "rectangle"), ("a slice of watermelon cut into a wedge with 3 straight sides", "triangle"), ("a chess board", "square"),
       ("the top of a cup", "circle"), ("a school lunchbox lid", "rectangle"), ("a party flag on bunting", "triangle"), ("a tile on the bathroom wall with 4 equal sides", "square")]


def set_env(rnd):
    its = []
    for i, (thing, sh) in enumerate(ENV):
        if i % 2 == 0:
            q = "Which shape is %s?" % thing
            its.append(mcq(q, sh.capitalize(), [s.capitalize() for s in SHAPES if s != sh and not (sh == "square" and s == "rectangle")] + ["Oval"], "%s. So %s is a <b>%s</b>." % (WHY[sh], thing, sh)))
        else:
            q = "Why is %s a %s?" % (thing, sh)
            right = WHY[sh]
            wr = [WHY[s] for s in SHAPES if s != sh]
            its.append(mcq(q, right, wr, "<b>%s</b>." % right))
    return {"title": "Shapes around us", "items": its}


def body():
    return (
        "<h2>Four shapes</h2>"
        "<p>A <b>circle</b> is round. A <b>triangle</b> has 3 sides and 3 corners. A <b>square</b> has 4 sides that are all the same. "
        "A <b>rectangle</b> has 4 sides: 2 long and 2 short.</p>"
        + figure(lettered_shapes_svg([("circle", "red"), ("triangle", "blue"), ("square", "yellow"), ("rectangle", "green")]),
                 "A circle, B triangle, C square, D rectangle.")
        + "<h2>Turning, colour and size</h2><p>A shape keeps its name when it is turned, coloured or made bigger. A square on its corner is still a square.</p>"
        + figure(one_shape_svg("square", "blue", 34, 45), "Still a square.")
        + "<h2>Shapes around us</h2><p>Look for shapes in everyday things: a plate is a circle, a door is a rectangle. Say why: count the sides and corners.</p>"
        + mistakes([["Calling a turned square a diamond", "Count the sides: 4 equal sides is a square"],
                    ["Calling a long rectangle a square", "A square has all 4 sides the same"],
                    ["Saying a circle has corners", "A circle is round: no corners"]]))


FAQ = [("What shapes do Foundation students learn?",
        "Familiar shapes like circles, triangles, squares and rectangles. They sort, name and make them, and find them in everyday objects, giving reasons (AC9MFSP01)."),
       ("Is a square on its corner a diamond?",
        "It is still a square. Turning a shape does not change its name. Count the sides: 4 equal sides and 4 square corners."),
       ("Is a square a rectangle?",
        "Yes, a square is a special rectangle with all four sides the same length. At Foundation we mostly call it a square."),
       ("How can I help my child learn shapes?",
        "Go on a shape hunt at home or in the park: a clock is a circle, a door is a rectangle. Ask: How do you know? How many sides?")]


def build():
    sets = [set_name(R), set_sides(R), set_find(R), set_count(R), set_env(R)]
    finish(sets, R, max_num=12)
    make("shapes", 10, "AC9MFSP01", "Space",
         "Familiar Shapes: Circles, Triangles, Squares and Rectangles",
         "Foundation Shapes Worksheets: Circle, Triangle, Square, Rectangle (Free, with Answers)",
         "Shapes",
         "Sort, name and create familiar shapes; recognise and describe familiar shapes within objects in the environment, giving reasons.",
         "Free Foundation (Prep, Kindergarten) maths worksheets on familiar shapes, matched to the Australian Curriculum (AC9MFSP01): name circles, triangles, squares and rectangles, count sides and corners, sort and find shapes around us. 100 picture questions with answers.",
         "Count the sides and corners to name a shape.",
         "Turning, colour and size never change a shape's name.",
         body(), FAQ, sets)


if __name__ == "__main__":
    build()
