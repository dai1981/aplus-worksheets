# -*- coding: utf-8 -*-
"""
Texas Grade 8 Math: Dilations on the Coordinate Plane (TEKS 8.3A, 8.3B, 8.3C, 8.10D)
  python3 tools/gen_ustx_math_g8_dilations.py
Dilating points with the origin as center (US Grade 8 maker with a new seed), finding the scale factor, the rule
(x, y) → (kx, ky), attributes kept and changed, and the effect on perimeter and area (own makers).
Wrong answers come from real mistakes: adding the scale factor, thinking a dilation keeps the size, and
multiplying the area by k instead of k².
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g8_transformations as trf
adopt(trf)
trf.R = random.Random(680050)
import gen_us_math_g8_congruence_and_similarity as cs
adopt(cs)
cs.R = random.Random(680051)
tx_common.GRADE = "grade-8"

from fractions import Fraction as F
from ws_common import num

INK = "#1f2937"


def g(v):
    s = ("%.2f" % v).rstrip("0").rstrip(".")
    if "." in s:
        a, b = s.split(".")
        return ("−" if v < 0 else "") + comma(abs(int(a))) + "." + b
    return num(int(s))


def pt(p):
    return "(%s, %s)" % (g(p[0]), g(p[1]))


def one_factor(r):
    k = r.choice([F(2), F(3), F(4), F(1, 2), F(1, 3), F(3, 2), F(5, 2)])
    x, y = r.randint(-6, 6), r.randint(-6, 6)
    if x == 0 or y == 0 or (k * x).denominator != 1 or (k * y).denominator != 1:
        return None
    img = (k * x, k * y)
    ks = g(float(k)) if k.denominator == 1 else fr(k.numerator, k.denominator)
    kind = "enlargement" if k > 1 else "reduction"
    w = [g(float(1 / k)) if (1 / k).denominator == 1 else fr((1 / k).numerator, (1 / k).denominator), g(float(img[0] - x)), g(float(k + 1)) if (k + 1).denominator == 1 else fr((k + 1).numerator, (k + 1).denominator)]
    w = [v for v in dict.fromkeys(w) if v != ks]
    return mcq("Point A%s is dilated with the origin as the center. Its image is A′%s. What is the scale factor?" % (pt((x, y)), pt(img)), ks, w,
               "%s ÷ %s = %s. The scale factor is <b>%s</b>, so it is %s %s." % (g(float(img[0])), g(x), ks, ks, "an" if kind == "enlargement" else "a", kind))


def one_rule(r):
    k = r.choice([F(2), F(3), F(1, 2), F(3, 2), F(1, 4), F(4)])
    ks = g(float(k)) if k.denominator == 1 else fr(k.numerator, k.denominator)
    if r.random() < 0.5:
        return mcq("Which rule describes a dilation with scale factor %s centered at the origin?" % ks, "(x, y) → (%sx, %sy)" % (ks, ks),
                   ["(x, y) → (x + %s, y + %s)" % (ks, ks), "(x, y) → (%sx, y)" % ks, "(x, y) → (x ÷ %s, y ÷ %s)" % (ks, ks)],
                   "A dilation from the origin multiplies <b>both</b> coordinates by the scale factor: <b>(%sx, %sy)</b>." % (ks, ks))
    return mcq("A figure is dilated by (x, y) → (%sx, %sy). Is the image an enlargement or a reduction?" % (ks, ks), "An enlargement" if k > 1 else "A reduction",
               ["A reduction" if k > 1 else "An enlargement", "The same size", "A reflection"], "The scale factor %s is %s 1, so it is <b>%s</b>." % (ks, "greater than" if k > 1 else "less than", "an enlargement" if k > 1 else "a reduction"))


ATTR = [("A triangle is dilated by a scale factor of 3. What happens to its angle measures?", "They stay the same", ["They are multiplied by 3", "They are divided by 3", "They are multiplied by 9"], "Dilations keep the <b>shape</b>: angle measures stay the same."),
        ("A figure is dilated by a scale factor of 2. Which statement is true?", "The image is similar to the original but not congruent", ["The image is congruent to the original", "The image has different angles", "The image is flipped over"], "The sides change length, so the image is <b>similar</b>, not congruent."),
        ("Which attribute changes when a figure is dilated by a scale factor of 1/2?", "The side lengths", ["The angle measures", "The orientation", "The shape"], "Every side length is halved; angles and orientation stay the same."),
        ("A rectangle is dilated by a scale factor of 1. What is true?", "The image is congruent to the original", ["The image is twice as big", "The image is half as big", "The image is a square"], "A scale factor of 1 keeps every length: the image is <b>congruent</b>."),
        ("A dilation has a scale factor between 0 and 1. What kind of dilation is it?", "A reduction", ["An enlargement", "A translation", "No change"], "Scale factors less than 1 make the figure <b>smaller</b>."),
        ("Which ratio is the same for every pair of matching sides in a figure and its dilation?", "Image side ÷ original side", ["Image side − original side", "Image side + original side", "Original side × image side"], "Matching sides are <b>proportional</b>: image ÷ original = scale factor.")]


def one_attr(r):
    q, a, w, e = r.choice(ATTR)
    return mcq(q, a, w, e)


def one_area(r):
    k = r.choice([2, 3, 4, 5, F(1, 2), F(1, 3)])
    kind = r.choice(["per", "area", "area"])
    ks = str(k) if not isinstance(k, F) else fr(k.numerator, k.denominator)
    if kind == "per":
        p = r.choice([12, 18, 24, 30, 36, 48])
        v = F(p) * k
        if v.denominator != 1:
            return None
        return mcq("A figure has a perimeter of %d cm. It is dilated by a scale factor of %s. What is the new perimeter?" % (p, ks), "%d cm" % v, ["%s cm" % g(float(p * F(k) * F(k))), "%s cm" % g(float(p / F(k))), "%d cm" % p],
                   "Lengths are multiplied by %s, so the perimeter is %d × %s = <b>%d cm</b>." % (ks, p, ks, v))
    a = r.choice([9, 12, 18, 20, 36, 45, 72])
    v = F(a) * F(k) * F(k)
    if v.denominator != 1:
        return None
    return mcq("A figure has an area of %d cm². It is dilated by a scale factor of %s. What is the new area?" % (a, ks), "%d cm²" % v, ["%s cm²" % g(float(a * F(k))), "%s cm²" % g(float(a * F(k) ** 3)), "%d cm²" % a],
               "Area is multiplied by the scale factor squared: %d × (%s)² = <b>%d cm²</b>." % (a, ks, v))


def build():
    sets, R = build_sets([
        ("Dilate points from the origin", [("run", trf.set_dilate, (), 20)]),
        ("Find the scale factor", [("collect", one_factor, 20)]),
        ("The dilation rule and enlargement or reduction", [("collect", one_rule, 10), ("collect", one_attr, 6), ("run", cs.set_grid, (), 4)]),
        ("Matching sides are proportional", [("run", cs.set_sides, (), 20)]),
        ("Effect on perimeter and area", [("collect", one_area, 20)]),
    ], 68005)
    finish(sets, R)
    body = lesson('<ul><li>A <b>dilation</b> centered at the origin multiplies both coordinates by the <b>scale factor</b> k: (x, y) → (kx, ky).</li><li>k &gt; 1 is an enlargement; 0 &lt; k &lt; 1 is a reduction.</li><li>Angles and orientation stay the same; side lengths are multiplied by k. The image is <b>similar</b> to the original.</li><li>Perimeter is multiplied by k; <b>area is multiplied by k²</b>.</li></ul>',
        [example("Dilate (4, −2) by k = 1/2", ["(1/2 × 4, 1/2 × −2)"], "(2, −1)"), example("Area 9 cm², k = 3", ["9 × 3²"], "81 cm²")],
        [['Adding the scale factor', '(x, y) → (kx, ky), not (x + k, y + k).'], ['Thinking a dilation keeps the size', 'Only k = 1 keeps the size.'], ['Multiplying the area by k', 'Area grows by k².']])
    faq = [('What does TEKS 8.3C ask?', 'Use an algebraic representation to explain the effect of a given positive rational scale factor applied to two-dimensional figures on a coordinate plane with the origin as the center of dilation.'), ('What does TEKS 8.10D ask?', 'Model the effect on linear and area measurements of dilated two-dimensional shapes.'), ('Is a dilation a rigid transformation?', 'No. It changes size, so it does not keep congruence unless k = 1.'), ('What does TEKS 8.3A ask?', 'Generalize that the ratio of corresponding sides of similar shapes are proportional, including a shape and its dilation.')]
    make('dilations', 5, 'Proportionality', '8.3A, 8.3B, 8.3C, 8.10D',
         '8.3A generalize that the ratio of corresponding sides of similar shapes are proportional, including a shape and its dilation; 8.3B compare and contrast the attributes of a shape and its dilation(s) on a coordinate plane; 8.3C use an algebraic representation to explain the effect of a given positive rational scale factor applied to two-dimensional figures on a coordinate plane with the origin as the center of dilation; 8.10D model the effect on linear and area measurements of dilated two-dimensional shapes',
         'Dilations on the Coordinate Plane', 'Dilations',
         'Free Grade 8 dilation worksheets for Texas TEKS 8.3 and 8.10D: dilate points from the origin, scale factors, the rule (kx, ky), proportional sides and the effect on perimeter and area. 100 questions with answers.',
         'Dilation from the origin: (x, y) → (kx, ky).', 'Perimeter × k, area × k². Angles stay the same.',
         body, faq, sets, seo_title='Grade 8 Dilations Worksheets: Scale Factor and the Coordinate Plane (TEKS 8.3C, STAAR)')


if __name__ == "__main__":
    build()
