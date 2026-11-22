# -*- coding: utf-8 -*-
"""
India Class 12 Maths, NCERT Chapter 9: Differential Equations (CBSE Unit III Calculus)
  python3 tools/gen_in_maths_c12_differential_equations.py
Order and degree, the number of arbitrary constants, checking a solution, general and particular solutions,
variables separable, homogeneous equations, and the integrating factor of a linear equation dy/dx + Py = Q
(own makers).
Wrong answers come from real mistakes: the highest power instead of the highest derivative for the order, a degree
for an equation that is not a polynomial in its derivatives, e^P instead of e^∫P dx, and forgetting the constant C.
"""
import random
from fractions import Fraction as F
from in_sr import U, T2, X, sup
from in_common import num, fv

R = random.Random(912109)
Y_ = "<i>y</i>"
D1, D2, D3 = Y_ + "′", Y_ + "″", Y_ + "‴"


def one_od(r):
    cases = [("(%s)² + %s = 0" % (D2, D1), 2, "1"), ("%s + (%s)³ − %s = 0" % (D2, D1, Y_), 2, "1"), ("(%s)⁴ + 3%s%s = 0" % (D3, X, D1), 3, "4"),
             ("%s + 5%s = 0" % (D1, Y_), 1, "1"), ("(d²<i>y</i>/d%s²)³ + (d<i>y</i>/d%s)² + sin(d<i>y</i>/d%s) + 1 = 0" % (X, X, X), 2, "not defined"),
             ("%s + sin %s = 0" % (D1, Y_), 1, "1"), ("(%s)² + (%s)³ + %s = %s" % (D3, D2, D1, Y_), 3, "2"), ("%s + e<sup>%s</sup> = 0" % (D2, D1), 2, "not defined"),
             ("%s · %s + %s = 0" % (Y_, D2, D1), 2, "1"), ("(%s)⁵ + %s = %s²" % (D1, Y_, X), 1, "5"), ("%s‴ + 2%s = 0" % (Y_ + "″", D2) if False else "<i>y</i><sup>(4)</sup> + sin(%s) = 0" % D3, 4, "not defined"),
             ("2%s²%s − 3%s = 0" % (X, D2, Y_), 2, "1"), ("(%s)² + 4%s(%s)³ = 0" % (D2, X, D1), 2, "2")]
    q, o, d = r.choice(cases)
    if r.random() < 0.5:
        return T2("What is the order of the differential equation %s?" % q, str(o), [str(o + 1), d if d not in ("not defined", str(o)) else str(max(1, o - 1)), str(o + 2)],
                  "The order is the order of the highest derivative in the equation: <b>%d</b>." % o)
    wr = [w for w in ["1", "2", "3", "4", "5", "not defined"] if w != d]
    r.shuffle(wr)
    return T2("What is the degree of the differential equation %s?" % q, d, wr[:3],
              ("The equation is not a polynomial in its derivatives, so its degree is <b>not defined</b>." if d == "not defined" else
               "The highest order derivative is raised to the power <b>%s</b> (the equation is a polynomial in its derivatives)." % d))


