# -*- coding: utf-8 -*-
"""
US Grade 7 Math: Area and Circumference of Circles (7.G.B.4)
  python tools/gen_us_math_g7_circles.py
Use π ≈ 3.14 (or leave answers in terms of π). Wrong answers come from real mistakes:
using the diameter in A = πr², mixing up the two formulas (2πr for area, πr² for
circumference), forgetting to square, squaring the diameter, and halving when not needed.
"""
import random
from fractions import Fraction as F
from ws_common import (num, mcq, balance, People, B, fig, figure, svg_wrap, text, line, table, example,
                       write_unit, GREEN, FILL, INK, BLUE)

R = random.Random(70701)
UPDATED = "2026-11-09"
PI = F("3.14")
SQ = "<sup>2</sup>"


def d(v):
    return num(F(v))


def circle_svg(label, value, unit, kind="r"):
    """Circle with a radius or diameter drawn and labelled."""
    W, H, cx, cy, r = 220, 200, 110, 100, 78
    s = ["<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='3'/>" % (cx, cy, r, FILL, GREEN),
         "<circle cx='%d' cy='%d' r='4' fill='%s'/>" % (cx, cy, INK)]
    if kind == "r":
        s.append(line(cx, cy, cx + r, cy, BLUE, 3))
        s.append(text(cx + r / 2, cy - 10, "%s %s" % (d(value), unit), 16, col=BLUE))
    else:
        s.append(line(cx - r, cy, cx + r, cy, BLUE, 3))
        s.append(text(cx, cy - 10, "%s %s" % (d(value), unit), 16, col=BLUE))
    return svg_wrap(W, H, "".join(s), label)


def mc(q, v, ws, e, unit=""):
    v = F(v)
    cands = []
    for w in ws:
        w = F(w)
        if w != v and w > 0 and num(w) is not None:
            cands.append((d(w) + unit, w))
    return mcq(q, (d(v) + unit, v), cands, e)


def pi_txt(k, power=""):
    k = F(k)
    return ("" if k == 1 else d(k)) + "π" + power


# ------------------------------------------------------------ set 1
def set_parts():
    its = []
    for r in [4, 9, F("2.5"), 15]:
        its.append(mc("A circle has a radius of %s cm. What is its diameter?" % d(r), 2 * r, [r / 2, r, r * r, r + 2],
                      "The diameter goes all the way across: d = 2r = 2 × %s = %s cm. Not %s: that halves the radius." % (d(r), d(2 * r), d(r / 2)), " cm"))
    for dd in [10, 7, 24, F("3.6")]:
        its.append(mc("A circle has a diameter of %s in. What is its radius?" % d(dd), F(dd, 2), [dd * 2, dd, F(dd, 2) + 1],
                      "The radius is half the diameter: r = %s ÷ 2 = %s in." % (d(dd), d(F(dd, 2))), " in."))
    its.append(mcq("Which formula gives the circumference of a circle?", ("C = 2πr", "a"), [("C = πr" + SQ, "b"), ("C = 2r", "c"), ("C = πr", "d")],
                   "Circumference is the distance around: C = 2πr, or C = πd. πr² is the area."))
    its.append(mcq("Which formula gives the area of a circle?", ("A = πr" + SQ, "a"), [("A = 2πr", "b"), ("A = πd", "c"), ("A = πd" + SQ, "d")],
                   "Area is the space inside: A = πr². 2πr and πd give the circumference."))
    its.append(mcq("What does π mean?", ("The circumference divided by the diameter", "a"),
                   [("The diameter divided by the radius", "b"), ("The area divided by the radius", "c"), ("The radius times 2", "d")],
                   "For every circle, circumference ÷ diameter is the same number, π ≈ 3.14."))
    its.append(mcq("A circle has circumference 31.4 cm and diameter 10 cm. What is circumference ÷ diameter?", ("3.14", "a"),
                   [("0.314", "b"), ("314", "c"), ("21.4", "d")], "31.4 ÷ 10 = 3.14, which is about π."))
    # in terms of pi
    for r in [3, 5, 8, 11]:
        its.append(mcq("A circle has a radius of %d m. What is its circumference in terms of π?" % r, (pi_txt(2 * r) + " m", "a"),
                       [(pi_txt(r * r) + " m", "b"), (pi_txt(r) + " m", "c"), (pi_txt(4 * r) + " m", "d")],
                       "C = 2πr = 2 × π × %d = %s m. Not %s: that is the area formula." % (r, pi_txt(2 * r), pi_txt(r * r))))
    for r in [4, 6, 10, 7]:
        its.append(mcq("A circle has a radius of %d ft. What is its area in terms of π?" % r, (pi_txt(r * r) + " ft" + SQ, "a"),
                       [(pi_txt(2 * r) + " ft" + SQ, "b"), (pi_txt(4 * r * r) + " ft" + SQ, "c"), (pi_txt(r) + " ft" + SQ, "d")],
                       "A = πr² = π × %d² = %s ft². Not %s: that squares the diameter." % (r, pi_txt(r * r), pi_txt(4 * r * r))))
    return {"title": "Radius, diameter and π", "items": its}


