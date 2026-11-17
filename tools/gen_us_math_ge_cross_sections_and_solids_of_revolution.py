# -*- coding: utf-8 -*-
"""
US Geometry: Cross Sections and Solids of Revolution (Common Core G-GMD.B.4)
  python3 tools/gen_us_math_ge_cross_sections_and_solids_of_revolution.py
The shapes of cross sections of prisms, pyramids, cylinders, cones and spheres; the solid made by rotating a
2D shape about a line; volumes of solids of revolution; and areas of cross sections.
Wrong answers come from real mistakes: thinking every slice of a solid has the shape of its base, swapping
the radius and the height when a shape is rotated, and using the radius of a sphere for every slice.
"""
import math
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, num, MINUS

R = random.Random(94201)


def kp(k, unit=""):
    k = F(k)
    if k.denominator == 1:
        s = ("" if k == 1 else num(k)) + "π"
    else:
        s = "<span class='fr'><span class='fn'>%sπ</span><span class='fd'>%d</span></span>" % ("" if k.numerator == 1 else k.numerator, k.denominator)
    return s + unit


# ------------------------------------------------------------ set 1: prisms and pyramids
PRISM = [
    ("A cube is cut by a plane parallel to one face.", "Square", ["Rectangle that is not a square", "Triangle", "Hexagon"],
     "Every slice parallel to a face is a copy of that face."),
    ("A cube is cut by a plane through two opposite edges (diagonally through the cube).", "Rectangle that is not a square", ["Square", "Triangle", "Pentagon"],
     "The cut goes along an edge and the diagonal of two faces, so it is longer one way than the other."),
    ("A cube is cut by a plane through three vertices that are each next to the same corner.", "Equilateral triangle", ["Right triangle", "Square", "Hexagon"],
     "Each side of the slice is a face diagonal, and all face diagonals are equal."),
    ("A cube is cut by a plane through the midpoints of six of its edges, perpendicular to a long diagonal.", "Regular hexagon", ["Square", "Octagon", "Pentagon"],
     "The slice crosses all six faces, and each side is the same length."),
    ("A rectangular prism is cut by a plane parallel to its base.", "Rectangle", ["Triangle", "Trapezoid", "Circle"], "Slices parallel to the base are copies of the base."),
    ("A triangular prism is cut by a plane parallel to its triangular bases.", "Triangle", ["Rectangle", "Square", "Pentagon"], "Slices parallel to the base are copies of the base."),
    ("A triangular prism is cut by a plane perpendicular to its bases, through two lateral edges' midpoints parallel to a lateral face.", "Rectangle", ["Triangle", "Circle", "Hexagon"],
     "A vertical slice of a prism runs the full height, with straight parallel sides."),
    ("A square pyramid is cut by a plane parallel to its base.", "Square", ["Triangle", "Rectangle that is not a square", "Trapezoid"],
     "A slice parallel to the base is a smaller copy of the base."),
    ("A square pyramid is cut by a vertical plane through its apex and the midpoints of two opposite base edges.", "Isosceles triangle", ["Square", "Trapezoid", "Rectangle"],
     "The slice goes through the apex down to the base, so it is a triangle with two equal slanted sides."),
    ("A square pyramid is cut by a vertical plane that does not pass through the apex but is parallel to a base edge.", "Trapezoid", ["Triangle", "Square", "Circle"],
     "The slice is cut off below the apex, so the top edge is shorter than the bottom edge."),
    ("A hexagonal prism is cut by a plane parallel to its bases.", "Hexagon", ["Rectangle", "Triangle", "Circle"], "Slices parallel to the base are copies of the base."),
    ("A pentagonal pyramid is cut by a plane parallel to its base.", "Pentagon", ["Triangle", "Square", "Hexagon"], "A slice parallel to the base is a smaller copy of the base."),
]


def one_prism(r):
    q, right, wr, e = r.choice(PRISM)
    return T("What shape is the cross section? %s" % q, right, wr, e + " <b>%s</b>." % right)


