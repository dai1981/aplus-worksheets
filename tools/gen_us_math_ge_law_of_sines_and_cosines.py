# -*- coding: utf-8 -*-
"""
US Geometry: Law of Sines and Law of Cosines (Common Core G-SRT.D.9, G-SRT.D.10, G-SRT.D.11)
  python3 tools/gen_us_math_ge_law_of_sines_and_cosines.py
The area formula ½ab sin C, the Law of Sines for sides and angles, the Law of Cosines for sides and
angles, and word problems with non-right triangles.
Wrong answers come from real mistakes: using the SOH CAH TOA ratios in a triangle with no right angle,
pairing a side with the wrong angle, adding 2ab cos C instead of subtracting, and forgetting the square root.
"""
import math
import random
from decimal import Decimal, ROUND_HALF_UP
from us_hs import B, S, make, lesson, collect, T, fig, num, MINUS, People
from us_geo import Canvas

R = random.Random(93701)


def d1(x):
    return "{:,.1f}".format(float(Decimal(str(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)))


def sin(d):
    return math.sin(math.radians(d))


def cos(d):
    return math.cos(math.radians(d))


def tri_fig(A, Bang, labels):
    """triangle with angles A at left and B at right (degrees); labels: a, b, c, A, B, C texts"""
    c = Canvas()
    base = 240
    ta, tb = math.tan(math.radians(A)), math.tan(math.radians(Bang))
    x = base * tb / (ta + tb) if A < 90 and Bang < 90 else None
    if x is None:
        return ""
    h = x * ta
    k = min(1, 150 / h)
    P, Q = (20, 170), (20 + base * k, 170)
    Rr = (20 + x * k, 170 - h * k)
    c.poly([P, Q, Rr])
    c.vlabels([P, Q, Rr], ["A", "B", "C"])
    cen = ((P[0] + Q[0] + Rr[0]) / 3, (P[1] + Q[1] + Rr[1]) / 3)
    for key, (p, q) in {"c": (P, Q), "a": (Q, Rr), "b": (P, Rr)}.items():
        if labels.get(key):
            c.side_label(p, q, labels[key], cen, 18, 13)
    for key, (v, p, q) in {"A": (P, Q, Rr), "B": (Q, Rr, P), "C": (Rr, P, Q)}.items():
        if labels.get(key):
            c.angle(v, p, q, "", r=18)
            c.angle_text(v, p, q, labels[key], r=40, fs=13)
    return fig(c.svg("triangle ABC, not drawn to scale"))


def opts(right, wr, unit=""):
    out = []
    for w in wr:
        if w is None or not (w > 0) or math.isnan(w):
            continue
        s = d1(w) + unit
        if s != right and s not in out:
            out.append(s)
    k = 1.5
    while len(out) < 3:
        s = d1(float(right.replace(unit, "").replace(",", "")) + k) + unit
        if s not in out and s != right:
            out.append(s)
        k += 1.3
    return out[:3]


# ------------------------------------------------------------ set 1: area = ½ab sin C
def one_area(r):
    a, b = r.randint(4, 20), r.randint(4, 20)
    C = r.choice([30, 35, 40, 45, 50, 60, 70, 75, 80, 100, 110, 120, 130, 150])
    A_ = 0.5 * a * b * sin(C)
    q = "In △ABC, <i>a</i> = %d, <i>b</i> = %d and m∠C = %d°. Find the area to the nearest tenth." % (a, b, C)
    right = d1(A_) + " square units"
    e = "Area = ½<i>ab</i> sin <i>C</i> = ½(%d)(%d) sin %d° = <b>%s square units</b>." % (a, b, C, d1(A_))
    return T(q, right, opts(right, [a * b * sin(C), 0.5 * a * b * cos(C) if C < 90 else 0.5 * a * b, 0.5 * a * b], " square units"), e)


# ------------------------------------------------------------ set 2: law of sines, find a side
def one_ls_side(r):
    A, Bg = r.randint(30, 80), r.randint(30, 80)
    C = 180 - A - Bg
    if C < 25:
        return None
    a = r.randint(6, 20)
    b = a * sin(Bg) / sin(A)
    kind = r.choice(["b", "c"])
    if kind == "b":
        q = "In △ABC, m∠A = %d°, m∠B = %d° and <i>a</i> = %d. Find <i>b</i> to the nearest tenth.%s" % (A, Bg, a, tri_fig(A, Bg, {"a": num(a), "b": "<i>b</i>", "A": "%d°" % A, "B": "%d°" % Bg}))
        right = d1(b)
        e = "Law of Sines: <i>b</i>/sin <i>B</i> = <i>a</i>/sin <i>A</i>. <i>b</i> = %d × sin %d° ÷ sin %d° = <b>%s</b>." % (a, Bg, A, right)
        return T(q, right, opts(right, [a * sin(A) / sin(Bg), a * sin(Bg), a * sin(C) / sin(A)]), e)
    c_ = a * sin(C) / sin(A)
    q = "In △ABC, m∠A = %d°, m∠B = %d° and <i>a</i> = %d. Find <i>c</i> to the nearest tenth.%s" % (A, Bg, a, tri_fig(A, Bg, {"a": num(a), "c": "<i>c</i>", "A": "%d°" % A, "B": "%d°" % Bg}))
    right = d1(c_)
    e = "First m∠C = 180° %s %d° %s %d° = %d°. Then <i>c</i> = %d × sin %d° ÷ sin %d° = <b>%s</b>." % (MINUS, A, MINUS, Bg, C, a, C, A, right)
    return T(q, right, opts(right, [a * sin(Bg) / sin(A), a * sin(A) / sin(C), a * sin(C)]), e)


# ------------------------------------------------------------ set 3: law of sines, find an angle
def one_ls_ang(r):
    A = r.randint(35, 80)
    a = r.randint(10, 20)
    b = r.randint(5, a - 1)
    sB = b * sin(A) / a
    Bg = math.degrees(math.asin(sB))
    if Bg < 12:
        return None
    q = "In △ABC, m∠A = %d°, <i>a</i> = %d and <i>b</i> = %d. Find m∠B to the nearest tenth of a degree." % (A, a, b)
    right = d1(Bg) + "°"
    e = "Law of Sines: sin <i>B</i>/<i>b</i> = sin <i>A</i>/<i>a</i>, so sin <i>B</i> = %d × sin %d° ÷ %d = %s. m∠B = sin<sup>−1</sup>(%s) = <b>%s</b>. (B is opposite a shorter side, so it is acute.)" % (
        b, A, a, "{:.4f}".format(sB), "{:.4f}".format(sB), right)
    wa = math.degrees(math.asin(min(1, a * sin(A) / b))) if a * sin(A) / b <= 1 else None
    return T(q, right, opts(right, [180 - Bg, wa, Bg * 1.0 + 0 if False else math.degrees(math.asin(b / a)), sB * 100], "°"), e)


# ------------------------------------------------------------ set 4: law of cosines, find a side
def one_lc_side(r):
    a, b = r.randint(5, 20), r.randint(5, 20)
    C = r.choice([35, 40, 50, 55, 65, 70, 80, 95, 100, 110, 120, 130])
    c2 = a * a + b * b - 2 * a * b * cos(C)
    c_ = math.sqrt(c2)
    q = "In △ABC, <i>a</i> = %d, <i>b</i> = %d and m∠C = %d°. Find <i>c</i> to the nearest tenth." % (a, b, C)
    right = d1(c_)
    e = "Law of Cosines: <i>c</i>² = <i>a</i>² + <i>b</i>² %s 2<i>ab</i> cos <i>C</i> = %d + %d %s 2(%d)(%d) cos %d° = %s. <i>c</i> = <b>%s</b>." % (
        MINUS, a * a, b * b, MINUS, a, b, C, d1(c2), right)
    return T(q, right, opts(right, [math.sqrt(a * a + b * b + 2 * a * b * cos(C)) if a * a + b * b + 2 * a * b * cos(C) > 0 else None, c2,
                                    math.sqrt(a * a + b * b), math.sqrt(abs(a * a + b * b - 2 * a * b)) + 0.0]), e)


# ------------------------------------------------------------ set 5: law of cosines for angles, and word problems
def one_mix(r):
    pp = People(r)
    nm, he, his = pp.next()
    kind = r.choice(["ang", "ang", "boat", "tri", "choose", "choose"])
    if kind == "ang":
        a, b, c_ = sorted(r.sample(range(4, 20), 3))
        if a + b <= c_:
            return None
        cosC = (a * a + b * b - c_ * c_) / (2 * a * b)
        C = math.degrees(math.acos(cosC))
        q = "A triangle has sides <i>a</i> = %d, <i>b</i> = %d and <i>c</i> = %d. Find the largest angle, m∠C, to the nearest tenth of a degree." % (a, b, c_)
        right = d1(C) + "°"
        e = "cos <i>C</i> = (<i>a</i>² + <i>b</i>² %s <i>c</i>²) ÷ 2<i>ab</i> = (%d + %d %s %d) ÷ %d = %s. m∠C = cos<sup>−1</sup>(%s) = <b>%s</b>." % (
            MINUS, a * a, b * b, MINUS, c_ * c_, 2 * a * b, "{:.4f}".format(cosC).replace("-", MINUS), "{:.4f}".format(cosC).replace("-", MINUS), right)
        bad = (a * a + b * b + c_ * c_) / (2 * a * b)
        return T(q, right, opts(right, [180 - C, math.degrees(math.acos(bad)) if bad <= 1 else None, math.degrees(math.acos(max(-1, min(1, (c_ * c_ - a * a - b * b) / (2 * a * b))))) if False else 90.0, C / 2], "°"), e)
    if kind == "boat":
        d1_, d2_ = r.randint(5, 15), r.randint(5, 15)
        ang = r.choice([40, 50, 60, 70, 110, 120])
        dist = math.sqrt(d1_ ** 2 + d2_ ** 2 - 2 * d1_ * d2_ * cos(ang))
        q = ("Two boats leave the same dock. One travels %d miles and the other travels %d miles, and the angle between their paths is %d°. "
             "How far apart are they, to the nearest tenth of a mile?" % (d1_, d2_, ang))
        right = d1(dist) + " miles"
        e = "Law of Cosines: <i>d</i>² = %d² + %d² %s 2(%d)(%d) cos %d°, so <i>d</i> = <b>%s miles</b>." % (d1_, d2_, MINUS, d1_, d2_, ang, d1(dist))
        return T(q, right, opts(right, [d1_ + d2_, math.sqrt(d1_ ** 2 + d2_ ** 2), dist ** 2], " miles"), e)
    if kind == "tri":
        A, Bg = r.randint(35, 70), r.randint(40, 75)
        c_ = r.randint(100, 400)
        C = 180 - A - Bg
        b = c_ * sin(Bg) / sin(C)
        q = ("Two lookout towers are %d m apart. A fire is seen at angles of %d° and %d° from the line joining the towers. "
             "How far is the fire from the first tower (the one with the %d° angle), to the nearest meter?" % (c_, A, Bg, A))
        right = "%d m" % round(b)
        wr = ["%d m" % round(c_ * sin(A) / sin(C)), "%d m" % round(c_ * sin(Bg)), "%d m" % round(c_ * sin(C) / sin(Bg))]
        e = "The third angle is %d°. The side from the first tower to the fire is opposite the %d° angle: <i>d</i> = %d × sin %d° ÷ sin %d° = <b>%s</b>." % (
            C, Bg, c_, Bg, C, right)
        return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3] + ([] if len(set(wr) - {right}) >= 3 else ["%d m" % (round(b) + 10)]), e)
    items = [("You know two angles and one side of a triangle. Which law should you use?", "Law of Sines", ["Law of Cosines", "Pythagorean theorem", "SOH CAH TOA only"],
              "With two angles and a side (AAS or ASA), you have a complete side-angle pair: use the Law of Sines."),
             ("You know two sides and the angle between them. Which law finds the third side?", "Law of Cosines", ["Law of Sines", "Pythagorean theorem", "Triangle Inequality"],
              "SAS gives no matching side-angle pair, so use the Law of Cosines."),
             ("You know all three sides of a triangle. Which law finds an angle?", "Law of Cosines", ["Law of Sines", "Pythagorean theorem", "Angle Addition Postulate"],
              "SSS: rearrange the Law of Cosines to find the cosine of an angle."),
             ("What does the Law of Cosines become when m∠C = 90°?", "The Pythagorean theorem", ["The Law of Sines", "The area formula", "Nothing; it does not work"],
              "cos 90° = 0, so <i>c</i>² = <i>a</i>² + <i>b</i>²."),
             ("Which is the Law of Sines?", "<i>a</i>/sin <i>A</i> = <i>b</i>/sin <i>B</i> = <i>c</i>/sin <i>C</i>", ["<i>a</i>/sin <i>B</i> = <i>b</i>/sin <i>A</i>",
              "<i>a</i> sin <i>A</i> = <i>b</i> sin <i>B</i>", "<i>c</i>² = <i>a</i>² + <i>b</i>² %s 2<i>ab</i> sin <i>C</i>" % MINUS], "Each side is paired with the sine of its opposite angle."),
             ("In the area formula ½<i>ab</i> sin <i>C</i>, where is angle C?", "Between sides <i>a</i> and <i>b</i>", ["Opposite side <i>a</i>", "Opposite side <i>b</i>", "Anywhere in the triangle"],
              "C must be the included angle, the one between the two sides you multiply.")]
    q, right, wr, e = r.choice(items)
    return T(q, right, wr, e + " <b>%s</b>." % right)


