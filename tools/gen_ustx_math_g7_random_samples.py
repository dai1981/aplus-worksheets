# -*- coding: utf-8 -*-
"""
Texas Grade 7 Math: Random Samples and Inferences (TEKS 7.6F, 7.12B, 7.12C)
  python3 tools/gen_ustx_math_g7_random_samples.py
Populations and samples, random or biased samples, estimating a population from a sample, variation between
samples, and inference word problems (the US Grade 7 makers with a new seed).
Wrong answers come from real mistakes: asking only one group, using the sample count as the population count, and
trusting a single small sample.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g7_random_sampling as rsm
adopt(rsm)
rsm.R = random.Random(670220)
tx_common.GRADE = "grade-7"



def build():
    sets, R = build_sets([
        ("Populations and samples", [("run", rsm.set_words, (), 20)]),
        ("Random or biased?", [("run", rsm.set_bias, (), 20)]),
        ("Estimate a population from a sample", [("run", rsm.set_estimate, (), 20)]),
        ("Variation between samples", [("run", rsm.set_variation, (), 20)]),
        ("Word problems: making inferences", [("run", rsm.set_wordprob, (), 20)]),
    ], 67022)
    finish(sets, R)
    body = lesson('<ul><li>The <b>population</b> is the whole group you want to know about. A <b>sample</b> is part of it.</li><li>A <b>random sample</b> gives every member the same chance of being chosen, so it represents the population.</li><li>A <b>biased</b> sample favors some members, like asking only the soccer team about favorite sports.</li><li>Use a proportion to estimate: 12 of 40 like rock, so about 12/40 × 500 = 150 of 500.</li></ul>',
        [example("12 of 40 sampled students like rock. 500 students in all.", ["12/40 = 0.3", "0.3 × 500"], "about 150")],
        [['Asking only one group', 'A sample must give everyone the same chance.'], ['Using the sample count as the answer', 'Scale up from the sample to the population.'], ['Trusting one small sample', 'Several random samples give a better estimate.']])
    faq = [('What does TEKS 7.12B ask?', 'Use data from a random sample to make inferences about a population.'), ('What does TEKS 7.12C ask?', 'Compare two populations based on data in random samples from these populations, including informal comparative inferences about differences between the two populations.'), ('What does TEKS 7.6F ask?', 'Use data from a random sample to make inferences about a population.'), ('Why use several samples?', 'Samples vary. Looking at several shows how much the estimate can change.')]
    make('random-samples-and-inferences', 22, 'Measurement and Data', '7.6F, 7.12B, 7.12C',
         '7.6F use data from a random sample to make inferences about a population; 7.12B use data from a random sample to make inferences about a population; 7.12C compare two populations based on data in random samples from these populations, including informal comparative inferences about differences between the two populations',
         'Random Samples and Inferences', 'Random Samples and Inferences',
         'Free Grade 7 statistics worksheets for Texas TEKS 7.6F, 7.12B and 7.12C: populations and samples, random or biased samples, estimating populations and making inferences. 100 questions with answers.',
         'A random sample represents the population.', '12 of 40 like rock → about 150 of 500.',
         body, faq, sets, seo_title='Grade 7 Random Samples and Inferences Worksheets (TEKS 7.12B, STAAR)')


if __name__ == "__main__":
    build()
