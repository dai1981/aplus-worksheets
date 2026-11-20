# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Properties of Operations and the Order of Operations (Grade 6: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g6_properties.py
The commutative, associative and distributive properties (US Grade 3 and Australia Year 5 makers) and the order of
operations with brackets (UK Year 6 and BC Grade 6 makers).
Wrong answers come from real mistakes: working only from left to right, ignoring brackets, and thinking subtraction
is commutative.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_us_math_g3_properties as usp
adopt(usp)
if isinstance(getattr(usp, 'R', None), random.Random): usp.R = random.Random(806080)
import gen_au_maths_y5_number_sentences as aun
adopt(aun)
if isinstance(getattr(aun, 'R', None), random.Random): aun.R = random.Random(806081)
import gen_uk_maths_y6_order_of_operations as uko
adopt(uko)
if isinstance(getattr(uko, 'R', None), random.Random): uko.R = random.Random(806082)
import gen_cabc_math_g6_order_of_operations as cbo
adopt(cbo)
if isinstance(getattr(cbo, 'R', None), random.Random): cbo.R = random.Random(806083)
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
        ("Commutative and associative", [("run", usp.set_commutative, ("rnd",), 10, nine), ("run", usp.set_associative, ("rnd",), 10, nine)]),
        ("Distributive property", [("run", usp.set_distributive, ("rnd",), 10, nine), ("run", aun.set_props, (), 10, nine)]),
        ("Order of operations", [("run", cbo.set_order, ("rnd", "seen"), 10, nine), ("run", uko.set_precedence, ("rnd", uko.People), 10, nine)]),
        ("Brackets", [("run", cbo.set_brackets, ("rnd", "seen"), 10, nine), ("run", uko.set_brackets, ("rnd", uko.People), 10, nine)]),
        ("Problems", [("run", cbo.set_words, ("rnd", "seen"), 7, nine), ("run", uko.set_words, ("rnd", uko.People), 13, nine)]),
    ], 80608)
    finish(sets, R)
    body = lesson('<ul><li><b>Commutative</b>: 25 + 48 = 48 + 25 and 6 × 9 = 9 × 6. <b>Associative</b>: (4 × 25) × 7 = 4 × (25 × 7).</li><li><b>Distributive</b>: 8 × 47 = 8 × 40 + 8 × 7.</li><li><b>Order of operations</b>: brackets first, then × and ÷ from left to right, then + and − from left to right.</li><li>The properties work for + and ×, not for − and ÷.</li></ul>',
        [example("20 − 4 × 3 + (6 + 2)", ["brackets: 8", "× : 12", "20 − 12 + 8"], "16")],
        [['Left to right only', '× and ÷ come before + and −.'], ['Ignoring brackets', 'Work out brackets first.'], ['− is not commutative', '9 − 4 ≠ 4 − 9.']])
    faq = [('What does CAPS Grade 6 say about properties?', 'Recognise and use the commutative, associative and distributive properties with whole numbers, and use brackets.'), ('What is done first: × or +?', '× and ÷ before + and −.'), ('Why use brackets?', 'To show what to work out first.'), ('Is 2 + 3 × 4 = 20?', 'No, 3 × 4 first: 2 + 12 = 14.')]
    make('properties-and-order-of-operations', 8, 'Numbers, Operations and Relationships', 'Grade 6: 1.1 Whole numbers',
         'Recognise and use the commutative, associative and distributive properties with whole numbers; recognise and use the order of operations, including brackets.',
         'Properties of Operations and the Order of Operations', 'Properties and Order of Operations',
         'Free CAPS Grade 6 worksheets: commutative, associative and distributive properties, the order of operations and brackets. 100 questions with memos.',
         'Brackets, then × and ÷, then + and −.', 'Order and grouping do not change + and ×.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
