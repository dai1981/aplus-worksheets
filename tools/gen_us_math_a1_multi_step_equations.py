# -*- coding: utf-8 -*-
"""
US Algebra 1: Multi-Step Equations (Common Core A-REI.B.3, A-CED.A.1)
  python3 tools/gen_us_math_a1_multi_step_equations.py
Distributing and combining like terms (including a negative in front of parentheses), parentheses on both
sides, equations with fractions (clearing denominators), equations with decimals and percents, and writing
and solving equations for word problems.
Wrong answers come from real mistakes: not changing both signs after a minus in front of parentheses,
distributing to the first term only, multiplying only some terms by the common denominator, and stopping
one step early.
"""
import random
from fractions import Fraction as F
from us_hs import num, B, S, make, lesson, collect, QN, T, expr, fr, dec, X, MINUS, usd

R = random.Random(90101)


def L(a, b, v=X):
    return expr([(a, v), (b, "")])


def f(v):
    v = F(v)
    if v.denominator == 1:
        return num(v)
    s = fr(abs(v.numerator), v.denominator)
    return (MINUS + s) if v < 0 else s


def QF(q, ans, wrongs, e):
    ans = F(ans)
    ws = [F(w) for w in wrongs if w is not None and F(w) != ans] + [ans + 1, ans - 1, -ans, ans + 2]
    seen, cands = {f(ans)}, []
    for w in ws:
        if f(w) not in seen:
            seen.add(f(w))
            cands.append((f(w), w))
    return T(q, f(ans), [c for c, _ in cands[:3]], e)


def cx(k):
    k = F(k)
    return (X if k == 1 else (MINUS + X if k == -1 else num(k) + X))


def coef(a, inside):
    return ("%s(%s)" % ("" if a == 1 else (MINUS if a == -1 else num(a)), inside))


# ------------------------------------------------------------ set 1: distribute and combine
def one_dist(r):
    x = r.randint(-8, 9)
    a, b, c = r.randint(2, 6), r.randint(1, 4), r.randint(-9, 9)
    d, e_, g_ = r.randint(1, 5), r.randint(1, 4), r.randint(-9, 9)
    if c == 0 or g_ == 0:
        return None
    k = a * b - d * e_
    if k == 0 or abs(k) > 12:
        return None
    rhs = k * x + a * c - d * g_
    q = "Solve %s." % B("%s %s %s = %s" % (coef(a, L(b, c)), MINUS, coef(d, L(e_, g_)), num(rhs)))
    e = ("Distribute both parts: %s and %s. Combine like terms: %s = %s. %s %s: %s%s = %s. Divide by %s: %s = <b>%s</b>." % (
        L(a * b, a * c), expr([(-d * e_, X), (-d * g_, "")]), L(k, a * c - d * g_), num(rhs),
        "Subtract" if a * c - d * g_ > 0 else "Add", num(abs(a * c - d * g_)), cx(k), "", num(rhs - a * c + d * g_), num(k), X, num(x)))
    wrong_sign = F(rhs - a * c - d * g_, k)                # −d(ex + g) taken as −dex + dg
    first_only = F(rhs - c + d * g_, k)                    # a(bx + c) taken as abx + c
    return QF(q, x, [wrong_sign, first_only, F(rhs, k)], e)


# ------------------------------------------------------------ set 2: parentheses on both sides
def one_both(r):
    x = r.randint(-9, 10)
    a, d = r.randint(2, 8), r.randint(2, 7)
    if a == d:
        return None
    b, e_ = r.randint(-7, 7), r.randint(-7, 7)
    if b == 0 or e_ == 0:
        return None
    c = a * (x + b) - d * (x + e_)
    if c == 0 or abs(c) > 40:
        return None
    rhs = "%s %s %s" % (coef(d, L(1, e_)), "+" if c > 0 else MINUS, num(abs(c)))
    q = "Solve %s." % B("%s = %s" % (coef(a, L(1, b)), rhs))
    k = a - d
    e = ("Distribute: %s = %s. Subtract %s from both sides: %s = %s. Then %s = %s, so %s = <b>%s</b>." % (
        L(a, a * b), L(d, d * e_ + c), (num(d) if d != 1 else "") + X, L(k, a * b), num(d * e_ + c),
        cx(k), num(d * e_ + c - a * b), X, num(x)))
    return QF(q, x, [F(d * e_ + c - a * b, a + d), F(d * e_ + c + a * b, k), F(d * e_ - c - a * b, k)], e)


