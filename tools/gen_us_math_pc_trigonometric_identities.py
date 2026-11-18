# -*- coding: utf-8 -*-
"""
US Precalculus: Trigonometric Identities (Common Core F-TF.C.8)
  python3 tools/gen_us_math_pc_trigonometric_identities.py
The Pythagorean identity sin²θ + cos²θ = 1 and its forms, reciprocal and quotient identities, even-odd and
cofunction identities, simplifying expressions, and finding values from one given value and the quadrant.
Wrong answers come from real mistakes: forgetting the ± and the quadrant, writing 1 + tan²θ = csc²θ,
cancelling terms instead of factors, and treating sin(−θ) as sin θ.
"""
import math
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, num, MINUS, fr
from a2_common import sf
from pc_common import GRADE, surd

R = random.Random(97401)
TH = "θ"
QUAD = {1: "Quadrant I", 2: "Quadrant II", 3: "Quadrant III", 4: "Quadrant IV"}


def sq(f):
    return "%s²%s" % (f, TH) if False else "%s² %s" % (f, TH)


# ------------------------------------------------------------ set 1: the Pythagorean identity
def one_pyth(r):
    p, q = r.choice([(1, 3), (2, 3), (1, 4), (3, 4), (2, 5), (1, 5), (3, 7), (5, 6), (4, 7), (1, 2), (3, 5), (5, 13), (4, 9)])
    given = r.choice(["sin", "cos"])
    other = "cos" if given == "sin" else "sin"
    qd = r.choice([1, 2, 3, 4])
    sx = 1 if qd in (1, 4) else -1
    sy = 1 if qd in (1, 2) else -1
    gs = sy if given == "sin" else sx
    os_ = sx if given == "sin" else sy
    gv = F(gs * p, q)
    right = surd(os_, q * q - p * p, q)
    q_ = "If %s %s = %s and %s is in %s, find %s %s." % (given, TH, sf(gv), TH, QUAD[qd], other, TH)
    return T(q_, right, [surd(-os_, q * q - p * p, q), surd(os_, q * q - p * p, q * q) if True else "", surd(os_, q - p, q) if q - p > 0 else surd(os_, 1, q)],
             "%s² %s = 1 − (%s)² = %s, so %s %s = ±%s. In %s %s is %s, so %s %s = <b>%s</b>." % (
                 other, TH, sf(F(p, q)), sf(1 - F(p * p, q * q)), other, TH, surd(1, q * q - p * p, q), QUAD[qd], other, "positive" if os_ > 0 else "negative", other, TH, right))


# ------------------------------------------------------------ set 2: basic identities
BASIC = [("1 + tan² θ", "sec² θ", ["csc² θ", "cot² θ", "1"]),
         ("1 + cot² θ", "csc² θ", ["sec² θ", "tan² θ", "1"]),
         ("1 − sin² θ", "cos² θ", ["tan² θ", "−cos² θ", "sec² θ"]),
         ("1 − cos² θ", "sin² θ", ["−sin² θ", "tan² θ", "csc² θ"]),
         ("sec² θ − tan² θ", "1", ["−1", "sec θ − tan θ", "0"]),
         ("csc² θ − cot² θ", "1", ["−1", "0", "tan² θ"]),
         ("sin θ / cos θ", "tan θ", ["cot θ", "sec θ", "1"]),
         ("cos θ / sin θ", "cot θ", ["tan θ", "csc θ", "1"]),
         ("1 / cos θ", "sec θ", ["csc θ", "cot θ", "cos⁻¹ θ"]),
         ("1 / sin θ", "csc θ", ["sec θ", "sin⁻¹ θ", "tan θ"]),
         ("1 / tan θ", "cot θ", ["tan⁻¹ θ", "sec θ", "csc θ"]),
         ("sin(−θ)", "−sin θ", ["sin θ", "−cos θ", "cos θ"]),
         ("cos(−θ)", "cos θ", ["−cos θ", "sin θ", "−sin θ"]),
         ("tan(−θ)", "−tan θ", ["tan θ", "cot θ", "−cot θ"]),
         ("sin(90° − θ)", "cos θ", ["sin θ", "−cos θ", "−sin θ"]),
         ("cos(90° − θ)", "sin θ", ["cos θ", "−sin θ", "−cos θ"]),
         ("tan(90° − θ)", "cot θ", ["tan θ", "−tan θ", "sec θ"]),
         ("sec(90° − θ)", "csc θ", ["sec θ", "cos θ", "sin θ"]),
         ("csc(−θ)", "−csc θ", ["csc θ", "sec θ", "−sec θ"]),
         ("sec(−θ)", "sec θ", ["−sec θ", "csc θ", "cos θ"]),
         ("sin² θ + cos² θ", "1", ["0", "2", "sin θ + cos θ"]),
         ("cot(90° − θ)", "tan θ", ["cot θ", "−cot θ", "csc θ"])]


