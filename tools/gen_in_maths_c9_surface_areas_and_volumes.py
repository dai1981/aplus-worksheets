# -*- coding: utf-8 -*-
"""
India Class 9 Maths, NCERT Chapter 11: Surface Areas and Volumes — Cones and Spheres (CBSE Unit V Mensuration)
  python3 tools/gen_in_maths_c9_surface_areas_and_volumes.py
Slant height and curved surface area of a right circular cone, total surface area, surface area of a sphere and a
hemisphere (curved and total), volume of a cone, volume of a sphere and a hemisphere, and problems (tents, cones of
ice-cream, domes, bowls, litres and rupees, what happens when the radius is doubled). π = 22/7.
Wrong answers come from real mistakes: the height used instead of the slant height (or the reverse), forgetting ⅓ for the
cone, 4πr² for a hemisphere, 2πr² for the total surface of a solid hemisphere, and doubling the volume when the radius doubles.
"""
import random
from fractions import Fraction as F
from in_common import num, S, make, lesson, mix, T, inr, People
from in_common import QN as _QN

R = random.Random(909011)
P = People(R)
PI = F(22, 7)
CONES = [(7, 24, 25), (21, 20, 29), (14, 48, 50), (F(7, 2), 12, F(25, 2)), (21, 72, 75), (F(21, 2), 36, F(75, 2)), (28, 21, 35), (14, F(21, 2), F(35, 2)), (7, F(21, 4), F(35, 4))]
RADII = [F(7, 2), 7, F(21, 2), 14, 21, F(7, 10), F(21, 10), 28, F(7, 4)]


RV = [F(21, 10), F(21, 5), F(63, 10), F(42, 5), F(21, 2), 21]


def QN(q, ans, wrongs, e, unit=""):
    ans = F(ans)
    return _QN(q, ans, list(wrongs) + [ans * 2, ans / 2, ans * 3, ans * 4], e, unit=unit, near=())


# ---------------------------------------------------------------- set 1: slant height and curved surface of a cone
def one_csa(r):
    r_, h, l = r.choice(CONES)
    kind = r.choice(["l", "csa", "csa", "csa_l"])
    if kind == "l":
        return QN("A cone has base radius %s cm and height %s cm. Find its slant height." % (num(r_), num(h)), l, [r_ + h, h - r_ if h > r_ else r_ - h + 1, l + 1],
                  "l = √(r² + h²) = √(%s² + %s²) = <b>%s cm</b>." % (num(r_), num(h), num(l)), unit=" cm")
    if kind == "csa":
        v = PI * r_ * l
        return QN("A cone has base radius %s cm and height %s cm. Find its curved surface area. (Use π = 22/7.)" % (num(r_), num(h)), v, [PI * r_ * h, PI * r_ * (l + r_), F(1, 3) * PI * r_ * r_ * h],
                  "First l = √(%s² + %s²) = %s cm. CSA = πrl = 22/7 × %s × %s = <b>%s cm²</b>." % (num(r_), num(h), num(l), num(r_), num(l), num(v)), unit=" cm²")
    v = PI * r_ * l
    return QN("A cone has slant height %s cm and base radius %s cm. Find its curved surface area. (Use π = 22/7.)" % (num(l), num(r_)), v, [2 * PI * r_ * l, PI * r_ * r_, PI * r_ * (l + r_)],
              "CSA = πrl = 22/7 × %s × %s = <b>%s cm²</b>." % (num(r_), num(l), num(v)), unit=" cm²")


# ---------------------------------------------------------------- set 2: total surface area of a cone, back to r or l
def one_tsa(r):
    r_, h, l = r.choice(CONES)
    kind = r.choice(["tsa", "tsa", "back", "tent"])
    if kind == "tsa":
        v = PI * r_ * (l + r_)
        return QN("Find the total surface area of a solid cone with radius %s cm and slant height %s cm. (Use π = 22/7.)" % (num(r_), num(l)), v, [PI * r_ * l, PI * r_ * (h + r_), PI * r_ * (l + 2 * r_)],
                  "TSA = πr(l + r) = 22/7 × %s × (%s + %s) = <b>%s cm²</b>." % (num(r_), num(l), num(r_), num(v)), unit=" cm²")
    if kind == "back":
        c = PI * r_ * l
        return QN("The curved surface area of a cone is %s cm² and its slant height is %s cm. Find the radius of its base. (Use π = 22/7.)" % (num(c), num(l)), r_, [c / l, r_ * 2, l - r_],
                  "πrl = %s, so r = %s ÷ (22/7 × %s) = <b>%s cm</b>." % (num(c), num(c), num(l), num(r_)), unit=" cm")
    rate = r.choice([50, 70, 100, 120])
    v = PI * r_ * l
    return T("A conical tent has base radius %s m and slant height %s m. Canvas costs %s per m². Find the cost of the canvas. (Use π = 22/7.)" % (num(r_), num(l), inr(rate)), inr(v * rate),
             [inr(PI * r_ * (l + r_) * rate), inr(PI * r_ * h * rate), inr(v)], "Canvas = πrl = %s m². Cost = %s × %d = <b>%s</b>." % (num(v), num(v), rate, inr(v * rate)))


