# -*- coding: utf-8 -*-
"""
Texas Algebra I: Systems of Linear Equations (TEKS A.5C, A.2I, A.3F, A.3G)
  python3 tools/gen_ustx_math_a1_systems_equations.py
Solving by graphing and counting solutions (US Grade 8 makers with a new seed), elimination and substitution, and
systems word problems (US Algebra 1 makers with a new seed and Texas names).
Wrong answers come from real mistakes: giving only one value, adding equations without lining up terms, and
multiplying only one side.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g8_systems_of_equations as sg8
adopt(sg8)
sg8.R = random.Random(695100)
import gen_us_math_a1_systems_of_linear_equations as sy
adopt(sy)
sy.R = random.Random(695101)
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
        ("Solve by graphing", [("run", sg8.set_graph, (), 20)]),
        ("One, none or infinitely many solutions", [("run", sg8.set_count, (), 20)]),
        ("Elimination", [("collect", W(sy.one_add), 6), ("collect", W(sy.one_sub), 6), ("collect", W(sy.one_mult), 8)]),
        ("Substitution", [("collect", W(sy.one_subst), 20)]),
        ("Systems word problems", [("run", PR(sy.problems), ("rnd",), 10), ("run", sg8.set_words, (), 10)]),
    ], 69510)
    finish(sets, R)
    body = lesson('<ul><li>The solution of a system is the point where the lines <b>cross</b>.</li><li><b>Substitution</b>: solve one equation for a variable and put it into the other.</li><li><b>Elimination</b>: add or subtract the equations so one variable cancels. Multiply first if needed.</li><li>Parallel lines: no solution. The same line: infinitely many solutions.</li></ul>',
        [example("<i>x</i> + <i>y</i> = 10 and <i>x</i> − <i>y</i> = 4", ["add: 2<i>x</i> = 14", "<i>x</i> = 7, <i>y</i> = 3"], "(7, 3)")],
        [['Giving only one value', 'A solution is an ordered pair.'], ['Not lining up terms', 'Line up <i>x</i>, <i>y</i> and numbers.'], ['Multiplying only one side', 'Multiply every term.']])
    faq = [('What does TEKS A.5C ask?', 'Solve systems of two linear equations with two variables for mathematical and real-world problems.'), ('What does TEKS A.2I ask?', 'Write systems of two linear equations given a table of values, a graph, and a verbal description.'), ('What does TEKS A.3F ask?', 'Graph systems of two linear equations in two variables on the coordinate plane and determine the solutions if they exist.'), ('What does TEKS A.3G ask?', 'Estimate graphically the solutions to systems of two linear equations with two variables in real-world problems.')]
    make('systems-of-linear-equations', 10, 'Linear Functions, Equations, and Inequalities', 'A.5C, A.2I, A.3F, A.3G',
         'A.5C solve systems of two linear equations with two variables for mathematical and real-world problems; A.2I write systems of two linear equations given a table of values, a graph, and a verbal description; A.3F graph systems of two linear equations in two variables on the coordinate plane and determine the solutions if they exist; A.3G estimate graphically the solutions to systems of two linear equations with two variables in real-world problems',
         'Systems of Linear Equations', 'Systems of Linear Equations',
         'Free Algebra I systems worksheets for Texas TEKS A.5C, A.2I, A.3F and A.3G: solve by graphing, elimination and substitution, count solutions and word problems. 100 questions with answers.',
         'The solution is where the lines cross.', 'x + y = 10, x − y = 4 gives (7, 3).',
         body, faq, sets, seo_title='Algebra I Systems of Linear Equations Worksheets (TEKS A.5C)')


if __name__ == "__main__":
    build()
