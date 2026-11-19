# -*- coding: utf-8 -*-
"""
Texas Precalculus: Sinusoidal Models (TEKS P.2O)
  python3 tools/gen_ustx_math_pc_sinusoidal_models.py
Amplitude, midline and period from real situations, Ferris wheel heights (US Algebra 2 and Precalculus makers with a
new seed), and writing a sinusoidal model from maximum, minimum and period, evaluating a model and finding when it
reaches its maximum (own makers).
Wrong answers come from real mistakes: using the full height as the amplitude, using the period as b, and forgetting the
midline.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a2_graphs_of_sine_and_cosine as sc
adopt(sc)
sc.R = random.Random(698140)
import gen_us_math_pc_six_trigonometric_functions as six
adopt(six)
six.R = random.Random(698141)
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


import math


def bpi(P):
    f = Fr(2, P)
    top = "π" if f.numerator == 1 else "%dπ" % f.numerator
    return top if f.denominator == 1 else "<span class='fr'><span class='fn'>%s</span><span class='fd'>%d</span></span>" % (top, f.denominator)


CTX = [("The water depth at a pier", "feet", "hours", [12, 12.4, 24]), ("The temperature in a desert town over one day", "°F", "hours", [24]),
       ("The height of a seat on a Ferris wheel", "feet", "minutes", [2, 4, 6, 8, 10]), ("The height of a point on a turning paddle wheel", "feet", "seconds", [4, 6, 8, 10, 12]),
       ("The number of daylight hours in a city", "hours", "months", [12])]


def one_write(r):
    t, u, tu, ps = r.choice(CTX)
    P = r.choice([p for p in ps if p == int(p)])
    lo = r.choice([2, 4, 5, 6, 8, 10, 40, 50, 60]) if u != "hours" else r.choice([9, 10])
    amp = r.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20]) if u != "hours" else r.choice([2, 3])
    if u == "°F":
        lo = r.choice([55, 60, 65, 70])
        amp = r.choice([10, 12, 15, 20])
    hi = lo + 2 * amp
    mid = lo + amp
    q = "%s goes between a minimum of %d %s and a maximum of %d %s, and repeats every %d %s. It is at its maximum at <i>t</i> = 0. Which model fits?" % (t, lo, u, hi, u, P, tu)
    B = bpi(P)
    right = "<i>y</i> = %d cos(%s<i>t</i>) + %d" % (amp, B, mid)
    w = ["<i>y</i> = %d cos(%s<i>t</i>) + %d" % (2 * amp, B, lo), "<i>y</i> = %d cos(%d<i>t</i>) + %d" % (amp, P, mid), "<i>y</i> = %d sin(%s<i>t</i>) + %d" % (amp, B, mid)]
    return mcq(q, right, w, "Amplitude = (%d − %d) ÷ 2 = %d. Midline = (%d + %d) ÷ 2 = %d. <i>b</i> = 2π ÷ %d = %s. Starting at a maximum means cosine. <b>%s</b>." % (hi, lo, amp, hi, lo, mid, P, B, right))


def one_eval(r):
    A = r.choice([2, 3, 4, 5, 6, 10, 20])
    D = r.choice([10, 12, 15, 20, 30, 40, 50])
    P = r.choice([4, 6, 8, 12, 24])
    t = r.randint(1, P - 1)
    ang = Fr(2 * t, P)
    vals = {Fr(0): 1, Fr(1, 6): math.sqrt(3) / 2, Fr(1, 4): math.sqrt(2) / 2, Fr(1, 3): 0.5, Fr(1, 2): 0, Fr(2, 3): -0.5, Fr(3, 4): -math.sqrt(2) / 2, Fr(5, 6): -math.sqrt(3) / 2, Fr(1): -1,
            Fr(7, 6): -math.sqrt(3) / 2, Fr(5, 4): -math.sqrt(2) / 2, Fr(4, 3): -0.5, Fr(3, 2): 0, Fr(5, 3): 0.5, Fr(7, 4): math.sqrt(2) / 2, Fr(11, 6): math.sqrt(3) / 2}
    if ang not in vals or abs(vals[ang]) not in (0, 0.5, 1):
        raise AssertionError
    c = vals[ang]
    y = D + A * c
    B = bpi(P)
    q = "A model is <i>h</i>(<i>t</i>) = %d cos(%s<i>t</i>) + %d. Find <i>h</i>(%d)." % (A, B, D, t)
    G = lambda v: ("%g" % v).replace("-", MINUS)
    right = G(y)
    w = [G(D + A), G(D - A * c) if D - A * c != y else G(D - A), G(A * c), G(D)]
    w = [v for v in dict.fromkeys(w) if v != right]
    return mcq(q, right, w, "The angle is %s × %d = %sπ, and its cosine is %s. %d(%s) + %d = <b>%s</b>." % (B, t, ft(ang) if ang != 1 else "", G(c), A, G(c), D, right))


def one_when(r):
    P = r.choice([4, 6, 8, 10, 12, 24])
    c = r.choice([k for k in range(1, P)])
    A, D = r.choice([3, 5, 8, 10]), r.choice([20, 30, 50])
    B = bpi(P)
    kind = r.choice(["max", "min"])
    q = "<i>h</i>(<i>t</i>) = %d cos(%s(<i>t</i> − %d)) + %d. At what time <i>t</i> in 0 ≤ <i>t</i> &lt; %d is <i>h</i> at its %s?" % (A, B, c, D, P, "maximum" if kind == "max" else "minimum")
    tt = c if kind == "max" else (c + Fr(P, 2)) % P
    right = "<i>t</i> = %s" % ft(tt)
    alt = [(c + Fr(P, 2)) % P if kind == "max" else c, (c + Fr(P, 4)) % P, (-c) % P]
    w = ["<i>t</i> = %s" % ft(v) for v in alt]
    w = [v for v in dict.fromkeys(w) if v != right]
    if len(w) < 3:
        w.append("<i>t</i> = %s" % ft((tt + 1) % P))
    e = "Cosine is at its maximum when the inside is 0, at <i>t</i> = %d%s." % (c, ", and at its minimum half a period (%s) later" % ft(Fr(P, 2)) if kind == "min" else "")
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Amplitude, midline and period from a situation", [("collect", W(sc.one_model), 20)]),
        ("Write a sinusoidal model", [("collect", uniq(one_write), 20)]),
        ("Evaluate a model", [("collect", uniq(one_eval), 20)]),
        ("When is it at its maximum or minimum?", [("collect", uniq(one_when), 20)]),
        ("Ferris wheels and circular motion", [("collect", W(six.one_word), 20)]),
    ], 69814)
    finish(sets, R)
    body = lesson('<ul><li>A <b>sinusoidal model</b> is <i>y</i> = <i>A</i> sin(<i>B</i>(<i>t</i> − <i>C</i>)) + <i>D</i> or the same with cos.</li><li>Amplitude <i>A</i> = (max − min) ÷ 2. Midline <i>D</i> = (max + min) ÷ 2.</li><li><i>B</i> = 2π ÷ period.</li><li>Start at a maximum: use cos. Start on the midline going up: use sin.</li></ul>',
        [example("Tide: low 4 ft, high 16 ft, period 12 hours, high at <i>t</i> = 0", ["<i>A</i> = 6, <i>D</i> = 10", "<i>B</i> = 2π ÷ 12 = π/6"], "<i>y</i> = 6 cos(<span class='fr'><span class='fn'>π</span><span class='fd'>6</span></span><i>t</i>) + 10")],
        [['The full height as the amplitude', 'Amplitude is half of max − min.'], ['The period as <i>B</i>', '<i>B</i> = 2π ÷ period.'], ['Forgetting the midline', 'Add <i>D</i>.']])
    faq = [('What does TEKS P.2O ask?', 'Develop and use a sinusoidal function that models a situation in mathematical and real-world problems.'), ('Can I use sine instead of cosine?', 'Yes, with a phase shift of a quarter period.'), ('What real things are sinusoidal?', 'Tides, daylight hours, temperatures over a day, and Ferris wheels.'), ('Why use radians in the model?', 'The period formula 2π ÷ B uses radians.')]
    make('sinusoidal-models', 14, 'Functions', 'P.2O',
         'P.2O develop and use a sinusoidal function that models a situation in mathematical and real-world problems',
         'Sinusoidal Models', 'Sinusoidal Models',
         'Free Precalculus worksheets on sinusoidal models for Texas TEKS P.2O: amplitude, midline and period from situations, writing and evaluating models, tides and Ferris wheels. 100 questions with answers.',
         'Amplitude = (max − min) ÷ 2; midline = (max + min) ÷ 2.', 'B = 2π ÷ period.',
         body, faq, sets, seo_title='Precalculus Sinusoidal Models Worksheets (TEKS P.2O)')


if __name__ == "__main__":
    build()
