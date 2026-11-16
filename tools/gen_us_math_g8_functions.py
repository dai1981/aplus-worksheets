# -*- coding: utf-8 -*-
"""
US Grade 8 Math: Functions (8.F.A.1, 8.F.A.2, 8.F.A.3)
  python3 tools/gen_us_math_g8_functions.py
A function gives each input exactly one output: ordered pairs, tables and the vertical line test;
evaluating functions; linear or nonlinear; comparing two functions given in different ways.
Wrong answers come from real mistakes: thinking repeated outputs break a function, reading x for y,
and calling every curve "not a function".
"""
import math, random
from fractions import Fraction as F
from ws_common import num, mcq, balance, B, table, example, write_unit, fig, X, MINUS, RED, BLUE
from g8_common import lin, grid_svg, xy_table, sl

R = random.Random(80401)
UPDATED = "2026-11-16"
Y = "<i>y</i>"
YES1 = "Yes: each input has exactly one output"
NO1 = "No: one input has two different outputs"
NO2 = "No: two inputs have the same output"
YES2 = "Yes: every output is different"


def pairs_txt(ps):
    return "{" + ", ".join("(%s, %s)" % (num(a), num(b)) for a, b in ps) + "}"


def is_func(ps):
    d = {}
    for a, b in ps:
        if a in d and d[a] != b:
            return False
        d[a] = b
    return True


def func_q(ps, how):
    ok = is_func(ps)
    xs = [a for a, _ in ps]
    ys = [b for _, b in ps]
    if how == "pairs":
        q = "Is this relation a function? %s" % B(pairs_txt(ps))
    else:
        q = xy_table([num(v) for v in xs], [num(v) for v in ys], "input", "output") + "Is this table a function?"
    if ok:
        rep = [b for b in ys if ys.count(b) > 1]
        ans = YES1
        e = "No input repeats with a different output. "
        if rep:
            e += "Outputs can repeat (%s appears more than once); that is fine. " % num(rep[0])
        e += "<b>Yes</b>, it is a function."
    else:
        bad = [a for a in xs if len({b for x, b in ps if x == a}) > 1][0]
        outs = sorted({b for x, b in ps if x == bad})
        ans = NO1
        e = "The input %s has two outputs (%s and %s). <b>No</b>, it is not a function." % (num(bad), num(outs[0]), num(outs[1]))
    ch = [YES1, NO1, NO2, YES2]
    return mcq(q, (ans, ans), [(c, c) for c in ch if c != ans], e)


