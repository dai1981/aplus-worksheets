# -*- coding: utf-8 -*-
"""
India Class 10 Maths, NCERT Chapter 3: Pair of Linear Equations in Two Variables (CBSE Unit II Algebra)
  python3 tools/gen_in_maths_c10_pair_of_linear_equations.py
Checking a solution and reading the solution from a graph, consistency from the ratios a₁/a₂, b₁/b₂, c₁/c₂ (unique,
infinitely many, no solution) and finding k, substitution and elimination (SG Secondary 2 makers with Indian wording),
and word problems (prices in rupees, ages, taxi fares, library fines, rectangles, fractions).
Wrong answers come from real mistakes: swapping x and y, comparing the wrong ratios, calling parallel lines
"infinitely many", and finding only one of the two values.
"""
import random
from fractions import Fraction as F
from in_common import num, S, make, lesson, mix, T, expr, fv, inr, People, adopt, MINUS
from pc_common import curve_svg
import gen_sg_maths_s2_simultaneous_equations as sgse

R = random.Random(910003)
P = People(R)
adopt(sgse, R)
X, Y = "<i>x</i>", "<i>y</i>"


def eq(a, b, c):
    return "%s = %s" % (expr([(a, X), (b, Y)]), num(c))


def eq0(a, b, c):
    return "%s = 0" % expr([(a, X), (b, Y), (c, "")])


def ans(x, y):
    return "%s = %s, %s = %s" % (X, fv(x), Y, fv(y))


def nz(lo, hi):
    return [k for k in range(lo, hi + 1) if k]


def wr(x, y, extra=()):
    out = []
    for a in [ans(y, x), ans(x, -y), ans(-x, y)] + list(extra):
        if a != ans(x, y) and a not in out:
            out.append(a)
    return out[:3]


def indian(f):
    def g(r):
        it = f(r)
        if it:
            it["q"] = it["q"].replace("Solve the simultaneous equations.", "Solve the pair of linear equations by elimination.")
        return it
    g.__name__ = f.__name__
    return g


# ---------------------------------------------------------------- set 1: check a solution, graphs
def one_graph(r):
    kind = r.choice(["graph", "graph", "check", "check"])
    if kind == "graph":
        x, y = r.choice(nz(-3, 3)), r.choice(nz(-3, 3))
        m1, m2 = r.sample([-2, -1, F(-1, 2), F(1, 2), 1, 2], 2)
        c1, c2 = y - m1 * x, y - m2 * x
        pic = curve_svg(lambda t: float(m1 * t + c1), -5, 5, -5, 5, unit=24, label="two lines")
        pic2 = curve_svg(lambda t: float(m2 * t + c2), -5, 5, -5, 5, unit=24, label="two lines", col="#c0392b")
        import re
        lines2 = re.findall(r"<polyline[^>]*/>", pic2)
        pic = pic.replace("</g></svg>", "".join(lines2) + "<circle cx='%.1f' cy='%.1f' r='5' fill='#2b2b2b'/></g></svg>" % (22 + (x + 5) * 24, 22 + (5 - y) * 24))
        return T(pic + "The graphs of two linear equations are shown. What is the solution of the pair?", ans(x, y), wr(x, y, [ans(x + 1, y)]),
                 "The solution is the point where the two lines intersect: (%s, %s), so <b>%s</b>." % (num(x), num(y), ans(x, y)))
    x, y = r.choice(nz(-6, 6)), r.choice(nz(-6, 6))
    a1, b1 = r.choice(nz(-4, 5)), r.choice(nz(-4, 5))
    a2, b2 = r.choice(nz(-4, 5)), r.choice(nz(-4, 5))
    if a1 * b2 == a2 * b1 or x == y:
        return None
    e1, e2 = eq(a1, b1, a1 * x + b1 * y), eq(a2, b2, a2 * x + b2 * y)
    cands = [(x, y), (y, x), (x, -y), (-x, y)]
    good = "(%s, %s)" % (num(x), num(y))
    wrongs_ = ["(%s, %s)" % (num(p), num(q)) for p, q in cands[1:] if (p, q) != (x, y)]
    return T("Which point (%s, %s) is the solution of the pair<br>%s<br>%s ?" % (X, Y, e1, e2), good, wrongs_,
             "Substitute into both equations: %s and %s are both true for <b>%s</b>." % (e1.replace(X, "(%s)" % num(x)).replace(Y, "(%s)" % num(y)), e2.replace(X, "(%s)" % num(x)).replace(Y, "(%s)" % num(y)), good))


