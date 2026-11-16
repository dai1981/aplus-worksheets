# -*- coding: utf-8 -*-
"""
US Grade 8 Math: Volume of Cylinders, Cones and Spheres (8.G.C.9)
  python3 tools/gen_us_math_g8_volume_of_cylinders_cones_spheres.py
V = πr²h, V = ⅓πr²h and V = ⁴⁄₃πr³: answers in terms of π and with π ≈ 3.14, diameters, missing
dimensions, and real-world problems. Wrong answers come from real mistakes: using the diameter as the
radius, forgetting the ⅓ for a cone, using r² instead of r³ for a sphere, and finding area instead of volume.
"""
import random
from fractions import Fraction as F
from g8_common import sl
from ws_common import num, mcq, balance, B, table, example, write_unit, fig, svg_wrap, text, line, INK, RED, GREEN, FILL

R = random.Random(81401)
UPDATED = "2026-11-16"
PI = "π"


def pi_txt(c, unit=" cm³"):
    c = F(c)
    if c.denominator == 1:
        return "%s%s%s" % (num(c) if c != 1 else "", PI, unit)
    return "%s%s%s" % (sl(c), PI, unit)


def dec(v, unit=" cm³"):
    return "%s%s" % ("{:,.2f}".format(float(v)).rstrip("0").rstrip("."), unit)


def cyl_svg(r, h, rl="r", hl="h", diam=False):
    W, H = 200, 190
    s = ["<ellipse cx='100' cy='160' rx='60' ry='16' fill='%s' stroke='%s' stroke-width='2'/>" % (FILL, GREEN),
         "<rect x='40' y='40' width='120' height='120' fill='%s' stroke='none'/>" % FILL,
         line(40, 40, 40, 160, GREEN, 2), line(160, 40, 160, 160, GREEN, 2),
         "<ellipse cx='100' cy='40' rx='60' ry='16' fill='#e6f2ea' stroke='%s' stroke-width='2'/>" % GREEN]
    if diam:
        s.append(line(40, 40, 160, 40, RED, 2))
        s.append(text(100, 34, "%s" % rl, 14, col=RED))
    else:
        s.append(line(100, 40, 160, 40, RED, 2))
        s.append(text(130, 34, "%s" % rl, 14, col=RED))
    s.append(line(176, 40, 176, 160, INK, 1.4))
    s.append(text(185, 104, hl, 14, anchor="start"))
    return svg_wrap(W + 40, H, "".join(s), "cylinder")


def cone_svg(rl, hl, diam=False):
    W, H = 220, 190
    s = ["<path d='M40 160 A60 16 0 0 0 160 160 L100 30 Z' fill='%s' stroke='%s' stroke-width='2'/>" % (FILL, GREEN),
         "<path d='M40 160 A60 16 0 0 1 160 160' fill='none' stroke='%s' stroke-width='1.4' stroke-dasharray='5 4'/>" % GREEN,
         line(100, 30, 100, 160, INK, 1.4, " stroke-dasharray='4 3'")]
    if diam:
        s.append(line(40, 160, 160, 160, RED, 2))
        s.append(text(100, 182, rl, 14, col=RED))
    else:
        s.append(line(100, 160, 160, 160, RED, 2))
        s.append(text(130, 182, rl, 14, col=RED))
    s.append(text(106, 100, hl, 14, anchor="start"))
    return svg_wrap(W, H + 10, "".join(s), "cone")


def sph_svg(rl, diam=False):
    W, H = 180, 180
    s = ["<circle cx='90' cy='90' r='70' fill='%s' stroke='%s' stroke-width='2'/>" % (FILL, GREEN),
         "<ellipse cx='90' cy='90' rx='70' ry='18' fill='none' stroke='%s' stroke-width='1.2' stroke-dasharray='5 4'/>" % GREEN]
    if diam:
        s.append(line(20, 90, 160, 90, RED, 2))
        s.append(text(90, 84, rl, 14, col=RED))
    else:
        s.append(line(90, 90, 160, 90, RED, 2))
        s.append(text(125, 84, rl, 14, col=RED))
    s.append("<circle cx='90' cy='90' r='3' fill='%s'/>" % INK)
    return svg_wrap(W, H, "".join(s), "sphere")


