# -*- coding: utf-8 -*-
"""
Texas Grade 5 Math: Perimeter, Area and Volume Problems (TEKS 5.4H)
  python3 tools/gen_ustx_math_g5_perimeter_area_volume.py
Perimeter and area of rectangles with formulas, finding a missing side, volume with V = l × w × h and V = B × h,
choosing perimeter, area or volume, and multi-step word problems.
Wrong answers come from real mistakes: adding only two sides, mixing up area and perimeter, and adding the edge
lengths of a prism instead of multiplying.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)

tx_common.GRADE = "grade-5"

INK = "#1f2937"


def rect_svg(l, w, u):
    W = 190
    H = max(50, min(130, int(W * w / l)))
    return fig("<svg viewBox='0 0 360 %d' width='360' role='img' aria-label='rectangle %d by %d %s'><rect x='30' y='15' width='%d' height='%d' fill='#dbeafe' stroke='%s' stroke-width='2'/>"
               "<text x='%d' y='%d' font-size='15' text-anchor='middle' fill='%s'>%d %s</text><text x='%d' y='%d' font-size='15' fill='%s'>%d %s</text></svg>"
               % (H + 45, l, w, u, W, H, INK, 30 + W // 2, H + 37, INK, l, u, 38 + W, 20 + H // 2, INK, w, u))


def box_svg(l, w, h, u):
    L, Wd, Hh = min(l * 12, 170), min(w * 7, 60), min(max(h * 10, 40), 110)
    x0, y0 = 120, 20 + Wd
    pts_front = "%d,%d %d,%d %d,%d %d,%d" % (x0, y0, x0 + L, y0, x0 + L, y0 + Hh, x0, y0 + Hh)
    pts_top = "%d,%d %d,%d %d,%d %d,%d" % (x0, y0, x0 + Wd, y0 - Wd, x0 + L + Wd, y0 - Wd, x0 + L, y0)
    pts_side = "%d,%d %d,%d %d,%d %d,%d" % (x0 + L, y0, x0 + L + Wd, y0 - Wd, x0 + L + Wd, y0 + Hh - Wd, x0 + L, y0 + Hh)
    return fig("<svg viewBox='0 0 480 %d' width='480' role='img' aria-label='rectangular prism %d by %d by %d %s'>"
               "<polygon points='%s' fill='#dbeafe' stroke='%s' stroke-width='2'/><polygon points='%s' fill='#bfdbfe' stroke='%s' stroke-width='2'/><polygon points='%s' fill='#93c5fd' stroke='%s' stroke-width='2'/>"
               "<text x='%d' y='%d' font-size='14' text-anchor='middle' fill='%s'>%d %s</text>"
               "<text x='%d' y='%d' font-size='14' fill='%s'>%d %s</text>"
               "<text x='%d' y='%d' font-size='14' text-anchor='end' fill='%s'>%d %s</text></svg>"
               % (y0 + Hh + 30, l, w, h, u, pts_front, INK, pts_top, INK, pts_side, INK,
                  x0 + L // 2, y0 + Hh + 20, INK, l, u,
                  x0 + L + Wd + 8, y0 - Wd + Hh // 2 + 5, INK, h, u,
                  x0 + Wd // 2 - 8, y0 - Wd // 2 + 2, INK, w, u))


def one_rect(r):
    u = r.choice(["feet", "meters", "inches", "yards", "centimeters"])
    l, w = r.randint(8, 48), r.randint(3, 30)
    if w >= l:
        return None
    su = "square " + u
    if r.random() < 0.5:
        return mcq(rect_svg(l, w, u) + "What is the perimeter of the rectangle?", "%d %s" % (2 * (l + w), u), ["%d %s" % (l + w, u), "%d %s" % (l * w, u), "%d %s" % (2 * l + w, u)],
                   "P = 2 × l + 2 × w = 2 × %d + 2 × %d = <b>%d %s</b>." % (l, w, 2 * (l + w), u))
    return mcq(rect_svg(l, w, u) + "What is the area of the rectangle?", "%s %s" % (comma(l * w), su), ["%d %s" % (2 * (l + w), su), "%d %s" % (l + w, su), "%s %s" % (comma(l * w + l), su)],
               "A = l × w = %d × %d = <b>%s %s</b>." % (l, w, comma(l * w), su))


def one_missing(r):
    u = r.choice(["feet", "meters", "yards"])
    l, w = r.randint(9, 40), r.randint(4, 25)
    if w >= l:
        return None
    kind = r.choice(["area", "per", "vol"])
    if kind == "area":
        return mcq("A rectangle has an area of %s square %s. Its length is %d %s. What is its width?" % (comma(l * w), u, l, u), "%d %s" % (w, u), ["%d %s" % (l * w - l, u), "%d %s" % (w + 2, u), "%d %s" % ((l * w) // 2 - l, u)],
                   "A = l × w, so w = A ÷ l = %s ÷ %d = <b>%d %s</b>." % (comma(l * w), l, w, u))
    if kind == "per":
        p = 2 * (l + w)
        return mcq("A rectangle has a perimeter of %d %s. Its length is %d %s. What is its width?" % (p, u, l, u), "%d %s" % (w, u), ["%d %s" % (p - l, u), "%d %s" % (p - 2 * l, u), "%d %s" % (p // 2, u)],
                   "Half the perimeter is l + w = %d. %d − %d = <b>%d %s</b>." % (p // 2, p // 2, l, w, u))
    a, b, h = r.randint(3, 12), r.randint(2, 9), r.randint(2, 10)
    v = a * b * h
    return mcq("A rectangular prism has a volume of %d cubic %s. Its base is %d %s by %d %s. What is its height?" % (v, u, a, u, b, u), "%d %s" % (h, u), ["%d %s" % (v - a * b, u), "%d %s" % (v // a, u), "%d %s" % (h + a, u)],
               "V = B × h. B = %d × %d = %d. h = %d ÷ %d = <b>%d %s</b>." % (a, b, a * b, v, a * b, h, u))


def one_vol(r):
    u = r.choice(["inches", "feet", "centimeters", "meters"])
    l, w, h = r.randint(3, 15), r.randint(2, 9), r.randint(2, 12)
    v = l * w * h
    if r.random() < 0.5:
        return mcq(box_svg(l, w, h, u) + "What is the volume of the rectangular prism?", "%s cubic %s" % (comma(v), u), ["%d cubic %s" % (l + w + h, u), "%d cubic %s" % (l * w, u), "%s cubic %s" % (comma(2 * (l * w + l * h + w * h)), u)],
                   "V = l × w × h = %d × %d × %d = <b>%s cubic %s</b>." % (l, w, h, comma(v), u))
    B = l * w
    return mcq("The base of a rectangular prism has an area of %d square %s. The prism is %d %s tall. What is its volume?" % (B, u, h, u), "%s cubic %s" % (comma(v), u), ["%d cubic %s" % (B + h, u), "%s cubic %s" % (comma(B * h * 2), u), "%d cubic %s" % (B, u)],
               "V = B × h = %d × %d = <b>%s cubic %s</b>." % (B, h, comma(v), u))


WHICH = [("How much fencing goes around a garden?", "Perimeter"), ("How much carpet covers a bedroom floor?", "Area"), ("How much water fills a fish tank?", "Volume"),
         ("How much ribbon goes around the edge of a picture frame?", "Perimeter"), ("How much paint covers one wall?", "Area"), ("How much sand fills a sandbox?", "Volume"),
         ("How many square tiles cover a kitchen floor?", "Area"), ("How many cubes fill a box?", "Volume"), ("How much border goes around a bulletin board?", "Perimeter"),
         ("How much grass sod covers a backyard?", "Area"), ("How much soil fills a planter box?", "Volume"), ("How far is one lap around a rectangular field?", "Perimeter"),
         ("How much wrapping paper covers the top of a table?", "Area"), ("How much cereal fits in a box?", "Volume"), ("How much trim goes around a window?", "Perimeter")]


def one_which(r):
    q, a = r.choice(WHICH)
    unit = {"Perimeter": "units", "Area": "square units", "Volume": "cubic units"}
    return mcq(q + " Which measure do you need?", "%s (%s)" % (a, unit[a]), ["%s (%s)" % (b, unit[b]) for b in unit if b != a] + ["%s (%s)" % (a, [unit[b] for b in unit if b != a][0])],
               "<b>%s</b> is measured in %s." % (a, unit[a]))


def one_story(r):
    k = Kid(r).next()
    kind = r.choice(["fence", "tile", "tank", "bed", "boxes"])
    if kind == "fence":
        l, w, c = r.randint(12, 40), r.randint(8, 25), r.randint(3, 9)
        if w >= l:
            return None
        p = 2 * (l + w)
        return mcq("%s's backyard garden is %d feet long and %d feet wide. Fencing costs $%d per foot. How much does fencing for all four sides cost?" % (k["n"], l, w, c), "$%s" % comma(p * c), ["$%s" % comma((l + w) * c), "$%s" % comma(l * w * c), "$%d" % p],
                       "P = 2 × %d + 2 × %d = %d feet. %d × $%d = <b>$%s</b>." % (l, w, p, p, c, comma(p * c)))
    if kind == "tile":
        l, w, n = r.randint(8, 16), r.randint(6, 12), r.choice([4, 6, 9])
        a = l * w
        return mcq("A kitchen floor is %d feet by %d feet. A box of tiles covers %d square feet. How many boxes are needed?" % (l, w, n), str(-(-a // n)), [str(a // n) if a % n else str(a // n + 2), str(a), str(-(-2 * (l + w) // n))],
                   "A = %d × %d = %d square feet. %d ÷ %d = %d R%d, so <b>%d boxes</b>." % (l, w, a, a, n, a // n, a % n, -(-a // n)) if a % n else "A = %d × %d = %d square feet. %d ÷ %d = <b>%d boxes</b>." % (l, w, a, a, n, a // n))
    if kind == "tank":
        l, w, h, f = r.randint(20, 36), r.randint(10, 16), r.randint(12, 20), r.randint(2, 6)
        return mcq("A fish tank is %d inches long, %d inches wide and %d inches tall. Water fills it up to %d inches from the top. What is the volume of the water?" % (l, w, h, f), "%s cubic inches" % comma(l * w * (h - f)),
                   ["%s cubic inches" % comma(l * w * h), "%s cubic inches" % comma(l * w * f), "%s cubic inches" % comma(l * w * (h + f))],
                   "The water is %d − %d = %d inches deep. %d × %d × %d = <b>%s cubic inches</b>." % (h, f, h - f, l, w, h - f, comma(l * w * (h - f))))
    if kind == "bed":
        l, w, h = r.randint(4, 10), r.randint(2, 4), r.choice([1, 2])
        bag = r.choice([2, 4])
        v = l * w * h
        if v % bag:
            return None
        return mcq("A raised garden bed is %d feet long, %d feet wide and %d %s deep. A bag of soil fills %d cubic feet. How many bags fill the bed?" % (l, w, h, "foot" if h == 1 else "feet", bag), str(v // bag), [str(v), str(l * w // bag), str((l + w + h) // bag + 1)],
                   "V = %d × %d × %d = %d cubic feet. %d ÷ %d = <b>%d bags</b>." % (l, w, h, v, v, bag, v // bag))
    a, b, c = r.randint(3, 6), r.randint(2, 5), r.randint(2, 4)
    e = r.randint(2, 4)
    return mcq("A box holds cubes in %d rows of %d cubes, %d layers high. %s fills %d boxes. How many cubes is that?" % (a, b, c, k["n"], e), str(a * b * c * e), [str(a * b * c), str((a + b + c) * e), str(a * b * e)],
               "One box: %d × %d × %d = %d cubes. %d × %d = <b>%d cubes</b>." % (a, b, c, a * b * c, a * b * c, e, a * b * c * e))


def build():
    sets, R = build_sets([
        ("Perimeter and area of rectangles", [("collect", one_rect, 20)]),
        ("Find the missing side", [("collect", one_missing, 20)]),
        ("Volume: V = l × w × h and V = B × h", [("collect", one_vol, 20)]),
        ("Perimeter, area or volume?", [("collect", one_which, 15), ("collect", one_rect, 5)]),
        ("Multi-step word problems", [("collect", one_story, 20)]),
    ], 65017)
    finish(sets, R)
    body = lesson('<ul><li><b>Perimeter</b> is the distance around: P = 2 × l + 2 × w. It is measured in units (feet).</li><li><b>Area</b> is the space inside a flat shape: A = l × w. It is measured in square units.</li><li><b>Volume</b> is the space inside a solid: V = l × w × h, or V = B × h where B is the area of the base. It is measured in cubic units.</li><li>To find a missing side, work backward with the formula.</li></ul>',
        [example("A garden is 20 ft by 12 ft. Fencing costs $4 per foot.", ["P = 2 × 20 + 2 × 12 = 64 ft", "64 × $4"], "$256"), example("A box is 8 in by 5 in by 6 in. Find V.", ["V = 8 × 5 × 6"], "240 cubic inches")],
        [['Adding only two sides for perimeter', 'A rectangle has four sides: add l + w, then double it.'], ['Mixing up area and perimeter', 'Inside a shape is area (square units); around it is perimeter.'], ['Adding the edges of a prism', 'Volume multiplies: l × w × h.']])
    faq = [('What does TEKS 5.4H ask?', 'Represent and solve problems related to perimeter and/or area and related to volume.'), ('What is the difference between area and volume?', 'Area measures a flat surface in square units. Volume measures the space inside a solid in cubic units.'), ('What is B in V = B × h?', 'B is the area of the base. For a rectangular prism, B = l × w.'), ('How do I find a missing length from the area?', 'Divide the area by the known side.')]
    make('perimeter-area-and-volume-problems', 17, 'Geometry and Measurement', '5.4H',
         '5.4H represent and solve problems related to perimeter and/or area and related to volume',
         'Perimeter, Area and Volume Problems', 'Perimeter, Area and Volume Problems',
         'Free Grade 5 worksheets for Texas TEKS 5.4H: perimeter and area of rectangles, missing sides, volume with V = l × w × h and V = B × h, choosing the right measure and multi-step word problems. 100 questions with answers.',
         'Perimeter goes around, area covers, volume fills.', 'P = 2l + 2w, A = l × w, V = l × w × h = B × h.',
         body, faq, sets, seo_title='Grade 5 Perimeter, Area and Volume Word Problems Worksheets (TEKS 5.4H, STAAR)')


if __name__ == "__main__":
    build()
