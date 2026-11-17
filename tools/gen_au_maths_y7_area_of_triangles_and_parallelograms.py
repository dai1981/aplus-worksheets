# -*- coding: utf-8 -*-
"""
AU Year 7 Maths: Area of triangles and parallelograms (Australian Curriculum v9.0: AC9M7M01)
  python3 tools/gen_au_maths_y7_area_of_triangles_and_parallelograms.py
Area of triangles and parallelograms from diagrams, finding a missing base or height, shapes made of a
rectangle and a triangle, units, and practical problems. Diagrams are inline SVG.
Wrong answers come from real mistakes: forgetting to halve for a triangle, using the slanted side instead of the
perpendicular height, adding instead of multiplying, and halving for a parallelogram.
"""
import random
from fractions import Fraction as F
from au_hs import num, mcq, B, S, make, lesson, collect, QN, T, svg_wrap, line, text, fig, GREEN, INK, RED, aud

R = random.Random(71301)
FILL = "#eef6f0"


def poly(pts, extra="", w=320, h=200, label="shape"):
    d = "M" + " L".join("%.1f %.1f" % p for p in pts) + " Z"
    return svg_wrap(w, h, "<path d='%s' fill='%s' stroke='%s' stroke-width='2.5'/>" % (d, FILL, INK) + extra, label)


def dash(x1, y1, x2, y2):
    return line(x1, y1, x2, y2, GREEN, 2, " stroke-dasharray='6 4'")


def rt(x, y, dx, dy, s=12):
    """Right-angle mark at (x,y) with arms along +dx and +dy (unit directions)."""
    return "<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f' fill='none' stroke='%s' stroke-width='1.8'/>" % (
        x + dx * s, y, x + dx * s, y + dy * s, x, y + dy * s, GREEN)


def lbl(x, y, t):
    return text(x, y, t, 15)


def rect_svg(l, w_, u="cm"):
    sc = min(220.0 / float(l), 120.0 / float(w_))
    W, H = max(float(l) * sc, 40), max(float(w_) * sc, 30)
    x0 = 40
    return poly([(x0, 30), (x0 + W, 30), (x0 + W, 30 + H), (x0, 30 + H)],
                lbl(x0 + W / 2, 30 + H + 24, "%s %s" % (num(l), u)) + lbl(x0 + W + 36, 30 + H / 2 + 5, "%s %s" % (num(w_), u)), 340, int(H + 70), "rectangle")


def tri_svg(b, h, slant=None, u="cm"):
    x0, y0, W, H = 40, 160, 240, 120
    apex = (x0 + W * 0.3, y0 - H)
    ex = lbl(x0 + W / 2, y0 + 24, "%s %s" % (num(b), u))
    ex += dash(apex[0], apex[1], apex[0], y0) + rt(apex[0], y0, 1, -1)
    ex += lbl(apex[0] + 26, y0 - H / 2, "%s %s" % (num(h), u))
    if slant:
        ex += lbl(x0 + W * 0.15 - 32, y0 - H / 2, "%s %s" % (num(slant), u))
    return poly([(x0, y0), (x0 + W, y0), apex], ex, 330, 200, "triangle")


def para_svg(b, h, slant=None, u="cm"):
    x0, y0, W, H, off = 40, 160, 200, 110, 60
    pts = [(x0, y0), (x0 + W, y0), (x0 + W + off, y0 - H), (x0 + off, y0 - H)]
    ex = lbl(x0 + W / 2, y0 + 24, "%s %s" % (num(b), u))
    ex += dash(x0 + off, y0 - H, x0 + off, y0) + rt(x0 + off, y0, 1, -1)
    ex += lbl(x0 + off + 30, y0 - H / 2 + 5, "%s %s" % (num(h), u))
    if slant:
        ex += lbl(x0 + W + off / 2 + 28, y0 - H / 2, "%s %s" % (num(slant), u))
    return poly(pts, ex, 340, 200, "parallelogram")



