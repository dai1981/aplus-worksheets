# -*- coding: utf-8 -*-
"""
South Africa Grade 8 Maths (CAPS): Common Fractions: All Four Operations (Grade 8: 1.4 Common fractions)
  python3 tools/gen_za_maths_g8_fractions.py
Adding, subtracting, multiplying and dividing fractions and mixed numbers, and squares and roots of fractions (UK
Year 7 and Australia Year 7 and Year 8 makers).
Wrong answers come from real mistakes: adding the denominators, dividing without the reciprocal, and squaring only
the numerator.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y7_adding_and_subtracting_fractions as uka
adopt(uka)
if isinstance(getattr(uka, 'R', None), random.Random): uka.R = random.Random(808060)
import gen_uk_maths_y7_multiplying_and_dividing_fractions as ukm
adopt(ukm)
if isinstance(getattr(ukm, 'R', None), random.Random): ukm.R = random.Random(808061)
import gen_au_maths_y8_integers_and_rational_numbers as aur
adopt(aur)
if isinstance(getattr(aur, 'R', None), random.Random): aur.R = random.Random(808062)
import gen_au_maths_y7_multiplying_and_dividing_fractions as aum
adopt(aum)
if isinstance(getattr(aum, 'R', None), random.Random): aum.R = random.Random(808063)
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
        ("Add and subtract fractions", [("collect", uka.one_any, 10), ("collect", uka.one_mixed, 10)]),
        ("Multiply fractions", [("collect", ukm.one_mul, 10), ("collect", ukm.one_mul_mixed, 10)]),
        ("Divide fractions", [("collect", ukm.one_div, 10), ("collect", aum.one_div, 10)]),
        ("Rational numbers", [("collect", aur.one_rat, 20)]),
        ("Fraction problems", [("run", ukm.problems, (), 10, ok8), ("run", aum.problems, (), 10, ok8)]),
    ], 80806)
    finish(sets, R)
    body = lesson("<ul><li>Add and subtract with a common denominator.</li><li>Multiply: numerator × numerator, denominator × denominator.</li><li>Divide: multiply by the reciprocal. <span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span> ÷ <span class='fr'><span class='fn'>2</span><span class='fd'>5</span></span> = <span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span> × <span class='fr'><span class='fn'>5</span><span class='fd'>2</span></span> = <span class='fr'><span class='fn'>15</span><span class='fd'>8</span></span>.</li><li>Square a fraction: square the top and the bottom.</li></ul>",
        [example("2 <span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span> ÷ <span class='fr'><span class='fn'>7</span><span class='fd'>9</span></span>", ["<span class='fr'><span class='fn'>7</span><span class='fd'>3</span></span> × <span class='fr'><span class='fn'>9</span><span class='fd'>7</span></span>"], "3")],
        [['Adding denominators', 'Keep the common denominator.'], ['No reciprocal', 'Turn the second fraction upside down.'], ['Squaring the top only', '(2/3)² = 4/9.']])
    faq = [('What does CAPS Grade 8 say about fractions?', 'Add, subtract, multiply and divide common fractions, including mixed numbers, and calculate squares, cubes, square roots and cube roots of fractions.'), ('What is 1/2 ÷ 1/4?', '2.'), ('What is √(9/16)?', '3/4.'), ('Do I change mixed numbers first?', 'Yes, to improper fractions.')]
    make('common-fractions', 6, 'Numbers, Operations and Relationships', 'Grade 8: 1.4 Common fractions',
         'Add, subtract, multiply and divide common fractions, including mixed numbers; calculate the squares, cubes, square roots and cube roots of common fractions; solve problems involving common fractions.',
         'Common Fractions: All Four Operations', 'Common Fractions',
         'Free CAPS Grade 8 fractions worksheets: adding, subtracting, multiplying and dividing fractions and mixed numbers, and rational numbers. 100 questions with memos.',
         'Divide: multiply by the reciprocal.', 'Change mixed numbers first.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
