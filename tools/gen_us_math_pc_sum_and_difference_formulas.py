# -*- coding: utf-8 -*-
"""
US Precalculus: Sum, Difference and Double-Angle Formulas (Common Core F-TF.C.9)
  python3 tools/gen_us_math_pc_sum_and_difference_formulas.py
Exact values such as sin 75° and cos 15°, recognizing an expansion, sin(α + β) from given values,
double-angle formulas, and applications such as the range of a projectile.
Wrong answers come from real mistakes: writing sin(A + B) = sin A + sin B, using the wrong sign in the
cosine formula, mixing up sine and cosine, and doubling sin θ instead of using 2 sin θ cos θ.
"""
import math
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, num, MINUS, fr, People
from a2_common import sf
from pc_common import GRADE, trig, vhtml, pis, rad

R = random.Random(97501)
TH = "θ"
QUAD = {1: "Quadrant I", 2: "Quadrant II", 3: "Quadrant III", 4: "Quadrant IV"}
S15, C15 = ("√6 − √2", 4), ("√6 + √2", 4)
SPLIT = {15: "45° − 30°", 75: "45° + 30°", 105: "60° + 45°", 165: "120° + 45°", 195: "150° + 45°", 255: "210° + 45°", 285: "240° + 45°", 345: "300° + 45°"}


def quad(d):
    return 1 if d < 90 else 2 if d < 180 else 3 if d < 270 else 4


def ref(d):
    return [d, 180 - d, d - 180, 360 - d][quad(d) - 1]


def h(v, sign):
    """v = (top, den) fraction or a plain string like '2 − √3'"""
    if isinstance(v, tuple):
        s = fr(*v)
        return (MINUS + s) if sign < 0 else s
    if sign > 0:
        return v
    return {"2 − √3": "√3 − 2", "2 + √3": MINUS + "2 − √3"}[v]


def val(fn, d):
    rf = ref(d)
    base = {"sin": S15 if rf == 15 else C15, "cos": C15 if rf == 15 else S15, "tan": "2 − √3" if rf == 15 else "2 + √3"}[fn]
    qd = quad(d)
    sign = {"sin": 1 if qd in (1, 2) else -1, "cos": 1 if qd in (1, 4) else -1, "tan": 1 if qd in (1, 3) else -1}[fn]
    return base, sign


# ------------------------------------------------------------ set 1: exact values
def one_exact(r):
    d = r.choice(list(SPLIT))
    fn = r.choice(["sin", "cos", "sin", "cos", "tan"])
    base, sign = val(fn, d)
    right = h(base, sign)
    other_fn = {"sin": "cos", "cos": "sin", "tan": "tan"}[fn]
    if fn == "tan":
        alt = "2 + √3" if base == "2 − √3" else "2 − √3"
        wr = [h(base, -sign), h(alt, sign), fr("3 + √3", 3)]
    else:
        alt = C15 if base == S15 else S15
        wr = [h(base, -sign), h(alt, sign), h(("√2 + 1", 2), sign) if fn == "sin" else h(("√2 + √3", 2), sign)]
    a, op, b = SPLIT[d].split(" ")
    fmla = {"sin": "sin(A %s B) = sin A cos B %s cos A sin B" % (op, op),
            "cos": "cos(A %s B) = cos A cos B %s sin A sin B" % (op, MINUS if op == "+" else "+"),
            "tan": "tan(A %s B) = (tan A %s tan B) / (1 %s tan A tan B)" % (op, op, MINUS if op == "+" else "+")}[fn]
    return T("Find the exact value of %s %d°." % (fn, d), right, wr,
             "Write %d° = %s and use %s. The result simplifies to <b>%s</b>." % (d, SPLIT[d], fmla, right))


