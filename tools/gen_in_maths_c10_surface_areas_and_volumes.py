# -*- coding: utf-8 -*-
"""
India Class 10 Maths, NCERT Chapter 12: Surface Areas and Volumes (CBSE Unit VI Mensuration)
  python3 tools/gen_in_maths_c10_surface_areas_and_volumes.py
Formulae for the cuboid, cube, cylinder, cone, sphere and hemisphere (π = 22/7), surface area of a combination of two solids
(toy, capsule, tent, cube with a hemisphere), volume of a combination, solids with a part removed, and problems in
litres and rupees.
Wrong answers come from real mistakes: adding total surface areas (counting the hidden circles), using the slant height
for the volume of a cone, 4πr² for a hemisphere's curved surface, forgetting ⅓ for a cone, and 1 m³ = 100 litres.
"""
import random, math
from fractions import Fraction as F
from in_common import num, S, make, lesson, mix, T, QN, inr, People

R = random.Random(910012)
P = People(R)
PI = F(22, 7)


def r7():
    return R.choice([F(7, 2), 7, 7, 14, F(21, 2), 21])


def ok2(v):
    return (F(v) * 100).denominator == 1


# ---------------------------------------------------------------- set 1: single solids
def one_single(r):
    kind = r.choice(["cylV", "cylC", "coneV", "coneC", "sphV", "sphS", "hemC", "hemT"])
    rad = r.choice([F(7, 2), 7, 14, 21, F(21, 2)])
    h = r.choice([5, 6, 10, 12, 14, 20, 24])
    if kind == "cylV":
        v = PI * rad * rad * h
        return QN("Find the volume of a cylinder of radius %s cm and height %d cm. (Use π = 22/7.)" % (num(rad), h), v, [2 * PI * rad * h, PI * rad * h, F(1, 3) * PI * rad * rad * h],
                  "V = πr²h = 22/7 × %s² × %d = <b>%s cm³</b>." % (num(rad), h, num(v)), unit=" cm³")
    if kind == "cylC":
        v = 2 * PI * rad * h
        return QN("Find the curved surface area of a cylinder of radius %s cm and height %d cm. (Use π = 22/7.)" % (num(rad), h), v, [PI * rad * rad * h, 2 * PI * rad * (rad + h), PI * rad * h],
                  "CSA = 2πrh = 2 × 22/7 × %s × %d = <b>%s cm²</b>." % (num(rad), h, num(v)), unit=" cm²")
    if kind in ("coneV", "coneC"):
        rr, hh, l = r.choice([(7, 24, 25), (21, 20, 29), (14, 48, 50), (F(7, 2), 12, F(25, 2)), (21, 72, 75)])
        if kind == "coneV":
            v = F(1, 3) * PI * rr * rr * hh
            return QN("Find the volume of a cone of radius %s cm and height %s cm. (Use π = 22/7.)" % (num(rr), num(hh)), v, [PI * rr * rr * hh, F(1, 3) * PI * rr * rr * l, PI * rr * l],
                      "V = ⅓πr²h = ⅓ × 22/7 × %s² × %s = <b>%s cm³</b>." % (num(rr), num(hh), num(v)), unit=" cm³")
        v = PI * rr * l
        return QN("A cone has radius %s cm and height %s cm. Find its curved surface area. (Use π = 22/7.)" % (num(rr), num(hh)), v, [PI * rr * hh, PI * rr * (l + rr), F(1, 3) * PI * rr * rr * hh],
                  "Slant height l = √(%s² + %s²) = %s cm. CSA = πrl = <b>%s cm²</b>." % (num(rr), num(hh), num(l), num(v)), unit=" cm²")
    if kind == "sphV":
        v = F(4, 3) * PI * rad ** 3
        return QN("Find the volume of a sphere of radius %s cm. (Use π = 22/7.)" % num(rad), v, [4 * PI * rad * rad, F(2, 3) * PI * rad ** 3, PI * rad ** 3],
                  "V = 4/3 πr³ = <b>%s cm³</b>." % num(v), unit=" cm³")
    if kind == "sphS":
        v = 4 * PI * rad * rad
        return QN("Find the surface area of a sphere of radius %s cm. (Use π = 22/7.)" % num(rad), v, [F(4, 3) * PI * rad ** 3, 2 * PI * rad * rad, PI * rad * rad],
                  "S = 4πr² = 4 × 22/7 × %s² = <b>%s cm²</b>." % (num(rad), num(v)), unit=" cm²")
    if kind == "hemC":
        v = 2 * PI * rad * rad
        return QN("Find the curved surface area of a hemisphere of radius %s cm. (Use π = 22/7.)" % num(rad), v, [4 * PI * rad * rad, 3 * PI * rad * rad, F(2, 3) * PI * rad ** 3],
                  "CSA = 2πr² = <b>%s cm²</b>." % num(v), unit=" cm²")
    v = 3 * PI * rad * rad
    return QN("Find the total surface area of a solid hemisphere of radius %s cm. (Use π = 22/7.)" % num(rad), v, [2 * PI * rad * rad, 4 * PI * rad * rad, F(2, 3) * PI * rad ** 3],
              "TSA = curved 2πr² + flat πr² = 3πr² = <b>%s cm²</b>." % num(v), unit=" cm²")


