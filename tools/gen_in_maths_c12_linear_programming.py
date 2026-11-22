# -*- coding: utf-8 -*-
"""
India Class 12 Maths, NCERT Chapter 12: Linear Programming (CBSE Unit V Linear Programming)
  python3 tools/gen_in_maths_c12_linear_programming.py
The objective function and constraints, writing constraints from a word problem, checking if a point is feasible,
corner points of the feasible region (where two boundary lines meet), the corner point method for the maximum and
the minimum, and bounded and unbounded regions (own makers).
Wrong answers come from real mistakes: the inequality the wrong way round, mixing up the coefficients of x and y,
taking the largest coordinate instead of the largest value of Z, and assuming a maximum always exists.
"""
import random
from fractions import Fraction as F
from in_sr import U, T2, X, Y
from in_common import num, fv, comma, expr

R = random.Random(912112)


def pt(p):
    return "(%s, %s)" % (fv(p[0]), fv(p[1]))


def Zs(a, b):
    return "Z = " + expr([(a, X), (b, Y)])


def region(r):
    """a bounded region from x ≥ 0, y ≥ 0, a1 x + b1 y ≤ c1, a2 x + b2 y ≤ c2 with integer corners"""
    for _ in range(200):
        px, py = r.randint(1, 8), r.randint(1, 8)
        a1, b1 = r.randint(1, 4), r.randint(1, 4)
        a2, b2 = r.randint(1, 4), r.randint(1, 4)
        if a1 * b2 == a2 * b1:
            continue
        c1, c2 = a1 * px + b1 * py, a2 * px + b2 * py
        xa, ya = F(c1, a1), F(c1, b1)
        xb, yb = F(c2, a2), F(c2, b2)
        # the corners: (0,0), x-int = min(xa, xb), y-int = min(ya, yb), and (px, py) if the lines cross inside
        if not ((xa < xb and ya > yb) or (xa > xb and ya < yb)):
            continue
        cs = [(F(0), F(0)), (min(xa, xb), F(0)), (px, py), (F(0), min(ya, yb))]
        if any(F(v).denominator != 1 for p in cs for v in p):
            continue
        return (a1, b1, c1), (a2, b2, c2), [(F(p[0]), F(p[1])) for p in cs]
    return None


def cons(a, b, c):
    return expr([(a, X), (b, Y)]) + " ≤ %d" % c


def one_corner(r):
    g = region(r)
    if not g:
        return None
    L1, L2, cs = g
    a, b = r.randint(1, 9), r.randint(1, 9)
    vals = [a * p[0] + b * p[1] for p in cs]
    mx = max(vals)
    if vals.count(mx) > 1:
        return None
    best = cs[vals.index(mx)]
    q = "Maximise %s subject to %s, %s, %s ≥ 0, %s ≥ 0. The corner points of the feasible region are %s. Find the maximum value of Z." % (
        Zs(a, b), cons(*L1), cons(*L2), X, Y, ", ".join(pt(p) for p in cs))
    others = sorted(set(vals) - {mx}, reverse=True)
    return T2(q, num(mx), [num(others[0]), num(max(max(p) for p in cs)) if max(max(p) for p in cs) != mx else num(mx + a), num(sum(vals))],
              "Work out Z at each corner: %s. The largest is <b>%s</b>, at %s." % (", ".join("%s → %s" % (pt(p), num(v)) for p, v in zip(cs, vals)), num(mx), pt(best)))


