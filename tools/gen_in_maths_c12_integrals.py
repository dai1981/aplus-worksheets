# -*- coding: utf-8 -*-
"""
India Class 12 Maths, NCERT Chapter 7: Integrals (CBSE Unit III Calculus)
  python3 tools/gen_in_maths_c12_integrals.py
Integration as the reverse of differentiation: powers, trigonometric, exponential and 1/x; integration by
substitution; the standard integrals of 1/(x² + a²), 1/(x² − a²) and 1/√(a² − x²); partial fractions; integration by
parts; and definite integrals with the fundamental theorem and the odd-function property (own makers).
Wrong answers come from real mistakes: xⁿ⁺¹/n, forgetting to divide by k in ∫ sin kx dx, the wrong sign for
∫ sin x dx, missing the inner derivative in a substitution, ∫ uv = ∫u ∫v, and F(a) − F(b) in a definite integral.
"""
import random
from fractions import Fraction as F
from in_sr import U, T2, X, sup, pi
from in_common import num, fv
import in_common, re

R = random.Random(912107)
C_ = " + C"
DX = " d%s" % X


def ex(terms):
    return re.sub(r"(\d)(sin|cos|log|tan|e<sup>)", r"\1 \2", in_common.expr(terms))


def coef(c):
    c = F(c)
    if c == 1:
        return ""
    if c == -1:
        return "−"
    if c.denominator == 1:
        return num(c)
    return ("−" if c < 0 else "") + "(%d/%d)" % (abs(c.numerator), c.denominator)


def one_power(r):
    n = r.choice([2, 3, 4, 5, 6, -2, -3, F(1, 2), F(3, 2)])
    a = r.choice([1, 2, 3, 4, 5, 6])
    m = F(n) + 1
    term = lambda c, p: "%s%s<sup>%s</sup>" % (coef(c), X, fv(p).replace("<span class='fr'><span class='fn'>", "").replace("</span><span class='fd'>", "/").replace("</span></span>", "")) if p != 1 else "%s%s" % (coef(c), X)
    q = "∫ %s%s%s" % (coef(a), "%s<sup>%s</sup>" % (X, frs(n)) if n != 1 else X, DX)
    right = term(F(a) / m, m) + C_
    return T2("Evaluate %s." % q, right, [term(F(a) / F(n), m) + C_, term(F(a) * F(n), F(n) - 1) + C_, term(F(a) / m, F(n)) + C_],
              "∫ %s<sup>n</sup> d%s = %s<sup>n+1</sup>/(n + 1) + C with n + 1 = %s: <b>%s</b>." % (X, X, X, frs(m), right))


def frs(v):
    v = F(v)
    s = "−" if v < 0 else ""
    v = abs(v)
    return s + (str(v.numerator) if v.denominator == 1 else "%d/%d" % (v.numerator, v.denominator))


