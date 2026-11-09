# -*- coding: utf-8 -*-
"""
US Grade 7 Math: Percent Problems (7.RP.A.3)
  python tools/gen_us_math_g7_percent_problems.py
Percent of a number, percent change, markups and discounts, tax, tips, commission,
simple interest and percent error. Wrong answers come from real mistakes: giving only the
discount or tax instead of the new price, dividing by the new amount instead of the original,
subtracting the percent as a number ($80 − 25), and multiplying by 0.5 for 5%.
"""
import random
from fractions import Fraction as F
from ws_common import (num, mcq, balance, People, B, table, example, write_unit)

R = random.Random(70501)
UPDATED = "2026-11-09"


def d(v):
    """Plain decimal or whole number."""
    return num(F(v))


def money(v):
    v = F(v)
    s = num(abs(v))
    if "." in s:
        whole, frac = s.split(".")
        s = whole + "." + (frac + "0")[:2]
    return ("−" if v < 0 else "") + "$" + s


def pc(p):
    return d(p) + "%"


def mc(q, v, ws, e, show=money):
    """Multiple choice with money (or other) display; skips duplicates and impossible values."""
    v = F(v)
    cands = []
    for w in ws:
        w = F(w)
        if w == v or (w.denominator > 1 and num(w) is None) or (w < 0 <= v):
            continue
        cands.append((show(w), w))
    return mcq(q, (show(v), v), cands, e)


def pct_show(v):
    return pc(v)


# ------------------------------------------------------------ set 1
def set_percent_of():
    its = []
    for p, x in [(25, 80), (10, 340), (5, 60), (40, 75), (15, 120), (150, 40), (8, 250), (120, 35), (2.5, 400), (0.5, 600),
                 (35, 180), (200, 14)]:
        p = F(str(p))
        v = p / 100 * x
        ws = [p * x / 10, F(x) - p, x / p if p else 0, v + x, p / 10 * x, x - v, F(x) + p, v / 10]
        e = "%s means %s ÷ 100 = %s. %s × %s = %s." % (pc(p), d(p), d(p / 100), d(p / 100), d(x), d(v))
        if p < 10:
            e += " Not %s: %s is %s, not %s." % (d(p / 10 * x), pc(p), d(p / 100), d(p / 10))
        elif p > 100:
            e += " More than 100% gives more than the whole."
        its.append(mc("What is %s of %s?" % (B(pc(p)), B(d(x))), v, ws, e, d))
    # what percent
    for part, whole in [(18, 72), (45, 60), (7, 20), (90, 60), (3, 150), (27, 36)]:
        p = F(part, whole) * 100
        ws = [F(whole, part) * 100, part, F(part, whole), 100 - p, F(whole - part, whole) * 100, p - 100, whole - part]
        e = "Percent = part ÷ whole × 100 = %d ÷ %d × 100 = %s." % (part, whole, pc(p))
        e += " Not %s: that divides the whole by the part." % pc(F(whole, part) * 100) if num(F(whole, part) * 100) else ""
        its.append(mc("%s is what percent of %s?" % (B(part), B(whole)), p, ws, e, pct_show))
    # find the whole
    for part, p in [(12, 30), (45, 75)]:
        whole = F(part) / (F(p) / 100)
        ws = [F(part) * p / 100, part + p, F(part) * p, whole / 2]
        e = "%s of the number is %d, so the number is %d ÷ %s = %s." % (pc(p), part, part, d(F(p) / 100), d(whole))
        its.append(mc("%s is %s of what number?" % (B(part), B(pc(p))), whole, ws, e, d))
    return {"title": "Percent of a number", "items": its}


