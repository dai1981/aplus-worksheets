# -*- coding: utf-8 -*-
"""
Texas Geometry: Dimensional Change: Perimeter, Area, Surface Area and Volume (TEKS G.10B)
  python3 tools/gen_ustx_math_ge_dimensional_change.py
How scaling all dimensions by k changes perimeter, area, surface area and volume, new measures after scaling,
finding the scale factor, and changing only some dimensions (own makers), plus scale factor problems (US Geometry
maker with a new seed).
Wrong answers come from real mistakes: multiplying the area by k, multiplying the volume by k², and doubling the volume
when only the radius doubles.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_ge_dilations_and_similarity as dl
adopt(dl)
dl.R = random.Random(696200)
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
KS = [Fr(2), Fr(3), Fr(4), Fr(5), Fr(1, 2), Fr(1, 3), Fr(3, 2), Fr(10)]
MEAS = [("perimeter", 1), ("area", 2), ("surface area", 2), ("volume", 3), ("circumference", 1), ("lateral area", 2)]


def kf(k):
    return str(k.numerator) if k.denominator == 1 else fr(k.numerator, k.denominator)


def one_effect(r):
    k = r.choice(KS)
    m, p = r.choice(MEAS)
    fig_ = r.choice(["a rectangle", "a triangle", "a cylinder", "a rectangular prism", "a cone", "a pyramid", "a circle"])
    if (m in ("surface area", "volume", "lateral area")) != (fig_ in ("a cylinder", "a rectangular prism", "a cone", "a pyramid")):
        raise AssertionError
    if m == "circumference" and fig_ != "a circle":
        raise AssertionError
    right = "Multiplied by %s" % kf(k ** p)
    w = ["Multiplied by %s" % kf(k ** q) for q in (1, 2, 3) if q != p] + ["Multiplied by %s" % kf(k * 2)]
    w = [x for x in w if x != right]
    lead = "The radius of a circle is" if fig_ == "a circle" else "Every length of %s is" % fig_
    return mcq("%s multiplied by %s. What happens to its %s?" % (lead, kf(k), m), right, w,
               "%s is a %s measure, so it is multiplied by (%s)<sup>%d</sup> = <b>%s</b>." % (m[0].upper() + m[1:], {1: "length", 2: "square", 3: "cubic"}[p], kf(k), p, kf(k ** p)))


def one_new(r):
    k = r.choice([2, 3, 4, 5])
    m, p = r.choice([("perimeter", 1), ("area", 2), ("volume", 3), ("surface area", 2)])
    v = r.choice([6, 8, 12, 15, 20, 24, 30, 36, 40, 45, 50])
    u = {"perimeter": "cm", "area": "cm²", "volume": "cm³", "surface area": "cm²"}[m]
    fig_ = "a solid" if m in ("volume", "surface area") else "a figure"
    ans = v * k ** p
    w = ["%s %s" % (comma(v * k ** q), u) for q in (1, 2, 3) if q != p] + ["%s %s" % (comma(v + k), u)]
    return mcq("The %s of %s is %d %s. It is enlarged by a scale factor of %d. What is the new %s?" % (m, fig_, v, u, k, m), "%s %s" % (comma(ans), u), w,
               "%d × %d<sup>%d</sup> = <b>%s %s</b>." % (v, k, p, comma(ans), u))


def one_k(r):
    k = r.choice([2, 3, 4, 5, 6])
    if r.random() < 0.5:
        a = r.choice([1, 2, 3, 4, 5])
        return mcq("Two similar figures have areas of %d and %d square units. What is the scale factor from the smaller to the larger?" % (a, a * k * k), str(k), [str(k * k), str(k * k * a), str(k + 1)],
                   "Areas scale by <i>k</i><sup>2</sup> = %d, so <i>k</i> = √%d = <b>%d</b>." % (k * k, k * k, k))
    a = r.choice([1, 2, 3, 4])
    return mcq("Two similar solids have volumes of %d and %d cubic units. What is the scale factor?" % (a, a * k ** 3), str(k), [str(k ** 3), str(k * k), str(k + 2)],
               "Volumes scale by <i>k</i><sup>3</sup> = %d, so <i>k</i> = ∛%d = <b>%d</b>." % (k ** 3, k ** 3, k))


NP = [("The length of a rectangle is doubled. The width stays the same. What happens to the area?", "It doubles", ["It is multiplied by 4", "It stays the same", "It is multiplied by 8"], "Only one dimension is doubled, so the area <b>doubles</b>."),
      ("The radius of a cylinder is doubled. The height stays the same. What happens to the volume?", "It is multiplied by 4", ["It doubles", "It is multiplied by 8", "It stays the same"], "V = πr²h; doubling r multiplies r² by 4: <b>×4</b>."),
      ("The height of a cylinder is tripled. The radius stays the same. What happens to the volume?", "It is multiplied by 3", ["It is multiplied by 9", "It is multiplied by 27", "It stays the same"], "Only h changes: <b>×3</b>."),
      ("The length of a box is doubled and its width is tripled. The height stays the same. What happens to the volume?", "It is multiplied by 6", ["It is multiplied by 5", "It is multiplied by 36", "It is multiplied by 216"], "2 × 3 = <b>6</b>."),
      ("The radius of a cone is tripled and the height is halved. What happens to the volume?", "It is multiplied by 4.5", ["It is multiplied by 1.5", "It is multiplied by 9", "It stays the same"], "9 × 1/2 = <b>4.5</b>."),
      ("The base of a triangle is tripled and its height is halved. What happens to the area?", "It is multiplied by 1.5", ["It is multiplied by 3", "It is multiplied by 6", "It stays the same"], "3 × 1/2 = <b>1.5</b>."),
      ("The side of a square is cut in half. What happens to its area?", "It is divided by 4", ["It is divided by 2", "It is divided by 8", "It stays the same"], "(1/2)² = 1/4: <b>divided by 4</b>."),
      ("The radius of a sphere is doubled. What happens to its volume?", "It is multiplied by 8", ["It is multiplied by 4", "It doubles", "It is multiplied by 6"], "2³ = <b>8</b>."),
      ("The radius of a sphere is tripled. What happens to its surface area?", "It is multiplied by 9", ["It is multiplied by 3", "It is multiplied by 27", "It is multiplied by 6"], "3² = <b>9</b>."),
      ("The width of a rectangle is multiplied by 4 and the length by 1/2. What happens to the perimeter?", "It depends on the original length and width", ["It doubles", "It stays the same", "It is multiplied by 4"], "Perimeter adds lengths, so the change <b>depends on the original sizes</b>."),
      ("A cube's edge is multiplied by 5. What happens to its surface area?", "It is multiplied by 25", ["It is multiplied by 5", "It is multiplied by 125", "It is multiplied by 10"], "5² = <b>25</b>."),
      ("The height of a cone is doubled. The radius stays the same. What happens to the volume?", "It doubles", ["It is multiplied by 4", "It is multiplied by 8", "It stays the same"], "Only h changes: <b>×2</b>.")]


def one_np(r):
    q, a, w, e = r.choice(NP)
    return mcq(q, a, w, e)


def build():
    sets, R = build_sets([
        ("Scale every length by k", [("collect", uniq(one_effect), 20)]),
        ("Find the new measure", [("collect", uniq(one_new), 20)]),
        ("Find the scale factor", [("collect", uniq(one_k), 20)]),
        ("Proportional and non-proportional change", [("collect", uniq(one_np), 12), ("collect", uniq(one_effect), 8)]),
        ("Scale factor problems", [("collect", W(dl.one_scale), 20)]),
    ], 69620)
    finish(sets, R)
    body = lesson('<ul><li>If every length is multiplied by <i>k</i>: perimeter × <i>k</i>, area and surface area × <i>k</i><sup>2</sup>, volume × <i>k</i><sup>3</sup>.</li><li>If only some lengths change (non-proportional), multiply by the change in each length that appears in the formula.</li><li>From an area ratio, take the square root to get <i>k</i>; from a volume ratio, the cube root.</li></ul>',
        [example("A box with volume 40 cm³, scale factor 3", ["40 × 3<sup>3</sup> = 40 × 27"], "1,080 cm³")],
        [['Multiplying area by <i>k</i>', 'Area uses <i>k</i><sup>2</sup>.'], ['Multiplying volume by <i>k</i><sup>2</sup>', 'Volume uses <i>k</i><sup>3</sup>.'], ['Doubling the volume when the radius doubles', 'r is squared in V = πr²h.']])
    faq = [('What does TEKS G.10B ask?', 'Determine and describe how changes in the linear dimensions of a shape affect its perimeter, area, surface area, or volume, including proportional and non-proportional dimensional change.'), ('If a figure is scaled by 1/2, what happens to its area?', 'It is multiplied by 1/4.'), ('What is a non-proportional change?', 'Changing some dimensions by different amounts.'), ('Do angles change?', 'Not in a proportional change.')]
    make('dimensional-change', 20, 'Two-Dimensional and Three-Dimensional Figures', 'G.10B',
         'G.10B determine and describe how changes in the linear dimensions of a shape affect its perimeter, area, surface area, or volume, including proportional and non-proportional dimensional change',
         'Dimensional Change: Perimeter, Area, Surface Area and Volume', 'Dimensional Change',
         'Free Geometry worksheets for Texas TEKS G.10B: how scale factors change perimeter, area, surface area and volume, finding scale factors and non-proportional change. 100 questions with answers.',
         'Length × k, area × k², volume × k³.', 'Double the radius of a sphere: volume × 8.',
         body, faq, sets, seo_title='Geometry Dimensional Change Worksheets (TEKS G.10B)')


if __name__ == "__main__":
    build()
