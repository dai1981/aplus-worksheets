# -*- coding: utf-8 -*-
"""
Texas Algebra II: Operations with Rational Expressions (TEKS 2A.7F)
  python3 tools/gen_ustx_math_a2_rational_expressions.py
Simplifying, multiplying, dividing, adding and subtracting rational expressions, complex fractions and word problems
(US Algebra 2 makers with a new seed).
Wrong answers come from real mistakes: cancelling terms instead of factors, adding denominators, and not flipping the
second fraction when dividing.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a2_rational_expressions as re_
adopt(re_)
re_.R = random.Random(697220)
tx_common.GRADE = "algebra-2"

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
        ("Simplify rational expressions", [("collect", W(re_.one_simp), 20)]),
        ("Multiply and divide", [("collect", W(re_.one_md), 20)]),
        ("Add and subtract", [("collect", W(re_.one_add), 20)]),
        ("Complex fractions", [("collect", W(re_.one_cx), 20)]),
        ("Rational expressions in context", [("collect", W(re_.one_word), 20)]),
    ], 69722)
    finish(sets, R)
    body = lesson('<ul><li>Factor first. Cancel only common <b>factors</b>, never terms.</li><li>Multiply: multiply tops and bottoms, then cancel. Divide: multiply by the reciprocal of the second fraction.</li><li>Add or subtract: use a common denominator, then combine the numerators.</li><li>Values that make any denominator 0 are excluded from the domain.</li></ul>',
        [example("<span class='fr'><span class='fn'><i>x</i><sup>2</sup> − 9</span><span class='fd'><i>x</i><sup>2</sup> + 5<i>x</i> + 6</span></span>", ["<span class='fr'><span class='fn'>(<i>x</i> − 3)(<i>x</i> + 3)</span><span class='fd'>(<i>x</i> + 2)(<i>x</i> + 3)</span></span>"], "<span class='fr'><span class='fn'><i>x</i> − 3</span><span class='fd'><i>x</i> + 2</span></span>, <i>x</i> ≠ −2, −3")],
        [['Cancelling terms', 'In (<i>x</i> + 3) ÷ (<i>x</i> + 5) nothing cancels.'], ['Adding denominators', 'Find a common denominator instead.'], ['Not flipping when dividing', 'Multiply by the reciprocal.']])
    faq = [('What does TEKS 2A.7F ask?', 'Determine the sum, difference, product, and quotient of rational expressions with integral exponents of degree one and of degree two.'), ('Why list excluded values?', 'The original expression is undefined there, even if the factor cancels.'), ('What is a complex fraction?', 'A fraction with fractions in its numerator or denominator.'), ('How do you find a common denominator?', 'Factor each denominator and use every factor the greatest number of times it appears.')]
    make('rational-expressions', 22, 'Number and Algebraic Methods', '2A.7F',
         '2A.7F determine the sum, difference, product, and quotient of rational expressions with integral exponents of degree one and of degree two',
         'Operations with Rational Expressions', 'Rational Expressions',
         'Free Algebra II rational expression worksheets for Texas TEKS 2A.7F: simplify, multiply, divide, add and subtract rational expressions and complex fractions. 100 questions with answers.',
         'Factor first, then cancel common factors.', 'To divide, multiply by the reciprocal.',
         body, faq, sets, seo_title='Algebra II Rational Expressions Worksheets (TEKS 2A.7F)')


if __name__ == "__main__":
    build()
