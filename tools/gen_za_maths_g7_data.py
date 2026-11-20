# -*- coding: utf-8 -*-
"""
South Africa Grade 7 Maths (CAPS): Collecting and Summarising Data: Mean, Median, Mode and Range (Grade 7: 5.1 Collect, organise and summarise data)
  python3 tools/gen_za_maths_g7_data.py
The mean, median, mode and range, finding a missing value, comparing data sets, and stem-and-leaf displays (UK Year 7
and Australia Year 7 makers).
Wrong answers come from real mistakes: finding the median without ordering, dividing by the wrong number for the
mean, and giving the biggest value as the range.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y7_averages_and_range as uka
adopt(uka)
if isinstance(getattr(uka, 'R', None), random.Random): uka.R = random.Random(807240)
import gen_au_maths_y7_mean_median_mode_and_range as aum
adopt(aum)
if isinstance(getattr(aum, 'R', None), random.Random): aum.R = random.Random(807241)
import gen_au_maths_y7_stem_and_leaf_plots as aus
adopt(aus)
if isinstance(getattr(aus, 'R', None), random.Random): aus.R = random.Random(807242)
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
        ("Mean", [("collect", uka.one_mean, 10), ("collect", aum.one_mean, 10)]),
        ("Median", [("collect", uka.one_median, 10), ("collect", aum.one_median, 10)]),
        ("Mode and range", [("collect", uka.one_mode_range, 10), ("collect", aum.one_mode_range, 10)]),
        ("Stem-and-leaf displays", [("collect", aus.one_read, 10), ("collect", aus.one_medmode, 10)]),
        ("Missing values", [("collect", uka.one_missing, 10), ("collect", aum.one_missing, 10)]),
    ], 80724)
    finish(sets, R)
    body = lesson('<ul><li><b>Mean</b> = total ÷ number of values.</li><li><b>Median</b> = the middle value when the data is in order.</li><li><b>Mode</b> = the value that appears most often. <b>Range</b> = highest − lowest.</li><li>In a stem-and-leaf display, 4 | 7 means 47.</li></ul>',
        [example("Marks: 12, 15, 9, 15, 14", ["total 65, 5 values", "in order: 9, 12, 14, 15, 15"], "mean 13, median 14, mode 15, range 6")],
        [['Median without ordering', 'Put the data in order first.'], ['Wrong number of values', 'Count every value.'], ['Range = biggest', 'Range = biggest − smallest.']])
    faq = [('What does CAPS Grade 7 say about summarising data?', 'Summarise data using the mean, median and mode, and describe the spread with the range; organise data in tables and stem-and-leaf displays.'), ('Which average is best with an outlier?', 'The median.'), ('Can the mean be a decimal?', 'Yes.'), ('What is an outlier?', 'A value far from the others.')]
    make('collecting-and-summarising-data', 24, 'Data Handling', 'Grade 7: 5.1 Collect, organise and summarise data',
         'Organise numerical data in different ways in order to summarise by determining measures of central tendency (mean, median, mode) and measures of dispersion (range); organise and record data using tally marks, tables and stem-and-leaf displays.',
         'Collecting and Summarising Data: Mean, Median, Mode and Range', 'Collecting and Summarising Data',
         'Free CAPS Grade 7 data handling worksheets: mean, median, mode, range, stem-and-leaf displays and comparing data. 100 questions with memos.',
         'Mean: total ÷ count. Median: the middle.', 'Order the data first.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
