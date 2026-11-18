# -*- coding: utf-8 -*-
"""
Texas Grade 3 Math: 2D and 3D Figures and Quadrilaterals (TEKS 3.6A, 3.6B)
  python3 tools/gen_ustx_math_g3_2d_and_3d_figures.py
Naming quadrilaterals by their attributes (rhombus, parallelogram, trapezoid, rectangle, square), shared
attributes, quadrilaterals that fit none of these names, faces, edges and vertices of 3D figures (cubes,
rectangular and triangular prisms, cones, cylinders, spheres), and the 2D faces and nets of 3D figures.
Sets 1 to 3 use the US Grade 3 quadrilateral makers, sets 4 and 5 the Ontario Grade 3 shape makers, with Texas
names and US spelling.
Wrong answers come from real mistakes: naming a shape by how it is turned, thinking a square is not a rectangle,
counting the hidden edges twice or not at all, and calling a circle face a sphere.
"""
import random
from tx_common import (finish, make, lesson, S, run_many, adopt, People, example)
import gen_us_math_g3_quadrilaterals as usq
import gen_caon_math_g3_shapes as on

adopt(usq)
adopt(on)
on.People = People
R = random.Random(61901)


def build():
    sets = []
    for title, fn, args in [("Name the quadrilateral", usq.set_name, ("rnd",)),
                            ("Sides and angles: shared attributes", usq.set_attr, ("rnd",)),
                            ("Other quadrilaterals and real-world shapes", usq.set_other, ("rnd",)),
                            ("Faces, edges and vertices of 3D figures", on.set_fev, ("rnd", People)),
                            ("2D faces of 3D figures, and nets", on.set_faces, ("rnd", People))]:
        sets.append(S(title, run_many(fn, *args, seed=201 + len(sets), avoid=sets)))
    for s in sets[3:]:
        for it in s["items"]:
            for k in ("q", "e"):
                it[k] = it[k].replace("3D object", "3D figure").replace("3D Object", "3D Figure")
            it["c"] = [c.replace("3D object", "3D figure") for c in it["c"]]
    finish(sets, R)
    body = lesson(
        "<ul><li>A <b>quadrilateral</b> has 4 straight sides and 4 angles. Its name comes from its attributes, not from how it is turned.</li>"
        "<li><b>Trapezoid</b>: at least one pair of parallel sides. <b>Parallelogram</b>: 2 pairs of parallel sides. <b>Rectangle</b>: 4 right angles. <b>Rhombus</b>: 4 equal sides. <b>Square</b>: 4 equal sides and 4 right angles, so a square is also a rectangle and a rhombus.</li>"
        "<li>Some quadrilaterals fit none of these names, like a kite or a shape with no parallel sides.</li>"
        "<li>3D figures have <b>faces</b> (flat surfaces), <b>edges</b> (where faces meet) and <b>vertices</b> (corners). A cube has 6 faces, 12 edges and 8 vertices. Cones, cylinders and spheres have curved surfaces.</li></ul>",
        [example("Is a square a rectangle?", ["A rectangle needs 4 right angles.", "A square has 4 right angles."], "Yes. Every square is a rectangle."),
         example("How many faces does a triangular prism have?", ["2 triangle faces", "3 rectangle faces"], "5 faces")],
        [["Naming a shape by how it is turned", "Check the sides and angles. A turned square is still a square."],
         ["Thinking a square is not a rectangle", "A square has 4 right angles, so it is a special rectangle."],
         ["Mixing up a circle and a sphere", "A circle is flat (2D). A sphere is solid (3D)."]])
    faq = [("What does TEKS 3.6A ask?", "Classify and sort 2D and 3D figures, including cones, cylinders, spheres, triangular and rectangular prisms and cubes, by their attributes using formal geometric language."),
           ("What does TEKS 3.6B ask?", "Use attributes to recognize rhombuses, parallelograms, trapezoids, rectangles and squares as quadrilaterals, and draw quadrilaterals that are none of these."),
           ("What is the difference between a face, an edge and a vertex?", "A face is a flat surface, an edge is a line where two faces meet, and a vertex is a corner where edges meet."),
           ("Why can one shape have more than one name?", "Names describe attributes. A square has 4 equal sides (rhombus), 4 right angles (rectangle) and 2 pairs of parallel sides (parallelogram).")]
    make("2d-and-3d-figures", 19, "Geometry and Measurement", "3.6A, 3.6B",
         "3.6A classify and sort two- and three-dimensional figures, including cones, cylinders, spheres, triangular and rectangular prisms, and cubes, based on attributes using formal geometric language; 3.6B use attributes to recognize rhombuses, parallelograms, trapezoids, rectangles, and squares as examples of quadrilaterals and draw examples of quadrilaterals that do not belong to any of these subcategories",
         "2D and 3D Figures: Quadrilaterals, Faces, Edges and Vertices", "2D and 3D Figures",
         "Free Grade 3 geometry worksheets for Texas TEKS 3.6A and 3.6B: name quadrilaterals, rhombuses, parallelograms, trapezoids, rectangles and squares, faces, edges and vertices of 3D figures, and nets. 100 questions with answers.",
         "Name a figure by its attributes: sides, angles, faces, edges and vertices.", "A square is also a rectangle and a rhombus. A cube has 6 faces, 12 edges and 8 vertices.",
         body, faq, sets, seo_title="Grade 3 2D and 3D Figures Worksheets: Quadrilaterals (TEKS 3.6A, 3.6B, STAAR)")


if __name__ == "__main__":
    build()
