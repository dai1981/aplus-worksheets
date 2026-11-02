# -*- coding: utf-8 -*-
"""
BC Grade 6 Math: Line graphs (BC Mathematics Curriculum, Grade 6: Data and probability, line graphs)
  python3 tools/gen_cabc_math_g6_line_graphs.py
Read line graphs and their scales, describe trends (increase, decrease, no change), read values between points,
choose a line graph or a bar graph, and solve problems with Vancouver rainfall and temperatures.
Climate data: Environment Canada 1981–2010 normals (Vancouver Int'l A, Kelowna A), rounded to the nearest
10 mm (rain) and 1 °C (average daily high).
Wrong answers come from real student mistakes: counting each small square as 1, reading a scale that starts at 5
as if it started at 0, reading the wrong month or the wrong line, adding instead of subtracting, choosing the highest
point instead of the steepest part, using the nearest dot instead of reading between points, and joining
categories with a line.
Canadian English. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, re, math, os, random
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
LINE1 = "#2e8b57"
LINE2 = "#c0392b"
BAR = "#2e8b57"
INK = "#2b2b2b"
GRID = "#d5ddd8"
GRID2 = "#9fb0a5"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
NBSP = " "


# ------------------------------------------------------------ helpers
def num(x):
    """BC style: 4536, 10 000 (no-break space), 4.5."""
    x = F(x)
    if x.denominator != 1:
        for k in (1, 2, 3):
            y = x * 10 ** k
            if y.denominator == 1:
                s = str(abs(y.numerator)).rjust(k + 1, "0")
                return (MINUS if x < 0 else "") + num(int(s[:-k])) + "." + s[-k:]
        raise AssertionError(x)
    v = abs(x.numerator)
    s = str(v)
    if len(s) >= 5:
        s = "{:,}".format(v).replace(",", NBSP)
    return (MINUS if x < 0 else "") + s


def unit(v, one, many):
    return "%s %s" % (num(v), one if F(v) == 1 else many)


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def mcq(q, right, wrongs, e):
    ch = [right]
    for w in wrongs:
        if plain(w) not in {plain(c) for c in ch}:
            ch.append(w)
        if len(ch) == 4:
            break
    assert len(ch) == 4, (q, right, wrongs)
    return {"q": q, "c": ch, "a": 0, "e": e}


def mcqv(q, right, wrongs, f, e, allow_zero=False):
    """Choices given as values: no two choices equal in value."""
    seen = [F(right)]
    pick = []
    for w in wrongs:
        w = F(w)
        if w in seen or (w <= 0 and not allow_zero):
            continue
        seen.append(w)
        pick.append(w)
    assert len(pick) == 3, (q, right, wrongs)
    return mcq(q, f(right), [f(w) for w in pick], e)


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


# ------------------------------------------------------------ line graphs
class LG:
    """Line graph. Labels every `lstep`, a grid line every `gstep`. One or two lines (the second is dashed)."""
    def __init__(self, title, xl, xt, yt, series, ymin, ymax, lstep, gstep, names=None, u="", gy=None, slot=46):
        self.title, self.xl, self.xt, self.yt = title, xl, xt, yt
        self.series, self.ymin, self.ymax, self.lstep, self.gstep = series, ymin, ymax, lstep, gstep
        self.names, self.u, self.gy, self.minslot = names, u, gy, slot
        for v in series:
            assert len(v) == len(xl)
            assert all(ymin <= x <= ymax for x in v)
            # every reading sits on a grid line or exactly halfway between two
            assert all((F(x) - ymin) * 2 % gstep == 0 for x in v), (title, v)
        assert (ymax - ymin) % lstep == 0 and lstep % gstep == 0 and ymin % lstep == 0

    def v(self, x):
        return "%s%s" % (num(x), self.u)

    def at(self, x, si=0):
        return self.series[si][self.xl.index(x)]

    def svg(self):
        fs = 14
        nt = (self.ymax - self.ymin) // self.gstep
        gy = self.gy or max(9, min(20, int(round(150.0 / nt))))
        ph = nt * gy
        ylabs = [num(v) for v in range(self.ymin, self.ymax + 1, self.lstep)]
        slot = max(self.minslot, max(tw(c, fs) for c in self.xl) + 12)
        x0 = 24 + max(tw(c, fs) for c in ylabs) + 8
        n = len(self.xl)
        pw = slot * (n - 1)
        y0 = 34 + (22 if self.names else 0)
        yb = y0 + ph
        W = x0 + pw + tw(self.xl[-1], fs) / 2 + 8
        W = max(W, tw(self.title, 16, True) + 16)
        s = [text(W / 2, 18, self.title, 16, bold=True)]
        Y = lambda v: yb - float(F(v) - self.ymin) / self.gstep * gy
        for k in range(nt + 1):
            v = self.ymin + k * self.gstep
            major = v % self.lstep == 0
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%s'/>"
                     % (x0, Y(v), x0 + pw, Y(v), GRID2 if major else GRID, "1" if major else "0.8"))
            if major:
                s.append(text(x0 - 5, Y(v) + 5, num(v), fs, anchor="end"))
        for i, c in enumerate(self.xl):
            x = x0 + slot * i
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (x, y0, x, yb, GRID2))
            s.append(text(x, yb + 18, c, fs))
        s.append("<path d='M%.1f %d V%.1f H%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0 - 6, yb, x0 + pw + 4, INK))
        for si, vals in enumerate(self.series):
            col = LINE1 if si == 0 else LINE2
            dash = "" if si == 0 else " stroke-dasharray='7 4'"
            pts = [(x0 + slot * i, Y(v)) for i, v in enumerate(vals)]
            s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='2.5'%s/>"
                     % (" ".join("%.1f,%.1f" % p for p in pts), col, dash))
            for p in pts:
                if si == 0:
                    s.append("<circle cx='%.1f' cy='%.1f' r='3.8' fill='%s'/>" % (p[0], p[1], GREEN))
                else:
                    s.append("<rect x='%.1f' y='%.1f' width='7' height='7' fill='%s'/>" % (p[0] - 3.5, p[1] - 3.5, LINE2))
        if self.names:
            ws = [tw(nm, fs) for nm in self.names]
            tot = sum(ws) + 2 * 34 + 24
            x = (W - tot) / 2
            for si, nm in enumerate(self.names):
                col = LINE1 if si == 0 else LINE2
                dash = "" if si == 0 else " stroke-dasharray='7 4'"
                s.append("<line x1='%.1f' y1='38' x2='%.1f' y2='38' stroke='%s' stroke-width='2.5'%s/>" % (x, x + 26, col, dash))
                if si == 0:
                    s.append("<circle cx='%.1f' cy='38' r='3.8' fill='%s'/>" % (x + 13, GREEN))
                else:
                    s.append("<rect x='%.1f' y='34.5' width='7' height='7' fill='%s'/>" % (x + 9.5, LINE2))
                s.append(text(x + 32, 43, nm, fs, anchor="start"))
                x += 34 + ws[si] + 24
        s.append(text(x0 + pw / 2, yb + 38, self.xt, fs, bold=True))
        mid = y0 + ph / 2
        s.append(text(13, mid, self.yt, fs, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % mid))
        assert tw(self.yt, fs, True) < ph + 30, (self.yt, ph)
        H = yb + 44
        return svg_wrap(W, H, "".join(s), "line graph: " + self.title.lower())


def col_svg(title, cat_axis, val_axis, cats, vals, top_v, lstep):
    """Bar graph, a grid line at every 1, labels every `lstep`."""
    fs = 14
    gy = 14
    ph = top_v * gy
    x0 = 22 + tw(top_v, fs) + 6
    slot = max(46, max(tw(c, fs) for c in cats) + 14)
    pw = slot * len(cats)
    y0 = 32
    yb = y0 + ph
    W = max(x0 + pw + 8, tw(title, 16, True) + 16)
    s = [text(W / 2, 18, title, 16, bold=True)]
    for k in range(top_v + 1):
        y = yb - k * gy
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>"
                 % (x0, y, x0 + pw, y, GRID2 if k % lstep == 0 else GRID))
        if k % lstep == 0:
            s.append(text(x0 - 5, y + 5, k, fs, anchor="end"))
    for i, (c, v) in enumerate(zip(cats, vals)):
        cx = x0 + slot * i + slot / 2
        bw = 34
        h = v * gy
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s'/>" % (cx - bw / 2, yb - h, bw, h, BAR))
        s.append(text(cx, yb + 17, c, fs))
    s.append("<path d='M%.1f %d V%.1f H%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0 - 6, yb, x0 + pw, INK))
    s.append(text(x0 + pw / 2, yb + 36, cat_axis, fs, bold=True))
    mid = y0 + ph / 2
    s.append(text(13, mid, val_axis, fs, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % mid))
    assert tw(val_axis, fs, True) < ph + 26, (val_axis, ph)
    return svg_wrap(W, yb + 42, "".join(s), "bar graph: " + title.lower())


MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MONTHN = dict(zip(MONTHS, ["January", "February", "March", "April", "May", "June", "July", "August",
                           "September", "October", "November", "December"]))
HOURS = ["6 a.m.", "8 a.m.", "10 a.m.", "12 p.m.", "2 p.m.", "4 p.m.", "6 p.m."]

RAIN = LG("Average rainfall in Vancouver", MONTHS, "Month", "Rainfall (mm)",
          [[170, 100, 110, 90, 70, 50, 40, 40, 50, 120, 190, 160]], 0, 200, 50, 10, u=" mm", gy=8, slot=36)
VAN = [7, 8, 10, 13, 17, 20, 22, 22, 19, 13, 9, 6]
KEL = [1, 3, 9, 15, 20, 24, 29, 28, 22, 13, 5, 0]
VTEMP = LG("Average high temperature in Vancouver", MONTHS, "Month", "Temperature (°C)",
           [VAN], 0, 25, 5, 1, u=" °C", gy=7, slot=36)
TWO = LG("Average high temperature", MONTHS, "Month", "Temperature (°C)",
         [VAN, KEL], 0, 30, 10, 2, names=["Vancouver", "Kelowna"], u=" °C", gy=11, slot=36)
DAY = LG("Temperature at Whistler on a summer day", HOURS, "Time", "Temperature (°C)",
         [[10, 13, 17, 21, 24, 23, 19]], 5, 25, 5, 1, u=" °C", gy=8)
SALMON = LG("Salmon counted in a BC river each week", [str(w) for w in range(1, 8)], "Week", "Salmon",
            [[150, 400, 850, 1200, 950, 500, 200]], 0, 1400, 200, 100, u=" salmon", gy=11)
BIKE = LG("Mei’s bike ride on the Stanley Park Seawall", [str(m) for m in range(0, 61, 10)], "Time (minutes)",
          "Distance (km)", [[0, 2, 4, 5, 5, 7, 9]], 0, 10, 2, 1, u=" km", gy=14)
PLANT = LG("Height of Arjun’s bean plant", [str(d) for d in range(0, 25, 4)], "Day", "Height (cm)",
           [[2, 6, 12, 20, 26, 30, 32]], 0, 40, 10, 2, u=" cm", gy=9)
SPORTS = (["Soccer", "Hockey", "Lacrosse", "Basketball", "Swimming"], [8, 6, 3, 5, 4])
SPORTLINE = LG("Favourite sport in 6B", SPORTS[0], "Sport", "Students", [SPORTS[1]], 0, 10, 2, 1, u="", gy=13)


def sport_bar():
    return col_svg("Favourite sport in 6B", "Sport", "Students", SPORTS[0], SPORTS[1], 10, 2)


def steps(T, si=0):
    v = T.series[si]
    return [v[k + 1] - v[k] for k in range(len(v) - 1)]


def mid(T, i):
    """Value halfway between point i and point i+1 (the line is straight between them)."""
    v = T.series[0]
    return F(v[i] + v[i + 1], 2)


def mo(i):
    return MONTHN[MONTHS[i]]


# ------------------------------------------------------------ set 1: read line graphs
def set_read():
    its = []
    T, V = RAIN, RAIN.series[0]
    f = fig(T.svg())
    its.append(mcqv(f + "What is each small square on the rainfall scale worth?", 10, [1, 5, 50], T.v,
                    "The labels go 0, 50, 100, 150, 200. There are 5 small squares between two labels. 50 ÷ 5 = 10, "
                    "so each small square is 10 mm."))
    v = T.at("Oct")
    assert v == 120
    its.append(mcqv(f + "How much rain falls in Vancouver in an average October?", v, [12, T.at("Nov"), 125], T.v,
                    "Go up from Oct to the dot, then across. It is 2 small squares above 100: 100 + 2 × 10 = 120 mm. "
                    "(12 mm counts each square as 1 mm.)"))
    assert V.index(max(V)) == 10 and V.count(max(V)) == 1
    its.append(mcq(f + "In which month does Vancouver get the most rain?", "November", ["January", "December", "October"],
                   "The highest dot is above Nov: 190 mm. January (170 mm) and December (160 mm) are lower."))
    v = T.at("Feb")
    its.append(mcqv(f + "How much rain falls in an average February?", v, [10, T.at("Mar"), T.at("Jan")], T.v,
                    "Go up from Feb to the dot. It is on the labelled line for 100, so 100 mm. "
                    "(110 mm is March and 170 mm is January.)"))
    assert V.count(90) == 1
    its.append(mcq(f + "Which month has an average of 90 mm of rain?", "April", ["March", "May", "September"],
                   "90 mm is 1 small square below 100. The only dot there is above Apr. "
                   "(March has 110 mm and May has 70 mm.)"))
    v = T.at("Nov")
    its.append(mcqv(f + "How much rain falls in an average November?", v, [19, 200, 180], T.v,
                    "The Nov dot is 1 small square below 200: 200 − 10 = 190 mm. "
                    "(200 mm is the top of the scale, not a reading.)"))
    T, V = VTEMP, VTEMP.series[0]
    f = fig(T.svg())
    its.append(mcqv(f + "What is each small square on the temperature scale worth?", 1, [5, 10, 2], T.v,
                    "The labels go up by 5. There are 5 small squares between two labels. 5 ÷ 5 = 1, so each square is 1 °C."))
    v = T.at("Jul")
    its.append(mcqv(f + "What is the average high temperature in Vancouver in July?", v, [20, 25, 23], T.v,
                    "Go up from Jul to the dot. It is 2 small squares above 20: 20 + 2 = 22 °C. "
                    "(20 °C and 25 °C are only the labels near it.)"))
    assert V.index(min(V)) == 11 and V.count(min(V)) == 1
    its.append(mcq(f + "Which month has the lowest average high temperature?", "December", ["January", "February", "November"],
                   "The lowest dot is above Dec: 6 °C. January is 7 °C and November is 9 °C."))
    v = T.at("Apr")
    its.append(mcqv(f + "What is the average high temperature in April?", v, [T.at("Mar"), 15, 3], T.v,
                    "The Apr dot is 3 small squares above 10: 10 + 3 = 13 °C. (3 °C forgets to start from 10.)"))
    assert V.count(9) == 1
    its.append(mcq(f + "In which month is the average high temperature 9 °C?", "November", ["February", "December", "March"],
                   "Find 9 on the scale: 1 small square below 10. The dot on that line is above Nov. "
                   "(February is 8 °C and March is 10 °C.)"))
    T, V = DAY, DAY.series[0]
    f = fig(T.svg())
    v = T.at("6 a.m.")
    its.append(mcqv(f + "What was the temperature at 6 a.m.?", v, [5, T.at("8 a.m."), 11], T.v,
                    "The scale starts at 5, not 0. At 6 a.m. the dot is on the labelled line for 10, so 10 °C. "
                    "(5 °C is the bottom of the scale.)"))
    v = T.at("10 a.m.")
    its.append(mcqv(f + "What was the temperature at 10 a.m.?", v, [v - 5, 15, T.at("12 p.m.")], T.v,
                    "At 10 a.m. the dot is 2 small squares above 15: 15 + 2 = 17 °C. "
                    "(12 °C counts 12 squares as if the scale started at 0, but it starts at 5.)"))
    assert V.index(max(V)) == 4 and V.count(max(V)) == 1
    its.append(mcq(f + "At which reading was it warmest?", "2 p.m.", ["12 p.m.", "4 p.m.", "6 p.m."],
                   "The highest dot is above 2 p.m. (24 °C). At 4 p.m. it was 23 °C, a little cooler."))
    v = T.at("4 p.m.")
    its.append(mcqv(f + "What was the temperature at 4 p.m.?", v, [v - 5, T.at("2 p.m."), 25], T.v,
                    "At 4 p.m. the dot is 2 small squares below 25: 25 − 2 = 23 °C. "
                    "(18 °C counts squares from 0, but the scale starts at 5.)"))
    T, V = SALMON, SALMON.series[0]
    f = fig(T.svg())
    its.append(mcqv(f + "What is each small square on the salmon scale worth?", 100, [200, 1, 50], T.v,
                    "The labels go up by 200. There are 2 small squares between two labels. 200 ÷ 2 = 100 salmon."))
    v = T.at("3")
    its.append(mcqv(f + "How many salmon were counted in week 3?", v, [800, 900, T.at("4")], T.v,
                    "In week 3 the dot is halfway between the lines for 800 and 900. Halfway is 850 salmon."))
    assert V.index(max(V)) == 3
    its.append(mcq(f + "In which week were the most salmon counted?", "Week 4", ["Week 5", "Week 3", "Week 7"],
                   "The highest dot is above week 4: 1200 salmon."))
    v = T.at("1")
    its.append(mcqv(f + "How many salmon were counted in week 1?", v, [100, 200, 15], T.v,
                    "In week 1 the dot is halfway between 100 and 200, so 150 salmon."))
    assert V.count(500) == 1
    its.append(mcq(f + "In which week were 500 salmon counted?", "Week 6", ["Week 2", "Week 5", "Week 3"],
                   "500 is halfway between 400 and 600. The dot there is above week 6. (Week 2 had 400 salmon.)"))
    return {"title": "Read line graphs and their scales", "items": its}


# ------------------------------------------------------------ set 2: trends
TR = ["It increases", "It decreases", "It stays the same", "It increases, then decreases", "It decreases, then increases"]


def set_trends():
    its = []
    T, V = RAIN, RAIN.series[0]
    f = fig(T.svg())
    assert all(x < 0 for x in steps(T)[2:6])
    its.append(mcq(f + "Describe the trend in rainfall from March to July.", TR[1], [TR[0], TR[2], TR[3]],
                   "March 110 mm, April 90, May 70, June 50, July 40. The line goes down each month, so rainfall decreases."))
    assert all(x > 0 for x in steps(T)[7:10])
    its.append(mcq(f + "Describe the trend in rainfall from August to November.", TR[0], [TR[1], TR[4], TR[2]],
                   "August 40 mm, September 50, October 120, November 190. The line goes up each month, so rainfall increases."))
    d = T.at("Nov") - T.at("Sep")
    its.append(mcqv(f + "By how much does the rainfall increase from September to November?", d,
                    [T.at("Nov"), 70, 14], T.v,
                    "September 50 mm, November 190 mm. 190 − 50 = 140 mm. (70 mm is only September to October.)"))
    st = steps(T)
    k = st.index(min(st))
    assert k == 0 and st.count(min(st)) == 1
    labs = ["%s to %s" % (mo(i), mo(i + 1)) for i in range(11)]
    its.append(mcq(f + "Between which two months does the rainfall decrease the most?", labs[0], [labs[10], labs[2], labs[5]],
                   "Find the steepest part going down. January to February: 170 − 100 = 70 mm. "
                   "November to December is only 190 − 160 = 30 mm."))
    assert [i for i, x in enumerate(st) if x == 0] == [6]
    its.append(mcq(f + "Between which two months does the rainfall stay the same?", labs[6], [labs[5], labs[7], labs[0]],
                   "A flat line shows no change. July and August both have 40 mm."))
    assert st[1] == 10
    its.append(mcq(f + "How does the rainfall change from February to March?", "It increases by 10 mm",
                   ["It decreases by 10 mm", "It increases by 1 mm", "It stays the same"],
                   "February 100 mm, March 110 mm. The line goes up 1 small square, and each square is 10 mm."))
    T, V = VTEMP, VTEMP.series[0]
    f = fig(T.svg())
    st = steps(T)
    assert all(x < 0 for x in st[7:]) and all(x >= 0 for x in st[:7])
    its.append(mcq(f + "In which part of the year does the line go down?", "August to December",
                   ["January to July", "March to June", "May to August"],
                   "From August (22 °C) the dots get lower each month until December (6 °C). Before July the line goes up."))
    d = T.at("Jul") - T.at("Jan")
    its.append(mcqv(f + "By how much does the average high rise from January to July?", d,
                    [T.at("Jul"), T.at("Jul") + T.at("Jan"), 6], T.v,
                    "January 7 °C, July 22 °C. Rise = 22 − 7 = 15 °C. (6 is the number of months, not degrees.)"))
    labs = ["%s to %s" % (mo(i), mo(i + 1)) for i in range(11)]
    k = st.index(min(st))
    assert k == 8 and st.count(min(st)) == 1
    its.append(mcq(f + "Between which two months does the average high fall the most?", labs[8], [labs[9], labs[10], labs[6]],
                   "September to October: 19 − 13 = 6 °C. October to November: 13 − 9 = 4 °C. "
                   "November to December: 9 − 6 = 3 °C. The biggest fall is 6 °C."))
    k = st.index(max(st))
    assert k == 3 and st.count(max(st)) == 1
    its.append(mcq(f + "Between which two months does the average high rise the most?", labs[3], [labs[5], labs[2], labs[6]],
                   "Find the steepest part going up. April to May: 17 − 13 = 4 °C. March to April: 3 °C. "
                   "June to July: only 2 °C, even though July is near the top."))
    its.append(mcq(f + "What does the flat part from July to August show?", "The temperature stays the same",
                   ["The temperature is 0 °C", "The temperature falls", "No data was collected"],
                   "A flat line means no change. July and August both have an average high of 22 °C."))
    T = TWO
    A, B = T.series
    f = fig(T.svg())
    i = 6
    its.append(mcqv(f + "Use the key. What is the average high in Kelowna in July?", B[i], [A[i], 30, B[7]], T.v,
                    "Kelowna is the dashed line with squares. Each small square is 2 °C. In July its square is halfway "
                    "between 28 and 30, so 29 °C. (22 °C is the Vancouver line.)"))
    da, db = A[6] - A[0], B[6] - B[0]
    assert (da, db) == (15, 28)
    its.append(mcq(f + "Which city has the bigger increase from January to July?", "Kelowna",
                   ["Vancouver", "They increase by the same amount", "Neither: both lines decrease"],
                   "Vancouver: 22 − 7 = 15 °C. Kelowna: 29 − 1 = 28 °C. Kelowna’s line is steeper."))
    same = [k for k in range(12) if A[k] == B[k]]
    assert same == [9]
    its.append(mcq(f + "In which month do the two cities have the same average high?", "October",
                   ["March", "April", "July"],
                   "The two lines meet in October: both are 13 °C. In March, Vancouver is 10 °C and Kelowna is 9 °C."))
    d = B[6] - A[6]
    its.append(mcqv(f + "How much warmer is Kelowna than Vancouver in July?", d, [B[6], B[6] + A[6], 6], T.v,
                    "Kelowna 29 °C, Vancouver 22 °C. How much warmer means subtract: 29 − 22 = 7 °C."))
    assert A[0] - B[0] == 6
    its.append(mcq(f + "In January, which city is warmer, and by how much?", "Vancouver, by 6 °C",
                   ["Kelowna, by 6 °C", "Vancouver, by 3 °C", "Vancouver, by 8 °C"],
                   "Vancouver 7 °C, Kelowna 1 °C. 7 − 1 = 6 °C. (3 °C counts the 3 squares, but each square is 2 °C. "
                   "8 °C adds the two numbers.)"))
    T, V = SALMON, SALMON.series[0]
    f = fig(T.svg())
    its.append(mcq(f + "Describe the trend in the salmon count over the 7 weeks.", TR[3], [TR[4], TR[0], TR[2]],
                   "The count goes up from week 1 to week 4 (1200 salmon), then goes down to week 7."))
    st = steps(T)
    k = st.index(max(st))
    assert k == 1 and st.count(max(st)) == 1
    labs = ["Week %s to week %s" % (T.xl[i], T.xl[i + 1]) for i in range(6)]
    its.append(mcq(f + "Between which two weeks did the count go up the most?", labs[1], [labs[2], labs[0], labs[3]],
                   "Week 2 to 3: 850 − 400 = 450. Week 3 to 4: 1200 − 850 = 350. Week 1 to 2: 250. "
                   "The steepest rise is week 2 to week 3, not the part that reaches the top."))
    d = T.at("4") - T.at("7")
    its.append(mcqv(f + "By how much did the count go down from week 4 to week 7?", d,
                    [T.at("4") + T.at("7"), 300, 10], T.v,
                    "Week 4: 1200. Week 7: 200. 1200 − 200 = 1000 salmon. (300 is only week 6 to week 7.)"))
    T, V = BIKE, BIKE.series[0]
    f = fig(T.svg())
    assert steps(T)[3] == 0
    its.append(mcq(f + "What does the flat part from 30 to 40 minutes show?", "Mei stopped for a rest",
                   ["Mei biked back to the start", "Mei biked faster", "Mei biked 5 km in 10 minutes"],
                   "A flat line means the distance did not change. Mei stayed at 5 km for 10 minutes, so she stopped."))
    return {"title": "Trends: increase, decrease and no change", "items": its}


# ------------------------------------------------------------ set 3: read between points
def set_between():
    its = []
    T, V = DAY, DAY.series[0]
    f = fig(T.svg())
    m = mid(T, 1)
    assert m == 15
    its.append(mcqv(f + "The temperature changed steadily between readings. What was it at about 9 a.m.?", m,
                    [V[1], V[2], V[1] + V[2]], T.v,
                    "9 a.m. is halfway between 8 a.m. (13 °C) and 10 a.m. (17 °C). Halfway between 13 and 17 is 15 °C."))
    m = mid(T, 2)
    assert m == 19
    its.append(mcqv(f + "About what was the temperature at 11 a.m.?", m, [V[2], V[3], m - 5], T.v,
                    "11 a.m. is halfway between 10 a.m. (17 °C) and 12 p.m. (21 °C). Halfway is 19 °C. "
                    "(Do not just use the nearest dot.)"))
    m = mid(T, 5)
    assert m == 21
    its.append(mcqv(f + "About what was the temperature at 5 p.m.?", m, [V[5], V[6], m - 5], T.v,
                    "5 p.m. is halfway between 4 p.m. (23 °C) and 6 p.m. (19 °C). Halfway between 23 and 19 is 21 °C."))
    its.append(mcq(f + "At about what time did the temperature reach 15 °C?", "9 a.m.", ["8 a.m.", "10 a.m.", "11 a.m."],
                   "15 °C is halfway between 13 °C (8 a.m.) and 17 °C (10 a.m.). So it was about halfway in time: 9 a.m."))
    its.append(mcq(f + "After 2 p.m., at about what time was it 21 °C?", "5 p.m.", ["12 p.m.", "4 p.m.", "6 p.m."],
                   "After 2 p.m. the line goes down from 23 °C (4 p.m.) to 19 °C (6 p.m.). 21 °C is halfway, at about 5 p.m. "
                   "(It was also 21 °C at 12 p.m., but that is before 2 p.m.)"))
    its.append(mcq(f + "Why does it make sense to read this graph between the dots?",
                   "The temperature keeps changing between readings",
                   ["Any graph with a line can be read between dots", "The temperature was measured every minute",
                    "The scale starts at 5"],
                   "Time and temperature change smoothly, so there is a real temperature between two readings. "
                   "The line gives a good estimate of it."))
    T, V = BIKE, BIKE.series[0]
    f = fig(T.svg())
    km = lambda x: unit(x, "km", "km")
    m = mid(T, 1)
    assert m == 3
    its.append(mcqv(f + "How far had Mei biked after 15 minutes?", m, [V[1], V[2], V[1] + V[2]], km,
                    "15 minutes is halfway between 10 minutes (2 km) and 20 minutes (4 km). Halfway is 3 km."))
    m = mid(T, 0)
    assert m == 1
    its.append(mcqv(f + "How far had Mei biked after 5 minutes?", m, [V[1], 5, 0], km,
                    "5 minutes is halfway between 0 minutes (0 km) and 10 minutes (2 km). Halfway is 1 km. "
                    "(5 is the number of minutes, not kilometres.)", allow_zero=True))
    m = mid(T, 2)
    assert m == F(9, 2)
    its.append(mcqv(f + "How far had Mei biked after 25 minutes?", m, [V[2], V[3], V[2] + V[3]], km,
                    "25 minutes is halfway between 20 minutes (4 km) and 30 minutes (5 km). Halfway between 4 and 5 is 4.5 km."))
    m = mid(T, 3)
    assert m == 5
    its.append(mcqv(f + "How far had Mei biked after 35 minutes?", m, [V[5], F(9, 2), 10], km,
                    "From 30 to 40 minutes the line is flat at 5 km. Mei was resting, so at 35 minutes she had still biked 5 km."))
    m = mid(T, 4)
    assert m == 6
    its.append(mcqv(f + "How far had Mei biked after 45 minutes?", m, [V[4], V[5], V[4] + V[5]], km,
                    "45 minutes is halfway between 40 minutes (5 km) and 50 minutes (7 km). Halfway is 6 km."))
    assert mid(T, 5) == 8
    mins = lambda x: unit(x, "minute", "minutes")
    its.append(mcqv(f + "At about what time had Mei biked 8 km?", 55, [50, 60, 45], mins,
                    "8 km is halfway between 7 km (50 minutes) and 9 km (60 minutes). So it was at about 55 minutes."))
    its.append(mcqv(f + "Mei kept biking at the same speed for 10 more minutes after 60 minutes. About how far would she be then?",
                    11, [9, 10, 18], km,
                    "From 40 to 60 minutes she biked 2 km every 10 minutes. 9 km + 2 km = 11 km. "
                    "Extending the line is only an estimate."))
    its.append(mcqv(f + "At about what time had Mei biked half of the 9 km?", 25, [30, 20, 45], mins,
                    "Half of 9 km is 4.5 km. 4.5 km is halfway between 4 km (20 minutes) and 5 km (30 minutes), "
                    "so about 25 minutes. (30 minutes is half the time, not half the distance.)"))
    T, V = PLANT, PLANT.series[0]
    f = fig(T.svg())
    m = mid(T, 2)
    assert m == 16
    its.append(mcqv(f + "About how tall was the plant on day 10?", m, [V[2], V[3], 10], T.v,
                    "Day 10 is halfway between day 8 (12 cm) and day 12 (20 cm). Halfway between 12 and 20 is 16 cm. "
                    "(10 is the day, not the height.)"))
    m = mid(T, 3)
    assert m == 23
    its.append(mcqv(f + "About how tall was the plant on day 14?", m, [V[3], V[4], V[3] + V[4]], T.v,
                    "Day 14 is halfway between day 12 (20 cm) and day 16 (26 cm). Halfway is 23 cm."))
    m = mid(T, 1)
    assert m == 9
    its.append(mcqv(f + "About how tall was the plant on day 6?", m, [V[1], V[2], V[1] + V[2]], T.v,
                    "Day 6 is halfway between day 4 (6 cm) and day 8 (12 cm). Halfway between 6 and 12 is 9 cm."))
    assert mid(T, 4) == 28
    its.append(mcq(f + "On about which day was the plant 28 cm tall?", "Day 18", ["Day 16", "Day 20", "Day 22"],
                   "28 cm is halfway between 26 cm (day 16) and 30 cm (day 20). So it was about day 18."))
    its.append(mcqv(f + "About how much did the plant grow from day 10 to day 14?", 7, [23, 8, 4], T.v,
                    "Day 10: about 16 cm. Day 14: about 23 cm. 23 − 16 = 7 cm. (4 is the number of days.)"))
    T, V = DAY, DAY.series[0]
    f = fig(T.svg())
    m = mid(T, 3)
    assert m == F(45, 2)
    its.append(mcqv(f + "What is the best estimate of the temperature at 1 p.m.?", m, [V[3], V[4], m - 5], T.v,
                    "1 p.m. is halfway between 12 p.m. (21 °C) and 2 p.m. (24 °C). Halfway between 21 and 24 is 22.5 °C."))
    return {"title": "Read between points", "items": its}


# ------------------------------------------------------------ set 4: line graph or bar graph
LT = "Line graph: it shows change over time"
BT = "Bar graph: it compares categories"
LW = "Line graph: it compares categories"
BW = "Bar graph: it shows change over time"


def pick(q, line):
    if line:
        return mcq(q, LT, [BT, LW, BW],
                   "The data is measured again and again over time, so a line graph shows how it changes.")
    return mcq(q, BT, [LT, LW, BW],
               "The data is in separate categories with nothing in between, so use a bar graph. "
               "Joining categories with a line makes no sense.")


def set_choose():
    its = []
    its.append(pick("Which graph is best to show the height of a sunflower every week for 8 weeks?", True))
    its.append(pick("Which graph is best to show the favourite sport of the students in your class?", False))
    its.append(pick("Which graph is best to show the temperature in Kamloops every hour for one day?", True))
    its.append(pick("Which graph is best to show the number of students in each Grade 6 class at your school?", False))
    its.append(pick("Which graph is best to show the number of salmon counted each day during a salmon run?", True))
    its.append(pick("Which graph is best to show how many cars of each colour are in the school parking lot?", False))
    its.append(pick("Which graph is best to show Ava’s mass on each birthday from age 6 to age 11?", True))
    its.append(pick("Which graph is best to show how many students walk, bike, take the bus or come by car to school?", False))
    its.append(pick("Which graph is best to show the average rainfall in Prince George each month of the year?", True))
    its.append(pick("Which graph is best to show the number of visitors to five BC parks last summer?", False))
    its.append(pick("Liam wants to show how many people joined his school’s Terry Fox Run each year from 2019 to 2026. "
                    "Which graph shows the change best?", True))
    its.append(pick("Olivia measured the temperature of a cup of hot chocolate every 2 minutes as it cooled. Which graph is best?", True))
    T = SPORTLINE
    f = fig(T.svg())
    its.append(mcq(f + "Kai showed his class’s favourite sports with this line graph. What is wrong with it?",
                   "Sports are categories, so the dots should not be joined",
                   ["The scale should start at 1", "The line should only go up", "A graph cannot show 5 sports"],
                   "A line shows change from one point to the next, like over time. Sports have no order and nothing in "
                   "between them, so Kai should use a bar graph."))
    assert mid(T, 1) == F(9, 2)
    its.append(mcq(f + "On Kai’s graph, the line between Hockey and Lacrosse passes 4.5. What does that point show?",
                   "Nothing: there is no sport between hockey and lacrosse",
                   ["4.5 students chose a sport between them", "Students who like both sports",
                    "The number of students who chose lacrosse"],
                   "Between two categories there is no data, so a point on the line there means nothing. "
                   "This is why categories are not joined with a line."))
    f = fig(sport_bar())
    its.append(mcqv(f + "How many students in 6B chose soccer?", 8, [6, 4, 9], lambda x: unit(x, "student", "students"),
                    "The soccer bar ends on the labelled line for 8, so 8 students. "
                    "(4 counts the labelled lines, but each small square is 1 student.)"))
    its.append(mcq(f + "Why is a bar graph a better choice than a line graph for this data?",
                   "Each sport is a separate category",
                   ["The data changes over time", "Bar graphs are always better", "Soccer has the most students"],
                   "The sports are separate categories with nothing in between. Bars compare them; a line would suggest "
                   "a change from one sport to the next."))
    its.append(mcq("Which data could be shown well on a line graph?", "The temperature at noon each day for a week",
                   ["The favourite fruit of each student", "The number of pets of each kind in a class",
                    "The colours of the bikes at school"],
                   "Temperature each day is measured over time, so a line graph shows how it changes. "
                   "The others are categories."))
    its.append(mcq("Which data should NOT be shown on a line graph?", "Favourite ice cream flavours in Grade 6",
                   ["The height of a cedar tree each year", "The price of a bus pass each year",
                    "The rainfall in Nanaimo each week"],
                   "Ice cream flavours are categories with no order, so they belong on a bar graph. "
                   "The others change over time."))
    f = fig(TWO.svg())
    its.append(mcq(f + "Why does this graph use two lines and a key?", "To compare two cities over the same months",
                   ["Because the months are categories", "To show the total for both cities",
                    "Because Kelowna is colder"],
                   "Each line shows one city over the same 12 months. The key tells you which line is which, "
                   "so you can compare them month by month."))
    its.append(mcq("A line graph is the best choice when the data…", "changes over time",
                   ["is in separate groups", "has no numbers", "is about favourite things"],
                   "Line graphs show change over time, like temperature or height. "
                   "For separate groups or favourites, use a bar graph."))
    return {"title": "Line graph or bar graph?", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_words():
    its = []
    T, V = RAIN, RAIN.series[0]
    f = fig(T.svg())
    tot = sum(V)
    assert tot == 1190
    its.append(mcqv(f + "What is the total of the 12 monthly amounts on the graph?", tot, [tot // 10, tot - V[-1], tot - V[0]], T.v,
                    "170 + 100 + 110 + 90 + 70 + 50 + 40 + 40 + 50 + 120 + 190 + 160 = 1190 mm. "
                    "That is more than a metre of rain in a year. (1030 mm or 1020 mm leaves out a month.)"))
    d = T.at("Mar") - T.at("Jul")
    its.append(mcqv(f + "Spring Break is in March. How much more rain falls in an average March than in an average July?", d,
                    [T.at("Mar") + T.at("Jul"), 7, 80], T.v,
                    "March 110 mm, July 40 mm. How much more means subtract: 110 − 40 = 70 mm."))
    n = sum(1 for x in V if x > 100)
    assert n == 5
    its.append(mcqv(f + "In how many months does Vancouver get more than 100 mm of rain?", n, [6, 4, 7],
                    lambda x: unit(x, "month", "months"),
                    "Above 100 mm: January, March, October, November and December. That is 5 months. "
                    "February has exactly 100 mm, which is not more than 100."))
    its.append(mcq(f + "What is the ratio of July rainfall to November rainfall, in lowest terms?", "4:19",
                   ["19:4", "40:150", "4:15"],
                   "July 40 mm, November 190 mm. 40:190. Divide both by 10: 4:19. July comes first, so it is 4:19, not 19:4."))
    s = T.at("Jun") + T.at("Jul") + T.at("Aug")
    its.append(mcqv(f + "What is the total rainfall for June, July and August?", s, [13, 90, 120], T.v,
                    "50 + 40 + 40 = 130 mm. (90 mm forgets June.)"))
    n = sum(1 for x in V if x >= 80)
    assert n == 7
    its.append(mcqv(f + "A garden needs at least 80 mm of water a month. In how many months does rain alone give enough?",
                    n, [5, 6, 8], lambda x: unit(x, "month", "months"),
                    "80 mm or more: January, February, March, April, October, November and December. That is 7 months."))
    w = sum(V[i] for i in (0, 1, 2, 9, 10, 11))
    assert w == 850
    its.append(mcqv(f + "How much of the year’s rain falls from October to March?", w, [tot - w, w - V[0], tot], T.v,
                    "October 120 + November 190 + December 160 + January 170 + February 100 + March 110 = 850 mm. "
                    "Most of Vancouver’s rain falls in fall and winter. (680 mm leaves out January.)"))
    T = TWO
    A, B = T.series
    f = fig(T.svg())
    d = B[7] - A[7]
    assert d == 6
    its.append(mcqv(f + "Kai’s family drives from Vancouver to Kelowna in August. How much warmer is the average high in Kelowna?",
                    d, [B[7] + A[7], B[7], 3], T.v,
                    "Kelowna 28 °C, Vancouver 22 °C. 28 − 22 = 6 °C. (3 counts the squares; each square is 2 °C.)"))
    n = sum(1 for x in B if x >= 20)
    assert n == 5
    its.append(mcqv(f + "In how many months is Kelowna’s average high 20 °C or more?", n, [4, 3, 6],
                    lambda x: unit(x, "month", "months"),
                    "May 20 °C, June 24, July 29, August 28, September 22. That is 5 months. "
                    "May counts, because 20 °C or more includes 20."))
    n = sum(1 for a, b in zip(A, B) if a > b)
    assert n == 5
    its.append(mcqv(f + "In how many months is Vancouver’s average high warmer than Kelowna’s?", n, [6, 7, 4],
                    lambda x: unit(x, "month", "months"),
                    "Vancouver’s line is above in January, February, March, November and December: 5 months. "
                    "In October the two are equal, so it does not count."))
    diffs = [abs(a - b) for a, b in zip(A, B)]
    assert diffs.index(max(diffs)) == 6 and diffs.count(max(diffs)) == 1
    its.append(mcq(f + "In which month is the difference between the two cities the greatest?", "July",
                   ["August", "January", "December"],
                   "July: 29 − 22 = 7 °C. August: 6 °C. January: 6 °C. December: 6 °C. The lines are farthest apart in July."))
    T, V = VTEMP, VTEMP.series[0]
    f = fig(T.svg())
    ok = [MONTHS[i] for i, x in enumerate(V) if x >= 17]
    assert ok == ["May", "Jun", "Jul", "Aug", "Sep"]
    its.append(mcq(f + "Ji-woo’s family wants a picnic in Stanley Park in a month with an average high of at least 17 °C. "
                   "Which months work?", "May to September", ["June to August", "April to October", "July and August"],
                   "May 17 °C, June 20, July 22, August 22, September 19. April (13 °C) and October (13 °C) are too cool."))
    d = T.at("Aug") - T.at("Mar")
    its.append(mcqv(f + "How much warmer is the average high in August than in March?", d,
                    [T.at("Aug") + T.at("Mar"), T.at("Aug"), 5], T.v,
                    "August 22 °C, March 10 °C. 22 − 10 = 12 °C. (5 is the number of months, not degrees.)"))
    T, V = DAY, DAY.series[0]
    f = fig(T.svg())
    d = T.at("2 p.m.") - T.at("8 a.m.")
    its.append(mcqv(f + "Leah’s class started a hike at 8 a.m. and finished at 2 p.m. How much did the temperature rise?", d,
                    [6, T.at("2 p.m.") + T.at("8 a.m."), T.at("2 p.m.")], T.v,
                    "8 a.m. 13 °C, 2 p.m. 24 °C. 24 − 13 = 11 °C. (6 is the number of hours.)"))
    assert mid(DAY, 2) == 19
    its.append(mcq(f + "The class wants to be off the trail before it gets warmer than 19 °C. By about what time should they finish?",
                   "11 a.m.", ["12 p.m.", "10 a.m.", "2 p.m."],
                   "10 a.m. is 17 °C and 12 p.m. is 21 °C. 19 °C is halfway, at about 11 a.m. "
                   "By 12 p.m. it is already 21 °C."))
    T, V = SALMON, SALMON.series[0]
    f = fig(T.svg())
    tot = sum(V)
    assert tot == 4250
    its.append(mcqv(f + "How many salmon were counted in all 7 weeks?", tot, [tot - V[0], max(V), tot - V[3]], T.v,
                    "150 + 400 + 850 + 1200 + 950 + 500 + 200 = 4250 salmon."))
    its.append(mcq(f + "Simran says the salmon count doubled from week 1 to week 2. Is she right?",
                   "No: double 150 is 300, and the count was 400",
                   ["Yes: it went from 150 to 300", "Yes: 400 is double 200", "No: the count went down"],
                   "Week 1: 150. Double 150 is 300. Week 2: 400, which is more than double."))
    T, V = BIKE, BIKE.series[0]
    f = fig(T.svg())
    its.append(mcqv(f + "Mei rested for part of her ride. For how many minutes was she moving?", 50, [60, 10, 40],
                    lambda x: unit(x, "minute", "minutes"),
                    "The ride lasted 60 minutes. The flat part (30 to 40 minutes) is a 10-minute rest. 60 − 10 = 50 minutes."))
    st = steps(T)
    moving = [x for x in st if x > 0]
    assert st.index(min(moving)) == 2 and moving.count(min(moving)) == 1
    its.append(mcq(f + "While she was moving, in which 10 minutes did Mei bike the shortest distance?", "20 to 30 minutes",
                   ["30 to 40 minutes", "0 to 10 minutes", "50 to 60 minutes"],
                   "20 to 30 minutes: 5 − 4 = 1 km. The other moving parts are 2 km each. "
                   "From 30 to 40 minutes she was resting, not moving."))
    T, V = RAIN, RAIN.series[0]
    f = fig(T.svg())
    its.append(mcq(f + "Owen says July has 4 mm of rain, because the dot is 4 small squares above 0. What is his mistake?",
                   "Each square is 10 mm, so July has 40 mm",
                   ["He is right", "Each square is 5 mm, so July has 20 mm", "He should count from the top: 160 mm"],
                   "The labels go up by 50 with 5 squares between them, so each square is 10 mm. 4 × 10 = 40 mm."))
    return {"title": "Word problems: Vancouver rainfall and temperatures", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


LESSON_LG = LG("Average high temperature in Victoria", MONTHS, "Month", "Temperature (°C)",
               [[8, 9, 11, 14, 17, 20, 22, 22, 20, 15, 10, 8]], 0, 25, 5, 1, u=" °C", gy=7, slot=36)


def body_html():
    V = LESSON_LG.series[0]
    assert V[9] == 15 and V[7] - V[11] == 14 and all(x < 0 for x in steps(LESSON_LG)[7:])
    return (
        "<h2>Read a line graph</h2>"
        "<p>A line graph shows how something changes over time. Time goes along the bottom. "
        "First check the <b>scale</b>: count the small squares between two labels and work out what one square is worth. "
        "Also check where the scale starts. It does not always start at 0.</p>"
        "<p>To read a value, go up from the time to the dot, then across to the scale.</p>"
        "<figure class='sn-fig'>" + LESSON_LG.svg() +
        "<figcaption>The labels go up by 5 with 5 small squares between them, so each square is 1 °C.</figcaption></figure>" +
        ex("Example 1", "What is the average high temperature in Victoria in October?",
           "Go up from Oct to the dot. It is on the labelled line for 15.", "15 °C") +
        "<h2>Trends</h2>"
        "<p>A line going <b>up</b> shows an increase. A line going <b>down</b> shows a decrease. A <b>flat</b> line shows no change. "
        "The <b>steepest</b> part shows the biggest change. It is not always next to the highest point.</p>" +
        ex("Example 2", "Describe the trend from August to December. How much does the temperature fall?",
           "The line goes down every month: 22, 20, 15, 10, 8. So it decreases. Fall = 22 − 8 = 14 °C.",
           "It decreases by 14 °C") +
        "<h2>Read between points</h2>"
        "<p>When the data changes over time, like temperature or distance, the line between two dots gives a good estimate. "
        "Halfway in time is about halfway in value.</p>" +
        ex("Example 3", "Mei biked 2 km in 10 minutes and 4 km in 20 minutes. About how far had she biked after 15 minutes?",
           "15 minutes is halfway between 10 and 20 minutes. Halfway between 2 km and 4 km is 3 km.", "about 3 km") +
        "<h2>Line graph or bar graph?</h2>"
        "<p>Use a <b>line graph</b> for data that changes over time. Use a <b>bar graph</b> to compare separate "
        "<b>categories</b>, like favourite sports. Never join categories with a line: there is nothing between "
        "“hockey” and “lacrosse”.</p>"
        "<figure class='sn-fig'>" + sport_bar() +
        "<figcaption>Sports are categories, so the bars stand apart and are not joined.</figcaption></figure>" +
        table(["Data", "Best graph"], [
            ["Height of a plant each week", "Line graph"],
            ["Rainfall in Vancouver each month", "Line graph"],
            ["Favourite sport of each student", "Bar graph"],
            ["Students in each Grade 6 class", "Bar graph"],
        ]) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting each small square as 1", "Work out the scale: 5 squares between 0 and 50 means 10 each"],
            ["Reading the scale as if it starts at 0", "Check the first label: the scale may start at 5"],
            ["Reading the wrong month or the wrong line", "Go straight up from the month; use the key"],
            ["Choosing the highest point for the biggest rise", "Find the steepest part and subtract"],
            ["Using the nearest dot instead of reading between points", "Halfway in time is about halfway in value"],
            ["Joining categories with a line", "Use a bar graph for categories"],
        ])
    )


FAQ = [
    {"q": "What do Grade 6 students learn about line graphs in BC?",
     "a": "Line graphs are part of Data and probability in the BC Grade 6 math curriculum. Students read and make line graphs, describe trends, estimate values between points and decide when a line graph is the right choice."},
    {"q": "When should you use a line graph instead of a bar graph?",
     "a": "Use a line graph when the data changes over time, such as temperature each month or the height of a plant each week. Use a bar graph to compare separate categories, such as favourite sports."},
    {"q": "What is a trend on a line graph?",
     "a": "A trend is the general direction of the line. If it goes up, the data increases; if it goes down, it decreases; if it is flat, there is no change."},
    {"q": "Can you read values between the points on a line graph?",
     "a": "Yes, when the data changes over time, like temperature or distance. Halfway between two times, the value is about halfway between the two readings, so it is an estimate."},
]


def balance(sets, rnd):
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


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    rnd = random.Random(56816)
    sets = [set_read(), set_trends(), set_between(), set_choose(), set_words()]
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
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-6", "slug": "line-graphs", "sort": 16,
        "updated": UPDATED, "pdf_url": "",
        "title": "Line Graphs: Scales, Trends and Reading Between Points",
        "seo_title": "Grade 6 Line Graphs Worksheets (BC Curriculum) – Free Math with Answer Key",
        "short_title": "Line graphs",
        "domain": "Data and probability",
        "standard_code": "Grade 6: Data and probability",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/6/core",
        "standard_text": "Line graphs",
        "meta_desc": "Free Grade 6 math worksheets on line graphs for the BC curriculum: read scales, describe trends, estimate values between points, choose a line graph or a bar graph, and solve problems with Vancouver rainfall and temperatures. 100 questions with an answer key.",
        "key_big": "A line graph shows change over time. Check what one small square is worth before you read it.",
        "key_sub": "Up is an increase, down is a decrease and flat is no change. Between two readings, the line gives a good estimate. Use a bar graph, not a line, for categories like favourite sports.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(line graph|bar graph)")


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