# ------------------------------------------------------------ set 2
def set_circumference():
    its = []
    for r in [5, 2, 12, 7, F("1.5"), 20]:
        C = 2 * PI * r
        svg = circle_svg("circle with radius %s cm" % d(r), r, "cm", "r")
        its.append(mc("Find the circumference. Use 3.14 for π." + fig(svg), C, [PI * r, PI * r * r, PI * 4 * r, C / 2 + 1],
                      "C = 2πr = 2 × 3.14 × %s = %s cm. Not %s: that uses πr, forgetting the 2." % (d(r), d(C), d(PI * r)), " cm"))
    for dd in [10, 6, 15, 30, 8, F("4.5")]:
        C = PI * dd
        svg = circle_svg("circle with diameter %s in." % d(dd), dd, "in.", "d")
        its.append(mc("Find the circumference. Use 3.14 for π." + fig(svg), C, [2 * PI * dd, PI * dd * dd / 4, PI * F(dd) / 2, C + 1],
                      "C = πd = 3.14 × %s = %s in. Not %s: 2πr uses the radius, not the diameter." % (d(dd), d(C), d(2 * PI * dd)), " in."))
    for r in [9, 25, 3, 14]:
        C = 2 * PI * r
        its.append(mc("A circle has a radius of %d m. Find its circumference. Use 3.14 for π." % r, C, [PI * r * r, PI * r, 4 * PI * r],
                      "C = 2 × 3.14 × %d = %s m." % (r, d(C)), " m"))
    for dd in [12, 50, 18, 100]:
        C = PI * dd
        its.append(mc("A circle has a diameter of %d yd. Find its circumference. Use 3.14 for π." % dd, C, [2 * PI * dd, PI * dd * dd / 4, PI * dd / 2],
                      "C = πd = 3.14 × %d = %s yd." % (dd, d(C)), " yd"))
    return {"title": "Circumference", "items": its}


