# -*- coding: utf-8 -*-
"""
US Algebra 1: Systems of Linear Equations (Common Core A-REI.C.6, A-REI.C.5, A-CED.A.3)
  python3 tools/gen_us_math_a1_systems_of_linear_equations.py
Elimination by adding or subtracting, multiplying one equation, multiplying both equations, substitution,
and word problems (tickets, coins, mixtures, rates and number of solutions).
Wrong answers come from real mistakes: swapping x and y, subtracting when the signs say add, finding one value
correctly and substituting wrongly, and only multiplying one side of an equation.
"""
import random
from us_hs import num, B, S, make, lesson, collect, T, expr, usd

R = random.Random(90801)
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
    q = "Solve the system.<br>" + pair(e1, e2)
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
    q = "Solve the system.<br>" + pair(e1, e2)
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
    q = "Solve the system.<br>" + pair(e1, e2)
    e = "Multiply the first equation by %d: %s. Now both have %s, so subtract to find %s = %s, then %s = %s. <b>%s</b>." % (
        k, eq(a1 * k, b1 * k, (a1 * x + b1 * y) * k), expr([(b2, Y)]), X, num(x), Y, num(y), ans(x, y))
    return T(q, ans(x, y), wrongs(x, y, [ans(x, y - 1)]), e)


