# -*- coding: utf-8 -*-
"""
South Africa Grade 12 Maths (CAPS): Analytical Geometry: the Equation of a Circle and Tangents (Grade 12: Analytical geometry)
  python3 tools/gen_za_maths_g12_circles_analytical.py
The equation of a circle with any centre, centre and radius by completing the square, points on circles and the
equation of a tangent to a circle (US Geometry makers; own makers).
Wrong answers come from real mistakes: using the wrong signs for the centre, giving r² as the radius, and using the
gradient of the radius for the tangent.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_us_math_ge_equations_of_circles as usc
adopt(usc)
if isinstance(getattr(usc, 'R', None), random.Random): usc.R = random.Random(812150)
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


def pol(cs, v="x"):
    """[a, b, c, d] from the highest power."""
    n = len(cs) - 1
    out = []
    for i, c in enumerate(cs):
        p = n - i
        if c == 0:
            continue
        c = _F(c)
        if p == 0:
            body = ff(abs(c))
        else:
            body = ("" if abs(c) == 1 else ff(abs(c))) + v + ("" if p == 1 else {2: "²", 3: "³", 4: "⁴", 5: "⁵"}[p])
        if not out:
            out.append(("−" if c < 0 else "") + body)
        else:
            out.append(("− " if c < 0 else "+ ") + body)
    return " ".join(out) or "0"


def dpol(cs):
    n = len(cs) - 1
    return [c * (n - i) for i, c in enumerate(cs[:-1])]


def peval(cs, x):
    v = 0
    for c in cs:
        v = v * x + c
    return v


def lim(r, k):
    if k == "sub":
        cs = [r.choice([1, 2, -1, 3]), r.randint(-5, 5), r.randint(-6, 6)]
        a = r.randint(-3, 4)
        v = peval(cs, a)
        return mcq("Find <b>lim<sub>x→%s</sub> (%s)</b>." % (s(a), pol(cs)), s(v), wr3(s(v), [s(peval(cs, -a)), s(cs[2]), s(v + cs[0]), s(peval(dpol(cs), a))]),
                   "The function is a polynomial, so substitute x = %s: <b>%s</b>." % (s(a), s(v)))
    a = r.randint(-5, 6)
    b = r.randint(-6, 6)
    if a == 0 or a == -b:
        raise AssertionError
    # (x − a)(x + b) / (x − a)
    num = pol([1, b - a, -a * b])
    v = a + b
    return mcq("Find <b>lim<sub>x→%s</sub> <span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span></b>." % (s(a), num, shift(-a)), s(v),
               wr3(s(v), ["0", "undefined", s(a - b), s(b), s(2 * a)]),
               "Factorise: <span class='fr'><span class='fn'>(%s)(%s)</span><span class='fd'>%s</span></span> = %s for x ≠ %s. Then substitute: <b>%s</b>." % (shift(-a), shift(b), shift(-a), shift(b), s(a), s(v)))


def fp(r, k):
    if k == "step":
        a = r.choice([1, 2, 3, -1, -2, 4])
        b = r.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        cs = [a, b, r.randint(-5, 5)]
        co = lambda c: "" if c == 1 else "−" if c == -1 else ff(c)
        bh = (" + " if b > 0 else " − ") + co(abs(b)) + "h"
        right = co(a) + "h(2x + h)" + bh
        wrong = [co(a) + "h²" + bh, co(a) + "(2x + h)" + (" + " if b > 0 else " − ") + ff(abs(b)), co(2 * a) + "xh" + bh, co(a) + "h(x + h)" + bh, co(a) + "h(2x + h)"]
        return mcq("f(x) = %s. Simplify <b>f(x + h) − f(x)</b>." % pol(cs), right, wr3(right, wrong),
                   "Expand f(x + h), then subtract f(x). The x², x and constant terms of f(x) cancel: <b>%s</b>." % right)
    if k == "quad":
        a = r.choice([1, 2, 3, 4, 5, -1, -2, -3])
        b = r.randint(-6, 6)
        c = r.randint(-6, 6)
        cs = [a, b, c]
        right = "f′(x) = " + pol(dpol(cs))
        return mcq("Use first principles to find f′(x) if <b>f(x) = %s</b>." % pol(cs), right,
                   wr3(right, ["f′(x) = " + pol([a, b]), "f′(x) = " + pol([2 * a, b, c]), "f′(x) = " + pol([2 * a, 0]), "f′(x) = " + pol([a, 0])]),
                   "f′(x) = lim<sub>h→0</sub> <span class='fr'><span class='fn'>f(x + h) − f(x)</span><span class='fd'>h</span></span> = lim<sub>h→0</sub> (%s) = <b>%s</b>." % (pol([2 * a, b]) + (" + " if a > 0 else " − ") + ("" if abs(a) == 1 else ff(abs(a))) + "h", pol(dpol(cs))))
    a = r.choice([1, 2, 3, 4, 5, 6, -2, -3])
    right = "f′(x) = <span class='fr'><span class='fn'>%s</span><span class='fd'>x²</span></span>" % ff(-a)
    return mcq("Use first principles to find f′(x) if <b>f(x) = <span class='fr'><span class='fn'>%s</span><span class='fd'>x</span></span></b>." % ff(a), right,
               wr3(right, ["f′(x) = <span class='fr'><span class='fn'>%s</span><span class='fd'>x²</span></span>" % ff(a), "f′(x) = <span class='fr'><span class='fn'>%s</span><span class='fd'>x</span></span>" % ff(-a), "f′(x) = %sx" % ff(a), "f′(x) = <span class='fr'><span class='fn'>1</span><span class='fd'>%sx²</span></span>" % ff(a)]),
               "f(x + h) − f(x) = <span class='fr'><span class='fn'>%s</span><span class='fd'>x + h</span></span> − <span class='fr'><span class='fn'>%s</span><span class='fd'>x</span></span> = <span class='fr'><span class='fn'>%sh</span><span class='fd'>x(x + h)</span></span>. Divide by h and let h → 0: <b>%s</b>." % (ff(a), ff(a), ff(-a), right))


def _term(c, p):
    c = _F(c)
    if p == 0:
        return ff(c)
    sp = {1: "", 2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶", 7: "⁷", 8: "⁸", 9: "⁹"}.get(p) if isinstance(p, int) and p > 0 else "<sup>%s</sup>" % ff(p)
    co = "" if c == 1 else "−" if c == -1 else ff(c)
    return co + "x" + sp


def _sum(terms):
    out = ""
    for t in terms:
        if not out:
            out = t
        elif t.startswith("−"):
            out += " − " + t[1:]
        else:
            out += " + " + t
    return out


def diff(r, k):
    if k == "power":
        n = r.choice([2, 3, 4, 5, 6, 7])
        c = r.choice([1, 2, 3, 4, 5, -2, -3, _F(1, 2), _F(1, 3)])
        right = _term(c * n, n - 1)
        return mcq("Find <span class='fr'><span class='fn'>dy</span><span class='fd'>dx</span></span> if <b>y = %s</b>." % _term(c, n), right,
                   wr3(right, [_term(c * n, n), _term(c, n - 1), _term(c * (n - 1), n - 1), _term(c * n, n + 1)]),
                   "Multiply by the power and subtract 1 from the power: <b>%s</b>." % right)
    if k == "poly":
        cs = [r.choice([1, 2, -1, 3, -2]), r.randint(-6, 6), r.randint(-9, 9), r.randint(-9, 9)]
        right = pol(dpol(cs))
        return mcq("Find f′(x) if <b>f(x) = %s</b>." % pol(cs), right,
                   wr3(right, [pol(dpol(cs) + [0]) if cs[3] else pol([cs[0] * 3, cs[1] * 2, cs[2], 1]), pol([cs[0] * 3, cs[1], cs[2]]), pol([cs[0], cs[1], cs[2]]), pol(dpol(cs)[:2] + [cs[3]])]),
                   "Differentiate term by term; a constant has derivative 0: <b>%s</b>." % right)
    if k == "neg":
        c = r.choice([1, 2, 3, 4, 5, 6, -2, -3, -4])
        n = r.choice([1, 2, 3])
        y = "<span class='fr'><span class='fn'>%s</span><span class='fd'>x%s</span></span>" % (ff(c), {1: "", 2: "²", 3: "³"}[n])
        right = _term(-c * n, -n - 1).replace("x", "x", 1)
        right = "%s<i>x</i><sup>%d</sup>" % ("" if -c * n == 1 else "−" if -c * n == -1 else ff(-c * n), -n - 1)
        right = right.replace("<sup>-", "<sup>−")
        def ex(co, p):
            return ("%s<i>x</i><sup>%d</sup>" % ("" if co == 1 else "−" if co == -1 else ff(co), p)).replace("<sup>-", "<sup>−")
        return mcq("Find <span class='fr'><span class='fn'>dy</span><span class='fd'>dx</span></span> if <b>y = %s</b>." % y, right,
                   wr3(right, [ex(c * n, -n - 1), ex(-c * n, -n + 1) if n > 1 else ex(-c, -1), ex(-c * n, n + 1), ex(-c * n, -n), ex(c, -n - 1), ex(-c * (n + 1), -n - 1)]),
                   "Write y = %s, then differentiate: <b>%s</b>." % (ex(c, -n), right))
    if k == "root":
        c = r.choice([2, 4, 6, 3, 8])
        kind = r.choice(["sqrt", "cbrt"])
        if kind == "sqrt":
            y = "%s√x" % ff(c)
            h = "" if c == 2 else ff(_F(c, 2))
            right = "%s<i>x</i><sup>−½</sup>" % h
            wrong = ["%s<i>x</i><sup>½</sup>" % h, "%s<i>x</i><sup>−½</sup>" % ff(c), "%s<i>x</i><sup>−1</sup>" % h, "%s<i>x</i><sup>−³⁄₂</sup>" % h]
            w = "%s<i>x</i><sup>½</sup>" % ff(c)
        else:
            if c % 3:
                raise AssertionError
            y = "%s∛(x²)" % ff(c)
            right = "%s<i>x</i><sup>−⅓</sup>" % ff(_F(2 * c, 3))
            wrong = ["%s<i>x</i><sup>⅔</sup>" % ff(_F(2 * c, 3)), "%s<i>x</i><sup>−⅓</sup>" % ff(c), "%s<i>x</i><sup>−⅔</sup>" % ff(_F(2 * c, 3)), "%s<i>x</i><sup>⅓</sup>" % ff(_F(2 * c, 3))]
            w = "%s<i>x</i><sup>⅔</sup>" % ff(c)
        return mcq("Find <span class='fr'><span class='fn'>dy</span><span class='fd'>dx</span></span> if <b>y = %s</b>." % y, right, wr3(right, wrong), "Write y = %s, then differentiate: <b>%s</b>." % (w, right))
    # expand first
    p, q = r.randint(-5, 5), r.randint(-5, 5)
    if p == 0 or q == 0:
        raise AssertionError
    if r.random() < 0.5:
        cs = [1, p + q, p * q]
        right = pol(dpol(cs))
        return mcq("Find <span class='fr'><span class='fn'>d</span><span class='fd'>dx</span></span>[(%s)(%s)]." % (shift(p), shift(q)), right,
                   wr3(right, ["1", pol([1, p + q]), pol([2, p * q]), pol([2, 0])]),
                   "Expand first: %s. Then differentiate: <b>%s</b>." % (pol(cs), right))
    a = r.choice([1, 2, 3])
    cs = [a, p, q]
    right = pol([a, 0, -q]).replace("x²", "x²") if False else None
    # (a x³ + p x² + q x) / x = a x² + p x + q
    cs3 = [a, p, q, 0]
    right = pol(dpol([a, p, q]))
    return mcq("Find f′(x) if <b>f(x) = <span class='fr'><span class='fn'>%s</span><span class='fd'>x</span></span></b>." % pol(cs3), right,
               wr3(right, [pol(dpol(cs3)), pol([3 * a, 2 * p, q]), pol([a, p]), pol([2 * a, p, q])]),
               "Divide each term by x first: f(x) = %s. Then differentiate: <b>%s</b>." % (pol([a, p, q]), right))


def tang(r, k):
    a = r.choice([1, 2, -1, 3, -2])
    b = r.randint(-5, 5)
    c = r.randint(-6, 6)
    cs = [a, b, c]
    x0 = r.randint(-3, 3)
    y0 = peval(cs, x0)
    m = peval(dpol(cs), x0)
    f = "f(x) = " + pol(cs)
    if k == "grad":
        return mcq("Find the gradient of the tangent to <b>%s</b> at x = %s." % (f, s(x0)), s(m), wr3(s(m), [s(y0), s(peval(dpol(cs), -x0)), s(2 * a + b), s(m + c)]),
                   "f′(x) = %s, so f′(%s) = <b>%s</b>." % (pol(dpol(cs)), s(x0), s(m)))
    if k == "eq":
        cc = y0 - m * x0
        right = "y = " + (pol([m, cc]) if m else s(cc))
        return mcq("Find the equation of the tangent to <b>%s</b> at the point where x = %s." % (f, s(x0)), right,
                   wr3(right, ["y = " + pol([m, y0]) if m else "y = %s" % s(y0 + 1), "y = " + pol([y0, m]) if y0 else "y = %sx" % s(m), "y = " + pol([-m, y0 + m * x0]) if m else "x = %s" % s(x0), "y = " + pol([m, cc + 1]) if m else "y = %s" % s(cc - 1)]),
                   "The point is (%s; %s) and m = f′(%s) = %s. y − (%s) = %s(x − (%s)), so <b>%s</b>." % (s(x0), s(y0), s(x0), s(m), s(y0), s(m), s(x0), right))
    if k == "where":
        mt = r.randint(-8, 8)
        xs = _F(mt - b, 2 * a)
        if xs.denominator != 1:
            raise AssertionError
        xs = int(xs)
        ys = peval(cs, xs)
        right = "(%s; %s)" % (s(xs), s(ys))
        return mcq("At which point on <b>%s</b> is the gradient of the tangent equal to %s?" % (f, s(mt)), right,
                   wr3(right, ["(%s; %s)" % (s(-xs), s(peval(cs, -xs))), "(%s; %s)" % (s(mt), s(peval(cs, mt))), "(%s; %s)" % (s(xs), s(mt)), "(%s; %s)" % (s(xs + 1), s(peval(cs, xs + 1)))]),
                   "f′(x) = %s = %s gives x = %s, and f(%s) = %s: <b>%s</b>." % (pol(dpol(cs)), s(mt), s(xs), s(xs), s(ys), right))
    # parallel to a line
    mt = r.choice([-6, -4, -2, 0, 2, 4, 6])
    xs = _F(mt - b, 2 * a)
    if xs.denominator != 1:
        raise AssertionError
    xs = int(xs)
    ys = peval(cs, xs)
    cc = ys - mt * xs
    right = "y = " + (pol([mt, cc]) if mt else s(cc))
    return mcq("Find the equation of the tangent to <b>%s</b> that is parallel to the line y = %s." % (f, (pol([mt, r.choice([1, -3, 5])]) if mt else "4")), right,
               wr3(right, ["y = " + pol([mt, ys]) if mt else "y = %s" % s(ys + 1), "y = " + pol([mt, cc + 2]) if mt else "y = %s" % s(cc - 2), "y = " + pol([-mt, cc]) if mt else "x = %s" % s(xs), "y = %s" % s(cc + 5)]),
               "Parallel: f′(x) = %s, so %s = %s and x = %s. The point is (%s; %s): <b>%s</b>." % (s(mt), pol(dpol(cs)), s(mt), s(xs), s(xs), s(ys), right))


def cubic(r, k):
    # f(x) = a x³ + b x² + c x + d with f′(x) = 3a(x − p)(x − q)
    a = r.choice([1, 1, -1, 2])
    p, q = sorted(r.sample(range(-4, 5), 2))
    b = _F(-3 * a * (p + q), 2)
    c = 3 * a * p * q
    if b.denominator != 1:
        raise AssertionError
    b = int(b)
    d = r.randint(-8, 8)
    cs = [a, b, c, d]
    f = "f(x) = " + pol(cs)
    fp_, fq = peval(cs, p), peval(cs, q)
    mx, mn = ((p, fp_), (q, fq)) if a > 0 else ((q, fq), (p, fp_))
    if k == "sp":
        right = "x = %s and x = %s" % (s(p), s(q))
        return mcq("Find the x-coordinates of the stationary points of <b>%s</b>." % f, right,
                   wr3(right, ["x = %s and x = %s" % (s(-p), s(-q)), "x = %s and x = %s" % (s(p), s(-q)), "x = 0 and x = %s" % s(_F(-2 * b, 3 * a)) if b else "x = 0 only", "x = %s and x = %s" % (s(p + 1), s(q + 1))]),
                   "f′(x) = %s = %s(%s)(%s) = 0, so <b>%s</b>." % (pol(dpol(cs)), s(3 * a), shift(-p), shift(-q), right))
    if k == "max":
        right = "(%s; %s)" % (s(mx[0]), s(mx[1]))
        return mcq("Find the local maximum point of <b>%s</b>." % f, right,
                   wr3(right, ["(%s; %s)" % (s(mn[0]), s(mn[1])), "(%s; %s)" % (s(mx[1]), s(mx[0])), "(%s; %s)" % (s(mx[0]), s(d)), "(%s; %s)" % (s(-mx[0]), s(peval(cs, -mx[0])))]),
                   "f′(x) = 0 at x = %s and x = %s. f″(x) = %s is negative at x = %s, so the maximum is <b>%s</b>." % (s(p), s(q), pol(dpol(dpol(cs))), s(mx[0]), right))
    if k == "inf":
        xi = _F(-b, 3 * a)
        yi = _F(peval([_F(v) for v in cs], xi))
        right = "x = %s" % ff(xi)
        return mcq("Find the x-coordinate of the point of inflection of <b>%s</b>." % f, right,
                   wr3(right, ["x = %s" % ff(-xi), "x = %s" % ff(_F(-b, a)), "x = %s" % ff(_F(-b, 2 * a)), "x = %s" % ff(xi + 1)]),
                   "f″(x) = %s = 0 gives <b>%s</b> (halfway between the stationary points %s and %s)." % (pol(dpol(dpol(cs))), right, s(p), s(q)))
    if k == "conc":
        xi = _F(-b, 3 * a)
        right = "x &lt; %s" % ff(xi) if a < 0 else "x &gt; %s" % ff(xi)
        return mcq("For which values of x is <b>%s</b> concave up?" % f, right,
                   wr3(right, ["x &gt; %s" % ff(xi) if a < 0 else "x &lt; %s" % ff(xi), "%s &lt; x &lt; %s" % (s(p), s(q)), "x &lt; %s or x &gt; %s" % (s(p), s(q))]),
                   "Concave up means f″(x) &gt; 0: %s &gt; 0, so <b>%s</b>." % (pol(dpol(dpol(cs))), right))
    if k == "dec":
        right = ("%s &lt; x &lt; %s" % (s(p), s(q))) if a > 0 else ("x &lt; %s or x &gt; %s" % (s(p), s(q)))
        wrong = ("x &lt; %s or x &gt; %s" % (s(p), s(q))) if a > 0 else ("%s &lt; x &lt; %s" % (s(p), s(q)))
        return mcq("For which values of x is <b>%s</b> decreasing?" % f, right,
                   wr3(right, [wrong, "x &lt; %s" % ff(_F(-b, 3 * a)), "x &gt; %s" % ff(_F(-b, 3 * a)), "%s &lt; x &lt; %s" % (s(-q), s(-p))]),
                   "f is decreasing where f′(x) &lt; 0: %s(%s)(%s) &lt; 0, so <b>%s</b>." % (s(3 * a), shift(-p), shift(-q), right))
    # factor theorem roots: x³ − (r1 + r2 + r3)x² + ... with integer roots
    r1, r2, r3 = r.sample(range(-4, 5), 3)
    cs = [1, -(r1 + r2 + r3), r1 * r2 + r1 * r3 + r2 * r3, -r1 * r2 * r3]
    right = "x = %s" % ", ".join(s(v) for v in sorted((r1, r2, r3)))
    return mcq("Find the x-intercepts of <b>f(x) = %s</b>." % pol(cs), right,
               wr3(right, ["x = %s" % ", ".join(s(-v) for v in sorted((r1, r2, r3))), "x = %s" % ", ".join(s(v) for v in sorted((r1, r2, -r3))), "x = %s" % ", ".join(s(v) for v in sorted((r1, -r2, r3)))]),
               "Find a root with the factor theorem: f(%s) = 0. Then divide and factorise: (%s)(%s)(%s) = 0, so <b>%s</b>." % (s(r1), shift(-r1), shift(-r2), shift(-r3), right))


def opt(r, k):
    if k == "fence":
        L = r.choice([40, 60, 80, 100, 120, 160, 200, 240])
        if r.random() < 0.5:
            x = L / 4
            A = x * x
            return mcq("A farmer has %d m of fencing for a rectangular kraal. What is the largest area he can enclose?" % L, "%s m²" % s(A),
                       wr3("%s m²" % s(A), ["%s m²" % s(L * L / 2), "%s m²" % s(L / 4), "%s m²" % s(L * L / 8), "%s m²" % s(A / 2)]),
                       "Width x, length %d/2 − x. A = x(%s − x); A′ = %s − 2x = 0 gives x = %s. The kraal is a square: A = <b>%s m²</b>." % (L, s(L / 2), s(L / 2), s(x), s(A)))
        x = L / 4
        A = x * (L - 2 * x)
        return mcq("A rectangular garden is fenced on three sides with %d m of fencing; the fourth side is a wall. What is the largest area?" % L, "%s m²" % s(A),
                   wr3("%s m²" % s(A), ["%s m²" % s(L * L / 16), "%s m²" % s(L * L / 4), "%s m²" % s(L * L / 9), "%s m²" % s(L * L / 6)]),
                   "Let the two sides at right angles to the wall be x. A = x(%d − 2x); A′ = %d − 4x = 0, so x = %s and A = <b>%s m²</b>." % (L, L, s(x), s(A)))
    if k == "box":
        side = r.choice([12, 18, 24, 30, 36, 48, 60])
        x = side / 6
        V = x * (side - 2 * x) ** 2
        return mcq("Squares of side x cm are cut from the corners of a %d cm by %d cm sheet, and the sides are folded up to make an open box. Which value of x gives the largest volume?" % (side, side), "x = %s cm" % s(x),
                   wr3("x = %s cm" % s(x), ["x = %s cm" % s(side / 4), "x = %s cm" % s(side / 2), "x = %s cm" % s(side / 3), "x = %s cm" % s(side / 8)]),
                   "V = x(%d − 2x)². V′ = (%d − 2x)(%d − 6x) = 0, so x = %s (x = %s gives no box). The volume is %s cm³." % (side, side, side, s(x), s(side / 2), s(V)))
    if k == "profit":
        a = r.choice([1, 2, 3, 4, 5])
        b = r.choice([40, 60, 80, 100, 120, 150, 200])
        c = r.choice([200, 300, 500, 800, 1000])
        x = b / (2 * a)
        if x != int(x):
            raise AssertionError
        P = -a * x * x + b * x - c
        return mcq("A spaza shop's daily profit is P(x) = −%s + %dx − %d rand when it sells x loaves. How many loaves give the greatest profit?" % (_term(a, 2) if a != 1 else "x²", b, c), "%d" % x,
                   wr3("%d" % x, ["%d" % (b / a), "%d" % b, "%d" % (x + 10), "%d" % round(c / b)]),
                   "P′(x) = −%dx + %d = 0, so <b>x = %d</b>. The profit is then %s." % (2 * a, b, x, money(P)))
    if k == "vel":
        a = r.choice([1, 2, 3])
        b = r.choice([-12, -9, -6, 6, 9, 12, 15, 24])
        c = r.randint(1, 20)
        t = r.randint(1, 5)
        cs = [-a, 0, b, c] if r.random() < 0.3 else [a, -3 * a * 2, b, c]
        v = peval(dpol(cs), t)
        return mcq("The displacement of a particle is s(t) = %s metres after t seconds. Find its velocity at t = %d s." % (pol(cs, "t"), t), "%s m/s" % s(v),
                   wr3("%s m/s" % s(v), ["%s m/s" % s(peval(cs, t)), "%s m/s" % s(peval(dpol(dpol(cs)), t)), "%s m/s" % s(peval(cs, t) / t), "%s m/s" % s(v + b)]),
                   "v(t) = s′(t) = %s, so v(%d) = <b>%s m/s</b>." % (pol(dpol(cs), "t"), t, s(v)))
    if k == "acc":
        a = r.choice([1, 2, 3, -1])
        b = r.randint(-6, 6)
        cs = [a, b, r.randint(-9, 9), r.randint(0, 30)]
        t = r.randint(1, 4)
        acc = peval(dpol(dpol(cs)), t)
        return mcq("A body moves so that s(t) = %s metres after t seconds. Find its acceleration at t = %d s." % (pol(cs, "t"), t), "%s m/s²" % s(acc),
                   wr3("%s m/s²" % s(acc), ["%s m/s²" % s(peval(dpol(cs), t)), "%s m/s²" % s(peval(cs, t)), "%s m/s²" % s(6 * a), "%s m/s²" % s(acc + 2 * b)]),
                   "v(t) = %s and a(t) = v′(t) = %s, so a(%d) = <b>%s m/s²</b>." % (pol(dpol(cs), "t"), pol(dpol(dpol(cs)), "t"), t, s(acc)))
    # rate of change of water level / temperature
    a = r.choice([_F(1, 2), 1, 2, 3])
    b = r.choice([2, 4, 6, 8, 10])
    cs = [-a, b, r.choice([10, 15, 20, 25])]
    t = r.randint(1, 5)
    rate = peval(dpol(cs), t)
    return mcq("The temperature of a pot of water is T(t) = %s °C after t minutes. At what rate is the temperature changing when t = %d?" % (pol(cs, "t"), t), "%s °C per minute" % s(rate),
               wr3("%s °C per minute" % s(rate), ["%s °C per minute" % s(peval(cs, t)), "%s °C per minute" % s(b), "%s °C per minute" % s(peval(cs, t) / t), "%s °C per minute" % s(-rate)]),
               "T′(t) = %s, so T′(%d) = <b>%s °C per minute</b>." % (pol(dpol(cs), "t"), t, s(rate)))


def _circ(a, b, rr):
    return "(%s)² + (%s)² = %s" % (shift(-a), shift(-b, "y"), s(rr)) if (a or b) else "x² + y² = %s" % s(rr)


def circ(r, k):
    a, b = r.randint(-5, 5), r.randint(-5, 5)
    dx, dy = r.choice([(3, 4), (4, 3), (5, 12), (12, 5), (6, 8), (8, 6), (1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (1, 1)])
    dx *= r.choice([1, -1])
    dy *= r.choice([1, -1])
    x0, y0 = a + dx, b + dy
    rr = dx * dx + dy * dy
    eq = _circ(a, b, rr)
    if k == "tan":
        mr = _F(dy, dx)
        mt = -1 / mr
        c = y0 - mt * x0
        def line(m, c):
            return "y = " + (pol([m, c]) if m else ff(c))
        right = line(mt, c)
        return mcq("Find the equation of the tangent to the circle <b>%s</b> at the point (%s; %s)." % (eq, s(x0), s(y0)), right,
                   wr3(right, [line(mr, y0 - mr * x0), line(mt, b - mt * a), line(-mt, y0 + mt * x0), line(mt, c + 1)]),
                   "The radius from (%s; %s) to (%s; %s) has gradient %s. The tangent is perpendicular, so m = %s. y − (%s) = %s(x − (%s)), so <b>%s</b>." % (s(a), s(b), s(x0), s(y0), ff(mr), ff(mt), s(y0), ff(mt), s(x0), right))
    if k == "write":
        right = eq
        return mcq("A circle has centre (%s; %s) and passes through (%s; %s). Find its equation." % (s(a), s(b), s(x0), s(y0)), right,
                   wr3(right, [_circ(-a, -b, rr), _circ(a, b, int(rr ** 0.5)) if int(rr ** 0.5) ** 2 == rr else _circ(a, b, rr * 2), _circ(x0, y0, rr), _circ(a, b, abs(dx) + abs(dy))]),
                   "r² = (%s − (%s))² + (%s − (%s))² = %s. <b>%s</b>." % (s(x0), s(a), s(y0), s(b), s(rr), right))
    # completing the square
    D, E = -2 * a, -2 * b
    F = a * a + b * b - rr
    expr = "x² + y²" + (" " + sgn(D) + "x" if D else "") + (" " + sgn(E) + "y" if E else "") + (" " + sgn(F) if F else "") + " = 0"
    right = "centre (%s; %s), radius %s" % (s(a), s(b), "√%d" % rr if int(rr ** 0.5) ** 2 != rr else s(int(rr ** 0.5)))
    rad = "√%d" % rr if int(rr ** 0.5) ** 2 != rr else s(int(rr ** 0.5))
    return mcq("Find the centre and radius of the circle <b>%s</b>." % expr, right,
               wr3(right, ["centre (%s; %s), radius %s" % (s(-a), s(-b), rad), "centre (%s; %s), radius %s" % (s(a), s(b), s(rr)), "centre (%s; %s), radius %s" % (s(D), s(E), rad), "centre (%s; %s), radius %s" % (s(b), s(a), rad)]),
               "Complete the square: (%s)² + (%s)² = %s. <b>%s</b>." % (shift(-a), shift(-b, "y"), s(rr), right))


def prop(r, k):
    p, q = r.choice([(2, 3), (3, 4), (1, 2), (2, 5), (3, 5), (4, 5), (3, 2), (5, 3), (1, 3), (4, 3)])
    m = r.choice([1, 2, 3, 4])
    AD, DB = p * m, q * m
    if k == "side":
        n = r.choice([1.5, 2, 2.5, 3, 4])
        AE = p * n
        EC = q * n
        return mcq("In △ABC, D lies on AB and E lies on AC with DE ∥ BC. AD = %s cm, DB = %s cm and AE = %s cm. Find EC." % (s(AD), s(DB), s(AE)), "%s cm" % s(EC),
                   wr3("%s cm" % s(EC), ["%s cm" % s(AE * p / q), "%s cm" % s(AE + DB - AD), "%s cm" % s(AE * (p + q) / p), "%s cm" % s(DB)]),
                   "Proportionality theorem: <span class='fr'><span class='fn'>AD</span><span class='fd'>DB</span></span> = <span class='fr'><span class='fn'>AE</span><span class='fd'>EC</span></span>, so EC = %s × %s ÷ %s = <b>%s cm</b>." % (s(AE), s(DB), s(AD), s(EC)))
    if k == "ratio":
        right = "%d : %d" % (p, p + q)
        return mcq("DE ∥ BC in △ABC with AD : DB = %d : %d. Find DE : BC." % (p, q), right,
                   wr3(right, ["%d : %d" % (p, q), "%d : %d" % (q, p + q), "%d : %d" % (p * p, (p + q) ** 2), "%d : %d" % (q, p)]),
                   "△ADE ||| △ABC, so <span class='fr'><span class='fn'>DE</span><span class='fd'>BC</span></span> = <span class='fr'><span class='fn'>AD</span><span class='fd'>AB</span></span> = <span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>: <b>%s</b>." % (p, p + q, right))
    if k == "area":
        right = "%d : %d" % (p * p, (p + q) ** 2)
        return mcq("DE ∥ BC in △ABC with AD : DB = %d : %d. Find area △ADE : area △ABC." % (p, q), right,
                   wr3(right, ["%d : %d" % (p, p + q), "%d : %d" % (p * p, q * q), "%d : %d" % (p, q), "%d : %d" % (2 * p, p + q)]),
                   "The triangles are similar with ratio %d : %d, so the areas are in the ratio of the squares: <b>%s</b>." % (p, p + q, right))
    # midpoint / bisect: x from proportion
    a1 = r.choice([2, 3, 4, 5])
    x = r.choice([2, 3, 4, 5, 6])
    # AD = x, DB = a1, AE = x + 2, EC = ?
    EC = _F(a1 * (x + 2), x)
    if EC.denominator != 1:
        raise AssertionError
    return mcq("DE ∥ BC with AD = x, DB = %d, AE = x + 2 and EC = %s. Find x." % (a1, ff(EC)), "x = %d" % x,
               wr3("x = %d" % x, ["x = %d" % (x + 1), "x = %d" % (x + 2), "x = %s" % ff(EC), "x = %d" % a1 if a1 != x else "x = %d" % (x - 1)]),
               "<span class='fr'><span class='fn'>x</span><span class='fd'>%d</span></span> = <span class='fr'><span class='fn'>x + 2</span><span class='fd'>%s</span></span>. Cross-multiply and solve: <b>x = %d</b>." % (a1, ff(EC), x))


def reg(r, k):
    if k == "pred":
        a = r.choice([12.5, 20.3, 35.1, 4.2, 48.6, 8.75])
        b = r.choice([1.25, 2.4, 3.15, 0.85, -1.6, 4.5])
        x = r.choice([8, 10, 12, 15, 20, 25])
        y = a + b * x
        right = s(round(y, 2))
        what = r.choice([("hours studied", "test mark"), ("temperature (°C)", "cold drinks sold"), ("age of a car (years)", "price (R thousand)"), ("rainfall (mm)", "maize yield (bags)")])
        return mcq("The least squares regression line for %s (x) and %s (y) is <b>ŷ = %s %s x</b>. Predict y when x = %d." % (what[0], what[1], s(a), sgn(b), x), right,
                   wr3(right, [s(round(b + a * x, 2)), s(round(a * x, 2)), s(round(a - b * x, 2)), s(round(y + b, 2))]),
                   "ŷ = %s %s(%d) = <b>%s</b>." % (s(a), sgn(b), x, right))
    if k == "slope":
        b = r.choice([2.5, 3.2, -1.8, 0.75, 4.1, -2.4])
        what = r.choice([("hours of practice", "points scored"), ("km driven", "rand spent on petrol"), ("days without rain", "dam level (%)")])
        right = "y %s by about %s for each extra unit of x" % ("increases" if b > 0 else "decreases", s(abs(b)))
        return mcq("The regression line for %s (x) and %s (y) is ŷ = 12 %s x. What does the gradient tell you?" % (what[0], what[1], sgn(b)), right,
                   wr3(right, ["y %s by about %s for each extra unit of x" % ("decreases" if b > 0 else "increases", s(abs(b))), "y is %s when x = 0" % s(b), "x changes by %s for each unit of y" % s(abs(b)), "the correlation coefficient is %s" % s(b)]),
                   "b = %s is how much ŷ changes when x increases by 1: <b>%s</b>." % (s(b), right))
    rv = r.choice([0.99, 0.98, 0.93, 0.91, 0.87, 0.84, 0.76, 0.72, 0.64, 0.55, 0.43, 0.32, 0.25, 0.08, 0.12, -0.06, -0.15, -0.28, -0.35, -0.47, -0.58, -0.62, -0.74, -0.79, -0.88, -0.95, -0.97])
    strength = "very strong" if abs(rv) >= 0.9 else "strong" if abs(rv) >= 0.7 else "moderate" if abs(rv) >= 0.5 else "weak" if abs(rv) >= 0.2 else "no (or very weak)"
    right = ("%s %s correlation" % (strength, "positive" if rv > 0 else "negative")) if abs(rv) >= 0.2 else "no (or very weak) correlation"
    opts = ["very strong positive correlation", "strong positive correlation", "moderate positive correlation", "weak positive correlation", "no (or very weak) correlation",
            "weak negative correlation", "moderate negative correlation", "strong negative correlation", "very strong negative correlation"]
    near = [o for o in opts if o != right]
    i = opts.index(right)
    wrong = [opts[j] for j in (i - 1, i + 1, len(opts) - 1 - i) if 0 <= j < len(opts) and opts[j] != right]
    return mcq("The correlation coefficient of a data set is r = %s. Describe the correlation." % s(rv), right, wr3(right, wrong + near),
               "r is close to %s and %s: <b>%s</b>." % ("±1" if abs(rv) >= 0.7 else "0" if abs(rv) < 0.2 else "the middle", "positive" if rv > 0 else "negative", right))


def count(r, k):
    if k == "fact":
        n = r.choice([5, 6, 7, 8, 9, 10])
        v = _m.factorial(n)
        what = r.choice(["learners stand in a line", "books are arranged on a shelf", "runners finish a race (no ties)", "cars park in a row of bays", "photos are hung in a row"])
        return mcq("In how many different ways can %d %s?" % (n, what), comma(v), wr3(comma(v), [comma(n * n), comma(_m.factorial(n - 1)), comma(n * (n - 1)), comma(2 ** n)]),
                   "%d choices for the first, %d for the second, …: %d! = <b>%s</b>." % (n, n - 1, n, comma(v)))
    if k == "code":
        rep = r.random() < 0.5
        L = r.choice([3, 4, 5, 6])
        pool, name = r.choice([(10, "digits 0 to 9"), (26, "letters of the alphabet"), (5, "digits 1 to 5"), (8, "digits 1 to 8")])
        if not rep and L > pool:
            raise AssertionError
        v = pool ** L if rep else _m.perm(pool, L)
        return mcq("A %d-character code uses the %s. How many codes are possible if characters %s be repeated?" % (L, name, "may" if rep else "may not"), comma(v),
                   wr3(comma(v), [comma(_m.perm(pool, L)) if rep else comma(pool ** L), comma(pool * L), comma(_m.factorial(L)), comma(_m.comb(pool, L))]),
                   ("%d choices for each of the %d places: %d<sup>%d</sup>" % (pool, L, pool, L) if rep else "%d × %d × … (%d factors)" % (pool, pool - 1, L)) + " = <b>%s</b>." % comma(v))
    if k == "word":
        w = r.choice(["MATHS", "DURBAN", "SOWETO", "LIMPOPO", "KAROO", "PRETORIA", "EASTER", "BANANA", "DRAKENSBERG", "ADDO", "LETTER", "KNYSNA"])
        from collections import Counter
        cnt = Counter(w)
        v = _m.factorial(len(w))
        den = 1
        for c in cnt.values():
            den *= _m.factorial(c)
        v //= den
        rep_txt = " × ".join("%d!" % c for c in cnt.values() if c > 1)
        return mcq("How many different arrangements of the letters of the word <b>%s</b> are possible?" % w, comma(v),
                   wr3(comma(v), [comma(_m.factorial(len(w))), comma(len(w) ** 2), comma(v * 2), comma(_m.factorial(len(w) - 1))]),
                   "%d letters: %d!%s = <b>%s</b>." % (len(w), len(w), (" ÷ (" + rep_txt + ") for the repeated letters") if rep_txt else "", comma(v)))
    if k == "together":
        n = r.choice([4, 5, 6, 7, 8, 9])
        v = 2 * _m.factorial(n - 1)
        if r.random() < 0.5:
            v2 = _m.factorial(n) - v
            return mcq("%d friends, including Sipho and Ayanda, sit in a row. In how many ways can they sit if Sipho and Ayanda must <b>not</b> sit next to each other?" % n, comma(v2),
                       wr3(comma(v2), [comma(v), comma(_m.factorial(n)), comma(_m.factorial(n - 1)), comma(_m.factorial(n) - _m.factorial(n - 1))]),
                       "All arrangements − together arrangements = %d! − 2 × %d! = <b>%s</b>." % (n, n - 1, comma(v2)))
        return mcq("%d friends, including Sipho and Ayanda, sit in a row. In how many ways can they sit if Sipho and Ayanda sit next to each other?" % n, comma(v),
                   wr3(comma(v), [comma(_m.factorial(n - 1)), comma(_m.factorial(n)), comma(_m.factorial(n) - v), comma(2 * _m.factorial(n - 2))]),
                   "Treat the pair as one unit: %d! arrangements, and the pair can swap: × 2 = <b>%s</b>." % (n - 1, comma(v)))
    kind = r.choice(["first", "ends", "code", "word"])
    n = r.choice([4, 5, 6, 7, 8])
    if kind == "first":
        what = "the letters A to %s are arranged at random" % "ABCDEFGH"[n - 1]
        ev = "A is first"
        p = _F(1, n)
        why = "%d! of the %d! arrangements start with A" % (n - 1, n)
    elif kind == "ends":
        what = "%d learners line up at random" % n
        ev = "the tallest is first and the shortest is last"
        p = _F(_m.factorial(n - 2), _m.factorial(n))
        why = "%d! of the %d! arrangements have both fixed" % (n - 2, n)
    elif kind == "code":
        L = r.choice([3, 4, 5])
        d = r.choice(["even", "odd"])
        what = "a %d-digit code is made at random from the digits 1 to 9, and digits may be repeated" % L
        ev = "every digit is %s" % d
        p = _F((4 if d == "even" else 5) ** L, 9 ** L)
        why = "There are %d %s digits, so %d<sup>%d</sup> of the 9<sup>%d</sup> codes work" % (4 if d == "even" else 5, d, 4 if d == "even" else 5, L, L)
    else:
        w = r.choice(["DURBAN", "SOWETO", "KAROO", "LIMPOPO", "MATHS", "PRETORIA", "KNYSNA", "BANANA"])
        from collections import Counter
        cnt = Counter(w)
        letter = r.choice(sorted(cnt))
        what = "the letters of the word %s are arranged at random" % w
        ev = "the arrangement starts with %s" % letter
        p = _F(cnt[letter], len(w))
        why = "%d of the %d letters are %s, so the probability is %d ÷ %d" % (cnt[letter], len(w), letter, cnt[letter], len(w))
    return mcq("%s. What is the probability that %s?" % (what[0].upper() + what[1:], ev), ff(p),
               wr3(ff(p), [ff(_F(1, 2)), ff(p * 2) if p * 2 < 1 else ff(p / 2), ff(_F(1, n * n)), ff(1 - p), ff(p / 3)]),
               "%s: <b>%s</b>." % (why[0].upper() + why[1:], ff(p)))


def build():
    sets, R = build_sets([
        ("Read the centre and radius", [("collect", kp(usc.one_read), 20)]),
        ("Write the equation", [("collect", kp(usc.one_write), 10), ("collect", fk(circ, "write"), 10)]),
        ("Completing the square", [("collect", kp(usc.one_cs), 10), ("collect", fk(circ, "cs"), 10)]),
        ("Points on a circle", [("collect", kp(usc.one_pt), 20)]),
        ("Tangents to a circle", [("collect", fk(circ, "tan"), 20)]),
    ], 81215)
    finish(sets, R)
    body = lesson('<ul><li>(x − a)² + (y − b)² = r² has centre (a; b) and radius r.</li><li>From x² + y² + Dx + Ey + F = 0, complete the square for x and for y.</li><li>A tangent is perpendicular to the radius at the point of contact.</li><li>Gradient of the tangent × gradient of the radius = −1.</li></ul>',
        [example("(x − 2)² + (y + 1)² = 25", ["centre (2; −1)"], "radius 5")],
        [['The signs', '(x − 2) gives a = 2; (y + 1) gives b = −1.'], ['r or r²', 'The radius is the square root.'], ['The gradient', 'Tangent ⊥ radius.']])
    faq = [('What does CAPS Grade 12 say?', 'Use a two-dimensional Cartesian co-ordinate system to derive and apply the equation of a circle (any centre) and the equation of a tangent to a circle at a given point on the circle.'), ('What is x² + y² = r²?', 'A circle with centre at the origin.'), ('Is the point inside the circle?', 'Yes, if the distance to the centre is less than r.'), ('How many tangents through an outside point?', 'Two.')]
    make('analytical-geometry-circles', 15, 'Euclidean and Analytical Geometry', 'Grade 12: Analytical geometry',
         'Use a two-dimensional Cartesian co-ordinate system to derive and apply: the equation of a circle (any centre); the equation of a tangent to a circle at a given point on the circle.',
         'Analytical Geometry: the Equation of a Circle and Tangents', 'Equation of a Circle',
         'Free CAPS Grade 12 analytical geometry worksheets: the equation of a circle, completing the square and tangents to a circle. 100 questions with memos.',
         '(x − a)² + (y − b)² = r².', 'Tangent ⊥ radius.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
