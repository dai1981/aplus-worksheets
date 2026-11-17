# -*- coding: utf-8 -*-
"""
UK Year 8 Maths: Linear Graphs, y = mx + c (KS3 Algebra)
  python3 tools/gen_uk_maths_y8_linear_graphs.py
Gradient and y-intercept from an equation, gradient from two points, the equation of a line from its graph,
parallel lines and lines through a given point, and real-life straight-line graphs.
Wrong answers come from real mistakes: swapping m and c, using change in x over change in y, losing the
sign of a negative gradient, and not rearranging to y = … first.
"""
import random
from fractions import Fraction as F
from uk_ks3 import num, mcq, B, S, make, lesson, collect, QN, T, fr, expr, fig, BLUE, RED, MINUS
from gen_uk_maths_y7_coordinates_and_straight_line_graphs import grid

R = random.Random(80701)
X, Y = "<i>x</i>", "<i>y</i>"


def sv(v):
    v = F(v)
    return num(v) if v.denominator == 1 else (MINUS if v < 0 else "") + fr(abs(v.numerator), v.denominator)


def eq(m, c):
    m, c = F(m), F(c)
    if m.denominator != 1:
        mt = (MINUS if m < 0 else "") + fr(abs(m.numerator), m.denominator) + X
        rest = expr([(c, "")]) if c else ""
        rest = ("" if not c else (" + " + num(c) if c > 0 else " %s %s" % (MINUS, num(-c))))
        return "%s = %s%s" % (Y, mt, rest)
    return "%s = %s" % (Y, expr([(m, X), (c, "")]))


def P(x, y):
    return "(%s, %s)" % (num(x), num(y))


# ------------------------------------------------------------ set 1: m and c from the equation
def one_mc(r):
    m = r.choice([2, 3, 4, 5, -1, -2, -3, F(1, 2), -4])
    c = r.randint(-8, 9)
    kind = r.random()
    if kind < 0.35:
        q = "What is the %s of the line %s?" % (B("gradient"), B(eq(m, c)))
        return T(q, sv(m), [sv(c) if c != m else sv(c + 1), sv(-m), sv(1 / F(m)) if abs(m) != 1 else sv(m + 1)],
                 "In <i>y</i> = <i>mx</i> + <i>c</i>, the gradient is the number in front of <i>x</i>: <b>%s</b>." % sv(m))
    if kind < 0.65:
        if c == 0:
            return None
        q = "Where does the line %s cross the <i>y</i>-axis?" % B(eq(m, c))
        return T(q, P(0, c), [P(c, 0), P(0, m) if m != c and F(m).denominator == 1 else P(0, -c), P(0, -c)],
                 "The line crosses the <i>y</i>-axis when <i>x</i> = 0, at <i>y</i> = <i>c</i>: <b>%s</b>." % P(0, c))
    # rearrange first
    k = r.choice([2, 3])
    a, b = r.randint(-4, 6) * k, r.randint(-4, 6) * k
    if a == 0 or b == 0:
        return None
    if r.random() < 0.5:
        q = "What is the gradient of the line %s?" % B("%s%s = %s" % (k, Y, expr([(a, X), (b, "")])))
        m2 = F(a, k)
        e = "Divide by %d first: %s. The gradient is <b>%s</b>." % (k, eq(m2, F(b, k)), sv(m2))
        return T(q, sv(m2), [sv(a), sv(F(b, k)), sv(-m2)], e)
    c2 = r.randint(-5, 9)
    m3 = r.choice([2, 3, 4, 5])
    q = "What is the gradient of the line %s?" % B("%s = %s %s %d%s" % (Y, num(c2), MINUS, m3, X))
    e = "Write it as %s = %s%d%s + %s: the gradient is <b>%s%d</b>." % (Y, MINUS, m3, X, num(c2), MINUS, m3)
    return T(q, "%s%d" % (MINUS, m3), [str(m3), num(c2), num(c2 - m3)], e)