# ---------------------------------------------------------------- set 2: surface area of combinations
def one_sa(r):
    kind = r.choice(["toy", "capsule", "tent", "cubehem", "cylhem"])
    if kind == "toy":
        rr, hh, l = r.choice([(F(7, 2), 12, F(25, 2)), (7, 24, 25), (21, 20, 29), (F(21, 2), 36, F(75, 2))])
        v = PI * rr * l + 2 * PI * rr * rr
        return QN("A toy is a cone of radius %s cm and height %s cm mounted on a hemisphere of the same radius. Find its total surface area. (Use π = 22/7.)" % (num(rr), num(hh)), v,
                  [PI * rr * l + 3 * PI * rr * rr, PI * rr * hh + 2 * PI * rr * rr, PI * rr * l + 4 * PI * rr * rr],
                  "Slant height = %s cm. TSA = CSA of cone + CSA of hemisphere = πrl + 2πr² = <b>%s cm²</b>. The joined circular faces are hidden." % (num(l), num(v)), unit=" cm²")
    if kind == "capsule":
        rad = r.choice([F(7, 2), 7, F(7, 4)])
        L = r.choice([10, 14, 20, 21])
        h = L - 2 * rad
        if h <= 0:
            return None
        v = 2 * PI * rad * h + 4 * PI * rad * rad
        return QN("A capsule is a cylinder with a hemisphere at each end. The whole capsule is %s mm long and its radius is %s mm. Find its surface area. (Use π = 22/7.)" % (num(L), num(rad)), v,
                  [2 * PI * rad * L + 4 * PI * rad * rad, 2 * PI * rad * h + 2 * PI * rad * rad, 2 * PI * rad * h + 4 * PI * rad * rad + 2 * PI * rad * rad],
                  "Cylinder length = %s − 2 × %s = %s mm. Area = 2πrh + 2 × 2πr² = <b>%s mm²</b>." % (num(L), num(rad), num(h), num(v)), unit=" mm²")
    if kind == "tent":
        rr, hh, l = r.choice([(21, 20, 29), (F(21, 2), 10, F(29, 2)), (14, F(21, 2), F(35, 2)), (7, F(21, 4), F(35, 4))])
        hc = r.choice([3, 4, 5, 6])
        v = 2 * PI * rr * hc + PI * rr * l
        return QN("A tent is a cylinder of height %d m and radius %s m with a cone of slant height %s m on top. Find the area of canvas used (no floor). (Use π = 22/7.)" % (hc, num(rr), num(l)), v,
                  [2 * PI * rr * hc + PI * rr * l + 2 * PI * rr * rr, PI * rr * rr * hc + PI * rr * l, 2 * PI * rr * hc + PI * rr * hh],
                  "Canvas = 2πrh + πrl = 2 × 22/7 × %s × %d + 22/7 × %s × %s = <b>%s m²</b>." % (num(rr), hc, num(rr), num(l), num(v)), unit=" m²")
    if kind == "cubehem":
        a = r.choice([7, 14, 21])
        d = r.choice([a, F(a, 2)])
        rad = F(d, 2)
        v = 6 * a * a + PI * rad * rad
        return QN("A hemisphere of diameter %s cm is placed on top of a cube of edge %d cm. Find the total surface area of the solid. (Use π = 22/7.)" % (num(d), a), v,
                  [6 * a * a + 2 * PI * rad * rad, 6 * a * a + 3 * PI * rad * rad, 6 * a * a], "TSA = 6a² − πr² + 2πr² = 6a² + πr² = %s + %s = <b>%s cm²</b>." % (num(6 * a * a), num(PI * rad * rad), num(v)), unit=" cm²")
    rad = r.choice([7, 14, F(7, 2)])
    h = r.choice([10, 13, 20, 25])
    v = 2 * PI * rad * h + 2 * PI * rad * rad + PI * rad * rad
    return QN("A solid is a cylinder of radius %s cm and height %d cm with a hemisphere of the same radius on top. Find its total surface area. (Use π = 22/7.)" % (num(rad), h), v,
              [2 * PI * rad * h + 2 * PI * rad * rad, 2 * PI * rad * h + 2 * PI * rad * rad + 2 * PI * rad * rad, 2 * PI * rad * (rad + h) + 3 * PI * rad * rad],
              "TSA = base πr² + cylinder 2πrh + hemisphere 2πr² = <b>%s cm²</b>." % num(v), unit=" cm²")


