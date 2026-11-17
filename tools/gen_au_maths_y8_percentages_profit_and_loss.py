# -*- coding: utf-8 -*-
"""
AU Year 8 Maths: Percentages, Profit and Loss (Australian Curriculum v9.0: AC9M8N05)
  python3 tools/gen_au_maths_y8_percentages_profit_and_loss.py
Increasing and decreasing with multipliers, percentage change, profit and loss, reverse percentages
(including prices with GST), and money problems.
Wrong answers come from real mistakes: dividing by the new amount, finding the change but not the new amount,
working out profit as a percentage of the selling price, and taking 10% off a GST-inclusive price.
"""
import random
from fractions import Fraction as F
from au_hs import num, mcq, B, S, make, lesson, collect, QN, T, People, aud

R = random.Random(80401)
P = People(R)


def money(v):
    v = F(v)
    return aud(v) if v >= 1 else "$" + "%.2f" % float(v)


def QM(q, ans, wrongs, e):
    return QN(q, ans, [w for w in wrongs if w is not None and w > 0 and (F(w) * 100).denominator == 1], e, fmt=money, near=(1, -1, 10, -10))


def pct(v):
    return num(v) + "%"


# ------------------------------------------------------------ set 1: multipliers
def one_mult(r):
    p = r.choice([5, 8, 12, 15, 17.5, 20, 25, 30, 35, 40, 3, 2.5, 60])
    p = F(str(p))
    up = r.random() < 0.5
    m = (100 + p) / 100 if up else (100 - p) / 100
    if r.random() < 0.4:
        q = "What multiplier is used to %s an amount by %s?" % ("increase" if up else "decrease", B(pct(p)))
        wr = [num((100 - p) / 100 if up else (100 + p) / 100), num(p / 100), num(p)]
        e = "%s%% %s %s%% = %s%%, so multiply by <b>%s</b>." % ("100", "+" if up else "−", num(p), num(m * 100), num(m))
        return T(q, num(m), [w for w in wr if w != num(m)], e)
    amt = r.choice([40, 60, 80, 120, 150, 240, 360, 480, 600, 850, 1200, 2400])
    ans = amt * m
    if (ans * 100).denominator != 1:
        return None
    q = "%s %s by %s." % ("Increase" if up else "Decrease", B(money(amt)), B(pct(p)))
    e = "Multiplier = %s. %s × %s = <b>%s</b>." % (num(m), num(m), num(amt), money(ans))
    return QM(q, ans, [amt * p / 100, amt * (100 - p) / 100 if up else amt * (100 + p) / 100, amt + p if up else amt - p], e)


# ------------------------------------------------------------ set 2: percentage change
def one_change(r):
    old = r.choice([20, 25, 40, 50, 80, 120, 150, 200, 250, 400, 500, 800])
    p = r.choice([5, 10, 12, 15, 20, 25, 30, 40, 50, 60, 75])
    up = r.random() < 0.5
    new = F(old * (100 + p if up else 100 - p), 100)
    if new.denominator != 1:
        return None
    q = "A price changes from %s to %s. What is the percentage %s?" % (money(old), money(new), "increase" if up else "decrease")
    ch = abs(new - old)
    e = "Change = %s. Percentage change = change ÷ original × 100 = %s ÷ %s × 100 = <b>%s%%</b>." % (money(ch), num(ch), num(old), num(p))
    wr = [ch * 100 / new, ch, F(new * 100, old)]
    return QN(q, p, [w for w in wr if w.denominator <= 4 and w != p], e, unit="%")