# ------------------------------------------------------------ set 2: gradient from two points
def one_grad(r):
    x1, y1 = r.randint(-5, 4), r.randint(-6, 6)
    dx = r.randint(1, 5)
    m = r.choice([1, 2, 3, -1, -2, -3, F(1, 2), F(-1, 2), F(3, 2)])
    dy = m * dx
    if dy.denominator != 1:
        return None
    x2, y2 = x1 + dx, y1 + int(dy)
    if r.random() < 0.5:
        (x1, y1), (x2, y2) = (x2, y2), (x1, y1)
    q = "Find the gradient of the line through %s and %s." % (B(P(x1, y1)), B(P(x2, y2)))
    e = "Gradient = change in <i>y</i> ÷ change in <i>x</i> = (%s − %s) ÷ (%s − %s) = %s ÷ %s = <b>%s</b>." % (
        num(y2), "(%s)" % num(y1) if y1 < 0 else num(y1), num(x2), "(%s)" % num(x1) if x1 < 0 else num(x1), num(y2 - y1), num(x2 - x1), sv(m))
    wr = [sv(F(x2 - x1, y2 - y1)) if y2 != y1 else "0", sv(-m), sv(F(y2 + y1, x2 + x1)) if x2 + x1 else sv(m * 2)]
    return T(q, sv(m), [w for w in wr if w != sv(m)] + [sv(m + 1)], e) if len(set(wr) - {sv(m)}) < 3 else T(q, sv(m), wr, e)


# ------------------------------------------------------------ set 3: equation from a graph
def one_from_graph(r):
    m = r.choice([1, 2, 3, -1, -2, F(1, 2), F(-1, 2), 2, -3, 0])
    c = r.randint(-3, 3)
    # endpoints within -5..5
    xs = [x for x in range(-5, 6) if -5 <= m * x + c <= 5]
    if len(xs) < 3:
        return None
    x1, x2 = xs[0], xs[-1]
    line = [(x1, float(m * x1 + c), x2, float(m * x2 + c), BLUE, "")]
    g = grid(lines=line)
    right = eq(m, c) if m != 0 else "%s = %s" % (Y, num(c))
    wr = [eq(c, m) if c not in (0,) and F(m).denominator == 1 and m != 0 else eq(m, -c) if c else eq(-m, c) if m else "%s = %s" % (X, num(c)),
          eq(-m, c) if m else "%s = %s" % (Y, num(-c)) if c else "%s = 1" % Y,
          eq(1 / F(m), c) if m not in (0, 1, -1) else eq(m * 2 if m else 1, c)]
    wr = [w for w in wr if w != right]
    if len(set(wr)) < 3:
        wr.append(eq(m, c + 1))
    e = "It crosses the <i>y</i>-axis at %s, so <i>c</i> = %s. %s" % (num(c), num(c),
         ("For every 1 across it goes %s %s, so <i>m</i> = %s. <b>%s</b>." % ("up" if m > 0 else "down", sv(abs(m)), sv(m), right)) if m else "It is horizontal, so <b>%s</b>." % right)
    return T("What is the equation of the line?%s" % fig(g), right, list(dict.fromkeys(wr))[:3], e)


