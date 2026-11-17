# -*- coding: utf-8 -*-
"""
US Algebra 1: Function Notation (Common Core F-IF.A.2)
  python3 tools/gen_us_math_a1_function_notation.py
Evaluating linear and quadratic functions (including negative inputs), solving f(x) = k, using expressions
as inputs such as f(a + 1) and f(2x), adding and multiplying function values, and reading function notation
in tables, graphs and real situations.
Wrong answers come from real mistakes: reading f(x) as f times x, squaring a negative input wrongly
((−3)² = 9, not −9), confusing f(3) = 10 (input 3) with f(x) = 3 (output 3), and writing f(a + 1) as f(a) + 1.
"""
import random
from fractions import Fraction as F
from us_hs import num, B, S, make, lesson, collect, T, QN, expr, fr, MINUS, fig
from g8_common import grid_svg, xy_table
from ws_common import BLUE, RED

R = random.Random(90501)
X = "<i>x</i>"
X2 = "<i>x</i><sup>2</sup>"


def quad(a, b, c, v=X):
    v2 = v + "<sup>2</sup>" if v == X else "(%s)<sup>2</sup>" % v
    return expr([(a, v2), (b, v), (c, "")])


def p(v):
    return "(%s)" % num(v) if v < 0 else num(v)


# ------------------------------------------------------------ set 1: evaluate
def one_eval(r):
    if r.random() < 0.4:
        m, b = r.choice([2, 3, 4, 5, -2, -3, -4]), r.randint(-9, 9)
        x = r.randint(-6, 6)
        name = r.choice(["f", "g", "h"])
        q = "If %s, find %s." % (B("<i>%s</i>(<i>x</i>) = %s" % (name, expr([(m, X), (b, "")]))), B("<i>%s</i>(%s)" % (name, num(x))))
        v = m * x + b
        e = "Replace <i>x</i> with %s: %s × %s %s %s = <b>%s</b>." % (num(x), num(m), p(x), "+" if b >= 0 else MINUS, num(abs(b)), num(v))
        return QN(q, v, [m * (-x) + b, m + x + b, m * x - b if b else v + m], e)
    a, b, c = r.choice([1, 1, 2, 3, -1, -2]), r.randint(-6, 6), r.randint(-9, 9)
    x = r.choice([-4, -3, -2, -1, 2, 3, 4, 5])
    if c == 0 or b == 0:
        return None
    name = r.choice(["f", "g", "h", "p"])
    q = "If %s, find %s." % (B("<i>%s</i>(<i>x</i>) = %s" % (name, quad(a, b, c))), B("<i>%s</i>(%s)" % (name, num(x))))
    v = a * x * x + b * x + c
    wrong_sq = a * (-(x * x)) + b * x + c if x < 0 else a * 2 * x + b * x + c        # −3² read as −9, or x² as 2x
    e = "Replace every <i>x</i> with %s: %s%s<sup>2</sup> %s %s(%s) %s %s = %s %s %s %s %s = <b>%s</b>." % (
        p(x), num(a) if a not in (1, -1) else ("" if a == 1 else MINUS), "(%s)" % num(x) if (x < 0 or a not in (1,)) else num(x), "+" if b >= 0 else MINUS, num(abs(b)), num(x), "+" if c >= 0 else MINUS, num(abs(c)),
        num(a * x * x), "+" if b * x >= 0 else MINUS, num(abs(b * x)), "+" if c >= 0 else MINUS, num(abs(c)), num(v))
    return QN(q, v, [wrong_sq, a * x * x - b * x + c, (a * x) ** 2 + b * x + c if a != 1 else v + 2 * x], e)


