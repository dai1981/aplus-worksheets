# -*- coding: utf-8 -*-
"""
US Precalculus: Solving Trigonometric Equations (Common Core F-TF.B.7)
  python3 tools/gen_us_math_pc_solving_trigonometric_equations.py
Basic equations on [0, 2π), equations that need one or two steps, quadratic-type equations solved by
factoring, multiple angles and general solutions, and calculator solutions in models.
Wrong answers come from real mistakes: giving only the calculator answer, missing the second quadrant,
dividing by a trig function and losing solutions, and forgetting that 2x doubles the number of solutions.
"""
import math
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, num, MINUS, fr, People
from a2_common import sf
from pc_common import GRADE, trig, vhtml, pis, rad

R = random.Random(97601)
X = "<i>x</i>"
ANG = sorted(set(list(range(0, 360, 30)) + list(range(45, 360, 90))))


def sols(fn, sk):
    return [d for d in ANG if trig(fn, d) == sk]


def show(ds, use_rad):
    if not ds:
        return "No solution"
    f = (lambda d: pis(rad(d))) if use_rad else (lambda d: "%d°" % d)
    ds = sorted(ds)
    if len(ds) == 1:
        return f(ds[0])
    return ", ".join(f(d) for d in ds[:-1]) + (" and " if len(ds) == 2 else ", and ") + f(ds[-1])


def wrongs(fn, sk, ds, use_rad):
    out = []
    if len(ds) >= 2:
        out.append(show(ds[:1], use_rad))
    neg = (-sk[0], sk[1])
    out.append(show(sols(fn, neg), use_rad) if sk[1] != "0" else show([d + 90 for d in ds if d + 90 < 360], use_rad))
    other = {"sin": "cos", "cos": "sin", "tan": "tan"}[fn]
    od = sols(other, sk) if other != fn else [(d + 90) % 360 for d in ds]
    out.append(show(od, use_rad))
    if ds:
        out.append(show(sorted({(180 - ds[0]) % 360, (360 - ds[0]) % 360} - set(ds)) or [ds[0] + 180], use_rad))
    return out


VALS = {"sin": [(1, "1/2"), (-1, "1/2"), (1, "r2/2"), (-1, "r2/2"), (1, "r3/2"), (-1, "r3/2"), (1, "1"), (-1, "1"), (1, "0")],
        "tan": [(1, "1"), (-1, "1"), (1, "r3"), (-1, "r3"), (1, "r3/3"), (-1, "r3/3"), (1, "0")]}
VALS["cos"] = VALS["sin"]


def why(fn, sk, ds, use_rad):
    return "The reference angle has %s = %s. %s is %s in %s, so on one turn the solutions are <b>%s</b>." % (
        fn, vhtml((1, sk[1])), fn, "positive" if sk[0] > 0 else "negative",
        {"sin": "Quadrants I and II" if sk[0] > 0 else "Quadrants III and IV", "cos": "Quadrants I and IV" if sk[0] > 0 else "Quadrants II and III",
         "tan": "Quadrants I and III" if sk[0] > 0 else "Quadrants II and IV"}[fn], show(ds, use_rad))


# ------------------------------------------------------------ set 1: basic equations
def one_basic(r):
    fn = r.choice(["sin", "cos", "tan"])
    sk = r.choice(VALS[fn])
    ds = sols(fn, sk)
    use_rad = r.random() < 0.75
    q = "Solve %s %s = %s for %s." % (fn, X, vhtml(sk), ("0 ≤ %s &lt; 2π" if use_rad else "0° ≤ %s &lt; 360°") % X)
    right = show(ds, use_rad)
    if sk[1] == "0" or (sk[1] == "1" and fn != "tan"):
        e = "On the unit circle, %s = %s at <b>%s</b>." % (fn, vhtml(sk), right)
    else:
        e = why(fn, sk, ds, use_rad)
    return T(q, right, wrongs(fn, sk, ds, use_rad), e)


