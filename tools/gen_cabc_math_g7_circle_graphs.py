# -*- coding: utf-8 -*-
"""
BC Grade 7 Math: Circle graphs (BC Mathematics Curriculum, Grade 7: Data and probability, circle graphs)
  python3 tools/gen_cabc_math_g7_circle_graphs.py
Read circle graphs in percents, find amounts from percents (25% of 80 students), find sector angles
(percent × 360°), make a circle graph from a table (choose the graph that matches, A–D), and choose the right
graph and draw conclusions in BC contexts (how students get to school, time spent in a day, spending money).
Wrong answers come from real student mistakes: 25% drawn as 25°, sectors that do not add up to 100% (or 360°),
using 100 instead of 360, the percent read as a number of people, the complement, decimal slips (0.35 × 360 = 12.6),
and a bigger sector read as more people when the totals are different.
Every answer is computed with fractions.Fraction. Circle graphs are drawn exactly from the data
(sector angle = share of 360°), starting at 12 o'clock and going clockwise. The pie helper is adapted from
gen_uk_maths_y6_pie_line.py. Canadian English, BC number style. HTML attributes use single quotes.
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-7")
UPDATED = "2026-11-02"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
PALETTE = ["#8fc9a3", "#f2d16b", "#9cbfe8", "#f0a58f", "#c9bde6", "#d7dcd9"]
M = "−"
NBSP = " "


# ------------------------------------------------------------ numbers
def num(x):
    """BC style: no separator for 4 digits, no-break space for 5+; up to 2 decimal places."""
    x = F(x)
    neg = x < 0
    x = abs(x)
    if x.denominator == 1:
        v = x.numerator
        s = str(v) if v < 10000 else "{:,}".format(v).replace(",", NBSP)
    else:
        for k in (1, 2, 3):
            d = x * 10 ** k
            if d.denominator == 1:
                v = int(d)
                s = "%d.%0*d" % (v // 10 ** k, k, v % 10 ** k)
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
    return "$%s" % ("%.2f" % float(x))


def unit(v, one, many):
    return "%s %s" % (num(v), one if F(v) == 1 else many)


def stu(v):
    return unit(v, "student", "students")


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def frs(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else fr(x.numerator, x.denominator)


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


# ------------------------------------------------------------ question helpers
def mcq(q, right, wrongs, e):
    ch = [right]
    for w in wrongs:
        if plain(w) not in {plain(c) for c in ch}:
            ch.append(w)
        if len(ch) == 4:
            break
    assert len(ch) == 4, (q, right, wrongs)
    return {"q": q, "c": ch, "a": 0, "e": e}


def mcqv(q, right, wrongs, f, e):
    """Choices given as values: equal values are dropped (no two choices equal in value)."""
    seen = [F(right)]
    pick = []
    for w in list(wrongs) + [F(right) + 1, F(right) - 1, F(right) * 2]:
        w = F(w)
        if w in seen or w <= 0:
            continue
        seen.append(w)
        pick.append(w)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, right, wrongs)
    return mcq(q, f(right), [f(w) for w in pick], e)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(x0, y0, w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='%d %d %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (x0, y0, w, h, w, h, label, FONT, body))


def tw(t, fs, bold=False):
    return len(str(t)) * fs * (0.62 if bold else 0.58)


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


# ------------------------------------------------------------ circle graphs
class Pie:
    """cats with parts (percents, degrees or counts); labels drawn outside each sector."""
    def __init__(self, title, cats, parts, labels=None, n=None):
        self.title, self.cats, self.parts = title, cats, [F(p) for p in parts]
        self.n = F(n) if n is not None else sum(self.parts)
        assert sum(self.parts) == self.n, (title, parts)
        self.labels = labels or cats
        self.fills = PALETTE[:len(cats)]
        assert len(set(cats)) == len(cats)


def pct_pie(title, data, hide=None):
    """data: [(cat, percent)]; hide: the category whose percent is shown as ?."""
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
    ty = min(ys) - 10
    s.append(text(0, ty, p.title, 15, bold=True))
    tww = tw(p.title, 15, True)
    bbox = (min(min(xs), -tww / 2), ty - 14, max(max(xe), tww / 2), max(ye))
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
    """options: four lists of (letter, angle in degrees); a part of the circle left over stays white.
    Graphs labelled A, B, C, D below."""
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
            if a == 360:
                s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s'/>" % (cx, cy, R, fills[let]))
            else:
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
    """A 'which circle graph matches' question. data: [(letter, angle)] for the right graph;
    wrong_opts: three [(letter, angle)] lists. The graph order is fixed when balance() picks the answer position."""
    fills = {let: PALETTE[i] for i, (let, _) in enumerate(data)}

    def build(t):
        opts = list(wrong_opts)
        notes = list(e_wrongs)
        opts.insert(t, data)
        notes.insert(t, None)
        L = "ABCD"
        q = fig(mini_pies(opts, fills, "circle graphs A, B, C and D: " + kind)) + lead + " Key: " + key + "."
        e = "Graph %s is right. %s " % (L[t], e_right)
        e += " ".join("Graph %s: %s" % (L[i], n) for i, n in enumerate(notes) if n)
        return {"q": q, "c": ["A", "B", "C", "D"], "a": t, "e": e}
    return {"_build": build}


# ------------------------------------------------------------ set 1: read a circle graph in percents
def set_read():
    its = []
    travel = pct_pie("How Grade 7 students get to school", [("Walk", 35), ("Bus", 25), ("Car", 30), ("Bike", 10)])
    f = fig(pie_svg(travel))
    its.append(mcqv(f + "What percent of the students take the bus?", 25, [75, 35, 30], pct,
                    "Read the label on the Bus sector: 25%."))
    its.append(mcq(f + "Which way of getting to school is used by the most students?", "Walk", ["Car", "Bus", "Bike"],
                   "The biggest sector has the biggest percent: Walk is 35%, more than Car (30%)."))
    its.append(mcqv(f + "What percent of the students do not walk to school?", 65, [35, 75, 45], pct,
                    "All the sectors make 100%. 100% − 35% = 65%. (Or: 25% + 30% + 10% = 65%.)"))
    its.append(mcqv(f + "What percent of the students take the bus or ride a bike?", 35, [25, 10, 65], pct,
                    "Add the two sectors: 25% + 10% = 35%."))
    season = pct_pie("Favourite season", [("Summer", 45), ("Winter", 25), ("Fall", 20), ("Spring", 10)], hide="Spring")
    its.append(mcqv(fig(pie_svg(season)) + "What percent of the students chose spring?", 10, [90, 270, 20], pct,
                    "The sectors add up to 100%. 45% + 25% + 20% = 90%. 100% − 90% = 10%. "
                    "(270 comes from 360 − 90: percents add up to 100, not 360.)"))
    sport = pct_pie("Favourite sport", [("Soccer", 30), ("Hockey", 25), ("Basketball", 20), ("Lacrosse", 15),
                                        ("Swimming", 10)], hide="Basketball")
    its.append(mcqv(fig(pie_svg(sport)) + "What percent of the students chose basketball?", 20, [80, 280, 25], pct,
                    "30% + 25% + 15% + 10% = 80%. The whole circle is 100%, so basketball is 100% − 80% = 20%."))
    subj = pct_pie("Favourite subject", [("Math", 20), ("Science", 30), ("PE", 25), ("Art", 15), ("Music", 10)])
    f = fig(pie_svg(subj))
    its.append(mcq(f + "Which two subjects together make exactly half of the circle graph?", "Math and Science",
                   ["PE and Art", "Science and PE", "Math and PE"],
                   "Half is 50%. Math 20% + Science 30% = 50%. PE and Art = 40%, Science and PE = 55%, Math and PE = 45%."))
    its.append(mcq(f + "Which subject was chosen by one-quarter of the students?", "PE", ["Math", "Science", "Art"],
                   "One-quarter is 25%. The PE sector is 25%."))
    its.append(mcq(f + "Which sector is %s of the circle graph?" % fr(1, 10), "Music", ["Art", "Math", "PE"],
                   "%s = 10%%. The Music sector is 10%%." % fr(1, 10)))
    fruit = pct_pie("Favourite fruit", [("Apples", 40), ("Berries", 25), ("Bananas", 20), ("Grapes", 15)])
    f = fig(pie_svg(fruit))
    its.append(mcqv(f + "How many percent more students chose apples than grapes?", 25, [55, 15, 40], pct,
                    "Subtract: 40% − 15% = 25%. (55% adds the two sectors.)"))
    its.append(mcqv(f + "What fraction of the students chose apples?", F(2, 5), [F(1, 40), F(1, 4), F(4, 5)], frs,
                    "40%% = %s = %s. (%s reads the percent as a denominator.)" % (fr(40, 100), frs(F(2, 5)), fr(1, 40))))
    its.append(mcq(f + "Which statement is true?", "Twice as many chose apples as bananas",
                   ["Half of the students chose berries", "Grapes is the second biggest sector",
                    "Apples and berries are less than half"],
                   "Apples 40% is 2 × 20% (bananas). Berries is 25%, not 50%. Apples and berries are 65%, more than half."))
    rec = pct_pie("Recycling at a Vancouver school", [("Paper", F(85, 2)), ("Plastic", F(55, 2)), ("Food scraps", 18),
                                                      ("Cans", 12)], hide="Food scraps")
    its.append(mcqv(fig(pie_svg(rec)) + "What percent of the recycling is food scraps?", 18, [82, 278, 19], pct,
                    "42.5% + 27.5% + 12% = 82%. 100% − 82% = 18%. (19% comes from adding 42.5 + 27.5 as 69 instead of 70.)"))
    its.append(mcq("Owen made a circle graph: hockey 40%, soccer 35%, lacrosse 30%. What is wrong?",
                   "The percents add to 105%", ["Nothing is wrong", "The percents must add to 360%",
                                                "Lacrosse must be the biggest"],
                   "40% + 35% + 30% = 105%. The sectors of a circle graph must add up to exactly 100%, so one percent is wrong."))
    its.append(mcq("The percents in a circle graph must add up to …", "100%", ["360%", "50%", "the number of sectors"],
                   "A circle graph shows one whole. The whole is 100%. (360 is the number of degrees, not the percent.)"))
    pets = pct_pie("Pets at home", [("Dog", 35), ("Cat", 25), ("No pet", 20), ("Fish", 15), ("Other", 5)])
    f = fig(pie_svg(pets))
    its.append(mcqv(f + "What percent of the students have a dog or a cat?", 60, [40, 35, 25], pct,
                    "35% + 25% = 60%. (40% is everyone else.)"))
    its.append(mcqv(f + "What percent of the students have a pet?", 80, [20, 100, 75], pct,
                    "Everyone not in the No pet sector has a pet: 100% − 20% = 80%. (75% forgets the Other sector.)"))
    its.append(mcq(f + "Which two sectors together are the same size as the Dog sector?", "No pet and Fish",
                   ["Cat and Other", "Cat and Fish", "Fish and Other"],
                   "Dog is 35%. No pet 20% + Fish 15% = 35%. Cat and Other = 30%, Cat and Fish = 40%, Fish and Other = 20%."))
    its.append(mcqv("A circle graph has 4 sectors that are all the same size. What percent is each sector?", 25,
                    [90, 4, 40], pct, "100% ÷ 4 = 25%. (90 is the angle in degrees, not the percent.)"))
    its.append(mcqv("A circle graph has 3 sectors. Two of them are 45% and 30%. What percent is the third sector?", 25,
                    [75, 285, 15], pct, "45% + 30% = 75%. 100% − 75% = 25%. (285 uses 360 instead of 100.)"))
    return {"title": "Read a circle graph in percents", "items": its}


# ------------------------------------------------------------ set 2: amounts from percents
def set_amounts():
    its = []
    a = pct_pie("How 80 students get to school", [("Walk", 45), ("Bus", 25), ("Car", 20), ("Bike", 10)])
    f = fig(pie_svg(a))
    its.append(mcqv(f + "How many students take the bus?", 20, [25, 60, 200], stu,
                    "25%% = %s. %s of 80 = 80 ÷ 4 = 20 students. (25 is the percent, not the number of students.)"
                    % (frs(F(1, 4)), frs(F(1, 4)))))
    its.append(mcqv(f + "How many students ride a bike?", 8, [10, 72, 16], stu,
                    "10% of 80 = 80 ÷ 10 = 8 students."))
    its.append(mcqv(f + "How many students walk?", 36, [45, 44, 40], stu,
                    "10% of 80 = 8 and 5% of 80 = 4. 45% = 4 × 8 + 4 = 36 students. (Or 0.45 × 80 = 36.)"))
    its.append(mcqv(f + "How many more students walk than ride a bike?", 28, [35, 44, 26], stu,
                    "Walk: 36. Bike: 8. 36 − 8 = 28 students. (35 is the difference in percent, not in students.)"))
    b = pct_pie("Favourite snack of 200 students", [("Fruit", 30), ("Chips", 25), ("Granola bars", 35), ("Yogurt", 10)])
    f = fig(pie_svg(b))
    its.append(mcqv(f + "How many students chose granola bars?", 70, [35, 130, 7], stu,
                    "1% of 200 = 2. 35% = 35 × 2 = 70 students. (35 would be right only for 100 students.)"))
    its.append(mcqv(f + "How many students chose yogurt?", 20, [10, 180, 2], stu, "10% of 200 = 200 ÷ 10 = 20 students."))
    its.append(mcqv(f + "How many students chose fruit or yogurt?", 80, [40, 120, 60], stu,
                    "30% + 10% = 40%. 40% of 200 = 0.4 × 200 = 80 students."))
    c = pct_pie("Favourite sport of 60 students", [("Soccer", 40), ("Hockey", 25), ("Basketball", 20), ("Lacrosse", 15)])
    f = fig(pie_svg(c))
    its.append(mcqv(f + "How many students chose lacrosse?", 9, [15, 51, 4], stu,
                    "10% of 60 = 6 and 5% of 60 = 3. 15% = 6 + 3 = 9 students. (4 comes from 60 ÷ 15.)"))
    its.append(mcqv(f + "How many students chose hockey?", 15, [25, 45, 12], stu,
                    "25%% = %s. 60 ÷ 4 = 15 students." % frs(F(1, 4))))
    its.append(mcqv(f + "How many students chose soccer?", 24, [40, 36, F(12, 5)], stu,
                    "40% = 0.4. 0.4 × 60 = 24 students. (2.4 puts the decimal point in the wrong place.)"))
    its.append(mcqv("24 of the 60 students in a survey chose soccer. What percent is that?", 40, [24, 36, F(5, 2)], pct,
                    "%s = %s = 0.4 = 40%%. (36 is the number of students who did not choose soccer.)"
                    % (fr(24, 60), frs(F(2, 5)))))
    its.append(mcqv("18 of 40 students chose hiking. What percent of the circle graph is hiking?", 45, [18, 22, 55], pct,
                    "%s = 0.45 = 45%%. (55%% is the rest of the circle.)" % fr(18, 40)))
    trip = pct_pie("Favourite field trip", [("Science World", 25), ("Aquarium", 40), ("Grouse Mountain", 35)])
    its.append(mcqv(fig(pie_svg(trip)) + "10 students chose Science World. How many students were in the survey?", 40,
                    [250, F(5, 2), 35], stu,
                    "Science World is 25%% = %s of the students. If %s is 10 students, the whole is 4 × 10 = 40 students."
                    % (frs(F(1, 4)), frs(F(1, 4)))))
    its.append(mcqv("In a survey, 30% of the students chose hiking. That is 12 students. How many students were in the survey?",
                    40, [36, 42, 4], stu,
                    "30% is 12 students, so 10% is 12 ÷ 3 = 4 students. 100% is 10 × 4 = 40 students."))
    d = pct_pie("How 500 Surrey students get to school", [("Walk", 32), ("Car", 38), ("Bus", 22), ("Bike", 8)])
    f = fig(pie_svg(d))
    its.append(mcqv(f + "How many students come by car?", 190, [38, 310, 19], stu,
                    "1% of 500 = 5. 38% = 38 × 5 = 190 students."))
    its.append(mcqv(f + "How many students ride a bike?", 40, [8, 460, 4], stu, "8% of 500 = 8 × 5 = 40 students."))
    its.append(mcqv("12.5% of the 80 students in a survey chose orcas as their favourite animal. How many students is that?", 10,
                    [8, 12, 70], stu,
                    "12.5%% = %s. 80 ÷ 8 = 10 students. (8 is only 10%%.)" % frs(F(1, 8))))
    its.append(mcqv("Mei’s class has 32 students. 75% of them have a library card. How many students have a library card?",
                    24, [8, 75, 25], stu,
                    "75%% = %s. 32 ÷ 4 = 8, and 3 × 8 = 24 students. (8 students do not have a card.)" % frs(F(3, 4))))
    e = pct_pie("How Ji-woo spends $40 a month", [("Savings", 40), ("Food", 25), ("Games", 20), ("Bus fare", 15)])
    its.append(mcqv(fig(pie_svg(e)) + "How much does Ji-woo spend on games each month?", 8, [20, 32, 2], dollars,
                    "20% of $40 = 0.2 × $40 = $8. ($20 reads the percent as dollars.)"))
    its.append(mcqv("300 students voted on a new school logo. The circle graph shows 45% voted Yes. How many students voted Yes?",
                    135, [45, 165, 150], stu,
                    "1% of 300 = 3. 45% = 45 × 3 = 135 students. (165 voted No.)"))
    return {"title": "Find amounts from percents", "items": its}


# ------------------------------------------------------------ set 3: sectors in degrees
def set_degrees():
    its = []
    D = deg
    its.append(mcqv("All the angles at the centre of a circle graph add up to …", 360, [100, 180, 90], D,
                    "A circle graph is a whole circle, and a full turn is 360°. (100 is for percents.)"))
    its.append(mcqv("A sector is 25% of a circle graph. What is its angle?", 90, [25, 50, 270], D,
                    "25% × 360° = 0.25 × 360° = 90°. A sector of 25% is NOT 25°: it is one-quarter of the circle, a right angle."))
    its.append(mcqv("A sector is 50% of a circle graph. What is its angle?", 180, [50, 100, 360], D,
                    "50% × 360° = 0.5 × 360° = 180°, half of the circle."))
    its.append(mcqv("A sector is 10% of a circle graph. What is its angle?", 36, [10, F(18, 5), 360], D,
                    "10% × 360° = 0.1 × 360° = 36°. (3.6° is 1%.)"))
    its.append(mcqv("A sector is 20% of a circle graph. What is its angle?", 72, [20, F(36, 5), 80], D,
                    "20% × 360° = 0.2 × 360° = 72°."))
    its.append(mcqv("A sector is 35% of a circle graph. What is its angle?", 126, [35, F(63, 5), 325], D,
                    "35% × 360° = 0.35 × 360° = 126°. (12.6° puts the decimal point in the wrong place.)"))
    its.append(mcqv("A sector is 15% of a circle graph. What is its angle?", 54, [15, F(27, 5), 45], D,
                    "15% × 360° = 0.15 × 360° = 54°. (45° multiplies by 3 instead of 3.6.)"))
    its.append(mcqv("A sector is 12.5% of a circle graph. What is its angle?", 45, [F(25, 2), F(9, 2), 40], D,
                    "12.5%% × 360° = 0.125 × 360° = 45°. Check: 12.5%% is %s, and 360 ÷ 8 = 45." % frs(F(1, 8))))
    its.append(mcqv("A sector of a circle graph has an angle of 90°. What percent is it?", 25, [90, 9, 75], pct,
                    "90° ÷ 360° = 0.25 = 25%. (90% reads the degrees as a percent.)"))
    its.append(mcqv("A sector of a circle graph has an angle of 72°. What percent is it?", 20, [72, F(36, 5), 28], pct,
                    "72° ÷ 360° = 0.2 = 20%."))
    its.append(mcqv("A sector of a circle graph has an angle of 108°. What percent is it?", 30, [108, F(54, 5), 36], pct,
                    "108° ÷ 360° = 0.3 = 30%."))
    its.append(mcqv("A sector is %s of a circle graph. What is its angle?" % fr(1, 3), 120, [33, 30, 240], D,
                    "360° ÷ 3 = 120°. (33 is about the percent, not the angle.)"))
    its.append(mcqv("24 students were asked. 8 chose art. What angle should the art sector be?", 120, [8, 15, 192], D,
                    "Each student is 360° ÷ 24 = 15°. 8 × 15° = 120°. (Or: %s of 360° = 120°.)" % frs(F(1, 3))))
    its.append(mcqv("40 students were asked. 14 have a dog. What angle should the dog sector be?", 126, [14, 35, 140], D,
                    "Each student is 360° ÷ 40 = 9°. 14 × 9° = 126°. (35 is the percent: 35% × 360° = 126°.)"))
    its.append(mcqv("A circle graph shows 45 students. How many degrees stand for each student?", 8, [45, 315, 4], D,
                    "360° ÷ 45 = 8° for each student."))
    walk = deg_pie("How students get to school", [("Walk", 126), ("Bus", 108), ("Car", 90), ("Bike", 36)], hide="Car")
    its.append(mcqv(fig(pie_svg(walk)) + "What is the angle of the Car sector?", 90, [270, 126, 108], D,
                    "126° + 108° + 36° = 270°. The angles add up to 360°, so 360° − 270° = 90°. "
                    "(270° is the total of the other three sectors, not the Car sector.)"))
    sp = pct_pie("Favourite winter sport", [("Skiing", 40), ("Snowboarding", 30), ("Skating", 20), ("Sledding", 10)])
    its.append(mcq(fig(pie_svg(sp)) + "Which sector has an angle of 72°?", "Skating", ["Sledding", "Snowboarding", "Skiing"],
                   "72° ÷ 360° = 0.2 = 20%. The Skating sector is 20%. (Sledding is 36°, Snowboarding 108°, Skiing 144°.)"))
    its.append(mcqv("In a circle graph, each person is 4°. How many people does the whole graph show?", 90, [1440, 25, 94],
                    lambda v: unit(v, "person", "people"),
                    "360° ÷ 4° = 90 people. (1440 multiplies instead of dividing. 25 uses 100 instead of 360.)"))
    its.append(mcqv("A circle graph shows 60 students. The soccer sector is 150°. How many students chose soccer?", 25,
                    [150, 6, 15], stu,
                    "Each student is 360° ÷ 60 = 6°. 150° ÷ 6° = 25 students. (15 uses 10° for each student.)"))
    its.append(mcqv("A circle graph shows 30 students. The walk sector is 132°. How many students walk?", 11,
                    [132, F(66, 5), 12], stu,
                    "Each student is 360° ÷ 30 = 12°. 132° ÷ 12° = 11 students. Check: 11 × 12° = 132°."))
    return {"title": "Find sector angles in degrees", "items": its}


# ------------------------------------------------------------ set 4: make a circle graph from a table
def set_make():
    its = []
    its.append(mcq("You have a table of counts. What do you do first to make a circle graph?", "Find the total",
                   ["Draw the biggest sector", "Multiply each count by 100", "Use 1° for each person"],
                   "First add the counts to find the total. Then find each part as a percent of the total "
                   "(or 360° ÷ total for each person)."))
    its.append(mcqv("To change a percent into a sector angle, you multiply the percent by …", F(18, 5), [360, 100, F(9, 25)],
                    num, "1% of 360° is 360 ÷ 100 = 3.6°. So 25% is 25 × 3.6° = 90°."))
    its.append(mcqv("A table shows that 9 of 36 students chose basketball. What percent should the sector show?", 25,
                    [9, 27, 4], pct, "%s = %s = 25%%. (27 is the number of students who did not choose basketball.)"
                    % (fr(9, 36), frs(F(1, 4)))))
    tab = "Favourite activity of 40 students: hiking 14, skiing 12, swimming 10, biking 4."
    its.append(mcqv(tab + " What percent should the hiking sector show?", 35, [14, 28, 26], pct,
                    "%s = 0.35 = 35%%. (28 doubles 14, but 40 is not 50.)" % fr(14, 40)))
    its.append(mcqv(tab + " What angle should the skiing sector be?", 108, [12, 30, 120], D_(),
                    "Each student is 360° ÷ 40 = 9°. 12 × 9° = 108°. (30 is the percent. 120 uses 10° for each student.)"))
    its.append(mcqv(tab + " What angle should the biking sector be?", 36, [4, 10, 40], D_(),
                    "4 × 9° = 36°. (10 is the percent, not the angle.)"))
    its.append(mcq("20 students: walk 9, bus 6, car 5. Which sector angles are correct?", "162°, 108°, 90°",
                   ["9°, 6°, 5°", "45°, 30°, 25°", "180°, 120°, 60°"],
                   "Each student is 360° ÷ 20 = 18°. 9 × 18° = 162°, 6 × 18° = 108°, 5 × 18° = 90°. Check: 162 + 108 + 90 = 360. "
                   "(45°, 30°, 25° are the percents used as degrees.)"))
    its.append(mcq("Walk 45%, bus 35%, car 20%. Which sector angles are correct?", "162°, 126°, 72°",
                   ["45°, 35°, 20°", "135°, 105°, 60°", "162°, 126°, 82°"],
                   "Multiply each percent by 3.6°: 45 × 3.6 = 162°, 35 × 3.6 = 126°, 20 × 3.6 = 72°. They add up to 360°. "
                   "(135°, 105°, 60° multiplies by 3, not 3.6.)"))
    its.append(mcqv("A table has a total of 50 students. How many degrees stand for each student?", F(36, 5),
                    [50, 2, 72], D_(), "360° ÷ 50 = 7.2° for each student. (2 uses 100 ÷ 50.)"))
    its.append(mcqv("A table shows that 12 of 48 students chose skating. What angle should the skating sector be?", 90,
                    [12, 25, 120], D_(), "%s = %s. %s of 360° = 90°. (25 is the percent.)"
                    % (fr(12, 48), frs(F(1, 4)), frs(F(1, 4)))))
    its.append(mcqv("A table shows that 7 of 40 students chose the bus. What percent should the bus sector show?", F(35, 2),
                    [7, 33, 28], pct, "%s = 7 ÷ 40 = 0.175 = 17.5%%. (28 multiplies 7 by 4 instead of 2.5.)" % fr(7, 40)))
    its.append(mcqv("A table shows that 6 of 25 students chose art. What angle should the art sector be?", F(432, 5),
                    [6, 24, 60], D_(), "Each student is 360° ÷ 25 = 14.4°. 6 × 14.4° = 86.4°. (24 is the percent.)"))
    its.append(mcq("Ava’s table says: soccer 45%, hockey 30%, lacrosse 20%, basketball 15%. Why can’t she make a circle graph?",
                   "The percents add to 110%", ["The percents must add to 360%", "Basketball is too small",
                                                "There are too many sports"],
                   "45 + 30 + 20 + 15 = 110. The sectors of a circle graph must add up to 100%, so Ava made a mistake."))
    its.append(mcq("Noah worked out the sector angles 150°, 120° and 80°. What is wrong?", "They add to 350°, not 360°",
                   ["They must add to 100°", "Nothing is wrong", "The biggest must be 180°"],
                   "150 + 120 + 80 = 350. The angles of a circle graph must add up to 360°, so one angle is wrong."))

    # which graph matches (A–D)
    its.append(match_item(
        [("W", 180), ("B", 90), ("C", 90)], "W = walk, B = bus, C = car", "walk, bus and car",
        [[("W", 50), ("B", 25), ("C", 25)], [("W", 90), ("B", 180), ("C", 90)], [("W", 120), ("B", 120), ("C", 120)]],
        "How students get to school: walk 50%, bus 25%, car 25%. Which circle graph matches?",
        "Walk 50% = 180° (half), bus and car 25% = 90° each.",
        ["uses 50° for 50% and 25° for 25%, so the sectors do not fill the circle.",
         "swaps walk and bus.", "makes every sector the same size."]))
    its.append(match_item(
        [("S", 180), ("H", 120), ("L", 60)], "S = soccer, H = hockey, L = lacrosse", "soccer, hockey and lacrosse",
        [[("S", 120), ("H", 180), ("L", 60)], [("S", 15), ("H", 10), ("L", 5)], [("S", 180), ("H", 60), ("L", 120)]],
        "30 students: soccer 15, hockey 10, lacrosse 5. Which circle graph matches?",
        "Each student is 360° ÷ 30 = 12°: soccer 15 × 12° = 180°, hockey 120°, lacrosse 60°.",
        ["swaps soccer and hockey.", "uses 1° for each student, so the sectors do not fill the circle.",
         "swaps hockey and lacrosse."]))
    its.append(match_item(
        [("D", 144), ("C", 108), ("F", 72), ("R", 36)], "D = dog, C = cat, F = fish, R = rabbit", "dog, cat, fish and rabbit",
        [[("D", 108), ("C", 144), ("F", 72), ("R", 36)], [("D", 90), ("C", 90), ("F", 90), ("R", 90)],
         [("D", 16), ("C", 12), ("F", 8), ("R", 4)]],
        "40 students: dog 16, cat 12, fish 8, rabbit 4. Which circle graph matches?",
        "Each student is 360° ÷ 40 = 9°: dog 144°, cat 108°, fish 72°, rabbit 36°.",
        ["swaps dog and cat.", "makes every sector the same size.",
         "uses 1° for each student, so the sectors do not fill the circle."]))
    its.append(match_item(
        [("W", 144), ("B", 108), ("C", 72), ("K", 36)], "W = walk, B = bus, C = car, K = bike", "walk, bus, car and bike",
        [[("W", 40), ("B", 30), ("C", 20), ("K", 10)], [("W", 144), ("B", 72), ("C", 108), ("K", 36)],
         [("W", 180), ("B", 90), ("C", 54), ("K", 36)]],
        "Walk 40%, bus 30%, car 20%, bike 10%. Which circle graph matches?",
        "Multiply by 3.6°: walk 144°, bus 108°, car 72°, bike 36°.",
        ["uses 40° for 40% and so on, so it fills only 100° of the circle.", "swaps bus and car.",
         "draws walk as half the circle, but 40% is less than half."]))
    its.append(match_item(
        [("P", 180), ("O", 108), ("C", 72)], "P = paper, O = organics, C = cans", "paper, organics and cans",
        [[("P", 180), ("O", 72), ("C", 108)], [("P", 50), ("O", 30), ("C", 20)], [("P", 144), ("O", 108), ("C", 108)]],
        "Recycling: paper 50%, organics 30%, cans 20%. Which circle graph matches?",
        "Paper 50% = 180°, organics 30% = 108°, cans 20% = 72°.",
        ["swaps organics and cans.", "uses 50° for 50% and so on, so the sectors do not fill the circle.",
         "makes paper less than half, but 50% is exactly half."]))
    its.append(match_item(
        [("S", 216), ("H", 90), ("G", 54)], "S = sleep, H = hiking, G = games", "sleep, hiking and games",
        [[("S", 90), ("H", 216), ("G", 54)], [("S", 120), ("H", 120), ("G", 120)], [("S", 60), ("H", 25), ("G", 15)]],
        "Kai’s camping trip day: sleep 60%, hiking 25%, games 15%. Which circle graph matches?",
        "Sleep 60% × 3.6° = 216°, hiking 25% = 90°, games 15% = 54°.",
        ["swaps sleep and hiking.", "makes every sector the same size.",
         "uses 60° for 60% and so on, so the sectors do not fill the circle."]))
    return {"title": "Make a circle graph from a table", "items": its}


def D_():
    return deg


# ------------------------------------------------------------ set 5: choose the right graph and draw conclusions
def set_problems():
    its = []
    its.append(mcq("Which graph is best to show what percent of a class gets to school each way?", "Circle graph",
                   ["Line graph", "Line plot", "Venn diagram"],
                   "The ways of getting to school are parts of one whole class. A circle graph shows parts of a whole."))
    its.append(mcq("Which graph is best to show how the temperature in Kamloops changes over one week?", "Line graph",
                   ["Circle graph", "Pictograph", "Venn diagram"],
                   "Temperature changes over time. A line graph shows how it goes up and down."))
    its.append(mcq("Which data can NOT be shown well in a circle graph?", "Sports students play (can pick more than one)",
                   ["How students get to school", "How Leah spends her $50", "How Owen spends 24 hours"],
                   "If students can pick more than one sport, the percents add up to more than 100%. "
                   "A circle graph needs parts of one whole."))
    its.append(mcq("Why is a circle graph a poor choice to show the number of salmon in the Fraser River each year?",
                   "The data change over time", ["Salmon are too many to count", "Circle graphs show only 4 sectors",
                                                 "The numbers are too small"],
                   "Counts for each year are not parts of one whole. A line graph or bar graph shows how they change over time."))
    day = deg_pie("Owen’s day (24 hours)", [("Sleep", 135), ("School", 90), ("Sports", 45), ("Homework", 15),
                                            ("Other", 75)])
    f = fig(pie_svg(day))
    H = lambda v: unit(v, "hour", "hours")
    its.append(mcqv(f + "How many hours does Owen sleep?", 9, [135, F(27, 2), 8], H,
                    "24 hours = 360°, so 1 hour = 360° ÷ 24 = 15°. Sleep: 135° ÷ 15° = 9 hours. (13.5 divides by 10.)"))
    its.append(mcqv(f + "What percent of Owen’s day is school?", 25, [6, 90, 24], pct,
                    "90° ÷ 360° = 0.25 = 25%. (6 is the number of hours, and 90 is the angle.)"))
    its.append(mcqv(f + "How many more hours does Owen sleep than spend at school?", 3, [45, 9, 15], H,
                    "Sleep: 135° ÷ 15° = 9 hours. School: 90° ÷ 15° = 6 hours. 9 − 6 = 3 hours. (45 is the difference in degrees.)"))
    its.append(mcq(f + "Which statement is true?", "He sleeps more than one-third of the day",
                   ["He is at school for half the day", "He spends 15 hours on homework",
                    "He is at school longer than he sleeps"],
                   "One-third of the day is 120°. Sleep is 135°, more than 120°. School is 90°, a quarter. Homework is 15° = 1 hour."))
    a = pct_pie("School A: 400 students", [("Walk", 25), ("Car", 40), ("Bus", 25), ("Bike", 10)])
    b = pct_pie("School B: 250 students", [("Walk", 40), ("Car", 30), ("Bus", 20), ("Bike", 10)])
    f = fig(pie_svg(a, b))
    its.append(mcq(f + "Which school has more students who walk?", "Both the same", ["School A", "School B", "You cannot tell"],
                   "School A: 25% of 400 = 100. School B: 40% of 250 = 100. The Walk sector is bigger at School B, "
                   "but School B has fewer students."))
    its.append(mcqv(f + "How many more students come by car at School A than at School B?", 85, [10, 160, 235], stu,
                    "School A: 40% of 400 = 160. School B: 30% of 250 = 75. 160 − 75 = 85 students. (10 is the difference in percent.)"))
    its.append(mcq(f + "Liam says, “10% ride a bike at both schools, so the same number of students bike.” Is he right?",
                   "No: 40 at A, 25 at B", ["Yes: 10% is 10%", "No: 25 at A, 40 at B", "Yes: 40 at each school"],
                   "School A: 10% of 400 = 40. School B: 10% of 250 = 25. The same percent of a different total is a different number."))
    v = pct_pie("How 800 visitors came to Victoria", [("BC Ferries", 60), ("Floatplane", 10), ("Plane", 25),
                                                     ("Cruise ship", 5)])
    f = fig(pie_svg(v))
    its.append(mcqv(f + "How many of the visitors came on BC Ferries?", 480, [60, 320, 48],
                    lambda x: unit(x, "visitor", "visitors"),
                    "10% of 800 = 80. 60% = 6 × 80 = 480 visitors. (320 came another way.)"))
    its.append(mcq(f + "Which conclusion does the graph support?", "More than half came on BC Ferries",
                   ["Most visitors came by plane", "A quarter came by floatplane", "The ferry sector is 60°"],
                   "BC Ferries is 60%, more than 50%. Plane is 25% (a quarter), floatplane is 10%. The ferry sector is "
                   "60% × 360° = 216°, not 60°."))
    j = pct_pie("How Jasleen uses $60", [("Savings", 40), ("Clothes", 25), ("Food", 20), ("Gifts", 15)])
    f = fig(pie_svg(j))
    its.append(mcqv(f + "Jasleen earned $60 babysitting. How much does she save?", 24, [40, 36, F(12, 5)], dollars,
                    "40% of $60 = 0.4 × $60 = $24. ($2.40 puts the decimal point in the wrong place.)"))
    its.append(mcqv(f + "Next month she earns $80 and uses the same percents. How much is for gifts?", 12, [15, 9, 68], dollars,
                    "15% of $80 = 0.15 × $80 = $12. ($9 is 15% of $60, last month.)"))
    t = pct_pie("Grade 7 Terry Fox Run: $1200", [("7A", 35), ("7B", 25), ("7C", 40)])
    its.append(mcqv(fig(pie_svg(t)) + "Three Grade 7 classes raised $1200 for the Terry Fox Run. How much did 7C raise?",
                    480, [40, 720, 400], dollars,
                    "10% of $1200 = $120. 40% = 4 × $120 = $480. ($720 is what 7A and 7B raised.)"))
    its.append(mcqv("In a circle graph, a 90° sector stands for 45 students. How many students does the whole graph show?",
                    180, [135, 90, 450], stu,
                    "90° is %s of 360°. If %s is 45 students, the whole is 4 × 45 = 180 students." % (frs(F(1, 4)), frs(F(1, 4)))))
    its.append(mcqv("In a class of 28 students, 25% take the bus. How many students in the class do not take the bus?",
                    21, [7, 25, 3], stu,
                    "25% of 28 = 28 ÷ 4 = 7 take the bus. 28 − 7 = 21 students do not. (7 answers the wrong question.)"))
    sk = pct_pie("Whistler visitors: 200 people", [("Skiing", 45), ("Snowboarding", 35), ("Other", 20)])
    f = fig(pie_svg(sk))
    its.append(mcq(f + "Which conclusion does the graph support?", "80% ski or snowboard",
                   ["35 people snowboard", "Skiing is half of the graph", "Other is 20°"],
                   "45% + 35% = 80%. Snowboarding is 35% of 200 = 70 people, not 35. Skiing is 45%, less than half. "
                   "Other is 20% × 3.6° = 72°."))
    its.append(mcqv(f + "How many more people ski than snowboard?", 20, [10, 70, 160],
                    lambda x: unit(x, "person", "people"),
                    "Skiing: 45% of 200 = 90. Snowboarding: 35% of 200 = 70. 90 − 70 = 20 people. (10 is the difference in percent.)"))
    return {"title": "Choose the right graph and draw conclusions", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    bd = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, bd)


def body_html():
    p1 = pct_pie("How 80 students get to school", [("Walk", 45), ("Bus", 25), ("Car", 20), ("Bike", 10)])
    p2 = deg_pie("Favourite sport of 40 students", [("Soccer", 144), ("Hockey", 108), ("Lacrosse", 72), ("Swimming", 36)])
    return (
        "<h2>A circle graph shows parts of a whole</h2>"
        "<p>A circle graph (also called a pie chart) splits one whole into <b>sectors</b>. "
        "Each sector shows a <b>percent</b> of the total. All the sectors add up to <b>100%</b>.</p>"
        "<figure class='sn-fig'>" + pie_svg(p1) +
        "<figcaption>45% + 25% + 20% + 10% = 100%. The Bus sector is 25%, one-quarter of the circle.</figcaption></figure>" +
        ex("Example 1", "How many of the 80 students take the bus?",
           "25%% = %s. 80 ÷ 4 = 20. (Or 0.25 × 80 = 20.)" % frs(F(1, 4)), "20 students") +
        ex("Example 2", "30% of the students in a survey chose hiking. That is 12 students. How many students were asked?",
           "30% is 12, so 10% is 12 ÷ 3 = 4. 100% is 10 × 4 = 40.", "40 students") +
        "<h2>Sector angles</h2>"
        "<p>The angles at the centre add up to <b>360°</b>. To find a sector angle, multiply the percent by 360°: "
        "25% × 360° = 0.25 × 360° = 90°. So 1% is 3.6°.</p>"
        "<h2>Make a circle graph from a table</h2>"
        "<p>1. Find the total. 2. Find each percent (count ÷ total). 3. Find each angle (percent × 360°, or "
        "360° ÷ total for each person). 4. Check: the percents add to 100% and the angles add to 360°. "
        "5. Draw each angle with a protractor, give the graph a title and label each sector.</p>" +
        table(["Sport", "Students", "Percent", "Angle"], [
            ["Soccer", "16", "16 ÷ 40 = 40%", "40% × 360° = 144°"],
            ["Hockey", "12", "30%", "108°"],
            ["Lacrosse", "8", "20%", "72°"],
            ["Swimming", "4", "10%", "36°"],
            ["Total", "40", "100%", "360°"]]) +
        "<figure class='sn-fig'>" + pie_svg(p2) +
        "<figcaption>The table drawn as a circle graph: each student is 360° ÷ 40 = 9°.</figcaption></figure>"
        "<h2>Choose the right graph</h2>"
        "<p>Use a circle graph when the data are parts of <b>one whole</b>: how a class gets to school, how a day or "
        "a budget is spent. Use a line graph for change over time, and a bar graph to compare amounts that are not "
        "parts of a whole. When two circle graphs have different totals, a bigger sector does not always mean more people: "
        "25% of 400 = 100, and 40% of 250 = 100.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Drawing 25% as 25°", "Multiply by 3.6: 25% × 360° = 90°"],
            ["Sectors that add up to 105% or 350°", "Check the totals: 100% and 360°"],
            ["Reading 25% as 25 students", "Find 25% of the total: 25% of 80 = 20"],
            ["Using 100 instead of 360 for angles", "Angles add to 360°; percents add to 100%"],
            ["Saying a bigger sector always means more people", "Work out the numbers when the totals are different"],
        ])
    )


FAQ = [
    {"q": "How do you make a circle graph in Grade 7?",
     "a": "Find the total, change each count to a percent, then multiply each percent by 360° to get the sector angle. Check that the percents add to 100% and the angles add to 360°, then draw the angles with a protractor."},
    {"q": "How do you find the angle of a sector from a percent?",
     "a": "Multiply the percent by 360°. For example, 25% × 360° = 0.25 × 360° = 90°, so a 25% sector is a right angle, not 25°."},
    {"q": "How do you find the number of people from a circle graph?",
     "a": "Find the percent of the total. If 25% of 80 students take the bus, 0.25 × 80 = 20 students take the bus."},
    {"q": "Are circle graphs on the Grade 7 FSA?",
     "a": "Circle graphs are part of the BC Grade 7 math curriculum, and the Grade 7 FSA numeracy section asks students to read and use data. Reading percents, finding amounts and drawing conclusions from graphs is good FSA practice."},
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
    rnd = random.Random(37814)
    sets = [set_read(), set_amounts(), set_degrees(), set_make(), set_problems()]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len({plain(c) for c in it["c"]}) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1, it["q"]
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-7", "slug": "circle-graphs", "sort": 14,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 7 Circle Graphs",
        "seo_title": "Grade 7 Circle Graphs Worksheets: Percents, Sector Angles and Conclusions (Free, with Answer Key, BC Curriculum)",
        "short_title": "Circle graphs",
        "domain": "Data and probability",
        "standard_code": "Grade 7: Data and probability",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/7/core",
        "standard_text": "Circle graphs",
        "meta_desc": "Free Grade 7 math worksheets on circle graphs for the BC curriculum: read sectors in percents, find amounts like 25% of 80 students, change percents to sector angles, make a circle graph from a table and draw conclusions. 100 questions with an answer key, good FSA practice.",
        "key_big": "A circle graph shows parts of one whole: the percents add to 100% and the angles add to 360°.",
        "key_sub": "Sector angle = percent × 360°, so 25% is 90°, not 25°. Number of people = percent × total, so 25% of 80 students is 20 students.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "circle graph")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
