# -*- coding: utf-8 -*-
"""
UK Year 9 Maths: Scatter Graphs and Correlation (KS3 Statistics)
  python3 tools/gen_uk_maths_y9_scatter_graphs_and_correlation.py
Describing correlation (positive, negative, none; strong or weak), correlation in context, using a line of best
fit to estimate, outliers, interpolation and extrapolation, and correlation versus causation.
Wrong answers come from real mistakes: mixing up positive and negative, calling weak correlation "none",
reading the wrong axis, trusting estimates far outside the data, and saying correlation proves cause.
"""
import random
from uk_ks3 import num, B, S, make, lesson, collect, T, QN, svg_wrap, line, text, fig, INK, RED, BLUE, FONT

R = random.Random(91201)
U = 26
L, TOP = 58, 14

# name, x0, xstep, xlabel, y0, ystep, ylabel, sign
CTX = [
    ("revision", 0, 1, "Hours of revision", 0, 10, "Test score (%)", 1),
    ("ice", 10, 2, "Temperature (°C)", 0, 20, "Ice creams sold", 1),
    ("car", 0, 1, "Age of car (years)", 0, 2, "Value (£1,000s)", -1),
    ("height", 140, 5, "Height (cm)", 140, 5, "Arm span (cm)", 1),
    ("tv", 0, 1, "Hours of TV per day", 0, 0.5, "Hours of homework", -1),
    ("cocoa", 0, 3, "Temperature (°C)", 0, 10, "Hot chocolates sold", -1),
    ("run", 0, 2, "Training (hours per week)", 10, 1, "5 km time (minutes)", -1),
    ("plant", 0, 2, "Fertiliser (g)", 0, 5, "Plant height (cm)", 1),
    ("shoe", 2, 1, "Shoe size", 0, 10, "Maths score (%)", 0),
    ("birth", 1, 3, "Day of birth", 140, 5, "Height (cm)", 0),
]


# name -> (x name, x format, y name, y format)
FMT = {
    "revision": ("hours of revision", "%s hours", "test score", "%s%%"),
    "ice": ("temperature", "%s°C", "number of ice creams sold", "%s"),
    "car": ("age of the car", "%s years", "value", "£%s,000"),
    "height": ("height", "%s cm", "arm span", "%s cm"),
    "tv": ("TV time", "%s hours per day", "homework time", "%s hours"),
    "cocoa": ("temperature", "%s°C", "number of hot chocolates sold", "%s"),
    "run": ("training time", "%s hours per week", "5 km time", "%s minutes"),
    "plant": ("amount of fertiliser", "%s g", "plant height", "%s cm"),
}


def sing(t):
    return t.replace("1 hours", "1 hour").replace("1 years", "1 year").replace("1 minutes", "1 minute") if t.startswith("1 ") else t


def fx(ctx, v):
    return sing(FMT[ctx[0]][1] % num(v))


def fy(ctx, v):
    return sing(FMT[ctx[0]][3] % num(v))


def tick(v):
    return num(v)


def scatter_svg(ctx, pts, bf=None, mark=None, label="scatter graph"):
    _, x0, xs, xl, y0, ys, yl, _ = ctx
    X = lambda u: L + u * U
    Y = lambda u: TOP + (10 - u) * U
    s = []
    for i in range(11):
        s.append(line(X(i), Y(0), X(i), Y(10), "#e2e2e2", 1))
        s.append(line(X(0), Y(i), X(10), Y(i), "#e2e2e2", 1))
    s.append(line(X(0), Y(0), X(10) + 6, Y(0), INK, 2))
    s.append(line(X(0), Y(0), X(0), Y(10) - 6, INK, 2))
    for i in range(0, 11, 2):
        s.append(text(X(i), Y(0) + 16, tick(x0 + xs * i), 11, weight=400))
        s.append(text(X(0) - 6, Y(i) + 4, tick(y0 + ys * i), 11, weight=400, anchor="end"))
    s.append(text(X(5), Y(0) + 36, xl, 13))
    s.append("<text x='14' y='%d' font-size='13' font-weight='700' fill='%s' text-anchor='middle' transform='rotate(-90 14 %d)'>%s</text>"
             % (Y(5), INK, Y(5), yl))
    if bf:
        (a, b) = bf
        s.append(line(X(0), Y(a), X(10), Y(b), RED, 2.5))
    for (x, y) in pts:
        s.append("<path d='M%.1f %.1f l8 8 M%.1f %.1f l-8 8' stroke='%s' stroke-width='2'/>" % (X(x) - 4, Y(y) - 4, X(x) + 4, Y(y) - 4, BLUE))
    if mark:
        x, y = mark
        s.append("<circle cx='%.1f' cy='%.1f' r='9' fill='none' stroke='%s' stroke-width='2'/>" % (X(x), Y(y), RED))
    return svg_wrap(L + 10 * U + 16, TOP + 10 * U + 46, "".join(s), label)


