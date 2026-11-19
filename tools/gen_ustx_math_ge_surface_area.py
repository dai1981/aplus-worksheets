# -*- coding: utf-8 -*-
"""
Texas Geometry: Surface Area of Prisms, Pyramids, Cylinders, Cones and Spheres (TEKS G.11C)
  python3 tools/gen_ustx_math_ge_surface_area.py
Surface area of rectangular prisms (US Grade 7 maker), triangular prisms and cylinders (Texas Grade 8 makers), and
pyramids, cones, spheres and hemispheres (own makers), with a new seed.
Wrong answers come from real mistakes: leaving out a face, using the height instead of the slant height, and using
2πr² for a sphere.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_ustx_math_g8_surface_area as sa8
import random
import gen_us_math_g7_area_surface_area_volume as asv
adopt(asv)
asv.R = random.Random(696220)
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



def one_pyr(r):
    if r.random() < 0.5:
        b, l = r.randint(3, 15), r.randint(4, 20)
        lat, tot = 2 * b * l, b * b + 2 * b * l
        if r.random() < 0.4:
            return mcq("A square pyramid has base edge %d in. and slant height %d in. What is its lateral area?" % (b, l), "%s in²" % comma(lat), ["%s in²" % comma(tot), "%s in²" % comma(4 * b * l), "%s in²" % comma(b * l)],
                       "Four triangles: 4 × ½ × %d × %d = <b>%s in²</b>." % (b, l, comma(lat)))
        return mcq("A square pyramid has base edge %d in. and slant height %d in. What is its total surface area?" % (b, l), "%s in²" % comma(tot), ["%s in²" % comma(lat), "%s in²" % comma(b * b + 4 * b * l), "%s in²" % comma(b * b * l)],
                   "Base %d + four triangles 4 × ½ × %d × %d = %s: <b>%s in²</b>." % (b * b, b, l, comma(lat), comma(tot)))
    rad, l = r.randint(2, 12), r.randint(3, 20)
    if l <= rad:
        raise AssertionError
    lat, tot = rad * l, rad * rad + rad * l
    if r.random() < 0.4:
        return mcq("A cone has radius %d cm and slant height %d cm. What is its lateral area in terms of π?" % (rad, l), "%sπ cm²" % comma(lat), ["%sπ cm²" % comma(tot), "%sπ cm²" % comma(2 * rad * l), "%sπ cm²" % comma(rad * rad * l)],
                   "Lateral area = π<i>rl</i> = π × %d × %d = <b>%sπ cm²</b>." % (rad, l, comma(lat)))
    return mcq("A cone has radius %d cm and slant height %d cm. What is its total surface area in terms of π?" % (rad, l), "%sπ cm²" % comma(tot), ["%sπ cm²" % comma(lat), "%sπ cm²" % comma(2 * rad * rad + rad * l), "%sπ cm²" % comma(rad * l + 2 * rad)],
               "π<i>r</i><sup>2</sup> + π<i>rl</i> = %dπ + %dπ = <b>%sπ cm²</b>." % (rad * rad, lat, comma(tot)))


def one_cone_h(r):
    a, b, c = r.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17), (12, 16, 20)])
    rad, h, l = (a, b, c) if r.random() < 0.5 else (b, a, c)
    tot = rad * rad + rad * l
    return mcq("A cone has radius %d m and height %d m. What is its total surface area in terms of π?" % (rad, h), "%sπ m²" % comma(tot), ["%sπ m²" % comma(rad * rad + rad * h), "%sπ m²" % comma(rad * l), "%sπ m²" % comma(rad * rad + 2 * rad * l)],
               "Slant height = √(%d² + %d²) = %d. π<i>r</i><sup>2</sup> + π<i>rl</i> = %dπ + %dπ = <b>%sπ m²</b>." % (rad, h, l, rad * rad, rad * l, comma(tot)))


def one_sph(r):
    rad = r.randint(2, 15)
    kind = r.randrange(3)
    if kind == 0:
        return mcq("A sphere has radius %d ft. What is its surface area in terms of π?" % rad, "%sπ ft²" % comma(4 * rad * rad), ["%sπ ft²" % comma(2 * rad * rad), "%sπ ft²" % comma(rad * rad), "%sπ ft²" % comma(4 * rad)],
                   "4π<i>r</i><sup>2</sup> = 4π × %d = <b>%sπ ft²</b>." % (rad * rad, comma(4 * rad * rad)))
    if kind == 1:
        d = 2 * rad
        return mcq("A ball has a diameter of %d cm. What is its surface area in terms of π?" % d, "%sπ cm²" % comma(4 * rad * rad), ["%sπ cm²" % comma(4 * d * d), "%sπ cm²" % comma(2 * rad * rad), "%sπ cm²" % comma(d * d)],
                   "<i>r</i> = %d. 4π<i>r</i><sup>2</sup> = <b>%sπ cm²</b>." % (rad, comma(4 * rad * rad)))
    return mcq("A solid hemisphere has radius %d in. What is its total surface area (curved part and flat base) in terms of π?" % rad, "%sπ in²" % comma(3 * rad * rad), ["%sπ in²" % comma(2 * rad * rad), "%sπ in²" % comma(4 * rad * rad), "%sπ in²" % comma(rad * rad)],
               "Curved part 2π<i>r</i><sup>2</sup> + base π<i>r</i><sup>2</sup> = 3π<i>r</i><sup>2</sup> = <b>%sπ in²</b>." % comma(3 * rad * rad))


def build():
    sets, R = build_sets([
        ("Rectangular prisms", [("run", asv.set_surface, (), 20)]),
        ("Triangular prisms", [("collect", W(sa8.one_tri), 20)]),
        ("Cylinders: lateral and total", [("collect", W(sa8.one_cyl), 20)]),
        ("Pyramids and cones", [("collect", uniq(one_pyr), 14), ("collect", uniq(one_cone_h), 6)]),
        ("Spheres, hemispheres and problems", [("collect", uniq(one_sph), 14), ("collect", W(sa8.one_story), 6)]),
    ], 69622)
    finish(sets, R)
    body = lesson('<ul><li><b>Lateral area</b> leaves out the bases; <b>total surface area</b> includes them.</li><li>Prism: <i>L</i> = <i>Ph</i>, <i>S</i> = <i>Ph</i> + 2<i>B</i>. Cylinder: <i>L</i> = 2π<i>rh</i>, <i>S</i> = 2π<i>rh</i> + 2π<i>r</i><sup>2</sup>.</li><li>Pyramid: <i>L</i> = ½<i>Pl</i>. Cone: <i>L</i> = π<i>rl</i>, <i>S</i> = π<i>rl</i> + π<i>r</i><sup>2</sup>, with slant height <i>l</i>.</li><li>Sphere: <i>S</i> = 4π<i>r</i><sup>2</sup>.</li></ul>',
        [example("Cone: radius 5, slant height 13", ["25π + 65π"], "90π")],
        [['Leaving out a face', 'Count every face.'], ['Using the height instead of the slant height', 'Lateral area uses the slant height.'], ['Using 2π<i>r</i><sup>2</sup> for a sphere', 'A sphere is 4π<i>r</i><sup>2</sup>.']])
    faq = [('What does TEKS G.11C ask?', 'Apply the formulas for the total and lateral surface area of three-dimensional figures, including prisms, pyramids, cones, cylinders, spheres, and composite figures, to solve problems using appropriate units of measure.'), ('What is slant height?', 'The height of a face of a pyramid or the side of a cone, measured along the surface.'), ('What units does surface area use?', 'Square units.'), ('How do I find a slant height?', 'Use the Pythagorean Theorem with the height and the radius.')]
    make('surface-area', 22, 'Two-Dimensional and Three-Dimensional Figures', 'G.11C',
         'G.11C apply the formulas for the total and lateral surface area of three-dimensional figures, including prisms, pyramids, cones, cylinders, spheres, and composite figures, to solve problems using appropriate units of measure',
         'Surface Area of Prisms, Pyramids, Cylinders, Cones and Spheres', 'Surface Area',
         'Free Geometry surface area worksheets for Texas TEKS G.11C: lateral and total surface area of prisms, pyramids, cylinders, cones and spheres. 100 questions with answers.',
         'Lateral area leaves out the bases.', 'Sphere: 4πr². Cone: πrl + πr².',
         body, faq, sets, seo_title='Geometry Surface Area Worksheets (TEKS G.11C)')


if __name__ == "__main__":
    build()