# ------------------------------------------------------------ set 2: solve f(x) = k
def one_solve(r):
    kind = r.choice(["lin", "lin", "quad"])
    if kind == "lin":
        m, b = r.choice([2, 3, 4, 5, -2, -3, 6]), r.randint(-12, 12)
        x = r.randint(-7, 9)
        k = m * x + b
        q = "If %s, find <i>x</i> when %s." % (B("<i>f</i>(<i>x</i>) = %s" % expr([(m, X), (b, "")])), B("<i>f</i>(<i>x</i>) = %s" % num(k)))
        e = "Set %s = %s. Then %s<i>x</i> = %s, so <b><i>x</i> = %s</b>." % (expr([(m, X), (b, "")]), num(k), num(m), num(k - b), num(x))
        return QN(q, x, [m * k + b, F(k + b, m), F(k, m) if F(k, m) != x else x + 3], e)
    s = r.randint(1, 7)
    c = r.randint(-9, 9)
    k = s * s + c
    q = "If %s, find all values of <i>x</i> with %s." % (B("<i>f</i>(<i>x</i>) = %s" % quad(1, 0, c)), B("<i>f</i>(<i>x</i>) = %s" % num(k)))
    right = "<i>x</i> = %s or <i>x</i> = %s" % (num(-s), num(s))
    e = "%s = %s, so <i>x</i><sup>2</sup> = %s and <b><i>x</i> = ±%s</b>." % (quad(1, 0, c), num(k), num(s * s), num(s))
    return T(q, right, ["<i>x</i> = %s" % num(s), "<i>x</i> = %s" % num(k * k + c), "<i>x</i> = %s or <i>x</i> = %s" % (num(-(k - c)), num(k - c)) if k - c != s else "<i>x</i> = 0"], e)


def one_table(r):
    xs = [-2, -1, 0, 1, 2, 3]
    m, b = r.choice([2, 3, -2, 4, -3]), r.randint(-5, 5)
    ys = [m * x + b for x in xs]
    tb = xy_table([num(x) for x in xs], [num(y) for y in ys], "x", "f(x)")
    if r.random() < 0.5:
        i = r.randrange(6)
        q = "Use the table to find %s.%s" % (B("<i>f</i>(%s)" % num(xs[i])), tb)
        wr = [num(v) for v in dict.fromkeys([ys[(i + 1) % 6], xs[i], ys[(i - 1) % 6]]) if v != ys[i]]
        return T(q, num(ys[i]), wr[:3] if len(wr) >= 3 else wr + [num(ys[i] + 7)], "Find the input %s in the top row; the output below it is <b>%s</b>." % (num(xs[i]), num(ys[i])))
    i = r.randrange(6)
    if ys[i] in xs and xs.index(ys[i]) != i:
        return None
    q = "Use the table to find <i>x</i> when %s.%s" % (B("<i>f</i>(<i>x</i>) = %s" % num(ys[i])), tb)
    wr = [num(ys[i] * m + b), num(xs[(i + 1) % 6]), num(xs[(i - 1) % 6])]
    wr = [w for w in dict.fromkeys(wr) if w != num(xs[i])]
    if len(wr) < 3:
        return None
    return T(q, num(xs[i]), wr, "Find the output %s in the bottom row; the input above it is <b>%s</b>." % (num(ys[i]), num(xs[i])))


