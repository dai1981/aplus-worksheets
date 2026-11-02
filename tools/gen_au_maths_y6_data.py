# -*- coding: utf-8 -*-
"""
AU Year 6 Maths: Interpreting data (Australian Curriculum v9.0: AC9M6ST01, AC9M6ST02)
  python3 tools/gen_au_maths_y6_data.py
Kinds of data (nominal, ordinal, discrete, continuous), side-by-side column graphs and dot plots, the mode and the
range, comparing two distributions (two classes' spelling scores, rainfall in Darwin and Perth, two basketball teams)
and deciding whether a claim in the media is supported (scales that do not start at 0, small and biased samples).
Rainfall: Bureau of Meteorology long-term monthly means, Darwin Airport (014015) and Perth Airport (009021),
added into seasons (summer = December to February) and rounded to the nearest 10 mm.
Wrong answers come from real student mistakes: the highest value or the frequency as the mode, the biggest number
(or last − first) as the range, reading the wrong class, judging columns by height when the scale does not start at 0,
and trusting small or biased samples.
HTML attributes use single quotes (no backslashes in the JSON). Australian English.
"""
import json, re, math, os, random
from fractions import Fraction as F
from decimal import Decimal as D

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
BAR = "#2e8b57"
BAR2 = "#e0a030"
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
    ch = [right]
    for w in wrongs:
        if plain(w) not in {plain(c) for c in ch}:
            ch.append(w)
        if len(ch) == 4:
            break
    assert len(ch) == 4, (q, right, wrongs)
    return {"q": q, "c": ch, "a": 0, "e": e}


def mcqv(q, right, wrongs, f, e, allow_zero=False):
    """Choices given as values: equal values are not allowed."""
    seen = [F(right)]
    pick = []
    for w in wrongs:
        w = F(w)
        assert w not in seen, (q, right, wrongs)
        assert w > 0 or allow_zero, (q, wrongs)
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


def line(x1, y1, x2, y2, col=INK, w=1):
    return "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%s'/>" % (x1, y1, x2, y2, col, w)


def mode_of(d):
    m = max(d.values())
    ks = [k for k, v in d.items() if v == m]
    assert len(ks) == 1, d
    return ks[0]


def rng(d):
    return max(d) - min(d)


# ------------------------------------------------------------ graphs
def dot_svg(title, axis, lo, hi, counts):
    """Dot plot: one dot for each piece of data, stacked above a number line."""
    fs = 14
    gap, r, dy = 34, 6.5, 15
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
            s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (x, yb - 9 - k * dy, r, GREEN))
    s.append(line(x0 - 12, yb, x0 + pw + 12, yb, INK, 2))
    s.append(text(W / 2, yb + 44, axis, fs, bold=True))
    assert all(lo <= k <= hi for k in counts)
    return svg_wrap(W, yb + 52, "".join(s), "dot plot: " + title.lower())


def dot2_svg(title, axis, lo, hi, groups):
    """Two dot plots on the same scale, one above the other, so the two sets of data can be compared."""
    fs = 14
    gap, r, dy = 30, 6, 13
    lab = max(tw(n, fs, True) for n, _ in groups) + 16
    pw = gap * (hi - lo)
    x0 = lab + 14
    W = max(x0 + pw + 16, tw(title, 16, True) + 16)
    s = [text(W / 2, 18, title, 16, bold=True)]
    y = 30
    for name, counts in groups:
        assert all(lo <= k <= hi for k in counts)
        mx = max(counts.values())
        yb = y + mx * dy + 8
        s.append(text(8, yb - 4, name, fs, anchor="start", bold=True))
        for v in range(lo, hi + 1):
            x = x0 + (v - lo) * gap
            s.append(line(x, yb, x, yb + 5, INK, 1.5))
            s.append(text(x, yb + 20, v, fs))
            for k in range(counts.get(v, 0)):
                s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (x, yb - 8 - k * dy, r, GREEN))
        s.append(line(x0 - 10, yb, x0 + pw + 10, yb, INK, 2))
        y = yb + 30
    s.append(text(x0 + pw / 2, y + 10, axis, fs, bold=True))
    return svg_wrap(W, y + 18, "".join(s), "dot plots: " + title.lower())


