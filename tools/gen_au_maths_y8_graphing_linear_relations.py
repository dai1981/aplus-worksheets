# -*- coding: utf-8 -*-
"""
AU Year 8 Maths: Graphing Linear Relations (Australian Curriculum v9.0: AC9M8A02)
  python3 tools/gen_au_maths_y8_graphing_linear_relations.py
Tables of values, checking whether a point is on a line, the equation of a line from its graph, how the
numbers in y = mx + c change the graph, and real-life linear relations (including solving graphically).
Wrong answers come from real mistakes: swapping m and c, using change in x over change in y, losing the
sign of a negative gradient, and not rearranging to y = … first.
"""
import random
from fractions import Fraction as F
from au_hs import num, mcq, B, S, make, lesson, collect, QN, T, fr, expr, fig, BLUE, RED, MINUS
from gen_uk_maths_y7_coordinates_and_straight_line_graphs import grid

R = random.Random(80801)
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
# ------------------------------------------------------------ set 1: tables of values
def eq7(m, c):
    return "<i>y</i> = " + expr([(m, "<i>x</i>"), (c, "")])


def one_table(r):
    m = r.choice([2, 3, 4, -2, -1, F(1, 2), 5])
    c = r.randint(-5, 6)
    x = r.choice([-3, -2, -1, 0, 1, 2, 3, 4, 5])
    if F(m * x).denominator != 1:
        return None
    y = m * x + c
    q = "For the line %s, find %s when %s." % (B(eq7(m, c)), "<i>y</i>", "<i>x</i> = %s" % num(x))
    e = "Substitute: %s × %s %s %s = <b>%s</b>." % (num(m), "(%s)" % num(x) if x < 0 else num(x), "+" if c >= 0 else MINUS, num(abs(c)), num(y))
    return QN(q, y, [m * (x + c), x + c, m * x - c if c else -y], e)


# ------------------------------------------------------------ set 2: points on a line
def one_onl(r):
    m = r.choice([2, 3, -2, -3, 4, 1])
    c = r.randint(-5, 5)
    xs = r.sample(range(-4, 5), 4)
    good = (xs[0], m * xs[0] + c)
    bad = [(xs[1], m * xs[1] + c + r.choice([-2, -1, 1, 2])), (m * xs[2] + c, xs[2]) if m * xs[2] + c != xs[2] else (xs[2], xs[2] + 3),
           (xs[3], m * xs[3] - c if c else m * xs[3] + 1)]
    bad = [b for b in bad if b[1] != m * b[0] + c]
    if len({P(*b) for b in bad}) < 3:
        return None
    q = "Which point lies on the line %s?" % B(eq7(m, c))
    e = "Substitute the <i>x</i>-coordinate: %s × %s %s %s = %s, which matches. So <b>%s</b>." % (
        num(m), "(%s)" % num(good[0]) if good[0] < 0 else num(good[0]), "+" if c >= 0 else MINUS, num(abs(c)), num(good[1]), P(*good))
    return T(q, P(*good), [P(*b) for b in bad], e)


def one_line_text(r):
    c = r.choice([v for v in range(-6, 7) if v])
    kind = r.random()
    if kind < 0.5:
        k = r.choice(["x", "y"])
        pts = [(c, r.randint(-6, 6)) if k == "x" else (r.randint(-6, 6), c) for _ in range(3)]
        bad = [(r.randint(-6, 6), c) if k == "x" else (c, r.randint(-6, 6)) for _ in range(3)]
        good = pts[0]
        wrong = [b for b in bad if (b[0] != c if k == "x" else b[1] != c)]
        if len({P(*w) for w in wrong}) < 3:
            return None
        q = "Which point lies on the line %s?" % B("<i>%s</i> = %s" % (k, num(c)))
        e = "On the line <i>%s</i> = %s, the <i>%s</i>-coordinate is always %s: <b>%s</b>." % (k, num(c), k, num(c), P(*good))
        return T(q, P(*good), [P(*w) for w in wrong], e)
    q = "Which line is %s?" % B("vertical" if c > 0 else "horizontal")
    right = ("<i>x</i> = %s" if c > 0 else "<i>y</i> = %s") % num(c)
    wr = [("<i>y</i> = %s" if c > 0 else "<i>x</i> = %s") % num(c), "<i>y</i> = <i>x</i>", ("<i>y</i> = %s" if c > 0 else "<i>x</i> = %s") % num(-c)]
    e = "<i>x</i> = a number is a vertical line; <i>y</i> = a number is a horizontal line. So <b>%s</b>." % right
    return T(q, right, wr, e)


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


