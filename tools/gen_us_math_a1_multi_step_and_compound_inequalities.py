# -*- coding: utf-8 -*-
"""
US Algebra 1: Multi-Step and Compound Inequalities (Common Core A-REI.B.3)
  python3 tools/gen_us_math_a1_multi_step_and_compound_inequalities.py
Multi-step inequalities (negatives and parentheses), variables on both sides, compound inequalities with
"and" (three-part) and "or", reading compound inequalities from number lines, and word problems.
Wrong answers come from real mistakes: not reversing the sign after dividing by a negative, doing a step to
only some parts of a three-part inequality, mixing up "and" and "or", and open and closed circles.
"""
import random
from fractions import Fraction as F
from us_hs import num, B, S, make, lesson, collect, T, fr, expr, svg_wrap, line, text, fig, INK, RED, MINUS

R = random.Random(90301)
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


# ------------------------------------------------------------ set 1: multi-step
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


# ------------------------------------------------------------ set 2: variables on both sides
def one_both(r):
    v = X
    a, c = r.randint(1, 6), r.randint(2, 9)
    if a == c:
        return None
    s = r.randint(-6, 8)
    b = r.randint(-9, 9)
    d = a * s + b - c * s
    if b == 0 or d == 0:
        return None
    sym = r.choice([LT, LE, GT, GE])
    q = "Solve %s." % B("%s %s %s" % (expr([(a, v), (b, "")]), sym, expr([(c, v), (d, "")])))
    k = a - c
    final = sym if k > 0 else FLIP[sym]
    right = "%s %s %s" % (v, final, num(s))
    wr = ["%s %s %s" % (v, FLIP[final], num(s)), "%s %s %s" % (v, final, sol(F(d + b, k))) if F(d + b, k) != s else "%s %s %s" % (v, final, num(s + 3)),
          "%s %s %s" % (v, final, num(-s)) if s else "%s %s 1" % (v, final)]
    e = "Subtract %s from both sides: %s %s %s. " % (expr([(c, v)]), expr([(k, v)]), sym, num(d - b))
    if k == 1:
        e = "Subtract %s from both sides: <b>%s</b>." % (expr([(c, v)]), right.replace(" ", " ", 0))
        e = "Subtract %s from both sides: %s %s %s, which is <b>%s</b>." % (expr([(c, v)]), v, sym, num(d - b), right)
    else:
        e += ("Divide by %s and <b>reverse the sign</b>: <b>%s</b>." % (num(k), right)) if k < 0 else ("Divide by %s: <b>%s</b>." % (num(k), right))
    if len(set(wr)) < 3 or right in wr:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 3: compound inequalities with "and"
def one_and(r):
    v = X
    a = r.choice([2, 3, 4, 5, -2, -3, 1])
    b = r.randint(-8, 8)
    lo, hi = r.randint(-6, 2), None
    hi = lo + r.randint(2, 7)
    s1, s2 = r.choice([LT, LE]), r.choice([LT, LE])
    p, q_ = a * lo + b, a * hi + b
    if a < 0:
        p, q_ = q_, p
    mid = expr([(a, v), (b, "")])
    q = "Solve %s." % B("%s %s %s %s %s" % (num(p), s1, mid, s2, num(q_)))
    if a > 0:
        right = "%s %s %s %s %s" % (num(lo), s1, v, s2, num(hi))
        T_ = {LT: LE, LE: LT}
        wrong_dir = "%s %s %s %s %s" % (num(lo), T_[s1], v, T_[s2], num(hi))
    else:
        right = "%s %s %s %s %s" % (num(lo), s2, v, s1, num(hi))
        wrong_dir = "%s %s %s %s %s" % (num(-lo), s1, v, s2, num(-hi)) if lo != -hi else "%s %s %s %s %s" % (num(hi), s1, v, s2, num(lo))
    only_b = "%s %s %s %s %s" % (sol(F(p - b)), s1, v, s2, sol(F(q_ - b)))
    no_div = "%s %s %s %s %s" % (sol(F(p, abs(a))), s1, v, s2, sol(F(q_, abs(a))))
    e = "Do the same to all three parts. %s %s: %s %s %s %s %s. " % (
        "Subtract" if b > 0 else "Add", num(abs(b)), num(p - b), s1, expr([(a, v)]), s2, num(q_ - b))
    if a < 0:
        e += "Divide every part by %s and <b>reverse both signs</b>: <b>%s</b>." % (num(a), right)
    elif a != 1:
        e += "Divide every part by %s: <b>%s</b>." % (num(a), right)
    else:
        e += "<b>%s</b>." % right
    if b == 0:
        return None
    wr = [w for w in dict.fromkeys([wrong_dir, only_b, no_div]) if w != right]
    if len(wr) < 3:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 4: compound inequalities with "or", and graphs
