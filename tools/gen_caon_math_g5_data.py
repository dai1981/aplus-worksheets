# -*- coding: utf-8 -*-
"""
CA Grade 5 Math: Data and graphs (Ontario Curriculum 2020, Grade 5: Data, D1.1, D1.2, D1.3, D1.5, D1.6)
  python3 tools/gen_caon_math_g5_data.py
Good samples, relative-frequency tables (fractions, decimals and percents), stacked-bar graphs,
the mean, median and mode, and misleading graphs and conclusions.
Wrong answers come from real student mistakes: the median taken without ordering, the highest value or the
count as the mode, dividing by the wrong number, reading the top of a stacked bar instead of the size of a part,
comparing a part with the rest instead of with the total, and judging bars by height when the scale does not start at 0.
Canadian English, Ontario number style (4536, 10 000 with a no-break space). HTML attributes use single quotes.
"""
import json, re, math, os, random
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
BAR = "#2e8b57"
BAR2 = "#e0a030"
BAR3 = "#5b8fd0"
INK = "#2b2b2b"
GRID = "#d5ddd8"
GRID2 = "#9fb0a5"
FILL2 = "#e6f2ea"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
NBSP = " "


# ------------------------------------------------------------ helpers
def num(x):
    """Ontario style: 4536, 10 000 (no-break space)."""
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


def pct(x):
    return "%s%%" % fmt(x)


def fr(n, d):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (n, d)


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


def mcqf(q, right, wrongs, e):
    """Fraction choices given as (n, d): no two may be equal in value."""
    vals = [F(n, d) for n, d in [right] + wrongs]
    assert len(set(vals)) == 4, (q, right, wrongs)
    return mcq(q, fr(*right), [fr(*w) for w in wrongs], e)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    assert "'" not in label, label
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


# ------------------------------------------------------------ figures
def table_svg(title, head, rows, label):
    fs, rh = 15, 27
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
            hd = r == 0 or k == 0
            s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, cw[k], rh, FILL2 if hd else "#ffffff", GREEN))
            s.append(text(x + cw[k] / 2, y + 19, cell, fs, bold=hd))
            x += cw[k]
    H = top + (len(rows) + 1) * rh + 4
    return svg_wrap(W, H, "".join(s), "table: " + label)


def bar_svg(title, cat_axis, val_axis, cats, vals, ymin, ymax, gstep, lstep, gy=14, bw=44, slot=110):
    """Bar graph. The scale runs from ymin (which may not be 0) to ymax."""
    fs = 14
    assert all(ymin <= v <= ymax for v in vals) and (ymax - ymin) % lstep == 0 and lstep % gstep == 0
    nt = (ymax - ymin) // gstep
    ph = nt * gy
    x0 = 24 + max(tw(num(ymax), fs), tw(num(ymin), fs)) + 6
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
    yaxis_title(s, val_axis, y0, ph)
    return svg_wrap(W, yb + 46, "".join(s), "bar graph: " + title.lower())


