# -*- coding: utf-8 -*-
"""
India Class 12 Maths, NCERT Chapter 5: Continuity and Differentiability (CBSE Unit III Calculus)
  python3 tools/gen_in_maths_c12_continuity_and_differentiability.py
Continuity of piecewise functions and finding k, left- and right-hand limits, the chain rule, derivatives of inverse
trigonometric, exponential and logarithmic functions, implicit and parametric differentiation, logarithmic
differentiation, and second order derivatives (own makers and TX Precalculus makers).
Wrong answers come from real mistakes: forgetting the inner derivative in the chain rule, d/dx(log x) = 1/x for
log(ax + b) without the a, dy/dx = −y/x for x² + y² = r², (dx/dt)/(dy/dt) for a parametric curve, and
d/dx(xˣ) = x·xˣ⁻¹.
"""
import random
from fractions import Fraction as F
from in_sr import U, T2, use, X, sup
from in_common import num, fv

R = random.Random(912105)
FX = [("behavior", "behaviour")]
pwk = use(__import__("gen_ustx_math_pc_piecewise_step"), "one_pwk", R, FX)
sides = use(__import__("gen_ustx_math_pc_discontinuities"), "one_sides", R, FX)
T_ = "<i>t</i>"
Yv = "<i>y</i>"


def lin(a, b, v=X):
    s = ("" if a == 1 else (MIN + "" if a == -1 else num(a))) + v
    return s + ("" if b == 0 else (" + %d" % b if b > 0 else " − %d" % -b))


MIN = "−"


def cf(c):
    return "" if c == 1 else (MIN if c == -1 else num(c))


