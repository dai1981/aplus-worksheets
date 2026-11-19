# -*- coding: utf-8 -*-
"""
Philippines Grade 1 Math (MATATAG): Subtraction with Numbers up to 20 (Grade 1: Number and Algebra)
  python3 tools/gen_ph_math_g1_subtraction_20.py
Taking away with pictures, subtracting within 10 and 20, subtracting on a number line (Singapore Primary 1, US
Grade 1 and BC Grade 1 makers), and take-away and comparing stories (Ontario Grade 1 maker).
Wrong answers come from real mistakes: counting the starting number when counting back, subtracting the small
number from the big one in the wrong order, and adding instead.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_sg_maths_p1_add_sub_20 as sga
adopt(sga)
if hasattr(sga, 'R'): sga.R = random.Random(701160)
import gen_us_math_g1_add_sub_20 as usa
adopt(usa)
if hasattr(usa, 'R'): usa.R = random.Random(701161)
import gen_cabc_math_g1_add_sub as cba
adopt(cba)
if hasattr(cba, 'R'): cba.R = random.Random(701162)
import gen_caon_math_g1_word_problems as caw
adopt(caw)
if hasattr(caw, 'R'): caw.R = random.Random(701163)
ph_common.GRADE = "grade-1"


import re as _re


def _nums(it):
    t = _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"])
    t = _re.sub(r"<[^>]+>", " ", t)
    return [int(x.replace(",", "")) for x in _re.findall(r"\d[\d,]*", t)]


def le100(it):
    return all(n <= 100 for n in _nums(it))


def le20(it):
    return all(n <= 20 for n in _nums(it))


from ws_common import number_line, RED


def one_cb(r):
    a = r.randint(6, 20)
    b = r.randint(2, min(6, a - 1))
    nl = number_line(max(0, a - 10), max(10, a), jumps=[(a, a - b, RED)], label="number line counting back from %d" % a)
    return mcq(fig(nl) + "Start at %d. Count back %d. What is <b>%d − %d</b>?" % (a, b, a, b), a - b, [a - b + 1, a + b if a + b <= 20 else a - b - 1, a - b - 1 if a - b > 1 else a - b + 2],
               "Say %s. You land on <b>%d</b>. (Do not count the %d.)" % (", ".join(str(a - k - 1) for k in range(b)), a - b, a), allow_zero=True)


def build():
    sets, R = build_sets([
        ("Take away", [("run", sga.set_take_away, (), 20)]),
        ("Subtract within 10", [("run", usa.set_sub10, (usa.People,), 20)]),
        ("Subtract within 20", [("run", usa.set_sub20, (usa.People,), 20)]),
        ("Count back on a number line", [("run", cba.set_number_line, (), 6, lambda it: "−" in it["q"]), ("collect", one_cb, 14)]),
        ("Subtraction stories", [("run", caw.set_take, ("rnd", caw.People, lambda r: caw.Ctx(r, caw.JOIN), "seen"), 10, le20), ("run", caw.set_compare, ("rnd", caw.People, lambda r: caw.Ctx(r, caw.CMP), "seen"), 10, le20)]),
    ], 70116)
    finish(sets, R)
    body = lesson('<ul><li>Subtract means take away: 12 − 5 means start with 12 and take away 5.</li><li>Count back from the bigger number: 12 → 11, 10, 9, 8, 7.</li><li>Think addition: 5 + ☐ = 12, so 12 − 5 = 7.</li><li>Subtraction also compares: how many more, how many fewer.</li></ul>',
        [example("15 − 6", ["15 − 5 = 10", "10 − 1"], "9")],
        [['Counting the start', 'Start counting back from the next number.'], ['Wrong order', 'Start with the bigger number.'], ['Adding instead', '“Left” and “fewer” mean subtract.']])
    faq = [('What does MATATAG Math 1 ask about subtraction?', 'Illustrate subtraction involving numbers up to 20 using models, and solve subtraction problems where both numbers are less than 20.'), ('What words tell us to subtract?', 'Left, take away, fewer, how many more.'), ('Is 7 − 7 = 0?', 'Yes.'), ('How does addition help?', 'Every subtraction fact has a related addition fact.')]
    make('subtraction-within-20', 16, 'Number and Algebra', 'Grade 1: Number and Algebra',
         'Illustrate subtraction involving numbers up to 20 using a variety of concrete and pictorial models; solve subtraction problems (given orally or in pictures) where both numbers are less than 20.',
         'Subtraction with Numbers up to 20', 'Subtraction within 20',
         'Free Grade 1 subtraction worksheets for the DepEd MATATAG curriculum: take away with pictures, subtract within 20, number lines and stories. 100 questions with pictures and answers.',
         'Take away, or count back.', '12 − 5 = 7 because 5 + 7 = 12.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
