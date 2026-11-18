# -*- coding: utf-8 -*-
"""
US Algebra 2: Radians and the Unit Circle (Common Core F-TF.A.1, F-TF.A.2, F-TF.C.8)
  python3 tools/gen_us_math_a2_unit_circle_and_radians.py
Converting between degrees and radians, coterminal and reference angles, exact sine, cosine and tangent
values from the unit circle, signs by quadrant, and the Pythagorean identity.
Wrong answers come from real mistakes: multiplying by 180/π instead of π/180, mixing up sine and cosine
(y and x), using the wrong sign for the quadrant, and taking the reference angle from the y-axis.
"""
import math
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, fig, num, MINUS, fr
from a2_common import sf
from us_geo import Canvas, pol, RED, BLUE, GREEN

R = random.Random(96301)
TH = "<i>θ</i>"
ANG = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]
R2, R3 = "√2", "√3"
VAL = {0: ("0", "1"), 30: ("1/2", "√3/2"), 45: ("√2/2", "√2/2"), 60: ("√3/2", "1/2"), 90: ("1", "0")}


def rad(deg):
    f = F(deg, 180)
    if f == 0:
        return "0"
    n, d = f.numerator, f.denominator
    top = ("" if abs(n) == 1 else str(abs(n))) + "π"
    s = top if d == 1 else fr(top, d)
    return (MINUS if n < 0 else "") + s


def frac_txt(t, neg=False):
    """'√3/2' -> html fraction"""
    if "/" in t:
        a, b = t.split("/")
        s = fr(a, b)
    else:
        s = t
    if neg and t != "0":
        s = MINUS + s
    return s


def trig(deg, fn):
    ref = deg % 180
    ref = ref if ref <= 90 else 180 - ref
    s, c = VAL[ref]
    q = (deg % 360) // 90 if deg % 90 else None
    d = deg % 360
    sin_neg = 180 < d < 360
    cos_neg = 90 < d < 270
    if fn == "sin":
        return frac_txt(s, sin_neg and s != "0")
    if fn == "cos":
        return frac_txt(c, cos_neg and c != "0")
    sv = {"0": 0, "1/2": 0.5, "√2/2": 0.7, "√3/2": 0.86, "1": 1}
    if c == "0":
        return "Undefined"
    tv = {0: "0", 30: "√3/3", 45: "1", 60: "√3", 90: None}[ref]
    neg = sin_neg != cos_neg and tv != "0"
    return frac_txt(tv, neg)


def circle_fig(deg):
    c = Canvas()
    O = (120, 120)
    c.circle(O, 90)
    c.seg((20, 120), (220, 120), w=1.5)
    c.seg((120, 20), (120, 220), w=1.5)
    P = pol(O[0], O[1], 90, deg)
    c.seg(O, P, col=BLUE)
    c.dot(P, 4, RED)
    c.text((P[0] + (14 if P[0] >= 120 else -14), P[1] + (-12 if P[1] <= 120 else 14)), "P", 15, RED)
    c.text((228, 124), "<i>x</i>", 13)
    c.text((124, 14), "<i>y</i>", 13)
    return c.svg("unit circle with a point P on the terminal side of the angle")


# ------------------------------------------------------------ set 1: degrees and radians
def one_conv(r):
    deg = r.choice([30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360, 20, 75, 540, -60, -135])
    if r.random() < 0.5:
        q = "Convert %s to radians." % B("%s°" % sf(deg))
        right = rad(deg)
        wr = [rad(2 * deg) if deg % 360 else rad(deg // 2), "%sπ" % sf(deg), (fr("%sπ" % num(abs(deg) * 180) if False else num(abs(deg) * 180), "π") if deg > 0 else MINUS + fr(num(-deg * 180), "π")), rad(-deg)]
        return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], "Multiply by π/180: %s × π/180 = <b>%s</b>." % (sf(deg), right))
    q = "Convert %s radians to degrees." % B(rad(deg))
    right = "%s°" % sf(deg)
    wr = ["%s°" % sf(F(deg, 2)), "%s°" % sf(-deg), "%s°" % sf(deg * 2), "%s°" % sf(deg + 180)]
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], "Multiply by 180/π (replace π with 180°): <b>%s</b>." % right)


