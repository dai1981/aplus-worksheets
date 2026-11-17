# -*- coding: utf-8 -*-
"""
US Algebra 1: Forms of Linear Equations (Common Core A-CED.A.2, F-LE.A.2, F-IF.C.8)
  python3 tools/gen_us_math_a1_forms_of_linear_equations.py
Point-slope form, slope-intercept form from a point and a slope or from two points, standard form and
intercepts, parallel and perpendicular lines, and linear models from real data.
Wrong answers come from real mistakes: sign errors in y − y₁ = m(x − x₁), using the y-intercept of a different
point, forgetting to distribute in point-slope form, taking the same slope (not the negative reciprocal) for a
perpendicular line, and mixing up the x- and y-intercepts.
"""
import random
from fractions import Fraction as F
from math import gcd
from us_hs import num, B, S, make, lesson, collect, T, expr, fr, MINUS

R = random.Random(90701)
X, Y = "<i>x</i>", "<i>y</i>"


def sf(v):
    v = F(v)
    if v.denominator == 1:
        return num(v)
    s = fr(abs(v.numerator), v.denominator)
    return (MINUS + s) if v < 0 else s


def si(m, b):
    """y = mx + b with fraction slopes."""
    m, b = F(m), F(b)
    if m == 0:
        return "%s = %s" % (Y, sf(b))
    t = X if m == 1 else (MINUS + X if m == -1 else sf(m) + X)
    if b == 0:
        return "%s = %s" % (Y, t)
    return "%s = %s %s %s" % (Y, t, "+" if b > 0 else MINUS, sf(abs(b)))


def ps(m, x1, y1):
    xs = "(%s %s %s)" % (X, MINUS if x1 >= 0 else "+", num(abs(x1))) if x1 else X
    ys = "%s %s %s" % (Y, MINUS if y1 >= 0 else "+", num(abs(y1))) if y1 else Y
    mm = "" if m == 1 else (MINUS if m == -1 else sf(m))
    return "%s = %s%s" % (ys, mm, xs)


def pt(x, y):
    return "(%s, %s)" % (num(x), num(y))


def uniq(right, wr):
    out = [w for w in dict.fromkeys(wr) if w != right]
    return out if len(out) >= 3 else None


# ------------------------------------------------------------ set 1: point-slope form
def one_ps(r):
    m = r.choice([2, 3, -2, -4, 5, F(1, 2), F(-2, 3), F(3, 4), -1])
    x1, y1 = r.randint(-6, 6), r.randint(-6, 6)
    if x1 == 0 or y1 == 0:
        return None
    q = "Write an equation in point-slope form for the line through %s with slope %s." % (B(pt(x1, y1)), B(sf(m)))
    right = ps(m, x1, y1)
    wr = uniq(right, [ps(m, -x1, -y1), ps(m, y1, x1), ps(-m, x1, y1)])
    if not wr:
        return None
    e = "Point-slope form is <i>y</i> − <i>y</i><sub>1</sub> = <i>m</i>(<i>x</i> − <i>x</i><sub>1</sub>). Put in <i>m</i> = %s, <i>x</i><sub>1</sub> = %s and <i>y</i><sub>1</sub> = %s: <b>%s</b>." % (
        sf(m), num(x1), num(y1), right)
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 2: slope-intercept from a point or two points
def one_si(r):
    if r.random() < 0.5:
        m = r.choice([2, 3, -2, -3, 4, F(1, 2), F(-1, 3), -1])
        x1 = r.choice([-4, -3, -2, 2, 3, 4, 6])
        b = F(r.randint(-8, 8))
        if (m * x1).denominator != 1:
            return None
        y1 = m * x1 + b
        q = "Write the equation in slope-intercept form of the line through %s with slope %s." % (B(pt(x1, y1)), B(sf(m)))
        right = si(m, b)
        wr = uniq(right, [si(m, y1), si(m, y1 + m * x1), si(m, b + 2 * m * x1) if m * x1 else si(m, -b)])
        e = "Substitute the point into <i>y</i> = <i>mx</i> + <i>b</i>: %s = %s(%s) + <i>b</i>, so <i>b</i> = %s. <b>%s</b>." % (num(y1), sf(m), num(x1), sf(b), right)
    else:
        x1, x2 = r.sample(range(-5, 7), 2)
        m = r.choice([1, 2, 3, -1, -2, F(1, 2), F(-3, 2)])
        b = F(r.randint(-6, 6))
        if ((m * x1).denominator != 1) or ((m * x2).denominator != 1):
            return None
        y1, y2 = m * x1 + b, m * x2 + b
        q = "Write the equation of the line through %s and %s in slope-intercept form." % (B(pt(x1, y1)), B(pt(x2, y2)))
        right = si(m, b)
        m_bad = F(x2 - x1, y2 - y1) if y2 != y1 else m + 1
        wr = uniq(right, [si(m_bad, y1 - m_bad * x1), si(m, y1), si(-m, y1 + m * x1)])
        e = "Slope = (%s − %s) ÷ (%s − %s) = %s. Then %s = %s(%s) + <i>b</i>, so <i>b</i> = %s. <b>%s</b>." % (
            num(y2), "(%s)" % num(y1) if y1 < 0 else num(y1), num(x2), "(%s)" % num(x1) if x1 < 0 else num(x1), sf(m), num(y1), sf(m), num(x1), sf(b), right)
    if not wr:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 3: standard form and intercepts
