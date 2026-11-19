# -*- coding: utf-8 -*-
"""
Texas Algebra II: Square Root Functions and Equations (TEKS 2A.4C, 2A.4F, 2A.4G)
  python3 tools/gen_ustx_math_a2_square_root_functions.py
Transformations of f(x) = √x: shifts, stretches and reflections (US Algebra 2 makers with a new seed, kept to the
square root parent) and f(bx) (own maker), plus solving square root equations and finding extraneous solutions (US
Algebra 2 makers with a new seed).
Wrong answers come from real mistakes: shifting the wrong way, multiplying x by b instead of dividing, and keeping an
extraneous solution.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a2_transformations_of_functions as tr
adopt(tr)
tr.R = random.Random(697110)
import gen_us_math_a2_rational_and_radical_equations as rr
adopt(rr)
rr.R = random.Random(697111)
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


def fam(fn, *kinds):
    """Use a US Algebra 2 transformation maker with only some parent functions."""
    def f(r):
        old = tr.PARENTS
        tr.PARENTS = {k: v for k, v in old.items() if k in kinds}
        try:
            return fn(r)
        finally:
            tr.PARENTS = old
    f.__name__ = fn.__name__
    return f


def bfrac(b):
    b = Fr(b)
    return ft(b)


def one_bx_maker(kinds):
    def one_bx(r):
        kind = r.choice(kinds)
        b = r.choice([Fr(2), Fr(3), Fr(4), Fr(1, 2), Fr(1, 3), Fr(-1), Fr(-2)])
        if kind == "abs" and b < 0:
            raise AssertionError
        base = {"sqrt": "√<i>x</i>", "cube": "<i>x</i><sup>3</sup>", "cbrt": "∛<i>x</i>", "abs": "|<i>x</i>|"}[kind]
        bx = ("−" if b == -1 else ft(b)) + "<i>x</i>" if b.denominator == 1 else "%s<i>x</i>" % ft(b)
        g = {"sqrt": "√(%s)" % bx, "cube": "(%s)<sup>3</sup>" % bx, "cbrt": "∛(%s)" % bx, "abs": "|%s|" % bx}[kind]
        ab = abs(b)
        if r.random() < 0.55:
            parts = []
            if ab > 1:
                parts.append("horizontal shrink by a factor of %s" % ft(1 / ab))
            elif ab < 1:
                parts.append("horizontal stretch by a factor of %s" % ft(1 / ab))
            if b < 0:
                parts.append("reflection over the <i>y</i>-axis")
            right = " and ".join(parts)
            right = right[0].upper() + right[1:]
            w = []
            if ab != 1:
                w.append(("Horizontal stretch by a factor of %s" if ab > 1 else "Horizontal shrink by a factor of %s") % ft(ab))
                w.append("Vertical shrink by a factor of %s" % ft(1 / ab) if ab > 1 else "Vertical stretch by a factor of %s" % ft(1 / ab))
            w.append("Shift %s %s" % ("left" if b > 0 else "right", ft(ab)))
            w.append("Shift %s %s" % ("right" if b > 0 else "left", ft(ab)))
            if b == -1:
                w.append("Horizontal stretch by a factor of 2")
            return mcq("How is the graph of <i>g</i>(<i>x</i>) = %s related to the graph of <i>f</i>(<i>x</i>) = %s?" % (g, base), right, w,
                       "Replacing <i>x</i> with <i>bx</i> changes the graph sideways: every <i>x</i>-coordinate is divided by <i>b</i> = %s. <b>%s</b>." % (ft(b), right))
        pts = {"sqrt": [(1, 1), (4, 2), (9, 3), (16, 4)], "cube": [(1, 1), (2, 8), (-1, -1), (-2, -8)], "cbrt": [(1, 1), (8, 2), (-8, -2), (27, 3), (-1, -1)], "abs": [(2, 2), (-3, 3), (4, 4), (-6, 6), (6, 6)]}[kind]
        x0, y0 = r.choice(pts)
        P = lambda x, y: "(%s, %s)" % (ft(x), ft(y))
        right = P(Fr(x0) / b, y0)
        w = [P(Fr(x0) * b, y0), P(x0, Fr(y0) * b), P(Fr(x0) / b, Fr(y0) / b), P(x0 + b, y0)]
        return mcq("The point %s is on the graph of <i>f</i>(<i>x</i>) = %s. Which point is on the graph of <i>g</i>(<i>x</i>) = %s?" % (P(x0, y0), base, g), right, w,
                   "<i>g</i>(%s) = <i>f</i>(%s · %s) = <i>f</i>(%s) = %s. Divide the <i>x</i>-coordinate by %s and keep the <i>y</i>-coordinate. <b>%s</b>." % (ft(Fr(x0) / b), ft(b), ft(Fr(x0) / b), sg(x0), sg(y0), ft(b), right))
    return one_bx


one_bx = one_bx_maker(["sqrt"])


def sq_only(it):
    return "√" in it["q"] and "∛" not in it["q"]


def build():
    sets, R = build_sets([
        ("Shifts of f(x) = √x", [("collect", W(fam(tr.one_desc, "sqrt")), 20)]),
        ("Write the transformed function", [("collect", W(fam(tr.one_write, "sqrt")), 20)]),
        ("Match the graph and f(bx)", [("collect", W(fam(tr.one_graph, "sqrt")), 10), ("collect", uniq(one_bx), 10)]),
        ("Solve square root equations", [("collect", W(rr.one_rad, sq_only), 20)]),
        ("Extraneous solutions", [("collect", W(rr.one_radext), 20)]),
    ], 69711)
    finish(sets, R)
    body = lesson('<ul><li><i>g</i>(<i>x</i>) = <i>a</i>√(<i>b</i>(<i>x</i> − <i>c</i>)) + <i>d</i> starts at the point (<i>c</i>, <i>d</i>).</li><li><i>x</i> − <i>c</i> moves the graph right <i>c</i>; + <i>d</i> moves it up <i>d</i>.</li><li><i>a</i> stretches or shrinks it vertically; a negative <i>a</i> reflects it over the <i>x</i>-axis. <i>bx</i> divides every <i>x</i>-coordinate by <i>b</i>; a negative <i>b</i> reflects it over the <i>y</i>-axis.</li><li>To solve a square root equation, get the root alone, square both sides, and <b>check</b> every answer: squaring can add extraneous solutions.</li></ul>',
        [example("√(<i>x</i> + 3) = <i>x</i> − 3", ["<i>x</i> + 3 = <i>x</i><sup>2</sup> − 6<i>x</i> + 9", "<i>x</i> = 1 or <i>x</i> = 6", "Check: <i>x</i> = 1 gives 2 = −2 ✗"], "<i>x</i> = 6")],
        [['Shifting the wrong way', '√(<i>x</i> − 4) moves right 4.'], ['Multiplying by <i>b</i>', '√(2<i>x</i>) divides the <i>x</i>-coordinates by 2.'], ['Not checking', 'An answer that makes the root negative is extraneous.']])
    faq = [('What does TEKS 2A.4C ask?', 'Determine the effect on the graph of f(x) = √x when f(x) is replaced by af(x), f(x) + d, f(bx), and f(x − c) for specific positive and negative values of a, b, c, and d.'), ('What does TEKS 2A.4G ask?', 'Identify extraneous solutions of square root equations.'), ('Why do extraneous solutions appear?', 'Squaring both sides can turn a false equation like 2 = −2 into a true one, 4 = 4.'), ('What is the domain of √(x − 3)?', 'x ≥ 3.')]
    make('square-root-functions-and-equations', 11, 'Quadratic and Square Root Functions, Equations, and Inequalities', '2A.4C, 2A.4F, 2A.4G',
         '2A.4C determine the effect on the graph of f(x) = √x when f(x) is replaced by af(x), f(x) + d, f(bx), and f(x − c) for specific positive and negative values of a, b, c, and d; 2A.4F solve quadratic and square root equations; 2A.4G identify extraneous solutions of square root equations',
         'Square Root Functions and Equations', 'Square Root Functions',
         'Free Algebra II square root function worksheets for Texas TEKS 2A.4C, 2A.4F and 2A.4G: transformations of √x, solving square root equations and extraneous solutions. 100 questions with answers.',
         'Square both sides, then check every answer.', '√(x − c) + d starts at (c, d).',
         body, faq, sets, seo_title='Algebra II Square Root Functions and Equations Worksheets (TEKS 2A.4C, 2A.4F, 2A.4G)')


if __name__ == "__main__":
    build()
