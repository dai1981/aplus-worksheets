# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Probability: Outcomes, Chance and Experiments (Grade 6: 5.4 Probability)
  python3 tools/gen_za_maths_g6_probability.py
The probability scale, possible outcomes, probability as a fraction, experiments and fair games (Australia Year 6,
BC Grade 6 and Ontario Grade 6 makers).
Wrong answers come from real mistakes: thinking all outcomes are equally likely, thinking a result is due after a
run of the other result, and expecting an experiment to match the prediction exactly.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y6_probability as aup
adopt(aup)
if isinstance(getattr(aup, 'R', None), random.Random): aup.R = random.Random(806340)
import gen_cabc_math_g6_probability as cbp
adopt(cbp)
if isinstance(getattr(cbp, 'R', None), random.Random): cbp.R = random.Random(806341)
import gen_caon_math_g6_probability as cap
adopt(cap)
if isinstance(getattr(cap, 'R', None), random.Random): cap.R = random.Random(806342)
za_common.GRADE = "grade-6"


import re as _re


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def _nums(it):
    return [int(x.replace(",", "").replace("\u00a0", "")) for x in _re.findall(r"(?<![\d.])\d[\d,\u00a0]*(?![.\d])", _txt(it)) if x.replace(",", "").replace("\u00a0", "").isdigit()]


def noneg(it):
    return not _re.search(r"(?<![\d)] )[−-]\d", _txt(it)) and "negative" not in _txt(it).lower()


def nine(it):
    """whole numbers to 9 digits, no negatives"""
    return all(n <= 999999999 for n in _nums(it)) and noneg(it)


def dec3(it):
    """decimals with at most 3 places, no negatives"""
    return noneg(it) and not _re.search(r"\d\.\d{4}", _txt(it))


def nodec(it):
    return noneg(it) and not _re.search(r"\d\.\d", _txt(it))


def flat(it):
    """first quadrant only: no negative numbers in the text or the picture"""
    return nodec(it) and "−" not in it["q"] and "-1" not in it["q"]


def nomean(it):
    return dec3(it) and not _re.search(r"\bmean\b", _txt(it))


def den12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " " + it["c"][it["a"]])]
    return all(d <= 12 or d in (20, 25, 50, 100) for d in ds) and nodec(it)



def build():
    sets, R = build_sets([
        ("The probability scale", [("run", aup.set_scale, (), 18, dec3), ("run", cap.set_line, (), 2, dec3)]),
        ("Possible outcomes", [("run", cbp.set_theory, (), 10, dec3), ("run", cap.set_find, (), 10, dec3)]),
        ("Probability as a fraction", [("run", aup.set_fdp, (), 10, dec3), ("run", aup.set_find, (), 10, dec3)]),
        ("Experiments", [("run", aup.set_experiments, (), 10, dec3), ("run", cbp.set_experimental, (), 10, dec3)]),
        ("Fair or not?", [("run", cbp.set_fair, (), 10, dec3), ("run", aup.set_problems, (), 10, dec3)]),
    ], 80634)
    finish(sets, R)
    body = lesson("<ul><li>Probability shows how likely an event is, from impossible (0) to certain (1).</li><li>List all the possible outcomes. A dice has 6.</li><li>Probability = number of ways it can happen ÷ number of possible outcomes: rolling a 5 is <span class='fr'><span class='fn'>1</span><span class='fd'>6</span></span>.</li><li>In an experiment, the results are close to the prediction but not always the same.</li></ul>",
        [example("A bag has 3 red and 5 blue beads", ["8 beads, 3 red"], "P(red) = 3/8")],
        [['All equally likely', 'Count the ways each can happen.'], ['It is due', 'A coin has no memory.'], ['Exact match', 'Results vary.']])
    faq = [('What does CAPS Grade 6 say about probability?', 'Perform simple repeated events, list possible outcomes, and count and compare the frequency of actual outcomes for a series of trials.'), ('What is the probability of a head?', '1/2.'), ('Is a probability more than 1?', 'No, 1 means certain.'), ('What makes a game fair?', 'Each player has the same chance to win.')]
    make('probability', 34, 'Data Handling', 'Grade 6: 5.4 Probability',
         'Perform simple repeated events and list possible outcomes for experiments such as tossing a coin, rolling a die and spinning a spinner; list possible outcomes for experiments; count and compare the frequency of actual outcomes for a series of trials up to 50 trials.',
         'Probability: Outcomes, Chance and Experiments', 'Probability',
         'Free CAPS Grade 6 probability worksheets: the probability scale, outcomes, probability as a fraction, experiments and fair games. 100 questions with memos.',
         'Probability = ways it can happen ÷ all outcomes.', 'Experiments vary from the prediction.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