# ------------------------------------------------------------ set 2
def set_change():
    its = []
    for old, new in [(40, 50), (80, 60), (25, 35), (200, 150), (50, 80), (120, 90), (16, 20), (75, 60), (30, 54), (250, 200)]:
        ch = F(new - old, old) * 100
        word = "increase" if new > old else "decrease"
        wrong_base = abs(F(new - old, new) * 100)
        ws = [wrong_base, abs(new - old), F(new, old) * 100, abs(ch) * 2, abs(ch) + 10]
        e = ("Change = %d − %d = %d. Percent %s = change ÷ original = %d ÷ %d = %s. Not %s: divide by the original amount, %d, not the new amount."
             % (max(old, new), min(old, new), abs(new - old), word, abs(new - old), old, pc(abs(ch)),
                pc(wrong_base) if num(wrong_base) else "the other one", old))
        if num(wrong_base) is None:
            e = e.split(" Not ")[0]
        its.append(mc("A value changes from %s to %s. What is the percent %s?" % (B(old), B(new), word), abs(ch), ws, e, pct_show))
    # increase / decrease by a percent
    for x, p, up in [(60, 20, True), (80, 25, False), (150, 10, True), (45, 40, False), (240, 15, True), (90, 50, False),
                     (36, 125, True), (500, 8, False)]:
        p = F(p)
        new = x * (1 + p / 100) if up else x * (1 - p / 100)
        part = x * p / 100
        ws = [part, x + p if up else x - p, x * (1 - p / 100) if up else x * (1 + p / 100), new + 1]
        e = "%s of %d is %s. %s: %d %s %s = %s. Or multiply by %s." % (
            pc(p), x, d(part), "Add it" if up else "Subtract it", x, "+" if up else "−", d(part), d(new), d(1 + p / 100 if up else 1 - p / 100))
        its.append(mc("%s %d by %s. What is the new amount?" % ("Increase" if up else "Decrease", x, pc(p)), new, ws, e, d))
    # multiplier
    for p, up in [(30, True), (15, False)]:
        m = 1 + F(p, 100) if up else 1 - F(p, 100)
        ws = [F(p, 100), 1 - F(p, 100) if up else 1 + F(p, 100), p]
        e = "An %s of %d%% leaves %s%% of the amount: %s." % ("increase" if up else "decrease", p, d(m * 100), d(m))
        its.append(mc("Which number do you multiply by to %s an amount by %d%%?" % ("increase" if up else "decrease", p), m, ws, e, d))
    return {"title": "Percent increase and decrease", "items": its}


# ------------------------------------------------------------ set 3
def set_discount():
    its = []
    P = People(R)
    items = [("jacket", 80, 25), ("pair of shoes", 64, 15), ("video game", 59, 20), ("backpack", 45, 30), ("bike", 240, 35),
             ("lamp", 38, 40), ("tablet", 320, 12)]
    for thing, price, p in items:
        disc = F(price * p, 100)
        sale = price - disc
        ws = [disc, price - p, price + disc, price * (1 - F(p, 10)) if p < 10 else sale + p]
        e = "Discount = %d%% of %s = %s. Sale price = %s − %s = %s. Not %s: that is only the discount." % (
            p, money(price), money(disc), money(price), money(disc), money(sale), money(disc))
        its.append(mc("A %s costs %s. It is on sale for %d%% off. What is the sale price?" % (thing, money(price), p), sale, ws, e))
    # markups
    for thing, cost, p in [("T-shirt", 12, 50), ("phone case", 8, 75), ("chair", 60, 40), ("box of pens", 4, 125), ("snack", F("2.5"), 60)]:
        up = F(cost) * p / 100
        price = cost + up
        ws = [up, F(cost) + p, F(cost) * p / 10, price * 2]
        e = "Markup = %d%% of %s = %s. Price = %s + %s = %s." % (p, money(cost), money(up), money(cost), money(up), money(price))
        its.append(mc("A store buys a %s for %s and marks it up %d%%. What is the selling price?" % (thing, money(cost), p), price, ws, e))
    # find the percent off
    for orig, sale in [(50, 40), (120, 84), (75, 60), (36, 27)]:
        p = F(orig - sale, orig) * 100
        ws = [F(orig - sale, sale) * 100, orig - sale, F(sale, orig) * 100, p + 5]
        e = "Discount = %s − %s = %s. %s ÷ %s = %s, so it is %s off." % (money(orig), money(sale), money(orig - sale),
                                                                      d(orig - sale), d(orig), d(p / 100), pc(p))
        its.append(mc("A shirt was %s and is now %s. What percent is the discount?" % (money(orig), money(sale)), p, ws, e, pct_show))
    # two discounts
    its.append(mc("A $100 coat is 20% off. Then you take another 10% off the sale price. What do you pay?", 72,
                  [70, 80, 90, 28], "20% off $100 is $80. 10% of $80 is $8, so you pay $80 − $8 = $72. Not $70: the second discount is on $80, not $100."))
    its.append(mc("A $40 game is 25% off, and the store adds 25% to the sale price later. What is the final price?", F("37.5"),
                  [40, 30, 50, 10], "25% off $40 is $30. 25% of $30 is $7.50, so the price is $37.50. Not $40: the two 25%s are of different amounts."))
    its.append(mc("Which is the better deal on a $60 item?", 1, [2, 3, 4],
                  "30% off: $60 × 0.70 = $42. $15 off: $45. So 30% off is better.",
                  show=lambda v: {1: "30% off", 2: "$15 off", 3: "They are the same", 4: "It depends on the tax"}[int(v)]))
    its.append(mc("A store has 40% off everything. A $55 sweater becomes how much?", 33, [22, 15, 77, 51],
                  "40% of $55 is $22. $55 − $22 = $33. Or $55 × 0.60 = $33."))
    return {"title": "Discounts and markups", "items": its}