# ------------------------------------------------------------ set 3b: multiply both equations
def one_both(r):
    x, y = nz(r, -5, 7), nz(r, -5, 7)
    if x == y or x == -y:
        return None
    a1, a2 = r.choice([2, 3, 4, 5]), r.choice([2, 3, 4, 5, 7])
    b1, b2 = r.choice([2, 3, 5, -2, -3]), r.choice([2, 3, 4, 7, -4, -5])
    if a1 == a2 or abs(b1) == abs(b2) or a1 * b2 - a2 * b1 == 0 or a2 % a1 == 0 or a1 % a2 == 0:
        return None
    c1, c2 = a1 * x + b1 * y, a2 * x + b2 * y
    q = "Solve the system.<br>" + pair(eq(a1, b1, c1), eq(a2, b2, c2))
    e = ("Multiply the first equation by %d and the second by %d so the %s-terms match: %s and %s. Subtract to find %s = %s, "
         "then substitute to find %s = %s. <b>%s</b>." % (a2, a1, X, eq(a1 * a2, b1 * a2, c1 * a2), eq(a2 * a1, b2 * a1, c2 * a1), Y, num(y), X, num(x), ans(x, y)))
    return T(q, ans(x, y), wrongs(x, y, [ans(x, y + 1)]), e)


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
    data = [
        ("A school play sold 300 tickets. Adult tickets cost $12 and student tickets cost $7. Ticket sales were $2,850. How many adult tickets were sold?", "150",
         ["120", "180", "237"], "<i>a</i> + <i>s</i> = 300 and 12<i>a</i> + 7<i>s</i> = 2,850. Multiply the first by 7: 7<i>a</i> + 7<i>s</i> = 2,100. Subtract: 5<i>a</i> = 750, so <i>a</i> = <b>150</b>."),
        ("Maya has 30 coins, all dimes and quarters, worth $5.40. How many quarters does she have?", "16", ["14", "20", "18"],
         "<i>d</i> + <i>q</i> = 30 and 10<i>d</i> + 25<i>q</i> = 540. Multiply the first by 10 and subtract: 15<i>q</i> = 240, so <i>q</i> = <b>16</b>."),
        ("A chemist mixes a 10% acid solution with a 40% acid solution to make 30 L of a 20% solution. How many liters of the 10% solution are used?", "20 L",
         ["10 L", "15 L", "25 L"], "<i>a</i> + <i>b</i> = 30 and 0.1<i>a</i> + 0.4<i>b</i> = 6. Multiply the first by 0.1 and subtract: 0.3<i>b</i> = 3, so <i>b</i> = 10 and <i>a</i> = <b>20 L</b>."),
        ("A coffee shop mixes beans that cost $8 per pound with beans that cost $14 per pound to make 60 lb worth $10 per pound. How many pounds of $8 beans are used?", "40 lb",
         ["20 lb", "30 lb", "45 lb"], "<i>x</i> + <i>y</i> = 60 and 8<i>x</i> + 14<i>y</i> = 600. Then 6<i>y</i> = 120, <i>y</i> = 20 and <i>x</i> = <b>40 lb</b>."),
        ("A boat goes 36 miles downstream in 2 hours and 36 miles back upstream in 3 hours. What is the speed of the current?", "3 mph", ["15 mph", "6 mph", "12 mph"],
         "<i>b</i> + <i>c</i> = 18 and <i>b</i> − <i>c</i> = 12. Subtract: 2<i>c</i> = 6, so <i>c</i> = <b>3 mph</b> (and the boat goes 15 mph)."),
        ("Gym A charges $50 to join and $30 a month. Gym B charges $20 to join and $35 a month. After how many months do they cost the same?", "6", ["4", "10", "14"],
         "<i>C</i> = 30<i>m</i> + 50 and <i>C</i> = 35<i>m</i> + 20. Set equal: 5<i>m</i> = 30, so <i>m</i> = <b>6</b>."),
        ("The sum of two numbers is 47 and their difference is 13. What is the smaller number?", "17", ["30", "13", "34"], "Add: 2<i>x</i> = 60, so <i>x</i> = 30 and the smaller number is <b>17</b>."),
        ("A farm has chickens and goats: 40 heads and 110 legs. How many goats are there?", "15", ["25", "20", "10"],
         "<i>c</i> + <i>g</i> = 40 and 2<i>c</i> + 4<i>g</i> = 110. Double the first and subtract: 2<i>g</i> = 30, so <i>g</i> = <b>15</b>."),
        ("2 burgers and 3 drinks cost $18.50. 4 burgers and 1 drink cost $24.50. How much is one burger?", "$5.50", ["$2.50", "$4.75", "$6.00"],
         "Double the first: 4<i>b</i> + 6<i>d</i> = 37. Subtract the second: 5<i>d</i> = 12.50, so <i>d</i> = 2.50 and <i>b</i> = <b>$5.50</b>."),
        ("A rectangle's perimeter is 54 ft. Its length is 3 ft less than twice its width. What is its length?", "17 ft", ["10 ft", "24 ft", "27 ft"],
         "2<i>l</i> + 2<i>w</i> = 54 and <i>l</i> = 2<i>w</i> − 3. Then 2(2<i>w</i> − 3) + 2<i>w</i> = 54, so 6<i>w</i> = 60, <i>w</i> = 10 and <i>l</i> = <b>17 ft</b>."),
        ("How many solutions does the system 2<i>x</i> − <i>y</i> = 4 and 4<i>x</i> − 2<i>y</i> = 8 have?", "Infinitely many", ["None", "Exactly one", "Exactly two"],
         "The second equation is the first times 2, so they are the same line: <b>infinitely many</b>."),
        ("How many solutions does the system <i>y</i> = 3<i>x</i> + 2 and <i>y</i> = 3<i>x</i> − 5 have?", "None", ["Exactly one", "Infinitely many", "Exactly two"],
         "Same slope, different intercepts: the lines are parallel, so there is <b>no solution</b>."),
        ("Which value of <i>k</i> makes the system <i>x</i> + 2<i>y</i> = 6 and 3<i>x</i> + <i>ky</i> = 10 have no solution?", "6", ["2", "3", "−6"],
         "For parallel lines the coefficients must be in the same ratio: <i>k</i> = 2 × 3 = <b>6</b> (and 10 ≠ 18)."),
        ("A phone plan charges a monthly fee plus a cost per GB. 3 GB costs $41 and 7 GB costs $61. What is the monthly fee?", "$26", ["$5", "$41", "$20"],
         "4 more GB cost $20, so 1 GB costs $5. Fee = 41 − 15 = <b>$26</b>."),
        ("At a fair, 3 hot dogs and 2 lemonades cost $16. 2 hot dogs and 4 lemonades cost $16. How much is a lemonade?", "$2", ["$4", "$3", "$1.50"],
         "Multiply the first by 2: 6<i>h</i> + 4<i>l</i> = 32. Subtract the second: 4<i>h</i> = 16, so <i>h</i> = 4 and <i>l</i> = <b>$2</b>."),
        ("Which ordered pair is the solution of <i>y</i> = −<i>x</i> + 5 and <i>y</i> = 2<i>x</i> − 4?", "(3, 2)", ["(2, 3)", "(1, 4)", "(3, −2)"], "−<i>x</i> + 5 = 2<i>x</i> − 4, so <i>x</i> = 3 and <i>y</i> = <b>2</b>: (3, 2)."),
        ("A plane flies 1,200 miles with the wind in 3 hours and back against the wind in 4 hours. What is its speed in still air?", "350 mph", ["400 mph", "300 mph", "50 mph"],
         "<i>p</i> + <i>w</i> = 400 and <i>p</i> − <i>w</i> = 300. Add: 2<i>p</i> = 700, so <i>p</i> = <b>350 mph</b>."),
        ("Liam invests $5,000, part at 3% and part at 5% simple interest. He earns $190 in a year. How much is at 5%?", "$2,000", ["$3,000", "$2,500", "$3,800"],
         "<i>a</i> + <i>b</i> = 5,000 and 0.03<i>a</i> + 0.05<i>b</i> = 190. Multiply the first by 0.03 and subtract: 0.02<i>b</i> = 40, so <i>b</i> = <b>$2,000</b>."),
        ("Which method is quickest for <i>y</i> = 4<i>x</i> − 1 and 3<i>x</i> + 2<i>y</i> = 20?", "Substitution", ["Elimination by adding", "Guess and check", "Graphing only"],
         "<i>y</i> is already alone, so put 4<i>x</i> − 1 in for <i>y</i>: <b>substitution</b>. (The solution is (2, 7).)"),
        ("Ethan solves a system and gets <i>x</i> = 2, <i>y</i> = 5. How can he check?", "Substitute into both equations", ["Substitute into one equation", "Add the two answers", "Graph only the first equation"],
         "The pair must make <b>both</b> equations true."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>A <b>system of linear equations</b> is two equations that must be true at the same time. "
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
    sets = [S("Elimination by adding or subtracting", collect(one_add, 10, R) + collect(one_sub, 10, R)),
            S("Multiply one equation, then eliminate", collect(one_mult, 20, R)),
            S("Multiply both equations", collect(one_both, 20, R)),
            S("Substitution", collect(one_subst, 20, R)),
            S("Systems word problems", problems())]
    make("systems-of-linear-equations", 8, "A-REI.C.6",
         "Systems of Linear Equations: Elimination, Substitution and Word Problems",
         "Algebra 1 Systems of Equations Worksheets: Elimination, Substitution and Word Problems (Free, Answer Key)",
         "Systems of linear equations",
         "Solve systems of linear equations exactly and approximately (e.g., with graphs), focusing on pairs of linear equations in two variables.",
         "Free Algebra 1 systems of equations worksheets (A-REI.C.6): elimination by adding or subtracting, multiplying one or both equations, "
         "substitution, and word problems with tickets, coins, mixtures and rates. 100 questions with an answer key.",
         "Eliminate one variable, solve for the other, then substitute back.",
         "Same signs: subtract. Different signs: add. Check the answer in both equations.",
         body(),
         [("What is a system of linear equations?", "Two linear equations with the same two variables. The solution is the pair of values that makes both equations true."),
          ("Do I add or subtract the equations?", "Look at the letter you want to remove. If its signs are the same, subtract. If they are different, add."),
          ("When should I use substitution?", "When one equation already says y = … or x = …. Put that expression into the other equation."),
          ("How can a system have no solution or infinitely many?", "Each equation is a line. Parallel lines never meet (no solution); the same line meets everywhere (infinitely many solutions).")],
         sets, R, domain="Systems")


if __name__ == "__main__":
    main()
