# -*- coding: utf-8 -*-
"""
Philippines Grade 1 Math (MATATAG): Comparing and Ordering Numbers up to 20 (Grade 1: Number and Algebra)
  python3 tools/gen_ph_math_g1_compare_20.py
Comparing two numbers up to 20 in words and with the signs &gt;, &lt; and =, largest and smallest, and ordering
numbers up to 20 (own makers and Australia Foundation makers).
Wrong answers come from real mistakes: thinking 12 is less than 9 because 1 is less than 9, turning the sign the
wrong way, and ordering only some of the numbers.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_au_maths_f_numbers_to_20 as auf
adopt(auf)
if hasattr(auf, 'R'): auf.R = random.Random(701050)
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


def one_cmp(r):
    a, b = r.sample(range(0, 21), 2)
    p = Kid(r)
    x, y = p.next(), p.next()
    what = r.choice(["mangoes", "pencils", "marbles", "eggs", "stickers", "shells", "candies", "books"])
    kind = r.choice(["more", "fewer", "sym"])
    if kind == "sym":
        s = "&gt;" if a > b else "&lt;"
        return mcq("Which sign goes in the box? <b>%d ☐ %d</b>" % (a, b), s, ["&gt;" if s == "&lt;" else "&lt;", "=", "+"],
                   "%d is %s than %d, so <b>%d %s %d</b>." % (a, "more" if a > b else "less", b, a, s, b))
    q = "%s has %d %s. %s has %d %s. Who has %s?" % (x["n"], a, what, y["n"], b, what, "more" if kind == "more" else "fewer")
    right = x["n"] if (a > b) == (kind == "more") else y["n"]
    return mcq(q, right, [y["n"] if right == x["n"] else x["n"], "They have the same", "No one"],
               "%d is %s than %d. <b>%s</b> has %s." % (max(a, b), "more", min(a, b), right, kind))


def one_ord(r):
    vs = r.sample(range(0, 21), 3)
    up = r.random() < 0.5
    s = sorted(vs, reverse=not up)
    show = lambda v: ", ".join(map(str, v))
    wr = [show(list(reversed(s))), show([s[1], s[0], s[2]]), show([s[0], s[2], s[1]])]
    return mcq("Put in order from %s: <b>%s</b>" % ("smallest to largest" if up else "largest to smallest", show(vs)), show(s), wr, "<b>%s</b>." % show(s))


def one_most(r):
    vs = r.sample(range(1, 21), 4)
    big = r.random() < 0.5
    t = max(vs) if big else min(vs)
    return mcq("Which number is the %s: %s?" % ("largest" if big else "smallest", ", ".join(map(str, vs))), t, [v for v in vs if v != t],
               "Compare the tens, then the ones. The %s is <b>%d</b>." % ("largest" if big else "smallest", t))


def build():
    sets, R = build_sets([
        ("Who has more? Who has fewer?", [("collect", uniq(one_cmp), 20)]),
        ("Compare pictures", [("run", auf.set_compare, ("rnd",), 20)]),
        ("Largest and smallest", [("collect", uniq(one_most), 20)]),
        ("Order three numbers", [("collect", uniq(one_ord), 20)]),
        ("Numbers in order", [("run", auf.set_order, ("rnd",), 20)]),
    ], 70105)
    finish(sets, R)
    body = lesson('<ul><li>On a number line, numbers get bigger to the right.</li><li>A teen number is more than any number from 0 to 9: 12 &gt; 9.</li><li>The sign opens to the bigger number: 15 &gt; 8, 8 &lt; 15.</li><li>To order, find the smallest first, then the next, and so on.</li></ul>',
        [example("Order 14, 6, 19", ["smallest: 6", "then 14", "then 19"], "6, 14, 19")],
        [['12 &lt; 9', '12 is 1 ten and 2: it is more than 9.'], ['Sign the wrong way', 'The open side faces the bigger number.'], ['Missing a number', 'Check that every number is in the list.']])
    faq = [('What does MATATAG Math 1 ask about comparing?', 'Compare two numbers up to 20, and order numbers up to 20 from smallest to largest, and vice versa.'), ('What does &gt; mean?', 'Greater than.'), ('Is 20 more than 19?', 'Yes, by 1.'), ('How do I teach the signs?', 'Say the open side eats the bigger number.')]
    make('comparing-and-ordering-numbers-to-20', 5, 'Number and Algebra', 'Grade 1: Number and Algebra',
         'Compare two numbers up to 20; order numbers up to 20 from smallest to largest, and vice versa.',
         'Comparing and Ordering Numbers up to 20', 'Comparing Numbers to 20',
         'Free Grade 1 worksheets on comparing and ordering numbers to 20 for the DepEd MATATAG curriculum: more and fewer, the signs &gt; and &lt;, and putting numbers in order. 100 questions with pictures and answers.',
         'Numbers get bigger to the right.', 'The sign opens to the bigger number.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
