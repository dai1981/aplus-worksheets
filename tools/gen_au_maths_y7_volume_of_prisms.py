# -*- coding: utf-8 -*-
"""
AU Year 7 Maths: Volume of prisms (Australian Curriculum v9.0: AC9M7M02)
  python3 tools/gen_au_maths_y7_volume_of_prisms.py
Volume of rectangular prisms, finding a missing dimension, volume of triangular prisms, volume from the area
of the cross-section, and practical problems. Diagrams are inline SVG.
Wrong answers come from real mistakes: adding the dimensions, forgetting to halve the triangle, using the
surface area, and mixing cm² and cm³.
"""
import random
from fractions import Fraction as F
from au_hs import num, mcq, B, S, make, lesson, collect, QN, T, svg_wrap, line, text, fig, INK, RED, GREEN

R = random.Random(71401)


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


# ------------------------------------------------------------ set 1: rectangular prisms
def one_cuboid(r):
    l, w, h = r.randint(2, 16), r.randint(2, 10), r.randint(2, 12)
    if len({l, w, h}) < 3:
        return None
    V = l * w * h
    q = "Find the volume of the rectangular prism.%s" % fig(cuboid_svg(l, w, h))
    e = "Volume = length × width × height = %d × %d × %d = <b>%s cm³</b>." % (l, w, h, num(V))
    return QN(q, V, [l + w + h, 2 * (l * w + w * h + l * h), l * w], e, unit=" cm³")


