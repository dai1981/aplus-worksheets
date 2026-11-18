# -*- coding: utf-8 -*-
"""
Texas Grade 6 Math: Categorical Data: Mode, Relative Frequency and Percent Bar Graphs (TEKS 6.12D)
  python3 tools/gen_ustx_math_g6_categorical_data.py
The mode of categorical data, relative frequency as a fraction and decimal, percents of categories, percent bar
graphs, and word problems with relative frequency tables.
Wrong answers come from real mistakes: using the largest count as the relative frequency, dividing by the wrong
total, and reading a percent bar as counts.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
from fractions import Fraction as F
tx_common.GRADE = "grade-6"

INK = "#1f2937"
COLS = ["#60a5fa", "#fbbf24", "#34d399", "#f87171", "#a78bfa"]

CATS = [("Favorite sport", ["Football", "Soccer", "Basketball", "Baseball", "Volleyball"]), ("Favorite food", ["Tacos", "Barbecue", "Pizza", "Enchiladas", "Burgers"]),
        ("Way to get to school", ["Bus", "Car", "Walk", "Bike"]), ("Pet at home", ["Dog", "Cat", "Fish", "Bird", "None"]), ("Favorite season", ["Spring", "Summer", "Fall", "Winter"])]


def dec(v):
    return ("%.3f" % float(v)).rstrip("0").rstrip(".")


def ftable(title, cats, counts, extra=None):
    rows = "".join("<tr><td>%s</td><td>%d</td>%s</tr>" % (c, n, "" if extra is None else "<td>%s</td>" % extra[i]) for i, (c, n) in enumerate(zip(cats, counts)))
    head = "<th>%s</th><th>Frequency</th>%s" % (title, "" if extra is None else "<th>Relative frequency</th>")
    return "<div class='qfig'><div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div></div>" % (head, rows)


def data(r, total_choices=(20, 25, 40, 50)):
    title, cats = r.choice(CATS)
    k = min(len(cats), r.choice([3, 4, 5]))
    cats = cats[:k]
    tot = r.choice(total_choices)
    for _ in range(50):
        cuts = sorted(r.sample(range(1, tot), k - 1))
        counts = [b - a for a, b in zip([0] + cuts, cuts + [tot])]
        if min(counts) >= 1 and len(set(counts)) == k:
            return title, cats, counts, tot
    return None


def one_mode(r):
    d = data(r)
    if not d:
        return None
    title, cats, counts, tot = d
    m = max(range(len(cats)), key=lambda i: counts[i])
    return mcq(ftable(title, cats, counts) + "What is the mode of the data?", cats[m], [str(counts[m]), cats[min(range(len(cats)), key=lambda i: counts[i])], str(tot)],
               "The mode is the category that occurs most often: <b>%s</b> (%d)." % (cats[m], counts[m]))


def one_rel(r):
    d = data(r)
    if not d:
        return None
    title, cats, counts, tot = d
    i = r.randrange(len(cats))
    v = F(counts[i], tot)
    if r.random() < 0.5:
        return mcq(ftable(title, cats, counts) + "What is the relative frequency of %s as a fraction?" % cats[i], fr(v.numerator, v.denominator) if v.denominator > 1 else "1",
                   [fr(counts[i], tot - counts[i]) if tot - counts[i] > 0 else "0", str(counts[i]), fr(1, len(cats))] if fr(1, len(cats)) != fr(v.numerator, v.denominator) else [fr(counts[i], tot - counts[i]), str(counts[i]), fr(counts[i], 100)],
                   "Relative frequency = frequency ÷ total = %d/%d = <b>%s</b>." % (counts[i], tot, fr(v.numerator, v.denominator)))
    return mcq(ftable(title, cats, counts) + "What is the relative frequency of %s as a decimal?" % cats[i], dec(v), [dec(F(counts[i], 100)), dec(F(tot - counts[i], tot)), str(counts[i])],
               "%d ÷ %d = <b>%s</b>." % (counts[i], tot, dec(v)))


def one_pct(r):
    d = data(r)
    if not d:
        return None
    title, cats, counts, tot = d
    i = r.randrange(len(cats))
    p = F(counts[i] * 100, tot)
    ps = dec(p) + "%"
    if r.random() < 0.5:
        return mcq(ftable(title, cats, counts) + "What percent of the answers were %s?" % cats[i], ps, ["%d%%" % counts[i], dec(F(counts[i] * 10, tot)) + "%", dec(F((tot - counts[i]) * 100, tot)) + "%"],
                   "%d/%d = %s = <b>%s</b>." % (counts[i], tot, dec(F(counts[i], tot)), ps))
    j = r.choice([t for t in range(len(cats)) if t != i])
    q = F((counts[i] + counts[j]) * 100, tot)
    return mcq(ftable(title, cats, counts) + "What percent of the answers were %s or %s?" % (cats[i], cats[j]), dec(q) + "%", [dec(p) + "%", "%d%%" % (counts[i] + counts[j]), dec(100 - q) + "%"],
               "(%d + %d)/%d = %d/%d = <b>%s%%</b>." % (counts[i], counts[j], tot, counts[i] + counts[j], tot, dec(q)))


def pbar_svg(title, cats, pcts):
    W, x0, x1 = 340, 10, 330
    s = ["<svg viewBox='0 0 %d 150' width='%d' data-pf='lg' role='img' aria-label='percent bar graph: %s'>" % (W, W, title)]
    x = x0
    for i, (c, p) in enumerate(zip(cats, pcts)):
        w = (x1 - x0) * p / 100.0
        s.append("<rect x='%.1f' y='20' width='%.1f' height='44' fill='%s' stroke='%s'/>" % (x, w, COLS[i], INK))
        s.append("<text x='%.1f' y='47' font-size='12' text-anchor='middle' fill='%s'>%d%%</text>" % (x + w / 2, INK, p))
        x += w
    for i, c in enumerate(cats):
        lx = x0 + (i % 3) * 110
        ly = 90 + (i // 3) * 22
        s.append("<rect x='%d' y='%d' width='14' height='14' fill='%s' stroke='%s'/><text x='%d' y='%d' font-size='12' fill='%s'>%s</text>" % (lx, ly - 11, COLS[i], INK, lx + 20, ly, INK, c))
    s.append("<text x='%d' y='12' font-size='12' text-anchor='middle' fill='%s'>%s</text></svg>" % (W // 2, INK, title))
    return fig("".join(s))


def one_pbar(r):
    title, cats = r.choice(CATS)
    k = min(len(cats), r.choice([3, 4]))
    cats = cats[:k]
    for _ in range(30):
        cuts = sorted(r.sample(range(5, 100, 5), k - 1))
        pcts = [b - a for a, b in zip([0] + cuts, cuts + [100])]
        if min(pcts) >= 10 and len(set(pcts)) == k:
            break
    else:
        return None
    pic = pbar_svg(title, cats, pcts)
    i = r.randrange(k)
    kind = r.choice(["read", "count", "more", "notcat"])
    if kind == "read":
        return mcq(pic + "What percent of students chose %s?" % cats[i], "%d%%" % pcts[i], ["%d%%" % (100 - pcts[i]), "%d%%" % pcts[(i + 1) % k], "%d%%" % (pcts[i] + 10)],
                   "The %s part of the bar is labeled <b>%d%%</b>." % (cats[i], pcts[i]))
    if kind == "count":
        n = r.choice([20, 40, 60, 80, 120, 200])
        if n * pcts[i] % 100:
            return None
        return mcq(pic + "%d students were surveyed. How many chose %s?" % (n, cats[i]), str(n * pcts[i] // 100), [str(pcts[i]), str(n - n * pcts[i] // 100), str(n * pcts[i] // 10)],
                   "%d%% of %d = %s × %d = <b>%d</b>." % (pcts[i], n, dec(F(pcts[i], 100)), n, n * pcts[i] // 100))
    if kind == "notcat":
        return mcq(pic + "What percent of students did <b>not</b> choose %s?" % cats[i], "%d%%" % (100 - pcts[i]), ["%d%%" % pcts[i], "%d%%" % (100 - pcts[i] - 10), "%d%%" % (pcts[i] + pcts[(i + 1) % k])],
                   "100%% − %d%% = <b>%d%%</b>." % (pcts[i], 100 - pcts[i]))
    j = r.choice([t for t in range(k) if t != i])
    a, b = (i, j) if pcts[i] > pcts[j] else (j, i)
    return mcq(pic + "How many percentage points more chose %s than %s?" % (cats[a], cats[b]), "%d" % (pcts[a] - pcts[b]), ["%d" % (pcts[a] + pcts[b]), "%d" % pcts[a], "%d" % (pcts[a] - pcts[b] + 5)],
               "%d − %d = <b>%d</b> percentage points." % (pcts[a], pcts[b], pcts[a] - pcts[b]))


def one_word(r):
    title, cats = r.choice(CATS)
    c = r.choice(cats)
    rf = r.choice([F(1, 4), F(1, 5), F(2, 5), F(3, 10), F(3, 4), F(1, 10), F(3, 5), F(7, 20)])
    n = rf.denominator * r.randint(2, 12)
    k = n * rf
    form = r.choice(["dec", "pct", "frac"])
    shown = {"dec": dec(rf), "pct": dec(rf * 100) + "%", "frac": fr(rf.numerator, rf.denominator)}[form]
    if r.random() < 0.5:
        return mcq("A survey of %d students asked about %s. The relative frequency of <b>%s</b> was %s. How many students chose %s?" % (n, title.lower(), c, shown, c), str(k), [str(n - k), str(rf.numerator * n // 10) if rf.numerator * n % 10 == 0 and rf.numerator * n // 10 != k else str(k + 2), str(n // rf.denominator) if n // rf.denominator != k else str(k * 2)],
                   "%s × %d = <b>%d</b>." % (shown, n, k))
    return mcq("%d of %d students chose %s. What is the relative frequency as a percent?" % (k, n, c), dec(rf * 100) + "%", ["%d%%" % k, dec((1 - rf) * 100) + "%", dec(rf * 10) + "%"],
               "%d ÷ %d = %s = <b>%s%%</b>." % (k, n, dec(rf), dec(rf * 100)))


def build():
    sets, R = build_sets([
        ("The mode of categorical data", [("collect", one_mode, 20)]),
        ("Relative frequency", [("collect", one_rel, 20)]),
        ("Percents of categories", [("collect", one_pct, 20)]),
        ("Percent bar graphs", [("collect", one_pbar, 20)]),
        ("Relative frequency word problems", [("collect", one_word, 20)]),
    ], 66024)
    finish(sets, R)
    body = lesson('<ul><li><b>Categorical data</b> are names or labels, such as favorite sport. You cannot find a mean, but you can find the <b>mode</b>.</li><li><b>Relative frequency</b> = frequency ÷ total. It can be a fraction, decimal or percent: 6 of 24 = 1/4 = 0.25 = 25%.</li><li>The relative frequencies of all the categories add to 1 (or 100%).</li><li>A <b>percent bar graph</b> shows each category as part of one bar that equals 100%.</li></ul>',
        [example("Soccer: 9 of 30 students", ["9 ÷ 30 = 0.3"], "30%"), example("Bar: Bus 45%. 80 students surveyed.", ["0.45 × 80"], "36 students")],
        [['Using the count as the relative frequency', 'Divide the count by the total.'], ['Dividing by the wrong total', 'The total is the sum of all the frequencies.'], ['Reading a percent bar as counts', 'The bar shows percents; multiply by the total to get counts.']])
    faq = [('What does TEKS 6.12D ask?', 'Summarize categorical data with numerical and graphical summaries, including the mode, the percent of values in each category (relative frequency table) and the percent bar graph, and use these summaries to describe the data distribution.'), ('Can categorical data have a mean?', 'No. You cannot add labels, so use the mode or relative frequencies.'), ('Do relative frequencies always add to 1?', 'Yes. All the parts together make the whole survey.'), ('What is a percent bar graph?', 'One bar that stands for 100%, divided into parts for each category.')]
    make('categorical-data-and-relative-frequency', 24, 'Measurement and Data', '6.12D',
         '6.12D summarize categorical data with numerical and graphical summaries, including the mode, the percent of values in each category (relative frequency table), and the percent bar graph, and use these summaries to describe the data distribution',
         'Categorical Data: Mode, Relative Frequency and Percent Bar Graphs', 'Categorical Data and Relative Frequency',
         'Free Grade 6 worksheets for Texas TEKS 6.12D: the mode of categorical data, relative frequency tables, percents of categories, percent bar graphs and word problems. 100 questions with answers.',
         'Relative frequency = frequency ÷ total.', '9 of 30 = 0.3 = 30%. All the relative frequencies add to 100%.',
         body, faq, sets, seo_title='Grade 6 Categorical Data and Relative Frequency Worksheets: Percent Bar Graphs (TEKS 6.12D, STAAR)')


if __name__ == "__main__":
    build()
