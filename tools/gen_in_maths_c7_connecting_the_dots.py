# -*- coding: utf-8 -*-
"""
India Class 7 Maths, Ganita Prakash Part 2, Chapter 5: Connecting the Dots
  python3 tools/gen_in_maths_c7_connecting_the_dots.py
Summarising data: the mean (average) and median, mode and range, a missing value from a mean, comparing two sets of data,
and reading bar graphs. Reuses the AU Year 7 makers and the Class 9 bar-graph maker.
Wrong answers come from real mistakes: the median taken before ordering, dividing by the wrong count, and the range taken
as the largest value.
"""
import random
from in_common import unit, adopt, gb
import gen_au_maths_y7_mean_median_mode_and_range as mm
import gen_in_maths_c9_statistics as st

R = random.Random(907013)
adopt(mm, R)


def c7(fn):
    def f(r):
        it = fn(r)
        if it:
            it["q"] = it["q"].replace("Class 9", "Class 7").replace("class 9", "class 7")
        return it
    f.__name__ = fn.__name__
    return f


def main():
    unit(7, 2, 5, "connecting-the-dots", 13, "D", "Connecting the Dots: Mean, Median and Data", "connecting the dots",
         "Representative values of data: mean (average), median, mode and range; comparing data sets; reading bar graphs (summary of NCERT Ganita Prakash Class 7)",
         "Class 7 Connecting the Dots worksheet (Ganita Prakash Part 2, Chapter 5): mean, median, mode, range, missing values and bar graphs. 100 questions with answers.",
         "Mean = sum ÷ count; median = middle value", "Put the data in order before finding the median.",
         "<p>The <b>mean</b> (average) shares the total equally: add all the values and divide by how many there are.</p>"
         "<p>The <b>median</b> is the middle value when the data are in order; with an even count, it is halfway between the two middle values. The <b>mode</b> is the most common value; the <b>range</b> is largest − smallest.</p>",
         [("Find the mean of 12, 15, 9, 20, 14.", ["Sum 70", "70 ÷ 5"], "14"),
          ("Find the median of 7, 3, 9, 5, 11, 2.", ["Order: 2, 3, 5, 7, 9, 11", "(5 + 7) ÷ 2"], "6")],
         ["Finding the median without ordering the data.", "Dividing by the wrong number of values.", "Giving the largest value as the range."],
         [("What is the mean?", "The sum of all values divided by the number of values."),
          ("What is the median?", "The middle value when the data are arranged in order."),
          ("When is the median better than the mean?", "When one or two values are very large or very small, because the median is not pulled by them.")],
         [("The mean", [(gb(mm.one_mean), 20)]),
          ("The median", [(gb(mm.one_median), 20)]),
          ("Mode and range", [(gb(mm.one_mode_range), 20)]),
          ("Missing values and comparing", [(gb(mm.one_missing), 10), (gb(mm.one_compare), 10)]),
          ("Reading bar graphs", [(c7(st.one_bar), 20)])], R)


if __name__ == "__main__":
    main()
