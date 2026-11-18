# -*- coding: utf-8 -*-
"""
Texas Grade 1 Math: Making 10 with Two or More Addends (TEKS 1.3C)
  python3 tools/gen_ustx_math_g1_making_10.py
Ten frames, pairs that make 10, three numbers that make 10, making a ten first (the US Grade 1 maker), and stories
(own makers; ten frames from the US Grade 1 place value maker).
Wrong answers come from real mistakes: counting the dots instead of the empty boxes, picking a pair that makes 9 or
11, and forgetting one of three addends.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g1_add_three as at
adopt(at)
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



def one_frame(r):
    n = r.randint(1, 9)
    pic = pv.fig(pv.tenframes_svg(n))
    q = r.choice(["How many more dots make 10?", "How many boxes are empty?"])
    return mcq(pic + q, str(10 - n), [str(n), str(11 - n), str(9 - n) if n < 9 else "10"], "%d dots. %d + %d = 10, so <b>%d</b>." % (n, n, 10 - n, 10 - n))


def one_pair(r):
    a = r.randint(1, 9)
    b = 10 - a
    w = set()
    while len(w) < 3:
        x = r.randint(1, 9)
        y = r.choice([9 - x, 11 - x, 8 - x, 12 - x])
        if 0 < y < 10:
            w.add("%d and %d" % (x, y))
    k = Kid(r).next()
    q = r.choice(["%s picks two number cards that add to 10. Which cards could %s pick?" % (k["n"], k["he"]),
                  "%s wants two numbers that make 10. Which two should %s use?" % (k["n"], k["he"])])
    return mcq(q, "%d and %d" % (a, b), sorted(w), "%d + %d = <b>10</b>." % (a, b))


def one_three(r):
    a, b = r.randint(1, 7), r.randint(1, 7)
    c = 10 - a - b
    if c < 1:
        raise AssertionError
    if r.random() < 0.6:
        return mcq("%d + %d + ☐ = 10. What number goes in the box?" % (a, b), str(c), [str(c + 1), str(c - 1) if c > 1 else str(c + 2), str(a + b)],
                   "%d + %d = %d. %d + %d = 10, so the box is <b>%d</b>." % (a, b, a + b, a + b, c, c))
    return mcq("Which three numbers make 10?", "%d, %d and %d" % (a, b, c), ["%d, %d and %d" % (a, b, c + 1), "%d, %d and %d" % (a, b + 1, c + 1), "%d, %d and %d" % (a, b, c - 1 if c > 1 else c + 2)],
               "%d + %d + %d = <b>10</b>." % (a, b, c))


THINGS = ["beads", "blocks", "shells", "stickers", "marbles", "crayons"]


def one_story(r):
    k = Kid(r).next()
    thing = r.choice(THINGS)
    a = r.randint(1, 9)
    kind = r.randrange(3)
    if kind == 0:
        return mcq("%s has %d %s. %s wants 10. How many more %s does %s need?" % (k["n"], a, thing, k["He"], thing, k["he"]), str(10 - a), [str(10 + a) if a < 10 else "20", str(a), str(9 - a) if a < 9 else "2"],
                   "%d + %d = 10, so %s needs <b>%d</b> more." % (a, 10 - a, k["he"], 10 - a))
    if kind == 1:
        if a < 2:
            raise AssertionError
        b = r.randint(2, 8 - a) if a < 7 else None
        if not b:
            raise AssertionError
        c = 10 - a - b
        return mcq("%s has %d red %s, %d blue %s and some green %s. %s has 10 %s in all. How many are green?" % (k["n"], a, thing, b, thing, thing, k["He"], thing), str(c), [str(a + b), str(c + 1), str(10 + a + b)],
                   "%d + %d = %d. %d + %d = 10, so <b>%d</b> are green." % (a, b, a + b, a + b, c, c))
    b = 10 - a
    return mcq("%s puts %d %s in one box and %d %s in another box. How many %s are there in all?" % (k["n"], a, thing, b, thing, thing), "10", [str(a), str(b), "9"],
               "%d + %d = <b>10</b>." % (a, b))


def build():
    sets, R = build_sets([
        ("Ten frames: how many more make 10?", [("collect", uniq(one_frame), 14), ("collect", uniq(one_pair), 6)]),
        ("Pairs that make 10", [("collect", uniq(one_pair), 20)]),
        ("Three numbers that make 10", [("collect", uniq(one_three), 20)]),
        ("Make a ten first", [("run", at.set_make_ten, (at.People,), 20)]),
        ("Making 10 stories", [("collect", uniq(one_story), 20)]),
    ], 69104)
    finish(sets, R)
    body = lesson('<ul><li>Pairs that make 10: 1 + 9, 2 + 8, 3 + 7, 4 + 6, 5 + 5.</li><li>On a <b>ten frame</b>, the empty boxes show how many more make 10.</li><li>Three numbers can make 10 too: 2 + 3 + 5 = 10.</li><li>When adding three numbers, find two that make 10 first.</li></ul>',
        [example("7 dots on a ten frame", ["3 boxes are empty"], "7 + 3 = 10")],
        [['Counting the dots instead of the empty boxes', 'How many more means count the empty boxes.'], ['Picking a pair that makes 9 or 11', 'Add the pair to check.'], ['Forgetting one addend', 'Add all three numbers.']])
    faq = [('What does TEKS 1.3C ask?', 'Compose 10 with two or more addends with and without concrete objects.'), ('Why is making 10 useful?', 'Adding to 10 is easy, so it helps with bigger facts.'), ('How many pairs make 10?', '1 + 9, 2 + 8, 3 + 7, 4 + 6, 5 + 5 and their turn-arounds.'), ('Can three numbers make 10?', 'Yes, like 2 + 3 + 5.')]
    make('making-10', 4, 'Number and Operations', '1.3C',
         '1.3C compose 10 with two or more addends with and without concrete objects',
         'Making 10 with Two or More Addends', 'Making 10',
         'Free Grade 1 making 10 worksheets for Texas TEKS 1.3C: ten frames, pairs and three numbers that make 10, make a ten first and stories. 100 questions with answers.',
         'Find the partner that makes 10.', '1 + 9, 2 + 8, 3 + 7, 4 + 6, 5 + 5',
         body, faq, sets, seo_title='Grade 1 Making 10 Worksheets (TEKS 1.3C)')


if __name__ == "__main__":
    build()
