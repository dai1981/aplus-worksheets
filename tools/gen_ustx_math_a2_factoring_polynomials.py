# -*- coding: utf-8 -*-
"""
Texas Algebra II: Factoring Polynomials of Degree 3 and 4 (TEKS 2A.7D, 2A.7E)
  python3 tools/gen_ustx_math_a2_factoring_polynomials.py
Sum and difference of cubes, factoring by grouping, quadratic form, the Factor Theorem and factoring completely
from one factor (US Algebra 2 makers with a new seed).
Wrong answers come from real mistakes: the wrong signs in a cubes pattern, stopping before factoring completely, and
using P(c) instead of P(−c).
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a2_polynomial_identities_and_factoring as pi
adopt(pi)
pi.R = random.Random(697210)
import gen_us_math_a2_polynomial_division_and_remainder_theorem as pd
adopt(pd)
pd.R = random.Random(697211)
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
        ("Sum and difference of cubes", [("collect", W(pi.one_cubes), 20)]),
        ("Factor by grouping", [("collect", W(pi.one_group), 20)]),
        ("Polynomials in quadratic form", [("collect", W(pi.one_qform), 20)]),
        ("The Factor Theorem", [("collect", W(pd.one_fac), 20)]),
        ("Factor completely from one factor", [("collect", W(pd.one_full), 20)]),
    ], 69721)
    finish(sets, R)
    body = lesson('<ul><li>Sum of cubes: <i>a</i><sup>3</sup> + <i>b</i><sup>3</sup> = (<i>a</i> + <i>b</i>)(<i>a</i><sup>2</sup> − <i>ab</i> + <i>b</i><sup>2</sup>). Difference: <i>a</i><sup>3</sup> − <i>b</i><sup>3</sup> = (<i>a</i> − <i>b</i>)(<i>a</i><sup>2</sup> + <i>ab</i> + <i>b</i><sup>2</sup>).</li><li>Grouping: factor pairs of terms, then factor out the common binomial.</li><li>Quadratic form: <i>x</i><sup>4</sup> − 5<i>x</i><sup>2</sup> + 4 is like <i>u</i><sup>2</sup> − 5<i>u</i> + 4 with <i>u</i> = <i>x</i><sup>2</sup>.</li><li>Factor Theorem: (<i>x</i> − <i>c</i>) is a factor exactly when <i>P</i>(<i>c</i>) = 0. Divide by it to get the other factors.</li></ul>',
        [example("<i>x</i><sup>3</sup> + 3<i>x</i><sup>2</sup> − 4<i>x</i> − 12", ["<i>x</i><sup>2</sup>(<i>x</i> + 3) − 4(<i>x</i> + 3)", "(<i>x</i> + 3)(<i>x</i><sup>2</sup> − 4)"], "(<i>x</i> + 3)(<i>x</i> − 2)(<i>x</i> + 2)")],
        [['Wrong signs in a cubes pattern', 'Difference: (<i>a</i> − <i>b</i>)(<i>a</i><sup>2</sup> + <i>ab</i> + <i>b</i><sup>2</sup>).'], ['Not factoring completely', '<i>x</i><sup>2</sup> − 4 still factors.'], ['Testing the wrong number', 'For (<i>x</i> + 3), find <i>P</i>(−3).']])
    faq = [('What does TEKS 2A.7D ask?', 'Determine the linear factors of a polynomial function of degree three and of degree four using algebraic methods.'), ('What does TEKS 2A.7E ask?', 'Determine linear and quadratic factors of a polynomial expression of degree three and of degree four, including factoring the sum and difference of two cubes and factoring by grouping.'), ('Does a² + ab + b² factor further?', 'Not over the real numbers.'), ('How do factors give zeros?', 'Each factor x − c gives a zero x = c.')]
    make('factoring-polynomials', 21, 'Number and Algebraic Methods', '2A.7D, 2A.7E',
         '2A.7D determine the linear factors of a polynomial function of degree three and of degree four using algebraic methods; 2A.7E determine linear and quadratic factors of a polynomial expression of degree three and of degree four, including factoring the sum and difference of two cubes and factoring by grouping',
         'Factoring Polynomials of Degree 3 and 4', 'Factoring Polynomials',
         'Free Algebra II factoring worksheets for Texas TEKS 2A.7D and 2A.7E: sum and difference of cubes, grouping, quadratic form, the Factor Theorem and factoring completely. 100 questions with answers.',
         'a³ − b³ = (a − b)(a² + ab + b²).', '(x − c) is a factor when P(c) = 0.',
         body, faq, sets, seo_title='Algebra II Factoring Polynomials Worksheets (TEKS 2A.7D, 2A.7E)')


if __name__ == "__main__":
    build()
