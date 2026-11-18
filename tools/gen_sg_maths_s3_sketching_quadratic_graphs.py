# -*- coding: utf-8 -*-
"""
SG Secondary 3 Maths: Sketching Graphs of Quadratic Functions (MOE syllabus N6 and the graphical method in N7)
  python3 tools/gen_sg_maths_s3_sketching_quadratic_graphs.py
y = (x − p)² + q and y = −(x − p)² + q (turning point, maximum or minimum, line of symmetry),
y = (x − a)(x − b) and y = −(x − a)(x − b) (intercepts and turning point), matching graphs to equations,
and solving quadratic equations by the graphical method.
Wrong answers come from real mistakes: taking the turning point of (x − 3)² as x = −3, mixing up maximum and
minimum, forgetting the y-intercept is the value at x = 0, and reading the wrong line on the graph.
"""
import random
from fractions import Fraction as F
from sg_sec import num, S, make, lesson, collect, T, expr, fr, fig, MINUS
from pc_common import curve_svg

R = random.Random(830700)
X = "<i>x</i>"
Y = "<i>y</i>"
X2 = X + "<sup>2</sup>"


def fv(v):
    v = F(v)
    return num(v) if v.denominator == 1 else (MINUS if v < 0 else "") + fr(abs(v.numerator), v.denominator)


def pt(a, b):
    return "(%s, %s)" % (fv(a), fv(b))


def sqf(p, q, s=1):
    """y = ±(x − p)² + q as HTML"""
    br = "(%s)<sup>2</sup>" % expr([(1, X), (-p, "")]) if p else X2
    lead = "" if s > 0 else MINUS
    tail = "" if q == 0 else " %s %s" % ("+" if q > 0 else MINUS, num(abs(q)))
    return "%s = %s%s%s" % (Y, lead, br, tail)


def rootf(a, b, s=1):
    lead = "" if s > 0 else MINUS
    fa = "(%s)" % expr([(1, X), (-a, "")]) if a else X
    fb = "(%s)" % expr([(1, X), (-b, "")]) if b else X
    if not b:
        fa, fb = fb, fa
    return "%s = %s%s%s" % (Y, lead, fa, fb)


def sol(vs):
    vs = sorted(set(F(v) for v in vs))
    return " or ".join("%s = %s" % (X, fv(v)) for v in vs)


def nz(r, lo, hi):
    return r.choice([v for v in range(lo, hi + 1) if v])


# ------------------------------------------------------------ set 1: y = (x − p)² + q
def one_min(r):
    p, q = nz(r, -6, 6), r.randint(-9, 9)
    kind = r.choice(["tp", "tp", "min", "sym", "yint"])
    f = sqf(p, q)
    if kind == "tp":
        return T("What are the coordinates of the turning point of %s?" % f, pt(p, q), [pt(-p, q), pt(q, p), pt(p, -q) if q else pt(-p, -q - 1)],
                 "(%s)<sup>2</sup> is smallest (0) when %s = %s, so the turning point is <b>%s</b>." % (expr([(1, X), (-p, "")]), X, num(p), pt(p, q)))
    if kind == "min":
        return T("What is the minimum value of %s?" % f, num(q), [num(p), num(-q) if q else num(1), num(p * p + q)],
                 "A square is never negative, so the least value is when (%s)<sup>2</sup> = 0: %s = <b>%s</b>." % (expr([(1, X), (-p, "")]), Y, num(q)))
    if kind == "sym":
        return T("What is the equation of the line of symmetry of the graph of %s?" % f, "%s = %s" % (X, num(p)),
                 ["%s = %s" % (X, num(-p)), "%s = %s" % (Y, num(q)), "%s = %s" % (X, num(q)) if q != p else "%s = %s" % (Y, num(p))],
                 "The graph is symmetrical about the vertical line through the turning point %s: <b>%s = %s</b>." % (pt(p, q), X, num(p)))
    return T("Where does the graph of %s cut the %s-axis?" % (f, Y), pt(0, p * p + q), [pt(0, q), pt(0, -p * p + q), pt(0, p + q)],
             "Put %s = 0: (%s)<sup>2</sup> %s %s = %s. The point is <b>%s</b>." % (X, num(-p), "+" if q >= 0 else MINUS, num(abs(q)), num(p * p + q), pt(0, p * p + q)))


