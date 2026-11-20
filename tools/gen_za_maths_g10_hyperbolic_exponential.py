# -*- coding: utf-8 -*-
"""
South Africa Grade 10 Maths (CAPS): Hyperbolic and Exponential Functions: y = a/x + q and y = abˣ + q (Grade 10: Functions)
  python3 tools/gen_za_maths_g10_hyperbolic_exponential.py
Asymptotes, domain, range, quadrants, points and equations of y = a/x + q and y = abˣ + q (own makers).
Wrong answers come from real mistakes: giving x = q as an asymptote, forgetting that b⁰ = 1, and mixing up increasing
and decreasing when b &lt; 1.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)

za_common.GRADE = "grade-10"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok10(it):
    """Grade 10: no complex numbers, logarithms, radians, sine or cosine rules, or calculus"""
    return not _re.search(r"imaginary|complex|\blog|radian|\bπ/|sine rule|cosine rule|law of (sines|cosines)|derivative|imperial|\bmiles?\b|\bfeet\b|\binch", _txt(it))


import math as _m


def uniq(fn):
    seen = set()
    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


SV = {("sin", 0): "0", ("sin", 30): "½", ("sin", 45): "√2/2", ("sin", 60): "√3/2", ("sin", 90): "1",
      ("cos", 0): "1", ("cos", 30): "√3/2", ("cos", 45): "√2/2", ("cos", 60): "½", ("cos", 90): "0",
      ("tan", 0): "0", ("tan", 30): "√3/3", ("tan", 45): "1", ("tan", 60): "√3"}
NUM = {"0": 0, "½": 0.5, "√2/2": 2 ** 0.5 / 2, "√3/2": 3 ** 0.5 / 2, "1": 1, "√3/3": 3 ** 0.5 / 3, "√3": 3 ** 0.5}



from fractions import Fraction as _F


def _ff(v):
    v = _F(v)
    sg = "−" if v < 0 else ""
    v = abs(v)
    if v.denominator == 1:
        return sg + str(v.numerator)
    return sg + fr(v.numerator, v.denominator)


RAT = {"sin 30°": _F(1, 2), "cos 60°": _F(1, 2), "tan 45°": _F(1), "sin 90°": _F(1), "cos 0°": _F(1), "sin 0°": _F(0), "cos 90°": _F(0), "tan 0°": _F(0)}
SQ = {"sin² 45°": _F(1, 2), "cos² 45°": _F(1, 2), "sin² 60°": _F(3, 4), "cos² 30°": _F(3, 4), "tan² 60°": _F(3), "tan² 30°": _F(1, 3), "sin² 30°": _F(1, 4), "cos² 60°": _F(1, 4)}
ALLT = dict(RAT, **SQ)


def _expr(r):
    t1, t2 = r.sample([k for k in ALLT if ALLT[k] != 0], 2)
    c1, c2 = r.choice([1, 2, 3, 4]), r.choice([1, 2, 3, 4])
    op = r.choice(["+", "−", "×"])
    v1, v2 = c1 * ALLT[t1], c2 * ALLT[t2]
    v = v1 + v2 if op == "+" else v1 - v2 if op == "−" else v1 * v2
    w = [v1 - v2 if op == "+" else v1 + v2, ALLT[t1] + ALLT[t2] if op != "×" else ALLT[t1] * ALLT[t2], v + 1, v1 * v2 if op != "×" else v1 + v2]
    st = lambda c, t: (str(c) if c > 1 else "") + t
    return st(c1, t1) + " " + op + " " + st(c2, t2), v, w


def one_special_k(k):
    def f(r):
        if k == "one":
            fn = r.choice(["sin", "cos", "tan"])
            a = r.choice([0, 30, 45, 60, 90] if fn != "tan" else [0, 30, 45, 60])
            right = SV[(fn, a)]
            other = "cos" if fn == "sin" else "sin"
            wr = [v for v in dict.fromkeys([SV.get((other, a)), "√3", "½", "√2/2", "1", "0", "√3/2"]) if v and v != right][:3]
            return mcq("Without a calculator, find the exact value of <b>%s %d°</b>." % (fn, a), right, wr, "From the special triangles: %s %d° = <b>%s</b>." % (fn, a, right))
        if k == "recip":
            tab = [("sin² 45°", "½"), ("cos² 45°", "½"), ("sin² 60°", "¾"), ("cos² 30°", "¾"), ("tan² 60°", "3"), ("tan² 30°", "⅓"), ("sin² 30°", "¼"), ("cos² 60°", "¼"),
                   ("cosec 30°", "2"), ("sec 60°", "2"), ("cot 45°", "1"), ("cosec 45°", "√2"), ("sec 45°", "√2"), ("cot 30°", "√3"), ("cot 60°", "√3/3"), ("sec 30°", "2√3/3"), ("cosec 60°", "2√3/3")]
            e, right = r.choice(tab)
            pool = ["½", "¾", "3", "⅓", "¼", "2", "1", "√2", "√3", "√3/3", "2√3/3", "√2/2", "√3/2"]
            wr = [x for x in pool if x != right]
            r.shuffle(wr)
            return mcq("Without a calculator, find the exact value of <b>%s</b>." % e, right, wr[:3], "Use the special triangles%s: <b>%s</b>." % (" and the reciprocal (cosec = 1/sin, sec = 1/cos, cot = 1/tan)" if e[:3] in ("cos", "sec", "cot") and "²" not in e else "", right))
        e, v, w = _expr(r)
        right = _ff(v)
        wr = [x for x in dict.fromkeys(_ff(x) for x in w) if x != right][:3]
        if len(wr) < 3:
            raise AssertionError
        return mcq("Without a calculator, evaluate <b>%s</b>." % e, right, wr, "Substitute the exact values, then work it out: <b>%s</b>." % right)
    f.__name__ = "one_special_" + k
    return uniq(f)


INV = {"sin": _m.asin, "cos": _m.acos, "tan": _m.atan}


def _d(x):
    return ("%.1f" % x).replace(".", ",") + "°"


def one_trigeq_k(k):
    def f(r):
        if k == "exact":
            fn, a, eq = r.choice([("sin", 30, "2 sin x = 1"), ("cos", 60, "2 cos x = 1"), ("tan", 45, "tan x = 1"), ("tan", 60, "tan x = √3"), ("sin", 60, "2 sin x = √3"),
                                   ("cos", 30, "2 cos x = √3"), ("cos", 45, "√2 cos x = 1"), ("sin", 45, "√2 sin x = 1"), ("tan", 30, "√3 tan x = 1"), ("tan", 60, "tan x − √3 = 0"),
                                   ("sin", 30, "4 sin x = 2"), ("cos", 60, "6 cos x − 3 = 0"), ("sin", 90, "sin x = 1"), ("cos", 0, "cos x = 1")])
            wr = [d for d in ["30°", "45°", "60°", "90°", "0°"] if d != "%d°" % a][:3]
            r.shuffle(wr)
            return mcq("Solve for x, where 0° ≤ x ≤ 90°: <b>%s</b>." % eq, "%d°" % a, wr, "Make %s x the subject, then use the special angles: <b>x = %d°</b>." % (fn, a))
        if k == "shift":
            fn, a, val = r.choice([("sin", 30, "0,5"), ("cos", 60, "0,5"), ("tan", 45, "1"), ("sin", 90, "1"), ("cos", 30, "√3/2"), ("tan", 60, "√3")])
            if r.random() < 0.5:
                b = r.choice([10, 15, 20, 5, 25])
                if a - b < 0:
                    raise AssertionError
                x = a - b
                eq = "%s(x + %d°) = %s" % (fn, b, val)
                why = "x + %d° = %d°" % (b, a)
                wr = ["%d°" % (a + b), "%d°" % a, "%d°" % (a - 2 * b if a - 2 * b > 0 else a + 2 * b)]
            else:
                if a % 2:
                    raise AssertionError
                x = a // 2
                eq = "%s 2x = %s" % (fn, val)
                why = "2x = %d°" % a
                wr = ["%d°" % a, "%d°" % (a * 2), "%d°" % (x + 15)]
            wr = [w for w in dict.fromkeys(wr) if w != "%d°" % x]
            return mcq("Solve for x, where 0° ≤ x ≤ 90°: <b>%s</b>." % eq, "%d°" % x, wr, "%s, so <b>x = %d°</b>." % (why, x))
        fn = r.choice(["sin", "cos", "tan"])
        if fn == "tan":
            p, q = r.choice([(1, 2), (3, 4), (4, 3), (5, 2), (2, 3), (7, 4), (5, 3), (3, 2)])
        else:
            p, q = r.choice([(1, 3), (2, 3), (3, 4), (1, 4), (2, 5), (3, 5), (4, 5), (5, 6), (3, 8), (5, 8), (7, 10), (3, 10), (9, 10)])
        x = _m.degrees(INV[fn](p / q))
        eq = "%d %s x = %d" % (q, fn, p)
        others = [_m.degrees(INV[g](p / q)) for g in ("sin", "cos", "tan") if g != fn]
        wr = [w for w in dict.fromkeys([_d(o) for o in others] + [_d(90 - x), _d(_m.degrees(INV[fn](q / p))) if q / p <= 1 or fn == "tan" else _d(x + 10)]) if w != _d(x)][:3]
        if len(wr) < 3:
            raise AssertionError
        return mcq("Solve for x correct to one decimal place, where 0° ≤ x ≤ 90°: <b>%s</b>." % eq, _d(x), wr,
                   "%s x = %d ÷ %d, so x = %s<sup>−1</sup>(%d ÷ %d) = <b>%s</b>." % (fn, p, q, fn, p, q, _d(x)))
    f.__name__ = "one_trigeq_" + k
    return uniq(f)


TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15)]


def one_xyr(r):
    a, b, c = r.choice(TRIPLES)
    if r.random() < 0.5:
        a, b = b, a
    sx, sy = r.choice([(1, 1), (-1, 1), (-1, -1), (1, -1)])
    x, y = sx * a, sy * b
    fn = r.choice(["sin", "cos", "tan"])
    v = {"sin": _F(y, c), "cos": _F(x, c), "tan": _F(y, x)}
    right = _ff(v[fn])
    wr = [_ff(-v[fn]), _ff({"sin": _F(x, c), "cos": _F(y, c), "tan": _F(x, y)}[fn]), _ff({"sin": _F(y, x), "cos": _F(c, x), "tan": _F(y, c)}[fn])]
    wr = [w for w in dict.fromkeys(wr) if w != right]
    if len(wr) < 3:
        raise AssertionError
    s = lambda n: ("−%d" % -n) if n < 0 else str(n)
    return mcq("P(%s; %s) is a point on the terminal arm of angle θ. Find <b>%s θ</b>." % (s(x), s(y), fn), right, wr,
               "r = √(x² + y²) = %d. %s θ = %s = <b>%s</b>." % (c, fn, {"sin": "y/r", "cos": "x/r", "tan": "y/x"}[fn], right))


RECIP = {"sin": "cosec", "cos": "sec", "tan": "cot"}


def one_recip(r):
    a, b, c = r.choice(TRIPLES[:4])
    if r.random() < 0.5:
        a, b = b, a
    given = r.choice(["sin", "cos", "tan"])
    gv = {"sin": _F(b, c), "cos": _F(a, c), "tan": _F(b, a)}
    ask = r.choice(["cosec", "sec", "cot", "sin", "cos", "tan"])
    if ask == given:
        raise AssertionError
    av = {"cosec": 1 / gv["sin"], "sec": 1 / gv["cos"], "cot": 1 / gv["tan"], "sin": gv["sin"], "cos": gv["cos"], "tan": gv["tan"]}
    right = _ff(av[ask])
    wr = [w for w in dict.fromkeys([_ff(1 / av[ask]), _ff(gv[given]), _ff(_F(c, b) if ask != "cosec" else _F(c, a)), _ff(av[ask] + 1)]) if w != right][:3]
    if len(wr) < 3:
        raise AssertionError
    return mcq("θ is an acute angle and %s θ = %s. Find <b>%s θ</b>." % (given, _ff(gv[given]), ask), right, wr,
               "Draw the triangle: the sides are %d, %d and %d (hypotenuse). %s θ = <b>%s</b>." % (a, b, c, ask, right) + (" (%s θ = 1 ÷ %s θ.)" % (ask, {v: k for k, v in RECIP.items()}[ask]) if ask in RECIP.values() else ""))


def tg(k, f=None):
    def g(r):
        return one_triggraph_k(r, k, f)
    g.__name__ = "tg_" + k
    return uniq(g)


def one_triggraph_k(r, k, fn=None):
    f = fn or r.choice(["sin", "cos"])
    a = r.choice([1, 2, 3, 4, -1, -2, -3, 0.5])
    q = r.choice([-3, -2, -1, 1, 2, 3, 4])
    s = lambda v: ("%g" % v).replace("-", "−").replace(".", ",")
    sa = {1: "", -1: "−", 0.5: "½"}.get(a, s(a))
    eq = "y = %s%s x %s %d" % (sa, f, "+" if q > 0 else "−", abs(q))
    amp = abs(a)
    mx, mn = amp + q, -amp + q
    if f == "tan":
        if k == "period":
            return mcq("What is the period of <b>%s</b>?" % eq, "180°", ["360°", "90°", "720°"], "The period of tan x is <b>180°</b>; a and q do not change it.")
        if k == "asym":
            return mcq("For 0° ≤ x ≤ 360°, where are the asymptotes of <b>%s</b>?" % eq, "x = 90° and x = 270°", ["x = 0° and x = 180°", "x = 180° only", "y = %s" % s(q)], "tan x is undefined at <b>x = 90° and x = 270°</b>.")
        x0 = r.choice([0, 45, 135, 180, 225, 315])
        tv = {0: 0, 45: 1, 135: -1, 180: 0, 225: 1, 315: -1}[x0]
        y = a * tv + q
        return mcq("Find y when x = %d° for <b>%s</b>." % (x0, eq), s(y), [s(a * tv - q), s(tv + q), s(-y if y else y + 2)], "tan %d° = %s, so y = %s × %s + (%s) = <b>%s</b>." % (x0, s(tv), s(a), s(tv), s(q), s(y)))
    if k == "max":
        return mcq("What is the maximum value of <b>%s</b>?" % eq, s(mx), [s(amp), s(mx + 1), s(mn)], "The largest value of %s x is 1, so the maximum is |a| + q = %s + (%s) = <b>%s</b>." % (f, s(amp), s(q), s(mx)))
    if k == "min":
        return mcq("What is the minimum value of <b>%s</b>?" % eq, s(mn), [s(-amp), s(mx), s(mn - 1)], "The minimum is −|a| + q = −%s + (%s) = <b>%s</b>." % (s(amp), s(q), s(mn)))
    if k == "range":
        return mcq("What is the range of <b>%s</b>?" % eq, "y ∈ [%s; %s]" % (s(mn), s(mx)), ["y ∈ [%s; %s]" % (s(-amp), s(amp)), "y ∈ [%s; %s]" % (s(q - 1), s(q + 1)), "y ∈ ℝ"],
                   "The graph goes from %s to %s: <b>y ∈ [%s; %s]</b>." % (s(mn), s(mx), s(mn), s(mx)))
    if k == "amp":
        if r.random() < 0.5:
            return mcq("What is the amplitude of <b>%s</b>?" % eq, s(amp), [s(amp * 2), s(abs(q)), s(mx)], "The amplitude is |a| = <b>%s</b>; q only moves the graph up or down." % s(amp))
        return mcq("What is the period of <b>%s</b>?" % eq, "360°", ["180°", "90°", "%s°" % s(360 * amp) if amp != 1 else "720°"], "a and q do not change the period of %s x: <b>360°</b>." % f)
    x0 = r.choice([0, 90, 180, 270, 360])
    tv = {"sin": {0: 0, 90: 1, 180: 0, 270: -1, 360: 0}, "cos": {0: 1, 90: 0, 180: -1, 270: 0, 360: 1}}[f][x0]
    y = a * tv + q
    return mcq("Find y when x = %d° for <b>%s</b>." % (x0, eq), s(y), [s(a * tv - q), s(tv + q), s(y + 2)], "%s %d° = %s, so y = %s × %s + (%s) = <b>%s</b>." % (f, x0, s(tv), s(a), s(tv), s(q), s(y)))


def _sf(v):
    return ("%g" % v).replace("-", "−").replace(".", ",")


def fk(fun, k):
    def g(r):
        return fun(r, k)
    g.__name__ = fun.__name__ + "_" + k
    return uniq(g)


def parab(r, k):
    a = r.choice([1, 2, 3, 4, -1, -2, -3, 0.5, -0.5])
    q = r.choice([-9, -8, -4, -2, -1, 1, 2, 3, 4, 5, 8])
    s = _sf
    sa = {1: "", -1: "−", 0.5: "½", -0.5: "−½"}.get(a, s(a))
    eq = "y = %sx² %s %s" % (sa, "+" if q > 0 else "−", s(abs(q)))
    if k == "tp":
        if r.random() < 0.5:
            return mcq("What is the turning point of <b>%s</b>?" % eq, "(0; %s)" % s(q), ["(%s; 0)" % s(q), "(0; %s)" % s(-q), "(0; 0)"], "y = ax² + q has its turning point at <b>(0; q) = (0; %s)</b>." % s(q))
        return mcq("Where does <b>%s</b> cut the y-axis?" % eq, "(0; %s)" % s(q), ["(%s; 0)" % s(q), "(0; %s)" % s(a), "(0; %s)" % s(a + q)], "Put x = 0: y = %s. <b>(0; %s)</b>." % (s(q), s(q)))
    if k == "range":
        right = "y ≥ %s" % s(q) if a > 0 else "y ≤ %s" % s(q)
        if r.random() < 0.5:
            sh = "a ∪ shape with a minimum" if a > 0 else "a ∩ shape with a maximum"
            return mcq("Describe the graph of <b>%s</b>." % eq, sh, ["a ∩ shape with a maximum" if a > 0 else "a ∪ shape with a minimum", "a straight line", "a hyperbola"], "a = %s is %s, so it is <b>%s</b>." % (s(a), "positive" if a > 0 else "negative", sh))
        return mcq("What is the range of <b>%s</b>?" % eq, right, ["y ≤ %s" % s(q) if a > 0 else "y ≥ %s" % s(q), "y ∈ ℝ", "x ≥ %s" % s(q)], "a %s 0, so the graph has a %s value of %s: <b>%s</b>." % ("&gt;" if a > 0 else "&lt;", "minimum" if a > 0 else "maximum", s(q), right))
    if k == "xint":
        v = -q / a
        if v <= 0:
            return mcq("How many x-intercepts does <b>%s</b> have?" % eq, "none", ["one", "two", "three"], "y = 0 gives x² = %s. A square cannot be negative, so there are <b>none</b>." % s(v))
        rt = _m.sqrt(v)
        if abs(rt - round(rt)) > 1e-9:
            raise AssertionError
        rt = int(round(rt))
        return mcq("Find the x-intercepts of <b>%s</b>." % eq, "x = ±%d" % rt, ["x = %d only" % rt, "x = ±%s" % s(v), "none"], "0 = %sx² %s %s, so x² = %s and <b>x = ±%d</b>." % (sa, "+" if q > 0 else "−", s(abs(q)), s(v), rt))
    if k == "point":
        x = r.choice([-3, -2, -1, 1, 2, 3])
        y = a * x * x + q
        return mcq("Find y when x = %s for <b>%s</b>." % (s(x), eq), s(y), [s(a * 2 * x + q), s(-(a * x * x) + q), s(a * x * x - q)], "%s × (%s)² %s %s = <b>%s</b>." % (s(a), s(x), "+" if q > 0 else "−", s(abs(q)), s(y)))
    x = r.choice([1, 2, 3, -2])
    a = r.choice([1, 2, 3, -1, -2, 4])
    y = a * x * x + q
    return mcq("y = ax² + q has its turning point at (0; %s) and passes through (%s; %s). Find a." % (s(q), s(x), s(y)), s(a), [s(y - q), s((y - q) / x) if (y - q) % x == 0 and (y - q) // x != a else s(a + 1), s(-a)],
               "q = %s. Then %s = a(%s)² + (%s), so %s = %da and <b>a = %s</b>." % (s(q), s(y), s(x), s(q), s(y - q), x * x, s(a)))


def hyp(r, k):
    a = r.choice([1, 2, 3, 4, 6, 8, 12, -1, -2, -3, -4, -6, -12])
    q = r.choice([-4, -3, -2, -1, 1, 2, 3, 5])
    s = _sf
    frac = "<span class='fr'><span class='fn'>%s</span><span class='fd'>x</span></span>" % s(a)
    eq = "y = %s %s %d" % (frac, "+" if q > 0 else "−", abs(q))
    if k == "asym":
        if r.random() < 0.6:
            return mcq("What are the asymptotes of " + eq + "?", "x = 0 and y = %s" % s(q), ["x = %s and y = 0" % s(q), "x = %s and y = %s" % (s(a), s(q)), "y = 0 only"], "For y = a/x + q, the asymptotes are x = 0 and y = q: <b>x = 0 and y = %s</b>." % s(q))
        return mcq("What is the domain of " + eq + "?", "x ∈ ℝ, x ≠ 0", ["x ∈ ℝ, x ≠ %s" % s(q), "x ∈ ℝ", "x &gt; 0"], "You cannot divide by 0, so <b>x ∈ ℝ, x ≠ 0</b>.")
    if k == "quad":
        if r.random() < 0.5:
            return mcq("What is the range of " + eq + "?", "y ∈ ℝ, y ≠ %s" % s(q), ["y ∈ ℝ, y ≠ 0", "y &gt; %s" % s(q), "y ∈ ℝ"], "The graph never touches the asymptote y = %s: <b>y ∈ ℝ, y ≠ %s</b>." % (s(q), s(q)))
        right = "first and third quadrants" if a > 0 else "second and fourth quadrants"
        return mcq("Before it is shifted by q, in which quadrants are the branches of y = %s?" % frac, right, ["second and fourth quadrants" if a > 0 else "first and third quadrants", "first and second quadrants", "only the first quadrant"],
                   "a %s 0, so the branches are in the <b>%s</b>." % ("&gt;" if a > 0 else "&lt;", right))
    if k == "point":
        x = r.choice([d for d in (1, 2, 3, 4, -1, -2, -3, -4) if a % d == 0])
        y = a // x + q
        return mcq("Find y when x = %s for " % s(x) + eq + ".", s(y), [s(a * x + q), s(a // x - q), s(a // x)], "y = %s ÷ (%s) %s %d = <b>%s</b>." % (s(a), s(x), "+" if q > 0 else "−", abs(q), s(y)))
    x = r.choice([1, 2, 3, -1, -2])
    if a % x:
        raise AssertionError
    y = a // x + q
    return mcq("y = <span class='fr'><span class='fn'>a</span><span class='fd'>x</span></span> + q has the asymptote y = %s and passes through (%s; %s). Find a." % (s(q), s(x), s(y)), s(a),
               [s(y - q), s(y * x), s(-a)] if y - q != a else [s(y * x), s(-a), s(a + q)],
               "q = %s. Then %s = a ÷ (%s) + (%s), so a ÷ (%s) = %s and <b>a = %s</b>." % (s(q), s(y), s(x), s(q), s(x), s(y - q), s(a)))


def expf(r, k):
    b = r.choice([2, 3, 0.5, 4, 5])
    a = r.choice([1, 2, 3, -1, -2])
    q = r.choice([-3, -2, -1, 1, 2, 4])
    s = _sf
    sb = {0.5: "(½)"}.get(b, str(b))
    sa = {1: "", -1: "−"}.get(a, s(a) + "·")
    eq = "y = %s%s<sup>x</sup> %s %d" % (sa, sb, "+" if q > 0 else "−", abs(q))
    if k == "asym":
        if r.random() < 0.5:
            return mcq("What is the asymptote of <b>%s</b>?" % eq, "y = %s" % s(q), ["x = %s" % s(q), "y = 0", "y = %s" % s(a + q)], "For y = a·bˣ + q the horizontal asymptote is <b>y = %s</b>." % s(q))
        right = "y &gt; %s" % s(q) if a > 0 else "y &lt; %s" % s(q)
        return mcq("What is the range of <b>%s</b>?" % eq, right, ["y &lt; %s" % s(q) if a > 0 else "y &gt; %s" % s(q), "y ∈ ℝ", "y &gt; 0"], "The graph never reaches the asymptote y = %s: <b>%s</b>." % (s(q), right))
    if k == "yint":
        return mcq("Where does <b>%s</b> cut the y-axis?" % eq, "(0; %s)" % s(a + q), ["(0; %s)" % s(q), "(0; %s)" % s(a), "(0; %s)" % s(a * b + q)], "x = 0: b⁰ = 1, so y = %s + (%s) = <b>%s</b>." % (s(a), s(q), s(a + q)))
    if k == "inc":
        inc = (b > 1) == (a > 0)
        return mcq("Is <b>%s</b> increasing or decreasing?" % eq, "increasing" if inc else "decreasing", ["decreasing" if inc else "increasing", "constant", "increasing, then decreasing"],
                   "b %s 1 and a %s 0, so the graph is <b>%s</b>." % ("&gt;" if b > 1 else "&lt;", "&gt;" if a > 0 else "&lt;", "increasing" if inc else "decreasing"))
    if k == "point":
        x = r.choice([1, 2, 3, -1])
        y = a * b ** x + q
        return mcq("Find y when x = %d for <b>%s</b>." % (x, eq), s(y), [s(a * b * x + q), s(a * b ** x), s(y + 1)], "%s × %s<sup>%s</sup> %s %d = <b>%s</b>." % (s(a), sb, s(x), "+" if q > 0 else "−", abs(q), s(y)))
    b = r.choice([2, 3, 4, 5, 6])
    x = r.choice([1, 2])
    y = b ** x + q
    return mcq("y = b<sup>x</sup> + q has the asymptote y = %s and passes through (%d; %s). Find b." % (s(q), x, s(y)), str(b), [s(y), s(y - q + 1), s(b + 1) if x == 1 else s((y - q) // 2)],
               "%s = b<sup>%d</sup> + (%s), so b<sup>%d</sup> = %s and <b>b = %d</b>." % (s(y), x, s(q), x, s(y - q), b))


def one_infl(r):
    p = r.choice([12, 18, 25, 40, 65, 120, 350, 900]) * 100
    i = r.choice([4, 5, 6, 7, 8])
    n = r.choice([2, 3, 4, 5, 10])
    what = r.choice(["a fridge", "a bicycle", "a school uniform", "a laptop", "a sofa", "a washing machine", "a year of taxi fares", "a television"])
    v = p * (1 + i / 100) ** n
    m = lambda x: "R" + comma(round(x, 2)) if False else "R%s" % ("{:,.2f}".format(x).replace(",", " ").replace(".", ","))
    right = m(v)
    wr = [m(p * (1 + i * n / 100)), m(p * (1 + i / 100) ** (n - 1)), m(p * (1 - i / 100) ** n)]
    wr = [w for w in dict.fromkeys(wr) if w != right]
    return mcq("%s costs R%s today. If inflation is %d%% per year, what will it cost in %d years?" % (what[0].upper() + what[1:], comma(p), i, n), right, wr,
               "A = P(1 + i)ⁿ = %s × 1,%02d<sup>%d</sup> = <b>%s</b>." % (comma(p), i, n, right))


def one_si10(r):
    P = r.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20]) * 1000
    i = r.choice([4, 5, 6, 7.5, 8, 9, 10, 12])
    n = r.choice([2, 3, 4, 5, 6, 8])
    A = P * (1 + i / 100 * n)
    if A != int(A):
        raise AssertionError
    s = lambda v: ("%g" % v).replace(".", ",")
    if r.random() < 0.5:
        return mcq("R%s is invested at %s%% simple interest per year. After how many years will it grow to R%s?" % (comma(P), s(i), comma(int(A))), "%d years" % n, ["%d years" % (n + 1), "%d years" % (n * 2), "%d years" % (n - 1 if n > 2 else 9)],
                   "A = P(1 + in): %s = %s(1 + %s × n), so n = <b>%d years</b>." % (comma(int(A)), comma(P), s(i / 100), n))
    return mcq("R%s grows to R%s in %d years at simple interest. What is the interest rate per year?" % (comma(P), comma(int(A)), n), "%s%%" % s(i), ["%s%%" % s(i * n), "%s%%" % s(i * 2), "%s%%" % s(i + 1)],
               "Interest = R%s. i = %s ÷ (%s × %d) = <b>%s%%</b>." % (comma(int(A - P)), comma(int(A - P)), comma(P), n, s(i)))

EVENTS = [("it rains tomorrow", "it does not rain tomorrow"), ("the taxi is late", "the taxi is not late"), ("Thandi wins the race", "Thandi does not win the race"),
          ("a learner walks to school", "a learner does not walk to school"), ("the spinner lands on red", "the spinner does not land on red"),
          ("the team scores a goal", "the team does not score a goal"), ("a bulb is faulty", "a bulb is not faulty"), ("the Gautrain is full", "the Gautrain is not full")]


def _p(v):
    return ("%g" % v).replace(".", ",")


def one_mex(r):
    k = r.choice(["comp", "comp", "mex", "mexb", "check", "check2"])
    if k == "comp":
        e, ne = r.choice(EVENTS)
        p = r.choice([5, 12, 15, 2, 35, 4, 45, 6, 65, 7, 85, 9, 25, 3, 75, 8]) / (100 if r.random() < 0.5 else 10)
        if p >= 1 or p <= 0:
            raise AssertionError
        q = round(1 - p, 3)
        return mcq("The probability that %s is %s. What is the probability that %s?" % (e, _p(p), ne), _p(q), [_p(p), _p(round(q - 0.1, 3)) if q > 0.15 else _p(round(q + 0.1, 3)), "1"],
                   "These are complementary events: P(not A) = 1 − P(A) = 1 − %s = <b>%s</b>." % (_p(p), _p(q)))
    a, b = r.randint(1, 6) / 10, r.randint(1, 5) / 10
    if a + b >= 1:
        raise AssertionError
    if k == "mex":
        return mcq("A and B are mutually exclusive. P(A) = %s and P(B) = %s. Find P(A or B)." % (_p(a), _p(b)), _p(round(a + b, 2)), [_p(round(a * b, 2)), _p(round(1 - a - b, 2)), _p(round(abs(a - b), 2)) if a != b else "1"],
                   "Mutually exclusive: P(A and B) = 0, so P(A or B) = %s + %s = <b>%s</b>." % (_p(a), _p(b), _p(round(a + b, 2))))
    if k == "mexb":
        s = round(a + b, 2)
        return mcq("A and B are mutually exclusive. P(A) = %s and P(A or B) = %s. Find P(B)." % (_p(a), _p(s)), _p(b), [_p(s), _p(round(1 - s, 2)), _p(round(s + a, 2)) if s + a < 1 else _p(round(1 - a, 2))],
                   "P(A or B) = P(A) + P(B), so P(B) = %s − %s = <b>%s</b>." % (_p(s), _p(a), _p(b)))
    if k == "check":
        ab = r.choice([0, 0, round(r.randint(1, 3) / 20, 2)])
        if ab > min(a, b):
            raise AssertionError
        s = round(a + b - ab, 2)
        right = "Yes, P(A and B) = 0" if ab == 0 else "No, P(A and B) ≠ 0"
        return mcq("P(A) = %s, P(B) = %s and P(A or B) = %s. Are A and B mutually exclusive?" % (_p(a), _p(b), _p(s)), right, ["No, P(A and B) ≠ 0" if ab == 0 else "Yes, P(A and B) = 0", "Only if P(A) = P(B)", "It cannot be decided"],
                   "P(A and B) = P(A) + P(B) − P(A or B) = %s + %s − %s = %s. <b>%s</b>." % (_p(a), _p(b), _p(s), _p(ab), right))
    die = r.choice([("rolling an even number", "rolling a 5", True), ("rolling a 1", "rolling a 6", True), ("rolling a number less than 3", "rolling a 2", False),
                    ("rolling a prime number", "rolling an even number", False), ("rolling an odd number", "rolling a 4", True), ("rolling a multiple of 3", "rolling a 6", False),
                    ("rolling a number greater than 4", "rolling a 1", True), ("rolling an odd number", "rolling a prime number", False)])
    if k == "check2":
        right = "mutually exclusive" if die[2] else "not mutually exclusive"
        return mcq("A die is rolled once. Are the events “%s” and “%s” mutually exclusive?" % (die[0], die[1]), right, ["not mutually exclusive" if die[2] else "mutually exclusive", "complementary", "impossible"],
                   "%s. They are <b>%s</b>." % ("They have no outcome in common" if die[2] else "They share at least one outcome", right))


def build():
    sets, R = build_sets([
        ("Hyperbola: asymptotes and domain", [("collect", fk(hyp, "asym"), 20)]),
        ("Hyperbola: range and quadrants", [("collect", fk(hyp, "quad"), 10), ("collect", fk(hyp, "point"), 10)]),
        ("Exponential: asymptote and range", [("collect", fk(expf, "asym"), 20)]),
        ("Exponential: intercepts and shape", [("collect", fk(expf, "yint"), 8), ("collect", fk(expf, "inc"), 6), ("collect", fk(expf, "point"), 6)]),
        ("Find the equation", [("collect", fk(hyp, "find"), 10), ("collect", fk(expf, "find"), 10)]),
    ], 81014)
    finish(sets, R)
    body = lesson('<ul><li>y = a/x + q has asymptotes x = 0 and y = q. a &gt; 0: branches in quadrants 1 and 3; a &lt; 0: quadrants 2 and 4.</li><li>y = abˣ + q has the asymptote y = q and cuts the y-axis at a + q (because b⁰ = 1).</li><li>b &gt; 1 with a &gt; 0: increasing; 0 &lt; b &lt; 1 with a &gt; 0: decreasing.</li><li>Find a or b by substituting a point.</li></ul>',
        [example("y = 3/x − 2", ["asymptotes x = 0, y = −2"], "x ≠ 0, y ≠ −2")],
        [['x = q', 'The horizontal asymptote is y = q.'], ['b⁰', 'b⁰ = 1, so the y-intercept is a + q.'], ['b &lt; 1', '(½)ˣ decreases.']])
    faq = [('What does CAPS Grade 10 say?', 'Investigate the effect of a and q on y = a/x + q and y = abˣ + q (b &gt; 0, b ≠ 1), and find domain, range, intercepts and asymptotes.'), ('Does a hyperbola cross its asymptote?', 'No.'), ('Can bˣ be negative?', 'No, bˣ &gt; 0 for b &gt; 0.'), ('What does q do?', 'Moves the graph and the horizontal asymptote.')]
    make('hyperbolic-and-exponential-functions', 14, 'Functions', 'Grade 10: Functions',
         'Investigate the effect of a and q on the graphs of y = a/x + q and y = abˣ + q (b &gt; 0, b ≠ 1); find the domain, range, intercepts with the axes and asymptotes; sketch graphs and find their equations.',
         'Hyperbolic and Exponential Functions: y = a/x + q and y = abˣ + q', 'Hyperbolic and Exponential',
         'Free CAPS Grade 10 worksheets: hyperbolas y = a/x + q and exponential graphs y = abˣ + q, asymptotes, domain, range and equations. 100 questions with memos.',
         'Horizontal asymptote: y = q.', 'y-intercept of abˣ + q is a + q.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
