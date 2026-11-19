# -*- coding: utf-8 -*-
"""
Texas Geometry: Parallelograms, Special Quadrilaterals and Polygon Angles (TEKS G.6E, G.5A)
  python3 tools/gen_ustx_math_ge_quadrilaterals.py
Angles of polygons, properties of parallelograms, rectangles, rhombuses and squares, trapezoids and kites, and
classifying and proving (the US Geometry makers with a new seed and Texas names).
Wrong answers come from real mistakes: using 180n instead of 180(n − 2), thinking all parallelogram diagonals are
equal, and calling every rhombus a square.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_ge_polygons_and_quadrilaterals as pq
adopt(pq)
pq.R = random.Random(696130)
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
        ("Interior and exterior angles of polygons", [("collect", W(pq.one_poly), 20)]),
        ("Properties of parallelograms", [("collect", W(pq.one_pg), 20)]),
        ("Rectangles, rhombuses and squares", [("collect", W(pq.one_spec), 20)]),
        ("Trapezoids and kites", [("collect", W(pq.one_trap), 20)]),
        ("Classify and prove", [("collect", W(pq.one_cls), 20)]),
    ], 69613)
    finish(sets, R)
    body = lesson('<ul><li>Interior angles of an <i>n</i>-gon add to 180°(<i>n</i> − 2). Exterior angles add to 360°.</li><li><b>Parallelogram</b>: opposite sides and angles are congruent; diagonals bisect each other.</li><li><b>Rectangle</b>: congruent diagonals. <b>Rhombus</b>: perpendicular diagonals. <b>Square</b>: both.</li><li>To prove a parallelogram: both pairs of opposite sides congruent or parallel, or diagonals bisect each other.</li></ul>',
        [example("Interior angle of a regular octagon", ["180 × 6 = 1080", "1080 ÷ 8"], "135°")],
        [['Using 180<i>n</i>', 'The sum is 180(<i>n</i> − 2).'], ['Thinking every parallelogram has equal diagonals', 'Only rectangles do.'], ['Calling every rhombus a square', 'A square also needs right angles.']])
    faq = [('What does TEKS G.6E ask?', 'Prove a quadrilateral is a parallelogram, rectangle, square, or rhombus using opposite sides, opposite angles, or diagonals and apply these relationships to solve problems.'), ('Is a square a rhombus?', 'Yes.'), ('What is the exterior angle of a regular hexagon?', '60°.'), ("Do a kite's diagonals bisect each other?", 'No, only one is bisected.')]
    make('quadrilaterals-and-polygon-angles', 13, 'Proof and Congruence', 'G.6E, G.5A',
         'G.6E prove a quadrilateral is a parallelogram, rectangle, square, or rhombus using opposite sides, opposite angles, or diagonals and apply these relationships to solve problems; G.5A investigate patterns to make conjectures about geometric relationships, including diagonals of quadrilaterals and interior and exterior angles of polygons',
         'Parallelograms, Special Quadrilaterals and Polygon Angles', 'Quadrilaterals and Polygons',
         'Free Geometry worksheets for Texas TEKS G.6E and G.5A: polygon angle sums, parallelograms, rectangles, rhombuses, squares, trapezoids and kites. 100 questions with answers.',
         'Interior sum 180(n − 2); exterior sum 360°.', 'Rhombus diagonals are perpendicular; rectangle diagonals are equal.',
         body, faq, sets, seo_title='Geometry Quadrilaterals and Polygon Angles Worksheets (TEKS G.6E)')


if __name__ == "__main__":
    build()
