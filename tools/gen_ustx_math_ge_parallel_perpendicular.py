# -*- coding: utf-8 -*-
"""
Texas Geometry: Equations of Parallel and Perpendicular Lines (TEKS G.2C)
  python3 tools/gen_ustx_math_ge_parallel_perpendicular.py
Parallel and perpendicular slopes, parallel, perpendicular or neither, and equations of parallel and perpendicular
lines (the US Geometry makers with a new seed).
Wrong answers come from real mistakes: the same slope for perpendicular lines, forgetting to change the sign, and
using the point's x-value as the y-intercept.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_ge_slopes_of_parallel_and_perpendicular_lines as sl
adopt(sl)
sl.R = random.Random(696050)
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
        ("Parallel and perpendicular slopes", [("collect", W(sl.one_sl), 20)]),
        ("Parallel, perpendicular or neither", [("collect", W(sl.one_cls), 20)]),
        ("Equations of parallel lines", [("collect", W(sl.one_par), 20)]),
        ("Equations of perpendicular lines", [("collect", W(sl.one_perp), 20)]),
        ("Mixed practice", [("collect", W(sl.one_par), 10), ("collect", W(sl.one_perp), 10)]),
    ], 69605)
    finish(sets, R)
    body = lesson('<ul><li>Parallel lines: <b>same slope</b>.</li><li>Perpendicular lines: slopes are <b>opposite reciprocals</b> (their product is −1).</li><li>Use the slope and the point in <i>y</i> − <i>y</i><sub>1</sub> = <i>m</i>(<i>x</i> − <i>x</i><sub>1</sub>), then simplify.</li></ul>',
        [example("Parallel to <i>y</i> = 3<i>x</i> − 1 through (2, 4)", ["4 = 3(2) + <i>b</i>", "<i>b</i> = −2"], "<i>y</i> = 3<i>x</i> − 2")],
        [['Same slope for perpendicular lines', 'Flip and change the sign.'], ['Not changing the sign', 'Perpendicular to 2 is −1/2.'], ['Using <i>x</i> as the intercept', 'Solve for <i>b</i>.']])
    faq = [('What does TEKS G.2C ask?', 'Determine an equation of a line parallel or perpendicular to a given line that passes through a given point.'), ('What is perpendicular to a horizontal line?', 'A vertical line.'), ('What is the product of perpendicular slopes?', '−1.'), ('Do parallel lines have the same y-intercept?', 'No, or they would be the same line.')]
    make('equations-of-parallel-and-perpendicular-lines', 5, 'Coordinate and Transformational Geometry', 'G.2C',
         'G.2C determine an equation of a line parallel or perpendicular to a given line that passes through a given point',
         'Equations of Parallel and Perpendicular Lines', 'Parallel and Perpendicular Lines',
         'Free Geometry worksheets for Texas TEKS G.2C: parallel and perpendicular slopes and equations of parallel and perpendicular lines through a point. 100 questions with answers.',
         'Parallel: same slope. Perpendicular: opposite reciprocal.', 'Parallel to y = 3x − 1 through (2, 4): y = 3x − 2',
         body, faq, sets, seo_title='Geometry Equations of Parallel and Perpendicular Lines Worksheets (TEKS G.2C)')


if __name__ == "__main__":
    build()
