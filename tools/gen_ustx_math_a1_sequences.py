# -*- coding: utf-8 -*-
"""
Texas Algebra I: Arithmetic and Geometric Sequences (TEKS A.12C, A.12D)
  python3 tools/gen_ustx_math_a1_sequences.py
Arithmetic or geometric, the nth term of arithmetic and geometric sequences, recursive and explicit formulas, and
sequence problems (the US Algebra 1 makers with a new seed and Texas names).
Wrong answers come from real mistakes: using n instead of n − 1, adding the ratio, and mixing up the first term and
the common difference.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a1_arithmetic_and_geometric_sequences as sq
adopt(sq)
sq.R = random.Random(695230)
tx_common.GRADE = "algebra-1"

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
        ("Arithmetic or geometric?", [("collect", W(sq.one_type), 20)]),
        ("The nth term of arithmetic sequences", [("collect", W(sq.one_nth), 20)]),
        ("Geometric sequences", [("collect", W(sq.one_geo), 20)]),
        ("Recursive and explicit formulas", [("collect", W(sq.one_rec), 20)]),
        ("Sequence problems", [("run", PR(sq.problems), ("rnd",), 10), ("collect", W(sq.one_nth), 10)]),
    ], 69523)
    finish(sets, R)
    body = lesson('<ul><li><b>Arithmetic</b>: add the same number <i>d</i> each time. <i>a</i><sub><i>n</i></sub> = <i>a</i><sub>1</sub> + (<i>n</i> − 1)<i>d</i>.</li><li><b>Geometric</b>: multiply by the same number <i>r</i>. <i>a</i><sub><i>n</i></sub> = <i>a</i><sub>1</sub> · <i>r</i><sup><i>n</i>−1</sup>.</li><li>A <b>recursive</b> formula uses the term before: <i>a</i><sub><i>n</i></sub> = <i>a</i><sub><i>n</i>−1</sub> + 4.</li></ul>',
        [example("5, 9, 13, 17, …: find <i>a</i><sub>20</sub>", ["<i>d</i> = 4", "5 + 19 × 4"], "81")],
        [['Using <i>n</i> instead of <i>n</i> − 1', 'The first term has no added <i>d</i>.'], ['Adding the ratio', 'Geometric means multiply.'], ['Mixing up <i>a</i><sub>1</sub> and <i>d</i>', '<i>a</i><sub>1</sub> is the first term.']])
    faq = [('What does TEKS A.12C ask?', 'Identify terms of arithmetic and geometric sequences when the sequences are given in function form using recursive processes.'), ('What does TEKS A.12D ask?', 'Write a formula for the nth term of arithmetic and geometric sequences, given the value of several of their terms.'), ('Is 2, 4, 8, 16 arithmetic?', 'No. It is geometric with r = 2.'), ('Is an arithmetic sequence a linear function?', 'Yes, on the whole numbers.')]
    make('arithmetic-and-geometric-sequences', 23, 'Algebraic Reasoning', 'A.12C, A.12D',
         'A.12C identify terms of arithmetic and geometric sequences when the sequences are given in function form using recursive processes; A.12D write a formula for the nth term of arithmetic and geometric sequences, given the value of several of their terms',
         'Arithmetic and Geometric Sequences', 'Arithmetic and Geometric Sequences',
         'Free Algebra I sequence worksheets for Texas TEKS A.12C and A.12D: arithmetic and geometric sequences, nth term formulas, recursive formulas and problems. 100 questions with answers.',
         'Arithmetic adds d; geometric multiplies by r.', 'aₙ = a₁ + (n − 1)d',
         body, faq, sets, seo_title='Algebra I Arithmetic and Geometric Sequences Worksheets (TEKS A.12D)')


if __name__ == "__main__":
    build()
