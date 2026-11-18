# -*- coding: utf-8 -*-
"""
SG Secondary 3 Maths: Graphs of Power and Exponential Functions (MOE syllabus N6)
  python3 tools/gen_sg_maths_s3_power_and_exponential_graphs.py
Graphs of y = axⁿ for n = −2, −1, 0, 1, 2, 3 and simple sums, tables of values, exponential graphs y = kaˣ,
reading graphs, and estimating the gradient of a curve by drawing a tangent.
Wrong answers come from real mistakes: mixing up y = 1/x and y = 1/x², thinking y = 2ˣ crosses the x-axis,
taking 2ˣ as 2x, squaring a negative number wrongly, and using run ÷ rise for the gradient.
"""
import random
from fractions import Fraction as F
from sg_sec import num, S, make, lesson, collect, T, expr, fr, fig, MINUS
from pc_common import curve_svg

R = random.Random(830800)
X = "<i>x</i>"
Y = "<i>y</i>"


def fv(v):
    v = F(v)
    return num(v) if v.denominator == 1 else (MINUS if v < 0 else "") + fr(abs(v.numerator), v.denominator)


def pw(n, a=1):
    """a x^n as HTML"""
    co = "" if a == 1 else (MINUS if a == -1 else num(a))
    if n == 0:
        return num(a)
    if n == 1:
        return co + X
    if n > 1:
        return co + X + "<sup>%d</sup>" % n
    top = num(a)
    return fr(top, X if n == -1 else X + "<sup>%d</sup>" % (-n))


def g(fn, lo=-4, hi=4, ylo=-8, yhi=8, slant=(), label="graph", unit=22, at=None):
    svg = curve_svg(fn, lo, hi, ylo, yhi, unit=unit, label=label)
    add = []
    Xp = lambda x: 22 + (x - lo) * unit
    Yp = lambda y: 22 + (yhi - y) * unit
    for m, b in slant:
        # clip the line to the grid
        pts = []
        for x in (lo, hi):
            y = m * x + b
            if ylo <= y <= yhi:
                pts.append((x, y))
        if m:
            for y in (ylo, yhi):
                x = (y - b) / m
                if lo <= x <= hi:
                    pts.append((x, y))
        pts = sorted(set((round(x, 6), round(y, 6)) for x, y in pts))
        if len(pts) >= 2:
            (x1, y1), (x2, y2) = pts[0], pts[-1]
            add.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#c0392b' stroke-width='2' stroke-dasharray='6 5'/>" % (Xp(x1), Yp(y1), Xp(x2), Yp(y2)))
    if at:
        add.append("<circle cx='%.1f' cy='%.1f' r='4.5' fill='#c0392b'/>" % (Xp(at[0]), Yp(at[1])))
    return fig(svg.replace("</g></svg>", "".join(add) + "</g></svg>"))


SHAPES = [(3, "a cubic curve through the origin, rising from bottom left to top right"),
          (2, "a ∪-shaped parabola with its minimum at the origin"),
          (1, "a straight line through the origin"),
          (0, "a horizontal straight line"),
          (-1, "two separate curves in opposite quadrants that approach both axes"),
          (-2, "two separate curves both above the x-axis that approach both axes")]


# ------------------------------------------------------------ set 1: recognising the graph
def one_shape(r):
    n = r.choice([3, 2, -1, -2, -1, -2, 3])
    a = r.choice([1, 2, 3, 4, -1, -2, -3])
    fn = lambda x: a * x ** n if x != 0 or n >= 0 else None
    lbl = "graph of y = %s x to the power %d" % (a, n)
    right = "%s = %s" % (Y, pw(n, a))
    wr_n = [m for m in [3, 2, -1, -2, 1] if m != n]
    r.shuffle(wr_n)
    wr = ["%s = %s" % (Y, pw(m, a)) for m in wr_n[:2]] + ["%s = %s" % (Y, pw(n, -a))]
    why = {3: "an S-shaped cubic", 2: "a parabola", -1: "a reciprocal graph in two opposite quadrants", -2: "a graph with both branches on the same side of the x-axis"}[n]
    return T("Which equation could this graph have?%s" % g(fn, label=lbl), right, wr,
             "It is %s%s, so <b>%s</b>." % (why, ", turned upside down by the negative coefficient" if a < 0 else "", right))


