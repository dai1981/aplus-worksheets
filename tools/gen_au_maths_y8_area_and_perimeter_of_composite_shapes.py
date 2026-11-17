# -*- coding: utf-8 -*-
"""
AU Year 8 Maths: Area and Perimeter of Composite Shapes (Australian Curriculum v9.0: AC9M8M01)
  python3 tools/gen_au_maths_y8_area_and_perimeter_of_composite_shapes.py
Area of trapeziums, rhombuses and kites; perimeter and area of L-shaped composite shapes; shapes with a piece
removed (borders and paths); and problems. Diagrams are inline SVG.
Wrong answers come from real mistakes: forgetting to halve, using a slanted side instead of the perpendicular
height, missing a side of an L-shape, and adding the hole instead of taking it away.
"""
import random
from fractions import Fraction as F
from au_hs import num, mcq, B, S, make, lesson, collect, QN, T, svg_wrap, line, text, fig, GREEN, INK, RED, aud

R = random.Random(80901)
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


def trap_svg(a, b, h, u="cm"):
    x0, y0, W, H = 40, 160, 240, 110
    top = W * float(a) / float(b)
    left = (W - top) * 0.4
    pts = [(x0, y0), (x0 + W, y0), (x0 + left + top, y0 - H), (x0 + left, y0 - H)]
    ex = lbl(x0 + W / 2, y0 + 24, "%s %s" % (num(b), u)) + lbl(x0 + left + top / 2, y0 - H - 10, "%s %s" % (num(a), u))
    ex += dash(x0 + left, y0 - H, x0 + left, y0) + rt(x0 + left, y0, 1, -1) + lbl(x0 + left + 30, y0 - H / 2 + 5, "%s %s" % (num(h), u))
    return poly(pts, ex, 330, 200, "trapezium")


def l_svg(W_, H_, cw, ch, labels):
    """L-shape: full W_ x H_ with a cw x ch rectangle cut from the top-right. labels: dict side->text."""
    sx = 240.0 / W_
    sy = 145.0 / H_
    s = min(sx, sy)
    x0, y0 = 50, 170
    Wp, Hp, cwp, chp = W_ * s, H_ * s, cw * s, ch * s
    pts = [(x0, y0), (x0 + Wp, y0), (x0 + Wp, y0 - (Hp - chp)), (x0 + Wp - cwp, y0 - (Hp - chp)), (x0 + Wp - cwp, y0 - Hp), (x0, y0 - Hp)]
    ex = ""
    ex += lbl(x0 + Wp / 2, y0 + 22, labels.get("bottom", ""))
    ex += lbl(x0 - 28, y0 - Hp / 2 + 5, labels.get("left", ""))
    ex += lbl(x0 + (Wp - cwp) / 2, y0 - Hp - 8, labels.get("top", ""))
    ex += lbl(x0 + Wp + 28, y0 - (Hp - chp) / 2 + 5, labels.get("right", ""))
    ex += lbl(x0 + Wp - cwp / 2, y0 - (Hp - chp) - 8, labels.get("step_h", ""))
    ex += text(x0 + Wp - cwp + 6, y0 - Hp + chp * 0.35 + 5, labels.get("step_v", ""), 15, anchor="start")
    return poly(pts, ex, 340, 200, "compound shape made of rectangles")


