# -*- coding: utf-8 -*-
"""
Hand-made question makers for UK A level Mathematics (uk_alevel.unit): algebra (quadratic inequalities, linear and
quadratic simultaneous equations, modulus, partial fractions, parametric equations), calculus (differentiating and
integrating powers of x, tangents and normals, stationary points), numerical methods, statistics (sampling, binomial
distribution, hypothesis tests) and mechanics (suvat, velocity–time graphs, F = ma, connected particles, resolving
forces, friction, moments, projectiles). g = 9.8 m/s². Every maker takes a random.Random and returns an item or None.
Wrong answers come from real mistakes: sign errors, forgetting to divide by the new power, using sin for cos when
resolving, forgetting the weight of a particle, taking the wrong tail in a hypothesis test.
"""
import math
from fractions import Fraction as F
from uk_ks3 import T, QN, expr, num, MINUS, GIRLS, BOYS

X = "<i>x</i>"
G = 9.8


def n(v):
    """number: integer, fraction or decimal; negative with the real minus sign"""
    v = F(v).limit_denominator(1000) if not isinstance(v, F) else v
    if v.denominator == 1:
        return num(v)
    s = "%s%d/%d" % (MINUS if v < 0 else "", abs(v.numerator), v.denominator)
    return s


def d(v, dp=1):
    s = ("%." + str(dp) + "f") % v
    s = s.rstrip("0").rstrip(".") if "." in s else s
    return s.replace("-", MINUS)


