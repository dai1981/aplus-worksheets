# -*- coding: utf-8 -*-
"""
US Precalculus: The Six Trigonometric Functions (Common Core F-TF.A.3, F-TF.A.2)
  python3 tools/gen_us_math_pc_six_trigonometric_functions.py
Reference angles, exact values of sine, cosine and tangent in all four quadrants, secant, cosecant and
cotangent, finding the other ratios from one ratio and the quadrant, and points on a circle.
Wrong answers come from real mistakes: forgetting the sign in the quadrant, mixing up sine and cosine,
taking the reciprocal of the wrong function, and measuring the reference angle from the y-axis.
"""
import math
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, num, MINUS, People, fr
from a2_common import sf, ps
from pc_common import GRADE, pis, trig, trig_h, vhtml, rad

R = random.Random(97201)
TH = "θ"
FN6 = ["sin", "cos", "tan", "sec", "csc", "cot"]
SPECIAL = [d for d in range(0, 360, 30)] + [45, 135, 225, 315]
QUAD = {1: "Quadrant I", 2: "Quadrant II", 3: "Quadrant III", 4: "Quadrant IV"}


def quad(d):
    d %= 360
    return 1 if d < 90 else 2 if d < 180 else 3 if d < 270 else 4


def ref(d):
    d %= 360
    return [d, 180 - d, d - 180, 360 - d][quad(d) - 1]


def pv(k):
    h = vhtml(k)
    return "(%s)" % h if h.startswith(MINUS) else h


def ang(d, use_rad):
    return pis(rad(d)) if use_rad else "%d°" % d


# ------------------------------------------------------------ set 1: reference angles
def one_ref(r):
    use_rad = r.random() < 0.4
    if use_rad:
        d = r.choice([d for d in range(15, 360, 15) if d % 90 and (d % 30 == 0 or d % 45 == 0)])
    else:
        d = r.choice([d for d in range(5, 360, 5) if d % 90])
    rf = ref(d)
    q = "What is the reference angle for %s?" % ang(d, use_rad)
    right = ang(rf, use_rad)
    wr = [ang(90 - rf, use_rad), ang((d % 180), use_rad) if d % 180 != rf else ang(180 - rf, use_rad), ang(360 - d, use_rad) if 360 - d != rf else ang(rf + 90, use_rad)]
    how = {1: "it is in Quadrant I, so it is its own reference angle", 2: "180° − %d° = %d°" % (d, rf), 3: "%d° − 180° = %d°" % (d, rf), 4: "360° − %d° = %d°" % (d, rf)}[quad(d)]
    return T(q, right, wr, "The reference angle is the acute angle to the <i>x</i>-axis. %s is in %s: %s. <b>%s</b>." % (ang(d, use_rad), QUAD[quad(d)], how, right))


# ------------------------------------------------------------ set 2: sin, cos, tan in all quadrants
def one_sct(r):
    d = r.choice([d for d in SPECIAL if d % 90])
    fn = r.choice(["sin", "cos", "tan"])
    v = trig(fn, d)
    right = vhtml(v)
    other = {"sin": "cos", "cos": "sin", "tan": "cot"}[fn]
    flip = (-v[0], v[1])
    wr = [vhtml(flip), vhtml(trig(other, d)), vhtml((-trig(other, d)[0], trig(other, d)[1]))]
    q = "Find the exact value of %s %s." % (fn, "%d°" % d)
    return T(q, right, wr, "Reference angle %d°: %s %d° = %s. In %s, %s is %s. <b>%s</b>." % (
        ref(d), fn, ref(d), vhtml(trig(fn, ref(d))), QUAD[quad(d)], fn, "positive" if v[0] > 0 else "negative", right))


# ------------------------------------------------------------ set 3: sec, csc, cot (radians)
def one_rec(r):
    d = r.choice([d for d in SPECIAL])
    fn = r.choice(["sec", "csc", "cot"])
    v = trig(fn, d)
    base = {"sec": "cos", "csc": "sin", "cot": "tan"}[fn]
    wrongfn = {"sec": "sin", "csc": "cos", "cot": "tan"}[fn]
    bv = trig(base, d)
    if v is None:
        right = "undefined"
        wr = [vhtml(bv) if bv else "1", "0", "1" if vhtml(bv) != "1" else MINUS + "1"]
        return T("Find the exact value of %s %s." % (fn, pis(rad(d))), right, wr,
                 "%s = 1 ÷ %s, and %s %s = 0. Dividing by 0 is not allowed, so it is <b>undefined</b>." % (fn, base, base, pis(rad(d))))
    q = "Find the exact value of %s %s." % (fn, pis(rad(d)))
    right = vhtml(v)
    wr = [vhtml(bv), vhtml(trig(wrongfn, d)) if wrongfn != "tan" else vhtml(trig("tan", d)) if trig("tan", d) else "undefined", vhtml((-v[0], v[1]))]
    return T(q, right, wr, "%s = 1 ÷ %s. %s %s = %s, so %s %s = <b>%s</b>." % (fn, base, base, pis(rad(d)), vhtml(bv), fn, pis(rad(d)), right))


