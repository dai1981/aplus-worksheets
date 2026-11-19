# -*- coding: utf-8 -*-
"""
Texas Geometry: Dilations and Similar Figures (TEKS G.7A)
  python3 tools/gen_ustx_math_ge_dilations.py
Dilations centered at the origin and at other points, scale factors, similar polygons, and word problems (the US
Geometry makers with a new seed and Texas names).
Wrong answers come from real mistakes: adding the scale factor, writing the ratio upside down, and thinking angles
change.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_ge_dilations_and_similarity as dl
adopt(dl)
dl.R = random.Random(696140)
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
        ("Dilations centered at the origin", [("collect", W(dl.one_org), 20)]),
        ("Dilations with another center", [("collect", W(dl.one_ctr), 20)]),
        ("Similar polygons", [("collect", W(dl.one_poly), 20)]),
        ("Scale factor and proportional sides", [("collect", W(dl.one_scale), 20)]),
        ("Word problems", [("collect", W(dl.one_word), 20)]),
    ], 69614)
    finish(sets, R)
    body = lesson('<ul><li>A <b>dilation</b> with scale factor <i>k</i> multiplies every distance from the center by <i>k</i>.</li><li><i>k</i> &gt; 1 enlarges; 0 &lt; <i>k</i> &lt; 1 reduces.</li><li>Figures are <b>similar</b> if a dilation (and rigid moves) maps one onto the other: angles are congruent and sides are proportional.</li></ul>',
        [example("Dilate (4, −6) by 1/2 from the origin", ["multiply both coordinates"], "(2, −3)")],
        [['Adding the scale factor', 'Multiply, do not add.'], ['Writing the ratio upside down', 'Image ÷ pre-image.'], ['Thinking angles change', 'Dilations keep angles.']])
    faq = [('What does TEKS G.7A ask?', 'Apply the definition of similarity in terms of a dilation to identify similar figures and their proportional sides and the congruent corresponding angles.'), ('Is a dilation rigid?', 'No. It changes size.'), ('What does k = 1 do?', 'Nothing changes.'), ('Are all squares similar?', 'Yes.')]
    make('dilations-and-similar-figures', 14, 'Similarity, Proof, and Trigonometry', 'G.7A',
         'G.7A apply the definition of similarity in terms of a dilation to identify similar figures and their proportional sides and the congruent corresponding angles',
         'Dilations and Similar Figures', 'Dilations and Similarity',
         'Free Geometry worksheets for Texas TEKS G.7A: dilations from the origin and other centers, scale factors and similar polygons. 100 questions with answers.',
         'Dilations multiply distances by k and keep angles.', '(4, −6) dilated by 1/2 is (2, −3).',
         body, faq, sets, seo_title='Geometry Dilations and Similar Figures Worksheets (TEKS G.7A)')


if __name__ == "__main__":
    build()
