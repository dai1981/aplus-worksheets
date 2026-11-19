# -*- coding: utf-8 -*-
"""
Texas Precalculus: Logarithmic and Exponential Equations (TEKS P.5F, P.5G, P.5H)
  python3 tools/gen_ustx_math_pc_exp_log_equations.py
Properties of logarithms, change of base, solving exponential and logarithmic equations, and applications (US
Algebra 2 makers with a new seed), plus natural log equations and time-to-reach problems (own makers).
Wrong answers come from real mistakes: log(M + N) = log M + log N, dividing instead of taking logs, and forgetting to
check the domain.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a2_logarithms_and_their_properties as lg
adopt(lg)
lg.R = random.Random(698260)
import gen_us_math_a2_exponential_and_logarithmic_equations as el
adopt(el)
el.R = random.Random(698261)
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


def r2(v):
    return ("%.2f" % v).replace("-", MINUS)


def one_ln(r):
    kind = r.choice(["ln", "lin"])
    a = r.choice([n for n in range(-9, 10) if n])
    b = r.choice([1, 2, 3, Fr(1, 2), Fr(3, 2)])
    if kind == "ln":
        q = "Solve ln(<i>x</i> %s %d) = %s. Round to the nearest hundredth." % ("+" if a > 0 else MINUS, abs(a), ft(b))
        v = math.exp(float(b)) - a
        if v + a <= 0:
            raise AssertionError
        right, w = r2(v), [r2(float(b) - a), r2(math.exp(float(b)) + a), r2(10 ** float(b) - a)]
        e = "Rewrite: <i>x</i> %s %d = <i>e</i><sup>%s</sup>, so <i>x</i> = <i>e</i><sup>%s</sup> %s %d ≈ %s." % ("+" if a > 0 else MINUS, abs(a), ft(b), ft(b), MINUS if a > 0 else "+", abs(a), right)
    elif kind == "exp":
        c = r.choice([5, 8, 12, 20, 30, 50, 100])
        k = r.choice([2, 3, 4, Fr(1, 2)])
        q = "Solve <i>e</i><sup>%s<i>x</i></sup> = %d. Round to the nearest hundredth." % ("" if k == 1 else ft(k), c)
        v = math.log(c) / float(k)
        right, w = r2(v), [r2(math.log(c) * float(k)), r2(c / math.e / float(k)), r2(math.log10(c) / float(k))]
        e = "Take ln of both sides: %s<i>x</i> = ln %d, so <i>x</i> = ln %d ÷ %s ≈ %s." % ("" if k == 1 else ft(k), c, c, ft(k), right)
    else:
        m = r.choice([2, 3, 5])
        c = r.choice([n for n in range(-6, 7) if n])
        d = r.choice([1, 2, 3])
        q = "Solve %d ln <i>x</i> %s %d = %s. Round to the nearest hundredth." % (m, "+" if c > 0 else MINUS, abs(c), sg(d + c))
        v = math.exp(d / m)
        right, w = r2(v), [r2(d / m), r2(math.exp(d)), r2(10 ** (d / m))]
        e = "%d ln <i>x</i> = %d, ln <i>x</i> = %s, <i>x</i> = <i>e</i><sup>%s</sup> ≈ %s." % (m, d, ft(Fr(d, m)), ft(Fr(d, m)), right)
    w = [x for x in dict.fromkeys(w) if x != right]
    return mcq(q, right, w, e + " <b>%s</b>." % right)


CTX = [("A town of %(p)s people grows by %(r)s%% each year.", "people", "reach %(t)s people"), ("A savings account of $%(p)s earns %(r)s%% interest compounded yearly.", "$", "grow to $%(t)s"),
       ("A rabbit population of %(p)s grows by %(r)s%% each month.", "rabbits", "reach %(t)s rabbits"), ("A colony of %(p)s bacteria grows by %(r)s%% each hour.", "bacteria", "reach %(t)s bacteria")]


def one_time(r):
    t, u, goal = r.choice(CTX)
    p = r.choice([500, 800, 1000, 2000, 5000, 12000])
    rate = r.choice([3, 4, 5, 6, 8, 10, 12, 15])
    mult = r.choice([2, 3, Fr(3, 2), 5])
    target = int(p * mult)
    per = "year" if "year" in t else ("month" if "month" in t else "hour")
    q = (t % {"p": comma(p), "r": rate}) + " About how many %ss will it take to %s? Round to the nearest tenth." % (per, goal % {"t": comma(target)})
    v = math.log(float(mult)) / math.log(1 + rate / 100)
    right = "%s %ss" % (("%.1f" % v), per)
    w = ["%s %ss" % (("%.1f" % (float(mult - 1) * 100 / rate)), per), "%s %ss" % (("%.1f" % (math.log(float(mult)) / (rate / 100) * 1.2 + 0.3)), per), "%s %ss" % (("%.1f" % (float(mult) / (1 + rate / 100))), per)]
    w = [x for x in dict.fromkeys(w) if x != right]
    return mcq(q, right, w, "%s(%s)<sup><i>t</i></sup> = %s, so (%s)<sup><i>t</i></sup> = %s and <i>t</i> = log %s ÷ log %s ≈ %s." % (
        comma(p), "%.2f" % (1 + rate / 100), comma(target), "%.2f" % (1 + rate / 100), ft(mult), ft(mult), "%.2f" % (1 + rate / 100), ("%.1f" % v)) + " <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Properties of logarithms", [("collect", W(lg.one_exp), 10), ("collect", W(lg.one_cond), 10)]),
        ("Change of base", [("collect", W(lg.one_cob), 20)]),
        ("Solve exponential equations", [("collect", W(el.one_log), 10), ("collect", W(el.one_base), 10)]),
        ("Solve logarithmic equations", [("collect", W(el.one_logeq), 10), ("collect", uniq(one_ln), 10)]),
        ("Exponential and logarithmic models", [("collect", W(el.one_app), 10), ("collect", uniq(one_time), 10)]),
    ], 69826)
    finish(sets, R)
    body = lesson("<ul><li>Product: log <i>MN</i> = log <i>M</i> + log <i>N</i>. Quotient: log <span class='fr'><span class='fn'><i>M</i></span><span class='fd'><i>N</i></span></span> = log <i>M</i> − log <i>N</i>. Power: log <i>M</i><sup><i>k</i></sup> = <i>k</i> log <i>M</i>.</li><li>Change of base: log<sub><i>b</i></sub> <i>x</i> = <span class='fr'><span class='fn'>ln <i>x</i></span><span class='fd'>ln <i>b</i></span></span>.</li><li>Exponential equation: get the power alone, then take a log of both sides.</li><li>Log equation: combine the logs, rewrite in exponential form, and check that every log input is positive.</li></ul>",
        [example("1,000(1.05)<sup><i>t</i></sup> = 2,000", ["1.05<sup><i>t</i></sup> = 2", "<i>t</i> = log 2 ÷ log 1.05"], "<i>t</i> ≈ 14.2")],
        [['log(<i>M</i> + <i>N</i>) = log <i>M</i> + log <i>N</i>', 'The product rule is for log <i>MN</i>.'], ['Dividing instead of taking logs', '1.05<sup><i>t</i></sup> = 2 needs logarithms.'], ['Not checking', 'A log input must be positive.']])
    faq = [('What does TEKS P.5F ask?', 'Use the properties of logarithms to evaluate or transform logarithmic expressions.'), ('What does TEKS P.5G ask?', 'Generate and solve logarithmic equations in mathematical and real-world problems.'), ('What does TEKS P.5H ask?', 'Generate and solve exponential equations in mathematical and real-world problems.'), ('Which log should I use?', 'Any base works; ln and log are on calculators.')]
    make('logarithmic-and-exponential-equations', 26, 'Algebraic Reasoning', 'P.5F, P.5G, P.5H',
         'P.5F use the properties of logarithms to evaluate or transform logarithmic expressions; P.5G generate and solve logarithmic equations in mathematical and real-world problems; P.5H generate and solve exponential equations in mathematical and real-world problems',
         'Logarithmic and Exponential Equations', 'Log and Exponential Equations',
         'Free Precalculus worksheets on logarithmic and exponential equations for Texas TEKS P.5F to P.5H: log properties, change of base, solving equations and growth models. 100 questions with answers.',
         'Get the power alone, then take a log of both sides.', 'Check that every log input is positive.',
         body, faq, sets, seo_title='Precalculus Logarithmic and Exponential Equations Worksheets (TEKS P.5F–P.5H)')


if __name__ == "__main__":
    build()
