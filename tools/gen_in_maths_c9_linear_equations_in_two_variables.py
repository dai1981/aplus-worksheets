# -*- coding: utf-8 -*-
"""
India Class 9 Maths, NCERT Chapter 4: Linear Equations in Two Variables (CBSE Unit II Algebra)
  python3 tools/gen_in_maths_c9_linear_equations_in_two_variables.py
Writing equations in the form ax + by + c = 0 and reading a, b, c, x = k and y = k as equations in two variables,
checking whether a pair is a solution, finding solutions and missing values (k), points on the axes, the number of
solutions, and writing equations for situations (prices in rupees, fares, sums of numbers, savings).
Wrong answers come from real mistakes: taking c from the right-hand side without changing its sign, swapping x and y,
saying a linear equation has one solution, and writing the price relation the wrong way round.
"""
import random
from fractions import Fraction as F
from in_common import num, S, make, lesson, mix, T, expr, fv, inr, People

R = random.Random(909004)
P = People(R)
X, Y = "<i>x</i>", "<i>y</i>"


def nz(lo, hi):
    return [k for k in range(lo, hi + 1) if k]


def eq(a, b, c):
    """ax + by + c = 0"""
    return "%s = 0" % expr([(a, X), (b, Y), (c, "")])


def pt(x, y):
    return "(%s, %s)" % (fv(x), fv(y))


# ---------------------------------------------------------------- set 1: standard form
def one_std(r):
    kind = r.choice(["abc", "abc", "abc", "one"])
    if kind == "abc":
        a, b, c = r.choice(nz(-6, 7)), r.choice(nz(-6, 7)), r.choice(nz(-12, 12))
        form = r.choice(["rhs", "rhs", "swap"])
        if form == "rhs":
            e = "%s = %s" % (expr([(a, X), (b, Y)]), num(-c))
        else:
            e = "%s = %s" % (expr([(a, X)]), expr([(-b, Y), (-c, "")]))
        ans = "a = %s, b = %s, c = %s" % (num(a), num(b), num(c))
        return T("Write %s in the form a%s + b%s + c = 0. What are a, b and c?" % (e, X, Y), ans,
                 ["a = %s, b = %s, c = %s" % (num(a), num(b), num(-c)), "a = %s, b = %s, c = %s" % (num(b), num(a), num(c)), "a = %s, b = %s, c = %s" % (num(a), num(-b), num(c)) if form == "swap" else "a = %s, b = %s, c = %s" % (num(-a), num(b), num(c))],
                 "Move everything to one side: <b>%s</b>, so %s." % (eq(a, b, c), ans))
    k = r.choice(nz(-9, 9))
    t = r.choice(["x", "y"])
    if t == "x":
        ans = "1·%s + 0·%s %s %s = 0" % (X, Y, "−" if k > 0 else "+", num(abs(k)))
        w = ["0·%s + 1·%s %s %s = 0" % (X, Y, "−" if k > 0 else "+", num(abs(k))), "1·%s + 1·%s %s %s = 0" % (X, Y, "−" if k > 0 else "+", num(abs(k))), "1·%s + 0·%s %s %s = 0" % (X, Y, "+" if k > 0 else "−", num(abs(k)))]
    else:
        ans = "0·%s + 1·%s %s %s = 0" % (X, Y, "−" if k > 0 else "+", num(abs(k)))
        w = ["1·%s + 0·%s %s %s = 0" % (X, Y, "−" if k > 0 else "+", num(abs(k))), "1·%s + 1·%s %s %s = 0" % (X, Y, "−" if k > 0 else "+", num(abs(k))), "0·%s + 1·%s %s %s = 0" % (X, Y, "+" if k > 0 else "−", num(abs(k)))]
    return T("Write %s = %s as an equation in two variables." % (X if t == "x" else Y, num(k)), ans, w,
             "The other variable has coefficient 0: <b>%s</b>." % ans)


