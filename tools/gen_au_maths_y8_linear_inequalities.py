# -*- coding: utf-8 -*-
"""
AU Year 8 Maths: Linear Inequalities (Australian Curriculum v9.0: AC9M8A02)
  python3 tools/gen_au_maths_y8_linear_inequalities.py
Inequality symbols and number lines, listing integers that satisfy an inequality, solving one- and two-step
linear inequalities, inequalities with negative coefficients and brackets, and problems.
Wrong answers come from real mistakes: open and closed circles mixed up, including the end that should be
excluded, not reversing the sign when dividing by a negative, and writing an equation instead of an inequality.
"""
import random
from fractions import Fraction as F
from au_hs import num, mcq, B, S, make, lesson, collect, T, fr, expr, svg_wrap, line, text, fig, GREEN, INK, RED, MINUS

R = random.Random(80701)
X = "<i>x</i>"
LT, LE, GT, GE = "&lt;", "≤", "&gt;", "≥"
FLIP = {LT: GT, GT: LT, LE: GE, GE: LE}


def sol(v):
    v = F(v)
    return num(v) if v.denominator == 1 else (MINUS if v < 0 else "") + fr(abs(v.numerator), v.denominator)


def nline(lo, hi, marks):
    """marks: list of (value, closed, direction) where direction is -1 (left), +1 (right) or 0 (segment end)."""
    u = 34
    x0 = 24
    W = x0 * 2 + (hi - lo) * u
    Xp = lambda v: x0 + (v - lo) * u
    y = 44
    s = [line(x0 - 12, y, W - x0 + 12, y, INK, 2)]
    for v in range(lo, hi + 1):
        s.append(line(Xp(v), y - 6, Xp(v), y + 6, INK, 1.5))
        s.append(text(Xp(v), y + 24, num(v), 13, weight=400))
    if len(marks) == 2:
        (a, ca, _), (b, cb, _) = marks
        s.append(line(Xp(a), y - 16, Xp(b), y - 16, RED, 4))
        for v, c in ((a, ca), (b, cb)):
            s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (Xp(v), y - 16, Xp(v), y - 16, RED))
            s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s' stroke='%s' stroke-width='2.5'/>" % (Xp(v), y - 16, RED if c else "#fff", RED))
    else:
        a, c, d = marks[0]
        end = Xp(hi) + 10 if d > 0 else Xp(lo) - 10
        s.append(line(Xp(a), y - 16, end, y - 16, RED, 4))
        s.append("<path d='M%.1f %d l%d -7 l0 14 Z' fill='%s'/>" % (end + (8 if d > 0 else -8), y - 16, -10 if d > 0 else 10, RED))
        s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s' stroke='%s' stroke-width='2.5'/>" % (Xp(a), y - 16, RED if c else "#fff", RED))
    return svg_wrap(W, 80, "".join(s), "number line showing an inequality")


# ------------------------------------------------------------ set 1: number lines and notation
def one_nl(r):
    if r.random() < 0.55:
        a = r.randint(-4, 4)
        closed = r.random() < 0.5
        d = r.choice([-1, 1])
        sym = (GE if closed else GT) if d > 0 else (LE if closed else LT)
        right = "%s %s %s" % (X, sym, num(a))
        others = [GE, GT, LE, LT]
        wr = ["%s %s %s" % (X, o, num(a)) for o in others if o != sym][:2] + ["%s = %s" % (X, num(a))]
        q = "Which inequality is shown on the number line?%s" % fig(nline(a - 4, a + 4, [(a, closed, d)]))
        e = "The circle is %s, so %s is %s included. The arrow points %s. So <b>%s</b>." % (
            "filled" if closed else "open", num(a), "" if closed else "not", "right (bigger)" if d > 0 else "left (smaller)", right)
        return T(q, right, wr, e)
    a = r.randint(-4, 1)
    b = a + r.randint(2, 5)
    ca, cb = r.random() < 0.5, r.random() < 0.5
    s1, s2 = (LE if ca else LT), (LE if cb else LT)
    right = "%s %s %s %s %s" % (num(a), s1, X, s2, num(b))
    alt1 = "%s %s %s %s %s" % (num(a), LT if ca else LE, X, s2, num(b))
    alt2 = "%s %s %s %s %s" % (num(a), s1, X, LT if cb else LE, num(b))
    alt3 = "%s %s %s %s %s" % (num(a), GT if not ca else GE, X, GT if not cb else GE, num(b))
    q = "Which inequality is shown on the number line?%s" % fig(nline(a - 2, b + 2, [(a, ca, 0), (b, cb, 0)]))
    e = "A filled circle means the number is included (≤); an open circle means it is not (&lt;). So <b>%s</b>." % right
    return T(q, right, [alt1, alt2, alt3], e)


