# -*- coding: utf-8 -*-
"""
Texas Grade 6 Math: Personal Financial Literacy: Accounts, Credit, College and Careers (TEKS 6.14A–6.14H)
  python3 tools/gen_ustx_math_g6_financial_literacy.py
Checking accounts, debit and credit cards, balancing a check register, credit history and credit reports, paying for
college, and comparing salaries and lifetime income.
Wrong answers come from real mistakes: treating a credit card as your own money, adding a withdrawal, thinking a
grant must be paid back, and forgetting to multiply by the number of working years.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_ustx_math_g4_financial_literacy as g4f
tx_common.GRADE = "grade-6"

facts = g4f.facts

CARDS = [("What is the main difference between a debit card and a credit card?", "A debit card uses money in your account; a credit card borrows money you must pay back", ["They are exactly the same", "A credit card uses money in your account; a debit card borrows money", "Only a debit card can be used online"], "<b>Debit</b> = your own money. <b>Credit</b> = a loan from the card company."),
         ("What can happen if you do not pay a credit card bill in full?", "You pay interest on the amount you still owe", ["The bank pays the rest", "Nothing happens", "Your checking account earns interest"], "Unpaid credit card balances are charged <b>interest</b>."),
         ("Which is a feature of a checking account?", "You can write checks and use a debit card to pay", ["It always pays high interest", "You can never take money out", "It is the same as a credit report"], "A <b>checking account</b> is for everyday paying."),
         ("Why should you compare checking accounts at different banks?", "Fees, minimum balances and ATM charges can be different", ["Every bank charges the same", "Only the color of the debit card is different", "Checking accounts never have fees"], "Banks and credit unions have different <b>fees and rules</b>."),
         ("What is an overdraft?", "Spending more than the money in your checking account", ["A deposit from a paycheck", "Interest a bank pays you", "A type of savings account"], "An <b>overdraft</b> happens when the balance goes below $0. Banks often charge a fee."),
         ("Which payment can lead to debt if you spend more than you can pay back?", "A credit card", ["A debit card with no overdraft", "Cash", "A prepaid gift card"], "A <b>credit card</b> lets you borrow, which can lead to debt.")]


def one_fee(r):
    a_fee, b_fee = r.choice([(0, 5), (3, 8), (5, 0), (6, 2), (4, 10)])
    a_atm, b_atm = r.choice([(2, 0), (3, 1), (2, 2), (0, 3)])
    n = r.randint(2, 6)
    ca, cb = a_fee + a_atm * n, b_fee + b_atm * n
    if ca == cb:
        return None
    best = "Bank A" if ca < cb else "Credit union B"
    return mcq("Bank A: $%d monthly fee and $%d for each ATM use. Credit union B: $%d monthly fee and $%d for each ATM use. Lena uses an ATM %d times a month. Which account costs less each month?" % (a_fee, a_atm, b_fee, b_atm, n),
               "%s ($%d)" % (best, min(ca, cb)), ["%s ($%d)" % ("Credit union B" if best == "Bank A" else "Bank A", max(ca, cb)), "They cost the same", "%s ($%d)" % (best, min(a_fee, b_fee))],
               "A: $%d + %d × $%d = $%d. B: $%d + %d × $%d = $%d. <b>%s</b> costs less." % (a_fee, n, a_atm, ca, b_fee, n, b_atm, cb, best))


def one_cards(r):
    return facts(CARDS)(r) if r.random() < 0.6 else one_fee(r)


def one_register(r):
    k = Kid(r).next()
    start = r.randint(150, 900)
    moves = [("Deposit: paycheck", r.randint(120, 400)), ("Check #%d: rent share" % r.randint(101, 140), -r.randint(80, 250)), ("Debit card: groceries", -r.randint(25, 90)),
             ("Transfer to savings", -r.choice([20, 25, 50, 100])), ("Deposit: birthday gift", r.randint(20, 75)), ("ATM withdrawal", -r.choice([20, 40, 60]))]
    r.shuffle(moves)
    moves = moves[:r.choice([3, 4])]
    bal = start
    rows = ["<tr><td>Starting balance</td><td></td><td></td><td>$%s</td></tr>" % comma(start)]
    for i, (d, a) in enumerate(moves):
        bal += a
        if bal < 0:
            return None
        rows.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (d, "$%d" % -a if a < 0 else "", "$%d" % a if a > 0 else "", "$%s" % comma(bal) if i < len(moves) - 1 else "?"))
    pic = "<div class='qfig'><div class='sn-tw'><table class='sn-table'><thead><tr><th>Description</th><th>Payment</th><th>Deposit</th><th>Balance</th></tr></thead><tbody>%s</tbody></table></div></div>" % "".join(rows)
    last = moves[-1][1]
    return mcq(pic + "What is the balance after the last entry?", "$%s" % comma(bal), ["$%s" % comma(bal - 2 * last), "$%s" % comma(start + sum(abs(a) for _, a in moves)), "$%s" % comma(bal + 10)],
               "Previous balance $%s %s $%d = <b>$%s</b>. Payments, withdrawals and transfers out are subtracted; deposits are added." % (comma(bal - last), "+" if last > 0 else "−", abs(last), comma(bal)))


CREDIT = [("What is a credit history?", "A record of how a person has borrowed and paid back money", ["A list of a person's school grades", "The amount in a savings account", "A list of things a person bought with cash"], "A <b>credit history</b> shows borrowing and payments."),
          ("Why is a positive credit history important?", "It helps you get loans at lower interest rates", ["It lets you skip paying bills", "It raises your salary", "It closes your bank account"], "Lenders trust borrowers with a good history and offer <b>lower interest rates</b>."),
          ("Which action helps build a positive credit history?", "Paying bills on time every month", ["Missing payments", "Borrowing as much as possible", "Using a credit card past its limit"], "<b>On-time payments</b> build good credit."),
          ("Which information is in a credit report?", "Loans and credit cards, payment history and amounts owed", ["Your favorite foods", "Your test scores", "Your height and weight"], "A credit report lists <b>accounts, payments and debts</b>."),
          ("About how long do most late payments stay on a credit report?", "About 7 years", ["About 1 month", "About 1 year", "Forever"], "Most negative information stays for about <b>7 years</b>; a bankruptcy can stay up to 10 years."),
          ("How do lenders use credit reports?", "To decide whether to lend money and at what interest rate", ["To choose a borrower's job", "To set the price of groceries", "To count a borrower's friends"], "Lenders check reports to judge <b>risk</b>."),
          ("How can a credit report help a borrower?", "It shows mistakes that can be fixed and what lenders will see", ["It pays off debts", "It lowers the price of a car", "It replaces a bank account"], "Checking your report lets you <b>spot errors</b>."),
          ("Who might check your credit report before you rent an apartment?", "A landlord", ["Your teacher", "A grocery store cashier", "Your neighbor"], "<b>Landlords</b> often check credit before renting."),
          ("What usually happens to someone with a poor credit history who asks for a loan?", "They pay a higher interest rate or are turned down", ["They get a lower interest rate", "They get the loan for free", "Nothing is different"], "Lenders see more risk, so they charge <b>more interest</b> or say no.")]


def one_credit_math(r):
    p = r.choice([5000, 8000, 10000, 12000, 15000, 20000])
    a, b = r.choice([(4, 9), (5, 10), (3, 8), (6, 12)])
    d = p * (b - a) // 100
    return mcq("Two friends each borrow $%s for a car for one year. One with good credit pays %d%% interest. One with poor credit pays %d%%. How much more interest does the person with poor credit pay?" % (comma(p), a, b),
               "$%s" % comma(d), ["$%s" % comma(p * b // 100), "$%d" % (b - a), "$%s" % comma(p * a // 100)],
               "%d%% of $%s = $%s and %d%% of $%s = $%s. The difference is <b>$%s</b>." % (b, comma(p), comma(p * b // 100), a, comma(p), comma(p * a // 100), comma(d)))


def one_credit(r):
    return facts(CREDIT)(r) if r.random() < 0.65 else one_credit_math(r)


COLLEGE = [("Which way to pay for college does <b>not</b> have to be paid back?", "A scholarship", ["A student loan", "A credit card", "A car loan"], "<b>Scholarships</b> and grants do not have to be repaid."),
           ("What is a grant?", "Money for college, often based on need, that does not have to be repaid", ["A loan with high interest", "A job on campus", "A savings account"], "A <b>grant</b> is gift aid, often based on financial need."),
           ("What is work-study?", "A part-time job that helps a student pay for college", ["A loan from a bank", "A free trip", "A test for college"], "<b>Work-study</b> lets students earn money while they study."),
           ("What must a student do with a student loan?", "Pay it back, usually with interest", ["Nothing; it is free", "Give it to the school", "Spend it only on food"], "A <b>loan</b> must be repaid with interest."),
           ("Why do families save for college early?", "Savings can grow with interest, so less needs to be borrowed", ["Colleges do not accept loans", "Savings are always tax-free", "It lowers the price of textbooks"], "Saving early means <b>less debt</b> later."),
           ("A scholarship is usually given for what?", "Good grades, talents or other achievements", ["Having a credit card", "Owning a car", "Missing payments"], "<b>Scholarships</b> reward achievements.")]


def one_college_math(r):
    cost = r.choice([12000, 15000, 18000, 22000, 25000])
    g, s, w = r.choice([2000, 3000, 4000]), r.choice([1500, 2500, 5000]), r.choice([2000, 3000])
    sav = r.choice([1000, 2000, 3000])
    need = cost - g - s - w - sav
    return mcq("One year of college costs $%s. Ana gets a $%s grant and a $%s scholarship, earns $%s in work-study and uses $%s of savings. How much must she borrow with a student loan?" % (comma(cost), comma(g), comma(s), comma(w), comma(sav)),
               "$%s" % comma(need), ["$%s" % comma(cost - g - s), "$%s" % comma(g + s + w + sav), "$%s" % comma(need + 2 * sav)],
               "$%s − $%s − $%s − $%s − $%s = <b>$%s</b>." % (comma(cost), comma(g), comma(s), comma(w), comma(sav), comma(need)))


def one_college(r):
    return facts(COLLEGE)(r) if r.random() < 0.5 else one_college_math(r)


JOBS = [("cashier", "high school diploma", 28000), ("electrician", "trade school", 58000), ("dental hygienist", "2-year degree", 76000),
        ("teacher", "4-year degree", 60000), ("engineer", "4-year degree", 92000), ("nurse practitioner", "graduate degree", 120000),
        ("welder", "trade school", 48000), ("accountant", "4-year degree", 75000), ("medical assistant", "certificate", 38000)]


def an(w):
    return ("an " if w[0] in "aeiou" else "a ") + w


def one_salary(r):
    a, b = r.sample(JOBS, 2)
    if a[2] == b[2]:
        return None
    hi, lo = (a, b) if a[2] > b[2] else (b, a)
    kind = r.choice(["year", "life", "diff"])
    yrs = r.choice([30, 35, 40])
    if kind == "year":
        return mcq("%s (%s) earns about $%s a year. %s (%s) earns about $%s a year. How much more does the %s earn in one year?" % (an(hi[0]).capitalize(), hi[1], comma(hi[2]), an(lo[0]).capitalize(), lo[1], comma(lo[2]), hi[0]),
                   "$%s" % comma(hi[2] - lo[2]), ["$%s" % comma(hi[2] + lo[2]), "$%s" % comma(hi[2]), "$%s" % comma((hi[2] - lo[2]) * 10)],
                   "$%s − $%s = <b>$%s</b>." % (comma(hi[2]), comma(lo[2]), comma(hi[2] - lo[2])))
    if kind == "life":
        return mcq("%s earns about $%s a year. About how much is that over a %d-year career?" % (an(hi[0]).capitalize(), comma(hi[2]), yrs), "$%s" % comma(hi[2] * yrs), ["$%s" % comma(hi[2] + yrs), "$%s" % comma(hi[2] * 10), "$%s" % comma(hi[2] * yrs * 10)],
                   "$%s × %d = <b>$%s</b>." % (comma(hi[2]), yrs, comma(hi[2] * yrs)))
    return mcq("Over a %d-year career, about how much more does %s ($%s a year) earn than %s ($%s a year)?" % (yrs, an(hi[0]), comma(hi[2]), an(lo[0]), comma(lo[2])),
               "$%s" % comma((hi[2] - lo[2]) * yrs), ["$%s" % comma(hi[2] - lo[2]), "$%s" % comma(hi[2] * yrs), "$%s" % comma((hi[2] + lo[2]) * yrs)],
               "($%s − $%s) × %d = $%s × %d = <b>$%s</b>." % (comma(hi[2]), comma(lo[2]), yrs, comma(hi[2] - lo[2]), yrs, comma((hi[2] - lo[2]) * yrs)))


def build():
    sets, R = build_sets([
        ("Checking accounts, debit cards and credit cards", [("collect", one_cards, 20)]),
        ("Balance a check register", [("collect", one_register, 20)]),
        ("Credit history and credit reports", [("collect", one_credit, 20)]),
        ("Ways to pay for college", [("collect", one_college, 20)]),
        ("Salaries and lifetime income", [("collect", one_salary, 20)]),
    ], 66025)
    finish(sets, R)
    body = lesson('<ul><li>A <b>checking account</b> and a <b>debit card</b> use your own money. Compare fees at different banks and credit unions.</li><li>A <b>credit card</b> is a loan. Unpaid balances are charged interest.</li><li>In a <b>check register</b>, add deposits and subtract payments, withdrawals and transfers out.</li><li>A <b>credit report</b> records borrowing and payments for years; a good history means lower interest.</li><li>Pay for college with savings, grants, scholarships, work-study and student loans. Only loans must be repaid.</li></ul>',
        [example("Balance $420. Check $135. Deposit $80.", ["$420 − $135 = $285", "$285 + $80"], "$365"), example("$92,000 vs $60,000 a year for 35 years", ["$32,000 × 35"], "$1,120,000")],
        [['Thinking a credit card is your own money', 'It is a loan; you must pay it back.'], ['Adding a withdrawal or transfer out', 'Money leaving the account is subtracted.'], ['Thinking a grant or scholarship must be repaid', 'Only loans are repaid.']])
    faq = [('What does TEKS 6.14 cover?', 'Checking accounts and debit cards, debit versus credit cards, check registers, credit history and credit reports, paying for college, and comparing salaries and lifetime income.'), ('How long does information stay on a credit report?', 'Most negative information stays about 7 years; a bankruptcy can stay up to 10 years.'), ('What is the difference between a grant and a loan?', 'A grant does not have to be paid back. A loan must be repaid, usually with interest.'), ('Why compare lifetime income?', 'Small yearly differences add up over a long career.')]
    make('personal-financial-literacy', 25, 'Personal Financial Literacy', '6.14A–6.14H',
         '6.14A compare the features and costs of a checking account and a debit card offered by different local financial institutions; 6.14B distinguish between debit cards and credit cards; 6.14C balance a check register that includes deposits, withdrawals, and transfers; 6.14D explain why it is important to establish a positive credit history; 6.14E describe the information in a credit report and how long it is retained; 6.14F describe the value of credit reports to borrowers and to lenders; 6.14G explain various methods to pay for college, including through savings, grants, scholarships, student loans, and work-study; 6.14H compare the annual salary of several occupations requiring various levels of post-secondary education or vocational training and calculate the effects of the different annual salaries on lifetime income',
         'Personal Financial Literacy: Accounts, Credit, College and Careers', 'Personal Financial Literacy',
         'Free Grade 6 personal financial literacy worksheets for Texas TEKS 6.14: checking accounts, debit and credit cards, check registers, credit reports, paying for college and lifetime income. 100 questions with answers.',
         'Debit spends your money; credit borrows it.', 'Register: add deposits, subtract payments. Good credit means lower interest.',
         body, faq, sets, seo_title='Grade 6 Personal Financial Literacy Worksheets: Credit, Check Registers and College (TEKS 6.14, STAAR)')


if __name__ == "__main__":
    build()
