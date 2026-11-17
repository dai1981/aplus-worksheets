# -*- coding: utf-8 -*-
"""
UK Year 7 Maths: Coordinates and Straight-Line Graphs (KS3 Algebra)
  python3 tools/gen_uk_maths_y7_coordinates_and_straight_line_graphs.py
Reading and plotting coordinates in all four quadrants, midpoints and missing vertices, the lines
x = a, y = b, y = x and y = −x, tables of values for y = mx + c, and checking whether a point is on a line.
Wrong answers come from real mistakes: swapping x and y, dropping a negative sign, and mixing up x = 3 (a
vertical line) with y = 3 (a horizontal line).
"""
import random
from fractions import Fraction as F
from uk_ks3 import num, mcq, B, S, make, lesson, collect, QN, T, svg_wrap, line, text, fig, GREEN, INK, RED, BLUE, MINUS, expr

R = random.Random(71801)
U = 24
LO, HI = -5, 5


def P(x, y):
    return "(%s, %s)" % (num(x), num(y))


def grid(points=(), lines=(), lo=LO, hi=HI, label="coordinate grid"):
    n = hi - lo
    W = n * U + 60
    ox = 30 - lo * U
    oy = 30 + hi * U
    X = lambda v: ox + v * U
    Y = lambda v: oy - v * U
    s = []
    for v in range(lo, hi + 1):
        s.append(line(X(v), Y(lo), X(v), Y(hi), "#d5d5d5", 1))
        s.append(line(X(lo), Y(v), X(hi), Y(v), "#d5d5d5", 1))
    s.append(line(X(lo) - 6, Y(0), X(hi) + 10, Y(0), INK, 2))
    s.append(line(X(0), Y(lo) + 6, X(0), Y(hi) - 10, INK, 2))
    for v in range(lo, hi + 1):
        if v == 0:
            continue
        s.append(text(X(v), Y(0) + 16, num(v), 11, weight=400))
        s.append(text(X(0) - 10, Y(v) + 4, num(v), 11, weight=400, anchor="end"))
    s.append(text(X(hi) + 14, Y(0) + 5, "<tspan font-style='italic'>x</tspan>", 14))
    s.append(text(X(0), Y(hi) - 14, "<tspan font-style='italic'>y</tspan>", 14))
    for (x1, y1, x2, y2, col, lab) in lines:
        s.append(line(X(x1), Y(y1), X(x2), Y(y2), col, 3))
        if lab:
            s.append(text(X(x2) + (8 if x2 >= x1 else -8), Y(y2) - 6, lab, 13, col=col, anchor="start" if x2 >= x1 else "end"))
    for (x, y, lab) in points:
        s.append("<circle cx='%.1f' cy='%.1f' r='5' fill='%s'/>" % (X(x), Y(y), RED))
        s.append(text(X(x) + 9, Y(y) - 7, lab, 15, col=RED, anchor="start"))
    return svg_wrap(W, n * U + 60, "".join(s), label)


def pt(r):
    while True:
        x, y = r.randint(-5, 5), r.randint(-5, 5)
        if x and y:
            return x, y


# ------------------------------------------------------------ set 1: reading coordinates
def one_read(r):
    pts = []
    while len(pts) < 4:
        p = pt(r)
        if p not in pts and (p[1], p[0]) not in pts:
            pts.append(p)
    names = ["A", "B", "C", "D"]
    k = r.randrange(4)
    x, y = pts[k]
    if x == y:
        return None
    g = grid([(a, b, n) for (a, b), n in zip(pts, names)])
    q = "What are the coordinates of point %s?%s" % (B(names[k]), fig(g))
    e = "Go across first (<i>x</i> = %s), then up or down (<i>y</i> = %s): <b>%s</b>." % (num(x), num(y), P(x, y))
    return T(q, P(x, y), [P(y, x), P(-x, y), P(x, -y)], e)


