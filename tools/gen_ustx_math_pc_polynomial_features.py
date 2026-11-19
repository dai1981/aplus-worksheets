# -*- coding: utf-8 -*-
"""
Texas Precalculus: Key Features of Polynomial Functions (TEKS P.2F, P.2I)
  python3 tools/gen_ustx_math_pc_polynomial_features.py
Zeros and multiplicity, matching graphs, rational roots and turning points (US Algebra 2 makers with a new seed), and
intervals of increase and decrease from turning points and y-intercepts, degree and turning points from factored
form (own makers).
Wrong answers come from real mistakes: changing the sign of a zero, using the leading coefficient as the y-intercept,
and counting the degree as the number of factors.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a2_polynomial_functions_and_zeros as pz
adopt(pz)
pz.R = random.Random(698050)
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


INF = "∞"


def iv(a, b):
    return "(%s, %s)" % (MINUS + INF if a is None else sg(a), INF if b is None else sg(b))


def one_turn(r):
    x1 = r.randint(-6, 2)
    x2 = r.randint(x1 + 2, 7)
    y1, y2 = r.randint(-9, 12), r.randint(-12, 9)
    up = r.random() < 0.5
    if up:
        y1 = max(y1, y2 + 3)
        desc = "a relative maximum at (%s, %s) and a relative minimum at (%s, %s)" % (sg(x1), sg(y1), sg(x2), sg(y2))
        inc = "%s ∪ %s" % (iv(None, x1), iv(x2, None))
        dec = iv(x1, x2)
    else:
        y2 = max(y2, y1 + 3)
        desc = "a relative minimum at (%s, %s) and a relative maximum at (%s, %s)" % (sg(x1), sg(y1), sg(x2), sg(y2))
        dec = "%s ∪ %s" % (iv(None, x1), iv(x2, None))
        inc = iv(x1, x2)
    want = r.choice(["increasing", "decreasing"])
    right = inc if want == "increasing" else dec
    other = dec if want == "increasing" else inc
    w = [other, iv(min(y1, y2), max(y1, y2)), "%s ∪ %s" % (iv(None, min(y1, y2)), iv(max(y1, y2), None)), iv(None, None)]
    w = [v for v in dict.fromkeys(w) if v != right]
    return mcq("The graph of a cubic function has %s, and no other turning points. On which interval(s) is it %s?" % (desc, want), right, w,
               "Before a maximum the graph rises and after it the graph falls; a minimum is the other way. Use the <i>x</i>-values for the intervals. <b>%s</b>." % right)


def fac(p):
    return "<i>x</i>" if p == 0 else "(<i>x</i> %s %d)" % (MINUS if p > 0 else "+", abs(p))


def one_feat(r):
    a = r.choice([1, 2, 3, -1, -2, 4])
    zs = r.sample([n for n in range(-6, 7) if n], r.choice([2, 3]))
    ms = [r.choice([1, 1, 2, 3]) for _ in zs]
    co = "" if a == 1 else (MINUS if a == -1 else sg(a))
    f = fx(co + "".join(fac(z) + ("<sup>%d</sup>" % m if m > 1 else "") for z, m in zip(zs, ms)))
    deg = sum(ms)
    kind = r.choice(["yint", "deg", "turn", "lead"])
    if kind == "yint":
        y = a
        for z, m in zip(zs, ms):
            y *= (-z) ** m
        if abs(y) > 5000:
            raise AssertionError
        right = "(0, %s)" % sg(y)
        alt = a
        for z, m in zip(zs, ms):
            alt *= z ** m
        w = ["(0, %s)" % sg(alt) if alt != y else "(0, %s)" % sg(-y) if y else "(0, 1)", "(0, %s)" % sg(a), "(%s, 0)" % sg(y)]
        q = "What is the <i>y</i>-intercept of %s?" % f
        e = "Put <i>x</i> = 0: " + " · ".join(["%s" % sg(a)] + ["(%s)%s" % (sg(-z), "<sup>%d</sup>" % m if m > 1 else "") for z, m in zip(zs, ms)]) + " = %s." % sg(y)
    elif kind == "deg":
        right = str(deg)
        w = [str(len(zs)), str(deg + 1), str(max(ms))]
        q = "What is the degree of %s?" % f
        e = "Add the exponents of the factors: " + " + ".join(str(m) for m in ms) + " = %d." % deg
    elif kind == "turn":
        right = str(deg - 1)
        w = [str(deg), str(deg + 1), str(len(zs))]
        q = "What is the greatest number of turning points the graph of %s can have?" % f
        e = "The degree is %d, so there are at most %d − 1 = %d turning points." % (deg, deg, deg - 1)
    else:
        lead = a
        right = sg(lead)
        w = [sg(-lead), str(deg), sg(lead * deg) if lead * deg != lead else "0"]
        q = "What is the leading coefficient of %s when it is multiplied out?" % f
        e = "Each factor starts with <i>x</i>, so the leading term is %s<i>x</i><sup>%d</sup>." % (sg(lead) if abs(lead) != 1 else ("" if lead == 1 else MINUS), deg)
    if right in w:
        w = [v for v in w if v != right]
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Zeros and multiplicity", [("collect", W(pz.one_zero), 20)]),
        ("Increasing and decreasing intervals", [("collect", uniq(one_turn), 20)]),
        ("Degree, intercepts and turning points", [("collect", uniq(one_feat), 20)]),
        ("Match the graph", [("collect", W(pz.one_graph), 20)]),
        ("Rational zeros and turning points", [("collect", W(pz.one_rrt), 20)]),
    ], 69805)
    finish(sets, R)
    body = lesson('<ul><li>A factor (<i>x</i> − <i>c</i>) gives a zero at <i>x</i> = <i>c</i>. An odd multiplicity crosses the <i>x</i>-axis; an even multiplicity touches and turns.</li><li>The degree is the sum of the exponents of the factors. A degree-<i>n</i> polynomial has at most <i>n</i> − 1 turning points.</li><li>The <i>y</i>-intercept is <i>f</i>(0).</li><li>Between turning points the graph is increasing or decreasing. Write the intervals with <i>x</i>-values.</li></ul>',
        [example("<i>f</i>(<i>x</i>) = 2(<i>x</i> − 1)<sup>2</sup>(<i>x</i> + 3)", ["Zeros 1 (touch) and −3 (cross)", "Degree 3", "<i>f</i>(0) = 2(1)(3) = 6"], "<i>y</i>-intercept (0, 6)")],
        [['Changing the sign of a zero', '(<i>x</i> + 3) gives <i>x</i> = −3.'], ['Using the leading coefficient as the <i>y</i>-intercept', 'Find <i>f</i>(0).'], ['Counting factors as the degree', 'Add the exponents.']])
    faq = [('What does TEKS P.2I ask?', 'Determine and analyze the key features of functions such as domain, range, symmetry, relative maximum, relative minimum, zeros, asymptotes, and intervals over which the function is increasing or decreasing.'), ('What is a relative maximum?', 'A point higher than the points just around it.'), ('Why use open intervals for increasing?', 'At a turning point the graph is neither increasing nor decreasing.'), ('Can a cubic have no turning points?', 'Yes, for example x³.')]
    make('key-features-of-polynomial-functions', 5, 'Functions', 'P.2F, P.2I',
         'P.2F graph exponential, logarithmic, rational, polynomial, power, trigonometric, inverse trigonometric, and piecewise defined functions, including step functions; P.2I determine and analyze the key features of exponential, logarithmic, rational, polynomial, power, trigonometric, inverse trigonometric, and piecewise defined functions, including step functions such as domain, range, symmetry, relative maximum, relative minimum, zeros, asymptotes, and intervals over which the function is increasing or decreasing',
         'Key Features of Polynomial Functions', 'Polynomial Key Features',
         'Free Precalculus worksheets on polynomial key features for Texas TEKS P.2F and P.2I: zeros and multiplicity, turning points, increasing and decreasing intervals, degree and intercepts. 100 questions with answers.',
         'Odd multiplicity crosses; even multiplicity touches.', 'Degree n: at most n − 1 turning points.',
         body, faq, sets, seo_title='Precalculus Key Features of Polynomial Functions Worksheets (TEKS P.2F, P.2I)')


if __name__ == "__main__":
    build()
