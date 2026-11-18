# -*- coding: utf-8 -*-
"""
SG Secondary 2 Maths: Direct and Inverse Proportion (Sec 2 Ratio, proportion and rates of change)
  python3 gen_sg_maths_s2_direct_and_inverse_proportion.py
The unitary method for direct proportion, recognising direct and inverse proportion, inverse proportion
problems (workers and days, speed and time), the formulae y = kx and y = k/x, and best buys.
Wrong answers come from real mistakes: treating an inverse relationship as direct, adding instead of
multiplying, and comparing prices without using the same amount.
"""
import random
from fractions import Fraction as F
from sg_sec import num, mcq, B, S, make, lesson, collect, QN, T, fr, table, sgd, People

R = random.Random(820900)
P = People(R)


def money(v):
    v = F(v)
    return sgd(v) if (v * 100).denominator == 1 else "$" + format(float(v), ",.2f")


# ------------------------------------------------------------ set 1: direct proportion (unitary)
def one_direct(r):
    kind = r.randint(0, 2)
    if kind == 0:
        n1 = r.randint(2, 8)
        each = F(r.randint(15, 250), 100) * 5 / 5
        n2 = r.choice([x for x in range(3, 15) if x != n1])
        c1 = each * n1
        if (c1 * 100).denominator != 1:
            return None
        item = r.choice(["pens", "notebooks", "cans of drink", "bus tickets", "packets of seeds"])
        q = "%d %s cost %s. How much do %d %s cost?" % (n1, item, money(c1), n2, item)
        ans = each * n2
        e = "1 costs %s ÷ %d = %s. %d cost %s × %d = <b>%s</b>." % (money(c1), n1, money(each), n2, money(each), n2, money(ans))
        return mcq(q, (money(ans), ans), [(money(w), w) for w in [c1 + (n2 - n1) if c1 + n2 - n1 > 0 else None, c1 * n2, each * (n2 + 1), c1 / n2] if w and w != ans and (w * 100).denominator == 1] +
                   [(money(ans + 1), ans + 1), (money(ans * 2), ans * 2)], e)
    if kind == 1:
        h1, p1 = r.choice([(4, 30), (5, 45), (3, 27), (6, 51), (8, 72)])
        h2 = r.choice([2, 7, 9, 10, 12])
        rate = F(p1, h1)
        ans = rate * h2
        nm, he, _ = P.next()
        q = "%s earns $%d for %d hours of work. How much does %s earn for %d hours at the same rate?" % (nm, p1, h1, he, h2)
        e = "Per hour: %d ÷ %d = %s. For %d hours: <b>%s</b>." % (p1, h1, money(rate), h2, money(ans))
        return mcq(q, (money(ans), ans), [(money(w), w) for w in [p1 + h2 - h1, p1 * h2, rate + h2] if w > 0 and w != ans] + [(money(ans + 3), ans + 3)], e)
    km1, l1 = r.choice([(150, 12), (240, 16), (90, 6), (300, 20), (120, 8)])
    km2 = r.choice([60, 75, 180, 210, 360, 450])
    ans = F(l1 * km2, km1)
    if ans.denominator > 10:
        return None
    q = "A car uses %d litres of petrol to travel %d km. How much petrol does it use for %d km?" % (l1, km1, km2)
    e = "1 km uses %d ÷ %d = %s litres. %d km uses <b>%s litres</b>." % (l1, km1, num(F(l1, km1)), km2, num(ans))
    return QN(q, ans, [F(km2 * km1, l1) / 100 if False else l1 + (km2 - km1) / 10, F(km2, l1), l1 * km2 / 10], e, unit=" litres", near=(1, -1, 2))


# ------------------------------------------------------------ set 2: direct or inverse?
SITU = [
    ("the number of cinema tickets bought and the total cost", "Direct proportion"),
    ("the number of people sharing a pizza equally and the amount each person gets", "Inverse proportion"),
    ("the speed of a car and the time it takes to drive 100 km", "Inverse proportion"),
    ("the number of hours worked (at a fixed hourly rate) and the pay", "Direct proportion"),
    ("the number of workers building a wall and the time it takes", "Inverse proportion"),
    ("the length of a side of a square and its perimeter", "Direct proportion"),
    ("the number of litres of petrol bought and the cost", "Direct proportion"),
    ("the number of taps filling a bath and the time to fill it", "Inverse proportion"),
    ("a person's age and their height", "Neither"),
    ("the number of pages in a book and its price in different shops", "Neither"),
    ("the amount of money and the number of euros you get for it", "Direct proportion"),
    ("the width of a rectangle with area 24 cm² and its length", "Inverse proportion"),
]


