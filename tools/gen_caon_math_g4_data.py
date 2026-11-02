# -*- coding: utf-8 -*-
"""
CA Grade 4 Math: Data and graphs (Ontario Curriculum 2020, Grade 4: Data, D1.1 to D1.6)
  python3 tools/gen_caon_math_g4_data.py
Qualitative and quantitative data, primary and secondary data, frequency tables, stem-and-leaf plots,
multiple-bar graphs (with a key, a scale and a source), the mean as a fair share, the median and the mode(s),
and drawing conclusions from data in Canadian contexts.
Wrong answers come from real student mistakes: the biggest value (or the frequency) as the mode, the median
taken without ordering, forgetting to halve the two middle values, the total instead of the mean, dividing by
the wrong count, reading the neighbouring bar, counting grid spaces instead of reading the scale, reading
6 | 2 as 26, and dropping repeated leaves.
Canadian English, Ontario number style. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, re, math, os, random
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
BAR = "#2e8b57"
BAR2 = "#e0a030"
FILL = "#cfe6d6"
FILL2 = "#e6f2ea"
INK = "#2b2b2b"
GRID = "#d5ddd8"
GRID2 = "#9fb0a5"
MUTE = "#555555"
FONT = "Arial, Helvetica, sans-serif"


# ------------------------------------------------------------ helpers
def num(x):
    x = F(x)
    assert x.denominator == 1 and 0 <= x < 10000, x
    return str(x.numerator)


def unit(v, one, many):
    return "%s %s" % (num(v), one if F(v) == 1 else many)


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def lst(v):
    return ", ".join(num(x) for x in v)


def median(v):
    s = sorted(F(x) for x in v)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def mean(v):
    return sum(F(x) for x in v) / len(v)


def modes(v):
    c = {}
    for x in v:
        c[x] = c.get(x, 0) + 1
    m = max(c.values())
    return sorted(k for k, n in c.items() if n == m) if m > 1 else []


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


def rect(x, y, w, h, fill, stroke="none", sw=1.5):
    return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s' stroke='%s' stroke-width='%s'/>"
            % (x, y, w, h, fill, stroke, sw))


# ------------------------------------------------------------ frequency table
def tally_marks(x, cy, v):
    s = []
    for g in range(v // 5):
        for k in range(4):
            s.append(line(x + k * 6, cy - 8, x + k * 6, cy + 8, INK, 2))
        s.append(line(x - 3, cy + 6, x + 21, cy - 6, INK, 2))
        x += 34
    for k in range(v % 5):
        s.append(line(x + k * 6, cy - 8, x + k * 6, cy + 8, INK, 2))
    return "".join(s)


def tally_width(v):
    return (v // 5) * 34 + (v % 5) * 6


def freq_svg(title, head, cats, vals):
    """Frequency table: category | tally | frequency."""
    fs, rh = 15, 28
    cols = [int(max(max(tw(c, fs) for c in cats), tw(head, fs, True)) + 20),
            int(max(max(tally_width(v) for v in vals) + 24, 70)),
            int(tw("Frequency", fs, True) + 20)]
    top = 28
    tot = sum(cols)
    W = int(max(tot + 8, tw(title, 16, True) + 16))
    x0 = (W - tot) / 2
    s = [text(W / 2, 19, title, 16, bold=True)]
    rows = [(head, None)] + list(zip(cats, vals))
    for r, (c, v) in enumerate(rows):
        y = top + r * rh
        hd = r == 0
        x = x0
        for k, cw in enumerate(cols):
            s.append(rect(x, y, cw, rh, FILL2 if hd or k == 0 else "#ffffff", GREEN))
            if k == 0:
                s.append(text(x + 10, y + 19, c, fs, anchor="start", bold=hd))
            elif hd:
                s.append(text(x + 10 if k == 1 else x + cw / 2, y + 19, "Tally" if k == 1 else "Frequency",
                              fs, anchor="start" if k == 1 else "middle", bold=True))
            elif k == 1:
                s.append(tally_marks(x + 14, y + rh / 2, v))
            else:
                s.append(text(x + cw / 2, y + 19, v, fs))
            x += cw
    H = top + len(rows) * rh + 4
    return svg_wrap(W, H, "".join(s), "frequency table: " + title.lower())


# ------------------------------------------------------------ stem-and-leaf plot
def stem_svg(title, data, key):
    """Stems are the tens, leaves are the ones, in order. Empty stems are shown."""
    fs, rh, lg = 15, 22, 19
    data = sorted(data)
    stems = list(range(data[0] // 10, data[-1] // 10 + 1))
    leaves = {st: [d % 10 for d in data if d // 10 == st] for st in stems}
    sx = 58
    mx = max(len(v) for v in leaves.values())
    W = int(max(sx + 14 + lg * mx + 12, tw(title, 16, True) + 16, tw(key, 14) + 16, sx + 80))
    s = [text(W / 2, 19, title, 16, bold=True)]
    hy = 46
    s.append(text(sx / 2 + 4, hy, "Stem", fs, bold=True))
    s.append(text(sx + 14, hy, "Leaves", fs, anchor="start", bold=True))
    s.append(line(8, hy + 7, W - 8, hy + 7, INK, 1.5))
    for i, st in enumerate(stems):
        y = hy + 7 + (i + 1) * rh - 6
        s.append(text(sx / 2 + 4, y, st, fs, bold=True))
        for j, lf in enumerate(leaves[st]):
            s.append(text(sx + 18 + j * lg, y, lf, fs))
    yb = hy + 7 + len(stems) * rh + 4
    s.append(line(sx, hy - 14, sx, yb, INK, 2))
    s.append(text(W / 2, yb + 22, key, 14, col=MUTE))
    return svg_wrap(W, yb + 30, "".join(s), "stem-and-leaf plot: " + title.lower())


# ------------------------------------------------------------ multiple-bar graph
def mbar_svg(title, cat_axis, val_axis, cats, series, names, ymax, gstep, lstep, gy=12, bw=22, source=None):
    fs = 14
    cols = [BAR, BAR2]
    assert ymax % lstep == 0 and lstep % gstep == 0
    for v in series:
        assert len(v) == len(cats) and all(0 <= x <= ymax for x in v)
    nt = ymax // gstep
    ph = nt * gy
    x0 = 24 + tw(num(ymax), fs) + 8
    slot = max(2 * bw + 28, max(tw(c, fs) for c in cats) + 12)
    pw = slot * len(cats)
    ws = [tw(n, fs) for n in names]
    ktot = sum(ws) + 2 * 22 + 24
    y0 = 58
    yb = y0 + ph
    W = max(x0 + pw + 8, tw(title, 16, True) + 16, ktot + 16)
    if source:
        W = max(W, tw(source, 13) + 16)
    s = [text(W / 2, 18, title, 16, bold=True)]
    kx = (W - ktot) / 2
    for i, n in enumerate(names):
        s.append(rect(kx, 31, 14, 14, cols[i], "none"))
        s.append(text(kx + 20, 43, n, fs, anchor="start"))
        kx += 22 + ws[i] + 24
    for k in range(nt + 1):
        v = k * gstep
        y = yb - k * gy
        major = v % lstep == 0
        s.append(line(x0, y, x0 + pw, y, GRID2 if major else GRID))
        if major:
            s.append(text(x0 - 5, y + 5, num(v), fs, anchor="end"))
    for i, c in enumerate(cats):
        cx = x0 + slot * i + slot / 2
        for j, ser in enumerate(series):
            h = F(ser[i], gstep) * gy
            bx = cx - bw + j * bw
            s.append(rect(bx, yb - float(h), bw, float(h), cols[j], "#ffffff", 1))
        s.append(text(cx, yb + 18, c, fs))
    s.append("<path d='M%.1f %d V%.1f H%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0 - 6, yb, x0 + pw, INK))
    s.append(text(x0 + pw / 2, yb + 38, cat_axis, fs, bold=True))
    mid = y0 + ph / 2
    assert tw(val_axis, fs, True) < ph + 30, (val_axis, ph)
    s.append(text(13, mid, val_axis, fs, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % mid))
    H = yb + 46
    if source:
        s.append(text(W / 2, H + 8, source, 13, col=MUTE))
        H += 16
    return svg_wrap(W, H, "".join(s), "multiple-bar graph: " + title.lower())


# ------------------------------------------------------------ cube towers (mean as a fair share)
def towers_svg(vals, names, mean_line=None):
    c, col = 16, 46
    mx = max(vals)
    top = 10
    yb = top + mx * c
    W = max(col * len(vals) + 16, 120)
    x0 = (W - col * len(vals)) / 2
    s = []
    for i, v in enumerate(vals):
        cx = x0 + col * i + col / 2
        for k in range(v):
            s.append(rect(cx - c / 2, yb - (k + 1) * c, c, c, FILL, GREEN, 1.5))
        s.append(text(cx, yb + 18, names[i], 14))
    s.append(line(x0 - 4, yb, x0 + col * len(vals) + 4, yb, INK, 2))
    if mean_line is not None:  # dashed line on top of the cubes
        y = yb - mean_line * c
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5' stroke-dasharray='5 4'/>"
                 % (x0 - 4, y, x0 + col * len(vals) + 4, y, BAR2))
    return svg_wrap(W, yb + 26, "".join(s), "cube towers: " + ", ".join(num(v) for v in vals))


# ------------------------------------------------------------ data
SL1 = [12, 15, 15, 15, 18, 21, 23, 26, 27, 30, 33, 36, 41, 45, 62]
SL2 = [38, 42, 45, 45, 45, 47, 51, 53, 56, 58, 60, 62, 64]
SL3 = [31, 35, 42, 48, 48]
MB_M = ["Oct", "Nov", "Dec", "Jan"]
MB_A = [28, 32, 12, 24]
MB_B = [20, 36, 24, 24]
WA = ["Hockey", "Skating", "Skiing", "Sledding"]
W4 = [12, 9, 5, 8]
W5 = [10, 6, 9, 11]
GO = (["Walk", "Bus", "Car", "Bike"], [9, 7, 6, 3])
SIB = (["0", "1", "2", "3", "4"], [4, 9, 6, 3, 1])
PZ = (["Pepperoni", "Cheese", "Veggie", "Hawaiian"], [9, 7, 6, 4])


def sl1_svg():
    return stem_svg("Minutes students read on Saturday", SL1, "Key: 1 | 2 means 12 minutes")


def sl2_svg():
    return stem_svg("Jumping jacks in 1 minute", SL2, "Key: 3 | 8 means 38 jumping jacks")


def mb1_svg():
    return mbar_svg("Books read by two Grade 4 classes", "Month", "Books", MB_M, [MB_A, MB_B], ["4A", "4B"], 40, 4, 4,
                    gy=15, source="Source: school library records")


def mb2_svg():
    return mbar_svg("Favourite winter activity", "Activity", "Students", WA, [W4, W5], ["Grade 4", "Grade 5"], 12, 1, 2,
                    gy=10, bw=20, source="Source: class surveys")


def go_svg():
    return freq_svg("How we get to school", "Way", GO[0], GO[1])


def sib_svg():
    return freq_svg("Number of brothers and sisters", "Siblings", SIB[0], SIB[1])


def pz_svg():
    return freq_svg("Favourite pizza in our class", "Pizza", PZ[0], PZ[1])


# ------------------------------------------------------------ set 1: qualitative or quantitative, frequency tables
QL, QN, BO, NE = "Qualitative", "Quantitative", "Both", "Neither"


def kind(q, right, e):
    return mcq("Is this data qualitative or quantitative?<br><b>%s</b>" % q, right,
               [k for k in (QL, QN, BO, NE) if k != right], e)


def set_kinds():
    its = [
        kind("Each student’s favourite colour", QL,
             "The answers are words, such as red or blue. Data in words or categories is qualitative."),
        kind("The number of brothers and sisters each student has", QN,
             "The answers are numbers you count: 0, 1, 2, 3 … Number data is quantitative."),
        kind("The height of each student in centimetres", QN,
             "Height is a number you measure, such as 136 cm. Number data is quantitative."),
        kind("Each student’s favourite hockey team", QL,
             "The answers are team names, not numbers, so the data is qualitative."),
        kind("How each student gets to school: walk, bus, car or bike", QL,
             "The answers are categories (walk, bus, car, bike), so the data is qualitative."),
        kind("The time each student takes to run one lap of the track, in seconds", QN,
             "Time is a number you measure, such as 75 seconds, so the data is quantitative."),
        kind("The kind of pet each student has", QL,
             "The answers are words such as dog, cat or fish, so the data is qualitative."),
        kind("The number of books each student read in March", QN,
             "The answers are numbers you count, so the data is quantitative."),
        kind("The temperature at recess each day, in °C", QN,
             "Temperature is a number you measure with a thermometer, so the data is quantitative."),
        kind("The month of each student’s birthday", QL,
             "The answers are month names (January, February …). They are categories, so the data is qualitative."),
        kind("The mass of each pumpkin at a Thanksgiving market, in kilograms", QN,
             "Mass is a number you measure on a scale, so the data is quantitative."),
        kind("The flavour of ice cream each student likes best", QL,
             "The answers are flavours such as chocolate or maple, so the data is qualitative."),
        kind("The number on each player’s hockey jersey", QL,
             "Jersey numbers only name the players, like labels. Adding them or finding their mean makes no sense, "
             "so they are qualitative, even though they look like numbers."),
        mcq("Which survey question gives <b>quantitative</b> data?", "How many pets do you have?",
            ["What is your favourite sport?", "What colour is your coat?", "Which pet would you like?"],
            "“How many pets?” is answered with a number, so it gives quantitative data. "
            "The other questions are answered with words."),
        mcq("Which survey question gives <b>qualitative</b> data?", "What is your favourite season?",
            ["How many cousins do you have?", "How tall are you?", "How many minutes do you read?"],
            "“What is your favourite season?” is answered with a word (winter, spring …), so it gives qualitative data. "
            "The other questions are answered with numbers."),
    ]
    S = lambda x: unit(x, "student", "students")
    c, v = GO
    f = fig(go_svg())
    assert sum(v) == 25
    its.append(mcqv(f + "How many students answered the survey?", sum(v), [len(v), max(v), sum(v) - v[3]], S,
                    "Add the frequencies: 9 + 7 + 6 + 3 = 25 students. (4 is the number of rows, 9 is only the biggest "
                    "row, and 22 leaves out Bike.)"))
    its.append(mcqv(f + "How many more students walk than take the bus?", v[0] - v[1], [v[0] + v[1], v[1], v[0]], S,
                    "Walk 9, bus 7. 9 − 7 = 2 more students. (16 adds the two rows.)"))
    c, v = SIB
    f = fig(sib_svg())
    assert sum(v) == 23
    its.append(mcqv(f + "What is the mode of this data?", 1, [9, 4, 2], lambda x: unit(x, "sibling", "siblings"),
                    "The most common answer is 1 sibling: 9 students gave it. The mode is the value, 1, not the frequency, 9. "
                    "(4 is the biggest value in the table.)"))
    its.append(mcqv(f + "How many students have 2 or more siblings?", v[2] + v[3] + v[4], [v[2], v[3] + v[4], sum(v[:3])], S,
                    "2 or more means the rows 2, 3 and 4: 6 + 3 + 1 = 10 students. "
                    "(6 is only the row for 2, and 19 counts 2 or fewer.)"))
    its.append(mcq(f + "Is this data qualitative or quantitative?", "Quantitative: the answers are numbers",
                   ["Qualitative: it is in a table", "Qualitative: it has tally marks", "Quantitative: it has a title"],
                   "Each student answered with a number (0, 1, 2, 3 or 4 siblings), so the data is quantitative. "
                   "A table or tally marks can show either kind of data."))
    return {"title": "Qualitative or quantitative data and frequency tables", "items": its}


# ------------------------------------------------------------ set 2: stem-and-leaf plots
def set_stem():
    its = []
    its.append(mcqv("In a stem-and-leaf plot, 3 | 7 means 37. What does 5 | 2 mean?", 52, [25, 7, 10], num,
                    "The stem is the tens digit and the leaf is the ones digit: 5 tens and 2 ones = 52. "
                    "(25 swaps the digits, and 7 adds them.)"))
    its.append(mcq("Which row of a stem-and-leaf plot shows 61, 64 and 68?", "6 | 1 4 8",
                   ["1 4 8 | 6", "6 | 61 64 68", "6 | 1 8"],
                   "All three numbers have 6 tens, so the stem is 6. The leaves are the ones digits: 1, 4 and 8. "
                   "(6 | 1 8 leaves out 64.)"))
    its.append(mcq("A row of a stem-and-leaf plot is <b>4 | 0 3 3 7</b>. Which values does it show?", "40, 43, 43, 47",
                   ["40, 43, 47", "4, 0, 3, 3, 7", "4, 7, 10, 14"],
                   "Each leaf makes one value with the stem 4: 40, 43, 43, 47. The leaf 3 is written twice, so 43 appears twice. "
                   "(40, 43, 47 drops the repeated leaf.)"))
    its.append(mcq("Where does the value 30 go in a stem-and-leaf plot?", "Stem 3, leaf 0",
                   ["Stem 0, leaf 3", "Stem 3, no leaf", "Stem 30, leaf 0"],
                   "30 is 3 tens and 0 ones, so it goes on stem 3 with a leaf of 0. Without the leaf 0, the value would be lost."))
    v = [23, 18, 27, 15, 21, 18]
    its.append(mcq("Data: %s. Which is the row for stem 1?" % lst(v), "1 | 5 8 8",
                   ["1 | 8 5 8", "1 | 5 8", "1 | 15 18 18"],
                   "The values with 1 ten are 18, 15 and 18. Their ones digits in order are 5, 8, 8. "
                   "(1 | 5 8 drops one 18, and 1 | 8 5 8 is not in order.)"))
    f = fig(sl1_svg())
    S = lambda x: unit(x, "student", "students")
    M = lambda x: unit(x, "minute", "minutes")
    assert len(SL1) == 15
    its.append(mcqv(f + "How many students are shown in this plot?", 15, [6, 5, 62], S,
                    "Each leaf is one student. Count the leaves: 5 + 4 + 3 + 2 + 0 + 1 = 15. "
                    "(6 counts the stems, 5 counts the rows that have leaves, and 62 is the largest value.)"))
    its.append(mcqv(f + "What is the longest time a student read?", 62, [45, 26, 6], M,
                    "The last row is 6 | 2, which means 62 minutes. (45 is the end of the row for 4, "
                    "and 26 reads the digits the wrong way round.)"))
    its.append(mcqv(f + "What is the shortest time a student read?", 12, [21, 2, 1], M,
                    "The first leaf on the first row: 1 | 2 means 12 minutes. (21 reads the digits the wrong way round.)"))
    its.append(mcqv(f + "How many students read for 50 to 59 minutes?", 0, [1, 5, 2], S,
                    "The row for stem 5 has no leaves, so 0 students read for 50 to 59 minutes. "
                    "(An empty row is not one student.)"))
    assert modes(SL1) == [15]
    its.append(mcqv(f + "What is the mode?", 15, [62, 5, 3], M,
                    "The leaf 5 appears three times on stem 1, so 15 appears most often. The mode is 15 minutes. "
                    "(62 is the largest value, and 3 is how many times 15 appears.)"))
    assert median(SL1) == 26
    its.append(mcqv(f + "What is the median?", 26, [37, 27, 15], M,
                    "The leaves are already in order. 15 values, so the median is the 8th: "
                    "12, 15, 15, 15, 18, 21, 23, <b>26</b>. "
                    "(37 is halfway between 12 and 62, which is not the median, and 27 is the 9th value.)"))
    assert len([x for x in SL1 if x >= 30]) == 6
    its.append(mcqv(f + "How many students read for 30 minutes or more?", 6, [5, 9, 3], S,
                    "30 or more: 30, 33, 36, 41, 45, 62. That is 6 students. "
                    "(5 forgets 30, and 9 counts the students under 30.)"))
    its.append(mcqv(f + "How many more students read for 10 to 19 minutes than for 40 to 49 minutes?", 3, [7, 5, 2], S,
                    "Row 1 has 5 leaves and row 4 has 2 leaves. 5 − 2 = 3 more students. (7 adds them.)"))
    f = fig(sl2_svg())
    J = lambda x: unit(x, "jumping jack", "jumping jacks")
    assert len(SL2) == 13 and median(SL2) == 51 and modes(SL2) == [45]
    its.append(mcqv(f + "What is the median?", 51, [47, 53, 45], J,
                    "There are 13 values, so the median is the 7th: 38, 42, 45, 45, 45, 47, <b>51</b>. "
                    "(47 is the 6th and 53 is the 8th value.)"))
    its.append(mcqv(f + "What is the mode?", 45, [64, 3, 5], J,
                    "45 appears three times (the leaf 5 three times on stem 4), more than any other value. "
                    "(64 is the largest value.)"))
    assert len([x for x in SL2 if x > 55]) == 5
    its.append(mcqv(f + "How many students did more than 55 jumping jacks?", 5, [3, 2, 7], S,
                    "More than 55: 56, 58, 60, 62, 64. That is 5 students. "
                    "(3 counts only the row for 6, and 7 counts everything from 50.)"))
    assert len([x for x in SL2 if x < 50]) == 6
    its.append(mcqv(f + "How many students did fewer than 50 jumping jacks?", 6, [5, 1, 2], S,
                    "Fewer than 50: the rows for 3 and 4. 1 + 5 = 6 students. (5 counts only the row for 4, "
                    "and 2 counts the rows, not the leaves.)"))
    its.append(mcq(f + "Mei did 48 jumping jacks. How does the row for 4 look after her value is added?",
                   "4 | 2 5 5 5 7 8", ["4 | 8 2 5 5 5 7", "4 | 2 5 7 8", "4 | 2 5 5 5 7 48"],
                   "48 has 4 tens and 8 ones, so the leaf 8 goes on stem 4, in order after 7. "
                   "(4 | 2 5 7 8 also loses the repeated 5s.)"))
    f = fig(stem_svg("Points scored in basketball games", SL3, "Key: 3 | 1 means 31 points"))
    its.append(mcq(f + "Which data set does this plot show?", "31, 35, 42, 48, 48",
                   ["13, 53, 24, 84, 84", "31, 35, 42, 48", "3, 1, 5, 4, 2, 8"],
                   "Stem 3 with leaves 1 and 5 gives 31 and 35. Stem 4 with leaves 2, 8, 8 gives 42, 48 and 48. "
                   "(13, 53 … read the digits the wrong way round, and 31, 35, 42, 48 drops the repeated 48.)"))
    its.append(mcq("Why are the leaves in a stem-and-leaf plot written in order from least to greatest?",
                   "The median and mode are easy to find", ["So the stems add up", "Leaves must be even numbers",
                                                            "It makes the values bigger"],
                   "When the leaves are in order, the whole data set is in order. You can count to the middle value for the median "
                   "and see repeated leaves for the mode."))
    return {"title": "Stem-and-leaf plots", "items": its}


# ------------------------------------------------------------ set 3: multiple-bar graphs
def set_mbar():
    its = []
    its.append(mcq("Which graph is best for comparing the favourite fruits of two classes?", "Multiple-bar graph",
                   ["Stem-and-leaf plot", "Line plot", "Tally marks only"],
                   "A multiple-bar graph puts a bar for each class side by side for each fruit, so the two classes are easy to compare. "
                   "A stem-and-leaf plot is for number data, not fruits."))
    its.append(mcq("What does the key on a multiple-bar graph tell you?", "Which colour is which group",
                   ["The total of all the bars", "What the scale counts by", "Where the data came from"],
                   "The key shows the colour for each group, such as green for 4A and orange for 4B. "
                   "The source tells where the data came from."))
    its.append(mcq("Which part of a graph tells where the data came from?", "The source",
                   ["The title", "The key", "The scale"],
                   "The source names where the data came from, such as “Source: class survey” or a website."))
    its.append(mcq("Which data is best shown in a stem-and-leaf plot?", "Test scores of 25 students",
                   ["Favourite colours of 25 students", "Votes from two classes", "Pets owned: dogs, cats, fish"],
                   "A stem-and-leaf plot shows number data, such as scores from 0 to 100. Colours, pets and votes for categories "
                   "are better in a bar graph."))
    f = fig(mb1_svg())
    B = lambda x: unit(x, "book", "books")
    its.append(mcqv(f + "How many books did 4B read in November?", 36, [32, 40, 9], B,
                    "Find the orange 4B bar for Nov. It reaches the line for 36. "
                    "(32 is the green 4A bar, and 9 counts the grid spaces instead of reading the scale, which counts by 4s.)"))
    its.append(mcq(f + "In which month did both classes read the same number of books?", "Jan", ["Nov", "Oct", "Dec"],
                   "In January both bars reach 24, so both classes read 24 books."))
    its.append(mcq(f + "In which month did 4A read more books than 4B?", "Oct", ["Nov", "Dec", "Jan"],
                   "Only in October is the green 4A bar taller: 28 books for 4A and 20 for 4B."))
    its.append(mcqv(f + "In December, how many more books did 4B read than 4A?", 12, [36, 24, 8], B,
                    "December: 4B read 24 and 4A read 12. 24 − 12 = 12 more books. (36 adds the bars, "
                    "and 8 is the difference in October.)"))
    assert sum(MB_A) == 96 and sum(MB_B) == 104
    its.append(mcqv(f + "How many books did 4A read in all four months?", 96, [104, 28, 32], B,
                    "Add the green bars: 28 + 32 + 12 + 24 = 96 books. (104 adds the orange 4B bars, "
                    "and 32 is only the tallest green bar.)"))
    its.append(mcqv(f + "What does the scale on this graph count by?", 4, [2, 1, 10], num,
                    "The numbers on the scale are 0, 4, 8, 12 … so each line is 4 more than the one below it."))
    f = fig(mb2_svg())
    S = lambda x: unit(x, "student", "students")
    its.append(mcqv(f + "How many Grade 5 students chose sledding?", 11, [8, 10, 12], S,
                    "Find the orange Grade 5 bar for sledding. It ends one line above 10, so it shows 11. "
                    "(8 is the green Grade 4 bar.)"))
    its.append(mcq(f + "Which activities got more votes from Grade 5 than from Grade 4?", "Skiing and sledding",
                   ["Hockey and skating", "Sledding only", "Skiing only"],
                   "Skiing: Grade 5 has 9 and Grade 4 has 5. Sledding: Grade 5 has 11 and Grade 4 has 8. "
                   "For hockey and skating, the Grade 4 bar is taller."))
    its.append(mcqv(f + "How many students chose skating in all?", 15, [9, 3, 6], S,
                    "Add both skating bars: 9 + 6 = 15 students. (3 is the difference between the bars.)"))
    its.append(mcqv(f + "How many more Grade 4 students than Grade 5 students chose hockey?", 2, [22, 12, 10], S,
                    "Hockey: Grade 4 has 12 and Grade 5 has 10. 12 − 10 = 2 more students. (22 adds the two bars.)"))
    its.append(mcq(f + "Which activity was the favourite in Grade 4?", "Hockey", ["Sledding", "Skiing", "Skating"],
                   "The tallest green bar is hockey, with 12 votes. (Sledding is the favourite in Grade 5.)"))
    assert sum(W4) == 34 and sum(W5) == 36
    its.append(mcqv(f + "How many Grade 4 students voted?", 34, [36, 70, 12], S,
                    "Add the green bars: 12 + 9 + 5 + 8 = 34. (36 adds the orange Grade 5 bars, and 70 adds both grades.)"))
    tot = [a + b for a, b in zip(W4, W5)]
    assert tot == [22, 15, 14, 19]
    its.append(mcq(f + "Which activity got the most votes from both grades together?", "Hockey: 22 votes",
                   ["Sledding: 19 votes", "Hockey: 12 votes", "Sledding: 11 votes"],
                   "Add the two bars for each activity: hockey 22, skating 15, skiing 14, sledding 19. Hockey has the most. "
                   "(12 and 11 are single bars.)"))
    d = [abs(a - b) for a, b in zip(W4, W5)]
    assert d == [2, 3, 4, 3]
    its.append(mcq(f + "For which activity is the difference between the two grades the greatest?", "Skiing",
                   ["Sledding", "Hockey", "Skating"],
                   "Differences: hockey 12 − 10 = 2, skating 9 − 6 = 3, skiing 9 − 5 = 4, sledding 11 − 8 = 3. "
                   "Skiing has the greatest difference, even though its bars are not the tallest."))
    its.append(mcq("Why use one multiple-bar graph instead of two separate bar graphs for two classes?",
                   "Side-by-side bars are easy to compare", ["It shows only one class", "It does not need a scale",
                                                             "It does not need a key"],
                   "In a multiple-bar graph the bars for both classes stand next to each other, so you can see at once which is taller. "
                   "It still needs a scale and a key."))
    its.append(mcq("Amira makes a multiple-bar graph of goals scored by two ringette teams in 5 games. What must her graph have?",
                   "Title, labels, scale, key and source",
                   ["Only a title and bars", "A key but no scale", "Stems and leaves"],
                   "Every graph needs a title, labels on the axes, a scale and a source. "
                   "A multiple-bar graph also needs a key to show which colour is which team."))
    return {"title": "Multiple-bar graphs", "items": its}


# ------------------------------------------------------------ set 4: mean, median and mode
def set_mmm():
    its = []
    v = [3, 6, 2, 4, 4, 5, 4, 1]
    assert modes(v) == [4] and v.count(4) == 3
    G = lambda x: unit(x, "goal", "goals")
    its.append(mcqv("Goals scored by a hockey team in 8 games:<br><b>%s</b><br>What is the mode?" % lst(v), 4, [6, 3, 8], G,
                    "The mode is the value that appears most often. 4 appears 3 times, so the mode is 4 goals. "
                    "(6 is the biggest value, 3 is how many times 4 appears, and 8 is the number of games.)"))
    v = [7, 9, 7, 8, 10, 9, 6]
    assert modes(v) == [7, 9]
    its.append(mcq("Laps skated by 7 students:<br><b>%s</b><br>What is the mode?" % lst(v), "7 and 9",
                   ["10", "9 only", "There is no mode"],
                   "7 appears twice and 9 appears twice. Every other value appears once. So there are two modes: 7 and 9. "
                   "(10 is the biggest value.)"))
    v = [12, 8, 15, 10, 9]
    assert modes(v) == [] and median(v) == 10
    its.append(mcq("Quiz scores out of 15:<br><b>%s</b><br>What is the mode?" % lst(v), "There is no mode",
                   ["15", "5", "10"],
                   "Each score appears only once, so no value appears most often. There is no mode. "
                   "(15 is the highest score, 5 is how many scores there are, and 10 is the median.)"))
    fr = ["apple", "banana", "apple", "orange", "grape", "apple", "banana"]
    assert modes(fr) == ["apple"]
    its.append(mcq("Favourite fruits of 7 students:<br><b>%s</b><br>What is the mode?" % ", ".join(fr), "Apple",
                   ["Banana", "3", "Grape"],
                   "Apple appears 3 times, more than any other fruit, so the mode is apple. "
                   "(3 is how many times it appears, not the mode.)"))
    v = [9, 4, 12, 7, 5]
    assert median(v) == 7
    its.append(mcqv("Minutes 5 students spent on homework:<br><b>%s</b><br>What is the median?" % lst(v), 7, [12, 8, 9],
                    lambda x: unit(x, "minute", "minutes"),
                    "Put the values in order first: 4, 5, 7, 9, 12. The middle value is 7. "
                    "(12 is the middle of the list before it was put in order, and 8 is halfway between 4 and 12.)"))
    v = [15, 22, 18, 30, 18, 25, 20]
    assert median(v) == 20
    its.append(mcqv("Ages of 7 people at a skating party:<br><b>%s</b><br>What is the median?" % lst(v), 20, [30, 18, 22],
                    lambda x: unit(x, "year", "years"),
                    "In order: 15, 18, 18, 20, 22, 25, 30. The middle (4th) value is 20. "
                    "(30 is the middle of the unordered list, and 18 is the mode.)"))
    v = [3, 11, 9, 5]
    assert median(v) == 7
    its.append(mcqv("Lengths swum by 4 students:<br><b>%s</b><br>What is the median?" % lst(v), 7, [10, 14, 5],
                    lambda x: unit(x, "length", "lengths"),
                    "In order: 3, 5, 9, 11. There are two middle values, 5 and 9. The median is halfway between them: "
                    "(5 + 9) ÷ 2 = 7. (10 uses 11 and 9 from the unordered list, and 14 forgets to divide by 2.)"))
    t = [3, 7, 5, 1, 4]
    assert mean(t) == 4
    f = fig(towers_svg(t, ["A", "B", "C", "D", "E"]))
    C = lambda x: unit(x, "cube", "cubes")
    its.append(mcqv(f + "Move cubes until all 5 towers are the same height. How tall is each tower? (This is the mean.)",
                    4, [20, 7, 5], C,
                    "There are 3 + 7 + 5 + 1 + 4 = 20 cubes. Shared fairly among 5 towers: 20 ÷ 5 = 4 cubes each. "
                    "(20 is the total, 7 is the tallest tower, and 5 is the number of towers.)"))
    t = [2, 8, 5]
    assert mean(t) == 5
    f = fig(towers_svg(t, ["A", "B", "C"]))
    its.append(mcqv(f + "What is the mean height of these towers?", 5, [15, 8, 3], C,
                    "Total: 2 + 8 + 5 = 15 cubes. Shared among 3 towers: 15 ÷ 3 = 5. "
                    "(15 is the total, 8 is the tallest tower, and 3 is the number of towers.)"))
    its.append(mcqv(f + "To make the towers even, how many cubes move from tower B to tower A?", 3, [6, 5, 2], C,
                    "The mean is 5. Tower B has 8, which is 3 too many. Tower A has 2, which is 3 too few. "
                    "Move 3 cubes from B to A: then A, B and C all have 5. (6 is the difference between B and A.)"))
    v = [2, 9, 5, 8]
    assert mean(v) == 6
    its.append(mcqv("Points scored by Priya in 4 basketball games:<br><b>%s</b><br>What is the mean?" % lst(v), 6,
                    [24, 8, 9], lambda x: unit(x, "point", "points"),
                    "Add: 2 + 9 + 5 + 8 = 24. There are 4 games: 24 ÷ 4 = 6 points. "
                    "(24 is the total, 8 divides by 3, and 9 is the highest score.)"))
    v = [0, 6, 3, 0, 6]
    assert mean(v) == 3
    its.append(mcqv("Centimetres of snow that fell each day for 5 days:<br><b>%s</b><br>What is the mean?" % lst(v), 3,
                    [5, 15, 6], lambda x: "%s cm" % num(x),
                    "Add: 0 + 6 + 3 + 0 + 6 = 15. There are 5 days, including the 2 days with 0 cm: 15 ÷ 5 = 3 cm. "
                    "(5 leaves out the zeros and divides by 3.)"))
    its.append(mcqv("Four friends picked 36 apples at an orchard. They share them equally. "
                    "How many apples does each friend get? (This is the mean.)", 9, [32, 40, 144],
                    lambda x: unit(x, "apple", "apples"),
                    "Share 36 equally among 4: 36 ÷ 4 = 9 apples each. (32 subtracts, 40 adds and 144 multiplies.)"))
    its.append(mcq("Which measure is the middle value when the data is in order?", "Median", ["Mean", "Mode", "Total"],
                   "The median is the middle value of the ordered data. The mode is the most common value, "
                   "and the mean is the fair share."))
    its.append(mcq("Students named their favourite colours. Which measure can you find for this data?", "The mode only",
                   ["The mean only", "The median only", "Mean, median and mode"],
                   "Colours are qualitative: you cannot add them or put them in number order. "
                   "You can only find the colour that appears most often, the mode."))
    its.append(mcq("Liam says the mode of 2, 3, 3, 9 is 9 because 9 is the biggest number. Who is right?",
                   "The mode is 3", ["Liam is right", "There is no mode", "The mode is 2"],
                   "The mode is the value that appears most often, not the biggest value. 3 appears twice, so the mode is 3. "
                   "(2 is how many times 3 appears.)"))
    assert median([8, 2, 5]) == 5
    its.append(mcq("Hana says the median of 8, 2, 5 is 2 because 2 is in the middle of the list. What is right?",
                   "Order first: the median is 5", ["Hana is right", "The median is 8", "There is no median"],
                   "Always put the values in order before you find the middle. In order: 2, 5, 8. The middle value is 5."))
    v = [19, 20, 14, 17, 20]
    assert mean(v) == 18 and median(v) == 19 and modes(v) == [20]
    its.append(mcqv("Ava’s spelling test scores out of 20:<br><b>%s</b><br>What is the mean?" % lst(v), 18, [90, 20, 19],
                    num,
                    "Add: 19 + 20 + 14 + 17 + 20 = 90. There are 5 tests: 90 ÷ 5 = 18. "
                    "(90 is the total, 20 is the mode, and 19 is the median.)"))
    assert 3 * 6 - 4 - 5 == 9
    its.append(mcqv("The mean of 3 numbers is 6. Two of the numbers are 4 and 5. What is the third number?", 9, [6, 15, 3],
                    num,
                    "A mean of 6 for 3 numbers means the total is 3 × 6 = 18. 4 + 5 = 9, and 18 − 9 = 9. "
                    "Check: (4 + 5 + 9) ÷ 3 = 6. (15 adds 6, 4 and 5, and 3 uses 2 × 6 = 12 instead of 18.)"))
    opts = [[3, 5, 5, 7], [5, 5, 6, 8], [1, 5, 9], [4, 5, 6, 6]]
    good = [o for o in opts if mean(o) == 5 and median(o) == 5 and modes(o) == [5]]
    assert good == [opts[0]]
    its.append(mcq("Which data set has a mean of 5, a median of 5 and a mode of 5?", lst(opts[0]),
                   [lst(o) for o in opts[1:]],
                   "3, 5, 5, 7: total 20, and 20 ÷ 4 = 5. Middle values 5 and 5, so the median is 5. 5 appears twice, so the mode is 5. "
                   "(5, 5, 6, 8 has a mean of 6, 1, 5, 9 has no mode, and 4, 5, 6, 6 has a mode of 6.)"))
    return {"title": "Mean (fair share), median and mode", "items": its}


# ------------------------------------------------------------ set 5: conclusions
def set_concl():
    its = []
    its.append(mcq("Noah asks everyone in his class how they get to school. What kind of data does he collect?",
                   "Primary: he collected it himself", ["Secondary: someone else collected it",
                                                        "Secondary: it is about school", "Primary: it is on a website"],
                   "Data you collect yourself, with a survey or by measuring, is primary data."))
    its.append(mcq("Maya finds the number of visitors to Algonquin Park last summer on a government website. "
                   "What kind of data is this?", "Secondary: someone else collected it",
                   ["Primary: she collected it herself", "Primary: it is about a park", "Secondary: it is qualitative"],
                   "Maya did not count the visitors herself. Data that someone else collected is secondary data."))
    cans = [("Liam", 14), ("Zoe", 9), ("Arjun", 12), ("Mei", 6), ("Owen", 9)]
    v = [b for _, b in cans]
    assert mean(v) == 10 and median(v) == 9 and modes(v) == [9]
    q0 = ("Cans collected for the food drive: %s.<br>" % ", ".join("%s %d" % c for c in cans))
    its.append(mcqv(q0 + "What is the mean number of cans?", 10, [50, 9, 14], lambda x: unit(x, "can", "cans"),
                    "Add: 14 + 9 + 12 + 6 + 9 = 50. There are 5 students: 50 ÷ 5 = 10 cans. "
                    "(50 is the total, 9 is the median and the mode, and 14 is the most.)"))
    its.append(mcq(q0 + "Who collected more cans than the mean?", "Liam and Arjun",
                   ["Only Liam", "Zoe and Owen", "Liam, Arjun, Zoe and Owen"],
                   "The mean is 50 ÷ 5 = 10. Liam (14) and Arjun (12) collected more than 10. "
                   "Zoe and Owen collected 9, which is less."))
    w = [8, 10, 9, 11, 42]
    assert median(w) == 10 and mean(w) == 16
    its.append(mcq("Minutes 5 friends take to walk to school: %s. Which number best describes a typical time?" % lst(w),
                   "The median, 10 minutes", ["The mean, 16 minutes", "The total, 80 minutes", "The longest, 42 minutes"],
                   "42 is far from the other times. It pulls the mean up to 80 ÷ 5 = 16, which is more than 4 of the 5 times. "
                   "The median, 10, is in the middle of the usual times."))
    f = fig(pz_svg())
    assert sum(PZ[1]) == 26 and PZ[1][0] * 2 < 26
    its.append(mcq(f + "Liam says, “Most of the class chose pepperoni.” Is this supported?", "No: 9 of 26 is less than half",
                   ["Yes: pepperoni is the mode", "Yes: 9 is the most votes", "No: cheese got more votes"],
                   "Pepperoni is the mode, but “most” means more than half. There are 9 + 7 + 6 + 4 = 26 votes. "
                   "Half of 26 is 13, and only 9 chose pepperoni."))
    its.append(mcq(f + "The class can order two kinds of pizza for a party. Which two should they choose?",
                   "Pepperoni and cheese", ["Pepperoni and Hawaiian", "Veggie and Hawaiian", "Cheese and veggie"],
                   "Choose the two kinds with the most votes: pepperoni (9) and cheese (7)."))
    f = fig(mb1_svg())
    its.append(mcq(f + "4A says, “We read more books than 4B every month.” Is this true?",
                   "No: 4B read more in Nov and Dec", ["Yes: 4A read 28 in October", "Yes: 4A has green bars",
                                                       "No: 4B read more every month"],
                   "4A read more only in October. In November and December the orange 4B bars are taller, "
                   "and in January the classes read the same."))
    f = fig(mb2_svg())
    its.append(mcq(f + "Owen thinks most Grade 4 students like skating best. Does the data support his idea?",
                   "No: hockey got more Grade 4 votes", ["Yes: skating has 9 votes", "Yes: skating is popular in Grade 5",
                                                         "No: skiing got the most votes"],
                   "In Grade 4, hockey got 12 votes and skating got 9. The data shows his idea is not right."))
    its.append(mcq(f + "Which conclusion is supported by the graph?", "More Grade 5 students chose sledding than hockey",
                   ["More Grade 4 students than Grade 5 students chose skiing", "Nobody in Grade 5 chose skating",
                    "Grade 4 students like skiing best"],
                   "Grade 5: sledding 11, hockey 10, so sledding has more. Grade 4 chose skiing only 5 times (Grade 5: 9), "
                   "6 Grade 5 students chose skating, and Grade 4 liked hockey best."))
    its.append(mcq("To find the favourite sport of all Grade 4 students, Kai asks only the players on his hockey team. "
                   "What is the problem?", "His team probably likes hockey best",
                   ["He asked too many people", "Hockey is not a sport", "He should ask adults"],
                   "Players on a hockey team are likely to choose hockey. To be fair, Kai should ask students from all "
                   "Grade 4 classes."))
    its.append(mcq("Ava asks 3 friends if they like broccoli. All 3 say yes. She says, “Everyone in our school likes broccoli.” "
                   "Why is this a weak conclusion?", "3 people are too few to ask",
                   ["3 out of 3 is less than half", "Broccoli is a vegetable", "She should ask only 1 friend"],
                   "3 friends cannot speak for a whole school. A different group could give a very different answer."))
    v = [12, 15, 9, 15, 14]
    assert mean(v) == 13 and median(v) == 14 and modes(v) == [15]
    its.append(mcqv("Litres of maple syrup a sugar bush made each week in spring: %s. What is the mean?" % lst(v), 13,
                    [65, 15, 14], lambda x: "%s L" % num(x),
                    "Add: 12 + 15 + 9 + 15 + 14 = 65. There are 5 weeks: 65 ÷ 5 = 13 L. "
                    "(65 is the total, 15 is the mode, and 14 is the median.)"))
    assert mean([7, 11, 9]) == 9
    its.append(mcqv("Three friends picked 7, 11 and 9 baskets of apples. They share all the baskets equally. "
                    "How many baskets does each friend get?", 9, [27, 11, 4], lambda x: unit(x, "basket", "baskets"),
                    "Total: 7 + 11 + 9 = 27 baskets. Shared among 3: 27 ÷ 3 = 9 baskets each. This fair share is the mean. "
                    "(27 is the total, and 4 is 11 − 7.)"))
    sk = [4, 5, 5, 6, 3, 5, 7, 4, 5]
    assert modes(sk) == [5]
    its.append(mcq("Sizes of skates rented at a rink one Saturday: %s. Which size should the rink keep the most of?" % lst(sk),
                   "Size 5: the mode", ["Size 7: the largest", "Size 3: the smallest", "Size 4: it appears twice"],
                   "Size 5 was rented 4 times, more than any other size. The mode tells the rink which size is needed most."))
    f = fig(sl2_svg())
    n50 = len([x for x in SL2 if x >= 50])
    assert n50 == 7 and 2 * n50 > len(SL2)
    its.append(mcq(f + "The coach says, “More than half of the students did 50 or more jumping jacks.” Is this supported?",
                   "Yes: 7 of the 13 did", ["No: only 3 did", "No: 6 of the 13 did", "Yes: all of them did"],
                   "50 or more: the rows for 5 and 6. 4 + 3 = 7 students. Half of 13 is 6 and a half, and 7 is more, "
                   "so the claim is supported. (3 counts only the row for 6.)"))
    A_, B_ = [3, 5, 2, 6], [4, 4, 5, 3]
    assert mean(A_) == mean(B_) == 4
    its.append(mcq("Goals scored by two ringette teams in 4 games:<br><b>Lightning: %s</b><br><b>Storm: %s</b><br>"
                   "Which statement is true?" % (lst(A_), lst(B_)), "Both teams have a mean of 4 goals",
                   ["The Lightning have the higher mean", "The Storm have the higher mean", "The Lightning scored more goals in all"],
                   "Lightning: 3 + 5 + 2 + 6 = 16, and 16 ÷ 4 = 4. Storm: 4 + 4 + 5 + 3 = 16, and 16 ÷ 4 = 4. "
                   "One big game (6 goals) does not give the Lightning a higher mean."))
    h = [166, 148, 172, 160]
    assert median(h) == 163
    its.append(mcqv("Heights of 4 sunflowers in a school garden (cm): %s. What is the median height?" % lst(h), 163,
                    [160, 326, 166], lambda x: "%s cm" % num(x),
                    "In order: 148, 160, 166, 172. The two middle values are 160 and 166: (160 + 166) ÷ 2 = 326 ÷ 2 = 163 cm. "
                    "(160 is halfway between 148 and 172 from the unordered list, and 326 forgets to divide by 2.)"))
    sl = [9, 10, 9, 8, 9, 10, 8]
    assert mean(sl) == 9 and median(sl) == 9 and modes(sl) == [9]
    its.append(mcq("Hours Kai slept each night for a week: %s. Which statement is true?" % lst(sl),
                   "Mean, median and mode are all 9", ["The mode is 10", "The median is 8", "The mean is 63"],
                   "Mean: 63 ÷ 7 = 9. In order: 8, 8, 9, 9, 9, 10, 10, so the median is 9. 9 appears 3 times, so the mode is 9. "
                   "(63 is the total, not the mean.)"))
    its.append(mcq("The 4 Grade 4 classes raised $480 for the Terry Fox Run. What is the mean amount raised per class?",
                   "$120", ["$476", "$484", "$1920"],
                   "Share $480 equally among 4 classes: 480 ÷ 4 = 120, so $120 per class. "
                   "($476 subtracts 4, $484 adds 4, and $1920 multiplies by 4.)"))
    return {"title": "Draw conclusions from data", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


LSL = [24, 27, 31, 35, 35, 38, 42, 46, 53]
LT = [2, 6, 4]
LMB = (["Apples", "Grapes", "Pears"], [8, 5, 3], [6, 7, 2])


def body_html():
    assert median(LSL) == 35 and modes(LSL) == [35]
    assert mean(LT) == 4
    return (
        "<h2>Qualitative and quantitative data</h2>"
        "<p><b>Qualitative</b> data is words or categories, such as favourite colours or ways to get to school. "
        "<b>Quantitative</b> data is numbers you count or measure, such as the number of pets or a height in centimetres. "
        "Data you collect yourself is <b>primary</b> data. Data someone else collected, such as on a website, is <b>secondary</b> data.</p>" +
        table(["Kind of data", "Examples", "Good ways to show it"], [
            ["Qualitative", "Favourite sport, kind of pet, month of birthday", "Frequency table, bar graph, multiple-bar graph"],
            ["Quantitative", "Number of siblings, height, minutes of reading", "Frequency table, stem-and-leaf plot"],
        ]) +
        "<h2>Stem-and-leaf plots</h2>"
        "<p>A <b>stem-and-leaf plot</b> shows every number in a data set. The <b>stem</b> is the tens digit. "
        "The <b>leaf</b> is the ones digit. The leaves are written in order, so the data is already sorted.</p>"
        "<figure class='sn-fig'>" + stem_svg("Laps run by Grade 4 students", LSL, "Key: 2 | 4 means 24 laps") +
        "<figcaption>The row 3 | 1 5 5 8 shows 31, 35, 35 and 38. The row for 5 has one leaf: 53.</figcaption></figure>" +
        ex("Example 1", "What are the median and the mode?",
           "There are 9 leaves, so the median is the 5th value: 24, 27, 31, 35, <b>35</b>. The leaf 5 appears twice on stem 3, "
           "so 35 is also the mode.", "Median 35 laps, mode 35 laps") +
        "<h2>Multiple-bar graphs</h2>"
        "<p>A <b>multiple-bar graph</b> puts bars for two or more groups side by side, so you can compare them. "
        "The <b>key</b> shows which colour is which group. Like every graph, it needs a title, labels, a scale and a source.</p>"
        "<figure class='sn-fig'>" + mbar_svg("Favourite fruit", "Fruit", "Students", LMB[0], [LMB[1], LMB[2]],
                                             ["4A", "4B"], 8, 1, 2, gy=13, bw=22, source="Source: class surveys") +
        "<figcaption>For grapes, the orange 4B bar (7) is taller than the green 4A bar (5).</figcaption></figure>" +
        ex("Example 2", "How many students chose apples in all?", "4A: 8. 4B: 6. 8 + 6 = 14.", "14 students") +
        "<h2>Mean, median and mode</h2>" +
        table(["Measure", "How to find it", "What it tells you"], [
            ["Mean", "Add all the values, then divide by how many there are", "The fair share: what each would get if shared equally"],
            ["Median", "Put the values in order and take the middle one", "The middle of the data"],
            ["Mode", "The value that appears most often (there can be two, or none)", "The most common value"],
        ]) +
        "<p>Think of the <b>mean</b> as levelling towers of cubes. Move cubes from tall towers to short towers "
        "until all the towers are the same height.</p>"
        "<figure class='sn-fig'>" + towers_svg(LT, ["A", "B", "C"], mean_line=4) +
        "<figcaption>2 + 6 + 4 = 12 cubes. Shared among 3 towers, each gets 4. Move 2 cubes from B to A.</figcaption></figure>" +
        "<p>With an even number of values, the median is halfway between the two middle values: "
        "for 3, 5, 9, 11 it is (5 + 9) ÷ 2 = 7.</p>" +
        ex("Example 3", "Goals in 5 games: 4, 1, 3, 1, 6. Find the mean, the median and the mode.",
           "Mean: 4 + 1 + 3 + 1 + 6 = 15, and 15 ÷ 5 = 3. Median: in order 1, 1, 3, 4, 6, so the middle is 3. "
           "Mode: 1 appears twice.", "Mean 3, median 3, mode 1") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Finding the median without putting the values in order", "Order the values first, then take the middle"],
            ["Giving the biggest number as the mode", "The mode is the value that appears most often"],
            ["Giving the frequency (how many times) as the mode", "The mode is the value itself, not its count"],
            ["Giving the total as the mean", "Divide the total by how many values there are"],
            ["Reading 6 | 2 as 26", "The stem is the tens: 6 | 2 means 62"],
            ["Reading the other group’s bar", "Check the key for the right colour"],
        ])
    )


FAQ = [
    {"q": "What do Grade 4 students learn about data in the Ontario math curriculum?",
     "a": "Grade 4 students tell qualitative from quantitative data, organize data in frequency tables and stem-and-leaf plots, read and make multiple-bar graphs, find the mean, median and mode, and draw conclusions from data."},
    {"q": "How do you explain the mean to a Grade 4 student?",
     "a": "The mean is a fair share. Add all the values, then share the total equally: for 2, 6 and 4, the total is 12, and 12 ÷ 3 = 4."},
    {"q": "How do you read a stem-and-leaf plot?",
     "a": "The stem is the tens digit and each leaf is a ones digit, so 4 | 2 7 means 42 and 47. Each leaf is one piece of data."},
    {"q": "What is the difference between qualitative and quantitative data?",
     "a": "Qualitative data is words or categories, such as favourite colours. Quantitative data is numbers you count or measure, such as the number of pets or a height."},
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
    rnd = random.Random(44811)
    sets = [set_kinds(), set_stem(), set_mbar(), set_mmm(), set_concl()]
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
        "country": "ca-on", "subject": "math", "grade": "grade-4", "slug": "data-and-graphs", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Data and Graphs: Stem-and-Leaf Plots, Multiple-Bar Graphs, Mean, Median and Mode",
        "seo_title": "Grade 4 Data and Graphs Worksheets: Stem-and-Leaf Plots, Mean, Median, Mode (Free, Answer Key, Ontario)",
        "short_title": "Data and graphs",
        "domain": "Data",
        "standard_code": "Grade 4: D1.5",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Determine the mean and the median and identify the mode(s), if any, for various data sets involving whole numbers, and explain what each of these measures indicates about the data",
        "meta_desc": "Free Grade 4 math worksheets on data and graphs for the Ontario curriculum: qualitative and quantitative data, frequency tables, stem-and-leaf plots, multiple-bar graphs, the mean as a fair share, the median and the mode, and drawing conclusions. 100 questions with an answer key.",
        "key_big": "Put the data in order first. The median is the middle value, the mode is the most common value, and the mean is a fair share.",
        "key_sub": "Mean = total ÷ number of values. The mode is the value that appears most often, not the biggest number. In a stem-and-leaf plot, 3 | 4 means 34.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (graphs, tables, plots) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "(multiple-bar graph|frequency table|stem-and-leaf)")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