# ------------------------------------------------------------ set 2: coterminal and reference angles
def one_ref(r):
    kind = r.choice(["cot", "ref", "ref", "quad"])
    deg = r.choice([x for x in range(15, 360, 5) if x % 90])
    if kind == "cot":
        k = r.choice([1, -1])
        right = "%s°" % sf(deg + 360 * k)
        q = "Which angle is coterminal with %s?" % B("%d°" % deg)
        return T(q, right, ["%s°" % sf(deg + 180), "%s°" % sf(-deg), "%s°" % sf(360 - deg)],
                 "Coterminal angles differ by a multiple of 360°: %d° %s 360° = <b>%s</b>." % (deg, "+" if k > 0 else MINUS, right))
    if kind == "quad":
        quad = deg // 90 + 1
        names = ["I", "II", "III", "IV"]
        right = "Quadrant %s" % names[quad - 1]
        return T("In which quadrant does the terminal side of %s lie?" % B("%d°" % deg), right, ["Quadrant %s" % n for n in names if n != names[quad - 1]],
                 "Quadrant I is 0° to 90°, II is 90° to 180°, III is 180° to 270° and IV is 270° to 360°. <b>%s</b>." % right)
    if deg < 90:
        ref = deg
    elif deg < 180:
        ref = 180 - deg
    elif deg < 270:
        ref = deg - 180
    else:
        ref = 360 - deg
    q = "Find the reference angle for %s." % B("%d°" % deg)
    wr = [abs(90 - deg % 180) if abs(90 - deg % 180) != ref else ref + 10, 360 - deg if 360 - deg != ref else 180 - ref, deg - 90 if deg > 90 and deg - 90 != ref else ref + 5]
    return T(q, "%d°" % ref, ["%d°" % w for w in dict.fromkeys(wr) if w != ref and w > 0][:3],
             "The reference angle is the acute angle between the terminal side and the <i>x</i>-axis: <b>%d°</b>." % ref)


# ------------------------------------------------------------ set 3: exact values
def one_exact(r):
    deg = r.choice(ANG + [360])
    fn = r.choice(["sin", "cos", "sin", "cos", "tan"])
    right = trig(deg, fn)
    use_rad = r.random() < 0.5
    ang = rad(deg) if use_rad else "%d°" % deg
    q = "Find the exact value of %s." % B("%s %s" % (fn, ang if not use_rad else "(%s)" % ang if "span" in ang else ang))
    other = "cos" if fn == "sin" else "sin"
    pool = [trig(deg, other) if fn != "tan" else trig(deg, "sin"), trig(deg + 180, fn) if fn != "tan" else trig(deg + 90, "tan"), trig((deg + 90) % 360, fn)]
    pool += ["0", "1", MINUS + "1", frac_txt("√3/2"), frac_txt("1/2"), frac_txt("√2/2"), MINUS + frac_txt("1/2"), "Undefined"]
    wr = [w for w in dict.fromkeys(pool) if w != right]
    ref = deg % 180 if deg % 180 <= 90 else 180 - deg % 180
    expl = "On the unit circle, cos %s is the <i>x</i>-coordinate and sin %s is the <i>y</i>-coordinate (tan = sin ÷ cos). " % (TH, TH)
    expl += "The reference angle is %d°, and the quadrant decides the sign. <b>%s</b>." % (ref, right)
    return T(q, right, wr[:3], expl)


# ------------------------------------------------------------ set 4: signs and points on the unit circle
def one_sign(r):
    kind = r.choice(["point", "point", "sign", "sign"])
    if kind == "point":
        deg = r.choice([30, 45, 60, 120, 135, 150, 210, 225, 240, 300, 315, 330])
        x, y = trig(deg, "cos"), trig(deg, "sin")
        right = "(%s, %s)" % (x, y)
        q = "Which point is on the unit circle at an angle of %s?%s" % (B("%d°" % deg if r.random() < 0.5 else rad(deg) + " radians"), fig(circle_fig(deg)))
        return T(q, right, ["(%s, %s)" % (y, x), "(%s, %s)" % (x.replace(MINUS, "") if MINUS in x else MINUS + x, y), "(%s, %s)" % (x, y.replace(MINUS, "") if MINUS in y else MINUS + y)],
                 "The point is (cos %s, sin %s). The reference angle gives the sizes and the quadrant gives the signs. <b>%s</b>." % (TH, TH, right))
    q_, fs = r.choice([("II", "sin"), ("III", "tan"), ("IV", "cos"), ("I", "all")])
    s1, s2 = r.choice([("positive", "negative"), ("negative", "positive"), ("negative", "negative"), ("positive", "positive")])
    combos = {("positive", "negative"): "II", ("negative", "negative"): "III", ("negative", "positive"): "IV", ("positive", "positive"): "I"}
    right = "Quadrant %s" % combos[(s1, s2)]
    q = "sin %s is %s and cos %s is %s. In which quadrant is the terminal side of %s?" % (TH, s1, TH, s2, TH)
    return T(q, right, ["Quadrant %s" % n for n in ["I", "II", "III", "IV"] if "Quadrant %s" % n != right],
             "sin is the <i>y</i>-coordinate and cos is the <i>x</i>-coordinate. <i>y</i> %s and <i>x</i> %s gives <b>%s</b>." % (s1, s2, right))


