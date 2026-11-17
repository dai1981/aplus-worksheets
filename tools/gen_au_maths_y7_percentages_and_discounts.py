# -*- coding: utf-8 -*-
"""
AU Year 7 Maths: Percentages and discounts (Australian Curriculum v9.0: AC9M7N09)
  python3 tools/gen_au_maths_y7_percentages_and_discounts.py
Finding percentages with and without a calculator, increasing and decreasing by a percentage, writing one
amount as a percentage of another, and financial problems (sales, GST of 10%, pay rises, deposits).
Wrong answers come from real mistakes: dividing by the percentage, finding the change but not the new
amount, adding instead of subtracting, and putting the numbers the wrong way round.
"""
import random
from fractions import Fraction as F
from au_hs import num, mcq, B, S, make, lesson, collect, QN, T, aud, People, comma

R = random.Random(70701)
P = People(R)


def money(v):
    v = F(v)
    if v.denominator == 1:
        return "$" + num(v)
    whole = int(v)
    cents = int(round((v - whole) * 100))
    return "$" + comma(whole) + ".%02d" % cents


def QM(q, ans, wrongs, e):
    return QN(q, ans, [w for w in wrongs if w is not None and w > 0], e, fmt=money, near=(1, -1, 5, -5))


# ------------------------------------------------------------ set 1: mental percentages
def one_mental(r):
    p = r.choice([10, 20, 5, 25, 50, 75, 15, 30, 35, 1, 40, 60, 12.5])
    p = F(str(p))
    amt = r.choice([40, 60, 80, 120, 160, 200, 240, 300, 360, 400, 480, 520, 640, 800, 1200])
    ans = p * amt / 100
    if ans.denominator > 4:
        return None
    if p == 10:
        how = "10%% = %s ÷ 10 = %s." % (num(amt), num(ans))
    elif p == 5:
        how = "10%% = %s, so 5%% is half of that: %s." % (num(F(amt, 10)), num(ans))
    elif p == 15:
        how = "10%% = %s and 5%% = %s, so 15%% = %s." % (num(F(amt, 10)), num(F(amt, 20)), num(ans))
    elif p in (25, 50, 75):
        how = "%s%% = %s of the amount: %s." % (num(p), {25: "1/4", 50: "1/2", 75: "3/4"}[int(p)], num(ans))
    elif p == 1:
        how = "1%% = %s ÷ 100 = %s." % (num(amt), num(ans))
    elif p == F(25, 2):
        how = "12.5%% = 1/8 of the amount: %s ÷ 8 = %s." % (num(amt), num(ans))
    else:
        how = "10%% = %s, so %s%% = %s × %s = %s." % (num(F(amt, 10)), num(p), num(p / 10), num(F(amt, 10)), num(ans))
    q = "Work out %s of %s." % (B(num(p) + "%"), B(num(amt)))
    wr = [F(amt, p) if (F(amt, p)).denominator == 1 else None, amt - ans, ans * 10, p]
    return QN(q, ans, wr, how + " The answer is <b>%s</b>." % num(ans))


# ------------------------------------------------------------ set 2: multipliers
def one_mult(r):
    p = r.choice([3, 7, 12, 17, 23, 34, 46, 58, 64, 81, 92, 8, 4])
    amt = r.choice([150, 250, 340, 420, 560, 680, 750, 920, 1250, 1800, 2400])
    ans = F(p * amt, 100)
    m = F(p, 100)
    kind = r.random()
    if kind < 0.5:
        q = "Which calculation finds %s of %s?" % (B("%d%%" % p), B(num(amt)))
        right = "%s × %s" % (num(m), num(amt))
        wr = ["%d × %s" % (p, num(amt)), "%s ÷ %d" % (num(amt), p), "%s × %s" % (num(m * 10), num(amt)) if p < 10 else "%s × %s" % (num(m / 10), num(amt))]
        return T(q, right, wr, "%d%% = %d/100 = %s, so multiply by <b>%s</b>." % (p, p, num(m), num(m)))
    q = "Use a calculator to work out %s of %s." % (B("%d%%" % p), B(num(amt)))
    return QN(q, ans, [p * amt, F(amt, p) if (F(amt, p)).denominator <= 4 else None, ans * 10, amt - ans],
              "%d%% as a decimal is %s. %s × %s = <b>%s</b>." % (p, num(m), num(m), num(amt), num(ans)))


