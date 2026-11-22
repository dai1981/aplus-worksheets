# -*- coding: utf-8 -*-
"""
India Class 12 Maths, NCERT Chapter 6: Application of Derivatives (CBSE Unit III Calculus)
  python3 tools/gen_in_maths_c12_application_of_derivatives.py
Rate of change (area, volume, marginal revenue and cost), related rates, increasing and decreasing intervals,
critical points, local maxima and minima by the first and second derivative tests, absolute maximum and minimum on a
closed interval, and simple optimisation problems (own makers).
Wrong answers come from real mistakes: forgetting to multiply by dr/dt, the wrong interval sign of f′, giving the
x-value instead of the maximum value, checking only critical points and not the end points, and the wrong
second derivative sign for a maximum.
"""
import random
from fractions import Fraction as F
from in_sr import U, T2, X, poly
from in_common import num, fv, comma

R = random.Random(912106)
PI = "π"


def one_rate(r):
    k = r.choice(["circ", "sphere", "cube", "related", "mr"])
    if k == "circ":
        rad = r.randint(2, 15)
        return T2("Find the rate of change of the area of a circle with respect to its radius r when r = %d cm." % rad, "%dπ cm²/cm" % (2 * rad),
                  ["%dπ cm²/cm" % (rad * rad), "%dπ cm²/cm" % rad, "%d cm²/cm" % (2 * rad)], "A = πr², so dA/dr = 2πr = <b>%dπ cm²/cm</b>." % (2 * rad))
    if k == "sphere":
        rad = r.randint(1, 10)
        return T2("Find the rate of change of the volume of a sphere with respect to its radius when r = %d cm." % rad, "%dπ cm³/cm" % (4 * rad * rad),
                  ["%sπ cm³/cm" % fv(F(4, 3) * rad ** 3), "%dπ cm³/cm" % (8 * rad), "%dπ cm³/cm" % (rad * rad)], "V = (4/3)πr³, so dV/dr = 4πr² = <b>%dπ cm³/cm</b>." % (4 * rad * rad))
    if k == "cube":
        e, de = r.randint(2, 12), r.randint(1, 5)
        return T2("The edge of a cube is increasing at %d cm/s. How fast is the volume increasing when the edge is %d cm?" % (de, e), "%s cm³/s" % comma(3 * e * e * de),
                  ["%s cm³/s" % comma(3 * e * e), "%s cm³/s" % comma(e ** 3 * de), "%s cm³/s" % comma(3 * e * de)],
                  "V = x³, so dV/dt = 3x² dx/dt = 3 × %d² × %d = <b>%s cm³/s</b>." % (e, de, comma(3 * e * e * de)))
    if k == "related":
        rad, dr = r.randint(2, 12), r.choice([F(1, 2), 1, 2, 3, F(3, 2)])
        v = 2 * rad * dr
        return T2("The radius of a circle is increasing at %s cm/s. How fast is its area increasing when the radius is %d cm?" % (num(dr), rad), "%sπ cm²/s" % num(v),
                  ["%sπ cm²/s" % num(2 * rad), "%sπ cm²/s" % num(rad * rad * dr), "%sπ cm²/s" % num(rad * dr)],
                  "dA/dt = 2πr dr/dt = 2π × %d × %s = <b>%sπ cm²/s</b>." % (rad, num(dr), num(v)))
    a, b, c = r.randint(1, 5), r.randint(1, 20), r.randint(1, 50)
    x0 = r.randint(2, 15)
    return T2("The total revenue from selling %s units is R(%s) = %s rupees. Find the marginal revenue when %s = %d." % (X, X, poly([a, b, c]), X, x0), "₹%s" % comma(2 * a * x0 + b),
              ["₹%s" % comma(a * x0 * x0 + b * x0 + c), "₹%s" % comma(2 * a * x0), "₹%s" % comma(a * x0 + b)],
              "Marginal revenue = dR/d%s = %s; at %s = %d it is <b>₹%s</b>." % (X, poly([2 * a, b]), X, x0, comma(2 * a * x0 + b)))


def cubic(r):
    p, q = sorted(r.sample(range(-5, 6), 2))
    if (p + q) % 2:
        return None
    a = r.choice([1, 2, -1])
    c = r.randint(-9, 9)
    # f' = 3a(x - p)(x - q) -> f = a x³ - (3a/2)(p+q) x² + 3a p q x + c
    cs = [a, F(-3 * a * (p + q), 2), 3 * a * p * q, c]
    if any(F(v).denominator != 1 for v in cs):
        return None
    cs = [int(v) for v in cs]
    return a, p, q, cs


def ev(cs, x):
    v = 0
    for c in cs:
        v = v * x + c
    return v


