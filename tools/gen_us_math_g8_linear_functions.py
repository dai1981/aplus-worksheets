# -*- coding: utf-8 -*-
"""
US Grade 8 Math: Linear Functions - Writing y = mx + b (8.F.B.4, 8.F.B.5)
  python3 tools/gen_us_math_g8_linear_functions.py
Write the equation of a line from a graph, from two points, from a table and from words;
explain what the slope and the initial value mean; and describe qualitative graphs.
Wrong answers come from real mistakes: swapping m and b, using run over rise, a sign slip in b,
and using a point's y-value as the intercept.
"""
import random
from fractions import Fraction as F
from ws_common import num, mcq, balance, B, table, example, write_unit, fig, X, MINUS, RED, BLUE
from g8_common import lin, grid_svg, xy_table, sl

R = random.Random(80501)
UPDATED = "2026-11-16"
Y = "<i>y</i>"


def yeq(m, b):
    return "%s = %s" % (Y, lin(m, b))


def eq_choices(m, b, py=None):
    m, b = F(m), F(b)
    cands = [(b, m), (m, -b), (1 / m if m else None, b), (-m, b), (m, py) if py is not None else None, (m, b + 1)]
    out = []
    for c in cands:
        if c is None or c[0] is None or c[1] is None:
            continue
        out.append((yeq(c[0], c[1]), (F(c[0]), F(c[1]))))
    return out


# ============================================================ set 1: from a graph
def set_graph():
    its = []
    for m, b in [(2, 1), (-1, 3), (F(1, 2), -2), (3, -4), (F(-2, 3), 2), (1, 0), (-2, -1), (F(3, 4), 1), (F(-1, 3), 4), (4, 2),
                 (0, -3), (F(5, 2), -5), (-3, 5), (F(2, 5), -1), (-1, -4), (F(3, 2), 0), (2, -6), (F(-4, 3), 3), (5, 1), (F(-1, 2), -2)]:
        pts = [(x, m * x + b) for x in range(-6, 7) if (m * x + b).denominator == 1 and -6 <= m * x + b <= 6]
        show = [pts[0], pts[-1]] if len(pts) >= 2 else pts
        svg = grid_svg(-6, 6, lines=[(m, b, BLUE)], points=[(x, y, "", RED) for x, y in show], unit=18)
        e = ("The line crosses the y-axis at %s, so b = %s. From %s to %s the slope is %s. The equation is <b>%s</b>."
             % (num(b), num(b), "(%s, %s)" % (num(show[0][0]), num(show[0][1])), "(%s, %s)" % (num(show[-1][0]), num(show[-1][1])),
                sl(m), yeq(m, b)))
        its.append(mcq(fig(svg) + "Which equation matches the line?", (yeq(m, b), (F(m), F(b))), eq_choices(m, b), e))
    return {"title": "Write the equation from a graph", "items": its}


# ============================================================ set 2: two points
def set_points():
    its = []
    for (x1, y1), (x2, y2) in [((0, 3), (2, 7)), ((1, 5), (3, 9)), ((2, 1), (4, -3)), ((-1, 2), (1, 6)), ((0, -4), (3, 2)),
                               ((2, 8), (5, 14)), ((-2, 7), (2, -1)), ((3, 3), (6, 5)), ((4, -1), (8, 1)), ((1, -2), (4, -11)),
                               ((-3, -5), (0, 1)), ((5, 10), (10, 12)), ((2, 2), (6, 0)), ((-4, 1), (4, 5)), ((6, -2), (9, -3)),
                               ((-1, -7), (2, 5)), ((0, 0), (5, -3)), ((3, 12), (5, 20)), ((-6, 2), (3, -4)), ((8, 1), (-4, 4))]:
        m = F(y2 - y1, x2 - x1)
        b = y1 - m * x1
        q = "Which equation is the line through %s and %s?" % (B("(%s, %s)" % (num(x1), num(y1))), B("(%s, %s)" % (num(x2), num(y2))))
        e = ("Slope = (%s − %s) ÷ (%s − %s) = %s. Then %s = %s × %s + b, so b = %s. Equation: <b>%s</b>."
             % (num(y2), "(%s)" % num(y1) if y1 < 0 else num(y1), num(x2), "(%s)" % num(x1) if x1 < 0 else num(x1), sl(m),
                num(y1), sl(m), "(%s)" % num(x1) if x1 < 0 else num(x1), num(b), yeq(m, b)))
        its.append(mcq(q, (yeq(m, b), (m, b)), eq_choices(m, b, py=y1 if y1 != b else None), e))
    return {"title": "Write the equation from two points", "items": its}


