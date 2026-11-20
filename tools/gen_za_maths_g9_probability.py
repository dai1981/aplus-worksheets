# -*- coding: utf-8 -*-
"""
South Africa Grade 9 Maths (CAPS): Probability: Compound Events, Tree Diagrams and Two-Way Tables (Grade 9: 5.3 Probability)
  python3 tools/gen_za_maths_g9_probability.py
Probability of single and complementary events, sample spaces for two events, Venn diagrams and two-way tables
(Singapore Secondary 2 and Australia Year 8 makers).
Wrong answers come from real mistakes: adding probabilities that should be multiplied, missing outcomes, and counting
the overlap of a Venn diagram twice.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_sg_maths_s2_probability as sgp
adopt(sgp)
if isinstance(getattr(sgp, 'R', None), random.Random): sgp.R = random.Random(809210)
import gen_au_maths_y8_probability_of_two_events as aup
adopt(aup)
if isinstance(getattr(aup, 'R', None), random.Random): aup.R = random.Random(809211)
za_common.GRADE = "grade-9"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok9(it):
    """Grade 9: no trigonometry, quadratic formula, simultaneous equations or cones and spheres (Grade 10+)"""
    return not _re.search(r"\b(sin|cos|tan)\b|quadratic formula|discriminant|simultaneous|\bcone|\bsphere|imperial|\bmiles?\b", _txt(it))



def build():
    sets, R = build_sets([
        ("Single events", [("collect", sgp.one_single, 10), ("collect", sgp.one_not, 10)]),
        ("Two dice and coins", [("collect", aup.one_dice, 10), ("collect", aup.one_coin_spinner, 10)]),
        ("Sample spaces", [("collect", sgp.one_space, 10), ("collect", aup.one_list, 10)]),
        ("Venn diagrams", [("collect", aup.one_venn, 10), ("collect", aup.one_comp, 10)]),
        ("Two-way tables", [("collect", aup.one_twoway, 20)]),
    ], 80921)
    finish(sets, R)
    body = lesson('<ul><li>Probability = favourable outcomes ÷ all equally likely outcomes.</li><li>P(not A) = 1 − P(A).</li><li>For two events, list the outcomes in a table or tree diagram.</li><li>In a Venn diagram, count the overlap only once.</li></ul>',
        [example("Two coins: at least one head", ["HH, HT, TH, TT", "3 of 4"], "3/4")],
        [['Adding instead of listing', 'List the outcomes.'], ['Missing outcomes', 'Use a table or tree.'], ['The overlap twice', 'Count it once.']])
    faq = [('What does CAPS Grade 9 say about probability?', 'Consider situations with equally probable outcomes, determine probabilities for compound events using two-way tables and tree diagrams, and compare relative frequency with probability.'), ('How many outcomes do two dice have?', '36.'), ('What is a tree diagram?', 'A diagram that shows all the outcomes step by step.'), ('What is the probability of rolling a total of 12?', '1/36.')]
    make('probability', 21, 'Data Handling', 'Grade 9: 5.3 Probability',
         'Consider situations with equally probable outcomes; determine probabilities for compound events using two-way tables and tree diagrams; determine the probabilities for outcomes of events and predict their relative frequency in simple experiments; compare relative frequency with probability and explain possible differences.',
         'Probability: Compound Events, Tree Diagrams and Two-Way Tables', 'Probability',
         'Free CAPS Grade 9 probability worksheets: single and complementary events, two dice, sample spaces, Venn diagrams and two-way tables. 100 questions with memos.',
         'Probability = favourable ÷ all outcomes.', 'List outcomes in a table or tree.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
