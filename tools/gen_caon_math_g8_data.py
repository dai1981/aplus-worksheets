# -*- coding: utf-8 -*-
"""
Ontario Grade 8 Math: Scatter plots and data (Ontario Curriculum 2020, Grade 8: Data, D1.1, D1.3, D1.5, D1.6)
  python3 tools/gen_caon_math_g8_data.py
One- and two-variable data, reading scatter plots, describing relationships (strong or weak, positive,
negative or none), outliers and predictions from a line of best fit, and misleading graphs and conclusions
(correlation is not causation, scales that do not start at 0, small or biased samples, predictions far outside the data).
Wrong answers come from real student mistakes: treating many values as two variables, swapping x and y,
reading the neighbouring grid line or the axis start, “steep” taken for “strong”, “going down” taken for
“no relationship”, the highest point taken for the outlier, a line of best fit that must pass through (0, 0)
or join the end points, and a strong relationship taken as proof of cause.
Helpers adapted from gen_caon_math_g6_data.py and gen_caon_math_g7_proportional.py.
Canadian English, real minus sign, no-break space in 5+ digit numbers, single-quoted HTML attributes.
"""
import json, re, math, os, random
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-8")
UPDATED = "2026-11-02"
GREEN = "#006633"
BAR = "#2e8b57"
ORANGE = "#d9822b"
INK = "#2b2b2b"
GRID = "#d5ddd8"
GRID2 = "#9fb0a5"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
NBSP = " "


# ------------------------------------------------------------ helpers
def num(x):
    """Ontario style: 4536, 10 000 (no-break space), −3."""
    x = F(x)
    assert x.denominator == 1, x
    v = abs(x.numerator)
    s = str(v)
    if len(s) >= 5:
        s = "{:,}".format(v).replace(",", NBSP)
    return (MINUS if x < 0 else "") + s


def fmt(x):
    x = F(x)
    if x.denominator == 1:
        return num(x)
    for k in (1, 2, 3):
        y = x * 10 ** k
        if y.denominator == 1:
            v = abs(y.numerator)
            s = str(v).rjust(k + 1, "0")
            return (MINUS if x < 0 else "") + num(int(s[:-k])) + "." + s[-k:]
    raise AssertionError(x)


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def mcq(q, right, wrongs, e, fix=None):
    """Correct answer first; balance() moves it. fix: picture labels keep A–D order, answer at index fix."""
    ch = [right] + list(wrongs)
    assert len(ch) == 4 and len({plain(c) for c in ch}) == 4, (q, ch)
    if fix is not None:
        order = sorted(ch, key=plain)
        assert order[fix] == right, (q, order, fix)
        return {"q": q, "c": order, "a": fix, "e": e, "fix": True}
    return {"q": q, "c": ch, "a": 0, "e": e}


def mcqv(q, right, wrongs, f, e):
    """Choices given as values: equal values are not allowed."""
    seen = [F(right)]
    for w in wrongs:
        assert F(w) not in seen, (q, right, wrongs)
        seen.append(F(w))
    return mcq(q, f(right), [f(w) for w in wrongs], e)


def stats(p):
    """Correlation r, slope and intercept of the least-squares line (used only to check the data)."""
    n = len(p)
    mx = sum(a for a, b in p) / n
    my = sum(b for a, b in p) / n
    sxy = sum((a - mx) * (b - my) for a, b in p)
    sxx = sum((a - mx) ** 2 for a, b in p)
    syy = sum((b - my) ** 2 for a, b in p)
    return sxy / math.sqrt(sxx * syy), sxy / sxx, my - sxy / sxx * mx


KINDS = {"sp": (0.9, 1.0), "wp": (0.4, 0.72), "sn": (-1.0, -0.9), "wn": (-0.72, -0.4), "no": (-0.05, 0.05)}


def check_kind(p, kind):
    lo, hi = KINDS[kind]
    r = stats([(float(a), float(b)) for a, b in p])[0]
    assert lo <= r <= hi, (kind, r, p)


def cloud(rnd, kind, n=13):
    """Points in a 10 × 10 box with the wanted kind of relationship (checked with r), not too close together."""
    lo, hi = KINDS[kind]
    for _ in range(5000):
        p = []
        while len(p) < n:
            x = rnd.uniform(0.6, 9.4)
            if kind == "no":
                y = rnd.uniform(0.8, 9.2)
            else:
                s = 1 if kind in ("sp", "wp") else -1
                sd = 0.45 if kind in ("sp", "sn") else 1.7
                y = 5 + s * 0.8 * (x - 5) + rnd.gauss(0, sd)
            if not 0.5 <= y <= 9.5:
                continue
            if any((x - a) ** 2 + (y - b) ** 2 < 0.55 ** 2 for a, b in p):
                continue
            p.append((round(x, 2), round(y, 2)))
        r = stats(p)[0]
        if lo <= r <= hi:
            return p
    raise AssertionError(kind)


# ------------------------------------------------------------ svg
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs, bold=False):
    return len(str(t)) * fs * (0.62 if bold else 0.58)


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK, extra=""):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, extra, t))


def line(x1, y1, x2, y2, col=INK, w=1, extra=""):
    return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%s'%s/>"
            % (x1, y1, x2, y2, col, w, extra))


def clip_line(m, b, x0, x1, y0, y1):
    """The part of y = mx + b inside the box [x0, x1] × [y0, y1]."""
    m, b = F(m), F(b)
    pts = []
    for x in (x0, x1):
        y = m * x + b
        if y0 <= y <= y1:
            pts.append((F(x), y))
    if m != 0:
        for y in (y0, y1):
            x = (y - b) / m
            if x0 <= x <= x1:
                pts.append((x, F(y)))
    pts = sorted(set(pts))
    assert len(pts) >= 2, (m, b)
    return pts[0], pts[-1]


def scatter_svg(title, xname, yname, pts, xr, yr, gx, gy, labels=None, fit=None):
    """Scatter plot. xr, yr = (min, max, grid step, label step). gx, gy = pixels per grid step.
    labels: letters next to the points. fit: (m, b) of a line of best fit, drawn in orange."""
    fs = 14
    xmin, xmax, xs, xl = [F(v) for v in xr]
    ymin, ymax, ys, yl = [F(v) for v in yr]
    for a, b in pts:
        assert xmin <= a <= xmax and ymin <= b <= ymax, (a, b)
    nx, ny = int((xmax - xmin) / xs), int((ymax - ymin) / ys)
    pw, ph = nx * gx, ny * gy
    ylabs = [ymin + k * ys for k in range(ny + 1) if (ymin + k * ys) % yl == 0]
    x0 = 24 + max(tw(fmt(v), fs) for v in ylabs) + 6
    y0 = 34
    yb = y0 + ph
    rpad = 14 + (16 if labels else 0)
    W = max(x0 + pw + rpad, tw(title, 16, True) + 16)
    s = [text(W / 2, 18, title, 16, bold=True)]
    X = lambda a: x0 + float((F(a) - xmin) / xs) * gx
    Y = lambda b: yb - float((F(b) - ymin) / ys) * gy
    for k in range(nx + 1):
        v = xmin + k * xs
        major = v % xl == 0
        s.append(line(X(v), y0, X(v), yb, GRID2 if major else GRID))
        if major:
            s.append(text(X(v), yb + 20, fmt(v), fs))
    for k in range(ny + 1):
        v = ymin + k * ys
        major = v % yl == 0
        s.append(line(x0, Y(v), x0 + pw, Y(v), GRID2 if major else GRID))
        if major:
            s.append(text(x0 - 5, Y(v) + 5, fmt(v), fs, anchor="end"))
    s.append("<path d='M%.1f %.1f V%.1f H%.1f' fill='none' stroke='%s' stroke-width='2'/>"
             % (x0, y0 - 6, yb, x0 + pw + 6, INK))
    if fit:
        (a1, b1), (a2, b2) = clip_line(fit[0], fit[1], xmin, xmax, ymin, ymax)
        s.append(line(X(a1), Y(b1), X(a2), Y(b2), ORANGE, 2.5))
    for i, (a, b) in enumerate(pts):
        s.append("<circle cx='%.1f' cy='%.1f' r='5' fill='%s' stroke='#ffffff' stroke-width='1.2'/>" % (X(a), Y(b), GREEN))
        if labels and labels[i]:
            s.append(text(X(a) + 8, Y(b) - 6, labels[i], fs, anchor="start", bold=True))
    s.append(text(x0 + pw / 2, yb + 40, xname, fs, bold=True))
    mid = y0 + ph / 2
    assert tw(yname, fs, True) < ph + 30, (yname, ph)
    s.append(text(13, mid, yname, fs, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % mid))
    return svg_wrap(W, yb + 48, "".join(s), "scatter plot: " + title.lower().replace("’", ""))