# ------------------------------------------------------------ set 4: parallel lines and lines through a point
def one_parallel(r):
    m = r.choice([2, 3, 4, -1, -2, -3, 5])
    c = r.randint(-6, 8)
    kind = r.random()
    if kind < 0.45:
        c2 = r.randint(-6, 8)
        if c2 == c:
            return None
        q = "Which line is parallel to %s?" % B(eq(m, c))
        right = eq(m, c2)
        wr = [eq(c2 if c2 else 7, c) if c2 not in (m, 0) else eq(m + 1, c), eq(-m, c2), eq(F(-1, m), c2)]
        return T(q, right, [w for w in wr if w != right], "Parallel lines have the same gradient (%s): <b>%s</b>." % (num(m), right))
    x0, y0 = r.randint(-4, 5), r.randint(-6, 8)
    cc = y0 - m * x0
    q = "Find the equation of the line with gradient %s that passes through %s." % (B(num(m)), B(P(x0, y0)))
    right = eq(m, cc)
    wr = [eq(m, y0), eq(m, y0 + m * x0) if y0 + m * x0 != cc else eq(m, cc + 1), eq(m, x0) if x0 != cc else eq(m, cc - 1)]
    e = "Substitute the point into <i>y</i> = %s + <i>c</i>: %s = %s × %s + <i>c</i>, so <i>c</i> = %s. <b>%s</b>." % (
        expr([(m, X)]), num(y0), num(m), "(%s)" % num(x0) if x0 < 0 else num(x0), num(cc), right)
    return T(q, right, [w for w in wr if w != right], e)


