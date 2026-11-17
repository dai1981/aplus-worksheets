# -*- coding: utf-8 -*-
"""
UK Year 9 Maths: Ratio Problems and Best Buys (KS3 Ratio, proportion and rates of change)
  python3 tools/gen_uk_maths_y9_ratio_problems_and_best_buys.py
Sharing in a ratio with three parts, problems given a difference or one share, best buys by unit price,
combining ratios (a : b and b : c), ratios as fractions, and recipe problems.
Wrong answers come from real mistakes: dividing by the number of people instead of the number of parts,
mixing up which share is which, choosing the cheapest pack instead of the best value, and adding ratios
instead of making the shared part equal.
"""
import random
from fractions import Fraction as F
from uk_ks3 import num, B, S, make, lesson, collect, T, gbp, GIRLS, BOYS

R = random.Random(91601)


def rat(*a):
    return " : ".join(num(x) for x in a)


def names(r, k):
    return r.sample(GIRLS + BOYS, k)


def pick(right, c):
    out = []
    for x in c:
        if x != right and x not in out:
            out.append(x)
    return out[:3]


# ------------------------------------------------------------ set 1: sharing in a ratio with three parts
def one_share3(r):
    a, b, c = r.randint(1, 6), r.randint(1, 6), r.randint(1, 6)
    from math import gcd
    if len({a, b, c}) < 3 or gcd(gcd(a, b), c) > 1:
        return None
    parts = a + b + c
    unit = r.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25])
    tot = parts * unit
    n = names(r, 3)
    who = r.randint(0, 2)
    q = "%s, %s and %s share %s in the ratio %s. How much does %s get?" % (n[0], n[1], n[2], gbp(tot), rat(a, b, c), n[who])
    share = [a, b, c][who] * unit
    right = gbp(share)
    wr = [gbp(F(tot, 3)) if tot % 3 == 0 else gbp(share + unit), gbp([a, b, c][(who + 1) % 3] * unit), gbp(F(tot, [a, b, c][who])) if tot % [a, b, c][who] == 0 else gbp(share - unit),
          gbp([a, b, c][who] * F(tot, 10))]
    e = "%d + %d + %d = %d parts. One part = %s ÷ %d = %s. %s gets %d × %s = <b>%s</b>." % (
        a, b, c, parts, gbp(tot), parts, gbp(unit), n[who], [a, b, c][who], gbp(unit), right)
    return T(q, right, pick(right, wr), e)


