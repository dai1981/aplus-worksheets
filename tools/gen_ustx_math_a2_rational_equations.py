# -*- coding: utf-8 -*-
"""
Texas Algebra II: Rational Equations and Inverse Variation (TEKS 2A.6H, 2A.6I, 2A.6J, 2A.6L)
  python3 tools/gen_ustx_math_a2_rational_equations.py
Solving rational equations, extraneous solutions and rate and work problems (US Algebra 2 makers with a new seed),
and writing and solving inverse variation equations (own makers).
Wrong answers come from real mistakes: keeping a value that makes a denominator 0, adding rates the wrong way, and
using direct variation instead of inverse variation.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a2_rational_and_radical_equations as rr
adopt(rr)
rr.R = random.Random(697180)
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


def kx(k):
    return "<i>y</i> = <span class='fr'><span class='fn'>%s</span><span class='fd'><i>x</i></span></span>" % comma(k)


def one_ivk(r):
    x = r.choice([2, 3, 4, 5, 6, 8, 10, 12])
    y = r.choice([n for n in range(2, 16) if n != x])
    k = x * y
    if r.random() < 0.5:
        q = "<i>y</i> varies inversely with <i>x</i>, and <i>y</i> = %d when <i>x</i> = %d. What is the constant of variation <i>k</i>?" % (y, x)
        right = str(k)
        w = [ft(Fr(y, x)), ft(Fr(x, y)), str(x + y), str(k * 2)]
        e = "Inverse variation: <i>xy</i> = <i>k</i>. <i>k</i> = %d × %d = <b>%d</b>." % (x, y, k)
    else:
        q = "<i>y</i> varies inversely with <i>x</i>, and <i>y</i> = %d when <i>x</i> = %d. Write the equation." % (y, x)
        right = kx(k)
        w = ["<i>y</i> = %d<i>x</i>" % k, "<i>y</i> = <span class='fr'><span class='fn'><i>x</i></span><span class='fd'>%d</span></span>" % k, "<i>y</i> = %s<i>x</i>" % ft(Fr(y, x))]
        e = "<i>k</i> = <i>xy</i> = %d, so <b>%s</b>." % (k, right)
    return mcq(q, right, w, e)


def one_ivf(r):
    k = r.choice([12, 18, 24, 30, 36, 48, 60, 72, 84, 90, 96, 120, 144, 180])
    ds = [d for d in range(2, 25) if k % d == 0 and k // d > 1]
    x1, x2 = r.sample(ds, 2)
    y1, y2 = k // x1, k // x2
    right = str(y2)
    w = [ft(Fr(y1 * x2, x1)), str(k * x2) if k * x2 < 10000 else str(y2 + 1), str(y1 + x1 - x2) if y1 + x1 - x2 > 0 else str(y2 + 2), str(x2)]
    return mcq("<i>y</i> varies inversely with <i>x</i>. If <i>y</i> = %d when <i>x</i> = %d, find <i>y</i> when <i>x</i> = %d." % (y1, x1, x2), right, w,
               "<i>k</i> = %d × %d = %d. <i>y</i> = %d ÷ %d = <b>%d</b>." % (x1, y1, k, k, x2, y2))


CTX = [("A trip takes {y1} hours at {x1} mph. The time varies inversely with the speed. How many hours does it take at {x2} mph?", " hours"),
       ("{x1} volunteers can clean a park in {y1} hours. The time varies inversely with the number of volunteers. How many hours would {x2} volunteers take?", " hours"),
       ("The cost per person to rent a bus varies inversely with the number of people. With {x1} people, each pays ${y1}. How much does each pay with {x2} people?", ""),
       ("A gas has a volume of {y1} liters at a pressure of {x1} atmospheres. Volume varies inversely with pressure. What is the volume at {x2} atmospheres, in liters?", " liters"),
       ("The number of slices each person gets varies inversely with the number of people. With {x1} people, each gets {y1} slices. How many slices does each get with {x2} people?", " slices"),
       ("A pump empties a tank in {y1} minutes when {x1} pumps are used. Time varies inversely with the number of pumps. How many minutes do {x2} pumps take?", " minutes"),
       ("The length of a rectangle with a fixed area varies inversely with its width. The length is {y1} cm when the width is {x1} cm. What is the length when the width is {x2} cm?", " cm")]


def one_ivw(r):
    t, unit_ = r.choice(CTX)
    k = r.choice([24, 36, 48, 60, 72, 90, 120, 144, 180, 240, 300, 360])
    ds = [d for d in range(2, 61) if k % d == 0 and 1 < k // d < 200]
    x1, x2 = r.sample(ds, 2)
    if "mph" in t and (x1 < 20 or x2 < 20):
        raise AssertionError
    if ("volunteers" in t or "pumps" in t or "people" in t) and (x1 > 30 or x2 > 30):
        raise AssertionError
    y1, y2 = k // x1, k // x2
    q = t.format(x1=x1, y1=y1, x2=x2)
    pre = "$" if "$" in t else ""
    f = lambda v: "%s%s%s" % (pre, ft(v), unit_)
    w = [f(Fr(y1 * x2, x1)), f(Fr(y1 + x1 - x2)) if y1 + x1 - x2 > 0 else f(Fr(y2 + 3)), f(Fr(y2 + 1)), f(Fr(k))]
    return mcq(q, f(y2), w, "<i>k</i> = %d × %d = %d. Then %d ÷ %d = <b>%s</b>." % (x1, y1, k, k, x2, f(y2)))


def build():
    sets, R = build_sets([
        ("Solve proportions with rational expressions", [("collect", W(rr.one_prop), 20)]),
        ("Extraneous solutions of rational equations", [("collect", W(rr.one_ext), 20)]),
        ("Rational equation word problems", [("collect", W(rr.one_word), 20)]),
        ("Inverse variation equations", [("collect", uniq(one_ivk), 10), ("collect", uniq(one_ivf), 10)]),
        ("Inverse variation word problems", [("collect", uniq(one_ivw), 20)]),
    ], 69718)
    finish(sets, R)
    body = lesson("<ul><li>To solve a rational equation, multiply both sides by the least common denominator. Then solve.</li><li><b>Check</b>: a value that makes any denominator 0 is extraneous.</li><li>Work problems: rates add. If one person takes 3 hours, the rate is <span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span> job per hour.</li><li><b>Inverse variation</b>: <i>y</i> = <span class='fr'><span class='fn'><i>k</i></span><span class='fd'><i>x</i></span></span>, so <i>xy</i> = <i>k</i>. As one goes up, the other goes down.</li></ul>",
        [example("<i>y</i> = 8 when <i>x</i> = 3; find <i>y</i> when <i>x</i> = 6", ["<i>k</i> = 3 × 8 = 24", "24 ÷ 6 = 4"], "<i>y</i> = 4")],
        [['Keeping a value that makes a denominator 0', 'Check every answer in the original equation.'], ['Adding times instead of rates', 'Add 1/3 + 1/6, not 3 + 6.'], ['Using direct variation', 'Inverse: multiply <i>x</i> and <i>y</i> to get <i>k</i>.']])
    faq = [('What does TEKS 2A.6H ask?', 'Formulate rational equations that model real-world situations.'), ('What do TEKS 2A.6I and 2A.6J ask?', 'Solve rational equations that have real solutions, and determine the reasonableness of a solution to a rational equation.'), ('What does TEKS 2A.6L ask?', 'Formulate and solve equations involving inverse variation.'), ('What does the graph of an inverse variation look like?', 'A curve like y = k/x with asymptotes on both axes.')]
    make('rational-equations-and-inverse-variation', 18, 'Cubic, Cube Root, Absolute Value, and Rational Functions, Equations, and Inequalities', '2A.6H, 2A.6I, 2A.6J, 2A.6L',
         '2A.6H formulate rational equations that model real-world situations; 2A.6I solve rational equations that have real solutions; 2A.6J determine the reasonableness of a solution to a rational equation; 2A.6L formulate and solve equations involving inverse variation',
         'Rational Equations and Inverse Variation', 'Rational Equations',
         'Free Algebra II worksheets for Texas TEKS 2A.6H to 2A.6L: solve rational equations, extraneous solutions, work and rate problems, and inverse variation. 100 questions with answers.',
         'Multiply by the LCD, solve, and check for extraneous solutions.', 'Inverse variation: xy = k.',
         body, faq, sets, seo_title='Algebra II Rational Equations and Inverse Variation Worksheets (TEKS 2A.6H–2A.6L)')


if __name__ == "__main__":
    build()
