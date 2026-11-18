# -*- coding: utf-8 -*-
"""
SG Secondary 3 Maths: Arc Length, Sector Area and Radians (MOE syllabus G5: arc length, sector area and area of a
segment of a circle; radian measure of angle, including conversion between radians and degrees)
  python3 tools/gen_sg_maths_s3_arc_length_sector_area_and_radians.py
Converting between degrees and radians, arc length (θ/360 × 2πr and s = rθ), sector area (θ/360 × πr² and ½r²θ),
segment area (sector minus triangle) and problems (perimeter of a sector, finding the angle or radius).
Answers are correct to 3 significant figures, as in O-Level papers.
Wrong answers come from real mistakes: using πr² for arc length, using the diameter as the radius, mixing
degree and radian formulas, forgetting the two radii in a perimeter, and subtracting the wrong triangle.
"""
import math
import random
from fractions import Fraction as F
from sg_sec import num, S, make, lesson, collect, T, fr, MINUS

R = random.Random(831400)
PI = math.pi


def sf3(x):
    if x == 0:
        return "0"
    d = 2 - int(math.floor(math.log10(abs(x))))
    v = round(x, d)
    s = ("%.*f" % (max(d, 0), v)) if d > 0 else num(int(round(v)))
    return s.replace("-", MINUS)


def pfrac(f):
    """f × π as HTML, e.g. 2π/3"""
    f = F(f)
    top = ("" if f.numerator == 1 else num(f.numerator)) + "π"
    return top if f.denominator == 1 else fr(top, num(f.denominator))


def ang_from_rad(f):
    return F(f) * 180


NICE = [F(1, 6), F(1, 4), F(1, 3), F(1, 2), F(2, 3), F(3, 4), F(5, 6), F(1), F(7, 6), F(5, 4), F(4, 3), F(3, 2), F(5, 3), F(7, 4), F(2), F(1, 12), F(5, 12)]


# ------------------------------------------------------------ set 1: degrees and radians
def one_conv(r):
    kind = r.choice(["d2r", "d2r", "r2d", "r2d", "dec"])
    f = r.choice(NICE)
    deg = ang_from_rad(f)
    if kind == "d2r":
        q = "Convert %s° to radians, giving your answer in terms of π." % num(deg)
        right = pfrac(f)
        wr = [pfrac(F(deg, 360)) if F(deg, 360) != f else pfrac(f * 2), pfrac(1 / f) if 1 / f != f else pfrac(f * 3), pfrac(f * 2) if f * 2 != F(deg, 360) else pfrac(f / 2)]
        return T(q, right, wr, "Multiply by π/180: %s × π ÷ 180 = <b>%s</b>." % (num(deg), right))
    if kind == "r2d":
        q = "Convert %s radians to degrees." % pfrac(f)
        return T(q, "%s°" % num(deg), ["%s°" % num(deg * 2), "%s°" % num(F(deg, 2)), "%s°" % sf3(float(f) * 180 / PI) if abs(float(f) * 180 / PI - float(deg)) > 1 else "%s°" % num(deg + 90)],
                 "π radians = 180°, so %s = %s × 180° = <b>%s°</b>." % (pfrac(f), num(f) if f.denominator == 1 else fr(num(f.numerator), num(f.denominator)), num(deg)))
    x = r.choice([0.5, 1, 1.2, 1.5, 2, 2.5, 0.8, 3])
    q = "Convert %s radians to degrees, correct to 1 decimal place." % ("%g" % x)
    d = x * 180 / PI
    return T(q, "%.1f°" % d, ["%.1f°" % (x * PI / 180) if x * PI / 180 > 0.05 else "%.1f°" % (x * 90), "%.1f°" % (x * 180), "%.1f°" % (x * 360 / PI)],
             "Multiply by 180/π: %s × 180 ÷ π = <b>%.1f°</b>. (1 radian ≈ 57.3°.)" % ("%g" % x, d))


