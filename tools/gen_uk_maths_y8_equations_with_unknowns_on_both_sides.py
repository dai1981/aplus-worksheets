# -*- coding: utf-8 -*-
"""
UK Year 8 Maths: Equations with Unknowns on Both Sides (KS3 Algebra)
  python3 tools/gen_uk_maths_y8_equations_with_unknowns_on_both_sides.py
Solving ax + b = cx + d, with negatives, with brackets on both sides, with fractions, and forming
equations from problems. Wrong answers come from real mistakes: moving a term without changing its sign,
adding the x terms instead of subtracting, expanding only the first term, and dividing the wrong way.
"""
import random
from fractions import Fraction as F
from uk_ks3 import num, par, mcq, B, S, make, lesson, collect, T, fr, expr, MINUS

R = random.Random(80401)
LET = ["<i>x</i>", "<i>n</i>", "<i>a</i>", "<i>y</i>", "<i>m</i>", "<i>p</i>"]


def sol(v):
    v = F(v)
    return num(v) if v.denominator == 1 else (MINUS if v < 0 else "") + fr(abs(v.numerator), v.denominator)


def QS(q, ans, wrongs, e, var):
    ans = F(ans)
    cands = []
    for w in list(wrongs) + [ans + 1, ans - 1, -ans, ans + 2]:
        if w is None:
            continue
        w = F(w)
        if w != ans and w.denominator <= 12 and abs(w) < 200:
            cands.append(("%s = %s" % (var, sol(w)), w))
    return mcq(q, ("%s = %s" % (var, sol(ans)), ans), cands, e)


def side(a, b, v):
    return expr([(a, v), (b, "")])


# ------------------------------------------------------------ set 1: ax + b = cx + d
def one_basic(r):
    v = r.choice(LET)
    s = r.randint(1, 12)
    c = r.randint(1, 6)
    a = c + r.randint(1, 6)
    b = r.randint(-10, 15)
    d = (a - c) * s + b
    if b == d or b == 0:
        return None
    q = "Solve %s." % B("%s = %s" % (side(a, b, v), side(c, d, v)))
    e = "Subtract %s from both sides: %s = %s. %s: %s = %s." % (
        side(c, 0, v), side(a - c, b, v), num(d), "Subtract %d" % b if b > 0 else "Add %d" % -b, side(a - c, 0, v), num(d - b))
    e += (" Divide by %d: <b>%s = %s</b>." % (a - c, v, num(s))) if a - c > 1 else " So <b>%s = %s</b>." % (v, num(s))
    return QS(q, s, [F(d - b, a + c), F(d + b, a - c), F(b - d, a - c), F(d - b, a)], e, v)


# ------------------------------------------------------------ set 2: negatives and the unknown on the right
def one_neg(r):
    v = r.choice(LET)
    s = r.choice([r.randint(-9, -1), r.randint(1, 9)])
    a = r.randint(1, 6)
    c = a + r.randint(1, 5)
    b = r.randint(-12, 12)
    d = b - (c - a) * s
    if d == b or r.random() < 0.3 and False:
        return None
    if r.random() < 0.4:
        # negative coefficient on one side: b - a x = d - c x  -> (c - a) x = d - b
        q = "Solve %s." % B("%s = %s" % (expr([(b, ""), (-a, v)]), expr([(d, ""), (-c, v)])) if b and d else None)
        if not b or not d:
            return None
        ans = F(d - b, c - a)
        e = "Add %s to both sides: %s = %s. Then %s = %s, so <b>%s = %s</b>." % (
            side(c, 0, v), expr([(b, ""), (c - a, v)]), num(d), side(c - a, 0, v), num(d - b), v, sol(ans))
        return QS(q, ans, [F(d - b, a - c), F(d + b, c - a), F(d - b, c + a)], e, v)
    q = "Solve %s." % B("%s = %s" % (side(a, b, v), side(c, d, v)))
    ans = F(b - d, c - a)
    e = "Subtract %s from both sides: %s = %s. Then %s = %s, so <b>%s = %s</b>." % (
        side(a, 0, v), num(b), side(c - a, d, v), side(c - a, 0, v), num(b - d), v, sol(ans))
    return QS(q, ans, [F(d - b, c - a), F(b + d, c - a), F(b - d, c + a)], e, v)


