# -*- coding: utf-8 -*-
"""
Texas Geometry: Conditional Statements, Converses and Counterexamples (TEKS G.4B, G.4C)
  python3 tools/gen_ustx_math_ge_conditional_statements.py
Hypothesis and conclusion, converse, inverse and contrapositive, counterexamples and truth values, laws of logic, and
reasons in a proof (the US Geometry makers with a new seed and Texas names).
Wrong answers come from real mistakes: swapping the inverse and the converse, thinking a true statement has a true
converse, and giving an example instead of a counterexample.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_ge_conditional_statements_and_proof as cs
adopt(cs)
cs.R = random.Random(696020)
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
        ("Hypothesis and conclusion", [("collect", W(cs.one_hc), 20)]),
        ("Converse, inverse and contrapositive", [("collect", W(cs.one_cic), 20)]),
        ("Counterexamples and truth values", [("collect", W(cs.one_ce), 20)]),
        ("Laws of Detachment and Syllogism", [("collect", W(cs.one_law), 20)]),
        ("Reasons in a proof", [("collect", W(cs.one_prop), 20)]),
    ], 69602)
    finish(sets, R)
    body = lesson('<ul><li>A <b>conditional</b>: if <i>p</i>, then <i>q</i>. <i>p</i> is the hypothesis, <i>q</i> the conclusion.</li><li><b>Converse</b>: if <i>q</i>, then <i>p</i>. <b>Inverse</b>: if not <i>p</i>, then not <i>q</i>. <b>Contrapositive</b>: if not <i>q</i>, then not <i>p</i>.</li><li>A conditional and its contrapositive are always both true or both false.</li><li>A <b>biconditional</b> (<i>p</i> if and only if <i>q</i>) is true when the conditional and its converse are both true.</li><li>One <b>counterexample</b> shows a statement is false.</li></ul>',
        [example("If an angle is 30°, then it is acute.", ["converse: if an angle is acute, it is 30°"], "converse false (60° is acute)")],
        [['Swapping inverse and converse', 'Converse swaps; inverse negates.'], ['Assuming the converse is true', 'Check it separately.'], ['Giving an example instead of a counterexample', 'It must make the hypothesis true and the conclusion false.']])
    faq = [('What does TEKS G.4B ask?', 'Identify and determine the validity of the converse, inverse, and contrapositive of a conditional statement and recognize the connection between a biconditional statement and a true conditional statement with a true converse.'), ('What does TEKS G.4C ask?', 'Verify that a conjecture is false using a counterexample.'), ('Which statement always has the same truth value as the conditional?', 'The contrapositive.'), ('What is a biconditional?', 'A statement with “if and only if”.')]
    make('conditional-statements-and-counterexamples', 2, 'Logical Argument and Constructions', 'G.4B, G.4C',
         'G.4B identify and determine the validity of the converse, inverse, and contrapositive of a conditional statement and recognize the connection between a biconditional statement and a true conditional statement with a true converse; G.4C verify that a conjecture is false using a counterexample',
         'Conditional Statements, Converses and Counterexamples', 'Conditional Statements',
         'Free Geometry worksheets for Texas TEKS G.4B and G.4C: conditional statements, converse, inverse, contrapositive, biconditionals and counterexamples. 100 questions with answers.',
         'A conditional and its contrapositive have the same truth value.', 'One counterexample proves a statement false.',
         body, faq, sets, seo_title='Geometry Conditional Statements and Counterexamples Worksheets (TEKS G.4B)')


if __name__ == "__main__":
    build()
