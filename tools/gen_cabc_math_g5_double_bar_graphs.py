# -*- coding: utf-8 -*-
"""
CA-BC Grade 5 Math: Double bar graphs
(BC Mathematics Curriculum, Grade 5, Data and probability:
 one-to-one correspondence and many-to-one correspondence, using double bar graphs)
  python3 tools/gen_cabc_math_g5_double_bar_graphs.py
Reading double bar graphs with a legend, scales of 1, 2, 5 and 10 (one grid line stands for 1 or for many),
comparing two groups, making a double bar graph from a table, and drawing conclusions in BC contexts.
Wrong answers come from real student mistakes: reading the other bar in the pair, counting grid lines
instead of reading the scale, reading the labelled step instead of the grid step, rounding a bar that ends
halfway between two lines, adding when the question asks for a difference, and choosing a scale that is
too short or too coarse.
Canadian English, BC number style (5 or more digits use a no-break space). HTML attributes use single quotes.
"""
import json, re, math, os, random
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
BAR = "#2e8b57"
BAR2 = "#e0a030"
INK = "#2b2b2b"
GRID = "#d5ddd8"
GRID2 = "#9fb0a5"
MUTE = "#555555"
FONT = "Arial, Helvetica, sans-serif"
NB = " "


# ------------------------------------------------------------ helpers
def num(x):
    x = F(x)
    assert x.denominator == 1 and 0 <= x < 1000000, x
    s = str(x.numerator)
    if len(s) >= 5:
        g = []
        while s:
            g.insert(0, s[-3:])
            s = s[:-3]
        s = NB.join(g)
    return s


def unit(v, one, many):
    return "%s %s" % (num(v), one if F(v) == 1 else many)


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


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


S = lambda x: unit(x, "student", "students")
D = lambda x: "$" + num(x)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
    assert "'" not in label
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


# ------------------------------------------------------------ double bar graph
def dbar_svg(title, cat_axis, val_axis, cats, series, names, ymax, gstep, lstep, gy=12, bw=22, source=None):
    """Two bars per category (green = first group, orange = second group), legend at the top.
    gstep = value of one grid line, lstep = labelled step. A value None leaves the bar out."""
    fs = 14
    cols = [BAR, BAR2]
    assert ymax % lstep == 0 and lstep % gstep == 0 and len(series) == 2
    for v in series:
        assert len(v) == len(cats) and all(x is None or 0 <= x <= ymax for x in v)
    nt = ymax // gstep
    ph = nt * gy
    x0 = 24 + tw(num(ymax), fs) + 8
    slot = max(2 * bw + 28, max(tw(c, fs) for c in cats) + 14)
    pw = slot * len(cats)
    ws = [tw(n, fs) for n in names]
    ktot = sum(ws) + 2 * 22 + 24
    y0 = 58
    yb = y0 + ph
    W = max(x0 + pw + 8, tw(title, 16, True) + 16, ktot + 16)
    if source:
        W = max(W, tw(source, 14) + 16)
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
            if ser[i] is None or ser[i] == 0:
                continue
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
        s.append(text(W / 2, H + 8, source, 14, col=MUTE))
        H += 16
    return svg_wrap(W, H, "".join(s), "double bar graph: " + title.lower())


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (cls, h, b)


# ------------------------------------------------------------ data
# Pets (scale 1: one-to-one)
PC = ["Dog", "Cat", "Fish", "No pet"]
PA = [8, 5, 2, 9]
PB = [6, 7, 4, 6]
# Books (scale 2)
BC_ = ["Sep", "Oct", "Nov", "Dec"]
BA = [14, 18, 11, 16]
BB = [12, 20, 16, 16]
# Winter sport (grid 5, labels 10)
WC = ["Skiing", "Snowboarding", "Skating", "Hockey"]
W5 = [25, 30, 15, 20]
W6 = [20, 35, 10, 30]
# Food bank cans (grid 10, labels 20)
CC = ["Week 1", "Week 2", "Week 3", "Week 4"]
C25 = [40, 70, 90, 60]
C26 = [60, 50, 110, 80]
# Getting to school (scale 2)
HC = ["Walk", "Bike", "Bus", "Car"]
HF = [12, 4, 8, 10]
HS = [14, 10, 6, 4]
# Terry Fox Run (grid 10, labels 20)
TC = ["5A", "5B", "5C", "5D"]
T25 = [120, 90, 150, 110]
T26 = [140, 100, 130, 150]
# Salmon (grid 5, labels 10)
EC = ["Week 1", "Week 2", "Week 3", "Week 4"]
E25 = [15, 35, 40, 20]
E26 = [10, 25, 45, 30]
# Library table (set 4)
LC = ["Fiction", "Non-fiction", "Comics", "Poetry"]
L4 = [35, 20, 45, 10]
L5 = [40, 30, 25, 15]
# Soccer table (set 4)
GC_ = ["Game 1", "Game 2", "Game 3", "Game 4"]
GR = [4, 7, 2, 5]
GO = [6, 3, 5, 5]


def pets_svg():
    return dbar_svg("Pets of students in two classes", "Pet", "Students", PC, [PA, PB], ["Class 5A", "Class 5B"],
                    10, 1, 2, gy=12, source="Source: class surveys")


def books_svg():
    return dbar_svg("Books read by two Grade 5 classes", "Month", "Books", BC_, [BA, BB], ["5A", "5B"],
                    20, 2, 2, gy=18, source="Source: school library")


def winter_svg():
    return dbar_svg("Favourite winter sport", "Sport", "Students", WC, [W5, W6], ["Grade 5", "Grade 6"],
                    40, 5, 10, gy=14, source="Source: school survey")


def cans_svg():
    return dbar_svg("Cans collected for the food bank", "Week", "Cans", CC, [C25, C26], ["2025", "2026"],
                    120, 10, 20, gy=11, source="Source: student council")


def school_svg():
    return dbar_svg("How Grade 5 students get to school", "Way", "Students", HC, [HF, HS], ["Fall", "Spring"],
                    16, 2, 2, gy=18, source="Source: class surveys")


