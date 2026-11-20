# -*- coding: utf-8 -*-
"""
South Africa Grade 4 Maths (CAPS): Probability: Outcomes of Simple Experiments (Grade 4: 5.4 Probability)
  python3 tools/gen_za_maths_g4_probability.py
Listing possible outcomes of tossing a coin, rolling a die and spinning a spinner, likelihood in words, counting the
results of repeated experiments (Australia Year 4 and Year 3 makers and BC Grade 4 makers).
Wrong answers come from real mistakes: missing outcomes, thinking a bigger number on a die is less likely, and
expecting an experiment to give exactly the same results every time.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y4_chance as auc
adopt(auc)
if hasattr(auc, 'R'): auc.R = random.Random(804290)
import gen_au_maths_y3_chance as au3
adopt(au3)
if hasattr(au3, 'R'): au3.R = random.Random(804291)
import gen_cabc_math_g4_probability as cbp
adopt(cbp)
if hasattr(cbp, 'R'): cbp.R = random.Random(804292)
za_common.GRADE = "grade-4"



def build():
    sets, R = build_sets([
        ("Possible outcomes", [("run", auc.set_outcomes, ("rnd",), 10), ("run", au3.set_outcomes, ("rnd",), 10)]),
        ("Likely or unlikely?", [("run", auc.set_words, ("rnd",), 10), ("run", au3.set_everyday, ("rnd",), 10)]),
        ("Spinners and bags", [("run", au3.set_spinners, ("rnd",), 10), ("run", au3.set_bags, ("rnd",), 10)]),
        ("Repeated experiments", [("run", auc.set_experiments, ("rnd",), 10), ("run", cbp.set_trials, ("rnd",), 10)]),
        ("Predict the results", [("run", cbp.set_predict, ("rnd",), 10), ("run", au3.set_experiments, ("rnd",), 10)]),
    ], 80429)
    finish(sets, R)
    body = lesson('<ul><li>An <b>outcome</b> is a possible result. Tossing a coin has 2 outcomes: heads or tails. Rolling a die has 6: 1, 2, 3, 4, 5, 6.</li><li>Describe how likely an event is: impossible, unlikely, even chance, likely, certain.</li><li>Do an experiment many times and count the results in a tally table.</li><li>Results change from one experiment to the next, but more trials give a better picture.</li></ul>',
        [example("Toss a coin 20 times: 11 heads", ["20 − 11"], "9 tails")],
        [['Missing outcomes', 'List them all in order.'], ['6 is harder to roll', 'Each number on a fair die is equally likely.'], ['Same results every time', 'Chance gives different results.']])
    faq = [('What does CAPS Grade 4 say about probability?', 'Perform simple repeated events and list possible outcomes, such as tossing a coin or rolling a die, and count and compare the frequency of actual outcomes.'), ('What is an outcome?', 'A possible result of an experiment.'), ('Is getting heads more likely after many tails?', 'No. Each toss is a new chance.'), ('Why repeat an experiment?', 'More trials show the pattern better.')]
    make('probability', 29, 'Data Handling', 'Grade 4: 5.4 Probability',
         'Perform simple repeated events and list possible outcomes for experiments such as tossing a coin or rolling a die; count and compare the frequency of actual outcomes for a series of trials.',
         'Probability: Outcomes of Simple Experiments', 'Probability',
         'Free CAPS Grade 4 probability worksheets: possible outcomes of coins, dice and spinners, likelihood words and repeated experiments. 100 questions with memos.',
         'Outcomes are all the possible results.', 'Each face of a fair die is equally likely.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
