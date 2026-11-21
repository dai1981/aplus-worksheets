# -*- coding: utf-8 -*-
"""
India Class 10 Maths, NCERT Chapter 4: Quadratic Equations (CBSE Unit II Algebra)
  python3 tools/gen_in_maths_c10_quadratic_equations.py
Recognising a quadratic equation and its standard form, solving by factorisation (SG Secondary 2 makers), the quadratic
formula with exact (surd) roots, the discriminant and nature of roots (equal roots, finding k), and word problems
(numbers, rectangles, right triangles from SG Secondary 3; speed and time, and ages, written here).
Wrong answers come from real mistakes: not expanding before deciding, −b/2a without the ±√D, using b² + 4ac,
"no real roots" when D = 0, and keeping a negative length.
"""
import random, math
from fractions import Fraction as F
from in_common import num, S, make, lesson, mix, T, expr, fv, People, adopt, MINUS
import gen_sg_maths_s2_quadratic_equations as sgq
import gen_sg_maths_s3_quadratic_equation_word_problems as sgw

R = random.Random(910004)
P = People(R)
adopt(sgq, R)
adopt(sgw, R)
X = "<i>x</i>"
X2 = X + "²"


def quad(a, b, c):
    return expr([(a, X2), (b, X), (c, "")])


def lin(a, b):
    return expr([(a, X), (b, "")])


def nz(lo=-9, hi=9):
    return [k for k in range(lo, hi + 1) if k]


# ---------------------------------------------------------------- set 1: is it quadratic? standard form
def one_std(r):
    kind = r.choice(["is", "is", "std", "std"])
    a, b = r.choice(nz(-5, 5)), r.choice(nz(-6, 6))
    c, d = r.choice(nz(-5, 5)), r.choice(nz(-6, 6))
    if kind == "is":
        t = r.choice(["yes", "no_cancel", "no_cubic", "yes2"])
        if t == "yes":
            e = "(%s)² = 2(%s)" % (lin(1, a), lin(1, b))
            ans, why = "Yes", "Expanding gives %s = 0, which has an %s² term." % (quad(1, 2 * a - 2, a * a - 2 * b), X)
        elif t == "yes2":
            e = "%s(%s) = %s" % (X, lin(1, a), lin(c, d))
            ans, why = "Yes", "Expanding gives %s = 0 (degree 2)." % quad(1, a - c, -d)
        elif t == "no_cancel":
            e = "(%s)² = %s" % (lin(1, a), quad(1, b, c))
            if 2 * a == b:
                return None
            ans, why = "No", "Expanding: %s = %s. The %s² terms cancel, leaving %s = 0, which is linear." % (quad(1, 2 * a, a * a), quad(1, b, c), X, lin(2 * a - b, a * a - c))
        else:
            e = "(%s)³ = %s" % (lin(1, a), expr([(1, X + "³"), (b, X)]))
            ans, why = "Yes", "Expanding: the %s³ terms cancel and %s = 0 remains, which has degree 2." % (X, quad(3 * a, 3 * a * a - b, a ** 3))
        return T("Is %s a quadratic equation?" % e, ans, ["No" if ans == "Yes" else "Yes", "Only if %s &gt; 0" % X, "It cannot be decided without solving"],
                 "Write it in the form a%s² + b%s + c = 0 first. %s <b>%s</b>." % (X, X, why, ans))
    e = "(%s)(%s) = %s" % (lin(1, a), lin(1, b), num(c))
    std = quad(1, a + b, a * b - c)
    return T("Write %s in the standard form a%s² + b%s + c = 0." % (e, X, X), std + " = 0",
             [quad(1, a + b, a * b + c) + " = 0", quad(1, a * b, a + b - c) + " = 0", quad(1, -(a + b), a * b - c) + " = 0"],
             "Expand: %s = %s, then subtract %s: <b>%s = 0</b>." % (quad(1, a + b, a * b), num(c), num(c), std))


