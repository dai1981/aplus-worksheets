# -*- coding: utf-8 -*-
"""
Texas Geometry: Permutations and Combinations (TEKS G.13A)
  python3 tools/gen_ustx_math_ge_counting.py
The counting principle, permutations, combinations, deciding if order matters, and probability by counting (the US
Precalculus makers with a new seed and Texas names).
Wrong answers come from real mistakes: adding instead of multiplying, using a permutation when order does not matter,
and dividing by the wrong factorial.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_pc_permutations_and_combinations as pm
adopt(pm)
pm.R = random.Random(696270)
tx_common.GRADE = "geometry"

import us_hs
adopt(us_hs)


def W(fn, keep=None):
    """Use an item maker of another generator: its odd failures count as a skipped try, and a question text
    is used only once (not again with other wrong answers)."""
    seen = set()

    def f(r):
        try:
            it = fn(r)
        except (TypeError, ValueError, ZeroDivisionError, IndexError, KeyError):
            raise AssertionError("skip")
        if not it or (keep and not keep(it)) or it["q"] in seen:
            raise AssertionError("skip")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


def PR(fn, keep=None):
    """A fixed word-problem list of another generator as a set maker: a shuffled share of it."""
    def f(r):
        its = [it for it in fn() if keep is None or keep(it)]
        r.shuffle(its)
        return {"title": fn.__name__, "items": its * 3}
    f.__name__ = fn.__name__
    return f


MINUS = "−"
X = "<i>x</i>"


def sg(v):
    return ("−%s" % abs(v)) if v < 0 else str(v)


def poly(cs, v="<i>x</i>"):
    """[a, b, c] highest power first, e.g. 2x² − 3x + 1."""
    deg = len(cs) - 1
    out = ""
    for i, c in enumerate(cs):
        if c == 0:
            continue
        p = deg - i
        mag = abs(c)
        if p == 0:
            body = str(mag)
        else:
            body = ("" if mag == 1 else str(mag)) + v + ("<sup>%d</sup>" % p if p > 1 else "")
        if not out:
            out = (MINUS if c < 0 else "") + body
        else:
            out += (" − " if c < 0 else " + ") + body
    return out or "0"


def build():
    sets, R = build_sets([
        ("The counting principle", [("collect", W(pm.one_fcp), 20)]),
        ("Permutations", [("collect", W(pm.one_perm), 20)]),
        ("Combinations", [("collect", W(pm.one_comb), 20)]),
        ("Does order matter?", [("collect", W(pm.one_which), 20)]),
        ("Probability by counting", [("collect", W(pm.one_prob), 20)]),
    ], 69627)
    finish(sets, R)
    body = lesson('<ul><li><b>Counting principle</b>: multiply the number of choices at each step.</li><li><b>Permutation</b> (order matters): <sub><i>n</i></sub>P<sub><i>r</i></sub> = <i>n</i>! ÷ (<i>n</i> − <i>r</i>)!.</li><li><b>Combination</b> (order does not matter): <sub><i>n</i></sub>C<sub><i>r</i></sub> = <i>n</i>! ÷ (<i>r</i>!(<i>n</i> − <i>r</i>)!).</li><li>Probability = favorable outcomes ÷ total outcomes.</li></ul>',
        [example("Choose a president and a treasurer from 10 people", ["order matters", "10 × 9"], "90")],
        [['Adding instead of multiplying', 'Multiply the choices.'], ['Permutation when order does not matter', 'A team of 3 is a combination.'], ['Dividing by the wrong factorial', 'Combinations divide by <i>r</i>!.']])
    faq = [('What does TEKS G.13A ask?', 'Develop strategies to use permutations and combinations to solve contextual problems.'), ('What is 0!?', '1.'), ('Is a lock code a permutation?', 'Yes, order matters.'), ('Is choosing 3 toppings a combination?', 'Yes, order does not matter.')]
    make('permutations-and-combinations', 27, 'Probability', 'G.13A',
         'G.13A develop strategies to use permutations and combinations to solve contextual problems',
         'Permutations and Combinations', 'Permutations and Combinations',
         'Free Geometry probability worksheets for Texas TEKS G.13A: the counting principle, permutations, combinations and probability by counting. 100 questions with answers.',
         'Order matters: permutation. Order does not: combination.', '10P2 = 90; 10C2 = 45.',
         body, faq, sets, seo_title='Geometry Permutations and Combinations Worksheets (TEKS G.13A)')


if __name__ == "__main__":
    build()
