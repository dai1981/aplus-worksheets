# -*- coding: utf-8 -*-
"""
Texas Grade 8 Math: Mean Absolute Deviation (MAD) (TEKS 8.11B)
  python3 tools/gen_ustx_math_g8_mad.py
Finding the mean and MAD (US Grade 7 maker with a new seed), computing MAD step by step for up to 10 values, comparing
spread with MAD, and word problems (own makers).
Wrong answers come from real mistakes: keeping negative distances, dividing by the wrong count, and thinking a
bigger mean means a bigger MAD.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g7_comparing_data_distributions as cdd
adopt(cdd)
cdd.R = random.Random(680190)
tx_common.GRADE = "grade-8"

from fractions import Fraction as F
from ws_common import num

INK = "#1f2937"


def g(v):
    s = ("%.2f" % v).rstrip("0").rstrip(".")
    if "." in s:
        a, b = s.split(".")
        return ("−" if v < 0 else "") + comma(abs(int(a))) + "." + b
    return num(int(s))


def pt(p):
    return "(%s, %s)" % (g(p[0]), g(p[1]))


def data(r, n=None):
    n = n or r.randint(4, 8)
    for _ in range(80):
        xs = [r.randint(2, 30) for _ in range(n)]
        if sum(xs) % n:
            continue
        mu = sum(xs) // n
        dev = [abs(x - mu) for x in xs]
        if sum(dev) == 0:
            continue
        mad = F(sum(dev), n)
        if mad.denominator in (1, 2, 4, 5):
            return xs, mu, dev, mad
    return None


def one_mad(r):
    d = data(r)
    if not d:
        return None
    xs, mu, dev, mad = d
    return mcq("Find the mean absolute deviation of %s." % ", ".join(map(str, xs)), g(float(mad)),
               [g(float(F(sum(x - mu for x in xs if x > mu), len(xs)))) if F(sum(x - mu for x in xs if x > mu), len(xs)) != mad else g(float(mad) + 1), g(float(F(sum(dev), len(xs) - 1))), g(float(mu))],
               "Mean = %d ÷ %d = %d. Distances: %s. MAD = %d ÷ %d = <b>%s</b>." % (sum(xs), len(xs), mu, ", ".join(map(str, dev)), sum(dev), len(xs), g(float(mad))))


def one_step(r):
    d = data(r, r.randint(4, 6))
    if not d:
        return None
    xs, mu, dev, mad = d
    kind = r.choice(["mean", "sum"])
    if kind == "mean":
        return mcq("What is the first step to find the MAD of %s? Find the mean. What is it?" % ", ".join(map(str, xs)), str(mu), [str(sum(xs)), str(sorted(xs)[len(xs) // 2]), str(max(xs) - min(xs))],
                   "%d ÷ %d = <b>%d</b>." % (sum(xs), len(xs), mu))
    return mcq("The mean of %s is %d. What is the sum of the distances from the mean?" % (", ".join(map(str, xs)), mu), str(sum(dev)), [str(sum(x - mu for x in xs)), str(sum(dev) // 2), str(sum(xs))],
               "Distances: %s. Sum = <b>%d</b>. (Without absolute values the sum would be 0.)" % (", ".join(map(str, dev)), sum(dev)))


def one_compare(r):
    a, b = data(r, 5), data(r, 5)
    if not a or not b or a[3] == b[3]:
        return None
    na, nb = r.sample(["Class A", "Class B", "Team Red", "Team Blue"], 2)
    more = na if a[3] > b[3] else nb
    return mcq("%s: %s. %s: %s. Which data set is more spread out from its mean?" % (na, ", ".join(map(str, a[0])), nb, ", ".join(map(str, b[0]))), "%s (MAD %s)" % (more, g(float(max(a[3], b[3])))),
               ["%s (MAD %s)" % (nb if more == na else na, g(float(min(a[3], b[3])))), "They are the same", "%s (mean %d)" % (na if a[1] > b[1] else nb, max(a[1], b[1]))],
               "MAD of %s = %s; MAD of %s = %s. The greater MAD is <b>%s</b>." % (na, g(float(a[3])), nb, g(float(b[3])), more))


def build():
    sets, R = build_sets([
        ("Mean and MAD", [("run", cdd.set_mad, (), 20)]),
        ("Step by step", [("collect", one_step, 20)]),
        ("Find the MAD", [("collect", one_mad, 20)]),
        ("Compare spread with MAD", [("collect", one_compare, 20)]),
        ("Word problems", [("run", cdd.set_words, (), 20)]),
    ], 68019)
    finish(sets, R)
    body = lesson("<ul><li>The <b>mean absolute deviation (MAD)</b> is the average distance of the data from the mean.</li><li>Step 1: find the mean. Step 2: find each value's distance from the mean (always positive). Step 3: average the distances.</li><li>A small MAD means the data are close to the mean; a large MAD means they are spread out.</li></ul>",
        [example("3, 5, 7, 9", ["Mean = 6", "Distances 3, 1, 1, 3", "8 ÷ 4"], "MAD = 2")],
        [['Keeping negative distances', 'Distances are absolute values; without them the sum is 0.'], ['Dividing by the wrong count', 'Divide by the number of values.'], ['Thinking a bigger mean means a bigger MAD', 'MAD measures spread, not size.']])
    faq = [('What does TEKS 8.11B ask?', 'Determine the mean absolute deviation and use this quantity as a measure of the average distance data are from the mean using a data set of no more than 10 data points.'), ('Can the MAD be 0?', 'Yes, when every value equals the mean.'), ('Is MAD the same as range?', 'No. Range uses only the max and min; MAD uses every value.'), ('Why use absolute values?', 'Distances above and below the mean would cancel out otherwise.')]
    make('mean-absolute-deviation', 19, 'Measurement and Data', '8.11B',
         '8.11B determine the mean absolute deviation and use this quantity as a measure of the average distance data are from the mean using a data set of no more than 10 data points',
         'Mean Absolute Deviation (MAD)', 'Mean Absolute Deviation',
         'Free Grade 8 mean absolute deviation worksheets for Texas TEKS 8.11B: find the mean and MAD step by step, compare spread and word problems. 100 questions with answers.',
         'MAD = average distance from the mean.', '3, 5, 7, 9: mean 6, distances 3, 1, 1, 3, MAD = 2.',
         body, faq, sets, seo_title='Grade 8 Mean Absolute Deviation (MAD) Worksheets (TEKS 8.11B, STAAR)')


if __name__ == "__main__":
    build()
