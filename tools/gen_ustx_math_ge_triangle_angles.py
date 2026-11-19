# -*- coding: utf-8 -*-
"""
Texas Geometry: Triangle Angle Sum, Exterior Angles and Isosceles Triangles (TEKS G.6D, G.5A)
  python3 tools/gen_ustx_math_ge_triangle_angles.py
The Triangle Angle Sum Theorem, the Exterior Angle Theorem, solving for x, isosceles and equilateral triangles, and
classifying triangles (the US Geometry makers with a new seed and Texas names).
Wrong answers come from real mistakes: adding the exterior angle to the remote angles, using the vertex angle as a
base angle, and forgetting the sum is 180°.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_ge_triangle_angle_theorems as ta
adopt(ta)
ta.R = random.Random(696090)
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
        ("Triangle Angle Sum Theorem", [("collect", W(ta.one_sum), 20)]),
        ("Exterior Angle Theorem", [("collect", W(ta.one_ext), 20)]),
        ("Solve for x", [("collect", W(ta.one_alg), 20)]),
        ("Isosceles and equilateral triangles", [("collect", W(ta.one_iso), 20)]),
        ("Classify triangles and word problems", [("collect", W(ta.one_word), 20)]),
    ], 69609)
    finish(sets, R)
    body = lesson('<ul><li>The angles of a triangle add to <b>180°</b>.</li><li>An <b>exterior angle</b> equals the sum of the two remote interior angles.</li><li>The <b>base angles</b> of an isosceles triangle are congruent. Each angle of an equilateral triangle is 60°.</li></ul>',
        [example("Remote angles 47° and 68°", ["47 + 68"], "exterior angle 115°")],
        [['Adding the exterior angle to the remote angles', 'The exterior angle equals their sum.'], ['Using the vertex angle as a base angle', 'Base angles are opposite the equal sides.'], ['Forgetting 180°', 'All three angles add to 180°.']])
    faq = [('What does TEKS G.6D ask?', 'Verify theorems about the relationships in triangles, including proof of the Pythagorean Theorem, the sum of interior angles, base angles of isosceles triangles, midsegments, and medians, and apply these relationships to solve problems.'), ('Can a triangle have two right angles?', 'No. Two right angles already make 180°.'), ('What is an exterior angle?', 'An angle formed by one side and the extension of another.'), ('Are the base angles always acute?', 'Yes.')]
    make('triangle-angle-theorems', 9, 'Proof and Congruence', 'G.6D, G.5A',
         'G.6D verify theorems about the relationships in triangles, including proof of the Pythagorean Theorem, the sum of interior angles, base angles of isosceles triangles, midsegments, and medians, and apply these relationships to solve problems',
         'Triangle Angle Sum, Exterior Angles and Isosceles Triangles', 'Triangle Angle Theorems',
         'Free Geometry worksheets for Texas TEKS G.6D: triangle angle sum, exterior angles, solving for x, and isosceles and equilateral triangles. 100 questions with answers.',
         'Angles add to 180°; exterior = sum of remote interior.', 'Isosceles: base angles are congruent.',
         body, faq, sets, seo_title='Geometry Triangle Angle Theorems Worksheets (TEKS G.6D)')


if __name__ == "__main__":
    build()