# ------------------------------------------------------------ set 2: arc length
def one_arc(r):
    rr = r.randint(3, 20)
    if r.random() < 0.5:
        th = r.choice([30, 40, 45, 60, 72, 80, 90, 100, 120, 135, 150, 210, 240, 270])
        s = th / 360 * 2 * PI * rr
        q = "A sector has radius %d cm and angle %d°. Find the arc length, correct to 3 significant figures." % (rr, th)
        return T(q, "%s cm" % sf3(s), ["%s cm" % sf3(th / 360 * PI * rr * rr), "%s cm" % sf3(th / 360 * PI * rr), "%s cm" % sf3(s + 2 * rr)],
                 "Arc length = %d/360 × 2π × %d = <b>%s cm</b>." % (th, rr, sf3(s)))
    th = r.choice([0.4, 0.6, 0.8, 1.2, 1.5, 2, 2.4, 0.9])
    s = rr * th
    q = "A sector has radius %d cm and angle %s radians. Find the arc length." % (rr, "%g" % th)
    return T(q, "%s cm" % ("%g" % s), ["%s cm" % sf3(0.5 * rr * rr * th), "%s cm" % sf3(th / 360 * 2 * PI * rr), "%s cm" % ("%g" % (s + 2 * rr))],
             "In radians, <i>s</i> = <i>r</i>θ = %d × %s = <b>%s cm</b>." % (rr, "%g" % th, "%g" % s))


# ------------------------------------------------------------ set 3: sector area
def one_sector(r):
    rr = r.randint(3, 18)
    if r.random() < 0.5:
        th = r.choice([30, 40, 45, 60, 72, 80, 90, 100, 120, 135, 150, 216, 240, 300])
        A = th / 360 * PI * rr * rr
        q = "Find the area of a sector with radius %d cm and angle %d°, correct to 3 significant figures." % (rr, th)
        return T(q, "%s cm²" % sf3(A), ["%s cm²" % sf3(th / 360 * 2 * PI * rr), "%s cm²" % sf3(th / 360 * PI * (2 * rr) ** 2), "%s cm²" % sf3(0.5 * rr * rr * th)],
                 "Sector area = %d/360 × π × %d² = <b>%s cm²</b>." % (th, rr, sf3(A)))
    f = r.choice([F(1, 3), F(1, 2), F(2, 3), F(3, 4), F(5, 6), F(1, 4)])
    th = float(f) * PI
    A = 0.5 * rr * rr * th
    q = "Find the area of a sector with radius %d cm and angle %s radians, correct to 3 significant figures." % (rr, pfrac(f))
    return T(q, "%s cm²" % sf3(A), ["%s cm²" % sf3(rr * rr * th), "%s cm²" % sf3(rr * th), "%s cm²" % sf3(0.5 * rr * th)],
             "Sector area = ½<i>r</i>²θ = ½ × %d² × %s = <b>%s cm²</b>." % (rr, pfrac(f), sf3(A)))


# ------------------------------------------------------------ set 4: segment area
def one_segment(r):
    rr = r.randint(4, 15)
    if r.random() < 0.5:
        th = r.choice([60, 90, 120, 100, 80, 150, 45])
        sec = th / 360 * PI * rr * rr
        tri = 0.5 * rr * rr * math.sin(math.radians(th))
        seg = sec - tri
        q = "A chord cuts off a minor segment from a circle of radius %d cm. The angle at the centre is %d°. Find the area of the segment, correct to 3 significant figures." % (rr, th)
        return T(q, "%s cm²" % sf3(seg), ["%s cm²" % sf3(sec), "%s cm²" % sf3(sec + tri), "%s cm²" % sf3(sec - 0.5 * rr * rr)],
                 "Sector = %d/360 × π × %d² = %s. Triangle = ½ × %d² × sin %d° = %s. Segment = <b>%s cm²</b>." % (th, rr, sf3(sec), rr, th, sf3(tri), sf3(seg)))
    th = r.choice([0.8, 1, 1.2, 1.5, 2, 2.5])
    sec = 0.5 * rr * rr * th
    tri = 0.5 * rr * rr * math.sin(th)
    seg = sec - tri
    q = "The angle at the centre of a minor segment is %s radians and the radius is %d cm. Find the area of the segment, correct to 3 significant figures." % ("%g" % th, rr)
    return T(q, "%s cm²" % sf3(seg), ["%s cm²" % sf3(sec), "%s cm²" % sf3(sec - 0.5 * rr * rr * math.sin(math.radians(th))), "%s cm²" % sf3(sec + tri)],
             "Area = ½<i>r</i>²(θ − sin θ) with θ in radians = ½ × %d² × (%s − sin %s) = <b>%s cm²</b>. (Set your calculator to radians.)" % (rr, "%g" % th, "%g" % th, sf3(seg)))


