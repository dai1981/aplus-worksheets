# -*- coding: utf-8 -*-
"""
Texas Grade 2 Math: 3D Solids: Faces, Edges and Vertices (TEKS 2.8B, 2.8D)
  python3 tools/gen_ustx_math_g2_solids_3d.py
Cubes (US Grade 2 maker), faces, edges and vertices and the faces of solids (Ontario makers with Texas names), and
sorting spheres, cones, cylinders, rectangular prisms and triangular prisms (own makers).
Wrong answers come from real mistakes: mixing up 2D and 3D names, counting only the faces you can see, and
thinking a cube is not a rectangular prism.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g2_shapes as sh
adopt(sh)
import gen_caon_math_g3_shapes as csh
adopt(csh)
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


SOL = [("sphere", "It is round like a ball and can roll", 0, 0, 0), ("cone", "It has 1 flat circle face and 1 vertex", 1, 0, 1), ("cylinder", "It has 2 flat circle faces and can roll", 2, 0, 0),
       ("cube", "It has 6 square faces", 6, 12, 8), ("rectangular prism", "It has 6 rectangle faces, like a box", 6, 12, 8), ("triangular prism", "It has 2 triangle faces and 3 rectangle faces", 5, 9, 6)]
REAL = [("a basketball", "sphere"), ("an ice cream cone", "cone"), ("a can of beans", "cylinder"), ("a number cube", "cube"), ("a cereal box", "rectangular prism"),
        ("a tent", "triangular prism"), ("a globe", "sphere"), ("a party hat", "cone"), ("a drum", "cylinder"), ("a brick", "rectangular prism"), ("a sugar cube", "cube"), ("a wedge of cheese", "triangular prism"), ("a juice box", "rectangular prism"), ("a candle", "cylinder"), ("a marble", "sphere"), ("a traffic cone", "cone")]


def one_clue(r):
    name, clue, f, e, v = r.choice(SOL)
    others = [s[0] for s in SOL if s[0] != name]
    return mcq("%s. Which solid is it?" % clue, "A " + name, ["A " + x for x in r.sample(others, 3)], "<b>A %s</b>: %s." % (name, clue[0].lower() + clue[1:]))


def one_real(r):
    obj, name = r.choice(REAL)
    others = [s[0] for s in SOL if s[0] != name]
    return mcq("Which solid is shaped like %s?" % obj, "A " + name, ["A " + x for x in r.sample(others, 3)], "%s is shaped like <b>a %s</b>." % (obj[0].upper() + obj[1:], name))


SORT = [("Which solid can roll and can also stack?", "A cylinder", ["A sphere", "A cube", "A triangular prism"], "A cylinder has flat faces to stack and a curved surface to roll."),
        ("Which solid has no flat faces?", "A sphere", ["A cone", "A cylinder", "A cube"], "A sphere is curved all over."),
        ("Which solid is a special rectangular prism with all square faces?", "A cube", ["A cylinder", "A cone", "A sphere"], "A cube is a rectangular prism with 6 equal square faces."),
        ("Which solids have a curved surface?", "Sphere, cone and cylinder", ["Cube and prism", "Only the cube", "Triangular prism and cube"], "Spheres, cones and cylinders have curved surfaces."),
        ("Two cubes are put side by side. What solid do they make?", "A rectangular prism", ["A cube", "A cylinder", "A pyramid"], "Two cubes together make a longer box: <b>a rectangular prism</b>."),
        ("Which solid has exactly 5 faces?", "A triangular prism", ["A cube", "A cylinder", "A cone"], "2 triangles + 3 rectangles = 5 faces."),
        ("How many vertices does a cone have?", "1", ["0", "2", "8"], "A cone has <b>1</b> vertex at its point.")]


def one_sort(r):
    q, a, w, e = r.choice(SORT)
    return mcq(q, a, w, e)


FEV = [("cube", 6, 12, 8), ("rectangular prism", 6, 12, 8), ("triangular prism", 5, 9, 6)]


def one_count(r):
    name, f, e, v = r.choice(FEV)
    part, n = r.choice([("faces", f), ("edges", e), ("vertices", v)])
    w = [str(x) for x in dict.fromkeys([f, e, v, n + 1, n - 1]) if x != n][:3]
    return mcq("Think of a %s. Count the hidden ones too. How many %s does it have in all?" % (name, part), str(n), w,
               "A %s has %d faces, %d edges and %d vertices, so it has <b>%d %s</b>." % (name, f, e, v, n, part))


CMP = [("Which has more faces: a cube or a triangular prism?", "A cube", ["A triangular prism", "They have the same number", "Neither has faces"], "A cube has 6 faces; a triangular prism has 5. <b>A cube</b> has more."),
       ("Which has more edges: a cube or a triangular prism?", "A cube", ["A triangular prism", "They have the same number", "Neither has edges"], "A cube has 12 edges; a triangular prism has 9."),
       ("Which has more vertices: a cone or a cylinder?", "A cone", ["A cylinder", "They have the same number", "Both have 2"], "A cone has 1 vertex; a cylinder has 0."),
       ("Which has more flat faces: a cylinder or a cone?", "A cylinder", ["A cone", "They have the same number", "A sphere"], "A cylinder has 2 flat faces; a cone has 1."),
       ("Which has fewer vertices: a triangular prism or a rectangular prism?", "A triangular prism", ["A rectangular prism", "They have the same number", "Neither has vertices"], "A triangular prism has 6 vertices; a rectangular prism has 8."),
       ("Do a cube and a rectangular prism have the same number of faces?", "Yes, both have 6", ["No, the cube has more", "No, the prism has more", "Yes, both have 4"], "Both have <b>6 faces</b>, 12 edges and 8 vertices.")]


def one_cmp(r):
    q, a, w, e = r.choice(CMP)
    return mcq(q, a, w, e)


def build():
    sets, R = build_sets([
        ("Name the solid from a clue", [("collect", uniq(one_clue), 6), ("collect", uniq(one_real), 14)]),
        ("Cubes: faces, edges and vertices", [("run", sh.set_cube, ("rnd", sh.People), 20)]),
        ("Faces, edges and vertices of solids", [("run", csh.set_fev, ("rnd", csh.People), 20)]),
        ("Faces of solids and nets", [("run", csh.set_faces, ("rnd", csh.People), 20)]),
        ("Sort, count and compare solids", [("collect", uniq(one_sort), 7), ("collect", uniq(one_count), 8), ("collect", uniq(one_cmp), 5)]),
    ], 69214)
    finish(sets, R)
    body = lesson('<ul><li>3D <b>solids</b>: sphere, cone, cylinder, cube, rectangular prism, triangular prism.</li><li><b>Faces</b> are flat surfaces, <b>edges</b> are where faces meet, <b>vertices</b> are corners.</li><li>A cube is a special rectangular prism: all 6 faces are squares.</li><li>Spheres, cones and cylinders have curved surfaces, so they can roll.</li></ul>',
        [example("A cereal box", ["6 rectangle faces"], "rectangular prism"), example("Faces of a cube", ["6 squares"], "6 faces, 12 edges, 8 vertices")],
        [['Mixing up 2D and 3D names', 'A circle is flat; a sphere is solid.'], ['Counting only the faces you can see', 'Count the back, bottom and hidden faces too.'], ['Thinking a cube is not a rectangular prism', 'A cube is a special rectangular prism.']])
    faq = [('What does TEKS 2.8B ask?', 'Classify and sort three-dimensional solids, including spheres, cones, cylinders, rectangular prisms (including cubes as special rectangular prisms) and triangular prisms, based on attributes using formal geometric language.'), ('What does TEKS 2.8D ask?', 'Compose two-dimensional shapes and three-dimensional solids with given properties or attributes.'), ('Does a cylinder have vertices?', 'No. It has 2 flat circle faces and no corners.'), ('What is a net?', 'A flat shape that folds up into a solid.')]
    make('3d-solids', 14, 'Geometry and Measurement', '2.8B, 2.8D',
         '2.8B classify and sort three-dimensional solids, including spheres, cones, cylinders, rectangular prisms (including cubes as special rectangular prisms), and triangular prisms, based on attributes using formal geometric language; 2.8D compose two-dimensional shapes and three-dimensional solids with given properties or attributes',
         '3D Solids: Faces, Edges and Vertices', '3D Solids',
         'Free Grade 2 3D solid worksheets for Texas TEKS 2.8B and 2.8D: spheres, cones, cylinders, cubes and prisms, faces, edges and vertices, and sorting solids. 100 questions with answers.',
         'Faces are flat, edges are lines, vertices are corners.', 'A cube has 6 faces, 12 edges and 8 vertices.',
         body, faq, sets, seo_title='Grade 2 3D Solids Worksheets: Faces, Edges and Vertices (TEKS 2.8B)')


if __name__ == "__main__":
    build()