# ------------------------------------------------------------ set 3: brackets on both sides
def one_br(r):
    v = r.choice(LET)
    s = r.randint(-6, 10)
    k1, k2 = r.randint(2, 6), r.randint(2, 6)
    if k1 == k2:
        return None
    b1 = r.randint(-6, 8)
    # k1(x + b1) = k2(x + b2)  =>  k1 s + k1 b1 = k2 s + k2 b2  => b2 = (k1 s + k1 b1 - k2 s)/k2
    num2 = k1 * s + k1 * b1 - k2 * s
    if num2 % k2 or b1 == 0:
        return None
    b2 = num2 // k2
    if b2 == 0:
        return None
    L = "%d(%s)" % (k1, side(1, b1, v))
    Rr = "%d(%s)" % (k2, side(1, b2, v))
    q = "Solve %s." % B("%s = %s" % (L, Rr))
    e = "Expand: %s = %s. Collect: %s = %s, so <b>%s = %s</b>." % (
        side(k1, k1 * b1, v), side(k2, k2 * b2, v), side(k1 - k2, 0, v), num(k2 * b2 - k1 * b1), v, num(s))
    wrong1 = F(b2 - b1, k1 - k2) if k1 != k2 else None            # forgot to multiply the numbers
    wrong2 = F(k2 * b2 - k1 * b1, k1 + k2)
    wrong3 = F(k1 * b1 - k2 * b2, k1 - k2)
    return QS(q, s, [wrong1, wrong2, wrong3], e, v)


