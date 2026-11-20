# -*- coding: utf-8 -*-
"""
South Africa Grade 8 Maths (CAPS): Probability: Two Events, Sample Spaces and Relative Frequency (Grade 8: 5.3 Probability)
  python3 tools/gen_za_maths_g8_probability.py
Probability with dice, coins and spinners, listing outcomes, complementary events, Venn diagrams and two-way tables
(UK Year 8 and Australia Year 8 makers).
Wrong answers come from real mistakes: adding probabilities that should be multiplied, missing outcomes in a list, and
counting the overlap of a Venn diagram twice.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y8_probability_of_combined_events as ukp
adopt(ukp)
if isinstance(getattr(ukp, 'R', None), random.Random): ukp.R = random.Random(808230)
import gen_au_maths_y8_probability_of_two_events as aup
adopt(aup)
if isinstance(getattr(aup, 'R', None), random.Random): aup.R = random.Random(808231)
za_common.GRADE = "grade-8"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok8(it):
    """Grade 8: no trigonometry, quadratic formula or surds beyond square roots"""
    return not _re.search(r"\b(sin|cos|tan)\b|quadratic|discriminant|imperial|\bmiles?\b", _txt(it))



def build():
    sets, R = build_sets([
        ("Two dice", [("collect", ukp.one_dice, 10), ("collect", aup.one_dice, 10)]),
        ("Coins and spinners", [("collect", ukp.one_coin_spinner, 10), ("collect", aup.one_coin_spinner, 10)]),
        ("List the outcomes", [("collect", ukp.one_list, 10), ("collect", aup.one_comp, 10)]),
        ("Venn diagrams", [("collect", ukp.one_venn, 10), ("collect", aup.one_venn, 10)]),
        ("Two-way tables", [("collect", ukp.one_twoway, 10), ("collect", aup.one_twoway, 10)]),
    ], 80823)
    finish(sets, R)
    body = lesson('<ul><li>List all the outcomes in a table or a tree. Two dice give 36 outcomes.</li><li>Probability = favourable outcomes ÷ all outcomes.</li><li>P(not A) = 1 − P(A).</li><li>In a Venn diagram, count the overlap only once.</li></ul>',
        [example("Two dice: total of 7", ["6 ways out of 36"], "1/6")],
        [['Adding instead of counting', 'List the outcomes.'], ['Missing outcomes', 'Use a table.'], ['The overlap twice', 'Count it once.']])
    faq = [('What does CAPS Grade 8 say about probability?', 'Consider situations with equally probable outcomes, determine probabilities for compound events using two-way tables and tree diagrams, and compare relative frequency with probability.'), ('How many outcomes do two coins have?', '4.'), ('What is the probability of a double six?', '1/36.'), ('What is a two-way table?', 'A table that shows two categories at once.')]
    make('probability', 23, 'Data Handling', 'Grade 8: 5.3 Probability',
         'Consider a simple situation (with equally probable outcomes) that can be described using probability; list all the possible outcomes; determine the probability of each possible outcome using the definition of probability; predict with reasons the relative frequency of the possible outcomes for a series of trials based on probability; compare relative frequency with probability and explain possible differences.',
         'Probability: Two Events, Sample Spaces and Relative Frequency', 'Probability',
         'Free CAPS Grade 8 probability worksheets: two dice, coins and spinners, sample spaces, Venn diagrams and two-way tables. 100 questions with memos.',
         'Probability = favourable ÷ all outcomes.', 'List outcomes in a table.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
