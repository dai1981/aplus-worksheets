# -*- coding: utf-8 -*-
"""
Texas Grade 4 Math: Frequency Tables, Dot Plots and Stem-and-Leaf Plots (TEKS 4.9A, 4.9B)
  python3 tools/gen_ustx_math_g4_data.py
Reading dot plots with fractions and adding and comparing their data (the US Grade 4 line plot makers with Texas
names; a dot plot is a line plot), frequency tables, and stem-and-leaf plots with one- and two-step problems.
Wrong answers come from real mistakes: reading a stem as the data value, counting the leaves of the wrong stem, and
forgetting the key.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g4_line_plots_fractions as usl
adopt(usl)
tx_common.GRADE = "grade-4"

def stem_leaf(vals):
    stems = sorted(set(v // 10 for v in vals))
    rows = []
    for s in range(stems[0], stems[-1] + 1):
        leaves = sorted(v % 10 for v in vals if v // 10 == s)
        rows.append("<tr><td>%d</td><td>%s</td></tr>" % (s, " ".join(str(l) for l in leaves)))
    key = "Key: %d | %d means %d" % (vals[0] // 10, vals[0] % 10, vals[0])
    return "<div class='qfig'><div class='sn-tw'><table class='sn-table'><thead><tr><th>Stem</th><th>Leaf</th></tr></thead><tbody>%s</tbody></table></div><p>%s</p></div>" % ("".join(rows), key)


CTX = [("Points scored by the team in each game", 20, 69), ("Ages of people at a family reunion", 21, 78), ("Heights of plants in centimeters", 12, 47),
       ("Minutes spent reading each day", 15, 58), ("Number of push-ups in one minute", 10, 45), ("Temperatures in degrees Fahrenheit in Austin", 52, 96)]


def data(r):
    title, lo, hi = r.choice(CTX)
    n = r.randint(8, 12)
    vals = sorted(r.randint(lo, hi) for _ in range(n))
    return title, vals


def one_stem_read(r):
    title, vals = data(r)
    pic = stem_leaf(vals)
    kind = r.choice(["count", "max", "min", "stem"])
    if kind == "count":
        return mcq(pic + title + ". How many data values are there?", len(vals), [len(set(v // 10 for v in vals)), len(vals) + 1, len(vals) - 1], "Count every leaf: <b>%d</b>." % len(vals))
    if kind == "max":
        return mcq(pic + title + ". What is the greatest value?", max(vals), [max(vals) // 10, max(vals) - 10, int(str(max(vals))[::-1]) if max(vals) % 10 else max(vals) + 1],
                   "The last stem with its greatest leaf: <b>%d</b>." % max(vals))
    if kind == "min":
        return mcq(pic + title + ". What is the least value?", min(vals), [min(vals) // 10, min(vals) + 10, int(str(min(vals))[::-1]) if min(vals) % 10 else min(vals) + 1],
                   "The first stem with its least leaf: <b>%d</b>." % min(vals))
    s = r.choice(sorted(set(v // 10 for v in vals)))
    c = sum(1 for v in vals if v // 10 == s)
    return mcq(pic + title + ". How many values are in the %ds (from %d to %d)?" % (s * 10, s * 10, s * 10 + 9), c, [s, c + 1, len(vals) - c if len(vals) - c != c else c + 2], "Count the leaves next to stem %d: <b>%d</b>." % (s, c), allow_zero=False)


def one_stem_solve(r):
    title, vals = data(r)
    pic = stem_leaf(vals)
    kind = r.choice(["range", "more_than", "diff", "total_small"])
    if kind == "range":
        return mcq(pic + title + ". What is the difference between the greatest and least values?", max(vals) - min(vals), [max(vals) - min(vals) + 10, max(vals) // 10 - min(vals) // 10, max(vals) + min(vals)],
                   "%d − %d = <b>%d</b>." % (max(vals), min(vals), max(vals) - min(vals)))
    if kind == "more_than":
        t = r.choice(vals[2:-2]) // 10 * 10 + 5
        c = sum(1 for v in vals if v > t)
        return mcq(pic + title + ". How many values are greater than %d?" % t, c, [len(vals) - c if len(vals) - c != c else c + 1, c + 1, c - 1 if c > 1 else c + 2], "Count the values above %d: <b>%d</b>." % (t, c), allow_zero=True)
    if kind == "diff":
        a, b = vals[-1], vals[-2]
        if a == b:
            return None
        return mcq(pic + title + ". How much greater is the greatest value than the second greatest?", a - b, [a + b, a - b + 10, b - vals[0]], "%d − %d = <b>%d</b>." % (a, b, a - b))
    a, b = vals[0], vals[1]
    return mcq(pic + title + ". What is the sum of the two least values?", a + b, [a, b, a + b + 10], "%d + %d = <b>%d</b>." % (a, b, a + b))


def one_freq(r):
    cats = r.choice([("Favorite sport", ["Soccer", "Football", "Basketball", "Baseball"]), ("Pets at home", ["Dog", "Cat", "Fish", "Bird"]), ("Lunch choice", ["Tacos", "Pizza", "Salad", "Sandwich"])])
    vals = r.sample(range(3, 19), 4)
    rows = "".join("<tr><td>%s</td><td>%d</td></tr>" % (c, v) for c, v in zip(cats[1], vals))
    pic = "<div class='qfig'><div class='sn-tw'><table class='sn-table'><thead><tr><th>%s</th><th>Frequency</th></tr></thead><tbody>%s</tbody></table></div></div>" % (cats[0], rows)
    kind = r.choice(["total", "more", "two"])
    i, j = r.sample(range(4), 2)
    if kind == "total":
        return mcq(pic + "How many students answered in all?", sum(vals), [sum(vals) - vals[i], max(vals) * 4, sum(vals) + 1], "%s = <b>%d</b>." % (" + ".join(map(str, vals)), sum(vals)))
    if kind == "more":
        a, b = (i, j) if vals[i] > vals[j] else (j, i)
        return mcq(pic + "How many more students chose %s than %s?" % (cats[1][a], cats[1][b]), vals[a] - vals[b], [vals[a] + vals[b], vals[a], vals[a] - vals[b] + 1], "%d − %d = <b>%d</b>." % (vals[a], vals[b], vals[a] - vals[b]))
    return mcq(pic + "How many students did <b>not</b> choose %s?" % cats[1][i], sum(vals) - vals[i], [vals[i], sum(vals), sum(vals) - vals[i] - 1], "%d − %d = <b>%d</b>." % (sum(vals), vals[i], sum(vals) - vals[i]))


def build():
    sets, R = build_sets([
        ("Read dot plots with fractions", [("run", usl.set_read, ("rnd", usl.People, usl.Ctx), 20)]),
        ("Add and compare data on dot plots", [("run", usl.set_total, ("rnd", usl.People, usl.Ctx), 10), ("run", usl.set_diff, ("rnd", usl.People, usl.Ctx), 10)]),
        ("Frequency tables", [("collect", one_freq, 20)]),
        ("Read stem-and-leaf plots", [("collect", one_stem_read, 20)]),
        ("Solve problems with stem-and-leaf plots", [("collect", one_stem_solve, 20)]),
    ], 64023)
    finish(sets, R)
    body = lesson('<ul><li>A <b>frequency table</b> lists each category and how many times it occurs.</li><li>A <b>dot plot</b> has one dot for each data value above a number line. Values can be whole numbers or fractions.</li><li>In a <b>stem-and-leaf plot</b>, the stem is the tens digit and each leaf is a ones digit. Read the key: 4 | 7 means 47.</li><li>Use the data to add, subtract and compare in one or two steps.</li></ul>',
        [stem_leaf([23, 27, 31, 35, 35, 42, 48]) + "<p>The values are 23, 27, 31, 35, 35, 42 and 48. The greatest is 48.</p>"],
        [['Reading a stem as a data value', 'Every value needs a stem and a leaf: 4 | 2 is 42.'], ['Counting the leaves of the wrong stem', 'Find the stem first, then count only its leaves.'], ['Ignoring fractions on a dot plot', 'Read each mark on the number line, such as 2 1/4.']])
    faq = [('What does TEKS 4.9A ask?', 'Represent data on a frequency table, dot plot or stem-and-leaf plot marked with whole numbers and fractions.'), ('What does TEKS 4.9B ask?', 'Solve one- and two-step problems using data in whole number, decimal and fraction form in a frequency table, dot plot or stem-and-leaf plot.'), ('How do you read a stem-and-leaf plot?', 'Put each stem with each of its leaves. With the key 3 | 6 = 36, the row 3 | 1 4 6 shows 31, 34 and 36.'), ('What is the difference between a dot plot and a frequency table?', 'A dot plot shows each value as a dot on a number line. A frequency table lists the counts as numbers.')]
    make('frequency-tables-dot-plots-and-stem-and-leaf-plots', 23, 'Data Analysis', '4.9A, 4.9B',
         '4.9A represent data on a frequency table, dot plot, or stem-and-leaf plot marked with whole numbers and fractions; 4.9B solve one- and two-step problems using data in whole number, decimal, and fraction form in a frequency table, dot plot, or stem-and-leaf plot',
         'Frequency Tables, Dot Plots and Stem-and-Leaf Plots', 'Dot Plots and Stem-and-Leaf Plots',
         'Free Grade 4 data worksheets for Texas TEKS 4.9A and 4.9B: dot plots with fractions, frequency tables, stem-and-leaf plots and one- and two-step problems. 100 STAAR-style questions with answers.',
         'A stem is the tens digit; a leaf is the ones digit.', 'Read the key first. In a dot plot each dot is one value; count the dots above each mark.',
         body, faq, sets, seo_title='Grade 4 Dot Plots and Stem-and-Leaf Plots Worksheets (TEKS 4.9A, 4.9B, STAAR)')


if __name__ == "__main__":
    build()
