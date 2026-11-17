# -*- coding: utf-8 -*-
"""
UK Year 9 Maths: Quadratic Graphs (KS3 Algebra)
  python3 tools/gen_uk_maths_y9_quadratic_graphs.py
Tables of values for y = x² + bx + c, reading roots, the y-intercept, the turning point and the line of symmetry
from a graph, solving x² + bx + c = k with a horizontal line, and problems.
Wrong answers come from real mistakes: (−3)² = −9, giving roots with the wrong signs from factorised form,
swapping the coordinates of the turning point, reading the y-intercept as a root, and giving only one solution.
"""
import random
from uk_ks3 import num, B, S, make, lesson, collect, QN, T, svg_wrap, line, text, fig, INK, RED, BLUE, expr

R = random.Random(90601)
X = "<i>x</i>"
X2 = "<i>x</i><sup>2</sup>"
XLO, XHI, YLO, YHI = -5, 5, -9, 9
UX, UY = 26, 15


def quad(a, b, c):
    return expr([(a, X2), (b, X), (c, "")])


def P(x, y):
    return "(%s, %s)" % (num(x), num(y))


def para_svg(f, hline=None, label="graph of a quadratic"):
    ox = 34 - XLO * UX
    oy = 24 + YHI * UY
    PX = lambda v: ox + v * UX
    PY = lambda v: oy - v * UY
    s = []
    for v in range(XLO, XHI + 1):
        s.append(line(PX(v), PY(YLO), PX(v), PY(YHI), "#dcdcdc", 1))
    for v in range(YLO, YHI + 1):
        s.append(line(PX(XLO), PY(v), PX(XHI), PY(v), "#dcdcdc", 1))
    s.append(line(PX(XLO) - 6, PY(0), PX(XHI) + 10, PY(0), INK, 2))
    s.append(line(PX(0), PY(YLO) + 6, PX(0), PY(YHI) - 8, INK, 2))
    for v in range(XLO, XHI + 1):
        if v:
            s.append(text(PX(v), PY(0) + 15, num(v), 11, weight=400))
    for v in range(YLO, YHI + 1):
        if v and v % 2 == 0:
            s.append(text(PX(0) - 7, PY(v) + 4, num(v), 11, weight=400, anchor="end"))
    s.append(text(PX(XHI) + 14, PY(0) + 5, "x", 14, italic=True))
    s.append(text(PX(0), PY(YHI) - 12, "y", 14, italic=True))
    if hline is not None:
        s.append(line(PX(XLO), PY(hline), PX(XHI), PY(hline), RED, 2.5))
    segs, cur = [], []
    n = 400
    for i in range(n + 1):
        x = XLO + (XHI - XLO) * i / n
        y = f(x)
        if YLO - 0.01 <= y <= YHI + 0.01:
            cur.append("%.1f,%.1f" % (PX(x), PY(y)))
        elif cur:
            segs.append(cur)
            cur = []
    if cur:
        segs.append(cur)
    for sg in segs:
        if len(sg) > 1:
            s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='3'/>" % (" ".join(sg), BLUE))
    W = (XHI - XLO) * UX + 68
    H = (YHI - YLO) * UY + 48
    return "<svg data-pf='lg'" + svg_wrap(W, H, "".join(s), label)[4:]


def sol(xs):
    xs = sorted(set(xs))
    return " or ".join("%s = %s" % (X, num(v)) for v in xs)


# ------------------------------------------------------------ set 1: tables of values
def one_table(r):
    b, c = r.randint(-4, 4), r.randint(-6, 6)
    x = r.choice([-4, -3, -2, -1, -4, -3, -2, 1, 2, 3, 4])
    if b == 0 and c == 0:
        return None
    y = x * x + b * x + c
    q = "Complete the table of values for %s. What is %s when %s = %s?" % (B("y = " + quad(1, b, c)), "<i>y</i>", X, num(x))
    wr = [-x * x + b * x + c, x * x - b * x + c, 2 * x + b * x + c]
    xs = "(%s)" % num(x) if x < 0 else num(x)
    sub = xs + "<sup>2</sup>"
    if b:
        sub += " %s %s%s" % ("+" if b > 0 else "−", abs(b) if abs(b) != 1 else "", "(%s)" % num(x) if (x < 0 or abs(b) != 1) else num(x))
    if c:
        sub += " %s %d" % ("+" if c > 0 else "−", abs(c))
    e = "Substitute %s = %s: %s = %s." % (X, num(x), sub, num(y))
    if x < 0:
        e += " Remember %s<sup>2</sup> = %s, not %s." % (xs, num(x * x), num(-x * x))
    e += " <b>%s</b>." % num(y)
    return QN(q, y, wr, e)


