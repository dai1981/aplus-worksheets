# -*- coding: utf-8 -*-
"""
Philippines Grade 1 Math (MATATAG): Composing and Decomposing Numbers up to 10 (Grade 1: Number and Algebra)
  python3 tools/gen_ph_math_g1_number_bonds.py
Ten frames, pairs that make a number, part-part-whole and number bonds up to 10 (Texas Grade 1, BC Grade 1 and
Australia Foundation makers, and own makers).
Wrong answers come from real mistakes: adding the parts when a part is missing, forgetting 0 as a part, and
counting empty boxes in a ten frame.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_ustx_math_g1_making_10 as txm
adopt(txm)
if hasattr(txm, 'R'): txm.R = random.Random(701070)
import gen_cabc_math_g1_make_10 as cbm
adopt(cbm)
if hasattr(cbm, 'R'): cbm.R = random.Random(701071)
import gen_au_maths_f_part_part_whole as aup
adopt(aup)
if hasattr(aup, 'R'): aup.R = random.Random(701072)
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


def one_bond(r):
    n = r.randint(3, 10)
    a = r.randint(0, n)
    kind = r.choice(["and", "split", "ways"])
    if kind == "and":
        return mcq("<b>%d</b> is %d and ☐." % (n, a), n - a, [n + a, n - a + 1 if n - a + 1 != n + a else n - a + 2, a if a != n - a else a + 1],
                   "%d and %d make %d. ☐ = <b>%d</b>." % (a, n - a, n, n - a), allow_zero=True)
    if kind == "split":
        b = r.randint(1, n - 1)
        right = "%d and %d" % (b, n - b)
        wr = ["%d and %d" % (b, n - b + 1), "%d and %d" % (b + 1, n - b + 1), "%d and %d" % (n, b)]
        return mcq("Which pair makes <b>%d</b>?" % n, right, wr, "%d + %d = %d. <b>%s</b>." % (b, n - b, n, right))
    if n > 8:
        raise AssertionError
    return mcq("How many ways can you split <b>%d</b> into two parts (like 0 and %d, 1 and %d, …)?" % (n, n, n - 1), n + 1, [n, n - 1, 2 * n],
               "From 0 and %d up to %d and 0 there are <b>%d</b> ways." % (n, n, n + 1))


def build():
    sets, R = build_sets([
        ("Ten frames", [("collect", txm.one_frame, 12), ("run", cbm.set_frames, (), 8)]),
        ("Pairs that make 10", [("collect", txm.one_pair, 20)]),
        ("Part, part, whole", [("run", aup.set_join, ("rnd",), 10), ("run", aup.set_hidden, ("rnd",), 10)]),
        ("Number bonds", [("run", aup.set_bonds, ("rnd",), 20)]),
        ("Ways to make a number", [("collect", uniq(one_bond), 20)]),
    ], 70107)
    finish(sets, R)
    body = lesson('<ul><li>A number can be split into two parts: 5 is 5 and 0, 4 and 1, 3 and 2.</li><li>Put the parts together to make the whole again: 3 and 2 make 5.</li><li>A ten frame shows how many more make 10: 7 dots and 3 empty boxes.</li><li>Pairs that make 10: 1 and 9, 2 and 8, 3 and 7, 4 and 6, 5 and 5.</li></ul>',
        [example("8 is 5 and ☐", ["5 and 3 make 8"], "3")],
        [['Adding the parts', '8 is 5 and 3, not 13.'], ['Forgetting 0', '6 is 6 and 0 too.'], ['Counting empty boxes', 'Count the dots, then the empty boxes.']])
    faq = [('What does MATATAG Math 1 ask about composing numbers?', 'Compose and decompose numbers up to 10 using concrete materials (for example, 5 is 5 and 0; 4 and 1; 3 and 2).'), ('What is a number bond?', 'A picture that shows a whole and its two parts.'), ('Why learn pairs that make 10?', 'They make adding and subtracting much easier.'), ('How many ways can 6 be split?', '7 ways, from 0 and 6 to 6 and 0.')]
    make('composing-and-decomposing-numbers-to-10', 7, 'Number and Algebra', 'Grade 1: Number and Algebra',
         'Compose and decompose numbers up to 10 using concrete materials (e.g., 5 is 5 and 0; 4 and 1; 3 and 2).',
         'Composing and Decomposing Numbers up to 10', 'Numbers up to 10',
         'Free Grade 1 worksheets on composing and decomposing numbers to 10 for the DepEd MATATAG curriculum: ten frames, pairs that make 10, part-part-whole and number bonds. 100 questions with pictures and answers.',
         '5 is 4 and 1, 3 and 2, 5 and 0.', 'Pairs that make 10: 1+9, 2+8, 3+7, 4+6, 5+5.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
