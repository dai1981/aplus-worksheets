# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Volume of Square and Rectangular Pyramids (Grade 7: Measurement and Geometry)
  python3 tools/gen_ph_math_g7_pyramids.py
A pyramid as one third of a prism with the same base and height (Texas Grade 7 maker), volumes of square and
rectangular pyramids, missing heights, estimating (own makers), and problems (Texas Grade 7 maker).
Wrong answers come from real mistakes: forgetting the one third, using the slant height, and multiplying only two
dimensions.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_ustx_math_g7_volume as txv
adopt(txv)
if hasattr(txv, 'R'): txv.R = random.Random(707170)
ph_common.GRADE = "grade-7"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


def one_sqpyr(r):
    kind = r.choice(["sq", "rect", "h"])
    if kind == "sq":
        s, h = r.choice([3, 4, 5, 6, 8, 9, 10, 12]), r.choice([3, 6, 9, 12, 15])
        V = s * s * h // 3
        if s * s * h % 3:
            raise AssertionError
        return mcq("A square pyramid has a base %d cm by %d cm and a height of %d cm. What is its volume?" % (s, s, h), "%s cm³" % comma(V), ["%s cm³" % comma(x) for x in (s * s * h, s * h, V * 2)],
                   "V = <span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span> × base area × height = <span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span> × %d × %d × %d = <b>%s cm³</b>." % (s, s, h, comma(V)))
    if kind == "rect":
        l, w, h = r.choice([4, 6, 8, 10, 12]), r.choice([3, 5, 6, 9]), r.choice([5, 6, 7, 9, 10])
        if l * w * h % 3 or l == w:
            raise AssertionError
        V = l * w * h // 3
        return mcq("A rectangular pyramid has a base %d m by %d m and a height of %d m. What is its volume?" % (l, w, h), "%s m³" % comma(V), ["%s m³" % comma(x) for x in (l * w * h, (l + w) * h, V + l * w)],
                   "V = <span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span> × %d × %d × %d = <b>%s m³</b>." % (l, w, h, comma(V)))
    s = r.choice([3, 6, 9, 12])
    h = r.choice([4, 5, 7, 8, 10])
    V = s * s * h // 3
    return mcq("A square pyramid has a volume of %s cm³ and a base %d cm by %d cm. What is its height?" % (comma(V), s, s), "%d cm" % h, ["%d cm" % x for x in (V // (s * s) if V // (s * s) != h else h + 1, 3 * h, h + 3)],
               "V = <span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span> × %d × h, so %s = %d × h ÷ 3 and h = 3 × %s ÷ %d = <b>%d cm</b>." % (s * s, comma(V), s * s, comma(V), s * s, h))


def one_est(r):
    s = r.choice([2.9, 3.1, 4.8, 5.2, 6.1, 7.9, 9.8, 10.2])
    h = r.choice([5.9, 6.2, 8.8, 9.1, 11.8, 12.1])
    rs, rh = round(s), round(h)
    est = rs * rs * rh / 3
    if abs(est - round(est)) > 1e-9:
        raise AssertionError
    est = int(round(est))
    q = "Estimate the volume of a square pyramid with base edges %s m and height %s m by rounding to whole numbers." % (s, h)
    return mcq(q, "about %s m³" % comma(est), ["about %s m³" % comma(x) for x in (rs * rs * rh, est * 2, rs * rh)],
               "Round: %s ≈ %d and %s ≈ %d. <span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span> × %d × %d × %d = <b>%s m³</b>." % (s, rs, h, rh, rs, rs, rh, comma(est)))


def build():
    sets, R = build_sets([
        ("Pyramids and prisms", [("collect", txv.one_rel, 14), ("collect", uniq(one_sqpyr), 6)]),
        ("Volume of a pyramid", [("collect", txv.one_pyr, 20)]),
        ("Square and rectangular pyramids", [("collect", uniq(one_sqpyr), 20)]),
        ("Estimate volumes", [("collect", uniq(one_est), 20)]),
        ("Pyramid problems", [("collect", txv.one_story, 10), ("collect", uniq(one_sqpyr), 10)]),
    ], 70717)
    finish(sets, R)
    body = lesson("<ul><li>A pyramid fits into a prism with the same base and height 3 times. So <b>V = <span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span> × base area × height</b>.</li><li>Square pyramid: V = <span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span>s²h. Rectangular pyramid: V = <span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span>lwh.</li><li>The height is measured straight up from the base to the top, not along a slanted face.</li><li>To estimate, round the measures to easy numbers first.</li></ul>",
        [example("Base 6 cm × 6 cm, height 10 cm", ["<span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span> × 36 × 10"], "120 cm³")],
        [['Forgetting the one third', 'A pyramid is one third of the prism.'], ['Using the slant height', 'Use the vertical height.'], ['Two dimensions only', 'Volume needs length, width and height.']])
    faq = [('What does MATATAG Math 7 ask about pyramids?', 'Explore inductively the volume of square and rectangular pyramids using rectangular prisms, estimate their volumes, and solve problems involving them.'), ('Why one third?', 'Three equal pyramids fill the prism with the same base and height.'), ('What is the slant height?', 'The height of a triangular face, not used for volume.'), ('What unit is volume in?', 'Cubic units, like cm³ or m³.')]
    make('volume-of-pyramids', 17, 'Measurement and Geometry', 'Grade 7: Measurement and Geometry',
         'Explore inductively the volume of square and rectangular pyramids using rectangular prisms, leading to the identification of the formula; estimate volumes of square and rectangular pyramids; solve problems involving volumes of square or rectangular pyramids.',
         'Volume of Square and Rectangular Pyramids', 'Volume of Pyramids',
         'Free Grade 7 volume of pyramids worksheets for the DepEd MATATAG curriculum: square and rectangular pyramids, the one-third rule, missing heights, estimates and problems. 100 questions with answers.',
         'V = ⅓ × base area × height.', 'A pyramid is one third of the prism with the same base and height.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
