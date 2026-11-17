# -*- coding: utf-8 -*-
"""
US Algebra 1: Domain and Range (Common Core F-IF.A.1, F-IF.B.5)
  python3 tools/gen_us_math_a1_domain_and_range.py
Domain and range of sets of ordered pairs, of graphs (segments with open and closed endpoints), and of
linear, quadratic, absolute value and square root functions; inequality and interval notation; and
reasonable domains in real situations.
Wrong answers come from real mistakes: swapping domain (x) and range (y), listing repeated values or
leaving values out, using a closed bracket for an open endpoint, and giving all real numbers for a
quantity that can only be a whole number or must stay positive.
"""
import random
from fractions import Fraction as F
from us_hs import num, B, S, make, lesson, collect, T, expr, MINUS, fig
from g8_common import grid_svg
from ws_common import BLUE, RED

R = random.Random(90601)
X = "<i>x</i>"
Y = "<i>y</i>"
LT, LE = "&lt;", "≤"
ALL = "All real numbers"


def setx(vs):
    return "{%s}" % ", ".join(num(v) for v in sorted(set(vs)))


# ------------------------------------------------------------ set 1: ordered pairs
def one_pairs(r):
    n = r.randint(4, 5)
    xs = r.sample(range(-5, 8), n)
    ys = [r.randint(-4, 9) for _ in xs]
    if len(set(ys)) == n and r.random() < 0.6:
        ys[1] = ys[0]
    pts = ", ".join("(%s, %s)" % (num(a), num(b)) for a, b in zip(xs, ys))
    if r.random() < 0.5:
        q = "What is the domain of the relation %s?" % B("{%s}" % pts)
        right = setx(xs)
        wr = [setx(ys), setx(xs + ys), setx(xs[:-1])]
        e = "The domain is the set of <b>inputs</b> (the <i>x</i>-values): <b>%s</b>." % right
    else:
        q = "What is the range of the relation %s?" % B("{%s}" % pts)
        right = setx(ys)
        wr = [setx(xs), "{%s}" % ", ".join(num(v) for v in ys) if len(set(ys)) < len(ys) else setx(xs + ys), setx(ys[:-1]) if len(set(ys[:-1])) < len(set(ys)) else setx(ys + [ys[0] + 10])]
        e = "The range is the set of <b>outputs</b> (the <i>y</i>-values), each listed once: <b>%s</b>." % right
    wr = [w for w in dict.fromkeys(wr) if w != right]
    if len(wr) < 3:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 2: graphs
def seg_svg(x1, y1, c1, x2, y2, c2):
    lo, hi = -6, 6
    svg = grid_svg(lo, hi, segs=[(x1, y1, x2, y2, BLUE)], unit=22, label="graph of a line segment")
    m, u = 22, 22
    X_ = lambda x: m + (x - lo) * u
    Y_ = lambda y: m + (hi - y) * u
    dots = ""
    for x, y, c in ((x1, y1, c1), (x2, y2, c2)):
        dots += "<circle cx='%.1f' cy='%.1f' r='5' fill='%s' stroke='%s' stroke-width='2.5'/>" % (X_(x), Y_(y), BLUE if c else "#fff", BLUE)
    return svg.replace("</svg>", dots + "</svg>")


def ineq(lo, s1, var, s2, hi):
    return "%s %s %s %s %s" % (num(lo), s1, var, s2, num(hi))


