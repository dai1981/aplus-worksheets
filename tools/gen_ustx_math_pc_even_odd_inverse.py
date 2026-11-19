# -*- coding: utf-8 -*-
"""
Texas Precalculus: Even and Odd Functions and Inverse Functions (TEKS P.2D, P.2E)
  python3 tools/gen_ustx_math_pc_even_odd_inverse.py
Testing functions for even and odd symmetry with f(−x) and with points (own makers), finding inverses and checking
them by composition (US Algebra 2 makers with a new seed), and inverses from tables (own maker).
Wrong answers come from real mistakes: calling a function odd because it has an odd power, forgetting the constant
term, and reading f⁻¹ as 1/f.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a2_composition_and_inverse_functions as ci
adopt(ci)
ci.R = random.Random(698020)
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


EO = ["Even", "Odd", "Neither even nor odd", "Both even and odd"]


def one_eo(r):
    kind = r.choice(["even", "odd", "neither", "neither"])
    if kind == "even":
        pw = r.sample([2, 4, 6], r.choice([1, 2])) + [0]
    elif kind == "odd":
        pw = r.sample([1, 3, 5], r.choice([1, 2, 3]))
    else:
        pw = r.sample([1, 3, 5], 1) + r.sample([0, 2, 4], r.choice([1, 2]))
    pw = sorted(set(pw), reverse=True)
    deg = max(pw)
    cs = [0] * (deg + 1)
    for p in pw:
        cs[deg - p] = r.choice([n for n in range(-9, 10) if n])
    f = fx(poly(cs))
    neg = [c * (-1) ** (deg - i) for i, c in enumerate(cs)]
    right = {"even": EO[0], "odd": EO[1], "neither": EO[2]}[kind]
    why = {"even": "<i>f</i>(−<i>x</i>) = <i>f</i>(<i>x</i>): the graph is symmetric about the <i>y</i>-axis.", "odd": "<i>f</i>(−<i>x</i>) = −<i>f</i>(<i>x</i>): the graph is symmetric about the origin.",
           "neither": "<i>f</i>(−<i>x</i>) is neither <i>f</i>(<i>x</i>) nor −<i>f</i>(<i>x</i>)."}[kind]
    return mcq("Is %s even, odd or neither?" % f, right, [v for v in EO if v != right], "<i>f</i>(−<i>x</i>) = %s. %s <b>%s</b>." % (poly(neg), why, right))


def one_eo2(r):
    a = r.randint(1, 9)
    b = r.choice([n for n in range(-12, 13) if n])
    kind = r.choice(["even", "odd"])
    t = r.randrange(3)
    if t == 0:
        right = sg(b) if kind == "even" else sg(-b)
        w = [sg(-b) if kind == "even" else sg(b), sg(a), sg(-a), "0"]
        q = "<i>f</i> is an %s function and <i>f</i>(%d) = %s. What is <i>f</i>(−%d)?" % (kind, a, sg(b), a)
        e = "%s, so <i>f</i>(−%d) = %s." % ("Even: <i>f</i>(−<i>x</i>) = <i>f</i>(<i>x</i>)" if kind == "even" else "Odd: <i>f</i>(−<i>x</i>) = −<i>f</i>(<i>x</i>)", a, right)
    elif t == 1:
        P = lambda x, y: "(%s, %s)" % (sg(x), sg(y))
        right = P(-a, b) if kind == "even" else P(-a, -b)
        w = [P(a, -b), P(-a, -b) if kind == "even" else P(-a, b), P(b, a)]
        q = "The point %s is on the graph of an %s function. Which point must also be on the graph?" % (P(a, b), kind)
        e = "%s: (<i>x</i>, <i>y</i>) → %s." % ("Mirror over the <i>y</i>-axis" if kind == "even" else "Turn halfway around the origin", "(−<i>x</i>, <i>y</i>)" if kind == "even" else "(−<i>x</i>, −<i>y</i>)")
    else:
        if kind == "even":
            right = "The graph is symmetric about the <i>y</i>-axis"
        else:
            right = "The graph is symmetric about the origin"
        w = ["The graph is symmetric about the <i>x</i>-axis", "The graph is symmetric about the line <i>y</i> = <i>x</i>", "The graph is symmetric about the origin" if kind == "even" else "The graph is symmetric about the <i>y</i>-axis"]
        q = "<i>f</i>(%d) = %s and <i>f</i>(−%d) = %s, and the same is true for every input. Which statement is true?" % (a, sg(b), a, sg(b if kind == "even" else -b))
        e = "%s for every <i>x</i> means <i>f</i> is %s." % ("<i>f</i>(−<i>x</i>) = <i>f</i>(<i>x</i>)" if kind == "even" else "<i>f</i>(−<i>x</i>) = −<i>f</i>(<i>x</i>)", kind)
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def tab(xs, ys, nm="f"):
    return "<table class='sn-table'><tr><th><i>x</i></th>%s</tr><tr><th><i>%s</i>(<i>x</i>)</th>%s</tr></table>" % ("".join("<td>%s</td>" % sg(v) for v in xs), nm, "".join("<td>%s</td>" % sg(v) for v in ys))


def one_invt(r):
    xs = sorted(r.sample(range(-6, 10), 5))
    ys = r.sample(range(-9, 20), 5)
    kind = r.choice(["find", "find", "comp", "yes", "no"])
    if kind == "no":
        i, j = r.sample(range(5), 2)
        ys[j] = ys[i]
    t = tab(xs, ys)
    if kind == "find":
        i = r.randrange(5)
        right = sg(xs[i])
        w = [sg(ys[i]), sg(ys[(i + 1) % 5]), ft(Fr(1, ys[i])) if ys[i] else "1"]
        w += [sg(xs[(i + 1) % 5])]
        return mcq(t + "Use the table. What is <i>f</i><sup>−1</sup>(%s)?" % sg(ys[i]), right, w,
                   "<i>f</i><sup>−1</sup>(%s) is the input that gives %s. In the table, <i>f</i>(%s) = %s. <b>%s</b>." % (sg(ys[i]), sg(ys[i]), sg(xs[i]), sg(ys[i]), right))
    if kind == "comp":
        i = r.randrange(5)
        right = sg(xs[i])
        w = [sg(ys[i]), sg(xs[(i + 2) % 5]), sg(ys[(i + 2) % 5])]
        return mcq(t + "Use the table. What is <i>f</i><sup>−1</sup>(<i>f</i>(%s))?" % sg(xs[i]), right, w,
                   "An inverse undoes <i>f</i>: <i>f</i><sup>−1</sup>(<i>f</i>(<i>x</i>)) = <i>x</i>. <b>%s</b>." % right)
    right = "Yes, every output comes from only one input" if kind == "yes" else "No, two inputs give the same output"
    w = ["No, two inputs give the same output" if kind == "yes" else "Yes, every output comes from only one input", "Yes, because every input has an output", "No, because some outputs are negative"]
    return mcq(t + "Does <i>f</i> have an inverse function?", right, w, "An inverse function exists only when <i>f</i> is one-to-one: no output repeats. <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Even, odd or neither?", [("collect", uniq(one_eo), 20)]),
        ("Use symmetry", [("collect", uniq(one_eo2), 20)]),
        ("Find the inverse of a function", [("collect", W(ci.one_inv), 20)]),
        ("Inverses from tables", [("collect", uniq(one_invt), 20)]),
        ("Check inverses with composition", [("collect", W(ci.one_check), 20)]),
    ], 69802)
    finish(sets, R)
    body = lesson('<ul><li><b>Even</b>: <i>f</i>(−<i>x</i>) = <i>f</i>(<i>x</i>). The graph is symmetric about the <i>y</i>-axis.</li><li><b>Odd</b>: <i>f</i>(−<i>x</i>) = −<i>f</i>(<i>x</i>). The graph is symmetric about the origin.</li><li>A polynomial with only even powers (and a constant) is even; with only odd powers it is odd.</li><li>An inverse function exists when <i>f</i> is one-to-one. Swap <i>x</i> and <i>y</i> and solve for <i>y</i>. Check with <i>f</i>(<i>f</i><sup>−1</sup>(<i>x</i>)) = <i>x</i>.</li></ul>',
        [example("<i>f</i>(<i>x</i>) = <i>x</i><sup>3</sup> − 4<i>x</i>", ["<i>f</i>(−<i>x</i>) = −<i>x</i><sup>3</sup> + 4<i>x</i> = −<i>f</i>(<i>x</i>)"], "Odd")],
        [['Odd because of one odd power', '<i>x</i><sup>3</sup> + 2 is neither: the constant is an even power.'], ['Mixing up the symmetries', 'Even: <i>y</i>-axis. Odd: origin.'], ['Reading <i>f</i><sup>−1</sup> as 1/<i>f</i>', '<i>f</i><sup>−1</sup> is the inverse function.']])
    faq = [('What does TEKS P.2D ask?', 'Describe symmetry of graphs of even and odd functions.'), ('What does TEKS P.2E ask?', 'Determine an inverse function, when it exists, for a given function over its domain or a subset of its domain and represent the inverse using multiple representations.'), ('Can a function be both even and odd?', 'Only f(x) = 0.'), ('Why does an even function have no inverse?', 'f(−a) = f(a), so two inputs give the same output (unless the domain is restricted).')]
    make('even-odd-and-inverse-functions', 2, 'Functions', 'P.2D, P.2E',
         'P.2D describe symmetry of graphs of even and odd functions; P.2E determine an inverse function, when it exists, for a given function over its domain or a subset of its domain and represent the inverse using multiple representations',
         'Even and Odd Functions and Inverse Functions', 'Even, Odd and Inverse Functions',
         'Free Precalculus worksheets for Texas TEKS P.2D and P.2E: even and odd functions, symmetry, inverse functions from equations and tables, and checking inverses. 100 questions with answers.',
         'Even: f(−x) = f(x). Odd: f(−x) = −f(x).', 'An inverse exists when no output repeats.',
         body, faq, sets, seo_title='Precalculus Even, Odd and Inverse Functions Worksheets (TEKS P.2D, P.2E)')


if __name__ == "__main__":
    build()
