# -*- coding: utf-8 -*-
"""
Texas Algebra II: Solving Quadratic Equations and Inequalities (TEKS 2A.4F, 2A.4H)
  python3 tools/gen_ustx_math_a2_quadratic_equations_inequalities.py
Solving quadratic equations by square roots (own maker), by the quadratic formula (US Algebra 1 maker with a new
seed) and with complex solutions (US Algebra 2 maker with a new seed), and solving quadratic inequalities with
factoring, sign tests and in context (own makers).
Wrong answers come from real mistakes: forgetting ±, choosing the inside instead of the outside, and keeping only one
interval.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a1_quadratic_formula_and_completing_the_square as qf
adopt(qf)
qf.R = random.Random(697100)
import gen_us_math_a2_complex_numbers as cx
adopt(cx)
cx.R = random.Random(697101)
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


from math import isqrt


def rad(n):
    """simplest radical form of √n: (outside, inside)"""
    o = 1
    for f in range(isqrt(n), 1, -1):
        if n % (f * f) == 0:
            o, n = f, n // (f * f)
            break
    return o, n


def lin_(h):
    return X if h == 0 else "%s %s %d" % (X, MINUS if h > 0 else "+", abs(h))


def one_sqrt(r):
    a = r.choice([1, 1, 2, 3, 4])
    h = r.randint(-6, 6)
    n = r.choice([4, 9, 16, 25, 36, 49, 2, 3, 5, 7, 8, 12, 18, 20, 27, 45, 50])
    k = r.choice([0, 0, 1, 2, 3, 5, -1, -2, -4])
    rhs = a * n + k
    q = "Solve %s(%s)<sup>2</sup> %s = %d." % ("" if a == 1 else str(a), lin_(h), (" %s %d" % ("+" if k > 0 else MINUS, abs(k))) if k else "", rhs)
    q = q.replace(")<sup>2</sup>  ", ")<sup>2</sup> ").replace("(<i>x</i>)<sup>2</sup>", "<i>x</i><sup>2</sup>")
    o, inn = rad(n)
    if inn == 1:
        lo, hi = h - o, h + o
        right = "<i>x</i> = %s or <i>x</i> = %s" % (sg(lo), sg(hi))
        w = ["<i>x</i> = %s" % sg(hi), "<i>x</i> = %s or <i>x</i> = %s" % (sg(-h - o), sg(-h + o)), "<i>x</i> = %s or <i>x</i> = %s" % (sg(h - n), sg(h + n))]
    else:
        rt = ("%d√%d" % (o, inn)) if o > 1 else "√%d" % inn
        right = "<i>x</i> = %s ± %s" % (sg(h), rt) if h else "<i>x</i> = ±%s" % rt
        w = [("<i>x</i> = %s ± %s" % (sg(-h), rt)) if h else "<i>x</i> = %s" % rt, ("<i>x</i> = %s ± %d" % (sg(h), n)) if h else "<i>x</i> = ±%d" % n, ("<i>x</i> = %s + %s" % (sg(h), rt)) if h else "<i>x</i> = ±√%d" % (2 * n)]
    return mcq(q, right, w, "Get the square alone: (%s)<sup>2</sup> = %d. Take the square root of both sides with ±: %s = ±√%d. <b>%s</b>." % (lin_(h), n, lin_(h), n, right))


def rel(sym):
    return {"lt": "&lt;", "le": "≤", "gt": "&gt;", "ge": "≥"}[sym]


def sol(p, q, sym):
    S = {"lt": "&lt;", "le": "≤", "gt": "&gt;", "ge": "≥"}
    if sym in ("lt", "le"):
        return "%s %s <i>x</i> %s %s" % (sg(p), S[sym], S[sym], sg(q))
    o = {"gt": "lt", "ge": "le"}[sym]
    return "<i>x</i> %s %s or <i>x</i> %s %s" % (S[o], sg(p), S[sym], sg(q))


FLIP = {"lt": "gt", "le": "ge", "gt": "lt", "ge": "le"}
STRICT = {"lt": "le", "le": "lt", "gt": "ge", "ge": "gt"}


def roots(r):
    p, q = sorted(r.sample(range(-8, 9), 2))
    return p, q


def one_ineq(r):
    p, q = roots(r)
    sym = r.choice(["lt", "le", "gt", "ge"])
    a = r.choice([1, 1, 1, 2])
    left = poly([a, -a * (p + q), a * p * q])
    right = sol(p, q, sym)
    w = [sol(p, q, FLIP[sym]), sol(p, q, STRICT[sym]), sol(-q, -p, sym)]
    return mcq("Solve %s %s 0." % (left, rel(sym)), right, w,
               "Factor: %s(<i>x</i> %s %d)(<i>x</i> %s %d). The zeros are %s and %s. The parabola opens up, so it is below 0 between the zeros and above 0 outside them. <b>%s</b>." % (
                   "" if a == 1 else str(a), MINUS if p > 0 else "+", abs(p), MINUS if q > 0 else "+", abs(q), sg(p), sg(q), right))


def one_ineq2(r):
    p, q = roots(r)
    sym = r.choice(["lt", "le", "gt", "ge"])
    k = r.randint(-9, 9)
    b, c = -(p + q), p * q
    if k == 0 or c - k == 0:
        raise AssertionError
    kind = r.choice(["move", "neg"])
    if kind == "move":
        left = "%s %s %s" % (poly([1, b, c - k]), rel(sym), sg(-k))
        e0 = "Move %s to the left: %s %s 0." % (sg(-k), poly([1, b, c]), rel(sym))
        s2 = sym
    else:
        left = "%s %s 0" % (poly([-1, -b, -c]), rel(sym))
        e0 = "Multiply by −1 and reverse the sign: %s %s 0." % (poly([1, b, c]), rel(FLIP[sym]))
        s2 = FLIP[sym]
    right = sol(p, q, s2)
    w = [sol(p, q, FLIP[s2]), sol(p, q, STRICT[s2]), sol(-q, -p, s2)]
    return mcq("Solve %s." % left, right, w, e0 + " The zeros are %s and %s. <b>%s</b>." % (sg(p), sg(q), right))


def one_ctx(r):
    t2 = r.choice([2, 3, 4, 5])
    t1 = r.choice([t for t in range(1, t2)])
    v = 16 * (t1 + t2)
    hh = 16 * t1 * t2
    s = r.choice([0, 0, 4, 6, 10])
    thing = r.choice(["ball", "rock", "toy rocket", "water balloon", "pumpkin"])
    if r.random() < 0.6:
        q = "A %s is launched upward. Its height is <i>h</i> = −16<i>t</i><sup>2</sup> + %d<i>t</i>%s feet after <i>t</i> seconds. When is it higher than %d feet?" % (thing, v, (" + %d" % s) if s else "", hh + s)
        right = "%d &lt; <i>t</i> &lt; %d" % (t1, t2)
        w = ["<i>t</i> &lt; %d or <i>t</i> &gt; %d" % (t1, t2), "0 &lt; <i>t</i> &lt; %d" % t2, "%d ≤ <i>t</i> ≤ %d" % (t1, t2 + 1)]
        e = "−16<i>t</i><sup>2</sup> + %d<i>t</i>%s &gt; %d gives <i>t</i><sup>2</sup> − %d<i>t</i> + %d &lt; 0, so (<i>t</i> − %d)(<i>t</i> − %d) &lt; 0." % (v, (" + %d" % s) if s else "", hh + s, t1 + t2, t1 * t2, t1, t2)
    else:
        p, q2 = r.choice([(10, 30), (5, 25), (20, 40), (10, 40), (15, 35), (5, 35), (20, 50)])
        m = r.choice([1, 2, 3, 4, 5])
        A = m
        B, C = m * (p + q2), m * p * q2
        q = "A company's profit is <i>P</i> = −%s<i>x</i><sup>2</sup> + %s<i>x</i> − %s dollars when it sells an item for <i>x</i> dollars. For which prices is the profit at least $0?" % (("" if A == 1 else str(A)), comma(B), comma(C))
        right = "%d ≤ <i>x</i> ≤ %d" % (p, q2)
        w = ["<i>x</i> ≤ %d or <i>x</i> ≥ %d" % (p, q2), "%d &lt; <i>x</i> &lt; %d" % (p, q2), "0 ≤ <i>x</i> ≤ %d" % q2]
        e = "Divide by −%d and reverse: <i>x</i><sup>2</sup> − %d<i>x</i> + %s ≤ 0, so (<i>x</i> − %d)(<i>x</i> − %d) ≤ 0." % (A, p + q2, comma(p * q2), p, q2)
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Solve by square roots", [("collect", uniq(one_sqrt), 20)]),
        ("The quadratic formula", [("collect", W(qf.one_radical), 10), ("collect", W(qf.one_rational), 10)]),
        ("Real and complex solutions", [("collect", W(cx.one_quad), 20)]),
        ("Solve quadratic inequalities", [("collect", uniq(one_ineq), 12), ("collect", uniq(one_ineq2), 8)]),
        ("Quadratic inequalities in context", [("collect", uniq(one_ctx), 20)]),
    ], 69710)
    finish(sets, R)
    body = lesson("<ul><li>Square roots: get the square alone, then take ± the square root.</li><li>Quadratic formula: <i>x</i> = <span class='fr'><span class='fn'>−<i>b</i> ± √(<i>b</i><sup>2</sup> − 4<i>ac</i>)</span><span class='fd'>2<i>a</i></span></span>. A negative discriminant gives two complex solutions.</li><li>Quadratic inequality: find the zeros, then test where the parabola is above or below 0.</li><li>For <i>x</i><sup>2</sup> + … &lt; 0 the answer is <b>between</b> the zeros; for &gt; 0 it is <b>outside</b> them.</li></ul>",
        [example("<i>x</i><sup>2</sup> − 2<i>x</i> − 8 &lt; 0", ["(<i>x</i> − 4)(<i>x</i> + 2) &lt; 0", "Zeros −2 and 4"], "−2 &lt; <i>x</i> &lt; 4"), example("(<i>x</i> − 3)<sup>2</sup> = 12", ["<i>x</i> − 3 = ±2√3"], "<i>x</i> = 3 ± 2√3")],
        [['Forgetting ±', '<i>x</i><sup>2</sup> = 9 gives 3 and −3.'], ['Inside instead of outside', '&gt; 0 means outside the zeros (for <i>a</i> &gt; 0).'], ['Not reversing the sign', 'Multiplying by a negative reverses the inequality.']])
    faq = [('What does TEKS 2A.4F ask?', 'Solve quadratic and square root equations.'), ('What does TEKS 2A.4H ask?', 'Solve quadratic inequalities.'), ('How can a graph help with a quadratic inequality?', 'The solutions are the x-values where the parabola is above (or below) the x-axis.'), ('When do you use ≤ instead of <?', 'When the zeros themselves are included.')]
    make('quadratic-equations-and-inequalities', 10, 'Quadratic and Square Root Functions, Equations, and Inequalities', '2A.4F, 2A.4H',
         '2A.4F solve quadratic and square root equations; 2A.4H solve quadratic inequalities',
         'Solving Quadratic Equations and Inequalities', 'Quadratic Equations and Inequalities',
         'Free Algebra II worksheets for Texas TEKS 2A.4F and 2A.4H: solve quadratic equations by square roots and the quadratic formula, complex solutions and quadratic inequalities. 100 questions with answers.',
         'For ax² + bx + c < 0 with a > 0, the answer is between the zeros.', 'Take ± when you take a square root.',
         body, faq, sets, seo_title='Algebra II Quadratic Equations and Inequalities Worksheets (TEKS 2A.4F, 2A.4H)')


if __name__ == "__main__":
    build()
