# -*- coding: utf-8 -*-
"""
US Algebra 1: Absolute Value Equations and Inequalities (Common Core A-CED.A.1, A-REI.B.3)
  python3 tools/gen_us_math_a1_absolute_value_equations_and_inequalities.py
Solving |x + a| = k, multi-step absolute value equations (isolate first), equations with no solution,
"less than" absolute value inequalities (and), "greater than" absolute value inequalities (or), and
tolerance and distance word problems.
Wrong answers come from real mistakes: giving only one solution, splitting before isolating the absolute
value, solving |x| = −3 as x = ±3, and turning |x| < k into an "or" inequality.
"""
import random
from fractions import Fraction as F
from us_hs import num, B, S, make, lesson, collect, T, expr, fr, MINUS

R = random.Random(90401)
X = "<i>x</i>"
LT, LE, GT, GE = "&lt;", "≤", "&gt;", "≥"
NONE = "No solution"


def sol(v):
    v = F(v)
    return num(v) if v.denominator == 1 else (MINUS if v < 0 else "") + fr(abs(v.numerator), v.denominator)


def ab(a, b):
    return "|%s|" % expr([(a, X), (b, "")])


def pair(p, q):
    p, q = sorted([F(p), F(q)])
    return "%s = %s or %s = %s" % (X, sol(p), X, sol(q))


# ------------------------------------------------------------ set 1: |ax + b| = k
def one_basic(r):
    a = r.choice([1, 1, 2, 3, 4])
    b = r.randint(-9, 9)
    k = r.randint(-3, 12)
    q = "Solve %s." % B("%s = %s" % (ab(a, b), num(k)))
    if k < 0:
        return T(q, NONE, [pair(F(-k - b, a), F(k - b, a)), "%s = %s" % (X, sol(F(k - b, a))), "%s = 0" % X],
                 "An absolute value is a distance, so it can never be negative: <b>no solution</b>.")
    if k == 0:
        if b == 0:
            return None
        right = "%s = %s" % (X, sol(F(-b, a)))
        return T(q, right, [pair(F(-b, a), F(b, a)), NONE, "%s = %s" % (X, sol(F(b, a)))], "Only zero has absolute value 0, so %s = 0 and <b>%s</b>." % (expr([(a, X), (b, "")]), right))
    p1, p2 = F(k - b, a), F(-k - b, a)
    right = pair(p1, p2)
    wr = ["%s = %s" % (X, sol(p1)), pair(F(k + b, a), F(-k + b, a)) if b else pair(p1, -p1 + 1), pair(F(k, a) - b, F(-k, a) - b) if a != 1 else pair(k + b, -k + b)]
    e = "Split into two equations: %s = %s or %s = %s%s. So <b>%s</b>." % (
        expr([(a, X), (b, "")]), num(k), expr([(a, X), (b, "")]), MINUS, num(k), right)
    wr = [w for w in dict.fromkeys(wr) if w != right]
    if len(wr) < 3:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 2: multi-step