# ---------------------------------------------------------------- set 2: is it a solution?
def one_check(r):
    a, b = r.choice(nz(-5, 6)), r.choice(nz(-5, 6))
    x, y = r.choice(nz(-6, 6)), r.choice(nz(-6, 6))
    c = a * x + b * y
    e = "%s = %s" % (expr([(a, X), (b, Y)]), num(c))
    kind = r.choice(["which", "which", "yesno"])
    if kind == "which":
        if (a * y + b * x) == c and x != y:
            return None
        cands = [pt(y, x), pt(-x, y), pt(x, -y), pt(x + 1, y)]
        cands = [p for p in cands if p != pt(x, y)]
        return T("Which pair is a solution of %s?" % e, pt(x, y), cands[:3],
                 "Substitute %s = %s, %s = %s: %s(%s) %s %s(%s) = %s. <b>%s</b> works." % (X, num(x), Y, num(y), num(a), num(x), "−" if b < 0 else "+", num(abs(b)), num(y), num(c), pt(x, y)))
    t = r.choice([(x, y), (y, x), (x, -y)])
    ok = a * t[0] + b * t[1] == c
    return T("Is %s a solution of %s?" % (pt(*t), e), "Yes" if ok else "No", ["No" if ok else "Yes", "Only if %s &gt; 0" % X, "It cannot be checked without a graph"],
             "Left side = %s(%s) %s %s(%s) = %s, right side = %s, so <b>%s</b>." % (num(a), num(t[0]), "−" if b < 0 else "+", num(abs(b)), num(t[1]), num(a * t[0] + b * t[1]), num(c), "yes" if ok else "no"))


# ---------------------------------------------------------------- set 3: find a missing value
def one_find(r):
    kind = r.choice(["k", "k", "y", "x"])
    a, b = r.choice(nz(-5, 6)), r.choice(nz(-5, 6))
    x, y = r.choice(nz(-5, 6)), r.choice(nz(-5, 6))
    if kind == "k":
        k = a * x + b * y
        if k == 0:
            return None
        return T("If %s = %s, %s = %s is a solution of %s = k, find k." % (X, num(x), Y, num(y), expr([(a, X), (b, Y)])), "k = %s" % num(k),
                 ["k = %s" % num(a * y + b * x) if a * y + b * x != k else "k = %s" % num(k + 1), "k = %s" % num(-k), "k = %s" % num(a + b)] if a + b not in (k, -k) else ["k = %s" % num(-k), "k = %s" % num(k + 2), "k = %s" % num(k - 2)],
                 "Substitute: %s(%s) %s %s(%s) = <b>%s</b>." % (num(a), num(x), "−" if b < 0 else "+", num(abs(b)), num(y), num(k)))
    c = a * x + b * y
    e = "%s = %s" % (expr([(a, X), (b, Y)]), num(c))
    if kind == "y":
        return T("For the equation %s, find %s when %s = %s." % (e, Y, X, num(x)), "%s = %s" % (Y, num(y)),
                 ["%s = %s" % (Y, fv(F(c + a * x, b))) if F(c + a * x, b) != y else "%s = %s" % (Y, num(y + 1)), "%s = %s" % (Y, num(-y)), "%s = %s" % (Y, fv(F(c, b))) if F(c, b) not in (y, -y) else "%s = %s" % (Y, num(y + 2))],
                 "%s(%s) %s %s%s = %s, so %s%s = %s and <b>%s = %s</b>." % (num(a), num(x), "−" if b < 0 else "+", num(abs(b)) if abs(b) != 1 else "", Y, num(c), ("−" if b < 0 else "") + (num(abs(b)) if abs(b) != 1 else ""), Y, num(c - a * x), Y, num(y)))
    return T("For the equation %s, find %s when %s = %s." % (e, X, Y, num(y)), "%s = %s" % (X, num(x)),
             ["%s = %s" % (X, fv(F(c + b * y, a))) if F(c + b * y, a) != x else "%s = %s" % (X, num(x + 1)), "%s = %s" % (X, num(-x)), "%s = %s" % (X, fv(F(c, a))) if F(c, a) not in (x, -x) else "%s = %s" % (X, num(x + 2))],
             "%s%s + %s(%s) = %s, so %s%s = %s and <b>%s = %s</b>." % (num(a), X, num(b), num(y), num(c), num(a), X, num(c - b * y), X, num(x)))