# ============================================================ set 1: cylinders
def set_cyl():
    its = []
    for r, h, diam in [(3, 5, False), (2, 10, False), (4, 6, False), (5, 2, False), (1, 9, False), (6, 4, False), (3, 12, False),
                       (10, 3, False), (7, 2, False), (8, 5, False), (6, 7, True), (10, 4, True), (4, 10, True), (2, 8, True),
                       (12, 5, True), (9, 2, False), (5, 10, True), (3, 3, False), (11, 1, False), (14, 3, True)]:
        rr = r / 2 if diam else r
        rr = F(rr)
        v = rr * rr * h
        lab = "%s cm" % num(r)
        q = fig(cyl_svg(r, h, ("d = " if diam else "r = ") + lab, "h = %s cm" % num(h), diam)) + "Find the volume of the cylinder in terms of π."
        e = ("%sV = πr²h = π × %s² × %s = <b>%s</b>." % ("The radius is half the diameter: r = %s cm. " % num(rr) if diam else "",
                                                       num(rr), num(h), pi_txt(v)))
        wr = [rr * h, 2 * rr * h, F(r if diam else 2 * r) ** 2 * h, v / 3, rr * rr]
        its.append(mcq(q, (pi_txt(v), v), [(pi_txt(w), w) for w in wr], e))
    return {"title": "Volume of cylinders", "items": its}


# ============================================================ set 2: cones
def set_cone():
    its = []
    for r, h, diam in [(3, 4, False), (6, 5, False), (2, 9, False), (3, 10, False), (5, 6, False), (4, 3, False), (9, 2, False),
                       (6, 7, False), (1, 12, False), (10, 3, False), (6, 8, True), (12, 5, True), (4, 9, True), (8, 6, True),
                       (3, 8, False), (7, 3, False), (10, 6, True), (2, 15, False), (12, 2, False), (18, 4, True)]:
        rr = F(r, 2) if diam else F(r)
        v = rr * rr * h / 3
        q = fig(cone_svg(("d = " if diam else "r = ") + "%s cm" % num(r), "h = %s cm" % num(h), diam)) + "Find the volume of the cone in terms of π."
        e = ("%sV = ⅓πr²h = ⅓ × π × %s² × %s = <b>%s</b>." % ("r = half the diameter = %s cm. " % num(rr) if diam else "",
                                                           num(rr), num(h), pi_txt(v)))
        wr = [rr * rr * h, F(r if diam else 2 * r) ** 2 * h / 3, rr * h / 3, rr * rr * h / 2]
        its.append(mcq(q, (pi_txt(v), v), [(pi_txt(w), w) for w in wr], e))
    return {"title": "Volume of cones", "items": its}