def one_chain(r):
    a = r.choice([2, 3, 4, 5, -2, -3])
    b = r.randint(-6, 6)
    u = lin(a, b)
    k = r.choice(["sin", "cos", "pow", "exp", "log", "sqrt", "sinsq"])
    if k == "sin":
        right = "%scos(%s)" % (cf(a), u)
        return T2("Find d<i>y</i>/d%s if <i>y</i> = sin(%s)." % (X, u), right, ["cos(%s)" % u, "%scos(%s)" % (cf(-a), u), "%ssin(%s)" % (cf(a), u)],
                  "Chain rule: cos(%s) × d/d%s(%s) = <b>%s</b>." % (u, X, u, right))
    if k == "cos":
        right = "%ssin(%s)" % (cf(-a), u)
        return T2("Find d<i>y</i>/d%s if <i>y</i> = cos(%s)." % (X, u), right, ["−sin(%s)" % u, "%ssin(%s)" % (cf(a), u), "%scos(%s)" % (cf(-a), u)],
                  "−sin(%s) × %s = <b>%s</b>." % (u, num(a), right))
    if k == "pow":
        n = r.randint(2, 7)
        right = "%s(%s)%s" % (num(n * a), u, sup(n - 1) if n > 2 else "")
        return T2("Find d<i>y</i>/d%s if <i>y</i> = (%s)%s." % (X, u, sup(n)), right, ["%d(%s)%s" % (n, u, sup(n - 1) if n > 2 else ""), "%s(%s)%s" % (num(n * a), u, sup(n)), "%s(%s)%s" % (num(a), u, sup(n - 1) if n > 2 else "")],
                  "n(%s)ⁿ⁻¹ × %s = <b>%s</b>." % (u, num(a), right))
    if k == "exp":
        right = "%se<sup>%s</sup>" % (cf(a), u)
        return T2("Find d<i>y</i>/d%s if <i>y</i> = e<sup>%s</sup>." % (X, u), right, ["e<sup>%s</sup>" % u, "(%s)e<sup>%s</sup>" % (u, lin(a, b - 0) if False else u) if False else "%se<sup>%s</sup>" % (cf(a), lin(a, b - a)), "%se<sup>%s</sup>" % (cf(b) if b else "", u) if b not in (0, 1, a) else "%se<sup>%s</sup>" % (num(a * a), u)],
                  "d/d%s(e<sup>u</sup>) = e<sup>u</sup> × u′, and u′ = %s: <b>%s</b>." % (X, num(a), right))
    if k == "log":
        if a < 0:
            return None
        right = "%s/(%s)" % (num(a), u)
        return T2("Find d<i>y</i>/d%s if <i>y</i> = log(%s)." % (X, u), right, ["1/(%s)" % u, "%s/%s" % (num(a), X), "1/%s" % num(a)],
                  "(1/(%s)) × %s = <b>%s</b>." % (u, num(a), right))
    if k == "sinsq":
        c = r.randint(2, 5)
        right = "%d sin %d%s" % (c, 2 * c, X) if False else "%s sin %s cos %s" % (num(2 * c), "%d%s" % (c, X), "%d%s" % (c, X))
        return T2("Find d<i>y</i>/d%s if <i>y</i> = sin²(%d%s)." % (X, c, X), right, ["2 sin %d%s cos %d%s" % (c, X, c, X), "2 sin %d%s" % (c, X), "%d cos² %d%s" % (c, c, X)],
                  "2 sin(%d%s) × cos(%d%s) × %d = <b>%s</b>." % (c, X, c, X, c, right))
    if a < 0 or b < 0:
        return None
    right = ("%s/√(%s)" % (a // 2, u)) if a % 2 == 0 else "%s/(2√(%s))" % (num(a), u)
    return T2("Find d<i>y</i>/d%s if <i>y</i> = √(%s)." % (X, u), right, ["1/(2√(%s))" % u, "%s/√(%s)" % (num(a), u), "%s√(%s)" % (num(a), u)],
              "(1/(2√(%s))) × %s = <b>%s</b>." % (u, num(a), right))


def one_inv(r):
    a = r.choice([2, 3, 4, 5])
    k = r.choice(["sin", "cos", "tan", "tan_lin"])
    if k == "sin":
        right = "%d/√(1 − %d%s²)" % (a, a * a, X)
        return T2("Find d<i>y</i>/d%s if <i>y</i> = sin<sup>−1</sup>(%d%s)." % (X, a, X), right, ["1/√(1 − %d%s²)" % (a * a, X), "%d/√(1 − %d%s²)" % (a, a, X), "%d/(1 + %d%s²)" % (a, a * a, X)],
                  "d/du(sin<sup>−1</sup> u) = 1/√(1 − u²) with u = %d%s, times u′ = %d: <b>%s</b>." % (a, X, a, right))
    if k == "cos":
        return T2("Find d/d%s (cos<sup>−1</sup> %s)." % (X, X), "−1/√(1 − %s²)" % X, ["1/√(1 − %s²)" % X, "−1/(1 + %s²)" % X, "−sin<sup>−1</sup> %s" % X],
                  "d/d%s(cos<sup>−1</sup> %s) = <b>−1/√(1 − %s²)</b>." % (X, X, X))
    if k == "tan":
        right = "%d/(1 + %d%s²)" % (a, a * a, X)
        return T2("Find d<i>y</i>/d%s if <i>y</i> = tan<sup>−1</sup>(%d%s)." % (X, a, X), right, ["1/(1 + %d%s²)" % (a * a, X), "%d/(1 + %d%s²)" % (a, a, X), "%d/√(1 − %d%s²)" % (a, a * a, X)],
                  "1/(1 + (%d%s)²) × %d = <b>%s</b>." % (a, X, a, right))
    return T2("Find d<i>y</i>/d%s if <i>y</i> = tan<sup>−1</sup>(%s²)." % (X, X), "2%s/(1 + %s⁴)" % (X, X), ["1/(1 + %s⁴)" % X, "2%s/(1 + %s²)" % (X, X), "1/(1 + %s²)" % X],
              "1/(1 + (%s²)²) × 2%s = <b>2%s/(1 + %s⁴)</b>." % (X, X, X, X))


def one_impl(r):
    k = r.choice(["circle", "xy", "mix", "line"])
    if k == "circle":
        a, b = r.randint(1, 5), r.randint(1, 5)
        right = fv(F(-a, b)) if True else ""
        right = "−%s%s/%s" % ("" if a == 1 else a, X, ("" if b == 1 else b) + "<i>y</i>")
        return T2("Find d<i>y</i>/d%s if %s%s² + %s<i>y</i>² = %d." % (X, "" if a == 1 else a, X, "" if b == 1 else b, r.randint(5, 50)), right,
                  [right[1:], "−%s<i>y</i>/%s" % ("" if a == 1 else a, ("" if b == 1 else b) + X), "−%s%s/%s" % ("" if b == 1 else b, X, ("" if a == 1 else a) + "<i>y</i>") if a != b else "−<i>y</i>/%s" % X],
                  "Differentiate both sides: %d%s + %d<i>y</i>(d<i>y</i>/d%s) = 0, so d<i>y</i>/d%s = <b>%s</b>." % (2 * a, X, 2 * b, X, X, right))
    if k == "xy":
        c = r.randint(2, 20)
        return T2("Find d<i>y</i>/d%s if %s<i>y</i> = %d." % (X, X, c), "−<i>y</i>/%s" % X, ["<i>y</i>/%s" % X, "−%s/<i>y</i>" % X, "%d/%s" % (c, X)],
                  "Product rule: <i>y</i> + %s(d<i>y</i>/d%s) = 0, so d<i>y</i>/d%s = <b>−<i>y</i>/%s</b>." % (X, X, X, X))
    if k == "mix":
        return T2("Find d<i>y</i>/d%s if %s² + %s<i>y</i> + <i>y</i>² = 100." % (X, X, X), "−(2%s + <i>y</i>)/(%s + 2<i>y</i>)" % (X, X),
                  ["−(2%s + <i>y</i>)/(2<i>y</i>)" % X, "(2%s + <i>y</i>)/(%s + 2<i>y</i>)" % (X, X), "−%s/<i>y</i>" % X],
                  "2%s + (<i>y</i> + %s<i>y</i>′) + 2<i>y</i><i>y</i>′ = 0, so <i>y</i>′ = <b>−(2%s + <i>y</i>)/(%s + 2<i>y</i>)</b>." % (X, X, X, X))
    a, b = r.choice([k for k in range(-6, 7) if k]), r.choice([k for k in range(1, 7)])
    over = lambda t: "(%s)/%d" % (t, b) if b != 1 else t
    sg = lambda pos: ("−" if pos else "+")
    right = over("cos %s %s %s" % (X, sg(a > 0), num(abs(a))))
    return T2("Find d<i>y</i>/d%s if %s%s + %s<i>y</i> = sin %s." % (X, num(a) if a not in (1, -1) else ("" if a == 1 else "−"), X, "" if b == 1 else b, X), right,
              [over("cos %s" % X), over("cos %s %s %s" % (X, sg(a < 0), num(abs(a)))), over("sin %s %s %s" % (X, sg(a > 0), num(abs(a))))],
              "%s + %s<i>y</i>′ = cos %s, so <i>y</i>′ = <b>%s</b>." % (num(a), "" if b == 1 else b, X, right))


def one_param(r):
    k = r.choice(["at", "circ", "ell", "t2t3", "t"])
    a = r.randint(2, 6)
    if k == "at":
        return T2("Find d<i>y</i>/d%s if %s = %d%s², <i>y</i> = %d%s." % (X, X, a, T_, 2 * a, T_), "1/%s" % T_, [T_, "%d%s" % (a, T_), "2/%s" % T_],
                  "d%s/d%s = %d%s and d<i>y</i>/d%s = %d, so d<i>y</i>/d%s = %d ÷ %d%s = <b>1/%s</b>." % (X, T_, 2 * a, T_, T_, 2 * a, X, 2 * a, 2 * a, T_, T_))
    if k == "circ":
        return T2("Find d<i>y</i>/d%s if %s = %d cos θ, <i>y</i> = %d sin θ." % (X, X, a, a), "−cot θ", ["cot θ", "−tan θ", "tan θ"],
                  "d%s/dθ = −%d sin θ and d<i>y</i>/dθ = %d cos θ, so d<i>y</i>/d%s = <b>−cot θ</b>." % (X, a, a, X))
    if k == "ell":
        b = r.choice([k for k in range(2, 8) if k != a])
        return T2("Find d<i>y</i>/d%s if %s = %d cos θ, <i>y</i> = %d sin θ." % (X, X, a, b), "−%s cot θ" % fv(F(b, a)), ["−%s cot θ" % fv(F(a, b)), "%s cot θ" % fv(F(b, a)), "−%s tan θ" % fv(F(b, a))],
                  "d<i>y</i>/d%s = (%d cos θ) ÷ (−%d sin θ) = <b>−%s cot θ</b>." % (X, b, a, fv(F(b, a))))
    if k == "t2t3":
        return T2("Find d<i>y</i>/d%s if %s = %s², <i>y</i> = %s³." % (X, X, T_, T_), "3%s/2" % T_, ["2/(3%s)" % T_, "3%s²" % T_, "%s/2" % T_],
                  "d<i>y</i>/d%s = 3%s² ÷ 2%s = <b>3%s/2</b>." % (X, T_, T_, T_))
    p, q = r.randint(1, 5), r.randint(1, 5)
    return T2("Find d<i>y</i>/d%s if %s = %d%s + 1, <i>y</i> = %d%s² − 1." % (X, X, p, T_, q, T_), "%s%s" % (fv(F(2 * q, p)) if F(2 * q, p) != 1 else "", T_),
              ["%s%s" % (fv(F(p, 2 * q)) if F(p, 2 * q) != 1 else "", T_) if F(p, 2 * q) != F(2 * q, p) else "%d%s" % (2 * q, T_), "%d%s" % (2 * q, T_) if p != 1 else "%d%s" % (q, T_), fv(F(2 * q, p))],
              "d<i>y</i>/d%s = %d%s ÷ %d = <b>%s%s</b>." % (X, 2 * q, T_, p, fv(F(2 * q, p)) if F(2 * q, p) != 1 else "", T_))


def one_second(r):
    k = r.choice(["poly", "exp", "sin", "log", "xx"])
    if k == "poly":
        a, b, c = r.randint(1, 5), r.randint(-6, 6), r.randint(-9, 9)
        n = r.choice([3, 4])
        f = "%s%s%s %s %s%s" % ("" if a == 1 else a, X, sup(n), "+" if b >= 0 else "−", abs(b), X + "²") + (" + %d%s" % (c, X) if c > 0 else (" − %d%s" % (-c, X) if c < 0 else ""))
        d2 = "%s%s %s %d" % (num(a * n * (n - 1)), X + (sup(n - 2) if n > 3 else ""), "+" if b >= 0 else "−", abs(2 * b))
        return T2("Find d²<i>y</i>/d%s² if <i>y</i> = %s." % (X, f), d2, ["%s%s %s %d%s %s %s" % (num(a * n), X + sup(n - 1), "+" if b >= 0 else "−", abs(2 * b), X, "+" if c >= 0 else "−", num(abs(c))),
                                                                     "%s%s %s %d" % (num(a * n * (n - 1)), X + (sup(n - 1) if n > 2 else ""), "+" if b >= 0 else "−", abs(2 * b)), "%s%s" % (num(a * n * (n - 1)), X + (sup(n - 2) if n > 3 else ""))],
                  "Differentiate twice: <b>%s</b>." % d2)
    if k == "exp":
        m = r.choice([2, 3, 4, 5, -2, -3])
        return T2("Find d²<i>y</i>/d%s² if <i>y</i> = e<sup>%s%s</sup>." % (X, num(m), X), "%se<sup>%s%s</sup>" % (num(m * m), num(m), X),
                  ["%se<sup>%s%s</sup>" % (num(m), num(m), X), "e<sup>%s%s</sup>" % (num(m), X), "%se<sup>%s%s</sup>" % (num(2 * m), num(m), X)],
                  "Each derivative multiplies by %s, so the second gives <b>%se<sup>%s%s</sup></b>." % (num(m), num(m * m), num(m), X))
    if k == "sin":
        m = r.randint(2, 6)
        fn = r.choice(["sin", "cos"])
        return T2("Find d²<i>y</i>/d%s² if <i>y</i> = %s %d%s." % (X, fn, m, X), "−%d %s %d%s" % (m * m, fn, m, X),
                  ["%d %s %d%s" % (m * m, fn, m, X), "−%d %s %d%s" % (m, fn, m, X), "−%d %s %d%s" % (m * m, "cos" if fn == "sin" else "sin", m, X)],
                  "d²<i>y</i>/d%s² = −%d² %s %d%s = <b>−%d %s %d%s</b>, so <i>y</i>″ + %d<i>y</i> = 0." % (X, m, fn, m, X, m * m, fn, m, X, m * m))
    if k == "log":
        return T2("Find d²<i>y</i>/d%s² if <i>y</i> = log %s." % (X, X), "−1/%s²" % X, ["1/%s²" % X, "1/%s" % X, "−1/%s" % X],
                  "<i>y</i>′ = 1/%s = %s<sup>−1</sup>, so <i>y</i>″ = <b>−1/%s²</b>." % (X, X, X))
    return T2("Find d<i>y</i>/d%s if <i>y</i> = %s<sup>%s</sup>." % (X, X, X), "%s<sup>%s</sup>(1 + log %s)" % (X, X, X), ["%s · %s<sup>%s − 1</sup>" % (X, X, X), "%s<sup>%s</sup> log %s" % (X, X, X), "%s<sup>%s</sup>" % (X, X)],
              "Take logs: log <i>y</i> = %s log %s, so (1/<i>y</i>)<i>y</i>′ = log %s + 1 and <i>y</i>′ = <b>%s<sup>%s</sup>(1 + log %s)</b>." % (X, X, X, X, X, X))


U(12, 5, "continuity-and-differentiability", 5, "Ca", "Continuity and Differentiability: Chain Rule, Implicit and Parametric Derivatives", "continuity and differentiability",
  "Continuity and differentiability, chain rule, derivative of inverse trigonometric functions, like sin⁻¹ x, cos⁻¹ x and tan⁻¹ x, derivative of implicit functions; concept of exponential and logarithmic functions; derivatives of logarithmic and exponential functions; logarithmic differentiation, derivative of functions expressed in parametric forms; second order derivatives (summary of the CBSE syllabus)",
  "Class 12 Continuity and Differentiability worksheet (NCERT Chapter 5): continuity of piecewise functions, chain rule, inverse trigonometric, exponential and log derivatives, implicit, parametric and logarithmic differentiation and second derivatives. 100 questions with answers.",
  "Chain rule: dy/dx = (dy/du)(du/dx).", "f is continuous at a when the left limit, the right limit and f(a) are equal.",
  "<ul><li>f is <b>continuous</b> at c if lim<sub>x→c</sub> f(x) = f(c): both one-sided limits must equal f(c).</li>"
  "<li><b>Chain rule</b>: d/dx f(g(x)) = f′(g(x)) g′(x). Example: d/dx sin(3x) = 3 cos 3x.</li>"
  "<li>d/dx(e<sup>x</sup>) = e<sup>x</sup>, d/dx(log x) = 1/x, d/dx(sin<sup>−1</sup> x) = 1/√(1 − x²), d/dx(tan<sup>−1</sup> x) = 1/(1 + x²).</li>"
  "<li>Implicit: differentiate both sides, treating <i>y</i> as a function of x. Parametric: dy/dx = (dy/dt) ÷ (dx/dt).</li>"
  "<li>For <i>y</i> = f(x)<sup>g(x)</sup>, take logs first (logarithmic differentiation).</li></ul>",
  [("Find dy/dx if y = sin(x²).", ["Outer: cos(x²); inner: x² with derivative 2x"], "2x cos(x²)")],
  ["Forgetting to multiply by the derivative of the inside.", "Using (dx/dt) ÷ (dy/dt) for a parametric curve.", "Writing d/dx(xˣ) = x · xˣ⁻¹."],
  [("Is every continuous function differentiable?", "No. |x| is continuous at 0 but not differentiable there."),
   ("What does log mean in NCERT calculus?", "The natural logarithm, base e.")],
  [("Continuity", [(pwk, 12), (sides, 8)]),
   ("Chain rule", [(one_chain, 20)]),
   ("Inverse trigonometric, implicit functions", [(one_inv, 8), (one_impl, 12)]),
   ("Parametric and logarithmic differentiation", [(one_param, 14), (one_second, 6)]),
   ("Second order derivatives and mixed problems", [(one_second, 10), (one_chain, 10)])], 912105)