# ---------------------------------------------------------------- set 4: solutions, axes and number of solutions
def one_sol(r):
    kind = r.choice(["count", "count", "axis", "axis", "list"])
    if kind == "count":
        a, b, c = r.choice(nz(-5, 6)), r.choice(nz(-5, 6)), r.choice(nz(-12, 12))
        return T("How many solutions does the linear equation %s have?" % eq(a, b, c), "Infinitely many", ["Only one", "Exactly two", "None"],
                 "For every value of %s there is a value of %s, so a linear equation in two variables has <b>infinitely many solutions</b>." % (X, Y))
    if kind == "axis":
        a, b = r.choice(nz(-6, 6)), r.choice(nz(-6, 6))
        m = a * b * r.choice(nz(-3, 3))
        e = "%s = %s" % (expr([(a, X), (b, Y)]), num(m))
        t = r.choice(["x", "y"])
        if t == "x":
            p = pt(F(m, a), 0)
            return T("Where does the line %s meet the x-axis?" % e, p, [pt(0, F(m, a)), pt(F(m, b), 0) if F(m, b) != F(m, a) else pt(F(m, a) + 1, 0), pt(0, F(m, b))],
                     "On the x-axis %s = 0, so %s%s = %s: <b>%s</b>." % (Y, num(a), X, num(m), p))
        p = pt(0, F(m, b))
        return T("Where does the line %s meet the y-axis?" % e, p, [pt(F(m, b), 0), pt(0, F(m, a)) if F(m, b) != F(m, a) else pt(0, F(m, b) + 1), pt(F(m, a), 0)],
                 "On the y-axis %s = 0, so %s%s = %s: <b>%s</b>." % (X, num(b), Y, num(m), p))
    a, b = r.choice(nz(-4, 5)), r.choice([1, -1, 2])
    c = r.choice(nz(-10, 10))
    xs = [0, 1, 2]
    pts = [pt(xx, F(c - a * xx, b)) for xx in xs]
    if any(F(c - a * xx, b).denominator != 1 for xx in xs):
        return None
    e = "%s = %s" % (expr([(a, X), (b, Y)]), num(c))
    return T("Which list gives three solutions of %s?" % e, ", ".join(pts),
             [", ".join(pt(F(c - a * xx, b), xx) for xx in xs), ", ".join(pt(xx, F(c + a * xx, b)) for xx in xs), ", ".join(pt(xx, F(c - a * xx, b) + 1) for xx in xs)],
             "Choose %s = 0, 1, 2 and find %s each time: <b>%s</b>." % (X, Y, ", ".join(pts)))


# ---------------------------------------------------------------- set 5: writing equations for situations
def one_word(r):
    kind = r.choice(["pen", "taxi", "sum", "fund", "age", "tickets"])
    name, he, his = P.next()
    if kind == "pen":
        k = r.choice([2, 3, 4])
        return T("The cost of a notebook is %s the cost of a pen. Taking the cost of a notebook as ₹%s and a pen as ₹%s, which equation is correct?" % ({2: "twice", 3: "three times", 4: "four times"}[k], X, Y),
                 "%s − %d%s = 0" % (X, k, Y), ["%d%s − %s = 0" % (k, X, Y), "%s + %d%s = 0" % (X, k, Y), "%s − %s = %d" % (X, Y, k)],
                 "Notebook = %d × pen: %s = %d%s, so <b>%s − %d%s = 0</b>." % (k, X, k, Y, X, k, Y))
    if kind == "taxi":
        f, c = r.choice([20, 25, 30, 40, 50]), r.choice([8, 10, 12, 15])
        d = r.randint(5, 25)
        return T("A taxi charges %s for the first km and %s for each further km. Total distance %s km, fare ₹%s. Which equation gives the fare? Then find the fare for %d km." % (inr(f), inr(c), X, Y, d),
                 "%s = %d%s + %d; %s" % (Y, c, X, f - c, inr(c * d + f - c)), ["%s = %d%s + %d; %s" % (Y, c, X, f, inr(c * d + f)), "%s = %d%s + %d; %s" % (Y, f, X, c, inr(f * d + c)), "%s = %d%s; %s" % (Y, c, X, inr(c * d))],
                 "Fare = %d + %d(%s − 1) = %d%s + %d. For %d km: %d × %d + %d = <b>%s</b>." % (f, c, X, c, X, f - c, d, c, d, f - c, inr(c * d + f - c)))
    if kind == "sum":
        s_ = r.randint(10, 60)
        return T("The sum of two numbers is %d. Which equation shows this, and which pair is one solution?" % s_, "%s + %s = %d; (%d, %d)" % (X, Y, s_, s_ - 3, 3),
                 ["%s − %s = %d; (%d, 3)" % (X, Y, s_, s_ + 3), "%s%s = %d; (%d, 1)" % (X, Y, s_, s_), "%s + %s = %d; (%d, %d)" % (X, Y, s_, s_ - 3, 4)],
                 "<b>%s + %s = %d</b>; for example %d + 3 = %d." % (X, Y, s_, s_ - 3, s_))
    if kind == "fund":
        a, b = r.choice([(100, 50), (200, 100), (500, 200), (50, 20)])
        return T("%s and %s friend together give ₹%d to a relief fund. If %s gives ₹%s and the friend ₹%s, which equation is correct?" % (name, his, a + b, name, X, Y),
                 "%s + %s = %d" % (X, Y, a + b), ["%s − %s = %d" % (X, Y, a + b), "%s = %d%s" % (X, a + b, Y), "%s + %s = %d" % (X, Y, a - b)],
                 "The two amounts add up to the total: <b>%s + %s = %d</b>. There are many possible pairs, such as (%d, %d)." % (X, Y, a + b, a, b))
    if kind == "age":
        k = r.choice([2, 3, 4])
        n = r.choice([5, 10])
        return T("%s's father is %s years old and %s is %s years old. In %d years the father will be %d times as old as %s. Which equation is correct?" % (name, X, name, Y, n, k, name),
                 "%s + %d = %d(%s + %d)" % (X, n, k, Y, n), ["%s + %d = %d%s + %d" % (X, n, k, Y, n), "%s = %d(%s + %d)" % (X, k, Y, n), "%d(%s + %d) = %s + %d" % (k, X, n, Y, n)],
                 "In %d years: father %s + %d, %s %s + %d. So <b>%s + %d = %d(%s + %d)</b>." % (n, X, n, name, Y, n, X, n, k, Y, n))
    p1, p2 = r.choice([(50, 30), (100, 60), (80, 40), (120, 75)])
    tot = p1 * r.randint(5, 20) + p2 * r.randint(5, 20)
    return T("Adult tickets cost %s and child tickets %s. A school paid %s for %s adult and %s child tickets. Which equation is correct?" % (inr(p1), inr(p2), inr(tot), X, Y),
             "%d%s + %d%s = %s" % (p1, X, p2, Y, num(tot)), ["%d%s + %d%s = %s" % (p2, X, p1, Y, num(tot)), "%s + %s = %s" % (X, Y, num(tot)), "%d%s − %d%s = %s" % (p1, X, p2, Y, num(tot))],
             "Cost = price × number for each kind: <b>%d%s + %d%s = %s</b>." % (p1, X, p2, Y, num(tot)))


