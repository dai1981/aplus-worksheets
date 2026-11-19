# -*- coding: utf-8 -*-
"""
Texas Precalculus: The Law of Sines and the Law of Cosines (TEKS P.4G, P.4H)
  python3 tools/gen_ustx_math_pc_laws_sines_cosines.py
Area with ½ab sin C, finding sides and angles with the Law of Sines, finding sides with the Law of Cosines, and
choosing a law (US Geometry makers with a new seed).
Wrong answers come from real mistakes: pairing a side with the wrong angle, forgetting the second (obtuse) angle, and
using + 2ab cos C.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_ge_law_of_sines_and_cosines as lsc
adopt(lsc)
lsc.R = random.Random(698190)
tx_common.GRADE = "precalculus"

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
def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


from fractions import Fraction as Fr


def ft(v):
    v = Fr(v)
    if v.denominator == 1:
        return sg(int(v))
    return (MINUS if v < 0 else "") + fr(abs(v.numerator), v.denominator)


def fx(body, name="f"):
    return "<i>%s</i>(<i>x</i>) = %s" % (name, body)



def build():
    sets, R = build_sets([
        ("Area of a triangle", [("collect", W(lsc.one_area), 20)]),
        ("Law of Sines: find a side", [("collect", W(lsc.one_ls_side), 20)]),
        ("Law of Sines: find an angle", [("collect", W(lsc.one_ls_ang), 20)]),
        ("Law of Cosines: find a side", [("collect", W(lsc.one_lc_side), 20)]),
        ("Choose and use a law", [("collect", W(lsc.one_mix), 20)]),
    ], 69819)
    finish(sets, R)
    body = lesson("<ul><li><b>Law of Sines</b>: <span class='fr'><span class='fn'><i>a</i></span><span class='fd'>sin <i>A</i></span></span> = <span class='fr'><span class='fn'><i>b</i></span><span class='fd'>sin <i>B</i></span></span> = <span class='fr'><span class='fn'><i>c</i></span><span class='fd'>sin <i>C</i></span></span>. Use it with two angles and a side, or two sides and an angle opposite one of them.</li><li><b>Law of Cosines</b>: <i>c</i><sup>2</sup> = <i>a</i><sup>2</sup> + <i>b</i><sup>2</sup> − 2<i>ab</i> cos <i>C</i>. Use it with two sides and the angle between them, or three sides.</li><li>Area = <span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span><i>ab</i> sin <i>C</i>.</li></ul>",
        [example("<i>a</i> = 7, <i>b</i> = 9, <i>C</i> = 60°", ["<i>c</i><sup>2</sup> = 49 + 81 − 2(7)(9)(0.5) = 67"], "<i>c</i> ≈ 8.2")],
        [['Pairing a side with the wrong angle', 'Side <i>a</i> is opposite angle <i>A</i>.'], ['Missing the obtuse angle', 'sin <i>B</i> = 0.6 gives <i>B</i> ≈ 36.9° or 143.1°.'], ['+ 2<i>ab</i> cos <i>C</i>', 'The Law of Cosines subtracts.']])
    faq = [('What does TEKS P.4G ask?', 'Use the Law of Sines in mathematical and real-world problems.'), ('What does TEKS P.4H ask?', 'Use the Law of Cosines in mathematical and real-world problems.'), ('What is the ambiguous case?', 'SSA: two sides and a non-included angle may give 0, 1 or 2 triangles.'), ('Does the Law of Cosines work for right triangles?', 'Yes: cos 90° = 0, so it becomes the Pythagorean theorem.')]
    make('law-of-sines-and-law-of-cosines', 19, 'Number and Measure', 'P.4G, P.4H',
         'P.4G use the Law of Sines in mathematical and real-world problems; P.4H use the Law of Cosines in mathematical and real-world problems',
         'The Law of Sines and the Law of Cosines', 'Law of Sines and Cosines',
         'Free Precalculus worksheets on the Law of Sines and the Law of Cosines for Texas TEKS P.4G and P.4H: missing sides and angles, triangle area and choosing a law. 100 questions with answers.',
         'Law of Sines: a/sin A = b/sin B = c/sin C.', 'Law of Cosines: c² = a² + b² − 2ab cos C.',
         body, faq, sets, seo_title='Precalculus Law of Sines and Law of Cosines Worksheets (TEKS P.4G, P.4H)')


if __name__ == "__main__":
    build()
