# -*- coding: utf-8 -*-
"""
Texas Grade 2 Math: 2D Shapes and Polygons (TEKS 2.8A, 2.8C, 2.8E)
  python3 tools/gen_ustx_math_g2_shapes_2d.py
Counting sides and vertices, naming shapes, which shape has more, shapes in the world (the US Grade 2 makers with
Texas names), polygons with up to 12 sides, and cutting shapes into parts (own makers).
Wrong answers come from real mistakes: counting a side twice, naming a shape by how it is turned, and thinking a
shape with a curve is a polygon.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g2_shapes as sh
adopt(sh)
tx_common.GRADE = "grade-2"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


POLY = [(3, "triangle"), (4, "quadrilateral"), (5, "pentagon"), (6, "hexagon"), (7, "heptagon"), (8, "octagon"), (9, "nonagon"), (10, "decagon"), (12, "dodecagon")]


def one_poly(r):
    n, name = r.choice(POLY)
    if r.random() < 0.5:
        others = [nm for k, nm in POLY if k != n]
        return mcq("A polygon has %d sides and %d vertices. What is it called?" % (n, n), "A %s" % name, ["A %s" % x for x in r.sample(others, 3)],
                   "A polygon with %d sides is a <b>%s</b>." % (n, name))
    w = [str(x) for x in dict.fromkeys([n + 1, n - 1, n + 2, 2 * n]) if x != n][:3]
    return mcq("How many vertices does %s %s have?" % ("an" if name[0] in "aeiou" else "a", name), str(n), w, "A %s has %d sides and <b>%d vertices</b>." % (name, n, n))


CUT = [("A square is cut on one diagonal. What two shapes do you get?", "2 triangles", ["2 squares", "2 rectangles", "1 triangle and 1 square"], "A line from corner to corner makes <b>2 triangles</b>."),
       ("A rectangle is cut down the middle from top to bottom. What do you get?", "2 smaller rectangles", ["2 triangles", "2 circles", "1 square and 1 triangle"], "A straight cut across a rectangle makes <b>2 rectangles</b>."),
       ("A square is cut from the end of a long rectangle. What shape is left?", "A rectangle", ["A triangle", "A circle", "A hexagon"], "Cutting a square off a rectangle leaves <b>a rectangle</b>."),
       ("A hexagon is cut into 6 equal parts from the center. What shape is each part?", "A triangle", ["A square", "A circle", "A pentagon"], "Each part has 3 sides: <b>a triangle</b>."),
       ("A circle is cut in half. What is each part called?", "A half circle", ["A triangle", "A square", "A quarter"], "Two equal parts of a circle are <b>half circles</b>."),
       ("A rectangle is cut into 2 identical triangles. How many sides does each triangle have?", "3", ["4", "2", "6"], "Every triangle has <b>3 sides</b>."),
       ("Two identical triangles are put together along their long sides. What shape can they make?", "A rectangle", ["A circle", "A pentagon", "An octagon"], "Two right triangles can make <b>a rectangle</b>."),
       ("A square is cut into 4 equal smaller squares. How many small squares are there?", "4", ["2", "8", "3"], "<b>4</b> small squares."),
       ("A trapezoid and a triangle are put together to make one shape with 5 sides. What is it?", "A pentagon", ["A hexagon", "A square", "A triangle"], "5 sides make <b>a pentagon</b>.")]


def one_cut(r):
    q, a, w, e = r.choice(CUT)
    return mcq(q, a, w, e)


def one_make(r):
    n = r.choice([3, 4, 5, 6, 8, 10])
    name = dict(POLY)[n]
    k = Kid(r).next()
    v = r.choice(["draws", "builds", "makes"])
    return mcq("%s %s a closed shape with %d straight sides. What could %s have made?" % (k["n"], v, n, k["he"]), "A %s" % name, ["A circle", "A %s" % dict(POLY)[n + 1 if n + 1 in dict(POLY) else n - 1], "An oval"],
               "A closed shape with %d straight sides is <b>a %s</b>." % (n, name))


def build():
    sets, R = build_sets([
        ("Count sides and vertices", [("run", sh.set_count, ("rnd", sh.People), 20)]),
        ("Name the shape", [("run", sh.set_name, ("rnd", sh.People), 20)]),
        ("Polygons with up to 12 sides", [("collect", uniq(one_poly), 14), ("collect", uniq(one_make), 6)]),
        ("Which shape has more?", [("run", sh.set_which, ("rnd", sh.People), 20)]),
        ("Cut and put shapes together", [("collect", uniq(one_cut), 9), ("run", sh.set_world, ("rnd", sh.People), 11)]),
    ], 69213)
    finish(sets, R)
    body = lesson('<ul><li>A <b>polygon</b> is a closed shape with straight sides. Circles are not polygons.</li><li>A <b>vertex</b> is a corner where two sides meet. A polygon has as many vertices as sides.</li><li>Names: triangle 3, quadrilateral 4, pentagon 5, hexagon 6, octagon 8, decagon 10.</li><li>Shapes can be cut into smaller shapes: a square cut corner to corner makes 2 triangles.</li></ul>',
        [example("A shape has 6 sides.", ["6 sides and 6 vertices"], "hexagon")],
        [['Counting a side twice', 'Put a finger on one side and go around once.'], ['Naming a shape by how it is turned', 'A turned square is still a square.'], ['Calling a circle a polygon', 'Polygons have only straight sides.']])
    faq = [('What does TEKS 2.8C ask?', 'Classify and sort polygons with 12 or fewer sides according to attributes, including identifying the number of sides and number of vertices.'), ('What does TEKS 2.8A ask?', 'Create two-dimensional shapes based on given attributes, including number of sides and vertices.'), ('What does TEKS 2.8E ask?', 'Decompose two-dimensional shapes such as cutting out a square from a rectangle, dividing a shape in half or partitioning a rectangle into identical triangles and identify the resulting geometric parts.'), ('Is a square a quadrilateral?', 'Yes. It has 4 sides.')]
    make('2d-shapes-and-polygons', 13, 'Geometry and Measurement', '2.8A, 2.8C, 2.8E',
         '2.8A create two-dimensional shapes based on given attributes, including number of sides and vertices; 2.8C classify and sort polygons with 12 or fewer sides according to attributes, including identifying the number of sides and number of vertices; 2.8E decompose two-dimensional shapes such as cutting out a square from a rectangle, dividing a shape in half, or partitioning a rectangle into identical triangles and identify the resulting geometric parts',
         '2D Shapes and Polygons', '2D Shapes and Polygons',
         'Free Grade 2 shape worksheets for Texas TEKS 2.8A, 2.8C and 2.8E: sides and vertices, naming polygons up to 12 sides, comparing shapes and cutting shapes into parts. 100 questions with answers.',
         'Polygons have straight sides; count sides and vertices.', 'Pentagon 5, hexagon 6, octagon 8, decagon 10.',
         body, faq, sets, seo_title='Grade 2 2D Shapes and Polygons Worksheets (TEKS 2.8C)')


if __name__ == "__main__":
    build()