# ------------------------------------------------------------ set 2: missing dimension
def one_missing(r):
    l, w, h = r.randint(2, 15), r.randint(2, 10), r.randint(2, 12)
    if len({l, w, h}) < 3:
        return None
    V = l * w * h
    if r.random() < 0.6:
        q = "A rectangular prism has a volume of %s cm³. It is %d cm long and %d cm wide. How high is it?" % (num(V), l, w)
        e = "Height = %s ÷ (%d × %d) = %s ÷ %d = <b>%d cm</b>." % (num(V), l, w, num(V), l * w, h)
        return QN(q, h, [V - l - w, F(V, l + w) if F(V, l + w).denominator == 1 else V // l, l * w], e, unit=" cm")
    A = l * w
    q = "A rectangular prism has a base area of %d cm² and a volume of %s cm³. How high is it?" % (A, num(V))
    e = "Volume = base area × height, so height = %s ÷ %d = <b>%d cm</b>." % (num(V), A, h)
    return QN(q, h, [V - A, F(V, 2 * A) if F(V, 2 * A).denominator == 1 else h * 2, A], e, unit=" cm")


# ------------------------------------------------------------ set 3: triangular prisms
def one_tri(r):
    b, h, l = r.randint(3, 12), r.randint(2, 10), r.randint(4, 20)
    A = F(b * h, 2)
    V = A * l
    q = "Find the volume of the triangular prism. The triangle has a right angle.%s" % fig(tri_prism_svg(b, h, l))
    e = "Area of the triangular end = ½ × %d × %d = %s cm². Volume = %s × %d = <b>%s cm³</b>." % (b, h, num(A), num(A), l, num(V))
    return QN(q, V, [b * h * l, A + l, b * h + l], e, unit=" cm³")


# ------------------------------------------------------------ set 4: area of cross-section × length
def one_cross(r):
    A = r.choice([6, 8, 12, 15, 18, 20, 24, 30, 36, 45, F(15, 2), F(25, 2)])
    l = r.randint(3, 15)
    V = A * l
    shape = r.choice(["an L-shaped", "a trapezium-shaped", "a hexagonal", "a triangular", "a T-shaped"])
    if r.random() < 0.7:
        q = "A right prism has %s cross-section with area %s cm². It is %d cm long. What is its volume?" % (shape, num(A), l)
        e = "Volume of a prism = area of cross-section × length = %s × %d = <b>%s cm³</b>." % (num(A), l, num(V))
        return QN(q, V, [A + l, 2 * A + l, V / 2], e, unit=" cm³")
    q = "A right prism has %s cross-section and a volume of %s cm³. It is %d cm long. What is the area of the cross-section?" % (shape, num(V), l)
    e = "Area = volume ÷ length = %s ÷ %d = <b>%s cm²</b>." % (num(V), l, num(A))
    return mcq(q, (num(A) + " cm²", A), [(num(w) + " cm²", w) for w in [V - l, V * l, A * 2, A + l] if w != A], e)


# ------------------------------------------------------------ set 5: problems
def problems():
    data = [
        ("How many 1 cm cubes fit in a box 7 cm by 4 cm by 3 cm?", "84", ["14", "122", "28"], "7 × 4 × 3 = <b>84</b>."),
        ("A cube has edges of 6 cm. What is its volume?", "216 cm³", ["36 cm³", "18 cm³", "216 cm²"], "6 × 6 × 6 = <b>216 cm³</b>."),
        ("A cube has a volume of 125 cm³. How long is each edge?", "5 cm", ["25 cm", "41.7 cm", "11 cm"], "5 × 5 × 5 = 125, so <b>5 cm</b>."),
        ("A sandpit is 3 m by 2 m and is filled with sand 0.5 m deep. What volume of sand is needed?", "3 m³", ["6 m³", "5.5 m³", "30 m³"], "3 × 2 × 0.5 = <b>3 m³</b>."),
        ("A shipping container is 6 m long, 2.4 m wide and 2.5 m high. What is its volume?", "36 m³", ["10.9 m³", "14.4 m³", "360 m³"], "6 × 2.4 × 2.5 = <b>36 m³</b>."),
        ("A tent is a triangular prism. The triangular end has base 2 m and height 1.5 m. The tent is 3 m long. What is its volume?", "4.5 m³", ["9 m³", "6.5 m³", "3 m³"],
         "End area = ½ × 2 × 1.5 = 1.5 m². Volume = 1.5 × 3 = <b>4.5 m³</b>."),
        ("A chocolate bar is a triangular prism. The triangle has base 3 cm and height 2.5 cm and the bar is 20 cm long. What is its volume?", "75 cm³", ["150 cm³", "25.5 cm³", "60 cm³"],
         "½ × 3 × 2.5 = 3.75 cm². 3.75 × 20 = <b>75 cm³</b>."),
        ("If every edge of a rectangular prism is doubled, what happens to the volume?", "It is multiplied by 8", ["It doubles", "It is multiplied by 4", "It is multiplied by 6"], "2 × 2 × 2 = 8, so the volume is <b>multiplied by 8</b>."),
        ("A rectangular prism has a square base of side 4 cm and a volume of 112 cm³. How high is it?", "7 cm", ["28 cm", "14 cm", "104 cm"], "Base area = 16 cm². 112 ÷ 16 = <b>7 cm</b>."),
        ("Which units are used for volume?", "cm³ or m³", ["cm² or m²", "cm or m", "kg or g"], "Volume is measured in <b>cubic units</b>."),
        ("Which two prisms have the same volume?", "2 × 3 × 10 and 5 × 4 × 3", ["2 × 3 × 10 and 5 × 5 × 2", "4 × 4 × 4 and 8 × 8 × 1", "6 × 1 × 1 and 3 × 3 × 3"],
         "2 × 3 × 10 = 60 and 5 × 4 × 3 = 60, so <b>2 × 3 × 10 and 5 × 4 × 3</b>."),
        ("A box is 20 cm by 10 cm by 10 cm. How many boxes fit in a carton 40 cm by 40 cm by 20 cm?", "16", ["8", "32", "4"], "Along each edge: 2 × 4 × 2 = <b>16</b> boxes."),
        ("A concrete path is 10 m long, 1.2 m wide and 0.1 m thick. What volume of concrete is needed?", "1.2 m³", ["12 m³", "11.3 m³", "0.12 m³"], "10 × 1.2 × 0.1 = <b>1.2 m³</b>."),
        ("A water trough is a triangular prism. Its end has area 0.3 m² and it is 2 m long. What is its volume?", "0.6 m³", ["2.3 m³", "0.15 m³", "6 m³"], "0.3 × 2 = <b>0.6 m³</b>."),
        ("A rectangular prism is 8 cm by 5 cm by 3 cm. What is its volume?", "120 cm³", ["16 cm³", "158 cm³", "40 cm³"], "8 × 5 × 3 = <b>120 cm³</b>."),
        ("A ramp is a triangular prism. The triangular side has base 120 cm and height 30 cm. The ramp is 80 cm wide. What is its volume?", "144 000 cm³", ["288 000 cm³", "3600 cm³", "230 cm³"],
         "½ × 120 × 30 = 1800 cm². 1800 × 80 = <b>144 000 cm³</b>."),
        ("Which is the formula for the volume of any right prism?", "Area of cross-section × length", ["Length + width + height", "Perimeter × height", "½ × base × height"],
         "<b>Volume = area of cross-section × length</b>."),
        ("A cubby house floor is 2 m by 1.5 m and the room is 1.8 m high. What volume of air is inside?", "5.4 m³", ["5.3 m³", "3 m³", "10.8 m³"], "2 × 1.5 × 1.8 = <b>5.4 m³</b>."),
        ("How many 2 cm cubes fit in a box 6 cm by 4 cm by 2 cm?", "6", ["48", "24", "12"], "Along the edges: 3 × 2 × 1 = <b>6</b> cubes. (48 counts 1 cm cubes.)"),
        ("A prism's cross-section is a triangle with area 18 cm². The prism is 10 cm long. What is its volume?", "180 cm³", ["90 cm³", "28 cm³", "360 cm³"], "18 × 10 = <b>180 cm³</b>. The ½ is already in the 18 cm²."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>A <b>right prism</b> has the same cross-section all the way through. <b>Volume = area of cross-section × length</b>.</p>"
        "<p>For a rectangular prism this is length × width × height. For a triangular prism, first find the area of the "
        "triangle (½ × base × height), then multiply by the length. Volume is measured in cubic units such as cm³ and m³.</p>"
        + fig(cuboid_svg(5, 3, 4)),
        [("Find the volume of the rectangular prism above.", ["5 × 3 × 4."], "60 cm³"),
         ("A triangular prism has a right-angled triangle 6 cm by 8 cm and length 10 cm.", ["Triangle area = ½ × 6 × 8 = 24 cm².", "24 × 10 = 240."], "240 cm³")],
        ["Adding the lengths instead of multiplying.",
         "Forgetting to halve when the cross-section is a triangle.",
         "Halving twice when the cross-section area is already given.",
         "Writing cm² instead of cm³ for a volume."])


def main():
    sets = [S("Volume of rectangular prisms", collect(one_cuboid, 20, R)),
            S("Finding a missing dimension", collect(one_missing, 20, R)),
            S("Volume of triangular prisms", collect(one_tri, 20, R)),
            S("Cross-section × length", collect(one_cross, 20, R)),
            S("Volume problems", problems())]
    make(7, "volume-of-prisms", 14, "AC9M7M02",
         "Volume of Prisms: Rectangular and Triangular Prisms",
         "Year 7 Volume of Prisms Worksheets: Rectangular and Triangular Prisms (Free, Answer Key)",
         "Volume of prisms",
         "solve problems involving the volume of right prisms including rectangular and triangular prisms, using established formulas and appropriate units",
         "Free Year 7 maths worksheets on the volume of prisms for the Australian Curriculum (AC9M7M02): rectangular prisms, "
         "missing dimensions, triangular prisms, area of cross-section × length and practical problems. 100 questions with an answer key.",
         "Volume of a prism = area of cross-section × length.",
         "For a triangular prism, find the triangle's area first (½ × base × height).",
         body(),
         [("How do I find the volume of a rectangular prism?", "Multiply length × width × height. A 5 cm by 3 cm by 4 cm prism has volume 60 cm³."),
          ("How do I find the volume of a triangular prism?", "Find the area of the triangular end (½ × base × height), then multiply by the length of the prism."),
          ("What is a right prism?", "A 3-D shape with the same cross-section all the way through, whose sides meet the ends at right angles."),
          ("How do I find a missing height?", "Divide the volume by the area of the base. 112 cm³ ÷ 16 cm² = 7 cm.")],
         sets, R)


if __name__ == "__main__":
    main()
