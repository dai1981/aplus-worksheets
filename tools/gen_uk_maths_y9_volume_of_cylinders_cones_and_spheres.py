# -*- coding: utf-8 -*-
"""
UK Year 9 Maths: Volume of Cylinders, Cones and Spheres (KS3 Geometry and measures)
  python3 tools/gen_uk_maths_y9_volume_of_cylinders_cones_and_spheres.py
V = πr²h for a cylinder, V = ⅓πr²h for a cone and V = ⁴⁄₃πr³ for a sphere, with answers to 1 decimal place and
in terms of π, hemispheres, capacity in litres and composite solids.
Wrong answers come from real mistakes: using the diameter as the radius, forgetting the ⅓ for a cone, using
2πrh (the curved surface) instead of the volume, and using r² instead of r³ for a sphere.
"""
import math
import random
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F
from uk_ks3 import num, B, S, make, lesson, collect, T, svg_wrap, line, text, fig, INK, RED, BLUE

R = random.Random(90901)
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
        q = "A cone has radius %d cm and perpendicular height %d cm. Find its volume in terms of %s." % (rad, h, PI)
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


# ------------------------------------------------------------ set 5: problems
def problems():
    data = [
        ("A cylindrical tin has radius 5 cm and height 12 cm. What is its capacity to the nearest millilitre? (1 cm³ = 1 ml)", "942 ml", ["377 ml", "314 ml", "3,770 ml"],
         "π × 5² × 12 = 300π = 942.47… cm³ = <b>942 ml</b>."),
        ("A cylindrical water tank has radius 50 cm and height 1.2 m. How many litres does it hold, to the nearest litre?", "942 litres", ["94 litres", "9,425 litres", "188 litres"],
         "Work in cm: π × 50² × 120 = 942,477.8 cm³. 1,000 cm³ = 1 litre, so <b>942 litres</b>."),
        ("A cylinder has volume 500 cm³ and radius 5 cm. What is its height, to 1 decimal place?", "6.4 cm", ["20 cm", "31.8 cm", "3.2 cm"],
         "<i>h</i> = 500 ÷ (π × 5²) = 500 ÷ 78.54… = <b>6.4 cm</b>."),
        ("A sphere has volume 36π cm³. What is its radius?", "3 cm", ["9 cm", "6 cm", "27 cm"],
         "⁴⁄₃π<i>r</i>³ = 36π, so <i>r</i>³ = 27 and <i>r</i> = <b>3 cm</b>."),
        ("A cone and a cylinder have the same radius and height. How many cones of water fill the cylinder?", "3", ["2", "4", "1.5"],
         "A cone is ⅓ of the cylinder with the same base and height, so <b>3</b> cones fill it."),
        ("An ice cream cone has radius 3 cm and height 10 cm, with a hemisphere of ice cream on top of radius 3 cm. Find the total volume in terms of π.", "48π cm³", ["30π cm³", "66π cm³", "36π cm³"],
         "Cone: ⅓ × π × 9 × 10 = 30π. Hemisphere: ⅔ × π × 27 = 18π. Total: <b>48π cm³</b>."),
        ("A ball has diameter 22 cm. What is its volume to the nearest cm³?", "5,575 cm³", ["44,602 cm³", "1,521 cm³", "1,394 cm³"],
         "<i>r</i> = 11 cm. ⁴⁄₃ × π × 11³ = 5,575.3 cm³ ≈ <b>5,575 cm³</b>."),
        ("If the radius of a sphere doubles, what happens to its volume?", "It is multiplied by 8", ["It doubles", "It is multiplied by 4", "It is multiplied by 6"],
         "Volume depends on <i>r</i>³, and 2³ = 8, so <b>it is multiplied by 8</b>."),
        ("If the height of a cylinder doubles and the radius stays the same, what happens to its volume?", "It doubles", ["It is multiplied by 4", "It is multiplied by 8", "It stays the same"],
         "<i>V</i> = π<i>r</i>²<i>h</i> and only <i>h</i> doubles, so <b>it doubles</b>."),
        ("If the radius of a cylinder doubles and the height stays the same, what happens to its volume?", "It is multiplied by 4", ["It doubles", "It is multiplied by 8", "It stays the same"],
         "<i>V</i> depends on <i>r</i>², and 2² = 4, so <b>it is multiplied by 4</b>."),
        ("Which formula gives the volume of a cone?", "⅓π<i>r</i>²<i>h</i>", ["π<i>r</i>²<i>h</i>", "⁴⁄₃π<i>r</i>³", "2π<i>rh</i>"],
         "A cone is one third of a cylinder: <b>⅓π<i>r</i>²<i>h</i></b>."),
        ("Which formula gives the volume of a sphere?", "⁴⁄₃π<i>r</i>³", ["4π<i>r</i>²", "⅓π<i>r</i>²<i>h</i>", "π<i>r</i>²<i>h</i>"],
         "<b>⁴⁄₃π<i>r</i>³</b>. 4π<i>r</i>² is the surface area."),
        ("A pipe is a cylinder 2 m long with radius 3 cm. What is its volume in cm³, to the nearest whole number?", "5,655 cm³", ["57 cm³", "3,770 cm³", "565 cm³"],
         "2 m = 200 cm. π × 3² × 200 = 1,800π = <b>5,655 cm³</b>."),
        ("A cylindrical glass of radius 4 cm is filled with 400 cm³ of water. How deep is the water, to 1 decimal place?", "8.0 cm", ["25.0 cm", "31.8 cm", "2.5 cm"],
         "Depth = 400 ÷ (π × 4²) = 400 ÷ 50.27 = <b>8.0 cm</b>."),
        ("Which holds more: a cylinder with radius 3 cm and height 4 cm, or a sphere with radius 3 cm?", "The sphere", ["The cylinder", "They hold the same", "You cannot tell"],
         "Cylinder: 36π cm³. Sphere: ⁴⁄₃ × π × 27 = 36π cm³. Wait: both are 36π, so they hold the same."),
        ("A solid metal sphere of radius 6 cm is melted and made into a cylinder of radius 6 cm. How tall is the cylinder?", "8 cm", ["6 cm", "12 cm", "4 cm"],
         "Sphere: ⁴⁄₃π × 216 = 288π. Cylinder: π × 36 × <i>h</i> = 288π, so <i>h</i> = <b>8 cm</b>."),
        ("A cone has volume 100π cm³ and radius 5 cm. What is its height?", "12 cm", ["4 cm", "20 cm", "60 cm"],
         "⅓ × π × 25 × <i>h</i> = 100π, so 25<i>h</i> = 300 and <i>h</i> = <b>12 cm</b>."),
        ("A hemisphere bowl has radius 9 cm. What is its capacity in terms of π?", "486π cm³", ["972π cm³", "162π cm³", "243π cm³"],
         "⅔ × π × 9³ = ⅔ × 729π = <b>486π cm³</b>."),
        ("Leo uses <i>r</i> = 10 for a cylinder labelled with diameter 10 cm and height 4 cm. What should the volume be, in terms of π?", "100π cm³", ["400π cm³", "40π cm³", "200π cm³"],
         "The radius is 5 cm, not 10 cm: π × 5² × 4 = <b>100π cm³</b>. Leo got 400π."),
        ("What is the volume of a cylinder with radius 1 cm and height 1 cm, to 2 decimal places?", "3.14 cm³", ["6.28 cm³", "1.00 cm³", "1.05 cm³"],
         "π × 1² × 1 = π = <b>3.14 cm³</b>."),
    ]
    data[14] = ("Which holds more: a cylinder with radius 3 cm and height 4 cm, or a sphere with radius 3 cm?", "They hold the same", ["The cylinder", "The sphere", "You cannot tell"],
                "Cylinder: π × 9 × 4 = 36π cm³. Sphere: ⁴⁄₃ × π × 27 = 36π cm³. <b>They hold the same.</b>")
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p><b>Cylinder:</b> <i>V</i> = π<i>r</i>²<i>h</i> (area of the circle × height). "
        "<b>Cone:</b> <i>V</i> = ⅓π<i>r</i>²<i>h</i>, one third of the cylinder with the same base and height. "
        "<b>Sphere:</b> <i>V</i> = ⁴⁄₃π<i>r</i>³. A <b>hemisphere</b> is half a sphere: ⅔π<i>r</i>³.</p>"
        "<p>Always use the <b>radius</b>. If you are given the diameter, halve it first. "
        "An answer “in terms of π” keeps π as a letter, for example 45π cm³.</p>",
        [("Cylinder: <i>r</i> = 4 cm, <i>h</i> = 10 cm.", ["π × 4² × 10 = 160π."], "502.7 cm³"),
         ("Cone: <i>r</i> = 3 cm, <i>h</i> = 8 cm.", ["⅓ × π × 9 × 8 = 24π."], "75.4 cm³"),
         ("Sphere: diameter 12 cm.", ["<i>r</i> = 6 cm.", "⁴⁄₃ × π × 216 = 288π."], "904.8 cm³")],
        ["Using the diameter instead of the radius.",
         "Forgetting the ⅓ in the cone formula.",
         "Using 4π<i>r</i>² (surface area) for the volume of a sphere.",
         "Mixing units, such as metres and centimetres, in one calculation."])


