# -*- coding: utf-8 -*-
"""
India Class 11 Maths, NCERT Chapter 3: Trigonometric Functions (CBSE Unit I Sets and Functions)
  python3 tools/gen_in_maths_c11_trigonometric_functions.py
Degrees and radians, arc length l = rθ (π = 22/7), signs and values of the six trigonometric functions in the four
quadrants, values of large and negative angles, sum and difference formulas and multiple angles, and the period of
sin kx and cos kx (own makers and US Algebra 2 / Precalculus makers).
Wrong answers come from real mistakes: multiplying by 180/π the wrong way, using θ in degrees in l = rθ, the wrong
sign in a quadrant, and sin(A + B) = sin A + sin B.
"""
import random
from fractions import Fraction as F
from in_sr import U, T2, use, pi, X
from in_common import num, fv
import gen_us_math_a2_unit_circle_and_radians as uc
import gen_us_math_pc_six_trigonometric_functions as six
import gen_us_math_pc_sum_and_difference_formulas as sd
import gen_us_math_pc_trigonometric_identities as ti

R = random.Random(911103)
Q = [("Quadrant IV", "the fourth quadrant"), ("Quadrant III", "the third quadrant"), ("Quadrant II", "the second quadrant"), ("Quadrant I", "the first quadrant")]
conv = use(uc, "one_conv", R, Q)
exact = use(uc, "one_exact", R, Q)
sign = use(uc, "one_sign", R, Q)
rec = use(six, "one_rec", R, Q)
other = use(six, "one_other", R, Q)
sexact = use(sd, "one_exact", R, Q)
given = use(sd, "one_given", R, Q)
double = use(sd, "one_double", R, Q)
val = use(ti, "one_val", R, Q)


def one_arc(r):
    k = r.choice(["l", "theta", "radius", "clock"])
    if k == "l":
        rad = r.choice([7, 14, 21, 28, 35])
        deg = r.choice([30, 45, 60, 90, 120, 150, 180, 72, 36])
        l = F(22, 7) * rad * deg / 180
        return T2("Find the length of the arc of a circle of radius %d cm that subtends an angle of %d° at the centre (π = 22/7)." % (rad, deg), "%s cm" % fv(l),
                  ["%s cm" % fv(l * 2), "%s cm" % fv(rad * deg), "%s cm" % fv(l / 2)],
                  "θ = %d° = %s radian. l = rθ = %d × %s = <b>%s cm</b>." % (deg, pi(F(deg, 180)), rad, pi(F(deg, 180)).replace("π", "(22/7)") if F(deg, 180).numerator != 1 else "(22/7)/%d" % F(deg, 180).denominator, fv(l)))
    if k == "theta":
        rad = r.choice([5, 10, 15, 20, 25, 30])
        l = r.choice([5, 10, 15, 20, 25, 30, 40])
        th = F(l, rad)
        return T2("An arc of length %d cm subtends an angle θ at the centre of a circle of radius %d cm. Find θ in radians." % (l, rad), fv(th) + " radian" + ("" if th == 1 else "s"),
                  [fv(1 / th) + " radian" + ("" if 1 / th == 1 else "s"), fv(th * 180) + "°", fv(l * rad) + " radians"],
                  "θ = l ÷ r = %d ÷ %d = <b>%s</b> radian%s." % (l, rad, fv(th), "" if th == 1 else "s"))
    if k == "radius":
        deg = r.choice([30, 45, 60, 90, 120, 180])
        l = F(22, 7) * 7 * r.choice([1, 2, 3]) * deg / 180
        rad = l / (F(22, 7) * deg / 180)
        return T2("An arc of length %s cm subtends an angle of %d° at the centre. Find the radius (π = 22/7)." % (fv(l), deg), "%s cm" % fv(rad),
                  ["%s cm" % fv(rad * 2), "%s cm" % fv(l * deg), "%s cm" % fv(rad / 2)],
                  "%d° = %s radian, and r = l ÷ θ = <b>%s cm</b>." % (deg, pi(F(deg, 180)), fv(rad)))
    m = r.choice([10, 15, 20, 30, 40, 45, 50])
    L = r.choice([F(21, 10), F(7, 2), F(14, 10), 7, 14, F(105, 10)])
    deg = 6 * m
    d = F(22, 7) * L * deg / 180
    return T2("The minute hand of a clock is %s cm long. How far does its tip move in %d minutes (π = 22/7)?" % (num(L), m), "%s cm" % (num(d) or fv(d)),
              ["%s cm" % (num(d * 2) or fv(d * 2)), "%s cm" % (num(L * m) or fv(L * m)), "%s cm" % (num(d / 2) or fv(d / 2))],
              "In %d minutes the hand turns %d × 6° = %d° = %s radian. Distance = rθ = <b>%s cm</b>." % (m, m, deg, pi(F(deg, 180)), num(d) or fv(d)))


VAL = {0: ("0", "1", "0"), 30: ("1/2", "√3/2", "1/√3"), 45: ("1/√2", "1/√2", "1"), 60: ("√3/2", "1/2", "√3"), 90: ("1", "0", "not defined")}


def ref(deg):
    d = deg % 360
    q = d // 90
    if d % 90 == 0:
        return None
    base = d if q == 0 else (180 - d if q == 1 else (d - 180 if q == 2 else 360 - d))
    return base, q


