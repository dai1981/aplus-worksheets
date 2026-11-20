# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Multiples, Factors, Prime Numbers, LCM and HCF (Grade 6: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g6_multiples_factors.py
Factors, prime numbers to 100, factor trees, the highest common factor (HCF) and the lowest common multiple (LCM),
and problems (UK Year 6, Ontario Grade 6 and Australia Year 6 makers).
Wrong answers come from real mistakes: calling 1 a prime number, mixing up the HCF and the LCM, and multiplying the
numbers to find the LCM.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y6_factors_primes as ukf
adopt(ukf)
if isinstance(getattr(ukf, 'R', None), random.Random): ukf.R = random.Random(806070)
import gen_caon_math_g6_factors as caf
adopt(caf)
if isinstance(getattr(caf, 'R', None), random.Random): caf.R = random.Random(806071)
import gen_au_maths_y6_primes_squares as aup
adopt(aup)
if isinstance(getattr(aup, 'R', None), random.Random): aup.R = random.Random(806072)
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
        ("Factors", [("run", ukf.set_factors, (ukf.People,), 10, nine), ("run", caf.set_factors, (caf.People,), 10, nine)]),
        ("Prime numbers", [("run", ukf.set_primes, (ukf.People,), 10, nine), ("run", aup.set_prime_composite, (aup.People,), 10, nine)]),
        ("Factor trees", [("run", caf.set_trees, (caf.People,), 10, nine), ("run", aup.set_factor_trees, (aup.People,), 10, nine)]),
        ("HCF and LCM", [("run", ukf.set_hcf, (ukf.People,), 10, nine), ("run", ukf.set_lcm, (ukf.People,), 10, nine)]),
        ("Factor and multiple problems", [("run", ukf.set_words, (ukf.People,), 10, nine), ("run", caf.set_words, (caf.People,), 10, nine)]),
    ], 80607)
    finish(sets, R)
    body = lesson('<ul><li>A <b>prime number</b> has exactly two factors: 1 and itself (2, 3, 5, 7, 11 …). 1 is not prime.</li><li>A <b>composite number</b> has more than two factors.</li><li>The <b>HCF</b> is the biggest factor two numbers share. The <b>LCM</b> is the smallest multiple they share.</li><li>A factor tree breaks a number into prime factors: 36 = 2 × 2 × 3 × 3.</li></ul>',
        [example("HCF and LCM of 12 and 18", ["factors of 12: 1, 2, 3, 4, 6, 12", "multiples: 36 is first in both lists"], "HCF 6, LCM 36")],
        [['1 is prime', '1 has only one factor.'], ['HCF or LCM?', 'Factors are small; multiples are big.'], ['Multiplying for the LCM', '12 × 18 = 216 is common, but not the lowest.']])
    faq = [('What does CAPS Grade 6 say about multiples and factors?', 'Find multiples and factors of numbers to at least 100, prime numbers to at least 100, and the LCM and HCF of whole numbers.'), ('Is 2 a prime number?', 'Yes, the only even prime.'), ('How many primes are below 100?', '25.'), ('Where is the LCM used?', 'To find a common denominator for fractions.')]
    make('multiples-factors-and-prime-numbers', 7, 'Numbers, Operations and Relationships', 'Grade 6: 1.1 Whole numbers',
         'Multiples of 2-digit and 3-digit whole numbers; factors of 2-digit and 3-digit whole numbers; prime factors of numbers to at least 100; prime numbers to at least 100; LCM and HCF of numbers to at least 3-digit whole numbers.',
         'Multiples, Factors, Prime Numbers, LCM and HCF', 'Multiples, Factors and Primes',
         'Free CAPS Grade 6 worksheets: factors, multiples, prime numbers, factor trees, HCF and LCM. 100 questions with memos.',
         'A prime has exactly two factors.', 'HCF: biggest shared factor. LCM: smallest shared multiple.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