def house_svg(w, h, t, u="m"):
    """Rectangle w by h with a triangle of height t on top."""
    s = min(200.0 / w, 140.0 / (h + t))
    x0, y0 = 60, 30 + (h + t) * s
    W, Hh, T_ = w * s, h * s, t * s
    pts = [(x0, y0), (x0 + W, y0), (x0 + W, y0 - Hh), (x0 + W / 2, y0 - Hh - T_), (x0, y0 - Hh)]
    ex = line(x0, y0 - Hh, x0 + W, y0 - Hh, INK, 1.5, " stroke-dasharray='5 4'")
    ex += dash(x0 + W / 2, y0 - Hh - T_, x0 + W / 2, y0 - Hh)
    ex += line(x0 + W + 14, y0 - Hh - T_, x0 + W + 14, y0 - Hh, GREEN, 1.5) + line(x0 + W / 2 + 4, y0 - Hh - T_, x0 + W + 18, y0 - Hh - T_, GREEN, 1, " stroke-dasharray='3 3'")
    ex += text(x0 + W + 20, y0 - Hh - T_ / 2 + 5, "%s %s" % (num(t), u), 15, anchor="start")
    ex += lbl(x0 + W / 2, y0 + 22, "%s %s" % (num(w), u)) + lbl(x0 - 30, y0 - Hh / 2 + 5, "%s %s" % (num(h), u))
    return poly(pts, ex, 330, int(y0 + 34), "rectangle with a triangle on top")


# ------------------------------------------------------------ set 1: triangles
def one_tri(r):
    b, h = r.randint(4, 18), r.randint(3, 14)
    A = F(b * h, 2)
    slant = h + r.randint(1, 4)
    q = "Find the area of the triangle.%s" % fig(tri_svg(b, h, slant))
    e = "Area = ½ × base × perpendicular height = ½ × %d × %d = <b>%s cm²</b>. Do not use the slanted side." % (b, h, num(A))
    return QN(q, A, [b * h, F(b * slant, 2), b + h + slant], e, unit=" cm²")


# ------------------------------------------------------------ set 2: parallelograms
def one_para(r):
    b, h = r.randint(5, 18), r.randint(3, 12)
    sl = h + r.randint(1, 3)
    A = b * h
    q = "Find the area of the parallelogram.%s" % fig(para_svg(b, h, sl))
    e = "Area = base × perpendicular height = %d × %d = <b>%d cm²</b>. The slanted side is not used." % (b, h, A)
    return QN(q, A, [b * sl, F(b * h, 2), 2 * (b + sl)], e, unit=" cm²")