def panels_svg(groups, names=None, fits=None, label="four scatter plots"):
    """Small scatter plots side by side (x and y from 0 to 10, no numbers). Names under the letters."""
    U, N = 12, 10
    PL, PT, PB, PR, GAP = 8, 26, 10, 8, 16
    if names:
        PB = 30
    PW = PL + U * N + PR
    if names:
        PW = max(PW, max(tw(nm, 14) for nm in names) + 6)
    k = len(groups)
    W = 4 + k * PW + (k - 1) * GAP
    H = PT + U * N + PB
    s = []
    for i, pts in enumerate(groups):
        ox = 2 + i * (PW + GAP)
        X0 = ox + (PW - U * N) / 2
        Y0 = PT + U * N
        s.append(text(X0 + U * N / 2, 18, "Graph " + "ABCD"[i], 15, bold=True, col=GREEN))
        for g in range(0, N + 1, 2):
            s.append(line(X0 + g * U, PT, X0 + g * U, Y0, GRID))
            s.append(line(X0, Y0 - g * U, X0 + N * U, Y0 - g * U, GRID))
        s.append("<path d='M%.1f %.1f V%.1f H%.1f' fill='none' stroke='%s' stroke-width='2'/>"
                 % (X0, PT - 4, Y0, X0 + N * U + 4, INK))
        if fits and fits[i] is not None:
            (a1, b1), (a2, b2) = clip_line(fits[i][0], fits[i][1], 0, N, 0, N)
            s.append(line(X0 + float(a1) * U, Y0 - float(b1) * U, X0 + float(a2) * U, Y0 - float(b2) * U, ORANGE, 2.5))
        for a, b in pts:
            assert 0 < a < N and 0 < b < N
            s.append("<circle cx='%.1f' cy='%.1f' r='3.8' fill='%s'/>" % (X0 + a * U, Y0 - b * U, GREEN))
        if names:
            s.append(text(X0 + U * N / 2, Y0 + 22, names[i], 14))
    return svg_wrap(W, H, "".join(s), label)


