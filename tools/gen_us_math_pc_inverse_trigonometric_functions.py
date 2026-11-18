# -*- coding: utf-8 -*-
"""
US Precalculus: Inverse Trigonometric Functions (Common Core F-TF.B.6, F-TF.B.7)
  python3 tools/gen_us_math_pc_inverse_trigonometric_functions.py
Exact values of sin⁻¹, cos⁻¹ and tan⁻¹, their domains and ranges, compositions such as cos(sin⁻¹ x),
calculator values, and angles in right-triangle problems.
Wrong answers come from real mistakes: giving an angle outside the range (5π/6 instead of π/6), reading
sin⁻¹ x as 1/sin x, using degrees when radians are asked, and choosing the wrong inverse function.
"""
import math
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, num, MINUS, People, fr
from a2_common import sf
from pc_common import GRADE, pis, trig, vhtml, rad, VAL, FLOAT

R = random.Random(97301)
INV = {"sin": "sin⁻¹", "cos": "cos⁻¹", "tan": "tan⁻¹"}
RANGE = {"sin": (-90, 90), "cos": (0, 180), "tan": (-90, 90)}


def principal(fn, sk):
    """angle in degrees with fn(angle) = value, inside the principal range"""
    lo, hi = RANGE[fn]
    for d in range(lo, hi + 1, 15):
        if (fn == "tan" and abs(d) == 90) or (d % 30 and d % 45):
            continue
        if trig(fn, d) == sk:
            return d
    return None


def all_vals(fn):
    keys = ["0", "1/2", "r2/2", "r3/2", "1"] if fn != "tan" else ["0", "r3/3", "1", "r3"]
    out = []
    for k in keys:
        for sg in (1, -1):
            if k == "0" and sg < 0:
                continue
            out.append((sg, k))
    return out


def ang(d, use_rad):
    return pis(rad(d)) if use_rad else (MINUS if d < 0 else "") + "%d°" % abs(d)


# ------------------------------------------------------------ set 1: exact values in radians
def one_exact(r):
    fn = r.choice(["sin", "cos", "tan", "sin", "cos"])
    sk = r.choice(all_vals(fn))
    d = principal(fn, sk)
    use_rad = r.random() < 0.7
    q = "Find the exact value of %s(%s)%s." % (INV[fn], vhtml(sk), "" if use_rad else " in degrees")
    right = ang(d, use_rad)
    other = []
    for dd in range(-180, 361, 15):
        if dd % 30 and dd % 45:
            continue
        if dd != d and trig(fn, dd) == sk and RANGE[fn][0] - 180 <= dd <= 360:
            other.append(dd)
    wr = [ang(other[0], use_rad) if other else ang(d + 180, use_rad), ang(-d, use_rad) if d else ang(90, use_rad), ang(90 - d, use_rad) if 90 - d != d else ang(d + 90, use_rad), ang(180 - d, use_rad)]
    lo, hi = RANGE[fn]
    return T(q, right, wr, "%s gives an angle between %s and %s. The angle there with %s = %s is <b>%s</b>." % (
        INV[fn], ang(lo, use_rad), ang(hi, use_rad), fn, vhtml(sk), right))


