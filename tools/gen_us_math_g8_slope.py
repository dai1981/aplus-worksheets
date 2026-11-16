# -*- coding: utf-8 -*-
"""
US Grade 8 Math: Slope (8.EE.B.5, 8.EE.B.6)
  python3 tools/gen_us_math_g8_slope.py
Slope as rise over run from a graph, from two points, from a table and from y = mx + b; zero and
undefined slope; slope as the unit rate of a proportional relationship; comparing rates; and why the
slope is the same between any two points (similar triangles). Wrong answers come from real mistakes:
run over rise, a lost negative sign, subtracting in a different order on top and bottom, and reading b as m.
"""
import random
from fractions import Fraction as F
from ws_common import num, mcq, balance, B, table, example, write_unit, fig, X, MINUS, RED, BLUE, GREEN
from g8_common import lin, grid_svg, xy_table, sl

R = random.Random(80301)
UPDATED = "2026-11-16"
Y = "<i>y</i>"
UNDEF = "Undefined"


def slope_choices(m, rise, run):
    out = []
    for w in [F(run, rise) if rise else None, -m, -F(run, rise) if rise else None, F(rise), m + 1, m - 1, 2 * m]:
        if w is not None:
            out.append((sl(w), w))
    return out


def pt(x, y):
    return "(%s, %s)" % (num(x), num(y))


# ============================================================ set 1: from a graph
def set_graph():
    its = []
    for (x1, y1), (x2, y2) in [((0, 1), (2, 5)), ((-2, -1), (1, 5)), ((0, 4), (3, -2)), ((-3, 0), (3, 2)), ((1, -4), (3, 4)),
                               ((-4, 3), (2, 0)), ((0, -3), (4, 0)), ((-2, 5), (2, -3)), ((-5, -2), (5, 2)), ((1, 1), (4, 3)),
                               ((-3, 4), (1, 4)), ((-1, -5), (1, 5)), ((-4, -4), (2, -1)), ((0, 2), (5, -2)), ((-2, -3), (2, -1)),
                               ((-1, 6), (2, -3)), ((-6, 1), (3, 4)), ((2, -5), (5, 1)), ((-3, -6), (0, 3)), ((-5, 5), (5, 1))]:
        rise, run = y2 - y1, x2 - x1
        m = F(rise, run)
        b = y1 - m * x1
        svg = grid_svg(-6, 6, lines=[(m, b, BLUE)], points=[(x1, y1, pt(x1, y1), RED), (x2, y2, pt(x2, y2), RED)], unit=20)
        if m == 0:
            e = "The line is flat. The rise is 0, so the slope is <b>0</b>."
        else:
            e = ("From %s to %s: rise = %s, run = %s. Slope = rise ÷ run = %s ÷ %s = <b>%s</b>."
                 % (pt(x1, y1), pt(x2, y2), num(rise), num(run), num(rise), num(run), sl(m)))
            if m < 0:
                e += " The line goes down from left to right, so the slope is negative."
        cands = slope_choices(m, rise, run) + [(UNDEF, "u")]
        its.append(mcq(fig(svg) + "What is the slope of the line?", (sl(m), m), cands, e))
    return {"title": "Slope from a graph", "items": its}


# ============================================================ set 2: two points
def set_points():
    its = []
    for (x1, y1), (x2, y2) in [((1, 2), (3, 8)), ((2, 5), (6, 7)), ((-1, 4), (2, -2)), ((0, -3), (5, 7)), ((3, 1), (7, -1)),
                               ((-4, -2), (-1, 7)), ((2, 3), (8, 3)), ((5, -2), (5, 6)), ((-6, 1), (2, 5)), ((4, 9), (1, 3)),
                               ((-2, -7), (3, 3)), ((0, 0), (6, -4)), ((-5, 8), (-2, -1)), ((7, 2), (-1, 6)), ((-3, -3), (-3, 4)),
                               ((1, -6), (9, -2)), ((10, 4), (-5, 1)), ((-8, 3), (4, -6)), ((2, -1), (-4, -1)), ((6, 11), (2, -1))]:
        rise, run = y2 - y1, x2 - x1
        q = "What is the slope of the line through %s and %s?" % (B(pt(x1, y1)), B(pt(x2, y2)))
        if run == 0:
            e = "The x-values are the same, so the run is 0. You cannot divide by 0: the line is vertical and the slope is <b>undefined</b>."
            its.append(mcq(q, (UNDEF, "u"), [("0", F(0)), (num(rise), F(rise)), (sl(F(-rise)), F(-rise))], e))
            continue
        m = F(rise, run)
        if m == 0:
            e = "The y-values are the same, so the rise is 0. The line is horizontal and the slope is <b>0</b>."
            its.append(mcq(q, ("0", F(0)), [(UNDEF, "u"), (num(run), F(run)), ("1", F(1))], e))
            continue
        e = ("Slope = (y₂ − y₁) ÷ (x₂ − x₁) = (%s − %s) ÷ (%s − %s) = %s ÷ %s = <b>%s</b>."
             % (num(y2), "(%s)" % num(y1) if y1 < 0 else num(y1), num(x2), "(%s)" % num(x1) if x1 < 0 else num(x1),
                num(rise), num(run), sl(m)))
        mixed = F(y2 - y1, x1 - x2)
        cands = [(sl(mixed), mixed)] + slope_choices(m, rise, run)
        its.append(mcq(q, (sl(m), m), cands, e))
    return {"title": "Slope from two points", "items": its}


