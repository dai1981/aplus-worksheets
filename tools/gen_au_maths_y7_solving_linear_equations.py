# -*- coding: utf-8 -*-
"""
AU Year 7 Maths: Solving linear equations (Australian Curriculum v9.0: AC9M7A03)
  python3 tools/gen_au_maths_y7_solving_linear_equations.py
One-step and two-step linear equations with natural number solutions, equations with brackets and fractions,
verifying a solution by substitution, and forming and solving equations from problems.
Wrong answers come from real mistakes: using the same operation instead of the inverse, dividing before
undoing the addition or subtraction, and dividing the wrong way round.
"""
import random
from fractions import Fraction as F
from au_hs import num, mcq, B, S, make, lesson, collect, QN, T, fr, expr

R = random.Random(71201)
LET = ["<i>x</i>", "<i>n</i>", "<i>a</i>", "<i>y</i>", "<i>m</i>", "<i>p</i>", "<i>k</i>"]


def QS(q, ans, wrongs, e, var):
    ans = F(ans)
    cands = []
    for w in list(wrongs) + [ans + 1, ans - 1, ans + 2]:
        if w is None:
            continue
        w = F(w)
        if w != ans and w.denominator == 1 and w > 0:
            cands.append(("%s = %s" % (var, num(w)), w))
    return mcq(q, ("%s = %s" % (var, num(ans)), ans), cands, e)


# ------------------------------------------------------------ set 1: one step
def one_step(r):
    x = r.choice(LET)
    s = r.randint(1, 20)
    k = r.randint(2, 12)
    kind = r.randint(0, 3)
    if kind == 0:
        c = s + k
        e = "Subtract %d from both sides: %s = %d − %d = <b>%d</b>." % (k, x, c, k, s)
        return QS("Solve %s." % B("%s + %d = %d" % (x, k, c)), s, [c + k, F(c, k)], e, x)
    if kind == 1:
        c = s + k
        e = "Add %d to both sides: %s = %d + %d = <b>%d</b>." % (k, x, s, k, c)
        return QS("Solve %s." % B("%s − %d = %d" % (x, k, s)), c, [s - k if s > k else s + 2 * k + 1, k - s if k > s else c + k], e, x)
    if kind == 2:
        c = s * k
        e = "Divide both sides by %d: %s = %d ÷ %d = <b>%d</b>." % (k, x, c, k, s)
        return QS("Solve %s." % B("%d%s = %d" % (k, x, c)), s, [c - k, c * k if c * k < 400 else None, c + k], e, x)
    e = "Multiply both sides by %d: %s = %d × %d = <b>%d</b>." % (k, x, s, k, s * k)
    return QS("Solve %s." % B("%s = %d" % (fr(x, k), s)), s * k, [F(s, k), s + k, abs(s - k)], e, x)


# ------------------------------------------------------------ set 2: two step
def two_step(r):
    x = r.choice(LET)
    s = r.randint(1, 15)
    a = r.randint(2, 9)
    b = r.randint(1, 20)
    kind = r.randint(0, 2)
    if kind == 0:
        c = a * s + b
        e = "Subtract %d: %d%s = %d. Divide by %d: <b>%s = %d</b>." % (b, a, x, c - b, a, x, s)
        return QS("Solve %s." % B("%d%s + %d = %d" % (a, x, b, c)), s, [F(c + b, a), F(c, a) - b, c - b], e, x)
    if kind == 1:
        c = a * s - b
        if c <= 0:
            return None
        e = "Add %d: %d%s = %d. Divide by %d: <b>%s = %d</b>." % (b, a, x, c + b, a, x, s)
        return QS("Solve %s." % B("%d%s − %d = %d" % (a, x, b, c)), s, [F(c - b, a), F(c, a) + b, c + b], e, x)
    c = s + b
    e = "Subtract %d: %s = %d. Multiply by %d: <b>%s = %d</b>." % (b, fr(x, a), s, a, x, s * a)
    return QS("Solve %s." % B("%s + %d = %d" % (fr(x, a), b, c)), s * a, [F(s, a), c * a - b, (c + b) * a], e, x)


