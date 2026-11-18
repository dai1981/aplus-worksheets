# -*- coding: utf-8 -*-
"""
SG Secondary 3 Maths: Areas and Volumes of Similar Figures (MOE syllabus G2: ratio of areas of similar plane
figures; ratio of volumes of similar solids)
  python3 tools/gen_sg_maths_s3_area_and_volume_of_similar_figures.py
Area ratio = (length ratio)², volume ratio = (length ratio)³, working backwards with square and cube roots,
mass and capacity of similar solids, and problems with triangles and models.
Wrong answers come from real mistakes: using the length ratio for area or volume, squaring instead of cubing,
and squaring when going back from an area ratio to a length ratio.
"""
import random
from fractions import Fraction as F
from sg_sec import num, S, make, lesson, collect, T, QN, fr, MINUS, People

R = random.Random(831100)
P = People(R)
SOLIDS = ["cones", "cylinders", "cuboids", "pyramids", "bottles", "jars", "statues", "spheres"]
SHAPES = ["triangles", "rectangles", "hexagons", "trapeziums", "pentagons", "parallelograms"]


def rat(a, b):
    return "%s : %s" % (num(a), num(b))


def fv(v):
    v = F(v)
    return num(v) if v.denominator == 1 else fr(v.numerator, v.denominator)


# ------------------------------------------------------------ set 1: area ratio from lengths
def one_aratio(r):
    a, b = r.sample(range(1, 8), 2)
    from math import gcd
    if gcd(a, b) != 1:
        return None
    sh = r.choice(SHAPES)
    kind = r.choice(["ratio", "ratio", "find"])
    if kind == "ratio":
        q = "Two similar %s have corresponding sides in the ratio %s. Find the ratio of their areas." % (sh, rat(a, b))
        return T(q, rat(a * a, b * b), [rat(a, b), rat(a ** 3, b ** 3), rat(2 * a, 2 * b + 1) if False else rat(a + a, b + b) if False else rat(a * 2, b * 2) if False else rat(a * a, b)],
                 "Area ratio = (length ratio)<sup>2</sup> = %d<sup>2</sup> : %d<sup>2</sup> = <b>%s</b>." % (a, b, rat(a * a, b * b)))
    A = a * a * r.choice([2, 3, 4, 5, 6])
    B_ = F(A * b * b, a * a)
    q = "Two similar %s have corresponding sides of %d cm and %d cm. The smaller one has an area of %s cm². Find the area of the larger one." % (sh, min(a, b), max(a, b), num(A if a < b else B_))
    small, big = (a, b) if a < b else (b, a)
    As = A if a < b else B_
    Ab = As * F(big * big, small * small)
    return QN(q, Ab, [As * F(big, small), As * F(big ** 3, small ** 3), As + (big - small) ** 2], "Area scale factor = (%d ÷ %d)<sup>2</sup> = %s. %s × %s = <b>%s cm²</b>." % (
        big, small, fv(F(big * big, small * small)), num(As), fv(F(big * big, small * small)), num(Ab)), unit=" cm²")


