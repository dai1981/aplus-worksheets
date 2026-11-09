# -*- coding: utf-8 -*-
"""
US Grade 7 Math: Area, Surface Area and Volume (7.G.B.6)
  python tools/gen_us_math_g7_area_surface_area_volume.py
Area of triangles, trapezoids and composite figures; volume and surface area of right prisms.
Wrong answers come from real mistakes: forgetting the 1/2 in a triangle, adding the sides,
using the slanted side as the height, mixing up surface area and volume, and counting only
three faces of a box.
"""
import random
from fractions import Fraction as F
from ws_common import (num, mcq, balance, B, fig, figure, svg_wrap, text, line, table, example, write_unit, GREEN, FILL, BLUE, INK)

R = random.Random(71501)
UPDATED = "2026-11-09"


def n(v):
    return num(F(v))


def item(q, v, ws, e, unit=""):
    v = F(v)
    cands = []
    for w in list(ws) + [v * 2, v / 2, v + 10, v - 10]:
        w = F(w)
        if w > 0 and w != v and num(w) is not None:
            cands.append((n(w) + unit, w))
    return mcq(q, (n(v) + unit, v), cands, e)


def box_svg(l, w, h, lab=("l", "w", "h")):
    """Oblique drawing of a rectangular prism."""
    s = 14
    L, W_, H_ = min(l * s, 190), min(w * s * 0.6, 70), min(h * s, 120)
    x0, y0 = 30, 40 + W_
    pts = lambda *p: " ".join("%.1f,%.1f" % q for q in p)
    a, b, c, d = (x0, y0), (x0 + L, y0), (x0 + L, y0 + H_), (x0, y0 + H_)
    a2, b2, c2 = (x0 + W_, y0 - W_), (x0 + L + W_, y0 - W_), (x0 + L + W_, y0 + H_ - W_)
    body = ("<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.5'/>" % (pts(a, b, c, d), FILL, GREEN)
            + "<polygon points='%s' fill='#e6f0ea' stroke='%s' stroke-width='2.5'/>" % (pts(a, a2, b2, b), GREEN)
            + "<polygon points='%s' fill='#b9d8c3' stroke='%s' stroke-width='2.5'/>" % (pts(b, b2, c2, c), GREEN)
            + text(x0 + L / 2, y0 + H_ + 22, lab[0], 15, col=BLUE)
            + text(x0 + L + W_ / 2 + 22, y0 + H_ - W_ / 2 + 10, lab[1], 15, "start", col=BLUE)
            + text(x0 - 8, y0 + H_ / 2 + 5, lab[2], 15, "end", col=BLUE))
    return svg_wrap(int(x0 + L + W_ + 90), int(y0 + H_ + 36), body, "rectangular prism")


def tri_svg(b, h, slant=None):
    s = 14
    B_, H_ = b * s, h * s
    x0, y0 = 30, 20
    apex = (x0 + B_ * 0.3, y0)
    body = ("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='2.5'/>" % (x0, y0 + H_, x0 + B_, y0 + H_, apex[0], apex[1], FILL, GREEN)
            + line(apex[0], apex[1], apex[0], y0 + H_, BLUE, 2, " stroke-dasharray='5 4'")
            + text(x0 + B_ / 2, y0 + H_ + 22, "%s cm" % n(b), 15, col=BLUE)
            + text(apex[0] + 6, y0 + H_ / 2 + 5, "%s cm" % n(h), 15, "start", col=BLUE))
    if slant:
        body += text(x0 + B_ * 0.72, y0 + H_ * 0.45, "%s cm" % n(slant), 15, "start", col=INK)
    return svg_wrap(int(x0 + B_ + 70), int(y0 + H_ + 34), body, "triangle with base and height")