# ------------------------------------------------------------ set 2: recognize the formula
def one_recog(r):
    kind = r.choice(["sin+", "sin-", "cos+", "cos-", "tan+"])
    target = r.choice([30, 45, 60, 90, 120, 135, 150, 180, 0])
    if kind.endswith("+"):
        A = r.choice([x for x in range(5, 90, 5) if x < target]) if target > 5 else None
        if A is None:
            return None
        Bv = target - A
    else:
        A = r.choice([x for x in range(target + 5, target + 80, 5)])
        Bv = A - target
    if A == Bv or Bv <= 0:
        return None
    if kind == "sin+":
        e = "sin %d° cos %d° + cos %d° sin %d°" % (A, Bv, A, Bv)
        fn, ang, wrong_ang = "sin", A + Bv, abs(A - Bv)
    elif kind == "sin-":
        e = "sin %d° cos %d° − cos %d° sin %d°" % (A, Bv, A, Bv)
        fn, ang, wrong_ang = "sin", A - Bv, A + Bv
    elif kind == "cos+":
        e = "cos %d° cos %d° − sin %d° sin %d°" % (A, Bv, A, Bv)
        fn, ang, wrong_ang = "cos", A + Bv, abs(A - Bv)
    elif kind == "cos-":
        e = "cos %d° cos %d° + sin %d° sin %d°" % (A, Bv, A, Bv)
        fn, ang, wrong_ang = "cos", A - Bv, A + Bv
    else:
        if A + Bv in (90,) or A >= 90 or Bv >= 90:
            return None
        e = "(tan %d° + tan %d°) / (1 − tan %d° tan %d°)" % (A, Bv, A, Bv)
        fn, ang, wrong_ang = "tan", A + Bv, abs(A - Bv)
    v = trig(fn, ang)
    if v is None:
        return None
    try:
        wv = trig(fn, wrong_ang)
        ov = trig("cos" if fn == "sin" else "sin", ang)
    except AssertionError:
        return None
    right = vhtml(v)
    wr = [vhtml(wv) if wv else "undefined", vhtml(ov) if ov else "1", vhtml((-v[0], v[1])) if v[1] != "0" else "1"]
    return T("Find the exact value of %s." % e, right, wr, "This is the expansion of %s(%d° %s %d°) = %s %d° = <b>%s</b>." % (fn, A, "+" if kind.endswith("+") else MINUS, Bv, fn, ang, right))


# ------------------------------------------------------------ set 3: sin(α + β) from given values
TR = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)]


def one_given(r):
    (a1, b1, c1), (a2, b2, c2) = r.sample(TR, 2) if r.random() < 0.7 else [r.choice(TR)] * 2
    # α in Quadrant I with sin α = b1/c1, β in Quadrant I with cos β = a2/c2
    sa, ca = F(b1, c1), F(a1, c1)
    sb, cb = F(b2, c2), F(a2, c2)
    want = r.choice(["sin(α + β)", "sin(α − β)", "cos(α + β)", "cos(α − β)"])
    vals = {"sin(α + β)": sa * cb + ca * sb, "sin(α − β)": sa * cb - ca * sb, "cos(α + β)": ca * cb - sa * sb, "cos(α − β)": ca * cb + sa * sb}
    ans = vals[want]
    mist = {"sin(α + β)": sa + sb, "sin(α − β)": sa - sb, "cos(α + β)": ca * cb + sa * sb, "cos(α − β)": ca * cb - sa * sb}[want]
    swap = {"sin(α + β)": vals["sin(α − β)"], "sin(α − β)": vals["sin(α + β)"], "cos(α + β)": vals["sin(α + β)"], "cos(α − β)": vals["sin(α − β)"]}[want]
    q = "α and β are in Quadrant I with sin α = %s and cos β = %s. Find %s." % (sf(sa), sf(cb), want)
    wr = [sf(mist), sf(swap), sf(-ans)]
    fm = {"sin(α + β)": "sin α cos β + cos α sin β", "sin(α − β)": "sin α cos β − cos α sin β",
          "cos(α + β)": "cos α cos β − sin α sin β", "cos(α − β)": "cos α cos β + sin α sin β"}[want]
    return T(q, sf(ans), wr, "cos α = %s and sin β = %s (from right triangles). %s = %s = <b>%s</b>." % (sf(ca), sf(sb), want, fm, sf(ans)))