def make_pts(r, kind, n=12):
    """kind: 'sp' strong +, 'wp' weak +, 'sn', 'wn', 'no'."""
    pts = []
    for _ in range(400):
        x = r.randint(1, 18) / 2.0
        if kind == "no":
            y = r.randint(2, 18) / 2.0
        else:
            m = 0.8 if kind[1] == "p" else -0.8
            c = 1.0 if m > 0 else 9.0
            noise = 0.6 if kind[0] == "s" else 2.2
            y = m * x + c + r.uniform(-noise, noise)
            y = round(y * 2) / 2.0
        if 0.5 <= y <= 9.5 and all(abs(x - p) + abs(y - q) > 0.6 for p, q in pts):
            pts.append((x, y))
        if len(pts) == n:
            break
    return pts


NAMES = {"sp": "Strong positive correlation", "wp": "Weak positive correlation", "sn": "Strong negative correlation",
         "wn": "Weak negative correlation", "no": "No correlation"}


# ------------------------------------------------------------ set 1: describing correlation from a graph
def one_desc(r):
    kind = r.choice(["sp", "wp", "sn", "wn", "no"])
    ctx = r.choice([c for c in CTX if (c[7] == 0) == (kind == "no") and (kind == "no" or (c[7] > 0) == (kind[1] == "p"))])
    pts = make_pts(r, kind)
    q = fig(scatter_svg(ctx, pts)) + "Describe the correlation shown."
    right = NAMES[kind]
    flip = {"sp": "sn", "sn": "sp", "wp": "wn", "wn": "wp"}
    if kind == "no":
        wr = [NAMES["wp"], NAMES["wn"], NAMES["sp"]]
        e = "The points are scattered with no pattern: <b>no correlation</b>."
    else:
        wr = [NAMES[flip[kind]], NAMES[("w" if kind[0] == "s" else "s") + kind[1]], NAMES["no"]]
        e = "As the %s goes up, the %s goes %s, so it is %s. The points are %s a straight line, so it is <b>%s</b>." % (
            FMT[ctx[0]][0], FMT[ctx[0]][2], "up" if kind[1] == "p" else "down",
            "positive" if kind[1] == "p" else "negative", "close to" if kind[0] == "s" else "spread out around", right.lower())
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 2: correlation in context
CONTEXTS = [
    ("the outside temperature and the number of ice creams sold", "Positive"),
    ("the outside temperature and the number of coats sold", "Negative"),
    ("the age of a car and its value", "Negative"),
    ("a person's height and their arm span", "Positive"),
    ("a person's shoe size and their favourite number", "None"),
    ("the number of hours of revision and the test score", "Positive"),
    ("the distance a taxi travels and the fare", "Positive"),
    ("the number of people sharing a pizza and the amount each person gets", "Negative"),
    ("the speed of a car and the time taken for a journey", "Negative"),
    ("a person's house number and their height", "None"),
    ("the amount of rainfall and the number of umbrellas sold", "Positive"),
    ("the number of hours of daylight and electricity used for lighting", "Negative"),
    ("the engine size of a car and the miles it can go per litre", "Negative"),
    ("the number of pages in a book and its weight", "Positive"),
    ("the day of the month a person was born and their test score", "None"),
    ("the altitude of a mountain town and its average temperature", "Negative"),
    ("the price of a train ticket and the distance travelled", "Positive"),
    ("a student's hair length and their maths score", "None"),
    ("the number of hours spent gaming and the hours of sleep", "Negative"),
    ("the age of a child and their reading age", "Positive"),
]