def poly(cs, var=X):
    """{power: coeff} -> 3x² − 2x + 5"""
    sup = {2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶"}
    terms = []
    for p in sorted(cs, reverse=True):
        c = cs[p]
        if c == 0:
            continue
        v = var + (sup.get(p, "<sup>%d</sup>" % p) if p > 1 else "") if p >= 1 else ""
        terms.append((c, v))
    return expr(terms)


def opts(right, wrongs):
    w = [x for x in dict.fromkeys(wrongs) if x != right]
    return w[:3] if len(w) >= 3 else None


def item(q, right, wrongs, e):
    w = opts(right, wrongs)
    if not w:
        return None
    return T(q, right, w, e)


# ----------------------------------------------------------------- algebra
def quad_ineq(r):
    a, b = sorted(r.sample(range(-7, 9), 2))
    sign = r.choice(["<", ">", "≤", "≥"])
    q = "Solve (%s − %s)(%s − %s) %s 0." % (X, n(a), X, n(b), {"<": "&lt;", ">": "&gt;"}.get(sign, sign))
    q = q.replace("− " + MINUS, "+ ")
    lt = sign in "<≤"
    s1, s2 = ("&lt;", "&gt;") if sign in "<>" else ("≤", "≥")
    inside = "%s %s %s %s %s" % (n(a), s1, X, s1, n(b))
    outside = "%s %s %s or %s %s %s" % (X, s1, n(a), X, s2, n(b))
    right, other = (inside, outside) if lt else (outside, inside)
    wrong = ["%s %s %s %s %s" % (n(-b), s1, X, s1, n(-a)), "%s %s %s or %s %s %s" % (X, s1, n(-b), X, s2, n(-a)), other]
    return item(q, right, wrong + ["%s %s %s" % (X, s2 if lt else s1, n(b))], "Critical values %s and %s. The graph is a U shape, so it is %s zero %s them." % (n(a), n(b), "below" if lt else "above", "between" if lt else "outside"))


def sim_lq(r):
    m, c = r.choice([1, 2, -1, 3]), r.randint(-3, 4)
    x1, x2 = r.sample(range(-4, 5), 2)
    # y = x² + px + q meets y = mx + c at x1, x2: x² + (p − m)x + (q − c) = 0
    p = m - (-(x1 + x2))
    qq = c + x1 * x2
    p = m - (x1 + x2) * -1
    p = m + (-(x1 + x2))
    pts = sorted([(x1, m * x1 + c), (x2, m * x2 + c)])
    curve = poly({2: 1, 1: p, 0: qq}).replace(X, X)
    line = poly({1: m, 0: c})
    q = "Solve the simultaneous equations <i>y</i> = %s and <i>y</i> = %s. Give the <i>x</i>-values." % (curve, line)
    def pair(a_, b_):
        a_, b_ = sorted([a_, b_])
        return None if a_ == b_ else "%s = %s or %s = %s" % (X, n(a_), X, n(b_))
    right = pair(pts[0][0], pts[1][0])
    wr = [pair(-pts[0][0], -pts[1][0]), pair(pts[0][1], pts[1][1]), pair(pts[0][0] + 1, pts[1][0] - 1), pair(pts[0][0] - 1, pts[1][0] + 1)]
    wr = [w for w in wr if w and w != right]
    return item(q, right, wr, "Set them equal: %s = 0, so (%s − %s)(%s − %s) = 0." % (poly({2: 1, 1: p - m, 0: qq - c}), X, n(x1), X, n(x2)))
    wr = ["%s = %s or %s = %s" % (X, n(-pts[0][0]), X, n(-pts[1][0])), "%s = %s or %s = %s" % (X, n(pts[0][1]), X, n(pts[1][1])),
          "%s = %s or %s = %s" % (X, n(pts[0][0] + 1), X, n(pts[1][0] - 1))]
    return item(q, right, wr, "Set them equal: %s = 0, so (%s − %s)(%s − %s) = 0." % (poly({2: 1, 1: p - m, 0: qq - c}), X, n(x1), X, n(x2)))


def modulus(r):
    a, b, c = r.choice([1, 2, 3]), r.randint(-6, 6), r.randint(1, 9)
    k = r.choice(["eq", "val"])
    if k == "val":
        v = r.randint(-6, 6)
        val = abs(a * v + b)
        return item("f(%s) = |%s|. Find f(%s)." % (X, poly({1: a, 0: b}), n(v)), n(val), [n(a * v + b), n(-val), n(abs(a * v) + abs(b)) if abs(a * v) + abs(b) != val else n(val + 2)],
                    "%s = %s, and the modulus makes it positive: <b>%s</b>." % (poly({1: a, 0: b}).replace(X, "(" + n(v) + ")"), n(a * v + b), n(val)))
    s1, s2 = F(c - b, a), F(-c - b, a)
    right = "%s = %s or %s = %s" % (X, n(min(s1, s2)), X, n(max(s1, s2)))
    return item("Solve |%s| = %s." % (poly({1: a, 0: b}), n(c)), right,
                ["%s = %s only" % (X, n(s1)), "%s = %s or %s = %s" % (X, n(-max(s1, s2)), X, n(-min(s1, s2))), "%s = %s or %s = %s" % (X, n(F(c + b, a)), X, n(F(-c + b, a)))],
                "%s = %s or %s = %s." % (poly({1: a, 0: b}), n(c), poly({1: a, 0: b}), n(-c)))


def pfrac(r):
    a, b = r.sample([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5], 2)
    A, B = r.choice([1, 2, 3, -1, -2]), r.choice([1, 2, 3, 4, -1, -3])
    # A/(x+a) + B/(x+b) = ((A+B)x + Ab + Ba)/((x+a)(x+b))
    num_ = poly({1: A + B, 0: A * b + B * a})
    if A + B == 0:
        return None
    den = "(%s)(%s)" % (poly({1: 1, 0: a}), poly({1: 1, 0: b}))
    f = lambda A_, B_: "%s/(%s) + %s/(%s)" % (n(A_), poly({1: 1, 0: a}), n(B_), poly({1: 1, 0: b}))
    right = f(A, B).replace("+ " + MINUS, "− ")
    wr = [f(B, A), f(-A, -B), f(A + 1, B - 1) if B != 1 else f(A - 1, B + 1)]
    wr = [w.replace("+ " + MINUS, "− ") for w in wr if not w.startswith("0/") and "+ 0/" not in w]
    return item("Express (%s)/(%s) in partial fractions." % (num_, den), right, wr,
                "Write A/(%s) + B/(%s). Put %s = %s and %s = %s to find A = %s and B = %s." % (poly({1: 1, 0: a}), poly({1: 1, 0: b}), X, n(-a), X, n(-b), n(A), n(B)))


def coef(v):
    v = F(v)
    return "" if v == 1 else (MINUS if v == -1 else n(v))


def param(r):
    a, b, c = r.choice([1, 2, 3]), r.randint(-4, 4), r.choice([1, 2, 3, -1])
    k = r.choice(["cart", "point"])
    t = "<i>t</i>"
    xs = poly({1: a, 0: b}, t)
    ys = poly({2: c}, t)
    if k == "point":
        tv = r.randint(-3, 3)
        return item("A curve has parametric equations %s = %s, <i>y</i> = %s. Find the point where %s = %s." % (X, xs, ys, t, n(tv)), "(%s, %s)" % (n(a * tv + b), n(c * tv * tv)),
                    ["(%s, %s)" % (n(c * tv * tv), n(a * tv + b)), "(%s, %s)" % (n(a * tv - b), n(c * tv * tv)), "(%s, %s)" % (n(a * tv + b), n(2 * c * tv))],
                    "Substitute %s = %s into both equations." % (t, n(tv)))
    # t = (x − b)/a, y = c((x − b)/a)²
    inner = "(%s)" % poly({1: 1, 0: -b}) if b else X
    right = "<i>y</i> = %s%s²" % (coef(F(c, a * a)), inner)
    wr = ["<i>y</i> = %s(%s)²" % (coef(F(c, a)), poly({1: 1, 0: -b})), "<i>y</i> = %s(%s)²" % (coef(F(c, a * a)), poly({1: 1, 0: b})),
          "<i>y</i> = %s%s²" % (coef(c), X)]
    return item("Find a Cartesian equation for %s = %s, <i>y</i> = %s." % (X, xs, ys), right, wr, "Make %s the subject: %s = %s, then substitute into <i>y</i>." % (t, t, "(%s)/%s" % (poly({1: 1, 0: -b}), a) if a != 1 else poly({1: 1, 0: -b})))


# ----------------------------------------------------------------- calculus
SUP = {2: "²", 3: "³", 4: "⁴", 5: "⁵"}


def diff_poly(r):
    cs = {p: r.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]) for p in r.sample([0, 1, 2, 3, 4], r.choice([2, 3]))}
    if max(cs) < 2:
        return None
    dcs = {p - 1: c * p for p, c in cs.items() if p > 0}
    right = poly(dcs)
    wr = [poly({p: c * p for p, c in cs.items() if p > 0}), poly({p - 1: c for p, c in cs.items() if p > 0}), poly({p - 1: c * p for p, c in cs.items()} if 0 in cs else {**dcs, 0: 1})]
    return item("Differentiate <i>y</i> = %s." % poly(cs), "d<i>y</i>/d%s = %s" % (X, right), ["d<i>y</i>/d%s = %s" % (X, w) for w in wr],
                "Multiply by the power, then reduce the power by 1. A constant differentiates to 0.")