# ------------------------------------------------------------ set 4: fraction answers and fraction equations
def one_frac(r):
    v = r.choice(LET)
    kind = r.random()
    if kind < 0.5:
        a, c = r.randint(3, 9), r.randint(1, 2)
        b, d = r.randint(-5, 10), r.randint(-5, 15)
        if a <= c or b == d:
            return None
        ans = F(d - b, a - c)
        if ans.denominator == 1:
            return None
        q = "Solve %s. Give your answer as a fraction." % B("%s = %s" % (side(a, b, v), side(c, d, v)))
        e = "%s = %s, so <b>%s = %s</b>." % (side(a - c, 0, v), num(d - b), v, sol(ans))
        return QS(q, ans, [F(a - c, d - b) if d != b else None, F(d - b, a + c), F(d + b, a - c)], e, v)
    k = r.randint(2, 5)
    s = r.randint(-4, 12)
    a = r.randint(-6, 6)
    c = r.randint(1, 3)
    # (x + a)/k = c x - something?  keep:  (x + a)/k = x - d  -> x + a = k x - k d -> (k-1) x = a + k d
    d = r.randint(1, 8)
    ans = F(a + k * d, k - 1)
    if ans.denominator != 1 or a == 0:
        return None
    q = "Solve %s." % B("%s = %s" % (fr(side(1, a, v), k), side(1, -d, v)))
    e = "Multiply both sides by %d: %s = %s. Subtract %s and add %d to both sides: " % (k, side(1, a, v), side(k, -k * d, v), v, k * d)
    e += ("%s = %s, so <b>%s = %s</b>." % (side(k - 1, 0, v), num(a + k * d), v, sol(ans))) if k > 2 else "<b>%s = %s</b>." % (v, sol(ans))
    return QS(q, ans, [F(a + d, k - 1), F(a - k * d, k - 1), F(k * d - a, k + 1)], e, v)


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    X = "<i>x</i>"
    data = [
        ("Think of a number. Multiply it by 5 and subtract 8. You get the same answer as when you double it and add 7. What is the number?", 5, [F(-1, 3), F(15, 7), 3],
         "5<i>n</i> − 8 = 2<i>n</i> + 7, so 3<i>n</i> = 15 and <i>n</i> = <b>5</b>."),
        ("Phone plan A costs £10 plus 5p a minute. Plan B costs £4 plus 8p a minute. For how many minutes do they cost the same?", 200, [F(1400, 13), 2, 600],
         "1000 + 5<i>m</i> = 400 + 8<i>m</i> (in pence), so 3<i>m</i> = 600 and <i>m</i> = <b>200 minutes</b>."),
        ("A rectangle has length 3%s + 2 and width %s + 10. It is a square. Find %s." % (X, X, X), 4, [6, 3, F(12, 4) + 1],
         "A square has equal sides: 3%s + 2 = %s + 10, so 2%s = 8 and %s = <b>4</b>." % (X, X, X, X)),
        ("Amelia has £(4%s + 6) and Oliver has £(2%s + 20). They have the same amount. Find %s." % (X, X, X), 7, [13, F(13, 3), 3],
         "4%s + 6 = 2%s + 20, so 2%s = 14 and %s = <b>7</b>." % (X, X, X, X)),
        ("Ben is 3 times as old as Kai. In 10 years Ben will be twice as old as Kai. How old is Kai now?", 10, [5, 20, 30],
         "3<i>k</i> + 10 = 2(<i>k</i> + 10), so 3<i>k</i> + 10 = 2<i>k</i> + 20 and <i>k</i> = <b>10</b>."),
        ("The perimeter of a square with side %s + 3 equals the perimeter of an equilateral triangle with side 2%s. Find %s." % (X, X, X), 6, [3, 12, F(3, 2)],
         "4(%s + 3) = 3 × 2%s, so 4%s + 12 = 6%s, 12 = 2%s and %s = <b>6</b>." % (X, X, X, X, X, X)),
        ("A gym charges £30 a month. Another charges £120 to join and £18 a month. After how many months do they cost the same?", 10, [4, F(5, 2), 8],
         "30<i>m</i> = 120 + 18<i>m</i>, so 12<i>m</i> = 120 and <i>m</i> = <b>10</b>."),
        ("Two angles on a straight line are 3%s + 20 and 5%s − 40. Find %s." % (X, X, X), 25, [30, 10, 50],
         "3%s + 20 + 5%s − 40 = 180, so 8%s = 200 and %s = <b>25</b>." % (X, X, X, X)),
        ("Vertically opposite angles are 4%s − 15 and 2%s + 35. Find %s." % (X, X, X), 25, [10, F(20, 6), 50],
         "Vertically opposite angles are equal: 4%s − 15 = 2%s + 35, so 2%s = 50 and %s = <b>25</b>." % (X, X, X, X)),
        ("Solve 0.5%s + 3 = 0.2%s + 6." % (X, X), 10, [F(9, 7), 30, 3], "0.3%s = 3, so %s = <b>10</b>." % (X, X)),
        ("Solve 7 − 2%s = 3%s − 8." % (X, X), 3, [F(1, 5), -3, -15], "Add 2%s: 7 = 5%s − 8. Add 8: 15 = 5%s, so %s = <b>3</b>." % (X, X, X, X)),
        ("Solve 2(%s + 4) = 5%s − 7." % (X, X), 5, [F(11, 3), F(-1, 3), 3], "2%s + 8 = 5%s − 7, so 15 = 3%s and %s = <b>5</b>." % (X, X, X, X)),
    ]
    for q, a, w, e in data:
        its.append(mcq(q, (num(a), F(a)), [(num(F(x)) if F(x).denominator == 1 else sol(x), F(x)) for x in w if F(x) != a] +
                       [(num(F(a) + 1), F(a) + 1), (num(F(a) + 2), F(a) + 2)], e))
    texts = [
        ("Jack solves 5%s + 3 = 2%s + 12. His first step is 7%s + 3 = 12. What is his mistake?" % (X, X, X), "He added 2%s instead of subtracting it" % X,
         ["He should have subtracted 3 first", "There is no mistake", "He should divide by 5 first"], "To remove 2%s from the right, <b>subtract</b> it from both sides: 3%s + 3 = 12." % (X, X)),
        ("Which equation has the solution %s = 4?" % X, "3%s + 1 = %s + 9" % (X, X), ["3%s + 1 = %s + 5" % (X, X), "2%s − 1 = %s + 4" % (X, X), "5%s = 2%s + 8" % (X, X)],
         "Check: 3 × 4 + 1 = 13 and 4 + 9 = 13. So <b>3%s + 1 = %s + 9</b>." % (X, X)),
        ("What should you do first to solve 6%s − 5 = 2%s + 11?" % (X, X), "Subtract 2%s from both sides" % X, ["Divide both sides by 6", "Add 2%s to both sides" % X, "Subtract 6%s from the right" % X],
         "Get the unknowns on one side: <b>subtract 2%s</b>, giving 4%s − 5 = 11." % (X, X)),
        ("Solve 4%s + 7 = 4%s + 7." % (X, X), "Every value of %s works" % X, ["%s = 0" % X, "%s = 7" % X, "There is no solution"], "Both sides are the same, so it is true for <b>every value</b> (an identity)."),
        ("Solve 3%s + 5 = 3%s + 2." % (X, X), "There is no solution", ["%s = 1" % X, "%s = 0" % X, "Every value of %s works" % X], "Subtracting 3%s gives 5 = 2, which is false, so there is <b>no solution</b>." % X),
        ("Check: is %s = −2 the solution of 3%s + 10 = %s + 6?" % (X, X, X), "Yes, both sides equal 4", ["No, the left side is 16", "No, the right side is 8", "Yes, both sides equal 0"],
         "3 × (−2) + 10 = 4 and −2 + 6 = 4. <b>Yes</b>."),
        ("Isla says 9 − %s = %s + 3 gives %s = 6. What is the correct answer?" % (X, X, X), "%s = 3" % X, ["%s = 6" % X, "%s = −3" % X, "%s = 12" % X], "Add %s: 9 = 2%s + 3, so 2%s = 6 and %s = <b>3</b>." % (X, X, X, X)),
        ("A balance has 5 bags of sweets and 2 loose sweets on one side, and 3 bags and 14 loose sweets on the other. Each bag holds the same number. How many sweets are in a bag?", "6",
         ["8", "2", "16"], "5<i>b</i> + 2 = 3<i>b</i> + 14, so 2<i>b</i> = 12 and <i>b</i> = <b>6</b>."),
    ]
    for q, a, w, e in texts:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p>When the unknown is on both sides, first get all the unknowns on one side by adding or subtracting the same "
        "term from both sides. Usually remove the smaller one. Then solve as a two-step equation.</p>"
        "<p>If there are brackets, expand them first. If there is a fraction, multiply both sides by the denominator.</p>",
        [("Solve 5<i>x</i> + 3 = 2<i>x</i> + 18.", ["Subtract 2<i>x</i>: 3<i>x</i> + 3 = 18.", "Subtract 3: 3<i>x</i> = 15.", "Divide by 3."], "<i>x</i> = 5"),
         ("Solve 3(<i>x</i> − 2) = <i>x</i> + 8.", ["Expand: 3<i>x</i> − 6 = <i>x</i> + 8.", "Subtract <i>x</i>: 2<i>x</i> − 6 = 8.", "2<i>x</i> = 14."], "<i>x</i> = 7")],
        ["Adding the <i>x</i> terms instead of subtracting: 5<i>x</i> + 3 = 2<i>x</i> + 18 does not become 7<i>x</i> + 3 = 18.",
         "Moving a term without changing its sign.",
         "Expanding only the first term in a bracket.",
         "Dividing the wrong way round at the end: 3<i>x</i> = 15 gives <i>x</i> = 5, not 1/5."])