# ------------------------------------------------------------ set 2: reading a graph
def one_read(r):
    p, q_ = r.randint(-4, 3), r.randint(-3, 4)
    if q_ - p < 2 or q_ - p > 6 or (p + q_) % 2:
        return None
    a = 1 if r.random() < 0.75 else -1
    f = lambda x: a * (x - p) * (x - q_)
    b, c = -a * (p + q_), a * p * q_
    if c == 0:
        return None
    m = (p + q_) // 2
    tv = f(m)
    g = fig(para_svg(f))
    kind = r.choice(["roots", "roots", "turn", "int", "sym"])
    title = "The graph shows %s." % B("y = " + quad(a, b, c))
    if kind == "roots":
        q = g + title + " What are the roots (where the curve crosses the %s-axis)?" % X
        right = sol([p, q_])
        wr = [sol([-p, -q_]), sol([c]) if c not in (p, q_) else sol([c + 1]), "%s = %s only" % (X, num(q_))]
        e = "The curve crosses the %s-axis at %s and %s, so <b>%s</b>." % (X, num(p), num(q_), right)
        if sol([-p, -q_]) == right:
            return None
        return T(q, right, wr, e)
    if kind == "turn":
        q = g + title + " What are the coordinates of the turning point?"
        right = P(m, tv)
        wr = [P(tv, m), P(m, -tv), P(0, c)]
        if right in wr[1:] or tv == m:
            return None
        e = "The %s point of the curve is at %s = %s, %s = %s: <b>%s</b>." % ("lowest" if a > 0 else "highest", X, num(m), "<i>y</i>", num(tv), right)
        return T(q, right, wr, e)
    if kind == "int":
        q = g + title + " Where does the curve cross the %s-axis?" % "<i>y</i>"
        right = P(0, c)
        wr = [P(c, 0), P(p, 0), P(m, tv)]
        if right in wr[1:] or c == 0:
            return None
        e = "Read where the curve meets the %s-axis (when %s = 0): <b>%s</b>. It equals the constant term %s." % ("<i>y</i>", X, right, num(c))
        return T(q, right, wr, e)
    q = g + title + " What is the equation of its line of symmetry?"
    right = "%s = %s" % (X, num(m))
    wr = ["<i>y</i> = %s" % num(m), "%s = %s" % (X, num(-m)) if m else "%s = %s" % (X, num(tv)), "<i>y</i> = %s" % num(tv)]
    e = "The line of symmetry is the vertical line through the turning point: <b>%s</b> (halfway between %s and %s)." % (right, num(p), num(q_))
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 3: features without drawing
def one_feature(r):
    k = r.randint(0, 4)
    if k == 0:
        c = r.randint(-9, 9)
        a = r.choice([1, -1])
        if c == 0:
            return None
        q = "What is the turning point of %s?" % B("y = " + quad(a, 0, c))
        right = P(0, c)
        return T(q, right, [P(c, 0), P(0, -c), P(a, c)], "There is no %s term, so the curve is symmetrical about the %s-axis. When %s = 0, %s = %s: <b>%s</b>." % (X, "<i>y</i>", X, "<i>y</i>", num(c), right))
    if k == 1:
        b, c = r.randint(-6, 6), r.randint(-9, 9)
        if c == 0 or b == 0:
            return None
        q = "Where does %s cross the %s-axis?" % (B("y = " + quad(1, b, c)), "<i>y</i>")
        right = P(0, c)
        return T(q, right, [P(c, 0), P(0, b), P(b, c)], "Put %s = 0: %s = %s. <b>%s</b>." % (X, "<i>y</i>", num(c), right))
    if k == 2:
        p, q_ = r.randint(-6, 6), r.randint(-6, 6)
        if p == q_ or p == -q_ or 0 in (p, q_):
            return None
        q = "What are the roots of %s?" % B("y = (%s)(%s)" % (expr([(1, X), (-p, "")]), expr([(1, X), (-q_, "")])))
        right = sol([p, q_])
        return T(q, right, [sol([-p, -q_]), sol([p, -q_]), sol([p * q_])], "Set each bracket equal to zero: %s = %s or %s = %s. <b>%s</b>." % (X, num(p), X, num(q_), right))
    if k == 3:
        p, q_ = r.randint(-6, 6), r.randint(-6, 6)
        if (p + q_) % 2 or p == q_ or p + q_ == 0:
            return None
        m = (p + q_) // 2
        q = "A quadratic graph has roots %s = %s and %s = %s. What is its line of symmetry?" % (X, num(min(p, q_)), X, num(max(p, q_)))
        right = "%s = %s" % (X, num(m))
        return T(q, right, ["%s = %s" % (X, num(-m)), "<i>y</i> = %s" % num(m), "%s = %s" % (X, num(p + q_))], "The line of symmetry is halfway between the roots: (%s + %s) ÷ 2 = %s. <b>%s</b>." % (num(p), num(q_), num(m), right))
    a = r.choice([1, -1, 2, -2, 3, -3])
    b, c = r.randint(-5, 5), r.randint(-5, 5)
    q = "What shape is the graph of %s?" % B("y = " + quad(a, b, c))
    right = "U-shaped, with a minimum point" if a > 0 else "∩-shaped, with a maximum point"
    other = "∩-shaped, with a maximum point" if a > 0 else "U-shaped, with a minimum point"
    wr = [other, "A straight line", "U-shaped, with a maximum point" if a > 0 else "∩-shaped, with a minimum point"]
    return T(q, right, wr, "The %s term is %s, so the curve is <b>%s</b>." % (X2, "positive" if a > 0 else "negative", right))


