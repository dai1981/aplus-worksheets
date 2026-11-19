# -*- coding: utf-8 -*-
"""
Texas Geometry: Pythagorean Theorem and Special Right Triangles (TEKS G.9B, G.6D)
  python3 tools/gen_ustx_math_ge_pythagorean.py
Finding a missing side, acute, right or obtuse, 45°-45°-90° and 30°-60°-90° triangles, and word problems (the US
Geometry makers with a new seed and Texas names).
Wrong answers come from real mistakes: adding the legs without squaring, using √2 in a 30°-60°-90° triangle, and
putting the short leg opposite the 60° angle.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_ge_pythagorean_theorem_and_special_right_triangles as py
adopt(py)
py.R = random.Random(696170)
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
        ("Find a missing side", [("collect", W(py.one_side), 20)]),
        ("Acute, right or obtuse?", [("collect", W(py.one_conv), 20)]),
        ("45°-45°-90° triangles", [("collect", W(py.one_45), 20)]),
        ("30°-60°-90° triangles", [("collect", W(py.one_30), 20)]),
        ("Word problems", [("collect", W(py.one_word), 20)]),
    ], 69617)
    finish(sets, R)
    body = lesson('<ul><li><b>Pythagorean Theorem</b>: <i>a</i><sup>2</sup> + <i>b</i><sup>2</sup> = <i>c</i><sup>2</sup>, with <i>c</i> the hypotenuse.</li><li><b>Pythagorean triples</b>: 3-4-5, 5-12-13, 8-15-17, 7-24-25 and their multiples.</li><li><b>45°-45°-90°</b>: legs <i>x</i>, hypotenuse <i>x</i>√2.</li><li><b>30°-60°-90°</b>: short leg <i>x</i>, long leg <i>x</i>√3, hypotenuse 2<i>x</i>.</li></ul>',
        [example("30°-60°-90° with hypotenuse 14", ["short leg 7"], "long leg 7√3")],
        [['Adding without squaring', 'Square, add, then take the root.'], ['√2 in a 30°-60°-90° triangle', 'Use √3 and 2.'], ['Short leg opposite 60°', 'The short leg is opposite 30°.']])
    faq = [('What does TEKS G.9B ask?', 'Apply the relationships in special right triangles 30°-60°-90° and 45°-45°-90° and the Pythagorean theorem, including Pythagorean triples, to solve problems.'), ('How can I tell if a triangle is right?', 'Check whether a² + b² = c².'), ('Is 6-8-10 a Pythagorean triple?', 'Yes, it is 2 × 3-4-5.'), ('What is the hypotenuse of a 45-45-90 triangle with legs 5?', '5√2.')]
    make('pythagorean-theorem-and-special-right-triangles', 17, 'Similarity, Proof, and Trigonometry', 'G.9B, G.6D',
         'G.9B apply the relationships in special right triangles 30°-60°-90° and 45°-45°-90° and the Pythagorean theorem, including Pythagorean triples, to solve problems',
         'Pythagorean Theorem and Special Right Triangles', 'Pythagorean Theorem and Special Right Triangles',
         'Free Geometry worksheets for Texas TEKS G.9B: the Pythagorean Theorem, triples, the converse, and 45°-45°-90° and 30°-60°-90° triangles. 100 questions with answers.',
         'a² + b² = c²; 45-45-90: x√2; 30-60-90: x, x√3, 2x.', 'Hypotenuse 14 in 30-60-90: legs 7 and 7√3.',
         body, faq, sets, seo_title='Geometry Pythagorean Theorem and Special Right Triangles Worksheets (TEKS G.9B)')


if __name__ == "__main__":
    build()