def one_std(r):
    k = r.randint(2, 6)
    t = r.choice(["sin", "cos", "exp", "sec2", "recip", "lin"])
    kx = "%d%s" % (k, X)
    if t == "sin":
        right = "−(1/%d) cos %s%s" % (k, kx, C_)
        return T2("Evaluate ∫ sin %s%s." % (kx, DX), right, ["(1/%d) cos %s%s" % (k, kx, C_), "−%d cos %s%s" % (k, kx, C_), "−cos %s%s" % (kx, C_)],
                  "d/d%s(cos %s) = −%d sin %s, so the integral is <b>%s</b>." % (X, kx, k, kx, right))
    if t == "cos":
        right = "(1/%d) sin %s%s" % (k, kx, C_)
        return T2("Evaluate ∫ cos %s%s." % (kx, DX), right, ["−(1/%d) sin %s%s" % (k, kx, C_), "%d sin %s%s" % (k, kx, C_), "sin %s%s" % (kx, C_)],
                  "d/d%s(sin %s) = %d cos %s, so divide by %d: <b>%s</b>." % (X, kx, k, kx, k, right))
    if t == "exp":
        right = "(1/%d)e<sup>%s</sup>%s" % (k, kx, C_)
        return T2("Evaluate ∫ e<sup>%s</sup>%s." % (kx, DX), right, ["%de<sup>%s</sup>%s" % (k, kx, C_), "e<sup>%s</sup>%s" % (kx, C_), "e<sup>%s</sup>/(%d + 1)%s" % (kx, k, C_)],
                  "Divide by the coefficient %d: <b>%s</b>." % (k, right))
    if t == "sec2":
        right = "(1/%d) tan %s%s" % (k, kx, C_)
        return T2("Evaluate ∫ sec² %s%s." % (kx, DX), right, ["%d tan %s%s" % (k, kx, C_), "tan %s%s" % (kx, C_), "(1/%d) sec %s%s" % (k, kx, C_)],
                  "d/d%s(tan %s) = %d sec² %s, so <b>%s</b>." % (X, kx, k, kx, right))
    if t == "recip":
        b = r.choice([k_ for k_ in range(-7, 8) if k_])
        u = "%d%s %s %d" % (k, X, "+" if b > 0 else "−", abs(b))
        right = "(1/%d) log|%s|%s" % (k, u, C_)
        return T2("Evaluate ∫ 1/(%s)%s." % (u, DX), right, ["log|%s|%s" % (u, C_), "%d log|%s|%s" % (k, u, C_), "−1/(%s)²%s" % (u, C_)],
                  "∫ 1/(a%s + b) d%s = (1/a) log|a%s + b| + C: <b>%s</b>." % (X, X, X, right))
    b = r.choice([k_ for k_ in range(-7, 8) if k_])
    n = r.randint(2, 6)
    u = "%d%s %s %d" % (k, X, "+" if b > 0 else "−", abs(b))
    right = "(%s)<sup>%d</sup>/%d%s" % (u, n + 1, k * (n + 1), C_)
    return T2("Evaluate ∫ (%s)<sup>%d</sup>%s." % (u, n, DX), right, ["(%s)<sup>%d</sup>/%d%s" % (u, n + 1, n + 1, C_), "(%s)<sup>%d</sup>/%d%s" % (u, n + 1, k, C_), ("%d(%s)<sup>%d</sup>%s" % (k * n, u, n - 1, C_)) if n > 2 else "%d(%s)%s" % (k * n, u, C_)],
              "(%s)<sup>%d</sup> ÷ (%d × %d) + C = <b>%s</b>." % (u, n + 1, n + 1, k, right))