# ------------------------------------------------------------ set 2: isolate the function first
def one_lin(r):
    fn = r.choice(["sin", "cos", "tan"])
    kind = r.choice(["a", "b"])
    if fn == "tan":
        sk = r.choice([(1, "r3"), (-1, "r3"), (1, "1"), (-1, "1")])
        if sk[1] == "r3":
            eq = "tan %s %s √3 = 0" % (X, "−" if sk[0] > 0 else "+")
            how = "tan %s = %s" % (X, vhtml(sk))
        else:
            k = r.choice([2, 3, 4])
            eq = "%d tan %s %s %d = 0" % (k, X, "−" if sk[0] > 0 else "+", k)
            how = "tan %s = %s" % (X, vhtml(sk))
    else:
        sk = r.choice([(1, "1/2"), (-1, "1/2"), (1, "r3/2"), (-1, "r3/2"), (1, "r2/2"), (-1, "r2/2")])
        if sk[1] == "1/2":
            c = r.choice([0, 3, -1, 5])
            if c == 0:
                eq = "2 %s %s %s 1 = 0" % (fn, X, "−" if sk[0] > 0 else "+")
            else:
                eq = "2 %s %s %s %d = %s" % (fn, X, "+" if c > 0 else "−", abs(c), sf(c + sk[0]))
            how = "%s %s = %s" % (fn, X, vhtml(sk))
        elif sk[1] == "r3/2":
            eq = "2 %s %s %s √3 = 0" % (fn, X, "−" if sk[0] > 0 else "+")
            how = "%s %s = %s" % (fn, X, vhtml(sk))
        else:
            eq = "√2 %s %s %s 1 = 0" % (fn, X, "−" if sk[0] > 0 else "+")
            how = "%s %s = %s" % (fn, X, vhtml(sk))
    eq = eq.replace("−", MINUS)
    ds = sols(fn, sk)
    q = "Solve %s for 0° ≤ %s &lt; 360°." % (eq, X)
    right = show(ds, False)
    return T(q, right, wrongs(fn, sk, ds, False), "Isolate the function: %s. %s" % (how, why(fn, sk, ds, False)))


# ------------------------------------------------------------ set 3: factoring
def one_fact(r):
    kind = r.choice(["quad", "quad", "quad", "common"])
    if kind == "common":
        fn, other = r.choice([("sin", "cos"), ("cos", "sin")])
        sk = r.choice([(1, "1/2"), (-1, "1/2"), (1, "r3/2"), (-1, "r3/2")])
        coef = {"1/2": "2", "r3/2": "2"}[sk[1]]
        rhs = {"1/2": "", "r3/2": "√3 "}[sk[1]]
        eq = "%s %s %s %s = %s%s%s" % (coef, fn, X, other + " " + X, MINUS if sk[0] < 0 else "", rhs, other + " " + X)
        ds = sorted(set(sols(fn, sk)) | set(sols(other, (1, "0"))))
        q = "Solve %s for 0° ≤ %s &lt; 360°." % (eq, X)
        right = show(ds, False)
        lost = show(sols(fn, sk), False)
        return T(q, right, [lost, show(sols(other, (1, "0")), False), show(sorted(set(sols(fn, (-sk[0], sk[1]))) | set(sols(other, (1, "0")))), False)],
                 "Move everything to one side and factor: %s %s(%s %s %s %s) = 0. So %s %s = 0 or %s %s = %s. Do not divide by %s %s, or you lose solutions. <b>%s</b>." % (
                     other, X, coef, fn + " " + X, "+" if sk[0] < 0 else MINUS, rhs.strip() or "1", other, X, fn, X, vhtml(sk), other, X, right))
    fn = r.choice(["sin", "cos"])
    pool = [(1, "1/2"), (-1, "1/2"), (1, "1"), (-1, "1"), (1, "0")]
    a, b = r.sample(pool, 2)
    va = F(a[0]) * {"1/2": F(1, 2), "1": 1, "0": 0}[a[1]]
    vb = F(b[0]) * {"1/2": F(1, 2), "1": 1, "0": 0}[b[1]]
    # (2u − 2va)(u − vb) style with integer coefficients: k(u − va)(u − vb)
    k = 2 if (va.denominator == 2 or vb.denominator == 2) else 1
    c2, c1, c0 = k, -k * (va + vb), k * va * vb
    if any(F(c).denominator != 1 for c in (c1, c0)):
        return None
    u = "%s %s" % (fn, X)
    parts = ["%s%s²%s" % ("" if c2 == 1 else str(c2) + " ", fn, " " + X)]
    for c, t in ((c1, u), (c0, "")):
        if c == 0:
            continue
        parts.append("%s %s%s" % ("+" if c > 0 else MINUS, "" if (abs(c) == 1 and t) else num(abs(c)), (" " + t) if t and abs(c) != 1 else t))
    eq = " ".join(parts) + " = 0"
    ds = sorted(set(sols(fn, a)) | set(sols(fn, b)))
    q = "Solve %s for 0° ≤ %s &lt; 360°." % (eq, X)
    right = show(ds, False)
    wr = [show(sols(fn, a), False), show(sorted(set(sols(fn, (-a[0], a[1]) if a[1] != "0" else a)) | set(sols(fn, (-b[0], b[1]) if b[1] != "0" else b))), False), show(sols(fn, b), False)]
    return T(q, right, wr, "Factor like a quadratic in %s: %s = %s or %s = %s. Solve each one. <b>%s</b>." % (u, u, sf(va), u, sf(vb), right))


