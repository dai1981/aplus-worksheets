# -*- coding: utf-8 -*-
"""
Texas Geometry: Circle Theorems: Angles, Chords, Tangents and Secants (TEKS G.12A)
  python3 tools/gen_ustx_math_ge_circle_theorems.py
Central angles and arcs, inscribed angles, inscribed quadrilaterals, tangent lines, and chords and secants (the US
Geometry makers with a new seed and Texas names).
Wrong answers come from real mistakes: using the whole arc for an inscribed angle, adding opposite angles of an
inscribed quadrilateral to 360°, and forgetting that a tangent meets the radius at 90°.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_ge_circle_angles_and_arcs as ca
adopt(ca)
ca.R = random.Random(696240)
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
        ("Central angles and arcs", [("collect", W(ca.one_central), 20)]),
        ("Inscribed angles", [("collect", W(ca.one_insc), 20)]),
        ("Inscribed quadrilaterals", [("collect", W(ca.one_quad), 20)]),
        ("Tangent lines", [("collect", W(ca.one_tan), 20)]),
        ("Chords, secants and reasoning", [("collect", W(ca.one_sec), 20)]),
    ], 69624)
    finish(sets, R)
    body = lesson('<ul><li>A <b>central angle</b> equals its arc. An <b>inscribed angle</b> is half its arc.</li><li>Opposite angles of an inscribed quadrilateral add to 180°.</li><li>A <b>tangent</b> is perpendicular to the radius at the point of tangency. Two tangents from one point are congruent.</li><li>Angles formed by chords and secants use half the sum or half the difference of the arcs.</li></ul>',
        [example("Inscribed angle on a 124° arc", ["half of 124"], "62°")],
        [['Using the whole arc for an inscribed angle', 'Take half.'], ['Opposite angles adding to 360°', 'They add to 180°.'], ['Forgetting the right angle', 'Radius ⊥ tangent.']])
    faq = [('What does TEKS G.12A ask?', 'Apply theorems about circles, including relationships among angles, radii, chords, tangents, and secants, to solve non-contextual problems.'), ('What is an angle inscribed in a semicircle?', '90°.'), ('Are two tangents from a point equal?', 'Yes.'), ('What is a secant?', 'A line that crosses a circle at two points.')]
    make('circle-angles-chords-tangents-and-secants', 24, 'Circles', 'G.12A',
         'G.12A apply theorems about circles, including relationships among angles, radii, chords, tangents, and secants, to solve non-contextual problems',
         'Circle Theorems: Angles, Chords, Tangents and Secants', 'Circle Theorems',
         'Free Geometry circle worksheets for Texas TEKS G.12A: central and inscribed angles, inscribed quadrilaterals, tangents, chords and secants. 100 questions with answers.',
         'Inscribed angle = half the arc.', 'A tangent is perpendicular to the radius.',
         body, faq, sets, seo_title='Geometry Circle Theorems Worksheets (TEKS G.12A)')


if __name__ == "__main__":
    build()
