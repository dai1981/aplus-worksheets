# -*- coding: utf-8 -*-
"""
Texas Grade 3 Math: Area of Rectangles and Composite Figures (TEKS 3.6C, 3.6D)
  python3 tools/gen_ustx_math_g3_area.py
Rows times squares in each row on a grid, counting square units (the Ontario Grade 3 maker with Texas names),
rectangles with side lengths, composite figures split into rectangles, and word problems with a missing side.
Wrong answers come from real mistakes: adding the sides (perimeter), counting the squares on the edge only, adding
the outside lengths of an L-shape, and counting an overlap twice.
"""
import random
from tx_common import (Kid, mcq, collect, finish, make, fig, figure, lesson, S, run, adopt, svg_wrap, text, comma,
                       GREEN, FILL, INK, example)
from gen_us_math_g3 import grid_rect_svg
import gen_caon_math_g3_area as on

adopt(on)
R = random.Random(61501)
UNITS = [("cm", "square centimeters"), ("in.", "square inches"), ("ft", "square feet"), ("m", "square meters"), ("yd", "square yards")]


def rect_svg(w, h, wl, hl, scale=None):
    s = scale or min(220.0 / max(w, h), 30)
    W, H = w * s, h * s
    b = ["<rect x='50' y='16' width='%.1f' height='%.1f' fill='%s' stroke='%s' stroke-width='3'/>" % (W, H, FILL, GREEN),
         text(50 + W / 2, 16 + H + 22, wl, 15), text(44, 16 + H / 2 + 5, hl, 15, anchor="end")]
    return svg_wrap(int(W + 70), int(H + 44), "".join(b), "rectangle %s by %s" % (wl, hl))


def l_svg(a, b, c, d, u):
    """L-shape: full width a, full height b; top-right notch c wide and d tall is cut out."""
    s = min(220.0 / max(a, b), 26)
    pts = [(0, 0), (a - c, 0), (a - c, d), (a, d), (a, b), (0, b)]
    poly = " ".join("%.1f,%.1f" % (60 + x * s, 16 + y * s) for x, y in pts)
    t = [("%d %s" % (a, u), 60 + a * s / 2, 16 + b * s + 22, "middle"), ("%d %s" % (b, u), 52, 16 + b * s / 2 + 5, "end"),
         ("%d %s" % (a - c, u), 60 + (a - c) * s / 2, 10, "middle"), ("%d %s" % (b - d, u), 66 + a * s, 16 + (d + b) * s / 2 + 5, "start"),
         ("%d %s" % (c, u), 60 + (a - c + c / 2.0) * s, 16 + d * s - 6, "middle"), ("%d %s" % (d, u), 66 + (a - c) * s, 16 + d * s / 2 + 5, "start")]
    b_ = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='3'/>" % (poly, FILL, GREEN)]
    for lab, x, y, an in t:
        b_.append(text(x, y, lab, 13, anchor=an))
    return svg_wrap(int(a * s + 130), int(b * s + 44), "".join(b_), "L-shaped figure")


# ------------------------------------------------------------ set 1: rows times squares
def one_rows(r):
    w, h = r.randint(2, 9), r.randint(2, 7)
    pic = fig(grid_rect_svg(w, h, 26))
    kind = r.choice(["area", "area", "expr"])
    if kind == "area":
        return mcq(pic + "Each square is 1 square unit. What is the area of the rectangle?", "%d square units" % (w * h),
                   ["%d square units" % (w + h), "%d square units" % (2 * (w + h)), "%d square units" % (w * h - w), "%d square units" % (w * h + h)],
                   "%d rows with %d squares in each row: %d × %d = <b>%d square units</b>." % (h, w, h, w, w * h))
    return mcq(pic + "Which expression gives the area in square units?", "%d × %d" % (h, w), ["%d + %d" % (h, w), "%d + %d + %d + %d" % (h, w, h, w), "%d × %d" % (h + 1, w)],
               "There are %d rows of %d squares, so the area is <b>%d × %d</b> = %d square units." % (h, w, h, w, w * h))


# ------------------------------------------------------------ set 3: rectangles with side lengths
def one_rect(r):
    w, h = r.randint(2, 10), r.randint(2, 9)
    if w == h and r.random() < 0.6:
        return None
    u, su = r.choice(UNITS)
    pic = fig(rect_svg(w, h, "%d %s" % (w, u), "%d %s" % (h, u)))
    return mcq(pic + "What is the area of the rectangle?", "%d %s" % (w * h, su),
               ["%d %s" % (2 * (w + h), su), "%d %s" % (w + h, su), "%d %s" % (w * h, u), "%d %s" % (w * (h + 1), su)],
               "Area = length × width = %d × %d = <b>%d %s</b>. Area is measured in square units." % (w, h, w * h, su))


