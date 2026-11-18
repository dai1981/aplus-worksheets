# -*- coding: utf-8 -*-
"""
Texas Grade 8 Math: Scatterplots, Association and Trend Lines (TEKS 8.5C, 8.5D, 8.11A)
  python3 tools/gen_ustx_math_g8_scatterplots.py
Describing association, judging trend lines, outliers and clusters, predicting with a trend line, and reasoning
with scatterplots (the US Grade 8 makers with a new seed).
Wrong answers come from real mistakes: calling a curve linear, choosing a line that misses most points, and
predicting far outside the data.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g8_scatter_plots as sp
adopt(sp)
sp.R = random.Random(680100)
tx_common.GRADE = "grade-8"



def build():
    sets, R = build_sets([
        ("Describe the association", [("run", sp.set_assoc, (), 20)]),
        ("Good and poor trend lines", [("run", sp.set_judge, (), 20)]),
        ("Outliers, clusters and fit", [("run", sp.set_outliers, (), 20)]),
        ("Predict with a trend line", [("run", sp.set_predict, (), 20)]),
        ("Reasoning with scatterplots", [("run", sp.set_reason, (), 20)]),
    ], 68010)
    finish(sets, R)
    body = lesson('<ul><li>A <b>scatterplot</b> shows pairs of data as points.</li><li><b>Positive</b> association: as x increases, y tends to increase. <b>Negative</b>: y tends to decrease. <b>None</b>: no pattern.</li><li>Points near a straight line show a <b>linear</b> association; a curve shows a nonlinear one.</li><li>A <b>trend line</b> passes close to most points with about as many above as below. Use its equation to predict.</li></ul>',
        [example("Trend line y = 5x + 60. Predict for x = 6.", ["5 × 6 + 60"], "90")],
        [['Calling a curved pattern linear', 'Linear means the points lie near a straight line.'], ['Choosing a line through only two points', 'A trend line follows all the points.'], ['Predicting far outside the data', 'Predictions are less reliable outside the data range.']])
    faq = [('What does TEKS 8.5C ask?', 'Contrast bivariate sets of data that suggest a linear relationship with bivariate sets of data that do not suggest a linear relationship from a graphical representation.'), ('What does TEKS 8.5D ask?', 'Use a trend line that approximates the linear relationship between bivariate sets of data to make predictions.'), ('What does TEKS 8.11A ask?', 'Construct a scatterplot and describe the observed data to address questions of association such as linear, non-linear and no association.'), ('Does association mean one thing causes the other?', 'No. Two things can be related without one causing the other.')]
    make('scatterplots-and-trend-lines', 10, 'Proportionality', '8.5C, 8.5D, 8.11A',
         '8.5C contrast bivariate sets of data that suggest a linear relationship with bivariate sets of data that do not suggest a linear relationship from a graphical representation; 8.5D use a trend line that approximates the linear relationship between bivariate sets of data to make predictions; 8.11A construct a scatterplot and describe the observed data to address questions of association such as linear, non-linear, and no association',
         'Scatterplots, Association and Trend Lines', 'Scatterplots and Trend Lines',
         'Free Grade 8 scatterplot worksheets for Texas TEKS 8.5C, 8.5D and 8.11A: association, linear and nonlinear patterns, trend lines, outliers and predictions. 100 questions with answers.',
         'Positive, negative or no association; linear or nonlinear.', "Use the trend line's equation to predict.",
         body, faq, sets, seo_title='Grade 8 Scatterplots and Trend Lines Worksheets (TEKS 8.5D, 8.11A, STAAR)')


if __name__ == "__main__":
    build()