def stacked_svg(title, cat_axis, val_axis, cats, parts, names, ymax, gstep, lstep, gy=9, bw=46, slot=80):
    """Stacked-bar graph: each bar is split into parts (bottom part first). A key names the parts."""
    fs = 14
    cols = [BAR, BAR2, BAR3]
    assert ymax % lstep == 0 and lstep % gstep == 0 and len(parts) == len(names)
    for p in parts:
        assert len(p) == len(cats) and all(v % gstep == 0 for v in p)
    tots = [sum(p[i] for p in parts) for i in range(len(cats))]
    assert max(tots) <= ymax
    nt = ymax // gstep
    ph = nt * gy
    x0 = 24 + tw(num(ymax), fs) + 6
    slot = max(slot, max(tw(c, fs) for c in cats) + 14)
    pw = slot * len(cats)
    ws = [tw(n, fs) for n in names]
    tot = sum(ws) + len(names) * 22 + (len(names) - 1) * 18
    y0 = 58
    yb = y0 + ph
    W = max(x0 + pw + 8, tw(title, 16, True) + 16, tot + 16)
    s = [text(W / 2, 18, title, 16, bold=True)]
    kx = (W - tot) / 2
    for i, n in enumerate(names):
        s.append("<rect x='%.1f' y='30' width='15' height='15' fill='%s'/>" % (kx, cols[i]))
        s.append(text(kx + 21, 43, n, fs, anchor="start"))
        kx += 22 + ws[i] + 18
    for k in range(nt + 1):
        v = k * gstep
        y = yb - k * gy
        major = v % lstep == 0
        s.append(line(x0, y, x0 + pw, y, GRID2 if major else GRID))
        if major:
            s.append(text(x0 - 5, y + 5, num(v), fs, anchor="end"))
    for i, c in enumerate(cats):
        cx = x0 + slot * i + slot / 2
        base = 0
        for j, p in enumerate(parts):
            h = p[i] / float(gstep) * gy
            s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s' stroke='#ffffff' stroke-width='1.5'/>"
                     % (cx - bw / 2, yb - base - h, bw, h, cols[j]))
            base += h
        s.append(text(cx, yb + 18, c, fs))
    s.append("<path d='M%.1f %d V%.1f H%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0 - 6, yb, x0 + pw, INK))
    s.append(text(x0 + pw / 2, yb + 38, cat_axis, fs, bold=True))
    yaxis_title(s, val_axis, y0, ph)
    return svg_wrap(W, yb + 46, "".join(s), "stacked-bar graph: " + title.lower())


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
WIN = [("Skating", 10), ("Hockey", 6), ("Skiing", 5), ("Sledding", 4)]
WAY = [("Walk", 9), ("Bus", 6), ("Car", 4), ("Bike", 1)]
FRUIT = [("Apples", "35%"), ("Bananas", "25%"), ("Grapes", "?"), ("Oranges", "15%")]
SPIN = [("Red", 12), ("Blue", 18), ("Yellow", 10)]
CLUB_X = ["Chess", "Art", "Coding", "Choir"]
CLUB = [[6, 10, 4, 8], [8, 6, 12, 10]]
CLUB_N = ["Grade 4", "Grade 5"]
WAYS_X = ["5A", "5B", "5C"]
WAYS = [[10, 6, 12], [8, 12, 6], [6, 8, 4]]
WAYS_N = ["Walk", "Bus", "Car"]
SYR_X = ["Friday", "Saturday", "Sunday"]
SYR = [[12, 24, 20], [8, 16, 12]]
SYR_N = ["Small bottles", "Large bottles"]
SIBS = {0: 2, 1: 6, 2: 4, 3: 5, 4: 2}
CANS = (["5A", "5B"], [54, 58])


def win_svg():
    return table_svg("Favourite winter activity", ["Activity", "Students"], [[a, n] for a, n in WIN],
                     "favourite winter activity")


def way_svg():
    return table_svg("How we get to school", ["Way", "Students"], [[a, n] for a, n in WAY], "how we get to school")


def fruit_svg():
    return table_svg("Favourite fruit", ["Fruit", "Relative frequency"], [list(r) for r in FRUIT], "favourite fruit")


def spin_svg():
    return table_svg("Results of 40 spins", ["Colour", "Times"], [[a, n] for a, n in SPIN], "results of 40 spins")


def club_svg():
    return stacked_svg("Students in after-school clubs", "Club", "Students", CLUB_X, CLUB, CLUB_N, 20, 2, 4, gy=9, slot=78)


def ways_svg():
    return stacked_svg("How Grade 5 students get to school", "Class", "Students", WAYS_X, WAYS, WAYS_N, 28, 2, 4,
                       gy=9, slot=80)


def syr_svg():
    return stacked_svg("Maple syrup sold at the sugar bush", "Day", "Bottles", SYR_X, SYR, SYR_N, 40, 4, 8,
                       gy=9, slot=88)


def sibs_svg():
    return dot_svg("Number of siblings in 5B", "Number of siblings", 0, 4, SIBS)


def cans_svg():
    return bar_svg("Cans collected for the food drive", "Class", "Cans", CANS[0], CANS[1], 50, 60, 1, 2, gy=13)


# ------------------------------------------------------------ set 1: good samples
def set_samples():
    its = []
    q0 = ("Mr. Patel wants to know the favourite winter sport of all 600 students at his school. "
          "He asks 60 students chosen at random. ")
    its.append(mcq(q0 + "What is the <b>sample</b>?", "The 60 students he asks",
                   ["All 600 students", "The favourite winter sport", "Only the Grade 5 students"],
                   "The population is the whole group you want to learn about (all 600 students). "
                   "The sample is the part of the population you actually ask: the 60 students."))
    its.append(mcq(q0 + "What is the <b>population</b>?", "All 600 students at the school",
                   ["The 60 students he asks", "The students who like hockey", "Mr. Patel’s class"],
                   "The population is everyone the question is about: all 600 students at the school. "
                   "The 60 students are only the sample."))
    its.append(mcq("Which sample is best for finding the favourite lunch of all the students at a school (Kindergarten to Grade 8)?",
                   "20 students chosen at random from every grade",
                   ["20 students in the Grade 1 class", "20 students on the soccer team", "20 of Maya’s friends"],
                   "A good sample is like the whole population. Choosing students at random from every grade gives "
                   "every student a fair chance. The other samples leave out most grades or most students."))
    its.append(mcq("Which question is fair and does not push people to one answer?", "What is your favourite season?",
                   ["Don’t you agree winter is the best season?", "Isn’t summer more fun than winter?",
                    "Winter is cold and dark. Do you like it?"],
                   "A fair survey question does not suggest an answer. The other three questions tell people "
                   "which answer the asker wants."))
    its.append(mcq("Which is a random way to choose 30 students from the whole school?",
                   "Draw 30 names from a hat with every name",
                   ["Ask the first 30 students at the door", "Ask 30 students in the chess club", "Ask 30 students who volunteer"],
                   "In a random sample, every student has the same chance to be chosen. Drawing names from a hat "
                   "that holds every student’s name does this. The other ways favour some students."))
    its.append(mcq("Kai wants to know how long an ice cube takes to melt on a sunny windowsill. How should he collect the data?",
                   "Do an experiment and time it",
                   ["Survey the students in his class", "Ask one friend to guess", "Look up a bar graph about snow"],
                   "The data comes from watching what happens, so Kai should do an experiment: put ice cubes on the "
                   "windowsill and time how long they take to melt."))
    its.append(mcq("Priya wants to know which birds visit the bird feeder outside her classroom. What is the best way to collect the data?",
                   "Watch the feeder and record each bird",
                   ["Survey the students in her class", "Ask one friend which bird is best", "Count the birds in a book"],
                   "This data comes from observation. Priya should watch the feeder at different times and "
                   "record each bird she sees, for example in a tally chart."))
    its.append(mcq("Owen wants to know how the students at his school get to school. He asks only the students on one school bus. "
                   "What is the problem?", "Everyone he asks takes the bus",
                   ["The sample is too big", "He should ask teachers instead", "Bus riders cannot answer surveys"],
                   "The sample is biased: every student on a bus will say “bus”. Students who walk, bike or come by car "
                   "are left out, so the results will not match the whole school."))
    its.append(mcq("Chloe asks 3 students what the school should buy for recess. Why is this sample too small?",
                   "3 students may not be typical",
                   ["3 is an odd number", "3 students is too many", "Small samples are always random"],
                   "With only 3 students, a few unusual answers can change the result a lot. A larger sample "
                   "chosen at random is more likely to match the whole school."))
    its.append(mcq("Ethan wants to find the favourite pizza topping of the Grade 5 students. Which sample is <b>biased</b>?",
                   "Students in line for pepperoni pizza",
                   ["Every 4th student on the class lists", "Names drawn from a hat", "5 students chosen at random from each class"],
                   "Students in line for pepperoni pizza probably like pepperoni, so they would push the results "
                   "toward pepperoni. The other three ways choose students fairly."))
    its.append(mcq("Are the 28 students in class 5B a good sample to learn the bedtime of all the students from Kindergarten to Grade 8?",
                   "No: the sample has only Grade 5 students",
                   ["Yes: 28 is a big number", "Yes: they are all students", "No: 28 students is too many"],
                   "Younger students usually go to bed earlier and older students later. A sample from one Grade 5 "
                   "class does not represent every grade."))
    its.append(mcq("Two random samples were taken at the same school. Sample A asked 10 students. Sample B asked 100 students. "
                   "Which result can you trust more?", "Sample B: it asked more students",
                   ["Sample A: it asked fewer students", "They are equally good", "Neither: samples never work"],
                   "When both samples are random, the larger one is more likely to be close to the whole population. "
                   "A few unusual answers matter less in a big sample."))
    its.append(mcqf("Leah surveys 25 of the 100 Grade 5 students at her school, chosen at random. "
                    "What fraction of the population is in her sample?", (1, 4), [(1, 25), (3, 4), (1, 100)],
                    "25 out of 100 is " + fr(25, 100) + " = " + fr(1, 4) + ". (" + fr(3, 4) + " is the part she did not ask.)"))
    its.append(mcqf("In a random sample of 20 students, 8 chose skating as their favourite winter activity. "
                    "What fraction of all the students would you expect to choose skating?", (2, 5), [(3, 5), (2, 3), (1, 8)],
                    "8 out of 20 is " + fr(8, 20) + " = " + fr(2, 5) + ". A random sample should be close to the whole "
                    "population. (" + fr(2, 3) + " compares 8 with the other 12 students instead of with all 20.)"))
    its.append(mcqv("In a random sample of 25 students, 15 like hockey. What percent of the sample likes hockey?",
                    60, [15, 40, 10], pct,
                    "15 out of 25 = " + fr(15, 25) + " = " + fr(60, 100) + " = 60%. (15% uses the count as a percent, "
                    "and 40% is the part who do not like hockey.)"))
    its.append(mcq("A survey at a library asked 40 people about their favourite hobby. 30 of them said reading. "
                   "Can you say that " + fr(3, 4) + " of the whole town likes reading best?",
                   "No: people at a library likely like reading",
                   ["Yes: 30 out of 40 is " + fr(3, 4), "Yes: 40 people is a big sample", "No: 30 out of 40 is not " + fr(3, 4)],
                   "30 out of 40 is " + fr(3, 4) + ", but only for people at the library. People who visit a library "
                   "are more likely to enjoy reading, so the sample is biased."))
    its.append(mcqv("In a random sample of 50 students, 10 walk to school. The school has 500 students. "
                    "About how many students at the school walk?", 100, [10, 50, 490],
                    lambda x: unit(x, "student", "students"),
                    "10 out of 50 is " + fr(1, 5) + ". " + fr(1, 5) + " of 500 is 500 ÷ 5 = 100 students. "
                    "(10 is only the walkers in the sample, and 490 subtracts 10 from 500.)"))
    its.append(mcqv("In a random sample of 40 Grade 5 students, 10 play ringette. There are 160 Grade 5 students in all. "
                    "About how many of them play ringette?", 40, [10, 16, 150],
                    lambda x: unit(x, "student", "students"),
                    "10 out of 40 is " + fr(1, 4) + ". " + fr(1, 4) + " of 160 is 160 ÷ 4 = 40 students. "
                    "(16 is 10% of 160, and 150 subtracts 10 from 160.)"))
    its.append(mcq("Hana asked 5 of her friends what the school should buy for recess. All 5 said a basketball. "
                   "How can she make her survey better?", "Ask more students, chosen at random",
                   ["Ask the same 5 friends again", "Ask only her best friend", "Ask 5 friends from her team"],
                   "Her friends may like the same things she does, and 5 is a small sample. "
                   "More students chosen at random will give a fairer result."))
    its.append(mcq("A town asks 200 people at a skating rink, “Should the town build a new skating rink?” "
                   "180 say yes. Which is the best conclusion?", "The town needs a fairer sample first",
                   ["90% of the town wants a new rink", "Almost nobody wants a new rink", "200 people is too small"],
                   "180 out of 200 is 90%, but only for people at a rink, who like skating. People who do not skate "
                   "were not asked, so the town cannot say 90% of everyone wants a rink."))
    return {"title": "Good samples", "items": its}


# ------------------------------------------------------------ set 2: relative-frequency tables
def set_relfreq():
    its = []
    tot = sum(n for _, n in WIN)
    assert tot == 25
    f = fig(win_svg())
    its.append(mcqv(f + "How many students were surveyed?", 25, [10, 4, 15], lambda x: unit(x, "student", "students"),
                    "Add the numbers in the table: 10 + 6 + 5 + 4 = 25 students. "
                    "(10 is only skating, and 4 is the number of activities.)"))
    its.append(mcq("The relative frequency of “cat” in a pet survey is " + fr(3, 10) + ". Which shows the same amount?",
                   "0.3 and 30%", ["0.03 and 3%", "0.3 and 3%", "3.10 and 310%"],
                   fr(3, 10) + " is 3 tenths, which is 0.3. 3 tenths = 30 hundredths = 30%."))
    its.append(mcq(f + "What is the relative frequency of skating as a fraction?", fr(10, 25),
                   [fr(10, 15), fr(1, 10), fr(25, 10)],
                   "Relative frequency = students who chose skating ÷ all the students = " + fr(10, 25) + ". "
                   "(" + fr(10, 15) + " compares skating with the other 15 students, not with all 25.)"))
    assert F(6, 25) == F("0.24")
    its.append(mcqv(f + "What is the relative frequency of hockey as a decimal?", F("0.24"), [F("0.6"), F("0.06"), F("0.4")],
                    fmt,
                    "6 out of 25 is " + fr(6, 25) + " = " + fr(24, 100) + " = 0.24. (0.6 means 6 tenths, not 6 out of 25, "
                    "and 0.4 is skating.)"))
    its.append(mcqv(f + "What percent of the students chose skiing?", 20, [5, 25, 80], pct,
                    "5 out of 25 is " + fr(5, 25) + " = " + fr(20, 100) + " = 20%. (5% uses the count as a percent, "
                    "and 80% is the students who did not choose skiing.)"))
    its.append(mcq(f + "Which activity has a relative frequency of 0.16?", "Sledding", ["Skating", "Hockey", "Skiing"],
                   "0.16 = " + fr(16, 100) + " = " + fr(4, 25) + ". 4 students chose sledding."))
    its.append(mcq(f + "What do the relative frequencies of all four activities add up to?", "1 whole (100%)",
                   ["25", "4", "10"],
                   fr(10, 25) + " + " + fr(6, 25) + " + " + fr(5, 25) + " + " + fr(4, 25) + " = " + fr(25, 25) + " = 1. "
                   "The relative frequencies of all the parts always add to 1 whole, or 100%."))
    f = fig(way_svg())
    assert sum(n for _, n in WAY) == 20
    its.append(mcqv(f + "20 students were surveyed. What percent of them walk?", 45, [9, 20, 55], pct,
                    "9 out of 20 is " + fr(9, 20) + " = " + fr(45, 100) + " = 45%. (9% uses the count, "
                    "and 55% is the students who do not walk.)"))
    its.append(mcqf(f + "What fraction of the 20 students come by car?", (1, 5), [(1, 4), (1, 20), (4, 5)],
                    "4 out of 20 is " + fr(4, 20) + " = " + fr(1, 5) + ". (" + fr(1, 4) + " compares the 4 car riders "
                    "with the other 16 students.)"))
    its.append(mcqv(f + "What is the relative frequency of “Bike” as a decimal?", F("0.05"), [F("0.5"), F("0.2"), F("0.01")],
                    fmt,
                    "1 out of 20 is " + fr(1, 20) + " = " + fr(5, 100) + " = 0.05. (0.5 is 1 out of 2, "
                    "and 0.2 is car.)"))
    its.append(mcq(f + "Which is greater: the relative frequency of “Walk” or " + fr(1, 2) + "?",
                   fr(1, 2) + ": 45% is less than 50%",
                   ["Walk: 9 is more than 2", "They are equal", "Walk: 45 is more than 1"],
                   "Walk is 9 out of 20 = 45%, and " + fr(1, 2) + " = 50%. 45% &lt; 50%, so fewer than half "
                   "of the students walk."))
    f = fig(fruit_svg())
    its.append(mcqv(f + "One relative frequency is missing. What percent chose grapes?", 25, [75, 40, 35], pct,
                    "All the parts add to 100%. 35% + 25% + 15% = 75%, so grapes = 100% − 75% = 25%. "
                    "(75% is the total of the others, and 40% forgets oranges.)"))
    assert F(35, 100) * 20 == 7
    its.append(mcqv(f + "20 students were surveyed. How many chose apples?", 7, [35, 13, 20],
                    lambda x: unit(x, "student", "students"),
                    "35% = " + fr(35, 100) + " = " + fr(7, 20) + ", so 7 of the 20 students chose apples. "
                    "(35 is the percent, not the number of students, and 13 is the students who did not choose apples.)"))
    f = fig(spin_svg())
    its.append(mcqv(f + "What is the relative frequency of blue as a decimal?", F("0.45"), [F("0.18"), F("0.55"), F("0.4")],
                    fmt,
                    "18 out of 40 is " + fr(18, 40) + " = " + fr(45, 100) + " = 0.45. (0.18 uses the count as hundredths, "
                    "and 0.55 is the spins that were not blue.)"))
    its.append(mcq(f + "Which colour came up " + fr(1, 4) + " of the time?", "Yellow", ["Red", "Blue", "None of them"],
                   fr(1, 4) + " of 40 spins is 40 ÷ 4 = 10 spins. Yellow came up 10 times."))
    its.append(mcq(f + "Which shows the relative frequency of red in three ways?",
                   fr(3, 10) + " = 0.3 = 30%",
                   [fr(12, 40) + " = 0.12 = 12%", fr(3, 10) + " = 0.03 = 3%", fr(3, 10) + " = 0.3 = 3%"],
                   "12 out of 40 = " + fr(12, 40) + " = " + fr(3, 10) + " = 0.3 = 30%. (12% uses the count, not the "
                   "fraction of 40.)"))
    its.append(mcqv("In a class survey, 6 students chose basketball. The relative frequency of basketball is "
                    + fr(1, 4) + ". How many students were surveyed?", 24, [10, 18, 4],
                    lambda x: unit(x, "student", "students"),
                    "6 is " + fr(1, 4) + " of the class, so the class is 4 × 6 = 24 students. (10 adds 6 and 4, "
                    "and 18 is the students who did not choose basketball.)"))
    its.append(mcqv("At a Canada Day picnic, 50 people chose an ice cream flavour. The relative frequency of maple is 0.6. "
                    "How many people chose maple?", 30, [6, 20, 60], lambda x: unit(x, "person", "people"),
                    "0.6 = " + fr(6, 10) + ". " + fr(1, 10) + " of 50 is 5, so " + fr(6, 10) + " of 50 is 6 × 5 = 30 people. "
                    "(6 reads the decimal as a count, and 20 is the people who did not choose maple.)"))
    assert F(16, 32) == F(1, 2) and F(15, 25) == F(3, 5)
    its.append(mcq("In class 5A, 16 of 32 students play hockey. In class 5B, 15 of 25 students play hockey. "
                   "Which class has the greater relative frequency of hockey players?", "5B: 60% vs 50%",
                   ["5A: 16 is more than 15", "They are the same", "5A: 60% vs 50%"],
                   "5A: " + fr(16, 32) + " = " + fr(1, 2) + " = 50%. 5B: " + fr(15, 25) + " = " + fr(3, 5) + " = 60%. "
                   "Compare the parts of each class, not the counts, because the classes are different sizes."))
    v = [F("0.35"), F("0.25"), F("0.3"), F("0.2")]
    assert sum(v) == F("1.1")
    its.append(mcq("Mateo’s relative-frequency table shows 0.35, 0.25, 0.3 and 0.2 for four choices. What is wrong?",
                   "They add to more than 1", ["0.2 is too small", "Decimals cannot be used", "Nothing is wrong"],
                   "0.35 + 0.25 + 0.3 + 0.2 = 1.1. The relative frequencies of all the choices must add to exactly 1, "
                   "so at least one of them is wrong."))
    return {"title": "Relative-frequency tables", "items": its}


# ------------------------------------------------------------ set 3: stacked-bar graphs
def set_stacked():
    its = []
    S = lambda x: unit(x, "student", "students")
    g4, g5 = CLUB
    f = fig(club_svg())
    its.append(mcqv(f + "How many Grade 5 students are in the Art club?", g5[1], [g4[1] + g5[1], g4[1], 8], S,
                    "The Grade 5 part of the Art bar goes from 10 up to 16. 16 − 10 = 6 students. "
                    "(16 is the top of the bar: all the Art students.)"))
    its.append(mcqv(f + "How many students are in the Coding club altogether?", g4[2] + g5[2],
                    [g5[2], g4[2], g4[2] + g5[2] + g5[2]], S,
                    "The top of the Coding bar is at 16, so 16 students are in the club: 4 in Grade 4 and 12 in Grade 5."))
    its.append(mcq(f + "Which club has the most Grade 5 students?", "Coding", ["Choir", "Chess", "Art"],
                   "Compare the sizes of the Grade 5 (orange) parts, not the heights of the bars. Coding: 16 − 4 = 12. "
                   "Choir: 18 − 8 = 10. Chess: 14 − 6 = 8. Art: 16 − 10 = 6. (Choir has the tallest bar, but not the "
                   "most Grade 5 students.)"))
    its.append(mcqv(f + "How many Grade 4 students are in the Chess club?", g4[0], [g5[0], g4[0] + g5[0], 4], S,
                    "The Grade 4 part is at the bottom. In the Chess bar it goes from 0 up to 6, so 6 students."))
    its.append(mcqv(f + "In the Coding club, how many more Grade 5 students are there than Grade 4 students?",
                    g5[2] - g4[2], [g5[2], g4[2] + g5[2], g4[2]], S,
                    "Grade 5: 16 − 4 = 12. Grade 4: 4. 12 − 4 = 8 more. (12 is the number of Grade 5 students, "
                    "not the difference.)"))
    assert sum(g4) == 28 and sum(g5) == 36
    its.append(mcqv(f + "How many Grade 4 students are in clubs altogether?", sum(g4), [sum(g4) + sum(g5), sum(g5), 18], S,
                    "Add the green parts: 6 + 10 + 4 + 8 = 28. (36 adds the orange Grade 5 parts, and 64 is "
                    "all the students.)"))
    w, b, c = WAYS
    f = fig(ways_svg())
    its.append(mcqv(f + "How many students in 5B take the bus?", b[1], [w[1] + b[1], w[1], w[1] + b[1] + c[1]], S,
                    "The bus part of the 5B bar goes from 6 up to 18. 18 − 6 = 12 students. "
                    "(18 is where the bus part ends, not its size.)"))
    tots = [w[i] + b[i] + c[i] for i in range(3)]
    assert tots == [24, 26, 22]
    its.append(mcq(f + "Which class has the most students?", "5B", ["5A", "5C", "They are all the same"],
                   "The total for each class is the top of its bar: 5A has 24, 5B has 26 and 5C has 22."))
    its.append(mcqv(f + "In 5C, how many students walk or take the bus?", w[2] + b[2], [tots[2], b[2], c[2] + b[2]], S,
                    "In 5C, walk is 12 and bus goes from 12 to 18, which is 6. 12 + 6 = 18. "
                    "(22 is the whole class, including the 4 students who come by car.)"))
    assert F(10, 24) == F(5, 12)
    its.append(mcqf(f + "In 5A, what fraction of the students walk?", (5, 12), [(5, 7), (1, 3), (1, 10)],
                    "5A has 24 students and 10 of them walk: " + fr(10, 24) + " = " + fr(5, 12) + ". "
                    "(" + fr(5, 7) + " compares the 10 walkers with the other 14 students, not with all 24.)"))
    its.append(mcqv(f + "How many students in the three classes take the bus?", sum(b), [b[1], sum(tots), sum(w)], S,
                    "Bus parts: 5A 8, 5B 12, 5C 6. 8 + 12 + 6 = 26. (28 adds the walk parts, and 72 is all the students.)"))
    its.append(mcq(f + "Which statement is true?", "5C has the most students who walk",
                   ["5B has the most students who walk", "5A has the fewest car riders", "Every class has more bus riders than walkers"],
                   "Walk parts: 5A 10, 5B 6, 5C 12, so 5C has the most. 5C has the fewest car riders (4), "
                   "and in 5A and 5C more students walk than take the bus."))
    sm, lg = SYR
    f = fig(syr_svg())
    B = lambda x: unit(x, "bottle", "bottles")
    its.append(mcqv(f + "How many large bottles were sold on Saturday?", lg[1], [sm[1] + lg[1], sm[1], 8], B,
                    "The large part of the Saturday bar goes from 24 up to 40. 40 − 24 = 16 bottles. "
                    "(40 is all the bottles sold on Saturday.)"))
    its.append(mcqv(f + "How many small bottles were sold on Sunday?", sm[2], [sm[2] + lg[2], lg[2], 24], B,
                    "The small part is at the bottom. On Sunday it goes from 0 up to 20, so 20 bottles."))
    assert sum(sm) + sum(lg) == 92 and sum(sm) == 56 and sum(lg) == 36
    its.append(mcqv(f + "How many bottles were sold altogether over the three days?", 92, [40, sum(sm), sum(lg)], B,
                    "Read the top of each bar: 20 + 40 + 32 = 92 bottles. (40 is only Saturday, "
                    "and 56 is only the small bottles.)"))
    assert [a - z for a, z in zip(sm, lg)] == [4, 8, 8]
    its.append(mcq(f + "On which day was the difference between small and large bottles sold the smallest?", "Friday",
                   ["Saturday", "Sunday", "They are all the same"],
                   "Friday: 12 − 8 = 4. Saturday: 24 − 16 = 8. Sunday: 20 − 12 = 8. The difference was smallest on Friday."))
    its.append(mcqv(f + "Large bottles cost $15 each. How much money did the large bottles bring in on Friday?",
                    8 * 15, [20 * 15, 12 * 15, 8 + 15], lambda x: "$" + num(x),
                    "On Friday, the large part goes from 12 up to 20, so 8 large bottles were sold. "
                    "8 × $15 = $120. ($300 uses all 20 bottles sold on Friday.)"))
    assert F(10, 18) == F(5, 9)
    its.append(mcqf(fig(club_svg()) + "What fraction of the Choir club is in Grade 5?", (5, 9), [(4, 9), (5, 4), (1, 2)],
                    "Choir has 18 students. The Grade 5 part goes from 8 to 18, so 10 students. "
                    + fr(10, 18) + " = " + fr(5, 9) + ". (" + fr(4, 9) + " is the Grade 4 part.)"))
    its.append(mcqv("In a stacked-bar graph, the bottom part of a bar goes up to 7 and the top part goes up to 12. "
                    "How big is the top part?", 5, [12, 19, 7], num,
                    "The top part starts where the bottom part ends. It goes from 7 to 12, so it is 12 − 7 = 5. "
                    "(12 is the whole bar, and 19 adds 7 and 12.)"))
    its.append(mcq("Why would you choose a stacked-bar graph instead of a simple bar graph?",
                   "It shows the parts and the total in one bar",
                   ["It only shows the total", "It shows the mode", "It does not need a scale"],
                   "Each bar of a stacked-bar graph is split into parts. The parts show the groups, and the top of the "
                   "bar shows the total. A key tells you which colour is which part."))
    return {"title": "Stacked-bar graphs", "items": its}


# ------------------------------------------------------------ set 4: mean, median and mode
def e_sort(v):
    return "In order: %s." % lst(sorted(v))


def set_mmm():
    its = []
    v = [3, 1, 4, 1, 6, 1, 2]
    assert modes(v) == [1] and median(v) == 2
    its.append(mcqv("Goals scored by a ringette team in 7 games:<br><b>%s</b><br>What is the mode?" % lst(v), 1,
                    [6, 3, 2], lambda x: unit(x, "goal", "goals"),
                    "The mode is the value that appears most often. 1 appears 3 times, so the mode is 1 goal. "
                    "(6 is the highest value, 3 is how many times 1 appears, and 2 is the median.)"))
    v = [12, 7, 15, 9, 20]
    assert median(v) == 12 and mean(v) == F("12.6")
    its.append(mcqv("Minutes that 5 students spent reading:<br><b>%s</b><br>What is the median?" % lst(v), 12,
                    [15, 20, F("12.6")], lambda x: unit(x, "minute", "minutes"),
                    e_sort(v) + " The middle value is 12. (15 is the middle of the list before it was put in order, "
                    "and 12.6 is the mean.)"))
    v = [2, 9, 4, 5]
    assert mean(v) == 5 and median(v) == F("4.5")
    its.append(mcqv("Cans collected by 4 students for the food drive:<br><b>%s</b><br>What is the mean?" % lst(v), 5,
                    [20, F("4.5"), 4], lambda x: unit(x, "can", "cans"),
                    "Add: 2 + 9 + 4 + 5 = 20. Share 20 equally among 4 students: 20 ÷ 4 = 5 cans. "
                    "(20 is the total, 4.5 is the median, and 4 divides by 5.)"))
    v = [8, 3, 6, 10, 5]
    assert modes(v) == []
    its.append(mcq("Quiz scores out of 10:<br><b>%s</b><br>What is the mode?" % lst(v), "There is no mode",
                   ["10", "5", "0"],
                   "Each score appears only once, so no value appears most often. There is no mode. "
                   "(10 is the highest score, and 5 is how many scores there are.)"))
    v = [2, 4, 4, 6, 7, 7, 9]
    assert modes(v) == [4, 7]
    its.append(mcq("Points scored by a basketball player in 7 games:<br><b>%s</b><br>What is the mode?" % lst(v),
                   "4 and 7", ["7 only", "9", "There is no mode"],
                   "4 appears twice and 7 appears twice. Every other value appears once. So there are two modes: 4 and 7."))
    v = [6, 10, 3, 8]
    assert median(v) == 7 and mean(v) == F("6.75")
    its.append(mcqv("Laps skated by 4 students:<br><b>%s</b><br>What is the median?" % lst(v), 7,
                    [F("6.5"), 14, 8], lambda x: unit(x, "lap", "laps"),
                    e_sort(v) + " With 4 values there are two middle values, 6 and 8. "
                    "The median is halfway between them: (6 + 8) ÷ 2 = 7. (6.5 uses 10 and 3 from the list before it "
                    "was put in order, and 14 forgets to divide by 2.)"))
    f = fig(sibs_svg())
    vals = [k for k, n in SIBS.items() for _ in range(n)]
    assert len(vals) == 19 and modes(vals) == [1] and median(vals) == 2
    its.append(mcqv(f + "Each X is one student. What is the mode?", 1, [6, 4, 2], lambda x: unit(x, "sibling", "siblings"),
                    "The tallest stack is above 1, so the mode is 1 sibling. (6 is the height of that stack, "
                    "and 4 is the highest value.)"))
    its.append(mcqv(f + "What is the median number of siblings?", 2, [1, 3, 10], lambda x: unit(x, "sibling", "siblings"),
                    "There are 19 X’s, so the median is the 10th value in order. Count from the left: 2 students have 0, "
                    "the next 6 have 1 (that makes 8), and the next 4 have 2. The 10th value is 2. "
                    "(1 is the mode, and 10 is the position of the median, not its value.)"))
    its.append(mcq("A shoe store looks at the sizes it sold in one day. What does the <b>mode</b> tell the store?",
                   "The size sold most often", ["The middle size", "The size if all were shared equally", "The biggest size"],
                   "The mode is the value that appears most often, so it tells the store which size to keep the most of."))
    v = [F("3.5"), F("4.0"), F("3.5"), F("4.5"), F("3.0")]
    assert modes(v) == [F("3.5")] and mean(v) == F("3.7")
    its.append(mcqv("Hours that Mei practised piano each week:<br><b>3.5, 4.0, 3.5, 4.5, 3.0</b><br>What is the mode?",
                    F("3.5"), [F("4.5"), 2, F("3.7")], lambda x: unit(x, "hour", "hours"),
                    "3.5 appears twice and every other value once, so the mode is 3.5 hours. "
                    "(4.5 is the highest, 2 is how many times 3.5 appears, and 3.7 is the mean.)"))
    v = [F("9.8"), F("10.4"), F("9.5"), F("11.2"), F("10.1")]
    assert median(v) == F("10.1") and mean(v) == F("10.2")
    its.append(mcqv("Times for 5 swimmers in a race (seconds):<br><b>%s</b><br>What is the median?" % lst(v), F("10.1"),
                    [F("9.5"), F("10.2"), F("11.2")], lambda x: "%s s" % fmt(x),
                    e_sort(v) + " The middle value is 10.1 s. (9.5 is the middle of the list before it was put in order, "
                    "10.2 is the mean, and 11.2 is the slowest time.)"))
    v = [F("1.2"), F("2.7"), F("1.5"), F("2.4"), F("1.7")]
    assert mean(v) == F("1.9") and median(v) == F("1.7") and sum(v) == F("9.5")
    its.append(mcqv("Lengths of 5 pieces of ribbon (m):<br><b>%s</b><br>What is the mean?" % lst(v), F("1.9"),
                    [F("9.5"), F("1.7"), F("1.5")], lambda x: "%s m" % fmt(x),
                    "Add: 1.2 + 2.7 + 1.5 + 2.4 + 1.7 = 9.5. Divide by 5 pieces: 9.5 ÷ 5 = 1.9 m. "
                    "(9.5 is the total, 1.7 is the median, and 1.5 is the middle of the list before it was put in order.)"))
    v = [0, 5, 0, 7, 3]
    assert mean(v) == 3 and F(15, 3) == 5
    its.append(mcqv("Centimetres of snow that fell each day for 5 days:<br><b>%s</b><br>What is the mean?" % lst(v), 3,
                    [5, 15, 7], lambda x: "%s cm" % fmt(x),
                    "Add: 0 + 5 + 0 + 7 + 3 = 15. There are 5 days, including the 2 days with 0 cm: 15 ÷ 5 = 3 cm. "
                    "(5 leaves out the zeros and divides by 3.)"))
    v = [F("4.50"), F("5.25"), F("3.75"), F("6.50")]
    assert mean(v) == 5
    its.append(mcq("Allowance Jayden got each week for 4 weeks:<br><b>%s</b><br>What is the mean?"
                   % ", ".join(money(x) for x in v), "$5.00", ["$20.00", "$4.00", "$6.50"],
                   "Add: $4.50 + $5.25 + $3.75 + $6.50 = $20.00. Share it equally over 4 weeks: $20.00 ÷ 4 = $5.00. "
                   "($4.00 divides by 5, and $6.50 is the highest amount.)"))
    its.append(mcq("Which data set has a mean of 6?", "5, 7, 4, 8", ["6, 6, 9", "2, 6, 9", "6, 10, 11"],
                   "5 + 7 + 4 + 8 = 24 and 24 ÷ 4 = 6. The others: 21 ÷ 3 = 7, 17 ÷ 3 is less than 6, and 27 ÷ 3 = 9. "
                   "(6, 6, 9 has a mode of 6, and 2, 6, 9 has a median of 6, but not a mean of 6.)"))
    v = [F("2.6"), F("3.1"), F("2.2"), F("2.8"), F("2.4"), F("3.0")]
    assert median(v) == F("2.7")
    its.append(mcqv("Long-jump distances for 6 students (m):<br><b>%s</b><br>What is the median?" % ", ".join("%.1f" % float(x) for x in v), F("2.7"),
                    [F("2.5"), F("5.4"), F("2.8")], lambda x: "%s m" % fmt(x),
                    "In order: 2.2, 2.4, 2.6, 2.8, 3.0, 3.1. The two middle values are 2.6 and 2.8. Halfway between them is 2.7 m. "
                    "(2.5 uses 2.2 and 2.8 from the list before it was put in order, and 5.4 forgets to divide by 2.)"))
    v = [8, 9, 10, 9, 39]
    assert mean(v) == 15 and median(v) == 9 and sum(v) == 75
    its.append(mcq("Cups of hot chocolate sold at the rink each day:<br><b>%s</b><br>The 39 was sold on a snow day. "
                   "Which value best describes a typical day?" % lst(v),
                   "The median, 9", ["The mean, 15", "The highest, 39", "The total, 75"],
                   "39 is far from the other values. It pulls the mean up to 75 ÷ 5 = 15, more than any other day. "
                   "The median, 9, is in the middle of the usual days."))
    its.append(mcqv("Zoe’s mean bowling score for 4 games is 90. Three of her scores are 85, 92 and 88. What is her 4th score?",
                    95, [90, 265, 5], num,
                    "A mean of 90 for 4 games means the total is 4 × 90 = 360. The three scores add to 85 + 92 + 88 = 265. "
                    "360 − 265 = 95. (90 is the mean, 265 is the total of three games, and 5 uses 3 × 90 instead of 4 × 90.)"))
    v = [5, 7, 9]
    assert mean(v) == 7 and mean(v + [15]) == 9
    its.append(mcqv("The mean of 5, 7 and 9 is 7. Ava adds a 4th value, 15. What is the new mean?", 9, [7, 11, 12], num,
                    "New total: 5 + 7 + 9 + 15 = 36. There are now 4 values: 36 ÷ 4 = 9. "
                    "(11 averages only 7 and 15, and 12 still divides by 3.)"))
    v = [120, 95, 150, 135]
    assert mean(v) == 125 and median(v) == F("127.5")
    its.append(mcq("Four classes raised money for the Terry Fox Run: $120, $95, $150 and $135. What is the mean amount per class?",
                   "$125.00", ["$500.00", "$127.50", "$100.00"],
                   "Add: $120 + $95 + $150 + $135 = $500. Share it equally among 4 classes: $500 ÷ 4 = $125. "
                   "($127.50 is the median, and $100 divides by 5.)"))
    return {"title": "Mean, median and mode", "items": its}


# ------------------------------------------------------------ set 5: misleading graphs and conclusions
def set_claims():
    its = []
    f = fig(cans_svg())
    a, b = CANS[1]
    assert (b - 50) == 2 * (a - 50)
    C = lambda x: unit(x, "can", "cans")
    its.append(mcqv(f + "How many cans did 5A collect?", a, [a - 50, b, 50], C,
                    "The 5A bar reaches the line for 54. (4 is the height above the bottom of the scale, which starts at 50, not 0.)"))
    its.append(mcqv(f + "How many more cans did 5B collect than 5A?", b - a, [b - 50, a + b, b], C,
                    "58 − 54 = 4 cans. (8 reads only the part of the 5B bar above 50.)"))
    its.append(mcq(f + "The 5B bar looks twice as tall as the 5A bar. Did 5B collect twice as many cans?",
                   "No: 58 is not 2 × 54", ["Yes: its bar is twice as tall", "Yes: 58 is more than 54", "No: 5A collected more"],
                   "2 × 54 = 108, but 5B collected 58. The scale starts at 50, so we only see 4 and 8 of the cans: "
                   "that makes one bar look twice as tall as the other."))
    its.append(mcq(f + "Why does this graph make the difference look big?", "The scale starts at 50, not 0",
                   ["The bars are the same colour", "The graph has a title", "The scale goes up by 1s"],
                   "When the scale starts at 50, the bottom part of each bar is cut off. A small difference (4 cans) then looks large."))
    its.append(mcq(f + "Liam redraws the graph with the scale starting at 0. What will the bars look like?",
                   "Almost the same height", ["5B twice as tall as 5A", "5A taller than 5B", "Both bars missing"],
                   "From 0, the bars are 54 and 58 high. 58 is only a little more than 54, so the bars look almost the same."))
    its.append(mcq("A bar graph’s scale is labelled 0, 10, 20, 50, 100, with equal spaces between the labels. "
                   "Why is it misleading?", "Equal spaces show unequal amounts",
                   ["It starts at 0", "The numbers are too big", "It goes up by 10s"],
                   "The space from 0 to 10 is the same as the space from 50 to 100, but one is 10 and the other is 50. "
                   "Bars drawn on this scale cannot be compared fairly."))
    its.append(mcq("A graph has no title and no numbers on its scale. What is the problem?",
                   "You cannot tell what the bars show",
                   ["The bars are too wide", "It needs more colours", "Nothing: the bars are enough"],
                   "Without a title you do not know what the data is about, and without numbers on the scale "
                   "you cannot read the value of any bar."))
    its.append(mcq("A website says, “Kids love broccoli! 3 out of 4 kids we asked said yes.” They asked only 4 kids. "
                   "Why is this claim weak?", "The sample is far too small",
                   ["3 out of 4 is less than half", "Broccoli is a vegetable", "They should have asked 3 kids"],
                   "4 kids is a tiny sample. A different 4 kids could give a very different answer. (3 out of 4 is more than half.)"))
    its.append(mcq("At a hockey arena, 45 of the 50 people asked said hockey is their favourite sport. "
                   "A headline says, “90% of Canadians love hockey most!” What is the main problem?",
                   "People at an arena likely like hockey", ["45 out of 50 is not 90%", "50 people is too many",
                                                             "Hockey is not a sport"],
                   "The sample is biased: people at a hockey arena are more likely to choose hockey. "
                   "45 out of 50 is 90%, but only for those 50 people."))
    assert 9 * 2 < 28
    its.append(mcq("In a class of 28, pepperoni pizza got 9 votes, more than any other kind. "
                   "Noah says, “Most of the class likes pepperoni best.” Is this supported?",
                   "No: 9 of 28 is less than half", ["Yes: pepperoni is the mode", "Yes: 9 is the most votes",
                                                     "No: pepperoni is not the mode"],
                   "Pepperoni is the mode, but “most” means more than half. Half of 28 is 14, and only 9 students chose pepperoni."))
    its.append(mcq("10 of the 25 students in Ms. Roy’s class chose skating as their favourite winter activity. "
                   "Olivia says, “Half the class likes skating best.” Is she right?", "No: 10 of 25 is 40%",
                   ["Yes: skating got the most votes", "Yes: 10 is half of 20", "No: 10 of 25 is 10%"],
                   "10 out of 25 = " + fr(40, 100) + " = 40%. Half the class would be 50%, which is 12 or 13 students."))
    assert F(60, 600) == F(1, 10) and F(45, 150) == F(3, 10)
    its.append(mcq("At School A, 60 of the 600 students walk to school. At School B, 45 of the 150 students walk. "
                   "At which school does a greater part of the students walk?", "School B: 30%",
                   ["School A: 60 is more", "School A: 10%", "They are the same"],
                   "Compare parts of each school, not counts. A: " + fr(60, 600) + " = " + fr(1, 10) + " = 10%. B: "
                   + fr(45, 150) + " = " + fr(3, 10) + " = 30%. School B has fewer walkers, but a greater part of its students walk."))
    al = [10, 10, 12, 15, 8, 95]
    assert mean(al) == 25 and median(al) == 11
    its.append(mcq("Weekly allowances of 6 friends: %s. Owen says, “The typical allowance in our group is $25.” "
                   "Which is a better typical value?" % ", ".join("$" + num(x) for x in al),
                   "The median, $11", ["The mean, $25", "The highest, $95", "The mode, $95"],
                   "The mean is $150 ÷ 6 = $25, but 5 of the 6 friends get $15 or less. The $95 pulls the mean up. "
                   "In order: 8, 10, 10, 12, 15, 95, so the median is (10 + 12) ÷ 2 = $11."))
    g4, g5 = CLUB
    its.append(mcq(fig(club_svg()) + "Amira says, “More Grade 5 students than Grade 4 students are in clubs.” Is this supported?",
                   "Yes: 36 Grade 5 and 28 Grade 4", ["No: Choir has the tallest bar", "No: they are equal",
                                                      "Yes: Coding has 16 students"],
                   "Grade 5 parts: 8 + 6 + 12 + 10 = 36. Grade 4 parts: 6 + 10 + 4 + 8 = 28. 36 &gt; 28, so the claim is supported."))
    its.append(mcq("A hockey player’s mean is 2.5 goals a game. Arjun says, “So in one game, the player scored 2.5 goals.” "
                   "What is wrong?", "A mean does not have to be a data value",
                   ["The mean must be a whole number", "Nothing: he is right", "The mean is the most common score"],
                   "Goals are counted: a player scores 2 or 3, never 2.5. The mean shares the total equally, "
                   "so it can be a value that never happened. For example, 2 and 3 goals have a mean of 2.5."))
    its.append(mcq("The mean height of the Grade 5 basketball team is 145 cm. Does that mean every player is 145 cm tall?",
                   "No: some are taller and some shorter",
                   ["Yes: the mean is every value", "Yes: the team is all one height", "No: the mean is the tallest"],
                   "The mean is what each player would be if the total height were shared equally. "
                   "Real players can be taller or shorter than the mean."))
    its.append(mcq("A cereal box says, “Kids’ favourite! Chosen by 4 out of 5 kids.” Which question best checks this claim?",
                   "How many kids were asked, and who?", ["What colour is the box?", "How much does it cost?",
                                                           "Is 4 more than 5?"],
                   "A claim like this depends on the sample. If only 5 kids were asked, or they were chosen by the cereal maker, "
                   "the claim is weak."))
    its.append(mcq("A survey asked, “Don’t you think recess should be longer?” 90% said yes. Why might this result be misleading?",
                   "The question pushes people to say yes",
                   ["90% is too high to be true", "Recess is not data", "Surveys can only ask about numbers"],
                   "The question is not fair: it tells people the answer the asker wants. A fair question would be "
                   "“How long should recess be?”"))
    its.append(mcq("A poster shows two beaver pictures for the trees planted: 50 trees last year and 100 trees this year. "
                   "This year’s beaver is twice as tall and twice as wide. Why is this misleading?",
                   "The big beaver looks 4 times as big",
                   ["It should be 3 times as tall", "Beavers are not data", "100 is not twice 50"],
                   "Doubling both the height and the width makes the picture 2 × 2 = 4 times as big. "
                   "The eye sees the whole picture, so 100 trees look like 4 times 50 instead of 2 times."))
    v = [85, 120, 96, 139]
    assert mean(v) == 110
    its.append(mcqv("The school play sold tickets on 4 nights: %s. What is the mean number of tickets per night?" % lst(v),
                    110, [440, 88, 108], lambda x: unit(x, "ticket", "tickets"),
                    "Add: 85 + 120 + 96 + 139 = 440. Share equally over 4 nights: 440 ÷ 4 = 110 tickets. "
                    "(88 divides by 5, and 108 is the median: (96 + 120) ÷ 2.)"))
    assert median(v) == 108
    return {"title": "Misleading graphs and conclusions", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


LS_X = ["Mon", "Tue", "Wed"]
LS = [[6, 10, 8], [8, 4, 10]]
LEX = [6, 3, 8, 3, 5]
LVOTE = (["Pizza", "Tacos"], [62, 54])


def body_html():
    assert mean(LEX) == 5 and median(LEX) == 5 and modes(LEX) == [3]
    assert (LVOTE[1][0] - 50) == 3 * (LVOTE[1][1] - 50)
    return (
        "<h2>Good samples</h2>"
        "<p>The <b>population</b> is the whole group you want to learn about. A <b>sample</b> is the part of it you "
        "actually ask. A good sample is chosen at random, is not too small, and is like the whole population.</p>"
        "<p>A sample is <b>biased</b> when it favours some answers, for example asking people at a hockey arena about "
        "their favourite sport. Survey questions must also be fair: ask “What is your favourite season?”, "
        "not “Don’t you agree winter is best?”</p>"
        "<h2>Relative-frequency tables</h2>"
        "<p>The <b>relative frequency</b> of a choice is the part of all the data it makes up: "
        "count for that choice ÷ total count. Write it as a fraction, a decimal or a percent.</p>" +
        table(["Activity", "Students", "Fraction", "Decimal", "Percent"], [
            ["Skating", "10", fr(10, 25), "0.4", "40%"],
            ["Hockey", "6", fr(6, 25), "0.24", "24%"],
            ["Skiing", "5", fr(5, 25), "0.2", "20%"],
            ["Sledding", "4", fr(4, 25), "0.16", "16%"],
            ["Total", "25", fr(25, 25), "1", "100%"],
        ]) +
        "<p>The relative frequencies always add to 1 whole, or 100%.</p>" +
        ex("Example 1", "In a survey of 20 students, 9 walk to school. What is the relative frequency of walking?",
           "9 out of 20 = " + fr(9, 20) + " = " + fr(45, 100) + " = 0.45 = 45%.", fr(9, 20) + ", 0.45 or 45%") +
        "<h2>Stacked-bar graphs</h2>"
        "<p>In a <b>stacked-bar graph</b>, each bar is split into parts. The key tells you which colour is which part. "
        "The top of a bar shows the total. To find the size of an upper part, subtract where it starts from where it ends.</p>"
        "<figure class='sn-fig'>" + stacked_svg("Students who skated at recess", "Day", "Students", LS_X, LS,
                                                ["Grade 4", "Grade 5"], 20, 2, 4, gy=9, slot=72) +
        "<figcaption>On Tuesday, the Grade 5 part goes from 10 up to 14, so 4 Grade 5 students skated.</figcaption></figure>" +
        ex("Example 2", "How many students skated on Wednesday, and how many of them were in Grade 5?",
           "The top of the Wednesday bar is at 18. The Grade 5 part goes from 8 to 18: 18 − 8 = 10.",
           "18 students; 10 in Grade 5") +
        "<h2>Mean, median and mode</h2>" +
        table(["Measure", "How to find it", "For 6, 3, 8, 3, 5", "What it tells you"], [
            ["Mean", "Add the values, then divide by how many there are", "25 ÷ 5 = 5", "The fair share if all were equal"],
            ["Median", "Put the values in order and take the middle one", "3, 3, 5, 6, 8 → 5", "The middle value"],
            ["Mode", "The value that appears most often", "3", "The most common value"],
        ]) +
        "<p>With an even number of values, the median is halfway between the two middle values. A data set can have "
        "one mode, two modes or no mode. One very large or very small value pulls the mean toward it, so the median "
        "often describes a typical value better.</p>" +
        ex("Example 3", "Find the median of 9, 4, 12, 6.",
           "In order: 4, 6, 9, 12. The two middle values are 6 and 9: (6 + 9) ÷ 2 = 7.5.", "7.5") +
        "<h2>Misleading graphs</h2>"
        "<p>Before you believe a graph or a claim, check: Does the scale start at 0? Are the spaces on the scale equal? "
        "How many people were asked, and who?</p>"
        "<figure class='sn-fig'>" + bar_svg("Favourite lunch", "Lunch", "Votes", LVOTE[0], LVOTE[1], 50, 66, 2, 4, gy=10) +
        "<figcaption>The scale starts at 50, so the pizza bar looks 3 times as tall. Really, pizza has only 62 − 54 = 8 more votes.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Finding the median without putting the values in order", "Order the values first, then take the middle"],
            ["Judging bars by height when the scale does not start at 0", "Read the real values and subtract"],
            ["Reading the top of an upper part of a stacked bar as its size", "Subtract where the part starts from where it ends"],
            ["Comparing a part with the rest instead of with the total", "Relative frequency = part ÷ total"],
            ["Giving the highest value as the mode", "The mode is the value that appears most often"],
            ["Trusting a survey of a few people, or of people chosen in one place", "Ask how many and who was asked"],
        ])
    )


