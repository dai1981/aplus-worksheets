# -*- coding: utf-8 -*-
"""
India Class 8 Maths, Ganita Prakash Part 2, Chapter 4: Exploring Some Geometric Themes
  python3 tools/gen_in_maths_c8_exploring_some_geometric_themes.py
Fractals (the Sierpinski triangle and carpet: counting pieces and the fraction left), visualising solids (top, front and
side views), faces, edges and vertices of prisms and pyramids, and Euler's formula F + V − E = 2.
Wrong answers come from real mistakes: adding pieces instead of multiplying at each stage, confusing edges with vertices,
and mixing up the top view with the front view.
"""
import random, re
from fractions import Fraction as F
from in_common import num, unit, T, QN, gb, fr
import gen_uk_maths_y9_plans_and_elevations as pe

R = random.Random(908011)


def views(fn):
    g = gb(fn)

    def f(r):
        it = g(r)
        if not it:
            return None
        for a, b in [(r"plan</b> \(the view from above\)", "top view</b>"), (r"front elevation</b> \(the view from the front\)", "front view</b>"),
                     (r"side elevation</b> \(the view from the side\)", "side view</b>"), ("plan", "top view"), ("front elevation", "front view"), ("side elevation", "side view")]:
            it["q"], it["e"] = re.sub(a, b, it["q"]), re.sub(a, b, it["e"])
        return it
    f.__name__ = fn.__name__
    return f


def one_fractal(r):
    kind = r.choice(["tri", "tri", "frac", "carpet", "carpetf"])
    n = r.randint(1, 6)
    if kind == "tri":
        return QN("In the Sierpinski triangle, each shaded triangle is split into 4 and the middle one is removed. Starting with 1 triangle, how many shaded triangles are there after step %d?" % n,
                  3 ** n, [4 ** n, 3 * n, 3 ** n - 1 if n > 1 else 4], "Each step multiplies the number by 3: 3<sup>%d</sup> = <b>%s</b>." % (n, num(3 ** n)))
    if kind == "frac":
        n = r.randint(1, 4)
        v = F(3, 4) ** n
        return T("What fraction of the original area is still shaded in the Sierpinski triangle after step %d?" % n, fr(str(v.numerator), str(v.denominator)),
                 [fr(str(3 * n), str(4 * n)) if F(3 * n, 4 * n) != v else fr("1", str(4 ** n)), fr("1", str(4 ** n)), fr(str(3 ** n), str(4 ** n + 1))],
                 "Each step keeps 3/4: (3/4)<sup>%d</sup> = <b>%d/%d</b>." % (n, v.numerator, v.denominator))
    n = r.randint(1, 4)
    if kind == "carpet":
        return QN("In the Sierpinski carpet, each square is split into 9 and the middle one is removed. Starting with 1 square, how many squares are left after step %d?" % n,
                  8 ** n, [9 ** n, 8 * n, 8 ** n - 1 if n > 1 else 9], "Each step multiplies by 8: 8<sup>%d</sup> = <b>%s</b>." % (n, num(8 ** n)))
    v = F(8, 9) ** n
    return T("What fraction of the area is left in the Sierpinski carpet after step %d?" % n, fr(str(v.numerator), str(v.denominator)),
             [fr("1", str(9 ** n)), fr(str(8 * n), str(9 * n)) if F(8 * n, 9 * n) != v else fr("8", str(9 ** n)), fr(str(8 ** n), str(9 ** n + 1))],
             "Each step keeps 8/9: (8/9)<sup>%d</sup> = <b>%d/%d</b>." % (n, v.numerator, v.denominator))


SOLIDS = [("cube", 6, 8, 12), ("cuboid", 6, 8, 12), ("triangular prism", 5, 6, 9), ("square pyramid", 5, 5, 8), ("triangular pyramid (tetrahedron)", 4, 4, 6),
          ("pentagonal prism", 7, 10, 15), ("hexagonal prism", 8, 12, 18), ("pentagonal pyramid", 6, 6, 10), ("hexagonal pyramid", 7, 7, 12), ("octahedron", 8, 6, 12)]