# ------------------------------------------------------------ set 1: area of 2D shapes
def set_area():
    its = []
    for b, h, sl in [(10, 6, 7), (8, 5, 6), (12, 7, 9), (9, 4, 5), (14, 6, 8)]:
        A = F(b * h, 2)
        its.append(item("Find the area of the triangle." + fig(tri_svg(b, h, sl)), A, [b * h, b * sl / F(2), b + h + sl],
                        "A = ½ × base × height = ½ × %d × %d = %s cm². Not %s: that forgets the ½. Use the height, not the slanted side." % (b, h, n(A), n(b * h)), " cm²"))
    for b1, b2, h in [(6, 10, 4), (5, 9, 6), (8, 12, 5), (3, 7, 8), (10, 16, 7)]:
        A = F(b1 + b2, 2) * h
        its.append(item("A trapezoid has bases %d m and %d m and height %d m. What is its area?" % (b1, b2, h), A, [(b1 + b2) * h, b1 * b2 * h, b1 + b2 + h],
                        "A = ½ × (b₁ + b₂) × h = ½ × (%d + %d) × %d = %s m²." % (b1, b2, h, n(A)), " m²"))
    for b, h in [(9, 4), (12, 5), (F("7.5"), 4)]:
        its.append(item("A parallelogram has base %s ft and height %s ft. What is its area?" % (n(b), n(h)), F(b) * h, [F(b) * h / 2, 2 * (F(b) + h), F(b) + h],
                        "A = base × height = %s × %s = %s ft²." % (n(b), n(h), n(F(b) * h)), " ft²"))
    comp = [("An L-shape is a 10 m × 6 m rectangle with a 4 m × 3 m rectangle cut from one corner. What is its area?", 48, [60, 72, 12], "60 − 12 = 48 m²."),
            ("A shape is an 8 cm × 5 cm rectangle with a triangle (base 8 cm, height 3 cm) on top. What is the total area?", 52, [64, 40, 12], "40 + ½ × 8 × 3 = 40 + 12 = 52 cm²."),
            ("A 12 ft × 12 ft square has a 4 ft × 4 ft square hole. What area is left?", 128, [144, 16, 136], "144 − 16 = 128 ft²."),
            ("A house shape: a 6 m × 4 m rectangle with a triangle on top (base 6 m, height 2 m). What is the area?", 30, [36, 24, 26], "24 + ½ × 6 × 2 = 24 + 6 = 30 m²."),
            ("Two rectangles side by side: 5 in. × 3 in. and 7 in. × 3 in. What is the total area?", 36, [15, 21, 18], "15 + 21 = 36 in²."),
            ("A rectangle 9 cm × 4 cm has a right triangle (legs 4 cm and 3 cm) attached at one end. What is the area?", 42, [48, 36, 30], "36 + ½ × 4 × 3 = 36 + 6 = 42 cm²."),
            ("A garden is a 20 m × 15 m rectangle with a 5 m × 5 m pond. What is the area of the grass?", 275, [300, 25, 325], "300 − 25 = 275 m².")]
    for q, v, ws, e in comp:
        its.append(item(q, v, ws, e, " " + ("m²" if " m" in q else "cm²" if "cm" in q else "ft²" if "ft" in q else "in²")))
    return {"title": "Area: triangles, trapezoids and composite shapes", "items": its}


# ------------------------------------------------------------ set 2: volume
def set_volume():
    its = []
    for l, w, h in [(5, 3, 4), (8, 2, 6), (10, 4, 3), (7, 5, 2), (6, 6, 6), (12, 3, 5)]:
        V = l * w * h
        its.append(item("Find the volume of the rectangular prism (%d cm by %d cm by %d cm)." % (l, w, h) + fig(box_svg(l, w, h, ("%d cm" % l, "%d cm" % w, "%d cm" % h))),
                        V, [l + w + h, 2 * (l * w + l * h + w * h), l * w], "V = l × w × h = %d × %d × %d = %d cm³. Not %d: that is the surface area." % (
                            l, w, h, V, 2 * (l * w + l * h + w * h)), " cm³"))
    for b, h, L in [(6, 4, 10), (8, 3, 5), (5, 6, 7), (10, 4, 9), (12, 5, 4)]:
        V = F(b * h, 2) * L
        its.append(item("A triangular prism has a triangle base with base %d in. and height %d in. The prism is %d in. long. What is its volume?" % (b, h, L),
                        V, [b * h * L, F(b * h, 2), b + h + L], "Area of the triangle = ½ × %d × %d = %s in². V = %s × %d = %s in³. Not %s: that forgets the ½." % (
                            b, h, n(F(b * h, 2)), n(F(b * h, 2)), L, n(V), n(b * h * L)), " in³"))
    for Bv, h in [(24, 5), (F("12.5"), 8), (36, 3)]:
        its.append(item("A prism has a base area of %s m² and a height of %s m. What is its volume?" % (n(Bv), n(h)), F(Bv) * h, [F(Bv) + h, F(Bv) * h / 2, F(Bv) * h * 2],
                        "V = base area × height = %s × %s = %s m³." % (n(Bv), n(h), n(F(Bv) * h)), " m³"))
    for l, w, h in [(F("2.5"), 4, 3), (F(1, 2), 6, 8), (F("1.5"), F("1.5"), 4)]:
        V = F(l) * w * h
        its.append(item("A box is %s ft by %s ft by %s ft. What is its volume?" % (n(l), n(w), n(h)), V, [F(l) + w + h, V * 2, F(l) * w], "V = %s × %s × %s = %s ft³." % (n(l), n(w), n(h), n(V)), " ft³"))
    for V, l, w in [(120, 6, 5), (84, 7, 3), (200, 10, 4)]:
        h = F(V, l * w)
        its.append(item("A rectangular prism has volume %d cm³, length %d cm and width %d cm. What is its height?" % (V, l, w), h, [V - l - w, F(V, l), V * l * w if V * l * w < 10000 else h + 3],
                        "h = V ÷ (l × w) = %d ÷ %d = %s cm." % (V, l * w, n(h)), " cm"))
    return {"title": "Volume of prisms", "items": its}