# ---------------------------------------------------------------- set 3: spheres and hemispheres
def one_sph(r):
    r_ = r.choice(RADII)
    kind = r.choice(["sphere", "sphere", "hcsa", "htsa", "back"])
    if kind == "sphere":
        v = 4 * PI * r_ * r_
        return QN("Find the surface area of a sphere of radius %s cm. (Use π = 22/7.)" % num(r_), v, [2 * PI * r_ * r_, PI * r_ * r_, 3 * PI * r_ * r_],
                  "S = 4πr² = 4 × 22/7 × %s² = <b>%s cm²</b>." % (num(r_), num(v)), unit=" cm²")
    if kind == "hcsa":
        v = 2 * PI * r_ * r_
        return QN("Find the curved surface area of a hemisphere of radius %s cm. (Use π = 22/7.)" % num(r_), v, [4 * PI * r_ * r_, 3 * PI * r_ * r_, PI * r_ * r_],
                  "CSA of a hemisphere = 2πr² = <b>%s cm²</b>." % num(v), unit=" cm²")
    if kind == "htsa":
        v = 3 * PI * r_ * r_
        return QN("Find the total surface area of a solid hemisphere of radius %s cm. (Use π = 22/7.)" % num(r_), v, [2 * PI * r_ * r_, 4 * PI * r_ * r_, PI * r_ * r_],
                  "TSA = 2πr² + πr² = 3πr² = <b>%s cm²</b>." % num(v), unit=" cm²")
    s = 4 * PI * r_ * r_
    return QN("The surface area of a sphere is %s cm². Find its radius. (Use π = 22/7.)" % num(s), r_, [r_ * r_, r_ * 2, r_ / 2],
              "4πr² = %s, so r² = %s and <b>r = %s cm</b>." % (num(s), num(r_ * r_), num(r_)), unit=" cm")


# ---------------------------------------------------------------- set 4: volume of a cone
def one_vcone(r):
    r_, h, l = r.choice(CONES)
    kind = r.choice(["v", "v", "vl", "litre", "back"])
    if kind == "v":
        v = F(1, 3) * PI * r_ * r_ * h
        return QN("Find the volume of a cone with radius %s cm and height %s cm. (Use π = 22/7.)" % (num(r_), num(h)), v, [PI * r_ * r_ * h, F(1, 3) * PI * r_ * r_ * l, F(1, 3) * PI * r_ * h],
                  "V = ⅓πr²h = ⅓ × 22/7 × %s² × %s = <b>%s cm³</b>." % (num(r_), num(h), num(v)), unit=" cm³")
    if kind == "vl":
        v = F(1, 3) * PI * r_ * r_ * h
        return QN("A cone has radius %s cm and slant height %s cm. Find its volume. (Use π = 22/7.)" % (num(r_), num(l)), v, [F(1, 3) * PI * r_ * r_ * l, PI * r_ * r_ * h, PI * r_ * l],
                  "First h = √(%s² − %s²) = %s cm. V = ⅓πr²h = <b>%s cm³</b>." % (num(l), num(r_), num(h), num(v)), unit=" cm³")
    if kind == "litre":
        rr, hh = r.choice([(F(7, 10), F(12, 5)), (F(7, 5), 3), (F(21, 10), F(5, 2)), (F(7, 10), 3)])
        v = F(1, 3) * PI * rr * rr * hh
        return QN("A conical vessel has radius %s m and height %s m. How many litres does it hold? (Use π = 22/7; 1 m³ = 1,000 litres.)" % (num(rr), num(hh)), v * 1000,
                  [v * 3000, v * 100, v], "V = ⅓πr²h = %s m³ = <b>%s litres</b>." % (num(v), num(v * 1000)), unit=" litres")
    v = F(1, 3) * PI * r_ * r_ * h
    return QN("The volume of a cone is %s cm³ and its radius is %s cm. Find its height. (Use π = 22/7.)" % (num(v), num(r_)), h, [h * 3, h / 3, l],
              "⅓πr²h = %s, so h = 3 × %s ÷ (22/7 × %s²) = <b>%s cm</b>." % (num(v), num(v), num(r_), num(h)), unit=" cm")


