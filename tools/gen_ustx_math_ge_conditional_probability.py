# -*- coding: utf-8 -*-
"""
Texas Geometry: Independent Events and Conditional Probability (TEKS G.13C, G.13D, G.13E)
  python3 tools/gen_ustx_math_ge_conditional_probability.py
The Addition Rule and complements, independent events, conditional probability, two-way tables, and drawing with and
without replacement (the US Geometry makers with a new seed and Texas names).
Wrong answers come from real mistakes: multiplying dependent probabilities as if independent, dividing by the wrong
total, and counting the overlap twice.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_ge_conditional_probability as cp
adopt(cp)
cp.R = random.Random(696290)
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
        ("The Addition Rule and complements", [("collect", W(cp.one_add), 20)]),
        ("Independent events", [("collect", W(cp.one_ind), 20)]),
        ("Conditional probability", [("collect", W(cp.one_cond), 20)]),
        ("Two-way tables", [("collect", W(cp.one_table), 20)]),
        ("With and without replacement", [("collect", W(cp.one_draw), 20)]),
    ], 69629)
    finish(sets, R)
    body = lesson('<ul><li>Events are <b>independent</b> if one does not change the other: P(A and B) = P(A) × P(B).</li><li><b>Conditional probability</b>: P(B | A) = P(A and B) ÷ P(A).</li><li><b>Without replacement</b>, the second draw has one fewer item.</li><li>P(A or B) = P(A) + P(B) − P(A and B).</li></ul>',
        [example("Draw 2 red from 5 red and 3 blue without replacement", ["5/8 × 4/7"], "20/56 = 5/14")],
        [['Treating dependent events as independent', 'Without replacement, update the second fraction.'], ['Dividing by the wrong total', "Given A, divide by A's total."], ['Counting the overlap twice', 'Subtract P(A and B).']])
    faq = [('What does TEKS G.13C ask?', 'Identify whether two events are independent and compute the probability of the two events occurring together with or without replacement.'), ('What does TEKS G.13D ask?', 'Apply conditional probability in contextual problems.'), ('What does TEKS G.13E ask?', 'Apply independence in contextual problems.'), ('Are coin flips independent?', 'Yes.')]
    make('independent-and-conditional-probability', 29, 'Probability', 'G.13C, G.13D, G.13E',
         'G.13C identify whether two events are independent and compute the probability of the two events occurring together with or without replacement; G.13D apply conditional probability in contextual problems; G.13E apply independence in contextual problems',
         'Independent Events and Conditional Probability', 'Independent and Conditional Probability',
         'Free Geometry probability worksheets for Texas TEKS G.13C–G.13E: independent events, conditional probability, two-way tables and drawing with and without replacement. 100 questions with answers.',
         'Independent: P(A and B) = P(A) × P(B).', 'P(B | A) = P(A and B) ÷ P(A).',
         body, faq, sets, seo_title='Geometry Independent and Conditional Probability Worksheets (TEKS G.13C)')


if __name__ == "__main__":
    build()
