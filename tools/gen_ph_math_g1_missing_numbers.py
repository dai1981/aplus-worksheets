# -*- coding: utf-8 -*-
"""
Philippines Grade 1 Math (MATATAG): Missing Numbers and Equivalent Expressions up to 20 (Grade 1: Number and Algebra)
  python3 tools/gen_ph_math_g1_missing_numbers.py
The equal sign as "the same as", true and false number sentences, missing numbers in addition and subtraction
sentences (US Grade 1 makers and own maker), and equivalent expressions like 2 + 3 = 1 + 4 (own maker).
Wrong answers come from real mistakes: writing the answer to the left side in the box, thinking the answer must come
after the equal sign, and adding the numbers that are shown.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g1_equal_sign as use
adopt(use)
if hasattr(use, 'R'): use.R = random.Random(701170)
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


def one_eqv(r):
    a, b = r.randint(1, 9), r.randint(1, 9)
    s = a + b
    if r.random() < 0.6:
        c = r.choice([x for x in range(1, s) if x not in (a, b)] or [1])
        right = "%d + %d" % (c, s - c)
        wr = ["%d + %d" % (c, s - c + 1), "%d + %d" % (a + 1, b + 1), "%d − %d" % (s, c)]
        return mcq("Which has the same value as <b>%d + %d</b>?" % (a, b), right, wr, "%d + %d = %d and %s = %d. <b>%s</b>." % (a, b, s, right, s, right))
    big = r.randint(8, 20)
    k = r.randint(1, big - 3)
    d = big - k
    c = r.randint(d + 1, 20) if d + 1 <= 20 else None
    if c is None or c == big:
        raise AssertionError
    right = "%d − %d" % (c, c - d)
    wr = ["%d − %d" % (c, c - d + 1), "%d − %d" % (big + 1, k - 1 if k > 1 else k + 2), "%d + %d" % (c, c - d)]
    return mcq("Which has the same value as <b>%d − %d</b>?" % (big, k), right, wr, "%d − %d = %d and %s = %d. <b>%s</b>." % (big, k, d, right, d, right))


def one_miss(r):
    kind = r.choice(["a", "b", "c", "e"])
    a, b = r.randint(1, 12), r.randint(1, 8)
    s = a + b
    if s > 20:
        raise AssertionError
    if kind == "a":
        return mcq("<b>%d + ☐ = %d</b>" % (a, s), b, [s, a, b + 1], "%d + <b>%d</b> = %d." % (a, b, s))
    if kind == "b":
        return mcq("<b>☐ − %d = %d</b>" % (b, a), s, [a - b if a > b else a + 1, a, s + 1], "<b>%d</b> − %d = %d." % (s, b, a))
    if kind == "c":
        return mcq("<b>%d − ☐ = %d</b>" % (s, a), b, [s + a if s + a <= 20 else b + 2, a, b + 1], "%d − <b>%d</b> = %d." % (s, b, a))
    c = r.randint(1, s - 1)
    return mcq("<b>%d + %d = %d + ☐</b>" % (a, b, c), s - c, [s, s + c if s + c <= 20 else s - c + 2, c], "Both sides must be %d: %d + <b>%d</b> = %d." % (s, c, s - c, s))


def build():
    sets, R = build_sets([
        ("The same as", [("run", use.set_same_as, (use.People,), 20)]),
        ("True or false?", [("run", use.set_true_false, (use.People,), 20)]),
        ("Find the missing number", [("collect", uniq(one_miss), 20)]),
        ("Equivalent expressions", [("collect", uniq(one_eqv), 20)]),
        ("Missing numbers in the middle", [("run", use.set_right_middle, (use.People,), 10), ("run", use.set_left_both, (use.People,), 10)]),
    ], 70117)
    finish(sets, R)
    body = lesson('<ul><li>The equal sign means <b>the same as</b>. Both sides have the same value.</li><li>2 + 3 = 1 + 4 is true: both sides are 5.</li><li>To find a missing number, work out the side you know, then make the other side the same.</li><li>The box can be anywhere: ☐ + 4 = 9, 9 = ☐ + 4.</li></ul>',
        [example("6 + 4 = ☐ + 7", ["6 + 4 = 10", "3 + 7 = 10"], "3")],
        [["Writing the left side's answer", 'In 6 + 4 = ☐ + 7, ☐ is not 10.'], ['Answer after =', '= means the same as.'], ['Adding what you see', 'Make both sides equal.']])
    faq = [('What does MATATAG Math 1 ask about missing numbers?', 'Find the missing number in addition or subtraction sentences involving numbers up to 20, and write an equivalent expression to a given addition or subtraction expression (for example, 2 + 3 = 1 + 4; 10 − 5 = 6 − 1).'), ('Is 8 = 8 true?', 'Yes.'), ('Can the answer be on the left?', 'Yes: 9 = 4 + 5.'), ('How can I check?', 'Work out both sides.')]
    make('missing-numbers-and-equivalent-expressions', 17, 'Number and Algebra', 'Grade 1: Number and Algebra',
         'Find the missing number in addition or subtraction sentences involving numbers up to 20; write an equivalent expression to a given addition or subtraction expression (e.g., 2 + 3 = 1 + 4; 10 − 5 = 6 − 1).',
         'Missing Numbers and Equivalent Expressions up to 20', 'Missing Numbers',
         'Free Grade 1 worksheets on missing numbers and equivalent expressions for the DepEd MATATAG curriculum: the equal sign, true or false, and missing numbers up to 20. 100 questions with answers.',
         '= means the same as.', 'Work out the side you know first.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