def main():
    sets = [S("Volume of a cylinder", collect(one_cyl, 20, R)),
            S("Volume of a cone", collect(one_cone, 20, R)),
            S("Volume of spheres and hemispheres", collect(one_sph, 20, R)),
            S("Answers in terms of π", collect(one_pi, 20, R)),
            S("Volume problems", problems())]
    make(9, "volume-of-cylinders-cones-and-spheres", 9, "G",
         "Volume of Cylinders, Cones and Spheres",
         "Year 9 Volume Worksheets: Cylinders, Cones, Spheres and Hemispheres (in terms of π)",
         "Cylinders, Cones and Spheres",
         "Calculate and solve problems involving: perimeters of 2-D shapes (including circles), areas of circles and composite "
         "shapes; surface area and volume of cuboids and other right prisms (including cylinders).",
         "Free Year 9 volume worksheets: volume of cylinders, cones, spheres and hemispheres, answers to 1 decimal place and "
         "in terms of π, capacity and composite solids. 100 questions with answers.",
         "Cylinder πr²h, cone ⅓πr²h, sphere ⁴⁄₃πr³.",
         "Always use the radius. Halve the diameter first.",
         body(),
         [("What is the formula for the volume of a cylinder?", "V = πr²h: the area of the circular end multiplied by the height."),
          ("Why is a cone one third of a cylinder?", "A cone with the same base and height as a cylinder holds exactly one third as much, so V = ⅓πr²h."),
          ("What is the volume of a sphere?", "V = ⁴⁄₃πr³. For a hemisphere, halve it: ⅔πr³."),
          ("What does 'in terms of π' mean?", "Leave π as a symbol instead of using 3.14…. For example a cylinder with r = 3 and h = 5 has volume 45π cm³.")],
         sets, R)


if __name__ == "__main__":
    main()
