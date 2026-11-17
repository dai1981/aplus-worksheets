# -*- coding: utf-8 -*-
"""
UK Year 7 Maths: Solving Equations (KS3 Algebra)
  python3 tools/gen_uk_maths_y7_solving_equations.py
One-step and two-step linear equations, equations with brackets, forming equations, and word problems.
Wrong answers come from real mistakes: using the same operation instead of the inverse, dividing before
undoing the addition, and sign slips with negative numbers.
"""
import random
from fractions import Fraction as F
from uk_ks3 import num, par, mcq, B, S, make, lesson, collect, QN, T, fr, expr, People, MINUS

R = random.Random(71301)
P = People(R)
X = "<i>x</i>"
LET = ["<i>x</i>", "<i>n</i>", "<i>a</i>", "<i>y</i>", "<i>m</i>", "<i>p</i>"]


def sol(x):
    return num(x) if F(x).denominator == 1 else (MINUS if x < 0 else "") + fr(abs(F(x).numerator), F(x).denominator)


def QS(q, ans, wrongs, e, var):
    ans = F(ans)
    cands = []
    for w in list(wrongs) + [ans + 1, ans - 1, -ans]:
        if w is None:
            continue
        w = F(w)
        if w != ans and w.denominator <= 12:
            cands.append(("%s = %s" % (var, sol(w)), w))
    return mcq(q, ("%s = %s" % (var, sol(ans)), ans), cands, e)


# ------------------------------------------------------------ set 1: one step
def one_step(r):
    x = r.choice(LET)
    s = r.randint(-9, 15)
    if s == 0:
        return None
    k = r.randint(2, 12)
    kind = r.randint(0, 3)
    if kind == 0:
        c = s + k
        q = "Solve %s." % B("%s + %d = %s" % (x, k, num(c)))
        e = "Subtract %d from both sides: %s = %s − %d = <b>%s</b>." % (k, x, num(c), k, num(s))
        return QS(q, s, [c + k, F(c, k) if c % k == 0 else None], e, x)
    if kind == 1:
        c = s - k
        q = "Solve %s." % B("%s − %d = %s" % (x, k, num(c)))
        e = "Add %d to both sides: %s = %s + %d = <b>%s</b>." % (k, x, num(c), k, num(s))
        return QS(q, s, [c - k, -c - k], e, x)
    if kind == 2:
        c = s * k
        q = "Solve %s." % B("%d%s = %s" % (k, x, num(c)))
        e = "Divide both sides by %d: %s = %s ÷ %d = <b>%s</b>." % (k, x, num(c), k, num(s))
        return QS(q, s, [c - k, c * k if abs(c * k) < 200 else None, c + k], e, x)
    c = s
    q = "Solve %s." % B("%s = %s" % (fr(x, k), num(c)))
    e = "Multiply both sides by %d: %s = %s × %d = <b>%s</b>." % (k, x, num(c), k, num(s * k))
    return QS(q, s * k, [F(s, k), s + k, s - k], e, x)


# ------------------------------------------------------------ set 2: two step
def two_step(r):
    x = r.choice(LET)
    s = r.randint(-6, 12)
    a = r.randint(2, 9)
    b = r.randint(1, 15)
    kind = r.randint(0, 2)
    if kind == 0:
        c = a * s + b
        q = "Solve %s." % B("%d%s + %d = %s" % (a, x, b, num(c)))
        e = "Subtract %d: %d%s = %s. Divide by %d: <b>%s = %s</b>." % (b, a, x, num(c - b), a, x, num(s))
        return QS(q, s, [F(c + b, a), F(c, a) - b, c - b, F(c - b, a) + 2], e, x)
    if kind == 1:
        c = a * s - b
        q = "Solve %s." % B("%d%s − %d = %s" % (a, x, b, num(c)))
        e = "Add %d: %d%s = %s. Divide by %d: <b>%s = %s</b>." % (b, a, x, num(c + b), a, x, num(s))
        return QS(q, s, [F(c - b, a), F(c, a) + b, c + b], e, x)
    c = s + b
    q = "Solve %s." % B("%s + %d = %s" % (fr(x, a), b, num(c)))
    e = "Subtract %d: %s = %s. Multiply by %d: <b>%s = %s</b>." % (b, fr(x, a), num(s), a, x, num(s * a))
    return QS(q, s * a, [F(s, a), c * a - b, (c + b) * a], e, x)