def one_or(r):
    v = X
    a, b = r.randint(2, 5), r.randint(-6, 6)
    lo = r.randint(-6, 1)
    hi = lo + r.randint(2, 6)
    c1, c2 = a * lo + b, a * hi + b
    s1 = r.choice([LT, LE])
    s2 = r.choice([GT, GE])
    q = "Solve %s." % B("%s %s %s <b>or</b> %s %s %s" % (expr([(a, v), (b, "")]), s1, num(c1), expr([(a, v), (b, "")]), s2, num(c2)))
    right = "%s %s %s or %s %s %s" % (v, s1, num(lo), v, s2, num(hi))
    wr = ["%s %s %s %s %s" % (num(lo), s1, v, FLIP[s2], num(hi)),
          "%s %s %s or %s %s %s" % (v, FLIP[s1], num(lo), v, FLIP[s2], num(hi)),
          "%s %s %s or %s %s %s" % (v, s1, sol(F(c1 - b)), v, s2, sol(F(c2 - b)))]
    e = "Solve each part on its own: %s %s %s; %s %s %s. With <b>or</b>, a number only has to satisfy one part: <b>%s</b>." % (
        v, s1, num(lo), v, s2, num(hi), right)
    if b == 0:
        return None
    return T(q, right, wr, e)


def one_graph(r):
    a = r.randint(-4, 1)
    b = a + r.randint(2, 5)
    if r.random() < 0.5:
        return one_nl_band(r, a, b)
    ca, cb = r.random() < 0.5, r.random() < 0.5
    s1 = LE if ca else LT
    s2 = GE if cb else GT
    right = "%s %s %s or %s %s %s" % (X, s1, num(a), X, s2, num(b))
    wr = ["%s %s %s %s %s" % (num(a), s1, X, LE if cb else LT, num(b)),
          "%s %s %s or %s %s %s" % (X, GE if ca else GT, num(a), X, LE if cb else LT, num(b)),
          "%s %s %s or %s %s %s" % (X, LT if ca else LE, num(a), X, GT if cb else GE, num(b))]
    q = "Which compound inequality is shown on the number line?%s" % fig(nline_or(a - 3, b + 3, a, ca, b, cb))
    e = "The graph goes left from %s and right from %s, so it is an <b>or</b> inequality. %s. So <b>%s</b>." % (
        num(a), num(b), "Filled circles are included (≤ or ≥); open circles are not", right)
    return T(q, right, wr, e)


def one_nl_band(r, a, b):
    ca, cb = r.random() < 0.5, r.random() < 0.5
    s1, s2 = (LE if ca else LT), (LE if cb else LT)
    right = "%s %s %s %s %s" % (num(a), s1, X, s2, num(b))
    alt1 = "%s %s %s %s %s" % (num(a), LT if ca else LE, X, s2, num(b))
    alt2 = "%s %s %s or %s %s %s" % (X, s1, num(a), X, GE if cb else GT, num(b))
    alt3 = "%s %s %s %s %s" % (num(a), s1, X, LT if cb else LE, num(b))
    q = "Which compound inequality is shown on the number line?%s" % fig(nline(a - 2, b + 2, [(a, ca, 0), (b, cb, 0)]))
    e = "The graph is the part between %s and %s, so it is an <b>and</b> inequality. A filled circle is included; an open circle is not. So <b>%s</b>." % (num(a), num(b), right)
    return T(q, right, [alt1, alt2, alt3], e)