# ------------------------------------------------------------ set 3: profit and loss
def one_profit(r):
    cost = r.choice([20, 25, 40, 50, 60, 80, 120, 150, 200, 240, 400, 500])
    p = r.choice([10, 15, 20, 25, 30, 40, 50, 60, 75])
    up = r.random() < 0.6
    sell = F(cost * (100 + p if up else 100 - p), 100)
    if sell.denominator != 1:
        return None
    word = "profit" if up else "loss"
    item = r.choice(["skateboard", "bike helmet", "pair of runners", "school bag", "cricket bat", "surfboard leash", "lamp", "backpack"])
    ch = abs(sell - cost)
    if r.random() < 0.35:
        q = "A shop buys a %s for %s and sells it for %s. How much %s does it make?" % (item, money(cost), money(sell), word)
        e = "%s = %s − %s = <b>%s</b>." % (word.capitalize(), money(max(sell, cost)), money(min(sell, cost)), money(ch))
        return QM(q, ch, [sell + cost, ch * 2, sell], e)
    q = "A shop buys a %s for %s and sells it for %s. What is the percentage %s?" % (item, money(cost), money(sell), word)
    e = "%s = %s. Percentage %s = %s ÷ cost price × 100 = %s ÷ %s × 100 = <b>%d%%</b>." % (word.capitalize(), money(ch), word, word, num(ch), num(cost), p)
    wr = [ch * 100 / sell, ch, F(sell * 100, cost)]
    return QN(q, p, [w for w in wr if w.denominator <= 4 and w != p], e, unit="%")


# ------------------------------------------------------------ set 4: reverse percentages
def one_reverse(r):
    p = r.choice([10, 20, 25, 15, 30, 40, 5, 50])
    up = r.random() < 0.5
    orig = r.choice([40, 60, 80, 120, 160, 200, 240, 300, 400, 480, 600])
    new = F(orig * (100 + p if up else 100 - p), 100)
    if new.denominator != 1:
        return None
    m = F(100 + p if up else 100 - p, 100)
    if up:
        q = "After a %d%% increase, a gym membership costs %s. What was the price before the increase?" % (p, money(new))
    else:
        q = "In a sale with %d%% off, a jacket costs %s. What was the original price?" % (p, money(new))
    e = "%s is %s%% of the original. Original = %s ÷ %s = <b>%s</b>." % (money(new), num(m * 100), num(new), num(m), money(orig))
    wrong = new * (100 - p) / 100 if up else new * (100 + p) / 100       # took the % of the new price
    return QM(q, orig, [wrong, new - p if up else new + p, new * m], e)


