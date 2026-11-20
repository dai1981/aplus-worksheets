# -*- coding: utf-8 -*-
"""
South Africa Grade 4 Maths (CAPS): Properties of Operations: Commutative, Associative and Distributive (Grade 4: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g4_properties.py
The commutative, associative and distributive properties and the role of 0 and 1 (US Grade 3 makers), and the
properties in number sentences (Australia Year 4 maker).
Wrong answers come from real mistakes: thinking subtraction is commutative, multiplying only one part when using
the distributive property, and thinking × 0 keeps the number.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_us_math_g3_properties as usp
adopt(usp)
if hasattr(usp, 'R'): usp.R = random.Random(804090)
import gen_au_maths_y4_number_sentences as aun
adopt(aun)
if hasattr(aun, 'R'): aun.R = random.Random(804091)
za_common.GRADE = "grade-4"


import re as _re


def _nums(it):
    t = _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"]
    t = _re.sub(r"<[^>]+>", " ", t)
    return [int(x.replace(",", "").replace("\u00a0", "")) for x in _re.findall(r"(?<![\d.])\d[\d,\u00a0]*(?![.\d])", t) if x.replace(",", "").replace("\u00a0", "").isdigit()]


def le10000(it):
    return all(n <= 10000 for n in _nums(it))


def le100k(it):
    return all(n <= 99999 for n in _nums(it))


def den12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " ".join(it["c"]))]
    return all(d <= 12 for d in ds)


def den8(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " ".join(it["c"]))]
    return all(d <= 8 for d in ds)



def build():
    sets, R = build_sets([
        ("Commutative property", [("run", usp.set_commutative, ("rnd",), 20)]),
        ("Associative property", [("run", usp.set_associative, ("rnd",), 20)]),
        ("Distributive property", [("run", usp.set_distributive, ("rnd",), 20)]),
        ("0 and 1", [("run", usp.set_one_zero, ("rnd",), 15), ("run", aun.set_equals, (aun.People,), 5)]),
        ("Properties in number sentences", [("run", aun.set_props, (aun.People,), 10), ("run", usp.set_name_and_story, ("rnd",), 10)]),
    ], 80409)
    finish(sets, R)
    body = lesson('<ul><li><b>Commutative</b>: the order does not change the answer for + and ×: 7 + 5 = 5 + 7; 4 × 9 = 9 × 4.</li><li><b>Associative</b>: the grouping does not change the answer for + and ×: (2 × 5) × 7 = 2 × (5 × 7).</li><li><b>Distributive</b>: 6 × 14 = 6 × 10 + 6 × 4.</li><li>Subtraction and division are <b>not</b> commutative.</li></ul>',
        [example("8 × 23", ["8 × 20 + 8 × 3", "160 + 24"], "184")],
        [['Subtraction turned around', '9 − 4 ≠ 4 − 9.'], ['Multiplying one part', 'Multiply every part.'], ['× 0', 'Any number × 0 = 0.']])
    faq = [('What does CAPS Grade 4 say about properties?', 'Recognise and use the commutative, associative and distributive properties with whole numbers.'), ('Why learn properties?', 'They make mental calculations easier.'), ('Is division associative?', 'No.'), ('What is 0 × 999?', '0.')]
    make('properties-of-operations', 9, 'Numbers, Operations and Relationships', 'Grade 4: 1.1 Whole numbers',
         'Recognise and use the commutative, associative and distributive properties with whole numbers.',
         'Properties of Operations: Commutative, Associative and Distributive', 'Properties of Operations',
         'Free CAPS Grade 4 worksheets on properties of operations: commutative, associative and distributive properties and 0 and 1. 100 questions with memos.',
         'Order and grouping do not change + and ×.', '6 × 14 = 6 × 10 + 6 × 4.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
