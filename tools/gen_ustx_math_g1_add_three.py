# -*- coding: utf-8 -*-
"""
Texas Grade 1 Math: Adding Three Numbers (TEKS 1.5G)
  python3 tools/gen_ustx_math_g1_add_three.py
Adding three groups with pictures, three numbers within 20, doubles first and any order, and word problems (the US
Grade 1 makers with Texas names), plus order and grouping (own maker).
Wrong answers come from real mistakes: adding only two of the numbers, counting a number twice, and thinking a new
order changes the sum.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g1_add_three as at
adopt(at)
tx_common.GRADE = "grade-1"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f



def one_order(r):
    a, b, c = r.sample(range(1, 10), 3)
    s = a + b + c
    if s > 20:
        raise AssertionError
    k = Kid(r).next()
    kind = r.randrange(3)
    if kind == 0:
        return mcq("%d + %d + %d = %d. What is %d + %d + %d?" % (a, b, c, s, c, a, b), str(s), [str(s + 1), str(s - 1), str(a + b)],
                   "Adding in a new order gives the same sum: <b>%d</b>." % s)
    if kind == 1:
        return mcq("Which has the same sum as %d + %d + %d?" % (a, b, c), "%d + %d + %d" % (b, c, a), ["%d + %d" % (a, b), "%d + %d + %d" % (a, b, c + 1), "%d + %d + %d" % (a - 1 if a > 1 else a + 2, b, c)],
                   "Same three numbers in a new order: the sum is still %d." % s)
    return mcq("%s adds %d + %d + %d. %s adds %d + %d first. What does %s get?" % (k["n"], a, b, c, k["He"], b, c, k["he"]), str(s), [str(b + c), str(s + 1), str(a + b)],
               "%d + %d = %d, then %d + %d = <b>%d</b>." % (b, c, b + c, a, b + c, s))


def build():
    sets, R = build_sets([
        ("Add three groups with pictures", [("run", at.set_pictures, (at.People,), 20)]),
        ("Add three numbers within 20", [("run", at.set_within_20, (at.People,), 20)]),
        ("Doubles first and any order", [("run", at.set_doubles_order, (at.People,), 20)]),
        ("Change the order or the grouping", [("collect", uniq(one_order), 20)]),
        ("Word problems with three numbers", [("run", at.set_word_problems, (at.People,), 20)]),
    ], 69113)
    finish(sets, R)
    body = lesson('<ul><li>Add two numbers first, then add the third.</li><li>You can add in <b>any order</b>. The sum stays the same.</li><li>Look for a <b>double</b> or a <b>10</b> first: 4 + 7 + 6 = 10 + 7 = 17.</li></ul>',
        [example("4 + 7 + 6", ["4 + 6 = 10", "10 + 7"], "17")],
        [['Adding only two numbers', 'Touch each number as you add it.'], ['Counting a number twice', 'Cross out each number you use.'], ['Thinking a new order changes the sum', '3 + 5 + 2 = 2 + 3 + 5.']])
    faq = [('What does TEKS 1.5G ask?', 'Apply properties of operations to add and subtract two or three numbers.'), ('Does the order matter when adding?', 'No. The sum is the same.'), ('What is a good first step?', 'Find two numbers that make 10 or a double.'), ('Can the sum be more than 20?', 'Not on these worksheets.')]
    make('adding-three-numbers', 13, 'Algebraic Reasoning', '1.5G',
         '1.5G apply properties of operations to add and subtract two or three numbers',
         'Adding Three Numbers', 'Adding Three Numbers',
         'Free Grade 1 worksheets for Texas TEKS 1.5G: add three numbers within 20 with pictures, doubles, make 10, any order and word problems. 100 questions with answers.',
         'Add in any order; look for 10 or a double first.', '4 + 7 + 6 = 10 + 7 = 17',
         body, faq, sets, seo_title='Grade 1 Adding Three Numbers Worksheets (TEKS 1.5G)')


if __name__ == "__main__":
    build()