# ------------------------------------------------------------ set 4: multiple angles and general solutions
def one_multi(r):
    kind = r.choice(["count", "count", "gen", "gen", "gen"])
    if kind == "count":
        fn = r.choice(["sin", "cos"])
        n = r.choice([2, 3, 4])
        sk = r.choice([(1, "1/2"), (-1, "r2/2"), (1, "r3/2"), (1, "0"), (1, "1")])
        base = len(sols(fn, sk))
        q = "How many solutions does %s %d%s = %s have for 0 ≤ %s &lt; 2π?" % (fn, n, X, vhtml(sk), X)
        ans = base * n
        return T(q, str(ans), [str(base), str(ans + n) if ans + n != base else str(ans + 1), str(n)],
                 "%s θ = %s has %d solution%s per turn. As %s goes from 0 to 2π, %d%s goes around %d times, so there are <b>%d</b>." % (
                     fn, vhtml(sk), base, "" if base == 1 else "s", X, n, X, n, ans))
    fn = r.choice(["sin", "cos", "tan"])
    sk = r.choice([(1, "1/2"), (1, "r3/2"), (-1, "r2/2"), (1, "1"), (-1, "r3")] if fn != "tan" else [(1, "1"), (-1, "1"), (1, "r3"), (-1, "r3/3")])
    if fn != "tan" and sk[1] == "r3":
        return None
    ds = sols(fn, sk)
    k = "<i>k</i>"
    if fn == "tan":
        right = "%s = %s + π%s" % (X, pis(rad(ds[0])), k)
        wr = ["%s = %s + 2π%s" % (X, pis(rad(ds[0])), k), "%s = %s + π%s" % (X, pis(rad((ds[0] + 90) % 180)), k), "%s = %s" % (X, pis(rad(ds[0])))]
        e = "Tangent repeats every π, so add π%s to one solution. <b>%s</b>, where %s is any integer." % (k, right, k)
    else:
        if len(ds) == 1:
            right = "%s = %s + 2π%s" % (X, pis(rad(ds[0])), k)
            wr = ["%s = %s + π%s" % (X, pis(rad(ds[0])), k), "%s = %s" % (X, pis(rad(ds[0]))), "%s = %s + 2π%s" % (X, pis(rad((ds[0] + 180) % 360)), k)]
        else:
            right = "%s = %s + 2π%s or %s = %s + 2π%s" % (X, pis(rad(ds[0])), k, X, pis(rad(ds[1])), k)
            wr = ["%s = %s + 2π%s" % (X, pis(rad(ds[0])), k), "%s = %s + π%s" % (X, pis(rad(ds[0])), k),
                  "%s = %s + 2π%s or %s = %s + 2π%s" % (X, pis(rad(ds[0])), k, X, pis(rad((ds[0] + 180) % 360)), k)]
        e = "Find all solutions on one turn, then add 2π%s to each because %s repeats every 2π. <b>%s</b>, where %s is any integer." % (k, fn, right, k)
    q = "Which gives all solutions of %s %s = %s?" % (fn, X, vhtml(sk))
    fix = lambda t: t.replace("= 0 + ", "= ")
    return T(q, fix(right), [fix(w) for w in wr], fix(e))