def grad_at(r):
    a, b, c = r.choice([1, 2, 3, -1]), r.randint(-6, 6), r.randint(-5, 5)
    v = r.randint(-3, 4)
    g = 2 * a * v + b
    return item("Find the gradient of <i>y</i> = %s at the point where %s = %s." % (poly({2: a, 1: b, 0: c}), X, n(v)), n(g),
                [n(a * v * v + b * v + c), n(a * v + b), n(2 * a * v - b)], "d<i>y</i>/d%s = %s. Substitute %s = %s: <b>%s</b>." % (X, poly({1: 2 * a, 0: b}), X, n(v), n(g)))


def tangent(r):
    a, b, c = r.choice([1, 2, -1]), r.randint(-4, 4), r.randint(-4, 6)
    v = r.randint(-2, 3)
    y0, m = a * v * v + b * v + c, 2 * a * v + b
    k = r.choice(["tan", "tan", "norm"])
    if k == "norm" and m == 0:
        return None
    if k == "tan":
        cc = y0 - m * v
        right = "<i>y</i> = %s" % poly({1: m, 0: cc})
        wr = ["<i>y</i> = %s" % poly({1: m, 0: y0}), "<i>y</i> = %s" % poly({1: y0, 0: m}), "<i>y</i> = %s" % poly({1: -m, 0: y0 + m * v})]
        return item("Find the equation of the tangent to <i>y</i> = %s at the point where %s = %s." % (poly({2: a, 1: b, 0: c}), X, n(v)), right, wr,
                    "Point (%s, %s), gradient %s. <i>y</i> − %s = %s(%s − %s)." % (n(v), n(y0), n(m), n(y0), n(m), X, n(v)))
    mn = F(-1, m)
    return item("Find the gradient of the normal to <i>y</i> = %s at the point where %s = %s." % (poly({2: a, 1: b, 0: c}), X, n(v)), n(mn),
                [n(m), n(-m), n(F(1, m))], "Tangent gradient %s. The normal is perpendicular: −1 ÷ %s = <b>%s</b>." % (n(m), n(m), n(mn)))


def stationary(r):
    a, b = r.choice([1, -1, 2]), r.randint(-6, 6)
    c = r.randint(-5, 5)
    xv = F(-b, 2 * a)
    if xv.denominator != 1:
        return None
    yv = a * xv * xv + b * xv + c
    k = r.choice(["pt", "nat"])
    if k == "pt":
        return item("Find the stationary point of <i>y</i> = %s." % poly({2: a, 1: b, 0: c}), "(%s, %s)" % (n(xv), n(yv)),
                    ["(%s, %s)" % (n(-xv), n(yv)), "(%s, %s)" % (n(xv), n(c)), "(%s, %s)" % (n(-xv), n(a * xv * xv - b * xv + c))],
                    "d<i>y</i>/d%s = %s = 0, so %s = %s." % (X, poly({1: 2 * a, 0: b}), X, n(xv)))
    return item("<i>y</i> = %s has a stationary point at %s = %s. Is it a maximum or a minimum?" % (poly({2: a, 1: b, 0: c}), X, n(xv)), "a minimum" if a > 0 else "a maximum",
                ["a maximum" if a > 0 else "a minimum", "a point of inflection", "you cannot tell"], "d²<i>y</i>/d%s² = %s, which is %s." % (X, n(2 * a), "positive, so a minimum" if a > 0 else "negative, so a maximum"))


def integ_poly(r):
    cs = {p: (p + 1) * r.choice([1, 2, 3, -1, -2]) for p in r.sample([0, 1, 2, 3], r.choice([2, 3]))}
    ics = {p + 1: F(c, p + 1) for p, c in cs.items()}
    def ps(d_):
        return expr([(c, X + (SUP.get(p, "<sup>%d</sup>" % p) if p > 1 else "")) for p, c in sorted(d_.items(), reverse=True)])
    right = ps(ics) + " + <i>c</i>"
    wr = [ps({p + 1: c for p, c in cs.items()}) + " + <i>c</i>", ps({p - 1: c * p for p, c in cs.items() if p > 0}) + " + <i>c</i>", ps(ics)]
    return item("Find ∫ (%s) d%s." % (poly(cs), X), right, wr, "Add 1 to the power and divide by the new power. Remember + <i>c</i>.")


def definite(r):
    a, b = r.choice([1, 2, 3, -1]), r.randint(-4, 6)
    lo, hi = sorted(r.sample(range(0, 5), 2))
    Fx = lambda x: F(a, 3) * x ** 3 + F(b, 2) * x * x
    v = Fx(hi) - Fx(lo)
    return item("Evaluate ∫<sub>%d</sub><sup>%d</sup> (%s) d%s." % (lo, hi, poly({2: a, 1: b}), X), n(v), [n(Fx(lo) - Fx(hi)), n(Fx(hi)), n((a * hi * hi + b * hi) - (a * lo * lo + b * lo))],
                "Integrate: %s, then work out the top limit minus the bottom limit." % expr([(F(a, 3), X + "³"), (F(b, 2), X + "²")]))


