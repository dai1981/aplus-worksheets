# -*- coding: utf-8 -*-
"""
Texas Geometry: Volume of Prisms, Pyramids, Cylinders, Cones and Spheres (TEKS G.11D)
  python3 tools/gen_ustx_math_ge_volume.py
Volume of cylinders, cones, spheres and hemispheres, answers in terms of π, and pyramids, composite solids and
density (the US Geometry makers with a new seed and Texas names).
Wrong answers come from real mistakes: forgetting the 1/3 for cones and pyramids, using the diameter as the radius,
and cubing the wrong number.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_ge_volume_of_solids as vs
adopt(vs)
vs.R = random.Random(696230)
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
        ("Volume of a cylinder", [("collect", W(vs.one_cyl), 20)]),
        ("Volume of a cone", [("collect", W(vs.one_cone), 20)]),
        ("Volume of spheres and hemispheres", [("collect", W(vs.one_sph), 20)]),
        ("Answers in terms of π", [("collect", W(vs.one_pi), 20)]),
        ("Pyramids, composite solids and density", [("collect", W(vs.one_prob), 20)]),
    ], 69623)
    finish(sets, R)
    body = lesson("<ul><li>Prism and cylinder: <i>V</i> = <i>Bh</i> (cylinder: π<i>r</i><sup>2</sup><i>h</i>).</li><li>Pyramid and cone: <i>V</i> = ⅓<i>Bh</i> (cone: ⅓π<i>r</i><sup>2</sup><i>h</i>).</li><li>Sphere: <i>V</i> = <span class='fr'><span class='fn'>4</span><span class='fd'>3</span></span>π<i>r</i><sup>3</sup>. Hemisphere: half of that.</li><li>Composite solids: add or subtract the parts.</li></ul>",
        [example("Cone: radius 3, height 10", ["⅓ × π × 9 × 10"], "30π")],
        [['Forgetting ⅓', 'Cones and pyramids are a third of a prism.'], ['Using the diameter as the radius', 'Halve the diameter.'], ['Cubing the wrong number', 'Only <i>r</i> is cubed for a sphere.']])
    faq = [('What does TEKS G.11D ask?', 'Apply the formulas for the volume of three-dimensional figures, including prisms, pyramids, cones, cylinders, spheres, and composite figures, to solve problems using appropriate units of measure.'), ('What units does volume use?', 'Cubic units.'), ('How are cone and cylinder volumes related?', 'A cone is one third of the cylinder with the same base and height.'), ('What is density?', 'Mass ÷ volume.')]
    make('volume', 23, 'Two-Dimensional and Three-Dimensional Figures', 'G.11D',
         'G.11D apply the formulas for the volume of three-dimensional figures, including prisms, pyramids, cones, cylinders, spheres, and composite figures, to solve problems using appropriate units of measure',
         'Volume of Prisms, Pyramids, Cylinders, Cones and Spheres', 'Volume',
         'Free Geometry volume worksheets for Texas TEKS G.11D: volume of prisms, pyramids, cylinders, cones, spheres and composite solids. 100 questions with answers.',
         'Prism Bh; pyramid ⅓Bh; sphere 4/3 πr³.', 'Cone r = 3, h = 10: 30π.',
         body, faq, sets, seo_title='Geometry Volume Worksheets (TEKS G.11D)')


if __name__ == "__main__":
    build()
