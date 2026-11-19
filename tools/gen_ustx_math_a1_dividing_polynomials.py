# -*- coding: utf-8 -*-
"""
Texas Algebra I: Dividing Polynomials (TEKS A.10C)
  python3 tools/gen_ustx_math_a1_dividing_polynomials.py
Dividing by a monomial, dividing x² + bx + c by a binomial factor, leading coefficients and degree-one divisors,
finding a missing factor, and area problems (own makers).
Wrong answers come from real mistakes: dividing only the first term, keeping the wrong sign, and adding instead of
factoring.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)

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



def lin(a, b, v="<i>x</i>"):
    return poly([a, b], v)


def one_mono(r):
    c = r.randint(2, 6)
    q1, q0 = r.choice([n for n in range(-7, 8) if n]), r.choice([n for n in range(-9, 10) if n])
    if r.random() < 0.6:
        dv = "%d<i>x</i>" % c
        num = poly([c * q1, c * q0, 0])
        right = poly([q1, q0])
        w = [poly([q1, c * q0]), poly([q1, q0, 0]), poly([c * q1, q0])]
    else:
        q2 = r.choice([n for n in range(-9, 10) if n])
        dv = str(c)
        num = poly([c * q1, c * q0, c * q2])
        right = poly([q1, q0, q2])
        w = [poly([q1, c * q0, c * q2]), poly([q1, q0, c * q2]), poly([c * q1, q0, q2])]
    w = [x for x in w if x != right]
    return mcq("Divide: (%s) ÷ %s" % (num, dv), right, w, "Divide <b>every</b> term by %s: <b>%s</b>." % (dv, right))


def one_bin(r):
    p, q = r.sample([n for n in range(-9, 10) if n], 2)
    num = poly([1, p + q, p * q])
    right = lin(1, q)
    w = [lin(1, -q), lin(1, p), lin(1, p + q)]
    w = [x for x in w if x != right]
    return mcq("Divide: (%s) ÷ (%s)" % (num, lin(1, p)), right, w,
               "%s = (%s)(%s), so the quotient is <b>%s</b>." % (num, lin(1, p), lin(1, q), right))


def one_lead(r):
    a = r.choice([2, 3, 4, 5, -2, -3])
    s = r.choice([n for n in range(-9, 10) if n])
    p = r.choice([n for n in range(-8, 9) if n])
    if r.random() < 0.3:
        k = r.choice([2, 3, 4, 5, 6, -2, -3])
        num = lin(k, k * p)
        right = sg(k)
        w = [lin(k, 0), sg(k * p), lin(1, k)]
        e = "%s = %s(%s), so the quotient is <b>%s</b>." % (num, sg(k), lin(1, p), sg(k))
    else:
        num = poly([a, a * p + s, s * p])
        right = lin(a, s)
        w = [lin(a, -s), lin(1, s), lin(a, s * p)]
        e = "%s = (%s)(%s), so the quotient is <b>%s</b>." % (num, lin(1, p), right, right)
    w = [x for x in w if x != right]
    return mcq("Divide: (%s) ÷ (%s)" % (num, lin(1, p)), right, w, e)


def one_missing(r):
    p, q = r.sample([n for n in range(-9, 10) if n], 2)
    a = r.choice([1, 1, 2, 3])
    prod = poly([a, a * q + p, p * q])
    right = lin(a, p)
    w = [lin(a, -p), lin(1, p) if a != 1 else lin(1, p + q), lin(a, p * q)]
    w = [x for x in w if x != right]
    return mcq("(%s)(☐) = %s. What is the missing factor?" % (lin(1, q), prod), right, w,
               "Divide: (%s) ÷ (%s) = <b>%s</b>. Check by multiplying." % (prod, lin(1, q), right))


SHAPES = [("A rectangle has an area of {A} square units. Its width is ({w}) units. What is its length?", "units"),
          ("A garden has an area of {A} square feet. One side is ({w}) feet. How long is the other side?", "feet"),
          ("A rug covers {A} square feet. It is ({w}) feet wide. How long is it?", "feet"),
          ("A poster has an area of {A} square inches and a height of ({w}) inches. What is its width?", "inches"),
          ("A parking lot has an area of {A} square meters. Its length is ({w}) meters. What is its width?", "meters")]


def one_area(r):
    t, u = r.choice(SHAPES)
    p, q = r.randint(1, 9), r.choice([n for n in range(-5, 10) if n and n != 0])
    a = r.choice([1, 1, 2, 3])
    if p == q and a == 1:
        raise AssertionError
    A = poly([a, a * p + q, p * q])
    right = "(%s) %s" % (lin(a, q), u)
    w = ["(%s) %s" % (lin(a, -q), u), "(%s) %s" % (lin(1, q * p), u), "(%s) %s" % (lin(a, q + p), u)]
    w = [x for x in w if x != right]
    return mcq(t.format(A=A, w=lin(1, p)), right, w, "Length = area ÷ width = (%s) ÷ (%s) = <b>%s</b>." % (A, lin(1, p), lin(a, q)))


def build():
    sets, R = build_sets([
        ("Divide by a monomial", [("collect", uniq(one_mono), 20)]),
        ("Divide x² + bx + c by a binomial", [("collect", uniq(one_bin), 20)]),
        ("Leading coefficients and degree-one quotients", [("collect", uniq(one_lead), 20)]),
        ("Find the missing factor", [("collect", uniq(one_missing), 20)]),
        ("Area and length problems", [("collect", uniq(one_area), 20)]),
    ], 69515)
    finish(sets, R)
    body = lesson('<ul><li>To divide by a monomial, divide <b>every term</b>: (6<i>x</i><sup>2</sup> + 9<i>x</i>) ÷ 3<i>x</i> = 2<i>x</i> + 3.</li><li>To divide by a binomial factor, <b>factor</b> the dividend and cancel the common factor.</li><li>Check: quotient × divisor = dividend.</li></ul>',
        [example("(<i>x</i><sup>2</sup> + 7<i>x</i> + 12) ÷ (<i>x</i> + 3)", ["(<i>x</i> + 3)(<i>x</i> + 4)"], "<i>x</i> + 4")],
        [['Dividing only the first term', 'Every term is divided.'], ['Keeping the wrong sign', 'Check by multiplying.'], ['Adding the constants', 'Factor, then cancel.']])
    faq = [('What does TEKS A.10C ask?', 'Determine the quotient of a polynomial of degree one and polynomial of degree two when divided by a polynomial of degree one and polynomial of degree two when the degree of the divisor does not exceed the degree of the dividend.'), ('How do I check a division?', 'Multiply the quotient by the divisor.'), ('What if the divisor is not a factor?', 'On these worksheets it always is.'), ('Can I use long division?', 'Yes, but factoring is often faster.')]
    make('dividing-polynomials', 15, 'Number and Algebraic Methods', 'A.10C',
         'A.10C determine the quotient of a polynomial of degree one and polynomial of degree two when divided by a polynomial of degree one and polynomial of degree two when the degree of the divisor does not exceed the degree of the dividend',
         'Dividing Polynomials', 'Dividing Polynomials',
         'Free Algebra I worksheets for Texas TEKS A.10C: divide polynomials by monomials and binomial factors, find missing factors and solve area problems. 100 questions with answers.',
         'Factor the dividend, then cancel the divisor.', '(x² + 7x + 12) ÷ (x + 3) = x + 4',
         body, faq, sets, seo_title='Algebra I Dividing Polynomials Worksheets (TEKS A.10C)')


if __name__ == "__main__":
    build()