# ---------------------------------------------------------------- set 3: quadratic formula (exact roots)
def surd_parts(n):
    k, m = 1, n
    for f in range(int(math.isqrt(n)), 1, -1):
        if n % (f * f) == 0:
            k, m = f, n // (f * f)
            break
    return k, m


def roots_str(a, b, c):
    D = b * b - 4 * a * c
    s = math.isqrt(D)
    if s * s == D:
        r1, r2 = F(-b + s, 2 * a), F(-b - s, 2 * a)
        return "%s = %s or %s = %s" % (X, fv(max(r1, r2)), X, fv(min(r1, r2)))
    k, m = surd_parts(D)
    g = math.gcd(math.gcd(abs(b), k), 2 * a)
    nb, nk, den = -b // g, k // g, 2 * a // g
    if den < 0:
        nb, nk, den = -nb, nk, -den
    top = "%s ± %s√%d" % (num(nb), "" if nk == 1 else num(nk), m) if nb else "±%s√%d" % ("" if nk == 1 else num(nk), m)
    if den == 1:
        return "%s = %s" % (X, top)
    return "%s = (%s)/%d" % (X, top, den)


def one_formula(r):
    a = r.choice([1, 1, 2, 3, 4])
    b = r.choice(nz(-9, 9))
    c = r.choice(nz(-9, 9))
    D = b * b - 4 * a * c
    if D <= 0:
        return None
    kind = r.choice(["solve", "solve", "solve", "D"])
    if kind == "D":
        return T("Find the discriminant of %s = 0." % quad(a, b, c), num(D), [num(b * b + 4 * a * c), num(b - 4 * a * c), num(-b * b + 4 * a * c) if -b * b + 4 * a * c != D else num(D + 4)],
                 "D = b² − 4ac = (%s)² − 4(%s)(%s) = <b>%s</b>." % (num(b), num(a), num(c), num(D)))
    ans = roots_str(a, b, c)
    w1 = roots_str(a, -b, c)
    alt = [w1]
    # mistakes: denominator a instead of 2a, only one root, forgetting to simplify
    s = math.isqrt(D)
    if s * s == D:
        r1, r2 = F(-b + s, a), F(-b - s, a)
        alt.append("%s = %s or %s = %s" % (X, fv(max(r1, r2)), X, fv(min(r1, r2))))
        r1, r2 = F(-b + s, 2 * a), F(-b - s, 2 * a)
        alt.append("%s = %s" % (X, fv(max(r1, r2))))
    else:
        k, m = surd_parts(D)
        alt.append("%s = %s ± %s√%d" % (X, fv(F(-b, 2 * a)), "" if k == 1 else num(k), m))
        alt.append("%s = %s ± √%d" % (X, num(-b), D))
    alt = [t for t in alt if t != ans]
    return T("Solve %s = 0 using the quadratic formula." % quad(a, b, c), ans, alt[:3] if len(alt) >= 3 else alt + [roots_str(a, b + 2 if (b + 2) else 3, c)],
             "D = b² − 4ac = %s. %s = (−b ± √D)/(2a) = (%s ± √%s)/%d, so <b>%s</b>." % (num(D), X, num(-b), num(D), 2 * a, ans))


