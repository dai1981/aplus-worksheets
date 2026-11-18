# -*- coding: utf-8 -*-
"""
Texas Grade 2 Math: Equal Groups: Joining and Sharing (TEKS 2.6A, 2.6B)
  python3 tools/gen_ustx_math_g2_equal_groups.py
Rows and columns in arrays, adding rows and columns, matching arrays (the US Grade 2 makers with Texas names),
sharing equally into groups (own maker), and stories.
Wrong answers come from real mistakes: counting the rows instead of the objects, adding the number of groups and
the group size, and sharing unequally.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g2_arrays as ar
adopt(ar)
tx_common.GRADE = "grade-2"

def abcd(fn):
    """Build the A-D array pictures now, with the right picture at a random position."""
    def f(P, rnd=None):
        st = fn(P)
        for it in st["items"]:
            if "_abcd" in it:
                prompt, right, wrong, kind = it.pop("_abcd")
                wrong = list(wrong)
                t = MATCH_R.randrange(4)
                MATCH_R.shuffle(wrong)
                it["q"] = ar.fig(ar.abcd_svg(wrong[:t] + [right] + wrong[t:], kind)) + prompt
                it["a"] = t
                it["e"] = it["e"].replace("{L}", "ABCD"[t])
        return st
    f.__name__ = fn.__name__
    return f


import random as _r
MATCH_R = _r.Random(692111)
set_match = abcd(ar.set_match)

THINGS = ["apples", "cookies", "crayons", "stickers", "toy cars", "pencils", "balloons", "pecans"]


def one_share(r):
    k = Kid(r).next()
    g = r.randint(2, 5)
    e = r.randint(2, 6)
    t = r.choice(THINGS)
    n = g * e
    if r.random() < 0.5:
        return mcq("%s puts %d %s into %d equal groups. How many are in each group?" % (k["n"], n, t, g), str(e), [str(n - g), str(g), str(e + 1)],
                   "Put %d %s into %d equal groups: %d in each. <b>%d</b>." % (n, t, g, e, e))
    return mcq("There are %d %s. Put %d in each bag. How many bags are there?" % (n, t, e), str(g), [str(n - e), str(e), str(g + 1)],
               "Make groups of %d until all %d are used: <b>%d bags</b>." % (e, n, g))


def build():
    sets, R = build_sets([
        ("Rows and columns", [("run", ar.set_rows_cols, (ar.People,), 20)]),
        ("Add the rows", [("run", ar.set_add_rows, (ar.People,), 20)]),
        ("Add the columns and match arrays", [("run", ar.set_add_cols, (ar.People,), 10), ("run", set_match, (ar.People,), 10)]),
        ("Share equally", [("collect", one_share, 20)]),
        ("Equal group stories", [("run", ar.set_stories, (ar.People,), 20)]),
    ], 69211)
    finish(sets, R)
    body = lesson('<ul><li><b>Equal groups</b> have the same number in each group.</li><li>Joining equal groups: 3 groups of 4 is 4 + 4 + 4 = 12.</li><li>An <b>array</b> puts objects in equal rows and columns.</li><li><b>Sharing</b> splits a total into equal groups: 12 shared by 3 is 4 each.</li></ul>',
        [example("4 rows of 5 chairs", ["5 + 5 + 5 + 5"], "20 chairs"), example("15 cookies shared by 3", ["3 groups of 5"], "5 each")],
        [['Counting rows instead of objects', 'Count every object, or add the rows.'], ['Adding the groups and the size', '3 groups of 4 is 12, not 7.'], ['Sharing unequally', 'Each group must have the same number.']])
    faq = [('What does TEKS 2.6A ask?', 'Model, create and describe contextual multiplication situations in which equivalent sets of concrete objects are joined.'), ('What does TEKS 2.6B ask?', 'Model, create and describe contextual division situations in which a set of concrete objects is separated into equivalent sets.'), ('What is an array?', 'Objects in equal rows and equal columns.'), ('How do I check sharing?', 'Add the groups back together to get the total.')]
    make('equal-groups-multiplication-and-division', 11, 'Number and Operations', '2.6A, 2.6B',
         '2.6A model, create, and describe contextual multiplication situations in which equivalent sets of concrete objects are joined; 2.6B model, create, and describe contextual division situations in which a set of concrete objects is separated into equivalent sets',
         'Equal Groups: Joining and Sharing', 'Equal Groups',
         'Free Grade 2 worksheets for Texas TEKS 2.6A and 2.6B: equal groups, arrays, adding rows and columns, sharing equally and stories. 100 questions with answers.',
         'Equal groups have the same number in each.', '3 groups of 4 = 4 + 4 + 4 = 12. 12 shared by 3 = 4 each.',
         body, faq, sets, seo_title='Grade 2 Equal Groups Worksheets: Arrays and Sharing (TEKS 2.6A, 2.6B)')


if __name__ == "__main__":
    build()