def one_sub(r):
    t = r.choice(["xcos", "xexp", "fpf", "sincos", "xsqrt"])
    a = r.randint(2, 5)
    if t == "xcos":
        return T2("Evaluate ∫ %s%s cos(%s²)%s." % ("" if a == 2 else num(a), X, X, DX), "%ssin(%s²)%s" % (coef(F(a, 2)), X, C_),
                  ["%ssin(%s²)%s" % (coef(a), X, C_), "%scos(%s²)%s" % (coef(F(a, 2)), X, C_), "%s%s² sin(%s²)%s" % (coef(F(a, 2)), X, X, C_)],
                  "Put t = %s², dt = 2%s d%s: the integral is %s∫ cos t dt = <b>%ssin(%s²) + C</b>." % (X, X, X, coef(F(a, 2)), coef(F(a, 2)), X))
    if t == "xexp":
        return T2("Evaluate ∫ %s%s e<sup>%s²</sup>%s." % ("" if a == 2 else num(a), X, X, DX), "%se<sup>%s²</sup>%s" % (coef(F(a, 2)), X, C_),
                  ["%se<sup>%s²</sup>%s" % (coef(a), X, C_), "%s%s² e<sup>%s²</sup>%s" % (coef(F(a, 2)), X, X, C_), "e<sup>%s²</sup>/(%s²)%s" % (X, X, C_)],
                  "Put t = %s², dt = 2%s d%s: <b>%se<sup>%s²</sup> + C</b>." % (X, X, X, coef(F(a, 2)), X))
    if t == "fpf":
        b = r.randint(2, 9)
        return T2("Evaluate ∫ 2%s/(%s² + %d)%s." % (X, X, b, DX), "log(%s² + %d)%s" % (X, b, C_), ["2 log(%s² + %d)%s" % (X, b, C_), "%s²/(%s² + %d)%s" % (X, X, b, C_), "(1/%d) tan<sup>−1</sup>(%s/%d)%s" % (b, X, b, C_)],
                  "The numerator 2%s is the derivative of the denominator, so the integral is <b>log(%s² + %d) + C</b>." % (X, X, b))
    if t == "sincos":
        n = r.randint(2, 5)
        return T2("Evaluate ∫ sin<sup>%d</sup>%s cos %s%s." % (n, X, X, DX), "sin<sup>%d</sup>%s/%d%s" % (n + 1, X, n + 1, C_),
                  ["cos<sup>%d</sup>%s/%d%s" % (n + 1, X, n + 1, C_), "sin<sup>%d</sup>%s/%d%s" % (n + 1, X, n, C_), "−sin<sup>%d</sup>%s/%d%s" % (n + 1, X, n + 1, C_)],
                  "Put t = sin %s, dt = cos %s d%s: ∫ t<sup>%d</sup> dt = <b>sin<sup>%d</sup>%s/%d + C</b>." % (X, X, X, n, n + 1, X, n + 1))
    b = r.randint(1, 9)
    return T2("Evaluate ∫ %s/√(%s² + %d)%s." % (X, X, b, DX), "√(%s² + %d)%s" % (X, b, C_), ["2√(%s² + %d)%s" % (X, b, C_), "(1/2)√(%s² + %d)%s" % (X, b, C_), "log(%s² + %d)%s" % (X, b, C_)],
              "Put t = %s² + %d, dt = 2%s d%s: (1/2)∫ t<sup>−1/2</sup> dt = <b>√(%s² + %d) + C</b>." % (X, b, X, X, X, b))


def one_form(r):
    a = r.randint(1, 7)
    t = r.choice(["atan", "asin", "diff", "pf"])
    if t == "atan":
        if a == 1:
            return None
        right = "(1/%d) tan<sup>−1</sup>(%s/%d)%s" % (a, X, a, C_) if a > 1 else "tan<sup>−1</sup> %s%s" % (X, C_)
        return T2("Evaluate ∫ 1/(%s² + %d)%s." % (X, a * a, DX), right,
                  ["tan<sup>−1</sup>(%s/%d)%s" % (X, a, C_) if a > 1 else "(1/2) tan<sup>−1</sup> %s%s" % (X, C_), "(1/%d) log|%s² + %d|%s" % (a, X, a * a, C_), "(1/%d) sin<sup>−1</sup>(%s/%d)%s" % (a, X, a, C_)],
                  "∫ d%s/(%s² + a²) = (1/a) tan<sup>−1</sup>(%s/a) + C with a = %d: <b>%s</b>." % (X, X, X, a, right))
    if t == "asin":
        if a == 1:
            return None
        right = "sin<sup>−1</sup>(%s/%d)%s" % (X, a, C_)
        return T2("Evaluate ∫ 1/√(%d − %s²)%s." % (a * a, X, DX), right, ["(1/%d) sin<sup>−1</sup>(%s/%d)%s" % (a, X, a, C_), "cos<sup>−1</sup>(%s/%d)%s" % (X, a, C_), "(1/%d) tan<sup>−1</sup>(%s/%d)%s" % (a, X, a, C_)],
                  "∫ d%s/√(a² − %s²) = sin<sup>−1</sup>(%s/a) + C: <b>%s</b>." % (X, X, X, right))
    if t == "diff":
        if a == 1:
            return None
        right = "(1/%d) log|(%s − %d)/(%s + %d)|%s" % (2 * a, X, a, X, a, C_)
        return T2("Evaluate ∫ 1/(%s² − %d)%s." % (X, a * a, DX), right, ["(1/%d) log|(%s − %d)/(%s + %d)|%s" % (a, X, a, X, a, C_), "(1/%d) log|(%s + %d)/(%s − %d)|%s" % (2 * a, X, a, X, a, C_), "(1/%d) tan<sup>−1</sup>(%s/%d)%s" % (a, X, a, C_)],
                  "∫ d%s/(%s² − a²) = (1/2a) log|(%s − a)/(%s + a)| + C: <b>%s</b>." % (X, X, X, X, right))
    p, q = sorted(r.sample(range(-6, 7), 2))
    d = q - p
    lin = lambda c: "%s %s %d" % (X, "−" if c > 0 else "+", abs(c)) if c else X
    right = "%slog|(%s)/(%s)|%s" % (coef(F(1, d)), lin(q), lin(p), C_)
    return T2("Evaluate ∫ 1/((%s)(%s))%s." % (lin(p), lin(q), DX), right,
              ["%slog|(%s)/(%s)|%s" % (coef(F(1, d)), lin(p), lin(q), C_), "log|(%s)(%s)|%s" % (lin(p), lin(q), C_), "%slog|(%s)/(%s)|%s" % (coef(d), lin(q), lin(p), C_)],
              "Partial fractions: 1/((%s)(%s)) = %s[1/(%s) − 1/(%s)], so the integral is <b>%s</b>." % (lin(p), lin(q), coef(F(1, d)) or "1 ×", lin(q), lin(p), right))