# ---------------------------------------------------------------- set 2: consistency
def one_cons(r):
    kind = r.choice(["type", "type", "type", "k", "k"])
    a1, b1 = r.choice(nz(-5, 6)), r.choice(nz(-5, 6))
    c1 = r.choice(nz(-9, 9))
    t = r.choice(["unique", "inf", "none"])
    if kind == "type":
        if t == "unique":
            a2, b2, c2 = r.choice(nz(-5, 6)), r.choice(nz(-5, 6)), r.choice(nz(-9, 9))
            if a1 * b2 == a2 * b1:
                return None
        else:
            k = r.choice([2, 3, -2, 4, F(1, 2)])
            a2, b2 = a1 * k, b1 * k
            c2 = c1 * k if t == "inf" else c1 * k + r.choice([1, 2, -3, 5])
            if any(F(v).denominator != 1 for v in (a2, b2, c2)):
                return None
        names = {"unique": "a unique solution (intersecting lines)", "inf": "infinitely many solutions (coincident lines)", "none": "no solution (parallel lines)"}
        why = {"unique": "a₁/a₂ ≠ b₁/b₂", "inf": "a₁/a₂ = b₁/b₂ = c₁/c₂", "none": "a₁/a₂ = b₁/b₂ ≠ c₁/c₂"}
        return T("How many solutions does this pair have?<br>%s<br>%s" % (eq0(a1, b1, c1), eq0(a2, b2, c2)), names[t].capitalize(),
                 [names[o].capitalize() for o in names if o != t] + ["Exactly two solutions"],
                 "a₁/a₂ = %s, b₁/b₂ = %s, c₁/c₂ = %s, so %s: <b>%s</b>." % (fv(F(a1) / a2), fv(F(b1) / b2), fv(F(c1) / c2), why[t], names[t]))
    k = r.choice([2, 3, 4, -2])
    a2 = a1 * k
    t = r.choice(["none", "inf"])
    c2 = c1 * k if t == "inf" else c1 * k + r.choice([1, 2, 3])
    want = b1 * k
    e2 = "%s + p%s %s %s = 0" % (expr([(a2, X)]), Y, "+" if c2 > 0 else MINUS, num(abs(c2)))
    if t == "none":
        return T("For which value of p does the pair %s and %s have no solution?" % (eq0(a1, b1, c1), e2),
                 "p = %s" % num(want), ["p = %s" % num(-want), "p = %s" % num(b1), "p = %s" % num(want + 1)],
                 "Parallel lines: a₁/a₂ = b₁/b₂ ≠ c₁/c₂. %s/%s = %s/p gives <b>p = %s</b> (and c₁/c₂ is different)." % (num(a1), num(a2), num(b1), num(want)))
    return T("For which value of p does the pair %s and %s have infinitely many solutions?" % (eq0(a1, b1, c1), e2),
             "p = %s" % num(want), ["p = %s" % num(-want), "p = %s" % num(b1), "p = %s" % num(c2) if c2 not in (want, -want, b1) else "p = %s" % num(want + 1)],
             "Coincident lines: a₁/a₂ = b₁/b₂ = c₁/c₂ = %s. So p = %s × %s = <b>%s</b>." % (fv(F(1, k)), num(k), "(%s)" % num(b1) if b1 < 0 else num(b1), num(want)))