# ------------------------------------------------------------ set 4: solving with a graph
def one_solve(r):
    s1, s2 = r.randint(-4, 3), r.randint(-3, 4)
    if s2 - s1 < 2 or s2 - s1 > 6:
        return None
    k = r.randint(-3, 5)
    if -1 <= k <= 1:
        return None
    a = 1
    b, c = -(s1 + s2), s1 * s2 + k
    f = lambda x: (x - s1) * (x - s2) + k
    if min(f(v / 2.0) for v in range(-10, 11)) < YLO:
        return None
    q = fig(para_svg(f, hline=k)) + "The graph shows %s and the line %s. Use the graph to solve %s." % (
        B("y = " + quad(a, b, c)), B("<i>y</i> = %s" % num(k)), B(quad(a, b, c) + " = %s" % num(k)))
    right = sol([s1, s2])
    wr = [sol([-s1, -s2]), "%s = %s only" % (X, num(s2)), "%s = %s" % (X, num(k)) if k not in (s1, s2) else sol([s1 - 1, s2])]
    if sol([-s1, -s2]) == right:
        wr[0] = sol([s1 - 1, s2 + 1])
    e = "Find where the curve meets the line %s. Read down to the %s-axis: <b>%s</b>." % (B("<i>y</i> = %s" % num(k)), X, right)
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 5: problems
def problems():
    Y = "<i>y</i>"
    data = [
        ("Which equation gives a U-shaped curve with its turning point at (0, −4)?", "%s = %s" % (Y, quad(1, 0, -4)), ["%s = %s" % (Y, quad(1, 0, 4)), "%s = %s" % (Y, quad(-1, 0, -4)), "%s = %s" % (Y, expr([(1, X), (-4, "")]))],
         "U-shaped needs a positive %s term, and the turning point (0, −4) needs the constant −4: <b>%s = %s</b>." % (X2, Y, quad(1, 0, -4))),
        ("Which of these is a quadratic equation?", "%s = %s" % (Y, quad(1, 3, 0)), ["%s = 3%s + 1" % (Y, X), "%s = 2<sup><i>x</i></sup>" % Y, "%s = <span class='fr'><span class='fn'>1</span><span class='fd'><i>x</i></span></span>" % Y],
         "A quadratic has %s as its highest power: <b>%s = %s</b>." % (X2, Y, quad(1, 3, 0))),
        ("A ball is thrown. Its height is %s = 20<i>t</i> − 5<i>t</i><sup>2</sup> metres after <i>t</i> seconds. What is its height after 1 second?" % "<i>h</i>", "15 m", ["25 m", "5 m", "20 m"],
         "20 × 1 − 5 × 1<sup>2</sup> = 20 − 5 = <b>15 m</b>."),
        ("A ball's height is <i>h</i> = 20<i>t</i> − 5<i>t</i><sup>2</sup> metres. When does it land (<i>h</i> = 0, <i>t</i> &gt; 0)?", "After 4 seconds", ["After 2 seconds", "After 20 seconds", "After 5 seconds"],
         "5<i>t</i>(4 − <i>t</i>) = 0, so <i>t</i> = 0 or <i>t</i> = 4. It lands <b>after 4 seconds</b>."),
        ("A ball's height is <i>h</i> = 20<i>t</i> − 5<i>t</i><sup>2</sup> metres. What is its greatest height?", "20 m", ["15 m", "40 m", "10 m"],
         "The maximum is halfway between <i>t</i> = 0 and <i>t</i> = 4, at <i>t</i> = 2: 40 − 20 = <b>20 m</b>."),
        ("How many times does %s cross the %s-axis?" % (B("%s = %s" % (Y, quad(1, 0, 4))), X), "0", ["1", "2", "4"],
         "%s is never negative, so %s + 4 is always at least 4. The curve never reaches the %s-axis: <b>0</b>." % (X2, X2, X)),
        ("How many times does %s touch the %s-axis?" % (B("%s = (%s)<sup>2</sup>" % (Y, expr([(1, X), (-3, "")]))), X), "1", ["0", "2", "3"],
         "It equals 0 only when %s = 3. The turning point sits on the axis: <b>1</b>." % X),
        ("The curve %s passes through which point?" % B("%s = %s" % (Y, quad(1, -2, -3))), "(3, 0)", ["(0, 3)", "(−3, 0)", "(1, 0)"],
         "At %s = 3: 9 − 6 − 3 = 0. So <b>(3, 0)</b>." % X),
        ("Leo works out %s = −3 for %s = %s<sup>2</sup>. What should %s be?" % (Y, X, X2, Y) if False else "Leo says that when %s = −3, %s<sup>2</sup> = −9. What is the correct value?" % (X, X), "9", ["−9", "−6", "6"],
         "(−3)<sup>2</sup> = (−3) × (−3) = <b>9</b>. A negative times a negative is positive."),
        ("A quadratic graph has a turning point at (2, −1). It crosses the %s-axis at %s = 1. Where else does it cross?" % (X, X), "%s = 3" % X, ["%s = −1" % X, "%s = 2" % X, "%s = 4" % X],
         "The curve is symmetrical about %s = 2. 1 is 1 to the left, so the other root is 1 to the right: <b>%s = 3</b>." % (X, X)),
        ("The graph of %s is reflected in the %s-axis. What is the new equation?" % (B("%s = %s" % (Y, X2)), X), "%s = −%s" % (Y, X2), ["%s = %s − 1" % (Y, X2), "%s = (−%s)<sup>2</sup>" % (Y, X), "%s = −%s" % (Y, X)],
         "Every %s-value changes sign: <b>%s = −%s</b>, a ∩-shaped curve." % (Y, Y, X2)),
        ("What is the minimum value of %s?" % B("%s = %s" % (Y, quad(1, 0, -7))), "−7", ["7", "0", "−49"],
         "%s is smallest (0) when %s = 0, so the minimum %s is <b>−7</b>." % (X2, X, Y)),
        ("What is the maximum value of %s?" % B("%s = %s" % (Y, quad(-1, 0, 5))), "5", ["−5", "0", "25"],
         "−%s is largest (0) when %s = 0, so the maximum %s is <b>5</b>." % (X2, X, Y)),
        ("A garden is %s m long and (10 − %s) m wide. For which length is its area greatest?" % (X, X), "5 m", ["10 m", "2.5 m", "25 m"],
         "Area = %s(10 − %s). The roots are 0 and 10, so the greatest area is halfway, at <b>5 m</b>." % (X, X)),
        ("A garden is %s m long and (10 − %s) m wide. What is the greatest possible area?" % (X, X), "25 m²", ["50 m²", "100 m²", "20 m²"],
         "At %s = 5: 5 × 5 = <b>25 m²</b>." % X),
        ("Which value is missing? For %s, when %s = −2, %s = ☐" % (B("%s = %s" % (Y, quad(1, 3, 0))), X, Y), "−2", ["10", "2", "−10"],
         "(−2)<sup>2</sup> + 3(−2) = 4 − 6 = <b>−2</b>."),
        ("For %s, which two %s-values give %s = 5?" % (B("%s = %s" % (Y, quad(1, 0, -4))), X, Y), "%s = 3 or %s = −3" % (X, X), ["%s = 3 only" % X, "%s = 9" % X, "%s = 1 or %s = −1" % (X, X)],
         "%s − 4 = 5, so %s = 9 and %s = ±3. <b>%s = 3 or %s = −3</b>." % (X2, X2, X, X, X)),
        ("Amelia plots %s and joins the points with straight lines. What should she draw instead?" % B("%s = %s" % (Y, X2)), "A smooth curve", ["A ruler-drawn V shape", "A single straight line", "A bar chart"],
         "Quadratic graphs are smooth curves. Join the points with <b>a smooth curve</b>, not straight lines."),
        ("Which point is the turning point of %s?" % B("%s = (%s)<sup>2</sup> + 2" % (Y, expr([(1, X), (-1, "")]))), "(1, 2)", ["(−1, 2)", "(2, 1)", "(1, −2)"],
         "(%s − 1)<sup>2</sup> is smallest (0) when %s = 1, then %s = 2: <b>(1, 2)</b>." % (X, X, Y)),
        ("A curve has roots %s = −1 and %s = 5. What is the %s-coordinate of its turning point?" % (X, X, X), "2", ["3", "4", "−3"],
         "Halfway between −1 and 5: (−1 + 5) ÷ 2 = <b>2</b>."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>A <b>quadratic graph</b> such as <i>y</i> = <i>x</i>² − 2<i>x</i> − 3 is a smooth curve called a <b>parabola</b>. "
        "If the <i>x</i>² term is positive it is U-shaped; if negative it is ∩-shaped.</p>"
        "<p>Key features: the <b>roots</b> (where it crosses the <i>x</i>-axis), the <b><i>y</i>-intercept</b> (the constant term), "
        "the <b>turning point</b> (lowest or highest point) and the <b>line of symmetry</b> (halfway between the roots).</p>",
        [("Find <i>y</i> when <i>x</i> = −3 for <i>y</i> = <i>x</i>² + 2<i>x</i>.", ["(−3)² + 2(−3) = 9 − 6."], "<i>y</i> = 3"),
         ("<i>y</i> = (<i>x</i> + 1)(<i>x</i> − 3). Find the roots and the line of symmetry.", ["Roots: <i>x</i> = −1 and <i>x</i> = 3.", "Halfway: (−1 + 3) ÷ 2 = 1."], "<i>x</i> = 1"),
         ("Use a graph to solve <i>x</i>² − 4 = 5.", ["Draw <i>y</i> = 5 and read where it meets the curve."], "<i>x</i> = −3 or <i>x</i> = 3")],
        ["Writing (−3)² = −9. A negative squared is positive: 9.",
         "Reading roots from (<i>x</i> + 1)(<i>x</i> − 3) as −3 and 1. Set each bracket to zero: −1 and 3.",
         "Swapping the coordinates of the turning point.",
         "Joining points with straight lines. Draw a smooth curve."])


def main():
    sets = [S("Tables of values", collect(one_table, 20, R)),
            S("Reading a quadratic graph", collect(one_read, 20, R)),
            S("Roots, turning points and shape", collect(one_feature, 20, R)),
            S("Solving equations with a graph", collect(one_solve, 20, R)),
            S("Quadratic graph problems", problems())]
    make(9, "quadratic-graphs", 6, "A",
         "Quadratic Graphs",
         "Year 9 Quadratic Graphs Worksheets: Tables of Values, Roots, Turning Points and Solving with Graphs",
         "Quadratic Graphs",
         "Recognise, sketch and produce graphs of linear and quadratic functions of one variable with appropriate scaling, "
         "using equations in x and y and the Cartesian plane; find approximate solutions to contextual problems from given graphs.",
         "Free Year 9 quadratic graphs worksheets: complete tables of values, read roots, y-intercepts, turning points and "
         "lines of symmetry, and solve equations using graphs. 100 questions with answers.",
         "A quadratic graph is a U- or ∩-shaped curve.",
         "Roots: where it crosses the x-axis. The line of symmetry is halfway between them.",
         body(),
         [("What does a quadratic graph look like?", "A smooth curve called a parabola. It is U-shaped if the x² term is positive and ∩-shaped if it is negative."),
          ("What are the roots of a quadratic?", "The x-values where the curve crosses the x-axis, so where y = 0."),
          ("How do I find the line of symmetry?", "It is the vertical line halfway between the roots. For roots −1 and 3 it is x = 1."),
          ("How do I solve x² + bx + c = k with a graph?", "Draw the horizontal line y = k and read the x-values where it meets the curve.")],
         sets, R)


if __name__ == "__main__":
    main()
