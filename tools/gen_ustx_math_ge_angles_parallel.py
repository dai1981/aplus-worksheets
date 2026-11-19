# -*- coding: utf-8 -*-
"""
Texas Geometry: Vertical Angles and Angles Formed by Parallel Lines (TEKS G.6A, G.5A)
  python3 tools/gen_ustx_math_ge_angles_parallel.py
Vertical angles and linear pairs, complementary and supplementary angles (US Geometry makers), naming angle pairs,
finding angles, solving for x and proving lines parallel (US Geometry makers), all with a new seed and Texas names.
Wrong answers come from real mistakes: adding to 90° instead of 180°, calling same-side interior angles congruent,
and using the converse backwards.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_ge_angle_pairs as ap
adopt(ap)
ap.R = random.Random(696060)
import gen_us_math_ge_parallel_lines_and_transversals as pt
adopt(pt)
pt.R = random.Random(696061)
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
        ("Vertical angles and linear pairs", [("collect", W(ap.one_vert), 20)]),
        ("Name the angle pair", [("collect", W(pt.one_name), 20)]),
        ("Find angle measures", [("collect", W(pt.one_find), 20)]),
        ("Solve for x", [("collect", W(pt.one_alg), 20)]),
        ("Prove lines parallel and word problems", [("collect", W(pt.one_conv), 10), ("collect", W(pt.one_word), 10)]),
    ], 69606)
    finish(sets, R)
    body = lesson('<ul><li><b>Vertical angles</b> are congruent. A <b>linear pair</b> adds to 180°.</li><li>With parallel lines: corresponding, alternate interior and alternate exterior angles are <b>congruent</b>.</li><li>Same-side (consecutive) interior angles are <b>supplementary</b>.</li><li>If these angle facts are true, the lines are parallel (the converses).</li></ul>',
        [example("Alternate interior angles: (3<i>x</i> + 10)° and (5<i>x</i> − 30)°", ["3<i>x</i> + 10 = 5<i>x</i> − 30"], "<i>x</i> = 20")],
        [['Adding to 90° instead of 180°', 'A linear pair makes a straight line.'], ['Calling same-side interior angles congruent', 'They are supplementary.'], ['Using the converse backwards', 'Angle facts prove the lines parallel.']])
    faq = [('What does TEKS G.6A ask?', 'Verify theorems about angles formed by the intersection of lines and line segments, including vertical angles, and angles formed by parallel lines cut by a transversal and prove equidistance between the endpoints of a segment and points on its perpendicular bisector and apply these relationships to solve problems.'), ('What does TEKS G.5A ask?', 'Investigate patterns to make conjectures about geometric relationships, including angles formed by parallel lines cut by a transversal, criteria required for triangle congruence, special segments of triangles, diagonals of quadrilaterals, interior and exterior angles of polygons, and special segments and angles of circles choosing from a variety of tools.'), ('Are vertical angles always congruent?', 'Yes.'), ('What is a transversal?', 'A line that crosses two or more lines.')]
    make('angles-and-parallel-lines', 6, 'Proof and Congruence', 'G.6A, G.5A',
         'G.6A verify theorems about angles formed by the intersection of lines and line segments, including vertical angles, and angles formed by parallel lines cut by a transversal and prove equidistance between the endpoints of a segment and points on its perpendicular bisector and apply these relationships to solve problems; G.5A investigate patterns to make conjectures about geometric relationships, including angles formed by parallel lines cut by a transversal',
         'Vertical Angles and Angles Formed by Parallel Lines', 'Angles and Parallel Lines',
         'Free Geometry worksheets for Texas TEKS G.6A and G.5A: vertical angles, linear pairs, angles formed by parallel lines and a transversal, solving for x and proving lines parallel. 100 questions with answers.',
         'Parallel lines: congruent pairs, or supplementary same-side angles.', 'Vertical angles are congruent.',
         body, faq, sets, seo_title='Geometry Angles and Parallel Lines Worksheets (TEKS G.6A)')


if __name__ == "__main__":
    build()
