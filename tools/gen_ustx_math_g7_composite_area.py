# -*- coding: utf-8 -*-
"""
Texas Grade 7 Math: Area of Composite Figures (TEKS 7.9C)
  python3 tools/gen_ustx_math_g7_composite_area.py
Area of triangles, trapezoids and simple composite shapes (US Grade 7 maker), rectangles with semicircles and
quarter circles, house shapes and L-shapes, shapes with a part cut out, and word problems (own makers with figures).
Wrong answers come from real mistakes: using the full circle instead of half, using the diameter as the radius, and
adding the part that should be cut out.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g7_area_surface_area_volume as asv
adopt(asv)
asv.R = random.Random(670130)
tx_common.GRADE = "grade-7"

INK = "#1f2937"
FILL = "#dbeafe"


def g(v):
    s = ("%.2f" % v).rstrip("0").rstrip(".")
    if "." in s:
        a, b = s.split(".")
        return comma(int(a)) + "." + b
    return comma(int(s))


def txt(x, y, t, anchor="middle", col=INK):
    return "<text x='%.1f' y='%.1f' font-size='13' text-anchor='%s' fill='%s'>%s</text>" % (x, y, anchor, col, t)


def semi_svg(w, h, kind):
    sc = min(200.0 / (w + h / 2.0), 120.0 / h)
    W, H = w * sc, h * sc
    x0, y0 = 55, 20
    s = ["<svg viewBox='0 0 330 %d' width='330' role='img' aria-label='composite figure'>" % (H + 60)]
    if kind == "semi":
        s.append("<path d='M%.1f %.1f L%.1f %.1f A%.1f %.1f 0 0 1 %.1f %.1f L%.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2'/>" % (x0, y0, x0 + W, y0, H / 2, H / 2, x0 + W, y0 + H, x0, y0 + H, FILL, INK))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-dasharray='4 3'/>" % (x0 + W, y0, x0 + W, y0 + H, INK))
    else:
        s.append("<path d='M%.1f %.1f L%.1f %.1f A%.1f %.1f 0 0 1 %.1f %.1f L%.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2'/>" % (x0, y0, x0 + W, y0, H, H, x0 + W + H, y0 + H, x0, y0 + H, FILL, INK))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-dasharray='4 3'/>" % (x0 + W, y0, x0 + W, y0 + H, INK))
    s.append(txt(x0 + W / 2, y0 + H + 18, "%s m" % g(w)))
    s.append(txt(x0 - 4, y0 + H / 2 + 4, "%s m" % g(h), "end"))
    s.append("</svg>")
    return fig("".join(s))


def one_semi(r):
    w, h = r.randint(5, 16), r.choice([2, 4, 6, 8, 10, 12])
    rad = h / 2.0
    A = w * h + 3.14 * rad * rad / 2
    pic = semi_svg(w, h, "semi")
    return mcq(pic + "The figure is a rectangle with a semicircle on one end. Find its area. Use 3.14 for π.", "%s m²" % g(A),
               ["%s m²" % g(w * h + 3.14 * rad * rad), "%s m²" % g(w * h + 3.14 * h * h / 2), "%s m²" % g(w * h + 3.14 * h / 2)],
               "Rectangle: %d × %d = %d. Semicircle: ½ × 3.14 × %s² = %s. Total = <b>%s m²</b>." % (w, h, w * h, g(rad), g(3.14 * rad * rad / 2), g(A)))


def one_quarter(r):
    w, h = r.randint(4, 14), r.choice([2, 3, 4, 5, 6, 8, 10])
    A = w * h + 3.14 * h * h / 4
    pic = semi_svg(w, h, "quarter")
    return mcq(pic + "The figure is a rectangle with a quarter circle of radius %d m on one end. Find its area. Use 3.14 for π." % h, "%s m²" % g(A),
               ["%s m²" % g(w * h + 3.14 * h * h), "%s m²" % g(w * h + 3.14 * h * h / 2), "%s m²" % g(w * h + 3.14 * (h / 2.0) ** 2 / 4)],
               "Rectangle: %d × %d = %d. Quarter circle: ¼ × 3.14 × %d² = %s. Total = <b>%s m²</b>." % (w, h, w * h, h, g(3.14 * h * h / 4), g(A)))


def house_svg(w, h, t):
    sc = min(180.0 / w, 150.0 / (h + t))
    W, H, Tt = w * sc, h * sc, t * sc
    x0, y0 = 70, 15 + Tt
    s = ["<svg viewBox='0 0 330 %d' width='330' role='img' aria-label='house shape'>" % (H + Tt + 50)]
    s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='2'/>" % (x0, y0, x0 + W / 2, y0 - Tt, x0 + W, y0, x0 + W, y0 + H, x0, y0 + H, FILL, INK))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-dasharray='4 3'/>" % (x0, y0, x0 + W, y0, INK))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#b45309' stroke-dasharray='3 3'/>" % (x0 + W / 2, y0, x0 + W / 2, y0 - Tt))
    s.append(txt(x0 + W / 2 + 6, y0 - Tt / 2 + 4, "%d ft" % t, "start", "#b45309"))
    s.append(txt(x0 + W / 2, y0 + H + 18, "%d ft" % w))
    s.append(txt(x0 + W + 6, y0 + H / 2 + 4, "%d ft" % h, "start"))
    s.append("</svg>")
    return fig("".join(s))


def one_house(r):
    w, h, t = r.choice([6, 8, 10, 12, 14, 16]), r.randint(4, 12), r.randint(2, 7)
    A = w * h + w * t / 2.0
    return mcq(house_svg(w, h, t) + "Find the area of the figure.", "%s ft²" % g(A), ["%s ft²" % g(w * h + w * t), "%s ft²" % g(w * h), "%s ft²" % g(w * h + t / 2.0)],
               "Rectangle: %d × %d = %d. Triangle: ½ × %d × %d = %s. Total = <b>%s ft²</b>." % (w, h, w * h, w, t, g(w * t / 2.0), g(A)))


def l_svg(W1, H1, cw, ch):
    sc = min(200.0 / W1, 150.0 / H1)
    a, b, c, d = W1 * sc, H1 * sc, cw * sc, ch * sc
    x0, y0 = 60, 15
    s = ["<svg viewBox='0 0 330 %d' width='330' role='img' aria-label='L-shaped figure'>" % (b + 50)]
    s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='2'/>" % (x0, y0, x0 + a - c, y0, x0 + a - c, y0 + d, x0 + a, y0 + d, x0 + a, y0 + b, x0, y0 + b, FILL, INK))
    s.append(txt(x0 + a / 2, y0 + b + 18, "%d cm" % W1))
    s.append(txt(x0 - 6, y0 + b / 2 + 4, "%d cm" % H1, "end"))
    s.append(txt(x0 + a - c / 2, y0 + d - 6, "%d cm" % cw))
    s.append(txt(x0 + a + 6, y0 + d / 2 + 4, "%d cm" % ch, "start"))
    s.append("</svg>")
    return fig("".join(s))


def one_l(r):
    W1, H1 = r.randint(8, 20), r.randint(6, 16)
    cw, ch = r.randint(2, W1 - 3), r.randint(2, H1 - 3)
    A = W1 * H1 - cw * ch
    return mcq(l_svg(W1, H1, cw, ch) + "A rectangle has a corner cut out. Find the area of the figure.", "%d cm²" % A, ["%d cm²" % (W1 * H1), "%d cm²" % (W1 * H1 + cw * ch), "%d cm²" % (2 * (W1 + H1))],
               "Big rectangle: %d × %d = %d. Cut out: %d × %d = %d. %d − %d = <b>%d cm²</b>." % (W1, H1, W1 * H1, cw, ch, cw * ch, W1 * H1, cw * ch, A))


def one_story(r):
    k = Kid(r).next()
    kind = r.choice(["track", "patio", "window", "yard"])
    if kind == "track":
        l, d = r.choice([40, 50, 60, 80]), r.choice([20, 30, 40])
        A = l * d + 3.14 * (d / 2.0) ** 2
        return mcq("A school field in Houston is a %d m by %d m rectangle with a semicircle on each short end. What is the area of the field? Use 3.14 for π." % (l, d), "%s m²" % g(A), ["%s m²" % g(l * d + 3.14 * d * d), "%s m²" % g(l * d), "%s m²" % g(l * d + 3.14 * (d / 2.0) ** 2 / 2)],
                   "Two semicircles make one circle with r = %d. %d × %d + 3.14 × %d² = %d + %s = <b>%s m²</b>." % (d // 2, l, d, d // 2, l * d, g(3.14 * (d / 2.0) ** 2), g(A)))
    if kind == "patio":
        s, c = r.choice([10, 12, 14, 16]), r.choice([2, 3, 4])
        A = s * s - c * c
        return mcq("%s's patio is a %d ft by %d ft square. A %d ft by %d ft square in the middle is a flower bed. How many square feet of the patio are paved?" % (k["n"], s, s, c, c), "%d ft²" % A, ["%d ft²" % (s * s), "%d ft²" % (s * s + c * c), "%d ft²" % (4 * s - 4 * c)],
                   "%d × %d − %d × %d = %d − %d = <b>%d ft²</b>." % (s, s, c, c, s * s, c * c, A))
    if kind == "window":
        w, h = r.choice([4, 6, 8]), r.choice([3, 4, 5, 6])
        A = w * h + 3.14 * (w / 2.0) ** 2 / 2
        return mcq("A window is a %d ft wide, %d ft tall rectangle with a semicircle on top. What is the area of the glass? Use 3.14 for π." % (w, h), "%s ft²" % g(A), ["%s ft²" % g(w * h + 3.14 * (w / 2.0) ** 2), "%s ft²" % g(w * h + 3.14 * w * w / 2), "%d ft²" % (w * h)],
                   "Rectangle: %d. Semicircle: ½ × 3.14 × %d² = %s. Total = <b>%s ft²</b>." % (w * h, w // 2, g(3.14 * (w / 2.0) ** 2 / 2), g(A)))
    b1, b2, h = r.choice([(20, 30, 12), (16, 24, 10), (30, 40, 15), (18, 26, 14)])
    A = (b1 + b2) * h / 2
    c = r.choice([2, 3])
    return mcq("A yard is a trapezoid with bases %d ft and %d ft and height %d ft. Sod costs $%d per square foot. How much does it cost to cover the yard?" % (b1, b2, h, c), "$%s" % comma(A * c), ["$%s" % comma((b1 + b2) * h * c), "$%s" % comma(A), "$%s" % comma((b1 + b2 + h) * c)],
               "A = ½ × (%d + %d) × %d = %d ft². %d × $%d = <b>$%s</b>." % (b1, b2, h, A, A, c, comma(A * c)))


def build():
    sets, R = build_sets([
        ("Triangles, trapezoids and simple composite shapes", [("run", asv.set_area, (), 20)]),
        ("House shapes and L-shapes", [("collect", one_house, 10), ("collect", one_l, 10)]),
        ("Rectangles with semicircles", [("collect", one_semi, 20)]),
        ("Rectangles with quarter circles", [("collect", one_quarter, 20)]),
        ("Word problems", [("collect", one_story, 20)]),
    ], 67013)
    finish(sets, R)
    body = lesson('<ul><li>Split a <b>composite figure</b> into shapes you know: rectangles, triangles, trapezoids, semicircles and quarter circles.</li><li>Find each area, then <b>add</b>. If a part is cut out, <b>subtract</b> it.</li><li>A semicircle is ½ of πr²; a quarter circle is ¼ of πr².</li><li>Check that every length you use matches the shape it belongs to.</li></ul>',
        [example("8 m × 6 m rectangle with a semicircle on the 6 m side", ["48 + ½ × 3.14 × 3²", "48 + 14.13"], "62.13 m²")],
        [['Using the whole circle', 'A semicircle is half: ½ × πr².'], ['Using the diameter as the radius', 'r = d ÷ 2.'], ['Adding a cut-out part', 'Subtract the part that is removed.']])
    faq = [('What does TEKS 7.9C ask?', 'Determine the area of composite figures containing combinations of rectangles, squares, parallelograms, trapezoids, triangles, semicircles and quarter circles.'), ('How do I know where to split the figure?', 'Draw lines that make shapes you have formulas for.'), ('Should I use 3.14 or 22/7?', 'Use what the problem says.'), ('What units does area use?', 'Square units, such as ft² or m².')]
    make('area-of-composite-figures', 13, 'Expressions, Equations and Relationships', '7.9C',
         '7.9C determine the area of composite figures containing combinations of rectangles, squares, parallelograms, trapezoids, triangles, semicircles, and quarter circles',
         'Area of Composite Figures', 'Area of Composite Figures',
         'Free Grade 7 worksheets for Texas TEKS 7.9C: area of composite figures with rectangles, triangles, trapezoids, semicircles and quarter circles, cut-out shapes and word problems. 100 questions with answers.',
         'Split into known shapes; add the parts and subtract the holes.', 'Semicircle = ½πr². Quarter circle = ¼πr².',
         body, faq, sets, seo_title='Grade 7 Area of Composite Figures Worksheets (TEKS 7.9C, STAAR)')


if __name__ == "__main__":
    build()
