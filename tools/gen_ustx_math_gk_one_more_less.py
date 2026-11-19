# -*- coding: utf-8 -*-
"""
Texas Kindergarten Math: One More and One Less (TEKS K.2F)
  python3 tools/gen_ustx_math_gk_one_more_less.py
Before, after and between (the Australian Foundation maker), and one more and one less with pictures, numbers and
stories (own makers; pictures from the US Kindergarten picture maker).
Wrong answers come from real mistakes: giving the same number, going the wrong way, and changing by 2.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_au_maths_f_numbers_to_20 as n20
adopt(n20)
from k_pics import row_svg, crossed_row_svg, name
tx_common.GRADE = "kindergarten"

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


PICS = ["apple", "star", "ball", "fish", "flower", "heart", "duck", "cup", "bug"]


def one_more_pic(r):
    n = r.randint(1, 15)
    k = r.choice(PICS)
    pic = fig(row_svg(n, k, per_row=5))
    return mcq(pic + "1 more %s comes. How many %s now?" % (name(k, 1), name(k)), str(n + 1), [str(n), str(n + 2), str(n - 1) if n > 1 else "3"],
               "%d and 1 more is <b>%d</b>." % (n, n + 1))


def one_less_pic(r):
    n = r.randint(2, 16)
    k = r.choice(PICS)
    pic = fig(crossed_row_svg(n, k, 1))
    return mcq(pic + "1 %s goes away. How many %s are left?" % (name(k, 1), name(k)), str(n - 1), [str(n), str(n + 1), str(n - 2) if n > 2 else "4"],
               "%d and 1 less is <b>%d</b>." % (n, n - 1))


def one_num(r):
    n = r.randint(1, 19)
    if r.random() < 0.5:
        return mcq("What number is 1 more than %d?" % n, str(n + 1), [str(n), str(n - 1), str(n + 2)], "Count on 1: %d, <b>%d</b>." % (n, n + 1))
    return mcq("What number is 1 less than %d?" % n, str(n - 1), [str(n), str(n + 1), str(n - 2) if n > 1 else "2"], "Count back 1: %d, <b>%d</b>." % (n, n - 1))


THINGS = ["blocks", "crayons", "stickers", "shells", "grapes", "cars", "rocks", "beads"]


def one_story(r):
    k = Kid(r).next()
    n = r.randint(2, 19)
    t = r.choice(THINGS)
    if r.random() < 0.5:
        return mcq("%s has %d %s. %s gets 1 more. How many %s does %s have now?" % (k["n"], n, t, k["He"], t, k["he"]), str(n + 1), [str(n), str(n - 1), str(n + 2)],
                   "1 more than %d is <b>%d</b>." % (n, n + 1))
    return mcq("%s has %d %s. %s gives 1 away. How many %s does %s have now?" % (k["n"], n, t, k["He"], t, k["he"]), str(n - 1), [str(n), str(n + 1), str(n - 2) if n > 2 else "4"],
               "1 less than %d is <b>%d</b>." % (n, n - 1))


def build():
    sets, R = build_sets([
        ("Before, after and between", [("run", n20.set_order, ("rnd",), 20)]),
        ("1 more with pictures", [("collect", uniq(one_more_pic), 20)]),
        ("1 less with pictures", [("collect", uniq(one_less_pic), 20)]),
        ("1 more and 1 less with numbers", [("collect", uniq(one_num), 20)]),
        ("1 more and 1 less stories", [("collect", uniq(one_story), 20)]),
    ], 69004)
    finish(sets, R)
    body = lesson('<ul><li><b>1 more</b> is the next number when you count: 1 more than 7 is 8.</li><li><b>1 less</b> is the number just before: 1 less than 7 is 6.</li><li>Use a number line or your fingers to check.</li></ul>',
        [example("1 more than 12", ["12, 13"], "13")],
        [['Giving the same number', '1 more changes the number.'], ['Going the wrong way', 'More goes up; less goes down.'], ['Changing by 2', 'Count just 1.']])
    faq = [('What does TEKS K.2F ask?', 'Generate a number that is one more than or one less than another number up to at least 20.'), ('What is 1 more than 19?', '20.'), ('What is 1 less than 10?', '9.'), ('How can a number line help?', 'Step right for 1 more and left for 1 less.')]
    make('one-more-and-one-less', 4, 'Number and Operations', 'K.2F',
         'K.2F generate a number that is one more than or one less than another number up to at least 20',
         'One More and One Less', 'One More and One Less',
         'Free kindergarten worksheets for Texas TEKS K.2F: one more and one less with pictures, numbers to 20 and stories. 100 questions with answers.',
         '1 more is the next number; 1 less is the number before.', '1 more than 7 is 8; 1 less is 6.',
         body, faq, sets, seo_title='Kindergarten One More and One Less Worksheets (TEKS K.2F)')


if __name__ == "__main__":
    build()