# ------------------------------------------------------------ set 3: brackets and fractions
def brackets(r):
    x = r.choice(LET)
    kind = r.randint(0, 2)
    if kind == 0:
        a, b, s = r.randint(2, 6), r.randint(-6, 8), r.randint(1, 12)
        if b == 0 or s + b <= 0:
            return None
        c = a * (s + b)
        e = "Divide by %d: %s = %d. Then %s: <b>%s = %d</b>." % (
            a, expr([(1, x), (b, "")]), c // a, "subtract %d" % b if b > 0 else "add %d" % -b, x, s)
        return QS("Solve %s." % B("%d(%s) = %d" % (a, expr([(1, x), (b, "")]), c)), s, [c - b, F(c - b, a), F(c, a) + b], e, x)
    if kind == 1:
        a, b, s = r.randint(2, 5), r.randint(1, 9), r.randint(1, 12)
        c = (s + b) * a
        e = "Multiply by %d: %s + %d = %d. Subtract %d: <b>%s = %d</b>." % (a, x, b, c, b, x, c - b)
        return QS("Solve %s." % B("%s = %d" % (fr("%s + %d" % (x, b), a), s + b)), c - b, [s, s + b - b * a, s * a], e, x)
    a, b, s = r.randint(2, 6), r.randint(10, 40), r.randint(1, 9)
    c = b - a * s
    if c <= 0:
        return None
    e = "Add %d%s to both sides: %d = %d + %d%s. Subtract %d: %d%s = %d. Divide by %d: <b>%s = %d</b>." % (
        a, x, b, c, a, x, c, a, x, b - c, a, x, s)
    return QS("Solve %s." % B("%d − %d%s = %d" % (b, a, x, c)), s, [F(b + c, a), F(c, a) if c % a == 0 else b - c, b - c], e, x)


# ------------------------------------------------------------ set 4: checking a solution
def check(r):
    x = r.choice(LET)
    a, b, s = r.randint(2, 9), r.randint(1, 15), r.randint(1, 12)
    kind = r.randint(0, 1)
    if kind == 0:
        c = a * s + b
        q = "Which value is the solution of %s?" % B("%d%s + %d = %d" % (a, x, b, c))
        wr = [s + 1, s - 1 if s > 1 else s + 2, F(c - b, a) + 2, F(c, a) if F(c, a).denominator == 1 else s + 3]
        e = "Check by substituting: %d × %d + %d = %d + %d = %d. ✓ So <b>%s = %d</b>." % (a, s, b, a * s, b, c, x, s)
        return QS(q, s, wr, e, x)
    test = s + r.choice([0, 0, 1, -1, 2])
    if test <= 0:
        return None
    c = a * s + b
    lhs = a * test + b
    ok = lhs == c
    q = "Is %s a solution of %s?" % (B("%s = %d" % (x, test)), B("%d%s + %d = %d" % (a, x, b, c)))
    right = "Yes, because %d × %d + %d = %d" % (a, test, b, c) if ok else "No, because %d × %d + %d = %d, not %d" % (a, test, b, lhs, c)
    wr = ["No, because %d × %d + %d = %d" % (a, test, b, lhs + 1) if ok else "Yes, because %d × %d + %d = %d" % (a, test, b, c),
          "Yes, because %d + %d + %d = %d" % (a, test, b, a + test + b) if a + test + b != lhs else "Yes, because it is a whole number",
          "You cannot tell without solving it first"]
    e = "Substitute %s = %d: %d × %d + %d = %d. %s" % (x, test, a, test, b, lhs, "This equals %d, so <b>yes</b>." % c if ok else "This is not %d, so <b>no</b>." % c)
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 5: forming and solving
def forming():
    its = []
    for k, add, res in [(4, 6, 34), (6, 5, 47), (3, 11, 41), (7, 2, 58)]:
        n = F(res - add, k)
        q = "I think of a number, multiply it by %d and add %d. The answer is %d. What is my number?" % (k, add, res)
        e = "%d<i>n</i> + %d = %d, so %d<i>n</i> = %d and <i>n</i> = <b>%s</b>." % (k, add, res, k, res - add, num(n))
        its.append(QN(q, n, [F(res + add, k), F(res, k) - add if F(res, k) - add > 0 else None, res - add], e))
    for k, sub, res in [(5, 4, 31), (8, 3, 37)]:
        n = F(res + sub, k)
        q = "I think of a number, multiply it by %d and subtract %d. The answer is %d. What is my number?" % (k, sub, res)
        e = "%d<i>n</i> − %d = %d, so %d<i>n</i> = %d and <i>n</i> = <b>%s</b>." % (k, sub, res, k, res + sub, num(n))
        its.append(QN(q, n, [F(res - sub, k) if F(res - sub, k) > 0 else None, res + sub, F(res, k) + sub], e))
    data = [
        ("The perimeter of a rectangle with sides <i>x</i> + 3 and <i>x</i> is 30 cm. Which equation is correct?", "4<i>x</i> + 6 = 30",
         ["2<i>x</i> + 3 = 30", "<i>x</i>(<i>x</i> + 3) = 30", "4<i>x</i> + 3 = 30"], "Perimeter = 2(<i>x</i> + 3) + 2<i>x</i> = 4<i>x</i> + 6, so <b>4<i>x</i> + 6 = 30</b> (and <i>x</i> = 6)."),
        ("The angles in a triangle are <i>x</i>, 3<i>x</i> and 80°. Which equation is correct?", "4<i>x</i> + 80 = 180",
         ["4<i>x</i> + 80 = 360", "3<i>x</i> + 80 = 180", "4<i>x</i> = 80"], "Angles in a triangle add up to 180°: <b>4<i>x</i> + 80 = 180</b>, so <i>x</i> = 25°."),
        ("Cooper is <i>c</i> years old. His sister is 5 years older. Their ages add up to 31. Which equation is correct?", "2<i>c</i> + 5 = 31",
         ["<i>c</i> + 5 = 31", "5<i>c</i> = 31", "2<i>c</i> − 5 = 31"], "<i>c</i> + (<i>c</i> + 5) = 31, so <b>2<i>c</i> + 5 = 31</b> and Cooper is 13."),
        ("Muesli bars cost <i>m</i> cents each. 6 bars and a 90c drink cost $3.90. Which equation is correct?", "6<i>m</i> + 90 = 390",
         ["6<i>m</i> + 90 = 3.90", "6(<i>m</i> + 90) = 390", "<i>m</i> + 96 = 390"], "Work in cents: <b>6<i>m</i> + 90 = 390</b>, so <i>m</i> = 50."),
    ]
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    for q, ans, wr, e in [
        ("The angles on a straight line are 4<i>x</i> and 2<i>x</i> + 60°. Find <i>x</i>.", 20, [40, 30, 10], "4<i>x</i> + 2<i>x</i> + 60 = 180, so 6<i>x</i> = 120 and <i>x</i> = <b>20</b>."),
        ("A square has sides of (2<i>x</i> + 3) cm. Its perimeter is 52 cm. Find <i>x</i>.", 5, [13, 10, 8], "4(2<i>x</i> + 3) = 52, so 2<i>x</i> + 3 = 13 and <i>x</i> = <b>5</b>."),
        ("A taxi charges $4 plus $2 per km. A trip cost $26. How many kilometres was it?", 11, [15, 13, 22], "4 + 2<i>d</i> = 26, so 2<i>d</i> = 22 and <i>d</i> = <b>11</b>."),
        ("Three consecutive whole numbers add up to 81. What is the smallest?", 26, [27, 24, 25], "<i>n</i> + (<i>n</i> + 1) + (<i>n</i> + 2) = 81, so 3<i>n</i> + 3 = 81 and <i>n</i> = <b>26</b>."),
        ("Isla has 4 times as many stickers as Noah. Together they have 85. How many does Noah have?", 17, [68, 21, 81], "<i>s</i> + 4<i>s</i> = 85, so 5<i>s</i> = 85 and <i>s</i> = <b>17</b>."),
        ("The mean of 9, 14 and <i>x</i> is 12. Find <i>x</i>.", 13, [12, 36, 11], "(9 + 14 + <i>x</i>) ÷ 3 = 12, so 23 + <i>x</i> = 36 and <i>x</i> = <b>13</b>."),
        ("A gym charges a $40 joining fee and $25 a week. Matilda has paid $315. For how many weeks has she been a member?", 11, [14, 13, 12], "40 + 25<i>w</i> = 315, so 25<i>w</i> = 275 and <i>w</i> = <b>11</b>."),
        ("A school orders 12 boxes of pencils and 5 loose pencils. There are 245 pencils in total. How many pencils are in a box?", 20, [25, 21, 240], "12<i>b</i> + 5 = 245, so 12<i>b</i> = 240 and <i>b</i> = <b>20</b>."),
        ("Ruby buys 3 drinks at $<i>d</i> each and pays with a $20 note. She gets $8.75 change. Which equation is correct?", 0, [], ""),
        ("An isosceles triangle has a top angle of 50°. Each base angle is <i>x</i>. Find <i>x</i>.", 65, [130, 50, 75], "2<i>x</i> + 50 = 180, so 2<i>x</i> = 130 and <i>x</i> = <b>65°</b>."),
    ]:
        if not e:
            continue
        its.append(QN(q, ans, wr, e))
    its.append(T("Ruby buys 3 drinks at $<i>d</i> each and pays with a $20 note. She gets $8.75 change. Which equation is correct?",
                 "20 − 3<i>d</i> = 8.75", ["3<i>d</i> − 20 = 8.75", "20 − <i>d</i> = 8.75", "3(20 − <i>d</i>) = 8.75"],
                 "She spends 3<i>d</i>, so the change is 20 − 3<i>d</i>: <b>20 − 3<i>d</i> = 8.75</b> (each drink costs $3.75)."))
    return its


def body():
    return lesson(
        "<p>An equation is like a balance: whatever you do to one side, do to the other. Use <b>inverse operations</b> "
        "to get the variable on its own: + and − undo each other, × and ÷ undo each other.</p>"
        "<p>For a two-step equation, undo the + or − first, then the × or ÷. "
        "<b>Verify</b> the solution by substituting it back into the equation.</p>",
        [("Solve 4<i>x</i> + 7 = 31.", ["Subtract 7: 4<i>x</i> = 24.", "Divide by 4: <i>x</i> = 6.", "Check: 4 × 6 + 7 = 31. ✓"], "<i>x</i> = 6"),
         ("Solve 3(<i>x</i> − 2) = 21.", ["Divide by 3: <i>x</i> − 2 = 7.", "Add 2: <i>x</i> = 9."], "<i>x</i> = 9"),
         ("Solve <i>n</i>/5 + 3 = 10.", ["Subtract 3: <i>n</i>/5 = 7.", "Multiply by 5: <i>n</i> = 35."], "<i>n</i> = 35")],
        ["Doing the same operation instead of the inverse: for <i>x</i> + 7 = 20, <i>x</i> = 13, not 27.",
         "Dividing before subtracting: for 4<i>x</i> + 7 = 31, do 31 − 7 first, then ÷ 4.",
         "Dividing the wrong way round: 6<i>x</i> = 30 gives <i>x</i> = 30 ÷ 6 = 5.",
         "Not checking: put your answer back into the equation to see if it works."])


def main():
    sets = [S("One-step equations", collect(one_step, 20, R)),
            S("Two-step equations", collect(two_step, 20, R)),
            S("Equations with brackets and fractions", collect(brackets, 20, R)),
            S("Checking a solution", collect(check, 20, R)),
            S("Forming and solving equations", forming())]
    make(7, "solving-linear-equations", 12, "AC9M7A03",
         "Solving Linear Equations: One-Step, Two-Step and Checking Solutions",
         "Year 7 Solving Equations Worksheets: One-Step, Two-Step, Brackets and Word Problems (Free, Answer Key)",
         "Solving linear equations",
         "solve one-variable linear equations with natural number solutions; verify the solution by substitution",
         "Free Year 7 maths worksheets on solving linear equations for the Australian Curriculum (AC9M7A03): one-step and "
         "two-step equations, brackets, checking solutions by substitution, and forming equations from problems. 100 questions with an answer key.",
         "Do the same to both sides. Undo + and − first, then × and ÷.",
         "Check your answer by substituting it back into the equation.",
         body(),
         [("How do you solve a two-step equation?", "Undo the addition or subtraction first, then the multiplication or division. For 4x + 7 = 31: 4x = 24, so x = 6."),
          ("How do I solve an equation with a bracket?", "Divide both sides by the number outside the bracket, or expand it first. 3(x − 2) = 21 gives x − 2 = 7, so x = 9."),
          ("How do I verify a solution?", "Substitute it back into the equation. If x = 6 in 4x + 7, then 24 + 7 = 31, so it is correct."),
          ("How do I turn a word problem into an equation?", "Choose a letter for the unknown, write each part of the story as an expression, then set it equal to the total.")],
         sets, R)


if __name__ == "__main__":
    main()
