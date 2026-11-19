# -*- coding: utf-8 -*-
"""
Texas Algebra II: Absolute Value Functions, Equations and Inequalities (TEKS 2A.6C, 2A.6D, 2A.6E, 2A.6F)
  python3 tools/gen_ustx_math_a2_absolute_value.py
Transformations of f(x) = |x| (US Algebra 2 makers with a new seed, kept to the absolute value parent, and own f(bx)
maker), writing absolute value equations and inequalities from words (own maker), and solving absolute value
equations and inequalities (US Algebra 1 makers with a new seed).
Wrong answers come from real mistakes: solving only one case, writing an “and” answer for |x| > a, and missing that
|x| = −3 has no solution.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a2_transformations_of_functions as tr
adopt(tr)
tr.R = random.Random(697160)
import gen_us_math_a1_absolute_value_equations_and_inequalities as av
adopt(av)
av.R = random.Random(697161)
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


one_bx = one_bx_maker(["abs"])

CTX = [("The temperature in a greenhouse must stay within {d}°F of {c}°F.", "<i>t</i>", "le"), ("A box of cereal should weigh {c} ounces, with an error of at most {d} ounces.", "<i>w</i>", "le"),
       ("A bolt must be {c} mm long, within {d} mm.", "<i>L</i>", "le"), ("A guess is wrong by more than {d} from the real number of {c}.", "<i>g</i>", "gt"),
       ("A thermostat is set to {c}°F. The heater turns on when the temperature is more than {d}°F away from it.", "<i>t</i>", "gt"), ("A swimmer's lap time is {c} seconds, give or take {d} seconds.", "<i>s</i>", "le"),
       ("Two numbers are each exactly {d} away from {c} on the number line.", "<i>x</i>", "eq"), ("A store's goal is {c} sales a day. A day counts as unusual if sales are at least {d} away from the goal.", "<i>n</i>", "ge"),
       ("A diver's target depth is {c} feet. She must stay within {d} feet of it.", "<i>d</i>", "le"), ("A cyclist rides {d} miles from mile marker {c} in one direction.", "<i>m</i>", "eq")]
S_ = {"le": "≤", "gt": "&gt;", "eq": "=", "ge": "≥"}


def one_form(r):
    t, v, s = r.choice(CTX)
    c = r.randint(8, 90)
    d = r.randint(2, 9)
    txt = t.format(c=c, d=d)
    right = "|%s − %d| %s %d" % (v, c, S_[s], d)
    alt = {"le": "≥", "gt": "&lt;", "eq": "≠", "ge": "&lt;"}[s]
    w = ["|%s − %d| %s %d" % (v, d, S_[s], c), "|%s − %d| %s %d" % (v, c, alt, d), "|%s + %d| %s %d" % (v, c, S_[s], d), "%s − %d %s %d" % (v, c, S_[s], d)]
    if s == "eq":
        lo, hi = c - d, c + d
        e = "Distance from %d is |%s − %d|, and it equals %d: the values are %d and %d." % (c, v, c, d, lo, hi)
    else:
        e = "The distance from %s to %d is |%s − %d|. %s means %s." % (v, c, v, c, {"le": "Within / at most", "gt": "More than", "ge": "At least"}[s], S_[s])
    return mcq(txt + " Which %s describes %s?" % ("equation" if s == "eq" else "inequality", v), right, w, e + " <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Transformations of f(x) = |x|", [("collect", W(fam(tr.one_desc, "abs")), 7), ("collect", W(fam(tr.one_graph, "abs")), 7), ("collect", uniq(one_bx), 6)]),
        ("Write absolute value equations and inequalities", [("collect", uniq(one_form), 20)]),
        ("Solve absolute value equations", [("collect", W(av.one_basic), 10), ("collect", W(av.one_multi), 10)]),
        ("Solve |ax + b| < c", [("collect", W(av.one_less), 20)]),
        ("Solve |ax + b| > c", [("collect", W(av.one_greater), 20)]),
    ], 69716)
    finish(sets, R)
    body = lesson('<ul><li><i>g</i>(<i>x</i>) = <i>a</i>|<i>b</i>(<i>x</i> − <i>c</i>)| + <i>d</i> has its vertex at (<i>c</i>, <i>d</i>). A negative <i>a</i> opens down.</li><li>|<i>x</i> − <i>c</i>| is the distance from <i>x</i> to <i>c</i>. “Within <i>d</i>” means |<i>x</i> − <i>c</i>| ≤ <i>d</i>.</li><li>|<i>A</i>| = <i>k</i> (<i>k</i> &gt; 0) gives two equations: <i>A</i> = <i>k</i> or <i>A</i> = −<i>k</i>. |<i>A</i>| = negative has no solution.</li><li>|<i>A</i>| &lt; <i>k</i>: −<i>k</i> &lt; <i>A</i> &lt; <i>k</i> (and). |<i>A</i>| &gt; <i>k</i>: <i>A</i> &lt; −<i>k</i> or <i>A</i> &gt; <i>k</i> (or).</li></ul>',
        [example("|2<i>x</i> − 3| ≤ 7", ["−7 ≤ 2<i>x</i> − 3 ≤ 7", "−4 ≤ 2<i>x</i> ≤ 10"], "−2 ≤ <i>x</i> ≤ 5"), example("Within 4 of 70", ["Distance from 70 is |<i>t</i> − 70|"], "|<i>t</i> − 70| ≤ 4")],
        [['Solving only one case', '|<i>x</i> − 2| = 5 gives 7 and −3.'], ['Using and for &gt;', '|<i>x</i>| &gt; 3 means <i>x</i> &lt; −3 or <i>x</i> &gt; 3.'], ['Solving |<i>A</i>| = −3', 'An absolute value is never negative: no solution.']])
    faq = [('What does TEKS 2A.6C ask?', 'Analyze the effect on the graphs of f(x) = |x| when f(x) is replaced by af(x), f(bx), f(x − c), and f(x) + d for specific positive and negative real values of a, b, c, and d.'), ('What does TEKS 2A.6D ask?', 'Formulate absolute value linear equations.'), ('What do TEKS 2A.6E and 2A.6F ask?', 'Solve absolute value linear equations and solve absolute value linear inequalities.'), ('Why does |x − c| mean distance?', 'It is how far x is from c on the number line.')]
    make('absolute-value-functions-equations-and-inequalities', 16, 'Cubic, Cube Root, Absolute Value, and Rational Functions, Equations, and Inequalities', '2A.6C, 2A.6D, 2A.6E, 2A.6F',
         '2A.6C analyze the effect on the graphs of f(x) = |x| when f(x) is replaced by af(x), f(bx), f(x − c), and f(x) + d for specific positive and negative real values of a, b, c, and d; 2A.6D formulate absolute value linear equations; 2A.6E solve absolute value linear equations; 2A.6F solve absolute value linear inequalities',
         'Absolute Value Functions, Equations and Inequalities', 'Absolute Value',
         'Free Algebra II absolute value worksheets for Texas TEKS 2A.6C to 2A.6F: transformations of |x|, writing and solving absolute value equations and inequalities. 100 questions with answers.',
         '|x − c| is the distance from x to c.', '|A| < k: and. |A| > k: or.',
         body, faq, sets, seo_title='Algebra II Absolute Value Functions, Equations and Inequalities Worksheets (TEKS 2A.6C–2A.6F)')


if __name__ == "__main__":
    build()