# ------------------------------------------------------------ set 2: domain and range
def one_dr(r):
    if r.random() < 0.55:
        fn = r.choice(["sin", "cos"])
        v = r.choice([F(3, 2), F(-5, 4), 2, -2, F(7, 5), F(1, 3), F(-2, 3), F(4, 5), F(-9, 10), 3])
        ok = abs(v) <= 1
        q = "Is %s(%s) defined?" % (INV[fn], sf(v))
        right = "Yes, because %s is between −1 and 1" % sf(v) if ok else "No, because %s is not between −1 and 1" % sf(v)
        wr = (["No, because %s is not between −1 and 1" % sf(v), "No, because %s must be an angle" % sf(v), "Yes, because every number has an inverse sine" if fn == "sin" else "Yes, because every number has an inverse cosine"]
              if ok else ["Yes, because %s is a real number" % sf(v), "Yes, it equals 1 ÷ %s(%s)" % (fn, sf(v)), "No, because %s is not an angle" % sf(v)])
        return T(q, right, wr, "The domain of %s is −1 ≤ <i>x</i> ≤ 1, because sine and cosine are never outside that interval. <b>%s</b>." % (INV[fn], right))
    items = [("What is the range of <i>y</i> = sin⁻¹ <i>x</i>?", "−π/2 ≤ <i>y</i> ≤ π/2", ["0 ≤ <i>y</i> ≤ π", "−1 ≤ <i>y</i> ≤ 1", "0 ≤ <i>y</i> ≤ 2π"], "Sine is restricted to Quadrants I and IV so that it is one-to-one."),
             ("What is the range of <i>y</i> = cos⁻¹ <i>x</i>?", "0 ≤ <i>y</i> ≤ π", ["−π/2 ≤ <i>y</i> ≤ π/2", "−1 ≤ <i>y</i> ≤ 1", "−π ≤ <i>y</i> ≤ π"], "Cosine is restricted to Quadrants I and II so that it is one-to-one."),
             ("What is the range of <i>y</i> = tan⁻¹ <i>x</i>?", "−π/2 &lt; <i>y</i> &lt; π/2", ["0 &lt; <i>y</i> &lt; π", "−π/2 ≤ <i>y</i> ≤ π/2", "All real numbers"], "tan is undefined at ±π/2, so the endpoints are not included."),
             ("What is the domain of <i>y</i> = tan⁻¹ <i>x</i>?", "All real numbers", ["−1 ≤ <i>x</i> ≤ 1", "−π/2 &lt; <i>x</i> &lt; π/2", "<i>x</i> ≥ 0"], "Tangent takes every real value, so any number can go into tan⁻¹."),
             ("What is the domain of <i>y</i> = cos⁻¹ <i>x</i>?", "−1 ≤ <i>x</i> ≤ 1", ["0 ≤ <i>x</i> ≤ π", "All real numbers", "<i>x</i> ≥ 0"], "The outputs of cosine are between −1 and 1, so those are the only inputs of cos⁻¹."),
             ("Why must the domain of sine be restricted to define sin⁻¹?", "Sine is not one-to-one, so it needs a piece where each output happens once", ["Sine is undefined for some angles", "Sine has no negative values", "Sine is a linear function"],
              "A function needs exactly one output for each input, so the inverse needs a one-to-one piece."),
             ("What does sin⁻¹ <i>x</i> mean?", "The angle whose sine is <i>x</i>", ["1 ÷ sin <i>x</i>", "−sin <i>x</i>", "sin <i>x</i> ÷ <i>x</i>"], "The −1 means inverse function, not a reciprocal. 1/sin <i>x</i> is csc <i>x</i>."),
             ("In which quadrants can the answer to cos⁻¹ <i>x</i> be?", "Quadrants I and II", ["Quadrants I and IV", "Quadrants I and III", "Any quadrant"], "The range of cos⁻¹ is 0 to π."),
             ("In which quadrants can the answer to sin⁻¹ <i>x</i> be?", "Quadrants I and IV", ["Quadrants I and II", "Quadrants II and III", "Any quadrant"], "The range of sin⁻¹ is −π/2 to π/2.")]
    q, right, wr, e = r.choice(items)
    return T(q, right, wr, e + " <b>%s</b>." % right)


# ------------------------------------------------------------ set 3: compositions
TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)]


