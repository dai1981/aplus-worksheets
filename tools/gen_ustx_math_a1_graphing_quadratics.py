# -*- coding: utf-8 -*-
"""
Texas Algebra I: Graphing Quadratic Functions: Vertex, Axis, Zeros and Intercepts (TEKS A.7A, A.7B)
  python3 tools/gen_ustx_math_a1_graphing_quadratics.py
Reading features from a graph, the vertex and axis from standard form, zeros, intercepts and shape (US Algebra 1
makers with a new seed and Texas names), linear factors and zeros (own maker), and quadratic graph problems.
Wrong answers come from real mistakes: using b/(2a) without the minus, reading the y-intercept as a zero, and
taking +3 from (x + 3) as a zero.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a1_graphing_quadratic_functions as gq
adopt(gq)
gq.R = random.Random(695170)
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



def fac(z):
    return X if z == 0 else "(%s %s %d)" % (X, MINUS if z > 0 else "+", abs(z))


def one_fz(r):
    r1, r2 = r.sample(range(-9, 10), 2)
    a = r.choice([1, 1, 2, -1, 3])
    lead = "" if a == 1 else (MINUS if a == -1 else str(a))
    if r.random() < 0.55:
        q = "What are the zeros of <i>f</i>(<i>x</i>) = %s%s%s?" % (lead, fac(r1), fac(r2))
        right = "%s and %s" % (sg(min(r1, r2)), sg(max(r1, r2)))
        w = ["%s and %s" % (sg(min(-r1, -r2)), sg(max(-r1, -r2))), "%s and %s" % (sg(min(r1, -r2)), sg(max(r1, -r2))), "%s and %s" % (sg(a * r1 * r2), sg(a))]
        e = "Set each factor to 0: <i>x</i> = %s or <i>x</i> = %s. The zeros are <b>%s</b>." % (sg(r1), sg(r2), right)
    else:
        q = "The graph of a quadratic function crosses the <i>x</i>-axis at %s and %s. Which is a factor of the function?" % (sg(r1), sg(r2))
        right = fac(r1)
        w = [fac(-r1), fac(-r2), "(%s %s %d)" % (X, "+" if r1 * r2 >= 0 else MINUS, abs(r1 * r2)) if r1 * r2 else fac(r1 + r2 + 1)]
        e = "A zero at %s gives the factor <b>%s</b>." % (sg(r1), right)
    w = [x for x in w if x != right]
    return mcq(q, right, w, e)


def build():
    sets, R = build_sets([
        ("Read features from a graph", [("collect", W(gq.one_read), 20)]),
        ("Vertex and axis from standard form", [("collect", W(gq.one_std), 20)]),
        ("Zeros, intercepts and shape", [("collect", W(gq.one_feature), 20)]),
        ("Linear factors and zeros", [("collect", uniq(one_fz), 20)]),
        ("Quadratic graph problems", [("run", PR(gq.problems), ("rnd",), 10), ("collect", uniq(one_fz), 10)]),
    ], 69517)
    finish(sets, R)
    body = lesson('<ul><li>For <i>f</i>(<i>x</i>) = <i>ax</i><sup>2</sup> + <i>bx</i> + <i>c</i>, the <b>axis of symmetry</b> is <i>x</i> = −<i>b</i> ÷ (2<i>a</i>). Put it in to get the <b>vertex</b>.</li><li><i>a</i> &gt; 0: opens up, minimum. <i>a</i> &lt; 0: opens down, maximum.</li><li>The <b><i>y</i>-intercept</b> is <i>c</i>. The <b>zeros</b> are the <i>x</i>-intercepts.</li><li>Each linear factor (<i>x</i> − <i>r</i>) gives a zero at <i>x</i> = <i>r</i>.</li></ul>',
        [example("<i>f</i>(<i>x</i>) = <i>x</i><sup>2</sup> − 6<i>x</i> + 5", ["axis <i>x</i> = 6 ÷ 2 = 3", "<i>f</i>(3) = −4", "(<i>x</i> − 1)(<i>x</i> − 5)"], "vertex (3, −4), zeros 1 and 5")],
        [['Forgetting the minus in −<i>b</i>/(2<i>a</i>)', 'For −6<i>x</i>, the axis is <i>x</i> = 3.'], ['Calling the <i>y</i>-intercept a zero', 'Zeros are on the <i>x</i>-axis.'], ['Taking the sign from the factor', '(<i>x</i> + 3) gives the zero −3.']])
    faq = [('What does TEKS A.7A ask?', 'Graph quadratic functions on the coordinate plane and use the graph to identify key attributes, if possible, including x-intercept, y-intercept, zeros, maximum value, minimum values, vertex, and the equation of the axis of symmetry.'), ('What does TEKS A.7B ask?', 'Describe the relationship between the linear factors of quadratic expressions and the zeros of their associated quadratic functions.'), ('Can a parabola have no zeros?', 'Yes, if it never touches the x-axis.'), ('Where is the axis of symmetry?', 'Through the vertex, halfway between the zeros.')]
    make('graphing-quadratic-functions', 17, 'Quadratic Functions and Equations', 'A.7A, A.7B',
         'A.7A graph quadratic functions on the coordinate plane and use the graph to identify key attributes, if possible, including x-intercept, y-intercept, zeros, maximum value, minimum values, vertex, and the equation of the axis of symmetry; A.7B describe the relationship between the linear factors of quadratic expressions and the zeros of their associated quadratic functions',
         'Graphing Quadratic Functions: Vertex, Axis, Zeros and Intercepts', 'Graphing Quadratic Functions',
         'Free Algebra I worksheets for Texas TEKS A.7A and A.7B: graph quadratic functions, find the vertex, axis of symmetry, zeros and intercepts, and link factors to zeros. 100 questions with answers.',
         'Axis x = −b ÷ 2a; zeros come from the factors.', '(x − 1)(x − 5): zeros 1 and 5, vertex (3, −4).',
         body, faq, sets, seo_title='Algebra I Graphing Quadratic Functions Worksheets (TEKS A.7A)')


if __name__ == "__main__":
    build()
