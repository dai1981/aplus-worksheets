# -*- coding: utf-8 -*-
"""
Texas Algebra I: Systems of Linear Inequalities (TEKS A.3H, A.2H)
  python3 tools/gen_ustx_math_a1_systems_inequalities.py
Is the point a solution, graphs of systems, writing a system, and systems in context (the US Algebra 1 makers with a
new seed and Texas names).
Wrong answers come from real mistakes: checking only one inequality, shading outside the overlap, and counting a
point on a dashed line.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a1_systems_of_linear_inequalities as si
adopt(si)
si.R = random.Random(695110)
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
        ("Is the point a solution?", [("collect", W(si.one_point), 20)]),
        ("Graph of a system", [("collect", W(si.one_graph2), 20)]),
        ("Write a system and read graphs", [("run", PR(si.problems_write), ("rnd",), 10), ("collect", W(si.one_graph1), 10)]),
        ("Systems in context and test points", [("run", PR(si.problems_use), ("rnd",), 10), ("collect", W(si.one_point), 10)]),
        ("Mixed practice", [("collect", W(si.one_point), 10), ("collect", W(si.one_graph2), 10)]),
    ], 69511)
    finish(sets, R)
    body = lesson('<ul><li>Graph each inequality. The solutions are where the shadings <b>overlap</b>.</li><li>A point is a solution only if it makes <b>every</b> inequality true.</li><li>Points on a dashed line are not solutions.</li></ul>',
        [example("Is (1, 2) a solution of <i>y</i> &gt; <i>x</i> and <i>y</i> ≤ 3?", ["2 &gt; 1 true", "2 ≤ 3 true"], "yes")],
        [['Checking only one inequality', 'Test both.'], ['Shading outside the overlap', 'Only the overlap is the solution.'], ['Counting points on a dashed line', 'Dashed means not included.']])
    faq = [('What does TEKS A.3H ask?', 'Graph the solution set of systems of two linear inequalities in two variables on the coordinate plane.'), ('What does TEKS A.2H ask?', 'Write linear inequalities in two variables given a table of values, a graph, and a verbal description.'), ('Can a system have no solution?', 'Yes, if the shadings never overlap.'), ('How do I check a point?', 'Put it into every inequality.')]
    make('systems-of-linear-inequalities', 11, 'Linear Functions, Equations, and Inequalities', 'A.3H, A.2H',
         'A.3H graph the solution set of systems of two linear inequalities in two variables on the coordinate plane; A.2H write linear inequalities in two variables given a table of values, a graph, and a verbal description',
         'Systems of Linear Inequalities', 'Systems of Linear Inequalities',
         'Free Algebra I worksheets for Texas TEKS A.3H and A.2H: test points, read graphs of systems of inequalities, write systems and solve problems in context. 100 questions with answers.',
         'Solutions are in the overlap.', 'A point must make every inequality true.',
         body, faq, sets, seo_title='Algebra I Systems of Linear Inequalities Worksheets (TEKS A.3H)')


if __name__ == "__main__":
    build()