# ------------------------------------------------------------ set 5: calculator solutions and models
def one_model(r):
    kind = r.choice(["calc", "calc", "tide", "wheel", "light"])
    if kind == "calc":
        fn = r.choice(["sin", "cos"])
        v = r.choice([0.2, 0.35, 0.4, 0.6, 0.75, 0.8, -0.25, -0.5, -0.6, -0.9])
        if v == -0.5:
            return None
        a = math.degrees(math.asin(v) if fn == "sin" else math.acos(v))
        if fn == "sin":
            s1 = a % 360
            s2 = (180 - a) % 360
        else:
            s1, s2 = a, 360 - a
        f1 = lambda d: num(F(round(d, 1)).limit_denominator(10)) + "°"
        ss = sorted([s1, s2])
        right = "%s and %s" % (f1(ss[0]), f1(ss[1]))
        q = "Solve %s %s = %s for 0° ≤ %s &lt; 360°. Round to the nearest tenth." % (fn, X, num(F(str(v))), X)
        p2 = sorted([a % 360, (a + 180) % 360])
        p3 = sorted([a % 360, (360 - a) % 360]) if fn == "sin" else sorted([a, 180 - a])
        wr = [f1(a), "%s and %s" % (f1(p2[0]), f1(p2[1])), "%s and %s" % (f1(p3[0]), f1(p3[1]))]
        return T(q, right, wr, "The calculator gives %s⁻¹(%s) ≈ %s. %s The solutions are <b>%s</b>." % (
            fn, num(F(str(v))), f1(a), "The other solution has the same sine: 180° − θ." if fn == "sin" else "The other solution has the same cosine: 360° − θ.", right))
    if kind == "tide":
        mid = r.choice([4, 5, 6])
        amp = r.choice([2, 3, 4])
        q = ("The depth of water in a harbor is <i>d</i>(<i>t</i>) = %d + %d sin(π<i>t</i>/6) meters, <i>t</i> hours after midnight. "
             "In the first 12 hours, when is the depth %s m?" % (mid, amp, num(F(2 * mid + amp, 2))))
        right = "At 1:00 a.m. and 5:00 a.m."
        return T(q, right, ["At 1:00 a.m. only", "At 3:00 a.m. and 9:00 a.m.", "At 2:00 a.m. and 4:00 a.m."],
                 "sin(π<i>t</i>/6) = %s ÷ %d = 1/2, so π<i>t</i>/6 = π/6 or 5π/6, and <i>t</i> = 1 or 5. <b>%s</b>" % (num(F(amp, 2)), amp, right))
    if kind == "wheel":
        rr = r.choice([20, 25, 30])
        c = rr + r.choice([3, 5])
        per = r.choice([8, 10, 12])
        h = c + F(rr, 2)
        q = ("A Ferris wheel seat is at height <i>h</i>(<i>t</i>) = %d − %d cos(2π<i>t</i>/%d) feet after <i>t</i> minutes. "
             "When does the seat first reach %s ft?" % (c, rr, per, num(h)))
        t1 = F(per, 3)
        right = "After %s minutes" % sf(t1)
        return T(q, right, ["After %s minutes" % sf(F(per, 6)), "After %s minutes" % sf(F(2 * per, 3)), "After %s minutes" % sf(F(per, 2))],
                 "cos(2π<i>t</i>/%d) = (%d − %s) ÷ %d = −1/2, so 2π<i>t</i>/%d = 2π/3 and <i>t</i> = %d/3. <b>%s</b>." % (per, c, num(h), rr, per, per, right))
    days = 365
    q = ("The hours of daylight in a city are <i>D</i>(<i>t</i>) = 12 + 3 sin(2π<i>t</i>/365), where <i>t</i> is days after March 20. "
         "Within one year, on which days after March 20 are there exactly 13.5 hours of daylight?")
    t1, t2 = days / 12, days * 5 / 12
    right = "About day %d and day %d" % (round(t1), round(t2))
    return T(q, right, ["About day %d only" % round(t1), "About day %d and day %d" % (round(days / 6), round(days / 3)), "About day %d and day %d" % (round(days / 4), round(days * 3 / 4))],
             "sin(2π<i>t</i>/365) = 1.5 ÷ 3 = 1/2, so 2π<i>t</i>/365 = π/6 or 5π/6. <i>t</i> = 365/12 ≈ %d or 5 × 365/12 ≈ %d. <b>%s</b>." % (round(t1), round(t2), right))