# ------------------------------------------------------------ set 4
def set_tax_tip():
    its = []
    for price, t in [(40, 6), (25, 8), (120, 7), (64, F("7.5")), (15, 5), (250, 4)]:
        tax = F(price) * t / 100
        total = price + tax
        ws = [tax, price + t, F(price) * t / 10 + price, F(price) * (100 - t) / 100]
        e = "Tax = %s%% of %s = %s. Total = %s + %s = %s. Not %s: that is the tax only." % (d(t), money(price), money(tax), money(price), money(tax), money(total), money(tax))
        its.append(mc("An item costs %s. The sales tax is %s%%. What is the total cost?" % (money(price), d(t)), total, ws, e))
    for bill, t in [(40, 15), (64, 20), (28, 18), (85, 20), (52, 15)]:
        tip = F(bill) * t / 100
        ws = [bill + tip, F(bill) * t / 10, bill + t, tip * 2]
        e = "Tip = %d%% of %s = %s × %s = %s." % (t, money(bill), d(F(t, 100)), money(bill), money(tip))
        its.append(mc("A meal costs %s. How much is a%s %d%% tip?" % (money(bill), "n" if t in (8, 11, 18) else "", t), tip, ws, e))
    for sales, c in [(2000, 5), (850, 8), (12000, 3)]:
        com = F(sales) * c / 100
        ws = [F(sales) * c / 10, sales + com, F(sales) / c, com * 2]
        e = "Commission = %d%% of %s = %s × %s = %s." % (c, money(sales), d(F(c, 100)), money(sales), money(com))
        its.append(mc("A salesperson earns %d%% commission. She sells %s of goods. How much commission does she earn?" % (c, money(sales)), com, ws, e))
    for pr, r, t in [(500, 4, 3), (1200, 5, 2), (800, F("2.5"), 4), (2000, 6, F("1.5")), (350, 3, 5), (1500, 2, 6)]:
        I = F(pr) * r / 100 * t
        ws = [pr + I, F(pr) * r / 100, F(pr) * r * t, I * 2]
        e = "Simple interest I = P × r × t = %s × %s × %s = %s." % (money(pr), d(F(r) / 100), d(t), money(I))
        its.append(mc("You put %s in an account that pays %s%% simple interest per year. How much interest do you earn in %s years?" % (money(pr), d(r), d(t)),
                      I, ws, e + " Not %s: that is the total in the account, not just the interest." % money(pr + I)))
    return {"title": "Tax, tips, commission and interest", "items": its}