# ------------------------------------------------------------ set 2: given a difference or one share
def one_diff(r):
    a, b = r.randint(1, 8), r.randint(1, 9)
    if a >= b or F(a, b).denominator != b:
        return None
    unit = r.choice([3, 4, 5, 6, 7, 8, 9, 12, 15])
    n = names(r, 2)
    k = r.randint(0, 2)
    if k == 0:
        diff = (b - a) * unit
        q = "%s and %s share some sweets in the ratio %s. %s gets %d more sweets than %s. How many sweets are there altogether?" % (
            n[0], n[1], rat(a, b), n[1], diff, n[0])
        ans = (a + b) * unit
        wr = [diff * (a + b), (a + b) * diff // (b - a) + diff if (b - a) > 1 else ans + unit, b * unit, a * unit + diff + unit]
        e = "The difference is %d − %d = %d part%s = %d, so one part = %d. Total = %d parts = <b>%d</b>." % (
            b, a, b - a, "" if b - a == 1 else "s", diff, unit, a + b, ans)
    elif k == 1:
        sh = a * unit
        q = "Money is shared between %s and %s in the ratio %s. %s gets %s. How much does %s get?" % (n[0], n[1], rat(a, b), n[0], gbp(sh), n[1])
        right = gbp(b * unit)
        wr = [gbp((a + b) * unit), gbp(sh * b), gbp(sh + b) if sh + b != b * unit else gbp(b * unit + unit), gbp((b - a) * unit)]
        e = "%s's %d part%s = %s, so one part = %s. %s gets %d × %s = <b>%s</b>." % (n[0], a, "" if a == 1 else "s", gbp(sh), gbp(unit), n[1], b, gbp(unit), right)
        return T(q, right, pick(right, wr), e)
    else:
        tot = (a + b) * unit
        q = "The ratio of boys to girls in a club is %s. There are %d children. How many more girls than boys are there?" % (rat(a, b), tot)
        ans = (b - a) * unit
        wr = [b * unit, b - a, tot // 2 - a * unit if tot % 2 == 0 and tot // 2 - a * unit != ans else ans + unit, a * unit]
        e = "%d parts = %d, so one part = %d. Girls − boys = %d − %d = %d part%s = <b>%d</b>." % (a + b, tot, unit, b, a, b - a, "" if b - a == 1 else "s", ans)
    return T(q, str(ans), pick(str(ans), [str(w) for w in wr]), e)


# ------------------------------------------------------------ set 3: best buys
ITEMS = [("cereal", "g", [(500, 750, 1000)], (180, 350)), ("orange juice", "ml", [(500, 1000, 1500)], (90, 300)),
         ("rice", "kg", [(1, 2, 5)], (150, 300)), ("washing-up liquid", "ml", [(400, 500, 900)], (80, 250)),
         ("pasta", "g", [(500, 1000)], (60, 200)), ("cola", "ml", [(500, 1250, 2000)], (80, 180))]


def one_best(r):
    it, u, sizes, (lo, hi) = r.choice(ITEMS)
    s1, s2 = sorted(r.sample(sizes[0], 2))
    p1 = r.randint(lo // 10, hi // 10) * 10 if u != "kg" else r.randint(lo // 10, hi // 10) * 10
    # unit price comparisons on a common amount
    base = {"g": 100, "ml": 100, "kg": 1}[u]
    up1 = F(p1, s1) * base
    # choose p2 so the big pack is better or worse, never equal
    better_big = r.random() < 0.6
    for _ in range(50):
        f = r.uniform(0.75, 0.95) if better_big else r.uniform(1.05, 1.25)
        p2 = int(round(float(up1 * s2 / base) * f / 5.0)) * 5
        up2 = F(p2, s2) * base
        if p2 > p1 and up2 != up1 and ((up2 < up1) == better_big):
            break
    else:
        return None
    lab = lambda s: ("%s %s" % (num(s), u)) if u != "kg" else ("%s kg" % num(s))
    q = "%s is sold in two sizes: %s for %s, or %s for %s. Which is better value?" % (
        it[0].upper() + it[1:], lab(s1), gbp(F(p1, 100)), lab(s2), gbp(F(p2, 100)))
    right = "The %s pack" % lab(s2) if better_big else "The %s pack" % lab(s1)
    other = "The %s pack" % lab(s1) if better_big else "The %s pack" % lab(s2)
    wr = [other, "They are the same value", "You cannot tell without more information"]

    def pp(x):
        x = float(x)
        if x < 100:
            t = ("%.1f" % x).rstrip("0").rstrip(".")
            return t + "p"
        return gbp(F(int(round(x)), 100))
    e = "Compare the price per %s %s: %s for the small pack and %s for the large pack. <b>%s</b> costs less per %s %s." % (
        num(base), u, pp(up1), pp(up2), right, num(base), u)
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 4: combining ratios, fractions, scaling
def one_comb(r):
    k = r.randint(0, 2)
    if k == 0:
        a, b1 = r.randint(1, 5), r.randint(2, 5)
        b2, c = r.randint(2, 6), r.randint(1, 7)
        if b1 == b2:
            return None
        from math import gcd
        l = b1 * b2 // gcd(b1, b2)
        A, Bv, C = a * l // b1, l, c * l // b2
        g = gcd(gcd(A, Bv), C)
        A, Bv, C = A // g, Bv // g, C // g
        q = "%s and %s. Write %s as a ratio in its simplest form." % (B("<i>a</i> : <i>b</i> = %s" % rat(a, b1)), B("<i>b</i> : <i>c</i> = %s" % rat(b2, c)), B("<i>a</i> : <i>b</i> : <i>c</i>"))
        right = rat(A, Bv, C)
        wr = [rat(a, b1 + b2, c), rat(a, b1, c), rat(a * b2, b1 * b2, c * b1) if rat(a * b2, b1 * b2, c * b1) != right else rat(a, b2, c), rat(a, b2, c)]
        e = "Make the <i>b</i> parts equal: the LCM of %d and %d is %d. %s and %s give <b>%s</b>." % (
            b1, b2, l, rat(a * l // b1, l), rat(l, c * l // b2), right)
        return T(q, right, pick(right, wr), e)
    if k == 1:
        a, b = r.randint(1, 7), r.randint(1, 9)
        if a == b:
            return None
        from math import gcd
        g = gcd(a, b)
        a, b = a // g, b // g
        q = "Red and blue counters are in the ratio %s. What fraction of the counters are red?" % rat(a, b)
        fr = lambda n, d: "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (n, d)
        right = fr(a, a + b)
        wr = [fr(a, b), fr(b, a + b), fr(1, a + b) if a != 1 else fr(b, a)]
        e = "There are %d + %d = %d parts and %d of them %s red: <b>%s</b>." % (a, b, a + b, a, "is" if a == 1 else "are", right)
        return T(q, right, pick(right, wr), e)
    serves = r.choice([4, 6, 8])
    want = r.choice([x for x in (2, 3, 6, 10, 12, 9) if x != serves])
    ing, amt, u = r.choice([("flour", r.choice([200, 240, 300, 360]), "g"), ("milk", r.choice([300, 400, 480, 600]), "ml"),
                            ("sugar", r.choice([120, 150, 180, 240]), "g"), ("butter", r.choice([80, 100, 120]), "g")])
    newamt = F(amt * want, serves)
    if newamt.denominator != 1:
        return None
    q = "A recipe for %d people uses %d %s of %s. How much %s is needed for %d people?" % (serves, amt, u, ing, ing, want)
    right = "%s %s" % (num(newamt), u)
    wr = ["%s %s" % (num(amt + (want - serves) * 10), u), "%s %s" % (num(amt * want), u), "%s %s" % (num(F(amt, serves)), u) if F(amt, serves).denominator == 1 else "%s %s" % (num(amt * 2), u),
          "%s %s" % (num(amt + want - serves), u)]
    e = "%d ÷ %d = %s %s per person. × %d = <b>%s</b>." % (amt, serves, num(F(amt, serves)), u, want, right)
    return T(q, right, pick(right, wr), e)


# ------------------------------------------------------------ set 5: problems
def problems():
    data = [
        ("The ratio of cats to dogs at a shelter is 3 : 5. There are 12 more dogs than cats. How many cats are there?", "18", ["30", "6", "48"],
         "5 − 3 = 2 parts = 12, so 1 part = 6. Cats: 3 × 6 = <b>18</b>."),
        ("£1 = €1.15. How many euros do you get for £240?", "€276", ["€208.70", "€241.15", "€255"],
         "240 × 1.15 = <b>€276</b>."),
        ("£1 = $1.25. A jacket costs $75. How much is that in pounds?", "£60", ["£93.75", "£75", "£50"],
         "75 ÷ 1.25 = <b>£60</b>."),
        ("A 6-pack of yoghurts costs £2.40 and a 4-pack costs £1.80. Which is better value?", "The 6-pack", ["The 4-pack", "They are the same value", "The cheapest one"],
         "6-pack: 40p each. 4-pack: 45p each. <b>The 6-pack</b>."),
        ("Shop A sells 3 pens for £2.10. Shop B sells 5 of the same pens for £3.40. Which is cheaper per pen?", "Shop B", ["Shop A", "They are the same", "You cannot tell"],
         "A: 70p each. B: 68p each. <b>Shop B</b>."),
        ("Concrete is made from cement, sand and gravel in the ratio 1 : 2 : 4. How much sand is in 350 kg of concrete?", "100 kg", ["50 kg", "200 kg", "117 kg"],
         "1 + 2 + 4 = 7 parts. One part = 50 kg. Sand: 2 × 50 = <b>100 kg</b>."),
        ("Ages of Amelia and her grandad are in the ratio 2 : 11. Grandad is 66. How old is Amelia?", "12", ["33", "6", "55"],
         "11 parts = 66, so 1 part = 6. Amelia: 2 × 6 = <b>12</b>."),
        ("The ratio of red to green sweets is 4 : 7. After 6 red sweets are eaten, the ratio is 1 : 3. How many green sweets are there?", "42", ["21", "24", "7"],
         "Red = 4<i>k</i>, green = 7<i>k</i>. (4<i>k</i> − 6) : 7<i>k</i> = 1 : 3 gives 12<i>k</i> − 18 = 7<i>k</i>, so <i>k</i> = 3.6… Check with whole numbers: this needs <i>k</i> = 6. Green = <b>42</b>."),
        ("Paint is mixed blue to yellow in the ratio 3 : 2. Jack has 9 litres of blue. How much yellow does he need?", "6 litres", ["4 litres", "13.5 litres", "15 litres"],
         "3 parts = 9 litres, so 1 part = 3 litres. Yellow: 2 × 3 = <b>6 litres</b>."),
        ("A map has scale 1 : 25,000. Two churches are 8 cm apart on the map. How far apart are they in real life?", "2 km", ["200 m", "20 km", "3.125 km"],
         "8 × 25,000 = 200,000 cm = <b>2 km</b>."),
        ("Which is better value: 400 g of cheese for £3.20 or 250 g for £2.10?", "400 g for £3.20", ["250 g for £2.10", "They are the same", "You cannot tell"],
         "400 g: 80p per 100 g. 250 g: 84p per 100 g. <b>400 g for £3.20</b>."),
        ("Divide £90 in the ratio 2 : 3 : 4. What is the largest share?", "£40", ["£30", "£20", "£36"],
         "9 parts, one part = £10. Largest: 4 × £10 = <b>£40</b>."),
        ("In a class, the ratio of students who walk to those who do not is 2 : 3. What percentage walk?", "40%", ["66.7%", "60%", "20%"],
         "2 out of 5 parts: 2 ÷ 5 = <b>40%</b>."),
        ("<i>x</i> : <i>y</i> = 3 : 4 and <i>y</i> = 28. What is <i>x</i>?", "21", ["37.3", "27", "12"],
         "4 parts = 28, so 1 part = 7. <i>x</i> = 3 × 7 = <b>21</b>."),
        ("A 1.5 litre bottle of water costs 90p and a 500 ml bottle costs 35p. How much do you save per litre with the large bottle?", "10p", ["55p", "5p", "20p"],
         "Large: 90p ÷ 1.5 = 60p per litre. Small: 35p × 2 = 70p per litre. Saving: <b>10p</b> per litre."),
        ("Grace and Leo share £72 in the ratio 5 : 3. Grace gives Leo £6. What is the new ratio?", "13 : 11", ["5 : 3", "39 : 33", "7 : 5"],
         "Grace £45, Leo £27. After: £39 and £33, which is 39 : 33 = <b>13 : 11</b>."),
        ("A recipe uses flour and sugar in the ratio 5 : 2. How much flour is needed with 150 g of sugar?", "375 g", ["60 g", "300 g", "525 g"],
         "2 parts = 150 g, so 1 part = 75 g. Flour: 5 × 75 = <b>375 g</b>."),
        ("Which ratio is the same as 0.4 : 1.2?", "1 : 3", ["4 : 1", "2 : 3", "1 : 2"],
         "Multiply by 10: 4 : 12. Divide by 4: <b>1 : 3</b>."),
        ("A car uses 6 litres of fuel to travel 80 km. How far can it go on 15 litres?", "200 km", ["120 km", "160 km", "1,200 km"],
         "80 ÷ 6 × 15 = <b>200 km</b>."),
        ("Write the ratio 45 minutes : 2 hours in its simplest form.", "3 : 8", ["45 : 2", "9 : 24", "3 : 2"],
         "2 hours = 120 minutes. 45 : 120 = <b>3 : 8</b>."),
    ]
    # fix the sweets explanation to be clean
    data[7] = ("The ratio of red to green sweets is 2 : 5. After 4 red sweets are eaten, the ratio is 1 : 5. How many green sweets are there?", "20", ["8", "4", "25"],
               "Green stays the same. Red goes from 2 parts to 1 part, so 1 part = 4 sweets. Green: 5 × 4 = <b>20</b>.")
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>To <b>share in a ratio</b>, add the parts, find one part, then multiply. "
        "If you know a difference or one share, find what <b>one part</b> is worth first.</p>"
        "<p>For a <b>best buy</b>, compare the price for the <b>same amount</b> (per 100 g, per litre or per item). "
        "To combine <i>a</i> : <i>b</i> and <i>b</i> : <i>c</i>, make the <i>b</i> parts the same.</p>",
        [("Share £120 in the ratio 1 : 2 : 3.", ["6 parts, one part = £20."], "£20, £40, £60"),
         ("Ratio 3 : 7. The second share is £28 more.", ["4 parts = £28, so one part = £7."], "£21 and £49"),
         ("500 g for £2.50 or 750 g for £3.60?", ["50p and 48p per 100 g."], "750 g is better value")],
        ["Dividing by the number of people instead of the number of parts.",
         "Mixing up which share goes with which person.",
         "Choosing the cheapest pack instead of the best value per unit.",
         "Adding the middle numbers when combining ratios instead of making them equal."])


def main():
    sets = [S("Sharing in a ratio with three parts", collect(one_share3, 20, R)),
            S("Using one share or a difference", collect(one_diff, 20, R)),
            S("Best buys", collect(one_best, 20, R)),
            S("Combining ratios, fractions and recipes", collect(one_comb, 20, R)),
            S("Ratio and proportion problems", problems())]
    make(9, "ratio-problems-and-best-buys", 16, "R",
         "Ratio Problems and Best Buys",
         "Year 9 Ratio Problems Worksheets: Sharing in a Ratio, Best Buys and Combining Ratios",
         "Ratio Problems and Best Buys",
         "Divide a given quantity into two parts in a given part : part or part : whole ratio; express the division of a "
         "quantity into two parts as a ratio; solve problems involving direct and inverse proportion; use compound units "
         "such as unit pricing.",
         "Free Year 9 ratio problems worksheets: share in a ratio with three parts, problems with a difference or one share, "
         "best buys by unit price, combining ratios and recipes. 100 questions with answers.",
         "Find the value of one part first.",
         "Best buy: compare the price for the same amount.",
         body(),
         [("How do I share an amount in a ratio?", "Add the parts of the ratio, divide the amount by that total to find one part, then multiply by each number in the ratio."),
          ("How do I solve a ratio problem when I know the difference?", "Subtract the parts of the ratio. That number of parts equals the difference, so you can find one part."),
          ("How do I find the best buy?", "Work out the price for the same amount of each, such as per 100 g. The lower price per unit is the better value."),
          ("How do I combine two ratios?", "For a : b and b : c, multiply so the b values match, then write a : b : c.")],
         sets, R)


if __name__ == "__main__":
    main()