FAQ = [
    {"q": "What do Grade 5 students learn about data in the Ontario math curriculum?",
     "a": "In Grade 5, students collect data through good samples, organize it in relative-frequency tables, read and make stacked-bar graphs, find the mean, median and mode, and spot misleading graphs and claims."},
    {"q": "What is a relative-frequency table?",
     "a": "It shows what part of all the data each choice makes up: the count for a choice divided by the total. The relative frequencies can be written as fractions, decimals or percents, and they always add to 1 (100%)."},
    {"q": "How do you read a stacked-bar graph?",
     "a": "Use the key to see which colour is which part. The top of a bar is the total; for an upper part, subtract where the part starts from where it ends."},
    {"q": "How do you find the mean, median and mode?",
     "a": "Mean: add the values and divide by how many there are. Median: put the values in order and take the middle one (or halfway between the two middle ones). Mode: the value that appears most often."},
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
    rnd = random.Random(45813)
    sets = [set_samples(), set_relfreq(), set_stacked(), set_mmm(), set_claims()]
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
        "country": "ca-on", "subject": "math", "grade": "grade-5", "slug": "data-and-graphs", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Data and Graphs: Samples, Relative Frequency, Stacked-Bar Graphs, Mean, Median and Mode",
        "seo_title": "Grade 5 Data and Graphs Worksheets: Mean, Median, Mode, Stacked-Bar Graphs (Free, Answer Key)",
        "short_title": "Data and graphs",
        "domain": "Data",
        "standard_code": "Grade 5: D1.5",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Determine the mean and the median and identify the mode(s), if any, for various data sets involving whole numbers and decimal numbers, and explain what each of these measures indicates about the data",
        "meta_desc": "Free Grade 5 math worksheets on data and graphs for the Ontario curriculum: good samples, relative-frequency tables with fractions, decimals and percents, stacked-bar graphs, mean, median and mode, and misleading graphs. 100 questions with an answer key.",
        "key_big": "Mean, median and mode describe a data set; check the sample and the scale before you trust a graph.",
        "key_sub": "Mean = total ÷ number of values. Median = the middle value in order. Mode = the most common value. Relative frequency = part ÷ total, as a fraction, decimal or percent.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (graphs, tables and line plots) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "(line plot|bar graph|stacked-bar graph|table)")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