def one_graph(r):
    x1, x2 = sorted(r.sample(range(-5, 6), 2))
    if x2 - x1 < 2:
        return None
    y1, y2 = r.randint(-5, 5), r.randint(-5, 5)
    if y1 == y2:
        return None
    c1, c2 = r.random() < 0.6, r.random() < 0.6
    pic = fig(seg_svg(x1, y1, c1, x2, y2, c2))
    sx1, sx2 = (LE if c1 else LT), (LE if c2 else LT)
    if r.random() < 0.5:
        q = "What is the domain of the function shown?%s" % pic
        right = ineq(x1, sx1, X, sx2, x2)
        ylo, yhi = min(y1, y2), max(y1, y2)
        wr = [ineq(ylo, LE, X, LE, yhi), ineq(x1, LT if c1 else LE, X, LT if c2 else LE, x2), ineq(x1, LE, X, LE, x2) if not (c1 and c2) else ineq(x1, LT, X, LT, x2)]
        e = "Read the <i>x</i>-values from left to right: from %s to %s. A filled dot is included (≤); an open dot is not (&lt;). So <b>%s</b>." % (num(x1), num(x2), right)
    else:
        q = "What is the range of the function shown?%s" % pic
        (ylo, clo), (yhi, chi) = sorted([(y1, c1), (y2, c2)])
        right = ineq(ylo, LE if clo else LT, Y, LE if chi else LT, yhi)
        wr = [ineq(x1, sx1, Y, sx2, x2), ineq(ylo, LT if clo else LE, Y, LT if chi else LE, yhi), ineq(yhi, LE, Y, LE, ylo)]
        e = "Read the <i>y</i>-values from bottom to top: from %s to %s. Filled dots are included and open dots are not. So <b>%s</b>." % (num(ylo), num(yhi), right)
    wr = [w for w in dict.fromkeys(wr) if w != right]
    if len(wr) < 3:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 3: rules
def one_rule(r):
    kind = r.choice(["lin", "quad_up", "quad_down", "abs", "sqrt", "sqrt_d"])
    if kind == "lin":
        m, b = r.choice([2, -3, 4, 1, -1, 5]), r.randint(-8, 8)
        q = "What is the range of %s?" % B("<i>f</i>(<i>x</i>) = %s" % expr([(m, X), (b, "")]))
        return T(q, ALL, ["<i>y</i> ≥ %s" % num(b), "<i>y</i> ≥ 0", "<i>x</i> ≥ %s" % num(b)], "A non-horizontal line goes up and down forever, so the range is <b>all real numbers</b>.")
    if kind in ("quad_up", "quad_down"):
        h, k = r.randint(-5, 5), r.randint(-8, 8)
        sgn = 1 if kind == "quad_up" else -1
        inside = expr([(1, X), (-h, "")])
        rule = ("%s(%s)<sup>2</sup>" % ("" if sgn == 1 else MINUS, inside) if h else ("%s<i>x</i><sup>2</sup>" % ("" if sgn == 1 else MINUS)))
        rule += (" %s %s" % ("+" if k > 0 else MINUS, num(abs(k)))) if k else ""
        q = "What is the range of %s?" % B("<i>f</i>(<i>x</i>) = %s" % rule)
        right = "<i>y</i> %s %s" % ("≥" if sgn == 1 else "≤", num(k))
        wr = ["<i>y</i> %s %s" % ("≤" if sgn == 1 else "≥", num(k)), ALL, "<i>y</i> %s %s" % ("≥" if sgn == 1 else "≤", num(h)) if h != k else "<i>x</i> ≥ %s" % num(h)]
        e = "The vertex is (%s, %s). The parabola opens %s, so the %s value of <i>y</i> is %s: <b>%s</b>. The domain is all real numbers." % (
            num(h), num(k), "up" if sgn == 1 else "down", "smallest" if sgn == 1 else "largest", num(k), right)
        return T(q, right, wr, e)
    if kind == "abs":
        h, k = r.randint(-5, 5), r.randint(-6, 6)
        rule = "|%s|" % expr([(1, X), (-h, "")]) + ((" %s %s" % ("+" if k > 0 else MINUS, num(abs(k)))) if k else "")
        q = "What is the range of %s?" % B("<i>g</i>(<i>x</i>) = %s" % rule)
        right = "<i>y</i> ≥ %s" % num(k)
        wr = ["<i>y</i> ≥ 0" if k else "<i>y</i> ≤ 0", ALL, "<i>y</i> ≤ %s" % num(k) if k else "<i>y</i> ≥ %s" % num(h if h else 1)]
        e = "An absolute value is never negative, so the smallest value of %s is %s. So <b>%s</b>." % (rule, num(k), right)
        wr = [w for w in dict.fromkeys(wr) if w != right]
        if len(wr) < 3:
            return None
        return T(q, right, wr, e)
    a = r.randint(-6, 6)
    k = r.randint(-5, 5)
    rad = "√(%s)" % expr([(1, X), (-a, "")]) if a else "√<i>x</i>"
    rule = rad + ((" %s %s" % ("+" if k > 0 else MINUS, num(abs(k)))) if k else "")
    if kind == "sqrt":
        q = "What is the domain of %s?" % B("<i>h</i>(<i>x</i>) = %s" % rule)
        right = "<i>x</i> ≥ %s" % num(a)
        wr = ["<i>x</i> ≥ %s" % num(-a) if a else "<i>x</i> &gt; 0", "<i>x</i> ≤ %s" % num(a), ALL]
        e = "You cannot take the square root of a negative number, so %s ≥ 0: <b>%s</b>." % (expr([(1, X), (-a, "")]), right)
    else:
        q = "What is the range of %s?" % B("<i>h</i>(<i>x</i>) = %s" % rule)
        right = "<i>y</i> ≥ %s" % num(k)
        wr = ["<i>y</i> ≥ %s" % num(a) if a != k else "<i>y</i> ≥ 0" if k else "<i>y</i> ≤ 0", ALL, "<i>y</i> ≤ %s" % num(k)]
        e = "A square root is never negative, so the smallest output is %s: <b>%s</b>." % (num(k), right)
    wr = [w for w in dict.fromkeys(wr) if w != right]
    if len(wr) < 3:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 4: interval notation