# ---------------------------------------------------------------- set 3: volume of combinations
def one_vol(r):
    kind = r.choice(["conehem", "cylhem", "cylcone", "capsule", "cubhem"])
    if kind == "conehem":
        rad = r.choice([F(7, 2), 7, F(21, 2)])
        h = r.choice([6, 12, 14, 21])
        v = F(1, 3) * PI * rad * rad * h + F(2, 3) * PI * rad ** 3
        return QN("A solid is a cone of height %d cm on a hemisphere, both of radius %s cm. Find its volume. (Use π = 22/7.)" % (h, num(rad)), v,
                  [F(1, 3) * PI * rad * rad * h + F(4, 3) * PI * rad ** 3, PI * rad * rad * h + F(2, 3) * PI * rad ** 3, F(1, 3) * PI * rad * rad * (h + rad)],
                  "V = ⅓πr²h + ⅔πr³ = <b>%s cm³</b>." % num(v), unit=" cm³")
    if kind == "cylhem":
        rad = r.choice([7, F(7, 2), 14])
        h = r.choice([6, 10, 12, 20])
        v = PI * rad * rad * h + F(2, 3) * PI * rad ** 3
        return QN("A vessel is a hollow hemisphere of radius %s cm topped by a cylinder of the same radius and height %d cm. How much can it hold? (Use π = 22/7.)" % (num(rad), h), v,
                  [PI * rad * rad * h + F(4, 3) * PI * rad ** 3, PI * rad * rad * (h + rad), 2 * PI * rad * h + 2 * PI * rad * rad],
                  "V = πr²h + ⅔πr³ = <b>%s cm³</b>." % num(v), unit=" cm³")
    if kind == "cylcone":
        rad = r.choice([7, 14, 21, F(7, 2)])
        h1, h2 = r.choice([10, 12, 15, 20]), r.choice([6, 9, 12, 15])
        v = PI * rad * rad * h1 + F(1, 3) * PI * rad * rad * h2
        return QN("A solid is a cylinder of radius %s cm and height %d cm with a cone of the same radius and height %d cm on top. Find its volume. (Use π = 22/7.)" % (num(rad), h1, h2), v,
                  [PI * rad * rad * (h1 + h2), PI * rad * rad * h1 + PI * rad * rad * h2 / 2, F(1, 3) * PI * rad * rad * (h1 + h2)],
                  "V = πr²h₁ + ⅓πr²h₂ = <b>%s cm³</b>." % num(v), unit=" cm³")
    if kind == "capsule":
        rad = r.choice([F(7, 2), 7])
        h = r.choice([6, 10, 14])
        v = PI * rad * rad * h + F(4, 3) * PI * rad ** 3
        return QN("A solid is a cylinder of radius %s cm and length %d cm with a hemisphere at each end. Find its volume. (Use π = 22/7.)" % (num(rad), h), v,
                  [PI * rad * rad * h + F(2, 3) * PI * rad ** 3, PI * rad * rad * (h + 2 * rad), 2 * PI * rad * h + 4 * PI * rad * rad],
                  "Two hemispheres make one sphere: V = πr²h + 4/3 πr³ = <b>%s cm³</b>." % num(v), unit=" cm³")
    a = r.choice([7, 14, 21])
    rad = F(a, 2)
    v = a ** 3 + F(2, 3) * PI * rad ** 3
    return QN("A hemisphere of diameter %d cm sits on a cube of edge %d cm. Find the volume of the solid. (Use π = 22/7.)" % (a, a), v,
              [a ** 3 + F(4, 3) * PI * rad ** 3, a ** 3 + F(2, 3) * PI * a ** 3, 6 * a * a + 2 * PI * rad * rad],
              "V = a³ + ⅔πr³ with r = %s: <b>%s cm³</b>." % (num(rad), num(v)), unit=" cm³")


