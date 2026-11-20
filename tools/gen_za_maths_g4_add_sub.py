# -*- coding: utf-8 -*-
"""
South Africa Grade 4 Maths (CAPS): Addition and Subtraction of 4-Digit Numbers (Grade 4: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g4_add_sub.py
Adding and subtracting whole numbers of at least 4 digits in columns, with carrying and borrowing, checking with the
inverse operation, and word problems (UK Year 4 makers with South African names and numbers).
Wrong answers come from real mistakes: forgetting to carry, subtracting the smaller digit from the bigger one in
every column, and misplacing digits in the columns.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_uk_maths_y4_column_add_sub as ukc
adopt(ukc)
if hasattr(ukc, 'R'): ukc.R = random.Random(804030)
za_common.GRADE = "grade-4"


import re as _re


def _nums(it):
    t = _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"]
    t = _re.sub(r"<[^>]+>", " ", t)
    return [int(x.replace(",", "").replace("\u00a0", "")) for x in _re.findall(r"(?<![\d.])\d[\d,\u00a0]*(?![.\d])", t) if x.replace(",", "").replace("\u00a0", "").isdigit()]


def le10000(it):
    return all(n <= 10000 for n in _nums(it))


def le100k(it):
    return all(n <= 99999 for n in _nums(it))


def den12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " ".join(it["c"]))]
    return all(d <= 12 for d in ds)


def den8(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " ".join(it["c"]))]
    return all(d <= 8 for d in ds)



def build():
    sets, R = build_sets([
        ("Add 4-digit numbers", [("run", ukc.set_add_easy, ("rnd", "seen"), 20, le100k)]),
        ("Add with carrying", [("run", ukc.set_add_hard, ("rnd", "seen"), 20, le100k)]),
        ("Subtract 4-digit numbers", [("run", ukc.set_sub, ("rnd", "seen"), 20, le100k)]),
        ("Check with the inverse", [("run", ukc.set_check, ("rnd",), 20, le100k)]),
        ("Addition and subtraction problems", [("run", ukc.set_story, ("rnd",), 20, le100k)]),
    ], 80403)
    finish(sets, R)
    body = lesson('<ul><li>Write the numbers in columns: units under units, tens under tens, and so on.</li><li>Add or subtract from the units column to the left.</li><li>When a column adds up to 10 or more, carry 1 to the next column.</li><li>When the top digit is too small, borrow 1 from the next column (1 ten = 10 units).</li><li>Check: subtraction undoes addition. 6 352 − 2 817 = 3 535 because 3 535 + 2 817 = 6 352.</li></ul>',
        [example("4 768 + 2 385", ["8 + 5 = 13, carry 1", "6 + 8 + 1 = 15, carry 1", "7 + 3 + 1 = 11, carry 1", "4 + 2 + 1 = 7"], "7 153")],
        [['Forgetting to carry', 'Write the carried 1 above the next column.'], ['Smaller from bigger', 'If the top digit is smaller, borrow.'], ['Wrong columns', 'Line up the units.']])
    faq = [('What does CAPS Grade 4 say about addition and subtraction?', 'Add and subtract whole numbers of at least 4 digits, using techniques such as building up and breaking down numbers, rounding off and compensating, and using inverse operations.'), ('How do I check a subtraction?', 'Add the answer to the number you subtracted.'), ('What is carrying?', 'Moving 10 units as 1 ten to the next column.'), ('Should learners estimate first?', 'Yes. It shows if an answer is far off.')]
    make('addition-and-subtraction', 3, 'Numbers, Operations and Relationships', 'Grade 4: 1.1 Whole numbers',
         'Add and subtract whole numbers of at least 4 digits; use techniques such as building up and breaking down numbers, rounding off and compensating, using a number line and using addition and subtraction as inverse operations.',
         'Addition and Subtraction of 4-Digit Numbers', 'Addition and Subtraction',
         'Free CAPS Grade 4 addition and subtraction worksheets: 4-digit column addition and subtraction with carrying and borrowing, checking and word problems. 100 questions with memos.',
         'Line up the columns and start with the units.', 'Check subtraction with addition.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
