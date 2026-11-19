# -*- coding: utf-8 -*-
"""
Texas Algebra I: Literal Equations: Solving Formulas for a Variable (TEKS A.12E)
  python3 tools/gen_ustx_math_a1_literal_equations.py
Solving for a variable in one or two steps, parentheses, fractions and factoring out, formulas from math and science,
and using rearranged formulas (the US Algebra 1 makers with a new seed and Texas names).
Wrong answers come from real mistakes: undoing operations in the wrong order, dividing only one term, and losing a
negative sign.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a1_literal_equations as le
adopt(le)
le.R = random.Random(695240)
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
        ("Solve for a variable in one or two steps", [("collect", W(le.one_step), 8), ("collect", W(le.two_step), 12)]),
        ("Solve for y", [("collect", W(le.one_std), 20)]),
        ("Parentheses, fractions and factoring out", [("collect", W(le.brackets), 14), ("collect", W(le.one_factor_out), 6)]),
        ("Formulas from math and science", [("run", PR(le.real_items), ("rnd",), 10), ("collect", W(le.two_step), 10)]),
        ("Using rearranged formulas", [("run", PR(le.problems), ("rnd",), 10), ("collect", W(le.brackets), 10)]),
    ], 69524)
    finish(sets, R)
    body = lesson('<ul><li>Treat the other letters like numbers.</li><li>Undo operations in reverse order: first addition or subtraction, then multiplication or division.</li><li>Do the same thing to <b>both sides</b> and to <b>every term</b>.</li><li>If the variable appears twice, collect those terms and factor it out.</li></ul>',
        [example("Solve <i>A</i> = <i>lw</i> for <i>w</i>", ["divide both sides by <i>l</i>"], "<i>w</i> = <i>A</i> ÷ <i>l</i>")],
        [['Undoing in the wrong order', 'Undo + and − first.'], ['Dividing only one term', 'Divide every term.'], ['Losing a negative sign', 'Check by putting values in.']])
    faq = [('What does TEKS A.12E ask?', 'Solve mathematic and scientific formulas, and other literal equations, for a specified variable.'), ('What is a literal equation?', 'An equation with two or more letters.'), ('Why rearrange a formula?', 'To find a different quantity quickly.'), ('How do I check?', 'Pick numbers and see if both forms agree.')]
    make('literal-equations-and-formulas', 24, 'Algebraic Reasoning', 'A.12E',
         'A.12E solve mathematic and scientific formulas, and other literal equations, for a specified variable',
         'Literal Equations: Solving Formulas for a Variable', 'Literal Equations',
         'Free Algebra I literal equation worksheets for Texas TEKS A.12E: solve formulas for a variable, standard form to slope-intercept form, science formulas and applications. 100 questions with answers.',
         'Treat the other letters like numbers.', 'A = lw, so w = A ÷ l.',
         body, faq, sets, seo_title='Algebra I Literal Equations Worksheets (TEKS A.12E)')


if __name__ == "__main__":
    build()
