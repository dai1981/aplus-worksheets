# -*- coding: utf-8 -*-
"""
CA Grade 6 Math: Data and graphs (Ontario Curriculum 2020, Grade 6: Data, D1)
  python3 tools/gen_ca_math_g6_data.py
Discrete and continuous data, histograms and broken-line graphs, the mean, median, mode and range,
comparing two data sets, and misleading graphs and conclusions (scales that do not start at 0,
uneven scales, small and biased samples, the mean pulled by an outlier).
Wrong answers come from real student mistakes: the highest value (or the frequency) as the mode, the median
taken without ordering, dividing by the wrong count, the biggest value as the range, ignoring minus signs,
reading the neighbouring bar, and judging bars by height when the scale does not start at 0.
Canadian English, Ontario number style (4536, 10 000 with a no-break space). HTML attributes use single quotes.
"""
import json, re, math, os, random
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
BAR = "#2e8b57"
BAR2 = "#e0a030"
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
    """Whole numbers or terminating decimals (up to 3 places)."""
    x = F(x)
    if x.denominator == 1:
        return num(x)
    for k in (1, 2, 3):
        y = x * 10 ** k
        if y.denominator == 1:
            v = abs(y.numerator)
            s = str(v).rjust(k + 1, "0")
            s = num(int(s[:-k])) + "." + s[-k:]
            return (MINUS if x < 0 else "") + s
    raise AssertionError(x)


