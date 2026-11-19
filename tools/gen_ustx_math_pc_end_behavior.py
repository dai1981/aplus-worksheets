# -*- coding: utf-8 -*-
"""
Texas Precalculus: End Behavior of Functions (TEKS P.2J)
  python3 tools/gen_ustx_math_pc_end_behavior.py
End behavior of polynomials in words (US Algebra 2 maker with a new seed) and in infinity notation, and end behavior
of exponential, logarithmic and rational functions and of real-world models (own makers).
Wrong answers come from real mistakes: using the first term written instead of the leading term, forgetting the
vertical shift of an exponential, and using the ratio of coefficients when the degrees differ.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a2_polynomial_functions_and_zeros as pz
adopt(pz)
pz.R = random.Random(698060)
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


INF = "∞"
PI, NI = INF, MINUS + INF


def lim(side, val):
    return "As <i>x</i> → %s, <i>f</i>(<i>x</i>) → %s" % (PI if side > 0 else NI, val)


def one_poly(r):
    n = r.randint(2, 7)
    a = r.choice([1, 2, 3, 4, 5, -1, -2, -3, -4])
    cs = [a] + [r.randint(-9, 9) for _ in range(n)]
    terms = poly(cs)
    side = r.choice([1, -1])
    sgn = (1 if a > 0 else -1) * (1 if side > 0 or n % 2 == 0 else -1)
    right = lim(side, PI if sgn > 0 else NI)
    w = [lim(side, NI if sgn > 0 else PI), lim(side, "0"), lim(side, sg(a))]
    return mcq("Which describes the end behavior of %s?" % fx(terms), right, w,
               "Only the leading term %s<i>x</i><sup>%d</sup> matters for large |<i>x</i>|. Degree %d is %s and the leading coefficient is %s. <b>%s</b>." % (
                   sg(a) if abs(a) != 1 else ("" if a == 1 else MINUS), n, n, "even" if n % 2 == 0 else "odd", "positive" if a > 0 else "negative", right))


def one_exp(r):
    kind = r.choice(["grow", "decay", "log", "neg"])
    a = r.choice([1, 2, 3, 5])
    d = r.choice([n for n in range(-9, 10) if n])
    tail = " %s %d" % ("+" if d > 0 else MINUS, abs(d))
    co = "" if a == 1 else "%d · " % a
    if kind == "grow":
        b = r.choice([2, 3, 10, "<i>e</i>"])
        f = fx("%s%s<sup><i>x</i></sup>%s" % (co, b, tail))
        side = r.choice([1, -1])
        right = lim(side, PI if side > 0 else sg(d))
        w = [lim(side, NI if side > 0 else PI), lim(side, "0") if d else lim(side, "1"), lim(side, sg(-d)) if side < 0 else lim(side, sg(d))]
        e = "%s grows without bound to the right and gets close to 0 to the left, so <i>f</i> gets close to %s." % (str(b) + "<sup><i>x</i></sup>", sg(d))
    elif kind == "decay":
        b = r.choice(["0.5", "<span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span>", "0.8"])
        f = fx("%s(%s)<sup><i>x</i></sup>%s" % (co.replace(" · ", ""), b, tail))
        side = r.choice([1, -1])
        right = lim(side, sg(d) if side > 0 else PI)
        w = [lim(side, "0") if side > 0 else lim(side, NI), lim(side, PI) if side > 0 else lim(side, sg(d)), lim(side, sg(-d))]
        e = "A base between 0 and 1 gets close to 0 to the right and grows to the left."
    elif kind == "log":
        f = fx("%slog(<i>x</i>)%s" % ("" if a == 1 else str(a), tail))
        right = lim(1, PI)
        w = [lim(1, sg(d)), lim(1, "0"), lim(1, NI)]
        e = "A logarithm keeps growing (slowly) without bound."
    else:
        b = r.choice([2, 3, 10])
        f = fx("−%s%d<sup><i>x</i></sup>%s" % (co, b, tail))
        side = r.choice([1, -1])
        right = lim(side, NI if side > 0 else sg(d))
        w = [lim(side, PI if side > 0 else sg(-d)), lim(side, "0"), lim(side, sg(d)) if side > 0 else lim(side, NI)]
        e = "The negative sign reflects the graph: it falls to the right and gets close to %s to the left." % sg(d)
    return mcq("Which describes the end behavior of %s?" % f, right, w, e + " <b>%s</b>." % right)


def one_rat(r):
    n = r.randint(1, 3)
    m = r.choice([n - 1, n, n, n + 1]) if n > 1 else r.choice([n, n + 1])
    a, b = r.choice([2, 3, 4, 6, -2, -3, 8]), r.choice([1, 2, 3, -1, 4])
    top = [a] + [r.randint(-6, 6) for _ in range(n)]
    bot = [b] + [r.randint(-6, 6) for _ in range(m)]
    if bot[-1] == 0:
        bot[-1] = 1
    f = fx("<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (poly(top), poly(bot)))
    if n < m:
        val, e = "0", "The degree of the bottom is bigger, so <i>f</i>(<i>x</i>) → 0."
    elif n == m:
        val, e = ft(Fr(a, b)), "The degrees are equal, so <i>f</i>(<i>x</i>) gets close to the ratio of the leading coefficients, %s ÷ %s." % (sg(a), sg(b))
    else:
        val = PI if a * b > 0 else NI
        e = "The top has a bigger degree, so <i>f</i> grows without bound (it follows a slant line)."
    right = lim(1, val)
    alts = ["0", ft(Fr(a, b)), PI, NI, sg(a)]
    w = [lim(1, v) for v in alts if v != val][:3]
    return mcq("Which describes the end behavior of %s?" % f, right, w, e + " <b>%s</b>." % right)


def one_ctx(r):
    kind = r.choice(["log", "cool", "cost", "drug"])
    if kind == "log":
        L = r.choice([500, 800, 1000, 1200, 2000, 5000])
        c = r.choice([4, 9, 19, 24])
        k = r.choice(["0.2", "0.3", "0.5"])
        q = "A population of fish is modeled by <i>P</i>(<i>t</i>) = <span class='fr'><span class='fn'>%s</span><span class='fd'>1 + %d<i>e</i><sup>−%s<i>t</i></sup></span></span>. What happens to <i>P</i>(<i>t</i>) as <i>t</i> → ∞?" % (comma(L), c, k)
        right = "It gets close to %s" % comma(L)
        w = ["It gets close to %s" % comma(L // (c + 1)), "It grows without bound", "It gets close to 0"]
        e = "<i>e</i><sup>−%s<i>t</i></sup> → 0, so the bottom → 1 and <i>P</i> → %s (the carrying capacity)." % (k, comma(L))
    elif kind == "cool":
        room = r.choice([68, 70, 72, 75])
        d = r.choice([110, 120, 130, 140])
        q = "The temperature of a cup of coffee is <i>T</i>(<i>t</i>) = %d + %d<i>e</i><sup>−0.1<i>t</i></sup> °F after <i>t</i> minutes. What happens to <i>T</i> as <i>t</i> → ∞?" % (room, d)
        right = "It gets close to %d°F" % room
        w = ["It gets close to %d°F" % (room + d), "It gets close to 0°F", "It decreases without bound"]
        e = "<i>e</i><sup>−0.1<i>t</i></sup> → 0, so <i>T</i> → %d, the room temperature." % room
    elif kind == "cost":
        F = r.choice([2000, 5000, 8000, 12000])
        v = r.choice([3, 4, 5, 8, 12])
        q = "The average cost per item of making <i>x</i> items is <i>C</i>(<i>x</i>) = <span class='fr'><span class='fn'>%s + %d<i>x</i></span><span class='fd'><i>x</i></span></span> dollars. What happens to <i>C</i>(<i>x</i>) as <i>x</i> → ∞?" % (comma(F), v)
        right = "It gets close to $%d" % v
        w = ["It gets close to $%s" % comma(F), "It gets close to $0", "It grows without bound"]
        e = "<i>C</i>(<i>x</i>) = %s ÷ <i>x</i> + %d, and %s ÷ <i>x</i> → 0." % (comma(F), v, comma(F))
    else:
        a = r.choice([20, 30, 40, 50])
        c = r.choice([4, 9, 16])
        q = "The amount of a medicine in the blood is <i>C</i>(<i>t</i>) = <span class='fr'><span class='fn'>%d<i>t</i></span><span class='fd'><i>t</i><sup>2</sup> + %d</span></span> mg/L after <i>t</i> hours. What happens to <i>C</i>(<i>t</i>) as <i>t</i> → ∞?" % (a, c)
        right = "It gets close to 0"
        w = ["It gets close to %d" % a, "It grows without bound", "It gets close to %s" % ft(Fr(a, c))]
        e = "The bottom has the bigger degree, so <i>C</i> → 0: the medicine leaves the body."
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("End behavior of polynomials", [("collect", W(pz.one_end), 20)]),
        ("Infinity notation for polynomials", [("collect", uniq(one_poly), 20)]),
        ("Exponential and logarithmic functions", [("collect", uniq(one_exp), 20)]),
        ("Rational functions", [("collect", uniq(one_rat), 20)]),
        ("End behavior of real-world models", [("collect", uniq(one_ctx), 20)]),
    ], 69806)
    finish(sets, R)
    body = lesson('<ul><li><b>End behavior</b> is what <i>f</i>(<i>x</i>) does as <i>x</i> → ∞ and as <i>x</i> → −∞.</li><li>Polynomial: only the leading term matters. Even degree: both ends the same way. Odd degree: opposite ways. A negative leading coefficient flips them.</li><li><i>a</i> · <i>b</i><sup><i>x</i></sup> + <i>d</i> gets close to <i>d</i> on one side (the horizontal asymptote).</li><li>Rational: compare degrees. Bottom bigger → 0; equal → ratio of leading coefficients; top bigger → ±∞.</li></ul>',
        [example("<i>f</i>(<i>x</i>) = −2<i>x</i><sup>3</sup> + 5<i>x</i>", ["Odd degree, negative leading coefficient"], "As <i>x</i> → ∞, <i>f</i>(<i>x</i>) → −∞; as <i>x</i> → −∞, <i>f</i>(<i>x</i>) → ∞")],
        [['Using the first term written', 'Find the term with the highest power.'], ['Forgetting the shift', '2<sup><i>x</i></sup> − 3 → −3 as <i>x</i> → −∞.'], ['Ratio when the degrees differ', 'Use the ratio only for equal degrees.']])
    faq = [('What does TEKS P.2J ask?', 'Analyze and describe end behavior of functions, including exponential, logarithmic, rational, polynomial, and power functions, using infinity notation to communicate this characteristic in mathematical and real-world problems.'), ('What does x → ∞ mean?', 'x gets larger and larger without bound.'), ('Can a function cross its horizontal asymptote?', 'Yes, in the middle; the asymptote describes the ends.'), ('Why do logs grow so slowly?', 'Each step of 1 in log x needs x to be 10 times bigger.')]
    make('end-behavior', 6, 'Functions', 'P.2J',
         'P.2J analyze and describe end behavior of functions, including exponential, logarithmic, rational, polynomial, and power functions, using infinity notation to communicate this characteristic in mathematical and real-world problems',
         'End Behavior of Functions', 'End Behavior',
         'Free Precalculus end behavior worksheets for Texas TEKS P.2J: polynomials, exponential, logarithmic and rational functions in infinity notation, and real-world models. 100 questions with answers.',
         "Only the leading term decides a polynomial's end behavior.", 'Rational: compare the degrees of the top and bottom.',
         body, faq, sets, seo_title='Precalculus End Behavior Worksheets (TEKS P.2J)')


if __name__ == "__main__":
    build()
