# -*- coding: utf-8 -*-
"""
South Africa Grade 7 Maths (CAPS): Percentages: Percentages of Amounts and Percentage Change (Grade 7: 1.4 Common fractions)
  python3 tools/gen_za_maths_g7_percentages.py
Mental percentages, percentages of amounts with a multiplier, percentage increase and decrease, writing one amount as a
percentage of another, and problems (UK Year 7 and Australia Year 7 makers) with rand.
Wrong answers come from real mistakes: reading 5% as 0,5, giving the increase instead of the new amount, and dividing
the wrong way round.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y7_percentages_of_amounts as ukp
adopt(ukp)
if isinstance(getattr(ukp, 'R', None), random.Random): ukp.R = random.Random(807100)
import gen_au_maths_y7_percentages_and_discounts as aup
adopt(aup)
if isinstance(getattr(aup, 'R', None), random.Random): aup.R = random.Random(807101)
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
        ("Mental percentages", [("collect", ukp.one_mental, 10), ("collect", aup.one_mental, 10)]),
        ("Percentages with a multiplier", [("collect", ukp.one_mult, 10), ("collect", aup.one_mult, 10)]),
        ("Increase and decrease", [("collect", ukp.one_change, 10), ("collect", aup.one_change, 10)]),
        ("One amount as a percentage", [("collect", ukp.one_as_pct, 10), ("collect", aup.one_as_pct, 10)]),
        ("Percentage problems", [("run", ukp.problems, (), 10, ok7), ("run", aup.problems, (), 10, ok7)]),
    ], 80710)
    finish(sets, R)
    body = lesson('<ul><li>Per cent means out of 100: 35% = 0,35.</li><li>Find 10% by dividing by 10, then build: 35% = 3 × 10% + 5%.</li><li>With a multiplier: 35% of R240 = 0,35 × R240 = R84.</li><li>Increase by 20%: × 1,2. Decrease by 20%: × 0,8.</li></ul>',
        [example("Increase R450 by 12%", ["12% of R450 = R54"], "R504")],
        [['5% as 0,5', '5% = 0,05.'], ['The increase, not the new amount', 'Add it on.'], ['Dividing the wrong way', 'Part ÷ whole × 100.']])
    faq = [('What does CAPS Grade 7 say about percentages?', 'Calculate percentages of whole numbers, express one quantity as a percentage of another, and find percentage increase and decrease.'), ('What is 25% of 80?', '20.'), ('What is 18 out of 24 as a percentage?', '75%.'), ('What is a multiplier?', 'The decimal you multiply by, like 0,35 for 35%.')]
    make('percentages', 10, 'Numbers, Operations and Relationships', 'Grade 7: 1.4 Common fractions',
         'Calculate the percentage of part of a whole; calculate percentage increase or decrease; solve problems in contexts involving percentages.',
         'Percentages: Percentages of Amounts and Percentage Change', 'Percentages',
         'Free CAPS Grade 7 percentages worksheets: percentages of amounts, multipliers, percentage increase and decrease and one amount as a percentage. 100 questions with memos.',
         'Per cent means out of 100.', 'Increase by 20%: × 1,2.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
