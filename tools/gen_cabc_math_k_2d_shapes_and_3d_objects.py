# -*- coding: utf-8 -*-
"""
BC Kindergarten Math: 2D Shapes and 3D Objects (BC Mathematics Curriculum, Kindergarten Content: Single attributes
of 2D shapes and 3D objects; using positional language)
  python3 tools/gen_cabc_math_k_2d_shapes_and_3d_objects.py
Naming circles, triangles, squares and rectangles, sides and corners, naming 3D objects (sphere, cube, cylinder,
cone) and how they move (roll, stack, slide), finding and sorting shapes by one attribute, and position words
(above, under, beside, in front of, behind). Sets 1, 2, 4 and 5 reuse the AU Foundation makers.
Wrong answers come from real mistakes: thinking a turned square is not a square, counting a curved edge as a
side, mixing up flat shapes and solid objects, and mixing up in front of and behind.
"""
import random
from k_pics import one_solid_svg, lettered_mix_svg
from bck_common import Kids, Cycle, mcq, letters, finish, make, fig, figure, lesson, collect, S
import gen_au_maths_f_shapes as au
import gen_au_maths_f_position as pos

R = random.Random(52901)
au.Kids = Kids
pos.Kids = Kids
POS = Cycle()
SOLIDS = {"sphere": ("Sphere", "rolls", "a ball"), "cube": ("Cube", "stacks", "a dice cube"), "cylinder": ("Cylinder", "rolls and stacks", "a can of soup"), "cone": ("Cone", "rolls in a circle and has a point", "a traffic cone")}
COLS = ["red", "blue", "yellow", "green"]


def take(fn, n, r):
    return fn(r)["items"][:n]


# ------------------------------------------------------------ set 3: 3D objects
def one_solid(r):
    kind = r.choice(["name", "name", "roll", "stack", "like", "which"])
    k = r.choice(list(SOLIDS))
    col = r.choice(COLS)
    if kind == "name":
        return mcq(fig(one_solid_svg(k, col)) + "What is the name of this 3D object?", SOLIDS[k][0], [SOLIDS[x][0] for x in SOLIDS if x != k],
                   "It is a <b>%s</b>, like %s." % (SOLIDS[k][0], SOLIDS[k][2]))
    if kind == "like":
        return mcq("Which 3D object is shaped like %s?" % SOLIDS[k][2], SOLIDS[k][0], [SOLIDS[x][0] for x in SOLIDS if x != k], "%s is shaped like a <b>%s</b>." % (SOLIDS[k][2].capitalize(), SOLIDS[k][0]))
    if kind == "roll":
        return mcq("Which object can <b>roll</b> but <b>cannot</b> stack?", "Sphere", ["Cube", "Cylinder", "Cone"], "A <b>Sphere</b> is curved all over, so it rolls in any direction but will not stay stacked.")
    if kind == "stack":
        return mcq("Which object stacks well but does <b>not</b> roll?", "Cube", ["Sphere", "Cylinder", "Cone"], "A <b>Cube</b> has only flat faces, so it stacks and slides but does not roll.")
    ks = r.sample(list(SOLIDS), 4)
    j = POS.next()
    target = ks[j]
    items = [("solid", x, r.choice(COLS), 0) for x in ks]
    it = mcq(fig(lettered_mix_svg(items)) + "Which one is a <b>%s</b>?" % SOLIDS[target][0].lower(), "ABCD"[j], [l for l in "ABCD" if l != "ABCD"[j]],
             "Object <b>%s</b> is a %s." % ("ABCD"[j], SOLIDS[target][0].lower()))
    return letters(it, "ABCD"[j])


def build():
    sets = [S("Name the shape", take(au.set_name, 20, R)),
            S("Sides and corners", take(au.set_sides, 20, R)),
            S("3D objects", collect(one_solid, 20, R)),
            S("Find and sort shapes", take(au.set_find, 20, R)),
            S("Where is it? Position words", take(pos.set_table, 10, R) + take(pos.set_box, 10, R))]
    finish(sets, R, max_num=10)
    body = lesson(
        "<ul><li><b>2D shapes</b> are flat: circle, triangle, square, rectangle. Count the straight <b>sides</b> and the <b>corners</b>.</li>"
        "<li>A shape keeps its name when it is turned or a different colour or size.</li>"
        "<li><b>3D objects</b> are solid: sphere, cube, cylinder, cone. Some <b>roll</b>, some <b>stack</b>, some <b>slide</b>.</li>"
        "<li>Position words tell where something is: above, under, beside, in front of, behind.</li></ul>",
        [figure(one_solid_svg("cylinder", "blue"), "A cylinder can roll and stack, like a can of soup."),
         figure(one_solid_svg("cube", "red"), "A cube has flat faces, so it stacks and slides.")],
        [["Thinking a turned square is not a square", "Count the sides and corners. It still has 4 equal sides."],
         ["Counting a curved edge as a side", "Sides are straight. A circle has no straight sides."],
         ["Mixing up in front of and behind", "In front of is closer to you. Behind is hidden by the other thing."]])
    faq = [("What shapes do Kindergarten children learn in BC?", "Flat 2D shapes such as circles, triangles, squares and rectangles, and solid 3D objects such as spheres, cubes, cylinders and cones."),
           ("What is a single attribute?", "One feature, such as the number of sides, the colour, or whether an object rolls. Children sort shapes using one attribute at a time."),
           ("What is the difference between 2D and 3D?", "2D shapes are flat, like a drawing. 3D objects are solid and can be picked up, like a ball or a box."),
           ("Why learn position words?", "Words like above, under, beside, in front of and behind help children describe where things are, which is the start of geometry and maps.")]
    make("2d-shapes-and-3d-objects", 9, "Geometry and measurement", "2D Shapes and 3D Objects: Names, Attributes and Position", "2D shapes and 3D objects",
         "Single attributes of 2D shapes and 3D objects: sorting 2D shapes and 3D objects using a single attribute, building and describing 3D objects, exploring, creating, and describing 2D shapes, using positional language, such as beside, on top of, under, and in front of",
         "Free Kindergarten math worksheets on 2D shapes and 3D objects for the BC curriculum: name shapes, sides and corners, spheres, cubes, cylinders and cones, sorting by one attribute, and position words. 100 picture questions with answers.",
         "2D shapes are flat; 3D objects are solid.", "Count straight sides and corners. Some 3D objects roll, some stack, some slide.",
         body, faq, sets)


if __name__ == "__main__":
    build()