def one_quadrant(r):
    x, y = pt(r)
    q = "In which quadrant is the point %s?" % B(P(x, y))
    quad = {(1, 1): "First (top right)", (-1, 1): "Second (top left)", (-1, -1): "Third (bottom left)", (1, -1): "Fourth (bottom right)"}
    key = (1 if x > 0 else -1, 1 if y > 0 else -1)
    right = quad[key]
    return T(q, right, [v for k, v in quad.items() if k != key],
             "<i>x</i> is %s and <i>y</i> is %s, so the point is <b>%s</b>." % ("positive" if x > 0 else "negative", "positive" if y > 0 else "negative", right.lower()))


# ------------------------------------------------------------ set 2: midpoints and missing vertices
def one_mid(r):
    x1, y1 = r.randint(-6, 6), r.randint(-6, 6)
    x2, y2 = x1 + 2 * r.randint(-4, 4), y1 + 2 * r.randint(-4, 4)
    if (x1, y1) == (x2, y2) or x1 == x2 and y1 == y2:
        return None
    mx, my = F(x1 + x2, 2), F(y1 + y2, 2)
    q = "Find the midpoint of %s and %s." % (B(P(x1, y1)), B(P(x2, y2)))
    e = "Add the <i>x</i>s and halve, add the <i>y</i>s and halve: (%s ÷ 2, %s ÷ 2) = <b>%s</b>." % (num(x1 + x2), num(y1 + y2), P(mx, my))
    wr = [P(x2 - x1, y2 - y1), P(F(x2 - x1, 2), F(y2 - y1, 2)), P(my, mx) if mx != my else P(mx + 1, my), P(x1 + x2, y1 + y2)]
    return T(q, P(mx, my), [w for w in wr if w != P(mx, my)][:3], e)


def one_vertex(r):
    x1, y1 = r.randint(-5, 1), r.randint(-5, 1)
    w, h = r.randint(2, 5), r.randint(2, 5)
    shape = "square" if r.random() < 0.4 else "rectangle"
    if shape == "square":
        h = w
    corners = [(x1, y1), (x1 + w, y1), (x1 + w, y1 + h), (x1, y1 + h)]
    k = r.randrange(4)
    given = [c for i, c in enumerate(corners) if i != k]
    ans = corners[k]
    q = "Three corners of a %s are %s. What are the coordinates of the fourth corner?" % (shape, ", ".join(P(*c) for c in given[:2]) + " and " + P(*given[2]))
    e = "The sides are horizontal and vertical, so the missing corner shares an <i>x</i>-coordinate with one corner and a <i>y</i>-coordinate with another: <b>%s</b>." % P(*ans)
    wr = [P(ans[1], ans[0]), P(-ans[0], ans[1]), P(ans[0], -ans[1]) if ans[1] else P(ans[0] + w, ans[1]), P(ans[0] + 1, ans[1] + 1)]
    return T(q, P(*ans), [x for x in wr if x != P(*ans) and x not in [P(*c) for c in given]][:3], e)


# ------------------------------------------------------------ set 3: x = a, y = b, y = x, y = -x
def one_lines(r):
    kind = r.choice(["v", "h", "d", "d2", "v", "h"])
    c = r.choice([v for v in range(-4, 5) if v])
    if kind == "v":
        lines = [(c, -5, c, 5, BLUE, "")]
        right = "<i>x</i> = %s" % num(c)
        wr = ["<i>y</i> = %s" % num(c), "<i>x</i> = %s" % num(-c), "<i>y</i> = <i>x</i> + %s" % num(c) if c > 0 else "<i>y</i> = %s<i>x</i>" % num(c)]
        e = "Every point on the line has <i>x</i>-coordinate %s, so it is <b>%s</b>. Lines <i>x</i> = … are vertical." % (num(c), right)
    elif kind == "h":
        lines = [(-5, c, 5, c, BLUE, "")]
        right = "<i>y</i> = %s" % num(c)
        wr = ["<i>x</i> = %s" % num(c), "<i>y</i> = %s" % num(-c), "<i>y</i> = %s<i>x</i>" % num(c) if c not in (1, -1) else "<i>y</i> = <i>x</i>"]
        e = "Every point on the line has <i>y</i>-coordinate %s, so it is <b>%s</b>. Lines <i>y</i> = … are horizontal." % (num(c), right)
    elif kind == "d":
        lines = [(-5, -5, 5, 5, BLUE, "")]
        right = "<i>y</i> = <i>x</i>"
        wr = ["<i>y</i> = %s<i>x</i>" % MINUS, "<i>x</i> = 0", "<i>y</i> = 0"]
        e = "The points (1, 1), (2, 2), (−3, −3) are on it: <i>y</i> is the same as <i>x</i>, so <b><i>y</i> = <i>x</i></b>."
    else:
        lines = [(-5, 5, 5, -5, BLUE, "")]
        right = "<i>y</i> = %s<i>x</i>" % MINUS
        wr = ["<i>y</i> = <i>x</i>", "<i>x</i> = %s<i>y</i>" % "", "<i>y</i> = 0"]
        wr[1] = "<i>x</i> = 0"
        e = "The points (1, −1), (−2, 2) are on it: <i>y</i> is the negative of <i>x</i>, so <b><i>y</i> = −<i>x</i></b>."
    g = grid(lines=lines)
    return T("What is the equation of the line?%s" % fig(g), right, wr, e)


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


