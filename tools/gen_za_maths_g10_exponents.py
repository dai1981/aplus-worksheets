# -*- coding: utf-8 -*-
"""
South Africa Grade 10 Maths (CAPS): Exponents and Exponential Equations (Grade 10: Exponents)
  python3 tools/gen_za_maths_g10_exponents.py
Laws of exponents with integral exponents, negative and zero exponents, simplifying with letters, and exponential
equations (UK Year 8, Australia Year 8 and Singapore Secondary 3 makers).
Wrong answers come from real mistakes: multiplying the bases, thinking a negative exponent gives a negative answer,
and equating exponents before the bases are the same.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y8_indices as uki
adopt(uki)
if isinstance(getattr(uki, 'R', None), random.Random): uki.R = random.Random(810040)
import gen_au_maths_y8_index_laws as aui
adopt(aui)
if isinstance(getattr(aui, 'R', None), random.Random): aui.R = random.Random(810041)
import gen_sg_maths_s3_indices as sgi
adopt(sgi)
if isinstance(getattr(sgi, 'R', None), random.Random): sgi.R = random.Random(810042)
za_common.GRADE = "grade-10"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok10(it):
    """Grade 10: no complex numbers, logarithms, radians, sine or cosine rules, or calculus"""
    return not _re.search(r"imaginary|complex|\blog|radian|\bπ/|sine rule|cosine rule|law of (sines|cosines)|derivative|imperial|\bmiles?\b|\bfeet\b|\binch", _txt(it))



def build():
    sets, R = build_sets([
        ("Laws of exponents", [("collect", uki.one_mul, 7), ("collect", uki.one_div, 7), ("collect", aui.one_pp, 6)]),
        ("Negative and zero exponents", [("collect", uki.one_neg, 20)]),
        ("Simplify with letters", [("collect", uki.one_alg, 10), ("collect", sgi.one_alg, 10)]),
        ("Evaluate", [("collect", uki.one_eval, 10), ("collect", aui.one_eval, 10)]),
        ("Exponential equations", [("collect", sgi.one_eq, 20)]),
    ], 81004)
    finish(sets, R)
    body = lesson("<ul><li>aᵐ × aⁿ = aᵐ⁺ⁿ, aᵐ ÷ aⁿ = aᵐ⁻ⁿ, (aᵐ)ⁿ = aᵐⁿ, (ab)ⁿ = aⁿbⁿ.</li><li>a⁰ = 1 and a⁻ⁿ = <span class='fr'><span class='fn'>1</span><span class='fd'>aⁿ</span></span>.</li><li>Write numbers as powers of primes to simplify: 8 = 2³, 27 = 3³.</li><li>Exponential equations: make the bases the same, then equate the exponents.</li></ul>",
        [example("3ˣ⁺¹ = 81", ["81 = 3⁴", "x + 1 = 4"], "x = 3")],
        [['Multiplying the bases', '2³ × 2⁴ = 2⁷.'], ['Negative means negative', '2⁻² = ¼.'], ['Different bases', 'Change to the same base first.']])
    faq = [('What does CAPS Grade 10 say about exponents?', 'Revise the laws of exponents and use them to simplify expressions and solve simple exponential equations.'), ('What is 4⁻½?', 'That is a rational exponent (Grade 11): ½.'), ('What is (2a³)²?', '4a⁶.'), ('How do I solve 2ˣ = ⅛?', '⅛ = 2⁻³, so x = −3.')]
    make('exponents-and-exponential-equations', 4, 'Algebra and Number Patterns', 'Grade 10: Exponents',
         'Revise laws of exponents learnt in Grade 9 where x, y > 0 and m, n ∈ ℤ: xⁿ × xᵐ = xⁿ⁺ᵐ, xⁿ ÷ xᵐ = xⁿ⁻ᵐ, (xⁿ)ᵐ = xⁿᵐ, (xy)ⁿ = xⁿyⁿ; also by definition x⁰ = 1 and x⁻ⁿ = 1/xⁿ; use the laws of exponents to simplify expressions and solve easy exponential equations.',
         'Exponents and Exponential Equations', 'Exponents',
         'Free CAPS Grade 10 exponents worksheets: laws of exponents, negative and zero exponents, simplifying and exponential equations. 100 questions with memos.',
         'Same base: equate the exponents.', 'a⁻ⁿ = 1/aⁿ.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
