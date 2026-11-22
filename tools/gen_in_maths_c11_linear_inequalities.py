# -*- coding: utf-8 -*-
"""
India Class 11 Maths, NCERT Chapter 5: Linear Inequalities (CBSE Unit II Algebra)
  python3 tools/gen_in_maths_c11_linear_inequalities.py
Solving linear inequalities in one variable, unknowns on both sides, writing the solution as an interval, solutions
in N or Z, showing the solution on the number line, double inequalities, and word problems (own makers and SG
Secondary 3 makers).
Wrong answers come from real mistakes: not reversing the sign when multiplying or dividing by a negative number,
using a closed end for a strict inequality, and including numbers that are not natural or not integers.
"""
import random
from fractions import Fraction as F
from in_sr import U, T2, use, X
from in_common import num, fv
import gen_sg_maths_s3_simultaneous_linear_inequalities as sgi

R = random.Random(911105)
both = use(sgi, "one_and", R)
pair = use(sgi, "one_pair", R)
prob = use(sgi, "one_prob", R)
FLIP = {"&lt;": "&gt;", "&gt;": "&lt;", "≤": "≥", "≥": "≤"}
SIGNS = ["&lt;", "&gt;", "≤", "≥"]


def lin(a, b):
    s = ("" if a == 1 else ("−" if a == -1 else num(a))) + X
    return s + ("" if b == 0 else (" + %d" % b if b > 0 else " − %d" % -b))


def interval(sg, v):
    v = fv(v)
    return {"&lt;": "(−∞, %s)" % v, "≤": "(−∞, %s]" % v, "&gt;": "(%s, ∞)" % v, "≥": "[%s, ∞)" % v}[sg]


def one_solve(r):
    a = r.choice([k for k in range(-7, 8) if k not in (0, 1)])
    x0 = r.randint(-8, 8)
    b = r.randint(-12, 12)
    sg = r.choice(SIGNS)
    c = a * x0 + b
    fin = FLIP[sg] if a < 0 else sg
    right = "%s %s %s" % (X, fin, num(x0))
    return T2("Solve %s %s %s for real %s." % (lin(a, b), sg, num(c), X), right, ["%s %s %s" % (X, sg if a < 0 else FLIP[sg], num(x0)), "%s %s %s" % (X, fin, num(-x0)) if x0 else "%s %s 1" % (X, fin),
                                                                             "%s %s %s" % (X, fin, fv(F(c + b, a)))],
              "%s %s %s, then divide by %s%s: <b>%s</b>." % (lin(a, 0), sg, num(c - b), num(a), " and reverse the sign because it is negative" if a < 0 else "", right))


def one_sides(r):
    a, c = r.sample([k for k in range(-6, 9) if k], 2)
    x0 = r.randint(-6, 6)
    b = r.randint(-10, 10)
    d = (a - c) * x0 + b
    sg = r.choice(SIGNS)
    k = a - c
    fin = FLIP[sg] if k < 0 else sg
    right = interval(fin, x0)
    return T2("Solve %s %s %s. Write the solution as an interval." % (lin(a, b), sg, lin(c, d)), right,
              [interval(FLIP[fin], x0), interval({"&lt;": "≤", "≤": "&lt;", "&gt;": "≥", "≥": "&gt;"}[fin], x0), interval(fin, -x0) if x0 else interval(fin, 1)],
              "Collect %s on one side: %s %s %s, so %s %s %s. The solution set is <b>%s</b>." % (X, lin(k, 0), sg, num(d - b), X, fin, num(x0), right))


def one_set(r):
    a = r.randint(2, 6)
    x0 = r.randint(2, 7)
    b = r.randint(-9, 9)
    dom = r.choice(["N", "Z"])
    sg = r.choice(["&lt;", "≤"])
    c = a * x0 + b
    top = x0 if sg == "≤" else x0 - 1
    if dom == "N":
        vals = list(range(1, top + 1))
        right = "{" + ", ".join(map(str, vals)) + "}"
        return T2("Solve %s %s %d when %s is a natural number." % (lin(a, b), sg, c, X), right,
                  ["{" + ", ".join(map(str, range(0, top + 1))) + "}", "{" + ", ".join(map(str, range(1, top + 2))) + "}", "{" + ", ".join(map(str, range(1, top))) + "}" if top > 1 else "φ"],
                  "%s %s %d. The natural numbers that fit are <b>%s</b>." % (X, sg, x0, right))
    lo = r.randint(-5, 0)
    return T2("How many integers %s satisfy %d &lt; %s %s %d?" % (X, a * lo + b, lin(a, b), sg, c), str(top - lo),
              [str(top - lo + 1), str(top - lo - 1), str(x0 - lo + (0 if sg == "≤" else 1))],
              "Dividing through: %d &lt; %s %s %d, so %s = %d, …, %d: <b>%d</b> integers." % (lo, X, sg, x0, X, lo + 1, top, top - lo))


def one_line(r):
    v = r.randint(-6, 6)
    sg = r.choice(SIGNS)
    dot = "an open (hollow) circle" if sg in ("&lt;", "&gt;") else "a filled circle"
    side = "left" if sg in ("&lt;", "≤") else "right"
    right = "%s at %s, shaded to the %s" % (dot[0].upper() + dot[1:], num(v), side)
    o = lambda d, s_: "%s at %s, shaded to the %s" % (d, num(v), s_)
    other_dot = "A filled circle" if "open" in dot else "An open (hollow) circle"
    other_side = "right" if side == "left" else "left"
    return T2("How is %s %s %s shown on the number line?" % (X, sg, num(v)), right, [o(other_dot, side), o(dot[0].upper() + dot[1:], other_side), o(other_dot, other_side)],
              "%s means %s %s is %s included, so use %s; the solutions are to the %s: <b>%s</b>." % (
                  sg, num(v), "" if "filled" in dot else "not", "is" if "filled" in dot else "", dot, side, right) if False else
              "%s %s is %s the solution, so use %s, and shade to the %s: <b>%s</b>." % (X + " = " + num(v), "", "part of" if "filled" in dot else "not part of", dot, side, right))