# ------------------------------------------------------------ set 5: real-life graphs
def problems():
    its = []
    data = [
        ("A taxi fare is given by <i>C</i> = 2<i>d</i> + 3, where <i>d</i> is miles. What does the 3 represent?", "A fixed charge of £3", ["The cost per mile", "The number of miles", "The total cost"],
         "When <i>d</i> = 0, <i>C</i> = 3. It is the <b>fixed charge</b> you pay before travelling."),
        ("A taxi fare is given by <i>C</i> = 2<i>d</i> + 3, where <i>d</i> is miles. What does the 2 represent?", "The cost per mile, £2", ["A fixed charge of £2", "2 miles", "The total cost"],
         "The gradient is the rate of change: each extra mile costs <b>£2</b>."),
        ("A candle is 20 cm tall and burns 2 cm every hour. Which equation gives its height <i>h</i> after <i>t</i> hours?", "<i>h</i> = 20 − 2<i>t</i>", ["<i>h</i> = 2<i>t</i> + 20", "<i>h</i> = 20<i>t</i> − 2", "<i>h</i> = 2 − 20<i>t</i>"],
         "Start at 20 and go down 2 each hour: <b><i>h</i> = 20 − 2<i>t</i></b>, a negative gradient."),
        ("A plumber charges £40 call-out plus £25 per hour. Which equation gives the cost <i>C</i> for <i>h</i> hours?", "<i>C</i> = 25<i>h</i> + 40", ["<i>C</i> = 40<i>h</i> + 25", "<i>C</i> = 65<i>h</i>", "<i>C</i> = 25<i>h</i> − 40"],
         "£25 for each hour, plus £40 once: <b><i>C</i> = 25<i>h</i> + 40</b>."),
        ("The line <i>y</i> = 3<i>x</i> − 6 crosses the <i>x</i>-axis at…", "(2, 0)", ["(0, −6)", "(−6, 0)", "(−2, 0)"], "On the <i>x</i>-axis <i>y</i> = 0: 3<i>x</i> − 6 = 0, so <i>x</i> = 2. <b>(2, 0)</b>."),
        ("Which line is steepest?", "<i>y</i> = −5<i>x</i> + 1", ["<i>y</i> = 4<i>x</i>", "<i>y</i> = 3<i>x</i> + 9", "<i>y</i> = <i>x</i> + 10"], "Steepness depends on the size of the gradient, ignoring its sign. |−5| is the biggest: <b><i>y</i> = −5<i>x</i> + 1</b>."),
        ("Which line slopes down from left to right?", "<i>y</i> = 7 − 2<i>x</i>", ["<i>y</i> = 2<i>x</i> − 7", "<i>y</i> = <i>x</i> + 7", "<i>y</i> = 7"], "A negative gradient slopes down: <b><i>y</i> = 7 − 2<i>x</i></b> has gradient −2."),
        ("Does the point (3, 11) lie on <i>y</i> = 4<i>x</i> − 1?", "Yes, because 4 × 3 − 1 = 11", ["No, because 4 × 3 − 1 = 12", "No, because 3 + 11 = 14", "Yes, because 11 − 3 = 8"], "Substitute <i>x</i> = 3: 12 − 1 = 11, which matches. <b>Yes</b>."),
        ("A phone plan costs £15 a month plus 10p per minute. What is the gradient of the graph of cost (£) against minutes?", "0.1", ["15", "10", "1.5"], "Each minute adds 10p = £0.10, so the gradient is <b>0.1</b>."),
        ("£1 = $1.25. On a graph of dollars against pounds, what is the gradient?", "1.25", ["0.8", "1", "125"], "Dollars = 1.25 × pounds, a straight line through (0, 0) with gradient <b>1.25</b>."),
        ("A line has gradient 2 and passes through (0, −4). What is its equation?", "<i>y</i> = 2<i>x</i> − 4", ["<i>y</i> = −4<i>x</i> + 2", "<i>y</i> = 2<i>x</i> + 4", "<i>y</i> = −2<i>x</i> − 4"], "<i>m</i> = 2 and <i>c</i> = −4: <b><i>y</i> = 2<i>x</i> − 4</b>."),
        ("Which two lines are parallel?", "<i>y</i> = 3<i>x</i> + 1 and <i>y</i> = 3<i>x</i> − 5", ["<i>y</i> = 3<i>x</i> + 1 and <i>y</i> = <i>x</i> + 3", "<i>y</i> = 2<i>x</i> and <i>y</i> = −2<i>x</i>", "<i>y</i> = 4 and <i>x</i> = 4"],
         "Parallel lines have the same gradient: <b>3<i>x</i></b> in both."),
        ("Where do <i>y</i> = 2<i>x</i> + 1 and <i>y</i> = 7 meet?", "(3, 7)", ["(7, 3)", "(4, 7)", "(3, 1)"], "2<i>x</i> + 1 = 7, so <i>x</i> = 3. They meet at <b>(3, 7)</b>."),
        ("A water tank holds 500 litres and drains at 25 litres per minute. After how many minutes is it empty?", "20", ["25", "475", "12.5"], "500 − 25<i>t</i> = 0, so <i>t</i> = <b>20 minutes</b>."),
        ("What is the gradient of a horizontal line?", "0", ["1", "Undefined", "−1"], "A horizontal line does not go up or down, so its gradient is <b>0</b>."),
        ("The line through (1, 4) and (3, 10) has equation…", "<i>y</i> = 3<i>x</i> + 1", ["<i>y</i> = 3<i>x</i> + 4", "<i>y</i> = 6<i>x</i> − 2", "<i>y</i> = 2<i>x</i> + 2"], "Gradient = 6 ÷ 2 = 3. 4 = 3 × 1 + <i>c</i>, so <i>c</i> = 1. <b><i>y</i> = 3<i>x</i> + 1</b>."),
    ]
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    g = grid(lines=[(-2, -5, 3, 5, BLUE, "")])
    its.append(T("What is the gradient of the line?%s" % fig(g), "2", [fr(1, 2), "−2", "−1"], "From (0, −1) to (1, 1) the line goes up 2 for 1 across: gradient <b>2</b>."))
    g2 = grid(lines=[(-5, 3.5, 5, -1.5, BLUE, "")])
    its.append(T("What is the gradient of the line?%s" % fig(g2), MINUS + fr(1, 2), [fr(1, 2), "−2", "1"], "It goes down 1 for every 2 across: gradient <b>−1/2</b>.".replace("−1/2", MINUS + fr(1, 2))))
    g3 = grid(lines=[(-4, 5, 5, -4, BLUE, "")])
    its.append(T("What is the equation of the line?%s" % fig(g3), "<i>y</i> = −<i>x</i> + 1", ["<i>y</i> = <i>x</i> + 1", "<i>y</i> = −<i>x</i> − 1", "<i>y</i> = <i>x</i> − 1"], "It crosses the <i>y</i>-axis at 1 and goes down 1 for each 1 across: <b><i>y</i> = −<i>x</i> + 1</b>."))
    g4 = grid(lines=[(-5, -2, 5, -2, BLUE, "")])
    its.append(T("What is the equation of the line?%s" % fig(g4), "<i>y</i> = −2", ["<i>x</i> = −2", "<i>y</i> = −2<i>x</i>", "<i>y</i> = 2"], "Every point has <i>y</i> = −2, so <b><i>y</i> = −2</b>."))
    return its


