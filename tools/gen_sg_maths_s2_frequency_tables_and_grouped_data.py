# -*- coding: utf-8 -*-
"""
SG Secondary 2 Maths: Frequency Tables and Charts (Sec 2 Statistics)
  python3 gen_sg_maths_s2_frequency_tables_and_grouped_data.py
Mean, median, mode and range from a frequency table; grouped frequency tables (modal class, estimated
mean, class containing the median); pie chart angles; and choosing and reading charts.
Wrong answers come from real mistakes: adding the frequencies and dividing by the number of rows, giving
the highest frequency as the mode, using class boundaries instead of midpoints, and dividing 360 by the
wrong total.
"""
import random
from fractions import Fraction as F
from sg_sec import ordinal, num, mcq, B, S, make, lesson, collect, QN, T, table, svg_wrap, text, fig, INK
import math

R = random.Random(821700)


def freq_table(xs, fs, head="Number"):
    return table([head, "Frequency"], [[num(x), str(f)] for x, f in zip(xs, fs)])


def make_data(r):
    h, start = r.choice([("Number of pets", 0), ("Goals scored", 0), ("Number of siblings", 0), ("Books read", 1),
                         ("Number of cars", 0), ("Shoe size", 3), ("Score out of 10", 5)])
    xs = list(range(start, start + r.choice([4, 5])))
    fs = [r.randint(1, 12) for _ in xs]
    return xs, fs, h


# ------------------------------------------------------------ set 1: mean from a frequency table
def one_mean(r):
    xs, fs, h = make_data(r)
    n = sum(fs)
    tot = sum(x * f for x, f in zip(xs, fs))
    m = F(tot, n)
    if m.denominator not in (1, 2, 4, 5, 10, 20, 25):
        return None
    q = "The table shows data for %d people. Find the %s.%s" % (n, B("mean"), freq_table(xs, fs, h))
    e = "Multiply each value by its frequency and add: %s = %d. Divide by the total frequency %d: <b>%s</b>." % (
        " + ".join("%d × %d" % (x, f) for x, f in zip(xs, fs)), tot, n, num(m))
    return QN(q, m, [F(n, len(xs)), F(sum(xs), len(xs)), F(tot, len(xs))], e, near=(F(1, 2), F(-1, 2)))