def build():
    sets = [S("Basic equations", collect(one_basic, 20, R)),
            S("Isolating the function", collect(one_lin, 20, R)),
            S("Solving by factoring", collect(one_fact, 20, R)),
            S("Multiple angles and general solutions", collect(one_multi, 20, R)),
            S("Calculator solutions and models", collect(one_model, 20, R))]
    body = lesson(
        "<ul><li>Isolate the trig function, find the reference angle, then use the sign to choose the quadrants.</li>"
        "<li>On one turn (0 to 2π), sin <i>x</i> = <i>c</i> and cos <i>x</i> = <i>c</i> usually have <b>two</b> solutions; tan <i>x</i> = <i>c</i> has two that are π apart.</li>"
        "<li>For quadratic-type equations, factor. Never divide by sin <i>x</i> or cos <i>x</i>; factor it out instead.</li>"
        "<li>All solutions: add 2π<i>k</i> (sine and cosine) or π<i>k</i> (tangent). For sin 2<i>x</i> = <i>c</i>, there are twice as many solutions on one turn.</li></ul>",
        [("Solve 2 sin <i>x</i> + 1 = 0 for 0 ≤ <i>x</i> &lt; 2π.", ["sin <i>x</i> = −1/2", "Reference angle π/6; sine is negative in Quadrants III and IV"], fr("7π", 6) + " and " + fr("11π", 6)),
         ("Solve 2 cos² <i>x</i> − cos <i>x</i> − 1 = 0 for 0° ≤ <i>x</i> &lt; 360°.", ["(2 cos <i>x</i> + 1)(cos <i>x</i> − 1) = 0", "cos <i>x</i> = −1/2 or cos <i>x</i> = 1"], "0°, 120°, and 240°")],
        ["Giving only the calculator answer and missing the second solution.",
         "Choosing the wrong quadrants for a negative value.",
         "Dividing both sides by cos <i>x</i> and losing the solutions where cos <i>x</i> = 0.",
         "Forgetting that sin 2<i>x</i> has twice as many solutions on one turn."])
    faq = [("How many solutions does sin x = 1/2 have?", "Two between 0 and 2π (π/6 and 5π/6), and infinitely many in all: x = π/6 + 2πk or x = 5π/6 + 2πk."),
           ("How do you solve a quadratic trig equation?", "Treat sin x (or cos x) as the variable, factor, set each factor to 0, and solve each basic equation."),
           ("Why should you not divide by sin x?", "Because sin x may be 0, and dividing removes those solutions. Factor sin x out instead."),
           ("How do you write the general solution?", "Find the solutions on one turn and add 2πk for sine and cosine, or πk for tangent, where k is any integer.")]
    make("solving-trigonometric-equations", 6, "F-TF.B.7",
         "Solving Trigonometric Equations",
         "Solving Trigonometric Equations Worksheet (Precalculus) | 100 Questions with Answers",
         "Trig Equations",
         "Use inverse functions to solve trigonometric equations that arise in modeling contexts; evaluate the solutions using technology, and interpret them in terms of the context.",
         "Free precalculus worksheet on solving trigonometric equations: basic equations, factoring, multiple angles, general solutions and periodic models. 100 questions with answers.",
         "Isolate the function, find the reference angle, then use the quadrants.",
         "Sine and cosine usually have two solutions per turn. Factor; do not divide.",
         body, faq, sets, R, domain="Trigonometric Functions", grade=GRADE)


if __name__ == "__main__":
    build()