def bar_svg(title, cat_axis, val_axis, cats, vals, ymin, ymax, gstep, lstep, gy=14, bw=44, slot=110, lab=num):
    """Bar graph. The scale runs from ymin (which may not be 0) to ymax."""
    fs = 14
    assert all(ymin <= v <= ymax for v in vals) and (ymax - ymin) % lstep == 0 and lstep % gstep == 0
    nt = (ymax - ymin) // gstep
    ph = nt * gy
    x0 = 24 + max(tw(lab(ymax), fs), tw(lab(ymin), fs)) + 6
    slot = max(slot, max(tw(c, fs) for c in cats) + 14)
    pw = slot * len(cats)
    y0 = 34
    yb = y0 + ph
    W = max(x0 + pw + 8, tw(title, 16, True) + 16)
    s = [text(W / 2, 18, title, 16, bold=True)]
    for k in range(nt + 1):
        v = ymin + k * gstep
        y = yb - k * gy
        major = (v - ymin) % lstep == 0
        s.append(line(x0, y, x0 + pw, y, GRID2 if major else GRID))
        if major:
            s.append(text(x0 - 5, y + 5, lab(v), fs, anchor="end"))
    for i, (c, v) in enumerate(zip(cats, vals)):
        cx = x0 + slot * i + slot / 2
        h = (v - ymin) / float(gstep) * gy
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s'/>" % (cx - bw / 2, yb - h, bw, h, BAR))
        s.append(text(cx, yb + 18, c, fs))
    s.append("<path d='M%.1f %d V%.1f H%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0 - 6, yb, x0 + pw, INK))
    s.append(text(x0 + pw / 2, yb + 38, cat_axis, fs, bold=True))
    mid = y0 + ph / 2
    assert tw(val_axis, fs, True) < ph + 30
    s.append(text(13, mid, val_axis, fs, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % mid))
    return svg_wrap(W, yb + 46, "".join(s), "bar graph: " + title.lower())


def bline_svg(title, x_axis, y_axis, xlabels, vals, ymin, ymax, gstep, lstep, gy=12, slot=64, lab=num):
    """Broken-line graph: points joined by straight line segments."""
    fs = 14
    assert (ymax - ymin) % lstep == 0 and lstep % gstep == 0 and all(ymin <= v <= ymax for v in vals)
    nt = (ymax - ymin) // gstep
    ph = nt * gy
    x0 = 24 + max(tw(lab(ymax), fs), tw(lab(ymin), fs)) + 6
    pw = slot * len(xlabels)
    y0 = 34
    yb = y0 + ph
    W = max(x0 + pw + 8, tw(title, 16, True) + 16)
    s = [text(W / 2, 18, title, 16, bold=True)]
    for k in range(nt + 1):
        v = ymin + k * gstep
        y = yb - k * gy
        major = (v - ymin) % lstep == 0
        s.append(line(x0, y, x0 + pw, y, GRID2 if major else GRID))
        if major:
            s.append(text(x0 - 5, y + 5, lab(v), fs, anchor="end"))
    for i, c in enumerate(xlabels):
        x = x0 + slot * i + slot / 2
        s.append(line(x, yb, x, yb + 5, INK, 1.5))
        s.append(text(x, yb + 20, c, fs))
    pts = [(x0 + slot * i + slot / 2, yb - (v - ymin) / float(gstep) * gy) for i, v in enumerate(vals)]
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='2.5'/>"
             % (" ".join("%.1f,%.1f" % p for p in pts), GREEN))
    for a, b in pts:
        s.append("<circle cx='%.1f' cy='%.1f' r='4.5' fill='%s'/>" % (a, b, GREEN))
    s.append("<path d='M%.1f %d V%.1f H%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0 - 6, yb, x0 + pw, INK))
    s.append(text(x0 + pw / 2, yb + 40, x_axis, fs, bold=True))
    mid = y0 + ph / 2
    assert tw(y_axis, fs, True) < ph + 30
    s.append(text(13, mid, y_axis, fs, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % mid))
    return svg_wrap(W, yb + 48, "".join(s), "broken-line graph: " + title.lower())


# ------------------------------------------------------------ data
# A: study time and test score (strong positive), line of best fit y = 6x + 44
STUDY = [(1, 50), (2, 60), (2, 55), (3, 60), (4, 70), (5, 70), (5, 80), (6, 80), (7, 90), (8, 90)]
STUDY_FIT = (6, 44)
# B: height and arm span of six students, labelled A to F
ARM = [(145, 150), (150, 145), (155, 160), (165, 165), (170, 175), (175, 180)]
ARM_L = ["A", "B", "C", "D", "E", "F"]
# C: temperature and cups of hot chocolate sold at an outdoor rink (strong negative), line y = 30 − 2x
COCOA = [(-15, 60), (-12, 60), (-10, 50), (-8, 50), (-7, 40), (-4, 35), (-2, 35), (0, 30), (2, 30), (4, 20), (5, 20)]
COCOA_FIT = (-2, 30)
# D: distance from school and travel time, with one outlier (3, 45)
TRAVEL = [(1, 5), (2, 10), (2, 15), (3, 15), (4, 20), (5, 20), (6, 25), (7, 30), (8, 35), (3, 45)]
# shoe size and math mark (none), screen time and sleep (weak negative), practice and free throws (weak positive)
SHOE = [(5, 82), (6, 64), (6, 90), (7, 71), (7, 58), (8, 86), (8, 67), (9, 75), (9, 92), (10, 61), (10, 79), (11, 80)]
SLEEP = [(F("1"), F("9.5")), (F("1.5"), 8), (2, 10), (2, F("8.5")), (F("2.5"), 9), (3, F("9.5")), (3, F("7.5")),
         (F("3.5"), F("8.5")), (4, 9), (4, F("7.5")), (F("4.5"), 8), (5, F("8.5")), (F("5.5"), F("7.5")), (6, 8)]
THROWS = [(30, 8), (40, 5), (50, 10), (60, 7), (70, 12), (80, 8), (90, 11), (100, 14), (110, 9), (120, 13),
          (130, 10), (140, 15), (150, 11)]


def study_svg(fit=False):
    return scatter_svg("Study time and test score", "Time spent studying (hours)", "Test score (%)", STUDY,
                       (0, 9, 1, 1), (40, 100, 5, 10), 30, 14, fit=STUDY_FIT if fit else None)


def arm_svg():
    return scatter_svg("Height and arm span", "Height (cm)", "Arm span (cm)", ARM,
                       (140, 185, 5, 10), (140, 185, 5, 10), 26, 18, labels=ARM_L)


def cocoa_svg(fit=False):
    return scatter_svg("Hot chocolate sales at the outdoor rink", "Temperature at noon (°C)", "Cups sold", COCOA,
                       (-16, 6, 1, 5), (0, 70, 5, 10), 14, 14, fit=COCOA_FIT if fit else None)


def travel_svg():
    return scatter_svg("Distance from school and travel time", "Distance (km)", "Time (minutes)", TRAVEL,
                       (0, 9, 1, 1), (0, 50, 5, 10), 30, 14)


def shoe_svg():
    return scatter_svg("Shoe size and math mark", "Shoe size", "Math mark (%)", SHOE,
                       (4, 12, 1, 2), (50, 100, 5, 10), 30, 14)


def sleep_svg():
    return scatter_svg("Screen time and sleep on a school night", "Screen time (hours)", "Sleep (hours)", SLEEP,
                       (0, 7, F(1, 2), 1), (6, 11, F(1, 2), 1), 21, 16)


def throws_svg():
    return scatter_svg("Practice time and free throws made", "Practice per week (minutes)", "Free throws (out of 20)",
                       THROWS, (20, 160, 10, 20), (0, 20, 1, 4), 18, 10)


# ------------------------------------------------------------ set 1: one- and two-variable data
ONE, TWO = "One-variable: one value for each", "Two-variable: a pair of values for each"
W_TWO, W_ONE = "Two-variable: it has many values", "One-variable: it is about one group"


def kind(q, right, e):
    return mcq("Is this one-variable or two-variable data?<br><b>%s</b>" % q, right,
               [k for k in (ONE, TWO, W_TWO, W_ONE) if k != right], e)


def set_variables():
    its = [
        kind("The height of each student in 8B", ONE,
             "Only one thing is recorded about each student: height. Many students give many values, "
             "but it is still one variable."),
        kind("The height and the arm span of each student in 8B", TWO,
             "Two things are recorded about each student, so each student gives a pair: (height, arm span)."),
        kind("The number of goals each player on a hockey team scored this season", ONE,
             "One thing is recorded about each player: the number of goals."),
        kind("The minutes each student practised piano and the mark each one got on the piano exam", TWO,
             "Each student gives a pair of values: (practice time, exam mark). That is two-variable data."),
        kind("The noon temperature and the number of skaters at the outdoor rink on each day in January", TWO,
             "Each day gives a pair: (temperature, number of skaters). Two variables are recorded for each day."),
        kind("The mass of each pumpkin at a Thanksgiving market", ONE,
             "One thing is measured for each pumpkin: its mass."),
        kind("The age and the price of each used car on a dealer’s lot", TWO,
             "Each car gives a pair: (age, price). Two variables are recorded for each car."),
        kind("Each student’s favourite winter sport", ONE,
             "One thing is recorded about each student. It is qualitative (sport names), and it is one variable."),
        mcq("Which question needs <b>two-variable</b> data to answer?", "Do taller students have longer arm spans?",
            ["What is the most common shoe size?", "How tall is a typical Grade 8 student?", "Which sport is most popular?"],
            "To see whether arm span goes with height, you need both values for each student. "
            "The other questions are about one variable."),
        mcq("Which question can be answered with <b>one-variable</b> data?", "What is the median height in 8B?",
            ["Do taller students jump farther?", "Does more sleep go with higher marks?",
             "Do colder days bring more skaters?"],
            "The median height needs only the heights. Each of the other questions compares two variables."),
        mcq("Kai asks, “Do students who live farther from school take longer to get there?” What data should he collect?",
            "Distance and travel time for each student",
            ["Travel time for each student", "Distance for each student", "The mean travel time of the class"],
            "His question links two variables, so he needs both values from every student. "
            "One of them alone cannot show a relationship."),
        mcq("Which graph is best for two-variable data, such as height and arm span?", "Scatter plot",
            ["Histogram", "Circle graph", "Bar graph"],
            "A scatter plot shows each pair as one point, so you can see how the two variables are related. "
            "The other graphs show one variable."),
        mcq("Which graph is best for one variable: the heights of 30 students, grouped into intervals?", "Histogram",
            ["Scatter plot", "Circle graph", "Pictograph"],
            "Height is continuous data, and grouping it into equal intervals makes a histogram. "
            "A scatter plot needs two variables."),
        mcq("On a scatter plot, what does each point show?", "One pair of values, such as one student",
            ["The mean of the data", "One variable only", "The number of students"],
            "Each point is placed using two values: x across and y up. One point = one student (or one day, one car …)."),
        mcq("Maya wants to know if more practice time leads to more free throws made. "
            "Which variable is the <b>independent</b> variable?", "Practice time",
            ["Free throws made", "The number of students", "The time of day"],
            "The independent variable is the one that may cause or explain the change: practice time. "
            "Free throws made depends on it, so it is the dependent variable."),
        mcq("On a scatter plot of practice time and free throws made, where does the independent variable usually go?",
            "On the horizontal (x) axis", ["On the vertical (y) axis", "In the title", "It is not shown"],
            "Put the independent variable (practice time) across, on the x-axis, "
            "and the dependent variable (free throws) up, on the y-axis."),
        mcq("Which data set is two-variable and quantitative (numbers on both)?", "Hours of sleep and test score",
            ["Favourite sport and grade", "Height of each student", "Eye colour and hair colour"],
            "Hours of sleep and test score are both numbers, and there are two of them. Favourite sport and "
            "eye colour are qualitative, and height alone is one variable."),
        mcq("Each student records hours of sleep and the number of goals in a ringette game. Which is true?",
            "Sleep: continuous. Goals: discrete",
            ["Sleep: discrete. Goals: continuous", "Both are discrete", "Both are continuous"],
            "Time is measured and can be 8.5 or 8.75 hours, so it is continuous. Goals are counted in whole numbers, "
            "so they are discrete."),
        mcq("A table shows height (cm): 152, 160, 168 and long jump (cm): 310, 345, 372 for some students. "
            "How many students are in the data?", "3 students", ["6 students", "2 students", "1 student"],
            "Each student gives a pair: (152, 310), (160, 345), (168, 372). That is 3 students, not 6 values. "
            "2 is the number of variables."),
        mcq("Priya asks 40 of the 620 students at her school how much they sleep and how much screen time they have. "
            "What are the 40 students?", "A sample", ["The population", "A variable", "An outlier"],
            "The population is all 620 students. The 40 students she asks are a sample of that population."),
    ]
    return {"title": "One-variable and two-variable data", "items": its}


# ------------------------------------------------------------ set 2: read scatter plots
def set_read():
    its = []
    S = lambda x: "%d students" % x if x != 1 else "1 student"
    f = fig(study_svg())
    its.append(mcqv(f + "How many students are shown on this scatter plot?", len(STUDY), [8, 9, 20], S,
                    "Count the points: there are 10. (8 counts the different hours, and 20 counts both values of every point.)"))
    its.append(mcq(f + "What score did the student who studied 8 hours get?", "90%", ["85%", "95%", "8%"],
                   "Go up from 8 on the x-axis to the point, then across to the y-axis: it is on the 90 line. "
                   "(85% and 95% are one grid line too low or too high, and 8 is the number of hours.)"))
    its.append(mcqv(f + "How many students studied for exactly 2 hours?",
                    sum(1 for a, b in STUDY if a == 2), [1, 3, 4], S,
                    "Above 2 on the x-axis there are 2 points: 55% and 60%."))
    its.append(mcq(f + "What scores did the students who studied 5 hours get?", "70% and 80%",
                   ["75%", "70% only", "80% and 85%"],
                   "There are 2 points above 5 hours: one on the 70 line and one on the 80 line. "
                   "(75% is halfway between them, but no student got it.)"))
    n80 = sum(1 for a, b in STUDY if b >= 80)
    assert n80 == 4 and sum(1 for a, b in STUDY if b > 80) == 2
    its.append(mcqv(f + "How many students scored 80% or more?", n80, [2, 3, 6], S,
                    "Points on or above the 80 line: (5, 80), (6, 80), (7, 90), (8, 90). That is 4. "
                    "(2 leaves out the points on the 80 line, and 6 counts the students below 80%.)"))
    n4 = sum(1 for a, b in STUDY if a < 4)
    assert n4 == 4
    its.append(mcqv(f + "How many students studied for less than 4 hours?", n4, [3, 5, 6], S,
                    "Points left of 4 on the x-axis: (1, 50), (2, 55), (2, 60), (3, 60). That is 4. "
                    "(3 counts the hours 1, 2 and 3 instead of the points, and 5 also counts 4 hours.)"))
    its.append(mcq(f + "What does the point (6, 80) mean?", "A student studied 6 hours and scored 80%",
                   ["A student studied 80 hours and scored 6%", "6 students scored 80%", "The mean score is 80%"],
                   "The first number is x (hours studied) and the second is y (score). So one student studied 6 hours "
                   "and scored 80%."))
    its.append(mcq(f + "What was the lowest score, and how long did that student study?", "50%, 1 hour",
                   ["40%, 0 hours", "50%, 0 hours", "55%, 2 hours"],
                   "The lowest point is at (1, 50). (40 and 0 are where the axes start, not data.)"))
    f = fig(arm_svg())
    st = lambda *ls: ["Student " + x for x in ls]
    its.append(mcq(f + "Which student is the tallest?", "Student F", st("A", "D", "E"),
                   "Height is on the x-axis, so the tallest student is the point farthest right: F, at 175 cm.", fix=3))
    its.append(mcq(f + "What is Student C’s arm span?", "160 cm", ["155 cm", "165 cm", "150 cm"],
                   "Arm span is on the y-axis. Go across from point C to the y-axis: 160 cm. (155 cm is C’s height.)"))
    its.append(mcq(f + "What is Student A’s height?", "145 cm", ["150 cm", "140 cm", "155 cm"],
                   "Height is on the x-axis. Go down from point A: 145 cm. (150 cm is A’s arm span, on the y-axis.)"))
    its.append(mcq(f + "Whose arm span is shorter than their height?", "Student B", st("A", "C", "D"),
                   "B is 150 cm tall with an arm span of 145 cm. A and C have arm spans longer than their heights, "
                   "and D’s are equal.", fix=1))
    its.append(mcq(f + "Whose arm span is the same as their height?", "Student D", st("B", "C", "E"),
                   "D is at (165, 165): 165 cm tall with a 165 cm arm span.", fix=2))
    its.append(mcq(f + "How much longer is Student E’s arm span than E’s height?", "5 cm", ["10 cm", "175 cm", "170 cm"],
                   "E is at (170, 175). 175 − 170 = 5 cm. (Each grid square is 5 cm, not 10 cm.)"))
    nl = sum(1 for a, b in ARM if b > a)
    assert nl == 4
    its.append(mcqv(f + "How many students have an arm span longer than their height?", nl, [3, 2, 6], S,
                    "A (145, 150), C (155, 160), E (170, 175) and F (175, 180): 4 students. "
                    "B is shorter, and D is equal."))
    f = fig(cocoa_svg())
    C = lambda x: "%d cups" % x
    its.append(mcq(f + "On the coldest day, how many cups were sold?", C(60), [C(15), C(50), C(20)],
                   "The coldest day is the point farthest left, at −15 °C. It is on the 60 line. "
                   "(15 drops the minus sign from the temperature, and 20 is the warmest day.)"))
    its.append(mcq(f + "How many cups were sold on the day it was 0 °C?", C(30), [C(0), C(35), C(25)],
                   "Go up from 0 on the x-axis to the point: it is on the 30 line. (0 is the temperature, not the cups.)"))
    na = sum(1 for a, b in COCOA if a > 0)
    assert na == 3 and sum(1 for a, b in COCOA if a < 0) == 7
    its.append(mcqv(f + "On how many days was the noon temperature above 0 °C?", na, [4, 7, 2],
                    lambda x: "%d days" % x,
                    "Points to the right of 0: 2 °C, 4 °C and 5 °C. That is 3 days. "
                    "(4 also counts the day at 0 °C, and 7 counts the days below 0 °C.)"))
    T = lambda x: "%s °C" % fmt(x)
    its.append(mcq(f + "What was the temperature on the day 40 cups were sold?", T(-7), [T(7), T(-8), T(-6)],
                   "The point on the 40 line is 3 grid lines left of −4 (or 2 grid lines left of −5): −7 °C. "
                   "(7 °C forgets that the point is left of 0.)"))
    its.append(mcq(f + "What does the point (−4, 35) mean?", "At −4 °C, 35 cups were sold",
                   ["At 35 °C, 4 cups were sold", "35 cups were sold on day 4", "At 4 °C, 35 cups were sold"],
                   "x is the temperature (−4 °C) and y is the number of cups sold (35)."))
    return {"title": "Read scatter plots", "items": its}


# ------------------------------------------------------------ set 3: describe relationships
SP, WP, SN, WN, NO = "Strong positive", "Weak positive", "Strong negative", "Weak negative", "No relationship"


def set_describe(rnd):
    its = []
    p1 = [cloud(rnd, "wp"), cloud(rnd, "sn"), cloud(rnd, "no"), cloud(rnd, "sp")]
    f = fig(panels_svg(p1))
    its.append(mcq(f + "Which graph shows a <b>strong positive</b> relationship?", "Graph D",
                   ["Graph A", "Graph B", "Graph C"],
                   "In Graph D the points go up from left to right (positive) and lie close to a straight line (strong). "
                   "Graph A also goes up, but its points are spread out.", fix=3))
    its.append(mcq(f + "Which graph shows a <b>strong negative</b> relationship?", "Graph B",
                   ["Graph A", "Graph C", "Graph D"],
                   "In Graph B the points go down from left to right (negative) and lie close to a line (strong).", fix=1))
    its.append(mcq(f + "Which graph shows <b>no relationship</b>?", "Graph C", ["Graph A", "Graph B", "Graph D"],
                   "In Graph C the points are scattered with no upward or downward trend. "
                   "Knowing x does not help you guess y.", fix=2))
    its.append(mcq(f + "Which graph shows a <b>weak positive</b> relationship?", "Graph A",
                   ["Graph B", "Graph C", "Graph D"],
                   "In Graph A the points tend to go up from left to right, but they are spread out "
                   "around the trend, so it is weak.", fix=0))
    p2 = [cloud(rnd, "wn"), cloud(rnd, "no"), cloud(rnd, "sn"), cloud(rnd, "wp")]
    f = fig(panels_svg(p2))
    its.append(mcq(f + "Which graph shows a <b>weak negative</b> relationship?", "Graph A",
                   ["Graph B", "Graph C", "Graph D"],
                   "In Graph A the points tend to go down from left to right, but they are spread out. "
                   "Graph C also goes down, but its points are close to a line, so it is strong.", fix=0))
    its.append(mcq(f + "In which graph are the points closest to a straight line?", "Graph C",
                   ["Graph A", "Graph B", "Graph D"],
                   "The points in Graph C lie in a narrow band along a line, so it shows the strongest relationship "
                   "(strong negative).", fix=2))
    its.append(mcq(f + "Which graph shows a <b>positive</b> relationship?", "Graph D", ["Graph A", "Graph B", "Graph C"],
                   "Only in Graph D do the points tend to go up from left to right: as x increases, y tends to increase.",
                   fix=3))
    # gentle but strong vs steep but weak
    rs = random.Random(48812 * 3)
    while True:
        ga = [(x, round(3 + 0.4 * x + rs.gauss(0, 0.18), 2)) for x in (1, 1.8, 2.6, 3.4, 4.2, 5, 5.8, 6.6, 7.4, 8.2, 9)]
        gb = [(x, round(-1 + 1.2 * x + rs.gauss(0, 1.9), 2)) for x in (2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8)]
        ra, ma, _ = stats(ga)
        rb, mb, _ = stats(gb)
        if (ra > 0.95 and 0.45 < rb < 0.7 and mb > 2 * ma and all(0.5 < b < 9.5 for a, b in ga + gb)
                and min((a - c) ** 2 + (b - d) ** 2 for i, (a, b) in enumerate(gb) for (c, d) in gb[i + 1:]) > 0.3):
            break
    f = fig(panels_svg([ga, gb], label="two scatter plots"))
    its.append(mcq(f + "Which graph shows the <b>stronger</b> relationship?", "Graph A",
                   ["Graph B", "Both the same", "Neither"],
                   "Strong means the points lie close to a line. Graph A’s points are almost on a line. "
                   "Graph B is steeper, but its points are spread out, so it is weaker. Steep does not mean strong.",
                   fix=1))
    f = fig(study_svg())
    its.append(mcq(f + "Describe the relationship between study time and test score.", SP, [SN, WP, NO],
                   "As study time increases, scores go up (positive), and the points lie close to a line (strong)."))
    f = fig(cocoa_svg())
    check_kind(COCOA, "sn")
    its.append(mcq(f + "Describe the relationship between temperature and cups sold.", SN, [SP, WN, NO],
                   "As the temperature rises, fewer cups are sold (negative), and the points lie close to a line (strong). "
                   "A downward trend is still a relationship."))
    f = fig(shoe_svg())
    check_kind(SHOE, "no")
    its.append(mcq(f + "Describe the relationship between shoe size and math mark.", NO, [WP, WN, SP],
                   "The points are scattered all over, with no upward or downward trend. "
                   "Shoe size tells you nothing about a student’s math mark."))
    f = fig(sleep_svg())
    check_kind(SLEEP, "wn")
    its.append(mcq(f + "Describe the relationship between screen time and sleep.", WN, [SN, WP, NO],
                   "Students with more screen time tend to sleep less (negative), but the points are spread out "
                   "around the trend (weak)."))
    f = fig(throws_svg())
    check_kind(THROWS, "wp")
    its.append(mcq(f + "Describe the relationship between practice time and free throws made.", WP, [SP, WN, NO],
                   "Students who practise more tend to make more free throws (positive), but the points are spread out, "
                   "and some students who practise a lot make fewer (weak)."))
    its.append(mcq("As a car is driven farther, the amount of gas left in its tank goes down. "
                   "What kind of relationship is this?", "Negative", ["Positive", "None", "Positive: both change"],
                   "When one variable increases and the other decreases, the relationship is negative. "
                   "“Negative” does not mean “no relationship”."))
    its.append(mcq("What kind of relationship would you expect between a student’s height and the month of their birthday?",
                   "None", ["Positive", "Negative", "Strong positive"],
                   "The month you were born does not go with being taller or shorter, so the points would be scattered."))
    its.append(mcq("What kind of relationship would you expect between the age of a maple tree and its height?",
                   "Positive", ["Negative", "None", "Strong negative"],
                   "Older trees tend to be taller, so as age increases, height tends to increase: positive."))
    xs, ys = [1, 2, 3, 4, 5, 6], [20, 17, 15, 11, 8, 5]
    check_kind(list(zip(xs, ys)), "sn")
    its.append(mcq("Hours after a snowstorm (x): <b>%s</b><br>Centimetres of snow on the school roof (y): <b>%s</b><br>"
                   "Describe the relationship." % (", ".join(map(str, xs)), ", ".join(map(str, ys))),
                   SN, [SP, WN, NO],
                   "As x goes up by 1, y goes down by about 3 each time. The values fall steadily, "
                   "so the points would lie close to a line going down: strong negative."))
    its.append(mcq("What does a <b>strong</b> relationship mean on a scatter plot?", "The points lie close to a line",
                   ["The line is very steep", "The points are high on the graph", "There are many points"],
                   "Strength is about how closely the points follow a line, not how steep the line is "
                   "or where the points are."))
    its.append(mcq("On a scatter plot, the points go down from left to right and lie close to a straight line. "
                   "Describe the relationship.", SN, [WN, SP, NO],
                   "Going down from left to right is negative. Close to a line is strong."))
    its.append(mcq("A scatter plot of age and reaction time for adults shows reaction time tends to get longer "
                   "with age, but the points are widely spread. Describe the relationship.", WP, [WN, SP, NO],
                   "As age increases, reaction time tends to increase: positive. Widely spread points make it weak. "
                   "Longer times are bigger numbers, so this is not negative."))
    return {"title": "Describe relationships: strong, weak, positive, negative or none", "items": its}


# ------------------------------------------------------------ set 4: outliers and lines of best fit
def set_fit(rnd):
    its = []
    r_all, m_all, b_all = stats(TRAVEL)
    r_no, m_no, b_no = stats(TRAVEL[:-1])
    assert r_no > 0.95 and r_all < 0.7
    assert all(m_all * x + b_all > m_no * x + b_no for x in range(1, 9))
    f = fig(travel_svg())
    its.append(mcq(f + "Which point is an outlier?", "(3, 45)", ["(8, 35)", "(1, 5)", "(7, 30)"],
                   "Most points follow a line going up. (3, 45) is far above that trend: a short distance but a long time. "
                   "(8, 35) is the farthest point, but it fits the trend."))
    its.append(mcq(f + "What could explain the outlier?", "That student walked instead of taking the bus",
                   ["That student lives the farthest away", "The data has a negative relationship",
                    "Every student takes about 45 minutes"],
                   "The student lives only 3 km away but took 45 minutes, much slower than the others. "
                   "Walking, waiting or a mistake in the data could explain it."))
    its.append(mcq(f + "Ignore the outlier. Describe the relationship between distance and travel time.", SP,
                   [WP, SN, NO],
                   "Without (3, 45), the points go up from left to right and lie close to a line: strong positive."))
    its.append(mcq(f + "If the outlier is included, how does it change the line of best fit?", "It pulls the line up",
                   ["It pulls the line down", "It does not change it", "It makes the line go down"],
                   "The outlier is far above the other points. A line of best fit tries to stay close to every point, "
                   "so it is pulled up toward the outlier."))
    its.append(mcq("Leah finds an outlier in her data. What should she do first?",
                   "Check if it is a mistake or a real value",
                   ["Always delete it", "Delete it because it is the largest", "Change it to the mean"],
                   "An outlier might be a recording mistake (fix or remove it) or a real but unusual value "
                   "(keep it and explain it). Never delete data just because it does not fit."))
    pairs = [(13, 158), (13, 162), (14, 165), (14, 210), (13, 155)]
    its.append(mcq("Ages and heights of some Grade 8 students: %s. Which pair is most likely a recording mistake?"
                   % ", ".join("(%d, %d)" % p for p in pairs), "(14, 210)", ["(13, 155)", "(14, 165)", "(13, 162)"],
                   "A Grade 8 student who is 210 cm tall is very unlikely, and it is far from the other heights. "
                   "It is probably a typing mistake. (13, 155) is the smallest, but it is a normal height."))
    f = fig(study_svg(fit=True))
    m, b = STUDY_FIT
    r, ls_m, ls_b = stats(STUDY)
    assert abs(ls_m - m) < 0.5 and abs(ls_b - b) < 2
    above = sum(1 for x, y in STUDY if y > m * x + b)
    below = sum(1 for x, y in STUDY if y < m * x + b)
    assert abs(above - below) <= 1
    P = lambda x: "%s%%" % fmt(x)
    its.append(mcq(f + "Use the line of best fit to predict the score for 3 hours of study.", P(m * 3 + b),
                   [P(60), P(65), P(56)],
                   "Go up from 3 to the orange line, then across: about 62%. (60% is the student who studied 3 hours, "
                   "not the line, and 56% is the line at 2 hours.)"))
    its.append(mcq(f + "Use the line to predict the score of a student who does not study at all (0 hours).", P(b),
                   [P(50), P(40), P(0)],
                   "Follow the line back to 0 hours: it meets the y-axis at 44%. "
                   "(50% is the lowest data point, and 40% is where the scale starts.)"))
    assert F(80 - b, m) == 6
    its.append(mcq(f + "About how many hours of study does the line predict for a score of 80%?", "6 hours",
                   ["5 hours", "7 hours", "8 hours"],
                   "Go across from 80% to the orange line, then down: 6 hours. The line gives 6 × 6 + 44 = 80."))
    for pt, on in (((6, 80), True), ((5, 80), False), ((2, 60), False), ((8, 90), False)):
        assert (m * pt[0] + b == pt[1]) == on
    its.append(mcq(f + "Which of these data points lies on the line of best fit?", "(6, 80)",
                   ["(5, 80)", "(2, 60)", "(8, 90)"],
                   "The line gives 6 × 6 + 44 = 80 at 6 hours, so (6, 80) is on it. (5, 80) and (2, 60) are above the line, "
                   "and (8, 90) is below it (the line gives 92 there)."))
    assert m * 12 + b == 116
    its.append(mcq(f + "The line predicts a score of 116% for 12 hours of study. What is wrong?",
                   "12 hours is far outside the data", ["The line goes the wrong way", "Scores can be over 100%",
                                                       "Nothing: the line is always right"],
                   "The data only goes up to 8 hours. A score cannot be more than 100%, so the line does not work "
                   "far outside the data."))
    its.append(mcq("Which is true about a line of best fit?", "About as many points are above it as below",
                   ["It must pass through every point", "It must start at (0, 0)", "It joins the first and last points"],
                   "A line of best fit follows the trend, with points on both sides. "
                   "It does not have to pass through any point, through (0, 0), or through the end points."))
    base = [(1, 3), (2, F("2.4")), (3, 4), (4, F("4.4")), (5, F("5.6")), (6, F("5.2")), (7, F("7.2")), (8, F("6.8")),
            (9, F("8.6"))]
    r, lm, lb = stats([(float(a), float(c)) for a, c in base])
    good = (F("0.7"), F("1.7"))
    assert abs(float(good[0]) - lm) < 0.08 and abs(float(good[1]) - lb) < 0.3
    fits = [(F("0.7"), F("4.2")), good, (F("1.4"), 0), (F("-0.3"), 7)]
    assert all(c < fits[0][0] * a + fits[0][1] for a, c in base)
    f = fig(panels_svg([base] * 4, fits=fits, label="four scatter plots with lines"))
    its.append(mcq(f + "Which graph shows the best line of best fit?", "Graph B", ["Graph A", "Graph C", "Graph D"],
                   "In Graph B the line follows the trend, with points on both sides. A is above every point, "
                   "C starts at (0, 0) and is too steep, and D goes down while the points go up.", fix=1))
    its.append(mcq(f + "Why is the line in Graph A a poor fit?", "All the points are below it",
                   ["It goes up", "It does not start at (0, 0)", "It is not steep enough"],
                   "Graph A’s line has about the right steepness, but it is too high: every point is below it."))
    f = fig(cocoa_svg(fit=True))
    m, b = COCOA_FIT
    above = sum(1 for x, y in COCOA if y > m * x + b)
    below = sum(1 for x, y in COCOA if y < m * x + b)
    assert abs(above - below) <= 1
    C = lambda x: "%d cups" % x
    its.append(mcq(f + "Use the line of best fit to predict the cups sold on a day when it is −5 °C.", C(m * -5 + b),
                   [C(35), C(50), C(20)],
                   "Go up from −5 to the orange line, then across: 40 cups. (35 is the data point at −4 °C, 50 is the line "
                   "at −10 °C, and 20 uses 5 °C instead of −5 °C.)"))
    assert F(50 - b, m) == -10
    T = lambda x: "%s °C" % fmt(x)
    its.append(mcq(f + "At what temperature does the line predict 50 cups sold?", T(-10), [T(10), T(-5), T(-15)],
                   "Go across from 50 to the line, then down: −10 °C. Check: 30 − 2 × (−10) = 50."))
    its.append(mcq(f + "According to the line, for each 1 °C warmer, about how many fewer cups are sold?", "2 cups",
                   ["5 cups", "30 cups", "1 cup"],
                   "From −10 °C to 0 °C (10 degrees warmer), the line drops from 50 to 30 cups: 20 fewer. "
                   "20 ÷ 10 = 2 cups per degree."))
    its.append(mcq(f + "The line predicts −10 cups on a 20 °C day. What does this show?",
                   "Do not use the line far outside the data", ["The rink loses 10 cups", "The relationship is positive",
                                                               "The line must be wrong everywhere"],
                   "A number of cups cannot be negative. The data stops at 5 °C, so predictions at 20 °C "
                   "are not reliable. Inside the data, the line still works well."))
    its.append(mcqv("The line of best fit for practice time (x hours) and goals (y) is y = 2x + 10. "
                    "Predict the goals for 5 hours of practice.", 20, [17, 30, 15], lambda x: "%d goals" % x,
                    "Replace x with 5: y = 2 × 5 + 10 = 10 + 10 = 20. (17 adds 2 + 5 + 10, 30 is 2 × (5 + 10), "
                    "and 15 leaves out the 2.)"))
    its.append(mcq("Owen plots the age and price of used cars: a strong negative relationship. One 30-year-old classic car "
                   "costs much more than the line predicts. What is that car on the scatter plot?", "An outlier",
                   ["The line of best fit", "Proof the relationship is positive", "The median"],
                   "One point far from the trend is an outlier. It does not change the overall pattern: most older cars cost less."))
    return {"title": "Outliers and predictions with a line of best fit", "items": its}


# ------------------------------------------------------------ set 5: conclusions and misleading graphs
SYRUP = (["Sugar bush A", "Sugar bush B"], [54, 51])
BUS_X = ["Jan", "Feb", "Mar", "Apr"]
BUS = [10200, 10250, 10300, 10350]


def syrup_svg():
    return bar_svg("Maple syrup made this spring", "Sugar bush", "Litres", SYRUP[0], SYRUP[1], 48, 56, 1, 2, gy=16, slot=130)


def bus_svg():
    return bline_svg("Bus riders each month", "Month", "Riders", BUS_X, BUS, 10200, 10400, 25, 50, gy=12, slot=70)


def set_conclusions():
    its = []
    its.append(mcq("In summer, ice cream sales and sunburns both go up: a strong positive relationship. "
                   "Does eating ice cream cause sunburns?", "No: hot, sunny weather causes both",
                   ["Yes: the relationship is strong", "Yes: both go up together", "No: the relationship is negative"],
                   "A strong relationship does not prove that one variable causes the other. "
                   "A third variable, sunny weather, makes both go up."))
    its.append(mcq("A survey finds that students who eat breakfast tend to have higher marks. Which conclusion is best?",
                   "They are related, but breakfast may not be the cause",
                   ["Eating breakfast causes higher marks", "Higher marks cause students to eat breakfast",
                    "There is no relationship"],
                   "The data shows a positive relationship, not a cause. Other things, such as sleep or "
                   "home routines, could explain both."))
    its.append(mcq("For students from Grade 1 to Grade 8, shoe size and reading level have a strong positive relationship. "
                   "Why?", "Older students have bigger feet and read better",
                   ["Big feet help you read", "Reading makes your feet grow", "The data must be wrong"],
                   "Age is the hidden third variable: as students get older, their feet grow and their reading improves."))
    its.append(mcq("Sales of snow shovels and sales of hot chocolate rise and fall together. "
                   "What third variable most likely explains this?", "Cold, snowy weather",
                   ["Shovelling makes people thirsty", "Hot chocolate makes it snow", "The price of shovels"],
                   "Both sales go up in cold, snowy weather. Neither one causes the other."))
    its.append(mcq("A scatter plot shows a strong negative relationship between screen time and sleep for 50 students. "
                   "Which statement is supported?", "Students with more screen time tend to sleep less",
                   ["Screen time causes students to sleep less", "Every student with more screen time sleeps less",
                    "Screen time and sleep are not related"],
                   "A negative relationship means more screen time tends to go with less sleep. It does not prove a cause, "
                   "and “tends to” is not “every”."))
    its.append(mcq("A scatter plot of hours of sleep and test scores for 40 students shows no relationship. "
                   "Which conclusion is supported?", "For these students, sleep and score were not related",
                   ["More sleep lowers scores", "More sleep raises scores", "The data was collected wrongly"],
                   "With no trend, knowing a student’s sleep does not help predict the score, for this sample."))
    its.append(mcq("Practice time and free throws made have a weak positive relationship. A few students practised a lot "
                   "but made few free throws. Does this disprove the trend?", "No: a weak trend has exceptions",
                   ["Yes: the trend is wrong", "Yes: it is now negative", "No: those points must be deleted"],
                   "A weak relationship means points are spread out around the trend. Some points go against it, "
                   "but the overall trend is still positive."))
    its.append(mcq("Arjun asks 3 friends about their study time and marks and finds a strong positive relationship. "
                   "Why is his conclusion weak?", "3 points are too few to show a trend",
                   ["Friends always tell the truth", "Study time cannot be measured", "Marks are not data"],
                   "With only 3 points, almost any pattern can happen by chance. He needs a much larger sample."))
    its.append(mcq("Mei wants to know if height increases with age, but she measures only 13-year-olds. "
                   "Why can her scatter plot not answer the question?", "All the ages are the same",
                   ["She measured too many students", "Height is not a variable", "Age is qualitative"],
                   "All her points line up above one age, so she cannot see how height changes as age changes."))
    f = fig(syrup_svg())
    a, b = SYRUP[1]
    assert (a - 48) == 2 * (b - 48) and a < 2 * b
    its.append(mcq(f + "The bar for Sugar bush A looks twice as tall. Did it make twice as much syrup?",
                   "No: 54 L is not 2 × 51 L", ["Yes: its bar is twice as tall", "Yes: 54 is more than 51",
                                                "No: Sugar bush B made more"],
                   "2 × 51 = 102, but A made only 54 L. The scale starts at 48, not 0, "
                   "so the bars show only 6 and 3 litres above 48."))
    its.append(mcqv(f + "How many more litres did Sugar bush A make than Sugar bush B?", a - b, [a - 48, b, a + b],
                    lambda x: "%d L" % x,
                    "54 − 51 = 3 L. (6 is only the part of bar A above 48, 51 is the amount for B, "
                    "and 105 adds the two amounts.)"))
    f = fig(bus_svg())
    d = BUS[-1] - BUS[0]
    assert d == 150
    R = lambda x: "%s riders" % num(x)
    its.append(mcq(f + "A news report says bus ridership “soared” from January to April. By how many riders did it grow?",
                   R(d), [R(BUS[-1]), R(300), R(BUS[-1] - BUS[-2])],
                   "April 10" + NBSP + "350 − January 10" + NBSP + "200 = 150 riders. (Each small grid step is 25, not 50, "
                   "so 300 doubles the change. 50 is only March to April.)"))
    assert F(d * 100, BUS[0]) < 2
    its.append(mcq(f + "Why does the line look like it “soared”?", "The scale starts at 10" + NBSP + "200, not 0",
                   ["The months are equally spaced", "The points are joined", "The graph has a title"],
                   "The increase is 150 riders, less than 2% of 10" + NBSP + "200. Starting the scale at "
                   "10" + NBSP + "200 makes a small change look huge."))
    assert (44 - 40) * 100 // 40 == 10
    its.append(mcq("Moose sightings in a park rose from 40 to 44. A graph makes the second bar look 3 times as tall. "
                   "By what percent did the sightings really increase?", "10%", ["4%", "300%", "44%"],
                   "The increase is 44 − 40 = 4. 4 ÷ 40 = 0.1 = 10%. (4% forgets to divide by 40, "
                   "and 300% trusts the bar heights.)"))
    its.append(mcq("A milk carton picture shows sales doubling. The second carton is twice as tall, twice as wide "
                   "and twice as deep. How many times as big does it look?", "8 times", ["2 times", "4 times", "6 times"],
                   "Doubling all three dimensions makes the volume 2 × 2 × 2 = 8 times as big, "
                   "so the picture makes sales look 8 times bigger instead of 2 times."))
    its.append(mcq("A company graph shows only March to May, when its sales rose. For the whole year, sales fell. "
                   "What makes the graph misleading?", "It shows only the months that help its claim",
                   ["It uses months", "It is a broken-line graph", "Sales cannot fall"],
                   "Choosing only part of the data can hide the real trend. A fair graph shows the whole year."))
    its.append(mcq("A survey at a skating rink asks people their favourite winter activity. 80% say skating. "
                   "A poster says, “80% of Canadians love skating most.” What is the main problem?",
                   "People at a rink are likely to choose skating",
                   ["80% is too high to be true", "The survey asked too many people", "Skating is not a winter activity"],
                   "The sample is biased: the people asked were at a skating rink. They do not represent all Canadians."))
    its.append(mcq("Zoe’s bean plant grew about 2 cm a week for 6 weeks. She uses this trend to predict it will be "
                   "2 m tall after 100 weeks. What is wrong?", "100 weeks is far outside her data",
                   ["2 cm a week is too slow", "The trend is negative", "She should use 2 m a week"],
                   "Her data covers 6 weeks. Plants stop growing, so the trend cannot be stretched to 100 weeks."))
    its.append(mcqv("For 8B, the line of best fit for height (x cm) and arm span (y cm) is y = x + 2. "
                    "Ethan is 172 cm tall. Predict his arm span.", 172 + 2, [170, 172, 2 * 172], lambda x: "%d cm" % x,
                    "Replace x with 172: y = 172 + 2 = 174 cm. (170 subtracts 2, 172 forgets the + 2, "
                    "and 344 reads x + 2 as 2x.)"))
    its.append(mcq("In a city, the number of firefighters sent to a fire and the damage the fire causes have a strong "
                   "positive relationship. Do firefighters cause the damage?", "No: bigger fires need more firefighters",
                   ["Yes: the relationship is strong", "Yes: more firefighters, more damage",
                    "No: the relationship is negative"],
                   "The size of the fire is the third variable. A big fire causes more damage and also needs more "
                   "firefighters. A strong relationship does not show what causes what."))
    return {"title": "Word problems: cause, misleading graphs and conclusions", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


LESSON = [(1, 4), (2, 6), (3, 5), (3, 8), (4, 9), (5, 10), (6, 12), (6, 10), (7, 13), (8, 15), (2, 14)]
LESSON_FIT = (F(3, 2), F(3))


def body_html(rnd):
    r, lm, lb = stats(LESSON[:-1])
    assert r > 0.95 and abs(lm - 1.5) < 0.2 and abs(lb - 3) < 1
    demo = [cloud(rnd, "sp"), cloud(rnd, "wn"), cloud(rnd, "no"), cloud(rnd, "sn")]
    return (
        "<h2>One-variable and two-variable data</h2>"
        "<p><b>One-variable</b> data records one value for each person or thing, such as each student’s height. "
        "<b>Two-variable</b> data records a pair of values for each, such as each student’s height <i>and</i> arm span. "
        "Two-variable data answers questions like “Do taller students have longer arm spans?”</p>" +
        table(["Data", "Variables", "Good graph"], [
            ["Height of each student", "One", "Histogram, stem-and-leaf plot"],
            ["Height and arm span of each student", "Two", "Scatter plot"],
        ]) +
        "<h2>Scatter plots</h2>"
        "<p>A <b>scatter plot</b> shows each pair as one point (x, y). Put the independent variable on the x-axis "
        "and the dependent variable on the y-axis. Do not join the points.</p>"
        "<figure class='sn-fig'>" +
        scatter_svg("Practice and goals", "Practice per week (hours)", "Goals this season", LESSON,
                    (0, 9, 1, 1), (0, 16, 1, 2), 28, 10, fit=LESSON_FIT) +
        "<figcaption>Each point is one ringette player. The orange line is a line of best fit. "
        "The point (2, 14) is an outlier.</figcaption></figure>" +
        ex("Example 1", "What does the point (6, 12) mean?",
           "x is practice time and y is goals.", "a player who practised 6 hours a week scored 12 goals") +
        "<h2>Describing a relationship</h2>"
        "<p>Look at the direction and the spread of the points. <b>Positive</b>: as x increases, y tends to increase. "
        "<b>Negative</b>: as x increases, y tends to decrease. <b>Strong</b>: the points lie close to a line. "
        "<b>Weak</b>: they are spread out around the trend. <b>None</b>: no trend at all.</p>"
        "<figure class='sn-fig'>" +
        panels_svg(demo, names=["Strong positive", "Weak negative", "None", "Strong negative"],
                   label="four kinds of relationship") +
        "<figcaption>Strength is about how close the points are to a line, not how steep the line is.</figcaption></figure>"
        "<h2>Outliers and the line of best fit</h2>"
        "<p>An <b>outlier</b> is a point far from the trend. Check it: it may be a mistake, or a real but unusual value. "
        "A <b>line of best fit</b> follows the trend, with about as many points above it as below. "
        "It does not have to pass through (0, 0) or through any point.</p>" +
        ex("Example 2", "Use the line of best fit in the graph above to predict the goals for 4 hours of practice.",
           "Go up from 4 to the orange line, then across: 1.5 × 4 + 3 = 9.", "about 9 goals") +
        "<p>Predictions inside the data are fairly reliable. Predictions far outside the data "
        "(for example, 40 hours of practice) may not make sense.</p>"
        "<h2>Correlation is not causation</h2>"
        "<p>A strong relationship does not prove that one variable causes the other. Ice cream sales and sunburns "
        "both rise in summer because of a third variable: hot, sunny weather.</p>"
        "<h2>Misleading graphs</h2>"
        "<p>Before you believe a graph or a claim, check: Does a bar graph’s scale start at 0? Are the spaces equal? "
        "How many people were asked, and who? Is the prediction far outside the data?</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Thinking a strong relationship proves a cause", "Look for a third variable; say the variables are related"],
            ["Calling a steep line “strong”", "Strong means the points are close to a line"],
            ["Calling a downward trend “no relationship”", "Going down is a negative relationship"],
            ["Taking the highest or farthest point as the outlier", "An outlier is far from the trend"],
            ["Drawing the line through (0, 0) or through the end points", "Follow the trend, with points on both sides"],
            ["Swapping x and y when reading a point", "(x, y): across first, then up"],
        ])
    )


