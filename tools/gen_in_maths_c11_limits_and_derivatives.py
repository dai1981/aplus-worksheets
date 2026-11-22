# -*- coding: utf-8 -*-
"""
India Class 11 Maths, NCERT Chapter 12: Limits and Derivatives (CBSE Unit IV Calculus)
  python3 tools/gen_in_maths_c11_limits_and_derivatives.py
Limits by substitution and by factorising, lim (xⁿ − aⁿ)/(x − a) = naⁿ⁻¹, lim sin x / x = 1, derivatives of
polynomials, of xⁿ for negative n, of sin x and cos x, the product and quotient rules, the derivative at a point,
and the derivative from first principles (own makers).
Wrong answers come from real mistakes: stopping at 0/0, aⁿ⁻¹ without the n, sin kx / x = 1, nxⁿ⁺¹, (uv)′ = u′v′,
the quotient rule with the wrong sign, and d/dx(cos x) = sin x.
"""
import random
from fractions import Fraction as F
from in_sr import U, T2, X, poly, xp, sup
from in_common import num, fv
import in_common, re


def expr(terms):
    return re.sub(r"(\d)(sin|cos)", r"\1 \2", in_common.expr(terms))

R = random.Random(911112)


def ev(cs, x):
    v = 0
    for c in cs:
        v = v * x + c
    return v


def der(cs):
    d = len(cs) - 1
    return [c * (d - i) for i, c in enumerate(cs[:-1])]


def lim_sub(r):
    a = r.randint(-4, 4)
    cs = [r.randint(1, 3), r.randint(-6, 6), r.randint(-9, 9)]
    v = ev(cs, a)
    return T2("Evaluate lim<sub>%s→%s</sub> (%s)." % (X, num(a), poly(cs)), num(v), [num(ev(cs, -a)) if ev(cs, -a) != v else num(v + 1), num(cs[-1]), num(v + cs[0])],
              "A polynomial is continuous, so substitute %s = %s: <b>%s</b>." % (X, num(a), num(v)))


def lim_fact(r):
    a = r.choice([k for k in range(-5, 6) if k])
    b = r.choice([k for k in range(-6, 7) if k != -a])
    top = [1, b - a, -a * b]          # (x - a)(x + b)
    if r.random() < 0.5:
        bot = [1, -a]
        val = a + b
        bs = poly(bot)
    else:
        c = r.choice([k for k in range(-5, 6) if k not in (-a,)])
        bot = [1, c - a, -a * c]
        val = F(a + b, a + c) if a + c else None
        if val is None:
            return None
        bs = poly(bot)
    return T2("Evaluate lim<sub>%s→%s</sub> (%s) ÷ (%s)." % (X, num(a), poly(top), bs), fv(val), ["0", "The limit does not exist", fv(val + 1) if val + 1 != 0 else "1"],
              "Substituting gives 0/0, so factorise: (%s − %s) is a factor of both. Cancel it and substitute %s = %s: <b>%s</b>." % (X, num(a) if a > 0 else "(" + num(a) + ")", X, num(a), fv(val)))


def lim_power(r):
    n = r.randint(2, 8)
    a = r.choice([1, 2, 3, -1, -2])
    v = n * a ** (n - 1)
    return T2("Evaluate lim<sub>%s→%s</sub> (%s %s %s) ÷ (%s %s %s)." % (X, num(a), xp(n), "−" if a ** n >= 0 else "+", num(abs(a ** n)), X, "−" if a > 0 else "+", num(abs(a))),
              num(v), [num(a ** (n - 1)), num(n * a ** n), num((n - 1) * a ** (n - 2)) if n > 2 else num(v + 1)],
              "lim (%sⁿ − aⁿ) ÷ (%s − a) = n·aⁿ⁻¹ = %d × (%s)<sup>%d</sup> = <b>%s</b>." % (X, X, n, num(a), n - 1, num(v)))