# ------------------------------------------------------------ set 3: expressions as inputs
def one_expr(r):
    m, b = r.choice([2, 3, 4, 5, -2, -3]), r.randint(-8, 8)
    if b == 0:
        return None
    f = expr([(m, X), (b, "")])
    kind = r.choice(["a1", "2x", "neg", "q"])
    if kind == "a1":
        k = r.choice([1, 2, 3, -1, -2])
        inp = expr([(1, "<i>a</i>"), (k, "")])
        right = expr([(m, "<i>a</i>"), (m * k + b, "")])
        wr = [expr([(m, "<i>a</i>"), (b + k, "")]), expr([(m, "<i>a</i>"), (k + b, "")]) if False else expr([(m, "<i>a</i>"), (k * b, "")]) if k * b != m * k + b else expr([(m, "<i>a</i>"), (b, "")]), expr([(m, "<i>a</i>"), (b, "")])]
        e = "Replace <i>x</i> with (%s): %s(%s) %s %s = <b>%s</b>." % (inp, num(m), inp, "+" if b > 0 else MINUS, num(abs(b)), right)
        q = "If %s, find %s." % (B("<i>f</i>(<i>x</i>) = %s" % f), B("<i>f</i>(%s)" % inp))
    elif kind == "2x":
        right = expr([(2 * m, X), (b, "")])
        wr = [expr([(2 * m, X), (2 * b, "")]), expr([(m, X), (b + 2, "")]), expr([(m + 2, X), (b, "")])]
        e = "Replace <i>x</i> with 2<i>x</i>: %s(2<i>x</i>) %s %s = <b>%s</b>. Note this is not 2<i>f</i>(<i>x</i>) = %s." % (num(m), "+" if b > 0 else MINUS, num(abs(b)), right, expr([(2 * m, X), (2 * b, "")]))
        q = "If %s, find %s." % (B("<i>f</i>(<i>x</i>) = %s" % f), B("<i>f</i>(2<i>x</i>)"))
    elif kind == "neg":
        right = expr([(-m, X), (b, "")])
        wr = [expr([(-m, X), (-b, "")]), expr([(m, X), (-b, "")]), f]
        e = "Replace <i>x</i> with −<i>x</i>: %s(−<i>x</i>) %s %s = <b>%s</b>." % (num(m), "+" if b > 0 else MINUS, num(abs(b)), right)
        q = "If %s, find %s." % (B("<i>f</i>(<i>x</i>) = %s" % f), B("<i>f</i>(−<i>x</i>)"))
    else:
        c = r.choice([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6])
        k = r.choice([1, 2, 3])
        q = "If %s, find %s." % (B("<i>g</i>(<i>x</i>) = %s" % quad(1, 0, c)), B("<i>g</i>(%s)" % expr([(1, X), (k, "")])))
        right = expr([(1, X2), (2 * k, X), (k * k + c, "")])
        wr = [expr([(1, X2), (k * k + c, "")]), expr([(1, X2), (k, X), (k * k + c, "")]), expr([(1, X2), (c + k, "")])]
        e = "Replace <i>x</i> with (%s): (%s)<sup>2</sup> %s %s = %s %s %s = <b>%s</b>." % (
            expr([(1, X), (k, "")]), expr([(1, X), (k, "")]), "+" if c >= 0 else MINUS, num(abs(c)),
            expr([(1, X2), (2 * k, X), (k * k, "")]), "+" if c >= 0 else MINUS, num(abs(c)), right)
    wr = [w for w in dict.fromkeys(wr) if w != right]
    if len(wr) < 3:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 4: combining function values
def one_comb(r):
    m1, b1 = r.choice([2, 3, -2, 4]), r.randint(-6, 6)
    a2, c2 = r.choice([1, 2, -1]), r.randint(-5, 5)
    f = lambda x: m1 * x + b1
    g = lambda x: a2 * x * x + c2
    fx, gx = expr([(m1, X), (b1, "")]), quad(a2, 0, c2)
    head = "Let %s and %s." % (B("<i>f</i>(<i>x</i>) = %s" % fx), B("<i>g</i>(<i>x</i>) = %s" % gx))
    kind = r.choice(["sum", "diff", "prod", "scal", "fg"])
    u, w = r.randint(-3, 4), r.randint(-3, 4)
    if kind == "sum":
        v = f(u) + g(w)
        q = head + " Find %s." % B("<i>f</i>(%s) + <i>g</i>(%s)" % (num(u), num(w)))
        e = "<i>f</i>(%s) = %s and <i>g</i>(%s) = %s, so the sum is <b>%s</b>." % (num(u), num(f(u)), num(w), num(g(w)), num(v))
        return QN(q, v, [f(w) + g(u), f(u) - g(w), f(u + w) if f(u + w) != v else v + 2], e)
    if kind == "diff":
        v = f(u) - g(w)
        q = head + " Find %s." % B("<i>f</i>(%s) − <i>g</i>(%s)" % (num(u), num(w)))
        e = "<i>f</i>(%s) = %s and <i>g</i>(%s) = %s, so %s − %s = <b>%s</b>." % (num(u), num(f(u)), num(w), num(g(w)), num(f(u)), p(g(w)), num(v))
        return QN(q, v, [g(w) - f(u), f(u) + g(w), f(w) - g(u)], e)
    if kind == "prod":
        v = f(u) * g(u)
        q = head + " Find %s." % B("<i>f</i>(%s) · <i>g</i>(%s)" % (num(u), num(u)))
        e = "<i>f</i>(%s) = %s and <i>g</i>(%s) = %s, so the product is <b>%s</b>." % (num(u), num(f(u)), num(u), num(g(u)), num(v))
        return QN(q, v, [f(u) + g(u), f(g(u)) if f(g(u)) != v else v + 3, -v if v else 5], e)
    if kind == "scal":
        k = r.choice([2, 3, -2])
        v = k * f(u) + g(w)
        q = head + " Find %s." % B("%s<i>f</i>(%s) + <i>g</i>(%s)" % (num(k), num(u), num(w)))
        e = "%s × <i>f</i>(%s) = %s × %s = %s. Add <i>g</i>(%s) = %s: <b>%s</b>." % (num(k), num(u), num(k), p(f(u)), num(k * f(u)), num(w), num(g(w)), num(v))
        return QN(q, v, [f(k * u) + g(w), f(u) + g(w), k * (f(u) + g(w))], e)
    v = f(g(u))
    q = head + " Find %s. (Work out <i>g</i>(%s) first.)" % (B("<i>f</i>(<i>g</i>(%s))" % num(u)), num(u))
    e = "<i>g</i>(%s) = %s. Then <i>f</i>(%s) = <b>%s</b>." % (num(u), num(g(u)), num(g(u)), num(v))
    return QN(q, v, [g(f(u)), f(u) * g(u), f(u) + g(u)], e)