def one_incr(r):
    t = cubic(r)
    if not t:
        return None
    a, p, q, cs = t
    if a > 0:
        inc, dec = "(−∞, %s) and (%s, ∞)" % (num(p), num(q)), "(%s, %s)" % (num(p), num(q))
    else:
        dec, inc = "(−∞, %s) and (%s, ∞)" % (num(p), num(q)), "(%s, %s)" % (num(p), num(q))
    fac = "%s(%s − %s)(%s − %s)" % (num(3 * a), X, num(p), X, num(q))
    fac = fac.replace("− −", "+ ")
    if r.random() < 0.5:
        return T2("Find the intervals in which f(%s) = %s is increasing." % (X, poly(cs)), inc, [dec, "(%s, ∞)" % num(q), "(−∞, %s)" % num(p)],
                  "f′(%s) = %s. f′ &gt; 0 on <b>%s</b>." % (X, fac, inc))
    return T2("Find the intervals in which f(%s) = %s is decreasing." % (X, poly(cs)), dec, [inc, "(%s, ∞)" % num(q), "(−∞, %s)" % num(p)],
              "f′(%s) = %s. f′ &lt; 0 on <b>%s</b>." % (X, fac, dec))


def one_ext(r):
    t = cubic(r)
    if not t:
        return None
    a, p, q, cs = t
    mx, mn = (p, q) if a > 0 else (q, p)
    k = r.choice(["maxval", "minval", "where"])
    if k == "maxval":
        return T2("Find the local maximum value of f(%s) = %s." % (X, poly(cs)), num(ev(cs, mx)), [num(ev(cs, mn)), num(mx), num(ev(cs, -mx)) if ev(cs, -mx) not in (ev(cs, mx), ev(cs, mn)) else num(ev(cs, mx) + 1)],
                  "f′(%s) = 0 at %s = %s and %s = %s. f″(%s) &lt; 0, so the local maximum is f(%s) = <b>%s</b>." % (X, X, num(p), X, num(q), num(mx), num(mx), num(ev(cs, mx))))
    if k == "minval":
        return T2("Find the local minimum value of f(%s) = %s." % (X, poly(cs)), num(ev(cs, mn)), [num(ev(cs, mx)), num(mn), num(ev(cs, -mn)) if ev(cs, -mn) not in (ev(cs, mx), ev(cs, mn)) else num(ev(cs, mn) - 1)],
                  "f′(%s) = 0 at %s and %s. f″(%s) &gt; 0, so the local minimum is f(%s) = <b>%s</b>." % (X, num(p), num(q), num(mn), num(mn), num(ev(cs, mn))))
    return T2("At which point does f(%s) = %s have a local maximum?" % (X, poly(cs)), "%s = %s" % (X, num(mx)), ["%s = %s" % (X, num(mn)), "%s = %s" % (X, num(-mx)) if mx else "%s = 1" % X, "%s = %s" % (X, num(ev(cs, mx)))],
              "f′ changes from + to − at %s = %s, so f has a local maximum there: <b>%s = %s</b>." % (X, num(mx), X, num(mx)))


def one_abs(r):
    a = r.choice([1, 2, 3, -1, -2])
    h = r.randint(-3, 3)
    k = r.randint(-9, 9)
    lo, hi = h - r.randint(1, 3), h + r.randint(2, 4)
    cs = [a, -2 * a * h, a * h * h + k]
    vals = [ev(cs, lo), ev(cs, hi), k]
    if r.random() < 0.5:
        right = max(vals)
        return T2("Find the absolute maximum value of f(%s) = %s on [%s, %s]." % (X, poly(cs), num(lo), num(hi)), num(right), [num(k) if k != right else num(min(vals)), num(min(vals)) if min(vals) not in (right, k) else num(right + 1), num(hi)],
                  "Check the critical point %s = %s and the end points: f = %s, %s, %s. The largest is <b>%s</b>." % (X, num(h), num(k), num(vals[0]), num(vals[1]), num(right)))
    right = min(vals)
    return T2("Find the absolute minimum value of f(%s) = %s on [%s, %s]." % (X, poly(cs), num(lo), num(hi)), num(right), [num(max(vals)), num(k) if k != right else num(vals[0]) if vals[0] != right else num(right - 1), num(lo)],
              "Compare f at %s = %s, %s and %s: %s, %s, %s. The smallest is <b>%s</b>." % (X, num(h), num(lo), num(hi), num(k), num(vals[0]), num(vals[1]), num(right)))