def nline_or(lo, hi, a, ca, b, cb):
    u, x0, y = 34, 24, 44
    W = x0 * 2 + (hi - lo) * u
    Xp = lambda t: x0 + (t - lo) * u
    s = [line(x0 - 12, y, W - x0 + 12, y, INK, 2)]
    for t in range(lo, hi + 1):
        s.append(line(Xp(t), y - 6, Xp(t), y + 6, INK, 1.5))
        s.append(text(Xp(t), y + 24, num(t), 13, weight=400))
    L0, R0 = Xp(lo) - 10, Xp(hi) + 10
    s.append(line(Xp(a), y - 16, L0, y - 16, RED, 4))
    s.append("<path d='M%.1f %d l10 -7 l0 14 Z' fill='%s'/>" % (L0 - 8, y - 16, RED))
    s.append(line(Xp(b), y - 16, R0, y - 16, RED, 4))
    s.append("<path d='M%.1f %d l-10 -7 l0 14 Z' fill='%s'/>" % (R0 + 8, y - 16, RED))
    for t, c in ((a, ca), (b, cb)):
        s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s' stroke='%s' stroke-width='2.5'/>" % (Xp(t), y - 16, RED if c else "#fff", RED))
    return svg_wrap(W, 80, "".join(s), "number line showing an or inequality")