# ---------------------------------------------------------------- set 5: volume of spheres and problems
def one_vs(r):
    r_ = r.choice(RV)
    v = F(4, 3) * PI * r_ ** 3
    return QN("Find the volume of a sphere of radius %s cm. (Use π = 22/7.)" % num(r_), v, [4 * PI * r_ * r_, F(2, 3) * PI * r_ ** 3, PI * r_ ** 3],
              "V = 4/3 πr³ = 4/3 × 22/7 × %s³ = <b>%s cm³</b>." % (num(r_), num(v)), unit=" cm³")


def one_vh(r):
    r_ = r.choice(RV)
    v = F(2, 3) * PI * r_ ** 3
    return QN("Find the volume of a hemisphere of radius %s cm. (Use π = 22/7.)" % num(r_), v, [F(4, 3) * PI * r_ ** 3, 2 * PI * r_ * r_, F(1, 3) * PI * r_ ** 3],
              "V = ⅔πr³ = ⅔ × 22/7 × %s³ = <b>%s cm³</b>." % (num(r_), num(v)), unit=" cm³")


def one_bowl(r):
    rr, lit = r.choice([(F(21, 2), False), (21, False), (21, True), (F(63, 10), False)])
    v = F(2, 3) * PI * rr ** 3
    if lit:
        return QN("A hemispherical bowl has inner radius %s cm. How many litres of milk can it hold? (Use π = 22/7; 1,000 cm³ = 1 litre.)" % num(rr), v / 1000,
                  [v / 500, v / 100, 2 * PI * rr * rr / 1000], "V = ⅔πr³ = %s cm³ = <b>%s litres</b>." % (num(v), num(v / 1000)), unit=" litres")
    return QN("A hemispherical bowl has inner radius %s cm. How much milk, in cm³, can it hold? (Use π = 22/7.)" % num(rr), v,
              [2 * v, 2 * PI * rr * rr, F(1, 3) * PI * rr ** 3], "V = ⅔πr³ = <b>%s cm³</b>." % num(v), unit=" cm³")


def one_scale(r):
    k = r.choice([2, 3])
    if r.random() < 0.5:
        return T("The radius of a sphere is multiplied by %d. By what factor is its volume multiplied?" % k, str(k ** 3), [str(k), str(k * k), str(3 * k)],
                 "V = 4/3 πr³, and (%dr)³ = %d r³. The volume is multiplied by <b>%d</b>." % (k, k ** 3, k ** 3))
    return T("The radius of a sphere is multiplied by %d. By what factor is its surface area multiplied?" % k, str(k * k), [str(k), str(k ** 3), str(2 * k)],
             "S = 4πr², and (%dr)² = %d r². The surface area is multiplied by <b>%d</b>." % (k, k * k, k * k))


def one_dome(r):
    rr = r.choice([7, F(21, 2), 14, F(7, 2)])
    rate = r.choice([20, 40, 50, 100])
    a = 2 * PI * rr * rr
    return T("The inside of a hemispherical dome of radius %s m is to be whitewashed at %s per m². Find the cost. (Use π = 22/7.)" % (num(rr), inr(rate)), inr(a * rate),
             [inr(4 * PI * rr * rr * rate), inr(3 * PI * rr * rr * rate), inr(a)], "Area = 2πr² = %s m². Cost = %s × %d = <b>%s</b>." % (num(a), num(a), rate, inr(a * rate)))