def newton(r):
    a, b = r.choice([2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20]), r.choice([1, 2, 3])
    x0 = r.choice([1, 2, 3, 4])
    # f(x) = x² − a ; x1 = x0 − f/f'
    f0, d0 = x0 * x0 - a, 2 * x0
    x1 = x0 - F(f0, d0)
    k = r.choice(["nr", "sign"])
    if k == "nr":
        return item("Use one step of the Newton–Raphson method on f(%s) = %s² − %d with %s<sub>0</sub> = %d. What is %s<sub>1</sub>?" % (X, X, a, X, x0, X), d(float(x1), 4),
                    [d(float(x0 + F(f0, d0)), 4), d(float(x0 - F(d0, f0)) if f0 else 0, 4), d(float(F(f0, d0)), 4)],
                    "%s<sub>1</sub> = %s<sub>0</sub> − f(%s<sub>0</sub>) ÷ f′(%s<sub>0</sub>) = %d − (%d) ÷ %d." % (X, X, X, X, x0, f0, d0))
    lo = int(math.floor(math.sqrt(a)))
    if lo * lo == a:
        return None
    return item("f(%s) = %s² − %d. f(%d) and f(%d) have different signs. What does this show?" % (X, X, a, lo, lo + 1), "There is a root between %d and %d." % (lo, lo + 1),
                ["There is no root between %d and %d." % (lo, lo + 1), "The root is exactly %d." % lo, "There is a root between 0 and %d only." % lo],
                "f is continuous, so a change of sign means a root in the interval.")


# ----------------------------------------------------------------- statistics
def comb(nn, k):
    return math.comb(nn, k)


def binom(r):
    nn = r.choice([5, 6, 8, 10, 12])
    p = r.choice([0.1, 0.2, 0.25, 0.3, 0.4, 0.5])
    k = r.choice(["eq", "eq", "mean", "le"])
    if k == "mean":
        return item("X ~ B(%d, %s). What is E(X)?" % (nn, d(p, 2)), d(nn * p, 2), [d(nn * p * (1 - p), 3), d(p, 2), d(nn / p, 2) if p else "0"], "E(X) = <i>np</i> = %d × %s." % (nn, d(p, 2)))
    x = r.randint(0, min(4, nn))
    pe = comb(nn, x) * p ** x * (1 - p) ** (nn - x)
    if k == "eq":
        return item("X ~ B(%d, %s). Find P(X = %d), to 4 decimal places." % (nn, d(p, 2), x), "%.4f" % pe,
                    ["%.4f" % (p ** x * (1 - p) ** (nn - x)), "%.4f" % (comb(nn, x) * p ** x), "%.4f" % (comb(nn, x) * p ** (nn - x) * (1 - p) ** x)],
                    "P(X = %d) = %dC%d × %s<sup>%d</sup> × %s<sup>%d</sup>." % (x, nn, x, d(p, 2), x, d(1 - p, 2), nn - x))
    if x == 0:
        return None
    pl = sum(comb(nn, i) * p ** i * (1 - p) ** (nn - i) for i in range(x + 1))
    return item("X ~ B(%d, %s). Find P(X ≤ %d), to 4 decimal places." % (nn, d(p, 2), x), "%.4f" % pl,
                ["%.4f" % pe, "%.4f" % (1 - pl), "%.4f" % (pl - pe)], "Add P(X = 0) up to P(X = %d)." % x)


def hyp(r):
    nn = r.choice([10, 12, 15, 20])
    p = r.choice([0.2, 0.25, 0.3, 0.4, 0.5])
    up = r.random() < 0.5
    obs = int(nn * p) + (r.choice([3, 4, 5, 6]) if up else -r.choice([2, 3, 4]))
    if not 0 <= obs <= nn:
        return None
    pv = sum(comb(nn, i) * p ** i * (1 - p) ** (nn - i) for i in (range(obs, nn + 1) if up else range(0, obs + 1)))
    sig = r.choice([0.05, 0.1])
    rej = pv < sig
    k = r.choice(["h1", "pv", "dec"])
    who = r.choice(GIRLS + BOYS)
    ctx = "%s thinks a spinner lands on red %s often than the claimed probability %s. In %d spins it lands on red %d times." % (who, "more" if up else "less", d(p, 2), nn, obs)
    if k == "h1":
        return item(ctx + " What is H<sub>1</sub>?", "<i>p</i> %s %s" % ("&gt;" if up else "&lt;", d(p, 2)), ["<i>p</i> %s %s" % ("&lt;" if up else "&gt;", d(p, 2)), "<i>p</i> = %s" % d(p, 2), "<i>p</i> ≠ %s" % d(p, 2)],
                    "H<sub>0</sub>: <i>p</i> = %s. A one-tailed test in the direction %s thinks." % (d(p, 2), who))
    if k == "pv":
        return item(ctx + " Find P(X %s %d) under H<sub>0</sub>, to 4 decimal places." % ("≥" if up else "≤", obs), "%.4f" % pv,
                    ["%.4f" % (1 - pv), "%.4f" % (comb(nn, obs) * p ** obs * (1 - p) ** (nn - obs)), "%.4f" % min(1, pv * 2)], "X ~ B(%d, %s). Add the probabilities in the tail." % (nn, d(p, 2)))
    return item(ctx + " P(X %s %d) = %.4f. Test at the %d%% significance level." % ("≥" if up else "≤", obs, pv, int(sig * 100)),
                "Reject H<sub>0</sub>: there is evidence for %s's claim." % who if rej else "Do not reject H<sub>0</sub>: there is not enough evidence for %s's claim." % who,
                ["Do not reject H<sub>0</sub>: there is not enough evidence for %s's claim." % who if rej else "Reject H<sub>0</sub>: there is evidence for %s's claim." % who,
                 "Accept H<sub>1</sub>: %s's claim is proved." % who, "Reject H<sub>1</sub>: the probability is exactly %s." % d(p, 2)],
                "%.4f %s %s, so %s." % (pv, "&lt;" if rej else "≥", d(sig, 2), "reject H<sub>0</sub>" if rej else "do not reject H<sub>0</sub>"))


