# -*- coding: utf-8 -*-
"""
Texas Algebra I: Linear Inequalities in One and Two Variables (TEKS A.5B, A.2H, A.3D)
  python3 tools/gen_ustx_math_a1_linear_inequalities.py
Multi-step inequalities, variables on both sides, compound inequalities (US Algebra 1 makers), graphs of linear
inequalities in two variables (US Algebra 1 maker), and inequality word problems, with a new seed and Texas names.
Wrong answers come from real mistakes: not flipping the sign when dividing by a negative, a solid line for &lt;, and
shading the wrong side.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a1_multi_step_and_compound_inequalities as iq
adopt(iq)
iq.R = random.Random(695090)
import gen_us_math_a1_systems_of_linear_inequalities as si
adopt(si)
si.R = random.Random(695091)
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
        ("Multi-step inequalities", [("collect", W(iq.one_hard), 20)]),
        ("Variables on both sides", [("collect", W(iq.one_both), 20)]),
        ("Compound inequalities", [("collect", W(iq.one_and), 20)]),
        ("Graph a linear inequality in two variables", [("collect", W(si.one_graph1), 20)]),
        ("Inequality word problems", [("run", PR(iq.problems), ("rnd",), 10), ("collect", W(iq.one_hard), 10)]),
    ], 69509)
    finish(sets, R)
    body = lesson('<ul><li>Solve like an equation, but <b>flip the sign</b> when you multiply or divide by a negative number.</li><li>For <i>y</i> &gt; <i>mx</i> + <i>b</i>, draw a <b>dashed</b> line and shade <b>above</b>. For ≥, use a solid line.</li><li>Test a point like (0, 0) to check the shading.</li></ul>',
        [example("−3<i>x</i> + 5 ≤ 17", ["−3<i>x</i> ≤ 12", "divide by −3, flip"], "<i>x</i> ≥ −4")],
        [['Not flipping the sign', 'Dividing by a negative flips the inequality.'], ['Solid line for &lt; or &gt;', 'Use a dashed line.'], ['Shading the wrong side', 'Test (0, 0).']])
    faq = [('What does TEKS A.5B ask?', 'Solve linear inequalities in one variable, including those for which the application of the distributive property is necessary and for which variables are included on both sides.'), ('What does TEKS A.2H ask?', 'Write linear inequalities in two variables given a table of values, a graph, and a verbal description.'), ('What does TEKS A.3D ask?', 'Graph the solution set of linear inequalities in two variables on the coordinate plane.'), ('When is the boundary solid?', 'For ≤ and ≥.')]
    make('linear-inequalities', 9, 'Linear Functions, Equations, and Inequalities', 'A.5B, A.2H, A.3D',
         'A.5B solve linear inequalities in one variable, including those for which the application of the distributive property is necessary and for which variables are included on both sides; A.2H write linear inequalities in two variables given a table of values, a graph, and a verbal description; A.3D graph the solution set of linear inequalities in two variables on the coordinate plane',
         'Linear Inequalities in One and Two Variables', 'Linear Inequalities',
         'Free Algebra I inequality worksheets for Texas TEKS A.5B, A.2H and A.3D: multi-step and compound inequalities, graphing inequalities in two variables and word problems. 100 questions with answers.',
         'Flip the sign when dividing by a negative.', 'Dashed line for < and >; solid for ≤ and ≥.',
         body, faq, sets, seo_title='Algebra I Linear Inequalities Worksheets (TEKS A.5B, A.3D)')


if __name__ == "__main__":
    build()