# ---------------------------------------------------------------- set 4: a part removed
def one_rem(r):
    kind = r.choice(["scoop", "conecut", "penstand", "hemcut", "drill", "drill"])
    if kind == "drill":
        L, B, H = r.choice([10, 12, 14, 15, 20]), r.choice([8, 10, 14]), r.choice([5, 7, 10, 14])
        rad = r.choice([F(7, 10), F(7, 5), F(7, 2), 2, 3])
        if 2 * rad >= min(L, B):
            return None
        v = L * B * H - PI * rad * rad * H
        return QN("A cylindrical hole of radius %s cm is drilled right through a cuboid %d cm × %d cm × %d cm, along the %d cm edge. Find the volume of what remains. (Use π = 22/7.)" % (num(rad), L, B, H, H), v,
                  [L * B * H - 2 * PI * rad * H, L * B * H + PI * rad * rad * H, L * B * H - PI * rad * rad * L],
                  "Remaining = cuboid − cylinder = %s − 22/7 × %s² × %d = <b>%s cm³</b>." % (num(L * B * H), num(rad), H, num(v)), unit=" cm³")
    if kind == "scoop":
        rad = r.choice([F(7, 2), 7, F(7, 4), F(7, 10), F(21, 10)])
        h = r.choice([10, 12, 14, 15, 20, 25])
        if 2 * rad >= h:
            return None
        v = PI * rad * rad * h - F(4, 3) * PI * rad ** 3
        return QN("From a solid cylinder of radius %s cm and height %d cm, a hemisphere of the same radius is scooped out at each end. Find the remaining volume. (Use π = 22/7.)" % (num(rad), h), v,
                  [PI * rad * rad * h - F(2, 3) * PI * rad ** 3, PI * rad * rad * h + F(4, 3) * PI * rad ** 3, PI * rad * rad * h],
                  "Remaining = πr²h − 2 × ⅔πr³ = <b>%s cm³</b>." % num(v), unit=" cm³")
    if kind == "conecut":
        rr, hh, l = r.choice([(7, 24, 25), (21, 20, 29), (F(7, 2), 12, F(25, 2)), (14, 48, 50), (21, 72, 75), (F(21, 2), 36, F(75, 2))])
        v = PI * rr * rr * hh - F(1, 3) * PI * rr * rr * hh
        return QN("A cone of the same radius and height is cut out of a solid cylinder of radius %s cm and height %s cm. Find the remaining volume. (Use π = 22/7.)" % (num(rr), num(hh)), v,
                  [F(1, 3) * PI * rr * rr * hh, PI * rr * rr * hh - PI * rr * l, PI * rr * rr * hh],
                  "Remaining = πr²h − ⅓πr²h = ⅔πr²h = <b>%s cm³</b>." % num(v), unit=" cm³")
    if kind == "penstand":
        L, B, H = r.choice([(15, 10, F(7, 2)), (20, 12, 5), (14, 10, 4)])
        rad = F(1, 2)
        n = 4
        d = F(7, 5)
        v = L * B * H - n * F(1, 3) * PI * rad * rad * d
        return QN("A wooden pen stand is a cuboid %d cm × %d cm × %s cm with four conical depressions, each of radius 0.5 cm and depth 1.4 cm. Find the volume of wood. (Use π = 22/7.)" % (L, B, num(H)), v,
                  [L * B * H - n * PI * rad * rad * d, L * B * H, L * B * H - F(1, 3) * PI * rad * rad * d],
                  "Wood = cuboid − 4 cones = %s − 4 × ⅓ × 22/7 × 0.25 × 1.4 = <b>%s cm³</b>." % (num(L * B * H), num(v)), unit=" cm³")
    a = r.choice([7, 14, 21, 28, 35])
    rad = F(a, 2) if r.random() < 0.5 else F(a, 4)
    v = 6 * a * a - PI * rad * rad + 2 * PI * rad * rad
    return QN("A hemispherical depression of diameter %s cm is cut out from one face of a cube of edge %d cm. Find the surface area of the remaining solid. (Use π = 22/7.)" % (num(2 * rad), a), v,
              [6 * a * a - PI * rad * rad, 6 * a * a + PI * rad * rad + 2 * PI * rad * rad, 6 * a * a],
              "Remove the circle πr², add the inside of the hemisphere 2πr²: 6a² + πr² = <b>%s cm²</b>." % num(v), unit=" cm²")


