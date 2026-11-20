# -*- coding: utf-8 -*-
"""
South Africa Grade 7 Maths (CAPS): Common Fractions: Adding, Subtracting and Mixed Numbers (Grade 7: 1.4 Common fractions)
  python3 tools/gen_za_maths_g7_fractions.py
Adding and subtracting fractions with the same, related and different denominators and mixed numbers, and problems
(UK Year 7 and Australia Year 7 makers).
Wrong answers come from real mistakes: adding the denominators, changing only the denominator, and forgetting to
regroup a whole in a mixed number.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y7_adding_and_subtracting_fractions as ukf
adopt(ukf)
if isinstance(getattr(ukf, 'R', None), random.Random): ukf.R = random.Random(807080)
import gen_au_maths_y7_adding_and_subtracting_fractions as auf
adopt(auf)
if isinstance(getattr(auf, 'R', None), random.Random): auf.R = random.Random(807081)
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
        ("Same denominators", [("collect", ukf.one_same, 10), ("collect", auf.one_same, 10)]),
        ("Related denominators", [("collect", ukf.one_related, 10), ("collect", auf.one_related, 10)]),
        ("Different denominators", [("collect", ukf.one_any, 10), ("collect", auf.one_any, 10)]),
        ("Mixed numbers", [("collect", ukf.one_mixed, 10), ("collect", auf.one_mixed, 10)]),
        ("Fraction problems", [("run", ukf.problems, (), 10, ok7), ("run", auf.problems, (), 10, ok7)]),
    ], 80708)
    finish(sets, R)
    body = lesson("<ul><li>To add or subtract fractions, give them a common denominator (use the LCM).</li><li><span class='fr'><span class='fn'>2</span><span class='fd'>3</span></span> + <span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span> = <span class='fr'><span class='fn'>8</span><span class='fd'>12</span></span> + <span class='fr'><span class='fn'>9</span><span class='fd'>12</span></span> = <span class='fr'><span class='fn'>17</span><span class='fd'>12</span></span> = 1 <span class='fr'><span class='fn'>5</span><span class='fd'>12</span></span>.</li><li>For mixed numbers, add the wholes and the fractions, then regroup.</li><li>Write the answer in simplest form.</li></ul>",
        [example("3 <span class='fr'><span class='fn'>1</span><span class='fd'>4</span></span> − 1 <span class='fr'><span class='fn'>2</span><span class='fd'>3</span></span>", ["2 <span class='fr'><span class='fn'>15</span><span class='fd'>12</span></span> − 1 <span class='fr'><span class='fn'>8</span><span class='fd'>12</span></span>"], "1 <span class='fr'><span class='fn'>7</span><span class='fd'>12</span></span>")],
        [['Adding denominators', 'Keep the common denominator.'], ['Changing the bottom only', 'Multiply the top too.'], ['Not regrouping', 'Borrow a whole when the fraction is too small.']])
    faq = [('What does CAPS Grade 7 say about fractions?', 'Add and subtract common fractions, including mixed numbers, and find fractions of whole numbers.'), ('What is 1/2 + 1/3?', '5/6.'), ('Do I use the LCM?', 'Yes, it gives the smallest common denominator.'), ('Should I simplify?', 'Yes.')]
    make('common-fractions', 8, 'Numbers, Operations and Relationships', 'Grade 7: 1.4 Common fractions',
         'Add and subtract common fractions, including mixed numbers; find fractions of whole numbers; convert mixed numbers to common fractions in order to perform calculations with them; use knowledge of multiples and factors to write fractions in the simplest form before or after calculations.',
         'Common Fractions: Adding, Subtracting and Mixed Numbers', 'Common Fractions',
         'Free CAPS Grade 7 fractions worksheets: adding and subtracting fractions with same, related and different denominators and mixed numbers. 100 questions with memos.',
         'Common denominator first.', 'Regroup and simplify.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