# ============================================================ set 3: tables and equations
def set_table_eq():
    its = []
    for x0, dx, y0, dy in [(0, 1, 3, 2), (1, 1, 10, -3), (0, 2, -4, 5), (2, 2, 1, 4), (-2, 3, 7, -6), (0, 5, 0, 2),
                           (1, 2, -3, -1), (-4, 4, 2, 6), (3, 1, 5, 0), (0, 3, 8, -2)]:
        xs = [x0 + k * dx for k in range(4)]
        ys = [y0 + k * dy for k in range(4)]
        m = F(dy, dx)
        tbl = xy_table([num(v) for v in xs], [num(v) for v in ys])
        e = "Each time x goes up by %s, y changes by %s. Slope = %s ÷ %s = <b>%s</b>." % (num(dx), num(dy), num(dy), num(dx), sl(m))
        cands = slope_choices(m, dy, dx) + [(num(ys[0]), F(ys[0])), (num(dy), F(dy))]
        its.append(mcq(tbl + "The table shows points on a line. What is the slope?", (sl(m), m), cands, e))
    for m, b in [(3, 2), (-2, 5), (F(1, 2), -4), (-1, 0), (F(-3, 4), 6), (4, -7), (0, 3), (F(2, 3), 1), (-5, -2), (1, 9)]:
        eq_txt = "%s = %s" % (Y, lin(m, b))
        if b != 0 and len(its) % 2 == 0:
            q = "What is the slope of %s?" % B(eq_txt)
            ans = (sl(m), F(m))
            cands = [(num(b), F(b)), (sl(-F(m)), -F(m)), (sl(1 / F(m)) if m else "1", 1 / F(m) if m else F(1)), (sl(F(m) + b), F(m) + b),
                     (UNDEF, "u"), (sl(F(m) + 1), F(m) + 1)]
            e = "In %s = <i>m</i>%s + <i>b</i>, the number in front of %s is the slope. Slope = <b>%s</b>." % (Y, X, X, sl(m))
            if m == 0:
                e = "There is no %s-term: %s = 0%s + %s. The slope is <b>0</b>." % (X, Y, X, num(b))
        else:
            q = "What is the y-intercept of %s?" % B(eq_txt)
            ans = (num(b), F(b))
            cands = [(sl(m), F(m)), (num(-b), F(-b)), (sl(F(-b, 1) / m) if m else "1", F(-b) / m if m else F(1)), (num(b + 1), F(b + 1)),
                     (num(b - 1), F(b - 1)), (num(b + 2), F(b + 2))]
            e = "In %s = <i>m</i>%s + <i>b</i>, <i>b</i> is the y-intercept: the line crosses the y-axis at <b>%s</b>." % (Y, X, num(b))
        its.append(mcq(q, ans, cands, e))
    o = its
    order = [o[10], o[0], o[11], o[1], o[12], o[2], o[13], o[3], o[14], o[4], o[15], o[5], o[16], o[6], o[17], o[7],
             o[18], o[8], o[19], o[9]]
    return {"title": "Slope from tables and equations", "items": order}


