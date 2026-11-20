# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): Probability: Outcomes and Simple Experiments (Grade 5: 5.4 Probability)
  python3 tools/gen_za_maths_g5_probability.py
Possible outcomes, likely and unlikely events, comparing chances, and experiments with coins, dice and spinners
(Australia Year 5, BC Grade 5 and Ontario Grade 5 makers).
Wrong answers come from real mistakes: thinking all outcomes are equally likely, thinking a result is due after a
run of the other result, and expecting an experiment to match the prediction exactly.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y5_chance as auc
adopt(auc)
if isinstance(getattr(auc, 'R', None), random.Random): auc.R = random.Random(805300)
import gen_cabc_math_g5_probability as cbp
adopt(cbp)
if isinstance(getattr(cbp, 'R', None), random.Random): cbp.R = random.Random(805301)
import gen_caon_math_g5_probability as cap
adopt(cap)
if isinstance(getattr(cap, 'R', None), random.Random): cap.R = random.Random(805302)
za_common.GRADE = "grade-5"


import re as _re


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def _nums(it):
    return [int(x.replace(",", "").replace("\u00a0", "")) for x in _re.findall(r"(?<![\d.])\d[\d,\u00a0]*(?![.\d])", _txt(it)) if x.replace(",", "").replace("\u00a0", "").isdigit()]


def six(it):
    """whole numbers to 6 digits, no decimals, no negatives"""
    t = _txt(it)
    return all(n <= 999999 for n in _nums(it)) and not _re.search(r"\d\.\d|−\d", t)


def nodec(it):
    return not _re.search(r"\d\.\d|−\d", _txt(it))


def den12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " " + it["c"][it["a"]])]
    return all(d <= 12 for d in ds) and nodec(it)



def build():
    sets, R = build_sets([
        ("Possible outcomes", [("run", auc.set_outcomes, (), 10, nodec), ("run", cbp.set_outcomes, (), 10, nodec)]),
        ("Likely or unlikely?", [("run", cbp.set_words, (), 10, nodec), ("run", auc.set_real, (), 10, nodec)]),
        ("Compare the chances", [("run", auc.set_compare, (), 10, nodec), ("run", auc.set_equal, (), 10, nodec)]),
        ("Experiments", [("run", auc.set_experiments, (), 10, nodec), ("run", cap.set_experimental, (), 10, nodec)]),
        ("Predict the results", [("run", cbp.set_predict, (), 10, nodec), ("run", cbp.set_fair, (), 10, nodec)]),
    ], 80530)
    finish(sets, R)
    body = lesson('<ul><li>An <b>outcome</b> is a possible result. A coin has 2 outcomes; a dice has 6.</li><li>Use words like impossible, unlikely, even chance, likely and certain.</li><li>In an experiment, record the results with tallies. Do at least 20 trials.</li><li>The results of an experiment are close to the prediction, but not always the same.</li></ul>',
        [example("A spinner: 6 red parts and 2 blue parts", ["6 parts out of 8 are red"], "red is more likely")],
        [['All equally likely', 'Count how many ways each can happen.'], ['It is due', 'A coin has no memory.'], ['Exact match', 'Results vary.']])
    faq = [('What does CAPS Grade 5 say about probability?', 'Perform simple repeated events and list possible outcomes, and count and compare the actual outcomes for experiments with up to 20 trials.'), ('What is a trial?', 'One go of the experiment, like one flip of a coin.'), ('Is getting 6 on a dice likely?', 'No, it is unlikely: 1 out of 6.'), ('Why repeat an experiment?', 'More trials give a better picture.')]
    make('probability', 30, 'Data Handling', 'Grade 5: 5.4 Probability',
         'Perform simple repeated events and list possible outcomes for experiments such as tossing a coin, rolling a die and spinning a spinner; list possible outcomes for experiments; count and compare the frequency of actual outcomes for a series of up to 20 trials.',
         'Probability: Outcomes and Simple Experiments', 'Probability',
         'Free CAPS Grade 5 probability worksheets: outcomes, likely and unlikely events, comparing chances and experiments. 100 questions with memos.',
         'Count the ways each outcome can happen.', 'Experiments vary from the prediction.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