# ---------------------------------------------------------------- set 5: word problems
def one_word(r):
    kind = r.choice(["shop", "age", "taxi", "fine", "rect", "frac", "notes"])
    name, he, his = P.next()
    if kind == "shop":
        (p1, s1, lo1, hi1), (p2, s2, lo2, hi2) = r.choice([
            (("pens", "pen", 10, 40), ("pencils", "pencil", 3, 10)), (("bats", "bat", 300, 900), ("balls", "ball", 50, 150)),
            (("notebooks", "notebook", 25, 60), ("erasers", "eraser", 5, 15)), (("chairs", "chair", 400, 900), ("stools", "stool", 150, 350))])
        st = 5 if lo1 >= 25 else 1
        x = r.randrange(lo1, hi1, st)
        y = r.randrange(lo2, hi2, 5 if lo2 >= 25 else 1)
        a1, b1, a2, b2 = r.randint(1, 5), r.randint(1, 6), r.randint(1, 5), r.randint(1, 6)
        if a1 * b2 == a2 * b1 or x == y:
            return None
        g = lambda n, p_, s_: "%d %s" % (n, p_ if n > 1 else s_)
        d = 5 if st == 5 else 1
        return T("%s and %s cost %s. %s and %s cost %s. Find the cost of one %s and one %s." % (g(a1, p1, s1), g(b1, p2, s2), inr(a1 * x + b1 * y), g(a2, p1, s1), g(b2, p2, s2), inr(a2 * x + b2 * y), s1, s2),
                 "%s and %s" % (inr(x), inr(y)), ["%s and %s" % (inr(y), inr(x)), "%s and %s" % (inr(x + d), inr(y - d)) if y > d else "%s and %s" % (inr(x + 2 * d), inr(y)), "%s and %s" % (inr(x - d), inr(y + d))],
                 "Let one %s cost ₹%s and one %s cost ₹%s: %s and %s. Solving gives <b>%s and %s</b>." % (s1, X, s2, Y, eq(a1, b1, a1 * x + b1 * y), eq(a2, b2, a2 * x + b2 * y), inr(x), inr(y)))
    if kind == "age":
        son = r.randint(6, 20)
        k = r.choice([2, 3, 4])
        fa = son * k + r.choice([0, 2, 4, 6])
        n = r.choice([5, 10])
        if fa - son < 18 or fa > 70:
            return None
        m = F(fa + n, son + n)
        if m.denominator != 1:
            return None
        return T("The sum of the ages of %s and %s father is %d years. After %d years, the father will be %d times as old as %s. How old are they now?" % (name, his, fa + son, n, m, name),
                 "%s: %d years, father: %d years" % (name, son, fa), ["%s: %d years, father: %d years" % (name, son + n, fa - n), "%s: %d years, father: %d years" % (name, son - 1, fa + 1), "%s: %d years, father: %d years" % (name, son + 2, fa - 2)],
                 "%s + %s = %d and %s + %d = %d(%s + %d). Solving gives <b>%d and %d years</b>." % (X, Y, fa + son, Y, n, m, X, n, son, fa))
    if kind == "taxi":
        f = r.choice([20, 25, 30, 40, 50])
        c = r.choice([8, 10, 12, 14, 15, 18])
        d1, d2 = r.sample(range(5, 26), 2)
        return T("A taxi charges a fixed amount plus a charge per km. For %d km the fare is %s and for %d km it is %s. What is the fixed charge?" % (d1, inr(f + c * d1), d2, inr(f + c * d2)),
                 inr(f), [inr(c), inr(f + c), inr(F(f + c * d1, d1)) if F(f + c * d1, d1).denominator == 1 and F(f + c * d1, d1) != c else inr(f + 10)],
                 "%s + %d%s = %d and %s + %d%s = %d. Subtract: %s = ₹%d per km, so fixed charge <b>%s</b>." % (X, d1, Y, f + c * d1, X, d2, Y, f + c * d2, Y, c, inr(f)))
    if kind == "fine":
        f = r.choice([10, 15, 20, 25, 30])
        c = r.choice([2, 3, 4, 5])
        d1, d2 = r.sample(range(3, 15), 2)
        return T("A library charges a fixed fee for the first 3 days and an extra charge for each day after that. %s paid %s for a book kept %d days and %s for %d days. What is the charge for each extra day?" % (name, inr(f + c * (d1 - 3)), d1, inr(f + c * (d2 - 3)), d2),
                 inr(c), [inr(f), inr(c + 1), inr(F(f + c * (d1 - 3), d1)) if F(f + c * (d1 - 3), d1).denominator == 1 and F(f + c * (d1 - 3), d1) not in (c, f, c + 1) else inr(c * 2)] if d1 > 3 and d2 > 3 else None,
                 "Difference in charge ÷ difference in days = %s ÷ %d = <b>%s</b> per extra day." % (inr(c * abs(d2 - d1)), abs(d2 - d1), inr(c))) if d1 > 3 and d2 > 3 else None
    if kind == "rect":
        w = r.randint(5, 30)
        l = w + r.randint(2, 20)
        return T("The perimeter of a rectangular garden is %d m and its length is %d m more than its width. Find the length and the width." % (2 * (l + w), l - w),
                 "length %d m, width %d m" % (l, w), ["length %d m, width %d m" % (l + 1, w - 1), "length %d m, width %d m" % (l + w - (l - w), l - w) if (l - w) != w else "length %d m, width %d m" % (l + 2, w - 2), "length %d m, width %d m" % (l + w, w)],
                 "2(%s + %s) = %d and %s − %s = %d. So %s + %s = %d, giving <b>length %d m, width %d m</b>." % (X, Y, 2 * (l + w), X, Y, l - w, X, Y, l + w, l, w))
    if kind == "notes":
        a, b = r.choice([(50, 100), (10, 20), (100, 200), (20, 50)])
        n1, n2 = r.randint(5, 30), r.randint(5, 30)
        tot = a * n1 + b * n2
        return T("%s has %d notes of ₹%d and ₹%d worth %s in all. How many ₹%d notes does %s have?" % (name, n1 + n2, a, b, inr(tot), a, he),
                 str(n1), [str(n2) if n2 != n1 else str(n1 + 2), str(n1 + 1), str(n1 - 1)],
                 "%s + %s = %d and %d%s + %d%s = %s. Solving gives <b>%d</b> notes of ₹%d." % (X, Y, n1 + n2, a, X, b, Y, num(tot), n1, a))
    p, q = r.randint(2, 9), r.randint(3, 15)
    if p >= q:
        return None
    a, b = r.choice([1, 2, 3]), r.choice([1, 2, 3])
    f1 = F(p + a, q + a)
    f2 = F(p - b, q - b)
    if p - b <= 0:
        return None
    if __import__("math").gcd(p, q) != 1:
        return None
    return T("A fraction becomes %s if %d is added to both the numerator and the denominator, and %s if %d is subtracted from both. Find the fraction." % (fv(f1), a, fv(f2), b),
             "%d/%d" % (p, q), ["%d/%d" % (q, p), "%d/%d" % (p + 1, q), "%d/%d" % (p, q + 1)],
             "Let it be %s/%s: (%s + %d)/(%s + %d) = %s and (%s − %d)/(%s − %d) = %s. Solving gives <b>%d/%d</b>." % (X, Y, X, a, Y, a, fv(f1), X, b, Y, b, fv(f2), p, q))