# ------------------------------------------------------------ set 5: Pythagorean identity
def one_id(r):
    a, b, c = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29)])
    quad = r.choice([1, 2, 3, 4])
    given = r.choice(["sin", "cos"])
    names = {1: "I", 2: "II", 3: "III", 4: "IV"}
    sin_sign = 1 if quad in (1, 2) else -1
    cos_sign = 1 if quad in (1, 4) else -1
    sv, cv = F(a * sin_sign, c), F(b * cos_sign, c)
    want = r.choice(["cos" if given == "sin" else "sin", "tan"])
    gv = sv if given == "sin" else cv
    q = "%s %s = %s and %s is in Quadrant %s. Find %s %s." % (given, TH, sf(gv), TH, names[quad], want, TH)
    ans = cv if want == "cos" else (sv if want == "sin" else sv / cv)
    wr = [-ans, F(ans.denominator, ans.numerator) if ans else 1, (cv / sv if want == "tan" else gv)]
    return T(q, sf(ans), [sf(w) for w in dict.fromkeys(wr) if w != ans][:3],
             "Use sin² %s + cos² %s = 1: the missing value is ±%s. In Quadrant %s, sin is %s and cos is %s. %s<b>%s</b>." % (
                 TH, TH, fr(b if given == "sin" else a, c), names[quad], "positive" if sin_sign > 0 else "negative", "positive" if cos_sign > 0 else "negative",
                 "tan = sin ÷ cos. " if want == "tan" else "", sf(ans)))


def build():
    sets = [S("Degrees and radians", collect(one_conv, 20, R)),
            S("Coterminal and reference angles", collect(one_ref, 20, R)),
            S("Exact values on the unit circle", collect(one_exact, 20, R)),
            S("Points and signs", collect(one_sign, 20, R)),
            S("The Pythagorean identity", collect(one_id, 20, R))]
    body = lesson(
        "<p>A <b>radian</b> is the angle that cuts off an arc equal to the radius. π radians = 180°, so multiply by π/180 to change degrees to radians and by 180/π to change back.</p>"
        "<p>On the <b>unit circle</b> (radius 1), the point at angle %s is (cos %s, sin %s), and tan %s = sin %s ÷ cos %s.</p>"
        "<ul><li>Use the <b>reference angle</b> (the acute angle to the <i>x</i>-axis) to get the size: 30°, 45° or 60° give 1/2, √2/2 and √3/2.</li>"
        "<li>Use the <b>quadrant</b> to get the sign: in II only sin is positive, in III only tan, in IV only cos.</li>"
        "<li><b>Pythagorean identity</b>: sin² %s + cos² %s = 1.</li></ul>" % (TH, TH, TH, TH, TH, TH, TH, TH),
        [("Find cos 210°.", ["Reference angle 30°, so |cos| = √3/2", "Quadrant III: cos is negative"], "%s√3/2" % MINUS),
         ("sin %s = 3/5 in Quadrant II. Find cos %s." % (TH, TH), ["cos² %s = 1 %s 9/25 = 16/25" % (TH, MINUS), "cos is negative in II"], "%s4/5" % MINUS)],
        ["Using 180/π to change degrees to radians. Use π/180.",
         "Swapping sine and cosine: sine is the <i>y</i>-coordinate.",
         "Forgetting the sign from the quadrant.",
         "Measuring the reference angle from the <i>y</i>-axis instead of the <i>x</i>-axis."])
    faq = [("How do you convert degrees to radians?", "Multiply by π/180. For example, 120° × π/180 = 2π/3."),
           ("What are the coordinates on the unit circle?", "The point at angle θ is (cos θ, sin θ). The x-coordinate is cosine and the y-coordinate is sine."),
           ("What is a reference angle?", "The acute angle between the terminal side of an angle and the x-axis. It gives the size of the trig values."),
           ("What is the Pythagorean identity?", "sin²θ + cos²θ = 1. If you know one of sin θ or cos θ and the quadrant, you can find the other.")]
    make("unit-circle-and-radians", 13, "F-TF.A.2",
         "Radians and the Unit Circle",
         "Unit Circle Worksheet: Radians, Reference Angles, Exact Trig Values (Algebra 2) | 100 Questions",
         "Unit Circle and Radians",
         "Explain how the unit circle in the coordinate plane enables the extension of trigonometric functions to all real numbers, interpreted as radian measures of angles traversed counterclockwise around the unit circle.",
         "Free Algebra 2 worksheet on radians and the unit circle: converting degrees and radians, coterminal and reference angles, exact sin, cos and tan, and sin² + cos² = 1. 100 questions.",
         "π radians = 180°. On the unit circle, the point at θ is (cos θ, sin θ).",
         "Reference angles give the size; the quadrant gives the sign.",
         body, faq, sets, R, domain="Trigonometric Functions", grade="algebra-2")


if __name__ == "__main__":
    build()