# ------------------------------------------------------------ set 3: brackets and harder answers
def brackets(r):
    x = r.choice(LET)
    kind = r.randint(0, 3)
    if kind == 0:
        a, b, s = r.randint(2, 6), r.randint(-6, 8), r.randint(-5, 9)
        if b == 0:
            return None
        c = a * (s + b)
        q = "Solve %s." % B("%d(%s) = %s" % (a, expr([(1, x), (b, "")]), num(c)))
        e = "Divide by %d: %s = %s. Then %s: <b>%s = %s</b>." % (
            a, expr([(1, x), (b, "")]), num(c // a), "subtract %d" % b if b > 0 else "add %d" % -b, x, num(s))
        return QS(q, s, [c - b, F(c - b, a), F(c, a) + b], e, x)
    if kind == 1:
        a, b = r.randint(2, 9), r.randint(1, 12)
        c = r.randint(1, 30)
        s = F(c - b, a)
        if s.denominator == 1 or s.denominator > 5:
            return None
        q = "Solve %s." % B("%d%s + %d = %d" % (a, x, b, c))
        e = "Subtract %d: %d%s = %d. Divide by %d: <b>%s = %s</b>. The answer can be a fraction." % (b, a, x, c - b, a, x, sol(s))
        return QS(q, s, [F(c + b, a), F(a, c - b) if c != b else None, c - b - a], e, x)
    if kind == 2:
        a, b, s = r.randint(2, 7), r.randint(1, 20), r.randint(1, 9)
        c = b - a * s
        q = "Solve %s." % B("%d − %d%s = %s" % (b, a, x, num(c)))
        e = "Subtract %d from both sides: %s%d%s = %s. Divide by %s%d: <b>%s = %d</b>." % (b, MINUS, a, x, num(c - b), MINUS, a, x, s)
        return QS(q, s, [-s, F(c - b, a) if F(c - b, a) != s else None, F(b + c, a)], e, x)
    a, b, s = r.randint(2, 5), r.randint(1, 9), r.randint(2, 9)
    c = (s + b) * a
    q = "Solve %s." % B("%s = %d" % (fr(expr([(1, x), (b, "")]), a), c // a if False else (s + b)))
    e = "Multiply by %d: %s = %d. Subtract %d: <b>%s = %d</b>." % (a, expr([(1, x), (b, "")]), c, b, x, c - b)
    return QS(q, c - b, [s, s + b - b * a, F(s + b, a) - b], e, x)


# ------------------------------------------------------------ set 4: forming equations
def forming():
    its = []
    for k, add, res in [(3, 7, 22), (5, 4, 39), (4, 9, 37), (6, 2, 44), (2, 15, 31)]:
        n = F(res - add, k)
        q = "I think of a number, multiply it by %d and add %d. The answer is %d. What is my number?" % (k, add, res)
        e = "%d%s + %d = %d, so %d%s = %d and %s = <b>%s</b>." % (k, "<i>n</i>", add, res, k, "<i>n</i>", res - add, "<i>n</i>", num(n))
        its.append(QN(q, n, [F(res + add, k), F(res, k) - add if F(res, k) - add > 0 else None, res - add], e))
    for k, sub, res in [(4, 3, 25), (7, 5, 30), (3, 8, 13)]:
        n = F(res + sub, k)
        q = "I think of a number, multiply it by %d and subtract %d. The answer is %d. What is my number?" % (k, sub, res)
        e = "%d<i>n</i> − %d = %d, so %d<i>n</i> = %d and <i>n</i> = <b>%s</b>." % (k, sub, res, k, res + sub, num(n))
        its.append(QN(q, n, [F(res - sub, k) if F(res - sub, k) > 0 else None, res + sub, F(res, k) + sub], e))
    for side_expr, per, s in [((2, 3), 34, None), ((3, 1), 50, None)]:
        pass
    data = [
        ("The perimeter of a rectangle with sides <i>x</i> + 2 and <i>x</i> is 28 cm. Which equation is correct?", "4<i>x</i> + 4 = 28",
         ["2<i>x</i> + 2 = 28", "<i>x</i>(<i>x</i> + 2) = 28", "4<i>x</i> + 2 = 28"], "Perimeter = 2(<i>x</i> + 2) + 2<i>x</i> = 4<i>x</i> + 4, so <b>4<i>x</i> + 4 = 28</b> (and <i>x</i> = 6)."),
        ("The angles in a triangle are <i>x</i>, 2<i>x</i> and 60°. Which equation is correct?", "3<i>x</i> + 60 = 180",
         ["3<i>x</i> + 60 = 360", "2<i>x</i> + 60 = 180", "3<i>x</i> = 60"], "Angles in a triangle add up to 180°: <b>3<i>x</i> + 60 = 180</b>, so <i>x</i> = 40°."),
        ("Ben is <i>b</i> years old. His sister is 4 years older. Together their ages add up to 30. Which equation is correct?", "2<i>b</i> + 4 = 30",
         ["<i>b</i> + 4 = 30", "4<i>b</i> = 30", "2<i>b</i> − 4 = 30"], "<i>b</i> + (<i>b</i> + 4) = 30, so <b>2<i>b</i> + 4 = 30</b> and Ben is 13."),
        ("Pens cost <i>p</i> pence each. 6 pens and a 50p ruler cost £2.90. Which equation is correct?", "6<i>p</i> + 50 = 290",
         ["6<i>p</i> + 50 = 2.90", "6(<i>p</i> + 50) = 290", "<i>p</i> + 56 = 290"], "Work in pence: <b>6<i>p</i> + 50 = 290</b>, so <i>p</i> = 40."),
    ]
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    for q, ans, wr, e in [
        ("The angles on a straight line are 3<i>x</i> and 2<i>x</i> + 30°. Find <i>x</i>.", 30, [42, 70, 36], "3<i>x</i> + 2<i>x</i> + 30 = 180, so 5<i>x</i> = 150 and <i>x</i> = <b>30</b>."),
        ("A square has sides of (2<i>x</i> + 1) cm. Its perimeter is 44 cm. Find <i>x</i>.", 5, [F(43, 2), 11, F(11, 2)], "4(2<i>x</i> + 1) = 44, so 2<i>x</i> + 1 = 11 and <i>x</i> = <b>5</b>."),
        ("A taxi costs £3 plus £2 per mile. A journey cost £19. How many miles was it?", 8, [11, F(19, 5), 16], "3 + 2<i>m</i> = 19, so 2<i>m</i> = 16 and <i>m</i> = <b>8</b>."),
        ("Three consecutive whole numbers add up to 72. What is the smallest?", 23, [24, 21, 22], "<i>n</i> + (<i>n</i> + 1) + (<i>n</i> + 2) = 72, so 3<i>n</i> + 3 = 72 and <i>n</i> = <b>23</b>."),
        ("Amelia has 3 times as many stickers as Leo. Together they have 64. How many does Leo have?", 16, [48, F(64, 3), 21], "<i>s</i> + 3<i>s</i> = 64, so 4<i>s</i> = 64 and <i>s</i> = <b>16</b>."),
        ("The mean of 7, 11 and <i>x</i> is 10. Find <i>x</i>.", 12, [10, 30, 8], "(7 + 11 + <i>x</i>) ÷ 3 = 10, so 18 + <i>x</i> = 30 and <i>x</i> = <b>12</b>."),
        ("A gym charges a £20 joining fee and £15 a month. Kai has paid £125 so far. For how many months has he been a member?", 7, [F(29, 3), 9, 8], "20 + 15<i>m</i> = 125, so 15<i>m</i> = 105 and <i>m</i> = <b>7</b>."),
        ("An isosceles triangle has a top angle of 40°. Each base angle is <i>x</i>. Find <i>x</i>.", 70, [140, 50, 40], "2<i>x</i> + 40 = 180, so 2<i>x</i> = 140 and <i>x</i> = <b>70°</b>."),
    ]:
        its.append(QN(q, ans, [w for w in wr if F(w).denominator == 1] or [ans + 2], e))
    return its


def body():
    return lesson(
        "<p>An equation is like a balance. Whatever you do to one side, do to the other. Use <b>inverse operations</b> "
        "to get the letter on its own: + and − undo each other, × and ÷ undo each other.</p>"
        "<p>For a two-step equation, undo the + or − first, then the × or ÷.</p>",
        [("Solve 4<i>x</i> + 7 = 31.", ["Subtract 7: 4<i>x</i> = 24.", "Divide by 4: <i>x</i> = 6."], "<i>x</i> = 6"),
         ("Solve 3(<i>x</i> − 2) = 21.", ["Divide by 3: <i>x</i> − 2 = 7.", "Add 2: <i>x</i> = 9."], "<i>x</i> = 9"),
         ("Solve <i>n</i>/5 − 3 = 4.", ["Add 3: <i>n</i>/5 = 7.", "Multiply by 5: <i>n</i> = 35."], "<i>n</i> = 35")],
        ["Doing the same operation instead of the inverse: for <i>x</i> + 7 = 20, <i>x</i> = 13, not 27.",
         "Dividing before subtracting: for 4<i>x</i> + 7 = 31, do 31 − 7 first, then ÷ 4.",
         "Forgetting that the answer can be negative or a fraction: 4<i>x</i> = 6 gives <i>x</i> = 3/2.",
         "Not checking: put your answer back into the equation to see if it works."])


def main():
    sets = [S("One-step equations", collect(one_step, 20, R)),
            S("Two-step equations", collect(two_step, 20, R)),
            S("Brackets, fractions and negatives", collect(brackets, 20, R)),
            S("Forming and solving equations", forming()[:12] + forming()[12:20]),
            S("Mixed equations", collect(one_step, 6, random.Random(5)) + collect(two_step, 7, random.Random(6)) + collect(brackets, 7, random.Random(7)))]
    # set 4 holds forming problems; set 5 is a mixed review of new equations (different seeds give new numbers)
    sets[3], sets[4] = sets[4], sets[3]
    sets[3]["title"], sets[4]["title"] = "Mixed practice", "Forming and solving equations"
    make(7, "solving-equations", 13, "A",
         "Solving Equations: One-Step, Two-Step and Brackets",
         "Year 7 Solving Equations Worksheets: One-Step, Two-Step, Brackets and Forming Equations",
         "Solving equations",
         "Use algebraic methods to solve linear equations in one variable (including all forms that require rearrangement); "
         "recognise and use relationships between operations including inverse operations.",
         "Free Year 7 solving equations worksheets: one-step and two-step equations, equations with brackets, negative "
         "and fraction answers, and forming equations from word problems. 100 questions with step-by-step answers.",
         "Do the same to both sides. Undo + and − first, then × and ÷.",
         "Check your answer by putting it back into the equation.",
         body(),
         [("How do you solve a two-step equation?", "Undo the addition or subtraction first, then the multiplication or division. For 4x + 7 = 31: 4x = 24, so x = 6."),
          ("How do I solve an equation with a bracket?", "Either divide both sides by the number outside the bracket, or expand the bracket first. 3(x − 2) = 21 gives x − 2 = 7, so x = 9."),
          ("Can the answer be a fraction or negative?", "Yes. 4x = 6 gives x = 3/2, and x + 9 = 4 gives x = −5."),
          ("How do I check my answer?", "Substitute it back. If x = 6 in 4x + 7, then 24 + 7 = 31, so it is correct.")],
         sets, R)


if __name__ == "__main__":
    main()