# ------------------------------------------------------------ set 5: problems
def one_prob(r):
    kind = r.choice(["perim", "perim", "angle", "radius", "minute", "pizza"])
    if kind == "perim":
        rr = r.randint(4, 15)
        th = r.choice([0.6, 0.8, 1.2, 1.5, 2, 2.5])
        P_ = 2 * rr + rr * th
        q = "Find the perimeter of a sector with radius %d cm and angle %s radians." % (rr, "%g" % th)
        return T(q, "%s cm" % ("%g" % round(P_, 4)), ["%s cm" % ("%g" % round(rr * th, 4)), "%s cm" % ("%g" % round(rr + rr * th, 4)), "%s cm" % sf3(0.5 * rr * rr * th + 2 * rr)],
                 "Perimeter = two radii + arc = 2 × %d + %d × %s = <b>%s cm</b>." % (rr, rr, "%g" % th, "%g" % round(P_, 4)))
    if kind == "angle":
        rr = r.randint(4, 12)
        s = rr * r.choice([0.5, 0.75, 1.2, 1.5, 2, 2.5])
        th = s / rr
        q = "An arc of length %s cm subtends an angle of θ radians at the centre of a circle of radius %d cm. Find θ." % ("%g" % s, rr)
        return T(q, "%g" % th, ["%g" % (s * rr), sf3(s / (2 * PI * rr) * 360), "%g" % round(s / (2 * rr), 4)],
                 "<i>s</i> = <i>r</i>θ, so θ = %s ÷ %d = <b>%s</b> radians." % ("%g" % s, rr, "%g" % th))
    if kind == "radius":
        th = r.choice([F(1, 2), F(2, 3), F(3, 4), F(1, 3)])
        rr = r.randint(4, 12)
        A = F(1, 2) * rr * rr * th
        q = "A sector with angle %s radians has an area of %s cm². Find its radius." % (fr(num(th.numerator), num(th.denominator)), num(A) if A.denominator == 1 else fr(num(A.numerator), num(A.denominator)))
        return T(q, "%d cm" % rr, ["%d cm" % (rr * rr) if rr * rr < 200 else "%d cm" % (rr + 2), "%s cm" % sf3(math.sqrt(float(A) / float(th))), "%s cm" % sf3(float(A) / float(th))],
                 "½<i>r</i>²θ = A, so <i>r</i>² = 2A ÷ θ = %s and <i>r</i> = <b>%d cm</b>." % (num(rr * rr), rr))
    if kind == "minute":
        L = r.randint(8, 20)
        m = r.choice([10, 15, 20, 25, 40, 45])
        s = m / 60 * 2 * PI * L
        q = "The minute hand of a clock is %d cm long. How far does its tip move in %d minutes, correct to 3 significant figures?" % (L, m)
        return T(q, "%s cm" % sf3(s), ["%s cm" % sf3(m / 60 * PI * L * L), "%s cm" % sf3(m / 60 * PI * L), "%s cm" % sf3(m / 12 * 2 * PI * L / 60 * 5)] if abs(m / 12 * 2 * PI * L / 60 * 5 - s) > 0.01 else ["%s cm" % sf3(m / 60 * PI * L * L), "%s cm" % sf3(m / 60 * PI * L), "%s cm" % sf3(s * 2)],
                 "In %d minutes the hand turns %d/60 of a full circle: %d/60 × 2π × %d = <b>%s cm</b>." % (m, m, m, L, sf3(s)))
    rr = r.randint(12, 20)
    n = r.choice([6, 8, 10, 12])
    th = 360 / n
    A = PI * rr * rr / n
    q = "A round cake of radius %d cm is cut into %d equal sectors. Find the area of the top of one piece, correct to 3 significant figures." % (rr, n)
    return T(q, "%s cm²" % sf3(A), ["%s cm²" % sf3(2 * PI * rr / n), "%s cm²" % sf3(PI * rr * rr), "%s cm²" % sf3(PI * (rr / 2) ** 2 / n)],
             "Each sector has angle 360° ÷ %d = %s°. Area = πr² ÷ %d = π × %d² ÷ %d = <b>%s cm²</b>." % (n, "%g" % th, n, rr, n, sf3(A)))