def one_basic(r):
    e, right, wr = r.choice(BASIC)
    q = "Which expression is equal to %s?" % e
    why = {"1": "It is a form of the Pythagorean identity."}.get(right, "")
    if "−θ" in e:
        why = "Sine, tangent, cosecant and cotangent are odd: f(−θ) = −f(θ). Cosine and secant are even: f(−θ) = f(θ)."
    elif "90°" in e:
        why = "Cofunction identity: a function of (90° − θ) equals its cofunction of θ."
    elif "/" in e:
        why = "Reciprocal and quotient identities."
    elif "²" in e:
        why = "Divide sin² θ + cos² θ = 1 by cos² θ or sin² θ, or rearrange it."
    return T(q, right, wr, "%s <b>%s</b>." % (why, right))


# ------------------------------------------------------------ set 3: simplifying expressions
SIMP = [("sin θ · cot θ", "cos θ", ["sin θ", "tan θ", "1"], "cot θ = cos θ/sin θ, and sin θ cancels."),
        ("cos θ · tan θ", "sin θ", ["cos θ", "cot θ", "1"], "tan θ = sin θ/cos θ, and cos θ cancels."),
        ("tan θ · cot θ", "1", ["tan² θ", "0", "sec θ"], "They are reciprocals."),
        ("sec θ · cos θ", "1", ["sec² θ", "0", "sin θ"], "They are reciprocals."),
        ("(1 − cos² θ) / sin θ", "sin θ", ["cos θ", "1 − cos θ", "csc θ"], "1 − cos² θ = sin² θ, and sin² θ / sin θ = sin θ."),
        ("(1 − sin² θ) / cos θ", "cos θ", ["sin θ", "1 − sin θ", "sec θ"], "1 − sin² θ = cos² θ, and cos² θ / cos θ = cos θ."),
        ("cos² θ (1 + tan² θ)", "1", ["cos² θ", "sec² θ", "sin² θ"], "1 + tan² θ = sec² θ, and cos² θ · sec² θ = 1."),
        ("sin² θ (1 + cot² θ)", "1", ["sin² θ", "csc² θ", "cos² θ"], "1 + cot² θ = csc² θ, and sin² θ · csc² θ = 1."),
        ("sec θ − sin θ tan θ", "cos θ", ["sin θ", "sec θ", "1"], "1/cos θ − sin² θ/cos θ = (1 − sin² θ)/cos θ = cos² θ/cos θ."),
        ("csc θ − cos θ cot θ", "sin θ", ["cos θ", "csc θ", "1"], "1/sin θ − cos² θ/sin θ = sin² θ/sin θ."),
        ("tan θ / sec θ", "sin θ", ["cos θ", "cot θ", "csc θ"], "(sin θ/cos θ) · cos θ = sin θ."),
        ("cot θ / csc θ", "cos θ", ["sin θ", "tan θ", "sec θ"], "(cos θ/sin θ) · sin θ = cos θ."),
        ("csc θ / cot θ", "sec θ", ["csc θ", "cos θ", "tan θ"], "(1/sin θ) · (sin θ/cos θ) = 1/cos θ."),
        ("sec θ / tan θ", "csc θ", ["sec θ", "sin θ", "cot θ"], "(1/cos θ) · (cos θ/sin θ) = 1/sin θ."),
        ("sin⁴ θ − cos⁴ θ", "sin² θ − cos² θ", ["1", "sin θ − cos θ", "0"], "Difference of squares: (sin² θ − cos² θ)(sin² θ + cos² θ), and the second factor is 1."),
        ("(sin θ + cos θ)² − 1", "2 sin θ cos θ", ["0", "1", "sin² θ + cos² θ"], "sin² θ + 2 sin θ cos θ + cos² θ − 1 = 2 sin θ cos θ."),
        ("(1 + sin θ)(1 − sin θ)", "cos² θ", ["1 − sin θ", "sin² θ", "1"], "1 − sin² θ = cos² θ."),
        ("(sec θ − 1)(sec θ + 1)", "tan² θ", ["sec² θ", "1", "cot² θ"], "sec² θ − 1 = tan² θ."),
        ("sin θ csc θ − cos² θ", "sin² θ", ["0", "cos² θ", "1"], "sin θ csc θ = 1, and 1 − cos² θ = sin² θ."),
        ("tan² θ − sec² θ", "−1", ["1", "0", "tan² θ"], "sec² θ = 1 + tan² θ, so the difference is −1."),
        ("cos θ + sin θ tan θ", "sec θ", ["cos θ", "1", "tan θ"], "cos θ + sin² θ/cos θ = (cos² θ + sin² θ)/cos θ = 1/cos θ."),
        ("sin θ + cos θ cot θ", "csc θ", ["sin θ", "1", "cot θ"], "sin θ + cos² θ/sin θ = (sin² θ + cos² θ)/sin θ = 1/sin θ."),
        ("cos(−θ) sec θ", "1", ["−1", "cos² θ", "sec² θ"], "cos(−θ) = cos θ, and cos θ sec θ = 1."),
        ("sin(−θ) csc θ", "−1", ["1", "sin² θ", "0"], "sin(−θ) = −sin θ, and −sin θ csc θ = −1.")]


