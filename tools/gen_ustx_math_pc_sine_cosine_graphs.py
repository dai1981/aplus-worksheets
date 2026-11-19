# -*- coding: utf-8 -*-
"""
Texas Precalculus: Graphs of Sine, Cosine and Tangent (TEKS P.2F, P.2G, P.2I)
  python3 tools/gen_ustx_math_pc_sine_cosine_graphs.py
Amplitude, period, midline, range, phase shift and matching graphs of sine and cosine (US Algebra 2 makers with a new
seed), and the period, asymptotes and zeros of tangent and key features of sine and cosine on [0, 2π] (own maker).
Wrong answers come from real mistakes: using b as the period, giving tangent a period of 2π, and putting the maximum of
sine at x = 0.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a2_graphs_of_sine_and_cosine as sc
adopt(sc)
sc.R = random.Random(698130)
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


def pin(n, d=1):
    f = Fr(n, d)
    if f == 0:
        return "0"
    s = MINUS if f < 0 else ""
    f = abs(f)
    top = "π" if f.numerator == 1 else "%dπ" % f.numerator
    return s + (top if f.denominator == 1 else "<span class='fr'><span class='fn'>%s</span><span class='fd'>%d</span></span>" % (top, f.denominator))


def one_tan(r):
    b = r.choice([1, 2, 3, 4, Fr(1, 2)])
    a = r.choice([1, 2, 3])
    bt = "" if b == 1 else ft(b)
    f = "<i>y</i> = %stan %s<i>x</i>" % ("" if a == 1 else str(a) + " ", bt)
    kind = r.choice(["period", "asym", "zero"])
    if kind == "period":
        right = pin(Fr(1) / b)
        w = [pin(Fr(2) / b), pin(b), pin(Fr(1, 2) / b)]
        q, e = "What is the period of %s?" % f, "Tangent repeats every π, so the period is π ÷ %s." % ft(b)
    elif kind == "asym":
        right = "<i>x</i> = %s" % pin(Fr(1, 2) / b)
        w = ["<i>x</i> = %s" % pin(Fr(1) / b), "<i>x</i> = 0", "<i>x</i> = %s" % pin(Fr(1, 4) / b)]
        q, e = "Which line is a vertical asymptote of %s?" % f, "tan θ is undefined at θ = π/2, so %s<i>x</i> = π/2 gives <i>x</i> = %s." % (bt, pin(Fr(1, 2) / b))
    else:
        right = "<i>x</i> = %s" % pin(Fr(1) / b)
        w = ["<i>x</i> = %s" % pin(Fr(1, 2) / b), "<i>x</i> = %s" % pin(Fr(1, 4) / b), "<i>x</i> = %s" % pin(Fr(3, 2) / b)]
        q, e = "Which is a zero of %s (other than <i>x</i> = 0)?" % f, "tan θ = 0 at θ = π, so %s<i>x</i> = π gives <i>x</i> = %s." % (bt, pin(Fr(1) / b))
    if right in w:
        raise AssertionError
    return mcq(q, right, w, e + " <b>%s</b>." % right)


FEAT = [("sin", "max", "<i>x</i> = <span class='fr'><span class='fn'>π</span><span class='fd'>2</span></span>"), ("sin", "min", "<i>x</i> = <span class='fr'><span class='fn'>3π</span><span class='fd'>2</span></span>"),
        ("cos", "max", "<i>x</i> = 0 and <i>x</i> = 2π"), ("cos", "min", "<i>x</i> = π"), ("sin", "zero", "<i>x</i> = 0, π and 2π"),
        ("cos", "zero", "<i>x</i> = <span class='fr'><span class='fn'>π</span><span class='fd'>2</span></span> and <i>x</i> = <span class='fr'><span class='fn'>3π</span><span class='fd'>2</span></span>")]
FW = {"max": "maximum", "min": "minimum", "zero": "zeros"}


def one_feat(r):
    fn, kind, right = r.choice(FEAT)
    a = r.choice([1, 2, 3, 4, 5])
    neg = r.random() < 0.4
    if neg:
        kind2 = {"max": "min", "min": "max", "zero": "zero"}[kind]
    else:
        kind2 = kind
    f = "<i>y</i> = %s%s%s <i>x</i>" % (MINUS if neg else "", "" if a == 1 else str(a) + " ", fn)
    q = "On 0 ≤ <i>x</i> ≤ 2π, where %s the %s of %s?" % ("are" if kind2 == "zero" else "is", FW[kind2], f)
    w = [v for (g, k, v) in FEAT if v != right][:]
    r.shuffle(w)
    e = "%s %s has its %s at %s%s." % (fn, "<i>x</i>", FW[kind], right, (" — the minus sign swaps maximum and minimum" if neg and kind != "zero" else ""))
    return mcq(q, right, w[:4], e + " <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Amplitude and period", [("collect", W(sc.one_ap), 20)]),
        ("Midline and range", [("collect", W(sc.one_mid), 20)]),
        ("Phase shift", [("collect", W(sc.one_shift), 20)]),
        ("Match the graph", [("collect", W(sc.one_graph), 20)]),
        ("Tangent and key points", [("collect", uniq(one_tan), 10), ("collect", uniq(one_feat), 10)]),
    ], 69813)
    finish(sets, R)
    body = lesson('<ul><li><i>y</i> = <i>a</i> sin(<i>b</i>(<i>x</i> − <i>c</i>)) + <i>d</i>: amplitude |<i>a</i>|, period 2π ÷ |<i>b</i>|, phase shift <i>c</i>, midline <i>y</i> = <i>d</i>.</li><li>The range is <i>d</i> − |<i>a</i>| ≤ <i>y</i> ≤ <i>d</i> + |<i>a</i>|.</li><li>sin <i>x</i> starts at 0 and rises; cos <i>x</i> starts at its maximum.</li><li><i>y</i> = tan <i>bx</i> has period π ÷ |<i>b</i>| and vertical asymptotes where cos <i>bx</i> = 0.</li></ul>',
        [example("<i>y</i> = 3 sin(2<i>x</i>) − 1", ["Amplitude 3", "Period 2π ÷ 2 = π", "Midline <i>y</i> = −1"], "Range −4 ≤ <i>y</i> ≤ 2")],
        [['Using <i>b</i> as the period', 'Period = 2π ÷ <i>b</i>.'], ['A tangent period of 2π', 'Tangent repeats every π.'], ['Maximum of sine at 0', 'sin is 0 at <i>x</i> = 0; cos is at its maximum.']])
    faq = [('What does TEKS P.2G ask?', 'Graph functions, including sine and cosine, and their transformations, including af(x), f(x) + d, f(x − c), f(bx).'), ('What does TEKS P.2I ask?', 'Determine and analyze key features of functions, including trigonometric functions, such as domain, range, symmetry, relative maximum, relative minimum, zeros, asymptotes, and intervals of increase and decrease.'), ('Is sine odd or even?', 'Sine is odd; cosine is even.'), ('Does tangent have an amplitude?', 'No. Its range is all real numbers.')]
    make('graphs-of-trigonometric-functions', 13, 'Functions', 'P.2F, P.2G, P.2I',
         'P.2F graph exponential, logarithmic, rational, polynomial, power, trigonometric, inverse trigonometric, and piecewise defined functions, including step functions; P.2G graph functions, including exponential, logarithmic, sine, cosine, rational, polynomial, and power functions and their transformations, including af(x), f(x) + d, f(x − c), f(bx) for specific values of a, b, c, and d, in mathematical and real-world problems; P.2I determine and analyze the key features of exponential, logarithmic, rational, polynomial, power, trigonometric, inverse trigonometric, and piecewise defined functions, including step functions such as domain, range, symmetry, relative maximum, relative minimum, zeros, asymptotes, and intervals over which the function is increasing or decreasing',
         'Graphs of Sine, Cosine and Tangent', 'Trigonometric Graphs',
         'Free Precalculus worksheets on trigonometric graphs for Texas TEKS P.2F, P.2G and P.2I: amplitude, period, midline, phase shift, tangent asymptotes and key points. 100 questions with answers.',
         'Period of a sin bx: 2π ÷ |b|.', 'Tangent has period π.',
         body, faq, sets, seo_title='Precalculus Graphs of Trigonometric Functions Worksheets (TEKS P.2F, P.2G, P.2I)')


if __name__ == "__main__":
    build()
