# -*- coding: utf-8 -*-
"""
Texas Grade 5 Math: Personal Financial Literacy: Taxes, Income and Budgets (TEKS 5.10A–5.10F)
  python3 tools/gen_ustx_math_g5_financial_literacy.py
Types of taxes, gross and net income, payment methods (check, credit card, debit card and electronic payments),
financial records, and balancing a simple budget.
Wrong answers come from real mistakes: mixing up gross and net income, thinking a credit card is your own money,
and adding expenses to income.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_ustx_math_g4_financial_literacy as g4f
tx_common.GRADE = "grade-5"

facts = g4f.facts

TAX = [("What is income tax?", "A tax on the money people earn", ["A tax on things you buy at a store", "A tax on land and buildings", "A fee a bank charges"], "<b>Income tax</b> is paid on money earned. Texas has no state income tax, but people pay federal income tax."),
       ("What is sales tax?", "A tax added to the price of things you buy", ["A tax on your paycheck", "A tax on houses and land", "Money a store pays you"], "<b>Sales tax</b> is added when you buy goods. In Texas the state rate is 6.25%, and cities can add more."),
       ("What is property tax?", "A tax on land and buildings that people own", ["A tax on food", "A tax taken from a paycheck for Social Security", "A tax on toys"], "<b>Property tax</b> is paid by owners of homes and land. It helps pay for schools and roads."),
       ("What is payroll tax?", "A tax taken from a paycheck for Social Security and Medicare", ["A tax on things you buy", "A tax on a house", "A fee for using a credit card"], "<b>Payroll taxes</b> are taken from paychecks and pay for Social Security and Medicare."),
       ("The Garcia family pays a tax each year on their house in Austin. What kind of tax is it?", "Property tax", ["Sales tax", "Payroll tax", "Income tax"], "A tax on a house is a <b>property tax</b>."),
       ("Maya buys a backpack and pays a little more than the price on the tag. Why?", "Sales tax is added", ["Property tax is added", "Payroll tax is added", "Income tax is added"], "<b>Sales tax</b> is added when you buy something."),
       ("Which tax helps pay for Social Security?", "Payroll tax", ["Sales tax", "Property tax", "A late fee"], "<b>Payroll tax</b> pays for Social Security and Medicare."),
       ("Which tax is taken out based on how much a worker earns in a year?", "Income tax", ["Property tax", "Sales tax", "Toll fee"], "<b>Income tax</b> is based on earnings."),
       ("Property taxes in Texas help pay for which of these?", "Public schools", ["A family's groceries", "A store's profits", "A person's credit card bill"], "Property taxes help pay for <b>public schools</b> and other local services.")]


def one_sales(r):
    p = r.choice([10, 20, 40, 50, 80, 100])
    t = r.choice([1, 2, 3, 4, 5, 6, 8])
    tax = p * t // 100 if p * t % 100 == 0 else None
    item = r.choice(["a bike helmet", "a pair of shoes", "a video game", "a jacket", "a lamp"])
    if tax is None:
        tt = p * t
        return mcq("The price of %s is $%d. The sales tax is $%d.%02d. What is the total cost?" % (item, p, tt // 100, tt % 100), "$%d.%02d" % (p + tt // 100, tt % 100), ["$%d" % p, "$%d.%02d" % (tt // 100, tt % 100), "$%d.%02d" % (p - tt // 100 - 1, 100 - tt % 100) if tt % 100 else "$%d" % (p - tt // 100)],
                   "Price + sales tax = $%d + $%d.%02d = <b>$%d.%02d</b>." % (p, tt // 100, tt % 100, p + tt // 100, tt % 100))
    return mcq("The price of %s is $%d. The sales tax is $%d. What is the total cost?" % (item, p, tax), "$%d" % (p + tax), ["$%d" % p, "$%d" % (p - tax), "$%d" % tax], "Price + sales tax = $%d + $%d = <b>$%d</b>." % (p, tax, p + tax))


def one_tax(r):
    return facts(TAX)(r) if r.random() < 0.6 else one_sales(r)


INC = [("What is gross income?", "All the money earned before taxes and other deductions", ["The money left after taxes", "The money spent on bills", "The money in a savings account"], "<b>Gross</b> income is the total earned before anything is taken out."),
       ("What is net income?", "The money left after taxes and other deductions are taken out", ["All the money earned before taxes", "The price of a house", "Money borrowed from a bank"], "<b>Net</b> income is the take-home pay."),
       ("Which is usually greater, gross income or net income?", "Gross income", ["Net income", "They are always equal", "It depends on the price of food"], "Taxes are taken out of gross income, so <b>gross income</b> is greater."),
       ("A paycheck shows: Earnings $800; Taxes $120. Which amount is the gross income?", "$800", ["$120", "$680", "$920"], "Gross income is the total earned: <b>$800</b>.")]


def one_net(r):
    k = Kid(r).next()
    kind = r.choice(["net", "gross", "tax", "year"])
    g = r.randint(18, 60) * 100
    t = g * r.choice([10, 12, 15, 20]) // 100
    job = r.choice(["teacher", "nurse", "mechanic", "chef", "electrician", "bus driver"])
    if kind == "net":
        return mcq("%s's aunt is a %s. Her gross income is $%s a month. $%s is taken out for taxes. What is her net income?" % (k["n"], job, comma(g), comma(t)), "$%s" % comma(g - t), ["$%s" % comma(g + t), "$%s" % comma(g), "$%s" % comma(t)],
                   "Net = gross − taxes = $%s − $%s = <b>$%s</b>." % (comma(g), comma(t), comma(g - t)))
    if kind == "gross":
        return mcq("A %s takes home $%s a month after $%s in taxes. What is the gross income?" % (job, comma(g - t), comma(t)), "$%s" % comma(g), ["$%s" % comma(g - 2 * t), "$%s" % comma(g - t), "$%s" % comma(t)],
                   "Gross = net + taxes = $%s + $%s = <b>$%s</b>." % (comma(g - t), comma(t), comma(g)))
    if kind == "tax":
        return mcq("A %s earns $%s (gross) and takes home $%s (net). How much was taken out for taxes?" % (job, comma(g), comma(g - t)), "$%s" % comma(t), ["$%s" % comma(g + g - t), "$%s" % comma(g - t), "$%s" % comma(t + 100)],
                   "$%s − $%s = <b>$%s</b>." % (comma(g), comma(g - t), comma(t)))
    w = r.randint(9, 25)
    h = r.choice([10, 20, 30, 40])
    tx = w * h * r.choice([1, 2]) // 10
    return mcq("%s works %d hours a week at $%d an hour. $%d a week is taken out for taxes. What is the net income for one week?" % (k["n"], h, w, tx), "$%s" % comma(w * h - tx), ["$%s" % comma(w * h), "$%s" % comma(w * h + tx), "$%s" % comma(w + h)],
               "Gross: %d × $%d = $%s. Net: $%s − $%d = <b>$%s</b>." % (h, w, comma(w * h), comma(w * h), tx, comma(w * h - tx)))


def one_income(r):
    return facts(INC)(r) if r.random() < 0.35 else one_net(r)


PAY = [("Which payment method takes money straight from your bank account when you swipe it?", "Debit card", ["Credit card", "Gift card from a friend", "Loan"], "A <b>debit card</b> uses money already in your bank account."),
       ("What is true about a credit card?", "You borrow money and must pay it back later, sometimes with interest", ["It uses money you already have in the bank", "It is the same as cash", "You never have to pay the money back"], "A <b>credit card</b> is a loan. If you do not pay the full bill on time, you pay interest."),
       ("What is one disadvantage of paying with a check?", "It can take days to clear, and some stores do not accept checks", ["It costs interest every month", "It can only be used online", "It never leaves a record"], "Checks are slow to clear and are <b>not accepted everywhere</b>."),
       ("What is one advantage of a debit card?", "You spend only money you have, so you do not get into debt", ["You can spend more than you have", "It earns interest for you", "It never needs a PIN"], "A debit card spends <b>only money in your account</b>."),
       ("What is one advantage of a credit card?", "You can buy something now and pay for it later", ["It never charges interest", "It uses only cash", "You never get a bill"], "A credit card lets you <b>pay later</b>, but you must pay the bill."),
       ("Which is an electronic payment?", "Paying a bill online with a bank app", ["Paying with coins", "Writing a paper check", "Trading toys"], "Paying through an app or website is an <b>electronic payment</b>."),
       ("What is one disadvantage of a credit card?", "Interest can make things cost more if you do not pay the bill in full", ["Money comes out of your account right away", "It cannot be used at stores", "It never leaves a record"], "<b>Interest</b> is charged on unpaid credit card balances."),
       ("What is one advantage of electronic payments?", "They are fast and leave a record of each payment", ["They never need an account", "They always cost interest", "They can only be used for groceries"], "Electronic payments are <b>quick</b> and keep a <b>record</b>."),
       ("Mr. Lee wants to pay rent by mail. Which method is best?", "A check", ["Coins in an envelope", "A debit card swipe", "A gift card"], "A <b>check</b> can be mailed safely."),
       ("Why should a person keep a credit card bill low?", "To avoid paying extra money as interest", ["To earn more interest", "So the bank pays them", "Credit cards have no bills"], "Paying the full balance <b>avoids interest</b>.")]


def one_paymath(r):
    k = Kid(r).next()
    kind = r.choice(["debit", "credit", "check"])
    if kind == "debit":
        b, p = r.randint(80, 400), r.randint(15, 75)
        return mcq("%s has $%d in a bank account. %s pays $%d for shoes with a debit card. How much is left in the account?" % (k["n"], b, k["He"], p), "$%d" % (b - p), ["$%d" % b, "$%d" % (b + p), "$%d" % p],
                   "A debit card takes money from the account right away: $%d − $%d = <b>$%d</b>." % (b, p, b - p))
    if kind == "credit":
        p, i = r.choice([100, 200, 300, 400, 500]), r.choice([10, 15, 20])
        it = p * i // 100
        return mcq("Ms. Ortiz buys a $%d tablet with a credit card. She does not pay the bill on time, so she is charged %d%% interest ($%d). How much does she owe now?" % (p, i, it), "$%d" % (p + it), ["$%d" % p, "$%d" % (p - it), "$%d" % it],
                   "With a credit card, unpaid bills grow with interest: $%d + $%d = <b>$%d</b>." % (p, it, p + it))
    b, c = r.randint(300, 900), r.randint(40, 250)
    return mcq("Mr. Nguyen has $%d in checking. He writes a check for $%d to pay a plumber. What will his balance be after the check clears?" % (b, c), "$%d" % (b - c), ["$%d" % (b + c), "$%d" % b, "$%d" % (b - c + 100)],
               "When the check clears, $%d leaves the account: $%d − $%d = <b>$%d</b>." % (c, b, c, b - c))


def one_record(r):
    k = Kid(r).next()
    start = r.randint(40, 300)
    moves = [("Deposit: birthday money", r.randint(10, 60)), ("Payment: soccer cleats", -r.randint(15, 70)), ("Deposit: dog walking", r.randint(8, 40)), ("Payment: movie tickets", -r.randint(8, 30))]
    r.shuffle(moves)
    moves = moves[:3]
    bal = start
    rows = ["<tr><td>Starting balance</td><td></td><td>$%d</td></tr>" % start]
    for i, (d, a) in enumerate(moves):
        bal += a
        rows.append("<tr><td>%s</td><td>%s$%d</td><td>%s</td></tr>" % (d, "+" if a > 0 else "−", abs(a), "$%d" % bal if i < len(moves) - 1 else "?"))
    if bal <= 0:
        return None
    pic = "<div class='qfig'><div class='sn-tw'><table class='sn-table'><thead><tr><th>%s's record</th><th>Amount</th><th>Balance</th></tr></thead><tbody>%s</tbody></table></div></div>" % (k["n"], "".join(rows))
    last = moves[-1][1]
    return mcq(pic + "What is the balance after the last entry?", "$%d" % bal, ["$%d" % (bal - 2 * last), "$%d" % (start + sum(abs(a) for _, a in moves)), "$%d" % (bal + 10)],
               "%s $%d %s $%d = <b>$%d</b>." % ("Previous balance", bal - last, "+" if last > 0 else "−", abs(last), bal))


RECF = [("Why do people keep financial records?", "To track income and spending and plan ahead", ["To make prices go down", "To avoid paying taxes", "To get a bigger paycheck"], "Records help people <b>track money</b> and make a plan."),
        ("Which is a financial record?", "A bank statement", ["A grocery list", "A birthday card", "A math test"], "A <b>bank statement</b> records deposits and payments."),
        ("Which is a financial record?", "A receipt from a store", ["A recipe", "A movie poster", "A library card"], "A <b>receipt</b> records what you bought and paid."),
        ("What is a deposit?", "Money put into an account", ["Money taken out of an account", "A tax on a house", "A credit card bill"], "A <b>deposit</b> adds money to an account."),
        ("What is a withdrawal?", "Money taken out of an account", ["Money put into an account", "Interest a bank pays", "A type of tax"], "A <b>withdrawal</b> takes money out.")]


def one_records(r):
    return facts(RECF)(r) if r.random() < 0.35 else one_record(r)


def one_budget(r):
    k = Kid(r).next()
    inc = r.randint(30, 90) * 10
    kind = r.choice(["left", "over", "action", "fix"])
    names = ["Food", "Phone", "Gas", "Fun", "Savings"]
    vals = [r.randint(2, 30) * 10 for _ in names]
    tot = sum(vals)
    rows = "".join("<tr><td>%s</td><td>$%d</td></tr>" % (n, v) for n, v in zip(names, vals))
    pic = "<div class='qfig'><div class='sn-tw'><table class='sn-table'><thead><tr><th>Monthly budget</th><th>Amount</th></tr></thead><tbody><tr><td><b>Income</b></td><td><b>$%s</b></td></tr>%s</tbody></table></div></div>" % (comma(inc), rows)
    if kind == "left":
        if tot >= inc:
            return None
        return mcq(pic + "How much money is left after all the expenses?", "$%s" % comma(inc - tot), ["$%s" % comma(inc + tot), "$%s" % comma(tot), "$%s" % comma(inc - tot + vals[0])],
                   "Expenses: %s = $%s. $%s − $%s = <b>$%s</b>." % (" + ".join("$%d" % v for v in vals), comma(tot), comma(inc), comma(tot), comma(inc - tot)))
    if kind == "over":
        if tot <= inc:
            return None
        return mcq(pic + "Is the budget balanced? By how much?", "No, expenses are $%s more than income" % comma(tot - inc), ["Yes, it is balanced", "No, income is $%s more than expenses" % comma(tot - inc), "No, expenses are $%s more than income" % comma(tot)],
                   "Expenses are $%s and income is $%s. $%s − $%s = <b>$%s too much</b>." % (comma(tot), comma(inc), comma(tot), comma(inc), comma(tot - inc)))
    if kind == "action":
        return facts([("A family's expenses are greater than their income. Which action helps balance the budget?", "Spend less on eating out", ["Use a credit card for everything", "Buy more toys", "Stop keeping records"], "Cutting a <b>variable expense</b> like eating out helps."),
                      ("Expenses are $50 more than income. Which plan balances the budget?", "Earn $30 more and spend $20 less", ["Spend $50 more", "Earn $20 more and spend $10 more", "Do nothing"], "$30 + $20 = $50, which covers the gap."),
                      ("What does a balanced budget mean?", "Income is equal to or greater than expenses", ["Expenses are greater than income", "There are no expenses", "All money goes to fun"], "A budget is balanced when <b>income covers expenses</b>."),
                      ("Which is a way to increase income?", "Get a part-time job", ["Buy a new phone", "Pay a bill late", "Spend savings on games"], "A <b>job</b> brings in more income."),
                      ("Which expense is easiest to cut to balance a budget?", "Entertainment", ["Rent", "Electricity", "Car insurance"], "<b>Entertainment</b> is a want, not a need.")])(r)
    if tot <= inc:
        return None
    cut = tot - inc
    i = max(range(5), key=lambda t: vals[t])
    if vals[i] < cut:
        return None
    return mcq(pic + "%s wants to balance the budget by cutting only the %s expense. What should the new amount be?" % (k["n"], names[i].lower()), "$%d" % (vals[i] - cut), ["$%d" % cut, "$%d" % (vals[i] + cut), "$%d" % (vals[i] - cut // 2)] if vals[i] != cut * 2 else ["$%d" % (vals[i] + cut), "$%d" % (vals[i] - 10), "$%d" % (cut + 10)],
               "Expenses are $%s more than income. $%d − $%s = <b>$%d</b>." % (comma(cut), vals[i], comma(cut), vals[i] - cut))


def build():
    sets, R = build_sets([
        ("Types of taxes", [("collect", one_tax, 20)]),
        ("Gross and net income", [("collect", one_income, 20)]),
        ("Ways to pay", [("collect", facts(PAY), 10), ("collect", one_paymath, 10)]),
        ("Financial records", [("collect", one_records, 20)]),
        ("Balance a budget", [("collect", one_budget, 20)]),
    ], 65022)
    finish(sets, R)
    body = lesson('<ul><li><b>Taxes</b>: income tax (on earnings), payroll tax (from paychecks, for Social Security and Medicare), sales tax (on things you buy) and property tax (on homes and land).</li><li><b>Gross income</b> is all you earn. <b>Net income</b> is what is left after taxes: net = gross − taxes.</li><li>Ways to pay: cash, check, debit card (your money), credit card (borrowed money) and electronic payments.</li><li>Keep <b>records</b> of deposits and payments. A budget is <b>balanced</b> when income covers expenses.</li></ul>',
        [example("Gross income $2,400. Taxes $360.", ["Net = gross − taxes", "$2,400 − $360"], "$2,040"), example("Income $500. Expenses $540.", ["$540 − $500 = $40 over", "Cut $40 from fun or earn $40 more"], "balanced")],
        [['Mixing up gross and net income', 'Gross is before taxes; net is take-home pay.'], ['Thinking a credit card is your own money', 'A credit card is a loan you must pay back.'], ['Adding expenses to income', 'Subtract expenses from income to see what is left.']])
    faq = [('What does TEKS 5.10 cover?', 'Defining income, payroll, sales and property taxes; gross and net income; payment methods; financial records; and balancing a simple budget.'), ('Does Texas have a state income tax?', 'No. Texans pay federal income tax but no state income tax. Texas has sales and property taxes.'), ('What is the difference between a debit card and a credit card?', 'A debit card spends money already in your bank account. A credit card borrows money you must pay back.'), ('What does it mean to balance a budget?', 'Make sure income is equal to or more than expenses, by spending less, earning more or both.')]
    make('personal-financial-literacy', 22, 'Personal Financial Literacy', '5.10A–5.10F',
         '5.10A define income tax, payroll tax, sales tax, and property tax; 5.10B explain the difference between gross income and net income; 5.10C identify the advantages and disadvantages of different methods of payment, including check, credit card, debit card, and electronic payments; 5.10D develop a system for keeping and using financial records; 5.10E describe actions that might be taken to balance a budget when expenses exceed income; 5.10F balance a simple budget',
         'Personal Financial Literacy: Taxes, Income and Budgets', 'Personal Financial Literacy',
         'Free Grade 5 personal financial literacy worksheets for Texas TEKS 5.10: types of taxes, gross and net income, payment methods, financial records and balancing a budget. 100 questions with answers.',
         'Net income = gross income − taxes. Balance a budget so income covers expenses.', 'Debit spends your money; credit borrows. Keep records of every deposit and payment.',
         body, faq, sets, seo_title='Grade 5 Personal Financial Literacy Worksheets: Taxes, Income and Budgets (TEKS 5.10, STAAR)')


if __name__ == "__main__":
    build()
