# -*- coding: utf-8 -*-
"""
Texas Algebra I: Correlation, Causation and Lines of Fit (TEKS A.4A, A.4B, A.4C)
  python3 tools/gen_ustx_math_a1_correlation.py
Describing scatter plots, the correlation coefficient, lines of fit in context, residuals, and correlation versus
causation (the US Algebra 1 makers with a new seed and Texas names).
Wrong answers come from real mistakes: thinking r = −0.9 is weak, reading correlation as causation, and subtracting
the residual the wrong way.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a1_correlation_and_residuals as cr
adopt(cr)
cr.R = random.Random(695120)
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
        ("Describe a scatter plot", [("collect", W(cr.one_scatter), 20)]),
        ("The correlation coefficient", [("collect", W(cr.one_r), 14), ("collect", W(cr.one_scatter), 6)]),
        ("Lines of fit in context", [("collect", W(cr.one_fit), 20)]),
        ("Residuals", [("collect", W(cr.one_res), 20)]),
        ("Correlation and causation", [("run", PR(cr.problems), ("rnd",), 10), ("collect", W(cr.one_fit), 10)]),
    ], 69512)
    finish(sets, R)
    body = lesson('<ul><li>The <b>correlation coefficient</b> <i>r</i> is between −1 and 1. Close to 1 or −1: strong. Close to 0: weak.</li><li>The sign tells the direction: positive up, negative down.</li><li>A <b>line of fit</b> predicts <i>y</i> from <i>x</i>. Residual = actual − predicted.</li><li><b>Correlation is not causation</b>: two things can rise together without one causing the other.</li></ul>',
        [example("<i>r</i> = −0.92", ["close to −1"], "strong negative")],
        [['Thinking negative means weak', '−0.9 is strong.'], ['Reading correlation as causation', 'Look for another cause.'], ['Residual the wrong way', 'Actual minus predicted.']])
    faq = [('What does TEKS A.4A ask?', 'Calculate, using technology, the correlation coefficient between two quantitative variables and interpret this quantity as a measure of the strength of the linear association.'), ('What does TEKS A.4B ask?', 'Compare and contrast association and causation in real-world problems.'), ('What does TEKS A.4C ask?', 'Write, with and without technology, linear functions that provide a reasonable fit to data to estimate solutions and make predictions for real-world problems.'), ('What does r = 0 mean?', 'No linear association.')]
    make('correlation-and-lines-of-fit', 12, 'Linear Functions, Equations, and Inequalities', 'A.4A, A.4B, A.4C',
         'A.4A calculate, using technology, the correlation coefficient between two quantitative variables and interpret this quantity as a measure of the strength of the linear association; A.4B compare and contrast association and causation in real-world problems; A.4C write, with and without technology, linear functions that provide a reasonable fit to data to estimate solutions and make predictions for real-world problems',
         'Correlation, Causation and Lines of Fit', 'Correlation and Lines of Fit',
         'Free Algebra I worksheets for Texas TEKS A.4A–A.4C: scatter plots, the correlation coefficient, lines of fit, residuals and correlation versus causation. 100 questions with answers.',
         'r near ±1 is strong; near 0 is weak.', 'Correlation is not causation.',
         body, faq, sets, seo_title='Algebra I Correlation and Lines of Fit Worksheets (TEKS A.4A)')


if __name__ == "__main__":
    build()
