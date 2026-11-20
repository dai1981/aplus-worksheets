# -*- coding: utf-8 -*-
"""
South Africa Grade 9 Maths (CAPS): Collecting and Summarising Data: Averages, Spread and Grouped Data (Grade 9: 5.1 Collect, organise and summarise data)
  python3 tools/gen_za_maths_g9_data.py
Mean, median, mode and range, missing values, frequency tables, grouped data and stem-and-leaf diagrams (Singapore
Secondary 2 makers).
Wrong answers come from real mistakes: finding the median without ordering, dividing by the number of groups instead
of the total frequency, and ignoring outliers.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_sg_maths_s2_mean_median_and_mode as sgm
adopt(sgm)
if isinstance(getattr(sgm, 'R', None), random.Random): sgm.R = random.Random(809190)
import gen_sg_maths_s2_frequency_tables_and_grouped_data as sgf
adopt(sgf)
if isinstance(getattr(sgf, 'R', None), random.Random): sgf.R = random.Random(809191)
import gen_sg_maths_s2_stem_and_leaf_diagrams as sgs
adopt(sgs)
if isinstance(getattr(sgs, 'R', None), random.Random): sgs.R = random.Random(809192)
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
        ("Mean, median, mode and range", [("collect", sgm.one_mean, 7), ("collect", sgm.one_median, 7), ("collect", sgm.one_mode_range, 6)]),
        ("Missing values and comparing", [("collect", sgm.one_missing, 20)]),
        ("Frequency tables", [("collect", sgf.one_mean, 10), ("collect", sgf.one_mmr, 10)]),
        ("Grouped data", [("collect", sgf.one_grouped, 20)]),
        ("Stem-and-leaf diagrams", [("collect", sgs.one_medmode, 10), ("collect", sgs.one_rangemean, 10)]),
    ], 80919)
    finish(sets, R)
    body = lesson('<ul><li>Mean = total ÷ number of values; median = middle value in order; mode = most common; range = highest − lowest.</li><li>From a frequency table: mean = Σ(value × frequency) ÷ Σfrequency.</li><li>Grouped data: use the modal class and estimate with midpoints.</li><li>An outlier can change the mean a lot but not the median.</li></ul>',
        [example("Marks 4, 6, 7, 7, 30", ["mean 10,8", "median 7"], "the median describes the data better")],
        [['Median without ordering', 'Order first.'], ['Dividing by the groups', 'Divide by the total frequency.'], ['Ignoring outliers', 'They pull the mean.']])
    faq = [('What does CAPS Grade 9 say about data?', 'Summarise data using measures of central tendency and dispersion, including range, extremes and outliers, and organise data in tables, grouped intervals and stem-and-leaf displays.'), ('What is the modal class?', 'The interval with the highest frequency.'), ('Why use midpoints?', 'To estimate the mean of grouped data.'), ('What is an outlier?', 'A value much higher or lower than the rest.')]
    make('collecting-and-summarising-data', 19, 'Data Handling', 'Grade 9: 5.1 Collect, organise and summarise data',
         'Organise numerical data in different ways in order to summarise by determining measures of central tendency (mean, median, mode) and measures of dispersion (range, percentiles, quartiles, interquartile range, extremes and outliers); group data into intervals; organise and record data using stem-and-leaf displays.',
         'Collecting and Summarising Data: Averages, Spread and Grouped Data', 'Collecting and Summarising Data',
         'Free CAPS Grade 9 data handling worksheets: mean, median, mode, range, frequency tables, grouped data and stem-and-leaf diagrams. 100 questions with memos.',
         'Mean from a table: Σ(value × frequency) ÷ Σfrequency.', 'Outliers pull the mean.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