def terry_svg():
    return dbar_svg("Money raised for the Terry Fox Run", "Class", "Dollars ($)", TC, [T25, T26], ["2025", "2026"],
                    160, 10, 20, gy=9, source="Source: school office")


def salmon_svg():
    return dbar_svg("Salmon counted at the creek in October", "Week", "Salmon", EC, [E25, E26], ["2025", "2026"],
                    50, 5, 10, gy=15, source="Source: class field trips")


def lib_graph(a, b):
    return dbar_svg("Books borrowed in one week", "Kind of book", "Books", LC, [a, b], ["Grade 4", "Grade 5"],
                    50, 5, 10, gy=13)


LIB_T = table(["Kind of book", "Grade 4", "Grade 5"], [[c, a, b] for c, a, b in zip(LC, L4, L5)])
GAME_T = table(["Game", "Rockets", "Orcas"], [[c, a, b] for c, a, b in zip(GC_, GR, GO)])


# ------------------------------------------------------------ set 1: read a double bar graph with a legend
def set_read():
    its = []
    its.append(mcq("What does the legend on a double bar graph tell you?", "Which colour shows which group",
                   ["What the scale counts by", "The total of all the bars", "Where the data came from"],
                   "The legend (or key) matches each colour to a group, such as green for Class 5A and orange for Class 5B. "
                   "The source tells where the data came from."))
    its.append(mcq("Why does a double bar graph have two bars for each category?", "To compare two groups",
                   ["To show the data twice", "To make the graph wider", "To show the total"],
                   "Each pair has one bar for each group, side by side, so you can see at once which group has more."))
    f = fig(pets_svg())
    assert PA[0] == 8 and PB[0] == 6
    its.append(mcqv(f + "How many students in Class 5A have a dog?", 8, [6, 14, 2], S,
                    "Class 5A is green in the legend. The green Dog bar reaches the line labelled 8. "
                    "(6 is the orange Class 5B bar, 14 adds both bars, and 2 is the difference.)"))
    its.append(mcqv(f + "How many students in Class 5B have a cat?", 7, [5, 12, 2], S,
                    "Class 5B is orange. The orange Cat bar ends one line above 6, so it shows 7. "
                    "(5 is the green Class 5A bar, and 12 adds both bars.)"))
    its.append(mcqv(f + "How many students in Class 5B have no pet?", 6, [9, 15, 3], S,
                    "Find the orange bar above “No pet”. It reaches the line labelled 6. "
                    "(9 is the green Class 5A bar, 15 adds both bars, and 3 is the difference.)"))
    its.append(mcq(f + "Which class has more students with fish?", "Class 5B", ["Class 5A", "Both the same", "Neither class"],
                   "For Fish, the orange Class 5B bar (4) is taller than the green Class 5A bar (2)."))
    its.append(mcq(f + "Which answer was the most common in Class 5A?", "No pet", ["Dog", "Cat", "Fish"],
                   "The tallest green bar is “No pet”, with 9 students. (Dog has 8. Cat is the tallest orange bar, for Class 5B.)"))
    assert PA[0] - PB[0] == 2
    its.append(mcqv(f + "How many more students in Class 5A than in Class 5B have a dog?", 2, [14, 8, 6], S,
                    "Dog: Class 5A has 8 and Class 5B has 6. 8 − 6 = 2 more students. (14 adds the two bars.)"))
    assert sum(PA) == 24 and sum(PB) == 23
    its.append(mcqv(f + "Every student in Class 5A answered. How many students are in Class 5A?", 24, [23, 47, 9], S,
                    "Add the green bars: 8 + 5 + 2 + 9 = 24. (23 adds the orange Class 5B bars, 47 adds both classes, "
                    "and 9 is only the tallest bar.)"))
    its.append(mcqv(f + "Every student in Class 5B answered. How many students are in Class 5B?", 23, [24, 47, 7], S,
                    "Add the orange bars: 6 + 7 + 4 + 6 = 23. (24 adds the green Class 5A bars, and 7 is only the tallest bar.)"))
    f = fig(books_svg())
    B = lambda x: unit(x, "book", "books")
    its.append(mcqv(f + "How many books did 5A read in October?", 18, [20, 9, 38], B,
                    "5A is green. The green October bar reaches the line labelled 18. "
                    "(20 is the orange 5B bar, 9 counts the grid lines as 1 each, but each line stands for 2, "
                    "and 38 adds both bars.)"))
    its.append(mcqv(f + "How many books did 5B read in November?", 16, [11, 8, 27], B,
                    "The orange November bar reaches the line labelled 16. "
                    "(11 is the green 5A bar, 8 counts grid lines instead of reading the scale, and 27 adds both bars.)"))
    its.append(mcqv(f + "How many books did 5A read in November?", 11, [12, 10, 16], B,
                    "The green November bar ends halfway between 10 and 12. Halfway between them is 11. "
                    "(12 and 10 are the lines on each side, and 16 is the orange 5B bar.)"))
    its.append(mcq(f + "In which month did both classes read the same number of books?", "Dec", ["Oct", "Sep", "Nov"],
                   "In December both bars reach 16, so the two bars are the same height."))
    its.append(mcq(f + "In which month did 5A read more books than 5B?", "Sep", ["Oct", "Nov", "Dec"],
                   "Only in September is the green 5A bar taller: 14 books for 5A and 12 for 5B."))
    its.append(mcq(f + "Which bars show 5B?", "The orange bars",
                   ["The green bars", "The taller bar in each pair", "The bars on the left"],
                   "The legend shows that orange is 5B. The taller bar is not always 5B: in September the green bar is taller."))
    its.append(mcq(f + "In October, which class read more books, and how many more?", "5B, 2 more books",
                   ["5A, 2 more books", "5B, 1 more book", "5B, 38 more books"],
                   "October: 5B (orange) read 20 and 5A (green) read 18. 20 − 18 = 2. "
                   "(1 more counts the grid lines, but each line stands for 2, and 38 adds the bars.)"))
    its.append(mcqv(f + "What is the greatest number of books one class read in one month?", 20, [18, 38, 10], B,
                    "The tallest bar is the orange 5B bar for October. It reaches 20. "
                    "(18 is the tallest green bar, 38 adds October’s two bars, and 10 counts grid lines.)"))
    its.append(mcq("On a double bar graph, the green bar for soccer is taller than the orange bar for soccer. What does this mean?",
                   "The green group chose soccer more", ["The orange group chose soccer more",
                                                        "Soccer is the most popular", "Both groups chose soccer equally"],
                   "In a pair, the taller bar shows the bigger number. It tells you nothing about the other sports."))
    its.append(mcq("Ji-woo is asked about Class 5A (green), but she reads the orange bar. What should she do first?",
                   "Check the legend for the colour", ["Read the taller bar", "Count the grid lines",
                                                        "Read the title again"],
                   "The legend tells which colour is Class 5A. Find that colour in the pair, then read the scale."))
    return {"title": "Read double bar graphs with a legend", "items": its}


