# -*- coding: utf-8 -*-
"""
Texas Algebra I: Graphing Linear Functions: Intercepts, Zeros and Slope (TEKS A.3C)
  python3 tools/gen_ustx_math_a1_graphing_linear.py
Matching graphs and equations, tables, the meaning of slope and intercept (US Grade 8 makers with a new seed),
standard form and intercepts (US Algebra 1 maker), and linear stories.
Wrong answers come from real mistakes: mixing up the x- and y-intercepts, plotting the slope as the intercept, and
forgetting that a zero is an x-intercept.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g8_linear_functions as lf
adopt(lf)
lf.R = random.Random(695040)
import gen_us_math_a1_forms_of_linear_equations as fl
adopt(fl)
fl.R = random.Random(695041)
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
        ("Match the graph and the equation", [("run", lf.set_graph, (), 20)]),
        ("Tables and graphs", [("run", lf.set_tables, (), 20)]),
        ("Standard form, intercepts and zeros", [("collect", W(fl.one_std), 20)]),
        ("What the slope and intercept mean", [("run", lf.set_meaning, (), 20)]),
        ("Linear stories", [("run", lf.set_story, (), 20)]),
    ], 69504)
    finish(sets, R)
    body = lesson('<ul><li>In <i>y</i> = <i>mx</i> + <i>b</i>, start at the <b><i>y</i>-intercept</b> (0, <i>b</i>) and move by the slope <i>m</i>.</li><li>The <b><i>x</i>-intercept</b> is where <i>y</i> = 0. It is also the <b>zero</b> of the function.</li><li>For <i>Ax</i> + <i>By</i> = <i>C</i>, put <i>x</i> = 0 to find the <i>y</i>-intercept and <i>y</i> = 0 to find the <i>x</i>-intercept.</li></ul>',
        [example("3<i>x</i> + 2<i>y</i> = 12", ["<i>x</i> = 0: <i>y</i> = 6", "<i>y</i> = 0: <i>x</i> = 4"], "intercepts (0, 6) and (4, 0); zero 4")],
        [['Mixing up the intercepts', 'The <i>x</i>-intercept has <i>y</i> = 0.'], ['Plotting the slope as the intercept', 'Start at <i>b</i>, then use <i>m</i>.'], ['Forgetting the zero', 'The zero is the <i>x</i>-intercept.']])
    faq = [('What does TEKS A.3C ask?', 'Graph linear functions on the coordinate plane and identify key features, including x-intercept, y-intercept, zeros, and slope, in mathematical and real-world problems.'), ('What is a zero of a function?', 'An input that gives an output of 0.'), ('How many zeros does a non-horizontal line have?', 'Exactly one.'), ('What does the y-intercept mean in a story?', 'The starting value.')]
    make('graphing-linear-functions', 4, 'Linear Functions, Equations, and Inequalities', 'A.3C',
         'A.3C graph linear functions on the coordinate plane and identify key features, including x-intercept, y-intercept, zeros, and slope, in mathematical and real-world problems',
         'Graphing Linear Functions: Intercepts, Zeros and Slope', 'Graphing Linear Functions',
         'Free Algebra I worksheets for Texas TEKS A.3C: graph linear functions, find x- and y-intercepts and zeros, read slope and intercept in context. 100 questions with answers.',
         'Start at the y-intercept, then move by the slope.', 'The zero is the x-intercept.',
         body, faq, sets, seo_title='Algebra I Graphing Linear Functions Worksheets (TEKS A.3C)')


if __name__ == "__main__":
    build()
