# -*- coding: utf-8 -*-
"""
India Class 8 Maths, Ganita Prakash Part 2, Chapter 5: Tales by Dots and Lines
  python3 tools/gen_in_maths_c8_tales_by_dots_and_lines.py
Data handling: mean and median of a list, a missing value from the mean, frequency tables (mean, mode, range), grouped
data, reading bar graphs and histograms, and pie-chart angles. The bar graphs and histograms reuse the Class 9 makers.
Wrong answers come from real mistakes: the median taken before ordering, dividing by the number of rows instead of the
total frequency, and reading the wrong grid line.
"""
import random
from in_common import unit, adopt, gb
import gen_au_maths_y7_mean_median_mode_and_range as mm
import gen_uk_maths_y8_frequency_tables_and_charts as ft
import gen_in_maths_c9_statistics as st

R = random.Random(908012)


def c8(fn):
    def f(r):
        it = fn(r)
        if it:
            it["q"] = it["q"].replace("Class 9", "Class 8").replace("class 9", "class 8")
        return it
    f.__name__ = fn.__name__
    return f
adopt(mm, R)
adopt(ft, R)


def main():
    unit(8, 2, 5, "tales-by-dots-and-lines", 12, "D", "Tales by Dots and Lines: Mean, Median and Graphs", "tales by dots and lines",
         "Collecting and organising data, mean and median, frequency tables, grouped data, bar graphs, histograms and pie charts (summary of NCERT Ganita Prakash Class 8)",
         "Class 8 Tales by Dots and Lines worksheet (Ganita Prakash Part 2, Chapter 5): mean, median, frequency tables, bar graphs, histograms and pie charts. 100 questions with answers.",
         "Mean = total ÷ number of values", "Median = the middle value after ordering.",
         "<p>The <b>mean</b> is the total divided by the number of values. The <b>median</b> is the middle value once the data are in order (the mean of the two middle values if there is an even number).</p>"
         "<p>In a <b>frequency table</b>, the total is Σ(value × frequency) and the number of values is the total frequency.</p>"
         "<p>A <b>histogram</b> shows grouped data; a <b>pie chart</b> uses 360° for the whole, so each item gets frequency ÷ total × 360°.</p>",
         [("Find the mean and median of 4, 9, 6, 3, 8.", ["Total 30 ÷ 5 = 6", "Ordered: 3, 4, 6, 8, 9"], "Mean 6, median 6"),
          ("In a survey of 60 people, 15 chose tea. What angle is tea on a pie chart?", ["15 ÷ 60 × 360°"], "90°")],
         ["Finding the median without putting the data in order.", "Dividing by the number of rows in a frequency table instead of the total frequency.", "Using 100 instead of 360° for a pie chart."],
         [("What is the difference between mean and median?", "The mean shares the total equally; the median is the middle value in order. One very large value changes the mean much more than the median."),
          ("How do you find the mean from a frequency table?", "Multiply each value by its frequency, add these, and divide by the total frequency."),
          ("How do you find an angle in a pie chart?", "Frequency ÷ total × 360°.")],
         [("Mean and median", [(gb(mm.one_mean), 10), (gb(mm.one_median), 10)]),
          ("Missing values and comparing data", [(gb(mm.one_missing), 10), (gb(mm.one_compare), 10)]),
          ("Frequency tables", [(gb(ft.one_mean), 8), (gb(ft.one_mmr), 8), (gb(ft.one_grouped), 4)]),
          ("Bar graphs and histograms", [(c8(st.one_bar), 10), (st.one_hist, 10)]),
          ("Pie charts and data problems", [(gb(ft.one_pie), 10), (st.K(st.one_prob, "pct"), 5), (st.K(st.one_prob, "between"), 5)])], R)


if __name__ == "__main__":
    main()
