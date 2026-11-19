# -*- coding: utf-8 -*-
"""
Texas Geometry: Area of Regular Polygons and Composite Figures (TEKS G.11A, G.11B)
  python3 tools/gen_ustx_math_ge_area.py
The area of regular polygons with the apothem, finding the apothem or side from the area (own makers), and areas of
trapezoids, kites, composite figures and figures with a piece removed (Australian Year 8 makers with a new seed and US
spelling).
Wrong answers come from real mistakes: using the side instead of the perimeter, forgetting the 1/2, and adding the
hole instead of subtracting it.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_au_maths_y8_area_and_perimeter_of_composite_shapes as ca
adopt(ca)
ca.R = random.Random(696210)
import au_hs
adopt(au_hs)
tx_common.GRADE = "geometry"

import us_hs
adopt(us_hs)


def W(fn, keep=None):
    """Use an item maker of another generator: its odd failures count as a skipped try, and a question text
    is used only once (not again with other wrong answers)."""
    seen = set()

    def f(r):
        try:
            it = fn(r)
        except (TypeError, ValueError, ZeroDivisionError, IndexError, KeyError):
            raise AssertionError("skip")
        if not it or (keep and not keep(it)) or it["q"] in seen:
            raise AssertionError("skip")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


def PR(fn, keep=None):
    """A fixed word-problem list of another generator as a set maker: a shuffled share of it."""
    def f(r):
        its = [it for it in fn() if keep is None or keep(it)]
        r.shuffle(its)
        return {"title": fn.__name__, "items": its * 3}
    f.__name__ = fn.__name__
    return f


MINUS = "−"
X = "<i>x</i>"


def sg(v):
    return ("−%s" % abs(v)) if v < 0 else str(v)


def poly(cs, v="<i>x</i>"):
    """[a, b, c] highest power first, e.g. 2x² − 3x + 1."""
    deg = len(cs) - 1
    out = ""
    for i, c in enumerate(cs):
        if c == 0:
            continue
        p = deg - i
        mag = abs(c)
        if p == 0:
            body = str(mag)
        else:
            body = ("" if mag == 1 else str(mag)) + v + ("<sup>%d</sup>" % p if p > 1 else "")
        if not out:
            out = (MINUS if c < 0 else "") + body
        else:
            out += (" − " if c < 0 else " + ") + body
    return out or "0"
def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


POLY = [(5, "pentagon"), (6, "hexagon"), (8, "octagon"), (10, "decagon"), (12, "dodecagon"), (3, "triangle"), (4, "square"), (9, "nonagon")]


def g1(v):
    s = ("%.1f" % v).rstrip("0").rstrip(".")
    return comma(int(s)) if "." not in s else s


def one_reg(r):
    n, name = r.choice(POLY)
    s = r.randint(4, 20)
    a = r.choice([x / 10 for x in range(25, 200, 5)])
    P = n * s
    area = 0.5 * a * P
    nm = "regular " + name if name not in ("square",) else "square"
    w = ["%s square units" % g1(a * P), "%s square units" % g1(0.5 * a * s), "%s square units" % g1(a * s)]
    return mcq("A %s has side length %d and apothem %s. What is its area?" % (nm, s, g1(a)), "%s square units" % g1(area), w,
               "<i>A</i> = ½<i>aP</i>. <i>P</i> = %d × %d = %d. <i>A</i> = ½ × %s × %d = <b>%s square units</b>." % (n, s, P, g1(a), P, g1(area)))


def one_back(r):
    n, name = r.choice(POLY[:5])
    s = r.randint(4, 16)
    a = r.randint(3, 18)
    P = n * s
    A = a * P / 2
    if r.random() < 0.5:
        w = [str(a * 2), str(int(A / s)) if A % s == 0 else str(a + 2), str(int(A / P))]
        return mcq("A regular %s has side length %d and area %s square units. What is its apothem?" % (name, s, g1(A)), str(a), w,
                   "%s = ½ × <i>a</i> × %d, so <i>a</i> = 2 × %s ÷ %d = <b>%d</b>." % (g1(A), P, g1(A), P, a))
    w = [str(P * 2), str(s), str(int(A / a))]
    return mcq("A regular %s has apothem %d and area %s square units. What is its perimeter?" % (name, a, g1(A)), str(P), w,
               "%s = ½ × %d × <i>P</i>, so <i>P</i> = 2 × %s ÷ %d = <b>%d</b>." % (g1(A), a, g1(A), a, P))


def build():
    sets, R = build_sets([
        ("Area of regular polygons", [("collect", uniq(one_reg), 20)]),
        ("Find the apothem or perimeter", [("collect", uniq(one_back), 20)]),
        ("Trapezoids, rhombuses and kites", [("collect", W(ca.one_trap), 14), ("collect", uniq(one_reg), 6)]),
        ("Area of composite figures", [("collect", W(ca.one_comp), 20)]),
        ("Figures with a piece removed", [("collect", W(ca.one_hole), 20)]),
    ], 69621)
    finish(sets, R)
    body = lesson('<ul><li>Area of a <b>regular polygon</b>: <i>A</i> = ½<i>aP</i>, where <i>a</i> is the apothem and <i>P</i> the perimeter.</li><li>The <b>apothem</b> goes from the center to the middle of a side, at a right angle.</li><li>Trapezoid: ½(<i>b</i><sub>1</sub> + <i>b</i><sub>2</sub>)<i>h</i>. Kite or rhombus: ½<i>d</i><sub>1</sub><i>d</i><sub>2</sub>.</li><li><b>Composite figures</b>: split into simple shapes and add; subtract any holes.</li></ul>',
        [example("Regular hexagon, side 10, apothem 8.7", ["<i>P</i> = 60", "½ × 8.7 × 60"], "261 square units")],
        [['Using the side instead of the perimeter', '<i>P</i> = <i>n</i> × side.'], ['Forgetting ½', '<i>A</i> = ½<i>aP</i>.'], ['Adding a hole', 'Subtract the cut-out part.']])
    faq = [('What does TEKS G.11A ask?', 'Apply the formula for the area of regular polygons to solve problems using appropriate units of measure.'), ('What does TEKS G.11B ask?', 'Determine the area of composite two-dimensional figures comprised of a combination of triangles, parallelograms, trapezoids, kites, regular polygons, or sectors of circles to solve problems using appropriate units of measure.'), ('What is an apothem?', 'The distance from the center of a regular polygon to the midpoint of a side.'), ('What units does area use?', 'Square units, such as cm² or ft².')]
    make('area-of-regular-polygons-and-composite-figures', 21, 'Two-Dimensional and Three-Dimensional Figures', 'G.11A, G.11B',
         'G.11A apply the formula for the area of regular polygons to solve problems using appropriate units of measure; G.11B determine the area of composite two-dimensional figures comprised of a combination of triangles, parallelograms, trapezoids, kites, regular polygons, or sectors of circles to solve problems using appropriate units of measure',
         'Area of Regular Polygons and Composite Figures', 'Area of Regular Polygons and Composite Figures',
         'Free Geometry worksheets for Texas TEKS G.11A and G.11B: area of regular polygons with the apothem, trapezoids, kites and composite figures. 100 questions with answers.',
         'Regular polygon: A = ½aP.', 'Composite: add the parts, subtract the holes.',
         body, faq, sets, seo_title='Geometry Area of Regular Polygons and Composite Figures Worksheets (TEKS G.11A)')


if __name__ == "__main__":
    build()
