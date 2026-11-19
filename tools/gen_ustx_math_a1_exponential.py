# -*- coding: utf-8 -*-
"""
Texas Algebra I: Exponential Functions: Growth and Decay (TEKS A.9B, A.9C, A.9D)
  python3 tools/gen_ustx_math_a1_exponential.py
Reading a and b in f(x) = ab^x, evaluating and comparing tables, writing exponential models, compound interest and
depreciation, and exponential problems (the US Algebra 1 makers with a new seed and Texas names).
Wrong answers come from real mistakes: multiplying a and b first, using r instead of 1 + r, and treating a growth
factor of 0.8 as growth.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a1_exponential_growth_and_decay as eg
adopt(eg)
eg.R = random.Random(695210)
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
        ("Read an exponential model", [("collect", W(eg.one_read), 20)]),
        ("Evaluate and compare tables", [("collect", W(eg.one_eval), 20)]),
        ("Write an exponential model", [("collect", W(eg.one_write), 20)]),
        ("Compound interest and depreciation", [("collect", W(eg.one_money), 20)]),
        ("Exponential growth and decay problems", [("run", PR(eg.problems), ("rnd",), 10), ("collect", W(eg.one_write), 10)]),
    ], 69521)
    finish(sets, R)
    body = lesson('<ul><li>In <i>f</i>(<i>x</i>) = <i>ab</i><sup><i>x</i></sup>, <i>a</i> is the <b>starting value</b> and <i>b</i> is the <b>growth factor</b>.</li><li><i>b</i> &gt; 1: growth. 0 &lt; <i>b</i> &lt; 1: decay.</li><li>Growth by <i>r</i> percent: <i>b</i> = 1 + <i>r</i>. Decay by <i>r</i> percent: <i>b</i> = 1 − <i>r</i>.</li><li>The graph has <i>y</i>-intercept <i>a</i> and never touches the <i>x</i>-axis.</li></ul>',
        [example("$500 grows 4% a year", ["<i>b</i> = 1.04"], "<i>f</i>(<i>t</i>) = 500(1.04)<sup><i>t</i></sup>")],
        [['Multiplying <i>a</i> and <i>b</i> first', 'Raise <i>b</i> to the power, then multiply by <i>a</i>.'], ['Using <i>r</i> instead of 1 + <i>r</i>', '4% growth is 1.04.'], ['Calling 0.8 growth', '<i>b</i> &lt; 1 is decay.']])
    faq = [('What does TEKS A.9B ask?', 'Interpret the meaning of the values of a and b in exponential functions of the form f(x) = ab<sup>x</sup> in real-world problems.'), ('What does TEKS A.9C ask?', 'Write exponential functions in the form f(x) = ab<sup>x</sup> (where b is a rational number) to describe problems arising from mathematical and real-world situations, including growth and decay.'), ('What does TEKS A.9D ask?', 'Graph exponential functions that model growth and decay and identify key features, including y-intercept and asymptote, in mathematical and real-world problems.'), ('What is the asymptote of y = 3(2)<sup>x</sup>?', 'The x-axis, y = 0.')]
    make('exponential-functions', 21, 'Exponential Functions and Equations', 'A.9B, A.9C, A.9D',
         'A.9B interpret the meaning of the values of a and b in exponential functions of the form f(x) = ab^x in real-world problems; A.9C write exponential functions in the form f(x) = ab^x (where b is a rational number) to describe problems arising from mathematical and real-world situations, including growth and decay; A.9D graph exponential functions that model growth and decay and identify key features, including y-intercept and asymptote, in mathematical and real-world problems',
         'Exponential Functions: Growth and Decay', 'Exponential Functions',
         'Free Algebra I worksheets for Texas TEKS A.9B–A.9D: exponential growth and decay, the meaning of a and b, writing f(x) = ab^x, compound interest and graphs. 100 questions with answers.',
         'f(x) = ab^x: a starts it, b multiplies it.', '4% growth: b = 1.04. 20% decay: b = 0.8.',
         body, faq, sets, seo_title='Algebra I Exponential Functions Worksheets (TEKS A.9C)')


if __name__ == "__main__":
    build()
