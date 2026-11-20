# -*- coding: utf-8 -*-
"""
South Africa Grade 8 Maths (CAPS): Collecting and Summarising Data: Samples, Averages and Spread (Grade 8: 5.1 Collect, organise and summarise data)
  python3 tools/gen_za_maths_g8_data.py
Samples and populations, the mean, median, mode and range, grouped data, and comparing data (UK Year 7 and Year 8
and Australia Year 7 and Year 8 makers).
Wrong answers come from real mistakes: finding the median without ordering, dividing by the wrong number, and
choosing a biased sample.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y8_sampling_and_data as aus
adopt(aus)
if isinstance(getattr(aus, 'R', None), random.Random): aus.R = random.Random(808210)
import gen_uk_maths_y8_frequency_tables_and_charts as ukf
adopt(ukf)
if isinstance(getattr(ukf, 'R', None), random.Random): ukf.R = random.Random(808211)
import gen_uk_maths_y7_averages_and_range as uka
adopt(uka)
if isinstance(getattr(uka, 'R', None), random.Random): uka.R = random.Random(808212)
import gen_au_maths_y7_stem_and_leaf_plots as aul
adopt(aul)
if isinstance(getattr(aul, 'R', None), random.Random): aul.R = random.Random(808213)
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
        ("Samples", [("collect", aus.one_est, 10), ("collect", aus.one_stat, 10)]),
        ("Mean, median and mode", [("collect", ukf.one_mmr, 10), ("collect", uka.one_mean, 10)]),
        ("Frequency tables", [("collect", ukf.one_mean, 20)]),
        ("Grouped data", [("collect", ukf.one_grouped, 20)]),
        ("Stem-and-leaf and missing values", [("collect", aul.one_rangemean, 10), ("collect", uka.one_missing, 10)]),
    ], 80821)
    finish(sets, R)
    body = lesson('<ul><li>A <b>sample</b> is part of a population. A good sample is random and large enough.</li><li>Mean = total ÷ number of values. Median = middle value in order. Mode = most common.</li><li>Range = highest − lowest.</li><li>From a frequency table: mean = sum of (value × frequency) ÷ total frequency.</li></ul>',
        [example("Scores 1, 2, 3 with frequencies 4, 5, 1", ["(4 + 10 + 3) ÷ 10"], "mean 1,7")],
        [['Median without ordering', 'Order the data first.'], ['Dividing by the wrong number', 'Divide by the total frequency.'], ['A biased sample', 'Choose people at random.']])
    faq = [('What does CAPS Grade 8 say about data?', 'Pose questions, select samples, organise data in tables and stem-and-leaf displays, and summarise data with the mean, median, mode and range.'), ('What is a population?', 'The whole group you want to know about.'), ('Which average is best with outliers?', 'The median.'), ('What is grouped data?', 'Data put into intervals like 10–19.')]
    make('collecting-and-summarising-data', 21, 'Data Handling', 'Grade 8: 5.1 Collect, organise and summarise data',
         'Distinguish between samples and populations and suggest appropriate samples for investigation; organise numerical data in different ways in order to summarise by determining measures of central tendency (mean, median, mode) and measures of dispersion (range, extremes, outliers).',
         'Collecting and Summarising Data: Samples, Averages and Spread', 'Collecting and Summarising Data',
         'Free CAPS Grade 8 data handling worksheets: samples, mean, median, mode, range, frequency tables and grouped data. 100 questions with memos.',
         'Mean from a table: Σ(value × frequency) ÷ total.', 'Order the data for the median.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
