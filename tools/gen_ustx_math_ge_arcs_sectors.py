# -*- coding: utf-8 -*-
"""
Texas Geometry: Arc Length, Sector Area and Radians (TEKS G.12B, G.12C, G.12D)
  python3 tools/gen_ustx_math_ge_arcs_sectors.py
Arc length, the area of a sector, radians, perimeter and finding the angle, and arc and sector problems (the US
Geometry makers with a new seed and Texas names).
Wrong answers come from real mistakes: using the area formula for arc length, using the diameter as the radius, and
multiplying by 180/π the wrong way.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_ge_arc_length_and_sector_area as al
adopt(al)
al.R = random.Random(696250)
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


def build():
    sets, R = build_sets([
        ("Arc length", [("collect", W(al.one_arc), 20)]),
        ("Area of a sector", [("collect", W(al.one_area), 20)]),
        ("Radians", [("collect", W(al.one_radian), 20)]),
        ("Perimeter and finding the angle", [("collect", W(al.one_perim), 20)]),
        ("Arc and sector problems", [("run", PR(al.problems), ("rnd",), 10), ("collect", W(al.one_area), 10)]),
    ], 69625)
    finish(sets, R)
    body = lesson("<ul><li>Arc length = <span class='fr'><span class='fn'>θ</span><span class='fd'>360</span></span> × 2π<i>r</i>.</li><li>Sector area = <span class='fr'><span class='fn'>θ</span><span class='fd'>360</span></span> × π<i>r</i><sup>2</sup>.</li><li>A <b>radian</b> is the angle whose arc equals the radius: θ = arc length ÷ radius. 180° = π radians.</li></ul>",
        [example("Radius 9, angle 80°", ["80/360 × 2π × 9"], "arc length 4π")],
        [['Using the area formula for arcs', 'Arcs use 2π<i>r</i>.'], ['Using the diameter', 'Use the radius.'], ['Converting the wrong way', 'Degrees to radians: × π/180.']])
    faq = [('What does TEKS G.12B ask?', 'Apply the proportional relationship between the measure of an arc length of a circle and the circumference of the circle to solve problems.'), ('What does TEKS G.12C ask?', 'Apply the proportional relationship between the measure of the area of a sector of a circle and the area of the circle to solve problems.'), ('What does TEKS G.12D ask?', 'Describe radian measure of an angle as the ratio of the length of an arc intercepted by a central angle and the radius of the circle.'), ('How many radians are in a full circle?', '2π.')]
    make('arc-length-sector-area-and-radians', 25, 'Circles', 'G.12B, G.12C, G.12D',
         'G.12B apply the proportional relationship between the measure of an arc length of a circle and the circumference of the circle to solve problems; G.12C apply the proportional relationship between the measure of the area of a sector of a circle and the area of the circle to solve problems; G.12D describe radian measure of an angle as the ratio of the length of an arc intercepted by a central angle and the radius of the circle',
         'Arc Length, Sector Area and Radians', 'Arc Length, Sector Area and Radians',
         'Free Geometry worksheets for Texas TEKS G.12B–G.12D: arc length, sector area, radians and sector problems. 100 questions with answers.',
         'A fraction of the circle: θ/360.', '180° = π radians.',
         body, faq, sets, seo_title='Geometry Arc Length, Sector Area and Radians Worksheets (TEKS G.12B)')


if __name__ == "__main__":
    build()