# ------------------------------------------------------------ set 2: median, mode, range
def one_mmr(r):
    xs, fs, h = make_data(r)
    n = sum(fs)
    kind = r.randint(0, 2)
    if kind == 0:
        mx = max(fs)
        if fs.count(mx) > 1:
            return None
        mode = xs[fs.index(mx)]
        q = "Find the %s.%s" % (B("mode"), freq_table(xs, fs, h))
        return QN(q, mode, [mx, xs[len(xs) // 2] if xs[len(xs) // 2] != mode else xs[0], max(xs)], "The mode is the value with the highest frequency (%d): <b>%s</b>." % (mx, num(mode)))
    if kind == 1:
        q = "Find the %s.%s" % (B("range"), freq_table(xs, fs, h))
        rg = max(xs) - min(xs)
        return QN(q, rg, [max(fs) - min(fs), max(xs), n], "Range = largest value − smallest value = %d − %d = <b>%d</b>. (Use the values, not the frequencies.)" % (max(xs), min(xs), rg))
    data = []
    for x, f in zip(xs, fs):
        data += [x] * f
    if n % 2 == 0:
        med = F(data[n // 2 - 1] + data[n // 2], 2)
        pos = "%s and %s values" % (ordinal(n // 2), ordinal(n // 2 + 1))
    else:
        med = F(data[n // 2])
        pos = "%s value" % ordinal((n + 1) // 2)
    q = "Find the %s.%s" % (B("median"), freq_table(xs, fs, h))
    e = "There are %d values. The median is the %s in order. Counting through the frequencies gives <b>%s</b>." % (n, pos, num(med))
    return QN(q, med, [F(n + 1, 2), xs[len(xs) // 2] if xs[len(xs) // 2] != med else xs[0], F(sorted(fs)[len(fs) // 2])], e)


# ------------------------------------------------------------ set 3: grouped data
def one_grouped(r):
    w = r.choice([5, 10, 20])
    start = r.choice([0, 10, 20, 40])
    k = r.choice([4, 5])
    groups = [(start + i * w, start + (i + 1) * w) for i in range(k)]
    fs = [r.randint(2, 15) for _ in groups]
    n = sum(fs)
    label = r.choice(["Height (cm)", "Time (minutes)", "Mass (kg)", "Score"])
    tbl = table([label, "Frequency"], [["%d &lt; <i>x</i> ≤ %d" % g, str(f)] for g, f in zip(groups, fs)])
    kind = r.randint(0, 2)
    if kind == 0:
        mx = max(fs)
        if fs.count(mx) > 1:
            return None
        g = groups[fs.index(mx)]
        right = "%d &lt; <i>x</i> ≤ %d" % g
        others = ["%d &lt; <i>x</i> ≤ %d" % gg for gg in groups if gg != g]
        return T("What is the %s?%s" % (B("modal class"), tbl), right, others[:3], "The modal class has the highest frequency (%d): <b>%s</b>." % (mx, right))
    if kind == 1:
        mids = [F(a + b, 2) for a, b in groups]
        est = sum(m * f for m, f in zip(mids, fs)) / n
        if est.denominator > 100 and (est * 10).denominator != 1:
            est_r = F(round(float(est), 1)).limit_denominator(10)
        else:
            est_r = est
        est_r = F(str(round(float(est), 1)))
        q = "Estimate the mean, to 1 decimal place.%s" % tbl
        wrong_upper = sum(b * f for (a, b), f in zip(groups, fs)) / F(n)
        wrong_rows = sum(m * f for m, f in zip(mids, fs)) / F(len(groups))
        e = "Use the midpoints (%s). Σ(midpoint × frequency) = %s. ÷ %d = %s… ≈ <b>%s</b>." % (
            ", ".join(num(m) for m in mids), num(sum(m * f for m, f in zip(mids, fs))), n, "{:.3f}".format(float(est)), num(est_r))
        return QN(q, est_r, [F(str(round(float(wrong_upper), 1))), F(str(round(float(wrong_rows), 1))), F(str(round(float(est) + w / 2.0 + 0.3, 1)))], e)
    target = (n + 1) / 2.0
    cum = 0
    for g, f in zip(groups, fs):
        cum += f
        if cum >= target:
            mg = g
            break
    right = "%d &lt; <i>x</i> ≤ %d" % mg
    others = ["%d &lt; <i>x</i> ≤ %d" % gg for gg in groups if gg != mg]
    return T("Which class contains the %s?%s" % (B("median"), tbl), right, others[:3],
             "There are %d values, so the median is about the %s value. Adding the frequencies, it is in <b>%s</b>." % (n, num(F(n + 1, 2)), right))


# ------------------------------------------------------------ set 4: pie charts
def pie_svg(fs, labels):
    tot = sum(fs)
    cx, cy, rr = 110, 110, 90
    cols = ["#1f5fa8", "#c0392b", "#2e8b57", "#d4a017", "#7d3c98"]
    s = []
    a0 = -90.0
    for i, f in enumerate(fs):
        a1 = a0 + 360.0 * f / tot
        x0, y0 = cx + rr * math.cos(math.radians(a0)), cy + rr * math.sin(math.radians(a0))
        x1, y1 = cx + rr * math.cos(math.radians(a1)), cy + rr * math.sin(math.radians(a1))
        large = 1 if a1 - a0 > 180 else 0
        s.append("<path d='M%d %d L%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z' fill='%s' stroke='#fff' stroke-width='2'/>" % (cx, cy, x0, y0, rr, rr, large, x1, y1, cols[i]))
        mid = math.radians((a0 + a1) / 2)
        s.append(text(cx + rr * 0.62 * math.cos(mid), cy + rr * 0.62 * math.sin(mid) + 5, "%d°" % round(360.0 * f / tot), 13, col="#fff"))
        a0 = a1
    for i, l in enumerate(labels):
        s.append("<rect x='225' y='%d' width='14' height='14' fill='%s'/>" % (40 + i * 24, cols[i]))
        s.append(text(245, 52 + i * 24, l, 13, anchor="start", col=INK))
    return svg_wrap(340, 220, "".join(s), "pie chart")


def one_pie(r):
    tot = r.choice([20, 30, 36, 40, 45, 60, 72, 90, 120, 180])
    k = r.choice([3, 4])
    cuts = sorted(r.sample(range(1, tot), k - 1))
    fs = [b - a for a, b in zip([0] + cuts, cuts + [tot])]
    if any(f * 360 < 30 * tot for f in fs) or any((360 * f) % tot for f in fs):
        return None
    labels, ctx = r.choice([(["Bus", "Car", "Walk", "Bike"], "how they travel to work"), (["Pizza", "Pasta", "Curry", "Salad"], "their favourite food"),
                            (["Red", "Blue", "Green", "Yellow"], "their favourite colour")])
    labels = labels[:k]
    i = r.randrange(k)
    ang = 360 * fs[i] // tot
    if r.random() < 0.55:
        q = "%d people were asked %s. %d said %s. What angle would this be on a pie chart?" % (tot, ctx, fs[i], B(labels[i].lower()))
        e = "Each person is 360 ÷ %d = %s°. %d × %s = <b>%d°</b>." % (tot, num(F(360, tot)), fs[i], num(F(360, tot)), ang)
        return QN(q, ang, [fs[i], F(360, fs[i]) if 360 % fs[i] == 0 else ang + 10, F(fs[i] * 100, tot) if F(fs[i] * 100, tot).denominator == 1 else ang - 10], e, unit="°")
    q = "The pie chart shows the choices of %d pupils. How many chose %s?%s" % (tot, B(labels[i].lower()), fig(pie_svg(fs, labels)))
    e = "%d° out of 360°: %d ÷ 360 × %d = <b>%d</b>." % (ang, ang, tot, fs[i])
    return QN(q, fs[i], [ang, F(ang, 10) if ang % 10 == 0 and ang // 10 != fs[i] else fs[i] + 3, F(ang * 100, 360) if (ang * 100) % 360 == 0 else fs[i] * 2], e)


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    data = [
        ("Which chart is best for showing how a city's temperature changes through a day?", "A line graph", ["A pie chart", "A pictogram", "A Venn diagram"], "Change over time is best shown on a <b>line graph</b>."),
        ("Which chart is best for showing what fraction of a budget is spent on each item?", "A pie chart", ["A line graph", "A scatter graph", "A frequency polygon"], "Parts of a whole are best shown on a <b>pie chart</b>."),
        ("In a pie chart, a sector of 90° represents 15 people. How many people are there altogether?", "60", ["15", "90", "24"], "90° is a quarter of 360°, so the total is 4 × 15 = <b>60</b>."),
        ("In a pie chart of 40 pupils, how many degrees represent 1 pupil?", "9°", ["40°", "0.11°", "320°"], "360 ÷ 40 = <b>9°</b>."),
        ("A frequency table has values 1, 2, 3 with frequencies 4, 5, 1. What is the mean?", "1.7", ["2", "3.3", "5.7"], "(4 + 10 + 3) ÷ 10 = 17 ÷ 10 = <b>1.7</b>."),
        ("A frequency table has values 0, 1, 2, 3 with frequencies 6, 9, 3, 2. What is the median?", "1", ["1.5", "4.5", "9"], "20 values; the 10th and 11th are both 1 (the 7th to 15th values are 1). Median = <b>1</b>."),
        ("Why is the mean from a grouped frequency table only an estimate?", "Because we do not know the exact values in each class", ["Because we round the answer", "Because the classes are different widths", "Because the frequencies are estimates"],
         "We use the midpoint of each class instead of the real values, so it is <b>an estimate</b>."),
        ("The midpoint of the class 20 &lt; <i>x</i> ≤ 30 is…", "25", ["20", "30", "10"], "(20 + 30) ÷ 2 = <b>25</b>."),
        ("Two pie charts show different numbers of pupils: 30 in class A and 60 in class B. The “walk” sector is 120° in both. Which class has more walkers?", "Class B", ["Class A", "They are the same", "You cannot tell"],
         "A: 120/360 × 30 = 10. B: 120/360 × 60 = 20. So <b>class B</b> (the angles are the same, but the totals are different)."),
        ("A bar chart's vertical axis starts at 50 instead of 0. Why could this be misleading?", "It makes small differences look large", ["It makes the bars too wide", "It hides the mode", "It changes the data"],
         "Starting above zero <b>makes small differences look large</b>."),
        ("Which average can you find from a grouped frequency table exactly?", "None of them exactly — only the modal class", ["The mean", "The median", "The range"],
         "Without the raw data you can only give the modal class and estimates of the others: <b>only the modal class</b>."),
        ("A table shows shoe sizes 4, 5, 6, 7 with frequencies 3, 8, 6, 3. What is the mode?", "5", ["8", "6", "5.5"], "Size 5 has the highest frequency (8): <b>5</b>."),
        ("A table shows shoe sizes 4, 5, 6, 7 with frequencies 3, 8, 6, 3. How many people are there?", "20", ["22", "4", "4 people"], "3 + 8 + 6 + 3 = <b>20</b>."),
        ("A table shows shoe sizes 4, 5, 6, 7 with frequencies 3, 8, 6, 3. What is the mean shoe size?", "5.45", ["5.5", "5", "27.25"], "(12 + 40 + 36 + 21) ÷ 20 = 109 ÷ 20 = <b>5.45</b>."),
        ("In a pie chart, the angles for three groups are 150°, 120° and <i>x</i>. Find <i>x</i>.", "90°", ["270°", "30°", "60°"], "360 − 150 − 120 = <b>90°</b>."),
        ("A survey of 72 people is shown in a pie chart. The “yes” sector is 200°. How many said yes?", "40", ["200", "36", "28"], "200 ÷ 360 × 72 = <b>40</b>."),
        ("What is the total frequency in a pie chart that uses 6° for each person?", "60", ["6", "360", "2160"], "360 ÷ 6 = <b>60</b>."),
        ("Which is the modal class: 0–10 (freq 7), 10–20 (freq 12), 20–30 (freq 9)?", "10–20", ["0–10", "20–30", "12"], "The class with the highest frequency, 12: <b>10–20</b>."),
        ("A frequency table has values 2, 4, 6 with frequencies 1, 1, 8. Which is larger, the mean or the median?", "The median (6) is larger than the mean (5.4)", ["The mean is larger", "They are equal", "You cannot tell"],
         "Mean = (2 + 4 + 48) ÷ 10 = 5.4. Median = 6. So <b>the median</b> is larger."),
        ("What does each bar in a bar chart of frequencies show?", "How many times each value or category occurs", ["The total of all the data", "The mean of the data", "The percentage of the total"],
         "The height of a bar is the frequency: <b>how many times</b> that value or category occurs."),
    ]
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p>For a frequency table, the <b>total frequency</b> is how many values there are. "
        "<b>Mean</b> = Σ(value × frequency) ÷ total frequency. The <b>mode</b> is the value with the highest frequency. "
        "For the <b>median</b>, count through the frequencies to the middle value.</p>"
        "<p>For <b>grouped</b> data, use the midpoint of each class to <b>estimate</b> the mean. The modal class has the highest frequency.</p>"
        "<p>For a <b>pie chart</b>, each item gets 360° ÷ total frequency.</p>",
        [("Values 1, 2, 3 have frequencies 5, 3, 2. Find the mean.", ["Σ = 5 + 6 + 6 = 17.", "17 ÷ 10."], "1.7"),
         ("30 people are surveyed and 8 choose walking. Find the pie chart angle.", ["360 ÷ 30 = 12° per person.", "8 × 12."], "96°")],
        ["Adding the frequencies and dividing by the number of rows instead of finding Σ(value × frequency).",
         "Giving the highest frequency as the mode instead of its value.",
         "Using the end of each class instead of the midpoint to estimate the mean.",
         "Dividing 360 by the number of categories instead of the total frequency."])


def main():
    sets = [S("Mean from a frequency table", collect(one_mean, 20, R)),
            S("Median, mode and range", collect(one_mmr, 20, R)),
            S("Grouped frequency tables", collect(one_grouped, 20, R)),
            S("Pie charts", collect(one_pie, 20, R)),
            S("Choosing and reading charts", problems())]
    make(2, "frequency-tables-and-grouped-data", 16, "S1",
         "Frequency Tables, Grouped Data and Pie Charts",
         "Secondary 2 Frequency Table Worksheets: Mean from a Table, Grouped Data, Modal Class and Pie Charts",
         "Frequency tables and charts",
         "Construct and interpret appropriate tables, charts, and diagrams, including frequency tables, bar charts, pie "
         "charts, and pictograms for categorical data, and vertical line (or bar) charts for ungrouped and grouped "
         "numerical data; describe, interpret and compare observed distributions using appropriate measures of central "
         "tendency and spread.",
         "Free Secondary 2 statistics worksheets: mean, median, mode and range from a frequency table, grouped data with modal "
         "class and estimated mean, pie chart angles and choosing charts. 100 questions with answers.",
         "Mean from a table = Σ(value × frequency) ÷ total frequency.",
         "For grouped data, use the midpoints to estimate the mean. For a pie chart, each item is 360° ÷ total.",
         body(),
         [("How do I find the mean from a frequency table?", "Multiply each value by its frequency, add these up, and divide by the total frequency."),
          ("Why is the mean of grouped data an estimate?", "Because you use the midpoint of each class, not the exact values."),
          ("What is the modal class?", "The class (group) with the highest frequency."),
          ("How do I work out pie chart angles?", "Divide 360° by the total frequency to get the angle for one item, then multiply by each frequency.")],
         sets, R)


if __name__ == "__main__":
    main()