# ------------------------------------------------------------ set 4: double-angle formulas
def one_double(r):
    a, b, c = r.choice(TR)
    if r.random() < 0.5:
        a, b = b, a
    qd = r.choice([1, 2, 3, 4])
    sx = 1 if qd in (1, 4) else -1
    sy = 1 if qd in (1, 2) else -1
    s, co = F(sy * b, c), F(sx * a, c)
    given = r.choice(["sin", "cos"])
    want = r.choice(["sin 2θ", "cos 2θ", "tan 2θ"])
    vals = {"sin 2θ": 2 * s * co, "cos 2θ": co * co - s * s, "tan 2θ": (2 * s * co) / (co * co - s * s)}
    ans = vals[want]
    mist = {"sin 2θ": 2 * s, "cos 2θ": 2 * co, "tan 2θ": 2 * s / co}[want]
    wr = [sf(mist), sf(-ans), sf(vals["cos 2θ"] if want != "cos 2θ" else vals["sin 2θ"])]
    gv = s if given == "sin" else co
    q = "If %s %s = %s and %s is in %s, find %s." % (given, TH, sf(gv), TH, QUAD[qd], want)
    how = {"sin 2θ": "sin 2θ = 2 sin θ cos θ = 2(%s)(%s)" % (sf(s), sf(co)), "cos 2θ": "cos 2θ = cos² θ − sin² θ = %s − %s" % (sf(co * co), sf(s * s)),
           "tan 2θ": "tan 2θ = sin 2θ / cos 2θ = %s ÷ %s" % (sf(vals["sin 2θ"]), "(%s)" % sf(vals["cos 2θ"]) if vals["cos 2θ"] < 0 else sf(vals["cos 2θ"]))}[want]
    return T(q, sf(ans), wr, "First, %s %s = %s (sign from %s). %s = <b>%s</b>." % ("cos" if given == "sin" else "sin", TH, sf(co if given == "sin" else s), QUAD[qd], how, sf(ans)))


# ------------------------------------------------------------ set 5: applications
def one_app(r):
    kind = r.choice(["range", "range", "max", "same", "rewrite", "rewrite"])
    if kind == "range":
        v = r.choice([40, 48, 56, 64, 80])
        ang = r.choice([15, 30, 45, 60, 75, 20, 35])
        rng = v * v * math.sin(math.radians(2 * ang)) / 32
        q = ("A ball is kicked at %d ft/s at an angle of %d° above the ground. Its range is <i>R</i> = <i>v</i>² sin 2θ / 32 feet. "
             "To the nearest foot, how far does it travel?" % (v, ang))
        right = "%d ft" % round(rng)
        wr = ["%d ft" % round(v * v * math.sin(math.radians(ang)) / 32), "%d ft" % round(2 * v * v * math.sin(math.radians(ang)) / 32), "%d ft" % round(v * v / 32)]
        if len(set(wr + [right])) < 4:
            return None
        return T(q, right, wr, "<i>R</i> = %d² × sin %d° ÷ 32 = %s × %.4f ÷ 32 ≈ <b>%s</b>. Use sin 2θ, not 2 sin θ." % (v, 2 * ang, num(v * v), math.sin(math.radians(2 * ang)), right))
    if kind == "max":
        q = "For the range <i>R</i> = <i>v</i>² sin 2θ / 32, which launch angle gives the greatest range?"
        right = "45°, because sin 2θ is largest (1) when 2θ = 90°"
        return T(q, right, ["90°, because sin 90° = 1", "30°, because sin 30° = 1/2", "60°, because it is the steepest useful angle"], "sin 2θ reaches its maximum 1 at 2θ = 90°. <b>%s</b>." % right)
    if kind == "same":
        a = r.choice([15, 20, 25, 30, 35, 40])
        q = "A projectile launched at %d° travels a certain distance. At what other angle, with the same speed, does it travel the same distance?" % a
        right = "%d°" % (90 - a)
        return T(q, right, ["%d°" % (180 - a), "%d°" % (2 * a), "%d°" % (45 + a)], "sin 2θ = sin(180° − 2θ) = sin 2(90° − θ), so %d° and <b>%s</b> give the same range." % (a, right))
    items = [("2 sin x cos x", "sin 2<i>x</i>", ["2 sin <i>x</i>", "cos 2<i>x</i>", "sin² <i>x</i>"]),
             ("cos² x − sin² x", "cos 2<i>x</i>", ["1", "sin 2<i>x</i>", "−cos 2<i>x</i>"]),
             ("1 − 2 sin² x", "cos 2<i>x</i>", ["cos² <i>x</i>", "sin 2<i>x</i>", "−cos 2<i>x</i>"]),
             ("2 cos² x − 1", "cos 2<i>x</i>", ["cos <i>x</i>", "sin² <i>x</i>", "2 cos 2<i>x</i>"]),
             ("sin 3x cos x + cos 3x sin x", "sin 4<i>x</i>", ["sin 2<i>x</i>", "cos 4<i>x</i>", "sin 3<i>x</i>"]),
             ("cos 5x cos 2x + sin 5x sin 2x", "cos 3<i>x</i>", ["cos 7<i>x</i>", "sin 3<i>x</i>", "cos 10<i>x</i>"]),
             ("cos 4x cos x − sin 4x sin x", "cos 5<i>x</i>", ["cos 3<i>x</i>", "sin 5<i>x</i>", "cos 4<i>x</i>"]),
             ("4 sin x cos x", "2 sin 2<i>x</i>", ["sin 4<i>x</i>", "4 sin 2<i>x</i>", "sin 2<i>x</i>"]),
             ("sin(x + π) ", "−sin <i>x</i>", ["sin <i>x</i>", "cos <i>x</i>", "−cos <i>x</i>"]),
             ("cos(x + π/2)", "−sin <i>x</i>", ["sin <i>x</i>", "cos <i>x</i>", "−cos <i>x</i>"]),
             ("sin(x − π/2)", "−cos <i>x</i>", ["cos <i>x</i>", "sin <i>x</i>", "−sin <i>x</i>"]),
             ("(sin x + cos x)²", "1 + sin 2<i>x</i>", ["1", "1 + cos 2<i>x</i>", "sin 2<i>x</i>"])]
    e, right, wr = r.choice(items)
    e = e.strip().replace("x", "<i>x</i>")
    return T("Which expression is equal to %s?" % e, right, wr, "Use the sum, difference or double-angle formulas. <b>%s</b>." % right)


