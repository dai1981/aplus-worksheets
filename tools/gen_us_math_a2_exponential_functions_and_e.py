# -*- coding: utf-8 -*-
"""
US Algebra 2: Exponential Functions and the Number e (Common Core F-IF.C.8b, F-LE.A.2, F-BF.B.3)
  python3 tools/gen_us_math_a2_exponential_functions_and_e.py
Growth or decay and the growth rate, graphs and asymptotes, compound interest n times a year, continuous
growth with e, and half-life and doubling.
Wrong answers come from real mistakes: reading the rate as the base, forgetting to divide the rate by n,
using the percent as a whole number, and confusing the horizontal asymptote with the y-intercept.
"""
import math
import random
from decimal import Decimal, ROUND_HALF_UP
from us_hs import B, S, make, lesson, collect, T, num, MINUS, People, usd
from a2_common import sf

R = random.Random(95901)


def money(x):
    return "$" + "{:,.2f}".format(float(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)))


def r2(x):
    return "{:,.2f}".format(float(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)))


def pct(x):
    s = ("%.2f" % x).rstrip("0").rstrip(".")
    return s + "%"


# ------------------------------------------------------------ set 1: growth or decay
def one_gd(r):
    kind = r.choice(["rate", "rate", "type", "e"])
    a = r.choice([50, 100, 200, 250, 500, 1200, 3000])
    if kind in ("rate", "type"):
        rate = r.choice([2, 3, 4, 5, 6, 8, 12, 15, 20, 25, 35])
        up = r.random() < 0.5
        b = 1 + rate / 100 if up else 1 - rate / 100
        bs = ("%.2f" % b).rstrip("0").rstrip(".")
        fx = "<i>y</i> = %s(%s)<sup><i>t</i></sup>" % (num(a), bs)
        if kind == "type":
            right = "Exponential %s" % ("growth" if up else "decay")
            return T("Does %s show exponential growth or decay?" % B(fx), right,
                     [x for x in ["Exponential growth", "Exponential decay", "Linear growth", "Linear decay"] if x != right],
                     "The base %s is %s 1, so the function %s. <b>%s</b>." % (bs, "greater than" if up else "between 0 and", "grows" if up else "decays", right))
        right = "%s %s" % (pct(rate), "growth" if up else "decay")
        wr = ["%s %s" % (pct(rate), "decay" if up else "growth"), "%s %s" % (pct(b * 100), "growth" if up else "decay"), "%s %s" % (pct(100 - rate), "growth" if up else "decay")]
        return T("What is the percent rate of change in %s?" % B(fx), right, [w for w in dict.fromkeys(wr) if w != right][:3],
                 "Write the base as 1 %s <i>r</i>: %s = 1 %s %s. <b>%s</b>." % ("+" if up else MINUS, bs, "+" if up else MINUS, ("%.2f" % (rate / 100)).rstrip("0").rstrip("."), right))
    k = r.choice([0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.1, 0.12])
    up = r.random() < 0.5
    ks = ("%.2f" % k).rstrip("0").rstrip(".")
    fx = "<i>y</i> = %s<i>e</i><sup>%s%s<i>t</i></sup>" % (num(a), "" if up else MINUS, ks)
    right = "Continuous %s at %s per unit of time" % ("growth" if up else "decay", pct(k * 100))
    return T("What does %s model?" % B(fx), right, ["Continuous %s at %s per unit of time" % ("decay" if up else "growth", pct(k * 100)),
                                                  "Continuous %s at %s per unit of time" % ("growth" if up else "decay", pct(k)), "Linear %s of %s per unit of time" % ("growth" if up else "decay", ks)],
             "In <i>y</i> = <i>ae</i><sup><i>kt</i></sup>, <i>k</i> is the continuous rate: <i>k</i> = %s%s = %s%s, so %s. <b>%s</b>." % ("" if up else MINUS, ks, "" if up else MINUS, pct(k * 100), "growth" if up else "decay", right))