def one_comp(r):
    kind = r.choice(["undo", "undo", "tri", "tri", "tri"])
    if kind == "undo":
        fn = r.choice(["sin", "cos", "tan"])
        d = r.choice([d for d in range(30, 360, 30) if d % 90] + [135, 225, 315, 45])
        sk = trig(fn, d)
        p = principal(fn, sk)
        if p == d:
            return None
        q = "Find the exact value of %s(%s %s)." % (INV[fn], fn, pis(rad(d)))
        right = pis(rad(p))
        return T(q, right, [pis(rad(d)), pis(rad(-p)) if p else pis(rad(180)), pis(rad(180 - p)) if 180 - p != d else pis(rad(p + 90))],
                 "%s %s = %s. %s gives the angle in its range with that value, which is <b>%s</b>, not %s." % (fn, pis(rad(d)), vhtml(sk), INV[fn], right, pis(rad(d))))
    a, b, c = r.choice(TRIPLES)
    if r.random() < 0.5:
        a, b = b, a
    inner = r.choice(["sin", "cos", "tan"])
    neg = r.random() < 0.35
    outer = r.choice([f for f in ["sin", "cos", "tan"] if f != inner])
    # triangle: opposite b, adjacent a, hypotenuse c for the inner angle
    val = {"sin": F(b, c), "cos": F(a, c), "tan": F(b, a)}[inner]
    if neg:
        val = -val
    # angle quadrant: sin⁻¹ and tan⁻¹ of negative -> Quadrant IV; cos⁻¹ of negative -> Quadrant II
    x, y = a, b
    if neg:
        if inner == "cos":
            x = -a
        else:
            y = -b
    res = {"sin": F(y, c), "cos": F(x, c), "tan": F(y, x)}[outer]
    q = "Find the exact value of %s(%s(%s))." % (outer, INV[inner], sf(val))
    right = sf(res)
    return T(q, right, [sf(-res), sf(1 / res), sf(val) if val != res and val != -res and val != 1 / res else sf(-1 / res)],
             "Draw the angle: %s, so use <i>x</i> = %s, <i>y</i> = %s, <i>r</i> = %d (%s). Then %s = <b>%s</b>." % (
                 "%s θ = %s" % (inner, sf(val)), sf(x), sf(y), c, "Quadrant I" if not neg else ("Quadrant II" if inner == "cos" else "Quadrant IV"), outer + " θ", right))


# ------------------------------------------------------------ set 4: calculator values
def one_calc(r):
    fn = r.choice(["sin", "cos", "tan"])
    if fn == "tan":
        v = r.choice([0.25, 0.4, 0.75, 1.5, 2.5, 3, 4, -0.6, -2])
    else:
        v = r.choice([0.15, 0.2, 0.35, 0.4, 0.6, 0.65, 0.8, 0.85, 0.9, -0.3, -0.45, -0.7])
    f = {"sin": math.asin, "cos": math.acos, "tan": math.atan}[fn]
    d = math.degrees(f(v))
    use_rad = r.random() < 0.35
    vt = num(F(str(v)))
    if use_rad:
        q = "Use a calculator. Find %s(%s) in radians, to the nearest hundredth." % (INV[fn], vt)
        rv = f(v)
        right = num(F(round(rv, 2)).limit_denominator(100))
        wr = [num(F(round(d, 2)).limit_denominator(100)), num(F(round(1 / {"sin": math.sin, "cos": math.cos, "tan": math.tan}[fn](v), 2)).limit_denominator(100)),
              num(F(round(math.pi - rv, 2)).limit_denominator(100)) if fn != "cos" else num(F(round(rv - 0.5 if rv > 1 else rv + 0.5, 2)).limit_denominator(100))]
        return T(q, right, wr, "With the calculator in radian mode, %s(%s) ≈ <b>%s</b>." % (INV[fn], vt, right))
    q = "Use a calculator. Find %s(%s) in degrees, to the nearest tenth." % (INV[fn], vt)
    right = num(F(round(d, 1)).limit_denominator(10)) + "°"
    alt = math.degrees(math.acos(v)) if fn == "sin" else math.degrees(math.asin(v)) if fn == "cos" else math.degrees(math.atan(1 / v))
    wr = [num(F(round(alt, 1)).limit_denominator(10)) + "°", num(F(round(180 - d, 1)).limit_denominator(10)) + "°" if fn != "cos" else num(F(round(-d, 1)).limit_denominator(10)) + "°",
          num(F(round(math.radians(d), 2)).limit_denominator(100)) + "°"]
    return T(q, right, wr, "With the calculator in degree mode, %s(%s) ≈ <b>%s</b>. %s" % (INV[fn], vt, right,
                                                                                         {"sin": "The answer is between −90° and 90°.", "cos": "The answer is between 0° and 180°.", "tan": "The answer is between −90° and 90°."}[fn]))