def std(a, b, c):
    return "%s = %s" % (expr([(a, X), (b, Y)]), num(c))


def one_std(r):
    kind = r.choice(["int", "int", "to_std", "to_si"])
    if kind == "int":
        a, b = r.choice([2, 3, 4, 5, 6, -2, -3]), r.choice([2, 3, 4, 5, -2, -4])
        L = abs(a * b) // gcd(abs(a), abs(b))
        c = L * r.choice([1, 2, -1, 2, 3])
        q = "Find the <i>x</i>- and <i>y</i>-intercepts of %s." % B(std(a, b, c))
        xi, yi = F(c, a), F(c, b)
        right = "<i>x</i>-intercept %s, <i>y</i>-intercept %s" % (sf(xi), sf(yi))
        wr = uniq(right, ["<i>x</i>-intercept %s, <i>y</i>-intercept %s" % (sf(yi), sf(xi)), "<i>x</i>-intercept %s, <i>y</i>-intercept %s" % (sf(c * a), sf(c * b)),
                          "<i>x</i>-intercept %s, <i>y</i>-intercept %s" % (sf(-xi), sf(-yi))])
        e = "Let <i>y</i> = 0: %s<i>x</i> = %s, so <i>x</i> = %s. Let <i>x</i> = 0: %s<i>y</i> = %s, so <i>y</i> = %s. <b>%s</b>." % (num(a), num(c), sf(xi), num(b), num(c), sf(yi), right)
    elif kind == "to_si":
        a, b = r.choice([2, 3, 4, 6, -2]), r.choice([2, 3, -2, -3, 4])
        c = r.choice([6, 12, -6, 8, 24, -12])
        q = "Write %s in slope-intercept form." % B(std(a, b, c))
        m, k = F(-a, b), F(c, b)
        right = si(m, k)
        wr = uniq(right, [si(-m, k), si(m, c), si(F(-b, a), k)])
        e = "%s both sides, then divide every term by %s: <b>%s</b>." % (("Subtract %s from" if a > 0 else "Add %s to") % expr([(abs(a), X)]), num(b), right)
    else:
        m = r.choice([F(2, 3), F(-3, 4), F(1, 2), F(-5, 2), 3, -2, F(4, 5)])
        b = r.randint(-6, 6)
        if b == 0:
            return None
        d = m.denominator
        A, Bc, C = -m.numerator, d, b * d
        if A < 0:
            A, Bc, C = -A, -Bc, -C
        q = "Write %s in standard form <i>Ax</i> + <i>By</i> = <i>C</i> with integer coefficients and <i>A</i> &gt; 0." % B(si(m, b))
        right = std(A, Bc, C)
        wr = uniq(right, [std(A, -Bc, C), std(A, Bc, -C), std(m.numerator if m.numerator > 0 else -m.numerator, Bc, b)])
        e = "Multiply every term by %d to clear the fraction, move the <i>x</i>-term to the left and make the <i>x</i>-coefficient positive: <b>%s</b>." % (d, right) if d > 1 else \
            "Move the <i>x</i>-term to the left side and make the <i>x</i>-coefficient positive: <b>%s</b>." % right
    if not wr:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 4: parallel and perpendicular
