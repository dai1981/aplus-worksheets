# -*- coding: utf-8 -*-
"""
Philippines Grade 4 Math (MATATAG): Adding and Subtracting Dissimilar Fractions (Grade 4: Number and Algebra)
  python3 tools/gen_ph_math_g4_dissimilar_fractions.py
Adding and subtracting fractions with different denominators: related denominators (UK Year 5 maker), common
denominators, proper fractions, mixed numbers and whole numbers, and multi-step word problems (US Grade 5 makers with
Filipino names). Denominators in the questions are up to 10.
Wrong answers come from real mistakes: adding the numerators and the denominators, renaming only one fraction, and
forgetting to regroup.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_uk_maths_y5_add_sub_fractions as ukf
adopt(ukf)
if hasattr(ukf, 'R'): ukf.R = random.Random(704180)
import gen_us_math_g5_add_sub_fractions as us5
adopt(us5)
if hasattr(us5, 'R'): us5.R = random.Random(704181)
ph_common.GRADE = "grade-4"


import re as _re


def den10(it):
    """Grade 4 MATATAG: dissimilar fractions with denominators up to 10."""
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " ".join(it["c"]))]
    return all(d <= 10 for d in ds)


def den12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " ".join(it["c"]))]
    return all(d <= 12 for d in ds)


def den_q12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"])]
    return all(d <= 12 for d in ds)


def den_q10(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"])]
    return all(d <= 10 for d in ds)



def build():
    sets, R = build_sets([
        ("Related denominators", [("run", ukf.set_related, ("rnd",), 20, den_q12)]),
        ("Add dissimilar fractions", [("run", us5.set_add, ("rnd", us5.People), 20, den_q10)]),
        ("Subtract dissimilar fractions", [("run", us5.set_subtract, ("rnd", us5.People), 20, den_q10)]),
        ("Mixed numbers and whole numbers", [("run", us5.set_mixed, ("rnd",), 20, den_q10)]),
        ("Multi-step word problems", [("run", us5.set_words, ("rnd", us5.People), 20, den_q10)]),
    ], 70418)
    finish(sets, R)
    body = lesson('<ul><li>Dissimilar fractions have different denominators. You cannot add the parts until they are the same size.</li><li>Rename the fractions with a <b>common denominator</b> (a common multiple of the denominators).</li><li>Then add or subtract the numerators and keep the denominator.</li><li>Mixed numbers: work with the fractions, then the wholes. Regroup 1 whole when you need more parts.</li><li>Write the answer in simplest form.</li></ul>',
        [example("<span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span> + <span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span>", ["<span class='fr'><span class='fn'>3</span><span class='fd'>6</span></span> + <span class='fr'><span class='fn'>2</span><span class='fd'>6</span></span>"], "<span class='fr'><span class='fn'>5</span><span class='fd'>6</span></span>")],
        [['Adding tops and bottoms', "<span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span> + <span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span> is not <span class='fr'><span class='fn'>2</span><span class='fd'>5</span></span>."], ['Renaming only one fraction', 'Both fractions need the common denominator.'], ['Not regrouping', 'Change 1 whole into parts when the fraction is too small.']])
    faq = [('What does MATATAG Math 4 ask about dissimilar fractions?', 'Add and subtract dissimilar fractions using models and with two proper fractions, two mixed numbers, a mixed number and a proper fraction, a whole number and a proper fraction, and a whole number and a mixed number, and solve multi-step problems.'), ('How do I find a common denominator?', 'Find a common multiple of the denominators, like 12 for 4 and 6.'), ('Must I use the least common denominator?', 'No, but it keeps the numbers small.'), ('What are related denominators?', 'One denominator is a multiple of the other, like 3 and 6.')]
    make('adding-and-subtracting-dissimilar-fractions', 18, 'Number and Algebra', 'Grade 4: Number and Algebra',
         'Add and subtract dissimilar fractions using models; add and subtract dissimilar fractions: two proper fractions, two mixed numbers, a mixed number and a proper fraction, a whole number and a proper fraction, and a whole number and a mixed number; solve multi-step problems involving addition and/or subtraction of fractions.',
         'Adding and Subtracting Dissimilar Fractions', 'Dissimilar Fractions',
         'Free Grade 4 worksheets on adding and subtracting dissimilar fractions for the DepEd MATATAG curriculum: common denominators, mixed numbers and multi-step word problems. 100 questions with answers.',
         'Rename with a common denominator, then add or subtract.', 'Never add the denominators.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
