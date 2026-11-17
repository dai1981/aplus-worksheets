# -*- coding: utf-8 -*-
"""
UK Year 9 Maths: Compound Interest and Growth (KS3 Ratio, proportion and rates of change)
  python3 tools/gen_uk_maths_y9_compound_interest_and_growth.py
Multipliers for percentage increase and decrease, compound interest, depreciation, growth and decay of
populations, comparing simple and compound interest, and problems.
Wrong answers come from real mistakes: using simple interest (adding the same interest every year), using
1.5 instead of 1.05 for 5%, giving only the interest instead of the total, and multiplying by r × n.
"""
import random
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F
from uk_ks3 import num, B, S, make, lesson, collect, QN, T, gbp, GIRLS, BOYS

R = random.Random(90801)


def money(x):
    d = Decimal(repr(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return gbp(F(str(d)))


def mstr(m):
    return num(F(str(Decimal(repr(m)).normalize())))


def mult(p, up=True):
    return round(1 + p / 100.0 if up else 1 - p / 100.0, 4)


def who(r):
    return r.choice(GIRLS + BOYS)


# ------------------------------------------------------------ set 1: multipliers
def one_mult(r):
    p = r.choice([2, 3, 4, 5, 6, 7, 8, 9, 12, 15, 20, 25, 30, 35, 40, 2.5, 1.5, 3.5, 17.5])
    up = r.random() < 0.55
    m = mult(p, up)
    q = "What is the multiplier for %s %s %s?" % ("an" if str(p).startswith("8") or str(p).startswith("18") or str(p).startswith("11") else "a", "%s%%" % mstr(p), "increase" if up else "decrease")
    right = mstr(m)
    wr = [(mstr(1 + p / 10.0) if p < 10 else mstr(round(1 + p / 1000.0, 4))) if up else mstr(round(p / 100.0, 4)), mstr(round(1 - p / 100.0, 4)) if up else mstr(round(1 + p / 100.0, 4)),
          mstr(p / 100.0) if up else mstr(round(1 - p / 10.0, 4)) if p < 10 else mstr(round(p / 100.0 + 1, 4) - 0.0)]
    if not up and p >= 10:
        wr[2] = mstr(round(1 - p / 1000.0, 4))
    wr = [w for w in dict.fromkeys(wr) if w != right]
    e = "100%% %s %s%% = %s%%, so the multiplier is <b>%s</b>." % ("+" if up else "−", mstr(p), mstr(round(100 + p if up else 100 - p, 4)), right)
    return T(q, right, wr[:3], e)


# ------------------------------------------------------------ set 2: compound interest
def one_ci(r):
    P = r.choice([200, 400, 500, 800, 1000, 1200, 1500, 2000, 2500, 3000, 5000, 6000, 8000, 10000])
    p = r.choice([1, 2, 3, 4, 5, 6, 1.5, 2.5, 3.5])
    n = r.randint(2, 5)
    m = 1 + p / 100.0
    A = P * m ** n
    simple = P * (1 + p * n / 100.0)
    q = "%s invests %s at %s%% compound interest per year. How much is in the account after %d years?" % (who(r), gbp(P), mstr(p), n)
    right = money(A)
    wr = [money(simple), money(A - P), money(P * m * n) if P * m * n != A else money(A + 1)]
    if money(simple) == right:
        return None
    e = "Multiplier %s. %s × %s<sup>%d</sup> = %s. To the nearest penny: <b>%s</b>." % (mstr(m), gbp(P), mstr(m), n, mstr(round(A, 4)), right)
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)


# ------------------------------------------------------------ set 3: depreciation
def one_dep(r):
    items = [("car", 8000, 30000), ("motorbike", 4000, 12000), ("laptop", 600, 2000), ("van", 10000, 25000), ("phone", 500, 1200), ("boat", 15000, 40000)]
    it, lo, hi = r.choice(items)
    P = r.randint(lo // 100, hi // 100) * 100
    p = r.choice([5, 10, 12, 15, 20, 25, 8])
    n = r.randint(2, 4)
    m = 1 - p / 100.0
    A = P * m ** n
    q = "A %s costs %s. Its value falls by %d%% each year. What is it worth after %d years?" % (it, gbp(P), p, n)
    right = money(A)
    wr = [money(P * (1 - p * n / 100.0)), money(P - A), money(P * (1 + p / 100.0) ** n)]
    e = "Multiplier %s. %s × %s<sup>%d</sup> = <b>%s</b>." % (mstr(m), gbp(P), mstr(m), n, right)
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)


# ------------------------------------------------------------ set 4: growth and decay, interest only
def one_growth(r):
    k = r.randint(0, 2)
    if k == 0:
        P = r.choice([2000, 5000, 8000, 12000, 20000, 40000, 60000])
        p = r.choice([2, 3, 4, 5, 10])
        n = r.randint(2, 4)
        up = r.random() < 0.6
        place = r.choice(["town", "village", "city"]) if up else r.choice(["village", "town"])
        A = P * (1 + (p if up else -p) / 100.0) ** n
        q = "The population of a %s is %s. It %s by %d%% each year. What is the population after %d years, to the nearest whole number?" % (
            place, num(P), "grows" if up else "falls", p, n)
        right = int(Decimal(repr(A)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
        simple = int(round(P * (1 + (p if up else -p) * n / 100.0)))
        if abs(A - right) < 1e-6:
            e = "%s × %s<sup>%d</sup> = <b>%s</b>." % (num(P), mstr(mult(p, up)), n, num(right))
        else:
            e = "%s × %s<sup>%d</sup> = %s, which rounds to <b>%s</b>." % (num(P), mstr(mult(p, up)), n, mstr(round(A, 3)), num(right))
        if simple == right:
            return None
        return QN(q, right, [simple, int(round(abs(A - P))), int(round(P * (1 + (-p if up else p) / 100.0) ** n))], e)
    if k == 1:
        P = r.choice([500, 1000, 2000, 4000, 5000])
        p = r.choice([2, 3, 4, 5])
        n = r.randint(2, 4)
        A = P * (1 + p / 100.0) ** n
        q = "%s invests %s at %d%% compound interest. How much <b>interest</b> is earned in %d years?" % (who(r), gbp(P), p, n)
        right = money(A - P)
        wr = [money(A), money(P * p * n / 100.0), money(P * p / 100.0)]
        e = "Total: %s × %s<sup>%d</sup> = %s. Interest = %s − %s = <b>%s</b>." % (gbp(P), mstr(1 + p / 100.0), n, money(A), money(A), gbp(P), right)
        return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)
    start = r.choice([100, 200, 400, 500, 800, 1000])
    p = r.choice([10, 20, 50])
    n = r.randint(2, 4)
    A = start * (1 + p / 100.0) ** n
    if abs(A - round(A)) > 1e-6:
        return None
    q = "A culture of %s bacteria grows by %d%% every hour. How many bacteria are there after %d hours?" % (num(start), p, n)
    e = "%s × %s<sup>%d</sup> = <b>%s</b>." % (num(start), mstr(mult(p)), n, num(round(A)))
    return QN(q, int(round(A)), [int(start * (1 + p * n / 100.0)), int(round(A - start)), int(start * (1 + p / 100.0) * n)], e)


# ------------------------------------------------------------ set 5: problems
def problems():
    data = [
        ("Which gives more money after 2 years on £1,000: 5% simple interest or 5% compound interest?", "Compound interest", ["Simple interest", "They are the same", "It depends on the bank"],
         "Simple: £1,100. Compound: £1,000 × 1.05<sup>2</sup> = £1,102.50. <b>Compound interest</b> gives more, because interest is earned on interest."),
        ("£1,000 is invested at 10% compound interest. How much is it worth after 3 years?", "£1,331", ["£1,300", "£1,030", "£331"],
         "£1,000 × 1.1<sup>3</sup> = <b>£1,331</b>."),
        ("Which calculation gives the value of £600 after 4 years at 3% compound interest?", "600 × 1.03<sup>4</sup>", ["600 × 1.3<sup>4</sup>", "600 × 1.03 × 4", "600 × 0.03<sup>4</sup>"],
         "The multiplier is 1.03, used once for each year: <b>600 × 1.03<sup>4</sup></b>."),
        ("Which calculation gives the value of a £9,000 car after 5 years if it loses 15% each year?", "9000 × 0.85<sup>5</sup>", ["9000 × 0.15<sup>5</sup>", "9000 × 1.15<sup>5</sup>", "9000 − 0.85 × 5"],
         "Losing 15% leaves 85%, so the multiplier is 0.85: <b>9000 × 0.85<sup>5</sup></b>."),
        ("A house is worth £200,000. Its value rises 10% one year then falls 10% the next. What is it worth now?", "£198,000", ["£200,000", "£202,000", "£180,000"],
         "£200,000 × 1.1 × 0.9 = <b>£198,000</b>. The 10% fall is of a bigger amount."),
        ("After a 20% increase, a price is £72. What was it before?", "£60", ["£57.60", "£52", "£86.40"],
         "Before × 1.2 = £72, so before = 72 ÷ 1.2 = <b>£60</b>."),
        ("After a 25% decrease in value, a bike is worth £300. What was it worth before?", "£400", ["£375", "£225", "£240"],
         "Before × 0.75 = £300, so before = 300 ÷ 0.75 = <b>£400</b>."),
        ("£2,000 grows at 6% compound interest. After how many whole years will it first be worth more than £2,400?", "4 years", ["3 years", "5 years", "2 years"],
         "Year 3: £2,382.03. Year 4: £2,524.95. It first passes £2,400 after <b>4 years</b>."),
        ("A population of 1,000 rabbits doubles every year. How many are there after 4 years?", "16,000", ["8,000", "4,000", "5,000"],
         "Doubling is a multiplier of 2: 1,000 × 2<sup>4</sup> = <b>16,000</b>."),
        ("A radioactive sample halves every day. It starts at 640 g. How much is left after 5 days?", "20 g", ["40 g", "128 g", "10 g"],
         "640 × 0.5<sup>5</sup> = 640 ÷ 32 = <b>20 g</b>."),
        ("What single multiplier means an increase of 10% followed by another increase of 10%?", "1.21", ["1.2", "1.01", "0.21"],
         "1.1 × 1.1 = <b>1.21</b>, an overall increase of 21%."),
        ("What is the overall percentage change after a 20% increase and then a 20% decrease?", "4% decrease", ["No change", "4% increase", "40% decrease"],
         "1.2 × 0.8 = 0.96, so it is a <b>4% decrease</b>."),
        ("A savings account pays 4% compound interest. What is the multiplier for 3 years?", "1.04<sup>3</sup>", ["1.12", "1.4<sup>3</sup>", "0.04<sup>3</sup>"],
         "Each year multiply by 1.04, so 3 years is <b>1.04<sup>3</sup></b> (about 1.1249, not 1.12)."),
        ("Isla puts £500 in an account at 2% simple interest per year. How much interest does she get in 3 years?", "£30", ["£30.60", "£10", "£530"],
         "Simple interest is the same each year: 2% of £500 = £10, × 3 = <b>£30</b>."),
        ("A car loses 20% of its value each year. After 2 years, what percentage of its original value is left?", "64%", ["60%", "40%", "80%"],
         "0.8 × 0.8 = 0.64, so <b>64%</b> is left."),
        ("Bank A pays 3% compound interest. Bank B pays 3.2% simple interest. For £1,000 over 2 years, which is better?", "Bank B", ["Bank A", "They are the same", "Neither earns interest"],
         "A: £1,000 × 1.03<sup>2</sup> = £1,060.90. B: £1,000 + 2 × £32 = £1,064. <b>Bank B</b> is better."),
        ("A town's population is 50,000 and falls by 2% a year. What is it after 2 years?", "48,020", ["48,000", "49,000", "47,980"],
         "50,000 × 0.98<sup>2</sup> = <b>48,020</b>."),
        ("An antique is worth £800. It gains 5% value each year. What is it worth after 2 years?", "£882", ["£880", "£840", "£82"],
         "£800 × 1.05<sup>2</sup> = <b>£882</b>."),
        ("Oliver says that 5% compound interest for 2 years is the same as 10% once. Why is he wrong?", "The second year's interest is on a bigger amount", ["Interest is only paid once", "Compound interest is always less", "5% of 5% is 25%"],
         "In year 2 interest is paid on the new total, so the overall increase is 10.25%. <b>The second year's interest is on a bigger amount.</b>"),
        ("Which multiplier would make an amount fall by 3.5%?", "0.965", ["0.65", "1.035", "0.35"],
         "100% − 3.5% = 96.5%, so the multiplier is <b>0.965</b>."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>A <b>multiplier</b> changes an amount by a percentage in one step. A 4% increase is × 1.04; a 15% decrease is × 0.85.</p>"
        "<p><b>Compound interest</b> is interest added to the total each year, so next year's interest is bigger. "
        "Value after <i>n</i> years = start × multiplier<sup><i>n</i></sup>. The same idea works for <b>depreciation</b> "
        "(a falling value) and for populations that grow or shrink by a percentage.</p>",
        [("£2,000 at 3% compound interest for 2 years.", ["Multiplier 1.03.", "2000 × 1.03<sup>2</sup> = 2121.80."], "£2,121.80"),
         ("A £12,000 car loses 20% a year. Value after 3 years?", ["Multiplier 0.8.", "12000 × 0.8<sup>3</sup> = 6144."], "£6,144"),
         ("Compare with 3% simple interest on £2,000 for 2 years.", ["£60 a year, × 2 = £120."], "£2,120 (less than compound)")],
        ["Using simple interest when the question says compound.",
         "Writing 1.5 for a 5% increase. 5% is 0.05, so the multiplier is 1.05.",
         "Giving the interest when the question asks for the total, or the total when it asks for the interest.",
         "Multiplying by the multiplier × the number of years (1.03 × 4) instead of using a power (1.03<sup>4</sup>)."])


def main():
    sets = [S("Multipliers", collect(one_mult, 20, R)),
            S("Compound interest", collect(one_ci, 20, R)),
            S("Depreciation", collect(one_dep, 20, R)),
            S("Growth, decay and interest earned", collect(one_growth, 20, R)),
            S("Compound interest problems", problems())]
    make(9, "compound-interest-and-growth", 8, "R",
         "Compound Interest and Growth",
         "Year 9 Compound Interest Worksheets: Multipliers, Depreciation, Growth and Decay",
         "Compound Interest",
         "Solve problems involving percentage change, including: percentage increase, decrease and original value problems "
         "and simple interest in financial mathematics; use compound units and repeated percentage change.",
         "Free Year 9 compound interest worksheets: percentage multipliers, compound interest, depreciation, population "
         "growth and decay, and simple vs compound interest. 100 questions with answers.",
         "Value after n years = start × multiplierⁿ.",
         "A 4% increase is × 1.04. A 15% decrease is × 0.85.",
         body(),
         [("What is the formula for compound interest?", "Amount = start × (1 + r/100)ⁿ, where r is the interest rate and n is the number of years. For 3% for 5 years, multiply by 1.03⁵."),
          ("What is the difference between simple and compound interest?", "Simple interest pays the same amount every year, based on the start amount. Compound interest pays interest on the interest too, so it grows faster."),
          ("What is depreciation?", "A loss in value over time. If a car loses 20% a year, multiply by 0.8 for each year."),
          ("How do I find a multiplier?", "For an increase add the percentage to 100%; for a decrease subtract it. Then divide by 100: 7% increase is 1.07, 7% decrease is 0.93.")],
         sets, R)


if __name__ == "__main__":
    main()