# ------------------------------------------------------------ set 2: scales of 2, 5 and 10
def set_scale():
    its = []
    its.append(mcqv("Each grid line on a graph stands for 2. A bar reaches the 6th line above 0. What value does it show?",
                    12, [6, 8, 3], num,
                    "This is many-to-one: 1 line stands for 2. 6 lines × 2 = 12. "
                    "(6 reads each line as 1, 8 adds 2, and 3 divides by 2.)"))
    its.append(mcqv("Each grid line on a graph stands for 5. A bar reaches the 7th line above 0. What value does it show?",
                    35, [7, 12, 30], num,
                    "1 line stands for 5, so 7 lines stand for 7 × 5 = 35. (7 reads each line as 1, and 12 adds 7 + 5.)"))
    its.append(mcqv("A graph counts by 10. A bar ends halfway between the lines for 40 and 50. What value does it show?",
                    45, [41, 50, 4], num,
                    "Halfway between 40 and 50 is 45, because half of 10 is 5. (41 treats the half line as 1, "
                    "50 rounds up to the next line, and 4 counts lines.)"))
    f = fig(winter_svg())
    its.append(mcqv(f + "How many Grade 5 students chose skiing?", 25, [20, 5, 30], S,
                    "Grade 5 is green. The green Skiing bar ends on the unlabelled line between 20 and 30. "
                    "Each line stands for 5, so it shows 25. (20 is the orange Grade 6 bar, and 5 counts the lines.)"))
    its.append(mcqv(f + "How many Grade 6 students chose snowboarding?", 35, [30, 7, 40], S,
                    "Grade 6 is orange. The orange Snowboarding bar ends on the line halfway between 30 and 40, which is 35. "
                    "(30 is the green Grade 5 bar, 7 counts the lines, and 40 rounds up.)"))
    its.append(mcqv(f + "How many Grade 6 students chose skating?", 10, [15, 2, 20], S,
                    "The orange Skating bar reaches the line labelled 10. (15 is the green Grade 5 bar, "
                    "and 2 counts the lines instead of reading the scale.)"))
    its.append(mcqv(f + "How many Grade 6 students chose hockey?", 30, [20, 6, 25], S,
                    "The orange Hockey bar reaches the line labelled 30. (20 is the green Grade 5 bar, and 6 counts the lines.)"))
    its.append(mcqv(f + "What does each grid line on this graph stand for?", 5, [10, 1, 2], S,
                    "The labels go 0, 10, 20 …, and there is one more line halfway between each pair. "
                    "So each line stands for 5 students. (10 is the step between the labels.)"))
    f = fig(cans_svg())
    C = lambda x: unit(x, "can", "cans")
    its.append(mcqv(f + "How many cans were collected in Week 3 of 2026?", 110, [90, 11, 100], C,
                    "2026 is orange. The orange Week 3 bar ends on the line between 100 and 120, which is 110. "
                    "(90 is the green 2025 bar, 11 counts the lines, and 100 reads the label below.)"))
    its.append(mcqv(f + "How many cans were collected in Week 2 of 2025?", 70, [50, 7, 60], C,
                    "2025 is green. The green Week 2 bar ends on the line between 60 and 80, which is 70. "
                    "(50 is the orange 2026 bar, and 7 counts the lines.)"))
    its.append(mcqv(f + "What does each grid line on this graph stand for?", 10, [20, 1, 5], C,
                    "There is one line between 0 and 20, so each line stands for 10 cans. (20 is the step between the labels.)"))
    its.append(mcqv(f + "How many cans were collected in Week 1 of 2026?", 60, [40, 6, 3], C,
                    "The orange Week 1 bar reaches the line labelled 60. "
                    "(40 is the green 2025 bar, 6 counts the lines, and 3 counts the labels.)"))
    assert sum(C26) == 300 and sum(C25) == 260
    its.append(mcqv(f + "How many cans were collected in 2026 in all?", 300, [260, 110, 30], C,
                    "Add the orange bars: 60 + 50 + 110 + 80 = 300. (260 adds the green 2025 bars, "
                    "110 is only the tallest bar, and 30 counts the lines.)"))
    f = fig(books_svg())
    its.append(mcq(f + "Which bar ends halfway between two grid lines?", "5A in November",
                   ["5B in November", "5A in October", "5B in December"],
                   "The green November bar ends between 10 and 12, so it shows 11. Every other bar ends on a line."))
    its.append(mcq("A double bar graph will show these numbers: 45, 80, 65, 120, 95, 110. Which scale works best?",
                   "0 to 120, counting by 10", ["0 to 120, counting by 1", "0 to 100, counting by 10",
                                               "0 to 1000, counting by 100"],
                   "Counting by 10 gives 12 lines, so the graph is easy to read. Counting by 1 needs 120 lines, "
                   "0 to 100 is too short for 110 and 120, and counting by 100 makes the bars too short to compare."))
    its.append(mcq("A double bar graph will show these numbers: 4, 9, 12, 7, 18, 10. Which scale works best?",
                   "0 to 20, counting by 2", ["0 to 10, counting by 1", "0 to 200, counting by 20",
                                             "0 to 100, counting by 50"],
                   "The greatest number is 18, so 0 to 20 fits. Counting by 2 gives 10 lines. "
                   "0 to 10 is too short for 12 and 18, and the other scales make all the bars tiny."))
    its.append(mcq("A double bar graph will show these numbers: 15, 25, 35, 40, 20. Which scale works best?",
                   "0 to 40, counting by 5", ["0 to 40, counting by 1", "0 to 30, counting by 5",
                                             "0 to 400, counting by 100"],
                   "Every number is a multiple of 5, so counting by 5 puts each bar on a line: 8 lines in all. "
                   "0 to 30 is too short for 35 and 40."))
    its.append(mcq("Kai reads a bar on a graph that counts by 5. The bar reaches the 6th line, and Kai says 6. What is right?",
                   "30, because 6 × 5 = 30", ["6, because it is the 6th line", "11, because 6 + 5 = 11",
                                              "35, because 7 × 5 = 35"],
                   "Each line stands for 5, not 1. 6 lines × 5 = 30."))
    its.append(mcqv("A graph counts by 10. How many grid lines above 0 tall is a bar that shows 80?", 8, [80, 18, 4],
                    lambda x: unit(x, "line", "lines"),
                    "Each line stands for 10, so 80 ÷ 10 = 8 lines. "
                    "(80 uses one line for each unit, and 4 divides by 20.)"))
    its.append(mcqv("A graph counts by 2. A bar ends halfway between the lines for 14 and 16. What value does it show?",
                    15, [14.5, 16, 7], lambda x: num(x) if F(x).denominator == 1 else "14.5",
                    "The lines go up by 2, so halfway between 14 and 16 is 15. "
                    "(14.5 adds only half of 1, 16 rounds up, and 7 counts lines.)"))
    return {"title": "Scales of 2, 5 and 10", "items": its}