def one_interval(r):
    a = r.randint(-8, 5)
    b = a + r.randint(2, 9)
    kind = r.choice(["both", "both", "ray_r", "ray_l", "back"])
    if kind == "both":
        c1, c2 = r.random() < 0.5, r.random() < 0.5
        q = "Write %s in interval notation." % B(ineq(a, LE if c1 else LT, X, LE if c2 else LT, b))
        right = "%s%s, %s%s" % ("[" if c1 else "(", num(a), num(b), "]" if c2 else ")")
        wr = ["%s%s, %s%s" % ("(" if c1 else "[", num(a), num(b), ")" if c2 else "]"), "%s%s, %s%s" % ("[" if c1 else "(", num(b), num(a), "]" if c2 else ")"),
              "%s%s, %s%s" % ("[" if c1 else "(", num(a), num(b), ")" if c2 else "]")]
        e = "Use a square bracket [ ] when the endpoint is included (≤) and a parenthesis ( ) when it is not (&lt;): <b>%s</b>." % right
    elif kind == "ray_r":
        c = r.random() < 0.5
        q = "Write %s in interval notation." % B("%s %s %s" % (X, "≥" if c else "&gt;", num(a)))
        right = "%s%s, ∞)" % ("[" if c else "(", num(a))
        wr = ["%s%s, ∞)" % ("(" if c else "[", num(a)), "(−∞, %s%s" % (num(a), "]" if c else ")"), "%s%s, ∞]" % ("[" if c else "(", num(a))]
        e = "The values go up forever, and ∞ always gets a parenthesis: <b>%s</b>." % right
    elif kind == "ray_l":
        c = r.random() < 0.5
        q = "Write %s in interval notation." % B("%s %s %s" % (X, "≤" if c else "&lt;", num(b)))
        right = "(−∞, %s%s" % (num(b), "]" if c else ")")
        wr = ["(−∞, %s%s" % (num(b), ")" if c else "]"), "%s%s, ∞)" % ("[" if c else "(", num(b)), "[−∞, %s%s" % (num(b), "]" if c else ")")]
        e = "The values go down forever, and −∞ always gets a parenthesis: <b>%s</b>." % right
    else:
        c1, c2 = r.random() < 0.5, r.random() < 0.5
        iv = "%s%s, %s%s" % ("[" if c1 else "(", num(a), num(b), "]" if c2 else ")")
        q = "Which inequality means the same as %s?" % B(iv)
        right = ineq(a, LE if c1 else LT, X, LE if c2 else LT, b)
        wr = [ineq(a, LT if c1 else LE, X, LT if c2 else LE, b), "%s ≤ %s or %s ≥ %s" % (X, num(a), X, num(b)), ineq(a, LE if c1 else LT, X, LT if c2 else LE, b)]
        e = "[ means included (≤), ( means not included (&lt;): <b>%s</b>." % right
    wr = [w for w in dict.fromkeys(wr) if w != right]
    if len(wr) < 3:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 5: reasonable domains