def main():
    sets = [S("Unknowns on both sides", collect(one_basic, 20, R)),
            S("Negative numbers and answers", collect(one_neg, 20, R)),
            S("Brackets on both sides", collect(one_br, 20, R)),
            S("Fractions", collect(one_frac, 20, R)),
            S("Problems", problems())]
    make(8, "equations-with-unknowns-on-both-sides", 4, "A",
         "Equations with Unknowns on Both Sides",
         "Year 8 Equations with Unknowns on Both Sides Worksheets: Brackets, Negatives and Word Problems",
         "Unknowns on both sides",
         "Use algebraic methods to solve linear equations in one variable (including all forms that require rearrangement).",
         "Free Year 8 worksheets on solving equations with unknowns on both sides: negatives, brackets on both sides, "
         "fraction answers and forming equations from word problems. 100 questions with step-by-step answers.",
         "Get the unknowns on one side first by subtracting the smaller term from both sides.",
         "Expand brackets first. Whatever you do to one side, do to the other.",
         body(),
         [("How do I solve an equation with x on both sides?", "Subtract the smaller x term from both sides so the unknowns are on one side, then solve the two-step equation that is left."),
          ("Which side should I move the x terms to?", "Either works, but moving the smaller x term avoids negative coefficients."),
          ("What if the x terms cancel out?", "If you get a true statement like 7 = 7, every value works. If you get a false one like 5 = 2, there is no solution."),
          ("Can the answer be negative or a fraction?", "Yes. For example 5x + 1 = 2x − 7 gives x = −8/3.")],
         sets, R)


if __name__ == "__main__":
    main()