def one_min(r):
    # unbounded region x + y ≥ p, a x + b y ≥ c ... use given corner points
    pts = [(0, r.randint(6, 12)), (r.randint(1, 4), r.randint(2, 5)), (r.randint(5, 9), 0)]
    a, b = r.randint(1, 9), r.randint(1, 9)
    vals = [a * x + b * y for x, y in pts]
    mn = min(vals)
    if vals.count(mn) > 1:
        return None
    q = "The feasible region of a problem is unbounded, with corner points %s. The half-plane %s &lt; %s has no point in common with the region. Find the minimum of %s." % (
        ", ".join("(%d, %d)" % p for p in pts), expr([(a, X), (b, Y)]), num(mn), Zs(a, b))
    return T2(q, num(mn), [num(max(vals)), "It has no minimum", num(sorted(vals)[1])],
              "Z at the corners: %s. Since %s &lt; %s has no point in the region, the smallest corner value <b>%s</b> is the minimum." % (
                  ", ".join("%s" % num(v) for v in vals), expr([(a, X), (b, Y)]), num(mn), num(mn)))


def one_meet(r):
    x0, y0 = r.randint(0, 9), r.randint(0, 9)
    a1, b1, a2, b2 = r.randint(1, 5), r.randint(1, 5), r.randint(1, 5), r.randint(1, 5)
    if a1 * b2 == a2 * b1:
        return None
    c1, c2 = a1 * x0 + b1 * y0, a2 * x0 + b2 * y0
    return T2("Find the corner point where the lines %s = %d and %s = %d meet." % (expr([(a1, X), (b1, Y)]), c1, expr([(a2, X), (b2, Y)]), c2), "(%d, %d)" % (x0, y0),
              ["(%d, %d)" % (y0, x0) if x0 != y0 else "(%d, %d)" % (x0 + 1, y0), "(%s, 0)" % fv(F(c1, a1)), "(0, %s)" % fv(F(c2, b2))],
              "Solve the two equations together: <b>(%d, %d)</b>." % (x0, y0))


def one_feas(r):
    a1, b1, a2, b2 = r.randint(1, 4), r.randint(1, 4), r.randint(1, 4), r.randint(1, 4)
    c1, c2 = r.randint(10, 30), r.randint(10, 30)
    if a1 * b2 == a2 * b1:
        return None
    pts = [(r.randint(0, 8), r.randint(0, 8)) for _ in range(12)]
    good = [p for p in pts if a1 * p[0] + b1 * p[1] <= c1 and a2 * p[0] + b2 * p[1] <= c2]
    bad = [p for p in pts if p not in good]
    if not good or len(set(bad)) < 3:
        return None
    g = r.choice(good)
    bs = list(dict.fromkeys(bad))[:3]
    return T2("Which point lies in the feasible region %s, %s, %s ≥ 0, %s ≥ 0?" % (cons(a1, b1, c1), cons(a2, b2, c2), X, Y), "(%d, %d)" % g, ["(%d, %d)" % p for p in bs],
              "Substitute each point. (%d, %d) gives %d ≤ %d and %d ≤ %d, so <b>(%d, %d)</b> is feasible; each of the others breaks a constraint." % (
                  g[0], g[1], a1 * g[0] + b1 * g[1], c1, a2 * g[0] + b2 * g[1], c2, g[0], g[1]))


ITEMS = [("chairs", "tables", "carpentry"), ("cakes", "biscuits", "baking"), ("bags", "belts", "stitching"), ("fans", "lamps", "assembly"), ("kurtas", "shirts", "tailoring"),
         ("toys of type A", "toys of type B", "machine"), ("pots", "vases", "glazing")]


def one_form(r):
    a_, b_, res = r.choice(ITEMS)
    p, q, h = r.randint(1, 6), r.randint(1, 6), r.randint(20, 120)
    if p == q:
        return None
    right = "%s ≤ %d" % (expr([(p, X), (q, Y)]), h)
    return T2("A factory makes %s %s and %s %s. Each of the %s needs %d hours of %s and each of the %s needs %d hours. At most %d hours of %s are available. Which constraint is correct?" % (
        X, a_, Y, b_, a_, p, res, b_, q, h, res), right,
              ["%s ≤ %d" % (expr([(q, X), (p, Y)]), h), "%s ≥ %d" % (expr([(p, X), (q, Y)]), h), "%s ≤ %d" % (expr([(1, X), (1, Y)]), h)],
              "Hours used = %d%s + %d%s, and it cannot be more than %d: <b>%s</b>." % (p, X, q, Y, h, right))


