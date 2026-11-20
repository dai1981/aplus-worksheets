# -*- coding: utf-8 -*-
"""
South Africa Grade 12 Maths (CAPS): Sigma Notation and the Sum to Infinity (Grade 12: Number patterns)
  python3 tools/gen_za_maths_g12_sigma_infinity.py
Evaluating sigma notation, the sum to infinity of a convergent geometric series, and the condition for convergence
(own makers; US Algebra 2 makers).
Wrong answers come from real mistakes: miscounting the number of terms, using S∞ when |r| ≥ 1, and using a/(1 + r).
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_us_math_a2_sequences_and_series as uss
adopt(uss)
if isinstance(getattr(uss, 'R', None), random.Random): uss.R = random.Random(812020)
za_common.GRADE = "grade-12"


import re as _re
import math as _m
from fractions import Fraction as _F
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok12(it):
    """Grade 12: no radians, sec/csc/cot, complex numbers, matrices, vectors, ln or e, nCr notation, integrals"""
    return not _re.search(r"radian|π ?/|\bπ\b|\bsec\b|\bcsc\b|\bcot\b|cosec|imaginary|complex|\bi\b(?=[ ²)+−])|matri|vector|\bln\b|\be<sup>|\be\^|integral|∫|<sub>\d+</sub>C|\d+C\d+|tan\(A|tan A tan B|exact value of tan|C\(\d|P\(\d+, ?\d|choose|imperial|\bmiles?\b|\bfeet\b|\binch", _txt(it))


def uniq(fn):
    seen = set()
    def f(r):
        it = fn(r)
        key = None
        if it:
            tmp = {"q": it["q"], "e": it.get("e", ""), "c": list(it.get("c", []))}
            za_common.localize(tmp)
            key = za_common.gb_text(tmp["q"]) + "|" + "|".join(sorted(za_common.gb_text(c) for c in tmp["c"]))
        if it is None or key in seen:
            raise AssertionError("repeat")
        seen.add(key)
        return it
    f.__name__ = fn.__name__
    return f


_KP = {}


def kp(fn):
    """Only Grade 12 items, and never the same question twice (one shared maker per function)."""
    if fn not in _KP:
        def f(r):
            it = fn(r)
            if not it or not ok12(it):
                raise AssertionError("out of scope")
            return it
        f.__name__ = fn.__name__
        _KP[fn] = uniq(f)
    return _KP[fn]


_FK = {}


def fk(fun, k):
    """One shared maker per kind, so two sets never repeat a question."""
    if (fun, k) not in _FK:
        def g(r):
            return fun(r, k)
        g.__name__ = fun.__name__ + "_" + k
        _FK[(fun, k)] = uniq(g)
    return _FK[(fun, k)]


def s(v):
    if isinstance(v, float) and abs(v - round(v)) < 1e-9:
        v = int(round(v))
    return ("%g" % v).replace("-", "−").replace(".", ",")


def ff(v):
    v = _F(v)
    sg = "−" if v < 0 else ""
    v = abs(v)
    if v.denominator == 1:
        return sg + str(v.numerator)
    return sg + fr(v.numerator, v.denominator)


def sgn(c, first=False):
    """+ 3 / − 3 for a term after the first."""
    if first:
        return s(c)
    return ("+ " if c >= 0 else "− ") + s(abs(c))


def quad(a, b, c, v="x"):
    out = []
    for co, pw in ((a, v + "²"), (b, v), (c, "")):
        if co == 0:
            continue
        t = ("" if abs(co) == 1 and pw else s(abs(co))) + pw
        if not out:
            out.append(("−" if co < 0 else "") + t)
        else:
            out.append(("+ " if co > 0 else "− ") + t)
    return " ".join(out) or "0"


def shift(p, v="x"):
    """x + 3 / x − 3"""
    return v if p == 0 else "%s %s %s" % (v, "+" if p > 0 else "−", s(abs(p)))


def wr3(right, cands):
    out = []
    for c in cands:
        if c != right and c not in out:
            out.append(c)
    if len(out) < 3:
        raise AssertionError("few wrong answers")
    return out[:3]


def money(x):
    return "R" + "{:,.2f}".format(x).replace(",", " ").replace(".", ",")


def seq12(r, k):
    if k == "asum":
        a = r.randint(-10, 15)
        d = r.choice([2, 3, 4, 5, 6, 7, -2, -3, -4])
        n = r.choice([10, 12, 15, 20, 25, 30, 40, 50])
        Sn = n * (2 * a + (n - 1) * d) // 2
        seq = "; ".join(s(a + i * d) for i in range(3)) + "; …"
        return mcq("Find the sum of the first %d terms of the arithmetic series <b>%s</b>." % (n, seq), s(Sn),
                   wr3(s(Sn), [s(n * (2 * a + n * d) // 2), s(a + (n - 1) * d), s(n * (a + (n - 1) * d)), s((n - 1) * (2 * a + (n - 2) * d) // 2)]),
                   "S<sub>n</sub> = <span class='fr'><span class='fn'>n</span><span class='fd'>2</span></span>[2a + (n − 1)d] = %d ÷ 2 × [2(%s) + %d(%s)] = <b>%s</b>." % (n, s(a), n - 1, s(d), s(Sn)))
    if k == "an":
        a = r.randint(1, 12)
        d = r.choice([2, 3, 4, 5, 6])
        n = r.choice([8, 10, 12, 15, 16, 20, 24])
        Sn = n * (2 * a + (n - 1) * d) // 2
        seq = "%s + %s + %s + …" % (s(a), s(a + d), s(a + 2 * d))
        return mcq("How many terms of <b>%s</b> must be added to give a sum of %s?" % (seq, s(Sn)), "%d" % n, wr3("%d" % n, ["%d" % (n + 1), "%d" % (n - 1), "%d" % (2 * n), "%d" % (Sn // max(a, 1))]),
                   "Solve <span class='fr'><span class='fn'>n</span><span class='fd'>2</span></span>[2(%s) + (n − 1)(%s)] = %s. This gives a quadratic in n; the positive whole-number root is <b>n = %d</b>." % (s(a), s(d), s(Sn), n))
    if k == "gsum":
        a = r.choice([1, 2, 3, 4, 5, -2, 6, 8, 16])
        q = r.choice([_F(2), _F(3), _F(-2), _F(1, 2), _F(-1, 2), _F(1, 3)])
        n = r.choice([5, 6, 7, 8, 10])
        S = lambda m: a * (q ** m - 1) / (q - 1)
        Sn = S(n)
        if Sn.denominator > 300:
            raise AssertionError
        sq = "(%s)" % ff(q) if q < 0 or q.denominator > 1 else ff(q)
        seq = "; ".join(ff(a * q ** i) for i in range(3)) + "; …"
        return mcq("Find the sum of the first %d terms of the geometric series <b>%s</b>." % (n, seq), ff(Sn),
                   wr3(ff(Sn), [ff(a * q ** (n - 1)), ff(S(n + 1)), ff(S(n - 1)), ff(a * q ** n), ff(-Sn)]),
                   "r = %s. S<sub>n</sub> = <span class='fr'><span class='fn'>a(rⁿ − 1)</span><span class='fd'>r − 1</span></span> = <span class='fr'><span class='fn'>%s(%s<sup>%d</sup> − 1)</span><span class='fd'>%s − 1</span></span> = <b>%s</b>." % (ff(q), s(a), sq, n, ff(q), ff(Sn)))
    if k == "inf":
        a = r.choice([4, 6, 8, 9, 10, 12, 18, 20, 24, 27, 36, 48, 54, 64, 81, 100])
        q = r.choice([_F(1, 2), _F(1, 3), _F(1, 4), _F(2, 3), _F(-1, 2), _F(3, 4), _F(-1, 3)])
        S = a / (1 - q)
        if S.denominator > 4:
            raise AssertionError
        terms = [a * q ** i for i in range(3)]
        seq = " + ".join(ff(x) for x in terms) + " + …"
        seq = seq.replace("+ −", "− ")
        return mcq("Find the sum to infinity of <b>%s</b>." % seq, ff(S), wr3(ff(S), [ff(a / (1 + q)), ff(a * q / (1 - q)), ff(a / q) if q else "0", ff(S * 2), ff(S + a)]),
                   "r = %s, and −1 &lt; r &lt; 1, so S<sub>∞</sub> = <span class='fr'><span class='fn'>a</span><span class='fd'>1 − r</span></span> = %s ÷ (1 − %s) = <b>%s</b>." % (ff(q), ff(a), ff(q) if q > 0 else "(%s)" % ff(q), ff(S)))
    if k == "conv":
        c = r.choice([1, 2, 3, -1, -2, -3])
        m = r.choice([1, 2, 3, 4])
        # r = (x + c)/m converges when −1 < (x + c)/m < 1
        lo, hi = -m - c, m - c
        rr = "<span class='fr'><span class='fn'>%s</span><span class='fd'>%d</span></span>" % (shift(c), m) if m > 1 else "(%s)" % shift(c)
        right = "%s &lt; x &lt; %s" % (s(lo), s(hi))
        return mcq("A geometric series has common ratio r = %s. For which values of x does the series converge?" % rr, right,
                   wr3(right, ["%s &lt; x &lt; %s" % (s(-m), s(m)), "x &lt; %s or x &gt; %s" % (s(lo), s(hi)), "%s ≤ x ≤ %s" % (s(lo), s(hi)), "%s &lt; x &lt; %s" % (s(-m + c), s(m + c))]),
                   "It converges when −1 &lt; r &lt; 1: −%d &lt; %s &lt; %d, so <b>%s</b>." % (m, shift(c), m, right))
    a = r.randint(1, 9)
    d = r.choice([2, 3, 4, 5])
    lo, hi = r.choice([(1, 10), (1, 12), (1, 15), (1, 20), (2, 10), (3, 12), (1, 8)])
    v = sum(a + d * (i - 1) for i in range(lo, hi + 1))
    expr = "%di %s" % (d, sgn(a - d)) if a - d else "%di" % d
    return mcq("Evaluate <b>Σ<sub>i=%d</sub><sup>%d</sup> (%s)</b>." % (lo, hi, expr), s(v), wr3(s(v), [s(sum(a + d * (i - 1) for i in range(lo, hi))), s(sum(a + d * (i - 1) for i in range(lo + 1, hi + 1))), s(hi * (a + d * (hi - 1))), s(v + d)]),
               "There are %d terms, from %s to %s. S = %d ÷ 2 × (%s + %s) = <b>%s</b>." % (hi - lo + 1, s(a + d * (lo - 1)), s(a + d * (hi - 1)), hi - lo + 1, s(a + d * (lo - 1)), s(a + d * (hi - 1)), s(v)))


def invf(r, k):
    if k == "lin":
        a = r.choice([2, 3, 4, 5, -2, -3, 0.5])
        q = r.choice([-6, -4, -3, -1, 1, 2, 5, 8])
        f = "f(x) = %s %s" % ((s(a) if a not in (1, -1) else "") + "x", sgn(q))
        right = "f<sup>−1</sup>(x) = <span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (shift(-q), s(a))
        wrong = ["f<sup>−1</sup>(x) = <span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (shift(q), s(a)),
                 "f<sup>−1</sup>(x) = %sx %s" % (s(a), sgn(-q)),
                 "f<sup>−1</sup>(x) = <span class='fr'><span class='fn'>1</span><span class='fd'>%s</span></span>" % (s(a) + "x " + sgn(q)),
                 "f<sup>−1</sup>(x) = <span class='fr'><span class='fn'>x</span><span class='fd'>%s</span></span> %s" % (s(a), sgn(q))]
        return mcq("Find the inverse of <b>%s</b>." % f, right, wr3(right, wrong), "Swap x and y: x = %sy %s. Make y the subject: <b>%s</b>." % (s(a), sgn(q), right))
    if k == "quad":
        a = r.choice([2, 3, 4, 5, _F(1, 2), _F(1, 3)])
        fa = ff(a) if a != 1 else ""
        neg = r.random() < 0.5
        right = "y = √(<span class='fr'><span class='fn'>x</span><span class='fd'>%s</span></span>), x ≥ 0" % ff(a) if _F(a).denominator == 1 else "y = √(%sx), x ≥ 0" % ff(1 / _F(a))
        if neg:
            right = right.replace("y = √", "y = −√")
            return mcq("f(x) = %sx² for x ≤ 0. Find f<sup>−1</sup>." % fa, right, wr3(right, [right.replace("−√", "√"), "y = −√(%sx), x ≥ 0" % ff(a), "y = <span class='fr'><span class='fn'>x²</span><span class='fd'>%s</span></span>" % ff(a), "y = −%sx²" % ff(1 / _F(a))]),
                       "Swap x and y: x = %sy², so y² = x ÷ %s. The domain of f is x ≤ 0, so the range of f<sup>−1</sup> is y ≤ 0: take the negative root, <b>%s</b>." % (fa, ff(a), right))
        wrong = ["y = √(%sx), x ≥ 0" % ff(a), "y = <span class='fr'><span class='fn'>x²</span><span class='fd'>%s</span></span>" % ff(a), "y = −√(<span class='fr'><span class='fn'>x</span><span class='fd'>%s</span></span>)" % ff(a), "y = %sx²" % ff(1 / _F(a))]
        return mcq("f(x) = %sx² for x ≥ 0. Find f<sup>−1</sup>." % fa, right, wr3(right, wrong),
                   "Swap x and y: x = %sy², so y² = x ÷ %s. Because the domain of f is x ≥ 0, take the positive root: <b>%s</b>." % (fa, ff(a), right))
    if k == "exp":
        b = r.choice([2, 3, 4, 5, 10, _F(1, 2), _F(1, 3)])
        sb = ff(b) if _F(b).denominator == 1 else "(%s)" % ff(b)
        right = "y = log<sub>%s</sub> x" % ff(b)
        return mcq("What is the inverse of <b>y = %s<sup>x</sup></b>?" % sb, right, wr3(right, ["y = log<sub>x</sub> %s" % ff(b), "y = %s<sup>−x</sup>" % sb, "y = x<sup>%s</sup>" % ff(b), "y = <span class='fr'><span class='fn'>1</span><span class='fd'>%s<sup>x</sup></span></span>" % sb]),
                   "Swap x and y: x = %s<sup>y</sup>, so <b>%s</b>." % (sb, right))
    if k == "pt":
        x, y = r.randint(-6, 6), r.randint(-6, 6)
        if x == y:
            raise AssertionError
        right = "(%s; %s)" % (s(y), s(x))
        return mcq("The point (%s; %s) lies on the graph of f. Which point lies on the graph of f<sup>−1</sup>?" % (s(x), s(y)), right, wr3(right, ["(%s; %s)" % (s(-x), s(-y)), "(%s; %s)" % (s(-y), s(-x)), "(%s; %s)" % (s(x), s(-y))]),
                   "The inverse swaps x and y (it is a reflection in y = x): <b>%s</b>." % right)
    b = r.choice([2, 3, 5, _F(1, 2), _F(1, 3)])
    inc = b > 1
    what = r.choice(["dom", "inc", "xint"])
    if what == "dom":
        return mcq("What is the domain of <b>y = log<sub>%s</sub> x</b>?" % ff(b), "x &gt; 0", ["x ≥ 0", "x ∈ ℝ", "x &lt; 0"], "You can only take the log of a positive number: <b>x &gt; 0</b>.")
    if what == "xint":
        return mcq("Where does <b>y = log<sub>%s</sub> x</b> cut the x-axis?" % ff(b), "(1; 0)", ["(0; 1)", "(0; 0)", "(%s; 0)" % ff(b)], "log<sub>b</sub> 1 = 0 for every base, so the graph passes through <b>(1; 0)</b>.")
    right = "increasing" if inc else "decreasing"
    return mcq("Is <b>y = log<sub>%s</sub> x</b> increasing or decreasing?" % ff(b), right, ["decreasing" if inc else "increasing", "constant", "increasing, then decreasing"],
               "The base is %s 1, so the graph is <b>%s</b>." % ("&gt;" if inc else "&lt;", right))


def ann(r, k):
    i_y = r.choice([6, 7, 7.5, 8, 9, 9.5, 10, 10.5, 11, 12])
    if k == "fv":
        x = r.choice([300, 500, 750, 800, 1000, 1200, 1500, 2000, 2500])
        yrs = r.choice([3, 5, 8, 10, 15, 20])
        i, n = i_y / 1200, yrs * 12
        FV = x * ((1 + i) ** n - 1) / i
        right = money(FV)
        return mcq("Thabo saves R%s at the end of every month for %d years at %s%% p.a. compounded monthly. How much will he have?" % (comma(x), yrs, s(i_y)), right,
                   wr3(right, [money(x * n), money(x * (1 + i) ** n), money(x * ((1 + i_y / 100) ** yrs - 1) / (i_y / 100)), money(x * (1 - (1 + i) ** -n) / i)]),
                   "F = <span class='fr'><span class='fn'>x[(1 + i)ⁿ − 1]</span><span class='fd'>i</span></span> with i = %s%% ÷ 12 and n = %d: <b>%s</b>." % (s(i_y), n, right))
    if k == "pv":
        x = r.choice([1500, 2000, 2500, 3500, 4200, 5000, 6000, 8000])
        yrs = r.choice([2, 3, 4, 5, 6, 10])
        i, n = i_y / 1200, yrs * 12
        PV = x * (1 - (1 + i) ** -n) / i
        right = money(PV)
        return mcq("A loan is repaid with monthly payments of R%s for %d years at %s%% p.a. compounded monthly. What was the amount borrowed?" % (comma(x), yrs, s(i_y)), right,
                   wr3(right, [money(x * n), money(x * ((1 + i) ** n - 1) / i), money(x * n / (1 + i_y / 100) ** yrs), money(x * (1 - (1 + i) ** (-n + 1)) / i)]),
                   "P = <span class='fr'><span class='fn'>x[1 − (1 + i)<sup>−n</sup>]</span><span class='fd'>i</span></span> with i = %s%% ÷ 12 and n = %d: <b>%s</b>." % (s(i_y), n, right))
    if k == "pay":
        P = r.choice([80, 120, 150, 180, 250, 350, 600, 850, 1200]) * 1000
        yrs = r.choice([3, 5, 6, 10, 20])
        what = "a car" if P < 400000 else "a house"
        i, n = i_y / 1200, yrs * 12
        x = P * i / (1 - (1 + i) ** -n)
        right = money(x)
        return mcq("Lerato takes out a loan of R%s for %s. It is repaid monthly over %d years at %s%% p.a. compounded monthly. Find the monthly payment." % (comma(P), what, yrs, s(i_y)), right,
                   wr3(right, [money(P / n), money(P * (1 + i) ** n / n), money(P * i / ((1 + i) ** n - 1)), money(P * i)]),
                   "x = <span class='fr'><span class='fn'>P × i</span><span class='fd'>1 − (1 + i)<sup>−n</sup></span></span> = <span class='fr'><span class='fn'>%s × %s</span><span class='fd'>1 − (1 + %s)<sup>−%d</sup></span></span> = <b>%s</b>." % (comma(P), s(round(i, 6)), s(round(i, 6)), n, right))
    if k == "n":
        P = r.choice([50, 80, 100, 150, 200]) * 1000
        x = r.choice([1500, 2000, 2500, 3000, 4000, 5000])
        i = i_y / 1200
        if P * i >= x:
            raise AssertionError
        n = -_m.log(1 - P * i / x) / _m.log(1 + i)
        nn = _m.ceil(n)
        right = "%d payments" % nn
        return mcq("A loan of R%s is repaid at R%s per month at %s%% p.a. compounded monthly. How many payments are needed? (The last one may be smaller.)" % (comma(P), comma(x), s(i_y)), right,
                   wr3(right, ["%d payments" % (nn - 1), "%d payments" % _m.ceil(P / x), "%d payments" % (nn + 5), "%d payments" % (nn + 1)]),
                   "Solve %s = %s[1 − (1 + i)<sup>−n</sup>] ÷ i with logs: n = %s, so <b>%s</b>." % (comma(P), comma(x), s(round(n, 2)), right))
    cost = r.choice([120, 180, 250, 300, 450, 600]) * 1000
    yrs = r.choice([4, 5, 6, 8, 10])
    infl = r.choice([5, 6, 7, 8])
    dep = r.choice([10, 12, 15, 18, 20])
    future = cost * (1 + infl / 100) ** yrs
    scrap = cost * (1 - dep / 100) ** yrs
    need = future - scrap
    i, n = i_y / 1200, yrs * 12
    x = need * i / ((1 + i) ** n - 1)
    item = r.choice(["a delivery truck", "a printing press", "a tractor", "a bakery oven", "a minibus taxi"])
    if k == "need":
        right = money(need)
        return mcq("A business buys %s for R%s. It will be replaced in %d years. Inflation is %d%% p.a. and the old one depreciates at %d%% p.a. on the reducing balance (and is sold). How much must be in the sinking fund?" % (item, comma(cost), yrs, infl, dep), right,
                   wr3(right, [money(future), money(future + scrap), money(cost - scrap), money(cost * (1 + infl / 100 * yrs) - scrap)]),
                   "New cost = %s × %s<sup>%d</sup> = %s. Scrap value = %s × %s<sup>%d</sup> = %s. Sinking fund = <b>%s</b>." % (comma(cost), s(1 + infl / 100), yrs, money(future), comma(cost), s(1 - dep / 100), yrs, money(scrap), right))
    right = money(x)
    return mcq("In %d years, a sinking fund must reach %s. Equal payments are made at the end of every month at %s%% p.a. compounded monthly. Find the monthly payment." % (yrs, money(need), s(i_y)), right,
               wr3(right, [money(need / n), money(need * i / (1 - (1 + i) ** -n)), money(need / ((1 + i) ** n)), money(need * i)]),
               "x = <span class='fr'><span class='fn'>F × i</span><span class='fd'>(1 + i)ⁿ − 1</span></span> with n = %d: <b>%s</b>." % (n, right))


def logs(r, k):
    if k == "law":
        b = r.choice([2, 3, 5, 10])
        a, c = r.sample([2, 3, 4, 5, 6, 8, 9, 12, 16, 25, 27, 32], 2)
        op = r.choice(["+", "−"])
        if op == "+":
            v = a * c
            if b ** round(_m.log(v, b)) != v:
                raise AssertionError
            e = round(_m.log(v, b))
            q = "log<sub>%d</sub> %d + log<sub>%d</sub> %d" % (b, a, b, c)
        else:
            if a % c:
                raise AssertionError
            v = a // c
            if v < 2 or b ** round(_m.log(v, b)) != v:
                raise AssertionError
            e = round(_m.log(v, b))
            q = "log<sub>%d</sub> %d − log<sub>%d</sub> %d" % (b, a, b, c)
        return mcq("Simplify without a calculator: <b>%s</b>." % q, str(e), wr3(str(e), [str(e + 1), str(e - 1) if e > 1 else "0", "log<sub>%d</sub> %d" % (b, a + c if op == "+" else a - c), str(v)]),
                   "%s = log<sub>%d</sub> %d = <b>%d</b>." % ("log(ab) = log a + log b" if op == "+" else "log(a ÷ b) = log a − log b", b, v, e))
    if k == "pow":
        b = r.choice([2, 3, 5])
        e = r.choice([2, 3, 4])
        m = r.choice([2, 3, 4, 5])
        q = "%d log<sub>%d</sub> %d" % (m, b, b ** e)
        return mcq("Simplify: <b>%s</b>." % q, str(m * e), wr3(str(m * e), [str(m + e), str(e), str(m * b ** e), str(m * e + 1)]),
                   "log<sub>%d</sub> %d = %d, so %d × %d = <b>%d</b>." % (b, b ** e, e, m, e, m * e))
    b = r.choice([2, 3, 5, 1.08, 1.12, 1.5])
    v = r.choice([7, 10, 20, 50, 100, 2.5, 3])
    x = _m.log(v) / _m.log(b)
    right = "x = %s" % ("%.2f" % x).replace(".", ",")
    return mcq("Solve for x correct to two decimal places: <b>%s<sup>x</sup> = %s</b>." % (s(b), s(v)), right,
               wr3(right, ["x = %s" % ("%.2f" % (v / b)).replace(".", ","), "x = %s" % ("%.2f" % (_m.log10(v) * b)).replace(".", ","), "x = %s" % ("%.2f" % (_m.log(b) / _m.log(v))).replace(".", ","), "x = %s" % ("%.2f" % (x + 1)).replace(".", ",")]),
               "Take the log of both sides: x = <span class='fr'><span class='fn'>log %s</span><span class='fd'>log %s</span></span> = <b>%s</b>." % (s(v), s(b), right[4:]))


def build():
    sets, R = build_sets([
        ("Sigma notation", [("collect", kp(uss.one_sig), 20)]),
        ("Evaluate sums", [("collect", fk(seq12, "sig"), 20)]),
        ("Sum to infinity", [("collect", fk(seq12, "inf"), 20)]),
        ("More sums to infinity", [("collect", kp(uss.one_inf), 20)]),
        ("When does it converge?", [("collect", fk(seq12, "conv"), 20)]),
    ], 81202)
    finish(sets, R)
    body = lesson("<ul><li>Σ<sub>i=1</sub><sup>n</sup> Tᵢ means add T₁ + T₂ + … + Tₙ.</li><li>The number of terms from i = p to i = q is q − p + 1.</li><li>A geometric series converges only if −1 &lt; r &lt; 1. Then S<sub>∞</sub> = <span class='fr'><span class='fn'>a</span><span class='fd'>1 − r</span></span>.</li><li>Find r by dividing a term by the term before it.</li></ul>",
        [example("8 + 4 + 2 + …", ["r = ½"], "S∞ = 8 ÷ ½ = 16")],
        [['Counting terms', 'From 3 to 10 there are 8 terms.'], ['|r| ≥ 1', 'Then there is no sum to infinity.'], ['1 + r', 'S∞ = a ÷ (1 − r).']])
    faq = [('What does CAPS Grade 12 say?', 'Use sigma notation, and find the sum to infinity of a convergent geometric series: S∞ = a/(1 − r) for −1 &lt; r &lt; 1.'), ('What does converge mean?', 'The sum gets closer and closer to one number.'), ('Does 1 + 2 + 4 + … converge?', 'No, r = 2.'), ('What is i in sigma notation?', 'The counter for the terms.')]
    make('sigma-notation-and-sum-to-infinity', 2, 'Algebra and Number Patterns', 'Grade 12: Number patterns',
         'Sigma notation; sum to infinity of a convergent geometric series: S∞ = a/(1 − r) for −1 &lt; r &lt; 1.',
         'Sigma Notation and the Sum to Infinity', 'Sigma Notation and Sum to Infinity',
         'Free CAPS Grade 12 worksheets: sigma notation, the sum to infinity and convergence of geometric series. 100 questions with memos.',
         'S∞ = a ÷ (1 − r).', 'Only when −1 &lt; r &lt; 1.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