# ------------------------------------------------------------ set 3: compare two groups
def set_compare():
    its = []
    f = fig(winter_svg())
    its.append(mcqv(f + "How many more Grade 6 students than Grade 5 students chose hockey?", 10, [50, 2, 30], S,
                    "Hockey: Grade 6 has 30 and Grade 5 has 20. 30 − 20 = 10 more students. "
                    "(50 adds the bars, and 2 counts the grid lines between the tops of the bars.)"))
    its.append(mcq(f + "Which sports did more Grade 5 students choose than Grade 6 students?", "Skiing and skating",
                   ["Snowboarding and hockey", "Skiing only", "Hockey only"],
                   "The green Grade 5 bar is taller for skiing (25 and 20) and skating (15 and 10). "
                   "For snowboarding and hockey the orange Grade 6 bar is taller."))
    assert W5[1] + W6[1] == 65
    its.append(mcqv(f + "How many students chose snowboarding in all?", 65, [5, 35, 13], S,
                    "Add both snowboarding bars: 30 + 35 = 65. (5 is the difference, 35 is one bar, and 13 counts lines.)"))
    d = [abs(a - b) for a, b in zip(W5, W6)]
    assert d == [5, 5, 5, 10]
    its.append(mcq(f + "For which sport is the difference between the two grades the greatest?", "Hockey",
                   ["Snowboarding", "Skiing", "Skating"],
                   "Differences: skiing 5, snowboarding 5, skating 5, hockey 30 − 20 = 10. Hockey has the biggest gap. "
                   "(Snowboarding has the tallest bars, but they are close in height.)"))
    assert sum(W5) == 90 and sum(W6) == 95
    its.append(mcq(f + "Each student chose one sport. Which grade had more students answer?", "Grade 6: 95 students",
                   ["Grade 5: 90 students", "Grade 6: 35 students", "They had the same number"],
                   "Grade 5: 25 + 30 + 15 + 20 = 90. Grade 6: 20 + 35 + 10 + 30 = 95. "
                   "(35 is only the tallest orange bar.)"))
    f = fig(cans_svg())
    C = lambda x: unit(x, "can", "cans")
    its.append(mcq(f + "In which week did 2025 collect more cans than 2026?", "Week 2", ["Week 1", "Week 3", "Week 4"],
                   "Only in Week 2 is the green 2025 bar taller: 70 cans in 2025 and 50 in 2026."))
    its.append(mcqv(f + "In Week 3, how many more cans were collected in 2026 than in 2025?", 20, [200, 2, 110], C,
                    "Week 3: 2026 has 110 and 2025 has 90. 110 − 90 = 20. "
                    "(200 adds the bars, 2 counts lines, and 110 is one bar.)"))
    its.append(mcqv(f + "How many cans were collected in Week 4 of both years together?", 140, [20, 80, 14], C,
                    "Week 4: 60 + 80 = 140 cans. (20 is the difference, 80 is one bar, and 14 counts lines.)"))
    assert sum(C26) - sum(C25) == 40
    its.append(mcqv(f + "How many more cans were collected in 2026 than in 2025, in all four weeks?", 40, [560, 20, 4], C,
                    "2026: 60 + 50 + 110 + 80 = 300. 2025: 40 + 70 + 90 + 60 = 260. 300 − 260 = 40. "
                    "(560 adds the two totals, 20 is only the Week 3 difference, and 4 counts lines.)"))
    tot = [a + b for a, b in zip(C25, C26)]
    assert tot == [100, 120, 200, 140]
    its.append(mcq(f + "Which week had the most cans for both years together?", "Week 3: 200 cans",
                   ["Week 4: 140 cans", "Week 2: 120 cans", "Week 3: 110 cans"],
                   "Add each pair: Week 1 100, Week 2 120, Week 3 200, Week 4 140. Week 3 has the most. "
                   "(110 is only one bar.)"))
    f = fig(school_svg())
    its.append(mcqv(f + "How many more students biked to school in spring than in fall?", 6, [14, 3, 10], S,
                    "Bike: spring 10, fall 4. 10 − 4 = 6. (14 adds the bars, 3 counts grid lines, "
                    "and 10 is only the spring bar.)"))
    its.append(mcq(f + "Which way to school went down the most from fall to spring?", "Car", ["Bus", "Walk", "Bike"],
                   "Car went from 10 to 4, down 6. Bus went from 8 to 6, down 2. Walk and bike went up. "
                   "(Bike changed by 6 too, but it went up.)"))
    its.append(mcqv(f + "In spring, how many students walked or biked?", 24, [14, 16, 12], S,
                    "Spring (orange): walk 14 + bike 10 = 24. (14 is walking only, 16 uses the fall bars, "
                    "and 12 counts grid lines.)"))
    assert HF[0] == 3 * HF[1]
    its.append(mcqv(f + "In fall, how many times as many students walked as biked?", 3, [8, 16, 4],
                    lambda x: "%s times" % num(x),
                    "Fall: walk 12, bike 4. 12 ÷ 4 = 3, so 3 times as many. "
                    "(8 is 12 − 4, which is how many more, 16 adds them, and 4 is the bike bar.)"))
    assert sum(HF) == sum(HS) == 34
    its.append(mcq(f + "Did the same number of students answer in fall and in spring?", "Yes: 34 each",
                   ["No: more in spring", "No: more in fall", "Yes: 68 each"],
                   "Fall: 12 + 4 + 8 + 10 = 34. Spring: 14 + 10 + 6 + 4 = 34. The same class answered twice. "
                   "(68 adds both seasons.)"))
    f = fig(pets_svg())
    d = [abs(a - b) for a, b in zip(PA, PB)]
    assert d == [2, 2, 2, 3]
    its.append(mcq(f + "For which answer is the difference between the two classes the greatest?", "No pet",
                   ["Dog", "Cat", "Fish"],
                   "Differences: dog 2, cat 2, fish 2, no pet 9 − 6 = 3. “No pet” has the biggest gap."))
    assert PA[0] + PA[1] == PB[0] + PB[1] == 13
    its.append(mcqv(f + "How many students in both classes have a dog or a cat?", 26, [13, 14, 12], S,
                    "Dogs: 8 + 6 = 14. Cats: 5 + 7 = 12. 14 + 12 = 26. "
                    "(13 is one class only, 14 is dogs only, and 12 is cats only.)"))
    its.append(mcqv("A graph counts by 4. Grade 5 has 48 votes for soccer and Grade 6 has 36. "
                    "How many grid lines taller is the Grade 5 bar?", 3, [12, 21, 9],
                    lambda x: unit(x, "line", "lines"),
                    "The difference is 48 − 36 = 12 votes. Each line stands for 4, so 12 ÷ 4 = 3 lines. "
                    "(12 is the difference in votes, 21 is 84 ÷ 4, and 9 is the Grade 6 bar.)"))
    its.append(mcq("In a double bar graph, the two bars for basketball are the same height. What does this tell you?",
                   "Both groups have the same number", ["Nobody chose basketball", "Basketball is the favourite",
                                                        "The graph has a mistake"],
                   "Bars of the same height show the same value, so both groups gave basketball the same number of votes."))
    its.append(mcqv("A double bar graph shows hockey wins. The Eagles’ bar reaches 14 and the Orcas’ bar reaches 9. "
                    "How many more wins do the Eagles have?", 5, [23, 14, 9], lambda x: unit(x, "win", "wins"),
                    "14 − 9 = 5 more wins. (23 adds the bars, and 14 and 9 are the bars themselves.)"))
    return {"title": "Compare two groups", "items": its}