def context_set():
    its = []
    for c, ans in CONTEXTS:
        q = "What type of correlation would you expect between %s?" % c
        e = {"Positive": "As one goes up, the other tends to go up: <b>positive</b>.",
             "Negative": "As one goes up, the other tends to go down: <b>negative</b>.",
             "None": "There is no reason for these to be linked: <b>no correlation</b>."}[ans]
        its.append(T(q, ans if ans != "None" else "No correlation", [w for w in ["Positive", "Negative", "No correlation", "Exactly zero, always"] if w != (ans if ans != "None" else "No correlation")][:3], e))
    return its


# ------------------------------------------------------------ set 3: using a line of best fit
def one_bf(r):
    ctx = r.choice([c for c in CTX if c[7] != 0])
    sg = ctx[7]
    a = r.randint(0, 3) if sg > 0 else r.randint(7, 10)
    b = a + sg * r.choice([5, 5, 5])
    b = a + sg * 5 if sg > 0 else a - 5
    pts = []
    for _ in range(300):
        x = r.randint(1, 19) / 2.0
        y = a + (b - a) * x / 10.0 + r.uniform(-0.8, 0.8)
        y = round(y * 2) / 2.0
        if 0.5 <= y <= 9.5 and all(abs(x - p) + abs(y - q) > 0.6 for p, q in pts):
            pts.append((x, y))
        if len(pts) == 11:
            break
    _, x0, xs, xl, y0, ys, yl, _ = ctx
    if r.random() < 0.6:
        xu = r.choice([2, 4, 6, 8])
        yu = a + (b - a) * xu / 10
        xv, yv = x0 + xs * xu, y0 + ys * yu
        q = fig(scatter_svg(ctx, pts, (a, b))) + "Use the line of best fit to estimate the %s when the %s is %s." % (
            FMT[ctx[0]][2], FMT[ctx[0]][0], fx(ctx, xv))
        wrongs = [y0 + ys * (yu + 1), y0 + ys * (yu - 1), y0 + ys * xu if xu != yu else y0 + ys * (yu + 2)]
        right = fy(ctx, yv)
        e = "Go up from %s on the horizontal axis to the line, then across: about <b>%s</b>." % (num(xv), right)
        return T(q, right, [fy(ctx, w) for w in dict.fromkeys(wrongs) if w != yv][:3], e)
    yu = r.choice([v for v in range(1, 10) if (v - a) * 10 % (b - a) == 0 and 0 < (v - a) * 10 // (b - a) < 10])
    xu = (yu - a) * 10 // (b - a)
    xv, yv = x0 + xs * xu, y0 + ys * yu
    q = fig(scatter_svg(ctx, pts, (a, b))) + "Use the line of best fit to estimate the %s when the %s is %s." % (
        FMT[ctx[0]][0], FMT[ctx[0]][2], fy(ctx, yv))
    right = fx(ctx, xv)
    e = "Go across from %s on the vertical axis to the line, then down: about <b>%s</b>." % (num(yv), right)
    wrongs = [x0 + xs * (xu + 1), x0 + xs * (xu - 1), x0 + xs * yu if yu != xu else x0 + xs * (xu + 2)]
    return T(q, right, [fx(ctx, w) for w in dict.fromkeys(wrongs) if w != xv][:3], e)


# ------------------------------------------------------------ set 4: outliers and reliability
def one_out(r):
    ctx = r.choice([c for c in CTX if c[7] != 0])
    kind = "sp" if ctx[7] > 0 else "sn"
    pts = make_pts(r, kind, 11)
    _, x0, xs, xl, y0, ys, yl, _ = ctx
    for _ in range(100):
        ox = r.randint(2, 8)
        oy = r.randint(1, 9)
        line_y = 0.8 * ox + 1 if kind == "sp" else -0.8 * ox + 9
        if abs(oy - line_y) >= 4 and all(abs(ox - p) + abs(oy - q) > 1 for p, q in pts):
            break
    else:
        return None
    allp = pts + [(ox, oy)]
    if r.random() < 0.6:
        q = fig(scatter_svg(ctx, allp)) + "One point does not fit the pattern. What are its values?"
        P = lambda xu_, yu_: "%s and %s" % (fx(ctx, x0 + xs * xu_), fy(ctx, y0 + ys * yu_))
        right = P(ox, oy)
        wr = [P(oy, ox), P(ox, oy + (2 if oy < 8 else -2)), P(ox + 1, oy)]
        e = "The point far from the others is an <b>outlier</b>: <b>%s</b>." % right
        if ox == oy:
            return None
        return T(q, right, wr, e)
    if ctx[0] == "tv":
        return None
    xv = x0 + xs * r.choice([12, 13, 14])
    q = fig(scatter_svg(ctx, pts)) + "Jack uses this graph to estimate the %s when the %s is %s. Is his estimate reliable?" % (
        FMT[ctx[0]][2], FMT[ctx[0]][0], fx(ctx, xv))
    right = "No, it is outside the range of the data"
    wr = ["Yes, the correlation is strong", "Yes, any value can be estimated", "No, because there is no correlation"]
    e = "%s is beyond the data shown. Estimating outside the data (extrapolation) is <b>not reliable</b>." % num(xv)
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 5: problems
def problems():
    data = [
        ("A line of best fit should…", "follow the trend, with about the same number of points on each side", ["go through the first and last points", "go through the origin", "join every point"],
         "A line of best fit shows the trend. It does not have to go through any particular point: <b>about the same number of points on each side</b>."),
        ("When is it reliable to use a line of best fit to estimate?", "When the value is inside the range of the data", ["When the value is far outside the data", "Always", "Only when there is no correlation"],
         "Estimating inside the data (interpolation) is reliable. <b>When the value is inside the range of the data.</b>"),
        ("Ice cream sales and sunburn cases show positive correlation. Does eating ice cream cause sunburn?", "No, both are caused by hot sunny weather", ["Yes, the correlation proves it", "Yes, because both go up", "No, because the correlation is negative"],
         "Correlation does not prove cause. <b>Both are caused by hot sunny weather.</b>"),
        ("What does strong negative correlation mean?", "As one variable increases, the other decreases, and the points are close to a line", ["Both variables decrease", "There is no link", "As one increases, the other increases"],
         "<b>As one variable increases, the other decreases, and the points are close to a line.</b>"),
        ("What is an outlier?", "A value that does not fit the pattern of the rest", ["The biggest value", "The first point plotted", "The point on the line of best fit"],
         "<b>A value that does not fit the pattern of the rest.</b> It may be a mistake or an unusual case."),
        ("Which pair of variables would most likely show no correlation?", "The last digit of a phone number and running speed", ["Height and weight", "Age and value of a phone", "Distance and taxi fare"],
         "There is no reason for these to be linked: <b>the last digit of a phone number and running speed</b>."),
        ("A scatter graph of hours worked and pay shows strong positive correlation. Which statement is correct?", "People who work more hours tend to earn more", ["Everyone earns the same", "People who work more hours earn less", "Pay does not depend on hours"],
         "Positive correlation: <b>people who work more hours tend to earn more</b>."),
        ("What is the name for estimating a value inside the range of the data?", "Interpolation", ["Extrapolation", "Correlation", "Causation"],
         "Inside the data is <b>interpolation</b>. Outside is extrapolation."),
        ("What is the name for estimating a value outside the range of the data?", "Extrapolation", ["Interpolation", "Correlation", "An outlier"],
         "Outside the data is <b>extrapolation</b>, which can be unreliable."),
        ("A graph of age and value of cars has a line of best fit. Why can't it be used for a 40-year-old classic car?", "Classic cars may go up in value, and 40 years is outside the data", ["Old cars have no value", "The line goes through the origin", "Classic cars are outliers so the line is wrong"],
         "<b>40 years is outside the data</b>, and classic cars may behave differently."),
        ("A line of best fit goes through (2, 30) and (6, 50). What is its gradient?", "5", ["20", "4", "10"],
         "(50 − 30) ÷ (6 − 2) = 20 ÷ 4 = <b>5</b>."),
        ("A line of best fit has gradient −2 and goes through (0, 40). Estimate <i>y</i> when <i>x</i> = 5.", "30", ["50", "38", "10"],
         "40 − 2 × 5 = <b>30</b>."),
        ("Which of these shows the weakest correlation?", "Points widely spread with a slight upward trend", ["Points close to a rising straight line", "Points close to a falling straight line", "Points exactly on a line"],
         "Weak correlation means the points are widely spread: <b>points widely spread with a slight upward trend</b>."),
        ("Grace says: 'There is negative correlation, so one variable causes the other to fall.' Why is she wrong?", "Correlation does not prove causation", ["Negative correlation means no link", "She should say positive", "Causation needs an outlier"],
         "A link in the data does not prove that one causes the other. <b>Correlation does not prove causation.</b>"),
        ("Which graph type is used to look for a relationship between two numerical variables?", "A scatter graph", ["A pie chart", "A bar chart", "A pictogram"],
         "Plotting pairs of values as points: <b>a scatter graph</b>."),
        ("Why might an outlier be removed before drawing a line of best fit?", "It may be a mistake and would pull the line away from the trend", ["Outliers are always the most important", "It makes the correlation negative", "It is the biggest value"],
         "<b>It may be a mistake and would pull the line away from the trend.</b> Only remove it if there is a good reason."),
        ("A survey finds that towns with more libraries have more crime. What is the most likely explanation?", "Bigger towns have more of both", ["Libraries cause crime", "Crime causes libraries", "It is negative correlation"],
         "Both depend on population: <b>bigger towns have more of both</b>."),
        ("On a scatter graph, temperature is plotted against heating cost. What correlation would you expect?", "Negative", ["Positive", "No correlation", "Perfect positive"],
         "Warmer weather means less heating: <b>negative</b>."),
        ("A line of best fit predicts a test score of 120% for 30 hours of revision. What does this show?", "Extrapolating far beyond the data gives impossible answers", ["The student will score 120%", "The line is perfect", "There is no correlation"],
         "Scores cannot be over 100%. <b>Extrapolating far beyond the data gives impossible answers.</b>"),
        ("Which is the best description of 'no correlation'?", "There is no linear relationship between the variables", ["Both variables are zero", "The points form a straight line", "The variables are the same"],
         "<b>There is no linear relationship between the variables.</b>"),
    ]
    return [T(q, a[0].upper() + a[1:], [w[0].upper() + w[1:] for w in ws], e) for q, a, ws, e in data]


def body():
    return lesson(
        "<p>A <b>scatter graph</b> plots pairs of values to show if two variables are linked. "
        "<b>Positive correlation</b>: as one goes up, the other goes up. <b>Negative correlation</b>: as one goes up, the other goes down. "
        "<b>No correlation</b>: no pattern. Points close to a line show <b>strong</b> correlation; spread-out points show <b>weak</b> correlation.</p>"
        "<p>A <b>line of best fit</b> follows the trend. Use it to estimate values <b>inside</b> the data (interpolation). "
        "Estimates <b>outside</b> the data (extrapolation) are less reliable. Correlation does not prove that one thing causes the other.</p>",
        [("Revision hours and test scores rise together.", ["As one rises, so does the other."], "Positive correlation"),
         ("Estimate a score for 4 hours.", ["Go up from 4 to the line, then across."], "Read the value on the y-axis"),
         ("A point far from the others.", ["It does not fit the pattern."], "An outlier")],
        ["Mixing up positive and negative correlation.",
         "Saying 'no correlation' when the correlation is weak.",
         "Reading the wrong axis when using the line of best fit.",
         "Saying that correlation proves one thing causes another."])


def main():
    sets = [S("Describing correlation", collect(one_desc, 20, R)),
            S("Correlation in real life", context_set()),
            S("Using a line of best fit", collect(one_bf, 20, R)),
            S("Outliers and reliable estimates", collect(one_out, 20, R)),
            S("Scatter graph problems", problems())]
    make(9, "scatter-graphs-and-correlation", 12, "S",
         "Scatter Graphs and Correlation",
         "Year 9 Scatter Graphs Worksheets: Correlation, Lines of Best Fit and Outliers",
         "Scatter Graphs",
         "Use and interpret scatter graphs of bivariate data; recognise correlation.",
         "Free Year 9 scatter graph worksheets: describe positive, negative and no correlation, use a line of best fit to "
         "estimate, find outliers, and correlation vs causation. 100 questions with answers.",
         "Positive: both go up. Negative: one goes up, the other goes down.",
         "Use a line of best fit only to estimate inside the data.",
         body(),
         [("What is a scatter graph?", "A graph that plots pairs of values as points to show whether two variables are related."),
          ("What are the types of correlation?", "Positive (both increase), negative (one increases while the other decreases) and none. Correlation can also be strong or weak."),
          ("How do I draw a line of best fit?", "Draw a straight line that follows the trend, with roughly the same number of points on each side. It does not have to go through the origin."),
          ("Does correlation mean causation?", "No. Two things can be linked because a third thing affects both, such as hot weather increasing both ice cream sales and sunburn.")],
         sets, R)


if __name__ == "__main__":
    main()