SAMP = [("Every 10th name on a list is chosen after a random start.", "systematic sampling"), ("Each person is given a number and a random number generator picks 30 of them.", "simple random sampling"),
        ("The sample has the same proportion of each year group as the school.", "stratified sampling"), ("An interviewer stops people in the street until 20 men and 20 women have answered.", "quota sampling"),
        ("A researcher asks the first 50 people who walk past.", "opportunity sampling"), ("Names are drawn from a hat.", "simple random sampling")]


def sampling(r):
    s, a = r.choice(SAMP)
    return item("Which sampling method is this? %s" % s, a, ["systematic sampling", "simple random sampling", "stratified sampling", "quota sampling", "opportunity sampling"],
                "Random methods: simple random, systematic, stratified. Non-random: quota and opportunity.")


def strat(r):
    groups = r.sample([("Year 12", 120, 180), ("Year 13", 100, 160), ("staff", 30, 60)], 2)
    a, b = r.randint(groups[0][1] // 10, groups[0][2] // 10) * 10, r.randint(groups[1][1] // 10, groups[1][2] // 10) * 10
    s = r.choice([20, 25, 30, 40, 50])
    exact = F(a * s, a + b)
    if exact.denominator != 1:
        return None
    return item("A stratified sample of %d is taken from %d %s and %d %s. How many %s should be in the sample?" % (s, a, groups[0][0], b, groups[1][0], groups[0][0]), n(exact),
                [n(s // 2), n(F(b * s, a + b)), n(F(a, 10))], "%d ÷ %d × %d = <b>%s</b>." % (a, a + b, s, n(exact)))


# ----------------------------------------------------------------- mechanics
def suvat(r):
    u = r.choice([0, 2, 3, 4, 5, 6, 8, 10])
    a = r.choice([0.5, 1, 1.5, 2, 2.5, 3, 4])
    t = r.choice([2, 3, 4, 5, 6, 8, 10])
    v = u + a * t
    s = u * t + 0.5 * a * t * t
    k = r.choice(["v", "s", "a", "s2"])
    obj = r.choice(["A car", "A cyclist", "A particle", "A train", "A sprinter"])
    if k == "v":
        return item("%s starts with speed %s m/s and accelerates at %s m/s² for %d s. Find its final speed." % (obj, d(u), d(a), t), "%s m/s" % d(v),
                    ["%s m/s" % d(a * t), "%s m/s" % d(u + a), "%s m/s" % d(s)], "<i>v</i> = <i>u</i> + <i>at</i> = %s + %s × %d." % (d(u), d(a), t))
    if k == "s":
        return item("%s starts with speed %s m/s and accelerates at %s m/s² for %d s. How far does it travel?" % (obj, d(u), d(a), t), "%s m" % d(s),
                    ["%s m" % d(u * t + a * t * t), "%s m" % d(v * t), "%s m" % d(0.5 * a * t * t)], "<i>s</i> = <i>ut</i> + ½<i>at</i>² = %s × %d + ½ × %s × %d²." % (d(u), t, d(a), t))
    if k == "a":
        return item("%s speeds up from %s m/s to %s m/s in %d s. Find its acceleration." % (obj, d(u), d(v), t), "%s m/s²" % d(a, 2),
                    ["%s m/s²" % d(v / t, 2), "%s m/s²" % d((v + u) / t, 2), "%s m/s²" % d(v - u)], "<i>a</i> = (<i>v</i> − <i>u</i>) ÷ <i>t</i>.")
    v2 = u * u + 2 * a * s
    return item("%s starts at %s m/s and accelerates at %s m/s² over %s m. Find its final speed." % (obj, d(u), d(a), d(s)), "%s m/s" % d(math.sqrt(v2), 2),
                ["%s m/s" % d(v2), "%s m/s" % d(math.sqrt(2 * a * s), 2) if u else "%s m/s" % d(a * s), "%s m/s" % d(u + 2 * a * s)], "<i>v</i>² = <i>u</i>² + 2<i>as</i>.")


def fall(r):
    h = r.choice([5, 10, 20, 40, 45, 80, 2.5])
    k = r.choice(["v", "t"])
    v = math.sqrt(2 * G * h)
    if k == "v":
        return item("A stone is dropped from rest from a height of %s m. Find its speed when it hits the ground (g = 9.8 m/s²)." % d(h), "%s m/s" % d(v, 1),
                    ["%s m/s" % d(2 * G * h, 1), "%s m/s" % d(G * h, 1), "%s m/s" % d(math.sqrt(G * h), 1)], "<i>v</i>² = 0 + 2 × 9.8 × %s." % d(h))
    t = math.sqrt(2 * h / G)
    return item("A ball is dropped from rest from a height of %s m. How long does it take to reach the ground (g = 9.8 m/s²)? Give your answer to 2 decimal places." % d(h), "%s s" % d(t, 2),
                ["%s s" % d(h / G, 2), "%s s" % d(math.sqrt(h / G), 2), "%s s" % d(2 * h / G, 2)], "<i>s</i> = ½<i>gt</i>², so <i>t</i> = √(2<i>s</i> ÷ <i>g</i>).")


def vt_graph(r):
    v = r.choice([4, 5, 6, 8, 10, 12])
    t1, t2, t3 = r.choice([2, 3, 4, 5]), r.choice([4, 5, 6, 8, 10]), r.choice([2, 3, 4])
    k = r.choice(["dist", "acc", "dec"])
    desc = "A cyclist accelerates uniformly from rest to %d m/s in %d s, travels at %d m/s for %d s, then decelerates uniformly to rest in %d s." % (v, t1, v, t2, t3)
    if k == "dist":
        s = F(v * t1, 2) + v * t2 + F(v * t3, 2)
        return item(desc + " Use the area under the velocity–time graph to find the total distance.", "%s m" % n(s),
                    ["%s m" % n(v * (t1 + t2 + t3)), "%s m" % n(v * t2), "%s m" % n(s + F(v * t2, 2))], "Area = two triangles and a rectangle.")
    if k == "acc":
        return item(desc + " Find the acceleration in the first part.", "%s m/s²" % d(v / t1, 2), ["%s m/s²" % d(v * t1), "%s m/s²" % d(t1 / v, 2), "%s m/s²" % d(v / (t1 + t2 + t3), 2)],
                    "Gradient = %d ÷ %d." % (v, t1))
    return item(desc + " Find the deceleration in the last part.", "%s m/s²" % d(v / t3, 2), ["%s m/s²" % d(v * t3), "%s m/s²" % d(t3 / v, 2), "%s m/s²" % d(v / t1, 2) if t1 != t3 else "%s m/s²" % d(v / (t1 + t2 + t3), 2)],
                "Gradient = %d ÷ %d." % (v, t3))


def fma(r):
    m = r.choice([2, 4, 5, 8, 10, 20, 50, 1200, 1500])
    a = r.choice([0.5, 1, 1.5, 2, 2.5, 3, 4])
    res = r.choice([0, 0, 5, 10, 20, 100]) if m < 100 else r.choice([200, 400, 600])
    k = r.choice(["drive", "acc"])
    Fd = m * a + res
    if k == "drive":
        return item("A body of mass %s kg accelerates at %s m/s². The resistance to motion is %s N. Find the driving force." % (num(m), d(a), num(res)), "%s N" % d(Fd),
                    ["%s N" % d(m * a), "%s N" % d(m * a - res), "%s N" % d(m * G * a)], "<i>F</i> − %s = %s × %s." % (num(res), num(m), d(a)))
    return item("A driving force of %s N acts on a body of mass %s kg. The resistance is %s N. Find the acceleration." % (d(Fd), num(m), num(res)), "%s m/s²" % d(a, 2),
                ["%s m/s²" % d(Fd / m, 2), "%s m/s²" % d((Fd + res) / m, 2), "%s m/s²" % d(m / Fd, 3)], "<i>a</i> = (%s − %s) ÷ %s." % (d(Fd), num(res), num(m)))


def lift(r):
    m = r.choice([50, 60, 70, 75, 80])
    a = r.choice([0.5, 1, 1.5, 2])
    up = r.random() < 0.5
    R_ = m * (G + a) if up else m * (G - a)
    return item("A person of mass %d kg stands in a lift that is accelerating %s at %s m/s². Find the reaction force from the floor (g = 9.8 m/s²)." % (m, "upwards" if up else "downwards", d(a)),
                "%s N" % d(R_, 1), ["%s N" % d(m * (G - a) if up else m * (G + a), 1), "%s N" % d(m * G, 1), "%s N" % d(m * a, 1)],
                "<i>R</i> − %dg = %d × %s." % (m, m, ("" if up else MINUS) + d(a)))


def pulley(r):
    m1, m2 = sorted(r.sample([2, 3, 4, 5, 6, 8], 2))
    a = G * (m2 - m1) / (m1 + m2)
    k = r.choice(["a", "T"])
    T_ = m1 * (G + a)
    ctx = "Particles of mass %d kg and %d kg hang on either side of a smooth pulley, connected by a light inextensible string. They are released from rest (g = 9.8 m/s²)." % (m1, m2)
    if k == "a":
        return item(ctx + " Find the acceleration, to 2 decimal places.", "%s m/s²" % d(a, 2), ["%s m/s²" % d(G * (m2 - m1) / m2, 2), "%s m/s²" % d(G, 2), "%s m/s²" % d(G * (m1 + m2) / (m2 - m1) if m2 != m1 else 0, 2)],
                    "%dg − %dg = (%d + %d)<i>a</i>." % (m2, m1, m1, m2))
    return item(ctx + " Find the tension in the string, to 1 decimal place.", "%s N" % d(T_, 1), ["%s N" % d(m1 * G, 1), "%s N" % d(m2 * G, 1), "%s N" % d((m1 + m2) * G, 1)],
                "For the lighter particle: <i>T</i> − %dg = %d<i>a</i>." % (m1, m1))


def resolve(r):
    Fv = r.choice([10, 20, 25, 40, 50, 60, 80, 100])
    ang = r.choice([20, 25, 30, 35, 40, 45, 50, 60])
    k = r.choice(["h", "v"])
    h, v = Fv * math.cos(math.radians(ang)), Fv * math.sin(math.radians(ang))
    if k == "h":
        return item("A force of %d N acts at %d° above the horizontal. Find its horizontal component, to 1 decimal place." % (Fv, ang), "%s N" % d(h, 1), ["%s N" % d(v, 1), "%s N" % d(Fv * math.tan(math.radians(ang)), 1), "%s N" % d(Fv / math.cos(math.radians(ang)), 1)],
                    "Horizontal = %d cos %d°." % (Fv, ang))
    return item("A force of %d N acts at %d° above the horizontal. Find its vertical component, to 1 decimal place." % (Fv, ang), "%s N" % d(v, 1), ["%s N" % d(h, 1), "%s N" % d(Fv * math.tan(math.radians(ang)), 1), "%s N" % d(Fv / math.sin(math.radians(ang)), 1)],
                "Vertical = %d sin %d°." % (Fv, ang))


def friction(r):
    m = r.choice([2, 3, 4, 5, 8, 10])
    mu = r.choice([0.1, 0.2, 0.25, 0.3, 0.4, 0.5])
    k = r.choice(["max", "slope", "acc"])
    if k == "max":
        Fr = mu * m * G
        return item("A box of mass %d kg rests on rough horizontal ground. μ = %s. Find the maximum friction, to 1 decimal place (g = 9.8 m/s²)." % (m, d(mu, 2)), "%s N" % d(Fr, 1),
                    ["%s N" % d(mu * m, 1), "%s N" % d(m * G, 1), "%s N" % d(m * G / mu, 1)], "<i>F</i><sub>max</sub> = μ<i>R</i> = %s × %d × 9.8." % (d(mu, 2), m))
    ang = r.choice([20, 25, 30, 35, 40])
    if k == "slope":
        comp = m * G * math.sin(math.radians(ang))
        return item("A particle of mass %d kg is on a smooth slope at %d° to the horizontal. Find the component of its weight down the slope, to 1 decimal place (g = 9.8 m/s²)." % (m, ang), "%s N" % d(comp, 1),
                    ["%s N" % d(m * G * math.cos(math.radians(ang)), 1), "%s N" % d(m * G, 1), "%s N" % d(m * math.sin(math.radians(ang)), 1)], "<i>mg</i> sin %d°." % ang)
    a = G * (math.sin(math.radians(ang)) - mu * math.cos(math.radians(ang)))
    if a <= 0:
        return None
    return item("A particle slides down a rough slope at %d° to the horizontal. μ = %s. Find its acceleration, to 2 decimal places (g = 9.8 m/s²)." % (ang, d(mu, 2)), "%s m/s²" % d(a, 2),
                ["%s m/s²" % d(G * math.sin(math.radians(ang)), 2), "%s m/s²" % d(G * (math.sin(math.radians(ang)) + mu * math.cos(math.radians(ang))), 2), "%s m/s²" % d(G * (math.cos(math.radians(ang)) - mu * math.sin(math.radians(ang))), 2)],
                "<i>a</i> = <i>g</i>(sin θ − μ cos θ). The mass cancels.")


def moments(r):
    L = r.choice([2, 3, 4, 5, 6])
    w = r.choice([20, 30, 40, 50, 60, 80])
    x = r.choice([0.5, 1, 1.5, 2])
    if x >= L:
        return None
    k = r.choice(["mom", "sup"])
    if k == "mom":
        Fv = r.choice([10, 15, 20, 25, 40])
        dist = r.choice([0.2, 0.25, 0.3, 0.4, 0.5, 1.5, 2])
        return item("A force of %d N acts at right angles to a spanner, %s m from the nut. Find the moment about the nut." % (Fv, d(dist, 2)), "%s Nm" % d(Fv * dist, 2),
                    ["%s Nm" % d(Fv / dist, 2), "%s Nm" % d(Fv + dist, 2), "%s Nm" % d(Fv * dist * 2, 2)], "Moment = force × perpendicular distance.")
    # uniform rod L, weight w, supports at ends; extra load P at x from left
    P = r.choice([10, 20, 30, 40])
    RB = (w * L / 2 + P * x) / L
    RA = w + P - RB
    return item("A uniform rod AB of length %d m and weight %d N rests on supports at A and B. A load of %d N is placed %s m from A. Find the reaction at B." % (L, w, P, d(x)), "%s N" % d(RB, 2),
                ["%s N" % d(RA, 2), "%s N" % d((w + P) / 2, 2), "%s N" % d(P * x / L, 2)], "Moments about A: %s × %d = %d × %s + %d × %s." % ("R<sub>B</sub>", L, w, d(L / 2), P, d(x)))


def projectile(r):
    u = r.choice([10, 14, 15, 20, 21, 25, 28, 30])
    ang = r.choice([30, 45, 60])
    k = r.choice(["t", "h", "range"])
    uy, ux = u * math.sin(math.radians(ang)), u * math.cos(math.radians(ang))
    T_ = 2 * uy / G
    ctx = "A ball is projected from level ground with speed %d m/s at %d° above the horizontal (g = 9.8 m/s², ignore air resistance)." % (u, ang)
    if k == "t":
        return item(ctx + " Find the time of flight, to 2 decimal places.", "%s s" % d(T_, 2), ["%s s" % d(uy / G, 2), "%s s" % d(2 * ux / G, 2), "%s s" % d(2 * u / G, 2)], "<i>T</i> = 2<i>u</i> sin θ ÷ <i>g</i>.")
    if k == "h":
        H = uy * uy / (2 * G)
        return item(ctx + " Find the greatest height, to 2 decimal places.", "%s m" % d(H, 2), ["%s m" % d(uy * uy / G, 2), "%s m" % d(u * u / (2 * G), 2), "%s m" % d(ux * ux / (2 * G), 2)], "<i>v</i>² = <i>u</i>² − 2<i>gh</i> with <i>v</i> = 0 vertically.")
    Rg = ux * T_
    return item(ctx + " Find the horizontal range, to 1 decimal place.", "%s m" % d(Rg, 1), ["%s m" % d(uy * T_, 1), "%s m" % d(ux * T_ / 2, 1), "%s m" % d(u * T_, 1)], "Range = horizontal speed × time of flight.")


def iterate(r):
    a, b = r.choice([2, 3, 4, 5, 6, 7]), r.choice([1, 2, 3])
    x0 = r.choice([1, 1.5, 2, 2.5, 3])
    # x_{n+1} = (a x_n + b)^(1/3)
    g = lambda x: (a * x + b) ** (1 / 3)
    x1 = g(x0)
    x2 = g(x1)
    k = r.choice(["x1", "x2"])
    v = x1 if k == "x1" else x2
    return item("Use the iteration %s<sub>n+1</sub> = ∛(%d%s<sub>n</sub> + %d) with %s<sub>0</sub> = %s. Find %s<sub>%s</sub>, to 4 decimal places." % (X, a, X, b, X, d(x0), X, k[1]),
                "%.4f" % v, ["%.4f" % (x1 if k == "x2" else x2), "%.4f" % ((a * x0 + b) / 3), "%.4f" % ((a * x0 + b) ** 0.5)],
                "Substitute each value back into the formula.")


def trapezium(r):
    f = r.choice([("x²", lambda x: x * x), ("x³", lambda x: x ** 3), ("√x", lambda x: x ** 0.5), ("1/x", lambda x: 1 / x),
                  ("x² + 1", lambda x: x * x + 1), ("2<sup>x</sup>", lambda x: 2 ** x), ("√(x + 1)", lambda x: (x + 1) ** 0.5), ("1/(1 + x)", lambda x: 1 / (1 + x))])
    a = r.choice([1, 2, 3])
    h = r.choice([0.25, 0.5, 1])
    nst = r.choice([2, 4])
    b = a + h * nst
    ys = [f[1](a + i * h) for i in range(nst + 1)]
    est = h / 2 * (ys[0] + ys[-1] + 2 * sum(ys[1:-1]))
    return item("Use the trapezium rule with %d strips to estimate ∫<sub>%s</sub><sup>%s</sup> %s d%s, to 3 decimal places." % (nst, d(a), d(b), f[0].replace("x", X), X), "%.3f" % est,
                ["%.3f" % (h * (ys[0] + ys[-1] + 2 * sum(ys[1:-1]))), "%.3f" % (h / 2 * sum(ys)), "%.3f" % (h * sum(ys[:-1]))],
                "Strip width %s. Area ≈ ½ × %s × [y₀ + y<sub>n</sub> + 2(the middle y-values)]." % (d(h), d(h)))


def varacc(r):
    a, b, c = r.choice([1, 2, 3]), r.randint(-6, 6), r.randint(0, 8)
    t = r.randint(1, 4)
    k = r.choice(["v", "a"])
    tt = "<i>t</i>"
    s = poly({3: a, 2: b, 1: c}, tt)
    v = 3 * a * t * t + 2 * b * t + c
    acc = 6 * a * t + 2 * b
    if k == "v":
        return item("A particle moves in a straight line with displacement <i>s</i> = %s metres at time %s seconds. Find its velocity when %s = %d." % (s, tt, tt, t), "%s m/s" % num(v),
                    ["%s m/s" % num(a * t ** 3 + b * t * t + c * t), "%s m/s" % num(acc), "%s m/s" % num(v + c)], "<i>v</i> = d<i>s</i>/d<i>t</i> = %s." % poly({2: 3 * a, 1: 2 * b, 0: c}, tt))
    return item("A particle moves in a straight line with displacement <i>s</i> = %s metres at time %s seconds. Find its acceleration when %s = %d." % (s, tt, tt, t), "%s m/s²" % num(acc),
                ["%s m/s²" % num(v), "%s m/s²" % num(6 * a * t), "%s m/s²" % num(acc + 2 * b if b else acc + 2)], "<i>a</i> = d²<i>s</i>/d<i>t</i>² = %s." % poly({1: 6 * a, 0: 2 * b}, tt))