# ------------------------------------------------------------ set 4: make a double bar graph from a table
def set_make():
    its = []
    T = "The table shows the books two grades borrowed from the library in one week." + LIB_T
    its.append(mcqv(T + "How many bars will a double bar graph of this table have?", 8, [4, 2, 6],
                    lambda x: unit(x, "bar", "bars"),
                    "There are 4 kinds of book and 2 grades, so 4 × 2 = 8 bars, in 4 pairs. "
                    "(4 counts only the pairs, and 2 counts only the grades.)"))
    its.append(mcq(T + "What should the legend of the graph show?", "Grade 4 and Grade 5",
                   ["Fiction, non-fiction, comics, poetry", "0, 10, 20, 30, 40, 50", "Books borrowed in one week"],
                   "The legend tells which colour is which group. The two groups are the columns of the table: Grade 4 and Grade 5. "
                   "The kinds of book go under the bars."))
    its.append(mcq(T + "Which scale works best for the graph?", "0 to 50, counting by 5",
                   ["0 to 50, counting by 1", "0 to 30, counting by 5", "0 to 500, counting by 100"],
                   "Every number is a multiple of 5 and the greatest is 45, so 0 to 50 by 5s fits every bar on a line. "
                   "0 to 30 is too short for 35, 40 and 45, counting by 1 needs 50 lines, and 0 to 500 makes the bars tiny."))
    its.append(mcq(T + "What label goes under the bars, along the bottom axis?", "Kind of book",
                   ["Number of books", "Grade 4 and Grade 5", "Counting by 5"],
                   "The categories go along the bottom, so the label is “Kind of book”. "
                   "“Number of books” labels the side axis with the scale."))
    its.append(mcq(T + "Which is the best title for the graph?", "Books Borrowed by Grade 4 and Grade 5",
                   ["Fiction and Comics", "Grade 4 Books", "Counting by 5"],
                   "A good title tells what the whole graph shows: books borrowed by both grades. "
                   "The other titles leave out a grade or the kinds of book."))
    assert L4[2] // 5 == 9
    its.append(mcqv(T + "The scale counts by 5. How many grid lines tall is the Grade 4 bar for comics?", 9, [45, 5, 8],
                    lambda x: unit(x, "line", "lines"),
                    "Grade 4 borrowed 45 comics. 45 ÷ 5 = 9 lines. "
                    "(45 uses one line for each book, 5 is the Grade 5 comics bar, 25 ÷ 5, and 8 is the Grade 5 fiction bar.)"))
    its.append(mcq(T + "The scale is labelled 0, 10, 20, 30 … Where does the Grade 5 bar for poetry end?",
                   "Halfway between 10 and 20", ["On the line labelled 10", "On the line labelled 20", "At the 15th line"],
                   "Grade 5 borrowed 15 poetry books. 15 is halfway between 10 and 20. "
                   "(The 15th line would be 75 if each line stands for 5.)"))
    f = fig(lib_graph(L4, [L5[0], None, L5[2], L5[3]]))
    its.append(mcqv(T + f + "Ava is making the graph. Which number should the orange bar for non-fiction reach?",
                    30, [20, 6, 25], num,
                    "Orange is Grade 5. The table shows Grade 5 borrowed 30 non-fiction books, so the bar reaches 30. "
                    "(20 is the Grade 4 number, 6 counts lines, and 25 is the Grade 5 comics.)"))
    bad = list(L4)
    bad[2] = 40
    f = fig(lib_graph(bad, L5))
    its.append(mcq(T + f + "Owen made this graph from the table. Which bar does not match the table?", "Grade 4 comics",
                   ["Grade 5 comics", "Grade 4 fiction", "Grade 5 fiction"],
                   "The green Grade 4 comics bar ends at 40, but the table says 45. It should end on the line halfway between 40 and 50. "
                   "Every other bar matches the table."))
    sw = [L5[0]] + L4[1:], [L4[0]] + L5[1:]
    f = fig(lib_graph(sw[0], sw[1]))
    its.append(mcq(T + f + "What mistake did Simran make in her graph?", "She swapped the two fiction bars",
                   ["She used the wrong scale", "She left out a bar", "She swapped the two comics bars"],
                   "In the table, Grade 4 fiction is 35 and Grade 5 fiction is 40. In her graph the green bar is 40 and the orange "
                   "bar is 35, so the two bars in the pair are switched. Always check the legend colour for each bar."))
    assert [b > a for a, b in zip(L4, L5)] == [True, True, False, True]
    its.append(mcq(T + "For which kinds of book will the Grade 5 bar be taller than the Grade 4 bar?",
                   "Fiction, non-fiction and poetry", ["Comics only", "Fiction only", "All four kinds"],
                   "Compare each row: fiction 40 &gt; 35, non-fiction 30 &gt; 20, poetry 15 &gt; 10, but comics 25 &lt; 45."))
    T = "The table shows the goals two soccer teams scored in four games." + GAME_T
    its.append(mcq(T + "Which scale works best for a double bar graph of these goals?", "0 to 8, counting by 1",
                   ["0 to 5, counting by 1", "0 to 70, counting by 10", "0 to 100, counting by 20"],
                   "The greatest number is 7, so 0 to 8 by 1s fits. Here each line stands for one goal (one-to-one). "
                   "0 to 5 is too short for 6 and 7, and the other scales make the bars tiny."))
    its.append(mcq(T + "In which game will the two bars be the same height?", "Game 4", ["Game 1", "Game 2", "Game 3"],
                   "In Game 4 both teams scored 5 goals, so the bars are the same height."))
    d = [abs(a - b) for a, b in zip(GR, GO)]
    assert d == [2, 4, 3, 0]
    its.append(mcq(T + "In which game will the gap between the two bars be the greatest?", "Game 2",
                   ["Game 1", "Game 3", "Game 4"],
                   "Differences: Game 1 is 2, Game 2 is 7 − 3 = 4, Game 3 is 3, Game 4 is 0. Game 2 has the biggest gap."))
    its.append(mcq(T + "The scale counts by 2. Where does the Rockets’ bar for Game 2 end?", "Halfway between 6 and 8",
                   ["On the line for 6", "On the line for 8", "At the 7th line"],
                   "The Rockets scored 7. 7 is halfway between 6 and 8. "
                   "(The 7th line would be 14 when each line stands for 2.)"))
    its.append(mcq("A table shows 0 for one group in a category. How do you show it on a double bar graph?",
                   "No bar, but keep the label", ["A bar 1 line tall", "Leave out the category", "Copy the other bar"],
                   "A value of 0 has no height, so there is no bar. Keep the category label so readers can see it is 0."))
    its.append(mcq("Which data fits a double bar graph best?", "Favourite fruits of Grade 5 and Grade 6",
                   ["Favourite fruits of one class", "Height of one sunflower each week", "Ages of students in one class"],
                   "A double bar graph compares two groups across the same categories. The other data has only one group."))
    its.append(mcq("Mateo forgot the legend on his double bar graph. What can a reader not tell?", "Which bar is which group",
                   ["How tall each bar is", "What the categories are", "What the graph is about"],
                   "Without a legend, the reader cannot tell which colour stands for which group."))
    its.append(mcq("Why should the scale of a bar graph start at 0?", "So bar heights compare fairly",
                   ["So the graph is shorter", "So the legend fits", "So every bar ends on a line"],
                   "If the scale starts at 0, a bar twice as tall really shows twice as much. "
                   "Starting higher makes small differences look big."))
    its.append(mcqv("A scale goes from 0 to 150, counting by 10. How many grid lines are above 0?", 15, [150, 10, 16],
                    lambda x: unit(x, "line", "lines"),
                    "150 ÷ 10 = 15 lines above 0. (16 also counts the line at 0, and 150 uses one line for each unit.)"))
    return {"title": "Make a double bar graph from a table", "items": its}


