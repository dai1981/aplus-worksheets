# -*- coding: utf-8 -*-
"""
India Class 10 Maths, NCERT Chapter 11: Areas Related to Circles (CBSE Unit VI Mensuration)
  python3 tools/gen_in_maths_c10_areas_related_to_circles.py
Circumference and area (π = 22/7), length of an arc, area of a sector, perimeter of a sector, area of a minor segment
for 60° and 90° (π = 3.14, √3 = 1.73), the major sector and major segment, and problems (clock hands, wipers, rings,
squares with quarter circles, wheels).
Wrong answers come from real mistakes: using 2πr for the sector area, θ/180 instead of θ/360, the diameter as the
radius, forgetting to subtract the triangle for a segment, and leaving out the two radii in the perimeter of a sector.
"""
import random
from fractions import Fraction as F
from in_common import num, S, make, lesson, mix, T, QN, People, svg_wrap, text, INK, RED, BLUE, FILL

R = random.Random(910011)
P = People(R)
PI = F(22, 7)
PI2 = F(314, 100)
RT3 = F(173, 100)
ANG = [30, 45, 60, 90, 120, 135, 150, 180, 210, 240, 270]


def a2(v, unit="cm²"):
    v = F(v)
    return "%s %s" % (num(v) if (v * 100).denominator == 1 else num(F(int(v * 100 + F(1, 2)), 100)), unit)


def sector_svg(ang, rlab):
    import math
    cx, cy, rr = 150, 120, 90
    a0 = 90 - ang / 2.0
    a1 = 90 + ang / 2.0
    P_ = lambda a: (cx + rr * math.cos(math.radians(a)), cy - rr * math.sin(math.radians(a)))
    x0, y0 = P_(a0)
    x1, y1 = P_(a1)
    s = ["<circle cx='%d' cy='%d' r='%d' fill='none' stroke='#999' stroke-width='1.6' stroke-dasharray='5 5'/>" % (cx, cy, rr),
         "<path d='M%d %d L%.1f %.1f A%d %d 0 %d 0 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2.4'/>" % (cx, cy, x0, y0, rr, rr, 1 if ang > 180 else 0, x1, y1, FILL, INK),
         "<circle cx='%d' cy='%d' r='3.5' fill='%s'/>" % (cx, cy, INK), text(cx - 10, cy + 20, "O", 15)]
    mx, my = (cx + x0) / 2, (cy + y0) / 2
    s.append(text(mx + 18, my + 14, rlab, 16, col=BLUE, anchor="start"))
    s.append(text(cx, cy - 26 if ang < 200 else cy - 30, "%d°" % ang, 15, col=RED))
    return svg_wrap(300, 240, "".join(s), "sector of a circle with angle %d degrees" % ang)


def r7(lo=1, hi=6):
    return 7 * R.randint(lo, hi)


