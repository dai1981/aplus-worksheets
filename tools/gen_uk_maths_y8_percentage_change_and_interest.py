# -*- coding: utf-8 -*-
"""
UK Year 8 Maths: Percentage Change and Simple Interest (KS3 Ratio, proportion and rates of change)
  python3 tools/gen_uk_maths_y8_percentage_change_and_interest.py
Increasing and decreasing with multipliers, finding the percentage change, reverse percentages (finding the
original amount), simple interest, and mixed money problems.
Wrong answers come from real mistakes: dividing by the new amount, finding the change but not the new amount,
taking the percentage off the sale price to undo a discount, and using compound instead of simple interest.
"""
import random
from fractions import Fraction as F
from uk_ks3 import num, mcq, B, S, make, lesson, collect, QN, T, People

R = random.Random(80801)
P = People(R)


def money(v):
    v = F(v)
    if v.denominator == 1:
        return "£" + num(v)
    return "£" + format(float(v), ",.2f")


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


# ------------------------------------------------------------ set 3: reverse percentages
def one_reverse(r):
    p = r.choice([10, 20, 25, 15, 30, 40, 5, 50])
    up = r.random() < 0.5
    orig = r.choice([40, 60, 80, 120, 160, 200, 240, 300, 400, 480, 600])
    new = F(orig * (100 + p if up else 100 - p), 100)
    if new.denominator != 1:
        return None
    m = F(100 + p if up else 100 - p, 100)
    if up:
        q = "After a %d%% increase, a price is %s. What was the price before the increase?" % (p, money(new))
    else:
        q = "In a sale with %d%% off, a jacket costs %s. What was the original price?" % (p, money(new))
    e = "%s is %s%% of the original. Original = %s ÷ %s = <b>%s</b>." % (money(new), num(m * 100), num(new), num(m), money(orig))
    wrong = new * (100 - p) / 100 if up else new * (100 + p) / 100       # took the % of the new price
    return QM(q, orig, [wrong, new - p if up else new + p, new * m], e)


