# -*- coding: utf-8 -*-
"""
Texas Algebra I: Solving Quadratic Equations (TEKS A.8A)
  python3 tools/gen_ustx_math_a1_solving_quadratics.py
Solving by factoring, setting to zero and a ≠ 1, taking square roots, completing the square, the quadratic formula,
and quadratic word problems (the US Algebra 1 makers with a new seed and Texas names).
Wrong answers come from real mistakes: forgetting the ± when taking a square root, the wrong signs from the factors,
and dividing only part of the formula by 2a.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a1_solving_quadratics_by_factoring as sq
adopt(sq)
sq.R = random.Random(695200)
import gen_us_math_a1_quadratic_formula_and_completing_the_square as qf
adopt(qf)
qf.R = random.Random(695201)
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
        ("Solve x² + bx + c = 0 by factoring", [("collect", W(sq.one_simple), 20)]),
        ("Set to zero, GCF and a ≠ 1", [("collect", W(sq.one_hard), 20)]),
        ("Square roots and completing the square", [("collect", W(sq.one_sqrt), 12), ("collect", W(qf.one_complete), 8)]),
        ("The quadratic formula", [("collect", W(qf.one_rational), 10), ("collect", W(qf.one_radical), 10)]),
        ("Quadratic equation word problems", [("run", PR(sq.problems), ("rnd",), 10), ("run", PR(qf.problems), ("rnd",), 10)]),
    ], 69520)
    finish(sets, R)
    body = lesson('<ul><li><b>Factoring</b>: set the equation to 0, factor, then set each factor to 0.</li><li><b>Square roots</b>: <i>x</i><sup>2</sup> = 25 gives <i>x</i> = ±5.</li><li><b>Completing the square</b>: add (<i>b</i> ÷ 2)<sup>2</sup> to both sides.</li><li><b>Quadratic formula</b>: <i>x</i> = (−<i>b</i> ± √(<i>b</i><sup>2</sup> − 4<i>ac</i>)) ÷ (2<i>a</i>).</li></ul>',
        [example("<i>x</i><sup>2</sup> + 2<i>x</i> − 15 = 0", ["(<i>x</i> + 5)(<i>x</i> − 3) = 0"], "<i>x</i> = −5 or <i>x</i> = 3")],
        [['Forgetting ±', '<i>x</i><sup>2</sup> = 25 has two solutions.'], ['Wrong signs from factors', '(<i>x</i> + 5) = 0 gives −5.'], ['Dividing only part by 2<i>a</i>', 'Divide the whole top.']])
    faq = [('What does TEKS A.8A ask?', 'Solve quadratic equations having real solutions by factoring, taking square roots, completing the square, and applying the quadratic formula.'), ('Which method should I use?', 'Factor if you can; otherwise use the formula.'), ('What does the discriminant tell?', 'b² − 4ac > 0: two solutions; = 0: one; < 0: none real.'), ('Why set the equation to 0?', 'The zero product property needs a product equal to 0.')]
    make('solving-quadratic-equations', 20, 'Quadratic Functions and Equations', 'A.8A',
         'A.8A solve quadratic equations having real solutions by factoring, taking square roots, completing the square, and applying the quadratic formula',
         'Solving Quadratic Equations', 'Solving Quadratic Equations',
         'Free Algebra I worksheets for Texas TEKS A.8A: solve quadratic equations by factoring, square roots, completing the square and the quadratic formula, with word problems. 100 questions with answers.',
         'Set to 0, then factor, take roots, complete the square or use the formula.', 'x² + 2x − 15 = 0 gives x = −5 or 3.',
         body, faq, sets, seo_title='Algebra I Solving Quadratic Equations Worksheets (TEKS A.8A)')


if __name__ == "__main__":
    build()
