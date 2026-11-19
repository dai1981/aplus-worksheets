# -*- coding: utf-8 -*-
"""
Texas Algebra I: Writing Linear Equations: Slope-Intercept, Point-Slope and Standard Form (TEKS A.2B, A.2C)
  python3 tools/gen_ustx_math_a1_writing_linear.py
Slope-intercept form from two points, point-slope form, from tables, converting standard form, and linear models
(US Algebra 1 and Grade 8 makers with a new seed and Texas names).
Wrong answers come from real mistakes: using the point's x-value as b, the wrong sign in point-slope form, and
dividing only one term when solving for y.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a1_forms_of_linear_equations as fl
adopt(fl)
fl.R = random.Random(695050)
import gen_us_math_g8_linear_functions as lf
adopt(lf)
lf.R = random.Random(695051)
import gen_us_math_a1_literal_equations as le
adopt(le)
le.R = random.Random(695052)
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


def build():
    sets, R = build_sets([
        ("Slope-intercept form from two points", [("collect", W(fl.one_si), 20)]),
        ("Point-slope form", [("collect", W(fl.one_ps), 20)]),
        ("From two points and tables", [("run", lf.set_points, (), 20)]),
        ("Standard form to slope-intercept form", [("collect", W(le.one_std), 20)]),
        ("Write a linear model", [("run", PR(fl.problems), ("rnd",), 10), ("run", lf.set_story, (), 10)]),
    ], 69505)
    finish(sets, R)
    body = lesson('<ul><li><b>Slope-intercept</b>: <i>y</i> = <i>mx</i> + <i>b</i>. Find <i>m</i>, then put a point in to find <i>b</i>.</li><li><b>Point-slope</b>: <i>y</i> − <i>y</i><sub>1</sub> = <i>m</i>(<i>x</i> − <i>x</i><sub>1</sub>).</li><li><b>Standard</b>: <i>Ax</i> + <i>By</i> = <i>C</i>. Solve for <i>y</i> to get slope-intercept form.</li></ul>',
        [example("Through (2, 7) with slope 3", ["7 = 3(2) + <i>b</i>", "<i>b</i> = 1"], "<i>y</i> = 3<i>x</i> + 1")],
        [["Using the point's <i>x</i> as <i>b</i>", '<i>b</i> is where <i>x</i> = 0.'], ['Wrong sign in point-slope form', 'Through (2, −5): <i>y</i> + 5 = <i>m</i>(<i>x</i> − 2).'], ['Dividing only one term', 'Divide every term by <i>B</i>.']])
    faq = [('What does TEKS A.2B ask?', 'Write linear equations in two variables in various forms, including y = mx + b, Ax + By = C, and y − y<sub>1</sub> = m(x − x<sub>1</sub>), given one point and the slope and given two points.'), ('What does TEKS A.2C ask?', 'Write linear equations in two variables given a table of values, a graph, and a verbal description.'), ('Which form is best?', 'Point-slope when you know a point and slope; slope-intercept for graphing.'), ('Are the forms the same line?', 'Yes, if they are rewritten correctly.')]
    make('writing-linear-equations', 5, 'Linear Functions, Equations, and Inequalities', 'A.2B, A.2C',
         'A.2B write linear equations in two variables in various forms, including y = mx + b, Ax + By = C, and y − y1 = m(x − x1), given one point and the slope and given two points; A.2C write linear equations in two variables given a table of values, a graph, and a verbal description',
         'Writing Linear Equations: Slope-Intercept, Point-Slope and Standard Form', 'Writing Linear Equations',
         'Free Algebra I worksheets for Texas TEKS A.2B and A.2C: write linear equations in slope-intercept, point-slope and standard form from points, tables and words. 100 questions with answers.',
         'Find the slope, then use a point.', 'y − y₁ = m(x − x₁)',
         body, faq, sets, seo_title='Algebra I Writing Linear Equations Worksheets (TEKS A.2B, A.2C)')


if __name__ == "__main__":
    build()