# ============================================================ set 4: proportional relationships
def set_prop():
    its = []
    for k, what, unit in [(3, "A printer prints pages", "pages per minute"), (F(5, 2), "Water fills a tank", "gallons per minute"),
                          (40, "A car travels", "miles per hour"), (F(3, 4), "A recipe uses cups of flour per batch", "cups per batch"),
                          (12, "A worker earns dollars", "dollars per hour"), (F(1, 2), "A snail moves feet", "feet per minute")]:
        xs = [1, 2, 4]
        pts = [(x, k * x) for x in xs]
        tbl = xy_table([num(x) for x in [0] + xs], [num(F(k) * x, "f" if F(k).denominator > 1 else "d") for x in [0] + xs])
        q = tbl + "%s. The table is a proportional relationship. What is the slope (the unit rate)?" % what
        e = "The line goes through (0, 0). Slope = y ÷ x = %s ÷ 1 = <b>%s</b> %s." % (sl(k), sl(k), unit)
        its.append(mcq(q, (sl(k), F(k)), [(sl(1 / F(k)), 1 / F(k)), (sl(2 * F(k)), 2 * F(k)), (sl(F(k) + 1), F(k) + 1),
                                           (sl(4 * F(k)), 4 * F(k))], e))
    for (k1, lab1), (k2, lab2), ask in [((3, "Pump A: graph through (2, 6)"), (F(5, 2), "Pump B: y = 2.5x"), "faster"),
                                        ((F(15, 2), "Runner A: 15 meters in 2 seconds"), (8, "Runner B: y = 8x"), "faster"),
                                        ((12, "Store A: 3 pounds for $36"), (11, "Store B: y = 11x"), "cheaper per pound"),
                                        ((F(9, 2), "Car A: 9 miles in 2 minutes"), (5, "Car B: y = 5x"), "slower"),
                                        ((F(4, 3), "Plan A: 4 GB for $3"), (F(3, 2), "Plan B: y = 1.5x"), "more GB per dollar")]:
        if ask in ("faster", "more GB per dollar"):
            win = "A" if k1 > k2 else "B"
        else:
            win = "A" if k1 < k2 else "B"
        q = "%s. %s. Which has the %s rate? (%s)" % (lab1, lab2, "greater" if ask in ("faster", "more GB per dollar") else "smaller", ask)
        e = "Compare the slopes: A is %s, B is %s. So the answer is <b>%s</b>." % (num(F(k1)), num(F(k2)), win)
        ans = win
        ch = ["A", "B", "They are the same", "We cannot tell"]
        its.append(mcq(q, (ans, ans), [(c, c) for c in ch if c != ans], e))
    for m in [2, F(1, 3), 5, F(3, 2)]:
        svg = grid_svg(0, 6, ylo=0, yhi=12 if m * 6 <= 12 else int(m * 6) + 1, lines=[(m, 0, BLUE)], unit=18, tick_every=2,
                       points=[(x, m * x, "", RED) for x in range(0, 7) if (m * x).denominator == 1])
        q = fig(svg) + "The graph shows a proportional relationship. What is the unit rate?"
        d = F(m).denominator
        e = ("Find a point with whole numbers, like (%d, %s). Unit rate = slope = %s ÷ %d = <b>%s</b>." % (
            d, num(m * d), num(m * d), d, sl(m))) if d > 1 else \
            "Find the point (1, %s). Unit rate = slope = %s ÷ 1 = <b>%s</b>." % (num(m), num(m), sl(m))
        its.append(mcq(q, (sl(m), F(m)), [(sl(1 / F(m)), 1 / F(m)), (sl(2 * F(m)), 2 * F(m)), (sl(F(m) + 1), F(m) + 1),
                                          (num(6 * F(m)), 6 * F(m))], e))
    for q, ans, wr, e in [
        ("Which equation shows a proportional relationship?", "y = 4x", ["y = 4x + 1", "y = x + 4", "y = 4"],
         "A proportional relationship goes through (0, 0): y = kx with no + b. The answer is <b>y = 4x</b>."),
        ("A line goes through (0, 0) and (5, 20). Which is true?", "It is proportional with unit rate 4", ["It is proportional with unit rate 5",
         "It is not proportional", "The unit rate is 1/4"], "It goes through the origin and slope = 20 ÷ 5 = 4. <b>It is proportional with unit rate 4</b>."),
        ("In y = 7x, what does 7 mean if x is hours and y is dollars?", "$7 per hour", ["7 hours per dollar", "$7 in all", "Start with $7"],
         "The slope is the unit rate: <b>$7 per hour</b>."),
        ("A line through the origin has slope 3/2. Which point is on it?", "(4, 6)", ["(6, 4)", "(3, 2)", "(2, 4)"],
         "y = 3/2 x. When x = 4, y = 6. The point is <b>(4, 6)</b>."),
        ("Pay is $15 per hour. Which equation is right?", "y = 15x", ["x = 15y", "y = x + 15", "y = 15"],
         "Dollars = 15 × hours: <b>y = 15x</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[15], o[1], o[11], o[16], o[2], o[6], o[17], o[3], o[12], o[18], o[4], o[7], o[19], o[5], o[8],
             o[13], o[9], o[14], o[10]]
    assert len({id(i) for i in order}) == 20
    return {"title": "Slope as a unit rate", "items": order}


# ============================================================ set 5: understanding slope
def set_ideas():
    its = []
    for q, ans, wr, e in [
        ("A line goes up from left to right. What sign is its slope?", "Positive", ["Negative", "Zero", "Undefined"],
         "Going up from left to right means a <b>positive</b> slope."),
        ("A line goes down from left to right. What sign is its slope?", "Negative", ["Positive", "Zero", "Undefined"],
         "Going down from left to right means a <b>negative</b> slope."),
        ("What is the slope of a horizontal line?", "0", ["Undefined", "1", "−1"], "A horizontal line has no rise: slope <b>0</b>."),
        ("What is the slope of a vertical line?", UNDEF, ["0", "1", "Infinity is 1"],
         "A vertical line has no run, and you cannot divide by 0: the slope is <b>undefined</b>."),
        ("Which line is steeper: slope 3 or slope 1/2?", "Slope 3", ["Slope 1/2", "They are the same", "We cannot tell"],
         "A bigger slope (ignoring the sign) is steeper. <b>Slope 3</b> is steeper."),
        ("Which line is steeper: slope −4 or slope 2?", "Slope −4", ["Slope 2", "They are the same", "We cannot tell"],
         "Compare the sizes: 4 is bigger than 2, so <b>slope −4</b> is steeper (it goes down)."),
        ("Two right triangles are drawn under the same line. One has rise 2 and run 3. The other has run 9. What is its rise?",
         "6", ["8", "5", "3"], "The triangles are similar, so rise ÷ run is the same: 2/3 = 6/9. The rise is <b>6</b>."),
        ("Why is the slope the same between any two points on a line?", "The slope triangles are similar",
         ["The points are always 1 apart", "Lines are always steep", "The y-intercept is 0"],
         "Any two slope triangles on the same line have the same angles. <b>The slope triangles are similar</b>, so rise ÷ run is equal."),
        ("A line has slope 2/5. If you go right 10, how far up do you go?", "4", ["25", "2", "5"],
         "Rise = slope × run = 2/5 × 10 = <b>4</b>."),
        ("A line has slope −3. If you go right 2, what happens to y?", "It goes down 6", ["It goes up 6", "It goes down 3/2", "It goes up 3"],
         "Change in y = −3 × 2 = −6. <b>It goes down 6</b>."),
        ("A hill rises 30 feet over a run of 150 feet. What is its slope?", "1/5", ["5", "30", "1/30"],
         "Slope = 30 ÷ 150 = <b>1/5</b>."),
        ("A ramp rises 2 feet over 24 feet. What is its slope?", "1/12", ["12", "2/12 = 6", "1/2"],
         "Slope = 2 ÷ 24 = <b>1/12</b>."),
        ("A plane goes down 3,000 feet over 15 miles of distance. What is the rate of change?", "−200 feet per mile",
         ["200 feet per mile", "−5 miles per foot", "−3,000 feet"], "Change ÷ distance = −3,000 ÷ 15 = <b>−200 feet per mile</b>."),
        ("The temperature goes from 50°F at 1 p.m. to 62°F at 4 p.m. What is the rate of change?", "4°F per hour",
         ["12°F per hour", "3°F per hour", "−4°F per hour"], "(62 − 50) ÷ (4 − 1) = 12 ÷ 3 = <b>4°F per hour</b>."),
        ("A line goes through (2, 5) with slope 3. Which point is also on the line?", "(3, 8)", ["(3, 6)", "(5, 8)", "(1, 8)"],
         "Go right 1 and up 3: (2 + 1, 5 + 3) = <b>(3, 8)</b>."),
        ("A line goes through (0, 4) with slope −1/2. Which point is also on the line?", "(2, 3)", ["(2, 5)", "(1, 2)", "(−2, 3)"],
         "Go right 2 and down 1: (0 + 2, 4 − 1) = <b>(2, 3)</b>."),
        ("Two lines are parallel. One has slope 5/3. What is the slope of the other?", "5/3", ["3/5", "−5/3", "−3/5"],
         "Parallel lines have the <b>same slope</b>: 5/3."),
        ("Which pair of points gives a slope of 1?", "(2, 3) and (5, 6)", ["(2, 3) and (6, 5)", "(1, 1) and (1, 4)", "(0, 2) and (2, 0)"],
         "(6 − 3) ÷ (5 − 2) = 3 ÷ 3 = 1. The answer is <b>(2, 3) and (5, 6)</b>."),
        ("Ana says the slope through (1, 2) and (4, 8) is 3/6. What did she do wrong?", "She divided run by rise",
         ["She added the numbers", "She used the y-intercept", "Nothing, she is right"],
         "Rise = 6 and run = 3, so the slope is 6/3 = 2. <b>She divided run by rise</b>."),
        ("Ben finds the slope through (1, 7) and (3, 3) as (3 − 7) ÷ (1 − 3) = 2. What is the correct slope?", "−2", ["2", "−1/2", "4"],
         "Subtract in the same order: (3 − 7) ÷ (3 − 1) = −4 ÷ 2 = <b>−2</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    return {"title": "Understanding slope", "items": its}


def body():
    svg = grid_svg(-1, 6, ylo=-1, yhi=6, lines=[(F(2, 3), 1, BLUE)], points=[(0, 1, "(0, 1)", RED), (3, 3, "(3, 3)", RED)],
                   segs=[(0, 1, 3, 1, GREEN), (3, 1, 3, 3, GREEN)], unit=30)
    return ("<h2>Slope is rise over run</h2>"
            "<p>Slope tells how steep a line is. Pick two points. Count how far up (<b>rise</b>) and how far right (<b>run</b>).</p>"
            "<figure class='sn-fig'>" + svg + "<figcaption>Rise 2, run 3: slope = 2/3.</figcaption></figure>"
            "<p>With two points: slope = (y₂ − y₁) ÷ (x₂ − x₁).</p>"
            + table(["Line", "Slope"], [["Goes up (left to right)", "positive"], ["Goes down", "negative"],
                                        ["Horizontal", "0"], ["Vertical", "undefined"]])
            + example("Find the slope through (2, 1) and (5, 10).", ["Rise: 10 − 1 = 9.", "Run: 5 − 2 = 3.", "Slope = 9 ÷ 3 = 3."], "3")
            + "<h2>Slope in y = mx + b</h2><p><i>m</i> is the slope and <i>b</i> is the y-intercept. "
            "In a proportional relationship y = kx, the slope k is the <b>unit rate</b>.</p>"
            + "<h2>Common mistakes</h2><ul><li>Run over rise: slope is up ÷ right, not right ÷ up.</li>"
            "<li>Mixing the order: subtract the same point first on top and bottom.</li>"
            "<li>Losing the sign: a line going down has a negative slope.</li>"
            "<li>Reading b as the slope in y = mx + b.</li></ul>")


def main():
    sets = [set_graph(), set_points(), set_table_eq(), set_prop(), set_ideas()]
    balance(sets, R)
    unit = {
        "slug": "slope",
        "title": "Slope: Rise Over Run",
        "seo_title": "Grade 8 Slope Worksheets: Rise Over Run, Two Points, Tables, y = mx + b and Unit Rate",
        "short_title": "Slope",
        "domain": "Expressions & Equations",
        "standard_code": "8.EE.B.6",
        "standard_url": "https://www.thecorestandards.org/Math/Content/8/EE/B/6/",
        "standard_text": "Use similar triangles to explain why the slope m is the same between any two distinct points on a non-vertical line in the coordinate plane; derive the equation y = mx for a line through the origin and the equation y = mx + b for a line intercepting the vertical axis at b.",
        "meta_desc": "Free Grade 8 slope worksheets: find slope from a graph, from two points, from a table and from y = mx + b, learn zero and undefined slope, use slope as a unit rate, and compare rates. 100 questions with an answer key.",
        "key_big": "Slope = rise ÷ run = (y₂ − y₁) ÷ (x₂ − x₁).",
        "key_sub": "Up is positive, down is negative, flat is 0, vertical is undefined. In y = mx + b, m is the slope.",
        "body_html": body(),
        "faq": [
            {"q": "How do you find the slope of a line?", "a": "Pick two points on the line. Slope = rise ÷ run = (y₂ − y₁) ÷ (x₂ − x₁). For (1, 2) and (4, 8), the slope is 6 ÷ 3 = 2."},
            {"q": "What does a negative slope mean?", "a": "The line goes down from left to right. As x gets bigger, y gets smaller."},
            {"q": "What is the slope of a horizontal or vertical line?", "a": "A horizontal line has slope 0. A vertical line has an undefined slope because the run is 0."},
            {"q": "How is slope related to unit rate?", "a": "In a proportional relationship y = kx, the slope k is the unit rate, such as miles per hour or dollars per pound."}],
        "sets": sets, "pdf_url": "", "sort": 3, "updated": UPDATED,
    }
    write_unit("us", "math", "grade-8", unit)


if __name__ == "__main__":
    main()