# ------------------------------------------------------------ set 2: tables of values and simple sums
def one_table(r):
    kind = r.choice(["recip", "cube", "sum", "sum", "inv2"])
    x = r.choice([-4, -3, -2, -1, 1, 2, 3, 4])
    if kind == "recip":
        a = r.choice([2, 4, 6, 8, 12, -6])
        y = F(a, x)
        f = "%s = %s" % (Y, pw(-1, a))
        wr = [fv(a * x), fv(-y), fv(F(x, a))]
    elif kind == "inv2":
        a = r.choice([4, 8, 12, 16, 18])
        y = F(a, x * x)
        f = "%s = %s" % (Y, pw(-2, a))
        wr = [fv(-y), fv(F(a, 2 * x)), fv(F(a, x))]
    elif kind == "cube":
        a = r.choice([1, 2, F(1, 2), -1])
        y = a * x ** 3
        f = "%s = %s" % (Y, (fv(a) if a not in (1, -1) else ("" if a == 1 else MINUS)) + X + "<sup>3</sup>")
        wr = [fv(-y), fv(a * 3 * x), fv(a * x * x)]
    else:
        p, q = r.choice([(1, 4), (1, 6), (2, 8), (1, 12), (2, 1)])
        # y = p x² + q/x  or x³ − q x
        if r.random() < 0.5:
            y = p * x * x + F(q, x)
            f = "%s = %s + %s" % (Y, pw(2, p), pw(-1, q))
            wr = [fv(p * x * x - F(q, x)), fv(2 * p * x + F(q, x)), fv(p * x * x + q * x)]
        else:
            y = x ** 3 - q * x
            f = "%s = %s %s %s" % (Y, X + "<sup>3</sup>", MINUS, pw(1, q))
            wr = [fv(-x ** 3 - q * x), fv(3 * x - q * x), fv(x ** 3 + q * x)]
    if len({fv(y)} | set(wr)) < 4:
        return None
    return T("Find the value of %s when %s = %s for %s." % (Y, X, num(x), f), fv(y), wr,
             "Substitute %s = %s carefully, using brackets for negative numbers: %s = <b>%s</b>." % (X, num(x), Y, fv(y)))


# ------------------------------------------------------------ set 3: exponential functions
def one_exp(r):
    kind = r.choice(["val", "val", "yint", "graph", "neg"])
    a = r.choice([2, 3, 2, 4])
    k = r.choice([1, 2, 3, 5, 10])
    f = "%s = %s%s<sup><i>x</i></sup>" % (Y, "" if k == 1 else num(k) + " × ", num(a))
    if kind == "val":
        x = r.choice([0, 1, 2, 3])
        if a ** x * k > 500:
            return None
        y = k * a ** x
        return T("Find the value of %s when %s = %d for %s." % (Y, X, x, f), num(y), [num(k * a * x), num((k * a) ** x) if k > 1 and (k * a) ** x != y else num(y + k), num(k * x ** a) if k * x ** a != y else num(y * a)],
                 "%s<sup>%d</sup> = %s, so %s = %s × %s = <b>%s</b>." % (num(a), x, num(a ** x), Y, num(k), num(a ** x), num(y)) if k != 1 else "%s<sup>%d</sup> = <b>%s</b>." % (num(a), x, num(y)))
    if kind == "neg":
        x = r.choice([-1, -2])
        y = F(k, a ** -x)
        return T("Find the value of %s when %s = %s for %s." % (Y, X, num(x), f), fv(y), [fv(-y), fv(k * a * x), fv(F(k, a * -x)) if F(k, a * -x) != y else fv(y * 2)],
                 "A negative index means 1 over: %s<sup>%s</sup> = %s, so %s = <b>%s</b>." % (num(a), num(x), fr(1, a ** -x), Y, fv(y)))
    if kind == "yint":
        return T("Where does the graph of %s cut the %s-axis?" % (f, Y), "(0, %s)" % num(k), ["(0, %s)" % num(k * a), "(0, 0)", "(%s, 0)" % num(k)],
                 "At %s = 0, %s<sup>0</sup> = 1, so %s = %s × 1. The point is <b>(0, %s)</b>. The graph never cuts the %s-axis." % (X, num(a), Y, num(k), num(k), X))
    fn = lambda x: 2 ** x
    right = "%s = 2<sup><i>x</i></sup>" % Y
    return T("Which equation could this graph have?%s" % g(fn, -4, 4, -2, 14, label="graph of y = 2 to the power x"), right,
             ["%s = %s" % (Y, pw(2, 1)), "%s = 2%s" % (Y, X), "%s = %s" % (Y, pw(-1, 2))],
             "The curve is always above the x-axis, passes through (0, 1) and grows faster and faster: an exponential graph, <b>%s</b>." % right)


