# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Number Sentences: Equations, Balances and Substitution (Grade 6: 2.3 Number sentences)
  python3 tools/gen_za_maths_g6_number_sentences.py
Number sentences with a missing number or a letter, balance pictures, checking solutions by substitution and writing
number sentences for stories (BC Grade 6, Ontario Grade 6 and UK Year 6 makers).
Wrong answers come from real mistakes: using the same operation instead of the inverse, doing something to only one
side of a balance, and choosing the wrong operation for the story.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_cabc_math_g6_equations as cbe
adopt(cbe)
if isinstance(getattr(cbe, 'R', None), random.Random): cbe.R = random.Random(806190)
import gen_caon_math_g6_equations as cae
adopt(cae)
if isinstance(getattr(cae, 'R', None), random.Random): cae.R = random.Random(806191)
import gen_uk_maths_y6_algebra as uka
adopt(uka)
if isinstance(getattr(uka, 'R', None), random.Random): uka.R = random.Random(806192)
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
        ("Balance the scales", [("run", cbe.set_balance, (cbe.People,), 20, nine)]),
        ("Missing numbers in + and −", [("run", cbe.set_add_sub, (cbe.People,), 20, nine)]),
        ("Missing numbers in × and ÷", [("run", cbe.set_mul, (cbe.People,), 10, nine), ("run", cbe.set_div, (cbe.People,), 10, nine)]),
        ("Check by substitution", [("run", cae.set_check, ("rnd", cae.People), 10, nine), ("run", uka.set_formulae, (uka.People,), 10, nine)]),
        ("Write a number sentence", [("run", cbe.set_words, (cbe.People,), 10, nine), ("run", uka.set_words, (uka.People,), 10, nine)]),
    ], 80619)
    finish(sets, R)
    body = lesson('<ul><li>A number sentence uses = to show both sides have the same value: 3 × ☐ + 4 = 25.</li><li>Use inverse operations to find the missing number: 25 − 4 = 21, 21 ÷ 3 = 7.</li><li>A letter can stand for the missing number: y − 38 = 64, so y = 102.</li><li>Check by substitution: put the number back in and see if both sides are equal.</li></ul>',
        [example("4 × n − 6 = 30", ["30 + 6 = 36", "36 ÷ 4"], "n = 9")],
        [['The same operation', 'Use the inverse.'], ['One side only', 'Keep the balance level.'], ['Wrong operation', 'Read what the story does.']])
    faq = [('What does CAPS Grade 6 say about number sentences?', 'Write number sentences to describe problem situations, solve and complete number sentences by inspection and trial and improvement, and check solutions by substitution.'), ('What is substitution?', 'Putting a number in place of the letter to check.'), ('What is an equation?', 'A number sentence with an = sign.'), ('Can there be two letters?', 'Yes, then there can be many solutions.')]
    make('number-sentences', 19, 'Patterns, Functions and Algebra', 'Grade 6: 2.3 Number sentences',
         'Write number sentences to describe problem situations; analyse and interpret number sentences that describe a given situation; solve and complete number sentences by inspection and by trial and improvement; check solutions by substitution.',
         'Number Sentences: Equations, Balances and Substitution', 'Number Sentences',
         'Free CAPS Grade 6 number sentences worksheets: balances, missing numbers, letters for unknowns, substitution and writing number sentences. 100 questions with memos.',
         'Use inverse operations, in reverse order.', 'Check by substitution.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