def col_svg(title, cat_axis, val_axis, cats, vals, ymin, ymax, gstep, lstep, gy=14, bw=40, slot=96):
    """Column graph. The scale runs from ymin (which may not be 0) to ymax."""
    fs = 14
    assert all(ymin <= v <= ymax for v in vals) and (ymax - ymin) % lstep == 0 and lstep % gstep == 0
    nt = (ymax - ymin) // gstep
    ph = nt * gy
    x0 = 24 + tw(ymax, fs) + 6
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
            s.append(text(x0 - 5, y + 5, num(v), fs, anchor="end"))
    for i, (c, v) in enumerate(zip(cats, vals)):
        cx = x0 + slot * i + slot / 2
        h = (v - ymin) / float(gstep) * gy
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s'/>" % (cx - bw / 2, yb - h, bw, h, BAR))
        s.append(text(cx, yb + 18, c, fs))
    s.append("<path d='M%.1f %d V%.1f H%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0 - 6, yb, x0 + pw, INK))
    s.append(text(x0 + pw / 2, yb + 38, cat_axis, fs, bold=True))
    mid = y0 + ph / 2
    s.append(text(13, mid, val_axis, fs, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % mid))
    assert tw(val_axis, fs, True) < ph + 26, (val_axis, ph)
    return svg_wrap(W, yb + 46, "".join(s), "column graph: " + title.lower())


def col2_svg(title, cat_axis, val_axis, cats, series, names, ymax, gstep, lstep, gy=12, bw=22, labels=False):
    """Side-by-side column graph: two columns for each category, with a key."""
    fs = 14
    cols = [BAR, BAR2]
    assert (ymax % lstep == 0) and lstep % gstep == 0
    for v in series:
        assert len(v) == len(cats) and all(0 <= x <= ymax for x in v)
        if not labels:
            assert all(x % gstep == 0 for x in v)
    nt = ymax // gstep
    ph = nt * gy
    x0 = 24 + tw(ymax, fs) + 6
    slot = max(2 * bw + 26, max(tw(c, fs) for c in cats) + 14)
    pw = slot * len(cats)
    y0 = 58 + (12 if labels else 0)
    yb = y0 + ph
    W = max(x0 + pw + 8, tw(title, 16, True) + 16)
    s = [text(W / 2, 18, title, 16, bold=True)]
    # key
    ws = [tw(n, fs) for n in names]
    tot = sum(ws) + 2 * 22 + 26
    kx = (W - tot) / 2
    for i, n in enumerate(names):
        s.append("<rect x='%.1f' y='31' width='14' height='14' fill='%s'/>" % (kx, cols[i]))
        s.append(text(kx + 20, 43, n, fs, anchor="start"))
        kx += 22 + ws[i] + 26
    for k in range(nt + 1):
        v = k * gstep
        y = yb - k * gy
        major = v % lstep == 0
        s.append(line(x0, y, x0 + pw, y, GRID2 if major else GRID))
        if major:
            s.append(text(x0 - 5, y + 5, num(v), fs, anchor="end"))
    for i, c in enumerate(cats):
        cx = x0 + slot * i + slot / 2
        for j, v in enumerate(series):
            x = cx - bw - 1 if j == 0 else cx + 1
            h = v[i] / float(gstep) * gy
            s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s'/>" % (x, yb - h, bw, h, cols[j]))
            if labels:
                assert tw(num(v[i]), fs) <= bw + 2
                s.append(text(x + bw / 2, yb - h - 5, num(v[i]), fs))
        s.append(text(cx, yb + 18, c, fs))
    s.append("<path d='M%.1f %d V%.1f H%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0 - 6, yb, x0 + pw, INK))
    s.append(text(x0 + pw / 2, yb + 38, cat_axis, fs, bold=True))
    mid = y0 + ph / 2
    s.append(text(13, mid, val_axis, fs, bold=True, extra=" transform='rotate(-90 13 %.1f)'" % mid))
    assert tw(val_axis, fs, True) < ph + 26, (val_axis, ph)
    return svg_wrap(W, yb + 46, "".join(s), "side-by-side column graph: " + title.lower())


# ------------------------------------------------------------ data
TRAVEL_C = ["Walk", "Bike", "Car", "Bus"]
TRAVEL = {"6A": [8, 5, 10, 3], "6B": [4, 9, 7, 6]}
DRINK_C = ["Water", "Milk", "Juice", "Hot choc"]
DRINK = {"Feb": [34, 12, 22, 4], "Jul": [16, 18, 10, 30]}
BOOKS = {1: 2, 2: 4, 3: 6, 4: 5, 5: 3, 6: 2, 9: 1}
CARS = {1: 6, 2: 9, 3: 5, 4: 3, 5: 1}
SPELL = {12: 1, 14: 2, 15: 3, 16: 5, 17: 4, 18: 3, 20: 1}
S6A = {5: 1, 6: 2, 7: 6, 8: 9, 9: 5, 10: 2}
S6B = {2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 2, 8: 3, 9: 6, 10: 3}
SEASONS = ["Summer", "Autumn", "Winter", "Spring"]
# BOM long-term mean monthly rainfall (mm): Darwin Airport 014015, Perth Airport 009021
DARWIN_M = [D("432.1"), D("372.4"), D("313.1"), D("102.4"), D("20.0"), D("1.8"),
            D("1.0"), D("4.4"), D("16.7"), D("69.7"), D("146.5"), D("255.5")]
PERTH_M = [D("10.2"), D("14.4"), D("17.1"), D("38.8"), D("95.2"), D("153.5"),
           D("152.8"), D("118.8"), D("71.8"), D("42.9"), D("25.5"), D("10.6")]


def seasons(m):
    # summer = Dec, Jan, Feb; autumn = Mar-May; winter = Jun-Aug; spring = Sep-Nov
    raw = [m[11] + m[0] + m[1], m[2] + m[3] + m[4], m[5] + m[6] + m[7], m[8] + m[9] + m[10]]
    return [int((x / 10).quantize(D("1"), rounding="ROUND_HALF_UP")) * 10 for x in raw]


DARWIN = seasons(DARWIN_M)
PERTH = seasons(PERTH_M)
assert DARWIN == [1060, 440, 10, 230] and PERTH == [40, 150, 430, 140], (DARWIN, PERTH)


def travel_svg():
    return col2_svg("How students travel to school", "Way of travel", "Students", TRAVEL_C,
                    [TRAVEL["6A"], TRAVEL["6B"]], ["6A", "6B"], 10, 1, 2, gy=13)


def drink_svg():
    return col2_svg("Drinks sold at the canteen in one week", "Drink", "Drinks sold", DRINK_C,
                    [DRINK["Feb"], DRINK["Jul"]], ["A week in February", "A week in July"], 40, 2, 10, gy=7)


def rain_svg():
    return col2_svg("Average rainfall in each season", "Season", "Rainfall (mm)", SEASONS,
                    [DARWIN, PERTH], ["Darwin", "Perth"], 1200, 100, 200, gy=13, bw=34, labels=True)


def books_svg():
    return dot_svg("Books read in Term 2: 6C", "Books read", 1, 9, BOOKS)


def cars_svg():
    return dot_svg("People in each car at school drop-off", "People in the car", 1, 5, CARS)


def spell_svg():
    return dot_svg("Spelling test scores out of 20", "Score", 12, 20, SPELL)


def scores_svg():
    return dot2_svg("Maths quiz scores out of 10", "Score", 2, 10, [("6A", S6A), ("6B", S6B)])


JUICE = (["Sunny Squeeze", "Other brands"], [52, 46])
FETE = (["2025", "2026"], [480, 510])


def juice_svg():
    return col_svg("Which juice do kids choose?", "Juice", "Kids", JUICE[0], JUICE[1], 40, 54, 2, 2, gy=17)


def fete_svg():
    return col_svg("Visitors to the school fete", "Year", "Visitors", FETE[0], FETE[1], 450, 520, 10, 10, gy=18)


# ------------------------------------------------------------ set 1: kinds of data
NOM, ORD, DIS, CON = "Nominal categorical", "Ordinal categorical", "Discrete numerical", "Continuous numerical"
KINDS = [NOM, ORD, DIS, CON]


def kind(q, right, e):
    return mcq("What kind of data is this?<br><b>%s</b>" % q, right, [k for k in KINDS if k != right], e)


def set_kinds():
    its = [
        kind("Each student’s favourite ice-cream flavour", NOM,
             "The answers are names of flavours, so the data is categorical. Flavours have no natural order, so it is nominal."),
        kind("The number of brothers and sisters each student has", DIS,
             "The answers are counted: 0, 1, 2, 3 … Counted data with only whole-number values is discrete. "
             "(Nobody has 2.5 brothers.)"),
        kind("Each student’s height in centimetres", CON,
             "Height is measured, so it can be any value in a range, such as 148.6 cm. Measured data is continuous."),
        kind("Shirt size: S, M, L or XL", ORD,
             "The answers are categories that have a natural order: S is smaller than M, M is smaller than L. "
             "They are letters, not counts, so the data is not numerical."),
        kind("The time each runner takes to run 100 m at the athletics carnival", CON,
             "Time is measured, and it can be any value, such as 15.37 seconds. So it is continuous numerical data."),
        kind("The number of goals scored in each netball game", DIS,
             "Goals are counted. You can score 12 or 13 goals but not 12.5, so the data is discrete numerical."),
        kind("How students rate the canteen’s new wrap: poor, OK, good or excellent", ORD,
             "The answers are words, so the data is categorical. Poor, OK, good, excellent have an order, so it is ordinal."),
        kind("The way each student gets to school: walk, bike, car or bus", NOM,
             "The answers are categories with no natural order, so the data is nominal categorical."),
        kind("The number on each player’s footy jumper", NOM,
             "The numbers are only names for the players. Adding them or putting them in order means nothing, "
             "so the data is nominal categorical, even though it looks like numbers."),
        kind("The mass of each student’s school bag in kilograms", CON,
             "Mass is measured, so it can be any value, such as 4.35 kg. Measured data is continuous numerical."),
        kind("The place each swimmer finishes in a race: 1st, 2nd, 3rd …", ORD,
             "The places are categories that tell the order the swimmers finished. They do not count or measure anything, "
             "so the data is ordinal categorical."),
        kind("The rainfall in Darwin each day, in millimetres", CON,
             "Rainfall is measured, and it can be any value, such as 12.4 mm. So it is continuous numerical data."),
        kind("The number of students on each school bus", DIS,
             "Students are counted, so the values are whole numbers only. The data is discrete numerical."),
        kind("The colour of each car in the school car park", NOM,
             "Colours are categories with no natural order, so the data is nominal categorical."),
        mcq("Which of these is <b>continuous</b> numerical data?", "The amount of water each student drinks in a day (mL)",
            ["The number of pets at home", "Each student’s favourite sport", "Year level: Year 4, Year 5, Year 6"],
            "Water is measured, so it can be any value in a range. Pets are counted (discrete), sports are nominal "
            "and year levels are ordinal."),
        mcq("Which of these is <b>discrete</b> numerical data?", "The number of books each student read in Term 2",
            ["The temperature at 9 am each day", "Each student’s favourite colour", "The length of each student’s hair (cm)"],
            "Books are counted in whole numbers, so the data is discrete. Temperature and length are measured "
            "(continuous), and colour is nominal."),
        mcq("Which of these is <b>ordinal</b> categorical data?", "The medal each athlete won: gold, silver or bronze",
            ["The type of pet each student has", "The number of people in each family", "The mass of each watermelon"],
            "Gold, silver and bronze are categories with an order. Pets have no order (nominal). "
            "People are counted and mass is measured, so those are numerical."),
        mcq("Which of these is <b>nominal</b> categorical data?", "The state or territory where each student was born",
            ["How much students agree: disagree, unsure, agree", "The number of cousins each student has",
             "The time each student spends reading"],
            "States and territories are categories with no natural order, so the data is nominal. "
            "Disagree, unsure, agree has an order (ordinal)."),
        mcq("Why is “the time taken to swim 50 m” continuous data?", "It is measured, so it can be any value in a range",
            ["It is counted in whole numbers", "The answers are names", "The answers are categories in order"],
            "Time is measured, not counted. A swimmer could take 48.2 s or 48.25 s, so any value in a range is possible."),
        mcq("Ruby counts the people in each car at school drop-off. She also measures how long each car stays. Which is true?",
            "People: discrete. Time: continuous",
            ["People: continuous. Time: discrete", "Both are discrete", "Both are categorical"],
            "People are counted in whole numbers (discrete). Time is measured and can be any value (continuous)."),
    ]
    return {"title": "Kinds of data: nominal, ordinal, discrete and continuous", "items": its}


# ------------------------------------------------------------ set 2: side-by-side column graphs and dot plots
def set_read():
    its = []
    S = lambda x: unit(x, "student", "students")
    A, B = TRAVEL["6A"], TRAVEL["6B"]
    f = fig(travel_svg())
    its.append(mcqv(f + "Use the key. How many students in 6B ride a bike?", B[1], [A[1], 10, 8], S,
                    "6B is the second (orange) column. The 6B column for Bike ends on the line between 8 and 10, so %d. "
                    "(%d is 6A.)" % (B[1], A[1])))
    its.append(mcqv(f + "How many students in 6A come by car?", A[2], [B[2], A[2] + B[2], 9], S,
                    "6A is the first (green) column. The 6A column for Car reaches 10. (%d is 6B, and %d is both classes.)"
                    % (B[2], A[2] + B[2])))
    its.append(mcqv(f + "How many students walk to school altogether, in both classes?", A[0] + B[0],
                    [A[0] - B[0], A[0], A[2] + B[2]], S,
                    "6A: %d walk. 6B: %d walk. Altogether means add: %d + %d = %d. (4 subtracts instead of adds.)"
                    % (A[0], B[0], A[0], B[0], A[0] + B[0])))
    its.append(mcqv(f + "How many more 6B students than 6A students ride a bike?", B[1] - A[1], [B[1] + A[1], B[1], A[1]], S,
                    "6B: %d. 6A: %d. How many more means subtract: %d − %d = %d." % (B[1], A[1], B[1], A[1], B[1] - A[1])))
    more = [TRAVEL_C[i] for i in range(4) if A[i] > B[i]]
    assert more == ["Walk", "Car"]
    its.append(mcq(f + "For which ways of travel does 6A have more students than 6B?", "Walk and car",
                   ["Bike and bus", "Car only", "Walk only"],
                   "Compare the two columns for each way. Walk: 8 and 4. Car: 10 and 7. In both, the green 6A column is taller. "
                   "For bike and bus the orange 6B column is taller."))
    its.append(mcq(f + "What is the mode for 6B?", "Bike", [str(max(B)), "Car", "Bus"],
                   "The mode is the category with the tallest column. For 6B (orange) that is Bike, with %d students. "
                   "The mode is the category, not the number %d. (Car is the mode for 6A.)" % (max(B), max(B))))
    its.append(mcqv(f + "How many students are in 6A?", sum(A), [max(A), sum(A) + sum(B), 4], S,
                    "Add all the 6A columns: %s = %d. (10 is only the tallest column.)" % (" + ".join(map(str, A)), sum(A))))
    tot = [a + b for a, b in zip(A, B)]
    assert tot.index(max(tot)) == 2 and sorted(tot)[-2] == 14
    its.append(mcq(f + "Using both classes, which way of travel is the most common?", "Car",
                   ["Bike", "Walk", "Bus"],
                   "Add the two classes. Walk 12, bike 14, car 17, bus 9. Car is the most common. "
                   "(Bike has the tallest single column, but you must add both classes.)"))
    Fb, Jl = DRINK["Feb"], DRINK["Jul"]
    f = fig(drink_svg())
    Dk = lambda x: unit(x, "drink", "drinks")
    its.append(mcqv(f + "The scale is labelled in 10s. What is each small square worth?", 2, [1, 10, 5], Dk,
                    "There are 5 small squares between 0 and 10. 10 ÷ 5 = 2, so each small square is 2 drinks."))
    its.append(mcqv(f + "How many hot chocolates were sold in the week in July?", Jl[3], [Fb[3], Jl[3] // 2, Jl[3] - 2], Dk,
                    "July is the orange column. The hot chocolate column reaches the line for 30. "
                    "(4 is February, and 15 counts each small square as 1.)"))
    its.append(mcqv(f + "How many bottles of water were sold in the week in February?", Fb[0], [32, Fb[0] // 2, Jl[0]], Dk,
                    "February is the green column. Water ends 2 small squares above 30. Each square is 2, so 30 + 4 = %d. (17 counts each small square as 1, and 16 is July.)" % Fb[0]))
    more = [DRINK_C[i] for i in range(4) if Jl[i] > Fb[i]]
    assert more == ["Milk", "Hot choc"]
    its.append(mcq(f + "Which drinks sold more in the July week than in the February week?", "Milk and hot chocolate",
                   ["Water and juice", "Hot chocolate only", "Milk only"],
                   "The orange July column is taller for milk (18 and 12) and for hot chocolate (30 and 4). "
                   "For water and juice, February is taller."))
    d = Jl[3] - Fb[3]
    its.append(mcqv(f + "How many more hot chocolates were sold in the July week than in the February week?", d,
                    [Jl[3] + Fb[3], Jl[3], d // 2], Dk,
                    "July: %d. February: %d. %d − %d = %d. Hot drinks sell more in winter, which in Australia is June to August."
                    % (Jl[3], Fb[3], Jl[3], Fb[3], d)))
    its.append(mcq(f + "What is the mode for the February week?", "Water", [str(max(Fb)), "Hot chocolate", "Juice"],
                   "The tallest green column is water (34). The mode is the drink, not the number. "
                   "(Hot chocolate is the mode for July.)"))
    f = fig(books_svg())
    n = sum(BOOKS.values())
    bk = sum(k * v for k, v in BOOKS.items())
    assert (n, bk) == (23, 84)
    its.append(mcqv(f + "Each dot is one student. How many students read 4 books?", BOOKS[4], [4, BOOKS[3], BOOKS[5]], S,
                    "Count the dots above 4: there are %d." % BOOKS[4]))
    its.append(mcqv(f + "How many students are in 6C?", n, [max(BOOKS), bk, len(BOOKS)], S,
                    "Each dot is one student, so count every dot: 2 + 4 + 6 + 5 + 3 + 2 + 1 = %d. "
                    "(%d is the number of books, and 9 is the highest value.)" % (n, bk)))
    more = sum(v for k, v in BOOKS.items() if k > 4)
    assert more == 6
    its.append(mcqv(f + "How many students read more than 4 books?", more,
                    [sum(v for k, v in BOOKS.items() if k >= 4), 4, BOOKS[5]], S,
                    "More than 4 means 5, 6 or 9 books: 3 + 2 + 1 = 6. Students who read exactly 4 do not count."))
    its.append(mcqv(f + "One value is far away from the rest. Which value is it?", 9, [6, 1, 3],
                    lambda x: unit(x, "book", "books"),
                    "The dot at 9 is on its own, with gaps at 7 and 8. All the other dots are from 1 to 6."))
    its.append(mcq(f + "What kind of data is shown in this dot plot?", DIS, [CON, NOM, ORD],
                   "The number of books is counted in whole numbers, so it is discrete numerical data."))
    mid = BOOKS[2] + BOOKS[3] + BOOKS[4] + BOOKS[5]
    assert mid == 18
    its.append(mcq(f + "Which sentence best describes the shape of the data?", "Most students read 2 to 5 books",
                   ["Most students read 9 books", "The dots are spread out evenly", "Every student read at least 2 books"],
                   "4 + 6 + 5 + 3 = 18 of the 23 students read 2, 3, 4 or 5 books. The dots are bunched in the middle, "
                   "with one far away at 9. (2 students read only 1 book.)"))
    return {"title": "Side-by-side column graphs and dot plots", "items": its}


# ------------------------------------------------------------ set 3: mode and range
def lst(v):
    return ", ".join(num(x) for x in v)


def dlist(v):
    return ", ".join(str(x) for x in v)


def set_mode_range():
    its = []
    G = lambda x: unit(x, "goal", "goals")
    g = [12, 18, 9, 12, 11, 12, 10]
    assert max(set(g), key=g.count) == 12 and g.count(12) == 3
    its.append(mcqv("Goals scored by the school netball team in 7 games:<br><b>%s</b><br>What is the mode?" % lst(g), 12,
                    [max(g), g.count(12), min(g)], G,
                    "The mode is the value that appears most often. 12 appears 3 times, so the mode is 12 goals. "
                    "(18 is the highest value, and 3 is how many times 12 appears.)"))
    its.append(mcqv("Goals scored by the school netball team in 7 games:<br><b>%s</b><br>What is the range?" % lst(g),
                    max(g) - min(g), [max(g), g[0] - g[-1], max(g) - 12], G,
                    "Range = highest − lowest = 18 − 9 = 9 goals. (18 is just the highest value, and 12 − 10 = 2 uses the "
                    "first and last numbers in the list instead of the highest and lowest. 18 − 12 = 6 uses the mode instead of the lowest value.)"))
    a = [11, 12, 11, 10, 12, 11, 13]
    its.append(mcqv("Ages of the children at a birthday party:<br><b>%s</b><br>What is the mode?" % lst(a), 11,
                    [13, 3, 12], lambda x: unit(x, "year", "years"),
                    "11 appears 3 times, more than any other age, so the mode is 11 years. "
                    "(13 is the highest age, and 3 is how many times 11 appears.)"))
    m = [31, 25, 40, 28, 36]
    its.append(mcqv("Masses of 5 dogs at the vet (kg):<br><b>%s</b><br>What is the range?" % lst(m), max(m) - min(m),
                    [max(m), m[-1] - m[0], max(m) + min(m)], lambda x: "%s kg" % num(x),
                    "Highest 40 kg, lowest 25 kg. Range = 40 − 25 = 15 kg. (36 − 31 = 5 uses the last and first numbers, "
                    "which are not the highest and lowest. 65 adds instead of subtracts.)"))
    f = fig(cars_svg())
    P = lambda x: unit(x, "person", "people")
    its.append(mcqv(f + "Each dot is one car. What is the mode?", mode_of(CARS), [CARS[2], max(CARS), 1], P,
                    "The tallest stack is above 2, so the mode is 2 people. (9 is the number of cars, and 5 is the highest value.)"))
    its.append(mcqv(f + "What is the range of the number of people in each car?", rng(CARS),
                    [max(CARS), CARS[2] - CARS[5], CARS[2]], P,
                    "Range = highest − lowest = 5 − 1 = 4 people. Use the values along the number line, "
                    "not the heights of the stacks (9 − 1 = 8)."))
    f = fig(spell_svg())
    Pt = lambda x: unit(x, "mark", "marks")
    its.append(mcqv(f + "Each dot is one student. What is the mode?", mode_of(SPELL), [SPELL[16], max(SPELL), 17], Pt,
                    "The tallest stack (5 dots) is above 16, so the mode is 16. (5 is how many students scored 16.)"))
    its.append(mcqv(f + "What is the range of the scores?", rng(SPELL), [max(SPELL), SPELL[16] - SPELL[12], max(SPELL) + min(SPELL)], Pt,
                    "Highest score 20, lowest score 12. Range = 20 − 12 = 8. "
                    "(Nobody scored 13 or 19, but the range only uses the highest and lowest. 5 − 1 = 4 uses the heights of the stacks, and 32 adds.)"))
    sh = [4, 5, 6, 5, 7, 6, 3]
    its.append(mcq("Shoe sizes of 7 students:<br><b>%s</b><br>What is the mode?" % lst(sh), "5 and 6",
                   ["5 only", "7", "There is no mode"],
                   "5 appears twice and 6 appears twice. Every other size appears once. So there are two modes: 5 and 6."))
    sc = [3, 8, 6, 9, 4]
    its.append(mcq("Quiz scores of 5 students:<br><b>%s</b><br>What is the mode?" % lst(sc), "There is no mode",
                   ["9", "5", "6"],
                   "Each score appears only once, so no value appears most often. There is no mode. "
                   "(9 is the highest score, and 5 is how many scores there are.)"))
    j = [D("2.35"), D("2.8"), D("3.1"), D("2.62"), D("2.9")]
    r = max(j) - min(j)
    assert r == D("0.75")
    its.append(mcq("Long jump distances at the athletics carnival (m):<br><b>%s</b><br>What is the range?" % dlist(j),
                   "0.75 m", ["3.1 m", "0.55 m", "0.3 m"],
                   "Highest 3.1 m, lowest 2.35 m. Line up the decimal points: 3.10 − 2.35 = 0.75 m. "
                   "(2.9 − 2.35 = 0.55 uses the last value, not the highest.)"))
    t = [-3, 1, -1, 2, -4, 0, 3]
    assert max(t) - min(t) == 7
    its.append(mcqv("Temperatures at 6 am in Canberra for one week in July (°C):<br><b>%s</b><br>What is the range?" % lst(t),
                    7, [1, 3, 4], lambda x: "%s °C" % num(x),
                    "Highest 3 °C, lowest −4 °C. From −4 up to 0 is 4 degrees, and from 0 up to 3 is 3 more: "
                    "range = 3 − (−4) = 7 °C. (4 − 3 = 1 ignores the minus sign, 3 °C is only the highest value, and 4 °C is only the size of the lowest.)"))
    vt = [("Zoo", 8), ("Beach", 11), ("Museum", 5), ("Movies", 10)]
    tb = ("<table class='sn-table'><thead><tr><th>Excursion</th><th>Votes</th></tr></thead><tbody>" +
          "".join("<tr><td>%s</td><td>%d</td></tr>" % p for p in vt) + "</tbody></table>")
    its.append(mcq("Year 6 voted for the end-of-year excursion." + tb + "What is the mode?", "Beach",
                   ["11", "Museum", "Movies"],
                   "The mode is the category with the most votes. Beach has 11 votes. The mode is Beach, not the number 11."))
    its.append(mcq("Year 6 voted for the end-of-year excursion." + tb +
                   "Isla says, “The range of this data is 11 − 5 = 6.” What is wrong?",
                   "The places are categorical, so they have no range",
                   ["Nothing: the range is 6", "The range is 11", "The range is 4 places"],
                   "The data is the place each student chose. Places are nominal categories with no order, "
                   "so there is no highest or lowest place. Range is only for numerical data."))
    sib = [(0, 5), (1, 11), (2, 7), (3, 2), (5, 1)]
    tb = ("<table class='sn-table'><thead><tr><th>Brothers and sisters</th><th>Students</th></tr></thead><tbody>" +
          "".join("<tr><td>%d</td><td>%d</td></tr>" % p for p in sib) + "</tbody></table>")
    its.append(mcqv("This table shows how many brothers and sisters the students in 6D have." + tb + "What is the mode?",
                    1, [11, 5, 2], lambda x: unit(x, "brother or sister", "brothers and sisters"),
                    "The most students (11) have 1 brother or sister, so the mode is 1. "
                    "(11 is the number of students, and 5 is the highest value.)"))
    its.append(mcqv("This table shows how many brothers and sisters the students in 6D have." + tb +
                    "What is the range of the data?", 5, [10, 4, 11], lambda x: num(x),
                    "Highest value 5, lowest value 0. Range = 5 − 0 = 5. (11 − 1 = 10 uses the student counts, "
                    "and 5 − 1 = 4 forgets that 0 is a value.)"))
    its.append(mcqv("The range of 5 test scores is 12. The lowest score is 7. What is the highest score?", 19,
                    [12, 5, 84], lambda x: num(x),
                    "Range = highest − lowest, so highest = lowest + range = 7 + 12 = 19. "
                    "(12 − 7 = 5 subtracts instead of adds, and 84 multiplies.)"))
    its.append(mcqv(fig(cars_svg()) + "One more car arrives with 3 people in it. What is the mode now?", 2,
                    [3, CARS[3] + 1, 5], lambda x: unit(x, "person", "people"),
                    "Add one dot above 3: now 6 cars have 3 people. The tallest stack is still above 2 (9 dots), "
                    "so the mode is still 2 people."))
    opts = [[4, 14, 9, 7], [10, 12, 15], [3, 10, 11], [8, 2, 5, 11]]
    rs = [max(o) - min(o) for o in opts]
    assert rs == [10, 5, 8, 9]
    its.append(mcq("Which set of data has a range of 10?", lst(opts[0]), [lst(o) for o in opts[1:]],
                   "Range = highest − lowest. 4, 14, 9, 7: 14 − 4 = 10. The others: 15 − 10 = 5, 11 − 3 = 8, 11 − 2 = 9. "
                   "(Having the number 10 in the list does not make the range 10.)"))
    h = [152, 168, 147, 175, 160, 149]
    assert max(h) - min(h) == 28
    its.append(mcqv("Heights of 6 sunflowers (cm):<br><b>%s</b><br>What is the range?" % lst(h), 28,
                    [175, h[0] - h[-1], 175 - 149], lambda x: "%s cm" % num(x),
                    "Highest 175 cm, lowest 147 cm. Range = 175 − 147 = 28 cm. "
                    "(152 − 149 = 3 uses the first and last values, and 149 is not the lowest.)"))
    return {"title": "Mode and range", "items": its}


# ------------------------------------------------------------ set 4: compare two distributions
def set_compare():
    its = []
    f = fig(scores_svg())
    Mk = lambda x: unit(x, "mark", "marks")
    assert sum(S6A.values()) == sum(S6B.values()) == 25
    its.append(mcqv(f + "Each dot is one student. What is the mode for 6A?", mode_of(S6A), [S6A[8], 10, 7], Mk,
                    "The tallest stack for 6A is above 8, so the mode is 8. (9 is how many students scored 8, "
                    "and 10 is the highest score.)"))
    its.append(mcqv(f + "What is the mode for 6B?", mode_of(S6B), [S6B[9], 10, mode_of(S6A)], Mk,
                    "The tallest stack for 6B is above 9 (6 dots), so the mode is 9. (6 is how many students scored 9.)"))
    its.append(mcqv(f + "What is the range of the 6A scores?", rng(S6A), [max(S6A), S6A[8] - S6A[5], max(S6A) + min(S6A)], Mk,
                    "6A: highest 10, lowest 5. Range = 10 − 5 = 5. (9 − 1 = 8 uses the heights of the stacks.)"))
    its.append(mcqv(f + "What is the range of the 6B scores?", rng(S6B), [max(S6B), rng(S6A), max(S6B) + min(S6B)], Mk,
                    "6B: highest 10, lowest 2. Range = 10 − 2 = 8. (5 is the range for 6A.)"))
    its.append(mcq(f + "Which class’s scores are more spread out?", "6B: its range is 8",
                   ["6A: its range is 5", "6B: it has the higher mode", "They are the same"],
                   "The range measures how spread out the data is. 6B’s range (8) is bigger than 6A’s (5). "
                   "The mode does not tell you about the spread."))
    hi_b = sum(v for k, v in S6B.items() if k >= 8)
    hi_a = sum(v for k, v in S6A.items() if k >= 8)
    assert (hi_a, hi_b) == (16, 12)
    its.append(mcqv(f + "How many students in 6B scored 8 or more?", hi_b, [S6B[9], S6B[9] + S6B[10], hi_a],
                    lambda x: unit(x, "student", "students"),
                    "8 or more means 8, 9 or 10: 3 + 6 + 3 = 12. (9 forgets the students who scored exactly 8, "
                    "and 16 is 6A.)"))
    its.append(mcq(f + "Mei says, “6B did better, because its mode is higher.” Is this supported?",
                   "No: more 6A students scored 8 or more",
                   ["Yes: 9 is higher than 8", "Yes: 6B has more scores of 10", "No: 6A has the higher mode"],
                   "One value is not enough. 16 students in 6A scored 8 or more, but only 12 in 6B. "
                   "Many 6B students scored 6 or less."))
    its.append(mcq(f + "Which sentence best compares the shapes of the data?",
                   "6A is bunched from 7 to 9; 6B is spread from 2 to 10",
                   ["6A is spread from 2 to 10; 6B is bunched from 7 to 9", "Both classes are spread out evenly",
                    "Both classes are bunched from 7 to 9"],
                   "6A: 6 + 9 + 5 = 20 of 25 dots are at 7, 8 or 9. 6B has dots all the way from 2 to 10, "
                   "with the most at 9."))
    f = fig(rain_svg())
    Mm = lambda x: "%s mm" % num(x)
    its.append(mcq(f + "Rainfall is rounded to the nearest 10 mm. Which season is the wettest in Perth?", "Winter",
                   ["Summer", "Autumn", "Spring"],
                   "Perth is the orange column. The tallest orange column is winter (430 mm). "
                   "In Australia, winter is June to August."))
    its.append(mcqv(f + "What is the average rainfall in Darwin in summer?", DARWIN[0], [PERTH[0], 1200, PERTH[2]], Mm,
                    "Darwin is the green column. The summer label says 1060 mm. (40 mm is Perth, and 1200 is the top of the scale.)"))
    its.append(mcqv(f + "What is the range of Darwin’s seasonal rainfall?", max(DARWIN) - min(DARWIN),
                    [max(DARWIN), max(DARWIN) - DARWIN[3], max(DARWIN) - min(PERTH)], Mm,
                    "Darwin: highest 1060 mm (summer), lowest 10 mm (winter). Range = 1060 − 10 = 1050 mm. (1060 − 230 = 830 does not use the lowest value, and 1060 − 40 = 1020 uses Perth’s lowest.)"))
    its.append(mcqv(f + "What is the range of Perth’s seasonal rainfall?", max(PERTH) - min(PERTH),
                    [max(PERTH), max(PERTH) - PERTH[3], max(DARWIN) - min(DARWIN)], Mm,
                    "Perth: highest 430 mm (winter), lowest 40 mm (summer). Range = 430 − 40 = 390 mm. (430 − 140 = 290 does not use the lowest value, and 1050 is Darwin’s range.)"))
    d = PERTH[2] - DARWIN[2]
    its.append(mcqv(f + "How much more rain does Perth get than Darwin in winter?", d, [PERTH[2] + DARWIN[2], PERTH[2], 1050], Mm,
                    "Winter: Perth 430 mm, Darwin 10 mm. 430 − 10 = %d mm. (440 adds instead of subtracts.)" % d))
    its.append(mcq(f + "Which sentence correctly compares the two cities?",
                   "Darwin’s rain falls mostly in summer; Perth’s mostly in winter",
                   ["Both cities get the most rain in winter", "Perth is wetter than Darwin in every season",
                    "Darwin gets about the same rain each season"],
                   "Darwin’s tallest column is summer (its wet season); its winter is almost dry. "
                   "Perth’s tallest column is winter. The shapes are opposite."))
    td, tp = sum(DARWIN), sum(PERTH)
    assert (td, tp) == (1740, 760)
    its.append(mcqv(f + "About how much more rain does Darwin get in a whole year than Perth?", td - tp,
                    [td + tp, max(DARWIN) - max(PERTH), max(DARWIN) - min(DARWIN)], Mm,
                    "Darwin: 1060 + 440 + 10 + 230 = 1740 mm. Perth: 40 + 150 + 430 + 140 = 760 mm. "
                    "1740 − 760 = 980 mm. (1060 − 430 = 630 compares only the wettest seasons.)"))
    K = [42, 38, 45, 38, 50, 39]
    W = [30, 55, 41, 55, 36, 47]
    q0 = ("Points scored by two basketball teams in 6 games:<br><b>Kookaburras: %s</b><br><b>Wombats: %s</b><br>"
          % (lst(K), lst(W)))
    assert max(set(K), key=K.count) == 38 and max(set(W), key=W.count) == 55
    its.append(mcq(q0 + "What is the mode for each team?", "Kookaburras 38, Wombats 55",
                   ["Kookaburras 50, Wombats 55", "Kookaburras 38, Wombats 30", "Kookaburras 2, Wombats 2"],
                   "Kookaburras: 38 appears twice. Wombats: 55 appears twice. "
                   "(50 is the Kookaburras’ highest score, and 2 is how many times each mode appears.)"))
    rk, rw = max(K) - min(K), max(W) - min(W)
    assert (rk, rw) == (12, 25)
    its.append(mcq(q0 + "What is the range for each team?", "Kookaburras 12, Wombats 25",
                   ["Kookaburras 50, Wombats 55", "Kookaburras 3, Wombats 17", "Kookaburras 25, Wombats 12"],
                   "Kookaburras: 50 − 38 = 12. Wombats: 55 − 30 = 25. (42 − 39 = 3 and 47 − 30 = 17 use the first and "
                   "last scores, not the highest and lowest.)"))
    its.append(mcq(q0 + "Which team’s scores are more consistent (closer together)?", "Kookaburras: smaller range",
                   ["Wombats: higher mode", "Wombats: bigger range", "Kookaburras: lower mode"],
                   "A smaller range means the scores are closer together. The Kookaburras’ range is 12 and the Wombats’ is 25."))
    sk, sw = sum(K), sum(W)
    assert (sk, sw) == (252, 264)
    its.append(mcq(q0 + "Which team scored more points altogether in the 6 games?", "Wombats, by 12 points",
                   ["Kookaburras, by 12 points", "Wombats, by 17 points", "Both scored the same"],
                   "Kookaburras: 42 + 38 + 45 + 38 + 50 + 39 = 252. Wombats: 30 + 55 + 41 + 55 + 36 + 47 = 264. "
                   "264 − 252 = 12. (55 − 38 = 17 compares the modes, not the totals.)"))
    W2 = [40 if x == 30 else x for x in W]
    assert max(W2) - min(W2) == 19
    its.append(mcqv(q0 + "If the Wombats had scored 40 instead of 30 in their first game, what would their range be?", 19,
                    [55 - 40, 25, 10], lambda x: num(x),
                    "The scores would be 40, 55, 41, 55, 36, 47. The lowest is now 36, not 40. Range = 55 − 36 = 19. (55 − 40 = 15 forgets the 36, and 10 is only the change in one score.)"))
    return {"title": "Compare two sets of data: mode, range and shape", "items": its}


# ------------------------------------------------------------ set 5: claims in the media, word problems
def set_claims():
    its = []
    f = fig(juice_svg())
    a, b = JUICE[1]
    K = lambda x: unit(x, "kid", "kids")
    its.append(mcqv(f + "A juice ad shows this graph. How many kids chose Sunny Squeeze?", a, [a - 40, b, 50], K,
                    "The Sunny Squeeze column reaches the line for 52. (12 is the height above the bottom of the scale, "
                    "which starts at 40, not 0.)"))
    its.append(mcqv(f + "How many more kids chose Sunny Squeeze than other brands?", a - b, [a + b, a - 40, b], K,
                    "52 − 46 = 6 kids. The difference is small, even though one column looks twice as tall."))
    its.append(mcq(f + "The ad says, “Twice as many kids choose Sunny Squeeze!” Is this true?",
                   "No: 52 is not twice 46",
                   ["Yes: its column is twice as tall", "Yes: 52 is more than 46", "No: more kids chose other brands"],
                   "Twice 46 is 92. Only 52 kids chose Sunny Squeeze. The column only looks twice as tall because the "
                   "scale starts at 40."))
    its.append(mcq(f + "Why does the graph make the difference look big?", "The scale starts at 40, not 0",
                   ["The columns are the same colour", "The graph has a title", "The scale goes up in 2s"],
                   "When the scale starts at 40, the bottom part of every column is cut off. The small difference "
                   "(6 kids) then looks huge."))
    its.append(mcqv(f + "To draw a fair column graph of this data, where should the scale start?", 0, [40, b, a],
                    lambda x: num(x),
                    "Column heights are only fair to compare when the scale starts at 0. Then the columns would be "
                    "52 and 46 high, and look almost the same.", allow_zero=True))
    f = fig(fete_svg())
    a, b = FETE[1]
    V = lambda x: unit(x, "visitor", "visitors")
    its.append(mcqv(f + "How many more visitors came to the school fete in 2026 than in 2025?", b - a, [a + b, b - 450, b], V,
                    "2026: 510. 2025: 480. 510 − 480 = 30 visitors. (60 is the height of the 2026 column above 450, "
                    "where the scale starts, and 510 is the number of visitors in 2026.)"))
    its.append(mcq(f + "The newsletter says, “Our fete crowd doubled in 2026!” Which is true?", "It grew by only 30 people",
                   ["It doubled from 480 to 960", "It went down by 30 people", "It grew by 510 people"],
                   "Doubling 480 would give 960 visitors, but only 510 came. The scale starts at 450, which makes the "
                   "2026 column look twice as tall."))
    its.append(mcq("A website says, “Kids love broccoli! 3 out of 4 kids we asked said yes.” They asked only 4 kids. "
                   "Why is this claim weak?", "The sample is far too small",
                   ["3 out of 4 is less than half", "Broccoli is a vegetable", "They should have asked 3 kids"],
                   "4 kids is a tiny sample. A different 4 kids could give a very different answer. "
                   "(3 out of 4 is more than half.)"))
    its.append(mcq("Which survey gives the best answer to “What is the favourite sport of the Year 6 students at our school?”",
                   "Ask every Year 6 student", ["Ask 3 friends", "Ask the netball team", "Ask students at footy training"],
                   "Asking everyone in Year 6 includes all the students. A few friends is too small a sample, "
                   "and the netball team or footy players will mostly choose their own sport."))
    its.append(mcq("A survey at the beach found that 45 of the 50 people asked love swimming. A headline says, "
                   "“90% of Australians love swimming!” What is the main problem?",
                   "People at the beach are likely to like swimming",
                   ["45 out of 50 is not 90%", "50 people is too many", "Swimming is not a sport"],
                   "The sample is biased: people at the beach were chosen, and they are more likely to enjoy swimming. "
                   "45 out of 50 is 90%, but only for those 50 people."))
    its.append(mcq("In the beach survey, 45 of the 50 people asked said they love swimming. What percentage is that?",
                   "90%", ["45%", "5%", "95%"],
                   "45 out of 50 = 90 out of 100 = 90%. (45% treats 45 out of 50 as if it were out of 100.)"))
    A, B = TRAVEL["6A"], TRAVEL["6B"]
    car, tot = A[2] + B[2], sum(A) + sum(B)
    assert (car, tot) == (17, 52)
    its.append(mcq(fig(travel_svg()) + "The principal says, “Most of our Year 6 students come to school by car.” "
                   "Is this supported by the graph?", "No: only 17 of the 52 students come by car",
                   ["Yes: car has the tallest columns", "Yes: 10 students in 6A come by car", "No: most students walk"],
                   "Car: 10 + 7 = 17 students. Altogether there are 26 + 26 = 52 students. “Most” means more than half, "
                   "and 17 is less than 26. Car is the most common way, but it is not most students."))
    its.append(mcq(fig(rain_svg()) + "A travel blog says, “Darwin is always wetter than Perth.” Is this supported?",
                   "No: Perth gets more rain in winter",
                   ["Yes: Darwin gets more rain in a year", "Yes: Darwin’s summer column is the tallest",
                    "No: Perth gets more rain in a year"],
                   "In winter Perth averages 430 mm and Darwin only 10 mm. Darwin is wetter over the whole year, "
                   "but not always."))
    its.append(mcq("A TV ad says, “9 out of 10 dog owners choose Wagz dog food.” Which question best checks this claim?",
                   "How many dog owners were asked, and how were they chosen?",
                   ["What colour is the bag?", "How much does the food cost?", "Is 9 more than 10?"],
                   "A claim like this depends on the sample. If only 10 owners were asked, or they were all at a Wagz shop, "
                   "the claim is weak."))
    Jl = DRINK["Jul"]
    its.append(mcqv(fig(drink_svg()) + "The canteen expects to sell the same number of hot chocolates each week as in "
                    "this July week. How many should it order for 10 winter weeks?", Jl[3] * 10,
                    [DRINK["Feb"][3] * 10, Jl[3], (Jl[3] - DRINK["Feb"][3]) * 10], lambda x: unit(x, "hot chocolate", "hot chocolates"),
                    "July week: 30 hot chocolates. 30 × 10 = 300. (40 uses the February week, which is summer, and 260 uses the difference between the weeks.)"))
    aw = S6A[9] + S6A[10] + S6B[9] + S6B[10]
    assert aw == 16
    its.append(mcqv(fig(scores_svg()) + "Students who score 9 or more get a merit award. How many awards are given "
                    "in the two classes altogether?", aw, [S6B[9] + S6B[10], S6A[9] + S6A[10], S6A[10] + S6B[10]],
                    lambda x: unit(x, "award", "awards"),
                    "6A: 5 + 2 = 7. 6B: 6 + 3 = 9. Altogether 7 + 9 = 16 awards."))
    its.append(mcq("Kai measured the temperature in Hobart at 3 pm on one day in July. It was 11 °C. He says, "
                   "“It is always 11 °C in Hobart in July.” Is this supported?",
                   "No: one reading is not enough data",
                   ["Yes: he measured it himself", "Yes: July is winter", "No: Hobart is warm in July"],
                   "One reading on one day cannot tell you about every day. The temperature changes during the day "
                   "and from day to day."))
    its.append(mcq("A school surveys 200 students and 50 say they walk to school. A poster says, "
                   "“Half of our students walk to school!” Is this supported?", "No: 50 out of 200 is a quarter",
                   ["Yes: 50 is half of 100", "Yes: 50 is a lot of students", "No: 50 out of 200 is 50%"],
                   "Half of 200 is 100. 50 out of 200 = 1 out of 4, which is a quarter (25%)."))
    its.append(mcq("Charlotte wants to compare the favourite sports of 6A and 6B. Which display is best?",
                   "A side-by-side column graph", ["A single dot plot", "A line graph", "A list of names"],
                   "A side-by-side column graph puts the two classes next to each other for each sport, so they are easy "
                   "to compare. Sport is categorical, so a dot plot or line graph does not fit."))
    its.append(mcq(fig(books_svg()) + "The school newsletter says, “6C students read 9 books each in Term 2.” "
                   "Is this supported?", "No: only 1 student read 9 books",
                   ["Yes: the highest value is 9", "Yes: 9 books is the mode", "No: they read 84 books each"],
                   "Only one dot is above 9. The mode is 3 books, and most students read 2 to 5 books. "
                   "84 is the total for the whole class."))
    return {"title": "Is the claim supported? Data in the media", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


L6D = {3: 1, 4: 3, 5: 5, 6: 3, 7: 1}
L6E = {1: 1, 2: 2, 4: 2, 6: 2, 7: 3, 8: 3}
LVOTE = (["Pizza", "Sushi"], [62, 54])


def body_html():
    assert mode_of(L6D) == 5 and rng(L6D) == 4 and rng(L6E) == 7
    assert sum(L6D.values()) == sum(L6E.values()) == 13
    assert (LVOTE[1][0] - 50) == 3 * (LVOTE[1][1] - 50)
    return (
        "<h2>Kinds of data</h2>"
        "<p>First decide what kind of data you have. <b>Categorical</b> data is words or labels. "
        "<b>Numerical</b> data is numbers you count or measure.</p>" +
        table(["Kind of data", "What the answers are", "Example"], [
            ["Nominal categorical", "Categories with no order", "Favourite sport, numbers on footy jumpers"],
            ["Ordinal categorical", "Categories with an order", "Shirt size S, M, L; gold, silver, bronze"],
            ["Discrete numerical", "Numbers you count (whole numbers)", "Number of pets, goals in a game"],
            ["Continuous numerical", "Numbers you measure (any value)", "Height in cm, time for 100 m"],
        ]) +
        "<h2>Mode and range</h2>"
        "<p>The <b>mode</b> is the value that appears most often. The <b>range</b> is highest value − lowest value. "
        "A small range means the data is close together. A large range means it is spread out.</p>"
        "<figure class='sn-fig'>" + dot2_svg("Laps swum in 5 minutes", "Laps", 1, 8, [("6D", L6D), ("6E", L6E)]) +
        "<figcaption>Two dot plots on the same scale make the two classes easy to compare.</figcaption></figure>" +
        ex("Example 1", "Find the mode and the range for 6D.",
           "The tallest stack is above 5, so the mode is 5 laps. Highest 7, lowest 3, so the range is 7 − 3 = 4 laps.",
           "mode 5 laps, range 4 laps") +
        ex("Example 2", "Compare the shapes of the two classes.",
           "6D is bunched in the middle (3 to 7, range 4). 6E is spread out from 1 to 8 (range 7), "
           "with the most dots at 7 and 8.",
           "6D is more consistent; 6E is more spread out") +
        "<p>To compare two sets of data, use the mode, the range and the shape: where most of the data is, "
        "any gaps, and any values far from the rest. A <b>side-by-side column graph</b> does the same job for categories: "
        "use the key to see which column belongs to which group.</p>"
        "<h2>Is the claim supported?</h2>"
        "<p>Before you believe a graph in an ad or the news, check three things. Does the scale start at 0? "
        "How many people were asked? Who was asked?</p>"
        "<figure class='sn-fig'>" + col_svg("Favourite lunch order", "Lunch", "Votes", LVOTE[0], LVOTE[1], 50, 64, 2, 2, gy=17) +
        "<figcaption>The scale starts at 50, so the pizza column looks three times as tall. "
        "Really it has only 62 − 54 = 8 votes more.</figcaption></figure>" +
        ex("Example 3", "A sign says, “Everyone loves the new playground: 100% of the kids we asked said yes!” "
           "They asked 3 kids. Is the claim supported?",
           "3 kids is far too small a sample to speak for everyone.", "No") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Giving the highest value as the mode", "The mode is the value that appears most often"],
            ["Giving the number of dots as the mode", "Give the value under the tallest stack, not the stack’s height"],
            ["Giving the biggest number as the range", "Range = highest − lowest"],
            ["Using the first and last numbers in a list", "Find the highest and lowest values first"],
            ["Judging by column heights when the scale does not start at 0", "Read the real values and subtract"],
            ["Trusting a survey of a few people, or of people chosen in one place", "Ask how many and who was asked"],
        ])
    )


FAQ = [
    {"q": "What do Year 6 students learn about data in the Australian Curriculum?",
     "a": "In Year 6 students interpret and compare data sets using side-by-side column graphs and dot plots, describe them using the mode, range and shape, and decide whether statistical claims in the media are supported."},
    {"q": "What is the difference between discrete and continuous data?",
     "a": "Discrete data is counted and has whole-number values, such as the number of pets. Continuous data is measured and can be any value in a range, such as height or time."},
    {"q": "How do you find the range of a set of data?",
     "a": "Find the highest value and the lowest value, then subtract: range = highest − lowest. Do not just use the biggest number or the first and last numbers in the list."},
    {"q": "How can a graph be misleading?",
     "a": "A column graph whose scale does not start at 0 makes small differences look big. Claims can also mislead when the sample is very small or the people asked were not chosen fairly."},
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
    rnd = random.Random(6819)
    sets = [set_kinds(), set_read(), set_mode_range(), set_compare(), set_claims()]
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
        "country": "au", "subject": "maths", "grade": "year-6", "slug": "interpreting-data", "sort": 19,
        "updated": UPDATED, "pdf_url": "",
        "title": "Interpreting Data: Comparing Data Sets, Mode, Range and Misleading Graphs",
        "seo_title": "Year 6 Interpreting Data Worksheets: Mode, Range, Dot Plots and Misleading Graphs (Free, Answer Key)",
        "short_title": "Interpreting data",
        "domain": "Statistics",
        "standard_code": "AC9M6ST01",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Interpret and compare data sets for ordinal and nominal categorical, discrete and continuous numerical variables using comparative displays or visualisations and digital tools; compare distributions in terms of mode, range and shape",
        "meta_desc": "Free Year 6 maths worksheets on interpreting data for the Australian Curriculum (AC9M6ST01, AC9M6ST02): kinds of data, side-by-side column graphs and dot plots, mode and range, comparing two data sets, and spotting misleading graphs and claims in the media. 100 questions with an answer key.",
        "key_big": "Compare data sets using the mode, the range and the shape.",
        "key_sub": "The mode is the value that appears most often. Range = highest − lowest. Before you trust a graph or a claim, check that the scale starts at 0 and ask how many people were asked, and who.",
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
        mark_large(u, "(dot plot|column graph|side-by-side)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
