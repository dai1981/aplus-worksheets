# -*- coding: utf-8 -*-
"""
UK Year 8 Maths: Volume and Surface Area of Prisms (KS3 Geometry and measures)
  python3 tools/gen_uk_maths_y8_volume_and_surface_area_of_prisms.py
Volume of cuboids and cubes, volume of prisms using the cross-section, volume of cylinders, surface area of
cuboids and triangular prisms, and capacity problems.
Wrong answers come from real mistakes: adding the dimensions, forgetting to halve the triangle, counting only
three faces for surface area, using the diameter as the radius, and 100 cm³ = 1 litre.
"""
import math
import random
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F
from uk_ks3 import num, mcq, B, S, make, lesson, collect, QN, T, svg_wrap, line, text, fig, INK, RED, GREEN

R = random.Random(81201)


def d1(x):
    return "{:,.1f}".format(float(Decimal(str(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)))


def cuboid_svg(l, w, h, u="cm"):
    x0, y0, L, H, D = 62, 150, 160, 80, 45
    dx, dy = D * 0.8, -D * 0.6
    front = [(x0, y0), (x0 + L, y0), (x0 + L, y0 - H), (x0, y0 - H)]
    s = ["<path d='M%d %d L%d %d L%d %d L%d %d Z' fill='#eef6f0' stroke='%s' stroke-width='2'/>" % (front[0] + front[1] + front[2] + front[3] + (INK,)),
         "<path d='M%d %d L%.1f %.1f L%.1f %.1f L%d %d Z' fill='#dcefe2' stroke='%s' stroke-width='2'/>" % (x0, y0 - H, x0 + dx, y0 - H + dy, x0 + L + dx, y0 - H + dy, x0 + L, y0 - H, INK),
         "<path d='M%d %d L%.1f %.1f L%.1f %.1f L%d %d Z' fill='#cfe6d6' stroke='%s' stroke-width='2'/>" % (x0 + L, y0, x0 + L + dx, y0 + dy, x0 + L + dx, y0 - H + dy, x0 + L, y0 - H, INK),
         text(x0 + L / 2, y0 + 22, "%s %s" % (num(l), u), 15), text(x0 - 10, y0 - H / 2 + 5, "%s %s" % (num(h), u), 15, anchor="end"),
         text(x0 + L + dx / 2 + 14, y0 + dy / 2 + 10, "%s %s" % (num(w), u), 15, anchor="start")]
    return svg_wrap(320, 180, "".join(s), "cuboid")


def tri_prism_svg(b, h, l, u="cm"):
    A = (62, 150); Bp = (162, 150); C = (62, 70)
    dx, dy = 130, -40
    s = ["<path d='M%d %d L%d %d L%d %d Z' fill='#eef6f0' stroke='%s' stroke-width='2'/>" % (A + Bp + C + (INK,)),
         "<path d='M%d %d L%d %d L%d %d L%d %d Z' fill='#dcefe2' stroke='%s' stroke-width='2'/>" % (C + (C[0] + dx, C[1] + dy) + (Bp[0] + dx, Bp[1] + dy) + Bp + (INK,)),
         line(Bp[0], Bp[1], Bp[0] + dx, Bp[1] + dy, INK, 2),
         "<path d='M62 138 L74 138 L74 150' fill='none' stroke='%s' stroke-width='1.6'/>" % GREEN,
         text(112, 172, "%s %s" % (num(b), u), 15), text(54, 115, "%s %s" % (num(h), u), 15, anchor="end"),
         text(Bp[0] + dx / 2 + 12, Bp[1] + dy / 2 + 18, "%s %s" % (num(l), u), 15, anchor="start")]
    return svg_wrap(340, 185, "".join(s), "triangular prism")


def cyl_svg(r, h, use_d=False, u="cm"):
    cx, top, bot, rx, ry = 110, 44, 154, 60, 16
    s = ["<path d='M%d %d L%d %d A%d %d 0 0 0 %d %d L%d %d' fill='#eef6f0' stroke='%s' stroke-width='2'/>" % (cx - rx, top, cx - rx, bot, rx, ry, cx + rx, bot, cx + rx, top, INK),
         "<ellipse cx='%d' cy='%d' rx='%d' ry='%d' fill='#dcefe2' stroke='%s' stroke-width='2'/>" % (cx, top, rx, ry, INK)]
    if use_d:
        s.append(line(cx - rx, top, cx + rx, top, RED, 2))
        s.append(text(cx, top - 6 - ry, "%s %s" % (num(r * 2), u), 15, col=RED))
    else:
        s.append(line(cx, top, cx + rx, top, RED, 2))
        s.append(text(cx + rx / 2, top - ry - 6, "%s %s" % (num(r), u), 15, col=RED))
    s.append(text(cx + rx + 10, (top + bot) / 2, "%s %s" % (num(h), u), 15, anchor="start"))
    return svg_wrap(240, 190, "".join(s), "cylinder")


# ------------------------------------------------------------ set 1: cuboids
def one_cuboid(r):
    l, w, h = r.randint(2, 15), r.randint(2, 10), r.randint(2, 12)
    if len({l, w, h}) < 3:
        return None
    if r.random() < 0.7:
        V = l * w * h
        q = "Find the volume of the cuboid.%s" % fig(cuboid_svg(l, w, h))
        e = "Volume = length × width × height = %d × %d × %d = <b>%s cm³</b>." % (l, w, h, num(V))
        return QN(q, V, [l + w + h, 2 * (l * w + w * h + l * h), l * w], e, unit=" cm³")
    V = l * w * h
    q = "A cuboid has a volume of %s cm³. It is %d cm long and %d cm wide. How high is it?" % (num(V), l, w)
    e = "Height = %s ÷ (%d × %d) = %s ÷ %d = <b>%d cm</b>." % (num(V), l, w, num(V), l * w, h)
    return QN(q, h, [V - l - w, F(V, l + w) if F(V, l + w).denominator == 1 else V // l, l * w], e, unit=" cm")


# ------------------------------------------------------------ set 2: prisms via cross-section
def one_prism(r):
    kind = r.random()
    if kind < 0.6:
        b, h, l = r.randint(3, 12), r.randint(2, 10), r.randint(4, 20)
        A = F(b * h, 2)
        V = A * l
        q = "Find the volume of the triangular prism. The triangle has a right angle.%s" % fig(tri_prism_svg(b, h, l))
        e = "Cross-section area = ½ × %d × %d = %s cm². Volume = %s × %d = <b>%s cm³</b>." % (b, h, num(A), num(A), l, num(V))
        return QN(q, V, [b * h * l, A + l, b * h + l], e, unit=" cm³")
    A = r.choice([12, 15, 18, 20, 24, 30, 36, 45])
    l = r.randint(3, 15)
    V = A * l
    shape = r.choice(["an L-shaped", "a trapezium-shaped", "a hexagonal", "a pentagonal"])
    q = "A prism has %s cross-section with area %d cm². It is %d cm long. What is its volume?" % (shape, A, l)
    e = "Volume of a prism = area of cross-section × length = %d × %d = <b>%s cm³</b>." % (A, l, num(V))
    return QN(q, V, [A + l, 2 * A + l, F(V, 2)], e, unit=" cm³")


# ------------------------------------------------------------ set 3: cylinders
def one_cyl(r):
    rad, h = r.randint(2, 10), r.randint(3, 20)
    use_d = r.random() < 0.4
    V = math.pi * rad * rad * h
    q = "Find the volume of the cylinder. Give your answer to 1 decimal place.%s" % fig(cyl_svg(rad, h, use_d))
    e = ("Radius = %d ÷ 2 = %d cm. " % (2 * rad, rad) if use_d else "") + "Volume = π<i>r</i>²<i>h</i> = π × %d² × %d = <b>%s cm³</b>." % (rad, h, d1(V))
    wrongs = [math.pi * (2 * rad) ** 2 * h if use_d else math.pi * rad * h, 2 * math.pi * rad * h, math.pi * rad * rad]
    right = d1(V) + " cm³"
    return mcq(q, (right, right), [(d1(w) + " cm³", d1(w)) for w in wrongs if d1(w) != d1(V)] + [(d1(V * 1.1) + " cm³", "a")], e)


# ------------------------------------------------------------ set 4: surface area
def one_sa(r):
    if r.random() < 0.6:
        l, w, h = r.randint(2, 12), r.randint(2, 9), r.randint(2, 10)
        if len({l, w, h}) < 3:
            return None
        SA = 2 * (l * w + w * h + l * h)
        q = "Find the surface area of the cuboid.%s" % fig(cuboid_svg(l, w, h))
        e = "Faces: 2 × (%d × %d) + 2 × (%d × %d) + 2 × (%d × %d) = %d + %d + %d = <b>%s cm²</b>." % (
            l, w, w, h, l, h, 2 * l * w, 2 * w * h, 2 * l * h, num(SA))
        return QN(q, SA, [l * w + w * h + l * h, l * w * h, 6 * l * w], e, unit=" cm²")
    b, h, l = r.choice([(3, 4, 10), (6, 8, 12), (5, 12, 10), (8, 6, 15), (9, 12, 20), (12, 5, 8)])
    hyp = int(round(math.hypot(b, h)))
    tri = b * h // 2
    SA = 2 * tri + (b + h + hyp) * l
    q = "Find the surface area of the triangular prism. The sloping side of the triangle is %d cm.%s" % (hyp, fig(tri_prism_svg(b, h, l)))
    e = "Two triangles: 2 × ½ × %d × %d = %d. Three rectangles: (%d + %d + %d) × %d = %d. Total <b>%s cm²</b>." % (
        b, h, 2 * tri, b, h, hyp, l, (b + h + hyp) * l, num(SA))
    return QN(q, SA, [tri + (b + h + hyp) * l, 2 * b * h + (b + h + hyp) * l, tri * l], e, unit=" cm²")


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    data = [
        ("How many cm³ are in 1 litre?", "1,000", ["100", "10", "10,000"], "1 litre = <b>1,000 cm³</b>."),
        ("A fish tank is 50 cm by 30 cm by 40 cm. How many litres of water does it hold when full?", "60 litres", ["600 litres", "6 litres", "120 litres"], "50 × 30 × 40 = 60,000 cm³ = <b>60 litres</b>."),
        ("A cube has a volume of 64 cm³. What is the length of each edge?", "4 cm", ["8 cm", "16 cm", "21.3 cm"], "4 × 4 × 4 = 64, so <b>4 cm</b>."),
        ("A cube has edges of 5 cm. What is its surface area?", "150 cm²", ["125 cm²", "25 cm²", "100 cm²"], "6 faces × 5 × 5 = <b>150 cm²</b>."),
        ("How many 1 cm cubes fit in a box 6 cm by 4 cm by 3 cm?", "72", ["13", "108", "24"], "6 × 4 × 3 = <b>72</b>."),
        ("How many cm³ are in 1 m³?", "1,000,000", ["100", "1,000", "10,000"], "1 m³ = 100 × 100 × 100 cm³ = <b>1,000,000 cm³</b>."),
        ("A cylindrical can has radius 4 cm and height 11 cm. About how many millilitres does it hold?", "553 ml", ["276 ml", "138 ml", "1,106 ml"], "π × 4² × 11 = 552.9 cm³, and 1 cm³ = 1 ml, so about <b>553 ml</b>."),
        ("A swimming pool is 25 m long, 10 m wide and 2 m deep. What is its volume?", "500 m³", ["37 m³", "250 m³", "5,000 m³"], "25 × 10 × 2 = <b>500 m³</b>."),
        ("A box is 20 cm by 10 cm by 5 cm. How many boxes like this fit in a crate 1 m by 40 cm by 20 cm?", "80", ["8", "800", "40"], "Crate 100 × 40 × 20 = 80,000 cm³. Box = 1,000 cm³. They stack exactly (5 × 4 × 4), so <b>80</b>."),
        ("If every edge of a cuboid is doubled, what happens to the volume?", "It is multiplied by 8", ["It doubles", "It is multiplied by 4", "It is multiplied by 6"], "2 × 2 × 2 = 8, so the volume is <b>multiplied by 8</b>."),
        ("A cuboid has a square base of side 5 cm and a volume of 150 cm³. What is its height?", "6 cm", ["30 cm", "10 cm", "3 cm"], "Base area 25 cm². 150 ÷ 25 = <b>6 cm</b>."),
        ("A water trough is a triangular prism. Its triangular end has area 600 cm² and it is 2 m long. How many litres does it hold?", "120 litres", ["1.2 litres", "1,200 litres", "12 litres"], "600 × 200 = 120,000 cm³ = <b>120 litres</b>."),
        ("Which units are used for volume?", "cm³ or m³", ["cm² or m²", "cm or m", "kg or g"], "Volume is measured in <b>cubic units</b>."),
        ("A cuboid is 10 cm by 4 cm by 2 cm. Which is larger, its volume in cm³ or its surface area in cm²?", "Its surface area (136) is larger than its volume (80)", ["Its volume is larger", "They are equal", "You cannot compare them"],
         "Volume = 80 cm³ and surface area = 2(40 + 8 + 20) = 136 cm². <b>Surface area</b> has the larger number (although the units are different)."),
        ("What is the volume of a prism with cross-section area 7.5 cm² and length 12 cm?", "90 cm³", ["19.5 cm³", "45 cm³", "900 cm³"], "7.5 × 12 = <b>90 cm³</b>."),
        ("A cylinder has volume 100π cm³ and radius 5 cm. What is its height?", "4 cm", ["20 cm", "10 cm", "2 cm"], "π × 25 × <i>h</i> = 100π, so <i>h</i> = <b>4 cm</b>."),
        ("Which net would fold to make a cube?", "Six squares in a cross shape", ["Five squares in a row", "Six squares in a 2 by 3 rectangle", "Four squares in a square"],
         "A cross of <b>six squares</b> folds into a cube; a 2 by 3 rectangle does not."),
        ("A tin of paint covers 12 m². A room's four walls are each 4 m long and 2.5 m high. How many tins are needed?", "4 tins", ["3 tins", "10 tins", "2 tins"], "4 × 4 × 2.5 = 40 m². 40 ÷ 12 = 3.33…, so <b>4 tins</b>."),
        ("A cuboid measures 3 cm by 4 cm by 5 cm. What is its volume?", "60 cm³", ["12 cm³", "94 cm³", "47 cm³"], "3 × 4 × 5 = <b>60 cm³</b>."),
        ("A cuboid measures 3 cm by 4 cm by 5 cm. What is its surface area?", "94 cm²", ["60 cm²", "47 cm²", "120 cm²"], "2(12 + 20 + 15) = 2 × 47 = <b>94 cm²</b>."),
    ]
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p>A <b>prism</b> has the same cross-section all the way through. <b>Volume = area of cross-section × length</b>. "
        "For a cuboid that is length × width × height; for a cylinder it is π<i>r</i>²<i>h</i>.</p>"
        "<p><b>Surface area</b> is the total area of all the faces. A cuboid has 6 faces in 3 matching pairs.</p>"
        "<p>1 cm³ = 1 ml, so 1,000 cm³ = 1 litre.</p>"
        + fig(cuboid_svg(5, 3, 4)),
        [("Find the volume and surface area of the cuboid above.", ["V = 5 × 3 × 4 = 60 cm³.", "SA = 2(15 + 12 + 20) = 94 cm²."], "60 cm³ and 94 cm²"),
         ("A triangular prism has a right-angled triangle 6 cm by 8 cm and length 10 cm. Find its volume.", ["Cross-section = ½ × 6 × 8 = 24 cm².", "24 × 10 = 240."], "240 cm³")],
        ["Adding the lengths instead of multiplying for volume.",
         "Forgetting to halve when the cross-section is a triangle.",
         "Counting only three faces of a cuboid for surface area (there are six).",
         "Using the diameter in π<i>r</i>²<i>h</i>, or thinking 100 cm³ = 1 litre."])


def main():
    sets = [S("Volume of cuboids", collect(one_cuboid, 20, R)),
            S("Volume of prisms", collect(one_prism, 20, R)),
            S("Volume of cylinders", collect(one_cyl, 20, R)),
            S("Surface area", collect(one_sa, 20, R)),
            S("Capacity and problems", problems())]
    make(8, "volume-and-surface-area-of-prisms", 12, "G",
         "Volume and Surface Area of Prisms and Cylinders",
         "Year 8 Volume and Surface Area Worksheets: Cuboids, Triangular Prisms, Cylinders and Capacity",
         "Volume and surface area",
         "Derive and apply formulae to calculate and solve problems involving: volume of cuboids (including cubes) and "
         "other prisms (including cylinders); calculate surface area of cuboids and other prisms.",
         "Free Year 8 volume and surface area worksheets with diagrams: cuboids, triangular prisms, cylinders, surface "
         "area and capacity in litres. 100 questions with answers.",
         "Volume of a prism = area of cross-section × length.",
         "Surface area = total area of all the faces. 1,000 cm³ = 1 litre.",
         body(),
         [("How do I find the volume of a prism?", "Find the area of the cross-section (the shape that runs all the way through) and multiply by the length."),
          ("What is the formula for the volume of a cylinder?", "V = πr²h: the area of the circle times the height."),
          ("How do I find the surface area of a cuboid?", "Find the area of the three different faces, add them, and double: 2(lw + wh + lh)."),
          ("How many cm³ are in a litre?", "1,000 cm³ = 1 litre, and 1 cm³ = 1 ml.")],
         sets, R)


if __name__ == "__main__":
    main()
