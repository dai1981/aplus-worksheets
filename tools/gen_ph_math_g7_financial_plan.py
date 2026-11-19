# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Budgets and Financial Plans (Grade 7: Number and Algebra)
  python3 tools/gen_ph_math_g7_financial_plan.py
Planning an allowance with percentages, saving for a goal, a family's monthly budget, the percent of income saved,
and needs and wants (own makers with pesos).
Wrong answers come from real mistakes: answering with the amount spent instead of the amount left, dividing the
wrong way, and treating wants as needs.
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

PARTS = [("food", 40), ("transportation", 15), ("school supplies", 10), ("savings", 20), ("load and internet", 10), ("others", 5)]


def one_part(r):
    k = Kid(r).next()
    w = r.choice([500, 600, 800, 1000, 1200, 1500, 2000])
    part, p = r.choice(PARTS)
    p = r.choice([p, p + 5, max(5, p - 5)])
    amt = F(w * p, 100)
    if amt.denominator != 1:
        raise AssertionError
    q = "%s gets a weekly allowance of %s. %s plans to spend %d%% on %s. How much is that?" % (k["n"], peso(w), k["He"], p, part)
    return mcq(q, peso(amt), [peso(x) for x in (w - amt, F(w, p) if F(w, p).denominator == 1 else amt + 10, amt * 10)], "%d%% of %s = <b>%s</b>." % (p, peso(w), peso(amt)))


def one_save(r):
    k = Kid(r).next()
    goal = r.choice([1500, 1800, 2400, 3000, 3600, 4500, 6000])
    per = r.choice([d for d in (100, 150, 200, 250, 300, 400, 500) if goal % d == 0])
    if r.random() < 0.5:
        q = "%s wants to buy a pair of rubber shoes for %s. %s saves %s every week. How many weeks will it take?" % (k["n"], peso(goal), k["He"], peso(per))
        n = goal // per
        return mcq(q, "%d weeks" % n, ["%d weeks" % x for x in (n + 1, n - 1, goal // 100)], "%s ÷ %s = <b>%d weeks</b>." % (peso(goal), peso(per), n))
    have = r.randrange(0, goal // 2, 100)
    weeks = r.choice([4, 5, 6, 8, 10, 12])
    need = goal - have
    if need % weeks:
        raise AssertionError
    q = "%s has saved %s and wants %s for a gadget in %d weeks. How much must %s save each week?" % (k["n"], peso(have), peso(goal), weeks, k["he"])
    return mcq(q, peso(need // weeks), [peso(x) for x in (goal // weeks, need // weeks + 50, (goal + have) // weeks)], "Still needed: %s − %s = %s. %s ÷ %d = <b>%s</b> a week." % (peso(goal), peso(have), peso(need), peso(need), weeks, peso(need // weeks)))


def one_bal(r):
    inc = r.choice([18000, 20000, 25000, 30000, 35000, 40000])
    rent = r.randrange(4000, 9000, 500)
    food = r.randrange(6000, 12000, 500)
    util = r.randrange(1500, 4000, 100)
    trans = r.randrange(1000, 3000, 100)
    exp = rent + food + util + trans
    if exp >= inc:
        raise AssertionError
    left = inc - exp
    q = "A family earns %s a month. They spend %s on rent, %s on food, %s on electricity and water, and %s on transportation. How much is left for savings?" % tuple(peso(x) for x in (inc, rent, food, util, trans))
    return mcq(q, peso(left), [peso(x) for x in (exp, left + util, inc - rent - food)], "Expenses: %s. Left: %s − %s = <b>%s</b>." % (peso(exp), peso(inc), peso(exp), peso(left)))


def one_pct(r):
    inc = r.choice([15000, 20000, 25000, 30000, 40000])
    s = r.randrange(1500, inc // 4, 500)
    p = F(s * 100, inc)
    if p.denominator != 1:
        raise AssertionError
    q = "Ana earns %s a month and saves %s. What percent of her income does she save?" % (peso(inc), peso(s))
    return mcq(q, "%d%%" % p, ["%g%%" % float(x) for x in (F(s, 100), F(inc, s)) if x.denominator <= 4] + ["%d%%" % (p + 5), "%d%%" % (100 - p)],
               "%s ÷ %s × 100 = <b>%d%%</b>." % (comma(s), comma(inc), p))


NW = [("Which is a <b>need</b>?", ["rice and food for the family", "electricity bill", "school fees", "medicine"], ["a new gaming console", "a second pair of designer shoes", "milk tea every day", "concert tickets"]),
      ("Which is a <b>want</b>?", ["milk tea every day", "a new gaming console", "concert tickets", "a branded bag"], ["rent", "rice", "water bill", "transportation to school"])]


def one_nw(r):
    q, good, bad = r.choice(NW)
    g = r.choice(good)
    return mcq(q, g, r.sample(bad, 3), "Needs are things we must have to live and study; wants are nice to have. A good financial plan pays for needs first. Answer: <b>%s</b>." % g)


def build():
    sets, R = build_sets([
        ("Plan an allowance", [("collect", uniq(one_part), 20)]),
        ("Saving for a goal", [("collect", uniq(one_save), 20)]),
        ("A family budget", [("collect", uniq(one_bal), 20)]),
        ("Percent of income saved", [("collect", uniq(one_pct), 20)]),
        ("Needs, wants and plans", [("collect", one_nw, 8), ("collect", uniq(one_save), 6), ("collect", uniq(one_part), 6)]),
    ], 70706)
    finish(sets, R)
    body = lesson('<ul><li>A <b>financial plan</b> (budget) shows the money that comes in (income) and how it will be used (expenses and savings).</li><li>Income − expenses = money left for savings.</li><li>Use percentages to plan: 20% of a ₱1,000 allowance for savings is ₱200.</li><li>Pay for <b>needs</b> (food, rent, school) before <b>wants</b>. Set a savings goal and a time: goal ÷ weeks = amount to save each week.</li></ul>',
        [example("Save for a ₱2,400 item in 8 weeks", ["2,400 ÷ 8"], "₱300 a week")],
        [['Spent instead of left', 'Subtract the expenses from the income.'], ['Dividing the wrong way', 'Goal ÷ amount per week = number of weeks.'], ['Wants before needs', 'Plan the needs first.']])
    faq = [('What does MATATAG Math 7 ask about financial plans?', 'Create a financial plan.'), ('What is the 50-30-20 rule?', 'A simple plan: about 50% for needs, 30% for wants and 20% for savings.'), ('Why save a percent of income?', 'It grows with your income and builds a habit.'), ('What should an emergency fund cover?', 'A few months of needs, like food, rent and bills.')]
    make('budgets-and-financial-plans', 6, 'Number and Algebra', 'Grade 7: Number and Algebra',
         'Create a financial plan.',
         'Budgets and Financial Plans', 'Budgets and Financial Plans',
         'Free Grade 7 budgeting worksheets for the DepEd MATATAG curriculum: allowance plans, saving for a goal, family budgets, percent saved and needs and wants. 100 questions with answers.',
         'Income − expenses = savings.', 'Plan needs first, then wants.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