def problems():
    data = [
        ("Movie tickets cost $11 each. <i>C</i>(<i>n</i>) = 11<i>n</i> is the cost of <i>n</i> tickets. A family can buy at most 6 tickets. What is a reasonable domain?", "{0, 1, 2, 3, 4, 5, 6}",
         ["0 ≤ <i>n</i> ≤ 6", "0 ≤ <i>n</i> ≤ 66", "All real numbers"], "You can only buy whole numbers of tickets: <b>{0, 1, 2, 3, 4, 5, 6}</b>."),
        ("Movie tickets cost $11 each. <i>C</i>(<i>n</i>) = 11<i>n</i> is the cost of <i>n</i> tickets, and a family buys at most 6. What is the range?", "{0, 11, 22, 33, 44, 55, 66}", ["0 ≤ <i>C</i> ≤ 66", "{0, 1, 2, 3, 4, 5, 6}", "<i>C</i> ≥ 0"], "Multiply each input by 11: <b>{0, 11, 22, 33, 44, 55, 66}</b>."),
        ("A ball is dropped from a 64 ft tower and hits the ground after 2 seconds. <i>h</i>(<i>t</i>) is its height. What is a reasonable domain?", "0 ≤ <i>t</i> ≤ 2", ["0 ≤ <i>t</i> ≤ 64", "<i>t</i> ≥ 0", "All real numbers"],
         "Time runs from the drop (0 s) until it lands (2 s): <b>0 ≤ <i>t</i> ≤ 2</b>."),
        ("A ball is dropped from a 64 ft tower and lands after 2 seconds. <i>h</i>(<i>t</i>) is its height in feet. What is the range?", "0 ≤ <i>h</i> ≤ 64", ["0 ≤ <i>h</i> ≤ 2", "<i>h</i> ≥ 64", "<i>h</i> ≤ 0"], "The height goes from 64 ft down to 0 ft: <b>0 ≤ <i>h</i> ≤ 64</b>."),
        ("A car's 15-gallon tank is full. It uses 1 gallon every 30 miles. <i>G</i>(<i>d</i>) is the fuel left after <i>d</i> miles. What is a reasonable domain?", "0 ≤ <i>d</i> ≤ 450",
         ["0 ≤ <i>d</i> ≤ 15", "<i>d</i> ≥ 0", "0 ≤ <i>d</i> ≤ 30"], "The tank lasts 15 × 30 = 450 miles: <b>0 ≤ <i>d</i> ≤ 450</b>."),
        ("<i>A</i>(<i>w</i>) = <i>w</i>(20 − <i>w</i>) is the area of a rectangle with perimeter 40 cm and width <i>w</i>. What is a reasonable domain?", "0 &lt; <i>w</i> &lt; 20",
         ["0 ≤ <i>w</i> ≤ 40", "<i>w</i> &gt; 0", "All real numbers"], "Both the width and the length 20 − <i>w</i> must be positive: <b>0 &lt; <i>w</i> &lt; 20</b>."),
        ("Which situation has a domain of whole numbers only?", "The cost of buying <i>n</i> pencils", ["The distance a car travels in <i>t</i> hours", "The temperature at time <i>t</i>", "The weight of <i>p</i> pounds of apples"],
         "You can't buy part of a pencil: <b>the cost of buying <i>n</i> pencils</b>."),
        ("Is the relation {(1, 4), (2, 5), (1, 6)} a function?", "No, the input 1 has two outputs", ["Yes, every output is different", "Yes, it has three points", "No, the outputs are not in order"],
         "A function gives each input exactly one output. Input 1 gives 4 and 6: <b>not a function</b>."),
        ("What is the domain of <i>f</i>(<i>x</i>) = <i>x</i><sup>2</sup> − 3?", ALL, ["<i>x</i> ≥ −3", "<i>x</i> ≥ 0", "<i>y</i> ≥ −3"], "You can square any number: <b>all real numbers</b>. (The range is <i>y</i> ≥ −3.)"),
        ("What is the domain of <i>f</i>(<i>x</i>) = √(<i>x</i> + 4)?", "<i>x</i> ≥ −4", ["<i>x</i> ≥ 4", "<i>x</i> ≥ 0", ALL], "<i>x</i> + 4 ≥ 0, so <b><i>x</i> ≥ −4</b>."),
        ("A gym membership costs $35 a month. <i>C</i>(<i>m</i>) = 35<i>m</i> is the cost for <i>m</i> months, for up to one year. What is the range?", "{35, 70, 105, …, 420}", ["0 ≤ <i>C</i> ≤ 12", "{1, 2, 3, …, 12}", "<i>C</i> ≥ 35"],
         "Months are whole numbers from 1 to 12, so costs are multiples of 35 up to 420: <b>{35, 70, …, 420}</b>."),
        ("A phone battery drains from 100% to 0% in 20 hours. <i>B</i>(<i>t</i>) is the charge after <i>t</i> hours. What is the range?", "0 ≤ <i>B</i> ≤ 100", ["0 ≤ <i>B</i> ≤ 20", "<i>B</i> ≥ 100", "0 ≤ <i>t</i> ≤ 20"], "The charge goes from 100 down to 0: <b>0 ≤ <i>B</i> ≤ 100</b>."),
        ("What is the domain of the relation shown by the table: <i>x</i> = 2, 4, 6, 8 and <i>y</i> = 5, 9, 13, 17?", "{2, 4, 6, 8}", ["{5, 9, 13, 17}", "2 ≤ <i>x</i> ≤ 8", "{2, 5, 4, 9}"], "Only these four inputs are shown: <b>{2, 4, 6, 8}</b>."),
        ("Which interval is the domain of a function that is defined for every number greater than −3?", "(−3, ∞)", ["[−3, ∞)", "(−∞, −3)", "(−3, ∞]"], "Greater than −3, not including −3: <b>(−3, ∞)</b>."),
        ("A pool fills at 50 gallons per minute and holds 2,000 gallons. <i>V</i>(<i>t</i>) is the water in the pool. What is a reasonable domain?", "0 ≤ <i>t</i> ≤ 40", ["0 ≤ <i>t</i> ≤ 2,000", "0 ≤ <i>t</i> ≤ 50", "<i>t</i> ≥ 40"], "2,000 ÷ 50 = 40 minutes: <b>0 ≤ <i>t</i> ≤ 40</b>."),
        ("The range of <i>f</i>(<i>x</i>) = −<i>x</i><sup>2</sup> + 9 is…", "<i>y</i> ≤ 9", ["<i>y</i> ≥ 9", ALL, "<i>y</i> ≤ −9"], "It opens down with vertex (0, 9), so the largest value is 9: <b><i>y</i> ≤ 9</b>."),
        ("Which set of points is a function with domain {1, 2, 3}?", "{(1, 7), (2, 7), (3, 8)}", ["{(1, 2), (1, 3), (2, 3)}", "{(7, 1), (7, 2), (8, 3)}", "{(1, 7), (2, 8)}"],
         "Each input 1, 2, 3 appears once: <b>{(1, 7), (2, 7), (3, 8)}</b>. Repeated outputs are fine."),
        ("A store sells boxes of 12 donuts. <i>D</i>(<i>b</i>) = 12<i>b</i> is the number of donuts in <i>b</i> boxes. Which number cannot be in the range?", "30", ["0", "36", "60"], "Outputs are multiples of 12. <b>30</b> is not."),
        ("What are the domain and range of <i>f</i>(<i>x</i>) = 7 (a horizontal line)?", "Domain: all real numbers; range: {7}", ["Domain: {7}; range: all real numbers", "Both are all real numbers", "Domain: <i>x</i> ≥ 7; range: <i>y</i> ≥ 7"],
         "Every input is allowed, but the only output is 7: <b>domain all real numbers, range {7}</b>."),
        ("Diego works up to 25 hours a week at $16 an hour. <i>P</i>(<i>h</i>) = 16<i>h</i>. What is the greatest value in the range?", "$400", ["$25", "$41", "$16"], "16 × 25 = <b>$400</b>."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>The <b>domain</b> is the set of all inputs (<i>x</i>-values). The <b>range</b> is the set of all outputs (<i>y</i>-values). "
        "For a list of points, list each value once. For a graph, read the <i>x</i>-values from left to right (domain) and the "
        "<i>y</i>-values from bottom to top (range). A filled dot is included; an open dot is not.</p>"
        "<p>Write intervals with inequalities (−2 ≤ <i>x</i> &lt; 5) or interval notation ([−2, 5)): a square bracket means included, "
        "a parenthesis means not included, and ∞ always gets a parenthesis.</p>"
        "<p>In a real situation, use a <b>reasonable domain</b>: you cannot buy −2 tickets or 2.5 tickets.</p>",
        [("Find the domain and range of {(2, 5), (−1, 3), (4, 5)}.", ["Inputs: 2, −1, 4.", "Outputs: 5, 3, 5 (list 5 once)."], "Domain {−1, 2, 4}; range {3, 5}"),
         ("Find the range of <i>f</i>(<i>x</i>) = (<i>x</i> − 1)<sup>2</sup> + 3.", ["The vertex is (1, 3) and the parabola opens up."], "<i>y</i> ≥ 3"),
         ("Find the domain of <i>g</i>(<i>x</i>) = √(<i>x</i> − 2).", ["<i>x</i> − 2 ≥ 0."], "<i>x</i> ≥ 2")],
        ["Swapping domain and range. Domain is <i>x</i> (inputs); range is <i>y</i> (outputs).",
         "Listing a repeated value twice, or leaving a value out.",
         "Using ≤ or [ for an open dot. Open dots mean the value is not included.",
         "Giving “all real numbers” for something that must be a whole number or must be positive, such as tickets or time."])


def main():
    sets = [S("Domain and range of ordered pairs", collect(one_pairs, 20, R)),
            S("Domain and range from graphs", collect(one_graph, 20, R)),
            S("Domain and range from rules", collect(one_rule, 20, R)),
            S("Inequality and interval notation", collect(one_interval, 20, R)),
            S("Reasonable domain and range", problems())]
    make("domain-and-range", 6, "F-IF.A.1",
         "Domain and Range: Ordered Pairs, Graphs, Rules and Interval Notation",
         "Algebra 1 Domain and Range Worksheets: Graphs, Functions and Interval Notation (Free, Answer Key)",
         "Domain and range",
         "Understand that a function from one set (called the domain) to another set (called the range) assigns to each element of "
         "the domain exactly one element of the range.",
         "Free Algebra 1 domain and range worksheets (F-IF.A.1, F-IF.B.5): ordered pairs, graphs with open and closed endpoints, "
         "linear, quadratic, absolute value and square root functions, interval notation and reasonable domains. 100 questions with an answer key.",
         "Domain = all the inputs (x). Range = all the outputs (y).",
         "Filled dot or ≤ means included: [ ]. Open dot or < means not included: ( ).",
         body(),
         [("What is the difference between domain and range?", "The domain is every input (x-value) a function can take. The range is every output (y-value) it gives."),
          ("How do you find the domain and range from a graph?", "Read the x-values from the leftmost point to the rightmost point for the domain, and the y-values from the lowest to the highest point for the range."),
          ("What is the range of a quadratic function?", "If the parabola opens up, the range is y ≥ the y-coordinate of the vertex. If it opens down, the range is y ≤ that value."),
          ("What is a reasonable domain?", "The inputs that make sense in the situation. A number of people must be a whole number, and time is usually 0 or more.")],
         sets, R, domain="Functions")


if __name__ == "__main__":
    main()