# ---------------------------------------------------------------- set 1: circumference and area
def one_basic(r):
    kind = r.choice(["C", "A", "A", "wheel", "ring", "back"])
    rad = 7 * r.randint(1, 6) if r.random() < 0.7 else F(7 * r.randint(1, 5), 2)
    if kind == "C":
        v = 2 * PI * rad
        return QN("Find the circumference of a circle of radius %s cm. (Use π = 22/7.)" % num(rad), v, [PI * rad, PI * rad * rad, 4 * PI * rad],
                  "C = 2πr = 2 × 22/7 × %s = <b>%s cm</b>." % (num(rad), num(v)), unit=" cm")
    if kind == "A":
        v = PI * rad * rad
        return QN("Find the area of a circle of radius %s cm. (Use π = 22/7.)" % num(rad), v, [2 * PI * rad, PI * 4 * rad * rad, PI * rad * rad / 2],
                  "A = πr² = 22/7 × %s² = <b>%s cm²</b>." % (num(rad), num(v)), unit=" cm²")
    if kind == "wheel":
        d = 7 * r.choice([4, 6, 8, 10, 12])
        n = r.choice([10, 20, 25, 50, 100])
        v = PI * d * n / 100
        return QN("A wheel has a diameter of %d cm. How far does it travel in %d complete revolutions? (Use π = 22/7.)" % (d, n), v, [PI * d * n / 200, 2 * PI * d * n / 100, F(d * n, 100)],
                  "One revolution = πd = 22/7 × %d = %s cm. %d revolutions = %s cm = <b>%s m</b>." % (d, num(PI * d), n, num(PI * d * n), num(v)), unit=" m")
    if kind == "ring":
        R1 = 7 * r.randint(2, 6)
        r1 = R1 - 7 * r.randint(1, R1 // 7 - 1)
        v = PI * (R1 * R1 - r1 * r1)
        return QN("Find the area of a ring between two concentric circles of radii %d cm and %d cm. (Use π = 22/7.)" % (R1, r1), v, [PI * (R1 - r1) ** 2, 2 * PI * (R1 - r1), PI * R1 * R1],
                  "Area = π(R² − r²) = 22/7 × (%s − %s) = <b>%s cm²</b>." % (num(R1 * R1), num(r1 * r1), num(v)), unit=" cm²")
    rad = 7 * r.randint(1, 6)
    C = 2 * PI * rad
    return QN("The circumference of a circle is %s cm. Find its area. (Use π = 22/7.)" % num(C), PI * rad * rad, [C, PI * 4 * rad * rad, PI * rad * rad * 2],
              "2πr = %s gives r = %d cm. Area = 22/7 × %d² = <b>%s cm²</b>." % (num(C), rad, rad, num(PI * rad * rad)), unit=" cm²")


# ---------------------------------------------------------------- set 2: length of an arc
def one_arc(r):
    ang = r.choice(ANG)
    rad = 7 * r.randint(1, 6)
    v = F(ang, 360) * 2 * PI * rad
    if (v * 100).denominator != 1:
        return None
    kind = r.choice(["arc", "arc", "perim"])
    pic = sector_svg(ang, "%d cm" % rad)
    if kind == "arc":
        return QN(pic + "Find the length of the arc of a sector of angle %d° in a circle of radius %d cm. (Use π = 22/7.)" % (ang, rad), v,
                  [F(ang, 360) * PI * rad * rad, F(ang, 180) * 2 * PI * rad, F(ang, 360) * PI * rad],
                  "Arc = θ/360° × 2πr = %d/360 × 2 × 22/7 × %d = <b>%s cm</b>." % (ang, rad, num(v)), unit=" cm")
    return QN(pic + "Find the perimeter of a sector of angle %d° in a circle of radius %d cm. (Use π = 22/7.)" % (ang, rad), v + 2 * rad,
              [v, v + rad, F(ang, 360) * PI * rad * rad + 2 * rad],
              "Perimeter = arc + 2r = %s + 2 × %d = <b>%s cm</b>." % (num(v), rad, num(v + 2 * rad)), unit=" cm")


# ---------------------------------------------------------------- set 3: area of a sector
def one_sec(r):
    kind = r.choice(["sec", "sec", "major", "clock", "clock"])
    if kind in ("sec", "major"):
        ang = r.choice([30, 45, 60, 90, 120, 135, 150])
        rad = 7 * r.randint(1, 4) if r.random() < 0.7 else F(7 * r.randint(1, 5), 2)
        pic = sector_svg(ang, "%s cm" % num(rad))
        v = F(ang, 360) * PI * rad * rad
        if (v * 100).denominator != 1:
            return None
        if kind == "sec":
            return QN(pic + "Find the area of a sector of a circle with radius %s cm and angle %d°. (Use π = 22/7.)" % (num(rad), ang), v,
                      [F(ang, 360) * 2 * PI * rad, F(ang, 180) * PI * rad * rad, PI * rad * rad - v],
                      "Area = θ/360° × πr² = %d/360 × 22/7 × %s² = <b>%s cm²</b>." % (ang, num(rad), num(v)), unit=" cm²")
        return QN("Find the area of the major sector of a circle of radius %s cm when the minor sector has angle %d°. (Use π = 22/7.)" % (num(rad), ang), PI * rad * rad - v,
                  [v, F(360 - ang, 360) * 2 * PI * rad, PI * rad * rad], "Major sector = πr² − minor sector = %s − %s = <b>%s cm²</b>." % (num(PI * rad * rad), num(v), num(PI * rad * rad - v)), unit=" cm²")
    L = r.choice([7, 14, 21, 28])
    m = r.choice([5, 10, 15, 20, 30, 40, 45])
    v = F(m, 60) * PI * L * L
    name, he, his = P.next()
    if r.random() < 0.5:
        return QN("The minute hand of a clock is %d cm long. Find the area swept by it in %d minutes. (Use π = 22/7.)" % (L, m), v,
                  [F(m, 60) * 2 * PI * L, F(m, 360) * PI * L * L, F(m, 30) * PI * L * L],
                  "In %d minutes it turns %d° (%d/60 of a turn). Area = %d/60 × 22/7 × %d² = <b>%s cm²</b>." % (m, 6 * m, m, m, L, num(v)), unit=" cm²")
    ang = r.choice([90, 105, 115, 120])
    L2 = r.choice([21, 28, 35, 42])
    v = F(ang, 360) * PI * L2 * L2
    return QN("A car has a wiper %d cm long that sweeps through an angle of %d°. Find the area cleaned in one sweep. (Use π = 22/7.)" % (L2, ang), v,
              [F(ang, 360) * 2 * PI * L2, F(ang, 180) * PI * L2 * L2, PI * L2 * L2],
              "Sector area = %d/360 × 22/7 × %d² = <b>%s cm²</b>." % (ang, L2, num(v)), unit=" cm²")


# ---------------------------------------------------------------- set 4: area of a segment (60° and 90°)
def one_seg(r):
    ang = r.choice([60, 90, 90, 60])
    rad = r.choice([10, 12, 14, 15, 20, 21, 28])
    sec = F(ang, 360) * PI2 * rad * rad
    tri = F(rad * rad, 2) if ang == 90 else RT3 / 4 * rad * rad
    seg = sec - tri
    which = r.choice(["minor", "minor", "major"])
    tri_txt = "½ × %d × %d" % (rad, rad) if ang == 90 else "(√3/4) × %d²" % rad
    if which == "minor":
        return T("A chord of a circle of radius %d cm subtends an angle of %d° at the centre. Find the area of the minor segment. (Use π = 3.14%s.)" % (rad, ang, "" if ang == 90 else ", √3 = 1.73"),
                 a2(seg), [a2(sec), a2(sec + tri), a2(tri)],
                 "Segment = sector − triangle = %s − %s (%s) = <b>%s</b>." % (a2(sec), a2(tri), tri_txt, a2(seg)))
    full = PI2 * rad * rad
    return T("A chord of a circle of radius %d cm subtends an angle of %d° at the centre. Find the area of the major segment. (Use π = 3.14%s.)" % (rad, ang, "" if ang == 90 else ", √3 = 1.73"),
             a2(full - seg), [a2(seg), a2(full - sec), a2(full - tri)],
             "Minor segment = %s − %s = %s. Major segment = πr² − minor = %s − %s = <b>%s</b>." % (a2(sec), a2(tri), a2(seg), a2(full), a2(seg), a2(full - seg)))


# ---------------------------------------------------------------- set 5: problems
def one_prob(r):
    kind = r.choice(["square", "square", "track", "semi", "horse", "design"])
    if kind == "square":
        s = 14 * r.randint(1, 4)
        q = F(s, 2)
        v = s * s - PI * q * q
        return QN("From each corner of a square of side %d cm, a quadrant of radius %s cm is cut off. Find the area of the remaining part. (Use π = 22/7.)" % (s, num(q)), v,
                  [PI * q * q, s * s - F(1, 4) * PI * q * q, s * s - PI * s * s],
                  "Four quadrants make one full circle of radius %s cm: %d² − 22/7 × %s² = <b>%s cm²</b>." % (num(q), s, num(q), num(v)), unit=" cm²")
    if kind == "track":
        rad = 7 * r.randint(2, 6)
        w = 7 * r.randint(1, 3)
        name, he, his = P.next()
        v = PI * ((rad + w) ** 2 - rad * rad)
        return QN("A circular park of radius %d m has a path %d m wide around it on the outside. Find the area of the path. (Use π = 22/7.)" % (rad, w), v,
                  [PI * w * w, 2 * PI * w, PI * (rad + w) ** 2], "Path = π(R² − r²) = 22/7 × (%d² − %d²) = <b>%s m²</b>." % (rad + w, rad, num(v)), unit=" m²")
    if kind == "semi":
        d = 14 * r.randint(1, 4)
        v = F(1, 2) * PI * F(d, 2) ** 2
        p_ = PI * F(d, 2) + d
        if r.random() < 0.5:
            return QN("Find the area of a semicircle of diameter %d cm. (Use π = 22/7.)" % d, v, [PI * F(d, 2) ** 2, F(1, 2) * PI * d * d, PI * F(d, 2)],
                      "Area = ½ πr² with r = %d: ½ × 22/7 × %d² = <b>%s cm²</b>." % (d // 2, d // 2, num(v)), unit=" cm²")
        return QN("Find the perimeter of a semicircular protractor of diameter %d cm. (Use π = 22/7.)" % d, p_, [PI * F(d, 2), 2 * PI * F(d, 2), PI * d + d],
                  "Perimeter = πr + d = 22/7 × %d + %d = <b>%s cm</b>." % (d // 2, d, num(p_)), unit=" cm")
    if kind == "horse":
        rope = r.choice([5, 7, 10, 14])
        v = F(1, 4) * PI2 * rope * rope
        return T("A horse is tied to a peg at one corner of a square grass field of side 15 m with a rope %d m long. Find the area of the field it can graze. (Use π = 3.14.)" % rope,
                 a2(v, "m²"), [a2(PI2 * rope * rope, "m²"), a2(F(1, 2) * PI2 * rope * rope, "m²"), a2(F(1, 4) * 2 * PI2 * rope, "m²")],
                 "The corner angle is 90°, so it grazes a quadrant: ¼ × 3.14 × %d² = <b>%s</b>." % (rope, a2(v, "m²")))
    rad = 7 * r.randint(1, 4)
    v = PI * rad * rad / 4
    return QN("A brooch is made of a circle of radius %d mm divided into 4 equal sectors by 2 diameters. Find the area of each sector. (Use π = 22/7.)" % rad, v,
              [PI * rad * rad, 2 * PI * rad / 4, PI * rad * rad / 2],
              "Each sector is a quarter: ¼ × 22/7 × %d² = <b>%s mm²</b>." % (rad, num(v)), unit=" mm²")


def main():
    seen = set()
    sets = [
        S("Circumference and area", mix(R, [(one_basic, 20)], seen)),
        S("Length of an arc", mix(R, [(one_arc, 20)], seen)),
        S("Area of a sector", mix(R, [(one_sec, 20)], seen)),
        S("Area of a segment", mix(R, [(one_seg, 20)], seen)),
        S("Problems", mix(R, [(one_prob, 20)], seen)),
    ]
    body = lesson(
        "<p>A <b>sector</b> is the part of a circle between two radii. For angle θ: area = θ/360° × πr², arc length = θ/360° × 2πr.</p>"
        "<p>A <b>segment</b> is the part between a chord and its arc. Minor segment = sector − triangle. For 90° the triangle is ½r²; for 60° it is equilateral with area (√3/4)r².</p>"
        "<p>Major sector = πr² − minor sector. Use π = 22/7 when the radius is a multiple of 7.</p>",
        [("Find the area of a sector of angle 60° in a circle of radius 21 cm.", ["60/360 × 22/7 × 21²", "⅙ × 1,386"], "231 cm²"),
         ("Find the area of the minor segment for a 90° chord in a circle of radius 10 cm (π = 3.14).", ["Sector = ¼ × 3.14 × 100 = 78.5", "Triangle = ½ × 10 × 10 = 50"], "28.5 cm²")],
        ["Using 2πr for the area of a sector. Area uses πr², arc length uses 2πr.",
         "Using θ/180 instead of θ/360.",
         "Forgetting the two radii when finding the perimeter of a sector: perimeter = arc + 2r."])
    faq = [
        ("What is the formula for the area of a sector?", "Area of a sector of angle θ = θ/360° × πr²."),
        ("What is the formula for the length of an arc?", "Length of the arc of a sector of angle θ = θ/360° × 2πr."),
        ("How do I find the area of a segment of a circle?", "Area of the minor segment = area of the sector − area of the triangle formed by the two radii and the chord."),
        ("What is the difference between a sector and a segment?", "A sector is bounded by two radii and an arc; a segment is bounded by a chord and an arc."),
    ]
    make(10, "areas-related-to-circles", 11, "VI", 11, "Areas Related to Circles: Sectors and Segments", "areas related to circles",
         "Area of sectors and segments of a circle; problems based on areas and perimeter / circumference of the above said plane figures; in calculating the area of a segment of a circle, problems are restricted to central angles of 60° and 90° only (summary of the CBSE syllabus)",
         "Class 10 Areas Related to Circles worksheet (NCERT Chapter 11): circumference and area, arc length, area of a sector, segments for 60° and 90°, and problems. 100 questions with answers.",
         "Sector area = θ/360° × πr²", "Arc length = θ/360° × 2πr. Segment = sector − triangle.",
         body, faq, sets, R)


if __name__ == "__main__":
    main()
