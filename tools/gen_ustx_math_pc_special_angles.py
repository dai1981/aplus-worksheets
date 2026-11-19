# -*- coding: utf-8 -*-
"""
Texas Precalculus: Trigonometric Values of Special Angles (TEKS P.2P, P.4A, P.4E)
  python3 tools/gen_ustx_math_pc_special_angles.py
Exact values of sine, cosine and tangent at special angles, points on the unit circle, the reciprocal functions,
and finding other ratios from one ratio and a quadrant (US Algebra 2 and Precalculus makers with a new seed).
Wrong answers come from real mistakes: the wrong sign for the quadrant, swapping sine and cosine, and flipping a ratio
that should not be flipped.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_a2_unit_circle_and_radians as uc
adopt(uc)
uc.R = random.Random(698100)
import gen_us_math_pc_six_trigonometric_functions as six
adopt(six)
six.R = random.Random(698101)
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
        ("Exact values of sine, cosine and tangent", [("collect", W(uc.one_exact), 20)]),
        ("Points on the unit circle", [("collect", W(uc.one_sign), 20)]),
        ("Secant, cosecant and cotangent", [("collect", W(six.one_rec), 20)]),
        ("One ratio and a quadrant", [("collect", W(uc.one_id), 20)]),
        ("Find the other ratios", [("collect", W(six.one_other), 20)]),
    ], 69810)
    finish(sets, R)
    body = lesson('<ul><li>On the unit circle, the point at angle θ is (cos θ, sin θ), and tan θ = sin θ ÷ cos θ.</li><li>Special angles: 30° (π/6), 45° (π/4), 60° (π/3) and their reference angles in every quadrant.</li><li>Signs: All positive in Quadrant I, Sine in II, Tangent in III, Cosine in IV.</li><li>csc θ = 1 ÷ sin θ, sec θ = 1 ÷ cos θ, cot θ = 1 ÷ tan θ.</li></ul>',
        [example("cos 240°", ["Reference angle 60°", "Quadrant III: cosine is negative"], "−<span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>")],
        [['The wrong sign', 'Check the quadrant first.'], ['Swapping sine and cosine', 'The <i>x</i>-coordinate is cosine.'], ['Flipping the wrong ratio', 'sec goes with cos, csc goes with sin.']])
    faq = [('What does TEKS P.2P ask?', 'Determine the values of the trigonometric functions at the special angles and relate them in mathematical and real-world problems.'), ('What does TEKS P.4A ask?', 'Determine the relationship between the unit circle and the definition of a periodic function to evaluate trigonometric functions in mathematical and real-world problems.'), ('What does TEKS P.4E ask?', 'Determine the value of trigonometric ratios of angles and solve problems involving trigonometric ratios in mathematical and real-world problems.'), ('Why are trig functions periodic?', 'Going once around the unit circle brings you back to the same point.')]
    make('trigonometric-values-of-special-angles', 10, 'Number and Measure', 'P.2P, P.4A, P.4E',
         'P.2P determine the values of the trigonometric functions at the special angles and relate them in mathematical and real-world problems; P.4A determine the relationship between the unit circle and the definition of a periodic function to evaluate trigonometric functions in mathematical and real-world problems; P.4E determine the value of trigonometric ratios of angles and solve problems involving trigonometric ratios in mathematical and real-world problems',
         'Trigonometric Values of Special Angles', 'Special Angle Values',
         'Free Precalculus worksheets for Texas TEKS P.2P, P.4A and P.4E: exact trig values of special angles, unit circle points, reciprocal functions and ratios from a quadrant. 100 questions with answers.',
         'The point at angle θ on the unit circle is (cos θ, sin θ).', 'All, Sine, Tangent, Cosine: the positive ratios in Quadrants I to IV.',
         body, faq, sets, seo_title='Precalculus Trigonometric Values of Special Angles Worksheets (TEKS P.2P, P.4A, P.4E)')


if __name__ == "__main__":
    build()
