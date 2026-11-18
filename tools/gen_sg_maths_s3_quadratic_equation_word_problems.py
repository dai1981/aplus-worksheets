# -*- coding: utf-8 -*-
"""
SG Secondary 3 Maths: Quadratic Equation Word Problems (MOE syllabus N7: formulating a quadratic equation in one
variable to solve problems)
  python3 tools/gen_sg_maths_s3_quadratic_equation_word_problems.py
Forming the equation, number problems, rectangles and paths, right-angled triangles (Pythagoras' theorem),
heights of objects thrown up, and problems that need answers correct to 2 decimal places.
Wrong answers come from real mistakes: forming the equation without making one side 0, keeping the negative
root, taking the wrong side as the answer, and squaring only one part of a bracket.
"""
import random
from math import sqrt
from sg_sec import num, S, make, lesson, collect, T, expr, MINUS, People, sgd

R = random.Random(830500)
P = People(R)
X = "<i>x</i>"
X2 = X + "<sup>2</sup>"


def lin(a, b):
    return expr([(a, X), (b, "")])


def quad(a, b, c):
    return expr([(a, X2), (b, X), (c, "")])


def eq0(a, b, c):
    return "%s = 0" % quad(a, b, c)


def d2(v):
    return ("%.2f" % v).replace("-", MINUS)


def ok_dp(v):
    return abs(abs(v) * 100 % 1 - 0.5) > 0.03


# ------------------------------------------------------------ set 1: forming the equation
def one_form(r):
    kind = r.choice(["rect", "rect", "cons", "tri", "square"])
    if kind == "rect":
        d = r.randint(2, 9)
        A = r.randint(20, 120)
        qh = "A rectangle is (%s) cm long and %s cm wide. Its area is %s cm². Which equation is correct?" % (lin(1, d), X, num(A))
        right = eq0(1, d, -A)
        return T(qh, right, [eq0(1, d, A), eq0(1, 2 * d, -A), "%s = 0" % expr([(2, X), (d, ""), (-A, "")]) if False else eq0(2, 2 * d, -A)],
                 "Area = length × width: %s(%s) = %s. Expand and make one side 0: <b>%s</b>." % (X, lin(1, d), num(A), right))
    if kind == "cons":
        n0 = r.randint(5, 20)
        p = n0 * (n0 + 1)
        qh = "The product of two consecutive whole numbers is %s. If the smaller number is %s, which equation is correct?" % (num(p), X)
        right = eq0(1, 1, -p)
        return T(qh, right, [eq0(1, 0, -p) if False else "%s = 0" % expr([(1, X2), (-p, "")]), eq0(1, 1, p), eq0(1, 2, -p)],
                 "The numbers are %s and %s + 1: %s(%s + 1) = %s, so <b>%s</b>." % (X, X, X, X, num(p), right))
    if kind == "tri":
        a, b = r.choice([(1, 2), (2, 1), (1, 7), (7, 1), (2, 7), (7, 8)])
        # legs x and x + a, hypotenuse x + b with b > a
        if b <= a:
            return None
        qh = "The sides of a right-angled triangle are %s cm, (%s) cm and (%s) cm, where (%s) cm is the longest side. Which equation is correct?" % (X, lin(1, a), lin(1, b), lin(1, b))
        # x² + (x + a)² = (x + b)²  ->  x² + (2a − 2b)x + a² − b² = 0
        right = eq0(1, 2 * a - 2 * b, a * a - b * b)
        return T(qh, right, [eq0(1, 2 * a + 2 * b, a * a + b * b), eq0(2, 2 * a, a * a - b * b) if False else eq0(3, 2 * a + 2 * b, a * a + b * b), eq0(1, 0, a * a - b * b)],
                 "Pythagoras' theorem: %s + (%s)<sup>2</sup> = (%s)<sup>2</sup>. Expand and simplify: <b>%s</b>." % (X2, lin(1, a), lin(1, b), right))
    s = r.randint(5, 20)
    w = r.choice([1, 2])
    A = (s + 2 * w) ** 2 - s * s
    qh = "A square lawn of side %s m has a path %s m wide all round it. The path has an area of %s m². Which equation is correct?" % (X, num(w), num(A))
    right = "%s = 0" % expr([(4 * w, X), (4 * w * w - A, "")])
    return T(qh, right, ["%s = 0" % expr([(2 * w, X), (w * w - A, "")]), eq0(1, 4 * w, 4 * w * w - A), "%s = 0" % expr([(4 * w, X), (-A, "")])],
             "(%s)<sup>2</sup> − %s = %s. The %s terms cancel, leaving <b>%s</b>. Not every problem gives a quadratic." % (lin(1, 2 * w), X2, num(A), X2, right))