# ------------------------------------------------------------ set 3: fractions
def one_frac(r):
    kind = r.choice(["sum", "cross", "coef"])
    if kind == "sum":
        p, q_ = r.sample([2, 3, 4, 5, 6], 2)
        m = p * q_
        x = m * r.choice([1, 2, 3, -1, -2])
        rr = F(x, p) + F(x, q_)
        if rr.denominator != 1:
            return None
        q = "Solve %s." % B("%s + %s = %s" % (fr(X, p), fr(X, q_), num(rr)))
        e = ("Multiply every term by %d (a common denominator): %d%s + %d%s = %s, so %d%s = %s and %s = <b>%s</b>." % (
            m, q_, X, p, X, num(rr * m), p + q_, X, num(rr * m), X, num(x)))
        return QF(q, x, [F(rr * (p + q_)), rr * m, F(rr, p + q_) * p * q_ / (p + q_)], e)
    if kind == "cross":
        p, q_ = r.sample([2, 3, 4, 5, 6, 7], 2)
        t = r.choice([-4, -3, -2, -1, 1, 2, 3, 4, 5, 6])
        x = r.randint(-6, 10)
        a = p * t - x
        b = x - q_ * t
        if a == 0 or b == 0 or abs(a) > 15 or abs(b) > 15:
            return None
        q = "Solve %s." % B("%s = %s" % (fr(L(1, a), p), fr(L(1, -b), q_)))
        e = ("Cross-multiply: %d(%s) = %d(%s). Distribute: %s = %s. Collect: %s = %s, so %s = <b>%s</b>." % (
            q_, L(1, a), p, L(1, -b), L(q_, q_ * a), L(p, -p * b), cx(q_ - p),
            num(-p * b - q_ * a), X, num(x)))
        return QF(q, x, [F(-p * b - a, q_ - p) if q_ != p else None, F(-b - q_ * a, q_ - p), F(p * b - q_ * a, q_ - p)], e)
    p = r.choice([2, 3, 4, 5])
    n_ = r.randint(1, p - 1) if p > 2 else 1
    if F(n_, p).denominator != p:
        return None
    qd = r.choice([2, 3, 4, 6])
    cn = r.randint(1, qd - 1)
    if F(cn, qd).denominator != qd:
        return None
    x = p * r.randint(-4, 6)
    if x == 0:
        return None
    rr = F(n_, p) * x - F(cn, qd)
    q = "Solve %s." % B("%s%s %s %s = %s" % (fr(n_, p), X, MINUS, fr(cn, qd), f(rr)))
    e = ("Add %s to both sides: %s%s = %s. Multiply by %s: %s = <b>%s</b>." % (
        fr(cn, qd), fr(n_, p), X, f(rr + F(cn, qd)), fr(p, n_) if n_ != 1 else num(p), X, num(x)))
    return QF(q, x, [(rr + F(cn, qd)) * F(n_, p), (rr - F(cn, qd)) * F(p, n_), rr * F(p, n_)], e)