# ------------------------------------------------------------ set 3: missing base or height
def one_missing(r):
    shape = r.choice(["triangle", "parallelogram", "triangle"])
    b, h = r.randint(4, 20), r.randint(3, 15)
    if shape == "triangle":
        if (b * h) % 2:
            return None
        A = b * h // 2
        if r.random() < 0.5:
            q = "A triangle has an area of %d cm² and a base of %d cm. What is its perpendicular height?" % (A, b)
            return QN(q, h, [F(A, b) if F(A, b) != h else h * 2, A * 2 // b * 2 if A * 2 // b * 2 != h else h + 1, A - b if A > b else h + 3],
                      "½ × %d × <i>h</i> = %d, so %s<i>h</i> = %d and <i>h</i> = <b>%d cm</b>." % (b, A, num(F(b, 2)), A, h), unit=" cm")
        q = "A triangle has an area of %d cm² and a perpendicular height of %d cm. What is its base?" % (A, h)
        return QN(q, b, [F(A, h) if F(A, h) != b else b * 2, A - h if A > h else b + 3, b * 2], "½ × <i>b</i> × %d = %d, so <i>b</i> = %d × 2 ÷ %d = <b>%d cm</b>." % (h, A, A, h, b), unit=" cm")
    A = b * h
    q = "A parallelogram has an area of %d cm² and a base of %d cm. What is its perpendicular height?" % (A, b)
    return QN(q, h, [h * 2, A - b, F(A, 2 * b) if F(A, 2 * b).denominator <= 2 else h + 2], "%d × <i>h</i> = %d, so <i>h</i> = %d ÷ %d = <b>%d cm</b>." % (b, A, A, b, h), unit=" cm")


# ------------------------------------------------------------ set 4: shapes made of a rectangle and a triangle
def one_house(r):
    w = r.choice([4, 6, 8, 10, 12])
    h, t = r.randint(3, 9), r.randint(2, 6)
    rect = w * h
    tri = F(w * t, 2)
    A = rect + tri
    q = "The end wall of a shed is a rectangle with a triangle on top. Find its area.%s" % fig(house_svg(w, h, t))
    e = "Rectangle: %d × %d = %d m². Triangle: ½ × %d × %d = %s m². Total = <b>%s m²</b>." % (w, h, rect, w, t, num(tri), num(A))
    return QN(q, A, [rect + w * t, w * (h + t), rect], e, unit=" m²")


# ------------------------------------------------------------ set 5: problems
def problems():
    data = [
        ("A triangular sail has a base of 3 m and a perpendicular height of 5 m. What is its area?", "7.5 m²", ["15 m²", "8 m²", "4 m²"], "½ × 3 × 5 = <b>7.5 m²</b>."),
        ("A garden bed is a parallelogram with base 6 m and perpendicular height 2.5 m. What is its area?", "15 m²", ["7.5 m²", "17 m²", "8.5 m²"], "6 × 2.5 = <b>15 m²</b>."),
        ("A triangle and a parallelogram have the same base and the same perpendicular height. How do their areas compare?", "The triangle is half the parallelogram", ["They are equal", "The triangle is double", "You cannot tell"],
         "Triangle: ½ × <i>b</i> × <i>h</i>. Parallelogram: <i>b</i> × <i>h</i>. <b>The triangle is half the parallelogram.</b>"),
        ("A road sign is a triangle with base 90 cm and perpendicular height 78 cm. What is its area?", "3510 cm²", ["7020 cm²", "168 cm²", "3600 cm²"], "½ × 90 × 78 = <b>3510 cm²</b>."),
        ("Turf costs $12 per m². A triangular lawn has base 10 m and perpendicular height 7 m. What does the turf cost?", "$420", ["$840", "$204", "$35"], "Area = ½ × 10 × 7 = 35 m². 35 × $12 = <b>$420</b>."),
        ("A parallelogram has sides 8 cm and 5 cm and a perpendicular height of 4 cm (to the 8 cm base). What is its area?", "32 cm²", ["40 cm²", "20 cm²", "26 cm²"], "Area = base × perpendicular height = 8 × 4 = <b>32 cm²</b>. The 5 cm side is not used."),
        ("A right-angled triangle has shorter sides of 6 cm and 8 cm. What is its area?", "24 cm²", ["48 cm²", "14 cm²", "28 cm²"], "The two shorter sides are at right angles, so they are the base and height: ½ × 6 × 8 = <b>24 cm²</b>."),
        ("Which units are used for area?", "cm², m² or km²", ["cm, m or km", "cm³ or m³", "litres"], "Area is measured in <b>square units</b> such as cm² and m²."),
        ("How many cm² are in 1 m²?", "10 000", ["100", "1000", "1 000 000"], "1 m² = 100 cm × 100 cm = <b>10 000 cm²</b>."),
        ("A triangle has area 18 cm². Which could be its base and perpendicular height?", "9 cm and 4 cm", ["9 cm and 2 cm", "6 cm and 3 cm", "18 cm and 2 cm"], "½ × 9 × 4 = <b>18</b>. The others give 9, 9 and 18… check: ½ × 18 × 2 = 18 too."),
        ("A rhombus-shaped tile is a parallelogram with base 15 cm and perpendicular height 12 cm. How many tiles cover 1.8 m²?", "100", ["10", "1000", "50"], "Tile area = 15 × 12 = 180 cm². 1.8 m² = 18 000 cm². 18 000 ÷ 180 = <b>100</b>."),
        ("A triangular flag has area 0.6 m² and base 1.2 m. What is its perpendicular height?", "1 m", ["0.5 m", "2 m", "0.72 m"], "½ × 1.2 × <i>h</i> = 0.6, so 0.6<i>h</i> = 0.6 and <i>h</i> = <b>1 m</b>."),
        ("A parallelogram is cut along its height and the triangle moved to the other end. What shape does it make?", "A rectangle with the same area", ["A triangle with half the area", "A square with double the area", "A trapezium with a bigger area"],
         "The pieces make <b>a rectangle with the same area</b>: base × height. That is why parallelogram area = base × height."),
        ("Two triangles each have base 10 cm. One has height 4 cm and the other 6 cm. What is their total area?", "50 cm²", ["100 cm²", "30 cm²", "24 cm²"], "20 + 30 = <b>50 cm²</b>."),
        ("A kite is made of two triangles, each with base 40 cm and height 25 cm. What is its area?", "1000 cm²", ["500 cm²", "2000 cm²", "130 cm²"], "Each triangle: ½ × 40 × 25 = 500 cm². Two: <b>1000 cm²</b>."),
        ("Paint covers 8 m² per litre. A triangular gable has base 8 m and height 3 m. How many litres are needed?", "1.5 L", ["3 L", "12 L", "24 L"], "Area = ½ × 8 × 3 = 12 m². 12 ÷ 8 = <b>1.5 L</b>."),
        ("A triangle has base 2<i>b</i> and height <i>h</i>. Which expression gives its area?", "<i>bh</i>", ["2<i>bh</i>", "½<i>bh</i>", "<i>b</i> + <i>h</i>"], "½ × 2<i>b</i> × <i>h</i> = <b><i>bh</i></b>."),
        ("A parallelogram has area 54 m² and perpendicular height 6 m. What is its base?", "9 m", ["18 m", "48 m", "324 m"], "54 ÷ 6 = <b>9 m</b>."),
        ("A school vegie patch is a triangle with base 12 m and height 5 m. Each square metre needs 4 seedlings. How many seedlings?", "120", ["240", "60", "68"], "Area = ½ × 12 × 5 = 30 m². 30 × 4 = <b>120</b>."),
        ("Which measurement is NOT needed to find the area of a triangle?", "The length of a slanted side", ["The base", "The perpendicular height", "The units"], "Area = ½ × base × perpendicular height, so <b>the slanted side is not needed</b>."),
    ]
    data[9] = ("A triangle has area 18 cm². Which could be its base and perpendicular height?", "9 cm and 4 cm", ["9 cm and 2 cm", "6 cm and 3 cm", "4 cm and 4.5 cm"],
               "½ × 9 × 4 = <b>18 cm²</b>. The others give 9, 9 and 9 cm².")
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>A <b>parallelogram</b> can be cut and rearranged into a rectangle, so its area = <b>base × perpendicular height</b>.</p>"
        "<p>A <b>triangle</b> is half of a parallelogram with the same base and height, so its area = <b>½ × base × perpendicular height</b>.</p>"
        "<p>The height must be <b>perpendicular</b> (at right angles) to the base. Slanted sides are not used for area.</p>"
        + fig(tri_svg(10, 6, 7)),
        [("Find the area of a triangle with base 10 cm and perpendicular height 6 cm.", ["½ × 10 × 6 = 30."], "30 cm²"),
         ("Find the area of a parallelogram with base 9 cm, slanted side 5 cm and height 4 cm.", ["9 × 4 = 36. Do not use the 5 cm."], "36 cm²"),
         ("A triangle has area 24 cm² and base 8 cm. Find its height.", ["½ × 8 × <i>h</i> = 24, so 4<i>h</i> = 24."], "6 cm")],
        ["Forgetting to halve for a triangle: base × height gives double the area.",
         "Halving for a parallelogram. Only triangles have the ½.",
         "Using the slanted side instead of the perpendicular height.",
         "Writing cm instead of cm² for an area."])


