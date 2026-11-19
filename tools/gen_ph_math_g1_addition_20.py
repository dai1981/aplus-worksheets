# -*- coding: utf-8 -*-
"""
Philippines Grade 1 Math (MATATAG): Addition with Sums up to 20: Pictures, Number Lines and Properties (Grade 1: Number and Algebra)
  python3 tools/gen_ph_math_g1_addition_20.py
Adding with pictures and counters, adding within 10, making 10, doubles (Singapore Primary 1 and US Grade 1 makers),
and the properties of addition: adding 0 and changing the order of the addends (own maker).
Wrong answers come from real mistakes: counting the first number again when counting on, thinking 5 + 0 is 0, and
thinking 3 + 8 and 8 + 3 are different.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_sg_maths_p1_add_sub_20 as sga
adopt(sga)
if hasattr(sga, 'R'): sga.R = random.Random(701080)
import gen_us_math_g1_add_sub_20 as usa
adopt(usa)
if hasattr(usa, 'R'): usa.R = random.Random(701081)
import gen_us_math_g1_strategies as uss
adopt(uss)
if hasattr(uss, 'R'): uss.R = random.Random(701082)
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


def one_prop(r):
    a, b = r.randint(0, 12), r.randint(1, 8)
    kind = r.choice(["zero", "zero", "order", "order", "same"])
    if kind == "zero":
        if r.random() < 0.5:
            return mcq("What is <b>%d + 0</b>?" % a, a, [a + 1, 0, 10], "Adding 0 does not change the number: %d + 0 = <b>%d</b>." % (a, a), allow_zero=True)
        return mcq("<b>0 + ☐ = %d</b>. What number goes in the box?" % a, a, [0, a + 1, a - 1 if a > 1 else 10], "0 and %d make %d. ☐ = <b>%d</b>." % (a, a, a), allow_zero=True)
    if a + b > 20 or a == b or a == 0:
        raise AssertionError
    if kind == "order":
        return mcq("<b>%d + %d = %d + ☐</b>. What number goes in the box?" % (a, b, b), a, [a + b, b, a + 1],
                   "Changing the order of the addends does not change the sum. %d + %d = %d + <b>%d</b>." % (a, b, b, a))
    right = "%d + %d" % (b, a)
    return mcq("Which has the same sum as <b>%d + %d</b>?" % (a, b), right, ["%d + %d" % (b, a + 1), "%d − %d" % (max(a, b), min(a, b)), "%d + %d" % (a, a)],
               "Turn the addends around: %d + %d = %d + %d = %d. <b>%s</b>." % (a, b, b, a, a + b, right))


def build():
    sets, R = build_sets([
        ("Add with pictures", [("run", sga.set_add_pictures, (), 20)]),
        ("Add within 10", [("run", usa.set_add10, (usa.People,), 20)]),
        ("Make 10 to add", [("run", usa.set_make10, (usa.People,), 20)]),
        ("Doubles", [("run", usa.set_doubles, (usa.People,), 20)]),
        ("Adding 0 and turn-around facts", [("collect", uniq(one_prop), 14), ("run", uss.set_turn_around, (uss.People,), 6)]),
    ], 70108)
    finish(sets, R)
    body = lesson('<ul><li>Count all, or count on from the bigger number: 8 + 3 → 9, 10, 11.</li><li>Make 10: 9 + 4 = 9 + 1 + 3 = 10 + 3 = 13.</li><li>Adding 0 does not change the number: 7 + 0 = 7.</li><li>Changing the order of the addends does not change the sum: 3 + 8 = 8 + 3.</li></ul>',
        [example("8 + 5", ["8 + 2 = 10", "10 + 3"], "13")],
        [['Counting the start again', 'Start counting on at the next number.'], ['5 + 0 = 0', '5 + 0 = 5.'], ['Order changes the sum', '3 + 8 and 8 + 3 are both 11.']])
    faq = [('What does MATATAG Math 1 ask about addition?', 'Illustrate addition of numbers with sums up to 20 using models, and illustrate the properties of addition: adding zero, and changing the order of the addends.'), ('What are doubles?', 'Adding a number to itself: 6 + 6.'), ('What is counting on?', 'Starting at one number and counting up.'), ('Why make 10?', 'Adding to 10 is easy.')]
    make('addition-within-20', 8, 'Number and Algebra', 'Grade 1: Number and Algebra',
         'Illustrate addition of numbers with sums up to 20 using a variety of concrete and pictorial models; illustrate by applying the following properties of addition, using sums up to 20: the sum of zero and any number is equal to the number, and changing the order of the addends does not change the sum.',
         'Addition with Sums up to 20: Pictures, Number Lines and Properties', 'Addition within 20',
         'Free Grade 1 addition worksheets for the DepEd MATATAG curriculum: sums up to 20 with pictures, making 10, doubles, adding 0 and turn-around facts. 100 questions with pictures and answers.',
         'Count on from the bigger number.', '3 + 8 = 8 + 3. Adding 0 keeps the number.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
