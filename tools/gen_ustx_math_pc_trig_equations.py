# -*- coding: utf-8 -*-
"""
Texas Precalculus: Solving Trigonometric Equations (TEKS P.5M)
  python3 tools/gen_ustx_math_pc_trig_equations.py
Solving basic and linear trigonometric equations, factoring, multiple angles and general solutions, and models
(US Precalculus makers with a new seed).
Wrong answers come from real mistakes: finding only one solution in [0, 2π), dividing by sin x and losing solutions,
and forgetting + 2πk.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_pc_solving_trigonometric_equations as te
adopt(te)
te.R = random.Random(698170)
tx_common.GRADE = "precalculus"

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


from fractions import Fraction as Fr


def ft(v):
    v = Fr(v)
    if v.denominator == 1:
        return sg(int(v))
    return (MINUS if v < 0 else "") + fr(abs(v.numerator), v.denominator)


def fx(body, name="f"):
    return "<i>%s</i>(<i>x</i>) = %s" % (name, body)



def build():
    sets, R = build_sets([
        ("Basic equations", [("collect", W(te.one_basic), 20)]),
        ("Linear trigonometric equations", [("collect", W(te.one_lin), 20)]),
        ("Solve by factoring", [("collect", W(te.one_fact), 20)]),
        ("Multiple angles and all solutions", [("collect", W(te.one_multi), 20)]),
        ("Trigonometric models", [("collect", W(te.one_model), 20)]),
    ], 69817)
    finish(sets, R)
    body = lesson('<ul><li>Get the trig function alone, then find the reference angle.</li><li>Use the signs in each quadrant to find <b>every</b> angle in 0 ≤ <i>x</i> &lt; 2π (usually two).</li><li>For sin<sup>2</sup> <i>x</i> − sin <i>x</i> = 0, factor: sin <i>x</i>(sin <i>x</i> − 1) = 0. Do not divide by sin <i>x</i>.</li><li>All solutions: add 2π<i>k</i> (π<i>k</i> for tangent). For sin 2<i>x</i>, solve for 2<i>x</i> first, then divide.</li></ul>',
        [example("2 cos <i>x</i> + 1 = 0, 0 ≤ <i>x</i> &lt; 2π", ["cos <i>x</i> = −<span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>", "Reference angle π/3, Quadrants II and III"], "<i>x</i> = <span class='fr'><span class='fn'>2π</span><span class='fd'>3</span></span>, <span class='fr'><span class='fn'>4π</span><span class='fd'>3</span></span>")],
        [['Only one solution', 'Look in both quadrants with the right sign.'], ['Dividing by sin <i>x</i>', 'Factor instead, or you lose sin <i>x</i> = 0.'], ['Forgetting + 2π<i>k</i>', 'All solutions repeat every period.']])
    faq = [('What does TEKS P.5M ask?', 'Generate and solve trigonometric equations in mathematical and real-world problems.'), ('How many solutions does sin x = 0.5 have in [0, 2π)?', 'Two: π/6 and 5π/6.'), ('Can a trig equation have no solution?', 'Yes, for example sin x = 2.'), ('Why do multiple angles give more solutions?', 'sin 2x completes two cycles in [0, 2π).')]
    make('trigonometric-equations', 17, 'Algebraic Reasoning', 'P.5M',
         'P.5M generate and solve trigonometric equations in mathematical and real-world problems',
         'Solving Trigonometric Equations', 'Trigonometric Equations',
         'Free Precalculus worksheets on trigonometric equations for Texas TEKS P.5M: basic and linear equations, factoring, multiple angles, general solutions and models. 100 questions with answers.',
         'Find the reference angle, then every quadrant with the right sign.', 'Factor; never divide by a trig function.',
         body, faq, sets, seo_title='Precalculus Trigonometric Equations Worksheets (TEKS P.5M)')


if __name__ == "__main__":
    build()