# ------------------------------------------------------------ set 2: listing integers
def one_list(r):
    a = r.randint(-5, 2)
    b = a + r.randint(2, 5)
    ca, cb = r.random() < 0.5, r.random() < 0.5
    lo = a if ca else a + 1
    hi = b if cb else b - 1
    vals = list(range(lo, hi + 1))
    if len(vals) < 2:
        return None
    q = "List the integers that satisfy %s." % (B("%s %s %s %s %s" % (num(a), LE if ca else LT, "<i>n</i>", LE if cb else LT, num(b))))
    right = ", ".join(num(v) for v in vals)
    wr = [", ".join(num(v) for v in range(a, b + 1)), ", ".join(num(v) for v in range(a + 1, b)) if ca or cb else ", ".join(num(v) for v in range(a, b)),
          ", ".join(num(v) for v in range(lo, hi + 2)), ", ".join(num(v) for v in range(lo - 1, hi + 1))]
    e = "%s %s included and %s %s included. The integers are <b>%s</b>." % (num(a), "is" if ca else "is not", num(b), "is" if cb else "is not", right)
    return T(q, right, [w for w in wr if w != right][:3], e)


# ------------------------------------------------------------ set 3: solving
def one_solve(r):
    v = r.choice([X, "<i>n</i>", "<i>y</i>", "<i>t</i>"])
    sym = r.choice([LT, LE, GT, GE])
    a = r.randint(2, 9)
    b = r.randint(-10, 15)
    s = r.randint(-5, 10)
    c = a * s + b
    if b == 0:
        return None
    q = "Solve %s." % B("%s %s %s" % (expr([(a, v), (b, "")]), sym, num(c)))
    right = "%s %s %s" % (v, sym, num(s))
    wr = ["%s %s %s" % (v, FLIP[sym], num(s)), "%s %s %s" % (v, sym, sol(F(c + b, a))) if F(c + b, a) != s else "%s %s %s" % (v, sym, num(s + 1)),
          "%s = %s" % (v, num(s)), "%s %s %s" % (v, sym, sol(F(c, a) - b))]
    e = "Solve like an equation: %s %s, %s. Divide by %d: <b>%s</b>." % (
        "subtract %d" % b if b > 0 else "add %d" % -b, "to get %s %s %s" % (expr([(a, v)]), sym, num(c - b)), "keep the same sign", a, right)
    return T(q, right, [w for w in wr if w != right][:3], e)