# ============================================================ set 3: tables and words
def set_tables():
    its = []
    for x0, dx, m, b in [(0, 1, 3, 2), (0, 2, F(1, 2), 5), (1, 1, -4, 10), (0, 1, -1, 0), (2, 2, 3, -1), (0, 5, F(2, 5), 3),
                         (-1, 1, 2, -3), (0, 3, F(-1, 3), 6), (3, 1, 5, -12), (0, 4, F(3, 4), -2)]:
        xs = [x0 + k * dx for k in range(4)]
        ys = [m * x + b for x in xs]
        tbl = xy_table([num(v) for v in xs], [num(v) for v in ys])
        e = ("y changes by %s when x goes up by %s, so m = %s. When x = 0, y = %s, so b = %s. Equation: <b>%s</b>."
             % (num(m * dx), num(dx), sl(m), num(b), num(b), yeq(m, b)))
        its.append(mcq(tbl + "Which equation fits the table?", (yeq(m, b), (F(m), F(b))),
                       eq_choices(m, b, py=ys[0] if ys[0] != b else None), e))
    for txt, m, b, mean in [
        ("A plumber charges $60 to come and $45 for each hour.", 45, 60, "x = hours, y = total cost"),
        ("A candle is 30 cm tall and burns 2 cm each hour.", -2, 30, "x = hours, y = height"),
        ("A phone plan costs $15 a month plus $0.10 per text.", F(1, 10), 15, "x = texts, y = cost"),
        ("A tank holds 500 gallons and drains 25 gallons a minute.", -25, 500, "x = minutes, y = gallons"),
        ("A taxi charges $3.50 plus $2 per mile.", 2, F(7, 2), "x = miles, y = cost"),
        ("Sam has $40 saved and adds $12 each week.", 12, 40, "x = weeks, y = savings"),
        ("A plant is 5 cm tall and grows 1.5 cm a week.", F(3, 2), 5, "x = weeks, y = height"),
        ("An elevator starts 120 feet up and goes down 8 feet each second.", -8, 120, "x = seconds, y = height"),
        ("A pool is filled with 200 gallons, then 50 gallons more each hour.", 50, 200, "x = hours, y = gallons"),
        ("A gift card has $75 and each coffee costs $3.", -3, 75, "x = coffees, y = money left"),
    ]:
        e = "The starting amount is b = %s. The change for each unit is m = %s. Equation: <b>%s</b> (%s)." % (num(b), num(m), yeq(m, b), mean)
        its.append(mcq("%s Which equation models it? (%s)" % (txt, mean), (yeq(m, b), (F(m), F(b))), eq_choices(m, b), e))
    o = its
    order = [o[0], o[10], o[1], o[11], o[2], o[12], o[3], o[13], o[4], o[14], o[5], o[15], o[6], o[16], o[7], o[17], o[8],
             o[18], o[9], o[19]]
    return {"title": "Equations from tables and words", "items": order}