# ------------------------------------------------------------ set 5: word problems
def problems():
    data = [
        ("A streaming plan costs $12 a month. Liam has at most $100 to spend. Which inequality shows the number of months <i>m</i>?", "12<i>m</i> ≤ 100", ["12<i>m</i> ≥ 100", "12<i>m</i> &lt; 100", "<i>m</i> + 12 ≤ 100"], "“At most” means ≤: <b>12<i>m</i> ≤ 100</b>."),
        ("A rideshare costs $3.50 plus $1.75 per mile. Emma has $24. What is the greatest whole number of miles she can ride?", "11", ["12", "13", "11.7"], "3.50 + 1.75<i>m</i> ≤ 24, so 1.75<i>m</i> ≤ 20.50 and <i>m</i> ≤ 11.7. She can ride <b>11</b> miles."),
        ("Ethan has scores of 78, 85 and 90. What is the lowest score on the fourth test that gives a mean of at least 85?", "87", ["85", "86", "88"], "(253 + <i>x</i>) ÷ 4 ≥ 85, so 253 + <i>x</i> ≥ 340 and <i>x</i> ≥ <b>87</b>."),
        ("A truck can carry at most 2,000 lb. The driver weighs 180 lb and each box weighs 65 lb. What is the greatest number of boxes?", "28", ["30", "27", "31"], "180 + 65<i>b</i> ≤ 2,000, so 65<i>b</i> ≤ 1,820 and <i>b</i> ≤ <b>28</b>."),
        ("Healthy body temperature is between 97 °F and 99 °F, inclusive. Which compound inequality shows the temperature <i>t</i>?", "97 ≤ <i>t</i> ≤ 99", ["97 &lt; <i>t</i> &lt; 99", "<i>t</i> ≤ 97 or <i>t</i> ≥ 99", "97 ≥ <i>t</i> ≥ 99"], "“Inclusive” means both ends are included: <b>97 ≤ <i>t</i> ≤ 99</b>."),
        ("A ride is closed to people shorter than 48 in. or taller than 76 in. Which inequality shows the heights <i>h</i> that are NOT allowed?", "<i>h</i> &lt; 48 or <i>h</i> &gt; 76", ["48 &lt; <i>h</i> &lt; 76", "<i>h</i> ≤ 48 or <i>h</i> ≥ 76", "48 ≤ <i>h</i> ≤ 76"], "Shorter than 48 <b>or</b> taller than 76: <b><i>h</i> &lt; 48 or <i>h</i> &gt; 76</b>."),
        ("Gym A costs $40 a month. Gym B costs $25 a month plus a $90 joining fee. For how many months <i>m</i> is Gym B cheaper?", "<i>m</i> &gt; 6", ["<i>m</i> &lt; 6", "<i>m</i> ≥ 6", "<i>m</i> &gt; 2"], "25<i>m</i> + 90 &lt; 40<i>m</i>, so 90 &lt; 15<i>m</i> and <b><i>m</i> &gt; 6</b>."),
        ("A phone plan costs $30 plus $0.10 per text. The bill must stay under $45. What is the greatest number of texts?", "149", ["150", "151", "450"], "30 + 0.1<i>t</i> &lt; 45, so <i>t</i> &lt; 150. The greatest whole number is <b>149</b>."),
        ("A club needs between $500 and $800 for a trip. It has $140 and raises $40 per car wash. Which inequality gives the number of car washes <i>c</i>?", "9 ≤ <i>c</i> ≤ 16.5", ["12.5 ≤ <i>c</i> ≤ 20", "3.5 ≤ <i>c</i> ≤ 6.5", "<i>c</i> ≥ 16.5"],
         "500 ≤ 140 + 40<i>c</i> ≤ 800, so 360 ≤ 40<i>c</i> ≤ 660 and <b>9 ≤ <i>c</i> ≤ 16.5</b>."),
        ("The sum of two consecutive integers is less than 45. What is the greatest possible smaller integer?", "21", ["22", "23", "44"], "<i>n</i> + (<i>n</i> + 1) &lt; 45, so 2<i>n</i> &lt; 44 and <i>n</i> &lt; 22. The greatest is <b>21</b>."),
        ("A rectangle has width 6 ft and length <i>x</i> ft. Its perimeter must be at most 50 ft. Which is correct?", "<i>x</i> ≤ 19", ["<i>x</i> ≤ 22", "<i>x</i> ≤ 44", "<i>x</i> ≥ 19"], "2<i>x</i> + 12 ≤ 50, so 2<i>x</i> ≤ 38 and <b><i>x</i> ≤ 19</b>."),
        ("Which number is a solution of 2<i>x</i> − 3 &lt; −5 or 2<i>x</i> − 3 &gt; 7?", "6", ["0", "4", "−1"], "The inequality means <i>x</i> &lt; −1 or <i>x</i> &gt; 5. Only <b>6</b> works."),
        ("Which number is a solution of −1 &lt; 3<i>x</i> + 2 &lt; 11?", "2", ["3", "−1", "4"], "Subtract 2 and divide by 3: −1 &lt; <i>x</i> &lt; 3. Only <b>2</b> works."),
        ("A thermostat keeps a room within 2 °F of 70 °F. Which inequality shows the temperature <i>t</i>?", "68 ≤ <i>t</i> ≤ 72", ["<i>t</i> ≤ 68 or <i>t</i> ≥ 72", "70 ≤ <i>t</i> ≤ 72", "66 ≤ <i>t</i> ≤ 74"], "Within 2 of 70 means from 68 to 72: <b>68 ≤ <i>t</i> ≤ 72</b>."),
        ("What is the solution of 2<i>x</i> &gt; 6 and 2<i>x</i> &lt; 4?", "No solution", ["2 &lt; <i>x</i> &lt; 3", "<i>x</i> &gt; 3", "All real numbers"], "<i>x</i> &gt; 3 and <i>x</i> &lt; 2 cannot both be true: <b>no solution</b>."),
        ("What is the solution of <i>x</i> &gt; 1 or <i>x</i> &lt; 4?", "All real numbers", ["1 &lt; <i>x</i> &lt; 4", "No solution", "<i>x</i> &gt; 4"], "Every number is greater than 1 or less than 4 (or both): <b>all real numbers</b>."),
        ("Grace earns $15 an hour and wants to earn at least $240 but no more than $360 a week. How many hours <i>h</i> can she work?", "16 ≤ <i>h</i> ≤ 24", ["<i>h</i> ≥ 16", "240 ≤ <i>h</i> ≤ 360", "16 &lt; <i>h</i> &lt; 24"], "240 ≤ 15<i>h</i> ≤ 360, so <b>16 ≤ <i>h</i> ≤ 24</b>."),
        ("Solve 5 − 2(<i>x</i> + 1) ≥ 9.", "<i>x</i> ≤ −3", ["<i>x</i> ≥ −3", "<i>x</i> ≤ 3", "<i>x</i> ≥ 3"], "5 − 2<i>x</i> − 2 ≥ 9, so −2<i>x</i> ≥ 6. Divide by −2 and reverse: <b><i>x</i> ≤ −3</b>."),
        ("A school dance needs at least 120 tickets sold to break even. 47 have been sold and 8 students each sell <i>t</i> more. What is the smallest <i>t</i>?", "10", ["9", "15", "21"], "47 + 8<i>t</i> ≥ 120, so 8<i>t</i> ≥ 73 and <i>t</i> ≥ 9.125. The smallest whole number is <b>10</b>."),
        ("Which inequality is the same as −4 &lt; −2<i>x</i> ≤ 6?", "−3 ≤ <i>x</i> &lt; 2", ["2 &lt; <i>x</i> ≤ −3", "−3 &lt; <i>x</i> ≤ 2", "2 &gt; <i>x</i> ≥ 3"], "Divide every part by −2 and reverse both signs: 2 &gt; <i>x</i> ≥ −3, which is <b>−3 ≤ <i>x</i> &lt; 2</b>."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>Solve a multi-step inequality like an equation. The one change: if you <b>multiply or divide by a negative number, "
        "reverse the inequality sign</b>.</p>"
        "<p>A <b>compound inequality</b> joins two inequalities. With <b>and</b>, both must be true, so the graph is the part in between: "
        "−2 &lt; <i>x</i> ≤ 3. With <b>or</b>, either can be true, so the graph goes out in two directions: <i>x</i> &lt; −2 or <i>x</i> ≥ 3. "
        "For a three-part inequality, do the same thing to all three parts.</p>"
        + fig(nline(-4, 5, [(-2, False, 0), (3, True, 0)])),
        [("Solve 2<i>x</i> + 5 &gt; 4<i>x</i> − 7.", ["Subtract 4<i>x</i>: −2<i>x</i> + 5 &gt; −7.", "Subtract 5: −2<i>x</i> &gt; −12.", "Divide by −2 and reverse."], "<i>x</i> &lt; 6"),
         ("Solve −3 ≤ 2<i>x</i> + 1 &lt; 9.", ["Subtract 1 from all parts: −4 ≤ 2<i>x</i> &lt; 8.", "Divide all parts by 2."], "−2 ≤ <i>x</i> &lt; 4")],
        ["Forgetting to reverse the sign after dividing by a negative.",
         "Doing a step to only one or two parts of a three-part inequality.",
         "Mixing up and/or: “between” is <b>and</b>; “less than … or more than …” is <b>or</b>.",
         "Using a filled circle for &lt; or &gt;. Only ≤ and ≥ get filled circles."])


def main():
    sets = [S("Multi-step inequalities", collect(one_hard, 20, R)),
            S("Variables on both sides", collect(one_both, 20, R)),
            S("Compound inequalities with and", collect(one_and, 20, R)),
            S("Compound inequalities with or, and graphs", collect(one_or, 10, R) + collect(one_graph, 10, R)),
            S("Inequality word problems", problems())]
    make("multi-step-and-compound-inequalities", 3, "A-REI.B.3",
         "Multi-Step and Compound Inequalities",
         "Algebra 1 Inequalities Worksheets: Multi-Step and Compound Inequalities with Graphs (Free, Answer Key)",
         "Multi-step and compound inequalities",
         "Solve linear equations and inequalities in one variable, including equations with coefficients represented by letters.",
         "Free Algebra 1 inequalities worksheets (A-REI.B.3): multi-step inequalities, variables on both sides, compound inequalities "
         "with and and or, graphing on a number line, and word problems. 100 questions with an answer key.",
         "Divide or multiply by a negative? Reverse the sign.",
         "And: the part in between. Or: two separate directions. Do the same to every part.",
         body(),
         [("When do you flip the inequality sign?", "Only when you multiply or divide both sides by a negative number. Adding or subtracting never flips it."),
          ("What is a compound inequality?", "Two inequalities joined by and or or. And means both are true (−2 < x ≤ 3); or means at least one is true (x < −2 or x ≥ 3)."),
          ("How do you solve a three-part inequality?", "Do the same operation to all three parts until x is alone in the middle. If you divide by a negative, reverse both signs."),
          ("How do you graph an or inequality?", "Draw two rays going in opposite directions, with an open circle for < or > and a filled circle for ≤ or ≥.")],
         sets, R, domain="Equations & Inequalities")


if __name__ == "__main__":
    main()
