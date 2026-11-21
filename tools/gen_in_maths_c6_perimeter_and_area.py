# -*- coding: utf-8 -*-
"""
India Class 6 Maths, Ganita Prakash Chapter 6: Perimeter and Area
  python3 tools/gen_in_maths_c6_perimeter_and_area.py
Perimeter of rectangles, squares, triangles and regular polygons, a missing side from the perimeter, area of rectangles
and squares, area of a triangle as half a rectangle, rectilinear shapes, and problems (fencing, tiles, running rounds).
Wrong answers come from real mistakes: adding only two sides for the perimeter, mixing up area and perimeter, and units
cm instead of cm².
"""
import random
from in_common import num, unit, T, QN, adopt, gb, inr
import gen_uk_maths_y7_perimeter_and_area as pa

R = random.Random(906006)
adopt(pa, R)


def one_per(r):
    kind = r.choice(["rect", "rect", "sq", "tri", "poly"])
    if kind == "rect":
        l, w = r.sample(range(3, 40), 2)
        return QN("Find the perimeter of a rectangle %d cm long and %d cm wide." % (l, w), 2 * (l + w), [l + w, l * w, 2 * l + w], "2 × (%d + %d) = <b>%d cm</b>." % (l, w, 2 * (l + w)), unit=" cm")
    if kind == "sq":
        s = r.randint(3, 40)
        return QN("Find the perimeter of a square of side %d cm." % s, 4 * s, [s * s, 2 * s, s + 4], "4 × %d = <b>%d cm</b>." % (s, 4 * s), unit=" cm")
    if kind == "tri":
        a, b, c = sorted(r.sample(range(4, 30), 3))
        if a + b <= c:
            return None
        return QN("A triangle has sides %d cm, %d cm and %d cm. Find its perimeter." % (a, b, c), a + b + c, [a + b, a * b * c // 10 if a * b * c // 10 != a + b + c else a + b + c + 10, a + b + c - a],
                  "%d + %d + %d = <b>%d cm</b>." % (a, b, c, a + b + c), unit=" cm")
    n, name = r.choice([(5, "pentagon"), (6, "hexagon"), (8, "octagon"), (3, "equilateral triangle"), (10, "decagon")])
    s = r.randint(3, 25)
    return QN("Find the perimeter of a regular %s with sides of %d cm." % (name, s), n * s, [s * (n - 1), s + n, s * s], "%d × %d = <b>%d cm</b>." % (n, s, n * s), unit=" cm")


def one_area(r):
    kind = r.choice(["rect", "rect", "sq", "back", "half"])
    if kind == "rect":
        l, w = r.sample(range(3, 30), 2)
        return QN("Find the area of a rectangle %d cm long and %d cm wide." % (l, w), l * w, [2 * (l + w), l + w, l * w // 2 if l * w % 2 == 0 else l * w + 1], "%d × %d = <b>%d cm²</b>." % (l, w, l * w), unit=" cm²")
    if kind == "sq":
        s = r.randint(3, 25)
        return QN("Find the area of a square of side %d m." % s, s * s, [4 * s, 2 * s, s * s + s], "%d × %d = <b>%d m²</b>." % (s, s, s * s), unit=" m²")
    if kind == "back":
        w, l = r.sample(range(3, 25), 2)
        return QN("A rectangle has area %d cm² and length %d cm. Find its width." % (l * w, l), w, [l * w - l, l * w // 2 - l if l * w // 2 - l > 0 and l * w // 2 - l != w else w + 2, w * 2], "%d ÷ %d = <b>%d cm</b>." % (l * w, l, w), unit=" cm")
    l, w = r.randint(3, 20), r.choice([2, 4, 6, 8, 10, 12])
    return QN("A rectangle %d cm by %d cm is cut along a diagonal. What is the area of each triangle?" % (l, w), l * w // 2, [l * w, l + w, l * w // 4 if l * w % 4 == 0 else l * w // 2 + 1],
              "Half of %d × %d = <b>%d cm²</b>." % (l, w, l * w // 2), unit=" cm²")


def one_word(r):
    kind = r.choice(["fence", "tiles", "rounds", "paint"])
    if kind == "fence":
        l, w = r.randint(10, 60), r.randint(8, 40)
        rate = r.choice([10, 15, 20, 25, 40, 50])
        return T("A rectangular park is %d m by %d m. Fencing costs %s per metre. What is the cost of fencing it?" % (l, w, inr(rate)), inr(2 * (l + w) * rate),
                 [inr(l * w * rate), inr((l + w) * rate), inr(2 * (l + w))], "Perimeter = %d m. Cost = %d × %d = <b>%s</b>." % (2 * (l + w), 2 * (l + w), rate, inr(2 * (l + w) * rate)))
    if kind == "tiles":
        t = r.choice([20, 25, 50])
        a, b = r.randint(2, 8) * t, r.randint(2, 8) * t
        n = (a // t) * (b // t)
        return QN("A floor is %d cm by %d cm. How many square tiles of side %d cm are needed to cover it?" % (a, b, t), n, [a * b // t, 2 * (a + b) // t, n + a // t],
                  "%d × %d tiles = <b>%d</b>." % (a // t, b // t, n))
    if kind == "rounds":
        l, w = r.randint(50, 150), r.randint(30, 100)
        k = r.randint(2, 5)
        return QN("A rectangular ground is %d m by %d m. Meena runs %d rounds. How far does she run?" % (l, w, k), 2 * (l + w) * k, [(l + w) * k, l * w * k, 2 * (l + w) + k],
                  "%d rounds × %d m = <b>%s m</b>." % (k, 2 * (l + w), num(2 * (l + w) * k)), unit=" m")
    l, w = r.randint(3, 9), r.randint(2, 6)
    rate = r.choice([20, 30, 40, 50])
    return T("A wall is %d m long and %d m high. Painting costs %s per m². What is the cost?" % (l, w, inr(rate)), inr(l * w * rate),
             [inr(2 * (l + w) * rate), inr(l * w), inr((l + w) * rate)], "Area = %d m². Cost = %d × %d = <b>%s</b>." % (l * w, l * w, rate, inr(l * w * rate)))


def main():
    unit(6, 0, 6, "perimeter-and-area", 6, "M", "Perimeter and Area: Rectangles, Squares and Triangles", "perimeter and area",
         "Perimeter of rectangles, squares, triangles and regular polygons; area of rectangles, squares and triangles; area on a grid and rectilinear shapes (summary of NCERT Ganita Prakash Class 6)",
         "Class 6 Perimeter and Area worksheet (Ganita Prakash Chapter 6): perimeter and area of rectangles, squares and triangles, composite shapes and word problems. 100 questions with answers.",
         "Perimeter is the distance around; area is the space inside", "Rectangle: P = 2 × (l + w), A = l × w.",
         "<p>The <b>perimeter</b> is the total length of the boundary. Rectangle: 2 × (length + width). Square: 4 × side. Regular polygon: number of sides × side.</p>"
         "<p>The <b>area</b> is the number of unit squares that cover a shape. Rectangle: length × width. Square: side × side. A diagonal cuts a rectangle into two triangles of half the area.</p>",
         [("A rectangle is 12 cm by 5 cm. Find its perimeter and area.", ["P = 2 × (12 + 5)", "A = 12 × 5"], "34 cm and 60 cm²"),
          ("A square has perimeter 36 m. Find its area.", ["Side = 36 ÷ 4 = 9 m"], "81 m²")],
         ["Adding only the length and width for the perimeter (it is twice that).", "Mixing up area and perimeter.", "Writing the area in cm instead of cm²."],
         [("What is the difference between perimeter and area?", "Perimeter is the length around a shape (in cm or m); area is the amount of surface inside it (in cm² or m²)."),
          ("How do you find the perimeter of a rectangle?", "Add all four sides: 2 × (length + width)."),
          ("How is the area of a triangle related to a rectangle?", "A diagonal cuts a rectangle into two equal triangles, so each has half the rectangle's area.")],
         [("Perimeter", [(one_per, 20)]),
          ("Area of rectangles and squares", [(one_area, 20)]),
          ("Area of triangles", [(gb(pa.one_rt), 14), (one_area, 6)]),
          ("Rectilinear shapes", [(gb(pa.one_comp), 10), (gb(pa.one_per), 10)]),
          ("Problems", [(one_word, 20)])], R)


if __name__ == "__main__":
    main()