# ------------------------------------------------------------ set 5: meaning
def problems():
    data = [
        ("<i>C</i>(<i>n</i>) is the cost in dollars of <i>n</i> concert tickets. What does <i>C</i>(4) = 90 mean?", "4 tickets cost $90", ["90 tickets cost $4", "Each ticket costs $90", "4 tickets cost $360"], "The input is the number of tickets (4) and the output is the cost ($90): <b>4 tickets cost $90</b>."),
        ("<i>h</i>(<i>t</i>) is the height of a ball in feet after <i>t</i> seconds. What does <i>h</i>(2) = 36 mean?", "After 2 seconds the ball is 36 ft high", ["After 36 seconds the ball is 2 ft high", "The ball rises 36 ft per second", "The ball is 2 ft high for 36 seconds"],
         "Input = time (2 s), output = height (36 ft): <b>after 2 seconds the ball is 36 ft high</b>."),
        ("<i>P</i>(<i>d</i>) = 12<i>d</i> + 30 is the cost of renting a bike for <i>d</i> days. Find <i>P</i>(5).", "$90", ["$47", "$60", "$102"], "12 × 5 + 30 = <b>90</b>."),
        ("<i>P</i>(<i>d</i>) = 12<i>d</i> + 30. For how many days is the cost $114?", "7", ["1,398", "12", "9.5"], "12<i>d</i> + 30 = 114, so 12<i>d</i> = 84 and <i>d</i> = <b>7</b>."),
        ("Which statement means “the output is 5 when the input is 2”?", "<i>f</i>(2) = 5", ["<i>f</i>(5) = 2", "<i>f</i> = 2 × 5", "2<i>f</i> = 5"], "Input goes inside the parentheses: <b><i>f</i>(2) = 5</b>."),
        ("Does <i>f</i>(<i>x</i>) mean <i>f</i> times <i>x</i>?", "No, it means the value of f at x", ["Yes, always", "Only when x is a number", "Only for linear functions"], "<i>f</i>(<i>x</i>) is read “<i>f</i> of <i>x</i>”: <b>the output of <i>f</i> for the input <i>x</i></b>."),
        ("The graph of <i>y</i> = <i>f</i>(<i>x</i>) passes through (3, −2). Which statement is true?", "<i>f</i>(3) = −2", ["<i>f</i>(−2) = 3", "<i>f</i>(3) = 3", "<i>f</i>(0) = −2"], "A point (<i>x</i>, <i>y</i>) on the graph means <i>f</i>(<i>x</i>) = <i>y</i>: <b><i>f</i>(3) = −2</b>."),
        ("<i>T</i>(<i>m</i>) is the temperature of an oven <i>m</i> minutes after it is turned on. Which is the best meaning of <i>T</i>(10) &gt; <i>T</i>(5)?", "The oven is hotter at 10 minutes than at 5 minutes",
         ["The oven takes 10 minutes to heat up", "The temperature doubles", "The oven is cooler at 10 minutes"], "Compare outputs at the two inputs: <b>hotter at 10 minutes than at 5</b>."),
        ("If <i>f</i>(<i>x</i>) = 3<i>x</i> − 1, which is larger: <i>f</i>(4) or <i>f</i>(−4)?", "<i>f</i>(4)", ["<i>f</i>(−4)", "They are equal", "You cannot tell"], "<i>f</i>(4) = 11 and <i>f</i>(−4) = −13: <b><i>f</i>(4)</b>."),
        ("If <i>g</i>(<i>x</i>) = <i>x</i><sup>2</sup>, which is true?", "<i>g</i>(3) = <i>g</i>(−3)", ["<i>g</i>(3) &gt; <i>g</i>(−3)", "<i>g</i>(−3) = −9", "<i>g</i>(3) = 6"], "3² = 9 and (−3)² = 9: <b><i>g</i>(3) = <i>g</i>(−3)</b>."),
        ("<i>A</i>(<i>s</i>) = <i>s</i><sup>2</sup> is the area of a square with side <i>s</i> cm. Find <i>A</i>(7).", "49 cm²", ["14 cm²", "28 cm²", "7 cm²"], "7<sup>2</sup> = <b>49 cm²</b>."),
        ("<i>A</i>(<i>s</i>) = <i>s</i><sup>2</sup>. Which side length gives an area of 64 cm²?", "8 cm", ["32 cm", "16 cm", "4,096 cm"], "<i>s</i><sup>2</sup> = 64 and <i>s</i> must be positive: <b>8 cm</b>."),
        ("A phone plan costs <i>C</i>(<i>g</i>) = 20 + 8<i>g</i> dollars for <i>g</i> GB of data. What does the 8 mean?", "Each GB costs $8", ["The plan costs $8", "You get 8 GB", "The fixed fee is $8"], "The 8 multiplies the GB, so it is the cost <b>per GB</b>."),
        ("If <i>f</i>(<i>x</i>) = 2<i>x</i> + 1, find <i>f</i>(<i>f</i>(1)).", "7", ["3", "5", "9"], "<i>f</i>(1) = 3, then <i>f</i>(3) = <b>7</b>."),
        ("If <i>f</i>(<i>x</i>) = 5 − <i>x</i>, find <i>f</i>(5) + <i>f</i>(−5).", "10", ["0", "−10", "20"], "<i>f</i>(5) = 0 and <i>f</i>(−5) = 10: <b>10</b>."),
        ("<i>D</i>(<i>t</i>) = 55<i>t</i> is the distance in miles a car travels in <i>t</i> hours. What is <i>D</i>(2.5)?", "137.5 miles", ["57.5 miles", "110 miles", "22 miles"], "55 × 2.5 = <b>137.5</b>."),
        ("If <i>f</i>(<i>x</i>) = 4<i>x</i>, which is equal to <i>f</i>(<i>a</i> + <i>b</i>)?", "<i>f</i>(<i>a</i>) + <i>f</i>(<i>b</i>)", ["<i>f</i>(<i>a</i>) · <i>f</i>(<i>b</i>)", "<i>f</i>(<i>a</i>) + <i>b</i>", "4<i>a</i> + <i>b</i>"], "4(<i>a</i> + <i>b</i>) = 4<i>a</i> + 4<i>b</i> = <b><i>f</i>(<i>a</i>) + <i>f</i>(<i>b</i>)</b>."),
        ("If <i>f</i>(<i>x</i>) = <i>x</i> + 3, Ava says <i>f</i>(2<i>x</i>) = 2<i>x</i> + 6. What is the correct answer?", "2<i>x</i> + 3", ["2<i>x</i> + 6", "<i>x</i> + 6", "2<i>x</i> + 5"], "Replace <i>x</i> with 2<i>x</i>: <b>2<i>x</i> + 3</b>. Ava found 2<i>f</i>(<i>x</i>)."),
        ("A population is <i>P</i>(<i>t</i>) = 500 · 2<sup><i>t</i></sup> after <i>t</i> years. Find <i>P</i>(3).", "4,000", ["3,000", "1,000", "1,500"], "2<sup>3</sup> = 8 and 500 × 8 = <b>4,000</b>."),
        ("The table shows <i>f</i>(0) = 4, <i>f</i>(1) = 7, <i>f</i>(2) = 10. Which rule fits?", "<i>f</i>(<i>x</i>) = 3<i>x</i> + 4", ["<i>f</i>(<i>x</i>) = 4<i>x</i> + 3", "<i>f</i>(<i>x</i>) = <i>x</i> + 4", "<i>f</i>(<i>x</i>) = 3<i>x</i>"], "The output starts at 4 and goes up 3 each time: <b>3<i>x</i> + 4</b>."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p><i>f</i>(<i>x</i>) is read “<i>f</i> of <i>x</i>”. It means <b>the output of the function <i>f</i> when the input is <i>x</i></b>. "
        "It does not mean <i>f</i> times <i>x</i>.</p>"
        "<p>To find <i>f</i>(3), replace <b>every</b> <i>x</i> with 3. Put negative inputs in parentheses: (−3)<sup>2</sup> = 9. "
        "The input can also be an expression: <i>f</i>(<i>a</i> + 1) means replace <i>x</i> with (<i>a</i> + 1).</p>"
        "<p><i>f</i>(3) = 10 tells you the point (3, 10) is on the graph of <i>y</i> = <i>f</i>(<i>x</i>).</p>",
        [("If <i>f</i>(<i>x</i>) = 2<i>x</i><sup>2</sup> − 3<i>x</i>, find <i>f</i>(−2).", ["2(−2)<sup>2</sup> − 3(−2) = 2(4) + 6."], "14"),
         ("If <i>f</i>(<i>x</i>) = 4<i>x</i> − 5, find <i>x</i> when <i>f</i>(<i>x</i>) = 11.", ["4<i>x</i> − 5 = 11.", "4<i>x</i> = 16."], "<i>x</i> = 4"),
         ("If <i>f</i>(<i>x</i>) = 3<i>x</i> + 2, find <i>f</i>(<i>a</i> − 1).", ["3(<i>a</i> − 1) + 2 = 3<i>a</i> − 3 + 2."], "3<i>a</i> − 1")],
        ["Reading <i>f</i>(<i>x</i>) as “<i>f</i> times <i>x</i>”.",
         "Squaring a negative input wrongly: for <i>x</i> = −3, <i>x</i><sup>2</sup> = 9, not −9.",
         "Mixing up input and output: <i>f</i>(<i>x</i>) = 3 asks for the input that gives 3, not for <i>f</i>(3).",
         "Writing <i>f</i>(2<i>x</i>) as 2<i>f</i>(<i>x</i>), or <i>f</i>(<i>a</i> + 1) as <i>f</i>(<i>a</i>) + 1."])


def main():
    sets = [S("Evaluate a function", collect(one_eval, 20, R)),
            S("Find the input: solve f(x) = k", collect(one_solve, 12, R) + collect(one_table, 8, R)),
            S("Expressions as inputs", collect(one_expr, 20, R)),
            S("Combining function values", collect(one_comb, 20, R)),
            S("Function notation in context", problems())]
    make("function-notation", 5, "F-IF.A.2",
         "Function Notation: Evaluate f(x), Solve f(x) = k and Interpret",
         "Algebra 1 Function Notation Worksheets: Evaluating Functions, f(x) = k and Word Problems (Free, Answer Key)",
         "Function notation",
         "Use function notation, evaluate functions for inputs in their domains, and interpret statements that use function notation in terms of a context.",
         "Free Algebra 1 function notation worksheets (F-IF.A.2): evaluate linear and quadratic functions, solve f(x) = k, use "
         "expressions such as f(a + 1) as inputs, combine function values and interpret f(x) in context. 100 questions with an answer key.",
         "f(x) means the output of f when the input is x. Replace every x with the input.",
         "f(3) = 10 means input 3 gives output 10, so (3, 10) is on the graph.",
         body(),
         [("What does f(x) mean?", "It is read “f of x” and means the output of the function f for the input x. It does not mean f times x."),
          ("How do you evaluate a function?", "Replace every x in the rule with the input value, using parentheses for negative numbers, then simplify."),
          ("What is the difference between f(3) and f(x) = 3?", "f(3) asks for the output when the input is 3. f(x) = 3 asks which input gives an output of 3."),
          ("How do you find f(a + 1)?", "Replace every x with (a + 1) and simplify. For f(x) = 2x + 5, f(a + 1) = 2(a + 1) + 5 = 2a + 7.")],
         sets, R, domain="Functions")


if __name__ == "__main__":
    main()
