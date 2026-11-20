# -*- coding: utf-8 -*-
"""
South Africa Grade 9 Maths (CAPS): Representing Data: Scatter Plots, Histograms and Pie Charts (Grade 9: 5.2 Represent and interpret data)
  python3 tools/gen_za_maths_g9_representing_data.py
Scatter plots and correlation, lines of best fit, outliers, histograms and pie charts (UK Year 9, Singapore Secondary 2
and BC Grade 7 makers).
Wrong answers come from real mistakes: thinking correlation means one causes the other, reading a value far outside
the data from a line of best fit, and using 100 instead of 360 for a pie chart.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y9_scatter_graphs_and_correlation as uks
adopt(uks)
if isinstance(getattr(uks, 'R', None), random.Random): uks.R = random.Random(809200)
import gen_sg_maths_s2_frequency_tables_and_grouped_data as sgf
adopt(sgf)
if isinstance(getattr(sgf, 'R', None), random.Random): sgf.R = random.Random(809201)
import gen_cabc_math_g7_circle_graphs as cbc
adopt(cbc)
if isinstance(getattr(cbc, 'R', None), random.Random): cbc.R = random.Random(809202)
za_common.GRADE = "grade-9"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok9(it):
    """Grade 9: no trigonometry, quadratic formula, simultaneous equations or cones and spheres (Grade 10+)"""
    return not _re.search(r"\b(sin|cos|tan)\b|quadratic formula|discriminant|simultaneous|\bcone|\bsphere|imperial|\bmiles?\b", _txt(it))



def build():
    sets, R = build_sets([
        ("Describe the correlation", [("collect", uks.one_desc, 20)]),
        ("Lines of best fit", [("collect", uks.one_bf, 20)]),
        ("Outliers", [("collect", uks.one_out, 20)]),
        ("Histograms", [("collect", sgf.one_grouped, 20)]),
        ("Pie charts", [("collect", sgf.one_pie, 10), ("run", cbc.set_degrees, (), 10, ok9)]),
    ], 80920)
    finish(sets, R)
    body = lesson('<ul><li>A scatter plot shows two sets of data. Positive correlation: both increase; negative: one increases as the other decreases.</li><li>A line of best fit follows the trend and can be used to estimate values inside the data range.</li><li>An outlier is a point far from the others.</li><li>Pie chart: angle = fraction × 360°.</li></ul>',
        [example("Hours studied and test marks rise together", ["points go up to the right"], "positive correlation")],
        [['Correlation is cause', 'It does not prove one causes the other.'], ['Far outside the data', 'Estimate only inside the range.'], ['100 for a pie chart', 'Use 360°.']])
    faq = [('What does CAPS Grade 9 say about representing data?', 'Draw and interpret bar graphs, histograms, pie charts, broken-line graphs and scatter plots.'), ('What is no correlation?', 'The points show no pattern.'), ('What is extrapolation?', 'Estimating outside the data range; it can be unreliable.'), ('When is a histogram used?', 'For grouped numerical data.')]
    make('scatter-plots-histograms-and-pie-charts', 20, 'Data Handling', 'Grade 9: 5.2 Represent and interpret data',
         'Draw a variety of graphs by hand or technology to display and interpret data, including bar graphs and double bar graphs, histograms with given and own intervals, pie charts, broken-line graphs and scatter plots; critically read and interpret data represented in a variety of ways.',
         'Representing Data: Scatter Plots, Histograms and Pie Charts', 'Representing Data',
         'Free CAPS Grade 9 worksheets: scatter plots, correlation, lines of best fit, histograms and pie charts. 100 questions with memos.',
         'Positive correlation: both go up.', 'Correlation is not cause.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