# ------------------------------------------------------------ set 2: y = −(x − p)² + q
def one_max(r):
    p, q = nz(r, -6, 6), r.randint(-6, 12)
    f = sqf(p, q, -1)
    kind = r.choice(["tp", "max", "shape", "yint"])
    if kind == "tp":
        return T("The graph of %s has a maximum point. What are its coordinates?" % f, pt(p, q), [pt(-p, q), pt(p, -q) if q else pt(p, 1), pt(-p, -q) if q else pt(q, p)],
                 "−(%s)<sup>2</sup> is never positive, so %s is greatest when %s = %s. The maximum point is <b>%s</b>." % (expr([(1, X), (-p, "")]), Y, X, num(p), pt(p, q)))
    if kind == "max":
        return T("What is the maximum value of %s, and when does it occur?" % f, "%s = %s when %s = %s" % (Y, num(q), X, num(p)),
                 ["%s = %s when %s = %s" % (Y, num(q), X, num(-p)), "%s = %s when %s = %s" % (Y, num(p), X, num(q)), "%s = %s when %s = %s" % (Y, num(-q) if q else "1", X, num(p))],
                 "The largest value of −(%s)<sup>2</sup> is 0, at %s = %s. So the maximum is <b>%s = %s when %s = %s</b>." % (expr([(1, X), (-p, "")]), X, num(p), Y, num(q), X, num(p)))
    if kind == "shape":
        right = "∩-shaped with a maximum point at %s" % pt(p, q)
        return T("Which describes the graph of %s?" % f, right,
                 ["∪-shaped with a minimum point at %s" % pt(p, q), "∩-shaped with a maximum point at %s" % pt(-p, q), "∪-shaped with a minimum point at %s" % pt(-p, q)],
                 "The minus sign in front of the square turns the graph upside down, so it is ∩-shaped: <b>%s</b>." % right)
    return T("Where does the graph of %s cut the %s-axis?" % (f, Y), pt(0, q - p * p), [pt(0, q + p * p), pt(0, q), pt(0, p * p - q) if p * p - q != q - p * p else pt(0, q - p)],
             "Put %s = 0: −(%s)<sup>2</sup> %s %s = −%s %s %s = %s. The point is <b>%s</b>." % (X, num(-p), "+" if q >= 0 else MINUS, num(abs(q)), num(p * p), "+" if q >= 0 else MINUS, num(abs(q)), num(q - p * p), pt(0, q - p * p)))


# ------------------------------------------------------------ set 3: y = ±(x − a)(x − b)
def one_roots(r):
    a, b = sorted(r.sample(range(-6, 7), 2))
    s = r.choice([1, 1, -1])
    f = rootf(a, b, s)
    kind = r.choice(["xint", "sym", "tp", "yint"])
    if kind == "xint":
        right = "%s and %s" % (pt(a, 0), pt(b, 0))
        return T("Where does the graph of %s cut the %s-axis?" % (f, X), right, ["%s and %s" % (pt(-a, 0), pt(-b, 0)), "%s and %s" % (pt(0, a), pt(0, b)), "%s only" % pt(s * a * b, 0) if a * b else "%s and %s" % (pt(a, 0), pt(-b, 0))],
                 "%s = 0 when %s = %s or %s = %s, so the graph cuts the %s-axis at <b>%s</b>." % (Y, X, num(a), X, num(b), X, right))
    m = F(a + b, 2)
    if kind == "sym":
        return T("What is the line of symmetry of the graph of %s?" % f, "%s = %s" % (X, fv(m)), ["%s = %s" % (X, fv(-m)) if m else "%s = 0" % Y, "%s = %s" % (X, fv(b - a)), "%s = %s" % (X, fv(a * b)) if a * b != m else "%s = %s" % (X, fv(m + 1))],
                 "The line of symmetry is halfway between the roots %s and %s: <b>%s = %s</b>." % (num(a), num(b), X, fv(m)))
    if kind == "tp":
        yv = s * (m - a) * (m - b)
        word = "minimum" if s > 0 else "maximum"
        return T("Find the %s point of the graph of %s." % (word, f), pt(m, yv), [pt(m, -yv), pt(-m, yv) if m else pt(yv, m), pt(m, s * a * b)] if s * a * b != yv else [pt(m, -yv), pt(-m, yv) if m else pt(yv, m), pt(m, yv + 1)],
                 "The turning point is on the line %s = %s. Put %s = %s: %s = <b>%s</b>, so the point is <b>%s</b>." % (X, fv(m), X, fv(m), Y, fv(yv), pt(m, yv)))
    yi = s * a * b
    return T("Where does the graph of %s cut the %s-axis?" % (f, Y), pt(0, yi), [pt(0, -yi) if yi else pt(0, 1), pt(0, a + b), pt(0, -(a + b)) if a + b else pt(0, 2)],
             "Put %s = 0: %s(%s)(%s) = %s. The point is <b>%s</b>." % (X, "" if s > 0 else MINUS, num(-a), num(-b), num(yi), pt(0, yi)))


