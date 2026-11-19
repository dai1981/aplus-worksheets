# -*- coding: utf-8 -*-
"""
Texas Geometry: Distance, Slope and Midpoint Formulas (TEKS G.2B)
  python3 tools/gen_ustx_math_ge_coordinate_formulas.py
The distance formula, distances in radical form, missing endpoints, perimeter and area on the coordinate plane, and
proving relationships with slopes (the US Geometry makers with a new seed and Texas names).
Wrong answers come from real mistakes: forgetting to square, subtracting in a different order, and adding the
coordinates instead of averaging them.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_ge_distance_and_midpoint_formulas as dm
adopt(dm)
dm.R = random.Random(696040)
import gen_us_math_ge_slopes_of_parallel_and_perpendicular_lines as sl
adopt(sl)
sl.R = random.Random(696041)
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
        ("The distance formula", [("collect", W(dm.one_dist), 20)]),
        ("Distances in radical form", [("collect", W(dm.one_rad), 20)]),
        ("Missing endpoints", [("collect", W(dm.one_end), 20)]),
        ("Perimeter and area on the coordinate plane", [("collect", W(dm.one_poly), 20)]),
        ("Verify relationships with slopes", [("collect", W(sl.one_proof), 20)]),
    ], 69604)
    finish(sets, R)
    body = lesson("<ul><li><b>Distance</b>: <i>d</i> = √((<i>x</i><sub>2</sub> − <i>x</i><sub>1</sub>)<sup>2</sup> + (<i>y</i><sub>2</sub> − <i>y</i><sub>1</sub>)<sup>2</sup>).</li><li><b>Slope</b>: (<i>y</i><sub>2</sub> − <i>y</i><sub>1</sub>) ÷ (<i>x</i><sub>2</sub> − <i>x</i><sub>1</sub>). Equal slopes: parallel. Product −1: perpendicular.</li><li><b>Midpoint</b>: average the <i>x</i>'s and the <i>y</i>'s.</li><li>Use them to show segments are congruent or lines are parallel or perpendicular.</li></ul>",
        [example("(1, 2) and (7, 10)", ["√(36 + 64)"], "10")],
        [['Forgetting to square', 'Square each difference first.'], ['Subtracting in different orders', 'Use the same point first.'], ['Adding instead of averaging', 'Divide the sum by 2.']])
    faq = [('What does TEKS G.2B ask?', 'Derive and use the distance, slope, and midpoint formulas to verify geometric relationships, including congruence of segments and parallelism or perpendicularity of pairs of lines.'), ('Where does the distance formula come from?', 'The Pythagorean Theorem.'), ('How do I show a quadrilateral is a parallelogram?', 'Show both pairs of opposite sides have equal slopes.'), ('How do I show segments are congruent?', 'Show they have the same length.')]
    make('distance-slope-and-midpoint-formulas', 4, 'Coordinate and Transformational Geometry', 'G.2B',
         'G.2B derive and use the distance, slope, and midpoint formulas to verify geometric relationships, including congruence of segments and parallelism or perpendicularity of pairs of lines',
         'Distance, Slope and Midpoint Formulas', 'Distance, Slope and Midpoint',
         'Free Geometry worksheets for Texas TEKS G.2B: the distance, slope and midpoint formulas, radical distances, missing endpoints and coordinate proofs. 100 questions with answers.',
         'Distance comes from the Pythagorean Theorem.', '(1, 2) to (7, 10): √(36 + 64) = 10',
         body, faq, sets, seo_title='Geometry Distance, Slope and Midpoint Formulas Worksheets (TEKS G.2B)')


if __name__ == "__main__":
    build()
