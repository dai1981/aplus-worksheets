# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Common Fractions: Equivalent Fractions, Simplest Form and Comparing (Grade 6: 1.2 Common fractions)
  python3 tools/gen_za_maths_g6_fractions.py
Equivalent fractions, simplifying, comparing and ordering fractions, and mixed numbers and improper fractions (UK
Year 6, Australia Year 6 and BC Grade 6 makers).
Wrong answers come from real mistakes: thinking a bigger denominator means a bigger fraction, dividing only the
numerator, and comparing the numerators of fractions with different denominators.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y6_simplify_compare_fractions as uks
adopt(uks)
if isinstance(getattr(uks, 'R', None), random.Random): uks.R = random.Random(806090)
import gen_au_maths_y6_compare_fractions as auc
adopt(auc)
if isinstance(getattr(auc, 'R', None), random.Random): auc.R = random.Random(806091)
import gen_cabc_math_g6_fractions as cbf
adopt(cbf)
if isinstance(getattr(cbf, 'R', None), random.Random): cbf.R = random.Random(806092)
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
        ("Equivalent fractions", [("run", auc.set_equivalent, ("rnd",), 10, den12), ("run", cbf.set_models, ("rnd",), 10, den12)]),
        ("Simplest form", [("run", uks.set_simplify, ("rnd",), 11, den12), ("run", uks.set_common, ("rnd",), 9, den12)]),
        ("Compare and order", [("run", uks.set_compare, ("rnd",), 10, den12), ("run", auc.set_order, ("rnd",), 10, den12)]),
        ("Mixed numbers and improper fractions", [("run", cbf.set_mixed, ("rnd",), 10, den12), ("run", cbf.set_convert, ("rnd",), 10, den12)]),
        ("Fraction problems", [("run", uks.set_words, ("rnd",), 10, den12), ("run", cbf.set_words, ("rnd",), 10, den12)]),
    ], 80609)
    finish(sets, R)
    body = lesson("<ul><li>Equivalent fractions: multiply or divide the numerator and denominator by the same number.</li><li>Simplest form: divide both by their HCF. <span class='fr'><span class='fn'>18</span><span class='fd'>24</span></span> = <span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span> (÷ 6).</li><li>To compare, give the fractions a common denominator.</li><li>Improper fraction to mixed number: divide. <span class='fr'><span class='fn'>17</span><span class='fd'>5</span></span> = 3 <span class='fr'><span class='fn'>2</span><span class='fd'>5</span></span>.</li></ul>",
        [example("Compare <span class='fr'><span class='fn'>5</span><span class='fd'>6</span></span> and <span class='fr'><span class='fn'>7</span><span class='fd'>9</span></span>", ["common denominator 18", "15 and 14"], "<span class='fr'><span class='fn'>5</span><span class='fd'>6</span></span> is bigger")],
        [['Bigger denominator, bigger fraction', 'Twelfths are smaller than sixths.'], ['Dividing one number', 'Divide the top and bottom.'], ['Comparing numerators', 'Use a common denominator first.']])
    faq = [('What does CAPS Grade 6 say about fractions?', 'Compare and order common fractions, including tenths and hundredths, recognise and use equivalent forms, and write fractions in simplest form.'), ('What is the simplest form of 12/16?', '3/4.'), ('Is 7/4 a mixed number?', 'No, it is an improper fraction; 1 3/4 is the mixed number.'), ('How do I find a common denominator?', 'Use the LCM of the denominators.')]
    make('common-fractions', 9, 'Numbers, Operations and Relationships', 'Grade 6: 1.2 Common fractions',
         'Count forwards and backwards in fractions; compare and order common fractions, including specifically tenths and hundredths; recognise and use equivalent forms of common fractions with 1-digit or 2-digit denominators (fractions where one denominator is a multiple of another).',
         'Common Fractions: Equivalent Fractions, Simplest Form and Comparing', 'Common Fractions',
         'Free CAPS Grade 6 common fractions worksheets: equivalent fractions, simplest form, comparing, ordering and mixed numbers. 100 questions with memos.',
         'Common denominator first, then compare.', 'Simplest form: divide by the HCF.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
