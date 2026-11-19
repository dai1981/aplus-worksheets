# -*- coding: utf-8 -*-
"""
Texas Geometry: Proving Triangles Congruent: SSS, SAS, ASA, AAS and HL (TEKS G.6B, G.6C)
  python3 tools/gen_ustx_math_ge_congruent_triangles.py
Which criterion proves congruence, corresponding parts, what else is needed, CPCTC with algebra, and shared sides
(the US Geometry makers with a new seed and Texas names).
Wrong answers come from real mistakes: using AAA or SSA, matching the parts in the wrong order, and forgetting a
shared side.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_ge_congruent_triangles as ct
adopt(ct)
ct.R = random.Random(696110)
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
        ("Which criterion proves congruence?", [("collect", W(ct.one_crit), 20)]),
        ("Corresponding parts", [("collect", W(ct.one_corr), 20)]),
        ("What else is needed?", [("collect", W(ct.one_need), 20)]),
        ("CPCTC with algebra", [("collect", W(ct.one_cpctc), 20)]),
        ("Shared sides and reasoning", [("collect", W(ct.one_reason), 20)]),
    ], 69611)
    finish(sets, R)
    body = lesson('<ul><li>Triangles are congruent when a rigid transformation maps one onto the other.</li><li>Criteria: <b>SSS</b>, <b>SAS</b>, <b>ASA</b>, <b>AAS</b>, and <b>HL</b> for right triangles.</li><li><b>AAA</b> and <b>SSA</b> do not prove congruence.</li><li>The order of letters matters: △ABC ≅ △DEF means A ↔ D, B ↔ E, C ↔ F.</li></ul>',
        [example("Two sides and the included angle are congruent", ["the angle is between the sides"], "SAS")],
        [['Using AAA or SSA', 'They are not criteria.'], ['Matching parts in the wrong order', 'Follow the letter order.'], ['Forgetting a shared side', 'A shared side is congruent to itself.']])
    faq = [('What does TEKS G.6B ask?', 'Prove two triangles are congruent by applying the Side-Angle-Side, Angle-Side-Angle, Side-Side-Side, Angle-Angle-Side, and Hypotenuse-Leg congruence conditions.'), ('What does TEKS G.6C ask?', 'Apply the definition of congruence, in terms of rigid transformations, to identify congruent figures and their corresponding sides and angles.'), ('What does CPCTC mean?', 'Corresponding parts of congruent triangles are congruent.'), ('When can HL be used?', 'Only for right triangles.')]
    make('proving-triangles-congruent', 11, 'Proof and Congruence', 'G.6B, G.6C',
         'G.6B prove two triangles are congruent by applying the Side-Angle-Side, Angle-Side-Angle, Side-Side-Side, Angle-Angle-Side, and Hypotenuse-Leg congruence conditions; G.6C apply the definition of congruence, in terms of rigid transformations, to identify congruent figures and their corresponding sides and angles',
         'Proving Triangles Congruent: SSS, SAS, ASA, AAS and HL', 'Congruent Triangles',
         'Free Geometry worksheets for Texas TEKS G.6B and G.6C: prove triangles congruent with SSS, SAS, ASA, AAS and HL, corresponding parts and CPCTC. 100 questions with answers.',
         'SSS, SAS, ASA, AAS, HL — never AAA or SSA.', '△ABC ≅ △DEF: A ↔ D, B ↔ E, C ↔ F.',
         body, faq, sets, seo_title='Geometry Proving Triangles Congruent Worksheets (TEKS G.6B)')


if __name__ == "__main__":
    build()