# ------------------------------------------------------------ set 4: matching graphs and equations
def graph(fn, lo=-6, hi=6, ylo=-8, yhi=8, h=(), label="graph"):
    return fig(curve_svg(fn, lo, hi, ylo, yhi, unit=20, hasym=h, label=label))


def one_match(r):
    kind = r.choice(["sq", "sq", "roots"])
    if kind == "sq":
        p, q = nz(r, -3, 3), r.randint(-4, 4)
        s = r.choice([1, -1])
        if s > 0 and q > 3 or s < 0 and q < -3:
            return None
        g = graph(lambda x: s * (x - p) ** 2 + q, label="graph of a quadratic with turning point (%d, %d)" % (p, q))
        right = sqf(p, q, s)
        wr = [sqf(-p, q, s), sqf(p, q, -s), sqf(p, -q, s) if q else sqf(-p, q, -s)]
        return T("The graph shows a quadratic function. Which is its equation?%s" % g, right, wr,
                 "The turning point is %s and the graph is %s-shaped (%s), so the equation is <b>%s</b>." % (pt(p, q), "∪" if s > 0 else "∩", "positive " + X2 if s > 0 else "negative " + X2, right))
    a, b = sorted(r.sample(range(-4, 5), 2))
    s = r.choice([1, -1])
    if max(abs(s * (F(a + b, 2) - a) * (F(a + b, 2) - b)), abs(a * b)) > 8:
        return None
    g = graph(lambda x: s * (x - a) * (x - b), label="graph of a quadratic crossing the x-axis at %d and %d" % (a, b))
    right = rootf(a, b, s)
    wr = [rootf(-b, -a, s) if (-b, -a) != (a, b) else rootf(a, b + 1, s), rootf(a, b, -s), rootf(-b, -a, -s) if (-b, -a) != (a, b) else rootf(a - 1, b, s)]
    return T("The graph shows a quadratic function. Which is its equation?%s" % g, right, wr,
             "It cuts the %s-axis at %s = %s and %s = %s and is %s-shaped, so <b>%s</b>. Check: at %s = 0, %s = %s." % (X, X, num(a), X, num(b), "∪" if s > 0 else "∩", right, X, Y, num(s * a * b)))


# ------------------------------------------------------------ set 5: the graphical method
def one_graphical(r):
    a, b = sorted(r.sample(range(-4, 5), 2))
    B_, C_ = -(a + b), a * b
    fn = lambda x: (x - a) * (x - b)
    m = F(a + b, 2)
    ymin = (m - a) * (m - b)
    if ymin < -8:
        return None
    kind = r.choice(["zero", "zero", "k", "k", "min"])
    eq = expr([(1, X2), (B_, X), (C_, "")])
    if kind == "zero":
        g = graph(fn, ylo=-8, yhi=8, label="graph of y = x squared %+d x %+d" % (B_, C_))
        right = sol([a, b])
        w1 = sol([-a, -b]) if {-a, -b} != {a, b} else sol([a - 1, b + 1])
        return T("The graph of %s = %s is shown. Use it to solve %s = 0.%s" % (Y, eq, eq, g), right,
                 [w1, sol([C_]) if C_ not in (a, b) else sol([C_ + 1]), sol([m]) if m not in (a, b) else sol([m + F(1, 2)])],
                 "The solutions are where the graph cuts the %s-axis (%s = 0): <b>%s</b>." % (X, Y, right))
    if kind == "k":
        # choose k so that x² + Bx + C = k has integer roots c, d with c + d = a + b
        c = r.choice([v for v in range(-5, 6) if v < m])
        d = a + b - c
        k = (c - a) * (c - b)
        if k == 0 or abs(k) > 8 or k < ymin or abs(d) > 6:
            return None
        g = graph(fn, ylo=-8, yhi=8, h=(k,), label="graph of a quadratic with the line y = %d" % k)
        right = sol([c, d])
        return T("The graph of %s = %s and the line %s = %s are shown. Use them to solve %s = %s.%s" % (Y, eq, Y, num(k), eq, num(k), g), right,
                 [sol([a, b]), sol([-c, -d]) if {-c, -d} != {c, d} else sol([c - 1, d + 1]), sol([k]) if k not in (c, d) else sol([k + 1])],
                 "Read the %s-values where the curve meets the line %s = %s: <b>%s</b>." % (X, Y, num(k), right))
    if m.denominator != 1:
        return None
    g = graph(fn, ylo=-8, yhi=8, label="graph of a quadratic showing its minimum point")
    right = "%s = %s" % (Y, fv(ymin))
    return T("The graph of %s = %s is shown. What is the minimum value of %s?%s" % (Y, eq, Y, g), right,
             ["%s = %s" % (Y, fv(m)), "%s = %s" % (Y, num(C_)), "%s = %s" % (Y, fv(-ymin)) if ymin else "%s = 1" % Y],
             "The lowest point of the curve is %s, so the minimum value is <b>%s</b>." % (pt(m, ymin), right))


