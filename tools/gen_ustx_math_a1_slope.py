# -*- coding: utf-8 -*-
"""
Texas Algebra I: Slope and Rate of Change (TEKS A.3A, A.3B)
  python3 tools/gen_ustx_math_a1_slope.py
Slope from graphs, two points, tables and equations, and slope ideas (US Grade 8 makers with a new seed), plus rate of
change over an interval in real situations (own maker).
Wrong answers come from real mistakes: flipping rise and run, subtracting in different orders, and dividing the
outputs instead of their change.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g8_slope as sl
adopt(sl)
sl.R = random.Random(695030)
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



CTX = [("A tank holds {a} gallons at {x1} minutes and {b} gallons at {x2} minutes.", "gallons per minute"),
       ("A plant is {a} cm tall on day {x1} and {b} cm tall on day {x2}.", "cm per day"),
       ("A phone plan costs ${a} for {x1} GB and ${b} for {x2} GB.", "dollars per GB"),
       ("A hiker is at {a} feet above sea level after {x1} hours and {b} feet after {x2} hours.", "feet per hour"),
       ("A savings account has ${a} after {x1} weeks and ${b} after {x2} weeks.", "dollars per week"),
       ("A candle is {a} cm tall after {x1} hours and {b} cm tall after {x2} hours.", "cm per hour")]


def one_rate(r):
    t, unit = r.choice(CTX)
    x1 = r.randint(1, 5)
    x2 = x1 + r.randint(2, 6)
    m = r.choice([-6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 8, 10, 12, 15])
    if "candle" in t:
        m = -abs(m)
    a = r.randint(20, 90)
    b = a + m * (x2 - x1)
    if b < 0:
        raise AssertionError
    q = t.format(a=a, b=b, x1=x1, x2=x2) + " What is the average rate of change?"
    right = "%s %s" % (sg(m), unit)
    w = ["%s %s" % (sg(-m), unit), "%s %s" % (sg(b - a), unit), "%s %s" % (str(round(b / x2, 2)).rstrip("0").rstrip("."), unit)]
    if len(set(w + [right])) < 4:
        raise AssertionError
    return mcq(q, right, w, "(%d − %d) ÷ (%d − %d) = %s ÷ %d = <b>%s</b>." % (b, a, x2, x1, sg(b - a), x2 - x1, right))


def build():
    sets, R = build_sets([
        ("Slope from a graph", [("run", sl.set_graph, (), 20)]),
        ("Slope from two points", [("run", sl.set_points, (), 20)]),
        ("Slope from tables and equations", [("run", sl.set_table_eq, (), 20)]),
        ("Slope ideas: zero, undefined, steeper", [("run", sl.set_ideas, (), 20)]),
        ("Rate of change in real situations", [("collect", uniq(one_rate), 20)]),
    ], 69503)
    finish(sets, R)
    body = lesson('<ul><li><b>Slope</b> = change in <i>y</i> ÷ change in <i>x</i> = (<i>y</i><sub>2</sub> − <i>y</i><sub>1</sub>) ÷ (<i>x</i><sub>2</sub> − <i>x</i><sub>1</sub>).</li><li>Up to the right: positive slope. Down to the right: negative. Horizontal: 0. Vertical: undefined.</li><li>In <i>y</i> = <i>mx</i> + <i>b</i> the slope is <i>m</i>. In <i>Ax</i> + <i>By</i> = <i>C</i> the slope is −<i>A</i> ÷ <i>B</i>.</li><li>The <b>rate of change</b> gives the units: dollars per week, feet per hour.</li></ul>',
        [example("(2, 5) and (6, 17)", ["(17 − 5) ÷ (6 − 2) = 12 ÷ 4"], "slope 3")],
        [['Flipping rise and run', 'Change in <i>y</i> goes on top.'], ['Subtracting in different orders', 'Use the same point first in both.'], ['Dividing the values instead of the changes', 'Use differences, not the numbers themselves.']])
    faq = [('What does TEKS A.3A ask?', 'Determine the slope of a line given a table of values, a graph, two points on the line, and an equation written in various forms, including y = mx + b, Ax + By = C, and y − y<sub>1</sub> = m(x − x<sub>1</sub>).'), ('What does TEKS A.3B ask?', 'Calculate the rate of change of a linear function represented tabularly, graphically, or algebraically in context of mathematical and real-world problems.'), ('What is the slope of a vertical line?', 'Undefined, because the change in x is 0.'), ('Is slope the same as rate of change?', 'For a line, yes.')]
    make('slope-and-rate-of-change', 3, 'Linear Functions, Equations, and Inequalities', 'A.3A, A.3B',
         'A.3A determine the slope of a line given a table of values, a graph, two points on the line, and an equation written in various forms, including y = mx + b, Ax + By = C, and y − y1 = m(x − x1); A.3B calculate the rate of change of a linear function represented tabularly, graphically, or algebraically in context of mathematical and real-world problems',
         'Slope and Rate of Change', 'Slope and Rate of Change',
         'Free Algebra I slope worksheets for Texas TEKS A.3A and A.3B: slope from graphs, two points, tables and equations, zero and undefined slope, and rate of change in context. 100 questions with answers.',
         'Slope = change in y ÷ change in x.', '(2, 5) to (6, 17): 12 ÷ 4 = 3.',
         body, faq, sets, seo_title='Algebra I Slope and Rate of Change Worksheets (TEKS A.3A, A.3B)')


if __name__ == "__main__":
    build()
