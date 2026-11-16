# -*- coding: utf-8 -*-
"""
US Grade 8 Math: Systems of Linear Equations (8.EE.C.8)
  python3 tools/gen_us_math_g8_systems_of_equations.py
Solve by graphing (the point where the lines cross), decide one / no / infinitely many solutions,
solve by substitution and by elimination, and solve word problems. Wrong answers come from real
mistakes: swapping x and y, stopping after finding one variable, sign slips, and adding instead of
subtracting when eliminating.
"""
import random
from fractions import Fraction as F
from ws_common import num, mcq, balance, B, table, example, write_unit, fig, X, MINUS, RED, BLUE
from g8_common import lin, grid_svg

R = random.Random(80201)
UPDATED = "2026-11-16"
Y = "<i>y</i>"
ONE, NONE, INF = "One solution", "No solution", "Infinitely many solutions"


def pt(x, y):
    return "(%s, %s)" % (num(x), num(y))


def yeq(m, b):
    return "%s = %s" % (Y, lin(m, b))


def std(a, b, c):
    """a x + b y = c"""
    a, b = F(a), F(b)
    s = lin(a, 0) if a else ""
    if b:
        yb = lin(b, 0, Y)
        if not s:
            s = yb
        elif b > 0:
            s += " + " + lin(b, 0, Y)
        else:
            s += " − " + lin(-b, 0, Y)
    return "%s = %s" % (s, num(c))


def pt_choices(x, y, extra=()):
    pairs = list(extra) + [(y, x), (-x, y), (x, -y), (x + 1, y), (x, y + 1), (x - 1, y - 1)]
    return [(pt(a, b), (F(a), F(b))) for a, b in pairs]


def system(a, b):
    return "<span class='sys'>%s<br>%s</span>" % (a, b)


# ============================================================ set 1: graph
def set_graph():
    its = []
    for (m1, b1), (m2, b2) in [((1, 1), (-1, 5)), ((2, -1), (-1, 5)), ((F(1, 2), 2), (-1, 5)), ((1, -2), (-2, 4)),
                               ((3, -4), (-1, 4)), ((-2, 1), (1, -5)), ((F(1, 3), 1), (-1, -3)), ((2, 3), (-1, -3)),
                               ((-1, 2), (1, 2)), ((F(-1, 2), 1), (1, -5)), ((1, 3), (-2, 0)), ((3, 1), (1, -3))]:
        x = (b2 - b1) / F(m1 - m2)
        y = m1 * x + b1
        assert x.denominator == 1 and y.denominator == 1, ((m1, b1), (m2, b2))
        svg = grid_svg(-6, 6, lines=[(m1, b1, RED), (m2, b2, BLUE)], points=[(x, y, "", "#2b2b2b")], unit=20)
        q = fig(svg) + "The graph shows %s and %s. What is the solution of the system?" % (B(yeq(m1, b1)), B(yeq(m2, b2)))
        e = ("The solution is where the lines cross: %s. Check: %s = %s × %s%s and %s = %s × %s%s."
             % (B(pt(x, y)), num(y), num(m1, "f" if F(m1).denominator > 1 else "d"), num(x),
                (" + " + num(b1)) if b1 >= 0 else (" − " + num(-b1)), num(y), num(m2, "f" if F(m2).denominator > 1 else "d"), num(x),
                (" + " + num(b2)) if b2 >= 0 else (" − " + num(-b2))))
        its.append(mcq(q, (pt(x, y), (x, y)), pt_choices(x, y, [(0, b1), (0, b2)]), e))
    for (m1, b1), (m2, b2), (tx, ty) in [((1, 1), (-1, 5), (2, 3)), ((2, -1), (-1, 5), (1, 1)), ((1, -2), (-2, 4), (3, 1)),
                                         ((3, -4), (-1, 4), (2, 3)), ((-2, 1), (1, -5), (1, -1)), ((2, 3), (-1, -3), (-1, 2)),
                                         ((1, 3), (-2, 0), (0, 3)), ((-1, 2), (1, 2), (1, 1))]:
        y1, y2 = m1 * tx + b1, m2 * tx + b2
        ok = (y1 == ty and y2 == ty)
        on1, on2 = y1 == ty, y2 == ty
        q = "Is %s a solution of the system %s?" % (B(pt(tx, ty)), system(yeq(m1, b1), yeq(m2, b2)))
        if ok:
            ans, e = "Yes, it makes both equations true", "Put x = %s in both: %s and %s. Both give y = %s, so <b>yes</b>." % (num(tx), num(y1), num(y2), num(ty))
        elif on1 or on2:
            ans = "No, it makes only one equation true"
            e = "Put x = %s: the first gives y = %s, the second gives y = %s. Only one equals %s, so <b>no</b>." % (num(tx), num(y1), num(y2), num(ty))
        else:
            ans = "No, it makes neither equation true"
            e = "Put x = %s: the equations give y = %s and y = %s, not %s. <b>No</b>." % (num(tx), num(y1), num(y2), num(ty))
        ch = ["Yes, it makes both equations true", "No, it makes only one equation true", "No, it makes neither equation true",
              "Yes, any point is a solution"]
        its.append(mcq(q, (ans, ans), [(c, c) for c in ch if c != ans], e))
    o = its
    order = [o[0], o[12], o[1], o[13], o[2], o[3], o[14], o[4], o[15], o[5], o[16], o[6], o[17], o[7], o[18], o[8],
             o[19], o[9], o[10], o[11]]
    return {"title": "Solve by graphing", "items": order}


