# -*- coding: utf-8 -*-
"""
Texas Algebra I: Equations of Parallel and Perpendicular Lines (TEKS A.2E, A.2F, A.2G)
  python3 tools/gen_ustx_math_a1_parallel_perpendicular.py
Parallel and perpendicular slopes, parallel, perpendicular or neither, and equations of parallel and perpendicular
lines (US Geometry makers with a new seed), plus lines parallel or perpendicular to the axes (own maker).
Wrong answers come from real mistakes: using the same slope for perpendicular lines, forgetting to change the sign,
and writing x = a for a horizontal line.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_ge_slopes_of_parallel_and_perpendicular_lines as pp
adopt(pp)
pp.R = random.Random(695060)
tx_common.GRADE = "algebra-1"

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



AX = [("parallel to the <i>x</i>-axis", "y"), ("parallel to the <i>y</i>-axis", "x"), ("perpendicular to the <i>x</i>-axis", "x"), ("perpendicular to the <i>y</i>-axis", "y"),
      ("horizontal", "y"), ("vertical", "x")]


def one_axis(r):
    d, v = r.choice(AX)
    a, b = r.choice([n for n in range(-9, 10) if n]), r.choice([n for n in range(-9, 10) if n])
    if a == b or a == -b:
        raise AssertionError
    pt = "(%s, %s)" % (sg(a), sg(b))
    right = "<i>y</i> = %s" % sg(b) if v == "y" else "<i>x</i> = %s" % sg(a)
    w = ["<i>x</i> = %s" % sg(a), "<i>y</i> = %s" % sg(b), "<i>y</i> = %s" % sg(a), "<i>x</i> = %s" % sg(b)]
    w = [x for x in w if x != right][:3]
    why = "A horizontal line has the same <i>y</i>-value everywhere" if v == "y" else "A vertical line has the same <i>x</i>-value everywhere"
    return mcq("Write the equation of the line through %s that is %s." % (pt, d), right, w, "%s, so the line is <b>%s</b>." % (why, right))


def build():
    sets, R = build_sets([
        ("Parallel and perpendicular slopes", [("collect", W(pp.one_sl), 20)]),
        ("Parallel, perpendicular or neither", [("collect", W(pp.one_cls), 20)]),
        ("Equations of parallel lines", [("collect", W(pp.one_par), 20)]),
        ("Equations of perpendicular lines", [("collect", W(pp.one_perp), 20)]),
        ("Lines parallel or perpendicular to an axis", [("collect", uniq(one_axis), 20)]),
    ], 69506)
    finish(sets, R)
    body = lesson("<ul><li><b>Parallel</b> lines have the <b>same slope</b>.</li><li><b>Perpendicular</b> lines have slopes that are <b>opposite reciprocals</b>: 2 and −<span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>.</li><li>Use the new slope and the given point in point-slope form.</li><li>A line parallel to the <i>x</i>-axis is horizontal: <i>y</i> = <i>b</i>. A line parallel to the <i>y</i>-axis is vertical: <i>x</i> = <i>a</i>.</li></ul>",
        [example("Perpendicular to <i>y</i> = 2<i>x</i> + 1 through (4, 3)", ["slope −1/2", "3 = −1/2(4) + <i>b</i>, <i>b</i> = 5"], "<i>y</i> = −1/2<i>x</i> + 5")],
        [['Same slope for perpendicular lines', 'Flip the fraction and change the sign.'], ['Forgetting to change the sign', 'The reciprocal of 3 for a perpendicular line is −1/3.'], ['Writing <i>x</i> = <i>a</i> for a horizontal line', 'Horizontal lines are <i>y</i> = <i>b</i>.']])
    faq = [('What does TEKS A.2E ask?', 'Write the equation of a line that contains a given point and is parallel to a given line.'), ('What does TEKS A.2F ask?', 'Write the equation of a line that contains a given point and is perpendicular to a given line.'), ('What does TEKS A.2G ask?', 'Write an equation of a line that is parallel or perpendicular to the x- or y-axis and determine whether the slope of the line is zero or undefined.'), ('What is the slope of a line parallel to the y-axis?', 'Undefined.')]
    make('parallel-and-perpendicular-lines', 6, 'Linear Functions, Equations, and Inequalities', 'A.2E, A.2F, A.2G',
         'A.2E write the equation of a line that contains a given point and is parallel to a given line; A.2F write the equation of a line that contains a given point and is perpendicular to a given line; A.2G write an equation of a line that is parallel or perpendicular to the x- or y-axis and determine whether the slope of the line is zero or undefined',
         'Equations of Parallel and Perpendicular Lines', 'Parallel and Perpendicular Lines',
         'Free Algebra I worksheets for Texas TEKS A.2E, A.2F and A.2G: parallel and perpendicular slopes, equations of parallel and perpendicular lines and lines parallel to the axes. 100 questions with answers.',
         'Parallel: same slope. Perpendicular: opposite reciprocal.', 'Slopes 2 and −1/2 are perpendicular.',
         body, faq, sets, seo_title='Algebra I Parallel and Perpendicular Lines Worksheets (TEKS A.2E, A.2F)')


if __name__ == "__main__":
    build()