# ------------------------------------------------------------ set 3: increase / decrease
def one_change(r):
    p = r.choice([10, 20, 5, 15, 25, 30, 40, 12, 8, 35])
    amt = r.choice([40, 60, 80, 120, 150, 200, 250, 300, 360, 450, 500, 800])
    up = r.random() < 0.5
    ch = F(p * amt, 100)
    if ch.denominator > 4:
        return None
    ans = amt + ch if up else amt - ch
    q = "%s %s by %s." % ("Increase" if up else "Decrease", B(money(amt)), B("%d%%" % p))
    mult = F(100 + p if up else 100 - p, 100)
    e = "%d%% of %s = %s. %s: %s. (Or multiply by %s.) The answer is <b>%s</b>." % (
        p, money(amt), money(ch), "Add it on" if up else "Take it off", money(ans), num(mult), money(ans))
    return QM(q, ans, [ch, amt - ch if up else amt + ch, amt + p if up else amt - p], e)


# ------------------------------------------------------------ set 4: one amount as a percentage of another
def one_as_pct(r):
    whole = r.choice([20, 25, 40, 50, 80, 200, 250, 400, 500, 60, 120, 160])
    part = r.randint(1, whole - 1)
    v = F(part * 100, whole)
    if v.denominator != 1 and v.denominator != 2:
        return None
    ctx = r.choice([("out of", ""), ("g of", " g"), ("m of", " m"), ("c of", "c")])
    if ctx[0] == "out of":
        q = "What is %s out of %s as a percentage?" % (B(num(part)), B(num(whole)))
    elif ctx[0] == "c of":
        q = "What is %s as a percentage of %s?" % (B("%dc" % part), B(aud(F(whole, 100)) if whole >= 100 else "%dc" % whole))
    else:
        q = "What is %s as a percentage of %s?" % (B(num(part) + ctx[1]), B(num(whole) + ctx[1]))
    wr = [F(whole * 100, part) if F(whole * 100, part).denominator <= 2 else None, F(part), F(part, whole) * 10 if F(part, whole) * 10 != v else None, 100 - v]
    e = "Write it as a fraction and × 100: %d/%d × 100 = <b>%s%%</b>." % (part, whole, num(v))
    return QN(q, v, wr, e, unit="%")


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    for item, price, off in [("school bag", 90, 25), ("pair of runners", 140, 20), ("bike", 360, 15), ("surfboard", 550, 30), ("video game", 84, 50)]:
        ans = F(price * (100 - off), 100)
        q = "A %s costs $%d. In a sale it has %d%% off. What is the sale price?" % (item, price, off)
        e = "%d%% of $%d = %s. $%d − %s = <b>%s</b>." % (off, price, money(F(price * off, 100)), price, money(F(price * off, 100)), money(ans))
        its.append(QM(q, ans, [F(price * off, 100), price - off, price + F(price * off, 100)], e))
    for item, price in [("phone case", 25), ("pair of headphones", 140), ("printer", 230), ("desk", 180)]:
        ans = F(price * 110, 100)
        q = "A %s costs $%d before GST. GST of 10%% is added. What is the price including GST?" % (item, price)
        e = "10%% of $%d = %s. $%d + %s = <b>%s</b>." % (price, money(F(price, 10)), price, money(F(price, 10)), money(ans))
        its.append(QM(q, ans, [F(price, 10), price + 10, F(price * 90, 100)], e))
    for name, pay, rise in [("Sienna", 1200, 4), ("Cooper", 1650, 3), ("Priya", 980, 5)]:
        ans = F(pay * (100 + rise), 100)
        q = "%s earns $%s a week. %s gets a %d%% pay rise. What is %s new weekly pay?" % (
            name, num(pay), "She" if name in ("Sienna", "Priya") else "He", rise, "her" if name in ("Sienna", "Priya") else "his")
        e = "%d%% of $%s = %s. New pay: <b>%s</b>." % (rise, num(pay), money(F(pay * rise, 100)), money(ans))
        its.append(QM(q, ans, [F(pay * rise, 100), pay + rise, F(pay * (100 - rise), 100)], e))
    for cost, dep in [(1200, 10), (640, 15), (2500, 20)]:
        ans = F(cost * dep, 100)
        q = "A school camp costs $%s. A %d%% deposit is paid first. How much is the deposit?" % (num(cost), dep)
        e = "%d%% of $%s = %s × %s = <b>%s</b>." % (dep, num(cost), num(F(dep, 100)), num(cost), money(ans))
        its.append(QM(q, ans, [cost - ans, F(cost, dep) if F(cost, dep).denominator == 1 else cost + ans, ans * 10], e))
    for n, total, what in [(21, 30, "students catch the bus to school"), (36, 45, "lollies in a bag are red"), (54, 120, "tickets were sold online"),
                           (11, 20, "answers in a quiz were correct"), (72, 80, "tomato seeds sprouted")]:
        v = F(n * 100, total)
        q = "%d out of %d %s. What percentage is this?" % (n, total, what)
        e = "%d/%d × 100 = <b>%s%%</b>." % (n, total, num(v))
        its.append(QN(q, v, [F(n), F(total - n) * 100 / total, v / 10], e, unit="%"))
    return its