# ============================================================ set 3: spheres
def set_sph():
    its = []
    for r, diam in [(3, False), (6, False), (1, False), (2, False), (9, False), (4, True), (10, True), (5, False), (12, True),
                    (3, True), (15, False), (8, True), (6, True), (7, False), (2, True), (30, True)]:
        rr = F(r, 2) if diam else F(r)
        v = F(4, 3) * rr ** 3
        q = fig(sph_svg(("d = " if diam else "r = ") + "%s cm" % num(r), diam)) + "Find the volume of the sphere in terms of π."
        e = ("%sV = ⁴⁄₃πr³ = ⁴⁄₃ × π × %s³ = <b>%s</b>." % ("r = half the diameter = %s cm. " % num(rr) if diam else "",
                                                          num(rr), pi_txt(v)))
        wr = [rr ** 3, 4 * rr * rr, F(4, 3) * F(r if diam else 2 * r) ** 3, F(4, 3) * rr * rr, F(1, 3) * rr ** 3]
        its.append(mcq(q, (pi_txt(v), v), [(pi_txt(w), w) for w in wr], e))
    for q, ans, wr, e in [
        ("A hemisphere is half a sphere. What is the volume of a hemisphere with radius 3 cm, in terms of π?", "18π cm³", ["36π cm³", "9π cm³", "27π cm³"],
         "Sphere: ⁴⁄₃π × 27 = 36π. Half of it: <b>18π cm³</b>."),
        ("A ball has radius 10 in. About what is its volume? (π ≈ 3.14)", "4,186.67 in³", ["1,256 in³", "314 in³", "12,560 in³"],
         "⁴⁄₃ × 3.14 × 1,000 ≈ <b>4,186.67 in³</b>."),
        ("Which formula gives the volume of a sphere?", "V = ⁴⁄₃πr³", ["V = πr²h", "V = 4πr²", "V = ⅓πr²h"],
         "<b>V = ⁴⁄₃πr³</b>. (4πr² is the surface area.)"),
        ("If the radius of a sphere doubles, its volume is multiplied by …", "8", ["2", "4", "6"], "r³ becomes (2r)³ = 8r³, so the volume is multiplied by <b>8</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[2], o[3], o[18], o[1], o[5], o[16], o[7], o[9], o[17], o[4], o[6], o[19], o[8], o[10], o[11], o[12],
             o[13], o[14], o[15]]
    return {"title": "Volume of spheres", "items": order}


# ============================================================ set 4: 3.14 and missing dimensions
def set_314():
    its = []
    for kind, r, h in [("cylinder", 2, 5), ("cone", 3, 10), ("sphere", 3, None), ("cylinder", 5, 4), ("cone", 6, 5), ("sphere", 6, None),
                       ("cylinder", 10, 2), ("cone", 2, 6), ("sphere", 1, None), ("cylinder", 1, 10)]:
        if kind == "cylinder":
            c = F(r * r * h)
            how = "3.14 × %d² × %d" % (r, h)
        elif kind == "cone":
            c = F(r * r * h, 3)
            how = "⅓ × 3.14 × %d² × %d" % (r, h)
        else:
            c = F(4, 3) * r ** 3
            how = "⁴⁄₃ × 3.14 × %d³" % r
        v = c * F("3.14")
        desc = ("radius %d m and height %d m" % (r, h)) if h else ("radius %d m" % r)
        q = "Find the volume of a %s with %s. Use π ≈ 3.14." % (kind, desc)
        e = "V = %s = <b>%s</b>." % (how, dec(v, " m³"))
        wr = [v * 3 if kind == "cone" else v / 3 if kind == "cylinder" else c * F("3.14") * 3 / 4, v * 2, c, v + 10]
        its.append(mcq(q, (dec(v, " m³"), v), [(dec(w, " m³"), w) for w in wr], e))
    for q, ans, wr, e in [
        ("A cylinder has volume 72π cm³ and radius 3 cm. What is its height?", "8 cm", ["24 cm", "4 cm", "12 cm"], "72π = π × 9 × h, so h = 72 ÷ 9 = <b>8 cm</b>."),
        ("A cylinder has volume 100π in³ and height 4 in. What is its radius?", "5 in.", ["25 in.", "10 in.", "12.5 in."], "100π = π × r² × 4, so r² = 25 and r = <b>5 in.</b>"),
        ("A cone has volume 12π cm³ and radius 3 cm. What is its height?", "4 cm", ["12 cm", "1.33 cm", "36 cm"], "12π = ⅓ × π × 9 × h = 3πh, so h = <b>4 cm</b>."),
        ("A cone has volume 50π m³ and height 6 m. What is its radius?", "5 m", ["25 m", "√(50/6) m", "8.33 m"], "50π = ⅓ × π × r² × 6 = 2πr², so r² = 25 and r = <b>5 m</b>."),
        ("A sphere has volume 36π cm³. What is its radius?", "3 cm", ["9 cm", "27 cm", "6 cm"], "⁴⁄₃πr³ = 36π, so r³ = 27 and r = <b>3 cm</b>."),
        ("A sphere has volume 288π in³. What is its radius?", "6 in.", ["216 in.", "12 in.", "72 in."], "⁴⁄₃πr³ = 288π, so r³ = 216 and r = <b>6 in.</b>"),
        ("A cylinder has volume 45π ft³ and radius 3 ft. What is its height?", "5 ft", ["15 ft", "9 ft", "2.5 ft"], "45π = 9πh, so h = <b>5 ft</b>."),
        ("A cone has volume 32π cm³ and height 6 cm. What is its radius?", "4 cm", ["16 cm", "8 cm", "√(32/6) cm"], "32π = ⅓πr² × 6 = 2πr², so r² = 16 and r = <b>4 cm</b>."),
        ("A cylinder has volume 160π mm³ and radius 4 mm. What is its height?", "10 mm", ["40 mm", "20 mm", "2.5 mm"], "160π = 16πh, so h = <b>10 mm</b>."),
        ("A sphere has volume ⁴⁄₃π m³. What is its radius?", "1 m", ["4 m", "3 m", "⁴⁄₃ m"], "⁴⁄₃πr³ = ⁴⁄₃π, so r³ = 1 and r = <b>1 m</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[10], o[1], o[11], o[2], o[14], o[3], o[12], o[4], o[13], o[5], o[15], o[6], o[16], o[7], o[17], o[8],
             o[18], o[9], o[19]]
    return {"title": "Use π ≈ 3.14 and find missing sizes", "items": order}


# ============================================================ set 5: real world
def set_world():
    its = []
    for q, ans, wr, e in [
        ("A can is 12 cm tall with radius 4 cm. How much does it hold, in terms of π?", "192π cm³", ["48π cm³", "96π cm³", "64π cm³"],
         "V = π × 4² × 12 = <b>192π cm³</b>."),
        ("An ice cream cone has radius 3 cm and height 10 cm. How much ice cream fits inside (level with the top), in terms of π?", "30π cm³",
         ["90π cm³", "10π cm³", "60π cm³"], "V = ⅓ × π × 9 × 10 = <b>30π cm³</b>."),
        ("A cone and a cylinder have the same radius and height. How many cones of water fill the cylinder?", "3", ["2", "4", "1"],
         "A cone holds ⅓ of the cylinder, so it takes <b>3</b> cones."),
        ("A basketball has a diameter of about 24 cm. About what is its volume, in terms of π?", "2,304π cm³", ["18,432π cm³", "576π cm³", "768π cm³"],
         "r = 12. V = ⁴⁄₃π × 1,728 = <b>2,304π cm³</b>."),
        ("A water tank is a cylinder 2 m across and 3 m tall. About how many cubic meters does it hold? (π ≈ 3.14)", "9.42 m³", ["37.68 m³", "18.84 m³", "3.14 m³"],
         "r = 1. V = 3.14 × 1 × 3 = <b>9.42 m³</b>."),
        ("A sand pile is a cone 2 m tall with radius 3 m. About how much sand is there? (π ≈ 3.14)", "18.84 m³", ["56.52 m³", "6.28 m³", "37.68 m³"],
         "V = ⅓ × 3.14 × 9 × 2 = <b>18.84 m³</b>."),
        ("A gumball has radius 1 cm. A jar holds 400π cm³. About how many gumballs fit if they filled all the space?", "300", ["400", "100", "133"],
         "One gumball: ⁴⁄₃π cm³. 400π ÷ ⁴⁄₃π = <b>300</b>."),
        ("A cylinder and a sphere both have radius 3. The cylinder is 4 tall. Which holds more?", "The sphere (36π vs 36π: they are equal)",
         ["The cylinder", "The sphere", "We cannot tell"], "Cylinder: π × 9 × 4 = 36π. Sphere: ⁴⁄₃π × 27 = 36π. They are equal."),
        ("A pipe is 10 m long with radius 0.1 m. How much water fills it, in terms of π?", "0.1π m³", ["π m³", "0.01π m³", "2π m³"],
         "V = π × 0.1² × 10 = π × 0.01 × 10 = <b>0.1π m³</b>."),
        ("A cylinder’s radius doubles and its height stays the same. Its volume is …", "4 times as much", ["2 times as much", "8 times as much", "the same"],
         "r² becomes 4r²: <b>4 times as much</b>."),
        ("A cylinder’s height doubles and its radius stays the same. Its volume is …", "2 times as much", ["4 times as much", "8 times as much", "the same"],
         "V = πr²h grows the same as h: <b>2 times as much</b>."),
        ("A snow globe is a sphere with radius 6 cm. How much water fills it, in terms of π?", "288π cm³", ["144π cm³", "864π cm³", "48π cm³"],
         "V = ⁴⁄₃π × 216 = <b>288π cm³</b>."),
        ("A silo is a cylinder (radius 3 m, height 10 m) with a hemisphere on top. What is its volume, in terms of π?", "108π m³",
         ["126π m³", "90π m³", "36π m³"], "Cylinder: π × 9 × 10 = 90π. Hemisphere: ½ × ⁴⁄₃π × 27 = 18π. Total: <b>108π m³</b>."),
        ("Ana finds the volume of a cone with r = 3, h = 4 as 36π. What did she forget?", "The ⅓", ["To square r", "To use the diameter", "Nothing"],
         "πr²h = 36π is the cylinder. The cone is ⅓ of it: 12π. <b>The ⅓</b>."),
        ("Ben finds a sphere with diameter 6 has volume 288π. What did he do wrong?", "He used the diameter as the radius", ["He forgot the ⁴⁄₃",
         "He used r²", "Nothing"], "r = 3, so V = 36π. 288π comes from r = 6. <b>He used the diameter as the radius</b>."),
        ("Kim writes the volume of a cylinder with r = 2, h = 5 as 20π. What should it be?", "20π is correct", ["10π", "40π", "100π"],
         "π × 2² × 5 = 20π. <b>20π is correct</b>."),
        ("Which unit is used for volume?", "Cubic units, like cm³", ["Square units, like cm²", "Units of length, like cm", "Degrees"],
         "Volume fills space in 3 directions: <b>cubic units, like cm³</b>."),
        ("A cone has radius 6 and height 6. A sphere has radius 6. What fraction of the sphere’s volume is the cone’s?", "¼", ["½", "⅓", "1"],
         "Cone: ⅓π × 36 × 6 = 72π. Sphere: ⁴⁄₃π × 216 = 288π. 72/288 = <b>¼</b>."),
        ("A cylinder holds 300 cm³. A cone with the same radius and height holds …", "100 cm³", ["150 cm³", "900 cm³", "300 cm³"],
         "A cone is ⅓ of the matching cylinder: <b>100 cm³</b>."),
        ("A tennis ball can holds 3 balls of radius 3.3 cm stacked. What is the height of the can?", "19.8 cm", ["9.9 cm", "6.6 cm", "29.7 cm"],
         "Each ball is 6.6 cm tall: 3 × 6.6 = <b>19.8 cm</b>."),
    ]:
        if ans.startswith("The sphere (36π"):
            ans, wr = "They hold the same amount", ["The cylinder", "The sphere", "We cannot tell"]
            e = "Cylinder: π × 9 × 4 = 36π. Sphere: ⁴⁄₃π × 27 = 36π. <b>They hold the same amount</b>."
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[1], o[2], o[16], o[3], o[18], o[4], o[5], o[13], o[9], o[10], o[6], o[14], o[11], o[8], o[15], o[7],
             o[17], o[12], o[19]]
    return {"title": "Real-world volume", "items": order}


def body():
    return ("<h2>Three volume formulas</h2>"
            + table(["Shape", "Formula", "Remember"], [
                ["Cylinder", "V = πr²h", "area of the circle × height"],
                ["Cone", "V = ⅓πr²h", "⅓ of the cylinder with the same r and h"],
                ["Sphere", "V = ⁴⁄₃πr³", "r is cubed"]])
            + "<figure class='sn-fig'>" + cyl_svg(3, 5, "r = 3 cm", "h = 5 cm") + "<figcaption>V = π × 3² × 5 = 45π cm³ ≈ 141.3 cm³.</figcaption></figure>"
            + example("Find the volume of a cone with r = 3 cm and h = 4 cm.", ["V = ⅓ × π × 3² × 4.", "= ⅓ × 36π = 12π."], "12π cm³ ≈ 37.68 cm³")
            + example("Find the volume of a sphere with diameter 6 m.", ["r = 6 ÷ 2 = 3.", "V = ⁴⁄₃ × π × 27 = 36π."], "36π m³")
            + "<h2>Common mistakes</h2><ul><li>Using the diameter as the radius. Halve it first.</li>"
            "<li>Forgetting the ⅓ for a cone.</li><li>Using r² instead of r³ for a sphere.</li>"
            "<li>Writing square units. Volume is in cubic units (cm³).</li></ul>")


def main():
    sets = [set_cyl(), set_cone(), set_sph(), set_314(), set_world()]
    balance(sets, R)
    unit = {
        "slug": "volume-of-cylinders-cones-spheres",
        "title": "Volume of Cylinders, Cones and Spheres",
        "seo_title": "Grade 8 Volume Worksheets: Cylinders, Cones and Spheres (V = πr²h, ⅓πr²h, ⁴⁄₃πr³)",
        "short_title": "Cylinders, cones, spheres",
        "domain": "Geometry",
        "standard_code": "8.G.C.9",
        "standard_url": "https://www.thecorestandards.org/Math/Content/8/G/C/9/",
        "standard_text": "Know the formulas for the volumes of cones, cylinders, and spheres and use them to solve real-world and mathematical problems.",
        "meta_desc": "Free Grade 8 volume worksheets: find the volume of cylinders, cones and spheres in terms of π and with π ≈ 3.14, use diameters, find missing dimensions, and solve real-world problems. 100 questions with an answer key.",
        "key_big": "Cylinder V = πr²h. Cone V = ⅓πr²h. Sphere V = ⁴⁄₃πr³.",
        "key_sub": "Use the radius, not the diameter. A cone holds one third of the cylinder with the same r and h.",
        "body_html": body(),
        "faq": [
            {"q": "What is the formula for the volume of a cylinder?", "a": "V = πr²h: the area of the circular base times the height."},
            {"q": "Why is the volume of a cone one third of a cylinder?", "a": "A cone with the same radius and height as a cylinder holds exactly one third as much. Three cones of water fill the cylinder."},
            {"q": "What is the formula for the volume of a sphere?", "a": "V = ⁴⁄₃πr³. For r = 3, V = ⁴⁄₃ × π × 27 = 36π."},
            {"q": "Should I leave π in the answer?", "a": "Answers in terms of π (like 36π) are exact. If asked to use π ≈ 3.14, multiply to get a decimal."}],
        "sets": sets, "pdf_url": "", "sort": 14, "updated": UPDATED,
    }
    write_unit("us", "math", "grade-8", unit)


if __name__ == "__main__":
    main()
