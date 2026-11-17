# -*- coding: utf-8 -*-
"""
AU Year 7 Maths: Ratios (Australian Curriculum v9.0: AC9M7N08)
  python3 tools/gen_au_maths_y7_ratios.py
Simplifying ratios (including different units), sharing in a ratio, using one known part, ratios and
fractions, recipes and other direct proportion problems.
Wrong answers come from real mistakes: dividing by the number of parts in the ratio instead of the total,
writing the fraction as part : part, ignoring units, and adding instead of scaling.
"""
import random
from fractions import Fraction as F
from math import gcd
from au_hs import num, mcq, B, S, make, lesson, collect, QN, T, fr, aud, People
gbp = aud

R = random.Random(70901)
P = People(R)


def rat(*xs):
    return " : ".join(num(x) for x in xs)


def simp(*xs):
    g = 0
    for x in xs:
        g = gcd(g, int(x))
    return tuple(int(x) // g for x in xs)


# ------------------------------------------------------------ set 1: simplifying
def one_simplify(r):
    kind = r.random()
    if kind < 0.55:
        a, b = r.randint(1, 9), r.randint(1, 9)
        if gcd(a, b) != 1 or a == b:
            return None
        k = r.randint(2, 12)
        q = "Write %s in its simplest form." % B(rat(a * k, b * k))
        small = [d for d in range(2, k) if k % d == 0]
        wr = [rat(a * k // small[0], b * k // small[0]) if small else rat(b, a), rat(b, a), rat(a + 1, b + 1) if gcd(a + 1, b + 1) == 1 else rat(a * 2, b)]
        e = "Divide both parts by the highest common factor, %d: <b>%s</b>." % (k, rat(a, b))
        return T(q, rat(a, b), wr, e)
    if kind < 0.8:
        a, b, c = r.randint(1, 6), r.randint(1, 6), r.randint(1, 6)
        if gcd(gcd(a, b), c) != 1:
            return None
        k = r.randint(2, 8)
        q = "Write %s in its simplest form." % B(rat(a * k, b * k, c * k))
        wr = [rat(c, b, a) if (a, b, c) != (c, b, a) else rat(a, c, b), rat(a * 2, b * 2, c * 2), rat(a, b, c + 1)]
        e = "Divide every part by %d: <b>%s</b>." % (k, rat(a, b, c))
        return T(q, rat(a, b, c), [w for w in wr if w != rat(a, b, c)], e)
    pairs = [(50, "cm", 2, "m", 100), (300, "g", 1, "kg", 1000), (45, "minutes", 2, "hours", 60), (75, "c", 3, "$", 100),
             (400, "ml", 2, "litres", 1000), (20, "cm", 1, "m", 100), (40, "minutes", 1, "hour", 60), (250, "m", 2, "km", 1000)]
    a, ua, b, ub, conv = r.choice(pairs)
    bb = b * conv
    sa, sb = simp(a, bb)
    shown_b = ("$%d" % b) if ub == "$" else "%d %s" % (b, ub)
    shown_a = ("%dc" % a) if ua == "c" else "%d %s" % (a, ua)
    q = "Write the ratio %s in its simplest form." % B("%s : %s" % (shown_a, shown_b))
    wr = [rat(*simp(a, b)), rat(a, b), rat(sb, sa)]
    e = "Change to the same units first: %s = %s. Then %d : %d = <b>%s</b>." % (
        shown_b, ("%dc" % bb) if ua == "c" else "%d %s" % (bb, ua), a, bb, rat(sa, sb))
    return T(q, rat(sa, sb), [w for w in wr if w != rat(sa, sb)], e)


# ------------------------------------------------------------ set 2: sharing
def one_share(r):
    a, b = r.randint(1, 7), r.randint(1, 7)
    if a == b or gcd(a, b) != 1:
        return None
    three = r.random() < 0.3
    c = r.randint(1, 5) if three else 0
    parts = a + b + c
    one = r.randint(2, 30)
    total = parts * one
    names = [P.next()[0] for _ in range(3)]
    if three:
        q = "Share $%s between %s, %s and %s in the ratio %s. How much does %s get?" % (num(total), names[0], names[1], names[2], rat(a, b, c), names[1])
        ans = b * one
        e = "%d + %d + %d = %d parts. One part = $%s ÷ %d = $%d. %s gets %d × $%d = <b>$%s</b>." % (a, b, c, parts, num(total), parts, one, names[1], b, one, num(ans))
        wr = [F(total, b) if total % b == 0 else None, a * one, total // 3 if total % 3 == 0 else None, F(total, a + b) * b if F(total, a + b).denominator == 1 else None]
    else:
        q = "Share $%s between %s and %s in the ratio %s. How much does %s get?" % (num(total), names[0], names[1], rat(a, b), names[0])
        ans = a * one
        e = "%d + %d = %d parts. One part = $%s ÷ %d = $%d. %s gets %d × $%d = <b>$%s</b>." % (a, b, parts, num(total), parts, one, names[0], a, one, num(ans))
        wr = [b * one, F(total, a) if total % a == 0 else None, F(total, 2)]
    return QN(q, ans, [w for w in wr if w is not None and w != ans], e, fmt=gbp)


# ------------------------------------------------------------ set 3: one part known, difference
def one_part(r):
    a, b = r.randint(1, 9), r.randint(1, 9)
    if a == b or gcd(a, b) != 1:
        return None
    one = r.randint(2, 12)
    kind = r.randint(0, 2)
    things = r.choice([("boys", "girls", "students"), ("red beads", "blue beads", "beads"), ("cats", "dogs", "animals"), ("adults", "children", "people")])
    if kind == 0:
        q = "The ratio of %s to %s is %s. There are %d %s. How many %s are there?" % (things[0], things[1], rat(a, b), a * one, things[0], things[1])
        ans = b * one
        e = "%d %s is %d part%s, so 1 part = %d. %s: %d × %d = <b>%d</b>." % (a * one, things[0], a, "" if a == 1 else "s", one, things[1].capitalize(), b, one, ans)
        return QN(q, ans, [a * one + b - a if a * one + b - a > 0 else None, F(a * one * a, b) if (a * one * a) % b == 0 else a * one * b, a * one + (b - a) if b > a else None, a * one * b], e)
    if kind == 1:
        q = "The ratio of %s to %s is %s. There are %d %s altogether. How many %s are there?" % (things[0], things[1], rat(a, b), (a + b) * one, things[2], things[1])
        ans = b * one
        e = "%d + %d = %d parts. 1 part = %d ÷ %d = %d. %s: %d × %d = <b>%d</b>." % (a, b, a + b, (a + b) * one, a + b, one, things[1].capitalize(), b, one, ans)
        return QN(q, ans, [a * one, F((a + b) * one, b) if ((a + b) * one) % b == 0 else (a + b) * one - b, (a + b) * one // 2 if ((a + b) * one) % 2 == 0 else None], e)
    if a == b:
        return None
    big, small = max(a, b), min(a, b)
    diff = (big - small) * one
    q = "The ratio of %s to %s is %s. There are %d more %s than %s. How many %s are there altogether?" % (
        things[0], things[1], rat(a, b), diff, things[0] if a > b else things[1], things[1] if a > b else things[0], things[2])
    ans = (a + b) * one
    e = "The difference is %d − %d = %d part%s = %d, so 1 part = %d. Total = %d parts = <b>%d</b>." % (
        big, small, big - small, "" if big - small == 1 else "s", diff, one, a + b, ans)
    return QN(q, ans, [diff * (a + b), big * one, diff + (a + b)], e)


# ------------------------------------------------------------ set 4: ratio and fractions, recipes
def one_frac(r):
    a, b = r.randint(1, 8), r.randint(1, 8)
    if a == b or gcd(a, b) != 1:
        return None
    if r.random() < 0.5:
        q = "Red and blue counters are in the ratio %s. What fraction of the counters are red?" % B(rat(a, b))
        right = fr(a, a + b)
        wr = [fr(a, b), fr(b, a + b), fr(b, a) if b > a or True else None]
        e = "There are %d + %d = %d parts and %d are red: <b>%s</b>." % (a, b, a + b, a, right)
        return T(q, right, wr, e)
    q = "%s of a class are girls. What is the ratio of girls to boys?" % B(fr(a, a + b))
    right = rat(a, b)
    wr = [rat(a, a + b), rat(b, a), rat(a + b, a)]
    e = "Out of every %d students, %d are girls and %d are boys: <b>%s</b>." % (a + b, a, b, right)
    return T(q, right, wr, e)


def one_recipe(r):
    serve = r.choice([2, 4, 5, 6, 8])
    new = r.choice([s for s in [1, 3, 4, 6, 9, 10, 12, 15, 20] if s != serve])
    item, qty, unit = r.choice([("flour", 200, "g"), ("milk", 300, "ml"), ("sugar", 120, "g"), ("butter", 80, "g"), ("eggs", 2, ""),
                                ("rice", 150, "g"), ("oats", 250, "g")])
    ans = F(qty * new, serve)
    if ans.denominator != 1 and (unit == "" or ans.denominator > 2):
        return None
    if unit == "":
        q = "A recipe for %d people uses %d eggs. How many eggs are needed for %d people?" % (serve, qty, new)
        fmt = lambda v: num(v)
    else:
        q = "A recipe for %d people uses %d %s of %s. How many %s of %s are needed for %d people?" % (
            serve, qty, unit, item, {"g": "grams", "ml": "millilitres"}[unit], item, new)
        fmt = lambda v: num(v) + " " + unit
    e = "For 1 person: %d ÷ %d = %s. For %d people: %s × %d = <b>%s</b>." % (qty, serve, num(F(qty, serve)), new, num(F(qty, serve)), new, fmt(ans))
    return QN(q, ans, [qty + new - serve, qty * new, F(qty * serve, new) if F(qty * serve, new).denominator == 1 else None], e, fmt=fmt)


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    for d_map, scale in [(5, 25000), (4, 50000), (6, 100000), (9, 20000)]:
        km = F(d_map * scale, 100000)
        q = "A map has a scale of 1 : %s. Two towns are %d cm apart on the map. How far apart are they in real life?" % (num(scale), d_map)
        e = "%d × %s = %s cm = <b>%s km</b> (100 000 cm = 1 km)." % (d_map, num(scale), num(d_map * scale), num(km))
        its.append(QN(q, km, [km * 10, km / 10, km * 100], e, unit=" km", near=()))
    for cost, n, m in [(F("4.80"), 4, 7), (F("2.70"), 3, 10), (F("13.50"), 5, 8), (F("5.40"), 6, 15)]:
        ans = cost / n * m
        q = "%d notebooks cost %s. How much do %d notebooks cost?" % (n, gbp(cost), m)
        e = "1 notebook costs %s ÷ %d = %s. %d notebooks cost <b>%s</b>." % (gbp(cost), n, gbp(cost / n), m, gbp(ans))
        its.append(mcq(q, (gbp(ans), ans), [(gbp(w), w) for w in [cost + (m - n), cost * m, cost / n, ans + 1] if w != ans], e))
    data = [
        ("Cordial is mixed with water in the ratio 1 : 5. How much water is needed for 60 ml of cordial?", 300, [65, 240, 360], "1 part = 60 ml, so water = 5 × 60 = <b>300 ml</b>.", " ml"),
        ("Concrete is cement, sand and gravel in the ratio 1 : 2 : 3. How much sand is in 48 kg of concrete?", 16, [8, 24, 32], "1 + 2 + 3 = 6 parts. 1 part = 8 kg. Sand = 2 × 8 = <b>16 kg</b>.", " kg"),
        ("A car uses 8 litres of petrol for 100 km. How far can it go on 30 litres?", 375, [130, 240, 800], "1 litre: 100 ÷ 8 = 12.5 km. 30 litres: 12.5 × 30 = <b>375 km</b>.", " km"),
        ("The ratio of teachers to students on an excursion must be 1 : 10. How many teachers are needed for 74 students?", 8, [7, F(37, 5), 10], "74 ÷ 10 = 7.4, so <b>8</b> teachers are needed (round up, because you cannot have part of a teacher).", ""),
        ("Paint is mixed blue : white = 3 : 4. Harper has 12 litres of white. How much blue does she need?", 9, [16, 11, 3], "4 parts = 12 litres, so 1 part = 3 litres. Blue = 3 × 3 = <b>9 litres</b>.", " litres"),
        ("The angles in a triangle are in the ratio 2 : 3 : 4. What is the largest angle?", 80, [60, 40, 120], "9 parts = 180°, so 1 part = 20°. Largest = 4 × 20 = <b>80°</b>.", "°"),
        ("A school has 720 students. The ratio of boys to girls is 5 : 4. How many more boys than girls are there?", 80, [400, 320, 160], "9 parts = 720, so 1 part = 80. Boys 400, girls 320: <b>80</b> more boys.", ""),
        ("A photo 10 cm wide is enlarged so that it is 15 cm wide. Its height was 8 cm. What is the new height?", 12, [13, 10, 23], "Scale factor = 15 ÷ 10 = 1.5. New height = 8 × 1.5 = <b>12 cm</b>.", " cm"),
        ("Ruby and Tom share some money in the ratio 3 : 5. Tom gets $40. How much money was there altogether?", 64, [24, 43, 200], "5 parts = $40, so 1 part = $8. Total = 8 × $8 = <b>$64</b>.", "$"),
        ("Which ratio is the same as 8 : 12?", "10 : 15", ["12 : 16", "12 : 8", "4 : 8"], "8 : 12 = 2 : 3, and 10 : 15 = 2 : 3. So <b>10 : 15</b>.", None),
        ("In a netball team of 12 players, the ratio of Year 7 to Year 8 students is 1 : 2. How many are from Year 8?", 8, [4, 6, 24], "3 parts = 12, so 1 part = 4. Year 8 = 2 × 4 = <b>8</b>.", ""),
        ("A recipe uses rolled oats and honey in the ratio 5 : 1. How much honey goes with 400 g of oats?", 80, [2000, 395, 100], "5 parts = 400 g, so 1 part = <b>80 g</b>.", " g"),
    ]
    for q, a, w, e, unit in data:
        if unit is None:
            its.append(T(q, a, w, e))
        elif unit == "$":
            its.append(QN(q, a, w, e, fmt=lambda v: "$" + num(v)))
        else:
            its.append(QN(q, a, [x for x in w if F(x).denominator <= 2], e, unit=unit))
    return its


def body():
    return lesson(
        "<p>A ratio compares parts: 2 : 3 means for every 2 of one thing there are 3 of the other. "
        "Simplify a ratio like a fraction, by dividing every part by the same number. Use the same units first.</p>"
        "<p>To <b>share in a ratio</b>: add the parts, find the value of one part, then multiply.</p>",
        [("Share $45 in the ratio 2 : 3.", ["2 + 3 = 5 parts.", "1 part = $45 ÷ 5 = $9.", "2 × $9 = $18 and 3 × $9 = $27."], "$18 and $27"),
         ("Simplify 50 cm : 2 m.", ["2 m = 200 cm.", "50 : 200 = 1 : 4."], "1 : 4"),
         ("The ratio of boys to girls is 3 : 4. There are 12 boys. How many girls?", ["3 parts = 12, so 1 part = 4.", "Girls = 4 × 4 = 16."], "16")],
        ["Dividing by the number of people instead of the number of parts: $45 in the ratio 2 : 3 is not $22.50 each.",
         "Writing 2 : 3 as the fraction 2/3. Red is 2/5 of the total, because there are 5 parts.",
         "Simplifying without changing units: 50 cm : 2 m is not 25 : 1.",
         "Adding instead of multiplying in recipes: for 6 people instead of 4, multiply by 1.5."])


def main():
    sets = [S("Simplifying ratios", collect(one_simplify, 20, R)),
            S("Sharing in a ratio", collect(one_share, 20, R)),
            S("Using one part of a ratio", collect(one_part, 20, R)),
            S("Ratios, fractions and recipes", collect(one_frac, 8, R) + collect(one_recipe, 12, R)),
            S("Problems", problems())]
    make(7, "ratios", 9, "AC9M7N08",
         "Ratios: Simplifying, Sharing and Scaling",
         "Year 7 Ratio Worksheets: Simplifying Ratios, Sharing in a Ratio, Map Scales and Recipes (Free, Answer Key)",
         "Ratios",
         "recognise, represent and solve problems involving ratios",
         "Free Year 7 maths worksheets on ratios for the Australian Curriculum (AC9M7N08): simplify ratios, share amounts in a "
         "ratio, use one known part, link ratios and fractions, recipes and map scales. 100 questions with an answer key.",
         "To share in a ratio: add the parts, find one part, then multiply.",
         "Simplify a ratio by dividing every part by the same number. Make the units the same first.",
         body(),
         [("How do I share an amount in a ratio?", "Add the numbers in the ratio to get the total parts. Divide the amount by the total parts to find one part, then multiply by each number in the ratio."),
          ("How do ratios relate to fractions?", "In the ratio 2 : 3 there are 5 parts, so the first share is 2/5 of the total and the second is 3/5."),
          ("How do I simplify a ratio with units?", "Change both quantities into the same unit, then divide by the highest common factor. 50 cm : 2 m = 50 : 200 = 1 : 4."),
          ("What does a map scale of 1 : 25 000 mean?", "1 cm on the map is 25 000 cm (250 m) in real life.")],
         sets, R)


if __name__ == "__main__":
    main()
