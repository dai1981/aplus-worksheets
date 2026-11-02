# -*- coding: utf-8 -*-
"""
Canada (British Columbia) Grade 9 Math: Statistics in society
(BC Mathematics Curriculum, Mathematics 9, Content — Data and probability: "statistics in society")
  python3 tools/gen_cabc_math_g9_statistics.py
Population and sample (census or sample, estimating a population from a random sample, capture–recapture),
bias in survey questions and samples (leading and loaded questions, missing choices, voluntary and non-response
bias, privacy), sampling methods (simple random, systematic, stratified, cluster, convenience, voluntary
response; pictures A–D), reading statistics in the news (margin of error “19 times out of 20”, sponsors,
percent change, rates and counts, correlation and causation) and misleading graphs and conclusions in BC
contexts (scales that do not start at 0, pictures scaled by area, mean pulled by outliers, small or biased
samples). Wrong answers come from real mistakes, above all “a small or biased sample represents everyone”,
the sample count used for the population, a count read as a percent, and bars judged by height.
Every number is checked with fractions.Fraction. Graphs are drawn exactly from the data.
Canadian English, SI number spacing (4536, 12 000 with a no-break space). HTML attributes use single quotes.
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-9")
UPDATED = "2026-11-02"
INK = "#2b2b2b"
GREEN = "#006633"
BAR = "#2e8b57"
GRID = "#d5ddd8"
GRID2 = "#9fb0a5"
DOT_ON = "#2e8b57"
DOT_OFF = "#ffffff"
FONT = "Arial, Helvetica, sans-serif"
M = "−"
NBSP = " "


# ------------------------------------------------------------ numbers
def num(x):
    """BC style: no separator for 4 digits, no-break space for 5+; up to 3 decimal places; real minus sign."""
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


def dollars(x):
    x = F(x)
    if x.denominator == 1:
        return "$" + num(x)
    c = int(x * 100)
    assert F(c, 100) == x
    return "$%s.%02d" % (num(c // 100), c % 100)


def unit(v, one, many):
    return "%s %s" % (num(v), one if F(v) == 1 else many)


def stu(v):
    return unit(v, "student", "students")


def ppl(v):
    return unit(v, "person", "people")


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def mean(v):
    return sum(F(x) for x in v) / len(v)


def median(v):
    s = sorted(F(x) for x in v)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


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
    return len(plain(str(t))) * fs * (0.62 if bold else 0.58)


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK, extra=""):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, extra, t))


def line(x1, y1, x2, y2, col=INK, w=1):
    return "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%s'/>" % (x1, y1, x2, y2, col, w)


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


# ------------------------------------------------------------ sample pictures: 4 homerooms (rows) × 10 students
ROWS, COLS = 4, 10
SAMPLES = {
    # 10 students each; (row, col)
    "random": [(0, 2), (0, 6), (0, 9), (1, 4), (2, 0), (2, 3), (2, 8), (3, 1), (3, 5), (3, 7)],
    "systematic": [divmod(i, COLS) for i in range(3, ROWS * COLS, 4)],          # every 4th student in the list
    "cluster": [(2, c) for c in range(COLS)],                                    # one whole homeroom
    "convenience": [(r, c) for r in (0, 1) for c in range(5)],                   # the 10 nearest the door
}
for _k, _v in SAMPLES.items():
    assert len(_v) == 10 and len(set(_v)) == 10, _k
assert SAMPLES["systematic"] == [(0, 3), (0, 7), (1, 1), (1, 5), (1, 9), (2, 3), (2, 7), (3, 1), (3, 5), (3, 9)]


def dots_svg(panels, labels, label, door=False):
    """Several panels of 4 × 10 dots side by side; chosen students are filled. Labels under each panel."""
    r, pitch = 5, 14
    pw = (COLS - 1) * pitch + 2 * r
    gap = 26
    top = 22 if door else 4
    s = []
    for pi, chosen in enumerate(panels):
        x0 = pi * (pw + gap) + 2
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='none' stroke='%s' stroke-width='1' rx='4'/>"
                 % (x0 - 2, top - 4, pw + 4 + 4, (ROWS - 1) * pitch + 2 * r + 8, GRID2))
        if door:
            s.append(text(x0, top - 8, "Door", 14, anchor="start"))
        for rr in range(ROWS):
            for cc in range(COLS):
                on = (rr, cc) in chosen
                s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='1.3'/>"
                         % (x0 + 2 + r + cc * pitch, top + r + rr * pitch, r, DOT_ON if on else DOT_OFF, INK))
        ly = top + (ROWS - 1) * pitch + 2 * r + 24
        s.append(text(x0 + 2 + pw / 2, ly, labels[pi], 16 if len(labels[pi]) == 1 else 14, bold=True))
    W = len(panels) * (pw + gap) - gap + 8
    H = top + (ROWS - 1) * pitch + 2 * r + 32
    for lab in labels:
        assert tw(lab, 14, True) < pw + gap, lab
    return svg_wrap(0, 0, W, H, "".join(s), label)


PIC_ORDER = ["random", "systematic", "cluster", "convenience"]
PIC_NOTE = {
    "random": "is a simple random sample: the dots are scattered with no pattern.",
    "systematic": "is a systematic sample: every 4th student in the list.",
    "cluster": "is a cluster sample: one whole homeroom.",
    "convenience": "is a convenience sample: the 10 students closest to the door.",
}


def pic_item(kind, lead):
    others = [k for k in PIC_ORDER if k != kind]

    def build(t):
        order = others[:t] + [kind] + others[t:]
        L = "ABCD"
        q = (fig(dots_svg([SAMPLES[k] for k in order], list(L), "sample pictures A, B, C and D: 4 homerooms of 10 students",
                          door=True)) + lead)
        e = "Picture %s %s " % (L[t], PIC_NOTE[kind])
        e += " ".join("Picture %s %s" % (L[i], PIC_NOTE[k]) for i, k in enumerate(order) if k != kind)
        return {"q": q, "c": ["A", "B", "C", "D"], "a": t, "e": e}
    return {"_build": build}


# ------------------------------------------------------------ set 1: population and sample
def set_population():
    its = []
    q0 = ("A Burnaby secondary school with 1200 students wants to know what its students think of a new lunch menu. "
          "It asks 150 students. ")
    its.append(mcq(q0 + "What is the <b>population</b>?", "All 1200 students",
                   ["The 150 students asked", "Everyone in Burnaby", "The cafeteria staff"],
                   "The population is the whole group you want to learn about: all 1200 students at the school. "
                   "(The 150 students asked are the sample.)"))
    its.append(mcq(q0 + "What is the <b>sample</b>?", "The 150 students asked",
                   ["All 1200 students", "The lunch menu", "Everyone in Burnaby"],
                   "The sample is the part of the population that is actually asked: the 150 students."))
    its.append(mcq("What is a <b>census</b>?", "Data from every member", ["Data from a small group", "A survey of volunteers",
                                                                          "A graph of the data"],
                   "A census collects data from every member of the population. A sample uses only part of it."))
    its.append(mcq("Which situation needs a census, not a sample?", "Counting votes in an election",
                   ["Finding teens’ favourite snack", "Testing how long batteries last", "Tasting soup for salt"],
                   "In an election every vote must be counted, so all of the data are needed. "
                   "In the other cases a sample is enough (or testing every item would use them all up)."))
    its.append(mcq("A company wants to know how long its batteries last. Why does it test a sample, not every battery?",
                   "Testing uses up the batteries", ["A sample is always exact", "Every battery is different",
                                                     "A census costs nothing"],
                   "To find how long a battery lasts, you must run it until it is dead. "
                   "Testing every battery would leave none to sell."))
    its.append(mcq("Why do people use a sample more often than a census?", "It saves time and money",
                   ["It is always more accurate", "It includes everyone", "It needs no planning"],
                   "Asking everyone in a large population is slow and costly. A well-chosen sample gives a good estimate "
                   "much faster. (A sample does not include everyone, so it is not always more accurate.)"))
    its.append(mcq("A researcher wants the mean height of Grade 9 students in BC. What is the population?",
                   "All Grade 9 students in BC", ["One Grade 9 class", "All students in BC", "All teens in Canada"],
                   "The question is about Grade 9 students in BC, so that whole group is the population. "
                   "One class would be a sample."))
    its.append(mcq("BC Ferries wants to know how its passengers rate the food on board. What is the population?",
                   "People who ride BC Ferries", ["Everyone in BC", "The ferry workers", "People on Vancouver Island"],
                   "The question is about passengers, so the population is the people who travel on BC Ferries."))
    its.append(mcq("Which of these is a sample, not a census?", "Asking every 10th shopper at a mall",
                   ["Asking every student in a class", "Counting every car on a ferry", "Measuring every player on a team"],
                   "Asking every 10th shopper uses only part of the shoppers, so it is a sample. "
                   "The others collect data from every member of their group."))
    its.append(mcq("A school has 900 students. Which sample will most likely give results close to the whole school?",
                   "90 students chosen at random", ["9 students chosen at random", "90 friends of the principal",
                                                    "The 30 students in chess club"],
                   "A sample should be random and big enough. 9 students is too small, and the principal’s friends or the "
                   "chess club are not like the whole school (biased)."))
    assert F(30, 80) * 1200 == 450
    its.append(mcqv("In a random sample of 80 of the 1200 students at a Surrey school, 30 said they bike to school. "
                    "About how many students in the whole school bike?", 450, [30, 360, 1170], stu,
                    "In the sample, %s = 37.5%% bike. 37.5%% of 1200 = 0.375 × 1200 = 450 students. "
                    "(30 is only the sample, 360 treats 30 as 30%%, and 1170 subtracts.)" % fr(30, 80)))
    assert F(85, 250) == F(34, 100)
    its.append(mcqv("In a random sample of 250 Kelowna residents, 85 said they go to the beach every week in summer. "
                    "What percent of the sample is that?", 34, [85, 66, F(17, 2)], pct,
                    "%s = 85 ÷ 250 = 0.34 = 34%%. (85%% reads the count as a percent, 66%% is the rest, "
                    "and 8.5%% puts the decimal point in the wrong place.)" % fr(85, 250)))
    assert F(40, 100) * 120000 == 48000
    its.append(mcqv("A random sample shows that 40% of adults in a city of 120 000 hike at least once a month. "
                    "About how many adults is that?", 48000, [4800, 480000, 72000], ppl,
                    "40% of 120 000 = 0.4 × 120 000 = 48 000 people. "
                    "(4800 and 480 000 have the place value wrong, and 72 000 is the other 60%.)"))
    its.append(mcq("Why might a random sample give a slightly different result from the whole population?",
                   "Only part of it was asked", ["The math must be wrong", "Samples are always biased",
                                                 "The population is too small"],
                   "A sample includes only some members, so its result is an estimate. "
                   "Different random samples give slightly different results."))
    its.append(mcq("Two random samples of 50 students from the same school give 22 and 26 students who walk. What does this show?",
                   "Sample results vary a little", ["One survey must be wrong", "Both samples are biased",
                                                    "The school has 48 walkers"],
                   "Random samples of the same population give slightly different results. This is called sampling "
                   "variability. Neither result is wrong."))
    its.append(mcq("What usually happens when a random sample is made larger?", "Results get closer to the population",
                   ["Results match it exactly", "The sample becomes biased", "Nothing changes"],
                   "A bigger random sample usually gives an estimate closer to the true value. "
                   "It is still an estimate, not an exact match."))
    its.append(mcq("Ji-woo asked 5 friends about a new movie, and 4 liked it. He says, “80% of Grade 9 students like this movie.” "
                   "What is the main problem?", "The sample is small and not random",
                   ["4 of 5 is not 80%", "He needed to ask 6 friends", "Nothing is wrong"],
                   "4 ÷ 5 = 80% is correct for his friends. But 5 friends are too few, and friends often like the same "
                   "things, so the result does not represent all Grade 9 students."))
    its.append(mcq("Which is NOT a good reason to use a sample?", "To make sure everyone is included",
                   ["It is faster", "It costs less", "Testing destroys the items"],
                   "A sample leaves most people out. If everyone must be included, you need a census."))
    assert F(200 * 150, 12) == 2500
    its.append(mcqv("Biologists catch, tag and release 200 salmon in a river. Later they catch 150 salmon, and 12 have tags. "
                    "Estimate the number of salmon in the river.", 2500, [16, 350, 30000],
                    lambda v: unit(v, "salmon", "salmon"),
                    "In the second catch, %s of the salmon have tags. So the 200 tagged salmon are about %s of all the salmon: "
                    "200 × %s = 200 × 12.5 = 2500 salmon. (16 is 200 × 12 ÷ 150, 350 adds 200 + 150, "
                    "and 30 000 multiplies 200 × 150.)" % (fr(12, 150), fr(12, 150), fr(150, 12))))
    assert F(58, 100) * 4500 == 2610
    its.append(mcqv("In a random sample of 200 Grade 9 students in a school district, 58% play a team sport. "
                    "The district has 4500 Grade 9 students. About how many play a team sport?", 2610,
                    [116, 1890, 261], stu,
                    "Use the sample percent for the whole district: 58% of 4500 = 0.58 × 4500 = 2610 students. "
                    "(116 is 58% of the 200 in the sample, 1890 are the others, and 261 has the place value wrong.)"))
    return {"title": "Population, sample and census", "items": its}


# ------------------------------------------------------------ set 2: bias in questions and samples
def set_bias():
    its = []
    its.append(mcq("Which survey question is biased?", "Don’t you agree the skatepark is great?",
                   ["What do you think of the skatepark?", "How often do you use the skatepark?",
                    "Should the city keep the skatepark?"],
                   "“Don’t you agree …” pushes people toward “yes”. This is a leading question. "
                   "The other questions do not suggest an answer."))
    its.append(mcq("Which survey question is fair?", "What is your favourite season?",
                   ["Isn’t summer the best season?", "Why is winter so boring?", "You love fall, right?"],
                   "A fair question does not suggest an answer. The other three each push toward one season."))
    its.append(mcq("“Most people love BC salmon. Do you like salmon?” What kind of bias is this?", "A leading question",
                   ["A sample that is too small", "A convenience sample", "There is no bias"],
                   "The first sentence tells people what most others think, which pushes them to say yes."))
    its.append(mcq("“Do you support the dangerous plan to widen the road?” Why is this question biased?",
                   "“Dangerous” pushes an answer", ["It is too short", "It asks about a road", "It has a yes/no answer"],
                   "The word “dangerous” is a loaded word. It makes the plan sound bad before people answer."))
    its.append(mcq("“Should the city stop wasting money on a new pool?” Which is the fair version?",
                   "Should the city build a new pool?", ["Shouldn’t the city stop wasting money?",
                                                         "Isn’t a new pool a waste?", "Why is a pool a bad idea?"],
                   "Remove the loaded words (“wasting money”) and ask the question in a neutral way."))
    its.append(mcq("“Do you like math and science?” What is the problem with this question?",
                   "It asks two things at once", ["It is a leading question", "It is too personal", "Nothing is wrong"],
                   "A student who likes math but not science cannot answer with yes or no. Ask two separate questions."))
    its.append(mcq("“What is your favourite sport: hockey or soccer?” What is the problem?",
                   "It leaves out other answers", ["It is too long", "It is a census", "It uses a loaded word"],
                   "A lacrosse or basketball fan has no choice to pick. Add other sports and an “Other” choice."))
    its.append(mcq("A teacher asks the class, “Raise your hand if you have ever copied homework.” Why may the results be wrong?",
                   "Students may not answer honestly", ["The class is too large", "The question is leading",
                                                        "Raising hands is random"],
                   "People often hide the truth on a personal question when others can see their answer. "
                   "An anonymous survey gives more honest results."))
    its.append(mcq("The cafeteria cook asks students face to face if they like the food. Why could the results be biased?",
                   "Students may not want to be rude", ["The cook asked too many", "Food cannot be surveyed",
                                                        "The question is too short"],
                   "Students may say “yes” to be polite to the person who made the food. "
                   "Who asks a question can change the answers."))
    its.append(mcq("A survey about adding bike lanes in Vancouver is done outside a bike shop. What is the problem?",
                   "Cyclists are over-represented", ["The sample is a census", "The question is leading",
                                                     "Vancouver is too big"],
                   "People near a bike shop are more likely to ride bikes and want bike lanes. "
                   "The sample does not represent all residents."))
    its.append(mcq("A hockey fan website asks, “Is hockey Canada’s best sport?” 92% say yes. Why can’t we trust this for all Canadians?",
                   "Mostly hockey fans answered", ["92% is too high to be real", "Websites cannot hold surveys",
                                                   "The question has two parts"],
                   "The people who visit a hockey fan site and choose to answer love hockey. "
                   "The sample is biased, so the result is true only for them."))
    its.append(mcq("A survey about how people spend their workday is done at a mall at 10 a.m. on a Tuesday. Who is left out?",
                   "People who are at work", ["People who shop", "People who like malls", "No one is left out"],
                   "At 10 a.m. on a weekday, most workers are at work, not at the mall. "
                   "The people asked are not like the whole population."))
    its.append(mcq("A survey is mailed to 500 homes and only 40 are returned. Why could the results be biased?",
                   "Those who reply may differ", ["40 is more than half", "Mail surveys are always fair",
                                                  "The homes are too far apart"],
                   "Only 8% replied. People who care a lot about the topic are more likely to reply, "
                   "so their views may not match everyone’s. This is non-response bias."))
    its.append(mcq("A survey about school start times asks only students in the 7:30 a.m. jazz band. What is wrong?",
                   "They are used to starting early", ["The sample is a census", "Jazz band is too large",
                                                       "The question is leading"],
                   "Band students who already come early may answer differently from other students. "
                   "The sample does not represent the whole school."))
    its.append(mcq("A survey about a new curfew for teens asks only parents. What is the main problem?",
                   "Teens’ views are left out", ["Parents are too busy", "The survey is a census",
                                                 "Curfews cannot be surveyed"],
                   "The rule affects teens, but no teens were asked. The sample leaves out an important group."))
    its.append(mcq("A survey form asks for each student’s name, address and family income. What is the main ethical problem?",
                   "It asks for private information", ["It is too short", "It asks too few people",
                                                       "It uses a loaded word"],
                   "A survey should ask only what it needs, keep answers private, and let people skip personal questions."))
    its.append(mcq("Which sample is least likely to be biased for the favourite music of Vancouver teens?",
                   "Random teens from all city schools", ["Teens at one concert", "Teens who reply online",
                                                          "The teens in one music class"],
                   "Choosing teens at random from schools across the city gives every teen a chance to be picked. "
                   "The others pick teens who are likely to share the same taste."))
    its.append(mcq("How can you fix the bike-shop survey about bike lanes?", "Ask random residents of the city",
                   ["Ask more people at the shop", "Ask only the shop owner", "Ask cyclists online"],
                   "Asking more people at the same shop keeps the same bias. A random sample of all residents "
                   "gives drivers, walkers and cyclists a fair chance to be picked."))
    its.append(mcq("Nadia asks 200 people at a Whistler ski hill, and 180 say skiing is their favourite sport. "
                   "She says, “90% of British Columbians love skiing most.” Is her conclusion valid?",
                   "No: the sample is biased", ["Yes: 180 of 200 is 90%", "Yes: 200 is a large sample",
                                                "No: 180 of 200 is 80%"],
                   "180 ÷ 200 = 90% is correct for the people asked. But people at a ski hill are much more likely to love "
                   "skiing. A large sample does not fix a biased sample."))
    its.append(mcq("Which change would make a survey less biased?", "Choose people at random",
                   ["Ask only your friends", "Add “Don’t you agree” to the question", "Let people choose to answer"],
                   "Random selection gives every member an equal chance, so no group is favoured. "
                   "Friends and volunteers are biased samples, and “Don’t you agree” is a leading question."))
    return {"title": "Bias in survey questions and samples", "items": its}


# ------------------------------------------------------------ set 3: sampling methods
def set_methods():
    its = []
    its.append(mcq("Each student’s name is put in a hat, and 30 names are drawn. What kind of sample is this?",
                   "Simple random", ["Systematic", "Convenience", "Cluster"],
                   "Every student has the same chance of being drawn, and the names are chosen by chance. "
                   "That is a simple random sample."))
    its.append(mcq("A teacher surveys every 10th student on the school list. What kind of sample is this?",
                   "Systematic", ["Simple random", "Stratified", "Convenience"],
                   "Choosing every k-th member from a list is a systematic sample."))
    its.append(mcq("Arjun surveys the students sitting near him at lunch. What kind of sample is this?",
                   "Convenience", ["Simple random", "Systematic", "Stratified"],
                   "He asks whoever is easy to reach. That is a convenience sample, and it is often biased."))
    its.append(mcq("A news website posts a poll, and anyone who wants to can answer. What kind of sample is this?",
                   "Voluntary response", ["Simple random", "Systematic", "Cluster"],
                   "People choose themselves to answer. This is a voluntary response (self-selected) sample."))
    its.append(mcq("A school picks 3 homerooms at random and surveys every student in them. What kind of sample is this?",
                   "Cluster", ["Stratified", "Systematic", "Convenience"],
                   "The school picks whole groups (clusters) at random and asks everyone in them."))
    its.append(mcq("A school randomly picks 20 students from each grade, 8 to 12. What kind of sample is this?",
                   "Stratified", ["Cluster", "Systematic", "Convenience"],
                   "The population is split into groups (grades), and a random sample is taken from each group. "
                   "That is a stratified sample."))
    its.append(mcq("A computer picks 40 random numbers from 1 to 850 to choose student ID numbers. What kind of sample is this?",
                   "Simple random", ["Systematic", "Cluster", "Voluntary response"],
                   "Each ID has the same chance of being picked, and the picks are random."))
    its.append(mcq("BC Ferries surveys the driver of every 25th car that boards. What kind of sample is this?",
                   "Systematic", ["Cluster", "Convenience", "Stratified"],
                   "Every 25th car in line is chosen, a fixed step each time. That is a systematic sample."))
    its.append(mcq("A city randomly chooses 5 neighbourhoods and surveys every home in them. What kind of sample is this?",
                   "Cluster", ["Simple random", "Stratified", "Systematic"],
                   "Whole neighbourhoods are chosen at random, and everyone in them is asked. That is a cluster sample."))
    its.append(mcq("Which method gives every member of the population the same chance of being chosen, one by one?",
                   "Simple random", ["Convenience", "Voluntary response", "Asking your friends"],
                   "In a simple random sample, every member has an equal chance. Convenience and voluntary samples do not."))
    its.append(mcq("Why is a convenience sample often biased?", "People nearby may be alike",
                   ["It is too large", "It uses random numbers", "It includes everyone"],
                   "The people who are easy to reach (friends, people at one place) often share the same views, "
                   "so they may not represent the population."))
    its.append(mcq("Why is a voluntary response sample often biased?", "People with strong views answer",
                   ["It is always too small", "It uses a list", "A computer chooses people"],
                   "People who care a lot, often those who are very upset or very happy, are the most likely to answer."))
    assert F(1200, 60) == 20
    its.append(mcqv("A school has 1200 students on its list. For a systematic sample of 60 students, "
                    "you choose every ___th student.", 20, [60, 12, 1140], num,
                    "1200 ÷ 60 = 20, so choose every 20th student. (12 divides by 100, and 1140 subtracts.)"))
    g = {"Grade 9": 450, "Grade 10": 270, "Grade 11": 180}
    assert sum(g.values()) == 900 and F(270, 900) * 60 == 18 and F(450, 900) * 60 == 30
    its.append(mcqv("A school has 450 Grade 9, 270 Grade 10 and 180 Grade 11 students. A stratified sample of 60 takes "
                    "each grade in proportion to its size. How many Grade 10 students are in the sample?", 18, [20, 27, 30],
                    stu,
                    "Grade 10 is %s = 30%% of the school. 30%% of 60 = 18 students. "
                    "(20 splits the sample equally, 27 is 270 ÷ 10, and 30 is the Grade 9 share.)" % fr(270, 900)))
    its.append(mcq("Which method is quickest but most likely to be biased?", "Convenience", ["Simple random", "Stratified",
                                                                                        "Systematic"],
                   "A convenience sample is easy because you ask whoever is nearby, but those people may not be "
                   "like the rest of the population."))
    its.append(mcq("A teacher picks the students she thinks will give good answers. Why is this not a random sample?",
                   "The teacher chose who to ask", ["The sample is too large", "Every student was asked",
                                                    "It uses a list"],
                   "In a random sample, chance decides who is picked. Here the teacher’s choice can bias the results."))
    its.append(mcq("What is an advantage of a stratified sample?", "Every group is included",
                   ["It is the quickest method", "No list is needed", "Only volunteers answer"],
                   "Taking a random sample from each group (each grade, each region) makes sure no group is left out."))
    its.append(pic_item("systematic", "4 homerooms of 10 students, listed row by row. The filled dots are the students "
                                      "chosen. Which picture shows a <b>systematic</b> sample?"))
    its.append(pic_item("cluster", "4 homerooms of 10 students, one row each. The filled dots are the students chosen. "
                                   "Which picture shows a <b>cluster</b> sample?"))
    its.append(pic_item("convenience", "4 homerooms of 10 students. The door is at the top left. The filled dots are the "
                                       "students chosen. Which picture shows a <b>convenience</b> sample?"))
    return {"title": "Sampling methods: random, systematic, convenience and more", "items": its}


# ------------------------------------------------------------ set 4: reading statistics in the news
def set_news():
    its = []
    its.append(mcqv("An ad says, “4 out of 5 dentists recommend this toothpaste.” What percent is that?", 80, [45, 20, 4],
                    pct, "4 ÷ 5 = 0.8 = 80%. (45% just puts the digits together, and 20% is the other 1 out of 5.)"))
    assert F(38, 100) * 1500 == 570
    its.append(mcqv("A news report says that in a survey of 1500 BC adults, 38% want more SkyTrain lines. "
                    "How many adults in the survey is that?", 570, [38, 930, 5700], ppl,
                    "38% of 1500 = 0.38 × 1500 = 570 people. "
                    "(38 is the percent, 930 are the others, and 5700 has the place value wrong.)"))
    its.append(mcq("A poll says 52% of voters support a plan, “accurate to within 3 percentage points, 19 times out of 20.” "
                   "What does this mean?", "Support is likely 49% to 55%",
                   ["Support is exactly 52%", "Support is 52% to 55%", "3% of voters disagree"],
                   "52% − 3% = 49% and 52% + 3% = 55%. The true value is very likely between them "
                   "(in 19 of 20 such polls)."))
    its.append(mcq("A poll gives candidate A 48% and candidate B 46%, accurate to within 3 percentage points. "
                   "Which statement is best?", "It is too close to tell", ["A will surely win",
                                                                           "B will surely win", "A leads by 48%"],
                   "A could be 45% to 51%, and B could be 43% to 49%. The ranges overlap, so the poll cannot say "
                   "who is really ahead."))
    its.append(mcq("When does the margin of error in a random poll usually get smaller?", "When the sample is larger",
                   ["When the sample is smaller", "When people volunteer", "When the question is leading"],
                   "A larger random sample gives a more precise estimate, so the margin of error shrinks."))
    its.append(mcq("A study paid for by a candy company says candy is good for you. What should a reader ask first?",
                   "Could the sponsor affect results?", ["Is candy sweet?", "Was the study long?",
                                                         "Did they use a graph?"],
                   "When the group paying for a study gains from one result, check how the study was done "
                   "and whether others found the same thing."))
    its.append(mcq("Which headline is backed by the most trustworthy survey?", "Random sample of 2000 BC adults",
                   ["12 people asked at a café", "An online poll of 5000 readers", "One school’s Grade 9 class"],
                   "A large random sample is best. The online poll is large but self-selected, "
                   "and 12 people or one class are small and not random."))
    its.append(mcq("A headline says, “Bike thefts up 100% in our town!” Thefts went from 3 to 6. What should readers know?",
                   "Only 3 more bikes were stolen", ["Thefts went up by 100 bikes", "Thefts went down",
                                                     "100% is impossible"],
                   "From 3 to 6 is double, which is a 100% increase. But it is only 3 more bikes. "
                   "Percents can sound big when the numbers are small."))
    its.append(mcq("A report says the risk of an illness doubles, from 1 in 10 000 people to 2 in 10 000. Which is true?",
                   "The risk is still very small", ["Half of people will get it", "The risk is now 2%",
                                                    "The risk went up by 100 people"],
                   "2 in 10 000 is 0.02%. Doubling a tiny risk still gives a tiny risk."))
    assert F(46000 - 40000, 40000) == F(15, 100)
    its.append(mcqv("A museum had 40 000 visitors last year and 46 000 this year. A report calls it a big increase. "
                    "What is the percent increase?", 15, [6, 115, 46], pct,
                    "Increase: 46 000 − 40 000 = 6000. 6000 ÷ 40 000 = 0.15 = 15%. "
                    "(6 uses thousands, 115% is the new number as a percent of the old, and 46 is just the new number.)"))
    its.append(mcq("A report says Vancouver had many more car crashes than Kamloops last year. Why doesn’t this show "
                   "Vancouver’s roads are more dangerous?", "Vancouver has far more people",
                   ["Kamloops has no roads", "Crashes cannot be counted", "The years were different"],
                   "A bigger city has more drivers, so it can have more crashes even if its roads are safer. "
                   "Compare a rate, such as crashes per 1000 people."))
    its.append(mcq("A report says, “Students who eat breakfast get higher marks.” A headline says, “Breakfast makes you "
                   "smarter!” What is the problem?", "Other things may explain both",
                   ["The marks are too high", "Breakfast is not data", "Nothing is wrong"],
                   "Two things that happen together do not prove one causes the other. "
                   "For example, more sleep or a calm morning could lead to both."))
    its.append(mcq("A store ad says, “Up to 70% off!” What does this really tell you?", "Some items may be 70% off",
                   ["Everything is 70% off", "Everything is at least 70% off", "Prices went up 70%"],
                   "“Up to” means 70% is the biggest discount. Most items may have a much smaller discount."))
    its.append(mcq("A news site’s online poll finds 75% of readers want a later school start. Why is this not good evidence "
                   "about all BC students?", "Readers chose to answer", ["75% is too high", "The site is online",
                                                                         "Polls must have 100 people"],
                   "This is a voluntary response sample. The people who answer chose themselves, "
                   "and they may not be students at all."))
    its.append(mcq("A survey of one Kamloops school says 70% of its students play hockey. A headline says, "
                   "“70% of BC teens play hockey.” What is wrong?", "One school is not all of BC",
                   ["70% of one school is wrong", "Hockey is not played in BC", "The headline used a percent"],
                   "The result may be true for that school, but one school is not a random sample of all BC teens."))
    assert F(3, 8) * 600000 == 225000
    its.append(mcqv("A random survey of 800 Surrey residents found that 3 out of 8 take transit to work. If Surrey has "
                    "600 000 residents, about how many take transit?", 225000, [300, 375000, 22500], ppl,
                    "%s of 600 000 = 600 000 ÷ 8 × 3 = 225 000 people. "
                    "(300 is %s of the 800 in the sample, 375 000 are the others, and 22 500 has the place value wrong.)"
                    % (fr(3, 8), fr(3, 8))))
    assert 600000 // 8 * 3 == 225000 and F(3, 8) * 800 == 300
    its.append(mcq("A survey reports: hiking 60%, swimming 45%, biking 30%. Why can the percents add up to more than 100%?",
                   "People could pick more than one", ["The math is wrong", "Some people were not asked",
                                                       "Percents always add to 135%"],
                   "If each person can choose several activities, the same person is counted in more than one group, "
                   "so the total can pass 100%."))
    assert F(1, 4) * 3600 == 900
    its.append(mcqv("A report says “1 in 4 students at our school is in a sports club.” The school has 3600 students. "
                    "How many students is that?", 900, [4, 14400, 2700], stu,
                    "1 in 4 = %s. 3600 ÷ 4 = 900 students. (14 400 multiplies by 4, and 2700 are the other 3 in 4.)"
                    % fr(1, 4)))
    h = [520000, 560000, 590000, 610000, 3720000]
    assert mean(h) == 1200000 and median(h) == 590000
    its.append(mcq("5 condos sold on one street last month for $520 000, $560 000, $590 000, $610 000 and $3 720 000. "
                   "A news story says, “The average condo price is $1 200 000.” Which better shows a typical price?",
                   "The median, $590 000", ["The mean, $1 200 000", "The highest, $3 720 000", "The lowest, $520 000"],
                   "The mean is $6 000 000 ÷ 5 = $1 200 000, but 4 of the 5 sold for less than $620 000. "
                   "The one very expensive condo pulls the mean up. The middle value, the median, is $590 000."))
    its.append(mcq("A report says, “The average Grade 9 student sleeps 7 hours a night.” Which detail would help you "
                   "judge it most?", "How many were asked and how", ["The font of the report", "The reporter’s age",
                                                                     "The day it was posted"],
                   "Check the sample: how big it was, how it was chosen, and who was asked. "
                   "That tells you if the statistic represents everyone."))
    return {"title": "Reading statistics in the news", "items": its}


# ------------------------------------------------------------ set 5: misleading graphs and conclusions (BC)
VOTE = (["Whistler", "Victoria"], [64, 58])
SALMON_X = ["2022", "2023", "2024", "2025", "2026"]
SALMON = [12000, 12100, 12250, 12400, 12600]


def vote_svg():
    return bar_svg("Votes for the Grade 9 field trip", "Place", "Votes", VOTE[0], VOTE[1], 55, 65, 1, 5, gy=12)


def salmon_svg():
    return bline_svg("Salmon counted in a creek", "Year", "Salmon", SALMON_X, SALMON, 12000, 12600, 50, 200,
                     gy=10, slot=58)


def set_misleading():
    its = []
    f = fig(vote_svg())
    a, b = VOTE[1]
    assert (a - 55) == 3 * (b - 55)
    Vo = lambda x: unit(x, "vote", "votes")
    its.append(mcqv(f + "How many more votes did Whistler get than Victoria?", a - b, [a - 55, b - 55, a], Vo,
                    "Whistler 64, Victoria 58. 64 − 58 = 6 votes. (9 and 3 are only the parts of the bars above 55, "
                    "and 64 is Whistler’s total.)"))
    its.append(mcq(f + "The Whistler bar looks 3 times as tall. Did Whistler get 3 times as many votes?",
                   "No: 64 is not 3 × 58", ["Yes: its bar is 3 times as tall", "Yes: 64 is more than 58",
                                            "No: Victoria got more"],
                   "3 × 58 = 174, but Whistler got 64 votes. The scale starts at 55, so we see only 9 and 3 of the votes."))
    its.append(mcqv(f + "To draw a fair bar graph of this data, where should the scale start?", 0, [55, 58, 64], num,
                    "Bar heights can be compared fairly only when the scale starts at 0. Then the bars are 64 and 58 high "
                    "and look almost the same."))
    assert F(a - b, b) == F(6, 58)
    its.append(mcq(f + "Harjot says, “Whistler won by a landslide.” Is this supported?", "No: it won by only 6 votes",
                   ["Yes: its bar is much taller", "Yes: it won by 9 votes", "No: Victoria won"],
                   "64 to 58 is a close result, about 52% to 48%. The cut-off scale makes the gap look huge."))
    assert F(64, 122) > F(52, 100) and F(64, 122) < F(53, 100)
    f = fig(salmon_svg())
    S = lambda x: unit(x, "salmon", "salmon")
    its.append(mcqv(f + "How many more salmon were counted in 2026 than in 2022?", 600, [12600, 200, 12000], S,
                    "2026: 12 600. 2022: 12 000. 12 600 − 12 000 = 600 salmon. "
                    "(12 600 is the 2026 count, and 200 is only the last year.)"))
    assert F(600, 12000) == F(5, 100)
    its.append(mcqv(f + "By what percent did the count grow from 2022 to 2026?", 5, [600, 50, 60], pct,
                    "Growth = 600. 600 ÷ 12 000 = 0.05 = 5%. (600% reads the count as a percent, "
                    "50% is a decimal slip (0.5 instead of 0.05), and 60% divides by 1000 instead of 12 000.)"))
    its.append(mcq(f + "A poster says, “The salmon run has exploded!” Why is the graph misleading?",
                   "The scale starts at 12 000", ["The years are not in order", "The line goes down",
                                                  "There are too few years"],
                   "The scale starts at 12 000, so a 5% rise fills the whole graph and looks steep. "
                   "With a scale from 0, the line would look almost flat."))
    its.append(mcq("A poster shows Terry Fox Run money doubling with two pictures of a runner. The second runner is "
                   "twice as wide and twice as tall. Why is this misleading?", "It looks 4 times as big",
                   ["It should be 3 times as tall", "Runners are not data", "The money did not change"],
                   "Doubling both the width and the height makes the area 2 × 2 = 4 times as big. "
                   "The eye sees the area, so the money looks 4 times bigger instead of 2 times."))
    its.append(mcq("A bar graph’s scale is labelled 0, 10, 20, 100, 500 with equal spaces between labels. Why is it misleading?",
                   "Equal spaces show unequal amounts", ["It starts at 0", "The numbers are too big", "It has 5 labels"],
                   "The space from 0 to 10 is the same as the space from 100 to 500, but one is 10 and the other is 400. "
                   "Bars on this scale cannot be compared fairly."))
    its.append(mcq("A graph shows Okanagan peach sales only for July and August, when sales are highest. "
                   "An ad says, “Sales are always booming!” What is the problem?", "It shows only part of the year",
                   ["Peaches do not grow in BC", "The months are wrong", "The graph has a title"],
                   "Choosing only the best months hides the rest of the year. "
                   "A fair graph shows the whole time period."))
    its.append(mcq("Why is a tilted 3-D circle graph often misleading?", "Front sectors look bigger",
                   ["It has too many colours", "Its percents add to 360%", "It has no sectors"],
                   "Tilting the circle stretches the sectors at the front and squashes the ones at the back, "
                   "so equal percents do not look equal."))
    its.append(mcq("Liam surveyed 8 people at a Grouse Mountain lift line, and 7 snowboard. He says, “Most people in "
                   "Vancouver snowboard.” What is wrong?", "The sample is small and biased",
                   ["7 of 8 is not most", "He should use a circle graph", "Nothing is wrong"],
                   "7 of 8 is most of his sample, but 8 people are too few, and people in a ski lift line are much more "
                   "likely to snowboard. The result does not represent Vancouver."))
    its.append(mcq("Every summer in BC, both ice cream sales and wildfires go up. Sofia says, “Ice cream causes wildfires.” "
                   "What is the best reply?", "Hot, dry weather causes both",
                   ["She is right: the data show it", "Wildfires cause ice cream sales", "Summer has 3 months"],
                   "Two things can rise together without one causing the other. "
                   "Hot, dry weather leads to more ice cream sales and also more wildfires."))
    assert F(20, 100) * 600 == F(40, 100) * 300 == 120
    its.append(mcq("Circle graphs show that 20% of the 600 students at School A and 40% of the 300 students at School B take "
                   "the bus. A report says, “Twice as many School B students take the bus.” Is this true?",
                   "No: both have 120", ["Yes: 40% is twice 20%", "No: School A has twice as many",
                                         "You cannot tell"],
                   "School A: 20% of 600 = 120. School B: 40% of 300 = 120. The percents differ, but the totals do too."))
    w = [42000, 45000, 46000, 48000, 49000, 290000]
    assert mean(w) == 86666 + F(2, 3) and median(w) == 47000
    assert mean(w[:5]) == 46000
    its.append(mcq("A small Nanaimo company pays its 5 workers $42 000, $45 000, $46 000, $48 000 and $49 000, and its "
                   "owner $290 000. A job ad says, “Average pay here is over $86 000!” Why is this misleading?",
                   "The owner’s pay pulls up the mean", ["The mean is $46 000", "All workers earn $86 000",
                                                         "The median is $86 000"],
                   "The mean of all 6 is $520 000 ÷ 6 ≈ $86 667, but every worker earns less than $50 000. "
                   "The median, $47 000, describes a typical worker much better."))
    assert sum(w) == 520000
    its.append(mcq("In a Grade 9 class of 30, Victoria got 11 votes for the field trip, more than any other place. "
                   "Owen says, “Most of the class wants to go to Victoria.” Is this supported?",
                   "No: 11 of 30 is less than half", ["Yes: Victoria is the mode", "Yes: 11 is the most votes",
                                                      "No: Victoria lost"],
                   "Victoria got the most votes, but “most” means more than half. Half of 30 is 15, and only 11 chose Victoria."))
    assert 11 * 2 < 30
    assert F(9, 12) == F(3, 4)
    its.append(mcq("An energy drink ad says, “75% of athletes surveyed prefer our drink!” Only 12 athletes were asked, "
                   "and all were sponsored by the company. What is the best conclusion?",
                   "The claim is not reliable", ["75% of all athletes prefer it", "9 of 12 proves it is best",
                                                 "The drink is unhealthy"],
                   "75% of 12 is 9 athletes. The sample is tiny and biased: the athletes are paid by the company. "
                   "It cannot represent all athletes."))
    its.append(mcq("A graph of BC Ferries’ on-time sailings has no scale numbers on the vertical axis. Why is this a problem?",
                   "You cannot read the real values", ["The graph is too small", "Ferries have no data",
                                                       "The bars are too wide"],
                   "Without numbers on the scale, the bars only show which is bigger, not by how much. "
                   "A reader cannot check any claim."))
    assert F(4, 50) * 1000 == 80 and F(4, 50) == F(8, 100)
    its.append(mcqv("In a random sample of 50 phones from a Prince George store, 4 had cracked screens. The store has "
                    "1000 phones. About how many have cracked screens?", 80, [4, 8, 920],
                    lambda v: unit(v, "phone", "phones"),
                    "%s = 8%% of the sample. 8%% of 1000 = 80 phones. "
                    "(4 is only the sample, 8 is the percent, and 920 are the phones without cracks.)" % fr(4, 50)))
    assert F(15, 60) * 2400 == 600 and F(15, 100) * 2400 == 360
    its.append(mcqv("Zara’s random sample of 60 students at her 2400-student Victoria school finds that 15 want a new "
                    "lacrosse team. She reports, “About 15 students want lacrosse.” What is a better estimate?", 600,
                    [15, 360, 2385], stu,
                    "15 of 60 = %s = 25%%. 25%% of 2400 = 600 students. (15 is only the sample count, "
                    "360 treats 15 as 15%%, and 2385 subtracts.)" % fr(1, 4)))
    return {"title": "Word problems: misleading graphs and conclusions", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    bd = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, bd)


LVOTE = (["Sushi", "Pizza"], [46, 42])


def body_html():
    a, b = LVOTE[1]
    assert (a - 40) == 3 * (b - 40)
    assert F(45, 120) * 960 == 360
    return (
        "<h2>Population, sample and census</h2>"
        "<p>The <b>population</b> is the whole group you want to learn about. A <b>census</b> asks every member. "
        "A <b>sample</b> asks only part of the population. A sample is faster and cheaper, "
        "but it must <b>represent</b> the population.</p>" +
        ex("Example 1", "A random sample of 120 of the 960 students at a Kamloops school finds that 45 play an instrument. "
                        "Estimate how many students in the school play.",
           "In the sample, %s = 37.5%% play. 37.5%% of 960 = 0.375 × 960 = 360." % fr(45, 120),
           "about 360 students") +
        "<h2>Sampling methods</h2>" +
        table(["Method", "How people are chosen", "Biased?"], [
            ["Simple random", "By chance: names from a hat, random numbers", "Least likely"],
            ["Systematic", "Every k-th person on a list", "Usually fair"],
            ["Stratified", "A random sample from each group (each grade)", "Fair; every group is included"],
            ["Cluster", "Whole groups chosen at random (whole homerooms)", "Fair if the groups are alike"],
            ["Convenience", "Whoever is easy to reach", "Often biased"],
            ["Voluntary response", "People choose to answer (online polls)", "Often biased"],
        ]) +
        "<figure class='sn-fig'>" +
        dots_svg([SAMPLES["random"], SAMPLES["convenience"]], ["Random", "Convenience"],
                 "random sample and convenience sample of 4 homerooms", door=True) +
        "<figcaption>Each dot is a student; filled dots are chosen. A random sample is spread out. "
        "A convenience sample takes the 10 students nearest the door.</figcaption></figure>"
        "<h2>Bias</h2>"
        "<p>A survey is <b>biased</b> when it favours some answers. Look for:</p>"
        "<ul><li><b>Biased samples</b>: asking only people at a ski hill about skiing.</li>"
        "<li><b>Leading or loaded questions</b>: “Don’t you agree …?”, “the dangerous plan …”.</li>"
        "<li><b>Missing choices</b>: “hockey or soccer?” with no other option.</li>"
        "<li><b>Personal questions</b> asked in public: people may not answer honestly.</li></ul>"
        "<p>A larger sample does not fix a biased sample. Choose people at random and ask neutral questions.</p>"
        "<h2>Statistics in the news</h2>"
        "<p>Before you trust a statistic, ask: Who was asked, and how many? Was the sample random? Who paid for the study? "
        "Is it a count or a rate? Does “linked to” really mean “causes”? A poll “accurate to within 3 percentage points, "
        "19 times out of 20” means 52% is really somewhere from 49% to 55%.</p>"
        "<h2>Misleading graphs</h2>"
        "<figure class='sn-fig'>" + bar_svg("Favourite lunch", "Lunch", "Votes", LVOTE[0], LVOTE[1], 40, 48, 1, 2, gy=12) +
        "<figcaption>The scale starts at 40, so the sushi bar looks 3 times as tall. Really, sushi has only "
        "46 − 42 = 4 more votes.</figcaption></figure>"
        "<p>Check that the scale starts at 0, the steps are equal, the pictures are scaled fairly, "
        "and the whole time period is shown.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Thinking a small or biased sample represents everyone", "Use a large enough random sample from the whole population"],
            ["Using the sample count for the population (15 of 60 → “15 students”)", "Find the sample percent, then apply it: 25% of 2400 = 600"],
            ["Thinking a bigger biased sample is fine", "Fix how people are chosen, not just how many"],
            ["Judging bars by height when the scale does not start at 0", "Read the real values and subtract"],
            ["Saying one thing causes another because they rise together", "Look for another cause, like the weather"],
            ["Trusting the mean when there is an outlier", "Also look at the median"],
        ])
    )


FAQ = [
    {"q": "What is the difference between a population and a sample in Grade 9 math?",
     "a": "The population is the whole group you want to learn about, such as all students in a school. A sample is the part of the population you actually survey, such as 100 students chosen at random."},
    {"q": "What are the main sampling methods in BC Math 9?",
     "a": "Simple random, systematic (every k-th person), stratified (a random sample from each group), cluster (whole groups chosen at random), convenience and voluntary response. Random methods are least likely to be biased; convenience and voluntary samples are often biased."},
    {"q": "How do you tell if a survey question is biased?",
     "a": "A biased question pushes people toward an answer, for example “Don’t you agree …?” or loaded words like “dangerous” or “wasteful”. A fair question is neutral, asks one thing at a time and gives all reasonable choices."},
    {"q": "How can a graph be misleading?",
     "a": "Common tricks are a scale that does not start at 0, unequal steps on the scale, pictures that grow in both width and height, and showing only part of a time period. Always read the real values before you trust the shape of a graph."},
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


SPACED = re.compile(r"(?<![\d.])(\d{1,3}) (\d{3})(?![\d])")


def nbsp_fix(o):
    """Turn typed spaces in 5+ digit numbers (“12 000”, “3 720 000”) into no-break spaces."""
    if isinstance(o, str):
        parts = re.split(r"(<[^>]*>)", o)
        for i in range(0, len(parts), 2):
            prev = None
            while prev != parts[i]:
                prev = parts[i]
                parts[i] = SPACED.sub(lambda m: m.group(1) + NBSP + m.group(2), parts[i])
        return "".join(parts)
    if isinstance(o, list):
        return [nbsp_fix(x) for x in o]
    if isinstance(o, dict):
        return {k: nbsp_fix(v) for k, v in o.items()}
    return o


def gen():
    rnd = random.Random(59808)
    sets = [set_population(), set_bias(), set_methods(), set_news(), set_misleading()]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-9", "slug": "statistics-in-society", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 9 Statistics in Society: Populations, Samples, Bias and Misleading Graphs",
        "seo_title": "Grade 9 Statistics in Society Worksheets: Free Math with Answer Key (BC Curriculum)",
        "short_title": "Statistics in society",
        "domain": "Data and probability",
        "standard_code": "Grade 9: Data and probability",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/9/core",
        "standard_text": "Statistics in society",
        "meta_desc": "Free Grade 9 math worksheets for the BC curriculum on statistics in society: population and sample, bias in survey questions and samples, random, systematic, stratified, cluster and convenience sampling, reading statistics in the news, and misleading graphs and conclusions. 100 questions with an answer key.",
        "key_big": "A sample tells you about a population only if it is random, large enough and asked fair questions.",
        "key_sub": "A small or biased sample does not represent everyone, and making a biased sample bigger does not fix it. Use the sample percent to estimate the population, and check the scale, the sample and the source before you trust a graph or a headline.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    u = nbsp_fix(u)
    return mark_large(u, "(bar graph|broken-line|sample pictures)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
