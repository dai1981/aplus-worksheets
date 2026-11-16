# -*- coding: utf-8 -*-
"""
US Grade 8 Math: Scatter Plots and Lines of Best Fit (8.SP.A.1, 8.SP.A.2, 8.SP.A.3)
  python3 tools/gen_us_math_g8_scatter_plots.py
Describe association (positive, negative, none; linear or nonlinear), spot outliers and clusters,
judge a line of best fit, and use its equation to predict and to explain slope and intercept.
Wrong answers come from real mistakes: reading the direction backwards, calling a weak trend "none",
thinking association means cause, and swapping the meaning of slope and intercept.
"""
import random, math
from ws_common import mcq, balance, B, table, example, write_unit, fig, svg_wrap, text, line, INK, RED, BLUE

R = random.Random(81501)
UPDATED = "2026-11-16"
POS, NEG, NONE = "Positive association", "Negative association", "No association"


def scatter_svg(pts, xlab="x", ylab="y", fit=None, hi=10, mark=None, u=22):
    m = 34
    W, H = hi * u + m + 16, hi * u + m + 16
    X_ = lambda x: m + x * u
    Y_ = lambda y: H - m + 6 - y * u
    s = []
    for k in range(0, hi + 1, 2):
        s.append(line(X_(k), Y_(0), X_(k), Y_(hi), "#e2e2e2", 1))
        s.append(line(X_(0), Y_(k), X_(hi), Y_(k), "#e2e2e2", 1))
        s.append(text(X_(k), Y_(0) + 14, str(k), 10, weight=400))
        s.append(text(X_(0) - 6, Y_(k) + 4, str(k), 10, anchor="end", weight=400))
    s.append(line(X_(0), Y_(0), X_(hi), Y_(0), INK, 1.8))
    s.append(line(X_(0), Y_(0), X_(0), Y_(hi), INK, 1.8))
    s.append(text(X_(hi / 2), H - 2, xlab, 11, weight=400))
    s.append("<text x='12' y='%d' font-size='11' fill='%s' transform='rotate(-90 12 %d)' text-anchor='middle'>%s</text>" % (Y_(hi / 2), INK, Y_(hi / 2), ylab))
    if fit:
        mm, b = fit
        x1, x2 = 0, hi
        y1, y2 = b, mm * hi + b
        if y2 > hi:
            x2 = (hi - b) / mm
            y2 = hi
        if y2 < 0:
            x2 = -b / mm
            y2 = 0
        s.append(line(X_(x1), Y_(y1), X_(x2), Y_(y2), RED, 2))
    for i, (x, y) in enumerate(pts):
        col = RED if mark is not None and i == mark else BLUE
        s.append("<circle cx='%.1f' cy='%.1f' r='4' fill='%s'/>" % (X_(x), Y_(y), col))
    return svg_wrap(int(W), int(H), "".join(s), "scatter plot")


def make(kind, seed, n=14, outlier=False):
    r = random.Random(seed)
    pts = []
    for i in range(n):
        x = 0.6 + i * 8.8 / (n - 1) + r.uniform(-0.25, 0.25)
        if kind == "pos":
            y = 1 + 0.75 * x + r.uniform(-1.1, 1.1)
        elif kind == "neg":
            y = 9 - 0.75 * x + r.uniform(-1.1, 1.1)
        elif kind == "none":
            y = r.uniform(0.8, 9.2)
        elif kind == "curve":
            y = 0.11 * (x - 5) ** 2 * 3 + 1 + r.uniform(-0.4, 0.4)
        elif kind == "strongpos":
            y = 0.5 + 0.9 * x + r.uniform(-0.35, 0.35)
        elif kind == "weakneg":
            y = 8 - 0.5 * x + r.uniform(-2.2, 2.2)
        pts.append((x, max(0.3, min(9.7, y))))
    if outlier:
        pts.append((9, 1) if kind in ("pos", "strongpos") else (9, 9) if kind in ("neg", "weakneg") else (5, 9))
    return pts