def one_gst(r):
    pre = r.choice([20, 30, 40, 50, 60, 70, 80, 90, 120, 150, 200, 250, 300, 450])
    inc = F(pre * 11, 10)
    item = r.choice(["haircut", "pair of shoes", "concert ticket", "tool kit", "board game", "plumbing job"])
    if r.random() < 0.5:
        q = "A %s costs %s including 10%% GST. What is the price before GST?" % (item, money(inc))
        e = "%s is 110%% of the price before GST. %s ÷ 1.1 = <b>%s</b>." % (money(inc), num(inc), money(pre))
        return QM(q, pre, [inc * F(9, 10), inc - 10, inc / F(11, 10) * F(9, 10)], e)
    q = "A %s costs %s including 10%% GST. How much GST is included?" % (item, money(inc))
    e = "Price before GST = %s ÷ 1.1 = %s. GST = %s − %s = <b>%s</b>." % (num(inc), money(pre), money(inc), money(pre), money(F(pre, 10)))
    return QM(q, F(pre, 10), [inc / 10, pre, F(pre, 10) * 2], e)


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    data = [
        ("A ute bought for $32 000 loses 15% of its value in a year. What is it worth after one year?", F(27200), [F(4800), F(36800), F(31985)], "0.85 × 32 000 = <b>$27 200</b>."),
        ("A shop buys a hoodie for $20 and sells it for $32. What is the percentage profit?", F(60), [F(12), F(375, 10), F(160)], "Profit = $12. 12 ÷ 20 × 100 = <b>60%</b>.", "%"),
        ("A TV costs $990 including GST at 10%. What was the price before GST?", F(900), [F(891), F(980), F(1089)], "$990 is 110%, so the price before GST = 990 ÷ 1.1 = <b>$900</b>."),
        ("A town's population rose from 25 000 to 27 500. What is the percentage increase?", F(10), [F(2500), F(11), F("9.09")], "Increase = 2500. 2500 ÷ 25 000 × 100 = <b>10%</b>.", "%"),
        ("Isla's wage of $24.50 an hour rises by 4%. What is her new hourly wage?", F("25.48"), [F("0.98"), F("28.50"), F("24.54")], "1.04 × 24.50 = <b>$25.48</b>."),
        ("A jacket is reduced by 30% to $56. What was the original price?", F(80), [F("72.80"), F(86), F("39.20")], "$56 is 70% of the original. 56 ÷ 0.7 = <b>$80</b>."),
        ("A café meal costs $40 before GST. What does it cost with 10% GST added?", F(44), [F(4), F(50), F(36)], "1.1 × 40 = <b>$44</b>."),
        ("A price goes up by 10% and then down by 10%. Compared with the start, the final price is…", "1% less", ["the same", "1% more", "10% less"], "1.1 × 0.9 = 0.99, so the final price is <b>1% less</b>."),
        ("Which is the bigger percentage increase: $50 to $60, or $80 to $95?", "$50 to $60", ["$80 to $95", "They are the same", "You cannot tell"], "$50 to $60 is 20%; $80 to $95 is 18.75%. So <b>$50 to $60</b>."),
        ("A house price fell from $750 000 to $705 000. What is the percentage decrease?", F(6), [F(45000), F(94), F("6.38")], "Decrease $45 000. 45 000 ÷ 750 000 × 100 = <b>6%</b>.", "%"),
        ("After a 25% increase, a ferry fare is $8.00. What was it before?", F("6.40"), [F(6), F("7.75"), F(10)], "$8 is 125%. 8 ÷ 1.25 = <b>$6.40</b>."),
        ("A bookshop buys a book for $16 and sells it for $12 in a clearance sale. What is the percentage loss?", F(25), [F(4), F("33.33"), F(75)], "Loss $4. 4 ÷ 16 × 100 = <b>25%</b>.", "%"),
        ("A receipt shows a total of $66 including GST. How much of this is GST?", F(6), [F("6.60"), F(60), F("5.40")], "Price before GST = 66 ÷ 1.1 = 60, so GST = <b>$6</b>."),
        ("A phone is reduced from $350 to $280. What percentage is this reduction?", F(20), [F(25), F(70), F(80)], "$70 off. 70 ÷ 350 × 100 = <b>20%</b>.", "%"),
        ("Which calculation increases $72 by 15%?", "72 × 1.15", ["72 × 0.15", "72 × 1.5", "72 + 15"], "Increase by 15% → multiplier 1.15: <b>72 × 1.15</b>."),
        ("Which calculation finds the original price if $68 is the price after a 15% discount?", "68 ÷ 0.85", ["68 × 0.85", "68 × 1.15", "68 ÷ 1.15"], "$68 is 85% of the original, so <b>68 ÷ 0.85</b>."),
        ("A gum tree grew from 40 cm to 52 cm. What is the percentage increase?", F(30), [F(12), F("23.08"), F(130)], "Increase 12 cm. 12 ÷ 40 × 100 = <b>30%</b>.", "%"),
        ("A retailer wants a 40% profit on a scooter that costs her $85. What should the selling price be?", F(119), [F(34), F(125), F("141.67")], "1.4 × 85 = <b>$119</b>."),
        ("A laptop loses 20% of its value each year (it is worth 80% of the year before). It costs $1500 new. What is it worth after 2 years?", F(960), [F(900), F(1200), F(540)], "1500 × 0.8 = 1200, then 1200 × 0.8 = <b>$960</b>."),
        ("A netball club had 160 members. It now has 136. What is the percentage decrease?", F(15), [F(24), F("17.65"), F(85)], "Decrease 24. 24 ÷ 160 × 100 = <b>15%</b>.", "%"),
    ]
    for row in data:
        q, a, w, e = row[:4]
        unit = row[4] if len(row) > 4 else None
        if isinstance(a, str):
            its.append(T(q, a, w, e))
        elif unit == "%":
            its.append(mcq(q, (num(a) + "%", a), [(num(x) + "%", x) for x in w if x != a], e))
        else:
            its.append(mcq(q, (money(a), a), [(money(x), x) for x in w if x != a], e))
    return its