PARTS = [("%s e<sup>%s</sup>" % (X, X), "e<sup>%s</sup>(%s − 1)" % (X, X), ["%s e<sup>%s</sup>" % (X, X), "e<sup>%s</sup>(%s + 1)" % (X, X), "(%s²/2) e<sup>%s</sup>" % (X, X)]),
         ("%s sin %s" % (X, X), "−%s cos %s + sin %s" % (X, X, X), ["%s cos %s − sin %s" % (X, X, X), "−%s cos %s − sin %s" % (X, X, X), "(%s²/2)(−cos %s)" % (X, X)]),
         ("%s cos %s" % (X, X), "%s sin %s + cos %s" % (X, X, X), ["%s sin %s − cos %s" % (X, X, X), "−%s sin %s + cos %s" % (X, X, X), "(%s²/2) sin %s" % (X, X)]),
         ("log %s" % X, "%s log %s − %s" % (X, X, X), ["1/%s" % X, "%s log %s + %s" % (X, X, X), "(log %s)²/2" % X]),
         ("%s log %s" % (X, X), "(%s²/2) log %s − %s²/4" % (X, X, X), ["(%s²/2) log %s" % (X, X), "%s log %s − %s" % (X, X, X), "(%s²/2) log %s + %s²/4" % (X, X, X)]),
         ("e<sup>%s</sup>(sin %s + cos %s)" % (X, X, X), "e<sup>%s</sup> sin %s" % (X, X), ["e<sup>%s</sup> cos %s" % (X, X), "e<sup>%s</sup>(sin %s − cos %s)" % (X, X, X), "−e<sup>%s</sup> sin %s" % (X, X)]),
         ("tan<sup>−1</sup> %s" % X, "%s tan<sup>−1</sup> %s − (1/2) log(1 + %s²)" % (X, X, X), ["1/(1 + %s²)" % X, "%s tan<sup>−1</sup> %s + (1/2) log(1 + %s²)" % (X, X, X), "%s tan<sup>−1</sup> %s" % (X, X)]),
         ("%s² e<sup>%s</sup>" % (X, X), "e<sup>%s</sup>(%s² − 2%s + 2)" % (X, X, X), ["e<sup>%s</sup>(%s² + 2%s + 2)" % (X, X, X), "%s² e<sup>%s</sup>" % (X, X), "(%s³/3) e<sup>%s</sup>" % (X, X)])]