def one_opt(r):
    k = r.choice(["prod", "rect", "recip", "sq", "fence"])
    if k == "prod":
        s = r.choice([10, 12, 16, 20, 24, 30, 40])
        return T2("Two positive numbers have sum %d. Find the largest possible value of their product." % s, str(s * s // 4), [str(s * s // 2), str(s // 2), str((s // 2 - 1) * (s // 2 + 1))],
                  "P = %s(%d − %s); dP/d%s = %d − 2%s = 0 gives %s = %d, so the maximum product is %d × %d = <b>%d</b>." % (X, s, X, X, s, X, X, s // 2, s // 2, s // 2, s * s // 4))
    if k == "rect":
        p = r.choice([20, 24, 36, 40, 48, 60, 100])
        return T2("A rectangle has perimeter %d cm. What is its largest possible area?" % p, "%d cm²" % (p * p // 16), ["%d cm²" % (p * p // 4), "%d cm²" % (p // 4), "%d cm²" % ((p // 4 - 1) * (p // 4 + 1))],
                  "Area = %s(%d − %s); it is greatest when %s = %d, a square: <b>%d cm²</b>." % (X, p // 2, X, X, p // 4, p * p // 16))
    if k == "recip":
        a = r.choice([1, 4, 9, 16, 25])
        s = int(a ** 0.5)
        return T2("Find the minimum value of %s + %d/%s for %s &gt; 0." % (X, a, X, X) if a != 1 else "Find the minimum value of %s + 1/%s for %s &gt; 0." % (X, X, X), str(2 * s), [str(s), str(a + 1), str(2 * a) if 2 * a != 2 * s else str(2 * s + 1)],
                  "f′ = 1 − %d/%s² = 0 at %s = %d; f″ &gt; 0, so the minimum is %d + %d = <b>%d</b>." % (a, X, X, s, s, s, 2 * s))
    if k == "sq":
        s = r.choice([6, 12, 18, 24, 30])
        x = s // 6
        v = (s - 2 * x) ** 2 * x
        return T2("Equal squares are cut from the corners of a %d cm square sheet, and the sides are folded up to make an open box. What side of square gives the largest volume?" % s, "%d cm" % x,
                  ["%d cm" % (s // 4), "%d cm" % (s // 2), "%d cm" % (s // 3)], "V = %s(%d − 2%s)²; dV/d%s = 0 gives %s = %d (the other root %d gives no box). <b>%d cm</b>, volume %s cm³." % (X, s, X, X, X, x, s // 2, x, comma(v)))
    L = r.choice([40, 60, 80, 100, 120])
    return T2("A farmer has %d m of fencing to fence three sides of a rectangular field; a wall forms the fourth side. What is the largest area he can enclose?" % L, "%s m²" % comma(L * L // 8),
              ["%s m²" % comma(L * L // 16), "%s m²" % comma(L * L // 9), "%s m²" % comma(L * L // 4)],
              "A = %s(%d − 2%s); dA/d%s = 0 gives %s = %d, so A = %d × %d = <b>%s m²</b>." % (X, L, X, X, X, L // 4, L // 4, L // 2, comma(L * L // 8)))


U(12, 6, "application-of-derivatives", 6, "Ca", "Application of Derivatives: Rates, Increasing Functions, Maxima and Minima", "application of derivatives",
  "Applications of derivatives: rate of change of quantities, increasing/decreasing functions, maxima and minima (first derivative test motivated geometrically and second derivative test given as a provable tool); simple problems that illustrate basic principles and understanding of the subject as well as real life situations (summary of the CBSE syllabus)",
  "Class 12 Application of Derivatives worksheet (NCERT Chapter 6): rate of change, related rates, increasing and decreasing functions, local and absolute maxima and minima and optimisation problems. 100 questions with answers.",
  "f′ &gt; 0: increasing; f′ &lt; 0: decreasing; f′ = 0: a critical point.", "Second derivative test: f″ &lt; 0 gives a maximum, f″ &gt; 0 a minimum.",
  "<ul><li>Rate of change: dA/dr, dV/dt and so on. Related rates use the chain rule: dA/dt = (dA/dr)(dr/dt).</li>"
  "<li>f is <b>increasing</b> where f′(x) &gt; 0 and <b>decreasing</b> where f′(x) &lt; 0.</li>"
  "<li>At a critical point (f′ = 0): f″ &lt; 0 gives a local maximum, f″ &gt; 0 a local minimum.</li>"
  "<li>On a closed interval [a, b], the absolute maximum and minimum are among f at the critical points and at a and b.</li></ul>",
  [("Find the local maximum of f(x) = x³ − 3x.", ["f′(x) = 3x² − 3 = 0 at x = ±1", "f″(−1) = −6 &lt; 0"], "f(−1) = 2")],
  ["Forgetting to multiply by dr/dt in related rates.", "Giving the x-value when the question asks for the maximum value.", "Checking only the critical points on a closed interval."],
  [("Can a local maximum be smaller than a local minimum?", "Yes. 'Local' only compares nearby values."),
   ("What if f″ = 0 at a critical point?", "The second derivative test fails; use the first derivative test.")],
  [("Rate of change", [(one_rate, 20)]),
   ("Increasing and decreasing functions", [(one_incr, 20)]),
   ("Local maxima and minima", [(one_ext, 20)]),
   ("Absolute maxima and minima", [(one_abs, 20)]),
   ("Optimisation problems", [(one_opt, 14), (one_rate, 6)])], 912106)