# ============================================================ set 2: how many solutions
def set_count():
    its = []
    for (m1, b1), (m2, b2) in [((2, 3), (2, -1)), ((1, 4), (-1, 4)), ((3, -2), (3, -2)), ((F(1, 2), 1), (F(1, 2), 5)),
                               ((-2, 5), (4, 5)), ((-3, 1), (-3, 1)), ((4, 0), (4, 7)), ((F(2, 3), -1), (F(-3, 2), 2))]:
        k = ONE if m1 != m2 else (INF if b1 == b2 else NONE)
        if k == ONE:
            e = "The slopes are different (%s and %s), so the lines cross once: <b>one solution</b>." % (
                num(m1, "f"), num(m2, "f"))
        elif k == NONE:
            e = "Same slope (%s) but different y-intercepts (%s and %s): the lines are parallel and never meet. <b>No solution</b>." % (
                num(m1, "f"), num(b1), num(b2))
        else:
            e = "Same slope and same y-intercept: it is the same line. <b>Infinitely many solutions</b>."
        svg = grid_svg(-6, 6, lines=[(m1, b1, RED), (m2, b2, BLUE)], unit=16)
        its.append(mcq(fig(svg) + "How many solutions does %s have?" % system(yeq(m1, b1), yeq(m2, b2)), (k, k),
                       [(c, c) for c in (ONE, NONE, INF, "Exactly two solutions") if c != k], e))
    for (a1, b1, c1), (a2, b2, c2), k, e in [
        ((2, 1, 5), (4, 2, 10), INF, "The second equation is the first one times 2. Same line: <b>infinitely many solutions</b>."),
        ((1, 1, 3), (1, 1, 7), NONE, "x + y cannot be 3 and 7 at the same time. Parallel lines: <b>no solution</b>."),
        ((3, -1, 2), (1, 1, 6), ONE, "y = 3x − 2 and y = −x + 6 have different slopes: <b>one solution</b>."),
        ((2, -2, 4), (1, -1, 2), INF, "Divide the first by 2: x − y = 2. It is the second equation: <b>infinitely many solutions</b>."),
        ((4, 2, 8), (2, 1, 3), NONE, "Divide the first by 2: 2x + y = 4, but the second says 2x + y = 3: <b>no solution</b>."),
        ((1, -2, 4), (2, 1, 3), ONE, "y = ½x − 2 and y = −2x + 3 have different slopes: <b>one solution</b>."),
        ((-3, 3, 9), (1, -1, -3), INF, "Divide the first by −3: x − y = −3, the same as the second: <b>infinitely many solutions</b>."),
        ((5, 5, 10), (1, 1, 1), NONE, "Divide the first by 5: x + y = 2, but the second says x + y = 1: <b>no solution</b>."),
    ]:
        its.append(mcq("How many solutions does %s have?" % system(std(a1, b1, c1), std(a2, b2, c2)), (k, k),
                       [(c, c) for c in (ONE, NONE, INF, "Exactly two solutions") if c != k], e))
    for m, b, want in [(3, 2, NONE), (-2, 1, INF), (F(1, 2), -4, ONE), (4, -3, NONE)]:
        if want == NONE:
            ans, wr = yeq(m, b + 5), [yeq(m, b), yeq(-m, b), yeq(m + 1, b)]
            e = "Use the same slope with a different y-intercept: parallel lines. The answer is <b>%s</b>." % ans
        elif want == INF:
            ans, wr = "%s = %s" % (lin(2, 0, Y), lin(2 * m, 2 * b)), [yeq(m, b + 1), yeq(m + 1, b), yeq(-m, -b)]
            e = "Divide by 2: %s. It is the same line. The answer is <b>%s</b>." % (yeq(m, b), ans)
        else:
            ans, wr = yeq(-m, b), [yeq(m, b + 3), yeq(m, b - 2), "%s = %s" % (lin(2, 0, Y), lin(2 * m, 2 * b))]
            e = "A different slope makes the lines cross once. The answer is <b>%s</b>." % ans
        its.append(mcq("The first equation is %s. Which second equation gives <b>%s</b>?" % (B(yeq(m, b)), want.lower()),
                       (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[1], o[2], o[3], o[16], o[4], o[5], o[17], o[6], o[7], o[8], o[9], o[18], o[10], o[11], o[12],
             o[19], o[13], o[14], o[15]]
    return {"title": "One, none or infinitely many", "items": order}


# ============================================================ set 3: substitution
def set_sub():
    its = []
    for m, b, a, c, x in [(2, 1, 3, 1, 2), (1, -3, 2, 1, 4), (3, -2, 1, 1, 1), (-1, 6, 2, -1, 3), (2, -5, 4, 1, 3),
                          (4, 1, -1, 1, -1), (-2, 7, 3, 1, 2), (1, 4, 5, -2, 2), (3, 0, 2, 1, -2), (-3, 2, 1, 2, 1),
                          (5, -8, 2, -1, 2), (F(1, 2), 3, 1, 2, 4), (-1, -2, 3, 2, -4), (2, 2, -3, 1, 1),
                          (6, -1, 1, -1, 1), (-4, 10, 2, 1, 2), (1, 7, -2, 3, -3), (3, 5, 4, -1, -2), (-2, -3, 1, 1, -1),
                          (2, -6, 5, 2, 2)]:
        m, b, a, c, x = map(F, (m, b, a, c, x))
        y = m * x + b
        rhs = a * x + c * y
        q = "Solve by substitution: %s" % system(yeq(m, b), std(a, c, rhs))
        e = ("Put %s in for %s: %s + %s(%s) = %s. Solve: %s = %s. Then %s = %s. Solution: <b>%s</b>."
             % (lin(m, b), Y, lin(a, 0), num(c), lin(m, b), num(rhs), X, num(x), Y, num(y), pt(x, y)))
        wrong_x = (rhs - c * b) / (a + c * m) if False else None
        cand = pt_choices(x, y, [(x, rhs - a * x), (y, m * y + b)])
        its.append(mcq(q, (pt(x, y), (x, y)), cand, e))
    return {"title": "Solve by substitution", "items": its}


# ============================================================ set 4: elimination
def set_elim():
    its = []
    for a1, b1, a2, b2, x, y in [(1, 1, 1, -1, 5, 2), (2, 1, 3, -1, 3, 1), (1, 2, -1, 3, 1, 4), (3, 2, 5, -2, 2, -1),
                                 (2, 3, 2, -1, 4, -2), (4, 1, 1, 1, 2, 3), (1, -1, 2, 1, -1, 3), (5, 2, 3, 2, 2, 1),
                                 (2, 5, -2, 3, 3, -1), (1, 3, 1, -2, -2, 2), (3, -1, 1, 1, 3, 5), (2, 2, 3, -2, 1, 4),
                                 (6, 1, 2, -1, 1, -4), (1, 4, -1, 2, 6, -1), (7, 3, 2, -3, 1, 2), (2, -3, 4, 3, 3, 1),
                                 (3, 4, 3, 1, -2, 3), (1, 1, 2, 1, -3, 5), (4, -2, 1, 2, 2, 3), (5, 1, -5, 2, 1, -2)]:
        c1, c2 = a1 * x + b1 * y, a2 * x + b2 * y
        q = "Solve by elimination: %s" % system(std(a1, b1, c1), std(a2, b2, c2))
        if b1 == -b2:
            how = "Add the equations: the %s-terms cancel. %s = %s, so %s = %s." % (Y, lin(a1 + a2, 0), num(c1 + c2), X, num(x))
        elif b1 == b2:
            how = "Subtract the equations: the %s-terms cancel. %s = %s, so %s = %s." % (Y, lin(a1 - a2, 0), num(c1 - c2), X, num(x))
        elif a1 == -a2:
            how = "Add the equations: the %s-terms cancel. %s = %s, so %s = %s." % (X, lin(b1 + b2, 0, Y), num(c1 + c2), Y, num(y))
        elif a1 == a2:
            how = "Subtract the equations: the %s-terms cancel. %s = %s, so %s = %s." % (X, lin(b1 - b2, 0, Y), num(c1 - c2), Y, num(y))
        else:
            k = F(b1, b2)
            how = ("Multiply the second equation by %s so the %s-terms match, then subtract to find %s = %s."
                   % (num(k, "f"), Y, X, num(x)))
        e = how + " Put it back in to find the other value. Solution: <b>%s</b>." % pt(x, y)
        its.append(mcq(q, (pt(x, y), (x, y)), pt_choices(x, y), e))
    return {"title": "Solve by elimination", "items": its}


# ============================================================ set 5: word problems
def set_words():
    its = []

    def item(q, ans, wr, e):
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))

    item("Two numbers add up to 20. Their difference is 6. What are the numbers?", "13 and 7", ["14 and 6", "10 and 10", "12 and 8"],
         "x + y = 20 and x − y = 6. Add: 2x = 26, so x = 13 and y = 7. The answer is <b>13 and 7</b>.")
    item("Adult tickets cost $8 and child tickets cost $5. 10 tickets cost $62. How many adult tickets were sold?", "4", ["6", "8", "5"],
         "a + c = 10 and 8a + 5c = 62. Then 8a + 5(10 − a) = 62, 3a = 12, a = <b>4</b>.")
    item("A farm has chickens and cows: 15 heads and 44 legs. How many cows are there?", "7", ["8", "11", "5"],
         "c + k = 15 and 2c + 4k = 44. Then 2(15 − k) + 4k = 44, 2k = 14, k = <b>7</b> cows.")
    item("Gym A: $20 to join and $15 a month. Gym B: $50 to join and $10 a month. After how many months is the total cost the same?",
         "6 months", ["3 months", "7 months", "14 months"], "20 + 15m = 50 + 10m, so 5m = 30 and m = <b>6 months</b>.")
    item("Pens cost $2 and notebooks cost $3. Kim buys 9 items for $22. How many notebooks does she buy?", "4", ["5", "7", "3"],
         "p + n = 9 and 2p + 3n = 22. Then 2(9 − n) + 3n = 22, so n = <b>4</b>.")
    item("A boat goes 24 miles downstream in 2 hours and back upstream in 3 hours. What is the speed of the boat in still water?",
         "10 mph", ["12 mph", "8 mph", "2 mph"], "b + c = 12 and b − c = 8. Add: 2b = 20, so b = <b>10 mph</b> (current 2 mph).")
    item("The sum of two numbers is 35. One number is 4 times the other. What is the larger number?", "28", ["7", "31", "21"],
         "x + y = 35 and y = 4x. Then 5x = 35, x = 7 and y = <b>28</b>.")
    item("Hot dogs cost $3 and drinks cost $2. Sam buys 2 hot dogs and 3 drinks. Lee buys 4 hot dogs and 1 drink. Who pays more?",
         "Lee", ["Sam", "They pay the same", "We cannot tell"],
         "Sam: 2(3) + 3(2) = $12. Lee: 4(3) + 1(2) = $14. <b>Lee</b> pays more.")
    item("A rectangle's perimeter is 30 cm. Its length is 3 cm more than its width. What is the width?", "6 cm", ["9 cm", "7.5 cm", "12 cm"],
         "2L + 2W = 30 and L = W + 3. Then 2(W + 3) + 2W = 30, 4W = 24, W = <b>6 cm</b>.")
    item("Mia has 14 coins, all dimes and quarters. They are worth $2.30. How many quarters does she have?", "6", ["8", "4", "10"],
         "d + q = 14 and 10d + 25q = 230. Then 10(14 − q) + 25q = 230, 15q = 90, q = <b>6</b>.")
    item("Plan A: $30 plus $0.10 per minute. Plan B: $10 plus $0.20 per minute. For how many minutes do the plans cost the same?",
         "200 minutes", ["100 minutes", "20 minutes", "400 minutes"], "30 + 0.1m = 10 + 0.2m, so 20 = 0.1m and m = <b>200 minutes</b>.")
    item("Two angles are supplementary (they add to 180°). One is 40° more than the other. What is the smaller angle?", "70°",
         ["110°", "40°", "90°"], "x + y = 180 and y = x + 40. Then 2x + 40 = 180, x = <b>70°</b>.")
    item("A test has 20 questions worth 2 or 5 points. The total is 64 points. How many 5-point questions are there?", "8", ["12", "10", "6"],
         "a + b = 20 and 2a + 5b = 64. Then 2(20 − b) + 5b = 64, 3b = 24, b = <b>8</b>.")
    item("Line A: y = 2x + 1. Line B: y = −x + 7. Where do the lines meet?", "(2, 5)", ["(5, 2)", "(3, 4)", "(2, −5)"],
         "2x + 1 = −x + 7, so 3x = 6, x = 2 and y = 5. They meet at <b>(2, 5)</b>.")
    item("A store sells 3 apples and 2 pears for $4, and 1 apple and 2 pears for $2. What is the price of 1 apple?", "$1", ["$0.50", "$2", "$1.50"],
         "Subtract the equations: 2 apples = $2, so 1 apple = <b>$1</b> (and a pear costs $0.50).")
    item("Car A leaves at 40 mph. Car B leaves from the same place 1 hour later at 60 mph. After how many hours of driving will car B catch up?",
         "2 hours", ["3 hours", "1 hour", "4 hours"], "60t = 40(t + 1), so 20t = 40 and t = <b>2 hours</b>.")
    item("A class has 28 students. There are 4 more girls than boys. How many girls are there?", "16", ["12", "14", "18"],
         "g + b = 28 and g = b + 4. Then 2b + 4 = 28, b = 12, g = <b>16</b>.")
    item("A mix of nuts costs $6 per pound and raisins cost $3 per pound. 10 pounds of the mix cost $45. How many pounds of nuts are in it?",
         "5 pounds", ["7.5 pounds", "3 pounds", "6 pounds"], "n + r = 10 and 6n + 3r = 45. Then 6n + 3(10 − n) = 45, 3n = 15, n = <b>5 pounds</b>.")
    item("The system y = 3x + 2 and y = 3x − 4 models two savings plans. When do they have the same amount?", "Never",
         ["After 1 week", "After 2 weeks", "Always"], "Same slope, different starting amounts: the lines are parallel. <b>Never</b>.")
    item("Movie tickets: 3 adults and 2 kids cost $47. 2 adults and 4 kids cost $46. What does an adult ticket cost?", "$12", ["$11", "$5.50", "$9"],
         "Double the first: 6a + 4k = 94. Subtract the second: 4a = 48, so a = <b>$12</b> (kids $5.50).")
    return {"title": "Word problems", "items": its}