def one_parts(r):
    f, right, wr = r.choice(PARTS)
    return T2("Evaluate ∫ %s%s." % (f, DX), right + C_, [w + C_ for w in wr],
              "Integrate by parts, ∫ u v d%s = u ∫v d%s − ∫(u′ ∫v d%s) d%s: <b>%s + C</b>. (Differentiate the answer to check.)" % (X, X, X, X, right))


def ev(cs, x):
    v = F(0)
    for c in cs:
        v = v * x + c
    return v


def one_def(r):
    t = r.choice(["poly", "poly", "std", "odd"])
    if t == "poly":
        cs = [r.randint(-3, 4), r.randint(-6, 6), r.randint(-6, 6)]
        a, b = sorted(r.sample(range(-2, 4), 2))
        anti = [F(cs[0], 3), F(cs[1], 2), F(cs[2]), F(0)]
        v = ev(anti, b) - ev(anti, a)
        poly_s = in_common.expr([(cs[0], X + "²"), (cs[1], X), (cs[2], "")])
        return T2("Evaluate ∫<sub>%s</sub><sup>%s</sup> (%s)%s." % (num(a), num(b), poly_s, DX), fv(v), [fv(-v) if v else "1", fv(ev(cs, b) - ev(cs, a)), fv(ev(anti, b)) if ev(anti, b) != v else fv(v + 1)],
                  "Find an antiderivative F and work out F(%s) − F(%s): <b>%s</b>." % (num(b), num(a), fv(v)))
    if t == "std":
        q, right, wr, why = r.choice([("∫<sub>0</sub><sup>π/2</sup> sin %s%s" % (X, DX), "1", ["0", "−1", "π/2"], "[−cos %s] from 0 to π/2 = 0 − (−1) = 1" % X),
                                      ("∫<sub>0</sub><sup>π</sup> sin %s%s" % (X, DX), "2", ["0", "1", "π"], "[−cos %s] from 0 to π = 1 − (−1) = 2" % X),
                                      ("∫<sub>0</sub><sup>1</sup> e<sup>%s</sup>%s" % (X, DX), "e − 1", ["e", "1", "e + 1"], "[e<sup>%s</sup>] from 0 to 1 = e − 1" % X),
                                      ("∫<sub>1</sub><sup>e</sup> (1/%s)%s" % (X, DX), "1", ["e", "e − 1", "0"], "[log %s] from 1 to e = 1 − 0 = 1" % X),
                                      ("∫<sub>0</sub><sup>1</sup> 1/(1 + %s²)%s" % (X, DX), "π/4", ["π/2", "1", "log 2"], "[tan<sup>−1</sup> %s] from 0 to 1 = π/4" % X),
                                      ("∫<sub>0</sub><sup>π/4</sup> sec² %s%s" % (X, DX), "1", ["0", "√2", "π/4"], "[tan %s] from 0 to π/4 = 1" % X),
                                      ("∫<sub>0</sub><sup>π/2</sup> cos %s%s" % (X, DX), "1", ["0", "−1", "π/2"], "[sin %s] from 0 to π/2 = 1" % X),
                                      ("∫<sub>2</sub><sup>3</sup> (1/%s)%s" % (X, DX), "log(3/2)", ["log 6", "1/6", "log 3 · log 2"], "[log %s] from 2 to 3 = log 3 − log 2" % X)])
        return T2("Evaluate %s." % q, right, wr, "%s: <b>%s</b>." % (why, right))
    a = r.randint(1, 5)
    f = r.choice(["%s³" % X, "sin %s" % X, "%s⁵ + %s" % (X, X), "%s cos %s" % (X, X), "tan %s" % X if a == 1 else "%s³ − 4%s" % (X, X), "%s|%s|" % (X, X)])
    fq = ("(%s)" % f) if (" + " in f or " − " in f) else f
    return T2("Evaluate ∫<sub>−%d</sub><sup>%d</sup> %s%s." % (a, a, fq, DX), "0", [num(2 * a), num(a * a), "It cannot be found without the antiderivative"],
              "%s is an odd function (f(−%s) = −f(%s)), so its integral over [−a, a] is <b>0</b>." % (f, X, X))


