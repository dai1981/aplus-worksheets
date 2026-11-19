# -*- coding: utf-8 -*-
"""
Texas Algebra I: Domain and Range (TEKS A.2A, A.6A, A.9A)
  python3 tools/gen_ustx_math_a1_domain_range.py
Domain and range from ordered pairs, graphs and rules, inequality and interval notation, and reasonable domain and
range in real situations (the US Algebra 1 makers with a new seed and Texas names).
Wrong answers come from real mistakes: swapping domain and range, using parentheses for included endpoints, and
allowing negative times or counts.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a1_domain_and_range as dr
adopt(dr)
dr.R = random.Random(695020)
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
        ("Domain and range of ordered pairs", [("collect", W(dr.one_pairs), 20)]),
        ("Domain and range from graphs", [("collect", W(dr.one_graph), 20)]),
        ("Domain and range from rules", [("collect", W(dr.one_rule), 20)]),
        ("Inequality and interval notation", [("collect", W(dr.one_interval), 20)]),
        ("Reasonable domain and range", [("run", PR(dr.problems), ("rnd",), 10), ("collect", W(dr.one_rule), 10)]),
    ], 69502)
    finish(sets, R)
    body = lesson('<ul><li>The <b>domain</b> is all the inputs (<i>x</i>-values). The <b>range</b> is all the outputs (<i>y</i>-values).</li><li>A linear function like <i>f</i>(<i>x</i>) = 2<i>x</i> + 1 has all real numbers for both.</li><li>A quadratic opening up has range <i>y</i> ≥ the <i>y</i>-value of the vertex.</li><li>An exponential function <i>f</i>(<i>x</i>) = <i>ab</i><sup><i>x</i></sup> with <i>a</i> &gt; 0 has range <i>y</i> &gt; 0.</li><li>In real situations, keep only values that make sense: no negative time, whole numbers for people.</li></ul>',
        [example("<i>f</i>(<i>x</i>) = (<i>x</i> − 2)<sup>2</sup> + 3", ["vertex (2, 3), opens up"], "domain: all real numbers; range: <i>y</i> ≥ 3")],
        [['Swapping domain and range', 'Domain is <i>x</i>; range is <i>y</i>.'], ['Using ( ) for an included endpoint', 'Use [ ] when the endpoint is included.'], ['Allowing impossible values in context', 'Time and counts cannot be negative.']])
    faq = [('What does TEKS A.2A ask?', 'Determine the domain and range of a linear function in mathematical problems; determine reasonable domain and range values for real-world situations, both continuous and discrete; and represent domain and range using inequalities.'), ('What does TEKS A.6A ask?', 'Determine the domain and range of quadratic functions and represent the domain and range using inequalities.'), ('What does TEKS A.9A ask?', 'Determine the domain and range of exponential functions of the form f(x) = ab<sup>x</sup> and represent the domain and range using inequalities.'), ('What is a discrete domain?', 'Separate values only, like whole numbers of tickets.')]
    make('domain-and-range', 2, 'Linear Functions, Equations, and Inequalities', 'A.2A, A.6A, A.9A',
         'A.2A determine the domain and range of a linear function in mathematical problems; determine reasonable domain and range values for real-world situations, both continuous and discrete; and represent domain and range using inequalities; A.6A determine the domain and range of quadratic functions and represent the domain and range using inequalities; A.9A determine the domain and range of exponential functions of the form f(x) = ab^x and represent the domain and range using inequalities',
         'Domain and Range', 'Domain and Range',
         'Free Algebra I domain and range worksheets for Texas TEKS A.2A, A.6A and A.9A: ordered pairs, graphs, linear, quadratic and exponential rules, inequality notation and reasonable values in context. 100 questions with answers.',
         'Domain: the x-values. Range: the y-values.', 'y = (x − 2)² + 3 has range y ≥ 3.',
         body, faq, sets, seo_title='Algebra I Domain and Range Worksheets (TEKS A.2A)')


if __name__ == "__main__":
    build()
