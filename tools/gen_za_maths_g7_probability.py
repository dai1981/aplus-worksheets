# -*- coding: utf-8 -*-
"""
South Africa Grade 7 Maths (CAPS): Probability: Outcomes, Relative Frequency and Probability (Grade 7: 5.3 Probability)
  python3 tools/gen_za_maths_g7_probability.py
The probability scale, probability of single events, events not happening, sample spaces, and relative frequency
from experiments (UK Year 7, Australia Year 7 and BC Grade 7 makers).
Wrong answers come from real mistakes: writing a probability bigger than 1, counting an outcome twice, and mixing up
relative frequency and probability.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y7_probability as ukp
adopt(ukp)
if isinstance(getattr(ukp, 'R', None), random.Random): ukp.R = random.Random(807260)
import gen_au_maths_y7_probability as aup
adopt(aup)
if isinstance(getattr(aup, 'R', None), random.Random): aup.R = random.Random(807261)
import gen_cabc_math_g7_probability as cbp
adopt(cbp)
if isinstance(getattr(cbp, 'R', None), random.Random): cbp.R = random.Random(807262)
za_common.GRADE = "grade-7"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok7(it):
    """Grade 7: no circles, pi or standard form (they come in Grade 8 and 9)"""
    return not _re.search(r"π|\bpi\b|circumference|radius|diameter|×\s?10<sup>|standard form|scientific notation", _txt(it))


def noneg(it):
    return ok7(it) and not _re.search(r"(?<![\d)] )[−-]\d", _txt(it))



def build():
    sets, R = build_sets([
        ("The probability scale", [("collect", ukp.one_scale, 10), ("collect", aup.one_scale, 10)]),
        ("Probability of an event", [("collect", ukp.one_single, 10), ("collect", aup.one_single, 10)]),
        ("Not happening", [("collect", ukp.one_not, 10), ("collect", aup.one_not, 10)]),
        ("Sample spaces", [("collect", ukp.one_space, 10), ("run", cbp.set_sample_spaces, (), 10, ok7)]),
        ("Relative frequency", [("run", cbp.set_experimental, (), 10, ok7), ("run", cbp.set_compare, (), 10, ok7)]),
    ], 80726)
    finish(sets, R)
    body = lesson('<ul><li>Probability = number of favourable outcomes ÷ number of possible outcomes.</li><li>Probabilities go from 0 (impossible) to 1 (certain).</li><li>P(not A) = 1 − P(A).</li><li>Relative frequency = number of times an outcome happened ÷ number of trials. With more trials it gets closer to the probability.</li></ul>',
        [example("A bag has 3 red, 5 blue and 2 green beads", ["10 beads", "not red: 7"], "P(not red) = 7/10")],
        [['More than 1', 'A probability is at most 1.'], ['Counting twice', 'List the outcomes carefully.'], ['Relative frequency = probability', 'It comes from an experiment and changes.']])
    faq = [('What does CAPS Grade 7 say about probability?', 'List possible outcomes for simple experiments, determine the probability of outcomes, and compare relative frequency with probability.'), ('What is the probability of rolling an even number?', '3/6 = 1/2.'), ('What is a sample space?', 'The list of all possible outcomes.'), ('Why do more trials help?', 'The relative frequency gets closer to the probability.')]
    make('probability', 26, 'Data Handling', 'Grade 7: 5.3 Probability',
         'Perform simple experiments where the possible outcomes are equally likely and list the possible outcomes based on the conditions of the activity; determine probabilities for each possible outcome; determine the relative frequency of the actual outcomes for a series of trials; compare relative frequency with probability and explain possible differences.',
         'Probability: Outcomes, Relative Frequency and Probability', 'Probability',
         'Free CAPS Grade 7 probability worksheets: the probability scale, single events, sample spaces and relative frequency. 100 questions with memos.',
         'P = favourable ÷ possible.', 'P(not A) = 1 − P(A).',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