def one_which(r):
    if r.random() < 0.55:
        s, ans = r.choice(SITU)
        q = "What is the relationship between %s?" % B(s)
        opts = ["Direct proportion", "Inverse proportion", "Neither", "Both"]
        why = {"Direct proportion": "When one doubles, the other doubles.", "Inverse proportion": "When one doubles, the other halves.",
               "Neither": "There is no fixed rule linking them."}[ans]
        return T(q, ans, [o for o in opts if o != ans], why + " <b>%s</b>." % ans)
    k = r.choice([12, 24, 36, 60, 48])
    xs = sorted(r.sample([1, 2, 3, 4, 6, 12], 3))
    kind = r.choice(["Direct proportion", "Inverse proportion"])
    m = r.randint(2, 7)
    ys = [m * x for x in xs] if kind == "Direct proportion" else [F(k, x) for x in xs]
    if any(F(y).denominator != 1 for y in ys):
        return None
    tbl = table(["<i>x</i>"] + [num(x) for x in xs], [["<i>y</i>"] + [num(y) for y in ys]])
    q = "What type of proportion is shown in the table?%s" % tbl
    why = "<i>y</i> ÷ <i>x</i> is always %d." % m if kind.startswith("Direct") else "<i>x</i> × <i>y</i> is always %d." % k
    return T(q, kind, [o for o in ["Direct proportion", "Inverse proportion", "Neither", "Both"] if o != kind], why + " <b>%s</b>." % kind)


