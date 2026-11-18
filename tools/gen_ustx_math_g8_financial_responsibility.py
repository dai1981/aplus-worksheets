# -*- coding: utf-8 -*-
"""
Texas Grade 8 Math: Payment Methods and Financial Responsibility (TEKS 8.12E, 8.12F)
  python3 tools/gen_ustx_math_g8_financial_responsibility.py
Advantages and disadvantages of cash, checks, debit cards, credit cards and electronic payments, the cost of late
fees and interest, and deciding whether a choice is financially responsible.
Wrong answers come from real mistakes: thinking a credit card is free money, ignoring fees, and buying wants before
needs.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_ustx_math_g4_financial_literacy as g4f
tx_common.GRADE = "grade-8"

facts = g4f.facts


def m(v):
    v = round(v + 1e-9, 2)
    d, c = divmod(int(round(v * 100)), 100)
    return "$%s.%02d" % (comma(d), c)


def md(v):
    return "$%s" % comma(int(round(v)))


def pc(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")


PAY = [("What is one advantage of paying with cash?", "You can only spend what you have", ["It builds a credit history", "It is easy to replace if lost", "It earns interest"], "With <b>cash</b> you cannot overspend, but it is hard to replace if lost."),
       ("What is one disadvantage of paying with cash?", "It cannot be replaced if it is lost or stolen", ["It always costs interest", "It needs a credit check", "It is accepted nowhere"], "Lost cash is usually gone for good."),
       ("What is an advantage of a credit card used responsibly?", "It can build a positive credit history", ["It never charges interest", "It uses money from your savings", "It cannot be stolen"], "Paying the full balance on time builds <b>good credit</b>."),
       ("What is a disadvantage of a credit card?", "High interest if the balance is not paid in full", ["It takes money from your checking account right away", "It cannot be used online", "It has no record"], "Unpaid balances grow with <b>interest</b>."),
       ("What is an advantage of a debit card?", "It takes money you already have, so you avoid debt", ["It always builds credit", "It has no daily limit", "It cannot be used at stores"], "A <b>debit card</b> spends money in your account."),
       ("What is a disadvantage of a debit card?", "Overdraft fees if you spend more than your balance", ["It charges interest every month", "It needs a co-signer", "It cannot be used online"], "Spending past your balance can bring <b>overdraft fees</b>."),
       ("What is an advantage of electronic payments, like paying with a phone app?", "They are fast and keep a record", ["They never need an account", "They can never be hacked", "They earn interest"], "Electronic payments are <b>quick</b> and leave a <b>record</b>."),
       ("What is a disadvantage of paying by check?", "It can take days to clear and some stores do not accept it", ["It charges interest", "It builds debt", "It cannot be tracked"], "Checks are <b>slow</b> and not accepted everywhere.")]

RESP = [("Which is a financially responsible decision?", "Paying the full credit card balance every month", ["Paying only the minimum and buying more", "Taking a payday loan for concert tickets", "Skipping the electric bill to buy shoes"], "Paying in full avoids interest and builds good credit."),
        ("Which is <b>not</b> financially responsible?", "Using a credit card for things you cannot pay off", ["Saving part of each paycheck", "Comparing prices before buying", "Keeping an emergency fund"], "Charging what you cannot repay leads to debt and interest."),
        ("What is a benefit of financial responsibility?", "Lower interest rates and less stress about money", ["Never needing a job", "Higher prices at stores", "More late fees"], "Good habits bring better rates and peace of mind."),
        ("What is a cost of financial irresponsibility?", "Late fees, high interest and a poor credit history", ["Lower interest rates", "More savings", "A higher credit score"], "Missed payments bring <b>fees, interest and bad credit</b>."),
        ("Marisol wants a $900 phone. Which plan is most responsible?", "Save $150 a month for 6 months, then buy it", ["Put it on a credit card and pay $25 a month", "Take a payday loan", "Use the rent money"], "Saving first avoids interest and debt."),
        ("Which should come first in a budget?", "Needs like housing and food", ["New video games", "Concert tickets", "Eating out every day"], "Pay for <b>needs</b> before wants.")]


def one_cmp(r):
    kind = r.choice(["card", "rto", "minimum"])
    if kind == "card":
        price = r.randrange(300, 1550, 50)
        n = r.choice([12, 18, 24])
        mo = -(-int(price * r.choice([1.12, 1.18, 1.25, 1.3])) // n)
        return mcq("A laptop costs %s in cash. A store card plan is %s a month for %d months. How much more does the card plan cost?" % (md(price), md(mo), n), md(mo * n - price), [md(mo * n), md(price - mo), md(mo)],
                   "%s × %d = %s. %s − %s = <b>%s</b> more." % (md(mo), n, md(mo * n), md(mo * n), md(price), md(mo * n - price)))
    if kind == "rto":
        price = r.randrange(200, 650, 50)
        n = r.choice([52, 78])
        wk = -(-int(price * r.choice([1.6, 1.9, 2.2])) // n)
        return mcq("A TV costs %s at a store. A rent-to-own plan charges %s a week for %d weeks. How much more does rent-to-own cost?" % (md(price), md(wk), n), md(wk * n - price), [md(wk * n), md(price), md(wk * 12)],
                   "%s × %d = %s. That is <b>%s</b> more than buying it." % (md(wk), n, md(wk * n), md(wk * n - price)))
    bal = r.randrange(800, 4200, 100)
    return mcq("Kai owes %s on a credit card at 20%% interest. Which plan costs him the least in interest?" % md(bal), "Pay the full balance as soon as he can", ["Pay only the minimum each month", "Keep using the card for new purchases", "Skip payments for a few months"],
               "Every month a balance stays, interest grows. <b>Paying it off fast</b> costs the least.")


def one_fee(r):
    kind = r.choice(["late", "over", "interest"])
    if kind == "late":
        f = r.choice([25, 30, 35, 40])
        n = r.choice([2, 3, 4, 6])
        return mcq("A credit card charges a %s late fee each time a payment is late. Jaden pays late %d times in a year. How much does he pay in late fees?" % (md(f), n), md(f * n), [md(f), md(f + n), md(f * 12)],
                   "%s × %d = <b>%s</b>, money spent on nothing." % (md(f), n, md(f * n)))
    if kind == "over":
        bal, buy, fee = r.randint(20, 80), r.randint(85, 140), r.choice([30, 35])
        return mcq("Leah has %s in checking. She uses her debit card for a %s purchase, and the bank charges a %s overdraft fee. What is her balance now?" % (md(bal), md(buy), md(fee)), "−" + md(buy + fee - bal), ["−" + md(buy - bal), md(bal - buy + fee) if bal - buy + fee > 0 else "−" + md(buy - bal - fee), "−" + md(fee)],
                   "%s − %s − %s = <b>−%s</b>." % (md(bal), md(buy), md(fee), md(buy + fee - bal)))
    price, rate = r.choice([600, 800, 1000, 1200]), r.choice([18, 20, 24])
    i = price * rate / 100.0
    return mcq("A %s TV is bought with a credit card at %d%% interest a year. If the balance is paid off after one full year (simple interest), what is the total cost?" % (md(price), rate), md(price + i), [md(price), md(i), md(price + rate)],
               "%s × %s = %s interest. Total = <b>%s</b>, compared with %s in cash." % (md(price), pc(rate / 100.0), md(i), md(price + i), md(price)))


def build():
    sets, R = build_sets([
        ("Advantages and disadvantages of payment methods", [("collect", facts(PAY), 8), ("collect", one_fee, 12)]),
        ("The cost of fees and interest", [("collect", one_fee, 20)]),
        ("Financially responsible decisions", [("collect", facts(RESP), 6), ("collect", one_fee, 14)]),
        ("Compare the cost of buying plans", [("collect", one_cmp, 12), ("collect", one_fee, 8)]),
        ("Review problems", [("collect", one_fee, 10), ("collect", one_cmp, 10)]),
    ], 68023)
    finish(sets, R)
    body = lesson('<ul><li><b>Cash</b>: you spend only what you have, but it is hard to replace. <b>Checks</b>: slow and not accepted everywhere.</li><li><b>Debit cards</b> use your own money; overdrafts bring fees. <b>Credit cards</b> are loans; they can build credit but charge interest.</li><li><b>Electronic payments</b> are fast and keep records.</li><li><b>Financial responsibility</b> means paying on time, avoiding high-cost debt, saving and paying for needs first.</li></ul>',
        [example("$800 on a card at 24% for a year", ["0.24 × 800 = $192"], "$992 total")],
        [['Thinking a credit card is free money', 'It is a loan with interest.'], ['Ignoring fees', 'Late and overdraft fees add up quickly.'], ['Buying wants before needs', 'Pay for housing, food and bills first.']])
    faq = [('What does TEKS 8.12E ask?', 'Identify and explain the advantages and disadvantages of different payment methods.'), ('What does TEKS 8.12F ask?', 'Analyze situations to determine if they represent financially responsible decisions and identify the benefits of financial responsibility and the costs of financial irresponsibility.'), ('What is an overdraft?', 'Spending more than is in your account. Banks often charge a fee.'), ('Can a credit card help you?', 'Yes, if you pay the full balance on time: it builds a good credit history.')]
    make('payment-methods-and-financial-responsibility', 23, 'Personal Financial Literacy', '8.12E, 8.12F',
         '8.12E identify and explain the advantages and disadvantages of different payment methods; 8.12F analyze situations to determine if they represent financially responsible decisions and identify the benefits of financial responsibility and the costs of financial irresponsibility',
         'Payment Methods and Financial Responsibility', 'Payment Methods and Responsibility',
         'Free Grade 8 personal financial literacy worksheets for Texas TEKS 8.12E and 8.12F: payment methods, fees and interest, and financially responsible decisions. 100 questions with answers.',
         'Pay on time, avoid high-cost debt and pay for needs first.', 'An $800 TV at 24% for a year costs $992.',
         body, faq, sets, seo_title='Grade 8 Payment Methods and Financial Responsibility Worksheets (TEKS 8.12E, 8.12F, STAAR)')


if __name__ == "__main__":
    build()