def money(x):
    x = F(x)
    assert (x * 100).denominator == 1 and x >= 0
    c = int(x * 100)
    return "$%s.%02d" % (num(c // 100), c % 100)


def unit(v, one, many):
    return "%s %s" % (fmt(v), one if F(v) == 1 else many)


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def lst(v):
    return ", ".join(fmt(x) for x in v)


def median(v):
    s = sorted(F(x) for x in v)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def mean(v):
    return sum(F(x) for x in v) / len(v)


def modes(v):
    c = {}
    for x in v:
        c[F(x)] = c.get(F(x), 0) + 1
    m = max(c.values())
    return sorted(k for k, n in c.items() if n == m) if m > 1 else []


def rng(v):
    return F(max(v)) - F(min(v))


def mcq(q, right, wrongs, e):
    ch = [right]
    for w in wrongs:
        assert plain(w) not in {plain(c) for c in ch}, (q, right, wrongs)
        ch.append(w)
    assert len(ch) == 4, (q, right, wrongs)
    return {"q": q, "c": ch, "a": 0, "e": e}


def mcqv(q, right, wrongs, f, e):
    """Choices given as values: equal values are not allowed."""
    seen = [F(right)]
    for w in wrongs:
        assert F(w) not in seen, (q, right, wrongs)
        seen.append(F(w))
    return mcq(q, f(right), [f(w) for w in wrongs], e)


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


def line(x1, y1, x2, y2, col=INK, w=1):
    return "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%s'/>" % (x1, y1, x2, y2, col, w)


def yaxis_title(s, val_axis, y0, ph, fs=14):
    mid = y0 + ph / 2
    assert tw(val_axis, fs, True) < ph + 30, (val_axis, ph)
    s.append(text(13, mid, val_axis, fs, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % mid))


# ------------------------------------------------------------ graphs
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
    yaxis_title(s, val_axis, y0, ph)
    return svg_wrap(W, yb + 46, "".join(s), "bar graph: " + title.lower())


def hist_svg(title, x_axis, y_axis, edges, freqs, ymax, lstep, gy=11, bw=52):
    """Histogram: equal intervals, bars touch, labels at the edges of the intervals."""
    fs = 14
    assert len(edges) == len(freqs) + 1 and all(0 <= f <= ymax for f in freqs) and ymax % lstep == 0
    ph = ymax * gy
    x0 = 30 + tw(ymax, fs) + 6
    pw = bw * len(freqs) + 20
    y0 = 34
    yb = y0 + ph
    W = max(x0 + pw + 14, tw(title, 16, True) + 16)
    s = [text(W / 2, 18, title, 16, bold=True)]
    for v in range(ymax + 1):
        y = yb - v * gy
        major = v % lstep == 0
        s.append(line(x0, y, x0 + pw, y, GRID2 if major else GRID))
        if major:
            s.append(text(x0 - 5, y + 5, num(v), fs, anchor="end"))
    bx = x0 + 10
    for i, f in enumerate(freqs):
        h = f * gy
        s.append("<rect x='%.1f' y='%.1f' width='%d' height='%.1f' fill='%s' stroke='#ffffff' stroke-width='1.5'/>"
                 % (bx + i * bw, yb - h, bw, h, BAR))
    for i, e in enumerate(edges):
        x = bx + i * bw
        s.append(line(x, yb, x, yb + 5, INK, 1.5))
        s.append(text(x, yb + 20, num(e), fs))
    s.append("<path d='M%.1f %d V%.1f H%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0 - 6, yb, x0 + pw, INK))
    s.append(text(x0 + pw / 2, yb + 40, x_axis, fs, bold=True))
    yaxis_title(s, y_axis, y0, ph)
    return svg_wrap(W, yb + 48, "".join(s), "histogram: " + title.lower())


def bline_svg(title, x_axis, y_axis, xlabels, series, ymin, ymax, gstep, lstep, gy=12, slot=64, lab=num, names=None):
    """Broken-line graph: points joined by straight line segments. Two series get a key."""
    fs = 14
    cols = [GREEN, BAR2]
    assert (ymax - ymin) % lstep == 0 and lstep % gstep == 0
    for v in series:
        assert len(v) == len(xlabels) and all(ymin <= x <= ymax for x in v)
    nt = (ymax - ymin) // gstep
    ph = nt * gy
    x0 = 24 + max(tw(lab(ymax), fs), tw(lab(ymin), fs)) + 6
    slot = max(slot, max(tw(c, fs) for c in xlabels) + 10)
    pw = slot * len(xlabels)
    y0 = 34 + (24 if names else 0)
    yb = y0 + ph
    W = max(x0 + pw + 8, tw(title, 16, True) + 16)
    if names:
        ws = [tw(n, fs) for n in names]
        tot = sum(ws) + 2 * 30 + 24
        W = max(W, tot + 16)
    s = [text(W / 2, 18, title, 16, bold=True)]
    if names:
        kx = (W - tot) / 2
        for i, n in enumerate(names):
            s.append(line(kx, 38, kx + 22, 38, cols[i], 3))
            s.append("<circle cx='%.1f' cy='38' r='4.5' fill='%s'/>" % (kx + 11, cols[i]))
            s.append(text(kx + 28, 43, n, fs, anchor="start"))
            kx += 30 + ws[i] + 24
    for k in range(nt + 1):
        v = ymin + k * gstep
        y = yb - k * gy
        major = (v - ymin) % lstep == 0
        s.append(line(x0, y, x0 + pw, y, INK if v == 0 and ymin < 0 else (GRID2 if major else GRID),
                      1.5 if v == 0 and ymin < 0 else 1))
        if major:
            s.append(text(x0 - 5, y + 5, lab(v), fs, anchor="end"))
    for i, c in enumerate(xlabels):
        x = x0 + slot * i + slot / 2
        s.append(line(x, yb, x, yb + 5, INK, 1.5))
        s.append(text(x, yb + 20, c, fs))
    for j, v in enumerate(series):
        pts = [(x0 + slot * i + slot / 2, yb - (F(val) - ymin) / gstep * gy) for i, val in enumerate(v)]
        s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (" ".join("%.1f,%.1f" % (float(a), float(b)) for a, b in pts), cols[j]))
        for a, b in pts:
            s.append("<circle cx='%.1f' cy='%.1f' r='4.5' fill='%s'/>" % (float(a), float(b), cols[j]))
    s.append("<path d='M%.1f %d V%.1f H%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0 - 6, yb, x0 + pw, INK))
    s.append(text(x0 + pw / 2, yb + 40, x_axis, fs, bold=True))
    yaxis_title(s, y_axis, y0, ph)
    return svg_wrap(W, yb + 48, "".join(s), "broken-line graph: " + title.lower())


def dot_svg(title, axis, lo, hi, counts):
    """Line plot: one X for each piece of data, stacked above a number line."""
    fs = 14
    gap, dy = 40, 15
    mx = max(counts.values())
    pw = gap * (hi - lo)
    W = max(26 * 2 + pw, tw(title, 16, True) + 16)
    x0 = (W - pw) / 2
    top = 34
    yb = top + mx * dy + 6
    s = [text(W / 2, 18, title, 16, bold=True)]
    for v in range(lo, hi + 1):
        x = x0 + (v - lo) * gap
        s.append(line(x, yb, x, yb + 6, INK, 1.5))
        s.append(text(x, yb + 22, v, fs))
        for k in range(counts.get(v, 0)):
            cy = yb - 9 - k * dy
            s.append("<path d='M%.1f %.1f L%.1f %.1f M%.1f %.1f L%.1f %.1f' stroke='%s' stroke-width='2.4'/>"
                     % (x - 5, cy - 5, x + 5, cy + 5, x - 5, cy + 5, x + 5, cy - 5, GREEN))
    s.append(line(x0 - 14, yb, x0 + pw + 14, yb, INK, 2))
    s.append(text(W / 2, yb + 44, axis, fs, bold=True))
    assert all(lo <= k <= hi for k in counts)
    return svg_wrap(W, yb + 52, "".join(s), "line plot: " + title.lower())


# ------------------------------------------------------------ data
RUN_E = [4, 5, 6, 7, 8, 9, 10]
RUN_F = [2, 6, 9, 7, 4, 2]
HT_E = [130, 140, 150, 160, 170]
HT_F = [3, 10, 12, 5]
TEMP_X = ["8 a.m.", "10 a.m.", "noon", "2 p.m.", "4 p.m.", "6 p.m."]
TEMP = [-18, -14, -10, -6, -8, -12]
SUN_X = ["1", "2", "3", "4", "5", "6"]
SUN = [10, 15, 25, 40, 55, 75]
PETS = {0: 3, 1: 6, 2: 5, 3: 2, 4: 1}
BEAN_X = ["1", "2", "3", "4", "5"]
BEAN_A = [4, 8, 14, 20, 26]
BEAN_B = [4, 6, 10, 12, 16]
VOTE = (["Science centre", "Zoo"], [46, 42])
TFR_X = ["2022", "2023", "2024", "2025", "2026"]
TFR = [1440, 1480, 1500, 1520, 1560]


def run_svg():
    return hist_svg("Time to run 1 km on Terry Fox Run day", "Time (minutes)", "Students", RUN_E, RUN_F, 10, 2, gy=11)


def ht_svg():
    return hist_svg("Heights of Grade 6 students", "Height (cm)", "Students", HT_E, HT_F, 14, 2, gy=9, bw=60)


def temp_svg():
    return bline_svg("Temperature on a January day in Winnipeg", "Time", "Temperature (°C)", TEMP_X, [TEMP],
                     -20, 0, 2, 4, gy=13, slot=66)


def sun_svg():
    return bline_svg("Height of Zoe’s sunflower", "Week", "Height (cm)", SUN_X, [SUN], 0, 80, 5, 10, gy=10, slot=50)


def pets_svg():
    return dot_svg("Pets owned by students in 6C", "Number of pets", 0, 4, PETS)


def bean_svg():
    return bline_svg("Height of two bean plants", "Week", "Height (cm)", BEAN_X, [BEAN_A, BEAN_B], 0, 28, 2, 4,
                     gy=9, slot=72, names=["Plant A: plant food", "Plant B: water only"])


def vote_svg():
    return bar_svg("Votes for the Grade 6 field trip", "Place", "Votes", VOTE[0], VOTE[1], 40, 48, 1, 2, gy=16)


def tfr_svg():
    return bline_svg("Money raised for the Terry Fox Run", "Year", "Money raised", TFR_X, [TFR], 1400, 1600, 20, 40,
                     gy=12, slot=58, lab=lambda v: "$" + num(v))


# ------------------------------------------------------------ set 1: discrete or continuous
DC, CM, DM, CC = "Discrete: it is counted", "Continuous: it is measured", "Discrete: it is measured", "Continuous: it is counted"


def kind(q, right, e):
    wr = [k for k in (DC, CM, DM, CC) if k != right]
    return mcq("Is this data discrete or continuous?<br><b>%s</b>" % q, right, wr, e)


def set_kinds():
    its = [
        kind("The number of pets each student has", DC,
             "Pets are counted: 0, 1, 2, 3 … Nobody has 2.5 pets, so the data is discrete."),
        kind("The height of each student in centimetres", CM,
             "Height is measured. It can be any value in a range, such as 148.6 cm, so the data is continuous."),
        kind("The time each student takes to skate one lap of the rink", CM,
             "Time is measured. It can be 41 s, 41.3 s or 41.35 s, so the data is continuous."),
        kind("The number of goals scored in each hockey game", DC,
             "Goals are counted. A team can score 3 or 4 goals but not 3.5, so the data is discrete."),
        kind("The mass of each pumpkin at a Thanksgiving market", CM,
             "Mass is measured, so it can be any value, such as 4.25 kg. The data is continuous."),
        kind("The number of people in each canoe on a canoe trip", DC,
             "People are counted in whole numbers, so the data is discrete."),
        kind("The amount of sap collected from each maple tree, in litres", CM,
             "The amount of sap is measured. It can be 2.4 L or 2.45 L, so the data is continuous."),
        kind("The number of snow days each winter", DC,
             "Snow days are counted in whole numbers, so the data is discrete."),
        kind("The temperature at noon each day in January", CM,
             "Temperature is measured with a thermometer. It can be −7.5 °C, so the data is continuous."),
        kind("The number of loons counted on the lake each morning", DC,
             "Loons are counted in whole numbers, so the data is discrete."),
        kind("The distance each student runs in the Terry Fox Run, in kilometres", CM,
             "Distance is measured. A student could run 3.2 km or 3.25 km, so the data is continuous."),
        kind("The number of books each student read over the summer holidays", DC,
             "Books are counted in whole numbers, so the data is discrete."),
        mcq("Which of these is <b>continuous</b> data?", "Hours of sleep each night",
            ["Number of cousins", "Goals in each game", "Number of pets"],
            "Sleep is measured in time, so it can be 8.5 or 8.75 hours. The others are counted, so they are discrete."),
        mcq("Which of these is <b>discrete</b> data?", "Cars in the parking lot",
            ["Mass of a backpack", "Length of a hockey stick", "Time to eat lunch"],
            "Cars are counted in whole numbers. Mass, length and time are measured, so they are continuous."),
        mcq("What kind of data is <b>each student’s favourite hockey team</b>?", "Qualitative: names, not numbers",
            ["Discrete: it is counted", "Continuous: it is measured", "Quantitative: it has numbers"],
            "The answers are team names, not numbers, so the data is qualitative (categories). "
            "Discrete and continuous are kinds of number data."),
        mcq("What kind of data is <b>the number on each player’s hockey jersey</b>?", "Qualitative: the numbers are labels",
            ["Discrete: they are whole numbers", "Continuous: they are measured", "Quantitative: you can add them"],
            "Jersey numbers only name the players. Adding them or finding their mean makes no sense, "
            "so they are labels: qualitative data, even though they look like numbers."),
        mcq("Students’ heights are grouped into intervals: 130 to 140 cm, 140 to 150 cm, and so on. Which graph fits best?",
            "Histogram", ["Pictograph", "Circle graph", "Bar graph with gaps"],
            "Height is continuous data. A histogram shows continuous data in equal intervals, with bars that touch."),
        mcq("Why do the bars of a histogram touch?", "The data is continuous",
            ["The data is counted", "To save space", "The bars are equal"],
            "In a histogram, one interval ends where the next begins (140 cm is the end of one and the start of the next). "
            "There are no gaps in continuous data, so there are no gaps between the bars."),
        mcq("Which data is best shown on a broken-line graph?", "A puppy’s mass each week",
            ["Favourite fruits", "Colours of cars", "Each student’s birth month"],
            "A broken-line graph shows how continuous data changes over time. The puppy’s mass changes from week to week. "
            "The other data is categories, so a bar graph fits better."),
        mcq("Maya records how many laps each student skates and how long each lap takes. Which is true?",
            "Laps: discrete. Time: continuous",
            ["Laps: continuous. Time: discrete", "Both are discrete", "Both are continuous"],
            "Laps are counted in whole numbers (discrete). Time is measured and can be any value (continuous)."),
    ]
    return {"title": "Discrete or continuous data", "items": its}


# ------------------------------------------------------------ set 2: histograms and broken-line graphs
def set_read():
    its = []
    S = lambda x: unit(x, "student", "students")
    f = fig(run_svg())
    assert sum(RUN_F) == 30
    its.append(mcqv(f + "How many students took from 6 to 7 minutes?", RUN_F[2], [RUN_F[3], RUN_F[1], 10], S,
                    "Find the bar between 6 and 7 on the time axis. It reaches 9. "
                    "(7 is the next bar, from 7 to 8 minutes, 6 is the bar before, and 10 is the labelled line above the bar.)"))
    its.append(mcq(f + "Which interval has the most students?", "6 to 7 minutes",
                   ["9 to 10 minutes", "5 to 6 minutes", "7 to 8 minutes"],
                   "The tallest bar is between 6 and 7 minutes (9 students). "
                   "The interval with the most data is not the one with the biggest times."))
    its.append(mcqv(f + "How many students ran 1 km in less than 6 minutes?", RUN_F[0] + RUN_F[1],
                    [RUN_F[1], sum(RUN_F[:3]), RUN_F[0]], S,
                    "Less than 6 minutes means the bars from 4 to 5 and from 5 to 6: 2 + 6 = 8. "
                    "(17 also adds the 6 to 7 bar.)"))
    its.append(mcqv(f + "How many students ran altogether?", sum(RUN_F), [max(RUN_F), len(RUN_F), 10], S,
                    "Add all the bars: 2 + 6 + 9 + 7 + 4 + 2 = 30. (9 is only the tallest bar, and 6 is the number of bars.)"))
    its.append(mcqv(f + "How many students took 8 minutes or more?", RUN_F[4] + RUN_F[5],
                    [RUN_F[3] + RUN_F[4] + RUN_F[5], RUN_F[4], RUN_F[5]], S,
                    "8 minutes or more means the bars from 8 to 9 and from 9 to 10: 4 + 2 = 6. "
                    "(13 also adds the 7 to 8 bar.)"))
    its.append(mcq(f + "What was the fastest time?", "You cannot tell exactly",
                   ["4 minutes", "5 minutes", "10 minutes"],
                   "The first bar shows that 2 students took from 4 to 5 minutes. A histogram groups the data, "
                   "so it does not show each exact time."))
    f = fig(ht_svg())
    assert sum(HT_F) == 30
    its.append(mcqv(f + "How many students are at least 150 cm tall?", HT_F[2] + HT_F[3],
                    [HT_F[2], HT_F[1] + HT_F[2] + HT_F[3], HT_F[3]], S,
                    "At least 150 cm means the bars from 150 to 160 and from 160 to 170: 12 + 5 = 17. "
                    "(27 also adds the 140 to 150 bar.)"))
    its.append(mcqv(f + "How many students are shorter than 150 cm?", HT_F[0] + HT_F[1],
                    [HT_F[1], HT_F[0] + HT_F[1] + HT_F[2], sum(HT_F)], S,
                    "Shorter than 150 cm means the bars from 130 to 140 and from 140 to 150: 3 + 10 = 13. "
                    "(10 is only one bar.)"))
    cum = [sum(HT_F[:i + 1]) for i in range(4)]
    assert cum == [3, 13, 25, 30]
    its.append(mcq(f + "Which interval has the median height?", "150 to 160 cm",
                   ["140 to 150 cm", "160 to 170 cm", "130 to 140 cm"],
                   "There are 30 students, so the median is between the 15th and 16th heights in order. "
                   "The first two bars hold 3 + 10 = 13 students, so the 14th to 25th students are in the 150 to 160 bar."))
    its.append(mcq(f + "What fraction of the students are 160 cm or taller?",
                   "<span class='fr'><span class='fn'>1</span><span class='fd'>6</span></span>",
                   ["<span class='fr'><span class='fn'>1</span><span class='fd'>5</span></span>",
                    "<span class='fr'><span class='fn'>2</span><span class='fd'>5</span></span>",
                    "<span class='fr'><span class='fn'>1</span><span class='fd'>4</span></span>"],
                   "5 of the 30 students are in the 160 to 170 bar. 5 out of 30 = 1 out of 6. "
                   "(1/5 comes from 5 out of 25, 2/5 reads the 150 to 160 bar (12 out of 30), and 1/4 counts the bars, not the students.)"))
    f = fig(temp_svg())
    T = lambda x: "%s °C" % fmt(x)
    its.append(mcq(f + "What was the temperature at noon?", T(-10), [T(10), T(-12), T(-8)],
                   "Go up from “noon” to the point, then across to the scale. The point is on the line for −10, "
                   "below 0, so it is −10 °C. (10 °C forgets the minus sign.)"))
    its.append(mcq(f + "At what time was it warmest?", "2 p.m.", ["8 a.m.", "6 p.m.", "noon"],
                   "The warmest temperature is the highest point on the graph: −6 °C at 2 p.m. "
                   "(At 8 a.m. it was −18 °C. 18 is the biggest number, but −18 °C is the coldest.)"))
    its.append(mcqv(f + "By how many degrees did the temperature rise from 8 a.m. to 2 p.m.?", 12, [24, 6, 18],
                    lambda x: "%s °C" % fmt(x),
                    "From −18 °C up to −6 °C: count up the scale. −18 to −6 is 12 degrees. "
                    "(24 adds 18 and 6, as if one were above 0.)"))
    its.append(mcq(f + "Between which two times did the temperature drop the most?", "4 p.m. to 6 p.m.",
                   ["2 p.m. to 4 p.m.", "8 a.m. to 10 a.m.", "noon to 2 p.m."],
                   "Look for the steepest line going down. From 4 p.m. to 6 p.m. it fell from −8 °C to −12 °C (4 degrees). "
                   "From 2 p.m. to 4 p.m. it fell only 2 degrees. In the morning it was rising."))
    its.append(mcq(f + "Use the line to estimate the temperature at 9 a.m.", T(-16), [T(16), T(-14), T(-18)],
                   "9 a.m. is halfway between 8 a.m. (−18 °C) and 10 a.m. (−14 °C). The line there is at about −16 °C."))
    its.append(mcq(f + "Why are the points on this graph joined with lines?", "The temperature changes all the time",
                   ["The data is counted", "Each point is a category", "To make the graph look neat"],
                   "Temperature is continuous: it has a value at every moment, not only at the times measured. "
                   "The lines show how it changed between the points."))
    f = fig(sun_svg())
    C = lambda x: "%s cm" % fmt(x)
    its.append(mcqv(f + "How tall was the sunflower in week 4?", SUN[3], [SUN[2], SUN[4], 45], C,
                    "Go up from week 4 to the point, then across: it is on the line for 40 cm."))
    its.append(mcqv(f + "How much did the sunflower grow from week 3 to week 4?", SUN[3] - SUN[2],
                    [SUN[3], SUN[3] + SUN[2], 10], C,
                    "Week 3: 25 cm. Week 4: 40 cm. Growth = 40 − 25 = 15 cm. (40 is the height, not the growth.)"))
    g = [b - a for a, b in zip(SUN, SUN[1:])]
    assert g == [5, 10, 15, 15, 20]
    its.append(mcq(f + "In which week did the sunflower grow the most?", "Week 5 to week 6",
                   ["Week 4 to week 5", "Week 1 to week 2", "Week 3 to week 4"],
                   "The steepest part of the line shows the most growth. Week 5 to week 6: 75 − 55 = 20 cm. "
                   "Every other week it grew 15 cm or less."))
    its.append(mcqv(f + "How much did the sunflower grow from week 1 to week 6?", SUN[5] - SUN[0],
                    [SUN[5], SUN[5] + SUN[0], sum(g[:-1])], C,
                    "Week 6: 75 cm. Week 1: 10 cm. 75 − 10 = 65 cm. (75 cm is its height, which includes the 10 cm it already had.)"))
    return {"title": "Read histograms and broken-line graphs", "items": its}


# ------------------------------------------------------------ set 3: mean, median, mode and range
def e_sort(v):
    return "In order: %s." % lst(sorted(v))


def set_mmmr():
    its = []
    g = [3, 5, 2, 5, 7, 1, 5, 4]
    assert modes(g) == [5] and g.count(5) == 3
    its.append(mcqv("Goals scored by the school hockey team in 8 games:<br><b>%s</b><br>What is the mode?" % lst(g), 5,
                    [7, 3, F(9, 2)], lambda x: unit(x, "goal", "goals"),
                    "The mode is the value that appears most often. 5 appears 3 times, so the mode is 5 goals. "
                    "(7 is the highest value, 3 is how many times 5 appears, and 4.5 is the median.)"))
    v = [12, 7, 15, 9, 20]
    assert median(v) == 12 and mean(v) == F(63, 5)
    its.append(mcqv("Minutes 5 students spent reading:<br><b>%s</b><br>What is the median?" % lst(v), 12,
                    [15, 13, F(63, 5)], lambda x: unit(x, "minute", "minutes"),
                    e_sort(v) + " The middle value is 12. (15 is the middle of the list before it was put in order, "
                    "13 is the range, and 12.6 is the mean.)"))
    v = [4, 9, 6, 3, 8, 10]
    assert median(v) == 7
    its.append(mcqv("Laps skated by 6 students:<br><b>%s</b><br>What is the median?" % lst(v), 7,
                    [F(9, 2), 14, 6], lambda x: unit(x, "lap", "laps"),
                    e_sort(v) + " With 6 values there are two middle values, 6 and 8. "
                    "The median is halfway between them: (6 + 8) ÷ 2 = 7. (4.5 uses 6 and 3 from the unordered list, "
                    "and 14 forgets to divide by 2.)"))
    v = [12, 15, 9, 14, 10]
    assert mean(v) == 12
    its.append(mcqv("Cans collected by 5 students for the food drive:<br><b>%s</b><br>What is the mean?" % lst(v), 12,
                    [60, 10, 6], lambda x: unit(x, "can", "cans"),
                    "Add: 12 + 15 + 9 + 14 + 10 = 60. There are 5 values, so 60 ÷ 5 = 12. "
                    "(60 is the total, 10 divides by 6, and 6 is the range.)"))
    v = [F("3.5"), F("4.2"), F("2.8"), F("5.1")]
    assert mean(v) == F("3.9")
    its.append(mcqv("Rain that fell on 4 days in Vancouver (mm):<br><b>%s</b><br>What is the mean?" % lst(v), F("3.9"),
                    [F("15.6"), F("3.12"), F("2.3")], lambda x: "%s mm" % fmt(x),
                    "Add: 3.5 + 4.2 + 2.8 + 5.1 = 15.6. Divide by 4: 15.6 ÷ 4 = 3.9 mm. "
                    "(3.12 divides by 5, and 2.3 is the range.)"))
    v = [-3, 4, -7, 2, 0, 5]
    assert rng(v) == 12
    its.append(mcqv("Temperatures at 7 a.m. in Ottawa for 6 days in March (°C):<br><b>%s</b><br>What is the range?" % lst(v),
                    12, [2, 5, 8], lambda x: "%s °C" % fmt(x),
                    "Highest 5 °C, lowest −7 °C. From −7 up to 0 is 7 degrees, and from 0 up to 5 is 5 more: 7 + 5 = 12 °C. "
                    "(2 ignores the minus sign: 7 − 5. 8 uses −3 instead of the lowest value, −7.)"))
    v = [11, 14, 11, 16, 13, 11, 14]
    assert modes(v) == [11]
    its.append(mcqv("Ages of the swimmers in a lesson:<br><b>%s</b><br>What is the mode?" % lst(v), 11,
                    [16, 3, 14], lambda x: unit(x, "year", "years"),
                    "11 appears 3 times, more than any other age, so the mode is 11 years. "
                    "(16 is the highest age, and 3 is how many times 11 appears.)"))
    v = [2, 4, 4, 6, 7, 7, 9]
    assert modes(v) == [4, 7]
    its.append(mcq("Points scored by a basketball player in 7 games:<br><b>%s</b><br>What is the mode?" % lst(v),
                   "4 and 7", ["7 only", "9", "There is no mode"],
                   "4 appears twice and 7 appears twice. Every other value appears once. So there are two modes: 4 and 7."))
    v = [8, 3, 6, 10, 5]
    assert modes(v) == []
    its.append(mcq("Quiz scores out of 10:<br><b>%s</b><br>What is the mode?" % lst(v), "There is no mode",
                   ["10", "5", "6"],
                   "Each score appears only once, so no value appears most often. There is no mode. "
                   "(10 is the highest score, and 5 is how many scores there are.)"))
    f = fig(pets_svg())
    vals = [k for k, n in PETS.items() for _ in range(n)]
    assert len(vals) == 17 and median(vals) == 1
    its.append(mcqv(f + "Each X is one student. What is the median number of pets?", 1, [2, 6, 0],
                    lambda x: unit(x, "pet", "pets"),
                    "There are 17 X’s, so the median is the 9th value in order. Count from the left: 3 students have 0 pets, "
                    "and the next 6 have 1 pet. The 9th value is 1. (2 is the middle of the number line, not of the data.)"))
    its.append(mcqv(f + "What is the mode?", 1, [6, 4, 2], lambda x: unit(x, "pet", "pets"),
                    "The tallest stack is above 1, so the mode is 1 pet. (6 is the height of that stack, and 4 is the highest value.)"))
    v3 = [75, 82, 78]
    assert 4 * 80 - sum(v3) == 85
    its.append(mcqv("The mean of Arjun’s 4 math tests is 80. Three of his scores are 75, 82 and 78. What is the 4th score?",
                    85, [80, 235, 5], lambda x: num(x),
                    "A mean of 80 for 4 tests means the total is 4 × 80 = 320. The first three add to 75 + 82 + 78 = 235. "
                    "320 − 235 = 85. (80 is the mean, not the missing score, and 5 uses 3 × 80 instead of 4 × 80.)"))
    its.append(mcq("One very large value is added to a data set. Which measure changes the most?", "The mean",
                   ["The median", "The mode", "None of them"],
                   "The mean uses every value, so one very large value pulls it up a lot. The median only moves by one "
                   "place, and the mode usually does not change."))
    v = [12, 14, 13, 15, 46]
    assert mean(v) == 20 and median(v) == 14
    its.append(mcq("Minutes 5 students took to get to school:<br><b>%s</b><br>Which value best describes a typical time?" % lst(v),
                   "The median, 14", ["The mean, 20", "The range, 34", "The highest, 46"],
                   "46 is far from the other values (it is an outlier). It pulls the mean up to 20, which is more than 4 of the 5 times. "
                   "The median, 14, is in the middle of the usual times."))
    v = [F("4.50"), F("5.25"), F("3.75"), F("6.10"), F("5.40")]
    assert mean(v) == 5
    its.append(mcq("Leah spent this on lunch at school each day for a week:<br><b>%s</b><br>What is the mean?"
                   % ", ".join(money(x) for x in v), "$5.00", ["$25.00", "$6.25", "$5.25"],
                   "Add: 4.50 + 5.25 + 3.75 + 6.10 + 5.40 = 25.00. Divide by 5 days: $25.00 ÷ 5 = $5.00. "
                   "($6.25 divides by 4, and $5.25 is the median, not the mean.)"))
    v = [F("3.2"), F("4.8"), F("5.5"), F("2.9"), F("6.1"), F("4.5")]
    assert mean(v) == F("4.5") and rng(v) == F("3.2") and sum(v) / 5 == F("5.4")
    its.append(mcqv("Masses of 6 pumpkins (kg):<br><b>%s</b><br>What is the mean?" % lst(v), F("4.5"),
                    [F("27"), F("5.4"), F("3.2")], lambda x: "%s kg" % fmt(x),
                    "Add: 3.2 + 4.8 + 5.5 + 2.9 + 6.1 + 4.5 = 27. There are 6 pumpkins: 27 ÷ 6 = 4.5 kg. "
                    "(27 is the total, 5.4 divides by 5, and 3.2 is the range.)"))
    v = [F("10.8"), F("9.95"), F("11.2"), F("10.25"), F("9.7")]
    assert median(v) == F("10.25") and mean(v) == F("10.38") and rng(v) == F("1.5")
    its.append(mcqv("Times for 5 swimmers in a race (seconds):<br><b>%s</b><br>What is the median?" % lst(v), F("10.25"),
                    [F("11.2"), F("10.38"), F("1.5")], lambda x: "%s s" % fmt(x),
                    e_sort(v) + " The middle value is 10.25 s. (11.2 is the middle of the unordered list, 10.38 is the mean, "
                    "and 1.5 is the range.)"))
    v = [0, 5, 0, 9, 6, 4]
    assert mean(v) == 4 and F(sum(v), 4) == 6
    its.append(mcqv("Centimetres of snow that fell each day for 6 days:<br><b>%s</b><br>What is the mean?" % lst(v), 4,
                    [6, 24, 9], lambda x: "%s cm" % fmt(x),
                    "Add: 0 + 5 + 0 + 9 + 6 + 4 = 24. There are 6 days, including the 2 days with 0 cm: 24 ÷ 6 = 4 cm. "
                    "(6 leaves out the zeros and divides by 4.)"))
    v = [2, 3, 3, 4, 13]
    assert mean(v) == 5 and median(v) == 3 and modes(v) == [3] and rng(v) == 11
    its.append(mcq("Hours of screen time for 5 students on a Saturday:<br><b>%s</b><br>Which statement is true?" % lst(v),
                   "The mean is greater than the median",
                   ["The median is 4", "The mode is 13", "The range is 13"],
                   "Mean = 25 ÷ 5 = 5. Median = 3 (the middle value). Mode = 3. Range = 13 − 2 = 11. "
                   "The value 13 pulls the mean above the median."))
    v = [152, 168, 147, 175, 160, 149]
    assert rng(v) == 28
    its.append(mcqv("Heights of 6 basketball players (cm):<br><b>%s</b><br>What is the range?" % lst(v), 28,
                    [175, 3, 26], lambda x: "%s cm" % fmt(x),
                    "Highest 175 cm, lowest 147 cm. Range = 175 − 147 = 28 cm. "
                    "(152 − 149 = 3 uses the first and last values, and 175 − 149 = 26 misses the lowest, 147.)"))
    return {"title": "Mean, median, mode and range", "items": its}


# ------------------------------------------------------------ set 4: compare two data sets
def set_compare():
    its = []
    L = [4, 6, 5, 7, 5, 3]
    S = [9, 2, 1, 8, 8, 2]
    assert mean(L) == mean(S) == 5 and median(L) == 5 and median(S) == 5 and rng(L) == 4 and rng(S) == 8
    assert modes(L) == [5] and modes(S) == [2, 8]
    q0 = ("Goals scored by two ringette teams in 6 games:<br><b>Lightning: %s</b><br><b>Storm: %s</b><br>" % (lst(L), lst(S)))
    G = lambda x: unit(x, "goal", "goals")
    its.append(mcqv(q0 + "What is the mean for the Lightning?", 5, [30, 6, 4], G,
                    "Add: 4 + 6 + 5 + 7 + 5 + 3 = 30. Divide by 6 games: 30 ÷ 6 = 5 goals. "
                    "(30 is the total, 6 divides by 5, and 4 is the range.)"))
    its.append(mcqv(q0 + "What is the median for the Storm?", 5, [F(9, 2), 10, 8], G,
                    "In order: 1, 2, 2, 8, 8, 9. The two middle values are 2 and 8: (2 + 8) ÷ 2 = 5. "
                    "(4.5 uses 1 and 8 from the unordered list, and 10 forgets to divide by 2.)"))
    its.append(mcq(q0 + "What is the mode for the Storm?", "2 and 8", ["9", "2 only", "There is no mode"],
                   "2 appears twice and 8 appears twice, so the Storm has two modes: 2 and 8. (9 is the highest value.)"))
    its.append(mcq(q0 + "What is the range for each team?", "Lightning 4, Storm 8",
                   ["Lightning 7, Storm 9", "Lightning 8, Storm 4", "Lightning 5, Storm 5"],
                   "Lightning: 7 − 3 = 4. Storm: 9 − 1 = 8. (7 and 9 are only the highest values, and 5 is the mean.)"))
    its.append(mcq(q0 + "Which team’s scores are more consistent?", "Lightning: smaller range",
                   ["Storm: bigger range", "Storm: highest score", "Neither: same mean"],
                   "Consistent means the values are close together. The Lightning’s range is 4 and the Storm’s is 8, "
                   "so the Lightning’s scores are closer together."))
    its.append(mcq(q0 + "Which conclusion is supported by the data?", "Both teams average 5 goals a game",
                   ["The Storm is better: it scored 9", "The Lightning scored more goals", "The Storm never scored under 2"],
                   "Both teams scored 30 goals in 6 games, so both means are 5. One high game (9) does not make the Storm better, "
                   "and the Storm scored 1 goal in one game."))
    A = [14, 16, 15, 17, 16, 18, 16]
    B = [12, 20, 15, 21, 11, 19, 14]
    assert mean(A) == mean(B) == 16 and median(A) == 16 and median(B) == 15 and rng(A) == 4 and rng(B) == 10
    q1 = ("Laps skated in 10 minutes by students in two gym classes:<br><b>6A: %s</b><br><b>6B: %s</b><br>" % (lst(A), lst(B)))
    Lp = lambda x: unit(x, "lap", "laps")
    its.append(mcqv(q1 + "What is the median for 6B?", 15, [21, 16, 10], Lp,
                    "In order: 11, 12, 14, 15, 19, 20, 21. The middle (4th) value is 15. "
                    "(21 is the middle of the unordered list, 16 is the mean, and 10 is the range.)"))
    its.append(mcqv(q1 + "What is the mean for 6A?", 16, [112, 14, 18], Lp,
                    "Add: 14 + 16 + 15 + 17 + 16 + 18 + 16 = 112. Divide by 7: 112 ÷ 7 = 16 laps. "
                    "(14 divides by 8, and 18 is the highest value.)"))
    its.append(mcqv(q1 + "What is the range for 6B?", 10, [21, 2, 4], Lp,
                    "Highest 21, lowest 11. Range = 21 − 11 = 10. (14 − 12 = 2 uses the last and first values, "
                    "and 4 is the range for 6A.)"))
    its.append(mcq(q1 + "Which sentence compares the two classes correctly?",
                   "Same mean, but 6B is more spread out",
                   ["Same mean, but 6A is more spread out", "6B has the higher mean", "6B has the higher median"],
                   "Both means are 112 ÷ 7 = 16. The ranges are 4 (6A) and 10 (6B), so 6B is more spread out. "
                   "The medians are 16 (6A) and 15 (6B)."))
    its.append(mcq(q1 + "Which class has the higher median, and by how much?", "6A, by 1 lap",
                   ["6B, by 1 lap", "6A, by 6 laps", "Neither: same median"],
                   "6A in order: 14, 15, 16, 16, 16, 17, 18, so its median is 16. 6B’s median is 15. 16 − 15 = 1 lap. "
                   "(6 laps compares the ranges, 10 − 4.)"))
    f = fig(bean_svg())
    C = lambda x: "%s cm" % fmt(x)
    its.append(mcq(f + "In which week were the two plants the same height?", "Week 1", ["Week 5", "Week 2", "Week 3"],
                   "The two lines start at the same point: both plants were 4 cm in week 1. After that, Plant A is always taller."))
    its.append(mcqv(f + "How much taller was Plant A than Plant B in week 5?", BEAN_A[4] - BEAN_B[4],
                    [BEAN_A[4] + BEAN_B[4], BEAN_A[4], BEAN_A[3] - BEAN_B[3]], C,
                    "Week 5: Plant A is 26 cm and Plant B is 16 cm. 26 − 16 = 10 cm. (8 cm is the gap in week 4.)"))
    its.append(mcq(f + "Which plant grew faster?", "Plant A: its line is steeper",
                   ["Plant B: its line is lower", "Neither: they started the same", "Plant B: it grew more each week"],
                   "A steeper line means faster growth. Plant A grew 26 − 4 = 22 cm, and Plant B grew only 16 − 4 = 12 cm."))
    gr = F(BEAN_A[4] - BEAN_A[0], 4)
    assert gr == F("5.5")
    its.append(mcqv(f + "What is the mean growth of Plant A per week, from week 1 to week 5?", gr,
                    [F(BEAN_A[4], 4), F(22, 5), 22], lambda x: "%s cm" % fmt(x),
                    "Plant A grew 26 − 4 = 22 cm. From week 1 to week 5 is 4 weeks: 22 ÷ 4 = 5.5 cm per week. "
                    "(4.4 divides by 5, but there are only 4 weeks of growth. 6.5 forgets the 4 cm it started with.)"))
    K = [18, 17, 19, 18, 3]
    Am = [16, 16, 15, 17, 16]
    assert mean(K) == 15 and median(K) == 18 and mean(Am) == 16 and median(Am) == 16 and rng(K) == 16 and rng(Am) == 2
    q2 = ("Quiz scores out of 20:<br><b>Kai: %s</b><br><b>Amira: %s</b><br>" % (lst(K), lst(Am)))
    its.append(mcq(q2 + "Who has the higher mean?", "Amira: 16", ["Kai: 18", "Kai: 15", "They are the same"],
                   "Kai: 75 ÷ 5 = 15. Amira: 80 ÷ 5 = 16. Amira’s mean is higher. (18 is Kai’s median and mode.)"))
    its.append(mcq(q2 + "Who has the higher median?", "Kai: 18", ["Amira: 16", "Kai: 3", "They are the same"],
                   "Kai in order: 3, 17, 18, 18, 19, so his median is 18. Amira in order: 15, 16, 16, 16, 17, so hers is 16."))
    its.append(mcq(q2 + "Kai was sick on the day he scored 3. Which measure best shows how he usually does?",
                   "The median: 3 is an outlier", ["The mean: it uses every score", "The range: 16",
                                                   "The lowest score: 3"],
                   "3 is far from Kai’s other scores (17 to 19). It pulls his mean down to 15. "
                   "The median, 18, is not affected much by one outlier."))
    its.append(mcq(q2 + "Whose scores are more consistent?", "Amira: range 2", ["Kai: range 16", "Kai: median 18",
                                                                                 "Amira: mean 16"],
                   "Amira’s range is 17 − 15 = 2 and Kai’s is 19 − 3 = 16. A smaller range means the scores are closer together."))
    assert F(120, 24) == 5 and F(108, 18) == 6
    its.append(mcq("For the food drive, 6A (24 students) collected 120 cans. 6B (18 students) collected 108 cans. "
                   "Which class collected more cans per student?", "6B: 6 per student",
                   ["6A: 5 per student", "6A: it has the bigger total", "They are the same"],
                   "Use the mean, because the classes are different sizes. 6A: 120 ÷ 24 = 5. 6B: 108 ÷ 18 = 6. "
                   "6B collected more per student, even though its total is smaller."))
    return {"title": "Compare two data sets", "items": its}


# ------------------------------------------------------------ set 5: misleading graphs and conclusions
def set_claims():
    its = []
    f = fig(vote_svg())
    a, b = VOTE[1]
    assert (a - 40) == 3 * (b - 40)
    V = lambda x: unit(x, "vote", "votes")
    its.append(mcqv(f + "How many students voted for the science centre?", a, [a - 40, b, 48], V,
                    "The bar reaches the line for 46. (6 is the height above the bottom of the scale, which starts at 40, not 0.)"))
    its.append(mcqv(f + "How many more votes did the science centre get than the zoo?", a - b, [a + b, a - 40, 2], V,
                    "46 − 42 = 4 votes. (6 reads only the part of the bar above 40, and 2 is the zoo bar above 40.)"))
    its.append(mcq(f + "The science centre bar looks 3 times as tall. Did it get 3 times as many votes?",
                   "No: 46 is not 3 × 42", ["Yes: its bar is 3 times as tall", "Yes: 46 is more than 42",
                                            "No: the zoo got more votes"],
                   "3 × 42 = 126, but the science centre got only 46 votes. The bars start at 40, "
                   "so we see only 6 and 2 of the votes: that makes one look 3 times the other."))
    its.append(mcq(f + "Why does this graph make the difference look big?", "The scale starts at 40, not 0",
                   ["The bars are the same colour", "The graph has a title", "The scale goes up by 1s"],
                   "When the scale starts at 40, the bottom part of every bar is cut off. The small difference (4 votes) then looks huge."))
    its.append(mcqv(f + "To draw a fair bar graph of this data, where should the scale start?", 0, [40, 42, 46],
                    lambda x: num(x),
                    "Bar heights are fair to compare only when the scale starts at 0. Then the bars would be 46 and 42 high, "
                    "and look almost the same."))
    f = fig(tfr_svg())
    d = TFR[-1] - TFR[0]
    assert d == 120
    D_ = lambda x: "$" + num(x)
    its.append(mcq(f + "How much more money was raised in 2026 than in 2022?", D_(d),
                   [D_(TFR[-1]), D_(TFR[-1] - 1400), D_(TFR[-1] - TFR[-2])],
                   "2026: $1560. 2022: $1440. $1560 − $1440 = $120. ($160 measures from $1400, where the scale starts, "
                   "and $40 is only the last year.)"))
    its.append(mcq(f + "A poster says, “Our school more than doubled the money it raised!” Is this supported?",
                   "No: $1560 is less than 2 × $1440", ["Yes: the line rises steeply", "Yes: $1560 is more than $1440",
                                                        "No: the money went down"],
                   "Doubling $1440 gives $2880. The school raised $1560, an increase of only $120. "
                   "The scale starts at $1400, so the line looks steeper than it is."))
    its.append(mcq("A bar graph’s scale is labelled 0, 5, 10, 50, 100, with equal spaces between the labels. "
                   "Why is it misleading?", "The equal spaces show unequal amounts",
                   ["It does not start at 0", "The numbers are too big", "It goes up by 5s"],
                   "The space from 0 to 5 is the same as the space from 10 to 50, but one is 5 and the other is 40. "
                   "Bars on this scale cannot be compared fairly."))
    its.append(mcq("A broken-line graph shows a town’s population in 2010, 2020, 2022, 2024 and 2026, "
                   "with equal spaces between the years. Why is it misleading?",
                   "The years are not equally far apart", ["It shows five years", "Population is discrete",
                                                           "The line goes up"],
                   "From 2010 to 2020 is 10 years, but the other gaps are 2 years. Equal spaces make 10 years of change "
                   "look like 2 years."))
    its.append(mcq("A website says, “Kids love broccoli! 3 out of 4 kids we asked said yes.” They asked only 4 kids. "
                   "Why is this claim weak?", "The sample is far too small",
                   ["3 out of 4 is less than half", "Broccoli is a vegetable", "They should have asked 3 kids"],
                   "4 kids is a tiny sample. A different 4 kids could give a very different answer. (3 out of 4 is more than half.)"))
    its.append(mcq("A survey at a hockey arena found that 45 of the 50 people asked said hockey is their favourite sport. "
                   "A headline says, “90% of Canadians love hockey most!” What is the main problem?",
                   "People at an arena likely like hockey", ["45 out of 50 is not 90%", "50 people is too many",
                                                             "Hockey is not a sport"],
                   "The sample is biased: people at a hockey arena are more likely to choose hockey. "
                   "45 out of 50 is 90%, but only for those 50 people."))
    al = [10, 10, 12, 15, 8, 95]
    assert mean(al) == 25 and median(al) == 11
    its.append(mcq("Weekly allowances of 6 friends: %s. Owen says, “The typical allowance in our group is $25.” "
                   "Which is a better typical value?" % ", ".join("$" + num(x) for x in al),
                   "The median, $11", ["The mean, $25", "The highest, $95", "The range, $87"],
                   "The mean is $150 ÷ 6 = $25, but 5 of the 6 friends get $15 or less. The $95 pulls the mean up. "
                   "In order: 8, 10, 10, 12, 15, 95, so the median is (10 + 12) ÷ 2 = $11."))
    assert 9 * 2 < 28
    its.append(mcq("In a class of 28, pepperoni pizza got 9 votes, more than any other kind. "
                   "Liam says, “Most of the class likes pepperoni best.” Is this supported?",
                   "No: 9 of 28 is less than half", ["Yes: pepperoni is the mode", "Yes: 9 is the most votes",
                                                     "No: pepperoni is not the mode"],
                   "Pepperoni is the mode, but “most” means more than half. Half of 28 is 14, and only 9 students chose pepperoni."))
    assert F(60, 600) == F(1, 10) and F(45, 150) == F(3, 10)
    its.append(mcq("At School A, 60 of the 600 students walk to school. At School B, 45 of the 150 students walk. "
                   "At which school does a greater part of the students walk?", "School B: 30%",
                   ["School A: 60 is more", "School A: 10%", "They are the same"],
                   "Compare parts of each school, not totals. A: 60 ÷ 600 = 10%. B: 45 ÷ 150 = 30%. "
                   "School B has fewer walkers, but a greater part of its students walk."))
    its.append(mcq(fig(run_svg()) + "A newsletter says, “Most of our students ran 1 km in under 6 minutes.” Is this supported?",
                   "No: only 8 of the 30 did", ["Yes: the first bar is at 4", "Yes: 6 students took 5 to 6 minutes",
                                                "No: nobody did"],
                   "Under 6 minutes means the first two bars: 2 + 6 = 8 students. That is 8 of 30, less than half."))
    its.append(mcq(fig(temp_svg()) + "Which conclusion is supported by this graph?", "It stayed below 0 °C all day",
                   ["It was warmest at 8 a.m.", "It got colder all day", "It was 18 °C at 8 a.m."],
                   "Every point is below the 0 line, so the temperature stayed below 0 °C. It rose until 2 p.m., "
                   "then fell. At 8 a.m. it was −18 °C, the coldest."))
    its.append(mcq("The mean number of goals for a hockey player is 2.5 a game. Hana says, “So in one game, the player "
                   "scored 2.5 goals.” What is wrong?", "A mean does not have to be a data value",
                   ["The mean must be a whole number", "Nothing: she is right", "The mean is the most common score"],
                   "Goals are discrete: a player scores 2 or 3, never 2.5. The mean shares the total equally, "
                   "so it can be a value that never happened. For example, 2 and 3 goals have a mean of 2.5."))
    its.append(mcq("A cereal box says, “Kids’ favourite! Chosen by 4 out of 5 kids.” Which question best checks this claim?",
                   "How many kids were asked, and who?", ["What colour is the box?", "How much does it cost?",
                                                           "Is 4 more than 5?"],
                   "A claim like this depends on the sample. If only 5 kids were asked, or they were chosen by the cereal maker, "
                   "the claim is weak."))
    its.append(mcq("An ad shows sales doubling with two maple leaf pictures. The second leaf is twice as wide and twice as tall. "
                   "Why is this misleading?", "The big leaf looks 4 times as big",
                   ["It should be 3 times as tall", "Maple leaves are not data", "Sales did not change"],
                   "Doubling both the width and the height makes the area 2 × 2 = 4 times as big. "
                   "The eye sees the area, so sales look 4 times bigger instead of 2 times."))
    v = [85, 120, 96, 139]
    assert mean(v) == 110
    its.append(mcqv("The school play sold tickets on 4 nights: %s. What is the mean number of tickets per night?" % lst(v),
                    110, [440, 88, 54], lambda x: unit(x, "ticket", "tickets"),
                    "Add: 85 + 120 + 96 + 139 = 440. Divide by 4 nights: 440 ÷ 4 = 110 tickets. "
                    "(88 divides by 5, and 54 is the range.)"))
    return {"title": "Misleading graphs and conclusions", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


LH_E = [20, 30, 40, 50, 60]
LH_F = [2, 7, 9, 4]
LT_X = ["Mon", "Tue", "Wed", "Thu", "Fri"]
LT = [-4, -8, -2, 2, 0]
LEX = [6, 3, 8, 3, 5]
LVOTE = (["Pizza", "Tacos"], [62, 54])


def body_html():
    assert sum(LH_F) == 22
    assert mean(LEX) == 5 and median(LEX) == 5 and modes(LEX) == [3] and rng(LEX) == 5
    assert (LVOTE[1][0] - 50) == 3 * (LVOTE[1][1] - 50)
    return (
        "<h2>Discrete and continuous data</h2>"
        "<p><b>Discrete</b> data is counted, so it has only certain values, such as 0, 1, 2, 3 goals. "
        "<b>Continuous</b> data is measured, so it can be any value in a range, such as 148.6 cm or 41.35 s.</p>" +
        table(["Kind of data", "How you get it", "Examples", "Good graph"], [
            ["Discrete", "Count", "Pets, goals, students on a bus", "Bar graph, line plot"],
            ["Continuous", "Measure", "Height, mass, time, temperature", "Histogram, broken-line graph"],
        ]) +
        "<h2>Histograms and broken-line graphs</h2>"
        "<p>A <b>histogram</b> groups continuous data into equal intervals. The bars touch, because one interval "
        "ends where the next one begins.</p>"
        "<figure class='sn-fig'>" + hist_svg("Time spent on homework one evening", "Time (minutes)", "Students",
                                             LH_E, LH_F, 10, 2, gy=10) +
        "<figcaption>The bar from 30 to 40 shows 7 students who spent 30 minutes up to (not including) 40 minutes.</figcaption></figure>" +
        ex("Example 1", "How many students spent 40 minutes or more on homework?",
           "40 minutes or more means the bars from 40 to 50 and from 50 to 60: 9 + 4 = 13.", "13 students") +
        "<p>A <b>broken-line graph</b> shows how continuous data changes over time. The points are joined by straight "
        "lines. A steep line means a fast change.</p>"
        "<figure class='sn-fig'>" + bline_svg("Temperature at 7 a.m. in Sudbury", "Day", "Temperature (°C)", LT_X, [LT],
                                              -12, 4, 2, 4, gy=14, slot=56) +
        "<figcaption>The temperature fell from Monday to Tuesday, then rose until Thursday.</figcaption></figure>" +
        ex("Example 2", "By how many degrees did the temperature rise from Tuesday to Thursday?",
           "Tuesday −8 °C, Thursday 2 °C. From −8 up to 0 is 8 degrees, and from 0 up to 2 is 2 more: 8 + 2 = 10.",
           "10 °C") +
        "<h2>Mean, median, mode and range</h2>" +
        table(["Measure", "How to find it", "For 6, 3, 8, 3, 5"], [
            ["Mean", "Add the values, then divide by how many there are", "25 ÷ 5 = 5"],
            ["Median", "Put the values in order and take the middle one", "3, 3, 5, 6, 8 → 5"],
            ["Mode", "The value that appears most often", "3"],
            ["Range", "Highest − lowest", "8 − 3 = 5"],
        ]) +
        "<p>With an even number of values, the median is halfway between the two middle values. "
        "One very large or very small value (an <b>outlier</b>) pulls the mean toward it, so the median often "
        "describes a typical value better.</p>"
        "<p>To <b>compare two data sets</b>, compare their means or medians (which is higher?) and their ranges "
        "(which is more spread out?). A smaller range means the data is more consistent.</p>"
        "<h2>Misleading graphs</h2>"
        "<p>Before you believe a graph or a claim, check: Does the scale start at 0? Are the spaces on the scale equal? "
        "How many people were asked, and who?</p>"
        "<figure class='sn-fig'>" + bar_svg("Favourite lunch", "Lunch", "Votes", LVOTE[0], LVOTE[1], 50, 66, 2, 4, gy=10) +
        "<figcaption>The scale starts at 50, so the pizza bar looks 3 times as tall. Really, pizza has only 62 − 54 = 8 more votes.</figcaption></figure>" +
        ex("Example 3", "A sign says, “Everyone loves the new playground: 100% of the kids we asked said yes!” "
           "They asked 3 kids. Is the claim supported?",
           "3 kids is far too small a sample to speak for everyone.", "No") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Giving the highest value as the mode", "The mode is the value that appears most often"],
            ["Finding the median without putting the values in order", "Order the values first, then take the middle"],
            ["Dividing by the wrong number for the mean", "Divide by how many values there are, including any zeros"],
            ["Giving the biggest number as the range", "Range = highest − lowest"],
            ["Judging bars by height when the scale does not start at 0", "Read the real values and subtract"],
            ["Trusting a survey of a few people, or of people chosen in one place", "Ask how many and who was asked"],
        ])
    )


FAQ = [
    {"q": "What do Grade 6 students learn about data in the Ontario math curriculum?",
     "a": "In Grade 6, students tell discrete from continuous data, read and make histograms and broken-line graphs, find the mean, median, mode and range, compare data sets, and spot misleading graphs. Data questions also appear on the Grade 6 EQAO math assessment."},
    {"q": "What is the difference between discrete and continuous data?",
     "a": "Discrete data is counted and has only certain values, such as the number of pets. Continuous data is measured and can be any value in a range, such as height, mass, time or temperature."},
    {"q": "What is the difference between a histogram and a bar graph?",
     "a": "A histogram shows continuous data grouped into equal intervals, so its bars touch. A bar graph shows categories or discrete data, so its bars have gaps between them."},
    {"q": "How can a graph be misleading?",
     "a": "A scale that does not start at 0 makes small differences look big, and unequal spaces on a scale distort the data. Conclusions can also mislead when the sample is very small or the people asked were not chosen fairly."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly: 5 at each of the 4 positions in every set."""
    for s in sets:
        items = s["items"]
        targets = [i for i in range(4) for _ in range(5)]
        rnd.shuffle(targets)
        for it, t in zip(items, targets):
            corr = it["c"][it["a"]]
            wrong = [c for k, c in enumerate(it["c"]) if k != it["a"]]
            rnd.shuffle(wrong)
            wrong.insert(t, corr)
            it["c"] = wrong
            it["a"] = t
        final = [sum(1 for it in items if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


def gen_unit():
    rnd = random.Random(36817)
    sets = [set_kinds(), set_read(), set_mmmr(), set_compare(), set_claims()]
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
        "country": "ca-on", "subject": "math", "grade": "grade-6", "slug": "data-and-graphs", "sort": 17,
        "updated": UPDATED, "pdf_url": "",
        "title": "Data and Graphs: Histograms, Broken-Line Graphs, Mean, Median, Mode and Misleading Graphs",
        "seo_title": "Grade 6 Data and Graphs Worksheets: Mean, Median, Mode, Histograms (Free, Answer Key)",
        "short_title": "Data and graphs",
        "domain": "Data",
        "standard_code": "Grade 6: Data, D1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Determine the range and the measures of central tendency for data sets, and use these measures to compare data sets; analyse different sets of data presented in various ways, including in misleading graphs, by asking and answering questions about the data and drawing conclusions",
        "meta_desc": "Free Grade 6 math worksheets on data and graphs for the Ontario curriculum: discrete and continuous data, histograms, broken-line graphs, mean, median, mode and range, comparing data sets and spotting misleading graphs. 100 questions with an answer key, good EQAO practice.",
        "key_big": "Mean, median, mode and range describe a data set; check the scale before you trust a graph.",
        "key_sub": "Mean = total ÷ number of values. Median = the middle value in order. Mode = the most common value. Range = highest − lowest. Discrete data is counted; continuous data is measured.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (graphs and line plots) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "(line plot|bar graph|histogram|broken-line)")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