# ============================================================ set 4: meaning of m and b
def set_meaning():
    its = []
    for eqtxt, ask, ans, wr, e in [
        ("y = 25x + 100", "What does 25 mean? (x = months, y = dollars saved)", "$25 saved each month",
         ["$25 at the start", "25 months", "$125 in all"], "The slope is the change for each month: <b>$25 saved each month</b>."),
        ("y = 25x + 100", "What does 100 mean? (x = months, y = dollars saved)", "$100 at the start",
         ["$100 each month", "100 months", "$125 after 1 month"], "The y-intercept is the value when x = 0: <b>$100 at the start</b>."),
        ("y = −3x + 60", "What does −3 mean? (x = minutes, y = liters of water)", "3 liters drain each minute",
         ["3 liters at the start", "3 minutes", "60 liters drain each minute"], "A negative slope is a decrease: <b>3 liters drain each minute</b>."),
        ("y = −3x + 60", "What does 60 mean? (x = minutes, y = liters of water)", "60 liters at the start",
         ["60 minutes to empty", "60 liters each minute", "−3 liters at the start"], "At x = 0 there are <b>60 liters at the start</b>."),
        ("y = 0.5x + 2", "What does 0.5 mean? (x = miles, y = taxi cost in dollars)", "$0.50 per mile",
         ["$2 per mile", "0.5 miles", "$0.50 in all"], "The slope is the cost for each mile: <b>$0.50 per mile</b>."),
        ("y = 8x", "What is the initial value? (x = hours, y = dollars earned)", "$0 (no money at the start)",
         ["$8", "8 hours", "We cannot tell"], "y = 8x + 0, so the initial value is <b>$0 (no money at the start)</b>."),
        ("y = 12x + 5", "When x goes up by 2, how much does y go up?", "24", ["12", "14", "29"],
         "Each step of 1 adds 12, so 2 steps add 12 × 2 = <b>24</b>."),
        ("y = −4x + 9", "What is y when x = 0?", "9", ["−4", "5", "0"], "Put 0 in for x: −4(0) + 9 = <b>9</b>."),
        ("y = 3x − 7", "Where does the line cross the y-axis?", "(0, −7)", ["(0, 3)", "(−7, 0)", "(3, −7)"],
         "The y-intercept is b = −7, the point <b>(0, −7)</b>."),
        ("y = 15x + 30", "A gym: x = classes, y = total cost. What is the cost for 4 classes?", "$90", ["$49", "$60", "$120"],
         "15(4) + 30 = 60 + 30 = <b>$90</b>."),
    ]:
        its.append(mcq("In %s, %s" % (B(eqtxt), ask[0].lower() + ask[1:]), (ans, ans), [(w, w) for w in wr], e))
    for m, b, x, ask in [(4, 10, 6, "y"), (-2, 50, 15, "y"), (F(1, 2), 3, 8, "y"), (3, -5, None, 16), (-5, 40, None, 0),
                         (6, 12, None, 48), (2, 7, 9, "y"), (-1, 20, None, 8), (10, 0, 7, "y"), (F(3, 2), -1, None, 11)]:
        if x is not None:
            y = m * x + b
            q = "For %s, what is %s when %s = %s?" % (B(yeq(m, b)), Y, X, num(x))
            e = "%s × %s %s = <b>%s</b>." % (sl(m), num(x), ("+ " + num(b)) if b >= 0 else ("− " + num(-b)), num(y))
            its.append(mcq(q, (num(y), y), [(num(m + b), F(m + b)), (num(m * x), F(m * x)), (num(y + m), y + m), (num(-y), -y)], e))
        else:
            yv = ask
            xv = (yv - F(b)) / F(m)
            q = "For %s, what is %s when %s = %s?" % (B(yeq(m, b)), X, Y, num(yv))
            e = "Solve %s = %s: %s = %s, so %s = <b>%s</b>." % (num(yv), lin(m, b), lin(m, 0), num(yv - b), X, num(xv))
            its.append(mcq(q, (num(xv), xv), [(num(m * yv + b), F(m * yv + b)), (num((yv + b) / F(m)), (yv + b) / F(m)),
                                              (num(xv + 1), xv + 1), (num(-xv), -xv)], e))
    o = its
    order = [o[0], o[10], o[1], o[11], o[2], o[12], o[3], o[13], o[4], o[14], o[5], o[15], o[6], o[16], o[7], o[17], o[8],
             o[18], o[9], o[19]]
    return {"title": "What m and b mean", "items": order}


# ============================================================ set 5: qualitative graphs
def story_graph(segs, ylab="y"):
    """segs: list of (x1, y1, x2, y2) in a 0..10 box, drawn as one path."""
    from ws_common import svg_wrap, line, text, INK
    m, u = 26, 22
    W, H = 10 * u + 2 * m, 8 * u + 2 * m
    s = [line(m, H - m, W - m + 4, H - m, INK, 2), line(m, H - m, m, m - 4, INK, 2),
         text(W - m, H - m + 16, "time", 11, weight=400), text(m - 4, m - 8, ylab, 11, anchor="start", weight=400)]
    for x1, y1, x2, y2 in segs:
        s.append(line(m + x1 * u, H - m - y1 * u, m + x2 * u, H - m - y2 * u, BLUE, 3))
    return svg_wrap(W, H, "".join(s), "a graph of a story")