def lim_trig(r):
    a, b = r.randint(1, 9), r.randint(1, 9)
    if a == b:
        return None
    k = r.choice(["sx", "ss", "tx"])
    if k == "sx":
        return T2("Evaluate lim<sub>%s→0</sub> sin %d%s ÷ %d%s." % (X, a, X, b, X), fv(F(a, b)), ["1", fv(F(b, a)), "0"],
                  "sin %d%s ÷ %d%s = (sin %d%s ÷ %d%s) × %d/%d → 1 × %d/%d = <b>%s</b>." % (a, X, b, X, a, X, a, X, a, b, a, b, fv(F(a, b))))
    if k == "ss":
        return T2("Evaluate lim<sub>%s→0</sub> sin %d%s ÷ sin %d%s." % (X, a, X, b, X), fv(F(a, b)), ["1", fv(F(b, a)), "0"],
                  "Divide top and bottom by %s: the limit is %d ÷ %d = <b>%s</b>." % (X, a, b, fv(F(a, b))))
    return T2("Evaluate lim<sub>%s→0</sub> tan %d%s ÷ %s." % (X, a, X, X), str(a), ["1", fv(F(1, a)), "0"],
              "tan %d%s ÷ %s = (sin %d%s ÷ %d%s) × %d ÷ cos %d%s → <b>%d</b>." % (a, X, X, a, X, a, X, a, a, X, a))


def dpoly(r):
    deg = r.randint(2, 4)
    cs = [r.choice([k for k in range(-5, 6) if k])] + [r.randint(-7, 7) for _ in range(deg)]
    d = der(cs)
    wrong1 = [c * (deg - i + 1) for i, c in enumerate(cs[:-1])]
    return T2("Find d/d%s (%s)." % (X, poly(cs)), poly(d), [poly(d + [0]) if False else expr([(c * (deg - i), xp(deg - i + 1)) for i, c in enumerate(cs[:-1])]),
                                                     poly(d[:-1] + [d[-1] + cs[-1]]) if cs[-1] else poly(d[:-1] + [d[-1] + 1]), poly([c for c in cs[:-1]])],
              "Differentiate term by term with d/d%s(%sⁿ) = n%sⁿ⁻¹; the constant gives 0: <b>%s</b>." % (X, X, X, poly(d)))


def dneg(r):
    a = r.choice([1, 2, 3, 4, 5, -2])
    n = r.choice([1, 2, 3, 4])
    f = "%s/%s" % (num(a), xp(n)) if n > 1 else "%s/%s" % (num(a), X)
    right = "%s%s" % (num(-a * n), X + sup(-(n + 1)))
    return T2("Find the derivative of %s." % f, right, ["%s%s" % (num(-a * n), X + sup(-(n - 1)) if n > 1 else ""), "%s%s" % (num(a * n), X + sup(-(n + 1))), "%s%s" % (num(-a), X + sup(-n))],
              "%s = %s%s, so the derivative is %s × %s<sup>−%d</sup> = <b>%s</b>." % (f, num(a), X + sup(-n), num(-n), X, n + 1, right))


def dtrig(r):
    a, b = r.choice([k for k in range(-5, 6) if k]), r.choice([k for k in range(-5, 6) if k])
    k = r.choice(["sc", "prod", "quot", "at"])
    if k == "sc":
        f = expr([(a, "sin " + X), (b, "cos " + X)])
        right = expr([(a, "cos " + X), (-b, "sin " + X)])
        return T2("Find the derivative of %s." % f, right, [expr([(a, "cos " + X), (b, "sin " + X)]), expr([(-a, "cos " + X), (-b, "sin " + X)]), expr([(b, "cos " + X), (-a, "sin " + X)])],
                  "d/d%s(sin %s) = cos %s and d/d%s(cos %s) = −sin %s, so the answer is <b>%s</b>." % (X, X, X, X, X, X, right))
    if k == "prod":
        n = r.randint(2, 4)
        right = "%s%s sin %s + %s cos %s" % (n, xp(n - 1), X, xp(n), X)
        return T2("Find the derivative of %s sin %s." % (xp(n), X), right, ["%s%s cos %s" % (n, xp(n - 1), X), "%s%s sin %s − %s cos %s" % (n, xp(n - 1), X, xp(n), X), "%s cos %s" % (xp(n), X)],
                  "Product rule: (uv)′ = u′v + uv′ = %s%s sin %s + %s cos %s. <b>%s</b>." % (n, xp(n - 1), X, xp(n), X, right))
    if k == "quot":
        p, q = r.choice([k for k in range(1, 6)]), r.choice([k for k in range(-6, 7) if k])
        num_ = p * 1 * 0
        top = "%s %s %d" % (X, "+" if q > 0 else "−", abs(q))
        right = "%d/(%s + %d)²" % (-2 * q, X, q) if False else None
        # f = (x + q)/(x - q): f' = -2q/(x - q)^2
        bot = "%s %s %d" % (X, "−" if q > 0 else "+", abs(q))
        right = "%s/(%s)²" % (num(-2 * q), bot)
        return T2("Find the derivative of (%s) ÷ (%s)." % (top, bot), right, ["%s/(%s)²" % (num(2 * q), bot), "1", "%s/(%s)" % (num(-2 * q), bot)],
                  "Quotient rule: (u/v)′ = (u′v − uv′) ÷ v² = ((%s) − (%s)) ÷ (%s)² = <b>%s</b>." % (bot, top, bot, right))
    cs = [r.choice([1, 2, 3]), r.randint(-5, 5), r.randint(-5, 5)]
    x0 = r.randint(-3, 3)
    v = ev(der(cs), x0)
    return T2("f(%s) = %s. Find f′(%s)." % (X, poly(cs), num(x0)), num(v), [num(ev(cs, x0)), num(ev(der(cs), -x0)) if ev(der(cs), -x0) != v else num(v + 2), num(2 * cs[0] * x0)],
              "f′(%s) = %s, so f′(%s) = <b>%s</b>." % (X, poly(der(cs)), num(x0), num(v)))