def build():
    sets = [S("Area with ½ab sin C", collect(one_area, 20, R)),
            S("Law of Sines: find a side", collect(one_ls_side, 20, R)),
            S("Law of Sines: find an angle", collect(one_ls_ang, 20, R)),
            S("Law of Cosines: find a side", collect(one_lc_side, 20, R)),
            S("Find an angle and solve problems", collect(one_mix, 20, R))]
    body = lesson(
        "<p>SOH CAH TOA only works in right triangles. For any triangle, side <i>a</i> is opposite ∠A, <i>b</i> opposite ∠B, and <i>c</i> opposite ∠C.</p>"
        "<ul><li><b>Area</b> = ½<i>ab</i> sin <i>C</i> (C is the angle between <i>a</i> and <i>b</i>).</li>"
        "<li><b>Law of Sines</b>: <i>a</i>/sin <i>A</i> = <i>b</i>/sin <i>B</i> = <i>c</i>/sin <i>C</i>. Use it when you know a side and its opposite angle (AAS, ASA, SSA).</li>"
        "<li><b>Law of Cosines</b>: <i>c</i>² = <i>a</i>² + <i>b</i>² %s 2<i>ab</i> cos <i>C</i>. Use it for SAS (find a side) or SSS (find an angle).</li></ul>"
        "<p>Round only at the end, and keep your calculator in degree mode.</p>" % MINUS,
        [("m∠A = 40°, m∠B = 75°, <i>a</i> = 12. Find <i>b</i>.", ["<i>b</i>/sin 75° = 12/sin 40°", "<i>b</i> = 12 sin 75° ÷ sin 40°"], "<i>b</i> ≈ 18.0"),
         ("<i>a</i> = 8, <i>b</i> = 11, m∠C = 60°. Find <i>c</i>.", ["<i>c</i>² = 64 + 121 %s 2(8)(11)(0.5) = 97" % MINUS], "<i>c</i> ≈ 9.8")],
        ["Using SOH CAH TOA in a triangle without a right angle.",
         "Pairing a side with an angle that is not opposite it.",
         "Adding 2<i>ab</i> cos <i>C</i> instead of subtracting it.",
         "Forgetting to take the square root at the end of the Law of Cosines."])
    faq = [("When do you use the Law of Sines?", "When you know an angle and the side opposite it, plus one more side or angle (AAS, ASA or SSA)."),
           ("When do you use the Law of Cosines?", "When you know two sides and the included angle (SAS) or all three sides (SSS)."),
           ("What is the formula for the area of a triangle using sine?", "Area = ½ab sin C, where C is the angle between sides a and b."),
           ("Is the Law of Cosines related to the Pythagorean theorem?", "Yes. When C is 90°, cos C = 0 and the Law of Cosines becomes c² = a² + b².")]
    make("law-of-sines-and-cosines", 17, "G-SRT.D.11",
         "Law of Sines and Law of Cosines",
         "Law of Sines and Law of Cosines Worksheet (Geometry, G-SRT.D.11) | 100 Questions with Answers",
         "Law of Sines and Cosines",
         "Understand and apply the Law of Sines and the Law of Cosines to find unknown measurements in right and non-right triangles (e.g., surveying problems, resultant forces).",
         "Free Geometry worksheet on the Law of Sines and the Law of Cosines: area with ½ab sin C, finding sides and angles, and word problems. 100 questions with answers.",
         "Law of Sines: a/sin A = b/sin B = c/sin C.",
         "Law of Cosines: c² = a² + b² − 2ab cos C.",
         body, faq, sets, R, domain="Right Triangles and Trigonometry", grade="geometry")


if __name__ == "__main__":
    build()