def body():
    return lesson(
        "<p>A <b>multiplier</b> does a percentage change in one step: increase by 15% → × 1.15; decrease by 15% → × 0.85.</p>"
        "<p><b>Percentage change</b> = change ÷ original × 100. In business, <b>percentage profit or loss</b> = profit or loss ÷ cost price × 100.</p>"
        "<p><b>Reverse percentage</b>: if the new amount is 85% of the original, divide by 0.85 to find the original. "
        "A price that includes 10% GST is 110% of the price before GST, so divide by 1.1.</p>",
        [("Increase $240 by 17.5%.", ["Multiplier 1.175.", "1.175 × 240 = 282."], "$282"),
         ("A shop buys a lamp for $80 and sells it for $92. Find the percentage profit.", ["Profit = $12.", "12 ÷ 80 × 100 = 15."], "15%"),
         ("A price including GST is $77. Find the price before GST.", ["$77 is 110%.", "77 ÷ 1.1 = 70."], "$70")],
        ["Dividing by the new amount when finding a percentage change. Always divide by the original (the cost price for profit and loss).",
         "Stopping at the change: a 15% increase on $240 is $276, not $36.",
         "Taking 10% off a GST-inclusive price to remove GST: $77 − $7.70 = $69.30 is wrong; 77 ÷ 1.1 = $70.",
         "Using 0.15 instead of 1.15 to increase by 15%."])


def main():
    sets = [S("Increase and decrease with multipliers", collect(one_mult, 20, R)),
            S("Finding the percentage change", collect(one_change, 20, R)),
            S("Profit and loss", collect(one_profit, 20, R)),
            S("Reverse percentages and GST", collect(one_reverse, 14, R) + collect(one_gst, 6, R)),
            S("Percentage problems", problems())]
    make(8, "percentages-profit-and-loss", 4, "AC9M8N05",
         "Percentages, Profit and Loss: Multipliers, Percentage Change and GST",
         "Year 8 Percentages Worksheets: Percentage Change, Profit and Loss and GST (Free, Answer Key)",
         "Percentages, profit and loss",
         "use mathematical modelling to solve practical problems involving rational numbers and percentages, including financial contexts; "
         "formulate problems, choosing representations and efficient calculation strategies, using digital tools as appropriate; "
         "interpret and communicate solutions in terms of the situation, justifying choices made about the representation",
         "Free Year 8 maths worksheets on percentages for the Australian Curriculum (AC9M8N05): multipliers, percentage change, "
         "profit and loss, reverse percentages and GST. 100 questions with an answer key.",
         "Increase by 15%: × 1.15. Decrease by 15%: × 0.85. Percentage change = change ÷ original × 100.",
         "To find the original amount, divide by the multiplier: a price with GST ÷ 1.1 gives the price before GST.",
         body(),
         [("How do I calculate percentage profit?", "Find the profit (selling price − cost price), divide by the cost price and multiply by 100."),
          ("What is a multiplier?", "The decimal you multiply by to make a percentage change in one step. A 20% increase is × 1.2 and a 20% decrease is × 0.8."),
          ("How do I remove GST from a price?", "GST in Australia is 10%, so a GST-inclusive price is 110% of the price before GST. Divide by 1.1. For example $66 ÷ 1.1 = $60."),
          ("How do I find the original price after a discount?", "Work out what percentage is left, write it as a decimal and divide. After 30% off, $56 ÷ 0.7 = $80.")],
         sets, R)


if __name__ == "__main__":
    main()
