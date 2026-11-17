# -*- coding: utf-8 -*-
"""
US Geometry: Arc Length and Sector Area (Common Core G-C.B.5)
  python3 tools/gen_us_math_ge_arc_length_and_sector_area.py
Ported from the UK Year 9 generator, with a set on radians (s = rθ, A = ½r²θ) for G-C.B.5.
Arc length = θ/360 × 2πr, sector area = θ/360 × πr², answers to 1 decimal place and in terms of π, the
perimeter of a sector, finding the angle, and problems.
Wrong answers come from real mistakes: mixing up the arc length and area formulas, forgetting the fraction
θ/360, forgetting to add the two radii for the perimeter, and using the diameter as the radius.
"""
import math
import random
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F
from us_hs import num, B, S, make, lesson, collect, T, svg_wrap, line, text, fig, INK, RED, BLUE

R = random.Random(93901)
PI = "π"
FILL = "#e8f1fb"


def d1(x):
    return "{:,.1f}".format(Decimal(repr(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def coef(c):
    c = F(c)
    if c.denominator == 1:
        return "" if c == 1 else num(c)
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%d</span></span>" % (num(c.numerator), c.denominator)


def pif(c, u):
    return "%s%s %s" % (coef(c), PI, u)


def sector_svg(theta, rlab):
    cx, cy, rr = 120, 112, 90
    t = math.radians(theta)
    x2, y2 = cx + rr * math.cos(t), cy - rr * math.sin(t)
    big = 1 if theta > 180 else 0
    s = ["<path d='M%d %d L%d %d A%d %d 0 %d 0 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, cx + rr, cy, rr, rr, big, x2, y2, FILL, INK)]
    s.append("<path d='M%d %d A%d %d 0 %d 0 %.1f %.1f' fill='none' stroke='%s' stroke-width='4'/>" % (cx + rr, cy, rr, rr, big, x2, y2, BLUE))
    ar = 24 if theta >= 60 else 34
    s.append("<path d='M%.1f %d A%d %d 0 %d 0 %.1f %.1f' fill='none' stroke='%s' stroke-width='1.5'/>" % (cx + ar, cy, ar, ar, big, cx + ar * math.cos(t), cy - ar * math.sin(t), INK))
    m = t / 2
    lr = 44 if theta >= 60 else 54
    s.append(text(cx + lr * math.cos(m), cy - lr * math.sin(m) + 5, "%d°" % theta, 14))
    s.append(text(cx + rr / 2, cy + 18, rlab, 15, col=RED))
    s.append("<circle cx='%d' cy='%d' r='3' fill='%s'/>" % (cx, cy, INK))
    H = cy + 30 if theta <= 180 else cy + rr + 14
    return svg_wrap(240, H, "".join(s), "sector of a circle")


ANGLES = [30, 40, 45, 60, 72, 80, 90, 100, 110, 120, 135, 140, 150, 160, 200, 210, 240, 270, 300]


def pick(right, cands):
    out = []
    for c in cands:
        if c != right and c not in out:
            out.append(c)
    return out[:3]


# ------------------------------------------------------------ set 1: arc length
def one_arc(r):
    th, rad = r.choice(ANGLES), r.randint(3, 20)
    L = th / 360.0 * 2 * math.pi * rad
    q = fig(sector_svg(th, "%d cm" % rad)) + "Find the length of the blue arc. Give your answer to 1 decimal place."
    right = d1(L) + " cm"
    wr = [d1(th / 360.0 * math.pi * rad * rad) + " cm", d1(2 * math.pi * rad) + " cm", d1(th / 360.0 * math.pi * rad) + " cm", d1(th / 360.0 * 4 * math.pi * rad) + " cm"]
    e = "Arc = <sup>%d</sup>/<sub>360</sub> × 2π × %d = <b>%s</b>." % (th, rad, right)
    return T(q, right, pick(right, wr), e)


# ------------------------------------------------------------ set 2: sector area
def one_area(r):
    th, rad = r.choice(ANGLES), r.randint(3, 18)
    A = th / 360.0 * math.pi * rad * rad
    q = fig(sector_svg(th, "%d cm" % rad)) + "Find the area of the sector. Give your answer to 1 decimal place."
    right = d1(A) + " cm²"
    wr = [d1(th / 360.0 * 2 * math.pi * rad) + " cm²", d1(math.pi * rad * rad) + " cm²", d1(th / 360.0 * math.pi * (2 * rad) ** 2) + " cm²", d1(th / 180.0 * math.pi * rad * rad) + " cm²"]
    e = "Area = <sup>%d</sup>/<sub>360</sub> × π × %d² = <b>%s</b>." % (th, rad, right)
    return T(q, right, pick(right, wr), e)


# ------------------------------------------------------------ set 3: in terms of π
def one_pi(r):
    th = r.choice([30, 45, 60, 90, 120, 180, 270, 150, 240, 72])
    rad = r.choice([2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 18, 20])
    frac = F(th, 360)
    name = {90: "quarter circle", 180: "semicircle"}.get(th)
    shape = ("a %s of radius %d cm" % (name, rad)) if name else ("a sector with angle %d° and radius %d cm" % (th, rad))
    if r.random() < 0.5:
        c = frac * 2 * rad
        q = "Find the arc length of %s, in terms of %s." % (shape, PI)
        right = pif(c, "cm")
        wr = [pif(frac * rad * rad, "cm"), pif(2 * rad, "cm"), pif(frac * rad, "cm"), pif(c * 2, "cm")]
        e = "<sup>%d</sup>/<sub>360</sub> × 2π × %d = <b>%s</b>." % (th, rad, right)
    else:
        c = frac * rad * rad
        q = "Find the area of %s, in terms of %s." % (shape, PI)
        right = pif(c, "cm²")
        wr = [pif(frac * 2 * rad, "cm²"), pif(rad * rad, "cm²"), pif(frac * 4 * rad * rad, "cm²"), pif(frac * rad, "cm²")]
        e = "<sup>%d</sup>/<sub>360</sub> × π × %d² = <b>%s</b>." % (th, rad, right)
    return T(q, right, pick(right, wr), e)


# ------------------------------------------------------------ set 4: perimeter and finding the angle
def one_perim(r):
    k = r.randint(0, 2)
    if k == 0:
        th, rad = r.choice(ANGLES), r.randint(4, 15)
        L = th / 360.0 * 2 * math.pi * rad
        q = fig(sector_svg(th, "%d cm" % rad)) + "Find the perimeter of the sector. Give your answer to 1 decimal place."
        right = d1(L + 2 * rad) + " cm"
        wr = [d1(L) + " cm", d1(L + rad) + " cm", d1(th / 360.0 * math.pi * rad * rad + 2 * rad) + " cm"]
        e = "Arc = %s cm. Perimeter = arc + 2 radii = %s + %d = <b>%s</b>." % (d1(L), d1(L), 2 * rad, right)
        return T(q, right, pick(right, wr), e)
    th = r.choice([30, 40, 45, 60, 72, 90, 120, 135, 150, 180, 240])
    rad = r.choice([3, 4, 5, 6, 8, 9, 10, 12])
    if k == 1:
        c = F(th, 360) * 2 * rad
        q = "A sector of radius %d cm has arc length %s. What is the angle of the sector?" % (rad, pif(c, "cm"))
        right = "%d°" % th
        wr = ["%d°" % (th * 2) if th * 2 < 360 else "%d°" % (th // 2), "%s°" % num(c), "%d°" % (360 - th)]
        e = "<sup>θ</sup>/<sub>360</sub> × 2π × %d = %s, so <sup>θ</sup>/<sub>360</sub> = %s ÷ %d and θ = <b>%d°</b>." % (rad, pif(c, ""), coef(c) or "1", 2 * rad, th)
        e = "<sup>θ</sup>/<sub>360</sub> × %d%s = %s. So θ = 360 × %s ÷ %d = <b>%d°</b>." % (2 * rad, PI, pif(c, "cm"), coef(c) or "1", 2 * rad, th)
        return T(q, right, pick(right, wr), e)
    c = F(th, 360) * rad * rad
    q = "A sector of radius %d cm has area %s. What is the angle of the sector?" % (rad, pif(c, "cm²"))
    right = "%d°" % th
    wr = ["%d°" % (th * 2) if th * 2 < 360 else "%d°" % (th // 2), "%d°" % (360 - th), "%d°" % (th // 2 if th * 2 < 360 and th % 2 == 0 else th + 30)]
    e = "<sup>θ</sup>/<sub>360</sub> × %d%s = %s. So θ = 360 × %s ÷ %d = <b>%d°</b>." % (rad * rad, PI, pif(c, "cm²"), coef(c) or "1", rad * rad, th)
    return T(q, right, pick(right, wr), e)


# ------------------------------------------------------------ radians
RAD = [(30, 1, 6), (45, 1, 4), (60, 1, 3), (90, 1, 2), (120, 2, 3), (135, 3, 4), (150, 5, 6), (180, 1, 1), (210, 7, 6), (225, 5, 4), (240, 4, 3), (270, 3, 2), (300, 5, 3), (315, 7, 4), (36, 1, 5), (72, 2, 5)]


def pr(n, d):
    """n pi / d"""
    top = ("" if n == 1 else str(n)) + "π"
    return top if d == 1 else "<span class='fr'><span class='fn'>%s</span><span class='fd'>%d</span></span>" % (top, d)


def kp(k):
    k = F(k)
    if k.denominator == 1:
        return ("" if k == 1 else str(k.numerator)) + "π"
    return pr(k.numerator, k.denominator)


def one_radian(r):
    deg, n, d = r.choice(RAD)
    kind = r.choice(["to_rad", "to_deg", "arc", "arc", "area", "area"])
    if kind == "to_rad":
        q = "Convert %s to radians." % B("%d°" % deg)
        right = pr(n, d)
        return T(q, right, pick(right, [kp(F(d, n)), kp(F(2 * n, d)), kp(F(n, 2 * d)), "%dπ" % deg]), "Multiply by π/180: %d × π ÷ 180 = <b>%s</b>." % (deg, right))
    if kind == "to_deg":
        q = "Convert %s radians to degrees." % B(pr(n, d))
        right = "%d°" % deg
        return T(q, right, pick(right, ["%d°" % (deg // 2 if deg % 2 == 0 else deg + 30), "%d°" % (360 - deg), "%d°" % (2 * deg), "%d°" % (deg + 45)]),
                 "π radians = 180°, so %s = <b>%d°</b>." % (pr(n, d), deg))
    rr = r.choice([2, 3, 4, 6, 8, 9, 10, 12, 15, 18])
    if kind == "arc":
        k = F(rr * n, d)
        q = "A sector has radius %d cm and central angle %s radians. Find the arc length in terms of π." % (rr, pr(n, d))
        right = kp(k) + " cm"
        return T(q, right, pick(right, [kp(k * rr / 2) + " cm", kp(k * 2) + " cm", kp(F(n, d)) + " cm", kp(k / 2) + " cm"]),
                 "In radians, arc length <i>s</i> = <i>r</i>θ = %d × %s = <b>%s</b>." % (rr, pr(n, d), right))
    k = F(rr * rr * n, 2 * d)
    q = "A sector has radius %d cm and central angle %s radians. Find its area in terms of π." % (rr, pr(n, d))
    right = kp(k) + " cm²"
    return T(q, right, pick(right, [kp(2 * k) + " cm²", kp(F(rr * n, d)) + " cm²", kp(k / rr) + " cm²", kp(k * 2 / rr) + " cm²"]),
             "In radians, sector area = ½<i>r</i>²θ = ½ × %d × %s = <b>%s</b>." % (rr * rr, pr(n, d), right))


# ------------------------------------------------------------ set 5: problems
def problems():
    data = [
        ("A pizza has radius 15 cm. It is cut into 8 equal slices. What is the area of one slice, to 1 decimal place?", "88.4 cm²", ["11.8 cm²", "706.9 cm²", "176.7 cm²"],
         "Each slice is a 45° sector: <sup>1</sup>/<sub>8</sub> × π × 15² = <b>88.4 cm²</b>."),
        ("A clock's minute hand is 10 cm long. How far does its tip travel in 15 minutes, to 1 decimal place?", "15.7 cm", ["78.5 cm", "62.8 cm", "31.4 cm"],
         "15 minutes is a quarter turn: ¼ × 2π × 10 = <b>15.7 cm</b>."),
        ("A clock's minute hand is 12 cm long. What area does it sweep in 20 minutes, in terms of π?", "48π cm²", ["8π cm²", "144π cm²", "72π cm²"],
         "20 minutes is ⅓ of a turn: ⅓ × π × 12² = <b>48π cm²</b>."),
        ("What fraction of a circle is a sector with angle 72°?", "<span class='fr'><span class='fn'>1</span><span class='fd'>5</span></span>", ["<span class='fr'><span class='fn'>1</span><span class='fd'>4</span></span>", "<span class='fr'><span class='fn'>1</span><span class='fd'>6</span></span>", "<span class='fr'><span class='fn'>72</span><span class='fd'>100</span></span>"],
         "72 ÷ 360 = <b>⅕</b>."),
        ("What is the perimeter of a semicircle with diameter 10 cm, to 1 decimal place?", "25.7 cm", ["15.7 cm", "31.4 cm", "20.7 cm"],
         "Curved part: ½ × π × 10 = 15.7 cm. Add the diameter: 15.7 + 10 = <b>25.7 cm</b>."),
        ("What is the area of a semicircle with diameter 10 cm, to 1 decimal place?", "39.3 cm²", ["78.5 cm²", "157.1 cm²", "15.7 cm²"],
         "<i>r</i> = 5 cm. ½ × π × 5² = <b>39.3 cm²</b>."),
        ("What is the perimeter of a quarter circle with radius 6 cm, in terms of π?", "(3π + 12) cm", ["3π cm", "(3π + 6) cm", "(9π + 12) cm"],
         "Arc: ¼ × 2π × 6 = 3π. Add two radii: <b>(3π + 12) cm</b>."),
        ("A sector has angle 90° and arc length 5π cm. What is its radius?", "10 cm", ["5 cm", "20 cm", "2.5 cm"],
         "¼ × 2π<i>r</i> = 5π, so <i>r</i>/2 = 5 and <i>r</i> = <b>10 cm</b>."),
        ("A sector has angle 40° and area 4π cm². What is its radius?", "6 cm", ["36 cm", "3 cm", "12 cm"],
         "<sup>1</sup>/<sub>9</sub> × π<i>r</i>² = 4π, so <i>r</i>² = 36 and <i>r</i> = <b>6 cm</b>."),
        ("A fan opens to 120°. Its ribs are 21 cm long. What area does the open fan cover, to the nearest cm²?", "462 cm²", ["44 cm²", "1,385 cm²", "231 cm²"],
         "⅓ × π × 21² = 147π = 461.8 ≈ <b>462 cm²</b>."),
        ("A windshield wiper is 50 cm long and turns through 110°. How far does its tip travel, to 1 decimal place?", "96.0 cm", ["2,400.0 cm", "48.0 cm", "314.2 cm"],
         "<sup>110</sup>/<sub>360</sub> × 2π × 50 = <b>96.0 cm</b>."),
        ("Two sectors have the same radius. One has angle 60° and the other 120°. How do their areas compare?", "The 120° sector is twice as big", ["They are equal", "The 120° sector is four times as big", "The 60° sector is bigger"],
         "Area is proportional to the angle, so doubling the angle doubles the area: <b>the 120° sector is twice as big</b>."),
        ("If the radius of a sector doubles and the angle stays the same, what happens to its area?", "It is multiplied by 4", ["It doubles", "It stays the same", "It is multiplied by 8"],
         "Area uses <i>r</i>², and 2² = 4, so <b>it is multiplied by 4</b>."),
        ("If the radius of a sector doubles and the angle stays the same, what happens to its arc length?", "It doubles", ["It is multiplied by 4", "It stays the same", "It halves"],
         "Arc length is proportional to <i>r</i>, so <b>it doubles</b>."),
        ("A running track bend is a semicircle with radius 36.5 m. How long is the bend, to 1 decimal place?", "114.7 m", ["229.3 m", "57.3 m", "4,185.4 m"],
         "½ × 2π × 36.5 = π × 36.5 = <b>114.7 m</b>."),
        ("A sector has radius 9 cm and arc length 6π cm. What is its area in terms of π?", "27π cm²", ["54π cm²", "81π cm²", "6π cm²"],
         "The circumference is 18π, so the sector is ⅓ of the circle. Area = ⅓ × 81π = <b>27π cm²</b>."),
        ("Which formula gives the arc length of a sector with angle θ?", "<sup>θ</sup>/<sub>360</sub> × 2π<i>r</i>", ["<sup>θ</sup>/<sub>360</sub> × π<i>r</i>²", "θ × 2π<i>r</i>", "<sup>360</sup>/<sub>θ</sub> × 2π<i>r</i>"],
         "Arc length is the fraction <sup>θ</sup>/<sub>360</sub> of the circumference: <b><sup>θ</sup>/<sub>360</sub> × 2π<i>r</i></b>."),
        ("Which formula gives the area of a sector with angle θ?", "<sup>θ</sup>/<sub>360</sub> × π<i>r</i>²", ["<sup>θ</sup>/<sub>360</sub> × 2π<i>r</i>", "θπ<i>r</i>²", "<sup>θ</sup>/<sub>180</sub> × π<i>r</i>²"],
         "Sector area is the fraction <sup>θ</sup>/<sub>360</sub> of the circle's area: <b><sup>θ</sup>/<sub>360</sub> × π<i>r</i>²</b>."),
        ("A cake of radius 12 cm has a 30° slice removed. What area of the top is left, in terms of π?", "132π cm²", ["12π cm²", "144π cm²", "120π cm²"],
         "330° is left: <sup>330</sup>/<sub>360</sub> × 144π = <b>132π cm²</b>."),
        ("A garden sprinkler waters a sector with radius 4 m and angle 270°. What area does it water, to 1 decimal place?", "37.7 m²", ["50.3 m²", "18.8 m²", "12.6 m²"],
         "¾ × π × 4² = 12π = <b>37.7 m²</b>."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>A <b>sector</b> is a slice of a circle between two radii. Its curved edge is an <b>arc</b>. "
        "If the angle at the center is θ, the sector is the fraction <sup>θ</sup>/<sub>360</sub> of the whole circle.</p>"
        "<p><b>Arc length</b> = <sup>θ</sup>/<sub>360</sub> × 2π<i>r</i>. "
        "<b>Sector area</b> = <sup>θ</sup>/<sub>360</sub> × π<i>r</i>². "
        "The <b>perimeter</b> of a sector is the arc length plus two radii.</p>",
        [("Arc length: θ = 60°, <i>r</i> = 9 cm.", ["<sup>60</sup>/<sub>360</sub> = ⅙.", "⅙ × 2π × 9 = 3π."], "9.4 cm"),
         ("Sector area: θ = 60°, <i>r</i> = 9 cm.", ["⅙ × π × 81 = 13.5π."], "42.4 cm²"),
         ("Perimeter of that sector.", ["9.4 + 9 + 9."], "27.4 cm")],
        ["Using 2π<i>r</i> for the area or π<i>r</i>² for the arc.",
         "Forgetting to multiply by <sup>θ</sup>/<sub>360</sub>.",
         "Forgetting the two straight edges when finding the perimeter.",
         "Using the diameter as the radius."])


def main():
    sets = [S("Arc length", collect(one_arc, 20, R)),
            S("Area of a sector", collect(one_area, 20, R)),
            S("Radians", collect(one_radian, 20, R)),
            S("Perimeter and finding the angle", collect(one_perim, 20, R)),
            S("Arc and sector problems", problems())]
    b = body().replace("Using the diameter as the radius.</li>", "Using the diameter as the radius.</li><li>Mixing degree and radian formulas. With radians, <i>s</i> = <i>r</i>θ and the area is ½<i>r</i>²θ.</li>")
    b = b.replace("The <b>perimeter</b> of a sector is the arc length plus two radii.</p>",
                  "The <b>perimeter</b> of a sector is the arc length plus two radii.</p><p>In <b>radians</b> (π radians = 180°), the arc length is <i>s</i> = <i>r</i>θ and the sector area is ½<i>r</i>²θ. "
                  "The radian measure of an angle is the arc length divided by the radius.</p>")
    make("arc-length-and-sector-area", 19, "G-C.B.5",
         "Arc Length and Sector Area (Degrees and Radians)",
         "Arc Length and Sector Area Worksheet with Radians (Geometry, G-C.B.5) | 100 Questions with Answers",
         "Arc Length and Sector Area",
         "Derive using similarity the fact that the length of the arc intercepted by an angle is proportional to the radius, and define the radian measure of the angle as the constant of proportionality; derive the formula for the area of a sector.",
         "Free Geometry worksheet on arc length and sector area in degrees and radians: answers in terms of π, perimeter of a sector, and word problems. 100 questions with answers.",
         "A sector is θ/360 of the whole circle.",
         "Arc length = θ/360 × 2πr. In radians, s = rθ and the area is ½r²θ.",
         b,
         [("How do I find the arc length?", "Multiply the circumference 2πr by the fraction θ/360. In radians, the arc length is simply s = rθ."),
          ("How do I find the area of a sector?", "Multiply the circle's area πr² by θ/360. In radians, the area is ½r²θ."),
          ("How do you convert degrees to radians?", "Multiply by π/180. For example, 60° × π/180 = π/3 radians."),
          ("What is the perimeter of a sector?", "The arc length plus the two radii.")],
         sets, R, domain="Circles", grade="geometry")


if __name__ == "__main__":
    main()
