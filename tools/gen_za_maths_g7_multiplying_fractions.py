# -*- coding: utf-8 -*-
"""
South Africa Grade 7 Maths (CAPS): Multiplying Fractions and Fractions of Amounts (Grade 7: 1.4 Common fractions)
  python3 tools/gen_za_maths_g7_multiplying_fractions.py
Fractions of amounts, multiplying fractions and mixed numbers, reciprocals and dividing by a fraction, and problems
(UK Year 7 and Australia Year 7 makers).
Wrong answers come from real mistakes: multiplying the whole number into the denominator, multiplying mixed numbers
part by part, and dividing the numerators and denominators separately.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y7_multiplying_and_dividing_fractions as ukm
adopt(ukm)
if isinstance(getattr(ukm, 'R', None), random.Random): ukm.R = random.Random(807090)
import gen_au_maths_y7_multiplying_and_dividing_fractions as aum
adopt(aum)
if isinstance(getattr(aum, 'R', None), random.Random): aum.R = random.Random(807091)
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
        ("Fractions of amounts", [("collect", ukm.one_of, 10), ("collect", aum.one_of, 10)]),
        ("Multiply fractions", [("collect", ukm.one_mul, 10), ("collect", aum.one_mul, 10)]),
        ("Multiply mixed numbers", [("collect", ukm.one_mul_mixed, 10), ("collect", aum.one_mul_mixed, 10)]),
        ("Reciprocals", [("collect", ukm.one_recip, 10), ("collect", aum.one_recip, 10)]),
        ("Fraction problems", [("run", ukm.problems, (), 10, ok7), ("run", aum.problems, (), 10, ok7)]),
    ], 80709)
    finish(sets, R)
    body = lesson("<ul><li>A fraction of an amount: divide by the denominator, multiply by the numerator.</li><li>Fraction × fraction: multiply the numerators and multiply the denominators. Simplify.</li><li>Change mixed numbers to improper fractions before you multiply.</li><li>The reciprocal of <span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span> is <span class='fr'><span class='fn'>4</span><span class='fd'>3</span></span>. A number × its reciprocal = 1.</li></ul>",
        [example("1 <span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span> × <span class='fr'><span class='fn'>2</span><span class='fd'>3</span></span>", ["<span class='fr'><span class='fn'>3</span><span class='fd'>2</span></span> × <span class='fr'><span class='fn'>2</span><span class='fd'>3</span></span> = <span class='fr'><span class='fn'>6</span><span class='fd'>6</span></span>"], "1")],
        [['Whole number into the bottom', '3 × 2/5 = 6/5.'], ['Part by part', 'Change mixed numbers to improper fractions first.'], ['Dividing separately', 'Multiply by the reciprocal.']])
    faq = [('What does CAPS Grade 7 say about multiplying fractions?', 'Multiply common fractions, including mixed numbers, and find fractions of whole numbers.'), ('What is 2/3 × 3/5?', '6/15 = 2/5.'), ('What is the reciprocal of 5?', '1/5.'), ('Does multiplying by a fraction make a number smaller?', 'Yes, if the fraction is less than 1.')]
    make('multiplying-fractions', 9, 'Numbers, Operations and Relationships', 'Grade 7: 1.4 Common fractions',
         'Multiply common fractions, including mixed numbers, not limited to fractions where one denominator is a multiple of another; find fractions of whole numbers; use knowledge of reciprocals.',
         'Multiplying Fractions and Fractions of Amounts', 'Multiplying Fractions',
         'Free CAPS Grade 7 worksheets: fractions of amounts, multiplying fractions and mixed numbers, reciprocals and fraction problems. 100 questions with memos.',
         'Top × top, bottom × bottom.', 'Mixed numbers: change to improper fractions first.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
