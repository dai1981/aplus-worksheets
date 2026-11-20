# -*- coding: utf-8 -*-
"""
South Africa Grade 8 Maths (CAPS): Exponents: Laws of Exponents (Grade 8: 1.3 Exponents)
  python3 tools/gen_za_maths_g8_exponents.py
Multiplying and dividing powers, a power of a power, zero exponents, evaluating powers and laws of exponents with
letters (UK Year 8 and Australia Year 8 makers).
Wrong answers come from real mistakes: multiplying the exponents when multiplying powers, multiplying the bases, and
thinking a⁰ = 0.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y8_indices as uki
adopt(uki)
if isinstance(getattr(uki, 'R', None), random.Random): uki.R = random.Random(808040)
import gen_au_maths_y8_index_laws as aui
adopt(aui)
if isinstance(getattr(aui, 'R', None), random.Random): aui.R = random.Random(808041)
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
        ("Multiply powers", [("collect", uki.one_mul, 10), ("collect", aui.one_mul, 10)]),
        ("Divide powers", [("collect", uki.one_div, 10), ("collect", aui.one_div, 10)]),
        ("Power of a power", [("collect", uki.one_pp, 10), ("collect", aui.one_pp, 10)]),
        ("Evaluate", [("collect", uki.one_eval, 10), ("collect", aui.one_eval, 10)]),
        ("Laws with letters", [("collect", uki.one_alg, 20)]),
    ], 80804)
    finish(sets, R)
    body = lesson('<ul><li>Multiply powers with the same base: add the exponents. 2³ × 2⁴ = 2⁷.</li><li>Divide: subtract the exponents. 5⁶ ÷ 5² = 5⁴.</li><li>Power of a power: multiply the exponents. (3²)³ = 3⁶.</li><li>Any number (not 0) to the power 0 is 1: 7⁰ = 1.</li></ul>',
        [example("x⁵ × x³ ÷ x²", ["x⁸ ÷ x²"], "x⁶")],
        [['Multiplying the exponents', 'When multiplying powers, add them.'], ['Multiplying the bases', '2³ × 2⁴ = 2⁷, not 4⁷.'], ['a⁰ = 0', 'a⁰ = 1.']])
    faq = [('What does CAPS Grade 8 say about exponents?', 'Use the laws of exponents: multiplying and dividing powers with the same base, a power of a power, and the zero exponent.'), ('What is 10⁰?', '1.'), ('Is 2³ × 3² = 6⁵?', 'No: the bases are different.'), ('What is (2x)³?', '8x³.')]
    make('exponents', 4, 'Numbers, Operations and Relationships', 'Grade 8: 1.3 Exponents',
         'Compare and represent integers in exponential form; compare and represent numbers in scientific notation; extend the general laws of exponents to include: a^m × a^n = a^(m+n), a^m ÷ a^n = a^(m−n) if m > n, (a^m)^n = a^(m×n), (a × t)^n = a^n × t^n, a^0 = 1.',
         'Exponents: Laws of Exponents', 'Exponents',
         'Free CAPS Grade 8 exponents worksheets: multiplying and dividing powers, power of a power, zero exponents and laws with letters. 100 questions with memos.',
         'Multiply: add the exponents.', 'a⁰ = 1.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
