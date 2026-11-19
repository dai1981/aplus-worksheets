# -*- coding: utf-8 -*-
"""
Texas Geometry: Midsegments, Perpendicular Bisectors and Medians (TEKS G.6D, G.6A, G.5C)
  python3 tools/gen_ustx_math_ge_midsegments.py
The Triangle Midsegment Theorem, perpendicular and angle bisectors, centroids and medians, and naming the center
(the US Geometry makers with a new seed and Texas names).
Wrong answers come from real mistakes: doubling instead of halving, using the 2 : 1 ratio the wrong way, and mixing
up the circumcenter and incenter.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_ge_midsegments_and_triangle_centers as mc
adopt(mc)
mc.R = random.Random(696120)
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
        ("Triangle Midsegment Theorem", [("collect", W(mc.one_mid), 20)]),
        ("Perpendicular and angle bisectors", [("collect", W(mc.one_bis), 20)]),
        ("Centroid and medians", [("collect", W(mc.one_cent), 20)]),
        ("Name the center", [("collect", W(mc.one_which), 20)]),
        ("Mixed practice", [("collect", W(mc.one_mid), 7), ("collect", W(mc.one_bis), 6), ("collect", W(mc.one_cent), 7)]),
    ], 69612)
    finish(sets, R)
    body = lesson('<ul><li>A <b>midsegment</b> joins two midpoints. It is parallel to the third side and half as long.</li><li>Any point on the <b>perpendicular bisector</b> of a segment is the same distance from both endpoints.</li><li>A <b>median</b> goes from a vertex to the midpoint of the opposite side. The <b>centroid</b> splits each median 2 : 1 from the vertex.</li><li>Perpendicular bisectors meet at the circumcenter; angle bisectors at the incenter.</li></ul>',
        [example("The third side is 18", ["half of 18"], "midsegment 9")],
        [['Doubling instead of halving', 'The midsegment is half the third side.'], ['Using 2 : 1 the wrong way', 'The longer part is next to the vertex.'], ['Mixing up the centers', 'Angle bisectors meet at the incenter.']])
    faq = [('What does TEKS G.6D ask?', 'Verify theorems about the relationships in triangles, including proof of the Pythagorean Theorem, the sum of interior angles, base angles of isosceles triangles, midsegments, and medians, and apply these relationships to solve problems.'), ('What does TEKS G.5C ask?', 'Use the constructions of congruent segments, congruent angles, angle bisectors, and perpendicular bisectors to make conjectures about geometric relationships.'), ('Where is the centroid?', 'Two-thirds of the way along each median from the vertex.'), ('What is the circumcenter equidistant from?', 'The three vertices.')]
    make('midsegments-bisectors-and-medians', 12, 'Proof and Congruence', 'G.6D, G.6A, G.5C',
         'G.6D verify theorems about the relationships in triangles, including midsegments and medians, and apply these relationships to solve problems; G.6A prove equidistance between the endpoints of a segment and points on its perpendicular bisector and apply these relationships to solve problems; G.5C use the constructions of congruent segments, congruent angles, angle bisectors, and perpendicular bisectors to make conjectures about geometric relationships',
         'Midsegments, Perpendicular Bisectors and Medians', 'Midsegments, Bisectors and Medians',
         'Free Geometry worksheets for Texas TEKS G.6D, G.6A and G.5C: midsegments, perpendicular and angle bisectors, medians, the centroid and triangle centers. 100 questions with answers.',
         'Midsegment = half the third side; centroid splits medians 2 : 1.', 'Points on a perpendicular bisector are equidistant from the endpoints.',
         body, faq, sets, seo_title='Geometry Midsegments, Bisectors and Medians Worksheets (TEKS G.6D)')


if __name__ == "__main__":
    build()
