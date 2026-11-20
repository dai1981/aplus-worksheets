# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): Properties of Operations: Commutative, Associative and Distributive (Grade 5: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g5_properties.py
The commutative, associative and distributive properties with whole numbers (US Grade 3 makers) and the properties
in number sentences (Australia Year 5 maker).
Wrong answers come from real mistakes: thinking subtraction and division are commutative, multiplying only one part
in the distributive property, and adding instead of multiplying.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_us_math_g3_properties as usp
adopt(usp)
if isinstance(getattr(usp, 'R', None), random.Random): usp.R = random.Random(805080)
import gen_au_maths_y5_number_sentences as aun
adopt(aun)
if isinstance(getattr(aun, 'R', None), random.Random): aun.R = random.Random(805081)
za_common.GRADE = "grade-5"


import re as _re


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def _nums(it):
    return [int(x.replace(",", "").replace("\u00a0", "")) for x in _re.findall(r"(?<![\d.])\d[\d,\u00a0]*(?![.\d])", _txt(it)) if x.replace(",", "").replace("\u00a0", "").isdigit()]


def six(it):
    """whole numbers to 6 digits, no decimals, no negatives"""
    t = _txt(it)
    return all(n <= 999999 for n in _nums(it)) and not _re.search(r"\d\.\d|−\d", t)


def nodec(it):
    return not _re.search(r"\d\.\d|−\d", _txt(it))


def den12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " " + it["c"][it["a"]])]
    return all(d <= 12 for d in ds) and nodec(it)



def build():
    sets, R = build_sets([
        ("Commutative property", [("run", usp.set_commutative, ("rnd",), 20)]),
        ("Associative property", [("run", usp.set_associative, ("rnd",), 20)]),
        ("Distributive property", [("run", usp.set_distributive, ("rnd",), 20)]),
        ("Properties in number sentences", [("run", aun.set_props, (), 20, six)]),
        ("Use the properties", [("run", usp.set_name_and_story, ("rnd",), 10), ("run", usp.set_one_zero, ("rnd",), 10)]),
    ], 80508)
    finish(sets, R)
    body = lesson('<ul><li><b>Commutative</b>: 25 + 48 = 48 + 25 and 6 × 9 = 9 × 6.</li><li><b>Associative</b>: (4 × 25) × 7 = 4 × (25 × 7).</li><li><b>Distributive</b>: 7 × 46 = 7 × 40 + 7 × 6.</li><li>These properties work for + and ×, not for − and ÷.</li></ul>',
        [example("4 × 37 × 25", ["(4 × 25) × 37", "100 × 37"], "3 700")],
        [['− and ÷ are not commutative', '12 ÷ 4 ≠ 4 ÷ 12.'], ['One part only', 'Multiply both parts.'], ['Adding', 'Distribute the multiplication.']])
    faq = [('What does CAPS Grade 5 say about properties?', 'Recognise and use the commutative, associative and distributive properties with whole numbers.'), ('Why use the associative property?', 'To group numbers that are easy together, like 4 × 25.'), ('Is 0 special?', 'Adding 0 keeps a number; multiplying by 0 gives 0.'), ('Where does the distributive property help?', 'In mental multiplication.')]
    make('properties-of-operations', 8, 'Numbers, Operations and Relationships', 'Grade 5: 1.1 Whole numbers',
         'Recognise and use the commutative, associative and distributive properties with whole numbers.',
         'Properties of Operations: Commutative, Associative and Distributive', 'Properties of Operations',
         'Free CAPS Grade 5 worksheets on properties of operations: commutative, associative and distributive properties. 100 questions with memos.',
         'Order and grouping do not change + and ×.', '7 × 46 = 7 × 40 + 7 × 6.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