# ------------------------------------------------------------ set 2: number problems
def one_num(r):
    kind = r.choice(["cons", "sumprod", "sq", "even"])
    if kind == "cons":
        n = r.randint(5, 25)
        qh = "The product of two consecutive positive whole numbers is %s. Find the larger number." % num(n * (n + 1))
        return T(qh, num(n + 1), [num(n), num(-(n + 1)), num(n * (n + 1) // 2)],
                 "%s = 0 gives (%s)(%s) = 0. %s = %d (the positive root), so the larger number is <b>%d</b>." % (
                     quad(1, 1, -n * (n + 1)), lin(1, -n), lin(1, n + 1), X, n, n + 1))
    if kind == "sumprod":
        a, b = r.sample(range(2, 20), 2)
        a, b = min(a, b), max(a, b)
        qh = "Two positive numbers add up to %d and multiply to %d. What is the smaller number?" % (a + b, a * b)
        return T(qh, num(a), [num(b), num(a + b - 1), num(a * b // (a + b)) if a * b // (a + b) not in (a, b) else num(a + 1)],
                 "Let one number be %s, so the other is %d − %s. %s(%d − %s) = %d gives %s, so (%s)(%s) = 0. The smaller number is <b>%d</b>." % (
                     X, a + b, X, X, a + b, X, a * b, eq0(1, -(a + b), a * b), lin(1, -a), lin(1, -b), a))
    if kind == "sq":
        n = r.randint(3, 15)
        k = r.choice([2, 3, 4, 5, 6])
        v = n * n + k * n
        qh = "When %d times a positive number is added to its square, the result is %d. Find the number." % (k, v)
        return T(qh, num(n), [num(n + k), num(-(n + k)), num(v // k) if v // k != n else num(n + 1)],
                 "%s + %d%s = %d gives (%s)(%s) = 0. The positive answer is <b>%d</b>." % (X2, k, X, v, lin(1, -n), lin(1, n + k), n))
    n = r.randint(2, 15) * 2
    v = n * n + (n + 2) ** 2
    qh = "The sum of the squares of two consecutive even numbers is %s. If both numbers are positive, what is the smaller one?" % num(v)
    return T(qh, num(n), [num(n + 2), num(n - 2), num(n + 4)],
             "%s + (%s)<sup>2</sup> = %s gives 2%s + 4%s %s %s = 0. Divide by 2: %s, so (%s)(%s) = 0. The answer is <b>%d</b>." % (
                 X2, lin(1, 2), num(v), X2, X, MINUS, num(v - 4), eq0(1, 2, -(v - 4) // 2), lin(1, -n), lin(1, n + 2), n))


# ------------------------------------------------------------ set 3: rectangles, triangles and paths
TRIPLES = [(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (9, 12, 15), (7, 24, 25), (12, 16, 20), (20, 21, 29), (9, 40, 41), (15, 20, 25)]


def one_geo(r):
    kind = r.choice(["rect", "perim", "tri", "tri", "path"])
    if kind == "rect":
        w = r.randint(3, 15)
        d = r.randint(2, 8)
        A = w * (w + d)
        qh = "A rectangular plot is %d m longer than it is wide. Its area is %s m². Find its length." % (d, num(A))
        return T(qh, "%d m" % (w + d), ["%d m" % w, "%d m" % (w + 2 * d), "%s m" % num(A // d) if A // d not in (w, w + d) else "%d m" % (w + d + 1)],
                 "Width %s m, length (%s) m: %s = 0, so (%s)(%s) = 0 and %s = %d. The length is <b>%d m</b>." % (X, lin(1, d), quad(1, d, -A), lin(1, -w), lin(1, w + d), X, w, w + d))
    if kind == "perim":
        w = r.randint(3, 15)
        l = w + r.randint(2, 10)
        qh = "A rectangle has a perimeter of %d cm and an area of %d cm². Find the length of its longer side." % (2 * (w + l), w * l)
        return T(qh, "%d cm" % l, ["%d cm" % w, "%d cm" % (w + l), "%d cm" % (2 * l)],
                 "If one side is %s, the other is %d − %s. %s(%d − %s) = %d gives %s, so the sides are %d and %d. The longer side is <b>%d cm</b>." % (
                     X, w + l, X, X, w + l, X, w * l, eq0(1, -(w + l), w * l), w, l, l))
    if kind == "tri":
        a, b, c = r.choice(TRIPLES)
        k = r.choice([1, 1, 2])
        a, b, c = a * k, b * k, c * k
        if (b - a) == (c - b):
            # sides x, x + d, x + 2d
            qh = "The sides of a right-angled triangle are %s cm, (%s) cm and (%s) cm. Find %s." % (X, lin(1, b - a), lin(1, c - a), X)
        else:
            qh = "The sides of a right-angled triangle are %s cm, (%s) cm and (%s) cm. Find %s." % (X, lin(1, b - a), lin(1, c - a), X)
        p, q = b - a, c - a
        # x² + (x+p)² = (x+q)² -> x² + (2p − 2q)x + p² − q² = 0, roots a and −(... )
        rts = [a, (p * p - q * q) // a] if a else [a]
        return T(qh, "%s = %d" % (X, a), ["%s = %d" % (X, b), "%s = %d" % (X, c), "%s = %d or %s = %d" % (X, rts[0], X, rts[1]) if rts[1] != rts[0] else "%s = %d" % (X, a + 1)],
                 "%s + (%s)<sup>2</sup> = (%s)<sup>2</sup> gives %s. The roots are %d and %s; a length is positive, so <b>%s = %d</b>." % (
                     X2, lin(1, p), lin(1, q), eq0(1, 2 * p - 2 * q, p * p - q * q), a, num(rts[1]), X, a))
    s = r.randint(4, 14)
    w = r.choice([1, 2, 3])
    l = s + r.randint(2, 8)
    tot = (s + 2 * w) * (l + 2 * w)
    qh = "A rectangular pond is %d m by %d m. A path of width %s m is built all round it. The pond and path together cover %s m². Find %s." % (s, l, X, num(tot), X)
    return T(qh, "%s = %d" % (X, w), ["%s = %d" % (X, 2 * w), "%s = %d" % (X, w + 1), "%s = %d" % (X, w + 2)],
             "(%d + 2%s)(%d + 2%s) = %s. Expand: %s. One root is negative, so <b>%s = %d</b>." % (
                 s, X, l, X, num(tot), eq0(4, 2 * (s + l), s * l - tot), X, w))


# ------------------------------------------------------------ set 4: heights, profit and other formulae
def one_formula(r):
    kind = r.choice(["height", "height", "height2", "profit"])
    if kind == "height":
        t1, t2 = sorted(r.sample([1, 2, 3, 4, 5, 6], 2))
        u = 5 * (t1 + t2)
        h = 5 * t1 * t2
        qh = "A ball is thrown upwards. Its height after <i>t</i> seconds is %d<i>t</i> − 5<i>t</i><sup>2</sup> metres. At what times is it %d m above the ground?" % (u, h)
        right = "<i>t</i> = %d and <i>t</i> = %d" % (t1, t2)
        return T(qh, right, ["<i>t</i> = %d only" % t1, "<i>t</i> = %d and <i>t</i> = %d" % (5 * t1, 5 * t2), "<i>t</i> = %s and <i>t</i> = %s" % (num(-t1), num(-t2))],
                 "%d<i>t</i> − 5<i>t</i><sup>2</sup> = %d gives <i>t</i><sup>2</sup> − %d<i>t</i> + %d = 0, so (<i>t</i> − %d)(<i>t</i> − %d) = 0. Going up and coming down: <b>%s</b>." % (
                     u, h, t1 + t2, t1 * t2, t1, t2, right))
    if kind == "height2":
        u = r.choice([20, 25, 30, 35, 40])
        tland = u / 5
        qh = "A stone is thrown up from the ground. Its height after <i>t</i> seconds is %d<i>t</i> − 5<i>t</i><sup>2</sup> metres. After how many seconds does it land?" % u
        return T(qh, "%s s" % num(int(tland)), ["0 s", "%s s" % num(u), "%s s" % num(int(tland) // 2) if int(tland) % 2 == 0 else "%s s" % (d2(tland / 2))],
                 "It lands when the height is 0: %d<i>t</i> − 5<i>t</i><sup>2</sup> = 0, so 5<i>t</i>(%d − <i>t</i>) = 0. <i>t</i> = 0 is the start, so it lands after <b>%d s</b>." % (u, int(tland), int(tland)))
    a, b = sorted(r.sample(range(10, 80, 5), 2))
    qh = "A shop's daily profit is −<i>x</i><sup>2</sup> + %d<i>x</i> − %d dollars when it sells <i>x</i> items. For which numbers of items does it make no profit and no loss?" % (a + b, a * b)
    right = "%d and %d items" % (a, b)
    return T(qh, right, ["%d items only" % b, "%d and %d items" % (a + b, a * b) if a * b < 10000 else "%d items" % (a + b), "%s and %s items" % (num(-a), num(-b))],
             "Set the profit to 0: <i>x</i><sup>2</sup> − %d<i>x</i> + %d = 0, so (<i>x</i> − %d)(<i>x</i> − %d) = 0: <b>%s</b>." % (a + b, a * b, a, b, right))


# ------------------------------------------------------------ set 5: answers to 2 decimal places
def one_dp(r):
    kind = r.choice(["rect", "tri", "path", "num", "speed"])
    if kind == "rect":
        d = r.randint(1, 9)
        A = r.randint(15, 150)
        D = d * d + 4 * A
        if int(sqrt(D)) ** 2 == D:
            return None
        w = (-d + sqrt(D)) / 2
        if not ok_dp(w) or not ok_dp(w + d):
            return None
        qh = "A rectangle is %d cm longer than it is wide, and its area is %d cm². Find its width, correct to 2 decimal places." % (d, A)
        return T(qh, "%s cm" % d2(w), ["%s cm" % d2(w + d), "%s cm" % d2(sqrt(A)), "%s cm" % d2((-d - sqrt(D)) / 2)],
                 "%s = 0. <i>x</i> = (−%d ± √%d) ÷ 2. The width is positive: <b>%s cm</b>." % (quad(1, d, -A), d, D, d2(w)))
    if kind == "tri":
        h = r.randint(8, 30)
        d = r.randint(1, 6)
        # legs x and x + d, hypotenuse h: 2x² + 2dx + d² − h² = 0
        D = 4 * d * d - 8 * (d * d - h * h)
        x = (-2 * d + sqrt(D)) / 4
        if x <= 0 or int(sqrt(D)) ** 2 == D or not ok_dp(x):
            return None
        qh = "The two shorter sides of a right-angled triangle differ by %d cm. Its longest side is %d cm. Find the shortest side, correct to 2 decimal places." % (d, h)
        return T(qh, "%s cm" % d2(x), ["%s cm" % d2(x + d), "%s cm" % d2(h / sqrt(2)), "%s cm" % d2((h - d) / 2)],
                 "%s + (%s)<sup>2</sup> = %d gives %s. Use the formula and take the positive root: <b>%s cm</b>." % (X2, lin(1, d), h * h, eq0(2, 2 * d, d * d - h * h), d2(x)))
    if kind == "path":
        s, l = r.randint(5, 15), r.randint(8, 20)
        A = r.randint(20, 80)
        # path width x round s by l, path area A: (s+2x)(l+2x) − sl = A -> 4x² + 2(s+l)x − A = 0
        D = 4 * (s + l) ** 2 + 16 * A
        x = (-2 * (s + l) + sqrt(D)) / 8
        if int(sqrt(D)) ** 2 == D or not ok_dp(x):
            return None
        qh = "A garden is %d m by %d m. A path of the same width goes all round it, and the path has an area of %d m². Find the width of the path, correct to 2 decimal places." % (s, l, A)
        return T(qh, "%s m" % d2(x), ["%s m" % d2(2 * x), "%s m" % d2(A / (2 * (s + l))), "%s m" % d2(x + 1)],
                 "(%d + 2%s)(%d + 2%s) − %d = %d gives %s. The positive root is <b>%s m</b>." % (s, X, l, X, s * l, A, eq0(4, 2 * (s + l), -A), d2(x)))
    if kind == "num":
        k = r.randint(2, 9)
        t = r.randint(5, 60)
        D = k * k + 4 * t
        if int(sqrt(D)) ** 2 == D:
            return None
        x = (-k + sqrt(D)) / 2
        if not ok_dp(x):
            return None
        qh = "A positive number %s satisfies %s(%s + %d) = %d. Find %s, correct to 2 decimal places." % (X, X, X, k, t, X)
        return T(qh, d2(x), [d2(x + k), d2((-k - sqrt(D)) / 2), d2(t / k)],
                 "%s = 0. %s = (−%d ± √%d) ÷ 2. The positive root is <b>%s</b>." % (quad(1, k, -t), X, k, D, d2(x)))
    nm, he, his = P.next()
    d = r.choice([12, 15, 18, 20, 24, 30])
    k = r.choice([2, 3, 4])
    t = r.choice([1, 2])
    # d/x − d/(x + k) = t  ->  t x² + t k x − d k = 0
    D = (t * k) ** 2 + 4 * t * d * k
    x = (-t * k + sqrt(D)) / (2 * t)
    if int(sqrt(D)) ** 2 == D or not ok_dp(x):
        return None
    qh = "%s cycles %d km at <i>x</i> km/h. Cycling %d km/h faster would save %d hour%s. Find <i>x</i>, correct to 2 decimal places." % (nm, d, k, t, "" if t == 1 else "s")
    return T(qh, d2(x), [d2(x + k), d2(d / t), d2((-t * k - sqrt(D)) / (2 * t))],
             "%s ÷ <i>x</i> − %s ÷ (<i>x</i> + %d) = %d gives %s. The positive root is <b>%s</b>." % (num(d), num(d), k, t, eq0(t, t * k, -d * k), d2(x)))


def build():
    sets = [S("Forming the equation", collect(one_form, 20, R)),
            S("Number problems", collect(one_num, 20, R)),
            S("Rectangles, triangles and paths", collect(one_geo, 20, R)),
            S("Heights and profits", collect(one_formula, 20, R)),
            S("Problems with answers to 2 decimal places", collect(one_dp, 20, R))]
    body = lesson(
        "<ol><li>Let the unknown be <i>x</i> and write the other quantities in terms of <i>x</i>.</li>"
        "<li>Form an equation, expand and make one side <b>0</b>.</li>"
        "<li>Solve by factorising, or by the formula if it does not factorise.</li>"
        "<li><b>Check</b> each root in the problem. Reject a negative length, time or number of people, then answer the question asked.</li></ol>",
        [("A rectangle is 3 cm longer than it is wide. Its area is 40 cm². Find its length.", ["x(x + 3) = 40, so x² + 3x − 40 = 0", "(x − 5)(x + 8) = 0, so x = 5 (reject −8)"], "8 cm"),
         ("The sides of a right-angled triangle are x, x + 7 and x + 8 cm. Find x.", ["x² + (x + 7)² = (x + 8)²", "x² − 2x − 15 = 0, so (x − 5)(x + 3) = 0"], "x = 5")],
        ["Forgetting to make one side 0 before factorising.",
         "Keeping the negative root when the answer is a length or a time.",
         "Giving <i>x</i> when the question asks for the length, which may be <i>x</i> + 3.",
         "Squaring only part of a bracket: (x + 7)² = x² + 14x + 49, not x² + 49."])
    faq = [("How do I form a quadratic equation from a word problem?", "Choose x for one unknown, write the others in terms of x, and use the fact given (area, product, Pythagoras' theorem or a formula) to write an equation. Then make one side 0."),
           ("What do I do with the negative root?", "Check it in the problem. A length, time, speed or number of objects cannot be negative, so reject it and say why."),
           ("When should I use the formula instead of factorising?", "When the quadratic does not factorise, or when the question asks for answers correct to 2 decimal places or 3 significant figures."),
           ("Why does a thrown ball reach the same height twice?", "It passes that height once going up and once coming down, so the quadratic has two positive roots.")]
    make(3, "quadratic-equation-word-problems", 5, "N7",
         "Quadratic Equation Word Problems",
         "", "Quadratic word problems", "",
         "Free Secondary 3 maths worksheets on quadratic equation word problems: forming the equation, number problems, rectangles, paths, right-angled triangles, heights and answers to 2 decimal places. 100 questions with answers.",
         "Form the equation, make one side 0, solve, then check each root makes sense.",
         "Reject negative lengths and times, and answer the exact question asked.",
         body, faq, sets, R)


if __name__ == "__main__":
    build()
