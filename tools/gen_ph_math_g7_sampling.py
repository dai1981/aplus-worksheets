# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Data Collection and Sampling Techniques (Grade 7: Data and Probability)
  python3 tools/gen_ph_math_g7_sampling.py
Populations and samples, random and biased samples, estimating from a sample, variation between samples and
problems (US Grade 7 makers with Filipino names).
Wrong answers come from real mistakes: surveying only friends, thinking a bigger biased sample is fair, and
forgetting to scale up from the sample.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g7_random_sampling as urs
adopt(urs)
if hasattr(urs, 'R'): urs.R = random.Random(707180)
ph_common.GRADE = "grade-7"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


SAMP = [("prefer adobo for lunch", "learners in the school"), ("walk to school", "learners in the school"), ("have a pet dog", "families in the barangay"),
        ("watch basketball", "residents of the town"), ("use a tablet for study", "Grade 7 learners in the division")]


def one_samp(r):
    t, pop = r.choice(SAMP)
    n = r.choice([20, 25, 40, 50, 80, 100])
    k = r.randint(2, n - 2)
    N = r.choice([400, 500, 800, 1000, 1200, 2000, 5000])
    est = k * N / n
    if est != int(est):
        raise AssertionError
    est = int(est)
    q = "In a random sample of %d %s, %d %s. About how many of the %s %s %s?" % (n, pop, k, t, comma(N), pop, t)
    return mcq(q, "about %s" % comma(est), ["about %s" % comma(x) for x in (k * 10, N - est, est * 2)],
               "%d out of %d is %s of the sample. %s × %s = <b>%s</b>." % (k, n, ("%g%%" % (k * 100 / n)), ("%g%%" % (k * 100 / n)), comma(N), comma(est)))


def build():
    sets, R = build_sets([
        ("Population and sample", [("run", urs.set_words, (), 16), ("collect", uniq(one_samp), 4)]),
        ("Random or biased?", [("run", urs.set_bias, (), 20)]),
        ("Estimate from a sample", [("run", urs.set_estimate, (), 20)]),
        ("Samples vary", [("run", urs.set_variation, (), 20)]),
        ("Sampling problems", [("run", urs.set_wordprob, (), 12), ("collect", uniq(one_samp), 8)]),
    ], 70718)
    finish(sets, R)
    body = lesson("<ul><li>The <b>population</b> is the whole group you want to know about. A <b>sample</b> is the part you actually ask or measure.</li><li>Ways to collect data: survey, interview, observation, experiment, and records.</li><li>A <b>random sample</b> gives everyone the same chance to be chosen, so it represents the population. A <b>biased</b> sample favors some people (only your friends, only one section).</li><li>To estimate, use the sample's rate for the whole population: 12 of 40 sampled → 30% of 800 learners ≈ 240.</li></ul>",
        [example("12 of 40 sampled learners walk to school; 800 learners", ["12 ÷ 40 = 30%", "30% of 800"], "about 240")],
        [['Asking only friends', 'That sample is biased.'], ['A bigger biased sample', 'Size does not fix bias.'], ['Not scaling up', 'Apply the sample rate to the population.']])
    faq = [('What does MATATAG Math 7 ask about sampling?', 'Investigate different data collection and sampling techniques.'), ('What is simple random sampling?', 'Every member has an equal chance, like drawing names from a box.'), ('What is stratified sampling?', 'Taking a random sample from each group, such as each grade level.'), ('Why not ask everyone?', 'It is often too slow or costly; a good sample is enough.')]
    make('data-collection-and-sampling', 18, 'Data and Probability', 'Grade 7: Data and Probability',
         'Investigate different data collection and sampling techniques.',
         'Data Collection and Sampling Techniques', 'Data Collection and Sampling',
         'Free Grade 7 sampling worksheets for the DepEd MATATAG curriculum: populations and samples, random and biased samples, estimates from samples and variation. 100 questions with answers.',
         'A random sample represents the population.', "Use the sample's rate to estimate for the population.",
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