# ============================================================ set 1: association
def set_assoc():
    its = []
    for kind, labels, ans, why in [
        ("pos", ("hours studied", "test score"), POS, "As x goes up, y tends to go up."),
        ("neg", ("hours of TV", "test score"), NEG, "As x goes up, y tends to go down."),
        ("none", ("shoe size", "test score"), NONE, "The points are spread out with no up or down pattern."),
        ("strongpos", ("height (ft)", "arm span (ft)"), POS, "The points rise together closely."),
        ("weakneg", ("price ($)", "sales"), NEG, "The trend is weak, but y still tends to go down as x goes up."),
        ("pos", ("temperature", "ice creams sold"), POS, "Warmer days go with more sales."),
        ("neg", ("car age (years)", "value ($1,000s)"), NEG, "Older cars tend to be worth less."),
        ("none", ("birth month", "height"), NONE, "There is no pattern."),
        ("strongpos", ("time (h)", "distance (mi)"), POS, "Distance grows steadily with time."),
        ("weakneg", ("absences", "grade"), NEG, "More absences tend to go with lower grades, though the points are spread."),
        ("pos", ("age (years)", "height (in.)"), POS, "Older children tend to be taller."),
        ("neg", ("altitude", "temperature"), NEG, "Higher up tends to be colder."),
    ]:
        pts = make(kind, seed=len(its) + 10)
        q = fig(scatter_svg(pts, *labels)) + "What kind of association does the scatter plot show?"
        its.append(mcq(q, (ans, ans), [(c, c) for c in [POS, NEG, NONE, "Both positive and negative"] if c != ans], why + " <b>%s</b>." % ans))
    for kind, ans, why in [("curve", "Nonlinear", "The points follow a curve, not a straight line."),
                           ("strongpos", "Linear", "The points lie close to a straight line."),
                           ("neg", "Linear", "The points go down along a rough straight line."),
                           ("curve", "Nonlinear", "The points go down and then up: a curve.")]:
        pts = make(kind, seed=len(its) + 50)
        q = fig(scatter_svg(pts)) + "Is the association linear or nonlinear?"
        its.append(mcq(q, (ans, ans), [(c, c) for c in ["Linear", "Nonlinear", "No association", "Negative only"] if c != ans],
                       why + " <b>%s</b>." % ans))
    for q, ans, wr, e in [
        ("A scatter plot shows that people who sleep more tend to make fewer mistakes. What kind of association is it?", NEG, [POS, NONE, "Nonlinear only"],
         "More sleep goes with fewer mistakes: one goes up as the other goes down. <b>%s</b>." % NEG),
        ("Taller trees tend to have wider trunks. What kind of association is it?", POS, [NEG, NONE, "We cannot tell"],
         "Both go up together: <b>%s</b>." % POS),
        ("Ice cream sales and sunburns both go up in summer. Does eating ice cream cause sunburn?", "No, both are linked to hot weather",
         ["Yes, the plot shows it", "Yes, always", "Only for children"], "Association does not prove cause. <b>No, both are linked to hot weather</b>."),
        ("A strong association means the points …", "lie close to a line or curve", ["are far apart", "go up", "are all the same"],
         "Strong means <b>the points lie close to a line or curve</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[1], o[2], o[16], o[3], o[12], o[4], o[17], o[5], o[13], o[6], o[18], o[7], o[14], o[8], o[19], o[9],
             o[15], o[10], o[11]]
    return {"title": "Describe the association", "items": order}


# ============================================================ set 2: outliers and clusters
def set_outliers():
    its = []
    for kind, seed in [("pos", 1), ("neg", 2), ("strongpos", 3), ("pos", 4), ("neg", 5), ("strongpos", 6), ("pos", 7), ("neg", 8)]:
        pts = make(kind, seed, n=11, outlier=True)
        ox, oy = pts[-1]
        q = fig(scatter_svg(pts)) + "Which point is an outlier?"
        ans = "(%d, %d)" % (round(ox), round(oy))
        others = [pts[2], pts[5], pts[8]]
        wr = ["(%d, %d)" % (round(x), round(y)) for x, y in others]
        e = "An outlier is far from the other points. The point near <b>%s</b> does not follow the pattern." % ans
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr if w != ans] + [("There is no outlier", "n")], e))
    for q, ans, wr, e in [
        ("A scatter plot has two groups of points close together, with a gap between them. What are these groups called?", "Clusters",
         ["Outliers", "Lines of best fit", "Axes"], "Groups of points close together are <b>clusters</b>."),
        ("What is an outlier?", "A point far away from the others", ["The highest point", "The first point", "A point on the line of best fit"],
         "An outlier is <b>a point far away from the others</b>."),
        ("Should a line of best fit go through the outlier?", "No, it should follow the main pattern", ["Yes, always", "It must start at the outlier",
         "Only if the outlier is high"], "The line shows the trend of most points: <b>no, it should follow the main pattern</b>."),
        ("Study hours vs. test score: one student studied 9 hours but scored 30. What is this point?", "An outlier", ["A cluster", "The slope", "The intercept"],
         "Most students who studied a lot scored high, so this point is <b>an outlier</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    for q, ans, wr, e in [
        ("Points are spread out with no pattern. Can you draw a useful line of best fit?", "No, there is no association",
         ["Yes, always", "Yes, through the middle point", "Only with an outlier"], "With no pattern, a line does not help: <b>no, there is no association</b>."),
        ("How many points should be above and below a good line of best fit?", "About the same number", ["All above", "All below", "Exactly two"],
         "A good line has <b>about the same number</b> of points on each side."),
        ("A line of best fit for a negative association has a …", "negative slope", ["positive slope", "slope of 0", "vertical line"],
         "Going down from left to right means a <b>negative slope</b>."),
        ("A line of best fit should be …", "close to most points", ["through the first and last point", "through the origin", "as steep as possible"],
         "It should be <b>close to most points</b>."),
        ("Two scatter plots both go up. In which is the association stronger?", "The one with points closer to a line", ["The one with more points",
         "The one with bigger numbers", "The one that starts higher"], "Strength is how close the points are to a line: <b>the one with points closer to a line</b>."),
        ("Most points rise, but a few at the right go down a lot. What might you see?", "A nonlinear pattern", ["No association", "A perfect line",
         "Only outliers"], "Rising then falling is a curve: <b>a nonlinear pattern</b>."),
        ("A scatter plot compares two …", "sets of numbers about the same things", ["categories like colors", "single numbers", "letters"],
         "Each point pairs two measurements: <b>sets of numbers about the same things</b>."),
        ("Why do we make a scatter plot?", "To see if two variables are related", ["To find one average", "To count categories", "To show parts of a whole"],
         "A scatter plot shows <b>if two variables are related</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[9], o[1], o[8], o[2], o[11], o[3], o[10], o[12], o[4], o[13], o[5], o[14], o[6], o[15], o[7], o[16],
             o[17], o[18], o[19]]
    return {"title": "Outliers, clusters and fit", "items": order}


# ============================================================ set 3: judge a line
def set_judge():
    its = []
    for kind, seed, good, bads in [("pos", 21, (0.75, 1), [(0.75, 3.5), (-0.5, 6), (0.2, 4)]), ("neg", 22, (-0.75, 9), [(-0.75, 6.5), (0.5, 3), (-1.6, 9)]),
                                   ("strongpos", 23, (0.9, 0.5), [(0.4, 0.5), (0.9, 3), (1.5, -1)]), ("weakneg", 24, (-0.5, 8), [(0.5, 2), (-0.5, 4.5), (0, 5)])]:
        pts = make(kind, seed)
        lines = [good] + bads
        idx = [0, 1, 2, 3]
        R.shuffle(idx)
        shown = [lines[i] for i in idx]
        ans = "ABCD"[idx.index(0)]
        svgs = "".join("<span style='display:inline-block;text-align:center'>%s<br><b>%s</b></span>" % (scatter_svg(pts, fit=ln, hi=10, u=13), "ABCD"[j])
                       for j, ln in enumerate(shown))
        q = fig(svgs) + "Which graph shows the best line of fit?"
        e = "The best line follows the trend with about as many points above it as below. The answer is <b>%s</b>." % ans
        its.append(mcq(q, (ans, ans), [(x, x) for x in "ABCD" if x != ans], e))
    for kind, seed, fit, ok in [("pos", 31, (0.75, 1), True), ("pos", 32, (0.75, 4), False), ("neg", 33, (-0.75, 9), True), ("neg", 34, (0.4, 2), False),
                                ("strongpos", 35, (0.9, 0.5), True), ("strongpos", 36, (0.3, 2), False), ("weakneg", 37, (-0.5, 8), True), ("neg", 38, (-0.75, 6), False)]:
        pts = make(kind, seed)
        ans = "Yes" if ok else "No"
        why = "It follows the trend with points on both sides." if ok else "Most points are on one side of it, or it goes the wrong way."
        q = fig(scatter_svg(pts, fit=fit)) + "Is the red line a good line of best fit?"
        its.append(mcq(q, (ans, ans), [(c, c) for c in ["Yes", "No", "Only if it goes through (0, 0)", "We cannot tell from a graph"] if c != ans],
                       why + " <b>%s</b>." % ans))
    for kind, seed, fit, slope_txt in [("pos", 41, (0.75, 1), "about 0.75"), ("neg", 42, (-0.75, 9), "about −0.75"), ("strongpos", 43, (1, 0), "about 1"),
                                       ("pos", 44, (0.5, 2), "about 0.5"), ("neg", 45, (-1, 10), "about −1"), ("weakneg", 46, (-0.5, 8), "about −0.5"),
                                       ("strongpos", 47, (0.8, 1), "about 0.8"), ("neg", 48, (-0.5, 7), "about −0.5")]:
        pts = make(kind, seed)
        m, b = fit
        q = fig(scatter_svg(pts, fit=fit)) + "Estimate the slope of the red line."
        e = ("From (0, %g) to (4, %g): the line changes by %g over 4. Slope ≈ %g, so <b>%s</b>." % (b, m * 4 + b, m * 4, m, slope_txt)).replace("-", "−")
        others = ["about %g" % -m, "about %g" % b, "about %g" % (2 * m)]
        others = [o.replace("-", "−") for o in others]
        its.append(mcq(q, (slope_txt, slope_txt), [(o, o) for o in others if o != slope_txt] + [("about 10", "t")], e))
    o = its
    order = [o[4], o[0], o[12], o[5], o[13], o[1], o[6], o[14], o[2], o[7], o[15], o[3], o[8], o[16], o[9], o[17], o[10],
             o[18], o[11], o[19]]
    return {"title": "Lines of best fit", "items": order}


# ============================================================ set 4: predict with the equation
def set_predict():
    its = []
    for eq, (m, b), xv, xlab, ylab, unit in [
        ("y = 5x + 60", (5, 60), 6, "hours studied", "test score", " points"), ("y = 2.5x + 10", (2.5, 10), 8, "age (years)", "height (in.)", " in."),
        ("y = −3x + 90", (-3, 90), 12, "days absent", "grade", " points"), ("y = 0.5x + 2", (0.5, 2), 30, "minutes", "miles", " mi"),
        ("y = 12x + 15", (12, 15), 5, "hours worked", "dollars", " dollars"), ("y = −1.5x + 40", (-1.5, 40), 10, "car age", "value ($1,000s)", ""),
        ("y = 4x + 30", (4, 30), 9, "temperature over 60°F", "drinks sold", " drinks"), ("y = 0.8x + 1", (0.8, 1), 15, "weeks", "plant height (cm)", " cm"),
        ("y = −2x + 75", (-2, 75), 20, "hours of TV a week", "score", " points"), ("y = 6x + 20", (6, 20), 7, "people", "cost ($)", " dollars"),
    ]:
        y = m * xv + b
        ys = ("%g" % y).replace("-", "−")
        q = "A line of best fit is %s, where x is %s and y is %s. Predict y when x = %d." % (B(eq), xlab, ylab, xv)
        e = "Put x = %d in: %s. So about <b>%s%s</b>." % (xv, eq.replace("x", "(%d)" % xv).replace("y = ", ""), ys, unit)
        wr = [m * xv, b, m + b, y + m]
        its.append(mcq(q, (ys + unit, y), [(("%g" % w).replace("-", "−") + unit, w) for w in wr], e))
    for eq, xname, yname, ask, ans, wr, e in [
        ("y = 5x + 60", "hours studied", "test score", "slope", "Each extra hour of study adds about 5 points", ["A student who studies 0 hours scores 5",
         "Each point adds 5 hours", "The highest score is 60"], "The slope 5 is the change in score for each hour: <b>each extra hour of study adds about 5 points</b>."),
        ("y = 5x + 60", "hours studied", "test score", "y-intercept", "A student who studies 0 hours is predicted to score about 60",
         ["Each hour adds 60 points", "The test has 60 questions", "Scores go down by 60"], "When x = 0, y = 60: <b>a student who studies 0 hours is predicted to score about 60</b>."),
        ("y = −3x + 90", "days absent", "grade", "slope", "Each day absent lowers the grade by about 3 points",
         ["Each day absent raises the grade by 3", "The grade starts at 3", "Students miss 3 days"], "−3 is the change per day: <b>each day absent lowers the grade by about 3 points</b>."),
        ("y = 12x + 15", "hours worked", "pay ($)", "y-intercept", "About $15 is paid even for 0 hours (a base amount)",
         ["$12 per hour", "15 hours of work", "The pay goes down by $15"], "When x = 0, y = 15: <b>about $15 is paid even for 0 hours (a base amount)</b>."),
        ("y = 0.8x + 1", "weeks", "plant height (cm)", "slope", "The plant grows about 0.8 cm each week",
         ["The plant starts at 0.8 cm", "The plant grows 1 cm each week", "It takes 0.8 weeks to grow"], "<b>The plant grows about 0.8 cm each week</b>."),
        ("y = −1.5x + 40", "car age (years)", "value ($1,000s)", "y-intercept", "A new car is worth about $40,000",
         ["The car loses $40,000 a year", "The car is 40 years old", "The car loses $1,500 a year"], "At age 0 the value is 40 thousand: <b>a new car is worth about $40,000</b>."),
        ("y = 4x + 30", "degrees over 60°F", "drinks sold", "slope", "About 4 more drinks are sold for each degree warmer",
         ["30 drinks are sold each degree", "4 drinks are sold at 60°F", "Drinks cost $4"], "<b>About 4 more drinks are sold for each degree warmer</b>."),
        ("y = 6x + 20", "people", "party cost ($)", "y-intercept", "A $20 cost even with no people (like a room fee)",
         ["$6 per person", "20 people came", "$26 for each person"], "When x = 0, y = 20: <b>a $20 cost even with no people (like a room fee)</b>."),
        ("y = 2.5x + 10", "age (years)", "height (in.)", "slope", "Children grow about 2.5 in. per year in this data",
         ["Children are 2.5 in. tall at birth", "Height doubles each year", "Children grow 10 in. a year"], "<b>Children grow about 2.5 in. per year in this data</b>."),
        ("y = −2x + 75", "hours of TV a week", "score", "slope", "Each extra hour of TV goes with about 2 fewer points",
         ["Each hour of TV adds 2 points", "Scores start at 2", "TV causes lower scores"], "The slope shows a trend, not a cause: <b>each extra hour of TV goes with about 2 fewer points</b>."),
    ]:
        q = "The line of best fit is %s (x = %s, y = %s). What does the %s mean?" % (B(eq.replace("-", "−")), xname, yname, ask)
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[10], o[1], o[11], o[2], o[12], o[3], o[13], o[4], o[14], o[5], o[15], o[6], o[16], o[7], o[17], o[8],
             o[18], o[9], o[19]]
    return {"title": "Predict and interpret", "items": order}


# ============================================================ set 5: reasoning
def set_reason():
    its = []
    for q, ans, wr, e in [
        ("A line of best fit predicts a score of 110 for 12 hours of study, but the test only goes to 100. What does this show?",
         "Predictions far outside the data can be wrong", ["The line is perfect", "The student will score 110", "The slope is negative"],
         "<b>Predictions far outside the data can be wrong</b>."),
        ("Which data would most likely show a negative association?", "Hours of exercise and resting heart rate", ["Height and weight",
         "Study time and test score", "Age and height of children"], "More exercise tends to go with a lower resting heart rate: <b>negative</b>."),
        ("Which data would most likely show no association?", "Shoe size and favorite number", ["Height and arm span", "Speed and distance in 1 hour",
         "Price and number sold"], "These are not related: <b>shoe size and favorite number</b>."),
        ("Which data would most likely show a positive association?", "Number of rooms and price of a house", ["Car age and value",
         "Altitude and temperature", "Absences and grades"], "More rooms tend to go with a higher price: <b>positive</b>."),
        ("A scatter plot of x = hours of sleep and y = test score shows a positive association. Which is true?", "Students who sleep more tend to score higher",
         ["Sleep causes higher scores for sure", "Every student who sleeps more scores higher", "Students who sleep more score lower"],
         "Association describes a tendency, not a rule or a cause: <b>students who sleep more tend to score higher</b>."),
        ("The points lie almost exactly on a straight line going down. How would you describe it?", "Strong negative linear association",
         ["Weak positive association", "No association", "Nonlinear association"], "<b>Strong negative linear association</b>."),
        ("The points go up but are widely spread. How would you describe it?", "Weak positive association", ["Strong positive association",
         "Negative association", "No association"], "<b>Weak positive association</b>."),
        ("A line of best fit is y = 3x + 2. For which x is the predicted y equal to 20?", "6", ["62", "18", "7.3"], "3x + 2 = 20, so 3x = 18 and x = <b>6</b>."),
        ("A line of best fit is y = −4x + 50. When does it predict y = 10?", "x = 10", ["x = 15", "x = 10.5", "x = −10"], "−4x + 50 = 10, −4x = −40, <b>x = 10</b>."),
        ("A line of best fit passes through (2, 5) and (6, 13). What is its slope?", "2", ["0.5", "8", "4"], "(13 − 5) ÷ (6 − 2) = 8 ÷ 4 = <b>2</b>."),
        ("A line of best fit passes through (0, 4) and (5, 14). What is its equation?", "y = 2x + 4", ["y = 4x + 2", "y = 2x + 14", "y = 10x + 4"],
         "Slope = 10 ÷ 5 = 2, intercept 4: <b>y = 2x + 4</b>."),
        ("A line of best fit passes through (0, 80) and (10, 30). What is its equation?", "y = −5x + 80", ["y = 5x + 80", "y = −5x + 30", "y = −50x + 80"],
         "Slope = (30 − 80) ÷ 10 = −5, intercept 80: <b>y = −5x + 80</b>."),
        ("Why is it better to use a line of best fit than two random points to predict?", "It uses the trend of all the data", ["It is always exact",
         "It goes through every point", "It ignores the data"], "<b>It uses the trend of all the data</b>."),
        ("A scatter plot of temperature and hot chocolate sales shows a negative association. Predict sales on a very cold day.", "High",
         ["Low", "Zero", "The same as a hot day"], "Colder (lower x) goes with more sales: <b>high</b>."),
        ("A scatter plot shows age and reading speed for children 6 to 12. Is it safe to use the line to predict for a 40-year-old?", "No, 40 is far outside the data",
         ["Yes, lines go on forever", "Yes, adults read fast", "Only if the slope is positive"], "<b>No, 40 is far outside the data</b>."),
        ("What is on each axis of a scatter plot?", "One variable on each axis", ["Categories on both axes", "The same variable twice", "Only counts"],
         "<b>One variable on each axis</b>."),
        ("A cluster of points sits in the bottom left, and another in the top right. What might this mean?", "There are two groups in the data",
         ["The data has no pattern", "There is a single outlier", "The line must be vertical"], "<b>There are two groups in the data</b>."),
        ("Removing an outlier usually makes the line of best fit …", "fit the other points better", ["much steeper always", "go through the origin", "disappear"],
         "<b>It fits the other points better</b>."),
        ("A line of best fit has slope 0. What does this suggest?", "No association", ["Strong positive association", "Strong negative association", "Nonlinear association"],
         "A flat trend means y does not change with x: <b>no association</b>."),
        ("Which is an example of bivariate data?", "Height and weight of 20 students", ["Favorite colors of 20 students", "Heights of 20 students",
         "Number of pets in one house"], "Bivariate means two variables measured on each item: <b>height and weight of 20 students</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    return {"title": "Reasoning with scatter plots", "items": its}


def body():
    return ("<h2>Scatter plots</h2>"
            "<p>A <b>scatter plot</b> shows pairs of numbers as points. It helps you see if two variables are related.</p>"
            "<figure class='sn-fig'>" + scatter_svg(make("pos", 99), "hours studied", "test score", fit=(0.75, 1)) + "<figcaption>Positive association with a line of best fit.</figcaption></figure>"
            + table(["Pattern", "Meaning"], [["Points go up", "positive association"], ["Points go down", "negative association"],
                                             ["No pattern", "no association"], ["Points follow a curve", "nonlinear association"]])
            + "<h2>Line of best fit</h2><p>A straight line close to most points, with about as many above as below. "
            "Its <b>slope</b> is the change in y for each 1 in x. Its <b>y-intercept</b> is the predicted y when x = 0.</p>"
            + example("A line of best fit is y = 5x + 60 (x = hours studied, y = score). Predict the score for 6 hours.", ["y = 5(6) + 60 = 30 + 60."], "90")
            + "<h2>Common mistakes</h2><ul><li>Saying a weak trend is no association.</li>"
            "<li>Thinking association means cause.</li><li>Drawing the line through the first and last points only.</li>"
            "<li>Predicting far outside the data.</li></ul>")


def main():
    sets = [set_assoc(), set_outliers(), set_judge(), set_predict(), set_reason()]
    balance(sets, R)
    unit = {
        "slug": "scatter-plots",
        "title": "Scatter Plots and Lines of Best Fit",
        "seo_title": "Grade 8 Scatter Plots Worksheets: Association, Outliers, Line of Best Fit and Predictions",
        "short_title": "Scatter plots",
        "domain": "Statistics & Probability",
        "standard_code": "8.SP.A.1",
        "standard_url": "https://www.thecorestandards.org/Math/Content/8/SP/A/1/",
        "standard_text": "Construct and interpret scatter plots for bivariate measurement data to investigate patterns of association between two quantities. Describe patterns such as clustering, outliers, positive or negative association, linear association, and nonlinear association.",
        "meta_desc": "Free Grade 8 scatter plot worksheets: describe positive, negative and no association, linear or nonlinear patterns, find outliers and clusters, judge a line of best fit, and use its equation to predict. 100 questions with an answer key.",
        "key_big": "Points going up show positive association; going down, negative; no pattern, none.",
        "key_sub": "A line of best fit follows the trend. Use its equation to predict, and read its slope as a rate.",
        "body_html": body(),
        "faq": [
            {"q": "What does a scatter plot show?", "a": "It shows pairs of data as points so you can see if two variables are related: positive, negative or no association."},
            {"q": "How do you draw a line of best fit?", "a": "Draw a straight line that follows the trend, close to most points, with about as many points above it as below it."},
            {"q": "What is an outlier in a scatter plot?", "a": "A point that is far away from the pattern of the other points."},
            {"q": "Does a strong association mean one thing causes the other?", "a": "No. Two things can be related because of a third factor. Association is not cause."}],
        "sets": sets, "pdf_url": "", "sort": 15, "updated": UPDATED,
    }
    write_unit("us", "math", "grade-8", unit)


if __name__ == "__main__":
    main()