# ------------------------------------------------------------ set 3
def set_area():
    its = []
    for r in [3, 10, 6, 13, F("2.5"), 8, 20]:
        A = PI * r * r
        svg = circle_svg("circle with radius %s cm" % d(r), r, "cm", "r")
        its.append(mc("Find the area. Use 3.14 for π." + fig(svg), A, [2 * PI * r, PI * 4 * r * r, PI * r, PI * 2 * r * 2],
                      "A = πr² = 3.14 × %s × %s = %s cm². Not %s: 2πr is the circumference." % (d(r), d(r), d(A), d(2 * PI * r)), " cm²"))
    for dd in [10, 4, 12, 30, 16, 22]:
        r = F(dd, 2)
        A = PI * r * r
        svg = circle_svg("circle with diameter %s m" % d(dd), dd, "m", "d")
        its.append(mc("Find the area. Use 3.14 for π." + fig(svg), A, [PI * dd * dd, PI * dd, 2 * PI * dd, PI * r],
                      "The radius is %s ÷ 2 = %s m. A = πr² = 3.14 × %s² = %s m². Not %s: that uses the diameter instead of the radius." % (
                          d(dd), d(r), d(r), d(A), d(PI * dd * dd)), " m²"))
    for r in [5, 9, 4, 7, 11, 15, 12]:
        A = PI * r * r
        its.append(mc("A circle has a radius of %d in. Find its area. Use 3.14 for π." % r, A, [2 * PI * r, PI * r * 2, 4 * PI * r * r, PI * r],
                      "A = πr² = 3.14 × %d² = 3.14 × %d = %s in². Not %s: that multiplies r by 2 instead of squaring it." % (r, r * r, d(A), d(PI * r * 2)), " in²"))
    return {"title": "Area", "items": its}


# ------------------------------------------------------------ set 4
def set_reverse():
    its = []
    for C, ans in [(F("31.4"), 10), (F("62.8"), 20), (F("18.84"), 6), (F("94.2"), 30)]:
        its.append(mc("A circle has circumference %s cm. What is its diameter? Use 3.14 for π." % d(C), ans, [ans / 2, ans * 2, C - PI],
                      "C = πd, so d = C ÷ π = %s ÷ 3.14 = %s cm. Not %s: that is the radius." % (d(C), d(ans), d(F(ans, 2))), " cm"))
    for C, r in [(F("25.12"), 4), (F("43.96"), 7), (F("62.8"), 10)]:
        its.append(mc("A circle has circumference %s m. What is its radius? Use 3.14 for π." % d(C), r, [2 * r, r * r, r + 1],
                      "C = 2πr, so r = %s ÷ 6.28 = %s m." % (d(C), d(r)), " m"))
    for A, r in [(F("78.5"), 5), (F("12.56"), 2), (F("314"), 10), (F("28.26"), 3)]:
        its.append(mc("A circle has area %s ft². What is its radius? Use 3.14 for π." % d(A), r, [r * r, 2 * r, A / PI / 2, A / 2, r + 1],
                      "A = πr², so r² = %s ÷ 3.14 = %s. Then r = %s ft, because %s × %s = %s." % (d(A), d(r * r), d(r), d(r), d(r), d(r * r)), " ft"))
    # in terms of pi reverse
    its.append(mcq("A circle has circumference 18π cm. What is its radius?", ("9 cm", 9), [("18 cm", 18), ("3 cm", 3), ("36 cm", 36)],
                   "C = 2πr = 18π, so r = 9 cm."))
    its.append(mcq("A circle has area 49π in². What is its diameter?", ("14 in.", 14), [("7 in.", 7), ("49 in.", 49), ("24.5 in.", 24)],
                   "A = πr² = 49π, so r² = 49 and r = 7. The diameter is 2 × 7 = 14 in."))
    # semicircles and quarter circles
    for r, kind in [(4, "semicircle"), (10, "semicircle"), (6, "quarter circle"), (2, "quarter circle")]:
        part = F(1, 2) if kind == "semicircle" else F(1, 4)
        A = PI * r * r * part
        its.append(mc("Find the area of a %s with radius %d cm. Use 3.14 for π." % (kind, r), A, [PI * r * r, A * 2 if kind == "quarter circle" else A / 2, PI * r * part],
                      "A full circle has area 3.14 × %d² = %s cm². A %s is %s of it: %s cm²." % (
                          r, d(PI * r * r), kind, "half" if kind == "semicircle" else "one quarter", d(A)), " cm²"))
    # perimeter of a semicircle
    its.append(mc("Find the distance around a semicircle with diameter 10 m (the curved part plus the straight edge). Use 3.14 for π.", F("25.7"),
                  [F("15.7"), F("31.4"), F("20.7")],
                  "Curved part = half of πd = 3.14 × 10 ÷ 2 = 15.7 m. Add the diameter: 15.7 + 10 = 25.7 m. Not 15.7 m: that leaves out the straight edge.", " m"))
    its.append(mcq("If the radius of a circle doubles, what happens to its area?", ("It becomes 4 times as large.", "a"),
                   [("It doubles.", "b"), ("It stays the same.", "c"), ("It becomes 8 times as large.", "d")],
                   "A = πr². With 2r, A = π(2r)² = 4πr². The circumference only doubles."))
    its.append(mcq("If the radius of a circle doubles, what happens to its circumference?", ("It doubles.", "a"),
                   [("It becomes 4 times as large.", "b"), ("It stays the same.", "c"), ("It is cut in half.", "d")],
                   "C = 2πr. With 2r, C = 2π(2r) = 2 × 2πr, which is twice as long."))
    return {"title": "Working backward and parts of circles", "items": its}


