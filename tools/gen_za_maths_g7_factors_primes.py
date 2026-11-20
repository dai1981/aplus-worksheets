# -*- coding: utf-8 -*-
"""
South Africa Grade 7 Maths (CAPS): Multiples, Factors, Prime Factorisation, HCF and LCM (Grade 7: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g7_factors_primes.py
Factors, multiples and primes, prime factorisation, index notation for prime factors, the HCF and the LCM, and
problems (UK Year 7 and Australia Year 7 makers).
Wrong answers come from real mistakes: calling 1 a prime number, leaving composite numbers in a factorisation, and
mixing up the HCF and the LCM.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y7_factors_multiples_and_primes as ukf
adopt(ukf)
if isinstance(getattr(ukf, 'R', None), random.Random): ukf.R = random.Random(807020)
import gen_au_maths_y7_prime_factorisation_and_index_notation as auf
adopt(auf)
if isinstance(getattr(auf, 'R', None), random.Random): auf.R = random.Random(807021)
za_common.GRADE = "grade-7"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok7(it):
    """Grade 7: no circles, pi or standard form (they come in Grade 8 and 9)"""
    return not _re.search(r"π|\bpi\b|circumference|radius|diameter|×\s?10<sup>|standard form|scientific notation", _txt(it))


def noneg(it):
    return ok7(it) and not _re.search(r"(?<![\d)] )[−-]\d", _txt(it))



def build():
    sets, R = build_sets([
        ("Factors, multiples and primes", [("collect", ukf.one_fmp, 20)]),
        ("Prime factorisation", [("collect", ukf.one_pf, 10), ("collect", auf.one_pf, 10)]),
        ("Index notation", [("collect", auf.one_index, 10), ("collect", auf.one_back, 10)]),
        ("HCF and LCM", [("collect", ukf.one_hcf, 7), ("collect", ukf.one_lcm, 7), ("collect", auf.one_hcf_lcm, 6)]),
        ("Using prime factors", [("collect", ukf.one_pf_use, 20)]),
    ], 80702)
    finish(sets, R)
    body = lesson('<ul><li>A prime number has exactly two factors: 1 and itself. 1 is not prime.</li><li>Prime factorisation writes a number as a product of primes: 360 = 2 × 2 × 2 × 3 × 3 × 5 = 2³ × 3² × 5.</li><li>HCF: multiply the prime factors the numbers share. LCM: use every prime factor the most times it appears.</li><li>A factor tree helps you find the prime factors.</li></ul>',
        [example("HCF and LCM of 24 and 36", ["24 = 2³ × 3", "36 = 2² × 3²"], "HCF 12, LCM 72")],
        [['1 is prime', '1 has only one factor.'], ['A composite factor left in', 'Keep breaking down until every factor is prime.'], ['HCF or LCM?', 'HCF ≤ the smaller number; LCM ≥ the bigger one.']])
    faq = [('What does CAPS Grade 7 say about factors?', 'Find multiples and factors, prime factors of numbers to at least 3 digits, and the LCM and HCF of numbers to at least 3 digits by inspection or factorisation.'), ('Is 51 prime?', 'No: 51 = 3 × 17.'), ('What is 2³?', '2 × 2 × 2 = 8.'), ('Where is the LCM used?', 'For common denominators.')]
    make('multiples-factors-and-prime-factorisation', 2, 'Numbers, Operations and Relationships', 'Grade 7: 1.1 Whole numbers',
         'Multiples and factors: list prime factors of numbers to at least 3-digit whole numbers; find the LCM and HCF of numbers to at least 3-digit whole numbers, by inspection or factorisation.',
         'Multiples, Factors, Prime Factorisation, HCF and LCM', 'Multiples, Factors and Primes',
         'Free CAPS Grade 7 worksheets: factors, multiples, primes, prime factorisation, index notation, HCF and LCM. 100 questions with memos.',
         'Break every number into primes.', 'HCF: shared primes. LCM: all primes, most times.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
