# -*- coding: utf-8 -*-
"""
Texas Algebra I: Functions and Function Notation (TEKS A.12A, A.12B)
  python3 tools/gen_ustx_math_a1_functions.py
Is it a function? (relations and graphs, US Grade 8 makers with a new seed), evaluating f(x), solving f(x) = k, and
function notation in context (US Algebra 1 makers with a new seed and Texas names).
Wrong answers come from real mistakes: thinking a repeated output breaks a function, reading f(x) as f times x, and
mixing up f(3) with f(x) = 3.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g8_functions as fg
adopt(fg)
fg.R = random.Random(695010)
import gen_us_math_a1_function_notation as fn
adopt(fn)
fn.R = random.Random(695011)
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
        ("Is it a function? Ordered pairs, tables and mappings", [("run", fg.set_relations, (), 20)]),
        ("Is it a function? Graphs", [("run", fg.set_graphs, (), 20)]),
        ("Evaluate f(x)", [("collect", W(fn.one_eval), 20)]),
        ("Solve f(x) = k and use tables", [("collect", W(fn.one_solve), 12), ("collect", W(fn.one_table), 8)]),
        ("Function notation in context", [("run", PR(fn.problems), ("rnd",), 10), ("collect", W(fn.one_expr), 10)]),
    ], 69501)
    finish(sets, R)
    body = lesson('<ul><li>A <b>function</b> gives exactly one output for each input. An input may not repeat with a different output.</li><li>On a graph, use the <b>vertical line test</b>: no vertical line may cross the graph twice.</li><li><i>f</i>(<i>x</i>) is read “<i>f</i> of <i>x</i>”: the output when the input is <i>x</i>. It does not mean <i>f</i> times <i>x</i>.</li><li>To find <i>f</i>(−2), replace every <i>x</i> with (−2).</li></ul>',
        [example("<i>f</i>(<i>x</i>) = 3<i>x</i><sup>2</sup> − 4. Find <i>f</i>(−2).", ["3(−2)<sup>2</sup> − 4 = 12 − 4"], "8")],
        [['Thinking a repeated output breaks a function', 'Two inputs may share an output.'], ['Reading <i>f</i>(<i>x</i>) as <i>f</i> times <i>x</i>', 'It names the output.'], ['Mixing up <i>f</i>(3) and <i>f</i>(<i>x</i>) = 3', '<i>f</i>(3) gives an input; <i>f</i>(<i>x</i>) = 3 gives an output.']])
    faq = [('What does TEKS A.12A ask?', 'Decide whether relations represented verbally, tabularly, graphically, and symbolically define a function.'), ('What does TEKS A.12B ask?', 'Evaluate functions, expressed in function notation, given one or more elements in their domains.'), ('Is a horizontal line a function?', 'Yes. Every input has one output.'), ('Is a vertical line a function?', 'No. One input has many outputs.')]
    make('functions-and-function-notation', 1, 'Algebraic Reasoning', 'A.12A, A.12B',
         'A.12A decide whether relations represented verbally, tabularly, graphically, and symbolically define a function; A.12B evaluate functions, expressed in function notation, given one or more elements in their domains',
         'Functions and Function Notation', 'Functions and Function Notation',
         'Free Algebra I worksheets for Texas TEKS A.12A and A.12B: decide if a relation is a function, the vertical line test, evaluate f(x), solve f(x) = k and function notation in context. 100 questions with answers.',
         'One input, exactly one output.', 'f(3) is the output when the input is 3.',
         body, faq, sets, seo_title='Algebra I Functions and Function Notation Worksheets (TEKS A.12A, A.12B)')


if __name__ == "__main__":
    build()