# ------------------------------------------------------------ set 5: conclusions and word problems
def set_concl():
    its = []
    f = fig(terry_svg())
    assert [b < a for a, b in zip(T25, T26)] == [False, False, True, False]
    its.append(mcq(f + "Which class raised less money in 2026 than in 2025?", "5C", ["5A", "5B", "5D"],
                   "Only for 5C is the orange 2026 bar shorter: $130 in 2026 and $150 in 2025."))
    assert sum(T25) == 470 and sum(T26) == 520
    its.append(mcqv(f + "How much more did the four classes raise in 2026 than in 2025?", 50, [990, 40, 5], D,
                    "2026: 140 + 100 + 130 + 150 = $520. 2025: 120 + 90 + 150 + 110 = $470. 520 − 470 = $50. "
                    "($990 adds the totals, $40 is only the 5D difference, and $5 counts grid lines.)"))
    assert min(T25 + T26) == 90
    its.append(mcq(f + "Which conclusion does the graph support?", "Every class raised at least $90 each year",
                   ["5C raised the most in both years", "5B raised more in 2025 than in 2026",
                    "5D raised twice as much in 2026"],
                   "The shortest bar is 5B in 2025, at $90, so every class raised $90 or more. "
                   "5D raised the most in 2026, 5B went up from $90 to $100, and 5D went from $110 to $150, not twice as much."))
    its.append(mcqv(f + "How much more did 5D raise in 2026 than in 2025?", 40, [260, 150, 4], D,
                    "5D: $150 in 2026 and $110 in 2025. 150 − 110 = $40. "
                    "($260 adds the bars, $150 is one bar, and $4 counts grid lines.)"))
    its.append(mcq(f + "The school’s goal for 2026 was $500. Did the four classes reach it?", "Yes: they raised $520",
                   ["No: they raised $470", "No: they raised $150", "Yes: they raised $990"],
                   "Add the orange 2026 bars: 140 + 100 + 130 + 150 = $520, which is more than $500. "
                   "($470 adds the green 2025 bars instead.)"))
    its.append(mcqv(f + "How much did all four classes raise in 2025 and 2026 together?", 990, [470, 520, 50], D,
                    "2025: $470. 2026: $520. 470 + 520 = $990. ($470 and $520 are each one year only.)"))
    f = fig(salmon_svg())
    its.append(mcq(f + "In which week were the most salmon counted in 2026?", "Week 3", ["Week 4", "Week 2", "Week 1"],
                   "The tallest orange bar is Week 3, at 45 salmon."))
    its.append(mcqv(f + "How many salmon were counted in Week 4 of both years together?", 50, [10, 30, 5],
                    lambda x: unit(x, "salmon", "salmon"),
                    "Week 4: 20 in 2025 and 30 in 2026. 20 + 30 = 50. "
                    "(10 is the difference, 30 is one bar, and 5 counts grid lines.)"))
    its.append(mcq(f + "Mei says, “More salmon came in 2026 than in 2025 every week.” Is she right?",
                   "No: Weeks 1 and 2 were higher in 2025", ["Yes: the tallest bar is orange",
                                                            "Yes: Week 3 had 45 salmon", "No: every week was higher in 2025"],
                   "Week 1: 15 in 2025, 10 in 2026. Week 2: 35 in 2025, 25 in 2026. 2026 was higher only in Weeks 3 and 4. "
                   "One tall bar does not prove “every week”."))
    assert sum(E25) == sum(E26) == 110
    its.append(mcq(f + "Which year had more salmon in all four weeks?", "Neither: both had 110",
                   ["2026: it has the tallest bar", "2025: 40 salmon", "2026: 45 salmon"],
                   "2025: 15 + 35 + 40 + 20 = 110. 2026: 10 + 25 + 45 + 30 = 110. The totals are the same, "
                   "even though 2026 has the tallest bar."))
    its.append(mcq(f + "Which statement is true for both years?", "The most salmon came in Week 3",
                   ["The fewest salmon came in Week 4", "More than 40 salmon came in Week 2", "The counts went up every week"],
                   "Week 3 has the tallest bar in both colours: 40 in 2025 and 45 in 2026. "
                   "The fewest came in Week 1 both years, and the counts dropped in Week 4."))
    f = fig(winter_svg())
    tot = [a + b for a, b in zip(W5, W6)]
    assert tot == [45, 65, 25, 50]
    its.append(mcq(f + "The school will buy gear for one sport for Grades 5 and 6. Which sport got the most votes in all?",
                   "Snowboarding: 65 votes", ["Hockey: 50 votes", "Skiing: 45 votes", "Snowboarding: 35 votes"],
                   "Add each pair: skiing 45, snowboarding 65, skating 25, hockey 50. Snowboarding has the most. "
                   "(35 is only the Grade 6 bar.)"))
    its.append(mcq(f + "Ryan says, “Hockey is the favourite sport in Grade 6.” Is this supported?",
                   "No: snowboarding got 35 votes", ["Yes: hockey got 30 votes", "Yes: hockey has the biggest gap",
                                                     "No: skiing got 35 votes"],
                   "The tallest orange bar is snowboarding, with 35. Hockey has 30 Grade 6 votes, which is second."))
    f = fig(school_svg())
    its.append(mcqv(f + "How many fewer students came by car in spring than in fall?", 6, [14, 4, 3], S,
                    "Car: fall 10, spring 4. 10 − 4 = 6 fewer. (14 adds the bars, 4 is one bar, and 3 counts grid lines.)"))
    its.append(mcq(f + "Which is a reasonable reason for the changes from fall to spring?",
                   "Spring weather is better for biking", ["The bus got faster", "Fewer students are in the class",
                                                           "The graph uses a scale of 2"],
                   "More students biked and walked in spring, and fewer came by car. Nicer spring weather is a sensible reason. "
                   "The class size did not change: 34 students both times."))
    its.append(mcq("At a Surrey school, Grade 5 voted 48 for soccer and 36 for hockey. Grade 6 voted 42 for soccer and "
                   "54 for hockey. Which statement is true?", "Grade 5 prefers soccer, Grade 6 hockey",
                   ["Both grades prefer hockey", "Both grades prefer soccer", "Grade 5 prefers hockey"],
                   "Grade 5: 48 &gt; 36, so soccer has more votes. Grade 6: 54 &gt; 42, so hockey has more votes."))
    assert 48000 - 42500 == 5500
    its.append(mcqv("A double bar graph shows visitors to a science centre in Vancouver. July 2025: %s visitors. "
                    "July 2026: %s visitors. How many more visitors came in July 2026?" % (num(42500), num(48000)),
                    5500, [90500, 6500, 6000], lambda x: unit(x, "visitor", "visitors"),
                    "48%s000 − 42%s500 = 5500. (90%s500 adds, 6500 subtracts 0 − 5 as 5 − 0 instead of regrouping, "
                    "and 6000 forgets the 500.)"
                    % (NB, NB, NB)))
    its.append(mcq("Two classes counted bald eagles on field trips. 5A saw 18 in December and 22 in January. "
                   "5B saw 12 in December and 30 in January. Which conclusion is supported?",
                   "Both classes saw more in January", ["5A saw more eagles both months", "5B saw fewer in January",
                                                        "Both classes saw 40 eagles in all"],
                   "5A: 18 then 22. 5B: 12 then 30. Both numbers went up in January. "
                   "5B saw more in January, and the totals are 40 and 42."))
    its.append(mcq("To compare the favourite sports of Grade 5 and Grade 6, Liam asks only the players on his hockey team. "
                   "What is the problem?", "His team will likely choose hockey",
                   ["He asked too many people", "Hockey is not a sport", "He needs a scale of 10"],
                   "Hockey players are likely to choose hockey, so the graph would not show what all students like. "
                   "He should ask students from all the classes."))
    its.append(mcq("A graph’s scale starts at 50, not 0. The Grade 5 bar shows 60 and the Grade 6 bar shows 55, so the "
                   "Grade 5 bar looks twice as tall. Is Grade 5 really twice as much?", "No: 60 is only 5 more than 55",
                   ["Yes: its bar is twice as tall", "Yes: 60 is more than 55", "No: Grade 6 is more"],
                   "From 50, the bars are 10 and 5 units tall, so one looks twice as tall. "
                   "But 60 is not twice 55. Always read the numbers on the scale."))
    return {"title": "Draw conclusions: BC word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def ltable(head, rows):
    return "<div class='sn-tw'>" + table(head, rows) + "</div>"


LD = (["Pizza", "Sushi", "Tacos"], [12, 8, 5], [10, 14, 7])


def body_html():
    g = dbar_svg("Favourite lunch", "Lunch", "Students", LD[0], [LD[1], LD[2]], ["Grade 5", "Grade 6"],
                 16, 2, 2, gy=18, source="Source: school survey")
    return (
        "<h2>What is a double bar graph?</h2>"
        "<p>A <b>double bar graph</b> shows two groups side by side. Each category has a pair of bars: one bar for each group. "
        "The <b>legend</b> tells you which colour is which group. Like every graph, it needs a title, axis labels, a scale and a source.</p>"
        "<figure class='sn-fig'>" + g +
        "<figcaption>Green is Grade 5 and orange is Grade 6. For sushi, the orange bar (14) is taller than the green bar (8).</figcaption></figure>" +
        "<h2>Read the legend, then the scale</h2>"
        "<p>First find the right colour in the legend. Then follow the top of that bar across to the scale. "
        "When one grid line stands for 1, it is <b>one-to-one</b>. When one line stands for 2, 5 or 10, it is <b>many-to-one</b>. "
        "A bar that ends halfway between two lines shows the number halfway between them.</p>" +
        ex("Example 1", "How many Grade 6 students chose tacos?",
           "Grade 6 is orange. The orange Tacos bar ends halfway between 6 and 8. The lines go up by 2, so halfway is 7.",
           "7 students") +
        ex("Example 2", "How many more Grade 6 students than Grade 5 students chose sushi?",
           "Sushi: Grade 6 has 14 and Grade 5 has 8. 14 − 8 = 6.", "6 more students") +
        "<h2>Make a double bar graph from a table</h2>" +
        ltable(["Lunch", "Grade 5", "Grade 6"], [[c, a, b] for c, a, b in zip(*LD)]) +
        "<p>1. Write a title. 2. Put the categories (Pizza, Sushi, Tacos) along the bottom. "
        "3. Choose a scale that starts at 0 and fits the greatest number (14 fits 0 to 16, counting by 2). "
        "4. Draw two bars for each category, the same colour for the same group every time. 5. Add a legend and a source.</p>"
        "<h2>Common mistakes</h2>" +
        ltable(["Mistake", "What to do instead"], [
            ["Reading the other bar in the pair", "Check the legend colour before you read"],
            ["Counting grid lines as 1 each", "Read the numbers on the scale: a line may stand for 2, 5 or 10"],
            ["Reading the labelled step as the grid step", "Labels 0, 10, 20 with a line between them mean each line is 5"],
            ["Rounding a bar that ends between two lines", "Halfway between 10 and 12 is 11"],
            ["Adding when the question asks “how many more”", "Subtract the shorter bar from the taller bar"],
            ["Choosing a scale that is too short", "The top of the scale must be at least the greatest number"],
        ])
    )


FAQ = [
    {"q": "What do Grade 5 students learn about graphs in the BC math curriculum?",
     "a": "The BC Grade 5 curriculum includes one-to-one and many-to-one correspondence, using double bar graphs. Students read, make and compare double bar graphs where one grid line stands for 1, 2, 5, 10 or more, and draw conclusions from them."},
    {"q": "What is a double bar graph?",
     "a": "A double bar graph shows two groups side by side, with a pair of bars for each category. A legend tells which colour is which group, so you can compare the groups at a glance."},
    {"q": "What is many-to-one correspondence on a bar graph?",
     "a": "It means one grid line stands for more than one thing. If the scale counts by 5, a bar 4 lines tall shows 4 × 5 = 20. One-to-one means each line stands for 1."},
    {"q": "How do you choose a scale for a double bar graph?",
     "a": "Start at 0 and make the top at least as big as the greatest number in the table. Count by 2, 5 or 10 so the graph has about 8 to 15 lines and is easy to read."},
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
    rnd = random.Random(55815)
    sets = [set_read(), set_scale(), set_compare(), set_make(), set_concl()]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-5", "slug": "double-bar-graphs", "sort": 15,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 5 Double Bar Graphs",
        "seo_title": "Grade 5 Double Bar Graphs Worksheets: Free Math Practice with Answer Key (BC Curriculum)",
        "short_title": "Double bar graphs",
        "domain": "Data and probability",
        "standard_code": "Grade 5: Data and probability",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/5/core",
        "standard_text": "One-to-one correspondence and many-to-one correspondence, using double bar graphs",
        "meta_desc": "Free Grade 5 math worksheets on double bar graphs for the BC curriculum: reading the legend, scales of 2, 5 and 10, comparing two groups, making a double bar graph from a table, and drawing conclusions. 100 questions with an answer key.",
        "key_big": "Check the legend for the right colour, then read the scale. One grid line can stand for 1, 2, 5 or 10.",
        "key_sub": "A bar halfway between 10 and 12 shows 11, not 12. To compare, subtract the shorter bar from the taller bar in the pair.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
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
    mark_large(u, "(double bar graph)")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