# ------------------------------------------------------------ set 2: volume ratio from lengths
def one_vratio(r):
    a, b = r.sample(range(1, 6), 2)
    from math import gcd
    if gcd(a, b) != 1:
        return None
    so = r.choice(SOLIDS)
    kind = r.choice(["ratio", "find", "find", "surface"])
    if kind == "ratio":
        q = "Two similar %s have heights in the ratio %s. Find the ratio of their volumes." % (so, rat(a, b))
        return T(q, rat(a ** 3, b ** 3), [rat(a * a, b * b), rat(a, b), rat(3 * a, 3 * b) if False else rat(a ** 3, b * b)],
                 "Volume ratio = (length ratio)<sup>3</sup> = %d<sup>3</sup> : %d<sup>3</sup> = <b>%s</b>." % (a, b, rat(a ** 3, b ** 3)))
    small, big = min(a, b), max(a, b)
    if kind == "surface":
        S_ = small * small * r.choice([5, 6, 8, 10, 12])
        q = "Two similar %s have heights %d cm and %d cm. The smaller one has a surface area of %s cm². Find the surface area of the larger one." % (so, small * 2, big * 2, num(S_))
        ans = S_ * F(big * big, small * small)
        return QN(q, ans, [S_ * F(big ** 3, small ** 3), S_ * F(big, small), S_ + big - small], "Surface area is an area, so square the scale factor: (%d ÷ %d)<sup>2</sup> = %s. %s × %s = <b>%s cm²</b>." % (
            big * 2, small * 2, fv(F(big * big, small * small)), num(S_), fv(F(big * big, small * small)), num(ans)), unit=" cm²")
    V = small ** 3 * r.choice([2, 3, 4, 5, 8, 10])
    unit = r.choice([1, 3])
    q = "Two similar %s have heights %d cm and %d cm. The smaller one has a volume of %s cm³. Find the volume of the larger one." % (so, small * unit, big * unit, num(V))
    ans = V * F(big ** 3, small ** 3)
    return QN(q, ans, [V * F(big * big, small * small), V * F(big, small), V + (big - small) ** 3], "Volume scale factor = (%d ÷ %d)<sup>3</sup> = %s. %s × %s = <b>%s cm³</b>." % (
        big * unit, small * unit, fv(F(big ** 3, small ** 3)), num(V), fv(F(big ** 3, small ** 3)), num(ans)), unit=" cm³")


