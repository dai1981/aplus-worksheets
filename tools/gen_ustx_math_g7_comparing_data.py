# -*- coding: utf-8 -*-
"""
Texas Grade 7 Math: Comparing Two Groups with Dot Plots and Box Plots (TEKS 7.12A)
  python3 tools/gen_ustx_math_g7_comparing_data.py
Median and interquartile range, comparing two groups, box plot tables, double box plots (own figures), and word
problems (US Grade 7 makers with a new seed).
Wrong answers come from real mistakes: comparing the maximums instead of the centers, using the range for the
spread of the middle half, and mixing up the two groups.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g7_comparing_data_distributions as cdd
adopt(cdd)
cdd.R = random.Random(670230)
tx_common.GRADE = "grade-7"

INK = "#1f2937"
BOX = [("Minutes of homework", 0, 60, 5, "Grade 7", "Grade 8"), ("Test scores", 50, 100, 5, "Class A", "Class B"), ("Heights of plants (cm)", 10, 40, 2, "Sunny spot", "Shady spot"),
       ("Points per game", 0, 40, 2, "Team A", "Team B"), ("Hours of sleep per week", 40, 64, 2, "Boys", "Girls")]


def box_two(label, lo, hi, step, ga, gb, A, B):
    W, x0, x1 = 340, 70, 330
    sx = lambda v: x0 + (x1 - x0) * (v - lo) / float(hi - lo)
    s = ["<svg viewBox='0 0 %d 170' width='%d' data-pf='lg' role='img' aria-label='double box plot: %s'>" % (W, W, label)]
    for name, f, y in ((ga, A, 40), (gb, B, 95)):
        mn, q1, md, q3, mx = f
        s.append("<text x='%d' y='%d' font-size='12' text-anchor='end' fill='%s'>%s</text>" % (x0 - 6, y + 4, INK, name))
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/><line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (sx(mn), y, sx(q1), y, INK, sx(q3), y, sx(mx), y, INK))
        for v in (mn, mx):
            s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (sx(v), y - 8, sx(v), y + 8, INK))
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='30' fill='%s' stroke='%s' stroke-width='2'/>" % (sx(q1), y - 15, sx(q3) - sx(q1), "#dbeafe" if y == 40 else "#fde68a", INK))
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (sx(md), y - 15, sx(md), y + 15, INK))
    tick = step * (2 if (hi - lo) // step > 12 else 1)
    s.append("<line x1='%d' y1='130' x2='%d' y2='130' stroke='%s'/>" % (x0, x1, INK))
    for t in range(lo, hi + 1, tick):
        s.append("<line x1='%.1f' y1='126' x2='%.1f' y2='134' stroke='%s'/><text x='%.1f' y='148' font-size='11' text-anchor='middle' fill='%s'>%d</text>" % (sx(t), sx(t), INK, sx(t), INK, t))
    s.append("<text x='%d' y='166' font-size='12' text-anchor='middle' fill='%s'>%s</text></svg>" % ((x0 + x1) // 2, INK, label))
    return fig("".join(s))


def five(r, lo, hi, step):
    p = sorted(r.sample(range(lo + step, hi, step), 5))
    return p


def one_double(r):
    label, lo, hi, step, ga, gb = r.choice(BOX)
    A, B = five(r, lo, hi, step), five(r, lo, hi, step)
    if A[2] == B[2] or (A[3] - A[1]) == (B[3] - B[1]):
        return None
    pic = box_two(label, lo, hi, step, ga, gb, A, B)
    kind = r.choice(["center", "spread", "diffmed", "range"])
    if kind == "center":
        hi_g = ga if A[2] > B[2] else gb
        lo_g = gb if hi_g == ga else ga
        return mcq(pic + "Which group has the greater median?", "%s (%d)" % (hi_g, max(A[2], B[2])), ["%s (%d)" % (lo_g, min(A[2], B[2])), "They are the same", "%s (%d)" % (hi_g, max(A[4], B[4]))],
                   "The line inside each box is the median: %s %d, %s %d. <b>%s</b> is greater." % (ga, A[2], gb, B[2], hi_g))
    if kind == "spread":
        ia, ib = A[3] - A[1], B[3] - B[1]
        g1 = ga if ia > ib else gb
        return mcq(pic + "Which group's middle half is more spread out (greater IQR)?", "%s (IQR %d)" % (g1, max(ia, ib)), ["%s (IQR %d)" % (gb if g1 == ga else ga, min(ia, ib)), "They are the same", "%s (IQR %d)" % (g1, max(A[4] - A[0], B[4] - B[0]))],
                   "IQR = Q3 − Q1: %s %d − %d = %d, %s %d − %d = %d. <b>%s</b> has the greater IQR." % (ga, A[3], A[1], ia, gb, B[3], B[1], ib, g1))
    if kind == "diffmed":
        d = abs(A[2] - B[2])
        return mcq(pic + "What is the difference between the two medians?", str(d), [str(abs(A[4] - B[4])) if abs(A[4] - B[4]) != d else str(d + step), str(A[2] + B[2]), str(abs((A[3] - A[1]) - (B[3] - B[1]))) if abs((A[3] - A[1]) - (B[3] - B[1])) != d else str(d * 2)],
                   "Medians: %d and %d. %d − %d = <b>%d</b>." % (A[2], B[2], max(A[2], B[2]), min(A[2], B[2]), d), allow_zero=False)
    ra, rb = A[4] - A[0], B[4] - B[0]
    if ra == rb:
        return None
    return mcq(pic + "What is the range of %s?" % ga, str(ra), [str(A[3] - A[1]), str(rb), str(A[4])], "Range = maximum − minimum = %d − %d = <b>%d</b>." % (A[4], A[0], ra))


def build():
    sets, R = build_sets([
        ("Median and interquartile range", [("run", cdd.set_iqr, (), 20)]),
        ("Compare two groups", [("run", cdd.set_compare, (), 20)]),
        ("Box plot tables and inferences", [("run", cdd.set_plots, (), 20)]),
        ("Double box plots", [("collect", one_double, 20)]),
        ("Word problems", [("run", cdd.set_words, (), 20)]),
    ], 67023)
    finish(sets, R)
    body = lesson('<ul><li>To compare two groups, look at <b>shape</b>, <b>center</b> and <b>spread</b>.</li><li><b>Center</b>: compare the medians (or means).</li><li><b>Spread</b>: compare the IQRs (Q3 − Q1) and ranges.</li><li>On a <b>double box plot</b>, both groups share one number line, so you can compare them at a glance.</li></ul>',
        [example("Class A median 75, IQR 10; Class B median 82, IQR 6", ["B has the higher center", "B is less spread out"], "Class B scored higher and more consistently")],
        [['Comparing the maximums instead of the centers', 'Compare the medians first.'], ['Using the range for the middle half', 'The middle half is the box: use the IQR.'], ['Mixing up the groups', 'Read the label next to each box.']])
    faq = [('What does TEKS 7.12A ask?', 'Compare two groups of numeric data using comparative dot plots or box plots by comparing their shapes, centers and spreads.'), ('Why compare medians?', 'The median shows a typical value and is not pulled by outliers.'), ('What does a narrow box mean?', 'The middle half of the data is close together.'), ('Can two groups have the same median but different spreads?', 'Yes. One group can be much more spread out.')]
    make('comparing-data-with-dot-plots-and-box-plots', 23, 'Measurement and Data', '7.12A',
         '7.12A compare two groups of numeric data using comparative dot plots or box plots by comparing their shapes, centers, and spreads',
         'Comparing Two Groups with Dot Plots and Box Plots', 'Comparing Data Distributions',
         'Free Grade 7 worksheets for Texas TEKS 7.12A: compare two groups with medians, IQR, double box plots and dot plots, and word problems. 100 questions with answers.',
         'Compare shape, center (median) and spread (IQR).', 'A narrow box means the middle half is close together.',
         body, faq, sets, seo_title='Grade 7 Comparing Data with Dot Plots and Box Plots Worksheets (TEKS 7.12A, STAAR)')


if __name__ == "__main__":
    build()