# ------------------------------------------------------------ set 2: round solids
ROUND = [
    ("A cylinder is cut by a plane parallel to its bases.", "Circle", ["Rectangle", "Ellipse that is not a circle", "Triangle"], "Each horizontal slice is a copy of the circular base."),
    ("A cylinder is cut by a vertical plane through its axis.", "Rectangle", ["Circle", "Triangle", "Trapezoid"], "The slice is as wide as the diameter and as tall as the cylinder."),
    ("A cylinder is cut by a tilted plane that does not touch the bases.", "Ellipse (an oval)", ["Circle", "Rectangle", "Parabola"], "A tilted slice through the curved side stretches the circle into an oval."),
    ("A cone is cut by a plane parallel to its base.", "Circle", ["Triangle", "Ellipse that is not a circle", "Trapezoid"], "A slice parallel to the base is a smaller circle."),
    ("A cone is cut by a vertical plane through its apex and the center of its base.", "Isosceles triangle", ["Circle", "Rectangle", "Right triangle"],
     "The slice has the two slant heights as equal sides and the diameter as the base."),
    ("A sphere is cut by any plane that passes through it.", "Circle", ["Ellipse that is not a circle", "Hemisphere", "Square"], "Every slice of a sphere is a circle. Through the center it is a great circle."),
    ("A sphere is cut by a plane through its center.", "The largest possible circle (a great circle)", ["The smallest possible circle", "An ellipse that is not a circle", "A hemisphere"],
     "The slice through the center has the same radius as the sphere."),
    ("A cone is cut by a tilted plane that crosses only the curved surface.", "Ellipse (an oval)", ["Circle", "Triangle", "Rectangle"], "Tilting the slice stretches the circle into an ellipse."),
]


def one_round(r):
    q, right, wr, e = r.choice(ROUND)
    if r.random() < 0.35:
        items = [("Which solid has a circle as its cross section parallel to the base and a triangle as its vertical cross section through the top?", "Cone", ["Cylinder", "Sphere", "Square pyramid"]),
                 ("Which solid has circles for all of its horizontal cross sections, all the same size?", "Cylinder", ["Cone", "Sphere", "Pyramid"]),
                 ("Which solid has a circle as every cross section, no matter how it is cut?", "Sphere", ["Cylinder", "Cone", "Cube"]),
                 ("Which solid has a square as its horizontal cross section and a triangle as its vertical cross section through the top?", "Square pyramid", ["Cube", "Cone", "Triangular prism"]),
                 ("Which solid has horizontal cross sections that are squares, all the same size?", "Square prism", ["Square pyramid", "Cone", "Sphere"])]
        q2, right2, wr2 = r.choice(items)
        return T(q2, right2, wr2, "Picture slicing the solid. <b>%s</b>." % right2)
    return T("What shape is the cross section? %s" % q, right, wr, e + " <b>%s</b>." % right)


# ------------------------------------------------------------ set 3: what solid is made?
def one_rev(r):
    kind = r.choice(["rect", "rect", "tri", "tri", "semi", "circ", "rect_off"])
    if kind == "rect":
        w, h = r.sample(range(2, 12), 2)
        axis = r.choice(["w", "h"])
        q = ("An " if w in (8, 11, 18) else "A ") + "%d cm by %d cm rectangle is rotated about its %d cm side. What solid is formed, and what are its dimensions?" % (w, h, h if axis == "h" else w)
        rad, ht = (w, h) if axis == "h" else (h, w)
        right = "A cylinder with radius %d cm and height %d cm" % (rad, ht)
        return T(q, right, ["A cylinder with radius %d cm and height %d cm" % (ht, rad), "A cone with radius %d cm and height %d cm" % (rad, ht),
                            "A cylinder with radius %s cm and height %d cm" % (num(F(rad, 2)), ht)],
                 "The side it turns around becomes the axis (the height). The other side sweeps out the radius. <b>%s</b>." % right)
    if kind == "tri":
        a, b = r.sample(range(3, 13), 2)
        q = "A right triangle with legs %d in. and %d in. is rotated about the %d in. leg. What solid is formed?" % (a, b, a)
        right = "A cone with height %d in. and radius %d in." % (a, b)
        return T(q, right, ["A cone with height %d in. and radius %d in." % (b, a), "A cylinder with height %d in. and radius %d in." % (a, b), "A pyramid with height %d in." % a],
                 "The leg it turns around is the height; the other leg sweeps out the circular base. <b>%s</b>." % right)
    if kind == "semi":
        rad = r.randint(2, 15)
        q = "A semicircle with radius %d ft is rotated about its diameter. What solid is formed?" % rad
        right = "A sphere with radius %d ft" % rad
        return T(q, right, ["A sphere with radius %d ft" % (2 * rad), "A cylinder with radius %d ft" % rad, "A cone with radius %d ft" % rad],
                 "Turning a half circle about its straight edge makes a ball. <b>%s</b>." % right)
    if kind == "circ":
        q = "A circle is rotated about a line in its plane that does not touch it. What solid is formed?"
        return T(q, "A torus (a donut shape)", ["A sphere", "A cylinder", "A cone"], "The circle sweeps around the line and leaves a hole in the middle. <b>A torus (a donut shape)</b>.")
    w, h = r.randint(2, 6), r.randint(3, 10)
    q = ("An " if w in (8, 11, 18) else "A ") + "%d by %d rectangle is rotated about its side of length %d. Which shape is the vertical cross section of the solid through its axis?" % (w, h, h)
    right = "%s %d by %d rectangle" % ("An" if 2 * w in (8, 11, 18) else "A", 2 * w, h)
    return T(q, right, ["%s %d by %d rectangle" % ("An" if w in (8, 11, 18) else "A", w, h), "A circle with radius %d" % w, "A triangle with base %d" % (2 * w)],
             "The solid is a cylinder with radius %d and height %d. A slice through the axis is %d wide (the diameter) and %d tall. <b>%s</b>." % (w, h, 2 * w, h, right))


