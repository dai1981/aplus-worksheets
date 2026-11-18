# -*- coding: utf-8 -*-
"""
SG Secondary 2 Maths: Simultaneous Equations (Sec 2 Algebra)
  python3 gen_sg_maths_s2_simultaneous_equations.py
Solving pairs of linear equations by elimination (adding, subtracting, multiplying first) and by substitution,
then word problems. Wrong answers come from real mistakes: swapping x and y, subtracting when the signs say add
(sign errors), finding one value correctly and substituting wrongly, and only finding one of the two values.
"""
import random
from sg_sec import num, B, S, make, lesson, collect, T, expr, sgd, GIRLS, BOYS

R = random.Random(820600)
X, Y = "<i>x</i>", "<i>y</i>"


def eq(a, b, c):
    return "%s = %s" % (expr([(a, X), (b, Y)]), num(c))


def pair(e1, e2):
    return B(e1) + "<br>" + B(e2)


def ans(x, y):
    return "%s = %s, %s = %s" % (X, num(x), Y, num(y))


def wrongs(x, y, extra):
    w = [ans(y, x), ans(x, -y), ans(-x, y)] + extra
    out = []
    for a in w:
        if a != ans(x, y) and a not in out:
            out.append(a)
    return out[:3]


def nz(r, lo, hi):
    while True:
        k = r.randint(lo, hi)
        if k:
            return k


# ------------------------------------------------------------ set 1: add to eliminate
def one_add(r):
    x, y = nz(r, -6, 9), nz(r, -6, 9)
    if x == y or x == -y:
        return None
    a1, a2 = r.randint(1, 4), r.randint(1, 4)
    b = r.randint(1, 5)
    e1, e2 = eq(a1, b, a1 * x + b * y), eq(a2, -b, a2 * x - b * y)
    q = "Solve the simultaneous equations.<br>" + pair(e1, e2)
    s = (a1 + a2) * x
    e = "Add the equations: the %s terms cancel. %s, so %s = %s. Substitute into the first equation: %s = %s. <b>%s</b>." % (
        Y, "%s = %s" % (expr([(a1 + a2, X)]), num(s)), X, num(x), Y, num(y), ans(x, y))
    return T(q, ans(x, y), wrongs(x, y, [ans(x, y + 1)]), e)


# ------------------------------------------------------------ set 2: subtract to eliminate
def one_sub(r):
    x, y = nz(r, -6, 9), nz(r, -6, 9)
    if x == y or x == -y:
        return None
    a1, a2 = r.randint(1, 5), r.randint(1, 5)
    if a1 == a2:
        return None
    b = r.randint(1, 4)
    e1, e2 = eq(a1, b, a1 * x + b * y), eq(a2, b, a2 * x + b * y)
    q = "Solve the simultaneous equations.<br>" + pair(e1, e2)
    d = a1 - a2
    step = "%s = %s" % (expr([(d, X)]), num(d * x))
    if d != 1:
        step += ", so %s = %s" % (X, num(x))
    e = "Both have %s, so subtract: %s. Substitute back to get %s = %s. <b>%s</b>." % (
        expr([(b, Y)]), step, Y, num(y), ans(x, y))
    # adding instead of subtracting
    return T(q, ans(x, y), wrongs(x, y, [ans(x + 1, y)]), e)


# ------------------------------------------------------------ set 3: multiply first
def one_mult(r):
    x, y = nz(r, -5, 8), nz(r, -5, 8)
    if x == y or x == -y:
        return None
    a1, b1 = r.randint(1, 5), nz(r, -4, 5)
    k = r.randint(2, 4)
    a2, b2 = r.randint(1, 6), b1 * k
    if a2 == a1 * k or (a1 * b2 - a2 * b1) == 0:
        return None
    e1, e2 = eq(a1, b1, a1 * x + b1 * y), eq(a2, b2, a2 * x + b2 * y)
    q = "Solve the simultaneous equations.<br>" + pair(e1, e2)
    e = "Multiply the first equation by %d: %s. Now both have %s, so subtract to find %s = %s, then %s = %s. <b>%s</b>." % (
        k, eq(a1 * k, b1 * k, (a1 * x + b1 * y) * k), expr([(b2, Y)]), X, num(x), Y, num(y), ans(x, y))
    return T(q, ans(x, y), wrongs(x, y, [ans(x, y - 1)]), e)