def main():
    seen = set()
    sets = [
        S("Solutions and graphs", mix(R, [(one_graph, 20)], seen)),
        S("Consistency of a pair of equations", mix(R, [(one_cons, 20)], seen)),
        S("Substitution method", mix(R, [(sgse.one_subst, 20)], seen)),
        S("Elimination method", mix(R, [(indian(sgse.one_add), 7), (indian(sgse.one_sub), 6), (indian(sgse.one_mult), 7)], seen)),
        S("Word problems", mix(R, [(one_word, 20)], seen)),
    ]
    body = lesson(
        "<p>A pair a₁x + b₁y + c₁ = 0, a₂x + b₂y + c₂ = 0 is shown by two lines. The solution is their point of intersection.</p>"
        "<p>a₁/a₂ ≠ b₁/b₂: one solution (intersecting). a₁/a₂ = b₁/b₂ = c₁/c₂: infinitely many (coincident). a₁/a₂ = b₁/b₂ ≠ c₁/c₂: none (parallel).</p>"
        "<p><b>Substitution</b>: make one variable the subject and put it into the other equation. <b>Elimination</b>: make the coefficients of one variable equal, then add or subtract.</p>",
        [("Solve x + y = 14, x − y = 4.", ["Add: 2x = 18, so x = 9", "Then y = 14 − 9 = 5"], "x = 9, y = 5"),
         ("Do 2x + 3y = 9 and 4x + 6y = 18 have a solution?", ["2/4 = 3/6 = 9/18 = ½"], "Infinitely many (coincident lines)")],
        ["Swapping the values of x and y at the end.",
         "Calling parallel lines “infinitely many solutions”. Parallel lines never meet: no solution.",
         "Stopping after finding x. Substitute back to find y too."])
    faq = [
        ("How do I know if a pair of linear equations has a unique solution?", "Compare the ratios: if a₁/a₂ ≠ b₁/b₂, the lines intersect at one point, so there is a unique solution."),
        ("When does a pair of linear equations have no solution?", "When a₁/a₂ = b₁/b₂ ≠ c₁/c₂. The lines are parallel and never meet. Such a pair is called inconsistent."),
        ("What is the elimination method?", "Multiply the equations so that one variable has the same coefficient, then add or subtract to remove it and solve for the other."),
        ("Which method is best: substitution or elimination?", "Use substitution when one variable already has coefficient 1; otherwise elimination is usually quicker."),
    ]
    make(10, "pair-of-linear-equations-in-two-variables", 3, "II", 3, "Pair of Linear Equations in Two Variables", "pair of linear equations",
         "Pair of linear equations in two variables and graphical method of their solution; consistency/inconsistency; algebraic conditions for number of solutions; solution by substitution and by elimination; simple situational problems (summary of the CBSE syllabus)",
         "Class 10 Pair of Linear Equations worksheet (NCERT Chapter 3): graphs, consistency, substitution, elimination and word problems in rupees. 100 questions with answers.",
         "Two lines: intersect, coincide or are parallel", "One solution, infinitely many, or none.",
         body, faq, sets, R)


if __name__ == "__main__":
    main()
