# -*- coding: utf-8 -*-
"""
Texas Geometry: Equations of Circles (TEKS G.12E)
  python3 tools/gen_ustx_math_ge_circle_equations.py
Writing the equation, finding the center and radius, completing the square, circles from a point or a diameter, and
graphs and points (the US Geometry makers with a new seed).
Wrong answers come from real mistakes: the wrong signs for h and k, writing r instead of r², and forgetting to add to
both sides when completing the square.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_ge_equations_of_circles as ec
adopt(ec)
ec.R = random.Random(696260)
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
        ("Write the equation", [("collect", W(ec.one_write), 20)]),
        ("Find the center and radius", [("collect", W(ec.one_read), 20)]),
        ("Complete the square", [("collect", W(ec.one_cs), 20)]),
        ("From a point or a diameter", [("collect", W(ec.one_pt), 20)]),
        ("Graphs, points and problems", [("collect", W(ec.one_mix), 20)]),
    ], 69626)
    finish(sets, R)
    body = lesson('<ul><li>A circle with center (<i>h</i>, <i>k</i>) and radius <i>r</i>: (<i>x</i> − <i>h</i>)<sup>2</sup> + (<i>y</i> − <i>k</i>)<sup>2</sup> = <i>r</i><sup>2</sup>.</li><li>Center at the origin: <i>x</i><sup>2</sup> + <i>y</i><sup>2</sup> = <i>r</i><sup>2</sup>. This comes from the distance formula.</li><li>To read the center, change the signs inside the parentheses.</li></ul>',
        [example("Center (2, −5), radius 4", ["(<i>x</i> − 2)<sup>2</sup> + (<i>y</i> + 5)<sup>2</sup>"], "= 16")],
        [['Wrong signs for <i>h</i> and <i>k</i>', '(<i>x</i> + 3) means <i>h</i> = −3.'], ['Writing <i>r</i> instead of <i>r</i><sup>2</sup>', 'The right side is <i>r</i><sup>2</sup>.'], ['Adding to only one side', 'Complete the square on both sides.']])
    faq = [('What does TEKS G.12E ask?', 'Show that the equation of a circle with center at the origin and radius r is x<sup>2</sup> + y<sup>2</sup> = r<sup>2</sup> and determine the equation for the graph of a circle with radius r and center (h, k), (x − h)<sup>2</sup> + (y − k)<sup>2</sup> = r<sup>2</sup>.'), ('Why is it r²?', 'It comes from the distance formula squared.'), ('How do I find the radius from a diameter?', 'Halve the distance between the endpoints.'), ('Is a point on the circle?', 'Check whether it makes the equation true.')]
    make('equations-of-circles', 26, 'Circles', 'G.12E',
         'G.12E show that the equation of a circle with center at the origin and radius r is x^2 + y^2 = r^2 and determine the equation for the graph of a circle with radius r and center (h, k), (x − h)^2 + (y − k)^2 = r^2',
         'Equations of Circles', 'Equations of Circles',
         'Free Geometry worksheets for Texas TEKS G.12E: write equations of circles, find the center and radius, complete the square and use points and diameters. 100 questions with answers.',
         '(x − h)² + (y − k)² = r²', 'Center (2, −5), r = 4: (x − 2)² + (y + 5)² = 16',
         body, faq, sets, seo_title='Geometry Equations of Circles Worksheets (TEKS G.12E)')


if __name__ == "__main__":
    build()