# ------------------------------------------------------------ set 2: graphs and key features
def one_feat(r):
    a = r.choice([1, 2, 3, 4, 5])
    b = r.choice([2, 3, 4, 5])
    h, k = r.randint(-4, 4), r.randint(-5, 5)
    kind = r.choice(["asym", "asym", "yint", "range", "eval"])
    sign = r.choice([1, 1, -1])
    pre = ("" if a == 1 else num(a)) if sign > 0 else (MINUS + ("" if a == 1 else num(a)))
    ex = "<i>x</i>" if h == 0 else "<i>x</i> %s %d" % (MINUS if h > 0 else "+", abs(h))
    fx = "<i>f</i>(<i>x</i>) = %s(%d)<sup>%s</sup>%s" % (pre, b, ex, (" %s %d" % ("+" if k > 0 else MINUS, abs(k))) if k else "")
    if kind == "asym":
        right = "<i>y</i> = %s" % sf(k)
        return T("What is the horizontal asymptote of %s?" % B(fx), right, ["<i>y</i> = %s" % sf(-k) if k else "<i>y</i> = %d" % a, "<i>x</i> = %s" % sf(h), "<i>y</i> = %s" % sf(sign * a + k) if sign * a + k != k else "<i>y</i> = 1"],
                 "The parent <i>b</i><sup><i>x</i></sup> has asymptote <i>y</i> = 0. Only a vertical shift moves it: <b>%s</b>." % right)
    if kind == "range":
        right = "<i>y</i> %s %s" % ("&gt;" if sign > 0 else "&lt;", sf(k))
        return T("What is the range of %s?" % B(fx), right, ["<i>y</i> %s %s" % ("&lt;" if sign > 0 else "&gt;", sf(k)), "All real numbers", "<i>y</i> %s %s" % ("&gt;" if sign > 0 else "&lt;", sf(h))],
                 "The graph approaches <i>y</i> = %s but never reaches it, and it lies %s the asymptote. <b>%s</b>." % (sf(k), "above" if sign > 0 else "below", right))
    from fractions import Fraction as F
    xv = 0 if kind == "yint" else r.randint(h - 1, h + 3)
    val = sign * a * F(b) ** (xv - h) + k
    if val.denominator > 125:
        return None
    if kind == "yint":
        q = "What is the <i>y</i>-intercept of %s?" % B(fx)
    else:
        q = "Find <i>f</i>(%s) for %s." % (sf(xv), B(fx))
    wrongs = [sign * a * b * (xv - h) + k, sign * a + k, val - k, sign * (a * b) ** (xv - h) + k if xv - h >= 0 else val + 1]
    return T(q, sf(val), [sf(w) for w in dict.fromkeys(F(x) for x in wrongs) if w != val][:3],
             "Substitute <i>x</i> = %s: %s · %d<sup>%s</sup> %s = <b>%s</b>." % (sf(xv), sf(sign * a), b, sf(xv - h), ("+ %d" % k) if k >= 0 else ("%s %d" % (MINUS, -k)), sf(val)))


# ------------------------------------------------------------ set 3: compound interest
def one_ci(r):
    P = r.choice([500, 1000, 1500, 2000, 2500, 5000, 8000, 10000])
    rate = r.choice([2, 3, 4, 5, 6, 2.5, 3.5, 4.5])
    t = r.choice([2, 3, 4, 5, 8, 10])
    n, word = r.choice([(1, "annually"), (4, "quarterly"), (12, "monthly"), (2, "semiannually")])
    A = P * (1 + rate / 100 / n) ** (n * t)
    q = "%s is invested at %s interest compounded %s. How much is in the account after %d years?" % ("$" + num(P), pct(rate), word, t)
    wr = [P * (1 + rate / 100) ** (n * t), P * (1 + rate / 100 * t), P * (1 + rate / n) ** t if rate / n < 2 else P * (1 + rate / 100) ** t * 1.001, P * math.exp(rate / 100 * t)]
    right = money(A)
    out = [money(w) for w in wr if money(w) != right]
    out = list(dict.fromkeys(out))[:3]
    return T(q, right, out,
             "<i>A</i> = <i>P</i>(1 + <i>r</i>/<i>n</i>)<sup><i>nt</i></sup> = %s(1 + %s/%d)<sup>%d</sup> = <b>%s</b>." % (num(P), ("%.4f" % (rate / 100)).rstrip("0"), n, n * t, right))


