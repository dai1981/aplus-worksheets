# -*- coding: utf-8 -*-
"""
SG Secondary 3 Maths: Sine and Cosine Rules (MOE syllabus G4: sine and cosine of obtuse angles, area = ½ab sin C,
sine rule and cosine rule for any triangle)
  python3 tools/gen_sg_maths_s3_sine_and_cosine_rules.py
Sine and cosine of obtuse angles, area of a triangle, the sine rule (sides and angles), the cosine rule
(sides), and finding angles with the cosine rule in problems. Sets 2 to 4 reuse the US Geometry makers with
Singapore names for the rules.
Wrong answers come from real mistakes: taking cos of an obtuse angle as positive, using ½ab without sin C,
pairing a side with the wrong angle, and forgetting the − 2bc cos A term.
"""
import math
import random
from sg_sec import num, S, make, lesson, collect, T, fig, MINUS, People, adopt
import gen_us_math_ge_law_of_sines_and_cosines as us

R = random.Random(831200)
adopt(us, R)
P = People(R)

FIX = [("Law of Sines", "Sine rule"), ("Law of Cosines", "Cosine rule"), ("law of sines", "sine rule"), ("law of cosines", "cosine rule"),
       ("m∠", "∠"), ("to the nearest tenth of a degree", "correct to 1 decimal place"), ("to the nearest tenth", "correct to 1 decimal place")]


def wrap(fn):
    def f(r):
        it = fn(r)
        if not it:
            return None
        for k in ("q", "e"):
            for a, b in FIX:
                it[k] = it[k].replace(a, b)
        return it
    return f


def d1(x):
    return ("%.1f" % x).replace("-", MINUS)


def d4(x):
    return ("%.4f" % x).replace("-", MINUS)


def sn(d):
    return math.sin(math.radians(d))


def cs(d):
    return math.cos(math.radians(d))


# ------------------------------------------------------------ set 1: obtuse angles
def one_obtuse(r):
    kind = r.choice(["same", "same", "cosneg", "solve", "solve2"])
    t = r.randint(10, 80)
    if kind == "same":
        q = "Which angle has the same sine as %d°?" % t
        return T(q, "%d°" % (180 - t), ["%d°" % (90 - t), "%d°" % (180 + t), "%d°" % (360 - t)],
                 "sin(180° − θ) = sin θ, so sin %d° = sin %d°: <b>%d°</b>." % (180 - t, t, 180 - t))
    if kind == "cosneg":
        q = "cos %d° = %s. What is cos %d°?" % (t, d4(cs(t)), 180 - t)
        return T(q, d4(-cs(t)), [d4(cs(t)), d4(sn(t)), d4(-sn(t))],
                 "cos(180° − θ) = −cos θ, so cos %d° = <b>%s</b>. Cosines of obtuse angles are negative." % (180 - t, d4(-cs(t))))
    if kind == "solve":
        v = round(sn(t), 4)
        q = "Find the two angles between 0° and 180° for which sin θ = %s. Give your answers correct to 1 decimal place." % d4(v)
        a = math.degrees(math.asin(v))
        right = "θ = %s° or θ = %s°" % (d1(a), d1(180 - a))
        return T(q, right, ["θ = %s° only" % d1(a), "θ = %s° or θ = %s°" % (d1(a), d1(90 + a)), "θ = %s° or θ = %s°" % (d1(a), d1(360 - a))],
                 "sin<sup>−1</sup> %s = %s°. Sine is also positive in the second quadrant: 180° − %s° = %s°. <b>%s</b>." % (d4(v), d1(a), d1(a), d1(180 - a), right))
    v = round(-cs(t), 4)
    q = "Find θ, where 0° &lt; θ &lt; 180°, if cos θ = %s. Give your answer correct to 1 decimal place." % d4(v)
    a = math.degrees(math.acos(v))
    return T(q, "%s°" % d1(a), ["%s°" % d1(180 - a), "%s°" % d1(a - 90), "No solution"],
             "cos θ is negative, so θ is obtuse. cos<sup>−1</sup>(%s) = <b>%s°</b>." % (d4(v), d1(a)))


