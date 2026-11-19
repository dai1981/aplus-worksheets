# -*- coding: utf-8 -*-
"""
Texas Algebra II: Domain and Range: Interval, Inequality and Set Notation (TEKS 2A.7I)
  python3 tools/gen_ustx_math_a2_domain_range_notation.py
Writing domain and range in interval notation, inequalities and set notation, domains of rational, square root and
log functions, ranges of transformed functions (own makers), plus reading domain and range from graphs (US Algebra 1
maker with a new seed).
Wrong answers come from real mistakes: a bracket for an open end, a bracket next to ∞, and forgetting the union for x ≠ a.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a1_domain_and_range as dr
adopt(dr)
dr.R = random.Random(697030)
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


INF = "∞"


def iv(lo, hi, lc, hc):
    """interval text; lo/hi None means infinite"""
    a = (MINUS + INF) if lo is None else sg(lo)
    b = INF if hi is None else sg(hi)
    return "%s%s, %s%s" % ("[" if lc and lo is not None else "(", a, b, "]" if hc and hi is not None else ")")


def setn(cond):
    return "{<i>x</i> | %s}" % cond


def ineq(lo, hi, lc, hc):
    if lo is None and hi is None:
        return "all real numbers"
    if lo is None:
        return "<i>x</i> %s %s" % ("≤" if hc else "&lt;", sg(hi))
    if hi is None:
        return "<i>x</i> %s %s" % ("≥" if lc else "&gt;", sg(lo))
    return "%s %s <i>x</i> %s %s" % (sg(lo), "≤" if lc else "&lt;", "≤" if hc else "&lt;", sg(hi))


def rand_iv(r):
    t = r.choice(["lo", "hi", "both", "both"])
    a = r.randint(-9, 6)
    b = r.randint(a + 1, a + 10)
    lc, hc = r.random() < 0.5, r.random() < 0.5
    if t == "lo":
        return a, None, lc, False
    if t == "hi":
        return None, b, False, hc
    return a, b, lc, hc


def one_three(r):
    lo, hi, lc, hc = rand_iv(r)
    forms = {"in interval notation": iv(lo, hi, lc, hc), "as an inequality": ineq(lo, hi, lc, hc), "in set notation": setn(ineq(lo, hi, lc, hc))}
    def wrongs(form):
        alt = [(lo, hi, not lc, hc), (lo, hi, lc, not hc), (lo, hi, not lc, not hc)]
        if lo is None:
            alt = [(None, hi, False, not hc), (hi, None, hc, False), (hi, None, not hc, False)]
        if hi is None:
            alt = [(lo, None, not lc, False), (None, lo, False, lc), (None, lo, False, not lc)]
        out = []
        for a in alt:
            if form == "in interval notation":
                out.append(iv(*a))
            elif form == "as an inequality":
                out.append(ineq(*a))
            else:
                out.append(setn(ineq(*a)))
        if form == "in interval notation" and (lo is None or hi is None):
            out.append(iv(lo, hi, lc, hc).replace("(" + MINUS + INF, "[" + MINUS + INF).replace(INF + ")", INF + "]"))
        return out
    src, dst = r.sample(list(forms), 2)
    q = "The domain of a function is %s. Write it %s." % (forms[src], dst)
    right = forms[dst]
    e = "( or ) means the end is not included (&lt; or &gt;); [ or ] means it is included (≤ or ≥). ∞ always gets a parenthesis. <b>%s</b>." % right
    return mcq(q, right, wrongs(dst), e)


def one_not(r):
    a = r.randint(-8, 8)
    kind = r.choice(["ne", "ne2", "all"])
    if kind == "ne":
        right = "(%s, %s) ∪ (%s, %s)" % (MINUS + INF, sg(a), sg(a), INF)
        w = ["(%s, %s)" % (MINUS + INF, INF), "(%s, %s] ∪ [%s, %s)" % (MINUS + INF, sg(a), sg(a), INF), "(%s, %s)" % (sg(a), INF)]
        q = "Write %s in interval notation." % setn("<i>x</i> ≠ %s" % sg(a))
        e = "Every number except %s: all numbers to the left of %s, together (∪) with all numbers to the right." % (sg(a), sg(a))
    elif kind == "ne2":
        b = r.randint(a + 1, a + 9)
        right = "(%s, %s) ∪ (%s, %s) ∪ (%s, %s)" % (MINUS + INF, sg(a), sg(a), sg(b), sg(b), INF)
        w = ["(%s, %s) ∪ (%s, %s)" % (MINUS + INF, sg(a), sg(b), INF), "(%s, %s)" % (sg(a), sg(b)), "[%s, %s]" % (sg(a), sg(b))]
        q = "Write %s in interval notation." % setn("<i>x</i> ≠ %s, <i>x</i> ≠ %s" % (sg(a), sg(b)))
        e = "Two numbers are left out, so the number line breaks into three pieces."
    else:
        b = r.randint(a + 1, a + 9)
        right = setn("<i>x</i> ≤ %s or <i>x</i> ≥ %s" % (sg(a), sg(b)))
        w = [setn("%s ≤ <i>x</i> ≤ %s" % (sg(a), sg(b))), setn("<i>x</i> &lt; %s or <i>x</i> &gt; %s" % (sg(a), sg(b))), setn("<i>x</i> ≥ %s or <i>x</i> ≤ %s" % (sg(a), sg(b)))]
        q = "Write (%s, %s] ∪ [%s, %s) in set notation." % (MINUS + INF, sg(a), sg(b), INF)
        e = "The two pieces are joined by the word <b>or</b>; the brackets mean %s and %s are included." % (sg(a), sg(b))
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def lin_(v):
    return X if v == 0 else "%s %s %d" % (X, MINUS if v > 0 else "+", abs(v))


def one_dom(r):
    a = r.choice([n for n in range(-9, 10) if n])
    kind = r.choice(["rat", "rat2", "root", "root2", "log", "poly"])
    if kind == "rat":
        f = fx("<span class='fr'><span class='fn'>%d</span><span class='fd'>%s</span></span>" % (r.randint(1, 9), lin_(a)))
        right = "(%s, %s) ∪ (%s, %s)" % (MINUS + INF, sg(a), sg(a), INF)
        w = ["(%s, %s) ∪ (%s, %s)" % (MINUS + INF, sg(-a), sg(-a), INF), "(%s, %s)" % (sg(a), INF), "(%s, %s)" % (MINUS + INF, INF)]
        e = "The denominator %s is 0 when <i>x</i> = %s, so leave out %s." % (lin_(a), sg(a), sg(a))
    elif kind == "rat2":
        b = r.choice([n for n in range(-9, 10) if n and n > a])
        f = fx("<span class='fr'><span class='fn'><i>x</i></span><span class='fd'>(%s)(%s)</span></span>" % (lin_(a), lin_(b)))
        right = "(%s, %s) ∪ (%s, %s) ∪ (%s, %s)" % (MINUS + INF, sg(a), sg(a), sg(b), sg(b), INF)
        w = ["(%s, %s) ∪ (%s, %s) ∪ (%s, %s)" % (MINUS + INF, sg(-b), sg(-b), sg(-a), sg(-a), INF), "(%s, %s)" % (sg(a), sg(b)), "(%s, %s) ∪ (%s, %s)" % (MINUS + INF, sg(a), sg(b), INF)]
        e = "The denominator is 0 at <i>x</i> = %s and <i>x</i> = %s; leave out both." % (sg(a), sg(b))
    elif kind == "root":
        f = fx("√(%s)" % lin_(a))
        right = "[%s, %s)" % (sg(a), INF)
        w = ["(%s, %s)" % (sg(a), INF), "[%s, %s)" % (sg(-a), INF), "(%s, %s]" % (MINUS + INF, sg(a))]
        e = "%s ≥ 0 gives <i>x</i> ≥ %s; the end is included." % (lin_(a), sg(a))
    elif kind == "root2":
        f = fx("√(%s %s <i>x</i>)" % (sg(a), MINUS))
        right = "(%s, %s]" % (MINUS + INF, sg(a))
        w = ["[%s, %s)" % (sg(a), INF), "(%s, %s)" % (MINUS + INF, sg(a)), "(%s, %s]" % (MINUS + INF, sg(-a))]
        e = "%s − <i>x</i> ≥ 0 gives <i>x</i> ≤ %s." % (sg(a), sg(a))
    elif kind == "log":
        f = fx("log(%s)" % lin_(a))
        right = "(%s, %s)" % (sg(a), INF)
        w = ["[%s, %s)" % (sg(a), INF), "(%s, %s)" % (sg(-a), INF), "(%s, %s)" % (MINUS + INF, INF)]
        e = "A logarithm needs a positive input: %s &gt; 0, so <i>x</i> &gt; %s (not ≥)." % (lin_(a), sg(a))
    else:
        f = fx("%s<sup>3</sup> %s %d<i>x</i>" % (X, MINUS, abs(a)))
        right = "(%s, %s)" % (MINUS + INF, INF)
        w = ["[0, %s)" % INF, "(%s, %s) ∪ (%s, %s)" % (MINUS + INF, sg(abs(a)), sg(abs(a)), INF), "(0, %s)" % INF]
        e = "A polynomial accepts every real number."
    return mcq("What is the domain of %s in interval notation?" % f, right, w, e + " <b>%s</b>." % right)


def one_rng(r):
    h, k = r.choice([n for n in range(-7, 8) if n]), r.choice([n for n in range(-9, 10) if n])
    a = r.choice([1, 2, 3, -1, -2, -3])
    kind = r.choice(["sq", "abs", "root", "exp", "rec"])
    lin = "(%s)" % lin_(h)
    co = "" if a == 1 else (MINUS if a == -1 else sg(a))
    tail = " %s %d" % ("+" if k > 0 else MINUS, abs(k))
    up = a > 0
    if kind == "sq":
        f = fx(co + lin + "<sup>2</sup>" + tail)
        right = "[%s, %s)" % (sg(k), INF) if up else "(%s, %s]" % (MINUS + INF, sg(k))
        w = ["(%s, %s]" % (MINUS + INF, sg(k)) if up else "[%s, %s)" % (sg(k), INF), "[%s, %s)" % (sg(h), INF), "(%s, %s)" % (MINUS + INF, INF)]
        e = "The vertex is (%s, %s) and the parabola opens %s." % (sg(h), sg(k), "up" if up else "down")
    elif kind == "abs":
        f = fx(co + "|%s|" % lin_(h) + tail)
        right = setn("<i>y</i> ≥ %s" % sg(k)).replace("<i>x</i> |", "<i>y</i> |") if up else setn("<i>y</i> ≤ %s" % sg(k)).replace("<i>x</i> |", "<i>y</i> |")
        w = [setn("<i>y</i> ≤ %s" % sg(k)).replace("<i>x</i> |", "<i>y</i> |") if up else setn("<i>y</i> ≥ %s" % sg(k)).replace("<i>x</i> |", "<i>y</i> |"),
             setn("<i>y</i> ≥ %s" % sg(h)).replace("<i>x</i> |", "<i>y</i> |"), setn("<i>y</i> &gt; %s" % sg(k)).replace("<i>x</i> |", "<i>y</i> |")]
        e = "The vertex is (%s, %s) and the V opens %s; the vertex is included." % (sg(h), sg(k), "up" if up else "down")
    elif kind == "root":
        a = abs(a)
        co = "" if a == 1 else sg(a)
        f = fx(co + "√(%s)" % lin_(h) + tail)
        right = "[%s, %s)" % (sg(k), INF)
        w = ["[%s, %s)" % (sg(h), INF), "(%s, %s)" % (sg(k), INF), "(%s, %s]" % (MINUS + INF, sg(k))]
        e = "√ is never negative, so the smallest output is %s (at <i>x</i> = %s)." % (sg(k), sg(h))
    elif kind == "exp":
        b = r.choice([2, 3, 5, 10])
        f = fx(co + ("·" if abs(a) > 1 else "") + "%d<sup>%s</sup>" % (b, X) + tail)
        f = f.replace(sg(a) + "·", sg(a) + "·")
        right = "(%s, %s)" % (sg(k), INF) if up else "(%s, %s)" % (MINUS + INF, sg(k))
        w = ["(%s, %s)" % (MINUS + INF, sg(k)) if up else "(%s, %s)" % (sg(k), INF), "[%s, %s)" % (sg(k), INF) if up else "(%s, %s]" % (MINUS + INF, sg(k)), "(0, %s)" % INF]
        e = "The horizontal asymptote is <i>y</i> = %s and the graph is %s it, never on it." % (sg(k), "above" if up else "below")
    else:
        f = fx(("" if a > 0 else MINUS) + "<span class='fr'><span class='fn'>%d</span><span class='fd'>%s</span></span>" % (abs(a), lin_(h)) + tail)
        right = "(%s, %s) ∪ (%s, %s)" % (MINUS + INF, sg(k), sg(k), INF)
        w = ["(%s, %s) ∪ (%s, %s)" % (MINUS + INF, sg(h), sg(h), INF), "(%s, %s)" % (sg(k), INF), "(%s, %s)" % (MINUS + INF, INF)]
        e = "The horizontal asymptote is <i>y</i> = %s: every output except %s." % (sg(k), sg(k))
    return mcq("What is the range of %s?" % f, right, w, e + " <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Interval, inequality and set notation", [("collect", uniq(one_three), 20)]),
        ("Unions and values left out", [("collect", uniq(one_not), 20)]),
        ("Domains of rational, square root and log functions", [("collect", uniq(one_dom), 20)]),
        ("Ranges of transformed functions", [("collect", uniq(one_rng), 20)]),
        ("Domain and range from a graph", [("collect", W(dr.one_graph), 20)]),
    ], 69703)
    finish(sets, R)
    body = lesson('<ul><li>Three ways to write the same set: inequality <i>x</i> ≥ 2, interval [2, ∞), set notation {<i>x</i> | <i>x</i> ≥ 2}.</li><li>( ) means the end is not included; [ ] means it is included. ∞ and −∞ always get ( ).</li><li>Use ∪ (union) to join pieces: <i>x</i> ≠ 3 is (−∞, 3) ∪ (3, ∞).</li><li>Domain: a denominator cannot be 0, a square root needs ≥ 0, a log needs &gt; 0.</li></ul>',
        [example("Domain of <i>f</i>(<i>x</i>) = <span class='fr'><span class='fn'>5</span><span class='fd'><i>x</i> − 4</span></span>", ["<i>x</i> − 4 ≠ 0, so <i>x</i> ≠ 4"], "(−∞, 4) ∪ (4, ∞)"), example("Range of <i>f</i>(<i>x</i>) = 2<sup><i>x</i></sup> − 3", ["The asymptote is <i>y</i> = −3", "The graph is above it"], "(−3, ∞)")],
        [['A bracket for &lt; or &gt;', '<i>x</i> &gt; 2 is (2, ∞), not [2, ∞).'], ['A bracket next to ∞', 'Always write ∞).'], ['Writing (−∞, ∞) for <i>x</i> ≠ 3', 'Leave out 3: (−∞, 3) ∪ (3, ∞).']])
    faq = [('What does TEKS 2A.7I ask?', 'Write the domain and range of a function in interval notation, inequalities, and set notation.'), ('What does ∪ mean?', 'Union: all numbers in either piece.'), ('How do you read {x | x > 2}?', 'The set of all x such that x is greater than 2.'), ('Why does ∞ get a parenthesis?', 'Infinity is not a number you can reach, so it is never included.')]
    make('domain-and-range-notation', 3, 'Number and Algebraic Methods', '2A.7I',
         '2A.7I write the domain and range of a function in interval notation, inequalities, and set notation',
         'Domain and Range: Interval, Inequality and Set Notation', 'Domain and Range Notation',
         'Free Algebra II worksheets for Texas TEKS 2A.7I: domain and range in interval notation, inequalities and set notation, domains of rational, square root and log functions. 100 questions with answers.',
         '( ) not included, [ ] included, ∞ always gets ( ).', 'x ≠ 3 is (−∞, 3) ∪ (3, ∞).',
         body, faq, sets, seo_title='Algebra II Domain and Range Notation Worksheets (TEKS 2A.7I)')


if __name__ == "__main__":
    build()