def one_pp(r):
    m = F(r.choice([2, 3, -2, F(1, 2), F(-2, 3), F(3, 4), -4, F(5, 2)]))
    b = r.randint(-6, 6)
    line = B(si(m, b))
    kind = r.choice(["slope_par", "slope_perp", "eq_par", "eq_perp"])
    neg = -1 / m
    if kind == "slope_par":
        return T("What is the slope of a line parallel to %s?" % line, sf(m), [w for w in dict.fromkeys([sf(neg), sf(-m), sf(1 / m)]) if w != sf(m)][:3],
                 "Parallel lines have <b>the same slope</b>: %s." % sf(m))
    if kind == "slope_perp":
        wr = [w for w in dict.fromkeys([sf(m), sf(-m), sf(1 / m)]) if w != sf(neg)]
        return T("What is the slope of a line perpendicular to %s?" % line, sf(neg), wr[:3],
                 "Perpendicular slopes are <b>negative reciprocals</b>: flip %s and change the sign to get <b>%s</b>." % (sf(m), sf(neg)))
    x1 = r.choice([-4, -3, -2, 2, 3, 4, 6])
    mm = m if kind == "eq_par" else neg
    y1 = r.randint(-6, 6)
    bb = F(y1) - mm * x1
    if bb.denominator > 2:
        return None
    q = "Write the equation of the line %s to %s that passes through %s." % ("parallel" if kind == "eq_par" else "perpendicular", line, B(pt(x1, y1)))
    right = si(mm, bb)
    other = neg if kind == "eq_par" else m
    wr = uniq(right, [si(mm, b), si(other, F(y1) - other * x1), si(mm, F(y1) + mm * x1)])
    if not wr:
        return None
    e = "The slope is %s (%s). Then %s = %s(%s) + <i>b</i>, so <i>b</i> = %s: <b>%s</b>." % (
        sf(mm), "same slope" if kind == "eq_par" else "negative reciprocal of %s" % sf(m), num(y1), sf(mm), num(x1), sf(bb), right)
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 5: linear models
def problems():
    data = [
        ("A plumber charges $85 for a 1-hour job and $145 for a 3-hour job. Which equation gives the cost <i>C</i> for <i>h</i> hours?", "<i>C</i> = 30<i>h</i> + 55",
         ["<i>C</i> = 60<i>h</i> + 25", "<i>C</i> = 30<i>h</i> + 85", "<i>C</i> = 85<i>h</i>"], "Slope = (145 − 85) ÷ (3 − 1) = 30. Then 85 = 30(1) + <i>b</i>, so <i>b</i> = 55: <b><i>C</i> = 30<i>h</i> + 55</b>."),
        ("A candle is 24 cm tall after 2 hours and 15 cm tall after 5 hours. Which equation gives its height <i>h</i> after <i>t</i> hours?", "<i>h</i> = −3<i>t</i> + 30",
         ["<i>h</i> = 3<i>t</i> + 18", "<i>h</i> = −3<i>t</i> + 24", "<i>h</i> = −9<i>t</i> + 42"], "Slope = (15 − 24) ÷ (5 − 2) = −3. 24 = −3(2) + <i>b</i>, so <i>b</i> = 30."),
        ("In the candle model <i>h</i> = −3<i>t</i> + 30, what does 30 mean?", "The candle was 30 cm tall at the start", ["It burns 30 cm an hour", "It burns out after 30 hours", "It is 30 cm after 3 hours"], "The <i>y</i>-intercept is the value when <i>t</i> = 0: <b>the starting height</b>."),
        ("A taxi ride costs $3.50 plus $2.25 per mile. Which equation in slope-intercept form gives the cost <i>C</i> for <i>m</i> miles?", "<i>C</i> = 2.25<i>m</i> + 3.50", ["<i>C</i> = 3.50<i>m</i> + 2.25", "<i>C</i> = 5.75<i>m</i>", "<i>C</i> = 2.25 + <i>m</i>"],
         "The rate per mile is the slope and the starting fee is the <i>y</i>-intercept: <b><i>C</i> = 2.25<i>m</i> + 3.50</b>."),
        ("Adult tickets cost $8 and child tickets cost $5. A school spends $400. Which standard-form equation models this?", "8<i>a</i> + 5<i>c</i> = 400", ["5<i>a</i> + 8<i>c</i> = 400", "8<i>a</i> − 5<i>c</i> = 400", "13(<i>a</i> + <i>c</i>) = 400"],
         "Cost of adults plus cost of children equals the total: <b>8<i>a</i> + 5<i>c</i> = 400</b>."),
        ("For 8<i>a</i> + 5<i>c</i> = 400, what does the <i>a</i>-intercept 50 mean?", "The school can buy 50 adult tickets and no child tickets", ["Each adult ticket costs $50", "50 child tickets cost $400", "There are 50 people"],
         "The <i>a</i>-intercept is where <i>c</i> = 0: <b>50 adult tickets and no child tickets</b>."),
        ("A gym had 120 members in month 1 and 180 members in month 4. Write a point-slope equation using the point (1, 120).", "<i>y</i> − 120 = 20(<i>x</i> − 1)",
         ["<i>y</i> − 1 = 20(<i>x</i> − 120)", "<i>y</i> − 120 = 60(<i>x</i> − 1)", "<i>y</i> + 120 = 20(<i>x</i> + 1)"], "Slope = 60 ÷ 3 = 20: <b><i>y</i> − 120 = 20(<i>x</i> − 1)</b>."),
        ("Which line is parallel to <i>y</i> = 4<i>x</i> − 7?", "<i>y</i> = 4<i>x</i> + 2", ["<i>y</i> = −4<i>x</i> − 7", "<i>y</i> = −¼<i>x</i> + 2", "<i>y</i> = 7<i>x</i> − 4"], "Same slope (4), different intercept: <b><i>y</i> = 4<i>x</i> + 2</b>."),
        ("Which line is perpendicular to <i>y</i> = 2<i>x</i> + 1?", "<i>y</i> = −½<i>x</i> + 3", ["<i>y</i> = 2<i>x</i> − 1", "<i>y</i> = −2<i>x</i> + 1", "<i>y</i> = ½<i>x</i> + 3"], "The negative reciprocal of 2 is −½: <b><i>y</i> = −½<i>x</i> + 3</b>."),
        ("What is the slope of the line 3<i>x</i> + 4<i>y</i> = 12?", "−" + fr(3, 4), [fr(3, 4), fr(4, 3), "3"], "4<i>y</i> = −3<i>x</i> + 12, so <i>y</i> = −¾<i>x</i> + 3. The slope is <b>−¾</b>."),
        ("Which equation is in standard form?", "2<i>x</i> − 5<i>y</i> = 10", ["<i>y</i> = 3<i>x</i> + 1", "<i>y</i> − 2 = 4(<i>x</i> + 1)", "<i>x</i> = 2<i>y</i> + 6"], "Standard form is <i>Ax</i> + <i>By</i> = <i>C</i>: <b>2<i>x</i> − 5<i>y</i> = 10</b>."),
        ("A line has point-slope equation <i>y</i> + 3 = 2(<i>x</i> − 5). Which point is on the line?", "(5, −3)", ["(−5, 3)", "(5, 3)", "(3, 5)"], "<i>y</i> − <i>y</i><sub>1</sub> = <i>m</i>(<i>x</i> − <i>x</i><sub>1</sub>) with <i>y</i> + 3 = <i>y</i> − (−3): the point is <b>(5, −3)</b>."),
        ("Write <i>y</i> + 3 = 2(<i>x</i> − 5) in slope-intercept form.", "<i>y</i> = 2<i>x</i> − 13", ["<i>y</i> = 2<i>x</i> − 7", "<i>y</i> = 2<i>x</i> − 8", "<i>y</i> = 2<i>x</i> + 13"], "Distribute: <i>y</i> + 3 = 2<i>x</i> − 10, then subtract 3: <b><i>y</i> = 2<i>x</i> − 13</b>."),
        ("A water tank holds 500 gallons and drains at 20 gallons per minute. Which equation gives the water <i>W</i> after <i>t</i> minutes?", "<i>W</i> = −20<i>t</i> + 500", ["<i>W</i> = 20<i>t</i> + 500", "<i>W</i> = −500<i>t</i> + 20", "<i>W</i> = 500 − <i>t</i>"],
         "Start at 500 and lose 20 each minute: <b><i>W</i> = −20<i>t</i> + 500</b>."),
        ("When does the tank above (<i>W</i> = −20<i>t</i> + 500) become empty?", "After 25 minutes", ["After 20 minutes", "After 500 minutes", "After 480 minutes"], "0 = −20<i>t</i> + 500, so <i>t</i> = <b>25</b>."),
        ("Lines with slopes " + fr(2, 3) + " and −" + fr(3, 2) + " are…", "Perpendicular", ["Parallel", "The same line", "Neither"], fr(2, 3) + " × (−" + fr(3, 2) + ") = −1, so they are <b>perpendicular</b>."),
        ("Are <i>y</i> = 3<i>x</i> + 2 and 6<i>x</i> − 2<i>y</i> = 8 parallel?", "Yes, both have slope 3", ["No, the slopes are 3 and 6", "No, they are perpendicular", "No, they have the same intercept"], "6<i>x</i> − 2<i>y</i> = 8 gives <i>y</i> = 3<i>x</i> − 4. Both have slope 3: <b>parallel</b>."),
        ("A phone costs $40 a month on a plan, and the total after 6 months is $330. Which equation gives the total <i>T</i> after <i>m</i> months?", "<i>T</i> = 40<i>m</i> + 90", ["<i>T</i> = 40<i>m</i> + 330", "<i>T</i> = 55<i>m</i>", "<i>T</i> = 90<i>m</i> + 40"],
         "330 = 40(6) + <i>b</i>, so <i>b</i> = 90 (the upfront cost): <b><i>T</i> = 40<i>m</i> + 90</b>."),
        ("What is the equation of the horizontal line through (4, −2)?", "<i>y</i> = −2", ["<i>x</i> = 4", "<i>y</i> = 4", "<i>x</i> = −2"], "A horizontal line has slope 0, so every point has <i>y</i> = −2: <b><i>y</i> = −2</b>."),
        ("What is the equation of the vertical line through (4, −2)?", "<i>x</i> = 4", ["<i>y</i> = −2", "<i>y</i> = 4<i>x</i>", "<i>x</i> = −2"], "A vertical line has every point with <i>x</i> = 4: <b><i>x</i> = 4</b>. Its slope is undefined."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>A line can be written in three common forms:</p>"
        "<ul><li><b>Slope-intercept</b>: <i>y</i> = <i>mx</i> + <i>b</i> (slope <i>m</i>, <i>y</i>-intercept <i>b</i>)</li>"
        "<li><b>Point-slope</b>: <i>y</i> − <i>y</i><sub>1</sub> = <i>m</i>(<i>x</i> − <i>x</i><sub>1</sub>) (through the point (<i>x</i><sub>1</sub>, <i>y</i><sub>1</sub>))</li>"
        "<li><b>Standard</b>: <i>Ax</i> + <i>By</i> = <i>C</i> (integers, <i>A</i> &gt; 0); find intercepts by setting <i>x</i> or <i>y</i> to 0</li></ul>"
        "<p><b>Parallel</b> lines have the same slope. <b>Perpendicular</b> lines have slopes that are negative reciprocals (their product is −1).</p>",
        [("Write the line through (2, 5) with slope 3 in point-slope and slope-intercept form.", ["<i>y</i> − 5 = 3(<i>x</i> − 2).", "<i>y</i> = 3<i>x</i> − 6 + 5."], "<i>y</i> = 3<i>x</i> − 1"),
         ("Find the intercepts of 2<i>x</i> + 3<i>y</i> = 12.", ["<i>y</i> = 0: <i>x</i> = 6.", "<i>x</i> = 0: <i>y</i> = 4."], "(6, 0) and (0, 4)"),
         ("Find the slope of a line perpendicular to <i>y</i> = −4<i>x</i> + 1.", ["Flip −4 to get −¼, then change the sign."], fr(1, 4))],
        ["Sign errors in point-slope form: through (−3, 2) it is <i>y</i> − 2 = <i>m</i>(<i>x</i> + 3).",
         "Using the <i>y</i>-value of the point as <i>b</i>. Substitute to find <i>b</i>.",
         "Giving a perpendicular line the same slope, or just the reciprocal without changing the sign.",
         "Mixing up the intercepts: the <i>x</i>-intercept is where <i>y</i> = 0."])


def main():
    sets = [S("Point-slope form", collect(one_ps, 20, R)),
            S("Slope-intercept form from points", collect(one_si, 20, R)),
            S("Standard form and intercepts", collect(one_std, 20, R)),
            S("Parallel and perpendicular lines", collect(one_pp, 20, R)),
            S("Linear models", problems())]
    make("forms-of-linear-equations", 7, "A-CED.A.2",
         "Forms of Linear Equations: Point-Slope, Slope-Intercept and Standard Form",
         "Algebra 1 Point-Slope and Standard Form Worksheets: Writing Linear Equations, Parallel and Perpendicular Lines (Free, Answer Key)",
         "Forms of linear equations",
         "Create equations in two or more variables to represent relationships between quantities; graph equations on coordinate axes with labels and scales.",
         "Free Algebra 1 worksheets on writing linear equations (A-CED.A.2, F-LE.A.2): point-slope form, slope-intercept form from points, "
         "standard form and intercepts, parallel and perpendicular lines and linear models. 100 questions with an answer key.",
         "y = mx + b, y − y₁ = m(x − x₁) and Ax + By = C all describe the same line.",
         "Parallel: same slope. Perpendicular: negative reciprocal slopes.",
         body(),
         [("What is point-slope form?", "y − y₁ = m(x − x₁), where m is the slope and (x₁, y₁) is a point on the line."),
          ("How do you convert standard form to slope-intercept form?", "Solve for y: move the x-term to the other side, then divide every term by the coefficient of y."),
          ("How do you find the slope of a perpendicular line?", "Take the negative reciprocal: flip the fraction and change the sign. Perpendicular to slope 2/3 is −3/2."),
          ("How do you find the intercepts from standard form?", "Set y = 0 and solve for x to get the x-intercept; set x = 0 and solve for y to get the y-intercept.")],
         sets, R, domain="Linear Functions")


if __name__ == "__main__":
    main()
