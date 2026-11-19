# -*- coding: utf-8 -*-
"""
Texas Precalculus: Conic Sections (TEKS P.3F, P.3G)
  python3 tools/gen_ustx_math_pc_conics.py
The conic formed when a plane cuts a double-napped cone and the locus definitions of the conics (own makers),
identifying conics from equations, parabolas and applications (US Precalculus makers with a new seed), and numbers from
locus definitions (own maker).
Wrong answers come from real mistakes: calling a cut parallel to the side an ellipse, mixing up the sum and the
difference of distances, and forgetting that 2a is the sum.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_pc_conic_sections as cs
adopt(cs)
cs.R = random.Random(698230)
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


CONICS = ["Circle", "Ellipse", "Parabola", "Hyperbola"]
CUTS = [("perpendicular to the axis of the cone (horizontal), not through the vertex", "Circle"),
        ("tilted a little from horizontal, cutting through only one nappe all the way around", "Ellipse"),
        ("tilted so it cuts only one nappe in a closed curve that is not a circle", "Ellipse"),
        ("parallel to one side (a generator line) of the cone", "Parabola"),
        ("tilted at the same angle as the side of the cone, cutting only one nappe in an open curve", "Parabola"),
        ("parallel to the axis of the cone, cutting both nappes", "Hyperbola"),
        ("steep enough to cut both nappes of the cone", "Hyperbola"),
        ("vertical, not through the vertex, so it meets the top and bottom nappes", "Hyperbola")]
LOCI = [("the set of all points the same distance from one fixed point", "Circle"), ("the set of all points whose distances to two fixed points add to a constant", "Ellipse"),
        ("the set of all points the same distance from a fixed point and a fixed line", "Parabola"), ("the set of all points whose distances to two fixed points differ by a constant", "Hyperbola"),
        ("a curve with a center, a radius and every point equally far from the center", "Circle"), ("a closed curve with two foci and a major axis", "Ellipse"),
        ("a curve with one focus and one directrix", "Parabola"), ("a curve with two branches, two foci and two asymptotes", "Hyperbola")]
deg_items = [("passes through the vertex of the cone and is horizontal", "A single point"), ("passes through the vertex and contains one side of the cone", "A single line"),
             ("passes through the vertex and is vertical", "Two crossing lines")]


def one_cone(r):
    if r.random() < 0.85:
        t, right = r.choice(CUTS)
        opts = [c for c in CONICS if c != right]
    else:
        t, right = r.choice(deg_items)
        opts = [v for _, v in deg_items if v != right] + ["Parabola"]
    return mcq("A plane cuts a double-napped cone. The plane is %s. What shape is the cut?" % t, right, opts,
               "The angle of the plane decides the conic: horizontal → circle; tilted, one nappe → ellipse; parallel to a side → parabola; both nappes → hyperbola. <b>%s</b>." % right)


def one_locus(r):
    t, right = r.choice(LOCI)
    return mcq("Which conic section is %s?" % t, right, [c for c in CONICS if c != right], "This is the locus definition of a %s. <b>%s</b>." % (right.lower(), right))


def one_num(r):
    kind = r.choice(["ell", "hyp", "par", "circ"])
    if kind == "ell":
        a = r.choice([5, 10, 13, 15, 17, 25])
        c = {5: 3, 10: 6, 13: 5, 15: 9, 17: 8, 25: 7}[a]
        b = int((a * a - c * c) ** 0.5)
        if r.random() < 0.5:
            q = "An ellipse has foci (±%d, 0). For every point on it, the distances to the two foci add to %d. What is the length of the minor axis?" % (c, 2 * a)
            right, w = str(2 * b), [str(b), str(2 * a), str(2 * c)]
            e = "2<i>a</i> = %d, so <i>a</i> = %d. <i>b</i><sup>2</sup> = <i>a</i><sup>2</sup> − <i>c</i><sup>2</sup> = %d − %d = %d, <i>b</i> = %d, minor axis 2<i>b</i> = %d." % (2 * a, a, a * a, c * c, b * b, b, 2 * b)
        else:
            q = "A point on an ellipse is %d units from one focus. The major axis is %d units long. How far is the point from the other focus?" % (a - c + 1, 2 * a)
            right, w = str(2 * a - (a - c + 1)), [str(a - c + 1), str(a + c - 1 + 2), str(2 * a + (a - c + 1))]
            e = "The distances add to the length of the major axis: %d − %d = %d." % (2 * a, a - c + 1, 2 * a - (a - c + 1))
    elif kind == "hyp":
        a = r.choice([3, 4, 5, 6, 8])
        c = a + r.choice([1, 2, 3])
        d1 = r.randint(2 * a + 2, 2 * a + 15)
        q = "For every point on a hyperbola, the distances to the two foci differ by %d. A point is %d units from the nearer focus. How far is it from the other focus?" % (2 * a, d1)
        right, w = str(d1 + 2 * a), [str(d1 - 2 * a) if d1 - 2 * a > 0 else str(d1 + a), str(2 * a), str(d1 + a)]
        e = "|<i>d</i><sub>1</sub> − <i>d</i><sub>2</sub>| = 2<i>a</i> = %d, so the far distance is %d + %d = %d." % (2 * a, d1, 2 * a, d1 + 2 * a)
    elif kind == "par":
        p = r.choice([1, 2, 3, 4, 5, 6])
        x0 = r.choice([2, 4, 6, 8]) * p
        y0 = Fr(x0 * x0, 4 * p)
        if y0.denominator != 1:
            raise AssertionError
        q = "A parabola has focus (0, %d) and directrix <i>y</i> = −%d. The point (%d, %s) is on it. How far is that point from the focus?" % (p, p, x0, ft(y0))
        right, w = ft(y0 + p), [ft(y0), ft(y0 - p), str(x0)]
        e = "On a parabola, distance to the focus = distance to the directrix = %s − (−%d) = %s." % (ft(y0), p, ft(y0 + p))
    else:
        h, k, rr = r.randint(-6, 6), r.randint(-6, 6), r.choice([3, 4, 5, 6, 7, 8, 9, 10])
        q = "A circle is the set of points %d units from (%s, %s). Which equation describes it?" % (rr, sg(h), sg(k))
        sh = lambda v, var: var if v == 0 else "(%s %s %d)" % (var, MINUS if v > 0 else "+", abs(v))
        E = lambda a_, b_, c_: "%s<sup>2</sup> + %s<sup>2</sup> = %d" % (sh(a_, X), sh(b_, "<i>y</i>"), c_)
        right, w = E(h, k, rr * rr), [E(h, k, rr), E(-h, -k, rr * rr) if (h, k) != (0, 0) else E(1, 1, rr * rr), E(k, h, rr * rr) if h != k else E(h + 1, k, rr * rr)]
        e = "Every point (<i>x</i>, <i>y</i>) is %d from the center: (<i>x</i> − <i>h</i>)<sup>2</sup> + (<i>y</i> − <i>k</i>)<sup>2</sup> = %d<sup>2</sup>." % (rr, rr)
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Slicing a cone", [("collect", uniq(one_cone), 10), ("collect", uniq(one_locus), 8), ("collect", W(cs.one_id), 2)]),
        ("Identify the conic from its equation", [("collect", W(cs.one_id), 20)]),
        ("Parabolas", [("collect", W(cs.one_par), 20)]),
        ("Use the locus definitions", [("collect", uniq(one_num), 20)]),
        ("Conics in the real world", [("collect", W(cs.one_app), 20)]),
    ], 69823)
    finish(sets, R)
    body = lesson('<ul><li>A plane cutting a double-napped cone makes a <b>circle</b> (horizontal), an <b>ellipse</b> (tilted, one nappe), a <b>parabola</b> (parallel to a side) or a <b>hyperbola</b> (both nappes).</li><li>Circle: every point is the same distance <i>r</i> from the center.</li><li>Ellipse: the distances to two foci <b>add</b> to 2<i>a</i>. Hyperbola: they <b>differ</b> by 2<i>a</i>.</li><li>Parabola: every point is the same distance from the focus and the directrix.</li></ul>',
        [example("Foci (±4, 0), distances add to 10", ["2<i>a</i> = 10, <i>a</i> = 5", "<i>b</i><sup>2</sup> = 25 − 16 = 9"], "<span class='fr'><span class='fn'><i>x</i><sup>2</sup></span><span class='fd'>25</span></span> + <span class='fr'><span class='fn'><i>y</i><sup>2</sup></span><span class='fd'>9</span></span> = 1")],
        [['Parallel to a side is an ellipse', 'It is a parabola.'], ['Sum and difference mixed up', 'Ellipse: sum. Hyperbola: difference.'], ['Using <i>a</i> for the sum', 'The sum is 2<i>a</i>.']])
    faq = [('What does TEKS P.3F ask?', 'Determine the conic section formed when a plane intersects a double-napped cone.'), ('What does TEKS P.3G ask?', 'Make connections between a locus definition of conic sections and its equation in rectangular coordinates.'), ('What is a degenerate conic?', 'A point, a line or two lines, made when the plane passes through the vertex.'), ('Why is a circle a special ellipse?', 'Its two foci are at the same point, the center.')]
    make('conic-sections', 23, 'Relations and Geometric Reasoning', 'P.3F, P.3G',
         'P.3F determine the conic section formed when a plane intersects a double-napped cone; P.3G make connections between a locus definition of conic sections and its equation in rectangular coordinates',
         'Conic Sections', 'Conic Sections',
         'Free Precalculus conic section worksheets for Texas TEKS P.3F and P.3G: slicing a cone, locus definitions, identifying conics, parabolas and applications. 100 questions with answers.',
         'Ellipse: distances to the foci add to 2a. Hyperbola: they differ by 2a.', 'Parabola: same distance from focus and directrix.',
         body, faq, sets, seo_title='Precalculus Conic Sections Worksheets (TEKS P.3F, P.3G)')


if __name__ == "__main__":
    build()