# ------------------------------------------------------------ set 5
def set_words():
    its = []
    P = People(R)
    its.append(mc("A bike wheel has a diameter of 26 inches. How far does the bike go in one full turn of the wheel? Use 3.14 for π.", F("81.64"),
                  [F("163.28"), F("530.66"), F("40.82")], "One turn = the circumference: C = πd = 3.14 × 26 = 81.64 in.", " in."))
    its.append(mc("A round pizza has a diameter of 14 inches. What is its area? Use 3.14 for π.", F("153.86"),
                  [F("615.44"), F("43.96"), F("87.92")], "r = 7 in. A = 3.14 × 7² = 3.14 × 49 = 153.86 in². Not 615.44: that uses the diameter.", " in²"))
    its.append(mc("A circular garden has a radius of 5 m. How much fencing goes around it? Use 3.14 for π.", F("31.4"),
                  [F("78.5"), F("15.7"), F("62.8")], "Fencing goes around, so find the circumference: 2 × 3.14 × 5 = 31.4 m.", " m"))
    its.append(mc("A sprinkler waters a circle with a radius of 6 ft. What area of lawn does it water? Use 3.14 for π.", F("113.04"),
                  [F("37.68"), F("452.16"), F("18.84")], "A = 3.14 × 6² = 3.14 × 36 = 113.04 ft².", " ft²"))
    its.append(mc("A circular track has a diameter of 100 m. How far is one lap? Use 3.14 for π.", 314,
                  [628, 7850, 157], "One lap is the circumference: 3.14 × 100 = 314 m.", " m"))
    name, he, his = P.next()
    its.append(mc("%s walks around a circular pond 3 times. The pond has a radius of 20 m. How far does %s walk? Use 3.14 for π." % (name, he), F("376.8"),
                  [F("125.6"), F("3768"), F("188.4")], "One lap = 2 × 3.14 × 20 = 125.6 m. Three laps = 3 × 125.6 = 376.8 m.", " m"))
    its.append(mc("A clock's minute hand is 10 cm long. How far does its tip travel in 1 hour? Use 3.14 for π.", F("62.8"),
                  [F("31.4"), F("314"), F("15.7")], "In 1 hour the tip goes all the way around a circle with radius 10 cm: 2 × 3.14 × 10 = 62.8 cm.", " cm"))
    its.append(mc("A round table top has a radius of 3 ft. Paint costs $2 per square foot. What does it cost to paint the top? Use 3.14 for π.", F("56.52"),
                  [F("28.26"), F("37.68"), F("18.84")], "A = 3.14 × 3² = 28.26 ft². Cost = 28.26 × 2 = $56.52.", ""))
    its[-1]["c"] = ["$" + x for x in its[-1]["c"]]
    its.append(mc("A circular rug has an area of 50.24 ft². What is its radius? Use 3.14 for π.", 4,
                  [16, 8, F("12.56")], "r² = 50.24 ÷ 3.14 = 16, so r = 4 ft.", " ft"))
    its.append(mc("A wheel has a circumference of 188.4 cm. What is its diameter? Use 3.14 for π.", 60,
                  [30, 120, F("185.26")], "d = C ÷ π = 188.4 ÷ 3.14 = 60 cm.", " cm"))
    its.append(mc("A trampoline has a diameter of 12 ft. A cover must go over the top. What area must it cover? Use 3.14 for π.", F("113.04"),
                  [F("452.16"), F("37.68"), F("75.36")], "r = 6 ft. A = 3.14 × 36 = 113.04 ft².", " ft²"))
    its.append(mc("A can of soup has a label that wraps around it once. The can has a diameter of 7 cm. How long is the label? Use 3.14 for π.", F("21.98"),
                  [F("43.96"), F("38.465"), F("10.99")], "The label goes around the can: C = 3.14 × 7 = 21.98 cm.", " cm"))
    its.append(mc("A circular window has a radius of 1.5 ft. What is its area? Use 3.14 for π.", F("7.065"),
                  [F("9.42"), F("28.26"), F("4.71")], "A = 3.14 × 1.5² = 3.14 × 2.25 = 7.065 ft².", " ft²"))
    its.append(mc("A dog is tied to a post with a 9 m rope. What area can the dog reach? Use 3.14 for π.", F("254.34"),
                  [F("56.52"), F("1017.36"), F("28.26")], "The dog can reach a circle with radius 9 m: A = 3.14 × 81 = 254.34 m².", " m²"))
    its.append(mc("A Ferris wheel has a radius of 25 m. How far does a seat travel in one full turn? Use 3.14 for π.", 157,
                  [F("78.5"), F("1962.5"), 314], "One turn = 2 × 3.14 × 25 = 157 m.", " m"))
    its.append(mc("A semicircle window sits on top of a door. The window's diameter is 4 ft. What is the area of the window? Use 3.14 for π.", F("6.28"),
                  [F("12.56"), F("25.12"), F("3.14")], "A full circle with r = 2 ft has area 3.14 × 4 = 12.56 ft². Half of it is 6.28 ft².", " ft²"))
    its.append(mc("A 12-inch pizza and an 8-inch pizza are both round. About how much more area does the 12-inch pizza have? Use 3.14 for π.", F("62.8"),
                  [F("12.56"), F("251.2"), F("50.24")], "12-inch: 3.14 × 6² = 113.04. 8-inch: 3.14 × 4² = 50.24. Difference: 113.04 − 50.24 = 62.8 in².", " in²"))
    its.append(mc("A square is 10 cm on each side. A circle with diameter 10 cm is cut out of it. What area is left? Use 3.14 for π.", F("21.5"),
                  [F("78.5"), F("68.6"), F("31.4")], "Square: 10 × 10 = 100 cm². Circle: 3.14 × 5² = 78.5 cm². Left: 100 − 78.5 = 21.5 cm².", " cm²"))
    its.append(mc("A wheel turns 50 times. Its radius is 0.3 m. How far does it roll? Use 3.14 for π.", F("94.2"),
                  [F("47.1"), F("14.13"), F("1.884")], "One turn = 2 × 3.14 × 0.3 = 1.884 m. 50 turns = 50 × 1.884 = 94.2 m.", " m"))
    its.append(mc("A circle's circumference is 6.28 m. What is its area? Use 3.14 for π.", F("3.14"),
                  [F("6.28"), F("12.56"), F("1.57")], "C = 2πr = 6.28, so r = 1 m. A = 3.14 × 1² = 3.14 m².", " m²"))
    return {"title": "Word problems", "items": its}