# ------------------------------------------------------------ set 4: continuous growth with e
def one_e(r):
    kind = r.choice(["cont", "cont", "pop", "comp"])
    if kind == "cont":
        P = r.choice([1000, 2000, 2500, 4000, 5000])
        rate = r.choice([2, 3, 4, 5, 6])
        t = r.choice([3, 5, 6, 8, 10])
        A = P * math.exp(rate / 100 * t)
        q = "%s is invested at %d%% interest compounded continuously. What is the balance after %d years?" % ("$" + num(P), rate, t)
        right = money(A)
        wr = [P * (1 + rate / 100) ** t, P * (1 + rate / 100 * t), P * math.exp(rate * t / 10) if rate * t < 40 else P * math.exp(rate / 100) * t]
        return T(q, right, list(dict.fromkeys(money(w) for w in wr if money(w) != right))[:3],
                 "<i>A</i> = <i>Pe</i><sup><i>rt</i></sup> = %s<i>e</i><sup>%s × %d</sup> = <b>%s</b>." % (num(P), ("%.2f" % (rate / 100)), t, right))
    if kind == "pop":
        P0 = r.choice([1200, 5000, 8000, 15000, 40000])
        k = r.choice([0.01, 0.02, 0.03, 0.015])
        t = r.choice([5, 10, 15, 20])
        down = r.random() < 0.4
        val = P0 * math.exp((-k if down else k) * t)
        q = "A town's population is modeled by <i>P</i>(<i>t</i>) = %s<i>e</i><sup>%s%s<i>t</i></sup>, where <i>t</i> is in years. What is the population after %d years, to the nearest person?" % (
            num(P0), MINUS if down else "", ("%.3f" % k).rstrip("0"), t)
        right = num(round(val))
        wr = [round(P0 * math.exp((k if down else -k) * t)), round(P0 * (1 + (-k if down else k) * t)), round(P0 * (1 - k if down else 1 + k) ** t) if round(P0 * (1 - k if down else 1 + k) ** t) != round(val) else round(val) + 15]
        return T(q, right, [num(w) for w in dict.fromkeys(wr) if num(w) != right][:3],
                 "Substitute <i>t</i> = %d: %s<i>e</i><sup>%s</sup> ≈ <b>%s</b>." % (t, num(P0), sf((-k if down else k) * t) if False else (MINUS if down else "") + ("%.3f" % (k * t)).rstrip("0").rstrip("."), right))
    P = r.choice([1000, 5000, 10000])
    rate = r.choice([4, 5, 6, 8])
    t = 10
    annual = P * (1 + rate / 100) ** t
    cont = P * math.exp(rate / 100 * t)
    q = "%s grows at %d%% for %d years. How much more does continuous compounding earn than annual compounding?" % ("$" + num(P), rate, t)
    right = money(cont - annual)
    return T(q, right, [money(cont - P * (1 + rate / 100 * t)), money(cont), money((cont - annual) * 10)],
             "Continuous: %s. Annual: %s. Difference: <b>%s</b>. More frequent compounding always earns a little more." % (money(cont), money(annual), right))