# ============================================================ set 1
def set_relations():
    its = []
    for ps, how in [([(1, 4), (2, 5), (3, 6), (4, 7)], "pairs"), ([(1, 3), (2, 3), (3, 3), (4, 3)], "pairs"),
                    ([(2, 1), (2, 5), (3, 6), (4, 8)], "pairs"), ([(-1, 0), (0, 1), (1, 0), (2, 3)], "pairs"),
                    ([(5, 2), (6, 4), (5, 2), (7, 9)], "pairs"), ([(0, 0), (1, 1), (1, -1), (4, 2)], "pairs"),
                    ([(-2, 4), (-1, 1), (0, 0), (1, 1), (2, 4)], "table"), ([(3, 1), (3, 2), (3, 3), (3, 4)], "table"),
                    ([(1, 10), (2, 20), (3, 30), (4, 40)], "table"), ([(0, 5), (1, 5), (2, 5), (3, 5)], "table"),
                    ([(4, -2), (4, 2), (9, 3), (9, -3)], "table"), ([(-3, 7), (-1, 7), (1, 8), (3, 8)], "table"),
                    ([(2, 9), (4, 7), (6, 5), (2, 3)], "pairs"), ([(10, 1), (20, 2), (30, 1), (40, 2)], "pairs"),
                    ([(7, 7), (8, 8), (9, 9), (8, 10)], "table"), ([(-5, 0), (-4, 1), (-3, 2), (-2, 3)], "pairs")]:
        its.append(func_q(ps, how))
    for q, ans, wr, e in [
        ("Each student has one birthday. Is “student → birthday” a function?", "Yes", ["No", "Only if birthdays are different", "We cannot tell"],
         "Each student (input) has exactly one birthday (output). Two students may share a birthday; that is fine. <b>Yes</b>."),
        ("Is “a person’s age → that person” a function?", "No", ["Yes", "Only for adults", "Always"],
         "Many people have the same age, so one input (an age) has many outputs (people). <b>No</b>."),
        ("Is “a number → its square” a function?", "Yes", ["No", "Only for positive numbers", "Only for whole numbers"],
         "Every number has exactly one square. 3 → 9 and −3 → 9 is fine. <b>Yes</b>."),
        ("A vending machine: button A gives chips, button B gives a drink, button C gives chips. Is it a function?", "Yes",
         ["No", "Only if every button gives something different", "We cannot tell"],
         "Each button (input) gives exactly one item (output). Two buttons giving chips is fine. <b>Yes</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[1], o[2], o[16], o[3], o[4], o[17], o[5], o[6], o[7], o[18], o[8], o[9], o[10], o[19], o[11],
             o[12], o[13], o[14], o[15]]
    return {"title": "Is it a function?", "items": order}


# ============================================================ set 2: graphs
def curve(fn, lo, hi, step=0.25):
    pts = []
    x = lo
    while x <= hi + 1e-9:
        y = fn(x)
        if y is not None and -6.2 <= y <= 6.2:
            pts.append((x, y))
        else:
            pts.append(None)
        x += step
    segs = []
    for a, b in zip(pts, pts[1:]):
        if a and b:
            segs.append((a[0], a[1], b[0], b[1], BLUE))
    return segs


def set_graphs():
    its = []
    shapes = [
        ("line", dict(lines=[(2, -1, BLUE)]), True, "Any vertical line crosses this line once."),
        ("vertical", dict(lines=[("v", 3, BLUE)]), False, "This is a vertical line: x = 3 has many outputs."),
        ("parabola", dict(segs=curve(lambda x: x * x - 3, -3, 3)), True, "A U-shape that opens up passes the test: each x has one y."),
        ("sideways", dict(segs=curve(lambda y: y * y / 2 - 3, -3.4, 3.4)), False, "This U opens sideways: one x has two y-values."),
        ("circle", dict(segs=[(4 * math.cos(t / 20 * 2 * math.pi), 4 * math.sin(t / 20 * 2 * math.pi),
                               4 * math.cos((t + 1) / 20 * 2 * math.pi), 4 * math.sin((t + 1) / 20 * 2 * math.pi), BLUE) for t in range(20)]),
         False, "A circle fails: a vertical line through the middle crosses it twice."),
        ("flat", dict(lines=[(0, 2, BLUE)]), True, "A horizontal line is a function: every x gives y = 2."),
        ("abs", dict(segs=curve(lambda x: abs(x) - 2, -6, 6)), True, "A V-shape passes the test: each x has one y."),
        ("cubic", dict(segs=curve(lambda x: x ** 3 / 4 - x, -3.5, 3.5)), True, "This wavy curve still passes: each vertical line crosses once."),
        ("negline", dict(lines=[(F(-1, 2), 3, BLUE)]), True, "A slanted line always passes the test."),
        ("ellipse", dict(segs=[(5 * math.cos(t / 24 * 2 * math.pi), 2.5 * math.sin(t / 24 * 2 * math.pi),
                                5 * math.cos((t + 1) / 24 * 2 * math.pi), 2.5 * math.sin((t + 1) / 24 * 2 * math.pi), BLUE) for t in range(24)]),
         False, "An oval fails: some vertical lines cross it twice."),
    ]
    for key, kw, ok, why in shapes:
        segs = kw.get("segs", [])
        if key == "sideways":
            segs = [(y1, x1, y2, x2, BLUE) for (x1, y1, x2, y2, c) in curve(lambda y: y * y / 2 - 3, -3.4, 3.4)]
        svg = grid_svg(-6, 6, lines=kw.get("lines", []), segs=segs, unit=18)
        ans = "Yes" if ok else "No"
        e = "Use the vertical line test. %s <b>%s</b>." % (why, ans)
        its.append(mcq(fig(svg) + "Is this graph a function?", (ans, ans),
                       [(c, c) for c in ["Yes", "No", "Only the right half", "We cannot tell"] if c != ans], e))
    for m, b, xq in [(2, -1, 3), (-1, 4, -2), (F(1, 2), 1, 4), (3, -5, 2), (-2, 0, -3)]:
        y = m * xq + b
        svg = grid_svg(-6, 6, lines=[(m, b, BLUE)], points=[(xq, y, "", RED)], unit=18)
        e = "Go to x = %s, then up or down to the line: y = <b>%s</b>." % (num(xq), num(y))
        its.append(mcq(fig(svg) + "Use the graph. What is the output when the input is %s?" % num(xq), (num(y), y),
                       [(num(xq), F(xq) if F(xq) != y else None), (num(y + 1), y + 1), (num(-y), -y), (num(y - 1), y - 1)], e))
    for q, ans, wr, e in [
        ("What is the vertical line test?", "If any vertical line crosses a graph more than once, it is not a function",
         ["If a horizontal line crosses twice, it is not a function", "Every graph with a curve is not a function", "A function must be a straight line"],
         "A vertical line is one input x. Crossing twice means two outputs. <b>If any vertical line crosses a graph more than once, it is not a function</b>."),
        ("Which graph is never a function?", "A vertical line", ["A horizontal line", "A slanted line", "A U-shape opening up"],
         "A vertical line has one x with every y. <b>A vertical line</b> is never a function."),
        ("Are all functions straight lines?", "No, curves can be functions too", ["Yes, always", "Yes, if they go through (0, 0)", "No, only circles"],
         "y = x² is a curve and a function. <b>No, curves can be functions too</b>."),
        ("A graph passes the vertical line test. What does that mean?", "It is a function", ["It is linear", "It goes through the origin",
         "It is not a function"], "Passing the test means each input has one output: <b>it is a function</b>."),
        ("The point (2, 5) is on the graph of a function. Can (2, 7) also be on it?", "No", ["Yes", "Only if the function is linear", "Yes, if 7 > 5"],
         "Input 2 already has output 5. A second output would break the rule. <b>No</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[15], o[0], o[1], o[10], o[2], o[3], o[16], o[11], o[4], o[5], o[17], o[12], o[6], o[7], o[18], o[13],
             o[8], o[9], o[19], o[14]]
    return {"title": "Graphs and the vertical line test", "items": order}


# ============================================================ set 3: evaluate
def set_eval():
    its = []
    for a, b, xv in [(3, -2, 4), (2, 5, -3), (-4, 1, 2), (F(1, 2), 6, 8), (5, 0, -2), (-1, 7, 7), (6, -10, 3), (F(-2, 3), 4, 9),
                     (10, -1, F(1, 2)), (-3, -3, -4)]:
        y = a * xv + b
        f = "<i>f</i>(%s) = %s" % (X, lin(a, b))
        q = "If %s, what is %s?" % (B(f), B("<i>f</i>(%s)" % num(xv)))
        e = "Replace %s with %s: %s × %s%s = <b>%s</b>." % (X, num(xv), sl(a), "(%s)" % num(xv) if xv < 0 else num(xv),
                                                          (" + " + num(b)) if b > 0 else ((" − " + num(-b)) if b < 0 else ""), num(y))
        its.append(mcq(q, (num(y), y), [(num(a + b), a + b), (num(a * xv - b), a * xv - b), (num(-y), -y), (num(y + a), y + a),
                                        (num(xv), F(xv))], e))
    for a, b, yv in [(2, 3, 11), (4, -1, 15), (-3, 6, 0), (5, 2, -8), (F(1, 2), -1, 3)]:
        xv = (yv - b) / F(a)
        f = "<i>f</i>(%s) = %s" % (X, lin(a, b))
        q = "If %s, for what input is the output %s?" % (B(f), B(num(yv)))
        e = "Solve %s = %s: %s = %s, so %s = <b>%s</b>." % (lin(a, b), num(yv), lin(a, 0), num(yv - b), X, num(xv))
        its.append(mcq(q, (num(xv), xv), [(num(a * yv + b), a * yv + b), (num((yv + b) / F(a)), (yv + b) / F(a)), (num(-xv), -xv),
                                          (num(xv + 1), xv + 1)], e))
    for xs, ys, xq in [([1, 2, 3, 4], [5, 8, 11, 14], 3), ([0, 2, 4, 6], [9, 5, 1, -3], 4), ([-2, -1, 0, 1], [4, 1, 0, 1], -1),
                       ([5, 10, 15, 20], [2, 4, 6, 8], 15), ([1, 3, 5, 7], [0, -4, -8, -12], 7)]:
        yq = ys[xs.index(xq)]
        tbl = xy_table([num(v) for v in xs], [num(v) for v in ys], X.replace("<i>", "").replace("</i>", ""), "f(x)")
        e = "Find %s in the top row. The value below it is <b>%s</b>." % (num(xq), num(yq))
        its.append(mcq(tbl + "Use the table. What is <i>f</i>(%s)?" % num(xq), (num(yq), F(yq)),
                       [(num(ys[xs.index(xq) - 1]), F(ys[xs.index(xq) - 1])), (num(xq), F(xq)),
                        (num(ys[(xs.index(xq) + 1) % 4]), F(ys[(xs.index(xq) + 1) % 4])), (num(yq + 1), F(yq + 1))], e))
    o = its
    order = [o[0], o[15], o[1], o[16], o[2], o[10], o[3], o[17], o[4], o[11], o[5], o[18], o[6], o[12], o[7], o[19], o[8],
             o[13], o[9], o[14]]
    return {"title": "Evaluate a function", "items": order}


# ============================================================ set 4: linear or nonlinear
def set_linear():
    its = []
    LIN, NON = "Linear", "Nonlinear"
    for txt, ok, why in [
        ("%s = 3%s + 1" % (Y, X), True, "It has the form y = mx + b."),
        ("%s = %s²" % (Y, X), False, "x is squared, so the graph is a curve."),
        ("%s = −2%s" % (Y, X), True, "It is y = mx + b with b = 0."),
        ("%s = 5" % Y, True, "It is a horizontal line: y = 0x + 5."),
        ("%s = <span class='fr'><span class='fn'>4</span><span class='fd'>%s</span></span>" % (Y, X), False, "x is in the bottom of a fraction, so it is a curve."),
        ("%s = %s³ − 1" % (Y, X), False, "x is cubed, so it is not a line."),
        ("%s = <span class='fr'><span class='fn'>%s</span><span class='fd'>2</span></span> + 7" % (Y, X), True, "x/2 is the same as ½x: y = ½x + 7."),
        ("%s = 2<sup>%s</sup>" % (Y, X), False, "x is an exponent, so y grows faster and faster."),
        ("%s = 4(%s − 3)" % (Y, X), True, "Distribute: y = 4x − 12, which is y = mx + b."),
        ("%s = %s%s" % (Y, X, X), False, "x · x = x², so it is a curve."),
    ]:
        ans = LIN if ok else NON
        its.append(mcq("Is %s linear or nonlinear?" % B(txt), (ans, ans),
                       [(c, c) for c in [LIN, NON, "Both", "Neither: it is not a function"] if c != ans],
                       why + " <b>%s</b>." % ans))
    for xs, ys in [([0, 1, 2, 3], [1, 3, 5, 7]), ([0, 1, 2, 3], [0, 1, 4, 9]), ([1, 2, 3, 4], [10, 7, 4, 1]), ([0, 1, 2, 3], [1, 2, 4, 8]),
                   ([0, 2, 4, 6], [3, 4, 5, 6]), ([1, 2, 3, 4], [1, 4, 9, 16]), ([-1, 0, 1, 2], [-5, -2, 1, 4]), ([0, 1, 2, 3], [5, 5, 6, 8])]:
        diffs = [b - a for a, b in zip(ys, ys[1:])]
        ok = len(set(diffs)) == 1
        ans = LIN if ok else NON
        tbl = xy_table([num(v) for v in xs], [num(v) for v in ys])
        e = ("x goes up by the same amount each time. y changes by %s each time. %s rate of change: <b>%s</b>."
             % (", ".join(num(d) for d in diffs), "The same" if ok else "Not the same", ans))
        its.append(mcq(tbl + "Is this function linear or nonlinear?", (ans, ans),
                       [(c, c) for c in [LIN, NON, "Both", "Neither: it is not a function"] if c != ans], e))
    for key, ok in [("line", True), ("parabola", False)]:
        segs = curve(lambda x: x * x / 2 - 4, -4, 4) if key == "parabola" else []
        lines = [(F(1, 2), -2, BLUE)] if key == "line" else []
        svg = grid_svg(-6, 6, lines=lines, segs=segs, unit=16)
        ans = LIN if ok else NON
        its.append(mcq(fig(svg) + "Is the function in the graph linear or nonlinear?", (ans, ans),
                       [(c, c) for c in [LIN, NON, "Both", "Neither: it is not a function"] if c != ans],
                       ("The graph is a straight line: <b>Linear</b>." if ok else "The graph is curved: <b>Nonlinear</b>.")))
    o = its
    order = [o[0], o[10], o[1], o[11], o[2], o[18], o[12], o[3], o[13], o[4], o[14], o[5], o[19], o[15], o[6], o[16],
             o[7], o[17], o[8], o[9]]
    return {"title": "Linear or nonlinear?", "items": order}


# ============================================================ set 5: compare
def set_compare():
    its = []
    for (desc1, m1, b1), (desc2, m2, b2), ask in [
        (("Function A: y = 3x + 2", 3, 2), ("Function B: the table (0, 1), (1, 5), (2, 9)", 4, 1), "greater rate of change"),
        (("Function A: y = 2x + 5", 2, 5), ("Function B: a line through (0, 3) and (2, 9)", 3, 3), "greater initial value"),
        (("Function A: y = −x + 8", -1, 8), ("Function B: the table (0, 6), (2, 2), (4, −2)", -2, 6), "steeper graph"),
        (("Function A: y = 0.5x + 4", F(1, 2), 4), ("Function B: starts at 4 and goes up 1 each step", 1, 4), "greater rate of change"),
        (("Function A: y = 6x", 6, 0), ("Function B: the table (1, 5), (2, 10), (3, 15)", 5, 0), "greater rate of change"),
        (("Function A: y = 2x − 3", 2, -3), ("Function B: a line through (0, −1) and (3, 5)", 2, -1), "greater initial value"),
        (("Taxi A: $3 plus $2 per mile", 2, 3), ("Taxi B: y = 2.5x + 1", F(5, 2), 1), "higher cost per mile"),
        (("Plan A: $20 plus $5 a month", 5, 20), ("Plan B: the table (0, 35), (1, 38), (2, 41)", 3, 35), "higher starting cost"),
        (("Car A: y = 55x", 55, 0), ("Car B: 120 miles in 2 hours", 60, 0), "greater speed"),
        (("Tank A: y = −4x + 50", -4, 50), ("Tank B: starts at 60 gallons, loses 3 gallons a minute", -3, 60), "faster draining"),
    ]:
        if ask in ("greater rate of change", "higher cost per mile", "greater speed"):
            v1, v2 = m1, m2
        elif ask in ("greater initial value", "higher starting cost"):
            v1, v2 = b1, b2
        elif ask == "steeper graph":
            v1, v2 = abs(F(m1)), abs(F(m2))
        else:   # faster draining
            v1, v2 = -F(m1), -F(m2)
        ans = "A" if v1 > v2 else ("B" if v2 > v1 else "They are the same")
        q = "%s. %s. Which has the %s?" % (desc1, desc2, ask)
        e = "A: rate %s, start %s. B: rate %s, start %s. The answer is <b>%s</b>." % (sl(m1), num(b1), sl(m2), num(b2), ans)
        its.append(mcq(q, (ans, ans), [(c, c) for c in ["A", "B", "They are the same", "We cannot tell"] if c != ans], e))
    for q, ans, wr, e in [
        ("Function A: y = 4x + 1. Function B goes through (0, 1) and (1, 5). How do they compare?", "They are the same function",
         ["A is steeper", "B is steeper", "They have different starting values"], "B has slope (5 − 1) ÷ 1 = 4 and starts at 1: <b>they are the same function</b>."),
        ("What is the initial value of the function in the table (0, 7), (1, 10), (2, 13)?", "7", ["3", "10", "0"],
         "The initial value is the output when x = 0: <b>7</b>."),
        ("What is the rate of change in the table (0, 7), (1, 10), (2, 13)?", "3", ["7", "10", "1/3"],
         "Each time x goes up 1, y goes up 3. The rate of change is <b>3</b>."),
        ("A function starts at 12 and goes down 2 each step. Which equation is it?", "y = −2x + 12", ["y = 12x − 2", "y = 2x + 12", "y = −12x + 2"],
         "Rate −2, initial value 12: <b>y = −2x + 12</b>."),
        ("Which describes y = 7 − 3x?", "Starts at 7 and goes down 3 each step", ["Starts at 3 and goes up 7", "Starts at −3 and goes up 7",
         "Starts at 7 and goes up 3"], "y = −3x + 7: initial value 7, rate −3. <b>Starts at 7 and goes down 3 each step</b>."),
        ("Function A: y = 3x. Function B: y = x². For x = 2, which is greater?", "A", ["B", "They are equal", "We cannot tell"],
         "A: 3 × 2 = 6. B: 2² = 4. <b>A</b> is greater."),
        ("Function A: y = 3x. Function B: y = x². For x = 5, which is greater?", "B", ["A", "They are equal", "We cannot tell"],
         "A: 15. B: 25. <b>B</b> is greater. A nonlinear function can pass a linear one."),
        ("A gym charges y = 25x + 50. What does 50 mean?", "A one-time fee of $50", ["$50 each month", "50 months", "The total after 1 month"],
         "The initial value is the cost at x = 0 months: <b>a one-time fee of $50</b>."),
        ("A gym charges y = 25x + 50. What does 25 mean?", "$25 each month", ["A one-time fee of $25", "25 months", "$25 in all"],
         "The rate of change is the cost for each month: <b>$25 each month</b>."),
        ("Line A has slope 2 and starts at 0. Line B has slope 2 and starts at 5. Which is true?", "They are parallel",
         ["They cross at (0, 0)", "B is steeper", "They are the same line"], "Same slope, different starts: <b>they are parallel</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[11], o[12], o[0], o[13], o[1], o[14], o[2], o[17], o[3], o[18], o[4], o[10], o[5], o[15], o[6], o[16], o[7],
             o[19], o[8], o[9]]
    return {"title": "Compare functions", "items": order}


def body():
    return ("<h2>What is a function?</h2>"
            "<p>A <b>function</b> is a rule that gives each input <b>exactly one</b> output. "
            "Outputs can repeat, but an input cannot have two different outputs.</p>"
            + table(["Relation", "Function?", "Why"], [
                ["(1, 3), (2, 3), (3, 3)", "Yes", "each input has one output"],
                ["(2, 1), (2, 5), (3, 6)", "No", "input 2 has two outputs"]])
            + "<h2>The vertical line test</h2><p>If any vertical line crosses a graph more than once, the graph is not a function.</p>"
            + example("If f(x) = 3x − 2, find f(4).", ["Replace x with 4: 3 × 4 − 2.", "12 − 2 = 10."], "f(4) = 10")
            + "<h2>Linear or nonlinear?</h2><p>A <b>linear</b> function has a constant rate of change and a straight-line graph: y = mx + b. "
            "If x is squared, cubed, in an exponent or in the bottom of a fraction, the function is <b>nonlinear</b>.</p>"
            + "<h2>Common mistakes</h2><ul><li>Thinking repeated outputs break a function. Only repeated inputs with different outputs do.</li>"
            "<li>Using a horizontal line for the test. Use a vertical line.</li>"
            "<li>Thinking every curve is not a function. y = x² is a function.</li></ul>")


def main():
    sets = [set_relations(), set_graphs(), set_eval(), set_linear(), set_compare()]
    balance(sets, R)
    unit = {
        "slug": "functions",
        "title": "Functions: Inputs and Outputs",
        "seo_title": "Grade 8 Functions Worksheets: Is It a Function, Vertical Line Test, Linear or Nonlinear",
        "short_title": "Functions",
        "domain": "Functions",
        "standard_code": "8.F.A.1",
        "standard_url": "https://www.thecorestandards.org/Math/Content/8/F/A/1/",
        "standard_text": "Understand that a function is a rule that assigns to each input exactly one output. The graph of a function is the set of ordered pairs consisting of an input and the corresponding output.",
        "meta_desc": "Free Grade 8 functions worksheets: decide if a relation is a function from pairs, tables and graphs, use the vertical line test, evaluate f(x), tell linear from nonlinear, and compare functions. 100 questions with an answer key.",
        "key_big": "A function gives each input exactly one output.",
        "key_sub": "Outputs may repeat. If a vertical line crosses the graph twice, it is not a function.",
        "body_html": body(),
        "faq": [
            {"q": "How do you know if a relation is a function?", "a": "Check the inputs. If any input has two different outputs, it is not a function. Outputs may repeat."},
            {"q": "What is the vertical line test?", "a": "Draw vertical lines through the graph. If any of them crosses the graph more than once, the graph is not a function."},
            {"q": "What does f(x) mean?", "a": "f(x) is the output of the function f for the input x. f(4) means put 4 in for x."},
            {"q": "How do you tell if a function is linear?", "a": "A linear function changes by the same amount each step and its graph is a straight line. It can be written as y = mx + b."}],
        "sets": sets, "pdf_url": "", "sort": 4, "updated": UPDATED,
    }
    write_unit("us", "math", "grade-8", unit)


if __name__ == "__main__":
    main()