def body():
    svg = circle_svg("circle with radius 5 cm", 5, "cm", "r")
    rows = [["Radius", "<i>r</i>", "Center to the edge"], ["Diameter", "<i>d</i> = 2<i>r</i>", "All the way across"],
            ["Circumference", "<i>C</i> = 2π<i>r</i> = π<i>d</i>", "Distance around (units)"],
            ["Area", "<i>A</i> = π<i>r</i>" + SQ, "Space inside (square units)"]]
    return ("<h2>The parts of a circle</h2><p>The <b>radius</b> goes from the center to the edge. The <b>diameter</b> goes all the way across, so it is twice the radius. "
            "For every circle, circumference ÷ diameter is the same number: <b>π ≈ 3.14</b>.</p>"
            + table(["Part", "Formula", "Meaning"], rows)
            + figure(svg, "r = 5 cm, so d = 10 cm.")
            + example("Find the circumference and area of a circle with radius 5 cm. Use 3.14 for π.",
                      ["C = 2 × 3.14 × 5 = 31.4 cm.", "A = 3.14 × 5" + SQ + " = 3.14 × 25 = 78.5 cm" + SQ + "."], "C = 31.4 cm, A = 78.5 cm" + SQ)
            + example("A circle has diameter 12 m. Find its area.", ["First find the radius: 12 ÷ 2 = 6 m.", "A = 3.14 × 6" + SQ + " = 3.14 × 36 = 113.04 m" + SQ + "."], "113.04 m" + SQ)
            + "<h2>Common mistakes</h2><ul><li>Using the diameter in A = πr" + SQ + ": halve it first.</li>"
            "<li>Mixing the formulas: 2π<i>r</i> is the distance around, π<i>r</i>" + SQ + " is the space inside.</li>"
            "<li>Writing r" + SQ + " as 2r: 5" + SQ + " = 25, not 10.</li><li>Forgetting square units for area.</li></ul>")


