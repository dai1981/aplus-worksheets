# -*- coding: utf-8 -*-
"""
Texas Algebra II: Polynomial Operations and Division (TEKS 2A.7B, 2A.7C)
  python3 tools/gen_ustx_math_a2_polynomial_operations.py
Adding, subtracting and multiplying polynomials and dividing by a quadratic (own makers), plus long division and
synthetic division (US Algebra 2 makers with a new seed).
Wrong answers come from real mistakes: changing the sign of only the first term when subtracting, adding exponents
wrong, and forgetting a term when multiplying.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a2_polynomial_division_and_remainder_theorem as pd
adopt(pd)
pd.R = random.Random(697200)
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


def pmul(p, q):
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def padd(p, q, s=1):
    n = max(len(p), len(q))
    p = [0] * (n - len(p)) + p
    q = [0] * (n - len(q)) + q
    return [a + s * b for a, b in zip(p, q)]


def rp(r, deg, lo=-9, hi=9):
    cs = [r.choice([n for n in range(lo, hi + 1) if n])] + [r.randint(lo, hi) for _ in range(deg)]
    return cs


def one_as(r):
    p, q = rp(r, 3), rp(r, r.choice([2, 3]))
    sub = r.random() < 0.6
    right = poly(padd(p, q, -1 if sub else 1))
    qq = [0] * (4 - len(q)) + q
    first = [qq[0]] + [-c for c in qq[1:]]
    w = [poly(padd(p, q, 1 if sub else -1)), poly(padd(p, first if sub else [-qq[0]] + qq[1:], 1)) if sub else poly(padd(p, q, 1)[:-1] + [p[-1]]),
         poly(padd(p, [-c for c in qq[:-1]] + [qq[-1]], 1)) if sub else poly([x for x in padd(p, q, 1)[:-1]] + [p[-1] - q[-1]])]
    w = [v for v in dict.fromkeys(w) if v != right]
    if len(w) < 3:
        w.append(poly(padd(padd(p, q, -1 if sub else 1), [1], 1)))
    return mcq("Simplify (%s) %s (%s)." % (poly(p), MINUS if sub else "+", poly(q)), right, w,
               ("Change the sign of <b>every</b> term in the second polynomial, then combine like terms: " if sub else "Combine like terms (same power of <i>x</i>): ") + "<b>%s</b>." % right)


def one_mul(r):
    kind = r.choice(["bt", "bt", "three", "sq"])
    if kind == "bt":
        p, q = [r.choice([1, 2, 3, -1]), r.choice([n for n in range(-6, 7) if n])], rp(r, 2, -6, 6)
        q[0] = r.choice([1, 2, -1, 3])
        txt = "(%s)(%s)" % (poly(p), poly(q))
    elif kind == "three":
        a, b, c = [r.choice([n for n in range(-5, 6) if n]) for _ in range(3)]
        p, q = pmul([1, a], [1, b]), [1, c]
        txt = "(%s)(%s)(%s)" % (poly([1, a]), poly([1, b]), poly([1, c]))
    else:
        a = r.choice([n for n in range(-5, 6) if n])
        p, q = pmul([1, a], [1, a]), [1, a]
        txt = "(%s)<sup>3</sup>" % poly([1, a])
    prod = pmul(p, q)
    right = poly(prod)
    w1 = prod[:]
    w1[1] = w1[1] + (2 if w1[1] != -2 else 3)
    w2 = prod[:]
    w2[-1] = -w2[-1] if w2[-1] else 1
    w3 = prod[:]
    w3[-2] = 0 if w3[-2] else 5
    w4 = pmul([p[0], 0], q)
    w = [poly(w1), poly(w2), poly(w3), poly(padd(w4, [p[1] * q[-1]] if len(p) == 2 else [0]))]
    w = [v for v in dict.fromkeys(w) if v != right]
    return mcq("Multiply %s." % txt, right, w, "Multiply every term by every term, then combine like terms: <b>%s</b>." % right)


def one_div2(r):
    p, q = r.choice([n for n in range(-5, 6) if n]), r.randint(-6, 6)
    d = [1, p, q]
    quo = [r.choice([1, 2, 3, -1]), r.randint(-6, 6), r.randint(-6, 6)]
    rem = [0, 0] if r.random() < 0.65 else [0, r.choice([n for n in range(-6, 7) if n])]
    if rem[1] == 0 and r.random() < 0.3:
        quo = [r.choice([1, 2, -1]), r.randint(-6, 6)]
    num = padd(pmul(d, quo), rem, 1)
    if all(c == 0 for c in num[1:]):
        raise AssertionError
    right = poly(quo) + ((", remainder %s" % sg(rem[1])) if rem[1] else "")
    wq = quo[:]
    wq[-1] = wq[-1] + 1
    wq2 = quo[:]
    wq2[1 if len(quo) > 2 else 0] = -wq2[1 if len(quo) > 2 else 0] if wq2[1 if len(quo) > 2 else 0] else 2
    w = [poly(wq) + ((", remainder %s" % sg(rem[1])) if rem[1] else ""), poly(wq2) + ((", remainder %s" % sg(rem[1])) if rem[1] else ""),
         poly(quo) + (", remainder %s" % sg(-rem[1]) if rem[1] else ", remainder %s" % sg(q)), poly([quo[0]] + [c + 1 for c in quo[1:]])]
    w = [v for v in dict.fromkeys(w) if v != right]
    return mcq("Divide (%s) ÷ (%s)." % (poly(num), poly(d)), right, w,
               "Use long division: divide the leading terms, multiply (%s) by that term, subtract, and repeat. Check: (%s)(%s)%s = %s. <b>%s</b>." % (
                   poly(d), poly(d), poly(quo), (" + (%s)" % sg(rem[1])) if rem[1] else "", poly(num), right))


def build():
    sets, R = build_sets([
        ("Add and subtract polynomials", [("collect", uniq(one_as), 20)]),
        ("Multiply polynomials", [("collect", uniq(one_mul), 20)]),
        ("Divide by a monomial or a binomial", [("collect", W(pd.one_long), 20)]),
        ("Synthetic division", [("collect", W(pd.one_syn), 20)]),
        ("Divide by a quadratic", [("collect", uniq(one_div2), 20)]),
    ], 69720)
    finish(sets, R)
    body = lesson('<ul><li>Add or subtract <b>like terms</b>: same power of <i>x</i>. When subtracting, change the sign of every term in the second polynomial.</li><li>To multiply, multiply every term by every term, then combine like terms.</li><li>Long division: divide the leading terms, multiply, subtract, bring down, repeat.</li><li>Synthetic division works for divisors <i>x</i> − <i>c</i>. Check: quotient × divisor + remainder = dividend.</li></ul>',
        [example("(<i>x</i><sup>3</sup> + 2<i>x</i><sup>2</sup> − 5<i>x</i> − 6) ÷ (<i>x</i><sup>2</sup> − <i>x</i> − 2)", ["<i>x</i><sup>3</sup> ÷ <i>x</i><sup>2</sup> = <i>x</i>", "Subtract <i>x</i><sup>3</sup> − <i>x</i><sup>2</sup> − 2<i>x</i>: 3<i>x</i><sup>2</sup> − 3<i>x</i> − 6", "3<i>x</i><sup>2</sup> ÷ <i>x</i><sup>2</sup> = 3"], "<i>x</i> + 3")],
        [['Changing only the first sign', '−(2<i>x</i><sup>2</sup> − 3<i>x</i> + 1) = −2<i>x</i><sup>2</sup> + 3<i>x</i> − 1.'], ['Missing a product', 'A binomial times a trinomial has 6 products.'], ['Skipping a missing power', 'Write 0<i>x</i> for a missing term before dividing.']])
    faq = [('What does TEKS 2A.7B ask?', 'Add, subtract, and multiply polynomials.'), ('What does TEKS 2A.7C ask?', 'Determine the quotient of a polynomial of degree three and of degree four when divided by a polynomial of degree one and of degree two.'), ('When can you use synthetic division?', 'When the divisor is x − c.'), ('How do you check a division?', 'Multiply the quotient by the divisor and add the remainder.')]
    make('polynomial-operations-and-division', 20, 'Number and Algebraic Methods', '2A.7B, 2A.7C',
         '2A.7B add, subtract, and multiply polynomials; 2A.7C determine the quotient of a polynomial of degree three and of degree four when divided by a polynomial of degree one and of degree two',
         'Polynomial Operations and Division', 'Polynomial Operations',
         'Free Algebra II polynomial worksheets for Texas TEKS 2A.7B and 2A.7C: add, subtract and multiply polynomials, long division, synthetic division and dividing by a quadratic. 100 questions with answers.',
         'Subtracting changes the sign of every term.', 'Check: quotient × divisor + remainder = dividend.',
         body, faq, sets, seo_title='Algebra II Polynomial Operations and Division Worksheets (TEKS 2A.7B, 2A.7C)')


if __name__ == "__main__":
    build()