def one_const(r):
    fams = [("<i>y</i> = A e<sup>%s</sup> + B e<sup>−%s</sup>" % (X, X), 2), ("<i>y</i> = <i>m</i>%s" % X, 1), ("<i>y</i> = <i>m</i>%s + <i>c</i>" % X, 2),
            ("<i>y</i> = A cos %s + B sin %s" % (X, X), 2), ("<i>y</i> = C e<sup>3%s</sup>" % X, 1), ("(%s − <i>a</i>)² + <i>y</i>² = <i>a</i>²" % X, 1),
            ("<i>y</i>² = 4<i>a</i>%s" % X, 1), ("<i>y</i> = <i>a</i>%s² + <i>b</i>%s + <i>c</i>" % (X, X), 3), ("%s²/<i>a</i>² + <i>y</i>²/<i>b</i>² = 1" % X, 2)]
    f, n = r.choice(fams)
    if r.random() < 0.5:
        return T2("What is the order of the differential equation of the family of curves %s (the letters other than %s and <i>y</i> are arbitrary constants)?" % (f, X), str(n),
                  [str(n + 1), str(n + 2), str(n - 1) if n > 1 else "0"],
                  "There %s %d arbitrary constant%s, so we differentiate %d time%s to remove %s: order <b>%d</b>." % ("is" if n == 1 else "are", n, "" if n == 1 else "s", n, "" if n == 1 else "s", "it" if n == 1 else "them", n))
    o = r.randint(1, 4)
    return T2("How many arbitrary constants does the general solution of a differential equation of order %d have?" % o, str(o), [str(o + 1), str(max(o - 1, 0)), "It depends on the degree"],
              "The general solution of an equation of order n has n arbitrary constants: <b>%d</b>." % o)


def one_sep(r):
    k = r.randint(2, 6)
    cases = [("d<i>y</i>/d%s = %d<i>y</i>" % (X, k), "<i>y</i> = C e<sup>%d%s</sup>" % (k, X), ["<i>y</i> = e<sup>%d%s</sup> + C" % (k, X), "<i>y</i> = %d%s + C" % (k, X), "<i>y</i> = C e<sup>%s/%d</sup>" % (X, k)]),
             ("d<i>y</i>/d%s = %s/<i>y</i>" % (X, X), "<i>y</i>² − %s² = C" % X, ["<i>y</i>² + %s² = C" % X, "<i>y</i> = %s + C" % X, "<i>y</i> = C%s" % X]),
             ("d<i>y</i>/d%s = −%s/<i>y</i>" % (X, X), "%s² + <i>y</i>² = C" % X, ["<i>y</i>² − %s² = C" % X, "<i>y</i> = −%s + C" % X, "%s<i>y</i> = C" % X]),
             ("d<i>y</i>/d%s = 1 + <i>y</i>²" % X, "tan<sup>−1</sup> <i>y</i> = %s + C" % X, ["<i>y</i> = %s + <i>y</i>³/3 + C" % X, "log(1 + <i>y</i>²) = %s + C" % X, "<i>y</i> = tan<sup>−1</sup> %s + C" % X]),
             ("d<i>y</i>/d%s = %d%s<i>y</i>" % (X, 2 * k, X), "<i>y</i> = C e<sup>%d%s²</sup>" % (k, X), ["<i>y</i> = C e<sup>%d%s²</sup>" % (2 * k, X), "<i>y</i> = %d%s² + C" % (k, X), "<i>y</i> = C e<sup>%d%s</sup>" % (2 * k, X)]),
             ("d<i>y</i>/d%s = e<sup>%s + <i>y</i></sup>" % (X, X), "e<sup>%s</sup> + e<sup>−<i>y</i></sup> = C" % X, ["e<sup>%s</sup> − e<sup>−<i>y</i></sup> = C" % X, "e<sup><i>y</i></sup> = e<sup>%s</sup> + C" % X, "<i>y</i> = %s + C" % X]),
             ("d<i>y</i>/d%s = <i>y</i>/%s" % (X, X), "<i>y</i> = C%s" % X, ["<i>y</i> = %s + C" % X, "<i>y</i> = C/%s" % X, "<i>y</i>² = %s² + C" % X]),
             ("d<i>y</i>/d%s = %s²<i>y</i>" % (X, X), "<i>y</i> = C e<sup>%s³/3</sup>" % X, ["<i>y</i> = C e<sup>%s³</sup>" % X, "<i>y</i> = %s³/3 + C" % X, "<i>y</i> = C e<sup>2%s</sup>" % X])]
    q, right, wr = r.choice(cases)
    return T2("Find the general solution of %s." % q, right, wr, "Separate the variables and integrate both sides: <b>%s</b>." % right)


