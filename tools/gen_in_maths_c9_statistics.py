# -*- coding: utf-8 -*-
"""
India Class 9 Maths, NCERT Chapter 12: Statistics — Bar Graphs, Histograms and Frequency Polygons (CBSE Unit VII)
  python3 tools/gen_in_maths_c9_statistics.py
Reading bar graphs, histograms of grouped data with equal class widths, histograms with varying widths (adjusted
heights, proportional to frequency ÷ class width), class marks and frequency polygons (including the imaginary classes
of frequency zero at both ends), and data problems.
Wrong answers come from real mistakes: reading the next grid line, the upper limit taken as the class mark, plotting the
frequency of an unequal class without adjusting, the class width taken as the class mark, and counting the wrong side
of a boundary (a value of 40 belongs to 40–50, not 30–40).
"""
import random
from fractions import Fraction as F
from in_common import num, S, make, lesson, mix, T, QN, table, svg_wrap, text, line, People, GREEN, FILL, INK, GRAY, BLUE, RED

R = random.Random(909012)
P = People(R)


def axes(W, H, L, B, top, step, ymax, ylab):
    out = []
    for v in range(0, ymax + 1, step):
        y = B - (B - top) * v / ymax
        out.append(line(L, y, W - 15, y, GRAY, 1))
        out.append(text(L - 6, y + 4, str(v), 12, "end", INK, weight=400))
    out.append(line(L, B, W - 15, B, INK, 2))
    out.append(line(L, top - 8, L, B, INK, 2))
    out.append("<text x='14' y='%d' font-size='12' fill='%s' text-anchor='middle' transform='rotate(-90 14 %d)'>%s</text>" % ((top + B) // 2, INK, (top + B) // 2, ylab))
    return out


def bar_svg(labels, vals, step, ylab, xlab):
    W, H, L, B, top = 470, 290, 58, 240, 20
    ymax = step * (-(-max(vals) // step))
    out = axes(W, H, L, B, top, step, ymax, ylab)
    n = len(vals)
    slot = (W - 15 - L) / n
    for i, (lb, v) in enumerate(zip(labels, vals)):
        x = L + i * slot + slot * 0.2
        h = (B - top) * v / ymax
        out.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x, B - h, slot * 0.6, h, FILL, GREEN))
        out.append(text(x + slot * 0.3, B + 16, lb, 12, "middle", INK, weight=400))
    out.append(text((L + W) / 2, H - 8, xlab, 12, "middle", INK, weight=700))
    return svg_wrap(W, H, "".join(out), "Bar graph of %s" % ylab.lower())


def hist_svg(cl, heights, step, ylab, xlab, poly=None):
    """cl: list of (a, b); heights: bar heights on the y-axis; poly: list of (x, y) points in data units"""
    W, H, L, B, top = 500, 290, 58, 240, 20
    ymax = step * (-(-max(heights) // step))
    out = axes(W, H, L, B, top, step, ymax, ylab)
    lo = cl[0][0] - (cl[0][1] - cl[0][0] if poly else 0)
    hi = cl[-1][1] + (cl[-1][1] - cl[-1][0] if poly else 0)
    off = 12 if lo else 0
    sx = lambda v: L + off + (W - 30 - L - off) * (v - lo) / (hi - lo)
    sy = lambda v: B - (B - top) * v / ymax
    if lo:
        out.append("<path d='M%.1f %.1f l4 -5 l4 10 l4 -5' fill='none' stroke='%s' stroke-width='1.5'/>" % (L, B, INK))
    for (a, b), h in zip(cl, heights):
        if h:
            out.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s' stroke='%s' stroke-width='1.5'/>" % (sx(a), sy(h), sx(b) - sx(a), sy(0) - sy(h), FILL, GREEN))
    ticks = sorted(set([a for a, b in cl] + [cl[-1][1]] + ([lo, hi] if poly else [])))
    for t in ticks:
        out.append(line(sx(t), B, sx(t), B + 4, INK, 1.5))
        out.append(text(sx(t), B + 17, num(t), 11, "middle", INK, weight=400))
    if poly:
        pts = " ".join("%.1f,%.1f" % (sx(x), sy(y)) for x, y in poly)
        out.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='2.5'/>" % (pts, BLUE))
        for x, y in poly:
            out.append("<circle cx='%.1f' cy='%.1f' r='3.5' fill='%s'/>" % (sx(x), sy(y), BLUE))
    out.append(text((L + W) / 2, H - 6, xlab, 12, "middle", INK, weight=700))
    return svg_wrap(W, H, "".join(out), "Histogram of %s" % xlab.lower())


# ---------------------------------------------------------------- data
BARS = [
    ("Favourite sport of students in Class 9", "Number of students", ["Cricket", "Football", "Hockey", "Kabaddi", "Badminton"], 5),
    ("Cars sold by a showroom", "Number of cars", ["Jan", "Feb", "Mar", "Apr", "May", "Jun"], 10),
    ("Rainfall in a town (mm)", "Rainfall (mm)", ["Jun", "Jul", "Aug", "Sep", "Oct"], 50),
    ("Books borrowed from a school library", "Number of books", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"], 10),
    ("Population of five villages (in hundreds)", "Population (hundreds)", ["Rampur", "Sitapur", "Nagla", "Kheri", "Barod"], 5),
    ("Trees planted by each house", "Number of trees", ["Red", "Blue", "Green", "Yellow"], 5),
]
HISTS = [
    ("Marks obtained by students", "Marks", "Number of students", 10, 0),
    ("Heights of plants (cm)", "Height (cm)", "Number of plants", 5, 20),
    ("Weights of students (kg)", "Weight (kg)", "Number of students", 5, 30),
    ("Daily wages of workers (₹)", "Daily wages (₹)", "Number of workers", 100, 300),
    ("Ages of people in a park (years)", "Age (years)", "Number of people", 10, 10),
    ("Time spent on homework (minutes)", "Time (minutes)", "Number of students", 15, 0),
]


def bars(r):
    title, ylab, labels, step = r.choice(BARS)
    vals = [step * r.randint(1, 9) for _ in labels]
    while len(set(vals)) < len(vals):
        vals = [step * r.randint(1, 9) for _ in labels]
    return title, ylab, labels, step, vals


def hist(r, k=None):
    title, xlab, ylab, h, start = r.choice(HISTS)
    k = k or r.choice([5, 6])
    cl = [(start + i * h, start + (i + 1) * h) for i in range(k)]
    while True:
        fr = [r.randint(1, 12) for _ in cl]
        if fr.count(max(fr)) == 1 and fr.count(min(fr)) == 1:
            break
    step = 2 if max(fr) > 8 else 1
    return title, xlab, ylab, cl, fr, step


def ct(a, b):
    return "%s–%s" % (num(a), num(b))


# ---------------------------------------------------------------- set 1: bar graphs
def lcf(t):
    return t[0].lower() + t[1:]


def K(fn, kind):
    f = lambda r: fn(r, kind)
    f.__name__ = fn.__name__ + "_" + kind
    return f


def one_bar(r, kind=None):
    title, ylab, labels, step, vals = bars(r)
    g = bar_svg(labels, vals, step, ylab, title)
    kind = kind or r.choice(["read", "read", "max", "min", "diff", "total", "times"])
    i = r.randrange(len(vals))
    if kind == "read":
        return QN(g + "The bar graph shows %s. Read the value for %s." % (lcf(title), labels[i]), vals[i], [vals[i] + step, vals[i] - step, vals[i] + 2 * step],
                  "The top of the bar for %s is level with <b>%d</b>." % (labels[i], vals[i]))
    if kind in ("max", "min"):
        j = vals.index(max(vals) if kind == "max" else min(vals))
        others = [l for l in labels if l != labels[j]]
        return T(g + "The bar graph shows %s. Which bar is the %s?" % (lcf(title), "tallest" if kind == "max" else "shortest"), labels[j], r.sample(others, 3),
                 "The %s bar is <b>%s</b> (%d)." % ("tallest" if kind == "max" else "shortest", labels[j], vals[j]))
    if kind == "diff":
        i, j = r.sample(range(len(vals)), 2)
        if vals[i] < vals[j]:
            i, j = j, i
        d = vals[i] - vals[j]
        return QN(g + "How much more is the value for %s than for %s?" % (labels[i], labels[j]), d, [vals[i] + vals[j], vals[i], d + step],
                  "%d − %d = <b>%d</b>." % (vals[i], vals[j], d))
    if kind == "total":
        t = sum(vals)
        return QN(g + "What is the total of all the bars?", t, [t - vals[-1], t + step, max(vals) * len(vals)],
                  "%s = <b>%d</b>." % (" + ".join(map(str, vals)), t))
    i, j = r.sample(range(len(vals)), 2)
    if vals[i] % vals[j] or vals[i] == vals[j]:
        return None
    k = vals[i] // vals[j]
    return QN(g + "How many times the value for %s is the value for %s?" % (labels[j], labels[i]), k, [vals[i] - vals[j], k + 1, k * 2],
              "%d ÷ %d = <b>%d</b>." % (vals[i], vals[j], k))


# ---------------------------------------------------------------- set 2: histograms with equal widths
def one_hist(r, kind=None):
    title, xlab, ylab, cl, fr, step = hist(r)
    g = hist_svg(cl, fr, step, ylab, xlab)
    kind = kind or r.choice(["read", "read", "max", "total", "width", "above", "below"])
    if kind == "read":
        i = r.randrange(len(cl))
        a, b = cl[i]
        return QN(g + "The histogram shows %s. What is the frequency of the class %s?" % (lcf(title), ct(a, b)), fr[i], [fr[i + 1] if i + 1 < len(fr) else fr[i - 1], fr[i] + 1, b - a],
                  "The bar from %s to %s reaches <b>%d</b>." % (num(a), num(b), fr[i]))
    if kind == "max":
        j = fr.index(max(fr))
        wr = [ct(*cl[x]) for x in range(len(cl)) if x != j]
        return T(g + "Which class has the highest frequency?", ct(*cl[j]), r.sample(wr, 3), "The tallest bar is over <b>%s</b>." % ct(*cl[j]))
    if kind == "total":
        t = sum(fr)
        return QN(g + "How many observations are shown in the histogram altogether?", t, [len(fr), t - fr[0], max(fr) * len(fr)],
                  "Add the heights: %s = <b>%d</b>." % (" + ".join(map(str, fr)), t))
    if kind == "width":
        h = cl[0][1] - cl[0][0]
        return QN(g + "What is the class width (class size) of this histogram?", h, [cl[0][0], (cl[0][0] + cl[0][1]) / F(2), len(cl)],
                  "Each class is %s − %s = <b>%s</b> wide." % (num(cl[0][1]), num(cl[0][0]), num(h)))
    i = r.randrange(1, len(cl) - 1)
    v = cl[i][0]
    if kind == "above":
        n = sum(fr[i:])
        return QN(g + "How many observations are %s or more?" % num(v), n, [sum(fr[i + 1:]), sum(fr[:i]), n + fr[i - 1]],
                  "Classes from %s upwards: %s = <b>%d</b>. (A value of %s belongs to the class %s.)" % (num(v), " + ".join(map(str, fr[i:])), n, num(v), ct(*cl[i])))
    n = sum(fr[:i])
    return QN(g + "How many observations are less than %s?" % num(v), n, [sum(fr[:i + 1]), sum(fr[i:]), n - fr[0] if n - fr[0] > 0 else n + 1],
              "Classes below %s: %s = <b>%d</b>." % (num(v), " + ".join(map(str, fr[:i])), n))


# ---------------------------------------------------------------- set 3: histograms with varying widths
UNEQ = [
    ("Marks", [(0, 20), (20, 30), (30, 40), (40, 50), (50, 70), (70, 100)], 10),
    ("Length of leaves (mm)", [(10, 15), (15, 20), (20, 30), (30, 35), (35, 45)], 5),
    ("Age (years)", [(0, 10), (10, 15), (15, 20), (20, 30), (30, 50)], 5),
    ("Distance (km)", [(0, 4), (4, 6), (6, 8), (8, 12), (12, 20)], 2),
    ("Weight (g)", [(100, 110), (110, 130), (130, 140), (140, 160), (160, 200)], 10),
]


def one_uneq(r, kind=None):
    xlab, cl, mw = r.choice(UNEQ)
    ws = [b - a for a, b in cl]
    while True:
        fr = [r.randint(2, 12) * ((b - a) // mw) for a, b in cl]
        adj = [F(f * mw, w) for f, w in zip(fr, ws)]
        if all(x.denominator == 1 for x in adj) and len(set(adj)) == len(adj):
            break
    kind = kind or r.choice(["adj", "adj", "adj", "which", "why", "minw", "back"])
    tb = table([xlab] + [ct(a, b) for a, b in cl], [["Frequency"] + [str(f) for f in fr]])
    if kind == "adj":
        wide = [i for i, w in enumerate(ws) if w != mw]
        i = r.choice(wide)
        a, b = cl[i]
        return QN(tb + "<p>A histogram is drawn using the minimum class size %d. What is the adjusted frequency (height of the bar) for the class %s?</p>" % (mw, ct(a, b)), adj[i],
                  [fr[i], fr[i] * ws[i] // mw, fr[i] - mw if fr[i] - mw > 0 else fr[i] + mw],
                  "Adjusted frequency = %d ÷ %d × %d = <b>%s</b>." % (fr[i], ws[i], mw, num(adj[i])))
    if kind == "which":
        j = adj.index(max(adj))
        k = fr.index(max(fr))
        if j == k:
            return None
        wr = [ct(*cl[k])] + [ct(*cl[x]) for x in range(len(cl)) if x not in (j, k)]
        return T(tb + "<p>In a correct histogram of this data, which class has the tallest bar?</p>", ct(*cl[j]), wr[:1] + r.sample(wr[1:], 2),
                 "Heights are frequency ÷ class width × %d: %s. The tallest is <b>%s</b>, not the largest frequency." % (mw, ", ".join(num(x) for x in adj), ct(*cl[j])))
    if kind == "minw":
        return QN(tb + "<p>What is the minimum class size in this table?</p>", mw, [max(ws), cl[0][0] if cl[0][0] else max(ws) // 2, len(cl)],
                  "The class widths are %s. The smallest is <b>%d</b>." % (", ".join(map(str, ws)), mw))
    if kind == "back":
        wide = [i for i, w in enumerate(ws) if w != mw]
        i = r.choice(wide)
        a, b = cl[i]
        return QN("<p>In a histogram with varying widths, the heights use the minimum class size %d. The bar over the class %s has height %s. What is the frequency of this class?</p>" % (mw, ct(a, b), num(adj[i])), fr[i],
                  [adj[i], adj[i] * mw, fr[i] + ws[i]], "Frequency = height × class width ÷ %d = %s × %d ÷ %d = <b>%d</b>." % (mw, num(adj[i]), ws[i], mw, fr[i]))
    return T(tb + "<p>Why should the heights of the bars be adjusted when this data is drawn as a histogram?</p>", "The classes have different widths, so the areas must be proportional to the frequencies",
             ["The frequencies are too large to fit", "The classes overlap", "The first class does not start at 0"],
             "In a histogram the <b>area</b> of each bar shows the frequency, so wider classes need lower bars.")


# ---------------------------------------------------------------- set 4: class marks and frequency polygons
def poly_pts(cl, fr):
    h = cl[0][1] - cl[0][0]
    xs = [F(a + b, 2) for a, b in cl]
    return [(xs[0] - h, 0)] + list(zip(xs, fr)) + [(xs[-1] + h, 0)]


def one_poly(r, kind=None):
    title, xlab, ylab, cl, fr, step = hist(r)
    pts = poly_pts(cl, fr)
    if cl[0][0] == 0 and kind != "mark":
        return None
    kind = kind or r.choice(["mark", "mark", "point", "start", "end", "read", "join"])
    i = r.randrange(len(cl))
    a, b = cl[i]
    if kind == "mark":
        return QN("<p>Find the class mark of the class %s.</p>" % ct(a, b), F(a + b, 2), [b, b - a, a + b],
                  "Class mark = (%s + %s) ÷ 2 = <b>%s</b>." % (num(a), num(b), num(F(a + b, 2))))
    tb = table([xlab] + [ct(p, q) for p, q in cl], [["Frequency"] + [str(f) for f in fr]])
    if kind == "point":
        m = F(a + b, 2)
        return T(tb + "<p>A frequency polygon is drawn for this data. Which point is plotted for the class %s?</p>" % ct(a, b), "(%s, %d)" % (num(m), fr[i]),
                 ["(%s, %d)" % (num(b), fr[i]), "(%s, %d)" % (num(a), fr[i]), "(%d, %s)" % (fr[i], num(m))],
                 "Plot (class mark, frequency): <b>(%s, %d)</b>." % (num(m), fr[i]))
    if kind in ("start", "end"):
        x = pts[0][0] if kind == "start" else pts[-1][0]
        near = pts[1][0] if kind == "start" else pts[-2][0]
        edge = cl[0][0] if kind == "start" else cl[-1][1]
        return T(tb + "<p>To close the frequency polygon, it is joined to the x-axis at the class mark of an imaginary class of frequency zero. Which point is used at the %s?</p>" % ("start" if kind == "start" else "end"),
                 "(%s, 0)" % num(x), ["(%s, 0)" % num(edge), "(%s, 0)" % num(near), "(0, 0)" if x != 0 and edge != 0 else "(%s, 0)" % num(2 * x - near)],
                 "The imaginary class next to the %s has class mark <b>%s</b>, so the point is (%s, 0)." % ("first class" if kind == "start" else "last class", num(x), num(x)))
    g = hist_svg(cl, fr, step, ylab, xlab, poly=pts)
    if kind == "read":
        m = F(a + b, 2)
        return QN(g + "The frequency polygon is drawn on the histogram. What is the frequency at the class mark %s?" % num(m), fr[i], [fr[i] + 1, fr[i + 1] if i + 1 < len(fr) else fr[i - 1], m],
                  "The point above %s is at height <b>%d</b>." % (num(m), fr[i]))
    return T(g + "How is the frequency polygon drawn on a histogram?", "By joining the mid-points of the tops of the bars",
             ["By joining the top left corners of the bars", "By joining the top right corners of the bars", "By joining the bottoms of the bars"],
             "Each point is (class mark, frequency): <b>the mid-point of the top of each bar</b>, closed at both ends on the x-axis.")


# ---------------------------------------------------------------- set 5: data problems
def one_prob(r, kind=None):
    kind = kind or r.choice(["pct", "pct", "between", "range", "polyfr", "classof", "tally"])
    if kind in ("pct", "between", "range", "classof"):
        title, xlab, ylab, cl, fr, step = hist(r)
        if kind == "classof":
            i = r.randrange(1, len(cl))
            v = cl[i][0]
            return T("<p>The classes are %s. In which class is an observation of %s counted?</p>" % (", ".join(ct(*c) for c in cl), num(v)), ct(*cl[i]),
                     [ct(*cl[i - 1]), "Both " + ct(*cl[i - 1]) + " and " + ct(*cl[i]), "Neither class"],
                     "With exclusive classes the upper limit is not included, so %s goes in <b>%s</b>." % (num(v), ct(*cl[i])))
        g = hist_svg(cl, fr, step, ylab, xlab)
        n = sum(fr)
        if kind == "pct":
            i = fr.index(max(fr))
            p = F(fr[i] * 100, n)
            if (p * 10).denominator != 1:
                return None
            return QN(g + "The histogram shows %s. What percentage of the observations are in the class %s?" % (lcf(title), ct(*cl[i])), p, [fr[i], F(fr[i] * 100, n - fr[i]), 100 - p],
                      "%d out of %d: %d ÷ %d × 100 = <b>%s%%</b>." % (fr[i], n, fr[i], n, num(p)), unit="%")
        if kind == "between":
            i = r.randrange(0, len(cl) - 2)
            j = i + 2
            s = sum(fr[i:j])
            return QN(g + "How many observations are from %s up to (but not including) %s?" % (num(cl[i][0]), num(cl[j][0])), s, [sum(fr[i:j + 1]), fr[i], s + fr[j - 1]],
                      "Classes %s and %s: %d + %d = <b>%d</b>." % (ct(*cl[i]), ct(*cl[i + 1]), fr[i], fr[i + 1], s))
        lo, hi = cl[0][0], cl[-1][1]
        return QN(g + "Find the difference between the upper limit of the last class and the lower limit of the first class in this histogram.", hi - lo,
                  [hi, cl[-1][0] - lo, len(cl)], "%s − %s = <b>%s</b>." % (num(hi), num(lo), num(hi - lo)))
    if kind == "polyfr":
        a, b = r.sample([("Section A", "Section B")], 1)[0]
        h = r.choice([10, 20])
        cl = [(i * h, (i + 1) * h) for i in range(5)]
        f1 = [r.randint(2, 12) for _ in cl]
        f2 = [r.randint(2, 12) for _ in cl]
        i = r.randrange(5)
        if f1[i] == f2[i]:
            return None
        more = a if f1[i] > f2[i] else b
        tb = table(["Marks"] + [ct(*c) for c in cl], [[a] + list(map(str, f1)), [b] + list(map(str, f2))])
        d = abs(f1[i] - f2[i])
        return T(tb + "<p>Frequency polygons for the two sections are drawn on the same axes. At the class mark %s, which polygon is higher, and by how much?</p>" % num(F(2 * i + 1, 2) * h),
                 "%s, by %d" % (more, d), ["%s, by %d" % (a if more == b else b, d), "%s, by %d" % (more, f1[i] + f2[i]), "They are at the same height"],
                 "At %s: %s has %d and %s has %d. <b>%s is higher by %d</b>." % (num(F(2 * i + 1, 2) * h), a, f1[i], b, f2[i], more, d))
    xs = [r.randint(1, 49) for _ in range(20)]
    cl = [(0, 10), (10, 20), (20, 30), (30, 40), (40, 50)]
    fr = [sum(1 for x in xs if a <= x < b) for a, b in cl]
    i = r.randrange(5)
    a, b = cl[i]
    return QN("<p>Here are the marks (out of 50) of 20 students: %s. Using classes 0–10, 10–20, …, 40–50, find the frequency of the class %s.</p>" % (", ".join(map(str, xs)), ct(a, b)), fr[i],
              [fr[i] + sum(1 for x in xs if x == b), fr[i] + 1, fr[i - 1] if i else fr[i] + 2],
              "Count the marks from %d up to but not including %d: <b>%d</b>." % (a, b, fr[i]))


def main():
    seen = set()
    sets = [
        S("Reading bar graphs", mix(R, [(one_bar, 20)], seen)),
        S("Histograms", mix(R, [(one_hist, 20)], seen)),
        S("Histograms with varying widths", mix(R, [(K(one_uneq, "adj"), 11), (K(one_uneq, "back"), 4), (K(one_uneq, "which"), 3), (K(one_uneq, "minw"), 1), (K(one_uneq, "why"), 1)], seen)),
        S("Class marks and frequency polygons", mix(R, [(K(one_poly, "mark"), 5), (K(one_poly, "point"), 5), (K(one_poly, "start"), 3), (K(one_poly, "end"), 3), (K(one_poly, "read"), 3), (K(one_poly, "join"), 1)], seen)),
        S("Data problems", mix(R, [(K(one_prob, "pct"), 5), (K(one_prob, "between"), 4), (K(one_prob, "tally"), 4), (K(one_prob, "polyfr"), 3), (K(one_prob, "classof"), 2), (K(one_prob, "range"), 2)], seen)),
    ]
    body = lesson(
        "<p>A <b>bar graph</b> uses bars of equal width with gaps between them. A <b>histogram</b> shows grouped data: the bars stand on the classes, with no gaps.</p>"
        "<p>If the class widths are different, the bar heights must be adjusted: <b>adjusted frequency = frequency ÷ class width × minimum class size</b>. Then the areas match the frequencies.</p>"
        "<p>For a <b>frequency polygon</b>, plot (class mark, frequency) for each class and join the points. Close it on the x-axis at the class marks of an imaginary class before the first and after the last.</p>",
        [("The class 20–40 has frequency 12 and the minimum class size is 10. Find the height of its bar.", ["12 ÷ 20 × 10"], "6"),
         ("Which point is plotted for the class 30–40 with frequency 7?", ["Class mark = (30 + 40) ÷ 2 = 35"], "(35, 7)")],
        ["Drawing bars for unequal classes with the frequency as the height.",
         "Plotting the upper limit of a class instead of its class mark.",
         "Counting a value of 40 in the class 30–40. With exclusive classes it belongs to 40–50."])
    faq = [
        ("What is the difference between a bar graph and a histogram?", "A bar graph shows separate categories with gaps between bars. A histogram shows continuous grouped data, with bars standing on the classes and no gaps."),
        ("How do you draw a histogram with varying class widths?", "Use the minimum class size and find each adjusted frequency = frequency ÷ class width × minimum class size. Use these as the heights."),
        ("What is a class mark?", "The mid-point of a class: (lower limit + upper limit) ÷ 2."),
        ("How do you draw a frequency polygon?", "Plot (class mark, frequency) for every class, join the points with straight lines and close the polygon at the class marks of imaginary classes of frequency zero at each end."),
    ]
    make(9, "statistics", 12, "St", 12, "Statistics: Bar Graphs, Histograms and Frequency Polygons", "statistics",
         "Bar graphs, histograms (with varying base lengths) and frequency polygons (summary of the CBSE syllabus)",
         "Class 9 Statistics worksheet (NCERT Chapter 12): reading bar graphs, histograms with equal and varying class widths, class marks and frequency polygons. 100 questions with answers.",
         "Histogram heights: frequency ÷ width × minimum width", "Frequency polygon: plot (class mark, frequency) and close it at both ends.",
         body, faq, sets, R)


if __name__ == "__main__":
    main()