# ------------------------------------------------------------ set 5: angles in right-triangle problems
def one_word(r):
    pp = People(r)
    nm, he, his = pp.next()
    kind = r.choice(["ladder", "ramp", "shadow", "kite", "road", "plane"])
    if kind == "ladder":
        L = r.choice([12, 14, 16, 20, 24])
        base = r.choice([3, 4, 5, 6])
        d = math.degrees(math.acos(base / L))
        q = "%s leans a %d-ft ladder against a wall. The foot of the ladder is %d ft from the wall. To the nearest degree, what angle does the ladder make with the ground?" % (nm, L, base)
        right = "%d°" % round(d)
        return T(q, right, ["%d°" % round(90 - d), "%d°" % round(math.degrees(math.atan(base / L))), "%d°" % round(math.degrees(math.atan(L / base)))],
                 "The ground side is adjacent and the ladder is the hypotenuse: θ = cos⁻¹(%d/%d) ≈ <b>%s</b>." % (base, L, right))
    if kind == "ramp":
        rise = r.choice([1, 2, 3])
        run = r.choice([12, 15, 20, 24])
        d = math.degrees(math.atan(rise / run))
        q = "A ramp rises %d ft over a horizontal distance of %d ft. To the nearest tenth of a degree, what angle does the ramp make with the ground?" % (rise, run)
        right = num(F(round(d, 1)).limit_denominator(10)) + "°"
        return T(q, right, [num(F(round(90 - d, 1)).limit_denominator(10)) + "°", num(F(round(math.degrees(math.asin(rise / run)), 1)).limit_denominator(10)) + "°", num(F(round(d * 10, 1)).limit_denominator(10)) + "°"],
                 "Rise is opposite and run is adjacent: θ = tan⁻¹(%d/%d) ≈ <b>%s</b>." % (rise, run, right))
    if kind == "shadow":
        h = r.choice([6, 15, 30, 40, 50])
        s = r.choice([4, 8, 10, 25, 60])
        d = math.degrees(math.atan(h / s))
        q = "A %d-ft pole casts a %d-ft shadow. To the nearest degree, what is the angle of elevation of the sun?" % (h, s)
        right = "%d°" % round(d)
        return T(q, right, ["%d°" % round(90 - d), "%d°" % round(math.degrees(math.atan(s / h)) + 3), "%d°" % round(math.degrees(math.asin(min(1, s / (h + s)))))],
                 "The pole is opposite the angle and the shadow is adjacent: θ = tan⁻¹(%d/%d) ≈ <b>%s</b>." % (h, s, right))
    if kind == "kite":
        L = r.choice([50, 80, 100, 120])
        h = r.choice([30, 40, 45, 60])
        if h >= L:
            return None
        d = math.degrees(math.asin(h / L))
        q = "%s flies a kite on %d m of string. The kite is %d m above %s hand. To the nearest degree, what angle does the string make with the horizontal?" % (nm, L, h, his)
        right = "%d°" % round(d)
        return T(q, right, ["%d°" % round(90 - d), "%d°" % round(math.degrees(math.atan(h / L))), "%d°" % round(math.degrees(math.acos(h / L)) + 5)],
                 "The height is opposite and the string is the hypotenuse: θ = sin⁻¹(%d/%d) ≈ <b>%s</b>." % (h, L, right))
    if kind == "road":
        g = r.choice([5, 6, 8, 10, 12])
        d = math.degrees(math.atan(g / 100))
        q = "A road sign says the grade is %d%%: the road rises %d ft for every 100 ft horizontally. To the nearest tenth of a degree, what angle does the road make with the horizontal?" % (g, g)
        right = num(F(round(d, 1)).limit_denominator(10)) + "°"
        return T(q, right, [num(F(round(g * 0.9, 1)).limit_denominator(10)) + "°" if round(g * .9, 1) != round(d, 1) else "%d°" % g, "%d°" % g if round(d, 1) != g else "%d°" % (g + 1), num(F(round(90 - d, 1)).limit_denominator(10)) + "°"],
                 "θ = tan⁻¹(%d/100) ≈ <b>%s</b>. A %d%% grade is not %d°." % (g, right, g, g))
    alt = r.choice([1000, 2000, 3000])
    dist = r.choice([8000, 10000, 12000, 15000])
    d = math.degrees(math.atan(alt / dist))
    q = "A plane is %s ft above the ground and %s ft (horizontally) from the start of the runway. To the nearest degree, what is the angle of depression from the plane to the runway?" % (num(alt), num(dist))
    right = "%d°" % round(d)
    return T(q, right, ["%d°" % round(90 - d), "%d°" % round(math.degrees(math.asin(alt / dist))) if round(math.degrees(math.asin(alt / dist))) != round(d) else "%d°" % (round(d) + 2), "%d°" % round(d * 2)],
             "θ = tan⁻¹(%s/%s) ≈ <b>%s</b>. The angle of depression equals the angle of elevation from the runway." % (num(alt), num(dist), right))