def body():
    return ("<h2>What is a system?</h2>"
            "<p>A <b>system of equations</b> is two equations with the same variables. "
            "The <b>solution</b> is the point (" + X + ", " + Y + ") that makes both equations true. "
            "On a graph, it is where the two lines cross.</p>"
            + table(["Lines", "Slopes", "Solutions"], [["Cross once", "different", "one"], ["Parallel", "same slope, different intercept", "none"],
                                                     ["Same line", "same slope and intercept", "infinitely many"]])
            + example("Substitution: " + Y + " = 2" + X + " + 1 and 3" + X + " + " + Y + " = 11",
                      ["Put 2" + X + " + 1 in for " + Y + ": 3" + X + " + 2" + X + " + 1 = 11.", "5" + X + " = 10, so " + X + " = 2.",
                       "Then " + Y + " = 2(2) + 1 = 5."], "(2, 5)")
            + example("Elimination: " + X + " + " + Y + " = 7 and " + X + " − " + Y + " = 3",
                      ["Add the equations: 2" + X + " = 10, so " + X + " = 5.", "Then 5 + " + Y + " = 7, so " + Y + " = 2."], "(5, 2)")
            + "<h2>Common mistakes</h2><ul>"
            "<li>Writing the point backwards: (" + X + ", " + Y + ") means " + X + " first.</li>"
            "<li>Stopping after one variable: find both " + X + " and " + Y + ".</li>"
            "<li>Adding when the terms have the same sign: subtract to cancel them.</li>"
            "<li>Not checking: put the point into <b>both</b> equations.</li></ul>")


