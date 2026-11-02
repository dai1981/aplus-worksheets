# -*- coding: utf-8 -*-
"""
AU Year 5 Maths: Line graphs and data (Australian Curriculum v9.0: AC9M5ST02, AC9M5ST01)
  python3 tools/gen_au_maths_y5_line_graphs.py
Read line graphs that show change over time (temperature in Brisbane, a sunflower, a rainwater tank, people at
the beach, a puppy’s mass), find rises and falls, compare two lines, find the mode and describe the shape of data
in dot plots and column graphs (nominal, ordinal and numerical data), and decide which conclusions the data supports.
Wrong answers come from real student mistakes: counting each small square as 1, reading a scale that does not start
at 0 as if it did, reading at the wrong time or on the wrong line, giving the highest value or the frequency as the
mode, choosing the highest point instead of the steepest part, and conclusions the data does not show.
HTML attributes use single quotes (no backslashes in the JSON). Australian English.
"""
import json, re, math, os, random
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
LINE1 = "#2e8b57"
LINE2 = "#c0392b"
BAR = "#2e8b57"
RED = "#c0392b"
INK = "#2b2b2b"
GRID = "#d5ddd8"
GRID2 = "#9fb0a5"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
NBSP = " "


# ------------------------------------------------------------ helpers
def num(x):
    """Australian Curriculum style: 4536, 10 000 (no-break space), −3."""
    x = F(x)
    assert x.denominator == 1, x
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
    """right + 3 wrongs (already formatted). balance() moves the answer."""
    ch = [right]
    for w in wrongs:
        if plain(w) not in {plain(c) for c in ch}:
            ch.append(w)
        if len(ch) == 4:
            break
    assert len(ch) == 4, (q, right, wrongs)
    return {"q": q, "c": ch, "a": 0, "e": e}


def mcqv(q, right, wrongs, f, e, allow_zero=False):
    """Choices given as values: equal values are dropped (no two choices equal in value)."""
    seen = [F(right)]
    pick = []
    for w in wrongs:
        w = F(w)
        if w in seen or (w <= 0 and not allow_zero):
            continue
        seen.append(w)
        pick.append(w)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, right, wrongs)
    return mcq(q, f(right), [f(w) for w in pick], e)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs, bold=False):
    """Approximate text width in px (Arial)."""
    return len(str(t)) * fs * (0.62 if bold else 0.58)


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK, extra=""):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, extra, t))


# ------------------------------------------------------------ line graphs
class LG:
    """Line graph. Labels every `lstep`, a grid line every `gstep`. One or two lines (the second is dashed)."""
    def __init__(self, title, xl, xt, yt, series, ymin, ymax, lstep, gstep, names=None, u=""):
        self.title, self.xl, self.xt, self.yt = title, xl, xt, yt
        self.series, self.ymin, self.ymax, self.lstep, self.gstep = series, ymin, ymax, lstep, gstep
        self.names, self.u = names, u
        for v in series:
            assert len(v) == len(xl)
            assert all(ymin <= x <= ymax for x in v)
            # every reading sits on a grid line or exactly halfway between two
            assert all((x - ymin) * 2 % gstep == 0 for x in v), (title, v)
        assert (ymax - ymin) % lstep == 0 and lstep % gstep == 0 and ymin % lstep == 0

    def v(self, x):
        return "%s%s" % (num(x), self.u)

    def at(self, x, si=0):
        return self.series[si][self.xl.index(x)]

    def svg(self):
        fs = 14
        nt = (self.ymax - self.ymin) // self.gstep
        gy = max(9, min(20, int(round(150.0 / nt))))
        ph = nt * gy
        ylabs = [num(v) for v in range(self.ymin, self.ymax + 1, self.lstep)]
        slot = max(46, max(tw(c, fs) for c in self.xl) + 12)
        x0 = 24 + max(tw(c, fs) for c in ylabs) + 8
        n = len(self.xl)
        pw = slot * (n - 1)
        y0 = 34 + (22 if self.names else 0)
        yb = y0 + ph
        W = x0 + pw + tw(self.xl[-1], fs) / 2 + 8
        W = max(W, tw(self.title, 16, True) + 16)
        s = [text(W / 2, 18, self.title, 16, bold=True)]
        Y = lambda v: yb - (v - self.ymin) / float(self.gstep) * gy
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


HOURS = ["6 am", "8 am", "10 am", "12 pm", "2 pm", "4 pm", "6 pm"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
DAYN = dict(zip(DAYS, ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]))
WEEKS7 = [str(w) for w in range(7)]

BRIS = LG("Temperature in Brisbane on one day", HOURS, "Time", "Temperature (°C)",
          [[21, 23, 27, 30, 31, 28, 26]], 20, 35, 5, 1, u=" °C")
TANK = LG("Water in a rainwater tank", DAYS, "Day", "Water (L)",
          [[4000, 3500, 3000, 4500, 4250, 3750, 3250]], 0, 5000, 1000, 500, u=" L")
SUN = LG("Height of Mia’s sunflower", WEEKS7, "Week", "Height (cm)",
         [[10, 20, 35, 55, 80, 100, 110]], 0, 120, 20, 10, u=" cm")
BEACH = LG("People at the beach on Saturday", HOURS, "Time", "People",
           [[25, 50, 125, 225, 275, 200, 75]], 0, 300, 50, 25, u=" people")
PUP = LG("Mass of Lachlan’s puppy", [str(m) for m in range(2, 9)], "Age (months)", "Mass (kg)",
         [[3, 5, 8, 10, 11, 12, 12]], 0, 14, 2, 1, u=" kg")
DM = LG("Temperature on one day in July", HOURS, "Time", "Temperature (°C)",
        [[20, 22, 28, 30, 32, 30, 26], [6, 8, 10, 12, 14, 12, 10]], 0, 40, 10, 2,
        names=["Darwin", "Melbourne"], u=" °C")
SUNS = LG("Height of two sunflowers", WEEKS7, "Week", "Height (cm)",
          [SUN.series[0], [15, 30, 40, 55, 70, 85, 115]], 0, 120, 20, 10, names=["Mia", "Kai"], u=" cm")
BOOKS = LG("Library books borrowed in Term 3", [str(w) for w in range(1, 7)], "Week", "Books",
           [[24, 30, 28, 36, 42, 38], [30, 26, 34, 36, 30, 44]], 20, 50, 10, 2, names=["5A", "5B"], u=" books")


def steps(T, si=0):
    v = T.series[si]
    return [v[k + 1] - v[k] for k in range(len(v) - 1)]


def between(T, k, word=""):
    return "%s%s to %s%s" % (word, T.xl[k], word.lower(), T.xl[k + 1])


# ------------------------------------------------------------ dot plots and column graphs
def dot_svg(title, axis, lo, hi, counts):
    """Dot plot: one dot for each piece of data, stacked above a number line."""
    fs = 14
    gap, r, dy = 34, 6.5, 15
    mx = max(counts.values())
    x0 = 26
    pw = gap * (hi - lo)
    W = max(x0 * 2 + pw, tw(title, 16, True) + 16)
    x0 = (W - pw) / 2
    top = 34
    yb = top + mx * dy + 6
    s = [text(W / 2, 18, title, 16, bold=True)]
    for v in range(lo, hi + 1):
        x = x0 + (v - lo) * gap
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.5'/>" % (x, yb, x, yb + 6, INK))
        s.append(text(x, yb + 22, v, fs))
        for k in range(counts.get(v, 0)):
            s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (x, yb - 9 - k * dy, r, GREEN))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (x0 - 12, yb, x0 + pw + 12, yb, INK))
    s.append(text(W / 2, yb + 44, axis, fs, bold=True))
    assert all(lo <= k <= hi for k in counts)
    return svg_wrap(W, yb + 52, "".join(s), "dot plot: " + title.lower())