# ------------------------------------------------------------ set 5
def set_words():
    its = []
    P = People(R)
    name, he, his = P.next()
    its.append(mc("%s guessed there were 40 marbles in a jar. There were 50. What was %s percent error?" % (name, his), 20,
                  [25, 10, 80, 40], "Error = 50 − 40 = 10. Percent error = 10 ÷ 50 (the actual value) = 0.2 = 20%. Not 25%: divide by the actual value, not the guess.", pct_show))
    its.append(mc("A board should be 2.5 m long. It was cut to 2.4 m. What is the percent error?", 4, [F("0.1"), F("4.17"), 10, 96],
                  "Error = 2.5 − 2.4 = 0.1 m. 0.1 ÷ 2.5 = 0.04 = 4%.", pct_show))
    its.append(mc("A town's population grew from 8,000 to 9,200. What was the percent increase?", 15, [F("13.04"), 12, 1200, 115],
                  "Increase = 1,200. 1,200 ÷ 8,000 = 0.15 = 15%.", pct_show))
    its.append(mc("A shirt is on sale for $24 after a 20% discount. What was the original price?", 30, [F("28.8"), F("19.2"), 44, 48],
                  "The sale price is 80% of the original, so the original is $24 ÷ 0.8 = $30. Not $28.80: adding 20% of $24 uses the wrong base."))
    its.append(mc("After 8% tax, a total bill is $54. What was the price before tax?", 50, [F("49.68"), 46, 62, F("58.32")],
                  "The total is 108% of the price: $54 ÷ 1.08 = $50."))
    its.append(mc("A family's dinner costs $72. They leave an 18% tip. What is the total they pay?", F("84.96"), [F("12.96"), 90, F("85.96"), F("59.04")],
                  "18% of $72 = $12.96. Total = $72 + $12.96 = $84.96."))
    its.append(mc("A store pays $30 for a game and sells it for $45. What percent is the markup?", 50, [F("33.33"), 15, 150, 45],
                  "Markup = $15. 15 ÷ 30 (the store's cost) = 0.5 = 50%. Not 33.33%: divide by the cost, not the selling price.", pct_show))
    its.append(mc("A $90 pair of jeans is 30% off, and then 6% tax is added to the sale price. What is the final cost?", F("66.78"),
                  [63, F("69.4"), F("66.6"), F("60.78")],
                  "30% off: $90 × 0.70 = $63. Tax: $63 × 1.06 = $66.78."))
    name, he, his = P.next()
    its.append(mc("%s's pay rose from $15 to $16.80 an hour. What was the percent raise?" % name, 12, [F("10.71"), F("1.8"), 112, 18],
                  "Raise = $1.80. 1.80 ÷ 15 = 0.12 = 12%.", pct_show))
    its.append(mc("A $250 bike loses 20% of its value each year. What is it worth after 1 year?", 200, [50, 230, 300, 225],
                  "20% of $250 = $50. $250 − $50 = $200."))
    its.append(mc("In a class of 32 students, 75% ride the bus. How many students ride the bus?", 24, [8, 25, F("42.67"), 43],
                  "75% of 32 = 0.75 × 32 = 24 students.", d))
    its.append(mc("A basketball player made 18 of 24 free throws. What percent did she make?", 75, [F("133.33"), 18, 25, 6],
                  "18 ÷ 24 = 0.75 = 75%.", pct_show))
    its.append(mc("A $2,400 loan has 5% simple interest per year. How much is owed in total after 3 years?", 2760, [360, 120, 2520, 3600],
                  "I = 2,400 × 0.05 × 3 = $360. Total = $2,400 + $360 = $2,760. Not $360: that is only the interest."))
    its.append(mc("A real estate agent earns 3% commission on a $280,000 house. How much does the agent earn?", 8400, [84000, 840, 2800, 9333],
                  "3% of $280,000 = 0.03 × 280,000 = $8,400."))
    its.append(mc("A water bill went from $60 to $48. What was the percent decrease?", 20, [25, 12, 80, 48],
                  "Decrease = $12. 12 ÷ 60 = 0.2 = 20%. Not 25%: divide by the original $60, not $48.", pct_show))
    its.append(mc("A recipe needs 400 g of flour. Mia uses 10% more. How much flour does she use?", 440, [40, 410, 360, 800],
                  "10% of 400 g = 40 g. 400 + 40 = 440 g.", lambda v: d(v) + " g"))
    its.append(mc("A phone's battery is at 80%. It loses 15% of the full charge. What percent is left?", 65, [68, 95, 12, 5],
                  "15% of the full charge is 15 percentage points: 80% − 15% = 65%.", pct_show))
    its.append(mc("A store marks up a $40 jacket by 50%. Later it is sold at 50% off. What is the final price?", 30, [40, 20, 60, 10],
                  "50% markup: $40 × 1.5 = $60. 50% off: $60 × 0.5 = $30. Not $40: the 50% off is of $60."))
    its.append(mc("A savings account pays 4% simple interest. How many years does it take $500 to earn $100?", 5, [4, 20, 2, 25],
                  "Interest each year = 4% of $500 = $20. $100 ÷ $20 = 5 years.", lambda v: d(v) + " years"))
    its.append(mc("A city's bus fare went from $2.50 to $3.00. What was the percent increase?", 20, [F("16.67"), 50, 120, F("0.5")],
                  "Increase = $0.50. 0.50 ÷ 2.50 = 0.2 = 20%. Not 16.67%: divide by the old fare.", pct_show))
    return {"title": "Word problems", "items": its}


