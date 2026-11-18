# -*- coding: utf-8 -*-
"""
SG Secondary 4 Maths: Cumulative Frequency and Box-and-Whisker Plots (MOE syllabus S1: quartiles and percentiles;
range and interquartile range; cumulative frequency diagrams; box-and-whisker plots)
  python3 tools/gen_sg_maths_s4_cumulative_frequency_and_box_plots.py
Quartiles and interquartile range from lists, cumulative frequency tables, reading cumulative frequency curves
(median, quartiles, percentiles, numbers above a value), reading box-and-whisker plots, and comparing two sets
of data.
Wrong answers come from real mistakes: forgetting to sort the data, reading the frequency axis instead of the
value axis, using n/2 for the lower quartile, subtracting from the wrong total, and comparing medians when the
question asks about spread.
"""
import random
from sg_sec import num, S, make, lesson, collect, T, QN, fig, svg_wrap, line, text, table

R = random.Random(840600)
BLUE, RED, INK, GRID = "#1f6fd1", "#c0392b", "#2b2b2b", "#dddddd"


def med(xs):
    xs = sorted(xs)
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def quart(xs):
    xs = sorted(xs)
    n = len(xs)
    lo, hi = xs[:n // 2], xs[(n + 1) // 2:]
    return med(lo), med(xs), med(hi)


def g(v):
    return num(int(v)) if v == int(v) else ("%g" % v)


# ------------------------------------------------------------ set 1: quartiles from a list
def one_list(r):
    n = r.choice([7, 8, 9, 10, 11, 12])
    xs = [r.randint(10, 60) for _ in range(n)]
    q1, m, q3 = quart(xs)
    kind = r.choice(["q1", "q3", "iqr", "iqr", "range"])
    shown = ", ".join(str(x) for x in xs)
    if kind == "q1":
        wr = [g(med(xs[:n // 2])), g(m), g(q3)]
        return T("Find the lower quartile of: %s." % shown, g(q1), [w for w in wr if w != g(q1)][:3] + ([g(q1 + 1)] if len([w for w in wr if w != g(q1)]) < 3 else []),
                 "Sorted: %s. The lower half is %s, and its median is <b>%s</b>." % (", ".join(map(str, sorted(xs))), ", ".join(map(str, sorted(xs)[:n // 2])), g(q1)))
    if kind == "q3":
        wr = [g(med(xs[(n + 1) // 2:])), g(m), g(q1)]
        return T("Find the upper quartile of: %s." % shown, g(q3), [w for w in wr if w != g(q3)][:3] + ([g(q3 + 1)] if len([w for w in wr if w != g(q3)]) < 3 else []),
                 "Sorted: %s. The upper half is %s, and its median is <b>%s</b>." % (", ".join(map(str, sorted(xs))), ", ".join(map(str, sorted(xs)[(n + 1) // 2:])), g(q3)))
    if kind == "range":
        rg = max(xs) - min(xs)
        return QN("Find the range of: %s." % shown, rg, [q3 - q1 if q3 - q1 != rg else rg + 1, max(xs), abs(xs[-1] - xs[0]) if abs(xs[-1] - xs[0]) != rg else rg - 1],
                  "Range = largest − smallest = %d − %d = <b>%d</b>." % (max(xs), min(xs), rg))
    iqr = q3 - q1
    return T("Find the interquartile range of: %s." % shown, g(iqr), [g(max(xs) - min(xs)), g(q3 - m), g(abs(quart(xs[:])[2] - quart(xs[:])[0]) + 1)],
             "Sorted: %s. Q<sub>1</sub> = %s and Q<sub>3</sub> = %s, so IQR = %s − %s = <b>%s</b>." % (", ".join(map(str, sorted(xs))), g(q1), g(q3), g(q3), g(q1), g(iqr)))


# ------------------------------------------------------------ cumulative frequency data
def cf_data(r):
    N = r.choice([40, 60, 80, 100, 120, 200])
    w = r.choice([10, 20])
    start = r.choice([0, 20, 40]) if w == 10 else 0
    k = r.choice([5, 6])
    while True:
        cuts = sorted(r.sample(range(1, N), k - 1))
        fs = [b - a for a, b in zip([0] + cuts, cuts + [N])]
        if min(fs) >= N // 25 and max(fs) <= N // 2:
            break
    bounds = [start + w * i for i in range(k + 1)]
    cum = [0]
    for f in fs:
        cum.append(cum[-1] + f)
    return N, bounds, fs, cum


def interp_x(bounds, cum, y):
    for i in range(len(cum) - 1):
        if cum[i] <= y <= cum[i + 1]:
            if cum[i + 1] == cum[i]:
                return bounds[i]
            return bounds[i] + (bounds[i + 1] - bounds[i]) * (y - cum[i]) / (cum[i + 1] - cum[i])
    return bounds[-1]


def interp_y(bounds, cum, x):
    for i in range(len(bounds) - 1):
        if bounds[i] <= x <= bounds[i + 1]:
            return cum[i] + (cum[i + 1] - cum[i]) * (x - bounds[i]) / (bounds[i + 1] - bounds[i])
    return cum[-1]


def cf_svg(N, bounds, cum, what, guide=None):
    W, H = 360, 250
    x0, y0, pw, ph = 50, 210, 290, 185
    Xp = lambda x: x0 + (x - bounds[0]) / (bounds[-1] - bounds[0]) * pw
    Yp = lambda y: y0 - y / N * ph
    s = []
    ystep = N // 10 if N >= 100 else N // 8 if N % 8 == 0 else N // 10
    yv = 0
    while yv <= N:
        s.append(line(x0, Yp(yv), x0 + pw, Yp(yv), GRID, 1))
        s.append(text(x0 - 6, Yp(yv) + 4, num(yv), 11, anchor="end", weight=400))
        yv += ystep
    for b in bounds:
        s.append(line(Xp(b), y0, Xp(b), y0 - ph, GRID, 1))
        s.append(text(Xp(b), y0 + 16, num(b), 11, weight=400))
    s.append(line(x0, y0, x0 + pw, y0, INK, 2))
    s.append(line(x0, y0, x0, y0 - ph, INK, 2))
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='2.6'/>" % (" ".join("%.1f,%.1f" % (Xp(b), Yp(c)) for b, c in zip(bounds, cum)), BLUE))
    for b, c in zip(bounds, cum):
        s.append("<circle cx='%.1f' cy='%.1f' r='3' fill='%s'/>" % (Xp(b), Yp(c), BLUE))
    s.append(text(x0 + pw / 2, y0 + 34, what, 12))
    s.append("<text x='14' y='%d' font-size='12' font-weight='700' fill='%s' transform='rotate(-90 14 %d)' text-anchor='middle'>Cumulative frequency</text>" % (y0 - ph / 2, INK, y0 - ph / 2))
    return fig(svg_wrap(W, H + 6, "".join(s), "cumulative frequency curve"))


WHATS = [("Marks", "students", "a test"), ("Time (minutes)", "students", "time spent on homework"), ("Mass (g)", "apples", "mass"), ("Height (cm)", "plants", "height")]


# ------------------------------------------------------------ set 2: cumulative frequency tables
def one_table(r):
    N, bounds, fs, cum = cf_data(r)
    what, who, _ = r.choice(WHATS)
    rows = [["%s &lt; <i>x</i> ≤ %s" % (num(a), num(b)), num(f)] for a, b, f in zip(bounds, bounds[1:], fs)]
    tb = table([what.split(" (")[0].replace("Marks", "Mark") + " <i>x</i>", "Frequency"], rows)
    i = r.randint(2, len(fs) - 1)
    kind = r.choice(["le", "le", "gt", "cf"])
    if kind == "le":
        return QN("The table shows %s %s. How many have <i>x</i> ≤ %s?%s" % (num(N), who, num(bounds[i]), tb), cum[i], [fs[i - 1], cum[i - 1], N - cum[i]],
                  "Add the frequencies up to %s: %s = <b>%d</b> (the cumulative frequency)." % (num(bounds[i]), " + ".join(map(str, fs[:i])), cum[i]))
    if kind == "gt":
        return QN("The table shows %s %s. How many have <i>x</i> &gt; %s?%s" % (num(N), who, num(bounds[i]), tb), N - cum[i], [cum[i], fs[i], N - cum[i - 1]],
                  "Cumulative frequency up to %s is %d, so %d − %d = <b>%d</b> are above it." % (num(bounds[i]), cum[i], N, cum[i], N - cum[i]))
    return T("The table shows %s %s. Which list gives the cumulative frequencies?%s" % (num(N), who, tb), ", ".join(map(str, cum[1:])),
             [", ".join(map(str, fs)), ", ".join(map(str, [N - c for c in cum[:-1]])), ", ".join(map(str, cum[1:-1] + [cum[-1] + fs[-1]]))],
             "Keep a running total of the frequencies: <b>%s</b>. The last one equals the total, %d." % (", ".join(map(str, cum[1:])), N))


# ------------------------------------------------------------ set 3: reading cumulative frequency curves
def one_curve(r):
    N, bounds, fs, cum = cf_data(r)
    what, who, _ = r.choice(WHATS)
    pic = cf_svg(N, bounds, cum, what)
    kind = r.choice(["med", "q1", "q3", "iqr", "above", "pct"])
    q1, m, q3 = (interp_x(bounds, cum, N * t) for t in (0.25, 0.5, 0.75))
    rd = lambda v: int(round(v))
    pre = "The cumulative frequency curve shows the %s of %s %s." % (what.split(" (")[0].lower(), num(N), who)
    if kind == "med":
        return QN(pre + " Estimate the median.%s" % pic, rd(m), [rd(q1), rd(q3), rd((bounds[0] + bounds[-1]) / 2) if abs(rd((bounds[0] + bounds[-1]) / 2) - rd(m)) > 2 else rd(m) + 5],
                  "The median is at the %s-th value (half of %s). Read across from %s to the curve and down: about <b>%d</b>." % (num(N // 2), num(N), num(N // 2), rd(m)))
    if kind in ("q1", "q3"):
        v = q1 if kind == "q1" else q3
        pos = N // 4 if kind == "q1" else 3 * N // 4
        return QN(pre + " Estimate the %s quartile.%s" % ("lower" if kind == "q1" else "upper", pic), rd(v), [rd(m), rd(q3 if kind == "q1" else q1), pos],
                  "Read across from %s (%s of %s) to the curve and down: about <b>%d</b>." % (num(pos), "a quarter" if kind == "q1" else "three quarters", num(N), rd(v)))
    if kind == "iqr":
        iqr = rd(q3) - rd(q1)
        return QN(pre + " Estimate the interquartile range.%s" % pic, iqr, [bounds[-1] - bounds[0], rd(q3), rd(m) - rd(q1) if rd(m) - rd(q1) != iqr else iqr + 4],
                  "Q<sub>1</sub> ≈ %d (at %s) and Q<sub>3</sub> ≈ %d (at %s). IQR ≈ %d − %d = <b>%d</b>." % (rd(q1), num(N // 4), rd(q3), num(3 * N // 4), rd(q3), rd(q1), iqr))
    if kind == "above":
        i = r.randint(1, len(bounds) - 2)
        x = bounds[i]
        c = cum[i]
        unit = (" " + what.split("(")[1].rstrip(")").replace("minutes", "minutes")) if "(" in what else " marks"
        return QN(pre + " How many %s have more than %s%s?%s" % (who, num(x), unit, pic), N - c, [c, N - cum[i - 1], fs[i]],
                  "Read up from %s to the curve and across: %d have %s or less. %s − %d = <b>%d</b>." % (num(x), c, num(x), num(N), c, N - c))
    p = r.choice([10, 20, 80, 90])
    v = interp_x(bounds, cum, N * p / 100)
    return QN(pre + " Estimate the %dth percentile.%s" % (p, pic), rd(v), [rd(N * p / 100), rd(interp_x(bounds, cum, N * (100 - p) / 100)), rd(m)],
              "The %dth percentile is at %d%% of %s = %s. Read across and down: about <b>%d</b>." % (p, p, num(N), g(N * p / 100), rd(v)))


# ------------------------------------------------------------ box plots
def box_svg(stats, lo, hi, step, labels=None, label="box-and-whisker plot"):
    W = 360
    x0, pw = 30, 300
    Xp = lambda v: x0 + (v - lo) / (hi - lo) * pw
    rows = len(stats)
    H = 60 + rows * 52
    s = []
    yaxis = 26 + rows * 52
    v = lo
    while v <= hi:
        s.append(line(Xp(v), yaxis, Xp(v), yaxis + 6, INK, 1.5))
        s.append(text(Xp(v), yaxis + 20, num(v), 11, weight=400))
        v += step
    s.append(line(x0, yaxis, x0 + pw, yaxis, INK, 2))
    for k, (mn, q1, m, q3, mx) in enumerate(stats):
        y = 30 + k * 52
        s.append(line(Xp(mn), y, Xp(q1), y, INK, 2))
        s.append(line(Xp(q3), y, Xp(mx), y, INK, 2))
        s.append(line(Xp(mn), y - 9, Xp(mn), y + 9, INK, 2))
        s.append(line(Xp(mx), y - 9, Xp(mx), y + 9, INK, 2))
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='34' fill='#eef6f0' stroke='%s' stroke-width='2'/>" % (Xp(q1), y - 17, Xp(q3) - Xp(q1), INK))
        s.append(line(Xp(m), y - 17, Xp(m), y + 17, RED, 3))
        if labels:
            s.append(text(x0 - 8, y - 22, labels[k], 12, anchor="start"))
    return fig(svg_wrap(W, H, "".join(s), label))


def rand_box(r, lo, hi, step):
    st = step if step == 5 else step // 2
    return sorted(r.sample(range(lo + st, hi - st + 1, st), 5))


# ------------------------------------------------------------ set 4: reading box plots
def one_box(r):
    lo, hi, step = r.choice([(0, 100, 10), (20, 80, 5), (0, 50, 5), (100, 200, 10)])
    st = rand_box(r, lo, hi, step)
    mn, q1, m, q3, mx = st
    pic = box_svg([st], lo, hi, step)
    kind = r.choice(["med", "iqr", "range", "pct", "q3"])
    if kind == "med":
        return QN("Find the median from the box-and-whisker plot.%s" % pic, m, [q1, q3, (mn + mx) // 2 if (mn + mx) // 2 != m else m + step], "The line inside the box is the median: <b>%d</b>." % m)
    if kind == "q3":
        return QN("Find the upper quartile from the box-and-whisker plot.%s" % pic, q3, [mx, m, q1], "The right edge of the box is the upper quartile: <b>%d</b>." % q3)
    if kind == "iqr":
        return QN("Find the interquartile range from the box-and-whisker plot.%s" % pic, q3 - q1, [mx - mn, q3, m - q1 if m - q1 != q3 - q1 else q3 - q1 + step], "IQR = upper quartile − lower quartile = %d − %d = <b>%d</b>." % (q3, q1, q3 - q1))
    if kind == "range":
        return QN("Find the range from the box-and-whisker plot.%s" % pic, mx - mn, [q3 - q1, mx, mx - m], "Range = largest − smallest = %d − %d = <b>%d</b>." % (mx, mn, mx - mn))
    which = r.choice([("above the upper quartile", 25), ("below the median", 50), ("between the quartiles", 50), ("below the lower quartile", 25), ("above the lower quartile", 75)])
    return QN("What percentage of the data lies %s?%s" % (which[0], pic), which[1], [x for x in [25, 50, 75, 100] if x != which[1]][:3], "The quartiles split the data into four quarters of 25%% each, so <b>%d%%</b>." % which[1], unit="%")


# ------------------------------------------------------------ set 5: comparing data sets
def one_cmp(r):
    lo, hi, step = r.choice([(0, 100, 10), (20, 80, 5), (0, 50, 5)])
    a = rand_box(r, lo, hi, step)
    b = rand_box(r, lo, hi, step)
    if a[2] == b[2] or (a[3] - a[1]) == (b[3] - b[1]):
        return None
    groups = r.choice([("Class A", "Class B"), ("Boys", "Girls"), ("Morning", "Evening"), ("Team X", "Team Y")])
    pic = box_svg([a, b], lo, hi, step, labels=groups, label="two box-and-whisker plots")
    kind = r.choice(["higher", "consistent", "consistent", "diffmed", "diffiqr"])
    if kind == "higher":
        hi_g = groups[0] if a[2] > b[2] else groups[1]
        lo_g = groups[1] if a[2] > b[2] else groups[0]
        return T("Which group has the higher median?%s" % pic, hi_g, [lo_g, "They are the same", "You cannot tell from box plots"], "Compare the lines inside the boxes: %d and %d. <b>%s</b>." % (a[2], b[2], hi_g))
    if kind == "consistent":
        ia, ib = a[3] - a[1], b[3] - b[1]
        c = groups[0] if ia < ib else groups[1]
        o = groups[1] if ia < ib else groups[0]
        return T("Which group's data is more consistent?%s" % pic, "%s, because its interquartile range is smaller" % c,
                 ["%s, because its interquartile range is larger" % o, "%s, because its median is higher" % (groups[0] if a[2] > b[2] else groups[1]), "%s, because its maximum is larger" % o],
                 "Consistency is about spread. IQRs: %s %d, %s %d. The smaller spread is <b>%s</b>." % (groups[0], ia, groups[1], ib, c))
    if kind == "diffmed":
        return QN("What is the difference between the two medians?%s" % pic, abs(a[2] - b[2]), [abs(a[3] - b[3]) if abs(a[3] - b[3]) != abs(a[2] - b[2]) else abs(a[2] - b[2]) + step, abs((a[3] - a[1]) - (b[3] - b[1])), a[2] + b[2]],
                  "Medians: %d and %d. Difference = <b>%d</b>." % (a[2], b[2], abs(a[2] - b[2])))
    ia, ib = a[3] - a[1], b[3] - b[1]
    return QN("What is the interquartile range of %s?%s" % (groups[1], pic), ib, [ia, b[4] - b[0], b[3]], "%s: upper quartile %d − lower quartile %d = <b>%d</b>." % (groups[1], b[3], b[1], ib))


def build():
    sets = [S("Quartiles and interquartile range", collect(one_list, 20, R)),
            S("Cumulative frequency tables", collect(one_table, 20, R)),
            S("Reading cumulative frequency curves", collect(one_curve, 20, R)),
            S("Reading box-and-whisker plots", collect(one_box, 20, R)),
            S("Comparing data sets", collect(one_cmp, 20, R))]
    body = lesson(
        "<ul><li>Sort the data. The <b>median</b> splits it in half; the <b>lower quartile</b> Q<sub>1</sub> and <b>upper quartile</b> Q<sub>3</sub> are the medians of the lower and upper halves.</li>"
        "<li><b>Interquartile range</b> = Q<sub>3</sub> − Q<sub>1</sub>. It measures the spread of the middle 50%.</li>"
        "<li>On a <b>cumulative frequency curve</b> for <i>n</i> values, read across from <i>n</i>/2 for the median, <i>n</i>/4 for Q<sub>1</sub> and 3<i>n</i>/4 for Q<sub>3</sub>, then read down.</li>"
        "<li>A <b>box-and-whisker plot</b> shows the minimum, Q<sub>1</sub>, median, Q<sub>3</sub> and maximum. A smaller IQR means more consistent data.</li></ul>",
        [("Find the IQR of 3, 5, 7, 8, 9, 12, 15, 20.", ["Lower half 3, 5, 7, 8: Q₁ = 6", "Upper half 9, 12, 15, 20: Q₃ = 13.5"], "7.5"),
         ("A cumulative frequency curve shows 80 students. Where do you read the upper quartile?", ["3/4 × 80 = 60"], "Across from 60, then down")],
        ["Forgetting to sort the data first.",
         "Reading the cumulative frequency axis instead of the value axis for the answer.",
         "Using n/2 instead of n/4 for the lower quartile.",
         "Comparing medians when the question asks which data is more consistent (spread)."])
    faq = [("How do you find quartiles from a list?", "Sort the data and find the median. Q₁ is the median of the lower half and Q₃ is the median of the upper half."),
           ("How do you read the median from a cumulative frequency curve?", "Find half the total on the cumulative frequency axis, go across to the curve, then down to the value axis."),
           ("What does a box-and-whisker plot show?", "The minimum, lower quartile, median, upper quartile and maximum. The box holds the middle 50% of the data."),
           ("How do you compare two box plots?", "Compare the medians to see which is higher on average, and the interquartile ranges to see which is more consistent.")]
    make(4, "cumulative-frequency-and-box-plots", 6, "S1",
         "Cumulative Frequency, Quartiles and Box-and-Whisker Plots",
         "", "Cumulative frequency and box plots", "",
         "Free Secondary 4 maths worksheets on quartiles, interquartile range, percentiles, cumulative frequency tables and curves, box-and-whisker plots and comparing data. 100 questions with answers.",
         "IQR = upper quartile − lower quartile: the spread of the middle half.",
         "On a cumulative frequency curve, read across from n/4, n/2 and 3n/4, then down.",
         body, faq, sets, R)


if __name__ == "__main__":
    build()
