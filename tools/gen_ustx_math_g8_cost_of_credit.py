# -*- coding: utf-8 -*-
"""
Texas Grade 8 Math: The Cost of Credit: Interest Rates and Loan Length (TEKS 8.12A, 8.12B)
  python3 tools/gen_ustx_math_g8_cost_of_credit.py
Total cost of a loan with simple interest, how the interest rate and loan length change the cost, monthly payments,
credit cards and easy-access (payday) loans.
Wrong answers come from real mistakes: forgetting to add the principal, using one year instead of the whole loan
length, and thinking a small fee is a small rate.
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


def one_total(r):
    p = r.choice([1000, 2000, 3000, 5000, 8000, 10000, 12000, 15000])
    rate = r.choice([3, 4, 5, 6, 8, 10, 12])
    t = r.choice([2, 3, 4, 5])
    i = p * rate * t / 100.0
    item = r.choice(["a used car", "a laptop and printer", "new tires and a repair", "a motorcycle", "furniture"])
    if r.random() < 0.5:
        return mcq("A loan of %s for %s has %d%% simple interest per year for %d years. How much interest is paid?" % (md(p), item, rate, t), md(i), [md(p * rate / 100.0), md(p + i), md(i * 10)],
                   "I = Prt = %s × %s × %d = <b>%s</b>." % (md(p), pc(rate / 100.0), t, md(i)))
    return mcq("A loan of %s for %s has %d%% simple interest per year for %d years. What is the total cost of repaying the loan?" % (md(p), item, rate, t), md(p + i), [md(i), md(p + p * rate / 100.0), md(p * (1 + rate / 100.0) * t)],
               "Interest = %s × %s × %d = %s. Total = %s + %s = <b>%s</b>." % (md(p), pc(rate / 100.0), t, md(i), md(p), md(i), md(p + i)))


def one_compare(r):
    p = r.choice([5000, 10000, 15000, 20000])
    kind = r.choice(["rate", "length"])
    if kind == "rate":
        a, b = sorted(r.sample([3, 4, 5, 6, 7, 8, 9], 2))
        t = r.choice([3, 4, 5])
        d = p * (b - a) * t / 100.0
        return mcq("Two banks offer a %s loan for %d years with simple interest. Bank A charges %d%% a year and Bank B charges %d%% a year. How much more does Bank B's loan cost?" % (md(p), t, a, b), md(d),
                   [md(p * (b - a) / 100.0), md(p * b * t / 100.0), md(b - a)], "%d%% − %d%% = %d%%. %s × %s × %d = <b>%s</b> more." % (b, a, b - a, md(p), pc((b - a) / 100.0), t, md(d)))
    rate = r.choice([4, 5, 6, 8])
    a, b = sorted(r.sample([2, 3, 4, 5, 6], 2))
    d = p * rate * (b - a) / 100.0
    return mcq("A %s loan has %d%% simple interest per year. How much more interest is paid on a %d-year loan than on a %d-year loan?" % (md(p), rate, b, a), md(d), [md(p * rate / 100.0), md(p * rate * b / 100.0), md(d * 2)],
               "Extra years: %d. %s × %s × %d = <b>%s</b>. Longer loans cost more interest." % (b - a, md(p), pc(rate / 100.0), b - a, md(d)))


def one_payment(r):
    p = r.choice([1200, 2400, 3600, 4800, 6000])
    rate = r.choice([5, 10, 15])
    t = r.choice([1, 2, 3])
    tot = p * (1 + rate * t / 100.0)
    months = 12 * t
    return mcq("Sara borrows %s at %d%% simple interest per year for %d year%s. She pays it back in equal monthly payments. What is each payment?" % (md(p), rate, t, "" if t == 1 else "s"), m(tot / months),
               [m(p / months), m(tot / t), m(tot / 12 / (t + 1))], "Total = %s × (1 + %s × %d) = %s. %s ÷ %d months = <b>%s</b>." % (md(p), pc(rate / 100.0), t, md(tot), md(tot), months, m(tot / months)))


def one_card(r):
    kind = r.choice(["payday", "card", "card", "fee"])
    if kind == "payday":
        loan = r.choice([200, 300, 400, 500])
        fee = loan * r.choice([10, 15, 20]) // 100
        return mcq("An easy-access (payday) loan of %s costs a %s fee for 2 weeks. If it is renewed for 6 weeks in all (3 times), what is the total in fees?" % (md(loan), md(fee)), md(3 * fee), [md(fee), md(loan + fee), md(6 * fee)],
                   "%s × 3 = <b>%s</b> in fees, and the %s is still owed. Easy-access loans are very expensive." % (md(fee), md(3 * fee), md(loan)))
    if kind == "fee":
        bal, rate = r.choice([500, 800, 1000, 1500, 2000]), r.choice([18, 20, 24])
        mo = bal * rate / 100.0 / 12
        return mcq("A credit card has a %s balance and an interest rate of %d%% a year (%s%% a month). About how much interest is charged for one month if nothing is paid?" % (md(bal), rate, pc(rate / 12.0)), m(mo), [m(bal * rate / 100.0), m(bal * 0.01), m(mo * 2)],
                   "%s × %s%% = <b>%s</b> in one month." % (md(bal), pc(rate / 12.0), m(mo)))
    bal = r.choice([600, 900, 1200, 1500])
    pay = r.choice([50, 75, 100])
    return mcq("A %s credit card balance has no interest (to keep it simple). How many months does it take to pay it off with %s a month?" % (md(bal), md(pay)), str(-(-bal // pay)), [str(bal // pay + 2), str(bal // 12), str(pay)],
               "%s ÷ %s = <b>%d months</b>. With real interest it takes even longer." % (md(bal), md(pay), -(-bal // pay)))


def build():
    sets, R = build_sets([
        ("Simple interest on a loan", [("collect", one_total, 20)]),
        ("Interest rate and loan length", [("collect", one_compare, 20)]),
        ("Monthly payments", [("collect", one_payment, 20)]),
        ("Credit cards and easy-access loans", [("collect", one_card, 20)]),
        ("Mixed loan problems", [("collect", one_compare, 10), ("collect", one_total, 10)]),
    ], 68021)
    finish(sets, R)
    body = lesson('<ul><li>The <b>cost of credit</b> is the interest and fees you pay to borrow money.</li><li>Simple interest: I = Prt. Total to repay = P + I.</li><li>A higher interest rate or a <b>longer loan</b> means more interest.</li><li>Credit card balances and easy-access (payday) loans can cost a lot when they are not paid off quickly.</li></ul>',
        [example("$5,000 at 6% for 4 years", ["I = 5,000 × 0.06 × 4 = 1,200"], "total $6,200")],
        [['Forgetting to add the principal', 'Total cost = principal + interest.'], ['Using only one year', 'Multiply by the number of years in the loan.'], ['Thinking a small fee is a small rate', 'A $45 fee on $300 for 2 weeks is a very high rate.']])
    faq = [('What does TEKS 8.12A ask?', 'Solve real-world problems comparing how interest rate and loan length affect the cost of credit.'), ('What does TEKS 8.12B ask?', 'Calculate the total cost of repaying a loan, including credit cards and easy access loans, under various rates of interest and over different periods using an online calculator.'), ('Why does a longer loan cost more?', 'Interest is charged for every year you owe money.'), ('Do real loans use simple interest?', 'Many use compound interest; online calculators handle it. Simple interest shows the idea.')]
    make('cost-of-credit-and-loans', 21, 'Personal Financial Literacy', '8.12A, 8.12B',
         '8.12A solve real-world problems comparing how interest rate and loan length affect the cost of credit; 8.12B calculate the total cost of repaying a loan, including credit cards and easy access loans, under various rates of interest and over different periods using an online calculator',
         'The Cost of Credit: Interest Rates and Loan Length', 'Cost of Credit and Loans',
         'Free Grade 8 personal financial literacy worksheets for Texas TEKS 8.12A and 8.12B: the cost of credit, interest rates, loan length, monthly payments, credit cards and payday loans. 100 questions with answers.',
         'Total cost = principal + interest. Higher rate or longer loan costs more.', '$5,000 at 6% for 4 years: $1,200 interest.',
         body, faq, sets, seo_title='Grade 8 Cost of Credit and Loans Worksheets (TEKS 8.12A, 8.12B, STAAR)')


if __name__ == "__main__":
    build()