def dfirst(r):
    a, b, c = r.choice([1, 2, 3, -1]), r.randint(-6, 6), r.randint(-9, 9)
    cs = [a, b, c]
    return T2("Using the first principle, f(%s) = %s. What is lim<sub><i>h</i>→0</sub> [f(%s + <i>h</i>) − f(%s)] ÷ <i>h</i>?" % (X, poly(cs), X, X), poly(der(cs)),
              [poly([a, b]) if b else poly([a, 1]), poly([2 * a, b, c]), poly([2 * a, 0]) if b else poly([a, 0])],
              "f(%s + <i>h</i>) − f(%s) = <i>h</i>(%s + %s<i>h</i>), so dividing by <i>h</i> and letting <i>h</i> → 0 gives <b>%s</b>." % (X, X, poly(der(cs)), num(a) if a != 1 else "", poly(der(cs))))


U(11, 12, "limits-and-derivatives", 12, "Ca", "Limits and Derivatives: Standard Limits and Rules of Differentiation", "limits and derivatives",
  "Derivative introduced as rate of change both as that of distance function and geometrically; intuitive idea of limit; limits of polynomials and rational functions, trigonometric, exponential and logarithmic functions; definition of derivative, relate it to slope of tangent of a curve; derivative of sum, difference, product and quotient of functions; derivatives of polynomial and trigonometric functions (summary of the CBSE syllabus)",
  "Class 11 Limits and Derivatives worksheet (NCERT Chapter 12): limits by substitution and factorising, standard limits, sin x/x, derivatives of polynomials and trigonometric functions, product and quotient rules and first principles. 100 questions with answers.",
  "lim (xⁿ − aⁿ)/(x − a) = naⁿ⁻¹ and lim sin x/x = 1.", "d/dx(xⁿ) = nxⁿ⁻¹; (uv)′ = u′v + uv′.",
  "<ul><li>If substituting gives a number, that is the limit. If it gives 0/0, factorise and cancel first.</li>"
  "<li>Standard limits: lim<sub>x→a</sub> (xⁿ − aⁿ)/(x − a) = naⁿ⁻¹; lim<sub>x→0</sub> sin x/x = 1.</li>"
  "<li>Derivative: f′(x) = lim<sub>h→0</sub> [f(x + h) − f(x)]/h. d/dx(xⁿ) = nxⁿ⁻¹, d/dx(sin x) = cos x, d/dx(cos x) = −sin x.</li>"
  "<li>Product rule (uv)′ = u′v + uv′; quotient rule (u/v)′ = (u′v − uv′)/v².</li></ul>",
  [("Evaluate lim<sub>x→2</sub> (x² − 4)/(x − 2).", ["0/0, so factorise: (x − 2)(x + 2)/(x − 2)", "= x + 2 → 4"], "4")],
  ["Stopping at 0/0 and saying the limit does not exist.", "Writing d/dx(cos x) = sin x.", "Using (uv)′ = u′v′."],
  [("Is lim sin x/x = 1 true for x in degrees?", "No. It needs x in radians."), ("What is the derivative of a constant?", "0.")],
  [("Limits by substitution and factorising", [(lim_sub, 6), (lim_fact, 14)]),
   ("Standard limits", [(lim_power, 10), (lim_trig, 10)]),
   ("Derivatives of polynomials", [(dpoly, 12), (dneg, 8)]),
   ("Trigonometric functions and rules", [(dtrig, 20)]),
   ("First principles and values", [(dfirst, 10), (dtrig, 10)])], 911112)
