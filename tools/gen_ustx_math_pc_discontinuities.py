# -*- coding: utf-8 -*-
"""
Texas Precalculus: Discontinuities and One-Sided Behavior (TEKS P.2L, P.2M)
  python3 tools/gen_ustx_math_pc_discontinuities.py
Classifying removable, jump and infinite discontinuities, finding holes, left and right behavior at a jump, and what a
graphing calculator hides (own makers), plus holes and vertical asymptotes (US Precalculus maker with a new seed).
Wrong answers come from real mistakes: calling a hole an asymptote, giving the y-value of a hole as 0, and trusting a
calculator graph that hides a hole.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_pc_rational_functions_and_asymptotes as ra
adopt(ra)
ra.R = random.Random(698080)
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


def lin_(d):
    return X if d == 0 else "(%s %s %d)" % (X, MINUS if d > 0 else "+", abs(d))


def fr_(t, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (t, b)


TYPES = ["Removable (a hole)", "Infinite (a vertical asymptote)", "Jump", "No discontinuity"]


def one_type(r):
    c = r.choice([n for n in range(-6, 7) if n])
    d = r.choice([n for n in range(-6, 7) if n and n != c])
    kind = r.choice(["hole", "inf", "jump", "none"])
    if kind == "hole":
        f = fx(fr_(lin_(c) + lin_(d), lin_(c)))
        right, e = TYPES[0], "(<i>x</i> %s %d) cancels, so the graph is the line <i>y</i> = <i>x</i> %s %d with a hole at <i>x</i> = %s." % (MINUS if c > 0 else "+", abs(c), MINUS if d > 0 else "+", abs(d), sg(c))
    elif kind == "inf":
        f = fx(fr_(lin_(d), lin_(c)))
        right, e = TYPES[1], "The bottom is 0 at <i>x</i> = %s but the top is not, so the graph shoots up or down there." % sg(c)
    elif kind == "jump":
        a = r.randint(-5, 5)
        b = a + r.choice([n for n in range(-6, 7) if n])
        f = "<i>f</i>(<i>x</i>) = %s if <i>x</i> &lt; %s, and <i>f</i>(<i>x</i>) = %s if <i>x</i> ≥ %s" % (poly([1, a - c]), sg(c), poly([1, b - c]), sg(c))
        right, e = TYPES[2], "The pieces give %s and %s at <i>x</i> = %s: the graph jumps." % (sg(a), sg(b), sg(c))
    else:
        a = r.randint(-5, 5)
        f = "<i>f</i>(<i>x</i>) = %s if <i>x</i> &lt; %s, and <i>f</i>(<i>x</i>) = %s if <i>x</i> ≥ %s" % (poly([1, a - c]), sg(c), poly([2, a - 2 * c]), sg(c))
        right, e = TYPES[3], "Both pieces give %s at <i>x</i> = %s, so the graph is connected there." % (sg(a), sg(c))
    return mcq("What kind of discontinuity does %s have at <i>x</i> = %s?" % (f, sg(c)), right, [v for v in TYPES if v != right], e + " <b>%s</b>." % right)


def one_hole(r):
    c = r.choice([n for n in range(-6, 7) if n])
    d, e_ = r.sample([n for n in range(-7, 8) if n != c], 2)
    a = r.choice([1, 2, 3])
    y = Fr(a * (c - d), c - e_)
    top = poly([a, -a * (c + d), a * c * d])
    bot = poly([1, -(c + e_), c * e_])
    f = fx(fr_(top, bot))
    P = lambda x, v: "(%s, %s)" % (ft(x), ft(v))
    right = P(c, y)
    w = [P(c, 0), P(-c, y), P(e_, Fr(a * (e_ - d), 1)) if e_ != d else P(e_, 1), P(d, 0)]
    w = [v for v in dict.fromkeys(w) if v != right]
    return mcq("Where is the hole in the graph of %s?" % f, right, w,
               "Factor: %s ÷ (%s%s). (<i>x</i> %s %d) cancels, leaving %s. Put <i>x</i> = %s into it: %s. <b>%s</b>." % (
                   ("%d" % a if a > 1 else "") + lin_(c) + lin_(d), lin_(c), lin_(e_), MINUS if c > 0 else "+", abs(c), fr_(("%d" % a if a > 1 else "") + lin_(d), lin_(e_)), sg(c), ft(y), right))


def one_sides(r):
    c = r.randint(-4, 4)
    m1, m2 = r.choice([1, 2, -1, 3]), r.choice([1, -2, 2, -1])
    a, b = r.randint(-6, 6), r.randint(-6, 6)
    L, Rv = m1 * c + a, m2 * c + b
    if L == Rv:
        raise AssertionError
    f = "<i>f</i>(<i>x</i>) = %s if <i>x</i> &lt; %s, and <i>f</i>(<i>x</i>) = %s if <i>x</i> ≥ %s" % (poly([m1, a]), sg(c), poly([m2, b]), sg(c))
    T = lambda p, q: "From the left, <i>f</i>(<i>x</i>) → %s; from the right, <i>f</i>(<i>x</i>) → %s" % (sg(p), sg(q))
    right = T(L, Rv)
    w = [T(Rv, L), T(L, L), T(Rv, Rv)]
    return mcq("%s. Describe the behavior of <i>f</i> as <i>x</i> → %s from each side." % (f, sg(c)), right, w,
               "Left side uses %s: %s. Right side uses %s: %s. <b>%s</b>." % (poly([m1, a]), sg(L), poly([m2, b]), sg(Rv), right))


def one_calc(r):
    c = r.choice([n for n in range(-6, 7) if n])
    d = r.choice([n for n in range(-6, 7) if n and n != -c])
    if r.random() < 0.6:
        top = poly([1, d - c, -c * d])
        f = fx(fr_(top, poly([1, -c])))
        line = poly([1, d])
        q = "A graphing calculator shows the graph of %s as the straight line <i>y</i> = %s with no break. What is really true at <i>x</i> = %s?" % (f, line, sg(c))
        right = "There is a hole at (%s, %s)" % (sg(c), sg(c + d))
        w = ["The graph is the line with no hole", "There is a vertical asymptote at <i>x</i> = %s" % sg(c), "There is a hole at (%s, 0)" % sg(c)]
        e = "<i>f</i>(%s) is undefined (0 ÷ 0), but the screen is too coarse to show a single missing point." % sg(c)
    else:
        f = fx(fr_(str(abs(d)), poly([1, -c])))
        q = "On some calculators, the graph of %s shows a nearly vertical line at <i>x</i> = %s. What is that line?" % (f, sg(c))
        right = "Not part of the graph: there is a vertical asymptote at <i>x</i> = %s" % sg(c)
        w = ["Part of the graph that connects the two sides", "A hole at <i>x</i> = %s" % sg(c), "A horizontal asymptote at <i>y</i> = %s" % sg(c)]
        e = "The calculator joins a very large and a very small value with a line; the function is undefined at <i>x</i> = %s." % sg(c)
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Types of discontinuities", [("collect", uniq(one_type), 20)]),
        ("Find the hole", [("collect", uniq(one_hole), 20)]),
        ("Holes and vertical asymptotes", [("collect", W(ra.one_va), 20)]),
        ("Left and right behavior at a jump", [("collect", uniq(one_sides), 20)]),
        ("What a graphing calculator hides", [("collect", uniq(one_calc), 20)]),
    ], 69808)
    finish(sets, R)
    body = lesson('<ul><li>A function is <b>continuous</b> at <i>x</i> = <i>c</i> when you can draw through it without lifting your pencil.</li><li><b>Removable</b> discontinuity (hole): a factor cancels from the top and bottom.</li><li><b>Infinite</b> discontinuity: the bottom is 0 but the top is not (a vertical asymptote).</li><li><b>Jump</b>: a piecewise function whose pieces give different values at the boundary. Compare the left and right sides.</li><li>A graphing calculator may hide a hole or draw a false line at an asymptote.</li></ul>',
        [example("<i>f</i>(<i>x</i>) = <span class='fr'><span class='fn'><i>x</i><sup>2</sup> − 9</span><span class='fd'><i>x</i> − 3</span></span>", ["(<i>x</i> − 3)(<i>x</i> + 3) ÷ (<i>x</i> − 3) = <i>x</i> + 3", "<i>x</i> = 3 gives 6"], "Hole at (3, 6)")],
        [['Calling a hole an asymptote', 'If the factor cancels, it is a hole.'], ['Giving the hole a <i>y</i>-value of 0', 'Put <i>x</i> into the simplified function.'], ['Trusting the calculator screen', 'Check the algebra.']])
    faq = [('What does TEKS P.2L ask?', 'Determine various types of discontinuities in the interval (−∞, ∞) as they relate to functions and explore the limitations of the graphing calculator as it relates to the behavior of the function around discontinuities.'), ('What does TEKS P.2M ask?', 'Describe the left and right-sided behavior of the graph of a function around discontinuities.'), ('Can a hole be filled?', "Yes. Defining f(c) as the hole's y-value makes the function continuous."), ('Is 1/x continuous?', 'It is continuous on its domain but has an infinite discontinuity at x = 0.')]
    make('discontinuities', 8, 'Functions', 'P.2L, P.2M',
         'P.2L determine various types of discontinuities in the interval (−∞, ∞) as they relate to functions and explore the limitations of the graphing calculator as it relates to the behavior of the function around discontinuities; P.2M describe the left and right-sided behavior of the graph of a function around discontinuities',
         'Discontinuities and One-Sided Behavior', 'Discontinuities',
         'Free Precalculus worksheets on discontinuities for Texas TEKS P.2L and P.2M: removable, jump and infinite discontinuities, holes, one-sided behavior and calculator limits. 100 questions with answers.',
         'A factor that cancels makes a hole; one that does not makes an asymptote.', 'A jump: the left and right values differ.',
         body, faq, sets, seo_title='Precalculus Discontinuities Worksheets (TEKS P.2L, P.2M)')


if __name__ == "__main__":
    build()