def one_metal(r):
    rr = r.choice(RV[:4])
    d = r.choice([8, 9])
    v = F(4, 3) * PI * rr ** 3
    return QN("A metal ball has radius %s cm. Each cm³ of the metal has a mass of %d g. Find the mass of the ball. (Use π = 22/7.)" % (num(rr), d), v * d, [v, 4 * PI * rr * rr * d, F(2, 3) * PI * rr ** 3 * d],
              "V = 4/3 πr³ = %s cm³, so mass = %s × %d = <b>%s g</b>." % (num(v), num(v), d, num(v * d)), unit=" g")


def one_cone_sph(r):
    rr = r.choice([F(21, 10), F(21, 5), F(63, 10), F(21, 2)])
    k = r.choice([1, 2, 4])
    h = rr * k
    vc = F(1, 3) * PI * rr * rr * h
    vs = F(4, 3) * PI * rr ** 3
    if vs % vc:
        return None
    n = vs / vc
    return QN("A solid metal sphere of radius %s cm is melted and recast into cones of the same radius and height %s cm. How many cones are made?" % (num(rr), num(h)), n, [n * 3, 4, n + 1 if n + 1 != 4 else n + 2],
              "Sphere: 4/3 πr³. Cone: ⅓πr²h. Number = 4r³ ÷ (r²h) = 4r ÷ h = <b>%s</b>." % num(n))


def two(fn):
    import re

    def f(r):
        it = fn(r)
        if it and any(re.search(r"\.\d{3}", c) for c in it["c"]):
            return None
        return it
    f.__name__ = fn.__name__
    return f


def main():
    seen = set()
    sets = [
        S("Slant height and curved surface of a cone", mix(R, [(two(one_csa), 20)], seen)),
        S("Total surface area of a cone", mix(R, [(two(one_tsa), 20)], seen)),
        S("Surface area of spheres and hemispheres", mix(R, [(two(one_sph), 20)], seen)),
        S("Volume of a cone", mix(R, [(two(one_vcone), 20)], seen)),
        S("Volume of spheres and problems", mix(R, [(one_vs, 5), (one_vh, 4), (one_bowl, 3), (one_scale, 2), (one_dome, 3), (one_metal, 2), (one_cone_sph, 1)], seen)),
    ]
    body = lesson(
        "<p><b>Cone</b> (radius r, height h, slant height l = √(r² + h²)): curved surface πrl, total surface πr(l + r), volume ⅓πr²h.</p>"
        "<p><b>Sphere</b>: surface 4πr², volume 4/3 πr³. <b>Hemisphere</b>: curved surface 2πr², total surface 3πr², volume ⅔πr³.</p>"
        "<p>Use π = 22/7 when the radius is a multiple of 7. 1 m³ = 1,000 litres and 1,000 cm³ = 1 litre.</p>",
        [("A cone has r = 7 cm and h = 24 cm. Find its curved surface area.", ["l = √(49 + 576) = 25", "πrl = 22/7 × 7 × 25"], "550 cm²"),
         ("Find the volume of a sphere of radius 21 cm.", ["4/3 × 22/7 × 21³"], "38,808 cm³")],
        ["Using the height h in πrl. The curved surface uses the slant height l.",
         "Forgetting ⅓ in the volume of a cone.",
         "Using 4πr² for a hemisphere. Its curved surface is 2πr²; a solid hemisphere has 3πr² in all."])
    faq = [
        ("What is the curved surface area of a cone?", "πrl, where r is the base radius and l = √(r² + h²) is the slant height."),
        ("What is the volume of a cone?", "⅓πr²h, one third of a cylinder with the same base and height."),
        ("What is the surface area of a sphere?", "4πr². A hemisphere has curved surface 2πr² and, if solid, total surface 3πr²."),
        ("What is the volume of a sphere and a hemisphere?", "Sphere: 4/3 πr³. Hemisphere: ⅔πr³."),
    ]
    make(9, "surface-areas-and-volumes", 11, "VI", 11, "Surface Areas and Volumes: Cones and Spheres", "surface areas and volumes",
         "Surface areas and volumes of spheres (including hemispheres) and right circular cones (summary of the CBSE syllabus)",
         "Class 9 Surface Areas and Volumes worksheet (NCERT Chapter 11): slant height, curved and total surface area of cones, spheres and hemispheres, and their volumes. 100 questions with answers.",
         "Cone: πrl and ⅓πr²h; sphere: 4πr² and 4/3 πr³", "Hemisphere: 2πr² curved, 3πr² total, ⅔πr³ volume.",
         body, faq, sets, R)


if __name__ == "__main__":
    main()
