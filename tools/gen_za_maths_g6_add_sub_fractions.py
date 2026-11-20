# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Adding and Subtracting Fractions and Mixed Numbers (Grade 6: 1.2 Common fractions)
  python3 tools/gen_za_maths_g6_add_sub_fractions.py
Adding and subtracting fractions where one denominator is a multiple of the other, and mixed numbers (UK Year 6,
Australia Year 6 and Ontario Grade 6 makers), and word problems.
Wrong answers come from real mistakes: adding the denominators, changing only the denominator, and forgetting to
regroup a whole in a mixed number.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y6_add_sub_fractions as ukf
adopt(ukf)
if isinstance(getattr(ukf, 'R', None), random.Random): ukf.R = random.Random(806100)
import gen_au_maths_y6_add_sub_fractions as auf
adopt(auf)
if isinstance(getattr(auf, 'R', None), random.Random): auf.R = random.Random(806101)
import gen_caon_math_g6_add_sub_fractions as caf
adopt(caf)
if isinstance(getattr(caf, 'R', None), random.Random): caf.R = random.Random(806102)
import gen_za_maths_g5_add_sub_fractions as zf5
adopt(zf5)
if isinstance(getattr(zf5, 'R', None), random.Random): zf5.R = random.Random(806103)
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
        ("Same denominators", [("run", caf.set_like, ("rnd", caf.People), 10, den12), ("collect", zf5.uniq(zf5.one_mixed), 10)]),
        ("Related denominators", [("run", ukf.set_related, ("rnd",), 10, den12), ("run", auf.set_related, ("rnd",), 10, den12)]),
        ("Improper fractions", [("run", ukf.set_improper, ("rnd",), 10, den12), ("run", auf.set_improper, ("rnd", auf.People), 10, den12)]),
        ("Mixed numbers", [("run", ukf.set_mixed, ("rnd",), 10, den12), ("run", caf.set_mixed, ("rnd",), 10, den12)]),
        ("Fraction problems", [("run", ukf.set_words, ("rnd", ukf.People), 10, den12), ("run", auf.set_words, ("rnd", auf.People), 10, den12)]),
    ], 80610)
    finish(sets, R)
    body = lesson("<ul><li>With the same denominator, add or subtract the numerators.</li><li>When one denominator is a multiple of the other, change one fraction: <span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span> = <span class='fr'><span class='fn'>2</span><span class='fd'>6</span></span>.</li><li>Mixed numbers: add or subtract the wholes and the fractions, then regroup.</li><li>Write the answer in simplest form.</li></ul>",
        [example("<span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span> + <span class='fr'><span class='fn'>5</span><span class='fd'>8</span></span>", ["<span class='fr'><span class='fn'>6</span><span class='fd'>8</span></span> + <span class='fr'><span class='fn'>5</span><span class='fd'>8</span></span> = <span class='fr'><span class='fn'>11</span><span class='fd'>8</span></span>"], "1 <span class='fr'><span class='fn'>3</span><span class='fd'>8</span></span>")],
        [['Adding denominators', 'Keep the common denominator.'], ['Changing the bottom only', 'Multiply the top too.'], ['Not regrouping', '11/8 = 1 3/8.']])
    faq = [('What does CAPS Grade 6 say about adding fractions?', 'Add and subtract common fractions in which one denominator is a multiple of the other, and mixed numbers.'), ('What is 1/2 + 1/4?', '3/4.'), ('Do I need the LCM?', 'In Grade 6, one denominator is a multiple of the other, so use the bigger one.'), ('Should I simplify?', 'Yes, write the answer in simplest form.')]
    make('adding-and-subtracting-fractions', 10, 'Numbers, Operations and Relationships', 'Grade 6: 1.2 Common fractions',
         'Add and subtract common fractions in which one denominator is a multiple of another; add and subtract mixed numbers; solve problems in contexts involving common fractions, including grouping and sharing.',
         'Adding and Subtracting Fractions and Mixed Numbers', 'Adding and Subtracting Fractions',
         'Free CAPS Grade 6 worksheets: adding and subtracting fractions with related denominators, improper fractions and mixed numbers. 100 questions with memos.',
         'Make the denominators the same, then add the numerators.', 'Regroup and simplify the answer.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