# ------------------------------------------------------------ set 3: inverse proportion
def one_inverse(r):
    kind = r.randint(0, 2)
    if kind == 0:
        w1, d1 = r.choice([(4, 6), (3, 10), (6, 8), (5, 12), (2, 15), (8, 3)])
        w2 = r.choice([x for x in [2, 3, 4, 5, 6, 8, 10, 12] if x != w1 and (w1 * d1) % x == 0])
        ans = F(w1 * d1, w2)
        q = "%d builders take %d days to build a wall. How long would %d builders take, working at the same rate?" % (w1, d1, w2)
        e = "Total work = %d × %d = %d builder-days. %d ÷ %d = <b>%s days</b>." % (w1, d1, w1 * d1, w1 * d1, w2, num(ans))
        return QN(q, ans, [F(d1 * w2, w1), d1 + w1 - w2 if d1 + w1 - w2 > 0 else None, w1 * d1], e,
                  fmt=lambda v: num(v) + (" day" if v == 1 else " days"), near=(1, 2, -1, 3))
    if kind == 1:
        s1, t1 = r.choice([(60, 3), (40, 6), (50, 4), (30, 8), (80, 3)])
        s2 = r.choice([x for x in [20, 30, 40, 45, 60, 80, 90, 120] if x != s1 and (s1 * t1) % x == 0])
        ans = F(s1 * t1, s2)
        q = "A journey takes %d hours at %d km/h. How long would it take at %d km/h?" % (t1, s1, s2)
        e = "Distance = %d × %d = %d km. %d ÷ %d = <b>%s hours</b>." % (s1, t1, s1 * t1, s1 * t1, s2, num(ans))
        return QN(q, ans, [w for w in [F(t1 * s2, s1), s1 * t1, t1 + (s1 - s2) // 10] if w > 0], e,
                  fmt=lambda v: num(v) + (" hour" if v == 1 else " hours"), near=(1, 2, -1, F(1, 2)))
    n1, each1 = r.choice([(4, 15), (6, 10), (5, 12), (8, 9), (3, 20)])
    n2 = r.choice([x for x in [2, 3, 4, 5, 6, 10, 12] if x != n1 and (n1 * each1) % x == 0])
    ans = F(n1 * each1, n2)
    q = "A bag of sweets is shared equally. With %d children, each gets %d sweets. How many would each get with %d children?" % (n1, each1, n2)
    e = "There are %d × %d = %d sweets. %d ÷ %d = <b>%s</b>." % (n1, each1, n1 * each1, n1 * each1, n2, num(ans))
    return QN(q, ans, [F(each1 * n2, n1), each1 + n1 - n2 if each1 + n1 - n2 > 0 else None, n1 * each1], e)


# ------------------------------------------------------------ set 4: y = kx and y = k/x
def one_formula(r):
    if r.random() < 0.5:
        k = r.choice([2, 3, 4, 5, 6, 8, F(5, 2)])
        x1 = r.randint(2, 8)
        y1 = k * x1
        x2 = r.choice([x for x in range(2, 15) if x != x1])
        ans = k * x2
        if ans.denominator if isinstance(ans, F) else 1 > 2:
            return None
        q = "<i>y</i> is directly proportional to <i>x</i>. When <i>x</i> = %d, <i>y</i> = %s. Find <i>y</i> when <i>x</i> = %d." % (x1, num(y1), x2)
        e = "<i>y</i> = <i>kx</i>. <i>k</i> = %s ÷ %d = %s. <i>y</i> = %s × %d = <b>%s</b>." % (num(y1), x1, num(k), num(k), x2, num(ans))
        return QN(q, ans, [F(y1 * x1, x2), F(y1) + x2 - x1, F(x2, k)], e)
    k = r.choice([12, 24, 36, 48, 60, 72, 120])
    x1 = r.choice([x for x in [2, 3, 4, 6, 8, 12] if k % x == 0])
    x2 = r.choice([x for x in [2, 3, 4, 5, 6, 8, 10, 12] if k % x == 0 and x != x1])
    y1 = k // x1
    ans = F(k, x2)
    q = "<i>y</i> is inversely proportional to <i>x</i>. When <i>x</i> = %d, <i>y</i> = %d. Find <i>y</i> when <i>x</i> = %d." % (x1, y1, x2)
    e = "<i>y</i> = <i>k</i>/<i>x</i>, so <i>k</i> = <i>xy</i> = %d × %d = %d. <i>y</i> = %d ÷ %d = <b>%s</b>." % (x1, y1, k, k, x2, num(ans))
    return QN(q, ans, [F(y1 * x2, x1), y1 + x1 - x2 if y1 + x1 - x2 > 0 else None, F(k * x2)], e)


# ------------------------------------------------------------ set 5: best buys and problems
def problems():
    its = []
    for (s1, p1), (s2, p2), unit in [((500, F("1.20")), (750, F("1.65")), "g"), ((2, F("1.50")), (3, F("2.40")), "litres"),
                                     ((6, F("3.30")), (10, F("5.20")), "eggs"), ((250, F("2.25")), (400, F("3.80")), "ml"),
                                     ((4, F("2.80")), (9, F("5.94")), "rolls")]:
        u1, u2 = p1 / s1, p2 / s2
        lab = (lambda n: "the %s %s pack" % (num(n), unit)) if unit in ("g", "ml") else (lambda n: "the %s-litre bottle" % num(n)) if unit == "litres" else (lambda n: "the pack of %s %s" % (num(n), unit))
        better = lab(s1) if u1 < u2 else lab(s2)
        other = lab(s2) if u1 < u2 else lab(s1)
        q = "Which is better value: %s %s for %s or %s %s for %s?" % (num(s1), unit, money(p1), num(s2), unit, money(p2))
        e = "Price per %s: %s and %s. The smaller cost per unit is <b>%s</b>." % (
            unit.rstrip("s") if unit not in ("g", "ml") else unit, money(u1) if (u1 * 100).denominator == 1 else "%sp" % num((u1 * 100).limit_denominator(1000)),
            money(u2) if (u2 * 100).denominator == 1 else "%sp" % num((u2 * 100).limit_denominator(1000)), better)
        its.append(T(q, better.capitalize(), [other.capitalize(), "They are the same value", "You cannot tell"], e))
    data = [
        ("$1 = €1.15. How many euros is $60?", "€69", ["€52.17", "€61.15", "€6.90"], "60 × 1.15 = <b>€69</b>."),
        ("S$1 = RM3.50. How many ringgit do you get for S$40?", "RM140", ["RM11.43", "RM43.50", "RM120"], "40 × 3.50 = <b>RM140</b>."),
        ("A recipe for 4 people uses 300 g of pasta. How much pasta is needed for 10 people?", "750 g", ["306 g", "1200 g", "120 g"], "300 ÷ 4 = 75 g each. 75 × 10 = <b>750 g</b>."),
        ("It takes 3 pumps 8 hours to empty a pool. How long would 4 pumps take?", "6 hours", ["10.7 hours", "9 hours", "32 hours"], "3 × 8 = 24 pump-hours. 24 ÷ 4 = <b>6 hours</b>."),
        ("6 apples cost $1.50. How much would 9 apples cost?", "$2.25", ["$4.50", "$2", "$13.50"], "1 apple = 25p. 9 × 25p = <b>$2.25</b>."),
        ("A machine fills 240 bottles in 15 minutes. How many does it fill in 1 hour?", "960", ["255", "300", "3600"], "1 hour = 4 × 15 minutes: 240 × 4 = <b>960</b>."),
        ("A map scale is 1 cm to 5 km. Two towns are 7.4 cm apart. How far apart are they?", "37 km", ["12.4 km", "74 km", "1.48 km"], "7.4 × 5 = <b>37 km</b>."),
        ("Food for 12 dogs lasts 10 days. How long would it last 8 dogs?", "15 days", ["6.7 days", "14 days", "12 days"], "12 × 10 = 120 dog-days. 120 ÷ 8 = <b>15 days</b>."),
        ("If <i>y</i> is directly proportional to <i>x</i> and <i>x</i> doubles, what happens to <i>y</i>?", "It doubles", ["It halves", "It stays the same", "It goes up by 2"], "Direct proportion: <b>it doubles</b> too."),
        ("If <i>y</i> is inversely proportional to <i>x</i> and <i>x</i> is multiplied by 3, what happens to <i>y</i>?", "It is divided by 3", ["It is multiplied by 3", "It goes down by 3", "It stays the same"], "Inverse proportion: <b><i>y</i> is divided by 3</b>."),
        ("Which graph shows direct proportion?", "A straight line through the origin", ["A straight line that does not pass through the origin", "A curve that gets closer to the axes", "A horizontal line"],
         "Direct proportion <i>y</i> = <i>kx</i> is <b>a straight line through (0, 0)</b>."),
        ("A 5 kg bag of rice costs $6.50. What is the cost per kilogram?", "$1.30", ["$32.50", "77p", "$1.50"], "6.50 ÷ 5 = <b>$1.30</b>."),
        ("Rachel types 450 words in 9 minutes. At this rate, how long will 1250 words take?", "25 minutes", ["50 minutes", "27.8 minutes", "18 minutes"], "450 ÷ 9 = 50 words per minute. 1250 ÷ 50 = <b>25 minutes</b>."),
        ("8 identical books weigh 3.2 kg. What do 5 of these books weigh?", "2 kg", ["0.4 kg", "1.6 kg", "5.12 kg"], "1 book = 0.4 kg. 5 × 0.4 = <b>2 kg</b>."),
        ("A coach travelling at 50 km/h takes 6 hours. How fast must it go to take 5 hours?", "60 km/h", ["41.7 km/h", "55 km/h", "300 km/h"], "Distance = 300 km. 300 ÷ 5 = <b>60 km/h</b>."),
    ]
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p><b>Direct proportion</b>: when one quantity doubles, so does the other (<i>y</i> = <i>kx</i>). Use the "
        "<b>unitary method</b>: find the value for 1, then multiply.</p>"
        "<p><b>Inverse proportion</b>: when one quantity doubles, the other halves (<i>y</i> = <i>k</i>/<i>x</i>). "
        "The product stays the same, so find the total first (for example builder-days), then divide.</p>",
        [("5 pens cost $3.50. Find the cost of 8 pens.", ["1 pen costs $3.50 ÷ 5 = 70p.", "8 pens cost 8 × 70p."], "$5.60"),
         ("4 workers take 6 days. How long would 3 workers take?", ["4 × 6 = 24 worker-days.", "24 ÷ 3 = 8."], "8 days")],
        ["Treating inverse proportion as direct: more workers means less time, not more.",
         "Adding instead of multiplying: if 4 cost $6, then 8 cost $12, not $10.",
         "Comparing best buys without using the same amount (find the cost per gram or per item).",
         "Forgetting to find k first when using <i>y</i> = <i>kx</i> or <i>y</i> = <i>k</i>/<i>x</i>."])


def main():
    sets = [S("Direct proportion", collect(one_direct, 20, R)),
            S("Direct or inverse?", collect(one_which, 20, R)),
            S("Inverse proportion", collect(one_inverse, 20, R)),
            S("Using y = kx and y = k/x", collect(one_formula, 20, R)),
            S("Best buys and problems", problems())]
    make(2, "direct-and-inverse-proportion", 8, "N2",
         "Direct and Inverse Proportion: Unitary Method, Best Buys and y = kx",
         "Secondary 2 Direct and Inverse Proportion Worksheets: Unitary Method, Best Buys, y = kx and y = k/x",
         "Direct and inverse proportion",
         "Solve problems involving direct and inverse proportion, including graphical and algebraic representations; "
         "use compound units such as unit pricing.",
         "Free Secondary 2 proportion worksheets: the unitary method, recognising direct and inverse proportion, workers and "
         "days, speed and time, y = kx and y = k/x, and best-buy problems. 100 questions with answers.",
         "Direct: both double together (find the value for 1). Inverse: one doubles, the other halves (find the total).",
         "For best buys, compare the cost per item, per gram or per litre.",
         body(),
         [("What is the difference between direct and inverse proportion?", "In direct proportion both quantities increase together at the same rate. In inverse proportion, as one increases the other decreases so that their product stays the same."),
          ("What is the unitary method?", "Find the value of one unit first, then multiply. If 5 pens cost $3.50, one costs 70p, so 8 cost $5.60."),
          ("How do I solve inverse proportion problems?", "Multiply to find the fixed total (such as builder-days), then divide by the new number."),
          ("How do I find the best buy?", "Work out the price of the same amount for each option, such as the cost per 100 g. The lowest is the best value.")],
         sets, R)


if __name__ == "__main__":
    main()