# ------------------------------------------------------------ set 4: simple interest
def one_interest(r):
    pr = r.choice([200, 500, 800, 1000, 1500, 2000, 2500, 4000, 5000])
    rate = F(str(r.choice([2, 3, 4, 5, 1.5, 2.5, 6])))
    yrs = r.randint(2, 6)
    I = pr * rate / 100 * yrs
    if (I * 100).denominator != 1:
        return None
    kind = r.random()
    if kind < 0.5:
        q = "%s is invested at %s%% %s for %d years. How much interest is earned?" % (money(pr), num(rate), B("simple interest") + " per year", yrs)
        e = "Interest each year = %s%% of %s = %s. For %d years: <b>%s</b>." % (num(rate), money(pr), money(pr * rate / 100), yrs, money(I))
        comp = pr * ((1 + rate / 100) ** yrs) - pr
        return QM(q, I, [pr * rate / 100, pr + I, comp.limit_denominator(100) if (comp * 100).denominator == 1 else None], e)
    q = "%s is invested at %s%% simple interest per year. What is the total in the account after %d years?" % (money(pr), num(rate), yrs)
    e = "Interest = %s × %d = %s. Total = %s + %s = <b>%s</b>." % (money(pr * rate / 100), yrs, money(I), money(pr), money(I), money(pr + I))
    return QM(q, pr + I, [I, pr + pr * rate / 100, pr * (100 + rate * yrs) / 100 + pr * rate / 100], e)


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    data = [
        ("A car bought for £12,000 loses 15% of its value in a year. What is it worth after one year?", F(10200), [F(1800), F(13800), F(11985)], "0.85 × 12,000 = <b>£10,200</b>."),
        ("A shop buys a jumper for £20 and sells it for £32. What is the percentage profit?", F(60), [F(12), F(375, 10), F(160)], "Profit = £12. 12 ÷ 20 × 100 = <b>60%</b>.", "%"),
        ("A TV costs £480 including VAT at 20%. What was the price before VAT?", F(400), [F(384), F(460), F(576)], "£480 is 120%, so the price before VAT = 480 ÷ 1.2 = <b>£400</b>."),
        ("A town's population rose from 25,000 to 27,500. What is the percentage increase?", F(10), [F(2500), F(11), F(9.09).limit_denominator(100)], "Increase = 2,500. 2,500 ÷ 25,000 × 100 = <b>10%</b>.", "%"),
        ("Isla's wage of £9.50 an hour rises by 4%. What is her new hourly wage?", F("9.88"), [F("0.38"), F("13.50"), F("9.54")], "1.04 × 9.50 = <b>£9.88</b>."),
        ("A coat is reduced by 30% to £56. What was the original price?", F(80), [F("72.80"), F(86), F("39.20")], "£56 is 70% of the original. 56 ÷ 0.7 = <b>£80</b>."),
        ("£3,000 is invested at 4% simple interest per year. How much interest is earned in 5 years?", F(600), [F(120), F(3600), F("649.96")], "4% of £3,000 = £120 a year. × 5 = <b>£600</b>."),
        ("A price goes up by 10% and then down by 10%. Compared with the start, the final price is…", "1% less", ["the same", "1% more", "10% less"], "1.1 × 0.9 = 0.99, so the final price is <b>1% less</b>."),
        ("Which is the bigger percentage increase: £50 to £60, or £80 to £95?", "£50 to £60", ["£80 to £95", "They are the same", "You cannot tell"], "£50 to £60 is 20%; £80 to £95 is 18.75%. So <b>£50 to £60</b>."),
        ("A house price fell from £250,000 to £235,000. What is the percentage decrease?", F(6), [F(15000), F(94), F("6.38")], "Decrease £15,000. 15,000 ÷ 250,000 × 100 = <b>6%</b>.", "%"),
        ("After a 25% increase, a bus fare is £2.50. What was it before?", F(2), [F("1.88"), F("2.25"), F("3.13")], "£2.50 is 125%. 2.50 ÷ 1.25 = <b>£2</b>."),
        ("A bank pays 3% simple interest per year. How long does it take £400 to earn £60 interest?", "5 years", ["2 years", "20 years", "6 years"], "3% of £400 = £12 a year. 60 ÷ 12 = <b>5 years</b>."),
        ("A meal costs £45 plus a 12.5% service charge. What is the total?", F("50.63"), [F("5.63"), F("57.50"), F("39.38")], "1.125 × 45 = 50.625 ≈ <b>£50.63</b>."),
        ("A phone is reduced from £350 to £280. What percentage is this reduction?", F(20), [F(25), F(70), F(80)], "£70 off. 70 ÷ 350 × 100 = <b>20%</b>.", "%"),
        ("Which calculation increases £72 by 15%?", "72 × 1.15", ["72 × 0.15", "72 × 1.5", "72 + 15"], "Increase by 15% → multiplier 1.15: <b>72 × 1.15</b>."),
        ("Which calculation finds the original price if £68 is the price after a 15% discount?", "68 ÷ 0.85", ["68 × 0.85", "68 × 1.15", "68 ÷ 1.15"], "£68 is 85% of the original, so <b>68 ÷ 0.85</b>."),
        ("A plant grew from 40 cm to 52 cm. What is the percentage increase?", F(30), [F(12), F("23.08"), F(130)], "Increase 12 cm. 12 ÷ 40 × 100 = <b>30%</b>.", "%"),
        ("Ben earns £1,800 a month and gets a 2.5% pay rise. How much more does he earn each month?", F(45), [F(1845), F(450), F("4.50")], "2.5% of £1,800 = 0.025 × 1,800 = <b>£45</b>."),
        ("A computer loses 20% of its value each year (it is worth 80% of the year before). It costs £1,000 new. What is it worth after 2 years?", F(640), [F(600), F(800), F(360)], "1,000 × 0.8 = 800, then 800 × 0.8 = <b>£640</b>."),
        ("A club had 160 members. It now has 136. What is the percentage decrease?", F(15), [F(24), F("17.65"), F(85)], "Decrease 24. 24 ÷ 160 × 100 = <b>15%</b>.", "%"),
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
        "<p><b>Percentage change</b> = change ÷ original × 100.</p>"
        "<p><b>Reverse percentage</b>: if the new amount is 85% of the original, divide by 0.85 to find the original.</p>"
        "<p><b>Simple interest</b> is the same amount every year: interest = principal × rate × years.</p>",
        [("Increase £240 by 17.5%.", ["Multiplier 1.175.", "1.175 × 240 = 282."], "£282"),
         ("A price rises from £80 to £92. Find the percentage increase.", ["Change = 12.", "12 ÷ 80 × 100 = 15."], "15%"),
         ("After 20% off, a bag costs £36. Find the original price.", ["£36 is 80%.", "36 ÷ 0.8 = 45."], "£45")],
        ["Dividing by the new amount when finding a percentage change. Always divide by the original.",
         "Stopping at the change: a 15% increase on £240 is £276, not £36.",
         "Adding the percentage back on to undo a discount: 20% off then +20% does not return to the original.",
         "Using 0.15 instead of 1.15 to increase by 15%."])


def main():
    sets = [S("Increase and decrease with multipliers", collect(one_mult, 20, R)),
            S("Finding the percentage change", collect(one_change, 20, R)),
            S("Reverse percentages", collect(one_reverse, 20, R)),
            S("Simple interest", collect(one_interest, 20, R)),
            S("Problems", problems())]
    make(8, "percentage-change-and-interest", 8, "R",
         "Percentage Change, Reverse Percentages and Simple Interest",
         "Year 8 Percentage Change Worksheets: Multipliers, Reverse Percentages and Simple Interest",
         "Percentage change and interest",
         "Solve problems involving percentage change, including: percentage increase, decrease and original value "
         "problems and simple interest in financial mathematics.",
         "Free Year 8 percentage change worksheets: increase and decrease with multipliers, find the percentage change, "
         "reverse percentages to find the original amount, and simple interest. 100 questions with answers.",
         "Increase by 15%: × 1.15. Decrease by 15%: × 0.85. Percentage change = change ÷ original × 100.",
         "To find the original amount, divide by the multiplier: £68 after 15% off → 68 ÷ 0.85 = £80.",
         body(),
         [("How do I calculate percentage change?", "Find the difference, divide by the original amount and multiply by 100."),
          ("What is a multiplier?", "The decimal you multiply by to make a percentage change in one step. A 20% increase is × 1.2 and a 20% decrease is × 0.8."),
          ("How do I find the original price after a discount?", "Work out what percentage is left, write it as a decimal and divide. After 30% off, £56 ÷ 0.7 = £80."),
          ("What is simple interest?", "Interest that is the same every year, worked out on the original amount: principal × rate × number of years.")],
         sets, R)


if __name__ == "__main__":
    main()