# ------------------------------------------------------------ set 4: reading graphs
def one_read(r):
    kind = r.choice(["recip", "cube", "exp"])
    if kind == "recip":
        a = r.choice([4, 6, 8, 12])
        x = r.choice([v for v in [1, 2, 3, 4, 6] if a % v == 0 and a // v <= 12])
        fn = lambda t: a / t if t != 0 else None
        k = a // x
        return T("The graph of %s = %s is shown. Use it to find %s when %s = %s.%s" % (Y, pw(-1, a), X, Y, num(k), g(fn, -6, 6, -12, 12, label="graph of y = %d over x" % a, unit=18)),
                 "%s = %s" % (X, num(x)), ["%s = %s" % (X, num(-x)), "%s = %s" % (X, num(k * a)) if k * a < 100 else "%s = %s" % (X, num(x + 1)), "%s = %s" % (X, fv(F(k, a)))],
                 "Go across from %s = %s to the curve and read down: <b>%s = %s</b> (check: %s ÷ %s = %s)." % (Y, num(k), X, num(x), num(a), num(x), num(k)))
    if kind == "cube":
        c = r.choice([0, 1, -1])
        x = r.choice([-2, -1, 1, 2])
        fn = lambda t: t ** 3 + c
        y = x ** 3 + c
        f = "%s = %s%s" % (Y, X + "<sup>3</sup>", "" if c == 0 else " %s %d" % ("+" if c > 0 else MINUS, abs(c)))
        return T("The graph of %s is shown. What is the value of %s when %s = %s?%s" % (f, Y, X, num(x), g(fn, -3, 3, -10, 10, label="graph of a cubic", unit=20)),
                 num(y), [num(-y) if y else "1", num(3 * x + c), num(x * x + c) if x * x + c != y else num(y + 1)],
                 "%s = (%s)<sup>3</sup>%s = <b>%s</b>." % (Y, num(x), "" if c == 0 else " %s %d" % ("+" if c > 0 else MINUS, abs(c)), num(y)))
    k = r.choice([1, 2, 3])
    yv = r.choice([2, 4, 8])
    x = {2: 1, 4: 2, 8: 3}[yv]
    if k * yv > 14:
        return None
    fn = lambda t: k * 2 ** t
    f = "%s = %s2<sup><i>x</i></sup>" % (Y, "" if k == 1 else num(k) + " × ")
    return T("The graph of %s is shown. Find %s when %s = %s.%s" % (f, X, Y, num(k * yv), g(fn, -3, 4, -2, 14, label="graph of an exponential function", unit=22)),
             "%s = %s" % (X, num(x)), ["%s = %s" % (X, num(x + 1)), "%s = %s" % (X, num(k * yv // 2)) if k * yv // 2 != x else "%s = %s" % (X, num(x + 2)), "%s = %s" % (X, num(-x))],
             "2<sup>%d</sup> = %d, so %s%d = %d. <b>%s = %d</b>." % (x, yv, "" if k == 1 else "%d × " % k, yv, k * yv, X, x))


# ------------------------------------------------------------ set 5: gradient of a curve by a tangent
def one_tangent(r):
    kind = r.choice(["sq", "sq", "sq", "cube", "recip", "recip"])
    if kind == "sq":
        a = r.choice([1, 1, F(1, 2)])
        c = r.choice([0, 0, -4, -2, 1, 2])
        x0 = r.choice([-3, -2, -1, 1, 2, 3])
        m = 2 * a * x0
        y0 = a * x0 * x0 + c
        fn = lambda t: float(a) * t * t + c
        f = "%s = %s%s" % (Y, (fv(a) if a != 1 else "") + X + "<sup>2</sup>", "" if c == 0 else " %s %d" % ("+" if c > 0 else MINUS, abs(c)))
        lo, hi, ylo, yhi, u = -4, 4, -8, 10, 20
    elif kind == "cube":
        x0 = r.choice([-1, 1])
        c = r.choice([0, 2, -2])
        m = 3 * x0 * x0
        y0 = x0 ** 3 + c
        fn = lambda t: t ** 3 + c
        f = "%s = %s%s" % (Y, X + "<sup>3</sup>", "" if c == 0 else " %s %d" % ("+" if c > 0 else MINUS, abs(c)))
        lo, hi, ylo, yhi, u = -3, 3, -8, 8, 22
    else:
        a = r.choice([4, 8])
        x0 = r.choice([1, 2, -2, -1] if a == 4 else [2, -2, 4])
        m = F(-a, x0 * x0)
        y0 = F(a, x0)
        fn = lambda t: a / t if t else None
        f = "%s = %s" % (Y, fr(num(a), X))
        lo, hi, ylo, yhi, u = -6, 6, -9, 9, 18
    b = y0 - m * x0
    pic = g(fn, lo, hi, ylo, yhi, slant=((float(m), float(b)),), label="curve with a tangent at x = %d" % x0, unit=u, at=(float(x0), float(y0)))
    right = fv(m)
    wr = [fv(-m) if m else "1", fv(1 / m) if m not in (0, 1, -1) else fv(m * 2), fv(y0) if y0 not in (m, -m) else fv(m + 1)]
    if len({right} | set(wr)) < 4:
        return None
    return T("The dashed line is the tangent to %s at the point (%s, %s). Estimate the gradient of the curve at this point.%s" % (f, num(x0), fv(y0), pic),
             right, wr,
             "Pick two points on the tangent far apart and work out rise ÷ run. The tangent has gradient <b>%s</b>%s." % (
                 right, " (it slopes downwards, so the gradient is negative)" if m < 0 else ""))


def build():
    sets = [S("Recognising power graphs", collect(one_shape, 20, R)),
            S("Tables of values", collect(one_table, 20, R)),
            S("Exponential functions", collect(one_exp, 20, R)),
            S("Reading values from graphs", collect(one_read, 20, R)),
            S("Gradient of a curve using a tangent", collect(one_tangent, 20, R))]
    body = lesson(
        "<ul><li><b>y = ax²</b>: a parabola. <b>y = ax³</b>: an S-shaped cubic through the origin.</li>"
        "<li><b>y = a/x</b>: two curves in opposite quadrants. <b>y = a/x²</b>: two curves on the same side of the x-axis. Neither touches the axes.</li>"
        "<li><b>y = kaˣ</b> (a &gt; 1): always above the x-axis, cuts the y-axis at (0, k), and grows faster and faster.</li>"
        "<li>The <b>gradient of a curve</b> at a point is the gradient of the tangent there: rise ÷ run using two points on the tangent.</li></ul>",
        [("Find y when x = −2 for y = x² + 4/x.", ["(−2)² = 4", "4 ÷ (−2) = −2", "4 + (−2)"], "2"),
         ("For y = 3 × 2ˣ, find y when x = 3.", ["2³ = 8", "3 × 8"], "24")],
        ["Mixing up y = 1/x (opposite quadrants) and y = 1/x² (both above the x-axis).",
         "Working out 2ˣ as 2 × x. 2³ = 8, not 6.",
         "Squaring a negative number wrongly: (−3)² = 9, but (−3)³ = −27.",
         "Using run ÷ rise for the gradient, or reading the gradient off the curve instead of the tangent."])
    faq = [("What do power graphs look like?", "y = x² is a ∪-shaped parabola, y = x³ is an S-shaped curve, y = 1/x has two branches in opposite quadrants, and y = 1/x² has two branches above the x-axis."),
           ("What does an exponential graph look like?", "y = kaˣ with a > 1 stays above the x-axis, passes through (0, k) and rises more and more steeply as x increases."),
           ("How do you estimate the gradient of a curve?", "Draw the tangent touching the curve at the point, choose two points on the tangent far apart, and divide the change in y by the change in x."),
           ("Why does y = 1/x never touch the axes?", "x cannot be 0, because you cannot divide by 0, and 1/x is never 0, so the curve gets closer to the axes without touching them.")]
    make(3, "power-and-exponential-graphs", 8, "N6",
         "Graphs of Power and Exponential Functions",
         "", "Power and exponential graphs", "",
         "Free Secondary 3 maths worksheets on graphs of power functions y = axⁿ, reciprocal graphs, exponential graphs y = kaˣ, tables of values and the gradient of a curve using a tangent. 100 questions with answers.",
         "Know the shapes: x², x³, 1/x, 1/x² and kaˣ each have their own graph.",
         "The gradient of a curve at a point is the gradient of its tangent: rise ÷ run.",
         body, faq, sets, R)


if __name__ == "__main__":
    build()