# ------------------------------------------------------------ set 4: substitution
def one_subst(r):
    x, y0 = nz(r, -5, 7), 0
    m, c = nz(r, -3, 4), nz(r, -6, 6)
    y = m * x + c
    if y == 0 or x == y or x == -y:
        return None
    a, b = r.randint(1, 4), nz(r, -3, 4)
    e1 = "%s = %s" % (Y, expr([(m, X), (c, "")]))
    e2 = eq(a, b, a * x + b * y)
    if a + b * m == 0:
        return None
    q = "Solve by substitution.<br>" + pair(e1, e2)
    e = "Replace %s in the second equation with %s, then solve: %s = %s. So %s = %s. <b>%s</b>." % (
        Y, expr([(m, X), (c, "")]), X, num(x), Y, num(y), ans(x, y))
    return T(q, ans(x, y), wrongs(x, y, [ans(x, m * x - c)]), e)


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    r = R
    # cost problems
    items = [("adult ticket", "child ticket", "adult ticket", "child ticket", 900, 1300, 500, 800),
             ("coffee", "tea", "coffee", "tea", 280, 380, 150, 250),
             ("pen", "pencil", "pen", "pencil", 90, 150, 30, 70),
             ("burger", "drink", "burger", "drink", 450, 700, 120, 220),
             ("notebook", "ruler", "notebook", "ruler", 200, 350, 60, 140)]
    for p, q2, _, _, alo, ahi, blo, bhi in items:
        a = r.randint(alo // 10, ahi // 10) * 10
        b = r.randint(blo // 10, bhi // 10) * 10
        n1, m1, n2, m2 = 2, 3, 3, 1
        t1, t2 = n1 * a + m1 * b, n2 * a + m2 * b
        q = ("%d %ss and %d %ss cost %s. %d %ss and %d %s cost %s. How much is one %s?" % (
            n1, p, m1, q2, sgd(t1 / 100), n2, p, m2, q2 + ("" if m2 == 1 else "s"), sgd(t2 / 100), p))
        right = sgd(a / 100)
        wr = [sgd(b / 100), sgd((t1 / 5) / 100) if t1 % 5 == 0 else sgd((a + 10) / 100), sgd((a - 10) / 100)]
        wr = [w for w in dict.fromkeys(wr) if w != right]
        if len(wr) < 3:
            wr.append(sgd((a + 20) / 100))
        e = "Let %s = one %s and %s = one %s (in cents): %s and %s. Multiply the second by 3 and subtract the first: 7%s = %s, so %s = %s. <b>%s</b>." % (
            X, p, Y, q2, B(eq(2, 3, t1)), B(eq(3, 1, t2)), X, num(7 * a), X, num(a), right)
        its.append(T(q, right, wr[:3], e))
    data = [
        ("Two numbers add to 30 and their difference is 8. What are the numbers?", "19 and 11", ["15 and 15", "22 and 8", "20 and 10"],
         "%s + %s = 30 and %s − %s = 8. Add: 2%s = 38, so %s = 19 and %s = 11. <b>19 and 11</b>." % (X, Y, X, Y, X, X, Y)),
        ("Two numbers add to 50 and their difference is 14. What is the larger number?", "32", ["18", "36", "25"],
         "2%s = 50 + 14 = 64, so the larger number is <b>32</b>." % X),
        ("The sum of two numbers is 17. Twice the first plus the second is 24. What is the first number?", "7", ["10", "12", "8"],
         "(2%s + %s) − (%s + %s) = 24 − 17, so %s = <b>7</b>." % (X, Y, X, Y, X)),
        ("A farm has hens and cows. There are 20 heads and 56 legs. How many cows are there?", "8", ["12", "14", "6"],
         "%s + %s = 20 and 2%s + 4%s = 56. Double the first: 2%s + 2%s = 40. Subtract: 2%s = 16, so %s = <b>8</b> cows." % (X, Y, X, Y, X, Y, Y, Y)),
        ("At which point do the lines %s and %s cross?" % (B("%s = 2%s + 1" % (Y, X)), B("%s = −%s + 7" % (Y, X))), "(2, 5)", ["(5, 2)", "(3, 7)", "(2, 3)"],
         "2%s + 1 = −%s + 7, so 3%s = 6 and %s = 2. Then %s = 5. The lines cross at <b>(2, 5)</b>." % (X, X, X, X, Y)),
        ("At which point do the lines %s and %s cross?" % (B("%s + %s = 10" % (X, Y)), B("%s = %s + 4" % (Y, X))), "(3, 7)", ["(7, 3)", "(4, 6)", "(3, 6)"],
         "%s + (%s + 4) = 10, so 2%s = 6 and %s = 3. Then %s = 7: <b>(3, 7)</b>." % (X, X, X, X, Y)),
        ("A theatre sold 200 tickets. Adult tickets cost $12 and child tickets cost $7. The total was $1900. How many adult tickets were sold?", "100", ["80", "120", "150"],
         "%s + %s = 200 and 12%s + 7%s = 1900. Multiply the first by 7: 7%s + 7%s = 1400. Subtract: 5%s = 500, so %s = <b>100</b>." % (X, Y, X, Y, X, Y, X, X)),
        ("Xin Yi has 25 coins. They are all 10p and 20p coins. They are worth $3.70. How many 20p coins does she have?", "12", ["13", "15", "10"],
         "%s + %s = 25 and 10%s + 20%s = 370. Multiply the first by 10 and subtract: 10%s = 120, so %s = <b>12</b>." % (X, Y, X, Y, Y, Y)),
        ("Which pair of values satisfies both %s and %s?" % (B(eq(1, 1, 9)), B(eq(1, -1, 3))), ans(6, 3), [ans(3, 6), ans(5, 4), ans(7, 2)],
         "Add: 2%s = 12, so %s = 6 and %s = 3. Check: 6 + 3 = 9 and 6 − 3 = 3. <b>%s</b>." % (X, X, Y, ans(6, 3))),
        ("Marcus solves %s and %s and gets %s = 4, %s = 1. What should he do to check?" % (B(eq(2, 1, 9)), B(eq(1, 3, 7)), X, Y),
         "Substitute into both equations", ["Substitute into one equation only", "Add the answers together", "Draw a bar chart"],
         "2(4) + 1 = 9 ✓ and 4 + 3(1) = 7 ✓. <b>Substitute into both equations</b>; the answer must work in each."),
        ("A rectangle has perimeter 34 cm. Its length is 5 cm more than its width. What is its length?", "11 cm", ["6 cm", "14.5 cm", "12 cm"],
         "2<i>l</i> + 2<i>w</i> = 34 and <i>l</i> = <i>w</i> + 5. So 2(<i>w</i> + 5) + 2<i>w</i> = 34, 4<i>w</i> = 24, <i>w</i> = 6, <i>l</i> = <b>11 cm</b>."),
        ("In 5 years, Mei Ling will be twice as old as her brother. Now the sum of their ages is 26. How old is Mei Ling now?", "19", ["7", "17", "13"],
         "<i>f</i> + <i>b</i> = 26 and <i>f</i> + 5 = 2(<i>b</i> + 5). So <i>f</i> = 2<i>b</i> + 5 and 3<i>b</i> + 5 = 26, <i>b</i> = 7, <i>f</i> = <b>19</b>."),
        ("How many solutions do %s and %s have?" % (B(eq(1, 1, 5)), B(eq(2, 2, 10))), "Infinitely many", ["Exactly one", "None", "Exactly two"],
         "The second equation is the first multiplied by 2, so they are the same line: <b>infinitely many</b> solutions."),
        ("How many solutions do %s and %s have?" % (B(eq(1, 1, 5)), B(eq(1, 1, 8))), "None", ["Exactly one", "Infinitely many", "Exactly two"],
         "%s + %s cannot be 5 and 8 at the same time. The lines are parallel: <b>no solution</b>." % (X, Y)),
        ("A taxi charges a fixed fee plus a cost per km. 4 km cost $10 and 10 km cost $19. What is the cost per km?", "$1.50", ["$2.50", "$1.90", "$9.00"],
         "<i>f</i> + 10<i>m</i> = 19 and <i>f</i> + 4<i>m</i> = 10. Subtract: 6<i>m</i> = 9, so <i>m</i> = <b>$1.50</b>."),
    ]
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p><b>Simultaneous equations</b> are two equations that are true at the same time. "
        "The solution is the one pair of values (<i>x</i>, <i>y</i>) that works in <b>both</b>. It is where the two lines cross.</p>"
        "<p><b>Elimination:</b> make one letter have the same number in front in both equations. "
        "If the signs are <b>different, add</b>. If the signs are the <b>same, subtract</b>. "
        "<b>Substitution:</b> if one equation says <i>y</i> = …, put that into the other equation.</p>",
        [("Solve 3<i>x</i> + <i>y</i> = 11 and <i>x</i> − <i>y</i> = 1.", ["Signs differ, so add: 4<i>x</i> = 12, <i>x</i> = 3.", "3 − <i>y</i> = 1, so <i>y</i> = 2."], "<i>x</i> = 3, <i>y</i> = 2"),
         ("Solve 2<i>x</i> + 3<i>y</i> = 12 and <i>x</i> + <i>y</i> = 5.", ["Multiply the second by 2: 2<i>x</i> + 2<i>y</i> = 10.", "Subtract: <i>y</i> = 2, then <i>x</i> = 3."], "<i>x</i> = 3, <i>y</i> = 2"),
         ("Solve <i>y</i> = 2<i>x</i> and <i>x</i> + <i>y</i> = 9.", ["<i>x</i> + 2<i>x</i> = 9, so <i>x</i> = 3.", "<i>y</i> = 2 × 3 = 6."], "<i>x</i> = 3, <i>y</i> = 6")],
        ["Adding when you should subtract. Same signs: subtract. Different signs: add.",
         "Multiplying only one side of an equation. Multiply every term.",
         "Finding <i>x</i> and stopping. You must find <i>y</i> as well.",
         "Swapping the values of <i>x</i> and <i>y</i>. Check your answer in both equations."])


def main():
    sets = [S("Elimination by adding", collect(one_add, 20, R)),
            S("Elimination by subtracting", collect(one_sub, 20, R)),
            S("Multiplying before eliminating", collect(one_mult, 20, R)),
            S("Substitution", collect(one_subst, 20, R)),
            S("Simultaneous equation problems", problems())]
    make(2, "simultaneous-equations", 5, "N7",
         "Simultaneous Equations",
         "Secondary 2 Simultaneous Equations Worksheets: Elimination, Substitution and Word Problems",
         "Simultaneous Equations",
         "Use algebraic methods to solve linear equations in one variable (including all forms that require rearrangement); "
         "find approximate solutions to contextual problems from given graphs of a variety of functions.",
         "Free Secondary 2 simultaneous equations worksheets: solve by elimination (adding, subtracting, multiplying first) and by "
         "substitution, then word problems. 100 questions with answers.",
         "Eliminate one letter, find the other, then substitute back.",
         "Same signs: subtract. Different signs: add. Always check in both equations.",
         body(),
         [("What are simultaneous equations?", "Two equations with two unknowns that are both true at once. The solution is the pair of values that works in both."),
          ("Do I add or subtract the equations?", "Look at the letter you want to remove. If its signs are the same, subtract. If they are different, add."),
          ("When should I use substitution?", "When one equation already says y = … or x = …. Put that expression into the other equation."),
          ("How do simultaneous equations link to graphs?", "Each equation is a straight line. The solution is the point where the two lines cross.")],
         sets, R)


if __name__ == "__main__":
    main()
