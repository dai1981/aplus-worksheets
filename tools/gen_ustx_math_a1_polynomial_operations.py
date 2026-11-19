# -*- coding: utf-8 -*-
"""
Texas Algebra I: Adding, Subtracting and Multiplying Polynomials (TEKS A.10A, A.10B, A.10D)
  python3 tools/gen_ustx_math_a1_polynomial_operations.py
Degree and standard form, adding and subtracting, multiplying, special products, and polynomial applications (the
US Algebra 1 makers with a new seed and Texas names).
Wrong answers come from real mistakes: not distributing the minus sign, adding exponents when adding terms, and
forgetting the middle term of (a + b)².
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a1_polynomial_operations as po
adopt(po)
po.R = random.Random(695140)
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
        ("Degree, leading coefficient and standard form", [("collect", W(po.one_class), 20)]),
        ("Add and subtract polynomials", [("collect", W(po.one_addsub), 20)]),
        ("Multiply polynomials", [("collect", W(po.one_mul), 20)]),
        ("Special products", [("collect", W(po.one_special), 20)]),
        ("Polynomial applications", [("run", PR(po.problems), ("rnd",), 10), ("collect", W(po.one_mul), 10)]),
    ], 69514)
    finish(sets, R)
    body = lesson('<ul><li>Add or subtract <b>like terms</b> only: same variable, same exponent.</li><li>When subtracting, change the sign of <b>every</b> term in the second polynomial.</li><li>To multiply, use the distributive property: each term times each term.</li><li>(<i>a</i> + <i>b</i>)<sup>2</sup> = <i>a</i><sup>2</sup> + 2<i>ab</i> + <i>b</i><sup>2</sup>, and (<i>a</i> + <i>b</i>)(<i>a</i> − <i>b</i>) = <i>a</i><sup>2</sup> − <i>b</i><sup>2</sup>.</li></ul>',
        [example("(2<i>x</i> + 3)(<i>x</i> − 4)", ["2<i>x</i><sup>2</sup> − 8<i>x</i> + 3<i>x</i> − 12"], "2<i>x</i><sup>2</sup> − 5<i>x</i> − 12")],
        [['Not distributing the minus sign', '−(3<i>x</i> − 2) = −3<i>x</i> + 2.'], ['Adding exponents when adding', '<i>x</i><sup>2</sup> + <i>x</i><sup>2</sup> = 2<i>x</i><sup>2</sup>.'], ['Forgetting the middle term', '(<i>x</i> + 3)<sup>2</sup> has 6<i>x</i>.']])
    faq = [('What does TEKS A.10A ask?', 'Add and subtract polynomials of degree one and degree two.'), ('What does TEKS A.10B ask?', 'Multiply polynomials of degree one and degree two.'), ('What does TEKS A.10D ask?', 'Rewrite polynomial expressions of degree one and degree two in equivalent forms using the distributive property.'), ('What is the degree of 3x² − 5x + 1?', '2.')]
    make('polynomial-operations', 14, 'Number and Algebraic Methods', 'A.10A, A.10B, A.10D',
         'A.10A add and subtract polynomials of degree one and degree two; A.10B multiply polynomials of degree one and degree two; A.10D rewrite polynomial expressions of degree one and degree two in equivalent forms using the distributive property',
         'Adding, Subtracting and Multiplying Polynomials', 'Polynomial Operations',
         'Free Algebra I polynomial worksheets for Texas TEKS A.10A, A.10B and A.10D: degree and standard form, add, subtract and multiply polynomials, special products and applications. 100 questions with answers.',
         'Combine like terms; distribute every term.', '(2x + 3)(x − 4) = 2x² − 5x − 12',
         body, faq, sets, seo_title='Algebra I Polynomial Operations Worksheets (TEKS A.10A, A.10B)')


if __name__ == "__main__":
    build()