def build():
    sets = [S("Exact values", collect(one_exact, 20, R)),
            S("Domain and range", collect(one_dr, 20, R)),
            S("Compositions", collect(one_comp, 20, R)),
            S("Calculator values", collect(one_calc, 20, R)),
            S("Finding angles in word problems", collect(one_word, 20, R))]
    body = lesson(
        "<ul><li>sin⁻¹ <i>x</i> (also arcsin <i>x</i>) is the <b>angle</b> whose sine is <i>x</i>. It is not 1/sin <i>x</i>.</li>"
        "<li>Each inverse gives one angle from a fixed range: sin⁻¹ and tan⁻¹ from −π/2 to π/2, cos⁻¹ from 0 to π.</li>"
        "<li>The domain of sin⁻¹ and cos⁻¹ is −1 ≤ <i>x</i> ≤ 1. tan⁻¹ takes every real number.</li>"
        "<li>For cos(sin⁻¹ <i>x</i>) and similar, draw a right triangle for the inner angle and read the outer ratio.</li></ul>",
        [("Find cos⁻¹(" + MINUS + fr(1, 2) + ").", ["The range is 0 to π", "cos(2π/3) = −1/2"], fr("2π", 3)),
         ("Find sin⁻¹(sin " + fr("5π", 6) + ").", ["sin(5π/6) = 1/2", "The angle in −π/2 to π/2 with sine 1/2 is π/6"], fr("π", 6)),
         ("Find tan(cos⁻¹ " + fr(3, 5) + ").", ["Adjacent 3, hypotenuse 5, so opposite 4", "tan = 4/3"], fr(4, 3))],
        ["Giving an angle outside the range, such as 5π/6 for sin⁻¹(1/2).",
         "Reading sin⁻¹ <i>x</i> as 1/sin <i>x</i>.",
         "Using cos⁻¹ when the sides are opposite and hypotenuse. Match the inverse to the sides you know.",
         "Leaving the calculator in the wrong mode (degrees or radians)."])
    faq = [("What is the difference between sin⁻¹ x and 1/sin x?", "sin⁻¹ x is the inverse function: the angle whose sine is x. 1/sin x is the reciprocal, csc x."),
           ("What are the ranges of the inverse trig functions?", "sin⁻¹ and tan⁻¹ give angles from −π/2 to π/2 (−90° to 90°); cos⁻¹ gives angles from 0 to π (0° to 180°)."),
           ("Why is sin⁻¹(sin 5π/6) not 5π/6?", "Because 5π/6 is outside the range of sin⁻¹. The answer is the angle in the range with the same sine, π/6."),
           ("How do you find cos(sin⁻¹ x)?", "Draw a right triangle with an angle whose sine is x, find the missing side with the Pythagorean theorem and read off the cosine.")]
    make("inverse-trigonometric-functions", 3, "F-TF.B.6",
         "Inverse Trigonometric Functions",
         "Inverse Trig Functions Worksheet: arcsin, arccos, arctan | 100 Questions with Answers",
         "Inverse Trig Functions",
         "Understand that restricting a trigonometric function to a domain on which it is always increasing or always decreasing allows its inverse to be constructed.",
         "Free precalculus worksheet on inverse trigonometric functions: exact values, domain and range, compositions, calculator values and angle word problems. 100 questions.",
         "sin⁻¹ x is the angle whose sine is x, taken from a fixed range.",
         "sin⁻¹ and tan⁻¹: −π/2 to π/2. cos⁻¹: 0 to π.",
         body, faq, sets, R, domain="Trigonometric Functions", grade=GRADE)


if __name__ == "__main__":
    build()