# ------------------------------------------------------------ set 4: gradient and y-intercept
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


# ------------------------------------------------------------ set 5: real-life linear relations
def problems():
    its = []
    data = [
        ("A taxi fare in Brisbane is given by <i>C</i> = 2<i>d</i> + 3, where <i>d</i> is kilometres. What does the 3 represent?", "A fixed charge of $3", ["The cost per kilometre", "The number of kilometres", "The total cost"],
         "When <i>d</i> = 0, <i>C</i> = 3. It is the <b>fixed charge</b> you pay before travelling."),
        ("A taxi fare is given by <i>C</i> = 2<i>d</i> + 3, where <i>d</i> is kilometres. What does the 2 represent?", "The cost per kilometre, $2", ["A fixed charge of $2", "2 kilometres", "The total cost"],
         "The gradient is the rate of change: each extra kilometre costs <b>$2</b>."),
        ("A candle is 20 cm tall and burns 2 cm every hour. Which equation gives its height <i>h</i> after <i>t</i> hours?", "<i>h</i> = 20 − 2<i>t</i>", ["<i>h</i> = 2<i>t</i> + 20", "<i>h</i> = 20<i>t</i> − 2", "<i>h</i> = 2 − 20<i>t</i>"],
         "Start at 20 and go down 2 each hour: <b><i>h</i> = 20 − 2<i>t</i></b>, a negative gradient."),
        ("A plumber charges a $40 call-out fee plus $25 per hour. Which equation gives the cost <i>C</i> for <i>h</i> hours?", "<i>C</i> = 25<i>h</i> + 40", ["<i>C</i> = 40<i>h</i> + 25", "<i>C</i> = 65<i>h</i>", "<i>C</i> = 25<i>h</i> − 40"],
         "$25 for each hour, plus $40 once: <b><i>C</i> = 25<i>h</i> + 40</b>."),
        ("The line <i>y</i> = 3<i>x</i> − 6 crosses the <i>x</i>-axis at…", "(2, 0)", ["(0, −6)", "(−6, 0)", "(−2, 0)"], "On the <i>x</i>-axis <i>y</i> = 0: 3<i>x</i> − 6 = 0, so <i>x</i> = 2. <b>(2, 0)</b>."),
        ("Which line is steepest?", "<i>y</i> = −5<i>x</i> + 1", ["<i>y</i> = 4<i>x</i>", "<i>y</i> = 3<i>x</i> + 9", "<i>y</i> = <i>x</i> + 10"], "Steepness depends on the size of the gradient, ignoring its sign. |−5| is the biggest: <b><i>y</i> = −5<i>x</i> + 1</b>."),
        ("Which line slopes down from left to right?", "<i>y</i> = 7 − 2<i>x</i>", ["<i>y</i> = 2<i>x</i> − 7", "<i>y</i> = <i>x</i> + 7", "<i>y</i> = 7"], "A negative gradient slopes down: <b><i>y</i> = 7 − 2<i>x</i></b> has gradient −2."),
        ("Does the point (3, 11) lie on <i>y</i> = 4<i>x</i> − 1?", "Yes, because 4 × 3 − 1 = 11", ["No, because 4 × 3 − 1 = 12", "No, because 3 + 11 = 14", "Yes, because 11 − 3 = 8"], "Substitute <i>x</i> = 3: 12 − 1 = 11, which matches. <b>Yes</b>."),
        ("A phone plan costs $15 a month plus 10c per minute. What is the gradient of the graph of cost ($) against minutes?", "0.1", ["15", "10", "1.5"], "Each minute adds 10c = $0.10, so the gradient is <b>0.1</b>."),
        ("1 Australian dollar is worth 0.6 euros. On a graph of euros against Australian dollars, what is the gradient?", "0.6", ["1.67", "1", "60"], "Euros = 0.6 × dollars, a straight line through (0, 0) with gradient <b>0.6</b>."),
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
    return lesson(
        "<p>A <b>linear relation</b> such as <i>y</i> = 2<i>x</i> + 1 gives a straight-line graph. Make a <b>table of values</b>: "
        "choose some <i>x</i> values, substitute to find each <i>y</i>, plot the points and join them with a ruler.</p>"
        "<p>A point is on the line if its coordinates make the rule true. In <i>y</i> = <i>mx</i> + <i>c</i>, <i>c</i> is where the line "
        "crosses the <i>y</i>-axis and <i>m</i> (the <b>gradient</b>) tells you how steep it is: up <i>m</i> for every 1 across. "
        "A negative gradient slopes down from left to right.</p>"
        "<p>Where two lines cross, both rules are true. Reading the crossing point is a <b>graphical</b> way to solve an equation.</p>",
        [("Complete the table for <i>y</i> = 3<i>x</i> − 2 when <i>x</i> = −1, 0, 1, 2.", ["Substitute each <i>x</i>: 3 × (−1) − 2 = −5, and so on."], "−5, −2, 1, 4"),
         ("Is (4, 9) on the line <i>y</i> = 2<i>x</i> + 1?", ["2 × 4 + 1 = 9."], "Yes"),
         ("Where do <i>y</i> = 2<i>x</i> + 1 and <i>y</i> = 7 meet?", ["2<i>x</i> + 1 = 7, so <i>x</i> = 3."], "(3, 7)")],
        ["Swapping <i>x</i> and <i>y</i> when plotting or checking a point.",
         "Losing a negative sign: when <i>x</i> = −2, 3<i>x</i> = −6.",
         "Mixing up the gradient and the <i>y</i>-intercept in <i>y</i> = <i>mx</i> + <i>c</i>.",
         "Thinking <i>x</i> = 3 is a horizontal line. It is vertical."])


def main():
    sets = [S("Tables of values", collect(one_table, 20, R)),
            S("Is the point on the line?", collect(one_onl, 14, R) + collect(one_line_text, 6, R)),
            S("Equation from a graph", collect(one_from_graph, 20, R)),
            S("Gradient and y-intercept", collect(one_mc, 20, R)),
            S("Linear relations in real life", problems())]
    make(8, "graphing-linear-relations", 8, "AC9M8A02",
         "Graphing Linear Relations: Tables of Values and Straight-Line Graphs",
         "Year 8 Linear Graphs Worksheets: Tables of Values, Gradient and Real-Life Linear Relations (Free, Answer Key)",
         "Graphing linear relations",
         "graph linear relations on the Cartesian plane using digital tools where appropriate; solve linear equations and "
         "one-variable inequalities using graphical and algebraic techniques; verify solutions by substitution",
         "Free Year 8 maths worksheets on graphing linear relations for the Australian Curriculum (AC9M8A02): tables of values, "
         "points on a line, equations from graphs, gradient and y-intercept, and real-life linear graphs. 100 questions with an answer key.",
         "A linear relation makes a straight line. Use a table of values to plot it.",
         "In y = mx + c, c is where the line crosses the y-axis and m is how steep it is.",
         body(),
         [("How do I graph a linear relation?", "Make a table of values: choose a few x values, work out y for each, plot the points and join them with a straight line."),
          ("How do I check if a point is on a line?", "Substitute the x-coordinate into the rule. If you get the y-coordinate, the point is on the line."),
          ("What do m and c mean in y = mx + c?", "m is the gradient (how far the line goes up for each 1 across) and c is the y-intercept (where it crosses the y-axis)."),
          ("How can a graph solve an equation?", "Graph both sides as lines. The x-coordinate where they cross is the solution.")],
         sets, R)


if __name__ == "__main__":
    main()
