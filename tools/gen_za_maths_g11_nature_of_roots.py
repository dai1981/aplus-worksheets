# -*- coding: utf-8 -*-
"""
South Africa Grade 11 Maths (CAPS): The Nature of Roots and the Discriminant (Grade 11: Equations and inequalities)
  python3 tools/gen_za_maths_g11_nature_of_roots.py
The discriminant Δ = b² − 4ac, the nature of the roots, and values of k for equal, real or non-real roots (own makers;
US Algebra 1 makers).
Wrong answers come from real mistakes: using +4ac, mixing up rational and irrational roots, and using Δ &gt; 0 for equal
roots.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_us_math_a1_quadratic_formula_and_completing_the_square as usq
adopt(usq)
if isinstance(getattr(usq, 'R', None), random.Random): usq.R = random.Random(811030)
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


def nature(r, k):
    if k == "disc":
        a = r.choice([1, 2, 3, -1, -2])
        b = r.randint(-9, 9)
        c = r.randint(-8, 8)
        if b == 0 or c == 0:
            raise AssertionError
        d = b * b - 4 * a * c
        return mcq("Find the discriminant Δ of <b>%s = 0</b>." % quad(a, b, c), s(d), wr3(s(d), [s(b * b + 4 * a * c), s(-b * b - 4 * a * c), s(b - 4 * a * c), s(b * b - 2 * a * c)]),
                   "Δ = b² − 4ac = (%s)² − 4(%s)(%s) = <b>%s</b>." % (s(b), s(a), s(c), s(d)))
    if k == "nat":
        a = r.choice([1, 2, 3, -1])
        b = r.randint(-9, 9)
        c = r.randint(-9, 9)
        if c == 0:
            raise AssertionError
        d = b * b - 4 * a * c
        if d < 0:
            right = "non-real roots"
        elif d == 0:
            right = "real, equal and rational roots"
        elif int(_m.isqrt(d)) ** 2 == d:
            right = "real, unequal and rational roots"
        else:
            right = "real, unequal and irrational roots"
        opts = ["non-real roots", "real, equal and rational roots", "real, unequal and rational roots", "real, unequal and irrational roots"]
        return mcq("Describe the nature of the roots of <b>%s = 0</b>." % quad(a, b, c), right, [o for o in opts if o != right],
                   "Δ = (%s)² − 4(%s)(%s) = %s. %s" % (s(b), s(a), s(c), s(d), "Δ &lt; 0, so the roots are <b>non-real</b>." if d < 0 else "Δ = 0, so the roots are <b>real and equal</b>." if d == 0 else "Δ &gt; 0 and %s a perfect square, so the roots are <b>%s</b>." % ("is" if "rational roots" in right and "irr" not in right else "is not", right.replace(" roots", ""))))
    if k == "equal":
        t = r.choice(["b", "c"])
        if t == "b":
            m = r.choice([1, 2, 3, 4, 5, 6, 7])
            a = r.choice([1, 1, 4, 9])
            c = m * m
            kk = 2 * m * int(_m.isqrt(a))
            return mcq("For which values of k does <b>%s + kx + %d = 0</b> have equal roots?" % (quad(a, 0, 0), c), "k = ±%d" % kk, wr3("k = ±%d" % kk, ["k = %d" % kk, "k = ±%d" % (kk // 2), "k = ±%d" % (kk * kk), "k = ±%d" % c]),
                       "Equal roots: Δ = 0. k² − 4(%d)(%d) = 0, so k² = %d and <b>k = ±%d</b>." % (a, c, kk * kk, kk))
        b = r.choice([2, 4, 6, 8, 10, -4, -6])
        a = r.choice([1, 2, 1])
        if (b * b) % (4 * a):
            raise AssertionError
        kk = b * b // (4 * a)
        return mcq("For which value of k does <b>%s = 0</b> have equal roots?" % (quad(a, b, 0) + " + k"), "k = %d" % kk, wr3("k = %d" % kk, ["k = %d" % -kk, "k = %d" % (b * b), "k = %d" % (kk * 2), "k = %d" % abs(b)]),
                   "Δ = (%s)² − 4(%d)k = 0, so %d = %dk and <b>k = %d</b>." % (s(b), a, b * b, 4 * a, kk))
    b = r.choice([2, 4, 6, 8, 10, 12, 14, -2, -4, -6, -8, -10, -12])
    kk = _F(b * b, 4)
    if kk.denominator != 1:
        raise AssertionError
    kk = int(kk)
    if r.random() < 0.5:
        return mcq("For which values of k does <b>x² %s + k = 0</b> have real roots?" % sgn(b).replace(s(abs(b)), s(abs(b)) + "x"), "k ≤ %d" % kk, ["k ≥ %d" % kk, "k &lt; %d" % kk, "k ≤ %s" % s(-kk)],
                   "Real roots: Δ ≥ 0. (%s)² − 4k ≥ 0, so 4k ≤ %d and <b>k ≤ %d</b>." % (s(b), b * b, kk))
    return mcq("For which values of k does <b>x² %s + k = 0</b> have non-real roots?" % sgn(b).replace(s(abs(b)), s(abs(b)) + "x"), "k &gt; %d" % kk, ["k &lt; %d" % kk, "k ≥ %d" % kk, "k &gt; %s" % s(-kk)],
               "Non-real roots: Δ &lt; 0. (%s)² − 4k &lt; 0, so <b>k &gt; %d</b>." % (s(b), kk))


def lq_tan(r):
    a = r.choice([1, 1, 2, -1])
    b = r.randint(-4, 4)
    c = r.randint(-5, 5)
    m = r.randint(-4, 4)
    if (b - m) ** 2 % (4 * abs(a)):
        raise AssertionError
    kk = c - _F((b - m) ** 2, 4 * a)
    if kk.denominator != 1:
        raise AssertionError
    kk = int(kk)
    par = "y = " + quad(a, b, c)
    ln = "y = " + (("" if m == 1 else "−" if m == -1 else s(m)) + "x + k" if m else "k")
    return mcq("For which value of k is the line <b>%s</b> a tangent to the parabola <b>%s</b>?" % (ln, par), "k = %s" % s(kk), wr3("k = %s" % s(kk), ["k = %s" % s(-kk), "k = %s" % s(c), "k = %s" % s(kk + 1), "k = %s" % s(c + _F((b - m) ** 2, 4 * a)) if (c + _F((b - m) ** 2, 4 * a)).denominator == 1 else "k = %s" % s(kk - 2)]),
               "Set them equal: %s = 0. A tangent touches once, so Δ = 0: (%s)² − 4(%s)(%s − k) = 0, so <b>k = %s</b>." % (quad(a, b - m, c) + " − k", s(b - m), s(a), s(c), s(kk)))


def qineq(r, k):
    p, q = sorted(r.sample(range(-7, 8), 2))
    b, c = -(p + q), p * q
    op = r.choice(["&lt;", "≤", "&gt;", "≥"])
    inside = op in ("&lt;", "≤")
    lo = "&lt;" if op in ("&lt;", "&gt;") else "≤"
    lo_out = "&lt;" if op in ("&lt;", "&gt;") else "≤"
    hi_out = "&gt;" if op in ("&lt;", "&gt;") else "≥"
    a_in = "%s %s x %s %s" % (s(p), lo, lo, s(q))
    a_out = "x %s %s or x %s %s" % (lo_out, s(p), hi_out, s(q))
    if k == "fact":
        expr = "(%s)(%s)" % (shift(-p), shift(-q))
        neg = False
    elif k == "exp":
        expr = quad(1, b, c)
        neg = False
    else:
        expr = quad(-1, -b, -c)
        neg = True
    right = a_in if inside != neg else a_out
    wrong = a_out if right == a_in else a_in
    flip = {"&lt;": "&gt;", "&gt;": "&lt;", "≤": "≥", "≥": "≤"}
    why = ("Multiply by −1 and reverse the sign: %s %s 0. " % (quad(1, b, c), flip[op]) if neg else "") + \
          "The roots are %s and %s. The parabola is ∪, so it is %s 0 %s the roots: <b>%s</b>." % (s(p), s(q), "below" if (inside != neg) else "above", "between" if right == a_in else "outside", right)
    return mcq("Solve <b>%s %s 0</b>." % (expr, op), right, wr3(right, [wrong, "%s %s x %s %s" % (s(-q), lo, lo, s(-p)), "x %s %s or x %s %s" % (lo_out, s(-q), hi_out, s(-p)), "x %s %s" % (op, s(q))]), why)


def qseq(r, k):
    a = r.choice([1, 2, 3, -1, -2, 0.5])
    b = r.randint(-5, 5)
    c = r.randint(-6, 8)
    T = lambda n: a * n * n + b * n + c
    terms = [T(n) for n in range(1, 5)]
    if any(abs(t - round(t)) > 1e-9 for t in terms):
        raise AssertionError
    seq = "; ".join(s(t) for t in terms) + "; …"
    if k == "second":
        d2 = 2 * a
        return mcq("Find the second difference of the quadratic pattern <b>%s</b>." % seq, s(d2), wr3(s(d2), [s(terms[1] - terms[0]), s(a), s(terms[2] - terms[1]), s(d2 + 1)]),
                   "First differences: %s; %s; %s. Second difference: <b>%s</b>." % (s(terms[1] - terms[0]), s(terms[2] - terms[1]), s(terms[3] - terms[2]), s(d2)))
    if k == "next":
        n5 = T(5)
        return mcq("Find the next term of the quadratic pattern <b>%s</b>." % seq, s(n5), wr3(s(n5), [s(terms[3] + (terms[3] - terms[2])), s(n5 + 2 * a), s(n5 - 2 * a), s(terms[3] + 2 * a)]),
                   "The second difference is %s, so the next first difference is %s. %s + %s = <b>%s</b>." % (s(2 * a), s(terms[3] - terms[2] + 2 * a), s(terms[3]), s(terms[3] - terms[2] + 2 * a), s(n5)))
    def tn(a_, b_, c_):
        return "T<sub>n</sub> = " + quad(a_, b_, c_, "n")
    if k == "rule":
        if a == 0.5:
            raise AssertionError
        right = tn(a, b, c)
        return mcq("Find the general term of the quadratic pattern <b>%s</b>." % seq, right, wr3(right, [tn(2 * a, b - a, c), tn(a, b, c + 1), tn(a, -b, c), tn(a, b + 1, c - 1)]),
                   "2a = %s, so a = %s. 3a + b = %s, so b = %s. a + b + c = %s, so c = %s: <b>%s</b>." % (s(2 * a), s(a), s(terms[1] - terms[0]), s(b), s(terms[0]), s(c), right))
    n = r.choice([10, 12, 15, 20, 25, 30])
    if k == "term":
        v = T(n)
        return mcq("The general term of a pattern is <b>%s</b>. Find T<sub>%d</sub>." % (tn(a, b, c)[len("T<sub>n</sub> = "):] and tn(a, b, c), n), s(v), wr3(s(v), [s(a * 2 * n + b * n + c), s(a * n * n + c), s(T(n - 1)), s(T(n + 1))]),
                   "T<sub>%d</sub> = %s(%d)² %s(%d) %s = <b>%s</b>." % (n, s(a), n, sgn(b), n, sgn(c), s(v)))
    if a < 0:
        raise AssertionError
    v = T(n)
    return mcq("For the pattern <b>%s</b>, which term has the value %s?" % (tn(a, b, c), s(v)), "T<sub>%d</sub>" % n, wr3("T<sub>%d</sub>" % n, ["T<sub>%d</sub>" % (n - 1), "T<sub>%d</sub>" % (n + 1), "T<sub>%d</sub>" % (2 * n), "T<sub>%d</sub>" % (n + 2)]),
               "Solve %s = %s. The positive whole-number solution is n = %d: <b>T<sub>%d</sub></b>." % (quad(a, b, c, "n"), s(v), n, n))


def build():
    sets, R = build_sets([
        ("The discriminant", [("collect", fk(nature, "disc"), 20)]),
        ("Describe the roots", [("collect", fk(nature, "nat"), 20)]),
        ("Number of real roots", [("collect", kp(usq.one_disc), 20)]),
        ("Equal roots", [("collect", fk(nature, "equal"), 20)]),
        ("Real or non-real roots", [("collect", fk(nature, "range"), 20)]),
    ], 81103)
    finish(sets, R)
    body = lesson('<ul><li>Δ = b² − 4ac.</li><li>Δ &lt; 0: non-real roots. Δ = 0: real, equal roots.</li><li>Δ &gt; 0: real, unequal roots, rational if Δ is a perfect square and irrational if it is not.</li><li>Real roots means Δ ≥ 0.</li></ul>',
        [example("2x² − 3x − 5 = 0", ["Δ = 9 + 40 = 49"], "real, unequal, rational")],
        [['The sign', 'Δ = b² − 4ac, so watch negative c.'], ['Rational or irrational', 'Check if Δ is a perfect square.'], ['Equal roots', 'Equal roots: Δ = 0.']])
    faq = [('What does CAPS Grade 11 say?', 'Determine the nature of the roots of a quadratic equation using the discriminant.'), ('What does non-real mean?', 'The roots are not real numbers.'), ('Is Δ = 0 rational?', 'Yes, the root is −b/2a.'), ('Can I use Δ for a graph?', 'Yes: it tells you how many x-intercepts there are.')]
    make('nature-of-roots', 3, 'Algebra and Number Patterns', 'Grade 11: Equations and inequalities',
         'Nature of roots: determine the nature of the roots of a quadratic equation using the discriminant Δ = b² − 4ac.',
         'The Nature of Roots and the Discriminant', 'Nature of Roots',
         'Free CAPS Grade 11 worksheets: the discriminant, nature of roots, and values of k for equal, real and non-real roots. 100 questions with memos.',
         'Δ = b² − 4ac.', 'Δ ≥ 0: real roots.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