# ---------------------------------------------------------------- set 4: nature of roots
def one_nature(r):
    kind = r.choice(["type", "type", "k", "k"])
    if kind == "type":
        t = r.choice(["two", "equal", "none"])
        a = r.choice([1, 2, 3, 4, 9])
        if t == "equal":
            m = r.choice(nz(-6, 6))
            sa = int(math.isqrt(a))
            if sa * sa != a:
                return None
            b, c = 2 * sa * m, m * m
        else:
            b = r.choice(nz(-9, 9))
            c = r.choice(nz(-9, 12))
            D = b * b - 4 * a * c
            if (t == "two" and D <= 0) or (t == "none" and D >= 0):
                return None
        D = b * b - 4 * a * c
        names = {"two": "two distinct real roots", "equal": "two equal real roots", "none": "no real roots"}
        return T("What is the nature of the roots of %s = 0?" % quad(a, b, c), names[t].capitalize(), [names[o].capitalize() for o in names if o != t] + ["Three real roots"],
                 "D = b² − 4ac = %s %s 0, so <b>%s</b>." % (num(D), "&gt;" if D > 0 else ("=" if D == 0 else "&lt;"), names[t]))
    a = r.choice([1, 2, 3, 4])
    m = r.choice([1, 2, 3, 4, 5, 6])
    t = r.choice(["b", "c"])
    if t == "c":
        b = 2 * m * r.choice([1, 2]) * (1 if a == 1 else a)
        if (b * b) % (4 * a):
            return None
        k = b * b // (4 * a)
        return T("Find k so that %s = 0 has two equal roots." % expr([(a, X2), (b, X), (1, "k")]).replace("1k", "k"), "k = %s" % num(k),
                 ["k = %s" % num(-k), "k = %s" % num(b * b), "k = %s" % num(F(b, 2 * a)) if F(b, 2 * a).denominator == 1 and F(b, 2 * a) != k else "k = %s" % num(k + 1)],
                 "Equal roots when D = 0: %s² − 4(%s)k = 0, so <b>k = %s</b>." % (num(b), num(a), num(k)))
    c = m * m * a
    kk = 2 * a * m
    return T("Find the positive value of k for which %s = 0 has two equal roots." % ("%skx + %s" % (expr([(a, X2)]) + " + ", num(c))).replace("kx", "k" + X), "k = %s" % num(kk),
             ["k = %s" % num(kk // 2) if kk // 2 != kk else "k = %s" % num(kk + 2), "k = %s" % num(4 * a * c), "k = %s" % num(m)],
             "D = k² − 4(%s)(%s) = 0, so k² = %s and k = ±%s. The positive value is <b>k = %s</b>." % (num(a), num(c), num(kk * kk), num(kk), num(kk)))


# ---------------------------------------------------------------- set 5: word problems (own)
def one_speed(r):
    kind = r.choice(["train", "age", "prod", "train"])
    name, he, his = P.next()
    if kind == "train":
        v = r.choice([30, 36, 40, 45, 48, 50, 60, 72])
        d = r.choice([180, 360, 240, 480, 300, 600])
        inc = r.choice([5, 10, 12, 15])
        t1, t2 = F(d, v), F(d, v + inc)
        dt = t1 - t2
        if dt.denominator != 1 and dt not in (F(1, 2), F(3, 2), F(5, 2)):
            return None
        hrs = ("%s hour%s" % (fv(dt), "" if dt <= 1 else "s"))
        return T("A train travels %d km at a uniform speed. If the speed had been %d km/h more, it would have taken %s less. Find the speed of the train." % (d, inc, hrs),
                 "%d km/h" % v, ["%d km/h" % (v + inc), "%d km/h" % (v - inc), "%d km/h" % (v * 2)],
                 "%d/%s − %d/(%s) = %s gives %s = 0. The positive root is <b>%d km/h</b>." % (d, X, d, lin(1, inc), fv(dt), quad(1, inc, int(-d * inc / dt)), v))
    if kind == "age":
        a = r.randint(8, 20)
        g = r.randint(2, 12)
        b = a + g
        n = r.choice([3, 4, 5])
        p_ = (a - n) * (b - n)
        if a - n <= 0:
            return None
        return T("%s's brother is %d years older than %s. %d years ago, the product of their ages was %s. How old is %s now?" % (name, g, "her" if he == "she" else "him", n, num(p_), name),
                 "%d years" % a, ["%d years" % b, "%d years" % (a - n), "%d years" % (a + n)],
                 "Let %s be %s years old: (%s)(%s) = %s. The positive root gives <b>%d years</b>." % (name, X, lin(1, -n), lin(1, g - n), num(p_), a))
    n = r.randint(6, 30)
    return T("The product of two consecutive odd positive integers is %s. Find the smaller integer." % num((2 * n - 1) * (2 * n + 1)), num(2 * n - 1),
             [num(2 * n + 1), num(2 * n), num(2 * n - 3)],
             "Let them be %s and %s + 2: %s(%s) = %s gives %s = 0, so the smaller is <b>%s</b>." % (X, X, X, lin(1, 2), num((2 * n - 1) * (2 * n + 1)), quad(1, 2, -(2 * n - 1) * (2 * n + 1)), num(2 * n - 1)))


def main():
    seen = set()
    sets = [
        S("Quadratic equations and standard form", mix(R, [(one_std, 20)], seen)),
        S("Solving by factorisation", mix(R, [(sgq.one_monic, 8), (sgq.one_nonmonic, 8), (sgq.one_special, 4)], seen)),
        S("Quadratic formula", mix(R, [(one_formula, 20)], seen)),
        S("Discriminant and nature of roots", mix(R, [(one_nature, 20)], seen)),
        S("Word problems", mix(R, [(sgw.one_num, 6), (sgw.one_geo, 6), (one_speed, 8)], seen)),
    ]
    body = lesson(
        "<p>A <b>quadratic equation</b> can be written as a%s² + b%s + c = 0 with a ≠ 0. Always expand and simplify before deciding.</p>"
        "<p>Solve by <b>factorisation</b> (split the middle term) or by the <b>quadratic formula</b> %s = (−b ± √(b² − 4ac))/(2a).</p>"
        "<p>The <b>discriminant</b> D = b² − 4ac tells the nature of the roots: D &gt; 0 two distinct real roots, D = 0 two equal real roots, D &lt; 0 no real roots.</p>" % (X, X, X),
        [("Solve 2x² − 5x + 3 = 0.", ["2x² − 2x − 3x + 3 = 0", "(x − 1)(2x − 3) = 0"], "x = 1 or x = 3/2"),
         ("Find k so that kx(x − 2) + 6 = 0 has equal roots.", ["kx² − 2kx + 6 = 0", "D = 4k² − 24k = 0"], "k = 6")],
        ["Deciding from the look of an equation without expanding it.",
         "Using b² + 4ac for the discriminant.",
         "Keeping a negative answer for a length, speed or age."])
    faq = [
        ("What is the quadratic formula?", "For ax² + bx + c = 0 with b² − 4ac ≥ 0, the roots are x = (−b ± √(b² − 4ac))/(2a)."),
        ("What does the discriminant tell us?", "D = b² − 4ac. If D > 0 there are two distinct real roots, if D = 0 two equal real roots, and if D < 0 no real roots."),
        ("How do I solve a quadratic equation by factorisation?", "Write it as ax² + bx + c = 0, split the middle term into two terms whose product is ac, factorise and set each factor to 0."),
        ("Why do we reject one root in word problems?", "A length, speed, age or number of items cannot be negative, so the negative root does not fit the situation."),
    ]
    make(10, "quadratic-equations", 4, "II", 4, "Quadratic Equations", "quadratic equations",
         "Standard form of a quadratic equation ax² + bx + c = 0 (a ≠ 0); solutions by factorisation and by using the quadratic formula; relationship between discriminant and nature of roots; situational problems based on quadratic equations related to day to day activities (summary of the CBSE syllabus)",
         "Class 10 Quadratic Equations worksheet (NCERT Chapter 4): standard form, factorisation, quadratic formula, discriminant and nature of roots, word problems. 100 questions with answers.",
         "x = (−b ± √(b² − 4ac)) / 2a", "D = b² − 4ac decides the nature of the roots.",
         body, faq, sets, R)


if __name__ == "__main__":
    main()
