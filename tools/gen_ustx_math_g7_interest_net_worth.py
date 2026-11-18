# -*- coding: utf-8 -*-
"""
Texas Grade 7 Math: Simple and Compound Interest, Net Worth and Incentives (TEKS 7.13C, 7.13E, 7.13F)
  python3 tools/gen_ustx_math_g7_interest_net_worth.py
Assets and liabilities, net worth statements, simple interest, compound interest compared with simple interest, and
sales, rebates and coupons.
Wrong answers come from real mistakes: adding liabilities to net worth, forgetting to multiply by the years, and
applying a coupon before a percent discount when the order matters.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_ustx_math_g4_financial_literacy as g4f
tx_common.GRADE = "grade-7"

facts = g4f.facts


def m(v):
    """Money with cents, commas for thousands."""
    v = round(v + 1e-9, 2)
    d, c = divmod(int(round(v * 100)), 100)
    return "$%s.%02d" % (comma(d), c)


def art(v):
    """'an' before amounts read as eight-, eleven- or eighteen-..."""
    n = str(int(v))
    return "an" if n[0] == "8" or n in ("11", "18") else "a"


def md(v):
    """Whole dollars."""
    return "$%s" % comma(int(round(v)))


AL = [("Which is an <b>asset</b>?", "Money in a savings account", ["A car loan", "Credit card debt", "A student loan"], "An <b>asset</b> is something of value that you own."),
      ("Which is a <b>liability</b>?", "A balance owed on a credit card", ["A savings account", "A bicycle you own", "Cash in your wallet"], "A <b>liability</b> is money you owe."),
      ("Which is an asset?", "A house the family owns", ["The mortgage on the house", "An unpaid medical bill", "A personal loan"], "The house is an <b>asset</b>; the mortgage is a liability."),
      ("Which is a liability?", "A student loan", ["A checking account", "A laptop you own", "A savings bond"], "Money still owed on a loan is a <b>liability</b>."),
      ("What is net worth?", "The value of assets minus liabilities", ["Assets plus liabilities", "Income minus expenses for one month", "The price of a house"], "<b>Net worth = assets − liabilities.</b>"),
      ("What does a negative net worth mean?", "The person owes more than they own", ["The person owns more than they owe", "The person has no income", "The person has no expenses"], "Liabilities are greater than assets.")]


def one_networth(r):
    k = Kid(r).next()
    assets = [("Savings account", r.randint(5, 60) * 100), ("Car", r.randint(40, 150) * 100), ("Checking account", r.randint(2, 30) * 100)]
    liab = [("Car loan", r.randint(20, 120) * 100), ("Credit card balance", r.randint(2, 30) * 100)]
    if r.random() < 0.4:
        assets = assets[:2]
    A, L = sum(v for _, v in assets), sum(v for _, v in liab)
    rows = "".join("<tr><td>%s</td><td>%s</td><td></td></tr>" % (n, md(v)) for n, v in assets) + "".join("<tr><td>%s</td><td></td><td>%s</td></tr>" % (n, md(v)) for n, v in liab)
    pic = "<div class='qfig'><div class='sn-tw'><table class='sn-table'><thead><tr><th>Item</th><th>Asset</th><th>Liability</th></tr></thead><tbody>%s</tbody></table></div></div>" % rows
    kind = r.choice(["nw", "nw", "a", "l"])
    if kind == "a":
        return mcq(pic + "What is the total value of the assets?", md(A), [md(A + L), md(L), md(A - L)], "Add the asset column: <b>%s</b>." % md(A), allow_zero=True)
    if kind == "l":
        return mcq(pic + "What is the total of the liabilities?", md(L), [md(A), md(A + L), md(abs(A - L))], "Add the liability column: <b>%s</b>." % md(L))
    nw = A - L
    s = md(abs(nw)) if nw >= 0 else "−" + md(abs(nw))
    return mcq(pic + "What is the net worth?", s, [md(A + L), ("−" + md(abs(nw))) if nw > 0 else md(abs(nw)), md(A)],
               "Net worth = assets − liabilities = %s − %s = <b>%s</b>." % (md(A), md(L), s))


def one_simple(r):
    p = r.choice([200, 500, 800, 1000, 1200, 1500, 2000, 2500, 5000])
    rate = r.choice([2, 3, 4, 5, 6])
    t = r.choice([2, 3, 4, 5])
    i = p * rate * t // 100
    if p * rate * t % 100:
        return None
    if r.random() < 0.6:
        return mcq("%s is deposited at %d%% simple interest per year for %d years. How much interest is earned?" % (md(p), rate, t), md(i), [md(p * rate // 100), md(p + i), md(i * 10)],
                   "I = Prt = %s × %s × %d = <b>%s</b>." % (md(p), ("%.2f" % (rate / 100.0)).rstrip("0"), t, md(i)))
    return mcq("%s earns %d%% simple interest each year. What is the balance after %d years?" % (md(p), rate, t), md(p + i), [md(i), md(p + p * rate // 100), md(p * (100 + rate) // 100 * t)],
               "I = %s × %s × %d = %s. Balance = %s + %s = <b>%s</b>." % (md(p), ("%.2f" % (rate / 100.0)).rstrip("0"), t, md(i), md(p), md(i), md(p + i)))


def one_compound(r):
    p = r.choice([1000, 2000, 5000, 10000])
    rate = r.choice([5, 10])
    t = r.choice([2, 3])
    bal = float(p)
    for _ in range(t):
        bal *= 1 + rate / 100.0
    simple = p + p * rate * t / 100.0
    kind = r.choice(["bal", "earn", "diff"])
    if kind == "bal":
        return mcq("%s is invested at %d%% interest compounded once a year. What is the balance after %d years?" % (md(p), rate, t), m(bal), [m(simple), m(p * (1 + rate * t / 100.0) * 1.1), m(p * rate * t / 100.0)],
                   "Each year multiply by %s: %s × %s<sup>%d</sup> = <b>%s</b>." % (1 + rate / 100.0, md(p), 1 + rate / 100.0, t, m(bal)))
    if kind == "earn":
        return mcq("%s earns %d%% interest compounded yearly for %d years. How much interest is earned in all?" % (md(p), rate, t), m(bal - p), [m(simple - p), m(bal), m(p * rate / 100.0)],
                   "Balance: %s. Interest: %s − %s = <b>%s</b>." % (m(bal), m(bal), md(p), m(bal - p)))
    return mcq("%s is saved for %d years at %d%%. How much more interest does compound interest (yearly) earn than simple interest?" % (md(p), t, rate), m(bal - simple), [m(simple - p), m(bal - p), "$0.00"],
               "Compound: %s. Simple: %s. %s − %s = <b>%s</b>. Compound interest also earns interest on the interest." % (m(bal), m(simple), m(bal), m(simple), m(bal - simple)))


def one_deal(r):
    k = Kid(r).next()
    kind = r.choice(["rebate", "coupon", "compare", "pct_vs_off"])
    price = r.choice([40, 60, 80, 120, 150, 200, 250, 300])
    if kind == "rebate":
        reb = r.choice([10, 15, 20, 25, 50])
        return mcq("A printer costs %s. It has %s %s mail-in rebate. What is the final cost after the rebate?" % (md(price), art(reb), md(reb)), md(price - reb), [md(price + reb), md(price), md(price * (100 - reb) // 100)],
                   "A rebate is money back after you buy: %s − %s = <b>%s</b>." % (md(price), md(reb), md(price - reb)))
    if kind == "coupon":
        c = r.choice([5, 10, 15, 20])
        return mcq("%s has %s %s coupon for %s %s pair of shoes. How much does %s pay before tax?" % (k["n"], art(c), md(c), art(price), md(price), k["he"]), md(price - c), [md(price), md(price + c), md(price * (100 - c) // 100)],
                   "%s − %s = <b>%s</b>." % (md(price), md(c), md(price - c)))
    if kind == "compare":
        pct = r.choice([10, 15, 20, 25, 30])
        off = r.choice([10, 15, 20, 25, 30, 40, 50])
        a, b = price * (100 - pct) / 100.0, price - off
        if a == b:
            return None
        best = "Store A (%s)" % m(a) if a < b else "Store B (%s)" % m(b)
        return mcq("%s %s bike helmet is on sale. Store A takes %d%% off. Store B takes %s off. Which is the better deal?" % (art(price).capitalize(), md(price), pct, md(off)), best, ["Store B (%s)" % m(b) if a < b else "Store A (%s)" % m(a), "They cost the same", "Store A (%s)" % m(price - pct) if a < b else "Store B (%s)" % m(price * (100 - off) / 100.0)],
                       "A: %s × %s = %s. B: %s − %s = %s. <b>%s</b> costs less." % (md(price), ("%.2f" % ((100 - pct) / 100.0)).rstrip("0"), m(a), md(price), md(off), m(b), best))
    pct = r.choice([10, 20, 25])
    c = r.choice([5, 10])
    first = price * (100 - pct) / 100.0 - c
    second = (price - c) * (100 - pct) / 100.0
    return mcq("%s %s jacket is %d%% off, and you also have %s %s coupon. The store takes the %d%% off first, then the coupon. What do you pay?" % (art(price).capitalize(), md(price), pct, art(c), md(c), pct), m(first), [m(second), m(price - c), m(price * (100 - pct) / 100.0)],
               "%s × %s = %s. %s − %s = <b>%s</b>." % (md(price), ("%.2f" % ((100 - pct) / 100.0)).rstrip("0"), m(price * (100 - pct) / 100.0), m(price * (100 - pct) / 100.0), md(c), m(first)))


def build():
    sets, R = build_sets([
        ("Assets and liabilities", [("collect", facts(AL), 6), ("collect", one_networth, 14)]),
        ("Net worth statements", [("collect", one_networth, 20)]),
        ("Simple interest", [("collect", one_simple, 20)]),
        ("Compound interest and simple interest", [("collect", one_compound, 20)]),
        ("Sales, rebates and coupons", [("collect", one_deal, 20)]),
    ], 67025)
    finish(sets, R)
    body = lesson('<ul><li><b>Assets</b> are things of value you own; <b>liabilities</b> are debts you owe. <b>Net worth</b> = assets − liabilities.</li><li><b>Simple interest</b>: I = Prt (principal × rate × time in years).</li><li><b>Compound interest</b> earns interest on the interest too: multiply by (1 + rate) each year.</li><li>Compare deals by finding the final price: sales and coupons lower the price now; rebates give money back later.</li></ul>',
        [example("$1,000 at 5% simple interest for 3 years", ["1,000 × 0.05 × 3"], "$150"), example("$1,000 at 10% compounded yearly for 2 years", ["1,000 × 1.1 × 1.1"], "$1,210")],
        [['Adding liabilities to net worth', 'Subtract what you owe from what you own.'], ['Forgetting to multiply by the years', 'I = Prt: use the number of years.'], ['Treating compound interest like simple interest', "Each year's interest is added before the next year."]])
    faq = [('What does TEKS 7.13C ask?', 'Create and organize a financial assets and liabilities record and construct a net worth statement.'), ('What does TEKS 7.13E ask?', 'Calculate and compare simple interest and compound interest earnings.'), ('What does TEKS 7.13F ask?', 'Analyze and compare monetary incentives, including sales, rebates and coupons.'), ('Why does compound interest earn more?', "Interest is added to the balance, so next year's interest is on a bigger amount.")]
    make('interest-net-worth-and-incentives', 25, 'Personal Financial Literacy', '7.13C, 7.13E, 7.13F',
         '7.13C create and organize a financial assets and liabilities record and construct a net worth statement; 7.13E calculate and compare simple interest and compound interest earnings; 7.13F analyze and compare monetary incentives, including sales, rebates, and coupons',
         'Simple and Compound Interest, Net Worth and Incentives', 'Interest, Net Worth and Incentives',
         'Free Grade 7 personal financial literacy worksheets for Texas TEKS 7.13C, 7.13E and 7.13F: assets, liabilities and net worth, simple and compound interest, sales, rebates and coupons. 100 questions with answers.',
         'Net worth = assets − liabilities. Simple interest I = Prt.', 'Compound interest earns interest on interest: $1,000 at 10% for 2 years = $1,210.',
         body, faq, sets, seo_title='Grade 7 Simple and Compound Interest, Net Worth and Incentives Worksheets (TEKS 7.13, STAAR)')


if __name__ == "__main__":
    build()