def set_story():
    its = []
    UP, DOWN, FLAT = "increasing", "decreasing", "constant"
    graphs = [
        ([(0, 1, 4, 5), (4, 5, 7, 5), (7, 5, 10, 1)], "height", "It goes up, stays the same, then goes down.",
         "It goes up, stays the same, then goes down", ["It goes down, stays the same, then goes up", "It goes up the whole time", "It stays the same the whole time"]),
        ([(0, 6, 5, 2), (5, 2, 10, 2)], "water", "It goes down, then stays the same.",
         "It goes down, then stays the same", ["It goes up, then stays the same", "It stays the same, then goes down", "It goes down the whole time"]),
        ([(0, 0, 3, 3), (3, 3, 6, 3), (6, 3, 10, 7)], "distance", "It goes up, stays the same, then goes up again.",
         "It goes up, stays the same, then goes up again", ["It goes up, then down, then up", "It goes up the whole time at the same speed", "It goes down, then up"]),
        ([(0, 2, 10, 2)], "speed", "It stays the same the whole time.",
         "It stays the same the whole time", ["It goes up", "It goes down", "It goes up, then down"]),
        ([(0, 7, 3, 4), (3, 4, 6, 6), (6, 6, 10, 1)], "temperature", "It goes down, goes up, then goes down.",
         "It goes down, goes up, then goes down", ["It goes up, goes down, then goes up", "It goes down the whole time", "It goes up the whole time"]),
    ]
    for segs, ylab, desc, ans, wr in graphs:
        its.append(mcq(fig(story_graph(segs, ylab)) + "Which describes the graph of %s over time?" % ylab, (ans, ans),
                       [(w, w) for w in wr], "Read from left to right. %s The answer is <b>%s</b>." % (desc, ans.lower())))
    stories = [
        ("Mia walks to school, stops to talk to a friend, then runs the rest of the way. Which graph shape fits distance from home?",
         "Up, flat, then up more steeply", ["Up, flat, then down", "Flat, up, then flat", "Down, flat, then down"],
         "Walking: going up. Stopping: flat. Running: going up faster (steeper). <b>Up, flat, then up more steeply</b>."),
        ("A bath fills with water, Ben takes a bath, then the water drains out. Which shape fits the water level?",
         "Up, flat, then down", ["Down, flat, then up", "Up the whole time", "Flat, up, then flat"],
         "Filling: up. Bath: flat. Draining: down. <b>Up, flat, then down</b>."),
        ("A car speeds up, drives at a steady speed, then slows to a stop. Which shape fits its speed?",
         "Up, flat, then down to 0", ["Down, flat, then up", "Up, then up faster", "Flat the whole time"],
         "Speeding up: up. Steady: flat. Stopping: down to 0. <b>Up, flat, then down to 0</b>."),
        ("A balloon is let go and rises at a steady rate. Which shape fits its height?", "A straight line going up",
         ["A straight line going down", "A flat line", "A curve going down"], "A steady rise is a straight line going up. <b>A straight line going up</b>."),
        ("A phone battery drains at a steady rate while you watch a video. Which shape fits the battery level?",
         "A straight line going down", ["A straight line going up", "A flat line", "Up, then down"],
         "A steady drain is a straight line going down: <b>a straight line going down</b>."),
    ]
    for q, ans, wr, e in stories:
        its.append(mcq(q, (ans, ans),
                       [(w, w) for w in wr], e))
    for q, ans, wr, e in [
        ("On a graph of distance over time, what does a flat part mean?", "Not moving", ["Moving fast", "Going back", "Speeding up"],
         "Distance does not change, so the person is <b>not moving</b>."),
        ("On a graph of distance from home over time, what does a part going down mean?", "Going back toward home",
         ["Moving away from home", "Not moving", "Moving faster away"], "Distance from home gets smaller: <b>going back toward home</b>."),
        ("Which part of a distance–time graph shows the fastest speed?", "The steepest part", ["The flattest part", "The highest point", "The lowest point"],
         "Steeper means more distance in the same time: <b>the steepest part</b>."),
        ("A function is increasing. What happens to y as x gets bigger?", "y gets bigger", ["y gets smaller", "y stays the same", "y becomes 0"],
         "Increasing means <b>y gets bigger</b> as x gets bigger."),
        ("A linear function has slope −2. Is it increasing or decreasing?", "Decreasing", ["Increasing", "Constant", "Neither"],
         "A negative slope means y goes down as x goes up: <b>decreasing</b>."),
        ("A linear function has slope 0. What does its graph look like?", "A horizontal line", ["A vertical line", "A line going up", "A curve"],
         "Slope 0 means y never changes: <b>a horizontal line</b>."),
        ("The height of a ball thrown up goes up, then comes down. Is height a linear function of time?", "No, it is nonlinear",
         ["Yes, it is linear", "Yes, with slope 0", "It is not a function"], "It rises then falls along a curve: <b>no, it is nonlinear</b>."),
        ("A runner keeps the same speed for the whole race. Is distance a linear function of time?", "Yes, it is linear",
         ["No, it is nonlinear", "It is constant", "It is not a function"], "The same speed means the same change each second: <b>yes, it is linear</b>."),
        ("In which interval is the function increasing: it goes from 2 to 8 between x = 0 and x = 3, then from 8 to 1 between x = 3 and x = 6?",
         "From x = 0 to x = 3", ["From x = 3 to x = 6", "From x = 0 to x = 6", "Nowhere"], "y goes up from 2 to 8 only <b>from x = 0 to x = 3</b>."),
        ("A graph of savings goes up by the same amount each week. What kind of function is it?", "Linear and increasing",
         ["Linear and decreasing", "Nonlinear and increasing", "Constant"], "The same increase each week: <b>linear and increasing</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[13], o[1], o[10], o[2], o[14], o[5], o[11], o[3], o[15], o[6], o[12], o[4], o[16], o[7], o[17], o[8],
             o[18], o[9], o[19]]
    assert len({id(i) for i in order}) == 20
    return {"title": "Describe graphs", "items": order}


def body():
    svg = grid_svg(-2, 5, ylo=-2, yhi=8, lines=[(2, 1, BLUE)], points=[(0, 1, "(0, 1)", RED), (2, 5, "(2, 5)", RED)], unit=24)
    return ("<h2>Slope-intercept form: y = mx + b</h2>"
            "<p><i>m</i> is the <b>slope</b> (rate of change). <i>b</i> is the <b>y-intercept</b> (initial value): where the line crosses the y-axis.</p>"
            "<figure class='sn-fig'>" + svg + "<figcaption>b = 1. Slope = (5 − 1) ÷ 2 = 2. So y = 2x + 1.</figcaption></figure>"
            + example("Write the equation through (2, 7) and (4, 11).", ["Slope: (11 − 7) ÷ (4 − 2) = 2.",
                      "Put in (2, 7): 7 = 2 × 2 + b, so b = 3."], "y = 2x + 3")
            + table(["Words", "m", "b", "Equation"], [["$40 to start, $12 a week", "12", "40", "y = 12x + 40"],
                                                    ["30 cm tall, burns 2 cm an hour", "−2", "30", "y = −2x + 30"]])
            + "<h2>Describe a graph</h2><p>Read from left to right: <b>increasing</b> (going up), <b>decreasing</b> (going down) "
            "or <b>constant</b> (flat). Steeper means faster change.</p>"
            + "<h2>Common mistakes</h2><ul><li>Swapping m and b: in y = 2x + 3, the slope is 2, not 3.</li>"
            "<li>Using a point's y-value as b. b is the y-value when x = 0.</li>"
            "<li>Forgetting the sign: a decrease means a negative slope.</li></ul>")


def main():
    sets = [set_graph(), set_points(), set_tables(), set_meaning(), set_story()]
    balance(sets, R)
    unit = {
        "slug": "linear-functions",
        "title": "Linear Functions: y = mx + b",
        "seo_title": "Grade 8 Linear Functions Worksheets: Write y = mx + b from Graphs, Points, Tables and Words",
        "short_title": "Linear functions",
        "domain": "Functions",
        "standard_code": "8.F.B.4",
        "standard_url": "https://www.thecorestandards.org/Math/Content/8/F/B/4/",
        "standard_text": "Construct a function to model a linear relationship between two quantities. Determine the rate of change and initial value of the function from a description of a relationship or from two (x, y) values, including reading these from a table or from a graph. Interpret the rate of change and initial value of a linear function in terms of the situation it models, and in terms of its graph or a table of values.",
        "meta_desc": "Free Grade 8 linear functions worksheets: write y = mx + b from a graph, two points, a table or a word problem, explain what the slope and initial value mean, and describe graphs as increasing, decreasing or constant. 100 questions with an answer key.",
        "key_big": "y = mx + b: m is the rate of change, b is the starting value.",
        "key_sub": "Find the slope from two points, then put one point in to find b.",
        "body_html": body(),
        "faq": [
            {"q": "How do you write the equation of a line from two points?", "a": "Find the slope m = (y₂ − y₁) ÷ (x₂ − x₁). Then put one point into y = mx + b and solve for b."},
            {"q": "What does b mean in a word problem?", "a": "b is the starting value: the amount when x = 0, such as a sign-up fee or a starting height."},
            {"q": "What does the slope mean in a word problem?", "a": "The slope is the rate of change: how much y changes for each 1 unit of x, such as dollars per hour."},
            {"q": "What is a qualitative graph?", "a": "A graph without numbers that shows how something changes: going up, going down or staying the same over time."}],
        "sets": sets, "pdf_url": "", "sort": 5, "updated": UPDATED,
    }
    write_unit("us", "math", "grade-8", unit)


if __name__ == "__main__":
    main()