def build():
    sets = [S("Degrees and radians", collect(one_conv, 20, R)),
            S("Arc length", collect(one_arc, 20, R)),
            S("Area of a sector", collect(one_sector, 20, R)),
            S("Area of a segment", collect(one_segment, 20, R)),
            S("Problems", collect(one_prob, 20, R))]
    body = lesson(
        "<ul><li><b>π radians = 180°.</b> Degrees → radians: × π/180. Radians → degrees: × 180/π.</li>"
        "<li>Arc length = θ/360 × 2π<i>r</i> (degrees) or <b><i>s</i> = <i>r</i>θ</b> (radians).</li>"
        "<li>Sector area = θ/360 × π<i>r</i>² (degrees) or <b>½<i>r</i>²θ</b> (radians).</li>"
        "<li>Segment area = sector area − triangle area = ½<i>r</i>²θ − ½<i>r</i>² sin θ.</li></ul>",
        [("Convert 135° to radians.", ["135 × π ÷ 180"], "3π/4"),
         ("A sector has radius 6 cm and angle 1.2 rad. Find its area and perimeter.", ["Area = ½ × 36 × 1.2 = 21.6 cm²", "Arc = 6 × 1.2 = 7.2 cm, perimeter = 6 + 6 + 7.2"], "21.6 cm² and 19.2 cm")],
        ["Using the radian formulas with an angle in degrees (or the other way round).",
         "Using 2πr for an area or πr² for a length.",
         "Forgetting the two radii when finding the perimeter of a sector.",
         "Leaving the calculator in degree mode when working out sin θ for θ in radians."])
    faq = [("What is a radian?", "The angle at the centre of a circle when the arc length equals the radius. 2π radians make a full turn, so π radians = 180° and 1 radian ≈ 57.3°."),
           ("What are the arc length and sector area formulas in radians?", "Arc length s = rθ and sector area = ½r²θ, where θ is in radians."),
           ("How do you find the area of a segment?", "Subtract the area of the triangle formed by the two radii and the chord, ½r² sin θ, from the area of the sector."),
           ("How do you find the perimeter of a sector?", "Add the two radii to the arc length: 2r + rθ.")]
    make(3, "arc-length-sector-area-and-radians", 14, "G5",
         "Arc Length, Sector Area and Radians",
         "", "Arc length, sector area and radians", "",
         "Free Secondary 3 maths worksheets on radian measure, converting between degrees and radians, arc length, sector area, segment area and perimeter of a sector. 100 questions with answers.",
         "In radians, arc length s = rθ and sector area = ½r²θ.",
         "π radians = 180°. Segment area = sector area − triangle area.",
         body, faq, sets, R)


if __name__ == "__main__":
    build()
