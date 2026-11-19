# -*- coding: utf-8 -*-
"""
Texas Geometry: Transformations: Translations, Reflections, Rotations and Dilations (TEKS G.3A, G.3B, G.3C)
  python3 tools/gen_ustx_math_ge_transformations.py
Translations, reflections, rotations, identifying and composing transformations (US Geometry makers), and dilations
with any center (US Geometry maker), with a new seed.
Wrong answers come from real mistakes: changing the wrong coordinate, rotating the wrong way, and dilating from the
origin when the center is another point.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_ge_rigid_transformations as rt
adopt(rt)
rt.R = random.Random(696070)
import gen_us_math_ge_dilations_and_similarity as dl
adopt(dl)
dl.R = random.Random(696071)
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
        ("Translations", [("collect", W(rt.one_tr), 20)]),
        ("Reflections", [("collect", W(rt.one_ref), 20)]),
        ("Rotations about the origin", [("collect", W(rt.one_rot), 20)]),
        ("Identify and compose transformations", [("collect", W(rt.one_id), 20)]),
        ("Dilations, including other centers", [("collect", W(dl.one_ctr), 10), ("collect", W(dl.one_org), 10)]),
    ], 69607)
    finish(sets, R)
    body = lesson('<ul><li><b>Translation</b> (<i>x</i>, <i>y</i>) → (<i>x</i> + <i>a</i>, <i>y</i> + <i>b</i>).</li><li><b>Reflection</b> over the <i>x</i>-axis: (<i>x</i>, −<i>y</i>); over the <i>y</i>-axis: (−<i>x</i>, <i>y</i>); over <i>y</i> = <i>x</i>: (<i>y</i>, <i>x</i>).</li><li><b>Rotation</b> 90° counterclockwise: (−<i>y</i>, <i>x</i>); 180°: (−<i>x</i>, −<i>y</i>).</li><li><b>Dilation</b> by <i>k</i> from center (<i>a</i>, <i>b</i>): move the center to the origin, multiply by <i>k</i>, move back.</li><li>Rigid transformations keep size and shape; dilations keep shape only.</li></ul>',
        [example("Rotate (3, −2) 90° counterclockwise", ["(<i>x</i>, <i>y</i>) → (−<i>y</i>, <i>x</i>)"], "(2, 3)")],
        [['Changing the wrong coordinate', 'Reflect over the <i>x</i>-axis: change <i>y</i>.'], ['Rotating the wrong way', 'Counterclockwise is the positive direction.'], ['Dilating from the origin', 'Use the given center.']])
    faq = [('What does TEKS G.3A ask?', 'Describe and perform transformations of figures in a plane using coordinate notation.'), ('What does TEKS G.3B ask?', 'Determine the image or pre-image of a given two-dimensional figure under a composition of rigid transformations, a composition of non-rigid transformations, and a composition of both, including dilations where the center can be any point in the plane.'), ('What does TEKS G.3C ask?', 'Identify the sequence of transformations that will carry a given pre-image onto an image on and off the coordinate plane.'), ('Which transformations are rigid?', 'Translations, reflections and rotations.')]
    make('transformations', 7, 'Coordinate and Transformational Geometry', 'G.3A, G.3B, G.3C',
         'G.3A describe and perform transformations of figures in a plane using coordinate notation; G.3B determine the image or pre-image of a given two-dimensional figure under a composition of rigid transformations, a composition of non-rigid transformations, and a composition of both, including dilations where the center can be any point in the plane; G.3C identify the sequence of transformations that will carry a given pre-image onto an image on and off the coordinate plane',
         'Transformations: Translations, Reflections, Rotations and Dilations', 'Transformations',
         'Free Geometry transformation worksheets for Texas TEKS G.3A–G.3C: translations, reflections, rotations, compositions and dilations with any center. 100 questions with answers.',
         'Rigid transformations keep size and shape.', '90° counterclockwise: (x, y) → (−y, x).',
         body, faq, sets, seo_title='Geometry Transformations Worksheets (TEKS G.3A, G.3B)')


if __name__ == "__main__":
    build()