# ------------------------------------------------------------ set 4: tables of values, y = mx + c
def eq(m, c):
    return "<i>y</i> = " + expr([(m, "<i>x</i>"), (c, "")])


def one_table(r):
    m = r.choice([2, 3, 4, -2, -1, F(1, 2), 5])
    c = r.randint(-5, 6)
    x = r.choice([-3, -2, -1, 0, 1, 2, 3, 4, 5])
    if F(m * x).denominator != 1:
        return None
    y = m * x + c
    q = "For the line %s, find %s when %s." % (B(eq(m, c)), "<i>y</i>", "<i>x</i> = %s" % num(x))
    e = "Substitute: %s × %s %s %s = <b>%s</b>." % (num(m), "(%s)" % num(x) if x < 0 else num(x), "+" if c >= 0 else MINUS, num(abs(c)), num(y))
    return QN(q, y, [m * (x + c), x + c, m * x - c if c else -y], e)


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
    q = "Which point lies on the line %s?" % B(eq(m, c))
    e = "Substitute the <i>x</i>-coordinate: %s × %s %s %s = %s, which matches. So <b>%s</b>." % (
        num(m), "(%s)" % num(good[0]) if good[0] < 0 else num(good[0]), "+" if c >= 0 else MINUS, num(abs(c)), num(good[1]), P(*good))
    return T(q, P(*good), [P(*b) for b in bad], e)


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    data = [
        ("Point A is (3, −2). It is moved 4 units left and 5 units up. Where is it now?", "(−1, 3)", ["(7, 3)", "(−1, −7)", "(3, −1)"], "<i>x</i>: 3 − 4 = −1. <i>y</i>: −2 + 5 = 3. So <b>(−1, 3)</b>."),
        ("Which point is on the <i>y</i>-axis?", "(0, −4)", ["(−4, 0)", "(4, 4)", "(−4, −4)"], "Every point on the <i>y</i>-axis has <i>x</i> = 0: <b>(0, −4)</b>."),
        ("Which point is on the <i>x</i>-axis?", "(6, 0)", ["(0, 6)", "(6, 6)", "(−6, 6)"], "Every point on the <i>x</i>-axis has <i>y</i> = 0: <b>(6, 0)</b>."),
        ("Where do the lines <i>x</i> = 3 and <i>y</i> = −2 cross?", "(3, −2)", ["(−2, 3)", "(3, 2)", "(0, 0)"], "The point has <i>x</i> = 3 and <i>y</i> = −2: <b>(3, −2)</b>."),
        ("What is the equation of the <i>x</i>-axis?", "<i>y</i> = 0", ["<i>x</i> = 0", "<i>y</i> = <i>x</i>", "<i>x</i> = 1"], "Every point on the <i>x</i>-axis has <i>y</i>-coordinate 0, so it is <b><i>y</i> = 0</b>."),
        ("The point (<i>k</i>, 7) lies on the line <i>y</i> = 2<i>x</i> + 1. Find <i>k</i>.", "3", ["15", "4", "−3"], "2<i>k</i> + 1 = 7, so 2<i>k</i> = 6 and <i>k</i> = <b>3</b>."),
        ("The point (−2, <i>m</i>) lies on the line <i>y</i> = 3<i>x</i> + 5. Find <i>m</i>.", "−1", ["11", "1", "−6"], "<i>m</i> = 3 × (−2) + 5 = −6 + 5 = <b>−1</b>."),
        ("A line goes through (0, 1), (1, 3), (2, 5) and (3, 7). What is its equation?", "<i>y</i> = 2<i>x</i> + 1", ["<i>y</i> = <i>x</i> + 2", "<i>y</i> = 2<i>x</i>", "<i>y</i> = <i>x</i> + 1"],
         "<i>y</i> goes up by 2 each time <i>x</i> goes up by 1, and <i>y</i> = 1 when <i>x</i> = 0: <b><i>y</i> = 2<i>x</i> + 1</b>."),
        ("Which line does NOT pass through the origin (0, 0)?", "<i>y</i> = <i>x</i> + 1", ["<i>y</i> = <i>x</i>", "<i>y</i> = −3<i>x</i>", "<i>y</i> = 5<i>x</i>"], "When <i>x</i> = 0, <i>y</i> = <i>x</i> + 1 gives 1, not 0. So <b><i>y</i> = <i>x</i> + 1</b>."),
        ("A, B and C are (1, 1), (5, 1) and (5, 4). What is the length of AB?", "4 units", ["3 units", "5 units", "6 units"], "A and B have the same <i>y</i>, so AB = 5 − 1 = <b>4 units</b>."),
        ("The midpoint of AB is (2, 3). A is (0, 1). What are the coordinates of B?", "(4, 5)", ["(1, 2)", "(2, 2)", "(−2, −1)"], "From A to the midpoint is +2 and +2. Do it again: <b>(4, 5)</b>."),
        ("Which is the steepest line?", "<i>y</i> = 4<i>x</i>", ["<i>y</i> = <i>x</i> + 4", "<i>y</i> = 2<i>x</i> + 3", "<i>y</i> = 3<i>x</i> − 1"], "The number in front of <i>x</i> shows how steep a line is. The biggest is 4: <b><i>y</i> = 4<i>x</i></b>."),
        ("Three points are (−1, −1), (2, 2) and (4, 4). Which line are they on?", "<i>y</i> = <i>x</i>", ["<i>y</i> = −<i>x</i>", "<i>x</i> = 2", "<i>y</i> = 2<i>x</i>"], "Each has <i>y</i> equal to <i>x</i>: <b><i>y</i> = <i>x</i></b>."),
        ("Which line is parallel to <i>y</i> = 3?", "<i>y</i> = −1", ["<i>x</i> = 3", "<i>y</i> = 3<i>x</i>", "<i>y</i> = <i>x</i> + 3"], "<i>y</i> = 3 is horizontal. Another horizontal line is <b><i>y</i> = −1</b>."),
        ("A square has corners at (1, 1), (4, 1) and (4, 4). What is its area?", "9 square units", ["12 square units", "16 square units", "6 square units"], "The side is 4 − 1 = 3, so the area is 3 × 3 = <b>9 square units</b>."),
        ("Complete the table for <i>y</i> = 2<i>x</i> − 3 when <i>x</i> = −1, 0, 1, 2.", "−5, −3, −1, 1", ["−1, 0, 1, 2", "5, 3, 1, −1", "−5, −3, 1, 3"], "2 × (−1) − 3 = −5, then add 2 each time: <b>−5, −3, −1, 1</b>."),
    ]
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    g = grid(points=[(-3, 2, "P"), (4, -1, "Q")])
    its.append(T("What are the coordinates of the midpoint of P and Q?%s" % fig(g), "(0.5, 0.5)", ["(1, 1)", "(3.5, −1.5)", "(7, −3)"],
                 "((−3 + 4) ÷ 2, (2 + (−1)) ÷ 2) = <b>(0.5, 0.5)</b>."))
    g2 = grid(lines=[(-5, -4, 5, 1, BLUE, "")])
    its.append(T("Which point is on the line shown?%s" % fig(g2), "(3, 0)", ["(0, 3)", "(3, 1)", "(−3, 0)"],
                 "Follow the line: when <i>x</i> = 3 it crosses the <i>x</i>-axis, so <b>(3, 0)</b>."))
    g3 = grid(points=[(2, 3, "A"), (-2, 3, "B"), (-2, -1, "C")])
    its.append(T("A, B and C are three corners of a square. Where is the fourth corner?%s" % fig(g3), "(2, −1)", ["(−1, 2)", "(2, 1)", "(−2, −3)"],
                 "The square has sides of 4. The fourth corner is below A and to the right of C: <b>(2, −1)</b>."))
    g4 = grid(points=[(0, -3, "D"), (-4, 0, "E")])
    its.append(T("What are the coordinates of point E?%s" % fig(g4), "(−4, 0)", ["(0, −4)", "(4, 0)", "(−4, −4)"],
                 "E is 4 to the left on the <i>x</i>-axis: <b>(−4, 0)</b>."))
    return its