def one_concept(r):
    qs = [("In a linear programming problem, where does the optimal value of Z occur (if it exists)?", "At a corner point of the feasible region",
           ["At the centre of the feasible region", "Anywhere inside the feasible region", "Only at the origin"]),
          ("The feasible region is bounded. Which is true?", "Z has both a maximum and a minimum value", ["Z has a maximum but never a minimum", "Z may have no maximum", "Z has no optimal value"]),
          ("The feasible region is unbounded. Which is true?", "A maximum or minimum may not exist", ["A maximum always exists", "A minimum never exists", "There are no corner points"]),
          ("What are the conditions x ≥ 0, y ≥ 0 called?", "Non-negative constraints", ["Objective functions", "Optimal solutions", "Feasible solutions"]),
          ("What is the function Z = ax + by that is maximised or minimised called?", "The objective function", ["The constraint", "The feasible region", "The decision variable"]),
          ("Two corner points give the same maximum value of Z. Which is true?", "Every point on the segment joining them also gives the maximum", ["The problem has no maximum", "Only those two points give the maximum", "The feasible region is unbounded"]),
          ("A set of constraints has no point that satisfies all of them. What is the feasible region called?", "Empty (the problem is infeasible)", ["Unbounded", "Bounded", "Convex"])]
    q, right, wr = r.choice(qs)
    return T2(q, right, wr, "<b>%s</b>." % right)


U(12, 12, "linear-programming", 12, "LP", "Linear Programming: Constraints, Feasible Regions and the Corner Point Method", "linear programming",
  "Introduction, related terminology such as constraints, objective function, optimization; graphical method of solution for problems in two variables, feasible and infeasible regions (bounded or unbounded), feasible and infeasible solutions, optimal feasible solutions (up to three non-trivial constraints) (summary of the CBSE syllabus)",
  "Class 12 Linear Programming worksheet (NCERT Chapter 12): objective functions, constraints, feasible points, corner points, the corner point method for maximum and minimum, and unbounded regions. 100 questions with answers.",
  "The optimal value of Z occurs at a corner point.", "For an unbounded region, check the half-plane before accepting a corner value.",
  "<ul><li>An LPP maximises or minimises an <b>objective function</b> Z = a<i>x</i> + b<i>y</i> subject to linear <b>constraints</b> and <i>x</i>, <i>y</i> ≥ 0.</li>"
  "<li>The <b>feasible region</b> is the set of points that satisfy every constraint.</li>"
  "<li><b>Corner point method</b>: find the corner points (where boundary lines meet), work out Z at each, and pick the largest or smallest.</li>"
  "<li>If the region is <b>unbounded</b>, the largest (smallest) corner value M is the maximum (minimum) only if the half-plane a<i>x</i> + b<i>y</i> &gt; M (&lt; M) has no point in the region.</li></ul>",
  [("Maximise Z = 3<i>x</i> + 4<i>y</i> with corner points (0, 0), (4, 0), (2, 3), (0, 4).", ["Z = 0, 12, 18, 16"], "18 at (2, 3)")],
  ["Writing the inequality the wrong way round.", "Swapping the coefficients of x and y in a constraint.", "Assuming a maximum always exists in an unbounded region."],
  [("Why only the corner points?", "For a linear Z, the optimum of a bounded region is always at a corner."),
   ("Can there be more than one optimal point?", "Yes. If two corners give the same optimum, every point between them does too.")],
  [("Terms and ideas", [(one_concept, 7), (one_form, 13)]),
   ("Feasible points and corners", [(one_feas, 10), (one_meet, 10)]),
   ("Maximum by the corner point method", [(one_corner, 20)]),
   ("Minimum and unbounded regions", [(one_min, 20)]),
   ("Mixed problems", [(one_corner, 8), (one_form, 6), (one_meet, 6)])], 912112)
