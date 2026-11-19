# -*- coding: utf-8 -*-
"""
Texas Algebra I: Factoring Trinomials, Differences of Squares and Perfect Squares (TEKS A.10E, A.10F)
  python3 tools/gen_ustx_math_a1_factoring.py
The greatest common factor, x² + bx + c, ax² + bx + c, differences of squares and perfect squares, and factoring
completely (the US Algebra 1 makers with a new seed and Texas names).
Wrong answers come from real mistakes: the right numbers with the wrong signs, factoring x² + 9 as (x + 3)(x − 3),
and stopping before the GCF is out.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a1_factoring_polynomials as fp
adopt(fp)
fp.R = random.Random(695160)
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
        ("Greatest common factor", [("collect", W(fp.one_gcf), 20)]),
        ("Factor x² + bx + c", [("collect", W(fp.one_simple), 20)]),
        ("Factor ax² + bx + c", [("collect", W(fp.one_ac), 20)]),
        ("Difference of squares and perfect squares", [("collect", W(fp.one_special), 20)]),
        ("Factor completely and apply", [("collect", W(fp.one_complete), 10), ("run", PR(fp.problems), ("rnd",), 10)]),
    ], 69516)
    finish(sets, R)
    body = lesson('<ul><li>Always take out the <b>greatest common factor</b> first.</li><li><i>x</i><sup>2</sup> + <i>bx</i> + <i>c</i>: find two numbers that multiply to <i>c</i> and add to <i>b</i>.</li><li><b>Difference of squares</b>: <i>a</i><sup>2</sup> − <i>b</i><sup>2</sup> = (<i>a</i> + <i>b</i>)(<i>a</i> − <i>b</i>). A <b>sum</b> of squares does not factor.</li><li><b>Perfect square</b>: <i>a</i><sup>2</sup> + 2<i>ab</i> + <i>b</i><sup>2</sup> = (<i>a</i> + <i>b</i>)<sup>2</sup>.</li></ul>',
        [example("<i>x</i><sup>2</sup> − 2<i>x</i> − 15", ["−5 × 3 = −15", "−5 + 3 = −2"], "(<i>x</i> − 5)(<i>x</i> + 3)")],
        [['Right numbers, wrong signs', 'Check the middle term by multiplying.'], ['Factoring <i>x</i><sup>2</sup> + 9', 'A sum of squares does not factor.'], ['Forgetting the GCF', 'Take it out first.']])
    faq = [('What does TEKS A.10E ask?', 'Factor, if possible, trinomials with real factors in the form ax<sup>2</sup> + bx + c, including perfect square trinomials of degree two.'), ('What does TEKS A.10F ask?', 'Decide if a binomial can be written as the difference of two squares and, if possible, use the structure of a difference of two squares to rewrite the binomial.'), ('Can x² − 7 be factored over the integers?', 'No. 7 is not a perfect square.'), ('How do I check a factoring?', 'Multiply the factors back out.')]
    make('factoring', 16, 'Number and Algebraic Methods', 'A.10E, A.10F',
         'A.10E factor, if possible, trinomials with real factors in the form ax^2 + bx + c, including perfect square trinomials of degree two; A.10F decide if a binomial can be written as the difference of two squares and, if possible, use the structure of a difference of two squares to rewrite the binomial',
         'Factoring Trinomials, Differences of Squares and Perfect Squares', 'Factoring',
         'Free Algebra I factoring worksheets for Texas TEKS A.10E and A.10F: GCF, x² + bx + c, ax² + bx + c, difference of squares, perfect square trinomials and applications. 100 questions with answers.',
         'GCF first, then find two numbers.', 'x² − 2x − 15 = (x − 5)(x + 3)',
         body, faq, sets, seo_title='Algebra I Factoring Worksheets (TEKS A.10E, A.10F)')


if __name__ == "__main__":
    build()