def one_multi(r):
    c = r.choice([2, 3, 4, 5, -2])
    a = r.choice([1, 2, 3])
    b = r.randint(-8, 8)
    d = r.randint(-9, 9)
    k = r.randint(-2, 8)
    if d == 0 or b == 0:
        return None
    rhs = c * k + d
    q = "Solve %s." % B("%s%s %s %s = %s" % (num(c) if c != 1 else "", ab(a, b), "+" if d > 0 else MINUS, num(abs(d)), num(rhs)))
    iso = "%s = %s" % (ab(a, b), num(k))
    if k < 0:
        e = "Isolate the absolute value first: %s. An absolute value cannot be negative: <b>no solution</b>." % iso
        return T(q, NONE, [pair(F(-k - b, a), F(k - b, a)), pair(F(rhs - b, a), F(-rhs - b, a)), "%s = %s" % (X, sol(F(k - b, a)))], e)
    if k == 0:
        return None
    p1, p2 = F(k - b, a), F(-k - b, a)
    right = pair(p1, p2)
    split_first = pair(F(rhs - d - b, a), F(-(rhs - d) - b, a))      # forgot to divide by c
    wr = [split_first, "%s = %s" % (X, sol(p1)), pair(F(rhs - b, a), F(-rhs - b, a))]
    wr = [w for w in dict.fromkeys(wr) if w != right]
    if len(wr) < 3:
        return None
    e = "Isolate the absolute value first: %s %s, then divide by %s: %s. Split: %s = ±%s. So <b>%s</b>." % (
        "subtract" if d > 0 else "add", num(abs(d)), num(c), iso, expr([(a, X), (b, "")]), num(k), right)
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 3: less than (and)
def one_less(r):
    a = r.choice([1, 1, 2, 3])
    b = r.randint(-8, 8)
    k = r.randint(1, 12)
    sym = r.choice([LT, LE])
    lo, hi = F(-k - b, a), F(k - b, a)
    q = "Solve %s." % B("%s %s %s" % (ab(a, b), sym, num(k)))
    right = "%s %s %s %s %s" % (sol(lo), sym, X, sym, sol(hi))
    other = {LT: GT, LE: GE}[sym]
    wr = ["%s %s %s or %s %s %s" % (X, sym, sol(lo), X, other, sol(hi)),
          "%s %s %s %s %s" % (sol(F(-k + b, a)), sym, X, sym, sol(F(k + b, a))) if b else "%s %s %s %s %s" % (sol(lo), sym, X, sym, sol(hi + 1)),
          "%s %s %s" % (X, sym, sol(hi))]
    e = "“Less than” gives an <b>and</b> inequality: %s %s %s %s %s. %sSo <b>%s</b>." % (
        MINUS + num(k), sym, expr([(a, X), (b, "")]), sym, num(k),
        ("Subtract %s from every part%s. " % (num(b), "" if a == 1 else ", then divide by %d" % a)) if b > 0 else (
            ("Add %s to every part%s. " % (num(-b), "" if a == 1 else ", then divide by %d" % a)) if b < 0 else ("Divide every part by %d. " % a if a != 1 else "")),
        right)
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 4: greater than (or)
def one_greater(r):
    a = r.choice([1, 1, 2, 3])
    b = r.randint(-8, 8)
    k = r.randint(-2, 12)
    sym = r.choice([GT, GE])
    if k < 0 and r.random() < 0.7:
        return None
    q = "Solve %s." % B("%s %s %s" % (ab(a, b), sym, num(k)))
    if k < 0:
        return T(q, "All real numbers", [NONE, "%s %s %s" % (X, sym, sol(F(k - b, a))), "%s %s 0" % (X, sym)],
                 "An absolute value is never negative, so it is always greater than %s: <b>all real numbers</b>." % num(k))
    if k == 0 and sym == GE:
        return None
    lo, hi = F(-k - b, a), F(k - b, a)
    less = {GT: LT, GE: LE}[sym]
    right = "%s %s %s or %s %s %s" % (X, less, sol(lo), X, sym, sol(hi))
    wr = ["%s %s %s %s %s" % (sol(lo), less, X, less, sol(hi)),
          "%s %s %s or %s %s %s" % (X, sym, sol(lo), X, less, sol(hi)),
          "%s %s %s" % (X, sym, sol(hi))]
    e = "“Greater than” gives an <b>or</b> inequality: %s %s %s or %s %s %s. Solve each part: <b>%s</b>." % (
        expr([(a, X), (b, "")]), less, MINUS + num(k) if k else "0", expr([(a, X), (b, "")]), sym, num(k), right)
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 5: problems
def problems():
    data = [
        ("A machine fills bags with 500 g of rice. A bag is accepted if it is within 8 g of 500 g. Which inequality shows the accepted masses <i>m</i>?", "|<i>m</i> − 500| ≤ 8",
         ["|<i>m</i> − 8| ≤ 500", "|<i>m</i> − 500| ≥ 8", "|<i>m</i> + 500| ≤ 8"], "“Within 8 of 500” means the distance from 500 is at most 8: <b>|<i>m</i> − 500| ≤ 8</b>."),
        ("Solve |<i>m</i> − 500| ≤ 8.", "492 ≤ <i>m</i> ≤ 508", ["<i>m</i> ≤ 492 or <i>m</i> ≥ 508", "−8 ≤ <i>m</i> ≤ 8", "500 ≤ <i>m</i> ≤ 508"], "−8 ≤ <i>m</i> − 500 ≤ 8, so <b>492 ≤ <i>m</i> ≤ 508</b>."),
        ("A thermostat is set to 68 °F. The heater turns on when the temperature is more than 3 °F away from 68 °F. Which inequality shows when it turns on?", "|<i>t</i> − 68| &gt; 3",
         ["|<i>t</i> − 68| &lt; 3", "|<i>t</i> − 3| &gt; 68", "<i>t</i> − 68 &gt; 3"], "“More than 3 away from 68” is <b>|<i>t</i> − 68| &gt; 3</b>."),
        ("Which numbers are 5 units from −2 on a number line?", "−7 and 3", ["−3 and 7", "3 only", "−7 only"], "|<i>x</i> + 2| = 5, so <i>x</i> + 2 = 5 or −5: <b>−7 and 3</b>."),
        ("Which equation has no solution?", "|<i>x</i> + 4| = −2", ["|<i>x</i> − 4| = 2", "|<i>x</i>| = 0", "−|<i>x</i>| = −3"], "An absolute value cannot equal a negative number: <b>|<i>x</i> + 4| = −2</b>."),
        ("Which equation has exactly one solution?", "|<i>x</i> − 6| = 0", ["|<i>x</i> − 6| = 1", "|<i>x</i>| = 6", "|<i>x</i> + 6| = −1"], "Only 0 has absolute value 0, so <i>x</i> = 6 is the only solution: <b>|<i>x</i> − 6| = 0</b>."),
        ("A cereal box should hold 16 oz. The actual weight may differ by up to 0.4 oz. What is the lightest acceptable box?", "15.6 oz", ["16.4 oz", "15.4 oz", "12 oz"], "|<i>w</i> − 16| ≤ 0.4 gives 15.6 ≤ <i>w</i> ≤ 16.4. The lightest is <b>15.6 oz</b>."),
        ("The ideal swimming pool pH is 7.5, and it must stay within 0.3. Which inequality shows the pH <i>p</i>?", "7.2 ≤ <i>p</i> ≤ 7.8", ["<i>p</i> ≤ 7.2 or <i>p</i> ≥ 7.8", "7.5 ≤ <i>p</i> ≤ 7.8", "7.2 &lt; <i>p</i> &lt; 7.5"],
         "|<i>p</i> − 7.5| ≤ 0.3, so <b>7.2 ≤ <i>p</i> ≤ 7.8</b>."),
        ("Solve |2<i>x</i> − 1| + 4 = 4.", "<i>x</i> = " + fr(1, 2), [NONE, "<i>x</i> = 4", "<i>x</i> = −" + fr(1, 2) + " or <i>x</i> = " + fr(1, 2)], "|2<i>x</i> − 1| = 0, so 2<i>x</i> − 1 = 0 and <b><i>x</i> = ½</b>."),
        ("Which absolute value equation has the solutions <i>x</i> = 2 and <i>x</i> = 10?", "|<i>x</i> − 6| = 4", ["|<i>x</i> − 4| = 6", "|<i>x</i> + 6| = 4", "|<i>x</i> − 2| = 10"], "The midpoint is 6 and each solution is 4 away: <b>|<i>x</i> − 6| = 4</b>."),
        ("Which absolute value inequality has the solution −3 &lt; <i>x</i> &lt; 7?", "|<i>x</i> − 2| &lt; 5", ["|<i>x</i> − 5| &lt; 2", "|<i>x</i> + 2| &lt; 5", "|<i>x</i> − 2| &gt; 5"], "The middle is 2 and each end is 5 away: <b>|<i>x</i> − 2| &lt; 5</b>."),
        ("Kai solves |<i>x</i> + 3| = 7 and gets only <i>x</i> = 4. What did he miss?", "<i>x</i> = −10", ["<i>x</i> = −4", "<i>x</i> = 10", "Nothing; 4 is the only solution"], "<i>x</i> + 3 could also be −7, giving <b><i>x</i> = −10</b>."),
        ("Sofia solves 3|<i>x</i>| − 2 = 10 by writing 3<i>x</i> − 2 = 10 or 3<i>x</i> − 2 = −10. What should she do first?", "Isolate |x|: |x| = 4", ["Square both sides", "Divide by −2", "Nothing; her method is right"],
         "Isolate the absolute value first: 3|<i>x</i>| = 12, so |<i>x</i>| = 4 and <i>x</i> = ±4."),
        ("A runner's goal time is 50 min, give or take 3 min. Which time is NOT within the goal?", "54 min", ["47 min", "50 min", "52.5 min"], "|<i>t</i> − 50| ≤ 3 means 47 to 53 min. <b>54 min</b> is outside."),
        ("Solve |<i>x</i>| &lt; −1.", NONE, ["All real numbers", "−1 &lt; <i>x</i> &lt; 1", "<i>x</i> &lt; −1"], "An absolute value is never less than a negative number: <b>no solution</b>."),
        ("Solve |<i>x</i> − 1| ≥ 0.", "All real numbers", [NONE, "<i>x</i> ≥ 1", "<i>x</i> = 1"], "Every absolute value is 0 or more: <b>all real numbers</b>."),
        ("What is the value of −|−8| + |3 − 5|?", "−6", ["10", "6", "−10"], "−8 + 2 = <b>−6</b>."),
        ("A part should be 2.50 cm long, with a tolerance of 0.05 cm. Which length is acceptable?", "2.47 cm", ["2.44 cm", "2.56 cm", "2.60 cm"], "Acceptable lengths are 2.45 to 2.55 cm: <b>2.47 cm</b>."),
        ("Which graph matches |<i>x</i>| &gt; 2?", "Two rays: left from −2 and right from 2, with open circles", ["A segment from −2 to 2 with open circles", "Two rays with filled circles", "A single ray to the right from 2"],
         "|<i>x</i>| &gt; 2 means <i>x</i> &lt; −2 or <i>x</i> &gt; 2: <b>two rays with open circles</b>."),
        ("Solve 2|<i>x</i> + 1| ≤ 10.", "−6 ≤ <i>x</i> ≤ 4", ["<i>x</i> ≤ −6 or <i>x</i> ≥ 4", "−11 ≤ <i>x</i> ≤ 9", "−4 ≤ <i>x</i> ≤ 6"], "|<i>x</i> + 1| ≤ 5, so −5 ≤ <i>x</i> + 1 ≤ 5 and <b>−6 ≤ <i>x</i> ≤ 4</b>."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>|<i>x</i>| is the <b>distance</b> of <i>x</i> from 0, so it is never negative. |<i>x</i>| = 5 has two solutions, 5 and −5.</p>"
        "<p>To solve an absolute value equation: <b>isolate the absolute value</b>, then split it into two equations: "
        "|<i>A</i>| = <i>k</i> means <i>A</i> = <i>k</i> or <i>A</i> = −<i>k</i>. If <i>k</i> is negative, there is no solution.</p>"
        "<p>For inequalities: |<i>A</i>| &lt; <i>k</i> becomes −<i>k</i> &lt; <i>A</i> &lt; <i>k</i> (an <b>and</b>, “less thAND”). "
        "|<i>A</i>| &gt; <i>k</i> becomes <i>A</i> &lt; −<i>k</i> <b>or</b> <i>A</i> &gt; <i>k</i> (“greatOR”).</p>",
        [("Solve 2|<i>x</i> − 3| + 1 = 9.", ["Subtract 1 and divide by 2: |<i>x</i> − 3| = 4.", "<i>x</i> − 3 = 4 or <i>x</i> − 3 = −4."], "<i>x</i> = 7 or <i>x</i> = −1"),
         ("Solve |<i>x</i> + 2| &lt; 5.", ["−5 &lt; <i>x</i> + 2 &lt; 5.", "Subtract 2 from every part."], "−7 &lt; <i>x</i> &lt; 3"),
         ("Solve |<i>x</i> − 1| ≥ 4.", ["<i>x</i> − 1 ≤ −4 or <i>x</i> − 1 ≥ 4."], "<i>x</i> ≤ −3 or <i>x</i> ≥ 5")],
        ["Giving only one solution. |<i>x</i> + 3| = 7 has two: 4 and −10.",
         "Splitting before isolating: in 3|<i>x</i>| − 2 = 10, first get |<i>x</i>| = 4.",
         "Solving |<i>x</i>| = −3 as <i>x</i> = ±3. There is no solution.",
         "Writing |<i>x</i>| &lt; 4 as <i>x</i> &lt; −4 or <i>x</i> &gt; 4. Less than gives the part between: −4 &lt; <i>x</i> &lt; 4."])


def main():
    sets = [S("Solve |ax + b| = k", collect(one_basic, 20, R)),
            S("Isolate the absolute value first", collect(one_multi, 20, R)),
            S("Less than: and inequalities", collect(one_less, 20, R)),
            S("Greater than: or inequalities", collect(one_greater, 20, R)),
            S("Absolute value word problems", problems())]
    make("absolute-value-equations-and-inequalities", 4, "A-CED.A.1",
         "Absolute Value Equations and Inequalities",
         "Algebra 1 Absolute Value Equations and Inequalities Worksheets (Free, Answer Key)",
         "Absolute value equations and inequalities",
         "Create equations and inequalities in one variable and use them to solve problems.",
         "Free Algebra 1 absolute value worksheets (A-CED.A.1, A-REI.B.3): solve absolute value equations with two, one or no "
         "solutions, isolate the absolute value first, and solve and/or absolute value inequalities and tolerance problems. 100 questions with an answer key.",
         "Isolate the absolute value, then split: |A| = k means A = k or A = −k.",
         "|A| < k is an and inequality; |A| > k is an or inequality. A negative k means no solution (or all numbers).",
         body(),
         [("How many solutions does an absolute value equation have?", "Usually two. |A| = k has two solutions when k > 0, one when k = 0 and none when k < 0."),
          ("Why do I isolate the absolute value first?", "The rule |A| = k → A = ±k only works when the absolute value is alone on one side. Undo the other operations first."),
          ("How do I solve |x − a| < k?", "Write it as −k < x − a < k and solve the three-part inequality. The solution is the numbers between a − k and a + k."),
          ("How do I solve |x − a| > k?", "Write it as x − a < −k or x − a > k and solve each part. The solution is two rays going in opposite directions.")],
         sets, R, domain="Equations & Inequalities")


if __name__ == "__main__":
    main()
