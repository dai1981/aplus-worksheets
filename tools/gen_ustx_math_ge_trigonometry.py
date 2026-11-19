# -*- coding: utf-8 -*-
"""
Texas Geometry: Trigonometric Ratios: Sine, Cosine and Tangent (TEKS G.9A)
  python3 tools/gen_ustx_math_ge_trigonometry.py
Labeling sides and choosing a ratio, finding a side, finding the hypotenuse or adjacent side, finding an angle, and
word problems (the US Geometry makers with a new seed and Texas names).
Wrong answers come from real mistakes: mixing up opposite and adjacent, multiplying when you should divide, and using
sin instead of sin⁻¹.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_ge_right_triangle_trigonometry as tg
adopt(tg)
tg.R = random.Random(696180)
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
        ("Label the sides and choose a ratio", [("collect", W(tg.one_label), 20)]),
        ("Find a side", [("collect", W(tg.one_side_mul), 20)]),
        ("Find the hypotenuse or adjacent side", [("collect", W(tg.one_side_div), 20)]),
        ("Find an angle", [("collect", W(tg.one_angle), 20)]),
        ("Word problems", [("run", PR(tg.problems), ("rnd",), 10), ("collect", W(tg.one_angle), 10)]),
    ], 69618)
    finish(sets, R)
    body = lesson('<ul><li><b>SOH-CAH-TOA</b>: sin = opposite ÷ hypotenuse, cos = adjacent ÷ hypotenuse, tan = opposite ÷ adjacent.</li><li>Opposite and adjacent depend on which angle you use.</li><li>Unknown on top: multiply. Unknown on the bottom: divide.</li><li>Find an angle with sin<sup>−1</sup>, cos<sup>−1</sup> or tan<sup>−1</sup>.</li></ul>',
        [example("Angle 35°, hypotenuse 20, find the opposite side", ["sin 35° = <i>x</i>/20"], "<i>x</i> ≈ 11.5")],
        [['Mixing up opposite and adjacent', 'Opposite is across from the angle.'], ['Multiplying instead of dividing', 'If <i>x</i> is on the bottom, divide.'], ['Using sin instead of sin<sup>−1</sup>', 'Use the inverse to find an angle.']])
    faq = [('What does TEKS G.9A ask?', 'Determine the lengths of sides and measures of angles in a right triangle by applying the trigonometric ratios sine, cosine, and tangent to solve problems.'), ('Should the calculator be in degrees?', 'Yes, for these problems.'), ('What is an angle of elevation?', 'The angle up from horizontal to a line of sight.'), ('Can sin be more than 1?', 'No.')]
    make('trigonometric-ratios', 18, 'Similarity, Proof, and Trigonometry', 'G.9A',
         'G.9A determine the lengths of sides and measures of angles in a right triangle by applying the trigonometric ratios sine, cosine, and tangent to solve problems',
         'Trigonometric Ratios: Sine, Cosine and Tangent', 'Trigonometric Ratios',
         'Free Geometry trigonometry worksheets for Texas TEKS G.9A: sine, cosine and tangent, finding sides and angles of right triangles and word problems. 100 questions with answers.',
         'SOH-CAH-TOA.', 'sin 35° = x/20, so x ≈ 11.5.',
         body, faq, sets, seo_title='Geometry Trigonometric Ratios Worksheets (TEKS G.9A)')


if __name__ == "__main__":
    build()
