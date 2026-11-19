# -*- coding: utf-8 -*-
"""
Philippines Grade 1 Math (MATATAG): Adding Numbers up to 100 without Regrouping (Grade 1: Number and Algebra)
  python3 tools/gen_ph_math_g1_add_100.py
Adding 2-digit and 1-digit numbers and 2-digit and 2-digit numbers without regrouping, adding tens, adding in
expanded form, and problems (own makers and US Grade 1 makers).
Wrong answers come from real mistakes: adding a ones digit to the tens, adding all the digits together, and
forgetting to add the tens.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g1_add_100 as usa
adopt(usa)
if hasattr(usa, 'R'): usa.R = random.Random(701140)
ph_common.GRADE = "grade-1"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


import re as _re


def _nums(it):
    t = _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"])
    t = _re.sub(r"<[^>]+>", " ", t)
    return [int(x.replace(",", "")) for x in _re.findall(r"\d[\d,]*", t)]


def le100(it):
    return all(n <= 100 for n in _nums(it))


def le20(it):
    return all(n <= 20 for n in _nums(it))


def noreg_pair(r, two):
    for _ in range(100):
        a = r.randint(10, 89)
        b = r.randint(10, 89) if two else r.randint(1, 9)
        if a % 10 + b % 10 <= 9 and a + b <= 99 and (not two or b % 10 or a % 10):
            return a, b
    raise AssertionError


def one_add(r):
    two = r.random() < 0.6
    a, b = noreg_pair(r, two)
    s = a + b
    wr = [s + 10, s - 10 if s - 10 > 0 else s + 20, a + b % 10 if two else s + 1, (a // 10 + b % 10) * 10 + a % 10 + b // 10 if two else s - 1]
    return mcq("<b>%d + %d = ☐</b>" % (a, b), s, wr, "Add the ones: %d + %d = %d. Add the tens: %d + %d = %d tens. <b>%d</b>." % (a % 10, b % 10, a % 10 + b % 10, a // 10, b // 10, a // 10 + b // 10, s))


def one_expand(r):
    a, b = noreg_pair(r, True)
    s = a + b
    q = "<b>%d + %d</b> = %d + %d + %d + %d = ☐" % (a, b, a // 10 * 10, a % 10, b // 10 * 10, b % 10)
    return mcq(q, s, [s + 10, a // 10 * 10 + b // 10 * 10, a % 10 + b % 10 + a // 10 + b // 10],
               "Tens: %d + %d = %d. Ones: %d + %d = %d. %d + %d = <b>%d</b>." % (a // 10 * 10, b // 10 * 10, (a // 10 + b // 10) * 10, a % 10, b % 10, a % 10 + b % 10, (a // 10 + b // 10) * 10, a % 10 + b % 10, s))


ITEMS = [("mangoes", "picks"), ("shells", "finds"), ("pandesal", "buys"), ("stickers", "gets"), ("marbles", "wins"), ("seeds", "plants"), ("bananas", "picks"), ("eggs", "collects")]


def one_add_story(r):
    k = Kid(r).next()
    what, verb = r.choice(ITEMS)
    a, b = noreg_pair(r, r.random() < 0.5)
    q = "%s has %d %s. %s %s %d more. How many %s does %s have now?" % (k["n"], a, what, k["He"], verb, b, what, k["he"])
    return mcq(q, a + b, [a + b + 10, a - b if a > b else a + b + 1, a + b - 1], "%d + %d = <b>%d</b> %s." % (a, b, a + b, what))


def build():
    sets, R = build_sets([
        ("Add tens", [("run", usa.set_tens, ("rnd", "seen"), 20, le100)]),
        ("Add 2-digit and 1-digit numbers", [("run", usa.set_ones, ("rnd", "seen"), 20, le100)]),
        ("Add 2-digit numbers", [("collect", uniq(one_add), 20)]),
        ("Add in expanded form", [("collect", uniq(one_expand), 20)]),
        ("Addition stories", [("collect", uniq(one_add_story), 20)]),
    ], 70114)
    finish(sets, R)
    body = lesson('<ul><li>Add the <b>ones</b> to the ones and the <b>tens</b> to the tens.</li><li>34 + 5: 4 + 5 = 9 ones, 3 tens. The answer is 39.</li><li>34 + 25: 4 + 5 = 9 ones, 3 + 2 = 5 tens. The answer is 59.</li><li>Expanded form: 34 + 25 = 30 + 4 + 20 + 5 = 50 + 9 = 59.</li></ul>',
        [example("42 + 36", ["ones: 2 + 6 = 8", "tens: 4 + 3 = 7"], "78")],
        [['Ones added to tens', 'Line up ones with ones.'], ['Adding all the digits', '34 + 25 is not 3 + 4 + 2 + 5.'], ['Forgetting the tens', 'Add the tens too.']])
    faq = [('What does MATATAG Math 1 ask about adding to 100?', 'Add numbers by expressing addends as tens and ones, add numbers with sums up to 100 without regrouping (2-digit and 1-digit, 2-digit and 2-digit), and solve problems.'), ('What is regrouping?', 'Changing 10 ones into 1 ten. Grade 1 sums do not need it.'), ('Why use expanded form?', 'It shows tens and ones clearly.'), ('What is 50 + 30?', '80.')]
    make('adding-within-100-without-regrouping', 14, 'Number and Algebra', 'Grade 1: Number and Algebra',
         'Add numbers by expressing addends as tens and ones (expanded form); add numbers with sums up to 100 without regrouping, using a variety of concrete and pictorial models for: a. 2-digit and 1-digit numbers, and b. 2-digit and 2-digit numbers; solve problems (given orally or in pictures) involving addition with sums up to 100 without regrouping.',
         'Adding Numbers up to 100 without Regrouping', 'Adding within 100',
         'Free Grade 1 worksheets on adding within 100 without regrouping for the DepEd MATATAG curriculum: tens and ones, expanded form and word problems. 100 questions with answers.',
         'Ones with ones, tens with tens.', '34 + 25 = 30 + 20 + 4 + 5 = 59.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
