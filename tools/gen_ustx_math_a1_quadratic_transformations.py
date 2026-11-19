# -*- coding: utf-8 -*-
"""
Texas Algebra I: Transformations of Quadratic Functions (TEKS A.7C)
  python3 tools/gen_ustx_math_a1_quadratic_transformations.py
Describing and writing transformations of f(x) = x², moving points, and matching graphs (US Algebra 2 makers with a
new seed, kept to the quadratic parent), plus narrower, wider, up or down (own maker).
Wrong answers come from real mistakes: shifting left for (x − h)², thinking a = 1/2 makes the graph narrower, and
mixing up up and down.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a2_transformations_of_functions as tr
adopt(tr)
tr.R = random.Random(695190)
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


from fractions import Fraction as Fr


def sq_only(it):
    t = it["q"] + " ".join(it["c"])
    return ("<sup>2</sup>" in t or "²" in t) and not any(s in t for s in ("|", "√", "³", "<sup>3</sup>", "1/<i>x</i>"))


AS = [Fr(2), Fr(3), Fr(4), Fr(1, 2), Fr(1, 3), Fr(1, 4), Fr(-1), Fr(-2), Fr(-3), Fr(-1, 2)]


def ft(v):
    if v.denominator != 1:
        return (MINUS if v < 0 else "") + fr(abs(v.numerator), v.denominator)
    return sg(int(v))


def words(a, d):
    s = ["narrower" if abs(a) > 1 else ("wider" if abs(a) < 1 else "the same width"), "opens down" if a < 0 else "opens up"]
    if d:
        s.append("vertex moved %s %d" % ("up" if d > 0 else "down", abs(d)))
    t = ", ".join(s)
    return t[0].upper() + t[1:]


def one_eff(r):
    a = r.choice(AS)
    d = r.choice([n for n in range(-6, 7)])
    lead = "" if a == 1 else (MINUS if a == -1 else ft(a))
    g = "%s%s<sup>2</sup>" % (lead, X) + ((" %s %d" % ("+" if d > 0 else MINUS, abs(d))) if d else "")
    right = words(a, d)
    w = [words(1 / a, d) if abs(a) != 1 else words(Fr(2) * (1 if a > 0 else -1), d), words(-a, d), words(a, -d) if d else words(a, 3)]
    w = [x for x in w if x != right]
    return mcq("Compared with <i>f</i>(<i>x</i>) = %s<sup>2</sup>, how is the graph of <i>g</i>(<i>x</i>) = %s different?" % (X, g), right, w,
               "|<i>a</i>| = %s is %s 1, so the graph is %s; <i>a</i> is %s; and %s. <b>%s</b>." % (ft(abs(a)), "greater than" if abs(a) > 1 else "less than", "narrower" if abs(a) > 1 else "wider", "negative, so it opens down" if a < 0 else "positive, so it opens up", "the vertex moves %s %d" % ("up" if d > 0 else "down", abs(d)) if d else "there is no shift", right))


def build():
    sets, R = build_sets([
        ("Describe the transformation", [("collect", W(tr.one_desc, sq_only), 20)]),
        ("Write the transformed function", [("collect", W(tr.one_write, sq_only), 20)]),
        ("Narrower, wider, up or down?", [("collect", uniq(one_eff), 20)]),
        ("Where does a point move?", [("collect", W(tr.one_point), 20)]),
        ("Match the graph", [("collect", W(tr.one_graph, sq_only), 20)]),
    ], 69519)
    finish(sets, R)
    body = lesson('<ul><li>The parent function is <i>f</i>(<i>x</i>) = <i>x</i><sup>2</sup>, vertex (0, 0).</li><li><i>f</i>(<i>x</i>) + <i>d</i>: up <i>d</i>. <i>f</i>(<i>x</i> − <i>c</i>): right <i>c</i>.</li><li><i>af</i>(<i>x</i>): |<i>a</i>| &gt; 1 is narrower, 0 &lt; |<i>a</i>| &lt; 1 is wider, <i>a</i> &lt; 0 opens down.</li><li><i>f</i>(<i>bx</i>) = (<i>bx</i>)<sup>2</sup> = <i>b</i><sup>2</sup><i>x</i><sup>2</sup>: |<i>b</i>| &gt; 1 is narrower.</li></ul>',
        [example("<i>g</i>(<i>x</i>) = −2(<i>x</i> − 3)<sup>2</sup> + 1", ["right 3, up 1", "−2: narrower, opens down"], "vertex (3, 1), narrower, opens down")],
        [['Shifting left for (<i>x</i> − <i>h</i>)<sup>2</sup>', 'Minus inside moves right.'], ['Thinking 1/2 makes it narrower', 'A small |<i>a</i>| makes it wider.'], ['Mixing up up and down', '+<i>d</i> outside moves up.']])
    faq = [('What does TEKS A.7C ask?', 'Determine the effects on the graph of the parent function f(x) = x<sup>2</sup> when f(x) is replaced by af(x), f(x) + d, f(x − c), f(bx) for specific values of a, b, c, and d.'), ('What is the vertex of (x − 4)<sup>2</sup> − 5?', '(4, −5).'), ('What does a = −1 do?', 'It flips the parabola to open down.'), ('Is f(2x) narrower or wider?', 'Narrower: f(2x) = 4x<sup>2</sup>.')]
    make('transformations-of-quadratic-functions', 19, 'Quadratic Functions and Equations', 'A.7C',
         'A.7C determine the effects on the graph of the parent function f(x) = x^2 when f(x) is replaced by af(x), f(x) + d, f(x − c), f(bx) for specific values of a, b, c, and d',
         'Transformations of Quadratic Functions', 'Transformations of Quadratic Functions',
         'Free Algebra I worksheets for Texas TEKS A.7C: transformations of f(x) = x² — shifts, stretches, compressions and reflections, moving points and matching graphs. 100 questions with answers.',
         'Inside moves sideways (opposite sign); outside moves up or down.', '−2(x − 3)² + 1: vertex (3, 1), narrower, opens down.',
         body, faq, sets, seo_title='Algebra I Transformations of Quadratic Functions Worksheets (TEKS A.7C)')


if __name__ == "__main__":
    build()