def main():
    seen = set()
    sets = [
        S("The form ax + by + c = 0", mix(R, [(one_std, 20)], seen)),
        S("Is it a solution?", mix(R, [(one_check, 20)], seen)),
        S("Finding missing values", mix(R, [(one_find, 20)], seen)),
        S("Solutions and the axes", mix(R, [(one_sol, 20)], seen)),
        S("Writing equations for situations", mix(R, [(one_word, 20)], seen)),
    ]
    body = lesson(
        "<p>A <b>linear equation in two variables</b> can be written as a%s + b%s + c = 0, where a and b are not both 0.</p>"
        "<p>A <b>solution</b> is a pair (%s, %s) that makes the equation true. A linear equation in two variables has <b>infinitely many</b> solutions: choose any %s and work out %s.</p>"
        "<p>On the x-axis y = 0; on the y-axis x = 0. Even x = 3 is an equation in two variables: 1·x + 0·y − 3 = 0.</p>" % (X, Y, X, Y, X, Y),
        [("Write 2x = −5y in the form ax + by + c = 0.", ["2x + 5y = 0"], "a = 2, b = 5, c = 0"),
         ("Find k if x = 2, y = 1 is a solution of 2x + 3y = k.", ["2(2) + 3(1)"], "k = 7")],
        ["Keeping the sign of c when moving it from the right-hand side. Its sign changes.",
         "Swapping x and y when checking a pair (x, y).",
         "Saying a linear equation in two variables has one solution. It has infinitely many."])
    faq = [
        ("What is a linear equation in two variables?", "An equation that can be written as ax + by + c = 0, where a, b, c are real numbers and a and b are not both zero."),
        ("How many solutions does a linear equation in two variables have?", "Infinitely many. Every point on its straight-line graph is a solution."),
        ("How do I check whether a pair is a solution?", "Substitute the values of x and y. If both sides are equal, the pair is a solution."),
        ("How do I write x = 4 as an equation in two variables?", "1·x + 0·y − 4 = 0, so a = 1, b = 0 and c = −4."),
    ]
    make(9, "linear-equations-in-two-variables", 4, "II", 4, "Linear Equations in Two Variables", "linear equations in two variables",
         "Introduction to the equation in two variables; focus on understanding that a linear equation in two variables has infinitely many solutions and justifying their being written as ordered pairs of real numbers (summary of the CBSE syllabus)",
         "Class 9 Linear Equations in Two Variables worksheet (NCERT Chapter 4): ax + by + c = 0, checking solutions, finding values, points on the axes and writing equations for situations. 100 questions with answers.",
         "ax + by + c = 0 has infinitely many solutions", "Each solution is an ordered pair (x, y).",
         body, faq, sets, R)


if __name__ == "__main__":
    main()
