# -*- coding: utf-8 -*-
"""
Texas Precalculus: Modeling with Exponential, Logarithmic, Rational and Power Functions (TEKS P.2N)
  python3 tools/gen_ustx_math_pc_function_models.py
Half-life and compound growth, continuous growth, logarithmic scales (pH, decibels, earthquakes), rational models
(average cost and mixtures) and power models (own makers).
Wrong answers come from real mistakes: dividing by the half-life instead of using it as an exponent, reading a
log scale as linear, and squaring when a model uses a cube.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)

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


def num(v, d=1):
    s = ("%." + str(d) + "f") % v
    i, _, f_ = s.partition(".")
    return comma(int(i)) + ("." + f_ if f_ and d else "")


def one_half(r):
    A = r.choice([80, 100, 120, 200, 400, 500, 640])
    h = r.choice([3, 5, 6, 8, 10, 12, 30])
    n = r.choice([2, 3, 4, 5])
    t = h * n
    thing = r.choice(["a medicine in the body", "a radioactive sample", "a chemical in a pond", "caffeine in the blood"])
    unit_ = "hours" if "medicine" in thing or "caffeine" in thing else r.choice(["days", "years"])
    if (A * 100) % (2 ** n):
        raise AssertionError
    val = A / 2 ** n
    q = "The half-life of %s is %d %s. There are %d mg now. How much is left after %d %s?" % (thing, h, unit_, A, t, unit_)
    right = "%s mg" % num(val, 2).rstrip("0").rstrip(".")
    w = ["%s mg" % num(A / (2 * n), 2).rstrip("0").rstrip("."), "%s mg" % num(A - A / 2 * n, 2).rstrip("0").rstrip(".") if A - A / 2 * n > 0 else "%s mg" % num(A / 2 ** (n - 1), 2).rstrip("0").rstrip("."), "%s mg" % num(A / 2 ** (n + 1), 2).rstrip("0").rstrip(".")]
    return mcq(q, right, w, "<i>A</i> = %d(<span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>)<sup><i>t</i>/%d</sup>; %d ÷ %d = %d half-lives, so %d ÷ 2<sup>%d</sup> = <b>%s</b>." % (A, h, t, h, n, A, n, right))


def one_cont(r):
    kind = r.choice(["amt", "double"])
    P = r.choice([1000, 2000, 2500, 5000, 8000, 10000])
    rate = r.choice([2, 3, 4, 5, 6, 7, 8])
    if kind == "amt":
        t = r.choice([5, 8, 10, 12, 15, 20])
        v = P * math.exp(rate / 100 * t)
        q = "$%s is invested at %d%% interest compounded continuously, <i>A</i> = <i>Pe</i><sup><i>rt</i></sup>. How much is in the account after %d years? Round to the nearest dollar." % (comma(P), rate, t)
        right = "$%s" % comma(int(round(v)))
        w = ["$%s" % comma(int(round(P * (1 + rate / 100 * t)))), "$%s" % comma(int(round(P * (1 + rate / 100) ** t))), "$%s" % comma(int(round(P * math.exp(rate * t / 1000))))]
        e = "%s<i>e</i><sup>%s × %d</sup> = %s<i>e</i><sup>%s</sup> ≈ %s." % (comma(P), "0.%02d" % rate, t, comma(P), ("%.2f" % (rate / 100 * t)).rstrip("0").rstrip("."), right)
    else:
        v = math.log(2) / (rate / 100)
        q = "Money grows at %d%% compounded continuously. About how many years does it take to double? (Solve 2 = <i>e</i><sup>%s<i>t</i></sup>.)" % (rate, "0.%02d" % rate)
        right = "%s years" % num(v, 1)
        w = ["%s years" % num(100 / rate / 2, 1), "%s years" % num(100 / rate, 1), "%s years" % num(math.log10(2) / (rate / 100), 1)]
        e = "Take ln of both sides: ln 2 = %s<i>t</i>, so <i>t</i> = 0.693 ÷ %s ≈ %s." % ("0.%02d" % rate, "0.%02d" % rate, right)
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def one_logscale(r):
    kind = r.choice(["ph", "db", "quake", "quake2"])
    if kind == "ph":
        n = r.randint(2, 12)
        q = "pH = −log[H<sup>+</sup>]. A solution has [H<sup>+</sup>] = 10<sup>−%d</sup> moles per liter. What is its pH?" % n
        right, w = str(n), [sg(-n), sg(10 - n) if 10 - n not in (n, -n) else str(n + 1), "10<sup>%d</sup>" % n]
        e = "−log(10<sup>−%d</sup>) = −(−%d) = %d." % (n, n, n)
    elif kind == "db":
        n = r.randint(3, 12)
        q = "Loudness is <i>L</i> = 10 log(<i>I</i> ÷ <i>I</i><sub>0</sub>) decibels. A sound is 10<sup>%d</sup> times as intense as <i>I</i><sub>0</sub>. How loud is it?" % n
        right, w = "%d dB" % (10 * n), ["%d dB" % n, "%d dB" % (10 ** 1 + n), "%d dB" % (n * n)]
        e = "10 log(10<sup>%d</sup>) = 10 × %d = %d." % (n, n, 10 * n)
    elif kind == "quake":
        m1 = Fr(r.randint(40, 70), 10)
        dm = r.choice([1, 2, 3])
        q = "On the Richter scale, each increase of 1 means 10 times the shaking. How many times as strong is the shaking of a magnitude %s earthquake as one of magnitude %s?" % (("%.1f" % float(m1 + dm)), ("%.1f" % float(m1)))
        right, w = comma(10 ** dm) + " times", [str(dm) + " times", str(2 * dm) + " times", comma(10 ** (dm + 1)) + " times"]
        e = "The difference is %d, so 10<sup>%d</sup> = %s." % (dm, dm, comma(10 ** dm))
    else:
        a = r.randint(4, 8)
        b = a + r.choice([1, 2])
        q = "One sound is %d dB and another is %d dB. Since <i>L</i> = 10 log(<i>I</i> ÷ <i>I</i><sub>0</sub>), how many times as intense is the louder sound?" % (10 * a, 10 * b)
        right, w = comma(10 ** (b - a)) + " times", [str(10 * (b - a)) + " times", str(b - a) + " times", str(round(b / a, 2)) + " times"]
        e = "%d dB more means 10<sup>%d</sup> = %s times as intense." % (10 * (b - a), b - a, comma(10 ** (b - a)))
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def one_rat(r):
    kind = r.choice(["cost", "mix", "mixw"])
    if kind == "cost":
        F = r.choice([1200, 2000, 3000, 4500, 6000])
        v = r.choice([2, 3, 4, 5, 6])
        target = v + r.choice([1, 2, 3, 4, 5])
        x = F / (target - v)
        if x != int(x):
            raise AssertionError
        q = "A club pays $%s for a printer and $%d for each shirt it prints. The average cost per shirt is <i>C</i>(<i>x</i>) = <span class='fr'><span class='fn'>%s + %d<i>x</i></span><span class='fd'><i>x</i></span></span>. How many shirts make the average cost $%d?" % (comma(F), v, comma(F), v, target)
        right, w = comma(int(x)), [comma(F // target), comma(int(F / v)), comma(int(x) + target)]
        e = "%s + %d<i>x</i> = %d<i>x</i>, so %s = %d<i>x</i> and <i>x</i> = %s." % (comma(F), v, target, comma(F), target - v, comma(int(x)))
    else:
        V = r.choice([10, 20, 25, 40, 50])
        p = r.choice([20, 25, 30, 40, 50])
        acid = V * p / 100
        new = r.choice([c for c in (5, 8, 10, 12, 15, 20) if c < p])
        x = acid / (new / 100) - V
        if x <= 0 or x != int(x):
            raise AssertionError
        q = "A %d-liter mix is %d%% juice. How many liters of water must be added to make it %d%% juice? Use <i>C</i>(<i>x</i>) = <span class='fr'><span class='fn'>%s</span><span class='fd'>%d + <i>x</i></span></span>." % (V, p, new, ("%g" % acid), V)
        Lt = lambda v: "%d liter%s" % (v, "" if v == 1 else "s")
        right, w = Lt(x), [Lt(V * (p - new) // 100) if V * (p - new) // 100 != x else Lt(x + 5), Lt(acid / (new / 100)), Lt(p - new)]
        e = "%s ÷ (%d + <i>x</i>) = %s, so %d + <i>x</i> = %s and <i>x</i> = %d." % (("%g" % acid), V, "0.%02d" % new if new < 100 else "1", V, ("%g" % (acid / (new / 100))), x)
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def one_pow(r):
    kind = r.choice(["fall", "scale", "kepler", "vol"])
    if kind == "fall":
        t = r.randint(2, 10)
        if r.random() < 0.5:
            q = "A dropped object falls <i>d</i> = 16<i>t</i><sup>2</sup> feet in <i>t</i> seconds. How far does it fall in %d seconds?" % t
            right, w = "%s feet" % comma(16 * t * t), ["%d feet" % (32 * t), "%d feet" % (16 * t), "%s feet" % comma((16 * t) ** 2)]
            e = "16(%d)<sup>2</sup> = 16 × %d = %s." % (t, t * t, comma(16 * t * t))
        else:
            q = "A dropped object falls <i>d</i> = 16<i>t</i><sup>2</sup> feet in <i>t</i> seconds. How long does it take to fall %s feet?" % comma(16 * t * t)
            right, w = "%d seconds" % t, ["%d seconds" % (t * t), "%d seconds" % (2 * t), "%d seconds" % (16 * t * t // 32)]
            e = "16<i>t</i><sup>2</sup> = %s, so <i>t</i><sup>2</sup> = %d and <i>t</i> = %d." % (comma(16 * t * t), t * t, t)
    elif kind == "scale":
        k = r.choice([2, 3, 4, 5])
        q = "A model of a statue is enlarged so every length is %d times as long. The area of a surface is a power function of length, <i>A</i> = <i>kL</i><sup>2</sup>. How many times as much paint does the larger statue need?" % k
        right, w = "%d times" % (k * k), ["%d times" % k, "%d times" % (k ** 3), "%d times" % (2 * k)]
        e = "Area grows with the square of the length: %d<sup>2</sup> = %d." % (k, k * k)
    elif kind == "vol":
        k = r.choice([2, 3, 4])
        q = "Every length of a box is multiplied by %d. Volume is <i>V</i> = <i>kL</i><sup>3</sup>. How many times as large is the volume?" % k
        right, w = "%d times" % (k ** 3), ["%d times" % (k * k), "%d times" % k, "%d times" % (3 * k)]
        e = "Volume grows with the cube of the length: %d<sup>3</sup> = %d." % (k, k ** 3)
    else:
        a = r.choice([4, 9, 16, 25, 36])
        q = "Kepler's third law says <i>T</i> = <i>a</i><sup>3/2</sup>, where <i>a</i> is a planet's distance from the Sun in AU and <i>T</i> is its year in Earth years. A planet is %d AU from its star (which has the Sun's mass). How long is its year?" % a
        right, w = "%d Earth years" % int(round(a ** 1.5)), ["%d Earth years" % int(round(a * 1.5)), "%d Earth years" % (a * a), "%d Earth years" % int(round(a ** (2 / 3) + 0.0001))]
        e = "%d<sup>3/2</sup> = (√%d)<sup>3</sup> = %d<sup>3</sup> = %d." % (a, a, int(a ** 0.5), int(round(a ** 1.5)))
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Half-life models", [("collect", uniq(one_half), 20)]),
        ("Continuous growth", [("collect", uniq(one_cont), 20)]),
        ("Logarithmic scales", [("collect", uniq(one_logscale), 20)]),
        ("Rational models", [("collect", uniq(one_rat), 20)]),
        ("Power models", [("collect", uniq(one_pow), 20)]),
    ], 69809)
    finish(sets, R)
    body = lesson("<ul><li><b>Exponential</b>: growth or decay by the same factor each period. Half-life: <i>A</i> = <i>A</i><sub>0</sub>(<span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>)<sup><i>t</i>/<i>h</i></sup>. Continuous: <i>A</i> = <i>Pe</i><sup><i>rt</i></sup>.</li><li><b>Logarithmic</b> scales (pH, decibels, Richter) count powers of 10: one step means 10 times as much.</li><li><b>Rational</b> models divide by a changing amount, like average cost or the strength of a mixture.</li><li><b>Power</b> models <i>y</i> = <i>kx</i><sup><i>n</i></sup>: area grows with the square of length, volume with the cube.</li></ul>",
        [example("Half-life 5 days, 80 mg, 15 days", ["15 ÷ 5 = 3 half-lives", "80 ÷ 2<sup>3</sup>"], "10 mg"), example("pH with [H<sup>+</sup>] = 10<sup>−4</sup>", ["−log 10<sup>−4</sup> = 4"], "pH 4")],
        [['Dividing by the half-life', "<i>t</i> ÷ <i>h</i> is the exponent of <span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>."], ['Reading a log scale as linear', 'Magnitude 6 shakes 10 times as much as 5.'], ['Squaring for volume', 'Volume uses the cube of the scale factor.']])
    faq = [('What does TEKS P.2N ask?', 'Analyze situations modeled by functions, including exponential, logarithmic, rational, and polynomial, and power functions, to solve real-world problems.'), ('How do you choose a model?', 'Equal factors: exponential. Powers of 10 on a scale: logarithmic. Dividing by a quantity: rational. A fixed power of x: power.'), ('Why does continuous growth use e?', 'It is the limit of compounding more and more often.'), ('Is a log scale a straight scale?', 'No. Equal steps mean equal ratios.')]
    make('modeling-with-functions', 9, 'Functions', 'P.2N',
         'P.2N analyze situations modeled by functions, including exponential, logarithmic, rational, polynomial, and power functions, to solve real-world problems',
         'Modeling with Exponential, Logarithmic, Rational and Power Functions', 'Modeling with Functions',
         'Free Precalculus modeling worksheets for Texas TEKS P.2N: half-life, continuous growth, pH, decibels and earthquakes, rational and power function models. 100 questions with answers.',
         'Choose the model by how the quantity changes.', 'One step on a log scale means 10 times as much.',
         body, faq, sets, seo_title='Precalculus Modeling with Functions Worksheets (TEKS P.2N)')


if __name__ == "__main__":
    build()
