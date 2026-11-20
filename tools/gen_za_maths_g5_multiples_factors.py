# -*- coding: utf-8 -*-
"""
South Africa Grade 5 Maths (CAPS): Multiples and Factors of 2-Digit Numbers (Grade 5: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g5_multiples_factors.py
Multiples and factors of 2-digit numbers to 100, factor pairs, all the factors and problems (makers from the
Philippines Grade 4 generator and Australia Year 5 makers).
Wrong answers come from real mistakes: mixing up factors and multiples, forgetting 1 and the number itself, and
leaving out the middle factor pair.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_ph_math_g4_factors_multiples as phf
adopt(phf)
if isinstance(getattr(phf, 'R', None), random.Random): phf.R = random.Random(805070)
import gen_au_maths_y5_factors as auf
adopt(auf)
if isinstance(getattr(auf, 'R', None), random.Random): auf.R = random.Random(805071)
za_common.GRADE = "grade-5"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


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
        ("Multiples", [("collect", uniq(phf.one_mult), 20)]),
        ("Factors", [("collect", uniq(phf.one_isfactor), 20)]),
        ("All the factors", [("collect", uniq(phf.one_all), 20)]),
        ("Factor pairs and products", [("collect", uniq(phf.one_pair), 10), ("run", auf.set_products, (auf.People,), 10, six)]),
        ("Multiples and factors problems", [("collect", uniq(phf.one_word), 20)]),
    ], 80507)
    finish(sets, R)
    body = lesson('<ul><li>Multiples of 12: 12, 24, 36, 48, 60 … (the 12 times table).</li><li>Factors of 48 divide 48 exactly: 1, 2, 3, 4, 6, 8, 12, 16, 24, 48.</li><li>Find factors in pairs: 1 × 48, 2 × 24, 3 × 16, 4 × 12, 6 × 8.</li><li>A number is always a multiple and a factor of itself.</li></ul>',
        [example("Factors of 60", ["1 × 60, 2 × 30, 3 × 20, 4 × 15, 5 × 12, 6 × 10"], "12 factors")],
        [['Factors or multiples?', 'Factors divide; multiples come from multiplying.'], ['Forgetting 1 and the number', 'They are always factors.'], ['A missing pair', 'Test every number up to the middle.']])
    faq = [('What does CAPS Grade 5 say about multiples and factors?', 'Find multiples of 2-digit whole numbers and factors of 2-digit whole numbers to at least 100.'), ('How many factors does 36 have?', '9.'), ('Is 1 a factor of every number?', 'Yes.'), ('Why learn factors?', 'They help with division, fractions and simplifying.')]
    make('multiples-and-factors', 7, 'Numbers, Operations and Relationships', 'Grade 5: 1.1 Whole numbers',
         'Multiples of 2-digit whole numbers to at least 100; factors of 2-digit whole numbers to at least 100.',
         'Multiples and Factors of 2-Digit Numbers', 'Multiples and Factors',
         'Free CAPS Grade 5 multiples and factors worksheets: multiples, factors, factor pairs and problems for 2-digit numbers. 100 questions with memos.',
         'List factor pairs until they meet.', 'Multiples come from the times table.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