def body():
    rows = [["Percent of a number", "part = percent × whole", "25% of 80 = 0.25 × 80 = 20"],
            ["Percent change", "change ÷ original", "40 to 50: 10 ÷ 40 = 25%"],
            ["Discount", "price × (1 − rate)", "$80, 25% off: 80 × 0.75 = $60"],
            ["Tax or markup", "price × (1 + rate)", "$40, 6% tax: 40 × 1.06 = $42.40"],
            ["Simple interest", "I = P × r × t", "$500, 4%, 3 years: $60"]]
    return ("<h2>Percent means out of 100</h2><p>Change the percent to a decimal: 25% = 0.25, 6% = 0.06, 150% = 1.5. "
            "Then multiply. Percent of means <b>times</b>.</p>"
            + table(["Problem", "Rule", "Example"], rows)
            + "<h2>Percent change</h2><p>Find the change, then divide by the <b>original</b> amount. "
            "Percent error works the same way, but you divide by the actual value.</p>"
            + example("A $64 pair of shoes is 15% off. What is the sale price?",
                      ["Discount: 0.15 × 64 = $9.60.", "Sale price: $64 − $9.60 = $54.40.", "Or in one step: 64 × 0.85 = $54.40."], "$54.40")
            + example("A price goes from $40 to $50. What is the percent increase?",
                      ["Change: 50 − 40 = 10.", "Divide by the original: 10 ÷ 40 = 0.25."], "25%")
            + "<h2>Common mistakes</h2><ul><li>Stopping at the discount: 25% off $80 is $60, not $20.</li>"
            "<li>Dividing by the new amount: 40 to 50 is a 25% increase, not 20%.</li>"
            "<li>Subtracting the percent as a number: 25% off $80 is not $80 − 25.</li>"
            "<li>Writing 5% as 0.5: 5% = 0.05.</li></ul>")


def main():
    sets = [set_percent_of(), set_change(), set_discount(), set_tax_tip(), set_words()]
    balance(sets, R)
    unit = {
        "slug": "percent-problems",
        "title": "Percent Problems",
        "seo_title": "Grade 7 Percent Problems Worksheets: Percent Change, Discounts, Tax, Tips and Simple Interest",
        "short_title": "Percent problems",
        "domain": "Ratios & Proportional Relationships",
        "standard_code": "7.RP.A.3",
        "standard_url": "https://www.thecorestandards.org/Math/Content/7/RP/A/3/",
        "standard_text": "Use proportional relationships to solve multistep ratio and percent problems. Examples: simple interest, tax, markups and markdowns, gratuities and commissions, fees, percent increase and decrease, percent error.",
        "meta_desc": "Free Grade 7 percent problems worksheets: percent of a number, percent increase and decrease, discounts and markups, sales tax, tips, commission, simple interest and percent error. 100 practice questions with an answer key.",
        "key_big": "Percent of means times: 25% of 80 = 0.25 × 80 = 20.",
        "key_sub": "For percent change, divide the change by the original amount. A discount subtracts, tax and markups add.",
        "body_html": body(),
        "faq": [
            {"q": "How do you find a percent of a number?", "a": "Change the percent to a decimal and multiply. 15% of 120 = 0.15 × 120 = 18."},
            {"q": "How do you find percent increase or decrease?", "a": "Subtract to find the change, then divide by the original amount and multiply by 100. From 80 to 60: 20 ÷ 80 = 0.25, a 25% decrease."},
            {"q": "How do I find a sale price?", "a": "Find the discount and subtract it, or multiply by what is left. 25% off $80: $80 × 0.75 = $60."},
            {"q": "What is simple interest?", "a": "Interest that is a fixed percent of the starting amount each year: I = P × r × t. $500 at 4% for 3 years earns 500 × 0.04 × 3 = $60."}],
        "sets": sets,
        "pdf_url": "",
        "sort": 5,
        "updated": UPDATED,
    }
    write_unit("us", "math", "grade-7", unit)


if __name__ == "__main__":
    main()
