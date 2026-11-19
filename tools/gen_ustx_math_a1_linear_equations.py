# -*- coding: utf-8 -*-
"""
Texas Algebra I: Solving Linear Equations (TEKS A.5A)
  python3 tools/gen_ustx_math_a1_linear_equations.py
Distributing and combining like terms, variables on both sides, fractions, decimals and percents, and writing and
solving equations (the US Algebra 1 makers with a new seed and Texas names).
Wrong answers come from real mistakes: distributing to only the first term, moving a term without changing its sign,
and multiplying only one side by the denominator.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a1_multi_step_equations as ms
adopt(ms)
ms.R = random.Random(695080)
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
        ("Distribute and combine like terms", [("collect", W(ms.one_dist), 20)]),
        ("Variables on both sides", [("collect", W(ms.one_both), 20)]),
        ("Equations with fractions", [("collect", W(ms.one_frac), 20)]),
        ("Equations with decimals and percents", [("collect", W(ms.one_dec), 20)]),
        ("Write and solve equations", [("run", PR(ms.problems), ("rnd",), 10), ("collect", W(ms.one_both), 10)]),
    ], 69508)
    finish(sets, R)
    body = lesson('<ul><li>Distribute and combine like terms on each side.</li><li>Get the variable terms on one side and the numbers on the other.</li><li>Clear fractions by multiplying <b>every term</b> by the common denominator.</li><li>Check by putting your answer back in.</li></ul>',
        [example("3(<i>x</i> − 4) + 2 = 5<i>x</i> − 16", ["3<i>x</i> − 10 = 5<i>x</i> − 16", "6 = 2<i>x</i>"], "<i>x</i> = 3")],
        [['Distributing to only the first term', '3(<i>x</i> − 4) = 3<i>x</i> − 12.'], ['Moving a term without changing its sign', 'Subtract from both sides.'], ['Clearing only one side', 'Multiply every term.']])
    faq = [('What does TEKS A.5A ask?', 'Solve linear equations in one variable, including those for which the application of the distributive property is necessary and for which variables are included on both sides.'), ('What if the variables cancel?', 'A true statement means all numbers; a false one means no solution.'), ('How do I clear decimals?', 'Multiply every term by 10 or 100.'), ('Why check?', 'It catches sign mistakes.')]
    make('solving-linear-equations', 8, 'Linear Functions, Equations, and Inequalities', 'A.5A',
         'A.5A solve linear equations in one variable, including those for which the application of the distributive property is necessary and for which variables are included on both sides',
         'Solving Linear Equations', 'Solving Linear Equations',
         'Free Algebra I worksheets for Texas TEKS A.5A: solve multi-step linear equations with distributing, variables on both sides, fractions, decimals and word problems. 100 questions with answers.',
         'Distribute, combine, then isolate the variable.', '3(x − 4) + 2 = 5x − 16 gives x = 3.',
         body, faq, sets, seo_title='Algebra I Solving Linear Equations Worksheets (TEKS A.5A)')


if __name__ == "__main__":
    build()
