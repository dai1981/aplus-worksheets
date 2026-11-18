# -*- coding: utf-8 -*-
"""
Texas Grade 8 Math: Random Samples and Simulations (TEKS 8.11C)
  python3 tools/gen_ustx_math_g8_random_samples.py
Populations and samples, random or biased, simulating samples from a population with known characteristics (own),
variation between samples, and estimating with samples (US Grade 7 makers with a new seed).
Wrong answers come from real mistakes: expecting every sample to match the population exactly, trusting a biased
sample, and scaling with the wrong total.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g7_random_sampling as rsm
adopt(rsm)
rsm.R = random.Random(680200)
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


def one_sim(r):
    pct = r.choice([20, 25, 30, 40, 50, 60, 75])
    n = r.choice([20, 40, 50, 60, 80, 100])
    e = n * pct // 100
    if n * pct % 100:
        return None
    thing = r.choice([("students in the school ride the bus", "ride the bus"), ("marbles in a huge jar are red", "are red"), ("voters in a county support a new park", "support the park"), ("seeds in a big bag are sunflower seeds", "are sunflower seeds")])
    kind = r.choice(["expect", "close", "many"])
    if kind == "expect":
        return mcq("%d%% of the %s. A computer picks random samples of %d. About how many in each sample should %s?" % (pct, thing[0], n, thing[1]), str(e), [str(pct), str(n - e), str(e * 2) if e * 2 <= n else str(e // 2)],
                   "%d%% of %d = <b>%d</b>. Each sample will be close to this, but not always exact." % (pct, n, e))
    if kind == "close":
        good = e + r.choice([-1, 1, 2, -2])
        bad = [e + n // 3, max(0, e - n // 3), n]
        return mcq("%d%% of the %s. In a simulation, which result for a random sample of %d is most likely?" % (pct, thing[0], n), "%d %s" % (good, thing[1]), ["%d %s" % (b, thing[1]) for b in bad],
                   "Random samples tend to be close to %d%% of %d = %d, so <b>%d</b> is most likely." % (pct, n, e, good), allow_zero=True)
    return mcq("Ten random samples of %d are taken from a population where %d%% of the %s. What is true about the results?" % (n, pct, thing[0]), "Most samples are near %d, but they vary" % e,
               ["Every sample is exactly %d" % e, "The samples have no pattern", "Every sample is %d" % n], "Random samples are representative, so they cluster near <b>%d</b>, with some variation." % e)


def build():
    sets, R = build_sets([
        ("Populations and samples", [("run", rsm.set_words, (), 20)]),
        ("Random or biased?", [("run", rsm.set_bias, (), 20)]),
        ("Simulate random samples", [("collect", one_sim, 20)]),
        ("Variation between samples", [("run", rsm.set_variation, (), 20)]),
        ("Estimate with samples", [("run", rsm.set_estimate, (), 20)]),
    ], 68020)
    finish(sets, R)
    body = lesson('<ul><li>A <b>random sample</b> gives every member of the population the same chance to be chosen, so it tends to <b>represent</b> the population.</li><li>In a simulation, random samples from a population with 30% red marbles will usually be about 30% red.</li><li>Samples <b>vary</b>: results cluster around the population value but are not all equal.</li><li>Larger samples usually vary less.</li></ul>',
        [example("40% of a population; samples of 50", ["0.4 × 50"], "about 20 per sample")],
        [['Expecting every sample to match exactly', 'Samples vary around the population value.'], ['Trusting a biased sample', 'A sample from one group may not represent everyone.'], ['Scaling with the wrong total', 'Use the population size when you scale up.']])
    faq = [('What does TEKS 8.11C ask?', 'Simulate generating random samples of the same size from a population with known characteristics to develop the notion of a random sample being representative of the population from which it was selected.'), ('Why do samples vary?', 'Each random sample includes different members by chance.'), ('Do bigger samples help?', 'Yes. Larger random samples are usually closer to the population value.'), ('What is a simulation?', 'A model of the situation, such as a computer picking random numbers.')]
    make('random-samples-and-simulations', 20, 'Measurement and Data', '8.11C',
         '8.11C simulate generating random samples of the same size from a population with known characteristics to develop the notion of a random sample being representative of the population from which it was selected',
         'Random Samples and Simulations', 'Random Samples and Simulations',
         'Free Grade 8 worksheets for Texas TEKS 8.11C: populations and samples, random or biased samples, simulations, sample variation and estimating with samples. 100 questions with answers.',
         'Random samples tend to represent the population.', '40% of a population → samples of 50 have about 20.',
         body, faq, sets, seo_title='Grade 8 Random Samples and Simulations Worksheets (TEKS 8.11C, STAAR)')


if __name__ == "__main__":
    build()
