# -*- coding: utf-8 -*-
"""
Texas Grade 5 Math: Bar Graphs, Dot Plots, Stem-and-Leaf Plots and Scatterplots (TEKS 5.9A, 5.9B, 5.9C)
  python3 tools/gen_ustx_math_g5_data.py
Bar graphs and frequency tables, dot plots with fractions (the US Grade 5 line plot makers with Texas names),
stem-and-leaf plots with whole numbers and decimals, reading scatterplots, and one- and two-step problems with
scatterplot data.
Wrong answers come from real mistakes: reading the wrong axis, misreading the scale, and reading a stem as a value.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g5_line_plots_fractions as lp5
import gen_ustx_math_g4_data as g4d
adopt(lp5)
tx_common.GRADE = "grade-5"

INK = "#1f2937"
GRID = "#d1d5db"


def bar_svg(title, cats, vals, step):
    top = (max(vals) // step + 1) * step
    W, H, x0, y0 = 340, 200, 46, 20
    ph = H - 40
    s = ["<svg viewBox='0 0 %d %d' width='%d' data-pf='lg' role='img' aria-label='bar graph: %s'>" % (W + 10, H + 40, W + 10, title)]
    for t in range(0, top + 1, step):
        y = y0 + ph - ph * t // top
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s'/><text x='%d' y='%d' font-size='12' text-anchor='end' fill='%s'>%d</text>" % (x0, y, W, y, GRID, x0 - 5, y + 4, INK, t))
    bw = (W - x0) // len(cats)
    for i, (c, v) in enumerate(zip(cats, vals)):
        x = x0 + i * bw + bw // 5
        h = ph * v // top
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#60a5fa' stroke='%s'/>" % (x, y0 + ph - h, bw * 3 // 5, h, INK))
        s.append("<text x='%d' y='%d' font-size='12' text-anchor='middle' fill='%s'>%s</text>" % (x + bw * 3 // 10, y0 + ph + 16, INK, c))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x0, y0 + ph, W, y0 + ph, INK))
    s.append("<text x='%d' y='%d' font-size='13' text-anchor='middle' fill='%s'>%s</text></svg>" % ((W + x0) // 2, H + 30, INK, title))
    return fig("".join(s))


BARS = [("Favorite Texas state park", ["Big Bend", "Palo Duro", "Enchanted", "Padre"]), ("Books read in March", ["Ana", "Ben", "Cruz", "Dee"]),
        ("Cans collected by grade", ["2nd", "3rd", "4th", "5th"]), ("Favorite lunch", ["Tacos", "Pizza", "Salad", "Chili"])]


def one_bar(r):
    title, cats = r.choice(BARS)
    step = r.choice([2, 5, 10])
    vals = [step * r.randint(1, 9) + (step // 2 if step == 10 and r.random() < 0.4 else 0) for _ in cats]
    if len(set(vals)) < 4:
        return None
    pic = bar_svg(title, cats, vals, step)
    i, j = r.sample(range(4), 2)
    kind = r.choice(["read", "diff", "total", "two"])
    if kind == "read":
        return mcq(pic + "What is the value for %s?" % cats[i], str(vals[i]), [str(vals[i] + step), str(vals[i] - step) if vals[i] > step else str(vals[i] + 2 * step), str(vals[i] // step)],
                   "The bar for %s ends at <b>%d</b>. Each grid line is %d." % (cats[i], vals[i], step))
    if kind == "diff":
        a, b = (i, j) if vals[i] > vals[j] else (j, i)
        return mcq(pic + "How much greater is %s than %s?" % (cats[a], cats[b]), str(vals[a] - vals[b]), [str(vals[a] + vals[b]), str(vals[a]), str(vals[a] - vals[b] + step)],
                   "%d − %d = <b>%d</b>." % (vals[a], vals[b], vals[a] - vals[b]))
    if kind == "total":
        return mcq(pic + "What is the total for all four bars?", str(sum(vals)), [str(sum(vals) - vals[i]), str(max(vals) * 4), str(sum(vals) + step)],
                   "%s = <b>%d</b>." % (" + ".join(map(str, vals)), sum(vals)))
    a = max(range(4), key=lambda t: vals[t])
    b = min(range(4), key=lambda t: vals[t])
    if vals[a] % vals[b]:
        return None
    return mcq(pic + "The greatest value is how many times as much as the least value?", str(vals[a] // vals[b]), [str(vals[a] - vals[b]), str(vals[a] // vals[b] + 1), str(vals[a] + vals[b])],
               "%d ÷ %d = <b>%d</b>." % (vals[a], vals[b], vals[a] // vals[b]))


def dec_stem(vals):
    stems = sorted(set(v // 10 for v in vals))
    rows = []
    for s in range(stems[0], stems[-1] + 1):
        rows.append("<tr><td>%d</td><td>%s</td></tr>" % (s, " ".join(str(v % 10) for v in sorted(vals) if v // 10 == s)))
    v = vals[0]
    return "<div class='qfig'><div class='sn-tw'><table class='sn-table'><thead><tr><th>Stem</th><th>Leaf</th></tr></thead><tbody>%s</tbody></table></div><p>Key: %d | %d means %d.%d</p></div>" % ("".join(rows), v // 10, v % 10, v // 10, v % 10)


DEC = [("Lengths of bean pods in centimeters", 52, 98), ("Long jump distances in meters", 21, 45), ("Rainfall in inches each month in Houston", 18, 67), ("Weights of puppies in pounds", 31, 79)]


def one_dstem(r):
    title, lo, hi = r.choice(DEC)
    vals = sorted(r.randint(lo, hi) for _ in range(r.randint(8, 11)))
    pic = dec_stem(vals)
    d = lambda v: "%d.%d" % (v // 10, v % 10)
    kind = r.choice(["max", "min", "range", "count"])
    if kind == "max":
        return mcq(pic + title + ". What is the greatest value?", d(max(vals)), [str(max(vals)), d(max(vals) - 10), "%d.%d" % (max(vals) % 10, max(vals) // 10)], "The last stem with its greatest leaf: <b>%s</b>." % d(max(vals)))
    if kind == "min":
        return mcq(pic + title + ". What is the least value?", d(min(vals)), [str(min(vals)), d(min(vals) + 10), "%d.%d" % (min(vals) % 10, min(vals) // 10)], "The first stem with its least leaf: <b>%s</b>." % d(min(vals)))
    if kind == "range":
        g = max(vals) - min(vals)
        return mcq(pic + title + ". What is the difference between the greatest and least values?", d(g), [str(g), d(g + 10), d(max(vals) + min(vals))], "%s − %s = <b>%s</b>." % (d(max(vals)), d(min(vals)), d(g)))
    t = r.choice(vals[2:-2])
    c = sum(1 for v in vals if v >= t)
    return mcq(pic + title + ". How many values are %s or greater?" % d(t), str(c), [str(len(vals) - c) if len(vals) - c != c else str(c + 2), str(c + 1), str(c - 1)], "Count the values from %s up: <b>%d</b>." % (d(t), c))


SC = [("Practice time (hours)", "Number of free throws", 8, 20, 1, "up"), ("TV time (hours a day)", "Reading time (minutes)", 6, 60, 1, "down"),
      ("Temperature (°F)", "Lemonade sold (glasses)", 100, 50, 1, "up"), ("Age of car (years)", "Value (thousands of dollars)", 10, 30, 1, "down"),
      ("Shoe size", "Spelling score", 10, 20, 0, "none"), ("Sunlight (hours a day)", "Plant height (cm)", 10, 30, 1, "up")]


def sc_data(r):
    xl, yl, xm, ym, _, trend = r.choice(SC)
    n = r.randint(7, 9)
    if xm == 100:
        xs = sorted(r.sample(range(60, 101, 5), n))
    else:
        xs = sorted(r.sample(range(1, xm + 1), min(n, xm)))
    pts = []
    for x in xs:
        f = (x - xs[0]) / float(xs[-1] - xs[0] or 1)
        base = {"up": 0.15 + 0.7 * f, "down": 0.85 - 0.7 * f, "none": r.uniform(0.15, 0.85)}[trend]
        y = int(round(ym * min(0.95, max(0.05, base + r.uniform(-0.1, 0.1)))))
        pts.append((x, y))
    return xl, yl, xm, ym, trend, pts


def sc_svg(xl, yl, xm, ym, pts):
    W, H, x0, y0 = 340, 220, 50, 15
    pw, ph = W - x0 - 10, H - 40
    xmin = 60 if xm == 100 else 0
    sx = lambda x: x0 + pw * (x - xmin) / float(xm - xmin)
    sy = lambda y: y0 + ph - ph * y / float(ym)
    ystep = ym // 5 if ym % 5 == 0 else ym // 4
    xstep = 5 if xm == 100 else 1
    s = ["<svg viewBox='0 0 %d %d' width='%d' data-pf='lg' role='img' aria-label='scatterplot of %s and %s'>" % (W, H + 25, W, xl, yl)]
    for t in range(0, ym + 1, ystep):
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s'/><text x='%d' y='%.1f' font-size='11' text-anchor='end' fill='%s'>%d</text>" % (x0, sy(t), x0 + pw, sy(t), GRID, x0 - 4, sy(t) + 4, INK, t))
    for t in range(xmin, xm + 1, xstep):
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s'/><text x='%.1f' y='%d' font-size='11' text-anchor='middle' fill='%s'>%d</text>" % (sx(t), y0, sx(t), y0 + ph, GRID, sx(t), y0 + ph + 14, INK, t))
    for x, y in pts:
        s.append("<circle cx='%.1f' cy='%.1f' r='4.5' fill='#2563eb'/>" % (sx(x), sy(y)))
    s.append("<text x='%d' y='%d' font-size='12' text-anchor='middle' fill='%s'>%s</text>" % (x0 + pw // 2, H + 18, INK, xl))
    s.append("<text x='12' y='%d' font-size='12' text-anchor='middle' fill='%s' transform='rotate(-90 12 %d)'>%s</text></svg>" % (y0 + ph // 2, INK, y0 + ph // 2, yl))
    return fig("".join(s))


def one_sc_read(r):
    xl, yl, xm, ym, trend, pts = sc_data(r)
    st = ym // 5 if ym % 5 == 0 else ym // 4
    pts = [(x, int(round(y / float(st) * 2)) * st // 2) for x, y in pts]
    if st % 2:
        pts = [(x, y // st * st) for x, y in pts]
    pic = sc_svg(xl, yl, xm, ym, pts)
    kind = r.choice(["y", "x", "max", "count"])
    x, y = r.choice(pts)
    if kind == "y":
        return mcq(pic + "What is the %s for the point at %s = %d?" % (yl.split(" (")[0].lower(), xl.split(" (")[0].lower(), x), str(y), [str(x), str(y + st), str(y - st // 2) if y > st else str(y + 2 * st)],
                   "Go up from %d on the bottom axis to the dot, then across: <b>%d</b>." % (x, y))
    if kind == "x":
        if sum(1 for p in pts if p[1] == y) > 1:
            return None
        return mcq(pic + "One point has a %s of %d. What is its %s?" % (yl.split(" (")[0].lower(), y, xl.split(" (")[0].lower()), str(x), [str(y), str(x + 1 if xm != 100 else x + 5), str(x - 1 if xm != 100 else x - 5)],
                   "Go across from %d to the dot, then down: <b>%d</b>." % (y, x))
    if kind == "max":
        m = max(pts, key=lambda p: p[1])
        if sum(1 for p in pts if p[1] == m[1]) > 1:
            return None
        return mcq(pic + "Which point has the greatest %s?" % yl.split(" (")[0].lower(), "(%d, %d)" % m, ["(%d, %d)" % (m[1], m[0])] + ["(%d, %d)" % p for p in r.sample([p for p in pts if p != m], 2)],
                   "The highest dot is at <b>(%d, %d)</b>." % m)
    return mcq(pic + "How many points are shown on the scatterplot?", str(len(pts)), [str(len(pts) + 1), str(len(pts) - 1), str(len(pts) + 2)], "Count every dot: <b>%d</b>." % len(pts))


def one_sc_solve(r):
    xl, yl, xm, ym, trend, pts = sc_data(r)
    st = ym // 5 if ym % 5 == 0 else ym // 4
    pts = [(x, y // (st // 2 or 1) * (st // 2 or 1)) for x, y in pts]
    pic = sc_svg(xl, yl, xm, ym, pts)
    yn = yl.split(" (")[0].lower()
    kind = r.choice(["trend", "trend", "diff", "above"])
    if kind == "trend":
        right = {"up": "As %s increases, %s tends to increase." % (xl.split(" (")[0].lower(), yn), "down": "As %s increases, %s tends to decrease." % (xl.split(" (")[0].lower(), yn), "none": "There is no clear pattern."}
        return mcq(pic + "Which statement describes the data?", right[trend], [v for k2, v in right.items() if k2 != trend] + ["Every point has the same %s." % yn],
                   {"up": "The dots go <b>up</b> from left to right.", "down": "The dots go <b>down</b> from left to right.", "none": "The dots are scattered with <b>no clear pattern</b>."}[trend])
    if kind == "diff":
        hi, lo = max(p[1] for p in pts), min(p[1] for p in pts)
        return mcq(pic + "What is the difference between the greatest and least %s?" % yn, str(hi - lo), [str(hi + lo), str(hi), str(hi - lo + st)], "%d − %d = <b>%d</b>." % (hi, lo, hi - lo))
    t = sorted(p[1] for p in pts)[len(pts) // 2]
    c = sum(1 for p in pts if p[1] > t)
    return mcq(pic + "How many points have a %s greater than %d?" % (yn, t), str(c), [str(c + 1), str(len(pts) - c), str(c - 1) if c > 1 else str(c + 2)], "Count the dots above the %d line: <b>%d</b>." % (t, c), allow_zero=True) if len(pts) - c != c else None


def build():
    sets, R = build_sets([
        ("Bar graphs and frequency tables", [("collect", one_bar, 10), ("collect", g4d.one_freq, 10)]),
        ("Dot plots with fractions", [("run", lp5.set_total, ("rnd", lp5.People, lp5.Ctx), 20)]),
        ("Stem-and-leaf plots", [("collect", one_dstem, 10), ("collect", g4d.one_stem_solve, 10)]),
        ("Read scatterplots", [("collect", one_sc_read, 20)]),
        ("Scatterplot patterns and problems", [("collect", one_sc_solve, 20)]),
    ], 65021)
    finish(sets, R)
    body = lesson('<ul><li><b>Bar graphs</b> and <b>frequency tables</b> show categories, such as favorite foods. Check the scale on a bar graph.</li><li><b>Dot plots</b> and <b>stem-and-leaf plots</b> show numbers, including fractions and decimals. Read the key: 4 | 7 can mean 47 or 4.7.</li><li>A <b>scatterplot</b> shows pairs of numbers as points. Read across for x and up for y.</li><li>If the points go up from left to right, y tends to increase as x increases.</li></ul>',
        [example("Stem-and-leaf plot with key 3 | 4 = 3.4: stems 3, 4; leaves 4 8 | 1 5", ["Values: 3.4, 3.8, 4.1, 4.5", "4.5 − 3.4"], "1.1")],
        [['Reading the wrong axis on a scatterplot', 'x is across the bottom; y goes up the side.'], ['Misreading the scale on a bar graph', 'Find what each grid line is worth first.'], ['Ignoring the key in a stem-and-leaf plot', 'The key tells you if 4 | 7 is 47 or 4.7.']])
    faq = [('What does TEKS 5.9A ask?', 'Represent categorical data with bar graphs or frequency tables and numerical data, including data sets of measurements in fractions or decimals, with dot plots or stem-and-leaf plots.'), ('What does TEKS 5.9B ask?', 'Represent discrete paired data on a scatterplot.'), ('What does TEKS 5.9C ask?', 'Solve one- and two-step problems using data from a frequency table, dot plot, bar graph, stem-and-leaf plot or scatterplot.'), ('What is a scatterplot?', 'A graph of paired data. Each point shows two numbers, such as hours of practice and free throws made.')]
    make('data-and-scatterplots', 21, 'Data Analysis', '5.9A, 5.9B, 5.9C',
         '5.9A represent categorical data with bar graphs or frequency tables and numerical data, including data sets of measurements in fractions or decimals, with dot plots or stem-and-leaf plots; 5.9B represent discrete paired data on a scatterplot; 5.9C solve one- and two-step problems using data from a frequency table, dot plot, bar graph, stem-and-leaf plot, or scatterplot',
         'Bar Graphs, Dot Plots, Stem-and-Leaf Plots and Scatterplots', 'Data and Scatterplots',
         'Free Grade 5 data worksheets for Texas TEKS 5.9A, 5.9B and 5.9C: bar graphs, frequency tables, dot plots with fractions, stem-and-leaf plots with decimals and scatterplots. 100 questions with answers.',
         'Read the scale, the key and the axes before you answer.', 'Scatterplot: x across, y up. Stem-and-leaf: check the key (4 | 7 = 4.7).',
         body, faq, sets, seo_title='Grade 5 Data Worksheets: Dot Plots, Stem-and-Leaf Plots and Scatterplots (TEKS 5.9, STAAR)')


if __name__ == "__main__":
    build()
