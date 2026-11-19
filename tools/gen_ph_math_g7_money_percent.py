# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Money Problems with Percentages: Discount, Commission, VAT and Simple Interest (Grade 7: Number and Algebra)
  python3 tools/gen_ph_math_g7_money_percent.py
Discounts, commissions, 12% VAT, simple interest and multi-step sale problems with pesos (own makers).
Wrong answers come from real mistakes: giving the discount instead of the sale price, writing 12% as 1.2, using only
one year of interest, and adding and subtracting percentages of different amounts.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)

ph_common.GRADE = "grade-7"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


from fractions import Fraction as F

ITEMS = [("a pair of shoes", 1800, 3500), ("a school bag", 900, 1600), ("an electric fan", 1200, 2500), ("a rice cooker", 1500, 3000),
         ("a bicycle", 4500, 9000), ("a cell phone", 6000, 15000), ("a uniform set", 600, 1200), ("a study table", 2000, 4000)]


def pm(v):
    return peso(v)


def one_disc(r):
    k = Kid(r).next()
    item, lo, hi = r.choice(ITEMS)
    price = r.randrange(lo, hi + 1, 100)
    p = r.choice([10, 15, 20, 25, 30, 40, 50])
    d = F(price * p, 100)
    if d.denominator != 1:
        raise AssertionError
    if r.random() < 0.5:
        q = "%s buys %s that costs %s. The store gives a %d%% discount. How much does %s pay?" % (k["n"], item, pm(price), p, k["he"])
        right = price - d
        return mcq(q, pm(right), [pm(x) for x in (d, price - p, price + d)], "Discount: %d%% of %s = %s. Sale price: %s − %s = <b>%s</b>." % (p, pm(price), pm(d), pm(price), pm(d), pm(right)))
    q = "%s is on sale for %s. The original price was %s. What percent is the discount?" % (item.capitalize(), pm(price - d), pm(price))
    return mcq(q, "%d%%" % p, ["%g%%" % float(F(d * 100, price - d)) if F(d * 100, price - d).denominator <= 4 else "%d%%" % (p + 5), "%d%%" % (100 - p), "%s%%" % comma(int(d) // 10)],
               "Discount: %s − %s = %s. %s ÷ %s × 100 = <b>%d%%</b>." % (pm(price), pm(price - d), pm(d), comma(int(d)), comma(price), p))


def one_comm(r):
    k = Kid(r).next()
    what = r.choice(["appliances", "cars", "houses and lots", "insurance plans", "cell phones"])
    rate = r.choice([2, 3, 4, 5, 6, 8, 10, 12, 15])
    sales = r.randrange({"cars": 500000, "houses and lots": 1500000}.get(what, 20000), {"cars": 1500000, "houses and lots": 5000000}.get(what, 120000), 1000)
    c = F(sales * rate, 100)
    if c.denominator != 1:
        raise AssertionError
    who = "%s's mother" % k["n"] if r.random() < 0.5 else "%s's uncle" % k["n"]
    if r.random() < 0.6:
        q = "%s sells %s and earns a %d%% commission. This month the sales are %s. How much is the commission?" % (who, what, rate, pm(sales))
        return mcq(q, pm(c), [pm(x) for x in (c * 10, F(c, 10), sales - c)], "%d%% of %s = 0.%02d × %s = <b>%s</b>." % (rate, pm(sales), rate, comma(sales), pm(c)))
    base = r.choice([10000, 12000, 15000])
    q = "%s earns a monthly salary of %s plus a %d%% commission on sales. The sales this month are %s. What is the total income?" % (who, pm(base), rate, pm(sales))
    return mcq(q, pm(base + c), [pm(x) for x in (c, base + sales, base + c * 10)], "Commission: %d%% of %s = %s. Total: %s + %s = <b>%s</b>." % (rate, pm(sales), pm(c), pm(base), pm(c), pm(base + c)))


def one_vat(r):
    item, lo, hi = r.choice(ITEMS)
    price = r.randrange(lo, hi + 1, 50)
    t = F(price * 12, 100)
    if r.random() < 0.6:
        q = "%s costs %s before the 12%% VAT (value-added tax). What is the price with VAT?" % (item.capitalize(), pm(price))
        right = price + t
        return mcq(q, pm(right), [pm(x) for x in (t, price + 12, price * F(112, 1000))], "VAT: 12%% of %s = %s. Price with VAT: %s × 1.12 = <b>%s</b>." % (pm(price), pm(t), pm(price), pm(right)))
    q = "%s costs %s before tax. How much is the 12%% VAT?" % (item.capitalize(), pm(price))
    return mcq(q, pm(t), [pm(x) for x in (price + t, F(price, 12), t * 10)], "12%% of %s = 0.12 × %s = <b>%s</b>." % (pm(price), comma(price), pm(t)))


def one_si(r):
    k = Kid(r).next()
    P_ = r.choice([5000, 8000, 10000, 12000, 15000, 20000, 25000, 50000])
    rate = r.choice([2, 3, 4, 5, 6, 8])
    t = r.randint(2, 6)
    I = F(P_ * rate * t, 100)
    kind = r.choice(["I", "A", "A"])
    place = r.choice(["a bank", "a cooperative", "a savings account"])
    if kind == "I":
        q = "%s deposits %s in %s that pays %d%% simple interest per year. How much interest does %s earn in %d years?" % (k["n"], pm(P_), place, rate, k["he"], t)
        return mcq(q, pm(I), [pm(x) for x in (F(P_ * rate, 100), P_ + I, I * 10)], "I = Prt = %s × %d%% × %d = <b>%s</b>." % (pm(P_), rate, t, pm(I)))
    q = "%s borrows %s at %d%% simple interest per year for %d years. How much must %s pay back in all?" % (k["n"], pm(P_), rate, t, k["he"])
    return mcq(q, pm(P_ + I), [pm(x) for x in (I, P_ + F(P_ * rate, 100), P_ + I * 2)], "I = %s × %d%% × %d = %s. Total: %s + %s = <b>%s</b>." % (pm(P_), rate, t, pm(I), pm(P_), pm(I), pm(P_ + I)))


def one_mix(r):
    k = Kid(r).next()
    item, lo, hi = r.choice(ITEMS)
    price = r.randrange(lo, hi + 1, 100)
    p = r.choice([10, 20, 25])
    sale = F(price * (100 - p), 100)
    total = sale * F(112, 100)
    if (total * 100).denominator != 1:
        raise AssertionError
    q = "%s costs %s. It is on sale at %d%% off, and then 12%% VAT is added to the sale price. How much does %s pay?" % (item.capitalize(), pm(price), p, k["n"])
    wrong1 = F(price * (100 - p + 12), 100)
    return mcq(q, pm(total), [pm(x) for x in (wrong1, sale, price * F(112, 100))],
               "Sale price: %s × %s = %s. With VAT: %s × 1.12 = <b>%s</b>. (Taking off %d%% and adding 12%% of the original gives a different answer.)" % (pm(price), "%g" % ((100 - p) / 100), pm(sale), pm(sale), pm(total), p))


def build():
    sets, R = build_sets([
        ("Discounts", [("collect", uniq(one_disc), 20)]),
        ("Commission", [("collect", uniq(one_comm), 20)]),
        ("12% VAT", [("collect", uniq(one_vat), 20)]),
        ("Simple interest", [("collect", uniq(one_si), 20)]),
        ("Multi-step money problems", [("collect", uniq(one_mix), 10), ("collect", uniq(one_disc), 5), ("collect", uniq(one_si), 5)]),
    ], 70705)
    finish(sets, R)
    body = lesson('<ul><li><b>Discount</b> = rate × original price. Sale price = original price − discount.</li><li><b>Commission</b> = rate × total sales. It is money a salesperson earns.</li><li><b>VAT</b> (value-added tax) in the Philippines is 12%. Price with VAT = price × 1.12.</li><li><b>Simple interest</b>: I = Prt (principal × rate per year × number of years). Amount to pay back = P + I.</li></ul>',
        [example("₱2,400 bag, 25% off", ["0.25 × 2,400 = 600", "2,400 − 600"], "₱1,800"), example("₱10,000 at 5% for 3 years", ["10,000 × 0.05 × 3"], "₱1,500 interest")],
        [['Giving the discount', 'Subtract it to get the sale price.'], ['12% as 1.2', '12% = 0.12; with VAT, × 1.12.'], ['One year of interest', 'Multiply by the number of years.']])
    faq = [('What does MATATAG Math 7 ask about money problems?', 'Solve money problems involving percentages, such as discount, commission, sales tax, and simple interest.'), ('What is VAT?', 'Value-added tax, a 12% tax added to the price of many goods in the Philippines.'), ('What is the difference between simple and compound interest?', 'Simple interest is always computed on the original principal.'), ('How is commission different from salary?', 'Commission depends on sales; salary is fixed.')]
    make('discount-commission-vat-and-simple-interest', 5, 'Number and Algebra', 'Grade 7: Number and Algebra',
         'Solve money problems involving percentages (e.g., discount, commission, sales tax, simple interest).',
         'Money Problems with Percentages: Discount, Commission, VAT and Simple Interest', 'Discount, Commission, VAT and Interest',
         'Free Grade 7 money worksheets for the DepEd MATATAG curriculum: discounts, commission, 12% VAT, simple interest and multi-step problems with pesos. 100 questions with answers.',
         'Discount, commission, tax and interest are all a percent of an amount.', 'Simple interest: I = Prt.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