# ------------------------------------------------------------ set 4: volume of a solid of revolution
def one_vol(r):
    kind = r.choice(["cyl", "cyl", "cone", "cone", "sph"])
    if kind == "cyl":
        a, b = r.sample(range(2, 10), 2)
        q = "A rectangle %d cm wide and %d cm tall is rotated about its %d cm side. Find the volume of the solid in terms of π." % (a, b, b)
        V = a * a * b
        return T(q, kp(V, " cm³"), [kp(b * b * a, " cm³"), kp(F(V, 3), " cm³"), kp(2 * a * b, " cm³")],
                 "The solid is a cylinder with radius %d and height %d: π × %d² × %d = <b>%s</b>." % (a, b, a, b, kp(V, " cm³")))
    if kind == "cone":
        a, b = r.sample(range(2, 10), 2)
        q = "A right triangle with legs %d in. and %d in. is rotated about the %d in. leg. Find the volume in terms of π." % (a, b, a)
        V = F(b * b * a, 3)
        return T(q, kp(V, " in.³"), [kp(F(a * a * b, 3), " in.³"), kp(b * b * a, " in.³"), kp(F(a * b, 3), " in.³")],
                 "The solid is a cone with radius %d and height %d: ⅓ × π × %d² × %d = <b>%s</b>." % (b, a, b, a, kp(V, " in.³")))
    rad = 3 * r.randint(1, 4)
    q = "A semicircle with radius %d m is rotated about its diameter. Find the volume in terms of π." % rad
    V = F(4 * rad ** 3, 3)
    return T(q, kp(V, " m³"), [kp(F(2 * rad ** 3, 3), " m³"), kp(4 * rad * rad, " m³"), kp(F(4 * (2 * rad) ** 3, 3), " m³")],
             "The solid is a sphere with radius %d: ⁴⁄₃ × π × %d³ = <b>%s</b>." % (rad, rad, kp(V, " m³")))