# ------------------------------------------------------------ set 3: surface area
def set_surface():
    its = []
    for l, w, h in [(5, 3, 4), (6, 2, 3), (8, 5, 2), (4, 4, 4), (10, 6, 3), (7, 3, 5), (9, 2, 4)]:
        S = 2 * (l * w + l * h + w * h)
        its.append(item("Find the surface area of a rectangular prism %d cm by %d cm by %d cm." % (l, w, h) + (fig(box_svg(l, w, h, ("%d cm" % l, "%d cm" % w, "%d cm" % h))) if l != 4 else ""),
                        S, [S // 2, l * w * h, l * w + l * h + w * h + l * w], "Three pairs of faces: 2(%d × %d) + 2(%d × %d) + 2(%d × %d) = %d + %d + %d = %d cm². Not %d: count all 6 faces." % (
                            l, w, l, h, w, h, 2 * l * w, 2 * l * h, 2 * w * h, S, S // 2), " cm²"))
    for s in [3, 5, 7, 10]:
        its.append(item("What is the surface area of a cube with edges %d in.?" % s, 6 * s * s, [s ** 3, 4 * s * s, 6 * s], "6 faces, each %d × %d = %d in². 6 × %d = %d in²." % (s, s, s * s, s * s, 6 * s * s), " in²"))
    tri = [(6, 8, 10, 5), (3, 4, 5, 10), (5, 12, 13, 4), (9, 12, 15, 6)]
    for a, b, c, L in tri:
        S = a * b + (a + b + c) * L
        its.append(item("A triangular prism has right-triangle bases with legs %d cm and %d cm and hypotenuse %d cm. The prism is %d cm long. What is its surface area?" % (a, b, c, L),
                        S, [F(a * b, 2) * L, (a + b + c) * L, a * b // 2 + (a + b + c) * L], "Two triangles: 2 × ½ × %d × %d = %d. Three rectangles: (%d + %d + %d) × %d = %d. Total %d cm²." % (
                            a, b, a * b, a, b, c, L, (a + b + c) * L, S), " cm²"))
    its.append(mcq("Which measures the space inside a box?", ("Volume", "v"), [("Surface area", "s"), ("Perimeter", "p"), ("Area of the base", "b")],
                   "Volume (cubic units) measures the space inside. Surface area (square units) measures the outside covering."))
    its.append(mcq("Wrapping paper covers a gift box. Which do you need to find?", ("Surface area", "s"), [("Volume", "v"), ("Perimeter of the base", "p"), ("Height only", "h")],
                   "Paper covers the outside faces, so you need the surface area."))
    its.append(mcq("Which unit fits a surface area?", ("cm²", "a"), [("cm³", "b"), ("cm", "c"), ("cm⁴", "d")], "Surface area is an area, so it uses square units."))
    its.append(mcq("A net of a rectangular prism has how many rectangles?", ("6", 6), [("4", 4), ("5", 5), ("8", 8)], "A rectangular prism has 6 faces, so its net has 6 rectangles."))
    its.append(mcq("Doubling every edge of a cube makes its volume how many times as large?", ("8 times", 8), [("2 times", 2), ("4 times", 4), ("6 times", 6)],
                   "Volume = s³. (2s)³ = 8s³. (Surface area becomes 4 times as large.)"))
    return {"title": "Surface area of prisms", "items": its}


# ------------------------------------------------------------ set 4: mixed
def set_mixed():
    its = []
    for l, w, h in [(4, 3, 2), (6, 5, 4), (10, 2, 2), (5, 5, 3), (8, 4, 1)]:
        V = l * w * h
        S = 2 * (l * w + l * h + w * h)
        its.append(mcq("A box is %d cm by %d cm by %d cm. What are its volume and surface area?" % (l, w, h), ("V = %d cm³, SA = %d cm²" % (V, S), "g"),
                       [("V = %d cm³, SA = %d cm²" % (S, V), "a"), ("V = %d cm³, SA = %d cm²" % (V, S // 2), "b"), ("V = %d cm³, SA = %d cm²" % (l + w + h, S), "c")],
                       "V = %d × %d × %d = %d cm³. SA = 2(%d + %d + %d) = %d cm²." % (l, w, h, V, l * w, l * h, w * h, S)))
    for side, k in [(2, 3), (3, 2), (1, 5), (4, 2)]:
        v = (side * k) ** 3
        its.append(item("A cube has edges %d ft. A bigger cube has edges %d times as long. What is the volume of the bigger cube?" % (side, k), v, [side ** 3 * k, side ** 3, (side * k) ** 2 * 6],
                        "New edge: %d ft. Volume = %d³ = %d ft³." % (side * k, side * k, v), " ft³"))
    shapes = [("A tent is a triangular prism. The triangle has base 6 ft and height 4 ft, and the tent is 8 ft long. How much space is inside?", 96, [192, 12, 18], "½ × 6 × 4 = 12 ft². 12 × 8 = 96 ft³.", " ft³"),
              ("A pool is 10 m long, 5 m wide and 2 m deep. How much water fills it?", 100, [17, 160, 50], "10 × 5 × 2 = 100 m³.", " m³"),
              ("A cereal box is 20 cm by 7 cm by 30 cm. How much cardboard is needed (no overlap)?", 1900, [4200, 950, 57], "2(140 + 600 + 210) = 2(950) = 1,900 cm².", " cm²"),
              ("A sandbox is 6 ft by 4 ft. Sand is filled 1.5 ft deep. How many cubic feet of sand?", 36, [24, F("11.5"), 72], "6 × 4 × 1.5 = 36 ft³.", " ft³"),
              ("A wall is 12 ft by 8 ft with a 3 ft by 7 ft door. How much wall needs paint?", 75, [96, 21, 117], "96 − 21 = 75 ft².", " ft²"),
              ("A gift box is a cube with 9 in. edges. How much paper covers it?", 486, [729, 324, 54], "6 × 81 = 486 in².", " in²")]
    for q, v, ws, e, u in shapes:
        its.append(item(q, v, ws, e, u))
    for V, b, h in [(60, 5, 4), (90, 6, 5), (84, 8, 3)]:
        L = F(V) / (F(b * h, 2))
        its.append(item("A triangular prism has volume %d cm³. Its triangle has base %d cm and height %d cm. How long is the prism?" % (V, b, h), L,
                        [F(V, b * h), V - b - h, L * 2 + 1], "Triangle area = ½ × %d × %d = %s. Length = %d ÷ %s = %s cm." % (b, h, n(F(b * h, 2)), V, n(F(b * h, 2)), n(L)), " cm"))
    for S_, s in [(150, 5), (54, 3)]:
        its.append(item("A cube has a surface area of %d in². What is the length of one edge?" % S_, s, [F(S_, 6), F(S_, 4), s * s], "Each face = %d ÷ 6 = %d in². %d = %d × %d, so the edge is %d in." % (S_, s * s, s * s, s, s, s), " in."))
    return {"title": "Volume and surface area together", "items": its}


# ------------------------------------------------------------ set 5: words
def set_words():
    its = []
    w = [("A fish tank is 24 in. long, 12 in. wide and 16 in. tall. How many cubic inches of water fill it?", 4608, [52, 1728, 2304], "24 × 12 × 16 = 4,608 in³.", " in³"),
         ("A storage unit is 10 ft by 8 ft by 9 ft. What is its volume?", 720, [27, 80, 524], "10 × 8 × 9 = 720 ft³.", " ft³"),
         ("A box is 3 ft by 2 ft by 2 ft. How many 1-foot cubes fit inside?", 12, [7, 32, 24], "3 × 2 × 2 = 12 cubes.", " cubes"),
         ("A 4 cm cube of clay is reshaped into a box with base 8 cm by 2 cm. How tall is the box?", 4, [8, 2, 16], "Volume = 4³ = 64 cm³. 64 ÷ (8 × 2) = 4 cm.", " cm"),
         ("A room is 15 ft by 12 ft. Carpet costs $3 per square foot. How much does carpet cost?", 540, [81, 180, 162], "15 × 12 = 180 ft². 180 × 3 = $540.", "$"),
         ("A garden bed is a trapezoid with parallel sides 8 m and 12 m and width 5 m between them. Soil is 0.5 m deep. How much soil is needed?", 25, [50, 240, F("12.5")],
          "Area = ½ × (8 + 12) × 5 = 50 m². 50 × 0.5 = 25 m³.", " m³"),
         ("A ramp is a triangular prism: triangle base 6 ft, height 2 ft, width 4 ft. How much concrete fills it?", 24, [48, 12, 6], "½ × 6 × 2 = 6 ft². 6 × 4 = 24 ft³.", " ft³"),
         ("A label wraps around the 4 side faces of a box 5 in. by 5 in. by 8 in. (not the top and bottom). What is the label's area?", 160, [200, 50, 80],
          "4 side faces, each 5 × 8 = 40 in². 4 × 40 = 160 in².", " in²"),
         ("A box of tissues is 9 in. by 5 in. by 4 in. How much cardboard makes it?", 202, [180, 101, 18], "2(45 + 36 + 20) = 2(101) = 202 in².", " in²"),
         ("A truck bed is 8 ft by 5 ft by 2 ft. Gravel weighs 100 pounds per cubic foot. How heavy is a full load?", 8000, [80, 1500, 4000], "8 × 5 × 2 = 80 ft³. 80 × 100 = 8,000 pounds.", " lb"),
         ("A 2 m × 3 m wall is tiled with 0.5 m × 0.5 m tiles. How many tiles are needed?", 24, [12, 6, 20], "Wall: 6 m². One tile: 0.25 m². 6 ÷ 0.25 = 24 tiles.", " tiles"),
         ("A juice box is 4 cm by 6 cm by 10 cm. 1 cm³ holds 1 mL. How many mL does it hold?", 240, [20, 248, 120], "4 × 6 × 10 = 240 cm³ = 240 mL.", " mL"),
         ("A pond is 12 m by 8 m with a 2 m × 2 m island in the middle. What is the water's surface area?", 92, [96, 4, 100], "96 − 4 = 92 m².", " m²"),
         ("Two boxes: A is 6 × 4 × 5 and B is 8 × 3 × 5 (in cm). How much more does B hold?", 0, [], "", ""),
         ("A triangular sail has base 3 m and height 5 m. Fabric costs $12 per square meter. How much is the fabric?", 90, [180, 45, 96], "½ × 3 × 5 = 7.5 m². 7.5 × 12 = $90.", "$"),
         ("A wooden block is 10 cm by 4 cm by 4 cm. Paint covers 50 cm² per mL. How many mL of paint cover the block?", F("4.48"), [F("3.2"), F("2.24"), 224],
          "SA = 2(40 + 40 + 16) = 192 cm². Hmm", " mL"),
         ("A planter is a box 30 in. by 10 in. by 12 in. It is filled to 3/4 of its height with soil. How much soil?", 2700, [3600, 900, 2400], "Soil depth = 9 in. 30 × 10 × 9 = 2,700 in³.", " in³"),
         ("An open box (no top) is 6 cm by 4 cm by 3 cm. What is its surface area?", 84, [108, 72, 60], "Bottom 24 + 2(18) + 2(12) = 24 + 36 + 24 = 84 cm².", " cm²"),
         ("A shed floor is a 10 ft × 8 ft rectangle. The roof forms a triangle on each end with base 8 ft and height 3 ft. What is the area of one end wall if the wall is 7 ft tall?", 68, [56, 80, 24],
          "Rectangle 8 × 7 = 56 ft² plus triangle ½ × 8 × 3 = 12 ft². 56 + 12 = 68 ft².", " ft²"),
         ("A cube-shaped water tank holds 27 m³. How long is each edge?", 3, [9, F("4.5"), 6], "3 × 3 × 3 = 27, so each edge is 3 m.", " m")]
    # fix two placeholder items
    w[13] = ("Box A is 6 cm × 4 cm × 5 cm and box B is 8 cm × 3 cm × 6 cm. How much more does box B hold?", 24, [120, 144, 2], "A: 120 cm³. B: 144 cm³. 144 − 120 = 24 cm³.", " cm³")
    w[15] = ("A wooden block is 10 cm by 4 cm by 4 cm. Paint covers 48 cm² per mL. How many mL of paint cover the block?", 4, [F("3.2"), 2, 8],
             "SA = 2(40 + 40 + 16) = 192 cm². 192 ÷ 48 = 4 mL.", " mL")
    for q, v, ws, e, u in w:
        q = q.replace("3/4", "¾")
        if u == "$":
            its.append(mcq(q, ("$%s" % "{:,}".format(v), v), [("$%s" % "{:,}".format(x), x) for x in ws if x != v], e))
        else:
            its.append(item(q, v, ws, e, u))
    return {"title": "Word problems", "items": its}


def body():
    rows = [["Triangle", "A = ½ × b × h", "square units"], ["Trapezoid", "A = ½ × (b₁ + b₂) × h", "square units"],
            ["Prism volume", "V = (area of base) × height", "cubic units"], ["Box volume", "V = l × w × h", "cubic units"],
            ["Box surface area", "SA = 2lw + 2lh + 2wh", "square units"]]
    return ("<h2>Area, surface area and volume</h2><p><b>Area</b> covers a flat shape. <b>Surface area</b> covers all the faces of a solid. "
            "<b>Volume</b> fills the space inside. Split a hard shape into rectangles and triangles, then add or subtract.</p>"
            + table(["Shape", "Formula", "Units"], rows)
            + figure(box_svg(5, 3, 4, ("5 cm", "3 cm", "4 cm")), "V = 5 × 3 × 4 = 60 cm³. SA = 2(15 + 20 + 12) = 94 cm².")
            + example("A tent is a triangular prism: triangle base 6 ft, height 4 ft, length 8 ft. How much space is inside?",
                      ["Base area = ½ × 6 × 4 = 12 ft².", "Volume = 12 × 8 = 96 ft³."], "96 ft³")
            + "<h2>Common mistakes</h2><ul><li>Forgetting the ½ for a triangle.</li><li>Using the slanted side instead of the height.</li>"
            "<li>Mixing up surface area (square units) and volume (cubic units).</li><li>Counting only 3 faces of a box: there are 6.</li></ul>")


def main():
    sets = [set_area(), set_volume(), set_surface(), set_mixed(), set_words()]
    balance(sets, R)
    unit = {
        "slug": "area-surface-area-volume",
        "title": "Area, Surface Area and Volume",
        "seo_title": "Grade 7 Area, Surface Area and Volume Worksheets: Triangles, Trapezoids and Prisms",
        "short_title": "Area, surface area and volume",
        "domain": "Geometry",
        "standard_code": "7.G.B.6",
        "standard_url": "https://www.thecorestandards.org/Math/Content/7/G/B/6/",
        "standard_text": "Solve real-world and mathematical problems involving area, volume and surface area of two- and three-dimensional objects composed of triangles, quadrilaterals, polygons, cubes, and right prisms.",
        "meta_desc": "Free Grade 7 area, surface area and volume worksheets: triangles, trapezoids and composite shapes, volume and surface area of rectangular and triangular prisms, and real-world problems. 100 practice questions with an answer key.",
        "key_big": "Volume = base area × height. Surface area = the total area of all the faces.",
        "key_sub": "Triangle: A = ½ × b × h. Box: V = l × w × h and SA = 2lw + 2lh + 2wh.",
        "body_html": body(),
        "faq": [
            {"q": "What is the difference between surface area and volume?", "a": "Surface area is the total area of the outside faces, in square units. Volume is the space inside, in cubic units."},
            {"q": "How do you find the volume of a triangular prism?", "a": "Find the area of the triangle (½ × base × height), then multiply by the length of the prism."},
            {"q": "How do you find the surface area of a box?", "a": "Add the areas of all 6 faces: SA = 2lw + 2lh + 2wh. A 5 × 3 × 4 box has SA = 2(15 + 20 + 12) = 94."},
            {"q": "How do I find the area of a composite shape?", "a": "Split it into rectangles and triangles, find each area, then add them. Subtract any parts that are cut out."}],
        "sets": sets,
        "pdf_url": "",
        "sort": 15,
        "updated": UPDATED,
    }
    write_unit("us", "math", "grade-7", unit)


if __name__ == "__main__":
    main()
