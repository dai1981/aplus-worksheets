# -*- coding: utf-8 -*-
"""
Philippines Grade 1 Math (MATATAG): Halves and Quarters (Grade 1: Number and Algebra)
  python3 tools/gen_ph_math_g1_halves_quarters.py
Equal parts, halves and quarters of shapes, shaded parts (US Grade 1 makers), quarters of amounts (UK Year 1 maker),
and comparing and counting halves and quarters (own maker).
Wrong answers come from real mistakes: calling unequal parts halves, thinking 1/4 is bigger than 1/2 because 4 is
bigger than 2, and counting the cuts instead of the parts.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g1_halves_fourths as ush
adopt(ush)
if hasattr(ush, 'R'): ush.R = random.Random(701200)
import gen_uk_maths_y1_halves_quarters as ukh
adopt(ukh)
if hasattr(ukh, 'R'): ukh.R = random.Random(701201)
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


def one_hq(r):
    kind = r.choice(["cmp", "count_h", "count_q", "whole"])
    what = r.choice(["pizza", "bibingka", "sandwich", "watermelon", "cake", "puto"])
    if kind == "cmp":
        q = "Two %ss are the same size. Ana eats 1/2 of one. Ben eats 1/4 of the other. Who eats more?" % what
        q = q.replace("1/2", fr(1, 2)).replace("1/4", fr(1, 4))
        return mcq(q, "Ana", ["Ben", "They eat the same", "No one"], "%s is bigger than %s: 1 half is the same as 2 quarters. <b>Ana</b> eats more." % (fr(1, 2), fr(1, 4)))
    if kind == "count_h":
        n = r.randint(2, 8)
        return mcq("How many halves make %d whole %s%s?" % (n, what, "s" if n > 1 else ""), 2 * n, [n, n + 2, 4 * n],
                   "Each whole has 2 halves. %d wholes have <b>%d</b> halves." % (n, 2 * n))
    if kind == "count_q":
        n = r.randint(1, 4)
        return mcq("How many quarters make %d whole %s%s?" % (n, what, "s" if n > 1 else ""), 4 * n, [2 * n, n, 4 * n + 4],
                   "Each whole has 4 quarters. %d whole%s %s <b>%d</b> quarters." % (n, "s" if n > 1 else "", "have" if n > 1 else "has", 4 * n))
    k = r.choice([2, 4])
    return mcq("How many %s make 1 whole?" % ("halves" if k == 2 else "quarters"), k, [6 - k, 1, 8], "<b>%d</b> %s make 1 whole." % (k, "halves" if k == 2 else "quarters"))


def build():
    sets, R = build_sets([
        ("Equal parts", [("run", ush.set_equal, ("rnd",), 12), ("run", ukh.set_equal, ("rnd",), 8)]),
        ("Halves", [("run", ush.set_halves, ("rnd",), 12), ("run", ukh.set_halves, ("rnd",), 8)]),
        ("Quarters", [("run", ukh.set_quarters, ("rnd",), 20)]),
        ("Shaded parts", [("run", ush.set_shaded, ("rnd",), 20)]),
        ("Compare and count halves and quarters", [("collect", one_hq, 10), ("run", ukh.set_amounts, ("rnd",), 10)]),
    ], 70120)
    finish(sets, R)
    body = lesson("<ul><li>A <b>half</b> (<span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>) is 1 of 2 equal parts. A <b>quarter</b> (<span class='fr'><span class='fn'>1</span><span class='fd'>4</span></span>) is 1 of 4 equal parts.</li><li>The parts must be the same size.</li><li>2 halves make 1 whole. 4 quarters make 1 whole.</li><li>A half of a pizza is bigger than a quarter of the same pizza.</li></ul>",
        [example("Cut a cake into 4 equal parts", ["each part is 1 quarter"], "4 quarters = 1 whole")],
        [['Unequal parts', 'Halves and quarters must be equal.'], ['1/4 bigger than 1/2', 'More parts means smaller parts.'], ['Counting the cuts', 'Count the parts.']])
    faq = [('What does MATATAG Math 1 ask about fractions?', 'Illustrate 1/2 and 1/4 as parts of a whole, compare 1/2 and 1/4 using models, and count halves and quarters.'), ('Is a quarter the same as a fourth?', 'Yes.'), ('How many quarters are in a half?', '2.'), ('Why must parts be equal?', 'So everyone gets a fair share.')]
    make('halves-and-quarters', 20, 'Number and Algebra', 'Grade 1: Number and Algebra',
         'Illustrate 1/2 and 1/4 as parts of a whole; compare 1/2 and 1/4 using models; count halves and quarters.',
         'Halves and Quarters', 'Halves and Quarters',
         'Free Grade 1 halves and quarters worksheets for the DepEd MATATAG curriculum: equal parts, halves and quarters of shapes and amounts, comparing and counting. 100 questions with pictures and answers.',
         'A half is 1 of 2 equal parts; a quarter is 1 of 4.', '1/2 is bigger than 1/4 of the same whole.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
