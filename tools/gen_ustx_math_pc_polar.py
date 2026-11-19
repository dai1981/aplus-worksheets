# -*- coding: utf-8 -*-
"""
Texas Precalculus: Polar Coordinates and Polar Graphs (TEKS P.3D, P.3E)
  python3 tools/gen_ustx_math_pc_polar.py
Converting points between polar and rectangular coordinates, naming the same point in different ways, converting
equations, and polar graphs such as circles, roses and limaçons (US Precalculus makers with a new seed).
Wrong answers come from real mistakes: swapping cos and sin, the wrong quadrant for θ, and doubling the petals of a
rose with an odd n.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_pc_polar_coordinates as po
adopt(po)
po.R = random.Random(698220)
tx_common.GRADE = "precalculus"

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


def ft(v):
    v = Fr(v)
    if v.denominator == 1:
        return sg(int(v))
    return (MINUS if v < 0 else "") + fr(abs(v.numerator), v.denominator)


def fx(body, name="f"):
    return "<i>%s</i>(<i>x</i>) = %s" % (name, body)



def build():
    sets, R = build_sets([
        ("Polar to rectangular", [("collect", W(po.one_p2r), 20)]),
        ("Rectangular to polar", [("collect", W(po.one_r2p), 20)]),
        ("Different names for the same point", [("collect", W(po.one_eq), 20)]),
        ("Convert equations", [("collect", W(po.one_conv), 20)]),
        ("Polar graphs", [("collect", W(po.one_graph), 20)]),
    ], 69822)
    finish(sets, R)
    body = lesson('<ul><li>A polar point (<i>r</i>, θ) is <i>r</i> units from the pole at angle θ.</li><li>Polar to rectangular: <i>x</i> = <i>r</i> cos θ, <i>y</i> = <i>r</i> sin θ.</li><li>Rectangular to polar: <i>r</i> = √(<i>x</i><sup>2</sup> + <i>y</i><sup>2</sup>), tan θ = <i>y</i> ÷ <i>x</i> (choose θ in the quadrant of the point).</li><li>Graphs: <i>r</i> = <i>a</i> is a circle; <i>r</i> = <i>a</i> cos <i>n</i>θ is a rose with <i>n</i> petals if <i>n</i> is odd and 2<i>n</i> if <i>n</i> is even.</li></ul>',
        [example("(4, <span class='fr'><span class='fn'>2π</span><span class='fd'>3</span></span>)", ["<i>x</i> = 4 cos(2π/3) = −2", "<i>y</i> = 4 sin(2π/3) = 2√3"], "(−2, 2√3)")],
        [['Swapping cos and sin', '<i>x</i> uses cos θ.'], ['The wrong quadrant', 'tan<sup>−1</sup> alone gives Quadrants I and IV.'], ['Petals of a rose', 'Odd <i>n</i>: <i>n</i> petals. Even <i>n</i>: 2<i>n</i>.']])
    faq = [('What does TEKS P.3D ask?', 'Graph points in the polar coordinate system and convert between rectangular coordinates and polar coordinates.'), ('What does TEKS P.3E ask?', 'Graph polar equations by plotting points and using technology.'), ('Can r be negative?', 'Yes. (−r, θ) is the same point as (r, θ + π).'), ('Does a point have one polar name?', 'No, infinitely many.')]
    make('polar-coordinates-and-graphs', 22, 'Relations and Geometric Reasoning', 'P.3D, P.3E',
         'P.3D graph points in the polar coordinate system and convert between rectangular coordinates and polar coordinates; P.3E graph polar equations by plotting points and using technology',
         'Polar Coordinates and Polar Graphs', 'Polar Coordinates',
         'Free Precalculus polar coordinate worksheets for Texas TEKS P.3D and P.3E: convert polar and rectangular points and equations, equivalent polar points, and polar graphs. 100 questions with answers.',
         'x = r cos θ, y = r sin θ.', "r = √(x² + y²); choose θ in the point's quadrant.",
         body, faq, sets, seo_title='Precalculus Polar Coordinates and Graphs Worksheets (TEKS P.3D, P.3E)')


if __name__ == "__main__":
    build()
