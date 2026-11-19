# -*- coding: utf-8 -*-
"""
Texas Precalculus: Sequences, Series and Sigma Notation (TEKS P.5A, P.5B, P.5C, P.5D, P.5E)
  python3 tools/gen_ustx_math_pc_sequences_series.py
Evaluating sums in sigma notation, arithmetic and geometric series, infinite geometric series (US Algebra 2 makers with
a new seed), and recursive formulas and writing series in sigma notation (own makers).
Wrong answers come from real mistakes: using n instead of n − 1 in the nth term, adding the ratio instead of
multiplying, and finding an infinite sum when |r| ≥ 1.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a2_sequences_and_series as ss
adopt(ss)
ss.R = random.Random(698250)
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


def seq(vs):
    return ", ".join(sg(v) for v in vs) + ", …"


def one_rec(r):
    kind = r.choice(["ar", "geo", "write_ar", "write_geo"])
    a1 = r.choice([n for n in range(-9, 13) if n])
    if kind in ("ar", "write_ar"):
        d = r.choice([n for n in range(-7, 8) if n])
        terms = [a1 + d * i for i in range(5)]
        if kind == "ar":
            q = "<i>a</i><sub>1</sub> = %s and <i>a</i><sub><i>n</i></sub> = <i>a</i><sub><i>n</i>−1</sub> %s %d. What is <i>a</i><sub>5</sub>?" % (sg(a1), "+" if d > 0 else MINUS, abs(d))
            right, w = sg(terms[4]), [sg(a1 + 5 * d), sg(terms[3]), sg(a1 * d ** 4) if abs(a1 * d ** 4) < 10 ** 5 else sg(terms[4] + d + 1)]
            e = "Add %s four times: %s." % (sg(d), ", ".join(sg(t) for t in terms))
        else:
            q = "Which recursive formula gives the sequence %s?" % seq(terms[:4])
            R = lambda op, v: "<i>a</i><sub>1</sub> = %s, <i>a</i><sub><i>n</i></sub> = <i>a</i><sub><i>n</i>−1</sub> %s" % (sg(a1), op % v)
            right = R("%s", ("+ %d" % d) if d > 0 else ("− %d" % -d))
            w = [R("%s", ("− %d" % d) if d > 0 else ("+ %d" % -d)), "<i>a</i><sub>1</sub> = %s, <i>a</i><sub><i>n</i></sub> = %s<i>a</i><sub><i>n</i>−1</sub>" % (sg(a1), sg(d)), "<i>a</i><sub>1</sub> = %s, <i>a</i><sub><i>n</i></sub> = <i>a</i><sub><i>n</i>−1</sub> %s" % (sg(d), ("+ %d" % a1) if a1 > 0 else ("− %d" % -a1))]
            e = "Each term is %s %d from the one before." % ("+" if d > 0 else "−", abs(d))
    else:
        rr = r.choice([2, 3, -2, -3, 4])
        a1 = r.choice([1, 2, 3, 4, 5, -2, -3])
        terms = [a1 * rr ** i for i in range(5)]
        if kind == "geo":
            q = "<i>a</i><sub>1</sub> = %s and <i>a</i><sub><i>n</i></sub> = %s · <i>a</i><sub><i>n</i>−1</sub>. What is <i>a</i><sub>5</sub>?" % (sg(a1), sg(rr))
            right, w = sg(terms[4]), [sg(a1 * rr ** 5), sg(terms[3]), sg(a1 + 4 * rr)]
            e = "Multiply by %s four times: %s." % (sg(rr), ", ".join(sg(t) for t in terms))
        else:
            q = "Which recursive formula gives the sequence %s?" % seq(terms[:4])
            right = "<i>a</i><sub>1</sub> = %s, <i>a</i><sub><i>n</i></sub> = %s · <i>a</i><sub><i>n</i>−1</sub>" % (sg(a1), sg(rr))
            dd = terms[1] - terms[0]
            w = ["<i>a</i><sub>1</sub> = %s, <i>a</i><sub><i>n</i></sub> = <i>a</i><sub><i>n</i>−1</sub> %s %d" % (sg(a1), "+" if dd > 0 else MINUS, abs(dd)), "<i>a</i><sub>1</sub> = %s, <i>a</i><sub><i>n</i></sub> = %s · <i>a</i><sub><i>n</i>−1</sub>" % (sg(rr), sg(a1)),
                 "<i>a</i><sub>1</sub> = %s, <i>a</i><sub><i>n</i></sub> = %s · <i>a</i><sub><i>n</i>−1</sub>" % (sg(a1), sg(-rr))]
            e = "Each term is %s times the one before." % sg(rr)
    w = [v for v in dict.fromkeys(w) if v != right]
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def sig(lo, hi, body):
    return "<span class='sig'>Σ<sub><i>k</i>=%d</sub><sup>%d</sup></span> %s" % (lo, hi, body)


def one_sigw(r):
    kind = r.choice(["ar", "ar", "geo"])
    n = r.randint(5, 12)
    if kind == "ar":
        d = r.choice([2, 3, 4, 5, -2, -3])
        a1 = r.randint(-5, 9)
        c = a1 - d
        terms = [a1 + d * i for i in range(n)]
        body = lambda dd, cc: "(%s)" % poly([dd, cc], "<i>k</i>")
        right = sig(1, n, body(d, c))
        w = [sig(1, n, body(d, a1)), sig(0, n, body(d, c)), sig(1, n, body(c, d)) if c else sig(1, n + 1, body(d, c))]
        e = "The <i>k</i>th term is %s + (<i>k</i> − 1)(%s) = %s, and there are %d terms." % (sg(a1), sg(d), poly([d, c], "<i>k</i>"), n)
    else:
        rr = r.choice([2, 3, 5])
        a1 = r.choice([1, 2, 3, 4])
        terms = [a1 * rr ** i for i in range(n)]
        bd = lambda co, ex: "%s(%d)<sup>%s</sup>" % ("" if co == 1 else str(co), rr, ex)
        right = sig(1, n, bd(a1, "<i>k</i>−1"))
        w = [sig(1, n, bd(a1, "<i>k</i>")), sig(1, n, bd(rr, "<i>k</i>−1")) if rr != a1 else sig(0, n, bd(a1, "<i>k</i>")), sig(1, n - 1, bd(a1, "<i>k</i>−1"))]
        e = "The <i>k</i>th term is %s · %d<sup><i>k</i>−1</sup>, for <i>k</i> = 1 to %d." % (sg(a1), rr, n)
    tt = lambda v: comma(v) if v >= 0 else "(%s)" % sg(v)
    shown = " + ".join(tt(t) for t in terms[:3]) + " + … + " + tt(terms[-1])
    w = [v for v in dict.fromkeys(w) if v != right]
    return mcq("Write the series %s in sigma notation." % shown, right, w, e + " <b>%s</b>." % right)


def nominus(it):
    return "+ −" not in it["q"] and "+ 0)" not in it["q"]


def build():
    sets, R = build_sets([
        ("Sigma notation", [("collect", W(ss.one_sig, nominus), 20)]),
        ("Arithmetic series", [("collect", W(ss.one_ar), 20)]),
        ("Geometric series", [("collect", W(ss.one_geo, nominus), 20)]),
        ("Infinite geometric series", [("collect", W(ss.one_inf, nominus), 20)]),
        ("Recursive formulas and writing series", [("collect", uniq(one_rec), 10), ("collect", uniq(one_sigw), 10)]),
    ], 69825)
    finish(sets, R)
    body = lesson("<ul><li>Arithmetic: add <i>d</i> each time; <i>a</i><sub><i>n</i></sub> = <i>a</i><sub>1</sub> + (<i>n</i> − 1)<i>d</i>; <i>S</i><sub><i>n</i></sub> = <span class='fr'><span class='fn'><i>n</i></span><span class='fd'>2</span></span>(<i>a</i><sub>1</sub> + <i>a</i><sub><i>n</i></sub>).</li><li>Geometric: multiply by <i>r</i>; <i>a</i><sub><i>n</i></sub> = <i>a</i><sub>1</sub><i>r</i><sup><i>n</i>−1</sup>; <i>S</i><sub><i>n</i></sub> = <i>a</i><sub>1</sub><span class='fr'><span class='fn'>1 − <i>r</i><sup><i>n</i></sup></span><span class='fd'>1 − <i>r</i></span></span>.</li><li>Infinite geometric series: if |<i>r</i>| &lt; 1, <i>S</i> = <span class='fr'><span class='fn'><i>a</i><sub>1</sub></span><span class='fd'>1 − <i>r</i></span></span>; otherwise there is no sum.</li><li>Recursive formula: give the first term and the rule from one term to the next.</li></ul>",
        [example("3 + 6 + 12 + … (8 terms)", ["<i>a</i><sub>1</sub> = 3, <i>r</i> = 2", "<i>S</i><sub>8</sub> = 3(1 − 256) ÷ (1 − 2)"], "765")],
        [['<i>n</i> instead of <i>n</i> − 1', '<i>a</i><sub><i>n</i></sub> = <i>a</i><sub>1</sub> + (<i>n</i> − 1)<i>d</i>.'], ['Adding the ratio', 'Geometric terms are multiplied by <i>r</i>.'], ['An infinite sum with |<i>r</i>| ≥ 1', 'No sum: the terms do not shrink.']])
    faq = [('What do TEKS P.5A and P.5D ask?', 'Evaluate finite sums and geometric series, when possible, written in sigma notation, and represent arithmetic series and geometric series using sigma notation.'), ('What does TEKS P.5B ask?', 'Represent arithmetic sequences and geometric sequences using recursive formulas.'), ('What do TEKS P.5C and P.5E ask?', 'Calculate the nth term and the nth partial sum of arithmetic and geometric series, and the sum of an infinite geometric series when it exists.'), ('What is the difference between a sequence and a series?', 'A sequence is a list; a series is the sum of its terms.')]
    make('sequences-series-and-sigma-notation', 25, 'Algebraic Reasoning', 'P.5A, P.5B, P.5C, P.5D, P.5E',
         'P.5A evaluate finite sums and geometric series, when possible, written in sigma notation; P.5B represent arithmetic sequences and geometric sequences using recursive formulas; P.5C calculate the nth term and the nth partial sum of an arithmetic series in mathematical and real-world problems; P.5D represent arithmetic series and geometric series using sigma notation; P.5E calculate the nth term of a geometric series, the nth partial sum of a geometric series, and sum of an infinite geometric series when it exists',
         'Sequences, Series and Sigma Notation', 'Sequences and Series',
         'Free Precalculus worksheets on sequences and series for Texas TEKS P.5A to P.5E: sigma notation, arithmetic and geometric series, infinite series and recursive formulas. 100 questions with answers.',
         'Arithmetic adds d; geometric multiplies by r.', 'Infinite geometric sum a₁ ÷ (1 − r) only when |r| < 1.',
         body, faq, sets, seo_title='Precalculus Sequences, Series and Sigma Notation Worksheets (TEKS P.5A–P.5E)')


if __name__ == "__main__":
    build()