def body():
    return lesson(
        "<p>Coordinates are written (<i>x</i>, <i>y</i>): go <b>across</b> first, then <b>up or down</b>. "
        "Left of the <i>y</i>-axis, <i>x</i> is negative; below the <i>x</i>-axis, <i>y</i> is negative.</p>"
        "<p><i>x</i> = 3 is a <b>vertical</b> line; <i>y</i> = 3 is a <b>horizontal</b> line. The midpoint of two points is the "
        "mean of the <i>x</i>s and the mean of the <i>y</i>s.</p>"
        + fig(grid(points=[(3, 2, "A"), (-4, -1, "B")], lines=[(2, -5, 2, 5, BLUE, "x = 2")])),
        [("What are the coordinates of B above?", ["4 to the left, 1 down."], "(−4, −1)"),
         ("Find the midpoint of (2, 5) and (8, −1).", ["(2 + 8) ÷ 2 = 5.", "(5 + (−1)) ÷ 2 = 2."], "(5, 2)"),
         ("Find <i>y</i> on the line <i>y</i> = 2<i>x</i> − 1 when <i>x</i> = −3.", ["2 × (−3) − 1 = −7."], "−7")],
        ["Swapping the coordinates: (3, 2) is 3 across and 2 up, not 2 across and 3 up.",
         "Forgetting a negative sign for points left of or below the axes.",
         "Thinking <i>x</i> = 3 is horizontal. It is vertical, because <i>x</i> is always 3.",
         "Subtracting instead of adding when finding a midpoint."])


