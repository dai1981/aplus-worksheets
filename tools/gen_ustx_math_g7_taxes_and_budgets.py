# -*- coding: utf-8 -*-
"""
Texas Grade 7 Math: Sales Tax, Income Tax and Personal Budgets (TEKS 7.13A, 7.13B, 7.13D)
  python3 tools/gen_ustx_math_g7_taxes_and_budgets.py
Calculating sales tax and income tax, the parts of a personal budget, finding what percent each budget category is,
and using a family budget to find the hourly wage needed.
Wrong answers come from real mistakes: forgetting to add the tax to the price, using the wrong total for a budget
percent, and dividing a yearly budget by 12 instead of by the hours worked.
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


def one_sales(r):
    rate = r.choice([6.25, 8.25, 8, 7.5])
    price = r.choice([12, 16, 20, 24, 36, 40, 48, 60, 80, 120, 200, 240])
    tax = price * rate / 100
    item = r.choice(["a pair of boots", "a backpack", "a video game", "a bike helmet", "a jacket", "a pair of jeans", "a phone case"])
    where = "Texas" if rate == 6.25 else "Houston" if rate == 8.25 else "a Texas town"
    note = " (the state rate)" if rate == 6.25 else ""
    if r.random() < 0.5:
        return mcq("The sales tax in %s is %g%%%s. What is the tax on %s that costs %s?" % (where, rate, note, item, md(price)), m(tax), [m(tax * 10), m(price + tax), m(price * rate / 1000)],
                   "%g%% of %s = %s × %s = <b>%s</b>." % (rate, md(price), ("%.4f" % (rate / 100)).rstrip("0"), md(price), m(tax)))
    return mcq("%s costs %s. The sales tax rate is %g%%. What is the total cost?" % (item[0].upper() + item[1:], md(price), rate), m(price + tax), [m(tax), m(price + rate), m(price - tax)],
               "Tax: %s × %s = %s. Total: %s + %s = <b>%s</b>." % (md(price), ("%.4f" % (rate / 100)).rstrip("0"), m(tax), md(price), m(tax), m(price + tax)))


def one_income(r):
    k = Kid(r).next()
    kind = r.choice(["flat", "flat", "after", "month"])
    pay = r.choice([24000, 30000, 36000, 42000, 48000, 52000, 60000])
    rate = r.choice([10, 12, 15])
    tax = pay * rate // 100
    job = r.choice(["mechanic", "teacher", "nurse", "chef", "electrician", "bus driver"])
    if kind == "flat":
        return mcq("A %s earns %s a year. Suppose the federal income tax is %d%% of that income. How much income tax is that?" % (job, md(pay), rate), md(tax), [md(pay - tax), md(tax * 10), md(pay * rate // 1000)],
                   "%d%% of %s = <b>%s</b>. (Texas has no state income tax.)" % (rate, md(pay), md(tax)))
    if kind == "after":
        return mcq("%s's aunt earns %s a year and pays %d%% in income tax. How much does she keep after income tax?" % (k["n"], md(pay), rate), md(pay - tax), [md(tax), md(pay + tax), md(pay - rate)],
                   "Tax: %s. %s − %s = <b>%s</b>." % (md(tax), md(pay), md(tax), md(pay - tax)))
    mo = r.choice([2500, 3000, 3500, 4000, 4500])
    return mcq("A worker earns %s a month. Suppose %d%% is withheld for federal income tax. How much is withheld each month?" % (md(mo), rate), md(mo * rate // 100), [md(mo * rate // 100 * 12), md(mo - mo * rate // 100), md(mo * rate // 1000)],
               "%d%% of %s = <b>%s</b>." % (rate, md(mo), md(mo * rate // 100)))


PARTS = [("Which is a <b>fixed</b> expense?", "Rent", ["Movie tickets", "Eating out", "Gifts"], "A <b>fixed expense</b> is the same every month, like rent."),
         ("Which is a <b>variable</b> expense?", "Groceries", ["Rent", "Car payment", "Insurance"], "A <b>variable expense</b> changes from month to month, like groceries."),
         ("Which is planned savings in a budget?", "Money set aside each month for emergencies", ["A movie ticket", "A credit card purchase", "A late fee"], "Budgets plan <b>savings</b> for emergencies, college and retirement."),
         ("Why does a budget include an emergency fund?", "To pay for unexpected costs, like a car repair", ["To buy more video games", "To pay higher taxes", "To avoid saving"], "An <b>emergency fund</b> covers surprises without borrowing."),
         ("Which is part of income in a personal budget?", "Wages from a job", ["Rent", "Groceries", "Gas"], "<b>Income</b> is money coming in, like wages."),
         ("Which is usually a fixed expense?", "A monthly phone plan", ["Gas for the car", "Clothes", "Concert tickets"], "A phone plan costs the same each month: <b>fixed</b>."),
         ("Why do people save for retirement?", "To have money when they stop working", ["To pay this month's rent", "To lower sales tax", "Because it is required for school"], "<b>Retirement savings</b> pay for life after work."),
         ("Taxes taken from a paycheck are part of which budget item?", "Taxes", ["Variable expenses", "Planned savings", "Entertainment"], "Payroll and income <b>taxes</b> are a budget category.")]


def one_parts(r):
    return facts(PARTS)(r)


def one_pct(r):
    inc = r.choice([2000, 2500, 3000, 4000, 5000])
    cats = ["Housing", "Food", "Transportation", "Savings", "Taxes", "Other"]
    pcts = r.choice([[30, 15, 10, 10, 20, 15], [25, 15, 15, 10, 15, 20], [35, 10, 10, 15, 15, 15], [30, 20, 10, 5, 15, 20], [40, 15, 10, 10, 10, 15]])
    vals = [inc * p // 100 for p in pcts]
    rows = "".join("<tr><td>%s</td><td>%s</td></tr>" % (c, md(v)) for c, v in zip(cats, vals))
    pic = "<div class='qfig'><div class='sn-tw'><table class='sn-table'><thead><tr><th>Category</th><th>Monthly amount</th></tr></thead><tbody>%s<tr><td><b>Total</b></td><td><b>%s</b></td></tr></tbody></table></div></div>" % (rows, md(inc))
    i = r.randrange(6)
    if r.random() < 0.7:
        return mcq(pic + "What percent of the budget is %s?" % cats[i].lower(), "%d%%" % pcts[i], ["%d%%" % (vals[i] // 10) if vals[i] // 10 != pcts[i] else "%d%%" % (pcts[i] + 5), "%d%%" % (100 - pcts[i]), "%d%%" % (pcts[i] + 10)],
                   "%s ÷ %s = %s = <b>%d%%</b>." % (md(vals[i]), md(inc), ("%.2f" % (pcts[i] / 100.0)).rstrip("0"), pcts[i]))
    j = r.choice([t for t in range(6) if t != i])
    return mcq(pic + "What percent of the budget is %s and %s together?" % (cats[i].lower(), cats[j].lower()), "%d%%" % (pcts[i] + pcts[j]), ["%d%%" % pcts[i], "%d%%" % (100 - pcts[i] - pcts[j]), "%d%%" % ((vals[i] + vals[j]) // 10) if (vals[i] + vals[j]) // 10 != pcts[i] + pcts[j] else "%d%%" % (pcts[i] + pcts[j] + 5)],
               "(%s + %s) ÷ %s = <b>%d%%</b>." % (md(vals[i]), md(vals[j]), md(inc), pcts[i] + pcts[j]))


def one_wage(r):
    kind = r.choice(["yearly", "monthly", "two"])
    hourly = r.choice([15, 18, 20, 22, 24, 25, 28, 30])
    if kind == "yearly":
        y = hourly * 2080
        return mcq("A family budget estimator says a family needs %s a year to meet basic needs. A full-time worker works 2,080 hours a year. What hourly wage is needed?" % md(y), "%s an hour" % md(hourly), ["%s an hour" % md(y / 12), "%s an hour" % md(y / 52), "%s an hour" % md(hourly * 2)],
                   "%s ÷ 2,080 = <b>%s an hour</b>." % (md(y), md(hourly)))
    if kind == "monthly":
        mo = hourly * 2080 // 12
        if hourly * 2080 % 12:
            return None
        return mcq("A minimum household budget is %s a month. How much is that for a year?" % md(mo), md(mo * 12), [md(mo * 52), md(mo * 10), md(mo + 12)],
                   "%s × 12 = <b>%s</b>." % (md(mo), md(mo * 12)))
    y = hourly * 2 * 2080
    return mcq("A family needs %s a year. Two adults each work full time (2,080 hours a year) at the same wage. What hourly wage does each need?" % md(y), "%s an hour" % md(hourly), ["%s an hour" % md(hourly * 2), "%s an hour" % md(y / 2080 / 4), "%s an hour" % md(y / 12 / 2)],
               "Each earns half: %s ÷ 2 = %s. %s ÷ 2,080 = <b>%s an hour</b>." % (md(y), md(y / 2), md(y / 2), md(hourly)))


def build():
    sets, R = build_sets([
        ("Sales tax", [("collect", one_sales, 20)]),
        ("Income tax", [("collect", one_income, 20)]),
        ("Parts of a personal budget", [("collect", one_parts, 8), ("collect", one_pct, 12)]),
        ("What percent is each category?", [("collect", one_pct, 20)]),
        ("Family budgets and the hourly wage needed", [("collect", one_wage, 20)]),
    ], 67024)
    finish(sets, R)
    body = lesson('<ul><li><b>Sales tax</b> is a percent of the price, added at the register. The Texas state rate is 6.25%; cities can add up to 2% more.</li><li><b>Income tax</b> is a percent of the money you earn. Texas has no state income tax, but there is federal income tax.</li><li>A <b>budget</b> lists income, taxes, planned savings (college, retirement, emergencies) and fixed and variable expenses.</li><li>Category percent = category amount ÷ total budget.</li></ul>',
        [example("$40 jeans, 8.25% tax", ["0.0825 × 40 = $3.30", "$40 + $3.30"], "$43.30"), example("$41,600 a year needed", ["41,600 ÷ 2,080"], "$20 an hour")],
        [['Forgetting to add the tax', 'Total = price + tax.'], ['Using the wrong total for a budget percent', 'Divide by the total budget, not another category.'], ['Dividing a yearly amount by 12 for an hourly wage', 'Full time is about 2,080 hours a year: divide by 2,080.']])
    faq = [('What does TEKS 7.13A ask?', 'Calculate the sales tax for a given purchase and calculate income tax for earned wages.'), ('What does TEKS 7.13B ask?', 'Identify the components of a personal budget, including income; planned savings for college, retirement and emergencies; taxes; and fixed and variable expenses, and calculate what percentage each category comprises of the total budget.'), ('What does TEKS 7.13D ask?', "Use a family budget estimator to determine the minimum household budget and average hourly wage needed for a family to meet its basic needs in the student's city or another large city nearby."), ('Why 2,080 hours?', '40 hours a week × 52 weeks = 2,080 hours.')]
    make('sales-tax-income-tax-and-budgets', 24, 'Personal Financial Literacy', '7.13A, 7.13B, 7.13D',
         "7.13A calculate the sales tax for a given purchase and calculate income tax for earned wages; 7.13B identify the components of a personal budget, including income; planned savings for college, retirement, and emergencies; taxes; and fixed and variable expenses, and calculate what percentage each category comprises of the total budget; 7.13D use a family budget estimator to determine the minimum household budget and average hourly wage needed for a family to meet its basic needs in the student's city or another large city nearby",
         'Sales Tax, Income Tax and Personal Budgets', 'Sales Tax, Income Tax and Budgets',
         'Free Grade 7 personal financial literacy worksheets for Texas TEKS 7.13A, 7.13B and 7.13D: sales tax, income tax, parts of a budget, budget percents and the hourly wage a family needs. 100 questions with answers.',
         'Tax = rate × amount. Budget percent = category ÷ total.', '$40 with 8.25% tax costs $43.30. $41,600 a year ÷ 2,080 = $20 an hour.',
         body, faq, sets, seo_title='Grade 7 Sales Tax, Income Tax and Budget Worksheets (TEKS 7.13, STAAR)')


if __name__ == "__main__":
    build()