# ------------------------------------------------------------ set 4: decimals and percents
def one_dec(r):
    kind = r.choice(["dec", "dec", "pct"])
    if kind == "dec":
        a, c = F(r.randint(2, 15), 10), F(r.randint(1, 9), 10)
        if a == c:
            return None
        x = r.randint(-6, 12)
        b = F(r.randint(-40, 40), 10)
        d = a * x + b - c * x
        if b == 0 or d == 0:
            return None
        q = "Solve %s." % B("%s = %s" % (L(a, b), L(c, d)))
        k = a - c
        e = ("Multiply every term by 10 to clear the decimals: %s = %s. Then %s = %s, so %s = <b>%s</b>." % (
            L(a * 10, b * 10), L(c * 10, d * 10), cx(k * 10), num((d - b) * 10), X, num(x)))
        return QF(q, x, [F(d - b, a + c), F(d + b, k), F((d - b) * 10, k)], e)
    p = r.choice([5, 6, 7, 8, 10, 15, 20, 25])
    base = r.choice([20, 40, 60, 80, 100, 120, 200, 240, 300])
    up = r.random() < 0.6
    tot = F(base * (100 + p if up else 100 - p), 100)
    if (tot * 100).denominator != 1:
        return None
    item = r.choice(["jacket", "bike", "phone case", "pair of sneakers", "concert ticket", "backpack"])
    if up:
        q = "A %s costs %s after a %d%% sales tax is added. Solve %s to find the price before tax." % (item, usd(tot), p, B("%s + %s%s = %s" % (X, dec(F(p, 100)), X, dec(tot))))
        e = "Combine like terms: %s%s = %s, so %s = %s ÷ %s = <b>%s</b>." % (dec(F(100 + p, 100)), X, dec(tot), X, dec(tot), dec(F(100 + p, 100)), usd(base))
        w = [tot * F(100 - p, 100), tot - p, tot / F(p, 100) if tot / F(p, 100) < 10000 else tot + p]
    else:
        q = "After a %d%% discount, a %s costs %s. Solve %s to find the original price." % (p, item, usd(tot), B("%s %s %s%s = %s" % (X, MINUS, dec(F(p, 100)), X, dec(tot))))
        e = "Combine like terms: %s%s = %s, so %s = %s ÷ %s = <b>%s</b>." % (dec(F(100 - p, 100)), X, dec(tot), X, dec(tot), dec(F(100 - p, 100)), usd(base))
        w = [tot * F(100 + p, 100), tot + p, tot / F(100 + p, 100)]
    cands = [usd(v) for v in w if F(v) > 0 and usd(v) != usd(base)]
    cands = list(dict.fromkeys(cands))
    while len(cands) < 3:
        cands.append(usd(base + 10 * (len(cands) + 1)))
    return T(q, usd(base), cands[:3], e)