def main():
    sets = [S("Area of triangles", collect(one_tri, 20, R)),
            S("Area of parallelograms", collect(one_para, 20, R)),
            S("Finding a missing base or height", collect(one_missing, 20, R)),
            S("Rectangles and triangles together", collect(one_house, 20, R)),
            S("Area problems", problems())]
    make(7, "area-of-triangles-and-parallelograms", 13, "AC9M7M01",
         "Area of Triangles and Parallelograms",
         "Year 7 Area of Triangles and Parallelograms Worksheets: Base × Height and Missing Lengths (Free, Answer Key)",
         "Area of triangles and parallelograms",
         "solve problems involving the area of triangles and parallelograms using established formulas and appropriate units",
         "Free Year 7 maths worksheets on the area of triangles and parallelograms for the Australian Curriculum (AC9M7M01): "
         "diagrams, missing base or height, composite shapes and practical problems. 100 questions with an answer key.",
         "Parallelogram area = base × height. Triangle area = ½ × base × height.",
         "Always use the perpendicular height, not the slanted side.",
         body(),
         [("What is the formula for the area of a triangle?", "Area = ½ × base × perpendicular height."),
          ("What is the formula for the area of a parallelogram?", "Area = base × perpendicular height. It is a rectangle that has been pushed over."),
          ("Why is a triangle half of a parallelogram?", "Two identical triangles fit together to make a parallelogram with the same base and height."),
          ("How do I find the height if I know the area?", "Work backwards. For a triangle with area 24 cm² and base 8 cm: ½ × 8 × h = 24, so h = 6 cm.")],
         sets, R)


if __name__ == "__main__":
    main()
