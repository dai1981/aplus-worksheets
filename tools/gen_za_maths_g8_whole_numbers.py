# -*- coding: utf-8 -*-
"""
South Africa Grade 8 Maths (CAPS): Whole Numbers: Prime Factors, HCF and LCM of Three Numbers, and Ratio (Grade 8: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g8_whole_numbers.py
Prime factorisation, the HCF and the LCM, using prime factors, ratio sharing and direct and inverse proportion (UK
Year 7 and Year 8 and Australia Year 7 makers).
Wrong answers come from real mistakes: leaving composite factors, mixing up the HCF and the LCM, and treating an
inverse proportion as direct.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y7_factors_multiples_and_primes as ukf
adopt(ukf)
if isinstance(getattr(ukf, 'R', None), random.Random): ukf.R = random.Random(808010)
import gen_au_maths_y7_prime_factorisation_and_index_notation as auf
adopt(auf)
if isinstance(getattr(auf, 'R', None), random.Random): auf.R = random.Random(808011)
import gen_uk_maths_y8_direct_and_inverse_proportion as ukd
adopt(ukd)
if isinstance(getattr(ukd, 'R', None), random.Random): ukd.R = random.Random(808012)
import gen_au_maths_y7_ratios as aur
adopt(aur)
if isinstance(getattr(aur, 'R', None), random.Random): aur.R = random.Random(808013)
za_common.GRADE = "grade-8"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok8(it):
    """Grade 8: no trigonometry, quadratic formula or surds beyond square roots"""
    return not _re.search(r"\b(sin|cos|tan)\b|quadratic|discriminant|imperial|\bmiles?\b", _txt(it))



def build():
    sets, R = build_sets([
        ("Prime factorisation", [("collect", ukf.one_pf, 10), ("collect", auf.one_pf, 10)]),
        ("HCF and LCM", [("collect", ukf.one_hcf, 10), ("collect", ukf.one_lcm, 10)]),
        ("Using prime factors", [("collect", ukf.one_pf_use, 10), ("collect", auf.one_hcf_lcm, 10)]),
        ("Ratio", [("collect", aur.one_share, 10), ("collect", aur.one_part, 10)]),
        ("Direct and inverse proportion", [("collect", ukd.one_inverse, 10), ("collect", ukd.one_which, 10)]),
    ], 80801)
    finish(sets, R)
    body = lesson('<ul><li>Write each number as a product of primes: 72 = 2³ × 3².</li><li>HCF: the primes the numbers share, with the smallest powers. LCM: every prime, with the biggest powers.</li><li>Ratio: add the parts, find one part, then multiply.</li><li>Direct proportion: both go up together. Inverse proportion: one goes up as the other goes down.</li></ul>',
        [example("HCF and LCM of 12, 18 and 30", ["12 = 2² × 3", "18 = 2 × 3²", "30 = 2 × 3 × 5"], "HCF 6, LCM 180")],
        [['Composite factors', 'Keep breaking down until all factors are prime.'], ['HCF or LCM?', 'HCF is small; LCM is big.'], ['Inverse as direct', 'More workers take less time.']])
    faq = [('What does CAPS Grade 8 say about whole numbers?', 'Use prime factorisation to find the LCM and HCF of numbers, and solve problems involving ratio, rate and direct and indirect proportion.'), ('What is indirect proportion?', 'When one quantity doubles, the other halves.'), ('Is 1 a prime number?', 'No.'), ('How do I find the LCM of 3 numbers?', 'Use every prime factor with its highest power.')]
    make('whole-numbers', 1, 'Numbers, Operations and Relationships', 'Grade 8: 1.1 Whole numbers',
         'Use prime factorisation of numbers to find LCM and HCF; solve problems in contexts involving ratio, rate and direct and indirect proportion.',
         'Whole Numbers: Prime Factors, HCF and LCM of Three Numbers, and Ratio', 'Whole Numbers',
         'Free CAPS Grade 8 whole numbers worksheets: prime factorisation, HCF and LCM, ratio and direct and inverse proportion. 100 questions with memos.',
         'Prime factors give the HCF and the LCM.', 'Inverse proportion: one up, the other down.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
