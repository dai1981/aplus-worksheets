# -*- coding: utf-8 -*-
"""
Texas Geometry: Similar Triangles and the Triangle Proportionality Theorem (TEKS G.7B, G.8A)
  python3 tools/gen_ustx_math_ge_similar_triangles.py
Are the triangles similar, nested similar triangles, the Triangle Proportionality Theorem, and indirect measurement
(the US Geometry makers with a new seed and Texas names).
Wrong answers come from real mistakes: matching sides that do not correspond, using a part instead of the whole side
in nested triangles, and setting up the proportion upside down.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_ge_similar_triangles as st
adopt(st)
st.R = random.Random(696150)
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
        ("Are the triangles similar?", [("collect", W(st.one_crit), 20)]),
        ("Nested similar triangles", [("collect", W(st.one_nest), 20)]),
        ("Triangle Proportionality Theorem", [("collect", W(st.one_prop), 20)]),
        ("Mixed practice", [("collect", W(st.one_crit), 10), ("collect", W(st.one_prop), 10)]),
        ("Indirect measurement", [("collect", W(st.one_word), 20)]),
    ], 69615)
    finish(sets, R)
    body = lesson('<ul><li><b>AA</b>: two pairs of congruent angles make triangles similar.</li><li>Similar triangles have proportional corresponding sides.</li><li><b>Triangle Proportionality Theorem</b>: a line parallel to one side divides the other two sides proportionally.</li><li>Use shadows or mirrors to measure tall things.</li></ul>',
        [example("A 6 ft person casts a 4 ft shadow; a tree casts 18 ft", ["6/4 = <i>h</i>/18"], "27 ft")],
        [['Matching non-corresponding sides', 'Match by the angles.'], ['Using a part instead of the whole side', 'Nested triangles use whole sides.'], ['Upside-down proportions', 'Keep the same order in both ratios.']])
    faq = [('What does TEKS G.7B ask?', 'Apply the Angle-Angle criterion to verify similar triangles and apply the proportionality of the corresponding sides to solve problems.'), ('What does TEKS G.8A ask?', 'Prove theorems about similar triangles, including the Triangle Proportionality theorem, and apply these theorems to solve problems.'), ('Is AAA needed?', 'No. Two angles are enough.'), ('Are congruent triangles similar?', 'Yes, with scale factor 1.')]
    make('similar-triangles-and-proportionality', 15, 'Similarity, Proof, and Trigonometry', 'G.7B, G.8A',
         'G.7B apply the Angle-Angle criterion to verify similar triangles and apply the proportionality of the corresponding sides to solve problems; G.8A prove theorems about similar triangles, including the Triangle Proportionality theorem, and apply these theorems to solve problems',
         'Similar Triangles and the Triangle Proportionality Theorem', 'Similar Triangles',
         'Free Geometry worksheets for Texas TEKS G.7B and G.8A: AA similarity, nested triangles, the Triangle Proportionality Theorem and indirect measurement. 100 questions with answers.',
         'Two congruent angles make triangles similar.', '6/4 = h/18 gives h = 27.',
         body, faq, sets, seo_title='Geometry Similar Triangles and Proportionality Worksheets (TEKS G.7B, G.8A)')


if __name__ == "__main__":
    build()
