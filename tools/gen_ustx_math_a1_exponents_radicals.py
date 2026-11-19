# -*- coding: utf-8 -*-
"""
Texas Algebra I: Laws of Exponents and Simplifying Radicals (TEKS A.11A, A.11B)
  python3 tools/gen_ustx_math_a1_exponents_radicals.py
Simplifying square roots, adding and multiplying radicals, exponent rules, radicals and rational exponents, and
reasoning with exponents (the US Algebra 1 makers with a new seed and Texas names).
Wrong answers come from real mistakes: taking the square root of only part of the number, multiplying exponents when
multiplying powers, and reading x^(−2) as −x².
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a1_simplifying_radicals as rd
adopt(rd)
rd.R = random.Random(695220)
import gen_us_math_a1_rational_exponents as rx
adopt(rx)
rx.R = random.Random(695221)
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
        ("Simplify square roots", [("collect", W(rd.one_simp), 20)]),
        ("Add, subtract and multiply radicals", [("collect", W(rd.one_add), 10), ("collect", W(rd.one_mul), 10)]),
        ("Laws of exponents", [("collect", W(rx.one_rules), 20)]),
        ("Rational exponents", [("collect", W(rx.one_convert), 10), ("collect", W(rx.one_eval), 10)]),
        ("Simplify and reason with exponents", [("collect", W(rx.one_simp), 10), ("run", PR(rx.problems), ("rnd",), 10)]),
    ], 69522)
    finish(sets, R)
    body = lesson('<ul><li>√72 = √36 × √2 = 6√2: take out the largest perfect square.</li><li><i>x</i><sup><i>a</i></sup> · <i>x</i><sup><i>b</i></sup> = <i>x</i><sup><i>a</i>+<i>b</i></sup>; (<i>x</i><sup><i>a</i></sup>)<sup><i>b</i></sup> = <i>x</i><sup><i>ab</i></sup>; <i>x</i><sup><i>a</i></sup> ÷ <i>x</i><sup><i>b</i></sup> = <i>x</i><sup><i>a</i>−<i>b</i></sup>.</li><li><i>x</i><sup>0</sup> = 1 and <i>x</i><sup>−<i>n</i></sup> = 1 ÷ <i>x</i><sup><i>n</i></sup>.</li><li><i>x</i><sup>1/2</sup> = √<i>x</i>.</li></ul>',
        [example("√75", ["√25 × √3"], "5√3")],
        [['Rooting only part of the number', '√72 is 6√2, not 36√2.'], ['Multiplying exponents when multiplying powers', '<i>x</i><sup>2</sup> · <i>x</i><sup>3</sup> = <i>x</i><sup>5</sup>.'], ['Reading <i>x</i><sup>−2</sup> as −<i>x</i><sup>2</sup>', 'It is 1 ÷ <i>x</i><sup>2</sup>.']])
    faq = [('What does TEKS A.11A ask?', 'Simplify numerical radical expressions involving square roots.'), ('What does TEKS A.11B ask?', 'Simplify numeric and algebraic expressions using the laws of exponents, including integral and rational exponents.'), ('What is 8<sup>2/3</sup>?', '4, because the cube root of 8 is 2 and 2² = 4.'), ('Can √2 + √3 be simplified?', 'No. Only like radicals combine.')]
    make('exponents-and-radicals', 22, 'Number and Algebraic Methods', 'A.11A, A.11B',
         'A.11A simplify numerical radical expressions involving square roots; A.11B simplify numeric and algebraic expressions using the laws of exponents, including integral and rational exponents',
         'Laws of Exponents and Simplifying Radicals', 'Exponents and Radicals',
         'Free Algebra I worksheets for Texas TEKS A.11A and A.11B: simplify square roots, add and multiply radicals, laws of exponents and rational exponents. 100 questions with answers.',
         'Take out perfect squares; add exponents when multiplying.', '√75 = 5√3 and x² · x³ = x⁵.',
         body, faq, sets, seo_title='Algebra I Exponents and Radicals Worksheets (TEKS A.11A, A.11B)')


if __name__ == "__main__":
    build()
