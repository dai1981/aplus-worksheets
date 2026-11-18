# -*- coding: utf-8 -*-
"""
Texas Grade 6 Math: Mean, Median, Range and IQR; Statistical Questions (TEKS 6.12B, 6.12C, 6.13B)
  python3 tools/gen_ustx_math_g6_mean_median.py
Statistical and non-statistical questions, median, mode and range, the mean, outliers and the IQR, and word problems
(the US Grade 6 makers with Texas names, plus an own statistical question maker).
Wrong answers come from real mistakes: finding the median without ordering, dividing by the wrong count, and
thinking a question with one answer is statistical.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g6_mean_median as mm
adopt(mm)
mm.CC_LIST = mm.Ctx(random.Random(66023), mm.LIST_CTX)
tx_common.GRADE = "grade-6"

STATQ = ["How many hours do students in our class sleep on school nights?", "How tall are the sixth graders at Lamar Middle School?", "How many pets do the families on Pecan Street have?",
         "How long does it take students in Grade 6 to get to school?", "What were the high temperatures in San Antonio each day last month?", "How many texts do my friends send each day?",
         "How much do cars at the dealership cost?", "How many points did the team score in each game this season?"]
NONQ = ["How tall is the flagpole at our school?", "How many students are in Ms. Ruiz's class today?", "What was the high temperature in Dallas yesterday?",
        "How old is my brother?", "How many pages are in this book?", "What time does the school bus leave on Monday?", "How much does this backpack cost?",
        "How far is it from Austin to Houston?", "What is the capital of Texas?", "How many windows are in my bedroom?"]


def one_statq(r):
    if r.random() < 0.6:
        right = r.choice(STATQ)
        return mcq("Which is a <b>statistical question</b>?", right, r.sample(NONQ, 3), "A statistical question expects answers that <b>vary</b>, so you collect many data values. <b>%s</b>" % right)
    right = r.choice(NONQ)
    return mcq("Which is <b>not</b> a statistical question?", right, r.sample(STATQ, 3), "This question has only one answer, so there is no variability in the data. <b>%s</b>" % right)


def build():
    sets, R = build_sets([
        ("Statistical questions", [("collect", one_statq, 20)]),
        ("Median, mode and range", [("run", mm.set_mmr, ("rnd", mm.People, lambda r: mm.Ctx(r, mm.LIST_CTX)), 20)]),
        ("The mean", [("run", mm.set_mean, ("rnd", mm.People, lambda r: mm.Ctx(r, mm.LIST_CTX)), 20)]),
        ("Outliers, spread and the IQR", [("run", mm.set_outlier, ("rnd", mm.People, lambda r: mm.Ctx(r, mm.OUT_CTX)), 20)]),
        ("Word problems", [("run", mm.set_word, ("rnd", mm.People), 20)]),
    ], 66023)
    finish(sets, R)
    body = lesson('<ul><li>A <b>statistical question</b> expects answers that vary: How many hours do students sleep?</li><li><b>Center</b>: the <b>mean</b> (add, then divide by how many) and the <b>median</b> (the middle value in order).</li><li><b>Spread</b>: the <b>range</b> (max − min) and the <b>IQR</b> (Q3 − Q1).</li><li>An <b>outlier</b> pulls the mean toward it but changes the median very little.</li></ul>',
        [example("3, 5, 6, 8, 9, 9, 9", ["Mean: 49 ÷ 7 = 7", "Median: 8", "Range: 9 − 3 = 6"], "mean 7, median 8"), example("Q1 = 5, Q3 = 9", ["IQR = 9 − 5"], "4")],
        [['Finding the median without ordering the data', 'Put the values in order first.'], ['Dividing by the wrong count for the mean', 'Divide by how many values there are.'], ['Calling a one-answer question statistical', 'Statistical questions expect many different answers.']])
    faq = [('What does TEKS 6.12C ask?', 'Summarize numeric data with numerical summaries, including the mean and median (measures of center) and the range and interquartile range (IQR) (measures of spread), and use these summaries to describe the center, spread and shape of the data distribution.'), ('What does TEKS 6.13B ask?', 'Distinguish between situations that yield data with and without variability.'), ('What does TEKS 6.12B ask?', 'Use the graphical representation of numeric data to describe the center, spread and shape of the data distribution.'), ('Mean or median: which is better with an outlier?', 'The median, because an outlier changes it very little.')]
    make('mean-median-range-and-iqr', 23, 'Measurement and Data', '6.12B, 6.12C, 6.13B',
         '6.12B use the graphical representation of numeric data to describe the center, spread, and shape of the data distribution; 6.12C summarize numeric data with numerical summaries, including the mean and median (measures of center) and the range and interquartile range (IQR) (measures of spread), and use these summaries to describe the center, spread, and shape of the data distribution; 6.13B distinguish between situations that yield data with and without variability',
         'Mean, Median, Range and IQR; Statistical Questions', 'Mean, Median, Range and IQR',
         'Free Grade 6 statistics worksheets for Texas TEKS 6.12B, 6.12C and 6.13B: statistical questions, mean, median, mode, range, outliers and IQR, and word problems. 100 questions with answers.',
         'Center: mean and median. Spread: range and IQR.', 'Order the data for the median. An outlier moves the mean more than the median.',
         body, faq, sets, seo_title='Grade 6 Mean, Median, Range and IQR Worksheets (TEKS 6.12C, STAAR)')


if __name__ == "__main__":
    build()