# ------------------------------------------------------------ set 5: cosine rule for angles and problems
def one_prob(r):
    kind = r.choice(["angle", "angle", "ships", "field", "park"])
    if kind == "angle":
        a, b, c = sorted(r.sample(range(4, 20), 3))
        if a + b <= c:
            return None
        cosC = (a * a + b * b - c * c) / (2 * a * b)
        C = math.degrees(math.acos(cosC))
        q = "A triangle has sides %d cm, %d cm and %d cm. Find the largest angle, correct to 1 decimal place." % (a, b, c)
        wrong = math.degrees(math.acos(max(-1, min(1, (a * a + b * b + c * c) / (2 * a * b))))) if abs((a * a + b * b + c * c) / (2 * a * b)) <= 1 else 180 - C
        return T(q, "%s°" % d1(C), ["%s°" % d1(180 - C), "%s°" % d1(math.degrees(math.acos((b * b + c * c - a * a) / (2 * b * c)))), "%s°" % d1(C / 2)],
                 "The largest angle is opposite the longest side, %d cm. cos C = (%d² + %d² − %d²) ÷ (2 × %d × %d) = %s, so C = <b>%s°</b>." % (c, a, b, c, a, b, d4(cosC), d1(C)))
    if kind == "ships":
        d1_, d2_ = r.randint(8, 40), r.randint(8, 40)
        ang = r.choice([40, 55, 70, 100, 115, 130])
        dist = math.sqrt(d1_ ** 2 + d2_ ** 2 - 2 * d1_ * d2_ * cs(ang))
        q = "Two ships leave a port at the same time. One sails %d km and the other sails %d km, and the angle between their paths is %d°. How far apart are they, correct to 1 decimal place?" % (d1_, d2_, ang)
        return T(q, "%s km" % d1(dist), ["%s km" % d1(math.sqrt(d1_ ** 2 + d2_ ** 2)), "%s km" % d1(math.sqrt(d1_ ** 2 + d2_ ** 2 + 2 * d1_ * d2_ * cs(ang))), "%s km" % d1(dist * dist / 10)],
                 "Cosine rule: <i>d</i>² = %d² + %d² − 2(%d)(%d) cos %d°, so <i>d</i> = <b>%s km</b>." % (d1_, d2_, d1_, d2_, ang, d1(dist)))
    if kind == "field":
        a, b = r.randint(20, 80), r.randint(20, 80)
        C = r.choice([35, 50, 65, 110, 125, 140])
        A = 0.5 * a * b * sn(C)
        q = "A triangular field has two sides of %d m and %d m with an angle of %d° between them. Find its area, correct to 1 decimal place." % (a, b, C)
        return T(q, "%s m²" % d1(A), ["%s m²" % d1(a * b * sn(C)), "%s m²" % d1(0.5 * a * b), "%s m²" % d1(0.5 * a * b * cs(C) if cs(C) > 0 else -0.5 * a * b * cs(C))],
                 "Area = ½ × %d × %d × sin %d° = <b>%s m²</b>." % (a, b, C, d1(A)))
    a = r.randint(30, 90)
    A_ = r.randint(35, 70)
    B_ = r.randint(30, 70)
    if A_ + B_ > 150:
        return None
    C_ = 180 - A_ - B_
    b = a * sn(B_) / sn(A_)
    q = "In a park, paths form a triangle PQR. ∠P = %d°, ∠Q = %d° and QR = %d m. Find PR, correct to 1 decimal place." % (A_, B_, a)
    return T(q, "%s m" % d1(b), ["%s m" % d1(a * sn(A_) / sn(B_)), "%s m" % d1(a * sn(C_) / sn(A_)), "%s m" % d1(a * cs(B_) / cs(A_)) if cs(A_) else "%s m" % d1(b + 1)],
             "QR is opposite ∠P and PR is opposite ∠Q. Sine rule: PR ÷ sin %d° = %d ÷ sin %d°, so PR = <b>%s m</b>." % (B_, a, A_, d1(b)))


def build():
    sets = [S("Sine and cosine of obtuse angles", collect(one_obtuse, 20, R)),
            S("Area of a triangle: ½ab sin C", collect(wrap(us.one_area), 20, R)),
            S("Sine rule: sides and angles", collect(wrap(us.one_ls_side), 10, R) + collect(wrap(us.one_ls_ang), 10, R)),
            S("Cosine rule: finding a side", collect(wrap(us.one_lc_side), 20, R)),
            S("Cosine rule for angles, and problems", collect(one_prob, 20, R))]
    body = lesson(
        "<ul><li>For an obtuse angle: <b>sin(180° − θ) = sin θ</b> and <b>cos(180° − θ) = −cos θ</b>.</li>"
        "<li><b>Area</b> of a triangle = ½<i>ab</i> sin <i>C</i>, where <i>C</i> is the angle between sides <i>a</i> and <i>b</i>.</li>"
        "<li><b>Sine rule</b>: <i>a</i> ÷ sin <i>A</i> = <i>b</i> ÷ sin <i>B</i> = <i>c</i> ÷ sin <i>C</i>. Use it when you know a side and the angle opposite it.</li>"
        "<li><b>Cosine rule</b>: <i>a</i>² = <i>b</i>² + <i>c</i>² − 2<i>bc</i> cos <i>A</i>. Use it with two sides and the angle between them, or with three sides.</li></ul>",
        [("In △ABC, a = 8 cm, ∠A = 40° and ∠B = 65°. Find b.", ["b ÷ sin 65° = 8 ÷ sin 40°", "b = 8 × sin 65° ÷ sin 40°"], "b = 11.3 cm"),
         ("Find the largest angle of a triangle with sides 5, 7 and 10 cm.", ["cos C = (5² + 7² − 10²) ÷ (2 × 5 × 7) = −0.3714"], "C = 111.8°")],
        ["Thinking cos of an obtuse angle is positive. It is negative.",
         "Using ½ab without sin C for a triangle that is not right-angled.",
         "Pairing a side with an angle that is not opposite it in the sine rule.",
         "Adding 2bc cos A instead of subtracting it in the cosine rule."])
    faq = [("When do I use the sine rule?", "When you know a side and the angle opposite it, plus one more side or angle."),
           ("When do I use the cosine rule?", "When you know two sides and the angle between them (to find the third side), or all three sides (to find an angle)."),
           ("What is sin of an obtuse angle?", "sin(180° − θ) = sin θ, so sin 150° = sin 30° = 0.5. Sines of obtuse angles are positive, but cosines are negative."),
           ("How do I find the area of a triangle without the height?", "Use area = ½ab sin C, with two sides and the angle between them.")]
    make(3, "sine-and-cosine-rules", 12, "G4",
         "Sine Rule, Cosine Rule and Area of a Triangle",
         "", "Sine and cosine rules", "",
         "Free Secondary 3 maths worksheets on the sine rule, the cosine rule, area = ½ab sin C and sine and cosine of obtuse angles, with answers correct to 1 decimal place. 100 questions with answers.",
         "Sine rule: a/sin A = b/sin B. Cosine rule: a² = b² + c² − 2bc cos A.",
         "Area of any triangle = ½ab sin C. For obtuse angles, sin stays positive but cos is negative.",
         body, faq, sets, R)


if __name__ == "__main__":
    build()