def body():
    g = grid(lines=[(-3, -5, 4, 9, BLUE, "y = 2x + 1")][:0] + [(-3, -5, 2, 5, BLUE, "")])
    return lesson(
        "<p>Every straight line (except vertical ones) can be written as <b><i>y</i> = <i>mx</i> + <i>c</i></b>. "
        "<i>m</i> is the <b>gradient</b> (how far up for 1 across; negative means it slopes down). "
        "<i>c</i> is the <b><i>y</i>-intercept</b> (where it crosses the <i>y</i>-axis).</p>"
        "<p>Gradient from two points = change in <i>y</i> ÷ change in <i>x</i>. Parallel lines have the same gradient.</p>"
        + fig(g),
        [("Find the gradient and <i>y</i>-intercept of <i>y</i> = 2<i>x</i> + 1 (shown above).", ["<i>m</i> = 2, <i>c</i> = 1."], "Gradient 2, crosses at (0, 1)"),
         ("Find the gradient through (1, 3) and (4, 12).", ["(12 − 3) ÷ (4 − 1) = 9 ÷ 3."], "3"),
         ("Find the line with gradient 3 through (2, 5).", ["5 = 3 × 2 + <i>c</i>, so <i>c</i> = −1."], "<i>y</i> = 3<i>x</i> − 1")],
        ["Swapping <i>m</i> and <i>c</i>: in <i>y</i> = 2<i>x</i> + 5 the gradient is 2, not 5.",
         "Using change in <i>x</i> ÷ change in <i>y</i> for the gradient.",
         "Missing the minus sign when the line slopes down.",
         "Reading the gradient of 2<i>y</i> = 6<i>x</i> + 4 as 6. Divide by 2 first: the gradient is 3."])


def main():
    sets = [S("Gradient and y-intercept", collect(one_mc, 20, R)),
            S("Gradient from two points", collect(one_grad, 20, R)),
            S("Equation from a graph", collect(one_from_graph, 20, R)),
            S("Parallel lines and lines through a point", collect(one_parallel, 20, R)),
            S("Real-life linear graphs", problems())]
    make(8, "linear-graphs", 7, "A",
         "Linear Graphs: Gradient, y-Intercept and y = mx + c",
         "Year 8 Linear Graphs Worksheets: Gradient, y-Intercept, y = mx + c and Parallel Lines",
         "Linear graphs y = mx + c",
         "Recognise, sketch and produce graphs of linear functions of one variable with appropriate scaling, using "
         "equations in x and y and the Cartesian plane; find the equation of the line through two given points, or "
         "through one point with a given gradient; interpret gradients and intercepts of linear functions graphically "
         "and algebraically.",
         "Free Year 8 linear graphs worksheets with grids: gradient and y-intercept, gradient from two points, equation "
         "of a line from its graph, parallel lines and real-life graphs. 100 questions with answers.",
         "y = mx + c: m is the gradient and c is where the line crosses the y-axis.",
         "Gradient = change in y ÷ change in x. Parallel lines have the same gradient.",
         body(),
         [("What do m and c mean in y = mx + c?", "m is the gradient (steepness) and c is the y-intercept, where the line crosses the y-axis."),
          ("How do I find the gradient from two points?", "Divide the change in y by the change in x. From (1, 3) to (4, 12): 9 ÷ 3 = 3."),
          ("What does a negative gradient look like?", "The line slopes down from left to right."),
          ("How do I find the equation of a line through a point?", "Put the gradient and the point into y = mx + c and solve for c.")],
         sets, R)


if __name__ == "__main__":
    main()
