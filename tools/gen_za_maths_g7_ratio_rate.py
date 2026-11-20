# -*- coding: utf-8 -*-
"""
South Africa Grade 7 Maths (CAPS): Ratio and Rate: Simplifying, Sharing and Speed (Grade 7: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g7_ratio_rate.py
Simplifying ratios, sharing in a ratio, finding a part, ratios and fractions, recipes (UK Year 7 and Australia Year 7
makers) and rates (makers from the Grade 4 generator and BC Grade 7 maker).
Wrong answers come from real mistakes: dividing by only one part of the ratio, writing the ratio the wrong way round,
and mixing up a rate and a ratio.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y7_ratio_and_proportion as ukr
adopt(ukr)
if isinstance(getattr(ukr, 'R', None), random.Random): ukr.R = random.Random(807040)
import gen_au_maths_y7_ratios as aur
adopt(aur)
if isinstance(getattr(aur, 'R', None), random.Random): aur.R = random.Random(807041)
import gen_za_maths_g4_money_rate_ratio as zm4
adopt(zm4)
if isinstance(getattr(zm4, 'R', None), random.Random): zm4.R = random.Random(807042)
import gen_cabc_math_g7_ratios as cbr
adopt(cbr)
if isinstance(getattr(cbr, 'R', None), random.Random): cbr.R = random.Random(807043)
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
        ("Simplify ratios", [("collect", ukr.one_simplify, 10), ("collect", aur.one_simplify, 10)]),
        ("Share in a ratio", [("collect", ukr.one_share, 10), ("collect", aur.one_share, 10)]),
        ("Find a part", [("collect", ukr.one_part, 10), ("collect", ukr.one_frac, 10)]),
        ("Rates", [("collect", zm4.uniq(zm4.one_rate), 10), ("run", cbr.set_rates, (), 10, noneg)]),
        ("Ratio and rate problems", [("collect", ukr.one_recipe, 10), ("collect", aur.one_recipe, 10)]),
    ], 80704)
    finish(sets, R)
    body = lesson('<ul><li>A <b>ratio</b> compares quantities of the same kind: 12 : 18 = 2 : 3 (÷ 6).</li><li>To share R500 in the ratio 2 : 3, there are 5 parts: R500 ÷ 5 = R100, so R200 and R300.</li><li>A <b>rate</b> compares different kinds of quantities: 240 km in 3 hours is 80 km/h.</li><li>Keep the order of the ratio the same as in the question.</li></ul>',
        [example("Share R720 in the ratio 3 : 5", ["8 parts", "R720 ÷ 8 = R90"], "R270 and R450")],
        [['One part only', 'Add the parts first.'], ['Wrong way round', 'Keep the order of the question.'], ['Rate or ratio?', 'A rate has units like km/h.']])
    faq = [('What does CAPS Grade 7 say about ratio and rate?', 'Solve problems involving ratio and rate, including sharing in a given ratio and finding speed, distance and time.'), ('Is 2 : 3 the same as 3 : 2?', 'No, the order matters.'), ('What is a unit rate?', 'The amount for one unit, like R12 per kg.'), ('How do I simplify 15 : 25?', 'Divide both by 5: 3 : 5.')]
    make('ratio-and-rate', 4, 'Numbers, Operations and Relationships', 'Grade 7: 1.1 Whole numbers',
         'Solve problems in contexts involving ratio and rate, including sharing in a given ratio where the whole is given, and comparing quantities of different kinds (rate) such as speed.',
         'Ratio and Rate: Simplifying, Sharing and Speed', 'Ratio and Rate',
         'Free CAPS Grade 7 ratio and rate worksheets: simplifying ratios, sharing in a ratio, finding a part, rates and recipes. 100 questions with memos.',
         'Add the parts, find one part, then multiply.', 'Rate: different units. Ratio: same kind.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
