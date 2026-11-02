# -*- coding: utf-8 -*-
"""
UK Year 5 Maths: Line graphs and tables, including timetables (National Curriculum: Year 5 Statistics)
  python3 tools/gen_uk_maths_y5_line_graphs_tables.py
HTML attributes use single quotes (no backslashes in the JSON).
Every graph, table and timetable is drawn from the data below, and every answer is worked out from that data.
"""
import json, re, math, os, random
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
LINE1 = "#2e8b57"
LINE2 = "#c0392b"
RED = "#c0392b"
INK = "#2b2b2b"
GREY = "#8a8f8c"
GRID = "#d5ddd8"
GRID2 = "#9fb0a5"
FILL2 = "#e6f2ea"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"


# ------------------------------------------------------------ helpers
def num(x):
    x = F(x)
    if x.denominator == 1:
        v = x.numerator
        return (MINUS if v < 0 else "") + "{:,}".format(abs(v))
    d = x * 100
    assert d.denominator == 1, x
    v = abs(int(d))
    return "%s%d.%02d" % (MINUS if x < 0 else "", v // 100, v % 100)


def unit(v, one, many):
    return "%s %s" % (num(v), one if F(v) == 1 else many)


def money(p):
    """p in pence: 30p, £4.20, £42.50"""
    p = int(p)
    if p < 100:
        return "%dp" % p
    if p % 100 == 0:
        return "£%s" % "{:,}".format(p // 100)
    return "£%s.%02d" % ("{:,}".format(p // 100), p % 100)


def dur(n):
    """1 hour 3 minutes / 47 minutes / 1 hour"""
    assert n > 0
    hh, mm = divmod(n, 60)
    parts = []
    if hh:
        parts.append("%d hour%s" % (hh, "" if hh == 1 else "s"))
    if mm:
        parts.append("%d minute%s" % (mm, "" if mm == 1 else "s"))
    return " ".join(parts)


def mins(n):
    return "%d minute%s" % (n, "" if n == 1 else "s")


def tmin(t):
    h, m = map(int, t.split(":"))
    return h * 60 + m


def t24(n):
    return "%02d:%02d" % (n // 60 % 24, n % 60)


def naive(a, b):
    """The ‘100 minutes in an hour’ mistake: 15:41 − 14:38 done as 1541 − 1438."""
    return int(b.replace(":", "")) - int(a.replace(":", ""))


def no_exchange_sub(a, b):
    """Column subtraction done digit by digit, always taking the smaller digit from the bigger one."""
    out, k = 0, 1
    while a or b:
        out += abs(a % 10 - b % 10) * k
        a, b, k = a // 10, b // 10, k * 10
    return out


def no_exchange_add(a, b):
    """Column addition that forgets to exchange ten ones for a ten (or ten tens for a hundred)."""
    out, k = 0, 1
    while a or b:
        out += ((a % 10 + b % 10) % 10) * k
        a, b, k = a // 10, b // 10, k * 10
    return out


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
    def __init__(self, title, xl, xt, yt, series, ymin, ymax, lstep, gstep, names=None, u=("", "")):
        self.title, self.xl, self.xt, self.yt = title, xl, xt, yt
        self.series, self.ymin, self.ymax, self.lstep, self.gstep = series, ymin, ymax, lstep, gstep
        self.names, self.u = names, u
        for v in series:
            assert len(v) == len(xl)
            assert all(ymin <= x <= ymax for x in v)
        assert (ymax - ymin) % lstep == 0 and lstep % gstep == 0 and ymin % lstep == 0

    def v(self, x):
        return "%s%s" % (num(x), self.u[0])

    def at(self, x, si=0):
        return self.series[si][self.xl.index(x)]

    def svg(self):
        fs = 14
        nt = (self.ymax - self.ymin) // self.gstep
        gy = max(9, min(20, int(round(150.0 / nt))))
        ph = nt * gy
        ylabs = [num(v) for v in range(self.ymin, self.ymax + 1, self.lstep)]
        slot = max(46, max(tw(c, fs) for c in self.xl) + 10)
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
        return svg_wrap(int(math.ceil(W)), int(H), "".join(s), "line graph: " + self.title.lower())


def times(h0, m0, step, n):
    return [t24(h0 * 60 + m0 + k * step) for k in range(n)]


C = (" °C", " °C")
CM = (" cm", " cm")
M = (" m", " m")

TEMP = LG("Temperature in the playground", times(6, 0, 120, 7), "Time", "Temperature (°C)",
          [[4, 7, 11, 16, 18, 13, 9]], 0, 20, 5, 1, u=C)
PLANT = LG("Height of a bean plant", [str(w) for w in range(7)], "Week", "Height (cm)",
           [[3, 6, 11, 18, 24, 29, 32]], 0, 40, 10, 2, u=CM)
WALK = LG("Freya’s distance from home", times(10, 0, 10, 7), "Time", "Distance (m)",
          [[0, 300, 650, 900, 900, 500, 0]], 0, 1000, 200, 100, u=M)
CHOC = LG("A cup of hot chocolate cooling", [str(m) for m in range(0, 35, 5)], "Minutes after making it",
          "Temperature (°C)", [[80, 65, 55, 45, 40, 35, 30]], 0, 80, 20, 10, u=C)
CITIES = LG("Average temperature", ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"], "Month", "Temperature (°C)",
            [[5, 6, 8, 10, 13, 16, 18], [3, 4, 5, 7, 10, 12, 15]], 0, 20, 5, 1, names=["Bristol", "Aberdeen"], u=C)
BOOKS = LG("Library books borrowed", [str(w) for w in range(1, 7)], "Week", "Books",
           [[24, 31, 28, 36, 42, 38], [30, 26, 33, 36, 29, 45]], 0, 50, 10, 2, names=["Year 5", "Year 6"],
           u=(" books", " books"))
FLOWERS = LG("Height of two sunflowers", [str(w) for w in range(7)], "Week", "Height (cm)",
             [[10, 20, 35, 50, 70, 85, 95], [15, 25, 30, 45, 60, 70, 100]], 0, 100, 20, 10,
             names=["Poppy", "Jack"], u=CM)
PARK = LG("Journey from school to the park", times(15, 30, 5, 7), "Time", "Distance (m)",
          [[0, 250, 500, 750, 1000, 1250, 1500], [0, 600, 1200, 1200, 1200, 1800, 1800]], 0, 2000, 500, 100,
          names=["Isla (walks)", "Leo (cycles)"], u=M)


# ------------------------------------------------------------ tables and timetables
def table_svg(title, head, rows, label, red="?"):
    """head = column headings; rows = lists of cells (first cell = row name). A ‘?’ cell is red."""
    fs, rh = 15, 28
    ncol = len(head)
    cw = []
    for k in range(ncol):
        cells = [head[k]] + [str(r[k]) for r in rows]
        cw.append(int(max(tw(x, fs, True) for x in cells) + 20))
    tot = sum(cw)
    W = int(max(tot + 8, tw(title, 16, True) + 16))
    x0 = (W - tot) / 2
    top = 28
    s = [text(W / 2, 19, title, 16, bold=True)]
    for r, row in enumerate([head] + rows):
        y = top + r * rh
        x = x0
        for k, cell in enumerate(row):
            cell = str(cell)
            hd = r == 0 or k == 0
            s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, cw[k], rh, FILL2 if hd else "#ffffff", GREEN))
            col = RED if cell == red else (GREY if cell == "—" else INK)
            s.append(text(x + cw[k] / 2, y + 19, cell, fs, bold=hd or cell == red, col=col))
            x += cw[k]
    H = top + (len(rows) + 1) * rh + 4
    return svg_wrap(W, H, "".join(s), "table: " + label)


class TT:
    """Timetable: stops (rows) and services (columns). A time of None means the service does not stop there."""
    def __init__(self, title, word, stops, cols):
        self.title, self.word, self.stops, self.cols = title, word, stops, cols

    def t(self, j, stop):
        return self.cols[j][self.stops.index(stop)]

    def name(self, j):
        return "%s %d" % (self.word.capitalize(), j + 1)

    def row(self, stop):
        return [c[self.stops.index(stop)] for c in self.cols]

    def svg(self):
        LW = int(max(max(tw(x, 16) for x in self.stops), tw(self.title, 15, True)) + 24)
        CW, RH = 74, 30
        W = LW + CW * len(self.cols) + 4
        H = RH * (len(self.stops) + 1) + 4
        s = ["<rect x='2' y='2' width='%d' height='%d' fill='%s'/>" % (W - 4, RH, GREEN)]
        s.append("<text x='10' y='%d' font-size='15' font-weight='700' fill='#fff'>%s</text>" % (2 + 21, self.title))
        for j in range(len(self.cols)):
            s.append("<text x='%.0f' y='%d' font-size='15' font-weight='700' fill='#fff' text-anchor='middle'>%s</text>"
                     % (2 + LW + CW * j + CW / 2.0, 2 + 21, self.name(j)))
        for i, st in enumerate(self.stops):
            y = 2 + RH * (i + 1)
            if i % 2:
                s.append("<rect x='2' y='%d' width='%d' height='%d' fill='#eef5f0'/>" % (y, W - 4, RH))
            s.append("<text x='10' y='%d' font-size='16' fill='%s'>%s</text>" % (y + 21, INK, st))
            for j, col in enumerate(self.cols):
                tt = col[i]
                s.append("<text x='%.0f' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                         % (2 + LW + CW * j + CW / 2.0, y + 21, INK if tt else GREY, tt or "—"))
        s.append("<rect x='2' y='2' width='%d' height='%d' fill='none' stroke='%s' stroke-width='1.5'/>" % (W - 4, H - 4, GREEN))
        for j in range(len(self.cols)):
            x = 2 + LW + CW * j
            s.append("<line x1='%d' y1='2' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x, x, H - 2, GREEN))
        lab = self.title.lower()
        return svg_wrap(W, H, "".join(s), "timetable: " + lab)


def make_cols(starts, legs, skip=None):
    cols = []
    for j, st in enumerate(starts):
        col = [t24(tmin(st) + l) for l in legs]
        for (jj, i) in (skip or []):
            if jj == j:
                col[i] = None
        cols.append(col)
    return cols


BUS_STOPS = ["Bus Station", "High Street", "Library", "Hospital", "Retail Park"]
BUS = TT("Number 7 bus", "bus", BUS_STOPS,
         make_cols(["08:45", "09:15", "09:45", "10:15"], [0, 13, 21, 34, 47], skip=[(2, 2)]))
TRAIN_STOPS = ["Westbrook", "Millford", "Ashby Road", "Kingsley", "Northgate"]
TRAIN = TT("Trains to Northgate", "train", TRAIN_STOPS,
           [["14:38", "14:52", "15:05", "15:19", "15:41"],
            ["15:08", None, None, "15:37", "15:56"],
            ["15:38", "15:52", "16:05", "16:19", "16:41"],
            ["16:08", "16:22", "16:35", "16:49", "17:11"]])

LUNCH = {"School dinner": (14, 17), "Packed lunch": (11, 9), "Home": (3, 4)}
CONCERT = {"Adult": (86, 97), "Child": (124, 158)}
ROAD = ["London", "Birmingham", "Manchester", "Leeds"]
ROAD_KM = {("London", "Birmingham"): 190, ("London", "Manchester"): 335, ("London", "Leeds"): 315,
           ("Birmingham", "Manchester"): 140, ("Birmingham", "Leeds"): 195, ("Manchester", "Leeds"): 70}
SWIM = {"Boys": (38, 7), "Girls": (41, 6)}
POOL = [("Monday", "06:30", "20:00"), ("Wednesday", "06:30", "21:30"), ("Saturday", "08:00", "17:30"),
        ("Sunday", "09:30", "16:00")]
TRAVEL = [("Walk", 23), ("Car", 14), ("Bus", 10), ("Bike", 8), ("Scooter", 5)]
FARES = {"Adult": (240, 420), "Child": (120, 210)}      # pence: single, return


def km(a, b):
    return ROAD_KM.get((a, b)) or ROAD_KM[(b, a)]


def lunch_svg():
    rows = [[k, a, b, a + b] for k, (a, b) in LUNCH.items()]
    rows.append(["Total", sum(a for a, b in LUNCH.values()), sum(b for a, b in LUNCH.values()),
                 sum(a + b for a, b in LUNCH.values())])
    return table_svg("Lunch in Year 5", ["Lunch", "5A", "5B", "Total"], rows, "lunch in year 5")


def concert_svg(hide):
    """hide = (row, col) cell shown as ?"""
    rows = [[k, a, b, a + b] for k, (a, b) in CONCERT.items()]
    rows.append(["Total", sum(a for a, b in CONCERT.values()), sum(b for a, b in CONCERT.values()),
                 sum(a + b for a, b in CONCERT.values())])
    r, c = hide
    rows[r][c] = "?"
    return table_svg("Tickets for the school concert", ["Ticket", "Thursday", "Friday", "Total"], rows,
                     "tickets for the school concert")


def concert_val(r, c):
    rows = [[k, a, b, a + b] for k, (a, b) in CONCERT.items()]
    rows.append(["Total", sum(a for a, b in CONCERT.values()), sum(b for a, b in CONCERT.values()),
                 sum(a + b for a, b in CONCERT.values())])
    return rows[r][c]


def road_svg():
    rows = [[a] + [("—" if a == b else km(a, b)) for b in ROAD] for a in ROAD]
    return table_svg("Road distances (km)", [""] + ROAD, rows, "road distances in km")


def swim_svg(hide):
    rows = [[k, a, b, a + b] for k, (a, b) in SWIM.items()]
    rows.append(["Total", sum(a for a, b in SWIM.values()), sum(b for a, b in SWIM.values()),
                 sum(a + b for a, b in SWIM.values())])
    r, c = hide
    val = rows[r][c]
    rows[r][c] = "?"
    return table_svg("Year 5: can you swim 25 m?", ["", "Can", "Cannot", "Total"], rows, "who can swim 25 m"), val


def pool_svg():
    return table_svg("Swimming pool opening times", ["Day", "Opens", "Closes"], [list(p) for p in POOL],
                     "swimming pool opening times")


def travel_svg(hide_bus):
    rows = [[k, ("?" if (hide_bus and k == "Bus") else v)] for k, v in TRAVEL]
    rows.append(["Total", sum(v for k, v in TRAVEL)])
    return table_svg("How Year 5 travel to school", ["Way", "Pupils"], rows, "how year 5 travel to school")


def fares_svg():
    rows = [[k, money(s), money(r)] for k, (s, r) in FARES.items()]
    return table_svg("Bus fares", ["Ticket", "Single", "Return"], rows, "bus fares")


# ------------------------------------------------------------ set 1: read line graphs
def set_read():
    its = []
    T, V = TEMP, TEMP.series[0]
    f = fig(T.svg())
    its.append(mcqv(f + "On the temperature scale, what is each small square worth?", 1, [5, 2, 10], T.v,
                    "The labels go 0, 5, 10, 15, 20. There are 5 small squares between two labels. 5 ÷ 5 = 1, so each small square is 1 °C."))
    v = T.at("10:00")
    its.append(mcqv(f + "What was the temperature at 10:00?", v, [10, 15, T.at("08:00"), 12], T.v,
                    "Go up from 10:00 to the point, then across to the scale. It is 1 small square above 10, so %s." % T.v(v)))
    hi = max(V)
    its.append(mcqv(f + "What was the highest temperature?", hi, [20, T.at("12:00"), T.at("16:00")], T.v,
                    "The highest point is at %s. It is 3 small squares above 15, so %s. (20 °C is the top of the scale, not a reading.)"
                    % (T.xl[V.index(hi)], T.v(hi))))
    lo = min(V)
    its.append(mcqv(f + "What was the lowest temperature?", lo, [6, 0, V[-1], 5], T.v,
                    "The lowest point is at 06:00. It is 4 small squares above 0, so %s. (6 is the time, 06:00, not the temperature.)"
                    % T.v(lo)))
    tt = T.xl[V.index(13)]
    its.append(mcq(f + "At what time was the temperature 13 °C?", tt, ["14:00", "18:00", "12:00"],
                   "Find 13 on the scale (3 small squares above 10). Go across to the line and down: %s." % tt))
    T, V = WALK, WALK.series[0]
    f = fig(T.svg())
    its.append(mcqv(f + "On the distance scale, what is each small square worth?", 100, [200, 10, 50], T.v,
                    "The labels go up in 200s. There are 2 small squares between two labels, so each square is 200 ÷ 2 = 100 m."))
    v = T.at("10:20")
    its.append(mcqv(f + "How far from home was Freya at 10:20?", v, [600, 700, T.at("10:10")], T.v,
                    "At 10:20 the point is halfway between the lines for 600 and 700, so %s." % T.v(v)))
    pk = max(V)
    its.append(mcqv(f + "The park is the furthest point from home on Freya’s walk. How far from home is the park?", pk,
                    [1000, 800, 2 * pk], lambda x: unit(x, "m", "m"),
                    "The highest part of the line is at %s m (1 small square below 1,000). (%s m is there and back.)" % (num(pk), num(2 * pk))))
    labs = ["%s to %s" % (T.xl[k], T.xl[k + 1]) for k in range(6)]
    k = [i for i in range(6) if V[i] == V[i + 1]]
    assert k == [3]
    its.append(mcq(f + "Freya stopped at the park. When was she at the park?", labs[3], [labs[4], labs[2], labs[5]],
                   "When Freya stops, her distance from home does not change, so the line is flat. "
                   "From 10:30 to 10:40 it stays at 900 m."))
    assert V[-1] == 0
    its.append(mcq(f + "At 11:00 the line is back at 0 m. What does this mean?", "She is back at home",
                   ["She is at the park", "She walked 0 m in total", "She is 900 m from home"],
                   "The graph shows the distance from home. 0 m from home means Freya is at home again. "
                   "She walked to the park and back."))
    T, V = PLANT, PLANT.series[0]
    f = fig(T.svg())
    v = T.at("2")
    its.append(mcqv(f + "How tall was the bean plant in week 2?", v, [10, 12, T.at("3"), T.at("1")], T.v,
                    "The labels go up in 10s and each small square is 2 cm. In week 2 the point is halfway between the lines "
                    "for 10 and 12, so %s." % T.v(v)))
    w = T.xl[V.index(24)]
    its.append(mcq(f + "In which week was the plant 24 cm tall?", "Week " + w, ["Week 3", "Week 5", "Week 2"],
                   "Find 24 on the scale: 2 small squares above 20. Go across to the line and down: week %s." % w))
    v = T.at("5")
    its.append(mcqv(f + "How tall was the plant in week 5?", v, [28, 30, T.at("4"), 25], T.v,
                    "In week 5 the point is halfway between the lines for 28 and 30, so %s." % T.v(v)))
    wk = next(i for i, x in enumerate(V) if x > 20)
    its.append(mcq(f + "In which week was the plant first taller than 20 cm?", "Week %d" % wk,
                   ["Week %d" % (wk - 1), "Week %d" % (wk + 1), "Week 2"],
                   "In week %d it was %s, which is not taller than 20 cm. In week %d it was %s, so week %d is the first."
                   % (wk - 1, T.v(V[wk - 1]), wk, T.v(V[wk]), wk)))
    v = V[0]
    its.append(mcqv(f + "How tall was the plant when it was first measured, in week 0?", v, [2, 4, V[1], 1], T.v,
                    "Week 0 is the first point. It is halfway between the lines for 2 and 4, so %s. "
                    "(The plant was already %s tall, not 0 cm.)" % (T.v(v), T.v(v))))
    T, V = CHOC, CHOC.series[0]
    f = fig(T.svg())
    v = T.at("5")
    its.append(mcqv(f + "What was the temperature of the hot chocolate after 5 minutes?", v, [60, 70, 75], T.v,
                    "The labels go up in 20s, so each small square is 10 °C. At 5 minutes the point is halfway between 60 and 70: %s."
                    % T.v(v)))
    m = T.xl[V.index(40)]
    its.append(mcq(f + "After how many minutes was the hot chocolate 40 °C?", "%s minutes" % m,
                   ["25 minutes", "15 minutes", "40 minutes"],
                   "Find 40 on the temperature scale, go across to the line, then down to the minutes: %s minutes." % m))
    v = T.at("15")
    its.append(mcqv(f + "What was the temperature after 15 minutes?", v, [40, 50, 15], T.v,
                    "At 15 minutes the point is halfway between 40 and 50, so %s. (15 is the time, not the temperature.)" % T.v(v)))
    drops = [V[k] - V[k + 1] for k in range(6)]
    k = drops.index(max(drops))
    assert drops.count(max(drops)) == 1 and k == 0
    labs = ["%s to %s minutes" % (T.xl[a], T.xl[a + 1]) for a in range(6)]
    its.append(mcq(f + "When was the hot chocolate cooling fastest?", labs[0], [labs[5], labs[1], labs[3]],
                   "Fastest means the steepest part of the line. From 0 to 5 minutes it fell 80 − 65 = 15 °C. "
                   "In every other 5 minutes it fell 10 °C or less."))
    T, V = TEMP, TEMP.series[0]
    drops = [V[k] - V[k + 1] for k in range(6)]
    k = drops.index(max(drops))
    assert drops.count(max(drops)) == 1 and T.xl[k] == "14:00"
    labs = ["%s to %s" % (T.xl[a], T.xl[a + 1]) for a in range(6)]
    its.append(mcq(fig(T.svg()) + "Between which two times did the temperature fall the most?", labs[k],
                   [labs[k + 1], labs[3], labs[2]],
                   "The line goes down after 14:00. 14:00 to 16:00: 18 − 13 = 5 °C. 16:00 to 18:00: 13 − 9 = 4 °C. "
                   "So it fell most from 14:00 to 16:00. (10:00 to 12:00 is the biggest rise, not a fall.)"))
    return {"title": "Read line graphs and scales", "items": its}


# ------------------------------------------------------------ set 2: compare, sum and difference
def set_compare():
    its = []
    T = BOOKS
    Y5, Y6 = T.series
    f = fig(T.svg())
    B = lambda x: unit(x, "book", "books")
    v = Y5[1]
    its.append(mcqv(f + "How many books did Year 5 borrow in week 2?", v, [Y6[1], 30, 32], B,
                    "Year 5 is the solid line with round dots. Each small square is 2 books. In week 2 the dot is halfway "
                    "between 30 and 32, so %d. (%d is the dashed Year 6 line.)" % (v, Y6[1])))
    a, b = Y5[4], Y6[4]
    its.append(mcqv(f + "How many books were borrowed altogether in week 5?", a + b, [no_exchange_add(a, b), a - b, a], B,
                    "Week 5: Year 5 %d, Year 6 %d. Altogether means add: %d + %d = %d." % (a, b, a, b, a + b)))
    a, b = Y5[5], Y6[5]
    its.append(mcqv(f + "How many more books did Year 6 borrow than Year 5 in week 6?", b - a,
                    [no_exchange_sub(b, a), a + b, b], B,
                    "Week 6: Year 6 %d, Year 5 %d. How many more means subtract: %d − %d = %d." % (b, a, b, a, b - a)))
    same = [i for i in range(6) if Y5[i] == Y6[i]]
    assert same == [3]
    its.append(mcq(f + "In which week did both year groups borrow the same number of books?", "Week 4",
                   ["Week 6", "Week 1", "Week 3"],
                   "Look for the place where the two lines meet. In week 4 both are on %d." % Y5[3]))
    a, b = Y6[0], Y6[1]
    its.append(mcqv(f + "How many books did Year 6 borrow in weeks 1 and 2 altogether?", a + b,
                    [Y5[0] + Y5[1], a - b, a + b + 10], B,
                    "Use the dashed Year 6 line: week 1 %d, week 2 %d. %d + %d = %d. (%d uses the Year 5 line.)"
                    % (a, b, a, b, a + b, Y5[0] + Y5[1])))
    more = [i + 1 for i in range(6) if Y6[i] > Y5[i]]
    assert more == [1, 3, 6]
    its.append(mcqv(f + "In how many of the weeks did Year 6 borrow more books than Year 5?", 3, [2, 4, 6],
                    lambda x: unit(x, "week", "weeks"),
                    "The dashed line is above the solid line in weeks 1, 3 and 6. In week 4 they are the same, so it does not count."))
    T = CITIES
    Br, Ab = T.series
    f = fig(T.svg())
    i = T.xl.index("May")
    its.append(mcqv(f + "How much warmer was Bristol than Aberdeen in May?", Br[i] - Ab[i], [Br[i] + Ab[i], Br[i], 2], T.v,
                    "May: Bristol %d °C, Aberdeen %d °C. How much warmer means find the difference: %d − %d = %d °C."
                    % (Br[i], Ab[i], Br[i], Ab[i], Br[i] - Ab[i])))
    d = [x - y for x, y in zip(Br, Ab)]
    k = d.index(max(d))
    assert d.count(max(d)) == 1 and T.xl[k] == "Jun"
    its.append(mcq(f + "In which month was the difference between the two cities the biggest?", "June",
                   ["July", "January", "May"],
                   "Find the biggest gap between the lines. June: 16 − 12 = 4 °C. Every other month the gap is 2 °C or 3 °C. "
                   "(July is the warmest month, but the gap is only 18 − 15 = 3 °C.)"))
    its.append(mcqv(f + "By how much did the temperature in Aberdeen rise from January to July?", Ab[-1] - Ab[0],
                    [Br[-1] - Br[0], Ab[-1], Ab[-1] + Ab[0]], T.v,
                    "Use the dashed Aberdeen line. January: %d °C. July: %d °C. %d − %d = %d °C. (%d °C is the Bristol line.)"
                    % (Ab[0], Ab[-1], Ab[-1], Ab[0], Ab[-1] - Ab[0], Br[-1] - Br[0])))
    m = T.xl[Ab.index(10)]
    assert m == "May" and T.xl[Br.index(10)] == "Apr"
    its.append(mcq(f + "In which month was the temperature in Aberdeen 10 °C?", "May", ["April", "June", "March"],
                   "Find 10 on the scale and go across to the dashed Aberdeen line: May. (Bristol, the solid line, was 10 °C in April.)"))
    T = FLOWERS
    P, J = T.series
    f = fig(T.svg())
    assert P[4] - J[4] == 10
    its.append(mcq(f + "Whose sunflower was taller in week 4, and by how much?", "Poppy’s, by 10 cm",
                   ["Jack’s, by 10 cm", "Poppy’s, by 130 cm", "Poppy’s, by 70 cm"],
                   "Each small square is 10 cm. Week 4: Poppy %d cm, Jack %d cm. Poppy’s is taller: %d − %d = 10 cm."
                   % (P[4], J[4], P[4], J[4])))
    jt = [i for i in range(7) if J[i] > P[i]]
    assert jt == [0, 1, 6]
    its.append(mcq(f + "Jack’s sunflower was taller at the start. In which week was it taller than Poppy’s again?", "Week 6",
                   ["Week 5", "Week 2", "Week 4"],
                   "From week 2 to week 5 the solid Poppy line is above. In week 6 the dashed Jack line is on top: 100 cm against 95 cm."))
    its.append(mcqv(f + "How much did Poppy’s sunflower grow from week 2 to week 5?", P[5] - P[2],
                    [J[5] - J[2], P[5], P[5] + P[2]], T.v,
                    "Poppy (solid line): week 2 %d cm, week 5 %d cm. %d − %d = %d cm. (%d cm is Jack’s line.)"
                    % (P[2], P[5], P[5], P[2], P[5] - P[2], J[5] - J[2])))
    d = [abs(x - y) for x, y in zip(P, J)]
    k = d.index(max(d))
    assert d.count(max(d)) == 1 and k == 5
    its.append(mcq(f + "In which week was the difference between the two sunflowers the biggest?", "Week 5",
                   ["Week 6", "Week 4", "Week 3"],
                   "Find the biggest gap between the lines. Week 5: 85 − 70 = 15 cm. Week 4: 10 cm. Week 6: 5 cm. "
                   "(Week 6 has the tallest sunflower, not the biggest gap.)"))
    its.append(mcqv(f + "What was the total height of both sunflowers in week 6?", P[6] + J[6], [J[6] - P[6], J[6], 190], T.v,
                    "Week 6: Poppy %d cm (halfway between 90 and 100), Jack %d cm. Total means add: %d + %d = %d cm."
                    % (P[6], J[6], P[6], J[6], P[6] + J[6])))
    T = PARK
    I, L = T.series
    f = fig(T.svg())
    v = T.at("15:45", 0)
    its.append(mcqv(f + "How far had Isla walked by 15:45?", v, [700, 800, T.at("15:45", 1)], T.v,
                    "Use the solid Isla line. Each small square is 100 m. At 15:45 the dot is halfway between 700 and 800: %s."
                    % T.v(v)))
    a, b = T.at("15:40", 1), T.at("15:40", 0)
    its.append(mcqv(f + "How far apart were Isla and Leo at 15:40?", a - b, [a + b, a, b], T.v,
                    "15:40: Leo %s, Isla %s. The distance between them is the difference: %s − %s = %s."
                    % (T.v(a), T.v(b), num(a), num(b), T.v(a - b))))
    a, b = T.at("15:50", 1), T.at("15:50", 0)
    its.append(mcqv(f + "How much further had Leo travelled than Isla at 15:50?", a - b, [a + b, b, 300], T.v,
                    "15:50: Leo %s, Isla %s. %s − %s = %s." % (T.v(a), T.v(b), num(a), num(b), T.v(a - b))))
    flat = [i for i in range(6) if L[i] == L[i + 1] and L[i] < max(L)]
    stop = (len(flat)) * 5
    assert flat == [2, 3] and stop == 10
    its.append(mcqv(f + "Leo stopped at a shop on the way. For how long did he stop?", stop, [5, 15, 20], mins,
                    "The Leo line is flat from 15:40 to 15:50. That is 10 minutes. (The dots are 5 minutes apart, "
                    "and the flat part covers 2 gaps.)"))
    park = max(L)
    its.append(mcqv(f + "The park is %s m from school. How much further did Isla still have to walk at 16:00?" % num(park),
                    park - I[-1], [I[-1], park + I[-1], 250], T.v,
                    "At 16:00 Isla had walked %s. %s − %s = %s still to walk." % (T.v(I[-1]), num(park), num(I[-1]), T.v(park - I[-1]))))
    return {"title": "Compare two lines: sum and difference", "items": its}


# ------------------------------------------------------------ set 3: tables and two-way tables
def set_tables():
    its = []
    P = lambda x: unit(x, "pupil", "pupils")
    f = fig(lunch_svg())
    L = LUNCH
    its.append(mcqv(f + "How many pupils in 5B have a packed lunch?", L["Packed lunch"][1],
                    [L["Packed lunch"][0], sum(L["Packed lunch"]), L["School dinner"][1]], P,
                    "Find the Packed lunch row, then go across to the 5B column: %d. (%d is 5A.)"
                    % (L["Packed lunch"][1], L["Packed lunch"][0])))
    its.append(mcqv(f + "How many pupils in 5A have a school dinner?", L["School dinner"][0],
                    [L["School dinner"][1], sum(L["School dinner"]), L["Packed lunch"][0]], P,
                    "School dinner row, 5A column: %d." % L["School dinner"][0]))
    a5 = sum(a for a, b in L.values())
    b5 = sum(b for a, b in L.values())
    its.append(mcqv(f + "How many pupils are in 5A?", a5, [b5, a5 + b5, L["School dinner"][0]], P,
                    "The Total row at the bottom gives each class. 5A: %d + %d + %d = %d." % (L["School dinner"][0],
                                                                                          L["Packed lunch"][0], L["Home"][0], a5)))
    sd, pl = sum(L["School dinner"]), sum(L["Packed lunch"])
    its.append(mcqv(f + "How many more pupils have a school dinner than a packed lunch?", sd - pl,
                    [sd + pl, L["School dinner"][0] - L["Packed lunch"][0], L["School dinner"][1] - L["Packed lunch"][1]], P,
                    "Use the Total column. School dinner: %d. Packed lunch: %d. %d − %d = %d. (Using only one class gives 3 or 8.)"
                    % (sd, pl, sd, pl, sd - pl)))
    its.append(mcqv(f + "How many pupils are in Year 5 altogether?", a5 + b5, [a5, sd + pl, b5], P,
                    "The bottom right cell is the total of everything: %d + %d = %d pupils." % (a5, b5, a5 + b5)))
    f = fig(pool_svg())
    sat = POOL[2]
    its.append(mcq(f + "What time does the swimming pool close on Saturday?", sat[2], [sat[1], "07:30", POOL[3][2]],
                   "Find the Saturday row, then go across to the Closes column: %s (5:30 pm)." % sat[2]))
    sun = POOL[3]
    d = tmin(sun[2]) - tmin(sun[1])
    assert dur(d) == "6 hours 30 minutes"
    its.append(mcq(f + "How long is the pool open on Sunday?", dur(d),
                   ["6 hours 70 minutes", "7 hours 30 minutes", "5 hours 30 minutes"],
                   "09:30 to 15:30 is 6 hours. 15:30 to 16:00 is 30 minutes. So the pool is open 6 hours 30 minutes. "
                   "(1600 − 930 = 670 treats an hour as 100 minutes.)"))
    lens = [tmin(c) - tmin(o) for _, o, c in POOL]
    k = lens.index(max(lens))
    assert lens.count(max(lens)) == 1 and POOL[k][0] == "Wednesday"
    its.append(mcq(f + "On which day is the pool open for the longest time?", "Wednesday", ["Monday", "Saturday", "Sunday"],
                   "Work out each day: Monday %s, Wednesday %s, Saturday %s, Sunday %s. Wednesday is the longest. "
                   "(Monday opens just as early, but closes earlier.)" % tuple(dur(x) for x in lens)))
    f = fig(road_svg())
    its.append(mcqv(f + "How far is it by road from Birmingham to Leeds?", km("Birmingham", "Leeds"),
                    [km("London", "Birmingham"), km("Birmingham", "Manchester"), km("London", "Leeds")],
                    lambda x: unit(x, "km", "km"),
                    "Find the Birmingham row and go across to the Leeds column: %d km. You get the same number from the "
                    "Leeds row and the Birmingham column." % km("Birmingham", "Leeds")))
    pairs = sorted(ROAD_KM, key=lambda p: ROAD_KM[p])
    nm = lambda p: "%s and %s" % p
    its.append(mcq(f + "Which two cities are the closest?", nm(pairs[0]), [nm(pairs[1]), nm(pairs[2]), nm(pairs[-1])],
                   "Find the smallest number in the table: %d km, between %s and %s." % ((ROAD_KM[pairs[0]],) + pairs[0])))
    a, b = km("London", "Birmingham"), km("Birmingham", "Manchester")
    its.append(mcqv(f + "Mohammed drives from London to Birmingham, then from Birmingham to Manchester. How far does he drive?",
                    a + b, [km("London", "Manchester"), a - b, a], lambda x: unit(x, "km", "km"),
                    "London to Birmingham: %d km. Birmingham to Manchester: %d km. %d + %d = %d km. "
                    "(%d km is the straight road from London to Manchester.)" % (a, b, a, b, a + b, km("London", "Manchester"))))
    a, b = km("London", "Manchester"), km("London", "Leeds")
    its.append(mcqv(f + "How much further is it from London to Manchester than from London to Leeds?", a - b,
                    [a + b, km("Manchester", "Leeds"), 25], lambda x: unit(x, "km", "km"),
                    "London row: Manchester %d km, Leeds %d km. %d − %d = %d km. (70 km is from Manchester to Leeds.)"
                    % (a, b, a, b, a - b)))
    T = lambda x: unit(x, "ticket", "tickets")
    v = concert_val(0, 2)
    f = fig(concert_svg((0, 2)))
    its.append(mcqv(f + "How many adult tickets were sold on Friday?", v,
                    [concert_val(0, 3) + concert_val(0, 1), no_exchange_sub(concert_val(0, 3), concert_val(0, 1)), concert_val(1, 2)], T,
                    "The adult row adds up to %d. Thursday is %d. %d − %d = %d tickets. Check: %d + %d = %d."
                    % (concert_val(0, 3), concert_val(0, 1), concert_val(0, 3), concert_val(0, 1), v, concert_val(0, 1), v,
                       concert_val(0, 3))))
    v = concert_val(1, 3)
    a, b = concert_val(1, 1), concert_val(1, 2)
    f = fig(concert_svg((1, 3)))
    its.append(mcqv(f + "How many child tickets were sold altogether?", v, [no_exchange_add(a, b), b - a, concert_val(2, 2)], T,
                    "Add along the Child row: %d + %d = %d. Remember to exchange: 4 + 8 = 12 ones." % (a, b, v)))
    v = concert_val(2, 3)
    a, b = concert_val(0, 3), concert_val(1, 3)
    f = fig(concert_svg((2, 3)))
    its.append(mcqv(f + "What number is missing from the table?", v, [no_exchange_add(a, b), b, b - a], T,
                    "The bottom right cell is the total of all tickets. Add the Total column: %d + %d = %d. "
                    "Check with the Total row: %d + %d = %d." % (a, b, v, concert_val(2, 1), concert_val(2, 2), v)))
    a, b = CONCERT["Child"]
    its.append(mcq(fig(concert_svg((1, 3))) + "On which day were more child tickets sold, and how many more?",
                   "Friday, %d more" % (b - a), ["Thursday, %d more" % (b - a), "Friday, %d more" % (a + b),
                                                 "Friday, %d more" % b],
                   "Child row: Thursday %d, Friday %d. Friday is more: %d − %d = %d." % (a, b, b, a, b - a)))
    svg, v = swim_svg((0, 2))
    tot = sum(SWIM["Boys"])
    its.append(mcqv(fig(svg) + "How many boys cannot swim 25 m?", v,
                    [tot + SWIM["Boys"][0], sum(x[1] for x in SWIM.values()), SWIM["Girls"][1]], lambda x: unit(x, "boy", "boys"),
                    "There are %d boys. %d of them can swim. %d − %d = %d boys cannot." % (tot, SWIM["Boys"][0], tot,
                                                                                          SWIM["Boys"][0], v)))
    svg, v = swim_svg((2, 1))
    a, b = SWIM["Boys"][0], SWIM["Girls"][0]
    its.append(mcqv(fig(svg) + "How many pupils can swim 25 m?", v, [b - a, 92, 13], P,
                    "Add down the Can column: %d + %d = %d. (92 is everyone in Year 5, and 13 is the Cannot column.)" % (a, b, v)))
    svg, v = swim_svg((2, 3))
    a, b = sum(SWIM["Boys"]), sum(SWIM["Girls"])
    its.append(mcqv(fig(svg) + "How many pupils are in Year 5 altogether?", v, [no_exchange_add(a, b), b - a, 79], P,
                    "Add the Total column: %d + %d = %d. 5 + 7 = 12 ones, so exchange 10 ones for 1 ten. "
                    "Check with the Total row: %d + %d = %d." % (a, b, v, 79, 13, v)))
    known = sum(v for k, v in TRAVEL if k != "Bus")
    tot = sum(v for k, v in TRAVEL)
    bus = dict(TRAVEL)["Bus"]
    its.append(mcqv(fig(travel_svg(True)) + "How many pupils come to school by bus?", bus, [known, tot + known, dict(TRAVEL)["Bike"]], P,
                    "Add the numbers you know: 23 + 14 + 8 + 5 = %d. The total is %d, so %d − %d = %d pupils come by bus."
                    % (known, tot, tot, known, bus)))
    return {"title": "Read and complete tables and two-way tables", "items": its}


# ------------------------------------------------------------ set 4: timetables
def set_timetables():
    its = []
    T = BUS
    f = fig(T.svg())
    S = T.stops
    a = T.t(1, "Hospital")
    its.append(mcq(f + "The bus leaves the Bus Station at 09:15. What time does it get to the Hospital?", a,
                   [T.t(1, "Library"), T.t(2, "Hospital"), T.t(1, "Retail Park")],
                   "Find 09:15 in the Bus Station row. Go down that column (Bus 2) to the Hospital row: %s." % a))
    its.append(mcq(f + "Which bus does not stop at the Library?", "Bus 3", ["Bus 1", "Bus 2", "Bus 4"],
                   "A dash (—) means the bus does not stop there. The dash in the Library row is in the Bus 3 column."))
    a, b = T.t(0, "Bus Station"), T.t(0, "Retail Park")
    d = tmin(b) - tmin(a)
    its.append(mcqv(f + "How long does Bus 1 take from the Bus Station to the Retail Park?", d,
                    [naive(a, b), 13, int(b[3:])], mins,
                    "%s to 09:00 is %d minutes. 09:00 to %s is %d minutes. %d + %d = %d minutes. "
                    "(%d minutes uses 100 minutes in an hour.)" % (a, 60 - int(a[3:]), b, int(b[3:]), 60 - int(a[3:]),
                                                                  int(b[3:]), d, naive(a, b))))
    a = T.t(0, "High Street")
    c, e = T.t(0, "Bus Station"), T.t(0, "Library")
    d = tmin(e) - tmin(a)
    its.append(mcqv(f + "How long does Bus 1 take from the High Street to the Library?", d, [tmin(a) - tmin(c), tmin(e) - tmin(c), 18],
                    mins, "High Street %s, Library %s. %s to %s is %d minutes." % (a, e, a, e, d)))
    arr = "09:31"
    hs = T.row("High Street")
    nxt = min(x for x in hs if x and tmin(x) >= tmin(arr))
    w = tmin(nxt) - tmin(arr)
    its.append(mcqv(f + "Arjun gets to the High Street at %s, just after a bus has left. How long must he wait for the next bus?" % arr,
                    w, [30, tmin(arr) - tmin("09:28"), 13], mins,
                    "The bus at 09:28 has gone. The next bus at the High Street is at %s. From %s to %s is %d minutes."
                    % (nxt, arr, nxt, w)))
    a, b = T.t(1, "High Street"), T.t(1, "Hospital")
    d = tmin(b) - tmin(a)
    its.append(mcqv(f + "How long does it take to go from the High Street to the Hospital?", d,
                    [13, tmin(b) - tmin(T.t(1, "Bus Station")), tmin(T.t(1, "Library")) - tmin(a)], mins,
                    "Use any bus that stops at both. Bus 2: High Street %s, Hospital %s. %s to %s is %d minutes."
                    % (a, b, a, b, d)))
    lim = "10:30"
    hosp = T.row("Hospital")
    j = max(i for i, x in enumerate(hosp) if tmin(x) <= tmin(lim))
    r = T.t(j, "Bus Station")
    its.append(mcq(f + "Zara must be at the Hospital by %s. What is the latest bus she can catch from the Bus Station?" % lim, r,
                   [T.t(j + 1, "Bus Station"), T.t(j - 1, "Bus Station"), T.t(j, "Hospital")],
                   "Look along the Hospital row for the last time before %s: %s. Go up that column to the Bus Station: %s. "
                   "The next bus gets to the Hospital at %s, which is too late." % (lim, hosp[j], r, hosp[j + 1])))
    lib = T.row("Library")
    arr = "09:52"
    nxt = min(x for x in lib if x and tmin(x) >= tmin(arr))
    w = tmin(nxt) - tmin(arr)
    assert nxt == "10:36" and w == 44
    its.append(mcqv(f + "Grace gets to the Library at %s. How long must she wait for a bus?" % arr, w,
                    [tmin("10:06") - tmin(arr), naive(arr, nxt), 30], mins,
                    "Bus 3 does not stop at the Library (—). So the next bus there is Bus 4 at %s. "
                    "%s to 10:00 is 8 minutes, 10:00 to %s is 36 minutes: 8 + 36 = %d minutes." % (nxt, arr, nxt, w)))
    a = T.t(0, "Library")
    late = t24(tmin(a) + 10)
    its.append(mcq(f + "Bus 1 is 10 minutes late at every stop. What time does it get to the Library?", late,
                   [a, t24(tmin(T.t(0, "Bus Station")) + 10), t24(tmin(a) + 20)],
                   "On the timetable Bus 1 gets to the Library at %s. 10 minutes later is %s." % (a, late)))
    n = sum(1 for x in T.row("Hospital") if tmin(x) < tmin("10:00"))
    its.append(mcqv(f + "How many buses get to the Hospital before 10:00?", n, [3, 1, 4], lambda x: unit(x, "bus", "buses"),
                    "Hospital row: %s. Only %s and %s are before 10:00, so %d buses." % (", ".join(T.row("Hospital")),
                                                                                    T.row("Hospital")[0], T.row("Hospital")[1], n)))
    T = TRAIN
    f = fig(T.svg())
    a, b = T.t(0, "Westbrook"), T.t(0, "Northgate")
    d = tmin(b) - tmin(a)
    assert naive(a, b) == 103
    its.append(mcq(f + "How long does Train 1 take from Westbrook to Northgate?", dur(d),
                   ["%d minutes" % naive(a, b), mins(int(b[3:]) - int(a[3:])), mins(int(b[3:]))],
                   "%s to 15:00 is %d minutes. 15:00 to %s is %d minutes. %d + %d = %d minutes = %s. "
                         "(103 minutes takes 1541 − 1438 as if an hour had 100 minutes.)"
                    % (a, 60 - int(a[3:]), b, int(b[3:]), 60 - int(a[3:]), int(b[3:]), d, dur(d))))
    times_ = [tmin(c[4]) - tmin(c[0]) for c in T.cols]
    k = times_.index(min(times_))
    assert times_.count(min(times_)) == 1 and k == 1
    its.append(mcq(f + "Which train is the quickest from Westbrook to Northgate?", "Train 2", ["Train 1", "Train 4", "Train 3"],
                   "Train 2 takes %s. The others take %s. Train 2 is quicker because it does not stop at Millford or Ashby Road."
                   % (dur(times_[1]), dur(times_[0]))))
    q = times_[0] - times_[1]
    its.append(mcqv(f + "How much quicker is Train 2 than Train 1 from Westbrook to Northgate?", q,
                    [30, times_[1], naive(T.t(0, "Westbrook"), T.t(0, "Northgate")) - times_[1]], mins,
                    "Train 1 takes %d minutes and Train 2 takes %d minutes. %d − %d = %d minutes."
                    % (times_[0], times_[1], times_[0], times_[1], q)))
    stop = [T.name(j) for j in range(4) if T.t(j, "Millford")]
    assert stop == ["Train 1", "Train 3", "Train 4"]
    its.append(mcq(f + "Which trains stop at Millford?", "Trains 1, 3 and 4", ["All four trains", "Train 2 only", "Trains 1 and 3"],
                   "Look along the Millford row. Train 2 has a dash (—), so it does not stop. Trains 1, 3 and 4 stop."))
    assert "16:49" in T.row("Kingsley")
    its.append(mcq(f + "Noah’s train gets to Kingsley at 4:49 pm. Which time on the timetable is this?", "16:49",
                   ["04:49", "14:49", "16:19"],
                   "4:49 pm is in the afternoon, so add 12 to the hour: 4 + 12 = 16. Look for 16:49 in the Kingsley row."))
    arr = "15:12"
    ash = T.row("Ashby Road")
    nxt = min(x for x in ash if x and tmin(x) >= tmin(arr))
    w = tmin(nxt) - tmin(arr)
    assert nxt == "16:05"
    its.append(mcqv(f + "Maya gets to Ashby Road station at %s. How long must she wait for the next train?" % arr, w,
                    [naive(arr, nxt), tmin(T.t(1, "Kingsley")) - tmin(arr), 30], mins,
                    "Train 2 does not stop at Ashby Road (—). The next train there is Train 3 at %s. "
                    "%s to 16:00 is 48 minutes, then 5 more minutes: 48 + 5 = %d minutes." % (nxt, arr, w)))
    lim = "16:45"
    ng = T.row("Northgate")
    j = max(i for i, x in enumerate(ng) if tmin(x) <= tmin(lim))
    r = T.t(j, "Westbrook")
    its.append(mcq(f + "Leo must be in Northgate by %s. What is the latest train he can catch from Westbrook?" % lim, r,
                   [T.t(j + 1, "Westbrook"), T.t(j - 1, "Westbrook"), ng[j]],
                   "Northgate row: the last time before %s is %s (Train %d). Go up to Westbrook: %s. Train %d gets in at %s, too late."
                   % (lim, ng[j], j + 1, r, j + 2, ng[j + 1])))
    a, b = T.t(2, "Millford"), T.t(2, "Kingsley")
    d = tmin(b) - tmin(a)
    its.append(mcqv(f + "How long does Train 3 take from Millford to Kingsley?", d,
                    [naive(a, b), tmin(b) - tmin(T.t(2, "Ashby Road")), int(b[3:])], mins,
                    "%s to 16:00 is %d minutes. 16:00 to %s is %d minutes. %d + %d = %d minutes. (Not 67: an hour has 60 minutes.)"
                    % (a, 60 - int(a[3:]), b, int(b[3:]), 60 - int(a[3:]), int(b[3:]), d)))
    a = T.t(3, "Northgate")
    late = t24(tmin(a) + 12)
    its.append(mcq(f + "Train 4 is 12 minutes late. What time does it get to Northgate?", late,
                   [a, t24(tmin(a) - 12), t24(tmin(T.t(3, "Westbrook")) + 12)],
                   "Train 4 should get to Northgate at %s. %s + 12 minutes: 11 + 12 = 23, so %s." % (a, a, late)))
    a, b = T.t(0, "Westbrook"), T.t(2, "Westbrook")
    d = tmin(b) - tmin(a)
    assert d == 60
    its.append(mcq(f + "How long is it between Train 1 and Train 3 leaving Westbrook?", dur(d),
                   ["%d minutes" % naive(a, b), "30 minutes", "1 hour 30 minutes"],
                   "%s to %s is exactly 1 hour (60 minutes). The minutes are the same and the hour goes up by 1. "
                   "(100 minutes takes 1538 − 1438 as if an hour had 100 minutes.)" % (a, b)))
    return {"title": "Timetables in 24-hour time", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_words():
    its = []
    P = lambda x: unit(x, "pupil", "pupils")
    V = PLANT.series[0]
    h, wk = V[-1], 6
    while h <= 40:
        h += 3
        wk += 1
    assert wk == 9
    its.append(mcq(fig(PLANT.svg()) + "After week 6, the bean plant grows 3 cm every week. In which week will it first be taller than 40 cm?",
                   "Week %d" % wk, ["Week 8", "Week 10", "Week 7"],
                   "Week 6: %d cm. Week 7: %d cm. Week 8: %d cm (not taller than 40 cm yet). Week 9: %d cm."
                   % (V[-1], V[-1] + 3, V[-1] + 6, V[-1] + 9)))
    ad_r, ch_r = FARES["Adult"][1], FARES["Child"][1]
    its.append(mcq(fig(fares_svg()) + "Mum and her two children buy return tickets. How much do they pay altogether?",
                   money(ad_r + 2 * ch_r), [money(ad_r + ch_r), money(FARES["Adult"][0] + 2 * FARES["Child"][0]), money(3 * ad_r)],
                   "Adult return %s. Two child returns: 2 × %s = %s. %s + %s = %s."
                   % (money(ad_r), money(ch_r), money(2 * ch_r), money(ad_r), money(2 * ch_r), money(ad_r + 2 * ch_r))))
    s1 = 2 * FARES["Child"][0] - ch_r
    its.append(mcq(fig(fares_svg()) + "How much does a child save by buying a return ticket instead of two single tickets?",
                   money(s1), [money(ch_r - FARES["Child"][0]), money(ch_r + FARES["Child"][0]), money(FARES["Child"][0])],
                   "Two singles: 2 × %s = %s. A return: %s. %s − %s = %s."
                   % (money(FARES["Child"][0]), money(2 * FARES["Child"][0]), money(ch_r), money(2 * FARES["Child"][0]),
                      money(ch_r), money(s1))))
    Y5 = BOOKS.series[0]
    s = sum(Y5)
    its.append(mcqv(fig(BOOKS.svg()) + "Year 5 want to borrow 250 books in these 6 weeks. How many more books do they need to borrow?",
                    250 - s, [s, no_exchange_sub(250, s), 250 + s], lambda x: unit(x, "book", "books"),
                    "Year 5 (solid line): %s = %d. 250 − %d = %d more books."
                    % (" + ".join(str(x) for x in Y5), s, s, 250 - s)))
    a = TRAIN.t(2, "Northgate")
    r = t24(tmin(a) + 12)
    its.append(mcq(fig(TRAIN.svg()) + "Kai catches Train 3. From Northgate station he walks for 12 minutes to the football stadium. "
                   "What time does he get to the stadium?", r,
                   [t24(tmin(TRAIN.t(2, "Westbrook")) + 12), t24(tmin(a) - 12), t24(tmin(a) + 72)],
                   "Train 3 gets to Northgate at %s. %s + 12 minutes = %s." % (a, a, r)))
    d = km("London", "Leeds")
    its.append(mcqv(fig(road_svg()) + "Mohammed drives from Leeds to London and back again. How far does he drive?", 2 * d,
                    [d, d + km("London", "Manchester"), 4 * d], lambda x: unit(x, "km", "km"),
                    "Leeds to London is %d km. There and back is 2 × %d = %d km." % (d, d, 2 * d)))
    V = CHOC.series[0]
    i = next(k for k, x in enumerate(V) if x < 50)
    its.append(mcq(fig(CHOC.svg()) + "Amelia waits until her hot chocolate is below 50 °C. After how many minutes is it first below 50 °C?",
                   "%s minutes" % CHOC.xl[i], ["%s minutes" % CHOC.xl[i - 1], "%s minutes" % CHOC.xl[i + 1], "50 minutes"],
                   "At %s minutes it is %d °C, which is not below 50 °C. At %s minutes it is %d °C, so %s minutes."
                   % (CHOC.xl[i - 1], V[i - 1], CHOC.xl[i], V[i], CHOC.xl[i])))
    k = LUNCH["School dinner"][1]
    p = LUNCH["School dinner"][1] * 250
    its.append(mcq(fig(lunch_svg()) + "A school dinner costs £2.50. How much do the pupils in 5B pay for school dinners in one day?",
                   money(p), [money(LUNCH["School dinner"][0] * 250), money(sum(LUNCH["School dinner"]) * 250), money(k * 200 + 50)],
                   "5B, School dinner: %d pupils. %d × £2 = £%d and %d × 50p = £%s. £%d + £%s = %s."
                   % (k, k, 2 * k, k, num(F(k, 2)), 2 * k, num(F(k, 2)), money(p))))
    ta, tc = CONCERT["Adult"][0], CONCERT["Child"][0]
    r = ta * 400 + tc * 200
    its.append(mcq(fig(concert_svg((2, 3))) + "Adult tickets cost £4 and child tickets cost £2. How much money did Thursday’s tickets make?",
                   money(r), [money((ta + tc) * 200), money((ta + tc) * 400), money(ta * 200 + tc * 400)],
                   "Thursday: %d adults × £4 = £%d. %d children × £2 = £%d. £%d + £%d = %s."
                   % (ta, ta * 4, tc, tc * 2, ta * 4, tc * 2, money(r))))
    sat = POOL[2]
    arr = "16:20"
    w = tmin(sat[2]) - tmin(arr)
    its.append(mcqv(fig(pool_svg()) + "Lily gets to the swimming pool at %s on Saturday. How long can she swim before it closes?" % arr,
                    w, [naive(arr, sat[2]), 50, 10], mins,
                    "Saturday closes at %s. %s to 17:00 is 40 minutes, 17:00 to %s is 30 minutes. 40 + 30 = %d minutes."
                    % (sat[2], arr, sat[2], w)))
    lim = "10:15"
    rp = BUS.row("Retail Park")
    j = max(i for i, x in enumerate(rp) if tmin(x) <= tmin(lim) and BUS.t(i, "Library"))
    r = BUS.t(j, "Library")
    its.append(mcq(fig(BUS.svg()) + "Ethan gets on the bus at the Library. He must be at the Retail Park by %s. "
                   "What is the latest bus he can catch from the Library?" % lim, r,
                   [BUS.t(3, "Library"), BUS.t(0, "Library"), rp[j]],
                   "Retail Park row: %s gets there before %s. That is Bus %d, which leaves the Library at %s. "
                   "Bus 3 gets there at %s, which is too late (and it does not stop at the Library)." % (rp[j], lim, j + 1, r, rp[2])))
    a, b = SWIM["Boys"][0], SWIM["Girls"][0]
    svg, _ = swim_svg((2, 3))
    its.append(mcqv(fig(svg) + "How many more girls than boys can swim 25 m?", b - a,
                    [a + b, sum(SWIM["Girls"]) - sum(SWIM["Boys"]), SWIM["Boys"][1] - SWIM["Girls"][1]], lambda x: unit(x, "girl", "girls"),
                    "Can column: girls %d, boys %d. %d − %d = %d. (2 uses the Total column, not the Can column.)" % (b, a, b, a, b - a)))
    I, L = PARK.series
    t0 = PARK.xl[0]
    t1 = PARK.xl[L.index(max(L))]
    d = tmin(t1) - tmin(t0)
    its.append(mcqv(fig(PARK.svg()) + "How long did Leo take to get from school to the park, including his stop?", d,
                    [d - 10, 30, 55], mins,
                    "Leo leaves at %s and reaches %s m at %s. %s to %s is %d minutes. The 10-minute stop is part of the journey."
                    % (t0, num(max(L)), t1, t0, t1, d)))
    P_, J_ = FLOWERS.series
    gp, gj = P_[-1] - P_[0], J_[-1] - J_[0]
    assert gp == gj == 85
    its.append(mcq(fig(FLOWERS.svg()) + "Poppy says, “My sunflower grew more than Jack’s from week 0 to week 6.” Is she right?",
                   "No: both grew 85 cm", ["Yes: hers grew 95 cm", "No: Jack’s grew 100 cm", "Yes: hers grew 10 cm more"],
                   "Poppy: %d − %d = %d cm. Jack: %d − %d = %d cm. They grew the same amount. "
                   "(95 cm and 100 cm are the heights, not how much they grew.)" % (P_[-1], P_[0], gp, J_[-1], J_[0], gj)))
    Br = CITIES.series[0]
    n = sum(1 for x in Br if x >= 10)
    its.append(mcqv(fig(CITIES.svg()) + "For how many of the months shown was Bristol 10 °C or warmer?", n, [n - 1, n + 1, 7],
                    lambda x: unit(x, "month", "months"),
                    "Bristol (solid line): April 10 °C, May 13 °C, June 16 °C, July 18 °C. That is %d months. "
                    "10 °C counts, because it says 10 °C or warmer." % n))
    d = km("Manchester", "Leeds")
    its.append(mcqv(fig(road_svg()) + "A lorry drives from Manchester to Leeds and back 3 times every day. How far does it drive each day?",
                    6 * d, [3 * d, 2 * d, 4 * d], lambda x: unit(x, "km", "km"),
                    "One trip there and back: 2 × %d = %d km. 3 trips: 3 × %d = %d km." % (d, 2 * d, 2 * d, 6 * d)))
    T = TRAIN
    k_arr = T.t(0, "Kingsley")
    ready = tmin(k_arr) + 80
    j = min(i for i in range(4) if T.t(i, "Kingsley") and tmin(T.t(i, "Kingsley")) >= ready)
    r = T.t(j, "Northgate")
    assert j == 3
    its.append(mcq(fig(T.svg()) + "Ava takes Train 1 from Westbrook to Kingsley. She stays in Kingsley for 1 hour 20 minutes, "
                   "then catches the next train to Northgate. What time does she get to Northgate?", r,
                   [t24(ready), T.t(2, "Northgate"), T.t(2, "Kingsley")],
                   "Train 1 gets to Kingsley at %s. 1 hour 20 minutes later is %s. The next train at Kingsley is Train 4 at %s. "
                   "It gets to Northgate at %s." % (k_arr, t24(ready), T.t(3, "Kingsley"), r)))
    walk, car = dict(TRAVEL)["Walk"], dict(TRAVEL)["Car"]
    its.append(mcqv(fig(travel_svg(False)) + "Half of the pupils who come by car start walking to school instead. "
                    "How many pupils walk now?", walk + car // 2, [walk + car, walk - car // 2, car // 2], P,
                    "Half of %d is %d. These pupils join the %d who already walk: %d + %d = %d."
                    % (car, car // 2, walk, walk, car // 2, walk + car // 2)))
    a, b = PLANT.at("3"), PLANT.at("6")
    its.append(mcqv(fig(PLANT.svg()) + "How much did the bean plant grow from week 3 to week 6?", b - a, [a + b, b, PLANT.at("5") - a],
                    PLANT.v, "Week 3: %d cm. Week 6: %d cm. Growth is the difference: %d − %d = %d cm." % (a, b, b, a, b - a)))
    its.append(mcq(fig(TEMP.svg()) + "At what time was the temperature half of the temperature at 14:00?",
                   TEMP.xl[TEMP.series[0].index(TEMP.at("14:00") // 2)], ["06:00", "10:00", "08:00"],
                   "At 14:00 it was %d °C. Half of %d is %d. The temperature was %d °C at %s."
                   % (TEMP.at("14:00"), TEMP.at("14:00"), TEMP.at("14:00") // 2, TEMP.at("14:00") // 2,
                      TEMP.xl[TEMP.series[0].index(TEMP.at("14:00") // 2)])))
    return {"title": "Word problems with graphs, tables and timetables", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


LESSON_LG = LG("Average temperature", ["Jan", "Feb", "Mar", "Apr", "May", "Jun"], "Month", "Temperature (°C)",
               [[6, 7, 9, 12, 15, 18], [4, 4, 6, 8, 11, 14]], 0, 20, 5, 1, names=["Cardiff", "Glasgow"], u=C)
LESSON_TT = TT("Number 4 bus", "bus", ["Town Hall", "Park Lane", "Station"],
               [["13:40", "13:52", "14:15"], ["14:10", None, "14:43"], ["14:40", "14:52", "15:15"]])


def body_html():
    Cd, Gl = LESSON_LG.series
    return (
        "<h2>Read a line graph</h2>"
        "<p>A line graph shows how something changes, often over time. First check the <b>scale</b>. "
        "Count the small squares between two labels and work out what one square is worth. "
        "Then go up from the bottom axis to the line, and across to the scale.</p>"
        "<p>Some points sit <b>between</b> two grid lines. If a point is halfway between 10 and 12, it shows 11.</p>"
        "<h2>Compare two lines</h2>"
        "<p>When a graph has two lines, check the <b>key</b> to see which line is which. "
        "<b>Sum</b> questions (altogether, in total) mean add. <b>Difference</b> questions (how many more, how much warmer) mean subtract.</p>"
        "<figure class='sn-fig'>" + LESSON_LG.svg() +
        "<figcaption>The labels go up in 5s with 5 small squares between them, so each square is 1 °C. "
        "In April Cardiff was %d °C and Glasgow was %d °C.</figcaption></figure>" % (Cd[3], Gl[3]) +
        ex("Example 1", "How much warmer was Cardiff than Glasgow in April?",
           "April: Cardiff %d °C, Glasgow %d °C. Difference: %d − %d = %d." % (Cd[3], Gl[3], Cd[3], Gl[3], Cd[3] - Gl[3]),
           "%d °C" % (Cd[3] - Gl[3])) +
        "<h2>Read and complete a two-way table</h2>"
        "<p>A two-way table sorts data in two ways at once. Find the <b>row</b> first, then go across to the <b>column</b>. "
        "The Total row and Total column help you find a missing number.</p>" +
        table(["", "5A", "5B", "Total"], [["Walk", "16", "?", "35"], ["Car", "12", "11", "23"], ["Total", "28", "30", "58"]]) +
        ex("Example 2", "How many pupils in 5B walk to school?",
           "The Walk row adds up to 35. 5A is 16. So 5B is 35 − 16 = 19. Check the 5B column: 19 + 11 = 30.", "19 pupils") +
        "<h2>Read a timetable</h2>"
        "<p>A timetable uses the <b>24-hour clock</b>. Each column is one bus or train. Go down a column to follow one journey. "
        "A dash (—) means it does not stop there.</p>"
        "<figure class='sn-fig'>" + LESSON_TT.svg() +
        "<figcaption>Bus 2 does not stop at Park Lane.</figcaption></figure>" +
        ex("Example 3", "How long does Bus 1 take from the Town Hall to the Station?",
           "Count on to the next hour: 13:40 to 14:00 is 20 minutes, 14:00 to 14:15 is 15 minutes. 20 + 15 = 35.", "35 minutes") +
        "<p>Do not take away the times like ordinary numbers: 1415 − 1340 = 75 is wrong, because an hour has 60 minutes, not 100.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting each small square as 1", "Work out the scale: 5 squares between 0 and 10 means 2 each"],
            ["Reading a point between grid lines as the line below", "Halfway between 600 and 700 is 650"],
            ["Reading the graph at the wrong time", "Go straight up from the time on the bottom axis"],
            ["Using the wrong line on a graph with two lines", "Check the key: solid or dashed"],
            ["Adding when the question asks how many more", "How many more, how much warmer: subtract"],
            ["Mixing up rows and columns in a table", "Row first, then go across to the column"],
            ["Taking away times as if an hour had 100 minutes", "Count on to the next hour, then add the minutes"],
        ])
    )


FAQ = [
    {"q": "What statistics do children learn in Year 5?",
     "a": "In Year 5 pupils solve comparison, sum and difference problems using line graphs, and they complete, read and interpret tables, including timetables. This builds on the bar charts and time graphs from Year 4."},
    {"q": "How do you read a line graph in Year 5?",
     "a": "Check what each small square on the scale is worth, then go up from the bottom axis to the line and across to the scale. If the point is halfway between two grid lines, the value is halfway between them too."},
    {"q": "How do you work out journey times on a timetable?",
     "a": "Find the start and end times in the same column, then count on: first to the next hour, then the extra minutes. From 14:38 to 15:41 is 22 + 41 = 63 minutes, or 1 hour 3 minutes."},
    {"q": "What is a two-way table?",
     "a": "A two-way table sorts data by two things at once, such as class and lunch choice. Read across a row and down a column to find a cell, and use the totals to work out any missing numbers."},
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
    rnd = random.Random(5517)
    sets = [set_read(), set_compare(), set_tables(), set_timetables(), set_words()]
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
        "country": "uk", "subject": "maths", "grade": "year-5", "slug": "line-graphs-and-tables", "sort": 17,
        "updated": UPDATED, "pdf_url": "",
        "title": "Line Graphs, Tables and Timetables",
        "seo_title": "Year 5 Line Graphs and Tables Worksheets: Two-Way Tables and Timetables (Free, with Answers)",
        "short_title": "Line graphs and tables",
        "domain": "Statistics",
        "standard_code": "Year 5: Statistics",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Solve comparison, sum and difference problems using information presented in a line graph; complete, read and interpret information in tables, including timetables.",
        "meta_desc": "Free Year 5 maths worksheets on line graphs and tables: read scales and values between grid lines, compare two lines, complete two-way tables and use 24-hour bus and train timetables. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "Check the scale first. Then read across, up or down carefully.",
        "key_sub": "Work out what one small square is worth. Sum means add; difference means subtract. In a table, find the row, then the column. For journey times, count on to the next hour: an hour has 60 minutes, not 100.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (graphs, tables, timetables) so their labels stay readable."""
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
        mark_large(u, "(line graph|table|timetable)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