# ------------------------------------------------------------ set 1: trapeziums, rhombuses and kites
def one_trap(r):
    a, b = r.randint(3, 12), r.randint(6, 18)
    if a >= b:
        return None
    h = r.randint(2, 11)
    A = F((a + b) * h, 2)
    if r.random() < 0.3:
        u = "m"
    else:
        u = "cm"
    q = "Find the area of the trapezium.%s" % fig(trap_svg(a, b, h, u))
    e = "Area = ½(<i>a</i> + <i>b</i>)<i>h</i> = ½ × (%d + %d) × %d = <b>%s %s²</b>." % (a, b, h, num(A), u)
    return QN(q, A, [(a + b) * h, F(a * b, 2) if a * b != (a + b) * h // 2 else a * h, F(a * h, 2) + b], e, unit=" %s²" % u)


def one_kite(r):
    p, q_ = r.randint(4, 16), r.randint(3, 14)
    if p == q_:
        return None
    shape = r.choice(["rhombus", "kite"])
    A = F(p * q_, 2)
    q = "A %s has diagonals of %d cm and %d cm. What is its area?" % (shape, p, q_)
    e = "The area of a %s is half the product of its diagonals: ½ × %d × %d = <b>%s cm²</b>." % (shape, p, q_, num(A))
    return QN(q, A, [p * q_, p + q_, 2 * (p + q_)], e, unit=" cm²")


# ------------------------------------------------------------ set 2: perimeter
def one_per(r):
    kind = r.choice([1, 3, 3, 3])
    if kind == 0:
        l, w_ = r.randint(4, 20), r.randint(2, 15)
        if l == w_:
            return None
        P = 2 * (l + w_)
        q = "Find the perimeter of the rectangle.%s" % fig(rect_svg(l, w_))
        return QN(q, P, [l * w_, l + w_, 2 * l + w_], "Perimeter = %d + %d + %d + %d = <b>%d cm</b>." % (l, w_, l, w_, P), unit=" cm")
    if kind == 1:
        w_ = r.randint(2, 12)
        l = r.randint(w_ + 1, 20)
        P = 2 * (l + w_)
        q = "A rectangle has a perimeter of %d cm and a length of %d cm. What is its width?" % (P, l)
        return QN(q, w_, [P - l, P // 2, F(P, l) if P % l == 0 else P - 2 * l], "2 × %d = %d. %d − %d = %d for the two widths, so each width is <b>%d cm</b>." % (l, 2 * l, P, 2 * l, 2 * w_, w_), unit=" cm")
    if kind == 2:
        s = r.randint(3, 15)
        n, name = r.choice([(3, "equilateral triangle"), (4, "square"), (5, "regular pentagon"), (6, "regular hexagon"), (8, "regular octagon")])
        if r.random() < 0.5:
            q = "A %s has sides of %d cm. What is its perimeter?" % (name, s)
            return QN(q, n * s, [s * s, (n - 1) * s, n + s], "%d sides × %d cm = <b>%d cm</b>." % (n, s, n * s), unit=" cm")
        q = "A %s has a perimeter of %d cm. How long is each side?" % (name, n * s)
        return QN(q, s, [n * s - n, F(n * s, n - 1) if (n * s) % (n - 1) == 0 else s + 2, n * s * n if n * s * n < 200 else s * 2], "%d ÷ %d = <b>%d cm</b>." % (n * s, n, s), unit=" cm")
    W_, H_ = r.randint(8, 16), r.randint(6, 12)
    cw, ch = r.randint(2, W_ - 3), r.randint(2, H_ - 2)
    if cw < 0.3 * W_ or ch < 0.3 * H_ or W_ - cw < 0.3 * W_ or H_ - ch < 0.3 * H_:
        return None
    P = 2 * (W_ + H_)
    labels = {"bottom": "%d cm" % W_, "left": "%d cm" % H_, "top": "%d cm" % (W_ - cw), "right": "%d cm" % (H_ - ch),
              "step_h": "%d cm" % cw, "step_v": "%d cm" % ch}
    q = "Find the perimeter of the shape. All corners are right angles.%s" % fig(l_svg(W_, H_, cw, ch, labels))
    e = "Add all six sides: %d + %d + %d + %d + %d + %d = <b>%d cm</b>. (It is the same as the rectangle around it.)" % (
        W_, H_ - ch, cw, ch, W_ - cw, H_, P)
    return QN(q, P, [W_ * H_ - cw * ch, P - cw - ch, W_ + H_], e, unit=" cm")


# ------------------------------------------------------------ set 3: composite area
def one_comp(r):
    W_, H_ = r.randint(8, 16), r.randint(6, 12)
    cw, ch = r.randint(2, W_ - 3), r.randint(2, H_ - 2)
    if cw < 0.3 * W_ or ch < 0.3 * H_ or W_ - cw < 0.3 * W_ or H_ - ch < 0.3 * H_:
        return None
    A = W_ * H_ - cw * ch
    hide = r.choice([[], ["right"], ["top"]])
    labels = {"bottom": "%d cm" % W_, "left": "%d cm" % H_, "top": "%d cm" % (W_ - cw), "right": "%d cm" % (H_ - ch),
              "step_h": "%d cm" % cw, "step_v": "%d cm" % ch}
    for k in hide:
        labels[k] = ""
    q = "Find the area of the shape. All corners are right angles.%s" % fig(l_svg(W_, H_, cw, ch, labels))
    e = "Big rectangle %d × %d = %d, take away the missing corner %d × %d = %d: <b>%d cm²</b>." % (W_, H_, W_ * H_, cw, ch, cw * ch, A)
    return QN(q, A, [W_ * H_, 2 * (W_ + H_), W_ * H_ - cw - ch], e, unit=" cm²")


# ------------------------------------------------------------ set 4: shapes with a piece removed
def one_hole(r):
    kind = r.choice(["path", "bed", "frame", "pool"])
    if kind == "path":
        L, W, w = r.randint(8, 20), r.randint(5, 12), r.choice([1, 1, 2])
        if W >= L:
            return None
        A = (L + 2 * w) * (W + 2 * w) - L * W
        q = "A path %d m wide goes all the way round a rectangular lawn %d m by %d m. What is the area of the path?" % (w, L, W)
        e = "Outside rectangle: %d × %d = %d m². Lawn: %d × %d = %d m². Path = <b>%d m²</b>." % (L + 2 * w, W + 2 * w, (L + 2 * w) * (W + 2 * w), L, W, L * W, A)
        return QN(q, A, [(L + w) * (W + w) - L * W, 2 * (L + W) * w, (L + 2 * w) * (W + 2 * w)], e, unit=" m²")
    if kind == "bed":
        L, W = r.randint(10, 25), r.randint(6, 15)
        a, b = r.randint(2, L // 2), r.randint(1, W // 2)
        A = L * W - a * b
        q = "A rectangular backyard is %d m by %d m. A garden bed %d m by %d m is dug in it. The rest is lawn. What is the area of the lawn?" % (L, W, a, b)
        e = "Backyard %d × %d = %d m². Garden bed %d × %d = %d m². Lawn = <b>%d m²</b>." % (L, W, L * W, a, b, a * b, A)
        return QN(q, A, [L * W + a * b, L * W, (L - a) * (W - b)], e, unit=" m²")
    if kind == "frame":
        L, W, w = r.choice([20, 25, 30, 40]), r.choice([15, 20, 25]), r.choice([2, 3, 4, 5])
        if W >= L:
            return None
        A = L * W - (L - 2 * w) * (W - 2 * w)
        q = "A picture frame is %d cm by %d cm on the outside. The wood is %d cm wide all round. What is the area of the wood?" % (L, W, w)
        e = "Outside %d × %d = %d cm². Inside (%d − %d) × (%d − %d) = %d × %d = %d cm². Wood = <b>%d cm²</b>." % (
            L, W, L * W, L, 2 * w, W, 2 * w, L - 2 * w, W - 2 * w, (L - 2 * w) * (W - 2 * w), A)
        return QN(q, A, [L * W - (L - w) * (W - w), (L - 2 * w) * (W - 2 * w), 2 * (L + W) * w], e, unit=" cm²")
    L, W = r.randint(12, 25), r.randint(8, 15)
    a, b = r.randint(4, L - 4), r.randint(2, W - 3)
    q = "A rectangular courtyard is %d m by %d m. A pool %d m by %d m is built in it and the rest is paved. Pavers cost $50 per m². How much do the pavers cost?" % (L, W, a, b)
    A = L * W - a * b
    e = "Paved area = %d × %d − %d × %d = %d m². Cost = %d × $50 = <b>%s</b>." % (L, W, a, b, A, A, aud(A * 50))
    return QN(q, A * 50, [L * W * 50, a * b * 50, A * 5], e, fmt=aud, near=(50, -50, 100))


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    data = [
        ("A backyard is 12 m by 8 m. Turf costs $4 per m². How much does it cost to turf the whole backyard?", 384, [160, 80, 96], "Area = 12 × 8 = 96 m². Cost = 96 × $4 = <b>$384</b>.", "$"),
        ("A paddock is 50 m by 30 m. A fence goes all the way round it. How long is the fence?", 160, [1500, 80, 130], "Perimeter = 2 × (50 + 30) = <b>160 m</b>.", " m"),
        ("A square has an area of 64 cm². What is its perimeter?", 32, [16, 256, 8], "Side = √64 = 8 cm, so perimeter = 4 × 8 = <b>32 cm</b>.", " cm"),
        ("A square has a perimeter of 36 cm. What is its area?", 81, [36, 9, 324], "Side = 36 ÷ 4 = 9 cm, so area = 9 × 9 = <b>81 cm²</b>.", " cm²"),
        ("A rectangle has an area of 72 cm² and a width of 6 cm. What is its length?", 12, [66, 18, 30], "Length = 72 ÷ 6 = <b>12 cm</b>.", " cm"),
        ("A triangle has an area of 30 cm² and a base of 10 cm. What is its perpendicular height?", 6, [3, 20, 12], "½ × 10 × <i>h</i> = 30, so 5<i>h</i> = 30 and <i>h</i> = <b>6 cm</b>.", " cm"),
        ("A wall is 5 m wide and 2.4 m high. One tin of paint covers 6 m². How many tins are needed?", 2, [3, 1, 12], "Area = 5 × 2.4 = 12 m². 12 ÷ 6 = <b>2 tins</b>.", ""),
        ("A room is 4.5 m by 3 m. Carpet costs $20 per m². What is the cost?", 270, [150, 300, F(135, 1)], "Area = 4.5 × 3 = 13.5 m². 13.5 × $20 = <b>$270</b>.", "$"),
        ("A rectangular photo is 15 cm by 10 cm. It has a 2 cm border all round. What is the perimeter of the outside of the border?", 66, [50, 58, 54], "Outside: (15 + 4) by (10 + 4) = 19 by 14. Perimeter = 2 × (19 + 14) = <b>66 cm</b>.", " cm"),
        ("Square tiles of side 50 cm cover a floor 4 m by 3 m. How many tiles are needed?", 48, [12, 24, 14], "4 m = 8 tiles and 3 m = 6 tiles, so 8 × 6 = <b>48 tiles</b>.", ""),
        ("Which has the larger area: a 6 cm by 6 cm square or a 9 cm by 4 cm rectangle?", None, None, None, None),
        ("A rectangle has a perimeter of 20 cm. Which of these could be its area?", None, None, None, None),
    ]
    for q, a, w, e, unit in data:
        if a is None:
            continue
        if unit == "$":
            its.append(QN(q, a, w, e, fmt=aud))
        else:
            its.append(QN(q, a, w, e, unit=unit))
    for q, a, w, e in [
        ("Which has the larger area: a 6 cm by 6 cm square or a 9 cm by 4 cm rectangle?", "They have the same area", ["The square", "The rectangle", "You cannot tell"],
         "Square: 36 cm². Rectangle: 36 cm². <b>They have the same area</b> (but different perimeters: 24 cm and 26 cm)."),
        ("A rectangle has a perimeter of 20 cm. Which of these could be its area?", "24 cm²", ["40 cm²", "100 cm²", "50 cm²"],
         "Length + width = 10. For example 6 × 4 = <b>24 cm²</b>. The largest possible area is 5 × 5 = 25 cm², so 40 and 100 are impossible."),
        ("What is the area of a triangle with base 7 cm and perpendicular height 6 cm?", "21 cm²", ["42 cm²", "13 cm²", "26 cm²"], "½ × 7 × 6 = <b>21 cm²</b>."),
        ("Which units are used for area?", "cm², m² or km²", ["cm, m or km", "cm³ or m³", "litres"], "Area is measured in <b>square units</b> such as cm² and m²."),
        ("A parallelogram has base 9 cm and perpendicular height 4 cm. Its slanted side is 5 cm. What is its area?", "36 cm²", ["45 cm²", "18 cm²", "28 cm²"],
         "Area = base × perpendicular height = 9 × 4 = <b>36 cm²</b>. The 5 cm side is not used."),
        ("A trapezium has parallel sides of 6 cm and 10 cm and a height of 5 cm. What is its area?", "40 cm²", ["80 cm²", "300 cm²", "21 cm²"], "½ × (6 + 10) × 5 = <b>40 cm²</b>."),
        ("How many cm² are in 1 m²?", "10 000", ["100", "1000", "1 000 000"], "1 m² = 100 cm × 100 cm = <b>10 000 cm²</b>."),
        ("The area of a rectangle is 48 m². Its length is 3 times its width. What is its width?", "4 m", ["16 m", "12 m", "8 m"], "<i>w</i> × 3<i>w</i> = 48, so <i>w</i>² = 16 and <i>w</i> = <b>4 m</b>."),
        ("Two identical squares are placed side by side to make a rectangle with perimeter 30 cm. What is the side of each square?", "5 cm", ["7.5 cm", "3.75 cm", "10 cm"],
         "The rectangle is 2<i>s</i> by <i>s</i>, so its perimeter is 6<i>s</i> = 30 and <i>s</i> = <b>5 cm</b>."),
        ("A path 1 m wide goes round a lawn 10 m by 6 m. What is the area of the path?", "36 m²", ["32 m²", "60 m²", "96 m²"], "Outside 12 × 8 = 96 m². Lawn 10 × 6 = 60 m². Path = 96 − 60 = <b>36 m²</b>."),
    ]:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p>A <b>composite shape</b> is made of simpler shapes. To find its area, split it into rectangles, triangles or "
        "trapeziums and add the areas, or find a bigger shape and <b>subtract</b> the part that is missing.</p>"
        "<ul><li>Trapezium: area = ½(<i>a</i> + <i>b</i>)<i>h</i></li><li>Rhombus or kite: area = ½ × diagonal × diagonal</li></ul>"
        "<p>For the <b>perimeter</b>, add every outside edge. Work out missing lengths from the lengths you know.</p>"
        + fig(trap_svg(4, 8, 5)),
        [("Find the area of a trapezium with parallel sides 4 cm and 8 cm and height 5 cm.", ["½ × (4 + 8) × 5 = ½ × 12 × 5."], "30 cm²"),
         ("A 1 m path goes round a lawn 10 m by 6 m. Find the area of the path.", ["Outside: 12 × 8 = 96 m².", "Lawn: 10 × 6 = 60 m².", "96 − 60."], "36 m²")],
        ["Forgetting to halve in the trapezium or kite formula.",
         "Using a slanted side instead of the perpendicular height.",
         "Missing a side when finding the perimeter of an L-shape: there are 6 sides.",
         "Adding the missing piece instead of taking it away."])


def main():
    sets = [S("Area of trapeziums, rhombuses and kites", collect(one_trap, 14, R) + collect(one_kite, 6, R)),
            S("Perimeter of composite shapes", collect(one_per, 20, R)),
            S("Area of composite shapes", collect(one_comp, 20, R)),
            S("Shapes with a piece removed", collect(one_hole, 20, R)),
            S("Area and perimeter problems", problems())]
    make(8, "area-and-perimeter-of-composite-shapes", 9, "AC9M8M01",
         "Area and Perimeter of Composite Shapes: Trapeziums, Kites and L-Shapes",
         "Year 8 Composite Area Worksheets: Trapeziums, Kites, L-Shapes and Paths (Free, Answer Key)",
         "Composite area and perimeter",
         "solve problems involving the area and perimeter of irregular and composite shapes using appropriate units",
         "Free Year 8 maths worksheets on composite shapes for the Australian Curriculum (AC9M8M01): area of trapeziums, rhombuses "
         "and kites, perimeter and area of L-shapes, paths, borders and real-life problems. 100 questions with an answer key.",
         "Split a composite shape into simple shapes, or take a piece away from a bigger shape.",
         "Trapezium area = ½(a + b)h. Rhombus or kite area = ½ × product of the diagonals.",
         body(),
         [("How do I find the area of a composite shape?", "Split it into rectangles, triangles or trapeziums and add their areas, or find the area of a bigger shape and subtract the missing part."),
          ("What is the formula for the area of a trapezium?", "Area = ½(a + b)h, where a and b are the parallel sides and h is the perpendicular height."),
          ("How do I find the area of a kite or rhombus?", "Multiply the two diagonals and halve the answer."),
          ("How do I find the perimeter of an L-shape?", "Find any missing side lengths first, then add all six outside edges.")],
         sets, R)


if __name__ == "__main__":
    main()
