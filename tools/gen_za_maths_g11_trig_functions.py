# -*- coding: utf-8 -*-
"""
South Africa Grade 11 Maths (CAPS): Trigonometric Functions: the Effect of k and p (Grade 11: Trigonometry)
  python3 tools/gen_za_maths_g11_trig_functions.py
Periods of y = sin kx, cos kx and tan kx, horizontal shifts of y = sin(x + p) and cos(x + p), maximum points and
values on the graphs (own makers).
Wrong answers come from real mistakes: multiplying the period by k, moving the graph the wrong way, and evaluating
sin x instead of sin(x + p).
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)

za_common.GRADE = "grade-11"


import re as _re
import math as _m
from fractions import Fraction as _F
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok11(it):
    """Grade 11: no logarithms, radians, sec/csc/cot, complex numbers, compound or double angles, calculus"""
    return not _re.search(r"\blog|radian|π ?/|\bπ\b|\bsec\b|\bcsc\b|\bcot\b|cosec|imaginary|complex|\bi\b(?=[ ²)+−])|matri|vector|derivative|\b(sin|cos|tan) ?2[xθA]|\b(sin|cos)\((A|x) ?[+−] ?(B|y)\)|imperial|\bmiles?\b|\bfeet\b|\binch", _txt(it))


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


def kp(fn):
    """Only Grade 11 items."""
    def f(r):
        it = fn(r)
        if not it or not ok11(it):
            raise AssertionError("out of scope")
        return it
    f.__name__ = fn.__name__
    return f


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


def _lin(m, c):
    if m == 0:
        return "y = %s" % s(c)
    t = ("" if m == 1 else "−" if m == -1 else s(m)) + "x"
    return "y = " + t + ("" if c == 0 else " " + sgn(c))


def d1(x):
    return ("%.1f" % x).replace("-", "−").replace(".", ",")


def incl(r, k):
    if k == "angle":
        m = r.choice([1, -1, 2, -2, 3, -3, 0.5, -0.5, 4, -4, 1.5, -1.5, 5, -5, 0.25])
        a = _m.degrees(_m.atan(m))
        th = a if a >= 0 else 180 + a
        right = "%s°" % d1(th)
        return mcq("Find the angle of inclination of the line <b>%s</b>, correct to one decimal place." % _lin(m, r.choice([-4, -3, -1, 2, 5, 7])), right,
                   wr3(right, ["%s°" % d1(a), "%s°" % d1(90 - abs(a)), "%s°" % d1(180 - th), "%s°" % d1(th + 90)]),
                   "tan θ = m = %s. %s<b>θ = %s</b>." % (s(m), "tan<sup>−1</sup>(%s) = %s°, so θ = 180° − %s° = " % (s(m), d1(a), d1(-a)) if a < 0 else "", right))
    if k == "grad":
        th, m = r.choice([(45, "1"), (135, "−1"), (60, "√3"), (120, "−√3"), (30, "√3/3"), (150, "−√3/3"), (0, "0")])
        return mcq("A line has an angle of inclination of %d°. What is its gradient?" % th, m, wr3(m, ["1", "−1", "√3", "−√3", "√3/3", "−√3/3", "0", "½"]),
                   "m = tan %d° = <b>%s</b>." % (th, m))
    x1, y1 = r.randint(-5, 4), r.randint(-5, 5)
    dx, dy = r.choice([1, 2, 3, 4]), r.choice([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6])
    x2, y2 = x1 + dx, y1 + dy
    m = dy / dx
    a = _m.degrees(_m.atan(m))
    th = a if a >= 0 else 180 + a
    right = "%s°" % d1(th)
    return mcq("Find the angle of inclination of the line through A(%s; %s) and B(%s; %s), correct to one decimal place." % (s(x1), s(y1), s(x2), s(y2)), right,
               wr3(right, ["%s°" % d1(a), "%s°" % d1(_m.degrees(_m.atan(dx / dy)) % 180), "%s°" % d1(90 - abs(a)), "%s°" % d1(180 - th)]),
               "m = %s ÷ %s = %s. tan θ = %s, so <b>θ = %s</b>." % (s(dy), s(dx), s(round(m, 4)), s(round(m, 4)), right))


def lineq(r, k):
    if k == "pt":
        m = r.choice([1, 2, 3, -1, -2, -3, 0.5, -0.5])
        x1, y1 = r.randint(-4, 4), r.randint(-5, 5)
        c = y1 - m * x1
        right = _lin(m, c)
        return mcq("Find the equation of the line with gradient %s through (%s; %s)." % (s(m), s(x1), s(y1)), right, wr3(right, [_lin(m, y1 + m * x1), _lin(m, y1), _lin(-m, c), _lin(m, x1 - m * y1)]),
                   "y − y₁ = m(x − x₁): y − (%s) = %s(x − (%s)), so <b>%s</b>." % (s(y1), s(m), s(x1), right))
    m = r.choice([1, 2, 3, -1, -2, -3, 0.5, -0.5, 4])
    c0 = r.randint(-5, 5)
    x1, y1 = r.randint(-4, 4), r.randint(-6, 6)
    if k == "par":
        c = y1 - m * x1
        right = _lin(m, c)
        return mcq("Find the equation of the line through (%s; %s) parallel to <b>%s</b>." % (s(x1), s(y1), _lin(m, c0)), right, wr3(right, [_lin(-1 / m, y1 + x1 / m), _lin(m, c0), _lin(m, y1), _lin(-m, y1 + m * x1)]),
                   "Parallel lines have equal gradients: m = %s. y − (%s) = %s(x − (%s)), so <b>%s</b>." % (s(m), s(y1), s(m), s(x1), right))
    if m in (0.5, -0.5):
        mp = -1 / m
    else:
        mp = -1 / m
    c = y1 - mp * x1
    if abs(c * 2 - round(c * 2)) > 1e-9 or abs(mp * 2 - round(mp * 2)) > 1e-9:
        raise AssertionError
    right = _lin(mp, c)
    return mcq("Find the equation of the line through (%s; %s) perpendicular to <b>%s</b>." % (s(x1), s(y1), _lin(m, c0)), right, wr3(right, [_lin(m, y1 - m * x1), _lin(-m, y1 + m * x1), _lin(1 / m, y1 - x1 / m), _lin(mp, c0)]),
               "m₁ × m₂ = −1, so m = %s. y − (%s) = %s(x − (%s)), so <b>%s</b>." % (s(mp), s(y1), s(mp), s(x1), right))


def parab11(r, k):
    a = r.choice([1, 2, 3, -1, -2, -3, 0.5, -0.5])
    p = r.choice([-4, -3, -2, -1, 1, 2, 3, 4])
    q = r.choice([-8, -6, -4, -2, -1, 1, 2, 3, 5, 8])
    sa = {1: "", -1: "−", 0.5: "½", -0.5: "−½"}.get(a, s(a))
    eq = "y = %s(%s)² %s" % (sa, shift(p), sgn(q))
    if k == "tp":
        right = "(%s; %s)" % (s(-p), s(q))
        if r.random() < 0.5:
            return mcq("What is the turning point of <b>%s</b>?" % eq, right, wr3(right, ["(%s; %s)" % (s(p), s(q)), "(%s; %s)" % (s(q), s(-p)), "(%s; %s)" % (s(-p), s(-q))]),
                       "y = a(x + p)² + q has its turning point at (−p; q): <b>%s</b>." % right)
        return mcq("What is the axis of symmetry of <b>%s</b>?" % eq, "x = %s" % s(-p), wr3("x = %s" % s(-p), ["x = %s" % s(p), "y = %s" % s(q), "x = %s" % s(q)]),
                   "The axis of symmetry passes through the turning point: <b>x = %s</b>." % s(-p))
    if k == "range":
        right = ("y ≥ %s" if a > 0 else "y ≤ %s") % s(q)
        return mcq("What is the range of <b>%s</b>?" % eq, right, wr3(right, [("y ≤ %s" if a > 0 else "y ≥ %s") % s(q), ("y ≥ %s" if a > 0 else "y ≤ %s") % s(-p), "y ∈ ℝ", "x ≥ %s" % s(-p)]),
                   "a %s 0, so the %s value is q = %s: <b>%s</b>." % ("&gt;" if a > 0 else "&lt;", "minimum" if a > 0 else "maximum", s(q), right))
    if k == "yint":
        y = a * p * p + q
        return mcq("Where does <b>%s</b> cut the y-axis?" % eq, "(0; %s)" % s(y), wr3("(0; %s)" % s(y), ["(0; %s)" % s(q), "(0; %s)" % s(a * p + q), "(0; %s)" % s(p * p + q), "(0; %s)" % s(-a * p * p + q)]),
                   "x = 0: y = %s(%s)² %s = <b>%s</b>." % (s(a), s(p), sgn(q), s(y)))
    if k == "xint":
        v = -q / a
        if v <= 0:
            raise AssertionError
        rt = _m.sqrt(v)
        if abs(rt - round(rt)) > 1e-9:
            raise AssertionError
        rt = int(round(rt))
        x1, x2 = -p - rt, -p + rt
        right = "x = %s or x = %s" % (s(x1), s(x2))
        return mcq("Find the x-intercepts of <b>%s</b>." % eq, right, wr3(right, ["x = %s or x = %s" % (s(p - rt), s(p + rt)), "x = %s or x = %s" % (s(-rt), s(rt)), "x = %s or x = %s" % (s(-p - v), s(-p + v))]),
                   "(%s)² = %s, so %s = ±%d and <b>%s</b>." % (shift(p), s(v), shift(p), rt, right))
    if k == "std":
        a = r.choice([1, 1, 2, -1, 3])
        h = r.randint(-4, 4)
        kk = r.randint(-9, 6)
        if h == 0:
            raise AssertionError
        b, c = -2 * a * h, a * h * h + kk
        right = "(%s; %s)" % (s(h), s(kk))
        return mcq("Find the turning point of <b>y = %s</b>." % quad(a, b, c), right, wr3(right, ["(%s; %s)" % (s(-h), s(kk)), "(%s; %s)" % (s(h), s(c)), "(%s; %s)" % (s(-h), s(a * h * h + b * -h + c)), "(%s; %s)" % (s(h), s(-kk))]),
                   "x = −b ÷ 2a = %s ÷ %s = %s. Then y = %s. <b>%s</b>." % (s(-b), s(2 * a), s(h), s(kk), right))
    h, kk = r.randint(-4, 4), r.randint(-6, 6)
    a = r.choice([1, 2, 3, -1, -2, -3])
    x = h + r.choice([-2, -1, 1, 2])
    y = a * (x - h) ** 2 + kk
    return mcq("A parabola has its turning point at (%s; %s) and passes through (%s; %s). Find a in y = a(x + p)² + q." % (s(h), s(kk), s(x), s(y)), s(a), wr3(s(a), [s(-a), s(y - kk), s(a * 2), s(y)]),
               "y = a(%s)² %s. Substitute (%s; %s): %s = a(%s)² %s, so <b>a = %s</b>." % (shift(-h), sgn(kk), s(x), s(y), s(y), s(x - h), sgn(kk), s(a)))


def hyp11(r, k):
    a = r.choice([1, 2, 3, 4, 6, -1, -2, -3, -4, -6])
    p = r.choice([-3, -2, -1, 1, 2, 3])
    q = r.choice([-4, -3, -2, -1, 1, 2, 3, 5])
    frac = "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (s(a), shift(p))
    eq = "y = %s %s" % (frac, sgn(q))
    if k == "asym":
        right = "x = %s and y = %s" % (s(-p), s(q))
        return mcq("What are the asymptotes of " + eq + "?", right, wr3(right, ["x = %s and y = %s" % (s(p), s(q)), "x = %s and y = %s" % (s(q), s(-p)), "x = 0 and y = %s" % s(q)]),
                   "y = a/(x + p) + q has asymptotes x = −p and y = q: <b>%s</b>." % right)
    if k == "dom":
        if r.random() < 0.5:
            right = "x ∈ ℝ, x ≠ %s" % s(-p)
            return mcq("What is the domain of " + eq + "?", right, wr3(right, ["x ∈ ℝ, x ≠ %s" % s(p), "x ∈ ℝ, x ≠ %s" % s(q), "x ∈ ℝ"]), "x + p ≠ 0, so <b>%s</b>." % right)
        right = "y ∈ ℝ, y ≠ %s" % s(q)
        return mcq("What is the range of " + eq + "?", right, wr3(right, ["y ∈ ℝ, y ≠ %s" % s(-p), "y ∈ ℝ, y ≠ 0", "y &gt; %s" % s(q)]), "The graph never reaches y = %s: <b>%s</b>." % (s(q), right))
    if k == "yint":
        if a % p:
            raise AssertionError
        y = a // p + q
        return mcq("Where does " + eq + " cut the y-axis?", "(0; %s)" % s(y), wr3("(0; %s)" % s(y), ["(0; %s)" % s(q), "(0; %s)" % s(-a // p + q), "(0; %s)" % s(a + q), "(0; %s)" % s(a * p + q)]),
                   "x = 0: y = %s ÷ %s %s = <b>%s</b>." % (s(a), s(p), sgn(q), s(y)))
    if k == "axis":
        c1, c2 = q + p, q - p
        right = "y = x %s" % sgn(c1) if c1 else "y = x"
        other = "y = −x %s" % sgn(c2) if c2 else "y = −x"
        return mcq("The axes of symmetry of " + eq + " have gradients 1 and −1. Which is the one with gradient 1?", right, wr3(right, ["y = x %s" % sgn(q - p) if q - p else "y = x", "y = x %s" % sgn(-q - p) if q + p else "y = x", other, "y = x %s" % sgn(q)]),
                   "The axes pass through the point (%s; %s) where the asymptotes meet. y = x + c: %s = %s + c, so <b>%s</b>." % (s(-p), s(q), s(q), s(-p), right))
    x = r.choice([d - p for d in (1, 2, -1, -2, 3) if a % d == 0])
    y = a // (x + p) + q
    return mcq("y = <span class='fr'><span class='fn'>a</span><span class='fd'>%s</span></span> %s passes through (%s; %s). Find a." % (shift(p), sgn(q), s(x), s(y)), s(a), wr3(s(a), [s(-a), s((y - q) * x), s(y - q), s(a + q)]),
               "%s = a ÷ (%s) %s, so a ÷ %s = %s and <b>a = %s</b>." % (s(y), s(x + p), sgn(q), s(x + p), s(y - q), s(a)))


def expf11(r, k):
    b = r.choice([2, 3, 0.5, 4])
    a = r.choice([1, 2, 3, -1, -2])
    p = r.choice([-2, -1, 1, 2])
    q = r.choice([-4, -3, -2, -1, 1, 2, 3])
    sb = {0.5: "(½)"}.get(b, str(b))
    sa = {1: "", -1: "−"}.get(a, s(a) + "·")
    eq = "y = %s%s<sup>%s</sup> %s" % (sa, sb, shift(p), sgn(q))
    if k == "asym":
        if r.random() < 0.5:
            return mcq("What is the asymptote of <b>%s</b>?" % eq, "y = %s" % s(q), wr3("y = %s" % s(q), ["x = %s" % s(-p), "y = 0", "y = %s" % s(a + q), "x = %s" % s(p)]),
                       "p moves the graph left or right; only q moves the asymptote: <b>y = %s</b>." % s(q))
        right = ("y &gt; %s" if a > 0 else "y &lt; %s") % s(q)
        return mcq("What is the range of <b>%s</b>?" % eq, right, wr3(right, [("y &lt; %s" if a > 0 else "y &gt; %s") % s(q), "y &gt; 0", "y ∈ ℝ"]), "The graph stays %s y = %s: <b>%s</b>." % ("above" if a > 0 else "below", s(q), right))
    if k == "yint":
        y = a * b ** p + q
        return mcq("Where does <b>%s</b> cut the y-axis?" % eq, "(0; %s)" % s(y), wr3("(0; %s)" % s(y), ["(0; %s)" % s(a + q), "(0; %s)" % s(a * b ** -p + q), "(0; %s)" % s(q), "(0; %s)" % s(a * b * p + q)]),
                   "x = 0: y = %s × %s<sup>%s</sup> %s = <b>%s</b>." % (s(a), sb, s(p), sgn(q), s(y)))
    if k == "point":
        x = r.choice([-p, 1 - p, 2 - p])
        y = a * b ** (x + p) + q
        return mcq("Find y when x = %s for <b>%s</b>." % (s(x), eq), s(y), wr3(s(y), [s(a * b ** x + q), s(a * b ** (x - p) + q), s(a * b ** (x + p) - q), s(y + 1)]),
                   "x + p = %s, so y = %s × %s<sup>%s</sup> %s = <b>%s</b>." % (s(x + p), s(a), sb, s(x + p), sgn(q), s(y)))
    b = r.choice([2, 3, 4, 5])
    pp = r.choice([-2, -1, 1, 2, 3])
    y = b ** 2 + q
    x = 2 - pp
    return mcq("y = b<sup>%s</sup> %s passes through (%s; %s). Find b (b &gt; 0)." % (shift(pp), sgn(q), s(x), s(y)), str(b), wr3(str(b), [s(y), s(y - q), str(b + 1), str(b * 2)]),
               "x + p = %s, so b² %s = %s, b² = %s and <b>b = %d</b>." % (s(x + pp), sgn(q), s(y), s(y - q), b))


SINV = {"sin": {0: 0, 30: 0.5, 90: 1, 150: 0.5, 180: 0, 210: -0.5, 270: -1, 330: -0.5, 360: 0},
        "cos": {0: 1, 60: 0.5, 90: 0, 120: -0.5, 180: -1, 240: -0.5, 270: 0, 300: 0.5, 360: 1}}


def tg11(r, k):
    s = lambda v, _s=globals()["s"]: {0.5: "½", -0.5: "−½"}.get(v, _s(v))
    f = r.choice(["sin", "cos"])
    if k == "period":
        kk = r.choice([2, 3, 4, 5, 6, 0.5])
        g = r.choice([f, "tan"])
        am = r.choice(["", "", "2 ", "3 ", "½ "])
        per = (180 if g == "tan" else 360) / kk
        right = "%s°" % s(per)
        sk = {0.5: "½"}.get(kk, str(kk))
        return mcq("What is the period of <b>y = %s%s %sx</b>?" % (am, g, sk), right, wr3(right, ["%s°" % s(360 * kk), "%s°" % s((360 if g == "tan" else 180) / kk), "360°", "180°", "%s°" % s(per * 2)]),
                   "Period = %d° ÷ k = %d° ÷ %s = <b>%s</b>." % (180 if g == "tan" else 360, 180 if g == "tan" else 360, s(kk), right))
    p = r.choice([30, 45, 60, 90, -30, -45, -60, -90])
    if k == "shift":
        f = r.choice(["sin", "cos", "tan"])
    eq = "y = %s(x %s %d°)" % (f, "+" if p > 0 else "−", abs(p))
    if k == "shift":
        right = "%d° to the %s" % (abs(p), "left" if p > 0 else "right")
        return mcq("How is the graph of y = %s x moved to get <b>%s</b>?" % (f, eq), right, wr3(right, ["%d° to the %s" % (abs(p), "right" if p > 0 else "left"), "%d units %s" % (abs(p), "up" if p > 0 else "down"), "%d units %s" % (abs(p), "down" if p > 0 else "up")]),
                   "x + p with p %s 0 moves the graph <b>%s</b>." % ("&gt;" if p > 0 else "&lt;", right))
    if k == "min":
        x = (270 - p) % 360 if f == "sin" else (180 - p) % 360
        right = "x = %d°" % x
        return mcq("For x ∈ [0°; 360°], where does <b>%s</b> have its minimum?" % eq, right, wr3(right, ["x = %d°" % ((270 + p) % 360 if f == "sin" else (180 + p) % 360), "x = 270°" if f == "sin" else "x = 180°", "x = %d°" % ((x + 180) % 360), "x = %d°" % ((x + 90) % 360)]),
                   "%s has its minimum value −1 when the angle is %d°: x %s %d° = %d°, so <b>%s</b>." % (f, x + p, "+" if p > 0 else "−", abs(p), x + p, right))
    if k == "max":
        x = (90 - p) % 360 if f == "sin" else (-p) % 360
        right = "x = %d°" % x
        return mcq("For x ∈ [0°; 360°], where does <b>%s</b> have its maximum?" % eq, right, wr3(right, ["x = %d°" % ((90 + p) % 360 if f == "sin" else p % 360), "x = 90°" if f == "sin" else "x = 0°", "x = %d°" % ((x + 180) % 360), "x = %d°" % ((x + 90) % 360)]),
                   "%s has its maximum value 1 when the angle is %d°: x %s %d° = %d°, so <b>%s</b>." % (f, x + p, "+" if p > 0 else "−", abs(p), x + p, right))
    if k == "kval":
        kk = r.choice([2, 3])
        x = r.choice([d for d in (15, 30, 45, 60, 90, 120, 135) if (kk * d) in SINV[f]])
        v = SINV[f][kk * x]
        return mcq("Find y when x = %d° for <b>y = %s %dx</b>." % (x, f, kk), s(v), wr3(s(v), [s(SINV[f].get(x, 2)) if x in SINV[f] else s(round(_m.sin(_m.radians(x)) if f == "sin" else _m.cos(_m.radians(x)), 2)), s(kk * (SINV[f].get(x, 0.3))), s(-v) if v else "1", "½" if v != 0.5 else "−1"]),
                   "%dx = %d°, and %s %d° = <b>%s</b>." % (kk, kk * x, f, kk * x, s(v)))
    xs = [x for x in range(0, 361, 30) if (x + p) % 360 in SINV[f] or (x + p) in SINV[f]]
    x = r.choice(xs)
    ang = x + p
    v = SINV[f].get(ang % 360) if ang % 360 in SINV[f] else SINV[f][ang]
    return mcq("Find y when x = %d° for <b>%s</b>." % (x, eq), s(v), wr3(s(v), [s(-v) if v else "1", s(SINV[f].get(x, 0.25)) if SINV[f].get(x) is not None and SINV[f].get(x) != v else "−1" if v != -1 else "½", "%s" % s(v + 1) if v + 1 <= 1 else "½", "−½" if v != -0.5 else "½"]),
               "x %s %d° = %d°, and %s %d° = <b>%s</b>." % ("+" if p > 0 else "−", abs(p), ang, f, ang, s(v)))


RED = {("sin", "180° − θ"): "sin θ", ("sin", "180° + θ"): "−sin θ", ("sin", "360° − θ"): "−sin θ", ("sin", "−θ"): "−sin θ", ("sin", "90° − θ"): "cos θ", ("sin", "90° + θ"): "cos θ", ("sin", "360° + θ"): "sin θ",
       ("cos", "180° − θ"): "−cos θ", ("cos", "180° + θ"): "−cos θ", ("cos", "360° − θ"): "cos θ", ("cos", "−θ"): "cos θ", ("cos", "90° − θ"): "sin θ", ("cos", "90° + θ"): "−sin θ", ("cos", "360° + θ"): "cos θ",
       ("tan", "180° − θ"): "−tan θ", ("tan", "180° + θ"): "tan θ", ("tan", "360° − θ"): "−tan θ", ("tan", "−θ"): "−tan θ", ("tan", "360° + θ"): "tan θ"}
EXACT = {"sin": {120: "√3/2", 135: "√2/2", 150: "½", 210: "−½", 225: "−√2/2", 240: "−√3/2", 300: "−√3/2", 315: "−√2/2", 330: "−½"},
         "cos": {120: "−½", 135: "−√2/2", 150: "−√3/2", 210: "−√3/2", 225: "−√2/2", 240: "−½", 300: "½", 315: "√2/2", 330: "√3/2"},
         "tan": {120: "−√3", 135: "−1", 150: "−√3/3", 210: "√3/3", 225: "1", 240: "√3", 300: "−√3", 315: "−1", 330: "−√3/3"}}


def _neg(t):
    return t[1:] if t.startswith("−") else "−" + t


_ORD = {"sin θ": 0, "cos θ": 1, "tan θ": 2}


def _mul(a, b):
    sg = (a.startswith("−")) != (b.startswith("−"))
    a, b = a.lstrip("−"), b.lstrip("−")
    if a == b:
        body = a.replace(" θ", "² θ")
    else:
        x, y = sorted((a, b), key=lambda z: _ORD[z])
        body = "sin θ" if (x, y) == ("cos θ", "tan θ") else x + " · " + y
    return ("−" if sg else "") + body


def red(r, k):
    if k == "one":
        (f, t), v = r.choice(list(RED.items()))
        base = f + " θ"
        co = {"sin": "cos θ", "cos": "sin θ", "tan": "tan θ"}[f]
        return mcq("Simplify <b>%s(%s)</b>." % (f, t), v, wr3(v, [_neg(v), base if v != base else "−" + base, co if co != v.lstrip("−") else _neg(co), _neg(co)] + ([_neg(base), "sin θ", "−cos θ"] if f == "tan" else [base, _neg(base), _neg(co), co])),
                   "Use the reduction formula (CAST): <b>%s(%s) = %s</b>." % (f, t, v))
    if k == "exact":
        f = r.choice(["sin", "cos", "tan"])
        a = r.choice(list(EXACT[f]))
        v = EXACT[f][a]
        ref = {120: 60, 135: 45, 150: 30, 210: 30, 225: 45, 240: 60, 300: 60, 315: 45, 330: 30}[a]
        pool = ["√3", "1", "√3/3", "−√3", "−1", "−√3/3"] if f == "tan" else ["½", "√3/2", "√2/2", "−½", "−√3/2", "−√2/2"]
        return mcq("Without a calculator, find <b>%s %d°</b>." % (f, a), v, wr3(v, [_neg(v), EXACT["cos" if f == "sin" else "sin"][a], _neg(EXACT["cos" if f == "sin" else "sin"][a])] + pool),
                   "The reference angle is %d°, and %d° is in quadrant %d. %s %d° = <b>%s</b>." % (ref, a, 2 if a < 180 else 3 if a < 270 else 4, f, a, v))
    if k == "quad":
        sp, cp = r.choice([(1, 1), (1, -1), (-1, -1), (-1, 1)])
        quadn = {(1, 1): 1, (1, -1): 2, (-1, -1): 3, (-1, 1): 4}[(sp, cp)]
        tp = sp * cp
        what = r.choice(["cos", "tan"])
        right = "quadrant %d" % quadn
        cond = "sin θ %s 0 and %s θ %s 0" % ("&gt;" if sp > 0 else "&lt;", what, "&gt;" if (cp if what == "cos" else tp) > 0 else "&lt;")
        return mcq("In which quadrant is θ if <b>%s</b>?" % cond, right, ["quadrant %d" % q for q in (1, 2, 3, 4) if q != quadn],
                   "CAST: sin is positive in quadrants 1 and 2, cos in 1 and 4, tan in 1 and 3. Both conditions hold in <b>%s</b>." % right)
    keys = list(RED)
    (f1, t1), (f2, t2) = r.sample(keys, 2)
    v = _mul(RED[(f1, t1)], RED[(f2, t2)])
    wrong = [_neg(v), _mul(f1 + " θ", f2 + " θ") if _mul(f1 + " θ", f2 + " θ") != v else _neg(_mul(f1 + " θ", f2 + " θ")), _mul(RED[(f1, t1)], _neg(RED[(f2, t2)]).replace("sin", "Q").replace("cos", "sin").replace("Q", "cos"))]
    return mcq("Simplify <b>%s(%s) · %s(%s)</b>." % (f1, t1, f2, t2), v, wr3(v, wrong + ["1", "−1"]),
               "%s(%s) = %s and %s(%s) = %s, so the product is <b>%s</b>." % (f1, t1, RED[(f1, t1)], f2, t2, RED[(f2, t2)], v))


def ident(r, k):
    items = [("1 − sin² θ", "cos² θ", ["sin² θ", "1 + cos² θ", "−cos² θ"]), ("1 − cos² θ", "sin² θ", ["cos² θ", "1 + sin² θ", "tan² θ"]),
             ("sin θ ÷ cos θ", "tan θ", ["1 ÷ tan θ", "sin² θ", "1"]), ("tan θ · cos θ", "sin θ", ["cos² θ", "tan² θ", "1"]),
             ("sin² θ + cos² θ", "1", ["0", "2", "tan² θ"]), ("(1 − sin θ)(1 + sin θ)", "cos² θ", ["1 − sin θ", "sin² θ", "1 + sin² θ"]),
             ("(1 − cos θ)(1 + cos θ)", "sin² θ", ["cos² θ", "1 − cos θ", "1"]), ("tan θ ÷ sin θ", "1 ÷ cos θ", ["cos θ", "sin θ", "tan² θ"]),
             ("sin² θ ÷ (1 − sin² θ)", "tan² θ", ["1", "sin² θ", "1 ÷ tan² θ"]), ("cos² θ − 1", "−sin² θ", ["sin² θ", "−cos² θ", "1"]),
             ("sin θ · tan θ + cos θ", "1 ÷ cos θ", ["1", "sin θ + cos θ", "tan θ"]), ("(sin θ + cos θ)² − 1", "2 sin θ cos θ", ["0", "1", "sin² θ − cos² θ"]),
             ("tan² θ · cos² θ", "sin² θ", ["cos² θ", "1", "tan² θ"]), ("1 ÷ cos² θ − 1", "tan² θ", ["sin² θ", "1", "cos² θ"]),
             ("(1 − cos² θ) ÷ sin θ", "sin θ", ["cos θ", "1", "sin² θ"]), ("cos θ ÷ tan θ", "cos² θ ÷ sin θ", ["sin θ", "cos θ", "1"]),
             ("sin⁴ θ − cos⁴ θ", "sin² θ − cos² θ", ["1", "0", "sin² θ + cos² θ"]), ("2 − 2 sin² θ", "2 cos² θ", ["2 sin² θ", "0", "2"]),
             ("3 sin² θ + 3 cos² θ", "3", ["6", "0", "3 tan² θ"]), ("tan θ − sin θ cos θ", "sin² θ tan θ", ["0", "tan θ", "cos² θ"])]
    e, v, w = r.choice(items)
    return mcq("Simplify <b>%s</b>." % e, v, w, "Use sin² θ + cos² θ = 1 and tan θ = sin θ ÷ cos θ: <b>%s</b>." % v)


GEN = [("sin", "½", 30), ("sin", "√3/2", 60), ("sin", "√2/2", 45), ("sin", "−½", -30), ("sin", "−√3/2", -60), ("sin", "1", 90),
       ("cos", "½", 60), ("cos", "√3/2", 30), ("cos", "√2/2", 45), ("cos", "−½", 120), ("cos", "−√3/2", 150), ("cos", "0", 90),
       ("tan", "1", 45), ("tan", "√3", 60), ("tan", "−1", -45), ("tan", "−√3", -60), ("tan", "√3/3", 30), ("tan", "−√3/3", -30)]


def _gs(f, a):
    if f == "sin":
        b = 180 - a
        if a == 90:
            return "x = 90° + k·360°, k ∈ ℤ"
        a2, b2 = a % 360, b % 360
        return "x = %d° + k·360° or x = %d° + k·360°, k ∈ ℤ" % tuple(sorted((a2, b2)))
    if f == "cos":
        return "x = ±%d° + k·360°, k ∈ ℤ" % a
    return "x = %d° + k·180°, k ∈ ℤ" % (a % 180)


def gensol(r, k):
    if k == "calc":
        f = r.choice(["sin", "cos", "tan"])
        v = r.choice([0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, -0.2, -0.3, -0.4, -0.6, -0.7, -0.8, 1.5, 2.5, -1.2, 3, -2.5, 0.42])
        if f != "tan" and abs(v) > 1:
            raise AssertionError
        a = _m.degrees({"sin": _m.asin, "cos": _m.acos, "tan": _m.atan}[f](v))
        d = lambda x: s(round(x % 360, 1))
        if f == "sin":
            right = "x = %s° + k·360° or x = %s° + k·360°, k ∈ ℤ" % tuple(sorted((d(a), d(180 - a)), key=lambda z: float(z.replace(",", ".").replace("−", "-"))))
            wrong = ["x = %s° + k·180°, k ∈ ℤ" % d(a), "x = %s° + k·360° or x = %s° + k·360°, k ∈ ℤ" % (d(a), d(180 + a)), "x = ±%s° + k·360°, k ∈ ℤ" % d(a)]
        elif f == "cos":
            right = "x = ±%s° + k·360°, k ∈ ℤ" % s(round(a, 1))
            wrong = ["x = %s° + k·360°, k ∈ ℤ" % s(round(a, 1)), "x = ±%s° + k·180°, k ∈ ℤ" % s(round(a, 1)), "x = %s° + k·360° or x = %s° + k·360°, k ∈ ℤ" % (s(round(a, 1)), d(180 - a))]
        else:
            right = "x = %s° + k·180°, k ∈ ℤ" % s(round(a % 180, 1))
            wrong = ["x = %s° + k·360°, k ∈ ℤ" % s(round(a % 180, 1)), "x = ±%s° + k·180°, k ∈ ℤ" % s(round(abs(a), 1)), "x = %s° + k·180°, k ∈ ℤ" % s(round((90 - a) % 180, 1))]
        return mcq("Find the general solution of <b>%s x = %s</b>, correct to one decimal place." % (f, s(v)), right, wr3(right, wrong),
                   "%s<sup>−1</sup>(%s) = %s°. %s" % (f, s(v), s(round(a, 1)), {"sin": "sin is also %s in the quadrant of 180° − x." % ("positive" if v > 0 else "negative"), "cos": "cos x = cos(−x).", "tan": "tan repeats every 180°."}[f]) + " <b>%s</b>" % right)
    f, v, a = r.choice(GEN)
    if k == "list":
        sols = sorted(set(x % 360 for x in ([a, 180 - a] if f == "sin" else [a, -a] if f == "cos" else [a, a + 180])))
        right = " or ".join("%d°" % x for x in sols)
        alt = sorted(set(x % 360 for x in ([a, 180 + a] if f == "sin" else [a, 180 - a] if f == "cos" else [a, 180 - a])))
        wrong = [" or ".join("%d°" % x for x in alt), "%d°" % (a % 360), " or ".join("%d°" % x for x in sorted(set(((a % 360) + 360 - 180) % 360 for _ in [0]) | {a % 360}))]
        return mcq("Solve <b>%s x = %s</b> for x ∈ [0°; 360°]." % (f, v), right, wr3(right, wrong + ["%d°" % ((a + 90) % 360)]),
                   "Reference angle %d°. %s is %s in quadrants %s: <b>%s</b>." % (abs(a) if abs(a) <= 90 else 180 - abs(a), f, "positive" if not v.startswith("−") else "negative",
                                                                                    {"sin": "1 and 2", "cos": "1 and 4", "tan": "1 and 3"}[f] if not v.startswith("−") else {"sin": "3 and 4", "cos": "2 and 3", "tan": "2 and 4"}[f], right))
    co = {"½": "1", "√3/2": "√3", "√2/2": "√2", "−½": "−1", "−√3/2": "−√3", "1": "2", "0": "0", "√3": "√3", "−1": "−1", "−√3": "−√3", "√3/3": "1", "−√3/3": "−1"}
    if k == "make":
        if f == "tan":
            eqn = {"√3/3": "3 tan x − √3 = 0", "−√3/3": "3 tan x + √3 = 0"}.get(v) or "tan x %s = 0" % ("− " + v if not v.startswith("−") else "+ " + v[1:])
        elif v == "0":
            eqn = "3 %s x = 0" % f
        else:
            c2 = co[v]
            eqn = "2 %s x %s = 0" % (f, "− " + c2 if not c2.startswith("−") else "+ " + c2[1:])
    else:
        eqn = "%s x = %s" % (f, v)
    right = _gs(f, a)
    if f == "sin":
        wrong = ["x = %d° + k·180°, k ∈ ℤ" % (a % 180), "x = ±%d° + k·360°, k ∈ ℤ" % abs(a), "x = %d° + k·360°, k ∈ ℤ" % (a % 360)]
    elif f == "cos":
        wrong = ["x = %d° + k·360°, k ∈ ℤ" % a, "x = ±%d° + k·180°, k ∈ ℤ" % a, "x = %d° + k·360° or x = %d° + k·360°, k ∈ ℤ" % (a, 180 - a)]
    else:
        wrong = ["x = %d° + k·360°, k ∈ ℤ" % (a % 180), "x = ±%d° + k·180°, k ∈ ℤ" % abs(a), "x = %d° + k·180°, k ∈ ℤ" % ((a + 90) % 180)]
    return mcq("Find the general solution of <b>%s</b>." % eqn, right, wr3(right, wrong),
               "%s x = %s, so the reference angle is %d°. <b>%s</b>" % (f, v, abs(a) if abs(a) <= 90 else 180 - abs(a), right))


def dep(r, k):
    what = r.choice(["a car", "a delivery van", "a tractor", "a laptop", "a photocopier", "a taxi", "a minibus", "a printing machine", "a fridge for a spaza shop"])
    P = r.choice([12, 15, 18, 24, 30, 45, 60, 85, 120, 250, 320, 450]) * 1000
    i = r.choice([8, 10, 12, 15, 18, 20, 25])
    n = r.choice([2, 3, 4, 5])
    money = lambda x: "R" + "{:,.2f}".format(x).replace(",", " ").replace(".", ",")
    if k == "straight":
        if i * n >= 100:
            raise AssertionError
        A = P * (1 - i / 100 * n)
        right = money(A)
        return mcq("%s costs R%s and depreciates at %d%% per year on the straight-line method. What is it worth after %d years?" % (what[0].upper() + what[1:], comma(P), i, n), right,
                   wr3(right, [money(P * (1 - i / 100) ** n), money(P * (1 + i / 100 * n)), money(P * i / 100 * n), money(P * (1 - i / 100 * (n - 1)))]),
                   "A = P(1 − in) = %s(1 − %s × %d) = <b>%s</b>." % (comma(P), s(i / 100), n, right))
    if k == "reducing":
        A = P * (1 - i / 100) ** n
        right = money(A)
        return mcq("%s costs R%s and depreciates at %d%% per year on the reducing-balance method. What is it worth after %d years?" % (what[0].upper() + what[1:], comma(P), i, n), right,
                   wr3(right, [money(P * (1 - i / 100 * n)), money(P * (1 + i / 100) ** n), money(P * (1 - i / 100) ** (n - 1)), money(P - P * (1 - i / 100) ** n)]),
                   "A = P(1 − i)ⁿ = %s × %s<sup>%d</sup> = <b>%s</b>." % (comma(P), s(1 - i / 100), n, right))
    if k == "eff":
        nom = r.choice([6, 7.5, 8, 9, 10, 11, 12, 13.5, 15, 18])
        m, word = r.choice([(12, "monthly"), (4, "quarterly"), (2, "half-yearly")])
        eff = ((1 + nom / 100 / m) ** m - 1) * 100
        right = "%s%%" % s(round(eff, 2))
        return mcq("Find the effective annual interest rate for %s%% p.a. compounded %s, correct to two decimal places." % (s(nom), word), right,
                   wr3(right, ["%s%%" % s(nom), "%s%%" % s(round(nom / m, 2)), "%s%%" % s(round(((1 + nom / 100) ** m - 1) * 100 / m, 2)), "%s%%" % s(round(eff + 0.5, 2))]),
                   "1 + i<sub>eff</sub> = (1 + %s ÷ %d)<sup>%d</sup>, so i<sub>eff</sub> = <b>%s</b>." % (s(nom / 100), m, m, right))
    nom = r.choice([6, 8, 9, 10, 12])
    m, word = r.choice([(12, "monthly"), (4, "quarterly")])
    P = r.choice([5, 8, 10, 12, 15, 20, 25, 50]) * 1000
    A = P * (1 + nom / 100 / m) ** (m * n)
    right = money(A)
    return mcq("R%s is invested at %s%% p.a. compounded %s. How much is it worth after %d years?" % (comma(P), s(nom), word, n), right,
               wr3(right, [money(P * (1 + nom / 100) ** n), money(P * (1 + nom / 100 / m) ** n), money(P * (1 + nom / 100 * n)), money(P * (1 + nom / 100 / m) ** (m * n) - P)]),
               "A = P(1 + i/m)<sup>mn</sup> = %s(1 + %s ÷ %d)<sup>%d</sup> = <b>%s</b>." % (comma(P), s(nom / 100), m, m * n, right))


def build():
    sets, R = build_sets([
        ("Period", [("collect", fk(tg11, "period"), 20)]),
        ("Horizontal shifts", [("collect", fk(tg11, "shift"), 20)]),
        ("Values of y = sin kx and cos kx", [("collect", fk(tg11, "kval"), 15), ("collect", fk(tg11, "pval"), 5)]),
        ("Values of y = sin(x + p) and cos(x + p)", [("collect", fk(tg11, "pval"), 20)]),
        ("Maximum and minimum points", [("collect", fk(tg11, "max"), 10), ("collect", fk(tg11, "min"), 10)]),
    ], 81110)
    finish(sets, R)
    body = lesson('<ul><li>k changes the period: 360° ÷ k for sin and cos, 180° ÷ k for tan.</li><li>p moves the graph sideways: x + 30° moves it 30° to the left; x − 30° moves it 30° to the right.</li><li>To find y, work out the angle first, then the ratio.</li><li>a and q still change the amplitude and move the graph up or down.</li></ul>',
        [example("y = cos(x − 60°)", ["max when x − 60° = 0°"], "x = 60°")],
        [['× k', 'The period is 360° ÷ k.'], ['The direction', '+ p moves left.'], ['The angle', 'Work out x + p first.']])
    faq = [('What does CAPS Grade 11 say?', 'Investigate the effect of k and p on y = sin kθ, cos kθ, tan kθ, sin(θ + p), cos(θ + p) and tan(θ + p), and sketch the graphs.'), ('What is the period of tan 2x?', '90°.'), ('Does p change the period?', 'No.'), ('Does k change the amplitude?', 'No.')]
    make('trigonometric-functions', 10, 'Functions', 'Grade 11: Trigonometry',
         'Investigate the effect of the parameter k on the graphs of y = sin(kx), y = cos(kx) and y = tan(kx); investigate the effect of the parameter p on the graphs of y = sin(x + p), y = cos(x + p) and y = tan(x + p); draw sketch graphs.',
         'Trigonometric Functions: the Effect of k and p', 'Trigonometric Functions',
         'Free CAPS Grade 11 worksheets: graphs of y = sin kx, cos kx, tan kx and y = sin(x + p), cos(x + p), periods, shifts and maximum points. 100 questions with memos.',
         'Period = 360° ÷ k.', 'x + p moves the graph left.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
