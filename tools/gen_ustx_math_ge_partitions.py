# -*- coding: utf-8 -*-
"""
Texas Geometry: Segments, Midpoints and Partitioning a Segment (TEKS G.2A)
  python3 tools/gen_ustx_math_ge_partitions.py
Segment addition, segment addition with algebra (US Geometry makers), the midpoint formula (US Geometry maker), and
a point a fraction of the way along a segment on a number line and on the coordinate plane (own makers).
Wrong answers come from real mistakes: measuring from the wrong endpoint, using a:b as the fraction a/b, and adding
the fraction of the length to the wrong coordinate.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_ge_segment_addition_and_midpoints as sa
adopt(sa)
sa.R = random.Random(696030)
import gen_us_math_ge_distance_and_midpoint_formulas as dm
adopt(dm)
dm.R = random.Random(696031)
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


def pt(x, y):
    return "(%s, %s)" % (sg(x), sg(y))


FRS = [Fr(1, 3), Fr(2, 3), Fr(1, 4), Fr(3, 4), Fr(2, 5), Fr(3, 5), Fr(1, 5), Fr(4, 5)]


def one_line(r):
    f = r.choice(FRS + [None, None])
    a = r.randint(-12, 6)
    if f is None:
        m, n = r.choice([(1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2)])
        f = Fr(m, m + n)
        say = "partitions <span class='ov'>AB</span> in the ratio %d : %d" % (m, n)
        wf = Fr(m, n) if m < n else Fr(n, m + n)
    else:
        say = "is %s of the way from A to B" % fr(f.numerator, f.denominator)
        wf = 1 - f
    L = f.denominator * r.randint(2, 6)
    b = a + L
    p = a + f * L
    if p.denominator != 1:
        raise AssertionError
    wrong = [a + wf * L, b - f * L if b - f * L != p else a + (f / 2) * L, Fr(a + b, 2), f * L]
    w = [sg(int(v)) for v in wrong if v.denominator == 1 and v != p]
    return mcq("On a number line, A = %s and B = %s. Point P %s. Where is P?" % (sg(a), sg(b), say), sg(int(p)), w,
               "AB = %d. P is %s of the way: %s + %s × %d = <b>%s</b>." % (L, fr(f.numerator, f.denominator), sg(a), fr(f.numerator, f.denominator), L, sg(int(p))))


def one_plane(r):
    f = r.choice(FRS + [None])
    if f is None:
        m, n = r.choice([(1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2)])
        f = Fr(m, m + n)
        say = "partitions the segment from A to B in the ratio %d : %d" % (m, n)
        wf = Fr(m, n) if Fr(m, n) < 1 else 1 - f
    else:
        say = "is %s of the way from A to B" % fr(f.numerator, f.denominator)
        wf = 1 - f
    d = f.denominator
    ax, ay = r.randint(-8, 6), r.randint(-8, 6)
    dx, dy = d * r.randint(-3, 3), d * r.randint(-3, 3)
    if dx == 0 and dy == 0:
        raise AssertionError
    bx, by = ax + dx, ay + dy
    px, py = ax + f * dx, ay + f * dy
    qx, qy = ax + wf * dx, ay + wf * dy
    cands = [(qx, qy), (bx - f * dx, by - f * dy), (Fr(ax + bx, 2), Fr(ay + by, 2)), (f * dx, f * dy)]
    w = [pt(int(x), int(y)) for x, y in cands if x.denominator == 1 and y.denominator == 1 and (x, y) != (px, py)] if True else []
    return mcq("A = %s and B = %s. Point P %s. What are the coordinates of P?" % (pt(ax, ay), pt(bx, by), say), pt(int(px), int(py)), w,
               "P = A + %s(B − A) = %s + %s(%s, %s) = <b>%s</b>." % (fr(f.numerator, f.denominator), pt(ax, ay), fr(f.numerator, f.denominator), sg(dx), sg(dy), pt(int(px), int(py))))


def build():
    sets, R = build_sets([
        ("Segment Addition Postulate", [("collect", W(sa.one_add), 20)]),
        ("Segment addition with algebra", [("collect", W(sa.one_alg), 20)]),
        ("The midpoint formula", [("collect", W(dm.one_mid), 20)]),
        ("A fraction of the way on a number line", [("collect", uniq(one_line), 20)]),
        ("A fraction of the way on the coordinate plane", [("collect", uniq(one_plane), 20)]),
    ], 69603)
    finish(sets, R)
    body = lesson('<ul><li><b>Segment addition</b>: if B is between A and C, then AB + BC = AC.</li><li><b>Midpoint</b>: ((<i>x</i><sub>1</sub> + <i>x</i><sub>2</sub>) ÷ 2, (<i>y</i><sub>1</sub> + <i>y</i><sub>2</sub>) ÷ 2).</li><li>A point <i>k</i> of the way from A to B is A + <i>k</i>(B − A). Do it for <i>x</i> and for <i>y</i>.</li><li>A ratio <i>m</i> : <i>n</i> means the fraction <i>m</i> ÷ (<i>m</i> + <i>n</i>) of the way.</li></ul>',
        [example("A(−2, 1), B(10, 7); P is 1/3 of the way from A to B", ["B − A = (12, 6)", "1/3 of it = (4, 2)"], "P(2, 3)")],
        [['Measuring from the wrong endpoint', 'Start at A when it says “from A”.'], ['Using <i>m</i> : <i>n</i> as <i>m</i>/<i>n</i>', '1 : 2 means 1/3 of the way.'], ['Adding the fraction of the length to the wrong coordinate', 'Work with <i>x</i> and <i>y</i> separately.']])
    faq = [('What does TEKS G.2A ask?', 'Determine the coordinates of a point that is a given fractional distance less than one from one end of a line segment to the other in one- and two-dimensional coordinate systems, including finding the midpoint.'), ('Is the midpoint 1/2 of the way?', 'Yes.'), ('What does a 2 : 3 ratio mean?', 'The point is 2/5 of the way from the first endpoint.'), ('Can the answer have fractions?', 'Yes, but these worksheets use whole numbers.')]
    make('segments-midpoints-and-partitions', 3, 'Coordinate and Transformational Geometry', 'G.2A',
         'G.2A determine the coordinates of a point that is a given fractional distance less than one from one end of a line segment to the other in one- and two-dimensional coordinate systems, including finding the midpoint',
         'Segments, Midpoints and Partitioning a Segment', 'Segments, Midpoints and Partitions',
         'Free Geometry worksheets for Texas TEKS G.2A: segment addition, midpoints, and finding a point a fraction of the way along a segment on a number line and the coordinate plane. 100 questions with answers.',
         'P = A + k(B − A).', 'A ratio 1 : 2 means 1/3 of the way.',
         body, faq, sets, seo_title='Geometry Segments, Midpoints and Partitions Worksheets (TEKS G.2A)')


if __name__ == "__main__":
    build()
