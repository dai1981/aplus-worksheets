# -*- coding: utf-8 -*-
"""
Texas Grade 6 Math: Dot Plots, Stem-and-Leaf Plots, Histograms and Box Plots (TEKS 6.12A, 6.13A)
  python3 tools/gen_ustx_math_g6_data_displays.py
Reading dot plots (the US Grade 6 maker), stem-and-leaf plots (the Texas Grade 4 makers), histograms, and box plots
with their five-number summary and spread.
Wrong answers come from real mistakes: reading a histogram bar as one value, reading the box as the median, and
using the range instead of the IQR.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g6_mean_median as mm
import gen_ustx_math_g4_data as g4d
adopt(mm)
tx_common.GRADE = "grade-6"

INK = "#1f2937"

HIST = [("Minutes spent on homework", 0, 10), ("Points scored per game", 10, 10), ("Ages of people at a rodeo", 10, 10), ("Heights of sunflowers (inches)", 20, 10),
        ("Number of push-ups", 0, 5), ("Daily high temperatures in El Paso (°F)", 60, 5)]


def hist_svg(title, lo, w, counts):
    n = len(counts)
    top = max(counts) + 1
    top += top % 2
    W, H, x0, y0 = 340, 200, 40, 14
    pw, ph = W - x0 - 10, H - 50
    bw = pw / float(n)
    s = ["<svg viewBox='0 0 %d %d' width='%d' data-pf='lg' role='img' aria-label='histogram: %s'>" % (W, H + 18, W, title)]
    for t in range(0, top + 1, 2):
        y = y0 + ph - ph * t / float(top)
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='#d1d5db'/><text x='%d' y='%.1f' font-size='11' text-anchor='end' fill='%s'>%d</text>" % (x0, y, x0 + pw, y, x0 - 4, y + 4, INK, t))
    for i, c in enumerate(counts):
        h = ph * c / float(top)
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#60a5fa' stroke='%s'/>" % (x0 + i * bw, y0 + ph - h, bw, h, INK))
        s.append("<text x='%.1f' y='%d' font-size='11' text-anchor='middle' fill='%s'>%d–%d</text>" % (x0 + i * bw + bw / 2, y0 + ph + 14, INK, lo + i * w, lo + (i + 1) * w - 1))
    s.append("<text x='%d' y='%d' font-size='12' text-anchor='middle' fill='%s'>%s</text>" % (x0 + pw // 2, H + 10, INK, title))
    s.append("<text x='12' y='%d' font-size='12' text-anchor='middle' fill='%s' transform='rotate(-90 12 %d)'>Frequency</text></svg>" % (y0 + ph // 2, INK, y0 + ph // 2))
    return fig("".join(s))


def one_hist(r):
    title, lo, w = r.choice(HIST)
    n = r.choice([4, 5, 6])
    counts = [r.randint(1, 12) for _ in range(n)]
    if len(set(counts)) < n - 1:
        return None
    pic = hist_svg(title, lo, w, counts)
    lab = lambda i: "%d–%d" % (lo + i * w, lo + (i + 1) * w - 1)
    kind = r.choice(["bin", "total", "atleast", "most", "less"])
    i = r.randrange(n)
    if kind == "bin":
        return mcq(pic + "How many data values are in the %s interval?" % lab(i), str(counts[i]), [str(counts[i] + 1), str(lo + i * w), str(sum(counts) - counts[i])],
                   "The bar above %s reaches <b>%d</b>." % (lab(i), counts[i]))
    if kind == "total":
        return mcq(pic + "How many data values are shown in all?", str(sum(counts)), [str(n), str(max(counts)), str(sum(counts) - min(counts))],
                   "Add the bar heights: %s = <b>%d</b>." % (" + ".join(map(str, counts)), sum(counts)))
    if kind == "atleast":
        i = r.randint(1, n - 1)
        v = sum(counts[i:])
        return mcq(pic + "How many data values are %d or more?" % (lo + i * w), str(v), [str(counts[i]), str(sum(counts[:i])), str(v + counts[i - 1])],
                   "Add the bars from %s up: <b>%d</b>." % (lab(i), v))
    if kind == "less":
        i = r.randint(1, n - 1)
        v = sum(counts[:i])
        return mcq(pic + "How many data values are less than %d?" % (lo + i * w), str(v), [str(counts[i]), str(sum(counts[i:])), str(v + counts[i])],
                   "Add the bars below %d: <b>%d</b>." % (lo + i * w, v))
    m = max(range(n), key=lambda t: counts[t])
    if counts.count(counts[m]) > 1:
        return None
    others = [lab(t) for t in r.sample([t for t in range(n) if t != m], 3)]
    return mcq(pic + "Which interval has the most data values?", lab(m), others, "The tallest bar is above <b>%s</b>." % lab(m))


def box_svg(mn, q1, md, q3, mx, lo, hi, step, label):
    W, x0, x1 = 340, 20, 320
    sx = lambda v: x0 + (x1 - x0) * (v - lo) / float(hi - lo)
    s = ["<svg viewBox='0 0 %d 120' width='%d' data-pf='lg' role='img' aria-label='box plot: %s'>" % (W, W, label)]
    s.append("<line x1='%d' y1='80' x2='%d' y2='80' stroke='%s' stroke-width='1.5'/>" % (x0, x1, INK))
    for t in range(lo, hi + 1, step):
        s.append("<line x1='%.1f' y1='76' x2='%.1f' y2='84' stroke='%s'/><text x='%.1f' y='100' font-size='11' text-anchor='middle' fill='%s'>%d</text>" % (sx(t), sx(t), INK, sx(t), INK, t))
    s.append("<line x1='%.1f' y1='40' x2='%.1f' y2='40' stroke='%s' stroke-width='2'/>" % (sx(mn), sx(q1), INK))
    s.append("<line x1='%.1f' y1='40' x2='%.1f' y2='40' stroke='%s' stroke-width='2'/>" % (sx(q3), sx(mx), INK))
    for v in (mn, mx):
        s.append("<line x1='%.1f' y1='32' x2='%.1f' y2='48' stroke='%s' stroke-width='2'/>" % (sx(v), sx(v), INK))
    s.append("<rect x='%.1f' y='22' width='%.1f' height='36' fill='#dbeafe' stroke='%s' stroke-width='2'/>" % (sx(q1), sx(q3) - sx(q1), INK))
    s.append("<line x1='%.1f' y1='22' x2='%.1f' y2='58' stroke='%s' stroke-width='3'/>" % (sx(md), sx(md), INK))
    s.append("<text x='%d' y='116' font-size='12' text-anchor='middle' fill='%s'>%s</text></svg>" % (W // 2, INK, label))
    return fig("".join(s))


BOX = [("Test scores", 50, 100, 5), ("Minutes to get to school", 0, 40, 2), ("Heights of students (inches)", 50, 70, 1), ("Hours of sleep in a week", 40, 64, 2),
       ("Pecans picked (pounds)", 0, 60, 5), ("Ages of volunteers", 10, 50, 2)]


def five(r, lo, hi, step):
    pts = sorted(r.sample(range(lo + step, hi, step), 5))
    if len(set(pts)) < 5:
        return None
    return pts


def one_box(r):
    label, lo, hi, step = r.choice(BOX)
    f = five(r, lo, hi, step)
    if not f:
        return None
    mn, q1, md, q3, mx = f
    pic = box_svg(mn, q1, md, q3, mx, lo, hi, step * (2 if (hi - lo) // step > 12 else 1), label)
    kind = r.choice(["median", "q1", "q3", "range", "iqr", "max"])
    if kind == "median":
        return mcq(pic + "What is the median?", str(md), [str((mn + mx) // 2) if (mn + mx) // 2 != md else str(md + step), str(q1), str(q3)], "The line inside the box is the median: <b>%d</b>." % md)
    if kind == "q1":
        return mcq(pic + "What is the first quartile (Q1)?", str(q1), [str(mn), str(md), str(q3)], "The left side of the box is Q1: <b>%d</b>." % q1)
    if kind == "q3":
        return mcq(pic + "What is the third quartile (Q3)?", str(q3), [str(mx), str(md), str(q1)], "The right side of the box is Q3: <b>%d</b>." % q3)
    if kind == "range":
        return mcq(pic + "What is the range of the data?", str(mx - mn), [str(q3 - q1), str(mx), str(mx - md)], "Range = maximum − minimum = %d − %d = <b>%d</b>." % (mx, mn, mx - mn))
    if kind == "iqr":
        return mcq(pic + "What is the interquartile range (IQR)?", str(q3 - q1), [str(mx - mn), str(q3 - md), str(md - q1) if md - q1 != q3 - md else str(q3)], "IQR = Q3 − Q1 = %d − %d = <b>%d</b>." % (q3, q1, q3 - q1))
    return mcq(pic + "What is the greatest value in the data?", str(mx), [str(q3), str(hi), str(mx - mn)] if hi != mx else [str(q3), str(md), str(mx - mn)], "The right end of the whisker is the maximum: <b>%d</b>." % mx)


def one_box2(r):
    label, lo, hi, step = r.choice(BOX)
    f = five(r, lo, hi, step)
    if not f:
        return None
    mn, q1, md, q3, mx = f
    pic = box_svg(mn, q1, md, q3, mx, lo, hi, step * (2 if (hi - lo) // step > 12 else 1), label)
    kind = r.choice(["half", "quarter", "middle", "n"])
    if kind == "half":
        return mcq(pic + "About what percent of the data is greater than %d?" % md, "50%", ["25%", "75%", "100%"], "The median splits the data in half, so about <b>50%%</b> is above %d." % md)
    if kind == "quarter":
        return mcq(pic + "About what percent of the data is greater than %d?" % q3, "25%", ["50%", "75%", "10%"], "Q3 marks the top quarter, so about <b>25%%</b> is above %d." % q3)
    if kind == "middle":
        return mcq(pic + "The middle half of the data is between which two values?", "%d and %d" % (q1, q3), ["%d and %d" % (mn, mx), "%d and %d" % (mn, md), "%d and %d" % (md, mx)],
                   "The box shows the middle 50%%: from Q1 = %d to Q3 = %d. <b>%d and %d</b>." % (q1, q3, q1, q3))
    n = r.choice([20, 40, 60, 80, 100])
    return mcq(pic + "The box plot shows %d data values. About how many are less than %d?" % (n, q1), str(n // 4), [str(n // 2), str(3 * n // 4), str(q1)], "About 25%% of the data is below Q1. 25%% of %d = <b>%d</b>." % (n, n // 4))


def build():
    sets, R = build_sets([
        ("Dot plots", [("run", mm.set_dot, ("rnd", mm.People, lambda r: mm.Ctx(r, mm.DOT_CTX)), 20)]),
        ("Stem-and-leaf plots", [("collect", g4d.one_stem_read, 10), ("collect", g4d.one_stem_solve, 10)]),
        ("Histograms", [("collect", one_hist, 20)]),
        ("Read a box plot", [("collect", one_box, 20)]),
        ("What a box plot tells you", [("collect", one_box2, 20)]),
    ], 66022)
    finish(sets, R)
    body = lesson('<ul><li>A <b>dot plot</b> and a <b>stem-and-leaf plot</b> show every data value.</li><li>A <b>histogram</b> groups numbers into equal intervals. Each bar shows how many values are in an interval, not the values themselves.</li><li>A <b>box plot</b> shows the five-number summary: minimum, Q1, median, Q3 and maximum.</li><li>Each part of a box plot holds about 25% of the data. The box is the middle 50%; its length is the IQR.</li></ul>',
        [example("Box plot: 12, 18, 25, 31, 40", ["Median = 25", "IQR = 31 − 18"], "13"), example("Histogram bars 3, 7, 5 for 0–9, 10–19, 20–29", ["Values 10 or more: 7 + 5"], "12")],
        [['Reading a histogram bar as one value', 'A bar counts all the values in its interval.'], ['Thinking the middle of the box is always the median', 'Look for the line inside the box.'], ['Using the range instead of the IQR', 'IQR = Q3 − Q1, the length of the box.']])
    faq = [('What does TEKS 6.12A ask?', 'Represent numeric data graphically, including dot plots, stem-and-leaf plots, histograms and box plots.'), ('What does TEKS 6.13A ask?', 'Interpret numeric data summarized in dot plots, stem-and-leaf plots, histograms and box plots.'), ('Can you find the mean from a box plot?', 'No. A box plot shows only the five-number summary, not every value.'), ('Why can a long whisker still hold 25% of the data?', 'The values in that quarter are spread out, but there are just as many as in each other quarter.')]
    make('dot-plots-histograms-and-box-plots', 22, 'Measurement and Data', '6.12A, 6.13A',
         '6.12A represent numeric data graphically, including dot plots, stem-and-leaf plots, histograms, and box plots; 6.13A interpret numeric data summarized in dot plots, stem-and-leaf plots, histograms, and box plots',
         'Dot Plots, Stem-and-Leaf Plots, Histograms and Box Plots', 'Dot Plots, Histograms and Box Plots',
         'Free Grade 6 data worksheets for Texas TEKS 6.12A and 6.13A: read dot plots, stem-and-leaf plots, histograms and box plots, quartiles, range and IQR. 100 questions with answers.',
         'A box plot splits the data into four quarters of about 25% each.', 'Histogram bars count values in intervals. IQR = Q3 − Q1.',
         body, faq, sets, seo_title='Grade 6 Dot Plots, Histograms and Box Plots Worksheets (TEKS 6.12A, 6.13A, STAAR)')


if __name__ == "__main__":
    build()