def one_simp(r):
    e, right, wr, why = r.choice(SIMP)
    return T("Simplify %s." % e, right, wr, why + " <b>%s</b>." % right)


# ------------------------------------------------------------ set 4: values from identities
def one_val(r):
    kind = r.choice(["sec", "csc", "sec", "csc", "both"])
    t = r.choice([2, 3, F(1, 2), F(3, 4), F(2, 3), 4, F(5, 12), 5])
    if kind == "sec":
        q = "If tan %s = %s and %s is in Quadrant I, find sec² %s." % (TH, sf(t), TH, TH)
        ans = 1 + t * t
        return T(q, sf(ans), [sf(t * t), sf(1 - t * t) if 1 - t * t != ans else sf(t * t + 2), sf(1 + t)],
                 "sec² %s = 1 + tan² %s = 1 + %s = <b>%s</b>." % (TH, TH, sf(t * t), sf(ans)))
    if kind == "csc":
        q = "If cot %s = %s, find csc² %s." % (TH, sf(t), TH)
        ans = 1 + t * t
        return T(q, sf(ans), [sf(t * t), sf(abs(1 - t * t)) if abs(1 - t * t) != ans else sf(ans + 1), sf(1 + 1 / (t * t))],
                 "csc² %s = 1 + cot² %s = 1 + %s = <b>%s</b>." % (TH, TH, sf(t * t), sf(ans)))
    s = r.choice([F(1, 3), F(2, 5), F(3, 5), F(1, 4), F(5, 13), F(2, 7)])
    want = r.choice(["cos² θ", "csc² θ", "cot² θ"])
    if want == "cos² θ":
        ans = 1 - s * s
        wr = [sf(s * s), sf(1 - s), sf(1 + s * s)]
    elif want == "csc² θ":
        ans = 1 / (s * s)
        wr = [sf(1 / s), sf(s * s), sf(1 - s * s)]
    else:
        ans = (1 - s * s) / (s * s)
        wr = [sf(1 / (s * s)), sf(1 - s * s), sf(s * s / (1 - s * s))]
    q = "If sin %s = %s, find %s." % (TH, sf(s), want)
    how = {"cos² θ": "cos² θ = 1 − sin² θ = 1 − %s" % sf(s * s), "csc² θ": "csc² θ = 1 / sin² θ = 1 ÷ %s" % sf(s * s),
           "cot² θ": "cot² θ = cos² θ / sin² θ = %s ÷ %s" % (sf(1 - s * s), sf(s * s))}[want]
    return T(q, sf(ans), wr, "%s = <b>%s</b>. Squares do not depend on the quadrant." % (how, sf(ans)))


