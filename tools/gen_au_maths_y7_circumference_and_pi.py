# -*- coding: utf-8 -*-
"""
AU Year 7 Maths: Circumference and pi (Australian Curriculum v9.0: AC9M7M03)
  python3 tools/gen_au_maths_y7_circumference_and_pi.py
The parts of a circle, radius and diameter, why circumference ÷ diameter is always π, finding the circumference
from the diameter or radius, working back from the circumference, and practical problems. Diagrams are inline SVG.
Wrong answers come from real mistakes: using the radius in C = πd, doubling twice, dividing by π the wrong way,
and confusing the circumference with the area.
"""
import math
import random
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F
from au_hs import comma, num, mcq, B, S, make, lesson, collect, T, QN, svg_wrap, line, text, fig, GREEN, INK, RED

R = random.Random(71501)
PI = "<i>π</i>"


def r1(x):
    return Decimal(str(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def d1(x):
    v = r1(x)
    whole, _, frac_ = ("%.1f" % float(v)).partition(".")
    return comma(int(whole)) + "." + frac_


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




# ------------------------------------------------------------ set 2: π as circumference ÷ diameter
OBJECTS = [("a dinner plate", 26), ("a bucket", 30), ("a bike wheel", 66), ("a hula hoop", 90), ("a cricket ball", F(72, 10)),
           ("a mug", 8), ("a tree trunk", 40), ("a round table", 120), ("a clock face", 30), ("a frisbee", 27)]


def one_ratio(r):
    kind = r.choice(["ratio", "ratio", "fact", "est"])
    if kind == "ratio":
        name, d = r.choice(OBJECTS)
        d = F(d)
        C = F(str(round(math.pi * float(d) + r.uniform(-0.15, 0.15), 1)))
        q = "Mei measures %s. Its circumference is %s cm and its diameter is %s cm. What is circumference ÷ diameter, to 2 decimal places?" % (name, num(C), num(d))
        val = float(C / d)
        right = "%.2f" % val
        wr = ["%.2f" % (float(d / C)), "%.2f" % (val * 2), "%.2f" % (val / 2)]
        return T(q, right, [w for w in dict.fromkeys(wr) if w != right], "%s ÷ %s = %s…, which is close to π = 3.14. This is true for every circle." % (num(C), num(d), "%.3f" % val))
    if kind == "fact":
        facts = [("For every circle, circumference ÷ diameter is…", "π, about 3.14", ["2", "about 6.28", "different for every circle"],
                  "Circumference ÷ diameter is always the same number: <b>π, about 3.14</b>."),
                 ("For every circle, circumference ÷ radius is…", "2π, about 6.28", ["π, about 3.14", "4", "different for every circle"],
                  "The diameter is twice the radius, so circumference ÷ radius = <b>2π, about 6.28</b>."),
                 ("Which is the best description of π?", "The number of diameters that fit around the circumference", ["The length of the radius", "The area of a circle with radius 1 cm squared", "Exactly 22/7"],
                  "π is <b>the number of diameters that fit around the circumference</b>, a little more than 3."),
                 ("Which value is π to 2 decimal places?", "3.14", ["3.41", "3.12", "22.7"], "π = 3.14159…, so <b>3.14</b>."),
                 ("Is π a whole number?", "No, it is about 3.14159… and the decimals never end or repeat", ["Yes, it is 3", "Yes, it is 22", "No, it is exactly 3.14"],
                  "<b>No.</b> π = 3.14159… The decimals go on forever without repeating."),
                 ("A circle has diameter 10 cm. About how long is its circumference?", "A bit more than 30 cm", ["Exactly 10 cm", "About 20 cm", "About 100 cm"],
                  "The circumference is a bit more than 3 diameters: <b>a bit more than 30 cm</b> (31.4 cm).")]
        q, a, w, e = r.choice(facts)
        return T(q, a, w, e)
    d = r.randint(3, 40)
    q = "Estimate the circumference of a circle with diameter %d cm, using π ≈ 3." % d
    return QN(q, 3 * d, [2 * d, d + 3, 6 * d], "Circumference ≈ 3 × diameter = 3 × %d = <b>%d cm</b>. (The exact value is a little more.)" % (d, 3 * d), unit=" cm")


# ------------------------------------------------------------ set 3: circumference
def one_circ(r):
    v = r.randint(2, 30)
    use_d = r.random() < 0.5
    if use_d:
        C = math.pi * v
        q = "Find the circumference of a circle with diameter %d cm. Give your answer to 1 decimal place.%s" % (v, fig(circ_svg(dia="%d cm" % v)))
        e = "<i>C</i> = %s<i>d</i> = %s × %d = %s… = <b>%s cm</b>." % (PI, PI, v, "{:.3f}".format(C), d1(C))
        return QD(q, C, [math.pi * v * 2, math.pi * (v / 2) ** 2, 2 * v + math.pi], e, " cm")
    C = 2 * math.pi * v
    q = "Find the circumference of a circle with radius %d cm. Give your answer to 1 decimal place.%s" % (v, fig(circ_svg(rad="%d cm" % v)))
    e = "<i>C</i> = 2%s<i>r</i> = 2 × %s × %d = %s… = <b>%s cm</b>." % (PI, PI, v, "{:.3f}".format(C), d1(C))
    return QD(q, C, [math.pi * v, math.pi * v * v, 4 * math.pi * v], e, " cm")


# ------------------------------------------------------------ set 4: working back from the circumference
def one_back(r):
    kind = r.randint(0, 2)
    v = r.randint(2, 20)
    if kind == 0:
        q = "A circle has a circumference of %d%s cm. What is its diameter?" % (v, PI)
        return T(q, "%d cm" % v, ["%s cm" % num(F(v, 2)), "%d cm" % (2 * v), "%d%s cm" % (v, PI)], "<i>C</i> = %s<i>d</i> = %d%s, so <i>d</i> = <b>%d cm</b>." % (PI, v, PI, v))
    if kind == 1:
        q = "A circle has a circumference of %d%s cm. What is its radius?" % (2 * v, PI)
        return T(q, "%d cm" % v, ["%d cm" % (2 * v), "%d cm" % (4 * v), "%s cm" % num(F(v, 2))], "<i>C</i> = 2%s<i>r</i> = %d%s, so <i>r</i> = <b>%d cm</b>." % (PI, 2 * v, PI, v))
    C = r.choice([31.4, 62.8, 50, 100, 25, 44, 88, 75, 120, 157])
    d = C / math.pi
    if r.random() < 0.5:
        q = "A circle has a circumference of %s cm. Find its diameter to 1 decimal place." % num(F(str(C)))
        e = "<i>d</i> = <i>C</i> ÷ %s = %s ÷ %s = <b>%s cm</b>." % (PI, num(F(str(C))), PI, d1(d))
        return QD(q, d, [C * math.pi, d / 2, C / 2], e, " cm")
    q = "A circle has a circumference of %s cm. Find its radius to 1 decimal place." % num(F(str(C)))
    e = "<i>r</i> = <i>C</i> ÷ 2%s = %s ÷ (2 × %s) = <b>%s cm</b>." % (PI, num(F(str(C))), PI, d1(d / 2))
    return QD(q, d / 2, [d, C / 2, C / math.pi * 4], e, " cm")


# ------------------------------------------------------------ set 5: problems
def semi_svg():
    s = ["<path d='M30 130 A90 90 0 0 1 210 130 Z' fill='#eef6f0' stroke='%s' stroke-width='2.5'/>" % INK,
         text(120, 150, "12 cm", 15, col=RED)]
    return svg_wrap(240, 160, "".join(s), "semicircle with diameter 12 cm")


def problems():
    data = [
        ("A bike wheel has a diameter of 66 cm. How far does it travel in one full turn, to the nearest cm?", "207 cm", ["104 cm", "415 cm", "3421 cm"], "%s × 66 = 207.3… ≈ <b>207 cm</b>." % PI),
        ("A bike wheel has a diameter of 66 cm. About how many full turns does it make in 1 km?", "482", ["48", "4823", "1515"], "1 km = 100 000 cm. 100 000 ÷ 207.3 ≈ 482.3, so about <b>482</b> turns."),
        ("A round pool has a diameter of 4 m. How long is a fence that goes right round the edge, to 1 decimal place?", "12.6 m", ["25.1 m", "6.3 m", "50.3 m"], "%s × 4 = 12.57… ≈ <b>12.6 m</b>." % PI),
        ("A running track bend is a semicircle with diameter 73 m. How long is the bend, to the nearest metre?", "115 m", ["229 m", "57 m", "188 m"], "½ × %s × 73 = 114.7 ≈ <b>115 m</b>." % PI),
        ("A semicircle has a diameter of 12 cm. Find its perimeter to 1 decimal place.%s" % fig(semi_svg()), "30.8 cm", ["18.8 cm", "37.7 cm", "24.8 cm"],
         "Curved part = ½ × %s × 12 = 18.85 cm. Add the straight edge: 18.85 + 12 = <b>30.8 cm</b>." % PI),
        ("A clock's minute hand is 9 cm long. How far does its tip travel in one hour, to 1 decimal place?", "56.5 cm", ["28.3 cm", "254.5 cm", "18 cm"], "One full circle: 2 × %s × 9 = <b>56.5 cm</b>." % PI),
        ("If the diameter of a circle doubles, what happens to the circumference?", "It doubles", ["It is multiplied by 4", "It stays the same", "It halves"], "<i>C</i> = %s<i>d</i>, so the circumference <b>doubles</b>." % PI),
        ("Ribbon is wrapped once around a round cake tin with diameter 22 cm. How much ribbon is needed, to the nearest cm?", "69 cm", ["35 cm", "138 cm", "25 cm"], "%s × 22 = 69.1 ≈ <b>69 cm</b>." % PI),
        ("A tree trunk has a circumference of 2.2 m. About how wide is it (its diameter), to 1 decimal place?", "0.7 m", ["6.9 m", "1.1 m", "0.4 m"], "<i>d</i> = 2.2 ÷ %s = 0.70… ≈ <b>0.7 m</b>." % PI),
        ("Which formula gives the circumference of a circle?", "<i>C</i> = %s<i>d</i>" % PI, ["<i>C</i> = %s<i>r</i>" % PI, "<i>C</i> = %s<i>r</i>²" % PI, "<i>C</i> = 2<i>d</i>"], "<b><i>C</i> = %s<i>d</i></b>, which is the same as 2%s<i>r</i>." % (PI, PI)),
        ("A circle has radius 5 cm. Which is its circumference?", "10%s cm" % PI, ["5%s cm" % PI, "25%s cm" % PI, "10 cm"], "2 × %s × 5 = <b>10%s cm</b>." % (PI, PI)),
        ("Charlotte rolls a hoop of diameter 80 cm forward 5 full turns. How far does it roll, to the nearest cm?", "1257 cm", ["251 cm", "400 cm", "2513 cm"], "5 × %s × 80 = 1256.6 ≈ <b>1257 cm</b>." % PI),
        ("A round table has a circumference of 377 cm. Roughly what is its diameter?", "120 cm", ["60 cm", "1184 cm", "377 cm"], "377 ÷ %s ≈ 120, so <b>120 cm</b>." % PI),
        ("A circle has diameter 7 cm. Using %s ≈ 22/7, what is its circumference?" % PI, "22 cm", ["44 cm", "11 cm", "154 cm"], "22/7 × 7 = <b>22 cm</b>."),
        ("A quarter circle has radius 10 cm. What is the length of its curved edge, to 1 decimal place?", "15.7 cm", ["31.4 cm", "62.8 cm", "7.9 cm"], "¼ × 2 × %s × 10 = <b>15.7 cm</b>." % PI),
        ("The diameter of a circle is 18 cm. What is the radius?", "9 cm", ["36 cm", "18 cm", "6 cm"], "The radius is half the diameter: <b>9 cm</b>."),
        ("Which is longer: the circumference of a circle with diameter 10 cm, or the perimeter of a square with side 8 cm?", "The square (32 cm)", ["The circle (31.4 cm)", "They are equal", "You cannot tell"],
         "Circle: %s × 10 = 31.4 cm. Square: 4 × 8 = 32 cm. <b>The square</b> is longer." % PI),
        ("A circular garden bed has radius 1.5 m. Edging costs $8 per metre. What does the edging cost, to the nearest dollar?", "$75", ["$38", "$57", "$12"], "2 × %s × 1.5 = 9.42 m. 9.42 × $8 = $75.40 ≈ <b>$75</b>." % PI),
        ("Hamish measures a can: circumference 22 cm, diameter 7 cm. What does C ÷ d tell him?", "It is about 3.14, which is π", ["It is the area of the can", "It is the radius", "It is about 15"], "22 ÷ 7 = 3.14…, which is <b>π</b>."),
        ("A wheel travels 157 cm in one turn. What is its diameter, to the nearest cm?", "50 cm", ["25 cm", "100 cm", "493 cm"], "157 ÷ %s ≈ <b>50 cm</b>." % PI),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>The <b>radius</b> <i>r</i> goes from the centre to the edge. The <b>diameter</b> <i>d</i> = 2<i>r</i> goes right across. "
        "The <b>circumference</b> <i>C</i> is the distance all the way round.</p>"
        "<p>For every circle, <b>circumference ÷ diameter = π</b> (about 3.14). So <b><i>C</i> = π<i>d</i></b>, or <b><i>C</i> = 2π<i>r</i></b>. "
        "Use the π button on a calculator and round at the end, or leave the answer in terms of π, such as 8π cm.</p>"
        + fig(circ_svg(rad="r")),
        [("Find the circumference of a circle with diameter 8 cm.", ["π × 8 = 25.13…"], "25.1 cm"),
         ("Find the circumference of a circle with radius 5 cm.", ["2 × π × 5 = 10π = 31.41…"], "31.4 cm"),
         ("A circle has circumference 40 cm. Find its diameter.", ["40 ÷ π = 12.73…"], "12.7 cm")],
        ["Using the radius in <i>C</i> = π<i>d</i>. With <i>r</i> = 5, the diameter is 10.",
         "Doubling twice: if you use the diameter, do not multiply by 2 as well.",
         "Multiplying by π when working backwards. To find <i>d</i>, divide <i>C</i> by π.",
         "For a semicircle's perimeter, forgetting to add the straight diameter."])


def main():
    sets = [S("Parts of a circle", collect(one_parts, 20, R)),
            S("Circumference and π", collect(one_ratio, 20, R)),
            S("Finding the circumference", collect(one_circ, 20, R)),
            S("Working back from the circumference", collect(one_back, 20, R)),
            S("Circumference problems", problems())]
    make(7, "circumference-and-pi", 15, "AC9M7M03",
         "Circumference and Pi: Radius, Diameter and C = πd",
         "Year 7 Circumference Worksheets: Parts of a Circle, Pi and C = πd (Free, Answer Key)",
         "Circumference and π",
         "describe the relationship between π and the features of circles including the circumference, radius and diameter",
         "Free Year 7 maths worksheets on circumference and π for the Australian Curriculum (AC9M7M03): parts of a circle, "
         "radius and diameter, why C ÷ d = π, finding the circumference and working backwards. 100 questions with an answer key.",
         "For every circle, circumference ÷ diameter = π ≈ 3.14.",
         "C = πd, or C = 2πr.",
         body(),
         [("What is π?", "π is the circumference of any circle divided by its diameter. It is about 3.14159 and its decimals never end."),
          ("What is the formula for circumference?", "C = πd, or C = 2πr, because the diameter is twice the radius."),
          ("How do I find the diameter from the circumference?", "Divide the circumference by π. A circle with C = 31.4 cm has d ≈ 10 cm."),
          ("What is the difference between radius and diameter?", "The radius goes from the centre to the edge. The diameter goes right across through the centre, so d = 2r.")],
         sets, R)


if __name__ == "__main__":
    main()