# ------------------------------------------------------------ set 5: half-life and doubling
def one_half(r):
    pp = People(r)
    nm, he, his = pp.next()
    kind = r.choice(["half", "half", "double", "write", "write"])
    if kind == "half":
        A0 = r.choice([80, 120, 200, 320, 400, 640, 800])
        hl = r.choice([3, 5, 8, 10, 12, 20, 30])
        n = r.choice([2, 3, 4])
        t = n * hl
        val = A0 / 2 ** n
        q = "A substance has a half-life of %d days. A sample has %d mg. How much is left after %d days?" % (hl, A0, t)
        right = "%s mg" % (("%.2f" % val).rstrip("0").rstrip("."))
        wr = [A0 / (2 * n), A0 - A0 / 2 * n if A0 - A0 / 2 * n > 0 else A0 / 2 ** (n + 1), A0 / 2 ** (n - 1)]
        return T(q, right, ["%s mg" % (("%.2f" % w).rstrip("0").rstrip(".")) for w in dict.fromkeys(wr) if ("%s mg" % (("%.2f" % w).rstrip("0").rstrip("."))) != right][:3],
                 "%d days is %d half-lives. %d × (½)<sup>%d</sup> = <b>%s</b>." % (t, n, A0, n, right))
    if kind == "double":
        P0 = r.choice([100, 250, 500, 1000])
        d = r.choice([2, 3, 4, 6])
        n = r.choice([3, 4, 5])
        q = "A bacteria culture starts with %s cells and doubles every %d hours. How many cells are there after %d hours?" % (num(P0), d, d * n)
        val = P0 * 2 ** n
        return T(q, num(val), [num(P0 * 2 * n), num(P0 * 2 ** (n * d)) if P0 * 2 ** (n * d) < 10 ** 9 else num(val * 2), num(P0 * 2 ** (n - 1))],
                 "%d hours is %d doubling periods: %s × 2<sup>%d</sup> = <b>%s</b>." % (d * n, n, num(P0), n, num(val)))
    A0 = r.choice([50, 100, 400, 600])
    hl = r.choice([4, 6, 10, 25])
    q = "A drug has a half-life of %d hours and the first dose is %d mg. Which function gives the amount left after <i>t</i> hours?" % (hl, A0)
    right = "<i>A</i>(<i>t</i>) = %d(½)<sup><i>t</i>/%d</sup>" % (A0, hl)
    return T(q, right, ["<i>A</i>(<i>t</i>) = %d(½)<sup>%d<i>t</i></sup>" % (A0, hl), "<i>A</i>(<i>t</i>) = %d(2)<sup><i>t</i>/%d</sup>" % (A0, hl), "<i>A</i>(<i>t</i>) = %d %s %d<i>t</i>" % (A0, MINUS, A0 // (2 * hl)) if A0 % (2 * hl) == 0 else "<i>A</i>(<i>t</i>) = %d(0.5)<i>t</i>" % A0],
             "The amount halves once every %d hours, so the exponent counts half-lives: <i>t</i>/%d. <b>%s</b>." % (hl, hl, right))


def build():
    sets = [S("Growth or decay", collect(one_gd, 20, R)),
            S("Key features of exponential functions", collect(one_feat, 20, R)),
            S("Compound interest", collect(one_ci, 20, R)),
            S("Continuous growth with e", collect(one_e, 20, R)),
            S("Half-life and doubling", collect(one_half, 20, R))]
    body = lesson(
        "<p>An exponential function <i>y</i> = <i>a</i>(<i>b</i>)<sup><i>x</i></sup> multiplies by the same factor <i>b</i> each step. If <i>b</i> &gt; 1 it shows <b>growth</b> and if 0 &lt; <i>b</i> &lt; 1 it shows <b>decay</b>. "
        "Write <i>b</i> = 1 + <i>r</i> (growth) or 1 %s <i>r</i> (decay) to read the percent rate.</p>"
        "<p><i>y</i> = <i>a</i>(<i>b</i>)<sup><i>x</i> %s <i>h</i></sup> + <i>k</i> has the horizontal asymptote <i>y</i> = <i>k</i>.</p>"
        "<ul><li>Compound interest: <i>A</i> = <i>P</i>(1 + <i>r</i>/<i>n</i>)<sup><i>nt</i></sup>.</li>"
        "<li>Continuous growth: <i>A</i> = <i>Pe</i><sup><i>rt</i></sup>, where <i>e</i> ≈ 2.718.</li>"
        "<li>Half-life: <i>A</i> = <i>A</i><sub>0</sub>(½)<sup><i>t</i>/<i>h</i></sup>.</li></ul>" % (MINUS, MINUS),
        [("$2,000 at 6%% compounded monthly for 5 years.", ["2,000(1 + 0.06/12)<sup>60</sup>"], "$2,697.70"),
         ("$2,000 at 6%% compounded continuously for 5 years.", ["2,000<i>e</i><sup>0.3</sup>"], "$2,699.72")],
        ["Reading the rate from the base: <i>b</i> = 0.85 is a 15%% decay, not 85%%.",
         "Forgetting to divide the rate by <i>n</i> or to multiply the time by <i>n</i>.",
         "Using 6 instead of 0.06 for 6%%.",
         "Thinking the graph crosses its asymptote. It gets close but never reaches it."])
    body = body.replace("%%", "%")
    faq = [("How can you tell if an exponential function shows growth or decay?", "Look at the base b. If b is greater than 1 it is growth; if b is between 0 and 1 it is decay."),
           ("What is the compound interest formula?", "A = P(1 + r/n)^(nt), where P is the principal, r is the annual rate as a decimal, n is the number of compounding periods per year and t is the time in years."),
           ("What is e?", "e ≈ 2.71828 is the base for continuous growth. Money compounded continuously grows as A = Pe^(rt)."),
           ("What is a half-life?", "The time it takes for a quantity to fall to half its amount. After n half-lives, (1/2)^n of the original amount is left.")]
    make("exponential-functions-and-e", 9, "F-LE.A.2",
         "Exponential Functions, Compound Interest, and e",
         "Exponential Growth and Decay Worksheet: Compound Interest and e (Algebra 2) | 100 Questions",
         "Exponential Functions and e",
         "Construct linear and exponential functions, including arithmetic and geometric sequences, given a graph, a description of a relationship, or two input-output pairs (include reading these from a table).",
         "Free Algebra 2 worksheet on exponential functions: growth and decay rates, asymptotes, compound interest, continuous growth with e and half-life. 100 questions with answers.",
         "b > 1: growth. 0 < b < 1: decay. A = P(1 + r/n)^(nt).",
         "Continuous growth uses e: A = Pe^(rt).",
         body, faq, sets, R, domain="Exponential and Logarithmic Functions", grade="algebra-2")


if __name__ == "__main__":
    build()