# ------------------------------------------------------------ set 5: harder problems
def one_hard(r):
    kind = r.choice(["tan", "tan", "param", "param", "unit"])
    if kind == "tan":
        p, q = r.choice([(1, 2), (2, 3), (1, 3), (3, 2), (2, 1), (3, 1), (1, 4), (4, 3), (5, 2)])
        qd = r.choice([1, 2, 3, 4])
        sx = 1 if qd in (1, 4) else -1
        sy = 1 if qd in (1, 2) else -1
        tv = F(sx * sy * p, q)
        hyp = p * p + q * q
        want = r.choice(["sin", "cos", "sec"])
        if want == "sin":
            right = surd(sy * p, hyp, hyp)
            wr = [surd(-sy * p, hyp, hyp), surd(sy * q, hyp, hyp), surd(sy * p, 1, q * q + p)]
        elif want == "cos":
            right = surd(sx * q, hyp, hyp)
            wr = [surd(-sx * q, hyp, hyp), surd(sx * p, hyp, hyp), surd(sx * q, hyp, 1)]
        else:
            right = surd(sx, hyp, q)
            wr = [surd(-sx, hyp, q), surd(sx, hyp, p), surd(sx * q, hyp, hyp)]
        if len({right} | set(wr)) < 4:
            return None
        return T("If tan %s = %s and %s is in %s, find %s %s." % (TH, sf(tv), TH, QUAD[qd], want, TH), right, wr,
                 "Use <i>x</i> = %s, <i>y</i> = %s (signs from %s). <i>r</i> = √(%d + %d) = √%d. Then %s %s = <b>%s</b>." % (
                     sf(sx * q), sf(sy * p), QUAD[qd], q * q, p * p, hyp, want, TH, right))
    if kind == "param":
        a = r.choice([2, 3, 4, 5, 6])
        b = r.choice([2, 3, 4, 5, 6, a, a])
        q = "A point moves along the curve <i>x</i> = %s cos <i>t</i>, <i>y</i> = %s sin <i>t</i>. Which equation describes the curve?" % (a, b)
        if a == b:
            right = "<i>x</i>² + <i>y</i>² = %d" % (a * a)
            wr = ["<i>x</i>² + <i>y</i>² = %d" % a, "<i>x</i> + <i>y</i> = %d" % a, "<i>x</i>² − <i>y</i>² = %d" % (a * a)]
            e = "<i>x</i>² + <i>y</i>² = %d(cos² <i>t</i> + sin² <i>t</i>) = %d. It is a circle of radius %d. <b>%s</b>." % (a * a, a * a, a, right)
        else:
            right = "<i>x</i>²/%d + <i>y</i>²/%d = 1" % (a * a, b * b)
            wr = ["<i>x</i>²/%d + <i>y</i>²/%d = 1" % (a, b), "<i>x</i>² + <i>y</i>² = %d" % (a * b), "<i>x</i>²/%d − <i>y</i>²/%d = 1" % (a * a, b * b)]
            e = "cos <i>t</i> = <i>x</i>/%d and sin <i>t</i> = <i>y</i>/%d, and cos² <i>t</i> + sin² <i>t</i> = 1, so <b>%s</b>." % (a, b, right)
        return T(q, right, wr, e)
    c = r.choice([F(3, 5), F(-4, 5), F(5, 13), F(-12, 13), F(8, 17), F(-15, 17), F(7, 25), F(24, 25)])
    above = r.random() < 0.5
    s = (1 - c * c)
    sv = F(int(round(math.sqrt(s.numerator))), int(round(math.sqrt(s.denominator))))
    if not above:
        sv = -sv
    q = "A point on the unit circle has <i>x</i>-coordinate %s and is %s the <i>x</i>-axis. What is its <i>y</i>-coordinate?" % (sf(c), "above" if above else "below")
    return T(q, sf(sv), [sf(-sv), sf(1 - abs(c)) if 1 - abs(c) != abs(sv) else sf(c), sf(1 - c * c)],
             "<i>x</i>² + <i>y</i>² = 1 (cos² + sin² = 1): <i>y</i>² = 1 − %s = %s, so <i>y</i> = <b>%s</b>." % (sf(c * c), sf(s), sf(sv)))


