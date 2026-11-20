# -*- coding: utf-8 -*-
"""
South Africa Grade 9 Maths (CAPS): Exponents: Laws of Exponents and Negative Exponents (Grade 9: 1.3 Exponents)
  python3 tools/gen_za_maths_g9_exponents.py
Multiplying and dividing powers, powers of powers, negative and zero exponents, and laws of exponents with letters and
fractions (UK Year 8, Australia Year 8 and Singapore Secondary 3 makers).
Wrong answers come from real mistakes: thinking a negative exponent makes a negative number, multiplying the bases,
and forgetting to raise the number in front.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y8_indices as uki
adopt(uki)
if isinstance(getattr(uki, 'R', None), random.Random): uki.R = random.Random(809030)
import gen_au_maths_y8_index_laws as aui
adopt(aui)
if isinstance(getattr(aui, 'R', None), random.Random): aui.R = random.Random(809031)
import gen_sg_maths_s3_indices as sgi
adopt(sgi)
if isinstance(getattr(sgi, 'R', None), random.Random): sgi.R = random.Random(809032)
za_common.GRADE = "grade-9"


import re as _re
za_common.GBP_TO_RAND = True


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def ok9(it):
    """Grade 9: no trigonometry, quadratic formula, simultaneous equations or cones and spheres (Grade 10+)"""
    return not _re.search(r"\b(sin|cos|tan)\b|quadratic formula|discriminant|simultaneous|\bcone|\bsphere|imperial|\bmiles?\b", _txt(it))



def build():
    sets, R = build_sets([
        ("Multiply and divide powers", [("collect", uki.one_mul, 10), ("collect", aui.one_div, 10)]),
        ("Power of a power", [("collect", uki.one_pp, 10), ("collect", aui.one_pp, 10)]),
        ("Negative and zero exponents", [("collect", uki.one_neg, 20)]),
        ("Laws with letters", [("collect", uki.one_alg, 10), ("collect", sgi.one_alg, 10)]),
        ("Fractions and equations", [("collect", sgi.one_frac, 10), ("collect", sgi.one_eq, 10)]),
    ], 80903)
    finish(sets, R)
    body = lesson("<ul><li>aᵐ × aⁿ = aᵐ⁺ⁿ, aᵐ ÷ aⁿ = aᵐ⁻ⁿ, (aᵐ)ⁿ = aᵐⁿ.</li><li>a⁰ = 1.</li><li>A negative exponent means 1 over: a⁻ⁿ = <span class='fr'><span class='fn'>1</span><span class='fd'>aⁿ</span></span>. 2⁻³ = <span class='fr'><span class='fn'>1</span><span class='fd'>8</span></span>.</li><li>(3x²)³ = 27x⁶: raise the number and the letter.</li></ul>",
        [example("2x⁻² × 5x⁵", ["2 × 5 = 10", "x⁻²⁺⁵ = x³"], "10x³")],
        [['Negative means negative', '2⁻³ = 1/8, not −8.'], ['Multiplying the bases', '2³ × 2⁴ = 2⁷.'], ['The number in front', '(3x²)³ = 27x⁶.']])
    faq = [('What does CAPS Grade 9 say about exponents?', 'Use the laws of exponents, including the negative exponent a⁻ⁿ = 1/aⁿ, to simplify expressions and solve equations.'), ('What is 5⁻¹?', '1/5.'), ('What is (−2)⁴?', '16.'), ('How do I solve 2ˣ = 32?', '32 = 2⁵, so x = 5.')]
    make('exponents', 3, 'Numbers, Operations and Relationships', 'Grade 9: 1.3 Exponents',
         'Extend the general laws of exponents to include: a^m × a^n = a^(m+n), a^m ÷ a^n = a^(m−n), (a^m)^n = a^(m×n), (a × t)^n = a^n × t^n, a^0 = 1, and a^(−n) = 1/a^n; recognise and use the appropriate laws of operations using numbers involving exponents and square and cube roots.',
         'Exponents: Laws of Exponents and Negative Exponents', 'Exponents',
         'Free CAPS Grade 9 exponents worksheets: laws of exponents, negative and zero exponents and exponential equations. 100 questions with memos.',
         'a⁻ⁿ = 1 over aⁿ.', 'Raise the number and the letter.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