# ------------------------------------------------------------ set 4: one ratio and the quadrant
TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29)]


def one_other(r):
    a, b, c = r.choice(TRIPLES)
    if r.random() < 0.5:
        a, b = b, a
    qd = r.choice([1, 2, 3, 4])
    sx = 1 if qd in (1, 4) else -1
    sy = 1 if qd in (1, 2) else -1
    x, y = sx * a, sy * b
    given = r.choice(["sin", "cos", "tan"])
    gv = {"sin": F(y, c), "cos": F(x, c), "tan": F(y, x)}[given]
    want = r.choice([f for f in FN6 if f != given])
    vals = {"sin": F(y, c), "cos": F(x, c), "tan": F(y, x), "csc": F(c, y), "sec": F(c, x), "cot": F(x, y)}
    ans = vals[want]
    q = "If %s %s = %s and %s is in %s, what is %s %s?" % (given, TH, sf(gv), TH, QUAD[qd], want, TH)
    right = sf(ans)
    wr = [sf(-ans), sf(1 / ans), sf(-1 / ans)]
    return T(q, right, wr, "Use a right triangle with sides %d, %d and %d. In %s, <i>x</i> is %s and <i>y</i> is %s, so <i>x</i> = %s, <i>y</i> = %s, <i>r</i> = %d. %s %s = <b>%s</b>." % (
        a, b, c, QUAD[qd], "positive" if sx > 0 else "negative", "positive" if sy > 0 else "negative", sf(x), sf(y), c, want, TH, right))