def one_part(r):
    a, b, c = r.randint(1, 4), r.randint(-5, 5), r.randint(-9, 9)
    x1 = r.randint(1, 4)
    # dy/dx = 2a x + b, y(0) = c ; find y(x1)
    v = a * x1 * x1 + b * x1 + c
    rhs = "%d%s" % (2 * a, X) + ("" if b == 0 else (" + %d" % b if b > 0 else " − %d" % -b))
    return T2("d<i>y</i>/d%s = %s and <i>y</i> = %s when %s = 0. Find <i>y</i> when %s = %d." % (X, rhs, num(c), X, X, x1), num(v),
              [num(v - c), num(2 * a * x1 + b), num(a * x1 * x1 + b * x1) if c == 0 else num(v + c)],
              "<i>y</i> = %d%s²%s + C, and <i>y</i>(0) = %s gives C = %s. So <i>y</i>(%d) = <b>%s</b>." % (a, X, ("" if b == 0 else (" + %d%s" % (b, X) if b > 0 else " − %d%s" % (-b, X))), num(c), num(c), x1, num(v)))


E = lambda t: "e<sup>%s</sup>" % t
IF = [("2", E("2" + X), [E("2"), E("−2" + X), "2" + X]), ("1/" + X, X, ["log " + X, "1/" + X, E(X)]), ("2/" + X, X + "²", [E("2/" + X), "1/" + X + "²", "2 log " + X]),
      ("tan " + X, "sec " + X, [E("tan " + X), "cos " + X, "sec² " + X]), ("−1/" + X, "1/" + X, [X, "−log " + X, E("−" + X)]), ("2" + X, E(X + "²"), [E("2" + X), "2" + X, E("−" + X + "²")]),
      ("cot " + X, "sin " + X, ["cos " + X, E("cot " + X), "cosec " + X]), ("3", E("3" + X), [E("3"), E("−3" + X), "3" + X]), ("−1", E("−" + X), [E(X), E("−1"), "−" + X]),
      ("3/" + X, X + "³", ["3 log " + X, "1/" + X + "³", E("3/" + X)]), ("−2", E("−2" + X), [E("2" + X), E("−2"), "−2" + X]), ("1", E(X), [E("−" + X), "1", X])]


def one_if(r):
    P, right, wr = r.choice(IF)
    Q = r.choice(["%s²" % X, "sin %s" % X, "e<sup>%s</sup>" % X, "4", X, "cos %s" % X, "%s³" % X])
    neg = P.startswith("−")
    body = P[1:] if neg else P
    term = (body if body.replace("2", "").replace("3", "") == "" or body in ("1",) else "(%s)" % body)
    if body == "1":
        term = ""
    lhs = "d<i>y</i>/d%s %s %s<i>y</i>" % (X, "−" if neg else "+", term)
    return T2("Find the integrating factor of %s = %s." % (lhs, Q), right, wr,
              "For d<i>y</i>/d%s + P<i>y</i> = Q, I.F. = e<sup>∫P d%s</sup> with P = %s, so I.F. = <b>%s</b>." % (X, X, P, right))