def col_svg(title, cat_axis, val_axis, cats, vals, scale):
    """Column graph with a grid line at every step of the scale (labels every 2 steps)."""
    fs = 14
    top_v = int(math.ceil(max(vals) / float(2 * scale)) * 2 * scale)
    nt = top_v // scale
    gy = 15
    ph = nt * gy
    x0 = 22 + tw(top_v, fs) + 6
    slot = max(46, max(tw(c, fs) for c in cats) + 12)
    pw = slot * len(cats)
    y0 = 32
    yb = y0 + ph
    W = max(x0 + pw + 8, tw(title, 16, True) + 16)
    s = [text(W / 2, 18, title, 16, bold=True)]
    for k in range(nt + 1):
        y = yb - k * gy
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>"
                 % (x0, y, x0 + pw, y, GRID2 if k % 2 == 0 else GRID))
        if k % 2 == 0:
            s.append(text(x0 - 5, y + 5, k * scale, fs, anchor="end"))
    for i, (c, v) in enumerate(zip(cats, vals)):
        cx = x0 + slot * i + slot / 2
        bw = min(30, slot * 0.62)
        h = v / float(scale) * gy
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s'/>" % (cx - bw / 2, yb - h, bw, h, BAR))
        s.append(text(cx, yb + 17, c, fs))
    s.append("<path d='M%.1f %d V%.1f H%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0 - 6, yb, x0 + pw, INK))
    s.append(text(x0 + pw / 2, yb + 36, cat_axis, fs, bold=True))
    mid = y0 + ph / 2
    s.append(text(13, mid, val_axis, fs, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % mid))
    assert tw(val_axis, fs, True) < ph + 26, (val_axis, ph)
    return svg_wrap(W, yb + 42, "".join(s), "column graph: " + title.lower())


PETS = {0: 4, 1: 9, 2: 6, 3: 3, 4: 1, 6: 1}
LAPS = {3: 1, 4: 2, 5: 4, 6: 7, 7: 5, 8: 2, 12: 1}
SPORT = (["AFL", "Cricket", "Netball", "Soccer", "Swimming"], [7, 4, 9, 6, 3])
SHIRT = (["S", "M", "L", "XL"], [5, 12, 9, 2])
FAMILY = (["2", "3", "4", "5", "6"], [3, 6, 10, 5, 2])


def pets_svg():
    return dot_svg("Number of pets at home: 5C", "Number of pets", 0, 6, PETS)


def laps_svg():
    return dot_svg("Laps swum in 10 minutes", "Laps", 3, 12, LAPS)


def sport_svg():
    return col_svg("Favourite sport in 5D", "Sport", "Students", SPORT[0], SPORT[1], 1)


def shirt_svg():
    return col_svg("Shirt sizes for the athletics carnival", "Size", "Students", SHIRT[0], SHIRT[1], 1)


def family_svg():
    return col_svg("People in each family: 5E", "People in the family", "Families", FAMILY[0], FAMILY[1], 1)


def mode_of(d):
    m = max(d.values())
    ks = [k for k, v in d.items() if v == m]
    assert len(ks) == 1
    return ks[0]


# ------------------------------------------------------------ set 1: read line graphs
def set_read():
    its = []
    T, V = BRIS, BRIS.series[0]
    f = fig(T.svg())
    its.append(mcqv(f + "What is each small square on the temperature scale worth?", 1, [5, 2, 10], T.v,
                    "The labels go 20, 25, 30, 35. There are 5 small squares between two labels. 5 ÷ 5 = 1, so each small square is 1 °C."))
    v = T.at("8 am")
    its.append(mcqv(f + "What was the temperature at 8 am?", v, [v - 20, T.at("10 am"), 25], T.v,
                    "Go up from 8 am to the dot, then across. It is 3 small squares above 20, so %s. "
                    "(3 °C forgets that the scale starts at 20, not 0.)" % T.v(v)))
    v = T.at("12 pm")
    its.append(mcqv(f + "What was the temperature at 12 pm?", v, [v - 20, T.at("2 pm"), T.at("10 am")], T.v,
                    "At 12 pm the dot is on the labelled line for 30, so %s. (31 °C is the reading at 2 pm.)" % T.v(v)))
    hi = max(V)
    its.append(mcqv(f + "What was the highest temperature?", hi, [35, T.at("12 pm"), hi - 20], T.v,
                    "The highest dot is at %s. It is 1 small square above 30, so %s. "
                    "(35 °C is the top of the scale, not a reading.)" % (T.xl[V.index(hi)], T.v(hi))))
    tt = T.xl[V.index(28)]
    its.append(mcq(f + "The temperature was measured every 2 hours. At which time did it read 28 °C?", tt,
                   ["12 pm", "2 pm", "6 pm"],
                   "Find 28 on the scale (3 small squares above 25). The dot on that line is at %s." % tt))
    lo = min(V)
    its.append(mcqv(f + "What was the lowest temperature?", lo, [20, T.at("6 pm"), 1], T.v,
                    "The lowest dot is at 6 am: 1 small square above 20, so %s. "
                    "(20 °C is the bottom of the scale, and 26 °C is the reading at 6 pm, not 6 am.)" % T.v(lo)))
    T, V = TANK, TANK.series[0]
    f = fig(T.svg())
    its.append(mcqv(f + "What is each small square on the water scale worth?", 500, [1000, 100, 250], T.v,
                    "The labels go up in 1000s. There are 2 small squares between two labels, so each square is 1000 ÷ 2 = 500 L."))
    v = T.at("Tue")
    its.append(mcqv(f + "How much water was in the tank on Tuesday?", v, [3000, 4000, T.at("Sun")], T.v,
                    "Go up from Tue to the dot. It is on the line halfway between 3000 and 4000, so %s." % T.v(v)))
    v = T.at("Fri")
    its.append(mcqv(f + "How much water was in the tank on Friday?", v, [4000, 4500, 4200], T.v,
                    "Each small square is 500 L. On Friday the dot is halfway between the lines for 4000 and 4500. "
                    "Halfway between them is %s." % T.v(v)))
    d = T.xl[V.index(3750)]
    its.append(mcq(f + "On which day were there 3750 L of water in the tank?", DAYN[d], ["Friday", "Sunday", "Tuesday"],
                   "3750 L is halfway between 3500 and 4000. The dot halfway between those lines is above Sat, so %s." % DAYN[d]))
    hi = max(V)
    its.append(mcqv(f + "What was the most water in the tank during the week?", hi, [5000, T.at("Fri"), 4000], T.v,
                    "The highest dot is on Thursday, on the line halfway between 4000 and 5000: %s. "
                    "(5000 L is the top of the scale, not a reading.)" % T.v(hi)))
    T, V = SUN, SUN.series[0]
    f = fig(T.svg())
    its.append(mcqv(f + "What is each small square on the height scale worth?", 10, [20, 1, 5], T.v,
                    "The labels go up in 20s. There are 2 small squares between two labels, so each square is 20 ÷ 2 = 10 cm."))
    v = T.at("2")
    its.append(mcqv(f + "How tall was the sunflower in week 2?", v, [30, 40, T.at("1")], T.v,
                    "In week 2 the dot is halfway between the lines for 30 and 40, so %s. (20 cm is week 1.)" % T.v(v)))
    v = T.at("4")
    its.append(mcqv(f + "How tall was the sunflower in week 4?", v, [8, T.at("3"), T.at("5")], T.v,
                    "In week 4 the dot is on the labelled line for 80, so %s. (8 cm counts each small square as 1 cm.)" % T.v(v)))
    wk = V.index(100)
    its.append(mcq(f + "In which week did the sunflower first reach 1 metre (100 cm)?", "Week %d" % wk,
                   ["Week %d" % (wk + 1), "Week %d" % (wk - 1), "Week 3"],
                   "Find 100 on the scale. The first dot on that line is in week %d. (In week 4 it was only 80 cm.)" % wk))
    v = V[0]
    its.append(mcqv(f + "How tall was the sunflower when it was first measured, in week 0?", v, [0, 20, 1], T.v,
                    "Week 0 is the first dot. It is on the first small line above 0, so %s. "
                    "(The sunflower was already %s tall, not 0 cm.)" % (T.v(v), T.v(v)), allow_zero=True))
    T, V = BEACH, BEACH.series[0]
    f = fig(T.svg())
    its.append(mcqv(f + "What is each small square on the scale for people worth?", 25, [50, 10, 5],
                    lambda x: unit(x, "person", "people"),
                    "The labels go up in 50s. There are 2 small squares between two labels, so each square is 50 ÷ 2 = 25 people."))
    v = T.at("10 am")
    its.append(mcqv(f + "How many people were at the beach at 10 am?", v, [100, 150, 120], T.v,
                    "At 10 am the dot is halfway between the lines for 100 and 150. Halfway is %s." % num(v)))
    v = T.at("2 pm")
    its.append(mcqv(f + "How many people were at the beach at 2 pm?", v, [250, 300, T.at("12 pm")], T.v,
                    "At 2 pm the dot is halfway between 250 and 300, so %s. (225 people is the 12 pm reading.)" % num(v)))
    tt = T.xl[V.index(200)]
    its.append(mcq(f + "A lifeguard counted the people every 2 hours. At which count were there 200 people?", tt,
                   ["12 pm", "2 pm", "6 pm"],
                   "Find 200 on the scale. The dot on that line is at %s. (At 12 pm there were 225 people.)" % tt))
    return {"title": "Read line graphs and scales", "items": its}


# ------------------------------------------------------------ set 2: change over time
def set_change():
    its = []
    T, V = BRIS, BRIS.series[0]
    f = fig(T.svg())
    d = T.at("2 pm") - T.at("6 am")
    its.append(mcqv(f + "By how much did the temperature rise from 6 am to 2 pm?", d, [T.at("2 pm"), 8, T.at("2 pm") + T.at("6 am")], T.v,
                    "6 am: %s. 2 pm: %s. Rise = %d − %d = %s. (8 is the number of hours, not degrees.)"
                    % (T.v(T.at("6 am")), T.v(T.at("2 pm")), T.at("2 pm"), T.at("6 am"), T.v(d))))
    st = steps(T)
    k = st.index(max(st))
    assert st.count(max(st)) == 1 and k == 1
    labs = [between(T, i) for i in range(6)]
    its.append(mcq(f + "Between which two readings did the temperature rise the most?", labs[1], [labs[2], labs[3], labs[0]],
                   "Find the steepest part going up. 8 am to 10 am: 27 − 23 = 4 °C. 10 am to 12 pm: 3 °C. "
                   "12 pm to 2 pm: only 1 °C, even though 2 pm is the highest point."))
    k = st.index(min(st))
    assert st.count(min(st)) == 1 and k == 4
    its.append(mcq(f + "Between which two readings did the temperature fall the most?", labs[4], [labs[5], labs[3], labs[1]],
                   "The line goes down after 2 pm. 2 pm to 4 pm: 31 − 28 = 3 °C. 4 pm to 6 pm: 28 − 26 = 2 °C. "
                   "So it fell most from 2 pm to 4 pm."))
    d = T.at("2 pm") - T.at("6 pm")
    its.append(mcqv(f + "How much did the temperature fall from 2 pm to 6 pm?", d, [3, T.at("6 pm"), 4], T.v,
                    "2 pm: 31 °C. 6 pm: 26 °C. Fall = 31 − 26 = %s. (3 °C is only the first 2 hours.)" % T.v(d)))
    its.append(mcq(f + "After which reading did the temperature start to fall?", "After 2 pm",
                   ["After 12 pm", "After 4 pm", "After 10 am"],
                   "The line goes up until the dot at 2 pm (31 °C). After 2 pm it goes down."))
    T, V = TANK, TANK.series[0]
    f = fig(T.svg())
    st = steps(T)
    ups = [i for i, x in enumerate(st) if x > 0]
    assert ups == [2]
    labs = ["%s to %s" % (DAYN[T.xl[i]], DAYN[T.xl[i + 1]]) for i in range(6)]
    its.append(mcq(f + "Between which two days did the amount of water go up?", labs[2], [labs[3], labs[0], labs[1]],
                   "The line goes up only once: from Wednesday (3000 L) to Thursday (4500 L). Everywhere else it goes down."))
    d = st[2]
    its.append(mcqv(f + "By how much did the water go up from Wednesday to Thursday?", d, [T.at("Thu"), 3, 1000], T.v,
                    "Thursday 4500 L − Wednesday 3000 L = %s. (3 is the number of small squares; each square is 500 L.)" % T.v(d)))
    d = T.at("Mon") - T.at("Wed")
    its.append(mcqv(f + "How much water was used from Monday to Wednesday?", d, [500, T.at("Wed"), T.at("Mon") + T.at("Wed")], T.v,
                    "Monday 4000 L, Wednesday 3000 L. 4000 − 3000 = %s. (500 L is only one day.)" % T.v(d)))
    assert st[4] == st[5] == -500
    its.append(mcqv(f + "From Friday to Sunday the line falls by the same amount each day. How much water was used each day?",
                    500, [1000, 250, T.at("Sun")], T.v,
                    "Friday 4250 L, Saturday 3750 L, Sunday 3250 L. Each day it fell by 500 L. (1000 L is the total for 2 days.)"))
    its.append(mcq(f + "What does the rise from Wednesday to Thursday most likely show?", "Rain added water to the tank",
                   ["The family used a lot of water", "The tank was empty", "Nothing happened on Thursday"],
                   "Using water makes the line go down. The line goes up, so water was added to the tank, most likely by rain."))
    T, V = PUP, PUP.series[0]
    f = fig(T.svg())
    d = V[-1] - V[0]
    its.append(mcqv(f + "How much mass did the puppy gain from 2 months to 8 months?", d, [V[-1], 6, V[-1] + V[0]], T.v,
                    "2 months: 3 kg. 8 months: 12 kg. Gain = 12 − 3 = %s. (6 is the number of months.)" % T.v(d)))
    st = steps(T)
    k = st.index(max(st))
    assert st.count(max(st)) == 1 and k == 1
    labs = ["%s to %s months" % (T.xl[i], T.xl[i + 1]) for i in range(6)]
    its.append(mcq(f + "Between which two ages did the puppy gain the most mass?", labs[1], [labs[5], labs[2], labs[0]],
                   "Find the steepest part. 3 to 4 months: 8 − 5 = 3 kg. Every other step is 2 kg or less. "
                   "(At 7 and 8 months the puppy is heaviest, but it is not gaining mass.)"))
    flat = [i for i, x in enumerate(st) if x == 0]
    assert flat == [5]
    its.append(mcq(f + "Between which two ages did the puppy’s mass stay the same?", labs[5], [labs[4], labs[0], labs[3]],
                   "A flat line shows no change. From 7 to 8 months the line stays on 12 kg."))
    its.append(mcq(f + "What does the flat part of the line at the end show?", "The puppy’s mass did not change",
                   ["The puppy lost mass", "The puppy stopped eating", "The puppy weighed 0 kg"],
                   "A flat line means the value stays the same: 12 kg at 7 months and at 8 months. "
                   "The graph does not tell us anything about eating."))
    T, V = BEACH, BEACH.series[0]
    f = fig(T.svg())
    st = steps(T)
    k = st.index(max(st))
    assert st.count(max(st)) == 1 and k == 2
    labs = [between(T, i) for i in range(6)]
    its.append(mcq(f + "Between which two counts did the number of people go up the most?", labs[2], [labs[3], labs[1], labs[0]],
                   "10 am to 12 pm: 225 − 125 = 100 people. 8 am to 10 am: 75. 12 pm to 2 pm: 50. "
                   "The steepest rise is 10 am to 12 pm, not the part that reaches the highest point."))
    k = st.index(min(st))
    assert st.count(min(st)) == 1 and k == 5
    its.append(mcq(f + "Between which two counts did the number of people go down the most?", labs[5], [labs[4], labs[3], labs[2]],
                   "2 pm to 4 pm: 275 − 200 = 75 fewer. 4 pm to 6 pm: 200 − 75 = 125 fewer. So 4 pm to 6 pm."))
    a, b = T.at("2 pm"), T.at("8 am")
    its.append(mcqv(f + "How many more people were at the beach at 2 pm than at 8 am?", a - b, [a + b, a, (a - b) // 25], T.v,
                    "2 pm: %d. 8 am: %d. How many more means subtract: %d − %d = %d. "
                    "(9 is the number of small squares; each one is 25 people.)" % (a, b, a, b, a - b)))
    T, V = SUN, SUN.series[0]
    f = fig(T.svg())
    st = steps(T)
    k = st.index(max(st))
    assert st.count(max(st)) == 1 and k == 3
    labs = ["Week %s to week %s" % (T.xl[i], T.xl[i + 1]) for i in range(6)]
    its.append(mcq(f + "Between which two weeks did the sunflower grow the most?", labs[3], [labs[5], labs[4], labs[0]],
                   "Find the steepest part. Week 3 to week 4: 80 − 55 = 25 cm. Week 4 to 5: 20 cm. Week 5 to 6: only 10 cm, "
                   "even though week 6 is the tallest."))
    d = T.at("6") - T.at("4")
    its.append(mcqv(f + "How much did the sunflower grow from week 4 to week 6?", d, [T.at("6"), T.at("6") + T.at("4"), 20], T.v,
                    "Week 4: 80 cm. Week 6: 110 cm. 110 − 80 = %s." % T.v(d)))
    its.append(mcq(f + "From week 5 to week 6 the line is less steep than before. What does that show?",
                   "It grew more slowly", ["It got shorter", "It stopped growing", "It grew faster"],
                   "The line still goes up, so it kept growing (100 cm to 110 cm). Less steep means it grew less that week: "
                   "10 cm instead of 20 cm."))
    return {"title": "Change over time: rises, falls and flat parts", "items": its}


# ------------------------------------------------------------ set 3: compare two lines
def set_two():
    its = []
    T = DM
    D, M = T.series
    f = fig(T.svg())
    i = T.xl.index("10 am")
    its.append(mcqv(f + "Use the key. What was the temperature in Melbourne at 10 am?", M[i], [D[i], 11, M[i] // 2], T.v,
                    "Melbourne is the dashed line with squares. Each small square is 2 °C. At 10 am it is on the labelled line "
                    "for 10, so %s. (%s is Darwin.)" % (T.v(M[i]), T.v(D[i]))))
    i = T.xl.index("2 pm")
    its.append(mcqv(f + "What was the temperature in Darwin at 2 pm?", D[i], [M[i], 31, D[i] // 2], T.v,
                    "Darwin is the solid line with dots. At 2 pm the dot is 1 small square above 30. "
                    "Each small square is 2 °C, so 30 + 2 = %s." % T.v(D[i])))
    its.append(mcqv(f + "How much warmer was Darwin than Melbourne at 2 pm?", D[i] - M[i], [D[i] + M[i], D[i], (D[i] - M[i]) // 2], T.v,
                    "2 pm: Darwin %d °C, Melbourne %d °C. How much warmer means subtract: %d − %d = %d °C. "
                    "(9 is the number of small squares between the lines; each is 2 °C.)" % (D[i], M[i], D[i], M[i], D[i] - M[i])))
    d = M[i] - M[0]
    its.append(mcqv(f + "By how much did the temperature in Melbourne rise from 6 am to 2 pm?", d,
                    [M[i], D[i] - D[0], M[i] + M[0]], T.v,
                    "Melbourne (dashed): 6 am %d °C, 2 pm %d °C. %d − %d = %d °C. (12 °C is the rise in Darwin.)"
                    % (M[0], M[i], M[i], M[0], d)))
    assert D.index(max(D)) == M.index(max(M)) == i
    its.append(mcq(f + "At what time were both cities at their warmest?", "2 pm", ["12 pm", "4 pm", "6 pm"],
                   "The highest point of each line is at 2 pm: Darwin %d °C and Melbourne %d °C." % (D[i], M[i])))
    its.append(mcqv(f + "How much warmer was Darwin than Melbourne at 6 am?", D[0] - M[0], [D[0] + M[0], D[0], (D[0] - M[0]) // 2], T.v,
                    "6 am: Darwin %d °C, Melbourne %d °C. %d − %d = %d °C." % (D[0], M[0], D[0], M[0], D[0] - M[0])))
    assert max(M) < min(D)
    its.append(mcq(f + "Was Melbourne’s highest temperature lower than Darwin’s lowest temperature?",
                   "Yes: 14 °C is lower than 20 °C",
                   ["No: 14 °C is higher than 6 °C", "Yes: 6 °C is lower than 32 °C", "No: they are both 20 °C"],
                   "Melbourne’s highest was %d °C (2 pm). Darwin’s lowest was %d °C (6 am). %d is lower than %d, "
                   "so the whole Melbourne line is below the Darwin line." % (max(M), min(D), max(M), min(D))))
    T = SUNS
    Mi, K = T.series
    f = fig(T.svg())
    its.append(mcqv(f + "How tall was Kai’s sunflower in week 2?", K[2], [Mi[2], 45, 4], T.v,
                    "Kai is the dashed line. In week 2 it is on the line for 40, so %s. (35 cm is Mia’s.)" % T.v(K[2])))
    its.append(mcqv(f + "How tall was Kai’s sunflower in week 6?", K[6], [Mi[6], 120, 105], T.v,
                    "Week 6, dashed line: halfway between 110 and 120, so %s. (110 cm is Mia’s.)" % T.v(K[6])))
    same = [w for w in range(7) if Mi[w] == K[w]]
    assert same == [3]
    its.append(mcq(f + "In which week were the two sunflowers the same height?", "Week 3", ["Week 6", "Week 0", "Week 5"],
                   "Look for the place where the two lines meet. In week 3 both are %d cm." % Mi[3]))
    assert Mi[5] - K[5] == 15
    its.append(mcq(f + "Whose sunflower was taller in week 5, and by how much?", "Mia’s, by 15 cm",
                   ["Kai’s, by 15 cm", "Mia’s, by 185 cm", "Mia’s, by 100 cm"],
                   "Week 5: Mia %d cm, Kai %d cm. Mia’s is taller: %d − %d = 15 cm." % (Mi[5], K[5], Mi[5], K[5])))
    kt = [w for w in range(7) if K[w] > Mi[w]]
    assert kt == [0, 1, 2, 6]
    its.append(mcqv(f + "In how many of the weeks was Kai’s sunflower taller than Mia’s?", len(kt), [3, 2, 7],
                    lambda x: unit(x, "week", "weeks"),
                    "The dashed Kai line is above the solid line in weeks 0, 1, 2 and 6. In week 3 they are the same, so it does not count."))
    d = [abs(a - b) for a, b in zip(Mi, K)]
    assert d.count(max(d)) == 1 and d.index(max(d)) == 5
    its.append(mcq(f + "In which week was the difference between the two heights the biggest?", "Week 5",
                   ["Week 6", "Week 4", "Week 1"],
                   "Find the biggest gap between the lines. Week 5: 15 cm. Week 1 and week 4: 10 cm. Week 6: 5 cm. "
                   "(Week 6 has the tallest sunflower, not the biggest gap.)"))
    T = BOOKS
    A, B = T.series
    f = fig(T.svg())
    Bk = lambda x: unit(x, "book", "books")
    its.append(mcqv(f + "How many books did 5B borrow in week 3?", B[2], [A[2], 33, B[2] - 20], Bk,
                    "5B is the dashed line. The scale starts at 20 and each small square is 2 books. In week 3 the square marker "
                    "is 2 small squares above 30, so %d. (14 forgets that the scale starts at 20.)" % B[2]))
    a, b = A[4], B[4]
    its.append(mcqv(f + "How many books did the two classes borrow altogether in week 5?", a + b, [a - b, a, b + 10], Bk,
                    "Week 5: 5A %d, 5B %d. Altogether means add: %d + %d = %d." % (a, b, a, b, a + b)))
    a, b = A[5], B[5]
    its.append(mcqv(f + "How many more books did 5B borrow than 5A in week 6?", b - a, [a + b, b, (b - a) // 2], Bk,
                    "Week 6: 5B %d, 5A %d. How many more means subtract: %d − %d = %d." % (b, a, b, a, b - a)))
    same = [w for w in range(6) if A[w] == B[w]]
    assert same == [3]
    its.append(mcq(f + "In which week did both classes borrow the same number of books?", "Week 4",
                   ["Week 6", "Week 1", "Week 5"],
                   "The two lines meet in week 4. Both classes borrowed %d books." % A[3]))
    sb = steps(T, 1)
    falls = [w for w, x in enumerate(sb) if x < 0]
    k = sb.index(min(sb))
    assert falls == [0, 3] and k == 3
    labs = ["Week %s to week %s" % (T.xl[w], T.xl[w + 1]) for w in range(5)]
    its.append(mcq(f + "Between which two weeks did 5B’s borrowing fall the most?", labs[3], [labs[0], labs[4], labs[1]],
                   "Use the dashed 5B line. It goes down twice: week 1 to 2 (30 − 26 = 4) and week 4 to 5 (36 − 30 = 6). "
                   "So week 4 to week 5. (Week 5 to 6 is the biggest change, but it is a rise.)"))
    ta, tb = sum(A), sum(B)
    assert (ta, tb) == (198, 200)
    its.append(mcq(f + "Which class borrowed more books in the 6 weeks altogether?", "5B, by 2 books",
                   ["5A, by 2 books", "5B, by 6 books", "Both the same"],
                   "5A: 24 + 30 + 28 + 36 + 42 + 38 = %d. 5B: 30 + 26 + 34 + 36 + 30 + 44 = %d. %d − %d = 2. "
                   "(5B is ahead by 6 in week 6, but you must add all 6 weeks.)" % (ta, tb, tb, ta)))
    d = [abs(a - b) for a, b in zip(A, B)]
    assert d.count(max(d)) == 1 and d.index(max(d)) == 4
    its.append(mcq(f + "In which week was the difference between the classes the biggest?", "Week 5",
                   ["Week 6", "Week 1", "Week 3"],
                   "Week 5: 42 − 30 = 12 books. In weeks 1, 3 and 6 the gap is 6. "
                   "(Week 6 has the highest point, but the gap is only 44 − 38 = 6.)"))
    return {"title": "Compare two lines on one graph", "items": its}


# ------------------------------------------------------------ set 4: mode and the shape of data
def set_mode():
    its = []
    S = lambda x: unit(x, "student", "students")
    f = fig(pets_svg())
    m = mode_of(PETS)
    its.append(mcqv(f + "Each dot is one student. What is the mode of the data?", m, [PETS[m], max(PETS), 2],
                    lambda x: unit(x, "pet", "pets"),
                    "The mode is the value that appears most often: the tallest stack of dots. %d students have 1 pet, "
                    "so the mode is 1 pet. (9 is how many students, and 6 is the highest value, not the mode.)" % PETS[m]))
    its.append(mcqv(f + "How many students have 2 pets?", PETS[2], [2, PETS[1], PETS[2] * 2], S,
                    "Count the dots above 2: there are %d. Each dot is one student." % PETS[2]))
    n = sum(PETS.values())
    pets = sum(k * v for k, v in PETS.items())
    assert (n, pets) == (24, 40)
    its.append(mcqv(f + "How many students are in 5C?", n, [pets, 7, n + 1], S,
                    "Each dot is one student, so count all the dots: 4 + 9 + 6 + 3 + 1 + 1 = %d. "
                    "(40 is the total number of pets, not students.)" % n))
    its.append(mcqv(f + "How many students have no pets?", PETS[0], [PETS[1], 1, 0 + 6], S,
                    "No pets is the value 0. There are %d dots above 0." % PETS[0], ))
    its.append(mcq(f + "Which sentence best describes the shape of the data?", "Most students have 0, 1 or 2 pets",
                   ["Most students have 4 or more pets", "The dots are spread out evenly", "Every student has a pet"],
                   "4 + 9 + 6 = 19 of the 24 students have 0, 1 or 2 pets. Most of the dots are on the left, "
                   "and only a few are on the right."))
    its.append(mcqv(f + "One value is far away from the rest of the data. Which value is it?", 6, [0, 4, 1],
                    lambda x: unit(x, "pet", "pets"),
                    "The dot at 6 is on its own, with a gap at 5. All the other dots are between 0 and 4.", allow_zero=True))
    f = fig(laps_svg())
    m = mode_of(LAPS)
    its.append(mcqv(f + "Each dot is one swimmer. What is the mode of the data?", m, [LAPS[m], max(LAPS), 5],
                    lambda x: unit(x, "lap", "laps"),
                    "The tallest stack of dots is above 6, so the mode is 6 laps. "
                    "(7 is how many swimmers swam 6 laps, and 12 is the highest value.)"))
    more = sum(v for k, v in LAPS.items() if k > 6)
    assert more == 8
    its.append(mcqv(f + "How many swimmers swam more than 6 laps?", more,
                    [sum(v for k, v in LAPS.items() if k >= 6), 3, LAPS[7]], lambda x: unit(x, "swimmer", "swimmers"),
                    "More than 6 means 7, 8 or 12 laps: 5 + 2 + 1 = 8 swimmers. Do not count the swimmers who swam exactly 6."))
    its.append(mcq(f + "Which numbers of laps did nobody swim?", "9, 10 and 11",
                   ["7, 8 and 9", "3 and 12", "10, 11 and 12"],
                   "There are no dots above 9, 10 and 11. This is a gap in the data. 3 and 12 each have one dot."))
    its.append(mcq(f + "Which sentence best describes the shape of the data?", "Most swimmers swam 5, 6 or 7 laps",
                   ["Most swimmers swam 12 laps", "Every swimmer swam a different number of laps",
                    "The swimmers are spread out evenly"],
                   "4 + 7 + 5 = 16 of the 22 swimmers swam 5, 6 or 7 laps. The dots are bunched in the middle, "
                   "with one far away at 12."))
    f = fig(sport_svg())
    cats, vals = SPORT
    m = cats[vals.index(max(vals))]
    its.append(mcq(f + "What is the mode of this data?", m, [str(max(vals)), cats[-1], cats[0]],
                   "The mode is the category chosen most often: the tallest column. That is %s. "
                   "The mode is the sport, not the number %d." % (m, max(vals))))
    v = vals[0]
    its.append(mcqv(f + "How many students chose AFL?", v, [6, 8, max(vals)], S,
                    "The scale is labelled in 2s, with a grid line for every 1. The AFL column ends on the line between 6 and 8, so %d." % v))
    its.append(mcq(f + "What kind of data is “favourite sport”?", "Nominal categorical",
                   ["Ordinal categorical", "Numerical", "It is not data"],
                   "The answers are names of sports, so the data is categorical. The sports have no natural order, "
                   "so it is nominal."))
    f = fig(shirt_svg())
    cats, vals = SHIRT
    m = cats[vals.index(max(vals))]
    its.append(mcq(f + "What is the mode of the shirt sizes?", "Size " + m, [str(max(vals)), "Size XL", "Size S"],
                   "The tallest column is M, so the mode is size M. (12 is how many students, and XL is the biggest size, "
                   "not the most common one.)"))
    its.append(mcq(f + "Shirt size is ordinal categorical data. What does ordinal mean here?",
                   "The sizes have an order: S, M, L, XL",
                   ["The sizes are numbers", "Each size has a different colour", "Every student chose a size"],
                   "Ordinal data is in categories that have a natural order. S is smaller than M, M is smaller than L, and so on."))
    its.append(mcq("Which of these is numerical data?", "The number of pets at home",
                   ["Favourite fruit", "Shirt size (S, M, L)", "Eye colour"],
                   "Numerical data is counted or measured, so the answers are numbers. Favourite fruit and eye colour are "
                   "nominal. Shirt size is ordinal."))
    its.append(mcq("Which of these is ordinal categorical data?", "Answers: never, sometimes, often, always",
                   ["Favourite colour", "Type of pet", "Number of brothers and sisters"],
                   "Never, sometimes, often, always are categories with an order. Colours and pets have no order (nominal). "
                   "Number of brothers and sisters is numerical."))
    f = fig(family_svg())
    cats, vals = FAMILY
    m = cats[vals.index(max(vals))]
    its.append(mcqv(f + "What is the mode of the family sizes?", int(m), [max(vals), int(cats[-1]), 5],
                    lambda x: unit(x, "person", "people"),
                    "The tallest column is above 4, so the mode is 4 people. "
                    "(10 is how many families, and 6 is the biggest family.)"))
    tot = sum(vals)
    mid = vals[1] + vals[2] + vals[3]
    assert (tot, mid) == (26, 21)
    its.append(mcq(f + "Which sentence best describes the shape of the data?", "Most families have 3, 4 or 5 people",
                   ["Most families have 6 people", "Most families have 2 people", "There are the same number of each size"],
                   "6 + 10 + 5 = 21 of the 26 families have 3, 4 or 5 people. The columns are tallest in the middle "
                   "and short at each end."))
    P2 = dict(PETS)
    P2[3] += 1
    assert mode_of(P2) == 1
    its.append(mcqv(fig(pets_svg()) + "A new student with 3 pets joins 5C. What is the mode now?", 1, [3, 2, PETS[1]],
                    lambda x: unit(x, "pet", "pets"),
                    "Add one dot above 3: now 4 students have 3 pets. The tallest stack is still above 1 (9 dots), "
                    "so the mode is still 1 pet."))
    return {"title": "Mode and the shape of data", "items": its}


# ------------------------------------------------------------ set 5: conclusions and word problems
def set_words():
    its = []
    its.append(mcq(fig(BRIS.svg()) + "Which statement is supported by the graph?", "It was warmer at 4 pm than at 10 am",
                   ["It is 31 °C at 2 pm every day", "It rained at 4 pm", "It was coldest at 6 pm"],
                   "4 pm: 28 °C. 10 am: 27 °C. So 4 pm was warmer. The graph shows one day only, so it cannot tell us about "
                   "every day. It does not show rain. 6 pm (26 °C) was warmer than 6 am (21 °C)."))
    T, V = TANK, TANK.series[0]
    its.append(mcq(fig(T.svg()) + "Which statement is supported by the graph?",
                   "There was more water on Thursday than on Monday",
                   ["The family used 500 L every day", "It will rain again next Thursday", "The tank was empty on Wednesday"],
                   "Thursday: 4500 L. Monday: 4000 L. The water did not fall by 500 L every day (Thursday to Friday it fell 250 L). "
                   "The graph cannot tell us about next week. On Wednesday there were still 3000 L."))
    r = V[-1] - 2 * 500
    its.append(mcqv(fig(T.svg()) + "After Sunday the family keeps using 500 L each day, and it does not rain. "
                    "How much water will be in the tank on Tuesday?", r, [V[-1] - 500, V[-1], 2500], T.v,
                    "Sunday: 3250 L. Monday: 3250 − 500 = 2750 L. Tuesday: 2750 − 500 = %s." % T.v(r)))
    its.append(mcqv(fig(T.svg()) + "The tank can hold 5000 L. How much more water could it hold on Thursday?",
                    5000 - T.at("Thu"), [T.at("Thu"), 1000, 5000 + T.at("Thu")], T.v,
                    "On Thursday it held 4500 L. 5000 − 4500 = 500 L more would fill it."))
    Mi, K = SUNS.series
    gm, gk = Mi[-1] - Mi[0], K[-1] - K[0]
    assert gm == gk == 100
    its.append(mcq(fig(SUNS.svg()) + "Kai says, “My sunflower grew more than Mia’s, because it is taller in week 6.” Is he right?",
                   "No: both grew 100 cm",
                   ["Yes: his grew 115 cm", "Yes: his grew 5 cm more", "No: Mia’s grew 110 cm"],
                   "Mia: %d − %d = %d cm. Kai: %d − %d = %d cm. They grew the same amount. Kai’s started taller, "
                   "so it finished taller. (115 cm and 110 cm are heights, not growth.)" % (Mi[-1], Mi[0], gm, K[-1], K[0], gk)))
    D, M = DM.series
    its.append(mcq(fig(DM.svg()) + "Isla says, “Darwin was 18 °C warmer than Melbourne all day.” Is this supported?",
                   "No: at 6 am it was only 14 °C warmer",
                   ["Yes: at 2 pm it was 18 °C warmer", "Yes: the lines are always the same distance apart",
                    "No: Melbourne was warmer at 6 pm"],
                   "At 2 pm the difference was 32 − 14 = 18 °C, but at 6 am it was 20 − 6 = 14 °C. "
                   "One time is not enough to say “all day”."))
    i, j = DM.xl.index("2 pm"), DM.xl.index("6 pm")
    fd, fm = D[i] - D[j], M[i] - M[j]
    assert (fd, fm) == (6, 4)
    its.append(mcq(fig(DM.svg()) + "From 2 pm to 6 pm, which city’s temperature fell more?", "Darwin: it fell 6 °C",
                   ["Melbourne: it fell 4 °C", "Melbourne: it fell 6 °C", "Darwin: it fell 26 °C"],
                   "Darwin: 32 − 26 = 6 °C. Melbourne: 14 − 10 = 4 °C. 6 is more than 4, so Darwin fell more. "
                   "(26 °C is the 6 pm reading, not the fall.)"))
    its.append(mcq(fig(pets_svg()) + "Which statement is supported by the dot plot?",
                   "More students have 1 pet than any other number",
                   ["Most students have 6 pets", "Half the class has no pets", "Students with more pets are happier"],
                   "1 pet has the tallest stack (9 dots). Only 4 of the 24 students have no pets, which is not half. "
                   "The dot plot does not tell us how happy anyone is."))
    its.append(mcq(fig(BEACH.svg()) + "Which statement is supported by the graph?", "The beach was busiest at 2 pm",
                   ["It rained at 6 pm, so people went home", "There are 275 people at 2 pm every Saturday",
                    "The beach was busiest at 6 pm"],
                   "The highest point is at 2 pm (275 people). The graph does not show the weather, and it is one Saturday only, "
                   "so it cannot tell us about every Saturday."))
    a = BEACH.at("2 pm")
    g = -(-a // 50)
    assert g == 6
    its.append(mcqv(fig(BEACH.svg()) + "The surf club wants 1 lifeguard on duty for every 50 people at the beach "
                    "(or part of 50). How many lifeguards are needed at 2 pm?", g, [5, 7, a // 25],
                    lambda x: unit(x, "lifeguard", "lifeguards"),
                    "At 2 pm there were 275 people. 5 lifeguards cover 5 × 50 = 250 people. 25 people are left over, "
                    "so 1 more is needed: 6 lifeguards."))
    hot = [BRIS.xl[k] for k, x in enumerate(BRIS.series[0]) if x >= 30]
    assert hot == ["12 pm", "2 pm"]
    its.append(mcq(fig(BRIS.svg()) + "Jack goes for a swim when the temperature is 30 °C or more. At which readings was it 30 °C or more?",
                   "12 pm and 2 pm", ["2 pm only", "12 pm, 2 pm and 4 pm", "10 am, 12 pm and 2 pm"],
                   "12 pm: 30 °C and 2 pm: 31 °C. 30 °C counts, because it says 30 °C or more. 4 pm (28 °C) and 10 am (27 °C) are below 30."))
    V = PUP.series[0]
    k = next(i for i, x in enumerate(V) if x > 3 * V[0])
    assert PUP.xl[k] == "5"
    its.append(mcq(fig(PUP.svg()) + "Lachlan’s puppy weighed 3 kg at 2 months. At what age did it first weigh more than 3 times as much?",
                   "5 months", ["4 months", "8 months", "6 months"],
                   "3 × 3 kg = 9 kg. At 4 months it was 8 kg, which is not more than 9 kg. At 5 months it was 10 kg, so 5 months."))
    V = SUN.series[0]
    r = V[-1] + 2 * (V[-1] - V[-2])
    its.append(mcqv(fig(SUN.svg()) + "Mia’s sunflower keeps growing the same amount each week as it did from week 5 to week 6. "
                    "How tall will it be in week 8?", r, [V[-1] + 10, V[-1], V[-1] + 2 * 25], SUN.v,
                    "From week 5 to week 6 it grew 110 − 100 = 10 cm. Two more weeks: 110 + 10 + 10 = %s." % SUN.v(r)))
    big = sum(LAPS[k] for k in LAPS if k >= 8)
    assert big == 3
    its.append(mcqv(fig(laps_svg()) + "Swimmers who swam 8 laps or more can join the relay team for the swimming carnival. "
                    "How many swimmers is that?", big, [LAPS[8], 8, LAPS[12]], lambda x: unit(x, "swimmer", "swimmers"),
                    "8 laps or more means 8 and 12 (nobody swam 9, 10 or 11). 2 + 1 = 3 swimmers."))
    cats, vals = SPORT
    d = vals[2] - vals[1]
    its.append(mcqv(fig(sport_svg()) + "How many more students chose netball than cricket?", d, [vals[2] + vals[1], vals[2], vals[1]],
                    lambda x: unit(x, "student", "students"),
                    "Netball: %d. Cricket: %d. How many more means subtract: %d − %d = %d." % (vals[2], vals[1], vals[2], vals[1], d)))
    its.append(mcq(fig(sport_svg()) + "A student says, “Netball is the most popular sport in Australia.” Is this supported by the graph?",
                   "No: the survey is of one class only",
                   ["Yes: netball has the tallest column", "Yes: 9 students chose netball", "No: AFL has the tallest column"],
                   "The graph shows the favourite sport in 5D only. One class cannot tell us about the whole of Australia."))
    cats, vals = SHIRT
    m = vals[1]
    p = -(-m // 5)
    assert p == 3
    its.append(mcqv(fig(shirt_svg()) + "Size M shirts come in packs of 5. How many packs must the school order so every student "
                    "who needs size M gets one?", p, [2, m, 4], lambda x: unit(x, "pack", "packs"),
                    "12 students need size M. 2 packs give 10 shirts, which is not enough. 3 packs give 15 shirts, so order 3 packs."))
    cats, vals = FAMILY
    b = vals[3] + vals[4]
    its.append(mcqv(fig(family_svg()) + "How many families have more than 4 people?", b, [b + vals[2], vals[4], vals[3]],
                    lambda x: unit(x, "family", "families"),
                    "More than 4 means 5 or 6 people: 5 + 2 = 7 families. Families with exactly 4 people do not count."))
    its.append(mcq(fig(family_svg()) + "Which question can you answer using this graph?", "What is the most common family size in 5E?",
                   ["How old is each person in the families?", "Which families have a dog?",
                    "How many families in Perth have 4 people?"],
                   "The graph shows how many people are in each family in 5E. So it can tell us the most common size (the mode). "
                   "It does not show ages, pets or other places."))
    A, B = BOOKS.series
    n = sum(1 for x in A + B if x >= 40)
    assert n == 2
    its.append(mcqv(fig(BOOKS.svg()) + "The librarian gives a class a prize in any week it borrows 40 books or more. "
                    "How many prizes were given in the 6 weeks?", n, [1, 0 + 3, 4], lambda x: unit(x, "prize", "prizes"),
                    "5A borrowed 42 books in week 5, and 5B borrowed 44 books in week 6. Every other point is below 40. "
                    "So 2 prizes."))
    return {"title": "Conclusions from data: word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


LESSON_LG = LG("Temperature in Adelaide on one day", HOURS, "Time", "Temperature (°C)",
               [[14, 16, 19, 23, 25, 22, 18]], 10, 30, 5, 1, u=" °C")
LESSON_DOTS = {0: 2, 1: 4, 2: 7, 3: 5, 4: 2, 8: 1}


def body_html():
    V = LESSON_LG.series[0]
    st = steps(LESSON_LG)
    assert st.index(max(st)) == 2 and st.count(max(st)) == 1
    assert st.index(min(st)) == 5 and st.count(min(st)) == 1
    assert mode_of(LESSON_DOTS) == 2
    return (
        "<h2>Read a line graph</h2>"
        "<p>A line graph shows how something changes over time. Time goes along the bottom. "
        "First check the <b>scale</b>: count the small squares between two labels and work out what one square is worth. "
        "Also check where the scale starts. It does not always start at 0.</p>"
        "<p>To read a value, go up from the time to the dot, then across to the scale.</p>"
        "<figure class='sn-fig'>" + LESSON_LG.svg() +
        "<figcaption>The scale starts at 10. The labels go up in 5s with 5 small squares between them, so each square is 1 °C.</figcaption></figure>" +
        ex("Example 1", "How much did the temperature rise from 6 am to 2 pm?",
           "6 am: %d °C. 2 pm: %d °C. Rise = %d − %d = %d." % (V[0], V[4], V[4], V[0], V[4] - V[0]), "%d °C" % (V[4] - V[0])) +
        "<h2>Rises, falls and flat parts</h2>"
        "<p>A line going <b>up</b> shows an increase. A line going <b>down</b> shows a decrease. A <b>flat</b> line shows no change. "
        "The <b>steepest</b> part shows the fastest change. It is not always next to the highest point.</p>" +
        ex("Example 2", "Between which two readings did the temperature rise the most?",
           "8 am to 10 am: 19 − 16 = 3. 10 am to 12 pm: 23 − 19 = 4. 12 pm to 2 pm: 25 − 23 = 2. The biggest rise is 4 °C.",
           "10 am to 12 pm") +
        "<p>When a graph has two lines, use the <b>key</b> to see which line is which. "
        "“How much warmer” or “how many more” means find the difference: subtract.</p>"
        "<h2>The mode and the shape of data</h2>"
        "<p>In a dot plot, each dot is one piece of data. The <b>mode</b> is the value that appears most often: the tallest stack. "
        "In a column graph, the mode is the category with the tallest column.</p>"
        "<figure class='sn-fig'>" + dot_svg("Books read in the holidays", "Books", 0, 8, LESSON_DOTS) +
        "<figcaption>The tallest stack is above 2. Most students read 1, 2 or 3 books, and one student read 8.</figcaption></figure>" +
        ex("Example 3", "What is the mode?",
           "The tallest stack has 7 dots, above 2. The mode is the value 2, not the number of dots (7) and not the biggest value (8).",
           "2 books") +
        "<p>To describe the <b>shape</b>, say where most of the data is, and point out any gaps or values far away from the rest.</p>"
        "<h2>Kinds of data</h2>" +
        table(["Kind of data", "What the answers are", "Example"], [
            ["Nominal categorical", "Categories with no order", "Favourite sport, eye colour"],
            ["Ordinal categorical", "Categories with an order", "Shirt size S, M, L; never, sometimes, always"],
            ["Numerical", "Numbers you count or measure", "Number of pets, height in cm"],
        ]) +
        "<h2>Is the conclusion supported?</h2>"
        "<p>A conclusion is supported only if the graph shows it. A graph of one day cannot tell you about every day, "
        "and a survey of one class cannot tell you about all of Australia. If the graph does not show something, such as rain, "
        "you cannot say it from the graph.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting each small square as 1", "Work out the scale: 2 squares between 0 and 20 means 10 each"],
            ["Reading the scale as if it starts at 0", "Check the first label: the scale may start at 20"],
            ["Reading the graph at the wrong time", "Go straight up from the time on the bottom axis"],
            ["Choosing the highest point for the biggest rise", "Find the steepest part and subtract"],
            ["Giving the highest value or the number of dots as the mode", "The mode is the value with the most dots"],
            ["Making a conclusion the data does not show", "Check that the graph really shows it"],
        ])
    )


FAQ = [
    {"q": "What do Year 5 students learn about data in the Australian Curriculum?",
     "a": "In Year 5 students interpret line graphs that show change over time and discuss what conclusions can be made. They also collect and show nominal, ordinal and numerical data, and describe it using the mode and the shape of the data."},
    {"q": "How do you read a line graph?",
     "a": "Check what each small square on the scale is worth and where the scale starts. Then go up from the time on the bottom axis to the line, and across to the scale."},
    {"q": "What is the mode in maths?",
     "a": "The mode is the value or category that appears most often. In a dot plot it is the tallest stack of dots, and in a column graph it is the tallest column."},
    {"q": "What is the difference between nominal and ordinal data?",
     "a": "Both are categorical data. Nominal categories have no order, such as favourite sport, while ordinal categories have an order, such as shirt sizes S, M, L."},
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
    rnd = random.Random(5816)
    sets = [set_read(), set_change(), set_two(), set_mode(), set_words()]
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
        "country": "au", "subject": "maths", "grade": "year-5", "slug": "line-graphs-and-data", "sort": 16,
        "updated": UPDATED, "pdf_url": "",
        "title": "Line Graphs and Data: Change over Time and the Mode",
        "seo_title": "Year 5 Line Graphs and Data Worksheets: Change over Time, Mode and Dot Plots (Free, with Answer Key)",
        "short_title": "Line graphs and data",
        "domain": "Statistics",
        "standard_code": "AC9M5ST02",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Interpret line graphs representing change over time; discuss the relationships that are represented and conclusions that can be made",
        "meta_desc": "Free Year 5 maths worksheets on line graphs and data for the Australian Curriculum: read scales, find rises and falls over time, compare two lines, find the mode in dot plots and column graphs, and decide which conclusions the data supports. 100 NAPLAN-style questions with an answer key.",
        "key_big": "Check the scale first. Then look for where the line rises, falls or stays flat.",
        "key_sub": "Work out what one small square is worth and where the scale starts. The steepest part shows the biggest change. The mode is the value that appears most often. A conclusion must be shown by the data.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (graphs and dot plots) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "(line graph|dot plot|column graph)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
