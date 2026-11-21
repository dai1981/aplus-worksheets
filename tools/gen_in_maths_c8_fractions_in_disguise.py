# -*- coding: utf-8 -*-
"""
India Class 8 Maths, Ganita Prakash Part 2, Chapter 1: Fractions in Disguise
  python3 tools/gen_in_maths_c8_fractions_in_disguise.py
Percentages as fractions in disguise: converting fractions and decimals to percentages, finding a percentage of a
quantity, expressing one quantity as a percentage of another, percentage increase and decrease, profit, loss and
discount, and simple and compound interest.
Wrong answers come from real mistakes: dividing by the new value for percentage change, adding the percentage to the
answer instead of multiplying, simple interest used for compound interest, and the profit percent taken on the selling price.
"""
import random
from fractions import Fraction as F
from in_common import num, unit, T, QN, adopt, gb, inr, fr, rs
import gen_uk_maths_y7_fractions_decimals_and_percentages as fdp
import gen_uk_maths_y7_percentages_of_amounts as pa
import gen_au_maths_y8_percentages_profit_and_loss as pl

R = random.Random(908008)
for m in (fdp, pa, pl):
    adopt(m, R)


def one_frac(r):
    d = r.choice([2, 4, 5, 8, 10, 20, 25, 40, 50])
    n = r.randint(1, d - 1)
    if F(n, d).denominator != d:
        return None
    p = F(n * 100, d)
    return QN("Write %s as a percentage." % fr(str(n), str(d)), p, [F(n * 10, d), n, F(d * 100, n) if F(d * 100, n) < 1000 else d], "%d/%d × 100%% = <b>%s%%</b>." % (n, d, num(p)), unit="%")


def one_disc(r):
    mp = r.choice([400, 500, 800, 1200, 1500, 2000, 2400, 3600, 4500])
    d = r.choice([5, 10, 15, 20, 25, 30, 40])
    sp = mp * (100 - d) // 100
    item = r.choice(["school bag", "pair of shoes", "kurta", "watch", "cricket bat", "mixer grinder"])
    return T("A %s is marked %s. The shop gives a %d%% discount. What is the selling price?" % (item, inr(mp), d), inr(sp),
             [inr(mp * d // 100), inr(mp + mp * d // 100), inr(mp - d)], "Discount = %d%% of %s = %s. Price = %s − %s = <b>%s</b>." % (d, inr(mp), inr(mp * d // 100), inr(mp), inr(mp * d // 100), inr(sp)))


def one_interest(r):
    p = r.choice([1000, 2000, 5000, 8000, 10000, 12000, 20000, 25000])
    rate = r.choice([5, 8, 10, 12, 15, 20])
    t = r.choice([2, 3]) if rate in (5, 10, 20) else 2
    if r.random() < 0.45:
        si = p * rate * t // 100
        return T("Find the simple interest on %s at %d%% per year for %d years." % (inr(p), rate, t), inr(si), [inr(p * rate // 100), inr(p + si), inr(p * rate * t // 10)],
                 "SI = P × R × T ÷ 100 = %s × %d × %d ÷ 100 = <b>%s</b>." % (inr(p), rate, t, inr(si)))
    a = F(p) * F(100 + rate, 100) ** t
    ci = a - p
    if ci.denominator != 1 and (ci * 100).denominator != 1:
        return None
    return T("%s is invested at %d%% per year compound interest. How much is it worth after %d years?" % (inr(p), rate, t), inr(a),
             [inr(p + p * rate * t // 100), inr(ci), inr(F(p) * F(100 + rate * t, 100) + F(p * rate, 100))] if inr(F(p) * F(100 + rate * t, 100) + F(p * rate, 100)) != inr(a) else [inr(p + p * rate * t // 100), inr(ci), inr(a + p * rate // 100)],
             "Multiply by %s each year: %s × %s<sup>%d</sup> = <b>%s</b>." % (num(F(100 + rate, 100)), inr(p), num(F(100 + rate, 100)), t, inr(a)))


def main():
    unit(8, 2, 1, "fractions-in-disguise", 8, "N", "Fractions in Disguise: Percentages, Profit, Loss and Interest", "fractions in disguise",
         "Percentages as fractions, percentage of a quantity, percentage increase and decrease, profit, loss and discount, simple and compound interest (summary of NCERT Ganita Prakash Class 8)",
         "Class 8 Fractions in Disguise worksheet (Ganita Prakash Part 2, Chapter 1): percentages, percentage change, profit and loss, discount, simple and compound interest. 100 questions with answers.",
         "A percentage is a fraction out of 100", "Percentage change = change ÷ original × 100.",
         "<p>A <b>percentage</b> is a fraction with denominator 100: 3/4 = 75/100 = 75%. To find p% of a quantity, multiply by p/100.</p>"
         "<p><b>Percentage change</b> = change ÷ original value × 100. A 20% increase multiplies by 1.2; a 20% decrease multiplies by 0.8.</p>"
         "<p>Profit or loss % is on the <b>cost price</b>. Discount % is on the <b>marked price</b>. Simple interest = P × R × T ÷ 100; compound interest multiplies by (1 + R/100) every year.</p>",
         [("A phone bought for ₹8,000 is sold for ₹9,200. Find the profit %.", ["Profit = ₹1,200", "1,200 ÷ 8,000 × 100"], "15%"),
          ("₹10,000 at 10% compound interest for 2 years.", ["10,000 × 1.1 × 1.1"], "₹12,100")],
         ["Working out percentage change on the new value instead of the original.", "Taking profit % on the selling price.", "Using simple interest when the interest is compounded."],
         [("Why are percentages called fractions in disguise?", "Because p% means p/100, a fraction with denominator 100."),
          ("How is profit percentage found?", "Profit ÷ cost price × 100."),
          ("What is the difference between simple and compound interest?", "Simple interest is on the original sum only; compound interest is also earned on the interest already added.")],
         [("Fractions, decimals and percentages", [(one_frac, 10), (gb(fdp.one_2p), 10)]),
          ("Percentage of a quantity", [(rs(pa.one_mental), 10), (rs(pa.one_mult), 5), (rs(pa.one_as_pct), 5)]),
          ("Percentage increase and decrease", [(rs(pa.one_change), 12), (gb(pl.one_reverse), 8)]),
          ("Profit, loss and discount", [(gb(pl.one_profit), 12), (one_disc, 8)]),
          ("Simple and compound interest", [(one_interest, 20)])], R)


if __name__ == "__main__":
    main()
