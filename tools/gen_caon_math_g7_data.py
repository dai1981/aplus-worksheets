# -*- coding: utf-8 -*-
"""
CA Grade 7 Math: Circle graphs and data (Ontario Curriculum 2020, Grade 7: Data, D1.1, D1.3, D1.5, D1.6)
  python3 tools/gen_caon_math_g7_data.py
Read circle graphs in percents and degrees (also percents of large populations), make a circle graph from a
table (percent × 360°, choose the graph that matches, A–D), choose the best graph and its title, labels, source
and scale, see how adding or removing a value changes the mean, median and mode, and spot misleading graphs
and conclusions (scales that do not start at 0, small and biased samples, outliers, different totals).
Wrong answers come from real student mistakes: 25% drawn as 25°, sectors that do not add up to 100% (or 360°),
using 100 instead of 360, the percent read as a number of people, decimal slips (0.35 × 360 = 12.6), dividing
by the old count after adding a value, the median taken without ordering, and bars judged by height.
Every answer is computed with fractions.Fraction. Circle graphs are drawn exactly from the data (sector angle =
share of 360°), starting at 12 o'clock and going clockwise. Helpers adapted from gen_cabc_math_g7_circle_graphs.py
and gen_caon_math_g6_data.py. Canadian English, Ontario number style (4536, 45 300 000 with no-break spaces).
HTML attributes use single quotes.
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-7")
UPDATED = "2026-11-02"
INK = "#2b2b2b"
GREEN = "#006633"
BAR = "#2e8b57"
GRID = "#d5ddd8"
GRID2 = "#9fb0a5"
FONT = "Arial, Helvetica, sans-serif"
PALETTE = ["#8fc9a3", "#f2d16b", "#9cbfe8", "#f0a58f", "#c9bde6", "#d7dcd9"]
M = "−"
NBSP = "\u00a0"


# ------------------------------------------------------------ numbers
def num(x):
    """Ontario style: no separator for 4 digits, no-break space for 5+; up to 3 decimal places; real minus sign."""
    x = F(x)
    neg = x < 0
    x = abs(x)
    for k in (0, 1, 2, 3):
        d = x * 10 ** k
        if d.denominator == 1:
            v = int(d)
            ip, fp = v // 10 ** k, v % 10 ** k
            s = str(ip) if ip < 10000 else "{:,}".format(ip).replace(",", NBSP)
            if k:
                s += ".%0*d" % (k, fp)
            break
    else:
        raise AssertionError(x)
    return (M if neg else "") + s


def pct(x):
    return num(x) + "%"


def deg(x):
    return num(x) + "°"


def dollars(x):
    x = F(x)
    if x.denominator == 1:
        return "$" + num(x)
    assert (x * 100).denominator == 1
    c = int(x * 100)
    return "$%s.%02d" % (num(c // 100), c % 100)


def unit(v, one, many):
    return "%s %s" % (num(v), one if F(v) == 1 else many)


def stu(v):
    return unit(v, "student", "students")


def ppl(v):
    return unit(v, "person", "people")


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def frs(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else fr(x.numerator, x.denominator)


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def lst(v):
    return ", ".join(num(x) for x in v)


def mean(v):
    return sum(F(x) for x in v) / len(v)


def median(v):
    s = sorted(F(x) for x in v)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def modes(v):
    c = {}
    for x in v:
        c[F(x)] = c.get(F(x), 0) + 1
    m = max(c.values())
    return sorted(k for k, n in c.items() if n == m) if m > 1 else []


# ------------------------------------------------------------ question helpers
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


def svg_wrap(x0, y0, w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='%d %d %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (x0, y0, w, h, w, h, label, FONT, body))


def tw(t, fs, bold=False):
    return len(str(t)) * fs * (0.62 if bold else 0.58)


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK, extra=""):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, extra, t))


def line(x1, y1, x2, y2, col=INK, w=1):
    return "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%s'/>" % (x1, y1, x2, y2, col, w)


# ------------------------------------------------------------ circle graphs
class Pie:
    def __init__(self, title, cats, parts, labels=None, n=None):
        self.title, self.cats, self.parts = title, cats, [F(p) for p in parts]
        self.n = F(n) if n is not None else sum(self.parts)
        assert sum(self.parts) == self.n, (title, parts)
        self.labels = labels or cats
        self.fills = PALETTE[:len(cats)]
        assert len(set(cats)) == len(cats)


def pct_pie(title, data, hide=None):
    cats = [c for c, _ in data]
    labels = ["%s %s" % (c, "?" if c == hide else pct(p)) for c, p in data]
    return Pie(title, cats, [p for _, p in data], labels, n=100)


def deg_pie(title, data, hide=None):
    cats = [c for c, _ in data]
    labels = ["%s %s" % (c, "?" if c == hide else deg(p)) for c, p in data]
    return Pie(title, cats, [p for _, p in data], labels, n=360)


def pie_parts(p, R=56, fs=14):
    s = []
    a0 = 0.0
    pt = lambda a, r: (r * math.sin(math.radians(a)), -r * math.cos(math.radians(a)))
    boxes = []
    for i, k in enumerate(p.parts):
        a1 = a0 + 360.0 * float(k / p.n)
        x1, y1 = pt(a0, R)
        x2, y2 = pt(a1, R)
        large = 1 if a1 - a0 > 180 else 0
        s.append("<path d='M0 0 L%.2f %.2f A%d %d 0 %d 1 %.2f %.2f Z' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x1, y1, R, R, large, x2, y2, p.fills[i], INK))
        am = (a0 + a1) / 2
        sn, cs = math.sin(math.radians(am)), math.cos(math.radians(am))
        rl = R + 7 + 5 * abs(cs)
        lx, ly = sn * rl, -cs * rl + 5
        lab = p.labels[i]
        w = tw(plain(lab), fs)
        if sn > 0.3:
            anc, bx = "start", lx
        elif sn < -0.3:
            anc, bx = "end", lx - w
        else:
            anc, bx = "middle", lx - w / 2
        boxes.append((bx, ly - 11, bx + w, ly + 3, lab))
        s.append(text(lx, ly, lab, fs, anchor=anc))
        a0 = a1
    s.append("<circle cx='0' cy='0' r='%d' fill='none' stroke='%s' stroke-width='1.8'/>" % (R, INK))
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i], boxes[j]
            assert a[2] + 3 < b[0] or b[2] + 3 < a[0] or a[3] + 1 < b[1] or b[3] + 1 < a[1], (p.title, a, b)
    xs = [b[0] for b in boxes] + [-R - 2]
    xe = [b[2] for b in boxes] + [R + 2]
    ys = [b[1] for b in boxes] + [-R - 2]
    ye = [b[3] for b in boxes] + [R + 2]
    if p.title:
        ty = min(ys) - 10
        s.append(text(0, ty, p.title, 15, bold=True))
        tww = tw(p.title, 15, True)
        bbox = (min(min(xs), -tww / 2), ty - 14, max(max(xe), tww / 2), max(ye))
    else:
        bbox = (min(xs), min(ys), max(xe), max(ye))
    return "".join(s), bbox


def pie_svg(*pies, label=None):
    parts = [pie_parts(p) for p in pies]
    x = 0.0
    top = min(b[1] for _, b in parts)
    bot = max(b[3] for _, b in parts)
    body = []
    for el, b in parts:
        dx = x - b[0]
        body.append("<g transform='translate(%.1f 0)'>%s</g>" % (dx, el))
        x += (b[2] - b[0]) + 30
    W = x - 30
    lab = label or ("circle graphs: " if len(pies) > 1 else "circle graph: ") + " and ".join(p.title.lower() for p in pies)
    return svg_wrap(-6, int(math.floor(top)) - 4, int(math.ceil(W)) + 12, int(math.ceil(bot - top)) + 10,
                    "".join(body), lab)


def mini_pies(options, fills, label, R=38):
    """options: four lists of (letter, angle); a part of the circle left over stays white. Labelled A–D below."""
    pitch = 2 * R + 26
    s = []
    pt = lambda cx, a, r: (cx + r * math.sin(math.radians(a)), R + 4 + -r * math.cos(math.radians(a)))
    for gi, sectors in enumerate(options):
        cx = R + 4 + gi * pitch
        cy = R + 4
        tot = sum(a for _, a in sectors)
        assert tot <= 360
        s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='#ffffff'/>" % (cx, cy, R))
        a0 = 0.0
        for k, (let, a) in enumerate(sectors):
            a1 = a0 + float(a)
            x1, y1 = pt(cx, a0, R)
            x2, y2 = pt(cx, a1, R)
            s.append("<path d='M%.1f %.1f L%.2f %.2f A%d %d 0 %d 1 %.2f %.2f Z' fill='%s' stroke='%s' stroke-width='1.3'/>"
                     % (cx, cy, x1, y1, R, R, 1 if a1 - a0 > 180 else 0, x2, y2, fills[let], INK))
            if a >= 34:
                am = (a0 + a1) / 2
                r = R * (0.58 if a >= 60 else 0.68)
                lx, ly = pt(cx, am, r)
                s.append(text(lx, ly + 5, let, 14, bold=True))
            a0 = a1
        if tot < 360:
            x1, y1 = pt(cx, 0, R)
            s.append("<line x1='%.1f' y1='%.1f' x2='%.2f' y2='%.2f' stroke='%s' stroke-width='1.3'/>" % (cx, cy, x1, y1, INK))
        s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='none' stroke='%s' stroke-width='1.6'/>" % (cx, cy, R, INK))
        s.append(text(cx, 2 * R + 26, "ABCD"[gi], 16, bold=True))
    W = 4 * pitch - 26 + 8
    return svg_wrap(0, 0, int(W), 2 * R + 32, "".join(s), label)


def match_item(data, key, kind, wrong_opts, lead, e_right, e_wrongs):
    """'Which circle graph matches?' The graph order is fixed when balance() picks the answer position."""
    fills = {let: PALETTE[i] for i, (let, _) in enumerate(data)}
    for o in wrong_opts:
        assert o != data and sum(a for _, a in o) <= 360
    assert sum(a for _, a in data) == 360

    def build(t):
        opts = list(wrong_opts)
        notes = list(e_wrongs)
        opts.insert(t, data)
        notes.insert(t, None)
        L = "ABCD"
        q = fig(mini_pies(opts, fills, "circle graphs A, B, C and D: " + kind)) + lead + " Key: " + key + "."
        e = "Graph %s is right. %s " % (L[t], e_right)
        e += " ".join("Graph %s %s" % (L[i], n) for i, n in enumerate(notes) if n)
        return {"q": q, "c": ["A", "B", "C", "D"], "a": t, "e": e}
    return {"_build": build}


# ------------------------------------------------------------ bar and broken-line graphs
def yaxis_title(s, val_axis, y0, ph, fs=14):
    mid = y0 + ph / 2
    assert tw(val_axis, fs, True) < ph + 30, (val_axis, ph)
    s.append(text(13, mid, val_axis, fs, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % mid))


def bar_svg(title, cat_axis, val_axis, cats, vals, ymin, ymax, gstep, lstep, gy=14, bw=44, slot=110, lab=num):
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
    return svg_wrap(0, 0, W, yb + 46, "".join(s), "bar graph: " + title.lower())


def bline_svg(title, x_axis, y_axis, xlabels, vals, ymin, ymax, gstep, lstep, gy=12, slot=64, lab=num):
    fs = 14
    assert (ymax - ymin) % lstep == 0 and lstep % gstep == 0
    assert len(vals) == len(xlabels) and all(ymin <= x <= ymax for x in vals)
    nt = (ymax - ymin) // gstep
    ph = nt * gy
    x0 = 24 + max(tw(lab(ymax), fs), tw(lab(ymin), fs)) + 6
    slot = max(slot, max(tw(c, fs) for c in xlabels) + 10)
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
    pts = [(x0 + slot * i + slot / 2, yb - float(F(val) - ymin) / gstep * gy) for i, val in enumerate(vals)]
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='2.5'/>"
             % (" ".join("%.1f,%.1f" % (a, b) for a, b in pts), GREEN))
    for a, b in pts:
        s.append("<circle cx='%.1f' cy='%.1f' r='4.5' fill='%s'/>" % (a, b, GREEN))
    s.append("<path d='M%.1f %d V%.1f H%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0 - 6, yb, x0 + pw, INK))
    s.append(text(x0 + pw / 2, yb + 40, x_axis, fs, bold=True))
    yaxis_title(s, y_axis, y0, ph)
    return svg_wrap(0, 0, W, yb + 48, "".join(s), "broken-line graph: " + title.lower())


# ------------------------------------------------------------ set 1: read circle graphs
def set_read():
    its = []
    D = deg
    a = pct_pie("How Grade 7 students get to school", [("Walk", 30), ("Bus", 35), ("Car", 25), ("Bike", 10)])
    f = fig(pie_svg(a))
    its.append(mcqv(f + "What percent of the students take the bus?", 35, [65, 25, 126], pct,
                    "Read the label on the Bus sector: 35%. (65% is everyone else, and 126 is the angle of the sector in degrees.)"))
    its.append(mcqv(f + "What is the angle of the Walk sector?", 108, [30, F(54, 5), 252], D,
                    "30% × 360° = 0.3 × 360° = 108°. (30° reads the percent as degrees, 10.8° puts the decimal point "
                    "in the wrong place, and 252° is the rest of the circle.)"))
    its.append(mcqv(f + "The class has 40 students. How many take the bus?", 14, [35, 26, 140], stu,
                    "35% of 40 = 0.35 × 40 = 14 students. (35 is the percent, 26 students do not take the bus, "
                    "and 140 forgets to divide by 100.)"))
    s = pct_pie("Favourite season", [("Summer", 40), ("Winter", 25), ("Fall", 20), ("Spring", 15)], hide="Spring")
    its.append(mcqv(fig(pie_svg(s)) + "What percent of the students chose spring?", 15, [85, 275, 25], pct,
                    "40% + 25% + 20% = 85%. The whole circle is 100%, so spring is 100% − 85% = 15%. "
                    "(275 subtracts from 360: percents add up to 100, not 360.)"))
    day = deg_pie("Kai’s day (24 hours)", [("Sleep", 135), ("School", 90), ("Homework", 30), ("Sports", 45),
                                           ("Other", 60)])
    f = fig(pie_svg(day))
    its.append(mcqv(f + "What percent of Kai’s day is school?", 25, [90, 6, 75], pct,
                    "90° ÷ 360° = 0.25 = 25%. (90 is the angle, and 6 is the number of hours.)"))
    its.append(mcqv(f + "How many hours does Kai sleep?", 9, [135, F(27, 2), F(75, 2)], lambda v: unit(v, "hour", "hours"),
                    "The whole day, 24 hours, is 360°, so 1 hour is 360° ÷ 24 = 15°. 135° ÷ 15° = 9 hours. "
                    "(13.5 divides by 10, and 37.5 is the percent.)"))
    its.append(mcq(f + "Which sector is %s of Kai’s day?" % fr(1, 8), "Sports", ["Homework", "Other", "School"],
                   "%s of 360° = 45°. The Sports sector is 45° (3 hours). (Homework is 30° and Other is 60°.)" % fr(1, 8)))
    w = deg_pie("Favourite winter activity", [("Skating", 126), ("Skiing", 99), ("Tobogganing", 63),
                                              ("Snowboarding", 72)], hide="Snowboarding")
    f = fig(pie_svg(w))
    its.append(mcqv(f + "What is the angle of the Snowboarding sector?", 72, [288, 20, 82], D,
                    "126° + 99° + 63° = 288°. The angles add up to 360°, so 360° − 288° = 72°. "
                    "(288° is the other three sectors, 20 is the percent, and 82° is a subtraction slip.)"))
    its.append(mcqv(f + "What percent of the students chose skating?", 35, [126, F(63, 5), 65], pct,
                    "126° ÷ 360° = 0.35 = 35%. (126 is the angle, not the percent, and 65% is everyone else.)"))
    c = deg_pie("Favourite city to visit", [("Montréal", 120), ("Vancouver", 108), ("Toronto", 72), ("Halifax", 60)])
    f = fig(pie_svg(c))
    its.append(mcq(f + "Which sector is %s of the circle graph?" % fr(1, 3), "Montréal", ["Vancouver", "Toronto", "Halifax"],
                   "%s of 360° = 120°. The Montréal sector is 120°." % fr(1, 3)))
    its.append(mcqv(f + "What percent of the students chose Vancouver?", 30, [108, F(54, 5), 70], pct,
                    "108° ÷ 360° = 0.3 = 30%. (108 is the angle, and 70% is everyone else.)"))
    its.append(mcqv(f + "90 students were asked. How many chose Toronto?", 18, [72, 20, 288], stu,
                    "Each student is 360° ÷ 90 = 4°. 72° ÷ 4° = 18 students. "
                    "(20 is the percent, and 288 multiplies 72 by 4 instead of dividing.)"))
    its.append(mcq(f + "Which statement is true?", "Montréal and Halifax make half",
                   ["Toronto is 72% of the students", "Vancouver is more than one-third", "Halifax is twice Toronto"],
                   "Montréal 120° + Halifax 60° = 180°, half of the circle. Toronto is 72°, which is 20%, not 72%. "
                   "Vancouver 108° is less than 120°. Halifax is smaller than Toronto."))
    its.append(mcqv("A sector is 12.5% of a circle graph. What is its angle?", 45, [F(25, 2), F(9, 2), 90], D,
                    "12.5%% × 360° = 0.125 × 360° = 45°. Check: 12.5%% is %s, and 360° ÷ 8 = 45°. "
                    "(4.5° puts the decimal point in the wrong place.)" % frs(F(1, 8))))
    its.append(mcqv("A sector of a circle graph has an angle of 54°. What percent is it?", 15, [54, F(27, 5), 85], pct,
                    "54° ÷ 360° = 0.15 = 15%. (54% reads the degrees as a percent.)"))
    v = pct_pie("How 2 400 000 viewers watched the final", [("TV", 55), ("Streaming", 35), ("Radio", 10)])
    f = fig(pie_svg(v))
    V = lambda x: unit(x, "viewer", "viewers")
    assert F(35, 100) * 2400000 == 840000
    its.append(mcqv(f + "How many viewers watched by streaming?", 840000, [84000, 8400000, 1560000], V,
                    "35% of 2 400 000 = 0.35 × 2 400 000 = 840 000 viewers. "
                    "(84 000 and 8 400 000 have the place value wrong, and 1 560 000 is everyone else.)"))
    its.append(mcqv(f + "How many more viewers watched on TV than on the radio?", 1080000, [45, 1320000, 108000], V,
                    "TV − radio = 55% − 10% = 45%. 45% of 2 400 000 = 0.45 × 2 400 000 = 1 080 000 viewers. "
                    "(45 is the difference in percent, 1 320 000 is the TV viewers only, and 108 000 has the place value wrong.)"))
    assert F(18, 100) * 650000 == 117000
    its.append(mcqv("A circle graph shows the ages of the 650 000 people in a city. The sector for children aged 0 to 14 "
                    "is 18%. How many children is that?", 117000, [11700, 1170000, 533000], ppl,
                    "1% of 650 000 = 6500. 18% = 18 × 6500 = 117 000 people. "
                    "(11 700 and 1 170 000 put the place value wrong, and 533 000 are the other 82%.)"))
    its.append(mcqv("In a survey, 30% of the people asked chose hockey. That is 450 000 people. "
                    "How many people answered the survey?", 1500000, [135000, 1350000, 4500000], ppl,
                    "30% is 450 000, so 10% is 450 000 ÷ 3 = 150 000. 100% is 10 × 150 000 = 1 500 000 people. "
                    "(135 000 is 30% of 450 000, and 1 350 000 multiplies by 3 instead of dividing.)"))
    its.append(mcqv("In a survey of 1 000 000 people, 250 000 chose loons as their favourite bird. "
                    "What is the angle of the loon sector?", 90, [25, 250, 9], D,
                    "250 000 ÷ 1 000 000 = 0.25 = 25%. 25% × 360° = 90°. "
                    "(25° is the percent used as degrees, the mistake “25% = 25°”.)"))
    return {"title": "Read circle graphs: percents and degrees", "items": its}


# ------------------------------------------------------------ set 2: make a circle graph from a table
def set_make():
    its = []
    D = deg
    its.append(mcq("You have a table of counts. What do you do first to make a circle graph?", "Find the total",
                   ["Draw the biggest sector", "Use 1° for each person", "Multiply each count by 100"],
                   "First add the counts to find the total. Then find each part as a percent of the total, "
                   "and each angle as percent × 360°."))
    its.append(mcqv("To change a percent into a sector angle, you multiply the percent by …", F(18, 5), [1, 100, 360], num,
                    "1% of 360° is 360° ÷ 100 = 3.6°. So 25% is 25 × 3.6° = 90°. "
                    "(Multiplying by 1 gives the mistake 25% = 25°.)"))
    its.append(mcqv("A sector is 25% of a circle graph. What is its angle?", 90, [25, 75, 270], D,
                    "25% × 360° = 0.25 × 360° = 90°. A 25% sector is NOT 25°: it is one-quarter of the circle, a right angle."))
    its.append(mcqv("A sector is 40% of a circle graph. What is its angle?", 144, [40, F(72, 5), 160], D,
                    "40% × 360° = 0.4 × 360° = 144°. (14.4° puts the decimal point in the wrong place, "
                    "and 160° multiplies by 4 instead of 3.6.)"))
    its.append(mcqv("A sector is 15% of a circle graph. What is its angle?", 54, [15, F(27, 5), 45], D,
                    "15% × 360° = 0.15 × 360° = 54°. (45° multiplies by 3 instead of 3.6.)"))
    tab = "Favourite lunch of 60 students: pizza 21, sushi 15, tacos 12, soup 9, salad 3."
    assert 21 + 15 + 12 + 9 + 3 == 60
    its.append(mcqv(tab + " What percent should the pizza sector show?", 35, [21, 39, 42], pct,
                    "%s = 21 ÷ 60 = 0.35 = 35%%. (39 students did not choose pizza, and 42 doubles 21, "
                    "which works only for a total of 50.)" % fr(21, 60)))
    its.append(mcqv(tab + " How many degrees stand for each student?", 6, [60, F(18, 5), 300], D,
                    "360° ÷ 60 = 6° for each student. (3.6° is 1%, not one student.)"))
    its.append(mcqv(tab + " What angle should the sushi sector be?", 90, [15, 25, 150], D,
                    "15 × 6° = 90°. (25 is the percent, not the angle, and 150 uses 10° for each student.)"))
    its.append(mcqv(tab + " What angle should the salad sector be?", 18, [3, 5, 30], D,
                    "3 × 6° = 18°. (5 is the percent, and 30 uses 10° for each student.)"))
    assert F(9, 40) == F(225, 1000)
    its.append(mcqv("A table shows that 9 of 40 students chose ringette. What percent should the sector show?", F(45, 2),
                    [9, 31, 36], pct,
                    "%s = 9 ÷ 40 = 0.225 = 22.5%%. (31 students did not choose ringette, and 36 multiplies 9 by 4 "
                    "instead of 2.5.)" % fr(9, 40)))
    its.append(mcqv("A table shows that 5 of 24 students chose soccer. What angle should the soccer sector be?", 75,
                    [5, 21, 50], D,
                    "Each student is 360° ÷ 24 = 15°. 5 × 15° = 75°. "
                    "(21 is about the percent, and 50 uses 10° for each student.)"))
    its.append(mcq("24 students: walk 8, bus 10, car 6. Which sector angles are correct?", "120°, 150°, 90°",
                   ["8°, 10°, 6°", "33°, 42°, 25°", "120°, 150°, 80°"],
                   "Each student is 360° ÷ 24 = 15°. 8 × 15° = 120°, 10 × 15° = 150°, 6 × 15° = 90°. Check: 120 + 150 + 90 = 360. "
                   "(33°, 42°, 25° are the rounded percents used as degrees.)"))
    its.append(mcq("Hockey 35%, soccer 30%, basketball 20%, other 15%. Which sector angles are correct?",
                   "126°, 108°, 72°, 54°", ["35°, 30°, 20°, 15°", "105°, 90°, 60°, 45°", "126°, 108°, 72°, 64°"],
                   "Multiply each percent by 3.6°: 126°, 108°, 72°, 54°. They add up to 360°. "
                   "(105°, 90°, 60°, 45° multiply by 3 and add up to only 300°.)"))
    its.append(mcq("Hana’s table says: soccer 40%, hockey 30%, swimming 25%, tennis 15%. Why can’t she make a circle graph?",
                   "The percents add to 110%", ["They must add to 360%", "Tennis is too small", "There are too many sports"],
                   "40 + 30 + 25 + 15 = 110. The sectors of a circle graph must add up to exactly 100%, so one percent is wrong. "
                   "(The angles add to 360°, not the percents.)"))
    its.append(mcq("Ethan worked out the sector angles 160°, 110° and 80°. What is wrong?", "They add to 350°, not 360°",
                   ["They must add to 100°", "Nothing is wrong", "The biggest must be 180°"],
                   "160 + 110 + 80 = 350. The angles of a circle graph must add up to 360°, so one angle is wrong."))

    its.append(match_item(
        [("P", 180), ("T", 108), ("S", 72)], "P = pizza, T = tacos, S = sushi", "pizza, tacos and sushi",
        [[("P", 50), ("T", 30), ("S", 20)], [("P", 180), ("T", 72), ("S", 108)], [("P", 120), ("T", 120), ("S", 120)]],
        "Favourite lunch: pizza 50%, tacos 30%, sushi 20%. Which circle graph matches?",
        "Pizza 50% = 180° (half), tacos 30% = 108°, sushi 20% = 72°.",
        ["uses 50° for 50% and so on, so the sectors do not fill the circle.", "swaps tacos and sushi.",
         "makes every sector the same size."]))
    its.append(match_item(
        [("H", 180), ("S", 120), ("B", 60)], "H = hockey, S = soccer, B = basketball", "hockey, soccer and basketball",
        [[("H", 18), ("S", 12), ("B", 6)], [("H", 120), ("S", 180), ("B", 60)], [("H", 180), ("S", 60), ("B", 120)]],
        "36 students: hockey 18, soccer 12, basketball 6. Which circle graph matches?",
        "Each student is 360° ÷ 36 = 10°: hockey 180°, soccer 120°, basketball 60°.",
        ["uses 1° for each student, so the sectors do not fill the circle.", "swaps hockey and soccer.",
         "swaps soccer and basketball."]))
    its.append(match_item(
        [("W", 90), ("B", 90), ("C", 144), ("K", 36)], "W = walk, B = bus, C = car, K = bike", "walk, bus, car and bike",
        [[("W", 25), ("B", 25), ("C", 40), ("K", 10)], [("W", 144), ("B", 90), ("C", 90), ("K", 36)],
         [("W", 75), ("B", 75), ("C", 120), ("K", 30)]],
        "Walk 25%, bus 25%, car 40%, bike 10%. Which circle graph matches?",
        "Multiply by 3.6°: walk 90°, bus 90°, car 144°, bike 36°.",
        ["uses 25° for 25% and so on, so it fills only 100° of the circle.", "swaps walk and car.",
         "multiplies by 3 instead of 3.6, so a gap is left."]))
    its.append(match_item(
        [("D", 160), ("C", 120), ("F", 80)], "D = dog, C = cat, F = fish", "dog, cat and fish",
        [[("D", 120), ("C", 160), ("F", 80)], [("D", 20), ("C", 15), ("F", 10)], [("D", 180), ("C", 120), ("F", 60)]],
        "45 students: dog 20, cat 15, fish 10. Which circle graph matches?",
        "Each student is 360° ÷ 45 = 8°: dog 160°, cat 120°, fish 80°.",
        ["swaps dog and cat.", "uses 1° for each student, so the sectors do not fill the circle.",
         "makes dog half the circle, but 20 of 45 is less than half."]))
    its.append(match_item(
        [("S", 135), ("C", 105), ("O", 120)], "S = sleep, C = school, O = other", "sleep, school and other",
        [[("S", 9), ("C", 7), ("O", 8)], [("S", 90), ("C", 70), ("O", 80)], [("S", 120), ("C", 105), ("O", 135)]],
        "Maya’s day (24 hours): sleep 9 hours, school 7 hours, other 8 hours. Which circle graph matches?",
        "Each hour is 360° ÷ 24 = 15°: sleep 135°, school 105°, other 120°.",
        ["uses 1° for each hour, so the sectors do not fill the circle.",
         "uses 10° for each hour, so a gap is left.", "swaps sleep and other."]))
    return {"title": "Make a circle graph from a table", "items": its}


# ------------------------------------------------------------ set 3: choose the best graph
NOTITLE = pct_pie("", [("Soccer", 40), ("Hockey", 30), ("Basketball", 20), ("Other", 10)])


def set_choose():
    its = []
    its.append(mcq("Which graph is best to show what percent of Owen’s $200 savings goes to each goal?", "Circle graph",
                   ["Broken-line graph", "Histogram", "Line plot"],
                   "The goals are parts of one whole ($200). A circle graph shows parts of a whole."))
    its.append(mcq("Which graph is best to show the temperature in Thunder Bay every hour for one day?", "Broken-line graph",
                   ["Circle graph", "Histogram", "Pictograph"],
                   "Temperature changes over time. A broken-line graph shows it going up and down."))
    its.append(mcq("Which graph is best to show the heights of 30 students, grouped 140 to 150 cm, 150 to 160 cm and so on?",
                   "Histogram", ["Circle graph", "Double bar graph", "Broken-line graph"],
                   "Height is continuous data grouped in equal intervals. A histogram shows this, with bars that touch."))
    its.append(mcq("Which graph is best to compare the favourite sports of the boys and the girls in a class?",
                   "Double bar graph", ["Circle graph", "Histogram", "Broken-line graph"],
                   "There are two groups to compare in each category. A double (multiple) bar graph puts the two bars side by side."))
    its.append(mcq("Which graph is best to show how many students in each grade walk, bike or take the bus, and each grade’s total?",
                   "Stacked-bar graph", ["Circle graph", "Histogram", "Broken-line graph"],
                   "In a stacked-bar graph, each bar is one grade. The parts of the bar show walk, bike and bus, "
                   "and the whole bar shows the total."))
    its.append(mcq("Which graph is best to show the times of 50 runners in a 5 km race?", "Histogram",
                   ["Circle graph", "Pictograph", "Double bar graph"],
                   "Time is continuous data. Grouping the times in equal intervals (20 to 25 minutes, 25 to 30 minutes …) "
                   "and drawing a histogram shows how the times are spread."))
    its.append(mcq("Which data can NOT be shown well in a circle graph?", "Clubs students join (can join more than one)",
                   ["How a class gets to school", "How Leah spends her $50", "How Owen spends 24 hours"],
                   "If students can join more than one club, the percents add up to more than 100%. "
                   "A circle graph needs parts of one whole."))
    its.append(mcq("Why is a circle graph a poor choice to show the population of Ottawa each year from 2000 to 2025?",
                   "The data change over time", ["The numbers are too big", "Circle graphs show only 4 sectors",
                                                 "Ottawa is a city"],
                   "Each year’s population is not a part of one whole. A broken-line graph shows how it changes over time."))
    its.append(mcq("Liam made a circle graph of his puppy’s mass each month. Why is this a poor choice?",
                   "The masses are not parts of a whole", ["The puppy is too small", "Mass is measured in kg",
                                                          "There are 12 months"],
                   "Adding the masses from 12 months gives no useful whole. A broken-line graph shows how the mass changes."))
    its.append(mcq(fig(pie_svg(NOTITLE, label="circle graph with no title")) + "What is missing from this circle graph?",
                   "A title", ["Percent labels", "A key for the sectors", "A sector for 100%"],
                   "Every sector is labelled, and the percents add up to 100%. But there is no title, "
                   "so a reader cannot tell what the graph is about or who was asked."))
    its.append(mcq("Which list shows what every graph should have?", "A title, labels and a source",
                   ["Bright colours and pictures", "At least 5 categories", "A 3-D look"],
                   "A title says what the graph shows, labels name the categories and scale, and the source "
                   "says where the data came from."))
    its.append(mcq("Where should the source of the data go?", "Under the graph", ["Inside the biggest sector",
                                                                                 "On every bar", "It is not needed"],
                   "The source, such as “Survey of 7B students, October 2026”, usually goes under the graph. "
                   "It tells readers where the data came from and how much to trust it."))
    its.append(mcq("A bar graph will show values from 120 to 890. Which scale is best?", "0 to 900, going up by 100",
                   ["0 to 90, going up by 10", "100 to 900, going up by 100", "0 to 900, going up by 1"],
                   "The scale must start at 0 and go past the biggest value, 890. Steps of 100 give 10 easy grid lines. "
                   "(Going up by 1 needs 900 lines, and starting at 100 makes bars look wrong.)"))
    its.append(mcq("A bar graph shows visitors to 4 parks. The biggest value is 4 800 000. Which scale is best?",
                   "0 to 5 000 000, by 1 000 000", ["0 to 5000, by 1000", "4 000 000 to 5 000 000, by 100 000",
                                                    "0 to 4 800 000, by 1"],
                   "Start at 0 and go up to a round number above 4 800 000. Steps of 1 000 000 are easy to read. "
                   "(5000 is far too small, and starting at 4 000 000 is misleading.)"))
    its.append(mcq("Maya wants to show what part of her day she spends on each activity. She drew a broken-line graph. "
                   "Which graph is better, and why?", "Circle graph: parts of one day",
                   ["Histogram: time is continuous", "Line plot: there are few values", "Broken-line graph is best"],
                   "The activities are parts of one whole day (24 hours). A circle graph shows each part of the whole. "
                   "A broken-line graph is for change over time."))
    its.append(mcq("School A has 600 students and School B has 300. Which graph lets you compare the NUMBER of walkers "
                   "at each school?", "Double bar graph", ["Two circle graphs", "One circle graph", "A histogram"],
                   "Two circle graphs show percents, not numbers, so a bigger sector can mean fewer students. "
                   "A double bar graph shows the numbers side by side."))
    its.append(mcq("When is a circle graph a good choice?", "The parts make one whole",
                   ["The data change over time", "The data are grouped in intervals", "Each person can pick many answers"],
                   "A circle graph works when every piece of data belongs to exactly one part, "
                   "so the parts add to 100% (360°)."))
    its.append(mcq("Why should the heights of students be shown in a histogram, not a bar graph?", "Height is continuous data",
                   ["Height is counted", "Histograms are more colourful", "Bar graphs cannot show numbers"],
                   "Height is measured, so it can be any value. A histogram groups it in equal intervals with bars that touch."))
    its.append(mcq("Arjun surveyed 200 students about their favourite fruit. Each student chose one fruit. "
                   "He wants to show each fruit’s share of the total. Which graph?", "Circle graph",
                   ["Broken-line graph", "Histogram", "Stacked-bar graph"],
                   "Each student chose one fruit, so the fruits are parts of one whole (200 students = 100%). "
                   "A circle graph shows each share."))
    its.append(mcq("Which graph is best to show how many people visited the CN Tower each month of 2025?",
                   "Bar or broken-line graph", ["Circle graph", "Histogram", "Pictograph of the tower"],
                   "Monthly visits show change over time, so a bar graph or broken-line graph fits. "
                   "The months are not parts of a whole that people chose between."))
    return {"title": "Choose the best graph", "items": its}


# ------------------------------------------------------------ set 4: adding or removing data
def set_change():
    its = []
    g = [3, 5, 6, 8, 8]
    g2 = g + [0]
    assert mean(g) == 6 and median(g) == 6 and modes(g) == [8]
    assert mean(g2) == 5 and median(g2) == F(11, 2) and modes(g2) == [8]
    q0 = "Goals scored by a ringette team in 5 games: <b>%s</b>. In a 6th game the team scores 0 goals. " % lst(g)
    G = lambda x: unit(x, "goal", "goals")
    its.append(mcqv(q0 + "What is the new mean?", 5, [6, 30, F(11, 2)], G,
                    "The total is still 3 + 5 + 6 + 8 + 8 + 0 = 30, but now there are 6 games: 30 ÷ 6 = 5 goals. "
                    "(6 leaves out the 0, 30 is the total, and 5.5 is the new median.)"))
    its.append(mcqv(q0 + "What is the new median?", F(11, 2), [6, 5, 7], G,
                    "In order: 0, 3, 5, 6, 8, 8. The two middle values are 5 and 6: (5 + 6) ÷ 2 = 5.5 goals. "
                    "(6 is the old median, 5 is the new mean, and 7 uses 6 and 8.)"))
    its.append(mcq(q0 + "What is the new mode?", "8", ["0", "6", "There is no mode"],
                   "8 still appears twice, and every other value appears once. Adding 0 does not change the mode."))
    its.append(mcq("A value greater than the mean is added to a data set. What happens to the mean?", "It goes up",
                   ["It goes down", "It stays the same", "It doubles"],
                   "The new value is above the mean, so it pulls the mean up. For example, the mean of 2, 4, 6 is 4; "
                   "add 8 and it becomes 20 ÷ 4 = 5."))
    its.append(mcq("A value equal to the mean is added to a data set. What happens to the mean?", "It stays the same",
                   ["It goes up", "It goes down", "It becomes 0"],
                   "The new value is exactly at the mean, so it does not pull the mean either way. "
                   "The mean of 2, 4, 6 is 4; add 4 and it is 16 ÷ 4 = 4."))
    t = [12, 14, 15, 15, 16, 48]
    t2 = t[:-1]
    assert mean(t) == 20 and median(t) == 15 and mean(t2) == F(72, 5) and median(t2) == 15 and F(72, 6) == 12
    q1 = "Minutes 6 students took to get to school: <b>%s</b>. The 48 is removed. " % lst(t)
    Mi = lambda x: unit(x, "minute", "minutes")
    its.append(mcqv(q1 + "What is the new mean?", F(72, 5), [20, 12, 15], Mi,
                    "Without 48 the total is 12 + 14 + 15 + 15 + 16 = 72, and there are 5 values: 72 ÷ 5 = 14.4 minutes. "
                    "(20 is the old mean, 12 divides by 6, and 15 is the median.)"))
    its.append(mcq(q1 + "What happens to the median?", "It stays 15",
                   ["It drops to 14", "It drops to 12", "It rises to 16"],
                   "Before: 12, 14, 15, 15, 16, 48, so the median is (15 + 15) ÷ 2 = 15. "
                   "After: 12, 14, 15, 15, 16, so the median is the middle value, 15. It does not change."))
    its.append(mcq(q1 + "Which measure changed more when 48 was removed?", "The mean",
                   ["The median", "Both the same", "Neither changed"],
                   "The mean went from 20 to 14.4. The median stayed at 15. An outlier like 48 pulls the mean a lot, "
                   "but hardly moves the median."))
    tt = [-6, -3, 0, 2, 7]
    tt2 = tt + [-12]
    assert mean(tt) == 0 and mean(tt2) == -2 and median(tt2) == F(-3, 2)
    q2 = "Temperatures at 7 a.m. in Sudbury for 5 days (°C): <b>%s</b>. A 6th day is %s °C. " % (lst(tt), num(-12))
    T = lambda x: "%s °C" % num(x)
    its.append(mcqv(q2 + "What is the new mean?", -2, [2, F(-12, 5), -12], T,
                    "The first 5 add to 0. With the 6th day the total is −12, and there are 6 days: −12 ÷ 6 = −2 °C. "
                    "(2 forgets the minus sign, −2.4 divides by 5, and −12 is the new value, not the mean.)"))
    its.append(mcqv(q2 + "What is the new median?", F(-3, 2), [0, -3, F(3, 2)], T,
                    "In order: −12, −6, −3, 0, 2, 7. The two middle values are −3 and 0: (−3 + 0) ÷ 2 = −1.5 °C. "
                    "(0 is the old median, and 1.5 forgets the minus sign.)"))
    its.append(mcq("A value is removed from a data set and the mean goes up. What was true about the removed value?",
                   "It was less than the mean", ["It was greater than the mean", "It was equal to the mean",
                                                 "It was the median"],
                   "Taking away a small value removes something that was pulling the mean down, so the mean goes up."))
    m = [2, 3, 3, 5, 7, 7, 7]
    m2 = [2, 3, 3, 5, 7, 7]
    assert modes(m) == [7] and modes(m2) == [3, 7]
    its.append(mcq("Data: <b>%s</b>. One 7 is removed. What is the new mode?" % lst(m), "3 and 7",
                   ["7 only", "3 only", "There is no mode"],
                   "After removing one 7, the data are 2, 3, 3, 5, 7, 7. Now 3 and 7 each appear twice, so there are two modes."))
    k = [F("4.5"), F("5.2"), F("6.1"), F("4.8")]
    k2 = k + [F("5.9")]
    assert mean(k) == F("5.15") and mean(k2) == F("5.3") and sum(k2) / 4 == F("6.625")
    its.append(mcqv("Masses of 4 pumpkins (kg): <b>%s</b>. A 5th pumpkin of 5.9 kg is added. What is the new mean?" % lst(k),
                    F("5.3"), [F("5.15"), F("6.625"), F("5.9")], lambda x: "%s kg" % num(x),
                    "New total: 4.5 + 5.2 + 6.1 + 4.8 + 5.9 = 26.5. Divide by 5 pumpkins: 26.5 ÷ 5 = 5.3 kg. "
                    "(5.15 is the old mean, and 6.625 divides by 4.)"))
    d = [11, 13, 14, 18, 20]
    assert median(d) == 14 and median(d + [25]) == 16
    its.append(mcqv("Data: <b>%s</b>. The value 25 is added. What is the new median?" % lst(d), 16, [14, 18, 32], num,
                    "In order: 11, 13, 14, 18, 20, 25. Now there are 6 values, so the median is halfway between 14 and 18: "
                    "(14 + 18) ÷ 2 = 16. (32 forgets to divide by 2.)"))
    six = [6, 8, 10, 10, 12, 14]
    assert mean(six) == 10 and mean(six + [7, 13]) == 10
    its.append(mcq("Data: <b>%s</b> (mean 10). The values 7 and 13 are added. What happens to the mean?" % lst(six),
                   "It stays 10", ["It goes up", "It goes down", "It becomes 20"],
                   "7 and 13 have a mean of (7 + 13) ÷ 2 = 10, the same as the data. New total 60 + 20 = 80, and 80 ÷ 8 = 10."))
    assert (150 * 24 + 175) / F(25) == 151
    its.append(mcqv("The mean height of 24 students is 150 cm. A new student who is 175 cm tall joins the class. "
                    "What is the new mean height?", 151, [F(325, 2), 150, 175], lambda x: "%s cm" % num(x),
                    "Old total: 24 × 150 = 3600 cm. New total: 3600 + 175 = 3775 cm. 3775 ÷ 25 students = 151 cm. "
                    "(162.5 just averages 150 and 175, as if the class had 2 students.)"))
    its.append(mcq("Data: 4, 5, 5, 6, 7. The value 60 is added. Which measure best describes a typical value now?",
                   "The median", ["The mean", "The range", "The highest value"],
                   "60 is an outlier. It pulls the mean up to 87 ÷ 6 = 14.5, more than every other value. "
                   "The median, (5 + 6) ÷ 2 = 5.5, still sits among the usual values."))
    assert mean([4, 5, 5, 6, 7, 60]) == F(29, 2) and median([4, 5, 5, 6, 7, 60]) == F(11, 2)
    h = [2, 4, 3, 5, 1]
    assert mean(h) == 3 and F(7, 2) * 6 - sum(h) == 6
    its.append(mcqv("A hockey player scored <b>%s</b> goals in her first 5 games (mean 3). After the 6th game her mean is 3.5. "
                    "How many goals did she score in the 6th game?" % lst(h), 6, [F(7, 2), F(1, 2), 21], G,
                    "New total = 6 × 3.5 = 21. Old total = 15. 21 − 15 = 6 goals. "
                    "(3.5 is the new mean, 0.5 is how much the mean went up, and 21 is the new total.)"))
    assert 5 * 8 - 4 * 9 == 4
    its.append(mcqv("5 test scores have a mean of 8. One score is removed, and the mean of the other 4 is 9. "
                    "What was the removed score?", 4, [9, 8, 1], num,
                    "Total of 5 scores: 5 × 8 = 40. Total of the other 4: 4 × 9 = 36. Removed score: 40 − 36 = 4. "
                    "(1 is how much the mean changed.)"))
    assert 5 * 80 - 4 * 78 == 88
    its.append(mcqv("Zoe’s mean on 4 math tests is 78. What must she score on the 5th test to raise her mean to 80?", 88,
                    [80, 82, 2], num,
                    "She needs a total of 5 × 80 = 400. She has 4 × 78 = 312. 400 − 312 = 88. "
                    "(82 only adds 4 to 78; the 5th score must make up 2 points for each of 5 tests.)"))
    return {"title": "Add or remove data: mean, median and mode", "items": its}


# ------------------------------------------------------------ set 5: misleading graphs and conclusions
VOTE = (["Ottawa", "Niagara Falls"], [58, 52])
CANS_X = ["2022", "2023", "2024", "2025", "2026"]
CANS = [2500, 2525, 2575, 2650, 2750]


def vote_svg():
    return bar_svg("Votes for the Grade 7 field trip", "Place", "Votes", VOTE[0], VOTE[1], 50, 60, 1, 2, gy=14)


def cans_svg():
    return bline_svg("Cans collected for the food drive", "Year", "Cans", CANS_X, CANS, 2500, 2800, 25, 50,
                     gy=10, slot=58)


def set_claims():
    its = []
    f = fig(vote_svg())
    a, b = VOTE[1]
    assert (a - 50) == 4 * (b - 50)
    Vo = lambda x: unit(x, "vote", "votes")
    its.append(mcqv(f + "How many more votes did Ottawa get than Niagara Falls?", a - b, [a - 50, 4, b - 50], Vo,
                    "Ottawa 58, Niagara Falls 52. 58 − 52 = 6 votes. (8 and 2 are only the parts of the bars above 50, "
                    "and 4 is how many times taller the Ottawa bar looks.)"))
    its.append(mcq(f + "The Ottawa bar looks 4 times as tall. Did Ottawa get 4 times as many votes?",
                   "No: 58 is not 4 × 52", ["Yes: its bar is 4 times as tall", "Yes: 58 is more than 52",
                                            "No: Niagara Falls got more"],
                   "4 × 52 = 208, but Ottawa got 58 votes. The scale starts at 50, so we only see 8 and 2 of the votes."))
    its.append(mcqv(f + "To draw a fair bar graph of this data, where should the scale start?", 0, [50, 52, 58], num,
                    "Bar heights can be compared fairly only when the scale starts at 0. Then the bars are 58 and 52 high "
                    "and look almost the same."))
    f = fig(cans_svg())
    C = lambda x: unit(x, "can", "cans")
    its.append(mcqv(f + "How many more cans were collected in 2026 than in 2022?", 250, [2750, 100, 2500], C,
                    "2026: 2750. 2022: 2500. 2750 − 2500 = 250 cans. (2750 is the 2026 total, "
                    "and 100 is only the last year.)"))
    its.append(mcqv(f + "By what percent did the number of cans grow from 2022 to 2026?", 10, [250, 100, 25], pct,
                    "Growth = 250 cans. 250 ÷ 2500 = 0.1 = 10%. (250% reads the cans as a percent, 25% divides by 1000 instead of 2500, and 100% would mean doubling: the steep line makes it look "
                    "that way because the scale starts at 2500.)"))
    its.append(mcq(f + "A poster says, “Our food drive more than doubled!” Is this supported?",
                   "No: 2750 is less than 2 × 2500", ["Yes: the line rises steeply", "Yes: 2750 is more than 2500",
                                                      "No: the cans went down"],
                   "Doubling 2500 gives 5000. The school collected 2750, only 10% more. The scale starts at 2500, "
                   "so the line looks steeper than it is."))
    A = pct_pie("School A: 600 students", [("Walk", 20), ("Bus", 45), ("Car", 35)])
    B = pct_pie("School B: 300 students", [("Walk", 40), ("Bus", 30), ("Car", 30)])
    f = fig(pie_svg(A, B))
    assert F(20, 100) * 600 == F(40, 100) * 300 == 120
    its.append(mcq(f + "Which school has more students who walk?", "Both the same",
                   ["School B", "School A", "You cannot tell"],
                   "School A: 20% of 600 = 120. School B: 40% of 300 = 120. The Walk sector is twice as big at School B, "
                   "but School B has half as many students."))
    assert F(45, 100) * 600 - F(30, 100) * 300 == 180
    its.append(mcqv(f + "How many more students take the bus at School A than at School B?", 180, [15, 270, 90], stu,
                    "School A: 45% of 600 = 270. School B: 30% of 300 = 90. 270 − 90 = 180 students. "
                    "(15 is the difference in percent.)"))
    assert F(25, 100) * 1200 == 300
    its.append(mcq("A circle graph shows that 25% of the 1200 students at a school chose hockey. "
                   "A reporter writes, “25 students chose hockey.” What is wrong?", "25% of 1200 is 300 students",
                   ["Nothing: 25% means 25", "25% of 1200 is 48 students", "Hockey should be 90 students"],
                   "A percent is a part of the total. 25% of 1200 = 1200 ÷ 4 = 300 students. "
                   "(48 comes from 1200 ÷ 25.)"))
    assert F(35, 100) * 18000 == 6300
    its.append(mcqv("In a random survey of 400 students in a school board, 35% said they walk to school. "
                    "The board has 18 000 students. About how many of them walk?", 6300, [140, 63000, 11700], stu,
                    "Use the sample percent for the whole board: 35% of 18 000 = 0.35 × 18 000 = 6300 students. "
                    "(140 is 35% of the 400 in the sample, and 11 700 are the ones who do not walk.)"))
    assert F(42, 100) * 750000 == 315000 and F(42, 100) * 1500 == 630
    its.append(mcqv("A city has 750 000 adults. In a random survey of 1500 of them, 42% said they skate in winter. "
                    "About how many adults in the city skate?", 315000, [630, 31500, 435000], ppl,
                    "42% of 750 000 = 0.42 × 750 000 = 315 000 people. "
                    "(630 is 42% of the sample, 31 500 has the place value wrong, and 435 000 are the other 58%.)"))
    its.append(mcq("A survey at a ski hill found that 80% of the people asked love skiing more than any other sport. "
                   "A headline says, “80% of Canadians love skiing most!” What is the main problem?",
                   "People at a ski hill likely like skiing", ["80% is less than half", "Skiing is not a sport",
                                                               "The survey asked too many people"],
                   "The sample is biased: people at a ski hill are much more likely to love skiing. "
                   "The result is true only for the people asked."))
    its.append(mcq("A new app had 4 users in January and 8 in February. An ad says, “Users doubled in one month!” "
                   "Why could this mislead?", "The numbers are very small", ["8 is not double 4", "Apps have no users",
                                                                             "February is a short month"],
                   "8 is double 4, so the claim is true, but 4 more users is a tiny change. "
                   "Percents and “doubled” can sound big when the numbers are small."))
    its.append(mcq("A bar graph’s scale is labelled 0, 10, 20, 100, 500, with equal spaces between the labels. "
                   "Why is it misleading?", "Equal spaces show unequal amounts",
                   ["It starts at 0", "The numbers are too big", "It has 5 labels"],
                   "The space from 0 to 10 is the same as the space from 100 to 500, but one is 10 and the other is 400. "
                   "Bars on this scale cannot be compared fairly."))
    its.append(mcq("An ad shows sales doubling with two loon pictures. The second loon is twice as wide and twice as tall. "
                   "Why is this misleading?", "The big loon looks 4 times as big",
                   ["It should be 3 times as tall", "Loons are not data", "Sales did not change"],
                   "Doubling both the width and the height makes the area 2 × 2 = 4 times as big. "
                   "The eye sees the area, so sales look 4 times bigger instead of 2 times."))
    its.append(mcq("A newspaper circle graph of favourite summer activities says: camping 45%, swimming 35%, biking 30%. What is wrong?",
                   "The percents add to 110%", ["The percents must add to 360%", "There should be 4 sectors",
                                                "Nothing is wrong"],
                   "45 + 35 + 30 = 110. The sectors of a circle graph must add up to exactly 100%, "
                   "so the graph cannot be right."))
    w = [40000, 42000, 45000, 48000, 275000]
    assert mean(w) == 90000 and median(w) == 45000
    its.append(mcq("The yearly pay of 5 workers at a small company: %s. The owner says, “The mean pay here is $90 000.” "
                   "Which better describes a typical worker’s pay?" % ", ".join(dollars(x) for x in w),
                   "The median, $45 000", ["The mean, $90 000", "The range, $235 000", "The highest, $275 000"],
                   "The mean is $450 000 ÷ 5 = $90 000, but 4 of the 5 workers earn less than $50 000. "
                   "The $275 000 pulls the mean up. The median is the middle value, $45 000."))
    assert 9 * 2 < 28
    its.append(mcq("In a class of 28, pepperoni pizza got 9 votes, more than any other kind. "
                   "Nathan says, “Most of the class likes pepperoni best.” Is this supported?",
                   "No: 9 of 28 is less than half", ["Yes: pepperoni is the mode", "Yes: 9 is the most votes",
                                                     "No: pepperoni is not the mode"],
                   "Pepperoni is the mode, but “most” means more than half. Half of 28 is 14, and only 9 students chose pepperoni."))
    its.append(mcq("In July, both ice cream sales and sunburns go up. Priya says, “Ice cream causes sunburns.” "
                   "What is the best reply?", "Hot, sunny weather causes both",
                   ["She is right: the data show it", "Sunburns cause ice cream sales", "July has 31 days"],
                   "Two things can rise together without one causing the other. Hot, sunny weather makes people buy "
                   "ice cream and also causes sunburns."))
    its.append(mcq("Why is a tilted 3-D circle graph often misleading?", "Front sectors look bigger than they are",
                   ["It has too many colours", "Its percents add to 360%", "It has no sectors"],
                   "Tilting the circle stretches the sectors at the front and squashes the ones at the back, "
                   "so equal percents do not look equal."))
    return {"title": "Misleading graphs and conclusions", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    bd = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, bd)


LVOTE = (["Pizza", "Tacos"], [62, 54])


def body_html():
    p1 = pct_pie("How 80 students get to school", [("Walk", 45), ("Bus", 25), ("Car", 20), ("Bike", 10)])
    p2 = deg_pie("Favourite sport of 40 students", [("Hockey", 144), ("Soccer", 108), ("Basketball", 72),
                                                    ("Swimming", 36)])
    ld = [6, 7, 8, 9, 10]
    assert mean(ld) == 8 and median(ld) == 8 and mean(ld + [32]) == 12 and median(ld + [32]) == F(17, 2)
    assert (LVOTE[1][0] - 50) == 3 * (LVOTE[1][1] - 50)
    return (
        "<h2>A circle graph shows parts of a whole</h2>"
        "<p>A circle graph splits one whole into <b>sectors</b>. Each sector shows a <b>percent</b> of the total. "
        "The percents add up to <b>100%</b>, and the angles at the centre add up to <b>360°</b>.</p>"
        "<figure class='sn-fig'>" + pie_svg(p1) +
        "<figcaption>45% + 25% + 20% + 10% = 100%. The Bus sector is 25%, one-quarter of the circle.</figcaption></figure>" +
        ex("Example 1", "How many of the 80 students take the bus? What is the angle of the Bus sector?",
           "25%% = %s. 80 ÷ 4 = 20 students. Angle: 25%% × 360° = 0.25 × 360° = 90°." % frs(F(1, 4)),
           "20 students, 90°") +
        "<p>The same steps work for large populations: if 25% of a city of 840 000 people take transit, "
        "that is 0.25 × 840 000 = 210 000 people.</p>"
        "<h2>Make a circle graph from a table</h2>"
        "<p>1. Find the total. 2. Find each percent (count ÷ total). 3. Find each angle (percent × 360°, or "
        "360° ÷ total for each person). 4. Check: 100% and 360°. 5. Draw each angle with a protractor. "
        "Add a title, a label on each sector and the source of the data.</p>" +
        table(["Sport", "Students", "Percent", "Angle"], [
            ["Hockey", "16", "16 ÷ 40 = 40%", "40% × 360° = 144°"],
            ["Soccer", "12", "30%", "108°"],
            ["Basketball", "8", "20%", "72°"],
            ["Swimming", "4", "10%", "36°"],
            ["Total", "40", "100%", "360°"]]) +
        "<figure class='sn-fig'>" + pie_svg(p2) +
        "<figcaption>The table drawn as a circle graph. Each student is 360° ÷ 40 = 9°. "
        "Source: survey of Grade 7 students.</figcaption></figure>"
        "<h2>Choose the best graph</h2>" +
        table(["The data", "Best graph"], [
            ["Parts of one whole (budget, a day, one choice each)", "Circle graph"],
            ["Amounts in categories", "Bar graph"],
            ["Two groups in the same categories", "Double bar graph"],
            ["Parts and totals for several groups", "Stacked-bar graph"],
            ["Change over time", "Broken-line graph"],
            ["Measured data in equal intervals", "Histogram"],
        ]) +
        "<p>Every graph needs a title, labels, a scale that starts at 0 with equal steps, and a source.</p>"
        "<h2>Adding or removing data</h2>"
        "<p>A new value above the mean pulls the mean up; a value below pulls it down. An outlier changes the mean "
        "a lot but the median only a little.</p>" +
        ex("Example 2", "Data: 6, 7, 8, 9, 10. The value 32 is added. How do the mean and the median change?",
           "Old mean 40 ÷ 5 = 8, old median 8. New total 72, and 72 ÷ 6 = 12. "
           "New median (8 + 9) ÷ 2 = 8.5.", "The mean rises by 4, the median by only 0.5") +
        "<h2>Misleading graphs</h2>"
        "<p>Before you trust a graph, check: Does the scale start at 0? Are the steps equal? Do the percents add to 100%? "
        "Who was asked, and how many?</p>"
        "<figure class='sn-fig'>" + bar_svg("Favourite lunch", "Lunch", "Votes", LVOTE[0], LVOTE[1], 50, 66, 2, 4, gy=10) +
        "<figcaption>The scale starts at 50, so the pizza bar looks 3 times as tall. Really, pizza has only "
        "62 − 54 = 8 more votes.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Drawing 25% as 25°", "Multiply by 3.6: 25% × 360° = 90°"],
            ["Sectors that add up to 110% or 350°", "Check the totals: 100% and 360°"],
            ["Reading 25% as 25 people", "Find 25% of the total: 25% of 1200 = 300"],
            ["Dividing by the old count after adding a value", "Count the values again"],
            ["Saying a bigger sector always means more people", "Work out the numbers when the totals differ"],
            ["Judging bars by height when the scale does not start at 0", "Read the real values and subtract"],
        ])
    )


FAQ = [
    {"q": "How do you make a circle graph in Grade 7?",
     "a": "Find the total, change each count to a percent, then multiply each percent by 360° to get the sector angle. Check that the percents add to 100% and the angles add to 360°, then draw the angles with a protractor and add a title, labels and a source."},
    {"q": "Why is 25% not 25° in a circle graph?",
     "a": "The whole circle is 360°, not 100°. So 25% of the circle is 0.25 × 360° = 90°, a right angle."},
    {"q": "How does adding or removing a value change the mean and median?",
     "a": "A value above the mean raises the mean, and a value below it lowers the mean. An outlier changes the mean a lot but moves the median only a little."},
    {"q": "When should you use a circle graph instead of a bar graph?",
     "a": "Use a circle graph when the data are parts of one whole, such as how a budget or a day is split. Use a bar graph to compare amounts and a broken-line graph to show change over time."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5). A–D picture questions are built for their answer position."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        out = []
        for it, t in zip(s["items"], targets):
            if "_build" in it:
                out.append(it["_build"](t))
                continue
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
            out.append(it)
        s["items"] = out
        final = [sum(1 for it in out if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(47815)
    sets = [set_read(), set_make(), set_choose(), set_change(), set_claims()]
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
        "country": "ca-on", "subject": "math", "grade": "grade-7", "slug": "circle-graphs-and-data", "sort": 15,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 7 Circle Graphs and Data: Choosing Graphs, Mean and Median, Misleading Graphs",
        "seo_title": "Grade 7 Circle Graphs and Data Worksheets (Free, Answer Key, Ontario Curriculum)",
        "short_title": "Circle graphs and data",
        "domain": "Data",
        "standard_code": "Grade 7: D1.3",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Select from among a variety of graphs, including circle graphs, the type of graph best suited to represent various sets of data; display the data in the graphs with proper sources, titles, and labels, and appropriate scales; and justify their choice of graphs",
        "meta_desc": "Free Grade 7 math worksheets on circle graphs and data for the Ontario curriculum: read sectors in percents and degrees, make a circle graph from a table, choose the best graph, see how adding or removing data changes the mean and median, and spot misleading graphs. 100 questions with an answer key.",
        "key_big": "A circle graph shows parts of one whole: the percents add to 100% and the angles add to 360°.",
        "key_sub": "Sector angle = percent × 360°, so 25% is 90°, not 25°. An outlier moves the mean a lot but the median only a little. Check the scale before you trust a graph.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(circle graph|bar graph|broken-line)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