def spaced(fn):
    def f(r):
        it = fn(r)
        if it:
            sp = lambda t: re.sub(r"(\d|\))(sin|cos|log|tan|sec|e<sup>)", r"\1 \2", t)
            it["q"], it["e"] = sp(it["q"]), sp(it["e"])
            it["c"] = [sp(c) for c in it["c"]]
        return it
    f.__name__ = fn.__name__
    return f


one_power, one_std, one_sub, one_form, one_parts, one_def = [spaced(g) for g in (one_power, one_std, one_sub, one_form, one_parts, one_def)]


U(12, 7, "integrals", 7, "Ca", "Integrals: Substitution, Partial Fractions, Parts and Definite Integrals", "integrals",
  "Integration as inverse process of differentiation; integration of a variety of functions by substitution, by partial fractions and by parts; evaluation of simple integrals of particular types (dx/(x² ± a²), dx/√(a² − x²) and others); fundamental theorem of calculus (without proof); basic properties of definite integrals and evaluation of definite integrals (summary of the CBSE syllabus)",
  "Class 12 Integrals worksheet (NCERT Chapter 7): standard integrals, substitution, special forms, partial fractions, integration by parts and definite integrals. 100 questions with answers.",
  "∫ xⁿ dx = xⁿ⁺¹/(n + 1) + C (n ≠ −1).", "∫ₐᵇ f(x) dx = F(b) − F(a).",
  "<ul><li>Integration reverses differentiation: ∫ <i>x</i><sup>n</sup> d<i>x</i> = <i>x</i><sup>n+1</sup>/(n + 1) + C, ∫ 1/<i>x</i> d<i>x</i> = log|<i>x</i>| + C, ∫ e<sup><i>x</i></sup> d<i>x</i> = e<sup><i>x</i></sup> + C.</li>"
  "<li>∫ sin k<i>x</i> d<i>x</i> = −(1/k) cos k<i>x</i> + C; ∫ cos k<i>x</i> d<i>x</i> = (1/k) sin k<i>x</i> + C.</li>"
  "<li><b>Substitution</b>: if the integrand has g(<i>x</i>) and g′(<i>x</i>), put t = g(<i>x</i>).</li>"
  "<li><b>Standard forms</b>: ∫ d<i>x</i>/(<i>x</i>² + a²) = (1/a) tan<sup>−1</sup>(<i>x</i>/a); ∫ d<i>x</i>/√(a² − <i>x</i>²) = sin<sup>−1</sup>(<i>x</i>/a).</li>"
  "<li><b>By parts</b>: ∫ u v d<i>x</i> = u∫v d<i>x</i> − ∫(u′∫v d<i>x</i>) d<i>x</i>. <b>Definite</b>: ∫<sub>a</sub><sup>b</sup> f = F(b) − F(a); for an odd f, ∫<sub>−a</sub><sup>a</sup> f = 0.</li></ul>",
  [("Evaluate ∫ <i>x</i> e<sup><i>x</i></sup> d<i>x</i>.", ["u = <i>x</i>, v = e<sup><i>x</i></sup>", "<i>x</i>e<sup><i>x</i></sup> − ∫ e<sup><i>x</i></sup> d<i>x</i>"], "e<sup><i>x</i></sup>(<i>x</i> − 1) + C")],
  ["Writing ∫ xⁿ dx = xⁿ⁺¹/n.", "Forgetting to divide by k in ∫ sin kx dx.", "Working out F(a) − F(b) for a definite integral."],
  [("Why add C?", "Every function has many antiderivatives that differ by a constant."), ("How can I check an integral?", "Differentiate your answer; you should get the integrand back.")],
  [("Standard integrals", [(one_power, 10), (one_std, 10)]),
   ("Integration by substitution", [(one_sub, 14), (one_std, 6)]),
   ("Special forms and partial fractions", [(one_form, 20)]),
   ("Integration by parts", [(one_parts, 8), (one_form, 6), (one_sub, 6)]),
   ("Definite integrals", [(one_def, 20)])], 912107)
