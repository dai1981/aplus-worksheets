# -*- coding: utf-8 -*-
"""
Texas Geometry: Geometric Probability: Length and Area (TEKS G.13B)
  python3 tools/gen_ustx_math_ge_geometric_probability.py
Probability on a segment, a circle inside a square, targets with rings, regions in rectangles, and spinners (own
makers).
Wrong answers come from real mistakes: using the radius ratio instead of the area ratio, using the complement, and
dividing by the wrong total.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)

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
import math


def frs(f):
    return fr(f.numerator, f.denominator) if f.denominator != 1 else str(f.numerator)


def one_seg(r):
    L = r.choice([10, 12, 15, 16, 18, 20, 24, 30, 36, 40])
    a = r.randint(0, L - 2)
    b = r.randint(a + 1, L - 1 if a + 1 < L - 1 else L)
    if b - a == L:
        raise AssertionError
    p = Fr(b - a, L)
    w = [frs(1 - p), frs(Fr(b - a, L + (b - a))), frs(Fr(b, L)) if b != b - a else frs(Fr(a + 1, L))]
    return mcq("A point is chosen at random on <span class='ov'>AB</span>, where A = 0 and B = %d on a number line. What is the probability it lies between %d and %d?" % (L, a, b), frs(p), w,
               "Favorable length %d ÷ total length %d = <b>%s</b>." % (b - a, L, frs(p)))


def one_circ(r):
    rad = r.randint(1, 6)
    s = r.choice([n for n in range(2 * rad, 2 * rad + 10)])
    p = math.pi * rad * rad / (s * s)
    right = "%d%%" % round(100 * p)
    w = [x for x in ("%d%%" % round(100 * (1 - p)), "%d%%" % round(100 * 2 * rad / s), "%d%%" % round(100 * math.pi * rad / s), "%d%%" % round(100 * rad / s), "%d%%" % round(100 * rad * rad / (s * s))) if int(x[:-1]) <= 100]
    return mcq("A circle of radius %d in. is drawn inside a square of side %d in. A point in the square is chosen at random. What is the probability it is inside the circle, to the nearest percent?" % (rad, s), right, w,
               "π × %d<sup>2</sup> ÷ %d<sup>2</sup> = %.3f ≈ <b>%s</b>." % (rad, s, p, right))


def one_ring(r):
    r1, r2 = sorted(r.sample(range(1, 11), 2))
    if r.random() < 0.5:
        p = Fr(r1 * r1, r2 * r2)
        q = "A target has a bullseye of radius %d cm inside a circle of radius %d cm. A dart hits the target at a random point. What is the probability it hits the bullseye?" % (r1, r2)
        w = [frs(Fr(r1, r2)) if Fr(r1, r2) != p else frs(1 - p), frs(1 - p), frs(Fr(r1, r2 * r2)) if Fr(r1, r2 * r2) != p else frs(Fr(r1, r1 + r2))]
        e = "π(%d)<sup>2</sup> ÷ π(%d)<sup>2</sup> = <b>%s</b>." % (r1, r2, frs(p))
    else:
        p = Fr(r2 * r2 - r1 * r1, r2 * r2)
        q = "A target has an inner circle of radius %d cm inside a circle of radius %d cm. A dart lands at a random point on the target. What is the probability it lands in the outer ring?" % (r1, r2)
        w = [frs(1 - p), frs(Fr(r2 - r1, r2)) if Fr(r2 - r1, r2) != p else frs(Fr(r1, r2)), frs(Fr(r2 - r1, r1 + r2)) if Fr(r2 - r1, r1 + r2) != p else frs(Fr(1, r2))]
        e = "(%d − %d) ÷ %d = <b>%s</b>." % (r2 * r2, r1 * r1, r2 * r2, frs(p))
    return mcq(q, frs(p), w, e)


def one_rect(r):
    W_, H = r.randint(6, 20), r.randint(5, 15)
    w_, h = r.randint(1, W_ - 1), r.randint(1, H - 1)
    p = Fr(w_ * h, W_ * H)
    place = r.choice(["a park", "a parking lot", "a field", "a garden", "a yard"])
    obj = r.choice(["a sandbox", "a food truck space", "a flower bed", "a pond", "a fountain area"])
    w = [frs(1 - p), frs(Fr(w_ + h, W_ + H)) if Fr(w_ + h, W_ + H) != p else frs(Fr(w_, W_ * H)), frs(Fr(w_ * h, W_ * H + w_ * h))]
    return mcq("%s is a %d m by %d m rectangle. Inside it, %s is %d m by %d m. A ball lands at a random point in %s. What is the probability it lands in %s?" % (place[0].upper() + place[1:], W_, H, obj, w_, h, place.replace("a ", "the ", 1), obj.replace("a ", "the ", 1)), frs(p), w,
               "%d ÷ %d = <b>%s</b>." % (w_ * h, W_ * H, frs(p)))


USED_A = set()


def one_spin(r):
    a = r.choice([20, 30, 36, 40, 45, 60, 72, 80, 90, 100, 120, 135, 150, 210, 240, 270])
    if a in USED_A:
        raise AssertionError
    p = Fr(a, 360)
    w = [frs(1 - p), frs(Fr(a, 180)) if a < 180 else frs(Fr(1, 3) if p != Fr(1, 3) else Fr(1, 4)), frs(Fr(a, 100)) if a < 100 and Fr(a, 100) != p else frs(Fr(1, 2) if p != Fr(1, 2) else Fr(1, 6))]
    c = r.choice(["red", "blue", "green", "yellow"])
    USED_A.add(a)
    return mcq("A spinner has a %s sector with a central angle of %d°. What is the probability the spinner lands on %s?" % (c, a, c), frs(p), w, "%d ÷ 360 = <b>%s</b>." % (a, frs(p)))


def build():
    sets, R = build_sets([
        ("Probability on a segment", [("collect", uniq(one_seg), 20)]),
        ("Spinners and sectors", [("collect", uniq(one_spin), 12), ("collect", uniq(one_seg), 8)]),
        ("Regions in rectangles", [("collect", uniq(one_rect), 20)]),
        ("Targets and rings", [("collect", uniq(one_ring), 20)]),
        ("Circles inside squares", [("collect", uniq(one_circ), 20)]),
    ], 69628)
    finish(sets, R)
    body = lesson('<ul><li><b>Geometric probability</b> = favorable length or area ÷ total length or area.</li><li>On a segment, use lengths. In a region, use areas.</li><li>For a spinner, use the angle of the sector ÷ 360°.</li><li>For circles, square the radii: a radius twice as big has 4 times the area.</li></ul>',
        [example("Bullseye radius 2, target radius 6", ["4π ÷ 36π"], "1/9")],
        [['Using the radius ratio', 'Area uses <i>r</i><sup>2</sup>.'], ['Using the complement', 'Read which region is asked for.'], ['Dividing by the wrong total', 'Divide by the whole region.']])
    faq = [('What does TEKS G.13B ask?', 'Determine probabilities based on area to solve contextual problems.'), ('What if the region is a sector?', 'Use the angle ÷ 360°.'), ('Can geometric probability be 1?', 'Yes, if the favorable region is the whole region.'), ('Do I need π?', 'Often it cancels; otherwise use 3.14 or a calculator.')]
    make('geometric-probability', 28, 'Probability', 'G.13B',
         'G.13B determine probabilities based on area to solve contextual problems',
         'Geometric Probability: Length and Area', 'Geometric Probability',
         'Free Geometry worksheets for Texas TEKS G.13B: geometric probability with lengths, areas, targets, spinners and circles inside squares. 100 questions with answers.',
         'Probability = favorable area ÷ total area.', 'Bullseye radius 2 in target radius 6: 1/9.',
         body, faq, sets, seo_title='Geometry Geometric Probability Worksheets (TEKS G.13B)')


if __name__ == "__main__":
    build()