def build():
    sets = [S("Graphs of y = (x − p)² + q", collect(one_min, 20, R)),
            S("Graphs of y = −(x − p)² + q", collect(one_max, 20, R)),
            S("Graphs of y = ±(x − a)(x − b)", collect(one_roots, 20, R)),
            S("Matching graphs and equations", collect(one_match, 20, R)),
            S("Solving equations using graphs", collect(one_graphical, 20, R))]
    body = lesson(
        "<ul><li><b>y = (x − p)² + q</b> is ∪-shaped with a <b>minimum point (p, q)</b>. <b>y = −(x − p)² + q</b> is ∩-shaped with a <b>maximum point (p, q)</b>.</li>"
        "<li><b>y = (x − a)(x − b)</b> cuts the x-axis at <b>x = a</b> and <b>x = b</b>. The line of symmetry is halfway between them.</li>"
        "<li>The <b>y-intercept</b> is the value of y when x = 0.</li>"
        "<li>To solve f(x) = k from a graph, read the x-values where the curve meets the line y = k.</li></ul>",
        [("Sketch y = (x − 2)² − 9.", ["Minimum point (2, −9)", "x = 0 gives y = −5", "y = 0 gives x − 2 = ±3, so x = −1 or 5"], "∪-shaped through (−1, 0), (5, 0) and (0, −5)"),
         ("Find the maximum point of y = −(x + 1)(x − 5).", ["Roots −1 and 5, so the line of symmetry is x = 2", "y = −(3)(−3) = 9"], "(2, 9)")],
        ["Taking the turning point of y = (x − 3)² + 1 as (−3, 1). It is (3, 1).",
         "Calling the turning point of −(x − p)² + q a minimum. The minus sign makes it a maximum.",
         "Reading the roots of (x − 2)(x + 4) as 2 and 4. They are 2 and −4.",
         "Reading the y-values instead of the x-values when solving from a graph."])
    faq = [("How do you find the turning point of y = (x − p)² + q?", "The turning point is (p, q). It is a minimum if the square is positive and a maximum if there is a minus sign in front of the square."),
           ("How do you sketch y = (x − a)(x − b)?", "Mark where it cuts the x-axis at x = a and x = b, find the y-intercept by putting x = 0, and draw a smooth ∪ (or ∩ for a minus sign) symmetrical about x = (a + b)/2."),
           ("What is the line of symmetry of a quadratic graph?", "A vertical line through the turning point, x = p for y = (x − p)² + q, or x = (a + b)/2 for y = (x − a)(x − b)."),
           ("How do I solve an equation using a graph?", "Draw the curve and the line y = k. The x-coordinates of the points where they meet are the solutions of f(x) = k.")]
    make(3, "sketching-quadratic-graphs", 7, "N6",
         "Sketching Graphs of Quadratic Functions",
         "", "Sketching quadratic graphs", "",
         "Free Secondary 3 maths worksheets on sketching quadratic graphs: turning points, maximum and minimum values, intercepts, lines of symmetry and solving equations by the graphical method. 100 questions with answers.",
         "y = (x − p)² + q has its turning point at (p, q).",
         "y = (x − a)(x − b) cuts the x-axis at a and b; a minus sign in front turns the graph upside down.",
         body, faq, sets, R)


if __name__ == "__main__":
    build()
