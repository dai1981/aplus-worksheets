# -*- coding: utf-8 -*-
"""
UK Year 8 Maths: Circles — Circumference and Area (KS3 Geometry and measures)
  python3 tools/gen_uk_maths_y8_circles.py
Parts of a circle, circumference and area from the radius or diameter (to 1 decimal place and in terms
of π), finding the radius from the circumference or area, and semicircles and wheels.
Wrong answers come from real mistakes: using the diameter in πr², mixing up 2πr and πr², squaring
π × r instead of r, and forgetting the straight edge of a semicircle.
"""
import math
import random
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F
from uk_ks3 import num, mcq, B, S, make, lesson, collect, T, svg_wrap, line, text, fig, GREEN, INK, RED

R = random.Random(81101)
PI = "<i>π</i>"


def r1(x):
    return Decimal(str(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def d1(x):
    v = r1(x)
    s = "{:,.1f}".format(float(v))
    return s


def circ_svg(rad=None, dia=None):
    cx, cy, R0 = 110, 100, 75
    s = ["<circle cx='%d' cy='%d' r='%d' fill='#eef6f0' stroke='%s' stroke-width='2.5'/>" % (cx, cy, R0, INK),
         "<circle cx='%d' cy='%d' r='3' fill='%s'/>" % (cx, cy, INK)]
    if rad is not None:
        s.append(line(cx, cy, cx + R0, cy, RED, 2.5))
        s.append(text(cx + R0 / 2, cy - 8, rad, 15, col=RED))
    if dia is not None:
        s.append(line(cx - R0, cy, cx + R0, cy, RED, 2.5))
        s.append(text(cx, cy - 8, dia, 15, col=RED))
    return svg_wrap(220, 200, "".join(s), "circle")


def QD(q, val, wrongs, e, unit):
    """Answer rounded to 1 dp."""
    right = d1(val) + unit
    cands = []
    for w in wrongs:
        if w is None:
            continue
        t = d1(w) + unit
        if t != right:
            cands.append((t, t))
    cands.append((d1(val * 1.1) + unit, "x1"))
    cands.append((d1(val * 0.9) + unit, "x2"))
    return mcq(q, (right, right), cands, e)


# ------------------------------------------------------------ set 1: parts of a circle
PARTS = [
    ("the distance from the centre to the edge", "Radius"),
    ("the distance across the circle through the centre", "Diameter"),
    ("the distance all the way round the circle", "Circumference"),
    ("a straight line joining two points on the circle (not through the centre)", "Chord"),
    ("part of the circumference", "Arc"),
    ("a straight line that touches the circle at one point", "Tangent"),
    ("the region between two radii and an arc (like a slice of pizza)", "Sector"),
    ("the region between a chord and an arc", "Segment"),
]


def one_parts(r):
    if r.random() < 0.55:
        desc, name = r.choice(PARTS)
        others = [n for _, n in PARTS if n != name]
        r.shuffle(others)
        return T("What is the name for %s?" % B(desc), name, others[:3], "This is the <b>%s</b>." % name.lower())
    rad = r.choice([F(r.randint(2, 30)), F(r.randint(11, 99), 10)])
    if r.random() < 0.5:
        q = "A circle has a radius of %s cm. What is its diameter?" % num(rad)
        return mcq(q, (num(rad * 2) + " cm", rad * 2), [(num(w) + " cm", w) for w in [rad / 2, rad + 2, rad * rad] if w != rad * 2] + [(num(rad * 4) + " cm", rad * 4)],
                   "The diameter is twice the radius: <b>%s cm</b>." % num(rad * 2))
    q = "A circle has a diameter of %s cm. What is its radius?" % num(rad * 2)
    return mcq(q, (num(rad) + " cm", rad), [(num(w) + " cm", w) for w in [rad * 4, rad * 2 + 2, rad * 2 - 1] if w != rad and w > 0], "The radius is half the diameter: <b>%s cm</b>." % num(rad))


# ------------------------------------------------------------ set 2: circumference
def one_circ(r):
    v = r.randint(2, 25)
    use_d = r.random() < 0.5
    if use_d:
        C = math.pi * v
        q = "Find the circumference of a circle with diameter %d cm. Give your answer to 1 decimal place.%s" % (v, fig(circ_svg(dia="%d cm" % v)))
        e = "<i>C</i> = %s<i>d</i> = %s × %d = %s… = <b>%s cm</b>." % (PI, PI, v, "{:.3f}".format(C), d1(C))
        return QD(q, C, [math.pi * v * 2, math.pi * (v / 2) ** 2, math.pi * v * v], e, " cm")
    C = 2 * math.pi * v
    q = "Find the circumference of a circle with radius %d cm. Give your answer to 1 decimal place.%s" % (v, fig(circ_svg(rad="%d cm" % v)))
    e = "<i>C</i> = 2%s<i>r</i> = 2 × %s × %d = %s… = <b>%s cm</b>." % (PI, PI, v, "{:.3f}".format(C), d1(C))
    return QD(q, C, [math.pi * v, math.pi * v * v, 2 * math.pi * v * v], e, " cm")


# ------------------------------------------------------------ set 3: area
def one_area(r):
    v = r.randint(2, 20)
    use_d = r.random() < 0.4
    if use_d:
        d = 2 * v
        A = math.pi * v * v
        q = "Find the area of a circle with diameter %d cm. Give your answer to 1 decimal place.%s" % (d, fig(circ_svg(dia="%d cm" % d)))
        e = "Radius = %d ÷ 2 = %d cm. <i>A</i> = %s<i>r</i>² = %s × %d² = <b>%s cm²</b>." % (d, v, PI, PI, v, d1(A))
        return QD(q, A, [math.pi * d * d, math.pi * d, (math.pi * v) ** 2], e, " cm²")
    A = math.pi * v * v
    q = "Find the area of a circle with radius %d cm. Give your answer to 1 decimal place.%s" % (v, fig(circ_svg(rad="%d cm" % v)))
    e = "<i>A</i> = %s<i>r</i>² = %s × %d² = %s × %d = <b>%s cm²</b>." % (PI, PI, v, PI, v * v, d1(A))
    return QD(q, A, [2 * math.pi * v, (math.pi * v) ** 2, math.pi * (2 * v) ** 2], e, " cm²")


# ------------------------------------------------------------ set 4: in terms of π and reverse problems
def one_pi(r):
    kind = r.randint(0, 3)
    v = r.randint(2, 12)
    if kind == 0:
        q = "Find the area of a circle with radius %d cm. Give your answer in terms of %s." % (v, PI)
        right = "%d%s cm²" % (v * v, PI)
        return T(q, right, ["%d%s cm²" % (2 * v, PI), "%d%s cm²" % (4 * v * v, PI), "%d%s<sup>2</sup> cm²" % (v, PI)], "<i>A</i> = %s × %d² = <b>%s</b>." % (PI, v, right))
    if kind == 1:
        q = "Find the circumference of a circle with radius %d cm. Give your answer in terms of %s." % (v, PI)
        right = "%d%s cm" % (2 * v, PI)
        return T(q, right, ["%d%s cm" % (v, PI), "%d%s cm" % (v * v, PI), "%d%s cm" % (4 * v, PI)], "<i>C</i> = 2 × %s × %d = <b>%s</b>." % (PI, v, right))
    if kind == 2:
        q = "A circle has an area of %d%s cm². What is its radius?" % (v * v, PI)
        return T(q, "%d cm" % v, ["%d cm" % (v * v // 2) if v * v // 2 != v else "%d cm" % (v + 1), "%d cm" % (2 * v), "%d cm" % (v * v)], "%s<i>r</i>² = %d%s, so <i>r</i>² = %d and <i>r</i> = <b>%d cm</b>." % (PI, v * v, PI, v * v, v))
    C = r.choice([31.4, 62.8, 50, 100, 25.1, 44])
    rad = C / (2 * math.pi)
    q = "A circle has a circumference of %s cm. Find its radius to 1 decimal place." % num(F(str(C)))
    e = "<i>r</i> = <i>C</i> ÷ 2%s = %s ÷ (2 × %s) = <b>%s cm</b>." % (PI, num(F(str(C))), PI, d1(rad))
    return QD(q, rad, [C / math.pi, math.sqrt(C / math.pi), C / 2], e, " cm")


# ------------------------------------------------------------ set 5: problems
def semi_svg():
    s = ["<path d='M30 130 A90 90 0 0 1 210 130 Z' fill='#eef6f0' stroke='%s' stroke-width='2.5'/>" % INK,
         text(120, 150, "10 cm", 15, col=RED)]
    return svg_wrap(240, 160, "".join(s), "semicircle with diameter 10 cm")


def problems():
    its = []
    data = [
        ("A semicircle has a diameter of 10 cm. Find its perimeter to 1 decimal place.%s" % fig(semi_svg()), "25.7 cm", ["15.7 cm", "31.4 cm", "39.3 cm"],
         "Curved part = ½ × %s × 10 = 15.7… cm. Add the straight edge: 15.7 + 10 = <b>25.7 cm</b>." % PI),
        ("A semicircle has a diameter of 10 cm. Find its area to 1 decimal place.%s" % fig(semi_svg()), "39.3 cm²", ["78.5 cm²", "157.1 cm²", "15.7 cm²"],
         "Radius 5 cm. ½ × %s × 5² = <b>39.3 cm²</b>." % PI),
        ("A bicycle wheel has a diameter of 70 cm. How far does it travel in one full turn, to the nearest cm?", "220 cm", ["440 cm", "110 cm", "3,848 cm"], "%s × 70 = 219.9… ≈ <b>220 cm</b>." % PI),
        ("A bicycle wheel has a diameter of 70 cm. About how many full turns does it make in 1 km?", "455", ["45", "4,547", "1,429"], "1 km = 100,000 cm. 100,000 ÷ 219.9 ≈ 454.7, so <b>455</b> turns."),
        ("A circular pond has a radius of 3 m. What is its area to 1 decimal place?", "28.3 m²", ["18.8 m²", "9.4 m²", "113.1 m²"], "%s × 3² = 28.27… ≈ <b>28.3 m²</b>." % PI),
        ("A circular table top has a diameter of 1.2 m. What is its area to 2 decimal places?", "1.13 m²", ["4.52 m²", "3.77 m²", "1.88 m²"], "Radius 0.6 m. %s × 0.6² = <b>1.13 m²</b>." % PI),
        ("A running track is a circle with radius 50 m. How many metres is one lap, to the nearest metre?", "314 m", ["157 m", "7,854 m", "100 m"], "2 × %s × 50 = 314.15… ≈ <b>314 m</b>." % PI),
        ("A pizza has diameter 30 cm. Another has diameter 20 cm. Roughly how many times bigger is the area of the larger pizza?", "2.25 times", ["1.5 times", "3 times", "10 times"],
         "Areas are %s × 15² and %s × 10²: 225 ÷ 100 = <b>2.25 times</b>." % (PI, PI)),
        ("If the radius of a circle doubles, what happens to the circumference?", "It doubles", ["It is multiplied by 4", "It stays the same", "It halves"], "<i>C</i> = 2%s<i>r</i>, so it <b>doubles</b>." % PI),
        ("If the radius of a circle doubles, what happens to the area?", "It is multiplied by 4", ["It doubles", "It is multiplied by 8", "It stays the same"], "<i>A</i> = %s<i>r</i>²; (2<i>r</i>)² = 4<i>r</i>², so it is <b>multiplied by 4</b>." % PI),
        ("A square of side 10 cm has a circle of diameter 10 cm cut out of it. What area is left, to 1 decimal place?", "21.5 cm²", ["78.5 cm²", "68.6 cm²", "31.4 cm²"], "100 − %s × 5² = 100 − 78.5 = <b>21.5 cm²</b>." % PI),
        ("A quarter circle has radius 8 cm. What is its area to 1 decimal place?", "50.3 cm²", ["201.1 cm²", "12.6 cm²", "100.5 cm²"], "¼ × %s × 8² = <b>50.3 cm²</b>." % PI),
        ("Which is the formula for the area of a circle?", "%s<i>r</i>²" % PI, ["2%s<i>r</i>" % PI, "%s<i>d</i>" % PI, "(%s<i>r</i>)²" % PI], "The area is <b>%s<i>r</i>²</b>; 2%s<i>r</i> and %s<i>d</i> are the circumference." % (PI, PI, PI)),
        ("What is the value of %s to 2 decimal places?" % PI, "3.14", ["3.41", "3.12", "22.7"], "%s = 3.14159…, which is <b>3.14</b> to 2 d.p." % PI),
        ("A circle has a circumference of 18%s cm. What is its diameter?" % PI, "18 cm", ["9 cm", "36 cm", "18%s cm" % PI], "<i>C</i> = %s<i>d</i> = 18%s, so <i>d</i> = <b>18 cm</b>." % (PI, PI)),
        ("A circular garden has area 154 m². Using %s ≈ 22/7, what is its radius?" % PI, "7 m", ["49 m", "14 m", "24.5 m"], "<i>r</i>² = 154 ÷ 22/7 = 49, so <i>r</i> = <b>7 m</b>."),
        ("A clock's minute hand is 12 cm long. How far does its tip travel in one hour, to 1 decimal place?", "75.4 cm", ["37.7 cm", "452.4 cm", "24 cm"], "One full circle: 2 × %s × 12 = <b>75.4 cm</b>." % PI),
        ("A circle fits exactly inside a square of side 6 cm. What is the circle's area in terms of %s?" % PI, "9%s cm²" % PI, ["36%s cm²" % PI, "6%s cm²" % PI, "3%s cm²" % PI], "The diameter is 6, so <i>r</i> = 3 and <i>A</i> = <b>9%s cm²</b>." % PI),
        ("A ring is made from two circles with radii 5 cm and 3 cm. What is the area of the ring in terms of %s?" % PI, "16%s cm²" % PI, ["4%s cm²" % PI, "34%s cm²" % PI, "2%s cm²" % PI], "%s × 5² − %s × 3² = 25%s − 9%s = <b>16%s cm²</b>." % (PI, PI, PI, PI, PI)),
        ("Which unit is the area of a circle measured in?", "cm²", ["cm", "cm³", "degrees"], "Area is measured in <b>square units</b> such as cm²."),
    ]
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p>The <b>radius</b> <i>r</i> goes from the centre to the edge; the <b>diameter</b> <i>d</i> = 2<i>r</i> goes right across.</p>"
        "<ul><li>Circumference: <b><i>C</i> = π<i>d</i></b> or <b><i>C</i> = 2π<i>r</i></b></li>"
        "<li>Area: <b><i>A</i> = π<i>r</i>²</b> (always use the radius)</li></ul>"
        "<p>Use the π button on a calculator and round at the end, or give an exact answer “in terms of π”, such as 25π.</p>"
        + fig(circ_svg(rad="r")),
        [("Find the circumference of a circle with diameter 8 cm.", ["π × 8 = 25.13…"], "25.1 cm"),
         ("Find the area of a circle with diameter 8 cm.", ["Radius = 4 cm.", "π × 4² = 16π = 50.26…"], "50.3 cm²")],
        ["Using the diameter in π<i>r</i>²: with <i>d</i> = 8, the area is π × 4², not π × 8².",
         "Mixing up the formulae: 2π<i>r</i> is the circumference, π<i>r</i>² is the area.",
         "Squaring π × <i>r</i> instead of just <i>r</i>.",
         "For a semicircle's perimeter, forgetting to add the straight diameter."])


def main():
    sets = [S("Parts of a circle", collect(one_parts, 20, R)),
            S("Circumference", collect(one_circ, 20, R)),
            S("Area", collect(one_area, 20, R)),
            S("In terms of π and working backwards", collect(one_pi, 20, R)),
            S("Problems", problems())]
    make(8, "circles", 11, "G",
         "Circles: Circumference and Area",
         "Year 8 Circles Worksheets: Parts of a Circle, Circumference, Area, Semicircles and π",
         "Circles",
         "Calculate and solve problems involving perimeters of 2-D shapes (including circles), areas of circles and "
         "composite shapes; know the formulae: circumference of a circle = 2πr = πd, area of a circle = πr².",
         "Free Year 8 circles worksheets with diagrams: parts of a circle, circumference and area to 1 decimal place and "
         "in terms of π, finding the radius, semicircles and wheels. 100 questions with answers.",
         "Circumference = πd = 2πr. Area = πr².",
         "Always use the radius for the area. Halve the diameter first if you need to.",
         body(),
         [("What is the formula for the circumference of a circle?", "C = πd, or C = 2πr, where d is the diameter and r is the radius."),
          ("What is the formula for the area of a circle?", "A = πr². Square the radius first, then multiply by π."),
          ("What does “in terms of π” mean?", "Leave π as a symbol instead of using its decimal value. A circle with radius 5 has area 25π cm²."),
          ("How do I find the perimeter of a semicircle?", "Half of πd for the curved part, plus the diameter for the straight edge.")],
         sets, R)


if __name__ == "__main__":
    main()
