# -*- coding: utf-8 -*-
"""
Texas Grade 1 Math: 2D Shapes: Sides, Vertices and Attributes (TEKS 1.6A, 1.6C, 1.6D, 1.6F)
  python3 tools/gen_ustx_math_g1_shapes_2d.py
Naming shapes, counting sides and vertices, what matters and what does not, and putting shapes together (the US
Grade 1 makers with Texas names), plus describing circles, triangles, rectangles, squares, rhombuses and hexagons
(own maker).
Wrong answers come from real mistakes: naming a shape by its color or size, counting a side twice, and thinking a
square is not a rectangle.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g1_shapes as sh
adopt(sh)
tx_common.GRADE = "grade-1"

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


ATTR = [("circle", "It is round. It has no sides and no vertices."), ("triangle", "It has 3 straight sides and 3 vertices."),
        ("rectangle", "It has 4 straight sides and 4 square corners."), ("square", "It has 4 sides that are all the same length and 4 square corners."),
        ("rhombus", "It has 4 sides that are all the same length, but its corners are not square."), ("hexagon", "It has 6 straight sides and 6 vertices.")]
FACT = [("Is a square a special rectangle?", "Yes, it has 4 square corners", ["No, it is too small", "No, it has 3 sides", "Yes, it is round"], "A square has 4 square corners, so it is a special <b>rectangle</b> with all sides the same."),
        ("How many vertices does a circle have?", "0", ["1", "4", "2"], "A circle is round. It has <b>0</b> vertices."),
        ("Which shape has 6 sides?", "Hexagon", ["Rhombus", "Triangle", "Rectangle"], "A <b>hexagon</b> has 6 sides."),
        ("Which shape has all sides the same length but no square corners?", "Rhombus", ["Rectangle", "Circle", "Triangle"], "A <b>rhombus</b> has 4 equal sides; its corners are not square."),
        ("What is a vertex?", "A corner where two sides meet", ["A curved line", "The inside of a shape", "A long side"], "A <b>vertex</b> is where two sides meet."),
        ("Two triangles are put together to make a square. How many sides does the square have?", "4", ["3", "6", "2"], "A square has <b>4</b> sides."),
        ("How many triangles of the same size can make a hexagon?", "6", ["2", "3", "4"], "<b>6</b> triangles fit together to make a hexagon.")]


def one_attr(r):
    name, clue = r.choice(ATTR)
    others = [n for n, c in ATTR if n != name]
    return mcq("%s Which shape is it?" % clue, name[0].upper() + name[1:], [x[0].upper() + x[1:] for x in r.sample(others, 3)], "%s That is a <b>%s</b>." % (clue, name))


def one_fact(r):
    q, a, w, e = r.choice(FACT)
    return mcq(q, a, w, e)


def build():
    sets, R = build_sets([
        ("Name the shape", [("run", sh.set_name, ("rnd", sh.People), 20)]),
        ("Count sides and vertices", [("run", sh.set_count, ("rnd", sh.People), 20)]),
        ("Describe the shape", [("collect", uniq(one_attr), 6), ("collect", uniq(one_fact), 7), ("run", sh.set_name, ("rnd", sh.People), 7)]),
        ("What makes a shape that shape?", [("run", sh.set_matters, ("rnd", sh.People), 20)]),
        ("Put shapes together", [("run", sh.set_compose, ("rnd", sh.People), 20)]),
    ], 69114)
    finish(sets, R)
    body = lesson('<ul><li>Count the <b>sides</b> (straight lines) and the <b>vertices</b> (corners).</li><li>Triangle 3, rectangle 4, square 4, rhombus 4, hexagon 6. A circle has none.</li><li>A <b>square</b> is a special rectangle with all sides the same.</li><li>Color, size and how a shape is turned do <b>not</b> change its name.</li></ul>',
        [example("4 equal sides, square corners", ["4 sides, 4 vertices"], "square")],
        [['Naming a shape by its color or size', 'A big blue triangle is still a triangle.'], ['Counting a side twice', 'Start at one side and go around once.'], ['Thinking a square is not a rectangle', 'A square has 4 square corners.']])
    faq = [('What does TEKS 1.6D ask?', 'Identify two-dimensional shapes, including circles, triangles, rectangles, and squares as special rectangles, rhombuses, and hexagons and describe their attributes using formal geometric language.'), ('What does TEKS 1.6A ask?', 'Classify and sort regular and irregular two-dimensional shapes based on attributes using informal geometric language.'), ('What does TEKS 1.6F ask?', 'Compose two-dimensional shapes by joining two, three, or four figures to produce a target figure in more than one way if possible.'), ('Does turning a shape change its name?', 'No.')]
    make('2d-shapes', 14, 'Geometry and Measurement', '1.6A, 1.6C, 1.6D, 1.6F',
         '1.6A classify and sort regular and irregular two-dimensional shapes based on attributes using informal geometric language; 1.6C create two-dimensional figures, including circles, triangles, rectangles, and squares, as special rectangles, rhombuses, and hexagons; 1.6D identify two-dimensional shapes, including circles, triangles, rectangles, and squares as special rectangles, rhombuses, and hexagons and describe their attributes using formal geometric language; 1.6F compose two-dimensional shapes by joining two, three, or four figures to produce a target figure in more than one way if possible',
         '2D Shapes: Sides, Vertices and Attributes', '2D Shapes',
         'Free Grade 1 2D shape worksheets for Texas TEKS 1.6A, 1.6C, 1.6D and 1.6F: name shapes, count sides and vertices, describe attributes and put shapes together. 100 questions with answers.',
         'Count sides and vertices to name a shape.', 'Triangle 3, square 4, hexagon 6, circle 0.',
         body, faq, sets, seo_title='Grade 1 2D Shapes Worksheets: Sides and Vertices (TEKS 1.6D)')


if __name__ == "__main__":
    build()