def build():
    sets = [S("Exact values with sum and difference formulas", collect(one_exact, 20, R)),
            S("Recognizing the formulas", collect(one_recog, 20, R)),
            S("Using given values", collect(one_given, 20, R)),
            S("Double-angle formulas", collect(one_double, 20, R)),
            S("Applications and rewriting", collect(one_app, 20, R))]
    body = lesson(
        "<ul><li>sin(A ± B) = sin A cos B ± cos A sin B</li>"
        "<li>cos(A ± B) = cos A cos B ∓ sin A sin B (the sign flips)</li>"
        "<li>tan(A ± B) = (tan A ± tan B) / (1 ∓ tan A tan B)</li>"
        "<li>Double angle: sin 2θ = 2 sin θ cos θ, cos 2θ = cos² θ − sin² θ = 2 cos² θ − 1 = 1 − 2 sin² θ.</li>"
        "<li>To find an exact value like sin 75°, write the angle as a sum or difference of special angles: 75° = 45° + 30°.</li></ul>",
        [("Find sin 75°.", ["sin(45° + 30°) = sin 45° cos 30° + cos 45° sin 30°", "= " + fr("√2", 2) + " · " + fr("√3", 2) + " + " + fr("√2", 2) + " · " + fr(1, 2)], fr("√6 + √2", 4)),
         ("If sin θ = " + fr(3, 5) + " and θ is in Quadrant II, find sin 2θ.", ["cos θ = " + MINUS + fr(4, 5), "sin 2θ = 2(" + fr(3, 5) + ")(" + MINUS + fr(4, 5) + ")"], MINUS + fr(24, 25))],
        ["Writing sin(A + B) = sin A + sin B. It is not true in general.",
         "Keeping the same sign in the cosine formula. cos(A + B) has a minus sign.",
         "Writing sin 2θ = 2 sin θ. Use 2 sin θ cos θ.",
         "Forgetting to find cos θ with the correct sign before using a formula."])
    faq = [("What is the sum formula for sine?", "sin(A + B) = sin A cos B + cos A sin B, and sin(A − B) = sin A cos B − cos A sin B."),
           ("Why does the sign change in the cosine formula?", "cos(A + B) = cos A cos B − sin A sin B. The sign in the middle is the opposite of the sign between the angles."),
           ("How do you find sin 15° exactly?", "Write 15° = 45° − 30° and use sin(A − B). The result is (√6 − √2)/4."),
           ("What are the double-angle formulas?", "sin 2θ = 2 sin θ cos θ and cos 2θ = cos²θ − sin²θ, which also equals 2cos²θ − 1 or 1 − 2sin²θ.")]
    make("sum-and-difference-formulas", 5, "F-TF.C.9",
         "Sum, Difference and Double-Angle Formulas",
         "Sum and Difference Formulas Worksheet with Double-Angle Formulas | 100 Questions",
         "Sum and Difference Formulas",
         "Prove the addition and subtraction formulas for sine, cosine, and tangent and use them to solve problems.",
         "Free precalculus worksheet on the sum, difference and double-angle formulas: exact values like sin 75°, recognizing expansions, given values and projectile range. 100 questions.",
         "sin(A + B) = sin A cos B + cos A sin B",
         "cos(A + B) = cos A cos B − sin A sin B. sin 2θ = 2 sin θ cos θ.",
         body, faq, sets, R, domain="Trigonometric Functions", grade=GRADE)


if __name__ == "__main__":
    build()
