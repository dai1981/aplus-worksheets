# -*- coding: utf-8 -*-
"""
South Africa Grade 7 Maths (CAPS): Integers: Ordering, Comparing, Adding and Subtracting (Grade 7: 1.3 Integers)
  python3 tools/gen_za_maths_g7_integers.py
Integers on a number line, ordering and comparing, adding and subtracting integers, and problems with temperatures
and money (UK Year 7, Australia Year 7 and BC Grade 7 makers).
Wrong answers come from real mistakes: thinking −8 is bigger than −3, moving the wrong way on the number line, and
subtracting a negative as if it were positive.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y7_place_value_and_ordering as ukp
adopt(ukp)
if isinstance(getattr(ukp, 'R', None), random.Random): ukp.R = random.Random(807070)
import gen_au_maths_y7_adding_and_subtracting_integers as aui
adopt(aui)
if isinstance(getattr(aui, 'R', None), random.Random): aui.R = random.Random(807071)
import gen_uk_maths_y7_negative_numbers as ukn
adopt(ukn)
if isinstance(getattr(ukn, 'R', None), random.Random): ukn.R = random.Random(807072)
import gen_cabc_math_g7_add_sub_integers as cbi
adopt(cbi)
if isinstance(getattr(cbi, 'R', None), random.Random): cbi.R = random.Random(807073)
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
        ("Order and compare integers", [("collect", ukp.one_neg_order, 10), ("collect", aui.one_order, 10)]),
        ("Integers on a number line", [("run", cbi.set_lines, ("rnd", cbi.People), 20, ok7)]),
        ("Add integers", [("collect", ukn.one_add, 10), ("collect", aui.one_add, 10)]),
        ("Subtract integers", [("collect", ukn.one_sub_pos, 7), ("collect", ukn.one_sub_neg, 7), ("collect", aui.one_sub_neg, 6)]),
        ("Integer problems", [("run", cbi.set_words, ("rnd", cbi.People), 10, ok7), ("collect", aui.one_mix, 10)]),
    ], 80707)
    finish(sets, R)
    body = lesson('<ul><li>Integers are whole numbers and their opposites: … −3, −2, −1, 0, 1, 2, 3 …</li><li>On a number line, numbers get bigger to the right: −3 &gt; −8.</li><li>Adding a negative number moves left: 5 + (−8) = −3.</li><li>Subtracting a negative number is the same as adding: 4 − (−6) = 4 + 6 = 10.</li></ul>',
        [example("−7 − (−12)", ["−7 + 12"], "5")],
        [['−8 &gt; −3', '−8 is further left, so it is smaller.'], ['The wrong way', 'Adding a negative moves left.'], ['− (−)', 'Subtracting a negative means add.']])
    faq = [('What does CAPS Grade 7 say about integers?', 'Count, order and compare integers, and add and subtract integers, using the number line and contexts like temperature and money.'), ('Is 0 an integer?', 'Yes, it is neither positive nor negative.'), ('What is −5 + 5?', '0; they are additive inverses.'), ('Where are integers used?', 'For temperatures, bank balances and heights above and below sea level.')]
    make('integers', 7, 'Numbers, Operations and Relationships', 'Grade 7: 1.3 Integers',
         'Count forwards and backwards in integers; order and compare integers; add and subtract integers; recognise and use commutative and associative properties of addition for integers; recognise and use additive inverses.',
         'Integers: Ordering, Comparing, Adding and Subtracting', 'Integers',
         'Free CAPS Grade 7 integers worksheets: ordering and comparing integers, the number line, adding and subtracting integers and problems. 100 questions with memos.',
         'Right is bigger on the number line.', 'Subtracting a negative: add.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
