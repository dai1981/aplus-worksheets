# -*- coding: utf-8 -*-
"""
South Africa Grade 4 Maths (CAPS): Multiples and Factors of Numbers to 100 (Grade 4: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g4_multiples_factors.py
Multiples of 1-digit numbers to 100, factors and factor pairs, and word problems with equal rows and packs (makers
from the Philippines Grade 4 generator with South African names).
Wrong answers come from real mistakes: mixing up factors and multiples, forgetting 1 and the number itself, and
leaving out the middle factor pair.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_ph_math_g4_factors_multiples as phf
adopt(phf)
if hasattr(phf, 'R'): phf.R = random.Random(804080)
za_common.GRADE = "grade-4"

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



def build():
    sets, R = build_sets([
        ("Multiples", [("collect", uniq(phf.one_mult), 20)]),
        ("Is it a factor?", [("collect", uniq(phf.one_isfactor), 20)]),
        ("Find all the factors", [("collect", uniq(phf.one_all), 20)]),
        ("Factor pairs", [("collect", uniq(phf.one_pair), 20)]),
        ("Multiples and factors problems", [("collect", uniq(phf.one_word), 20)]),
    ], 80408)
    finish(sets, R)
    body = lesson('<ul><li>A <b>multiple</b> of a number is in its times table: the multiples of 6 are 6, 12, 18, 24, …</li><li>A <b>factor</b> divides a number exactly: 4 is a factor of 24, because 24 ÷ 4 = 6.</li><li>Find all the factors in pairs: 1 × 24, 2 × 12, 3 × 8, 4 × 6.</li><li>1 and the number itself are always factors.</li></ul>',
        [example("Factors of 36", ["1 × 36, 2 × 18, 3 × 12, 4 × 9, 6 × 6"], "1, 2, 3, 4, 6, 9, 12, 18, 36")],
        [['Factors or multiples?', 'Factors divide; multiples come from multiplying.'], ['Forgetting 1 and the number', 'They are always factors.'], ['Missing the middle pair', '6 × 6 = 36: 6 is a factor.']])
    faq = [('What does CAPS Grade 4 say about multiples and factors?', 'Learners work with multiples of 1-digit numbers to at least 100.'), ('Is a number a multiple of itself?', 'Yes.'), ('Is 1 a factor of every number?', 'Yes.'), ('Why learn factors?', 'They help with division and fractions.')]
    make('multiples-and-factors', 8, 'Numbers, Operations and Relationships', 'Grade 4: 1.1 Whole numbers',
         'Multiples of 1-digit numbers to at least 100.',
         'Multiples and Factors of Numbers to 100', 'Multiples and Factors',
         'Free CAPS Grade 4 multiples and factors worksheets: multiples of 1-digit numbers to 100, factors, factor pairs and word problems. 100 questions with memos.',
         'Factors divide exactly; multiples come from multiplying.', 'List factor pairs until they meet.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
