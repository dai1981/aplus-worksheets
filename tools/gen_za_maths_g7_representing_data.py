# -*- coding: utf-8 -*-
"""
South Africa Grade 7 Maths (CAPS): Representing Data: Bar Graphs, Histograms and Pie Charts (Grade 7: 5.2 Represent and interpret data)
  python3 tools/gen_za_maths_g7_representing_data.py
Reading bar graphs and grouped frequency tables, histograms, and pie charts with degrees and amounts (UK Year 8, BC
Grade 7 and Ontario Grade 7 makers).
Wrong answers come from real mistakes: reading the scale wrongly, treating a group as a single value, and using 100
instead of 360 for the degrees of a pie chart.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y8_frequency_tables_and_charts as ukf
adopt(ukf)
if isinstance(getattr(ukf, 'R', None), random.Random): ukf.R = random.Random(807250)
import gen_cabc_math_g7_circle_graphs as cbc
adopt(cbc)
if isinstance(getattr(cbc, 'R', None), random.Random): cbc.R = random.Random(807251)
import gen_caon_math_g7_data as cad
adopt(cad)
if isinstance(getattr(cad, 'R', None), random.Random): cad.R = random.Random(807252)
za_common.GRADE = "grade-7"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok7(it):
    """Grade 7: no circles, pi or standard form (they come in Grade 8 and 9)"""
    return not _re.search(r"π|\bpi\b|circumference|radius|diameter|×\s?10<sup>|standard form|scientific notation", _txt(it))


def noneg(it):
    return ok7(it) and not _re.search(r"(?<![\d)] )[−-]\d", _txt(it))



def build():
    sets, R = build_sets([
        ("Read graphs", [("run", cad.set_read, (), 13, ok7), ("run", cbc.set_problems, (), 7, ok7)]),
        ("Grouped data and histograms", [("collect", ukf.one_grouped, 20)]),
        ("Pie charts: reading", [("run", cbc.set_read, (), 10, ok7), ("run", cbc.set_amounts, (), 10, ok7)]),
        ("Pie charts: degrees", [("run", cbc.set_degrees, (), 10, ok7), ("collect", ukf.one_pie, 10)]),
        ("Choose and interpret graphs", [("run", cad.set_choose, (), 10, ok7), ("run", cad.set_claims, (), 10, ok7)]),
    ], 80725)
    finish(sets, R)
    body = lesson('<ul><li>A bar graph compares categories; a histogram shows grouped numerical data with bars that touch.</li><li>In a pie chart, the whole circle is 360°. A sector of 90° is a quarter of the data.</li><li>Sector angle = fraction of the data × 360°.</li><li>Choose a graph that suits the data and the question.</li></ul>',
        [example("12 of 40 learners chose soccer", ["12/40 × 360°"], "108°")],
        [['Reading the scale', 'Check what each line is worth.'], ['A group as one value', 'A group like 10–19 has many values.'], ['100 for a pie chart', 'Use 360°.']])
    faq = [('What does CAPS Grade 7 say about representing data?', 'Draw and interpret bar graphs, double bar graphs, histograms with given and own intervals, and pie charts.'), ('What is the difference between a bar graph and a histogram?', 'A histogram groups numbers into intervals and its bars touch.'), ('How many degrees is half a pie chart?', '180°.'), ('When is a pie chart best?', 'When you compare parts of a whole.')]
    make('bar-graphs-histograms-and-pie-charts', 25, 'Data Handling', 'Grade 7: 5.2 Represent and interpret data',
         'Draw a variety of graphs by hand or technology to display and interpret data, including bar graphs and double bar graphs, histograms with given and own intervals, and pie charts; critically read and interpret data represented in words, bar graphs, double bar graphs, pie charts and histograms.',
         'Representing Data: Bar Graphs, Histograms and Pie Charts', 'Representing Data',
         'Free CAPS Grade 7 worksheets: bar graphs, grouped data, histograms and pie charts with degrees. 100 questions with memos.',
         'Pie chart: fraction × 360°.', 'Histogram bars touch.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