# ------------------------------------------------------------ set 4: negative coefficients, brackets, both sides
def one_hard(r):
    v = X
    kind = r.randint(0, 2)
    sym = r.choice([LT, LE, GT, GE])
    if kind == 0:
        a = r.randint(2, 6)
        b = r.randint(-8, 12)
        s = r.randint(-4, 6)
        c = b - a * s
        if b == 0:
            return None
        q = "Solve %s." % B("%s %s %s" % (expr([(b, ""), (-a, v)]), sym, num(c)))
        right = "%s %s %s" % (v, FLIP[sym], num(s))
        wr = ["%s %s %s" % (v, sym, num(s)), "%s %s %s" % (v, FLIP[sym], num(-s)) if s else "%s %s %s" % (v, FLIP[sym], num(1)), "%s %s %s" % (v, sym, num(-s)) if s else "%s %s 1" % (v, sym)]
        e = "%s: %s%d%s %s %s. Dividing by a negative number <b>reverses the sign</b>: <b>%s</b>." % (
            ("Subtract %d" % b) if b > 0 else ("Add %d" % -b), MINUS, a, v, sym, num(c - b), right)
        if len(set(wr)) < 3 or right in wr:
            return None
        return T(q, right, wr, e)
    if kind == 1:
        k, b = r.randint(2, 5), r.randint(-5, 6)
        s = r.randint(-3, 8)
        c = k * (s + b)
        if b == 0:
            return None
        q = "Solve %s." % B("%d(%s) %s %s" % (k, expr([(1, v), (b, "")]), sym, num(c)))
        right = "%s %s %s" % (v, sym, num(s))
        wr = ["%s %s %s" % (v, sym, sol(F(c - b, k))) if F(c - b, k) != s else "%s %s %s" % (v, sym, num(s + 2)), "%s %s %s" % (v, FLIP[sym], num(s)), "%s %s %s" % (v, sym, num(c - b))]
        e = "Divide by %d: %s %s %s. Then <b>%s</b>." % (k, expr([(1, v), (b, "")]), sym, num(c // k), right)
        if len(set(wr)) < 3 or right in wr:
            return None
        return T(q, right, wr, e)
    a, c2 = r.randint(3, 8), r.randint(1, 2)
    if a <= c2:
        return None
    b, d = r.randint(-6, 8), r.randint(-6, 15)
    ans = F(d - b, a - c2)
    if ans.denominator != 1:
        return None
    q = "Solve %s." % B("%s %s %s" % (expr([(a, v), (b, "")]), sym, expr([(c2, v), (d, "")])))
    right = "%s %s %s" % (v, sym, num(ans))
    wr = ["%s %s %s" % (v, FLIP[sym], num(ans)), "%s %s %s" % (v, sym, sol(F(d - b, a + c2))), "%s %s %s" % (v, sym, sol(F(d + b, a - c2)))]
    e = "Subtract %s from both sides, then solve: %s %s %s, so <b>%s</b>." % (expr([(c2, v)]), expr([(a - c2, v)]), sym, num(d - b), right)
    if len(set(wr)) < 3 or right in wr:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    data = [
        ("A lift can carry at most 8 people. Which inequality shows the number of people <i>p</i>?", "<i>p</i> ≤ 8", ["<i>p</i> &lt; 8", "<i>p</i> ≥ 8", "<i>p</i> &gt; 8"], "“At most 8” means 8 or fewer: <b><i>p</i> ≤ 8</b>."),
        ("You must be over 12 to go on a ride at the Royal Easter Show. Which inequality shows the age <i>a</i>?", "<i>a</i> &gt; 12", ["<i>a</i> ≥ 12", "<i>a</i> &lt; 12", "<i>a</i> ≤ 12"], "“Over 12” does not include 12: <b><i>a</i> &gt; 12</b>."),
        ("Ava has $20. Movie tickets cost $3 each at a school film night. What is the greatest number of tickets she can buy?", "6", ["7", "6.67", "60"], "3<i>t</i> ≤ 20, so <i>t</i> ≤ 6.67. She can buy <b>6</b> tickets."),
        ("A taxi costs $4 plus $2 per kilometre. Leo has $15. What is the greatest whole number of kilometres he can travel?", "5", ["6", "5.5", "9"], "4 + 2<i>m</i> ≤ 15, so <i>m</i> ≤ 5.5. The greatest whole number is <b>5</b>."),
        ("Which value of <i>x</i> satisfies 3<i>x</i> − 1 &gt; 11?", "5", ["4", "3", "0"], "3<i>x</i> &gt; 12, so <i>x</i> &gt; 4. Only <b>5</b> works (4 is not included)."),
        ("What is the smallest integer that satisfies 2<i>x</i> + 5 ≥ 12?", "4", ["3", "3.5", "7"], "2<i>x</i> ≥ 7, so <i>x</i> ≥ 3.5. The smallest integer is <b>4</b>."),
        ("What is the largest integer that satisfies 5<i>n</i> &lt; 32?", "6", ["7", "6.4", "5"], "<i>n</i> &lt; 6.4, so the largest integer is <b>6</b>."),
        ("The perimeter of a square with side <i>s</i> cm must be less than 30 cm. Which inequality is correct?", "<i>s</i> &lt; 7.5", ["<i>s</i> &lt; 30", "<i>s</i> ≤ 7.5", "<i>s</i> &gt; 7.5"], "4<i>s</i> &lt; 30, so <b><i>s</i> &lt; 7.5</b>."),
        ("Which number is NOT a solution of <i>x</i> ≥ −2?", "−3", ["−2", "0", "5"], "<i>x</i> must be −2 or more. <b>−3</b> is less than −2."),
        ("Solve 4 ≤ 2<i>x</i> &lt; 10.", "2 ≤ <i>x</i> &lt; 5", ["4 ≤ <i>x</i> &lt; 10", "2 &lt; <i>x</i> ≤ 5", "8 ≤ <i>x</i> &lt; 20"], "Divide every part by 2: <b>2 ≤ <i>x</i> &lt; 5</b>."),
        ("Solve −3 &lt; <i>x</i> + 2 ≤ 6.", "−5 &lt; <i>x</i> ≤ 4", ["−1 &lt; <i>x</i> ≤ 8", "−5 ≤ <i>x</i> &lt; 4", "−3 &lt; <i>x</i> ≤ 4"], "Subtract 2 from every part: <b>−5 &lt; <i>x</i> ≤ 4</b>."),
        ("How many integers satisfy −2 ≤ <i>n</i> &lt; 3?", "5", ["4", "6", "3"], "−2, −1, 0, 1, 2: <b>5</b> integers."),
        ("Mia says −<i>x</i> &gt; 4 means <i>x</i> &gt; −4. What is the correct answer?", "<i>x</i> &lt; −4", ["<i>x</i> &gt; −4", "<i>x</i> &gt; 4", "<i>x</i> &lt; 4"], "Multiplying both sides by −1 reverses the sign: <b><i>x</i> &lt; −4</b>."),
        ("A bus holds 52 people. 4 teachers and some students go on an excursion. Which inequality shows the number of students <i>p</i>?", "<i>p</i> ≤ 48", ["<i>p</i> ≤ 52", "<i>p</i> &lt; 48", "<i>p</i> ≥ 48"], "<i>p</i> + 4 ≤ 52, so <b><i>p</i> ≤ 48</b>."),
        ("Which inequality has the solution set shown by 3 &lt; <i>x</i>?", "<i>x</i> &gt; 3", ["<i>x</i> &lt; 3", "<i>x</i> ≥ 3", "<i>x</i> ≤ 3"], "3 &lt; <i>x</i> means <i>x</i> is bigger than 3: <b><i>x</i> &gt; 3</b>."),
        ("<i>n</i> is an integer with 2<i>n</i> &gt; 7 and <i>n</i> ≤ 6. Which list shows all the possible values?", "4, 5, 6", ["3, 4, 5, 6", "4, 5", "3.5, 4, 5, 6"], "2<i>n</i> &gt; 7 means <i>n</i> &gt; 3.5. With <i>n</i> ≤ 6: <b>4, 5, 6</b>."),
        ("A rectangle has length 8 cm and width <i>w</i> cm. Its area must be at least 40 cm². Which inequality is correct?", "<i>w</i> ≥ 5", ["<i>w</i> &gt; 5", "<i>w</i> ≤ 5", "<i>w</i> ≥ 32"], "“At least” means ≥: 8<i>w</i> ≥ 40, so <b><i>w</i> ≥ 5</b>."),
        ("Which symbol means “is greater than or equal to”?", "≥", ["&gt;", "≤", "≠"], "<b>≥</b> means greater than or equal to."),
        ("Solve 10 − 3<i>x</i> ≥ 1.", "<i>x</i> ≤ 3", ["<i>x</i> ≥ 3", "<i>x</i> ≤ −3", "<i>x</i> ≥ −3"], "−3<i>x</i> ≥ −9. Dividing by −3 reverses the sign: <b><i>x</i> ≤ 3</b>."),
        ("Which of these is the solution of 6 &gt; <i>x</i> − 2?", "<i>x</i> &lt; 8", ["<i>x</i> &gt; 8", "<i>x</i> &lt; 4", "<i>x</i> &gt; 4"], "Add 2: 8 &gt; <i>x</i>, which means <b><i>x</i> &lt; 8</b>."),
    ]
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p>&lt; less than, &gt; greater than, ≤ less than or equal to, ≥ greater than or equal to. On a number line an "
        "<b>open circle</b> means the number is not included and a <b>filled circle</b> means it is.</p>"
        "<p>Solve an inequality like an equation, but if you <b>multiply or divide by a negative number, reverse the sign</b>.</p>"
        + fig(nline(-2, 6, [(2, False, 1)])),
        [("Solve 3<i>x</i> + 4 &lt; 19.", ["Subtract 4: 3<i>x</i> &lt; 15.", "Divide by 3."], "<i>x</i> &lt; 5"),
         ("Solve 7 − 2<i>x</i> ≥ 1.", ["Subtract 7: −2<i>x</i> ≥ −6.", "Divide by −2 and reverse the sign."], "<i>x</i> ≤ 3"),
         ("List the integers with −2 &lt; <i>n</i> ≤ 3.", ["−2 is not included; 3 is."], "−1, 0, 1, 2, 3")],
        ["Mixing up open and filled circles.",
         "Including an end that is not allowed: −2 &lt; <i>n</i> does not include −2.",
         "Forgetting to reverse the sign when dividing by a negative number.",
         "Writing = instead of an inequality sign in the answer."])


def main():
    sets = [S("Inequalities on a number line", collect(one_nl, 20, R)),
            S("Listing integers", collect(one_list, 20, R)),
            S("Solving inequalities", collect(one_solve, 20, R)),
            S("Negatives, brackets and both sides", collect(one_hard, 20, R)),
            S("Inequalities in problems", problems())]
    make(8, "linear-inequalities", 7, "AC9M8A02",
         "Linear Inequalities: Number Lines, Integer Solutions and Solving",
         "Year 8 Inequalities Worksheets: Number Lines and Solving Linear Inequalities (Free, Answer Key)",
         "Linear inequalities",
         "graph linear relations on the Cartesian plane using digital tools where appropriate; solve linear equations and "
         "one-variable inequalities using graphical and algebraic techniques; verify solutions by substitution",
         "Free Year 8 maths worksheets on linear inequalities for the Australian Curriculum (AC9M8A02): inequality notation, "
         "number lines, listing integer solutions, solving one-variable inequalities and reversing the sign. 100 questions with an answer key.",
         "Solve an inequality like an equation. If you divide by a negative, reverse the sign.",
         "On a number line, an open circle means not included (< or >), a filled circle means included (≤ or ≥).",
         body(),
         [("What is the difference between < and ≤?", "x < 5 means x is less than 5, so 5 is not included. x ≤ 5 includes 5."),
          ("Why do I reverse the sign when dividing by a negative?", "Multiplying by a negative flips the order of numbers: 2 < 3 but −2 > −3. So the inequality sign must flip too."),
          ("How do I show an inequality on a number line?", "Draw a circle at the number, filled if it is included and open if not, and a line or arrow over all the values that work."),
          ("What does “at least” mean?", "At least means greater than or equal to (≥). “At most” means less than or equal to (≤).")],
         sets, R)


if __name__ == "__main__":
    main()
