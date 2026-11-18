# -*- coding: utf-8 -*-
"""
Texas Grade 4 Math: Personal Financial Literacy: Expenses, Profit, Saving and Banks (TEKS 4.10A–4.10E)
  python3 tools/gen_ustx_math_g4_financial_literacy.py
Fixed and variable expenses, calculating profit, savings options, sharing an allowance among spending, saving and
giving, and what financial institutions do. Each set mixes idea questions with money calculations.
Wrong answers come from real mistakes: calling a bill that changes every month a fixed expense, treating income as
profit, and thinking a bank only stores money.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)

tx_common.GRADE = "grade-4"

def facts(lst):
    def maker(r):
        q, a, w, e = r.choice(lst)
        w = list(w)
        r.shuffle(w)
        return mcq(q, a, w, e)
    return maker


EXP = [("Which is a fixed expense for a family?", "Rent of $1,200 every month", ["The grocery bill", "The electric bill", "Gas for the car"], "A fixed expense costs the same each time: <b>rent</b>."),
       ("Which is a variable expense?", "The water bill", ["A $15 monthly music plan", "Rent", "A car payment of $300 every month"], "The water bill changes with how much water you use, so it is <b>variable</b>."),
       ("What is a fixed expense?", "A cost that stays the same each time it is paid", ["A cost that changes every month", "Money you earn", "Money you save"], "<b>Fixed</b> means the amount stays the same."),
       ("What is a variable expense?", "A cost that can change from month to month", ["A cost that is always the same", "Money a bank lends you", "A gift"], "<b>Variable</b> means the amount can change."),
       ("The Lopez family's phone plan is $60 every month. What kind of expense is it?", "Fixed", ["Variable", "Profit", "Income"], "It is the same every month: <b>fixed</b>."),
       ("Which expense can a family most easily lower by making choices?", "Eating at restaurants", ["Rent", "A car loan payment", "Insurance with a set price"], "Variable expenses like <b>eating out</b> depend on choices.")]


def one_exp_math(r):
    k = Kid(r).next()
    rent, phone = r.choice([800, 900, 1000, 1200]), r.choice([40, 50, 60])
    food = [r.randint(300, 500) for _ in range(3)]
    return mcq("A family pays $%s rent and $%d for phones every month (fixed). Food cost $%d, $%d and $%d in three months (variable). What were the total fixed expenses for the three months?" % (comma(rent), phone, food[0], food[1], food[2]),
               "$%s" % comma(3 * (rent + phone)), ["$%s" % comma(rent + phone), "$%s" % comma(3 * (rent + phone) + sum(food)), "$%s" % comma(sum(food))],
               "Fixed expenses are the same each month: 3 × ($%s + $%d) = <b>$%s</b>." % (comma(rent), phone, comma(3 * (rent + phone))))


def one_exp(r):
    return facts(EXP)(r) if r.random() < 0.45 else one_exp_math(r)


def one_profit(r):
    k = Kid(r).next()
    kind = r.choice(["lemon", "cookies", "crafts", "idea"])
    if kind == "idea":
        return facts([("What is profit?", "The money left after you subtract the costs from the income", ["All the money you collect", "The money you spend on supplies", "Money you borrow"], "Profit = income − costs."),
                      ("A lemonade stand earns $40 and spends $12 on supplies. Which shows the profit?", "$40 − $12", ["$40 + $12", "$40 × $12", "$12 − $40"], "Profit = income − costs: <b>$40 − $12</b>."),
                      ("If costs are greater than income, what happens?", "There is no profit; the business loses money", ["The profit is very large", "The costs disappear", "The income doubles"], "Income − costs is less than 0: the business <b>loses money</b>.")])(r)
    if kind == "lemon":
        n, p, cost = r.randint(20, 60), r.choice([1, 2]), r.randint(10, 30)
        inc = n * p
        if inc <= cost:
            return None
        return mcq("%s sells %d cups of lemonade for $%d each. Supplies cost $%d. What is the profit?" % (k["n"], n, p, cost), "$%d" % (inc - cost), ["$%d" % inc, "$%d" % (inc + cost), "$%d" % (n - cost if n > cost else n + cost)], "Income: %d × $%d = $%d. Profit: $%d − $%d = <b>$%d</b>." % (n, p, inc, inc, cost, inc - cost))
    if kind == "cookies":
        n, p, cost = r.randint(3, 9) * 12, 1, r.randint(15, 40)
        return mcq("A class bakes %d cookies and sells each for $1. Ingredients cost $%d. What is the profit?" % (n, cost), "$%d" % (n - cost), ["$%d" % n, "$%d" % (n + cost), "$%d" % cost], "$%d − $%d = <b>$%d</b>." % (n, cost, n - cost))
    n, p, c = r.randint(5, 15), r.randint(6, 12), r.randint(2, 5)
    return mcq("%s makes %d bracelets. Each costs $%d to make and sells for $%d. What is the profit if all are sold?" % (k["n"], n, c, p), "$%d" % (n * (p - c)), ["$%d" % (n * p), "$%d" % (n * c), "$%d" % (p - c)],
               "Income $%d − costs $%d = <b>$%d</b>." % (n * p, n * c, n * (p - c)))


SAVE = [("Which savings option keeps money safe and pays interest?", "A savings account at a bank", ["A piggy bank", "A shoebox under the bed", "Your pocket"], "A <b>savings account</b> is safe and can earn interest."),
        ("What is one advantage of a piggy bank?", "You can get your money quickly at home", ["It pays interest", "It is insured by the government", "It makes your money grow"], "A piggy bank is <b>easy to reach</b>, but it earns no interest."),
        ("What is one disadvantage of keeping savings in a piggy bank?", "It does not earn interest and could be lost", ["It pays too much interest", "You cannot put coins in it", "The bank charges a fee"], "Money at home <b>earns no interest and could be lost</b>."),
        ("Why might someone choose a savings account over a checking account for a long-term goal?", "Savings accounts usually pay more interest", ["Checking accounts cannot hold money", "Savings accounts are for spending every day", "Banks do not allow checking accounts"], "<b>Savings accounts usually pay more interest</b>, which helps long-term goals.")]


def one_save(r):
    if r.random() < 0.4:
        return facts(SAVE)(r)
    k = Kid(r).next()
    a = r.choice([100, 200, 300, 400, 500])
    i = r.choice([2, 3, 4, 5])
    yrs = r.randint(2, 4)
    return mcq("%s puts $%d in a savings account. The bank pays $%d interest each year. If %s takes nothing out, how much will be in the account after %d years?" % (k["n"], a, i, k["he"], yrs), "$%d" % (a + i * yrs),
               ["$%d" % (a + i), "$%d" % (a * i), "$%d" % (a + i * (yrs + 1))], "$%d + %d × $%d = <b>$%d</b>." % (a, yrs, i, a + i * yrs))


def one_allow(r):
    k = Kid(r).next()
    a = r.choice([10, 12, 15, 20, 25])
    kind = r.choice(["save", "share", "spend", "idea"])
    s, g = r.randint(2, a // 2), r.randint(1, 3)
    sp = a - s - g
    if kind == "idea":
        return facts([("Which shows a balanced plan for a $10 weekly allowance?", "Spend $5, save $3, share $2", ["Spend $10, save $0, share $0", "Spend $12, save $0, share $0", "Save $0, share $10, spend $0"], "A plan splits money among <b>spending, saving and sharing</b>."),
                      ("Why might a student save part of an allowance for college?", "College costs a lot, so saving a little each week adds up", ["College is free", "Saving makes prices go down", "Banks pay for college"], "Small amounts <b>add up over time</b>."),
                      ("What does sharing mean in an allowance plan?", "Giving some money to help others, like a food bank", ["Spending on yourself", "Putting money in savings", "Borrowing from a friend"], "Sharing is <b>giving to help others</b>.")])(r)
    if kind == "save":
        w = r.randint(4, 10)
        return mcq("%s gets $%d a week and saves $%d of it for college. How much does %s save in %d weeks?" % (k["n"], a, s, k["he"], w), "$%d" % (s * w), ["$%d" % (a * w), "$%d" % (s + w), "$%d" % ((a - s) * w)], "%d × $%d = <b>$%d</b>." % (w, s, s * w))
    if kind == "share":
        return mcq("%s gets $%d a week. %s saves $%d and spends $%d. How much is left to share?" % (k["n"], a, k["He"], s, sp), "$%d" % g, ["$%d" % (s + sp), "$%d" % (a - s), "$%d" % (a - sp)], "$%d − $%d − $%d = <b>$%d</b>." % (a, s, sp, g))
    return mcq("%s gets $%d a week. %s saves $%d and gives $%d to charity. How much can %s spend?" % (k["n"], a, k["He"], s, g, k["he"]), "$%d" % sp, ["$%d" % (a - s), "$%d" % (a - g), "$%d" % (s + g)], "$%d − $%d − $%d = <b>$%d</b>." % (a, s, g, sp))


BANK = [("What is one basic purpose of a bank?", "To keep money safe", ["To set prices in stores", "To print money for families", "To pay students allowances"], "Banks <b>keep money safe</b>."),
        ("How does a bank help people buy a house?", "It lends money that is paid back with interest", ["It gives houses away", "It builds the houses", "It pays the rent"], "Banks <b>lend</b> money, and borrowers pay it back with interest."),
        ("Where does the money a bank lends come from?", "Partly from money people keep in their accounts", ["It is printed at the bank", "From the store", "From nowhere"], "Banks lend some of the money people <b>deposit</b>."),
        ("What is a deposit?", "Putting money into a bank account", ["Taking money out of an account", "Borrowing money", "Paying a bill"], "A <b>deposit</b> puts money into an account."),
        ("What is a withdrawal?", "Taking money out of a bank account", ["Putting money into an account", "Earning interest", "Paying back a loan"], "A <b>withdrawal</b> takes money out."),
        ("Why does a bank pay interest on savings?", "Because it uses the money to make loans", ["Because it has to give money away", "Because savings are free", "Because people never take money out"], "The bank pays interest because it <b>uses deposits to make loans</b>."),
        ("Which is a financial institution?", "A credit union", ["A grocery store", "A school", "A library"], "A <b>credit union</b>, like a bank, keeps money, lends and borrows."),
        ("Why do people borrow money from a bank?", "To buy something big now and pay for it over time", ["Because borrowed money is free", "To avoid paying interest", "To get a gift"], "Loans help people <b>pay for big things over time</b>, with interest.")]


def one_bank(r):
    if r.random() < 0.5:
        return facts(BANK)(r)
    k = Kid(r).next()
    b = r.choice([100, 200, 300, 500])
    d, w = r.choice([20, 25, 40, 50]), r.choice([10, 15, 30, 35])
    return mcq("%s has $%d in a bank account. %s deposits $%d and then withdraws $%d. How much is in the account now?" % (k["n"], b, k["He"], d, w), "$%d" % (b + d - w), ["$%d" % (b + d + w), "$%d" % (b - d + w), "$%d" % (b + d)],
               "Deposit adds, withdrawal subtracts: $%d + $%d − $%d = <b>$%d</b>." % (b, d, w, b + d - w))


def build():
    sets, R = build_sets([
        ("Fixed and variable expenses", [("collect", one_exp, 20)]),
        ("Calculate profit", [("collect", one_profit, 20)]),
        ("Savings options", [("collect", one_save, 20)]),
        ("Spending, saving and sharing an allowance", [("collect", one_allow, 20)]),
        ("What banks and other financial institutions do", [("collect", one_bank, 20)]),
    ], 64024)
    finish(sets, R)
    body = lesson('<ul><li>A <b>fixed expense</b> costs the same each time (rent). A <b>variable expense</b> can change (groceries, electricity).</li><li><b>Profit</b> = income − costs.</li><li>Savings can be kept at home or in a bank. A savings account is safer and can earn interest.</li><li>A good allowance plan splits money among <b>spending, saving</b> (including for college) and <b>sharing</b>.</li><li>Banks and credit unions keep money safe, lend money and borrow money from depositors.</li></ul>',
        [example("A bake sale earns $85. Supplies cost $27. What is the profit?", ["$85 − $27"], "$58"), example("Lena gets $12 a week. She saves $4 and gives $2. How much can she spend?", ["$12 − $4 − $2"], "$6")],
        [['Calling a bill that changes a fixed expense', 'Fixed means the same amount every time.'], ['Treating all income as profit', 'Subtract the costs first.'], ['Thinking a bank only stores money', 'Banks also lend money and pay interest.']])
    faq = [('What does TEKS 4.10A ask?', 'Distinguish between fixed and variable expenses.'), ('What does TEKS 4.10B ask?', 'Calculate profit in a given situation: income minus costs.'), ('What do TEKS 4.10C and 4.10D ask?', 'Compare the advantages and disadvantages of savings options, and describe how to divide a weekly allowance among spending, saving (including for college) and sharing.'), ('What does TEKS 4.10E ask?', 'Describe the basic purpose of financial institutions, including keeping money safe, borrowing money and lending.')]
    make('personal-financial-literacy', 24, 'Personal Financial Literacy', '4.10A–4.10E',
         '4.10A distinguish between fixed and variable expenses; 4.10B calculate profit in a given situation; 4.10C compare the advantages and disadvantages of various savings options; 4.10D describe how to allocate a weekly allowance among spending; saving, including for college; and sharing; 4.10E describe the basic purpose of financial institutions, including keeping money safe, borrowing money, and lending',
         'Personal Financial Literacy: Expenses, Profit, Saving and Banks', 'Personal Financial Literacy',
         'Free Grade 4 personal financial literacy worksheets for Texas TEKS 4.10: fixed and variable expenses, profit, savings options, allowance plans and what banks do. 100 questions with answers.',
         'Profit = income − costs.', 'Fixed expenses stay the same; variable expenses change. Split an allowance among spending, saving and sharing.',
         body, faq, sets, seo_title='Grade 4 Personal Financial Literacy Worksheets (TEKS 4.10, Texas)')


if __name__ == "__main__":
    build()
