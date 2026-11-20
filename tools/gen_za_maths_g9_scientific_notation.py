# -*- coding: utf-8 -*-
"""
South Africa Grade 9 Maths (CAPS): Scientific Notation: Calculating with Large and Small Numbers (Grade 9: 1.3 Exponents)
  python3 tools/gen_za_maths_g9_scientific_notation.py
Writing large and small numbers in scientific notation, changing back, ordering, and multiplying and dividing in
scientific notation (Singapore Secondary 3 and UK Year 8 makers).
Wrong answers come from real mistakes: a first number of 10 or more, getting the sign of the exponent wrong for small
numbers, and adding the exponents when dividing.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_sg_maths_s3_standard_form as sgs
adopt(sgs)
if isinstance(getattr(sgs, 'R', None), random.Random): sgs.R = random.Random(809040)
import gen_uk_maths_y8_standard_form as uks
adopt(uks)
if isinstance(getattr(uks, 'R', None), random.Random): uks.R = random.Random(809041)
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
        ("Large numbers", [("collect", sgs.one_big, 20)]),
        ("Small numbers", [("collect", sgs.one_small, 20)]),
        ("Change back", [("collect", sgs.one_back, 20)]),
        ("Order numbers", [("collect", sgs.one_order, 20)]),
        ("Multiply and divide", [("collect", sgs.one_md, 10), ("collect", uks.one_md, 10)]),
    ], 80904)
    finish(sets, R)
    body = lesson('<ul><li>Scientific notation: a × 10ⁿ with 1 ≤ a &lt; 10.</li><li>Large numbers have a positive exponent; small numbers a negative one.</li><li>Multiply: multiply the front numbers and add the exponents.</li><li>Divide: divide the front numbers and subtract the exponents. Adjust if the front number is not between 1 and 10.</li></ul>',
        [example("(6 × 10⁸) ÷ (3 × 10⁻²)", ["6 ÷ 3 = 2", "8 − (−2) = 10"], "2 × 10¹⁰")],
        [['Front number too big', 'Adjust 19,2 × 10⁸ to 1,92 × 10⁹.'], ['The sign', '0,005 = 5 × 10⁻³.'], ['Adding when dividing', 'Subtract the exponents.']])
    faq = [('What does CAPS Grade 9 say about scientific notation?', 'Compare and represent numbers in scientific notation, and calculate using numbers in scientific notation, including very large and very small numbers.'), ('What is the mass of an atom?', 'Very small, like 10⁻²⁶ kg.'), ('Is 0,8 × 10⁵ correct?', 'No: 8 × 10⁴.'), ('Why use it?', 'To work with very big and very small numbers.')]
    make('scientific-notation', 4, 'Numbers, Operations and Relationships', 'Grade 9: 1.3 Exponents',
         'Compare and represent numbers in scientific notation, including negative exponents; calculate using numbers in scientific notation, including very large and very small numbers.',
         'Scientific Notation: Calculating with Large and Small Numbers', 'Scientific Notation',
         'Free CAPS Grade 9 scientific notation worksheets: large and small numbers, ordering, multiplying and dividing. 100 questions with memos.',
         'a × 10ⁿ with 1 ≤ a &lt; 10.', 'Divide: subtract the exponents.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