FAQ = [
    {"q": "What do Grade 8 students learn about scatter plots in the Ontario math curriculum?",
     "a": "In Grade 8, students collect two-variable data, make and read scatter plots, describe relationships as strong or weak and positive, negative or none, and look at how outliers affect the data. They also judge conclusions and spot misleading graphs."},
    {"q": "How do you describe the relationship on a scatter plot?",
     "a": "Look at the direction and the spread. If the points go up from left to right it is positive, if they go down it is negative, and if they lie close to a line it is strong; spread-out points are weak, and no trend means no relationship."},
    {"q": "What is a line of best fit?",
     "a": "It is a straight line drawn through the middle of the points on a scatter plot, with about as many points above it as below. You can use it to make predictions inside the range of the data."},
    {"q": "Does correlation mean causation?",
     "a": "No. Two variables can be strongly related because a third variable affects both, such as hot weather raising both ice cream sales and sunburns. A scatter plot shows a relationship, not a cause."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5). Items with fixed A–D choices keep their place."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        for it in s["items"]:
            if it.get("fix"):
                targets.remove(it["a"])
        rnd.shuffle(targets)
        k = 0
        for it in s["items"]:
            if it.pop("fix", False):
                continue
            t = targets[k]
            k += 1
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        final = [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


def gen_unit():
    rnd = random.Random(48812)
    sets = [set_variables(), set_read(), set_describe(rnd), set_fit(rnd), set_conclusions()]
    body = body_html(rnd)
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len({plain(c) for c in it["c"]}) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1, it["q"]
            k = plain(it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-8", "slug": "scatter-plots-and-data", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 8 Scatter Plots and Data: Relationships, Lines of Best Fit and Misleading Graphs",
        "seo_title": "Grade 8 Scatter Plots Worksheets: Correlation, Line of Best Fit (Free, Answer Key, Ontario Curriculum)",
        "short_title": "Scatter plots and data",
        "domain": "Data",
        "standard_code": "Grade 8: D1.5",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use mathematical language, including the terms “strong”, “weak”, “none”, “positive”, and “negative”, to describe the relationship between two variables for various data sets with and without outliers",
        "meta_desc": "Free Grade 8 math worksheets on scatter plots for the Ontario curriculum: one- and two-variable data, reading scatter plots, strong, weak, positive, negative or no relationship, outliers, predictions with a line of best fit, and misleading graphs. 100 questions with an answer key.",
        "key_big": "A scatter plot shows pairs of data. Describe the trend by its direction (positive, negative or none) and how close the points are to a line (strong or weak).",
        "key_sub": "An outlier is a point far from the trend. A line of best fit has about as many points above it as below and is used for predictions inside the data. A strong relationship does not prove that one variable causes the other.",
        "body_html": body, "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (graphs) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "(scatter plot|four scatter|two scatter|bar graph|broken-line)")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