# ------------------------------------------------------------ set 3: working backwards
def one_back(r):
    a, b = r.sample(range(1, 7), 2)
    from math import gcd
    if gcd(a, b) != 1:
        return None
    kind = r.choice(["a2l", "v2l", "v2a", "a2v"])
    if kind == "a2l":
        q = "The areas of two similar figures are in the ratio %s. Find the ratio of their corresponding lengths." % rat(a * a, b * b)
        return T(q, rat(a, b), [rat(a * a, b * b), rat(a ** 4, b ** 4), rat(a * a // 2 if a * a % 2 == 0 else a * a, b * b * 2) if False else rat(a ** 3, b ** 3)],
                 "Length ratio = √(area ratio) = √%d : √%d = <b>%s</b>." % (a * a, b * b, rat(a, b)))
    if kind == "v2l":
        if max(a, b) > 5:
            return None
        q = "The volumes of two similar solids are in the ratio %s. Find the ratio of their heights." % rat(a ** 3, b ** 3)
        return T(q, rat(a, b), [rat(a ** 3, b ** 3), rat(a * a, b * b), rat(a ** 3 // 3 if a ** 3 % 3 == 0 else a ** 3, b ** 3 * 3) if False else rat(a + 1, b + 1)],
                 "Length ratio = cube root of the volume ratio: <b>%s</b>." % rat(a, b))
    if kind == "v2a":
        if max(a, b) > 5:
            return None
        q = "The volumes of two similar solids are in the ratio %s. Find the ratio of their surface areas." % rat(a ** 3, b ** 3)
        return T(q, rat(a * a, b * b), [rat(a ** 3, b ** 3), rat(a, b), rat(a ** 6, b ** 6) if max(a, b) < 4 else rat(a ** 3, b * b)],
                 "Cube root gives the length ratio %s. Square it for area: <b>%s</b>." % (rat(a, b), rat(a * a, b * b)))
    q = "The surface areas of two similar solids are in the ratio %s. Find the ratio of their volumes." % rat(a * a, b * b)
    return T(q, rat(a ** 3, b ** 3), [rat(a * a, b * b), rat(a ** 4, b ** 4), rat(a, b)],
             "Square root gives the length ratio %s. Cube it for volume: <b>%s</b>." % (rat(a, b), rat(a ** 3, b ** 3)))


# ------------------------------------------------------------ set 4: mass and capacity
def one_mass(r):
    small, big = sorted(r.sample(range(1, 6), 2))
    kind = r.choice(["mass", "mass", "cap", "heightfrommass"])
    nm, he, his = P.next()
    if kind == "mass":
        m = small ** 3 * r.choice([20, 40, 50, 60, 80])
        q = "Two similar solid metal statues are %d cm and %d cm tall. The smaller one has a mass of %s g. Find the mass of the larger one." % (small * 5, big * 5, num(m))
        ans = m * F(big ** 3, small ** 3)
        return QN(q, ans, [m * F(big * big, small * small), m * F(big, small), m + (big - small) * 100], "Mass is proportional to volume, so cube the length ratio: (%d ÷ %d)<sup>3</sup> × %s = <b>%s g</b>." % (
            big * 5, small * 5, num(m), num(ans)), unit=" g")
    if kind == "cap":
        c = r.choice([250, 300, 500, 400])
        q = "A small bottle holds %d ml. A similar bottle is %d times as tall. How much does the larger bottle hold?" % (c, big)
        ans = c * big ** 3
        unit = " ml"
        return QN(q, ans, [c * big * big, c * big, c + big ** 3], "Capacity is a volume: %d<sup>3</sup> = %d, so %s × %d = <b>%s ml</b>." % (big, big ** 3, num(c), big ** 3, num(ans)), unit=unit)
    m1 = small ** 3 * 10
    m2 = big ** 3 * 10
    h1 = small * r.choice([4, 6, 8])
    q = "Two similar solid blocks have masses %s g and %s g. The smaller block is %d cm high. How high is the larger block?" % (num(m1), num(m2), h1)
    ans = F(h1 * big, small)
    return QN(q, ans, [h1 * F(m2, m1), h1 * F(big * big, small * small), h1 + big - small], "Mass ratio = volume ratio = %s, so the length ratio is %s. %d × %s = <b>%s cm</b>." % (
        rat(small ** 3, big ** 3), rat(small, big), h1, fv(F(big, small)), num(ans)), unit=" cm")


# ------------------------------------------------------------ set 5: problems
def one_prob(r):
    kind = r.choice(["tri", "tri", "trap", "model", "map", "cone"])
    if kind in ("tri", "trap"):
        a, b = r.sample(range(1, 6), 2)
        a, b = min(a, b), max(a, b)
        A_small = a * a * r.choice([2, 3, 4, 5])
        A_big = A_small * F(b * b, a * a)
        if kind == "tri":
            q = "In △ABC, DE is parallel to BC with D on AB and E on AC. AD : AB = %s. The area of △ADE is %s cm². Find the area of △ABC." % (rat(a, b), num(A_small))
            return QN(q, A_big, [A_small * F(b, a), A_big - A_small, A_small * F(b ** 3, a ** 3)], "△ADE and △ABC are similar with length ratio %s, so the area ratio is %s. %s × %s = <b>%s cm²</b>." % (
                rat(a, b), rat(a * a, b * b), num(A_small), fv(F(b * b, a * a)), num(A_big)), unit=" cm²")
        q = "In △ABC, DE is parallel to BC with D on AB and E on AC. AD : DB = %s. The area of △ADE is %s cm². Find the area of the trapezium DBCE." % (rat(a, b - a), num(A_small))
        return QN(q, A_big - A_small, [A_big, A_small * F(b - a, a) * F(b - a, a), A_small * F(b, a) - A_small], "AD : AB = %s, so △ADE : △ABC = %s. △ABC = %s cm², so DBCE = %s − %s = <b>%s cm²</b>." % (
            rat(a, b), rat(a * a, b * b), num(A_big), num(A_big), num(A_small), num(A_big - A_small)), unit=" cm²")
    if kind == "model":
        k = r.choice([10, 20, 25, 50])
        area = r.choice([12, 18, 24, 30, 40])
        q = "A model car is made to a scale of 1 : %d. The area of the model's windscreen is %d cm². Find the area of the real windscreen, in m²." % (k, area)
        ans = F(area * k * k, 10000)
        return QN(q, ans, [F(area * k, 10000), F(area * k * k, 100), F(area * k ** 3, 10000)], "Area scale factor = %d<sup>2</sup> = %s. %d × %s = %s cm² = <b>%s m²</b> (1 m² = 10 000 cm²)." % (
            k, num(k * k), area, num(k * k), num(area * k * k), num(ans)), unit=" m²")
    if kind == "map":
        n = r.choice([20000, 25000, 50000])
        a = r.choice([2, 4, 6, 8])
        ans = F(a * n * n, 10 ** 10)
        q = "A map has a scale of 1 : %s. A park has an area of %d cm² on the map. Find its actual area in km²." % (num(n), a)
        return QN(q, ans, [F(a * n, 100000), F(a * n * n, 10 ** 8), F(a * n * n, 10 ** 11)], "1 cm represents %s km, so 1 cm² represents %s km². %d × %s = <b>%s km²</b>." % (
            num(F(n, 100000)), num(F(n * n, 10 ** 10)), a, num(F(n * n, 10 ** 10)), num(ans)), unit=" km²")
    h = r.choice([2, 3, 4])
    V = r.choice([270, 540, 810, 1080, 640, 320])
    V_small = F(V, h ** 3)
    if V_small.denominator != 1:
        return None
    q = "A cone of volume %s cm³ is cut parallel to its base, %s of the way down from the tip, to make a small cone. Find the volume of the small cone." % (num(V), fr(1, h))
    return QN(q, V_small, [F(V, h * h), F(V, h), V - V_small], "The small cone is similar with length ratio 1 : %d, so the volume ratio is 1 : %d. %s ÷ %d = <b>%s cm³</b>." % (
        h, h ** 3, num(V), h ** 3, num(V_small)), unit=" cm³")


def build():
    sets = [S("Areas of similar figures", collect(one_aratio, 20, R)),
            S("Volumes of similar solids", collect(one_vratio, 20, R)),
            S("Working backwards", collect(one_back, 20, R)),
            S("Mass and capacity", collect(one_mass, 20, R)),
            S("Problems", collect(one_prob, 20, R))]
    body = lesson(
        "<p>If two figures are similar with lengths in the ratio <i>a</i> : <i>b</i>, then</p>"
        "<ul><li>areas (including surface areas) are in the ratio <b><i>a</i><sup>2</sup> : <i>b</i><sup>2</sup></b>;</li>"
        "<li>volumes (and masses or capacities of the same material) are in the ratio <b><i>a</i><sup>3</sup> : <i>b</i><sup>3</sup></b>.</li></ul>"
        "<p>To go back, take the square root of an area ratio or the cube root of a volume ratio to get the length ratio first.</p>",
        [("Two similar jugs are 10 cm and 15 cm tall. The small one holds 400 ml. How much does the large one hold?", ["Length ratio 2 : 3", "Volume ratio 8 : 27", "400 × 27 ÷ 8"], "1350 ml"),
         ("The areas of two similar triangles are 16 cm² and 49 cm². Find the ratio of their sides.", ["√16 : √49"], "4 : 7")],
        ["Using the length ratio for an area or a volume.",
         "Squaring instead of cubing for volume, mass or capacity.",
         "Squaring an area ratio to get a length ratio. Take the square root instead.",
         "Using AD : DB instead of AD : AB when DE ∥ BC."])
    faq = [("How are the areas of similar figures related?", "If the lengths are in the ratio a : b, the areas are in the ratio a² : b²."),
           ("How are the volumes of similar solids related?", "If the lengths are in the ratio a : b, the volumes are in the ratio a³ : b³. Masses and capacities of the same material follow the same ratio."),
           ("How do I find a length ratio from a volume ratio?", "Take the cube root of each part of the volume ratio. For an area ratio, take the square root."),
           ("Is surface area an area or a volume?", "An area, so it scales by the square of the length ratio.")]
    make(3, "area-and-volume-of-similar-figures", 11, "G2",
         "Areas and Volumes of Similar Figures",
         "", "Areas and volumes of similar figures", "",
         "Free Secondary 3 maths worksheets on areas of similar figures and volumes of similar solids: area ratio = (length ratio)², volume ratio = (length ratio)³, mass, capacity and problems. 100 questions with answers.",
         "Lengths a : b give areas a² : b² and volumes a³ : b³.",
         "To go back, take the square root of an area ratio or the cube root of a volume ratio.",
         body, faq, sets, R)


if __name__ == "__main__":
    build()