# ------------------------------------------------------------ set 5: word problems
def problems():
    data = [
        ("The sum of three consecutive odd integers is 87. What is the largest?", "31", ["29", "27", "33"], "<i>n</i> + (<i>n</i> + 2) + (<i>n</i> + 4) = 87, so 3<i>n</i> + 6 = 87 and <i>n</i> = 27. The largest is <b>31</b>."),
        ("A rectangle's length is 4 less than 3 times its width. Its perimeter is 64 cm. What is its width?", "9 cm", ["8 cm", "17 cm", "23 cm"],
         "2<i>w</i> + 2(3<i>w</i> − 4) = 64, so 8<i>w</i> − 8 = 64 and <i>w</i> = <b>9 cm</b>."),
        ("Maya has $15 more than twice what Liam has. Together they have $105. How much does Liam have?", "$30", ["$45", "$75", "$37.50"], "<i>x</i> + 2<i>x</i> + 15 = 105, so 3<i>x</i> = 90 and <i>x</i> = <b>$30</b>."),
        ("Adult tickets cost $12 and student tickets cost $8. A group buys 3 more student tickets than adult tickets and pays $164. How many adult tickets did they buy?", "7", ["10", "8", "6"],
         "12<i>a</i> + 8(<i>a</i> + 3) = 164, so 20<i>a</i> + 24 = 164 and <i>a</i> = <b>7</b>."),
        ("Two trains leave the same station in opposite directions. One travels at 60 mph and the other at 75 mph. After how many hours are they 405 miles apart?", "3 hours", ["2.5 hours", "6.75 hours", "5.4 hours"],
         "60<i>t</i> + 75<i>t</i> = 405, so 135<i>t</i> = 405 and <i>t</i> = <b>3 hours</b>."),
        ("A car leaves 2 hours after a bus, on the same road. The bus goes 45 mph and the car goes 63 mph. How long after the car leaves does it catch the bus?", "5 hours", ["2 hours", "7 hours", "3 hours"],
         "63<i>t</i> = 45(<i>t</i> + 2), so 18<i>t</i> = 90 and <i>t</i> = <b>5 hours</b>."),
        ("The angles of a triangle are <i>x</i>°, (2<i>x</i> + 10)° and (3<i>x</i> − 4)°. What is the largest angle?", "83°", ["29°", "68°", "87°"],
         "6<i>x</i> + 6 = 180, so <i>x</i> = 29. The angles are 29°, 68° and <b>83°</b>."),
        ("A phone costs $480. Ethan pays $120 now and $45 a month. After how many months will he have paid it off?", "8", ["10.7", "13.3", "6"], "120 + 45<i>m</i> = 480, so 45<i>m</i> = 360 and <i>m</i> = <b>8</b>."),
        ("A plumber charges a $65 fee plus $40 per hour. The bill is $225. How many hours did the job take?", "4", ["5.6", "7.25", "3"], "65 + 40<i>h</i> = 225, so 40<i>h</i> = 160 and <i>h</i> = <b>4</b>."),
        ("Grace is 6 years older than her brother. In 4 years the sum of their ages will be 40. How old is Grace now?", "19", ["13", "23", "17"],
         "(<i>b</i> + 6 + 4) + (<i>b</i> + 4) = 40, so 2<i>b</i> + 14 = 40 and <i>b</i> = 13. Grace is <b>19</b>."),
        ("A jar has dimes and quarters worth $4.00. There are 5 more dimes than quarters. How many quarters are there?", "10", ["15", "11", "16"],
         "0.25<i>q</i> + 0.10(<i>q</i> + 5) = 4.00, so 0.35<i>q</i> + 0.5 = 4 and <i>q</i> = <b>10</b> (and 15 dimes)."),
        ("A gym charges a $60 joining fee plus $25 a month. Another charges $40 a month with no fee. After how many months do they cost the same?", "4", ["2.4", "1.5", "6"],
         "60 + 25<i>m</i> = 40<i>m</i>, so 60 = 15<i>m</i> and <i>m</i> = <b>4</b>."),
        ("Three times the sum of a number and 5 is 9 less than 5 times the number. What is the number?", "12", ["−12", "7", "3"], "3(<i>n</i> + 5) = 5<i>n</i> − 9, so 15 + 9 = 2<i>n</i> and <i>n</i> = <b>12</b>."),
        ("Half of a number, plus a third of the number, is 25. What is the number?", "30", ["15", "50", "75"], "<i>n</i>/2 + <i>n</i>/3 = 25. Multiply by 6: 5<i>n</i> = 150, so <i>n</i> = <b>30</b>."),
        ("A store raises a price by 20% to $54. What was the original price?", "$45", ["$43.20", "$34", "$64.80"], "1.2<i>p</i> = 54, so <i>p</i> = <b>$45</b>."),
        ("Olivia's test scores are 82, 75 and 91. What must she score on the fourth test to have a mean of 85?", "92", ["85", "83", "248"], "(82 + 75 + 91 + <i>x</i>) ÷ 4 = 85, so 248 + <i>x</i> = 340 and <i>x</i> = <b>92</b>."),
        ("A rental van costs $35 a day plus $0.40 per mile. A 2-day rental costs $118. How many miles were driven?", "120", ["207.5", "295", "60"], "70 + 0.4<i>m</i> = 118, so 0.4<i>m</i> = 48 and <i>m</i> = <b>120</b>."),
        ("The perimeter of an isosceles triangle is 52 in. The base is 8 in. shorter than each equal side. How long is the base?", "12 in.", ["20 in.", "17.3 in.", "28 in."],
         "<i>s</i> + <i>s</i> + (<i>s</i> − 8) = 52, so 3<i>s</i> = 60 and <i>s</i> = 20. The base is 20 − 8 = <b>12 in.</b>"),
        ("Supplementary angles measure (4<i>x</i> + 12)° and (2<i>x</i> − 6)°. Find <i>x</i>.", "29", ["14", "31", "174"], "4<i>x</i> + 12 + 2<i>x</i> − 6 = 180, so 6<i>x</i> = 174 and <i>x</i> = <b>29</b>."),
        ("A water tank holds 500 gallons and loses 12 gallons an hour. Another holds 200 gallons and gains 18 gallons an hour. When do they hold the same amount?", "After 10 hours", ["After 50 hours", "After 23.3 hours", "After 5 hours"],
         "500 − 12<i>h</i> = 200 + 18<i>h</i>, so 300 = 30<i>h</i> and <i>h</i> = <b>10</b>."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>Solve a multi-step equation in this order: <b>clear parentheses</b> (distribute), <b>clear fractions or decimals</b> "
        "(multiply every term by the same number), <b>collect</b> the variable terms on one side and the numbers on the other, then <b>divide</b>. "
        "Do the same thing to both sides each time, and check by substituting your answer.</p>"
        "<p>A minus sign in front of parentheses changes the sign of <b>every</b> term inside: −2(<i>x</i> − 3) = −2<i>x</i> + 6.</p>",
        [("Solve 4(2<i>x</i> + 1) − 3(<i>x</i> − 2) = 25.", ["Distribute: 8<i>x</i> + 4 − 3<i>x</i> + 6 = 25.", "Combine: 5<i>x</i> + 10 = 25.", "5<i>x</i> = 15."], "<i>x</i> = 3"),
         ("Solve <span class='fr'><span class='fn'><i>x</i></span><span class='fd'>3</span></span> + <span class='fr'><span class='fn'><i>x</i></span><span class='fd'>4</span></span> = 14.",
          ["Multiply every term by 12: 4<i>x</i> + 3<i>x</i> = 168.", "7<i>x</i> = 168."], "<i>x</i> = 24"),
         ("Solve 0.3<i>x</i> + 1.2 = 0.1<i>x</i> + 2.", ["Multiply by 10: 3<i>x</i> + 12 = <i>x</i> + 20.", "2<i>x</i> = 8."], "<i>x</i> = 4")],
        ["Changing only the first sign after a minus: −3(<i>x</i> − 2) is −3<i>x</i> + 6, not −3<i>x</i> − 6.",
         "Distributing to the first term only: 4(2<i>x</i> + 1) is 8<i>x</i> + 4, not 8<i>x</i> + 1.",
         "Multiplying only the fractions by the common denominator. Every term, on both sides, must be multiplied.",
         "Stopping at 5<i>x</i> = 15. Divide to get <i>x</i> on its own."])


def main():
    sets = [S("Distribute and combine like terms", collect(one_dist, 20, R)),
            S("Parentheses on both sides", collect(one_both, 20, R)),
            S("Equations with fractions", collect(one_frac, 20, R)),
            S("Equations with decimals and percents", collect(one_dec, 20, R)),
            S("Write and solve equations", problems())]
    make("multi-step-equations", 1, "A-REI.B.3",
         "Multi-Step Equations: Parentheses, Fractions and Decimals",
         "Algebra 1 Multi-Step Equations Worksheets: Distributing, Fractions, Decimals and Word Problems (Free, Answer Key)",
         "Multi-step equations",
         "Solve linear equations and inequalities in one variable, including equations with coefficients represented by letters.",
         "Free Algebra 1 multi-step equations worksheets (A-REI.B.3): distribute and combine like terms, parentheses on both sides, "
         "equations with fractions and decimals, and writing equations for word problems. 100 questions with an answer key.",
         "Clear parentheses, clear fractions, collect like terms, then divide.",
         "Do the same thing to both sides, and check by substituting your answer.",
         body(),
         [("How do you solve multi-step equations?", "Distribute to clear parentheses, multiply to clear fractions or decimals, collect the variable terms on one side and the numbers on the other, then divide by the coefficient."),
          ("How do you solve an equation with fractions?", "Multiply every term on both sides by a common denominator. The fractions disappear and you solve the equation that is left."),
          ("What happens to a minus sign in front of parentheses?", "It changes the sign of every term inside: −(x − 4) = −x + 4."),
          ("How do I check my answer?", "Substitute it into the original equation. Both sides should give the same number.")],
         sets, R, domain="Equations & Inequalities")


if __name__ == "__main__":
    main()
