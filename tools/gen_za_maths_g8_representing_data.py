# -*- coding: utf-8 -*-
"""
South Africa Grade 8 Maths (CAPS): Representing Data: Histograms, Pie Charts and Broken-Line Graphs (Grade 8: 5.2 Represent and interpret data)
  python3 tools/gen_za_maths_g8_representing_data.py
Pie charts with degrees and amounts, grouped data and histograms, line graphs, and choosing and interpreting graphs
(UK Year 8, BC Grade 7 and Grade 6, and Ontario Grade 7 makers).
Wrong answers come from real mistakes: using 100 instead of 360 for a pie chart, reading the scale wrongly, and
drawing conclusions the data does not support.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y8_frequency_tables_and_charts as ukf
adopt(ukf)
if isinstance(getattr(ukf, 'R', None), random.Random): ukf.R = random.Random(808220)
import gen_cabc_math_g7_circle_graphs as cbc
adopt(cbc)
if isinstance(getattr(cbc, 'R', None), random.Random): cbc.R = random.Random(808221)
import gen_cabc_math_g6_line_graphs as cbl
adopt(cbl)
if isinstance(getattr(cbl, 'R', None), random.Random): cbl.R = random.Random(808222)
import gen_caon_math_g7_data as cad
adopt(cad)
if isinstance(getattr(cad, 'R', None), random.Random): cad.R = random.Random(808223)
za_common.GRADE = "grade-8"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok8(it):
    """Grade 8: no trigonometry, quadratic formula or surds beyond square roots"""
    return not _re.search(r"\b(sin|cos|tan)\b|quadratic|discriminant|imperial|\bmiles?\b", _txt(it))



def build():
    sets, R = build_sets([
        ("Pie charts", [("collect", ukf.one_pie, 10), ("run", cbc.set_degrees, (), 10, ok8)]),
        ("Pie chart amounts", [("run", cbc.set_amounts, (), 10, ok8), ("run", cbc.set_make, (), 9, ok8), ("run", cbc.set_read, (), 1, ok8)]),
        ("Histograms", [("collect", ukf.one_grouped, 20)]),
        ("Broken-line graphs", [("run", cbl.set_between, (), 10, ok8), ("run", cbl.set_choose, (), 10, ok8)]),
        ("Interpret the data", [("run", cad.set_change, (), 10, ok8), ("run", cad.set_claims, (), 10, ok8)]),
    ], 80822)
    finish(sets, R)
    body = lesson('<ul><li>Pie chart: sector angle = fraction × 360°.</li><li>A histogram shows grouped numerical data; the bars touch.</li><li>A broken-line graph shows change over time.</li><li>Check that a conclusion is really supported by the data.</li></ul>',
        [example("45 of 120 learners walk to school", ["45/120 × 360°"], "135°")],
        [['100 for a pie chart', 'Use 360°.'], ['Reading the scale', 'Check what each line is worth.'], ['Unsupported claims', 'Only say what the data shows.']])
    faq = [('What does CAPS Grade 8 say about representing data?', 'Draw and interpret bar graphs, double bar graphs, histograms, pie charts and broken-line graphs.'), ('When is a line graph best?', 'For change over time.'), ('What is 90° in a pie chart?', 'A quarter of the data.'), ('Can a graph mislead?', 'Yes, for example with a scale that does not start at 0.')]
    make('histograms-pie-charts-and-line-graphs', 22, 'Data Handling', 'Grade 8: 5.2 Represent and interpret data',
         'Draw a variety of graphs by hand or technology to display and interpret data, including bar graphs and double bar graphs, histograms with given and own intervals, pie charts and broken-line graphs; critically read and interpret data represented in a variety of ways.',
         'Representing Data: Histograms, Pie Charts and Broken-Line Graphs', 'Representing Data',
         'Free CAPS Grade 8 worksheets: pie charts, histograms, broken-line graphs and interpreting data. 100 questions with memos.',
         'Pie chart: fraction × 360°.', 'Only claim what the data shows.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