def one_big(r):
    fn = r.choice(["sin", "cos", "tan"])
    base = r.choice([30, 45, 60])
    q = r.randrange(4)
    deg = [base, 180 - base, 180 + base, 360 - base][q] + 360 * r.choice([1, 2, 3, -1, -2])
    if r.random() < 0.3:
        deg = -deg
    b, qq = ref(deg)
    i = ["sin", "cos", "tan"].index(fn)
    v = VAL[b][i]
    pos = {"sin": (0, 1), "cos": (0, 3), "tan": (0, 2)}[fn]
    neg = qq not in pos
    right = ("−" if neg else "") + v
    other = ("" if neg else "−") + v
    wrong_f = VAL[b][(i + 1) % 2] if fn != "tan" else VAL[90 - b][2]
    shown = str(deg).replace("-", "−")
    return T2("Find the value of %s(%s°)." % (fn, shown), right, [other, ("−" if neg else "") + wrong_f, ("" if neg else "−") + wrong_f],
              "%s° and %s° end in the same place (whole turns of 360° do not matter). That is in the %s quadrant, with reference angle %d°, where %s is %s. So %s(%s°) = <b>%s</b>." % (
                  shown, str(deg % 360), ["first", "second", "third", "fourth"][qq], b, fn, "negative" if neg else "positive", fn, shown, right))


def one_period(r):
    k = r.randint(2, 6)
    fn = r.choice(["sin", "cos", "tan"])
    p = F(1, k) if fn == "tan" else F(2, k)
    a = r.choice([1, 2, 3, 5])
    if r.random() < 0.6:
        return T2("What is the period of f(%s) = %s%s %d%s?" % (X, "" if a == 1 else a, fn, k, X), pi(p), [pi(p * k * k) if fn != "tan" else pi(1), pi(p * 2) if fn != "tan" else pi(F(2, k)), pi(F(k, 2))],
                  "%s has period %s, so %s %d%s has period %s ÷ %d = <b>%s</b>." % (fn, "π" if fn == "tan" else "2π", fn, k, X, "π" if fn == "tan" else "2π", k, pi(p)))
    if fn == "tan":
        return None
    b = r.randint(-3, 4)
    lo, hi = b - a, b + a
    sh = (" + %d" % b) if b > 0 else (" − %d" % -b if b < 0 else "")
    return T2("What is the range of f(%s) = %d %s %s%s?" % (X, a, fn, X, sh), "[%s, %s]" % (num(lo), num(hi)),
              ["[%s, %s]" % (num(-1 + b), num(1 + b)), "[%s, %s]" % (num(-a), num(a)), "(%s, %s)" % (num(lo), num(hi))],
              "%s %s lies between −1 and 1, so %d %s %s lies between %s and %s: the range is <b>[%s, %s]</b>." % (fn, X, a, fn, X, num(-a), num(a), num(lo), num(hi)))


U(11, 3, "trigonometric-functions", 3, "SF", "Trigonometric Functions: Radians, Values, Signs and Sum Formulas", "trigonometric functions",
  "Positive and negative angles; measuring angles in radians and in degrees and conversion from one measure to another; definition of trigonometric functions with the help of the unit circle; truth of the identity sin²x + cos²x = 1 for all x; signs of trigonometric functions; domain and range of trigonometric functions and their graphs; expressing sin(x ± y) and cos(x ± y) in terms of sin x, sin y, cos x and cos y; identities related to sin 2x, cos 2x, tan 2x, sin 3x, cos 3x and tan 3x (summary of the CBSE syllabus)",
  "Class 11 Trigonometric Functions worksheet (NCERT Chapter 3): radians and degrees, arc length, values in all four quadrants, sum and difference formulas, multiple angles, period and range. 100 questions with answers.",
  "π radian = 180°; l = rθ with θ in radians.", "All, Sin, Tan, Cos: the functions that are positive in quadrants I, II, III, IV.",
  "<ul><li>π radian = 180°, so 1° = π/180 radian. To change degrees to radians multiply by π/180.</li>"
  "<li>Arc length: l = rθ, with θ in radians.</li>"
  "<li>Signs: all positive in the first quadrant, only sin (and cosec) in the second, tan (and cot) in the third, cos (and sec) in the fourth.</li>"
  "<li>Large angles: take away whole turns of 360°, then use the reference angle and the sign of the quadrant.</li>"
  "<li>sin(x + y) = sin x cos y + cos x sin y; cos(x + y) = cos x cos y − sin x sin y; sin 2x = 2 sin x cos x; cos 2x = cos²x − sin²x.</li></ul>",
  [("Find sin 765°.", ["765° − 2 × 360° = 45°", "sin 45° = 1/√2"], "1/√2"), ("Convert 40°20′ to radians.", ["40°20′ = 121/3 degrees", "× π/180 = 121π/540"], "121π/540")],
  ["Using θ in degrees in l = rθ.", "Forgetting the sign of the quadrant.", "Writing sin(A + B) = sin A + sin B."],
  [("How many degrees is one radian?", "180/π ≈ 57°16′."), ("What is the period of sin x?", "2π; tan x has period π.")],
  [("Radians and arc length", [(conv, 10), (one_arc, 10)]),
   ("Values and signs", [(exact, 8), (sign, 4), (one_big, 8)]),
   ("Six trigonometric functions", [(rec, 6), (other, 8), (val, 6)]),
   ("Sum and difference formulas", [(sexact, 8), (given, 12)]),
   ("Multiple angles, period and range", [(double, 10), (one_period, 10)])], 911103)