def body():
    return lesson(
        "<p>Without a calculator, build from easy percentages: <b>10%</b> = ÷ 10, <b>5%</b> = half of 10%, "
        "<b>1%</b> = ÷ 100, <b>50%</b> = half, <b>25%</b> = a quarter.</p>"
        "<p>With a calculator, use a <b>multiplier</b>: 17% of 340 = 0.17 × 340. To increase by 20%, multiply by 1.2; "
        "to decrease by 20%, multiply by 0.8.</p>"
        "<p>To write one amount as a percentage of another: divide, then × 100.</p>",
        [("Find 35% of 240.", ["10% = 24, so 30% = 72.", "5% = 12.", "35% = 72 + 12."], "84"),
         ("Decrease $80 by 15%.", ["15% of $80 = $12.", "$80 − $12 = $68. (Or 0.85 × 80.)"], "$68"),
         ("What is 18 out of 30 as a percentage?", ["18/30 = 0.6.", "0.6 × 100 = 60%."], "60%")],
        ["Dividing by the percentage: 20% of 80 is 16, not 80 ÷ 20 = 4.",
         "Stopping at the change: a 25% discount on $80 makes the price $60, not $20.",
         "Using 0.5 for 5%: 5% as a decimal is 0.05.",
         "Dividing the wrong way round: 18 out of 30 is 18 ÷ 30, not 30 ÷ 18."])


def main():
    sets = [S("Percentages without a calculator", collect(one_mental, 20, R)),
            S("Using a multiplier", collect(one_mult, 20, R)),
            S("Percentage increase and decrease", collect(one_change, 20, R)),
            S("One amount as a percentage of another", collect(one_as_pct, 20, R)),
            S("Money problems", problems())]
    make(7, "percentages-and-discounts", 7, "AC9M7N09",
         "Percentages and Discounts: Percentages of Amounts, GST and Sales",
         "Year 7 Percentages Worksheets: Percentage of an Amount, Discounts, GST and Pay Rises (Free, Answer Key)",
         "Percentages and discounts",
         "use mathematical modelling to solve practical problems involving rational numbers and percentages, including financial "
         "contexts; formulate problems, choosing representations and efficient calculation strategies, using digital tools as "
         "appropriate; interpret and communicate solutions in terms of the situation, justifying choices made about the representation",
         "Free Year 7 maths worksheets on percentages for the Australian Curriculum (AC9M7N09): percentages of amounts with and "
         "without a calculator, increase and decrease, discounts, GST and pay rises. 100 questions with an answer key.",
         "10% = ÷ 10. Build other percentages from 10%, 5% and 1%.",
         "With a calculator, multiply by the decimal: 17% of 340 = 0.17 × 340. To add GST of 10%, multiply by 1.1.",
         body(),
         [("How do I find 15% of a number without a calculator?", "Find 10% by dividing by 10, halve it to get 5%, then add them together."),
          ("What is a multiplier?", "The decimal you multiply by. 17% is 0.17. To increase by 20% multiply by 1.2, and to decrease by 20% multiply by 0.8."),
          ("How do I write one number as a percentage of another?", "Divide the part by the whole and multiply by 100. 18 out of 30 = 18 ÷ 30 × 100 = 60%."),
          ("How do I add GST?", "GST in Australia is 10%. Add 10% of the price, or multiply the price by 1.1.")],
         sets, R)


if __name__ == "__main__":
    main()