def one_word(r):
    k = r.choice(["temp", "marks", "odd", "sum"])
    if k == "temp":
        lo, hi = r.choice([(68, 77), (95, 104), (59, 86), (50, 95), (77, 86)])
        clo, chi = (lo - 32) * 5 // 9, (hi - 32) * 5 // 9
        return T2("A solution must be kept between %d°F and %d°F. Using F = (9/5)C + 32, what is the range in Celsius?" % (lo, hi), "%d &lt; C &lt; %d" % (clo, chi),
                  ["%d &lt; C &lt; %d" % (lo - 32, hi - 32), "%d &lt; C &lt; %d" % (clo + 5, chi + 5), "%d &lt; C &lt; %d" % (lo * 5 // 9, hi * 5 // 9)],
                  "%d &lt; (9/5)C + 32 &lt; %d gives %d &lt; (9/5)C &lt; %d, so <b>%d &lt; C &lt; %d</b>." % (lo, hi, lo - 32, hi - 32, clo, chi))
    if k == "marks":
        m1, m2 = r.randint(55, 90), r.randint(55, 90)
        need = r.choice([60, 65, 70, 75, 80])
        x = 3 * need - m1 - m2
        if not 0 < x <= 100:
            return None
        return T2("A student scored %d and %d in two unit tests. What is the least score in the third test for an average of at least %d?" % (m1, m2, need), str(x),
                  [str(need), str(x - 1), str(2 * need - m1 - m2 + need // 2)],
                  "(%d + %d + %s) ÷ 3 ≥ %d, so %s ≥ %d − %d = <b>%d</b>." % (m1, m2, X, need, X, 3 * need, m1 + m2, x))
    if k == "odd":
        n = r.choice([10, 12, 14, 20, 30])
        s_ = r.choice([20, 24, 30, 40, 50])
        x = (s_ - 2) // 2
        lo = x if x % 2 == 1 else x + 1
        if lo > n * 2:
            return None
        pairs = [(o, o + 2) for o in range(1, 2 * n, 2) if o > n and o + o + 2 < s_]
        if not pairs:
            return None
        right = ", ".join("(%d, %d)" % p for p in pairs)
        return T2("Find all pairs of consecutive odd numbers, both greater than %d, whose sum is less than %d." % (n, s_), right,
                  [", ".join("(%d, %d)" % p for p in pairs + [(pairs[-1][0] + 2, pairs[-1][1] + 2)]), ", ".join("(%d, %d)" % (a - 1, b - 1) for a, b in pairs), "(%d, %d)" % (n, n + 2)],
                  "Let the numbers be %s and %s + 2: %s &gt; %d and 2%s + 2 &lt; %d. The pairs are <b>%s</b>." % (X, X, X, n, X, s_, right))
    w, l = r.randint(3, 12), None
    l = w + r.randint(2, 8)
    p = 2 * (w + l)
    return T2("The length of a rectangle is %d cm more than its width. Its perimeter is at least %d cm. What is the least width?" % (l - w, p), "%d cm" % w,
              ["%d cm" % l, "%d cm" % (p // 4), "%d cm" % (w + 1)], "2(%s + %s + %d) ≥ %d, so 4%s ≥ %d and %s ≥ <b>%d cm</b>." % (X, X, l - w, p, X, p - 2 * (l - w), X, w))


U(11, 5, "linear-inequalities", 5, "II", "Linear Inequalities: Solving and Showing Solutions on the Number Line", "linear inequalities",
  "Linear inequalities; algebraic solutions of linear inequalities in one variable and their representation on the number line (summary of the CBSE syllabus)",
  "Class 11 Linear Inequalities worksheet (NCERT Chapter 5): solving in one variable, interval answers, solutions in N and Z, the number line, double inequalities and word problems. 100 questions with answers.",
  "Multiplying or dividing by a negative number reverses the sign.", "Strict signs (&lt;, &gt;) leave the end point out.",
  "<ul><li>You may add or subtract the same number on both sides.</li><li>You may multiply or divide both sides by a positive number; for a <b>negative</b> number, reverse the sign.</li>"
  "<li>On the number line, &lt; and &gt; use an open circle; ≤ and ≥ use a filled circle.</li><li>Interval form: <i>x</i> &lt; 3 is (−∞, 3); <i>x</i> ≥ 3 is [3, ∞).</li></ul>",
  [("Solve 3 − 2<i>x</i> ≤ 9.", ["−2<i>x</i> ≤ 6", "Divide by −2 and reverse: <i>x</i> ≥ −3"], "[−3, ∞)")],
  ["Not reversing the sign when dividing by a negative number.", "Using [ ] for a strict inequality.", "Including 0 among the natural numbers."],
  [("Why does the sign reverse?", "Multiplying by a negative number reverses the order: 2 &lt; 3 but −2 &gt; −3."), ("Is 0 a natural number?", "No. In NCERT, N = {1, 2, 3, …}.")],
  [("Solving inequalities", [(one_solve, 20)]),
   ("Unknowns on both sides", [(one_sides, 14), (one_line, 6)]),
   ("Solutions in N and Z", [(one_set, 12), (pair, 8)]),
   ("Double inequalities", [(both, 20)]),
   ("Word problems", [(one_word, 12), (prob, 8)])], 911105)
