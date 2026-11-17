# -*- coding: utf-8 -*-
"""
US Geometry: Volume of Cylinders, Pyramids, Cones, and Spheres (Common Core G-GMD.A.3, G-GMD.A.1, G-MG.A.2)
  python3 tools/gen_us_math_ge_volume_of_solids.py
Cylinders, cones and spheres (ported from the UK Year 9 generator) and a US problem set with pyramids,
Cavalieri's principle, composite solids and density.
Wrong answers come from real mistakes: using the diameter as the radius, forgetting the 1/3 for a cone or a
pyramid, using surface area instead of volume, and using r² instead of r³ for a sphere.
"""
import math
import random
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F
from us_hs import num, B, S, make, lesson, collect, T, svg_wrap, line, text, fig, INK, RED, BLUE

R = random.Random(94101)
PI = "π"
FILL = "#e8f1fb"


def d1(x):
    d = Decimal(repr(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    return "{:,.1f}".format(d)


def coef(c):
    c = F(c)
    if c.denominator == 1:
        return num(c)
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%d</span></span>" % (num(c.numerator), c.denominator)


def cm3(x, u="cm"):
    return "%s %s³" % (d1(x), u)


def pi_form(c, u="cm"):
    c = F(c)
    return "%s%s %s³" % (coef(c) if c != 1 else "", PI, u)


def dash():
    return " stroke-dasharray='5 4'"


def cyl_svg(rlab, hlab, use_d=False):
    cx, rx, ry, top, h = 110, 62, 16, 52, 120
    bot = top + h
    s = ["<path d='M%d %d L%d %d A%d %d 0 0 0 %d %d L%d %d Z' fill='%s' stroke='none'/>" % (cx - rx, top, cx - rx, bot, rx, ry, cx + rx, bot, cx + rx, top, FILL),
         "<ellipse cx='%d' cy='%d' rx='%d' ry='%d' fill='#f5f9fe' stroke='%s' stroke-width='2'/>" % (cx, top, rx, ry, INK),
         line(cx - rx, top, cx - rx, bot), line(cx + rx, top, cx + rx, bot),
         "<path d='M%d %d A%d %d 0 0 0 %d %d' fill='none' stroke='%s' stroke-width='2'/>" % (cx - rx, bot, rx, ry, cx + rx, bot, INK),
         "<path d='M%d %d A%d %d 0 0 1 %d %d' fill='none' stroke='%s' stroke-width='1.5'%s/>" % (cx - rx, bot, rx, ry, cx + rx, bot, INK, dash())]
    if use_d:
        s.append(line(cx - rx, top, cx + rx, top, RED, 2.5))
        s.append(text(cx, top - ry - 6, rlab, 15, col=RED))
    else:
        s.append(line(cx, top, cx + rx, top, RED, 2.5))
        s.append("<circle cx='%d' cy='%d' r='3' fill='%s'/>" % (cx, top, RED))
        s.append(text(cx + rx / 2, top - ry - 6, rlab, 15, col=RED))
    s.append(line(cx + rx + 14, top, cx + rx + 14, bot, BLUE, 2))
    s.append(text(cx + rx + 20, (top + bot) / 2 + 5, hlab, 15, col=BLUE, anchor="start"))
    return svg_wrap(270, bot + 26, "".join(s), "cylinder")


def cone_svg(rlab, hlab, use_d=False):
    cx, rx, ry, ap, by = 110, 64, 16, 18, 160
    s = ["<path d='M%d %d L%d %d A%d %d 0 0 0 %d %d Z' fill='%s' stroke='none'/>" % (cx, ap, cx - rx, by, rx, ry, cx + rx, by, FILL),
         line(cx, ap, cx - rx, by), line(cx, ap, cx + rx, by),
         "<path d='M%d %d A%d %d 0 0 0 %d %d' fill='none' stroke='%s' stroke-width='2'/>" % (cx - rx, by, rx, ry, cx + rx, by, INK),
         "<path d='M%d %d A%d %d 0 0 1 %d %d' fill='none' stroke='%s' stroke-width='1.5'%s/>" % (cx - rx, by, rx, ry, cx + rx, by, INK, dash()),
         line(cx, ap, cx, by, BLUE, 2, dash()),
         "<path d='M%d %d l10 0 l0 -10' fill='none' stroke='%s' stroke-width='1.5'/>" % (cx, by - 10, BLUE) if False else
         "<path d='M%d %d l0 -10 l10 0' fill='none' stroke='%s' stroke-width='1.5'/>" % (cx, by - 10 + 10, BLUE),
         line(cx + rx + 16, ap, cx + rx + 16, by, BLUE, 2), line(cx + 4, ap, cx + rx + 20, ap, BLUE, 1, dash()),
         text(cx + rx + 22, (ap + by) / 2 + 5, hlab, 15, col=BLUE, anchor="start")]
    if use_d:
        s.append(line(cx - rx, by, cx + rx, by, RED, 2.5))
        s.append(text(cx + rx / 2, by + ry + 18, rlab, 15, col=RED))
    else:
        s.append(line(cx, by, cx + rx, by, RED, 2.5))
        s.append(text(cx + rx / 2, by + ry + 18, rlab, 15, col=RED))
    return svg_wrap(270, by + ry + 28, "".join(s), "cone")


def sphere_svg(rlab, use_d=False, hemi=False):
    cx, cy, rr = 110, 100, 72
    s = []
    if hemi:
        cy = 40
        s.append("<path d='M%d %d A%d %d 0 0 0 %d %d Z' fill='%s' stroke='%s' stroke-width='2'/>" % (cx - rr, cy, rr, rr, cx + rr, cy, FILL, INK))
        s.append("<ellipse cx='%d' cy='%d' rx='%d' ry='%d' fill='#f5f9fe' stroke='%s' stroke-width='2'/>" % (cx, cy, rr, 16, INK))
        H = cy + rr + 28
    else:
        s.append("<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, rr, FILL, INK))
        s.append("<path d='M%d %d A%d %d 0 0 0 %d %d' fill='none' stroke='%s' stroke-width='1.5'/>" % (cx - rr, cy, rr, 18, cx + rr, cy, INK))
        s.append("<path d='M%d %d A%d %d 0 0 1 %d %d' fill='none' stroke='%s' stroke-width='1.2'%s/>" % (cx - rr, cy, rr, 18, cx + rr, cy, INK, dash()))
        H = cy + rr + 14
    if use_d:
        s.append(line(cx - rr, cy, cx + rr, cy, RED, 2.5))
        s.append(text(cx, cy - 24, rlab, 15, col=RED))
    else:
        s.append(line(cx, cy, cx + rr, cy, RED, 2.5))
        s.append("<circle cx='%d' cy='%d' r='3' fill='%s'/>" % (cx, cy, RED))
        s.append(text(cx + rr / 2, cy + (22 if hemi else -24), rlab, 15, col=RED))
    return svg_wrap(220, H, "".join(s), "hemisphere" if hemi else "sphere")


def pick_wr(right, cands):
    out = []
    for c in cands:
        if c != right and c not in out:
            out.append(c)
    return out[:3]


# ------------------------------------------------------------ set 1: cylinders
def one_cyl(r):
    rad, h = r.randint(2, 12), r.randint(3, 25)
    use_d = r.random() < 0.3
    lab = ("%d cm" % (2 * rad)) if use_d else ("%d cm" % rad)
    V = math.pi * rad * rad * h
    q = fig(cyl_svg(lab, "%d cm" % h, use_d)) + "Find the volume of the cylinder. Give your answer to 1 decimal place."
    right = cm3(V)
    wr = [cm3(math.pi * (2 * rad) ** 2 * h), cm3(2 * math.pi * rad * h), cm3(V / 3), cm3(math.pi * rad * h)]
    if use_d:
        wr = [cm3(math.pi * (2 * rad) ** 2 * h)] + wr
        e = "The diameter is %d cm, so <i>r</i> = %d cm. " % (2 * rad, rad)
    else:
        e = ""
    e += "<i>V</i> = π<i>r</i>²<i>h</i> = π × %d² × %d = %s%s = <b>%s</b>." % (rad, h, num(rad * rad * h), PI, right)
    return T(q, right, pick_wr(right, wr), e)


# ------------------------------------------------------------ set 2: cones
def one_cone(r):
    rad, h = r.randint(2, 12), r.randint(4, 24)
    use_d = r.random() < 0.25
    lab = ("%d cm" % (2 * rad)) if use_d else ("%d cm" % rad)
    V = math.pi * rad * rad * h / 3
    q = fig(cone_svg(lab, "%d cm" % h, use_d)) + "Find the volume of the cone. Give your answer to 1 decimal place."
    right = cm3(V)
    wr = [cm3(3 * V), cm3(math.pi * (2 * rad) ** 2 * h / 3), cm3(math.pi * rad * h / 3), cm3(V / 2)]
    e = ("The diameter is %d cm, so <i>r</i> = %d cm. " % (2 * rad, rad)) if use_d else ""
    e += "<i>V</i> = ⅓π<i>r</i>²<i>h</i> = ⅓ × π × %d² × %d = %s%s = <b>%s</b>." % (rad, h, coef(F(rad * rad * h, 3)), PI, right)
    return T(q, right, pick_wr(right, wr), e)


# ------------------------------------------------------------ set 3: spheres and hemispheres
def one_sph(r):
    rad = r.randint(2, 15)
    hemi = r.random() < 0.3
    use_d = (not hemi) and r.random() < 0.25
    lab = ("%d cm" % (2 * rad)) if use_d else ("%d cm" % rad)
    V = 4 * math.pi * rad ** 3 / 3 / (2 if hemi else 1)
    q = fig(sphere_svg(lab, use_d, hemi)) + "Find the volume of the %s. Give your answer to 1 decimal place." % ("hemisphere" if hemi else "sphere")
    right = cm3(V)
    wr = [cm3(4 * math.pi * rad ** 2 / (2 if hemi else 1)), cm3(4 * math.pi * rad ** 3 / 3 / (1 if hemi else 2)) if hemi else cm3(4 * math.pi * (2 * rad) ** 3 / 3),
          cm3(4 * math.pi * rad ** 2 / 3 / (2 if hemi else 1)), cm3(math.pi * rad ** 3)]
    e = ("The diameter is %d cm, so <i>r</i> = %d cm. " % (2 * rad, rad)) if use_d else ""
    c = F(4 * rad ** 3, 3) / (2 if hemi else 1)
    e += "<i>V</i> = %s × ⁴⁄₃ × π × %d³ = %s%s = <b>%s</b>." % ("½" if hemi else "1", rad, coef(c), PI, right) if hemi else \
        "<i>V</i> = ⁴⁄₃π<i>r</i>³ = ⁴⁄₃ × π × %d³ = %s%s = <b>%s</b>." % (rad, coef(c), PI, right)
    return T(q, right, pick_wr(right, wr), e)


# ------------------------------------------------------------ set 4: in terms of π
def one_pi(r):
    k = r.randint(0, 3)
    if k == 0:
        rad, h = r.randint(2, 10), r.randint(2, 12)
        q = "A cylinder has radius %d cm and height %d cm. Find its volume in terms of %s." % (rad, h, PI)
        right = pi_form(rad * rad * h)
        wr = [pi_form(2 * rad * h), pi_form(rad * h), pi_form(F(rad * rad * h, 3))]
        e = "π × %d² × %d = <b>%s</b>." % (rad, h, right)
    elif k == 1:
        rad, h = r.randint(2, 10), 3 * r.randint(1, 6)
        q = "A cone has radius %d cm and height %d cm. Find its volume in terms of %s." % (rad, h, PI)
        right = pi_form(F(rad * rad * h, 3))
        wr = [pi_form(rad * rad * h), pi_form(F(rad * h, 3)), pi_form(F(rad * rad * h, 2))]
        e = "⅓ × π × %d² × %d = <b>%s</b>." % (rad, h, right)
    elif k == 2:
        rad = 3 * r.randint(1, 4)
        q = "A sphere has radius %d cm. Find its volume in terms of %s." % (rad, PI)
        right = pi_form(F(4 * rad ** 3, 3))
        wr = [pi_form(4 * rad ** 2), pi_form(F(4 * rad ** 2, 3)), pi_form(rad ** 3)]
        e = "⁴⁄₃ × π × %d³ = ⁴⁄₃ × %s %s = <b>%s</b>." % (rad, num(rad ** 3), PI, right)
    else:
        rad = 3 * r.randint(1, 4)
        q = "A hemisphere has radius %d cm. Find its volume in terms of %s." % (rad, PI)
        right = pi_form(F(2 * rad ** 3, 3))
        wr = [pi_form(F(4 * rad ** 3, 3)), pi_form(2 * rad ** 2), pi_form(F(rad ** 3, 2))]
        e = "Half of ⁴⁄₃π<i>r</i>³ is ⅔π<i>r</i>³: ⅔ × π × %d³ = <b>%s</b>." % (rad, right)
    return T(q, right, pick_wr(right, wr), e)


# ------------------------------------------------------------ set 5: pyramids, composite solids and density
def one_prob(r):
    from us_hs import People
    nm, he, his = People(r).next()
    kind = r.choice(["pyr", "pyr", "cav", "comp", "dens", "dens", "ratio", "solve"])
    if kind == "pyr":
        s_, h = r.randint(3, 15), 3 * r.randint(1, 8)
        q = "A square pyramid has a base %d in. on each side and a height of %d in. Find its volume." % (s_, h)
        V = s_ * s_ * h // 3
        return T(q, "%s in.³" % num(V), ["%s in.³" % num(w) for w in dict.fromkeys([s_ * s_ * h, s_ * h // 3 if (s_ * h) % 3 == 0 else s_ * h, s_ * s_ * h // 2 if (s_ * s_ * h) % 2 == 0 else V + 12]) if w != V][:3],
                 "<i>V</i> = ⅓<i>Bh</i> = ⅓ × %d² × %d = <b>%s in.³</b>" % (s_, h, num(V)))
    if kind == "cav":
        n = r.randint(10, 30)
        rad, h = r.randint(9, 15), 2 * n
        q = ("Two stacks of %d coins have the same height. One stack is straight and the other leans to one side. "
             "Each coin has radius %d mm and the stacks are %d mm tall. How do their volumes compare?" % (n, rad, h))
        right = "They are equal (%dπ mm³ each)" % (rad * rad * h)
        return T(q, right, ["The leaning stack has more volume", "The straight stack has more volume", "They are equal (%dπ mm³ each)" % (2 * rad * h)],
                 "Cavalieri's principle: same height and the same cross-section at every level means the same volume. π × %d² × %d = %dπ. <b>%s</b>." % (rad, h, rad * rad * h, right))
    if kind == "comp":
        rad, h = r.randint(2, 6), r.randint(4, 12)
        q = "A silo is a cylinder with radius %d m and height %d m, topped by a hemisphere. Find its volume in terms of π." % (rad, h)
        c = F(rad * rad * h) + F(2 * rad ** 3, 3)
        right = pi_form(c, "m")
        return T(q, right, pick_wr(right, [pi_form(F(rad * rad * h) + F(4 * rad ** 3, 3), "m"), pi_form(rad * rad * h, "m"), pi_form(F(rad * rad * h) + 2 * rad * rad, "m")]),
                 "Cylinder: π × %d² × %d = %dπ. Hemisphere: ⅔π × %d³ = %s. Total: <b>%s</b>." % (rad, h, rad * rad * h, rad, pi_form(F(2 * rad ** 3, 3), "m").replace(" m³", ""), right))
    if kind == "dens":
        mat, d = r.choice([("aluminum", F(27, 10)), ("ice", F(9, 10)), ("oak wood", F(3, 4)), ("granite", F(27, 10)), ("steel", F(39, 5))])
        a, b, c = r.randint(2, 10), r.randint(2, 10), r.randint(2, 10)
        V = a * b * c
        m = d * V
        q = "A block of %s measures %d cm by %d cm by %d cm. Its density is %s g/cm³. What is its mass?" % (mat, a, b, c, num(d))
        return T(q, "%s g" % num(m), ["%s g" % num(w) for w in dict.fromkeys([F(V) / d, V, d * (a + b + c)]) if w != m and num(w)][:3],
                 "Mass = density × volume = %s × (%d × %d × %d) = %s × %d = <b>%s g</b>." % (num(d), a, b, c, num(d), V, num(m)))
    if kind == "ratio":
        k = r.choice([2, 3])
        q = "The radius and the height of a cone are both multiplied by %d. By what factor does the volume change?" % k
        return T(q, num(k ** 3), [num(k), num(k * k), num(3 * k)],
                 "Volume is three dimensions, so it changes by the cube of the scale factor: %d³ = <b>%d</b>." % (k, k ** 3))
    rad = r.randint(2, 9)
    h = r.randint(3, 15)
    V = rad * rad * h
    q = "A cylinder has volume %dπ cm³ and radius %d cm. Find its height." % (V, rad)
    return T(q, "%d cm" % h, ["%s cm" % num(w) for w in dict.fromkeys([F(V, rad), F(V, 2 * rad), F(V, rad * rad * 3)]) if w != h and num(w)][:3] + ["%d cm" % (h + 2)],
             "<i>V</i> = π<i>r</i>²<i>h</i>: %dπ = π × %d × <i>h</i>, so <i>h</i> = %d ÷ %d = <b>%d cm</b>." % (V, rad * rad, V, rad * rad, h)) if False else T(
        q, "%d cm" % h, ["%s cm" % num(w) for w in dict.fromkeys([F(V, rad), F(V, 2 * rad) , h * 3]) if w != h and num(w)][:3] if len([w for w in dict.fromkeys([F(V, rad), F(V, 2 * rad), h * 3]) if w != h and num(w)]) >= 3 else ["%d cm" % (h + 1), "%d cm" % (h * 3), "%d cm" % (V // rad)],
        "<i>V</i> = π<i>r</i>²<i>h</i>: %dπ = π × %d × <i>h</i>, so <i>h</i> = %d ÷ %d = <b>%d cm</b>." % (V, rad * rad, V, rad * rad, h))


def body():
    return lesson(
        "<p><b>Cylinder:</b> <i>V</i> = π<i>r</i>²<i>h</i> (area of the circle × height). "
        "<b>Cone:</b> <i>V</i> = ⅓π<i>r</i>²<i>h</i>, one third of the cylinder with the same base and height. "
        "<b>Sphere:</b> <i>V</i> = ⁴⁄₃π<i>r</i>³. A <b>hemisphere</b> is half a sphere: ⅔π<i>r</i>³. "
        "<b>Pyramid:</b> <i>V</i> = ⅓<i>Bh</i>, where <i>B</i> is the area of the base.</p>"
        "<p><b>Cavalieri's principle</b>: two solids with the same height and the same cross-sectional area at every level have the same volume. "
        "<b>Density</b> = mass ÷ volume.</p>"
        "<p>Always use the <b>radius</b>. If you are given the diameter, halve it first. "
        "An answer “in terms of π” keeps π as a letter, for example 45π cm³.</p>",
        [("Cylinder: <i>r</i> = 4 cm, <i>h</i> = 10 cm.", ["π × 4² × 10 = 160π."], "502.7 cm³"),
         ("Cone: <i>r</i> = 3 cm, <i>h</i> = 8 cm.", ["⅓ × π × 9 × 8 = 24π."], "75.4 cm³"),
         ("Sphere: diameter 12 cm.", ["<i>r</i> = 6 cm.", "⁴⁄₃ × π × 216 = 288π."], "904.8 cm³")],
        ["Using the diameter instead of the radius.",
         "Forgetting the ⅓ in the cone formula.",
         "Using 4π<i>r</i>² (surface area) for the volume of a sphere.",
         "Mixing units, such as meters and centimeters, in one calculation."])


def main():
    sets = [S("Volume of a cylinder", collect(one_cyl, 20, R)),
            S("Volume of a cone", collect(one_cone, 20, R)),
            S("Volume of spheres and hemispheres", collect(one_sph, 20, R)),
            S("Answers in terms of π", collect(one_pi, 20, R)),
            S("Pyramids, composite solids and density", collect(one_prob, 20, R))]
    make("volume-of-solids", 21, "G-GMD.A.3",
         "Volume of Cylinders, Pyramids, Cones, and Spheres",
         "Volume of Cylinders, Cones, Pyramids and Spheres Worksheet (Geometry, G-GMD.A.3) | 100 Questions",
         "Volume of Solids",
         "Use volume formulas for cylinders, pyramids, cones, and spheres to solve problems.",
         "Free Geometry worksheet on volume: cylinders, cones, spheres, hemispheres and pyramids, answers in terms of π, Cavalieri's principle and density. 100 questions with answers.",
         "Cylinder πr²h. Cone ⅓πr²h. Sphere ⁴⁄₃πr³. Pyramid ⅓Bh.",
         "Always use the radius. Cones and pyramids are one third of the matching prism or cylinder.",
         body(),
         [("What is the formula for the volume of a cone?", "V = (1/3)πr²h. It is one third of a cylinder with the same base and height."),
          ("What is the formula for the volume of a sphere?", "V = (4/3)πr³, where r is the radius."),
          ("What is Cavalieri's principle?", "If two solids have the same height and the same cross-sectional area at every level, they have the same volume."),
          ("How do you find the volume of a pyramid?", "Multiply the area of the base by the height and divide by 3: V = (1/3)Bh.")],
         sets, R, domain="Volume and Solids", grade="geometry")


if __name__ == "__main__":
    main()