def one_hom(r):
    k = r.choice(["which", "sub"])
    if k == "which":
        good = r.choice(["(%s² + <i>y</i>²) d%s − 2%s<i>y</i> d<i>y</i> = 0" % (X, X, X), "d<i>y</i>/d%s = (%s + <i>y</i>)/%s" % (X, X, X), "%s d<i>y</i> − <i>y</i> d%s = √(%s² + <i>y</i>²) d%s" % (X, X, X, X),
                         "d<i>y</i>/d%s = (%s² + <i>y</i>²)/(%s<i>y</i>)" % (X, X, X)])
        bad = ["d<i>y</i>/d%s = (%s + <i>y</i> + 1)/%s" % (X, X, X), "d<i>y</i>/d%s = %s² + <i>y</i>" % (X, X), "d<i>y</i>/d%s = (%s<i>y</i> + 1)/<i>y</i>" % (X, X), "d<i>y</i>/d%s = sin %s + <i>y</i>" % (X, X)]
        return T2("Which differential equation is homogeneous?", good, r.sample(bad, 3),
                  "In <b>%s</b>, replacing %s by λ%s and <i>y</i> by λ<i>y</i> leaves the right side (or each term's degree) unchanged." % (good, X, X))
    return T2("Which substitution is used to solve a homogeneous differential equation d<i>y</i>/d%s = F(<i>y</i>/%s)?" % (X, X), "<i>y</i> = <i>v</i>%s" % X,
              ["<i>y</i> = %s + <i>v</i>" % X, "<i>v</i> = %s<i>y</i>" % X, "<i>y</i> = e<sup><i>v</i></sup>"], "Put <b><i>y</i> = <i>v</i>%s</b>, so d<i>y</i>/d%s = <i>v</i> + %s d<i>v</i>/d%s." % (X, X, X, X))


U(12, 9, "differential-equations", 9, "Ca", "Differential Equations: Order, Degree, Separable and Linear Equations", "differential equations",
  "Definition, order and degree, general and particular solutions of a differential equation; solution of differential equations by method of separation of variables, solutions of homogeneous differential equations of first order and first degree; solutions of linear differential equations of the type dy/dx + py = q, where p and q are functions of x or constants, and dx/dy + px = q, where p and q are functions of y or constants (summary of the CBSE syllabus)",
  "Class 12 Differential Equations worksheet (NCERT Chapter 9): order and degree, arbitrary constants, variables separable, particular solutions, homogeneous equations and integrating factors. 100 questions with answers.",
  "Order = highest derivative; degree = its power (if the equation is a polynomial in derivatives).", "For dy/dx + Py = Q, I.F. = e^∫P dx.",
  "<ul><li><b>Order</b>: the order of the highest derivative. <b>Degree</b>: the power of that derivative, defined only when the equation is a polynomial in its derivatives.</li>"
  "<li>The general solution of an equation of order n has n arbitrary constants; a particular solution uses given values to fix them.</li>"
  "<li><b>Variables separable</b>: write g(<i>y</i>) d<i>y</i> = f(<i>x</i>) d<i>x</i> and integrate both sides.</li>"
  "<li><b>Homogeneous</b>: d<i>y</i>/d<i>x</i> = F(<i>y</i>/<i>x</i>); put <i>y</i> = v<i>x</i>.</li>"
  "<li><b>Linear</b>: d<i>y</i>/d<i>x</i> + P<i>y</i> = Q; I.F. = e<sup>∫P d<i>x</i></sup>, and <i>y</i>(I.F.) = ∫Q(I.F.) d<i>x</i> + C.</li></ul>",
  [("Solve d<i>y</i>/d<i>x</i> + <i>y</i>/<i>x</i> = <i>x</i>².", ["I.F. = e<sup>∫1/<i>x</i> d<i>x</i></sup> = <i>x</i>", "<i>xy</i> = ∫<i>x</i>³ d<i>x</i> = <i>x</i>⁴/4 + C"], "<i>y</i> = <i>x</i>³/4 + C/<i>x</i>")],
  ["Taking the highest power as the order.", "Giving a degree for an equation with sin(dy/dx) in it.", "Using e^P instead of e^∫P dx for the integrating factor."],
  [("Does every differential equation have a degree?", "No. If it is not a polynomial in its derivatives (for example it has sin(y′)), the degree is not defined."),
   ("What is a particular solution?", "A solution with no arbitrary constants, found using given conditions.")],
  [("Order and degree", [(one_od, 20)]),
   ("General solutions and constants", [(one_const, 10), (one_part, 10)]),
   ("Variables separable", [(one_sep, 8), (one_part, 12)]),
   ("Homogeneous equations and integrating factors", [(one_hom, 2), (one_od, 2), (one_if, 16)]),
   ("Linear equations", [(one_if, 20)])], 912109)