# ------------------------------------------------------------ set 5: area of a cross section
def one_area(r):
    kind = r.choice(["sph", "sph", "cone", "pyr", "cyl"])
    if kind == "sph":
        rad, d, c = r.choice([(5, 3, 4), (5, 4, 3), (10, 6, 8), (10, 8, 6), (13, 5, 12), (13, 12, 5), (15, 9, 12), (17, 8, 15), (25, 7, 24)])
        q = "A sphere has radius %d cm. A plane cuts it %d cm from the center. Find the area of the cross section in terms of π." % (rad, d)
        return T(q, kp(c * c, " cm²"), [kp(rad * rad, " cm²"), kp((rad - d) ** 2, " cm²"), kp(c, " cm²")],
                 "The slice is a circle. Its radius, the distance %d and the sphere's radius %d form a right triangle: <i>r</i>² = %d² %s %d² = %d. Area = <b>%s</b>." % (
                     d, rad, rad, MINUS, d, c * c, kp(c * c, " cm²")))
    if kind == "cone":
        rad, h = 2 * r.randint(2, 9), r.randint(4, 20)
        q = "A cone has base radius %d in. and height %d in. It is cut parallel to the base halfway up. Find the area of the cross section in terms of π." % (rad, h)
        k = (rad // 2) ** 2
        return T(q, kp(k, " in.²"), [kp(rad * rad, " in.²"), kp(F(rad * rad, 2), " in.²"), kp(rad // 2, " in.²")],
                 "Halfway up, the slice is a circle with half the radius: %d. Area = π × %d² = <b>%s</b>." % (rad // 2, rad // 2, kp(k, " in.²")))
    if kind == "pyr":
        s_, f = 2 * r.randint(2, 9), r.choice([F(1, 2), F(1, 3), F(2, 3)])
        if (s_ * f).denominator > 1:
            return None
        q = "A square pyramid has base edges of %d ft. A cross section parallel to the base is taken %s of the way down from the apex. Find its area." % (
            s_, {F(1, 2): "half", F(1, 3): "one third", F(2, 3): "two thirds"}[f])
        side = s_ * f
        A = side * side
        return T(q, "%s ft²" % num(A), ["%s ft²" % num(w) for w in dict.fromkeys([s_ * s_ * f, s_ * s_, side]) if w != A][:3],
                 "The slice is a square whose side is %s of %d, which is %s ft. Area = %s² = <b>%s ft²</b>." % (
                     {F(1, 2): "half", F(1, 3): "one third", F(2, 3): "two thirds"}[f], s_, num(side), num(side), num(A)))
    rad, h = r.randint(2, 10), r.randint(3, 15)
    q = "A cylinder has radius %d cm and height %d cm. Find the area of the vertical cross section through its axis." % (rad, h)
    A = 2 * rad * h
    return T(q, "%d cm²" % A, ["%d cm²" % w for w in dict.fromkeys([rad * h, rad * rad * h, 2 * rad + 2 * h]) if w != A][:3] + (["%d cm²" % (A + 4)] if len({rad * h, rad * rad * h, 2 * rad + 2 * h} - {A}) < 3 else []),
             "The slice is a rectangle as wide as the diameter (%d) and as tall as the cylinder (%d): <b>%d cm²</b>." % (2 * rad, h, A))


def build():
    sets = [S("Cross sections of prisms and pyramids", prism_set()),
            S("Cross sections of cylinders, cones and spheres", collect(one_round, 13, R) + collect_items(R)),
            S("Rotate a shape: what solid?", collect(one_rev, 20, R)),
            S("Volume of a solid of revolution", collect(one_vol, 20, R)),
            S("Area of a cross section", collect(one_area, 20, R))]
    body = lesson(
        "<p>A <b>cross section</b> is the flat shape you see when you slice a solid with a plane.</p>"
        "<ul><li>A slice <b>parallel to the base</b> of a prism or cylinder is a copy of the base. For a pyramid or cone it is a smaller copy.</li>"
        "<li>A <b>vertical slice through the top</b> of a pyramid or cone is a triangle. Through the axis of a cylinder it is a rectangle.</li>"
        "<li>Every slice of a <b>sphere</b> is a circle.</li></ul>"
        "<p>Rotating a 2D shape about a line makes a <b>solid of revolution</b>: a rectangle makes a cylinder, a right triangle makes a cone, "
        "and a semicircle makes a sphere. The side you turn around becomes the height; the other side becomes the radius.</p>",
        [("A 3 by 5 rectangle is rotated about its 5 side. Find the volume.", ["Cylinder: radius 3, height 5", "π × 9 × 5"], "45π"),
         ("A sphere of radius 10 is cut 6 units from the center. Find the area of the slice.", ["<i>r</i>² = 100 %s 36 = 64" % MINUS], "64π")],
        ["Thinking every slice of a solid looks like its base. Tilted and vertical slices can be different shapes.",
         "Swapping the radius and the height when a shape is rotated.",
         "Using the sphere's radius for a slice that does not pass through the center.",
         "Forgetting that a cone's slice halfway up has half the radius, so a quarter of the area."])
    faq = [("What is a cross section?", "The two-dimensional shape made where a plane slices through a three-dimensional solid."),
           ("What shapes can a cross section of a cube be?", "Depending on the angle of the cut: a square, a rectangle, a triangle, a pentagon or a hexagon."),
           ("What solid do you get by rotating a rectangle?", "A cylinder. The side it rotates around becomes the height, and the other side becomes the radius."),
           ("What solid do you get by rotating a right triangle about a leg?", "A cone. The leg it rotates around is the height, and the other leg is the radius of the base.")]
    make("cross-sections-and-solids-of-revolution", 22, "G-GMD.B.4",
         "Cross Sections and Solids of Revolution",
         "Cross Sections and Solids of Revolution Worksheet (Geometry, G-GMD.B.4) | 100 Questions",
         "Cross Sections and Solids of Revolution",
         "Identify the shapes of two-dimensional cross-sections of three-dimensional objects, and identify three-dimensional objects generated by rotations of two-dimensional objects.",
         "Free Geometry worksheet on cross sections of prisms, pyramids, cylinders, cones and spheres, and solids made by rotating 2D shapes. 100 questions with answers.",
         "A slice parallel to the base copies the base. Every slice of a sphere is a circle.",
         "Rotate a rectangle: cylinder. Rotate a right triangle: cone. Rotate a semicircle: sphere.",
         body, faq, sets, R, domain="Volume and Solids", grade="geometry")


def prism_set():
    items = []
    for q, right, wr, e in PRISM:
        items.append(T("What shape is the cross section? %s" % q, right, wr, e + " <b>%s</b>." % right))
    extra = [("Which cross section is NOT possible for a cube?", "Circle", ["Triangle", "Hexagon", "Rectangle"], "A cube has only flat faces and straight edges, so a slice can never be curved."),
             ("Which cross section is NOT possible for a square pyramid?", "Hexagon", ["Triangle", "Square", "Trapezoid"], "A square pyramid has only five faces, so a slice can have at most five sides."),
             ("How many sides can a cross section of a cube have at most?", "6", ["4", "5", "8"], "A plane can cross each of the 6 faces at most once, so at most 6 sides."),
             ("A rectangular prism is cut by a plane perpendicular to its base. What shape is the cross section?", "Rectangle", ["Triangle", "Circle", "Hexagon"],
              "A vertical slice of a box has straight vertical sides and a straight top and bottom."),
             ("A cube with edges of 6 cm is cut parallel to one face. What is the area of the cross section?", "36 cm²", ["6 cm²", "216 cm²", "24 cm²"], "The slice is a 6 cm by 6 cm square."),
             ("A rectangular prism is 4 by 5 by 9 (height 9). What is the area of a cross section parallel to the base?", "20", ["36", "45", "180"], "The slice is a copy of the 4 by 5 base: 4 × 5 = 20."),
             ("A triangular prism has a right-triangle base with legs 6 and 8. What is the area of a cross section parallel to the base?", "24", ["48", "14", "30"], "The slice is a copy of the base: ½ × 6 × 8 = 24."),
             ("A cube is cut through four of its vertices, two on the top face and two on the bottom face, along diagonals of opposite faces. What shape is formed?", "Rectangle that is not a square",
              ["Square", "Triangle", "Rhombus that is not a square"], "Its sides are an edge and a face diagonal, which are different lengths.")]
    for q, right, wr, e in extra:
        items.append(T(q, right, wr, e + " <b>%s</b>." % right))
    return items[:20]


def collect_items(r):
    items = [("Which shape is the cross section of a sphere through its center if the sphere's radius is 7?", "A circle with radius 7", ["A circle with radius 14", "A circle with radius 3.5", "A square with side 7"],
              "A slice through the center is a great circle with the same radius as the sphere."),
             ("A cylinder has radius 4 and height 10. What is the area of a slice parallel to its bases, in terms of π?", "16π", ["8π", "40π", "160π"], "Each such slice is a circle with radius 4: π × 4² = 16π."),
             ("A cone is sliced parallel to its base, closer to the apex. Compared with the base, the slice is", "A smaller circle", ["A larger circle", "The same circle", "An ellipse"],
              "The cone narrows toward the apex, so the circles get smaller."),
             ("Which solid has a rectangle as its vertical cross section through the middle and a circle as its horizontal cross section?", "Cylinder", ["Cone", "Sphere", "Cube"],
              "Vertical: rectangle. Horizontal: circle. That is a cylinder."),
             ("Which solid has a triangle as its vertical cross section through the middle and a circle as its horizontal cross section?", "Cone", ["Cylinder", "Sphere", "Pyramid"],
              "Vertical through the apex: triangle. Horizontal: circle. That is a cone."),
             ("Which solid has a circle as both its vertical and horizontal cross sections through the middle?", "Sphere", ["Cylinder", "Cone", "Cube"], "Every slice of a sphere is a circle."),
             ("A plane touches a sphere at exactly one point. What is the cross section?", "A single point", ["A small circle", "A great circle", "A line segment"], "A tangent plane meets the sphere in just one point.")]
    return [T(q, right, wr, e + " <b>%s</b>." % right) for q, right, wr, e in items]


if __name__ == "__main__":
    build()