def main():
    sets = [set_graph(), set_count(), set_sub(), set_elim(), set_words()]
    balance(sets, R)
    unit = {
        "slug": "systems-of-equations",
        "title": "Systems of Linear Equations",
        "seo_title": "Grade 8 Systems of Equations Worksheets: Graphing, Substitution, Elimination and Word Problems",
        "short_title": "Systems of equations",
        "domain": "Expressions & Equations",
        "standard_code": "8.EE.C.8",
        "standard_url": "https://www.thecorestandards.org/Math/Content/8/EE/C/8/",
        "standard_text": "Analyze and solve pairs of simultaneous linear equations. a. Understand that solutions to a system of two linear equations in two variables correspond to points of intersection of their graphs. b. Solve systems of two linear equations in two variables algebraically, and estimate solutions by graphing the equations. c. Solve real-world and mathematical problems leading to two linear equations in two variables.",
        "meta_desc": "Free Grade 8 systems of equations worksheets: solve by graphing, decide one, no or infinitely many solutions, solve by substitution and elimination, and write systems for word problems. 100 questions with an answer key.",
        "key_big": "The solution of a system is the point that makes both equations true: where the lines cross.",
        "key_sub": "Different slopes: one solution. Parallel lines: none. Same line: infinitely many.",
        "body_html": body(),
        "faq": [
            {"q": "What is the solution of a system of equations?", "a": "It is the pair (x, y) that makes both equations true. On a graph it is the point where the two lines cross."},
            {"q": "When should I use substitution or elimination?", "a": "Use substitution when one equation already says y = … or x = …. Use elimination when the x- or y-terms already match or are opposites."},
            {"q": "How can a system have no solution?", "a": "If the lines are parallel (same slope, different y-intercepts), they never meet, so no point makes both equations true."},
            {"q": "How do I check my answer?", "a": "Put the x and y values into both original equations. If both are true, the answer is correct."}],
        "sets": sets, "pdf_url": "", "sort": 2, "updated": UPDATED,
    }
    write_unit("us", "math", "grade-8", unit)


if __name__ == "__main__":
    main()