# ------------------------------------------------------------ set 5: points on a circle and applications
def one_word(r):
    kind = r.choice(["point", "point", "wheel", "wheel", "terminal"])
    if kind == "terminal":
        a, b, c = r.choice(TRIPLES)
        x, y = r.choice([1, -1]) * a, r.choice([1, -1]) * b
        fn = r.choice(FN6)
        vals = {"sin": F(y, c), "cos": F(x, c), "tan": F(y, x), "csc": F(c, y), "sec": F(c, x), "cot": F(x, y)}
        q = "The point (%s, %s) is on the terminal side of an angle %s in standard position. What is %s %s?" % (sf(x), sf(y), TH, fn, TH)
        right = sf(vals[fn])
        return T(q, right, [sf(-vals[fn]), sf(1 / vals[fn]), sf(F(y, x)) if fn not in ("tan",) and F(y, x) != vals[fn] else sf(F(x, y)) if F(x, y) != vals[fn] else sf(F(c, 1))],
                 "<i>r</i> = √(%s² + %s²) = %d. Then sin = <i>y</i>/<i>r</i>, cos = <i>x</i>/<i>r</i>, tan = <i>y</i>/<i>x</i> and the reciprocals. %s %s = <b>%s</b>." % (ps(x), ps(y), c, fn, TH, right))
    if kind == "point":
        rr = r.choice([2, 4, 6, 8, 10])
        d = r.choice([d for d in SPECIAL if d % 90 and d % 60 and True] + [120, 150, 210, 240, 300, 330])
        sk, ck = trig("sin", d), trig("cos", d)
        def mulh(k):
            s, key = k
            sg = MINUS if s < 0 else ""
            m = {"1/2": str(rr // 2), "r2/2": ("%d√2" % (rr // 2)) if rr // 2 != 1 else "√2", "r3/2": ("%d√3" % (rr // 2)) if rr // 2 != 1 else "√3"}[key]
            return sg + m
        q = "A point moves counterclockwise around a circle of radius %d centered at the origin, starting at (%d, 0). Where is it after turning %s?" % (rr, rr, pis(rad(d)))
        right = "(%s, %s)" % (mulh(ck), mulh(sk))
        return T(q, right, ["(%s, %s)" % (mulh(sk), mulh(ck)), "(%s, %s)" % (mulh((-ck[0], ck[1])), mulh(sk)), "(%s, %s)" % (mulh(ck), mulh((-sk[0], sk[1])))],
                 "The point is (<i>r</i> cos %s, <i>r</i> sin %s) = (%d · %s, %d · %s) = <b>%s</b>." % (TH, TH, rr, pv(ck), rr, pv(sk), right))
    rr = r.choice([20, 30, 40, 50])
    hub = rr + r.choice([2, 4, 5])
    d = r.choice([30, 60, 120, 150, 210, 240, 300, 330, 45, 135])
    s = math.sin(math.radians(d))
    h = hub + rr * s
    q = ("A Ferris wheel has a radius of %d ft, and its center is %d ft above the ground. A seat starts level with the center on the right and turns %d° counterclockwise. "
         "To the nearest foot, how high is the seat?" % (rr, hub, d))
    right = "%d ft" % round(h)
    return T(q, right, ["%d ft" % round(hub + rr * math.cos(math.radians(d))) if round(hub + rr * math.cos(math.radians(d))) != round(h) else "%d ft" % round(h + 5),
                        "%d ft" % abs(round(rr * s)) if abs(round(rr * s)) != round(h) else "%d ft" % round(h - 3), "%d ft" % round(hub - rr * s) if round(hub - rr * s) != round(h) else "%d ft" % round(h + 2)],
             "Height = center + <i>r</i> sin %s = %d + %d sin %d° ≈ %d %s %.1f ≈ <b>%s</b>." % (TH, hub, rr, d, hub, "+" if s > 0 else MINUS, abs(rr * s), right))


def build():
    sets = [S("Reference angles", collect(one_ref, 20, R)),
            S("Sine, cosine and tangent in all quadrants", collect(one_sct, 20, R)),
            S("Secant, cosecant and cotangent", collect(one_rec, 20, R)),
            S("Finding the other ratios", collect(one_other, 20, R)),
            S("Points on a circle and applications", collect(one_word, 20, R))]
    body = lesson(
        "<ul><li>For a point (<i>x</i>, <i>y</i>) on the terminal side at distance <i>r</i> from the origin: sin θ = <i>y</i>/<i>r</i>, cos θ = <i>x</i>/<i>r</i>, tan θ = <i>y</i>/<i>x</i>.</li>"
        "<li>The reciprocals: csc θ = 1/sin θ, sec θ = 1/cos θ, cot θ = 1/tan θ.</li>"
        "<li>The <b>reference angle</b> is the acute angle to the <i>x</i>-axis. Find the value for the reference angle, then choose the sign from the quadrant.</li>"
        "<li>Signs: all positive in Quadrant I, sine (and csc) positive in II, tangent (and cot) positive in III, cosine (and sec) positive in IV.</li></ul>",
        [("Find cos 240°.", ["Quadrant III, reference angle 240° − 180° = 60°", "cos 60° = " + fr(1, 2) + ", and cosine is negative in III"], MINUS + fr(1, 2)),
         ("If sin θ = " + fr(3, 5) + " and θ is in Quadrant II, find tan θ.", ["<i>y</i> = 3, <i>r</i> = 5, so |<i>x</i>| = 4", "In Quadrant II, <i>x</i> = −4", "tan θ = 3/(−4)"], MINUS + fr(3, 4))],
        ["Forgetting the sign from the quadrant.",
         "Taking sec as 1/sin. sec goes with cos, csc goes with sin.",
         "Measuring the reference angle to the <i>y</i>-axis. Always use the <i>x</i>-axis.",
         "Mixing up sine and cosine: cosine is the <i>x</i>-coordinate, sine is the <i>y</i>-coordinate."])
    faq = [("What are the six trigonometric functions?", "Sine, cosine and tangent, and their reciprocals cosecant, secant and cotangent."),
           ("How do you find a reference angle?", "Find the acute angle between the terminal side and the x-axis: 180° − θ in Quadrant II, θ − 180° in Quadrant III and 360° − θ in Quadrant IV."),
           ("How do I remember which functions are positive?", "All are positive in Quadrant I, sine in II, tangent in III and cosine in IV. Some students say All Students Take Calculus."),
           ("When is a trigonometric function undefined?", "When its denominator is 0. For example, tan 90° and sec 90° are undefined because cos 90° = 0.")]
    make("six-trigonometric-functions", 2, "F-TF.A.3",
         "The Six Trigonometric Functions",
         "Six Trigonometric Functions Worksheet: Reference Angles and Exact Values | 100 Questions",
         "Six Trig Functions",
         "Use special triangles to determine geometrically the values of sine, cosine, tangent for π/3, π/4 and π/6, and use the unit circle to express the values of sine, cosine, and tangent for π−x, π+x, and 2π−x in terms of their values for x, where x is any real number.",
         "Free precalculus worksheet on the six trigonometric functions: reference angles, exact values in all quadrants, secant, cosecant, cotangent and points on a circle. 100 questions.",
         "Find the value for the reference angle, then take the sign from the quadrant.",
         "sec = 1/cos, csc = 1/sin, cot = 1/tan.",
         body, faq, sets, R, domain="Trigonometric Functions", grade=GRADE)


if __name__ == "__main__":
    build()