def build():
    sets = [S("The Pythagorean identity", collect(one_pyth, 20, R)),
            S("Basic identities", collect(one_basic, 20, R)),
            S("Simplifying expressions", collect(one_simp, 20, R)),
            S("Values from identities", collect(one_val, 20, R)),
            S("Harder problems", collect(one_hard, 20, R))]
    body = lesson(
        "<ul><li><b>Pythagorean identities</b>: sin² θ + cos² θ = 1, 1 + tan² θ = sec² θ, 1 + cot² θ = csc² θ.</li>"
        "<li><b>Reciprocal and quotient</b>: csc θ = 1/sin θ, sec θ = 1/cos θ, tan θ = sin θ/cos θ, cot θ = cos θ/sin θ.</li>"
        "<li><b>Even-odd</b>: cos(−θ) = cos θ, but sin(−θ) = −sin θ and tan(−θ) = −tan θ. <b>Cofunction</b>: sin(90° − θ) = cos θ.</li>"
        "<li>To simplify, rewrite everything in sine and cosine, then factor and use sin² θ + cos² θ = 1.</li>"
        "<li>When you take a square root, choose the sign from the quadrant.</li></ul>",
        [("If sin θ = " + fr(1, 3) + " and θ is in Quadrant II, find cos θ.", ["cos² θ = 1 − " + fr(1, 9) + " = " + fr(8, 9), "cos θ = ±" + surd(2, 2, 3) + "; cosine is negative in Quadrant II"], surd(-2, 2, 3)),
         ("Simplify sec θ − sin θ tan θ.", ["= 1/cos θ − sin² θ/cos θ", "= (1 − sin² θ)/cos θ = cos² θ/cos θ"], "cos θ")],
        ["Forgetting the ± when taking a square root, or choosing the wrong sign for the quadrant.",
         "Writing 1 + tan² θ = csc² θ. Tangent goes with secant.",
         "Cancelling terms across a sum, such as (1 − cos² θ)/cos θ = 1 − cos θ.",
         "Treating sin(−θ) as sin θ. Only cosine and secant are even."])
    faq = [("What is the Pythagorean identity?", "sin²θ + cos²θ = 1 for every angle θ. Dividing it by cos²θ or sin²θ gives 1 + tan²θ = sec²θ and 1 + cot²θ = csc²θ."),
           ("How do you simplify a trigonometric expression?", "Rewrite every function in terms of sine and cosine, combine fractions, factor, and use sin²θ + cos²θ = 1."),
           ("How do you know whether the answer is positive or negative?", "Use the quadrant: sine is positive in Quadrants I and II, cosine in I and IV, and tangent in I and III."),
           ("Which trig functions are even and which are odd?", "Cosine and secant are even: f(−θ) = f(θ). Sine, tangent, cosecant and cotangent are odd: f(−θ) = −f(θ).")]
    make("trigonometric-identities", 4, "F-TF.C.8",
         "Trigonometric Identities",
         "Trigonometric Identities Worksheet: Pythagorean, Reciprocal, Even-Odd | 100 Questions",
         "Trig Identities",
         "Prove the Pythagorean identity sin²(θ) + cos²(θ) = 1 and use it to find sin(θ), cos(θ), or tan(θ) given sin(θ), cos(θ), or tan(θ) and the quadrant of the angle.",
         "Free precalculus worksheet on trigonometric identities: the Pythagorean identity, reciprocal, quotient, even-odd and cofunction identities, and simplifying expressions. 100 questions.",
         "sin² θ + cos² θ = 1",
         "Rewrite in sine and cosine, then use the identity. Take the sign from the quadrant.",
         body, faq, sets, R, domain="Trigonometric Functions", grade=GRADE)


if __name__ == "__main__":
    build()
