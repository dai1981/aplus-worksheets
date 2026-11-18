# -*- coding: utf-8 -*-
"""
Texas Grade 1 Math: Adding Tens and Ones: 40 + 7 (TEKS 1.3A)
  python3 tools/gen_ustx_math_g1_tens_and_ones.py
Adding a multiple of 10 and a one-digit number with base-ten blocks, in either order, with a missing part, in
expanded form, and in stories (own makers; blocks from the US Grade 1 place value maker).
Wrong answers come from real mistakes: adding the digits (4 + 7 = 11), swapping the digits (74), and adding 10
more than needed.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g1_place_value as pv
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



def one_blocks(r):
    t, o = r.randint(1, 9), r.randint(1, 9)
    n = 10 * t + o
    pic = pv.fig(pv.blocks_svg(t, o))
    return mcq(pic + "The blocks show %d tens and %d ones. What is %d + %d?" % (t, o, 10 * t, o), str(n), [str(t + o), str(10 * o + t), str(n + 10)],
               "%d tens is %d. %d + %d = <b>%d</b>." % (t, 10 * t, 10 * t, o, n))


def one_sum(r):
    t, o = r.randint(1, 9), r.randint(1, 9)
    n = 10 * t + o
    if r.random() < 0.5:
        return mcq("%d + %d = ?" % (10 * t, o), str(n), [str(t + o), str(10 * o + t), str(n + 10)], "%d tens and %d ones make <b>%d</b>." % (t, o, n))
    return mcq("%d + %d = ?" % (o, 10 * t), str(n), [str(t + o), str(10 * o + t), str(n - 10 if t > 1 else n + 20)], "Add in any order: %d + %d = <b>%d</b>." % (10 * t, o, n))


def one_missing(r):
    t, o = r.randint(1, 9), r.randint(1, 9)
    n = 10 * t + o
    if r.random() < 0.5:
        return mcq("%d + ☐ = %d. What number goes in the box?" % (10 * t, n), str(o), [str(10 * o), str(n - o + 1), str(t)],
                   "%d is %d tens and %d ones, so the box is <b>%d</b>." % (n, t, o, o))
    return mcq("☐ + %d = %d. What number goes in the box?" % (o, n), str(10 * t), [str(t), str(10 * t + 10), str(n - 1)],
               "%d is %d tens and %d ones, so the box is <b>%d</b>." % (n, t, o, 10 * t))


def one_expand(r):
    t, o = r.randint(1, 9), r.randint(1, 9)
    n = 10 * t + o
    if r.random() < 0.5:
        return mcq("Which is the same as %d?" % n, "%d + %d" % (10 * t, o), ["%d + %d" % (t, o), "%d + %d" % (10 * o, t), "%d + %d" % (10 * t + 10, o)],
                   "%d = %d tens and %d ones = <b>%d + %d</b>." % (n, t, o, 10 * t, o))
    return mcq("What number is %d tens and %d ones?" % (t, o), str(n), [str(t + o), str(10 * o + t), str(n + 1)], "%d + %d = <b>%d</b>." % (10 * t, o, n))


THINGS = [("crayons", "boxes"), ("pencils", "packs"), ("eggs", "cartons"), ("stickers", "sheets"), ("cookies", "bags"), ("markers", "sets")]


def one_story(r):
    k = Kid(r).next()
    t, o = r.randint(2, 9), r.randint(1, 9)
    n = 10 * t + o
    thing, box = r.choice(THINGS)
    if r.random() < 0.5:
        return mcq("%s has %d %s of 10 %s and %d loose %s. How many %s does %s have?" % (k["n"], t, box, thing, o, thing, thing, k["he"]), str(n), [str(t + o), str(10 * o + t), str(n + 10)],
                   "%d %s of 10 is %d. %d + %d = <b>%d</b>." % (t, box, 10 * t, 10 * t, o, n))
    return mcq("%s has %d %s. %s gets %d more. How many %s does %s have now?" % (k["n"], 10 * t, thing, k["He"], o, thing, k["he"]), str(n), [str(t + o), str(10 * o + t), str(n + 10)],
               "%d + %d = <b>%d</b>." % (10 * t, o, n))


def build():
    sets, R = build_sets([
        ("Tens and ones with blocks", [("collect", uniq(one_blocks), 20)]),
        ("Add tens and ones", [("collect", uniq(one_sum), 20)]),
        ("Same number, two ways", [("collect", uniq(one_expand), 20)]),
        ("Find the missing part", [("collect", uniq(one_missing), 20)]),
        ("Tens and ones stories", [("collect", uniq(one_story), 20)]),
    ], 69103)
    finish(sets, R)
    body = lesson('<ul><li>A number like 40 is <b>4 tens</b>. A number like 7 is <b>7 ones</b>.</li><li>40 + 7: put the tens and ones together. 4 tens and 7 ones is <b>47</b>.</li><li>You can add in any order: 7 + 40 = 47.</li></ul>',
        [example("40 + 7", ["4 tens and 7 ones"], "47")],
        [['Adding the digits', '40 + 7 is not 11.'], ['Swapping the digits', '4 tens and 7 ones is 47, not 74.'], ['Adding an extra ten', 'Count the rods carefully.']])
    faq = [('What does TEKS 1.3A ask?', 'Use concrete and pictorial models to determine the sum of a multiple of 10 and a one-digit number in problems up to 99.'), ('What is 60 + 5?', '65.'), ('Is 5 + 60 the same as 60 + 5?', 'Yes. Both are 65.'), ('Why are blocks helpful?', 'You can see the tens and the ones.')]
    make('adding-tens-and-ones', 3, 'Number and Operations', '1.3A',
         '1.3A use concrete and pictorial models to determine the sum of a multiple of 10 and a one-digit number in problems up to 99',
         'Adding Tens and Ones: 40 + 7', 'Adding Tens and Ones',
         'Free Grade 1 worksheets for Texas TEKS 1.3A: add a multiple of 10 and a one-digit number with base-ten blocks, missing parts and stories. 100 questions with answers.',
         '40 + 7 is 4 tens and 7 ones: 47.', 'Add in any order: 7 + 40 = 47.',
         body, faq, sets, seo_title='Grade 1 Adding Tens and Ones Worksheets (TEKS 1.3A)')


if __name__ == "__main__":
    build()