def main():
    sets = [set_parts(), set_circumference(), set_area(), set_reverse(), set_words()]
    balance(sets, R)
    unit = {
        "slug": "circles-area-and-circumference",
        "title": "Area and Circumference of Circles",
        "seo_title": "Grade 7 Circles Worksheets: Area and Circumference with π, Radius and Diameter",
        "short_title": "Circles: area and circumference",
        "domain": "Geometry",
        "standard_code": "7.G.B.4",
        "standard_url": "https://www.thecorestandards.org/Math/Content/7/G/B/4/",
        "standard_text": "Know the formulas for the area and circumference of a circle and use them to solve problems; give an informal derivation of the relationship between the circumference and area of a circle.",
        "meta_desc": "Free Grade 7 circles worksheets: radius and diameter, circumference C = 2πr, area A = πr², answers in terms of π, working backward, semicircles and real-world problems. 100 practice questions with an answer key.",
        "key_big": "Circumference C = 2πr (distance around). Area A = πr² (space inside).",
        "key_sub": "π ≈ 3.14. If you are given the diameter, halve it to get the radius before finding the area.",
        "body_html": body(),
        "faq": [
            {"q": "What is the formula for the circumference of a circle?", "a": "C = 2πr or C = πd. A circle with radius 5 cm has circumference 2 × 3.14 × 5 = 31.4 cm."},
            {"q": "What is the formula for the area of a circle?", "a": "A = πr². A circle with radius 5 cm has area 3.14 × 25 = 78.5 cm²."},
            {"q": "What if I only know the diameter?", "a": "For circumference you can use C = πd. For area, divide the diameter by 2 to get the radius first."},
            {"q": "What does in terms of π mean?", "a": "Leave π as a symbol instead of using 3.14. A circle with radius 3 has area 9π and circumference 6π."}],
        "sets": sets,
        "pdf_url": "",
        "sort": 7,
        "updated": UPDATED,
    }
    write_unit("us", "math", "grade-7", unit)


if __name__ == "__main__":
    main()
