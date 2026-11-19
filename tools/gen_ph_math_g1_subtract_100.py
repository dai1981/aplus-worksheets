# -*- coding: utf-8 -*-
"""
Philippines Grade 1 Math (MATATAG): Subtracting Numbers up to 100 without Regrouping (Grade 1: Number and Algebra)
  python3 tools/gen_ph_math_g1_subtract_100.py
Subtracting tens, 2-digit minus 1-digit and 2-digit minus 2-digit numbers without regrouping, subtracting in
expanded form, and stories (US Grade 1 maker and own makers).
Wrong answers come from real mistakes: subtracting a ones digit from the tens, adding instead of subtracting, and
forgetting to subtract the tens.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g1_subtract_tens as ust
adopt(ust)
if hasattr(ust, 'R'): ust.R = random.Random(701180)
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


def nr_sub(r, two):
    for _ in range(100):
        a = r.randint(11, 99)
        b = r.randint(10, a) if two else r.randint(1, 9)
        if a % 10 >= b % 10 and a != b and a - b > 0:
            return a, b
    raise AssertionError


def one_sub1(r):
    return one_sub(r, False)


def one_sub2(r):
    return one_sub(r, True)


def one_sub(r, two=True):
    a, b = nr_sub(r, two)
    d = a - b
    wr = [d + 10, a + b if a + b <= 100 else d - 10, d + 1, (a // 10 - b // 10) * 10 + (a % 10 + b % 10) % 10 if two else d - 1]
    return mcq("<b>%d − %d = ☐</b>" % (a, b), d, [x for x in wr if x >= 0], "Ones: %d − %d = %d. Tens: %d − %d = %d tens. <b>%d</b>." % (a % 10, b % 10, a % 10 - b % 10, a // 10, b // 10, a // 10 - b // 10, d), allow_zero=True)


def one_sub_exp(r):
    a, b = nr_sub(r, True)
    d = a - b
    q = "<b>%d − %d</b>: (%d − %d) + (%d − %d) = ☐" % (a, b, a // 10 * 10, b // 10 * 10, a % 10, b % 10)
    return mcq(q, d, [d + 10, a // 10 * 10 - b // 10 * 10 if a // 10 * 10 - b // 10 * 10 != d else d + 1, a % 10 - b % 10 + 10 if a % 10 - b % 10 + 10 != d else d + 2],
               "Tens: %d − %d = %d. Ones: %d − %d = %d. %d + %d = <b>%d</b>." % (a // 10 * 10, b // 10 * 10, (a // 10 - b // 10) * 10, a % 10, b % 10, a % 10 - b % 10, (a // 10 - b // 10) * 10, a % 10 - b % 10, d), allow_zero=True)


THING = [("mangoes", "eats"), ("pesos", "spends"), ("pages", "reads"), ("stickers", "gives away"), ("shells", "loses"), ("eggs", "uses")]


def one_sub_story(r):
    k = Kid(r).next()
    what, verb = r.choice(THING)
    a, b = nr_sub(r, r.random() < 0.5)
    q = "%s has %d %s. %s %s %d. How many %s are left?" % (k["n"], a, what, k["He"], verb, b, what)
    return mcq(q, a - b, [a + b if a + b <= 100 else a - b + 10, a - b + 10, a - b - 1 if a - b > 1 else a - b + 2], "%d − %d = <b>%d</b>." % (a, b, a - b), allow_zero=True)


def build():
    sets, R = build_sets([
        ("Subtract tens", [("run", ust.set_rods, ("rnd",), 10, le100), ("run", ust.set_facts, ("rnd",), 10, le100)]),
        ("2-digit minus 1-digit", [("collect", uniq(one_sub1), 20)]),
        ("2-digit minus 2-digit", [("collect", uniq(one_sub2), 20)]),
        ("Subtract in expanded form", [("collect", uniq(one_sub_exp), 20)]),
        ("Subtraction stories", [("collect", uniq(one_sub_story), 20)]),
    ], 70118)
    finish(sets, R)
    body = lesson('<ul><li>Subtract the <b>ones</b> from the ones and the <b>tens</b> from the tens.</li><li>48 − 5: 8 − 5 = 3 ones, 4 tens. The answer is 43.</li><li>68 − 25: 8 − 5 = 3 ones, 6 − 2 = 4 tens. The answer is 43.</li><li>Expanded form: 68 − 25 = (60 − 20) + (8 − 5) = 40 + 3 = 43.</li></ul>',
        [example("79 − 34", ["ones: 9 − 4 = 5", "tens: 7 − 3 = 4"], "45")],
        [['Ones from tens', 'Line up the ones with the ones.'], ['Adding', '“Left” means subtract.'], ['Forgetting the tens', 'Subtract the tens too.']])
    faq = [('What does MATATAG Math 1 ask about subtracting to 100?', 'Subtract numbers where both numbers are less than 100 without regrouping (2-digit minus 1-digit and 2-digit minus 2-digit), and subtract numbers by expressing them as tens and ones.'), ('What is 70 − 30?', '40.'), ('How can I check a subtraction?', 'Add the answer to the number you took away.'), ('Why no regrouping?', 'Grade 1 learners subtract tens and ones separately first.')]
    make('subtracting-within-100-without-regrouping', 18, 'Number and Algebra', 'Grade 1: Number and Algebra',
         'Subtract numbers where both numbers are less than 100 using concrete and pictorial models, without regrouping: a. 2-digit minus 1-digit numbers, and b. 2-digit minus 2-digit numbers; subtract numbers by expressing minuends and subtrahends as tens and ones (expanded form), without regrouping.',
         'Subtracting Numbers up to 100 without Regrouping', 'Subtracting within 100',
         'Free Grade 1 worksheets on subtracting within 100 without regrouping for the DepEd MATATAG curriculum: tens and ones, expanded form and stories. 100 questions with answers.',
         'Ones from ones, tens from tens.', 'Check: answer + number taken away = start.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