# ---------------------------------------------------------------- set 5: problems in litres and rupees
def one_prob(r):
    kind = r.choice(["tank", "paint", "jamun", "canvas", "bird"])
    name, he, his = P.next()
    if kind == "tank":
        rad = r.choice([F(7, 10), F(7, 5), F(21, 10)])
        h = r.choice([2, 3, 4, 5])
        v = PI * rad * rad * h
        lit = v * 1000
        return QN("A cylindrical water tank has a radius of %s m and a height of %d m. How many litres of water can it hold? (Use π = 22/7; 1 m³ = 1,000 litres.)" % (num(rad), h), lit,
                  [v * 100, v, 2 * PI * rad * h * 1000], "V = πr²h = %s m³ = <b>%s litres</b>." % (num(v), num(lit)), unit=" litres")
    if kind == "paint":
        rad = r.choice([F(7, 20), F(7, 10), F(21, 50)])
        h = r.choice([1, F(7, 5), F(6, 5)])
        rate = r.choice([50, 100, 150, 200])
        area = 2 * PI * rad * rad + 2 * PI * rad * h
        return T("A bird bath is a cylinder of radius %s m and height %s m with a hemispherical bowl at the top (open, same radius). Find the cost of painting its outer curved surface and the bowl at %s per m². (Use π = 22/7.)" % (num(rad), num(h), inr(rate)),
                 inr(area * rate), [inr((area + PI * rad * rad) * rate), inr(2 * PI * rad * h * rate), inr(area * rate / 2)],
                 "Area = 2πrh + 2πr² = %s m². Cost = %s × %s = <b>%s</b>." % (num(area), num(area), num(rate), inr(area * rate)))
    if kind == "jamun":
        n = r.choice([30, 45, 60])
        L = 5
        d = F(14, 5)
        rad = d / 2
        v = PI * rad * rad * (L - d) + F(4, 3) * PI * rad ** 3
        syrup = v * F(3, 10) * n
        if not ok2(syrup):
            return None
        return QN("A gulab jamun is a cylinder with two hemispherical ends, 5 cm long with diameter 2.8 cm. It contains sugar syrup up to 30%% of its volume. How much syrup is in %d gulab jamuns? (Use π = 22/7.)" % n, syrup,
                  [v * n, v * F(3, 10), PI * rad * rad * L * F(3, 10) * n],
                  "One jamun: πr²h + 4/3 πr³ = %s cm³ with h = 5 − 2.8 = 2.2 cm. Syrup = 30%% × %s × %d = <b>%s cm³</b>." % (num(v), num(v), n, num(syrup)), unit=" cm³")
    if kind == "canvas":
        rr, hh, l = r.choice([(21, 20, 29), (F(21, 2), 10, F(29, 2)), (14, F(21, 2), F(35, 2))])
        hc = r.choice([2, 3, 4])
        rate = r.choice([100, 200, 500])
        area = 2 * PI * rr * hc + PI * rr * l
        return T("A tent is a cylinder (radius %s m, height %d m) with a cone of slant height %s m on top. Canvas costs %s per m². Find the cost of the canvas. (Use π = 22/7.)" % (num(rr), hc, num(l), inr(rate)),
                 inr(area * rate), [inr((area + PI * rr * rr) * rate), inr(PI * rr * l * rate), inr(2 * PI * rr * hc * rate)],
                 "Canvas = 2πrh + πrl = %s m². Cost = <b>%s</b>." % (num(area), inr(area * rate)))
    rad = r.choice([F(7, 2), 7])
    h = r.choice([6, 9, 12])
    v = F(1, 3) * PI * rad * rad * h + F(2, 3) * PI * rad ** 3
    return QN("An ice-cream cone is a cone of radius %s cm and height %d cm filled with ice cream and topped with a hemisphere of ice cream of the same radius. Find the volume of ice cream. (Use π = 22/7.)" % (num(rad), h), v,
              [F(1, 3) * PI * rad * rad * h + F(4, 3) * PI * rad ** 3, F(1, 3) * PI * rad * rad * h, PI * rad * rad * h + F(2, 3) * PI * rad ** 3],
              "V = ⅓πr²h + ⅔πr³ = <b>%s cm³</b>." % num(v), unit=" cm³")


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
    global one_single, one_sa, one_vol, one_rem, one_prob
    one_single, one_sa, one_vol, one_rem, one_prob = two(one_single), two(one_sa), two(one_vol), two(one_rem), two(one_prob)
    sets = [
        S("Formulae for single solids", mix(R, [(one_single, 20)], seen)),
        S("Surface area of combined solids", mix(R, [(one_sa, 20)], seen)),
        S("Volume of combined solids", mix(R, [(one_vol, 20)], seen)),
        S("Solids with a part removed", mix(R, [(one_rem, 20)], seen)),
        S("Problems in litres and rupees", mix(R, [(one_prob, 20)], seen)),
    ]
    body = lesson(
        "<p>Cylinder: CSA 2πrh, V πr²h. Cone: CSA πrl (l = √(r² + h²)), V ⅓πr²h. Sphere: S 4πr², V 4/3 πr³. Hemisphere: CSA 2πr², TSA 3πr², V ⅔πr³.</p>"
        "<p><b>Surface area of a combination</b>: add only the surfaces you can see. The faces where the solids are joined are hidden.</p>"
        "<p><b>Volume of a combination</b>: add the volumes (or subtract the part that is removed).</p>",
        [("A toy is a cone (r = 3.5 cm, h = 12 cm) on a hemisphere. Find its surface area.", ["l = √(3.5² + 12²) = 12.5", "πrl + 2πr² = 137.5 + 77"], "214.5 cm²"),
         ("A cylinder (r = 7 cm, h = 10 cm) has a cone (h = 6 cm) on top. Find its volume.", ["πr²h = 1,540", "⅓πr²h = 308"], "1,848 cm³")],
        ["Adding the total surface areas of both solids. The joined circles are not on the outside.",
         "Using the slant height l in the volume of a cone. Volume uses the vertical height h.",
         "Using 1 m³ = 100 litres. 1 m³ = 1,000 litres."])
    faq = [
        ("How do I find the surface area of a combination of solids?", "Add the curved or flat surfaces that are visible. Do not include the faces where the two solids are joined."),
        ("How do I find the volume of a combination of solids?", "Add the volumes of the parts. If a part is removed, subtract its volume."),
        ("What is the total surface area of a solid hemisphere?", "3πr²: the curved surface 2πr² plus the flat circle πr²."),
        ("Why is π taken as 22/7?", "NCERT problems often use radii that are multiples of 7, so 22/7 gives exact answers. Use 3.14 when the question says so."),
    ]
    make(10, "surface-areas-and-volumes", 12, "VI", 12, "Surface Areas and Volumes: Combined Solids", "surface areas and volumes",
         "Surface areas and volumes of combinations of any two of the following: cubes, cuboids, spheres, hemispheres and right circular cylinders/cones (summary of the CBSE syllabus)",
         "Class 10 Surface Areas and Volumes worksheet (NCERT Chapter 12): formulae, surface area and volume of combined solids, solids with parts removed, problems in litres and rupees. 100 questions with answers.",
         "Combined solid: add only the visible surfaces", "Volumes simply add up (or subtract what is removed).",
         body, faq, sets, R)


if __name__ == "__main__":
    main()
