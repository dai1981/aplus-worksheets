# -*- coding: utf-8 -*-
"""
Texas Precalculus: Inverse Trigonometric Functions (TEKS P.2F, P.2H)
  python3 tools/gen_ustx_math_pc_inverse_trig.py
Exact values of arcsin, arccos and arctan, their restricted domains and ranges, compositions, calculator values and
angle problems (US Precalculus makers with a new seed).
Wrong answers come from real mistakes: giving an angle outside the range, taking arcsin of a number greater than 1, and
using degrees when the answer is asked in radians.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_pc_inverse_trigonometric_functions as it
adopt(it)
it.R = random.Random(698150)
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
        ("Exact values", [("collect", W(it.one_exact), 20)]),
        ("Domain and range", [("collect", W(it.one_dr), 20)]),
        ("Compositions", [("collect", W(it.one_comp), 20)]),
        ("Calculator values", [("collect", W(it.one_calc), 20)]),
        ("Find angles in real situations", [("collect", W(it.one_word), 20)]),
    ], 69815)
    finish(sets, R)
    body = lesson('<ul><li>sin<sup>−1</sup> <i>x</i> (arcsin) gives the angle in [−π/2, π/2] whose sine is <i>x</i>. Its domain is −1 ≤ <i>x</i> ≤ 1.</li><li>cos<sup>−1</sup> <i>x</i> (arccos) gives the angle in [0, π]. tan<sup>−1</sup> <i>x</i> gives the angle in (−π/2, π/2) for any <i>x</i>.</li><li>These ranges are why the domain of sine and cosine is restricted: so each output comes from only one angle.</li><li>For tan(sin<sup>−1</sup> <i>a</i>), draw a right triangle with the given ratio.</li></ul>',
        [example("cos<sup>−1</sup>(−<span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>)", ["The range is [0, π]", "cos(2π/3) = −1/2"], "<span class='fr'><span class='fn'>2π</span><span class='fd'>3</span></span>")],
        [['An angle outside the range', 'sin<sup>−1</sup> answers are between −π/2 and π/2.'], ['sin<sup>−1</sup> of 2', 'Not defined: the input must be from −1 to 1.'], ['Degrees for radians', 'Set the calculator mode to match.']])
    faq = [('What does TEKS P.2H ask?', 'Graph arcsin x and arccos x and describe the limitations on the domain.'), ('Is sin⁻¹ x the same as 1/sin x?', 'No. 1/sin x is csc x.'), ('Why is the range of arccos [0, π]?', 'Cosine takes every value from −1 to 1 exactly once on that interval.'), ('What is the domain of arctan?', 'All real numbers.')]
    make('inverse-trigonometric-functions', 15, 'Functions', 'P.2F, P.2H',
         'P.2F graph exponential, logarithmic, rational, polynomial, power, trigonometric, inverse trigonometric, and piecewise defined functions, including step functions; P.2H graph arcsin x and arccos x and describe the limitations on the domain',
         'Inverse Trigonometric Functions', 'Inverse Trig Functions',
         'Free Precalculus worksheets on inverse trigonometric functions for Texas TEKS P.2F and P.2H: exact values, domain and range of arcsin and arccos, compositions and angle problems. 100 questions with answers.',
         'arcsin gives an angle in [−π/2, π/2]; arccos in [0, π].', 'The input of arcsin and arccos must be from −1 to 1.',
         body, faq, sets, seo_title='Precalculus Inverse Trigonometric Functions Worksheets (TEKS P.2F, P.2H)')


if __name__ == "__main__":
    build()