# ------------------------------------------------------------ set 4: composite figures
def one_comp(r):
    a, b = r.randint(5, 10), r.randint(5, 9)
    c, d = r.randint(2, a - 2), r.randint(2, b - 2)
    u, su = r.choice(UNITS[:3])
    area = a * b - c * d
    pic = fig(l_svg(a, b, c, d, u))
    kind = r.choice(["area", "area", "split"])
    if kind == "area":
        return mcq(pic + "Split the figure into two rectangles. What is its area?", "%d %s" % (area, su),
                   ["%d %s" % (a * b, su), "%d %s" % (2 * (a + b), su), "%d %s" % ((a - c) * b + a * (b - d), su), "%d %s" % (area + c * d // 2 if c * d > 2 else area + 2, su)],
                   "Left part: %d × %d = %d. Right part: %d × %d = %d. Add: %d + %d = <b>%d %s</b>." % (a - c, b, (a - c) * b, c, b - d, c * (b - d), (a - c) * b, c * (b - d), area, su))
    right = "(%d × %d) + (%d × %d)" % (a - c, b, c, b - d)
    return mcq(pic + "Which expression finds the area of the figure?", right,
               ["(%d × %d) + (%d × %d)" % (a, b, c, d), "%d + %d + %d + %d" % (a, b, a - c, b - d), "(%d × %d) + (%d × %d)" % (a - c, b, a, b - d)],
               "Cut it into a %d by %d rectangle and a %d by %d rectangle that do not overlap: <b>%s</b> = %d %s." % (a - c, b, c, b - d, right, area, su))


# ------------------------------------------------------------ set 5: word problems
def one_story(r):
    k = Kid(r).next()
    kind = r.choice(["rug", "garden", "missing", "missing", "compare"])
    if kind in ("rug", "garden"):
        w, h = r.randint(3, 10), r.randint(2, 9)
        what = "rug" if kind == "rug" else "vegetable garden"
        u, su = ("ft", "square feet") if kind == "rug" else ("yd", "square yards")
        return mcq("%s's %s is a rectangle %d %s long and %d %s wide. What is its area?" % (k["n"], what, w, u, h, u), "%d %s" % (w * h, su),
                   ["%d %s" % (2 * (w + h), su), "%d %s" % (w + h, su), "%d %s" % (w * h + w, su)], "%d × %d = <b>%d %s</b>." % (w, h, w * h, su))
    if kind == "missing":
        w, h = r.randint(2, 10), r.randint(2, 10)
        return mcq("A rectangle has an area of %d square inches. One side is %d inches long. How long is the other side?" % (w * h, w), "%d inches" % h,
                   ["%d inches" % (w * h - w), "%d inches" % (w * h // 2), "%d inches" % (h + 1), "%d inches" % (w * h + w)],
                   "Area = %d × ☐ = %d. %d ÷ %d = <b>%d inches</b>." % (w, w * h, w * h, w, h))
    a, b, c, d = r.randint(3, 8), r.randint(3, 8), r.randint(3, 8), r.randint(3, 8)
    if a * b == c * d or a + b == c + d:
        return None
    k2 = Kid(r).next()
    if k2["n"] == k["n"]:
        return None
    win = k["n"] if a * b > c * d else k2["n"]
    return mcq("%s's poster is %d in. by %d in. %s's poster is %d in. by %d in. Whose poster has the greater area?" % (k["n"], a, b, k2["n"], c, d), win,
               [k2["n"] if win == k["n"] else k["n"], "They are the same", "The one with the longer side"],
               "%d × %d = %d and %d × %d = %d square inches. <b>%s</b>'s poster has the greater area." % (a, b, a * b, c, d, c * d, win))


def build():
    sets = [S("Rows times squares in each row", collect(one_rows, 20, R)),
            S("Count square units", run(on.set_count, "rnd", "seen", seed=161)["items"]),
            S("Rectangles with side lengths", collect(one_rect, 20, R)),
            S("Composite figures", collect(one_comp, 20, R)),
            S("Area word problems", collect(one_story, 20, R))]
    finish(sets, R)
    body = lesson(
        "<ul><li><b>Area</b> is the number of unit squares that cover a shape, with no gaps or overlaps.</li>"
        "<li>A rectangle is rows of squares: area = number of rows × squares in each row = length × width.</li>"
        "<li>Area uses <b>square units</b>: square inches, square feet, square centimeters.</li>"
        "<li>For a <b>composite figure</b>, cut it into rectangles that do not overlap, find each area, and add.</li></ul>",
        [figure(grid_rect_svg(6, 4, 26), "4 rows of 6 squares: 4 × 6 = 24 square units."),
         figure(l_svg(8, 6, 3, 2, "ft"), "Cut it into 5 × 6 = 30 and 3 × 4 = 12. Area = 30 + 12 = 42 square feet.")],
        [["Adding the sides (that is perimeter)", "Area multiplies: rows × squares in each row."],
         ["Writing ft instead of square feet", "Area is always in square units."],
         ["Multiplying the outside lengths of an L-shape", "Cut it into rectangles first, then add their areas."]])
    faq = [("What does TEKS 3.6C ask?", "Find the area of rectangles with whole-number side lengths by multiplying the number of rows by the number of unit squares in each row."),
           ("What does TEKS 3.6D ask?", "Split composite figures made of rectangles into non-overlapping rectangles and add their areas to find the area of the whole figure."),
           ("What is the difference between area and perimeter?", "Area is the space inside, in square units. Perimeter is the distance around, in units."),
           ("How do you find a missing side if you know the area?", "Divide the area by the side you know. A 24 square inch rectangle with a 6 inch side has a 4 inch side.")]
    make("area", 15, "Geometry and Measurement", "3.6C, 3.6D",
         "3.6C determine the area of rectangles with whole number side lengths in problems using multiplication related to the number of rows times the number of unit squares in each row; 3.6D decompose composite figures formed by rectangles into non-overlapping rectangles to determine the area of the original figure using the additive property of area",
         "Area of Rectangles and Composite Figures", "Area",
         "Free Grade 3 area worksheets for Texas TEKS 3.6C and 3.6D: rows times squares, count square units, rectangles with side lengths, composite figures split into rectangles and word problems. 100 STAAR-style questions with answers.",
         "Area of a rectangle = rows × squares in each row.", "Split a composite figure into rectangles that do not overlap, then add their areas.",
         body, faq, sets, seo_title="Grade 3 Area Worksheets: Rectangles and Composite Figures (TEKS 3.6C, 3.6D, STAAR)")


if __name__ == "__main__":
    build()