def one_fve(r):
    name, f, v, e = r.choice(SOLIDS)
    kind = r.choice(["f", "v", "e", "euler", "euler"])
    if kind == "f":
        return QN("How many faces does a %s have?" % name, f, [v, e, f + 1], "A %s has <b>%d faces</b>." % (name, f))
    if kind == "v":
        return QN("How many vertices (corners) does a %s have?" % name, v, [e, f if f != v else v + 2, v + 1], "A %s has <b>%d vertices</b>." % (name, v))
    if kind == "e":
        return QN("How many edges does a %s have?" % name, e, [v, f + v, e - 2], "A %s has <b>%d edges</b>." % (name, e))
    miss = r.choice(["F", "V", "E"])
    if miss == "E":
        return QN("A solid has %d faces and %d vertices. Use Euler's formula F + V − E = 2 to find the number of edges." % (f, v), e, [f + v, f + v + 2, e + 1],
                  "E = F + V − 2 = %d + %d − 2 = <b>%d</b>." % (f, v, e))
    if miss == "V":
        return QN("A solid has %d faces and %d edges. Use F + V − E = 2 to find the number of vertices." % (f, e), v, [e - f, e + f - 2, v + 1],
                  "V = 2 + E − F = 2 + %d − %d = <b>%d</b>." % (e, f, v))
    return QN("A solid has %d vertices and %d edges. Use F + V − E = 2 to find the number of faces." % (v, e), f, [e - v, e + v - 2, f + 1],
              "F = 2 + E − V = 2 + %d − %d = <b>%d</b>." % (e, v, f))


def one_prism(r):
    n = r.randint(5, 12)
    kind = r.choice(["prism", "pyr"])
    poly = "%d-sided" % n
    if kind == "prism":
        k = r.choice(["faces", "vertices", "edges"])
        val = {"faces": n + 2, "vertices": 2 * n, "edges": 3 * n}[k]
        return QN("A prism has a %s polygon as its base. How many %s does it have?" % (poly, k), val, [n, {"faces": n + 1, "vertices": n + 2, "edges": 2 * n}[k], val + 2],
                  "A prism with an n-sided base has n + 2 faces, 2n vertices and 3n edges: <b>%d</b>." % val)
    k = r.choice(["faces", "vertices", "edges"])
    val = {"faces": n + 1, "vertices": n + 1, "edges": 2 * n}[k]
    return QN("A pyramid has a %s polygon as its base. How many %s does it have?" % (poly, k), val, [n, 3 * n if k == "edges" else n + 2, val + 2],
              "A pyramid with an n-sided base has n + 1 faces, n + 1 vertices and 2n edges: <b>%d</b>." % val)


def main():
    unit(8, 2, 4, "exploring-some-geometric-themes", 11, "G", "Exploring Some Geometric Themes: Fractals, Views and Solids", "exploring some geometric themes",
         "Fractals such as the Sierpinski triangle and carpet, visualising 3-D shapes from different views, and faces, edges and vertices of polyhedra with Euler's formula (summary of NCERT Ganita Prakash Class 8)",
         "Class 8 Exploring Some Geometric Themes worksheet (Ganita Prakash Part 2, Chapter 4): Sierpinski fractals, top, front and side views, faces, edges and vertices, Euler's formula. 100 questions with answers.",
         "F + V − E = 2", "Euler's formula holds for every polyhedron, such as a cube: 6 + 8 − 12 = 2.",
         "<p>A <b>fractal</b> repeats the same rule at smaller and smaller sizes. In the Sierpinski triangle each step keeps 3 of 4 smaller triangles, so the count is 3<sup>n</sup> and the area left is (3/4)<sup>n</sup>.</p>"
         "<p>A solid can be drawn from the <b>top</b>, <b>front</b> and <b>side</b>.</p>"
         "<p>For a polyhedron, faces F, vertices V and edges E satisfy <b>F + V − E = 2</b>. A prism on an n-sided base has n + 2 faces, 2n vertices and 3n edges.</p>",
         [("How many edges does a hexagonal prism have?", ["n = 6", "3n = 18"], "18"),
          ("A solid has 8 faces and 12 vertices. How many edges?", ["E = F + V − 2"], "18")],
         ["Adding 3 each step in the Sierpinski triangle instead of multiplying by 3.", "Mixing up vertices (corners) and edges (lines).", "Drawing the front view when the top view is asked."],
         [("What is a fractal?", "A shape made by repeating the same rule at smaller and smaller scales, such as the Sierpinski triangle."),
          ("What is Euler's formula?", "For any polyhedron, faces + vertices − edges = 2."),
          ("How many faces, vertices and edges does a prism have?", "A prism with an n-sided base has n + 2 faces, 2n vertices and 3n edges.")],
         [("Fractals and solids", [(one_fractal, 16), (one_prism, 4)]),
          ("Views of solids", [(views(pe.one_plan), 7), (views(pe.one_front), 7), (views(pe.one_numbered), 6)]),
          ("Faces, vertices and edges", [(one_fve, 20)]),
          ("Prisms and pyramids", [(one_prism, 20)]),
          ("Euler's formula and mixed problems", [(one_fve, 12), (one_prism, 8)])], R)


if __name__ == "__main__":
    main()