def main():
    sets = [S("Reading coordinates", collect(one_read, 15, R) + collect(one_quadrant, 5, R)),
            S("Midpoints and missing corners", collect(one_mid, 12, R) + collect(one_vertex, 8, R)),
            S("Horizontal, vertical and diagonal lines", collect(one_lines, 12, R) + collect(one_line_text, 8, R)),
            S("Tables of values for straight lines", collect(one_table, 12, R) + collect(one_onl, 8, R)),
            S("Problems", problems())]
    make(7, "coordinates-and-straight-line-graphs", 18, "A",
         "Coordinates and Straight-Line Graphs: Four Quadrants, Midpoints and y = mx + c",
         "Year 7 Coordinates Worksheets: Four Quadrants, Midpoints, x = a, y = b and Straight-Line Graphs",
         "Coordinates and straight-line graphs",
         "Work with coordinates in all four quadrants; recognise, sketch and produce graphs of linear functions of one "
         "variable with appropriate scaling, using equations in x and y and the Cartesian plane.",
         "Free Year 7 coordinates worksheets with grids: read coordinates in four quadrants, midpoints and missing corners, "
         "lines x = a, y = b, y = x and y = −x, and tables of values for straight-line graphs. 100 questions with answers.",
         "(x, y): go across first, then up or down.",
         "x = 3 is a vertical line and y = 3 is a horizontal line. The midpoint is the mean of the coordinates.",
         body(),
         [("Which comes first, x or y?", "x comes first. Go along the corridor, then up (or down) the stairs."),
          ("What does the line x = 3 look like?", "A vertical line through 3 on the x-axis. Every point on it has x-coordinate 3."),
          ("How do I find a midpoint?", "Add the two x-coordinates and halve, then add the two y-coordinates and halve."),
          ("How do I know if a point is on a line?", "Substitute the x-coordinate into the equation. If you get the y-coordinate, the point is on the line.")],
         sets, R)


if __name__ == "__main__":
    main()
