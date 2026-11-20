# -*- coding: utf-8 -*-
"""
South Africa Grade 8 Maths (CAPS): Scientific Notation: Large and Small Numbers (Grade 8: 1.3 Exponents)
  python3 tools/gen_za_maths_g8_scientific_notation.py
Writing large and small numbers in scientific notation, changing back, ordering and calculating with scientific
notation (UK Year 8 makers; scientific notation is what UK books call standard form).
Wrong answers come from real mistakes: a first number of 10 or more, counting the zeros instead of the places, and
getting the sign of the exponent wrong for small numbers.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y8_standard_form as uks
adopt(uks)
if isinstance(getattr(uks, 'R', None), random.Random): uks.R = random.Random(808050)
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
        ("Large numbers", [("collect", uks.one_big, 20)]),
        ("Small numbers", [("collect", uks.one_small, 20)]),
        ("Change back", [("collect", uks.one_back, 20)]),
        ("Order numbers", [("collect", uks.one_order, 20)]),
        ("Multiply and divide", [("collect", uks.one_md, 20)]),
    ], 80805)
    finish(sets, R)
    body = lesson('<ul><li>Scientific notation: a × 10ⁿ, where 1 ≤ a &lt; 10.</li><li>Large numbers: 45 000 = 4,5 × 10⁴ (the comma moves 4 places).</li><li>Small numbers: 0,0032 = 3,2 × 10⁻³.</li><li>To compare, look at the powers of 10 first.</li></ul>',
        [example("(3 × 10⁴) × (2 × 10³)", ["3 × 2 = 6", "10⁴ × 10³ = 10⁷"], "6 × 10⁷")],
        [['The first number too big', '45 × 10³ is not in scientific notation.'], ['Counting zeros', 'Count the places the comma moves.'], ['The sign', 'Small numbers have a negative exponent.']])
    faq = [('What does CAPS Grade 8 say about scientific notation?', 'Compare and represent numbers in scientific notation, including very large and very small numbers.'), ('What is the distance to the Sun?', 'About 1,5 × 10⁸ km.'), ('Is 0,5 × 10³ correct?', 'No: it should be 5 × 10².'), ('Why use scientific notation?', 'It is a short way to write very big and very small numbers.')]
    make('scientific-notation', 5, 'Numbers, Operations and Relationships', 'Grade 8: 1.3 Exponents',
         'Compare and represent numbers in scientific notation; calculate using numbers in scientific notation, including very large and very small numbers.',
         'Scientific Notation: Large and Small Numbers', 'Scientific Notation',
         'Free CAPS Grade 8 scientific notation worksheets: writing large and small numbers, changing back, ordering and calculating. 100 questions with memos.',
         'a × 10ⁿ with 1 ≤ a &lt; 10.', 'Small numbers: negative exponent.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
