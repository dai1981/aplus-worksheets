# -*- coding: utf-8 -*-
"""
Texas Geometry: Right Triangle Similarity and the Geometric Mean (TEKS G.8B)
  python3 tools/gen_ustx_math_ge_geometric_mean.py
The geometric mean of two numbers, the altitude to the hypotenuse, the leg rule, a missing segment (own makers), and
geometric mean problems (US Geometry maker with a new seed).
Wrong answers come from real mistakes: averaging instead of taking the square root of the product, multiplying the
wrong segments for a leg, and forgetting the square root.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_ge_similar_triangles as st
adopt(st)
st.R = random.Random(696160)
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


import math


def sqp(r):
    k = r.choice([1, 1, 2, 3, 5])
    m, n = r.sample(range(1, 7), 2)
    return k * m * m, k * n * n, k * m * n


def one_gm(r):
    a, b, g = sqp(r)
    w = [str((a + b) // 2) if (a + b) % 2 == 0 else str(a + b), str(a * b), str(g + 1), str(abs(a - b))]
    w = [x for x in w if x != str(g) and x != "0"]
    return mcq("What is the geometric mean of %d and %d?" % (a, b), str(g), w, "√(%d × %d) = √%d = <b>%d</b>." % (a, b, a * b, g))


def one_alt(r):
    p, q, h = sqp(r)
    w = [str((p + q) // 2) if (p + q) % 2 == 0 else str(p + q), str(p * q), str(int(math.isqrt(p * p + q * q))) if math.isqrt(p * p + q * q) ** 2 == p * p + q * q else str(h + 2), str(h * 2)]
    w = [x for x in w if x != str(h)]
    return mcq("The altitude to the hypotenuse of a right triangle divides the hypotenuse into segments of %d and %d. How long is the altitude?" % (p, q), str(h), w,
               "The altitude is the geometric mean of the segments: √(%d × %d) = √%d = <b>%d</b>." % (p, q, p * q, h))


def one_leg(r):
    k = r.choice([1, 2, 3])
    m, n = sorted(r.sample(range(1, 8), 2))
    p, c = k * m * m, k * n * n
    leg = k * m * n
    q = c - p
    if q <= 0:
        raise AssertionError
    w = [str(int(math.isqrt(p * q))) if math.isqrt(p * q) ** 2 == p * q else str(leg + 1), str(p * c), str((p + c) // 2) if (p + c) % 2 == 0 else str(leg * 2), str(c - leg) if c - leg > 0 else str(leg + 3)]
    w = [x for x in w if x != str(leg)]
    return mcq("In a right triangle, the altitude to the hypotenuse splits the hypotenuse (length %d) into segments %d and %d. How long is the leg next to the segment of length %d?" % (c, p, q, p), str(leg), w,
               "Leg = √(hypotenuse × adjacent segment) = √(%d × %d) = √%d = <b>%d</b>." % (c, p, c * p, leg))


def one_seg(r):
    h = r.randint(2, 12)
    p = r.choice([d for d in range(1, h * h) if (h * h) % d == 0 and d < h])
    q = h * h // p
    w = [str(h * h - p), str(h - p) if h - p > 0 else str(q + 1), str(q * 2), str(p * h)]
    w = [x for x in w if x != str(q)]
    return mcq("The altitude to the hypotenuse of a right triangle is %d. One segment of the hypotenuse is %d. How long is the other segment?" % (h, p), str(q), w,
               "<i>h</i><sup>2</sup> = <i>p</i> × <i>q</i>: %d = %d × <i>q</i>, so <i>q</i> = <b>%d</b>." % (h * h, p, q))


def build():
    sets, R = build_sets([
        ("Geometric mean of two numbers", [("collect", uniq(one_gm), 20)]),
        ("The altitude to the hypotenuse", [("collect", uniq(one_alt), 20)]),
        ("A missing segment of the hypotenuse", [("collect", uniq(one_seg), 20)]),
        ("The leg rule", [("collect", uniq(one_leg), 20)]),
        ("Geometric mean problems", [("collect", W(st.one_gm), 20)]),
    ], 69616)
    finish(sets, R)
    body = lesson('<ul><li>The <b>geometric mean</b> of <i>a</i> and <i>b</i> is √(<i>ab</i>).</li><li>The altitude to the hypotenuse makes three similar right triangles.</li><li><b>Altitude rule</b>: the altitude is the geometric mean of the two hypotenuse segments.</li><li><b>Leg rule</b>: each leg is the geometric mean of the whole hypotenuse and the segment next to that leg.</li></ul>',
        [example("Segments 4 and 9", ["√(4 × 9) = √36"], "altitude 6")],
        [['Averaging instead', 'Multiply, then take the square root.'], ['Using the wrong segment for a leg', 'Use the segment next to the leg.'], ['Forgetting the square root', '√36 = 6, not 36.']])
    faq = [('What does TEKS G.8B ask?', 'Identify and apply the relationships that exist when an altitude is drawn to the hypotenuse of a right triangle, including the geometric mean, to solve problems.'), ('Why are the three triangles similar?', 'Each shares an angle with the big triangle and has a right angle (AA).'), ('What is the geometric mean of 2 and 8?', '4.'), ('Is the geometric mean always smaller than the average?', 'It is never larger.')]
    make('right-triangle-similarity-and-geometric-mean', 16, 'Similarity, Proof, and Trigonometry', 'G.8B',
         'G.8B identify and apply the relationships that exist when an altitude is drawn to the hypotenuse of a right triangle, including the geometric mean, to solve problems',
         'Right Triangle Similarity and the Geometric Mean', 'Geometric Mean in Right Triangles',
         'Free Geometry worksheets for Texas TEKS G.8B: the geometric mean, the altitude to the hypotenuse, the leg rule and similar right triangles. 100 questions with answers.',
         'Altitude = √(segment × segment).', 'Leg = √(hypotenuse × adjacent segment).',
         body, faq, sets, seo_title='Geometry Right Triangle Similarity and Geometric Mean Worksheets (TEKS G.8B)')


if __name__ == "__main__":
    build()
